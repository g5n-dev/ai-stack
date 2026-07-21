# 分支架构与 CI 合并契约

状态：当前生产事实。工作流文件和 [`DEPLOYMENT.md`](../DEPLOYMENT.md) 是最终依据；本文用于解释分支责任、稳定检查名、权限边界和恢复条件。

> 当前 v1 工作流已经覆盖内容来源门禁、历史修复固定点、跨 URL 事件谱系、内容质量、图谱/趋势派生数据、真实浏览器烟测、Hugo 与 Pagefind 交付构建。

## 当前分支事实

- `main` 同时保存代码、配置、Markdown 文章、内部/公开 lineage、质量清单、趋势与图谱静态资产。
- 功能分支通过 Pull Request 合入 `main`；本项目约定 Codex 分支使用 `codex/` 前缀。
- 当前没有生产使用的 `content` 或 `ops` orphan 分支，也不以双 SHA 构建站点。
- 机器人只能在生产工作流的 `persist` 阶段，以 expected base SHA 和路径白名单 CAS 写入 `main`；冲突直接失败，不 reset、rebase 或 force push。
- `[skip ci]` 与 bot actor 条件阻止数据提交递归触发部署；小时任务不取消正在运行的生产链。

## 稳定的 CI/CD 外部契约

| 场景 | 工作流名 | 触发器 | 稳定检查或结果 |
| --- | --- | --- | --- |
| Pull Request | `PR CI` | `pull_request` → `main`；手动 | `Unit Tests`；同一 PR 的旧运行可取消 |
| 发布与数据刷新 | `Build and Deploy` | push → `main`；`17 * * * *`；手动 | 精确 SHA 的验证、持久化、构建、部署与生产烟测 |
| 生产状态巡检 | `System Monitoring & Content Quality Tracking` | `41 * * * *`；手动 | 只读比较 `main` 与生产 release marker；3 小时分歧、12 小时陈旧阈值 |
| 安全删除 | `Delete Post` | 手动 | 只读分析与有保护的 writer 分离；重建派生数据后触发主部署 |
| 已验证版本恢复 | `Production Recovery` | 手动 | 只接受仍有生产验证回执的完整 `main` 祖先 SHA |

工作流名和 required check 名是仓库 ruleset 的外部接口。内部 job 可以演进，但不能通过改名、删除检查或增加无检查旁路规避保护。

## 当前发布协调器

生产 DAG 已经接入 `.github/workflows/deploy.yml`：

```text
refresh → validate → persist → build → deploy → production-verify → notify
```

| Job | 权限与机密 | 责任 |
| --- | --- | --- |
| `refresh` | `contents: read`；完整刷新时读取模型密钥 | 在精确 base SHA 上采集/整理，输出受保护 handoff |
| `validate` | `contents: read`；无模型密钥 | 复验 handoff，重建 lineage、质量、趋势和图谱，输出 validated handoff |
| `persist` | `contents: write`；无模型密钥 | 只替换白名单路径，以 exact-base CAS 推送 `main` |
| `build` | `contents: read`；无业务密钥 | 检出 persisted SHA，证明固定点，构建 Hugo/Pagefind 与 release marker |
| `deploy` | `pages: write`、`id-token: write` | 只部署已 guard 的 Pages artifact |
| `production-verify` | `contents: read` | 比对线上 SHA/release ID，保留 90 天 `verified-release-<sha>` |
| `notify` | `contents: read`；可选索引通知配置 | 只在生产验证成功后通知搜索索引 |

顶层 `permissions: {}`。没有 job 同时持有模型密钥和 Git 写权，也没有 job 同时持有 Git 写权和 Pages 写权。跨 job artifact 必须复验摘要、路径、类型、大小、schema 和密钥特征；writer 禁止 `git add -A`。

## 数据与去重边界

主流程先按规范 URL 去重，再仅使用有限的原始来源证据构建跨 URL 谱系；生成文章正文不作为原创性证据。界面对外描述本站最早观测、疑似源头、转载、衍生、同事件和仅相关，不声称绝对原创。趋势按稳定 `event_id` 计算 `unique_events`，只合并 allowlist 认可的 `same_event`，并把多来源重复观察记录为 `redundant_observations`。

生成数据依次通过：

```text
lineage → content quality → trends → graph
```

任何分片、哈希、来源契约或固定点不一致都会失败关闭；不能靠手改 JSON 或放宽阈值继续发布。

## 精确发布与恢复

`build` 绑定 `persist` 输出的完整 SHA，release marker 同时绑定质量、lineage、趋势和图谱摘要。Pages 部署完成后，`production-verify` 必须确认线上 marker 和关键资源属于同一 release；只有成功版本才留下可恢复回执并进入 `notify`。

`Production Recovery` 不接受分支名、短 SHA 或任意旧提交。目标必须是完整 40 位 `main` 祖先 SHA，并存在未过期、来源为成功 `deploy.yml` 的 `verified-release-<sha>`。恢复仍会重建、guard、部署并重新烟测，不移动或重写 Git 历史。

## 未来 orphan 账本方向（未启用）

仓库保留一套可选迁移 CLI，用于研究将代码、内容和运维事实拆成独立账本。以下是目标描述，不是当前生产事实：

- `main`：只保存代码、锁文件、配置、模板、测试和架构文档。
- `content`：orphan 内容账本，保存 canonical 事件、文章修订和有限证据。
- `ops`：orphan 运维事实账本，保存预算、release sequence、outbox 和渠道回执。

启用该方向需要新的分支、ruleset、Environment、影子构建、CAS 身份和受控切换窗口。当前工作流不会读取这些分支，当前发布也不应宣称双 SHA、release sequence 或社交渠道 exactly-once 已生效。实验 CLI 的契约见 [pipeline-cli.md](architecture/pipeline-cli.md)。

## 合并与运维核对

1. 功能分支每次更新后，确认 `PR CI / Unit Tests` 针对最新 SHA 运行并通过。
2. 合并到 `main` 后，确认 `Build and Deploy` 显示完整七段 DAG，而非旧的单 job。
3. 数据提交仅来自 `persist` 白名单，远端 SHA 竞争时运行必须失败。
4. 发布成功后确认 `production-verify` 绿色，并存在对应 SHA 的生产验证回执。
5. `System Monitoring & Content Quality Tracking` 每小时第 41 分钟只读巡检；异常通过 Actions Summary 定位，不修改历史或阈值掩盖。
6. 删除使用独立工作流；密钥事件先撤销/轮换，再处理历史和日志暴露面。

更细的权限和 artifact 复验见 [CI 信任模型](architecture/ci-trust-model.md)，操作命令见 [部署指南](../DEPLOYMENT.md)。
