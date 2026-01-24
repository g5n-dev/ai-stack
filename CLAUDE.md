# AI-Stack 工作流程文档

## 概述

本文档记录AI-Stack项目的完整工作流程，包括内容生成、标签系统、知识图谱构建、AI主题过滤和自动化部署。

## 核心流程

### 1. 内容生成流程

内容生成由 `scripts/generate_content.py` 驱动，执行以下5个步骤：

```bash
python3 scripts/generate_content.py
```

**步骤说明：**

1. **数据采集** (1/5)
   - 从 blogs_podcasts 和 github_discussions 采集数据
   - 数据位置：`data/`

2. **数据处理** (2/5)
   - 清洗和预处理原始数据
   - 生成标签（使用 LLM）

3. **生成超级增强版 Markdown 文章** (3/5)
   - 基于处理后的数据生成 Markdown 文章
   - 输出位置：`blog/content/posts/`

4. **生成标签图谱** (4/5)
   - 构建标签共现关系图谱
   - 输出位置：`blog/static/data/tag-graph.json`

5. **推送内容** (5/5)
   - 发布到社交平台

### 2. 标签系统

#### 标签生成
- 使用 LLM（glm-4.7）自动为文章生成标签
- 标签生成器：`processor/tagger.py`

#### 标签图谱
- 构建标签共现关系，展示标签之间的关联
- 图谱生成器：`processor/tag_graph.py`
- 数据格式：JSON（包含 nodes 和 edges）
- 前端渲染：使用 D3.js 力导向图

**手动生成标签图谱：**
```bash
python3 processor/tag_graph.py
```

**图谱数据结构：**
```json
{
  "nodes": [
    {
      "id": "ai",
      "group": "tag",
      "label": "AI",
      "weight": 1.0,
      "articles": ["article1", "article2"]
    }
  ],
  "edges": [
    {
      "source": "ai",
      "target": "llm",
      "weight": 2,
      "label": "co-occurrence"
    }
  ]
}
```

### 3. AI 主题过滤

#### 过滤脚本
- 位置：`processor/ai_filter.py`
- 功能：使用 LLM 判断内容是否与 AI 主题相关
- 支持严格模式和置信度阈值

#### 使用方法
```python
from processor.ai_filter import AIThemeFilter, filter_batch

# 创建过滤器
filter = AIThemeFilter(client=anthropic_client)

# 过滤单条内容
result = filter.filter(content_dict)

# 批量过滤
ai_related, non_ai_related = filter_batch(contents, filter)
```

#### 配置选项
- `enabled`: 是否启用过滤（默认：true）
- `strict_mode`: 严格模式（默认：false）
- `min_confidence`: 最小置信度阈值（默认：0.6）

### 4. AI 主题自动过滤和图谱构建

#### 自动化工作流
在 [Sync to gh-pages](.github/workflows/sync-to-gh-pages.yml) 工作流中集成了自动过滤和图谱构建功能：

**触发条件：**
- 推送到 main 分支
- 手动触发

**工作流程：**
1. **Setup Python 环境**
   - 使用 Python 3.10
   - 安装 anthropic 依赖

2. **清理非 AI 文章**
   - 使用 Claude-3.5-Sonnet 判断文章是否与 AI 相关
   - 置信度阈值：0.6
   - 自动删除非 AI 相关文章

3. **重建标签图谱**
   - 基于清理后的文章重新构建图谱
   - 包含 7 层架构（语言、框架、模型、应用、场景、标签、概念）

4. **构建和部署**
   - 构建 Hugo 站点
   - 推送到 gh-pages 分支

**环境变量：**
- `ANTHROPIC_API_KEY`: Claude API 密钥（在 GitHub Secrets 中配置）

### 5. 文章管理

#### 文章目录
- 位置：`blog/content/posts/`
- 命名格式：`YYYY-MM-DD-title.md`

#### Frontmatter 格式
```yaml
---
title: "文章标题"
date: 2025-01-24T10:30:00+08:00
draft: false
tags: ["tag1", "tag2", "tag3"]
entry_kind: "auto"
source: "blogs_podcasts"
---
```

### 5. 知识图谱可视化

#### 前端集成
- 页面位置：`blog/themes/terminal-theme/layouts/scenarios/list.html`
- 数据加载：从 `/data/tag-graph.json` 加载图谱数据
- 图表引擎：`blog/themes/terminal-theme/assets/js/graph-engine.js`

#### 技术栈
- D3.js 力导向图
- 支持节点拖拽、缩放、悬停交互
- 节点分组：6 层架构 + 标签层

## GitHub Actions 工作流

### 1. Sync to gh-pages
**文件：** `.github/workflows/sync-to-gh-pages.yml`

**触发条件：**
- 推送到 main 分支
- 手动触发

**详细工作流程：**

