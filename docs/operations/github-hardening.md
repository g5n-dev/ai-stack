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
uv run python scripts/github_hardening.py --repository g5n-dev/ai-stack
```

输出中的 `snapshot_sha256`、repository ID 和 `main_sha` 是后续审批输入。计划应由第二人核对
`config/github-hardening.expected.json`、全部 operation 以及列出的未知 ruleset。不要把 token、
凭据或 dirty patch 写入计划。

## 显式执行门禁

实际执行必须重新读取当前快照，并同时提供四项期望值：

```bash
uv run python scripts/github_hardening.py \
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
update/create 的幂等语义继续。不要使用旧摘要重试。

## 期望控制及准确边界

- Actions 默认 `GITHUB_TOKEN` 为 read，且 `can_approve_pull_request_reviews=false`。
- immutable releases 开启后，已发布 release 的资产和 tag 受保护；应先创建 draft、上传并校验
  全部资产，最后发布，因为发布后资产不可改。
- `main` 禁止删除和 force push，必须从 PR 合入，并要求稳定检查 `Unit Tests`、`static-site`、
  `browser-e2e`。PR 规则的 approving review count 为 0：它强制 PR 和检查，但不会虚称已经建立
  双人审批；单维护者仓库若直接要求 1 个非作者审批会造成永久阻塞。
- `content`/`ops` 禁止删除、force push 和 merge commit（`required_linear_history`），但这些规则
  本身只约束更新形状，不会把普通 fast-forward push 自动限定为某个 writer。
- `backup-*` 与 `content-seed-*` tag 创建后禁止更新和删除；创建本身仍允许，以便先产生新的、
  不可移动的备份或内容种子 tag。
- `github-pages` 保留既有 `gh-pages` 并增加 `main` 的 custom deployment branch policy，避免改变
  原 Pages 发布路径，同时允许新协调流程从 `main` 部署。`production-publish`、`data-deletion`
  仍只允许 `main`。前两个 Environment 用于隔离 Pages/渠道凭据但不要求人工审批；
  `data-deletion` 把仓库 owner 配为
  required reviewer，且 `prevent_self_review=false`，在单维护者仓库中仍保留一次显式 Environment
  审批而不自锁。若后续增加独立管理员，应把它改为独立 reviewer 并开启禁止自审。

最重要的身份边界：同一个 `GITHUB_TOKEN` 不能提供严格的 job 级 writer identity。job 的
`permissions` 能缩小 token 权限，但 ruleset 无法把同一仓库中不同 job 使用的同一种 Actions
身份可靠地区分为“content writer”“ops writer”。若要严格指定 writer，必须安装权限最小化的
专用 GitHub App，使用独立 installation token，并将对应 Integration actor 纳入经过审计的
ruleset 设计；当前工具不会虚报已经实现了该身份隔离。

本工具也不修改 workflow、secret、environment secret 或仓库成员权限。未知 ruleset 被保留，
因此计划中的 `unmanaged_rulesets` 必须人工检查是否与目标策略冲突。
