# Runner 镜像固定策略

关联事故：[INCIDENT-2026-10-05](./INCIDENT-2026-10-05.md)

## 规则

所有 `.github/workflows/*.yml` 中的 job 必须使用固定的 `runs-on: ubuntu-24.04`，
**禁止** `ubuntu-latest`。该规则由 `tests/test_runner_pinning_contract.py` 在 CI 中逐
job 校验，任何新增工作流或新增 job 都自动纳入检查。

## 为什么

`ubuntu-latest` 是浮动标签，由 GitHub 在镜像升级时切换，切换时间不由本仓库控制。
2026-10-05 它转向 `ubuntu26.04-x64`，而本仓库锁定的 Playwright 1.57.0 不支持该镜像，
导致生产刷新连续失败 30 天。代码没有变更、Secrets 没有失效、调度也没有被禁用——
唯一变化的是 runner 镜像。

固定工具链而不固定其底座，等于把发布可用性外包给上游的发布时间表。本仓库已经固定
Python 3.11、Node.js 22、Hugo Extended 0.153.4 与全部 Python/Node 依赖版本，runner OS
是最后一块浮动拼图。

## 浏览器依赖的边界

| 位置 | 是否需要 Chromium | 说明 |
| --- | --- | --- |
| `deploy.yml` → `refresh`（生产刷新） | **否，禁止** | 5 类来源均为 HTTP/RSS/API，见 `config/sources.yaml` |
| `ci.yml` → PR 测试套件 | 是 | `tests/e2e/test_static_site.py` 与图谱烟测需要浏览器 |
| `crawler/twitter_crawler.py` | 仅本地可选 | X/Twitter 来源默认不启用，不在生产来源集合中 |

清理规则：**浏览器安装只允许出现在 CI/测试 job，不允许出现在发布关键路径**。
若未来确实需要在生产抓取中使用浏览器，正确做法是先新增一个独立、可失败降级的可选 job，
而不是把它塞进 `refresh` 的必经步骤。

## 升级 runner OS 的流程

1. 在功能分支中把 `PINNED_RUNNER`（`tests/test_runner_pinning_contract.py`）与目标版本一起修改。
2. 在 PR CI 中确认 `python3 -m playwright install --with-deps chromium` 与 e2e 浏览器烟测全绿——这是 Playwright 是否支持新镜像的唯一可信判据。
3. 确认 `deploy.yml` 的 `refresh` 仍不含浏览器安装。
4. 合并后手动触发一次 `deploy.yml`（`refresh_data=true`），走完 `production-verify`。
5. 观察下一次 `monitoring.yml` 为绿色，再认为升级完成。

不要在发布中断期间用放宽 `--max-stale-hours` / `--max-divergence-hours` 的方式「让监控变绿」。

## 相关检查

- 契约测试：`tests/test_runner_pinning_contract.py`
- 故障定位：`scripts/check_release_runs.py`（告警中直接给出首个失败 job 与步骤）
- 排障手册：`docs/operations/freshness-runbook.md`
- 新鲜度阈值：3 小时版本分歧 / 12 小时刷新陈旧，不因镜像问题调整
