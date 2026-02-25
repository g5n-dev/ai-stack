---
title: "通过 CLI 优化降低 MCP 运行成本"
date: 2026-02-25T22:01:33+08:00
draft: false
entry_kind: "auto"
tags: ["MCP", "CLI", "成本优化", "Anthropic", "模型上下文协议", "工具集成", "命令行", "架构设计"]
categories: ["AI 工程", "开发工具"]
source: hacker_news
description: "在资源受限的环境中运行 Model Context Protocol (MCP) 服务器往往意味着高昂的计算成本。本文探讨了如何通过命令行界面 (CLI) 优化 MCP 的部署，从而有效降低对硬件资源的需求。通过阅读本文，读者将掌握具体的实施步骤，在保持系统功能完整的同时，显著减少基础设施的开支。"
external_url: https://kanyilmaz.me/2026/02/23/cli-vs-mcp.html
scenarios: ["命令行工具"]
---

# 通过 CLI 优化降低 MCP 运行成本

---

## 基本信息

- **作者**: thellimist
- **评分**: 18
- **评论数**: 17
- **链接**: [https://kanyilmaz.me/2026/02/23/cli-vs-mcp.html](https://kanyilmaz.me/2026/02/23/cli-vs-mcp.html)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47157398](https://news.ycombinator.com/item?id=47157398)

---
## 导语

在资源受限的环境中运行 Model Context Protocol (MCP) 服务器往往意味着高昂的计算成本。本文探讨了如何通过命令行界面 (CLI) 优化 MCP 的部署，从而有效降低对硬件资源的需求。通过阅读本文，读者将掌握具体的实施步骤，在保持系统功能完整的同时，显著减少基础设施的开支。

---
## 评论

**文章中心观点**
文章主张通过命令行界面（CLI）而非图形界面（GUI）或浏览器交互的方式来运行模型上下文协议（MCP）服务器，能够显著降低资源消耗、提升性能，并增强大模型（LLM）工具调用的稳定性与可控性。

**支撑理由与边界条件分析**

1.  **资源消耗与性能优化（事实陈述 / 作者观点）**
    *   **支撑理由**：文章指出，传统的 MCP 部署往往依赖于浏览器扩展或桌面应用（如 Claude Desktop）的 GUI 交互层，这引入了额外的内存开销和渲染成本。通过 CLI 直接启动 MCP 服务，可以剥离繁重的 UI 渲染逻辑，仅保留核心的数据传输功能。
    *   **技术深度**：从技术角度看，这实际上是去除了“中间件”的冗余。LLM 调用本地工具时，若通过 GUI 中转，往往涉及 JSON 序列化/反序列化的多次转换以及进程间通信（IPC）的额外开销。CLI 模式通常允许更直接的 Stdin/Stdout 通信或本地 Socket 通信，从而降低延迟。
    *   **边界条件/反例**：这种优化主要针对的是**客户端**的资源占用。如果 MCP 服务器本身（例如连接到一个昂贵的数据库 API）是计算密集型的，CLI 并不能减少后端的计算成本。此外，对于非技术型用户，CLI 缺乏可视化的状态反馈（如进度条、错误弹窗），可能导致排查问题时的“认知成本”反而上升。

2.  **可观测性与调试能力（事实陈述 / 你的推断）**
    *   **支撑理由**：CLI 环境天然适合日志记录和管道操作。作者暗示，通过 CLI 运行 MCP 可以更方便地捕获原始输出，结合 Unix 管道（Pipes）与其他开发工具链集成。
    *   **技术深度**：在 GUI 模式下，调试工具调用往往需要打开特定的“开发者工具”窗口，查看被封装在 WebSocket 消息中的日志。而在 CLI 下，开发者可以直接利用 `jq`、`grep` 等标准工具实时分析 MCP 协议的请求与响应流。这对于协议层面的错误排查（如 Schema 不匹配）具有极高的实用价值。
    *   **边界条件/反例**：CLI 的日志输出往往是未经处理的文本流，当并发请求量较大时，终端刷屏会导致日志难以阅读。相比之下，GUI 可以提供结构化的、折叠的日志视图，在处理复杂交互链时可能更直观。

3.  **部署灵活性与容器化（作者观点 / 行业趋势）**
    *   **支撑理由**：CLI 工具更容易被容器化（Docker）和无头服务化。文章暗示这使得 MCP 服务更容易部署在服务器端或轻量级设备上，而非必须绑定在用户的本地桌面环境中。
    *   **技术深度**：这是“Serverless”思维的体现。如果 MCP 服务器仅通过 CLI 暴露接口，它可以作为一个微服务常驻在后台，通过网络被多个 LLM 客户端复用，打破了“一个客户端绑定一套工具”的孤岛效应。
    *   **边界条件/反例**：CLI 模式通常意味着失去了本地沙箱的某种“物理隔离”。如果 MCP 工具具有高危操作（如删除文件），CLI 的直接执行权限可能带来更大的安全风险，而 GUI 往往会弹出二次确认窗口。

**综合评价**

1.  **内容深度：**
    文章触及了 AI Agent 基础设施建设中一个常被忽视的痛点：**客户端臃肿**。目前的 LLM 客户端（如 Cursor, Claude Desktop）越来越像浏览器，承载了过多的渲染逻辑。文章提出的“CLI 优先”不仅是成本优化，更是一种回归 Unix 哲学（“做好一件事”）的工程修正。论证虽然偏向工程实践，缺乏严谨的基准测试数据，但逻辑链条清晰。

2.  **实用价值：**
    对于开发者而言，价值极高。在构建私有化 MCP 服务器时，CLI 模式是集成到 CI/CD 流程或后端服务的必经之路。它解决了 GUI 应用难以在服务器环境运行的问题。

3.  **创新性：**
    观点虽不激进，但在当前“万物皆 App”的趋势下，提出回归 CLI 是一种务实的反讽。它强调了 MCP 协议本身应该是传输层无关的。

4.  **行业影响：**
    这篇文章可能会推动 MCP 社区开发更轻量级的 SDK，促使厂商将 MCP Server 的运行环境与客户端解耦。长期来看，有利于 MCP 协议在边缘计算设备上的普及。

5.  **争议点：**
    *   **易用性 vs 效率**：降低成本不应以牺牲易用性为代价。如何让 CLI 工具对普通用户友好（例如提供一键安装脚本），是该方法能否普及的关键。
    *   **标准化的缺失**：目前的 MCP CLI 实现可能各家各异，缺乏统一的连接管理标准。

**实际应用建议**

1.  **开发环境隔离**：建议在 Docker 容器中运行 MCP CLI 工具，通过 `docker exec` 交互，避免污染宿主机环境，同时利用容器的资源限制（CPU/Memory）来控制 LLM 工具的滥用。
2.  **日志中间件**：在 CLI 启动命令前加入 `tee` 或自定义的日志脚本，将所有 LLM 与工具的交互记录持久化存储，用于后续的分析和审计。
3.  **守护进程

---
## 代码示例




```python
# 示例1：批量处理MCP请求以降低API调用成本
import requests
import time

def batch_process_mcp_requests(requests_list, batch_size=10):
    """
    将多个MCP请求批量处理以减少API调用次数
    :param requests_list: 待处理的MCP请求列表
    :param batch_size: 每批处理的请求数量
    :return: 批处理结果列表
    """
    results = []
    for i in range(0, len(requests_list), batch_size):
        batch = requests_list[i:i+batch_size]
        # 模拟批量API调用
        batch_response = {"batch_id": i//batch_size, "results": [f"processed_{req}" for req in batch]}
        results.extend(batch_response["results"])
        time.sleep(0.1)  # 避免触发速率限制
    return results

# 使用示例
requests = ["req1", "req2", "req3", "req4", "req5"]
processed = batch_process_mcp_requests(requests)
print(processed)
```




```python
# 示例2：实现本地缓存减少重复MCP调用
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_mcp_call(param):
    """
    带缓存的MCP调用函数
    :param param: 调用参数
    :return: 模拟的API响应
    """
    # 模拟API调用
    return f"response_for_{param}"

# 使用示例
print(cached_mcp_call("test"))  # 第一次调用会执行实际请求
print(cached_mcp_call("test"))  # 第二次调用直接返回缓存结果
```




```python
# 示例3：异步并发处理MCP请求
import asyncio
import aiohttp

async def async_mcp_call(session, url, params):
    """
    异步MCP调用函数
    :param session: aiohttp会话
    :param url: API地址
    :param params: 请求参数
    :return: 响应结果
    """
    async with session.get(url, params=params) as response:
        return await response.json()

async def concurrent_mcp_requests(requests_data):
    """
    并发处理多个MCP请求
    :param requests_data: 请求数据列表
    :return: 所有响应结果
    """
    async with aiohttp.ClientSession() as session:
        tasks = [async_mcp_call(session, req["url"], req["params"]) for req in requests_data]
        return await asyncio.gather(*tasks)

# 使用示例
requests_data = [
    {"url": "https://api.example.com/mcp", "params": {"id": 1}},
    {"url": "https://api.example.com/mcp", "params": {"id": 2}},
]
# 注意：实际运行需要有效的API端点
# results = asyncio.run(concurrent_mcp_requests(requests_data))
```


---
## 案例研究


### 1：AI 辅助编程工具的本地化部署

 1：AI 辅助编程工具的本地化部署

**背景**:
某初创公司开发了一款基于大语言模型（LLM）的代码补全插件。该插件最初完全依赖云端 API（如 OpenAI GPT-4）进行推理，每次代码补全请求都需要通过网络传输上下文代码并等待响应。

**问题**:
随着用户量增长，云端 API 调用成本（Token 计费）急剧上升，成为公司最大的运营支出。此外，云端请求存在 200-500ms 的网络延迟，严重影响了用户的编程体验和流畅度。对于涉及私有代码库的场景，直接发送到云端还存在数据安全合规的风险。

**解决方案**:
技术团队决定引入 Model Context Protocol (MCP) 并将其与本地运行的开源模型（如 Llama 3 或 CodeLlama）相结合。他们开发了一个轻量级的命令行界面（CLI）工具，作为 MCP 的宿主程序。该 CLI 工具直接在开发者的本地机器上启动推理引擎（利用本地 GPU 或 CPU），通过标准接口接收来自 IDE 插件的代码上下文，并在本地完成推理。

**效果**:
1. **成本归零**：完全消除了云端 API 的 Token 调用费用，将边际成本降低为 0（仅消耗本地电力和算力）。
2. **延迟降低**：补全响应时间从网络延迟降低至本地推理的 50-100ms，体验接近原生 IDE。
3. **数据隐私**：代码上下文不再出域，完美解决了企业客户的数据安全顾虑。

---



### 2：企业级知识库的智能检索

 2：企业级知识库的智能检索

**背景**:
一家大型跨国企业的内部 IT 支持团队维护着包含数万页文档的 Wiki 和知识库。员工在查找解决方案时，往往需要手动搜索关键词并阅读大量无关文档。

**问题**:
部署一套基于 RAG（检索增强生成）的智能问答系统需要高昂的云端向量数据库和 Embedding 模型调用费用。此外，由于企业内部网络策略，将所有内部文档通过 API 发送给外部 LLM 供应商进行审核和生成存在严重的合规阻碍。

**解决方案**:
团队构建了一个基于 MCP 的 CLI 工具，该工具集成了本地 Embedding 模型和轻量级向量数据库（如 SQLite-VSS 或 Chroma 的本地模式）。员工可以通过命令行输入问题，CLI 工具在本地完成文档的向量化检索，并调用本地运行的小型参数模型（Llama 3-8B）生成基于上下文的答案，整个过程完全在离线或内网环境中闭环运行。

**效果**:
1. **大幅节省开支**：避免了高频次调用云端 Embedding API 和 LLM API 的费用，相比云端 SaaS 方案节省了 90% 以上的运营成本。
2. **合规性提升**：数据从未离开企业内网，满足了严格的 ISO 27001 和 GDPR 合规要求。
3. **响应可控**：即使在外部网络断开的情况下，员工依然可以高效检索知识库，保证了业务连续性。

---



### 3：自动化运维脚本生成器

 3：自动化运维脚本生成器

**背景**:
某 DevOps 团队负责管理数千台服务器的配置和部署。工程师经常需要编写复杂的 Bash 或 PowerShell 脚本来处理特定的系统状态。

**问题**:
虽然使用云端 LLM 可以生成这些脚本，但由于涉及生产环境的敏感配置信息，工程师不能直接将系统状态数据粘贴到公网 AI 聊天窗口。此外，频繁的脚本生成请求在高峰期会产生显著的 API 费用。

**解决方案**:
团队开发了一套名为 "ops-gen" 的内部 CLI 工具，集成了 MCP 服务器端。该工具允许工程师在终端直接输入自然语言指令（例如：“重启所有 CPU 占用超过 80% 的 Nginx 服务”）。CLI 工具捕获当前系统上下文，通过 MCP 协议传递给部署在运维跳板机上的本地 LLM，模型直接在本地生成可执行的脚本并展示给工程师确认，或直接执行。

**效果**:
1. **安全性增强**：敏感系统信息无需传输至云端，防止了潜在的数据泄露。
2. **成本优化**：利用公司现有的闲置服务器算力运行本地模型，将脚本生成的运营成本降至最低。
3. **效率提升**：工程师无需在浏览器和终端之间切换，直接在 CLI 工作流中完成意图到脚本的转化，大幅提升了运维操作的自动化率和速度。

---
## 最佳实践

## 最佳实践指南

### 实践 1：使用本地 MCP 服务器替代云端 API

**说明**: 
MCP (Model Context Protocol) 允许通过 CLI 连接到本地运行的模型服务，而非必须调用 OpenAI 或 Anthropic 等昂贵的云端 API。通过在本地或廉价 VPS 上部署兼容的 LLM 服务（如 Ollama, LocalAI），可以显著降低 Token 消耗成本。

**实施步骤**:
1. 安装本地推理框架，例如 `ollama pull llama3`。
2. 配置 MCP 客户端环境变量，将 `api_base` 指向本地端点（如 `http://localhost:11434`）。
3. 修改调用脚本，将模型参数指定为本地模型名称。

**注意事项**: 
本地模型的推理能力通常弱于 GPT-4，建议在非关键任务或简单摘要/提取任务中使用。

---

### 实践 2：实施严格的 Token 预算与截断策略

**说明**: 
上下文窗口直接与成本挂钩。在 CLI 交互中，长篇上下文（如代码库或长文档）会迅速消耗 Token。通过 CLI 工具（如 `sed` 或 `awk`）预处理数据，仅发送模型所需的特定片段，可大幅节省费用。

**实施步骤**:
1. 在发送请求前，使用 CLI 命令统计 Token 数量（例如利用 `tiktoken` 的 CLI 封装）。
2. 设定硬性限制，例如仅发送文件的前 2000 行或最后 1000 行。
3. 编写 Shell 脚本封装逻辑：`head -n 1000 large_file.log | mcp_client --process`。

**注意事项**: 
截断数据可能会导致模型丢失上下文中的关键信息，需确保截断位置具有逻辑完整性。

---

### 实践 3：利用 CLI 进行批量处理与缓存

**说明**: 
交互式对话往往伴随着重复的系统提示词。通过 CLI 编写脚本，将多个 Prompt 打包一次性提交（批处理），并利用本地文件系统缓存常见问题的回答，避免重复计费。

**实施步骤**:
1. 将所有待处理问题写入一个文本文件 `batch_prompts.txt`。
2. 编写脚本读取文件并构造单次 API 请求（如果模型支持多轮对话批处理）。
3. 建立简单的键值存储（如使用 `sqlite3` 或 JSON 文件），在请求前检查是否已有相同 Prompt 的结果。

**注意事项**: 
批处理可能会受到 API 的速率限制，需在脚本中加入重试和退避逻辑。

---

### 实践 4：优化 Prompt 结构以减少轮次

**说明**: 
多轮对话是成本的主要来源之一。在 CLI 环境下，应精心设计 Prompt，使其包含尽可能多的上下文和指令，力求通过“零样本”或“少样本”一次性完成任务，避免反复追问。

**实施步骤**:
2. 在 CLI 中使用变量替换将模板与具体数据结合：`cat prompt_template.txt | sed "s/{{DATA}}/$actual_data/g" | mcp_client`。
3. 测试并迭代 Prompt，直到模型能在一个回复中给出满意结果。

**注意事项**: 
过长的 Prompt 会增加单次输入成本，需要在“详细指令”和“输入长度”之间找到平衡点。

---

### 实践 5：选择高性价比的小参数模型

**说明**: 
并非所有任务都需要旗舰模型。对于代码补全、日志分析或格式化等任务，通过 CLI 切换到更便宜的小型模型（如 GPT-3.5-Turbo 或 Llama-3-8B），成本可降低 90% 以上。

**实施步骤**:
1. 分析任务复杂度，区分“创意/推理类”和“模式匹配/提取类”任务。
2. 在 CLI 配置文件中设置别名，例如 `alias mcp_cheap='mcp_client --model=gpt-3.5-turbo'` 和 `alias mcp_smart='mcp_client --model=gpt-4'`。
3. 在日常高频操作中默认使用 `mcp_cheap`。

**注意事项**: 
需建立自动化测试集，定期验证小模型在特定任务上的输出质量，防止劣币驱逐良币。

---

### 实践 6：使用流式输出提前终止

**说明**: 
在某些场景下（如生成代码或列表），模型可能在生成初期就已经给出了足够的信息，或者生成了错误的内容。通过 CLI 启用流式传输，并编写脚本监控输出，一旦满足条件即可中断连接，节省未生成的 Token。

**实施步骤**:
1. 在 MCP 客户端配置中启用 `stream: true` 模式。
2. 编写包装脚本，逐行读取输出流。
3. 设定终止条件（如检测到特定关键词、达到行数限制或错误标记），一旦触发立即调用 `SIGINT` 或 `curl` 的断开机制终止请求。

**注意事项**: 
强制

---
## 学习要点

- 通过命令行界面（CLI）直接运行 MCP 服务器，可以避免部署额外的 API 服务，从而显著降低运行成本。
- 利用本地脚本或工具直接处理数据请求，能够减少对昂贵云服务的依赖，提升处理效率。
- 这种方法特别适合轻量级任务和开发测试环境，能够快速验证概念而无需投入大量资源。
- CLI 集成 MCP 的方式简化了部署流程，使得开发者可以更专注于核心逻辑的实现。
- 通过优化 MCP 的调用方式，可以在保持功能完整性的同时，大幅降低整体运营开销。

---
## 常见问题


### 1: 什么是 MCP，以及它为什么会产生费用？

1: 什么是 MCP，以及它为什么会产生费用？

**A**: MCP 是 Model Context Protocol（模型上下文协议）的缩写，它是一种开放标准，旨在帮助 AI 应用程序与外部数据源和工具进行连接。当您使用 MCP 服务器（例如通过 Claude Desktop 或其他兼容客户端）时，AI 模型需要读取 MCP 提供的文件或数据库内容。这个过程会消耗 Token（输入 Token），因为数据被发送给了大语言模型（LLM）。如果频繁交互或处理大量上下文，这些 Token 的消耗会迅速累积，导致 API 使用成本增加。

---



### 2: 如何通过 CLI（命令行界面）来降低 MCP 的使用成本？

2: 如何通过 CLI（命令行界面）来降低 MCP 的使用成本？

**A**: 通过 CLI 使用 MCP 的核心思路是**绕过图形界面（GUI）的频繁轮询和中间处理**。在传统的 GUI 模式（如 Claude Desktop）中，客户端可能会频繁检查服务器状态或在后台进行不可见的 Token 消耗。而使用 CLI（例如直接运行 Python 脚本或使用 `mcp-cli` 等工具），您可以：
1.  **按需调用**：仅在需要时执行一次命令，获取结果后结束，而不是保持长连接。
2.  **精准控制**：手动指定需要读取的文件范围，避免 AI 自动扫描整个目录。
3.  **本地预处理**：在将数据发送给 LLM 之前，利用 CLI 工具在本地进行过滤或格式化，只发送最精简的有效数据，从而大幅减少输入 Token 的数量。

---



### 3: 使用 CLI 方式操作 MCP 是否需要很强的编程能力？

3: 使用 CLI 方式操作 MCP 是否需要很强的编程能力？

**A**: 这取决于您使用的具体工具。虽然 MCP 本身是基于 JSON-RPC 的协议，直接编写原始代码需要一定的编程知识，但目前社区已经出现了许多封装好的 CLI 工具（如 `mcp-client-cli` 或相关 Python 库）。这些工具通常允许用户通过简单的命令行参数（如 `mcp-cli read ./path/to/file`）来与服务器交互。基本的终端操作能力（如 `cd`、`ls`）通常是足够的，但为了实现极致的成本优化，编写简单的脚本来自动化这些流程会更有帮助。

---



### 4: 除了 CLI，还有哪些方法可以降低 MCP 带来的 Token 消耗？

4: 除了 CLI，还有哪些方法可以降低 MCP 带来的 Token 消耗？

**A**: 除了使用 CLI 替代 GUI 之外，还可以采取以下策略：
1.  **优化资源访问**：在 MCP 配置文件中，尽量缩小允许访问的目录范围，避免将整个根目录或庞大的 node_modules 暴露给 AI。
2.  **使用上下文压缩**：某些 MCP 服务器支持智能索引或向量化搜索，确保只检索与当前问题最相关的片段，而不是全量导入。
3.  **调整系统提示词**：明确指示 AI 仅在必要时才调用 MCP 工具，而不是在每个回合都默认检查上下文。

---



### 5: 切换到 CLI 模式会影响 AI 回答的质量吗？

5: 切换到 CLI 模式会影响 AI 回答的质量吗？

**A**: 通常不会影响质量，甚至可能有所提高。通过 CLI，您可以更精确地控制输入给 AI 的上下文信息，减少噪音（无关的文件内容）。这意味着 AI 能够专注于更相关的数据，从而可能生成更准确的回复。唯一的缺点是丧失了 GUI 的便捷性，您需要手动将 CLI 获取的数据复制粘贴回对话窗口，或者编写脚本将两者串联起来。

---



### 6: 这种方法适用于所有支持 MCP 的 AI 平台（如 Claude、Anthropic API 等）吗？

6: 这种方法适用于所有支持 MCP 的 AI 平台（如 Claude、Anthropic API 等）吗？

**A**: 是的。MCP 是一个开放协议，本身并不绑定特定的平台。无论您是使用 Claude Desktop、官方 API 还是其他集成了 MCP 的客户端，通过 CLI 直接与 MCP 服务器通信并获取数据，然后将这些数据作为 Prompt 的一部分发送给模型，这一逻辑是通用的。这是一种通过改变“数据获取方式”来优化成本的通用手段。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单] 基础环境搭建与协议验证

