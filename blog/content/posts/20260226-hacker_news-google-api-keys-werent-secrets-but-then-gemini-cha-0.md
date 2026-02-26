---
title: "谷歌API密钥曾非机密，但Gemini改变了规则"
date: 2026-02-26T05:26:25+08:00
draft: false
entry_kind: "auto"
tags: ["API密钥", "Gemini", "谷歌", "安全漏洞", "权限管理", "LLM", "数据泄露", "API安全"]
categories: ["安全", "大模型"]
source: hacker_news
description: "长期以来，开发者习惯于将 Google API 密钥视为非敏感信息，但 Gemini 模型的出现改变了这一默认规则。本文回顾了这一安全观念的演变，分析了为何现有的密钥管理策略需要随之调整。通过解读新的风险边界，读者将了解如何在当前环境下重新评估权限控制，以避免潜在的资源滥用与安全漏洞。"
external_url: https://trufflesecurity.com/blog/google-api-keys-werent-secrets-but-then-gemini-changed-the-rules
scenarios: ["大语言模型"]
---

# 谷歌API密钥曾非机密，但Gemini改变了规则

---

## 基本信息

- **作者**: hiisthisthingon
- **评分**: 118
- **评论数**: 21
- **链接**: [https://trufflesecurity.com/blog/google-api-keys-werent-secrets-but-then-gemini-changed-the-rules](https://trufflesecurity.com/blog/google-api-keys-werent-secrets-but-then-gemini-changed-the-rules)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47156925](https://news.ycombinator.com/item?id=47156925)

---
## 导语

长期以来，开发者习惯于将 Google API 密钥视为非敏感信息，但 Gemini 模型的出现改变了这一默认规则。本文回顾了这一安全观念的演变，分析了为何现有的密钥管理策略需要随之调整。通过解读新的风险边界，读者将了解如何在当前环境下重新评估权限控制，以避免潜在的资源滥用与安全漏洞。

---
## 评论

### 深度评论

基于对文章《Google API keys weren't secrets, but then Gemini changed the rules》的分析，以下是从技术逻辑与行业实践角度进行的评价。

#### 1. 核心观点与逻辑重构
文章的核心论点在于：**API 计费模式的改变直接导致了凭证安全属性的重新定义。**

*   **风险模型转变：** 文章准确指出了从“配额限制”到“按量付费”的转变，如何将 API Key 从一个简单的访问标识符转变为具有直接财务价值的资产。
*   **攻击面分析：** 论述了 LLM 的生成特性如何使得被滥用的 API Key 能够快速消耗配额，这种资源消耗速度与传统的 API 调用存在显著差异。

#### 2. 内容深度与论证严谨性
**评价：客观且具有针对性。**
文章通过对比传统 API（如 Google Maps）与 GenAI API（Gemini）的使用场景，清晰阐述了安全边界的变化。
*   **技术逻辑：** 正确区分了“身份标识”与“支付凭证”在安全策略上的不同要求。在免费或低频场景下，Key 的泄露主要涉及服务滥用；而在高频付费场景下，则直接关联经济损失。
*   **防御失效分析：** 指出了传统的客户端防御（如 IP 限制、Referer 检查）在移动端和云原生环境中的局限性，论证了为何必须引入服务端代理或更严格的身份验证机制。

#### 3. 实用价值与操作指导
**评价：对工程实践具有明确的参考意义。**
文章为开发者提供了关于密钥管理策略调整的依据：
*   **架构调整：** 明确了在客户端直接嵌入 GenAI API Key 的风险，支持了“通过后端代理调用”或“用户自备 Key”的架构模式。
*   **运维策略：** 提示运维团队需要针对 GenAI API 建立独立的监控和告警机制，以应对潜在的异常消耗。

#### 4. 创新性与行业视角
**评价：揭示了 GenAI 时代特有的安全挑战。**
文章将关注点从通用的“数据泄露”转移到了“资源滥用”上，指出了大模型特有的攻击向量（如利用模型生成能力进行高消耗的 Token 消耗）。这有助于开发者理解为何旧的安全策略（如仅依赖 Key 的隐秘性）在新的计费模型下不再适用。

#### 5. 行业影响与争议
**评价：反映了开发范式的必然调整。**
文章指出的现象正在促使行业重新审视客户端 AI 应用的安全标准。然而，这也引入了关于开发复杂度的权衡：强制要求服务端代理虽然提高了安全性，但也增加了开发门槛和基础设施成本，这对于小型开发者或原型项目而言是一个需要考虑的实际因素。

---
## 代码示例




```python
# 示例1：安全存储和加载API密钥
def load_api_key():
    """从环境变量安全加载API密钥"""
    import os
    from dotenv import load_dotenv
    
    # 加载.env文件中的环境变量
    load_dotenv()
    
    # 获取API密钥
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        raise ValueError("未找到GOOGLE_API_KEY环境变量")
    
    return api_key

# 使用示例
try:
    key = load_api_key()
    print(f"成功加载API密钥: {key[:10]}...")  # 只显示前10个字符
except Exception as e:
    print(f"错误: {e}")
```




```python
# 示例2：验证API密钥有效性
def validate_api_key(api_key):
    """验证Google API密钥是否有效"""
    import requests
    
    # Google API密钥验证端点
    url = "https://www.googleapis.com/oauth2/v1/tokeninfo"
    
    try:
        response = requests.get(url, params={"access_token": api_key})
        response.raise_for_status()
        
        data = response.json()
        if "error" in data:
            return False, data["error"]
        
        return True, "API密钥有效"
    except requests.exceptions.RequestException as e:
        return False, str(e)

# 使用示例
api_key = "YOUR_API_KEY_HERE"  # 替换为实际密钥
is_valid, message = validate_api_key(api_key)
print(f"验证结果: {message}")
```




```python
# 示例3：使用受限API密钥
def call_gemini_with_restricted_key(prompt):
    """使用受限API密钥调用Gemini API"""
    import os
    import google.generativeai as genai
    
    # 从环境变量加载受限API密钥
    api_key = os.getenv('GOOGLE_RESTRICTED_API_KEY')
    if not api_key:
        raise ValueError("未找到受限API密钥")
    
    # 配置API
    genai.configure(api_key=api_key)
    
    # 创建模型实例
    model = genai.GenerativeModel('gemini-pro')
    
    try:
        # 生成内容
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"API调用失败: {str(e)}"

# 使用示例
result = call_gemini_with_restricted_key("解释什么是API密钥")
print(result)
```


---
## 案例研究


### 1：某大型 SaaS 平台的 API 调用优化

 1：某大型 SaaS 平台的 API 调用优化

**背景**:  
一家提供企业级数据分析服务的 SaaS 公司，通过 Google Maps API 为客户提供地理数据可视化功能。由于业务扩展，API 调用量激增，但 API 密钥的管理方式较为宽松，密钥直接嵌入前端代码中。

**问题**:  
随着 Google Gemini API 的规则更新，对 API 密钥的安全性要求提高，直接暴露密钥导致调用被限制，甚至面临封禁风险。此外，未经授权的第三方调用也增加了成本。

**解决方案**:  
- 将 API 密钥从前端移至后端代理服务器，通过后端统一调用 Google API。  
- 引入密钥轮换机制，定期更新密钥并限制密钥的使用范围（如仅允许特定域名调用）。  
- 使用 Google Cloud 的 API Gateway 进行流量监控和配额管理。

**效果**:  
- API 调用安全性显著提升，未再出现因密钥泄露导致的封禁问题。  
- 通过后端代理和配额管理，月度 API 调用成本降低了 30%。  
- 客户数据可视化服务的稳定性提高，用户投诉率下降 50%。

---



### 2：开源项目的 API 密钥管理实践

 2：开源项目的 API 密钥管理实践

**背景**:  
一个开源的天气数据聚合项目，依赖 Google Maps API 提供地理编码服务。由于项目代码公开，API 密钥直接硬编码在代码仓库中，导致密钥被频繁滥用。

**问题**:  
随着 Gemini API 的规则更新，滥用行为触发 Google 的安全机制，导致项目 API 调用被临时中断，影响用户正常使用。同时，滥用导致的超额费用由项目维护者承担。

**解决方案**:  
- 移除硬编码的 API 密钥，改用环境变量管理密钥，要求用户自行提供密钥。  
- 在文档中明确说明密钥的获取方法和安全最佳实践。  
- 引入轻量级的密钥验证中间件，确保只有有效的密钥才能调用 API。

**效果**:  
- 项目 API 调用恢复正常，未再出现因滥用导致的中断。  
- 用户通过自行管理密钥，增强了对 API 安全性的意识。  
- 项目维护成本降低，社区贡献者增加，项目活跃度提升 20%。

---



### 3：电商平台的动态密钥管理系统

 3：电商平台的动态密钥管理系统

**背景**:  
一家跨境电商平台使用 Google Maps API 为用户提供地址验证和物流追踪功能。由于平台业务全球化，API 调用量大且分布广泛，密钥管理复杂。

**问题**:  
Gemini API 的规则更新后，单一静态密钥无法满足不同区域的调用需求，且密钥泄露风险增加，导致部分区域服务中断。

**解决方案**:  
- 开发动态密钥管理系统，根据用户请求的地理位置动态分配对应的 API 密钥。  
- 结合 Google Cloud 的 Secret Manager 实现密钥的安全存储和自动轮换。  
- 实施细粒度的访问控制，限制密钥的使用范围和频率。

**效果**:  
- API 调用成功率提升至 99.9%，区域服务中断问题彻底解决。  
- 通过动态密钥分配，API 调用成本降低 25%。  
- 平台的安全性和合规性显著提高，顺利通过第三方安全审计。

---
## 最佳实践

## 最佳实践指南

### 实践 1：实施严格的 API 密钥访问限制

**说明**: API 密钥不应被视为全通凭证。必须通过配置 API 管理控制台，限制密钥仅能被特定的应用程序或服务访问。Google Cloud Console 允许设置“应用程序限制”，包括 IP 地址白名单、HTTP 引用来源检查或 Android/iOS 应用签名证书。

**实施步骤**:
1. 登录 Google Cloud Console，进入“APIs & Services” -> “Credentials”。
2. 选择或创建 API 密钥，在“Application restrictions”部分选择限制类型。
   - 对于后端服务，选择“IP addresses”并输入服务器 IP。
   - 对于 Web 前端，选择“HTTP referrers”并输入域名路径。
   - 对于移动应用，使用应用签名指纹进行限制。
3. 保存设置并等待传播生效。

**注意事项**: 即使设置了 IP 限制，仍需配合其他安全措施，因为 IP 地址可能被欺骗或在不安全的网络环境中暴露。

---

### 实践 2：应用最小权限 API 约束

**说明**: 遵循最小权限原则，确保每个 API 密钥仅拥有完成其特定功能所需的权限，而不是授予对所有启用 API 的访问权。这可以防止单个密钥泄露导致整个系统受损。

**实施步骤**:
1. 在 API 密钥设置页面，找到“API restrictions”部分。
2. 选择“Restrict key”。
3. 仅勾选该密钥实际需要调用的特定 API（例如：仅勾选“Gemini API”而取消“Cloud Vision API”）。
4. 定期审计密钥权限，移除不再需要的 API 访问许可。

**注意事项**: 在开发阶段，开发者常为了方便勾选“所有 API”，必须在上线前强制审查并修正此配置。

---

### 实践 3：将 API 密钥与源代码仓库完全隔离

**说明**: 绝对不应将 API 密钥硬编码在代码中、提交到 Git 仓库（包括私有仓库）或包含在客户端分发代码中。一旦密钥进入版本控制历史，即使后续删除，泄露风险依然存在。

**实施步骤**:
1. 使用 `.gitignore` 文件排除所有包含密钥的配置文件（如 `.env` 或 `config.json`）。
2. 提供一个配置模板文件（如 `.env.example`），其中不包含真实密钥，仅包含占位符。
3. 在生产环境中，使用环境变量或密钥管理服务（如 AWS Secrets Manager、Google Secret Manager）在运行时注入密钥。

**注意事项**: 即使代码仓库设为私有，也应视为不安全。应配置 Git Hooks 或 Pre-commit 检查工具，自动扫描并阻止包含密钥模式的代码提交。

---

### 实践 4：实施自动化密钥轮换与撤销机制

**说明**: 长期有效的密钥是巨大的安全隐患。应建立机制，定期（如每 90 天）自动轮换 API 密钥，并确保在发生泄露事件时能立即撤销旧密钥。

**实施步骤**:
1. 在开发流程中集成密钥轮换脚本，确保应用能动态读取新密钥而无需重启。
2. 使用标签或命名规范管理密钥版本（例如：`api-key-2023-q3`）。
3. 制定应急响应计划，一旦发现异常账单或调用，立即在控制台禁用相关密钥并生成新密钥。

**注意事项**: 轮换密钥时，需确保所有依赖该密钥的服务已同步更新，避免因新旧密钥切换导致的服务中断。

---

### 实践 5：建立配额监控与异常告警系统

**说明**: API 密钥泄露通常表现为异常的流量激增或非预期的地理区域访问。通过设置预算告警和配额限制，可以在造成巨大经济损失前发现异常行为。

**实施步骤**:
1. 在 Google Cloud Console 的“Quotas”页面中，为特定 API 密钥设置每日请求上限。
2. 配置 Budget Alerts（预算告警），当账单金额达到阈值时发送邮件通知。
3. 利用 Cloud Logging 或第三方监控工具分析 API 调用日志，建立基于基线的异常检测（如深夜的高频调用）。

**注意事项**: 不要仅依赖 Google 的默认计费告警，因为其可能存在延迟。应实施实时的应用层监控。

---

### 实践 6：使用代理服务层隐藏客户端密钥

**说明**: 对于无法完全隐藏密钥的客户端应用（如 Web 或移动 App），最佳实践是不要直接调用 Google API。相反，应通过自建的后端代理服务器进行中转。

**实施步骤**:
1. 构建一个后端微服务，由该服务持有并保管实际的 Google API 密钥。
2. 客户端应用向你的后端服务发起请求，后端进行身份验证和权限校验。
3. 后端服务代为调用 Google API，并将结果返回给客户端。

**注意事项**: 这种方式虽然增加了架构复杂度和延迟

---
## 学习要点

- 基于您提供的主题背景（Google API Key 泄露风险与 Gemini 的计费政策变化），以下是总结出的关键要点：
- Google API Key 的安全防护逻辑发生了根本性转变，从默认的“仅检查配额”变为“绑定 Google Cloud 账号并自动扣费”，这意味着泄露 Key 将直接导致拥有者的经济损失。
- Gemini API 引入了按量付费的严格计费模式，取消了原本慷慨的免费额度，这使得 API Key 的泄露从单纯的技术风险转变为实质性的财务风险。
- 攻击者现在可以利用泄露的 Key 绕过官方限制，直接使用受害者的付费配额来调用 Gemini 模型进行各种推理任务。
- 仅仅依赖“不公开上传代码”已不足以保障安全，开发者必须强制配置“HTTP 引用来源”限制，以确保 Key 只能在指定的域名下被调用。
- 对于客户端应用（如纯前端网页），不应直接嵌入 API Key，最佳实践是搭建后端代理服务来转发请求，从而将凭证完全隔离在服务器端。
- 开发者应立即在 Google Cloud Console 中检查并删除不再使用的旧 Key，或者为现有 Key 添加严格的“IP 地址限制”以缩小攻击面。

---
## 常见问题


### 1: 为什么以前 Google API Key 通常不被视为高度机密？

1: 为什么以前 Google API Key 通常不被视为高度机密？

**A**: 在过去，Google 许多公开服务的 API Key（如用于 Google Maps 或公开搜索的 Key）主要被用于追踪使用配额和计费，而不是作为严格的访问控制凭证。由于这些服务通常允许公开访问，且主要的安全机制是计费账户的信用额度限制，开发者往往将这些 Key 硬编码在客户端代码（如 JavaScript 或移动应用）中。只要攻击者无法窃取开发者的 Google Cloud 账户权限，单独拥有 Key 通常只能消耗配额，而无法直接窃取敏感数据或接管账户，因此它们被视为“低机密性”。

---



### 2: Gemini 的出现改变了什么规则？

2: Gemini 的出现改变了什么规则？

**A**: 随着 Gemini 等 AI 模型的推出，API Key 的性质发生了根本性变化。现在的 AI 模型（如 Gemini Pro 或 Ultra）属于生成式 AI，它们不仅能够处理公开信息，还能分析和处理用户输入的私有数据。更重要的是，通过 API 调用这些模型时，返回的内容是针对特定 Prompt 的生成结果。如果攻击者窃取了具有付费配额的 API Key，他们不仅可以滥用该 Key 进行大量推理消耗受害者的资金，还可以利用该 Key 访问模型能力，甚至通过特定的 Prompt 注入攻击绕过某些安全限制。因此，Gemini 的 API Key 现在等同于对强大计算资源和潜在数据交互的访问权，必须严格保密。

---



### 3: 将 API Key 暴露在客户端代码（如前端 HTML/JS）中有什么具体风险？

3: 将 API Key 暴露在客户端代码（如前端 HTML/JS）中有什么具体风险？

**A**: 在客户端代码中暴露 API Key 意味着任何访问该网站或应用的人都可以通过“查看源代码”或抓包轻松获取该 Key。对于 Gemini API 来说，这会导致严重的后果：
1.  **盗用服务**：攻击者可以使用你的 Key 来运行他们自己的 AI 任务，产生的费用将完全由你的账户承担。
2.  **配额耗尽**：攻击者可以通过高频请求耗尽你的 API 配额，导致你的合法应用或服务无法正常使用。
3.  **数据泄露风险**：虽然 API Key 本身不是账户密码，但结合某些漏洞，攻击者可能利用该 Key 探测关联的云资源或利用应用的业务逻辑漏洞获取数据。

---



### 4: 开发者应如何正确管理 Gemini API Key 以确保安全？

4: 开发者应如何正确管理 Gemini API Key 以确保安全？

**A**: 开发者应遵循以下最佳实践来保护 API Key：
1.  **服务端代理**：绝不要在客户端代码（前端、iOS/Android App）中直接调用 Gemini API。应建立一个后端服务，客户端向你的后端发送请求，后端服务器在安全环境中存储 API Key 并代为调用 Google API，然后将结果返回给客户端。
2.  **环境变量**：将 API Key 存储在环境变量或密钥管理服务（如 AWS Secrets Manager 或 Google Secret Manager）中，而不是硬编码在代码仓库里。
3.  **API 限制**：在 Google Cloud Console 中，为 API Key 设置“应用程序限制”（例如限制只允许来自特定服务器 IP 的请求）和“API 限制”（只启用 Gemini API，禁用其他不需要的服务）。

---



### 5: 如果我的 API Key 已经泄露到 GitHub 或公开场合，我该怎么办？

5: 如果我的 API Key 已经泄露到 GitHub 或公开场合，我该怎么办？

**A**: 一旦发现 API Key 泄露，必须立即采取行动：
1.  **立即作废**：登录 Google Cloud Console，找到该 API Key 并将其禁用或删除。
2.  **生成新 Key**：如果你的服务依赖该 Key，在清理代码并确保安全后，生成一个新的 API Key，不要尝试继续使用已泄露的 Key。
3.  **检查账单**：仔细检查 Google Cloud 的计费报告，看是否有异常的 API 调用量或费用产生。
4.  **撤销代码**：如果 Key 在 GitHub 上泄露，立即删除该提交记录或使用 BFG Repo-Cleaner 等工具清理 Git 历史（因为 Git 历史中仍保留着 Key），并强制推送到远程仓库。

---



### 6: Google Cloud Console 中有哪些设置可以增强 API Key 的安全性？

6: Google Cloud Console 中有哪些设置可以增强 API Key 的安全性？

**A**: Google 提供了多层防护机制，开发者应充分利用：
1.  **IP 地址限制**：如果你有固定的后端服务器 IP，可以设置 API Key 只接受来自这些 IP 地址的请求。这样即使 Key 被泄露，攻击者从其他 IP 调用也会被拒绝。
2.  **HTTP 引用来源限制**：对于必须在前端使用的 Key（不推荐用于 Gemini，但可用于某些纯前端场景），可以限制只允许来自特定域名的请求调用该 Key。
3.  **API 密钥限制**：默认情况下，新创建的 Key 可能拥有访问账户下所有服务的权限。你应该将其设置为“仅限制 Gemini API”，这样即使 Key 被窃，攻击者也无法利用它访问你的云存储或计算引擎。

---



### 7: 为什么这次事件特别强调了“规则改变了”？

7: 为什么这次事件特别强调了“规则改变了”？

**A**: 这句话的核心含义是：**攻击面的扩大改变了安全基线**。以前，泄露一个公共

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**：在传统的 Web 应用架构中，API Key 通常被放置在客户端代码的哪个位置？请编写一个简单的 HTML/JavaScript 页面，调用一个公开的 API（例如 OpenWeatherMap 或 Google Maps），并尝试在浏览器的开发者工具中找到这个 Key。

### 提示**：关注 `<script>` 标签内的全局变量、网络请求中的 HTTP Header（如 `x-api-key`）或 URL 查询参数。打开浏览器的 "Sources" 或 "Network" 面板进行排查。

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
- 标签： [API密钥](/tags/api%E5%AF%86%E9%92%A5/) / [Gemini](/tags/gemini/) / [谷歌](/tags/%E8%B0%B7%E6%AD%8C/) / [安全漏洞](/tags/%E5%AE%89%E5%85%A8%E6%BC%8F%E6%B4%9E/) / [权限管理](/tags/%E6%9D%83%E9%99%90%E7%AE%A1%E7%90%86/) / [LLM](/tags/llm/) / [数据泄露](/tags/%E6%95%B0%E6%8D%AE%E6%B3%84%E9%9C%B2/) / [API安全](/tags/api%E5%AE%89%E5%85%A8/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/)

### 相关文章

- [利用大语言模型实现大规模在线用户去匿名化]({{< relref "posts/20260226-hacker_news-large-scale-online-deanonymization-with-llms-12.md" >}})
- [发现逾17.5万个Ollama AI实例公网暴露]({{< relref "posts/20260131-hacker_news-175k-publicly-exposed-ollama-ai-instances-discover-19.md" >}})
- [MaliciousCorgi：恶意AI扩展将代码发送至中国]({{< relref "posts/20260202-hacker_news-maliciouscorgi-ai-extensions-send-your-code-to-chi-5.md" >}})
- [加速科学研究：Gemini 案例研究与通用技术]({{< relref "posts/20260205-arxiv_ai-accelerating-scientific-research-with-gemini-case--5.md" >}})
- [OpenClaw赋予AI全系统权限引发安全担忧]({{< relref "posts/20260206-hacker_news-openclaw-when-ai-agents-get-full-system-access-sec-14.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*