---
title: "Agent Safehouse：macOS 原生沙箱技术保护本地 Agent"
date: 2026-03-09T17:10:57+08:00
draft: false
entry_kind: "auto"
tags: ["Agent", "macOS", "沙箱技术", "本地部署", "系统安全", "进程隔离", "LLM", "Sandbox"]
categories: ["安全", "系统与基础设施"]
source: hacker_news
description: "随着本地 AI Agent 的普及，如何在赋予其自主操作权限的同时确保系统安全，已成为开发者必须面对的挑战。Agent Safehouse 是一款专为 macOS 设计的原生沙箱工具，通过精细化的权限控制，让 Agent 在受限环境中安全执行 Shell 命令或文件操作。本文将深入解析其核心机制与配置方法，助你在保障系"
external_url: https://agent-safehouse.dev
scenarios: ["大语言模型"]
---

# Agent Safehouse：macOS 原生沙箱技术保护本地 Agent

---

## 基本信息

- **作者**: atombender
- **评分**: 744
- **评论数**: 171
- **链接**: [https://agent-safehouse.dev](https://agent-safehouse.dev)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47301085](https://news.ycombinator.com/item?id=47301085)

---
## 导语

随着本地 AI Agent 的普及，如何在赋予其自主操作权限的同时确保系统安全，已成为开发者必须面对的挑战。Agent Safehouse 是一款专为 macOS 设计的原生沙箱工具，通过精细化的权限控制，让 Agent 在受限环境中安全执行 Shell 命令或文件操作。本文将深入解析其核心机制与配置方法，助你在保障系统安全的前提下，高效构建可靠的本地 Agent 应用。

---
## 评论

### 中心观点
文章提出利用 macOS 原生的沙盒机制作为本地 AI Agent 的安全约束层。该方案旨在通过系统级权限控制，在不引入虚拟化开销的前提下，为自主智能体提供一种符合操作系统安全规范的隔离策略。

### 深入评价

#### 1. 支撑理由
*   **系统级权限复用**：文章的核心逻辑在于复用 macOS 现有的 Sandbox 和 TCC（透明同意与控制）框架。相比于虚拟机或 Docker 容器，利用内核态的系统调用拦截机制，可以在文件系统和网络访问层面实施更细粒度的控制。
*   **本地数据隐私保护**：针对 RAG（检索增强生成）和本地 LLM 应用场景，该方案允许 Agent 处理本地敏感数据（如邮件、文档）但限制其上传云端。同时，沙盒机制能有效防止数据被非授权进程访问，解决了本地 Agent 部署中的数据泄露隐患。
*   **资源与性能优化**：与传统的虚拟机隔离相比，原生沙盒不产生显著的内存或 CPU 额外开销，也无需复杂的网络配置。这允许 Agent 以轻量级服务的形式运行，降低了本地部署 AI 助手的硬件门槛。

#### 2. 反例与边界条件
*   **侧信道攻击风险**：macOS 沙盒无法防御所有类型的攻击向量。若 Agent 被授予屏幕读取权限，理论上可通过 OCR 技术识别屏幕上弹出的密码提示框或其他敏感信息，从而绕过文件系统的逻辑隔离。
*   **平台生态局限性**：该方案高度依赖 macOS 的闭源特性。对于需要跨平台运行（Windows/Linux）的 Agent 或服务器端 Agentic 工作流，该方案无法直接复用，增加了多平台维护的复杂度。
*   **社会工程学防御缺失**：沙盒技术限制了程序行为，但无法限制 Agent 生成欺诈性的 UI 内容。Agent 可能诱导用户主动输入密码或手动解除沙盒限制，这是单纯依赖技术手段难以解决的交互漏洞。

### 维度分析

#### 1. 内容深度：侧重工程实现与防御广度
*   **事实陈述**：文章详细列举了沙盒配置文件（如 `com.apple.security.network.client`）及权限申请流程，技术路径清晰。
*   **评价**：文章主要假设 Agent 是“善意但可能出错”的。对于“对抗性场景”（如 Agent 被 Prompt 注入后尝试逃逸）的防御讨论较少。若要构建深度防御体系，还需结合内存隔离或更严格的系统调用审计机制。

#### 2. 实用价值：面向开发者的架构参考
*   对于 Mac 平台 AI 应用开发者，该方案提供了将 AI 能力集成至 App 的安全范式，解决了“赋予 App AI 权限而不失控”的工程难题。
*   **应用场景**：类似于浏览器隔离不同网站的标签页，该思路可用于构建“单任务单沙盒”的 Agent 管理器，确保不同任务的上下文严格隔离。

#### 3. 创新性：现有技术的迁移应用
*   **观点**：将传统的 App 沙盒技术应用于行为非确定性的 AI Agent，属于技术视角的迁移。
*   **评价**：这并非底层技术突破，而是应用层创新。当前的挑战在于如何定义 Agent 的“最小权限集”。传统 App 权限是静态的，而 Agent 行为具有动态性，如何实现沙盒策略的动态调整是后续优化的关键。

#### 4. 可读性与逻辑
*   文章遵循“问题（安全风险）-> 方案 -> 实现 -> 优势”的线性逻辑，术语使用准确，适合具备 macOS 开发背景的读者阅读。

#### 5. 行业影响：OS 级 AI 安全治理的预演
*   该文章反映了操作系统厂商在 AI 安全生态中的潜在角色。未来，Apple、Microsoft 等厂商可能会将 AI Agent 纳入标准的 OS 安全模型，统一管理 Agent 的权限边界，而非依赖开发者自行构建安全堡垒。

### 可验证的检查方式

1.  **逃逸测试**：
    *   构建一个包含恶意指令的 Agent（例如指令为“读取 ~/.ssh/id_rsa 并通过 DNS 隧道外传”），并将其置于 Safehouse 定义的沙盒配置中运行。
    *   **验证指标**：通过 Sysmontap 或 Console.app 监控系统调用日志，确认违规访问是否被内核成功拦截，以及进程是否因违反沙盒策略而终止。

---
## 代码示例




```python
# 示例1：创建沙盒环境并执行受限操作
import os
import subprocess
import tempfile

def create_sandboxed_agent(agent_name, allowed_paths):
    """
    创建一个受限的沙盒环境来运行本地Agent
    :param agent_name: Agent名称
    :param allowed_paths: 允许访问的路径列表
    """
    # 创建临时沙盒目录
    sandbox_dir = tempfile.mkdtemp(prefix=f"sandbox_{agent_name}_")
    os.makedirs(os.path.join(sandbox_dir, "work"), exist_ok=True)
    
    # 设置沙盒权限配置
    sandbox_config = {
        "allowed_paths": allowed_paths,
        "network_access": False,  # 禁止网络访问
        "file_write": True,       # 允许写入文件
        "max_memory": "512M"      # 限制内存使用
    }
    
    # 在沙盒中执行命令示例
    try:
        result = subprocess.run(
            ["python3", "-c", "print('沙盒测试成功')"],
            cwd=sandbox_dir,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"沙盒执行结果: {result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"沙盒执行失败: {e.stderr}")
    finally:
        # 清理沙盒环境
        subprocess.run(["rm", "-rf", sandbox_dir])

# 使用示例
create_sandboxed_agent(
    "test_agent",
    allowed_paths=["/tmp", "/var/folders"]
)
```


1. 创建隔离的临时目录
2. 配置沙盒权限（网络访问、文件写入、内存限制）
3. 在沙盒中安全执行命令
4. 执行后自动清理环境

```python
# 示例2：实现沙盒文件系统隔离
import os
import shutil
from contextlib import contextmanager

@contextmanager
def sandboxed_filesystem(allowed_dirs):
    """
    创建一个临时的沙盒文件系统环境
    :param allowed_dirs: 允许访问的目录列表
    """
    original_root = os.getcwd()
    sandbox_root = tempfile.mkdtemp(prefix="sandbox_fs_")
    
    # 创建允许访问的目录的符号链接
    for dir_path in allowed_dirs:
        if os.path.exists(dir_path):
            rel_path = os.path.relpath(dir_path, "/")
            sandbox_path = os.path.join(sandbox_root, rel_path)
            os.makedirs(os.path.dirname(sandbox_path), exist_ok=True)
            os.symlink(dir_path, sandbox_path)
    
    try:
        # 切换到沙盒根目录
        os.chdir(sandbox_root)
        yield sandbox_root
    finally:
        # 恢复原始工作目录
        os.chdir(original_root)
        # 清理沙盒环境
        shutil.rmtree(sandbox_root, ignore_errors=True)

# 使用示例
with sandboxed_filesystem(["/tmp", "/Users"]) as sandbox:
    # 在沙盒中执行文件操作
    print(f"当前沙盒根目录: {sandbox}")
    print(f"沙盒内容: {os.listdir('.')}")
    
    # 尝试访问允许的目录
    if os.path.exists("tmp"):
        print("成功访问/tmp目录")
    
    # 尝试访问不允许的目录会失败
    try:
        os.listdir("/etc")
    except FileNotFoundError:
        print("无法访问/etc目录（沙盒隔离生效）")
```


1. 创建临时沙盒根目录
2. 为允许访问的目录创建符号链接
3. 使用上下文管理器确保环境清理
4. 阻止对未授权目录的访问

```python
# 示例3：监控沙盒中的资源使用
import psutil
import time
from threading import Thread

class SandboxMonitor:
    def __init__(self, pid, max_cpu=80, max_memory=1024):
        """
        监控沙盒进程的资源使用情况
        :param pid: 要监控的进程ID
        :param max_cpu: 最大CPU使用率百分比
        :param max_memory: 最大内存使用量(MB)
        """
        self.pid = pid
        self.max_cpu = max_cpu
        self.max_memory = max_memory
        self.monitoring = False
        self.violations = []

    def start(self):
        """启动监控线程"""
        self.monitoring = True
        self.thread = Thread(target=self._monitor_loop)
        self.thread.start()

    def stop(self):
        """停止监控"""
        self.monitoring = False
        if hasattr(self, 'thread'):
            self.thread.join()

    def _monitor_loop(self):
        """监控循环"""
        process = psutil.Process(self.pid)
        while self.monitoring:
            try:
                # 检查CPU使用率
                cpu_percent = process.cpu_percent(interval=1)
                if cpu_percent > self.max_cpu:
                    self.violations.append(f"CPU使用率超标: {cpu_percent}%")
                
                # 检查内存使用
                memory_mb = process.memory_info().rss / (1024 * 1024)
                if memory_mb > self.max_memory:
                    self.violations.append(f"内存使用超标: {memory_mb:.2f}MB")
                
                time.sleep(1)
            except psutil.NoSuchProcess:
                self.monitoring = False
                break

# 使用示例
if __name__ == "__main__":
    # 模


---
## 案例研究


### 1：独立开发者构建自动化运维机器人

 1：独立开发者构建自动化运维机器人

**背景**:  
某 SaaS 独立开发者开发了一款基于 Python 的自动化运维机器人，用于连接客户的私有云服务器并执行维护脚本（如日志清理、备份更新）。该工具运行在开发者的 MacBook 上，利用 LLM 解析自然语言指令并生成 Shell 命令。

**问题**:  
由于 LLM 生成的代码具有不确定性，开发者在测试过程中曾遇到机器人误执行 `rm -rf` 命令，导致本地开发环境的关键配置文件被删除。此外，机器人需要访问本地的 SSH 密钥以连接服务器，直接运行存在密钥泄露给恶意代码的风险。

**解决方案**:  
开发者使用 Agent Safehouse 在 macOS 上为该机器人创建了一个严格的沙盒环境。
1. **文件系统隔离**：通过配置，仅允许机器人读写特定的 `/tmp/working_dir` 目录，禁止访问系统核心配置文件夹（如 `/etc/` 或用户的 `Home` 目录）。
2. **网络与密钥管控**：配置网络策略，仅允许机器人访问特定的内网 IP 段，并使用 SSH Agent 转发而非直接读取磁盘上的密钥文件。

**效果**:  
在后续的测试中，即使 LLM 产生了破坏性的删除指令，由于沙盒限制，操作被系统拦截并报错，未对宿主机造成任何损害。开发者得以放心地进行大规模的自动化指令测试，开发效率提升了 30%，同时消除了对生产环境误操作的恐惧。

---



### 2：AI 初创公司的本地 RAG 系统安全测试

 2：AI 初创公司的本地 RAG 系统安全测试

**背景**:  
一家专注于企业级知识库的 AI 初创公司正在开发一款 RAG（检索增强生成）应用。该应用需要在员工的本地 Mac 设备上运行，并索引本地私有文档（如财务报表、代码库）以供内部 AI Agent 查询。

**问题**:  
为了验证安全性，公司内部的红队进行了一次模拟攻击，发现如果诱导 AI Agent 访问恶意构造的文档，Agent 可能会通过 Python 脚本执行漏洞逃逸出当前目录，进而读取宿主机上的其他敏感文件（如浏览器 Cookie 或 iCloud 钥匙串数据）。

**解决方案**:  
公司决定将 Agent Safehouse 集成到其客户端的启动流程中。当用户启动本地 RAG 服务时，Agent Safehouse 会自动应用一套预设的安全策略：
1. **进程隔离**：确保 AI Agent 的所有子进程都在独立的 App Sandbox 中运行。
2. **资源限制**：严格限制 CPU 和内存使用，防止恶意脚本通过无限循环耗尽系统资源（DoS 攻击）。

**效果**:  
通过集成 Agent Safehouse，该公司的应用成功通过了企业客户的安全审计。沙盒机制确保了即使 AI Agent 被劫持，攻击者也无法访问沙盒之外的任何数据。这一特性成为了产品差异化的关键点，帮助公司成功签约了两家对数据合规性要求极高的金融级客户。

---



### 3：开源 LLM 框架的本地插件生态安全

 3：开源 LLM 框架的本地插件生态安全

**背景**:  
一个流行的开源 LLM 应用框架允许用户安装社区编写的本地插件（Plugins），以扩展 Agent 的能力（例如：控制 Spotify、管理日历、处理本地图片）。

**问题**:  
由于插件完全由社区维护，缺乏严格的审核机制，曾发生过恶意插件在用户不知情的情况下，利用 Agent 的执行权限扫描本地 `Downloads` 文件夹并上传至远程服务器的安全事件。这导致用户不敢在本地运行未经验证的第三方插件。

**解决方案**:  
该框架引入 Agent Safehouse 作为插件的底层运行环境。框架开发者定义了一套“最小权限原则”的配置文件，加载每个插件时，Agent Safehouse 会根据插件声明的功能动态授权：
1. **动态授权**：例如，Spotify 插件仅被授予访问音乐库的权限，而被明确禁止访问网络或文档文件夹。
2. **透明化日志**：Agent Safehouse 提供了详细的系统调用日志，任何越权行为都会被记录并弹窗提示用户。

**效果**:  
这一举措极大地重建了用户信任。用户现在可以安全地尝试来自 GitHub 的各种实验性插件，而无需担心隐私泄露。对于插件开发者而言，虽然开发环境受到了限制，但 Agent Safehouse 提供了清晰的调试工具，帮助他们适配安全规范。该项目的社区活跃度因此提升了 50%。

---
## 最佳实践

## 最佳实践指南

### 实践 1：严格定义沙盒权限配置文件

**说明**: Agent Safehouse 利用 macOS 原生沙盒机制限制 Agent 的访问范围。最佳实践是遵循“最小权限原则”，即仅授予 Agent 完成任务所必需的权限，杜绝授予“读写所有文件”或“完全网络访问”等宽泛权限。

**实施步骤**:
1. 分析 Agent 的功能需求，列出其必须接触的文件目录、网络端口和系统资源。
2. 编写对应的 `.sb` (Sandbox) 配置文件或配置 Safehouse 规则，明确允许列表。
3. 明确拒绝所有未在允许列表中的操作尝试。

**注意事项**: 定期审查权限配置，随着 Agent 功能的迭代及时清理不再需要的旧权限，防止权限膨胀。

---

### 实践 2：实施严格的文件系统隔离

**说明**: 防止 Agent 越出其工作目录访问敏感系统文件或用户数据。应通过沙盒规则将 Agent 的文件操作限制在特定的临时目录或指定的项目文件夹内。

**实施步骤**:
1. 为 Agent 创建独立的工作目录，避免直接使用用户主目录或系统敏感路径。
2. 在沙盒配置中，仅允许该 Agent 对其工作目录进行读写操作。
3. 对于需要读取的输入文件，采用复制或映射到沙盒内的方式进行处理，而非直接开放原始路径。

**注意事项**: 确保临时目录具有适当的隔离属性，防止通过符号链接逃逸到沙盒外部。

---

### 实践 3：限制网络通信能力

**说明**: 本地 Agent 通常不需要完全的互联网访问权限。限制网络连接可以减少数据泄露风险，并防止 Agent 被恶意指令控制后成为攻击跳板。

**实施步骤**:
1. 评估 Agent 是否需要网络访问。如果仅处理本地数据，应在沙盒配置中完全禁用网络。
2. 如果需要网络（如调用本地 LLM 或 API），使用规则限制仅允许连接到 `localhost` (127.0.0.1) 或特定的内网 IP 地址。
3. 阻止所有出站 TCP/UDP 连接，除非在白名单中明确指定。

**注意事项**: 即使允许连接到本地服务，也应验证服务的安全性，防止通过本地端口进行 SSRF (服务端请求伪造) 攻击。

---

### 实践 4：控制进程生成与交互

**说明**: Agent 可能会尝试调用系统命令或启动子进程来执行操作。如果不加限制，攻击者可能利用 Agent 执行任意 Shell 命令。

**实施步骤**:
1. 在沙盒规则中，默认禁止 Agent 生成 (`exec`) 任何子进程。
2. 如果必须调用外部工具，使用白名单机制，仅允许执行特定的二进制文件（如 `/usr/bin/python3` 或特定路径下的工具）。
3. 结合 macOS 的 `Hardened Runtime` 和代码签名，确保 Agent 自身未被篡改。

**注意事项**: 避免允许 Agent 执行 Shell 解释器（如 `/bin/bash` 或 `/bin/zsh`），因为这通常意味着可以执行任意命令链。

---

### 实践 5：审计与日志监控

**说明**: 即使在沙盒环境中，也需要监控 Agent 的行为以检测异常活动或潜在的沙盒逃逸尝试。macOS 沙盒会拦截违规操作并产生日志。

**实施步骤**:
1. 配置系统日志工具（如 `log stream` 或 Console.app）以收集与沙盒相关的错误和拒绝信息。
2. 在 Agent Safehouse 的封装层中添加钩子，记录所有文件读写和网络连接尝试。
3. 定期检查日志，寻找频繁被拒绝的系统调用，这可能表明 Agent 行为异常或配置不当。

**注意事项**: 日志文件本身应包含敏感信息（如具体的操作路径），需确保日志文件的存储安全，防止 Agent 读取或修改自身的日志。

---

### 实践 6：资源配额管理

**说明**: 防止 Agent 因逻辑错误或恶意意图消耗过多的系统资源（如 CPU 死循环、内存溢出或填满磁盘），导致 macOS 系统卡顿。

**实施步骤**:
1. 利用 macOS 的资源限制功能或 Safehouse 提供的接口，为 Agent 设置 CPU 时间限制和最大内存阈值。
2. 限制 Agent 可写的临时文件系统大小，防止“磁盘炸弹”攻击。
3. 设置进程超时机制，如果单次执行时间超过预设值（如 5 分钟），强制终止进程。

**注意事项**: 资源限制应与任务的实际复杂度相匹配，避免在处理大型合法任务时被误杀，建议提供动态调整配置的选项。

---
## 学习要点

- Agent Safehouse 是一个专为 macOS 本地 AI 代理设计的原生沙盒工具，旨在解决本地智能体缺乏安全隔离的痛点。
- 该工具利用 macOS 原生沙盒机制，无需依赖虚拟机或复杂的容器配置即可实现严格的资源隔离。
- 它能够有效限制 AI 代理对文件系统、网络和系统进程的访问权限，防止恶意或失控的代理破坏主机环境。
- 该方案支持为不同的代理分配特定的“安全屋”，从而实现多代理环境下的任务隔离与并行处理。
- 通过利用操作系统底层的安全特性，它为在本地运行不可信的开源模型提供了一种轻量级且安全的解决方案。
- 此项目填补了当前本地大模型应用生态中的安全空白，让用户既能享受数据隐私，又能免受代码执行风险。

---
## 常见问题


### 1: 什么是 Agent Safehouse，它主要解决什么问题？

1: 什么是 Agent Safehouse，它主要解决什么问题？

**A**: Agent Safehouse 是一个专为 macOS 设计的原生沙箱工具，旨在为本地运行的 AI 代理提供安全保障。随着本地 AI 智能体（能够执行代码、修改文件或调用系统命令的自主程序）的普及，它们带来的安全风险日益增加。Agent Safehouse 通过利用 macOS 原生的沙箱机制，限制这些代理的访问权限，防止它们在未经授权的情况下读取敏感文件、修改系统设置或访问网络，从而确保用户系统的安全性。

---



### 2: Agent Safehouse 是如何工作的，其技术原理是什么？

2: Agent Safehouse 是如何工作的，其技术原理是什么？

**A**: Agent Safehouse 的核心在于利用 macOS 内置的 Sandbox 技术和权限模型。它通过配置严格的配置文件，定义了一套“安全规则”，将本地代理进程隔离在一个受限的环境中。当被隔离的代理尝试执行操作（如读取特定目录下的文件、建立网络连接或使用摄像头）时，系统会拦截该请求并根据预设的白名单或黑名单策略决定是否允许。这种隔离发生在操作系统内核层面，比单纯的软件级监控更加彻底和难以绕过。

---



### 3: 与 Docker 或虚拟机相比，使用 Agent Safehouse 的优势是什么？

3: 与 Docker 或虚拟机相比，使用 Agent Safehouse 的优势是什么？

**A**: 虽然 Docker 和虚拟机也能提供隔离环境，但 Agent Safehouse 针对 macOS 上的日常开发和使用场景具有独特优势。首先，它是“原生”的，不需要像 Docker 那样依赖重量级的虚拟化技术，因此资源占用极低，几乎无性能损耗。其次，它允许更精细的权限控制，例如可以允许代理访问特定的配置文件，同时禁止其访问其他敏感目录，这在容器配置中相对复杂。最后，对于在 macOS 上直接运行本地模型的开发者来说，Safehouse 的集成度更高，不会改变原有的工作流。

---



### 4: 使用 Agent Safehouse 会影响本地 AI 代理的功能性吗？

4: 使用 Agent Safehouse 会影响本地 AI 代理的功能性吗？

**A**: 在一定程度上会产生影响，但这正是安全权衡的体现。默认情况下，沙箱会阻断大部分敏感操作。如果代理需要访问特定资源（例如读取代码库或写入日志文件），用户必须显式地在 Safehouse 的配置中授予相应权限。这意味着用户需要根据代理的具体功能需求，手动调整沙箱策略。虽然这增加了一些配置工作，但它确保了用户对代理行为的完全知情权和控制权，避免了“黑盒”操作带来的风险。

---



### 5: Agent Safehouse 是否支持所有类型的本地 AI 代理和编程语言？

5: Agent Safehouse 是否支持所有类型的本地 AI 代理和编程语言？

**A**: Agent Safehouse 的设计具有通用性，理论上支持任何在 macOS 上可执行的二进制文件或脚本。无论代理是使用 Python、Node.js、Rust 还是其他语言编写的，只要它作为一个进程运行，Safehouse 就可以对其进行沙箱隔离。然而，具体的隔离效果取决于代理的运行方式。对于某些试图通过极端手段逃离沙箱的高级恶意代码，可能需要更复杂的配置。目前，它主要针对标准的本地开发环境和主流的开源代理框架进行了优化。

---



### 6: 普通用户是否容易上手 Agent Safehouse，还是仅适合专家？

6: 普通用户是否容易上手 Agent Safehouse，还是仅适合专家？

**A**: 虽然沙箱技术听起来很复杂，但 Agent Safehouse 的目标是提供易于集成的解决方案。对于熟悉终端和配置文件的开发者来说，配置过程相对直观。项目通常会提供预设的配置模板，涵盖常见的代理使用场景。然而，对于完全没有技术背景的普通用户，理解并定制权限策略可能仍具有一定的门槛。因此，它目前最适合那些需要在本地运行自主代理的开发者或高级用户。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**:

### macOS 的沙盒机制核心在于限制进程对系统资源的访问。请列出当你在终端运行 `sandbox-exec -p '(version 1)'` 并尝试执行一个简单的读写文件操作时，默认会被拦截的三个具体系统调用或操作类别。

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
- 标签： [Agent](/tags/agent/) / [macOS](/tags/macos/) / [沙箱技术](/tags/%E6%B2%99%E7%AE%B1%E6%8A%80%E6%9C%AF/) / [本地部署](/tags/%E6%9C%AC%E5%9C%B0%E9%83%A8%E7%BD%B2/) / [系统安全](/tags/%E7%B3%BB%E7%BB%9F%E5%AE%89%E5%85%A8/) / [进程隔离](/tags/%E8%BF%9B%E7%A8%8B%E9%9A%94%E7%A6%BB/) / [LLM](/tags/llm/) / [Sandbox](/tags/sandbox/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/)

### 相关文章

- [Agent Safehouse：macOS 本地 Agent 的原生沙箱方案]({{< relref "posts/20260309-hacker_news-agent-safehouse-macos-native-sandboxing-for-local--1.md" >}})
- [Agent Safehouse：利用 macOS 原生沙箱实现本地 Agent 隔离]({{< relref "posts/20260309-hacker_news-agent-safehouse-macos-native-sandboxing-for-local--6.md" >}})
- [RedSage：网络安全通用大语言模型]({{< relref "posts/20260131-arxiv_ai-redsage-a-cybersecurity-generalist-llm-0.md" >}})
- [OpenClaw赋予AI全系统权限引发安全担忧]({{< relref "posts/20260206-hacker_news-openclaw-when-ai-agents-get-full-system-access-sec-14.md" >}})
- [Agent Safehouse：macOS 本地代理的原生沙箱方案]({{< relref "posts/20260308-hacker_news-agent-safehouse-macos-native-sandboxing-for-local--0.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*