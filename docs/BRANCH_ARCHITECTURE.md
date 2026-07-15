# 分支架构与 CI 合并契约

状态：P0 迁移基线，目标协调器尚未启用。本文同时说明目标架构、过渡期事实，以及现行
GitHub Actions 的可靠性边界。

> 合并边界：本次可靠性修复修改 `deploy.yml` 与 `monitoring.yml`，只处理非整点唤醒、增量数据写入、
> fail-closed 图谱构建和真实线上新鲜度巡检。
> 目标协调 DAG 尚未接入 GitHub Actions。新的 CAS、预算、artifact guard、release health 和 outbox
> 代码只是待切换能力，不能据此宣称生产权限隔离、安全删除或双 SHA 发布已经生效。`ci.yml` 仅在
> 原 `Unit Tests` job 内加入本次数据新鲜度与 workflow 语义回归，`delete-post.yml` 保持既有字节契约。

## 结论

目标分支职责如下：

- `main`：只保存代码、锁文件、配置、模板、测试和架构文档；不再追加生成文章或构建产物。
- `content`：orphan 内容账本，保存 canonical 当前态、事件、修订、短证据快照、路由和有限媒体。
- `ops`：orphan 运维事实账本，保存预算、release sequence、outbox、发布回执和备份记录。
- 功能分支：通过 Pull Request 合并到 `main`，默认使用 `codex/` 前缀。

`content` 和 `ops` 没有共同祖先，也不与 `main` 相互 merge。它们只能由对应的 CAS writer
在预期父 SHA 上 fast-forward 更新。任何常规路径都禁止 reset、rebase、force push、删除分支、
GC/prune 和历史重写。

过渡期内，远端 `main` 仍含历史生成内容，旧发布流程仍可能向它写入。只有完成影子运行、完整构建、
稳定期、备份和最终增量同步后，才会冻结旧 writer 并切换到上述目标状态。在切换前启用阻止旧 writer
的分支规则会直接中断现网，因此仓库规则和新工作流必须在同一个受控切换窗口生效。

## CI 外部契约：稳定名称、触发器与失败语义

当前行为如下：

| 场景 | 工作流名 | 精确触发器 | 稳定检查/行为 |
| --- | --- | --- | --- |
| 功能分支更新、PR 新提交 | `PR CI` | `pull_request` → `main`；`workflow_dispatch` | 单 job `unit-tests`，显示名 `Unit Tests`；同一 PR 的旧运行可取消 |
| PR 合并或直接推送到 main | `Build and Deploy` | `push` → `main` | 单 job `build-and-deploy`、bot-push 过滤；直接验证并部署已评审快照，不运行抓取或改写生成数据 |
| 周期性采集唤醒 | `Build and Deploy` | `17 * * * *`；`workflow_dispatch` | `cancel-in-progress: false`；候选池历史去重后生成、校验、提交并部署 |
| 生产巡检 | `System Monitoring & Content Quality Tracking` | `23 */6 * * *`；`workflow_dispatch` | 只读校验 main 与线上 v2 图谱时间、文章数和 JSON 契约，异常非零退出 |

`content`、`ops` 提交不匹配上述 push 分支，因此不会触发代码 PR CI 或递归部署。测试继续以 SHA-256
锁住未改动的 `delete-post.yml`；`ci.yml` 保留同名 required job 并运行新增回归，对数据生成和巡检
工作流则锁定触发器、最小权限、顺序、白名单与 fail-closed 语义。

## 为什么旧 Action 会是一个大 Job

旧系统把四种事实放在同一个 `main` 工作树：源代码、抓取输入、生成 Markdown 和 Hugo 输出。因此一次
定时运行按顺序完成“检出 main → 安装依赖 → 抓取候选 → 历史去重 → 生成文章 → 构建并验证图谱
→ 白名单提交生成数据 → Hugo 构建 → 部署 Pages”。它仍是单 Job，是由单分支持久化模型推导出的：

1. 抓取结果只有写回当前工作树才会在下次运行继续存在，所以 job 需要 `contents: write`。
2. 同一进程既生成内容又部署，模型密钥、Git 写权和 Pages 权限自然集中在一起。
3. 机器人提交生成内容后也会命中 `push main`；`[skip ci]` 和 bot actor 条件用于阻断自触发循环。
4. 多次小时任务可能重叠，`cancel-in-progress: false` 避免一个已开始写内容的运行在中途被取消。
5. 并发写同一分支会冲突；现行快速修复禁止冲突后 reset/rebase，push 被拒时直接失败并等待下一轮，
   同时只暂存文章与图谱目录，避免静默丢数据或把无关文件带入机器人提交。
6. 小时 cron 是低成本调度器，不保存 crawler cursor；GitHub 排队、超时或失败都可能造成间隔，因此
   它只能是唤醒信号。

所以迁移不能只“改几行 YAML”。如果先删除 `[skip ci]` 或 bot 防循环，却仍让旧 job 写 `main`，会产生
递归运行；如果先保护 `main` 禁止机器人写入，却没有切换内容账本，内容刷新会停止；如果先启用新 writer
而未冻结旧 writer，则两个系统会争用不同事实源。

## 目标 Action 信任模型（尚未接入）

后续独立迁移应保留 `Build and Deploy` 的工作流名、三个触发入口和并发组，再把内部切换为单一可信
协调 DAG：

