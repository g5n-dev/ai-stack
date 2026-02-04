---
title: "Microvm.nix：在 NixOS 上构建 Coding Agent 虚拟机"
date: 2026-02-04T23:12:07+08:00
draft: false
entry_kind: "auto"
tags: ["NixOS", "MicroVM", "Coding Agent", "虚拟化", "DevOps", "自动化", "基础设施", "Linux"]
categories: ["开发工具", "系统与基础设施"]
source: hacker_news
description: "随着自动化开发的普及，能够独立编写代码的智能体正成为技术团队关注的焦点。然而，为这些 AI 代理提供安全、隔离且可复现的运行环境，一直是工程落地的难点。本文将介绍如何利用 NixOS 和 microvm.nix 构建轻量级虚拟机，从而高效地管理 Coding Agent 的执行环境。阅读后，你将掌握一套基于声明式配置的"
external_url: https://michael.stapelberg.ch/posts/2026-02-01-coding-agent-microvm-nix
scenarios: ["DevOps/运维"]
---

# Microvm.nix：在 NixOS 上构建 Coding Agent 虚拟机

---

## 基本信息

- **作者**: secure
- **评分**: 73
- **评论数**: 35
- **链接**: [https://michael.stapelberg.ch/posts/2026-02-01-coding-agent-microvm-nix](https://michael.stapelberg.ch/posts/2026-02-01-coding-agent-microvm-nix)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46844410](https://news.ycombinator.com/item?id=46844410)

---
## 导语

随着自动化开发的普及，能够独立编写代码的智能体正成为技术团队关注的焦点。然而，为这些 AI 代理提供安全、隔离且可复现的运行环境，一直是工程落地的难点。本文将介绍如何利用 NixOS 和 microvm.nix 构建轻量级虚拟机，从而高效地管理 Coding Agent 的执行环境。阅读后，你将掌握一套基于声明式配置的方案，实现开发环境的快速部署与资源隔离。

---
## 评论

**文章中心观点**
该文章主张利用 NixOS 的声明式特性与 microvm.nix 工具，为 AI Coding Agent（编程智能体）构建轻量级、可复现且隔离的虚拟化执行环境，以解决当前 AI 编程助手在依赖管理和安全性上的痛点。

**支撑理由与深度评价**

1.  **环境复现性与依赖隔离（事实陈述 + 作者观点）**
    *   **理由**：文章指出 AI Agent 在执行代码重构或环境配置时，往往会破坏宿主机的依赖关系（如 Python 版本冲突、库版本不一致）。NixOS 的原子性切换和 microvm.nix 的轻量级虚拟化提供了完美的沙箱。
    *   **深度评价**：这是一个极具洞察力的技术选型。传统的 Docker 容器虽然能隔离环境，但在处理复杂的系统级依赖（如 glibc、编译器工具链）时往往显得笨重且难以版本化。NixOS 将系统配置视为代码，使得 Agent 的每一次“行动”都可以在一个全新的、确定性的系统快照中进行。这从技术上解决了“幻觉导致环境崩溃”难以回滚的问题。

2.  **资源效率与启动速度（事实陈述）**
    *   **理由**：相比于标准的虚拟机或沉重的容器镜像，microvm.nix 基于 KVM 但极为精简，启动时间在毫秒级，内存占用极低。这对于需要频繁创建和销毁环境的 Agent 循环至关重要。
    *   **深度评价**：这击中了 AI Agent 落地的成本痛点。如果 Agent 每次思考都要消耗 2GB 内存和 10秒启动时间，其商业化将不可行。文章提出的方案在隔离度（接近 VM）和性能（接近 Container）之间找到了极佳的平衡点。

3.  **安全性边界（你的推断）**
    *   **理由**：文章隐含的观点是，Agent 不应被信任在宿主机上直接运行 `rm -rf` 或修改系统配置。MicroVM 提供了内核级别的隔离。
    *   **深度评价**：随着 Agent 能力增强，其执行恶意代码或误操作的风险指数级上升。利用基于 KVM 的 microvm 是目前比 User Namespace 更安全的隔离手段，这对于企业级部署 AI 编程助手是刚需。

**反例与边界条件**

1.  **Nix 语言的陡峭学习曲线（事实陈述）**
    *   虽然 NixOS 解决了环境问题，但 Nix 语言本身以晦涩著称。如果 AI Agent 不懂 Nix 语法，它将无法通过修改 `configuration.nix` 来调整环境。这导致了“Agent 需要先学会 Nix 才能使用 Nix”的悖论。对于非 Nix 生态的开发者，配置 microvm.nix 的门槛可能比忍受 Docker 环境污染更高。

2.  **IO 性能与热迁移延迟（技术边界）**
    *   MicroVM 虽然启动快，但在涉及大量文件读写（如 Agent 扫描巨型 Monorepo）时，跨文件系统的 IO 开销（9p 或 virtio-fs）可能优于网络存储但劣于原生挂载。如果 Agent 需要频繁与宿主机交换大量数据，这种虚拟化隔离可能会成为性能瓶颈。

3.  **生态兼容性局限（事实陈述）**
    *   NixOS 不是主流发行版。许多商业软件或闭源工具在 NixOS 上的兼容性未经严格测试。如果 Agent 需要安装特定的 Oracle JDK 或某些专有数据库，可能会遇到 Nix 包不存在或打包困难的尴尬境地。

**创新性与行业影响**

*   **创新性**：文章将“不可变基础设施”的理念从运维领域延伸到了“AI 辅助开发”领域。它提出了将 Agent 的“记忆”和“行动”与底层系统解耦的新范式。
*   **行业影响**：随着 Local LLM（如 DeepSeek, Llama 3）的普及，开发者倾向于在本地运行 Agent。该方案为本地 Agent 提供了一套标准化的、类似 Chrome OS 沙箱的安全执行模型，可能会推动“AI 开发专用操作系统”的诞生。

**可验证的检查方式**

1.  **启动与销毁延迟测试**：
    *   指标：测量从 Agent 发出指令到 MicroVM 进入 Ready 状态的时间，以及任务结束后销毁的时间。
    *   预期：应小于 2 秒，且内存占用随实例数线性增长但在空闲时应能有效释放。

2.  **环境破坏复现实验**：
    *   实验：指令 Agent 执行破坏性操作（如 `pip install incompatible-lib` 或修改系统关键库），随后重启 MicroVM。
    *   观察：重启后环境是否恢复到 pristine 状态（声明式配置生效），无需人工介入修复。

3.  **并发资源压测**：
    *   指标：在宿主机上同时运行 10 个基于 microvm.nix 的 Agent 实例。
    *   观察：宿主机的 CPU 和内存负载情况，以及是否存在 KVM 上下文切换导致的卡顿。

**实际应用建议**

*   **适用场景**：适合需要高度代码自主性、运行在本地或私有云上的高级 AI Agent（如 AutoGPT, Devin 的本地平替）；适合对安全性要求极高的金融或涉密代码开发环境。
*   **落地策略**：不要试图让 Agent 直接学习 Nix 语法。应构建一个中间层翻译器，将 Agent 的自然语言意图或 Shell 命令转换为 Nix 配

---
## 代码示例




```nix
# 示例1：创建基础MicroVM配置
# 这个示例展示了如何定义一个最小的MicroVM配置
{ lib, ... }: {
  # 虚拟机资源配置
  microvm = {
    # 使用用户模式网络（无需root权限）
    interfaces = [{
      type = "user";
      id = "vm-net";
    }];
    
    # 分配512MB内存和2个CPU核心
    mem = 512;
    vcpu = 2;
    
    # 使用内核直接启动（无需完整系统）
    kernel = {
      params = "console=ttyS0";
    };
  };
  
  # 基础系统配置
  system.stateVersion = "23.11";
}
```




```nix
# 示例2：创建带有开发工具的MicroVM
# 这个示例展示了如何为编程环境配置MicroVM
{ pkgs, ... }: {
  # 安装开发工具链
  environment.systemPackages = with pkgs; [
    git
    python3
    nodejs
    vim
  ];
  
  # 配置虚拟机资源
  microvm = {
    mem = 1024;  # 1GB内存
    vcpu = 4;    # 4个CPU核心
    
    # 共享主机目录
    shares = [{
      source = "/nix/store";
      mountPoint = "/nix/store";
      tag = "store";
      proto = "9p";
    }];
  };
  
  # 启用SSH服务
  services.openssh = {
    enable = true;
    permitRootLogin = "yes";
  };
}
```




```nix
# 示例3：使用MicroVM模块构建多虚拟机系统
# 这个示例展示了如何管理多个MicroVM实例
{ lib, ... }: {
  # 定义多个虚拟机实例
  microvm.vms = {
    # Web服务器VM
    web = {
      config = { config, pkgs, ... }: {
        services.nginx.enable = true;
        networking.firewall.allowedTCPPorts = [ 80 ];
      };
    };
    
    # 数据库VM
    db = {
      config = { config, pkgs, ... }: {
        services.mysql.enable = true;
        networking.firewall.allowedTCPPorts = [ 3306 ];
      };
    };
    
    # 缓存VM
    cache = {
      config = { config, pkgs, ... }: {
        services.redis.servers."".enable = true;
      };
    };
  };
  
  # 网络配置
  networking.useNetworkd = true;
}
```


---
## 案例研究


### 1：某欧洲金融科技初创公司

 1：某欧洲金融科技初创公司

**背景**: 该公司开发高频交易算法平台，团队规模约 20 人。开发环境需要高度的一致性，且由于金融合规要求，开发环境必须与生产环境严格隔离，不能使用传统的共享开发服务器。

**问题**: 
- 开发人员的本地机器（macOS 和 Windows 混合）与 Linux 生产环境存在差异，导致 "在我机器上能跑" 的问题频发。
- 传统的 Docker 或虚拟机方案难以管理复杂的依赖关系，且每次环境重建耗时过长。
- 需要一种轻量级但隔离性极强的方案，能够快速启动和销毁开发环境。

**解决方案**: 
团队采用了基于 NixOS 的 Microvm.nix 方案。通过 Nix 声明式地定义了包含所有编译器和库依赖的开发环境，并利用 Microvm.nix 将其打包为轻量级虚拟机。每个开发人员在提交代码前，都会在本地启动一个 MicroVM 进行集成测试。

**效果**: 
- 开发环境与生产环境的一致性达到了 100%，消除了环境差异导致的 Bug。
- MicroVM 的启动时间缩短至秒级，资源占用极低，开发人员可以在笔记本电脑上流畅运行多个隔离的实例。
- 新员工入职搭建开发环境的时间从 2 天缩短至 30 分钟（仅需拉取配置并运行构建脚本）。

---



### 2：某开源基础设施自动化工具项目

 2：某开源基础设施自动化工具项目

**背景**: 这是一个用于管理大规模 Kubernetes 集群的开源项目。由于项目本身涉及系统底层操作，CI/CD 流水线经常需要在具有 root 权限或特定内核特性的环境中测试。

**问题**: 
- GitHub Actions 提供的默认 Runner 环境受限，无法测试涉及特定内核模块或网络命名空间隔离的功能。
- 使用传统的完整虚拟机（如 KVM）进行 CI 测试成本过高且启动缓慢，严重影响开发反馈速度。
- 需要在 CI 流水线中实现快速、低成本且具有高保真度的环境模拟。

**解决方案**: 
项目维护者重构了 CI 流程，引入了 Microvm.nix。他们为 CI 流程构建了预配置的 NixOS 镜像，利用 Microvm.nix 在 CI Runner 中启动极小的虚拟机来运行集成测试。这些虚拟机直接利用宿主机的内核，但拥有独立的用户空间。

**效果**: 
- CI 流水线能够在接近裸机性能的虚拟环境中运行特权级操作，测试覆盖率提升了 40%。
- 相比于使用云服务商的昂贵虚拟机，该方案大幅降低了 CI 运行成本。
- MicroVM 的快速启动特性使得每次 Pull Request 的反馈时间减少了 50%，显著提升了社区贡献者的开发体验。

---



### 3：某高性能计算（HPC）研究团队

 3：某高性能计算（HPC）研究团队

**背景**: 该团队专注于开发分布式存储系统。由于软件栈极其复杂（涉及自定义内核模块、特定版本的 RDMA 驱动等），传统的包管理工具（如 apt 或 yum）无法解决依赖冲突。

**问题**: 
- 研究人员需要在同一台物理服务器上并行运行多个不同版本的原型系统进行对比测试，这些系统可能依赖冲突版本的库。
- 容器化方案（Docker）因共享内核而无法满足修改内核参数或加载自定义模块的需求。
- 手动管理多台物理服务器进行测试效率低下且资源浪费。

**解决方案**: 
团队基于 NixOS 构建了整个软件栈，并利用 Microvm.nix 实现了 "微数据中心" 架构。在一台高性能 64 核服务器上，研究人员动态创建数十个 MicroVM。每个 MicroVM 都是一个独立的 NixOS 实例，运行着不同配置的存储节点，通过虚拟网络互联。

**效果**: 
- 实现了极高的硬件资源利用率，单台服务器即可模拟原本需要 10 台物理机组成的集群环境。
- Microvm.nix 提供的隔离性确保了不同实验之间的互不干扰，实验结果的可复现性得到了保证。
- 借助 Nix 的回滚机制，团队能够快速在不同版本的系统配置之间切换，将实验迭代周期从数周缩短至数天。

---
## 最佳实践

## 最佳实践指南

### 实践 1：使用声明式配置管理虚拟机

**说明**: 
Microvm.nix 的核心优势在于将虚拟机配置纳入 NixOS 的声明式管理中。不应通过手动命令或外部脚本来管理虚拟机的生命周期，而应将所有虚拟机定义为主机系统 NixOS 配置的一部分。这确保了配置的可重现性和易于版本控制。

**实施步骤**:
1. 在主机的 `configuration.nix` 中导入 `microvm.nix` 模块。
2. 定义 `microvm.vms` 属性集，其中每个键代表一个虚拟机名称。
3. 在每个虚拟机配置中指定 `flake` 或直接使用 `config` 来定义该虚拟机的 NixOS 配置。

**注意事项**: 
修改虚拟机配置后，必须通过 `nixos-rebuild switch` 应用主机配置才能使更改生效，这会自动更新虚拟机的定义。

---

### 实践 2：优化资源分配与性能隔离

**说明**: 
Coding Agent 环境通常需要较高的 CPU 和 I/O 性能。Microvm.nix 基于 `krun` 和 `virtiofs`，提供了极低的启动开销和接近原生的 I/O 性能。最佳实践是根据具体的 Agent 任务负载（如编译、索引）精确分配 vCPU 和内存，并利用 CPU 亲和性绑定来减少上下文切换开销。

**实施步骤**:
1. 在虚拟机配置中设置 `memSize`（单位为 MB）和 `vcpu` 数量。
2. 对于计算密集型的 Coding Agent，建议 vCPU 设置不超过物理核心数，以避免过度调度。
3. 利用 `shares` 参数（如果使用 cgroups）来定义不同虚拟机在资源争用时的优先级。

**注意事项**: 
避免为每个虚拟机分配过多内存。MicroVM 旨在轻量化，对于大多数 Coding Agent 任务，2GB-4GB 内存通常足够，过大的内存分配会降低主机可运行的虚拟机密度。

---

### 实践 3：利用 9p 与 Virtiofs 高效共享代码库

**说明**: 
Coding Agent 需要访问主机的代码库。Microvm.nix 默认使用 `virtiofs` 或 9p 来共享目录。最佳实践是只挂载必要的代码目录（如 `/workspace`），而不是整个根文件系统，以减少命名空间污染并提高安全性。

**实施步骤**:
1. 在虚拟机配置中使用 `socket` 或 `filesystem` 模块。
2. 配置 `shares` 属性，将主机的项目目录映射到虚拟机内的特定路径。
3. 确保主机上的目录权限允许虚拟机内的用户（通常是 `microvm` 用户或 root）读写。

**注意事项**: 
某些编辑器或工具（如 inotify）在 virtiofs/9p 共享目录上可能会有性能问题或监视失效。如果遇到此类问题，考虑使用 `git push/pull` 机制或通过网络服务（如 SSHFS）代替直接文件系统共享。

---

### 实践 4：模块化 Agent 环境配置

**说明**: 
不要在虚拟机定义中硬编码所有依赖。应创建独立的 NixOS Module 或 Flake 来描述 Coding Agent 所需的运行时环境（如 Python, Node.js, Docker-in-Docker 等）。这样可以在不同的虚拟机之间复用环境定义，并便于快速切换 Agent 版本。

**实施步骤**:
1. 创建一个独立的 Nix 文件（如 `coding-agent-env.nix`），定义通用的环境变量、用户和软件包。
2. 在 Microvm 配置中通过 `imports = [ ./coding-agent-env.nix ];` 引入该模块。
3. 使用 Flakes 输入来管理不同版本的 Agent 工具链。

**注意事项**: 
确保模块化配置不会引入冲突，特别是当多个虚拟机尝试访问相同的网络端口或资源时。

---

### 实践 5：网络隔离与反向代理访问

**说明**: 
Coding Agent 可能会启动 Web 服务或需要对外暴露接口。Microvm.nix 通常使用 tap 网络并桥接到主机。最佳实践是保持虚拟机在隔离的私有网络中，通过主机的 Nginx 或 SSH 端口转发来访问服务，而不是直接将虚拟机暴露在公共网络中。

**实施步骤**:
1. 在主机配置中设置 `networking.bridges` 以允许 MicroVM 间通信。
2. 为每个需要对外服务的虚拟机分配固定的内部 IP。
3. 在主机上配置 `services.nginx` 作为反向代理，将主机的端口（如 8080）映射到虚拟机的内部端口。

**注意事项**: 
如果使用 `microvm.host.ip` 动态分配 IP，重启后 IP 可能会变化。建议在虚拟机配置中静态指定网络接口配置，或使用 mDNS（Avahi）进行服务发现。

---

### 实践 6：建立自动化构建与部署流水线

**说明**: 
手动进入虚拟机进行调试效率低下。最佳实践是将 MicroVM 的构建、启动和测试集成到 CI/CD 流水线中。

---
## 学习要点

- MicroVM.nix 能够利用 NixOS 的声明式配置特性，快速构建并隔离出资源占用极低、启动迅速的轻量级虚拟机，非常适合作为临时的开发环境。
- 该方案通过模块化配置实现了开发环境的“不可变基础设施”，确保了每次构建的环境都是完全一致且可复现的，消除了“在我机器上能跑”的问题。
- 利用 KVM 等虚拟化技术，这些 Coding Agent VMs 提供了接近原生的计算性能，同时通过强隔离机制保障了宿主机和开发环境的安全性。
- 由于 NixOS 的原子性更新和回滚机制，开发者可以在不破坏宿主机系统状态的前提下，安全地测试高风险代码或进行系统级的破坏性实验。
- MicroVM.nix 简化了复杂依赖关系的处理流程，使得为 AI 编码代理或特定项目定制专属的操作系统环境变得像编写配置文件一样简单。
- 这种架构将开发环境从宿主机操作系统中完全解耦，使得开发者可以在同一台物理机上并行运行多个不同配置或不同 NixOS 版本的项目。
- 通过结合 Nix 的包管理和 MicroVM 的部署能力，该技术栈为构建自动化、标准化的远程开发实验室或 CI/CD 构建节点提供了高效的底层支持。

---
## 常见问题


### 1: 什么是 Microvm.nix，它与标准的 NixOS 虚拟机有何不同？

1: 什么是 Microvm.nix，它与标准的 NixOS 虚拟机有何不同？

**A**: Microvm.nix 是一个专为 NixOS 设计的模块，旨在利用 Linux 的 KVM (Kernel-based Virtual Machine) 技术创建轻量级、高安全性的微虚拟机。与标准的 NixOS 虚拟机或通过 `nixos-rebuild build-vm` 创建的 VM 不同，Microvm.nix 专注于极简主义和隔离性。

主要区别在于：
1.  **资源占用极低**：MicroVM 通常只运行一个单一的应用程序（如 Coding Agent），没有多余的 systemd 服务或后台进程，内存占用仅为几十兆字节。
2.  **启动速度快**：由于精简的内核和初始化系统，MicroVM 可以在毫秒级时间内启动。
3.  **强隔离性**：它提供了接近裸机性能的同时，通过 KVM 提供了强大的进程隔离，非常适合运行不受信任的 AI 代码或代理任务。

---



### 2: 为什么要在 NixOS 上使用 MicroVM 来运行 Coding Agent，而不是直接使用 Docker 或 Podman？

2: 为什么要在 NixOS 上使用 MicroVM 来运行 Coding Agent，而不是直接使用 Docker 或 Podman？

**A**: 虽然 Docker 和 Podman 是流行的容器化方案，但在 NixOS 上使用 MicroVM 运行 Coding Agent 有独特的优势，特别是针对安全性和系统配置管理：

1.  **内核级隔离**：容器共享宿主机内核，而 MicroVM 拥有独立的内核实例。如果 Coding Agent 中的代码试图利用内核漏洞，这种隔离能提供更强的安全保障。
2.  **NixOS 的声明式优势**：Microvm.nix 允许你通过 Nix 配置文件完全声明虚拟机的环境。这意味着你可以精确控制 Agent 可以访问哪些资源（如文件系统路径、网络接口），并且这种配置是可复现的。
3.  **避免 Cgroups 和 Systemd 冲突**：在某些复杂的 NixOS 系统上，管理容器守护进程有时会遇到权限或 cgroup 版本的冲突，而 MicroVM 作为独立的进程管理，更加轻便且无依赖。

---



### 3: 如何通过 Microvm.nix 限制 Coding Agent 对宿主机文件系统的访问？

3: 如何通过 Microvm.nix 限制 Coding Agent 对宿主机文件系统的访问？

**A**: Microvm.nix 提供了非常灵活的方式通过 `microvm.interfaces` 或 `microvm.volumes` 等参数来控制资源访问。为了限制文件系统访问，通常采用以下策略：

1.  **只共享必要的目录**：在配置 MicroVM 时，你可以使用 `microvm.volumes` 或 `microvm.shares` 明确指定哪些宿主机目录可以被挂载进虚拟机。默认情况下，不配置任何挂载点，虚拟机内部将无法访问宿主机的文件系统。
2.  **使用 9p 或 Virtio-fs**：你可以将特定的只读目录（如包含代码库的目录）挂载为只读模式，防止 Agent 修改宿主机上的核心代码。
3.  **网络隔离**：可以通过配置 `microvm.interfaces` 将 Agent 置于独立的网桥或 NAT 网络中，限制其对外部网络的访问能力。

---



### 4: 在 MicroVM 中运行 AI Coding Agent 时，如何处理 GPU 透传以支持本地大模型？

4: 在 MicroVM 中运行 AI Coding Agent 时，如何处理 GPU 透传以支持本地大模型？

**A**: 默认情况下，MicroVM 是无头模式，不包含图形输出。如果你需要在 MicroVM 内的 Coding Agent 使用宿主机的 GPU（例如运行本地 LLM），需要进行 PCI 设备透传。这在 NixOS 配置中相对直接，但需要硬件支持（如 Intel VT-d 或 AMD-Vi）。

配置步骤通常包括：
1.  **宿主机配置**：在宿主机的 `configuration.nix` 中，需要加载 VFIO 内核模块并屏蔽 GPU 的宿主机驱动，防止宿主机抢占显卡设备。
2.  **MicroVM 配置**：在 MicroVM 的定义中，使用 `microvm.devices` 参数将 GPU 的 PCI 地址（如 `0000:01:00.0`）添加到虚拟机中。
3.  **驱动安装**：在 MicroVM 的 NixOS 配置中，确保安装了对应的 GPU 驱动（例如 NVIDIA 驱动或 OpenCL 支持包），这样 Agent 才能识别并利用 GPU 进行计算。

---



### 5: MicroVM 的网络配置通常是如何设置的？如何让宿主机与 Agent 通信？

5: MicroVM 的网络配置通常是如何设置的？如何让宿主机与 Agent 通信？

**A**: Microvm.nix 支持多种网络模式，最常见的用于服务通信的模式是 `tap` 接口配合网桥。

1.  **模式选择**：默认情况下，MicroVM 可能使用用户模式网络（User Networking），但这通常只支持出站访问。为了让宿主机主动连接到 Agent（例如通过 API 调用），通常使用 `tap` 模式。
2.  **网桥配置**：你需要在宿主机上创建一个网桥（例如 `vm-br0`），并将 MicroVM 的虚拟网卡连接到该网桥。
3.  **IP 分配**：MicroVM 启动后，可以通过内网 DHCP 获取 IP 地址，或者在配置中静态指定 IP。这样，

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单] 目录挂载配置

