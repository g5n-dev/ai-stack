---
title: "谷歌API密钥曾非机密，但Gemini改变了规则"
date: 2026-02-26T19:08:23+08:00
draft: false
entry_kind: "auto"
tags: ["API密钥", "Gemini", "谷歌", "安全漏洞", "LLM", "认证机制", "数据泄露", "API管理"]
categories: ["安全", "大模型"]
source: hacker_news
description: "长期以来，开发者习惯于将 Google API Keys 视为公开资源，因为其计费机制主要依赖调用方账户。然而，随着 Gemini API 的引入，Google 调整了授权规则，不再允许通过简单的 Header 传递密钥，这一变化直接影响了大量依赖客户端集成的应用。本文将深入解析这一政策转变背后的技术逻辑与安全考量，并"
external_url: https://trufflesecurity.com/blog/google-api-keys-werent-secrets-but-then-gemini-changed-the-rules
scenarios: ["大语言模型"]
---

# 谷歌API密钥曾非机密，但Gemini改变了规则

---

## 基本信息

- **作者**: hiisthisthingon
- **评分**: 1088
- **评论数**: 259
- **链接**: [https://trufflesecurity.com/blog/google-api-keys-werent-secrets-but-then-gemini-changed-the-rules](https://trufflesecurity.com/blog/google-api-keys-werent-secrets-but-then-gemini-changed-the-rules)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47156925](https://news.ycombinator.com/item?id=47156925)

---
## 导语

长期以来，开发者习惯于将 Google API Keys 视为公开资源，因为其计费机制主要依赖调用方账户。然而，随着 Gemini API 的引入，Google 调整了授权规则，不再允许通过简单的 Header 传递密钥，这一变化直接影响了大量依赖客户端集成的应用。本文将深入解析这一政策转变背后的技术逻辑与安全考量，并探讨开发者应如何调整现有的鉴权流程以适应新的环境。

---
## 评论

**中心观点**
文章的核心观点在于：随着 Gemini API 等新一代 AI 服务采用了基于“项目”而非单一静态密钥的计费与鉴权模式，传统的“代码即密钥”分发模式已不再适用，API Key 的属性已从单纯的“技术凭证”转变为一种需要严格全生命周期管理的“高价值资产”，行业必须摒弃将 API Key 视为可随意嵌入客户端代码的“非机密”旧习。

**支撑理由与边界分析**

**支撑理由：**

1.  **技术架构的范式转移（事实陈述）：** 过去，许多简单的 Google API（如 Maps 搜索）允许在客户端直接嵌入 Key，配合 HTTP Referer 限制即可防止盗用。然而，Gemini 等生成式 AI API 的核心成本在于 Token 的推理消耗，且其调用模式更为复杂。文章敏锐地指出了这一变化：AI 时代的高额、动态计费模式使得“客户端直连”的风险从“配额被盗用”升级为“直接的经济损失”。
2.  **安全边界的模糊化（作者观点）：** 文章强调了 AI 的交互特性使得传统的“Referer 限制”防御失效。在 Web 应用中，Referer 头可以被伪造或被隐私浏览器插件屏蔽，而在移动端或桌面应用中，API Key 往往被硬编码在二进制文件中，极易通过逆向工程提取。这论证了为何在 AI 时代，Key 必须被视为绝密。
3.  **身份与访问管理（IAM）的必要性（你的推断）：** 文章暗示了单一静态 Key 的局限性。现代云安全最佳实践是转向基于角色的短期凭证。虽然文章未深入展开 IAM 的技术细节，但其逻辑指向了必须引入后端代理机制来隔离用户与密钥，这是将 Key 从“公开分发的实体”转变为“后端受控资源”的关键一步。

**反例与边界条件：**

1.  **纯前端/无后端场景的困境（边界条件）：** 对于个人开发者、原型验证或完全静态的网站（如 GitHub Pages 上的 Demo），搭建独立的后端服务器来代理 API 请求会显著增加运维成本和复杂度。在这种低风险、低频次的场景下，API Key 仍可能被视为一种“不得不公开”的便利工具，只要配合严格的每日配额限制。
2.  **公开数据集的只读访问（反例）：** 如果 API 的用途仅限于读取公开的非计费数据（例如某些公共知识图谱查询），且服务提供方设置了零成本或极低的硬性配额上限，那么将 Key 暴露在前端依然是可行的。并非所有 API Key 都等同于 Gemini Key 那样的“直接提款卡”。

**维度评价**

1.  **内容深度：** 文章虽然指出了现象，但在技术原理的挖掘上略显不足。它更多是在陈述“规则变了”，而没有深入剖析 Google Cloud IAM（Identity and Access Management）中 Service Account 与 API Key 的底层权限差异。它未能详细解释为何 Google 不直接强制所有 Key 启用“应用限制”来从技术上解决这一问题，而是依赖开发者的自觉。
2.  **实用价值：** 具有极高的警醒价值。许多开发者仍停留在“只要不把数据库密码写死在前端就行”的旧思维中。文章明确指出了 Gemini Key 的特殊性，迫使开发者重新审视自己的代码仓库，防止因误提交代码而导致云账单被刷爆。
3.  **创新性：** 观点虽新颖但属于“行业痛点的滞后总结”。它并没有提出新的技术方案，而是对现有安全规范的一次“追认”。其创新之处在于将 AI 的经济属性（Token 成本）直接挂钩到了安全策略上，超越了单纯的数据泄露视角。
4.  **可读性：** 结构清晰，逻辑流畅。文章成功地将技术变更与商业风险联系起来，非技术背景的管理者也能理解为何“一把钥匙”不再能通开门锁。
5.  **行业影响：** 该文章反映了安全社区对 AI 应用层安全的焦虑。它可能会推动 CI/CD 流程中针对 API Key 扫描规则的升级（例如将 Gemini Key 列为高危敏感词），并促进“Backend-for-Frontend (BFF)”模式在 AI 应用开发中的普及。

**争议点与批判性思考**

文章存在一个潜在的**幸存者偏差**：它假设所有开发者都具备搭建后端的能力。对于“低代码”或“无代码”构建者，以及利用 Google Apps Script 或 Streamlit 等快速构建工具的用户，强制隐藏 Key 极大地提高了门槛。此外，文章过分强调了“Key 的保密性”，却忽略了**API 端自身的速率限制和异常检测**才是最后一道防线。即便 Key 泄露，如果云平台能智能识别异常流量（如突然的 DDoS 攻击）并自动熔断，风险也是可控的。单纯依靠“隐藏 Key”是防御纵深不足的表现。

**实际应用建议**

1.  **架构层面：** 严禁在前端（Web/Mobile）直接存储 Gemini 或其他高价值 LLM 的 API Key。必须建立轻量级后端（BFF 层），前端调用后端，后端使用环境变量中的 Key 向 Google 发起请求。
2.  **密钥管理：** 使用 Google Cloud Console 的“API Keys”页面，手动为每个 Key 设置严格的应用限制和 API 限制。不要使用通配符。
3.  **监控与审计：** 开启 Cloud Billing Alerts，设置异常消费告警（例如单日超过 $5 立即邮件通知）。

---
## 代码示例




```python
# 示例1：从环境变量安全加载API密钥
import os
from dotenv import load_dotenv

def load_api_key():
    """从.env文件加载API密钥，避免硬编码"""
    load_dotenv()  # 加载.env文件中的环境变量
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        raise ValueError("未找到GOOGLE_API_KEY环境变量")
    return api_key

# 使用示例
try:
    key = load_api_key()
    print(f"成功加载API密钥（前4位）: {key[:4]}****")
except Exception as e:
    print(f"错误: {e}")
```




```python
# 示例2：验证API密钥有效性
import requests

def validate_gemini_key(api_key):
    """验证Google Gemini API密钥是否有效"""
    url = "https://generativelanguage.googleapis.com/v1beta/models"
    headers = {"x-goog-api-key": api_key}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return True
        elif response.status_code == 403:
            print("API密钥无效或权限不足")
            return False
        else:
            print(f"验证失败，状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"请求错误: {e}")
        return False

# 使用示例
api_key = "YOUR_API_KEY_HERE"  # 替换为实际密钥
if validate_gemini_key(api_key):
    print("API密钥有效")
else:
    print("API密钥无效")
```




```python
# 示例3：API密钥轮换机制
import json
from datetime import datetime, timedelta

class ApiKeyRotator:
    """API密钥轮换管理器"""
    def __init__(self, key_file="api_keys.json"):
        self.key_file = key_file
        self.keys = self._load_keys()
    
    def _load_keys(self):
        """从JSON文件加载API密钥"""
        try:
            with open(self.key_file) as f:
                return json.load(f)
        except FileNotFoundError:
            return {"keys": []}
    
    def add_key(self, api_key, expiry_days=30):
        """添加新密钥并设置过期时间"""
        expiry = datetime.now() + timedelta(days=expiry_days)
        self.keys["keys"].append({
            "key": api_key,
            "expiry": expiry.isoformat(),
            "active": True
        })
        self._save_keys()
    
    def get_active_key(self):
        """获取当前有效的API密钥"""
        now = datetime.now()
        for key in self.keys["keys"]:
            expiry = datetime.fromisoformat(key["expiry"])
            if key["active"] and expiry > now:
                return key["key"]
        raise ValueError("没有可用的有效API密钥")
    
    def _save_keys(self):
        """保存密钥到文件"""
        with open(self.key_file, "w") as f:
            json.dump(self.keys, f, indent=2)

# 使用示例
rotator = ApiKeyRotator()
rotator.add_key("NEW_API_KEY", expiry_days=30)  # 添加新密钥
try:
    current_key = rotator.get_active_key()
    print(f"当前有效密钥: {current_key[:4]}****")
except ValueError as e:
    print(e)
```


---
## 案例研究


### 1：某知名开源开发者工具项目

 1：某知名开源开发者工具项目

**背景**: 该项目是一款面向开发者的桌面客户端工具，集成了 Google Maps API 以提供地理位置可视化功能。为了方便用户直接使用，项目在早期的文档和代码中默认内置了公开的 API Key，这在当时是许多开源项目的通用做法，因为 Google 的免费额度足够覆盖此类非商业或轻量级使用的成本。

**问题**: 随着 Google Gemini API 的更新以及安全策略的收紧，Google 开始严查未受保护的 API Key。该项目的默认 Key 被系统自动检测到并标记为“不安全”，导致 Key 被立即禁用。这导致全球成千上万的直接用户在没有任何操作的情况下，软件地图功能瞬间失效，并在 GitHub Issues 中爆发了大量报错。

**解决方案**: 开发团队紧急移除了硬编码在代码库中的 API Key，并重构了鉴权逻辑。新的方案要求用户在首次使用地图功能时，必须在设置界面填入自己的 Google Cloud API Key。同时，项目更新了文档，指导用户如何去 Google Cloud Console 创建一个受限的 API Key（限制引用 HTTP 来源或 Android/IOS 应用包名），以确保 Key 仅能被该客户端调用。

**效果**: 虽然短期内增加了用户的使用门槛（需要用户自己去申请 Key），但彻底解决了 Key 因共享而被滥用或封禁的问题。新的架构确保了即使恶意用户获取了客户端代码，也无法利用该 Key 进行其他未授权的调用，保障了项目的长期稳定运行和合规性。

---



### 2：某初创科技公司的 Web 应用

 2：某初创科技公司的 Web 应用

**背景**: 这是一家专注于生成式 AI 应用的初创公司，其产品前端网页直接集成了 Google 的 Gemini API 模型，用于提供实时的文本对话功能。为了加快开发速度，开发人员最初将 API Key 直接存储在前端 JavaScript 代码中，认为只要代码混淆了就足够安全。

**问题**: 随着 Gemini API 的普及，攻击者开始利用自动化脚本扫描 GitHub 和公共网页，寻找泄露的 Google Cloud Key。该公司的前端代码被爬取，API Key 被提取。攻击者利用该 Key 消耗了巨额的 API 配额进行恶意调用，导致公司在短短几天内收到了一张远超预算的 Google Cloud 账单，且服务因配额耗尽而对正常用户不可用。

**解决方案**: 团队实施了“零信任”架构，彻底移除了前端 API 调用。他们搭建了一个轻量级的后端代理服务（使用 Node.js 或 Python），前端不再直接请求 Google，而是请求自己的后端服务器。后端服务器在安全的环境变量中存储 API Key，并负责与 Google API 交互。此外，他们启用了 Google Cloud 的 API Key 限制策略，将 Key 绑定到后端服务器的特定出口 IP 地址。

**效果**: 后端代理不仅完全隐藏了敏感凭证，还使得公司能够实施精细化的速率限制和用户鉴权，防止了恶意刷单。通过绑定 IP 和设置每日预算上限，该公司成功将 API 成本控制在可预测范围内，并消除了凭证泄露带来的财务风险。

---



### 3：某在线教育平台的课程演示

 3：某在线教育平台的课程演示

**背景**: 该平台提供大量关于 Web 开发和 AI 集成的视频教程。为了降低学习门槛，讲师在过去的录播课程中，直接使用了自己申请的 Google API Key 进行演示，并将包含该 Key 的示例代码上传到了课程仓库供学生下载。

**问题**: 随着课程受众的扩大，代码仓库中的 Key 被广泛传播。部分学生出于好奇或测试目的，频繁调用该 Key，导致讲师的 Google Cloud 账户产生了异常高额的费用。同时，Google 的安全系统检测到该 Key 来自多个不同的地理位置和 IP，触发了欺诈警报，将 Key 强制停用，导致正在进行直播演示的课程无法加载模型。

**解决方案**: 讲师团队开发了一个简单的“凭证交换系统”。他们移除了所有公开代码中的真实 Key，替换为占位符 `YOUR_API_KEY`。同时，他们开发了一个微服务，允许注册的学生申请一个“临时受限 Key”。这些临时 Key 通过 Google Cloud 的“API Keys Service”生成，并被严格限制了每日调用次数（例如每天 100 次）和仅允许访问特定的 AI 模型 API。

**效果**: 这一举措既保护了讲师的主账户安全，又为真实的学习环境提供了沙箱机制。学生可以合法地申请 Key 进行实验，而无需担心产生高额费用；平台也杜绝了因 Key 泄露导致的服务中断风险，确保了教学内容的持续可用性。

---
## 最佳实践

## 最佳实践指南

### 实践 1：实施严格的 API 密钥访问控制

**说明**：
Google API 密钥曾经被视为无需严格保密的公开标识符，但随着 Gemini 等 AI 模型引入按量计费和配额限制，泄露密钥可能导致资源被滥用或产生高额费用。必须将 API 密钥视为高敏感凭证进行管理。

**实施步骤**:
1. 在 Google Cloud Console 中，进入“API 和服务” > “凭据”页面。
2. 创建 API 密钥时，点击“编辑 API 密钥”。
3. 在“应用限制”部分，选择特定的 IP 地址、HTTP 引用来源（网站）或 Android/iOS 应用作为限制条件。
4. 在“API 限制”部分，仅勾选该密钥实际需要调用的具体 API（例如仅启用“Gemini API”而非所有 Google 服务）。

**注意事项**:
不要在生产环境中使用“无限制”的 API 密钥。一旦密钥泄露，攻击者可以利用该密钥访问所有授权的服务。

---

### 实践 2：杜绝客户端代码中的硬编码密钥

**说明**：
在 Web 前端（HTML/JS）或移动端 App 中硬编码 API 密钥是极其危险的做法，因为这些代码可以被任何人下载和反编译，从而导致密钥直接暴露。

**实施步骤**:
1. 将所有调用 Google API 的逻辑从客户端移除。
2. 建立后端代理服务（如 Python Flask, Node.js Express 或 Cloud Functions）。
3. 客户端向您的后端服务器发起请求，后端服务器从安全的环境变量中读取 API 密钥。
4. 后端服务器代表客户端向 Google API 发起请求，并将结果返回给客户端。

**注意事项**:
如果必须使用客户端调用（如纯静态网站），请务必配合“实践 1”中的 HTTP 引用来源限制，以限制密钥只能在您的域名下使用。

---

### 实践 3：建立实时监控与预算预警机制

**说明**：
由于 Gemini 等生成式 AI 服务通常按 Token 使用量计费，密钥泄露可能导致费用在短时间内急剧飙升。设置预算预警是防止经济损失的最后一道防线。

**实施步骤**:
1. 登录 Google Cloud Console，进入“计费” (Billing) 页面。
2. 导航至“预算和预警” > “创建预算”。
3. 设置具体的金额阈值（例如 10 美元或 50 美元）。
4. 配置预警通知，通过电子邮件和短信发送给运维团队。
5. 在“API 和服务”中启用“Cloud Billing Budget”相关的 API 以便自动化监控。

**注意事项**:
不要将预算上限设置得过高。对于测试项目，建议设置极低的阈值（如 5 美元），以便在异常发生的第一时间发现。

---

### 实践 4：定期轮换与撤销密钥

**说明**：
长期有效的密钥增加了暴露窗口期。定期轮换密钥可以确保即使某个密钥在不经意间泄露，其有效期也仅限于很短的时间范围内。

**实施步骤**:
1. 制定密钥轮换计划，建议每 90 天进行一次。
2. 在 Google Cloud Console 中创建新的 API 密钥。
3. 将新密钥部署到应用的非生产环境进行验证。
4. 将新密钥部署到生产环境，并更新所有相关引用。
5. 确认应用运行正常后，立即在控制台中删除或禁用旧的 API 密钥。

**注意事项**:
在删除旧密钥之前，务必检查是否有遗留的脚本或旧版应用仍在使用它，以免导致服务中断。

---

### 实践 5：利用密钥指纹识别与审计日志

**说明**：
当怀疑密钥泄露时，需要确认泄露的具体位置。Google 会在创建密钥时生成“密钥指纹”（SHA-256 哈希值），这有助于区分泄露的是官方密钥还是第三方打包的版本。

**实施步骤**:
1. 在 Google Cloud Console 的凭据页面，点击密钥详情查看其指纹。
2. 如果在 GitHub 或其他平台发现疑似泄露的密钥，计算该泄露字符串的 SHA-256 哈希值。
3. 将计算出的哈希值与控制台中的指纹进行比对。
4. 启用 Cloud Audit Logs，记录所有针对该 API 密钥的调用和配置变更。

**注意事项**:
不要试图通过比对明文密钥来确认身份，始终使用指纹哈希值进行比对，以确保安全性。

---

### 实践 6：使用密钥管理服务 (KMS) 或 Secrets Manager

**说明**：
将 API 密钥存储在代码仓库或配置文件中是不安全的。使用专门的密钥管理工具可以提供加密存储和动态注入功能。

**实施步骤**:
1. 使用 Google Secret Manager 或 AWS Secrets Manager 等工具存储 API 密钥。
2. 在应用程序启动时，通过 SDK 或环境变量动态获取密钥，而不是将其写入代码。
3. 确保只有运行应用程序的服务账号（

---
## 学习要点

- Google API 密钥长期被视为非敏感信息，因为其默认仅绑定计费账户而不限制具体调用者，导致开发者常将其直接硬编码在客户端代码中。
- Gemini API 的引入打破了这一惯例，因为调用该模型会消耗昂贵的资源配额，使得拥有密钥等同于拥有可直接变现的资产。
- 攻击者现在可以通过逆向工程 Android 应用或抓取网络流量，在几秒钟内窃取 API 密钥并迅速耗尽受害者的配额。
- Google 现有的安全机制（如针对 Python 脚本的“应用限制”）存在缺陷，无法有效区分合法的自动化工具与恶意脚本，导致误报率高。
- 开发者必须立即停止在客户端代码中暴露 API 密钥，转而使用代理服务器或后端中转来隔离密钥，这是防止配额被盗的唯一有效方法。
- 事件揭示了云安全模型中的核心矛盾：API 设计旨在鼓励便捷的客户端调用，但新的计费模式却要求必须像保护银行凭证一样保护密钥。

---
## 常见问题


### 1: 为什么以前 Google API Key 不被视为严格保密的机密信息？

1: 为什么以前 Google API Key 不被视为严格保密的机密信息？

**A**: 在很长一段时间里，开发者社区普遍认为 Google API Key（尤其是用于公开端点的 Key）属于“低敏感”凭证。这主要有两个原因：
1.  **公开可见性**：Google 官方文档和许多开源项目（如 GitHub 上的代码）经常直接在前端代码或示例中展示 API Key。由于这些请求通常来自客户端，Google 依靠 HTTP Referer 检查或 IP 白名单来限制滥用，而不是完全依赖 Key 的保密性。
2.  **默认配额保护**：Google 对 API Key 设有默认的每日配额限制。即便 Key 被泄露，攻击者也只能使用有限的免费额度，很难对拥有者造成直接的经济损失（除非拥有者主动绑定了高额计费账户）。

---



### 2: Gemini 的出现改变了什么规则？

2: Gemini 的出现改变了什么规则？

**A**: 随着 Google Gemini API 的推出和普及，风险模型发生了根本性变化。与传统的地图或搜索 API 不同，Gemini 是生成式 AI 模型（大语言模型 LLM）。
1.  **高昂的调用成本**：LLM 的推理成本远高于传统 API。如果有人盗用了你的 API Key 来运行大量的 Prompt 或进行微调，可能会在短时间内产生巨额账单。
2.  **模型滥用风险**：攻击者可能利用被盗的 Key 绕过安全过滤器，利用 Google 的算力生成恶意内容，而责任可能会追溯到 Key 的持有者。
3.  **绑定计费账户**：为了使用 Gemini，许多开发者必须将 API Key 与启用了自动计费的 Cloud 项目关联，这使得 Key 直接具备了“扣款凭证”的属性。

---



### 3: 如果我的 Google API Key 已经泄露到了 GitHub 或公网上，应该怎么办？

3: 如果我的 Google API Key 已经泄露到了 GitHub 或公网上，应该怎么办？

**A**: 必须立即采取行动以止损：
1.  **在 Google Cloud Console 中撤销密钥**：不要试图修改它，直接在凭据页面删除或禁用该 Key。
2.  **创建新密钥并重新配置**：生成新的 API Key，并更新你的应用程序配置。
3.  **检查使用情况**：在 Google Cloud 的“计费”和“API 仪表板”中查看泄露期间是否有异常的调用量和费用。
4.  **清理公网痕迹**：虽然代码已经公开，但应立即从 GitHub 仓库中删除密钥（如果可能，建议使用 Git 历史清理工具，或者直接将该仓库设为私有/联系 GitHub 支持处理敏感信息）。

---



### 4: 如何正确保护 Google API Key？

4: 如何正确保护 Google API Key？

**A**: 最佳实践是永远不要将 API Key 硬编码在客户端代码（如 HTML, JS, Android/iOS App）中。
1.  **使用代理服务器**：架构上应采用“客户端 -> 后端服务器 -> Google API”的模式。API Key 只保存在后端服务器的环境变量中，前端发起请求由后端转发。
2.  **配置 Google Cloud 安全设置**：如果必须在客户端使用，必须在 Google Cloud Console 的凭据页面中，严格设置“应用程序限制”（如指定 Android/iOS 包名或 HTTP Referer）和“API 限制”（只启用该 Key 必须访问的 API，如仅启用 Gemini API，禁用其他所有 API）。

---



### 5: Google 官方是否有提供工具来帮助管理或扫描泄露的 Key？

5: Google 官方是否有提供工具来帮助管理或扫描泄露的 Key？

**A**: 是的，Google 提供了多种机制来辅助管理：
1.  **Secret Manager**：Google Cloud 提供的 Secret Manager 服务可以安全地存储密钥、密码和敏感信息，并与 Compute Engine 或 Kubernetes 等服务集成，避免硬编码。
2.  **GitHub 集成**：Google Cloud 会自动扫描 GitHub 上的公开仓库，如果发现属于你项目的 Cloud Key，会尝试通过邮件通知你（前提是该 Key 关联了你的 Google 账号）。
3.  **Health Check API**：开发者可以使用 `apikeys.googleapis.com` 提供的接口来查询 Key 的配置是否安全（例如是否检查了 Referer 限制）。

---



### 6: 仅仅限制 API Key 的“引用站点”就足够安全了吗？

6: 仅仅限制 API Key 的“引用站点”就足够安全了吗？

**A**: 不够。虽然设置 HTTP Referer 限制（即只允许特定域名调用）是基础防御，但它并非无懈可击：
1.  **Referer 可以被伪造**：在服务器端发起的请求中，HTTP Referer 头是可以被任意伪造的，攻击者可以绕过这一限制。
2.  **中间人攻击**：在不安全的网络环境下，Referer 信息可能被截获。
因此，最安全的做法依然是**不在客户端暴露任何带有调用权限的 API Key**，或者确保该 Key 仅拥有极低权限且受到严格的计费告警监控。

---



### 7: 这次规则变化对开源项目维护者有什么具体影响？

7: 这次规则变化对开源项目维护者有什么具体影响？

**A**: 影响巨大，因为开源项目通常要求代码“开箱即用”：
1.  **无法再提供演示 Key**：以前开源作者可以在代码中内置一个 Key 用于演示功能，现在

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: 基础安全风险

### 问题**: 在 Web 开发中，区分前端公开代码与后端私密代码是安全的基础。请列出三种常见的 API Key 或敏感信息泄露途径，并解释将 API Key 硬编码在客户端代码中的具体风险。

### 提示**: 请结合代码仓库管理、版本控制历史以及浏览器开发者工具的功能进行分析。重点在于攻击者获取明文信息的难易程度。

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
- 标签： [API密钥](/tags/api%E5%AF%86%E9%92%A5/) / [Gemini](/tags/gemini/) / [谷歌](/tags/%E8%B0%B7%E6%AD%8C/) / [安全漏洞](/tags/%E5%AE%89%E5%85%A8%E6%BC%8F%E6%B4%9E/) / [LLM](/tags/llm/) / [认证机制](/tags/%E8%AE%A4%E8%AF%81%E6%9C%BA%E5%88%B6/) / [数据泄露](/tags/%E6%95%B0%E6%8D%AE%E6%B3%84%E9%9C%B2/) / [API管理](/tags/api%E7%AE%A1%E7%90%86/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/)

### 相关文章

- [Google API密钥曾非机密，但Gemini改变了规则]({{< relref "posts/20260226-hacker_news-google-api-keys-werent-secrets-but-then-gemini-cha-4.md" >}})
- [谷歌API密钥非机密但Gemini改变规则]({{< relref "posts/20260226-hacker_news-google-api-keys-werent-secrets-but-then-gemini-cha-0.md" >}})
- [谷歌API密钥曾非机密，Gemini规则变更引发安全隐忧]({{< relref "posts/20260226-hacker_news-google-api-keys-werent-secrets-but-then-gemini-cha-1.md" >}})
- [谷歌API密钥曾非机密 但Gemini改变了规则]({{< relref "posts/20260226-hacker_news-google-api-keys-werent-secrets-but-then-gemini-cha-2.md" >}})
- [谷歌DeepMind推出SynthID：为AI生成文本添加水印的技术]({{< relref "posts/20260226-hacker_news-synthid-7.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*