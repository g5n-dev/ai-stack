# AI Stack 部署指南

AI Stack 使用 Hugo、Pagefind、GitHub Actions 与 GitHub Pages 发布 `https://ai-stack.site/`。生产系统不依赖数据库、消息队列或常驻服务；内容、质量清单、图谱和趋势快照都保存在仓库中。

## 1. 两条部署路径

| 触发 | 是否刷新数据 | 主要用途 |
| --- | --- | --- |
| Push 到 `main` | 否 | 发布已经审查的代码、样式与静态快照 |
| 每小时第 17 分钟 | 是 | 采集、生成文章、重建质量清单/图谱/趋势并发布 |
| 手动触发 | 可选 | 故障恢复、验证配置或立即刷新 |

生产入口是 [`.github/workflows/deploy.yml`](./.github/workflows/deploy.yml)，工作流名称为 **Build and Deploy**。独立新鲜度监控位于 [`.github/workflows/monitoring.yml`](./.github/workflows/monitoring.yml)。

## 2. 前置条件

- 公共 GitHub 仓库，默认分支为 `main`。
- GitHub Pages 的 Source 设为 **GitHub Actions**。
- 自定义域名已经解析到 GitHub Pages。
- 一个兼容 Anthropic Messages 请求结构的模型端点，仅在完整数据刷新时需要。

只发布现有静态站点不需要模型密钥。浏览站点或本地启动 Hugo 也不会调用模型。

## 3. GitHub Actions Secrets

在仓库 **Settings → Secrets and variables → Actions** 中配置：

| 名称 | 必需 | 用途 |
| --- | --- | --- |
| `ANTHROPIC_AUTH_TOKEN` | 完整刷新必需 | 模型端点认证令牌 |
| `ANTHROPIC_BASE_URL` | 完整刷新必需 | Anthropic Messages 兼容基础地址 |
| `ANTHROPIC_MODEL` | 建议 | 显式指定模型 ID |
| `SEARXNG_BASE_URL` | 可选 | 自建搜索兜底地址 |
| `BING_INDEXNOW_API_KEY` | 可选 | IndexNow 专用公开 ownership key；8–128 位字母、数字或连字符 |
| `GOOGLE_INDEXING_API_KEY` | 可选 | Google 索引通知认证信息 |
| `GOOGLE_INDEXING_API_URL` | 可选 | Google 索引通知地址 |

`BING_INDEXNOW_API_KEY` 按 IndexNow 协议会作为站点根目录下的公开文本文件发布，用于证明域名控制权；它不是保密令牌，必须单独生成，且不可复用模型、搜索、GitHub 或其他服务的敏感凭据。工作流会在写入文件名及提交通知前校验格式。

使用明显占位符准备配置：

```env
ANTHROPIC_AUTH_TOKEN=replace_with_your_token
ANTHROPIC_BASE_URL=https://llm.example.com/anthropic
ANTHROPIC_MODEL=replace_with_your_model_id
```

不要把真实值写入 `.env.example`、README、Issue、PR、截图或 Actions 日志。疑似泄漏时先轮换，再提交脱敏诊断信息。

## 4. GitHub Pages 与域名

1. 打开仓库 **Settings → Pages**。
2. 在 **Build and deployment** 中选择 **GitHub Actions**。
3. 在 **Custom domain** 中填写 `ai-stack.site`。
4. DNS 按 GitHub Pages 当前提示配置 A/AAAA 或 CNAME 记录。
5. DNS 生效后开启 **Enforce HTTPS**。

生产构建显式使用：

```bash
cd blog
hugo --baseURL "https://ai-stack.site/" --minify --cleanDestinationDir
```

不建议在文档中复制固定 IP；以 GitHub Pages 设置页和官方文档为准，避免地址变化后留下陈旧配置。

## 5. 首次发布

代码通过 PR 合并到 `main` 后会自动执行 push 发布路径：

1. 安装固定版本的 Python、Node.js 与 Hugo。
2. 验证已经提交的内容质量 manifest 和历史修复固定点。
3. 验证图谱与趋势分片。
4. 构建 Hugo 与 Pagefind 搜索目录。
5. 上传 Pages artifact 并部署。
6. 按配置通知搜索引擎。

push 路径不会执行采集和模型处理，因此代码/样式变更可以快速、确定性上线。

## 6. 定时完整刷新

计划任务在 UTC 的每小时第 17 分钟触发。它会：

1. 采集已启用来源，并在模型调用前做全历史 URL 去重。
2. 生成或修复 Markdown 文章。
3. 校验来源契约、正文结构、标签与历史质量固定点。
4. 重建 `blog/data/content_quality.json`。
5. 重建 Graph JSON v2 与 STACK 趋势分片并校验哈希。
6. 构建 Hugo、Pagefind 与结果 catalog。
7. 仅在生成资产有变化时提交 `[skip ci]` 数据提交。
8. 以 CAS/冲突失败关闭策略推送 `main`，随后部署已验证 artifact。

