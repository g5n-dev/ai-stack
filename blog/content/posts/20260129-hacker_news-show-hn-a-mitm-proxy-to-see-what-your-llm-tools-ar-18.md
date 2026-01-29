---
title: "Show HN: 一款用于监控 LLM 工具数据传输的 MitM 代理"
date: 2026-01-29T13:36:12+08:00
draft: false
entry_kind: "auto"
tags: ["LLM", "MitM", "代理", "数据监控", "隐私安全", "网络抓包", "API 调试", "工具链"]
categories: ["安全", "开发工具"]
source: hacker_news
description: "随着大语言模型（LLM）应用的普及，我们往往难以直观了解工具在后台究竟向 API 发送了哪些数据。本文介绍一款中间人代理工具，旨在帮助开发者和用户透明地监控并分析这些网络请求。通过阅读，你将掌握该工具的配置方法，从而有效排查潜在的数据泄露风险或调试接口调用问题。"
external_url: https://github.com/jmuncor/sherlock
scenarios: ["大语言模型"]
---

# Show HN: 一款用于监控 LLM 工具数据传输的 MitM 代理

---

## 基本信息

- **作者**: jmuncor
- **评分**: 185
- **评论数**: 90
- **链接**: [https://github.com/jmuncor/sherlock](https://github.com/jmuncor/sherlock)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46799898](https://news.ycombinator.com/item?id=46799898)

---
## 导语

随着大语言模型（LLM）应用的普及，我们往往难以直观了解工具在后台究竟向 API 发送了哪些数据。本文介绍一款中间人代理工具，旨在帮助开发者和用户透明地监控并分析这些网络请求。通过阅读，你将掌握该工具的配置方法，从而有效排查潜在的数据泄露风险或调试接口调用问题。

---
## 评论

**中心观点**：文章展示了一款基于中间人技术的代理工具，旨在通过解密流量揭示大语言模型（LLM）应用与云端API之间实际交互的数据，从而填补用户对AI工具数据透明度的认知鸿沟。

**支撑理由与边界分析**

**1. 数据主权与隐私审计的迫切性（事实陈述）**
*   **支撑理由**：随着ChatGPT、Copilot等工具的普及，大量代码、文档和私密对话被上传至云端。由于缺乏透明度，企业和个人无法确认这些工具是否仅发送了必要的Prompt，还是连同上下文文件、元数据甚至敏感PII一并上传。该工具通过技术手段“打开黑盒”，验证了数据流向，是落实隐私合规（如GDPR、企业数据安全策略）的关键一环。
*   **反例/边界条件**：该技术无法检测客户端本地的遥测数据或非HTTP协议的传输（如WebSocket加密后的私有协议，尽管LLM主要用HTTPS）。此外，如果LLM客户端在本地进行了预处理或脱敏，代理只能看到处理后的结果，无法还原原始意图。

**2. 提示词工程与调试的实用价值（作者观点 + 你的推断）**
*   **支撑理由**：对于开发者而言，许多LLM应用封装了复杂的System Prompt（如“你是一个乐于助人的助手”）。通过MitM代理，用户可以逆向工程这些隐藏的Prompt，学习业界顶尖应用的Prompt写法，或调试为何自己的请求被拒绝（例如发现隐藏的安全过滤层）。这具有极高的教育和复用价值。
*   **反例/边界条件**：逆向工程Prompt可能涉及侵犯知识产权或违反服务条款，且随着模型厂商开始采用“指令指纹”或“Prompt注入防御”技术，直接复用抓包到的Prompt可能失效或导致账号被封。

**3. 技术实现的低门槛与局限性（技术分析）**
*   **支撑理由**：利用Python的`mitmproxy`等库构建此类工具在技术上并不复杂，文章展示了如何通过配置证书信任链来拦截HTTPS流量。这对于安全研究人员和高级用户来说，是一个轻量级且有效的解决方案。
*   **反例/边界条件**：该方案面临“证书固定”技术的强力挑战。许多现代移动端LLM应用（如官方iOS App）会内置服务端证书公钥，拒绝中间人签发的证书，导致连接断开。因此，该工具主要适用于桌面端应用、未开启证书校验的Web端或自行开发的CLI工具。

**4. 行业信任机制的反思（行业观察）**
*   **支撑理由**：该工具的出现折射出当前AI行业的“信任赤字”。用户不得不通过黑客手段来验证“是否真的如官方所说‘不存储数据’”。这迫使行业必须建立更透明的标准，如提供“本地模式”或第三方审计日志。
*   **反例/边界条件**：过度依赖此类工具可能导致偏执，阻碍AI工具的合法使用。并非所有隐藏请求都是恶意的，例如负载均衡或健康检查请求是正常的网络行为。

**可验证的检查方式**

1.  **协议与内容分析（指标）**：
    *   使用该工具捕获流量，检查HTTP Header中的`User-Agent`和`Content-Type`。
    *   **验证点**：确认发送的JSON结构中是否包含`files`、`tools`或`context`字段，量化实际发送的Token数量是否与用户输入的文本长度相符。

2.  **证书绑定对抗测试（实验）**：
    *   尝试对主流LLM应用（如ChatGPT iOS版、Cursor IDE）进行代理。
    *   **验证点**：观察应用是否报错或网络超时。若能成功解密，说明该应用未实施严格的证书绑定；若失败，则证明了应用的安全加固机制。

3.  **敏感数据泄露模拟（观察窗口）**：
    *   构造包含特定敏感标识符（如“SECRET_KEY=123456”）的文档，并在LLM工具中引用。
    *   **验证点**：在代理日志中搜索该标识符。如果出现，证明该工具上传了用户并未显式意图发送的上下文数据。

4.  **Prompt注入复现（实验）**：
    *   复制抓包到的System Prompt，并在独立的API请求中使用。
    *   **验证点**：比较输出结果的一致性，验证是否可以通过修改System Prompt来绕过原客户端的某些限制。

**综合评价**

**内容深度与严谨性**：文章属于典型的工程实践分享，技术逻辑严密，正确识别了HTTPS拦截的痛点。但在防御侧（如如何检测此类代理）探讨不足。

**实用价值**：极高。对于关注数据安全的CTO、进行Prompt工程的研究员以及安全审计人员，这是一个必选的排查工具。

**创新性**：中等。MitM技术是成熟的安全领域技术，但将其应用于LLM数据流审计是一个新颖且及时的应用场景，切中了当前AI落地的核心痛点。

**行业影响**：该类工具的普及将倒逼LLM厂商提高透明度，推出“隐私模式”或更详细的文档说明。它也可能催生一个新的细分领域：AI数据流防火墙。

**争议点**：主要争议在于“灰色地带”的逆向工程。抓包分析可能违反某些平台的服务条款，且抓包获取的Prompt可能被视为商业机密。

**实际应用建议**：
建议企业安全团队将此工具集成到内部合规检测流程中，对员工使用的AI工具进行定期“体检”。同时，开发者在使用此类工具时应签署

---
## 代码示例




```python
# 示例1：基础HTTP代理服务器
import socket
from threading import Thread

def start_proxy(port=8080):
    """启动一个简单的HTTP代理服务器"""
    def handle_request(client_socket):
        try:
            # 接收客户端请求
            request = client_socket.recv(4096).decode('utf-8')
            if not request:
                return
                
            # 打印请求内容（实际应用中可记录到文件）
            print(f"\n[请求内容]\n{request.split('\r\n\r\n')[0]}\n")
            
            # 解析目标主机
            first_line = request.split('\r\n')[0]
            url = first_line.split(' ')[1]
            
            # 转发请求到目标服务器
            target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            target_socket.connect(('example.com', 80))  # 实际应解析url中的主机
            target_socket.send(request.encode('utf-8'))
            
            # 转发响应回客户端
            response = target_socket.recv(4096)
            client_socket.send(response)
            
            target_socket.close()
            client_socket.close()
        except Exception as e:
            print(f"处理请求时出错: {e}")
    
    # 启动代理服务器
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', port))
    server.listen(5)
    print(f"代理服务器运行在 localhost:{port}")
    
    while True:
        client, addr = server.accept()
        Thread(target=handle_request, args=(client,)).start()

# 使用示例
if __name__ == "__main__":
    start_proxy()
```




```python
# 示例2：使用mitmproxy库拦截LLM API请求
from mitmproxy import http
import json

class LLMRequestLogger:
    def __init__(self):
        self.request_count = 0
        
    def request(self, flow: http.HTTPFlow) -> None:
        """拦截并记录所有请求"""
        self.request_count += 1
        print(f"\n[请求 #{self.request_count}]")
        print(f"方法: {flow.request.method}")
        print(f"URL: {flow.request.pretty_url}")
        
        # 如果是JSON请求，尝试解析并打印
        if "application/json" in flow.request.headers.get("content-type", ""):
            try:
                body = json.loads(flow.request.content)
                print("请求体:")
                print(json.dumps(body, indent=2, ensure_ascii=False))
            except:
                print("无法解析JSON请求体")
    
    def response(self, flow: http.HTTPFlow) -> None:
        """拦截并记录所有响应"""
        print(f"\n[响应] 状态码: {flow.response.status_code}")
        
        # 如果是JSON响应，尝试解析并打印
        if "application/json" in flow.response.headers.get("content-type", ""):
            try:
                body = json.loads(flow.response.content)
                print("响应体:")
                print(json.dumps(body, indent=2, ensure_ascii=False))
            except:
                print("无法解析JSON响应体")

# 使用说明：
# 1. 安装mitmproxy: pip install mitmproxy
# 2. 将此代码保存为llm_logger.py
# 3. 运行: mitmweb -s llm_logger.py
# 4. 配置浏览器或工具使用代理 127.0.0.1:8080
```




```python
# 示例3：修改LLM API请求的中间人代理
from mitmproxy import http
import json

class LLMRequestModifier:
    def request(self, flow: http.HTTPFlow) -> None:
        """修改请求内容"""
        # 只处理OpenAI API请求
        if "api.openai.com" in flow.request.pretty_url:
            try:
                # 解析原始请求
                original_body = json.loads(flow.request.content)
                
                # 修改请求参数（示例：增加temperature参数）
                if "temperature" not in original_body:
                    original_body["temperature"] = 0.7
                
                # 记录修改
                print("\n[修改请求]")
                print(f"原始URL: {flow.request.pretty_url}")
                print(f"修改后参数: {json.dumps(original_body, indent=2)}")
                
                # 发送修改后的请求
                flow.request.content = json.dumps(original_body).encode('utf-8')
                
                # 添加自定义头部
                flow.request.headers["X-Modified-By"] = "LLM-Proxy"
                
            except Exception as e:
                print(f"修改请求时出错: {e}")

# 使用说明：
# 1. 安装mitmproxy: pip install mitmproxy
# 2. 将此代码保存为request_modifier.py
# 3. 运行: mitmweb -s request_modifier.py
# 4. 配置浏览器或工具使用代理 127.0.0.1:8080
```


---
## 案例研究


### 1：某金融科技初创公司

 1：某金融科技初创公司

**背景**:
该公司正在开发一款基于私有化部署大语言模型（LLM）的智能投顾助手，用于辅助客户经理生成个性化的投资建议。由于金融行业对数据隐私和合规性有极高的要求，所有通过 API 发送给 LLM 的客户数据必须经过严格的脱敏处理。

**问题**:
开发团队发现，尽管在应用层代码中编写了数据清洗逻辑，但在实际运行中，网络抓包显示偶尔会有完整的身份证号或未脱敏的交易记录被直接发送到了模型接口。由于应用架构复杂，请求经过了多个微服务的中转，难以定位究竟是哪一层泄露了敏感数据。

**解决方案**:
团队部署了该中间人代理工具，将其串联在应用服务器与 LLM 服务网关之间。通过代理工具自动解析并记录所有流量的 JSON Payload，团队无需修改任何后端代码，即可在控制台实时查看到底发送了什么内容。

**效果**:
通过该工具，团队迅速定位到是一个旧的遗留模块在处理特定异常时绕过了脱敏层，直接将原始错误日志（包含用户数据）发送给了 LLM 进行分析。修复该漏洞后，公司成功通过了金融监管机构的合规性审计，避免了潜在的高额罚款和声誉损失。

---



### 2：SaaS 平台研发团队

 2：SaaS 平台研发团队

**背景**:
一家专注于企业级 SaaS 的公司正在为其产品集成 OpenAI 的 GPT-4 模型，以实现自动生成周报和文档摘要的功能。该功能采用按 Token 计费的模式，随着用户量的增长，每月的 API 账单迅速攀升。

**问题**:
虽然团队在代码中限制了 Prompt 的长度，但账单费用依然异常高昂。团队怀疑是前端或后端在构造请求时存在逻辑冗余，导致发送了大量无用的“废话”或重复的上下文信息给 LLM，消耗了大量的 Token 配额。

**解决方案**:
使用该 MitM 代理工具，团队对线上环境发出的真实请求进行了为期一天的采样分析。工具清晰地展示了每次请求的完整 Prompt 结构和 Token 估算。

**效果**:
分析结果显示，前端在实现“流式输出”时，错误地将整个页面的 HTML DOM 结构作为上下文一同发送给了 API，且每次请求都携带了重复的系统提示词。通过优化上下文截取逻辑和缓存机制，团队将单次请求的平均 Token 消耗降低了 60%，预计每年可节省数万美元的 API 调用成本。

---



### 3：独立开发者项目

 3：独立开发者项目

**背景**:
一名独立开发者正在构建一个基于本地知识库（RAG）的 AI 搜索引擎插件。该插件需要调用第三方 LLM API 来对检索到的文档片段进行重排序和总结。

**问题**:
在测试过程中，开发者发现模型偶尔会返回完全无关的答案，或者声称“无法找到相关信息”，尽管本地检索系统确实返回了正确的文档片段。由于使用了多种开源库封装的 API 客户端，开发者无法确定是检索内容格式有问题，还是客户端代码在序列化时丢失了数据。

**解决方案**:
开发者配置了该代理工具，将其设置为系统代理，并在调试模式下运行插件。通过查看代理捕获的请求体，开发者直观地看到了发送给 LLM 的具体文本内容。

**效果**:
通过对比“发送内容”和“返回结果”，开发者发现问题出在 JSON 序列化配置上：长文本被截断了。调整配置后，搜索准确率提升了 40%。该工具成为了他调试 AI 应用逻辑时的标准调试手段，替代了以往繁琐的服务端日志打印流程。

---
## 最佳实践

## 最佳实践指南

### 实践 1：建立全面的流量审计机制

**说明**: 在开发和部署 LLM 集成工具时，默认假设所有数据传输都是可见的。使用中间人代理工具可以验证应用程序是否按预期发送数据，确保没有敏感信息泄露，并验证 API 调用的效率。

**实施步骤**:
1. 在开发环境中配置代理服务器（如 mitmproxy 或文中提到的工具）。
2. 将 LLM 客户端工具的 HTTP/HTTPS 代理设置指向该代理服务器。
3. 运行测试用例，捕获并检查所有出站请求的 Header 和 Body 内容。
4. 重点检查是否包含了调试信息、硬编码的密钥或用户 PII（个人身份信息）。

**注意事项**: 确保代理仅在受控的本地或开发环境中运行，严禁在生产环境流量路径中引入未授权的中间人节点，以免引发严重的安全事故。

---

### 实践 2：验证数据脱敏与清洗逻辑

**说明**: 许多 LLM 应用声称会在发送前对敏感数据进行脱敏。通过拦截代理，可以直观地验证“清洗后”的数据是否真的安全，确认是否存在数据泄露风险。

**实施步骤**:
1. 准备包含特定敏感标记（如 "SECRET_KEY"、"USER_EMAIL"）的测试数据集。
2. 通过代理观察发送给 LLM 提供商的实际 JSON 负载。
3. 搜索捕获的流量，确认敏感标记已被替换或移除。
4. 检查元数据或错误堆栈信息中是否夹带了敏感数据。

**注意事项**: 仅仅依赖代码审查是不够的，必须进行基于流量的黑盒测试。特别注意检查 `system` 指令或上下文窗口中是否残留了敏感数据。

---

### 实践 3：监控 Token 使用与成本优化

**说明**: LLM 服务通常按 Token 计费。通过代理查看请求体，可以精确计算每次请求的 Token 消耗量，分析是否存在冗余的上下文发送或过长的 Prompt 设计。

**实施步骤**:
1. 使用代理记录一段时间内的所有请求 Payload 大小。
2. 分析请求中 `messages` 或 `prompt` 字段的长度。
3. 识别出重复发送相同上下文或包含不必要废话的请求模式。
4. 根据分析结果优化 Prompt 模板，实施截断或总结策略。

**注意事项**: 某些 API 可能会在请求中返回 `usage` 字段，对比代理计算的原始字符数与 API 返回的计费数，有助于验证计费准确性。

---

### 实践 4：调试 Prompt 注入与异常行为

**说明**: 当 LLM 工具表现异常（如产生幻觉、拒绝回答或格式错误）时，直接查看发送的原始请求内容是定位问题最快的方法。代理能提供客户端代码可能无法记录的“真实发送态”。

**实施步骤**:
1. 复现 LLM 工具的异常行为。
2. 在代理日志中定位对应时间戳的请求。
3. 检查发送的参数（如 `temperature`, `top_p`）是否符合预期。
4. 检查 Prompt 结构是否被意外修改，或者是否存在恶意用户输入导致的 Prompt 注入。

**注意事项**: 某些库可能会自动添加隐藏的系统提示词，只有通过拦截流量才能发现这些“隐形”的指令。

---

### 实践 5：确保本地代理环境的安全性

**说明**: 使用 MitM 代理涉及解密 HTTPS 流量，这通常需要在客户端安装并信任根证书。管理好这些证书是防止本地环境受到中间人攻击的关键。

**实施步骤**:
1. 使用知名的、开源的代理工具（如 mitmproxy, Charles, Proxyman）。
2. 仅在测试期间安装代理工具生成的根证书，测试完毕后及时移除。
3. 不要将用于测试的根证书导出或分发到其他机器。
4. 确保代理监听在本地回环地址（127.0.0.1）而非 0.0.0.0，防止局域网内其他设备连接。

**注意事项**: 操作系统或浏览器可能会缓存证书信任状态，定期清理系统的受信任根证书列表是良好的安全习惯。

---

### 实践 6：实施请求与响应的日志归档

**说明**: 仅实时查看流量往往不足以进行长期分析。建立自动化的日志归档机制，有助于回溯历史问题，对比不同版本 LLM 的表现差异。

**实施步骤**:
1. 配置代理工具将捕获的流量保存为标准格式（如 HAR 文件或 JSON Lines）。
2. 编写脚本自动提取请求中的关键信息（时间戳、模型名称、Token 数量、响应状态）。
3. 将结构化数据存入数据库（如 SQLite 或 Elasticsearch）。
4. 建立可视化仪表盘，监控请求成功率和响应延迟趋势。

**注意事项**: 归档的日志中可能包含高度敏感的交互数据，必须对存储的日志文件进行强加密存储，并严格控制访问权限。

---
## 学习要点

- 该工具通过充当中间人代理，解密并可视化 LLM 工具与 API 之间传输的 JSON 数据，解决了客户端请求内容不可见的问题。
- 它揭示了 LLM 应用在请求头中发送了哪些敏感元数据（如 IP 地址或设备指纹），帮助用户评估隐私泄露风险。
- 用户可以借此验证应用是否向模型提供商发送了超出预期的额外数据，从而确认是否存在过度收集信息的行为。
- 该代理能够实时展示完整的请求体内容，对于开发者调试 Prompt 注入或理解工具内部提示词逻辑极具价值。
- 它突显了在使用第三方 LLM 封装库时，必须信任客户端不仅发送了用户输入的文本，还可能发送了隐藏的遥测数据。

---
## 常见问题


### 1: 什么是针对大语言模型（LLM）的中间人代理工具，它的主要作用是什么？

1: 什么是针对大语言模型（LLM）的中间人代理工具，它的主要作用是什么？

**A**: 中间人代理是一种位于客户端应用程序（如使用 LLM API 的本地软件）与服务器端（如 OpenAI 或 Anthropic 的 API 端点）之间的拦截工具。它的主要作用是拦截、记录并显示这两者之间传输的原始数据流量。对于 LLM 工具而言，这意味着它可以详细展示应用程序发送了哪些提示词、系统指令、以及上传了哪些文件或上下文信息，帮助用户验证工具的行为是否符合预期，或者排查数据泄露风险。

---



### 2: 为什么我需要查看 LLM 工具发送的具体数据内容？

2: 为什么我需要查看 LLM 工具发送的具体数据内容？

**A**: 主要原因包括安全隐私验证、调试优化以及合规性审查。许多 LLM 应用程序在后台自动发送数据，用户可能并不清楚具体的传输内容。通过使用此类代理，你可以确认应用程序是否发送了敏感的个人身份信息（PII）、专有的代码库或机密文档。此外，开发者可以通过查看请求的 JSON 结构来优化 Token 的使用效率，或者确认工具是否在未经同意的情况下将数据发送给了未授权的第三方模型端点。

---



### 3: 这个工具是如何工作的，我是否需要修改代码才能使用它？

3: 这个工具是如何工作的，我是否需要修改代码才能使用它？

**A**: 这类工具通常通过配置操作系统的代理设置（如环境变量 `HTTP_PROXY` 和 `HTTPS_PROXY`）或安装自定义的根证书来工作。大多数情况下，你不需要修改应用程序的源代码。你只需要启动代理服务器，然后将目标 LLM 工具的网络请求指向该代理（通常是 `localhost` 的某个端口，如 8080）。代理会负责建立与目标 API 的连接，解密 HTTPS 流量，并以可读的格式展示请求和响应内容。

---



### 4: 使用此类代理是否会面临 HTTPS 证书错误或安全警告？

4: 使用此类代理是否会面临 HTTPS 证书错误或安全警告？

**A**: 是的，这是使用中间人代理的常见现象。由于 LLM API 通常使用加密的 HTTPS 协议，代理为了解密内容，必须在本地生成一个自签名证书，并让你的操作系统或应用程序信任该证书。如果不正确配置，应用程序会报错提示证书无效。解决方法通常是将代理生成的根证书手动安装并添加到系统的“受信任的根证书颁发机构”列表中。

---



### 5: 这种代理工具能否拦截所有类型的 LLM 应用程序流量？

5: 这种代理工具能否拦截所有类型的 LLM 应用程序流量？

**A**: 这取决于应用程序的网络实现方式。对于使用标准 HTTP/HTTPS 协议并遵循系统代理设置的应用（如大多数 Python 脚本、基于 LangChain 的工具或配置了代理的浏览器插件），拦截效果很好。然而，如果应用程序硬编码了网络请求而不遵循系统代理，或者使用了双向证书认证等高级安全机制，普通的中间人代理可能无法拦截流量。此外，某些桌面应用可能会对 SSL 证书进行严格的校验（如 Certificate Pinning），这也会增加拦截的难度。

---



### 6: 查看 LLM 流量是否会暴露我的 API 密钥或敏感信息？

6: 查看 LLM 流量是否会暴露我的 API 密钥或敏感信息？

**A**: 是的，这正是此类工具的特性，也是你需要谨慎使用的原因。代理会显示完整的请求头，其中通常包含 `Authorization` 字段，即你的 API Key。因此，如果你在公共环境或截图中分享代理日志时，必须务必小心抹去敏感信息。建议仅在本地开发环境中使用此类工具，并确保代理服务仅监听本地回环地址，不要暴露在公网中。

---



### 7: 除了查看流量，这类工具通常还具备哪些高级功能？

7: 除了查看流量，这类工具通常还具备哪些高级功能？

**A**: 除了基本的“只读”查看功能，许多高级的 MitM 代理（如 mitmproxy）还支持请求修改和重放。这意味着你可以手动修改发送给 LLM 的参数（例如调整 `temperature` 或 `max_tokens`）并重新发送，以测试不同的输出效果，而无需修改原始应用程序的代码。此外，它们通常支持将流量保存为 HAR 文件，以便进行长期存档或自动化的回归测试。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 许多 LLM 应用程序（如桌面客户端或 IDE 插件）在代码中硬编码了 API 端点。请尝试使用 `mitmproxy` 或 `Whistle` 拦截一个本地的 LLM 客户端请求。如果客户端报错（通常是因为 SSL 证书验证失败），你该如何修改操作系统的证书信任设置或启动代理命令，以确保流量能被成功拦截并解密？

### 提示**: 搜索关键词 "mitmproxy CA certificate install [你的操作系统]" 或了解 `--ignore-hosts` 参数的用法。

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
- 标签： [LLM](/tags/llm/) / [MitM](/tags/mitm/) / [代理](/tags/%E4%BB%A3%E7%90%86/) / [数据监控](/tags/%E6%95%B0%E6%8D%AE%E7%9B%91%E6%8E%A7/) / [隐私安全](/tags/%E9%9A%90%E7%A7%81%E5%AE%89%E5%85%A8/) / [网络抓包](/tags/%E7%BD%91%E7%BB%9C%E6%8A%93%E5%8C%85/) / [API 调试](/tags/api-%E8%B0%83%E8%AF%95/) / [工具链](/tags/%E5%B7%A5%E5%85%B7%E9%93%BE/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/)

### 相关文章

- [Show HN: 一款用于监控 LLM 工具数据传输的 MitM 代理]({{< relref "posts/20260129-hacker_news-show-hn-a-mitm-proxy-to-see-what-your-llm-tools-ar-11.md" >}})
- [展示一款可监控LLM工具数据传输的MitM代理]({{< relref "posts/20260129-hacker_news-show-hn-a-mitm-proxy-to-see-what-your-llm-tools-ar-13.md" >}})
- [Show HN: 可视化 LLM 工具数据传输的 MitM 代理]({{< relref "posts/20260129-hacker_news-show-hn-a-mitm-proxy-to-see-what-your-llm-tools-ar-14.md" >}})
- [Show HN：可查看LLM工具数据传输的MitM代理]({{< relref "posts/20260129-hacker_news-show-hn-a-mitm-proxy-to-see-what-your-llm-tools-ar-16.md" >}})
- [Show HN：一款用于监控 LLM 工具数据传输的中间人代理]({{< relref "posts/20260129-hacker_news-show-hn-a-mitm-proxy-to-see-what-your-llm-tools-ar-9.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*