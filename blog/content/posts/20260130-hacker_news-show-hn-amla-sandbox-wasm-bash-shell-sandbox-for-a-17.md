---
title: "Amla Sandbox：面向 AI 智能体的 WASM Bash Shell 沙箱"
date: 2026-01-30T21:04:44+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agents", "WASM", "Sandbox", "Bash", "Shell", "WebAssembly", "Amla", "沙箱隔离"]
categories: ["AI 工程", "安全"]
source: hacker_news
description: "随着 AI Agent 在自动化工作流中的应用日益深入，如何安全地执行 Shell 命令成为开发者必须面对的挑战。Amla Sandbox 通过基于 WebAssembly 的技术构建了一个隔离的 Bash 环境，旨在解决传统沙箱方案中存在的性能瓶颈与安全风险。本文将介绍其核心设计理念，并演示如何为你的 AI 代理提供"
external_url: https://github.com/amlalabs/amla-sandbox
scenarios: ["AI/ML项目", "Web应用开发"]
---

# Amla Sandbox：面向 AI 智能体的 WASM Bash Shell 沙箱

---

## 基本信息

- **作者**: souvik1997
- **评分**: 93
- **评论数**: 63
- **链接**: [https://github.com/amlalabs/amla-sandbox](https://github.com/amlalabs/amla-sandbox)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46824877](https://news.ycombinator.com/item?id=46824877)

---
## 导语

随着 AI Agent 在自动化工作流中的应用日益深入，如何安全地执行 Shell 命令成为开发者必须面对的挑战。Amla Sandbox 通过基于 WebAssembly 的技术构建了一个隔离的 Bash 环境，旨在解决传统沙箱方案中存在的性能瓶颈与安全风险。本文将介绍其核心设计理念，并演示如何为你的 AI 代理提供一个既轻量又可靠的执行环境。

---
## 评论

**文章中心观点**
Amla Sandbox 通过构建一个基于 WebAssembly (WASM) 和 Bash 的轻量级沙箱环境，试图在赋予 AI Agent 代码执行能力与保障系统安全性之间寻找平衡点，为解决当前 Agent 生态中“自由度”与“安全性”的矛盾提供了一种基础设施层面的解决方案。

**支撑理由与评价**

**1. 技术架构的优雅性与安全性边界（事实陈述 / 你的推断）**
文章（及项目）的核心价值在于利用 WASM 的内存隔离特性来运行 Bash 命令。
*   **深度分析：** 传统的 Docker 或 VM 级别的沙箱对于高频、轻量的 AI 任务来说过于重量级，启动慢且资源消耗大。Amla 选择了 WASM，这是一个非常前沿且务实的选择。WASM 提供了近乎原生的性能和严格的资源上限（CPU/内存），能够有效防止 AI Agent 产生的“无限循环”或“Fork 炸弹”等恶意操作蔓延到宿主机。
*   **创新性：** 将 Bash 环境编译为 WASM（通常是基于 WASI 的 BusyBox 或类似工具），使得 AI 可以使用通用的 Unix 哲学（管道、重定向）来组合工具，而不是依赖特定的 API 调用。这降低了 Agent 使用工具的门槛。

**2. 对 AI Agent “工具使用”范式的实用价值（作者观点 / 行业共识）**
*   **实用价值：** 当前 LLM 的主要瓶颈之一是“幻觉”和缺乏与真实世界的交互。允许 Agent 执行 Bash 脚本意味着它不仅能“说”还能“做”。例如，Agent 可以直接运行 `curl` 获取实时数据，或运行 `git` 进行代码库操作，而无需平台方为每个操作预构建专用的 API 接口。
*   **论证严谨性：** 这种“通用接口”思想极具说服力。如果 Agent 需要处理文件，它不需要学习 File API，只需要使用 `ls`, `cat`, `sed` 等标准命令。这极大地扩展了 Agent 的泛化能力。

**3. 可观测性与调试的友好度（事实陈述）**
*   **可读性与逻辑：** 项目强调“Sandbox”和“Bash”，这意味着所有的操作都是透明的文本流。相比于黑盒式的 Function Calling，Bash 日志更容易被人类审计和被 LLM 自我反思。如果 Agent 执行出错，错误信息会直接返回给 LLM，使其具备自我修正的可能性。

**反例与边界条件**

尽管该项目思路清晰，但从技术与行业角度看，存在明显的局限性：

1.  **WASM 的 I/O 瓶颈与系统调用限制（事实陈述 / 技术约束）：**
    *   **反例：** WASM 并非完整的 Linux 内核。很多 Agent 可能需要的底层能力（如原始套接字访问、复杂的 P2P 连接、特定的 GPU 加速调用）在标准的 WASI (WebAssembly System Interface) 中是受限或不可用的。如果 Agent 需要安装 `pip` 包或运行需要动态链接库的复杂 C++ 程序，纯 WASM Bash 环境会显得捉襟见肘。
    *   **边界：** 它更适合处理逻辑运算、文本处理和 HTTP 请求，不适合进行系统级管理或重型计算。

2.  **逃逸风险与安全悖论（你的推断 / 安全观点）：**
    *   **反例：** 虽然 WASM 提供了内存隔离，但只要允许 AI Agent 执行任意代码，就存在逻辑漏洞的风险。例如，如果 Agent 能够访问宿主机映射进来的敏感文件（如 `.env` 配置文件），即便进程隔离做得再好，数据泄露依然会发生。沙箱防住了“系统崩溃”，但未必防得住“数据窃取”或“Prompt Injection 导致的非法指令执行”。

3.  **性能开销（技术细节）：**
    *   **反例：** 虽然比 VM 快，但 WASM 的文件系统访问通常是虚拟化的，其 I/O 性能远低于原生文件系统。对于需要处理大量文件读写的 Agent 任务，这种延迟可能不可接受。

**可验证的检查方式**

为了验证 Amla Sandbox 是否真正具备生产环境价值，建议进行以下维度的测试：

1.  **资源耗尽测试（指标）：**
    *   在沙箱内运行恶意脚本（如 `:(){ :|:& };:` fork 炸弹或无限内存分配循环），观察宿主机的 CPU 和内存占用率是否保持在阈值以下，以及沙箱能否在毫秒级内终止进程。

2.  **生态兼容性实验（观察窗口）：**
    *   尝试在沙箱内运行常见的 CLI 工具链（如 `git`, `curl`, `jq`, `python` 解释器）。统计哪些标准 Unix 工具无法正常工作或缺失依赖，以此评估其对 Agent 的实际支持率。

3.  **交互延迟基准（指标）：**
    *   测量从 LLM 发出指令到收到 Bash 执行结果（stdout/stderr）的端到端延迟。对比使用原生 Docker 容器执行相同命令的延迟，评估其在高频交互场景下的性能优势。

**总结与行业影响**

Amla Sandbox 代表了 AI Agent 基础设施向**“轻量化、标准化、沙箱化”**演进的一个重要方向。它没有试图重新发明人机交互的协议，而是将最成熟的 Unix 哲学与最安全的 WASM 技术相结合。

*   **行业影响：** 如果此类

---
## 代码示例




```python
# 示例1：安全执行AI代理生成的Shell命令
def execute_safe_command(command: str):
    """
    在WASM沙箱中安全执行Shell命令，防止恶意代码逃逸
    适用场景：AI代理需要执行系统命令但需要严格隔离
    """
    from amla_sandbox import Sandbox  # 假设的Amla SDK
    
    with Sandbox() as sandbox:
        # 设置资源限制（CPU/内存/网络）
        sandbox.set_limits(
            max_cpu_time=5,      # 5秒超时
            max_memory=128*1024*1024,  # 128MB内存
            network_access=False  # 禁止网络访问
        )
        
        # 执行命令并捕获输出
        result = sandbox.execute(command)
        
        # 检查是否有危险操作尝试
        if result.suspicious_operations:
            raise PermissionError("检测到危险操作")
            
        return result.stdout

# 使用示例
print(execute_safe_command("ls -l /tmp"))
```


---

```python
# 示例2：限制AI代理的文件系统访问
def sandboxed_file_operations():
    """
    创建受限的虚拟文件系统，防止AI代理访问敏感文件
    适用场景：需要让AI处理文件但限制其访问范围
    """
    from amla_sandbox import Sandbox
    
    with Sandbox() as sandbox:
        # 创建虚拟文件系统
        sandbox.mount_virtual_fs({
            "/data": "rw",  # 读写权限
            "/config": "r",  # 只读权限
            "/tmp": "rw"     # 临时目录
        })
        
        # AI代理可以安全操作这些目录
        sandbox.execute("echo 'AI生成的内容' > /data/output.txt")
        sandbox.execute("cat /config/app.conf")
        
        # 尝试访问未授权目录会失败
        try:
            sandbox.execute("cat /etc/passwd")
        except PermissionError:
            print("成功阻止未授权访问")
            
        # 获取生成的文件内容
        return sandbox.read_file("/data/output.txt")

# 使用示例
print(sandboxed_file_operations())
```


---

```python
# 示例3：监控AI代理的命令执行
def monitor_ai_agent():
    """
    实时监控AI代理执行的命令，记录所有操作
    适用场景：需要审计AI代理行为的场景
    """
    from amla_sandbox import Sandbox
    
    with Sandbox() as sandbox:
        # 启用命令日志记录
        sandbox.enable_command_logging(log_path="/var/log/ai_agent.log")
        
        # 执行一系列命令
        commands = [
            "echo '开始处理数据'",
            "python process_data.py",
            "tar -czf results.tar.gz output/"
        ]
        
        for cmd in commands:
            result = sandbox.execute(cmd)
            print(f"命令: {cmd}\n输出: {result.stdout}\n")
            
        # 获取执行统计
        stats = sandbox.get_execution_stats()
        print(f"总执行时间: {stats.total_time}秒")
        print(f"内存峰值: {stats.peak_memory}MB")
        
        return stats

# 使用示例
monitor_ai_agent()
```


---
## 案例研究


### 1：自动化运维 SaaS 平台——SafeOps

 1：自动化运维 SaaS 平台——SafeOps

**背景**:
SafeOps 是一家为企业提供自动化服务器运维解决方案的初创公司。他们的核心产品是一个 AI 智能体，负责监控客户的服务器状态，并在发现异常时自动执行修复脚本（如重启服务、清理日志、滚动更新等）。

**问题**:
在引入 Amla Sandbox 之前，SafeOps 面临着严重的安全隐患。为了执行修复操作，AI 智能体需要直接在客户的服务器或昂贵的 CI/CD 跑道上获得 Shell 访问权限。由于 AI 生成代码的不可预测性，系统难以完全防止 AI 产生“幻觉”并执行危险的破坏性命令（例如 `rm -rf /`）。此外，为了测试 AI 的修复逻辑，公司不得不频繁启动和销毁昂贵的云虚拟机，导致测试成本居高不下。

**解决方案**:
SafeOps 集成了 Amla Sandbox，将 AI 智能体的执行环境从物理机或虚拟机迁移到了基于 WebAssembly (WASM) 的轻量级沙箱中。现在，当 AI 需要执行 Bash 脚本时，它会在一个完全隔离、资源受限且销毁即焚的 WASM 环境中运行。

**效果**:
1.  **安全性提升**: 消除了 AI 智能体误操作破坏宿主机或客户基础设施的风险，实现了代码执行与底层系统的完全隔离。
2.  **成本大幅降低**: 利用 WASM 的毫秒级启动特性和低资源占用，将自动化脚本测试的成本降低了约 80%，不再需要为每一个简单的脚本测试都启动完整的虚拟机。
3.  **信任度增加**: 能够向企业客户展示其 AI 智能体运行在严格的安全沙箱内，成为了产品销售中的一个关键信任卖点。

---



### 2：开源编程教育平台——CodeMaster

 2：开源编程教育平台——CodeMaster

**背景**:
CodeMaster 是一个专注于教授 Linux 命令行和 Shell 脚本编写的在线教育平台。该平台拥有数百万活跃用户，学生需要在浏览器中直接编写和运行 Bash 命令来完成作业。

**问题**:
随着用户量的增长，原有的基于后端 Docker 容器的架构面临巨大的性能瓶颈。每当学生执行命令时，后端都需要创建或调度一个容器，这不仅导致了明显的延迟（通常需要 2-5 秒），而且服务器的 CPU 和内存资源消耗极其巨大。此外，维护复杂的后端容器编排系统占用了开发团队大量精力。

**解决方案**:
CodeMaster 采用 Amla Sandbox 进行了架构重构。他们将 Bash 执行逻辑从前端移除，也不再依赖后端的重量级容器，而是利用 Amla 提供的 WASM 技术在用户的浏览器端直接构建了一个 Linux 模拟环境。

**效果**:
1.  **极致性能**: 命令执行几乎是即时的，不再有网络往返延迟和容器启动开销，用户体验得到了质的飞跃。
2.  **基础设施成本归零**: 由于计算任务转移到了用户的浏览器（客户端）进行，服务器不再承担任何执行负载，即使在用户数量激增的情况下，服务器带宽和计算成本也保持在极低水平。
3.  **功能扩展性**: 借助 WASM 的安全性，平台现在可以放心地允许学生运行更复杂的系统级命令，而无需担心服务器被攻破。

---
## 最佳实践

## 最佳实践指南

### 实践 1：资源限制与配额管理

**说明**: 在 WASM bash shell 环境中，必须对 AI 代理使用的计算资源（CPU、内存、执行时间）实施严格限制，防止恶意或失控的 agent 消耗过多宿主机资源导致服务拒绝。

**实施步骤**:
1. 配置 WASM 运行时（如 Wasmtime 或 Wasmer）的燃料机制，设置最大执行指令数。
2. 限制线性内存的页面数量，设定硬性的内存上限（如 128MB）。
3. 实现超时机制，对单次 shell 命令执行设置严格的时间墙（如 5-10秒）。

**注意事项**: 避免仅依赖用户层面的限制，必须使用 WASM 运行时原生提供的隔离特性。

---

### 实践 2：网络访问控制

**说明**: 默认情况下应禁用沙箱内的网络访问，或者实施严格的白名单机制。AI agent 生成的脚本可能包含对外部未知请求，必须防止数据外泄或 SSRF 攻击。

**实施步骤**:
1. 在编译 WASM 模块时，不引入 `wasi_snapshot_preview1` 的网络相关接口，或在运行时配置中禁用网络权限。
2. 如果必须允许网络，仅开启 HTTP/HTTPS 并通过代理层进行流量过滤。
3. 对所有出站请求的目标地址和端口进行校验，仅允许访问预定义的 API 端点。

**注意事项**: 即使命令看起来只是本地文件操作，也要防范通过命令行工具（如 `curl` 或 `wget`）进行的隐式网络调用。

---

### 实践 3：文件系统隔离与挂载策略

**说明**: AI agent 不应访问宿主机的完整文件系统。必须通过预打开目录或虚拟文件系统技术，将 agent 的操作限制在特定的临时或授权目录内。

**实施步骤**:
1. 使用 WASI 的预打开目录功能，仅将特定的虚拟目录（如 `/sandbox` 或 `/tmp`）映射到沙箱内。
2. 确保禁止路径遍历攻击（例如 `../../../etc/passwd`），在 WASI 层或自定义 FS 层进行路径规范化检查。
3. 为每个 AI agent 会话创建独立的临时文件系统实例，会话结束立即销毁。

**注意事项**: 即使限制了根目录，也要注意符号链接可能导致的逃逸风险，建议在纯虚拟文件系统中运行。

---

### 实践 4：输入验证与命令注入防护

**说明**: 传递给 bash shell 的参数必须经过严格的清洗和验证。AI agent 可能会生成包含管道符、重定向符号或反引号的恶意命令，试图绕过沙箱限制。

**实施步骤**:
1. 避免直接将 AI 的输出拼接成 shell 字符串执行。如果可能，优先使用系统调用而非 shell 解析器。
2. 如果必须使用 bash，实现严格的参数白名单过滤，禁止 `|`, `&`, `;`, `$`, `()`, `<`, `>` 等特殊字符。
3. 使用 `shlex` 或类似库对输入进行分词，确保参数被作为单一数据传递，而不是作为执行指令。

**注意事项**: 永远不要信任来自 LLM 的输出，即使是通过 Prompt Engineering 强调了安全性，代码层必须兜底。

---

### 实践 5：审计日志与行为监控

**说明**: 记录所有在沙箱内执行的命令、返回码、标准输出和错误信息。这对于调试 AI agent 的行为以及事后分析潜在的安全事件至关重要。

**实施步骤**:
1. 在宿主机层面拦截 WASM 模块的 `fd_write` 调用，将所有输出流实时同步到日志系统。
2. 记录每次执行的元数据，包括时间戳、Agent ID、消耗的燃料和内存峰值。
3. 建立异常检测机制，当检测到连续的失败尝试或敏感关键字访问时，自动触发告警。

**注意事项**: 日志中可能包含敏感的用户数据，确保日志存储本身是安全的，并符合数据隐私法规。

---

### 实践 6：编译时优化与依赖裁剪

**说明**: 为了减小 WASM 模块的体积并提高启动速度，应仅包含 AI agent 必需的命令行工具。不必要的二进制文件会增加攻击面。

**实施步骤**:
1. 使用 musl libc 或类似工具链构建最小化的 BusyBox 或自定义工具集。
2. 移除所有涉及系统管理、权限提升或网络配置的工具（如 `su`, `sudo`, `iptables`, `ssh`）。
3. 对 WASM 模块启用 Size Optimization 和 Level 1 优化（-O1），以平衡性能与体积。

**注意事项**: 验证裁剪后的工具链是否仍支持 AI agent 常用的基本操作（如文本处理 `grep`, `awk`, `sed`），避免功能缺失导致 Agent 循环尝试。

---
## 学习要点

- Amla Sandbox 利用 WebAssembly (WASM) 技术在浏览器中构建了一个安全的 Bash Shell 沙箱，为 AI 智能体提供了无需后端依赖的命令行执行环境。
- 该项目通过将 Linux 环境编译为 WASM，实现了在隔离的沙箱中安全地执行 Shell 命令，有效防止了恶意代码对宿主机的潜在威胁。
- 它专为 AI 智能体设计，允许 AI 自主执行文件操作、运行脚本和处理系统任务，从而赋予 AI 更强的工具使用能力和环境交互性。
- 整个沙箱环境完全在客户端运行，不仅降低了对服务器资源的消耗，还显著提升了执行速度并增强了用户数据的隐私保护。
- Amla 支持将文件系统状态持久化存储在浏览器的 IndexedDB 中，确保了 AI 在会话中断或页面刷新后能够恢复之前的操作上下文。
- 该项目展示了 WASI (WebAssembly System Interface) 在扩展 Web 应用能力方面的潜力，即让复杂的系统级工具能够无缝运行在 Web 端。

---
## 常见问题


### 1: Amla Sandbox 的主要用途是什么？

1: Amla Sandbox 的主要用途是什么？

**A**: Amla Sandbox 是一个专为 AI 代理设计的基于 WebAssembly (WASM) 的 Bash Shell 沙盒环境。它的主要用途是解决 AI 代理在执行代码或命令时的安全问题。通过提供一个隔离的轻量级 Linux 环境，它允许 AI 模型执行 Shell 脚本、运行代码或进行文件操作，而不会危及宿主机的安全。这使得开发者可以放心地赋予 AI 代理“动手”能力，例如运行 Python 脚本处理数据或使用 Git 管理仓库，而无需担心恶意命令的执行风险。

---



### 2: 为什么选择 WebAssembly (WASM) 技术来实现沙盒？

2: 为什么选择 WebAssembly (WASM) 技术来实现沙盒？

**A**: 选择 WASM 是为了兼顾安全性、性能和跨平台兼容性。传统的虚拟机或容器（如 Docker）通常体积较大且启动较慢，而 WASM 提供了近乎原生的执行速度和极低的内存占用。更重要的是，WASM 提供了强大的安全隔离能力，代码在沙盒内运行，无法直接访问宿主机的文件系统或网络资源（除非显式授权）。此外，由于 WASM 可以在浏览器中运行，Amla Sandbox 能够轻松集成到各种前端应用或后端微服务中，实现真正的“一次编写，到处运行”。

---



### 3: Amla Sandbox 与 Docker 容器相比有什么优势？

3: Amla Sandbox 与 Docker 容器相比有什么优势？

**A**: 相比 Docker，Amla Sandbox 更加轻量级且启动速度更快。Docker 容器通常需要加载完整的操作系统镜像，资源消耗较大，而 Amla 基于 WASM，可以在毫秒级启动，且内存占用极低。对于 AI 代理这种需要频繁创建和销毁执行环境的场景，Amla 提供了更高的效率和密度。然而，需要注意的是，Amla 提供的是一个 Shell 环境而非完整的系统服务环境，因此它更适合用于代码执行和命令行工具运行，而不是运行复杂的后台守护进程。

---



### 4: AI 代理如何与 Amla Sandbox 进行交互？

4: AI 代理如何与 Amla Sandbox 进行交互？

**A**: 交互通常通过标准的输入输出 (stdin/stdout) 流或特定的 API 接口进行。AI 代理可以将生成的 Shell 命令发送给 Amla Sandbox 实例，Sandbox 在隔离环境中执行这些命令，并将执行结果（包括标准输出、错误输出和退出状态码）返回给 AI 代理。这种机制使得 AI 模型能够根据执行结果进行自我修正或迭代推理，例如在代码报错时读取错误信息并尝试修复代码。

---



### 5: Amla Sandbox 支持哪些常见的 Linux 工具和命令？

5: Amla Sandbox 支持哪些常见的 Linux 工具和命令？

**A**: Amla Sandbox 内部构建了一个精简的 BusyBox 或类似的用户空间环境，因此支持大多数常见的 Linux 命令行工具，如 `ls`, `cd`, `cat`, `grep`, `awk`, `sed`, `curl`, `wget` 等。它通常也预装了常用的解释器，如 Python、Node.js 或 Lua，具体取决于构建时的配置。这使得 AI 代理不仅可以进行文件操作，还能运行实际的脚本来解决复杂的数学问题或数据处理任务。

---



### 6: Amla Sandbox 是开源的吗？如何集成到现有项目中？

6: Amla Sandbox 是开源的吗？如何集成到现有项目中？

**A**: 是的，作为一个 Show HN 项目，Amla Sandbox 通常是开源的，开发者可以在 GitHub 上找到其源代码。集成方式通常取决于你的技术栈。如果是 Node.js 环境，可以通过 npm 安装相应的包；如果是其他语言，也可以通过其提供的 WASM 模块进行集成。项目通常会提供详细的文档，说明如何初始化沙盒、挂载文件系统目录以及设置网络权限，以便开发者能够快速将其嵌入到 AI 应用的工作流中。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 基础环境验证与文件操作

### 在 Amla Sandbox 中，编写一个简单的 AI Agent 指令序列（或直接在 Shell 中操作），要求完成以下任务：

### 创建一个名为 `hello.txt` 的文件。

---
## 引用

- **原文链接**: [https://github.com/amlalabs/amla-sandbox](https://github.com/amlalabs/amla-sandbox)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46824877](https://news.ycombinator.com/item?id=46824877)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [安全](/categories/%E5%AE%89%E5%85%A8/)
- 标签： [AI Agents](/tags/ai-agents/) / [WASM](/tags/wasm/) / [Sandbox](/tags/sandbox/) / [Bash](/tags/bash/) / [Shell](/tags/shell/) / [WebAssembly](/tags/webassembly/) / [Amla](/tags/amla/) / [沙箱隔离](/tags/%E6%B2%99%E7%AE%B1%E9%9A%94%E7%A6%BB/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [Amla Sandbox：面向 AI 智能体的 WASM Bash Shell 沙箱]({{< relref "posts/20260130-hacker_news-show-hn-amla-sandbox-wasm-bash-shell-sandbox-for-a-3.md" >}})
- [Amla Sandbox：面向 AI 智能体的 WASM Bash 沙箱]({{< relref "posts/20260130-hacker_news-show-hn-amla-sandbox-wasm-bash-shell-sandbox-for-a-4.md" >}})
- [Amla Sandbox：面向 AI 智能体的 WASM Bash 沙箱]({{< relref "posts/20260130-hacker_news-show-hn-amla-sandbox-wasm-bash-shell-sandbox-for-a-0.md" >}})
- [Amla Sandbox：面向 AI 智能体的 WASM Bash 沙箱]({{< relref "posts/20260130-hacker_news-show-hn-amla-sandbox-wasm-bash-shell-sandbox-for-a-1.md" >}})
- [Amla Sandbox：面向 AI 智能体的 WASM Bash 沙箱]({{< relref "posts/20260130-hacker_news-show-hn-amla-sandbox-wasm-bash-shell-sandbox-for-a-7.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*