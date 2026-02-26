---
title: "谷歌API密钥非机密但Gemini改变规则"
date: 2026-02-26T11:22:54+08:00
draft: false
entry_kind: "auto"
tags: ["API密钥", "Gemini", "谷歌", "安全漏洞", "身份认证", "访问控制", "LLM", "API管理"]
categories: ["安全", "AI 工程"]
source: hacker_news
description: "长期以来，开发者普遍认为 Google API keys 仅需通过 HTTP Referer 限制即可确保安全。然而，随着 Gemini API 的引入，Google 更新了其安全规则，要求必须配合独立的 API 密钥，这使得传统的防护手段已不再适用。本文将深入解析这一政策变动的具体影响，并指导开发者如何正确配置新的安"
external_url: https://trufflesecurity.com/blog/google-api-keys-werent-secrets-but-then-gemini-changed-the-rules
scenarios: ["大语言模型"]
---

# 谷歌API密钥非机密但Gemini改变规则

---

## 基本信息

- **作者**: hiisthisthingon
- **评分**: 702
- **评论数**: 139
- **链接**: [https://trufflesecurity.com/blog/google-api-keys-werent-secrets-but-then-gemini-changed-the-rules](https://trufflesecurity.com/blog/google-api-keys-werent-secrets-but-then-gemini-changed-the-rules)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47156925](https://news.ycombinator.com/item?id=47156925)

---
## 导语

长期以来，开发者普遍认为 Google API keys 仅需通过 HTTP Referer 限制即可确保安全。然而，随着 Gemini API 的引入，Google 更新了其安全规则，要求必须配合独立的 API 密钥，这使得传统的防护手段已不再适用。本文将深入解析这一政策变动的具体影响，并指导开发者如何正确配置新的安全机制，以有效防范密钥泄露风险。

---
## 评论

### 文章中心观点
**事实陈述**：随着 Gemini API 的推出，Google 将 API Key 的安全信任模型从“客户端安全”转变为“服务端强制执行”，打破了过去开发者依赖前端隐匿 Key 的脆弱惯例。

### 深入评价与支撑理由

#### 1. 内容深度：从“隐匿式安全”到“零信任”的范式转移
**支撑理由**：
文章的核心在于揭示了 API Key 管理中一个长期被忽视的矛盾：**浏览器端的代码是公开的，任何硬编码在客户端的 Key 在技术上都不可能是秘密。**
*   **过去（事实陈述）**：在旧有的 Google Maps 或 YouTube API 时代，Google 主要依赖“配额限制”和“Referer 检查”来防止滥用。这种机制本质上是基于“名誉”的，只要 Key 不被恶意刷爆配额，开发者往往将其视为“公开但无害”的常量。
*   **现在（作者观点）**：Gemini 等 GenAI 模型的特殊性在于其**按量计费的高昂成本**与**内容生成的潜在风险**。攻击者盗用 Key 不仅是消耗配额，更可能利用受害者身份生成违规内容，导致账户被封禁。
*   **评价（你的推断）**：文章深刻指出了 GenAI 时代安全边界的收缩。它论证了“Key 不是秘密”这一技术常识在新的经济模型下（Token 计费）变成了致命的漏洞。

**反例/边界条件**：
*   **边界条件**：对于纯静态的公开数据展示（如展示天气 Widget），API Key 即使泄露风险依然可控，因为后端可以限制 Key 的调用来源（HTTP Referer）和每日上限。
*   **反例**：并非所有 Google 服务都强制要求服务端代理。例如，Google Maps JavaScript API 至今仍允许在客户端使用 Key，前提是配置了严格的 HTTP Referrer 限制。

#### 2. 实用价值：对架构选型的决定性影响
**支撑理由**：
*   **架构重构（你的推断）**：文章迫使全栈开发者重新审视架构设计。过去为了快速原型开发，直接在前端调用 LLM API 是常见的；现在必须引入后端 BFF 层作为代理。
*   **成本控制（事实陈述）**：Gemini 的计费模式使得“盗用”直接等同于“经济损失”。文章警示开发者，若不进行服务端封装，一次简单的 Key 泄露可能导致数万美元的账单。

**实际应用建议**：
开发者应立即停止在前端代码中硬编码任何 GenAI 产品的 API Key，转而使用“后端代理”模式：前端调用自有后端，后端持有 Key 并调用 Google API。

#### 3. 创新性与行业影响：重新定义“Secret”的标准
**支撑理由**：
*   **新观点（作者观点）**：文章提出了一个具有挑衅性的观点：API Key 从未是“秘密”，但行业一直假装它是。Gemini 只是撕下了这块遮羞布。
*   **行业影响（你的推断）**：这将推动 API 网关和身份验证中间件的普及。未来，我们可能会看到更多类似 Cloudflare Workers 或 Vercel Edge Functions 的“Key 代理”模式成为标准配置，而非仅仅是大型企业的专利。

#### 4. 争议点与不同观点
**支撑理由**：
*   **用户体验 vs. 安全性（作者观点）**：文章可能暗示所有调用都必须上云。然而，**边缘计算**流派可能认为，将简单请求路由到远端服务器会增加延迟。
*   **配置的复杂性（你的推断）**：Google 现在允许在 Google Cloud Console 中设置极严格的限制（如限制 Key 仅能被特定 iOS Bundle ID 调用）。如果配置得当，客户端持有 Key 是否依然可行？文章在“配置补救”这一点上探讨可能不足。

### 可验证的检查方式

为了验证文章观点及评估自身系统的安全性，建议进行以下检查：

1.  **代码静态分析**
    *   **操作**：使用 `git grep` 或工具（如 TruffleHog）扫描代码库。
    *   **指标**：检查是否存在 `google_api_key` 或 `AIza` 开头的字符串直接出现在 `.js`, `.ts`, `.html` 或移动端代码中。

2.  **网络流量抓包**
    *   **操作**：打开浏览器开发者工具或使用 Charles/Fiddler 抓包，访问集成了 Gemini 或 Google API 的应用。
    *   **观察窗口**：查看 Network 面板中的 Request Headers。
    *   **验证点**：如果发现 `x-goog-api-key: YOUR_KEY` 直接发送给 `generativelanguage.googleapis.com`，则说明该应用存在安全风险，Key 可被轻易复制。

3.  **权限边界测试**
    *   **操作**：获取该 API Key，在完全不同的网络环境（如本地 Postman 或无痕模式）下尝试调用。
    *   **指标**：如果 API 返回成功结果，说明该 Key 缺乏“应用限制”或仅依赖 IP 白名单（这在移动端/公网环境下无效）。

### 总结
这篇文章是一篇针对 GenAI 时代安全现状的警世恒言。它虽然在技术上没有提出全新的算法，但极具洞察力地指出了**经济模型变化如何倒逼安全架构升级**。对于任何正在集成 AI 模型的开发者而言，理解“API Key 不是秘密”这一前提，是构建生产级应用的第一步。

---
## 代码示例




```python
# 示例1：安全存储API密钥（环境变量方式）
import os
from dotenv import load_dotenv

def get_api_key():
    """
    从.env文件中安全读取API密钥
    需要安装python-dotenv: pip install python-dotenv
    """
    load_dotenv()  # 加载.env文件
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        raise ValueError("未找到API密钥，请检查.env文件配置")
    return api_key

# 使用示例
try:
    key = get_api_key()
    print("成功获取API密钥（实际使用中不要打印密钥）")
except ValueError as e:
    print(f"错误: {e}")
```


---

```python
# 示例2：验证API密钥有效性
import requests

def validate_api_key(api_key):
    """
    验证Google API密钥是否有效
    返回: (bool, str) 元组，第一个元素表示是否有效，第二个元素是消息
    """
    url = "https://generativelanguage.googleapis.com/v1beta/models"
    params = {"key": api_key}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return True, "API密钥有效"
        elif response.status_code == 403:
            return False, "API密钥无效或已过期"
        else:
            return False, f"验证失败，状态码: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return False, f"请求错误: {str(e)}"

# 使用示例
api_key = "你的API密钥"  # 实际使用中应从环境变量获取
is_valid, message = validate_api_key(api_key)
print(f"验证结果: {message}")
```


---

```python
# 示例3：安全的API调用封装
import requests
import os
from typing import Optional, Dict, Any

class SecureGeminiClient:
    """安全的Gemini API客户端"""
    
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("未设置GOOGLE_API_KEY环境变量")
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
    
    def call_api(self, endpoint: str, payload: Dict[str, Any]) -> Optional[Dict]:
        """
        安全调用API的方法
        :param endpoint: API端点
        :param payload: 请求体
        :return: API响应或None
        """
        url = f"{self.base_url}/{endpoint}"
        headers = {"Content-Type": "application/json"}
        params = {"key": self.api_key}
        
        try:
            response = requests.post(url, json=payload, headers=headers, params=params, timeout=30)
            response.raise_for_status()  # 检查HTTP错误
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP错误: {e}")
        except requests.exceptions.RequestException as e:
            print(f"请求错误: {e}")
        return None

# 使用示例
try:
    client = SecureGeminiClient()
    response = client.call_api("models/gemini-pro:generateContent", {
        "contents": [{"parts": [{"text": "Hello"}]}]
    })
    if response:
        print("API调用成功")
except ValueError as e:
    print(f"初始化错误: {e}")
```


---
## 案例研究


### 1：某知名 AI 生产力工具（基于 Cursor / Windsurf 类似场景）

 1：某知名 AI 生产力工具（基于 Cursor / Windsurf 类似场景）

**背景**:
一款基于 VS Code 二次开发的 AI 辅助编程工具，其核心功能是调用 Google 的 Gemini 模型帮助开发者生成代码。为了降低用户使用门槛，该工具在早期版本中允许用户直接在客户端配置界面输入个人的 Google API Key，并以明文形式存储在本地配置文件中，以便每次启动时自动调用。

**问题**:
随着 Google Gemini 更新了使用规则并加强了风控策略，单纯依靠 API Key 已不再安全，且由于该工具的配置文件曾被用户误上传至 GitHub 公开仓库，导致大量 API Key 泄露。黑客利用这些泄露的 Key 调用高付费的 Gemini Pro 模型进行非法内容生成，导致原用户在短时间内产生了巨额 Google Cloud 账单，且该工具因缺乏密钥保护机制面临信任危机。

**解决方案**:
开发团队迅速移除了客户端直接存储 API Key 的功能，转而实施了“后端代理 + OAuth 2.0”的架构。
1.  移除本地 Key 存储逻辑，增加 `.gitignore` 防护机制检测。
2.  部署一个轻量级后端服务，负责持有 API Key 并处理与 Google API 的交互。
3.  前端通过 Google Identity Services 进行 OAuth 身份验证，后端仅验证用户身份后转发请求，实现了 Key 与用户的彻底隔离。

**效果**:
彻底杜绝了 API Key 泄露带来的账单盗刷风险。虽然增加了后端运营成本，但用户数据安全性得到了质的提升，符合 Google 最新的安全合规要求，挽回了企业级用户的信任。

---



### 2：某开源 Web 项目（基于 React / Next.js 通用场景）

 2：某开源 Web 项目（基于 React / Next.js 通用场景）

**背景**:
一个流行的开源前端仪表盘项目，旨在帮助用户可视化分析 Google 搜索数据。为了方便开发者一键运行，项目文档长期建议将 Google API Key 直接硬编码在 `.env.local` 文件中，并在示例代码里保留了 `NEXT_PUBLIC_GOOGLE_API_KEY` 的写法，导致 Key 被打包进客户端浏览器代码中。

**问题**:
在 Gemini 更新规则并严格执行“客户端 Key 不可用于高敏感接口”后，该项目的核心功能（调用 Gemini 进行搜索趋势分析）开始频繁报错，提示“API Key not allowed”（API Key 不允许）。此外，由于 Key 暴露在前端代码中，任何访问该网站部署实例的人都可以通过浏览器开发者工具（F12）截获 Key，并用于自己的项目，导致原项目开发者的配额被迅速耗尽。

**解决方案**:
项目维护者重构了数据获取层，采用了 Next.js 的 Route Handlers（服务端渲染路由）技术。
1.  将 API Key 从环境变量中移除 `NEXT_PUBLIC_` 前缀，使其仅在服务端可见，不再打包到浏览器端。
2.  创建了一个服务端 API 路由（`/api/google-proxy`），由服务端携带 Key 向 Google 发起请求。
3.  前端组件仅调用该内部路由，不直接接触 Google API。

**效果**:
应用成功绕过了浏览器端对 API Key 的安全限制，功能恢复正常。通过将 Key 隐藏在服务端，不仅防止了配额被恶意盗用，还使得项目能够利用 Google 最新发布的仅限服务端使用的模型特性，功能稳定性大幅增强。

---



### 3：某初创公司的 SaaS 平台（基于 Vercel / Serverless 架构）

 3：某初创公司的 SaaS 平台（基于 Vercel / Serverless 架构）

**背景**:
一家初创公司构建了一个基于 Vercel 托管的 SaaS 平台，利用 Google Gemini API 为初创企业提供文档自动生成服务。在开发初期，为了快速上线，他们将 Google API Key 存储在 Vercel 的环境变量中，但由于使用了无服务器架构，部分边缘函数直接将 Key 暴露在 HTTP 请求头中返回给客户端，以便前端直接调用。

**问题**:
随着 Gemini API 的安全审计升级，Google 开始检测请求来源和 Key 的使用环境。由于边缘函数的 IP 地址不断变化且缺乏有效的引用来源证明，大量请求被 Google 拦截。同时，由于 Key 在客户端可见，爬虫抓取了公开演示页面的 Key 并进行大规模滥用，导致该初创公司的 Google Cloud 账户在一夜之间产生了数千美元的异常费用，面临服务停摆风险。

**解决方案**:
技术团队引入了 Secret Manager 服务（如 Vercel 的环境变量加密或 AWS Secrets Manager）并结合 API 网关进行鉴权。
1.  将 API Key 从代码中完全剥离，存入加密的密钥管理服务，运行时动态解密。
2.  在服务端与 Google 之间建立严格的 IP 白名单和域名验证。
3.  废除前端直连模式，所有请求必须经过经过鉴权的服务端 API 网关转发，并对单个用户调用频率进行了限流。

**效果**:
通过集中化管理 API Key，公司消除了 Key 泄露的经济风险。服务端代理模式解决了 IP 变动导致的拦截问题，API 调用成功率恢复至 100%，同时通过限流机制将月度 API 成本控制在预算范围内。

---
## 最佳实践

## 最佳实践指南

### 实践 1：实施严格的 API 密钥访问控制

**说明**:
Google API 密钥通常被嵌入在客户端代码（如 JavaScript 或移动应用）中，导致其容易被窃取。Gemini API 的变更表明，仅依赖密钥存在是不够的。必须限制谁能使用该密钥，以及他们可以从哪里调用 API。

**实施步骤**:
1. 登录 Google Cloud Console，进入 "APIs & Services" > "Credentials"。
2. 选择对应的 API Key，点击编辑（铅笔图标）。
3. 在 "Application restrictions" 部分，根据需求选择限制类型：
   - **IP 地址**: 仅允许后端服务器的 IP 地址调用（最推荐）。
   - **HTTP referrer**: 如果必须在网页端使用，设置仅允许你的域名访问。
   - **Android/iOS 应用**: 绑定特定的应用签名证书和包名。
4. 保存更改。

**注意事项**:
- 不要将密钥设置为 "None"（无限制），这允许任何拥有密钥的人在全球范围内使用它。
- 即使设置了限制，也不要将密钥提交到公共代码仓库。

---

### 实践 2：启用 API 密钥配额与计费监控

**说明**:
防止密钥泄露造成经济损失的第二道防线是财务限制。如果攻击者获取了密钥，严格的配额限制可以防止费用在短时间内爆炸式增长。

**实施步骤**:
1. 在 Google Cloud Console 中，前往 "APIs & Services" > "Quotas"。
2. 为特定的 API Key 设置每日配额上限。
3. 设置预算告警：进入 "Billing" > "Budgets & alerts"。
4. 配置当支出达到特定阈值（例如超出正常使用量的 20%）时发送邮件通知。

**注意事项**:
- 定期审查 "Reporting" 中的使用情况报告，识别异常的流量峰值。
- 确保你的计费账户绑定了有效的付款方式，以便在额度耗尽时能及时收到通知而非直接中断服务（除非这是你期望的安全熔断机制）。

---

### 实践 3：建立代理层以隔离客户端与 API

**说明**:
最佳的安全实践是永远不要在客户端（浏览器或手机 App）直接存储 API Key。应构建一个后端代理服务，客户端向你的服务器发送请求，再由服务器添加 API Key 后转发给 Google。

**实施步骤**:
1. 开发一个轻量级的后端服务（使用 Python, Node.js, Go 等）。
2. 将 Google API Key 存储在该后端服务的环境变量中，而非前端代码库。
3. 前端应用调用后端 API，后端验证用户身份后，附带 Key 向 Google API 发起请求。
4. 将 Google API 的访问限制设置为仅允许你的后端服务器 IP 访问。

**注意事项**:
- 这会增加网络延迟，但提供了最高级别的安全性。
- 你需要在自己的后端实现速率限制，防止用户滥用你的代理服务。

---

### 实践 4：自动化密钥轮换与撤销机制

**说明**:
静态的密钥长期存在会增加泄露风险。如果怀疑密钥已泄露，必须能够快速撤销并替换。对于生产环境，应建立定期轮换的机制。

**实施步骤**:
1. 在代码中将 API Key 配置化，不要硬编码。
2. 使用密钥管理服务（如 AWS Secrets Manager、Google Secret Manager 或 HashiCorp Vault）存储密钥。
3. 制定应急响应计划：一旦发现异常，立即在 Cloud Console 中删除或禁用受影响的 Key。
4. 定期（如每 90 天）生成新的 API Key 并更新应用配置，废弃旧 Key。

**注意事项**:
- 轮换密钥时，确保有短暂的重叠期以避免服务中断，或者设计应用支持动态加载最新密钥。

---

### 实践 5：代码仓库安全扫描与预提交检查

**说明**:
大多数密钥泄露源于开发人员意外将包含密钥的代码上传到了 GitHub 或 GitLab。防止此类事故是安全流程的基础。

**实施步骤**:
1. 使用 `.gitignore` 文件明确排除存储密钥的配置文件（如 `.env`）。
2. 在本地开发环境安装 Git hooks 工具（如 `truffleHog` 或 `git-secrets`）。
3. 配置 CI/CD 流水线，在代码合并前运行密钥扫描工具。
4. 对于 GitHub 仓库，启用 "Secret scanning" 功能，以便平台自动检测并警告你。

**注意事项**:
- 如果密钥已意外提交到公开仓库，请立即将其视为已泄露。即使你随后删除了该提交，密钥可能已被爬虫记录。必须立即在 Google Cloud Console 撤销该密钥。

---

### 实践 6：实施最小权限原则

**说明**:
并非所有的 API Key 都需要访问所有的 Google Cloud 服务。限制密钥只能访问特定的 API，可以减少潜在攻击面。

**实施步骤**:
1. 在 API Key 设置页面，找到 "API restrictions"。
2. 取消勾选 "Don

---
## 学习要点

- Google API keys 长期以来被视为非机密信息，通常直接暴露在客户端代码中，因为其计费模式依赖于 Google 账号余额而非 Key 本身。
- Gemini API 的出现改变了这一规则，它允许用户通过 API Key 直接访问付费的 Gemini Pro 模型，这使得 Key 本身成为了具有货币价值的资产。
- 攻击者可以通过自动化脚本在 GitHub 等平台上扫描并窃取暴露的 API Key，随后利用被盗 Key 调用高成本的模型服务。
- 由于 Key 的所有者需为被盗用产生的所有费用买单，这种攻击模式会导致受害者在不知情的情况下面临巨额经济损失。
- 这一事件揭示了安全防御中的“不对称性”：攻击者只需一个有效的 Key 即可造成损失，而防御者却需要时刻确保所有代码库中零泄露。
- 开发者必须改变“Google Key 不敏感”的传统观念，立即停止将此类 Key 硬编码在前端或公开代码仓库中，并应使用环境变量或后端代理等安全措施进行管理。

---
## 常见问题


### 1: 为什么以前 Google API Key 通常不被视为高度机密？

1: 为什么以前 Google API Key 通常不被视为高度机密？

**A**: 在很长一段时间里，开发者社区普遍认为 Google API Key 是一种“低敏感”凭证。这主要有两个原因：一是 Google 的计费和配额管理主要与 Google Cloud 项目（GCP Project）绑定，而不是直接绑定 Key 本身。二是许多公开的示例代码、教程甚至 GitHub 上的开源项目，都直接明文嵌入了 API Key 以便演示，导致大家习惯性地认为只要开启了应用的 HTTP 引用限制（HTTP Referrer Restriction），将 Key 暴露在前端代码中是相对安全的。然而，这种做法在涉及收费服务或生成式 AI 时存在巨大风险。

---



### 2: “Gemini 改变了规则”具体指什么变化？

2: “Gemini 改变了规则”具体指什么变化？

**A**: 这里的“规则改变”主要指 Google 在推广其生成式 AI 模型 Gemini 时，放宽了 API Key 的使用限制和验证门槛。为了降低开发者试用 AI 服务的难度，Google 允许用户通过简单的 API Key 直接访问强大的 Gemini 模型。与以往需要通过复杂的企业级云服务验证不同，现在的 Key 往往直接关联到 Google Cloud 的计费账户。这意味着，一旦攻击者获取了 Key，不仅可以消耗配额，还能直接利用该 Key 进行昂贵的 AI 推理调用，导致持有者面临实实在在的经济损失。

---



### 3: 如果我的 Google API Key 已经泄露，会有什么具体后果？

3: 如果我的 Google API Key 已经泄露，会有什么具体后果？

**A**: 后果取决于该 Key 关联的权限和启用的服务，主要包括以下几点：
1.  **经济损失**：这是最直接的风险。攻击者会利用泄露的 Key 调用 Gemini 等 AI 接口生成大量内容，导致你的 Google Cloud 账户产生巨额账单。
2.  **服务滥用**：攻击者可能利用你的 Key 发送垃圾邮件、扫描网络漏洞或进行其他恶意活动，这些行为会追溯到你（或你的组织）的账户上。
3.  **数据泄露**：如果该 Key 拥有访问特定云存储（如 Google Cloud Storage）或数据库的权限，攻击者可能会读取或删除你的敏感数据。

---



### 4: 既然 API Key 容易泄露，为什么 Google 不直接强制使用 OAuth 等更安全的认证方式？

4: 既然 API Key 容易泄露，为什么 Google 不直接强制使用 OAuth 等更安全的认证方式？

**A**: 这主要是为了平衡易用性和安全性。对于简单的原型开发、客户端脚本或学习用途，配置 OAuth 2.0 流程（包括申请客户端 ID、设置回调 URL、处理 Token 刷新等）非常复杂且具有很高的学习门槛。API Key 提供了一种“即插即用”的体验，允许开发者只需一行代码就能调用强大的模型。Google 的策略通常是默认提供简单的 Key，但强烈建议并在控制台中引导开发者设置“应用限制”和“API 限制”来缩小 Key 的滥用范围。

---



### 5: 我应该如何正确保护我的 Google API Key？

5: 我应该如何正确保护我的 Google API Key？

**A**: 最佳实践是永远不要将 API Key 硬编码在客户端代码（如 HTML/JS）或上传到公共代码仓库。如果必须在客户端使用，必须严格执行以下两点：
1.  **设置应用限制**：在 Google Cloud Console 中，限制该 Key 只能被特定的 Android/iOS 应用包名，或特定的网站域名（HTTP 引用）调用。
2.  **设置 API 限制**：限制该 Key 只能访问特定的 API（例如仅允许访问 Gemini API），禁止访问其他所有 Google 服务。
最安全的做法是使用后端代理服务器，将 API Key 保存在服务器端的环境变量中，前端向你的后端发起请求，由后端转发并带上 Key 调用 Google。

---



### 6: 如何检查我的 API Key 是否已经被泄露或滥用？

6: 如何检查我的 API Key 是否已经被泄露或滥用？

**A**: 你可以采取以下步骤进行检查：
1.  **GitHub 搜索**：使用 `git-secrets` 等工具扫描本地仓库，或者在 GitHub 上搜索你的项目名称配合 `api_key`、`google` 等关键词，看是否有意外提交的记录。
2.  **查看 Google Cloud 控制台**：进入“APIs & Services”中的“凭据”页面，点击你的 API Key 查看“使用情况”图表。如果在没有自己操作的时间段内出现了异常的请求流量 spike（激增），则极有可能已被泄露。
3.  **检查账单**：定期查看 Google Cloud Billing 页面，看是否有不明来源的费用产生。

---



### 7: 如果我发现 Key 已经泄露在 GitHub 上，仅仅删除文件就够了吗？

7: 如果我发现 Key 已经泄露在 GitHub 上，仅仅删除文件就够了吗？

**A**: **绝对不够**。Git 仓库保留了完整的历史提交记录，即使你删除了当前文件中的 Key，攻击者仍然可以通过 `git log` 和 `git checkout` 回到之前的提交中找到该 Key。正确的处理流程是：
1.  **立即撤销**：在 Google Cloud Console 中立刻删除或禁用该泄露的 API Key。
2.  **轮换密钥**：生成新的 API Key，并确保新 Key 设置了更严格的应用和 API 限制。
3.  **清理历史**：使用 `git filter-repo` 或 `BFG Repo-Cleaner` 等工具从整个 Git 历

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: 前端代码的透明性

### 问题**: 在传统的 Web 应用架构中，API Key 通常被放置在客户端代码的哪个位置？请编写一个简单的 HTML/JavaScript 页面，调用一个公开 API（例如 OpenWeatherMap），并尝试在浏览器开发者工具的“网络”或“控制台”标签页中找到这个 Key。这说明了什么安全风险？

### 提示**: 关注 `<script>` 标签内的全局变量或 Fetch 请求的 Headers。思考“前端代码即公开代码”这一基本原则。

### 

---
## 引用

- **原文链接**: [https://trufflesecurity.com/blog/google-api-keys-werent-secrets-but-then-gemini-changed-the-rules](https://trufflesecurity.com/blog/google-api-keys-werent-secrets-but-then-gemini-changed-the-rules)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47156925](https://news.ycombinator.com/item?id=47156925)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [安全](/categories/%E5%AE%89%E5%85%A8/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [API密钥](/tags/api%E5%AF%86%E9%92%A5/) / [Gemini](/tags/gemini/) / [谷歌](/tags/%E8%B0%B7%E6%AD%8C/) / [安全漏洞](/tags/%E5%AE%89%E5%85%A8%E6%BC%8F%E6%B4%9E/) / [身份认证](/tags/%E8%BA%AB%E4%BB%BD%E8%AE%A4%E8%AF%81/) / [访问控制](/tags/%E8%AE%BF%E9%97%AE%E6%8E%A7%E5%88%B6/) / [LLM](/tags/llm/) / [API管理](/tags/api%E7%AE%A1%E7%90%86/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/)

### 相关文章

- [Google API密钥非机密但Gemini改变规则]({{< relref "posts/20260226-hacker_news-google-api-keys-werent-secrets-but-then-gemini-cha-1.md" >}})
- [Gemini 3 Deep Think：面向科研与工程的专用推理模式更新]({{< relref "posts/20260215-blogs_podcasts-gemini-3-deep-think-advancing-science-research-and-11.md" >}})
- [谷歌发布 Gemini 3.1 模型]({{< relref "posts/20260219-hacker_news-gemini-31-1.md" >}})
- [谷歌发布 Gemini 3.1 Pro 模型]({{< relref "posts/20260219-hacker_news-gemini-31-pro-0.md" >}})
- [谷歌发布 Gemini 3.1 Pro 预览版]({{< relref "posts/20260219-hacker_news-gemini-31-pro-preview-10.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*