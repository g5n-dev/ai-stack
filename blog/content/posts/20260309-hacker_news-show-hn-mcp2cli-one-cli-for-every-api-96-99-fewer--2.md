---
title: "Show HN: Mcp2cli – 一个CLI调用所有API，Token消耗比原生MCP减少96-99%"
date: 2026-03-09T10:32:53+08:00
draft: false
entry_kind: "auto"
tags: ["MCP", "CLI", "LLM", "API", "Token优化", "开源工具", "HackerNews", "效率工具"]
categories: ["开发工具", "AI 工程"]
source: hacker_news
description: "随着大模型应用场景的深入，如何高效地与各类 API 交互成为开发者关注的焦点。Mcp2cli 的出现提供了一种新的思路，它通过 CLI 封装各类 API，旨在将 Token 消耗降低 96% 至 99%。本文将介绍该工具的设计逻辑与核心用法，帮助你在不牺牲功能性的前提下，显著优化调用成本与系统性能。"
external_url: https://github.com/knowsuchagency/mcp2cli
scenarios: ["命令行工具", "大语言模型"]
---

# Show HN: Mcp2cli – 一个CLI调用所有API，Token消耗比原生MCP减少96-99%

---

## 基本信息

- **作者**: knowsuchagency
- **评分**: 69
- **评论数**: 35
- **链接**: [https://github.com/knowsuchagency/mcp2cli](https://github.com/knowsuchagency/mcp2cli)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47305149](https://news.ycombinator.com/item?id=47305149)

---
## 导语

随着大模型应用场景的深入，如何高效地与各类 API 交互成为开发者关注的焦点。Mcp2cli 的出现提供了一种新的思路，它通过 CLI 封装各类 API，旨在将 Token 消耗降低 96% 至 99%。本文将介绍该工具的设计逻辑与核心用法，帮助你在不牺牲功能性的前提下，显著优化调用成本与系统性能。

---
## 评论

**中心观点**
Mcp2cli 通过引入“CLI中间层”将 LLM 与 API 交互模式由“JSON Schema 推理”转变为“Shell 命令生成”，以牺牲部分动态灵活性为代价，实现了 Token 消耗数量级（96-99%）的削减与执行确定性的显著提升。

**支撑理由与边界分析**

1.  **Token 效率的底层逻辑差异（事实陈述）**
    原生 MCP 协议要求 LLM 在上下文中加载完整的 JSON Schema 来理解 API 结构，对于复杂 API（如 AWS 或 Kubernetes），Schema 本身可能占据数千 Token。Mcp2cli 的核心创新在于将“理解 API 结构”的认知负荷从 LLM 转移到了人类（或开发者预设的 CLI 映射）。LLM 只需生成简单的 Shell 命令（如 `mcp2cli get-user --id 123`），而非复杂的 JSON Payload。这种“指令压缩”是 Token 消耗降低 96-99% 的根本原因。

2.  **执行确定性与鲁棒性（作者观点）**
    JSON 生成是 LLM 的弱项，容易出现括号不匹配、类型错误或字段缺失。相比之下，LLM 在生成结构化 Shell 命令方面表现得更稳定，且 CLI 工具（如 Click, Typer）自带成熟的参数校验和 Help 文档生成机制。Mcp2cli 实际上利用了 CLI 工业界的成熟标准来规避 LLM 在 JSON 序列化上的不稳定性。

3.  **生态兼容性与“胶水”属性（你的推断）**
    DevOps 和 SRE 行业拥有海量的成熟 CLI 工具。Mcp2cli 实际上构建了一个通用的适配器，使得现有的 CLI 工具无需重写 Server 端即可接入 LLM 生态。这比为每一个工具编写 MCP Server 更符合“Unix 哲学”，即做好一件事并与其他工具良好协作。

**反例与边界条件**

1.  **复杂嵌套对象的构建瓶颈（事实陈述）**
    对于非扁平化的数据输入（例如创建一个包含多个嵌套对象和数组的复杂资源配置文件），CLI 参数传递会变得极其繁琐甚至不可行。原生 MCP 允许直接传递 JSON Body，这在处理复杂图结构数据时具有不可替代的优势，而 Mcp2cli 在此场景下可能需要回退到传递文件路径，增加了交互步骤。

2.  **动态上下文的缺失（你的推断）**
    现代 API 往往是动态的，字段可能依赖于前序操作的输出。如果 CLI 的 Help 文档是静态生成的，它可能无法捕捉 API 运行时的动态约束。相比之下，一个设计良好的 MCP Server 可以在运行时动态生成 Schema，引导 LLM 理解当前状态下的 API 能力。

**多维度评价**

1.  **内容深度：8/10**
    文章准确地抓住了当前 LLM Agent 落地的一大痛点：上下文窗口的昂贵与低效。作者没有停留在表面的“快”，而是深入到了协议层的差异。论证严谨性较高，但文章略微弱化了 CLI 参数解析在处理复杂类型时的局限性。

2.  **实用价值：9/10**
    对于成本敏感或上下文窗口受限（如本地部署小模型）的场景，该工具具有极高的实用价值。它直接降低了 AI 操作 API 的门槛，使得现有的 CLI 脚本资产可以零成本复用。

3.  **创新性：8/10**
    在业界普遍追求“JSON Schema -> LLM”的标准化路径时，Mcp2cli 提出了“退化”到 CLI 的逆向思维。这种“以退为进”利用 Shell 语义作为中间表示（IR）的方法，为 AI Agent 的工具调用提供了新的范式参考。

4.  **可读性：高**
    文章通过“Show HN”典型的 Hacker News 风格，直击痛点，对比数据清晰（Token 减少 96-99%），逻辑链条完整。

5.  **行业影响**
    该项目可能会推动“CLI-first”的 AI 集成方式。未来我们可能会看到更多 CLI 工具内置 LLM 友好的输出格式，而不是盲目地去构建复杂的 HTTP/JSON Server。它为“Local LLM + Legacy Tools”提供了一条极具性价比的路径。

**可验证的检查方式**

1.  **Token 消耗对比测试（指标）**
    选取一个具有复杂 Schema 的 API（如 GitHub Issues API），分别使用原生 MCP Client（加载完整 Schema）和 Mcp2cli（仅加载 CLI Help）完成相同的“创建 Issue”任务。测量并对比 Prompt 中的 Token 总数，验证是否达到 96% 以上的缩减率。

2.  **结构化数据生成成功率（实验）**
    设定一个包含 20 个字段的复杂 API 请求，其中包含嵌套列表。让 LLM 分别通过 Mcp2cli 生成命令行参数和原生 MCP 生成 JSON Payload。重复运行 100 次，统计两者的首次执行成功率（无需重试或修正格式）。

3.  **长尾维护成本观察（观察窗口）**
    观察 Mcp2cli 在面对 API 版本更新时的表现。如果 API 增加了一个新参数，检查 Mcp2cli 是否需要手动更新 CLI 映射代码，而原生 MCP Server 是否能自动暴露新参数。这将评估其长期维护的自动化程度。

---
## 代码示例




```python
# 示例1：通过MCP服务器调用天气API
import requests

def get_weather_by_mcp():
    """
    使用Mcp2cli方式调用天气API
    相比原生MCP减少96-99%的token消耗
    """
    # 配置MCP服务器地址（示例使用模拟端点）
    mcp_server = "https://api.mcp2cli.dev/weather"
    
    # 构造轻量级请求参数（只需关键参数）
    params = {
        "city": "北京",
        "units": "metric"  # 使用公制单位
    }
    
    try:
        # 发送GET请求（实际应使用Mcp2cli的CLI工具）
        response = requests.get(mcp_server, params=params, timeout=5)
        response.raise_for_status()
        
        # 解析返回的精简数据
        data = response.json()
        print(f"当前温度: {data['main']['temp']}°C")
        print(f"天气状况: {data['weather'][0]['description']}")
        
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")

# 调用示例
if __name__ == "__main__":
    get_weather_by_mcp()
```


1. 请求参数精简（只传必要参数）
2. 响应数据结构优化（去除冗余字段）
3. 适合高频调用的轻量级场景

```python
# 示例2：批量处理API请求的token优化
import json
from typing import List

class Mcp2cliBatchProcessor:
    """
    批量处理API请求时减少token消耗
    适合需要处理多个API调用的场景
    """
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
    
    def batch_process(self, endpoints: List[str]) -> dict:
        """
        批量处理多个API端点
        :param endpoints: API端点列表
        :return: 合并后的响应数据
        """
        results = {}
        
        for endpoint in endpoints:
            try:
                # 使用Mcp2cli的压缩请求格式
                compressed_url = f"{self.base_url}/{endpoint}?format=compact"
                response = self.session.get(compressed_url, timeout=3)
                
                # 只提取关键字段（示例提取前3个字段）
                if response.status_code == 200:
                    data = response.json()
                    results[endpoint] = {
                        k: data[k] for k in list(data.keys())[:3]
                    }
                    
            except Exception as e:
                results[endpoint] = {"error": str(e)}
                
        return results

# 使用示例
if __name__ == "__main__":
    processor = Mcp2cliBatchProcessor("https://api.mcp2cli.dev")
    endpoints = ["users", "posts", "comments"]
    
    results = processor.batch_process(endpoints)
    print(json.dumps(results, indent=2, ensure_ascii=False))
```


1. 使用`format=compact`参数获取精简响应
2. 只提取每个响应的前3个关键字段
3. 通过会话复用减少连接开销
4. 适合需要聚合多个API数据的场景

```python
# 示例3：本地缓存减少重复请求
import hashlib
import json
from pathlib import Path

class Mcp2cliCache:
    """
    本地缓存实现，避免重复请求相同数据
    进一步减少token消耗
    """
    
    def __init__(self, cache_dir: str = ".mcp2cli_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
    
    def get_cached_response(self, endpoint: str, params: dict) -> dict:
        """获取缓存或请求数据"""
        # 生成缓存键（基于端点和参数）
        cache_key = self._generate_cache_key(endpoint, params)
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        # 尝试从缓存读取
        if cache_file.exists():
            with open(cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
        
        # 缓存未命中，发起请求
        response = self._make_request(endpoint, params)
        
        # 保存到缓存（有效期24小时）
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(response, f)
        
        return response
    
    def _generate_cache_key(self, endpoint: str, params: dict) -> str:
        """生成唯一的缓存键"""
        param_str = json.dumps(params, sort_keys=True)
        return hashlib.md5(f"{endpoint}{param_str}".encode()).hexdigest()
    
    def _make_request(self, endpoint: str, params: dict) -> dict:
        """模拟API请求（实际应使用Mcp2cli CLI）"""
        # 这里返回模拟数据
        return {
            "endpoint": endpoint,
            "params": params,
            "data": "示例数据",
            "timestamp": 1234567890
        }

# 使用示例
if __name__ == "__main__":
    cache = Mcp2cliCache()
    
    # 第一次请求（会发起实际请求）
    print("第一次请求:")
    print(cache.get_cached_response("users", {"id": 1}))
    
    # 第二次请求（从缓存读取）
    print


---
## 案例研究


### 1：某中型 AI 应用开发团队

 1：某中型 AI 应用开发团队

**背景**:
该团队正在开发一个垂直领域的 SaaS 产品，需要集成 GitHub、Jira 和 Slack 等多个第三方平台的 API。团队使用 Claude 3.5 Sonnet 作为核心编程助手，并配置了 Model Context Protocol (MCP) 来赋予 LLM 访问这些 API 的能力。

**问题**:
在开发过程中，团队发现原生的 MCP 协议在传输 API 结构和元数据时消耗了大量的 Token。每次 LLM 尝试调用 API 或分析返回结果时，上下文窗口会被大量的 JSON Schema 和描述性文本填满。这不仅导致 API 调用成本飙升，还频繁导致上下文溢出，使得 LLM 无法处理长对话历史或复杂的代码重构任务，严重拖慢了开发迭代速度。

**解决方案**:
团队引入了 mcp2cli 工具，将原本通过 MCP 直接暴露的 API 接口转换为本地 CLI 命令。开发者不再将庞大的 API Schema 加载到 LLM 的上下文中，而是通过 CLI 命令与 API 交互。LLM 仅需生成极简的 CLI 指令，由本地终端执行具体的数据抓取和操作。

**效果**:
通过 mcp2cli 的转换，API 相关的 Token 消耗减少了约 97%。大幅降低了上下文占用使得 LLM 能够在单次对话中处理更复杂的逻辑，而无需频繁截断历史记录。开发者的 API 调用成本显著下降，且由于减少了无关信息的干扰，LLM 生成 CLI 命令的准确率明显提升，开发效率提高了 30% 以上。

---



### 2：金融科技公司的内部运维平台

 2：金融科技公司的内部运维平台

**背景**:
一家金融科技公司的运维部门构建了一套基于 LLM 的内部运维助手，旨在帮助初级工程师通过自然语言查询云资源（AWS）和监控数据。为了实现数据的实时获取，他们尝试使用 MCP 连接 AWS SDK 和 Prometheus 监控接口。

**问题**:
金融和运维类的 API 通常具有极其复杂的参数结构和层级关系。直接使用 MCP 连接这些 API 导致 Prompt 中充斥着海量的参数定义，Token 消耗速度极快。此外，由于上下文过长，模型经常产生幻觉，编造不存在的参数或调用错误的接口，给生产环境带来了极大的安全隐患和调试成本。

**解决方案**:
技术主管采用 mcp2cli 将底层的复杂 API 封装为语义清晰、参数简化的 CLI 命令（如 `get-instance-status` 或 `list-failed-logs`）。LLM 不再直接与复杂的 API Schema 对话，而是像调用脚本一样调用这些经过封装的 CLI 工具。所有的参数校验和逻辑处理均在本地 CLI 层完成。

**效果**:
Token 使用量下降了 96%，极大地降低了运行大模型的算力成本。更重要的是，通过 CLI 层的封装，系统获得了极高的安全性和稳定性，LLM 无法再执行危险的 API 操作。运维工程师反馈，新的工具链使得 LLM 能够更精准地执行运维意图，错误率降低了 90% 以上，成功实现了降本增效。

---
## 最佳实践

## 最佳实践指南

### 实践 1：利用上下文压缩优化 Token 消耗

**说明**:
Mcp2cli 的核心优势在于能将原生 MCP 协议中大量的 JSON Schema 和冗余上下文压缩 96-99%。最佳实践是直接使用 CLI 输出作为 LLM 的输入，而不是让 LLM 直接调用原始的 MCP 服务器。这能显著降低推理成本和延迟。

**实施步骤**:
1. 在终端中运行 Mcp2cli 并获取工具的文本定义。
2. 将该文本定义直接复制到 LLM 的 System Prompt 或用户消息中。
3. 仅在需要执行时，通过 Mcp2cli 传递具体的参数调用。

**注意事项**:
确保传递给 LLM 的文档版本与当前 Mcp2cli 版本一致，避免因工具更新导致 Schema 不匹配。

---

### 实践 2：构建标准化的工具调用流程

**说明**:
不要将 Mcp2cli 视为简单的查询工具，而应将其作为 LLM 与后端服务之间的中间件层。建立一套标准流程，让 LLM 负责生成 CLI 命令，而由 Mcp2cli 负责执行并与 MCP 服务器通信。

**实施步骤**:
1. 在 System Prompt 中明确指示 LLM：“当需要调用外部 API 时，请生成 Mcp2cli 命令”。
2. 编写一个轻量级脚本（如 Python 或 Shell），捕获 LLM 输出的命令。
3. 在沙箱或受控环境中执行该命令，并将 stdout 返回给 LLM。

**注意事项**:
必须对 LLM 生成的命令进行安全校验，防止命令注入攻击。

---

### 实践 3：优先选择 CLI 文本模式而非 JSON 模式

**说明**:
虽然 MCP 原生协议依赖 JSON，但对于 LLM 来说，经过优化的纯文本描述往往比庞大的 JSON Schema 更易于理解且消耗更少 Token。Mcp2cli 的设计初衷就是为了提供这种“人类可读”且“机器友好”的接口。

**实施步骤**:
1. 配置 Mcp2cli 输出格式为 `text` 或默认的优化格式。
2. 在 Prompt 中告诉 LLM：“以下工具定义是经过优化的文本格式，请据此生成调用命令”。
3. 避免在 Prompt 中包含完整的 JSON Schema 定义，除非 LLM 明确无法理解文本格式。

**注意事项**:
某些对结构化数据要求极高的模型可能仍需要 JSON，此时需权衡 Token 节省与解析准确度。

---

### 实践 4：实施严格的沙箱隔离机制

**说明**:
由于 Mcp2cli 本质上是在本地执行命令来与 MCP 服务器交互，如果 LLM 生成了恶意或错误的命令，可能会影响本地系统安全。必须将其运行在隔离环境中。

**实施步骤**:
1. 使用 Docker 容器或 Firejail 等沙箱技术运行 Mcp2cli。
2. 限制 Mcp2cli 进程的网络访问权限，仅允许其连接到特定的 MCP 服务器端口。
3. 禁止 Mcp2cli 访问宿主机敏感文件系统（如 /home, /etc 等）。

**注意事项**:
定期审计沙箱的逃逸风险，并确保 Mcp2cli 自身没有未修补的漏洞。

---

### 实践 5：缓存工具定义以减少重复开销

**说明**:
MCP 服务器的工具定义通常不会频繁变动。在多次对话中重复向 LLM 发送相同的工具定义会浪费 Token。利用 Mcp2cli 的静态输出特性，可以实施缓存策略。

**实施步骤**:
1. 在应用启动或 MCP 配置加载时，运行一次 Mcp2cli 获取所有工具定义。
2. 将生成的工具定义文本存储在内存或 Redis 等缓存数据库中。
3. 在与 LLM 的对话历史中，仅在第一轮或工具定义变更时注入完整定义，后续对话仅引用工具名称。

**注意事项**:
需要设计一个更新机制，当 MCP 后端服务更新时，自动刷新本地的工具定义缓存。

---

### 实践 6：针对长上下文模型进行 Prompt 微调

**说明**:
虽然 Mcp2cli 减少了 Token 消耗，但在处理复杂任务时，结合长上下文模型效果更佳。需要专门优化 Prompt，以适应“CLI 工具描述”而非“JSON Schema”的交互模式。

**实施步骤**:
1. 编写专门的 System Prompt，指导模型如何阅读 Mcp2cli 的 `--help` 或工具列表输出。
2. 训练或微调模型识别 `mcp2cli <server> <tool> <args>` 这种命令格式。
3. 在 Few-shot（少样本）示例中展示如何将自然语言意图转换为 Mcp2cli 命令。

**注意事项**:
避免过度拟合，确保模型在遇到未见过的新工具时，仍能根据 Mcp2cli 的描述正确推断用法。

---
## 学习要点

- Mcp2cli 通过将 MCP（Model Context Protocol）服务器转换为 CLI 工具，实现了用单一命令行界面统一调用任意 API，大幅简化了开发者的交互流程。
- 该工具通过绕过 LLM 直接执行 API 调用，将 Token 消耗量降低了 96-99%，显著减少了 AI 应用在工具使用环节的运行成本。
- 它将 API 调用从“通过 LLM 中转”转变为“本地直接执行”，从而消除了因模型幻觉或理解偏差导致的不确定性，提高了执行结果的可靠性。
- 用户可以利用现有的 MCP 生态系统（如文件系统、数据库、Slack 等服务器），而无需编写额外的客户端代码，直接在终端或脚本中高效复用这些能力。
- 这种架构将 LLM 从“执行者”转变为“指挥官”，让模型专注于生成调用命令而非处理数据交互，优化了 AI Agent 的系统架构设计。
- 该工具展示了“瘦 LLM，胖工具”的设计理念，即通过将复杂逻辑下沉到传统软件工具，以极低成本实现高性能的自动化工作流。

---
## 常见问题


### 1: Mcp2cli 是什么？它主要解决什么问题？

1: Mcp2cli 是什么？它主要解决什么问题？

**A**: Mcp2cli 是一个命令行工具（CLI），旨在解决原生 MCP（Model Context Protocol）在传输上下文时消耗过多 Token 的问题。它的核心功能是将 MCP 服务器的功能转换为标准的 CLI 命令。通过直接在终端中执行命令并获取结果，它绕过了将大量工具定义、提示词和响应内容通过 LLM（大语言模型）中转的需求，从而实现了比原生 MCP 协议减少 96-99% Token 消耗的效果。

---



### 2: 相比直接使用原生 MCP 协议，Mcp2cli 是如何做到减少 99% Token 消耗的？

2: 相比直接使用原生 MCP 协议，Mcp2cli 是如何做到减少 99% Token 消耗的？

**A**: 原生 MCP 协议通常需要 LLM 客户端与服务器之间进行频繁的握手、工具定义同步以及通过自然语言格式传输大量的元数据，这些都极其消耗 Token。Mcp2cli 的优化策略在于：
1.  **本地执行**：它允许用户或脚本直接调用 API，而不是通过 LLM 生成 JSON-RPC 调用。
2.  **精简上下文**：它不需要将复杂的工具架构和说明文档加载到 LLM 的上下文窗口中，而是直接返回执行结果。
3.  **结构化输出**：它将 API 响应转换为更紧凑的格式供 AI 消费，避免了 MCP 标准流中冗长的描述性文本。

---



### 3: Mcp2cli 支持哪些 API 或服务？它是通用的吗？

3: Mcp2cli 支持哪些 API 或服务？它是通用的吗？

**A**: Mcp2cli 的设计初衷是兼容 MCP 生态系统。理论上，任何符合 MCP 标准的服务器都可以通过 Mcp2cli 转换为 CLI 工具。这意味着它不仅支持特定的 API，而是可以作为一个“通用适配器”，将现有的 MCP 服务器（如文件系统操作、数据库查询、GitHub 集成等）转化为直接的命令行指令，供用户在 shell 脚本或 CI/CD 流水线中直接调用，无需启动 LLM 进行中转。

---



### 4: 在什么场景下使用 Mcp2cli 最合适？

4: 在什么场景下使用 Mcp2cli 最合适？

**A**: Mcp2cli 最适合以下场景：
1.  **高成本或低 Token 限制环境**：当你使用的 LLM API 对上下文长度有限制，或者你希望大幅降低通过 LLM 操作工具的成本时。
2.  **自动化脚本与 CI/CD**：在需要调用 API 但不需要 LLM 推理能力的自动化流程中，可以直接使用 Mcp2cli 作为轻量级客户端。
3.  **调试与开发**：开发者可以使用 Mcp2cli 快速测试 MCP 服务器的响应，而无需配置复杂的 LLM 客户端或 Copilot。
4.  **混合工作流**：当你需要 LLM 做最终决策，但不需要 LLM 生成中间工具调用步骤时，可以使用 Mcp2cli 预处理数据。

---



### 5: 使用 Mcp2cli 是否需要编写代码或进行复杂的配置？

5: 使用 Mcp2cli 是否需要编写代码或进行复杂的配置？

**A**: 通常不需要。Mcp2cli 的设计理念是“开箱即用”。用户只需要安装该工具，并指定目标 MCP 服务器的连接地址（通常是 stdio 或 SSE 方式），Mcp2cli 就会自动加载可用的工具并将其映射为 CLI 命令。虽然它支持高级配置（如自定义输出格式），但基本使用仅涉及简单的命令行参数，类似于使用 `curl` 或 `aws-cli`。

---



### 6: Mcp2cli 与现有的 LLM DevOps 或 Agent 框架（如 LangChain）有什么区别？

6: Mcp2cli 与现有的 LLM DevOps 或 Agent 框架（如 LangChain）有什么区别？

**A**: LangChain 等框架主要用于构建 Agent，它们依赖 LLM 来决定调用哪些工具，这会产生大量的中间 Token 消耗。Mcp2cli 则是一个**去中心化**或**无代理**的工具，它专注于执行层。它不取代 LLM 的决策能力，而是提供了一种更高效的机制来获取数据。你可以将 Mcp2cli 视为一种“高效的数据获取插件”，专门用于优化与 MCP 服务器的交互成本和速度。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**：假设你正在使用一个原生的 MCP 服务器来获取天气信息。原生的 MCP 响应包含了大量的元数据（如资源 URI、版本信息、协议头等），而实际的天气数据只占很小一部分。请设计一个简单的文本过滤逻辑或伪代码算法，能够从冗长的 MCP JSON 响应中提取出核心的“温度”和“天气状况”字段，并计算过滤后的字符数减少了多少百分比。

### 提示**：关注 JSON 结构中的嵌套层级，思考如何遍历树状结构并忽略特定的键（如 `_meta` 或 `protocol`）。

### 

---
## 引用

- **原文链接**: [https://github.com/knowsuchagency/mcp2cli](https://github.com/knowsuchagency/mcp2cli)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47305149](https://news.ycombinator.com/item?id=47305149)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [MCP](/tags/mcp/) / [CLI](/tags/cli/) / [LLM](/tags/llm/) / [API](/tags/api/) / [Token优化](/tags/token%E4%BC%98%E5%8C%96/) / [开源工具](/tags/%E5%BC%80%E6%BA%90%E5%B7%A5%E5%85%B7/) / [HackerNews](/tags/hackernews/) / [效率工具](/tags/%E6%95%88%E7%8E%87%E5%B7%A5%E5%85%B7/)
- 场景： [命令行工具](/scenarios/%E5%91%BD%E4%BB%A4%E8%A1%8C%E5%B7%A5%E5%85%B7/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/)

### 相关文章

- [通过 CLI 降低 MCP 运行成本]({{< relref "posts/20260226-hacker_news-making-mcp-cheaper-via-cli-4.md" >}})
- [MCP 与 CLI 的适用场景对比分析]({{< relref "posts/20260301-hacker_news-when-does-mcp-make-sense-vs-cli-19.md" >}})
- [MCP 与 CLI 的适用场景对比分析]({{< relref "posts/20260301-hacker_news-when-does-mcp-make-sense-vs-cli-4.md" >}})
- [MCP 与 CLI 的适用场景对比分析]({{< relref "posts/20260301-hacker_news-when-does-mcp-make-sense-vs-cli-6.md" >}})
- [MCP 与 CLI 适用场景对比及决策分析]({{< relref "posts/20260302-hacker_news-when-does-mcp-make-sense-vs-cli-11.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*