# 数据新鲜度排障手册

这是一份面向静态博客的轻量手册。AI Stack 不建设独立监控服务：GitHub Actions 每小时第 41 分钟只读比较 `main` 与生产 release marker；版本分歧达到 **3 小时**或已部署来源证据超过 **12 小时**没有成功刷新即失败。

## 先看三处证据

1. **System Monitoring & Content Quality Tracking** 的最新运行状态。
2. 失败运行的 **Actions Summary**：查看 `status`、`refresh_as_of`、`refresh_age_hours`、`data_as_of`、`data_age_hours`、`divergence_hours`，以及线上 marker 的精确 SHA 和 release ID。公开 lineage index 的 `generated_at` 表示最近一次已部署证据刷新；marker 的 `generated_at` 表示最新合格趋势事件时间。两者都不是部署墙钟。
3. 最近一次 **Build and Deploy** 中首个失败 job；当前顺序为 `refresh → validate → persist → build → deploy → production-verify → notify`。

不要把“没有新增文章”直接判断为故障。规范 URL 去重和跨 URL 事件谱系后，本轮候选全部已存在或只是同一事件的重复观察，都可能是正常结果。

刷新日志中的候选数必须闭合：归档过滤、来源配额和文章生成各自都要有明确终态。`policy_rejected` 可以为正，但被策略拒绝的候选不能提前耗尽该来源配额；无法闭合的计数应让任务失败。

CI 会为每个启用来源请求 20–30 条轻量候选元数据，再执行归档与策略检查；只有检查通过的候选才进入每来源生成配额。扩大候选池不能扩大模型调用或掘金正文抓取配额。排障时如果来源实际返回量低于 20，应按上游 feed/访问异常处理，而不是放宽新鲜度阈值。

## 决策顺序

| 首个失败阶段 | 含义 | 首要动作 |
| --- | --- | --- |
| `refresh` | 采集或模型处理未完成 | 查看来源级超时、候选数和脱敏错误类型 |
| `validate` | artifact、lineage、内容质量或派生数据拒绝候选 | 定位首个验证器，修生成器或透明归档，不手改分片 |
| `persist` | exact-base CAS 写入冲突 | 等待当前运行结束，在最新 `main` 上重跑，禁止 force push |
| `build` | 固定点、CSS、Hugo、Pagefind 或 release guard 失败 | 本地 clean build，检查零差异与公开树门禁 |
| `deploy` | Pages 发布失败 | 检查 Pages 设置、权限和 artifact，不重新抓取内容 |
| `production-verify` | 线上 SHA/release ID 或关键资源未收敛 | 比较 marker、缓存与部署记录；烟测通过前不会通知 |
| `notify` | 已验证版本的可选索引通知失败 | 站点已经验证上线；单独修通知配置，不回滚内容 |
| `monitoring` | 线上新鲜度或版本收敛失败 | 比较 `main` SHA、marker SHA、`stale_hours` 与 `divergence_hours` |

## 采集失败

1. 查看 `refresh` 是否真正失败，而不是成功但新增数为零。
2. 按来源区分网络失败、访问限制、结构解析失败和模型调用失败。
3. 单个来源异常时保持其他来源可运行；不要为追求数量放宽正文质量门禁。
4. 如果模型认证失败，轮换或修复 Secret 后手动执行完整刷新。

严禁把认证值、cookie、私有 endpoint、完整请求头或外部响应正文复制到 Issue。

## 内容质量失败

本地复现：

```bash
python3 scripts/build_content_quality_manifest.py \
  --content-root blog/content \
  --output /tmp/content_quality.json \
  --fail-on-quarantine \
  --fail-on-structural-warning \
  --fail-on-unverified-provenance
python3 scripts/repair_historical_content.py --check
```

- `quarantined`：文章不满足公开契约，修生成器或来源恢复逻辑。
- `empty_section`：存在空标题壳，删除空节或生成有效内容。
- 来源不可恢复：转成带失败类型、原因、尝试时间与原始链接的透明归档。
- 不允许用模型推测正文填补来源证据空白。

## 派生数据失败

按发布依赖顺序验证：

