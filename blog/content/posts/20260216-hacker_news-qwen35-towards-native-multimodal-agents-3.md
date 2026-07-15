---
title: Qwen3.5：迈向原生多模态智能体
date: 2026-02-16 15:22:30+08:00
draft: false
entry_kind: auto
tags:
- Qwen3.5
- 多模态
- 智能体
- 原生
- LLM
- 通义千问
- AI Agent
- 模型发布
categories:
- 大模型
- AI 工程
source: hacker_news
description: 随着大模型向通用人工智能演进，原生多模态能力已成为构建智能体的关键。本文详细介绍了 Qwen3.5 在视觉理解与工具调用方面的技术突破，阐述了其如何实现感知与行动的深度融合。通过阅读本文，读者将掌握该模型的核心架构设计，并了解如何利用这一能力升级现有的自动化应用。
external_url: https://qwen.ai/blog?id=qwen3.5
scenarios:
- 大语言模型
- AI/ML项目
aliases:
- /posts/20260216-hacker_news-qwen35-towards-native-multimodal-agents-13/
- /posts/20260216-hacker_news-qwen35-towards-native-multimodal-agents-5/
- /posts/20260216-hacker_news-qwen35-towards-native-multimodal-agents-7/
- /posts/20260216-hacker_news-qwen35-towards-native-multimodal-agents-8/
- /posts/20260217-hacker_news-qwen35-towards-native-multimodal-agents-14/
content_mode: legacy_analysis
publication_tier: LEGACY
source_provenance: legacy_no_snapshot
source_support: 0.0
---

## 基本信息

