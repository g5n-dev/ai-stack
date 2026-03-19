# AI Stack 部署指南 - 使用 ai-stack.site 域名

本文档详细介绍如何将 ai-stack 项目部署到 GitHub Pages，并通过自定义域名 `ai-stack.site` 访问。

---

## 📋 部署前准备

### 1. GitHub 仓库准备

1. **创建 GitHub 仓库**
   - 访问 https://github.com/new
   - 仓库名称：`ai-stack`
   - 设置为 Public（免费 GitHub Pages 需要）
   - 不要初始化 README、.gitignore 或 License

2. **初始化本地 Git 仓库**
   ```bash
   cd /Users/frank/WorkPlace/ai-stack
   git init
   git add .
   git commit -m "Initial commit"
   ```

3. **关联远程仓库并推送**
   ```bash
   git remote add origin https://github.com/yourusername/ai-stack.git
   git branch -M main
   git push -u origin main
   ```

---

## 🔐 配置 GitHub Secrets

### 必需的 Secrets

进入 GitHub 仓库页面：**Settings → Secrets and variables → Actions → New repository secret**

添加以下密钥：

| Secret 名称 | 说明 | 示例 |
|------------|------|------|
| `ANTHROPIC_AUTH_TOKEN` | Anthropic API 密钥 | `sk-ant-xxxxx` |
| `ANTHROPIC_BASE_URL` | API 基础 URL | `https://api.minimaxi.com/anthropic` |
| `ANTHROPIC_MODEL` | 模型名称 | `MiniMax-M2.7-highspeed` |

### 可选的 Secrets（用于社交媒体推送）

| Secret 名称 | 说明 |
|------------|------|
| `TWITTER_API_KEY` | Twitter API 密钥 |
| `TWITTER_API_SECRET` | Twitter API 密钥 |
| `TWITTER_ACCESS_TOKEN` | Twitter 访问令牌 |
| `TWITTER_ACCESS_TOKEN_SECRET` | Twitter 访问令牌密钥 |
| `TWITTER_BEARER_TOKEN` | Twitter Bearer 令牌 |
| `TELEGRAM_BOT_TOKEN` | Telegram Bot 令牌 |
| `TELEGRAM_CHAT_ID` | Telegram 聊天 ID |
| `WECHAT_APPID` | 微信应用 ID |
| `WECHAT_SECRET` | 微信应用密钥 |

---

## 🌐 配置 GitHub Pages

### 1. 启用 GitHub Pages

1. 进入 GitHub 仓库
2. 点击 **Settings**
3. 左侧菜单选择 **Pages**
4. 在 **Build and deployment** 部分：
   - **Source**: 选择 `GitHub Actions`
   - 点击 **Save**

### 2. 配置自定义域名

#### 方法一：直接在 GitHub Pages 设置（推荐）

1. 在 Pages 设置页面找到 **Custom domain**
2. 输入：`ai-stack.site`
3. 点击 **Save**

GitHub 会自动创建 CNAME 文件，并提供 DNS 配置信息。

#### 方法二：手动创建 CNAME 文件

在 `blog` 目录下创建 `static/CNAME` 文件：

```bash
cd blog
mkdir -p static
echo "ai-stack.site" > static/CNAME
```

---

## 🌍 域名 DNS 配置

### 配置 DNS 记录

登录你的域名服务商（如阿里云、腾讯云、GoDaddy 等），为 `ai-stack.site` 添加 DNS 记录：

#### 如果使用 GitHub Pages 标准方式：

**记录类型**: `CNAME`
**主机记录**: `@` 或留空
**记录值**: `yourusername.github.io`

#### 如果使用 GitHub Pages 专用域名（推荐）：

**记录类型**: `A` 记录
**主机记录**: `@` 或留空
**记录值**: 选择以下任一 IP 地址：
- `185.199.108.153`
- `185.199.109.153`
- `185.199.110.153`
- `185.199.111.153`

**记录类型**: `CNAME`
**主机记录**: `www`
**记录值**: `yourusername.github.io`

### 等待 DNS 生效

DNS 生效通常需要 10 分钟到 48 小时，可以使用以下命令检查：

```bash
# 检查 A 记录
dig ai-stack.site

# 检查 CNAME 记录
dig www.ai-stack.site

# 或者使用在线工具
# https://whatsmydns.net/
```

---

## 🚀 配置 GitHub Actions Workflow

### 检查 Workflow 文件

确保 `.github/workflows/daily-update.yml` 存在并且配置正确。

