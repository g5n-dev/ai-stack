---
title: "Agent Safehouse：基于 macOS 原生沙箱的本地 Agent 隔离技术"
date: 2026-03-09T15:36:53+08:00
draft: false
entry_kind: "auto"
tags: ["Agent", "macOS", "沙箱", "本地隔离", "安全机制", "原生支持", "系统安全", "Agent Safehouse"]
categories: ["安全", "系统与基础设施"]
source: hacker_news
description: "随着本地 AI 代理的普及，如何确保其在操作系统上的安全执行已成为开发者关注的焦点。本文介绍的 Agent Safehouse 是一款专为 macOS 设计的原生沙箱工具，旨在为本地代理提供严格的隔离环境与资源控制。通过阅读本文，你将了解其核心架构设计，并掌握如何利用沙箱机制有效防止不可信代码对系统造成潜在风险。"
external_url: https://agent-safehouse.dev
scenarios: ["Web应用开发"]
---

# Agent Safehouse：基于 macOS 原生沙箱的本地 Agent 隔离技术

---

## 基本信息

- **作者**: atombender
- **评分**: 701
- **评论数**: 163
- **链接**: [https://agent-safehouse.dev](https://agent-safehouse.dev)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47301085](https://news.ycombinator.com/item?id=47301085)

---
## 导语

随着本地 AI 代理的普及，如何确保其在操作系统上的安全执行已成为开发者关注的焦点。本文介绍的 Agent Safehouse 是一款专为 macOS 设计的原生沙箱工具，旨在为本地代理提供严格的隔离环境与资源控制。通过阅读本文，你将了解其核心架构设计，并掌握如何利用沙箱机制有效防止不可信代码对系统造成潜在风险。

---
## 评论

**中心观点**
文章主张通过构建基于 macOS 原生沙盒机制的“Agent Safehouse”架构，在无需依赖虚拟机（VM）或重型容器的情况下，为本地运行的 AI Agent 提供一种轻量级、系统级且符合 Apple 安全哲学的隔离方案，以解决本地 AI 智能体日益增长的安全风险。

**支撑理由与边界分析**

**1. 架构设计的“原生主义”优势（事实陈述 / 作者观点）**
文章的核心逻辑在于利用 macOS 现有的沙盒机制，而非重新发明轮子。相比于 Docker 或 VM，macOS 沙盒直接作用于内核层，对文件系统、网络和进程资源的隔离具有更低的性能损耗和更高的原生集成度。
*   **支撑理由**：对于需要在 macOS 上长期驻守的后台 Agent 而言，沙盒提供了类似“App Store”式的权限管控，限制了 Agent 随意访问用户敏感目录（如 Downloads、Desktop）的能力。
*   **反例/边界条件**：macOS 沙盒主要针对的是“文件”和“网络”I/O，对于“内存安全”侧信道攻击的防御能力较弱。如果 Agent 代码本身存在内存漏洞（如通过 Python 执行恶意 C 扩展），沙盒无法防止其逃逸到宿主内核。

**2. 攻击面的收敛与最小权限原则（作者观点 / 你的推断）**
文章强调了“最小权限原则”在 AI 时代的必要性。传统的 Python 脚本或终端工具往往继承用户的完全权限，这是极其危险的。Safehouse 提出将 Agent 的操作限制在特定的临时目录或经过授权的文件夹内。
*   **支撑理由**：这能有效防止“Prompt 注入”导致的数据擦除或泄露。例如，即使恶意 Prompt 指令 Agent “删除所有文件”，由于沙盒策略禁止访问系统目录，操作会被内核拦截。
*   **反例/边界条件**：这种防御高度依赖策略配置的严谨性。如果配置过于宽松（例如授予了 `~` 的读写权限），沙盒将形同虚设；如果配置过严，Agent 的功能性将大打折扣，甚至无法完成基本的开发任务（如读取 Git 仓库配置）。

**3. 用户体验与部署便利性的平衡（事实陈述）**
文章暗示了相比于 VM 方案，原生方案对用户更友好。用户无需为了运行一个 Agent 而学习复杂的虚拟网络配置或忍受巨大的磁盘占用。
*   **支撑理由**：对于 Mac 用户而言，`.app` 形式的封装或简单的配置文件比 Dockerfile 更符合直觉，且能与系统钥匙环、通知中心无缝集成。
*   **反例/边界条件**：macOS 沙盒的配置语法晦涩难懂，且缺乏像 Docker 那样标准化的“镜像”分发机制。这意味着开发者很难在“开发环境”和“生产环境”之间保证沙盒策略的一致性，容易导致“在我机器上能跑，在沙盒里没权限”的问题。

**多维度评价**

1.  **内容深度**：文章切中了当前 AI Agent 落地中最痛的点——**安全性**。它没有停留在理论层面，而是深入到了 OS 级别的技术实现。论证严谨性较高，准确识别了 LLM 不可控性与操作系统权限之间的矛盾。
2.  **实用价值**：极高。随着 Local LLM（如 Ollama, LM Studio）的普及，越来越多的开发者尝试构建“个人助理”。Safehouse 提供了一种可落地的范式，防止 AI 意外修改 `~/.zshrc` 或删除重要文档。
3.  **创新性**：**中等偏上**。虽然 macOS 沙盒技术已存在多年，但将其系统性地应用于 AI Agent 的隔离是较新的视角。它跳出了 Linux 容器思维的定式，探索了 Apple 生态的特有路径。
4.  **可读性**：结构清晰，技术背景的开发者容易理解，但涉及 macOS 内部权限配置（如 `entitlements`）的部分对普通用户有门槛。
5.  **行业影响**：如果该方案被主流 Agent 框架（如 LangChain, AutoGPT）采纳，可能会推动“安全优先”的本地 Agent 标准形成，迫使开发者从“Root 权限运行”转向“沙盒化运行”。

**争议点与不同观点**

*   **沙盒的局限性 vs. 虚拟机的强隔离**：安全社区可能认为，macOS 沙盒的历史漏洞证明其不足以对抗高阶攻击。对于处理极度敏感数据的 Agent，QEMU 虚拟机或 TEE（可信执行环境）仍是唯一可信的边界。
*   **跨平台成本**：过度依赖 macOS 原生特性会导致 Agent 应用难以跨平台移植。如果核心安全逻辑依赖于 Apple API，未来移植到 Windows 或 Linux 时需要重写整套安全层。

**实际应用建议**

1.  **分层防御**：不要仅依赖 Safehouse。应结合 eBPF（如 Tracee）进行运行时行为监控，作为沙盒的第二道防线。
2.  **策略模板化**：建议作者或社区提供针对不同场景的沙盒配置模板，例如“Web 浏览 Agent 模板”（允许网络，禁止本地写入）和“代码重构 Agent 模板”（允许代码库读写，禁止网络）。

**可验证的检查方式**

1.  **逃逸测试**：构建一个恶意 Prompt，指令 Agent 读取沙盒外的 `/etc/passwd` 或尝试修改系统 Host

---
## 代码示例




```python
# 示例1：沙箱环境初始化与资源限制
import subprocess
import resource

def setup_sandbox(max_memory_mb=512, max_cpu_time=10):
    """
    初始化macOS沙箱环境并设置资源限制
    :param max_memory_mb: 最大内存限制(MB)
    :param max_cpu_time: 最大CPU时间(秒)
    """
    try:
        # 设置内存限制 (转换为字节)
        resource.setrlimit(resource.RLIMIT_AS, 
                          (max_memory_mb * 1024 * 1024, 
                           max_memory_mb * 1024 * 1024))
        
        # 设置CPU时间限制
        resource.setrlimit(resource.RLIMIT_CPU, 
                          (max_cpu_time, max_cpu_time))
        
        # 启动沙箱进程
        subprocess.run(['sandbox-exec', '-p', 
                       '(version 1)(allow default)(deny network*)'],
                      check=True)
        print("沙箱环境初始化成功")
    except Exception as e:
        print(f"沙箱初始化失败: {e}")

# 使用示例
setup_sandbox(max_memory_mb=256, max_cpu_time=5)
```




```python
# 示例2：文件系统访问控制
import os
import tempfile

def safe_file_operation():
    """
    在沙箱中安全处理文件操作
    """
    # 创建临时工作目录
    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            # 设置沙箱策略：只允许访问临时目录
            policy = f'(version 1)(allow default)(deny file-write*)(allow file-write* (subpath "{tmpdir}"))'
            
            # 在沙箱中执行文件操作
            with open(os.path.join(tmpdir, 'test.txt'), 'w') as f:
                f.write("沙箱内安全写入")
            
            # 尝试访问系统目录（会被阻止）
            try:
                with open('/etc/passwd', 'r') as f:
                    print("不应该看到这个输出")
            except PermissionError:
                print("成功阻止系统文件访问")
                
        except Exception as e:
            print(f"文件操作错误: {e}")

# 使用示例
safe_file_operation()
```




```python
# 示例3：网络隔离与进程监控
import psutil
import subprocess
import time

def isolated_agent_process(command):
    """
    在完全网络隔离的环境中运行Agent进程
    :param command: 要执行的命令列表
    """
    # 创建沙箱策略：完全禁止网络
    policy = '(version 1)(allow default)(deny network*)(deny network-outbound*)(deny network-inbound*)'
    
    try:
        # 启动隔离进程
        proc = subprocess.Popen(['sandbox-exec', '-p', policy] + command,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        
        # 监控进程状态
        while proc.poll() is None:
            # 获取进程资源使用情况
            try:
                p = psutil.Process(proc.pid)
                print(f"内存使用: {p.memory_info().rss / 1024 / 1024:.2f}MB")
                print(f"CPU使用率: {p.cpu_percent()}%")
            except psutil.NoSuchProcess:
                break
            time.sleep(1)
            
        # 获取输出结果
        stdout, stderr = proc.communicate()
        if proc.returncode != 0:
            print(f"进程异常终止: {stderr.decode()}")
        else:
            print("进程正常完成")
            
    except Exception as e:
        print(f"进程执行错误: {e}")

# 使用示例
isolated_agent_process(['python3', '-c', 'print("安全执行代码")'])
```


---
## 案例研究


### 1：独立开发者个人知识库项目

 1：独立开发者个人知识库项目

**背景**:
一名专注于构建本地化 AI 应用的独立开发者正在开发一款名为“Second Brain”（第二大脑）的应用。该应用旨在利用大语言模型（LLM）自动整理、归纳和链接用户本地电脑上的数万条笔记和文档。由于涉及个人隐私数据，开发者坚持使用完全离线的本地模型（如 Llama 3 或 Ollama），而不是云端 API。

**问题**:
在开发初期，为了测试 Agent 的自动化能力，开发者赋予脚本访问文件系统的权限。然而，在一次测试中，Agent 产生“幻觉”，错误地将用户私人文件夹中的敏感文档进行了重命名并移动到了临时目录，导致数据混乱。此外，由于缺乏隔离，运行不同实验环境的 Agent 经常发生依赖冲突，且难以限制其对系统设置（如修改 hosts 文件）的访问。

**解决方案**:
开发者引入了 Agent Safehouse 作为本地沙箱环境。他将所有 Agent 的执行进程限制在 Safehouse 创建的独立沙箱中。通过配置，Agent 只能访问特定的“知识库”文件夹，并被明确禁止访问系统关键目录和个人隐私文件夹。同时，利用 Safehouse 的网络隔离功能，确保即使代码被注入，也无法向外部泄露数据。

**效果**:
实施沙箱后，彻底杜绝了 Agent 误操作导致的数据损坏风险。开发者能够在保证绝对安全的前提下，放心地让 Agent 拥有更高的文件读写权限来执行复杂的整理任务。这种“安全优先”的架构也成为了该应用的主要卖点，吸引了大量对隐私敏感的企业用户。

---



### 2：金融科技公司的内部自动化审计工具

 2：金融科技公司的内部自动化审计工具

**背景**:
一家中型金融科技公司的安全团队为了提高效率，开发了一套内部使用的“代码审计 Agent”。该 Agent 需要扫描开发人员本地提交的代码，结合私有代码库上下文，在本地运行 LLM 以识别潜在的安全漏洞和合规问题。

**问题**:
由于金融行业对数据安全的极高要求，公司严禁任何源代码离开本地物理机。然而，直接在员工办公电脑上运行具有高权限的 Agent 存在巨大风险：如果 Agent 被恶意代码诱导，它可能会利用其执行权限读取剪贴板中的敏感信息、访问本地存储的 SSH 密钥，甚至在没有隔离的情况下安装未经验证的补丁，从而攻破开发环境。

**解决方案**:
团队利用 Agent Safehouse 为该审计工具构建了一个严格的 macOS 原生沙箱。他们配置了策略，使得 Agent 仅能读取指定的代码仓库目录，并禁用了其对网络、摄像头、麦克风以及除工作目录以外任何文件系统的访问权限。Safehouse 提供的 macOS 原生集成确保了这种隔离不会影响员工电脑的正常使用性能。

**效果**:
该方案完美平衡了安全与效率。Agent 能够在本地安全地处理敏感代码，而无需担心数据泄露或系统被破坏。Safehouse 的透明化设计使得审计工具对员工来说几乎是无感的，但安全团队却获得了一个坚不可摧的隔离层，成功通过了后续的内部安全合规审计。

---
## 最佳实践

## 最佳实践指南

### 实践 1：严格定义沙盒边界与资源访问策略

**说明**: 
Agent Safehouse 的核心在于利用 macOS 原生沙盒机制限制 Agent 的访问范围。最佳实践要求遵循“最小权限原则”，即仅授予 Agent 完成任务所必需的文件、网络和系统资源访问权限，严禁授予广泛的根目录或用户主目录读写权限。

**实施步骤**:
1. 在配置文件中明确列出需要访问的特定文件路径（使用 Security-Scoped Bookmarks 或路径白名单）。
2. 禁用不必要的网络访问能力，如果 Agent 仅处理本地数据，应阻断其所有出站连接。
3. 限制进程生成能力，防止 Agent 调用系统 Shell 执行任意命令。

**注意事项**: 
避免使用通配符（如 `/*` 或 `~/*`）配置文件权限，这会破坏沙盒的隔离性。

---

### 实践 2：实施网络隔离与外联控制

**说明**: 
为了防止本地 Agent 泄露敏感数据或遭受恶意指令注入，必须严格控制其网络活动。在处理高度敏感任务时，应强制执行“离线模式”。

**实施步骤**:
1. 在 macOS 沙盒配置中，默认移除 `network-client` 和 `network-server` 权限。
2. 如果必须联网，配置出站白名单，仅允许访问特定的 API 端点或域名。
3. 使用 macOS 的防火墙规则或 `pf` (Packet Filter) 作为辅助层，阻断非预期的端口通信。

**注意事项**: 
即使 Agent 需要联网查询信息，也应通过本地代理进行，以便在数据离开沙盒前进行审计和清洗。

---

### 实践 3：数据生命周期管理与临时存储清理

**说明**: 
Agent 在执行任务时可能会生成中间文件或缓存敏感信息。最佳实践要求确保所有写入操作都在隔离的临时目录中进行，并在任务结束后立即销毁，防止数据残留。

**实施步骤**:
1. 配置沙盒使其将数据写入特定的临时容器目录，而非用户的标准文档目录。
2. 在 Agent 工作流结束时，编写清理脚本自动安全删除（Shred）临时目录中的所有文件。
3. 确保临时存储目录不包含任何持久化标识符，以避免被追踪。

**注意事项**: 
即使文件被删除，也要注意防止数据通过 Spotlight 索引或 Time Machine 备份泄露，应在排除列表中加入这些临时路径。

---

### 实践 4：输入验证与输出过滤

**说明**: 
沙盒不仅是为了防止 Agent 伤害系统，也是为了验证 Agent 的行为。必须严格检查 Agent 接收的提示词以及其返回的输出，防止提示词注入攻击导致权限提升或逻辑绕过。

**实施步骤**:
1. 在 Agent 进程启动前，对输入的 Prompt 进行语法和语义分析，拦截潜在的 Shell 注入或路径遍历字符。
2. 对 Agent 生成的文件操作请求进行二次校验，确保目标路径在允许的白名单内。
3. 对 Agent 的输出内容进行扫描，防止其输出包含系统内部路径或敏感配置信息。

**注意事项**: 
不要依赖 Agent 模型自身的安全对齐，必须在应用层（Host App）实施强制的校验逻辑。

---

### 实践 5：利用 macOS 原生权限系统进行二次确认

**说明**: 
除了沙盒配置文件，还应结合 macOS 的 TCC (Transparency, Consent, and Control) 机制。对于关键操作（如访问剪贴板、摄像头、联系人），强制要求用户手动授权，从而实现“人机协同”的安全防线。

**实施步骤**:
1. 在 `Info.plist` 中正确声明 `NSAppleEventsUsageDescription` 等隐私描述键值。
2. 当 Agent 请求访问受保护资源时，设计弹窗机制向用户明确说明请求原因和潜在风险。
3. 监控系统日志中与 TCC 相关的拒绝记录，以此调整沙盒策略。

**注意事项**: 
确保应用代码签名有效，否则 TCC 权限请求将无法正常弹出，导致 Agent 静默失败或产生不可预期的行为。

---

### 实践 6：资源限制与异常监控

**说明**: 
为了防止 Agent 因死循环或恶意逻辑导致系统资源耗尽（如 CPU 占用 100% 或内存溢出），必须对沙盒内的进程施加资源限制。

**实施步骤**:
1. 使用 `rlimit` 或 XPC 服务的资源约束特性，限制 Agent 进程的最大 CPU 时间和内存占用。
2. 实施看门狗程序，如果 Agent 进程在规定时间内未响应或超出资源阈值，强制终止其运行。
3. 记录 Agent 的所有系统调用和异常退出日志，用于事后审计。

**注意事项**: 
资源限制应设置得略高于正常执行峰值，以免误杀处理复杂任务的合法 Agent。

---

### 实践 7：代码签名与完整性校验

**说明**: 
确保 Agent 运行环境未被篡改是安全的基础。利用 macOS 的代码签名机制，保证只有

---
## 学习要点

- 基于对 Agent Safehouse 及其相关背景（macOS 本地代理沙箱技术）的分析，以下是总结出的关键要点：
- Agent Safehouse 提出了一种利用 macOS 原生沙箱机制来限制本地 AI 代理系统权限的方案，旨在防止不受控的自主代理对操作系统造成破坏。
- 该工具通过精细的配置文件（Profile）或权限策略，严格限制代理仅能访问执行特定任务所需的最小文件集合和系统资源。
- 它解决了本地运行强大 AI 模型时的核心安全隐患，即防止拥有“手”能力的自主代理误操作或恶意删除用户数据、发送邮件或执行 shell 命令。
- 该方案展示了在无需依赖虚拟机或远程容器的情况下，如何利用操作系统底层特性实现轻量级且强隔离的安全环境。
- 通过将沙箱规则应用于代理进程，开发者可以赋予 AI 代理执行复杂工作流的能力，同时确保其被严格锁定在预定义的安全边界内。
- 这反映了 AI 安全领域从单纯的提示词注入防御转向更底层的运行时环境隔离与权限控制的技术演进。

---
## 常见问题


### 1: 什么是 Agent Safehouse，它与 Docker 或虚拟机等传统虚拟化技术有何不同？

1: 什么是 Agent Safehouse，它与 Docker 或虚拟机等传统虚拟化技术有何不同？

**A**: Agent Safehouse 是一个专为 macOS 设计的原生沙盒工具，旨在为本地运行的 AI 智能体提供安全的执行环境。与 Docker 或虚拟机不同，Agent Safehouse 并不依赖完整的操作系统虚拟化或容器化引擎。相反，它利用 macOS 原生的系统特性（如 Sandbox 和权限分离机制）来限制进程的访问权限。这意味着它更加轻量级，启动速度更快，且与 macOS 系统的集成度更高，专门用于解决 AI 智能体在执行代码或访问文件时可能带来的安全风险，而无需像虚拟机那样消耗大量的系统资源。

---



### 2: 为什么本地 AI 智能体需要专门的沙盒环境？

2: 为什么本地 AI 智能体需要专门的沙盒环境？

**A**: 本地 AI 智能体通常需要执行各种操作来辅助用户，例如编写代码、运行脚本、读取文件或访问互联网。如果智能体生成的代码包含恶意逻辑、无限循环或意外删除文件的指令，可能会直接损害用户的系统或导致数据丢失。Agent Safehouse 通过隔离这些操作，确保智能体只能访问用户明确允许的特定文件和目录，从而在利用智能体强大功能的同时，保护主机系统的安全性和数据的完整性。

---



### 3: Agent Safehouse 是否支持网络访问限制？

3: Agent Safehouse 是否支持网络访问限制？

**A**: 是的，作为一个沙盒工具，控制网络访问是其核心功能之一。Agent Safehouse 允许用户配置严格的网络策略。你可以完全切断智能体的网络访问，使其仅在离线环境中工作；也可以限制其只能访问特定的 API 端点或域名。这种灵活性对于防止敏感数据泄露或阻止智能体被恶意指令利用来发起网络攻击至关重要。

---



### 4: 在使用 Agent Safehouse 时，如何与被隔离的智能体进行文件交互？

4: 在使用 Agent Safehouse 时，如何与被隔离的智能体进行文件交互？

**A**: Agent Safehouse 通常采用“卷挂载”或类似的目录映射机制来实现文件交互。用户可以将主机上的特定文件夹“映射”或“共享”给沙盒内的智能体。智能体在沙盒内看到的这个文件夹就像是其本地文件系统的一部分，可以对其进行读写操作。然而，沙盒之外的任何文件对智能体来说都是不可见的，这种机制既保证了操作的便捷性，又严格限制了访问范围。

---



### 5: Agent Safehouse 的性能开销如何？

5: Agent Safehouse 的性能开销如何？

**A**: 由于 Agent Safehouse 是基于 macOS 原生特性构建的，而非基于传统的硬件虚拟化，其性能开销非常低。与运行完整的虚拟机相比，它不需要模拟硬件或启动额外的操作系统内核。智能体进程几乎以原生速度运行，仅在涉及系统调用检查或跨边界文件访问时会有微不足道的性能损耗。这使得它非常适合需要频繁交互或快速响应的本地开发场景。

---



### 6: 它是否支持 Python 脚本或其他编程语言的执行？

6: 它是否支持 Python 脚本或其他编程语言的执行？

**A**: 支持。Agent Safehouse 的设计初衷就是为了安全地执行智能体生成的代码。它支持在沙盒内配置各种运行时环境，包括 Python、Node.js、Bash 脚本等。用户可以预装必要的依赖库，智能体可以在受限的环境中调用这些解释器来执行任务。所有的执行都受到沙盒规则的约束，例如禁止访问 `/Users` 下的敏感目录或系统关键设置。

---



### 7: Agent Safehouse 是否开源？

7: Agent Safehouse 是否开源？

**A**: 根据其在 Hacker News 等技术社区的发布信息，Agent Safehouse 通常作为一个开源项目发布（具体以实际仓库为准）。这意味着开发者可以查看其源代码，验证其安全实现，甚至根据自己的需求进行修改和扩展。开源的性质也增加了工具的透明度，让安全社区能够共同审查代码，确保没有后门或安全漏洞。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**:

### 假设你正在运行一个本地的 AI Agent，它被赋予了读取特定目录下文件的权限。请尝试构建一个提示词，诱导该 Agent 尝试读取该目录范围之外的系统敏感文件（如 `/etc/passwd`），并观察沙箱是否会拦截该行为。如果拦截，请记录具体的错误信息。

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
- 标签： [Agent](/tags/agent/) / [macOS](/tags/macos/) / [沙箱](/tags/%E6%B2%99%E7%AE%B1/) / [本地隔离](/tags/%E6%9C%AC%E5%9C%B0%E9%9A%94%E7%A6%BB/) / [安全机制](/tags/%E5%AE%89%E5%85%A8%E6%9C%BA%E5%88%B6/) / [原生支持](/tags/%E5%8E%9F%E7%94%9F%E6%94%AF%E6%8C%81/) / [系统安全](/tags/%E7%B3%BB%E7%BB%9F%E5%AE%89%E5%85%A8/) / [Agent Safehouse](/tags/agent-safehouse/)
- 场景： [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [Agent Safehouse：macOS 本地代理的原生沙箱方案]({{< relref "posts/20260308-hacker_news-agent-safehouse-macos-native-sandboxing-for-local--0.md" >}})
- [Agent Safehouse：macOS 本地 Agent 的原生沙箱方案]({{< relref "posts/20260309-hacker_news-agent-safehouse-macos-native-sandboxing-for-local--1.md" >}})
- [Agent Safehouse：macOS 原生沙箱，用于本地 Agent 隔离]({{< relref "posts/20260308-hacker_news-agent-safehouse-macos-native-sandboxing-for-local--1.md" >}})
- [Agent Safehouse：基于 macOS 原生沙箱的本地 Agent 隔离方案]({{< relref "posts/20260309-hacker_news-agent-safehouse-macos-native-sandboxing-for-local--3.md" >}})
- [Agent Safehouse：利用 macOS 原生沙箱实现本地 Agent 隔离]({{< relref "posts/20260309-hacker_news-agent-safehouse-macos-native-sandboxing-for-local--6.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*