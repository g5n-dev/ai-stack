# GitHub Actions 信任模型与发布状态机

状态：P0 设计基线。此文档解释每个触发器、权限和门禁存在的原因。

## 不变的触发契约

- 功能分支更新后，关联 `main` 的 Pull Request 必须重新执行同一组必需检查。
- Pull Request 通过必需检查并合并到 `main` 后，自动进入精确版本构建与部署。
- 定时任务只唤醒协调流程；它不代表采集游标已经完整推进。
- 手工触发保留给恢复、补抓和 dry-run；不能绕过验证、预算或 release sequence。
- `content`、`ops` 的数据提交不触发代码 PR CI，避免机器人提交形成递归运行。

检查名称应保持稳定，仓库 ruleset 直接绑定这些名称。工作流内部可以演进，但不得通过改名、
删除检查或增加无检查的旁路来规避保护规则。

## 为什么采用一个协调 workflow

协调 workflow 用 `needs` 表达以下有向无环图：

```text
crawl
  -> validate-discovery
  -> persist-discovery
  -> reserve-budget
  -> generate
  -> validate-result
  -> persist-result
  -> build-exact-revision
  -> deploy
  -> production-health
  -> publish-outbox
  -> persist-receipt
```

这里不采用多层 `workflow_run`。后者把触发方与被触发方的权限、代码版本和 artifact 来源拆开，
容易让低权限运行生成的数据被高权限运行误当作可信输入。单一协调器仍将每个 job 隔离在独立 runner，
但能把输入摘要、父提交和失败传播放在同一条可审计状态链上。

## 权限与密钥边界

顶层 `permissions` 为只读或空；需要写能力的 job 单独声明。任何 job 都不得同时拥有模型密钥和
Git 写权限，也不得同时拥有渠道密钥和 Git 写权限。

| Job 类别 | Git 权限 | 机密 | 允许的输出 |
| --- | --- | --- | --- |
| PR CI | `contents: read` | 无 | 测试与报告 |
| 采集/规范化 | `contents: read` | 必要的只读来源凭证 | discovery artifact |
| 预算预留 writer | `contents: write`（仅 `ops` 身份） | 无模型密钥 | 预算预留记录 |
| 模型生成 | `contents: read` | 模型密钥 | 候选文章 artifact |
| content writer | `contents: write`（仅 `content` 身份） | 无模型密钥 | 事件、证据、文章修订 |
| Pages build/deploy | read + `pages/id-token` | 无模型/渠道密钥 | 固定双 SHA 的站点 |
| Publisher | 无 Git 写权 | 单一渠道密钥 | 平台回执 artifact |
| Receipt writer | `contents: write`（仅 `ops` 身份） | 无渠道密钥 | receipt/UNKNOWN 状态 |

删除工作流是独立的 break-glass 路径：默认 dry-run、限制批量、绑定预期源 SHA 和备份 ID，并要求
受保护 Environment 审批。正常发布链没有删除权限。

## 跨 job artifact 为什么必须复验

上传成功只证明 GitHub 保存了某个文件，不证明生产者可信，也不证明文件符合消费者的权限边界。
消费者在解包前必须验证：

- artifact 总摘要和逐文件 SHA-256；
- 路径白名单、文件数量、单文件与总大小；
- 只允许普通、不可执行文件，拒绝 symlink、hardlink、设备和重复路径；
- MIME、UTF-8、JSON schema、必需字段及版本兼容；
- 密钥特征、恶意 Markdown、最终 HTML DOM；
- 生产者声明的 `base_content_sha`、`code_sha` 和配置摘要。

writer 只显式暂存白名单路径，禁止 `git add -A`。同一父 SHA 的并发 writer 通过 CAS 决出一个成功者；
失败者重新读取、确定性归并后再尝试，不使用 rebase、reset 或 force push。

## 为什么部署需要双 SHA 和 release sequence

每次发布绑定：

```text
code_sha + content_sha + schema_version + release_seq + artifact_digest
```

HTML 和 `/api/v1` 固定引用同一个 `release_id`。部署前读取 `ops` 中的最新 sequence；迟到运行的
sequence 不得覆盖更高 sequence。回滚不是移动分支指针，而是用更高 sequence 重新部署一组已验证的
旧 `code_sha + content_sha`，因此预算和已发送回执不会随内容回滚。

只有部署后的生产健康检查成功，publisher 才能消费 outbox。渠道调用超时且结果不明时写入
`UNKNOWN`，不得自动重发，也不得声称 exactly-once。

## 并发、缓存与失败语义

- PR CI 对同一 PR 启用 `cancel-in-progress`，避免浪费旧提交的算力；新提交仍完整执行检查。
- 持久化与部署不依赖取消来保证正确性，正确性由 CAS 和 release sequence 保证。
- 缓存只用于锁文件命中的依赖和内容寻址的模型结果；缓存命中不能跳过验证。
- 缺指标、validator 异常、全部来源失败、摘要不匹配都 fail closed。
- 通知、索引提交等外部副作用必须在生产健康后发生，并留下可协调回执。

## 仓库级控制

上线前需要同步启用：

- Actions 默认 workflow 权限为只读，禁止 Actions 审批 Pull Request；
- workflow 中所有第三方 action 使用完整 commit SHA；
- `main`、`content`、`ops` 和备份 tag 禁止删除与 force push；
- `main` 必须 Pull Request + 稳定命名的 CI 检查；
- 数据分支只允许对应 writer 身份 fast-forward 更新；
- Pages、生产通知和数据删除使用不同的受保护 Environment。

这些设置与仓库中的 workflow 必须一起启用；只做其中一半会留下旁路。