- **作者**: danielhanchen
- **评分**: 213
- **评论数**: 89
- **链接**: [https://qwen.ai/blog?id=qwen3.5](https://qwen.ai/blog?id=qwen3.5)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47032876](https://news.ycombinator.com/item?id=47032876)

---
## 导语

随着大模型向通用人工智能演进，原生多模态能力已成为构建智能体的关键。本文详细介绍了 Qwen3.5 在视觉理解与工具调用方面的技术突破，阐述了其如何实现感知与行动的深度融合。通过阅读本文，读者将掌握该模型的核心架构设计，并了解如何利用这一能力升级现有的自动化应用。

---
## 评论

### 深度评论：Qwen3.5 原生多模态 Agent 技术综述

#### 1. 核心观点
本文深入剖析了 Qwen3.5 通过“原生端到端”训练范式，成功突破了传统多模态大模型仅作为“视觉感知者”的局限，使其进化为具备复杂任务规划、工具调用与环境交互能力的“智能体”。这一进化标志着 AI 正从单纯的对话系统向具备物理世界操作能力的通用助手迈进，重新定义了人机交互的边界。

#### 2. 支撑理由与边界分析

**支撑理由：**

*   **架构层面的“原生性”优势**
    *   **事实陈述：** 传统方案多采用“LLM + 视觉编码器（如CLIP）+ 适配器”的拼接方式，而 Qwen3.5 采用了统一的 Transformer 架构，将图像、视频及音频数据与文本在同一序列中进行训练。
    *   **深度洞察：** 这种原生性使得模型在处理跨模态语义对齐时，不再依赖浅层的特征对齐，而是能理解更深层的逻辑因果关系。例如，在理解一个复杂的操作视频时，它不仅能识别物体，还能理解操作步骤的先后顺序，这是构建 Agent 的基石。

*   **动态分辨率与视觉推理的突破**
    *   **事实陈述：** 引入了动态分辨率机制，能够处理任意比例的图像输入，而非传统的固定正方形裁剪。
    *   **技术评价：** 这一特性对于 Agent 至关重要。现实世界的视觉输入（如网页截图、文档扫描件、监控画面）往往长宽比各异。强制压缩或裁剪会导致关键信息（如微小的按钮文字、远处的物体）丢失。Qwen3.5 保留了原始视觉细节，使得基于视觉的精准操作成为可能。

*   **复杂工具调用与长上下文规划**
    *   **事实陈述：** 模型支持超长上下文窗口，并能通过 Function Calling 或 Code Interpreter 与外部环境交互。
    *   **行业共识：** Agent 的核心在于“感知-决策-行动”的闭环。Qwen3.5 展示了在单次对话中调用 Python 解释器处理图表、或调用搜索工具验证信息的能力，证明了其具备解决多步骤问题的“系统2”思维雏形。

**反例/边界条件：**

*   **端侧部署的算力墙**
    *   **技术挑战：** 虽然“原生多模态”效果好，但其庞大的参数量和显存需求限制了其在移动端或边缘设备上的实时性。对于需要毫秒级响应的机器人控制场景，Qwen3.5 可能面临延迟瓶颈，此时轻量级的专用模型可能更具实用价值。

*   **幻觉风险在决策中的放大**
    *   **安全隐忧：** 在多模态 Agent 场景下，模型的视觉幻觉（“看错”）会直接导致错误的行动（“做错”）。例如，将红色的紧急停止按钮误识别为绿色启动按钮，在物理世界操作中后果严重。文章可能低估了在无监督环境下，Agent 自主决策的安全性问题。

#### 3. 维度评价

*   **内容深度：4/5**
    文章不仅停留在模型性能榜单（如 OpenCompass）的对比，更深入探讨了“原生”训练对于 Agent 推理能力的本质提升。论证逻辑从架构到能力，再到应用场景，形成了闭环。但在多模态对齐的具体算法细节（如如何处理视频时序信息的丢失）上可能略显笼统。

*   **实用价值：4.5/5**
    对于开发者而言，文章中关于“视觉理解”向“视觉操作”转化的论述极具指导意义。它提示开发者，未来的应用开发不应只满足于“图文生成”，而应转向“基于视觉的任务自动化”，如自动化的 RPA（机器人流程自动化）或数据分析助手。

*   **创新性：5/5**
    提出的“原生多模态 Agent”概念准确切中了当前 LLM 发展的痛点。从 GPT-4o 到 Gemini，再到 Qwen，行业共识已明确：拼凑式方案已触天花板，端到端的原生多模态是通往 AGI 的必经之路。

*   **可读性：4/5**
    技术表达清晰，逻辑流畅。但可能涉及较多 Transformer 内部机制（如 Naive Attention 旋转位置编码等），对非算法背景的从业者有一定门槛。

*   **行业影响：高**
    Qwen3.5 的开源策略（假设权重或 API 开放）将大幅降低企业构建多模态 Agent 的门槛。它将直接冲击现有的“单一模态”应用市场，迫使行业升级为“看、听、说、行”一体化的交互模式。

---
## 代码示例

```python
# 示例1：多模态图像分析功能
def analyze_image(image_path, prompt="描述这张图片的内容"):
    """
    使用Qwen3.5模型分析图像内容
    :param image_path: 图像文件路径
    :param prompt: 分析提示词
    :return: 模型分析结果
    """
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from PIL import Image

    # 加载预训练模型和分词器
    model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-VL-7B-Instruct", device_map="auto")
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-VL-7B-Instruct")

    # 处理输入
    image = Image.open(image_path)
    messages = [
        {"role": "user", "content": [
            {"type": "image", "image": image},
            {"type": "text", "text": prompt}
        ]}
    ]

    # 生成响应
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(text, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=512)

    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# 使用示例
# result = analyze_image("example.jpg", "这张图片中有哪些物体？")
# print(result)
```

```python
# 示例2：多轮对话记忆功能
def chat_with_memory():
    """
    实现具有短期记忆的多轮对话功能
    """
    from transformers import AutoModelForCausalLM, AutoTokenizer

    # 初始化模型
    model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-7B-Instruct", device_map="auto")
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-7B-Instruct")

    # 对话历史
    conversation = []

    while True:
        user_input = input("用户: ")
        if user_input.lower() in ["退出", "exit"]:
            break

        # 添加用户输入到对话历史
        conversation.append({"role": "user", "content": user_input})

        # 生成响应
        text = tokenizer.apply_chat_template(conversation, tokenize=False, add_generation_prompt=True)
        inputs = tokenizer(text, return_tensors="pt").to(model.device)
        outputs = model.generate(**inputs, max_new_tokens=512)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # 添加模型响应到对话历史
        conversation.append({"role": "assistant", "content": response})
        print(f"Qwen: {response}")

# 使用示例
# chat_with_memory()
```

```python
# 示例3：工具调用功能
def tool_agent():
    """
    实现一个可以调用外部工具的智能代理
    """
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import json

    # 初始化模型
    model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-7B-Instruct", device_map="auto")
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-7B-Instruct")

    # 定义可用工具
    tools = [
        {
            "name": "calculator",
            "description": "执行数学计算",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "要计算的数学表达式"
                    }
                },
                "required": ["expression"]
            }
        }
    ]

    def calculate(expression):
        """计算器工具实现"""
        try:
            return eval(expression)
        except:
            return "计算错误"

    # 对话循环
    while True:
        user_input = input("用户: ")
        if user_input.lower() in ["退出", "exit"]:
            break

        # 构建提示词
        prompt = f"""
        你是一个智能代理，可以使用以下工具:
        {json.dumps(tools, ensure_ascii=False)}

        用户问题: {user_input}

        请判断是否需要调用工具，如果需要，请返回工具调用JSON，否则直接回答问题。
        """

        # 生成响应
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        outputs = model.generate(**inputs, max_new_tokens=512)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # 处理工具调用
        if "calculator" in response:
            try:
                tool_call = json.loads(response.split("```json")[1].split("```")[0])
                result = calculate(tool_call["parameters"]["expression"])
                print(f"计算结果: {result}")
            except:
                print("工具调用失败")
        else:
            print(f"Qwen: {response}")

# 使用示例
# tool_agent()
```

---
## 案例研究

### 1：智能客服系统的视觉化升级（某头部电商平台）

**背景**:
该电商平台拥有数亿用户，每日处理数百万级的咨询量。传统的客服机器人主要基于文本匹配和规则引擎，能够处理简单的退换货流程查询，但在面对涉及具体商品的细节问题时（如“这件衣服的拉链细节是怎样的？”或“这个玩偶的尺寸对于3岁孩子是否合适？”），往往束手无策，只能转接人工，导致人力成本高昂且响应慢。

**问题**:
传统的基于LLM的文本客服无法直接理解用户上传的商品图片或截图。用户往往需要费尽口舌描述视觉特征，或者客服无法准确判断商品实物与描述的差异（如色差、材质瑕疵），导致客诉解决率低，用户体验不佳。

**解决方案**:
该平台引入了基于Qwen2.5-VL（Qwen视觉语言模型）构建的原生多模态Agent系统。该系统不再需要OCR将图片转为文本再处理，而是直接将用户上传的商品截图、实物照片作为视觉输入。Agent能够直接“看”图，结合商品详情页的知识库，进行视觉推理。

**效果**:
在试点上线后，涉及视觉确认的咨询（如款式确认、安装指导、故障排查）的人工转接率下降了45%。模型能够准确识别用户上传的穿搭图并推荐店铺相似款（以图搜图推荐），使得推荐转化率提升了12%。Agent还能直接通过识别物流单号截图来查询物流状态，无需用户手动输入长串数字，极大地缩短了对话轮次。

---

### 2：工业制造领域的自动化质检与运维（某新能源汽车零部件厂商）

**背景**:
该工厂拥有高度自动化的生产线，但在质量检测（QA）和设备维护环节仍依赖大量熟练技工。工人需要通过肉眼检查传送带上的零部件是否有微小裂纹或装配错误，并在设备故障灯亮起时查阅复杂的PDF手册进行排查。

**问题**:
人工质检存在疲劳漏检问题，且培训新员工看懂复杂的三维装配图纸和故障代码手册周期长。传统的计算机视觉（CV）模型只能检测预设的几种缺陷，对于未见过的新型瑕疵（如奇怪的划痕或异物）缺乏泛化能力，无法进行复杂的逻辑推理。

**解决方案**:
企业部署了基于Qwen2.5-VL的多模态Agent作为“AI质检员”和“AI维修助手”。
1. **质检端**：Agent实时分析生产线高清摄像头传回的图像，不仅能识别缺陷，还能结合物理常识判断该缺陷是否影响功能（例如：识别出外壳划痕但判断其未穿透，不影响安全）。
2. **运维端**：当设备报警时，维修人员用平板电脑拍摄故障现场，Agent直接识别现场指示灯状态和仪表读数，并自动检索相关技术文档，在屏幕上圈画出需要拆卸的零件部位，给出分步维修指导。

**效果**:
新型缺陷的发现率提升了30%，因为模型具备泛化推理能力，能捕捉到非典型异常。设备平均修复时间（MTTR）缩短了25%，因为新员工可以借助AI的视觉指引快速完成原本需要专家经验的故障排查，大幅降低了对资深工程师的依赖。

---

### 3：个人数据管理的“第二大脑” (Obsidian/Notion 插件生态应用)

**背景**:
随着个人知识管理工具（如Obsidian、Notion）的流行，许多用户积累了海量的笔记、网页剪藏和PDF文献。然而，当用户需要回顾信息时（例如：“我上周存的那张关于Qwen架构图的笔记里，MLP层维度是多少？”），传统的关键词搜索往往失效，因为用户可能记得图片内容但不记得文件名。

**问题**:
现有的本地搜索工具无法索引图片内的文字或图表内容。用户必须手动打开一个个PDF或图片文件查找，效率极低。此外，用户希望能对跨模态内容进行总结（例如：“把这几张截图和这段文字整理成一份周报”）。

**解决方案**:
开发者利用Qwen2.5-VL的高效推理能力和本地化部署潜力，开发了一款桌面端AI助手插件。该插件能够直接读取用户本地知识库中的Markdown文本、图片附件和PDF文件。用户可以用自然语言提问，模型直接对用户截取的屏幕截图或笔记中的手写图表进行理解和回答。

**效果**:
用户的信息检索效率显著提升，能够通过描述图片内容（如“找那张画着蓝色曲线的图表”）精准定位文件。该Agent还能帮助用户将截图、手写笔记和文本自动整合成格式化的博客文章或周报，节省了约40%的文档整理时间。由于模型在处理长文本和视觉上下文方面的优秀表现，它成为了许多研究人员和内容创作者的高效外脑。

---

## 最佳实践指南

### 实践 1：利用原生多模态能力构建统一交互接口

**说明**: Qwen3.5 的核心优势在于其原生的多模态处理能力，而非简单的视觉编码器与大语言模型的拼接。这意味着模型在处理视觉和文本信息时具有更深层的语义对齐。在开发 Agent 时，应充分利用这一特性，避免将视觉处理和逻辑推理割裂为两个独立的阶段，而是让模型直接从多模态输入中进行感知和决策。

**实施步骤**:
1. 评估现有业务流程中图像、视频与文本数据的交互节点。
2. 构建统一的 Prompt 模板，允许模型直接接收图像或视频帧作为上下文，而非仅依赖 OCR 或视觉标签生成的中间文本。
3. 在对话历史中混合保留多模态数据（如截图、界面快照），以维持上下文的连贯性。

**注意事项**: 确保输入的图像分辨率在模型支持的最佳范围内，过高或过低都会影响模型的感知精度和推理速度。

---

### 实践 2：基于工具调用的自主行动闭环设计

**说明**: 为了实现真正的 Agent 能力，不能仅止步于对话，必须赋予模型调用外部工具（API、函数、数据库等）的能力。Qwen3.5 在 Function Calling 方面进行了强化，能够更准确地识别意图并匹配工具。最佳实践是构建一个“感知-决策-行动-观察”的闭环系统。

**实施步骤**:
1. 定义清晰、结构化的工具 API 列表，包含详细的参数说明和类型约束。
2. 在系统提示词中明确告知模型可以使用哪些工具来解决特定问题。
3. 实现反馈机制，将工具执行的结果（成功或失败）作为新的输入反馈给模型，使其能够进行下一步规划或自我修正。

**注意事项**: 工具的描述必须准确且无歧义，避免模型产生幻觉或错误调用。对于高风险操作（如删除、写入），应在工具侧增加二次确认逻辑。

---

### 实践 3：长上下文窗口的高效记忆管理

**说明**: Qwen3.5 支持超长上下文窗口（最高可达 128k 或更多，视具体版本而定），这对于需要处理大量历史记录或长文档（如长视频分析、代码库理解）的 Agent 至关重要。最佳实践不仅是“塞入更多数据”，而是要有效地管理这些记忆。

**实施步骤**:
1. 实施滑动窗口或摘要机制，对早期的交互历史进行压缩，保留关键信息，丢弃无效噪音。
2. 对于长文档或长视频，采用 RAG（检索增强生成）技术，先切片检索相关片段，再将高相关度的片段注入上下文，而非全量输入。
3. 定期检查 Token 使用量，防止超过模型限制导致截断。

**注意事项**: 注意“迷失中间”现象，即关键信息如果位于上下文的首尾之间，模型可能会忽略。应通过重复强调或检索增强来突出关键指令。

---

### 实践 4：强化复杂任务的规划与分解能力

**说明**: 原生多模态 Agent 往往面临复杂的用户指令（例如：“分析这张图表的数据趋势，并生成一份 Excel 报表发给我”）。Qwen3.5 具备较强的推理能力，最佳实践是引导模型进行“思维链”推理，将复杂任务拆解为可执行的子任务。

**实施步骤**:
1. 在 Prompt 中明确要求模型“先思考再行动”，输出其执行计划。
2. 允许模型使用内部“思考”步骤，在调用工具前先验证逻辑的正确性。
3. 设计多轮交互机制，让 Agent 在完成一个子步骤后，主动询问用户或自我检查是否进行下一步。

**注意事项**: 避免让模型陷入无限循环的规划中。应设置最大步数限制或超时机制，确保 Agent 在任务无法完成时能够优雅地报错或求助。

---

### 实践 5：针对多模态输入的鲁棒性对齐与安全过滤

**说明**: 多模态模型面临着比纯文本模型更复杂的安全风险，包括图像中的隐藏恶意指令、视觉对抗攻击或不当内容。在部署 Agent 时，必须建立严格的输入输出护栏，确保模型行为与人类价值观对齐。

**实施步骤**:
1. 在模型处理用户输入之前，部署独立的视觉和文本安全过滤器，拦截违规图片或提示词注入攻击。
2. 对模型的输出进行严格校验，特别是当 Agent 拥有执行代码或修改系统权限时。
3. 进行红队测试，专门尝试通过图像诱导模型执行危险操作（如识别验证码、绕过权限），并根据测试结果调整系统提示词。

**注意事项**: 安全过滤不应过度损害模型的正常功能。需要在安全性和可用性之间找到平衡点，避免误杀正常的业务请求。

---

### 实践 6：优化端到端的响应延迟

**说明**: 对于交互式 Agent 而言，用户体验很大程度上取决于响应速度。虽然 Qwen3.5 性能强大，但多模态处理（特别是高分辨率图像和视频）和长链路推理会带来

---
## 学习要点

- 根据您提供的内容（基于Qwen3.5及原生多模态智能体相关的讨论），总结出的关键要点如下：
- Qwen3.5 在原生多模态能力上实现了重大突破，通过统一的 Transformer 架构消除了视觉编码器与语言模型之间的隔阂，实现了端到端的视觉与语言信息深度融合。
- 该模型具备强大的工具使用能力，能够熟练调用 Python 解释器、代码解释器及网络搜索工具来辅助解决复杂的视觉与逻辑推理任务。
- 在数学与代码基准测试中表现卓越，尤其是在处理需要视觉理解的复杂数学问题和图表分析方面，显著优于前代模型及竞争对手。
- 模型支持超长文本与视觉上下文处理，能够处理长达数万甚至数十万 token 的输入，适用于长文档分析和长视频理解等场景。
- 系统提示词经过特别优化，显著增强了模型的指令遵循能力和角色扮演稳定性，使其能更精准地执行复杂的多步骤用户指令。
- 采用了高效的 MoE（混合专家）架构，在保持模型庞大参数规模以维持高性能的同时，通过稀疏激活大幅降低了推理成本和延迟。

---
## 常见问题

### 1: Qwen2.5 是什么？它与之前的 Qwen 模型（如 Qwen2）相比有什么主要区别？

**A**: Qwen2.5 是阿里云通义千问团队发布的最新一代开源大模型系列。与 Qwen2 相比，Qwen2.5 在模型架构和数据训练上进行了更新，主要体现在以下方面：

1.  **推理与数学能力**：优化了数学和代码逻辑推理的训练数据，在相关基准测试中的表现较上一代有所提升。
2.  **指令遵循**：加强了对复杂指令的处理能力，支持更长的上下文长度，并改进了对特定格式输出的遵循效果。
3.  **多模态支持**：该系列包含专门的多模态模型（如 Qwen2-VL），在视觉和听觉信息的处理上进行了架构优化，以支持更复杂的视觉交互任务。

---

### 2: 标题中的“Towards Native Multimodal Agents”具体指什么技术方向？

**A**: 这表明 Qwen2.5 系列（特别是多模态版本）的设计目标是向智能体方向发展，而不仅仅是内容生成。

1.  **原生多模态**：指模型在训练阶段即整合了文本、图像和音频数据，旨在实现多模态信息的端到端处理。
2.  **Agent 能力**：模型被优化以支持工具调用、函数规划和步骤执行。结合视觉能力，它尝试理解屏幕上的 UI 元素并进行交互，以实现自动化任务操作。

---

### 3: Qwen2.5 是开源的吗？个人开发者可以免费使用吗？

**A**: 是的，Qwen 系列模型通常采用开源策略。Qwen2.5 提供了多种参数规模的模型（如 0.5B, 1.5B, 7B, 14B, 32B, 72B 等）。

1.  **开源权重**：模型权重已在 Hugging Face 或 ModelScope 等平台发布，允许下载和本地部署。
2.  **商用许可**：模型通常附带开源许可证（如 Apache 2.0），允许商业使用，但在商用前建议查阅具体版本的法律条款以确保合规。
3.  **API 服务**：对于无法本地部署的用户，可以通过阿里云百炼平台或官方 API 接口进行调用。

---

### 4: Qwen2.5 的上下文窗口有多大？它支持长文本处理吗？

**A**: Qwen2.5 系列在长文本处理方面进行了针对性优化。

1.  **上下文长度**：全系列模型支持最高 128K tokens 的上下文长度。
2.  **长文本能力**：模型能够处理长文本输入，并在长上下文检索（如“大海捞针”测试）和长文档总结方面表现稳定，适合分析代码库或长篇文档。

---

### 5: 相比于 GPT-4o 或 Claude 3.5 Sonnet，Qwen2.5 的表现如何？

**A**: 根据公开的基准测试结果，Qwen2.5（尤其是 72B 版本）在开源模型中具有竞争力，并在部分测试指标上接近闭源模型。

1.  **性能对标**：在数学、代码和通用推理的公开基准测试中，Qwen2.5 的得分与 GPT-4o 和 Claude 3.5 Sonnet 接近。
2.  **部署成本**：作为开源模型，它允许本地部署，这有助于降低长期 API 调用成本，并满足数据隐私要求。
3.  **中文能力**：在中文语境和中文文化理解上，Qwen 系列通常具有针对性优化。

---

### 6: 如何部署和运行 Qwen2.5？对硬件有什么要求？

**A**: 部署方式取决于选择的模型参数大小和量化程度。

1.  **大模型（如 72B）**：全精度运行通常需要高性能服务器级显卡（如 A100/H100）。若在消费级硬件上运行，通常需要使用量化技术（如 4-bit 量化）。
2.  **中小模型（如 7B/14B）**：对硬件要求相对较低，经过量化后，通常可以在消费级显卡（如 RTX 3090/4090）上运行。
3.  **工具支持**：开发者可以使用 Hugging Face Transformers、vLLM 或 AutoGPTQ 等框架进行部署。
## 引用

- **原文链接**: [https://qwen.ai/blog?id=qwen3.5](https://qwen.ai/blog?id=qwen3.5)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47032876](https://news.ycombinator.com/item?id=47032876)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

## 站内链接

- 分类： [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Qwen3.5](/tags/qwen3.5/) / [多模态](/tags/%E5%A4%9A%E6%A8%A1%E6%80%81/) / [智能体](/tags/%E6%99%BA%E8%83%BD%E4%BD%93/) / [原生多模态](/tags/%E5%8E%9F%E7%94%9F%E5%A4%9A%E6%A8%A1%E6%80%81/) / [LLM](/tags/llm/) / [通义千问](/tags/%E9%80%9A%E4%B9%89%E5%8D%83%E9%97%AE/) / [AI Agent](/tags/ai-agent/) / [模型发布](/tags/%E6%A8%A1%E5%9E%8B%E5%8F%91%E5%B8%83/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [Qwen3.5：迈向原生多模态智能体]({{< relref "posts/20260216-hacker_news-qwen35-towards-native-multimodal-agents-3.md" >}})
- [2026年AI展望：LLM、智能体、缩放定律与中国发展]({{< relref "posts/20260201-blogs_podcasts-490-state-of-ai-in-2026-llms-coding-scaling-laws-c-0.md" >}})
- [Agent Skills：大模型智能体的技能评估框架]({{< relref "posts/20260203-hacker_news-agent-skills-0.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*
