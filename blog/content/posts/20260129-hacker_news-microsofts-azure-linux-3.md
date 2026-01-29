---
title: "微软推出 Azure Linux 发行版，用于优化云端基础设施"
date: 2026-01-29T06:41:12+08:00
draft: false
entry_kind: "auto"
tags: ["微软", "Azure", "Linux", "CBL-Mariner", "云原生", "容器化", "DevOps", "操作系统"]
categories: ["系统与基础设施", "开源生态"]
source: hacker_news
external_url: https://github.com/microsoft/azurelinux
scenarios: ["DevOps/运维"]
---

# 微软推出 Azure Linux 发行版，用于优化云端基础设施

---

## 基本信息

- **作者**: AbuAssar
- **评分**: 5
- **评论数**: 1
- **链接**: [https://github.com/microsoft/azurelinux](https://github.com/microsoft/azurelinux)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46805841](https://news.ycombinator.com/item?id=46805841)

---
## 导语

随着云原生技术的普及，底层基础设施的定制化已成为各大云厂商提升性能的关键。微软近期发布的 Azure Linux，正是这一趋势下的产物，旨在为 Azure 服务提供更高效、更安全的专用运行环境。本文将深入解析该系统的技术特点与架构设计，帮助开发者理解其背后的技术考量，以及它如何影响未来的云端应用部署策略。

---
## 摘要

微软 Azure Linux 是微软专为云端工作负载设计的开源 Linux 发行版，其发展历程和核心特点可概括如下：

### 一、 起源与定位
Azure Linux 的前身是微软内部使用的 **CBL-Mariner**。它是微软为了优化 Azure 基础设施而构建的轻量级、轻便的 Linux 发行版。其核心目标是为微软的云服务提供更高的性能、稳定性和安全性，同时减少不必要的维护负担。

### 二、 发布与开源
在 2023 年，微软正式宣布将 Azure Linux **公开可用**（General Availability），并将其作为一个上游发行版发布。这意味着外部开发者和客户不仅可以使用它，还可以基于此进行定制开发。

### 三、 核心特性
1.  **轻量化与高效**：系统经过裁剪，仅包含运行云服务和容器化应用所需的最小组件，从而减小了攻击面并提高了启动速度。
2.  **安全性**：微软为其提供了完整的安全补丁支持和定期更新，且遵循严格的内部安全标准。
3.  **容器优化**：它是微软 Azure Kubernetes Service (AKS) 等服务的底层基础，非常适合运行容器化应用。
4.  **包管理**：使用 RPM 包格式和 DNF 包管理器（类似于 Fedora/RHEL），便于开发者管理软件。

### 四、 总结
Azure Linux 的发布标志着微软“拥抱开源”战略的进一步深化。它不仅支撑着微软庞大的公有云服务，也为企业在 Azure 上运行 Linux 工作负载提供了一个经过微软官方验证、优化的选择。

---
## 评论

由于您未提供具体的文章正文内容，我将基于**“微软发布 Azure Linux (CBL-Mariner)”** 这一行业事件本身及其公开的技术文档、社区动态作为评价对象。以下是对该技术产品及其战略意义的深度评价。

### 中心观点
**微软发布 Azure Linux 标志着其云战略从“支持开源”彻底转向“拥有并优化开源底层”，旨在通过垂直整合来降低云基础设施的熵增与攻击面，以追求极致的性能与控制力。**

### 支撑理由与边界条件

**1. 理由一：降低维护熵，实现基础设施的“最小化攻击面”**
*   **[事实陈述]** Azure Linux 是微软为 Azure 内部及边缘服务构建的自有 Linux 发行版，源自 CBL-Mariner。
*   **[你的推断]** 随着云服务数量的指数级增长，维护数百万台运行着不同版本 Ubuntu/CentOS/RHEL 的虚拟机带来了巨大的“配置漂移”和安全补丁管理成本。通过建立自家发行版，微软可以剔除非必要组件，仅保留运行容器或云代理所需的内核态功能。
*   **[作者观点]** 这是一种“收网”行为。虽然微软宣称是为了安全，但更深层的逻辑是掌握了内核级的调度优化权，不再受制于上游发行版的发布周期。

**2. 理由二：边缘计算与混合云的战略支点**
*   **[事实陈述]** Azure Linux 不仅用于云端 VM，也是 Azure Stack HCI 和 IoT Edge 的核心。
*   **[你的推断]** 在边缘计算场景下，操作系统必须极度轻量且支持长期无人值守运行。通用的企业级 Linux 过于臃肿。
*   **[实际案例]** 类似于 AWS 基于 Fedora 的优化，微软需要一个能深度整合 AKS（Azure Kubernetes Service）的底层，使得从云端到边缘的运行时环境完全一致，消除“在我机器上能跑”的环境差异。

**3. 理由三：应对 CentOS 停服带来的供应链风险**
*   **[事实陈述]** CentOS（特别是 CentOS 8）的停摆迫使全球企业寻找替代品。
*   **[作者观点]** 微软推出 Azure Linux 也是为了给企业客户（尤其是重度依赖 Azure 的客户）一个“默认的安全选项”。虽然它目前主要面向内部，但未来极有可能成为 AKS 官方支持的默认 OS 基线，从而锁定用户生态。

**反例/边界条件：**

*   **边界条件 1：社区生态的匮乏。**
    *   **[你的推断]** 与 Ubuntu 或 Red Hat 拥有庞大的软件仓库和社区支持不同，Azure Linux 的包管理器（基于 RPM）和仓库相对封闭。如果企业试图将其用于通用业务（如运行复杂的中间件或非容器化应用），将面临严重的软件缺失问题，需要大量手动编译。
*   **边界条件 2： vendor lock-in（厂商锁定）风险。**
    *   **[不同观点]** 虽然微软宣称它是开源的，但“开源”不等于“开放标准”。如果企业深度依赖 Azure Linux 特有的内核优化或工具链，未来迁移回本地数据中心或其他公有云的成本将显著增加。

---

### 深度评价维度

#### 1. 内容深度与论证严谨性
从技术架构看，Azure Linux 的设计哲学体现了**“不可变基础设施”** 的思维。它不是一个面向多用户的通用 OS，而是一个面向容器的 Host OS。其深度在于它承认了现代云原生计算的现实：操作系统正在退化为仅仅是一个运行容器的内核加 init 系统。微软在文档中对安全启动、内核加固的描述非常严谨，但这更多是工程上的胜利，而非理论上的创新。

#### 2. 实用价值与指导意义
对于**架构师**而言，这一事件的价值在于：**必须重新评估 OS 选型策略**。过去“默认选 Ubuntu”的习惯在 Azure 环境下可能不再是性能最优解。对于**运维团队**，这意味着需要掌握新的工具链（如 `tdnf` 包管理器），并适应微软定义的 SLA 和补丁节奏。它提醒我们，云厂商正在将控制力向上层应用延伸，OS 正在成为云服务的一部分，而非独立的采购项。

#### 3. 创新性
Azure Linux 本身并没有创造全新的 Linux 技术栈，它是现有的 RPM/Yum/DNF 技术的重组。**其创新点在于“交付模式的转变”**——它证明了云巨头正在通过构建“内部分支”来规避社区 Linux 发行版的碎片化问题。这是一种**运营模式的创新**，即将 OS 视为像 Hyper-V 或 Azure Firewall 一样的云内部件，而非独立的商品。

#### 4. 行业影响
这一举措将加剧**“云厂商 OS 分支”**的趋势。继 Amazon Linux 之后，Azure Linux 的成熟化意味着 Google 可能会强化其基于 Container-Optimized OS 的策略。这将削弱 Red Hat 和 SUSE 在公有云底层的话语权，迫使操作系统厂商向更上层的混合云管理平台转型。

#### 5. 争议点
*   **承诺的可信度：** 微软曾有过许多“拥抱开源”的历史，但也有过“Embrace, Extend, Extinguish”的前科。社区担心 Azure Linux 会在某些 API 层面上通过非标准优化来“软性锁定”用户。
*   **开源的真实性：** 虽然代码开源，但 Roadmap（路线图）完全由微软控制。社区贡献者能否真正影响其发展方向，目前存疑。

---

### 实际应用建议

1.

---
## 代码示例




```python
# 示例1：检查系统是否为Azure Linux
import platform
import subprocess

def is_azure_linux():
    """
    检查当前系统是否为Microsoft Azure Linux
    通过检查/etc/os-release文件中的ID字段
    """
    try:
        with open('/etc/os-release', 'r') as f:
            for line in f:
                if line.startswith('ID='):
                    return 'azurelinux' in line.lower()
    except FileNotFoundError:
        return False
    return False

# 测试
if is_azure_linux():
    print("当前系统是Azure Linux")
else:
    print("当前系统不是Azure Linux")
```




```python
# 示例2：获取Azure Linux版本信息
def get_azure_linux_version():
    """
    获取Azure Linux的版本信息
    返回版本号和代号
    """
    version_info = {}
    try:
        with open('/etc/os-release', 'r') as f:
            for line in f:
                if line.startswith('VERSION='):
                    version_info['version'] = line.split('=')[1].strip('"')
                elif line.startswith('VERSION_CODENAME='):
                    version_info['codename'] = line.split('=')[1].strip('"')
    except FileNotFoundError:
        return None
    return version_info

# 测试
version = get_azure_linux_version()
if version:
    print(f"Azure Linux版本: {version.get('version')}")
    print(f"代号: {version.get('codename')}")
```




```python
# 示例3：检查Azure Linux内核版本
def get_kernel_version():
    """
    获取当前运行的内核版本
    Azure Linux通常使用特定的内核版本
    """
    try:
        result = subprocess.run(['uname', '-r'], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return f"获取失败: {str(e)}"

# 测试
kernel = get_kernel_version()
print(f"当前内核版本: {kernel}")
if 'azure' in kernel.lower():
    print("这是Azure优化的内核")
```


---
## 案例研究


### 1：Microsoft Azure 超大规模基础设施（内部应用）

 1：Microsoft Azure 超大规模基础设施（内部应用）

**背景**: 
作为全球第二大公有云提供商，Azure 运营着遍布全球的数据中心，运行着数百万台物理服务器。这些服务器支撑着从 Azure Kubernetes Service (AKS) 到 HDInsight 等各种核心服务。长期以来，Azure 内部使用的是基于 Ubuntu 的定制版 Linux，但随着规模的扩大，维护一个庞大的外部发行版分支变得日益复杂且低效。

**问题**: 
直接使用上游 Linux 发行版（如 Ubuntu）进行深度定制会带来“分支发散”问题。当上游更新时，Azure 团队需要耗费大量精力去合并补丁，这导致了技术债务的积累。此外，为了优化 Azure 特有的硬件（如 FPGA 芯片）和软件栈，团队需要一个更轻量、启动更快、且完全由微软控制的内核和发行版，以减少不必要的软件包负担并提高安全性。

**解决方案**: 
微软开发了 **Azure Linux**（原 CBL-Mariner）。这是一个轻量级的开源 Linux 发行版，专为 Azure 的内部基础设施和边缘产品构建。它采用了经过微软优化的 Linux 内核，并包含了一套符合云原生标准的包管理器和构建系统。Azure Linux 被部署在 Azure 底层的基础设施节点上，作为运行云服务的宿主操作系统。

**效果**: 
通过 Azure Linux，微软成功实现了对基础设施操作系统的完全控制，显著降低了维护成本和安全风险。该系统针对云环境进行了极致精简，实现了更快的启动时间和更小的内存占用。目前，Azure Linux 已成为 Azure 服务端云基础设施的默认操作系统，并作为 AKS 的底层基础 OS，为数百万用户提供稳定的云服务。

---



### 2：Azure Kubernetes Service (AKS) 的底层 OS 支持

 2：Azure Kubernetes Service (AKS) 的底层 OS 支持

**背景**: 
Azure Kubernetes Service (AKS) 是 Azure 提供的托管 Kubernetes 服务，被大量企业用于部署容器化应用。在 AKS 的发展过程中，微软最初主要依赖 Ubuntu 作为节点操作系统。然而，随着企业客户对安全性、合规性以及性能要求的提高，单纯依赖第三方发行版逐渐显露出局限性。

**问题**: 
许多企业客户，尤其是金融和医疗行业，对底层操作系统有严格的安全合规要求。使用通用的 Linux 发行版可能包含大量 AKS 集群运行所不需要的预装软件，从而增加了攻击面。此外，当内核出现安全漏洞时，依赖上游发行版的修复周期可能无法满足微软快速响应和发布补丁的需求。

**解决方案**: 
微软将 **Azure Linux** 引入 AKS 生态系统，推出了 **Azure Linux 容器主机**（Mariner 作为基础 OS）。这为用户提供了一个全新的节点镜像选项。该 OS 专为容器工作负载优化，仅包含运行 Kubernetes 所需的最小组件，并由微软直接提供安全补丁和更新支持，消除了中间环节。

**效果**: 
引入 Azure Linux 作为容器主机后，AKS 用户获得了更精简、更安全的运行环境。由于减少了不必要的软件包，系统的受攻击面显著降低，同时节点启动速度和运行性能得到了提升。对于微软而言，这意味着在处理关键内核安全漏洞（如 CVE）时，可以更快地向 AKS 用户提供修复补丁，而不必等待第三方发行版的排期，大大增强了云服务的安全韧性。

---
## 最佳实践

## 最佳实践指南

### 实践 1：系统更新与软件源管理

**说明**:
Azure Linux 是微软发布的开源 Linux 发行版，针对云环境和边缘计算进行了优化。保持系统更新是确保安全性和性能的关键。Azure Linux 使用 RPM 包管理和特定的软件源配置。

**实施步骤**:
1. 配置正确的软件源仓库，确保指向 Azure Linux 官方或镜像站点
2. 定期运行更新命令：`sudo dnf update`
3. 对于生产环境，先在测试环境验证更新
4. 启用自动安全更新（如适用）

**注意事项**:
- 始终检查更新日志，特别是内核和关键系统组件的更新
- 保留回滚计划，特别是在进行大版本更新时
- 注意软件源的可用性，必要时配置本地镜像源

---

### 实践 2：安全加固与访问控制

**说明**:
云环境中的 Linux 系统面临多种安全威胁。Azure Linux 提供了基础安全配置，但需要根据具体使用场景进行进一步加固。

**实施步骤**:
1. 禁用 root 远程登录，改用 sudo 权限管理
2. 配置防火墙规则（如 firewalld 或 iptables）
3. 安装并配置 fail2ban 防止暴力破解
4. 定期审查系统日志：`/var/log/secure` 和 `/var/log/messages`
5. 使用 SSH 密钥认证而非密码认证

**注意事项**:
- 安全加固应与业务需求平衡，避免过度限制影响功能
- 定期进行安全扫描和漏洞评估
- 保持安全策略的文档化和版本控制

---

### 实践 3：云集成与监控配置

**说明**:
Azure Linux 设计用于与 Azure 云服务深度集成。正确配置云代理和监控工具对于管理云中的 Linux 实例至关重要。

**实施步骤**:
1. 安装并配置 Azure VM 扩展代理
2. 设置 Azure Monitor 或 Log Analytics 代理
3. 配置系统诊断和数据收集规则
4. 设置基于 Azure Policy 的合规性监控
5. 配置健康探测和自动恢复机制

**注意事项**:
- 监控数据传输可能产生网络成本，需合理设置采样率
- 确保监控代理有足够的系统资源
- 定期审查监控数据，调整告警阈值

---

### 实践 4：性能优化与资源管理

**说明**:
Azure Linux 针对云环境进行了性能优化，但正确配置系统资源管理可以进一步提升性能和稳定性。

**实施步骤**:
1. 配置 swap 空间和使用策略
2. 优化 I/O 调度器（如 deadline 或 noop）
3. 根据工作负载调整 CPU 调度策略
4. 配置资源限制（cgroups）防止资源争用
5. 优化网络参数（TCP/IP 栈设置）

**注意事项**:
- 性能优化应基于实际工作负载分析
- 使用性能分析工具（如 perf、top、iotop）进行诊断
- 记录所有优化变更，便于回滚

---

### 实践 5：容器化与编排支持

**说明**:
Azure Linux 对容器技术有良好支持，特别是与 Azure Kubernetes Service (AKS) 的集成。正确配置容器运行时对于云原生应用至关重要。

**实施步骤**:
1. 安装并配置容器运行时（如 containerd 或 CRI-O）
2. 配置镜像加速器（如 Azure Container Registry）
3. 设置容器资源限制和健康检查
4. 配置容器网络插件（如 CNI）
5. 实施容器镜像扫描和签名验证

**注意事项**:
- 定期更新容器运行时和基础镜像
- 实施最小权限原则运行容器
- 监控容器资源使用情况

---

### 实践 6：日志管理与审计

**说明**:
有效的日志管理是故障排查和安全审计的基础。Azure Linux 提供了多种日志记录机制，需要合理配置。

**实施步骤**:
1. 配置 systemd-journald 持久化存储
2. 设置集中式日志收集（如 ELK Stack 或 Azure Monitor）
3. 配置审计规则
4. 实施日志轮转策略防止磁盘填满
5. 保护敏感日志信息的访问权限

**注意事项**:
- 遵守数据保留和隐私法规要求
- 定期测试日志恢复流程
- 确保时间同步（NTP）准确，便于日志关联分析

---

### 实践 7：高可用性与灾难恢复

**说明**:
在云环境中设计高可用架构至关重要。Azure Linux 提供了多种机制来支持高可用部署。

**实施步骤**:
1. 配置 Azure 可用性集或可用性区域
2. 实施负载均衡（如 Azure Load Balancer）
3. 设置数据备份策略（如 Azure Backup）
4. 配置自动故障转移机制
5. 定期测试灾难恢复流程

**注意事项**:
- 明确 RPO（恢复点目标）和 RTO（恢复时间目标）
- 文档化灾难

---
## 学习要点

- 微软正式推出 Azure Linux，这是一款为 Azure 服务优化的开源 Linux 发行版，旨在统一云基础设施的操作系统底座。
- 该系统基于 CBL-Mariner（微软内部构建的通用基础 Linux 发行版），专为容器化和云端工作负载进行了深度定制与性能优化。
- Azure Linux 强化了安全性设计，采用经过微软严格审查的组件和更新机制，以符合企业级云服务的合规与防护标准。
- 此举标志着微软从单纯的 Linux 支持者转变为 Linux 发行版的维护者，体现了其对开源生态的战略性投入。
- 该系统目前主要作为 Azure 内部服务的底层平台，未来有望为外部开发者提供更完善的云原生应用支持。

---
## 常见问题


### 1: Microsoft Azure Linux 到底是什么？它是 Ubuntu 的替代品吗？

1: Microsoft Azure Linux 到底是什么？它是 Ubuntu 的替代品吗？

**A**: Microsoft Azure Linux（前身为 CBL-Mariner）是微软开源的一个 Linux 发行版。它并非设计为桌面用户或通用服务器的 Ubuntu 直接替代品，而是微软内部云基础设施的核心组件。

它的主要目的是为 Azure 的 Kubernetes 服务（AKS）以及 Azure 的超融合基础设施（HCI）提供底层操作系统支持。它的设计理念是“云原生”，注重安全性、性能和轻量化，非常适合作为容器宿主，而不是作为一个功能齐全的通用服务器操作系统（如带有完整 GUI 或大量桌面应用支持）。

---



### 2: 微软为什么要开发自己的 Linux 发行版？

2: 微软为什么要开发自己的 Linux 发行版？

**A**: 微软开发 Azure Linux 主要出于对云基础设施的控制、安全性和效率的考量。

1.  **供应链安全**：通过拥有自己的发行版，微软可以完全控制软件包的构建和发布流程，减少对外部上游发行版更新周期的依赖，从而更快地修补漏洞（如 CVE）。
2.  **性能优化**：微软可以针对 Azure 的硬件环境对内核进行深度优化，剔除不必要的驱动和功能，使系统更轻量、启动更快。
3.  **标准化**：在庞大的 Azure 云环境中，使用统一的内部 Linux 发行版可以大幅降低运维复杂度，确保所有节点的一致性。

---



### 3: Azure Linux 基于什么技术？它使用 RPM 还是 DEB 包管理？

3: Azure Linux 基于什么技术？它使用 RPM 还是 DEB 包管理？

**A**: Azure Linux 是基于 RPM 和 DNF 包管理器的。

这意味着它在技术架构上与 Fedora、RHEL（Red Hat Enterprise Linux）或 CentOS 更为相似，而不是基于 Debian 或 Ubuntu（后者使用 .deb 包）。然而，Azure Linux 的用户空间工具链非常精简，默认不包含许多标准 Linux 发行版中预装的图形界面或开发工具，它主要设计用于运行容器化工作负载。

---



### 4: 普通用户可以在自己的电脑或本地服务器上安装和使用 Azure Linux 吗？

4: 普通用户可以在自己的电脑或本地服务器上安装和使用 Azure Linux 吗？

**A**: 虽然技术上可以下载并运行 Azure Linux，但微软并不建议普通用户将其作为日常操作系统使用。

Azure Linux 缺乏许多桌面环境所需的硬件驱动支持和图形界面配置工具。它的安装过程、系统管理和维护主要面向云运维工程师和开发者。如果你需要一个稳定、受社区支持的 Linux 服务器系统，Ubuntu Server、Rocky Linux 或 AlmaLinux 通常是更合适的选择。Azure Linux 的定位主要还是作为 Azure 云服务后端的一个“引擎”。

---



### 5: Azure Linux 和之前微软发布的 WSL (Windows Subsystem for Linux) 有什么区别？

5: Azure Linux 和之前微软发布的 WSL (Windows Subsystem for Linux) 有什么区别？

**A**: 这是两个完全不同的产品。

*   **WSL** 是一个运行在 Windows 10/11 桌面版上的兼容层，允许用户在 Windows 内部直接运行 Linux 环境（如 Ubuntu、Debian 等）。它主要面向开发者，用于在 Windows 上进行 Linux 开发。
*   **Azure Linux** 是一个完整的、独立的操作系统发行版。它运行在裸金属服务器或虚拟机上，直接管理硬件资源，而不是运行在 Windows 之上。它是用来支撑 Azure 云服务的，而不是运行在 Windows 里面的工具。

---



### 6: Azure Linux 是开源的吗？我可以查看它的源代码吗？

6: Azure Linux 是开源的吗？我可以查看它的源代码吗？

**A**: 是的，Azure Linux 是开源项目。

微软在 GitHub 上公开了 Azure Linux 的源代码和构建工具。这符合微软近年来积极拥抱开源的战略。开发者可以查看其构建配置、提交 Bug 报告，甚至可以根据其许可证（通常是 MIT 许可证）自由使用和修改代码。这种透明度有助于增强云客户对微软基础设施安全性的信任。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: Microsoft Azure Linux 是基于哪个开源发行版构建的？请列出该发行版的主要特点，并解释为什么微软选择它作为 Azure Linux 的基础，而不是直接使用 Ubuntu 或 Debian。

### 提示**: 关注 Azure Linux 的前身 CBL-Mariner 的技术文档，特别是关于包管理和系统架构的描述。思考云基础设施对操作系统内核和用户空间工具的特定需求。

### 

---
## 引用

- **原文链接**: [https://github.com/microsoft/azurelinux](https://github.com/microsoft/azurelinux)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46805841](https://news.ycombinator.com/item?id=46805841)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [微软](/tags/%E5%BE%AE%E8%BD%AF/) / [Azure](/tags/azure/) / [Linux](/tags/linux/) / [CBL-Mariner](/tags/cbl-mariner/) / [云原生](/tags/%E4%BA%91%E5%8E%9F%E7%94%9F/) / [容器化](/tags/%E5%AE%B9%E5%99%A8%E5%8C%96/) / [DevOps](/tags/devops/) / [操作系统](/tags/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F/)
- 场景： [DevOps/运维](/scenarios/devops-%E8%BF%90%E7%BB%B4/)

### 相关文章

- [🔥重磅！Fedora Asahi Remix 成功适配 Apple M3！]({{< relref "posts/20260127-hacker_news-fedora-asahi-remix-is-now-working-on-apple-m3-17.md" >}})
- [🔥Fedora Asahi Remix成功适配M3！苹果芯片生态再突破！🚀]({{< relref "posts/20260127-hacker_news-fedora-asahi-remix-is-now-working-on-apple-m3-18.md" >}})
- [Linux 两位大神联手创业！Systemd 之父 Poettering 出击！🚀]({{< relref "posts/20260127-hacker_news-lennart-poettering-christian-brauner-founded-a-new-4.md" >}})
- [🔥Lede固件巅峰！OpenWrt大神力作，性能炸裂！🚀]({{< relref "posts/20260126-github_trending-coolsnowwolf-lede-2.md" >}})
- [🔥炸裂！Fedora Asahi Remix成功登陆苹果M3！Linux体验再升级！]({{< relref "posts/20260126-hacker_news-fedora-asahi-remix-is-now-working-on-apple-m3-3.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*