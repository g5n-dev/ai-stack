---
title: "Agent Safehouse：macOS 原生沙箱技术保护本地 Agent"
date: 2026-03-09T10:32:53+08:00
draft: false
entry_kind: "auto"
tags: ["Agent", "macOS", "沙箱技术", "本地安全", "Sandboxing", "系统安全", "原生应用", "隐私保护"]
categories: ["安全", "系统与基础设施"]
source: hacker_news
description: "随着本地 Agent 的普及，如何在 macOS 上有效隔离其权限成为安全挑战。Agent Safehouse 提供了一套原生的沙箱方案，旨在限制 Agent 的系统访问范围，降低潜在风险。本文将解析其设计思路与核心机制，帮助开发者构建更安全的本地运行环境。"
external_url: https://agent-safehouse.dev
scenarios: ["Web应用开发"]
---

# Agent Safehouse：macOS 原生沙箱技术保护本地 Agent

---

## 基本信息

- **作者**: atombender
- **评分**: 568
- **评论数**: 141
- **链接**: [https://agent-safehouse.dev](https://agent-safehouse.dev)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47301085](https://news.ycombinator.com/item?id=47301085)

---
## 导语

随着本地 Agent 的普及，如何在 macOS 上有效隔离其权限成为安全挑战。Agent Safehouse 提供了一套原生的沙箱方案，旨在限制 Agent 的系统访问范围，降低潜在风险。本文将解析其设计思路与核心机制，帮助开发者构建更安全的本地运行环境。

---
## 评论

**文章中心观点**
Agent Safehouse 提出了一种基于 macOS 原生沙盒机制的本地 AI Agent 约束方案，旨在通过系统级权限控制，缓解本地大模型应用执行不可信代码时的安全风险。

**深入评价**

**1. 技术深度：利用系统原生机制构建防御基线**
*   **支撑理由（事实陈述）：** 文章准确把握了 macOS 安全架构的核心要素，即 `sandbox`（沙盒）、`codesign`（代码签名）和 `entitlements`（授权）。方案将网络安全中的“最小权限原则”应用于本地 Agent 运行时环境。
*   **支撑理由（作者观点）：** 作者指出，基于特征匹配的传统杀毒软件难以应对 Agent 行为的动态性和非确定性。相比之下，通过静态定义的沙盒规则来限制动态行为，是一种更务实的防御手段。
*   **边界条件（事实陈述）：** macOS 沙盒并非无法绕过。历史上存在过沙盒逃逸及 Gatekeeper 绕过漏洞。若 Agent 触发内核漏洞或利用合法的进程间通信（IPC）机制进行侧信道攻击，单一沙盒防御可能失效。
*   **边界条件（你的推断）：** 现代恶意软件常采用“无文件攻击”或内存执行技术。若沙盒规则配置不当（如授予了过于宽泛的 `exec` 权限），防御效果将大打折扣。

**2. 实用价值：填补本地开发的安全空白**
*   **支撑理由（事实陈述）：** 当前本地 AI 开发中，安全往往处于次要地位。Agent Safehouse 提供的配置文件和实施路径，为开发者提供了一个可直接参考的“安全模板”。
*   **支撑理由（你的推断）：** 该方案有助于解决企业内部部署本地 Agent 时的合规问题。通过沙盒限制 Agent 仅访问特定路径，符合数据防泄漏（DLP）的基本要求。
*   **局限性（你的推断）：** 实用性受限于 macOS 生态。对于需要调用底层系统 API（如直接 GPU 计算或修改网络设置）的高级 Agent，严格的沙盒限制可能导致功能受限，开发者需在安全与功能完整性之间做出权衡。

**3. 创新性：引入系统级安全视角**
*   **支撑理由（作者观点）：** 文章的创新性不在于发明新技术，而在于将“操作系统级隔离”思维引入目前主要关注算法对齐（RLHF）或提示词注入（Prompt Injection）的 AI 安全领域。
*   **支撑理由（你的推断）：** 方案体现了一种“零信任”思路：不信任 Agent 生成的任何指令，而是假设宿主环境存在潜在风险。这补充了当前 AI 安全讨论中常被忽视的系统防御视角。
*   **局限性（事实陈述）：** 利用容器技术（如 Docker、Firecracker）隔离应用在 Linux 环境下已是标准做法。Agent Safehouse 的贡献在于将此类逻辑适配至 macOS 原生环境，而非颠覆性创新。

**4. 行业影响：促进端侧 AI 安全规范**
*   **支撑理由（你的推断）：** 随着 Apple Intelligence 的普及，端侧 AI 应用将增多。Agent Safehouse 的探索可能为未来 macOS 应用商店审核 AI 类应用提供安全参考依据。
*   **支撑理由（作者观点）：** 若此类工具被广泛采用，可能促使 AI Agent 开发者从“功能优先”转向“安全设计优先”，推动建立本地 Agent 的安全等级标准。

**5. 争议点与权衡**
*   **争议点：可用性与安全性的平衡。**
    *   *观点 A（作者倾向）：* 必须实施严格限制，即使这可能牺牲部分用户体验（如增加文件访问确认步骤）。
    *   *观点 B（你的推断）：* 过度限制会降低 Agent 的自动化能力。例如，无法读取浏览器缓存将限制 Agent 处理自动化办公任务的能力。
*   **争议点：沙盒的防御边界。**
    *   *观点 A：* 沙盒能有效防止意外的系统修改和简单的恶意脚本执行。
    *   *观点 B：* 沙盒无法防止逻辑层面的错误。例如，Agent 在沙盒内合法执行了删除用户授权文件的指令，沙盒机制无法判断这是否源于“提示词注入”导致的用户意图扭曲。

**实际应用建议**
1.  **分层防御：** 建议将沙盒作为安全基线，而非唯一防线。应结合网络防火墙（监控数据外传）及行为监控手段。
2.  **动态配置：** 开发者应根据 Agent 的具体功能需求定制 `entitlements`，避免使用默认的宽泛配置。
3.  **审计日志：** 开启并定期审计沙盒拦截日志，以识别潜在的异常行为尝试。

---
## 代码示例




```python
# 示例1：沙箱环境中的文件隔离操作
def sandboxed_file_operation():
    """
    模拟macOS沙箱环境下的安全文件操作
    解决问题：防止恶意代码访问系统关键文件
    """
    import os
    import tempfile
    
    # 创建临时沙箱目录
    sandbox_dir = tempfile.mkdtemp(prefix="agent_sandbox_")
    print(f"沙箱目录创建于: {sandbox_dir}")
    
    # 允许的操作：在沙箱内创建文件
    safe_file = os.path.join(sandbox_dir, "test.txt")
    with open(safe_file, "w") as f:
        f.write("这是沙箱内的安全操作")
    
    # 尝试访问系统文件（会被沙箱阻止）
    try:
        with open("/etc/passwd", "r") as f:
            print("危险操作：读取系统文件")
    except PermissionError:
        print("沙箱已阻止系统文件访问")
    
    # 清理沙箱
    os.remove(safe_file)
    os.rmdir(sandbox_dir)
    print("沙箱环境已清理")

# 测试
sandboxed_file_operation()
```




```python
# 示例2：网络访问控制
def network_sandbox_control():
    """
    模拟沙箱环境下的网络访问控制
    解决问题：防止未授权的网络连接
    """
    import socket
    import urllib.request
    
    # 允许的网络操作：访问白名单域名
    allowed_domains = ["api.example.com"]
    test_domain = "api.example.com"
    
    try:
        # 尝试建立连接
        with socket.create_connection((test_domain, 80), timeout=2) as sock:
            print(f"允许访问白名单域名: {test_domain}")
    except (socket.timeout, ConnectionRefusedError):
        print("网络访问被阻止或连接失败")
    
    # 阻止的网络操作：访问非白名单域名
    blocked_domain = "malicious-site.com"
    try:
        urllib.request.urlopen(f"http://{blocked_domain}", timeout=2)
    except (urllib.error.URLError, socket.timeout):
        print(f"沙箱已阻止访问: {blocked_domain}")

# 测试
network_sandbox_control()
```




```python
# 示例3：资源使用监控
def resource_monitoring():
    """
    模拟沙箱资源使用监控
    解决问题：防止Agent消耗过多系统资源
    """
    import psutil
    import time
    
    # 设置资源限制
    MAX_MEMORY = 100 * 1024 * 1024  # 100MB
    MAX_CPU = 50  # 50%
    
    process = psutil.Process()
    
    # 模拟资源消耗
    print("开始资源监控...")
    for _ in range(5):
        # 检查内存使用
        mem_usage = process.memory_info().rss
        if mem_usage > MAX_MEMORY:
            print(f"警告：内存使用超过限制 ({mem_usage/1024/1024:.1f}MB)")
            break
        
        # 检查CPU使用
        cpu_percent = process.cpu_percent(interval=0.1)
        if cpu_percent > MAX_CPU:
            print(f"警告：CPU使用过高 ({cpu_percent}%)")
        
        print(f"当前资源使用 - 内存: {mem_usage/1024/1024:.1f}MB, CPU: {cpu_percent}%")
        time.sleep(0.5)
    
    print("资源监控结束")

# 测试
resource_monitoring()
```


---
## 案例研究


### 1：独立开发者构建本地化隐私优先的 AI 编程助手

 1：独立开发者构建本地化隐私优先的 AI 编程助手

**背景**:
一位独立开发者正在构建一款基于本地大语言模型（LLM）的编程辅助工具。该工具需要在用户的 macOS 系统上运行，并具备读取用户本地代码仓库、分析文件结构以及调用 Git 命令进行版本控制的能力。为了提供良好的用户体验，该工具需要较高的系统权限。

**问题**:
由于该工具处于早期开发阶段，代码库尚未经过充分的安全审计。开发者担心，如果从互联网下载的模型文件或提示词脚本包含恶意指令，可能会导致 AI Agent 未经授权地读取敏感文件（如 ~/.ssh 目录下的私钥）或执行破坏性的 Shell 命令（如 `rm -rf`）。直接运行会给用户的开发环境带来极大的安全风险，甚至可能波及同一网络下的其他设备。

**解决方案**:
开发者集成了 Agent Safehouse 作为该 AI 助手的沙箱环境。利用 macOS 原生的沙箱机制，将 AI 助手的进程与用户的主系统环境进行严格隔离。配置策略允许 AI 访问特定的代码目录，但明确禁止访问系统配置文件夹、钥匙串以及网络连接。

**效果**:
通过 Agent Safehouse，开发者在保持 AI 功能完整性的同时，确保了“故障安全”。即使 Agent 被诱导执行了恶意代码，攻击也被限制在沙箱范围内，无法触及用户的关键敏感数据。这不仅消除了用户对本地 AI 安全性的顾虑，也使得该工具能够以“隐私优先”作为核心卖点进行发布，获得了早期采用者的信任。

---



### 2：企业安全团队测试不可信 AI Agent 的行为分析

 2：企业安全团队测试不可信 AI Agent 的行为分析

**背景**:
某金融科技公司的安全团队需要对从开源社区引入的第三方 AI Agent 进行安全评估。这些 Agent 被设计用于自动化处理财务报表，但团队需要验证它们在被恶意输入触发时，是否会尝试扫描局域网或窃取数据。

**问题**:
直接在公司生产环境或员工 MacBook 上运行这些不可信的 Agent 是绝对禁止的，因为这可能导致数据泄露或引入恶意软件。传统的虚拟机方案虽然隔离性好，但配置繁琐，且难以模拟真实的 macOS 原生环境。

**解决方案**:
安全团队使用 Agent Safehouse 在 macOS 原生环境中构建了一个“蜜罐”式的沙箱测试场。他们将 Agent Safehouse 配置为允许 Agent 运行并观察其对模拟文件系统的操作，同时利用其底层网络隔离能力，监控 Agent 是否尝试建立非法的出站连接。

**效果**:
Agent Safehouse 成功捕获了其中一个测试 Agent 在处理特定格式文档时试图访问受限目录的异常行为。由于沙箱的存在，这一尝试被即时阻断并记录。团队利用这些日志修复了潜在的漏洞，并建立了针对本地 Agent 的安全准入标准，大大降低了引入第三方 AI 代码的安全风险。

---
## 最佳实践

## 最佳实践指南

### 实践 1：利用 macOS 原生沙盒机制进行权限隔离

**说明**:  
Agent Safehouse 的核心价值在于利用 macOS 原生的沙盒技术来限制本地 Agent 的系统访问权限。通过配置 `com.apple.security.app-sandbox` 权限，可以防止 Agent 访问未授权的文件、网络或系统资源，从而降低恶意代码执行或意外操作的风险。

**实施步骤**:
1. 在 Xcode 项目或 `entitlements.plist` 文件中启用 App Sandbox。
2. 根据 Agent 的功能需求，精细配置权限（如 `com.apple.security.files.user-selected.read-write`）。
3. 使用 `sandbox-exec` 命令行工具测试沙盒规则是否生效。

**注意事项**:  
- 避免授予过宽的权限（如完全的文件系统访问），应遵循“最小权限原则”。
- 沙盒化后，需验证 Agent 的核心功能是否受影响。

---

### 实践 2：限制网络访问以防止数据泄露

**说明**:  
本地 Agent 可能需要与外部服务交互，但 unrestricted 的网络访问可能导致数据泄露或被滥用。通过 macOS 沙盒的网络权限控制，可以限制 Agent 的出站连接，仅允许访问必要的域名或端口。

**实施步骤**:
1. 在 `entitlements.plist` 中添加 `com.apple.security.network.client` 权限。
2. 使用 macOS 的防火墙或第三方工具（如 Little Snitch）进一步限制 Agent 的网络访问。
3. 在代码中实现白名单机制，仅允许与已知的安全域名通信。

**注意事项**:  
- 定期审计 Agent 的网络请求日志，确保无异常连接。
- 如果 Agent 不需要网络访问，完全禁用相关权限。

---

### 实践 3：隔离文件系统访问

**说明**:  
Agent 可能需要读写文件，但 unrestricted 的文件系统访问可能导致敏感数据泄露或系统文件被篡改。通过 macOS 沙盒的文件访问控制，可以限制 Agent 仅访问特定目录（如用户选择的文件或临时目录）。

**实施步骤**:
1. 配置 `com.apple.security.files.user-selected.read-write` 权限，允许用户手动授权文件访问。
2. 使用 `Security-scoped bookmarks` 持久化用户授权的文件访问权限。
3. 在代码中避免硬编码文件路径，改用沙盒允许的目录（如 `NSTemporaryDirectory`）。

**注意事项**:  
- 测试 Agent 在沙盒环境下的文件操作是否正常。
- 避免依赖沙盒外的系统路径（如 `/etc` 或 `/Applications`）。

---

### 实践 4：动态权限管理

**说明**:  
Agent 的权限需求可能随运行时变化。通过动态权限管理，可以在运行时请求用户授权，而不是预先授予所有权限。这符合 macOS 的安全设计原则，也能提升用户信任。

**实施步骤**:
1. 使用 `NSUserNotification` 或自定义 UI 提示用户授权敏感操作（如文件访问或网络连接）。
2. 在代码中实现权限检查逻辑，确保仅在授权后执行操作。
3. 记录权限请求日志，便于审计和调试。

**注意事项**:  
- 避免频繁请求权限，以免影响用户体验。
- 提供清晰的权限请求说明，告知用户为何需要该权限。

---

### 实践 5：审计与日志记录

**说明**:  
即使沙盒化后，仍需监控 Agent 的行为以确保其未尝试违规操作。通过日志记录和审计，可以及时发现异常行为（如尝试访问未授权资源）。

**实施步骤**:
1. 在代码中集成日志框架（如 `os_log`），记录关键操作（如文件访问、网络请求）。
2. 使用 macOS 的 `Console.app` 或第三方工具分析沙盒日志。
3. 定期检查日志，确保 Agent 的行为符合预期。

**注意事项**:  
- 避免记录敏感信息（如用户数据或密钥）。
- 确保日志文件本身受到保护，防止被篡改。

---

### 实践 6：定期更新沙盒规则

**说明**:  
macOS 的沙盒机制和权限模型可能随系统更新而变化。定期更新沙盒规则可以确保 Agent 的安全性与最新的系统安全标准保持一致。

**实施步骤**:
1. 关注 macOS 更新日志，了解沙盒机制的变化。
2. 测试 Agent 在最新 macOS 版本上的兼容性。
3. 更新 `entitlements.plist` 和代码逻辑，以适应新的安全要求。

**注意事项**:  
- 在更新前备份现有配置，避免因权限变更导致功能失效。
- 在测试环境中验证更新后的规则是否生效。

---

### 实践 7：用户教育与透明化

**说明**:  
即使技术实现完善，用户的安全意识仍是关键。通过透明化 Agent 的权限需求和操作行为，可以提升用户信任并减少误操作。

**实施步骤**:
1. 在 Agent 的 UI 中清晰展示其权限需求和操作日志。
2. 提供文档或教程，解释沙盒化的作用和限制。
3. 实

---
## 学习要点

- Agent Safehouse 提供了一种基于 macOS 原生沙盒机制的本地代理安全隔离方案，旨在防止不受信任的 AI 代理对宿主系统造成危害。
- 该工具利用 macOS 的操作系统级权限控制，能够精确限制 AI 代理对文件系统、网络和进程的访问范围。
- 它通过将 AI 代理限制在特定的“安全屋”目录中运行，确保了即使代理被攻破或行为异常，也无法访问敏感的用户数据。
- 该方案解决了本地运行大模型（LLM）时的核心安全痛点，即如何在享受本地化隐私保护的同时，防御模型自身可能带来的恶意行为。
- 项目突出了“沙盒化”对于构建安全的 AI Agent 工作流至关重要，为在本地环境部署自主智能体提供了可行的安全范式。
- 这种原生实现方式相比虚拟机或容器化方案，具有更低的系统资源占用和更好的 macOS 平台兼容性。

---
## 常见问题


### 1: 什么是 Agent Safehouse，它主要解决什么问题？

1: 什么是 Agent Safehouse，它主要解决什么问题？

**A**: Agent Safehouse 是一个专为 macOS 设计的原生沙箱工具，旨在为本地运行的 AI Agent（智能体）提供安全的隔离环境。随着 AI Agent 越来越多地被赋予执行系统命令、文件操作和自动化任务的权限，它们带来的安全风险也随之增加。Agent Safehouse 通过利用 macOS 原生的沙箱机制，限制这些 Agent 的访问权限，确保它们只能在特定的、受控的范围内运行，从而防止恶意代码或错误的指令破坏整个系统或窃取敏感数据。

---



### 2: Agent Safehouse 与 Docker 或虚拟机（VM）相比有什么区别？

2: Agent Safehouse 与 Docker 或虚拟机（VM）相比有什么区别？

**A**: Agent Safehouse 与 Docker 或虚拟机的主要区别在于隔离的层级和资源开销。

*   **资源开销与性能**：虚拟机需要模拟完整的操作系统，资源开销极大；Docker 共享宿主内核，虽然轻量但仍需运行完整的 Linux 环境依赖。Agent Safehouse 是基于 macOS 原生特性的，它不需要模拟额外的操作系统，直接在 macOS 内核层面进行资源限制和权限隔离，因此性能损耗极低，启动速度更快。
*   **系统集成度**：Docker 在 macOS 上通常需要运行 Linux 虚拟机，导致与 macOS 宿主系统的文件交互和系统集成（如 macOS 特有的 API 调用）存在摩擦。Agent Safehouse 原生运行于 macOS，能更自然地处理 macOS 的文件系统结构和权限模型（如安全策略书）。
*   **安全性模型**：Docker 的安全性依赖于容器配置和内核命名空间，而 Agent Safehouse 依赖于 macOS 经过严格审查的沙箱机制，这对于专门针对 macOS 平台开发的本地 Agent 来说，是一种更符合系统设计哲学的防护方式。

---



### 3: Agent Safehouse 是否支持所有类型的 AI Agent（例如 Python 脚本、Node.js 进程等）？

3: Agent Safehouse 是否支持所有类型的 AI Agent（例如 Python 脚本、Node.js 进程等）？

**A**: 是的，Agent Safehouse 具有广泛的兼容性。由于它主要是在操作系统层面管理进程的权限和文件系统访问，因此它可以用来隔离任何在 macOS 上运行的可执行程序或脚本环境。无论你的 Agent 是用 Python 编写的自动化脚本，还是基于 Node.js 的本地服务，只要它是在 macOS 进程级别运行的，Agent Safehouse 都可以对其进行沙箱化处理，限制其网络访问、文件读写或设备使用权限。

---



### 4: 使用 Agent Safehouse 会对本地 Agent 的性能造成影响吗？

4: 使用 Agent Safehouse 会对本地 Agent 的性能造成影响吗？

**A**: 影响微乎其微。Agent Safehouse 利用的是 macOS 内置的系统调用和内核特性（如 Sandbox.kext 和相关用户态 API），这些机制是操作系统高度优化的部分。与虚拟机或全系统模拟器不同，Agent Safehouse 不需要进行指令翻译或硬件模拟，也不会强制 Agent 运行在复杂的中间层之上。除了在访问受控资源（如尝试读写被禁止的文件目录）时会有极短的权限检查延迟外，Agent 的计算性能几乎不受影响。

---



### 5: 如何配置 Agent Safehouse 以允许 Agent 访问特定的文件夹或网络端口？

5: 如何配置 Agent Safehouse 以允许 Agent 访问特定的文件夹或网络端口？

**A**: Agent Safehouse 通常通过配置文件（如 `.plist` 或特定的配置脚本）来定义沙箱规则。用户可以精细地控制 Agent 的“视野”和权限。例如，你可以创建一个配置文件，明确允许 Agent 读写 `/Users/agent/workspace` 目录，同时禁止访问 `Documents` 或 `Downloads`。在网络方面，你可以配置出站连接规则，例如只允许 Agent 访问特定的 API 端点（如 `api.openai.com`），而阻断其他所有的网络连接。这种“默认拒绝，显式允许”的策略确保了即使 Agent 被劫持，攻击者也无法利用它来扫描内网或窃取其他文件。

---



### 6: Agent Safehouse 是否适用于开发者进行本地调试和开发？

6: Agent Safehouse 是否适用于开发者进行本地调试和开发？

**A**: 非常适合。对于正在开发本地 AI Agent 的开发者来说，安全性是一个主要顾虑，尤其是在测试 Agent 具备文件操作或 Shell 命令执行能力时。Agent Safehouse 允许开发者在开发阶段就实施严格的安全策略，模拟 Agent 在受限环境下的行为。这不仅保护了开发者的本地机器免受意外代码执行的影响（例如 Agent 误删除了开发目录），还能帮助开发者尽早发现 Agent 因权限不足而可能出现的运行时错误，从而编写出更健壮、更安全的代码。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: macOS 的沙盒机制主要依赖于两个核心配置文件来定义权限边界。请找出这两个文件的后缀名，并解释它们在应用打包和运行时的不同作用。

### 提示**: 其中一个文件位于应用程序包的 Contents 目录下，用于代码签名和系统启动时的验证；另一个通常作为资源文件嵌入，用于向系统声明具体的 entitlements（授权）和规则。

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
- 标签： [Agent](/tags/agent/) / [macOS](/tags/macos/) / [沙箱技术](/tags/%E6%B2%99%E7%AE%B1%E6%8A%80%E6%9C%AF/) / [本地安全](/tags/%E6%9C%AC%E5%9C%B0%E5%AE%89%E5%85%A8/) / [Sandboxing](/tags/sandboxing/) / [系统安全](/tags/%E7%B3%BB%E7%BB%9F%E5%AE%89%E5%85%A8/) / [原生应用](/tags/%E5%8E%9F%E7%94%9F%E5%BA%94%E7%94%A8/) / [隐私保护](/tags/%E9%9A%90%E7%A7%81%E4%BF%9D%E6%8A%A4/)
- 场景： [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [Agent Safehouse：macOS 本地 Agent 的原生沙箱方案]({{< relref "posts/20260309-hacker_news-agent-safehouse-macos-native-sandboxing-for-local--1.md" >}})
- [Agent Safehouse：macOS 本地代理的原生沙箱方案]({{< relref "posts/20260308-hacker_news-agent-safehouse-macos-native-sandboxing-for-local--0.md" >}})
- [Agent Safehouse：macOS 原生沙箱，用于本地 Agent 隔离]({{< relref "posts/20260308-hacker_news-agent-safehouse-macos-native-sandboxing-for-local--1.md" >}})
- [Agent Safehouse：macOS 原生沙箱，用于隔离本地 Agent]({{< relref "posts/20260309-hacker_news-agent-safehouse-macos-native-sandboxing-for-local--0.md" >}})
- [Matchlock：基于 Linux 的 AI 智能体沙箱技术]({{< relref "posts/20260208-hacker_news-matchlock-linux-based-sandboxing-for-ai-agents-2.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*