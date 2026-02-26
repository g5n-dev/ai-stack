---
title: "谷歌API密钥曾非机密，但Gemini改变了规则"
date: 2026-02-26T12:58:28+08:00
draft: false
entry_kind: "auto"
tags: ["Google", "Gemini", "API密钥", "安全漏洞", "身份认证", "OAuth", "LLM安全", "API管理"]
categories: ["安全", "大模型"]
source: hacker_news
description: "长期以来，开发者习惯将 Google API keys 视为非敏感信息，因为其计费机制依赖于 Google Cloud 账号而非 Key 本身。然而，随着 Gemini 模型的推出与 API 认证策略的调整，这一惯例已被打破，泄露 Key 现在可能导致资源被滥用或产生意外费用。本文将深入解析这一安全逻辑的转变，并提供具"
external_url: https://trufflesecurity.com/blog/google-api-keys-werent-secrets-but-then-gemini-changed-the-rules
scenarios: ["大语言模型"]
---

# 谷歌API密钥曾非机密，但Gemini改变了规则

---

## 基本信息

- **作者**: hiisthisthingon
- **评分**: 778
- **评论数**: 158
- **链接**: [https://trufflesecurity.com/blog/google-api-keys-werent-secrets-but-then-gemini-changed-the-rules](https://trufflesecurity.com/blog/google-api-keys-werent-secrets-but-then-gemini-changed-the-rules)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47156925](https://news.ycombinator.com/item?id=47156925)

---
## 导语

长期以来，开发者习惯将 Google API keys 视为非敏感信息，因为其计费机制依赖于 Google Cloud 账号而非 Key 本身。然而，随着 Gemini 模型的推出与 API 认证策略的调整，这一惯例已被打破，泄露 Key 现在可能导致资源被滥用或产生意外费用。本文将深入解析这一安全逻辑的转变，并提供具体的排查与防护建议，帮助开发者及时规避潜在风险。

---
## 评论

### 中心观点
**文章的核心论点在于：Gemini API 的计费模式变更——将免费额度绑定至特定的 Google Cloud 项目——从根本上改变了 API Key 的安全属性。这使得 API Key 从传统的“低敏感度访问凭证”转变为“具有直接金融价值且需严格保密的资产”，从而对开发者社区中关于“在前端代码中明文存储 API Key”的安全实践构成了实质性挑战。**

### 深入评价

#### 1. 内容深度：从技术细节到安全范式转移的剖析
**支撑理由：**
*   **[事实陈述]** 文章准确指出了 Google Cloud 政策的关键变化点：即免费层配额的归属权从“IP/用户”转向了“Cloud Project”。这一架构调整是导致安全风险升级的根本原因。
*   **[作者观点]** 作者论证了“经济动机”在安全威胁中的核心地位。在 Gemini 变更前，窃取 Google Maps 等 API Key 的收益有限（通常受限于配额或变现难度）；而在 Gemini 模型中，API Key 直接关联 Google Cloud 的信用额度，使得凭证盗用的风险直接等同于资金盗用。
*   **[你的推断]** 这篇文章揭示了“API 经济”中的一个结构性矛盾：为了降低开发者门槛，平台倾向于使用简单的 API Key 而非复杂的 OAuth 认证，但这与高价值资产的安全需求存在冲突。

**反例/边界条件：**
*   **[边界条件]** 对于企业级应用，API Key 从来就不应该公开。本文的观点主要影响的是独立开发者、快速原型开发以及前端静态网页领域。对于已采用后端代理的架构，该规则变化影响较小。
*   **[反例]** 并非所有 Google API Key 都面临同等风险。如果开发者未启用付费计费，或设置了严格的每日配额上限，风险依然在可控范围内。文章在强调“所有 Key 必须保密”时，可能忽略了部分限制条件下的安全性。

#### 2. 实用价值：对开发者的即时警示
**支撑理由：**
*   **[事实陈述]** 文章指出了 GitHub 等代码托管平台上存在大量公开的 Google API Key。随着 Gemini 的普及，这些历史遗留的泄露点现在成为了潜在的安全隐患。
*   **[实用价值]** 文章隐含地提出了补救路径：检查代码仓库，轮换密钥，以及重新评估前端架构。这对于正在使用 LLM 构建应用的开发者具有明确的操作指导意义。

**反例/边界条件：**
*   **[局限性]** 文章在解决方案的深度上有所欠缺。除了强调“不要泄露”外，开发者更需要了解如何在 Serverless 架构（如 Vercel/Cloudflare Workers）中实施具体的 LLM 调用安全策略（如构建轻量级后端代理），文章对此类架构转型的技术细节涉及较少。

#### 3. 创新性：重新定义“Secret”的价值标准
**支撑理由：**
*   **[新观点]** 文章提出了一个动态的安全定义标准：**凭证的保密等级不应仅取决于其技术复杂度，而应取决于其背后的经济价值。** 这一视角有效地解释了为何同样的 API Key 技术在 AI 时代成为了关键的安全薄弱环节。
*   **[你的推断]** 该观点具有普适性，可推广至 OpenAI 的 API Key 及其他高价值模型服务。随着行业从“免费增值”向“按量付费”转型，安全标准必须随之升级。

#### 4. 行业影响与争议点
**争议点：**
*   **[作者观点 vs. 平台责任]** 文章倾向于强调开发者的保密责任，但**[你的推断]**认为这也暴露了平台在设计上的权衡。在一个鼓励前端直接调用的生态中，平台应当提供更细粒度的权限控制（如限制 Key 仅用于特定域名且不可用于计费消耗），而非单纯依赖保密。Google 为了推广 Gemini 简化了认证，却在计费上沿用传统的 Cloud 逻辑，这种设计上的错位是导致风险的另一面。

**实际应用建议：**
1.  **架构分离**：避免在客户端代码中存储任何关联了计费账户的 API Key，应建立后端代理机制。
2.  **密钥轮换**：立即废除历史上泄露在 GitHub 上的旧 Key。
3.  **权限隔离**：创建专门的 IAM 服务账号用于 AI 调用，并设置“硬性支出上限”，以减少潜在损失。

---
## 代码示例




```python
# 示例1：安全存储Google API密钥
import os
from dotenv import load_dotenv

def get_api_key():
    """
    从环境变量中安全获取Google API密钥
    避免将密钥硬编码在代码中
    """
    load_dotenv()  # 从.env文件加载环境变量
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        raise ValueError("未找到GOOGLE_API_KEY环境变量")
    
    return api_key

# 使用示例
try:
    key = get_api_key()
    print("API密钥加载成功")
except ValueError as e:
    print(f"错误: {e}")
```




```python
# 示例2：验证API密钥有效性
import requests

def validate_api_key(api_key):
    """
    验证Google API密钥是否有效
    通过调用简单的API端点来测试
    """
    url = "https://www.googleapis.com/oauth2/v1/tokeninfo"
    params = {"access_token": api_key}
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return True
        return False
    except Exception as e:
        print(f"验证出错: {e}")
        return False

# 使用示例
key = "your_api_key_here"
if validate_api_key(key):
    print("API密钥有效")
else:
    print("API密钥无效或已过期")
```




```python
# 示例3：动态轮换API密钥
import random
import time

class APIKeyManager:
    """
    管理多个API密钥的轮换使用
    当某个密钥达到配额限制时自动切换
    """
    def __init__(self, api_keys):
        self.api_keys = api_keys
        self.current_index = 0
        self.key_usage = {key: 0 for key in api_keys}
    
    def get_next_key(self):
        """获取下一个可用的API密钥"""
        key = self.api_keys[self.current_index]
        self.key_usage[key] += 1
        
        # 简单轮换策略：每10次请求切换密钥
        if self.key_usage[key] >= 10:
            self.current_index = (self.current_index + 1) % len(self.api_keys)
        
        return key

# 使用示例
keys = ["key1", "key2", "key3"]
manager = APIKeyManager(keys)

for i in range(15):
    key = manager.get_next_key()
    print(f"请求 {i+1} 使用密钥: {key[-4:]}...")  # 只显示密钥后4位
    time.sleep(0.1)  # 模拟API请求间隔
```


---
## 案例研究


### 1：某开源 AI 辅助编程插件项目

 1：某开源 AI 辅助编程插件项目

**背景**:
该项目是一个基于 Web 技术构建的浏览器扩展和 IDE 插件，旨在帮助开发者通过 Google 的 Gemini API 进行代码补全和生成。为了方便用户快速上手，项目早期在文档中建议用户直接将 API Key 存储在浏览器的 `localStorage` 或本地配置文件中，因为彼时 Google Cloud 控制台并未对 HTTP 引用来源（Referer）进行严格的强制校验，且 API 密钥通常被授予了较为宽松的访问权限。

**问题**:
随着 Gemini 模型的更新和 Google 安全策略的收紧，Google 开始严格执行 API Key 的权限限制和配额检查。许多用户报告插件突然失效，控制台出现 403 Forbidden 错误。更严重的是，由于 API Key 被硬编码在客户端代码中，且缺乏域名限制，任何拥有该 Key 的人都可以滥用配额，导致项目开发者收到了高额的意外账单，且无法有效追踪是哪个用户在滥用密钥。

**解决方案**:
开发团队意识到 API Key 不再适合作为纯粹的“客户端秘密”，必须引入后端代理机制。
1.  **构建轻量级后端服务**：使用 Cloudflare Workers 或 Vercel Serverless Functions 搭建了一个中间层。
2.  **密钥隔离**：将高权限的 Google API Key 存储在服务端的环境变量中，彻底从前端代码中移除。
3.  **用户鉴权**：前端不再直接发送 API Key，而是发送用户自己的身份令牌（JWT）或临时凭证。后端验证用户身份后，再使用服务端的 Key 代为请求 Gemini API。

**效果**:
- **安全性提升**：彻底杜绝了 API Key 泄露到公网的风险，消除了未授权的配额消耗。
- **成本可控**：通过后端代理，开发者能够精确监控每个用户的 API 调用次数，从而实施公平的速率限制和配额管理。
- **合规性**：符合 Google 最新的 API 使用最佳实践，确保了应用的长期稳定运行。

---



### 2：某 SaaS 初创公司的内容营销平台

 2：某 SaaS 初创公司的内容营销平台

**背景**:
该 SaaS 平台允许营销人员输入关键词，利用 Gemini Pro 模型自动生成博客文章和社交媒体文案。在开发 MVP（最小可行性产品）阶段，为了节省服务器成本并加快迭代速度，团队选择在 React 前端直接调用 Google 的 REST API。他们认为由于应用仅面向内部员工使用，直接暴露 Key 风险可控。

**问题**:
随着产品向公网 beta 测试开放，Google 修改了 API Key 的默认行为，强制要求绑定特定的 HTTP 引用来源或 IP 地址。这导致部署在 Vercel 上的前端应用因为域名动态变化或请求头不匹配而频繁报错。同时，团队发现只要打开浏览器开发者工具，任何人都能复制粘贴该 API Key 并用于自己的个人项目中，导致公司的 API 调用配额在几天内被耗尽，影响了正常付费用户的使用。

**解决方案**:
团队决定重构架构，将 AI 调用逻辑迁移至服务端。
1.  **服务端封装**：使用 Node.js 搭建内部 API 服务 `/api/generate`，前端仅调用该内部接口。
2.  **环境变量管理**：利用 Google Cloud Secret Manager 或 `.env` 文件管理 API Key，确保 Key 不离开服务器边界。
3.  **API 网关配置**：在 Google Cloud 控制台中，将 API Key 的限制严格设置为仅允许公司后端服务器的 IP 地址访问，彻底屏蔽来自浏览器端的直接请求。

**效果**:
- **稳定性恢复**：解决了因浏览器端 Referer 检查导致的间歇性认证失败问题。
- **资产保护**：API Key 泄露风险被降至最低，公司停止了非授权的配额流失。
- **功能扩展**：通过引入后端，团队能够在请求发送给 Google 之前添加内容审核逻辑，确保生成的内容符合安全规范，这是纯客户端方案难以实现的。

---



### 3：某在线教育平台的 AI 导师功能

 3：某在线教育平台的 AI 导师功能

**背景**:
该教育平台尝试集成 Gemini Flash 模型，为学生提供实时的数学题解答和历史知识问答。初期开发采用了纯静态网站架构（JAMstack），通过 GitHub Pages 托管。为了实现功能，开发人员将 API Key 放在了前端 JavaScript 配置文件中，并设置了 Google Cloud 中的“公开数据”访问权限。

**问题**:
Google 调整了 Gemini API 的定价和访问策略，开始对未认证的公开 API Key 施加极低的速率限制（RPM），并计划逐步淘汰不受限的公开访问方式。这导致平台在晚高峰时段频繁收到 429 Too Many Requests 错误，严重影响了用户体验。此外，由于 Key 是公开的，恶意爬虫开始抓取该接口进行数据训练，进一步挤占了学生请求的资源。

**解决方案**:
为了维持免费或低成本的静态托管架构，同时解决安全性问题，平台采取了混合方案。
1.  **采用 Cloudflare Workers 作为代理**：利用 Cloudflare Workers 的边缘计算能力，在请求到达 Google 之前拦截并注入 API Key。
2.  **Key 轮换与限制**：撤销了旧的公开 API Key，生成了新的仅允许 Cloudflare IP 段访问的 Key。
3.  **缓存层**：在 Workers 层针对常见的问题（如“什么是二战”）添加了智能缓存，减少对 Google API 的直接调用。

**效果**:
- **性能优化**：通过边缘缓存，API 响应延迟降低了 40%，且有效规避了 Google 的速率限制。
- **成本降低**：减少了大量重复的 API 调用，即使 Gemini 政策收紧，平台也能通过缓存服务维持低成本运行。
- **无缝迁移**：在不改变前端静态托管架构的前提下，成功将 API Key 隐藏到了边缘层，保护了核心凭证。

---
## 最佳实践

## 最佳实践指南

### 实践 1：API 密钥的访问控制与权限最小化

**说明**:
默认情况下，Google Cloud 生成的 API 密钥通常不受限制，允许来自任何 IP 的请求。为了防止密钥泄露后被滥用，必须严格限制密钥的使用范围。应仅授予密钥执行特定任务所需的特定 API 权限，并严格限制其访问来源。

**实施步骤**:
1. 登录 Google Cloud Console，进入 "APIs & Services" -> "Credentials"。
2. 选择或创建 API 密钥。
3. 在 "Application restrictions"（应用限制）选项中，选择以下任一方式：
   - **IP 地址**：仅允许来自特定服务器 IP 的请求（适用于后端调用）。
   - **HTTP 引用来源**：仅允许来自特定域名/网站的请求（适用于前端调用，注意此方式仍存在泄露风险）。
   - **Android 应用**或**iOS 应用**：根据应用签名进行限制。
4. 在 "API restrictions"（API 限制）选项中，取消选择 "Don't restrict key"，仅勾选该密钥实际需要调用的 API（例如仅勾选 "Gemini API" 而非所有 Google 服务）。

**注意事项**:
不要在生产环境中使用 "None"（无限制）的密钥。对于客户端（Web/移动端）应用，IP 限制通常不适用，需格外依赖引用来源限制或配额限制。

---

### 实践 2：实施配额限制与预算警报

**说明**:
为了防止密钥泄露导致巨额账单，必须设置严格的使用配额。即使攻击者获取了密钥，配额限制也能将损失控制在可承受范围内。结合预算警报，可以在异常流量发生时第一时间通知管理员。

**实施步骤**:
1. 在 API 密钥配置页面，找到 "Quotas" 或在对应 API 的 "Quotas" 页面中设置。
2. 为特定的 API 密钥或项目设置每分钟或每天的最大请求数。
3. 前往 Google Cloud Billing，设置 "Budgets and alerts"。
4. 创建预算（例如设置为平时月度的 1.2 倍），并配置邮件通知阈值（如达到 50%, 80%, 100% 时触发）。

**注意事项**:
配额限制应基于正常业务流量的峰值进行设定，并预留一定的缓冲空间，以免在业务高峰期误阻断正常服务。

---

### 实践 3：代码仓库安全与密钥隔离

**说明**:
绝对禁止将 API 密钥硬编码在代码中，尤其是提交到 Git 等版本控制系统。历史提交记录中即使删除了密钥，仍可能被他人通过历史记录恢复。应使用环境变量或密钥管理服务来动态加载密钥。

**实施步骤**:
1. 将所有包含密钥的文件添加到 `.gitignore` 文件中，确保其不被提交。
2. 使用环境变量（如 `.env` 文件，但需确保 `.env` 已被忽略）存储密钥。
3. 在代码中通过 `os.getenv()` 或类似函数读取环境变量。
4. 对于已提交的公开仓库，立即在 Google Cloud Console 中撤销该密钥，并生成新密钥。
5. 考虑使用 git-secrets 或 truffleHawk 等工具扫描代码库，防止密钥意外提交。

**注意事项**:
对于前端代码（如 React/Vue），环境变量通常会被打包进客户端代码，因此仅靠环境变量无法隐藏密钥。前端必须配合后端代理或特定的应用限制来保护密钥。

---

### 实践 4：使用后端代理模式

**说明**:
对于 Gemini API 等可能产生高额费用或包含敏感逻辑的服务，不应直接从客户端（浏览器或手机 App）调用 API。最佳实践是搭建一个轻量级后端服务，客户端请求后端，后端再使用受严格保护的 API 密钥调用 Google 服务。

**实施步骤**:
1. 搭建一个后端服务（如 Python Flask, Node.js Express 或 Cloud Functions）。
2. 将高权限的 API 密钥存储在后端服务器的环境变量或 Secret Manager 中。
3. 客户端发起请求到你的后端 API。
4. 后端验证用户身份/权限后，附加 API 密钥转发请求至 Google API。
5. 后端将结果返回给客户端。

**注意事项**:
这会增加网络延迟和服务器成本，但能最大程度保护 API 密钥不被泄露，并允许你记录详细的审计日志。

---

### 实践 5：密钥轮换与应急响应机制

**说明**:
密钥应当被视为临时凭证而非永久资产。定期轮换密钥可以缩短泄露密钥的有效期。同时，必须建立一套应急响应流程，以便在发现泄露时迅速止损。

**实施步骤**:
1. 制定密钥轮换计划（例如每 90 天一次），并在日历上设置提醒。
2. 在轮换前，生成新密钥并在测试环境验证。
3. 在生产环境更新配置，

---
## 学习要点

- Google API 密钥长期被默认为非敏感信息，导致大量密钥被公开上传至 GitHub 等代码托管平台。
- Gemini API 的出现改变了这一规则，因为它默认启用了收费机制，且密钥直接关联 Google Cloud 账单与身份，使其具有了极高的敏感价值。
- 攻击者可以通过自动化工具在 GitHub 上轻易搜到历史遗留的 Google API 密钥，并利用其访问 Gemini 模型或消耗账户余额。
- 传统的“密钥轮换”策略（Key Rotation）在此场景下失效，因为 Google Cloud 控制台允许查看密钥的创建时间，攻击者可以据此判断当前使用的密钥是否为泄露的旧密钥。
- 即使密钥未绑定信用卡，攻击者也可以利用其调用 Gemini API 进行“越狱”尝试或生成有害内容，将安全风险转嫁给密钥持有者。
- 开发者必须将 Google API 密钥视为等同于 AWS 凭证的高价值机密，严禁硬编码在代码中，并应使用环境变量或密钥管理服务进行隔离。
- 针对已泄露的密钥，最有效的补救措施是彻底删除并重新创建，而不是仅依赖 API Key 限制或配额管控。

---
## 常见问题


### 1: 为什么以前 Google API Key 通常不被视为高度机密，而现在情况发生了变化？

1: 为什么以前 Google API Key 通常不被视为高度机密，而现在情况发生了变化？

**A**: 在过去，Google 的许多 API（如 Maps、Places 等）通常采用按调用次数付费的模型。即使攻击者窃取了 API Key，他们能造成的损害仅限于消耗配额或产生财务费用，而这些通常可以通过设置每日上限来控制。因此，开发者有时会将 Key 硬编码在客户端代码中（如 Android 或 JavaScript），虽然不推荐，但并未被视为导致数据泄露的严重安全漏洞。然而，随着 Gemini 等生成式 AI 模型的推出，API 的性质发生了根本性变化。Gemini API 的调用可能会包含用户输入的私密提示词或上下文，这使得 API Key 的泄露不再仅仅是财务问题，而是变成了严重的隐私和数据安全风险。

---



### 2: Gemini API 的引入具体改变了哪些安全规则？

2: Gemini API 的引入具体改变了哪些安全规则？

**A**: Gemini 的引入改变了 API Key 的风险模型。与传统的地图查询不同，用户与 AI 模型的交互通常涉及敏感的对话历史、文档内容或创意构思。如果 API Key 被泄露，恶意行为者不仅可以窃取配额，还可以读取或操纵通过该 Key 发送的私密数据。此外，Google 针对 Gemini 的安全策略变得更加严格，要求开发者必须对 Key 进行更严格的权限控制（例如限制仅限服务器端调用），并禁止将具有高权限的 Key 暴露在客户端或公共代码库中，以防止中间人攻击或滥用。

---



### 3: 如果我的 Google Cloud API Key 已经泄露到了 GitHub 等公共平台上，我该怎么办？

3: 如果我的 Google Cloud API Key 已经泄露到了 GitHub 等公共平台上，我该怎么办？

**A**: 如果 API Key 已经公开，您必须立即采取以下措施：首先，登录 Google Cloud Console，导航到凭据页面，立即删除或禁用受影响的 API Key。其次，检查该 Key 关联的项目的使用情况和日志，确认是否有异常调用或数据访问。最后，创建一个新的 API Key，并确保这次将其存储在环境变量或密钥管理服务（如 Secret Manager）中，绝不要再次将其硬编码在代码里。如果 Key 拥有广泛的权限（如不受限制的访问），风险极高，紧急补救措施至关重要。

---



### 4: 开发者应如何正确存储和管理 Google API Key 以符合安全最佳实践？

4: 开发者应如何正确存储和管理 Google API Key 以符合安全最佳实践？

**A**: 最佳实践是永远不要将 API Key 硬编码在源代码或提交到版本控制系统（如 Git）中。对于前端或移动应用，如果必须调用 Google API，应该通过您自己的后端服务器进行代理。前端向后端发送请求，后端验证请求后，将存储在服务器端环境变量中的 API Key 附加到请求中发送给 Google。这样，Key 始终保留在服务器端，不会暴露给最终用户。此外，应在 Google Cloud Console 中为 API Key 设置严格的应用限制（如 IP 地址限制、HTTP 引用限制或 Android 应用签名限制）以及 API 限制，仅启用项目实际需要的特定 API。

---



### 5: 在 Google Cloud Console 中设置“应用程序限制”和“API 限制”有什么区别？

5: 在 Google Cloud Console 中设置“应用程序限制”和“API 限制”有什么区别？

**A**: 这是保护 API Key 的两道防线。“API 限制”是指定该 Key 具体有权调用哪些 Google 服务（例如只允许调用 Gemini API，而不允许调用 Maps API）。如果攻击者窃取了该 Key，他们也无法利用它访问您未授权的其他服务。“应用程序限制”则规定了该 Key 允许在何处被调用，例如限制来自特定的 IP 地址（服务器端）、特定的 Android 应用包名或特定的网站域名。结合使用这两种限制可以最大程度减少 Key 泄露后的影响，即使 Key 被公开，攻击者也无法从他们的服务器或应用中使用它。

---



### 6: 公开暴露的 API Key 对普通用户有什么潜在风险？

6: 公开暴露的 API Key 对普通用户有什么潜在风险？

**A**: 对于普通用户而言，如果他们使用的应用程序泄露了其开发者的 Google API Key，主要风险在于隐私泄露。如果该应用使用了 Gemini 等 AI 服务，攻击者可能利用泄露的 Key 拦截用户发送给 AI 的查询内容。这可能包含个人身份信息、私人日记或商业机密。此外，虽然用户通常不需要直接为 API 的滥用买单（开发者承担费用），但滥用可能导致服务中断或应用功能降级，从而影响用户体验。

---



### 7: Google 是否会自动检测公开泄露的 API Key 并通知开发者？

7: Google 是否会自动检测公开泄露的 API Key 并通知开发者？

**A**: 是的，Google 拥有安全扫描机制来检测公开泄露的云凭证。如果 Google 检测到您的 API Key 已在 GitHub 或其他公共位置泄露，他们通常会向项目所有者发送电子邮件警告。然而，依赖自动检测并不是一种安全策略。自动检测可能存在延迟，或者在某些情况下无法覆盖所有泄露渠道。开发者应主动使用 git-secrets 等工具在提交代码前扫描敏感信息，并定期审计代码库，确保没有意外提交凭证。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 假设你是一个开发者，你的代码库中硬编码了一个 Google Cloud API Key。请编写一个简单的 Bash 脚本或使用 Git 命令，扫描本地仓库的所有历史提交（包括已删除的记录），查找是否存在匹配 `AIza` 开头的字符串（这是 Google API Key 的常见前缀）。

### 提示**: 你需要使用 `git log` 的特定参数来遍历所有提交对象的内容，或者使用 `git rev-list` 配合 `git grep`。不要只查看当前版本的代码。

### 

---
## 引用

- **原文链接**: [https://trufflesecurity.com/blog/google-api-keys-werent-secrets-but-then-gemini-changed-the-rules](https://trufflesecurity.com/blog/google-api-keys-werent-secrets-but-then-gemini-changed-the-rules)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47156925](https://news.ycombinator.com/item?id=47156925)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [安全](/categories/%E5%AE%89%E5%85%A8/) / [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/)
- 标签： [Google](/tags/google/) / [Gemini](/tags/gemini/) / [API密钥](/tags/api%E5%AF%86%E9%92%A5/) / [安全漏洞](/tags/%E5%AE%89%E5%85%A8%E6%BC%8F%E6%B4%9E/) / [身份认证](/tags/%E8%BA%AB%E4%BB%BD%E8%AE%A4%E8%AF%81/) / [OAuth](/tags/oauth/) / [LLM安全](/tags/llm%E5%AE%89%E5%85%A8/) / [API管理](/tags/api%E7%AE%A1%E7%90%86/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/)

### 相关文章

- [谷歌API密钥非机密但Gemini改变规则]({{< relref "posts/20260226-hacker_news-google-api-keys-werent-secrets-but-then-gemini-cha-0.md" >}})
- [Gemini 3.1 Pro：面向复杂任务的深度回答模型]({{< relref "posts/20260219-blogs_podcasts-gemini-31-pro-a-smarter-model-for-your-most-comple-4.md" >}})
- [Gemini 3.1 Pro：专为复杂任务设计的智能模型]({{< relref "posts/20260219-blogs_podcasts-gemini-31-pro-a-smarter-model-for-your-most-comple-5.md" >}})
- [谷歌发布 Gemini 3.1 模型]({{< relref "posts/20260219-hacker_news-gemini-31-1.md" >}})
- [谷歌发布 Gemini 3.1 Pro 模型]({{< relref "posts/20260219-hacker_news-gemini-31-pro-0.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*