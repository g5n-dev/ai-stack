# AI Stack 工作流程文档

> 本文件面向在本仓库内工作的 AI 协作者与维护者。以代码和 CI 契约为准；若本文与
> `.github/workflows/` 不一致，优先修本文。
> 最近一次重大修订：2026-11-04（INCIDENT-2026-10-05 复盘后）。

## 1. 项目定位

AI Stack 是**无数据库、无消息队列、无常驻服务**的静态 AI 情报档案与知识图谱：
多源采集 → URL 去重与事件谱系 → AI 精炼 → Markdown 归档 → Hugo + Pagefind →
GitHub Pages。内容是 Markdown，关系是 Graph JSON v2，产物全部可版本化、可回查。

生产地址 <https://ai-stack.site/>；趋势 `/trends/`；图谱 `/scenarios/`。

## 2. 分支与发布模型

- 唯一主干 `main`，受保护；Pages 从 Actions artifact 部署，不使用 `gh-pages` 分支。
- 数据写入由 `scripts/git_cas_writer.py` 以 **exact-base CAS** 提交到临时
  `automation/data-<run_id>` 分支，再由 `scripts/protected_branch_merge.py` 合并。
- 严禁 `reset --hard`、`git pull --rebase`、force push 绕过 CAS。
- 提交形如 `chore(data): persist validated release [skip ci]`；push 由 bot 触发时不再重复刷新。

## 3. 生产 DAG

`deploy.yml` 的 7 个 job 严格串联，任一失败后续全部 skipped：

| # | Job | 权限 | 职责 |
| --- | --- | --- | --- |
| 1 | `refresh` | `contents: read` | 抓取 + 模型精炼；**唯一接触模型密钥的阶段** |
| 2 | `validate` | `contents: read` | artifact 校验、刷新跃迁守卫、派生数据重建 |
| 3 | `persist` | 写权限 | 精确 SHA 的 CAS 写入与受保护分支合并 |
| 4 | `build` | `contents: read` | 固定点复现、Hugo/Pagefind/CSS、release marker |
| 5 | `deploy` | `pages: write` | 上传并发布已守卫的 artifact |
| 6 | `production-verify` | `contents: read` | 线上 SHA / release ID 烟测，保留 90 天验证回执 |
| 7 | `notify` | `contents: read` | 验证通过后才通知搜索索引 |

调度：每小时 `:17` 完整刷新；`:41` 只读新鲜度监控；push 到 `main` 只部署已提交快照
（`AI_STACK_REFRESH_DATA=false`）；`workflow_dispatch` 可选 `refresh_data` 与 `expected_sha`。
监控阈值固定为 3 小时版本分歧 / 12 小时刷新陈旧，**不得为掩盖停滞而放宽**。

`Production Recovery` 只接受有未过期生产验证回执的精确 `main` 祖先 SHA。

## 4. Runner 与浏览器边界（重要）

所有 job 固定 `runs-on: ubuntu-24.04`，**禁止 `ubuntu-latest`**。
`ubuntu-latest` 在 2026-10-05 滚到 `ubuntu26.04-x64`，锁定的 Playwright 1.57.0
拒绝在该镜像安装 Chromium，导致 `refresh` 前置步骤失败、全链中断 30 天。
详见 `docs/operations/INCIDENT-2026-10-05.md` 与 `docs/operations/runner-pinning.md`。

- 生产 `refresh` **不得**出现浏览器/Chromium 安装：5 类来源全是 HTTP/RSS/API。
- Chromium 只允许出现在 `ci.yml` 的 PR 测试套件（`tests/e2e/test_static_site.py`、
  图谱烟测）与可选的本地 `crawler/twitter_crawler.py`。
- 固定工具链：Python 3.11、Node.js 22、Hugo Extended 0.153.4、全部依赖锁版本。

## 5. 目录结构

