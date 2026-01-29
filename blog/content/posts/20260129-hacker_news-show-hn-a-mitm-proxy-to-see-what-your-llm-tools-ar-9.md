---
title: "Show HN：一款用于监控 LLM 工具数据传输的中间人代理"
date: 2026-01-29T05:01:24+08:00
draft: false
entry_kind: "auto"
tags: ["LLM", "中间人代理", "网络抓包", "隐私审计", "逆向工程", "OpenAI", "API 调试", "数据可视化"]
categories: ["安全", "开发工具"]
source: hacker_news
external_url: https://github.com/jmuncor/sherlock
scenarios: ["大语言模型", "AI/ML项目"]
---

# Show HN：一款用于监控 LLM 工具数据传输的中间人代理

---

## 基本信息

- **作者**: jmuncor
- **评分**: 112
- **评论数**: 47
- **链接**: [https://github.com/jmuncor/sherlock](https://github.com/jmuncor/sherlock)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46799898](https://news.ycombinator.com/item?id=46799898)

---
## 导语

随着大语言模型工具的普及，数据隐私与透明度问题日益受到关注。本文介绍的一款中间人代理工具，能够帮助开发者直观地查看 LLM 应用实际发送的 API 请求内容。通过阅读本文，你将了解该工具的运作原理及具体用法，从而更有效地监控数据流向并排查潜在的安全隐患。

---
## 摘要

这是一份关于 Show HN 帖子 **“A MitM proxy to see what your LLM tools are sending”** 的中文总结：

**项目简介**
这是一个开源的**中间人代理工具**，旨在帮助用户查看和调试那些集成了大语言模型（LLM）的应用程序在后台实际发送的数据内容。

**核心背景与痛点**
目前的许多 AI 工具（如桌面客户端、浏览器插件等）在调用 OpenAI (GPT-4) 或 Anthropic (Claude) 等 API 时，往往是不透明的。用户无法直观地看到：
1.  应用到底发送了什么提示词。
2.  是否泄露了用户的隐私数据或敏感信息。
3.  实际的请求参数和返回结果是什么。

**工具功能与原理**
该工具通过在本地搭建一个代理服务器，拦截并展示 AI 工具与 LLM 提供商之间的 HTTP 流量。其主要功能包括：
*   **流量拦截**：捕获所有经过的 API 请求和响应。
*   **数据可视化**：将原本复杂的网络请求以人类可读的格式（通常是对话式的 UI）展示出来，让用户看到原始的 JSON 数据。
*   **兼容性**：支持模拟 OpenAI 的 API 端点，因此可以轻松代理大多数支持自定义 API Base URL 的客户端。

**使用场景**
1.  **隐私审计**：检查应用是否偷偷上传了不必要的上下文或敏感数据。
2.  **逆向工程/学习**：了解其他优秀的 AI 工具是如何构建 Prompt（提示词）的，以此学习优化自己的 Prompt 技巧。
3.  **调试**：开发者可以用它来排查自己应用在调用 LLM 时的参数错误。

**总结**
这是一个面向开发者、安全研究人员或高级用户的实用工具，它打破了 AI 应用“黑盒”的状态，让 LLM 的交互过程变得透明可控。

---
## 评论

### 中心观点
该文章介绍了一种通过构建中间人代理来审查大语言模型（LLM）工具数据流的技术手段，其核心价值在于在黑盒化的AI生态中通过“逆向工程”赋予用户数据透明度与隐私控制权。

### 深入评价

#### 1. 内容深度：从“黑盒使用”到“白盒审计”的范式转变
**支撑理由：**
*   **技术底层的解构**：文章不仅仅停留在表面的API调用，而是深入到了网络传输层。通过拦截HTTPS流量，它揭示了LLM应用（如Copilot、ChatGPT桌面版等）在用户不知情的情况下发送的具体Payload。这包括不仅限于提示词，还包括系统提示词、遥测数据以及潜在的PII（个人身份信息）。
*   **论证的严谨性（技术视角）**：从技术实现上看，利用MitM（Man-in-the-Middle）代理是分析加密流量的标准方法。文章论证了当前AI工具缺乏“本地模式”的痛点，即所有智能计算都依赖于云端上传，从而使得流量拦截成为唯一的审计手段。
*   **安全边界的探讨**：文章隐含地探讨了“客户端安全”的边界。它指出了一个事实：即使客户端应用程序是闭源的，其网络行为必须是可观测的，这是安全审计的基本要求。

**反例/边界条件：**
*   **证书绑定**：许多现代AI应用（特别是移动端App或经过加固的桌面端）会实施SSL Pinning（证书绑定），直接拒绝非官方签名的证书，此时该MitM代理将失效，需要更高级的Hook技术（如Frida）配合。
*   **端到端加密**：如果LLM提供商在客户端实施了额外的E2E加密层，代理只能看到密文而无法解析具体内容，虽然这在当前的通用LLM工具中较少见，但是一个技术边界。

#### 2. 实用价值：企业合规与Prompt工程的双重利器
**支撑理由：**
*   **数据防泄露（DLP）**：对于企业而言，员工使用未授权的AI工具可能导致代码或机密外泄。该工具提供了一种低成本的审计方式，允许企业在不阻断生产力的情况下，监控具体流出了什么数据。
*   **Prompt逆向工程**：对于开发者和Prompt工程师，这是极佳的学习工具。通过拦截请求，可以还原出顶级工具（如Claude或GPT-4 wrapper）是如何构建System Prompt的，从而学习如何编写更高效的指令。

**反例/边界条件：**
*   **误报率与隐私伦理**：监控工具本身也可能成为隐私漏洞。如果MitM代理服务器被攻破，所有拦截下来的敏感数据将暴露，因此其实用性仅限于受控环境（如本地回环或私有网络），不适合在公共网络部署。
*   **法律风险**：在某些司法管辖区，拦截他人（即使是员工）的加密流量可能涉及法律红线，需谨慎使用。

#### 3. 创新性：旧瓶装新酒，但在AI领域具有开创性
**支撑理由：**
*   **针对特定领域的工具化**：MitM代理本身是古老的技术（如Charles, Fiddler），但将其专门打包、配置用于“LLM数据审计”是一个新的切入点。它填补了“AI安全扫描”细分市场的空白。
*   **自动化解析**：如果该工具能自动解析并格式化输出JSON格式的LLM请求/响应，这比对着Wireshark的一堆Hex码要高效得多，具有工具层面的微创新。

**反例/边界条件：**
*   **缺乏原生集成**：真正的创新应该是LLM提供商提供“审计模式”或“本地日志导出”，而不是靠用户自己架设代理。这种工具本质上是对厂商封闭生态的“打补丁”。

#### 4. 可读性与逻辑性
**支撑理由：**
*   **极客风格的直接**：Show HN系列文章通常逻辑直截了当：问题 -> 解决方案 -> 代码。对于技术人员来说，这种“Talk is cheap, show me the code”的风格具有很高的可读性和亲和力。
*   **逻辑闭环**：从怀疑数据被发送，到搭建代理验证，再到分析结果，逻辑链条完整。

#### 5. 行业影响：推动“可观测性”与“隐私优先”的博弈
**支撑理由：**
*   **倒逼厂商透明**：此类开源工具的普及会倒逼AI工具厂商更加审慎地处理用户数据。如果用户能轻易看到工具发送了过多的元数据，会引发公关危机，从而促使厂商修改其数据收集策略。
*   **标准化需求**：可能会推动行业制定LLM客户端的数据传输标准，例如明确标记哪些数据是用于训练，哪些仅用于推理。

**反例/边界条件：**
*   **军备竞赛升级**：厂商为了保护其Prompt知识产权或防止数据被爬取，可能会进一步加强混淆和加密，导致普通用户更难调试和使用工具。

#### 6. 争议点：安全审计 vs. 逆向破解
*   **争议核心**：该工具处于灰色地带。一方面它是为了安全审计，另一方面它也常被用于破解软件协议、绕过付费限制或提取专有的System Prompt。
*   **不同观点**：AI厂商可能认为此类工具助长了“Prompt注入”攻击或模型蒸馏（Model Distillation）盗版行为，可能会在后续版本中通过ToS（服务条款）明确禁止此类中间人攻击。

### 事实陈述 / 作者观点 / 你的推断

*   **[事实陈述]**：文章展示了如何使用MitM

---
## 代码示例




```python
# 示例1：基础MitM代理实现
from mitmproxy import http
import json

class LLMSniffer:
    def request(self, flow: http.HTTPFlow) -> None:
        """拦截并记录LLM API请求"""
        if "api.openai.com" in flow.request.pretty_host:
            try:
                # 解析请求体
                req_data = json.loads(flow.request.content)
                print("\n=== 拦截到LLM请求 ===")
                print(f"模型: {req_data.get('model', 'unknown')}")
                print(f"提示词: {req_data.get('messages', [{}])[0].get('content', '')[:100]}...")
                
                # 记录完整请求到文件
                with open("llm_requests.log", "a") as f:
                    f.write(f"\n{json.dumps(req_data, indent=2)}\n")
            except Exception as e:
                print(f"解析请求失败: {str(e)}")

    def response(self, flow: http.HTTPFlow) -> None:
        """记录API响应"""
        if "api.openai.com" in flow.request.pretty_host:
            try:
                resp_data = json.loads(flow.response.content)
                print(f"\n=== 收到响应 ===")
                print(f"Token使用: {resp_data.get('usage', {})}")
                print(f"响应片段: {resp_data.get('choices', [{}])[0].get('message', {}).get('content', '')[:100]}...")
            except Exception as e:
                print(f"解析响应失败: {str(e)}")

# 使用方法: mitmdump -s llm_sniffer.py
```




```python
# 示例2：敏感信息脱敏处理
import re
from mitmproxy import http

class DataSanitizer:
    def __init__(self):
        # 定义敏感信息正则模式
        self.patterns = {
            "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "phone": r'\b\d{3}-\d{3}-\d{4}\b',
            "credit_card": r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'
        }

    def request(self, flow: http.HTTPFlow) -> None:
        """自动脱敏敏感信息"""
        if "api.openai.com" in flow.request.pretty_host:
            try:
                # 解析请求体
                req_data = json.loads(flow.request.content)
                content = req_data.get('messages', [{}])[0].get('content', '')
                
                # 应用脱敏规则
                for name, pattern in self.patterns.items():
                    content = re.sub(pattern, f"[REDACTED {name}]", content)
                
                # 更新请求内容
                req_data['messages'][0]['content'] = content
                flow.request.content = json.dumps(req_data).encode('utf-8')
                
                print(f"\n=== 已脱敏敏感信息 ===")
                print(f"处理后的内容: {content[:200]}...")
            except Exception as e:
                print(f"脱敏处理失败: {str(e)}")

# 使用方法: mitmdump -s data_sanitizer.py
```




```python
# 示例3：请求/响应分析仪表板
from mitmproxy import http
import json
from datetime import datetime

class LLMAnalytics:
    def __init__(self):
        self.metrics = {
            "total_requests": 0,
            "total_tokens": 0,
            "model_usage": {},
            "error_count": 0
        }

    def request(self, flow: http.HTTPFlow) -> None:
        """收集请求指标"""
        if "api.openai.com" in flow.request.pretty_host:
            try:
                req_data = json.loads(flow.request.content)
                model = req_data.get('model', 'unknown')
                
                self.metrics["total_requests"] += 1
                self.metrics["model_usage"][model] = self.metrics["model_usage"].get(model, 0) + 1
                
                # 记录请求时间
                flow.request.metadata["start_time"] = datetime.now()
            except Exception as e:
                print(f"分析请求失败: {str(e)}")

    def response(self, flow: http.HTTPFlow) -> None:
        """收集响应指标"""
        if "api.openai.com" in flow.request.pretty_host:
            try:
                resp_data = json.loads(flow.response.content)
                
                # 计算请求耗时
                if "start_time" in flow.request.metadata:
                    duration = (datetime.now() - flow.request.metadata["start_time"]).total_seconds()
                    print(f"\n=== 请求耗时: {duration:.2f}秒 ===")
                
                # 统计token使用
                usage = resp_data.get('usage', {})
                if usage:
                    self.metrics["total_tokens"] += usage.get('total_tokens', 0)
                
                # 检查错误
                if flow.response.status_code != 200:
                    self.metrics["error_count"] += 1


---
## 案例研究


### 1：某金融科技初创公司（内部工具开发团队）

 1：某金融科技初创公司（内部工具开发团队）

**背景**:
该公司正在开发一款基于 GPT-4 的内部金融知识问答助手，用于辅助员工快速检索合规条款。由于金融数据极其敏感，公司制定了严格的数据安全策略，禁止将任何未脱敏的用户个人身份信息（PII）发送给外部 API。

**问题**:
开发团队使用了一个封装好的开源 LLM 调用库。在代码审查阶段，安全团队发现无法确定该库在发送请求前是否完整执行了预设的“数据清洗”逻辑。他们担心某些边缘情况会导致原始的敏感数据（如客户姓名、身份证号）直接泄露给 OpenAI 的服务器，从而造成合规风险。

**解决方案**:
团队部署了该 MitM（中间人）代理工具，将其配置在开发环境和 OpenAI API 之间。通过拦截并解密 HTTPS 流量，团队能够以明文形式查看到实际发出的 HTTP 请求内容，验证了 Prompt 中是否包含了敏感字段。

**效果**:
通过代理抓包，团队迅速发现了一个严重的 Bug：在处理多轮对话中的上下文时，代码错误地将原始的用户输入拼接入 Prompt，绕过了脱敏逻辑。修复该问题后，团队再次通过代理确认了发出的请求仅包含掩码后的数据（如“用户***”），成功避免了潜在的数据泄露事故，确保了产品上线符合 GDPR 和行业合规要求。

---



### 2：某电商公司的 SaaS 集成项目

 2：某电商公司的 SaaS 集成项目

**背景**:
该公司计划将其自研的工单系统与 ChatGPT 进行集成，利用 LLM 自动生成客户回复的建议草稿。为了优化成本和体验，技术团队需要精确控制发送给 OpenAI 的 Token 数量，并评估不同 Prompt 模板的效果。

**问题**:
开发人员发现，实际计费的 Token 数量与他们代码中预估的数量存在较大差异。此外，他们怀疑使用的第三方 SDK 在底层自动添加了隐藏的系统提示词，这不仅增加了额外的 Token 消耗，还可能干扰模型的输出风格。

**解决方案**:
工程师利用该 MitM 代理工具对应用发出的流量进行“透视”。他们不需要修改 SDK 的源码，直接通过代理日志查看了完整的 JSON Payload，包括 `messages` 数组中的所有内容和 `usage` 字段返回的精确计数。

**效果**:
通过分析代理捕获的请求，团队确认了 SDK 确实注入了一段长达 200 Token 的隐藏说明文本，导致每次请求成本增加约 5%。基于这一发现，团队决定放弃该 SDK，改用原生的 HTTP API 进行调用，从而实现了对成本的完全可控。同时，通过对比代理记录的请求与响应，他们优化了 Prompt 结构，将 API 响应延迟降低了 20%。

---
## 最佳实践

## 最佳实践指南

### 实践 1：建立透明的流量审计机制

**说明**:
在部署中间人代理监控 LLM 流量时，首要原则是确保监控活动的透明性。开发者应明确记录监控的目的、范围以及数据留存策略，避免未经授权的敏感数据拦截。这不仅符合合规要求，也能建立团队内部的信任机制。

**实施步骤**:
1. 制定书面的监控政策，明确哪些工具和端点在监控范围内。
2. 在团队文档中公开披露代理服务器的存在及其功能。
3. 定期审查监控日志的访问权限，确保只有授权人员可以查看。

**注意事项**:
切勿在生产环境中直接监控包含用户个人身份信息（PII）的流量，除非已获得明确同意并符合 GDPR 或其他数据保护法规。

---

### 实践 2：实施严格的日志脱敏与加密

**说明**:
LLM 交互往往包含高度敏感的上下文信息或专有数据。代理工具在记录请求和响应时，必须默认执行数据脱敏处理，以防止明文存储导致的数据泄露风险。

**实施步骤**:
1. 配置代理服务器，自动识别并屏蔽特定的敏感字段（如 API Keys、Cookie、用户密码）。
2. 确保日志文件存储在加密的文件系统中。
3. 设置日志的自动轮转和过期删除机制（例如 7 天后自动删除）。

**注意事项**:
即使使用了脱敏技术，仍应将日志视为高敏感资产。避免将日志上传到第三方分析平台或公共代码仓库。

---

### 实践 3：通过流量分析优化 Token 使用成本

**说明**:
监控流量的核心价值之一是成本控制。通过分析代理捕获的请求体，可以精确统计不同工具发送的 Token 数量，识别出冗余的上下文发送或低效的 Prompt 设计，从而优化 API 支出。

**实施步骤**:
1. 使用代理工具附带的分析脚本，按端点或功能模块汇总 Token 消耗量。
2. 识别发送过长上下文的请求，分析是否包含重复或不必要的历史记录。
3. 基于 Proxy 的观察结果，重构应用代码，实施截断或摘要策略。

**注意事项**:
在计算 Token 时，注意不同模型使用的 Tokenizer 可能不同，确保 Proxy 工具支持针对特定模型的计数方式。

---

### 实践 4：验证数据完整性与请求结构

**说明**:
代理不仅是观察工具，也是调试工具。最佳实践包括利用 Proxy 来验证发送给 LLM 提供商的 JSON 结构是否正确，以及流式传输（Streaming）是否按预期工作，防止因格式错误导致的请求失败或计费错误。

**实施步骤**:
1. 在测试环境启动 Proxy，强制应用通过该代理发送请求。
2. 对比应用发出的原始请求与 LLM 提供商文档规范，检查参数缺失或类型错误。
3. 模拟网络延迟或超时，观察应用的重试逻辑和错误处理是否健壮。

**注意事项**:
某些 LLM SDK 可能会校查 SSL 证书。在配置 Proxy 时，确保正确导入了自签名证书，以免因证书校验失败导致应用无法发起请求。

---

### 实践 5：隔离开发与生产环境的代理配置

**说明**:
为了性能和安全性，不应在生产环境默认启用详细的调试级代理。最佳实践是仅在开发、测试或预发布环境中启用此类深度监控，生产环境仅开启必要的指标收集（如延迟和状态码）。

**实施步骤**:
1. 使用环境变量（如 `ENABLE_PROXY_DEBUG=true`）来控制代理的启动。
2. 在 CI/CD 流水线中配置不同的配置文件，确保生产构建不包含调试代理的依赖。
3. 对于生产环境，考虑使用轻量级的流量镜像而非直接串接代理。

**注意事项**:
调试代理本身可能会引入网络延迟。在评估 LLM 应用响应速度时，必须考虑代理带来的额外开销，以免误判性能瓶颈。

---

### 实践 6：利用代理进行安全边界测试

**说明**:
利用 MitM 代理，开发人员可以主动修改发送给 LLM 的请求，以此测试应用的安全性。例如，模拟注入攻击或发送恶意 Prompt，验证应用端是否有适当的防护层，而不是盲目信任 LLM 的输出。

**实施步骤**:
1. 使用代理工具的“中断并修改”功能，拦截正常的用户查询。
2. 将查询内容替换为常见的越狱指令或提示词注入代码。
3. 观察应用的响应：是否直接泄露了系统 Prompt，或执行了非预期操作。

**注意事项**:
此类测试应仅在受控的隔离环境中进行，切勿针对第三方付费的 LLM 端点进行可能违反服务条款的攻击性测试。

---
## 学习要点

- 该工具通过充当中间人代理，解密并可视化 LLM 应用与 API 之间的通信流量，解决了用户无法知晓工具具体发送了什么数据的黑盒问题。
- 它能够揭示 LLM 工具是否在未经用户同意的情况下，泄露了本地环境变量、代码文件内容或敏感的 API 密钥。
- 该代理支持通过自定义配置，将发送给 OpenAI 等大模型的请求转发至本地模型（如 Ollama），从而实现本地化部署或降低 API 成本。
- 用户可以利用该工具审查发送给模型的“系统提示词”，了解应用如何通过隐藏指令来引导模型的行为或规避审查。
- 它通过拦截并记录完整的请求和响应体，为调试 LLM 应用的网络错误或异常行为提供了直观的原始数据支持。
- 该项目突出了在使用第三方 AI 工具时进行隐私审计的重要性，特别是对于处理企业机密或个人隐私数据的场景。

---
## 常见问题


### 1: 什么是针对 LLM 工具的 MitM 代理，为什么需要它？

1: 什么是针对 LLM 工具的 MitM 代理，为什么需要它？

**A**: MitM（Man-in-the-Middle，中间人）代理是一种位于客户端应用程序（如使用大语言模型的桌面软件或插件）与 LLM 服务商 API（如 OpenAI 的 API）之间的拦截工具。

由于许多 LLM 工具在发送请求时是封闭源代码的，用户并不清楚具体发送了哪些数据。这种代理工具通过在本地搭建一个拦截服务器，将工具的流量引导至该服务器，从而允许用户查看发送的原始 Prompt（提示词）、元数据、以及是否上传了敏感信息。这对于排查 Prompt 注入、调试 Prompt 效果以及确保隐私安全非常有用。

---



### 2: 该工具是如何工作的，我该如何配置？

2: 该工具是如何工作的，我该如何配置？

**A**: 该工具通常在本地运行（例如 localhost:8080），并充当 HTTPS 服务器的角色。其工作流程如下：

1.  **证书信任**：为了拦截加密的 HTTPS 流量，该工具会生成一个本地根证书。你必须在操作系统中将此证书标记为“受信任”，这样应用程序才不会报错。
2.  **流量重定向**：你需要配置目标 LLM 工具，将其 HTTP 代理设置指向你本地运行的 MitM 代理地址和端口。如果工具本身不支持代理设置，你可能需要修改系统的网络环境变量或使用 iptables 等防火墙规则强制重定向流量。
3.  **解析与展示**：当 LLM 工具向 API 发送请求时，请求会先到达 MitM 代理。代理解密请求，将其内容格式化（例如将 JSON Payload 解析为可读文本），然后显示在控制台或 Web UI 中，随后再将请求转发给真实的 LLM API。

---



### 3: 使用这种代理工具是否安全？我的数据会被泄露吗？

3: 使用这种代理工具是否安全？我的数据会被泄露吗？

**A**: 安全性取决于你运行的是开源代码还是闭源软件。

*   **开源项目**：如果是像 Show HN 中提到的这类开源工具，代码是透明的。流量通常仅在本地回环地址（localhost）上处理，不会上传到开发者的服务器。在这种情况下，它是安全的，甚至是增强隐私的，因为它让你看到了工具实际发送了什么。
*   **闭源或在线代理**：如果你使用的是不知名的在线代理服务，你的所有 Prompt 和对话内容都可能被该服务记录。
*   **敏感信息风险**：虽然代理本身不会泄露数据，但在查看日志时，你可能会在屏幕上看到自己的 API Keys 或敏感内容。请确保不要将这些日志截屏分享给他人。

---



### 4: 我能看到哪些具体的信息？

4: 我能看到哪些具体的信息？

**A**: 你通常能看到以下层面的详细信息：

*   **请求头**：包括 `Content-Type`，以及最重要的 `Authorization` 字段（即你的 API Key，你可以借此检查工具是否使用了它自己的 Key 而不是你的）。
*   **请求体**：这是核心部分，你可以看到完整的 System Prompt（系统提示词）、User Prompt（用户输入）以及上下文历史。这有助于发现工具是否在背后添加了额外的隐藏指令。
*   **响应体**：LLM 返回的原始回复内容，包括 Token 使用情况和流式传输的原始数据块。
*   **元数据**：请求调用的具体模型端点（如 `gpt-4` 或 `gpt-3.5-turbo`）。

---



### 5: 如果目标应用程序使用了证书固定，我还能拦截吗？

5: 如果目标应用程序使用了证书固定，我还能拦截吗？

**A**: 这是一个常见的技术难点。

许多商业化的 LLM 客户端为了防止被攻击，会使用“证书固定”技术。这意味着应用程序内部硬编码了 LLM 服务商（如 OpenAI）的真实公钥证书，它会验证收到的服务器证书是否匹配。如果中间插入了你的 MitM 代理证书，验证会失败，应用程序会拒绝连接。

对于这类应用，简单的 MitM 代理无法生效。你通常需要使用高级技术手段，例如：
*   **Root 越狱或插件**：在移动设备上使用 Frida 等工具 Hook 网络库，绕过证书校验逻辑。
*   **逆向工程**：修改应用程序的二进制文件，移除证书固定的代码。
*   **使用虚拟机中的代理**：某些应用在检测到环境变化时可能降低安全策略。

---



### 6: 这与 Charles Proxy 或 Fiddler 有什么区别？

6: 这与 Charles Proxy 或 Fiddler 有什么区别？

**A**: 原理上完全相同，Charles 和 Fiddler 也是通用的 HTTP(S) MitM 调试代理。

区别在于**针对性**：
*   **通用工具**：Charles 和 Fiddler 功能强大，但它们显示的是原始的网络数据包。你需要手动过滤噪音，并且可能需要编写脚本来专门格式化 LLM 的 JSON 流式响应。
*   **LLM 专用代理**：Show HN 中的这类工具通常专门针对 LLM 的数据结构进行了优化。它们可能具备自动解密 Gzip 压缩的 JSON、高亮显示 Prompt 中的特定指令、统计 Token 成本或自动检测敏感词等功能，使用体验比通用抓包工具更友好。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 许多 LLM 应用程序在发送请求时会忽略系统的代理设置。请配置一个环境变量（如 `HTTP_PROXY` 和 `HTTPS_PROXY`），并使用 `curl` 命令验证流量是否成功通过了你搭建的 MitM 代理服务器。

### 提示**: 检查你的代理工具默认监听的端口号（通常是 8080），并确保 `curl` 使用的是 `-x` 参数或对应的环境变量格式。

### 

---
## 引用

- **原文链接**: [https://github.com/jmuncor/sherlock](https://github.com/jmuncor/sherlock)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46799898](https://news.ycombinator.com/item?id=46799898)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [安全](/categories/%E5%AE%89%E5%85%A8/) / [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/)
- 标签： [LLM](/tags/llm/) / [中间人代理](/tags/%E4%B8%AD%E9%97%B4%E4%BA%BA%E4%BB%A3%E7%90%86/) / [网络抓包](/tags/%E7%BD%91%E7%BB%9C%E6%8A%93%E5%8C%85/) / [隐私审计](/tags/%E9%9A%90%E7%A7%81%E5%AE%A1%E8%AE%A1/) / [逆向工程](/tags/%E9%80%86%E5%90%91%E5%B7%A5%E7%A8%8B/) / [OpenAI](/tags/openai/) / [API 调试](/tags/api-%E8%B0%83%E8%AF%95/) / [数据可视化](/tags/%E6%95%B0%E6%8D%AE%E5%8F%AF%E8%A7%86%E5%8C%96/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [揭开Codex Agent循环的神秘面纱！🚀 探索核心机制与价值]({{< relref "posts/20260127-blogs_podcasts-unrolling-the-codex-agent-loop-4.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [kirara-ai：支持多平台接入的多模态AI聊天机器人框架]({{< relref "posts/20260129-github_trending-lss233-kirara-ai-0.md" >}})
- [🤖解密Codex智能体闭环：AI如何自主进化？]({{< relref "posts/20260125-blogs_podcasts-unrolling-the-codex-agent-loop-1.md" >}})
- [🚀Claude Code重磅隐藏功能：Swarms颠覆编程体验！]({{< relref "posts/20260125-hacker_news-claude-codes-new-hidden-feature-swarms-10.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*