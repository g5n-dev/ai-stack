# GitHub Actions 信任模型

状态：当前生产实现。本文解释 `.github/workflows/*.yml` 中已经生效的 job、权限和证据链；仓库级 ruleset 与 Environment 的实际开关仍应在 GitHub Settings 中单独核验。

## 信任目标

AI Stack 是静态博客，但生产链同时处理外部内容、模型密钥、Git 写入和 Pages 发布。最小安全目标是：

1. 外部内容和跨 job handoff 默认不可信，先验证再使用。
2. 模型密钥、Git 写权与 Pages 写权不进入同一个 job。
3. 只发布一个精确、可重建、已在生产验证的 Git SHA。
4. 外部通知只能发生在生产验证之后。
5. 恢复只能选择有留存验证证据的历史版本。

## 触发契约

- Pull Request 运行 `PR CI / Unit Tests`，只读验证测试、内容固定点和交付构建。
- `main` push 走快速发布，不采集、不调用模型。
- `17 * * * *` 和手动 `refresh_data=true` 运行完整刷新。
- `41 * * * *` 运行只读生产状态巡检。
- 删除和生产恢复使用独立手动工作流，不是发布链的隐藏旁路。

## 已接入的协调 DAG

```text
refresh → validate → persist → build → deploy → production-verify → notify
```

| Job | Git / Pages 权限 | 机密 | 可产生的副作用 |
| --- | --- | --- | --- |
| `refresh` | `contents: read` | 完整刷新时的模型与可选搜索配置 | 只产生 refresh artifact |
| `validate` | `contents: read` | 无 | 只产生 validated artifact |
| `persist` | `contents: write` | 无模型/渠道密钥 | CAS 写入 `blog`、`data` 白名单 |
| `build` | `contents: read` | 公开 IndexNow ownership variable | Pages artifact、release marker/proof |
| `deploy` | `pages: write`、`id-token: write` | 无模型/渠道密钥 | 切换 GitHub Pages |
| `production-verify` | `contents: read` | 无 | 线上烟测与 90 天生产验证回执 |
| `notify` | `contents: read` | 可选搜索索引配置 | 生产验证后通知搜索索引 |

顶层权限为空。job 通过 `needs` 只接收必要输出，Git 写入与 Pages 写入不会同时存在。可选社交发布器在 `config/publisher.yaml` 中默认关闭，不应把搜索索引通知描述成社交渠道发布回执。

## Artifact 复验

`refresh` 输出被视为不可信。消费者使用 `artifact_guard.py` 校验并安全解包，包括：

- artifact manifest 与逐文件 SHA-256；
- 路径白名单、文件数量、单文件和总大小；
- 拒绝 symlink、hardlink、设备文件、可执行文件和重复路径；
- JSON/Markdown 结构、UTF-8 与密钥特征；
- 精确 `base_sha` 和允许的数据根。

`validate` 在无模型密钥、无写权限的 runner 上重建 lineage、质量 manifest、趋势和图谱，再生成独立 validated handoff。`persist` 不信任生产者声明，仍再次验证 artifact；只显式复制和暂存白名单路径。

## CAS 写入与固定点

`persist` 检出当前 `main`，首先要求 HEAD 等于 `refresh` 记录的 base SHA。`git_cas_writer.py` 只允许指定根与文件模式；远端不再等于 expected base 时失败，不 rebase、reset、force push 或覆盖赢家。

`build` 随后检出 `persisted_sha`，重新执行确定性派生链和 CSS 构建，并要求工作树零差异。这证明“被持久化的内容”与“将要发布的静态资产”来自同一个固定点。

## Release marker、生产验证与回执

Hugo 与 Pagefind 构建完成后，`release_marker.py` 创建 `ai_stack_release_v1.json`，绑定精确 SHA、release ID、内容质量、lineage、趋势与图谱摘要。`release_guard.py` 再验证公开树、路由、文件类型和体积预算，防止把意外文件或不完整代际上传到 Pages。

部署后，`production_smoke.py` 等待缓存收敛并核对线上 SHA、release ID、关键页面和数据。成功才上传 `verified-release-<sha>`，保留 90 天；`notify` 依赖该 job，因此不会为未上线或烟测失败的版本发搜索通知。

这个回执只证明“精确版本曾通过生产烟测”。它不证明每小时调度都产生新文章，也不等同于 7 天 SLO 报表。静态博客的日常可靠性由小时巡检、Actions 历史和回执共同覆盖，无需常驻监控服务。

## 生产巡检

`monitoring.yml` 顶层同样为 `permissions: {}`，唯一 job 只有 `contents: read`。它每小时第 41 分钟读取 `main` SHA/提交时间与线上 marker：

- SHA 分歧超过 3 小时失败；
- 生产 release 超过 12 小时未更新失败；
- 网络、schema、版本或时间异常均失败关闭。

监控只读，不尝试自动修 Git 历史、重跑模型或放宽阈值。

## 已验证版本恢复

`production-recovery.yml` 的授权阶段要求：目标是完整 40 位小写 SHA、属于 `main` 历史、存在未过期 `verified-release-<sha>`，且证据来自成功的 `deploy.yml / production-verify`。通过后才重建并部署目标 SHA，最后再次执行生产烟测。

这不是 `git reset`。恢复不会强推、改写分支或回退运维事实，只把一个已经验证过的快照重新发布。

## 独立删除路径

`delete-post.yml` 把只读分析/模型阶段与 writer 分开。writer 复验带摘要的 artifact，只在显式执行和受保护环境条件满足时写入，并重建质量、lineage、趋势和图谱；完成后触发正常部署并等待结果。删除不能借用发布 job 绕过来源和派生数据门禁。

## 仓库级设置核对

workflow 文件无法单独证明 GitHub Settings 已启用。维护者仍需核对：

- Actions 默认权限为只读，禁止 Actions 审批 Pull Request；
- `main` 禁止删除与 force push，并要求 `PR CI / Unit Tests`；
- `github-pages`、`production-recovery` 和删除环境按风险设置审批；
- 第三方 action 固定到已审查的完整 commit SHA；
- 真实密钥只存在于 Secrets，不进入 Variables、artifact、日志、截图或文档。

当前分支与恢复契约见 [分支架构](../BRANCH_ARCHITECTURE.md)。实验性 orphan 账本 CLI 见 [pipeline-cli.md](pipeline-cli.md)，它不是当前 Actions 的生产协调器。
