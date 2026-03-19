# AI Stack - 终端风格自动博客系统

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Hugo](https://img.shields.io/badge/Hugo-0.121+-ff4081.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-automated-blueviolet.svg)

**一个基于 GitHub Pages 的终端风格自动博客系统，每日自动从多个来源爬取内容，使用 Anthropic API 进行总结、翻译和生成，并推送到社交媒体平台。**

[功能特性](#功能特性) • [快速开始](#快速开始) • [文档](docs/README.md) • [演示](#演示) • [贡献](#贡献)

</div>

---

## 功能特性

- 🔍 **多源爬取**：支持 GitHub Trending、Hacker News、ArXiv AI 论文、掘金、博客/播客 RSS 等多个数据源
- 🤖 **AI 处理**：使用 Anthropic API 自动总结、翻译和生成内容
- 💻 **终端风格**：独特的终端界面设计，黑底绿字，等宽字体
- 🔄 **自动化**：GitHub Actions 定时任务，每日自动更新
- 📱 **多平台推送**：支持微信公众号、Twitter/X、Telegram 推送
- ⚙️ **高度可配置**：通过 YAML 配置文件灵活定制
- 🌍 **国际化**：支持多语言内容翻译
- 📊 **智能分析**：AI 生成深度评论和技术分析

## 技术栈

- **爬虫**：Python + requests + BeautifulSoup + feedparser
- **AI 处理**：Anthropic API (Claude)
- **静态站点**：Hugo
- **自动化**：GitHub Actions
- **推送**：各平台官方 API

---

## 快速开始

### 前置要求

- Python 3.11 或更高版本
- Git
- GitHub 账户
- Anthropic API 密钥

### 1. 克隆仓库

```bash
git clone https://github.com/yourusername/ai-stack.git
cd ai-stack
```

### 2. 运行设置脚本

```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

这将自动：

- 创建 Python 虚拟环境
- 安装所有依赖
- 生成配置文件模板

### 3. 配置环境变量

编辑 `.env` 文件，填入你的 API 密钥：

```bash
nano .env
```

必需配置：

```env
ANTHROPIC_AUTH_TOKEN=your_anthropic_token
ANTHROPIC_BASE_URL=https://api.minimaxi.com/anthropic
ANTHROPIC_MODEL=MiniMax-M2.7-highspeed
```

### 4. 本地测试运行

```bash
# 激活虚拟环境
source venv/bin/activate

# 生成内容
python scripts/generate_content.py

# 本地预览 Hugo 站点
cd blog
hugo server -D
```

访问 `http://localhost:1313` 查看效果。

### 5. 部署到 GitHub Pages

```bash
# 提交代码
git add .
git commit -m "Initial setup"
git push origin main
```

GitHub Actions 会自动构建和部署！

---

## 项目结构

```
ai-stack/
├── crawler/                    # 爬虫模块
│   ├── __init__.py
│   ├── github_trending.py     # GitHub Trending 爬虫
│   ├── hacker_news.py         # Hacker News 爬虫
│   ├── arxiv_papers.py        # ArXiv 论文爬虫
│   ├── juejin_rss.py          # 掘金 RSS 爬虫
│   ├── blogs_podcasts.py      # 大佬博客/播客 RSS 聚合
│   ├── dedupe.py              # 去重工具
│   └── main.py                # 爬虫调度器
├── processor/                 # 内容处理模块
│   ├── __init__.py
│   ├── anthropic_client.py    # Anthropic API 客户端
│   ├── summarizer.py          # 内容总结
│   ├── translator.py          # 翻译功能
│   ├── generator.py           # 内容生成
│   ├── enricher.py            # DeepWiki 等内容增强
│   └── main.py                # 处理流程编排
├── publisher/                 # 推送模块
│   ├── __init__.py
│   ├── twitter_publisher.py    # Twitter 推送
│   ├── telegram_publisher.py  # Telegram 推送
│   ├── wechat_publisher.py    # 微信公众号推送
│   └── main.py                # 推送调度器
├── blog/                      # Hugo 博客站点
│   ├── content/
│   │   └── posts/             # 生成的 Markdown 文章
│   ├── themes/
│   │   └── terminal-theme/    # 终端风格主题
│   ├── static/css/
│   │   └── terminal.css       # 终端样式
│   └── config.toml            # Hugo 配置
├── scripts/                   # 辅助脚本
│   ├── generate_content.py    # 内容生成主脚本
│   ├── deploy.sh              # 部署脚本
│   └── setup.sh               # 环境设置脚本
├── config/                    # 配置文件
│   ├── sources.yaml           # 爬虫源配置
│   ├── anthropic.yaml         # Anthropic API 配置
│   └── publisher.yaml         # 推送平台配置
├── docs/                      # 详细文档
│   └── README.md
├── requirements.txt           # Python 依赖
├── .github/workflows/
│   └── daily-update.yml       # GitHub Actions 定时任务
├── .gitignore               # Git 忽略文件
└── README.md               # 项目说明
```

---

## 配置说明

### 爬虫源配置 (config/sources.yaml)

```yaml
sources:
  github_trending:
    enabled: true
    period: daily             # daily 或 weekly
    language: all             # all, python, javascript 等
    limit: 10
    spoken_language_code: 'zh'

  hacker_news:
    enabled: true
    limit: 20

  arxiv_ai:
    enabled: true
    categories:
      - 'cs.AI'
      - 'cs.LG'
      - 'cs.CL'
    limit: 10
    sort_by: 'submittedDate'

  juejin:
    enabled: true
    tags:
      - '人工智能'
      - '机器学习'
    limit: 5

  blogs_podcasts:
    enabled: true
    limit: 10
    feeds:
      - name: "Andrej Karpathy Blog"
        url: "https://karpathy.github.io/feed.xml"
        type: "blog"
      - name: "Lex Fridman Podcast"
        url: "https://lexfridman.com/feed/podcast/"
        type: "podcast"
```

### Anthropic API 配置 (config/anthropic.yaml)

```yaml
anthropic:
  api_key: "${ANTHROPIC_AUTH_TOKEN}"
  base_url: "${ANTHROPIC_BASE_URL}"
  model: "${ANTHROPIC_MODEL}"
  max_tokens: 4096
  temperature: 0.7
  disable_thinking: true

  summary:
    max_length: 200
    style: "concise"      # concise, detailed, bullet

  translation:
    default_target_lang: "zh"
    preserve_formatting: true

  generation:
    intro_length: 100
    comment_length: 300
    style: "professional"
```

### 推送平台配置 (config/publisher.yaml)

```yaml
publishers:
  twitter:
    enabled: false          # 改为 true 启用
    auto_tweet: true
    max_length: 280

  telegram:
    enabled: false
    chat_id: "${TELEGRAM_CHAT_ID}"
    bot_token: "${TELEGRAM_BOT_TOKEN}"

  wechat:
    enabled: false
    app_id: "${WECHAT_APPID}"
    app_secret: "${WECHAT_SECRET}"
```

---

## 使用指南

### 日常使用

**手动生成内容：**

```bash
python scripts/generate_content.py
```

**长时间抓取（例如 8 小时）+ 去重：**

```bash
python scripts/generate_content.py --crawl-duration-hours 8 --crawl-interval-minutes 30
```

**预览本地站点：**

```bash
cd blog
hugo server -D
```

**构建生产版本：**

```bash
cd blog
hugo --minify
```

### GitHub Actions

- **定时任务**：每天 UTC 时间 02:00（北京时间 10:00）自动运行
- **手动触发**：访问 Actions 页面，点击 "Run workflow"

### 自定义

**添加新的爬虫源：**

1. 在 `crawler/` 目录创建新文件
2. 在 `config/sources.yaml` 添加配置
3. 在 `crawler/main.py` 注册爬虫

**自定义终端主题：**
编辑 `blog/themes/terminal-theme/assets/css/style.css`

---

## API 密钥配置

在 GitHub 仓库的 **Settings > Secrets and variables > Actions** 中添加：

### 必需的 Secrets

- `ANTHROPIC_AUTH_TOKEN` - 你的 Anthropic API 密钥
- `ANTHROPIC_BASE_URL` - Anthropic API 基础 URL
- `ANTHROPIC_MODEL` - 模型名称，例如 `MiniMax-M2.7-highspeed`

### 可选的 Secrets

**Twitter 推送：**

- `TWITTER_API_KEY`
- `TWITTER_BEARER_TOKEN`

**Telegram 推送：**

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

**微信推送：**

- `WECHAT_APPID`
- `WECHAT_SECRET`

详细的 API 密钥获取方法请查看 [详细文档](docs/README.md)。

---

## 演示

### 博客页面

[访问演示站点](https://yourusername.github.io/ai-stack/) 查看终端风格博客效果。

### 文章示例

生成的文章包含：

- 原始内容链接和信息
- AI 生成的中文总结
- 翻译内容
- AI 评论和深度分析

### 社交媒体推送

内容会自动推送到启用的平台：

- Twitter/X（短推文）
- Telegram（富文本消息）
- 微信公众号（图文消息）

---

## 贡献

欢迎贡献！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 贡献方向

- 新增数据源爬虫
- 改进终端主题样式
- 优化 AI 提示词
- 添加新的推送平台
- 文档改进

---

## 文档

查看 [详细文档](docs/README.md) 了解：

- 完整的配置说明
- 故障排查指南
- 开发指南
- API 密钥获取方法

---

## 常见问题

**Q: 如何修改爬取频率？**

A: 编辑 `.github/workflows/daily-update.yml`，修改 `cron` 表达式。

**Q: 如何调整 AI 生成内容长度？**

A: 编辑 `config/anthropic.yaml` 中的 `intro_length` 和 `comment_length`。

**Q: 如何自定义终端颜色？**

A: 编辑 `blog/themes/terminal-theme/assets/css/style.css` 中的 CSS 变量。

**Q: 爬虫失败了怎么办？**

A: 查看日志，可能是网络问题或网站结构变更。可以尝试更换代理或联系开发者。

更多问题请查看 [详细文档](docs/README.md) 或提交 Issue。

---

## 许可证

本项目采用 [MIT 许可证](LICENSE)。

---

## 致谢

- [Hugo](https://gohugo.io/) - 强大的静态站点生成器
- [Anthropic](https://www.anthropic.com/) - AI API 提供商
- [GitHub Actions](https://github.com/features/actions) - CI/CD 平台

---

---

<div align="center">

**如果这个项目对你有帮助，请给个 ⭐ Star！**

Made with ❤️ by AI Stack

</div>
