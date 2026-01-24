---
title: "Hugo 静态站点部署指南"
date: 2025-01-24T10:30:00+08:00
draft: false
tags: ["hugo", "deployment", "github-pages"]
entry_kind: "manual"
---

本文档详细介绍了使用 Hugo 构建静态站点并部署到 GitHub Pages 的完整流程。

## Hugo 基础配置

Hugo 是一个快速的静态站点生成器，支持自定义主题和丰富的内容类型。

### 环境准备

```bash
brew install hugo
hugo new site my-site
cd my-site
git submodule add https://github.com/your-theme.git themes/your-theme
```

## GitHub Pages 部署

### 分支结构

- `main` 分支：存储源代码和 Hugo 配置
- `gh-pages` 分支：存储构建后的静态文件

### 自动化部署

通过 GitHub Actions 实现自动构建和部署：

```yaml
name: Deploy to GitHub Pages
on:
  push:
    branches: [main]
jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v2
      - name: Build
        run: hugo --minify
      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
```

## 自定义域名配置

1. 在仓库根目录创建 `CNAME` 文件，内容为你的域名
2. 配置 DNS 记录指向 GitHub Pages
3. 更新 Hugo 的 `config.toml` 中的 `baseURL` 配置
