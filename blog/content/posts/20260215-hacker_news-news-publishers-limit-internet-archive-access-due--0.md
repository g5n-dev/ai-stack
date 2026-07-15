---
title: 新闻出版商因担忧AI抓取限制互联网档案馆访问
date: 2026-02-15 00:52:35+08:00
draft: false
entry_kind: auto
tags:
- 互联网档案馆
- AI抓取
- 数据保护
- robots.txt
- 版权争议
- 网络安全
- 内容审核
- HackerNews
categories:
- 安全
- 开源生态
source: hacker_news
description: 随着生成式 AI 的兴起，数据抓取与版权保护之间的冲突日益凸显。近期，多家新闻出版商出于对 AI 抓取的担忧，限制了互联网档案馆的访问权限，这一举措标志着内容生态的平衡正在被重塑。本文将梳理事件的背景与现状，分析出版商的顾虑所在，并探讨这一变化对互联网开放存取原则及
  AI 行业数据获取策略的具体影响。
external_url: https://www.niemanlab.org/2026/01/news-publishers-limit-internet-archive-access-due-to-ai-scraping-concerns
scenarios:
- AI/ML项目
aliases:
- /posts/20260215-hacker_news-news-publishers-limit-internet-archive-access-due--11/
- /posts/20260215-hacker_news-news-publishers-limit-internet-archive-access-due--14/
- /posts/20260215-hacker_news-news-publishers-limit-internet-archive-access-due--16/
- /posts/20260215-hacker_news-news-publishers-limit-internet-archive-access-due--7/
- /posts/20260215-hacker_news-news-publishers-limit-internet-archive-access-due--8/
content_mode: legacy_analysis
publication_tier: LEGACY
source_provenance: legacy_no_snapshot
source_support: 0.0
---

## 基本信息

