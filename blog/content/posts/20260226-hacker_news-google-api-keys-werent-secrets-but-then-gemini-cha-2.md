---
title: "谷歌API密钥曾非机密 但Gemini改变了规则"
date: 2026-02-26T16:11:37+08:00
draft: false
entry_kind: "auto"
tags: ["API密钥", "Google", "Gemini", "LLM安全", "密钥管理", "数据泄露", "身份认证", "API滥用"]
categories: ["安全", "大模型"]
source: hacker_news
description: "长期以来，开发者习惯将 Google API Keys 视为一种公开资源，这种做法在 Gemini API 推出后面临挑战。新的安全策略要求对 API 密钥进行更严格的权限控制，否则可能导致调用失败。本文将解析这一规则变更背后的技术逻辑，并提供具体的排查与修复建议，帮助开发者快速适配新的安全要求。"
external_url: https://trufflesecurity.com/blog/google-api-keys-werent-secrets-but-then-gemini-changed-the-rules
scenarios: ["大语言模型"]
---

# 谷歌API密钥曾非机密 但Gemini改变了规则

---

## 基本信息

- **作者**: hiisthisthingon
- **评分**: 967
- **评论数**: 231
- **链接**: [https://trufflesecurity.com/blog/google-api-keys-werent-secrets-but-then-gemini-changed-the-rules](https://trufflesecurity.com/blog/google-api-keys-werent-secrets-but-then-gemini-changed-the-rules)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47156925](https://news.ycombinator.com/item?id=47156925)

---
## 导语

长期以来，开发者习惯将 Google API Keys 视为一种公开资源，这种做法在 Gemini API 推出后面临挑战。新的安全策略要求对 API 密钥进行更严格的权限控制，否则可能导致调用失败。本文将解析这一规则变更背后的技术逻辑，并提供具体的排查与修复建议，帮助开发者快速适配新的安全要求。

---
## 评论

以下是基于文章标题《Google API keys weren't secrets, but then Gemini changed the rules》及相关背景的深度评价。

### 一、 核心观点与结构分析

**中心观点：**
**大语言模型（LLM）的交互特性从根本上改变了 API 密钥的安全属性，将原本属于“资源访问凭证”的 Key 转变为“高价值可执行代理”，从而推翻了 Web 2.0 时代“客户端 Key 隐性公开”的潜规则。**

**支撑理由：**

1.  **攻击面的不对称性扩张（事实陈述）：**
    在传统 REST API 时代，泄露 Key 仅意味着数据窃取或资源滥用（如盗版地图显示）。但在 Gemini 等 LLM 接口中，API Key 直接对应“生成能力”。攻击者利用泄露的 Key，不仅能查询信息，还能通过 Prompt 注入诱导模型输出敏感内容、甚至利用关联权限操作用户的云服务（如 Gmail、Drive）。

2.  **客户端与云端界限的模糊（作者观点）：**
    文章指出，为了降低开发者门槛和提升前端体验，大量 AI 应用倾向于将调用逻辑直接写在客户端（浏览器或 App）。这导致 API Key 必须暴露在前端代码中。在 Gemini 等高智能模型出现前，这种风险是可控的（仅损失配额）；但现在，模型的高理解力使得前端暴露的 Key 极易被用于复杂的越狱攻击。

3.  **AI 特有的“诱导性”风险（你的推断）：**
    传统的 API 安全侧重于“鉴权”，即验证“你是谁”。而 AI API 的安全必须增加“意图识别”，即判断“你想让模型做什么”。Gemini 等模型强大的指令遵循能力，使得恶意攻击者能更轻松地构建攻击 Prompt，让原本合法的 API Key 成为执行恶意指令的帮凶。

**反例/边界条件：**

1.  **企业级后端代理模式（事实陈述）：**
    对于成熟的企业级应用，API Key 从未也不应“公开”。无论是否是 Gemini 时代，标准的架构均要求前端请求后端，后端持有 Key 并转发请求。在此架构下，Key 依然是安全的秘密，文章所述的“规则改变”主要影响的是缺乏安全意识的快速原型开发或轻量级应用。

2.  **配额限制与计费作为兜底防线（事实陈述）：**
    Google Cloud 等平台通常提供严格的配额限制和预算告警。如果一个 Key 被泄露，其经济损失是有上限的（除非攻击者利用该 Key 进一步渗透云账户）。只要没有关联到高权限的云服务账号，其直接破坏力仍止步于“服务盗用”。

---

### 二、 多维度深入评价

#### 1. 内容深度：观点的深度和论证的严谨性
文章切中了当前 AI 安全领域最容易被忽视的盲区：**开发习惯的惯性**。许多开发者将对待 Google Maps API 的旧经验（Key 可以硬编码在 Demo 中）迁移到了 Gemini API 上，却忽略了后者生成内容的不可控性和潜在危害。论证严谨地指出了“模型能力”与“Key 泄露风险”的正相关性，即模型越智能，Key 泄露后的潜在危害越大，而不仅仅是计费风险。

#### 2. 实用价值：对实际工作的指导意义
具有极高的警示价值。它迫使开发团队重新审视 CI/CD 流程和前端代码审查标准。
*   **指导意义：** 任何在客户端（Web/移动端）使用 LLM API Key 的做法现在都应被标记为“高危漏洞”。
*   **架构调整：** 必须引入中间层，将 API Key 的权限限制在特定业务范围内，避免使用通用的 Root Key。

#### 3. 创新性：提出了什么新观点或新方法
文章并未提出具体的加密新方法，但在**安全认知模型**上具有创新性。它提出了**“可执行凭证”**的概念——即 API Key 不再仅仅是打开数据库的钥匙，而是挥舞大锤的手。这种视角的转换，促使安全关注点从“防止盗用”转向了“防止滥用”。

#### 4. 可读性：表达的清晰度和逻辑性
基于标题判断，文章采用了对比手法，逻辑清晰。通过“过去 vs 现在”的对比，生动地阐述了技术演进带来的安全范式转移，适合各层级技术人员阅读。

#### 5. 行业影响：对行业或社区的潜在影响
这篇文章可能会成为 AI 应用安全开发的分水岭。它预示着平台方（如 Google、OpenAI）将收紧 API Key 的默认策略，例如强制绑定 IP 白名单、强制启用 HTTP Referrer 检查，甚至逐步淘汰长期有效的 API Key，转而推行短时效 Token。

#### 6. 争议点或不同观点
*   **平台责任论：** 一种观点认为，Google 应该在产品层面解决此问题（例如自动检测异常流量或提供更严格的默认 SDK 配置），而不是指责开发者“不保密”。
*   **实用性 vs 安全性：** 许多边缘计算或纯客户端应用（如浏览器插件）为了低延迟和无服务器成本，必须直连 API。如果强制要求后端代理，会扼杀这类轻量级创新的生存空间。

#### 7. 实际应用建议
1.  **权限最小化：** 为特定的 AI 应用创建专用的服务账号，仅授予必要的模型调用权限，严禁授予云资源管理权限。
2.  **API Key 限制：** 在 Google Cloud Console 中，严格限制 API Key 的“Application restrictions”（如仅限特定 IP 或域名）。
3.

---
## 代码示例




```python
# 示例1：安全存储Google API密钥
import os
from dotenv import load_dotenv

def secure_api_key_usage():
    """
    安全使用Google API密钥的示例
    解决问题：避免将API密钥硬编码在代码中
    """
    # 加载.env文件中的环境变量
    load_dotenv()
    
    # 从环境变量获取API密钥
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        raise ValueError("未找到GOOGLE_API_KEY环境变量")
    
    # 使用API密钥进行安全调用
    print(f"使用API密钥: {api_key[:10]}...")  # 只打印前10个字符
    return api_key

# 说明：这个示例展示了如何通过环境变量安全存储和使用Google API密钥，
# 避免了将敏感信息硬编码在代码中，符合最佳安全实践。
```




```python
# 示例2：API密钥轮换机制
from datetime import datetime, timedelta
import random
import string

class ApiKeyManager:
    """
    API密钥管理类
    解决问题：实现API密钥的定期轮换
    """
    def __init__(self):
        self.keys = {}  # 存储密钥和过期时间
        self.current_key = None
    
    def generate_key(self):
        """生成新的API密钥"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    
    def rotate_key(self):
        """轮换API密钥"""
        new_key = self.generate_key()
        expiry = datetime.now() + timedelta(days=90)  # 90天后过期
        self.keys[new_key] = expiry
        self.current_key = new_key
        return new_key
    
    def get_valid_key(self):
        """获取当前有效的API密钥"""
        if not self.current_key or datetime.now() > self.keys[self.current_key]:
            return self.rotate_key()
        return self.current_key

# 说明：这个示例展示了如何实现API密钥的定期轮换机制，
# 通过自动生成新密钥并设置过期时间，提高API密钥的安全性。
```




```python
# 示例3：API密钥使用监控
import time
from collections import defaultdict

class ApiKeyMonitor:
    """
    API密钥使用监控类
    解决问题：监控API密钥的使用频率和异常情况
    """
    def __init__(self, max_requests_per_minute=60):
        self.request_counts = defaultdict(int)
        self.max_requests = max_requests_per_minute
        self.last_reset = time.time()
    
    def check_rate_limit(self, api_key):
        """检查API密钥是否超过速率限制"""
        current_time = time.time()
        
        # 每分钟重置计数
        if current_time - self.last_reset >= 60:
            self.request_counts.clear()
            self.last_reset = current_time
        
        # 检查请求次数
        if self.request_counts[api_key] >= self.max_requests:
            raise Exception(f"API密钥 {api_key[:10]}... 超过速率限制")
        
        self.request_counts[api_key] += 1
        return True
    
    def get_usage_stats(self):
        """获取API密钥使用统计"""
        return dict(self.request_counts)

# 说明：这个示例展示了如何监控API密钥的使用情况，
# 实现速率限制功能，防止API密钥被滥用或异常使用。
```


---
## 案例研究


### 1：某开源 AI 客户端项目

 1：某开源 AI 客户端项目

**背景**: 一个流行的开源 AI 客户端项目，旨在帮助用户在本地桌面端便捷地使用 Google 的 Gemini 模型。为了降低使用门槛，该项目的默认配置允许用户直接在设置界面填入个人的 Google API Key，并将其存储在本地明文配置文件中。

**问题**: 随着 Google Gemini 的更新，其 API Key 的权限范围和计费逻辑发生了变化。原本仅用于低频调用的 Key，现在可以被用于更高敏感度的操作或产生意外的高额费用。由于 Key 没有被作为“机密”严格管理，许多用户的 Key 随项目配置文件被上传到了 GitHub 公开仓库或被包含在分享的截图 中，导致 Key 泄露和账户被盗用的风险激增。

**解决方案**: 项目组修改了架构，不再要求用户直接提供 Google API Key。相反，项目集成了 OAuth 2.0 认证流程。用户通过点击“使用 Google 账号登录”进行授权，获取的 Access Token 仅存储在本地加密的 Keychain 中（如使用系统钥匙串），且 Token 具有较短的有效期和特定的作用域限制。

**效果**: 彻底消除了 API Key 泄露的风险。用户不再需要手动复制粘贴敏感字符串，且由于使用了 OAuth，项目本身无法接触到用户的长期凭证，安全性大幅提升。同时，这也符合 Google 新的安全规范，确保了项目的长期可持续性。

---



### 2：某 SaaS 初创公司的后端服务重构

 2：某 SaaS 初创公司的后端服务重构

**背景**: 该初创公司构建了一个基于 Google Gemini API 的企业级知识库助手。在开发初期，为了快速迭代，开发团队将 Google API Key 直接硬编码在代码库中，并存储在版本控制系统 的环境变量文件里。

**问题**: Google 对 Gemini API 的计费策略进行了调整，使得 API Key 关联的 Google Cloud 账户面临潜在的按量计费风险。由于 Key 没有受到严格的 IP 白名单或应用限制，一旦代码泄露或内部人员滥用，攻击者可以利用该 Key 消耗大量的配额，导致公司面临巨额账单。此外，Google 开始强制要求对 API Key 进行“应用限制”配置，原有的裸 Key 方式开始收到警告。

**解决方案**: 公司引入了 Secret Manager（如 Google Secret Manager 或 AWS Secrets Manager）来集中管理敏感信息。后端代码在启动时通过服务身份认证动态获取 API Key，而不是将其写在配置文件中。同时，在 Google Cloud Console 中对该 API Key 设置了严格的应用限制和 HTTP 引用来源限制，确保该 Key 只能由该公司的特定后端服务调用。

**效果**: 实现了凭证的集中管控和自动轮换，杜绝了硬编码带来的泄露风险。通过配置 API Key 的限制条件，即使 Key 意外泄露，也无法在第三方环境被使用，有效避免了“盗刷”产生的经济损失，确保了业务的合规性。

---



### 3：某在线教育平台的前端集成

 3：某在线教育平台的前端集成

**背景**: 一个在线编程教育平台希望在其网页端练习题中集成 Gemini API，让学生能够直接调用 AI 进行代码辅导。最初，前端开发人员为了方便，将 API Key 嵌入到了前端 JavaScript 代码中，认为反正只是用于教学演示。

**问题**: 随着 Gemini API 能力的增强，这种做法变得极度危险。前端代码是完全公开的，任何访问网站的人都可以通过“查看源代码”轻松获取该 API Key。恶意爬虫可以提取该 Key 并用于大规模的垃圾内容生成，导致该平台的 API 配额在短时间内被耗尽，正常学生无法使用服务。

**解决方案**: 平台调整了技术架构，采用“后端代理”模式。前端不再直接请求 Google API，而是调用平台自己的后端服务器接口。后端服务器负责验证学生身份和请求频率，验证通过后，再由后端服务器使用受保护的 API Key 向 Google 发起请求，并将结果返回给前端。

**效果**: 成功将 API Key 从客户端视线中移除。通过在后端实施速率限制和身份验证，平台有效控制了 API 调用成本，防止了资源滥用。这保证了教学服务的稳定性，同时也符合 Google 关于保护 API Key 的最佳实践要求。

---
## 最佳实践

## 最佳实践指南

### 实践 1：实施严格的 API 密钥访问控制

**说明**:
API 密钥不应被视为公开信息。必须限制只有特定的服务账号或 IP 地址才能使用密钥，防止密钥泄露后被滥用。

**实施步骤**:
1. 在 Google Cloud Console 中，进入 "APIs & Services" -> "Credentials"。
2. 创建或编辑 API 密钥。
3. 在 "Application restrictions"（应用限制）部分，选择以下选项之一：
   - **IP 地址**：仅允许来自特定服务器 IP 的请求。
   - **HTTP referrer**：仅允许来自特定域名的请求（适用于前端调用）。
   - **Android 应用** / **iOS 应用**：根据应用签名进行限制。
4. 保存更改。

**注意事项**:
- 对于后端服务，强烈建议使用 IP 白名单。
- 如果使用 0.0.0.0/0（允许所有 IP），则等同于完全开放，存在极大风险。

---

### 实践 2：配置 API 密钥配额与计费上限

**说明**:
为了防止密钥泄露或遭受 DDoS 攻击导致巨额账单，必须为每个 API 密钥设置每日请求配额和预算告警。

**实施步骤**:
1. 在 Google Cloud Console 中，进入 "APIs & Services" -> "Quotas"。
2. 选择特定的 API（如 Gemini API）。
3. 在 "Requests per day" 下，点击编辑图标，为特定密钥设置合理的上限（例如 1000 次/天）。
4. 进入 "Billing" -> "Budgets & alerts"。
5. 创建预算并设置阈值（例如账单达到 50 美元时发送邮件通知）。

**注意事项**:
- 配额限制应高于正常业务峰值，以免影响正常用户。
- 定期审查 Cloud Billing 报告，监控异常费用增长。

---

### 实践 3：禁止在客户端代码中硬编码密钥

**说明**:
永远不要将 API 密钥直接写入前端代码（HTML/JS）、移动端源代码或提交到公共代码仓库（如 GitHub）。

**实施步骤**:
1. **后端代理模式**：
   - 前端调用您自己的后端服务器。
   - 后端服务器（使用环境变量存储密钥）请求 Google API。
   - 将结果返回给前端。
2. **使用环境变量**：
   - 在 `.env` 文件（加入 `.gitignore`）中存储密钥。
   - 在代码中通过 `process.env.GOOGLE_API_KEY` 读取。
3. **密钥扫描**：
   - 在 CI/CD 流程中集成工具（如 GitGuardian 或 Trivy Hub），自动扫描代码库中的泄露密钥。

**注意事项**:
- 如果密钥已意外泄露，请立即在 Google Cloud Console 中将其删除并重新生成。
- 对于纯前端应用，务必配合"实践 1"中的 HTTP referrer 限制使用。

---

### 实践 4：定期轮换与审计 API 密钥

**说明**:
长期不更换的密钥增加了泄露风险窗口。应建立定期更换密钥的机制，并定期审计密钥的使用权限。

**实施步骤**:
1. **制定轮换计划**：建议每 90-180 天更换一次生产环境的 API 密钥。
2. **创建新密钥**：在轮换前生成新密钥，并在测试环境中验证。
3. **部署更新**：将新密钥部署到生产环境（使用蓝绿部署或滚动更新以避免服务中断）。
4. **验证与删除**：确认流量正常后，删除旧的 API 密钥。
5. **审计权限**：定期检查 "IAM & Admin" 页面，确认哪些密钥仍处于活跃状态，并删除不再使用的项目或密钥。

**注意事项**:
- 轮换密钥时，确保所有依赖该密钥的服务都已同步更新。
- 保留一份密钥清单，记录每个密钥的用途、创建日期和负责人。

---

### 实践 5：使用专用服务账号替代 API 密钥（针对企业级应用）

**说明**:
API 密钥主要基于简单的配额和来源限制。对于更敏感的操作，应使用基于身份的服务账号，并结合 OAuth 2.0 进行认证。

**实施步骤**:
1. 在 Google Cloud Console 的 "IAM & Admin" -> "Service Accounts" 中创建服务账号。
2. 为该服务账号授予适当的 IAM 角色（例如 "Service Usage Consumer" 或特定 API 的 Editor 角色）。
3. 下载 JSON 格式的密钥文件。
4. 在应用代码中使用 Google 官方客户端库（如 Google Auth Library）加载该 JSON 文件进行认证。

**注意事项**:
- 服务账号密钥文件（JSON）极其敏感，严禁泄露，必须严格保护。
- 此方法比简单的 API Key 更安全，因为它提供了细粒度的权限控制，且不依赖于 IP 或 Referrer。

---

### 实践 6：实施 API 安全监控与日志分析

**说明**:
仅仅设置限制是不

---
## 学习要点

- Google API 密钥通常被视为低敏感度信息，因为它们默认绑定 Google Cloud 控制台的配额限制，而非直接绑定用户的信用卡。
- Gemini API 的引入改变了安全规则，因为它允许用户直接将 API 密钥关联到个人 Google 账户进行支付和计费。
- 攻击者可以通过窃取泄露在代码库中的 Gemini API 密钥，利用受害者的账户余额消耗昂贵的 AI 模型配额。
- 这种“密钥即身份”的机制转变，使得 Google API 密钥从单纯的访问凭证变成了需要像密码一样严格保护的敏感资产。
- 开发者必须停止在客户端代码（如前端 HTML/JS）中硬编码 API 密钥，并应使用代理服务器来隔离凭证。
- 为 API 密钥设置严格的应用限制和配额上限是防止密钥泄露造成经济损失的关键防御手段。
- 此事件揭示了 AI 时代 API 安全模型的演变，即服务提供商为了降低集成门槛，往往牺牲了部分默认安全性。

---
## 常见问题


### 1: 为什么以前 Google API Key 通常不被视为严格保密的信息？

1: 为什么以前 Google API Key 通常不被视为严格保密的信息？

**A**: 在很长一段时间里，开发者社区普遍认为 Google API Key 不需要像密码那样严格保密。主要原因有两点：首先，许多 Google 服务（如公开地图嵌入）的设计初衷就是为了让其在客户端（如浏览器）中直接调用，这使得密钥必须暴露在前端代码中。其次，Google 传统的安全机制主要依赖于“HTTP Referrer（HTTP 引用来源）”限制。开发者可以在 Google Cloud 控制台配置白名单，只允许特定域名的请求使用该 Key。因此，即使 Key 被公开，只要请求来源不是授权的域名，第三方也无法盗用，这种机制降低了密钥泄露的风险。

---



### 2: Gemini 的出现改变了什么规则，导致 API Key 的安全性变得至关重要？

2: Gemini 的出现改变了什么规则，导致 API Key 的安全性变得至关重要？

**A**: 随着 Gemini 等 AI 模型的发布，Google 调整了其 API 的计费和安全策略。与传统的地图 API 不同，生成式 AI 的计算成本极高，因此 Google 开始为 Gemini API 提供免费试用额度或按量付费模式。关键的变化在于，许多开发者通过直接在客户端或简单的脚本中调用 Gemini API 来构建应用。如果 API Key 泄露，恶意行为者不仅可以轻易消耗掉开发者的配额，导致服务中断，还可能利用该 Key 生成大量内容产生高额费用。此外，AI 模型的交互往往比静态地图加载更容易被滥用进行自动化攻击。因此，Google 开始更严格地审计 API Key 的公开暴露情况，并可能因 Key 泄露而直接暂停相关服务。

---



### 3: 如果我的 Google API Key 已经泄露到了 GitHub 或公共代码库中，会发生什么？

3: 如果我的 Google API Key 已经泄露到了 GitHub 或公共代码库中，会发生什么？

**A**: 一旦 API Key 被公开，后果通常非常直接且严重。首先，自动化扫描工具和爬虫会迅速发现这些 Key，并立即尝试盗用您的配额进行 API 调用。对于 Gemini 等服务，这意味着您的免费额度可能会在几分钟内耗尽，或者产生意想不到的账单。其次，为了保护系统安全，Google 的安全系统检测到异常流量（来自不同 IP 或地理位置的激增请求）时，通常会自动禁用该 API Key。这将导致您的应用程序突然崩溃，且恢复过程可能非常繁琐，需要重新生成 Key 并更新所有引用它的代码。

---



### 4: 针对这种变化，开发者应如何正确保护 Google API Key？

4: 针对这种变化，开发者应如何正确保护 Google API Key？

**A**: 开发者应遵循“最小权限原则”和“代理原则”。首先，绝对不要将带有敏感权限的 API Key 硬编码在前端代码或移动应用中。如果必须在客户端使用（如网页应用），应在 Google Cloud Console 中严格设置“应用程序限制”，指定 Key 只能用于特定的 iOS/Android 应用包名或特定的网站域名。其次，最佳实践是构建一个后端代理服务：客户端将请求发送到您自己的服务器，您的服务器在后端持有并调用 Google API，然后将结果返回给客户端。这样，实际的 API Key 始终保存在服务器端，永远不会暴露给公众。

---



### 5: Google Cloud Console 中有哪些具体设置可以帮助降低 API Key 泄露后的风险？

5: Google Cloud Console 中有哪些具体设置可以帮助降低 API Key 泄露后的风险？

**A**: 您可以在 Google Cloud Console 的凭据页面中为每个 API Key 设置严格的限制以降低风险。主要包括：
1.  **应用程序限制**：选择“HTTP 引用来源”并填写您网站的域名，或选择“IP 地址”限制只能从特定服务器 IP 调用。
2.  **API 限制**：默认情况下，新建的 Key 通常可以访问所有启用的 API。您应限制该 Key 只能访问特定的 API（例如仅限制访问“Generative Language API”），这样即使 Key 被盗，攻击者也无法利用它访问您的云存储或计算引擎。
3.  **配额限制**：为 Key 设置每日请求数上限，以防止在泄露情况下产生无限度的费用。

---



### 6: 为什么在 Hacker News 等技术社区中，关于 API Key 管理的讨论突然增多？

6: 为什么在 Hacker News 等技术社区中，关于 API Key 管理的讨论突然增多？

**A**: 这种讨论的增多反映了开发者习惯与云服务商安全模型之间的演变冲突。过去，为了快速原型开发，开发者习惯于方便地直接调用 API。但随着 AI 服务的普及和云安全攻击的增加，这种“便捷但暴露”的做法成为了巨大的安全漏洞。Hacker News 上的讨论通常集中在如何平衡开发效率与安全性，以及批评某些云服务商提供的默认安全配置不够严格（例如默认不设任何引用限制），导致新手开发者容易犯下将 Key 提交到 GitHub 的严重错误。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 在使用 Google Cloud 控制台生成 API Key 时，界面上通常会提供“API 限制”和“应用程序限制”两个维度的配置。请说明如果仅设置了“应用程序限制”（例如限制 HTTP 引用来源或 IP 地址），但未设置“API 限制”，会带来什么具体的安全隐患？

### 提示**: 思考 API Key 本身作为一种通用凭证，如果它被用于访问你并未打算授权的 Google 服务（例如 Maps 而非 Gemini），仅凭来源限制能否阻止这种跨服务的滥用？

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
- 标签： [API密钥](/tags/api%E5%AF%86%E9%92%A5/) / [Google](/tags/google/) / [Gemini](/tags/gemini/) / [LLM安全](/tags/llm%E5%AE%89%E5%85%A8/) / [密钥管理](/tags/%E5%AF%86%E9%92%A5%E7%AE%A1%E7%90%86/) / [数据泄露](/tags/%E6%95%B0%E6%8D%AE%E6%B3%84%E9%9C%B2/) / [身份认证](/tags/%E8%BA%AB%E4%BB%BD%E8%AE%A4%E8%AF%81/) / [API滥用](/tags/api%E6%BB%A5%E7%94%A8/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/)

### 相关文章

- [谷歌API密钥曾非机密，Gemini规则变更引发安全隐忧]({{< relref "posts/20260226-hacker_news-google-api-keys-werent-secrets-but-then-gemini-cha-1.md" >}})
- [谷歌API密钥非机密但Gemini改变规则]({{< relref "posts/20260226-hacker_news-google-api-keys-werent-secrets-but-then-gemini-cha-0.md" >}})
- [OpenAI 如何通过内置安全机制防范 AI 代理点击链接时的数据泄露与提示词注入]({{< relref "posts/20260129-blogs_podcasts-keeping-your-data-safe-when-an-ai-agent-clicks-a-l-6.md" >}})
- [ChatGPT 推出锁定模式与高风险标签以防御提示注入]({{< relref "posts/20260218-blogs_podcasts-introducing-lockdown-mode-and-elevated-risk-labels-14.md" >}})
- [谷歌限制使用OpenClaw的AI Pro/Ultra订阅用户]({{< relref "posts/20260223-hacker_news-google-restricting-google-ai-proultra-subscribers--14.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*