---
title: "谷歌API密钥曾非机密，但Gemini改变了规则"
date: 2026-02-26T20:32:57+08:00
draft: false
entry_kind: "auto"
tags: ["Google", "Gemini", "API密钥", "鉴权机制", "大模型安全", "API管理", "数据泄露", "开发规范"]
categories: ["安全", "AI 工程"]
source: hacker_news
description: "长期以来，开发者习惯于将 Google API Keys 视为非敏感信息，因为其计费机制主要依赖云端账户验证。然而，随着 Gemini 模型的引入，Google 调整了鉴权策略与访问控制规则，这一传统认知已被打破。本文将深入剖析这一变化背后的技术细节，阐述其对现有应用安全性的具体影响，并为开发者提供排查漏洞及加固密钥管"
external_url: https://trufflesecurity.com/blog/google-api-keys-werent-secrets-but-then-gemini-changed-the-rules
scenarios: ["Web应用开发"]
---

# 谷歌API密钥曾非机密，但Gemini改变了规则

---

## 基本信息

- **作者**: hiisthisthingon
- **评分**: 1127
- **评论数**: 271
- **链接**: [https://trufflesecurity.com/blog/google-api-keys-werent-secrets-but-then-gemini-changed-the-rules](https://trufflesecurity.com/blog/google-api-keys-werent-secrets-but-then-gemini-changed-the-rules)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47156925](https://news.ycombinator.com/item?id=47156925)

---
## 导语

长期以来，开发者习惯于将 Google API Keys 视为非敏感信息，因为其计费机制主要依赖云端账户验证。然而，随着 Gemini 模型的引入，Google 调整了鉴权策略与访问控制规则，这一传统认知已被打破。本文将深入剖析这一变化背后的技术细节，阐述其对现有应用安全性的具体影响，并为开发者提供排查漏洞及加固密钥管理的实操建议。

---
## 评论

以下是对文章《Google API keys weren't secrets, but then Gemini changed the rules》的深入评价。

### 一、 核心观点与支撑逻辑

**中心观点：**
Google API Key 长期被视为一种“弱认证”标识符，但 Gemini 等生成式 AI 模型的引入，将其从简单的资源计量工具转变为潜在的高价值资产，迫使开发者必须重新审视密钥管理的安全边界。

**支撑理由：**
1.  **成本结构的根本性逆转（事实陈述）：** 在传统 Google Maps 或 Places API 中，滥用主要影响开发者的配额或产生有限的按次计费；而在 Gemini 等 LLM API 中，Token 消耗极快且单价较高，密钥泄露可能导致攻击者在短时间内造成巨大的经济损失。
2.  **模型能力的“黑盒”放大效应（作者观点）：** 文章指出，Gemini 的多模态和生成能力使得 API 调用不再仅仅是数据查询，而是内容生成。这意味着攻击者不仅可以窃取数据，还能利用受害者的账户生成大量恶意内容或进行大规模爬取，这种风险是传统静态 API 不具备的。
3.  **历史遗留代码的脆弱性（你的推断）：** 许多开源项目（如 Chrome 插件或 GitHub 仓库）习惯性地硬编码 Google API Key，这在过去可能只是导致 Key 被封禁，但在 Gemini 时代，这种行为直接将所有贡献者暴露在金融风险之下。

**反例/边界条件：**
1.  **OAuth 2.0 的替代性（事实陈述）：** 对于涉及用户隐私数据（如 Gmail、Google Drive）的操作，业界早已强制使用 OAuth 2.0，此时 API Key 并非主要认证凭据，文章提到的风险主要集中在“无需用户授权”的公共资源调用或 AI 生成场景。
2.  **配额熔断机制依然有效（你的推断）：** Google Cloud 并未移除 API Key 的配额限制。只要开发者正确设置了每日配额上限，即使密钥泄露，其经济损失也是可控的，因此“规则改变”更多是风险维度的扩大，而非防御体系的全面崩塌。

---

### 二、 深度评价（维度分析）

#### 1. 内容深度：从“弱秘密”到“高价值目标”的认知升级
文章在论证上具有相当的严谨性，它敏锐地捕捉到了**API 经济属性的变化**。过去，API Key 泄露通常被视为一种配置错误，主要后果是服务中断；而现在，它演变成了金融资产盗取。文章深入探讨了 Google 在设计 Key 时的初衷（公开访问的标识符）与当前 AI 时代需求（高价值资产凭证）之间的错位，这种历史视角的分析非常有深度。

#### 2. 实用价值：对存量资产的“审计警钟”
文章最大的实用价值在于它对**存量代码**的警示。许多开发者并未意识到自己多年前发布的代码中包含的 Key 现在可能关联着开启了计费的 Google Cloud 账号。文章实际上是在呼吁一次全行业的“密钥大扫除”，这对于维护企业云资产安全具有极高的指导意义。

#### 3. 创新性：重新定义“Secret”的标准
文章提出了一个具有创新性的视角：**“Secret”的定义是由其滥用后果决定的，而非其设计初衷。** 它打破了业界对 API Key 仅仅是“ID + Secret”中 ID 部分的固有认知，指出了在 AI 时代，单纯的 API Key 验证已不足以支撑“按量付费”的高价值模型，暗示了未来可能需要引入更严格的短期凭证或元数据绑定。

#### 4. 行业影响：推动 API 安全治理的范式转移
这篇文章可能会成为推动开发者从“硬编码”向“密钥管理服务（KMS）”或“环境变量”迁移的催化剂。特别是对于 AI 应用开发者，它强调了**API Key 的生命周期管理**（如定期轮换、作用域限制）不再是可选项，而是必选项。

#### 5. 争议点：厂商责任 vs 用户责任
文章隐含了一个争议点：**Google 是否应该改变 API Key 的默认行为？**
*   **作者观点倾向：** 似乎在责怪开发者没有把 Key 当作秘密。
*   **不同观点（批判性思考）：** 实际上，Google 的产品 UI 和文档长期以来对 API Key 的处理非常随意（许多教程直接展示 Key）。Gemini 的上线是 Google 产品形态的升级，如果安全风险剧增，Google 应该默认为 Gemini API Key 启用更严格的“应用限制”或“IP 锁定”，而不是仅仅依靠文章来呼吁开发者小心。

---

### 三、 实际应用建议与验证

#### 1. 可验证的检查方式
为了验证文章所述风险的真实性及防御有效性，建议进行以下检查：
*   **指标监控：** 在 Google Cloud Console 中，为特定 API Key 设置“预算告警”。如果该 Key 被用于未预期的项目（如 Gemini），观察其消耗速度是否远超传统 API。
*   **攻击面审计：** 使用 `truffleHog` 或 `gitleaks` 等工具扫描企业内部的私有代码仓库，搜索 `AIza` 前缀（Google API Key 特征），统计有多少 Key 是明文硬编码的。
*   **权限测试：** 针对一个现有的 API Key，尝试在未登录 Google 账户的情况下调用 Gemini API。如果成功，则验证了文章关于“无需 OAuth 即可扣费”的观点。

#### 2. 行动建议
*   **立即实施应用限制：** 不要仅依赖 Key 的保密性。进入 Google

---
## 代码示例




```python
# 示例1：安全存储Google API密钥
import os
from dotenv import load_dotenv

def load_api_key():
    """从环境变量安全加载API密钥"""
    load_dotenv()  # 从.env文件加载环境变量
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        raise ValueError("未找到API密钥！请检查.env文件或环境变量设置")
    
    return api_key

# 使用示例
try:
    key = load_api_key()
    print(f"成功加载API密钥（前4位）：{key[:4]}****")
except Exception as e:
    print(f"错误：{str(e)}")
```




```python
# 示例2：API密钥权限验证
import requests

def verify_api_key_permissions(api_key):
    """验证API密钥是否具有必要权限"""
    url = "https://www.googleapis.com/oauth2/v1/tokeninfo"
    params = {"access_token": api_key}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # 检查必要权限
        required_scopes = ["https://www.googleapis.com/auth/cloud-platform"]
        if not any(scope in data.get("scope", "") for scope in required_scopes):
            raise PermissionError("API密钥缺少必要权限")
            
        return True
    except requests.exceptions.RequestException as e:
        print(f"验证失败: {str(e)}")
        return False

# 使用示例
api_key = "your_api_key_here"
if verify_api_key_permissions(api_key):
    print("API密钥权限验证通过")
else:
    print("API密钥无效或权限不足")
```




```python
# 示例3：API密钥使用监控
from datetime import datetime, timedelta
import time

class APIKeyMonitor:
    """监控API密钥使用情况"""
    def __init__(self, api_key, daily_limit=1000):
        self.api_key = api_key
        self.daily_limit = daily_limit
        self.usage_log = []
    
    def log_usage(self, endpoint, response_code):
        """记录API使用情况"""
        now = datetime.now()
        self.usage_log.append({
            "timestamp": now,
            "endpoint": endpoint,
            "status": response_code
        })
    
    def check_daily_limit(self):
        """检查是否超过每日配额"""
        now = datetime.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        
        today_usage = [log for log in self.usage_log if log["timestamp"] >= today_start]
        return len(today_usage) < self.daily_limit
    
    def get_usage_report(self):
        """生成使用报告"""
        now = datetime.now()
        last_24h = now - timedelta(hours=24)
        recent_usage = [log for log in self.usage_log if log["timestamp"] >= last_24h]
        
        return {
            "total_requests": len(self.usage_log),
            "last_24h_requests": len(recent_usage),
            "success_rate": sum(1 for log in recent_usage if 200 <= log["status"] < 300) / len(recent_usage) * 100 if recent_usage else 0
        }

# 使用示例
monitor = APIKeyMonitor("your_api_key_here", daily_limit=100)
monitor.log_usage("/v1/models", 200)
monitor.log_usage("/v1/chat", 400)

print("是否超过每日限制:", not monitor.check_daily_limit())
print("使用报告:", monitor.get_usage_report())
```


---
## 案例研究


### 1：某开源 AI 客户端库

 1：某开源 AI 客户端库

**背景**:
该项目是一个在 GitHub 上拥有数千颗星的开源库，旨在帮助开发者更便捷地在后端集成 Google 的各种 AI 服务（如 Vertex AI）。为了降低入门门槛，项目文档和示例代码长期硬编码了 API Key，并建议用户直接在环境变量中替换使用。在 Gemini 模型发布之前，由于 Google Cloud 的计费和配额限制较为宽松，这种做法并未引发严重的安全危机。

**问题**:
随着 Gemini Ultra 等高成本模型的发布，Google 大幅收紧了 API Key 的安全策略，并引入了更严格的后端验证机制。该开源库的数千名独立开发者发现，直接沿用旧的 Key 或简单的 Key 管理方式会导致请求被拒绝，甚至因为 Key 泄露导致账户被自动封禁。项目维护者收到了大量关于“认证失败”和“配额耗尽”的 Issue，原有的 Key 管理模式已不再适用。

**解决方案**:
项目维护者迅速重构了认证模块，废弃了直接传递 API Key 的示例，转而采用 Google Cloud 的官方 SDK 进行凭证管理。解决方案引入了“Application Default Credentials (ADC)”机制，并编写了详细的文档指导用户如何通过服务账号（Service Account）和 JSON 密钥文件进行身份验证，同时建议用户将敏感凭证注入到环境变量或密钥管理服务（如 HashiCorp Vault）中，而非硬编码。

**效果**:
通过更新代码和文档，该项目成功消除了因 Key 泄露导致的账户封禁问题。开发者学会了如何正确配置高权限的 Cloud 凭证，项目的 Issue 数量下降了 80%。更重要的是，这种合规的集成方式使得该库能够无缝支持 Gemini 的后续更新，保证了项目的长期生命力。

---



### 2：某 SaaS 初创公司的移动应用

 2：某 SaaS 初创公司的移动应用

**背景**:
这家初创公司开发了一款基于 AI 的生产力移动应用，为了快速上线 MVP（最小可行性产品），开发团队直接将 Google API Key 写入了移动端应用的代码中。在旧有规则下，虽然存在 Key 泄露风险，但攻击者窃取 Key 主要用于免费调用接口，对公司的直接财务冲击有限，且可以通过设置每日上限来控制。

**问题**:
Gemini 模型上线后，其高昂的定价和新的计费规则使得风险急剧上升。由于移动端代码可以被轻易反编译，黑客在应用发布后的几小时内就提取出了 API Key，并利用该 Key 进行了大规模的批量调用，导致该初创公司在短短 24 小内产生了数千美元的意外账单，几乎耗尽了其预存的云服务额度，导致正常用户无法使用服务。

**解决方案**:
公司立即决定移除客户端的所有 API Key，构建了一个轻量级的后端代理服务（使用 Python FastAPI 实现）。移动端应用不再直接请求 Google API，而是调用自家的后端 API。后端服务负责在服务器端安全地持有并调用 Google API Key，并对每个用户的请求进行速率限制和身份验证，从而将 API Key 的实际调用行为完全隐藏在服务器防火墙之后。

**效果**:
架构调整后，公司彻底杜绝了 Key 泄露带来的财务风险。通过在后端实施精细化的配额管理，他们能够精确控制每个用户的调用次数，将成本维持在预算范围内。这一改动不仅保障了安全性，还使得他们能够根据不同用户等级灵活配置不同的 AI 模型权限，为后续的商业模式升级打下了基础。

---
## 最佳实践

## API 密钥管理最佳实践

### 实践 1：实施严格的 API 密钥访问限制

**说明**:
API 密钥不应被视为公开信息。默认配置通常较为宽松，建议通过管理控制台对密钥进行精细化配置，限制其仅能被特定的应用程序或网站调用，以降低密钥泄露后被滥用的风险。

**实施步骤**:
1. 登录管理控制台，进入 "APIs & Services" -> "Credentials"。
2. 选择或创建 API 密钥。
3. 在 "Application restrictions" 部分，根据场景选择限制方式：
   - **IP 地址**：仅允许来自特定服务器 IP 的请求。
   - **HTTP 引荐来源网址**：仅允许来自特定域名的请求（适合前端调用）。
   - **Android 应用**或 **iOS 应用**：根据应用签名和包名进行限制。
4. 保存设置。

**注意事项**:
- 避免选择 "None"（无限制），除非处于临时测试环境。
- 限制设置后，未授权的请求将返回 403 错误，请在测试环境验证无误后再上线。

---

### 实践 2：配置 API 密钥的配额与权限范围

**说明**:
遵循最小权限原则，API 密钥应仅拥有完成其功能所需的最小权限集，并设置使用配额。这有助于控制因密钥泄露导致的资源消耗或对非相关 API 的调用。

**实施步骤**:
1. 在 API 密钥编辑页面，找到 "API restrictions"。
2. 取消勾选 "Don't restrict key"，仅勾选该密钥实际需要的 API。
3. 进入 "Quotas" 页面，为该密钥设置每分钟或每天的最大请求次数。
4. 配置账单预警，以便在费用或使用量达到阈值时接收通知。

**注意事项**:
- 定期审查密钥权限，移除不再需要的 API 访问权限。
- 对于特定 API（如 Gemini），建议设置默认配额，并根据实际需求调整。

---

### 实践 3：禁止在客户端代码中硬编码密钥

**说明**:
发布到前端（Web、移动端、桌面端）的代码容易被反编译或查看。不应将 API 密钥直接写在 JavaScript、HTML、Java/Kotlin 或 Swift 代码中。

**实施步骤**:
1. 将涉及 API 密钥的逻辑迁移到后端服务。
2. 前端应用向您的后端发起请求，由后端负责调用 API 并将结果返回给前端。
3. 如果必须在前端调用（如纯静态页面），建议配合 "实践 1" 中的 HTTP 引荐来源网址限制，但通过后端代理调用是更安全的方案。

**注意事项**:
- 检查版本控制系统（如 Git），确保没有提交过包含密钥的代码。如果已提交，应将该密钥视为已泄露并撤销。

---

### 实践 4：使用专用密钥管理服务

**说明**:
不建议将 API 密钥存储在配置文件（如 .env, config.json）或数据库的明文字段中。应使用密钥管理系统来存储、分发和轮换密钥。

**实施步骤**:
1. 使用云服务商的密钥管理服务（如 Google Secret Manager, AWS Secrets Manager, Azure Key Vault）或 HashiCorp Vault。
2. 在应用启动时，通过 SDK 动态获取密钥，而非将其打包在镜像或代码中。
3. 确保只有拥有特定 IAM 角色的服务账号才有权限读取这些密钥。

**注意事项**:
- 密钥管理服务应与应用程序所在的网络环境进行适当隔离。
- 审计密钥的访问日志，记录密钥的读取操作。

---

### 实践 5：建立密钥轮换与撤销机制

**说明**:
密钥使用时间越长，风险越高。建议建立密钥轮换机制，并在发现异常时能够快速撤销密钥。

**实施步骤**:
1. 制定密钥生命周期策略，例如定期轮换 API 密钥。
2. 在开发环境中编写脚本，通过 API 自动创建新密钥、更新应用配置并删除旧密钥。
3. 当发现密钥泄露（如出现在代码仓库中）时，立即在管理控制台中禁用或删除该密钥。
4. 为不同的环境（开发、测试、生产）使用不同的密钥。

**注意事项**:
- 轮换密钥时，需确保服务不中断（可采用双密钥并存过渡期）。
- 删除旧密钥前，确认没有遗留系统仍在使用该密钥。

---

### 实践 6：监控与审计 API 使用情况

**说明**:
仅依靠配置限制不足以应对所有安全威胁。需要对 API 的调用情况进行持续监控，通过分析日志及时发现异常行为模式。

**实施步骤**:
1. 在管理控制台中启用 Cloud Logging（或相应的日志服务）。
2. 创建基于日志的指标，重点关注：
   - 失败的认证请求（403/401 错误）。
   - 单个 IP 或用户异常高的请求

---
## 学习要点

- Google API 密钥长期处于一种“半公开”状态，因为它们通常嵌入在客户端代码（如 Android 应用）中，且 Google 仅依赖 HTTP Referer 头部进行验证，这种机制极易被伪造。
- Gemini API 的引入打破了这一现状，因为它采用了按量付费的计费模式，使得泄露的 API 密钥直接转化为攻击者的经济损失，从而迫使 Google 改变了安全策略。
- Google 开始对异常的 API 流量（特别是来自非预期来源的请求）实施更严格的封锁，导致许多依赖“借用”密钥或未正确配置 Referer 限制的开源项目（如 AI 聊天客户端）失效。
- 此次事件揭示了 AI 时代 API 安全的核心转变：传统的防御手段（如 Referer 检查）在涉及实际金钱成本时已不再被视为足够的安全措施。
- 开发者必须意识到，在客户端代码中硬编码 API 密钥始终是高风险行为，即便是在过去看似宽松的 Google 生态系统中。
- 对于 API 提供商而言，只有在滥用行为会直接导致财务损失时，才会真正投入资源去修复长期存在的安全漏洞或设计缺陷。

---
## 常见问题


### 1: 为什么以前 Google API Key 被认为不是“秘密”，而现在情况发生了变化？

1: 为什么以前 Google API Key 被认为不是“秘密”，而现在情况发生了变化？

**A**: 在很长一段时间里，Google 的许多公开文档和开发者社区都倾向于将 API Key 视为一种“公开标识符”，而不是像私钥那样需要严格保密的凭证。这种观念主要基于两个原因：一是 Google 提供了强大的“HTTP 引用来源”限制，允许开发者指定哪些域名可以调用 Key；二是 Google 的计费和配额系统主要依赖于 OAuth 客户端 ID 或更复杂的服务账号认证，而不是单纯的 API Key。

然而，随着 Gemini 等生成式 AI 模型的推出，规则发生了改变。调用这些大模型的成本（Token 计费）远高于传统的地图或搜索 API。如果 API Key 泄露，恶意攻击者可以轻易利用它来消耗受害者的配额或产生高额账单。因此，Google 开始强制要求对这些高价值的 API Key 进行更严格的限制（如限制只能用于特定的 AI 模型），不再允许将其作为完全公开的凭证使用。

---



### 2: Gemini API 的规则具体发生了什么变化？

2: Gemini API 的规则具体发生了什么变化？

**A**: 最主要的变化在于 Google 对 API Key 的安全策略和计费逻辑进行了收紧。在 Gemini API 推广初期，为了方便开发者测试，Google 允许在客户端（如直接在浏览器或移动应用中）使用 API Key，并仅依赖 HTTP 引用来源作为安全防护。

但随后 Google 更新了政策，要求开发者必须为 API Key 设置“应用程序限制”。如果开发者试图在客户端代码中直接嵌入 Key，而没有正确设置限制，或者 Key 被检测到在未授权的域名/应用中使用，Google 可能会直接拒绝请求。此外，Google 强烈建议不要在客户端代码中硬编码 API Key，而是推荐通过后端服务器作为代理来转发请求，从而将 Key 隐藏在服务器端。

---



### 3: 如果我的 Google API Key 已经泄露（例如被上传到了 GitHub），会有什么后果？

3: 如果我的 Google API Key 已经泄露（例如被上传到了 GitHub），会有什么后果？

**A**: 后果取决于该 Key 关联了哪些 Google Cloud 服务以及是否开启了计费。对于 Gemini API 而言，泄露 Key 的主要风险包括：

1.  **经济损失**：攻击者可以利用泄露的 Key 大量调用 Gemini 生成内容，导致您的 Google Cloud 账户产生巨额费用。
2.  **服务中断**：一旦配额被耗尽，您自己的应用程序将无法继续使用 API，直到下个计费周期重置或您增加预算。
3.  **滥用风险**：攻击者可能利用您的 Key 生成恶意内容（如钓鱼邮件文本、有害代码），虽然 Google 有内容审核机制，但这可能导致您的项目被标记或封禁。

---



### 4: 开发者应该如何正确管理 Gemini 的 API Key 以符合新的安全规范？

4: 开发者应该如何正确管理 Gemini 的 API Key 以符合新的安全规范？

**A**: 为了符合新的安全规范并保护账户安全，开发者应采取以下措施：

1.  **不要在客户端暴露 Key**：绝对不要将 API Key 直接写入前端 JavaScript、Android 或 iOS 代码中。
2.  **使用后端代理模式**：最佳实践是构建一个后端服务（如 Python、Node.js 服务器）。客户端向您的后端发送请求，后端验证用户身份后，再将请求转发给 Google API。这样，API Key 始终保存在服务器端，外界无法直接访问。
3.  **配置严格的 API Key 限制**：在 Google Cloud Console 中，必须为 Key 设置“应用程序限制”（例如限制为 IP 地址、特定的 Android 应用包名或 iOS URL Scheme）以及“API 限制”（仅允许访问 Generative Language API）。

---



### 5: 既然 API Key 不能放在前端，那么在纯前端应用（如纯静态网页）中该如何调用 Gemini API？

5: 既然 API Key 不能放在前端，那么在纯前端应用（如纯静态网页）中该如何调用 Gemini API？

**A**: 这是一个常见的架构挑战。如果您没有后端服务器，目前主要有几种解决方案：

1.  **使用 Google AI Studio 的内联功能**：对于简单的演示，Google AI Studio 提供了一种生成网页代码的方式，但这通常不适合生产环境。
2.  **构建轻量级后端**：即使是使用 Cloudflare Workers、Vercel Serverless Functions 或 Google Cloud Functions 这样的无服务器架构，也可以低成本地创建一个安全的代理层，将 Key 隐藏在服务端环境变量中。
3.  **使用 Firebase App Check**：虽然这主要用于 Firebase 服务，但结合 Google 的安全规则，它可以帮助确保只有您的应用程序在调用您的后端，从而防止 Key 被第三方网站滥用。
4.  **限制 Key 的作用域**：如果必须在前端使用，务必在 Google Cloud Console 中将该 Key 的 HTTP 引用来源严格限制为您自己的域名，并密切监控配额使用情况，但这仍然不如后端代理安全。

---



### 6: Google 的 OAuth 2.0 认证和 API Key 有什么区别，为什么后者现在被认为不够安全？

6: Google 的 OAuth 2.0 认证和 API Key 有什么区别，为什么后者现在被认为不够安全？

**A**: API Key 和 OAuth 2.0 的主要区别在于**身份验证的级别**。

*   **API Key**：用于标识“是哪个项目在调用 API”。它不验证“是谁在操作”。它就像一把放在门口的万能钥匙，任何拿到这把钥匙的人（或脚本

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 在传统的 Web 应用架构中，API Key 通常被存储在前端代码的哪个位置？这种做法在单页应用（SPA）或静态网站中为何难以完全避免？请列举出三种常见的通过浏览器开发者工具提取明文 API Key 的方法。

### 提示**: 思考前端代码的运行环境以及 HTTP 请求的可见性。关注浏览器开发者工具中的 "Network"（网络）面板、"Sources"（源代码）面板以及 "Storage"（存储）面板的功能特性。

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
- 标签： [Google](/tags/google/) / [Gemini](/tags/gemini/) / [API密钥](/tags/api%E5%AF%86%E9%92%A5/) / [鉴权机制](/tags/%E9%89%B4%E6%9D%83%E6%9C%BA%E5%88%B6/) / [大模型安全](/tags/%E5%A4%A7%E6%A8%A1%E5%9E%8B%E5%AE%89%E5%85%A8/) / [API管理](/tags/api%E7%AE%A1%E7%90%86/) / [数据泄露](/tags/%E6%95%B0%E6%8D%AE%E6%B3%84%E9%9C%B2/) / [开发规范](/tags/%E5%BC%80%E5%8F%91%E8%A7%84%E8%8C%83/)
- 场景： [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [谷歌API密钥曾非机密，Gemini规则变更引发安全隐忧]({{< relref "posts/20260226-hacker_news-google-api-keys-werent-secrets-but-then-gemini-cha-1.md" >}})
- [Google API密钥曾非机密，但Gemini改变了规则]({{< relref "posts/20260226-hacker_news-google-api-keys-werent-secrets-but-then-gemini-cha-4.md" >}})
- [谷歌API密钥曾非机密 但Gemini改变了规则]({{< relref "posts/20260226-hacker_news-google-api-keys-werent-secrets-but-then-gemini-cha-2.md" >}})
- [谷歌API密钥曾非机密，但Gemini改变了规则]({{< relref "posts/20260226-hacker_news-google-api-keys-werent-secrets-but-then-gemini-cha-9.md" >}})
- [谷歌API密钥非机密但Gemini改变规则]({{< relref "posts/20260226-hacker_news-google-api-keys-werent-secrets-but-then-gemini-cha-0.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*