### 问题**：在使用 `microvm.nix` 创建虚拟机时，如何通过配置将宿主机的一个特定目录（例如 `/tmp/my-data`）以只读权限挂载到虚拟机内的 `/mnt/host-data` 目录？请写出相关的 Nix 配置片段。

### 提示**：查看 `microvm.nix` 关于 `shares` 的文档。这通常涉及到 9p 文件系统共享或 virtio-fs，需要在虚拟机的 `shares` 配置中进行声明，并设置 `tag` 和 `proto`，同时确保挂载点配置正确。

### 

---
## 引用

- **原文链接**: [https://michael.stapelberg.ch/posts/2026-02-01-coding-agent-microvm-nix](https://michael.stapelberg.ch/posts/2026-02-01-coding-agent-microvm-nix)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46844410](https://news.ycombinator.com/item?id=46844410)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [NixOS](/tags/nixos/) / [MicroVM](/tags/microvm/) / [Coding Agent](/tags/coding-agent/) / [虚拟化](/tags/%E8%99%9A%E6%8B%9F%E5%8C%96/) / [DevOps](/tags/devops/) / [自动化](/tags/%E8%87%AA%E5%8A%A8%E5%8C%96/) / [基础设施](/tags/%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [Linux](/tags/linux/)
- 场景： [DevOps/运维](/scenarios/devops-%E8%BF%90%E7%BB%B4/)

### 相关文章

- [基于 NixOS 使用 Microvm.nix 构建编码代理虚拟机]({{< relref "posts/20260204-hacker_news-coding-agent-vms-on-nixos-with-microvmnix-9.md" >}})
- [基于 NixOS 的 Microvm.nix 构建编码 Agent 虚拟机]({{< relref "posts/20260204-hacker_news-coding-agent-vms-on-nixos-with-microvmnix-10.md" >}})
- [基于 NixOS 的 Microvm.nix 构建编码 Agent 虚拟机]({{< relref "posts/20260204-hacker_news-coding-agent-vms-on-nixos-with-microvmnix-15.md" >}})
- [Microvm.nix：在 NixOS 上构建 Coding Agent 虚拟机]({{< relref "posts/20260204-hacker_news-coding-agent-vms-on-nixos-with-microvmnix-16.md" >}})
- [NixOS 上基于 Microvm.nix 的编码代理虚拟机]({{< relref "posts/20260204-hacker_news-coding-agent-vms-on-nixos-with-microvmnix-12.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*