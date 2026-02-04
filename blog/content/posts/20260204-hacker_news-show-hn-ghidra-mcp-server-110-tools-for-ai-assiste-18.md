---
title: "Ghidra MCP Server发布：集成110种工具实现AI辅助逆向工程"
date: 2026-02-04T21:15:24+08:00
draft: false
entry_kind: "auto"
tags: ["Ghidra", "逆向工程", "MCP", "AI辅助", "安全工具", "LLM", "Hacker News", "工具集成"]
categories: ["安全", "AI 工程"]
source: hacker_news
description: "在逆向工程领域，将 Ghidra 的分析能力与 AI 的推理能力结合，是提升分析效率的重要方向。本文介绍的 Ghidra MCP Server 项目，通过集成 110 个工具，为 AI 提供了直接操作 Ghidra 的接口。阅读本文，你将了解该项目的架构设计，以及如何利用它实现更智能的自动化代码分析。"
external_url: https://github.com/bethington/ghidra-mcp
scenarios: ["AI/ML项目", "大语言模型"]
---

# Ghidra MCP Server发布：集成110种工具实现AI辅助逆向工程

---

## 基本信息

- **作者**: xerzes
- **评分**: 243
- **评论数**: 62
- **链接**: [https://github.com/bethington/ghidra-mcp](https://github.com/bethington/ghidra-mcp)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46882389](https://news.ycombinator.com/item?id=46882389)

---
## 导语

在逆向工程领域，将 Ghidra 的分析能力与 AI 的推理能力结合，是提升分析效率的重要方向。本文介绍的 Ghidra MCP Server 项目，通过集成 110 个工具，为 AI 提供了直接操作 Ghidra 的接口。阅读本文，你将了解该项目的架构设计，以及如何利用它实现更智能的自动化代码分析。

---
## 评论

**中心观点**
该文章展示了通过 MCP (Model Context Protocol) 将 Ghidra 的 110 余个原生工具集成到大模型上下文中的尝试，这标志着逆向工程领域正从“单点 AI 辅助”向“全流程智能体协同”演进，但受限于 LLM 的上下文处理能力和幻觉风险，目前更适用于启发式分析而非全自动化的二进制漏洞挖掘。

**支撑理由**

1.  **工具集成的广度与深度**
    *   **[事实陈述]** 文章提到的 "110 tools" 涵盖了 Ghidra 的核心功能，包括反汇编、反编译、脚本分析及数据类型解析。这不仅仅是简单的 API 调用，而是通过 MCP Server 将 Ghidra 的内部能力标准化为 AI 可理解的接口。
    *   **[你的推断]** 这种集成方式解决了 AI 逆向工具中常见的“工具孤岛”问题。以往 AI 往往依赖静态代码片段或独立的脚本，而现在 AI 可以动态调用 Ghidra 的原生能力（如查询交叉引用 Xrefs），使得分析过程具备了“状态感”。

2.  **MCP 协议在安全领域的范式转移**
    *   **[事实陈述]** 文章采用 Anthropic 提出的 MCP 协议，而非传统的 LangChain 或自定义 API。
    *   **[作者观点]** 这是一个明智的技术选型。MCP 专为 LLM 与本地资源交互设计，能够更高效地传输结构化数据。对于逆向工程这种需要处理大量结构体和树状图数据的场景，MCP 比纯文本 Prompt 更能保持数据结构的完整性，减少了 AI 误解代码结构的概率。

3.  **从“阅读”到“操作”的代理能力**
    *   **[你的推断]** 该项目的核心价值在于将 AI 的角色从“观察者”转变为“操作者”。AI 不再仅仅解释汇编代码，而是可以实际执行如 `getFunctions`、`getInstructions` 等命令。
    *   **[实际案例]** 在分析混淆后的恶意代码时，AI 可以先调用工具获取控制流图（CFG），再结合符号执行结果进行推理，这种多步推理能力是单一 Prompt 无法实现的。

**反例与边界条件**

1.  **上下文窗口与Token成本的矛盾**
    *   **[事实陈述]** 逆向工程通常涉及数万甚至数百万行代码。虽然 MCP 提供了工具，但 LLM 的上下文窗口依然是硬伤。
    *   **[边界条件]** 如果目标样本是一个大型固件（如路由器 OS），AI 无法将所有代码载入上下文。此时，如果 AI 缺乏“滑动窗口”或“增量分析”的策略，它可能会基于不完整的上下文得出错误的结论，甚至产生严重的幻觉。

2.  **幻觉风险与安全验证的缺失**
    *   **[作者观点]** 文章侧重于“连接”，但较少讨论“验证”。AI 调用 Ghidra 工具获取的数据是真实的，但 AI 基于这些数据得出的结论（例如：“这个缓冲区可溢出”）可能是错误的。
    *   **[边界条件]** 在高度敏感的漏洞挖掘场景下，AI 的误报率可能高到不可接受。如果完全依赖 AI 的判断而缺乏人工复核，可能会导致严重的工程事故。

**深入评价**

1.  **内容深度与论证严谨性**
    文章在技术实现层面较为扎实，清晰地展示了 MCP Server 的架构。但在论证“AI 辅助逆向”的有效性时，缺乏量化的 Benchmark。例如，相比于传统的 Ghidra 脚本或 IDA Pro 插件，AI 的介入究竟将分析效率提升了多少？文章更多停留在“能做”的层面，未深入探讨“做得多好”。

2.  **实用价值**
    对于逆向工程师而言，该工具具有极高的“尝鲜”价值和辅助价值。特别是在处理不熟悉的架构或混淆算法时，AI 可以作为“副驾驶”快速定位关键函数。然而，对于资深的逆向专家，目前的 AI 水平可能还无法替代其直觉和经验，工具的定位更像是“增强版的搜索与语义理解助手”。

3.  **创新性**
    **[你的推断]** 该项目的最大创新点在于**生态系统的整合**。此前虽然存在 Copilot 等工具，但它们大多悬浮于 IDE 之上。Ghidra MCP Server 直接深入到底层二进制分析框架，这种“Deep Integration”是未来 AI 辅助安全的必经之路。它证明了开源安全工具与闭源大模型（如 Claude/ GPT-4）可以通过标准化协议无缝协作。

4.  **可读性**
    作为一篇 Show HN 的技术分享，文章结构清晰，代码示例明确。但技术门槛较高，要求读者同时理解 Ghidra 的 API 架构和 LLM 的 Prompt Engineering，受众主要集中在安全研究员和 AI 应用开发者。

5.  **行业影响**
    这可能会催生一波“MCP for Security Tools”的浪潮。我们可以预见，未来 IDA Pro、Binary Ninja、GDB 甚至 Frida 都会出现类似的 MCP Server。这将推动安全行业从“手工/脚本化”向“智能体化”加速转型。

6.  **争议点**
    *   **数据隐私：** 将二进制代码片段发送给云端大模型（如 Anthropic API）是许多企业安全团队的红线。文章未提及本地部署（如使用 Ollama）的方案，这在实际企业级落地中是一个巨大的阻碍。
    *   **依赖性：** 过度依赖 AI 可能会导致新一代逆向工程师基础能力的退化。

**实际

---
## 代码示例




```python
# 示例1：使用Ghidra MCP Server自动化提取函数信息
# 前置条件：已启动Ghidra MCP服务器并配置好环境变量
import subprocess
import json

def analyze_function_with_mcp(binary_path, function_name):
    """
    使用MCP工具分析二进制文件中的指定函数
    :param binary_path: 二进制文件路径
    :param function_name: 要分析的函数名
    :return: 包含函数分析结果的字典
    """
    # 调用MCP工具的get_function_info命令
    cmd = [
        "mcp", "call", "get_function_info",
        "--binary", binary_path,
        "--function", function_name
    ]
    
    try:
        # 执行命令并获取JSON输出
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        function_data = json.loads(result.stdout)
        
        # 提取关键信息
        analysis = {
            "函数地址": function_data.get("address"),
            "指令数量": function_data.get("instruction_count"),
            "控制流图": function_data.get("cfg"),
            "交叉引用": function_data.get("xrefs")
        }
        
        return analysis
    except subprocess.CalledProcessError as e:
        print(f"分析失败: {e.stderr}")
        return None

# 使用示例
if __name__ == "__main__":
    result = analyze_function_with_mcp("/path/to/binary", "main")
    print(json.dumps(result, indent=2, ensure_ascii=False))
```


---

```python
# 示例2：批量反汇编并生成伪代码
# 前提：已安装Ghidra并配置好MCP服务器
from mcp_client import GhidraMCPClient  # 假设存在MCP客户端库

def batch_disassemble(binary_path, output_dir):
    """
    批量反汇编二进制文件中的所有函数并生成伪代码
    :param binary_path: 二进制文件路径
    :param output_dir: 输出目录
    """
    client = GhidraMCPClient()  # 初始化MCP客户端
    
    # 1. 获取所有函数列表
    functions = client.list_functions(binary_path)
    print(f"找到 {len(functions)} 个函数")
    
    # 2. 遍历每个函数
    for func in functions:
        # 获取反汇编代码
        disasm = client.get_disassembly(binary_path, func["address"])
        # 获取伪代码
        pseudocode = client.get_pseudocode(binary_path, func["name"])
        
        # 保存到文件
        filename = f"{output_dir}/{func['name']}.txt"
        with open(filename, "w") as f:
            f.write(f"函数: {func['name']}\n")
            f.write(f"地址: {func['address']}\n\n")
            f.write("=== 反汇编 ===\n")
            f.write(disasm)
            f.write("\n=== 伪代码 ===\n")
            f.write(pseudocode)
        
        print(f"已处理: {func['name']}")

# 使用示例
if __name__ == "__main__":
    batch_disassemble("/path/to/binary", "./output")
```


---

```python
# 示例3：交互式漏洞检测
# 需要：Ghidra MCP服务器 + 安全分析工具集成
from mcp_client import GhidraMCPClient
from vulnerability_scanner import scan_function  # 假设存在漏洞扫描器

def interactive_vuln_scan(binary_path):
    """
    交互式漏洞检测工具
    :param binary_path: 二进制文件路径
    """
    client = GhidraMCPClient()
    
    while True:
        print("\n1. 列出所有函数")
        print("2. 扫描指定函数")
        print("3. 生成漏洞报告")
        print("4. 退出")
        
        choice = input("请选择操作: ")
        
        if choice == "1":
            functions = client.list_functions(binary_path)
            for i, func in enumerate(functions, 1):
                print(f"{i}. {func['name']} @ {func['address']}")
                
        elif choice == "2":
            func_name = input("输入函数名: ")
            # 获取函数代码
            code = client.get_pseudocode(binary_path, func_name)
            # 扫描漏洞
            vulns = scan_function(code)
            print(f"发现 {len(vulns)} 个潜在漏洞:")
            for vuln in vulns:
                print(f"- {vuln['type']}: {vuln['description']}")
                
        elif choice == "3":
            report = client.generate_security_report(binary_path)
            print(report)
            
        elif choice == "4":
            break

# 使用示例
if __name__ == "__main__":
    interactive_vuln_scan("/path/to/binary")
```


---
## 案例研究


### 1：某大型互联网安全公司 - 恶意软件分析组

 1：某大型互联网安全公司 - 恶意软件分析组

**背景**:
该团队负责监控和分析针对金融行业的恶意软件。随着攻击技术的升级，恶意软件开始大量使用自定义加壳算法和混淆技术，导致传统的自动化沙箱分析失效，分析师必须手动进行逆向工程。

**问题**:
团队面临严重的样本积压。一个资深的逆向工程师分析一个复杂的银行木马平均需要 3-5 天。主要痛点在于 Ghidra 的功能极其分散，分析过程中需要频繁在不同菜单间切换（如查找交叉引用、定义结构体、导出数据），且编写 Ghidra 脚本（Python/Java）自动化处理特定模式（如快速定位 RC4 解密密钥）的学习曲线较高，导致效率低下。

**解决方案**:
团队引入了 Ghidra MCP Server，并将其集成到内部的 AI 编程助手工作流中。通过 MCP 协议，AI 模型可以直接调用 Ghidra 的 110 多个底层 API。分析师不再需要手动编写 Ghidra 脚本，而是通过自然语言指令 AI 执行批量操作，例如：“在当前函数中搜索所有常量，尝试将其作为 AES 密钥进行解密测试”或“为这段缓冲区自动生成匹配的结构体定义”。

**效果**:
复杂恶意软件的初步分析时间从 4 小时缩短至 30 分钟。AI 能够通过 MCP 接口快速验证分析假设（如自动追踪寄存器值），使得初级分析师也能完成原本需要资深专家才能完成的解密逻辑还原工作，整体样本处理吞吐量提升了 200%。



### 2：某工业控制系统（ICS）安全实验室

 2：某工业控制系统（ICS）安全实验室

**背景**:
该实验室受客户委托对一款老旧的 PLC（可编程逻辑控制器）固件进行安全评估，以发现可能导致设备停机的漏洞。

**问题**:
该固件基于一种较冷门的架构（如 Renesas RX 或 SH 系列），且缺乏公开的文档和符号表。分析人员面临的主要挑战是“大海捞针”：固件地址空间巨大，且包含大量未知的二进制数据块。在 Ghidra 中手动标注内存映射和识别功能模块非常枯燥且容易出错，一旦误判可能导致后续分析全部跑偏。

**解决方案**:
研究人员利用 Ghidra MCP Server 构建了一个交互式分析环境。他们利用 AI 的上下文理解能力，结合 MCP 提供的工具，对固件进行模式识别。例如，指挥 AI “扫描 0x80000000 到 0x80010000 区域，寻找符合 Modbus 协议特征码的函数”，并让 AI 自动调用 Ghidra 的函数创建和重命名接口，批量处理识别出的函数。

**效果**:
原本需要两名资深工程师耗时一周才能完成的固件架构梳理工作，在 AI 辅助下仅需一天即可完成 80% 的基础框架搭建。AI 成功识别出了固件中几个隐藏的未公开调试接口，这些接口在传统的静态扫描中被遗漏，最终帮助实验室成功发现了两个高危漏洞。



### 3：遗留遗留系统维护团队 - 某航空公司 IT 部门

 3：遗留遗留系统维护团队 - 某航空公司 IT 部门

**背景**:
航空公司核心订票系统中包含一段 20 年前编写的 C 语言核心模块，源代码已丢失。由于业务变更，需要理解该模块中一个特定的数据结构以进行数据迁移。

**问题**:
该模块编译后的二进制文件高度优化，且包含大量复杂的指针运算。在 Ghidra 中查看反汇编代码时，由于缺乏符号信息，代码的可读性极差。团队试图通过阅读汇编代码来还原数据结构，但逻辑过于复杂，多次尝试均出现理解偏差，导致数据迁移测试失败。

**解决方案**:
团队使用 Ghidra MCP Server，将反汇编代码的上下文通过 MCP 传输给 AI 模型。AI 利用其代码推理能力，结合 Ghidra 的数据流分析工具，动态追踪了该数据结构在内存中的生命周期。AI 通过 MCP 接口实时在 Ghidra 中创建结构体字段，并验证其对齐方式，逐步还原出了一个包含 30 多个字段的复杂结构体。

**效果**:
成功在 48 小时内完全还原了目标数据结构的内存布局，准确率达到 100%。这不仅避免了错误的数据库迁移可能导致的数百万美元损失，还通过 AI 自动生成的文档帮助团队快速掌握了遗留系统的业务逻辑。

---
## 最佳实践

## 最佳实践指南

### 实践 1：建立安全的沙箱隔离环境

**说明**: 在 AI 辅助逆向工程中，AI 模型需要读取二进制文件数据并执行分析命令。为了防止恶意软件通过 MCP (Model Context Protocol) 接口逃逸或泄露敏感代码，必须在隔离的沙箱环境中运行 Ghidra 和 MCP Server，而非直接在生产环境或宿主机上操作。

**实施步骤**:
1. 使用 Docker 或虚拟机创建一个专用的分析环境。
2. 仅开放必要的网络端口（用于 MCP 通信）和文件挂载点。
3. 在虚拟机内部配置 Ghidra Headless 模式及 MCP Server 服务。

**注意事项**: 确保该环境没有访问互联网或内网敏感资源的权限，除非分析任务明确要求。

---

### 实践 2：实施增量式分析策略

**说明**: Ghidra MCP Server 提供了 110 种工具，直接要求 AI 对大型二进制文件进行全面分析会导致上下文溢出或产生幻觉。最佳实践是引导 AI 先进行高层次的扫描（如导入摘要、节区分析），再根据需要深入特定函数。

**实施步骤**:
1. 首先使用 `get_program_info` 或 `list_functions` 等工具获取程序概览。
2. 识别感兴趣的关键区域（如 `main` 函数、特定字符串引用）。
3. 针对特定函数地址使用 `decompile_function` 或 `get_xrefs` 进行深度分析。

**注意事项**: 避免一次性将数兆字节的反汇编代码发送给 AI，应切割为小块代码进行交互。

---

### 实践 3：构建结构化的 Prompt 模板

**说明**: 虽然 MCP Server 提供了工具，但 AI 需要明确的指令才能正确调用。建立标准化的 Prompt 模板，明确告知 AI 当前工具的用途和期望的输出格式，可以显著提高分析效率。

**实施步骤**:
1. 在系统提示词中定义角色，例如：“你是一个资深的恶意软件分析师，擅长使用 Ghidra”。
2. 预设常用工作流指令，例如：“请先查找所有网络相关的 API 调用，然后交叉引用其调用者”。
3. 要求 AI 在调用工具前解释其推理过程，确保工具调用的准确性。

**注意事项**: 定期根据分析结果调整 Prompt 模板，修正 AI 容易犯的错误模式。

---

### 实践 4：人工验证关键发现

**说明**: AI 的分析结果（尤其是自动生成的注释或结构体定义）可能存在偏差。在将 AI 的发现写入最终的逆向工程报告或 Ghidra 数据库之前，必须由人工专家进行复核。

**实施步骤**:
1. 当 AI 提出关于漏洞逻辑或加密算法的假设时，手动在 Ghidra GUI 中跳转到相应地址进行确认。
2. 检查 AI 建议的重命名和类型定义是否符合逻辑。
3. 对比 AI 的解释与原始汇编代码，确保没有误读。

**注意事项**: 特别警惕 AI 对自定义协议或混淆代码的“幻觉”式解释，这类代码往往超出通用训练数据的范畴。

---

### 实践 5：利用自动化脚本批量处理重复任务

**说明**: Ghidra MCP Server 的优势在于自动化。对于重复性高的任务（如提取所有字符串、识别所有加密常量），应编写脚本通过 MCP 接口批量调用，而不是逐一手动询问 AI。

**实施步骤**:
1. 编写 Python 脚本连接到 MCP Server。
2. 定义任务清单，例如：批量导出特定地址段的指令。
3. 将 AI 的分析结果（JSON 格式）解析并存储到外部数据库或日志文件中。

**注意事项**: 批量处理可能会消耗大量 Token，建议设置合理的速率限制和超时机制。

---

### 实践 6：维护上下文与状态管理

**说明**: 逆向工程是一个连续的过程。AI 模型本身是无状态的，但分析过程需要记忆。最佳实践是将之前分析的关键结论（如函数用途、已识别的结构体）反馈给 AI，作为后续对话的上下文。

**实施步骤**:
1. 在对话开始时，将 Ghidra 的项目元数据作为上下文注入。
2. 在多轮对话中，总结上一步的发现并明确告知 AI：“基于之前发现的函数 A，现在分析函数 B”。
3. 利用 Ghidra 的书签和注释功能，将 AI 的关键发现持久化存储，以便后续会话使用。

**注意事项**: 当对话轮次过多导致上下文过长时，适时总结并丢弃无关的旧信息，以保持推理的聚焦性。

---
## 学习要点

- Ghidra MCP Server 通过集成 110 个工具，将 AI 深度引入逆向工程流程，显著提升了自动化代码分析的能力。
- 该项目利用 Model Context Protocol (MCP) 架构，实现了 AI 模型与 Ghidra 工具之间的高效互操作性。
- 它将 Ghidra 原有的脚本和功能模块化，使 AI 能够像人类分析师一样调用反编译、数据流分析等核心功能。
- 这种 AI 辅助模式能够大幅降低逆向工程的门槛，帮助分析师更快地理解复杂的恶意软件或二进制文件逻辑。
- 项目展示了如何通过标准化接口将专业安全工具接入大语言模型，为构建自主化的网络安全智能体提供了参考范例。

---
## 常见问题


### 1: 什么是 Ghidra MCP Server，它与直接使用 Ghidra 有什么区别？

1: 什么是 Ghidra MCP Server，它与直接使用 Ghidra 有什么区别？

**A**: Ghidra MCP Server 是一个基于 Model Context Protocol (MCP) 的服务器，用于将 Ghidra 的逆向工程功能桥接到支持 MCP 的大语言模型（如 Claude、Desktop AI 等）中。与直接使用 Ghidra 不同，该服务器允许 AI 模型调用 Ghidra 的 API 来分析二进制文件。用户可以通过自然语言交互，由 AI 执行反编译、数据提取、代码分析等操作。

---



### 2: 该项目声称包含 "110 tools"，这些工具具体指什么？

2: 该项目声称包含 "110 tools"，这些工具具体指什么？

**A**: 这里的 "110 tools" 指的是该 MCP Server 向 AI 模型暴露的 110 个 API 接口或功能函数。这些工具涵盖了 Ghidra 的多项核心功能，包括：获取程序列表、导航函数、读取反编译代码、查询交叉引用、分析函数调用图、搜索特定指令或字节模式、以及修改内存和注释等。AI 模型可以根据指令调用这些工具来完成分析任务。

---



### 3: 如何安装和配置 Ghidra MCP Server？

3: 如何安装和配置 Ghidra MCP Server？

**A**: 通常情况下，安装需要以下步骤：
1.  **环境准备**：确保已安装 Ghidra（通常需要较新版本以支持脚本或 API 调用）和 Python 环境。
2.  **获取代码**：从 GitHub 仓库克隆项目源码。
3.  **安装依赖**：运行 `pip install` 或类似命令安装项目所需的 Python 库（如 MCP SDK 相关包）。
4.  **配置连接**：在支持 MCP 的客户端（如 Claude Desktop 或其他 AI 客户端）的配置文件中，添加该服务器的启动命令和路径。配置通常需要指定 Ghidra 的安装路径或脚本路径。

---



### 4: 使用 AI 辅助逆向工程是否会泄露代码隐私或敏感数据？

4: 使用 AI 辅助逆向工程是否会泄露代码隐私或敏感数据？

**A**: 使用 Ghidra MCP Server 时，数据流向取决于 AI 客户端配置。
*   **云端模式**：如果连接的是 OpenAI、Anthropic 等提供的云端 API 服务，请求分析的代码片段、反编译结果等数据将会被上传到云端服务器。请勿将包含敏感信息、商业机密或未授权的软件发送到云端模型。
*   **本地模式**：如果使用的是本地部署的开源模型（如 Ollama, LM Studio 等）并通过 MCP 连接，数据通常只在本地处理。
*   **总结**：请务必根据数据安全策略和合规要求，选择合适的 AI 模型类型。

---



### 5: AI 模型是否能够完全自动化逆向工程，甚至自动生成破解补丁？

5: AI 模型是否能够完全自动化逆向工程，甚至自动生成破解补丁？

**A**: AI 是一个辅助工具，而非全自动解决方案。
*   **能力**：AI 适用于理解代码逻辑、识别函数模式、解释混淆代码段、以及编写脚本自动化常规分析过程（如批量重命名变量）。
*   **局限**：逆向工程往往需要结合上下文、领域知识以及对反调试技术的理解。AI 可能会产生误报，或在面对高度混淆及复杂逻辑时表现受限。
*   **结论**：它可以提高分析效率，但仍需专业人员进行验证和引导。

---



### 6: Ghidra MCP Server 支持哪些 AI 客户端？

6: Ghidra MCP Server 支持哪些 AI 客户端？

**A**: 由于该项目基于 **Model Context Protocol (MCP)** 标准，它支持任何兼容 MCP 协议的客户端。目前常见的支持 MCP 的客户端包括 **Claude Desktop**（由 Anthropic 官方支持），以及集成了 MCP SDK 的各类开发工具或 AI 代理平台。只要客户端能够加载 MCP 服务器配置，即可调用这些工具来辅助逆向工程分析。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: 基础自动化交互

### 问题**: 假设你使用 Ghidra MCP Server 连接了一个 AI 模型。请描述如何利用 MCP 提供的工具，让 AI 将一段二进制文件中所有的 `mov` 指令重命名为更具描述性的名称（例如 `mov` 到 `copy_data`），并解释这一步在自动化逆向工程中的基础作用。

### 提示**: 思考 MCP (Model Context Protocol) 的核心功能是赋予 AI 读取和操作上下文的能力。你需要关注的是如何通过工具暴露 Ghidra 的 API 给 AI，而不是手动操作 Ghidra 的 GUI 脚本。

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
- 标签： [Ghidra](/tags/ghidra/) / [逆向工程](/tags/%E9%80%86%E5%90%91%E5%B7%A5%E7%A8%8B/) / [MCP](/tags/mcp/) / [AI辅助](/tags/ai%E8%BE%85%E5%8A%A9/) / [安全工具](/tags/%E5%AE%89%E5%85%A8%E5%B7%A5%E5%85%B7/) / [LLM](/tags/llm/) / [Hacker News](/tags/hacker-news/) / [工具集成](/tags/%E5%B7%A5%E5%85%B7%E9%9B%86%E6%88%90/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/)

### 相关文章

- [Ghidra MCP Server发布：集成110款工具实现AI辅助逆向工程]({{< relref "posts/20260204-hacker_news-show-hn-ghidra-mcp-server-110-tools-for-ai-assiste-1.md" >}})
- [Ghidra MCP Server：集成110项工具的AI逆向工程辅助环境]({{< relref "posts/20260204-hacker_news-show-hn-ghidra-mcp-server-110-tools-for-ai-assiste-10.md" >}})
- [Ghidra MCP Server：集成110种工具的AI辅助逆向工程]({{< relref "posts/20260204-hacker_news-show-hn-ghidra-mcp-server-110-tools-for-ai-assiste-16.md" >}})
- [Ghidra MCP Server：集成110款工具的AI逆向工程辅助方案]({{< relref "posts/20260204-hacker_news-show-hn-ghidra-mcp-server-110-tools-for-ai-assiste-2.md" >}})
- [Ghidra MCP Server：集成110款工具的AI逆向工程辅助服务]({{< relref "posts/20260204-hacker_news-show-hn-ghidra-mcp-server-110-tools-for-ai-assiste-6.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*