生成机器人提交不会再次触发完整 push 部署，避免递归工作流。

## 7. 手动触发

在 GitHub 页面：

1. 打开 **Actions**。
2. 选择 **Build and Deploy**。
3. 点击 **Run workflow**。
4. `refresh_data=true` 执行完整刷新；设为 `false` 只发布已提交快照。

也可以使用 GitHub CLI：

```bash
gh workflow run deploy.yml \
  --repo g5n-dev/ai-stack \
  -f refresh_data=true
```

不要在命令行参数中传递密钥；模型配置只能来自 GitHub Actions Secrets 或本地 `.env`。

## 8. 本地发布前验证

只预览静态 UI：

```bash
git clone https://github.com/g5n-dev/ai-stack.git
cd ai-stack/blog
hugo server -D
```

运行稳定发布闸门：

```bash
cd ai-stack
npm ci --ignore-scripts
npm test
python3 -m pytest -q
npm run build:css
cd blog
hugo --minify --cleanDestinationDir
cd ..
npm run build:search
```

完整检查清单见 [docs/V1_RELEASE_CHECKLIST.md](./docs/V1_RELEASE_CHECKLIST.md)。

## 9. 线上验证

部署完成后至少检查：

```bash
curl --fail --silent --show-error --head https://ai-stack.site/
curl --fail --silent --show-error https://ai-stack.site/data/tag-graph/index.json
curl --fail --silent --show-error https://ai-stack.site/data/stack-trends/index.json
```

浏览器烟测：

- 首页与归档能看到文章和真实更新时间。
- 搜索可以按关键词、来源和标签返回结果。
- 趋势筛选会改变数据，可下钻文章和图谱。
- 图谱三种模式可切换，搜索与节点详情可用。
- 移动端没有菜单、侧栏或抽屉遮挡。

## 10. 新鲜度监控

**System Monitoring & Content Quality Tracking** 每 6 小时第 23 分钟运行：

- 校验仓库与线上 Graph JSON v2 的生成时间和文章数。
- 校验趋势分片哈希、字节数与线上生成时间。
- 使用 12 小时阈值区分正常与陈旧数据。
- 通过步骤名称与诊断摘要区分内容、派生数据、部署和线上新鲜度故障；长期状态直接查看 Actions 历史与 README 徽章。

监控失败不应通过放宽阈值解决。先判断是计划任务未启动、采集/质量闸门失败、推送冲突、部署失败还是线上缓存/资源问题。

按步骤处理见 [新鲜度排障手册](./docs/operations/freshness-runbook.md)。

## 11. 常见故障

### 页面仍是旧样式

1. 确认改动已合并到 `main`，不是只存在本地分支。
2. 查看最新 Build and Deploy 是否包含该提交。
3. 检查 Pages deployment job 是否成功。
4. 比较线上与本地 CSS/JS 哈希，必要时强制刷新浏览器缓存。
5. 检查 Hugo 模板使用 `relURL`，资源路径没有写死为本机或错误子路径。

### 图谱或趋势内容加载失败

1. 直接访问两个 `index.json`，确认 HTTP 200 与 JSON 格式。
2. 执行 `scripts/verify_graph.py` 和 `scripts/verify_stack_trends.py`。
3. 检查分片 path、bytes 与 sha256 是否和索引一致。
4. 确认 Deploy 上传的是本次构建后的 `blog/public`。

### 定时任务没有新文章

“成功运行但没有新增”可能是正常去重结果。检查 Actions Summary 中的候选数、重复数、来源错误和质量闸门，而不是只看提交数量。

### 生成提交推送失败

生产任务故意在并发冲突时失败关闭，不会强制覆盖 `main`。先同步最新主分支，确认人工改动与生成资产边界，再重新触发完整刷新。

### Secrets 无效

日志只能确认变量是否存在，不能打印值。轮换认证令牌后重新运行手动完整刷新；不要在 Issue 中粘贴响应头或请求命令。

## 12. 回滚

- 代码/样式回滚：通过新的 PR revert 对应提交，再让 push 发布路径部署。
- 生成数据回滚：优先修复生成器并重建，不直接手改清单或分片。
- 内容安全事件：使用 **Delete Post** 工作流的 dry run 核对，再执行删除与派生数据重建。
- 密钥事件：先轮换与撤销，再处理仓库历史和日志暴露面。

生产操作以 Actions 运行记录、PR CI 与 [v1.0 发布清单](./docs/V1_RELEASE_CHECKLIST.md) 为最终证据。
