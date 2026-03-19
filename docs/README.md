# AI Stack 博客系统 - 详细文档

## 目录

- [快速开始](#快速开始)
- [项目结构](#项目结构)
- [配置说明](#配置说明)
- [使用指南](#使用指南)
- [API 密钥配置](#api-密钥配置)
- [故障排查](#故障排查)
- [开发指南](#开发指南)

---

## 快速开始

### 前置要求

- Python 3.11 或更高版本
- Git
- GitHub 账户（用于 GitHub Pages 部署）
- Anthropic API 密钥

### 安装步骤

1. **克隆仓库**

```bash
git clone https://github.com/yourusername/ai-stack.git
cd ai-stack
```

2. **运行设置脚本**

```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

设置脚本会自动：
- 检查 Python 版本
- 创建虚拟环境
- 安装依赖
- 创建配置文件

3. **配置环境变量**

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

可选配置（用于社交媒体推送）：
```env
TWITTER_API_KEY=your_twitter_key
TWITTER_BEARER_TOKEN=your_bearer_token
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
WECHAT_APPID=your_wechat_appid
WECHAT_SECRET=your_wechat_secret
```

4. **测试运行**

```bash
# 激活虚拟环境
source venv/bin/activate

# 生成内容
python scripts/generate_content.py

# 长时间抓取（例如 8 小时）+ 去重
python scripts/generate_content.py --crawl-duration-hours 8 --crawl-interval-minutes 30

# 本地预览 Hugo 站点
cd blog
hugo server -D
```

访问 `http://localhost:1313` 查看效果。

5. **部署到 GitHub Pages**

```bash
# 提交代码
git add .
git commit -m "Initial commit"
git push origin main

# GitHub Actions 会自动部署
```

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
│
├── processor/                 # 内容处理模块
│   ├── __init__.py
│   ├── anthropic_client.py    # Anthropic API 客户端
│   ├── summarizer.py          # 内容总结
│   ├── translator.py          # 翻译功能
│   ├── generator.py           # 内容生成
│   ├── enricher.py            # DeepWiki 等内容增强
│   └── main.py                # 处理流程编排
│
├── publisher/                 # 推送模块
│   ├── __init__.py
│   ├── twitter_publisher.py    # Twitter 推送
│   ├── telegram_publisher.py  # Telegram 推送
│   ├── wechat_publisher.py    # 微信公众号推送
│   └── main.py                # 推送调度器
│
├── blog/                      # Hugo 博客站点
│   ├── content/
│   │   └── posts/             # 生成的 Markdown 文章
│   ├── themes/
│   │   └── terminal-theme/    # 终端风格主题
│   │       ├── layouts/          # 模板文件
│   │       ├── assets/          # 静态资源
│   │       │   └── css/
│   │       │       └── style.css
│   │       └── archetypes/      # 内容原型
│   └── config.toml            # Hugo 配置
│
├── scripts/                   # 辅助脚本
│   ├── generate_content.py    # 内容生成主脚本
│   ├── deploy.sh              # 部署脚本
│   └── setup.sh               # 环境设置脚本
│
├── config/                    # 配置文件
│   ├── sources.yaml           # 爬虫源配置
│   ├── anthropic.yaml         # Anthropic API 配置
│   └── publisher.yaml         # 推送平台配置
│
├── .github/workflows/
│   └── daily-update.yml       # GitHub Actions 定时任务
│
├── requirements.txt           # Python 依赖
├── .env.example              # 环境变量示例
├── .gitignore               # Git 忽略文件
└── README.md               # 项目说明
```

---

## 配置说明

### 爬虫源配置 (config/sources.yaml)

```yaml
sources:
  github_trending:
    enabled: true              # 是否启用
    period: daily             # 期间: daily 或 weekly
    language: all             # 编程语言: all, python, javascript 等
    limit: 10               # 获取数量限制
    spoken_language_code: 'zh' # 口语代码

  hacker_news:
    enabled: true
    limit: 20

  arxiv_ai:
    enabled: true
    categories:             # ArXiv 分类
      - 'cs.AI'           # 人工智能
      - 'cs.LG'           # 机器学习
      - 'cs.CL'           # 计算语言学
    limit: 10
    sort_by: 'submittedDate'

  juejin:
    enabled: true
    tags:                  # 掘金标签过滤
      - '人工智能'
      - '机器学习'
      - '深度学习'
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
  api_key: "${ANTHROPIC_AUTH_TOKEN}"  # 从环境变量读取
  base_url: "${ANTHROPIC_BASE_URL}"
  model: "${ANTHROPIC_MODEL}"
  max_tokens: 4096
  temperature: 0.7               # 创造性 (0-2)
  disable_thinking: true

  summary:
    max_length: 200             # 总结最大字数
    style: "concise"            # 风格: concise, detailed, bullet

  translation:
    default_target_lang: "zh"     # 默认翻译目标语言
    preserve_formatting: true

  generation:
    intro_length: 100           # 引言长度
    comment_length: 300          # 评论长度
    style: "professional"        # 风格
```

### 推送平台配置 (config/publisher.yaml)

```yaml
publishers:
  wechat:
    enabled: false              # 是否启用微信推送
    auto_post: true
    media_id: null
    app_id: "${WECHAT_APPID}"
    app_secret: "${WECHAT_SECRET}"

  twitter:
    enabled: false              # 是否启用 Twitter 推送
    auto_tweet: true
    max_length: 280
    api_key: "${TWITTER_API_KEY}"
    # ... 其他 Twitter 配置

  telegram:
    enabled: false              # 是否启用 Telegram 推送
    chat_id: "${TELEGRAM_CHAT_ID}"
    bot_token: "${TELEGRAM_BOT_TOKEN}"
    parse_mode: "HTML"
    disable_web_page_preview: false
```

---

## 使用指南

### 日常使用

#### 1. 手动生成内容

```bash
python scripts/generate_content.py
```

长时间抓取（例如 8 小时）：

```bash
python scripts/generate_content.py --crawl-duration-hours 8 --crawl-interval-minutes 30
```

这会执行以下步骤：
1. 从所有启用的源爬取内容
2. 使用 Anthropic API 处理内容（总结、翻译、生成）
3. 生成 Markdown 文章到 `blog/content/posts/`
4. 推送到启用的社交媒体平台

#### 2. 预览本地站点

```bash
cd blog
hugo server -D
```

访问 `http://localhost:1313` 查看效果。

#### 3. 构建生产版本

```bash
cd blog
hugo --minify
```

生成的文件在 `blog/public/` 目录。

#### 4. 部署到 GitHub Pages

```bash
# 使用脚本部署
chmod +x scripts/deploy.sh
./scripts/deploy.sh

# 或手动推送
git add .
git commit -m "Update blog"
git push origin main
```

GitHub Actions 会自动触发部署。

### 定时任务

GitHub Actions 配置为每天 UTC 时间 02:00（北京时间 10:00）自动运行。

你也可以手动触发：
1. 访问 GitHub 仓库的 Actions 页面
2. 选择 "Daily Blog Update" 工作流
3. 点击 "Run workflow"

---

## API 密钥配置

### GitHub Secrets 配置

在 GitHub 仓库设置中添加以下 Secrets：

**必需的 Secrets：**
- `ANTHROPIC_AUTH_TOKEN` - 你的 Anthropic API 密钥
- `ANTHROPIC_BASE_URL` - Anthropic API 基础 URL
- `ANTHROPIC_MODEL` - 模型名称，例如 `MiniMax-M2.7-highspeed`

**可选的 Secrets：**

**Twitter 推送：**
- `TWITTER_API_KEY`
- `TWITTER_API_SECRET`
- `TWITTER_ACCESS_TOKEN`
- `TWITTER_ACCESS_TOKEN_SECRET`
- `TWITTER_BEARER_TOKEN`

**Telegram 推送：**
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

**微信推送：**
- `WECHAT_APPID`
- `WECHAT_SECRET`

### 获取 API 密钥

#### Anthropic API

1. 访问 [Anthropic 控制台](https://console.anthropic.com/)
2. 注册/登录账户
3. 生成 API 密钥
4. 复制到 GitHub Secrets

#### Twitter API

1. 访问 [Twitter Developer Portal](https://developer.twitter.com/)
2. 创建应用
3. 获取 API 密钥和访问令牌
4. 复制到 GitHub Secrets

#### Telegram Bot Token

1. 在 Telegram 中与 [@BotFather](https://t.me/BotFather) 对话
2. 发送 `/newbot`
3. 按提示创建机器人
4. 复制 Bot Token

**获取 Chat ID：**
1. 在 Telegram 中与 [@userinfobot](https://t.me/userinfobot) 对话
2. 获取你的 Chat ID
3. 如果是群组/频道，需要将机器人添加为管理员

#### 微信公众号 API

1. 访问 [微信公众平台](https://mp.weixin.qq.com/)
2. 登录开发者中心
3. 获取 AppID 和 AppSecret

---

## 故障排查

### 常见问题

**Q: 爬虫失败，无法获取内容**

A: 检查网络连接，某些网站可能有反爬机制。可以尝试：
- 更换 User-Agent
- 添加代理
- 检查网站是否变更了结构

**Q: Anthropic API 调用失败**

A: 检查：
- API 密钥是否正确
- 账户是否有足够的配额
- 网络是否可以访问 API

**Q: Hugo 构建失败**

A: 检查：
- Hugo 是否正确安装
- 配置文件语法是否正确
- Markdown 文章格式是否正确

**Q: GitHub Actions 部署失败**

A: 检查：
- GitHub Secrets 是否正确配置
- workflow 文件语法是否正确
- 仓库权限设置

**Q: 社交媒体推送失败**

A: 检查：
- API 密钥是否正确
- API 权限是否足够
- 内容是否符合平台规范

### 日志查看

**本地运行：**
```bash
# 查看详细日志
python scripts/generate_content.py --log-level DEBUG
```

**GitHub Actions：**
1. 访问仓库的 Actions 页面
2. 点击失败的工作流运行
3. 查看详细日志

---

## 开发指南

### 添加新的爬虫源

1. 在 `crawler/` 目录创建新文件，例如 `custom_crawler.py`：

```python
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class CustomCrawler:
    def __init__(self, config):
        self.config = config

    def fetch(self) -> List[Dict]:
        """实现爬取逻辑"""
        try:
            # 爬取内容
            items = []
            # ...
            return items
        except Exception as e:
            logger.error(f"Failed to fetch: {e}")
            return []
```

2. 在 `crawler/main.py` 中注册：

```python
from .custom_crawler import CustomCrawler

class CrawlerOrchestrator:
    def _init_crawlers(self):
        # ...
        if config.get('custom', {}).get('enabled', False):
            crawlers['custom'] = CustomCrawler(config['custom'])
```

3. 在 `config/sources.yaml` 中添加配置：

```yaml
sources:
  custom:
    enabled: true
    limit: 5
```

### 自定义终端主题

编辑 `blog/themes/terminal-theme/assets/css/style.css` 来定制样式：

```css
/* 修改颜色 */
:root {
    --bg-color: #0d1117;
    --accent-color: #00ff00;
    --text-color: #c9d1d9;
}

/* 修改字体 */
body {
    font-family: 'Your-Font', monospace;
}
```

### 添加新的推送平台

1. 在 `publisher/` 目录创建新文件，例如 `mastodon_publisher.py`：

```python
class MastodonPublisher:
    def __init__(self):
        # 初始化客户端
        pass

    def publish_content(self, content: Dict) -> bool:
        # 实现推送逻辑
        pass
```

2. 在 `publisher/main.py` 中注册：

```python
from .mastodon_publisher import MastodonPublisher

class PublisherOrchestrator:
    def _init_publishers(self):
        # ...
        if config.get('mastodon', {}).get('enabled', False):
            publishers['mastodon'] = MastodonPublisher()
```

---

## 贡献

欢迎贡献！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

---

## 联系方式

如有问题或建议，请：
- 提交 [Issue](https://github.com/yourusername/ai-stack/issues)
- 发送邮件至 [your-email@example.com]