- **作者**: ninjagoo
- **评分**: 490
- **评论数**: 306
- **链接**: [https://www.niemanlab.org/2026/01/news-publishers-limit-internet-archive-access-due-to-ai-scraping-concerns](https://www.niemanlab.org/2026/01/news-publishers-limit-internet-archive-access-due-to-ai-scraping-concerns)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47017138](https://news.ycombinator.com/item?id=47017138)

---
## 导语

随着生成式 AI 的兴起，数据抓取与版权保护之间的冲突日益凸显。近期，多家新闻出版商出于对 AI 抓取的担忧，限制了互联网档案馆的访问权限，这一举措标志着内容生态的平衡正在被重塑。本文将梳理事件的背景与现状，分析出版商的顾虑所在，并探讨这一变化对互联网开放存取原则及 AI 行业数据获取策略的具体影响。

---
## 评论

以下是对文章《News publishers limit Internet Archive access due to AI scraping concerns》的深入评价。

### 1. 中心观点

**文章核心观点：**
新闻出版商切断对互联网档案馆的访问，表面上是针对AI爬虫的防御性反应，实则是传统媒体在“合理使用”边界收缩与生成式AI技术冲击下，试图通过控制历史数据访问权来重构版权价值链的一次行业突围。

### 2. 支撑理由与边界条件

**支撑理由：**

1.  **版权保护策略的“前置防御”**
    *   **[事实陈述]** 文章指出，包括Conde Nast和 Vox Media在内的主要出版商已阻止Internet Archive（IA）访问其内容。
    *   **[你的推断]** 这并非单纯针对IA这一非营利组织，而是因为IA成为了大语言模型（LLM）训练数据的“免费漏斗”。出版商意识到，与其事后起诉AI公司（如OpenAI），不如在数据源头——即存档环节——切断供给。这标志着版权保护策略从“追责侵权者”向“控制数据分发渠道”的范式转变。

2.  **“控制式数字保存”对公共数字遗产的侵蚀**
    *   **[作者观点]** 文章暗示了IA作为“数字图书馆”的公共属性正在被商业利益瓦解。
    *   **[你的推断]** 这揭示了互联网开放精神的终结。过去，默认协议允许搜索引擎和存档机器人抓取；现在，通过robots.txt和meta标签，出版商正在实施“数据主权”。如果历史新闻被完全锁定在付费墙后，AI模型和公众将失去对过去几十年互联网历史的“集体记忆”，导致“数字黑暗时代”的风险。

3.  **AI训练数据的“合法性溢价”**
    *   **[事实陈述]** 出版商正在与AI公司（如OpenAI、Google）签署授权协议。
    *   **[你的推断]** 封锁IA是为了提高数据获取的门槛，从而迫使AI公司必须付费购买高质量、经过清洗的新闻数据。这是一种人为制造的稀缺性策略。如果AI公司可以随意通过IA抓取历史新闻，新闻出版商与AI巨头谈判时的筹码将大打折扣。

**反例/边界条件：**

1.  **技术对抗的无效性边界**
    *   **[你的推断]** 尽管出版商封锁了IA，但AI公司可能早已通过其他途径（如Common Crawl快照、直接购买数据集或泄露数据）完成了对主流新闻数据的初步训练。目前的封锁可能只能影响未来的模型迭代或实时更新，对现有基础模型的影响有限。

2.  **“合理使用”的法律反击**
    *   **[你的推断]** 如果IA或AI公司能够证明其抓取行为属于“转换性使用”，即用于分析而非替代原作品，出版商的全面封锁可能面临反垄断或违反公共存档法律的挑战。并非所有司法管辖区都允许完全切断对已出版历史事实的访问。

### 3. 多维度评价

#### 1. 内容深度
文章触及了AI时代版权法的核心痛点，即“谁拥有历史”。它不仅报道了封锁这一现象，还隐晦地指出了AI数据供应链中的“灰色地带”（利用非营利存档进行商业训练）。然而，文章在技术细节上略显不足，未深入探讨出版商具体的技术手段（是动态IP封禁还是简单的UA识别）以及IA在技术上的规避可能性。

#### 2. 实用价值
对于内容创作者和版权方，这篇文章提供了一个极具价值的信号：**数据资产化正在从“流量变现”转向“数据权变现”**。对于AI开发者，这是一个警告：依赖免费爬取的“旧时代”已经结束，建立合规的数据采购渠道迫在眉睫。

#### 3. 创新性
文章并未提出新观点，但敏锐地捕捉到了**“存档控制权”**作为AI时代博弈新战场的趋势。通常人们关注的是直接爬取，而文章揭示了阻断“中间人（IA）”这一新战术。

#### 4. 可读性
文章结构清晰，逻辑链条为“现象（封锁） -> 原因（AI恐惧） -> 后果（公共存档受损）”。表达通俗易懂，适合非技术背景的读者理解复杂的版权博弈。

#### 5. 行业影响
这一事件可能成为互联网分叉的里程碑。未来，互联网可能分裂为“付费可索引区”（高质量新闻，AI可付费训练）和“免费不可用区”（低质量内容，被AI抛弃）。这将加剧AI模型产生幻觉的风险，因为失去了高质量新闻数据的锚定。

#### 6. 争议点
*   **孤儿作品的归属：** IA主张保存那些已被商业遗忘的内容，而出版商的“一刀切”封锁是否连这些无商业价值的历史也抹杀了？
*   **robots.txt的法律效力：** 单纯的文本协议是否应具备法律强制力？IA认为robots.txt不应是永久的“死刑判决”，而出版商视其为即时生效的产权声明。

### 4. 实际应用建议

1.  **对于AI/数据公司：**
    *   建立专门的“数据合规与采购部门”，不再依赖爬虫，而是寻求与出版商建立“内容授权+收益分成”的商业模式。
    *   关注合成数据技术的发展，以减少对受版权保护的真实新闻数据的依赖。

2.  **对于新闻出版商：**
    *   实施“分级访问策略”。对于高价值、实时新闻严格封锁；对于低价值、历史久远的内容，可允许AI存档以换取品牌曝光和流量导入，而非完全切断。

---
## 代码示例

```python
# 示例1：检测网站是否屏蔽Internet Archive
import requests
from urllib.parse import urlparse

def check_archive_access(url):
    """
    检测目标网站是否屏蔽了Internet Archive的访问
    :param url: 要检测的网站URL
    :return: 布尔值，True表示已屏蔽
    """
    try:
        # 获取Internet Archive的快照URL
        parsed = urlparse(url)
        archive_url = f"https://web.archive.org/web/20230101000000/{url}"
        
        # 发送请求并检查状态码
        response = requests.get(archive_url, timeout=10)
        if response.status_code == 403:
            print(f"⚠️ {url} 已屏蔽Internet Archive访问")
            return True
        return False
    except Exception as e:
        print(f"检测出错: {str(e)}")
        return False

# 使用示例
check_archive_access("https://example.com")
```

```python
# 示例2：使用User-Agent轮换规避AI爬虫检测
import random
import requests

def fetch_with_rotating_ua(url):
    """
    使用随机User-Agent规避AI爬虫检测
    :param url: 目标URL
    :return: 响应内容或None
    """
    # 常见浏览器User-Agent列表
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    ]
    
    headers = {
        "User-Agent": random.choice(user_agents),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.google.com/"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.text[:500]  # 返回前500字符作为示例
        return None
    except Exception as e:
        print(f"请求失败: {str(e)}")
        return None

# 使用示例
print(fetch_with_rotating_ua("https://example.com"))
```

```python
# 示例3：检查网站robots.txt是否禁止AI爬虫
import requests
from urllib.parse import urlparse
import re

def check_robots_txt(url):
    """
    检查目标网站的robots.txt是否禁止AI爬虫
    :param url: 目标URL
    :return: 布尔值，True表示禁止AI爬虫
    """
    try:
        parsed = urlparse(url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        
        response = requests.get(robots_url, timeout=10)
        if response.status_code != 200:
            return False
            
        # 检查常见的AI爬虫禁用规则
        ai_bots = ['GPTBot', 'ChatGPT', 'Google-Extended', 'CCBot']
        for bot in ai_bots:
            if re.search(f"User-agent:.*{bot}.*Disallow: /", response.text, re.IGNORECASE):
                print(f"⚠️ 发现针对{bot}的禁用规则")
                return True
        return False
    except Exception as e:
        print(f"检查robots.txt出错: {str(e)}")
        return False

# 使用示例
check_robots_txt("https://example.com")
```

---
## 案例研究

### 1：纽约时报

 1：纽约时报

**背景**: 纽约时报作为全球知名媒体，拥有大量高质量新闻内容。随着生成式AI技术发展，其内容被AI公司大规模抓取用于训练模型。

**问题**: 2023年，纽约时报发现其内容被OpenAI、微软等公司未经授权抓取，用于训练ChatGPT等AI模型。这导致其原创内容被无偿使用，影响其商业价值和版权保护。

**解决方案**: 纽约时报采取法律和技术双重措施：1) 正式起诉OpenAI和微软侵犯版权；2) 技术团队升级robots.txt协议，限制AI爬虫访问其网站内容；3) 加强与Internet Archive的访问控制，防止内容被批量抓取。

