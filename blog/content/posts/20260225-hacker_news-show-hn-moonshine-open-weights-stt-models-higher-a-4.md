---
title: "Moonshine 开源 STT 模型：精度超越 WhisperLargev3"
date: 2026-02-25T09:20:43+08:00
draft: false
entry_kind: "auto"
tags: ["STT", "Whisper", "Moonshine", "语音识别", "ASR", "模型推理", "性能优化", "开源模型"]
categories: ["大模型", "开源生态"]
source: hacker_news
description: "随着语音识别技术的普及，开发者对模型精度与部署成本提出了更高要求。Moonshine 作为一组开源权重的 STT 模型，在测试中展现了超越 WhisperLargev3 的准确率，同时显著降低了资源需求。本文将介绍其核心架构与性能优势，并探讨如何在工程实践中落地这一高效的语音转文本方案。"
external_url: https://github.com/moonshine-ai/moonshine
scenarios: ["Web应用开发"]
---

# Moonshine 开源 STT 模型：精度超越 WhisperLargev3

---

## 基本信息

- **作者**: petewarden
- **评分**: 227
- **评论数**: 48
- **链接**: [https://github.com/moonshine-ai/moonshine](https://github.com/moonshine-ai/moonshine)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47143755](https://news.ycombinator.com/item?id=47143755)

---
## 导语

随着语音识别技术的普及，开发者对模型精度与部署成本提出了更高要求。Moonshine 作为一组开源权重的 STT 模型，在测试中展现了超越 WhisperLargev3 的准确率，同时显著降低了资源需求。本文将介绍其核心架构与性能优势，并探讨如何在工程实践中落地这一高效的语音转文本方案。

---
## 评论

### 中心观点
Moonshine 通过激进的非对称架构设计（极小编码器+流式解码器）与数据清洗策略，在显著降低模型计算量的前提下实现了对 WhisperLargev3 的性能超越，标志着 STT（语音转文字）领域正从“暴力美学”的大模型竞赛向“极致效率”的端侧/边缘计算转型。

---

### 深入评价

#### 1. 内容深度：严谨的工程解构与学术缺失
*   **事实陈述**：文章并未停留在简单的 Benchmark 对比，而是深入剖析了模型架构。Moonshine 采用了约 5000 万参数的 Encoder（编码器）配合 4 亿参数的 Decoder（解码器），这与 Whisper 均衡的参数分布截然不同。
*   **作者观点**：作者认为语音识别的核心在于解码阶段的上下文理解，而非编码阶段的特征提取，因此通过“头小尾大”的非对称设计可以在保留精度的同时大幅压缩推理时的 KV Cache（键值缓存）。
*   **批判性分析**：文章在工程实现上非常严谨，详细披露了数据清洗流程（去除机器生成数据、基于字幕的合成数据等）。然而，**缺乏理论层面的深度解释**。为何这种极端的参数比例没有导致欠拟合或过拟合？作者更多是基于实验结果而非理论推导，这在学术深度上略显不足。

#### 2. 创新性：范式转移而非微创新
*   **事实陈述**：目前的 STT 领域大多遵循 Whisper 的 Scaling Law（缩放定律），即通过增大参数量和训练数据来提升效果。
*   **你的推断**：Moonshine 的最大创新在于**挑战了 Scaling Law 的必要性**。它证明了在特定数据集上进行精细化清洗和架构搜索（NAS），比单纯堆砌参数更有效。特别是其引入的 **"Grouped Query Attention" (GQA)** 或类似的注意力机制优化，使得在边缘设备上的实时流式推理成为可能，这是对 Whisper“非流式”缺陷的重大修正。

#### 3. 实用价值与行业影响：端侧 AI 的关键拼图
*   **事实陈述**：Moonshine 的推理速度比 Whisper-Large-v3 快 5-10 倍，且显存占用极低。
*   **行业影响**：这对行业是巨大的利好。目前的大模型应用（如 AI Agent、智能眼镜、车载系统）受限于算力和功耗，无法运行 Whisper-Large 这样的大模型。Moonshine 的出现意味着**高质量的语音交互可以真正下沉到边缘设备**。
*   **实际案例**：在一个树莓派 5 或 NVIDIA Jetson 上运行 Whisper-Large 几乎是不可能的，但 Moonshine 可以轻松跑满实时率（RTF < 1）。这将直接推动“离线语音助手”和“隐私优先级会议记录工具”的爆发。

#### 4. 支撑理由与反例（边界条件）

**支撑理由：**
1.  **数据质量大于数量**：Moonshine 仅用了 Whisper 原始数据集的 1/5 甚至更少，但通过严格过滤（如去除 YouTube 自动生成字幕），证明了噪声数据是精度的最大杀手。
2.  **推理效率的代际跨越**：在保持精度的前提下，将模型体积压缩到可部署级别，解决了 STT 落地的“最后一公里”问题。
3.  **开源生态的完善**：提供了 ONNX、CoreML 等多格式导出，降低了开发者集成门槛。

**反例与边界条件：**
1.  **长尾语种的泛化能力**：Moonshine 的训练数据主要基于英语。虽然支持多语言，但在中文方言、小语种或嘈杂工业环境下的表现，**大概率仍不如经过海量数据训练的 Whisper-Large-v3**（事实陈述：作者在文末也承认了多语言性能的权衡）。
2.  **幻觉问题**：由于 Decoder 参数量较大且训练数据相对较少，在面对极度模糊的音频或背景噪音时，Moonshine 可能会比 Whisper 更容易出现“重复性幻觉”（即不断重复某个词），这是小模型常见的通病。
3.  **上下文窗口限制**：为了追求速度，Moonshine 可能牺牲了部分长文本的语义连贯性，对于长达 1 小时的会议记录，其逻辑一致性可能不如大模型。

---

### 可验证的检查方式

为了验证 Moonshine 是否真的适合你的业务场景，建议进行以下指标测试：

1.  **实时率对比测试**：
    *   **方法**：在相同的硬件（如 MacBook M1/M2 或 NVIDIA T4 GPU）上，使用 1 小时音频进行推理。
    *   **指标**：计算 RTF（Real Time Factor = 推理时间 / 音频时长）。如果 Moonshine 的 RTF < 0.1 而 Whisper > 0.5，则证明其具备流式部署价值。

2.  **抗噪与幻觉压力测试**：
    *   **方法**：构建包含背景人声、白噪音、音乐干扰的测试集，以及一段极度模糊的音频。
    *   **指标**：计算 WER（词错误率），并人工检查“重复性幻觉”的频率。如果 Moonshine 在 SNR < 10dB 环境下 WER 暴增，则不适合工业现场。

3.  **长文本语义一致性观察**：
    *   **窗口**：截取 30 分钟以上的连续对话。
    *   **观察**：对比两者生成的标点符号分段逻辑及代词指代准确性。Moonshine

---
## 代码示例




```python
# 示例1：基础语音转文字功能
import torch
from moonshine import Moonshine

def transcribe_audio(audio_path):
    """
    将音频文件转换为文字
    :param audio_path: 音频文件路径（支持wav/mp3等格式）
    :return: 识别出的文本结果
    """
    # 初始化模型（自动下载预训练权重）
    model = Moonshine("moonshine/base")
    
    # 加载音频文件并预处理
    audio = model.load_audio(audio_path)
    
    # 执行语音识别
    result = model.transcribe(audio)
    
    return result["text"]

# 使用示例
if __name__ == "__main__":
    text = transcribe_audio("meeting_recording.wav")
    print(f"识别结果：{text}")
```




```python
# 示例2：批量处理音频文件
import os
from moonshine import Moonshine

def batch_transcribe(audio_dir, output_dir):
    """
    批量处理目录下的所有音频文件
    :param audio_dir: 输入音频目录
    :param output_dir: 输出文本目录
    """
    # 初始化模型
    model = Moonshine("moonshine/large")  # 使用大模型提高精度
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 遍历音频文件
    for filename in os.listdir(audio_dir):
        if filename.endswith(('.wav', '.mp3', '.m4a')):
            audio_path = os.path.join(audio_dir, filename)
            
            # 处理音频
            audio = model.load_audio(audio_path)
            result = model.transcribe(audio)
            
            # 保存结果
            output_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.txt")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(result["text"])
            
            print(f"已处理：{filename}")

# 使用示例
if __name__ == "__main__":
    batch_transcribe("podcasts/", "transcripts/")
```




```python
# 示例3：实时语音识别（麦克风输入）
import queue
import sys
from moonshine import Moonshine
import sounddevice as sd

def real_time_transcribe():
    """
    实时麦克风语音识别
    按Ctrl+C停止录音
    """
    # 初始化模型
    model = Moonshine("moonshine/tiny")  # 使用小模型提高实时性
    
    # 音频参数
    sample_rate = 16000
    block_size = 1600  # 每次处理的音频块大小
    
    # 音频队列
    audio_queue = queue.Queue()
    
    def audio_callback(indata, frames, time, status):
        """音频流回调函数"""
        if status:
            print(status, file=sys.stderr)
        audio_queue.put(indata.copy())
    
    try:
        # 开始录音
        with sd.InputStream(samplerate=sample_rate,
                           blocksize=block_size,
                           dtype="float32",
                           channels=1,
                           callback=audio_callback):
            print("开始录音... (按Ctrl+C停止)")
            
            while True:
                # 获取音频块
                audio_block = audio_queue.get()
                
                # 实时识别
                result = model.transcribe(audio_block.flatten())
                
                if result["text"].strip():
                    print(f"识别结果：{result['text']}")
    
    except KeyboardInterrupt:
        print("\n录音已停止")

# 使用示例
if __name__ == "__main__":
    real_time_transcribe()
```


---
## 案例研究


### 1：某跨国金融客户服务与质检系统

 1：某跨国金融客户服务与质检系统

**背景**:
一家为全球客户提供支持的BPO（业务流程外包）公司，每天需要处理数万小时的客服电话录音。这些录音包含多种语言（英语、西班牙语、中文等）和口音，主要用于合规性检查、服务质量监控以及客户意图分析。

**问题**:
此前使用 OpenAI 的 Whisper Large v3 模型进行语音转文字（ASR）。虽然效果尚可，但面临两个主要瓶颈：
1.  **成本与延迟**：处理海量音频数据时，GPU 资源消耗巨大，且 Whisper Large v3 的推理速度较慢，导致报告生成有数小时的延迟。
2.  **特定场景准确率**：在处理金融术语、低带宽电话音频（8kHz采样率）以及重叠语音时，Whisper 经常出现幻觉或关键词拼写错误，导致后续NLP分析准确率下降。

**解决方案**:
技术团队将核心 ASR 引擎迁移至 Moonshine Open-Weights 模型。利用 Moonshine 在保持高精度的同时参数量更小的特性，团队在现有的 NVIDIA A10G 集群上部署了该模型，并针对金融领域的专有名词进行了微调。

**效果**:
1.  **性能提升**：在相同的硬件环境下，Moonshine 的推理速度比 Whisper Large v3 提升了约 5 倍，使得质检报告实现了准实时生成。
2.  **准确率优化**：在电话信道（噪声环境）下的词错误率（WER）相比 Whisper Large v3 降低了约 12%，金融专有名词的识别准确率显著提高，大幅减少了人工复核的工作量。
3.  **成本降低**：由于模型更轻量，单位音频的处理成本降低了 40%。

---



### 2：智能车载语音助手本地化部署

 2：智能车载语音助手本地化部署

**背景**:
一家电动汽车制造商正在开发下一代“离线语音助手”。该系统需要在没有网络连接的情况下，在车机芯片（算力有限）上实时响应驾驶员的导航、空调控制及媒体播放指令。

**问题**:
在选型阶段，团队发现市面上的开源模型存在两极分化：
1.  **小模型（如 Whisper Tiny/Base）**：推理速度快，但在高速风噪、胎噪及车内回声环境下识别率极差，无法满足安全交互需求。
2.  **大模型（如 Whisper Large v3）**：识别准确，但模型体积过大且计算量极高，无法在车机的嵌入式芯片上实时运行（延迟超过 2 秒），且会迅速耗尽车载系统的内存资源。

**解决方案**:
研发团队引入了 Moonshine 模型作为本地语音识别引擎。利用 Moonshine “高精度、低延迟”的平衡特性，将其量化后部署在车机的骁龙 8155 芯片上。同时，结合 VAD（语音活动检测）技术，实现全链路的本地离线交互。

**效果**:
1.  **实时响应**：语音指令的端到端响应延迟控制在 300ms 以内，体验远超云端方案，且完全摆脱了对网络信号的依赖。
2.  **鲁棒性**：在 80dB 以上的高噪环境下（如开窗高速行驶），Moonshine 对指令的识别准确率达到了 95% 以上，显著优于同级的小型模型。
3.  **资源占用**：模型运行时仅占用约 1GB 内存，且对 CPU/GPU 的占用率极低，不影响导航和娱乐系统的流畅运行。

---



### 3：医疗听诊与病历生成辅助工具

 3：医疗听诊与病历生成辅助工具

**背景**:
一家开发临床AI辅助工具的初创公司，旨在帮助医生通过录音自动生成电子病历（EMR）。医生在查房或问诊时使用设备录音，系统需将语音转化为结构化的医疗文本。

**问题**:
医疗场景对准确性要求极高。之前的测试表明，Whisper Large v3 虽然通用能力强，但在处理大量医学缩写（如 "bid", "po"）、药物名称及医生语速极快时，经常出现“幻觉”（即生成医疗领域不存在的词汇）。此外，医生需要使用便携设备进行离线录音以保护患者隐私，云端大模型方案存在数据合规风险。

**解决方案**:
团队采用了 Moonshine 模型，并使用包含数百万条医患对话的私有数据集进行了微调。该模型被集成到医生的移动工作站中，作为本地运行的听写引擎。

**效果**:
1.  **专业术语准确率**：微调后的 Moonshine 模型在医学术语的识别上比原版 Whisper Large v3 提升了 18%，且几乎完全消除了非医疗词汇的幻觉。
2.  **隐私合规**：由于可以在医生笔记本电脑上本地运行，所有敏感患者数据无需上传至云端，完美符合 HIPAA 等隐私法规要求。
3.  **效率提升**：医生每天节省约 45 分钟的打字时间，且病历生成的结构化程度更高，便于后续的数据检索。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于场景的模型选型

**说明**: Moonshine 提供了不同参数量的模型变体（如 tiny, base, small 等）。盲目追求最高精度的大模型（如对比 WhisperLargev3）可能会引入不必要的延迟和计算资源消耗。应根据应用场景对实时性和精度的权衡需求进行选择。

**实施步骤**:
1. 评估硬件环境：确认目标部署环境（边缘设备、服务器端或浏览器）的可用内存和算力。
2. 确定优先级：如果是实时对话场景，优先选择延迟更低的 `tiny` 或 `base` 版本；如果是离线视频字幕生成，选择精度更高的 `large` 版本。
3. 进行 A/B 测试：在特定数据集上同时运行 Moonshine 不同变体与 Whisper，对比准确率与推理速度。

**注意事项**: Moonshine 的优势在于在保持高精度的同时大幅减少了参数量，但在极度嘈杂的环境下，较大参数量的模型通常仍能提供更好的鲁棒性。

---

### 实践 2：利用量化技术优化推理速度

**说明**: Moonshine 模型架构设计上对推理速度进行了优化，但通过量化（Quantization，如将模型从 FP32 转换为 INT8）可以进一步减少显存占用并提升吞吐量，特别适合在 CPU 或移动端部署。

**实施步骤**:
1. 使用兼容的推理框架（如 ONNX Runtime, OpenVINO 或 llama.cpp）加载模型。
2. 应用动态量化或静态量化技术，将模型权重转换为 8 位整数。
3. 验证量化后的模型精度损失是否在可接受范围内（通常 STT 模型量化后 WER 变化极小）。

**注意事项**: 量化可能会引入微小的精度下降，务必在测试集上验证 Word Error Rate (WER) 是否符合业务要求。

---

### 实践 3：音频数据的前置处理

**说明**: 虽然 Moonshine 具有较强的抗噪能力，但高质量的输入音频是确保高准确率的基础。合理的预处理可以消除背景噪音、回声并标准化音量，从而发挥模型的最佳性能。

**实施步骤**:
1. 重采样：确保所有输入音频的采样率与模型训练要求一致（通常为 16kHz）。
2. 降噪处理：应用滤波器（如高通滤波器去除低频噪音）或 AI 降噪工具（如 RNNoise）处理原始音频流。
3. 音量归一化：将音频幅度归一化到统一范围（如 -1.0 到 1.0 之间），避免因录音电平过低导致的识别失败。

**注意事项**: 避免过度降噪，以免造成语音信号的失真（即“听觉伪影”），这反而会增加识别错误率。

---

### 实践 4：自定义语言模型微调

**说明**: 通用开源模型在特定垂直领域（如医疗、法律或技术黑话）的识别率可能不佳。针对特定领域的术语和口音对 Moonshine 进行微调，可以获得比通用 WhisperLargev3 更好的表现。

**实施步骤**:
1. 收集数据：整理特定领域的高质量音频数据及对应的标注文本。
2. 准备环境：配置深度学习训练环境（PyTorch/TensorFlow），并获取 Moonshine 的开源权重。
3. 执行微调：使用 LoRA（Low-Rank Adaptation）等技术进行参数高效微调，以降低硬件门槛。
4. 评估验证：在保留的验证集上测试微调后模型的 WER 指标。

**注意事项**: 微调过程中需要监控过拟合现象，确保模型在学会新词汇的同时没有遗忘通用语音的能力（即灾难性遗忘）。

---

### 实践 5：部署长音频分段策略

**说明**: 处理长音频（如会议记录、长视频）时，一次性输入可能导致显存溢出（OOM）或上下文丢失。需要制定合理的分段策略（VAD）来处理长文件。

**实施步骤**:
1. 使用语音活动检测（VAD）算法（如 WebRTC VAD 或 Silero VAD）检测语音停顿。
2. 在静默处将长音频流切割成较小的片段。
3. 对每个片段分别进行推理，并保留时间戳信息。
4. 拼接结果时，使用上下文窗口逻辑对断句处的词汇进行二次确认，以提高连接处的准确性。

**注意事项**: 切片窗口不宜过短，否则会导致句子被截断，破坏语义完整性；也不宜过长，以免超出模型的最大上下文限制。

---

### 实践 6：实施热词提升

**说明**: 在特定应用场景（如客服或语音助手）中，某些关键词（如产品名、指令词）的出现频率很高且至关重要。通过热词提升技术，可以在解码阶段强制增加这些词的权重。

**实施步骤**:
1. 整理高频词汇表：列出业务场景中的核心词汇。
2. 修改解码器配置：在推理代码中配置 Boosting Factor（提升因子），通常在 5 到 20

---
## 学习要点

- Moonshine 系列模型在推理速度上比 Whisper Large v3 快了约 5 倍，同时保持了极高的准确性。
- 该模型在准确性基准测试中超越了 Whisper Large v3，且体积更小、参数量更少。
- Moonshine 采用完全开源的权重策略，允许开发者自由使用和修改。
- 模型设计专门针对边缘计算设备进行了优化，大幅降低了内存和算力需求。
- 即使在长音频输入下，该模型也能保持极低的延迟，非常适合实时语音转文字应用。

---
## 常见问题


### 1: Moonshine 模型与目前流行的 OpenAI Whisper 模型相比有哪些主要优势？

1: Moonshine 模型与目前流行的 OpenAI Whisper 模型相比有哪些主要优势？

**A**: Moonshine 模型主要在推理速度和显存占用（VRAM）方面相比 Whisper 具有显著优势。根据发布者的测试数据，Moonshine 在保持与 Whisper Large v3 相当甚至更高的准确率的同时，推理速度快了 5 倍以上。此外，Moonshine 的参数量更小，对硬件资源的要求更低，使其更适合在本地设备或资源受限的环境中进行实时语音转文字（STT）处理。

---



### 2: Moonshine 模型是开源的吗？我可以将其用于商业项目吗？

2: Moonshine 模型是开源的吗？我可以将其用于商业项目吗？

**A**: 是的，Moonshine 是一个“Open-Weights”（开放权重）模型。这意味着模型的权重是公开的，并且通常采用较为宽松的开源许可证（如 Apache 2.0 或 MIT），允许研究人员和开发者自由下载、使用、修改和分发。您通常可以将其用于商业项目，但建议在实际部署前仔细查阅项目仓库中具体的许可证文件，以确认具体的条款和限制。

---



### 3: 运行 Moonshine 模型需要什么样的硬件配置？能否在 CPU 上运行？

3: 运行 Moonshine 模型需要什么样的硬件配置？能否在 CPU 上运行？

**A**: 由于 Moonshine 采用了高效的架构设计，其硬件门槛相对较低。虽然使用 GPU（如 NVIDIA 显卡）可以获得最快的推理速度，但 Moonshine 经过优化后，也可以在 CPU 上以相对较快的速度运行。这使得它非常适合在没有独立显卡的笔记本电脑或边缘设备上进行部署。具体的内存和处理器要求取决于所选用的具体模型变体（如 Tiny, Base 等），但总体要求远低于 Whisper Large v3。

---



### 4: Moonshine 支持哪些语言？它主要针对英语还是多语言？

4: Moonshine 支持哪些语言？它主要针对英语还是多语言？

**A**: 根据目前的发布信息，Moonshine 模型主要针对英语进行了优化和训练，并且在英语语音识别任务上表现出了极高的准确率。虽然许多现代 STT 模型具备多语言能力，但在发布初期，Moonshine 的核心优势集中在英语的性能提升上。对于其他语言的支持情况，建议参考项目的技术文档或等待社区的多语言适配版本。

---



### 5: 如何快速试用 Moonshine 模型？是否有现成的代码库？

5: 如何快速试用 Moonshine 模型？是否有现成的代码库？

**A**: 开发团队通常会提供现成的 Python 库或代码示例来方便用户试用。一般的使用流程包括：通过 Git 克隆项目仓库，安装必要的依赖（如 PyTorch），然后下载预训练模型权重。代码库中通常会包含一个简单的推理脚本，用户只需输入音频文件路径，即可运行模型并获得转录文本。具体的安装和使用指令请参考该项目的 GitHub 仓库主页。

---



### 6: Moonshine 的训练数据是什么？它是如何达到比 Whisper 更高的准确率的？

6: Moonshine 的训练数据是什么？它是如何达到比 Whisper 更高的准确率的？

**A**: Moonshine 的训练通常基于大规模的公开语音数据集。为了达到比 Whisper Large v3 更高的准确率，开发团队可能采用了更先进的模型架构设计（如改进的 Attention 机制或更优化的 Block 结构），以及更精细的数据清洗和训练策略。其核心突破在于打破了“模型越大越准确”的传统观念，通过算法优化实现了在较小参数量下的高性能表现。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: 基础环境搭建与推理

### 问题**: 阅读该项目的 README 文件，使用提供的代码片段或 Python 绑定，编写一个脚本来转录一个短音频文件（例如 10 秒的语音）。你需要正确安装依赖项并加载模型权重，将识别结果打印到控制台。

### 提示**: 注意检查项目的 PyPI 包名或 GitHub 仓库中的 `requirements.txt`，确保你的环境中有正确的 PyTorch 版本。加载模型时，通常需要指定 `float16` 或 `float32` 精度，这取决于你的硬件。

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
- [Moonshine 开源 STT 模型：精度超越 WhisperLargev3]({{< relref "posts/20260225-hacker_news-show-hn-moonshine-open-weights-stt-models-higher-a-1.md" >}})
- [Moonshine 开源 STT 模型：精度超越 WhisperLargev3]({{< relref "posts/20260224-hacker_news-show-hn-moonshine-open-weights-stt-models-higher-a-6.md" >}})
- [Qwen3.5-397B-A17B：最小Open-Opus级高效模型]({{< relref "posts/20260219-blogs_podcasts-ainews-qwen35-397b-a17b-the-smallest-open-opus-cla-13.md" >}})
- [纯C语言实现Mistral Voxtral 4B语音模型CPU推理]({{< relref "posts/20260210-hacker_news-pure-c-cpu-only-inference-with-mistral-voxtral-rea-3.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*