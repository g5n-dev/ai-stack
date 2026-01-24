# AI-Stack 工作流程文档

## 概述

AI-Stack 项目采用单分支架构（main 分支）：

- **main 分支**：包含所有代码逻辑、数据、Hugo 构建产物和部署配置
- **GitHub Pages**：自动从 main 分支部署，无需额外的 gh-pages 分支

## 核心架构

### 单分支结构

```
main 分支（完整仓库）
├── crawler/              # 爬虫逻辑
├── processor/            # 内容处理逻辑
├── scripts/              # 生成脚本
├── blog/                 # Hugo 配置和主题
│   ├── config.toml       # Hugo 配置
│   ├── content/posts/    # 文章目录
│   ├── static/data/      # 图谱数据（tag-graph.json）
│   ├── themes/           # Hugo 主题
│   └── public/           # Hugo 构建产物（gitignore）
├── .github/workflows/    # GitHub Actions 工作流
│   └── deploy.yml        # 构建和部署工作流
└── data/                 # 本地测试数据
```

## GitHub Actions 工作流

### Deploy Workflow（构建和部署）

**文件：** `.github/workflows/deploy.yml`

**触发条件：**
- 定时触发：每 30 分钟
- 推送到 main 分支
- 手动触发

**工作流程：**

```yaml
1. Checkout main branch
   - 获取 main 分支的最新代码和数据

2. 配置 Git 和环境
   - 配置 Git 用户信息
   - 安装 Python 和 Hugo

3. 运行爬虫系统
   - 执行 crawler/main.py 采集数据
   - 输出原始数据到 data/ 目录

4. 运行内容处理系统
   - 执行 processor/main.py 处理数据
   - 生成标签和元数据

5. 构建标签图谱
   - 执行 processor/tag_graph.py
   - 生成 tag-graph.json 到 blog/static/data/

6. 构建 Hugo 站点
   - 执行 hugo --baseURL "https://ai-stack.site/" --minify
   - 生成静态站点到 blog/public/

7. 提交更改
   - 提交更新的 posts 和 data
   - 推送到 main 分支

8. 部署到 GitHub Pages
   - 上传 blog/public/ 为 Pages artifact
   - 自动部署到 https://ai-stack.site/
```

**关键配置：**

```yaml
on:
  schedule:
    - cron: "*/30 * * * *"  # 每 30 分钟运行一次
  workflow_dispatch:
  push:
    branches:
      - main

permissions:
  contents: write
  pages: write
  id-token: write

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout main branch
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4

      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v2

      - name: Run crawler
        run: python3 crawler/main.py

      - name: Run processor
        run: python3 processor/main.py

      - name: Build tag graph
        run: python3 processor/tag_graph.py

      - name: Build Hugo site
        run: |
          cd blog
          hugo --baseURL "https://ai-stack.site/" --minify

      - name: Commit changes
        run: |
          git add -A
          git diff --cached --quiet || git commit -m "Update content and build"
          git push origin main

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: blog/public

      - name: Deploy to GitHub Pages
        uses: actions/deploy-pages@v4
```

## 数据流

### 完整流程

```
main 分支（开发者修改或定时触发）
  ↓
deploy.yml（运行爬虫和处理器）
  ↓
main 分支（更新 posts 和 data）
  ↓
deploy.yml（构建 Hugo 站点）
  ↓
GitHub Pages（自动部署到 https://ai-stack.site/）
```

### 数据一致性保证

1. **单分支管理**
   - 所有代码、数据、配置都在 main 分支
   - 无需跨分支同步

2. **自动构建和部署**
   - 每次 main 分支更新都自动触发部署
   - GitHub Pages 直接从 main 分支部署

3. **构建产物管理**
   - blog/public/ 目录在 .gitignore 中
   - GitHub Actions 自动构建并上传为 artifact

## 核心组件

### 1. 爬虫系统

**位置：** `crawler/main.py`

**功能：**
- 协调多个数据源爬虫
- 采集 blogs_podcasts、github_discussions 等数据
- 输出原始数据到 `data/` 目录

**运行方式：**
```bash
python3 crawler/main.py
```

### 2. 内容处理系统

**位置：** `processor/main.py`

**功能：**
- 清洗和预处理爬虫数据
- 生成标签（使用 LLM）
- 提取关键信息

**运行方式：**
```bash
python3 processor/main.py
```

### 3. 标签图谱系统

**位置：** `processor/tag_graph.py`

**功能：**
- 构建标签共现关系图谱
- 生成 7 层架构（语言、框架、模型、应用、场景、标签、概念）
- 输出到 `blog/static/data/tag-graph.json`

**运行方式：**
```bash
python3 processor/tag_graph.py
```

### 4. AI 主题过滤

**位置：** `processor/ai_filter.py`

