# GitHub 仓库加固操作说明

`scripts/github_hardening.py` 把仓库级控制分成两步：先读取 GitHub REST API 当前快照并生成
canonical plan；只有显式传入 `--apply`，且仓库全名、不可复用的 repository ID、`main` 完整 SHA
和当前快照 SHA-256 四项同时吻合时，才执行计划中的 `PUT`/`POST`。工具没有任何 `DELETE`
操作，不会删除未知 ruleset；同名的三个托管 ruleset 只会幂等创建或更新。

本实现按 GitHub REST API `2026-03-10` 核对，使用的官方接口为
[Actions 默认权限](https://docs.github.com/en/rest/actions/permissions?apiVersion=2026-03-10)、
[仓库 ruleset](https://docs.github.com/en/rest/repos/rules?apiVersion=2026-03-10)、
[deployment environment](https://docs.github.com/en/rest/deployments/environments?apiVersion=2026-03-10)、
[deployment branch policy](https://docs.github.com/en/rest/deployments/branch-policies?apiVersion=2026-03-10)
及 [immutable releases](https://docs.github.com/en/rest/repos/repos?apiVersion=2026-03-10#enable-immutable-releases)。

## 先生成 dry-run 计划

默认命令只读，不接受“隐式执行”：

```bash
python3 scripts/github_hardening.py --repository g5n-dev/ai-stack
```

输出中的 `snapshot_sha256`、repository ID 和 `main_sha` 是后续审批输入。计划应由第二人核对
`config/github-hardening.expected.json`、全部 operation 以及列出的未知 ruleset。不要把 token、
凭据或 dirty patch 写入计划。

## 显式执行门禁

实际执行必须重新读取当前快照，并同时提供四项期望值：

```bash
python3 scripts/github_hardening.py \
  --repository g5n-dev/ai-stack \
  --apply \
  --expected-full-name g5n-dev/ai-stack \
  --expected-repository-id '<数字 ID>' \
  --expected-main-sha '<完整 SHA>' \
  --expected-snapshot-digest '<64 位 SHA-256>'
```

任一字段变化、API 响应缺失、同名托管 ruleset 重复、bypass actor 不可见、托管 Environment
存在额外 branch policy 或写请求失败都会 fail closed。额外 policy 会列入
`unmanaged_environment_policies`，工具不自动删除，需人工确认并移除后重新生成计划。部分请求
已经成功后发生失败时不做破坏性回滚；重新读取快照、重新审批新 plan，再依靠同名
update/create 的幂等语义继续。不要使用旧摘要重试。GitHub API 失败信息只保留请求方法、仓库内
endpoint 和可解析的 HTTP status，不转发响应正文或 `gh` stderr；确定性的 4xx（包括 422）不会
重试，apply 中任一写失败后也不会继续执行后续 operation。

## 期望控制及准确边界

- Actions 默认 `GITHUB_TOKEN` 为 read，并开启
  `can_approve_pull_request_reviews=true`（GitHub 界面的 “Allow GitHub Actions to create and
  approve pull requests”）。这是自动数据提交通过受保护 PR 合入所需的仓库级能力，不是默认写
  权限：只有明确声明 `pull-requests: write` / `checks: write` / `contents: write` 的无 Secret writer
  job 才能使用；采集、验证和来自 PR 的测试保持只读。不得给执行不受信任 PR 代码的 job 增加
  这些写权限。
- immutable releases 开启后，已发布 release 的资产和 tag 受保护；应先创建 draft、上传并校验
  全部资产，最后发布，因为发布后资产不可改。
- 所有三个托管 ruleset 的 `bypass_actors` 都必须是空数组；GitHub Actions App（Integration ID
  `15368`）也不能绕过 `main`。
- `main` 禁止删除和 force push，必须从 PR 合入，并要求唯一的稳定检查
  `Unit Tests`，且该 check 精确绑定 Integration ID `15368`。实际测试 job 名为
  `PR Test Suite`，包含 Python/JavaScript、安全、图谱浏览器烟测、Hugo 与 Pagefind 交付边界；
  `pull_request_target` controller 始终从精确 base SHA checkout 受信代码，且绝不 checkout、下载或
  执行 PR 内容；它只把 PR number/head SHA 作为数据，复核当前 PR 后，dispatch `main` 上的受信
  `ci.yml`。该测试定义用只读 token checkout exact target SHA，禁用共享 pip/npm cache，并把真实
  测试结果绑定到 exact workflow run。controller 只有在再次核验 head/base、run identity、测试
  check 与 GitHub Actions App 身份后，才为同一 PR head 发布 `Unit Tests`。因此 PR 可以提供待测
  代码，但不能修改“如何测试自己”后自证通过；同名外部 status 或 fork 伪造 check 也不能满足规则。
  PR 规则的 approving review count 为 0：它强制 PR 和检查，
  但不会虚称已经建立双人审批；单维护者仓库若直接要求 1 个非作者审批会造成永久阻塞。
- 定时数据与已审批删除不会直接 push `main`：无 Secret writer 先基于 exact `main` SHA 创建
  `automation/data-*` 或 `automation/delete-*`，触发同一 `PR Test Suite`，核验 exact run/check 后
  为该 head 发布 `Unit Tests`，再创建 PR，并用 base/head CAS 与 SHA-locked squash merge 合入。
  `main` 在验证或合并前移动都会失败，不能 rebase、force 或绕过 ruleset。
- `content`/`ops` 禁止删除、force push 和 merge commit（`required_linear_history`），但这些规则
  本身只约束更新形状，不会把普通 fast-forward push 自动限定为某个 writer。
- GitHub 还会在 `main` 的 pull-request rule 响应中自动补出空的
  `required_reviewers: []`。工具只把“缺失”和“空数组”规范化为同一无额外 reviewer 策略；任何
  非空值都会 fail closed，避免把服务端新增的真实审批策略静默吞掉。
- `backup-*` 与 `content-seed-*` tag 创建后禁止更新和删除；创建本身仍允许，以便先产生新的、
  不可移动的备份或内容种子 tag。GitHub 对 tag `update` rule 的只读语义可能返回“省略
  parameters”或显式 `update_allows_fetch_and_merge=false`，工具将二者规范化为同一策略以避免
  永久漂移；若返回 `true` 或未知参数则 fail closed。
- `github-pages`、`production-publish`、`data-deletion` 与 `production-recovery` 都只允许 `main`。
  生产站点由 Pages artifact 发布，不再依赖独立发布分支。前两个 Environment 用于隔离
  Pages/渠道凭据但不要求人工审批；后两个把仓库 owner 配为 required reviewer，且
  `prevent_self_review=false`，在单维护者仓库中仍保留一次显式 Environment 审批而不自锁。若后续
  增加独立管理员，应把它们改为独立 reviewer 并开启禁止自审。

最重要的身份边界：同一个 `GITHUB_TOKEN` 不能提供严格的 job 级 writer identity。job 的
`permissions` 能缩小 token 权限，但 ruleset 无法把同一仓库中不同 job 使用的同一种 Actions
身份可靠地区分为“content writer”“ops writer”。当前闭环因此不把该 Integration 设为 bypass，
而用 default-branch controller、exact SHA/run/check 校验、无 Secret writer 和 PR/CAS 组合降低
风险。若未来需要严格指定 writer，应安装权限最小化的专用 GitHub App，使用独立 installation
token；仍应优先让它走受保护 PR，而不是授予永久 bypass。当前工具不会虚报已经实现了 job 级
身份隔离。

本工具也不修改 workflow、secret、environment secret 或仓库成员权限。未知 ruleset 被保留，
因此计划中的 `unmanaged_rulesets` 必须人工检查是否与目标策略冲突。
