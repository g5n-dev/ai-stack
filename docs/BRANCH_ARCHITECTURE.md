# 分支架构与 CI 合并契约

状态：P0 迁移基线。本文同时说明目标架构、过渡期事实，以及为什么 GitHub Actions
必须保持当前的外部行为。

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

## CI 外部契约：分支更新和合并时不得变化

工作流内部可以升级为更安全的 DAG，但以下外部合同必须保持稳定：

| 场景 | 工作流名 | 精确触发器 | 稳定检查/行为 |
| --- | --- | --- | --- |
| 功能分支更新、PR 新提交 | `PR CI` | `pull_request` → `main`；`workflow_dispatch` | 必需检查 `Unit Tests` 保持同名；同一 PR 的旧运行可取消，新 SHA 必须完整重跑 |
| PR 合并或直接推送到 main | `Build and Deploy` | `push` → `main` | 构建精确代码 SHA；生产副作用必须晚于健康检查 |
| 周期性采集唤醒 | `Build and Deploy` | `0 * * * *`；`workflow_dispatch` | `cancel-in-progress: false`；cron 只表示唤醒，不表示数据游标完整 |
| 生产巡检 | `System Monitoring & Content Quality Tracking` | `0 */6 * * *`；`workflow_dispatch` | 全程只读，不生成虚构指标 |

`content`、`ops` 提交不匹配上述 push 分支，因此不会触发代码 PR CI 或递归部署。ruleset 应绑定稳定的
检查名，而不是内部 job 数量。任何修改工作流名称、触发分支、cron、`Unit Tests` 名称或并发语义的
Pull Request，都应被仓库测试直接拒绝。

## 为什么旧 Action 会是一个大 Job

旧系统把四种事实放在同一个 `main` 工作树：源代码、抓取输入、生成 Markdown 和 Hugo 输出。因此一次
定时运行必须按顺序完成“检出 main → 安装依赖 → 抓取/生成 → 构建图谱 → Hugo 构建 → 提交生成文件
→ 部署 Pages”。它不是无缘无故写成单 Job，而是由单分支持久化模型推导出的：

1. 抓取结果只有写回当前工作树才会在下次运行继续存在，所以 job 需要 `contents: write`。
2. 同一进程既生成内容又部署，模型密钥、Git 写权和 Pages 权限自然集中在一起。
3. 机器人提交生成内容后也会命中 `push main`；`[skip ci]` 和 bot actor 条件用于阻断自触发循环。
4. 多次小时任务可能重叠，`cancel-in-progress: false` 避免一个已开始写内容的运行在中途被取消。
5. 并发写同一分支会冲突，旧实现用工作树级同步和宽泛暂存解决；这在内容较少时能工作，但无法证明
   无丢失，也扩大了误删和密钥泄漏半径。
6. 小时 cron 是低成本调度器，不保存 crawler cursor；GitHub 排队、超时或失败都可能造成间隔，因此
   它只能是唤醒信号。

所以迁移不能只“改几行 YAML”。如果先删除 `[skip ci]` 或 bot 防循环，却仍让旧 job 写 `main`，会产生
递归运行；如果先保护 `main` 禁止机器人写入，却没有切换内容账本，内容刷新会停止；如果先启用新 writer
而未冻结旧 writer，则两个系统会争用不同事实源。

## 新 Action 保持外壳，替换内部信任模型

`Build and Deploy` 仍保留原工作流名、三个触发入口和并发组，但内部改为单一可信协调 DAG：

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

这里的“不改变 CI 流程”指外部触发、检查名和开发者合并体验不变，不是继续保留旧系统的危险内部实现。
功能分支每次更新仍触发 `PR CI`；合并到 `main` 后仍触发 `Build and Deploy`；小时任务仍按原 cron 唤醒；
只是内部增加可验证的权限边界和失败传播。

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

## 运维核对

- PR 分支更新后，GitHub 上显示 `PR CI / Unit Tests`，名称未变化。
- 合并到 `main` 后，显示 `Build and Deploy`，触发来源仍为 push。
- 小时运行仍使用 `0 * * * *`，六小时巡检仍使用 `0 */6 * * *`。
- `main` 不接受数据 writer；`content` 与 `ops` 不触发代码部署。
- 页面公开真实 build SHA、content SHA、最近健康刷新时间和来源降级状态。
- 任何发布失败都停在明确状态，不以空列表、原始对象或通知成功伪装整体成功。

更细的 job 权限、artifact 复验和 release 状态说明见
[GitHub Actions 信任模型](architecture/ci-trust-model.md)；CLI 与迁移参数见
[统一流水线 CLI](architecture/pipeline-cli.md)。