**功能：**
- 使用 Claude-3.5-Sonnet 判断内容是否与 AI 相关
- 置信度阈值：0.6
- 自动过滤非 AI 相关内容

**环境变量：**
- `ANTHROPIC_API_KEY`: Claude API 密钥

## 常用命令

### 本地开发

```bash
# 运行爬虫
python3 crawler/main.py

# 运行内容处理
python3 processor/main.py

# 生成标签图谱
python3 processor/tag_graph.py

# 本地 Hugo 开发
cd blog
hugo server

# 本地 Hugo 构建
cd blog
hugo --baseURL "https://ai-stack.site/" --minify
```

### GitHub Actions 管理

```bash
# 手动触发部署工作流
gh workflow run deploy.yml

# 查看工作流运行状态
gh run list
gh run view <run-id>

# 查看部署状态
gh api repos/{owner}/{repo}/pages
```

## 文件结构

```
ai-stack/
├── crawler/
│   └── main.py              # 爬虫主程序
├── processor/
│   ├── main.py              # 内容处理主程序
│   ├── tag_graph.py         # 标签图谱生成器
│   ├── tagger.py            # 标签生成器
│   ├── ai_filter.py         # AI 主题过滤器
│   └── tech_stack.py        # 技术栈节点定义
├── scripts/
│   └── generate_content.py  # 内容生成脚本
├── blog/
│   ├── config.toml          # Hugo 配置
│   ├── content/posts/       # 文章目录
│   ├── static/data/         # 图谱数据
│   ├── themes/              # Hugo 主题
│   └── public/              # Hugo 构建产物（gitignore）
├── .github/workflows/
│   └── deploy.yml           # 构建和部署工作流
├── .gitignore               # Git 忽略配置
└── CLAUDE.md               # 本文档
```

## Gitignore 配置

**关键配置：**
```gitignore
# Hugo 构建产物
blog/public/

# 临时文件
*.pyc
__pycache__/

# 环境变量
.env
.env.local
```

## 故障排查

### 1. GitHub Pages 未更新

**问题：** 推送 main 分支后网站未更新

**解决方案：**
```bash
# 检查 deploy.yml 运行状态
gh run list --workflow=deploy.yml

# 查看详细日志
gh run view <run-id> --log

# 手动触发部署
gh workflow run deploy.yml
```

### 2. 爬虫未运行

**问题：** 没有新的 posts 或 tag-graph.json

**解决方案：**
```bash
# 检查工作流日志中的爬虫步骤
gh run view <run-id> --log | grep -A 20 "Run crawler"

# 本地测试爬虫
python3 crawler/main.py
```

### 3. 图谱未显示

**问题：** scenarios 页面没有显示图谱

**检查项：**
1. 确认 `blog/static/data/tag-graph.json` 文件存在
2. 检查 Hugo 构建是否成功
3. 清除浏览器缓存
4. 检查前端控制台错误

### 4. Anthropic API 错误

**问题：** AI 主题过滤失败

**解决方案：**
```bash
# 检查 GitHub Secrets 配置
gh secret list

# 确认 ANTHROPIC_AUTH_TOKEN 已设置
gh secret set ANTHROPIC_AUTH_TOKEN
```

### 5. GitHub Pages 部署失败

**问题：** Deploy to GitHub Pages 步骤失败

**检查项：**
1. 确认仓库启用了 GitHub Pages
2. 检查 Pages 设置是否正确配置（Source: GitHub Actions）
3. 确认工作流有正确的权限（contents: write, pages: write, id-token: write）

## 最佳实践

1. **分支管理**
   - 所有开发都在 main 分支进行
   - 无需额外的 gh-pages 分支
   - 使用功能分支开发，然后合并到 main

2. **测试流程**
   - 在 main 分支本地测试爬虫和内容处理
   - 确认逻辑正确后推送到 main
   - GitHub Actions 自动运行部署

3. **监控和调试**
   - 定期检查 GitHub Actions 运行状态
   - 查看 main 分支的提交历史
   - 监控 https://ai-stack.site/ 的更新情况

4. **文档维护**
   - 重大流程变更时更新本文档
   - 记录故障排查经验
   - 同步更新工作流注释

## GitHub Pages 配置

### 仓库设置

1. **启用 GitHub Pages**
   - 进入仓库 Settings → Pages
   - Source 选择 "GitHub Actions"

2. **配置工作流权限**
   - Settings → Actions → General
   - Workflow permissions 选择 "Read and write permissions"
   - 勾选 "Allow GitHub Actions to create and approve pull requests"

3. **环境变量配置**
   - Settings → Secrets and variables → Actions
   - 配置以下 Secrets：
     - `ANTHROPIC_AUTH_TOKEN`: Claude API 密钥
     - `ANTHROPIC_BASE_URL`: Claude API Base URL（可选）

## 联系和支持

如有问题或建议，请查看 GitHub Issues 或联系维护团队。
