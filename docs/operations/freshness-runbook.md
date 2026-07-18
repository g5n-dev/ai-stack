# 数据新鲜度排障手册

这是一份面向静态博客的轻量手册。AI Stack 不建设独立监控服务：每 6 小时由 GitHub Actions 检查线上与仓库数据是否在 **12 小时**阈值内，长期运行状态直接查看 Actions 历史与 README 徽章。

## 先看三处证据

1. **System Monitoring & Content Quality Tracking** 的最新运行状态。
2. 失败运行的 **Actions Summary**：图谱和趋势分别显示仓库/线上状态、生成时间与文章数。
3. 最近一次 **Build and Deploy** 中首个失败步骤。

不要把“没有新增文章”直接判断为故障。全历史 URL 去重后，本轮候选全部已存在是正常结果。

## 决策顺序

| 首个失败阶段 | 含义 | 首要动作 |
| --- | --- | --- |
| Run crawler | 采集或模型处理未完成 | 查看来源级超时、候选数和脱敏错误类型 |
| Build historical content quality manifest | 内容质量拒绝新增/变更文章 | 定位 manifest 原因，修生成器或透明归档 |
| Verify historical repair fixed point | 历史修复发生非预期回退 | 运行本地 `--check`，不要直接提交计划变更 |
| Build/Verify tag graph 或 STACK trends | 派生数据 schema、分片或哈希异常 | 重建对应资产并运行验证器 |
| Build Hugo / Build Pagefind | 模板、站内链接或搜索 catalog 异常 | 本地 clean build，修内容或模板 |
| Commit generated data | 没有变化或写入冲突 | 无变化是成功；冲突时同步 `main` 后重跑，禁止 force push |
| Upload artifact / Deploy to GitHub Pages | Pages 发布失败 | 检查 Pages 设置、权限和 artifact，不重新抓取内容 |
| Verify local and live graph/trend freshness | 线上新鲜度或完整性失败 | 比较仓库与线上 `generated_at`、hash 和部署提交 |

## 采集失败

1. 查看 `Run crawler` 是否真正失败，而不是成功但新增数为零。
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

图谱：

```bash
python3 scripts/verify_graph.py --assets-only --public-dir blog/static
```

趋势：

```bash
python3 scripts/verify_stack_trends.py \
  --root blog/static/data/stack-trends \
  --verify-hashes
```

错误通常来自索引与分片 path、bytes、sha256 或 schema 不一致。必须通过生成器重建，不能手工修改 JSON 绕过校验。

## 写入冲突

生成任务以失败关闭方式保护 `main`。如果推送前远端发生变化：

1. 确认新提交来自人工 PR 还是另一轮生成任务。
2. 让失败运行结束，不执行 force push。
3. 在最新 `main` 上重新触发 `refresh_data=true`。
4. 再次确认生成资产和 Hugo/Pagefind 构建通过。

## Pages 部署失败或线上仍是旧内容

1. 确认 Build and Deploy 对应最新 `main` 提交。
2. 检查 Upload artifact 与 Deploy to GitHub Pages 两步。
3. 直接访问：
   - `https://ai-stack.site/data/tag-graph/index.json`
   - `https://ai-stack.site/data/stack-trends/index.json`
4. 对比仓库与线上 `generated_at`；如果仓库新、线上旧，问题在构建/部署而非采集。
5. 样式问题再比较 JS/CSS 哈希和浏览器缓存，不重跑模型生成。

## 线上新鲜度失败

- **仓库和线上都旧**：最近完整刷新没有产生或提交有效数据，向前追溯 scheduled Build and Deploy。
- **仓库新、线上旧**：Pages artifact 或部署链路问题。
- **生成时间新但 hash 错**：索引与分片代际混用或资产不完整，重新构建并部署。
- **网络/HTTP 错误**：先确认站点和具体资源可访问，不把传输故障误判为数据陈旧。

12 小时阈值已经为 GitHub 计划任务延迟留出余量。不要通过持续放宽阈值掩盖停止更新。

## 手动恢复

```bash
gh workflow run deploy.yml \
  --repo g5n-dev/ai-stack \
  -f refresh_data=true
```

随后等待 Build and Deploy 成功，再手动运行监控：

```bash
gh workflow run monitoring.yml --repo g5n-dev/ai-stack
```

恢复完成的证据是：最新部署绿色、监控绿色、线上两个索引在 12 小时内、关键页面可正常下钻；不是单纯“工作流启动了”。

## 安全边界

- GitHub Actions 日志只写布尔状态、计数、错误类别、运行链接和公开资源 URL。
- 密钥只存在于本地 `.env` 或 GitHub Actions Secrets。
- 诊断截图先裁掉终端历史、浏览器自动填充和请求头。
- 疑似泄漏时先撤销/轮换，再提交脱敏报告。
- 不在监控中新增数据库、持久化日志平台或常驻进程。
