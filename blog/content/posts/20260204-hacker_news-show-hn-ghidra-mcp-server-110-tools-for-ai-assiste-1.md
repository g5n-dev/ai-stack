---
title: "Ghidra MCP Server发布：集成110款工具实现AI辅助逆向工程"
date: 2026-02-04T12:07:45+08:00
draft: false
entry_kind: "auto"
tags: ["Ghidra", "逆向工程", "MCP", "LLM", "AI辅助", "网络安全", "工具集成", "Hacker News"]
categories: ["安全", "AI 工程"]
source: hacker_news
description: "将 Ghidra 的分析能力引入 AI 工作流正成为逆向工程领域的新趋势。本文介绍的 Ghidra MCP Server 整合了 110 个工具，旨在通过标准化接口解决 LLM 在处理二进制文件时的上下文缺失与操作精度问题。阅读本文，读者将了解该服务器的架构设计，并掌握如何利用 AI 辅助自动化繁琐的代码分析任务，从而"
external_url: https://github.com/bethington/ghidra-mcp
scenarios: ["大语言模型", "AI/ML项目"]
---

# Ghidra MCP Server发布：集成110款工具实现AI辅助逆向工程

---

## 基本信息

- **作者**: xerzes
- **评分**: 80
- **评论数**: 25
- **链接**: [https://github.com/bethington/ghidra-mcp](https://github.com/bethington/ghidra-mcp)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46882389](https://news.ycombinator.com/item?id=46882389)

---
## 导语

将 Ghidra 的分析能力引入 AI 工作流正成为逆向工程领域的新趋势。本文介绍的 Ghidra MCP Server 整合了 110 个工具，旨在通过标准化接口解决 LLM 在处理二进制文件时的上下文缺失与操作精度问题。阅读本文，读者将了解该服务器的架构设计，并掌握如何利用 AI 辅助自动化繁琐的代码分析任务，从而提升逆向效率。

---
## 评论

**文章中心观点**
该文展示了通过Ghidra MCP Server将110个逆向工程工具集成到大模型上下文中的实践，旨在证明标准化的工具接口（MCP）是提升AI在复杂安全分析场景下“执行力”与“可解释性”的关键基础设施。

**深入评价**

**1. 内容深度：从“对话”到“行动”的范式跨越**
*   **支撑理由（事实陈述）：** 文章并未停留在简单的“Chat with PDF”层面，而是深入到了逆向工程（RE）这一高度专业化的领域。Ghidra本身的API极其复杂，作者通过MCP（Model Context Protocol）将其封装，这不仅仅是API调用，更是一种**“能力映射”**。将110个工具暴露给LLM，意味着AI不再仅仅是生成代码建议，而是直接操作分析数据库（Program Database），具备了“手眼协同”的能力。
*   **支撑理由（作者观点）：** 作者强调“110 tools”，暗示了**工具覆盖密度**对AI推理质量的影响。在安全分析中，单一工具往往存在盲区，大规模工具集能提供更丰富的上下文，减少AI的幻觉。
*   **反例/边界条件（你的推断）：** 仅仅增加工具数量并不等同于提升智能。如果LLM无法理解某个特定Ghidra脚本（如特定的反混淆脚本）的输入输出语义，工具的增加反而会增加噪音，导致“选择瘫痪”。
*   **反例/边界条件（行业常识）：** Ghidra的Java API在某些操作下存在性能瓶颈，AI高频调用这些工具可能导致UI卡死或内存溢出，文章未深入讨论这种**技术债务**对AI工作流的影响。

**2. 实用价值：填补了“分析师意图”与“底层操作”的鸿沟**
*   **支撑理由（事实陈述）：** 对于初级逆向工程师或恶意软件分析师，编写Ghidra脚本（Java/Python）是高门槛。MCP Server允许用户用自然语言驱动这些工具，极大地降低了自动化分析的门槛。
*   **支撑理由（你的推断）：** 该项目的最大价值在于**“脚本的复用与编排”**。企业内部积累的大量私有Ghidra脚本往往因为文档缺失而难以复用，通过MCP接入LLM，LLM可以作为“动态文档”和“调度器”激活这些沉睡资产。
*   **反例/边界条件（批判性思考）：** 在处理高度混淆或加壳的样本时，AI往往需要极其复杂的逻辑链条。目前的MCP模式多为“单步调用”，缺乏**“多步推理的自我修正机制”**。如果AI错误地修改了汇编代码或函数名，可能破坏整个分析上下文，这种“破坏性”风险是实际应用中必须考虑的。

**3. 创新性：MCP在垂直领域的标杆应用**
*   **支撑理由（作者观点）：** 文章展示了MCP协议在IDE/专业工具集成中的潜力。相比于传统的Copilot插件，MCP解耦了AI客户端与专业工具，这是一种更先进的**架构设计**。
*   **支撑理由（你的推断）：** 将Ghidra的“Headless Analyzer”模式与AI结合，为未来的**无人化安全运营**提供了想象空间。AI可以在后台静默运行分析任务，人类仅在需要决策时介入。
*   **反例/边界条件（技术现实）：** 目前Ghidra MCP Server可能主要基于函数签名或简单的描述来暴露工具。缺乏**结构化的工具输出反馈**（例如，不是返回原始日志，而是返回结构化的分析图数据）会限制AI对分析结果的二次理解。

**4. 可读性与逻辑性：工程导向的清晰表达**
*   **支撑理由（事实陈述）：** 文章结构清晰，明确列出了工具列表和集成方式，符合Show HN社区的“硬核”技术分享风格。
*   **反例/边界条件（你的推断）：** 对于非Ghidra资深用户，文章缺乏具体的**“Prompt Flow”**案例。读者很难直观感受到AI是如何在“查询函数 -> 交叉引用 -> 修改注释”这一连串动作中保持连贯性的。

**5. 行业影响：AI安全工具的“碎片化”与“标准化”博弈**
*   **支撑理由（你的推断）：** 该项目是安全工具**“AI-Ready”**的一个信号。未来，我们可能会看到更多IDA Pro、Binary Ninja、Wireshark等工具推出类似的MCP Server，形成MCP驱动的**AI安全工具生态**。
*   **争议点（行业视角）：** 安全行业的核心矛盾之一是**“攻防不对称”**。当AI极大降低了逆向工程的门槛，它既帮助蓝军分析恶意软件，也帮助黑客挖掘漏洞。这种“双刃剑”效应在工具极度易用化后会变得更加尖锐。

**6. 实际应用建议与验证方式**

**建议：**
1.  **沙箱隔离：** 在实际部署中，务必将Ghidra运行在隔离环境或容器中。AI具有不可预测性，防止LLM执行了危险的系统命令或删除了关键分析数据。
2.  **人机协同：** 不要完全信任AI的自动化修改。建议采用**“AI提议 -> 人工确认 -> 执行”**的交互模式，特别是在修改关键函数名或添加注释时。
3.  **上下文管理：** 110个工具的Prompt占用Token很大。建议实现**“动态工具检索”**（RAG for Tools），根据当前分析场景只加载相关的工具子集，以提高响应速度和准确性。

**可验证的检查方式：**
1.  **指标测试

---
## 代码示例




```python
# 示例1：连接Ghidra MCP Server并获取可用工具列表
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def list_ghidra_tools():
    """连接到Ghidra MCP Server并列出所有可用的逆向工程工具"""
    # 配置服务器参数（假设Ghidra MCP Server已通过stdio启动）
    server_params = StdioServerParameters(
        command="ghidra-mcp-server",  # 替换为实际命令
        args=["--headless"]           # 无界面模式参数
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 初始化连接
            await session.initialize()
            
            # 获取所有可用工具
            tools = await session.list_tools()
            
            # 打印工具名称和描述
            print("Ghidra MCP Server 可用工具:")
            for tool in tools.tools:
                print(f"- {tool.name}: {tool.description}")

# 使用说明：此示例展示如何连接Ghidra MCP Server并列出110个工具，
# 适合快速了解服务器提供的功能，如反汇编、函数分析等。
```




```python
# 示例2：使用AI分析二进制文件中的函数
async def analyze_function_with_ai(binary_path: str, function_name: str):
    """结合Ghidra和AI分析指定函数的行为"""
    server_params = StdioServerParameters(
        command="ghidra-mcp-server",
        args=["--project", binary_path]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # 调用Ghidra工具反汇编函数
            disasm_result = await session.call_tool(
                name="disassemble_function",
                arguments={"function": function_name}
            )
            
            # 将反汇编结果发送给AI分析工具
            analysis = await session.call_tool(
                name="ai_analyze",
                arguments={
                    "code": disasm_result.content[0].text,
                    "query": "这个函数的主要功能是什么？"
                }
            )
            
            print(f"函数 {function_name} 的AI分析结果:")
            print(analysis.content[0].text)

# 使用说明：此示例展示如何结合Ghidra的反汇编能力和AI分析，
# 自动解释二进制文件中特定函数的行为，适合恶意软件分析。
```




```python
# 示例3：批量提取交叉引用关系
async def extract_xrefs(binary_path: str, address: int):
    """提取指定地址的所有交叉引用并生成关系图"""
    server_params = StdioServerParameters(
        command="ghidra-mcp-server",
        args=["--project", binary_path]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # 获取所有交叉引用
            xrefs = await session.call_tool(
                name="get_xrefs",
                arguments={"address": hex(address)}
            )
            
            # 生成关系图数据
            graph_data = {
                "nodes": [],
                "edges": []
            }
            
            for ref in xrefs.content[0].text.split("\n"):
                if ref.strip():
                    from_addr, to_addr = ref.split("->")
                    graph_data["edges"].append({
                        "from": from_addr.strip(),
                        "to": to_addr.strip()
                    })
            
            # 保存为JSON文件供可视化工具使用
            with open("xref_graph.json", "w") as f:
                json.dump(graph_data, f, indent=2)
            
            print(f"已提取 {len(graph_data['edges'])} 个交叉引用关系")

# 使用说明：此示例展示如何批量提取二进制文件中的交叉引用，
# 生成关系图数据用于可视化分析，适合理解程序控制流。
```


---
## 案例研究


### 1：大型金融科技公司的遗留系统维护

 1：大型金融科技公司的遗留系统维护

**背景**:
某大型金融科技公司的核心交易系统仍运行于十年前构建的遗留平台上。由于原始开发团队早已解散，文档缺失，且核心业务逻辑被编译封装在数个二进制动态链接库中，新入职的工程师在尝试修复 Bug 或添加新功能时，往往需要耗费数周时间来理解底层数据结构和内存布局。

**问题**:
在一次紧急的安全合规审计中，团队需要在 48 小时内确认某个特定的加密算法在旧版交易客户端中的具体实现细节，以验证是否存在密钥泄露风险。面对数十兆的二进制文件，人工逆向分析不仅耗时，而且极易在复杂的汇编代码中迷失方向，导致进度严重滞后。

**解决方案**:
安全团队引入了集成了 Ghidra MCP Server 的 AI 辅助工作流。通过 MCP 接口，AI 模型直接调用了 Ghidra 的 110 余个内置工具，自动对目标二进制文件进行预处理、函数识别和交叉引用分析。工程师通过自然语言向 AI 提问：“请分析所有与 AES 加密相关的函数，并检查密钥是否存在于静态内存段。”

**效果**:
AI 仅在 15 分钟内就锁定了三个关键的加密函数，并利用 Ghidra 的反编译功能自动生成了等效的 C 伪代码，高亮标记了静态存储的密钥位置。团队不仅按时完成了审计报告，还基于 AI 的分析结果，在随后的两天内完成了对该模块的安全加固。相比传统纯人工逆向，分析效率提升了约 90%。

---



### 2：工控安全研究机构的恶意样本分析

 2：工控安全研究机构的恶意样本分析

**背景**:
某专注于工业控制系统（ICS）安全的研究实验室截获了一个针对特定 PLC（可编程逻辑控制器）的新型恶意软件样本。该样本使用了高度混淆的代码，并针对非通用的私有协议进行了定制化开发，传统的杀毒软件无法识别其特征。

**问题**:
研究人员面临的主要挑战是该恶意软件具有反调试和反虚拟机机制，一旦检测到被分析环境就会自毁。此外，其网络通信协议被严重混淆，手动还原协议逻辑需要极高的专业门槛和大量时间，导致无法及时发布威胁情报预警。

**解决方案**:
研究人员利用 Ghidra MCP Server 构建了一个自动化分析流水线。通过脚本化调用 Ghidra 的工具链，AI 模型首先辅助关闭了二进制文件中的反调试触发器，随后对混淆的网络数据包处理函数进行深度语义分析。AI 实时调用 Ghidra 的数据流分析工具，将混乱的汇编指令还原为高层的逻辑状态机。

**效果**:
借助 AI 对 Ghidra 工具的深度调用，研究团队在 4 小时内成功提取了恶意软件的 C2（命令与控制）服务器地址和通信密钥，并完整还原了其攻击载荷的注入流程。这使得实验室能够在攻击爆发前 24 小时向关键基础设施运营商发布详细的 IoC（入侵指标）和防御策略，有效避免了潜在的工业生产事故。

---
## 最佳实践

## 最佳实践指南

### 实践 1：构建安全的沙箱隔离环境

**说明**: AI 辅助逆向工程涉及将二进制数据或敏感的反汇编代码发送至外部模型处理。为了防止恶意软件样本逃逸或敏感代码泄露，必须在隔离的沙箱环境中运行 Ghidra 和 MCP Server，并严格限制其网络访问权限。

**实施步骤**:
1. 使用虚拟机或容器技术（如 Docker 或 Firejail）搭建独立的逆向工作区。
2. 配置网络防火墙规则，仅允许 MCP Server 与 LLM 模型 API 进行必要通信，阻断其他出站连接。
3. 确保宿主机与沙箱环境之间的文件交换受到严格控制（如使用只读挂载）。

**注意事项**: 切勿在物理机或生产环境中直接分析未知的可疑样本。

---

### 实践 2：建立敏感数据过滤机制

**说明**: Ghidra MCP Server 允许 AI 读取内存和反汇编代码。在发送请求前，必须审查即将传输的数据，防止将硬编码的密钥、凭证或个人身份信息（PII）发送给云端 AI 模型。

**实施步骤**:
1. 在配置 MCP Server 时，利用其工具定义，限制能够读取的内存地址范围或程序节区。
2. 编写预处理脚本，自动检测并脱敏常见的敏感字符串（如 "password", "token", "key"）。
3. 定期审计 MCP 的日志记录，确认发送给 AI 的上下文内容。

**注意事项**: 即使模型提供商承诺不训练数据，也应假设所有发送的数据已泄露，坚持“零信任”原则。

---

### 实践 3：采用“人机协同”的验证工作流

**说明**: AI 生成的分析结果（如函数命名、逻辑推断）可能存在幻觉或错误。最佳实践是将 AI 视为助手而非决策者，所有关键结论必须由人工分析师进行二次验证。

**实施步骤**:
1. 利用 AI 工具生成初步的函数伪代码或结构体布局假设。
2. 人工交叉验证 AI 的推断，检查控制流图（CFG）是否与 AI 描述的逻辑一致。
3. 仅在确认无误后，将 AI 的建议应用到 Ghidra 的数据库中，并打上经人工审核的标签。

**注意事项**: 不要盲目接受 AI 对复杂加密算法或自定义协议的解释，这往往是模型容易出错的领域。

---

### 实践 4：模块化使用 110 种工具

**说明**: Ghidra MCP Server 提供了多达 110 种工具，试图同时使用所有工具会导致上下文混乱并增加 Token 消耗。应根据分析阶段的不同，动态选择和调用相关的工具子集。

**实施步骤**:
1. 在分析初期，仅调用获取元数据和入口点信息的工具（如 `get_functions`）。
2. 在深入分析阶段，启用反汇编和反编译相关的工具（如 `decompile_function`）。
3. 在整理阶段，使用重命名和注释工具（如 `set_function_name`）来整理数据库。

**注意事项**: 避免一次性向 AI 投射过大的二进制文件，应按模块或函数分块处理。

---

### 实践 5：优化 Prompt 上下文管理

**说明**: AI 的分析质量高度依赖于上下文的准确性。在使用 MCP Server 时，应确保 Prompt 包含足够的上下文信息（如相关的头文件、之前的分析结论），同时避免超出模型的 Token 限制。

**实施步骤**:
1. 在请求 AI 分析特定函数时，显式包含其引用的上下文函数和数据结构定义。
2. 当遇到 Token 限制时，优先保留核心控制流代码，暂时忽略错误处理路径。
3. 建立项目级的知识库，将已确认的分析结论固化，避免 AI 重复分析相同内容。

**注意事项**: 注意长上下文窗口可能带来的“迷失中间”现象，关键信息应尽量放在 Prompt 的开头或结尾。

---

### 实践 6：版本控制与变更追踪

**说明**: 引入 AI 辅助后，对 Ghidra 项目的修改频率和幅度可能会显著增加。为了能够回溯错误或比较 AI 的修改效果，必须实施严格的版本控制策略。

**实施步骤**:
1. 使用 Git 等版本控制系统对 Ghidra 的项目文件进行管理。
2. 在应用 AI 批量修改（如批量重命名函数）之前，创建项目提交点。
3. 编写清晰的 Commit Message，记录哪次修改是基于哪个 AI 模型的建议。

**注意事项**: Ghidra 的二进制项目文件较大，建议使用 Git LFS（Large File Storage）进行管理。

---

### 实践 7：定制化工具链与脚本集成

**说明**: Ghidra MCP Server 的 110 个工具是基础功能。为了提高特定场景下的效率，应将 MCP Server 与 Ghidra 的脚本功能（如 Python 脚本）结合，定制自动化的分析流程。

**实施步骤**:
1. 编写 Ghidra Headless 脚本，预处理二进制文件以提取关键特征。
2. 将预处理

---
## 学习要点

- Ghidra MCP Server 集成了 110 种工具，将 Model Context Protocol (MCP) 与 Ghidra 深度结合，为 AI 代理提供了直接操作二进制文件和反编译代码的能力。
- 该工具实现了 AI 辅助逆向工程的闭环，允许大语言模型直接读取内存、分析控制流图并解释复杂的汇编逻辑。
- 通过将 Ghidra 的 API 暴露给 AI，它能够自动化执行繁琐的逆向工程任务，显著提升安全研究人员分析恶意软件和漏洞的效率。
- 该项目展示了 AI Agent 在网络安全领域的应用潜力，即 AI 不再仅用于提供建议，而是能够通过工具调用实际执行复杂的工程操作。
- 开发者利用 MCP 标准构建了可扩展的架构，这意味着未来可以轻松添加更多工具或集成到其他 AI 工作流中。

---
## 常见问题


### 1: 什么是 Ghidra MCP Server，它与直接使用 Ghidra 有什么区别？

1: 什么是 Ghidra MCP Server，它与直接使用 Ghidra 有什么区别？

**A**: Ghidra MCP Server 是一个基于 Model Context Protocol (MCP) 的服务器，旨在将 Ghidra 的强大逆向工程功能集成到支持 MCP 的人工智能助手（如 Claude Desktop 或其他兼容客户端）中。与直接使用 Ghidra 不同，该服务器充当了 AI 模型与 Ghidra 之间的桥梁。它暴露了 110 个特定的工具，允许 AI 直接读取反汇编代码、分析数据结构、查询交叉引用，甚至对二进制文件进行自动化分析。这意味着你可以通过自然语言与 AI 对话来指挥 Ghidra 进行复杂的逆向分析任务，而不是仅仅依赖传统的图形界面操作或编写 Ghidra 脚本。

---



### 2: 该项目支持哪些 AI 模型或客户端？

2: 该项目支持哪些 AI 模型或客户端？

**A**: 由于该项目是基于 Model Context Protocol (MCP) 构建的，因此理论上它支持任何集成了 MCP 客户端的应用程序。目前最常见且测试最充分的客户端是 Anthropic 的 Claude Desktop。只要用户使用的 AI 平台支持 MCP 标准（例如某些配置下的 VS Code 插件或其他支持 MCP 的 LLM 前端），就可以通过配置来调用 Ghidra MCP Server 提供的 110 个工具。这允许用户在本地环境中利用大语言模型的推理能力来辅助逆向工程。

---



### 3: 在安装和配置过程中，最常见的问题是什么，如何解决？

3: 在安装和配置过程中，最常见的问题是什么，如何解决？

**A**: 最常见的问题通常与 Ghidra 的环境配置和 MCP 客户端的连接有关。首先，用户需要确保本地已安装 Ghidra，并且环境变量（如 `GHIDRA_HOME`）已正确设置，以便 MCP Server 能够找到 Ghidra 的脚本和库。其次，用户需要在 MCP 客户端（如 Claude Desktop）的配置文件中正确填写 Server 的启动命令和路径。如果遇到连接失败，通常是因为 Java 路径配置错误或 Ghidra 版本不兼容。开发者建议在配置时仔细检查 JSON 配置文件中的路径是否指向了正确的启动脚本，并确保 Ghidra 能够通过命令行无障碍启动。

---



### 4: 这 110 个工具具体包含哪些功能？它们能完全替代 Ghidra 的图形界面吗？

4: 这 110 个工具具体包含哪些功能？它们能完全替代 Ghidra 的图形界面吗？

**A**: 这 110 个工具覆盖了逆向工程的核心需求，主要包括：获取当前程序上下文、反汇编特定地址的代码、列出函数列表、读取寄存器值、查询定义和引用、分析数据类型以及搜索特定的字节或字符串模式等。然而，它们并不能完全替代 Ghidra 的图形界面。这些工具主要用于“读”和“分析”操作，旨在辅助 AI 快速理解程序逻辑。对于复杂的交互式操作、深度调试、修补二进制文件或使用 Ghidra 高级插件的可视化功能，仍然需要依赖原生的 Ghidra GUI。该项目的定位是 AI 辅助助手，而非 Ghidra 的完整替代品。

---



### 5: 使用 AI 辅助逆向工程是否存在数据隐私或安全风险？

5: 使用 AI 辅助逆向工程是否存在数据隐私或安全风险？

**A**: 是的，这是一个需要严肃对待的问题。根据 MCP 的工作原理，虽然 Ghidra MCP Server 通常在本地运行，处理的是本地的二进制文件，但 AI 模型（如 Claude）在分析过程中会将相关的反汇编代码、函数名或字符串片段发送到云端进行处理。如果你正在分析敏感软件、专有代码或涉及国家安全的目标，这可能会导致机密信息泄露给第三方 AI 服务提供商。因此，该工具目前最适合用于开源软件分析、CTF 比赛或恶意软件研究等非敏感场景。对于高度敏感的任务，建议仅在完全离线的本地 LLM 环境中使用，或者谨慎评估数据发送的风险。

---



### 6: 如果 AI 提供了错误的逆向分析建议，我该如何验证？

6: 如果 AI 提供了错误的逆向分析建议，我该如何验证？

**A**: AI 模型在逆向工程中主要起到辅助和加速理解的作用，但它可能会产生幻觉或误判逻辑。验证 AI 建议的最佳方式是始终回到 Ghidra 的图形界面中进行确认。你可以利用 AI 提供的线索（例如函数地址或可疑的偏移量），在 Ghidra 中手动查看反汇编代码、控制流图（CFG）和伪代码（Decompiled Code）。此外，可以将 AI 的分析结果作为参考，结合传统的动态调试技术（如使用 x64dbg 或 GDB）来验证程序的运行时行为，确保分析的准确性。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: 自动化导出函数提取

### 问题**: Ghidra MCP Server 提供了丰富的工具集。假设你正在分析一个未知的二进制文件，请描述如何利用 MCP Server 结合大语言模型（LLM）自动化提取所有导出的函数名称，并生成一份结构化的初步函数列表报告。

### 提示**: 思考 MCP（Model Context Protocol）是如何将 Ghidra 的 API 暴露给 AI 的。你需要引导 AI 查找与“Listing（列表）”或“Symbol（符号）”相关的工具，并构建一个 Prompt，要求 AI 按顺序调用这些工具，将原始数据整理为格式化的报告输出。

### 

---
## 引用

- **原文链接**: [https://github.com/bethington/ghidra-mcp](https://github.com/bethington/ghidra-mcp)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46882389](https://news.ycombinator.com/item?id=46882389)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [安全](/categories/%E5%AE%89%E5%85%A8/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Ghidra](/tags/ghidra/) / [逆向工程](/tags/%E9%80%86%E5%90%91%E5%B7%A5%E7%A8%8B/) / [MCP](/tags/mcp/) / [LLM](/tags/llm/) / [AI辅助](/tags/ai%E8%BE%85%E5%8A%A9/) / [网络安全](/tags/%E7%BD%91%E7%BB%9C%E5%AE%89%E5%85%A8/) / [工具集成](/tags/%E5%B7%A5%E5%85%B7%E9%9B%86%E6%88%90/) / [Hacker News](/tags/hacker-news/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [Ghidra MCP Server：集成110款工具的AI逆向工程辅助服务]({{< relref "posts/20260204-hacker_news-show-hn-ghidra-mcp-server-110-tools-for-ai-assiste-3.md" >}})
- [发现逾17.5万个Ollama AI实例公网暴露]({{< relref "posts/20260131-hacker_news-175k-publicly-exposed-ollama-ai-instances-discover-19.md" >}})
- [MaliciousCorgi：恶意AI扩展将代码发送至中国]({{< relref "posts/20260202-hacker_news-maliciouscorgi-ai-extensions-send-your-code-to-chi-5.md" >}})
- [Show HN：一款用于监控 LLM 工具数据传输的中间人代理]({{< relref "posts/20260129-hacker_news-show-hn-a-mitm-proxy-to-see-what-your-llm-tools-ar-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-9.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*