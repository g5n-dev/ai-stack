# AI Stack v1.0 发布清单

本清单把 `v1.0 · 可持续情报闭环` 的完成条件转成可重复执行的发布闸门。它适用于功能 PR、内容管线变更和正式版本发布。

## 1. 变更边界

- [ ] PR 只包含本次目标相关文件，没有意外生成物或个人环境配置。
- [ ] 已说明是否影响内容格式、Graph JSON、趋势分片、搜索索引或 GitHub Actions 权限。
- [ ] 数据迁移具有固定点检查；失败时不会覆盖已验证的历史文章。
- [ ] 不引入数据库、消息队列或常驻服务，除非方案明确说明成本与退出路径。

## 2. 内容与历史证据

```bash
python3 scripts/build_content_quality_manifest.py \
  --content-root blog/content \
  --output /tmp/content_quality.json \
  --fail-on-quarantine \
  --fail-on-structural-warning \
  --fail-on-unverified-provenance
cmp --silent blog/data/content_quality.json /tmp/content_quality.json
python3 scripts/repair_historical_content.py --check
```

- [ ] 活跃文章没有 quarantined 项或空章节。
- [ ] 来源链接、日期、标签、内容模式和转写说明完整。
- [ ] 无法恢复的历史来源保留透明归档原因，不发布推测正文。
- [ ] 质量 manifest 的 `source_tree_sha256` 与当前文章树一致。

## 3. 图谱数据与交互

```bash
python3 scripts/verify_graph.py --assets-only --public-dir blog/static
node --test tests/js/graph-runtime.test.js tests/js/test_graph_workbench.mjs
```

- [ ] 首屏只加载核心 overview，不下载全量标签图。
- [ ] community 与 focus 只请求当前可见子图；任一视图不超过 100 节点、500 边。
- [ ] focus 最多 80 条边，粒子只沿高亮路径且有明确上限。
- [ ] 1280×720 与 390×844 下控件不遮挡，触控目标不少于 44px。
- [ ] reduced-motion、页面隐藏、恢复和销毁不会留下重复动画循环。

## 4. 趋势数据与下钻

```bash
python3 scripts/build_stack_trends.py
python3 scripts/verify_stack_trends.py \
  --root blog/static/data/stack-trends \
  --verify-hashes
node --test tests/js/test_trends.mjs
```

- [ ] 24h、7d、30d 窗口均可加载，分片哈希与字节数匹配。
- [ ] 信号、来源、场景和主题筛选真实改变结果，URL 刷新后状态保持。
- [ ] 默认节点只显示主题与状态；hover/focus 展示分数、证据与来源。
- [ ] 每个趋势均可下钻到证据文章与相关图谱，并保留返回上下文。

## 5. Hugo、搜索与静态资源

```bash
npm ci --ignore-scripts
npm run build:css
cd blog
hugo --minify --cleanDestinationDir
cd ..
npm run build:search
```

- [ ] Hugo 构建成功，站点基址为 `https://ai-stack.site/`。
- [ ] Pagefind 生成 `pagefind.js`、`catalog.json` 与 catalog manifest。
- [ ] 首页、归档、搜索、标签、趋势、图谱、文章详情与 404 无资源错误。
- [ ] 共享顶部导航在所有页面保持一致。

## 6. 自动化与新鲜度

- [ ] [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) 在 PR 上通过稳定测试矩阵。
- [ ] [`.github/workflows/deploy.yml`](../.github/workflows/deploy.yml) 的 push 路径不抓取，schedule 路径在每小时第 17 分钟刷新。
- [ ] [`.github/workflows/monitoring.yml`](../.github/workflows/monitoring.yml) 每 6 小时验证仓库与线上图谱/趋势的新鲜度。
- [ ] 图谱与趋势未超过 12 小时陈旧阈值；失败步骤能定位到采集、质量、派生数据、写入或部署阶段。
- [ ] 数据生成提交使用 CAS/冲突失败关闭策略，不覆盖并发人工改动。

故障处置以 [新鲜度排障手册](./operations/freshness-runbook.md) 为准。

## 7. 安全与成本边界

- [ ] 文档、Issue、PR、日志和截图中没有真实密钥、cookie、token、私有 endpoint 或完整认证请求头。
- [ ] `.env` 未被跟踪，示例只含明显占位符。
- [ ] Actions 权限未无故扩大；第三方 Action 使用已审查的明确 major 版本。
- [ ] 静态 UI 不需要模型密钥；完整刷新产生的模型/API 用量成本已说明。
- [ ] 自托管前端依赖没有退回运行时 CDN。

## 8. 线上烟测

部署成功后逐项验证：

- [ ] [首页](https://ai-stack.site/) 能看到最新文章时间和真实统计。
- [ ] [搜索](https://ai-stack.site/search/) 可按关键词、来源和标签查到文章。
- [ ] [趋势](https://ai-stack.site/trends/?window=30d) 可筛选、hover 查看解释并双通道下钻。
- [ ] [图谱](https://ai-stack.site/scenarios/) 可切换三种模式、搜索并清除节点选择。
- [ ] 抽查文章详情：正文、标签、来源和返回路径完整。
- [ ] 关键 JS、CSS、Graph JSON 与趋势分片均为 HTTP 200，无控制台异常。

## 9. 发布收口

- [ ] PR 已关联并更新对应 Issue 的验收清单。
- [ ] PR CI 全绿后才合并到 `main`。
- [ ] Build and Deploy 成功，线上烟测通过。
- [ ] Issue 附上测试、运行与部署证据后关闭。
- [ ] 所有 v1.0 Issue 关闭后再关闭里程碑，不以“代码已写”代替“线上已验证”。