```yaml
1. Checkout main branch
   - 使用 actions/checkout@v4
   - ref: main
   - fetch-depth: 0 (获取完整历史)

2. Configure Git
   - 配置全局用户名：github-actions[bot]
   - 配置全局邮箱：github-actions[bot]@users.noreply.github.com

3. Fetch gh-pages branch
   - 尝试拉取 gh-pages 分支
   - 如果不存在则创建新分支

4. Create or checkout gh-pages branch
   - 如果 gh-pages 存在：checkout 现有分支
   - 如果不存在：创建 orphan 分支并清空

5. Stash untracked files before merge
   - 使用 git stash push -u 保存未跟踪文件
   - 防止合并时出现冲突

6. Merge main into gh-pages
   - 使用 -X theirs 保留 gh-pages 的更改
   - 使用 --allow-unrelated-histories 处理无关历史
   - 首次合并和后续合并使用不同策略

7. Setup Python 环境
   - 使用 Python 3.10
   - 安装 anthropic 依赖

8. 清理非 AI 文章
   - 使用 Claude-3.5-Sonnet 判断文章是否与 AI 相关
   - 置信度阈值：0.6
   - 自动删除非 AI 相关文章

9. 重建标签图谱
   - 基于清理后的文章重新构建图谱
   - 包含 7 层架构（语言、框架、模型、应用、场景、标签、概念）

10. Setup Hugo
   - 使用 peaceiris/actions-hugo@v2
   - 版本：latest
   - extended: true

11. Build Hugo site
   - 检查 blog/config.toml 是否存在
   - 执行 hugo --baseURL "https://ai-stack.site/" --minify --cleanDestinationDir
   - 将构建产物复制到根目录
   - 清理临时文件

12. Push to gh-pages
   - git add -A 添加所有更改
   - git diff --cached --quiet 检查是否有更改
   - git commit -m "Sync from main [skip ci]" 提交
   - git push origin gh-pages --force-with-lease 推送
```

**关键配置说明：**
- **Stash 步骤**：防止未跟踪文件导致合并冲突
- **Theirs 策略**：在冲突时保留 gh-pages 分支的更改
- **Force-with-lease**：安全推送，避免覆盖他人的提交
- **Skip ci**：避免触发其他 CI/CD 流程
- **Gitignore**：验证报告文件 `*_verification_report.json` 已被忽略

**环境变量：**
- `ANTHROPIC_API_KEY`: Claude API 密钥（在 GitHub Secrets 中配置）

### 2. Monitoring
**文件：** `.github/workflows/monitoring.yml`

**触发条件：**
- 每 6 小时自动执行
- 手动触发

**监控内容：**
- 分支活跃度（main 和 gh-pages）
- 内容质量指标
- 知识图谱状态
- 标签系统指标
- Token 使用情况
- 同步状态

### 3. Gitignore 配置

**验证报告排除：**
```
# Verification reports
*_verification_report.json
```

## 常用命令

### 内容生成
```bash
python3 scripts/generate_content.py
```

### 标签图谱生成
```bash
python3 processor/tag_graph.py
```

### Hugo 本地开发
```bash
cd blog
hugo server
```

### Hugo 生产构建
```bash
cd blog
hugo --baseURL "https://ai-stack.site/" --minify --cleanDestinationDir
```

## 文件结构

```
ai-stack/
├── processor/
│   ├── tagger.py              # 标签生成器
│   ├── tag_graph.py           # 标签图谱生成器
│   ├── tech_stack.py          # 技术栈节点定义
│   ├── ai_filter.py           # AI 主题过滤器
│   └── scenarios.py           # 场景处理器
├── scripts/
│   └── generate_content.py    # 内容生成主脚本
├── blog/
│   ├── content/posts/         # 文章目录
│   ├── static/data/           # 静态数据（图谱数据）
│   └── themes/terminal-theme/
│       ├── layouts/scenarios/list.html
│       └── assets/js/graph-engine.js
├── .github/workflows/
│   ├── sync-to-gh-pages.yml   # 同步到 gh-pages 工作流
│   ├── gh-pages-content.yml   # gh-pages 内容管理
│   └── monitoring.yml         # 监控工作流
└── CLAUDE.md                  # 本文档
```

## 故障排查

### 1. 标签图谱未更新
**问题：** 图谱数据未包含最新文章

**解决方案：**
```bash
# 重新生成图谱
python3 processor/tag_graph.py

# 检查输出文件
cat blog/static/data/tag-graph.json
```

### 2. GitHub Actions 失败
**问题：** Sync to gh-pages 工作流失败

**检查项：**
1. 确认 Hugo 配置文件存在：`blog/config.toml`
2. 检查验证报告是否被正确忽略：`*_verification_report.json`
3. 查看工作流日志中的错误信息

### 3. 标签未显示
**问题：** 文章标签未在图谱中显示

**检查项：**
1. 确认文章 frontmatter 包含 `tags` 字段
2. 运行标签图谱生成脚本
3. 刷新浏览器缓存

## 最佳实践

1. **内容质量保证**
   - GitHub Actions 自动过滤非 AI 相关内容
   - 置信度阈值设置为 0.6 以平衡准确性和召回率
   - 定期审查被删除的文章，确保误判率在可接受范围

2. **图谱维护**
   - 每次 GitHub Actions 运行时自动重建图谱
   - 图谱包含 7 层架构，支持标签和概念挖掘
   - 监控图谱统计信息（节点数、连线数、概念数量）

3. **持续监控**
   - 定期检查 GitHub Actions 运行状态
   - 关注监控报告中的关键指标
   - 验证 ANTHROPIC_API_KEY 是否正确配置

4. **文档更新**
   - 重大流程变更时更新本文档
   - 记录故障排查经验
   - 同步更新代码注释和工作流描述

## 联系和支持

如有问题或建议，请查看 GitHub Issues 或联系维护团队。
