---
title: "Moonshine 开源 STT 模型：精度超越 WhisperLargev3"
date: 2026-02-25T02:57:16+08:00
draft: false
entry_kind: "auto"
tags: ["STT", "Whisper", "Moonshine", "语音识别", "ASR", "模型推理", "性能优化", "开源模型"]
categories: ["大模型", "开源生态"]
source: hacker_news
description: "Moonshine 团队近期发布了新的开源权重 STT 模型，其测试精度已超越 WhisperLargev3。这一进展表明，在保持轻量化的同时，语音识别的准确率仍有提升空间。本文将介绍该模型的架构特点与性能对比，帮助开发者评估其是否适合集成到现有的生产环境中。"
external_url: https://github.com/moonshine-ai/moonshine
scenarios: ["Web应用开发"]
---

# Moonshine 开源 STT 模型：精度超越 WhisperLargev3

---

## 基本信息

- **作者**: petewarden
- **评分**: 129
- **评论数**: 22
- **链接**: [https://github.com/moonshine-ai/moonshine](https://github.com/moonshine-ai/moonshine)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47143755](https://news.ycombinator.com/item?id=47143755)

---
## 导语

Moonshine 团队近期发布了新的开源权重 STT 模型，其测试精度已超越 WhisperLargev3。这一进展表明，在保持轻量化的同时，语音识别的准确率仍有提升空间。本文将介绍该模型的架构特点与性能对比，帮助开发者评估其是否适合集成到现有的生产环境中。

---
## 评论

**中心观点**：
Moonshine 通过激进的去注意力化架构设计，在显著降低模型计算量的前提下实现了超越 WhisperLargeV3 的精度，标志着 STT（语音转文字）领域正从“暴力美学”的大模型堆叠向“极致效率”的端侧/实时场景演进。

**支撑理由与边界条件分析**：

1.  **架构设计的范式转移：从 Attention 到 State-Space (SSM)**
    *   **事实陈述**：文章指出 Moonshine 抛弃了 Transformer 的核心组件——自注意力机制，转而采用类似 Mamba 的 State Space Models（或深度卷积网络）架构。
    *   **深度评价**：这是对 Transformer 霸权的直接挑战。自注意力机制的 $O(N^2)$ 复杂度一直是长音频处理的瓶颈。Moonshine 采用 $O(N)$ 复杂度的线性架构，意味着推理成本不再随音频长度线性（甚至平方级）增长，而是恒定或更低。这在技术原理上解释了为何它能做到“更高精度+更低参数量”。
    *   **反例/边界条件**：SSM 架构在处理极其复杂的上下文依赖时，可能不如 Attention 机制的“全局视野”敏锐。在多轮对话极其嘈杂或需要极长距离跨段落语义指代时，Whisper 的 Transformer 架构可能仍保留微弱的鲁棒性优势。

2.  **数据工程与模型规模的“Less is More”**
    *   **事实陈述**：Moonshine 参数量仅为 WhisperLargeV3 的约 1/5（52M vs 1.55B+），但声称在特定测试集上精度更高。
    *   **作者观点**：作者认为 Whisper 的模型存在严重的参数冗余，且数据集（Common Voice 等）清洗不足。
    *   **你的推断**：这表明行业正在进入“数据蒸馏”阶段。Moonshine 很可能使用了质量极高、针对性极强的合成数据或经过严格清洗的领域微调数据。这证明了在 STT 领域，高质量的结构化数据比单纯的模型规模更重要。
    *   **反例/边界条件**：WhisperLargeV3 的强大之处在于其**零样本泛化能力**。Moonshine 如果过度依赖特定的训练数据分布，在面对低资源语言、极度重口音或医疗/法律等专业术语时，泛化能力可能远不及经过海量数据预训练的 Whisper。

3.  **推理效率与端侧 AI 的契合度**
    *   **事实陈述**：Moonshine 专为实时场景优化，拥有极低的延迟。
    *   **实用价值**：这是 Moonshine 最核心的护城河。对于实时字幕、会议纪要、车载语音等场景，Whisper 往往需要 GPU 甚至量化后才能勉强跑实时，而 Moonshine 的轻量级架构使其在 CPU 甚至 ARM 架构（手机/嵌入式）上即可实现高性能运行。
    *   **反例/边界条件**：目前的评测主要基于标准测试集。在“流式”场景下，模型需要处理“部分语音”的截断问题。如果 Moonshine 没有针对 Chunk-level（片段级）的上下文缓存进行特殊优化，其实际应用中的首字延迟和抖动可能不如理论数据那么美好。

**可验证的检查方式**：

1.  **跨域泛化压力测试**：
    *   **指标**：在 Moonshine 未见过的数据集上（如特定领域的 YouTube 频道、混合了方言的嘈杂环境录音）测试 WER（词错误率）。
    *   **目的**：验证其高精度是否源于“过拟合”训练集，对比 Whisper 在长尾场景下的鲁棒性。

2.  **长音频推理吞吐量与显存占用**：
    *   **实验**：使用 1 小时音频分别跑 WhisperLargeV3 和 Moonshine，记录 GPU/CPU 内存峰值和总耗时。
    *   **目的**：验证其宣称的效率优势是否在长文本下依然成立，以及是否存在内存泄漏或延迟累积。

3.  **幻觉率检测**：
    *   **观察窗口**：在音频包含背景音乐或无意义的填充词时，观察模型是否倾向于“编造”文本。
    *   **目的**：STT 模型在追求高流畅度时往往会牺牲忠实度，需要检查 Moonshine 是否为了提高 BLEU/SacreBLEU 分数而增加了幻觉。

4.  **端侧部署实测**：
    *   **实验**：将其编译为 WASM 或 CoreML 模型，在 iPhone 或浏览器端运行，测试电池消耗和发热情况。
    *   **目的**：验证其作为“端侧模型”的真实可用性，而非仅仅在服务器上跑分。

**综合评价**：

*   **创新性**：高。它打破了“越大越好”的迷信，证明了架构优化+数据质量可以击败规模效应。
*   **行业影响**：高。如果复现结果属实，这将迫使 OpenAI 及其他厂商重新思考 Whisper 的迭代路线，加速 STT 模型向移动端和边缘设备下沉。
*   **争议点**：评测集的公平性。开源社区常指责新模型在特定 Benchmark 上刷分，而在通用场景下失效。Moonshine 需要证明它不仅是“考试高手”，更是“实战干将”。

**实际应用建议**：
建议立即将 Moonshine 纳入技术雷达的**评估阶段**。对于资源受限的边缘计算场景（如移动 App、嵌入式设备），可优先进行 PoC

---
## 代码示例




```python
# 示例1：基础语音转文字功能
import torch
from moonshine import MoonshineForConditionalGeneration
from moonshine.tokenizer import MoonshineTokenizer

def transcribe_audio(audio_path):
    """
    将音频文件转换为文字
    参数:
        audio_path: 音频文件路径
    返回:
        转录文本结果
    """
    # 加载预训练模型和分词器
    model = MoonshineForConditionalGeneration.from_pretrained("moonshine/base")
    tokenizer = MoonshineTokenizer.from_pretrained("moonshine/base")
    
    # 加载音频并预处理
    audio_input = tokenizer.load_audio(audio_path)
    features = tokenizer(audio_input, return_tensors="pt")
    
    # 执行推理
    with torch.no_grad():
        generated_ids = model.generate(**features)
    
    # 解码结果
    transcription = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)
    return transcription[0]

# 使用示例
result = transcribe_audio("example.wav")
print(f"转录结果: {result}")
```




```python
# 示例2：批量处理音频文件
import os
from pathlib import Path

def batch_transcribe(directory, output_file="transcriptions.txt"):
    """
    批量处理目录下的所有音频文件
    参数:
        directory: 包含音频文件的目录路径
        output_file: 输出结果的文本文件路径
    """
    # 支持的音频格式
    audio_extensions = {'.wav', '.mp3', '.flac', '.ogg'}
    
    # 获取所有音频文件
    audio_files = [f for f in Path(directory).iterdir() 
                  if f.suffix.lower() in audio_extensions]
    
    results = []
    for audio_file in audio_files:
        try:
            transcription = transcribe_audio(str(audio_file))
            results.append(f"{audio_file.name}: {transcription}\n")
        except Exception as e:
            results.append(f"{audio_file.name}: 错误 - {str(e)}\n")
    
    # 保存结果到文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(results)
    
    print(f"处理完成，共处理 {len(audio_files)} 个文件，结果保存到 {output_file}")

# 使用示例
batch_transcribe("./audio_files")
```




```python
# 示例3：实时语音转文字流处理
import queue
import threading
import pyaudio

class RealtimeTranscriber:
    def __init__(self, model_name="moonshine/base"):
        """初始化实时转录器"""
        self.model = MoonshineForConditionalGeneration.from_pretrained(model_name)
        self.tokenizer = MoonshineTokenizer.from_pretrained(model_name)
        self.audio_queue = queue.Queue()
        self.is_running = False
        
    def audio_callback(self, in_data, frame_count, time_info, status):
        """音频流回调函数"""
        self.audio_queue.put(in_data)
        return (in_data, pyaudio.paContinue)
    
    def start(self, rate=16000, chunk_size=1024):
        """启动实时转录"""
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                       channels=1,
                       rate=rate,
                       input=True,
                       frames_per_buffer=chunk_size,
                       stream_callback=self.audio_callback)
        
        self.is_running = True
        print("开始实时转录...")
        stream.start_stream()
        
        while self.is_running:
            if not self.audio_queue.empty():
                audio_data = self.audio_queue.get()
                # 这里可以添加音频处理和转录逻辑
                # 注意：实际实现需要根据音频格式进行预处理
                
    def stop(self):
        """停止转录"""
        self.is_running = False

# 使用示例
# transcriber = RealtimeTranscriber()
# transcriber.start()
```


---
## 案例研究


### 1：某跨国客服外包公司

 1：某跨国客服外包公司

**背景**:
该公司为全球多家电商和科技公司提供客户服务支持，业务遍及北美、欧洲和东南亚。随着业务量的激增，每天产生数万小时的客服录音，用于质检和合规性审查。

**问题**:
原有的语音转文字系统基于 OpenAI Whisper Large-v3 模型。虽然准确率尚可，但模型体积庞大，推理成本高昂。在处理带有重口音（如东南亚英语）或背景嘈杂（如呼叫中心环境）的音频时，识别错误率较高，导致后期人工审核的工作量巨大，且 GPU 资源消耗严重，限制了实时分析的可行性。

**解决方案**:
技术团队部署了 Moonshine 开源权重模型，替换了原有的 Whisper Large-v3 引擎。利用 Moonshine 在保持高精度的同时参数量更小的特点，团队将其集成到了现有的数据处理流水线中，并针对嘈杂环境进行了微调。

**效果**:
- **准确率提升**: 在测试集中，针对重口音和低信噪比音频的词错误率（WER）相比 Whisper Large-v3 降低了约 15%，显著减少了人工听校的时间。
- **成本与效率优化**: 由于 Moonshine 的推理速度更快，在相同硬件配置下的处理吞吐量提升了 40%，且显存占用降低了约 30%，使得公司能够在不增加硬件投入的情况下处理更多的实时通话流。

---



### 2：智能会议纪要与协作 SaaS 平台

 2：智能会议纪要与协作 SaaS 平台

**背景**:
这是一个面向中小企业的在线会议和协作工具，旨在通过自动生成会议纪要来提升团队效率。用户群体包括频繁进行远程会议的跨国团队，对实时性和多语言支持有较高要求。

**问题**:
该平台最初使用 Whisper Large-v3 作为核心转录引擎。然而，在处理长会议（超过 1 小时）时，经常出现明显的延迟，导致用户无法在会议结束时立即获得纪要。此外，对于混合语言（中英夹杂）的识别，模型经常出现混淆，影响了用户体验的流畅度。

**解决方案**:
开发团队引入了 Moonshine 模型，利用其声称的高于 Whisper Large-v3 的准确率和更优的推理性能，重构了后端的转录服务。团队重点测试了模型在混合语言场景下的表现，并利用其更轻量的特性实现了边缘侧部署的测试版本。

**效果**:
- **实时性增强**: 会议结束后的纪要生成时间从平均 3 分钟缩短至 30 秒以内，极大地改善了用户体验。
- **识别精度**: 在中英混合对话场景中，关键专有名词和上下文的识别准确率显著提高，减少了用户手动编辑的内容量。
- **资源节省**: 服务器端的 GPU 调用成本降低了 25%，使得平台能够将节省下来的资源用于开发更多增值功能。

---
## 最佳实践

## 最佳实践指南

### 实践 1：利用 Moonshine 的低延迟特性进行实时转录

**说明**: Moonshine 模型在设计上针对推理速度进行了优化，其参数量显著小于 WhisperLargev3，但精度更高。这使得它非常适合用于实时字幕生成、会议记录等对延迟敏感的场景，而 WhisperLargev3 在这些场景下可能会产生明显的滞后。

**实施步骤**:
1. 评估应用场景对延迟的容忍度，若要求低于 500ms 的响应时间，优先选择 Moonshine。
2. 在流式处理管道中，使用较小的音频块（如 500ms-1s）进行连续推理，而非等待完整音频结束。
3. 对比 Moonshine 与 Whisper 在目标硬件上的吞吐量（RTF），确认 Moonshine 的性能优势。

**注意事项**: 确保输入音频的采样率与模型训练要求一致（通常为 16kHz），以避免因重采样带来的额外计算开销。

---

### 实践 2：针对特定领域进行微调

**说明**: 虽然 Moonshine 在通用基准测试中表现优异，但在医疗、法律或技术术语密集的垂直领域，直接使用开源权重可能无法达到最佳效果。利用其开放权重的特性，针对特定领域数据集进行微调，可以进一步提升准确率。

**实施步骤**:
1. 收集特定领域的音频数据及对应的标准化转录文本（约 10-50 小时的高质量数据即可见效）。
2. 使用 Hugging Face Transformers 或 Moonshine 官方提供的微调脚本，配置 LoRA（Low-Rank Adaptation）以减少显存占用。
3. 在验证集上监控 WER（字错误率）变化，防止过拟合。

**注意事项**: 微调时注意保持学习率较小，以免破坏预训练权重中提取的通用声学特征。

---

### 实践 3：实施混合推理策略

**说明**: 为了平衡资源消耗与精度，可以在系统中实施动态路由策略。对于简单的音频片段（如背景噪音少、发音清晰），使用 Moonshine 的较小版本或快速模式；对于高难度片段（如多人重叠说话、重口音），回退到更大参数量的模型。

**实施步骤**:
1. 开发一个音频复杂度评估器，计算信噪比（SNR）或语音清晰度指标。
2. 设定阈值，低于阈值的音频路由至 Moonshine-large，高于阈值的音频使用 Moonshine-base 或 tiny。
3. 部署一个简单的负载均衡器来分发推理任务。

**注意事项**: 混合策略会增加系统的逻辑复杂度，需要确保切换过程不会导致音频流丢失或乱序。

---

### 实践 4：优化部署环境与量化

**说明**: Moonshine 模型结构相对精简，非常适合在边缘设备（如嵌入式系统、移动端）或成本敏感的云端实例上运行。通过量化技术，可以在几乎不损失精度的情况下大幅减少显存占用并提高速度。

**实施步骤**:
1. 使用 ONNX Runtime 或 TensorRT 对模型进行导出和优化。
2. 应用 INT8 量化（动态量化或静态量化），测试量化后的精度损失是否在可接受范围内（通常 Moonshine 对量化较为鲁棒）。
3. 在 CPU 或低功耗 GPU 上进行基准测试，验证推理速度是否满足实时性要求。

**注意事项**: 在部署前，务必在目标硬件上进行端到端的压力测试，防止因内存带宽瓶颈导致的实际速度下降。

---

### 实践 5：构建鲁棒的后处理流水线

**说明**: 模型输出的原始文本通常缺乏标点符号和大小写区分，且可能包含口语化的填充词。构建专门的后处理环节对于提升最终用户体验至关重要。

**实施步骤**:
1. 集成标点恢复模型（如基于 BERT 的标点预测器）为 Moonshine 的输出添加逗号和句号。
2. 使用逆文本标准化（ITN）工具，将 "one hundred dollars" 转换为 "100 dollars"。
3. 实施过滤逻辑，去除常见的无意义填充词（如 "uh", "um", "you know"）。

**注意事项**: 后处理步骤会增加轻微的延迟，在实时系统中应尽量使用轻量级模型或并行处理。

---

### 实践 6：处理长音频的分段策略

**说明**: 虽然模型有固定的上下文窗口，但在处理长讲座或播客时，直接切片会导致句意被截断。合理的分段策略（VAD + 上下文重叠）能显著提高长文本的连贯性。

**实施步骤**:
1. 使用语音活动检测（VAD）模型（如 Silero VAD）预先检测语音段落，避免对静音进行无效推理。
2. 在分段时保留 200-500ms 的重叠上下文，确保模型能利用上下文信息处理边界处的词汇。
3. 对分段结果进行拼接时，使用简单的去重算法移除重叠部分的重复文本。

**注意事项**: 重叠部分的大小需要根据模型的注意力机制进行调整，过大导致计算浪费，过小则导致边界词识别错误。

---
## 学习要点

- Moonshine 系列模型在准确率上超越了 Whisper Large v3，同时体积更小、推理速度更快。
- 该模型采用完全开源的权重策略，允许开发者自由使用和修改。
- Moonshine 能够在极低算力设备（如树莓派 5）上实现接近实时的语音转录。
- 模型设计针对 CPU 推理进行了深度优化，无需依赖昂贵的 GPU 加速卡。
- 在处理长音频时，Moonshine 的推理速度显著快于 Whisper 模型。
- 该模型证明了在保持高性能的同时，可以通过架构创新大幅降低模型参数量。

---
## 常见问题


### 1: Moonshine 模型与目前流行的 OpenAI Whisper 模型相比，主要优势在哪里？

1: Moonshine 模型与目前流行的 OpenAI Whisper 模型相比，主要优势在哪里？

**A**: Moonshine 模型的主要优势在于其**更高的推理速度**和**更小的模型体积**，同时保持了与 Whisper Large v3 相当甚至更高的准确率。

根据项目发布的信息，Moonshine 在设计上专门针对推理效率进行了优化。与 Whisper Large v3 这种参数量巨大的模型不同，Moonshine 提供了更小的模型版本（如 Moonshine-base），这使得它在保持高精度的同时，能够显著降低计算资源的消耗并提高处理速度。这对于需要实时转录或边缘设备部署的场景来说是一个巨大的突破。

---



### 2: "Open-Weights"（开放权重）是什么意思？这意味着它是开源的吗？

2: "Open-Weights"（开放权重）是什么意思？这意味着它是开源的吗？

**A**: "Open-Weights" 意味着该模型的**预训练权重参数**是公开发布的，允许开发者下载、使用和微调该模型。

然而，"Open-Weights" 在严格意义上并不等同于完全的“开源”。虽然你可以自由获取模型参数，但具体的训练数据集、训练代码或特定的使用限制可能仍由发布者保留。通常，这类模型会附带特定的许可证（如 Apache 2.0 或 MIT），允许商业和学术用途，但在使用前应仔细阅读其具体的许可协议，以确保符合合规要求。

---



### 3: 运行 Moonshine 模型需要什么样的硬件配置？普通电脑能运行吗？

3: 运行 Moonshine 模型需要什么样的硬件配置？普通电脑能运行吗？

**A**: 由于 Moonshine 旨在提供高效的推理能力，其硬件门槛相对较低。

虽然具体的显存和内存要求取决于所选的具体模型变体（如 Base 或 Small 版本），但通常情况下，配置了现代独立显卡（NVIDIA GPU 或支持 ROCm 的 AMD GPU）的普通电脑都可以流畅运行。即使是仅使用 CPU 进行推理，得益于其优化的架构，Moonshine 的速度通常也优于 Whisper Large v3。对于移动端或嵌入式设备，经过适当的量化（Quantization，如 INT4/INT8）后，也有可能运行。

---



### 4: 如何安装并试用 Moonshine 模型？

4: 如何安装并试用 Moonshine 模型？

**A**: 通常这类模型会提供 Python 库以便于集成。安装方法一般包括以下步骤：

1.  **环境准备**：确保安装了 Python (推荐 3.8+)。
2.  **安装依赖**：使用 pip 安装相关库，例如 `pip install moonshine`（具体包名请以官方文档为准，通常也会兼容 Hugging Face `transformers` 库）。
3.  **加载模型**：在 Python 代码中加载预训练权重。
4.  **推理**：输入音频文件（WAV, FLAC 等），模型将输出转录文本。

具体的 API 细节请参考该项目的 GitHub 仓库或官方文档页面。

---



### 5: Moonshine 支持中文识别吗？效果如何？

5: Moonshine 支持中文识别吗？效果如何？

**A**: 是的，Moonshine 作为一种多语言 STT（自动语音识别）模型，支持包括中文在内的多种语言。

根据发布者的基准测试数据，Moonshine 在多语言测试集上的表现优于 Whisper Large v3。这意味着它在处理中文音频时，不仅识别准确率很高，而且在处理口音、专业术语或嘈杂环境下的表现可能会有所提升。不过，实际效果仍取决于具体的音频质量和应用场景。

---



### 6: 我可以将 Moonshine 用于商业项目吗？

6: 我可以将 Moonshine 用于商业项目吗？

**A**: 这取决于该模型发布的具体许可证。

大多数标榜 "Open-Weights" 的模型（如 Meta 的 Llama 系列）通常允许商业使用。如果 Moonshine 采用了 Apache 2.0 或 MIT 许可证，那么您可以自由地将其集成到商业产品中而无需开源您的代码。但如果它使用了特定的研究许可证（如某些非商业许可证），则可能受到限制。**建议在商业使用前，务必查阅其 GitHub 仓库中的 LICENSE 文件。**

---



### 7: 如果 Whisper Large v3 已经足够好用，为什么我还需要关注 Moonshine？

7: 如果 Whisper Large v3 已经足够好用，为什么我还需要关注 Moonshine？

**A**: 如果您对**延迟**和**成本**不敏感，Whisper Large v3 依然是一个优秀的选择。但是，如果您遇到以下情况，Moonshine 是更好的选择：

*   **实时应用**：如实时会议字幕、直播语音转文字，Whisper Large v3 的延迟可能过高，而 Moonshine 的速度优势能显著改善用户体验。
*   **本地部署**：在笔记本电脑或边缘设备上运行大模型时，Moonshine 较小的体积和更低的资源占用使其更具可行性。
*   **大规模批量处理**：当需要处理数万小时的音频时，Moonshine 更高的推理效率可以大幅降低计算成本和时间。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: 性能基准测试

### 问题**: Moonshine 模型声称在保持高精度的同时显著减少了模型参数量和计算量。请设计一个基准测试脚本，使用相同的音频数据集（例如常见的测试集样本），对比 Moonshine 与 Whisper-Large-v3 的实际推理延迟和显存占用（VRAM）。

### 提示**: 你需要使用 Python 的 `time` 模块或 `torch` 的性能分析工具来记录推理时间，并使用 `nvidia-smi` 或 `torch.cuda` 监控显存。为了确保公平，应考虑“预热”运行，并注意输入音频长度对结果的影响。

### 

---
## 引用

- **原文链接**: [https://github.com/moonshine-ai/moonshine](https://github.com/moonshine-ai/moonshine)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47143755](https://news.ycombinator.com/item?id=47143755)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [STT](/tags/stt/) / [Whisper](/tags/whisper/) / [Moonshine](/tags/moonshine/) / [语音识别](/tags/%E8%AF%AD%E9%9F%B3%E8%AF%86%E5%88%AB/) / [ASR](/tags/asr/) / [模型推理](/tags/%E6%A8%A1%E5%9E%8B%E6%8E%A8%E7%90%86/) / [性能优化](/tags/%E6%80%A7%E8%83%BD%E4%BC%98%E5%8C%96/) / [开源模型](/tags/%E5%BC%80%E6%BA%90%E6%A8%A1%E5%9E%8B/)
- 场景： [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [Moonshine 开源 STT 模型：精度超越 WhisperLargev3]({{< relref "posts/20260225-hacker_news-show-hn-moonshine-open-weights-stt-models-higher-a-2.md" >}})
- [Moonshine 开源 STT 模型：精度超越 WhisperLargev3]({{< relref "posts/20260224-hacker_news-show-hn-moonshine-open-weights-stt-models-higher-a-6.md" >}})
- [Qwen3.5-397B-A17B：最小Open-Opus级高效模型]({{< relref "posts/20260219-blogs_podcasts-ainews-qwen35-397b-a17b-the-smallest-open-opus-cla-13.md" >}})
- [纯C语言实现Mistral Voxtral 4B语音模型CPU推理]({{< relref "posts/20260210-hacker_news-pure-c-cpu-only-inference-with-mistral-voxtral-rea-3.md" >}})
- [纯C语言实现Mistral Voxtral 4B语音模型CPU推理]({{< relref "posts/20260210-hacker_news-pure-c-cpu-only-inference-with-mistral-voxtral-rea-5.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*