文件已经存在于项目中，它会：
- 每天自动运行（UTC 时间 02:00 = 北京时间 10:00）
- 自动生成内容
- 构建 Hugo 站点
- 部署到 GitHub Pages

### 手动触发部署

如果需要立即部署：

1. 进入 GitHub 仓库
2. 点击 **Actions** 标签页
3. 选择 **Daily Blog Update** workflow
4. 点击右侧 **Run workflow** 按钮
5. 点击 **Run workflow** 确认

---

## 🔧 修改配置文件

### 1. 修改 `blog/config.toml`

将 baseURL 改为你的域名：

```toml
baseURL = "https://ai-stack.site/"
languageCode = "zh-CN"
title = "AI Stack - 终端风格博客"
theme = "terminal-theme"

[params]
  description = "每日 AI 资讯精选 - GitHub Trending, Hacker News, ArXiv 论文"
  author = "AI Stack Bot"
  github = "https://github.com/yourusername/ai-stack"
  # ... 其他配置保持不变
```

将 `yourusername` 替换为你的 GitHub 用户名。

### 2. 更新 README.md 中的链接

搜索并替换：
- `yourusername.github.io` → `ai-stack.site`
- `yourusername` → 你的 GitHub 用户名

---

## ✅ 验证部署

### 1. 检查 GitHub Actions

进入仓库的 **Actions** 页面，查看 workflow 是否成功运行。

### 2. 访问网站

等待 DNS 生效后，访问：
- https://ai-stack.site
- https://www.ai-stack.site

### 3. 检查 HTTPS 证书

GitHub Pages 会自动为你的自定义域名提供 HTTPS 证书。在 Pages 设置页面，找到 **Enforce HTTPS** 并开启。

---

## 📊 监控和维护

### 查看部署日志

```bash
# 查看 GitHub Actions 运行日志
# 在仓库的 Actions 页面点击具体的工作流运行记录
```

### 查看网站状态

```bash
# 检查网站是否可访问
curl -I https://ai-stack.site

# 查看 DNS 解析
nslookup ai-stack.site
```

---

## 🔄 更新内容

### 自动更新

GitHub Actions 每天自动运行，无需手动干预。

### 手动更新

如需立即更新内容：

```bash
# 方法 1：在 GitHub Actions 页面手动触发
# （推荐）

# 方法 2：本地生成并提交
cd /Users/frank/WorkPlace/ai-stack
source venv/bin/activate
python scripts/generate_content.py
git add .
git commit -m "Update content"
git push origin main
```

---

## 🐛 故障排查

### 问题 1：网站无法访问

**检查清单：**
- [ ] DNS 记录是否正确配置
- [ ] DNS 是否已生效（等待 10-48 小时）
- [ ] GitHub Pages 是否已启用
- [ ] Workflow 是否成功运行
- [ ] CNAME 文件是否存在

### 问题 2：HTTPS 证书未生效

**解决方案：**
1. 在 Pages 设置中检查 **Enforce HTTPS** 选项
2. 等待几小时让证书生成
3. 如果仍有问题，删除自定义域名后重新添加

### 问题 3：部署失败

**检查步骤：**
1. 查看 GitHub Actions 日志
2. 检查 Secrets 是否正确配置
3. 检查 Python 和 Hugo 版本
4. 查看是否有语法错误

---

## 📚 附录

### A. 完整命令参考

```bash
# 初始化仓库
git init
git add .
git commit -m "Initial commit"

# 关联远程仓库
git remote add origin https://github.com/yourusername/ai-stack.git
git branch -M main
git push -u origin main

# 本地测试
python scripts/generate_content.py
cd blog && hugo server -D

# 查看 DNS
dig ai-stack.site
dig www.ai-stack.site

# 检查网站状态
curl -I https://ai-stack.site
```

### B. 环境变量模板

创建 `.env` 文件（不要提交到 Git）：

```env
ANTHROPIC_AUTH_TOKEN=your_token_here
ANTHROPIC_BASE_URL=https://api.minimaxi.com/anthropic
ANTHROPIC_MODEL=MiniMax-M2.7-highspeed
```

### C. 常用链接

- GitHub Pages 文档：https://docs.github.com/pages
- GitHub Actions 文档：https://docs.github.com/actions
- Hugo 文档：https://gohugo.io/documentation/
- DNS 检测工具：https://whatsmydns.net/

---

## 🎉 完成！

现在你的 AI Stack 博客应该可以通过 https://ai-stack.site 访问了。

如果遇到任何问题，请参考故障排查章节或提交 Issue。

---

**需要帮助？**
- 📧 Email: your-email@example.com
- 🐛 Issues: https://github.com/yourusername/ai-stack/issues