```text
ai-stack/
├── crawler/             # 多源抓取（5 类生产源 + 可选本地源）
├── processor/           # 模型兼容层、内容精炼、标签、图谱
├── publisher/           # 可选发布器，默认全部关闭
├── ai_stack/            # 领域模型、事件谱系、清单、流水线 CLI
├── blog/                # Hugo 内容/主题、静态数据、Graph JSON v2
├── config/              # 来源、模型、趋势、谱系、发布配置
├── scripts/             # 生成、校验、构建、CAS、监控、运维脚本
├── tests/               # Python / JS / Playwright 测试
├── docs/                # 架构、部署、操作手册与事故复盘
└── .github/workflows/   # deploy / monitoring / ci / pr-gate / recovery / delete-post
```

关键配置：`config/sources.yaml`（来源与配额）、`config/anthropic.yaml`、
`config/lineage.yaml`、`config/stack_trends.yaml`、`runtime_profile.py`（本地/CI 档位）。

## 6. 常用命令

```bash
# 本地环境与完整流水线
bash scripts/setup.sh
bash scripts/run_local.sh --serve

# 只看站点（无需 Python / 密钥）
cd blog && hugo server -D

# 数据质量与派生数据校验
python3 scripts/build_content_quality_manifest.py --content-root blog/content \
  --output /tmp/content_quality.json --fail-on-quarantine \
  --fail-on-structural-warning --fail-on-unverified-provenance
python3 scripts/repair_historical_content.py --check
python3 scripts/verify_lineage.py --verify-hashes
bash scripts/rebuild_release_data.sh

# 与本次修复相关的回归测试
python3 -m pytest -q tests/test_runner_pinning_contract.py \
  tests/test_check_release_runs.py tests/test_workflow_security.py \
  tests/test_v1_release_contract.py

# 手动刷新 / 只读监控
gh workflow run deploy.yml --repo g5n-dev/ai-stack -f refresh_data=true
gh workflow run monitoring.yml --repo g5n-dev/ai-stack
```

新增测试必须同时注册进 `ci.yml` 的 pytest 清单，否则不执行。

## 7. 数据与告警约定

- 趋势按稳定 `event_id` 计算 `unique_events`，只有 allowlist 认可的 `same_event` 才合并；
  必须满足 `redundant_observations = observations - unique_events`。
- 派生 JSON（lineage / trends / tag-graph / content_quality）只能由生成器重建，
  **禁止手工编辑绕过哈希校验**；索引与分片的 path/bytes/sha256/schema 必须一致。
- 来源不可恢复时转成带失败类型、原因、时间与原始链接的**透明归档**，不得用模型
  推测正文填补证据空白，不得把抓取时间伪装成事件时间。
- 告警由 `scripts/ops_alert.py` 以 Issue 形式维护，持续故障只更新正文，恢复自动关闭。
  `scripts/check_release_runs.py` 会把最近一次失败运行的**首个失败 job 与步骤**写进告警；
  诊断查询自身失败时只记录，不掩盖已检出的故障。

## 8. 安全边界

- 密钥只存在于本地 `.env` 或 GitHub Actions Secrets；公开 IndexNow key 用 repository Variable。
- GitHub Actions 日志只写布尔状态、计数、错误类别、运行链接与公开资源 URL。
- 不把认证值、cookie、私有 endpoint、完整请求头或外部响应正文复制到日志、Issue、PR 或文档。
- 本地 `git remote` 不应内嵌明文 token；疑似泄露先轮换，再提交脱敏报告。

## 9. 常见陷阱

1. 看到「工作流一直在跑」就认为健康——定时任务可以每小时失败，告警也会持续刷屏。
2. 按告警里的固定阶段名排障——始终以 API 定位的**首个失败步骤**为准。
3. 把可选依赖放进发布关键路径——任何非必需安装步骤都可能成为单点故障。
4. 用放宽阈值、手工改 JSON、force push 让流水线「变绿」。
5. 改了测试却没注册进 CI，或改了 workflow 却没有对应契约测试。

## 10. 文档索引

- `README.md` — 能力、快速开始、自动化与可靠性
- `DEPLOYMENT.md` — Pages、域名、Secrets、部署验证
- `docs/README.md` — 详细使用文档
- `docs/operations/freshness-runbook.md` — 新鲜度排障决策顺序
- `docs/operations/runner-pinning.md` — runner 固定策略与升级流程
- `docs/operations/INCIDENT-2026-10-05.md` — 30 天断更事故复盘
- `docs/architecture/ci-trust-model.md` — 工作流权限与信任边界