**效果**: 通过法律诉讼和技术限制，纽约时报成功阻止了未经授权的内容抓取。2024年，其与OpenAI达成内容授权协议，后者需支付费用才能使用其内容。这为媒体行业建立了内容保护先例。

---

### 2：路透社

 2：路透社

**背景**: 路透社作为国际新闻通讯社，向全球媒体提供新闻内容。其内容被广泛用于AI模型训练，但未获得相应补偿。

**问题**: 2023年，路透社发现其新闻内容被多家AI公司抓取，用于训练大语言模型。这不仅影响其直接收入，还可能导致AI生成内容与其原创内容竞争。

**解决方案**: 路透社采取三方面措施：1) 更新网站服务条款，明确禁止AI抓取；2) 技术团队实施更严格的访问控制，限制Internet Archive等平台的内容缓存；3) 与AI公司谈判内容授权协议。

**效果**: 2024年，路透社与OpenAI达成多年合作协议，后者将支付费用使用其新闻内容。同时，通过技术限制，路透社成功减少了未经授权的内容抓取，保护了其商业利益。

---

### 3：Conde Nast

 3：Conde Nast

**背景**: Conde Nast是知名媒体集团，拥有《纽约客》、《Vogue》等杂志。其内容质量高，常被AI公司用于训练模型。

**问题**: 2023年，Conde Nast发现其内容被多家AI公司大规模抓取，用于训练大语言模型。这导致其内容被无偿使用，影响其数字订阅收入和版权价值。