### 问题**:

### 在不使用任何现成 MCP Server SDK 的情况下，仅使用标准输入和标准输出，编写一个最简单的命令行脚本（可以使用 Bash、Python 或 Node.js）。该脚本需要能够接收 JSON-RPC 请求并返回一个静态的响应（例如响应 `initialize` 请求）。请验证你的脚本是否能够成功与一个 MCP Client（如 Inspector 或 Model Context Protocol 客户端）完成握手。

### 提示**:

---
## 引用

- **原文链接**: [https://kanyilmaz.me/2026/02/23/cli-vs-mcp.html](https://kanyilmaz.me/2026/02/23/cli-vs-mcp.html)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47157398](https://news.ycombinator.com/item?id=47157398)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/)
- 标签： [MCP](/tags/mcp/) / [CLI](/tags/cli/) / [成本优化](/tags/%E6%88%90%E6%9C%AC%E4%BC%98%E5%8C%96/) / [Anthropic](/tags/anthropic/) / [模型上下文协议](/tags/%E6%A8%A1%E5%9E%8B%E4%B8%8A%E4%B8%8B%E6%96%87%E5%8D%8F%E8%AE%AE/) / [工具集成](/tags/%E5%B7%A5%E5%85%B7%E9%9B%86%E6%88%90/) / [命令行](/tags/%E5%91%BD%E4%BB%A4%E8%A1%8C/) / [架构设计](/tags/%E6%9E%B6%E6%9E%84%E8%AE%BE%E8%AE%A1/)
- 场景： [命令行工具](/scenarios/%E5%91%BD%E4%BB%A4%E8%A1%8C%E5%B7%A5%E5%85%B7/)

### 相关文章

- [使用MCP将外部工具集成至Amazon Quick Agents的六步指南]({{< relref "posts/20260222-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--3.md" >}})
- [使用MCP集成外部工具至Amazon Quick Agents的实操指南]({{< relref "posts/20260223-blogs_podcasts-integrate-external-tools-with-amazon-quick-agents--4.md" >}})
- [🚀Claude.ai重大更新！Anthropic发布MCP Apps开放规范]({{< relref "posts/20260128-blogs_podcasts-ainews-anthropic-launches-the-mcp-apps-open-spec-i-3.md" >}})
- [Anthropic 发布 MCP Apps 开放标准，定义富生成式 UI 规范]({{< relref "posts/20260129-blogs_podcasts-ainews-anthropic-launches-the-mcp-apps-open-spec-i-9.md" >}})
- [Claude Code 发布：面向基础设施的编程工具]({{< relref "posts/20260205-hacker_news-claude-code-for-infrastructure-7.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*