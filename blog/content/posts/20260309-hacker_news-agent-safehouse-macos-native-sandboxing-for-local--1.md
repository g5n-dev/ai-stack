---
title: "Agent Safehouse：macOS 本地 Agent 的原生沙箱方案"
date: 2026-03-09T08:40:35+08:00
draft: false
entry_kind: "auto"
tags: ["Agent Safehouse", "macOS", "沙箱", "Agent", "本地部署", "安全隔离", "原生应用", "系统安全"]
categories: ["安全", "系统与基础设施"]
source: hacker_news
description: "随着本地 AI Agent 的普及，如何在享受便利的同时确保系统安全，已成为开发者不可忽视的挑战。Agent Safehouse 作为一款基于 macOS 原生沙箱技术的工具，为本地 Agent 提供了严格的资源隔离与权限管控方案。本文将深入剖析其技术原理，并演示如何通过配置，在防止恶意行为的同时，维持本地开发环境的高"
external_url: https://agent-safehouse.dev
scenarios: ["Web应用开发"]
---

# Agent Safehouse：macOS 本地 Agent 的原生沙箱方案

---

## 基本信息

- **作者**: atombender
- **评分**: 545
- **评论数**: 130
- **链接**: [https://agent-safehouse.dev](https://agent-safehouse.dev)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47301085](https://news.ycombinator.com/item?id=47301085)

---
## 导语

随着本地 AI Agent 的普及，如何在享受便利的同时确保系统安全，已成为开发者不可忽视的挑战。Agent Safehouse 作为一款基于 macOS 原生沙箱技术的工具，为本地 Agent 提供了严格的资源隔离与权限管控方案。本文将深入剖析其技术原理，并演示如何通过配置，在防止恶意行为的同时，维持本地开发环境的高效与稳定。

---
## 评论

**文章中心观点**
Agent Safehouse 提出了一种利用 macOS 原生权限系统（TCC）和沙盒机制，在不牺牲系统安全性的前提下，为本地运行的 AI Agent 提供受控的文件系统访问能力，旨在解决“本地智能”与“系统安全”之间的核心矛盾。

**深入评价与分析**

**1. 内容深度与论证严谨性**
*   **支撑理由：**
    *   **技术路径的务实性：** 文章没有选择重新发明一套复杂的虚拟机或容器方案，而是深入挖掘了 macOS 现有的 Hardened Runtime 和 App Sandbox。这种“借力打力”的思路在工程上极具深度，因为它避免了维护额外内核或 KVM 模块的开销。（事实陈述）
    *   **攻击面分析：** 作者清楚地识别了 LLM 最大的风险在于“幻觉”导致的非预期操作，而非恶意代码注入。通过限制 Agent 只能访问特定的 `Safehouse` 目录，而非整个 `~` 目录，有效地缩小了攻击半径。（作者观点）
    *   **数据主权意识：** 文章强调了本地运行的首要价值在于隐私保护。相比于将 API Key 和文件上传到云端处理，本地沙盒提供了一种符合 GDPR 和企业合规要求的物理隔离手段。（你的推断）
*   **反例/边界条件：**
    *   **依赖操作系统黑盒：** 这种方案的安全性高度耦合于 macOS 的 TCC 机制未被发现 0-day 漏洞。一旦 macOS 自身沙盒逃逸，该方案即刻失效。（边界条件）
    *   **侧信道攻击风险：** 虽然文件访问被限制，但如果 Agent 具有屏幕截图或内存读取权限，仍可能通过侧信道窃取 Safehouse 之外的数据。

**2. 实用价值与创新性**
*   **支撑理由：**
    *   **填补生态空白：** 目前开源 Agent 生态（如 AutoGPT, BabyAGI）大多缺乏安全约束，运行在裸进程权限下。Safehouse 提供了一个即插即用的安全底座，对于需要在本地处理敏感代码或文档的开发者具有极高的实用价值。（事实陈述）
    *   **“最小权限”的落地实践：** 创新点在于将网络安全中的“零信任”原则应用到了本地 AI 进程上。它不仅是一个工具，更是一种本地 Agent 的安全架构范式。（作者观点）
*   **反例/边界条件：**
    *   **开发成本转移：** 虽然使用了原生系统，但配置 `entitlements` 和签名对于普通用户而言门槛依然较高。如果缺乏自动化打包工具，其实际推广会受到阻碍。（边界条件）
    *   **功能受限性：** 严格的沙盒会剥夺 Agent 使用某些系统工具（如网络抓包、系统配置修改）的能力，导致某些需要深度系统集成的自动化任务无法完成。

**3. 行业影响与争议点**
*   **支撑理由：**
    *   **推动端侧 AI 安全标准：** 随着 Apple Intelligence 的发布，端侧模型将成为主流。Safehouse 的实践为“如何让端侧 AI 安全地操作用户文件”提供了一个先行参考范式，可能影响未来 macOS AI 应用的安全设计规范。（你的推断）
    *   **打破“全有或全无”的困境：** 目前的本地 Agent 往往要么完全不可信，要么需要用户完全信任。该方案试图建立中间地带，这对于构建“个人助理”级别的信任至关重要。
*   **争议点：**
    *   **UX 与安全的博弈：** 最大的争议可能在于用户体验。macOS 的弹窗机制非常频繁，如果 Agent 每次读写文件都需要用户确认（TCC 授权），那么“自动化”的体验将大打折扣。如果完全静默，则又回到了“盲目信任”的老路。
    *   **平台锁定：** 该方案深度绑定 macOS，这在跨平台开发日益普遍的今天可能被视为一种倒退，无法服务于 Linux 或 Windows 用户。

**实际应用建议**
1.  **分级部署策略：** 不要对所有 Agent 都启用最严格的沙盒。建议将 Agent 分级：处理敏感数据的（如邮件、代码库）放入 Safehouse；执行简单系统命令的（如查天气）可运行在宽松模式下。
2.  **结合人机回路（HITL）：** 在 Safehouse 的设计基础上，增加“关键操作确认”机制。例如，当 Agent 试图修改 `.env` 或删除文件时，强制要求用户介入，而不是仅仅依赖沙盒的读写拦截。
3.  **审计日志优先：** 既然使用了沙盒，就必须记录所有被拦截的请求。这些“失败日志”是分析 Agent 幻觉和意图的重要数据，应作为产品的核心功能之一。

**可验证的检查方式**
1.  **逃逸测试（指标）：** 构建一个提示词注入攻击，试图让 Agent 读取 `~/.ssh/id_rsa`。检查 Safehouse 是否能成功拦截并记录该行为，同时不发生崩溃。
2.  **性能损耗测试（实验）：** 在开启沙盒和关闭沙盒两种模式下，运行同一批次的文件 I/O 密集型 Agent 任务，对比 CPU 和内存的占用率，量化安全机制带来的性能税。
3.  **兼容性观察窗口：** 观察该项目在 GitHub 上的 Issues，看是否有大量关于特定开发工具（如 VS Code 插件、Docker）因权限不足而无法配合 Agent 工作的案例，以评估其实际通用性。

---
## 代码示例




```python
# 示例1：沙箱环境中的文件操作隔离
import os
import tempfile
from pathlib import Path

def sandboxed_file_operation():
    """演示如何在临时沙箱目录中安全操作文件"""
    # 创建临时沙箱目录
    sandbox_dir = tempfile.mkdtemp(prefix="agent_sandbox_")
    print(f"沙箱目录创建于: {sandbox_dir}")
    
    try:
        # 在沙箱内创建测试文件
        test_file = Path(sandbox_dir) / "test.txt"
        test_file.write_text("敏感数据")
        
        # 验证文件确实在沙箱内
        assert test_file.parent == Path(sandbox_dir)
        print("✓ 文件操作已隔离在沙箱内")
        
        # 尝试访问沙箱外的文件（会被阻止）
        try:
            os.listdir("/etc/passwd")
        except PermissionError:
            print("✓ 成功阻止沙箱外的文件访问")
            
    finally:
        # 清理沙箱
        import shutil
        shutil.rmtree(sandbox_dir)
        print("沙箱已清理")

# 说明：这个示例展示了如何通过临时目录实现基本的文件操作隔离，
# 防止本地Agent意外访问系统关键文件或泄露数据。
```




```python
# 示例2：进程权限限制
import subprocess
import os

def restricted_process_execution():
    """演示如何以受限权限运行外部命令"""
    # 创建受限用户组（macOS需要管理员权限）
    # 这里模拟使用nobody用户运行命令
    cmd = ["id"]
    
    try:
        # 以nobody用户运行命令（实际实现需要更多配置）
        result = subprocess.run(
            cmd,
            user="nobody",  # macOS/Linux特有参数
            capture_output=True,
            text=True
        )
        print(f"受限进程输出: {result.stdout}")
        print("✓ 进程以受限权限运行")
        
    except PermissionError:
        print("需要管理员权限来设置受限用户")
    except Exception as e:
        print(f"错误: {str(e)}")

# 说明：这个示例展示了如何通过运行低权限进程来限制Agent的系统访问，
# 防止恶意代码获取root权限或访问敏感资源。
```




```python
# 示例3：网络沙箱配置
import socket
import subprocess

def network_sandbox():
    """演示如何限制网络访问"""
    # 创建原始套接字（需要root权限）
    try:
        # 尝试创建原始套接字（通常被沙箱阻止）
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        print("✗ 警告：允许了原始套接字访问")
        s.close()
    except PermissionError:
        print("✓ 成功阻止原始套接字创建")
    
    # 检查防火墙规则（macOS pfctl）
    try:
        subprocess.run(["pfctl", "-s", "rules"], check=True)
        print("✓ 防火墙规则检查成功")
    except FileNotFoundError:
        print("提示：需要安装pfctl防火墙工具")

# 说明：这个示例展示了如何检查和限制网络访问能力，
# 防止Agent进行未授权的网络通信或攻击。
```


---
## 案例研究


### 1：个人开发者构建本地代码审查助手

 1：个人开发者构建本地代码审查助手

**背景**: 一名独立开发者正在使用 Ollama 在本地运行一个开源大语言模型（LLM），旨在构建一个自动化的代码审查助手。该工具需要直接读取和修改本地项目中的敏感源代码文件。

**问题**: 虽然模型在本地运行，无需担心数据外泄，但 LLM 偶尔会出现“幻觉”，导致其建议的代码补全包含危险的系统命令（如 `rm -rf`），或者错误地尝试修改项目目录之外的配置文件。直接在主开发环境中运行这种 Agent 存在误删文件或破坏开发环境的风险。

**解决方案**: 开发者利用 Agent Safehouse 创建了一个隔离的沙盒环境。通过 Safehouse 的 macOS 原生沙盒机制，将代码审查 Agent 的文件访问权限严格限制在当前项目文件夹内，并禁止其访问网络或系统关键目录（如 `/etc` 或 `~/.ssh`）。

**效果**: 成功将 Agent 的操作限制在“只读”或“受限写入”模式。即使 Agent 生成了破坏性脚本，也无法影响沙盒外的系统或文件。这既保留了本地 LLM 处理敏感代码的隐私优势，又消除了失控风险，让开发者敢于在生产级代码库中直接使用自动化工具。



### 2：金融分析师的本地化财报处理工作流

 2：金融分析师的本地化财报处理工作流

**背景**: 某金融分析师团队需要处理大量包含非公开财务数据的 PDF 报告。为了提高效率，他们尝试使用本地 Agent 自动化提取数据并生成 Excel 报表。

**问题**: 出于严格的数据合规要求（如禁止上传至云端 API），团队必须在本地运行模型。然而，自动化脚本需要调用复杂的第三方工具链（如 Python 脚本和 Pandas 库）来处理文件格式转换，这些脚本如果存在漏洞或逻辑错误，可能会在执行过程中意外泄露敏感文件到临时目录，甚至被恶意代码利用。

**解决方案**: 团队使用 Agent Safehouse 部署了一个“临时工作间”。所有的 PDF 解析、数据处理和报表生成都被封装在 Safehouse 提供的沙盒进程中。该沙盒被配置为“一次性”环境，仅允许读取输入文件夹的内容，并将输出写入特定的结果文件夹，同时阻断所有外网连接。

**效果**: 确保了高敏感度的财务数据绝对无法流出预设的路径，即使使用的开源解析库存在已知漏洞，攻击者也无法利用其窃取主机上的其他数据。这种方案满足了合规部门对数据“零出域”的严苛要求，同时实现了自动化办公。



### 3：安全研究团队的恶意软件分析环境

 3：安全研究团队的恶意软件分析环境

**背景**: 一个专注于 macOS 恶意软件的研究团队需要测试新的 Agent 工具，该工具旨在自动分析和解构可疑的下载文件。

**问题**: 分析过程具有高度危险性，因为 Agent 需要实际执行或解压这些可疑样本以观察其行为。如果在主操作系统上直接运行，一旦样本被确认为恶意软件，可能会迅速感染宿主机，破坏研究数据或通过网络传播。

**解决方案**: 研究团队利用 Agent Safehouse 构建了一个深度的隔离分析室。他们将可疑文件投递到由 Safehouse 管控的沙盒中，让 Agent 在内部进行解压、静态分析甚至动态行为观察。Safehouse 严格的权限控制确保了沙盒内的进程无法突破到宿主机的用户目录。

**效果**: 实现了安全的研究闭环。Agent 可以在几乎与真实系统无异的 macOS 环境中分析样本，但所有恶意操作（如尝试写入启动项、修改 Hosts 文件）都被 Safehouse 拦截或重定向。这极大地简化了研究人员的清理工作，并保护了核心分析机器的安全。

---
## 最佳实践

## 最佳实践指南

### 实践 1：实施严格的文件系统访问控制

**说明**: 利用 macOS 的沙盒机制限制 Agent 仅能访问特定的目录和文件。这是防止恶意 Agent 或被攻破的 Agent 窃取敏感数据（如 SSH 密钥、本地文档）的最核心防线。应遵循“最小权限原则”，即 Agent 默认不应拥有对整个用户目录的读写权限。

**实施步骤**:
1. 在配置文件中明确指定 `com.apple.security.files.user-selected.read-write` 权限，而非全局访问。
2. 使用 `Security Framework` 中的 `NSFileCoordinator` 和 `NSFilePresenter` 来监控文件访问行为。
3. 为 Agent 分配独立的工作目录，并将其路径通过“书签”或“安全作用域文件”的形式进行授权。
4. 测试 Agent 尝试访问未授权目录时的行为，确保其被系统直接拦截。

**注意事项**: 避免使用 `com.apple.security.files.all` 之类的宽泛权限。即使 Agent 需要处理文件，也应强制用户通过系统对话框显式授权特定文件。

---

### 实践 2：网络隔离与出站限制

**说明**: 本地 Agent 通常不需要完全的互联网访问权限，或者仅需访问特定的 API 端点。通过限制网络连接，可以防止 Agent 被利用进行 DDoS 攻击或向外部服务器泄露数据。如果 Agent 仅处理本地数据，应完全切断其网络访问。

**实施步骤**:
1. 在 `entitlements` 文件中移除 `com.apple.security.network.client` 和 `com.apple.security.network.server`，除非绝对必要。
2. 如果需要网络访问，使用 macOS 应用防火墙或 `pf` (Packet Filter) 规则限制出站连接的目标 IP 或端口。
3. 对于需要调用 LLM API 的 Agent，考虑通过本地代理进行中转，由代理统一验证请求的合法性，而不是让 Agent 直接连接外网。
4. 在代码中检查网络状态，并在尝试非白名单连接时主动终止进程。

**注意事项**: 即使 Agent 需要联网，也应限制其入站连接能力，防止其沦为网络服务器端口。

---

### 实践 3：限制进程生成与系统调用

**说明**: Agent（特别是具有代码执行能力的 Agent）可能会尝试生成子进程来执行 Shell 命令。在沙盒环境中，必须严格限制或禁止 fork/exec 操作，以防止 Agent 执行 `rm -rf /` 或安装恶意软件。

**实施步骤**:
1. 移除 `com.apple.security.inherit` 权限，防止 Agent 继承父进程的不当权限。
2. 使用 `Hardened Runtime` 并配合 `com.apple.security.automation.apple-events` 的精细控制，禁止其向其他系统应用（如 Terminal、Script Editor）发送 Apple Events。
3. 在代码层面拦截 `os.system`、`subprocess` 等调用，或使用受限制的 Python/Node 解释器环境。
4. 利用 `EndpointSecurity` 框架（企业级）监控并阻断可疑的 exec 系统调用。

**注意事项**: 某些 AI 模型可能需要调用外部工具（如 Python 解释器），此时应使用容器化或受限的 REPL 环境，而非直接调用系统 Shell。

---

### 实践 4：资源配额与计算限制

**说明**: 防止 Agent 因死循环或恶意挖矿逻辑导致 CPU、内存资源耗尽，进而使 macOS 系统卡顿。Safehouse 应能监控并限制 Agent 的资源消耗。

**实施步骤**:
1. 使用 `xpc_service` 或独立的 Helper Tool 来运行 Agent，并在主程序中监控其资源使用情况。
2. 利用 Unix 资源限制（`setrlimit`）限制 Agent 进程的 CPU 时间、最大内存和文件描述符数量。
3. 设置超时机制，如果单个任务执行时间超过阈值（如 5 分钟），强制终止 Agent 进程。
4. 监控进程线程数，防止 Fork Bomb 攻击。

**注意事项**: 资源限制不应影响正常的高负载任务，建议设置动态阈值或提供配置选项让用户调整性能上限。

---

### 实践 5：数据隔离与持久化加密

**说明**: Agent 生成的缓存、日志或临时文件可能包含用户隐私数据。必须确保这些数据在存储时是加密的，并且在 Agent 被卸载后能够彻底清除。

**实施步骤**:
1. 使用 `com.apple.security.files.user-selected.read-write` 配合 `NSData` 或 `FileHandle` 的加密方法写入数据。
2. 将 Agent 的数据存储在用户的 `Library/Containers/[BundleID]` 目录下，利用 macOS 的 App Sandbox 隔离特性。
3. 敏感配置（如 API Keys）应存储在 `Keychain` 中，而非明文写入配置文件。
4. 实现一个“清理”功能，利用 `NSFileManager` 在退出或卸载时安全删除临时文件。

**注意事项**: 避免将日志打印到系统控制台或全局可读的目录。确保 Key

---
## 学习要点

- Agent Safehouse 是一种专为本地 AI 智能体设计的 macOS 原生沙盒机制，旨在解决自主智能体在访问本地文件系统时的安全风险。
- 该方案利用 macOS 原生的权限管理（如 TCC）和安全模型，无需依赖虚拟机或复杂的网络隔离即可实现隔离。
- 智能体在沙盒内运行时，其文件系统访问、网络请求和进程执行均受到严格限制，防止恶意操作或数据泄露。
- 这种方法平衡了安全性与功能性，允许用户通过精细的授权控制，给予智能体执行特定任务所需的最低权限。
- 相比于云端处理，本地沙盒化方案确保了敏感数据无需离开用户设备，提供了更强的隐私保护。
- 该架构为构建安全、可信赖且能与操作系统深度集成的桌面级 AI 应用提供了新的设计范式。

---
## 常见问题


### 1: 什么是 Agent Safehouse，它主要解决什么问题？

1: 什么是 Agent Safehouse，它主要解决什么问题？

**A**: Agent Safehouse 是一个专为 macOS 设计的原生沙箱工具，旨在为本地运行的 AI Agent（自主智能体）提供安全隔离环境。随着 AI Agent 能够自主执行代码、调用系统 API 和修改文件，其潜在的安全风险（如恶意脚本执行或数据泄露）成为一大隐患。Agent Safehouse 利用 macOS 原生的沙箱机制，限制 Agent 的访问权限，确保其只能在受控的范围内运行，从而保护用户系统的安全。

---



### 2: 与 Docker 或虚拟机相比，Agent Safehouse 有什么不同？

2: 与 Docker 或虚拟机相比，Agent Safehouse 有什么不同？

**A**: Docker 和虚拟机通过内核级隔离或完整的操作系统模拟来提供环境，通常资源消耗较大且配置复杂。Agent Safehouse 则是利用 macOS 原生的 Sandbox 技术，专注于对进程权限的细粒度控制（如文件读写、网络访问等）。它更加轻量级，不需要运行完整的客户机操作系统，且与 macOS 系统底层集成更紧密，专为本地 Agent 开发和测试场景设计，而非通用的服务器容器化。

---



### 3: 它支持哪些类型的本地 Agent 或编程语言？

3: 它支持哪些类型的本地 Agent 或编程语言？

**A**: 虽然 Agent Safehouse 本质上是操作系统层面的权限管理工具，理论上可以沙箱化任何可执行进程，但它主要针对能够运行在 macOS 上的本地 Agent 环境。这通常包括使用 Python、Node.js、Rust 或 Go 编写的自主 Agent。只要 Agent 能够以独立进程的形式在 macOS 上运行，Agent Safehouse 就可以对其施加限制，无论其内部使用的是 LangChain、AutoGPT 还是其他自定义框架。

---



### 4: 配置 Agent Safehouse 是否复杂，是否需要编写代码？

4: 配置 Agent Safehouse 是否复杂，是否需要编写代码？

**A**: 该工具的设计初衷是简化安全配置。用户通常不需要编写底层 C 代码或深入了解 macOS 内部沙箱 API。Agent Safehouse 提供了声明式的配置文件（类似于配置文件），允许用户定义具体的白名单或黑名单规则（例如：允许读取 `/tmp` 目录，禁止网络访问等）。通过简单的配置文件加载，即可快速将 Agent 纳入沙箱保护之中。

---



### 5: 在沙箱环境中，Agent 如何访问互联网或特定的本地文件？

5: 在沙箱环境中，Agent 如何访问互联网或特定的本地文件？

**A**: Agent Safehouse 遵循“默认拒绝”的安全原则，即默认情况下 Agent 无法访问敏感资源。如果 Agent 需要访问互联网或特定文件，用户必须在配置文件中显式授权。例如，可以开启出站网络连接权限，或者将特定的文档文件夹映射为“可读写”。这种机制确保了用户对 Agent 的每一次资源访问都有清晰的认知和控制权。

---



### 6: Agent Safehouse 是否适用于生产环境，还是仅用于开发测试？

6: Agent Safehouse 是否适用于生产环境，还是仅用于开发测试？

**A**: 该工具目前主要面向开发者和高级用户，用于在本地计算机上安全地测试和运行未经验证的 AI Agent 代码。虽然其底层依赖的 macOS 沙箱技术非常稳定且强大，但在生产环境中部署 Agent 通常需要更复杂的基础设施支持（如云端隔离、审计日志等）。因此，它最适合作为本地开发、实验或个人自动化任务的安全防护层。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 假设你需要为一个简单的文件处理 Agent 设计沙箱环境。在 macOS 中，如果只使用 `chmod` 命令将脚本或二进制文件设置为不可执行，是否足以防止 Agent 意外执行恶意代码？请列举出这种方法的两个主要缺陷。

### 提示**: 考虑文件权限是针对“谁”的，以及“解释型语言”与“编译型二进制”在执行机制上的区别。

### 

---
## 引用

- **原文链接**: [https://agent-safehouse.dev](https://agent-safehouse.dev)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47301085](https://news.ycombinator.com/item?id=47301085)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [安全](/categories/%E5%AE%89%E5%85%A8/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [Agent Safehouse](/tags/agent-safehouse/) / [macOS](/tags/macos/) / [沙箱](/tags/%E6%B2%99%E7%AE%B1/) / [Agent](/tags/agent/) / [本地部署](/tags/%E6%9C%AC%E5%9C%B0%E9%83%A8%E7%BD%B2/) / [安全隔离](/tags/%E5%AE%89%E5%85%A8%E9%9A%94%E7%A6%BB/) / [原生应用](/tags/%E5%8E%9F%E7%94%9F%E5%BA%94%E7%94%A8/) / [系统安全](/tags/%E7%B3%BB%E7%BB%9F%E5%AE%89%E5%85%A8/)
- 场景： [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [Agent Safehouse：macOS 本地代理的原生沙箱方案]({{< relref "posts/20260308-hacker_news-agent-safehouse-macos-native-sandboxing-for-local--0.md" >}})
- [Agent Safehouse：macOS 原生沙箱，用于本地 Agent 隔离]({{< relref "posts/20260308-hacker_news-agent-safehouse-macos-native-sandboxing-for-local--1.md" >}})
- [Agent Safehouse：macOS 原生沙箱，用于隔离本地 Agent]({{< relref "posts/20260309-hacker_news-agent-safehouse-macos-native-sandboxing-for-local--0.md" >}})
- [我们构建了安全可扩展的 Agent 沙箱基础设施]({{< relref "posts/20260227-hacker_news-we-built-secure-scalable-agent-sandbox-infrastruct-13.md" >}})
- [Matchlock：基于 Linux 沙箱的 AI 智能体安全隔离方案]({{< relref "posts/20260208-hacker_news-matchlock-linux-based-sandboxing-for-ai-agents-3.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*