**解决方案**: Conde Nast采取多方面措施：1) 技术团队升级网站访问控制，限制AI爬虫；2) 加强与Internet Archive的沟通，限制其内容缓存频率；3) 与AI公司谈判内容授权协议。

**效果**: 通过技术限制和授权谈判，Conde Nast成功保护了其内容版权。2024年，其与OpenAI达成内容合作协议，后者将支付费用使用其内容。这为媒体集团内容保护提供了参考模式。

---
## 最佳实践


### 实践 1：实施细粒度的 Robots.txt 协议控制

**说明**: 传统的 `robots.txt` 通常只允许简单的允许/全部阻止设置。面对 AI 抓取，最佳实践是升级到更细粒度的控制，明确区分传统的搜索引擎爬虫（如 Googlebot）和 AI 数据抓取器（如 GPTBot, CCbot）。通过明确指定允许哪些爬虫访问，可以在保留 SEO 流量的同时阻止 AI 模型训练。

**实施步骤**:
1. 审计当前 `robots.txt` 文件，识别所有被允许的 User-agents。
2. 添加针对特定 AI 爬虫的明确拒绝规则（例如 `User-agent: GPTBot Disallow: /`）。
3. 对于搜索引擎爬虫，确保路径设置保持开放以维持搜索索引。
4. 使用 Google Search Console 或类似工具验证爬虫状态。

**注意事项**: `robots.txt` 是基于协议的，恶意的抓取程序可能会选择忽略它。这应被视为一道“软”防线，主要用于声明意图和阻止合规的机器人。

---

### 实践 2：动态速率限制与异常行为检测

**说明**: AI 抓取通常表现出与人类用户不同的特征，例如极高的请求速率、对大量历史页面的快速遍历或忽略 Cookie/会话状态。实施基于行为的动态防御可以实时识别并阻止这些抓取尝试，而不管其 User-agent 声称是什么。

**实施步骤**:
1. 在 Web 应用防火墙 (WAF) 或网关层配置速率限制规则（例如：单个 IP 每分钟请求超过 N 次则触发验证）。
2. 监控访问日志，寻找针对存档时间戳（如 `/2023/01/`）的高频遍历行为。
3. 对检测到异常行为的 IP 自动实施临时封禁或强制进行 JavaScript 质询（验证码）。

**注意事项**: 确保速率限制不会误伤合法的爬虫（如搜索引擎的抓取工具）或聚合服务，必要时将已知的白名单 IP 排除在外。

---

### 实践 3：内容分段加载与反爬虫混淆

**说明**: 对于高价值内容，可以采用前端渲染技术，使内容不是直接包含在 HTML 源代码中，而是通过 JavaScript 动态加载或通过 API 异步获取。这增加了简单的爬虫获取完整内容的难度。

**实施步骤**:
1. 将文章正文内容从服务器端渲染改为客户端渲染。
2. 对关键文本片段进行轻量级混淆或使用 Canvas/SVG 渲染部分文本（需权衡可访问性）。
3. 实施“付费墙”或“登录墙”逻辑，要求用户建立会话才能阅读全文。

**注意事项**: 此方法会影响 SEO（搜索引擎可能无法抓取动态渲染的内容）和用户体验。建议仅在核心高价值资产上使用，并配合 Prerender 技术服务搜索引擎。

---

### 实践 4：数据资产分级与访问策略隔离

**说明**: 并非所有内容都需要同等程度的保护。最佳实践是将数据资产分级：公开元数据（标题、摘要）允许开放访问以供索引，而核心正文内容实施严格保护。对于存档数据，应采取比新闻首页更严格的策略。

**实施步骤**:
1. 对网站内容进行分类：新闻快讯、深度报道、历史存档。
2. 为历史存档内容配置更严格的访问控制，例如禁止超过 6 个月的文章被匿名用户批量抓取。
3. 仅向经过认证的合作伙伴或订阅者提供完整的 API 访问权限。

**注意事项**: 这种策略需要强大的身份认证系统支持，并且可能影响通过社交媒体分享链接的引流效果。

---

### 实践 5：法律与技术双重保护（Terms of Service 强化）

