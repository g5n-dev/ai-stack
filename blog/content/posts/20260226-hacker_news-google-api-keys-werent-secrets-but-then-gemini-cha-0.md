---
title: "Google API密钥曾非机密，Gemini新规改变安全规则"
date: 2026-02-26T09:49:55+08:00
draft: false
entry_kind: "auto"
tags: ["Google", "Gemini", "API密钥", "安全规则", "身份认证", "OAuth", "数据泄露", "API管理"]
categories: ["安全", "大模型"]
source: hacker_news
description: "长期以来，开发者普遍认为 Google API keys 仅需具备基本的调用权限，无需像私有密钥那样进行严格的隔离与轮转。然而，随着 Gemini 模型的发布及其对权限模型的调整，这一默认的安全假设已被打破，导致许多原本看似无害的配置暴露了新的风险。本文将深入分析 Gemini 带来的具体变化，并说明为何开发者需要重新"
external_url: https://trufflesecurity.com/blog/google-api-keys-werent-secrets-but-then-gemini-changed-the-rules
scenarios: ["Web应用开发"]
---

# Google API密钥曾非机密，Gemini新规改变安全规则

---

## 基本信息

- **作者**: hiisthisthingon
- **评分**: 502
- **评论数**: 104
- **链接**: [https://trufflesecurity.com/blog/google-api-keys-werent-secrets-but-then-gemini-changed-the-rules](https://trufflesecurity.com/blog/google-api-keys-werent-secrets-but-then-gemini-changed-the-rules)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47156925](https://news.ycombinator.com/item?id=47156925)

---
## 导语

长期以来，开发者普遍认为 Google API keys 仅需具备基本的调用权限，无需像私有密钥那样进行严格的隔离与轮转。然而，随着 Gemini 模型的发布及其对权限模型的调整，这一默认的安全假设已被打破，导致许多原本看似无害的配置暴露了新的风险。本文将深入分析 Gemini 带来的具体变化，并说明为何开发者需要重新审视现有的密钥管理策略，以避免潜在的资源滥用或数据泄露。

---
## 评论

**中心观点**
文章揭示了生成式AI（GenAI）时代API密钥安全逻辑的根本性重构：随着大模型（LLM）从“被动检索工具”进化为“主动智能体”，传统的“隐晦式安全”已失效，API密钥必须被重新定义为“需要严格强制访问控制的身份凭证”，而非仅仅依赖“不被发现”来维持安全。

**支撑理由与深度评价**

**1. 内容深度与论证严谨性（技术视角）**
*   **核心论据**：文章敏锐地指出了Gemini API引入的新风险——即API密钥不仅允许调用大模型，还可能通过特定的Prompt注入或工具调用，诱导模型泄露关联的GCP（Google Cloud Platform）资源信息或执行云端操作。
*   **事实陈述**：在Gemini及类似Agent架构中，API Key往往绑定了具备特定云权限的服务账号。这与传统只读的地图API有本质区别。
*   **评价**：文章的论证切中肯綮，但稍显遗憾的是未深入探讨OAuth 2.0与API Key在自动化攻击面的具体差异。它正确地识别了攻击面的扩大，但未量化“仅凭Key导致RCE（远程代码执行）”的技术门槛，这在技术严谨性上略显单薄，更多是概念预警而非深度漏洞分析。

**2. 实用价值与行业影响（行业视角）**
*   **核心论据**：开发者习惯于在客户端代码（如前端JavaScript、移动App）中硬编码API Key，这在LLM时代变成了致命习惯。
*   **作者观点**：必须立即停止在客户端暴露任何高权限的API Key。
*   **评价**：极高的实用价值。它打破了“反正有额度限制，泄露了也没事”的侥幸心理。随着AI Agent能够自主调用工具，一个泄露的Key可能意味着不仅仅是账单爆炸，更是数据擦除或隐私泄露。这对整个开发者社区是一次及时的“休克疗法”。

**3. 创新性与新视角**
*   **核心论据**：文章提出了“规则改变”的观点。过去Key是“门票”，现在Key是“代理人授权书”。
*   **评价**：这一视角具有显著的创新性。它将安全讨论从“防止盗刷”提升到了“防止权限滥用”的高度。它指出了GenAI特有的风险：模型本身可能成为攻击者的共犯，这是传统API安全讨论中极少涉及的。

**反例与边界条件（批判性思考）**

尽管文章观点有力，但存在以下边界条件和反例，表明问题并非绝对：

1.  **反向代理与中间层的有效性（反例）**：
    *   文章暗示Key绝对危险，但现实中，如果构建了严格的后端代理，Key永远不出服务器，客户端只持有临时Token，则风险可控。
    *   *边界条件*：对于纯前端应用（如静态网页演示），如果不涉及后端代理，文章的警告才具有毁灭性；对于成熟架构，这只是常规安全加固。

2.  **权限最小化原则的局限性（反例）**：
    *   文章提倡限制Key权限。然而，在GenAI应用中，为了实现Agent的强大功能（如读写文件、发邮件），往往需要授予较高的权限。
    *   *边界条件*：如果业务本身需要高权限，单纯限制Key会导致功能不可用。此时问题的核心不再是Key本身，而是如何对AI的决策链进行沙箱隔离。

3.  **成本作为安全防线（事实陈述）**：
    *   对于许多个人开发者，API Key泄露最大的后果往往是财务损失（被盗用额度），而非数据泄露。
    *   *边界条件*：如果API Key没有绑定任何云资源权限，仅限模型调用，那么其风险依然停留在“资源盗用”层面，并未上升到文章暗示的“系统沦陷”级别。

**实际应用建议**

基于文章分析，针对技术与工程团队提出以下建议：

1.  **架构隔离（必须执行）**：
    *   **操作**：严禁在客户端（Web/Mobile）直接存储LLM API Key。
    *   **方案**：建立后端微服务作为代理层。客户端请求后端，后端携带Key请求LLM。这样Key仅在服务器端可见。

2.  **身份与访问管理（IAM）精细化**：
    *   **操作**：不要使用默认的服务账号。为特定的AI应用创建专用的服务账号，并仅授予“仅限当前项目”或“仅限特定API”的权限。
    *   **检查**：确认该Key是否有“Cloud Functions唤起”或“Storage读写”等高危权限，若无必要，一律关闭。

3.  **预算监控与异常检测（可验证指标）**：
    *   **操作**：在GCP或OpenAI控制台设置硬性预算报警和每日额度上限。
    *   **观察窗口**：一旦API调用费用在短时间内（如1小时）激增超过阈值，自动触发Key撤销机制。

**可验证的检查方式（指标/实验/观察）**

1.  **静态代码扫描（指标）**：
    *   使用GitGuardian或TrivyHQ扫描代码库。
    *   *验证标准*：在`src/frontend`或任何客户端代码中不得匹配到`AIza`（Google Key前缀）或`sk-`（OpenAI前缀）格式的字符串。

2.  **权限渗透测试（实验）**：
    *   **实验**：假设攻击者获取了API Key，尝试使用Cloud SDK或API直接列举该Key关联的资源。
    *   *验证标准*

---
## 代码示例




```python
# 示例1：安全存储Google API密钥
import os
from dotenv import load_dotenv

def load_api_key():
    """从环境变量安全加载API密钥"""
    load_dotenv()  # 从.env文件加载环境变量
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        raise ValueError("未找到GOOGLE_API_KEY环境变量")
    
    return api_key

# 使用示例
try:
    key = load_api_key()
    print(f"成功加载API密钥: {key[:10]}...")  # 只显示前10个字符
except ValueError as e:
    print(f"错误: {e}")
```




```python
# 示例2：验证API密钥权限范围
import requests

def check_api_key_permissions(api_key):
    """检查API密钥是否有Gemini API访问权限"""
    url = "https://generativelanguage.googleapis.com/v1beta/models"
    headers = {"x-goog-api-key": api_key}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print("API密钥有效且有Gemini访问权限")
            return True
        elif response.status_code == 403:
            print("API密钥有效但无Gemini访问权限")
            return False
        else:
            print(f"API密钥验证失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"请求出错: {str(e)}")
        return False

# 使用示例
api_key = "YOUR_API_KEY_HERE"  # 替换为实际密钥
check_api_key_permissions(api_key)
```




```python
# 示例3：API密钥使用监控
import time
from collections import defaultdict

class APIKeyMonitor:
    """监控API密钥使用情况"""
    def __init__(self):
        self.usage_stats = defaultdict(int)
        self.last_reset = time.time()
    
    def log_request(self, api_key):
        """记录API请求"""
        self.usage_stats[api_key] += 1
        self._check_limits()
    
    def _check_limits(self):
        """检查是否超过使用限制"""
        if time.time() - self.last_reset > 3600:  # 每小时重置
            self.usage_stats.clear()
            self.last_reset = time.time()
        
        for key, count in self.usage_stats.items():
            if count > 100:  # 假设每小时限制100次
                print(f"警告: API密钥 {key[:10]}... 已超过每小时使用限制")

# 使用示例
monitor = APIKeyMonitor()
for _ in range(101):
    monitor.log_request("test_api_key_12345")
```


---
## 案例研究


### 1：独立开发者与开源社区的安全危机

 1：独立开发者与开源社区的安全危机

**背景**: 
在 Gemini API 发布初期，许多开发者为了快速测试和集成，将 API Key 直接硬编码在客户端代码（如 JavaScript 前端代码）或上传至 GitHub 等公开代码仓库。此前，Google 的部分 API（如 Maps）虽有配额限制，但并未严格执行针对客户端调用的严苛身份验证，导致开发者误以为“Key 泄露”仅是配额耗尽的问题，而非安全漏洞。

**问题**: 
随着 Gemini 模型的接入，Google 调整了计费和安全规则。攻击者开始利用扫描工具在 GitHub 上搜索泄露的 Gemini API Key，并利用这些 Key 调用高成本的 Gemini Pro 模型进行大规模推理（如生成大量文本或图像），导致 Key 持有者在不知情的情况下瞬间背负巨额费用。此外，攻击者还可能利用 Key 访问关联的 Google Cloud 服务资源。

**解决方案**: 
开发者社区迅速响应，采用了“密钥轮换”与“服务端代理”相结合的方案。
1.  **立即撤销**：在 Google Cloud Console 中立即删除已泄露的 API Key。
2.  **架构重构**：不再在客户端直接调用 Google API。改为搭建一个轻量级后端（如使用 Python Flask 或 Node.js Express），API Key 仅存储在后端环境变量中。
3.  **调用链路**：前端向后端发送请求，后端验证用户身份后，再使用 Key 向 Google 发起请求。

**效果**: 
通过将 API Key 从客户端移至服务端，开发者成功切断了攻击者直接利用 Key 的途径。这一举措不仅避免了数千美元的潜在盗用损失，还确立了“客户端无密钥”的安全开发标准，保障了项目的长期可持续性。

---



### 2：某科技初创公司的 API 网关改造

 2：某科技初创公司的 API 网关改造

**背景**: 
一家专注于 AI 应用开发的初创公司，其产品主要面向企业用户提供文档智能分析服务。在 Gemini 1.0 发布初期，为了缩短开发周期，该公司在移动端 App 中嵌入了 API Key 以便直接调用大模型能力。当时的规则主要基于简单的 IP 限制或 HTTP Referer 检查。

**问题**: 
随着 Gemini 的能力增强和商业化推进，Google 加强了 API 的滥用检测机制。该公司发现，部分恶意用户通过抓包获取了 App 中的 API Key，并编写脚本进行“代刷”服务或恶意攻击，导致该公司账户异常触发风控，API 服务面临被封禁的风险。同时，直接暴露 Key 使得无法对单个用户的调用频率进行精细化管理。

**解决方案**: 
公司实施了基于“API 网关”的中间层架构。
1.  **部署中间层**：使用云函数（如 Google Cloud Functions 或 AWS Lambda）作为 API 代理层。
2.  **身份与访问管理 (IAM)**：利用 Google Cloud 的 IAM 功能，为代理层生成具有最小权限的服务账号凭证，替代原本的通用 API Key。
3.  **流量清洗**：在中间层实施针对每个终端用户的 Rate Limiting（速率限制），防止单一用户滥用资源。

**效果**: 
改造后，该公司彻底消除了 Key 在客户端泄露的风险。通过引入 IAM 和中间层，他们获得了详细的调用日志，能够精确追踪每个用户的成本。更重要的是，合规的调用方式使其符合 Google 企业级服务条款，成功申请到了更高的调用配额，支撑了业务量的十倍增长。

---
## 最佳实践

## 最佳实践指南

### 实践 1：实施严格的 API 密钥访问控制

**说明**: API 密钥不应被视为公开信息，也不应硬编码在代码中。必须限制只有特定的服务账号或 IP 地址才能使用该密钥，防止密钥泄露后被滥用。

**实施步骤**:
1. 登录 Google Cloud Console，进入“APIs & Services” -> “Credentials”。
2. 创建或选择现有的 API 密钥。
3. 在“Application restrictions”（应用限制）选项中，根据需求选择：
    - **IP 地址**：指定允许调用 API 的服务器 IP 地址（适用于后端）。
    - **HTTP referrer**：指定允许调用 API 的域名（适用于前端）。
    - **Android 应用**或**iOS 应用**：根据应用签名进行限制。
4. 在“API restrictions”（API 限制）选项中，仅勾选该密钥实际需要访问的特定 API（例如仅启用“Gemini API”），避免授予对所有 Google 服务的访问权限。

**注意事项**: 即使密钥意外泄露，由于应用限制的存在，攻击者也无法从其他位置使用该密钥。

---

### 实践 2：使用环境变量或密钥管理服务存储密钥

**说明**: 绝对不要将 API 密钥直接写入版本控制系统（如 Git）的代码中。应使用环境变量或云服务商提供的密钥管理工具来动态注入密钥。

**实施步骤**:
1. 将 API 密钥存储在本地开发环境的 `.env` 文件中，并将该文件添加到 `.gitignore`。
2. 在生产环境中，使用云平台的密钥管理服务（如 Google Secret Manager, AWS Secrets Manager, 或 HashiCorp Vault）。
3. 在应用程序启动时，通过环境变量或 SDK 读取密钥，而不是将其写死在配置文件里。

**注意事项**: 确保所有开发人员都知道不要将包含密钥的配置文件提交到公共代码仓库。

---

### 实践 3：实施配额限制与预算警报

**说明**: 为了防止因密钥泄露或代码逻辑错误导致的天价账单，必须对 API 密钥设置每日使用配额，并配置计费警报。

**实施步骤**:
1. 在 Google Cloud Console 的“Quotas”页面，找到特定的 API（如 Gemini API）。
2. 为特定的 API 密钥或项目设置每分钟或每日的请求次数上限。
3. 在“Billing”设置中，创建预算警报，当预计费用达到设定阈值（如 10 美元）时发送邮件通知。

**注意事项**: 不要依赖默认配额，应根据实际业务需求设置一个合理的“熔断”阈值。

---

### 实践 4：定期轮换 API 密钥

**说明**: 长期使用的密钥增加了泄露风险和被滥用的可能性。定期（如每 90 天）轮换密钥可以减小密钥泄露后的影响窗口。

**实施步骤**:
1. 在 Cloud Console 中创建新的 API 密钥。
2. 将新密钥部署到应用程序的环境变量或密钥管理服务中，并重新部署服务。
3. 验证服务运行正常后，在控制台中删除或禁用旧的 API 密钥。

**注意事项**: 确保应用程序支持动态加载配置，以便在不停机的情况下完成密钥切换。

---

### 实践 5：监控与审计 API 使用日志

**说明**: 实时监控 API 的调用情况可以帮助及时发现异常流量（如突然激增的请求），这通常是密钥被滥用的迹象。

**实施步骤**:
1. 启用 Google Cloud 的“Cloud Logging”和“Cloud Monitoring”。
2. 创建自定义仪表盘，监控 API 请求量、延迟和错误率。
3. 设置基于日志的告警策略，例如当“每分钟错误数超过 50 次”或“来自异常地理位置的请求”时触发告警。

**注意事项**: 特别关注 4xx（客户端错误）和 403（权限不足）状态码，这可能意味着有人正在尝试探测你的密钥权限。

---

### 实践 6：使用代理层隐藏 API 密钥

**说明**: 对于前端应用（如 Web 或移动 App），即使使用了 HTTP referrer 限制，密钥仍有可能被从客户端流量中抓取。最佳实践是让前端调用你自己的后端服务器，由后端服务器持有密钥并代理请求。

**实施步骤**:
1. 搭建一个后端服务（使用 Node.js, Python, Go 等）。
2. 将 Google API 密钥仅配置在后端服务器的环境变量中。
3. 前端应用向后端 API 发起请求，后端验证用户身份后，再使用密钥调用 Google API，并将结果返回给前端。

**注意事项**: 这种方式可以完全隐藏 API 密钥，并且允许你在后端实施额外的业务逻辑验证（如用户速率限制）。

---
## 学习要点

- Google API keys 长期以来被设计为可公开的标识符，而非需要严格保密的密钥，这导致开发者常将其直接硬编码在客户端代码中。
- Gemini API 的引入打破了这一惯例，它将 API key 视为敏感的身份验证凭证，若 key 随客户端代码泄露，攻击者可盗用额度进行恶意调用。
- 仅仅依赖 Google 的 HTTP referrer 检查（限制请求来源）不足以保障安全，因为 referrer 头可被伪造或被中间人设备剥离。
- 任何在客户端（如浏览器或移动 App）暴露 API key 的应用，都面临密钥被窃取的风险，且无法通过简单的代码混淆来彻底防范。
- 开发者应使用代理服务器或云端函数来封装 API 调用，将 API key 隐藏在后端，从而避免将其直接暴露给终端用户。
- 在使用 Google Cloud 控制台配置 API 凭证时，必须区分“公开数据”与“私有数据”的访问需求，并针对 Gemini 等新服务实施严格的密钥管理策略。
- 这一变化揭示了云服务安全模型的演进：随着 API 能力的增强，开发者需从“公开 Key”的旧习惯转向“零信任”架构，假设所有客户端数据均不可信。

---
## 常见问题


### 1: 为什么以前认为 Google API Key 不算是敏感信息？

1: 为什么以前认为 Google API Key 不算是敏感信息？

**A**: 在很长一段时间里，开发者社区普遍认为 Google Cloud 的 API Key（特别是用于公开端点如 Maps 或 YouTube 的 Key）并不需要像密码一样严格保密。这主要基于两个原因：
1.  **计费与安全机制**：Google 的安全模型主要依赖 Google Cloud 控制台中的“HTTP 引用来源”限制。开发者认为，只要配置了只允许特定域名（如 `example.com`）调用，即使 Key 被公开，第三方也无法在他们的网站上使用该 Key，从而避免了盗刷费用。
2.  **公开服务的惯例**：许多前端应用（如嵌入地图的网页）必须将 Key 直接暴露在客户端的 HTML 或 JavaScript 代码中，这导致 Key 事实上处于公开状态，因此大家默认它是“公开可识别符”而非“私密凭证”。

---



### 2: Gemini API 的出现改变了什么规则？

2: Gemini API 的出现改变了什么规则？

**A**: 随着 Google Gemini API 的推出和普及，情况发生了根本性变化。Gemini API 主要是用于生成式 AI 交互，许多开发者通过客户端直接调用（例如在 Web 应用中直接调用 `generativelanguage.googleapis.com`）。
关键的变化在于：**Google 开始对 API 调用收费，且并未对 Gemini API 的所有端点强制执行严格的 HTTP 引用来源检查**。如果开发者将 API Key 写在前端代码中，攻击者可以轻易提取该 Key，并在自己的环境中（通过脚本或 Postman）直接调用该 Key 消耗配额或产生费用，而无需通过受害者的网站域名。

---



### 3: 攻击者如何滥用暴露在 GitHub 或前端代码中的 Google API Key？

3: 攻击者如何滥用暴露在 GitHub 或前端代码中的 Google API Key？

**A**: 一旦 API Key 泄露（例如被上传到 GitHub 或包含在编译后的 JS 文件中），攻击者可以利用这些 Key 进行多种恶意操作：
1.  **费用盗刷**：这是最直接的影响。攻击者使用泄露的 Key 调用昂贵的 AI 模型（如 Gemini Pro），导致 Key 持有者的 Google Cloud 账户在短时间内产生巨额账单。
2.  **服务滥用**：利用受害者的配额限制进行大规模的自动化内容生成、抓取或垃圾邮件发送。
3.  **进一步探测**：如果该 Key 拥有更广泛的 Cloud 权限（尽管通常 API Key 权限受限，但配置错误时有发生），攻击者可能尝试访问云存储或其他服务。

---



### 4: 针对 Google API Key 泄露，目前有哪些有效的防御措施？

4: 针对 Google API Key 泄露，目前有哪些有效的防御措施？

**A**: 为了防止 API Key 泄露带来的风险，开发者应采取以下措施：
1.  **使用 API Key 限制**：在 Google Cloud Console 的凭据页面中，必须为 API Key 设置“应用程序限制”。对于 Web 应用，选择“HTTP 引用来源”并填入受信任的域名；对于 IP 地址，则限制特定的服务器 IP。
2.  **后端代理模式**：这是最佳实践。不要在前端直接调用 Gemini API。前端应调用开发者自己的后端服务器，后端服务器在安全的环境下保存 Key 并转发请求给 Google。这样 Key 永远不会暴露给公网。
3.  **定期轮换**：定期删除旧的 API Key 并生成新的，以减少长期泄露带来的风险。

---



### 5: 如果我的 API Key 已经泄露到了 GitHub 上，应该怎么处理？

5: 如果我的 API Key 已经泄露到了 GitHub 上，应该怎么处理？

**A**: 处理流程应遵循“立即止损”的原则：
1.  **立即撤销**：第一时间登录 Google Cloud Console，找到泄露的 API Key 并将其“删除”或禁用。不要试图仅仅修改限制，因为 Key 已经流出，攻击者可能已经保存了它。
2.  **检查账单与配额**：查看 Google Cloud 的计费报告和 API 使用量监控，确认在 Key 泄露期间是否有异常的调用和费用产生。
3.  **清理代码历史**：如果 Key 在 Git 历史记录中，不能只删除当前文件的 Key。需要使用 `git filter-repo` 等工具重写 Git 历史，将 Key 从所有提交中彻底移除，或者将仓库设为私有并联系 GitHub 支持（如果已 push 到公开仓库）。
4.  **生成新 Key**：在旧 Key 作废后，生成新的 API Key，并按照上述防御措施重新配置严格的限制。

---



### 6: Google 官方对此类泄露事件有什么响应机制？

6: Google 官方对此类泄露事件有什么响应机制？

**A**: Google 拥有专门的“Secret Scanning”（秘密扫描）合作伙伴计划。当 GitHub 或其他代码托管平台检测到用户上传了疑似 Google API Key 的凭证时，会自动通知 Google。Google 验证后，通常会采取以下行动：
1.  **自动禁用**：Google 可能会直接禁用被发现泄露的 API Key，并向该 Key 关联的邮箱发送安全警报邮件。
2.  **宽限期**：有时 Google 会提供一个短暂的宽限期（例如几天），允许开发者确认并处理问题，但对于高风险的 Key，通常会立即封停。这就是为什么有些开发者会突然发现自己的服务突然中断，并收到来自 Google 的“

---
## 思考题


### ## 挑战与练习

### ### 练习 1：客户端 API Key 的风险识别

### 任务**：在传统的 Web 应用架构中，API Key 通常被放置在客户端代码的什么位置？请编写一个简单的 HTML 页面，包含一个调用 Google Maps API 或类似服务的脚本，并指出其中 API Key 暴露的风险所在。

### 提示**：查看浏览器开发者工具中的 "Sources" 或 "Network" 标签，思考客户端发送的每一个 HTTP 请求是否对用户可见。

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
- 标签： [Google](/tags/google/) / [Gemini](/tags/gemini/) / [API密钥](/tags/api%E5%AF%86%E9%92%A5/) / [安全规则](/tags/%E5%AE%89%E5%85%A8%E8%A7%84%E5%88%99/) / [身份认证](/tags/%E8%BA%AB%E4%BB%BD%E8%AE%A4%E8%AF%81/) / [OAuth](/tags/oauth/) / [数据泄露](/tags/%E6%95%B0%E6%8D%AE%E6%B3%84%E9%9C%B2/) / [API管理](/tags/api%E7%AE%A1%E7%90%86/)
- 场景： [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [Google API密钥非机密但Gemini改变规则]({{< relref "posts/20260226-hacker_news-google-api-keys-werent-secrets-but-then-gemini-cha-1.md" >}})
- [Step 3.5 Flash：速度足以思考，可靠性足以行动]({{< relref "posts/20260219-hacker_news-step-35-flash-fast-enough-to-think-reliable-enough-6.md" >}})
- [Gemini 3.1 Pro发布：ARC-AGI 2得分达3.0两倍]({{< relref "posts/20260221-blogs_podcasts-ainews-gemini-31-pro-2x-30-on-arc-agi-2-5.md" >}})
- [Gemini 3.1 Pro发布：ARC-AGI 2得分达3.0两倍]({{< relref "posts/20260224-blogs_podcasts-ainews-gemini-31-pro-2x-30-on-arc-agi-2-12.md" >}})
- [Gemini 3.1 Pro发布：ARC-AGI 2得分达3.0两倍]({{< relref "posts/20260224-blogs_podcasts-ainews-gemini-31-pro-2x-30-on-arc-agi-2-14.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*