```bash
python3 scripts/verify_lineage.py --verify-hashes
python3 scripts/verify_stack_trends.py \
  --root blog/static/data/stack-trends \
  --verify-hashes
python3 scripts/verify_graph.py --assets-only --public-dir blog/static
```

错误通常来自索引与分片 path、bytes、sha256 或 schema 不一致。必须通过生成器重建，不能手工修改 JSON 绕过校验。趋势还应满足 `redundant_observations = observations - unique_events`，且只有 allowlist 认可的 `same_event` 才合并。

## 写入冲突

`persist` 以失败关闭方式保护 `main`。如果 expected base SHA 已变化：

1. 确认新提交来自人工 PR 还是另一轮生成任务。
2. 让失败运行结束，不执行 force push、reset 或 rebase。
3. 在最新 `main` 上重新触发 `refresh_data=true`。
4. 再次确认 lineage、质量、趋势、图谱和 Hugo/Pagefind 固定点通过。

## Pages 部署或生产验证失败

1. 确认 `build` 检出的 SHA 等于 `persist` 输出的完整 SHA。
2. 检查 release guard、Upload Pages artifact 与 Deploy to GitHub Pages。
3. 访问 `https://ai-stack.site/ai_stack_release_v1.json`，核对 exact SHA、release ID 与产品摘要。
4. 如果 deploy 绿色但 production-verify 失败，检查缓存收敛、路由、共享顶部、CSS/JS、文章链接和数据分片。
5. 样式问题比较线上与 artifact 的 JS/CSS 哈希，不重跑模型生成。

production-verify 失败时不会生成 `verified-release-<sha>`，也不会执行搜索索引通知。

## 线上新鲜度失败

- **`main` 与线上 SHA 相同但 `refresh_age_hours` 达到 12 小时**：部署已经收敛，但完整刷新没有持久化并发布新的来源观察；向前追溯 scheduled Build and Deploy。
- **`data_age_hours` 超过 12 小时但 `refresh_age_hours` 正常**：采集发布链路健康，只是来源没有提供更新的合格事件；检查来源返回量和策略拒绝数，但不要用抓取时间覆盖真实事件时间。
- **`main` 新、线上旧且接近 3 小时**：persist 后的构建、Pages 部署或缓存收敛问题；查看首个失败 job。
- **SHA 相同但 release ID/摘要不符**：marker 与公开资产代际混用，重新构建并部署。
- **网络/HTTP 错误**：先确认站点和 marker 可访问，不把传输故障误判为数据陈旧。

3 小时收敛和 12 小时刷新阈值已经为 GitHub 计划任务延迟留出余量。不要持续放宽阈值掩盖停止更新，也不要把来源事件时间改写为抓取时间来制造“新鲜”趋势。

## 手动刷新与历史恢复

重新运行主链：

```bash
gh workflow run deploy.yml \
  --repo g5n-dev/ai-stack \
  -f refresh_data=true
```

随后可以手动运行只读监控：

```bash
gh workflow run monitoring.yml --repo g5n-dev/ai-stack
```

恢复完成的证据是：production-verify 绿色、对应精确 SHA 的 `verified-release-<sha>` 已保留、监控绿色且关键页面可正常下钻；不是单纯“工作流启动了”。需要回到历史版本时，使用 **Production Recovery**，目标必须是有未过期生产验证回执的完整 `main` 祖先 SHA。

## 是否需要 7 天 SLO 报表

对当前静态博客，它不是发布必需项。小时巡检、Actions 历史和 90 天生产验证回执已经提供可复用证据；如需周度复盘，可按需汇总部署成功率、新鲜度达标率和恢复时间，不新增数据库、日志平台或常驻报表服务，也不把 7 天窗口包装成对外可用性承诺。

## 安全边界

- GitHub Actions 日志只写布尔状态、计数、错误类别、运行链接和公开资源 URL。
- 密钥只存在于本地 `.env` 或 GitHub Actions Secrets；公开 IndexNow ownership key 使用 repository Variable。
- 诊断截图先裁掉终端历史、浏览器自动填充和请求头。
- 疑似泄漏时先撤销/轮换，再提交脱敏报告。
- 不在监控中新增数据库、持久化日志平台或常驻进程。
