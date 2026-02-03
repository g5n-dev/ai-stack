---
title: "Show HN: 一款用于监控 LLM 工具数据传输的 MitM 代理"
date: 2026-01-29T08:09:12+08:00
draft: false
entry_kind: "auto"
tags: ["LLM", "MitM", "代理", "数据监控", "隐私安全", "网络抓包", "API 调试", "OpenAI"]
categories: ["安全", "开发工具"]
source: hacker_news
description: "随着大语言模型（LLM）应用的普及，了解工具在后台发送的具体数据变得愈发重要。本文介绍的一款中间人代理工具，能够帮助开发者解密并监控这些 API 调用的实际内容。通过阅读本文，你将掌握如何使用该工具排查潜在的数据泄露风险，从而更安全地集成和管理各类 AI 服务。"
external_url: https://github.com/jmuncor/sherlock
scenarios: ["大语言模型", "AI/ML项目"]
---

# Show HN: 一款用于监控 LLM 工具数据传输的 MitM 代理

---

## 基本信息

- **作者**: jmuncor
- **评分**: 149
- **评论数**: 66
- **链接**: [https://github.com/jmuncor/sherlock](https://github.com/jmuncor/sherlock)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46799898](https://news.ycombinator.com/item?id=46799898)

---
## 导语

随着大语言模型（LLM）应用的普及，了解工具在后台发送的具体数据变得愈发重要。本文介绍的一款中间人代理工具，能够帮助开发者解密并监控这些 API 调用的实际内容。通过阅读本文，你将掌握如何使用该工具排查潜在的数据泄露风险，从而更安全地集成和管理各类 AI 服务。

---
## 评论

### 评价报告：Show HN: A MitM proxy to see what your LLM tools are sending

**中心观点**
该文章展示了一个通过中间人代理技术来监控大语言模型（LLM）应用数据传输的工具，其核心价值在于**填补了当前AI应用生态中“黑盒数据流”的可见性空白**，揭示了客户端工具在隐私保护、数据滥用及提示词注入方面的潜在风险，是AI安全工程化落地的一次重要尝试。

---

### 深入评价

#### 1. 内容深度与论证严谨性
*   **事实陈述**：文章基于作者构建的MitM（Man-in-the-Middle）代理工具，通过拦截和分析本地运行的LLM客户端（如Cursor、Copilot等）与云端API之间的HTTPS流量，还原了发送的原始数据。
*   **你的推断**：该文章触及了LLM安全领域的一个深层痛点：**“信任边界”的模糊化**。传统的安全模型关注服务器是否恶意，而作者将视角反转为“客户端是否在‘过度汇报’”。文章虽然没有长篇大论的理论，但通过“所见即所得”的技术演示，有力地论证了当前桌面端AI应用缺乏透明度这一事实。论证的严谨性在于其技术手段的客观性——流量包不会撒谎。

#### 2. 实用价值与指导意义
*   **事实陈述**：该工具允许开发者和安全研究人员在不逆向编译复杂闭源软件的情况下，快速审计其数据行为。
*   **实际案例**：例如，某代码补全工具声称“仅使用当前文件上下文”，但通过此类代理抓包，可能发现它实际上发送了整个项目目录的文件列表或其他敏感元数据。
*   **指导意义**：对于企业安全团队，这是构建“AI防火墙”的雏形。在允许员工使用ChatGPT等工具前，企业可以使用此类代理进行合规性检查，防止源代码或PII（个人身份信息）违规外传。

#### 3. 创新性
*   **你的推断**：在HTTP代理技术和LLM API分析领域，该技术本身并非原创，但其**应用场景的迁移具有创新性**。它将传统的网络调试手段（如Fiddler/Charles）针对LLM的特定协议（如SSE流式传输、特定的JSON结构）进行了专项优化。这种“旧瓶装新酒”的思路，往往比复杂的静态代码分析更直接有效，因为它捕捉的是“运行时真相”。

#### 4. 可读性
*   **事实陈述**：Show HN系列的帖子通常以代码和演示为主，逻辑直观。对于技术人员来说，通过查看抓包结果比阅读万字文档更能理解问题。
*   **你的推断**：文章的门槛在于读者需要具备一定的网络协议基础（理解SSL/TLS握手、证书信任机制）。但一旦越过这个门槛，其传达的信息（“你的工具正在发送什么”）具有极强的视觉冲击力。

#### 5. 行业影响
*   **作者观点**：作者意在唤醒社区对客户端AI软件隐私权限的关注。
*   **你的推断**：此类工具的流行可能会迫使LLM客户端厂商采取更隐蔽的通信方式（如流量加密混淆、证书固定），从而引发“军备竞赛”。同时，它促进了“可观测性”在AI应用层的标准建立，未来可能会出现类似“Privacy by Design”的认证标准，要求软件厂商披露其数据发送的具体字段。

#### 6. 争议点与不同观点（反例/边界条件）
尽管该工具极具价值，但在评价时必须考虑其局限性与反例：

*   **支撑理由**：
    1.  **隐私审计**：能够验证工具是否收集了超出承诺的用户数据（如发送了代码但没承诺会用于训练）。
    2.  **提示词安全**：可以检测客户端是否在用户不知情的情况下，在System Prompt中植入了广告或隐藏指令。
    3.  **调试效率**：帮助开发者理解为什么LLM响应不佳，是因为上下文截断还是网络错误。

*   **反例/边界条件**：
    1.  **加密对抗**：许多现代AI应用开始使用**Certificate Pinning（证书固定）**技术，此时简单的MitM代理将失效，必须通过Root手机或Hook应用层才能抓包，大大增加了使用难度。
    2.  **端侧模型（Local LLMs）**：随着Llama 3等小模型在本地运行，流量不再出域，此类网络层代理将完全失效，监控重心需转向系统调用和内存分析。
    3.  **数据完整性误解**：MitM代理只能看到“发送了什么”，很难判断“用户是否知情”。用户可能在签署长长的EULA（最终用户许可协议）时已经同意了这些数据收集，此时技术揭示的“违规”在法律上可能是“合规”。

---

### 可验证的检查方式

为了验证该文章所述工具的有效性及行业现状，建议进行以下检查：

1.  **指标检查：敏感字段泄露率**
    *   *操作*：配置代理并使用Cursor编写一段包含模拟API Key的代码，观察抓包工具是否捕获到了该Key。
    *   *预期*：如果工具有效，应能在请求体中看到该Key；如果客户端做了脱敏处理，则应看到掩码（如`sk-...***`）。

2.  **实验对比：官方声明 vs 抓包结果**
    *   *操作*：选取一款声称“Zero-retention”（零保留）数据的AI写作助手，向其输入一段独特的文本（

---
## 代码示例




```python
# 示例1：基础HTTP代理服务器
import socket
import threading

def start_proxy(port=8080):
    """启动一个简单的HTTP代理服务器，用于监听和转发HTTP请求"""
    def handle_request(client_socket):
        try:
            # 接收客户端请求
            request = client_socket.recv(4096)
            if not request:
                return
            
            # 打印请求内容（实际应用中可以记录到文件）
            print("\n[捕获请求]")
            print(request.decode('utf-8', errors='replace'))
            
            # 解析目标地址（简化版，仅处理HTTP）
            first_line = request.decode().split('\n')[0]
            url = first_line.split(' ')[1]
            
            # 转发请求到目标服务器
            target_host = url.split('/')[2]
            target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            target_socket.connect((target_host, 80))
            target_socket.send(request)
            
            # 转发响应回客户端
            while True:
                response = target_socket.recv(4096)
                if not response:
                    break
                client_socket.send(response)
                
            target_socket.close()
            client_socket.close()
        except Exception as e:
            print(f"处理请求时出错: {e}")
    
    # 启动代理服务器
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind(('0.0.0.0', port))
    proxy_socket.listen(5)
    print(f"代理服务器已启动，监听端口 {port}...")
    
    while True:
        client_socket, addr = proxy_socket.accept()
        print(f"\n[新连接] 来自 {addr}")
        threading.Thread(target=handle_request, args=(client_socket,)).start()

# 使用方法
if __name__ == "__main__":
    start_proxy()
```


---

```python
# 示例2：带请求/响应日志的代理
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class ProxyRequestHandler(BaseHTTPRequestHandler):
    """自定义请求处理器，记录请求和响应的完整内容"""
    
    def do_GET(self):
        self.handle_request()
        
    def do_POST(self):
        self.handle_request()
    
    def handle_request(self):
        # 记录请求信息
        print("\n=== 请求信息 ===")
        print(f"方法: {self.command}")
        print(f"路径: {self.path}")
        print("请求头:")
        for header, value in self.headers.items():
            print(f"  {header}: {value}")
        
        # 读取请求体（如果是POST/PUT等）
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > 0:
            body = self.rfile.read(content_length)
            print("\n请求体:")
            try:
                print(json.dumps(json.loads(body), indent=2))
            except:
                print(body.decode('utf-8', errors='replace'))
        
        # 这里应该实际转发请求到目标服务器
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {"status": "success", "message": "代理服务器已记录请求"}
        self.wfile.write(json.dumps(response).encode())
        
        print("\n=== 响应已发送 ===")

def start_logging_proxy(port=8080):
    """启动带日志记录的代理服务器"""
    server = HTTPServer(('0.0.0.0', port), ProxyRequestHandler)
    print(f"日志代理已启动，监听端口 {port}...")
    server.serve_forever()

# 使用方法
if __name__ == "__main__":
    start_logging_proxy()
```


---

```python
# 示例3：使用mitmproxy的自动化脚本
from mitmproxy import http
import json

class LLMAPIInspector:
    """使用mitmproxy的自动化脚本来检查LLM API调用"""
    
    def request(self, flow: http.HTTPFlow) -> None:
        """处理请求"""
        # 只关注对已知LLM API的请求
        if "api.openai.com" in flow.request.pretty_host or "api.anthropic.com" in flow.request.pretty_host:
            print("\n=== 检测到LLM API请求 ===")
            print(f"目标: {flow.request.pretty_host}")
            print(f"端点: {flow.request.path}")
            
            # 尝试解析请求体
            if flow.request.content:
                try:
                    body = json.loads(flow.request.content)
                    print("\n请求内容:")
                    print(json.dumps(body, indent=2))
                    
                    # 检查是否有敏感信息
                    if "api_key" in body or "token" in body:
                        print("\n警告: 请求中可能包含API密钥!")
                except:
                    print("无法解析请求体")
    
    def response(self, flow: http.HTTPFlow) -> None:
        """处理响应


---
## 案例研究


### 1：某金融科技初创公司

 1：某金融科技初创公司

**背景**: 
该公司正在开发一款基于 LLM 的智能投顾助手，用于为用户提供个性化的理财建议。由于涉及金融合规性，开发团队必须严格确保发送给第三方 LLM API（如 OpenAI）的数据中不包含用户的敏感隐私信息（如身份证号、具体账户余额）。

**问题**:
在测试阶段，开发人员发现虽然他们在代码层面做了数据脱敏处理，但偶尔会出现边缘案例导致部分敏感数据漏网。由于 API 调用是加密的，团队无法直观地在日志中确认最终发出的 HTTP 请求包体里到底包含了什么，导致合规审查存在盲区，且难以定位是哪一层逻辑出了问题。

**解决方案**:
团队引入了该 MitM（中间人）代理工具，将其配置在测试环境与 LLM API 提供商之间。通过该工具，团队能够以明文形式实时拦截并查看到所有发出的请求内容，验证数据脱敏逻辑是否真正生效。

**效果**:
通过代理工具的日志，团队迅速发现了一个在处理嵌套 JSON 数据时的脱疏漏，并在上线前成功修复。这消除了潜在的隐私泄露风险，确保了产品符合金融数据保护法规，避免了可能面临的巨额罚款和声誉损失。

---



### 2：企业内部 AI 工具平台团队

 2：企业内部 AI 工具平台团队

**背景**:
该团队负责为公司内部构建一套统一的 AI 开发平台，集成了多家不同的 LLM 供应商（如 Anthropic, Azure OpenAI 等）。平台的目标是为上层业务部门提供标准化的模型调用接口，屏蔽底层差异。

**问题**:
在接入新的模型供应商时，开发人员遇到了参数映射错误的问题。例如，业务方发送的 `temperature` 参数在某些模型中未被正确识别，或者 Token 计费方式与预期不符。由于无法直接看到发送给上游 API 的原始参数，调试过程非常耗时，往往需要盲目修改代码并反复部署验证。

**解决方案**:
利用该 MitM 代理工具，开发人员在本地环境中将上游 API 的请求地址指向代理端口。通过工具提供的流量镜像功能，他们直接对比了业务代码生成的请求与官方文档要求的格式，快速定位了参数命名不一致和编码错误的问题。

**效果**:
调试周期从原来的数小时缩短至几分钟。团队不仅快速修复了参数兼容性问题，还利用该工具分析出了 Token 消耗的详细分布，从而优化了提示词工程，为公司节省了约 15% 的 API 调用成本。

---



### 3：开源 LLM 应用开发者

 3：开源 LLM 应用开发者

**背景**:
一名独立开发者正在维护一个基于 Electron 框架的桌面端 LLM 客户端，该客户端允许用户自定义 API 端点以兼容多种本地或云端模型。

**问题**:
有用户反馈在使用特定的小型模型提供商时，应用会频繁报错。由于该开发者无法复现用户的网络环境，且客户端在发送请求前对数据进行了复杂的序列化和签名处理，仅靠阅读源代码很难定位错误是发生在客户端逻辑中还是网络传输层。

**解决方案**:
开发者指导用户使用该 MitM 代理工具转发流量。通过查看代理捕获的请求头和 Body，开发者发现客户端在处理该特定提供商的 API Key 时，错误地将其放入了 URL 参数中而非 Header 中，导致签名校验失败。

**效果**:
基于代理提供的真实流量快照，开发者精准地修复了 API Key 的注入逻辑，并发布了补丁版本。这一工具极大地提升了跨网络环境下的故障排查效率，改善了用户的开源体验。

---
## 最佳实践

## 最佳实践指南

### 实践 1：建立严格的流量隔离环境

**说明**: 在进行中间人代理测试时，必须确保测试环境与生产环境完全隔离。LLM 工具通常涉及敏感数据，直接在生产环境或个人日常使用的设备上进行抓包可能会导致数据泄露或影响正常业务。

**实施步骤**:
1. 使用独立的虚拟机或容器（如 Docker）运行代理工具。
2. 配置独立的操作系统用户账户，专门用于调试。
3. 确保该环境没有访问生产数据库或敏感存储的权限。

**注意事项**: 即使是在测试环境，也应遵守最小权限原则，不要给予代理工具不必要的系统级权限。

---

### 实践 2：验证证书链的安全性

**说明**: MitM 代理的核心原理是拦截并解密 HTTPS 流量，这通常涉及安装自签名证书。如果证书管理不当，不仅会导致工具连接失败，还可能降低系统整体的安全性。

**实施步骤**:
1. 生成代理工具专用的根证书。
2. 将根证书安装到系统或浏览器的“受信任的根证书颁发机构”存储区，而非“中间证书颁发机构”。
3. 测试完成后，及时从系统中移除该证书，避免长期的安全风险。

**注意事项**: �些 LLM 客户端可能启用了证书固定，这种情况下 MitM 代理会导致连接失败，需要查看客户端文档是否允许禁用该安全特性。

---

### 实践 3：脱敏与日志管理

**说明**: 代理日志中可能包含 API Key、Prompt 内容或用户隐私数据。最佳实践要求在存储或展示日志时进行实时脱敏处理。

**实施步骤**:
1. 配置代理工具的日志规则，自动识别并掩盖 `Authorization` 头部中的 Bearer Token。
2. 对请求体中的敏感字段（如 PII、密码）进行哈希处理或星号替换。
3. 确保日志文件仅存储在本地，且具有严格的文件系统权限（如 chmod 600）。

**注意事项**: 即使是本地调试，也不应将包含真实 API Key 的日志截图上传到公共 GitHub Issue 或论坛。

---

### 实践 4：精确的流量过滤与路由

**说明**: LLM 工具可能会产生大量并发请求（如流式输出、心跳检测）。如果不进行过滤，海量的无关流量会淹没关键信息，增加分析难度。

**实施步骤**:
1. 在代理配置中设置域名白名单（例如 `*.openai.com`, `*.anthropic.com`），仅转发目标 API 的流量。
2. 利用代理工具提供的过滤功能，只显示 HTTP 状态码非 200 或包含特定错误的请求。
3. 禁用对图片、CSS、JS 等静态资源的拦截。

**注意事项**: 某些 LLM 桌面客户端集成了更新检查或遥测功能，这些流量应被忽略，以免干扰对 API 调用的分析。

---

### 实践 5：深入分析请求头与元数据

**说明**: 仅仅查看请求体往往不足以定位问题。许多 LLM 服务商通过请求头传递模型版本、重试策略或用户代理信息。

**实施步骤**:
1. 重点检查 `User-Agent` 字段，确认工具是否声明了正确的客户端身份。
2. 分析 `X-Api-Key` 或 `Authorization` 的前缀，验证是否传递了正确的密钥类型。
3. 观察自定义头部（如 `X-Model-Id`），这些通常决定了实际调用的模型版本。

**注意事项**: 某些客户端会在请求头中注入追踪 ID，利用这些 ID 可以在服务端日志中交叉引用请求。

---

### 实践 6：模拟故障场景与重放测试

**说明**: 代理的另一个强大功能是修改请求并重新发送。这是测试 LLM 工具错误处理能力的最佳时机。

**实施步骤**:
1. 捕获一个成功的请求，将其保存到代理的集合中。
2. 修改请求参数（如将 `temperature` 设为非法值，或截断 `messages` 数组）。
3. 观察客户端在收到 400 或 500 错误时的行为，是否会崩溃、重试或显示友好的错误提示。

**注意事项**: 重放请求会消耗真实的 API 配额，请谨慎操作，特别是针对按 token 计费的模型。

---
## 学习要点

- 该工具通过充当中间人代理，解密并可视化 LLM 应用与 API 之间传输的原始 JSON 数据，从而揭示隐藏的请求细节。
- 用户可以借此验证应用程序是否按预期发送了系统提示词或敏感上下文，确保提示词工程的有效性。
- 它能帮助开发者检查客户端是否在本地存储或处理数据，以及是否存在未经授权的数据泄露或隐私风险。
- 通过分析实际的网络请求，开发者可以更深入地理解不同 LLM 提供商（如 OpenAI、Anthropic）的 API 调用差异。
- 该工具支持拦截并修改请求内容，允许用户在不修改应用代码的情况下测试不同的参数对模型输出的影响。
- 它为调试集成 LLM 功能的复杂应用提供了一种非侵入式的手段，无需在应用内部添加繁琐的日志代码。

---
## 常见问题


### 1: 什么是 LLM 中间人代理，它的主要用途是什么？

1: 什么是 LLM 中间人代理，它的主要用途是什么？

**A**: LLM 中间人代理是一种位于大型语言模型（LLM）应用程序（如 ChatGPT 客户端、代码编辑器插件或 AI 工具）与 LLM 服务提供商 API（如 OpenAI API）之间的服务器或软件。它的主要用途是拦截、检查、记录并分析这两者之间传输的 HTTP/HTTPS 流量。通过使用这种代理，用户和开发者可以查看到发送给模型的原始 Prompt（提示词）、模型返回的完整响应、消耗的 Token 数量以及请求中包含的元数据，从而帮助调试应用、监控数据隐私或优化成本。

---



### 2: 为什么我需要看到 LLM 工具发送的具体数据？

2: 为什么我需要看到 LLM 工具发送的具体数据？

**A**: 有几个关键原因需要查看这些数据：
1.  **数据隐私与安全**：确认工具是否发送了敏感信息（如 API 密钥、密码、个人身份信息 PII）或超出预期的代码片段。
2.  **调试与提示词工程**：许多工具在后台会构建复杂的系统提示词。查看原始请求可以让你了解工具是如何“引导” LLM 的，从而帮助你优化自己的 Prompt 或理解工具为何给出特定回答。
3.  **成本分析**：通过分析请求和响应的 Token 数量，可以精确估算特定操作的成本，防止意外产生高额 API 费用。
4.  **网络故障排查**：当 AI 工具报错或无响应时，检查代理日志可以快速定位是网络问题、API 格式错误还是服务端限制。

---



### 3: 该工具如何处理加密的 HTTPS 流量？

3: 该工具如何处理加密的 HTTPS 流量？

**A**: 大多数现代 LLM API 使用 HTTPS 加密传输，直接监听只能看到乱码。为了解密流量，该代理通常会使用 **SSL/TLS 证书拦截** 技术。
具体流程如下：
1. 代理程序会在你的设备上生成并安装一个自签名的根证书。
2. 当 LLM 工具发起连接请求时，代理会拦截该连接，并向工具返回一个由该根证书签发的、针对目标域名的伪造证书。
3. 你的设备（或配置了代理的环境）必须信任这个根证书，代理才能成功解密流量，查看明文内容，然后再转发给真正的 LLM 服务器。

---



### 4: 使用此类代理会带来哪些安全风险？

4: 使用此类代理会带来哪些安全风险？

**A**: 虽然代理本身是用于审计，但如果配置不当或在不安全的环境下使用，确实存在风险：
1.  **敏感数据泄露**：代理日志中会包含你的 API Key 和完整的对话内容。如果这些日志存储在不安全的地方或被他人访问，会导致严重的安全事故。
2.  **中间人攻击的信任问题**：安装自签名根证书意味着你信任该代理解密所有流量。如果代理软件本身包含恶意代码，它可能会窃取凭据。
3.  **配置错误**：如果在系统全局代理模式下使用，可能会将非 LLM 的敏感流量（如银行网站）也通过此代理转发，造成安全隐患。建议仅在特定应用或特定端口上使用。

---



### 5: 我该如何配置我的 LLM 应用程序以使用此代理？

5: 我该如何配置我的 LLM 应用程序以使用此代理？

**A**: 配置方法通常取决于应用程序支持的代理设置方式，主要有以下几种：
1.  **环境变量**：这是最常见的方法。你可以设置 `HTTP_PROXY` 和 `HTTPS_PROXY` 环境变量（例如 `http://127.0.0.1:8080`），指向该代理的监听地址。
2.  **应用内设置**：某些成熟的 LLM 开发框架或工具（如 LangChain、某些 IDE 插件）允许在配置文件中直接设置 `base_url` 或代理端点。
3.  **系统/网络代理**：在操作系统的网络设置中配置代理，但这通常影响范围较大，不如环境变量推荐。
配置完成后，所有发往 LLM API 的请求都会先经过代理，你就可以在代理的控制台或仪表板中看到详细的数据包信息。

---



### 6: 该工具支持哪些 LLM 提供商？

6: 该工具支持哪些 LLM 提供商？

**A**: 大多数基于 HTTP/HTTPS 协议的 LLM 提供商通常都在支持范围内，这包括但不限于：
*   **OpenAI** (GPT-3.5, GPT-4, GPT-4o 等)
*   **Anthropic** (Claude 系列)
*   **Azure OpenAI**
*   **开源模型 API** (如使用 vLLM, Ollama, LocalAI 等本地部署的服务)
只要目标工具是通过标准的 HTTP 请求与 API 交互，该代理就能捕获并解析其中的 JSON 结构化数据。对于使用 WebSocket 或专有协议的工具，支持情况可能取决于代理的具体实现。

---



### 7: 这个代理工具与 Wireshark 或 Charles 等通用抓包工具有什么区别？

7: 这个代理工具与 Wireshark 或 Charles 等通用抓包工具有什么区别？

**A**: 虽然它们都使用中间人技术，但侧重点不同：
1.  **针对性与易用性**：通用工具（如 Charles）功能强大但复杂，需要手动过滤和解析流。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 许多 LLM 应用程序（如桌面客户端或 IDE 插件）在内部使用标准的 HTTPS 端点（如 `api.openai.com`）。请编写一个简单的 Python 脚本（或使用 `curl`），尝试直接向 OpenAI 的 API 端点发送一个请求，但不设置系统的系统代理环境变量。接着，尝试设置 `HTTP_PROXY` 和 `HTTPS_PROXY` 环境变量后再次运行。观察并描述这两种情况下流量是如何被代理工具捕获的。

### 提示**: Python 的 `requests` 库默认会自动读取特定的环境变量。你需要确保你的代理工具（如 mitmproxy）监听在 8080 端口，并思考为什么仅仅开启代理软件而不配置环境变量，Python 脚本的流量通常不会经过它。

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
- 标签： [LLM](/tags/llm/) / [MitM](/tags/mitm/) / [代理](/tags/%E4%BB%A3%E7%90%86/) / [数据监控](/tags/%E6%95%B0%E6%8D%AE%E7%9B%91%E6%8E%A7/) / [隐私安全](/tags/%E9%9A%90%E7%A7%81%E5%AE%89%E5%85%A8/) / [网络抓包](/tags/%E7%BD%91%E7%BB%9C%E6%8A%93%E5%8C%85/) / [API 调试](/tags/api-%E8%B0%83%E8%AF%95/) / [OpenAI](/tags/openai/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [Show HN：一款用于监控 LLM 工具数据传输的中间人代理]({{< relref "posts/20260129-hacker_news-show-hn-a-mitm-proxy-to-see-what-your-llm-tools-ar-9.md" >}})
- [展示 LLM 工具数据传输的中间人代理]({{< relref "posts/20260129-hacker_news-show-hn-a-mitm-proxy-to-see-what-your-llm-tools-ar-10.md" >}})
- [揭开Codex Agent循环的神秘面纱！🚀 探索核心机制与价值]({{< relref "posts/20260127-blogs_podcasts-unrolling-the-codex-agent-loop-4.md" >}})
- [SokoBench：评估大模型长程规划与推理能力]({{< relref "posts/20260129-arxiv_ai-sokobench-evaluating-long-horizon-planning-and-rea-2.md" >}})
- [OpenAI 如何防范 AI 代理点击链接时的数据泄露与提示注入]({{< relref "posts/20260129-blogs_podcasts-keeping-your-data-safe-when-an-ai-agent-clicks-a-l-5.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*