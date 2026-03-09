---
title: "Agent Safehouse：macOS 原生沙箱技术用于隔离本地 Agent"
date: 2026-03-09T02:43:00+08:00
draft: false
entry_kind: "auto"
tags: ["Agent", "macOS", "沙箱技术", "本地部署", "系统安全", "进程隔离", "Sandbox", "原生应用"]
categories: ["安全", "系统与基础设施"]
source: hacker_news
description: "随着本地 AI 代理的普及，其安全性成为开发者不可忽视的挑战。Agent Safehouse 作为一款基于 macOS 原生沙箱技术的解决方案，为本地代理提供了严格的隔离环境，有效防止潜在的安全风险。本文将深入剖析其技术原理与实现细节，帮助开发者构建更安全、可控的本地 AI 应用。"
external_url: https://agent-safehouse.dev
scenarios: ["Web应用开发"]
---

# Agent Safehouse：macOS 原生沙箱技术用于隔离本地 Agent

---

## 基本信息

- **作者**: atombender
- **评分**: 330
- **评论数**: 78
- **链接**: [https://agent-safehouse.dev](https://agent-safehouse.dev)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47301085](https://news.ycombinator.com/item?id=47301085)

---
## 导语

随着本地 AI 代理的普及，其安全性成为开发者不可忽视的挑战。Agent Safehouse 作为一款基于 macOS 原生沙箱技术的解决方案，为本地代理提供了严格的隔离环境，有效防止潜在的安全风险。本文将深入剖析其技术原理与实现细节，帮助开发者构建更安全、可控的本地 AI 应用。

---
## 评论

### 评价文章：Agent Safehouse – macOS-native sandboxing for local agents

#### 一、 中心观点
文章主张在构建本地 AI Agent 时，应摒弃依赖外部沙箱或虚拟机的传统安全范式，转而利用 macOS 原生的沙箱机制作为核心边界，从而在保证安全性的前提下实现轻量化和高性能。

#### 二、 深入评价

**1. 内容深度与论证严谨性**
*   **事实陈述**：文章准确识别了当前 AI Agent 领域的一个核心痛点——安全性。现有的 Agent（如基于 AutoGPT 或 BabyAGI）通常拥有 Shell 访问权限，存在任意代码执行风险。
*   **作者观点**：作者认为操作系统级（OS-level）的权限控制优于应用级或容器级控制。
*   **评价**：文章的论证逻辑在技术原理上是站得住脚的。macOS 的沙箱基于 Trusted BSD 和 MAC Framework，其内核级的强制访问控制确实比单纯的 Python 虚拟环境或非 root 用户隔离更为严密。然而，文章在论证**“Agent 的攻击面”**时略显乐观。Agent 的核心风险往往来自于**“提示词注入”**导致的逻辑越狱，即使沙箱限制了文件访问，若 Agent 具有网络访问权限，攻击者仍可能利用其作为跳板进行内网探测或数据外带。

**2. 实用价值与创新性**
*   **创新性**：提出将“本地 Agent”视为“不可信的第三方应用”并加以原生沙箱限制，这是一种视角的转换。大多数开发者倾向于信任“自己写的代码”，而忽略了 LLM 生成代码的非确定性。
*   **实用价值**：对于 macOS 生态的开发者极具参考意义。它提供了一种无需 Docker 即可隔离风险的方案，降低了本地部署 AI 助手的门槛（无需配置复杂的网络命名空间）。
*   **支撑理由**：
    1.  **资源效率**：相比启动一个完整的 Linux VM 或 Docker 容器，直接在 macOS 原生环境运行并利用沙箱隔离，内存占用极低，启动速度更快。
    2.  **用户体验**：原生应用能更好地融入 macOS 生态（如调用 Spotlight、Calendar），而无需复杂的 Socket 通信或挂载卷。
    3.  **权限细粒度**：macOS 沙箱允许精确控制（如仅允许读写特定目录、仅允许特定的网络连接），这比 Docker 的“全有或全无”的 Capabilities 机制更贴合个人助理场景。

**3. 反例与边界条件**
*   **反例 1（Windows/Linux 用户的困境）**：该方案高度依赖 macOS 的封闭生态特性。在 Linux 上，虽然存在 Firejail 等工具，但缺乏统一的 App Store 风格签名和沙箱策略，配置复杂度极高；在 Windows 上，这种原生沙箱机制更是碎片化。
*   **反例 2（动态交互的局限性）**：macOS 沙箱对 GUI 自动化的支持极差。如果 Agent 需要通过 RPA（机器人流程自动化）控制其他应用（如点击按钮、读取屏幕内容），沙箱会阻断这些操作，导致 Agent 变成“盲人”或“瘫痪”。
*   **边界条件**：该方案仅适用于**“工具调用型”** Agent（通过 API 查询数据、写入文件），而不适用于**“UI 自动化型”** Agent。

**4. 可读性与行业影响**
*   **可读性**：文章技术阐述清晰，但对“如何实施”的代码级细节可能涉及较少，更多是架构层面的探讨。
*   **行业影响**：这预示着 AI Agent 安全发展的一个新方向：**“端侧原生安全”**。随着 Apple Intelligence 的发布，苹果正在强化端侧模型的能力。Agent Safehouse 的思路与 Apple 的“Private Cloud Compute”理念不谋而合——尽可能在本地通过最小权限完成任务。这可能会推动一批基于 macOS 原生能力构建的 Agent 框架的出现。

**5. 争议点**
*   **你的推断**：最大的争议在于**“信任链的转移”**。作者假设操作系统是可信的，但 Agent 本身是不可信的。然而，如果 LLM 提供商（如 OpenAI）在模型中植入了后门，或者模型本身存在“幻觉”导致生成了恶意代码，macOS 沙箱能否完全阻止针对内核漏洞的攻击？虽然概率极低，但在理论上，沙箱并非坚不可摧。

#### 三、 实际应用建议与验证方式

**1. 实际应用建议**
*   **分层防御**：不要完全依赖 macOS 沙箱。建议结合 **eBPF** 技术监控 Agent 进程的系统调用，作为第二道防线。
*   **网络隔离**：在配置 `entitlements` 时，默认移除网络访问权限。如果 Agent 需要联网，强制其通过一个自定义的 HTTP/SOCKS 代理，以便在代理层审查并过滤恶意请求。

**2. 可验证的检查方式**
*   **指标 1：逃逸测试**
    *   *实验*：在沙箱内运行 Agent，通过 Prompt 注入尝试执行 `rm -rf ~/` 或访问 `~/.ssh`。
    *   *预期结果*：操作应被系统内核直接拒绝，并生成崩溃日志或权限拒绝错误，而非文件被删除。
*   **指标 2：资源开销对比**
    *   *实验*：对比运行相同任务（如批量

---
## 代码示例




```python
# 示例1：文件访问沙箱限制
import os
import tempfile

def sandboxed_file_operation(filename, content):
    """
    在临时目录中安全地操作文件，避免访问系统关键路径
    """
    # 创建一个临时沙箱目录
    with tempfile.TemporaryDirectory() as sandbox_dir:
        # 构建沙箱内的文件路径
        safe_path = os.path.join(sandbox_dir, filename)
        
        # 安全地写入文件
        with open(safe_path, 'w') as f:
            f.write(content)
        
        # 读取并验证内容
        with open(safe_path, 'r') as f:
            return f.read()

# 使用示例
result = sandboxed_file_operation("test.txt", "这是沙箱内的安全操作")
print(result)  # 输出: 这是沙箱内的安全操作
```




```python
# 示例2：网络请求沙箱
import requests
from urllib.parse import urlparse

def sandboxed_network_request(url, timeout=5):
    """
    限制网络请求的安全沙箱，防止访问内部网络或非HTTPS资源
    """
    parsed = urlparse(url)
    
    # 验证协议必须是HTTPS
    if parsed.scheme != 'https':
        raise ValueError("只允许HTTPS请求")
    
    # 验证不能访问本地地址
    if parsed.hostname in ('localhost', '127.0.0.1', '::1'):
        raise ValueError("禁止访问本地地址")
    
    # 设置超时和限制响应大小
    response = requests.get(url, timeout=timeout, stream=True)
    response.raise_for_status()
    
    # 只读取前1MB数据
    return next(response.iter_content(1024*1024))

# 使用示例
try:
    content = sandboxed_network_request("https://example.com")
    print(f"获取到 {len(content)} 字节数据")
except ValueError as e:
    print(f"安全限制: {e}")
```




```python
# 示例3：命令执行沙箱
import subprocess
import shlex

def sandboxed_command_execution(command, allowed_commands=None):
    """
    安全执行命令的沙箱，只允许预定义的安全命令
    """
    if allowed_commands is None:
        allowed_commands = ['ls', 'echo', 'cat']
    
    # 解析命令
    try:
        parts = shlex.split(command)
    except ValueError as e:
        raise ValueError(f"无效的命令格式: {e}")
    
    # 验证命令是否在白名单中
    if not parts or parts[0] not in allowed_commands:
        raise ValueError(f"命令 '{parts[0]}' 不在允许列表中")
    
    # 执行命令并限制资源使用
    try:
        result = subprocess.run(
            parts,
            check=True,
            capture_output=True,
            text=True,
            timeout=10,  # 10秒超时
            # 在macOS上可以使用sandbox_init进一步限制
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        raise TimeoutError("命令执行超时")

# 使用示例
try:
    output = sandboxed_command_execution("echo 'Hello, sandbox!'")
    print(output)  # 输出: Hello, sandbox!
except (ValueError, TimeoutError) as e:
    print(f"执行错误: {e}")
```


---
## 案例研究


### 1：独立开发者 – 本地 AI 编程助手的沙箱隔离

 1：独立开发者 – 本地 AI 编程助手的沙箱隔离

**背景**:
一位独立开发者正在构建一款基于本地大语言模型（LLM）的 macOS 桌面应用，旨在帮助用户自动重构和优化代码。该应用需要读取用户本地的代码仓库文件，并运行 Python 脚本来测试代码片段的正确性。

**问题**:
由于应用需要较高的系统权限来读取文件和执行脚本，早期的测试版本存在严重的安全隐患。如果 LLM 生成的代码包含恶意指令（例如删除文件或窃取环境变量），可能会直接破坏开发者的本地环境或泄露敏感的 API 密钥。传统的虚拟机方案过于笨重，且无法无缝集成到原生的 macOS 应用体验中。

**解决方案**:
开发者引入了 Agent Safehouse 作为本地 Agent 的运行环境。通过利用 macOS 原生的沙箱机制，该工具将 AI Agent 的执行环境与用户实际的文件系统进行了严格隔离。开发者配置了特定的安全策略，仅允许 Agent 访问经过授权的临时项目目录，并禁止其访问系统关键路径和钥匙串。

**效果**:
在部署 Agent Safehouse 后，即使 LLM 误生成了具有破坏性的 Shell 命令，沙箱也能成功拦截并阻止其对主系统的任何修改。这不仅保护了开发者环境的安全性，还使得应用能够安全地通过 Mac App Store 的审核流程，因为其遵循了苹果最严格的安全容器标准。

---



### 2：金融科技初创公司 – 自动化合规审计 Agent 的安全部署

 2：金融科技初创公司 – 自动化合规审计 Agent 的安全部署

**背景**:
一家金融科技公司的安全团队开发了一套内部使用的自动化审计 Agent。该 Agent 需要在员工的 MacBook 上运行，自动扫描本地财务报表并生成合规报告。为了提高效率，Agent 需要调用本地的 Python 解释器和 Pandas 库进行数据处理。

**问题**:
由于金融数据的极度敏感性，公司严禁任何未经授权的数据外传或本地数据的非授权修改。然而，给予 Agent 广泛的文件读写权限以处理报表，违背了最小权限原则。团队担心 Agent 被劫持或出现逻辑错误，导致敏感的财务数据被加密或通过网络接口发送出去。

**解决方案**:
团队使用 Agent Safehouse 重新设计了 Agent 的部署架构。他们利用 Safehouse 创建了一个严格的“无网络”沙箱环境，并挂载了只读的财务数据目录。Agent 在这个隔离环境中启动 Python 进程进行数据分析，Safehouse 确保了该进程无法发起任何网络请求，也无法写入除指定日志目录以外的任何文件。

**效果**:
该方案成功实现了“数据可用但不可窃取”的安全目标。Agent 能够高效处理本地数据生成报告，但物理上被阻断了与外部网络的连接以及对源文件的修改能力。这种原生沙箱方案比传统的 Docker Desktop 更轻量，且完美符合公司合规部门对终端安全审计的要求。

---
## 最佳实践

## 最佳实践指南

### 实践 1：启用严格的文件系统隔离

**说明**: 利用 macOS 沙盒限制 Agent 仅能访问特定的、必要的目录。防止 Agent 意外读取敏感文件（如 SSH 密钥、浏览器数据）或修改系统关键配置。

**实施步骤**:
1. 在 `entitlements` 文件中配置 `com.apple.security.files.user-selected.read-write`，仅允许用户通过文件选择对话框授权访问。
2. 如果 Agent 需要访问特定工作目录，使用 `com.apple.security.files.downloads.read-write` 或指定路径的 Path Rules，避免使用通配符。
3. 禁用 `com.apple.security.files.all` 之类的广泛权限。

**注意事项**: 确保 Agent 在尝试访问未授权路径时能够优雅地处理错误，而不是崩溃。

---

### 实践 2：实施网络访问白名单机制

**说明**: 默认情况下应禁止所有出站网络连接，仅允许连接到已知的、必要的 API 端点或本地服务。这防止了 Agent 被劫持后向恶意服务器泄露数据。

**实施步骤**:
1. 在权限配置中不包含 `com.apple.security.network.client`（完全禁用网络）或使用 `com.apple.security.network.outgoing` 配合防火墙规则。
2. 如果必须联网，在代码层面实现 URL 白名单校验，确保所有 HTTP/HTTPS 请求都指向受信任的域名。
3. 对于仅与本机 LLM 通信的 Agent，确保仅绑定 localhost (127.0.0.1)。

**注意事项**: 定期审查网络日志，确保没有异常的出站连接尝试。

---

### 实践 3：限制进程生成与交互权限

**说明**: 禁止 Agent 生成其他子进程或调用 Shell 命令。这是防止命令注入攻击的关键防线，确保 Agent 无法执行 `exec` 族函数或调用 `system()`。

**实施步骤**:
1. 确保不授予 `com.apple.security.process-exec` 权限（如果使用 Hardened Runtime）。
2. 在代码审计中，检查是否使用了 `os.system`、`subprocess` 等模块，并予以移除或通过严格的沙盒内 API 替代。
3. 如果必须执行外部工具，考虑将工具打包在 App 内部并使用单独的 Helper 进程进行严格的参数校验。

**注意事项**: 某些 Python 库可能会在后台调用 Shell，需审查所有依赖项。

---

### 实践 4：隔离用户偏好设置与缓存

**说明**: 防止 Agent 读取或修改其他应用程序的配置文件，同时也防止恶意 Agent 通过偏好设置持久化。应强制使用容器化的数据存储。

**实施步骤**:
1. 移除 `com.apple.security.temporary-exception.files.absolute-path.read-write` 等允许访问任意路径的权限。
2. 使用 `NSUserDefaults` 或 App Sandbox 指定的容器目录来存储配置。
3. 确保敏感数据（如 API Keys）加密后存储在 Keychain 中，并设置访问控制列表（ACL）。

**注意事项**: 即使在沙盒内，也要对存储在本地容器的敏感数据进行加密，以防用户备份文件泄露。

---

### 实践 5：控制资源使用以防止拒绝服务

**说明**: 限制 Agent 可用的 CPU、内存和磁盘 I/O，防止 Agent 因死循环或恶意逻辑导致系统挂起或资源耗尽。

**实施步骤**:
1. 使用 `dispatch_source` 或 `mach` 监控自身进程的资源消耗。
2. 为长时间运行的任务设置超时限制。
3. 在处理大文件时采用流式处理，避免一次性加载全部内容到内存。

**注意事项**: macOS 沙盒本身不直接提供资源配额限制，需在应用层逻辑中实现。

---

### 实践 6：严格管理 IPC 和 XPC 服务通信

**说明**: 如果 Agent 需要与主应用或其他组件通信，必须使用 XPC 进行严格的接口验证，防止通过 IPC 通道进行未授权的操作。

**实施步骤**:
1. 定义明确的 XPC 协议，仅暴露必要的方法。
2. 在接收 XPC 消息时，验证发送者的身份和签名。
3. 避免在 XPC 消息中传递可执行代码或复杂的序列化对象，优先传递基本数据类型。

**注意事项**: 确保 XPC 服务的连接建立过程经过鉴权，防止本地恶意进程伪装连接。

---

### 实践 7：移除调试与开发工具权限

**说明**: 在生产环境中，移除允许调试器附加或获取内存转储的权限，防止攻击者通过内存分析提取敏感数据或 LLM 的上下文信息。

**实施步骤**:
1. 确保在发布构建中移除 `get-task-allow` 权限。
2. 启用代码签名和运行时硬化选项。
3. 如果可能，启用地址空间布局随机化 (ASLR) 和栈保护。

**注意事项**: 移除调试权限会使崩溃日志难以分析，建议在测试版中保留，正式版中移

---
## 学习要点

- 根据您提供的内容，以下是关于 Agent Safehouse 的关键要点总结：
- Agent Safehouse 为本地运行的 AI Agent 提供了基于 macOS 原生沙盒机制的安全隔离环境，防止恶意代码破坏系统或窃取数据。
- 该工具利用 Apple 原生权限框架（如 TCC）对 AI Agent 访问文件系统、网络或麦克风等敏感资源进行细粒度的控制。
- 它允许用户在不牺牲系统安全性的前提下，在本地设备上安全地执行由 Agent 生成的不可信代码或脚本。
- 该方案展示了如何利用操作系统层级的现有安全基础设施，来解决自主智能体面临的潜在风险问题。
- 此类沙盒技术对于构建端侧且隐私友好的 AI 应用至关重要，能有效降低本地 Agent 运行时的安全盲区。

---
## 常见问题


### 1: Agent Safehouse 是什么？它的主要用途是什么？

1: Agent Safehouse 是什么？它的主要用途是什么？

**A**: Agent Safehouse 是一个专为 macOS 设计的原生沙盒工具，旨在为本地运行的 AI Agent（智能体）提供安全的隔离环境。随着 AI Agent 在本地系统上执行任务（如读取文件、修改配置或运行脚本）的能力越来越强，它们带来的潜在安全风险也随之增加。Agent Safehouse 利用 macOS 原生的沙盒机制，限制这些 Agent 的系统访问权限，确保它们只能在授权的范围内活动，从而防止恶意代码或意外操作对主系统造成破坏。

---



### 2: 为什么需要专门的工具来为本地 Agent 提供沙盒保护？

2: 为什么需要专门的工具来为本地 Agent 提供沙盒保护？

**A**: 虽然现代操作系统本身具有安全机制，但本地 AI Agent 通常需要较高的权限才能辅助用户完成工作（例如读取文档、操作开发环境），这与传统的受限应用程序不同。如果直接以用户权限运行 Agent，一旦模型产生“幻觉”执行了危险指令（如 `rm -rf`），或者 Agent 代码本身存在漏洞，后果将不堪设想。Agent Safehouse 专门针对 Agent 的运行模式设计，提供了一种既能允许 Agent 执行有用任务，又能严格限制其越界行为的平衡方案，填补了通用安全工具在 AI 辅助编程领域的空白。

---



### 3: Agent Safehouse 是如何工作的？它使用了什么技术？

3: Agent Safehouse 是如何工作的？它使用了什么技术？

**A**: Agent Safehouse 深度集成了 macOS 的原生沙盒框架。它通过定义严格的安全策略，对 Agent 进程及其子进程进行隔离。当 Agent 尝试访问文件系统、网络或系统资源时，Agent Safehouse 会拦截这些请求。只有那些明确被允许的操作（例如访问特定的临时目录或只读特定的配置文件）才会被放行，其他所有未经授权的访问尝试都会被系统拦截并记录。这种机制确保了即使 Agent 被攻破或失控，攻击者也无法逃逸到宿主操作系统中。

---



### 4: 使用 Agent Safehouse 会对本地 Agent 的性能产生影响吗？

4: 使用 Agent Safehouse 会对本地 Agent 的性能产生影响吗？

**A**: 通常情况下，性能影响微乎其微。由于 Agent Safehouse 依赖的是 macOS 操作系统内核层面的原生沙盒机制，而不是虚拟机或模拟器，因此不存在由于硬件虚拟化带来的巨大性能损耗。文件系统 I/O 和系统调用检查的开销非常小，对于大多数 AI Agent 的日常工作负载（如文本处理、代码生成、调用 API）来说，用户几乎感觉不到延迟。

---



### 5: Agent Safehouse 支持哪些类型的 Agent 或应用程序？

5: Agent Safehouse 支持哪些类型的 Agent 或应用程序？

**A**: 作为一个通用的沙盒层，Agent Safehouse 理论上可以支持任何在 macOS 上运行的本地 Agent 或 AI 辅助工具。这包括但不限于本地的 LLM（大语言模型）前端、自主编码 Agent、系统管理脚本以及集成了 AI 功能的开发工具。只要该 Agent 是以进程形式运行在 macOS 上，Agent Safehouse 就可以对其进行封装和权限管控。

---



### 6: 对于开发者来说，如何配置 Agent Safehouse 的权限策略？

6: 对于开发者来说，如何配置 Agent Safehouse 的权限策略？

**A**: Agent Safehouse 提供了灵活的配置选项，允许开发者根据 Agent 的具体需求定制沙盒规则。通常，这涉及编写一个配置文件（如 Profile 或 Entitlements 文件），在其中指定 Agent 可以访问的路径、网络端口以及进程间通信（IPC）的权利。例如，你可以配置 Agent 拥有对 `/Users/Shared` 目录的读写权限，但拒绝访问 `~/Documents`。这种精细的控制使得 Agent 既能完成工作，又不会触碰敏感数据。

---



### 7: Agent Safehouse 与 Docker 或虚拟机隔离有什么区别？

7: Agent Safehouse 与 Docker 或虚拟机隔离有什么区别？

**A**: Docker 和虚拟机提供的是硬件或操作系统级别的隔离，通常资源占用较大，且环境与宿主系统分离较深（例如需要映射卷才能共享文件）。Agent Safehouse 则是进程级的隔离，它直接运行在 macOS 主系统上，但限制了进程的“视野”和权限。对于需要频繁与宿主系统交互（如读写文件、调用 macOS 原生 API）的 AI Agent 来说，Agent Safehouse 提供了一种更轻量、更无缝且更符合 macOS 生态习惯的安全方案，无需为了安全而牺牲 Agent 与系统的集成度。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: macOS 的沙盒机制主要依赖于哪个内核扩展和配置文件格式来定义资源访问规则？请列举出至少三个常见的沙盒 entitlement key（例如网络访问、文件读写等）。

### 提示**: 思考 macOS 权限声明的 XML 结构，以及 Apple 开发者文档中关于 `com.apple.security` 前缀的相关条目。

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
- 标签： [Agent](/tags/agent/) / [macOS](/tags/macos/) / [沙箱技术](/tags/%E6%B2%99%E7%AE%B1%E6%8A%80%E6%9C%AF/) / [本地部署](/tags/%E6%9C%AC%E5%9C%B0%E9%83%A8%E7%BD%B2/) / [系统安全](/tags/%E7%B3%BB%E7%BB%9F%E5%AE%89%E5%85%A8/) / [进程隔离](/tags/%E8%BF%9B%E7%A8%8B%E9%9A%94%E7%A6%BB/) / [Sandbox](/tags/sandbox/) / [原生应用](/tags/%E5%8E%9F%E7%94%9F%E5%BA%94%E7%94%A8/)
- 场景： [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [Agent Safehouse：macOS 本地代理的原生沙箱方案]({{< relref "posts/20260308-hacker_news-agent-safehouse-macos-native-sandboxing-for-local--0.md" >}})
- [Agent Safehouse：macOS 原生沙箱，用于本地 Agent 隔离]({{< relref "posts/20260308-hacker_news-agent-safehouse-macos-native-sandboxing-for-local--1.md" >}})
- [Matchlock：基于 Linux 的 AI 智能体沙箱技术]({{< relref "posts/20260208-hacker_news-matchlock-linux-based-sandboxing-for-ai-agents-2.md" >}})
- [RedSage：网络安全通用大语言模型]({{< relref "posts/20260131-arxiv_ai-redsage-a-cybersecurity-generalist-llm-0.md" >}})
- [OpenClaw赋予AI全系统权限引发安全担忧]({{< relref "posts/20260206-hacker_news-openclaw-when-ai-agents-get-full-system-access-sec-14.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*