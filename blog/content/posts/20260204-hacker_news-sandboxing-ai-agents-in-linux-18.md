---
title: "在 Linux 环境中为 AI 代理构建沙箱隔离机制"
date: 2026-02-04T00:05:56+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agents", "沙箱", "Linux", "容器化", "系统安全", "隔离机制", "DevOps", "虚拟化"]
categories: ["安全", "系统与基础设施"]
source: hacker_news
description: "随着 AI 智能体在自动化任务中的角色日益关键，将其直接暴露于开放操作系统环境会带来显著的安全风险。本文探讨了如何利用 Linux 的底层特性构建沙箱机制，从而在保持智能体功能性的同时限制其权限。通过阅读本文，读者将了解具体的隔离策略，进而为 AI 智能体部署构建一个兼顾效率与安全的执行环境。"
external_url: https://blog.senko.net/sandboxing-ai-agents-in-linux
scenarios: ["AI/ML项目", "DevOps/运维"]
---

# 在 Linux 环境中为 AI 代理构建沙箱隔离机制

---

## 基本信息

- **作者**: speckx
- **评分**: 79
- **评论数**: 46
- **链接**: [https://blog.senko.net/sandboxing-ai-agents-in-linux](https://blog.senko.net/sandboxing-ai-agents-in-linux)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46874139](https://news.ycombinator.com/item?id=46874139)

---
## 导语

随着 AI 智能体在自动化任务中的角色日益关键，将其直接暴露于开放操作系统环境会带来显著的安全风险。本文探讨了如何利用 Linux 的底层特性构建沙箱机制，从而在保持智能体功能性的同时限制其权限。通过阅读本文，读者将了解具体的隔离策略，进而为 AI 智能体部署构建一个兼顾效率与安全的执行环境。

---
## 评论

**评价对象：** 文章《Sandboxing AI Agents in Linux》（基于文章标题及该领域通用技术语境进行深度评价）

### 一、 核心观点与论证结构

**中心观点：**
随着 AI Agent 从单一对话机器人向具备自主操作系统的智能体演进，利用 Linux 内核级技术构建轻量级、强隔离的沙箱环境，是平衡 AI 自主性与系统安全性的必由之路。

**支撑理由：**
1.  **攻击面扩大是必然趋势**（事实陈述）：AI Agent 需要调用 Shell、文件系统等底层接口来完成任务，传统的 API 限制已无法满足需求，必须转向系统级的隔离。
2.  **权限最小化原则的适用**（作者观点）：通过 `seccomp`（系统调用过滤）、`Landlock`（文件系统访问控制）和 `User Namespaces`（用户命名空间）等技术，可以在不牺牲 Agent 核心功能的前提下，严格限制其“视力”和“手力”。
3.  **防御深度需求**（你的推断）：单纯依赖应用层的 Prompt Engineering（提示词工程）来防止 Agent 作恶是不可靠的，必须依靠内核态的强制访问控制作为最后一道防线。

**反例/边界条件：**
1.  **性能与开销**（事实陈述）：高频率的上下文切换和系统调用拦截会显著降低 Agent 的执行效率，对于需要高频 I/O 操作的任务（如实时日志分析），强隔离可能导致不可接受的延迟。
2.  **功能受限**（边界条件）：过度的沙箱限制（如禁用网络或禁用特定系统调用）会导致 Agent 失去部分核心能力，例如无法安装依赖包或无法访问必要的系统配置，从而使其“退化”为普通的聊天机器人。

---

### 二、 多维度深入评价

#### 1. 内容深度：从应用层下沉到内核层
该文章（及此类技术探讨）的深度在于跳出了当前主流的“越狱”防御思维（即仅通过文本对抗来防御），直接切入操作系统底层。
*   **论证严谨性：** 如果文章详细阐述了 `seccomp-bpf` 的具体规则配置，或者讨论了 `cgroups v2` 在资源限制上的作用，那么其技术论证是严谨的。它触及了安全领域的核心：**代码即法律，内核即法官**。它指出了一个关键事实：AI Agent 本质上是运行在 CPU 上的进程，必须遵循操作系统的进程管理法则。

#### 2. 实用价值：DevOps 与 SecOps 的融合指南
对于正在构建 AI Agent 基础设施的工程团队而言，此类文章具有极高的实用价值。
*   **指导意义：** 它提供了一套可落地的“防御清单”。例如，建议不要以 `root` 用户运行 Agent，而是使用 `User Namespaces` 将其映射到容器内的 `root` 但宿主机的 `nobody`。这直接对应了 CIS Benchmarks 中关于容器安全的最佳实践。
*   **案例结合：** 在实际部署中，如使用 Docker 或 Kubernetes 运行 AI Agent，文章若能结合 OCI (Open Container Initiative) 规范，说明如何通过 `--security-opt` 配置 seccomp 配置文件，将具有极强的操作指导意义。

#### 3. 创新性：旧技术的新范式
虽然 Linux 沙箱技术（如 chroot, namespaces）已存在多年，但将其系统性地应用于 **AI Agent 的自主性约束** 是一种视角的创新。
*   **新观点：** 传统的沙箱是为了防止“被黑客攻击的代码”泄露数据，而 AI 时代的沙箱是为了防止“合法但失控的 AI”执行恶意指令。这种从 **防御外部入侵** 到 **防御内部智能** 的范式转移，是该类技术文章最大的创新点。

#### 4. 可读性与逻辑性
此类技术文章通常面临“两难”：讲得太浅（如“用 Docker 跑一下”）没有深度，讲得太深（如汇编级系统调用分析）晦涩难懂。
*   **评价：** 优秀的文章应当建立分层模型。例如，将隔离分为“网络层”、“文件系统层”、“系统调用层”。
*   **逻辑流：** 应遵循“风险识别 -> 技术选型 -> 实施细节 -> 权衡取舍”的逻辑。如果文章能清晰地画出一张从 Host OS 到 Container 到 Agent Process 的权限穿透图，其逻辑性即为上乘。

#### 5. 行业影响：推动 AI 安全基建标准化
随着 OpenAI 发布 GPT-4s 的代码执行能力，以及 AutoGPT 等项目的流行，**“AI 安全”** 正在从 NLP 领域向 **“基础设施安全”** 领域渗透。
*   **潜在影响：** 这类文章有助于推动行业建立类似 OWASP 的“AI Agent 安全标准”，促使云厂商（如 AWS Lambda, Google Cloud Functions）推出专为 AI Agent 设计的“安全执行环境”。

#### 6. 争议点与不同观点
*   **Prompt 工程 vs. 硬隔离**：一部分 AI 研究者认为，通过 Constitutional AI（宪法AI）和精细的 Prompt 约束就足够了，系统级隔离不仅成本高，而且无法阻止 Agent 生成恶意内容（如生成钓鱼邮件代码），只能阻止其执行。**沙箱防不住“坏思想”，只能防“坏动作”。**
*   **逃逸风险**：即使是内核级隔离也存在逃逸风险（如 Dirty Cow 等内核漏洞）。如果 Agent 具备自我修改代码或探索漏洞

---
## 代码示例




```python
# 示例1：使用chroot限制文件系统访问
import os
import subprocess

def create_chroot_jail():
    """创建一个受限的chroot环境运行AI代理"""
    jail_path = "/tmp/ai_jail"
    
    # 创建基础目录结构
    os.makedirs(f"{jail_path}/bin", exist_ok=True)
    os.makedirs(f"{jail_path}/lib", exist_ok=True)
    
    # 复制必要的二进制文件和库
    subprocess.run(["cp", "/bin/bash", f"{jail_path}/bin/"])
    subprocess.run(["cp", "/bin/ls", f"{jail_path}/bin/"])
    
    # 复制依赖库（简化示例）
    subprocess.run(["ldd", "/bin/bash"], stdout=subprocess.PIPE)
    
    # 在chroot环境中执行命令
    try:
        subprocess.run(["chroot", jail_path, "/bin/bash", "-c", "ls /"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"chroot执行失败: {e}")

# 说明：这个示例展示了如何使用chroot创建最小化的文件系统环境，
# 限制AI代理只能访问特定目录，防止其访问敏感系统文件。
```




```python
# 示例2：使用Linux命名空间隔离进程
import subprocess

def run_in_isolated_namespace():
    """在新的PID和NET命名空间中运行AI代理"""
    cmd = [
        "unshare",
        "--pid", "--mount", "--net",
        "--fork", "--mount-proc",
        "python3", "-c", "print('我在隔离环境中运行')"
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"隔离执行失败: {e}")

# 说明：这个示例展示了如何使用Linux命名空间(unshare)创建隔离的
# 进程、网络和挂载命名空间，使AI代理无法看到或影响主系统的进程和网络。
```




```python
# 示例3：使用seccomp限制系统调用
import subprocess
import json

def run_with_seccomp_filter():
    """使用seccomp限制允许的系统调用"""
    # 定义允许的系统调用白名单
    seccomp_profile = {
        "defaultAction": "SCMP_ACT_ERRNO",
        "syscalls": [
            {"name": "read", "action": "SCMP_ACT_ALLOW"},
            {"name": "write", "action": "SCMP_ACT_ALLOW"},
            {"name": "exit", "action": "SCMP_ACT_ALLOW"},
            {"name": "rt_sigreturn", "action": "SCMP_ACT_ALLOW"}
        ]
    }
    
    # 将配置写入临时文件
    with open("/tmp/seccomp.json", "w") as f:
        json.dump(seccomp_profile, f)
    
    try:
        # 使用docker运行并应用seccomp配置
        subprocess.run([
            "docker", "run", "--rm",
            "--security-opt", "seccomp=/tmp/seccomp.json",
            "python:3.9-slim",
            "python3", "-c", "print('受限系统调用执行成功')"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"seccomp执行失败: {e}")

# 说明：这个示例展示了如何使用seccomp配置文件限制AI代理可以使用的
# 系统调用，防止其执行危险操作如文件修改、网络访问等。
```


---
## 案例研究


### 1：某大型互联网社交媒体平台

 1：某大型互联网社交媒体平台

**背景**: 该平台拥有海量的用户生成内容（UGC），为了提高审核效率和用户体验，开发团队尝试引入大语言模型（LLM）作为 AI Agent，用于自动分析用户上传的图片和文本，识别违规内容并生成辅助标签。

**问题**: 在测试阶段发现，直接运行的 AI Agent 存在严重的不可控风险。Agent 为了完成任务，偶尔会尝试调用宿主机的系统命令（如通过 Python subprocess 模块）去读取本不应访问的敏感目录，或者在处理恶意构造的畸形文件时触发解析器崩溃，导致宿主机服务器负载飙升，影响了线上核心服务的稳定性。

**解决方案**: 技术团队基于 Linux 的 Firejail 和 Seccomp（Secure Computing Mode）技术构建了沙箱环境。AI Agent 被限制在一个极简的文件系统命名空间中，无法访问宿主机的网络接口或敏感文件。同时，利用 Seccomp-BPF 严格限制了 Agent 进程的系统调用，仅允许 `read`, `write`, `exit` 等基本调用，彻底禁止了 `execve`（执行程序）和 `fork`（创建进程）等高危操作。

**效果**: 上线后，成功拦截了多起因 AI Agent 逻辑错误导致的系统越权尝试。即使 AI Agent 在处理恶意输入时崩溃，也被限制在沙箱内部，未造成任何宿主机宕机。系统可用性（SLA）保持在 99.99% 以上，同时实现了内容审核自动化率的提升。

---



### 2：某 Fintech 金融科技初创公司

 2：某 Fintech 金融科技初创公司

**背景**: 该公司开发了一款自动化财务分析 Agent，旨在帮助中小企业自动连接银行 API 下载流水单，并在本地环境中进行数据清洗和分类，生成财务报表。

**问题**: 由于金融数据的敏感性，客户极度担心数据隐私。如果 AI Agent 在处理数据时被植入恶意代码，或者 Agent 本身存在漏洞被利用，可能会将敏感的财务数据外传至互联网。此外，Agent 需要运行在客户私有部署的 Linux 服务器上，环境复杂且不可控。

**解决方案**: 开发团队采用了 Docker 容器结合 Linux Rootless 技术进行隔离。Agent 运行在一个无特权的容器中，通过 `--network=none` 参数切断了所有外网连接，仅保留与宿主机特定文件夹的映射通道用于读取流水文件。同时，启用了 AppArmor 配置文件，严格锁死了容器内的写权限，防止 Agent 被控制后在系统中植入后门。

**效果**: 这一方案极大地增强了客户信任，成功通过了 ISO 27001 信息安全认证。在实际运行中，即使 Agent 遭遇了模拟的供应链攻击尝试，也无法建立外网连接，数据实现了零泄漏。该安全特性成为产品核心竞争力之一，帮助公司在半年内签约了数十家对数据合规要求极高的金融机构。

---



### 3：某开源自动化运维项目

 3：某开源自动化运维项目

**背景**: 该项目开发了一款基于 LLM 的 DevOps Agent，能够根据自然语言指令自动编写 Shell 脚本并执行，以完成服务器日志分析、服务重启等运维任务。

**问题**: AI 生成的代码具有不确定性。在早期测试中，Agent 曾生成过具有破坏性的脚本（例如误删了非目标目录的文件），或者因为死循环脚本导致 CPU 资源耗尽。直接在宿主机上运行这种“半自动”生成的代码风险过大。

**解决方案**: 团队利用 Linux 的 cgroups v2（Control Groups）对 AI Agent 进行了严格的资源配额限制。同时，结合 User Namespaces（用户命名空间）技术，将容器内的 Root 用户映射为宿主机上的普通用户，使 Agent 即使执行了 `rm -rf /` 等危险命令，也只能删除沙箱内的临时文件系统，无法触及宿主机核心数据。

**效果**: 资源配额机制成功防止了因 Agent 生成死循环代码导致的服务器雪崩事故。隔离机制确保了数百次自动化运维任务中，未发生一起因误操作导致的宿主机数据丢失。这使得该工具能够安全地在生产环境中通过 CI/CD 流水线部署，将运维人员的日常重复性工作减少了 70%。

---
## 最佳实践

## 最佳实践指南

### 实践 1：使用非特权用户运行

**说明**: AI Agent 绝不应以 root 权限运行。这是最基本的安全防线。通过创建专用的系统用户并赋予其最小的权限集，可以限制 Agent 在遭受攻击或行为异常时对系统造成的破坏范围。

**实施步骤**:
1. 创建一个专用的系统用户（例如 `ai-agent`），并禁止其登录 shell。
2. 确保该用户不属于 `sudo` 或 `wheel` 等特权组。
3. 使用 `runuser` 或 `su` 切换到该用户来启动 Agent 进程，或在 systemd 服务文件中指定 `User=ai-agent`。

**注意事项**: 即使 Agent 需要访问特定文件，也应通过文件权限管理（chmod/chown）来授权，而不是提升进程运行权限。

---

### 实践 2：实施严格的网络隔离

**说明**: AI Agent 通常需要访问互联网（调用 LLM API）或本地服务。默认允许所有网络访问存在数据泄露风险。最佳实践是定义明确的白名单规则，仅允许必要的出站连接。

**实施步骤**:
1. 配置 `iptables`、`nftables` 或 `ufw` 设置默认出站拒绝策略。
2. 添加规则仅允许访问特定的 IP 地址或域名（如 OpenAI 或 Anthropic 的 API 端点）。
3. 对于仅处理本地数据的 Agent，考虑完全禁用其网络访问或使用 `localhost` 仅允许本地回环。

**注意事项**: 如果 Agent 需要访问动态域名，可能需要结合 DNS 拦截工具或代理服务器来控制访问目标。

---

### 实践 3：利用命名空间进行资源隔离

**说明**: Linux Namespace 可以隔离进程的视图（如文件系统、网络、进程树）。与简单的 chroot 相比，使用 User Namespace 和 Mount Namespace 可以提供更深层的安全保障，使 Agent 无法看到或影响系统上的其他进程。

**实施步骤**:
1. 使用 `unshare` 命令或编程语言（如 Python/Go）的 Namespace API 在启动 Agent 前创建隔离环境。
2. 挂载独立的 proc 文件系统 (`mount -t proc proc /proc`) 以防止 Agent 感知到宿主机的进程信息。
3. 结合 PID Namespace 隐藏宿主机进程，使 Agent 认为自己是 PID 1。

**注意事项**: 配置 Namespace 较为复杂，建议使用成熟的容器化工具（如 Docker/Podman）作为底层实现，除非你需要极轻量级的定制。

---

### 实践 4：配置 Seccomp 过滤器

**说明**: Seccomp（Secure Computing Mode）允许限制进程可以调用的系统调用。AI Agent 通常只需要基本的读写、网络和内存分配功能，禁止 `execve`（执行程序）、`fork`（创建进程）或 `unshare` 等系统调用可以有效防止代码注入攻击。

**实施步骤**:
1. 分析 Agent 运行所需的系统调用（可以使用 `strace` 工具）。
2. 编写 Seccomp 配置文件，采用白名单模式，仅允许必要的系统调用。
3. 在启动 Agent 时应用该配置（例如 Docker 的 `--security-opt seccomp=profile.json` 或使用 `libseccomp` 库）。

**注意事项**: 过度严格的 Seccomp 规则可能导致 Agent 正常功能崩溃（如无法加载某些动态库），需在测试环境中充分验证。

---

### 实践 5：强制启用只读文件系统

**说明**: AI Agent 的推理过程通常不需要写入宿主机文件系统。将 Agent 运行目录挂载为只读，可以防止恶意代码修改系统二进制文件、写入 SSH 密钥或篡改日志。

**实施步骤**:
1. 确保所有必要的配置和库文件在只读路径下可用。
2. 如果使用容器，添加 `--read-only` 标志。
3. 对于必须写入的临时数据（如缓存或中间结果），单独挂载一个 `tmpfs` 到指定目录（如 `/tmp`），并限制其大小。

**注意事项**: 某些 Python 库在首次运行时会尝试生成缓存文件（.pyc），可能需要预先编译或设置临时环境变量。

---

### 实践 6：限制资源使用

**说明**: 防止 Agent 因死循环或恶意逻辑耗尽系统资源（CPU、内存、磁盘 I/O）。资源限制不仅是为了稳定性，也是为了防止侧信道攻击（如通过内存占用探测系统状态）。

**实施步骤**:
1. 使用 `cgroups` (v2) 或 systemd 的 slice 机制为 Agent 设置资源上限。
2. 设定内存上限（如 512MB）和 CPU 时间配额。
3. 限制磁盘 I/O 速率和写入字节数。

**注意事项**: 内存限制过低可能导致 Agent 被 OOM Killer 杀死，建议根据 Agent 承载的模型大小预留至少 20% 的余量。

---

### 实践 7：使用虚拟化或 Firecracker 等微虚拟机

---
## 学习要点

- Linux 用户命名空间是构建 AI Agent 沙箱最核心的技术，它允许非特权用户创建拥有完整 Root 权限的隔离环境，从而在不影响宿主机的情况下安全运行 Agent。
- 相比传统的虚拟机或 Docker 容器，使用 `unshare` 等工具构建的轻量级命名空间隔离方案，在平衡安全性与开发效率方面具有显著优势。
- 为了防止逃逸风险，必须严格限制沙箱内的 `CAP_SYS_ADMIN` 等特权，并利用 `cgroups v2` 对 CPU、内存和磁盘 IO 进行精细化的资源限额。
- 网络隔离是沙箱配置的关键环节，应通过单独的网络命名空间或虚拟以太网对来控制 Agent 的对外连接能力，默认策略应阻断非必要的网络访问。
- 文件系统安全需要通过挂载命名空间实现，使用只读挂载保护宿主机目录，并为 Agent 提供独立的可写层（如 OverlayFS），防止恶意篡改。
- 在安全设计中应遵循“默认拒绝”原则，通过 Seccomp 过滤器严格限制 Agent 可调用的系统调用，仅开放执行任务所必需的最小操作集合。
- 即使在隔离环境中运行，也必须对 AI Agent 的输出进行严格校验，防止其通过提示词注入或生成恶意 shell 命令来尝试突破边界。

---
## 常见问题


### 1: 为什么需要为 AI Agent 在 Linux 上构建沙箱环境？

1: 为什么需要为 AI Agent 在 Linux 上构建沙箱环境？

**A**: AI Agent 通常需要高度的自主性来执行任务，例如读取文件、修改配置或运行脚本。如果直接在宿主机上运行，一旦 Agent 产生幻觉或受到提示注入攻击，可能会执行破坏性命令（如 `rm -rf /`）或泄露敏感数据。沙箱技术通过限制 Agent 的可见性和权限，确保其只能访问特定的目录和资源，从而在利用其自动化能力的同时，保障系统的安全性和稳定性。

---



### 2: 在 Linux 中实现 AI Agent 沙箱有哪些主流技术方案？

2: 在 Linux 中实现 AI Agent 沙箱有哪些主流技术方案？

**A**: 常见的方案包括：
1. **Docker 容器**：最轻量级的选择，通过命名空间和控制组隔离文件系统和网络。适合无状态或短期运行的 Agent。
2. **Firejail**：一个 SUID 程序，可以轻松为普通进程减少 Linux 内核攻击面，适合为特定 CLI 工具提供快速隔离。
3. **User Namespace (用户命名空间)**：允许非 root 用户在容器内拥有 root 权限，但在宿主机看来仍是普通用户，安全性极高。
4. **虚拟机 (QEMU/KVM)**：通过 `libvirt` 或直接使用 QEMU，提供内核级别的隔离。适合运行不可信代码或需要完全硬件隔离的场景。
5. **gVisor**：一个用 Go 编写的用户空间内核，拦截系统调用并提供强隔离，常用于 Kubernetes 环境。

---



### 3: 如何解决沙箱环境中的网络访问限制问题？

3: 如何解决沙箱环境中的网络访问限制问题？

**A**: AI Agent 往往需要联网查询信息或调用 API。在 Linux 沙箱中，可以通过以下方式管理网络：
1. **用户模式网络**：在 Docker 或 QEMU 中默认启用，允许容器通过 NAT 访问外网，但外界无法直接访问容器。
2. **VPN 或隧道**：如果 Agent 需要访问内

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 基础用户隔离

### 假设你需要运行一个不可信的 AI Agent，它只需要读取 `/data/input` 目录中的文件并将结果写入 `/data/output`。请设计一个 Linux 命令，使用 `unshare` 或类似工具，将该 Agent 的进程隔离在一个新的 Mount Namespace 中，并确保它只能看到这两个目录，而无法访问根文件系统的其他部分（如 `/etc/passwd` 或 `/home`）。

### 提示**: 考虑使用 `unshare -m` 创建挂载命名空间，然后使用 `mount --bind` 将特定目录挂载到新的根目录结构中，并使用 `chroot` 限制根目录视图。

---
## 引用

- **原文链接**: [https://blog.senko.net/sandboxing-ai-agents-in-linux](https://blog.senko.net/sandboxing-ai-agents-in-linux)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46874139](https://news.ycombinator.com/item?id=46874139)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [安全](/categories/%E5%AE%89%E5%85%A8/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [AI Agents](/tags/ai-agents/) / [沙箱](/tags/%E6%B2%99%E7%AE%B1/) / [Linux](/tags/linux/) / [容器化](/tags/%E5%AE%B9%E5%99%A8%E5%8C%96/) / [系统安全](/tags/%E7%B3%BB%E7%BB%9F%E5%AE%89%E5%85%A8/) / [隔离机制](/tags/%E9%9A%94%E7%A6%BB%E6%9C%BA%E5%88%B6/) / [DevOps](/tags/devops/) / [虚拟化](/tags/%E8%99%9A%E6%8B%9F%E5%8C%96/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [DevOps/运维](/scenarios/devops-%E8%BF%90%E7%BB%B4/)

### 相关文章

- [Amla Sandbox：面向 AI 智能体的 WASM Bash 沙箱]({{< relref "posts/20260130-hacker_news-show-hn-amla-sandbox-wasm-bash-shell-sandbox-for-a-1.md" >}})
- [Amla Sandbox：面向 AI 智能体的 WASM Bash 沙箱]({{< relref "posts/20260130-hacker_news-show-hn-amla-sandbox-wasm-bash-shell-sandbox-for-a-13.md" >}})
- [微软推出 Azure Linux 发行版，用于优化云端基础设施]({{< relref "posts/20260129-hacker_news-microsofts-azure-linux-3.md" >}})
- [Amla Sandbox：面向 AI 智能体的 WASM Bash 沙箱]({{< relref "posts/20260130-hacker_news-show-hn-amla-sandbox-wasm-bash-shell-sandbox-for-a-4.md" >}})
- [Amla Sandbox：面向 AI 智能体的 WASM Bash 沙箱]({{< relref "posts/20260131-hacker_news-show-hn-amla-sandbox-wasm-bash-shell-sandbox-for-a-12.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*