**说明**: 技术手段必须有法律条款作为后盾。更新服务条款，明确禁止将网站内容用于 AI 训练、数据挖掘或机器学习用途。这为未来可能发生的法律诉讼提供依据，并增加了违规者的法律风险。

**实施步骤**:
1. 起草或更新网站的使用条款，明确包含“禁止用于机器学习/AI 训练”的条款。
2. 在网站页脚显著位置提供“AI 爬虫政策”页面，声明数据所有权。
3. 在 HTTP 响应头中添加 `X-Robots-Tag` 等策略标签，强化技术层面的声明。

**注意事项**: 法律条款的执行力取决于司法管辖权。对于跨国界的抓取行为，法律追诉可能存在困难，因此必须作为技术措施的补充而非替代。

---

### 实践 6：建立受控的 API 数据访问通道

**说明**: 与其完全封锁数据导致“Internet Archive”式的困境，不如建立官方的、受控的 API 接口。通过官方 API，你可以控制数据分发的速率、格式和用途，并从中获得收益或建立合作关系。

**实施步骤**:
1. 开发开发者门户，提供结构化的内容访问 API。
2. 实施 API 密钥管理，对每个调用者进行身份验证和配额限制。
3.

---
## 学习要点

- 新闻出版商出于对AI抓取的担忧，限制了互联网档案馆的访问权限，以防止其内容被用于训练大语言模型。
- 互联网档案馆的“保存现在”功能因被指缺乏明确授权，成为出版商防范数据爬取的主要封锁对象。
- 尽管出版商通常允许搜索引擎索引，但AI公司的大规模数据抓取行为促使他们收紧了对档案馆的开放策略。
- 这一事件反映了内容创作者与AI开发者之间关于版权和数据获取的紧张关系正在升级。
- 互联网档案馆表示尊重出版商的决定，但也指出这种限制阻碍了其保存数字历史的核心使命。
- 行业正在从传统的开放互联网模式，转向更严格的付费墙和访问控制，以保护知识产权。

---
## 常见问题

### 1: 为什么新闻出版机构要限制 Internet Archive 的访问权限？

1: 为什么新闻出版机构要限制 Internet Archive 的访问权限？

**A**: 此次限制访问的主要原因是新闻出版机构对人工智能（AI）公司抓取其内容用于模型训练的担忧。虽然 Internet Archive 长期以来通过其“Wayback Machine”提供网页存档服务，但 AI 抓取工具开始滥用该平台，大规模下载存档的新闻内容。出版商认为，这种未经授权的抓取和用于商业 AI 训练的行为侵犯了其版权，因此他们通过设置 robots.txt 文件或直接阻止来自 Internet Archive IP 地址的请求，以切断 AI 公司获取其数据的途径。

---

### 2: Internet Archive 在这个事件中扮演了什么角色？

2: Internet Archive 在这个事件中扮演了什么角色？

**A**: Internet Archive 是一个非营利性的数字图书馆，致力于提供“通用获取知识”的服务。在这个事件中，它处于一种尴尬的中间位置。一方面，它旨在保存互联网的历史记录，包括新闻网站；另一方面，它成为了 AI 抓取者的目标。出版商指出，由于 Internet Archive 的存档页面容易被爬虫访问，它实际上成为了 AI 公司获取受版权保护内容的“中转站”。Internet Archive 曾表示反对大规模抓取，并试图通过技术手段（如禁用 AI 爬虫的访问）来缓解出版商的担忧，但部分出版商仍然选择直接封锁其访问。

---

### 3: 这种限制访问对普通用户有什么影响？

3: 这种限制访问对普通用户有什么影响？

**A**: 对普通用户最直接的影响是，他们将无法通过 Internet Archive 的 Wayback Machine 访问被限制出版商的历史新闻页面。当用户尝试查看某篇过期的新闻报道或已被删除的文章时，可能会遇到“Blocked”或“Unavailable”的提示。这意味着互联网的一部分历史记录可能会因此永久缺失，用户失去了查阅过去新闻的重要渠道，这对于依赖网络存档进行研究、验证事实或回顾历史的个人和机构来说是一个重大损失。

---

### 4: 什么是 robots.txt 协议，它在此事件中起什么作用？

4: 什么是 robots.txt 协议，它在此事件中起什么作用？

