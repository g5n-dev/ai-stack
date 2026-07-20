# 为 AI Stack 贡献

感谢你帮助 AI Stack 把一次性信息流变成可追溯、可解释、可持续生长的技术档案。

## 从哪里开始

- Bug、数据异常与功能建议：先创建 GitHub Issue。
- 边界较清楚的小改动：可以直接提交 Pull Request，并在描述中关联 Issue。
- 涉及内容来源、评分语义、图谱数据格式或 CI/CD 权限的改动：先在 Issue 中写明迁移与回滚方案。
- 当前路线图见 [v1.0 · 可持续情报闭环](https://github.com/g5n-dev/ai-stack/milestone/1)。

## 安全边界

提交前请确认：

- 不提交 `.env`、API token、cookie、私有 endpoint、完整请求头或含敏感值的日志。
- 示例只使用明显的占位符，例如 `replace_with_your_token` 与 `https://llm.example.com/anthropic`。
- 文章转写不伪造原文；来源不可恢复时使用透明归档状态，不用生成文本填补证据空白。
- 动态内容使用安全 DOM API 构建，不把外部文本直接注入 `innerHTML`。
- CI 权限保持最小化；修改 `contents: write`、`pages: write`、`id-token: write` 前说明必要性。

疑似密钥泄露时不要把值贴进 Issue。先轮换密钥，再只提供脱敏后的错误类型、时间和运行链接。

## 本地准备

项目支持 Python `>=3.11,<3.14`（即 3.11–3.13）；生产 Actions 固定使用 3.11。只改 UI 或文档时，不需要模型密钥：

```bash
cd blog
hugo server -D
```

运行完整流水线时：

```bash
bash scripts/setup.sh
nano .env
python3 scripts/preflight.py --require-hugo
```

## 测试矩阵

先运行与改动范围最接近的测试，再运行稳定回归：

```bash
# 浏览器运行时、趋势、搜索与图谱契约
npm test

# Python 全量回归
python3 -m pytest -q

# 内容质量固定点
python3 scripts/build_content_quality_manifest.py \
  --content-root blog/content \
  --output /tmp/content_quality.json \
  --fail-on-quarantine \
  --fail-on-structural-warning \
  --fail-on-unverified-provenance
cmp --silent blog/data/content_quality.json /tmp/content_quality.json

# 历史修复固定点
python3 scripts/repair_historical_content.py --check

# 谱系、图谱与趋势静态资产
python3 scripts/verify_lineage.py --verify-hashes
python3 scripts/verify_graph.py --assets-only --public-dir blog/static
python3 scripts/verify_stack_trends.py \
  --root blog/static/data/stack-trends \
  --verify-hashes
```

涉及模板、样式或脚本时，还应构建站点与搜索索引：

```bash
npm ci --ignore-scripts
npm run build:css
cd blog
hugo --minify --cleanDestinationDir
cd ..
npm run build:search
```

## Pull Request 要求

Pull Request 描述至少包含：

1. 解决的问题与用户可见结果。
2. 关键设计边界与未覆盖范围。
3. 测试命令和真实结果。
4. 数据格式、CI/CD、密钥权限或部署行为是否变化。
5. UI 改动在桌面与移动端的截图或录屏。

保持一次 PR 只有一个主要目标。不要混入自动生成内容、无关格式化或个人环境文件。

## 提交与生成数据

- 人工代码提交不要直接写入 `main`，使用功能分支和 PR。
- 定时生成的 Markdown、谱系、质量清单、图谱与趋势资产由生产工作流统一提交。
- 如果代码改动会改变确定性生成结果，请在同一 PR 中提交对应资产并说明重建命令。
- 不要手工修改谱系、质量 manifest、图谱分片或趋势分片来绕过生成器。

## 完成定义

改动只有在以下条件满足时才算完成：

- 测试先于实现覆盖了新行为或修复的回归场景。
- Hugo、Pagefind 和相关静态资产验证通过。
- 无密钥、个人路径、失效链接和虚假实时指标。
- 移动端、键盘和 reduced-motion 行为没有退化。
- PR CI 绿色；发布路径、精确 SHA 的生产验证证据及恢复方式清楚。

完整发布闸门见 [docs/V1_RELEASE_CHECKLIST.md](./docs/V1_RELEASE_CHECKLIST.md)。
