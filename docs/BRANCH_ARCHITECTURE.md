# 分支架构文档

## 概述

本项目使用两个主要分支：`main` 和 `gh-pages`，每个分支都有特定的职责和工作流程。

## 分支职责

### main 分支

**主要职责：**
- 存储源代码和配置文件
- 开发和测试新功能
- 代码质量检查和单元测试
- 触发到 gh-pages 的自动同步

**包含内容：**
- 爬虫代码 (`crawler/`)
- 内容处理器 (`processor/`)
- 发布器 (`publisher/`)
- 脚本工具 (`scripts/`)
- 配置文件 (`config/`)
- UI 组件和主题 (`blog/themes/`)
- Hugo 配置 (`blog/config.toml`)
- 依赖文件 (`requirements.txt`)
- 文档 (`docs/`)

**工作流：**
- 推送到 main 分支触发：
  1. 代码质量检查（flake8, black, isort, mypy, bandit）
  2. 单元测试（pytest）
  3. 集成测试
  4. UI 测试
  5. 部署到 gh-pages（通过 [sync-to-gh-pages.yml](../.github/workflows/sync-to-gh-pages.yml)）

### gh-pages 分支

**主要职责：**
- 存储生成的网站内容
- 执行定时内容抓取和处理
- 部署到 GitHub Pages
- 监控和健康检查

**包含内容：**
- 生成的 HTML 文件
- Markdown 文章（从 main 同步或自动生成）
- 静态资源（CSS, JS, 图片）
- GitHub Pages 配置（.nojekyll, CNAME）
- 同步的源代码（从 main）

**工作流：**
- 定时任务（每天 UTC 02:00）触发内容更新：
  1. 从 main 合并最新代码
  2. 运行内容生成脚本（15+ LLM 调用）
  3. 使用 Hugo 构建网站
  4. 部署到 GitHub Pages

## 同步机制

### main → gh-pages 同步

**触发条件：**
- 推送到 main 分支
- 手动触发 [sync-to-gh-pages.yml](../.github/workflows/sync-to-gh-pages.yml)

**同步内容：**
- UI 组件和主题文件
- 爬虫脚本和逻辑
- 配置文件
- 依赖文件

**保留内容：**
- gh-pages 特有的部署配置
- 已生成的文章和内容
- .nojekyll 和 CNAME 文件

**同步策略：**
- 使用 Git merge 策略 `-X theirs` 优先使用 gh-pages 的变更
- 忽略空格变化以减少冲突
- 强制推送（force-with-lease）确保同步成功

## 工作流文件

### Main 分支工作流

1. **[sync-to-gh-pages.yml](../.github/workflows/sync-to-gh-pages.yml)**
   - 同步 main 到 gh-pages
   - 构建 Hugo 网站
   - 推送到 gh-pages 分支

2. **[main-ci.yml](../.github/workflows/main-ci.yml)**
   - 代码质量检查
   - 单元测试
   - 集成测试
   - UI 测试
   - 部署验证

### gh-pages 分支工作流

1. **[gh-pages-content.yml](../.github/workflows/gh-pages-content.yml)**
   - 定时内容抓取
   - AI 内容增强（15+ LLM 调用）
   - Hugo 构建
   - 社交媒体发布（Twitter, Telegram）

2. **[gh-pages-ci.yml](../.github/workflows/gh-pages-ci.yml)**
   - 爬虫验证
   - 构建验证
   - 部署检查
   - 同步验证
   - 健康检查

### 监控工作流

1. **[monitoring.yml](../.github/workflows/monitoring.yml)**
   - 分支活动监控（每 6 小时）
   - 工作流状态监控
   - 同步状态监控
   - 告警通知（Slack, Telegram）

## 冲突解决策略

### 常见冲突场景

1. **代码同步冲突**
   - 使用 `git merge -X theirs` 优先保留 gh-pages 的变更
   - 自动忽略空格变化

2. **配置文件冲突**
   - main 分支的配置文件作为源
   - gh-pages 可以有特定的覆盖配置

3. **内容文件冲突**
   - 自动生成的内容保留在 gh-pages
   - 手动编辑的内容使用合并策略

### 验证脚本

[verify_sync.py](../scripts/verify_sync.py) 脚本用于：
- 检查关键目录是否同步
- 验证文件一致性
- 生成同步报告
- 检测配置完整性

## 部署流程

### 从 main 部署

```
main 分支提交
    ↓
触发 sync-to-gh-pages.yml
    ↓
同步代码到 gh-pages
    ↓
构建 Hugo 网站
    ↓
推送 gh-pages
    ↓
GitHub Pages 自动部署
```

### 定时内容更新

```
定时触发 (每天 UTC 02:00)
    ↓
触发 gh-pages-content.yml
    ↓
从 main 合并最新代码
    ↓
运行内容生成脚本
    ↓
Hugo 构建
    ↓
推送 gh-pages
    ↓
社交媒体发布
```

## 监控和告警

### 监控指标

- 分支活动（提交频率）
- 工作流状态（成功/失败率）
- 同步延迟（main → gh-pages）
- 内容新鲜度（文章更新频率）
- 构建状态（Hugo 构建成功率）

### 告警渠道

- **Slack**: 主要通知渠道
- **Telegram**: 紧急告警
- **GitHub Actions Summary**: 工作流摘要

### 告警触发条件

- 工作流失败
- 同步延迟超过 24 小时
- 内容抓取失败
- 构建失败
- 检测到安全问题

## 最佳实践

### 开发流程

1. 在 main 分支进行开发和测试
2. 提交前运行本地测试
3. 推送到 main 触发 CI/CD
4. 等待同步到 gh-pages
5. 验证部署结果

### 分支管理

- **main**: 主开发分支
- **gh-pages**: 只读部署分支（由自动化流程管理）
- **feature/***: 功能开发分支
- **hotfix/***: 紧急修复分支

### 代码提交规范

- 提交信息清晰描述变更
- 避免频繁的小提交
- 使用 `[skip ci]` 跳过不必要的 CI
- 重大变更更新文档

## 故障排查

### 同步失败

1. 检查 [sync-to-gh-pages.yml](../.github/workflows/sync-to-gh-pages.yml) 日志
2. 验证 Git 权限
3. 检查冲突解决策略

### 内容生成失败

1. 检查 API 密钥配置
2. 验证网络连接
3. 查看生成脚本日志

### 部署失败

1. 检查 GitHub Pages 配置
2. 验证 .nojekyll 文件
3. 查看 GitHub Actions 日志

## 相关文件

- [工作流配置](../.github/workflows/)
- [验证脚本](../scripts/verify_sync.py)
- [配置文件](../config/)
- [部署文档](../DEPLOYMENT.md)
- [系统设计文档](../docs/系统设计文档.md)

## 变更日志

- 2026-01-24: 初始版本，建立分支架构和工作流