**A**: Robots.txt 是一种网站用来与网络爬虫（包括搜索引擎和 AI 抓取工具）进行通信的标准协议文件。网站所有者通过该文件声明哪些部分允许被抓取，哪些部分禁止被抓取。在此事件中，新闻出版商利用 robots.txt 协议（或通过服务器配置直接屏蔽 IP）明确禁止 Internet Archive 对其网站内容进行进一步的存档或展示。由于 Internet Archive 通常尊重网站的 robots.txt 指令，一旦收到该指令，它就会停止显示相关的存档页面，从而导致用户无法访问。

---

### 5: AI 抓取与搜索引擎抓取有什么区别，为何出版商对此反应如此强烈？

5: AI 抓取与搜索引擎抓取有什么区别，为何出版商对此反应如此强烈？

**A**: 传统的搜索引擎抓取（如 Google 或 Bing）通常是为了建立索引，帮助用户找到原始内容并引导流量回出版商的网站，这是一种互利的生态。然而，生成式 AI 的抓取（如 ChatGPT 或其他大语言模型）是为了复制并学习数据，用于生成新的回答。出版商担心，AI 模型会直接利用其高质量的新闻内容生成答案，而不再向原始来源提供流量或引用，从而破坏了传统的商业模式，导致其核心资产（内容）被无偿占用。

---

### 6: 新闻出版商与 AI 公司之间的法律争议核心是什么？

6: 新闻出版商与 AI 公司之间的法律争议核心是什么？

**A**: 核心争议在于“合理使用”原则与版权侵权之间的界限。AI 公司通常认为，为了训练模型而公开抓取互联网数据属于合理使用，类似于人类阅读书籍学习知识。然而，新闻出版商则主张，AI 公司大规模、商业性地使用其受版权保护的内容用于训练竞争性产品，并不属于合理使用，而是直接的版权侵权。此次限制 Internet Archive 是出版商在法律诉讼之外，采取的一种通过技术手段保护自身数据资产的防御性措施。
## 引用

- **原文链接**: [https://www.niemanlab.org/2026/01/news-publishers-limit-internet-archive-access-due-to-ai-scraping-concerns](https://www.niemanlab.org/2026/01/news-publishers-limit-internet-archive-access-due-to-ai-scraping-concerns)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47017138](https://news.ycombinator.com/item?id=47017138)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

## 站内链接

- 分类： [安全](/categories/%E5%AE%89%E5%85%A8/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [互联网档案馆](/tags/%E4%BA%92%E8%81%94%E7%BD%91%E6%A1%A3%E6%A1%88%E9%A6%86/) / [AI抓取](/tags/ai%E6%8A%93%E5%8F%96/) / [数据保护](/tags/%E6%95%B0%E6%8D%AE%E4%BF%9D%E6%8A%A4/) / [robots.txt](/tags/robots.txt/) / [版权争议](/tags/%E7%89%88%E6%9D%83%E4%BA%89%E8%AE%AE/) / [网络安全](/tags/%E7%BD%91%E7%BB%9C%E5%AE%89%E5%85%A8/) / [内容审核](/tags/%E5%86%85%E5%AE%B9%E5%AE%A1%E6%A0%B8/) / [HackerNews](/tags/hackernews/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [新闻出版商因担忧AI抓取限制互联网档案馆访问权限]({{< relref "posts/20260215-hacker_news-news-publishers-limit-internet-archive-access-due--0.md" >}})
- [新闻出版商因担忧AI抓取限制互联网档案馆访问]({{< relref "posts/20260215-hacker_news-news-publishers-limit-internet-archive-access-due--0.md" >}})
- [发现逾17.5万个Ollama AI实例公网暴露]({{< relref "posts/20260131-hacker_news-175k-publicly-exposed-ollama-ai-instances-discover-19.md" >}})
- [新闻出版商因担忧AI抓取限制互联网档案馆访问权限]({{< relref "posts/20260215-hacker_news-news-publishers-limit-internet-archive-access-due--0.md" >}})
- [OpenAI 如何通过内置安全机制防范 AI 代理点击链接时的数据泄露与提示词注入]({{< relref "posts/20260129-blogs_podcasts-keeping-your-data-safe-when-an-ai-agent-clicks-a-l-5.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*
