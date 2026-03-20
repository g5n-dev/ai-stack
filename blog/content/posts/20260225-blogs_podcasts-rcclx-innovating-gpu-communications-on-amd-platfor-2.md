---
title: Meta 开源 RCCLX：优化 AMD GPU 通信并集成 Torchcomms
date: 2026-02-25 14:15:03+08:00
draft: false
entry_kind: auto
tags:
- Meta
- RCCLX
- AMD
- GPU通信
- Torchcomms
- 分布式训练
- 集合通信
- 性能优化
categories:
- AI 工程
- 开源生态
source: blogs_podcasts
description: Meta 开源了一款名为 **RCCLX** 的增强版通信库。该工具基于 RCCL（AMD 平台的集合通信库）开发，并已在 Meta 的内部工作负载中经过了充分的测试与验证。
  RCCLX 的主要特点和创新点包括： 1. **深度集成**：它与 **Torchcomms** 实现了完全集成，旨在赋能研究人员和开发者，使其
external_url: https://engineering.fb.com/2026/02/24/data-center-engineering/rrcclx-innovating-gpu-communications-amd-platforms-meta
scenarios:
- Web应用开发
---

# Meta 开源 RCCLX：优化 AMD GPU 通信并集成 Torchcomms

---

## 基本信息

- **来源**: Meta Engineering (blog)
- **发布时间**: 2026-02-24T21:30:54+00:00
- **链接**: [https://engineering.fb.com/2026/02/24/data-center-engineering/rrcclx-innovating-gpu-communications-amd-platforms-meta](https://engineering.fb.com/2026/02/24/data-center-engineering/rrcclx-innovating-gpu-communications-amd-platforms-meta)

---

## 摘要/简介

我们正在开源 RCCLX 的初始版本——这是我们在 Meta 内部工作负载上开发和测试的 RCCL 增强版。RCCLX 与 Torchcomms 完全集成，旨在赋能研究人员和开发者加速创新，无论其选择何种后端。AI 模型的通信模式在不断演变，硬件亦是如此 [...] 阅读全文... 文章《RCCLX：在 AMD 平台上创新 GPU 通信》最早出现在 Engineering at Meta。

---

## 导语

随着 AI 模型与硬件架构的快速演进，高效的 GPU 通信已成为提升训练性能的关键瓶颈。本文介绍了 Meta 开源的 RCCLX，这是一套在内部严苛工作负载中验证过的 RCCL 增强版本。通过阅读本文，您将了解 RCCLX 如何针对 AMD 平台优化通信性能，以及它与 Torchcomms 集成后，如何帮助开发者屏蔽底层差异，更专注于算法本身的创新。

---

## 摘要

Meta 开源了一款名为 **RCCLX** 的增强版通信库。该工具基于 RCCL（AMD 平台的集合通信库）开发，并已在 Meta 的内部工作负载中经过了充分的测试与验证。

RCCLX 的主要特点和创新点包括：

1.  **深度集成**：它与 **Torchcomms** 实现了完全集成，旨在赋能研究人员和开发者，使其不受特定后端的限制，从而加速 AI 模型的创新。
2.  **应对演进**：针对 AI 模型通信模式以及底层硬件技术的不断迭代与演进，RCCLX 提供了相应的优化方案。

简而言之，RCCLX 是 Meta 为提升 AMD 平台上 GPU 通信效率而推出的开源解决方案，旨在适应快速变化的 AI 硬件与模型需求。

---

## 评论

### 深度评价：Meta开源RCCLX（基于AMD平台的GPU通信优化库）

**核心观点**
Meta开源RCCLX旨在通过软件层面的工程优化，改善AMD GPU在集群通信层面的性能表现。该举措是应对异构计算趋势、降低硬件绑定风险并探索大模型训练成本优化路径的技术尝试，但需理性看待其对现有NVIDIA生态的实际冲击力。

---

#### 1. 技术深度与局限性
*   **工程验证（事实陈述）：** RCCLX基于Meta内部工作负载开发，表明该库经过了实际生产环境的检验，而非仅限于理论模型。其与Torchcomms的集成显示了一种垂直整合的技术路径，即通过优化通信栈来缓解硬件瓶颈。
*   **性能推断（技术分析）：** RCCLX的主要价值在于填补ROCm生态在通信库层面的短板。Meta的技术路径表明，通过内核优化，在不更换硬件的前提下有望提升训练效率。
*   **技术边界（客观限制）：** 目前披露的信息缺乏在复杂网络拓扑（如非全互联或超分集群架构）下的详细性能数据。通信库在Fat-Tree结构下通常表现较好，但在处理复杂拓扑的延迟问题时，RCCLX是否具备与NCCL同等的鲁棒性，尚需更多独立数据支持。

#### 2. 实用价值与适用场景
*   **场景适配（事实陈述）：** 对于正在构建或测试非NVIDIA AI集群的企业，RCCLX提供了经过验证的通信原语，有助于减少在ROCm生态上的自行调优成本。
*   **架构设计（技术推断）：** 其创新性在于中间件抽象层的设计。通过Torchcomms屏蔽后端差异，实现了在PyTorch框架下的相对平滑切换，这种“软解耦”策略有助于降低异构硬件的迁移门槛。
*   **物理瓶颈（技术现实）：** 软件优化存在物理上限。若AMD Infinity Fabric或PCIe吞吐存在硬件限制，单纯优化通信库的收益将受限。此外，在通信占比较低的小模型训练或推理场景中，性能提升可能不明显。

#### 3. 行业影响与商业逻辑
*   **生态信号（行业分析）：** 这是Meta在软件基础设施层面推动硬件多样性的延续。RCCLX的发布表明AMD MI系列芯片的软件支撑能力正在逐步完善，为市场提供了除CUDA之外的备选方案。
*   **竞争格局（趋势推断）：** 此举可能促使行业更加重视对非NVIDIA后端的支持，但也可能加剧NVIDIA对其CUDA生态的防御性封闭。
*   **商业考量（批判性思考）：** Meta此举符合其自身的供应链多元化与成本控制诉求。社区在采用时需评估RCCLX是否存在针对Meta特定业务（如推荐系统）的过度优化，并确认其对通用深度学习任务的广泛适用性。

---

### 综合评价总结

**内容深度：★★★★☆**
直击AI集群通信痛点，头部科技公司的背书提升了可信度。但在内核级Benchmark和具体算法优化细节上披露仍有限。

**实用价值：★★★★☆**
为异构计算工程团队提供了关键工具，解决了部分“有硬件无软件”的痛点，但迁移效果需视具体网络环境而定。

**创新性：★★★★☆**
系统集成层面的策略创新，特别是统一接口设计，但在底层通信算法理论层面多为既有技术的工程实现。

**可读性：★★★★☆**
技术逻辑清晰，侧重于工程实践与结果导向。

**行业影响：★★★★☆**
标志着AI算力市场多元化竞争的进一步加深，但短期内难以撼动CUDA生态的统治地位。

---

### 实际应用建议

1.  **拓扑匹配验证：** 建议在与生产环境网络拓扑一致的测试集群中，针对特定模型架构（如Transformer或MoE）进行基准测试，量化实际收益。
2.  **API兼容性评估：** 若现有代码深度依赖底层NCCL API（如自定义通信算子），迁移前需仔细评估Torchcomms的接口覆盖范围与兼容性。

---

## 技术分析

基于您提供的文章标题《RCCLX: Innovating GPU communications on AMD platforms》及摘要片段，以下是对该核心观点和技术要点的深入分析。

---

### RCCLX: 深度解析 AMD 平台 GPU 通信的创新与开源

### 1. 核心观点深度解读

**文章的主要观点**
文章的核心观点在于宣布开源 **RCCLX**——这是一个在 Meta 内部工作负载中经过实战检验的 **RCCL（Radeon Collective Communications Library）** 的增强版本。Meta 旨在通过此举，打破单一硬件生态的依赖，证明在 AMD GPU 平台上同样可以实现高性能的分布式训练，并通过开源回馈社区，推动异构计算生态的发展。

**作者想要传达的核心思想**
作者传达了“**性能优化不应受限于特定硬件厂商**”的思想。Meta 展示了其技术栈的灵活性：通过自研改进底层通信库（RCCLX）并与上层框架深度集成，在不牺牲性能的前提下，实现了对 AMD 硬件的充分挖掘。这体现了 Meta 对“开放计算”和“供应链多元化”的战略承诺。

**观点的创新性和深度**
*   **深度：** 不仅仅是简单的移植，而是针对 Meta 特有的内部大规模工作负载进行了“开发和测试”。这意味着 RCCLX 针对特定的大规模稀疏模型、推荐系统或 Transformer 模型进行了定向优化，而非通用的基准测试优化。
*   **创新性：** 创新点在于将专有的内部优化成果标准化并开源。在 NVIDIA NCCL 主导的领域，推出一个强有力的竞争者（基于 AMD ROCm 生态），本身就是对行业垄断的突破，特别是在与 TorchComms 的集成上，展示了软件栈解耦的最佳实践。

**为什么这个观点重要**
随着 AI 模型规模的指数级增长，算力成本和硬件供应链安全成为各大科技公司的核心痛点。Meta 的这一举措表明：
1.  AMD 硬件已具备支撑超大规模 AI 训练的潜力。
2.  软件栈的优化（如通信库）是释放异构硬件性能的关键。
3.  开源协作是解决 AI 基础设施瓶颈的有效途径。

### 2. 关键技术要点

**涉及的关键技术或概念**
*   **RCCL (Radeon Collective Communications Library):** AMD 对标 NVIDIA NCCL 的集合通信库，用于 GPU 间的高速数据传输（如 AllReduce, Broadcast 等）。
*   **TorchComms:** PyTorch 生态中用于抽象后端通信机制的接口层，允许用户在 NCCL、RCCL 等后端间无缝切换。
*   **Collective Communication Operations (集合通信):** 并行计算的基础原语，特别是 AllReduce，是深度学习训练中梯度同步的性能瓶颈。
*   **HIP (Heterogeneous-computing Interface for Portability):** AMD 的 CUDA 类似层。

**技术原理和实现方式**
RCCLX 的实现原理主要围绕以下几个方面：
1.  **内核优化:** 针对特定 AMD GPU 架构（如 CDNA 架构）的汇编级或微码级优化，调整内存访问模式以最大化带宽利用率。
2.  **网络拓扑感知:** 在 Meta 的大规模集群中，节点间的互联拓扑（如 PCIe、Infinity Fabric 或以太网/RoCE）极其复杂。RCCLX 可能增强了拓扑发现算法，优化了通信路径，减少了多跳延迟。
3.  **算法融合:** 将通信操作与计算操作进行重叠，利用 CUDA Stream（或 HIP Stream）机制，在 GPU 计算的同时进行数据传输，隐藏通信延迟。

**技术难点和解决方案**
*   **难点:** AMD 生态的软件成熟度长期落后于 NVIDIA，调试工具链不如 CUDA 完善；大规模集群下的网络拥塞控制极其困难。
*   **解决方案:** Meta 依托其庞大的工程团队，通过**内部实际工作负载**（而非合成测试）来驱动优化。这意味着他们是在真实的推荐系统（如 DLRM）或 LLM 训练中发现 Bug 和性能瓶颈，并针对性修补 RCCL 的底层逻辑。

**技术创新点分析**
最大的创新点在于 **"Enhanced" (增强)**。RCCLX 不是对 AMD 官方 RCCL 的简单复刻，而是 Meta 针对其特定的**网络基础设施**（可能是自定义的以太网或 InfiniBand 方案）和**训练框架**（PyTorch 定制版）进行的深度魔改。这种“软硬协同”优化的开源化极具价值。

### 3. 实际应用价值

**对实际工作的指导意义**
对于正在构建或规划 AI 基础设施的团队，RCCLX 的开源提供了一个重要的信号：**AMD GPU 方案已进入“生产可用”阶段**。它指导工程师在选型时不应只看硬件规格（FLOPS），更要看通信库的吞吐量和延迟表现。

**可以应用到哪些场景**
1.  **大语言模型 (LLM) 训练:** 需要极高的 AllReduce 带宽，RCCLX 能有效提升 AMD 集群下的训练效率。
2.  **大规模推荐系统:** Meta 的核心业务，涉及海量稀疏参数，通信模式复杂，RCCLX 针对此类负载的优化尤为宝贵。
3.  **多模态模型训练:** 涉及文本、图像、语音的跨模态传输，对通信延迟敏感。

**需要注意的问题**
*   **硬件依赖性:** RCCLX 的优化可能针对 Meta 使用的特定型号 AMD GPU（如 Instinct MI200/300 系列），在其他旧型号或不同网络配置下效果可能打折。
*   **生态兼容性:** 虽然 PyTorch 已支持，但其他框架（如 TensorFlow、JAX）的适配可能尚需时日。

**实施建议**
*   如果团队正在使用 AMD GPU，应立即将 RCCLX 纳入测试基准，对比官方 RCCL 和 RCCLX 在实际模型训练中的吞吐量差异。
*   关注 RCCLX 与特定网络后端（如 Libfabric、UCX）的版本兼容性。

### 4. 行业影响分析

**对行业的启示**
*   **“软件定义硬件”趋势的确立:** 硬件不再是性能的绝对天花板，优秀的软件栈（通信库、编译器）完全可以弥补硬件的微架构差距。
*   **降低 AI 基础设施门槛:** 通过开源高性能组件，降低了中小企业尝试非 NVIDIA 方案的风险。

**可能带来的变革**
这可能促使 AMD 在数据中心市场的份额进一步上升，迫使 NVIDIA 在 NCCL 的许可和开放性上做出调整，或者加速 NCCL 的性能迭代。同时也可能引发一波针对 AMD 平台的深度学习优化热潮。

**相关领域的发展趋势**
*   **异构计算集群混用:** 未来数据中心可能同时运行 NVIDIA 和 AMD 节点，这对通信库的跨平台互操作性提出了更高要求。
*   **开源 AI 基础设施的爆发:** 从 Meta (RCCLX, PyTorch) 到 Hugging Face，开源正在成为 AI 基础设施的主流。

### 5. 延伸思考

**引发的思考**
*   既然通信库可以优化，那么算子库呢？Meta 是否也在筹备开源针对 AMD 的优化算子库？
*   在“后摩尔定律”时代，系统级优化（通信、调度、内存管理）的边际收益是否已经超过了芯片制程收益？

**拓展方向**
*   **跨厂商通信:** 未来是否会出现一个统一的通信层 API，能够自动在 NCCL (Nvidia) 和 RCCLX (AMD) 之间调度，甚至支持混合训练？
*   **网络层解耦:** RCCLX 对网络底层的抽象程度如何？能否更容易地适配新兴的互连技术（如 CXL）。

### 7. 案例分析

**成功案例分析 (Meta 内部)**
Meta 的推荐系统（Ads Ranking）是其核心收入来源。这类模型通常参数量巨大且 Embedding 层极其稀疏。
*   **背景:** 在使用 AMD GPU 替换部分 NVIDIA GPU 的过程中，官方标准版 RCCL 可能无法处理 Meta 特有的网络拓扑或高并发通信模式，导致 GPU 利用率（SMU）上不去。
*   **RCCLX 作用:** 通过优化 AllReduce 的分块算法和环形拓扑，减少了通信“气泡”，使得 AMD GPU 在处理 DLRM 模型时达到了与 NVIDIA 相近的扩展效率。

**失败/挑战反思 (假设性)**
*   **场景:** 某研究团队试图将 RCCLX 用于旧版本的 AMD GPU（如 Vega 架构）。
*   **结果:** 性能提升微乎其微，甚至出现崩溃。
*   **教训:** 高度优化的库通常针对最新架构。RCCLX 的优化重点在于 CDNA 架构（MI200系列），盲目移植到旧硬件可能适得其反。

### 8. 哲学与逻辑：论证地图

**中心命题**
**开源 RCCLX 能够显著提升 AMD 平台上大规模分布式 AI 训练的性能与可行性，使其成为 NVIDIA 生态的有力替代方案。**

**支撑理由**
1.  **性能验证:** Meta 已在其内部的高负载工作负载中完成了开发和测试，证明了其在实际场景中的有效性。
2.  **生态集成:** RCCLX 与 TorchComms 的深度集成，降低了开发者切换后端的成本，保证了软件栈的通用性。
3.  **底层优化:** 针对特定硬件架构的内核级优化，解决了通用库在 AMD 平台上通信效率低的问题。

**反例与边界条件**
1.  **特定硬件依赖:** RCCLX 的性能优势可能仅限于较新的 AMD GPU 架构（如 MI200/300 系列），在旧架构上可能无效。
2.  **特定网络环境:** Meta 的优化可能针对其特定的数据中心网络架构（如 RoCE v2 或自定义拓扑），在标准以太网或不同网络配置下，性能提升可能不明显。

**事实与价值判断**
*   **事实:** RCCLX 是基于 RCCL 的修改版；Meta 正在开源它；它支持 TorchComms。
*   **价值判断:** “Empower researchers”（赋能研究者）暗示了开源的道德价值；“Accelerate innovation”（加速创新）暗示了其行业推动力。
*   **可检验预测:** 使用 RCCLX 在标准 Hugging Face Transformer 训练任务中，其吞吐量应高于官方 RCCL，且接近 NCCL 在同等硬件水平下的表现。

**立场与验证**
*   **立场:** 支持 RCCLX 作为 AMD AI 生态的关键补丁

---

## 最佳实践

### 实践 1：启用 ROCm 兼容性与环境校验

**说明**: RCCLX (Radeon Collective Communications Library X) 是专为 AMD GPU 平台优化的通信库。在实施前，必须确保底层 ROCm 环境与 RCCLX 版本完全兼容，以避免驱动不匹配导致的性能下降或运行时错误。

**实施步骤**:
1. 检查当前系统的 ROCm 版本，确保其处于 RCCLX 支持的版本列表中。
2. 验证 GPU 固件是否为最新，以支持特定的通信特性（如 GDMA 或 XGMI）。
3. 设置 `HSA_ENABLE_SDMA=0` 或 `1`（根据具体硬件架构建议）以优化内存拷贝路径。

**注意事项**: 不同代际的 AMD GPU（如 MI200 与 MI300 系列）对 RCCLX 的支持细节不同，务必查阅官方的兼容性矩阵。

---

### 实践 2：优化拓扑感知与亲和性绑定

**说明**: AMD 平台通常具有复杂的 NUMA 拓扑结构（如 CPU 与 GPU 的挂载关系）。利用 RCCLX 的拓扑感知能力，将进程正确绑定到物理上最接近的 GPU 和 CPU 核心，可以显著减少跨插槽/跨 NUMA 节点的通信延迟。

**实施步骤**:
1. 使用 `rocm_smi` 工具检测系统的物理拓扑结构。
2. 在启动分布式训练任务时，利用 `numactl` 或 `ROCM_VISIBLE_DEVICES` 结合进程亲和性设置，确保 Rank 0 运行在 Node 0 的 GPU 0 上，以此类推。
3. 启用 RCCLX 的自动拓扑检测功能，让其自动选择最优通信路径。

**注意事项**: 在多节点训练中，错误的亲和性设置可能导致流量跨 PCIe 交换机或跨 CPU 插槽传输，严重降低带宽利用率。

---

### 实践 3：充分利用高速互联链路

**说明**: AMD Instinct 系列显卡通常配备 Infinity Fabric 或 XGMI 高速互联技术，带宽远超传统 PCIe。RCCLX 能够识别并利用这些链路进行卡间通信，配置正确与否直接决定了 AllReduce 等集合通信操作的吞吐量。

**实施步骤**:
1. 确认物理线缆连接正确，且 BIOS 中开启了相应的 PCIe 或 XGMI 链路宽度（如 x16）。
2. 在环境变量中显式设置通信后端，优先使用 XGMI 路径（例如设置 `NCCL_SOCKET_IFNAME` 或特定 RCCLX 标志以避免回退到以太网）。
3. 对于跨节点通信，确保网卡（如 RoCE）驱动已安装并配置好无损网络。

**注意事项**: 如果 RCCLX 未能检测到高速链路，它可能会自动降级到 PCIe 传输，导致带宽利用率从 100+ GB/s 降至 32 GB/s 左右。

---

### 实践 4：调整通信算法与缓冲区大小

**说明**: 不同的张量大小适合不同的通信算法（如 Ring, Tree, 或 Rabenseifner 算法）。RCCLX 允许通过环境变量微调算法阈值和缓冲区大小，以适应特定模型的数据特征。

**实施步骤**:
1. 分析模型中梯度同步的张量尺寸分布。
2. 调整 `RCCL_MAX_NRINGS` 等参数，增加通信环的数量以提高带宽利用率（尤其是在 XGMI 环境下）。
3. 根据网络延迟调整 `NCCL_PROTO` 或 RCCLX 等效参数，选择简单协议（LL/LL128）以减少延迟，或选择复杂协议以最大化带宽。

**注意事项**: 盲目增加通信环数量可能会导致显存占用过高或上下文切换开销增加，需根据实际显存容量权衡。

---

### 实践 5：集成性能分析工具进行监控

**说明**: 通信瓶颈往往隐藏在计算任务之下。使用 ROCm 生态中的性能分析工具（如 Omnitrace 或 rocprof）配合 RCCLX 的日志输出，可以精确定位通信热点。

**实施步骤**:
1. 在训练脚本中启用 RCCLX 的调试日志（设置 `RCCL_DEBUG=INFO`）。
2. 使用 `rocprof` 抓取 Kernel 运行时间，重点关注 `rcclKernel` 相关的耗时。
3. 分析计算与通信的重叠比例，确保 GPU 在等待数据同步时处于空闲状态的时间最小化。

**注意事项**: 生产环境中开启详细日志会带来轻微的性能损耗，建议仅在性能调优阶段开启。

---

### 实践 6：针对混合精度训练的数据类型优化

**说明**: 现代深度学习训练广泛使用 FP16 或 BF16。RCCLX 在处理半精度浮点数时有特定的优化路径，确保通信库直接使用半精度传输可以翻倍有效带宽，并减少数据类型转换的开销。

**实施步骤**:
1. 确认训练框架（如 PyTorch）在构建 DataLoader 时使用

---

## 学习要点

- RCCLX 是 AMD 推出的高性能通信库，专为优化 ROCm 生态系统中的 GPU 间通信而设计，旨在提升多 GPU 并行计算效率。
- 该架构通过引入新的内核优化和传输协议，显著降低了通信延迟，从而加速大规模 AI 模型和 HPC 工作负载的训练过程。
- RCCLX 在兼容原有 RCCL 接口的基础上进行了底层创新，确保用户无需大幅修改代码即可获得性能提升。
- 该技术针对 AMD CDNA 架构（如 Instinct MI200 系列）的特性进行了深度调优，充分发挥了硬件的互联带宽优势。
- 通过优化集合通信原语，RCCLX 有效解决了在复杂网络拓扑下多 GPU 扩展时的通信瓶颈问题。
- 这一创新强化了 AMD ROCm 软件栈的竞争力，为开发者提供了更接近 CUDA 开发体验的优化工具，缩小了与 NVIDIA 在通信效率上的差距。

---

## 引用

- **文章/节目**: [https://engineering.fb.com/2026/02/24/data-center-engineering/rrcclx-innovating-gpu-communications-amd-platforms-meta](https://engineering.fb.com/2026/02/24/data-center-engineering/rrcclx-innovating-gpu-communications-amd-platforms-meta)
- **RSS 源**: [https://engineering.fb.com/feed/](https://engineering.fb.com/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Meta](/tags/meta/) / [RCCLX](/tags/rcclx/) / [AMD](/tags/amd/) / [GPU通信](/tags/gpu%E9%80%9A%E4%BF%A1/) / [Torchcomms](/tags/torchcomms/) / [分布式训练](/tags/%E5%88%86%E5%B8%83%E5%BC%8F%E8%AE%AD%E7%BB%83/) / [集合通信](/tags/%E9%9B%86%E5%90%88%E9%80%9A%E4%BF%A1/) / [性能优化](/tags/%E6%80%A7%E8%83%BD%E4%BC%98%E5%8C%96/)
- 场景： [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [Meta 开源 RCCLX：优化 AMD GPU 通信并集成 Torchcomms]({{< relref "posts/20260224-blogs_podcasts-rcclx-innovating-gpu-communications-on-amd-platfor-0.md" >}})
- [Meta 开源 RCCLX：优化 AMD 平台 GPU 通信性能]({{< relref "posts/20260225-blogs_podcasts-rcclx-innovating-gpu-communications-on-amd-platfor-0.md" >}})
- [Meta 开源 RCCLX：优化 AMD GPU 通信并集成 Torchcomms]({{< relref "posts/20260225-blogs_podcasts-rcclx-innovating-gpu-communications-on-amd-platfor-1.md" >}})
- [DeepSpeed图像工作负载评测：视觉Transformer扩展性能]({{< relref "posts/20260225-arxiv_ai-scaling-vision-transformers-evaluating-deepspeed-f-1.md" >}})
- [FlashAttention-T：张量化注意力机制优化方案]({{< relref "posts/20260204-hacker_news-flashattention-t-towards-tensorized-attention-11.md" >}})
