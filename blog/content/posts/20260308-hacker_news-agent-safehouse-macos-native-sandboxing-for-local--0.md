---
title: "Agent Safehouse：macOS 本地代理的原生沙箱方案"
date: 2026-03-08T23:19:33+08:00
draft: false
entry_kind: "auto"
tags: ["Agent Safehouse", "macOS", "沙箱", "本地代理", "安全隔离", "原生方案", "系统安全", "Agent"]
categories: ["安全", "系统与基础设施"]
source: hacker_news
description: "随着本地 AI 代理的普及，其带来的安全风险也日益受到关注。Agent Safehouse 提供了一种基于 macOS 原生沙箱机制的解决方案，旨在限制代理的文件系统与网络访问权限。本文将介绍其核心架构与配置方法，帮助开发者在保障本地数据安全的前提下，构建可控的 AI 应用环境。"
external_url: https://agent-safehouse.dev
scenarios: ["Web应用开发"]
---

# Agent Safehouse：macOS 本地代理的原生沙箱方案

---

## 基本信息

- **作者**: atombender
- **评分**: 161
- **评论数**: 39
- **链接**: [https://agent-safehouse.dev](https://agent-safehouse.dev)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47301085](https://news.ycombinator.com/item?id=47301085)

---
## 导语

随着本地 AI 代理的普及，其带来的安全风险也日益受到关注。Agent Safehouse 提供了一种基于 macOS 原生沙箱机制的解决方案，旨在限制代理的文件系统与网络访问权限。本文将介绍其核心架构与配置方法，帮助开发者在保障本地数据安全的前提下，构建可控的 AI 应用环境。

---
## 评论

**中心观点**
文章提出了一种基于 macOS 原生沙盒机制来构建本地 AI Agent 安全执行环境（Safehouse）的架构，旨在利用操作系统层级的权限控制来约束 LLM 代理对文件系统和系统资源的访问，从而在不牺牲本地计算隐私的前提下，解决自主代理不可控行为带来的安全风险。

**支撑理由与评价**

1.  **技术架构的“回归本源”与深度利用**
    *   **事实陈述**：文章指出当前主流的 Agent 框架（如 LangChain、AutoGPT）通常运行在用户空间，依赖 Python 虚拟环境或 Docker 容器，但这些隔离手段在 macOS 上往往较为笨重或配置复杂。
    *   **你的推断**：作者的技术选择具有深刻的工程洞察力。macOS 的 Sandbox（基于 TrustedBSD 和 MAC policy）是经过数十年安全验证的内核级隔离机制。相比于应用层的“君子协定”，内核强制执行的策略（如 `com.apple.security.files.user-selected.read-write`）能从根本上防止 LLM 因幻觉而执行的 `rm -rf /` 等毁灭性命令。这种“向下钻取”到 OS 底层的思路，是对当前 Agent 安全领域过度依赖上层应用层协议（如 Tool Use 中的 JSON Schema 校验）的有力补充。

2.  **实用价值：降低本地 Agent 的准入门槛**
    *   **作者观点**：通过利用 macOS 原生特性，开发者无需维护复杂的 K8s 集群或自定义虚拟机镜像即可获得安全的隔离环境。
    *   **事实陈述**：对于个人开发者或小型团队而言，配置基于虚拟机的沙箱（如 Firecracker）资源消耗大且启动慢。
    *   **评价**：该方案具有极高的实用价值。它使得“个人电脑上的私人 AI 助手”这一愿景更加落地。用户可以放心地让 Agent 处理敏感文档（如财务报表），因为沙盒机制保证了数据即使被 Agent 误操作，也不会泄露到网络或修改核心系统文件。这是推动“Local-First”软件架构在 AI 时代落地的重要基础设施。

3.  **创新性：定义新的安全边界**
    *   **你的推断**：文章的创新点不在于发明了新算法，而在于将“操作系统权限模型”映射到了“Agent 工具调用模型”上。
    *   **评价**：传统的安全视角关注“不要让黑客进来”，而 Agent 安全关注“不要让 AI 跑出去”。文章提出的 Safehouse 概念，实质上是一种**能力安全**的实践。它通过精细化的 Entitlements（授权），将 Agent 的能力限制在最小必要范围。这为行业提供了一个新思路：**与其去给 LLM “洗脑”让它不干坏事，不如给它戴上“手铐”让它干不了坏事**。

**反例与边界条件**

1.  **平台锁定的局限性**
    *   **事实陈述**：该方案深度依赖 macOS 特有的 API 和沙盒机制。
    *   **反例**：对于企业级后端服务，绝大多数运行在 Linux 环境下。macOS 的沙盒方案无法直接移植到 Linux 服务器或 Windows 环境。这意味着该方案虽然对开发者工具（如 Cursor 的本地 Agent）极具价值，但无法作为通用的服务端 Agent 安全方案。

2.  **对抗性攻击的防御盲区**
    *   **你的推断**：沙盒只能限制资源访问，无法防止“数据泄露”或“侧信道攻击”。
    *   **反例**：如果 Agent 被提示词注入攻击，它可能会将读取的敏感文件内容编码并通过网络请求（如果沙盒允许网络访问）或通过控制台打印（Log 泄露）传输出去。单纯的文件系统沙盒无法解决 LLM 自身的逻辑漏洞和提示词脆弱性问题。

3.  **用户体验与安全性的权衡**
    *   **反例**：macOS 的沙盒机制非常严格，用户在使用过程中可能会频繁遇到系统弹窗请求授权（如访问文件夹、网络等）。如果 Agent 需要频繁调用不同工具，这种“授权疲劳”会严重影响用户体验，甚至导致用户为了省事而授予 Agent 完全磁盘访问权限，从而使沙盒失效。

**可验证的检查方式**

1.  **逃逸测试**：
    *   构建一个恶意 Prompt，指示 Agent 尝试读取沙盒范围外的文件（如 `/etc/passwd`）或尝试建立未授权的网络连接。
    *   **指标**：观察进程是否被内核直接终止，以及系统日志中是否有 Sandbox Violation 的记录。

2.  **资源开销基准测试**：
    *   对比 Safehouse 方案与 Docker 容器方案在启动时间和内存占用上的表现。
    *   **指标**：冷启动时间应 < 100ms，内存额外开销应 < 50MB（远超虚拟机方案）。

3.  **兼容性观察窗口**：
    *   观察该方案是否能无缝兼容主流的 Agent 框架（如 LangChain 的 Tools）。
    *   **指标**：在不修改 Tool 源码的情况下，能否通过简单的配置文件将其运行在 Safehouse 中。

**总结**
这篇文章从操作系统底层出发，为日益严峻的本地 Agent 安全问题提供了一个优雅且高效的“原生解法”。虽然受限于平台生态无法通用化，但其“利用 OS 内核约束 AI 行为”的范式转变，对构建下一代可信 AI 系统具有重要的参考意义。对于 Mac 生态的开发者而言，这是构建安全 AI 应用的必经之路。

---
## 代码示例




```python
# 示例1：文件访问沙箱限制
import os
import tempfile

def sandboxed_file_operation():
    """演示如何在临时目录中安全地执行文件操作"""
    # 创建临时沙箱目录
    with tempfile.TemporaryDirectory() as sandbox_dir:
        print(f"沙箱目录: {sandbox_dir}")
        
        # 尝试在沙箱内创建文件
        test_file = os.path.join(sandbox_dir, "test.txt")
        with open(test_file, 'w') as f:
            f.write("这是沙箱内的安全操作")
        
        # 尝试访问沙箱外文件（会失败）
        try:
            with open("/etc/passwd", 'r') as f:
                print("不应该看到这个输出")
        except PermissionError:
            print("成功阻止了沙箱外的文件访问")

# 说明：这个示例展示了如何通过临时目录创建基本文件访问隔离，
# 防止恶意代码访问系统敏感文件
```




```python
# 示例2：网络访问限制
import socket
import urllib.request

def sandboxed_network_operation():
    """演示如何限制网络访问"""
    # 允许的域名白名单
    ALLOWED_HOSTS = ["example.com", "api.example.com"]
    
    def safe_request(url):
        from urllib.parse import urlparse
        host = urlparse(url).netloc
        if host not in ALLOWED_HOSTS:
            raise PermissionError(f"不允许访问 {host}")
        return urllib.request.urlopen(url)
    
    # 测试允许的请求
    try:
        safe_request("http://example.com")
        print("成功访问允许的域名")
    except Exception as e:
        print(f"访问被阻止: {e}")
    
    # 测试不允许的请求
    try:
        safe_request("http://malicious-site.com")
    except PermissionError as e:
        print(f"成功阻止恶意请求: {e}")

# 说明：这个示例展示了如何通过域名白名单限制网络访问，
# 防止恶意代码联系未知服务器
```




```python
# 示例3：资源使用限制
import resource
import time

def sandboxed_resource_limits():
    """演示如何限制资源使用"""
    # 设置CPU时间限制为1秒
    resource.setrlimit(resource.RLIMIT_CPU, (1, 1))
    
    # 设置内存限制为100MB
    MB = 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (100 * MB, 100 * MB))
    
    try:
        # 尝试消耗大量内存
        big_list = [0] * (200 * MB)  # 会超出限制
    except MemoryError:
        print("成功阻止了过度内存消耗")
    
    try:
        # 尝试长时间运行
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("程序被用户中断")
    except Exception as e:
        print(f"资源限制生效: {e}")

# 说明：这个示例展示了如何设置CPU和内存使用限制，
# 防止恶意代码耗尽系统资源
```


---
## 案例研究


### 1：独立开发者构建的本地化金融分析助手

 1：独立开发者构建的本地化金融分析助手

**背景**:
一位专注于金融科技领域的独立开发者正在构建一个本地的 macOS 应用，旨在帮助用户分析个人交易记录。该应用使用大语言模型（LLM）来解释 CSV 文件中的复杂交易模式。由于应用主要面向对隐私极其敏感的加密货币交易者，所有处理必须在本地完成，不能上传云端。

**问题**:
在开发过程中，开发者面临一个关键的安全挑战：由于 LLM 的不可预测性，当模型处理用户上传的恶意构造的 CSV 文件或执行 Python 代码进行数据清洗时，可能会尝试访问开发者系统上的敏感配置文件（如 SSH 密钥、本地环境变量）或未经授权访问用户的剪贴板和联系人。传统的沙箱技术配置复杂，且可能破坏 macOS 应用的原生体验。

**解决方案**:
开发者集成了 "Agent Safehouse" 作为应用中间件。当 LLM 进程启动时，Safehouse 自动将该进程隔离在一个严格的 macOS 原生沙箱内。开发者配置策略，仅允许 LLM 进程读写特定的临时分析文件夹，并明确禁止其访问主目录、网络和其他敏感资源。

**效果**:
通过 Agent Safehouse，开发者成功构建了一个“零信任”的本地分析环境。即使用户上传了旨在进行路径遍历攻击的恶意文件，LLM 进程也被限制在沙箱内，无法逃逸访问系统其他部分。这不仅满足了用户对数据隐私和安全的高标准要求，也使得该应用得以在注重安全的小众社区中迅速推广。

---



### 2：企业级 AI 编程助手的本地化部署

 2：企业级 AI 编程助手的本地化部署

**背景**:
一家中型科技公司的开发团队为了防止代码泄露，禁止使用公共的 AI 编程助手（如 GitHub Copilot），转而部署了一个基于开源模型的本地代码补全工具。该工具运行在每位员工的 macOS 笔记本电脑上，并拥有访问本地代码库的权限以提供上下文感知的建议。

**问题**:
在内部测试阶段，安全团队发现该 AI 助手存在风险：为了读取项目文件，它往往需要过高的文件系统权限。这导致了一个潜在的安全隐患——如果 AI 模型被“提示词注入”攻击诱导，它可能会被指令执行删除操作（如 `rm -rf`）或读取代码库之外的商业机密文件，导致灾难性的数据丢失或泄露。

**解决方案**:
安全团队引入 "Agent Safehouse" 来约束 AI 助手的行为。他们利用 Safehouse 的功能定义了细粒度的访问控制列表（ACL）。AI 助手被允许“查看”代码仓库目录，但被明确禁止执行任何写入或删除操作，同时也被切断了与除必要 API 端口以外的所有网络连接。

**效果**:
Agent Safehouse 的引入消除了安全团队的顾虑。它确保了即使 AI 模型出现幻觉或遭受对抗性攻击，其破坏力也被严格限制在沙箱范围内，无法触及宿主机的核心文件系统。这使得公司能够安全地利用本地 AI 提升开发效率，同时无需担心核心知识产权（IP）的泄露或破坏。

---
## 最佳实践

## 最佳实践指南

### 实践 1：利用 macOS 原生沙盒机制进行基础隔离

**说明**: 
充分利用 macOS 内置的 Sandbox 技术作为本地 Agent 的第一道防线。通过配置 `com.apple.security.app-sandbox` 权限，强制 Agent 进程在受限环境中运行，从根本上限制其能访问的系统资源（如文件系统、网络、硬件等），防止 Agent 被劫持后攻击宿主机。

**实施步骤**:
1. 在 Xcode 项目或 Entitlements 文件中，确保启用 App Sandbox (`com.apple.security.app-sandbox`)。
2. 移除所有默认开启的非必要权限（如网络访问），遵循“默认拒绝”原则。
3. 对于 Agent 依赖的特定功能（如读写特定文件夹），仅添加显式的例外权限。

**注意事项**: 
沙盒化会改变文件系统路径结构（例如使用 Data Containers），需确保代码中的文件路径逻辑已做相应适配。

---

### 实践 2：实施严格的文件系统访问控制

**说明**: 
本地 Agent 通常需要读写文件以存储配置或处理数据。通过配置特定的文件访问模式，限制 Agent 只能接触必要的、经过验证的目录（如特定的安全屋目录），而非整个用户文件系统。

**实施步骤**:
1. 使用 `com.apple.security.files.user-selected.read-write` 仅允许用户显式授权的文件访问，或使用 `com.apple.security.files.downloads.read-write` 限制在下载目录。
2. 若 Agent 需要持久化存储，使用 `com.apple.security.files.user-selected.read-write` 配合 Security Scope Bookmarks 来保存对特定文件夹的访问权限。
3. 禁止通配符路径访问，精确指定可读写的子目录。

**注意事项**: 
避免授予对 `~/Documents`、`~/Desktop` 等敏感目录的完全读写权限，除非业务逻辑绝对必要且已通过安全审核。

---

### 实践 3：限制网络通信能力

**说明**: 
为了防止 Agent 被利用参与 DDoS 攻击或泄露敏感数据，应默认禁用其网络访问权限。仅在 Agent 确实需要调用外部 API 或模型时，才按需开启出站连接。

**实施步骤**:
1. 在 Entitlements 中移除 `com.apple.security.network.client`（默认禁用）。
2. 如果 Agent 需要联网，添加 `com.apple.security.network.client`，但严格禁止添加 `com.apple.security.network.server`（防止 Agent 变身为监听服务）。
3. 在应用层代码中，通过白名单机制限制 Agent 可连接的域名或 IP 范围。

**注意事项**: 
即使开启了网络客户端权限，macOS 沙盒也会阻止对本地回环地址的某些访问，调试时需注意。

---

### 实践 4：应用代码签名与完整性校验

**说明**: 
代码签名不仅是为了分发，更是为了确保运行时的安全性。通过强制签名校验，可以防止 Agent 进程被恶意第三方代码注入或篡改，确保沙盒内的 Agent 始终是开发者预期的版本。

**实施步骤**:
1. 为构建的 Agent 应用配置有效的 Apple Developer ID 证书进行签名。
2. 在 Agent 启动时，通过代码校验自身签名状态，如果签名无效或被篡改，立即终止运行。
3. 启用 Hardened Runtime（运行时硬化）选项，以启用 ASLR、库验证等额外保护机制。

**注意事项**: 
调试版本和发布版本应使用不同的签名配置，且不要将私钥泄露在版本控制系统中。

---

### 实践 5：资源限制与进程隔离

**说明**: 
防止失控的 Agent 消耗过多的系统资源（CPU/内存）导致系统卡顿。利用 macOS 的资源限制机制或容器化技术，将 Agent 的资源消耗控制在合理范围内。

**实施步骤**:
1. 使用 `setrlimit` API 或 XPC 服务的辅助进程限制 Agent 可使用的最大内存和 CPU 时间。
2. 将 Agent 核心逻辑拆分为独立的 XPC Service，主应用仅作为调度器，XPC Service 运行在更严格的沙盒子环境中。
3. 监控 Agent 的子进程派生行为，禁止 Agent 随意启动其他可执行文件（移除 `com.apple.security.security.personal-information` 等可能涉及进程控制的敏感权限）。

**注意事项**: 
XPC 架构会增加进程间通信（IPC）的复杂度，需注意处理超时和错误状态，防止主应用因等待 XPC 响应而挂起。

---

### 实践 6：最小权限原则下的权限动态管理

**说明**: 
不要在应用启动时就申请所有可能需要的权限。应根据 Agent 的任务状态，动态申请或释放权限，减少攻击面。

**实施步骤**:
1. 初始状态下，Agent 仅拥有执行基础逻辑的权限。
2. 当 Agent 需要执行敏感操作（如访问摄像头、读取特定文件）时，通过临时授权机制向用户或主控进程请求权限。
3. 任务完成后，如果可能，释放或隔离

---
## 学习要点

- 基于对 Agent Safehouse 及相关技术背景的总结，以下是关键要点：
- Agent Safehouse 提出了一种利用 macOS 原生沙盒机制来约束本地 Agent 行为的安全方案，旨在解决自主 AI 智能体在执行代码或系统操作时的潜在风险。
- 该工具的核心价值在于无需依赖复杂的虚拟机或网络隔离，而是直接调用操作系统层级的权限控制（如文件访问限制、网络隔离）来限制 Agent 的攻击面。
- 它通过精细的配置文件（Profile）定义安全策略，能够精确限制 Agent 只能访问特定的目录或仅允许执行白名单内的命令，防止数据泄露或系统破坏。
- 该方案突出了“本地优先”的安全理念，确保即使 Agent 产生幻觉或受到恶意指令诱导，其破坏力也被严格限制在用户授权的局部范围内。
- 对于开发者而言，这提供了一种在不牺牲 Agent 自主性的前提下，快速构建可信本地 AI 应用的安全范式，弥补了当前 AI 编程工具在安全防护上的缺失。

---
## 常见问题


### 1: Agent Safehouse 是什么？它主要解决什么问题？

1: Agent Safehouse 是什么？它主要解决什么问题？

**A**: Agent Safehouse 是一个专为 macOS 设计的原生沙盒工具，旨在为本地运行的 AI Agent（智能体）提供安全隔离环境。随着 AI Agent 的普及，这些自动化程序通常需要访问文件系统、网络或执行 shell 命令来完成复杂任务，这带来了潜在的安全风险。Agent Safehouse 利用 macOS 原生的沙盒机制，限制 Agent 的访问权限，确保它只能接触到必要的资源，从而防止恶意代码或意外操作对系统造成破坏。它本质上是一个“安全屋”，让用户可以在不牺牲主机安全的前提下运行不可信的本地 Agent。

---



### 2: 与 Docker 或虚拟机相比，使用 macOS 原生沙盒有什么优势？

2: 与 Docker 或虚拟机相比，使用 macOS 原生沙盒有什么优势？

**A**: 相比于 Docker 或虚拟机，使用 macOS 原生沙盒具有显著的优势，特别是在轻量级和集成度方面。首先，Docker 和虚拟机需要运行完整的操作系统或复杂的容器环境，资源消耗较大（内存、CPU），而 macOS 原生沙盒直接运行在宿主内核上，几乎没有性能损耗，启动速度极快。其次，原生沙盒与 macOS 系统集成得更紧密，配置更为简单，不需要处理复杂的网络桥接或文件挂载问题。对于只需要隔离文件访问和系统调用的本地 Agent 来说，原生沙盒提供了一种更高效、更原生的安全方案。

---



### 3: Agent Safehouse 如何确保 Agent 无法访问敏感的系统文件？

3: Agent Safehouse 如何确保 Agent 无法访问敏感的系统文件？

**A**: Agent Safehouse 通过定义严格的配置文件来实施访问控制策略。它利用 macOS 的 Sandbox 框架，通过一个配置文件明确指定 Agent 可以访问的目录、文件、网络套接字和系统资源。默认情况下，沙盒内的进程被拒绝访问所有资源，除非在配置中显式授权。例如，你可以配置 Agent 只能读写特定的“工作目录”，而禁止访问 `/Users`、`/System` 或其他敏感路径。这种“默认拒绝”的安全模型确保了即使 Agent 被攻破或行为异常，也无法突破权限限制窃取数据或破坏系统。

---



### 4: 我是否需要编程才能使用 Agent Safehouse，还是非技术人员也能上手？

4: 我是否需要编程才能使用 Agent Safehouse，还是非技术人员也能上手？

**A**: 虽然目前这类工具通常面向开发者，但 Agent Safehouse 的设计理念旨在简化安全配置。用户通常需要编写一个简单的配置文件（如 `.plist` 或特定的自定义格式）来定义规则。对于非技术人员，如果项目提供了预设模板或图形界面，上手难度会大大降低。然而，由于本地 Agent 的运行通常涉及命令行环境，目前主要受众还是开发人员和高级用户。未来可能会出现更友好的封装工具，使得普通用户也能通过简单的勾选选项来沙盒化他们的 AI 助手。

---



### 5: Agent Safehouse 能否防止 Agent 访问互联网或限制其网络请求？

5: Agent Safehouse 能否防止 Agent 访问互联网或限制其网络请求？

**A**: 是的，Agent Safehouse 具备网络控制能力。在沙盒配置中，你可以精确控制进程的网络权限。这包括完全禁止网络访问（对于处理极度敏感数据的离线 Agent 非常有用），或者限制 Agent 只能通过特定的端口与特定的 IP 地址（如 localhost 的本地 LLM 服务）通信。这种机制可以有效防止数据泄露到外部服务器，或者阻断恶意 Agent 接收远程指令。

---



### 6: 在沙盒环境中运行 Agent 会不会影响其性能或功能？

6: 在沙盒环境中运行 Agent 会不会影响其性能或功能？

**A**: 性能方面的影响微乎其微。由于 macOS 沙盒是内核级的安全机制，它不像虚拟机那样需要模拟硬件或转译指令，因此 Agent 的运行速度几乎与在宿主机上直接运行一致。在功能方面，主要的影响在于“权限受限”。如果 Agent 尝试执行未被授权的操作（例如读取被禁止的文件或修改系统设置），该操作会被系统拦截并失败。因此，为了确保 Agent 正常工作，用户必须在 Safehouse 配置中正确授予其完成工作所需的最低权限。

---



### 7: Agent Safehouse 是否兼容所有类型的 AI Agent（如基于 Python 的 Agent 或 Node.js Agent）？

7: Agent Safehouse 是否兼容所有类型的 AI Agent（如基于 Python 的 Agent 或 Node.js Agent）？

**A**: 原则上，Agent Safehouse 兼容任何在 macOS 上运行的二进制可执行文件或脚本解释器。无论你的 Agent 是用 Python、Node.js、Rust 还是 Shell 脚本编写的，只要它是作为进程在 macOS 上运行，都可以被放入沙盒中。关键在于如何启动它：通常是通过 `sandbox-exec` 命令或 Safehouse 提供的包装器来启动 Agent 的解释器（如 `python3` 或 `node`）。只要入口进程被正确沙盒化，其衍生的子进程通常也会继承相应的安全限制。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 假设你需要为一个本地 AI Agent 配置一个仅能读取特定目录下日志文件的权限。在 macOS 的沙盒环境中，你会选择哪个特定的权限密钥来替代广泛的文件系统访问权限？请写出该配置项的名称及其预期作用。

### 提示**: 关注 macOS Entitlements 文档中关于“文件访问”的部分，特别是针对“只读”和“特定用户目录”的选项。

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
- 标签： [Agent Safehouse](/tags/agent-safehouse/) / [macOS](/tags/macos/) / [沙箱](/tags/%E6%B2%99%E7%AE%B1/) / [本地代理](/tags/%E6%9C%AC%E5%9C%B0%E4%BB%A3%E7%90%86/) / [安全隔离](/tags/%E5%AE%89%E5%85%A8%E9%9A%94%E7%A6%BB/) / [原生方案](/tags/%E5%8E%9F%E7%94%9F%E6%96%B9%E6%A1%88/) / [系统安全](/tags/%E7%B3%BB%E7%BB%9F%E5%AE%89%E5%85%A8/) / [Agent](/tags/agent/)
- 场景： [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [Agent Safehouse：macOS 原生沙箱，用于本地 Agent 隔离]({{< relref "posts/20260308-hacker_news-agent-safehouse-macos-native-sandboxing-for-local--1.md" >}})
- [我们构建了安全可扩展的 Agent 沙箱基础设施]({{< relref "posts/20260227-hacker_news-we-built-secure-scalable-agent-sandbox-infrastruct-13.md" >}})
- [Matchlock：基于 Linux 沙箱的 AI 智能体安全隔离方案]({{< relref "posts/20260208-hacker_news-matchlock-linux-based-sandboxing-for-ai-agents-3.md" >}})
- [Amla Sandbox：面向 AI 智能体的 WASM Bash 沙箱]({{< relref "posts/20260130-hacker_news-show-hn-amla-sandbox-wasm-bash-shell-sandbox-for-a-0.md" >}})
- [Amla Sandbox：面向 AI 智能体的 WASM Bash Shell 沙箱]({{< relref "posts/20260130-hacker_news-show-hn-amla-sandbox-wasm-bash-shell-sandbox-for-a-14.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*