```text
crawl
  → validate-discovery
  → persist-discovery(content CAS)
  → reserve-budget(ops CAS)
  → generate(no Git write)
  → validate-result
  → persist-result(content CAS)
  → build(code_sha + content_sha)
  → deploy
  → production-health
  → persist-healthy-release(ops CAS)
  → publish-outbox
  → persist-receipt(ops CAS)
```

以上 DAG 是已实现但未接线的目标，不描述本 PR 合并后的 GitHub Actions 事实。切换它会改变 job/check、
DAG、权限、Environment 和副作用顺序，因此必须在 ruleset、环境审批和回滚窗口就绪后单独评审。

关键边界：

- 有模型密钥的 job 只有读权限；content writer 无模型密钥。
- publisher 有渠道密钥但无 Git 写权；receipt writer 无渠道密钥。
- 跨 job artifact 一律视为不可信，并复验路径、类型、大小、数量、摘要、schema、密钥特征和最终 DOM。
- writer 只暂存白名单目录，并以 expected SHA 执行 CAS；冲突后重新读取、确定性归并，不改写历史。
- 每次部署固定 `code_sha + content_sha + schema_version + release sequence + artifact_digest`。
- 只有生产健康后才推进健康 release、消费 outbox 和持久化回执。
- 外部发送是 at-least-once；超时结果进入 `UNKNOWN`，不得盲目重发。

## 分支更新与合并规程

### 代码分支

1. 从已知 `main` SHA 创建功能分支。
2. 更新分支只允许普通提交；需要吸收远端变化时使用可审计 merge，不重写已共享历史。
3. PR 的每个新 SHA 都必须运行同名 `PR CI`，至少保持 `Unit Tests` 这一稳定 required check。
4. CI 通过并完成评审后合并；合并提交触发原名 `Build and Deploy`。
5. 自动化身份不得审批自己的 PR，也不得绕过 ruleset。

### 数据分支

1. writer 检出 `content` 或 `ops` 的精确父 SHA。
2. 验证 artifact 与业务 schema，只生成白名单路径。
3. 本地提交后，以远端仍等于预期父 SHA 为条件 fast-forward push。
4. 如果 CAS 失败，丢弃尚未发布的临时工作目录，读取新 HEAD，按稳定 ID 合并后重算；绝不覆盖赢家。
5. 同一输入重跑应得到 0 新页面、0 模型调用、0 Git 变化和 0 重复通知。

`main`、`content`、`ops` 之间不做普通内容合并。站点构建使用 Hugo mount 从精确 `content_sha` 读取内容，
而不是把内容复制回代码分支。

## 安全切换顺序

以下步骤必须按顺序完成，不能用一次大合并替代：

1. 验证原脏工作区可逐字节恢复，并验证本地与不可变 release 备份。
2. 将现有内容原样种入 `content`，建立独立 `ops`，不同时去重、改 URL 或升级图谱。
3. 连续完成至少 24 次影子运行和 3 次完整影子构建；文章数、路由、外链和逐文件哈希一致。
4. 冻结旧 workflow，等待所有旧运行结束，再做一次最终增量同步。
5. 在同一切换窗口启用 Actions 默认只读、ruleset、Environment 审批和新协调 workflow。
6. 用固定双 SHA 部署，执行生产健康检查；失败时不推进健康 release。
7. 稳定运行至少 7 天后，才允许每批最多 100 篇的历史精确 URL 去重。
8. 最后才从 `main` HEAD 移走生成内容；不清理既有 Git 历史。

只要任一门禁缺证据，迁移和去重命令必须 fail closed。时间门禁不能靠伪造时间戳或重复 run ID 补齐。

## 回滚

回滚不是回退数据分支，也不是强推旧提交。应分配更高的 release sequence，重新部署已验证的旧
`code_sha + content_sha` 组合。这样预算预留、发送回执和 `UNKNOWN` 状态不会倒退，恢复站点也无需
重新调用模型。

只有密钥泄漏、PII 或法律删除请求可以进入独立 break-glass 删除流程；该流程默认 dry-run、绑定预期
源 SHA、备份 ID 和变更上限，并要求受保护 Environment 审批。

## 当前 PR 运维核对

- PR 分支更新后，GitHub 上显示 `PR CI / Unit Tests`，名称未变化。
- 合并到 `main` 后，显示 `Build and Deploy`，触发来源仍为 push。
- 小时运行使用 `17 * * * *`，六小时巡检使用 `23 */6 * * *`，避开整点拥塞窗口。
- `delete-post.yml` 的 SHA-256 仍与基线一致；`ci.yml` 保持同名 required job 并加入数据可靠性回归。
- 图谱失败不再复用旧数据；远端冲突不再 `reset --hard` 后假成功；巡检不再读取废弃的 `gh-pages`。
- `content` 与 `ops` 不触发代码部署，但旧 workflow 仍可能把生成内容写回 `main`。
- 仓库 ruleset、默认只读 Actions 权限和受保护 Environment 未实际启用前，不宣称强推/删除防护或
  权限分离已经落地。

更细的 job 权限、artifact 复验和 release 状态说明见
[GitHub Actions 信任模型](architecture/ci-trust-model.md)；CLI 与迁移参数见
[统一流水线 CLI](architecture/pipeline-cli.md)。
