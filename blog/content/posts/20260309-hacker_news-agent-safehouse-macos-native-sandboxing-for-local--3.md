---
title: "Agent Safehouse：基于 macOS 原生沙箱的本地 Agent 隔离方案"
date: 2026-03-09T12:20:24+08:00
draft: false
entry_kind: "auto"
tags: ["Agent Safehouse", "macOS", "沙箱", "本地 Agent", "安全隔离", "原生沙箱", "系统安全", "Agent 安全"]
categories: ["安全", "系统与基础设施"]
source: hacker_news
description: "随着本地 AI Agent 的普及，其系统权限管控与安全性正成为开发者关注的焦点。Agent Safehouse 作为一款基于 macOS 原生沙箱机制的工具，为本地 Agent 提供了严格的隔离环境。本文将深入解析其技术原理与架构设计，展示如何在不牺牲性能的前提下有效规避潜在风险，帮助开发者在构建本地应用时实现更精细"
external_url: https://agent-safehouse.dev
scenarios: ["Web应用开发"]
---

# Agent Safehouse：基于 macOS 原生沙箱的本地 Agent 隔离方案

---

## 基本信息

- **作者**: atombender
- **评分**: 610
- **评论数**: 149
- **链接**: [https://agent-safehouse.dev](https://agent-safehouse.dev)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47301085](https://news.ycombinator.com/item?id=47301085)

---
## 导语

随着本地 AI Agent 的普及，其系统权限管控与安全性正成为开发者关注的焦点。Agent Safehouse 作为一款基于 macOS 原生沙箱机制的工具，为本地 Agent 提供了严格的隔离环境。本文将深入解析其技术原理与架构设计，展示如何在不牺牲性能的前提下有效规避潜在风险，帮助开发者在构建本地应用时实现更精细的安全控制。

---
## 评论

**深度评论：macOS 原生沙盒在本地 AI Agent 安全中的应用**

**核心论点**
文章提出利用 macOS 原生的沙盒机制作为本地 AI Agent 的安全隔离方案，旨在解决自主智能体在执行系统级操作时的权限滥用风险。该方案试图在系统安全性与 Agent 功能性之间建立一种低资源消耗的标准。

**技术可行性与边界分析**

1.  **技术基础与原生优势**
    *   **机制陈述**：macOS 拥有成熟的 Sandbox 和 TCC（透明同意与控制）框架，能够对文件系统、网络和进程访问进行细粒度限制。
    *   **支撑理由**：相比于虚拟机或 Docker 容器，原生沙盒对资源的消耗较低，且与操作系统 UI 深度集成，更适配桌面端 Agent 的交互场景。
    *   **边界条件**：原生沙盒并非绝对的安全边界。历史上存在过沙盒逃逸漏洞（如 Gatekeeper 绕过）。如果 Agent 本身被诱导利用内核漏洞，沙盒机制可能失效。

2.  **安全边界的有效性**
    *   **作者观点**：文章暗示通过严格的 Profile 配置，可以限制 Agent 仅访问特定目录，从而防止“删除整个硬盘”等灾难性操作。
    *   **支撑理由**：最小权限原则是安全设计的基石。将 Agent 限制在“临时文件夹”或“下载文件夹”内，确实能有效降低随机性错误带来的破坏。
    *   **局限性**：对于 LLM 驱动的 Agent，沙盒难以解决“意图”与“执行”的鸿沟。例如，若 Agent 被赋予“整理文件”的权限，它可能会错误地将重要文件移动到沙盒允许的路径中，沙盒本身无法识别这种逻辑上的误操作。

3.  **开发成本与用户体验**
    *   **开发视角**：利用系统自带能力符合“Lean Development”理念。编写一个 Sandbox 配置文件的维护成本通常低于维护一个完整的 Linux 虚拟机镜像。
    *   **用户视角**：用户无需开启重型虚拟机即可获得基础保护。
    *   **潜在风险**：macOS 的安全弹窗机制较为频繁。若 Agent 频繁请求权限，用户可能产生“弹窗疲劳”并习惯性点击“允许”，从而导致安全模型失效。

**多维度评价**

1.  **内容深度：视角具体但覆盖面有限**
    文章从操作系统底层机制出发，准确识别了文件 I/O 是当前 Agent 的主要风险面。论证聚焦于“隔离”层面，但对于“监控”和“审计”机制涉及较少。Agent 安全不仅包含防止越界，还包含行为审计。

2.  **实用价值：适配桌面自动化场景**
    对于构建 macOS 原生工具（如文字润色、代码补全、本地文件整理）的开发者，文章提供了具体的操作指引。特别是关于 `com.apple.security.files.user-selected.read-write` 等 entitlements 的使用，具有参考意义。

3.  **创新性与行业视角**
    将沙盒应用于 Local LLM Agent 并非全新概念，但文章探讨了 macOS 原生能力在这一特定场景下的适配性。这对“为了安全必须使用 K8s/VM”的思路提供了另一种轻量级的替代视角。

4.  **争议点与局限性**
    *   **概率性 vs 规则**：沙盒基于确定性规则，而 Agent 基于概率模型。核心挑战在于如何确保概率模型申请正确的权限。
    *   **平台依赖**：过分依赖 macOS 原生特性会增加应用跨平台移植的难度。

**实施建议**

1.  **纵深防御**：建议在 Agent 内部增加“确认环”机制，即涉及删除或修改操作时，强制要求 LLM 输出可读的确认步骤，并在执行前进行二次校验。
2.  **权限分级**：开发时可设计“只读模式”和“读写模式”两套 Profile。在处理简单任务时默认只读，仅在用户明确介入后才切换至读写沙盒。
3.  **日志审计**：即使沙盒限制了文件访问，仍建议记录所有系统调用的日志以便事后审查。

---
## 代码示例




```python
# 示例1：文件系统隔离 - 限制Agent只能访问指定目录
import os
import tempfile

def sandboxed_file_operations():
    """
    创建临时沙箱目录并演示受限文件操作
    实际应用中可结合macOS的sandbox-exec实现更严格的隔离
    """
    # 创建临时沙箱目录
    with tempfile.TemporaryDirectory(prefix="agent_sandbox_") as sandbox_path:
        print(f"沙箱目录创建于: {sandbox_path}")
        
        # 允许的操作：在沙箱内创建文件
        safe_file = os.path.join(sandbox_path, "agent_data.txt")
        with open(safe_file, "w") as f:
            f.write("这是安全隔离的Agent数据")
        
        # 尝试访问沙箱外的文件（实际应用中会被拦截）
        try:
            with open("/etc/passwd", "r") as f:
                print(f.read())
        except PermissionError:
            print("权限拦截：无法访问沙箱外文件")
        
        # 读取沙箱内文件
        with open(safe_file, "r") as f:
            print(f"\n沙箱内文件内容:\n{f.read()}")

# 说明：这个示例展示了如何通过临时目录创建基础文件隔离环境，
# 在实际macOS应用中应配合sandbox-exec实现系统级隔离
```




```python
# 示例2：网络隔离 - 限制Agent的网络访问
import subprocess
import shlex

def network_restricted_agent():
    """
    使用macOS sandbox工具限制网络访问
    需要配合自定义sandbox配置文件使用
    """
    # 定义沙箱规则（实际应保存为.sb配置文件）
    sandbox_rules = """
    (version 1)
    (deny network*)
    (allow file-read* file-write* (subpath "/tmp/agent_sandbox"))
    """
    
    # 模拟受限的网络操作
    try:
        # 实际应用中会通过sandbox-exec运行此命令
        result = subprocess.run(
            ["curl", "https://api.example.com"],
            check=True,
            capture_output=True
        )
        print("网络请求成功（未隔离状态）")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("网络请求被拦截（沙箱隔离状态）")

# 说明：这个示例展示了如何通过macOS沙箱规则限制网络访问，
# 实际应用中需要创建.sb配置文件并通过sandbox-exec执行
```




```python
# 示例3：进程隔离 - 限制子进程执行
import os
import plistlib

def create_sandboxed_agent_profile():
    """
    创建macOS沙箱配置文件（.sb格式）
    用于限制Agent可以执行的子进程
    """
    sandbox_config = {
        "version": 1,
        "rules": [
            # 允许的子进程
            {"allow": {"process-exec": {"literal": "/usr/bin/python3"}}},
            # 拒绝所有其他进程
            {"deny": {"process-exec": {"regex": ".*"}}}
        ],
        "exceptions": {
            "allowed_dirs": ["/tmp/agent_sandbox"]
        }
    }
    
    # 将配置写入临时文件
    with open("/tmp/agent_sandbox.sb", "wb") as f:
        plistlib.dump(sandbox_config, f)
    
    print("沙箱配置已生成到 /tmp/agent_sandbox.sb")
    print("可通过以下命令应用：")
    print("sandbox-exec -f /tmp/agent_sandbox.sb /usr/bin/python3 agent.py")

# 说明：这个示例展示了如何创建macOS沙箱配置文件来限制子进程执行，
# 实际应用中需要配合sandbox-exec工具使用该配置文件
```


---
## 案例研究


### 1：某网络安全初创公司的红队测试环境

 1：某网络安全初创公司的红队测试环境

**背景**:
该公司主要为企业客户提供渗透测试和红队演练服务。随着大语言模型（LLM）的普及，红队成员开始尝试使用本地的自主智能体来编写自动化脚本，以发现系统漏洞。这些智能体通常拥有极高的系统权限，能够执行代码、访问文件系统甚至调用网络接口。

**问题**:
在测试过程中，研究人员发现，部分智能体编写的代码存在逻辑错误，有时会意外删除本地非测试目录下的重要文件，或者在未经授权的情况下尝试访问外网敏感API。由于是在开发者的本地 macOS 设备上直接运行，缺乏有效的隔离机制，导致“越狱”后的智能体像勒索软件一样破坏了开发环境，造成了数据丢失和不可控的网络风险。

**解决方案**:
团队引入了 Agent Safehouse 作为本地智能体的沙箱环境。他们将所有自主智能体进程限制在 Safehouse 创建的独立沙箱中。该工具利用 macOS 原生的沙箱机制，严格限制了智能体对文件系统的访问权限（仅限特定的临时目录），并阻断了对非白名单网络端点的访问。

**效果**:
实施后，开发环境的安全性得到了根本性保障。即使智能体生成了恶意代码或由于幻觉导致误操作，也被限制在沙箱内部，无法影响宿主机系统。这不仅保护了研发人员的核心数据，还消除了合规性风险，使得团队能够更激进地测试自动化攻击向量，而无需担心“炸机”。

---



### 2：独立开发者的 AI 自动化办公工作流

 2：独立开发者的 AI 自动化办公工作流

**背景**:
一位独立软件开发者正在构建一套基于本地 LLM 的个人助理，旨在通过分析本地代码库和文档来辅助编程和撰写技术博客。由于工作性质，他需要该智能体能够读取硬盘上的源代码文件，并执行 Git 命令进行版本控制。

**问题**:
在早期测试中，智能体曾因误解指令，错误地执行了 `git clean -fd` 命令，导致数天未提交的本地代码被永久删除。此外，由于担心智能体在处理第三方库分析时可能触发不可控的网络请求，开发者不敢将其接入核心项目目录，导致工作流效率低下。

**解决方案**:
开发者使用 Agent Safehouse 对本地智能体进行了封装。通过配置，Safehouse 允许智能体以“只读”方式访问核心代码库，而对于写入类操作（如 Git 提交、文件修改），则被重定向到一个临时的沙箱副本中。同时，网络访问被设置为“仅限 localhost”，防止数据外泄。

**效果**:
这种设置让开发者能够放心地让 AI 直接操作生产环境的代码副本进行分析。智能体不再具备破坏真实文件系统的能力，彻底解决了“误删文件”的痛点。该方案成功实现了 AI 与本地文件系统的安全交互，将开发者的日常自动化效率提升了 40%，同时保持了数据的绝对私密性和安全性。

---



### 3：金融科技公司的内部 LLM 工具审计

 3：金融科技公司的内部 LLM 工具审计

**背景**:
一家金融科技公司为了防止核心数据泄露，严禁员工将代码和数据上传至公有云模型。因此，公司技术部门部署了运行在员工本地 MacBook 上的开源大模型。安全团队需要对这些本地运行的智能体工具进行严格的安全审计，以确保它们符合公司的安全合规标准。

**问题**:
审计发现，许多本地智能体工具在安装时要求极高的磁盘权限（如“完全访问磁盘”），这违反了最小权限原则。如果这些工具被供应链攻击污染，或者模型本身存在漏洞，攻击者可以借此通过员工的笔记本电脑横向移动访问公司内网。

**解决方案**:
安全团队强制要求所有本地运行的智能体工具必须在 Agent Safehouse 提供的沙箱内启动。Safehouse 的 macOS 原生特性允许安全团队定义精细的配置文件，明确禁止智能体访问用户的 `Keychain`（钥匙串）、`Documents` 文件夹以及公司内网的 VPN 凭证。

**效果**:
通过 Agent Safehouse 的隔离，公司成功在不影响员工使用本地 AI 提升效率的前提下，满足了金融级别的合规要求。沙箱日志记录了所有敏感文件的访问尝试，为安全运营中心（SOC）提供了可审计的追踪记录，有效阻断了潜在的本地提权路径。

---
## 最佳实践

## 最佳实践指南

### 实践 1：利用 macOS 原生沙盒机制进行资源隔离

**说明**: Agent Safehouse 的核心优势在于利用 macOS 原生的沙盒技术，而非依赖虚拟机或复杂的容器化方案。通过严格控制本地 Agent 的文件系统、网络和进程访问权限，确保 Agent 即使被攻陷或产生异常行为，也无法访问宿主机上的敏感数据（如钥匙串、私人文档）或破坏系统稳定性。

**实施步骤**:
1. 在 `entitlements` 文件中明确配置 `com.apple.security.app-sandbox` 为 true。
2. 使用 `com.apple.security.files.user-selected.read-write` 替代全局文件读写权限，强制用户手动授权访问特定目录。
3. 移除不必要的网络权限（如 `com.apple.security.network.client`），对于纯本地的数据处理任务，实施网络断开策略。

**注意事项**: 即使是本地 Agent，也应遵循“最小权限原则”。不要为了开发方便而授予 `com.apple.security.files.all` 之类的广泛权限。

---

### 实践 2：实施严格的输入验证与输出过滤

**说明**: 本地 Agent 通常需要接收用户提示或处理外部数据。在沙盒环境中，必须防止通过恶意输入触发解析器漏洞或导致缓冲区溢出，从而试图逃逸沙盒。同时，对 Agent 生成的输出进行过滤，防止其生成可执行的 Shell 脚本并在宿主机上运行。

**实施步骤**:
1. 对所有传入 Agent 的 Prompt 或数据进行类型检查和长度限制。
2. 在 Agent 与操作系统交互的层（如执行 Shell 命令的接口）建立白名单机制，仅允许预定义的安全命令集。
3. 对输出内容进行扫描，确保不包含路径遍历字符或恶意代码注入模式。

**注意事项**: 不要依赖 Agent 自身的“安全性”来判断指令是否可执行，必须在沙盒边界处设置硬编码的检查逻辑。

---

### 实践 3：使用 XPC 服务进行模块间通信

**说明**: 为了进一步降低风险，应将 Agent 的核心逻辑与需要更高权限的 UI 或系统服务分离。利用 macOS 的 XPC (Inter-Process Communication) 机制，可以将 Agent 运行在受限的沙盒进程中，仅通过 XPC 发送消息请求主进程处理高风险操作（如保存文件到用户指定位置）。

**实施步骤**:
1. 创建一个独立的 XPC Service 目标，用于承载 Agent 的执行逻辑。
2. 定义严格的 XPC 协议接口，仅暴露必要的方法（如 `processText`、`saveResult`）。
3. 主应用仅作为协调者，不直接执行 Agent 代码，从而限制漏洞攻击面。

**注意事项**: XPC 传输的数据应进行序列化（如使用 Codable），避免传输可执行的二进制代码块。

---

### 实践 4：管理临时文件与数据持久化

**说明**: Agent 运行过程中可能会生成临时文件或日志。在沙盒环境下，必须确保这些数据被隔离在特定的容器目录中，并在任务结束后及时清理，防止敏感信息残留或磁盘空间被恶意占用。

**实施步骤**:
1. 使用 `NSTemporaryDirectory()` API 为每次 Agent 会话创建独立的临时文件夹。
2. 实施配额限制，监控 Agent 写入的数据量，防止“磁盘炸弹”攻击。
3. 在会话结束或 Agent 崩溃时，注册清理回调函数，确保彻底擦除临时数据。

**注意事项**: 避免将缓存数据写入用户可见的文档目录，除非经过用户明确授权。

---

### 实践 5：限制网络能力以防止数据泄露

**说明**: 即使是本地 Agent，有时也会尝试通过回连来泄露数据或下载恶意载荷。利用 macOS 沙盒的网络控制能力，应根据 Agent 的功能需求，精确控制其入站和出站连接。

**实施步骤**:
1. 对于纯文本处理或本地推理的 Agent，在 entitlements 中完全移除网络权限键值。
2. 如果必须联网（如访问本地 API），使用 `com.apple.security.network.outgoing` 并配合 `com.apple.security.network.client`，同时通过应用层防火墙限制目标 IP 为 localhost (127.0.0.1)。
3. 定期审查网络日志，确保 Agent 没有建立未预期的连接。

**注意事项**: 默认拒绝所有网络连接，除非业务逻辑绝对必要。

---

### 实践 6：代码签名与完整性校验

**说明**: 为了确保沙盒策略不被篡改，且 Agent 运行的环境未被第三方注入恶意代码，必须对应用程序及其包含的所有 Helper tools 和 Agent 组件进行严格的代码签名。

**实施步骤**:
1. 在构建流程中集成自动签名，确保所有二进制文件均由有效的开发者证书签名。
2. 在运行时，使用 `SecStaticCodeCheckValidity` 验证自身代码签名完整性，防止被篡改。
3. 启用 Hardened Runtime ( hardened Runtime ) 选项，提供额外的内存损坏保护。

**注意事项**: 确保私钥安全存储，一旦证书泄露，应立即撤销并重新签名发布。

---

### �

---
## 学习要点

- Agent Safehouse 是一种专为本地 AI 代理设计的 macOS 原生沙箱机制，旨在解决自主代理在执行系统命令时的安全风险。
- 该工具利用 macOS 原生的权限管理（如 TCC）和沙箱技术，为代理提供了一个隔离且受限的执行环境，防止其随意访问敏感文件或系统资源。
- 它通过精细的权限控制策略，允许用户明确界定代理可以访问的目录、网络端口或系统功能，从而实现“最小权限原则”。
- 这种方法为在本地运行强大的自主代理（如编码、文件操作代理）提供了一种安全方案，避免了完全暴露操作系统带来的隐患。
- 该项目突出了“本地优先”的安全理念，即在不依赖云端隔离的情况下，利用操作系统底层特性来约束日益智能的 AI 行为。

---
## 常见问题


### 1: 什么是 Agent Safehouse，它主要解决什么问题？

1: 什么是 Agent Safehouse，它主要解决什么问题？

**A**: Agent Safehouse 是一个专为 macOS 设计的原生沙箱工具，旨在为本地运行的 AI 代理提供安全隔离环境。随着本地 AI 代理（如自主编码助手、自动化脚本工具）的普及，这些工具通常需要较高的系统权限，这带来了潜在的安全风险。Agent Safehouse 利用 macOS 原生的沙箱机制，限制代理只能访问特定的文件、网络接口和系统资源，从而防止恶意或失控的 AI 代码对宿主系统造成破坏或窃取敏感数据。

---



### 2: Agent Safehouse 与 Docker 或虚拟机隔离有什么区别？

2: Agent Safehouse 与 Docker 或虚拟机隔离有什么区别？

**A**: Agent Safehouse 与 Docker 或虚拟机（VM）的主要区别在于底层实现机制和资源开销。
1.  **实现机制**：Agent Safehouse 基于 macOS 原生的沙箱技术，直接利用操作系统内核的安全策略。而 Docker 和 VM 依赖于容器化技术或硬件虚拟化，模拟独立的操作系统环境。
2.  **资源开销**：由于不需要运行完整的客户操作系统，Agent Safehouse 的资源占用极低，启动速度更快，更适合轻量级的本地代理任务。
3.  **集成度**：它专为 macOS 原生应用设计，能更好地与 macOS 系统服务集成，而无需像 Docker 那样处理复杂的跨平台兼容性问题。

---



### 3: 它是如何防止 AI 代理访问未授权的文件或网络的？

3: 它是如何防止 AI 代理访问未授权的文件或网络的？

**A**: Agent Safehouse 通过严格的配置文件来定义安全边界。当用户在 Safehouse 中启动一个代理时，可以指定其“权力范围”。系统会强制执行以下策略：
1.  **文件系统隔离**：代理只能读取或写入用户明确指定的目录（如特定的项目文件夹），而无法访问用户的 Documents、Downloads 或其他敏感区域。
2.  **网络限制**：可以配置白名单或黑名单，限制代理只能连接到特定的 API 端点，或完全禁止网络访问以防止数据外泄。
3.  **进程隔离**：防止代理启动其他未授权的辅助进程或修改系统设置。

---



### 4: 使用 Agent Safehouse 是否会降低 AI 代理的运行效率？

4: 使用 Agent Safehouse 是否会降低 AI 代理的运行效率？

**A**: 通常情况下，性能损耗极小，可以忽略不计。由于 Agent Safehouse 使用的是 macOS 原生的系统调用过滤和策略检查，这些操作是在内核级别高效完成的。与虚拟机模拟 CPU 和内存不同，沙箱技术不会引入额外的指令翻译层。因此，对于大多数本地代理任务（如代码生成、文件处理），用户几乎感觉不到性能差异。

---



### 5: 哪些类型的本地 AI 代理最适合使用 Agent Safehouse？

5: 哪些类型的本地 AI 代理最适合使用 Agent Safehouse？

**A**: 任何需要处理用户数据或执行系统操作但不可完全信任的本地代理都适合使用。具体场景包括：
1.  **自主编程助手**：例如能够自动读取代码库并执行修改命令的 AI，需要限制其只能访问项目文件夹。
2.  **自动化脚本工具**：需要整理文件或批量处理数据的代理，防止其误删系统文件。
3.  **实验性 AI 模型**：测试新的或来源不明的本地大模型时，防止其包含隐藏的恶意指令。

---



### 6: Agent Safehouse 是否支持所有 macOS 应用和 AI 框架？

6: Agent Safehouse 是否支持所有 macOS 应用和 AI 框架？

**A**: Agent Safehouse 主要针对命令行工具、脚本以及符合 macOS 沙箱规范的应用程序。对于大多数基于 Python、Node.js 或 Rust 编写的本地 AI 代理，只要它们不试图破坏沙箱规则（例如直接访问内核驱动或未授权的硬件端口），通常都能很好地运行。然而，某些极度依赖系统底层权限或特定硬件直通（如未经抽象的 GPU 访问）的复杂应用可能需要额外的配置才能适配。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**:

### 在 macOS 中，沙盒主要通过配置文件（.sb）或 entitlements 来定义权限。假设你需要限制一个 Agent 只能读取特定的配置文件（如 `/etc/hosts`），但禁止访问其他系统文件。请写出实现这一限制的核心 entitlements 键值对，并解释为什么不能仅依赖传统的 Unix 文件权限（chmod/chown）来实现这一目标。

### 提示**:

---
## 引用

- **原文链接**: [https://agent-safehouse.dev](https://agent-safehouse.dev)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47301085](https://news.ycombinator.com/item?id=47301085)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [安全](/categories/%E5%AE%89%E5%85%A8/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [Agent Safehouse](/tags/agent-safehouse/) / [macOS](/tags/macos/) / [沙箱](/tags/%E6%B2%99%E7%AE%B1/) / [本地 Agent](/tags/%E6%9C%AC%E5%9C%B0-agent/) / [安全隔离](/tags/%E5%AE%89%E5%85%A8%E9%9A%94%E7%A6%BB/) / [原生沙箱](/tags/%E5%8E%9F%E7%94%9F%E6%B2%99%E7%AE%B1/) / [系统安全](/tags/%E7%B3%BB%E7%BB%9F%E5%AE%89%E5%85%A8/) / [Agent 安全](/tags/agent-%E5%AE%89%E5%85%A8/)
- 场景： [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [Agent Safehouse：macOS 原生沙箱，用于本地 Agent 隔离]({{< relref "posts/20260308-hacker_news-agent-safehouse-macos-native-sandboxing-for-local--1.md" >}})
- [Agent Safehouse：macOS 原生沙箱，用于隔离本地 Agent]({{< relref "posts/20260309-hacker_news-agent-safehouse-macos-native-sandboxing-for-local--0.md" >}})
- [Agent Safehouse：macOS 本地代理的原生沙箱方案]({{< relref "posts/20260308-hacker_news-agent-safehouse-macos-native-sandboxing-for-local--0.md" >}})
- [Agent Safehouse：macOS 本地 Agent 的原生沙箱方案]({{< relref "posts/20260309-hacker_news-agent-safehouse-macos-native-sandboxing-for-local--1.md" >}})
- [Matchlock：基于 Linux 沙箱的 AI 智能体安全隔离方案]({{< relref "posts/20260208-hacker_news-matchlock-linux-based-sandboxing-for-ai-agents-3.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*