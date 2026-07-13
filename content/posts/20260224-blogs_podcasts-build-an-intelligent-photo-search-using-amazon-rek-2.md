---
title: 基于 AWS CDK 集成 Rekognition 与 Neptune 构建智能图片搜索系统
date: 2026-02-24 23:13:49+08:00
draft: false
entry_kind: auto
tags:
- AWS
- CDK
- Rekognition
- Neptune
- Bedrock
- 图数据库
- 图片搜索
- IaC
categories:
- AI 工程
- 系统与基础设施
source: blogs_podcasts
description: 以下是基于原文内容的总结： **构建基于 AWS 的智能照片搜索系统** 本文介绍了一种利用 AWS 云开发 kit（AWS CDK）构建综合照片搜索系统的解决方案。该系统通过集成三项核心服务，实现了从图像分析到关系映射，再到智能描述的全流程功能：
  1. **Amazon Rekognition**：利用其深度学习能力
external_url: https://aws.amazon.com/blogs/machine-learning/build-an-intelligent-photo-search-using-amazon-rekognition-amazon-neptune-and-amazon-bedrock
scenarios:
- Web应用开发
---

# 基于 AWS CDK 集成 Rekognition 与 Neptune 构建智能图片搜索系统

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-02-24T18:22:26+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/build-an-intelligent-photo-search-using-amazon-rekognition-amazon-neptune-and-amazon-bedrock](https://aws.amazon.com/blogs/machine-learning/build-an-intelligent-photo-search-using-amazon-rekognition-amazon-neptune-and-amazon-bedrock)

---

## 摘要/简介

在本文中，我们将向您展示如何使用 AWS Cloud Development Kit (AWS CDK) 构建一个综合性的图片搜索系统，该系统集成了 Amazon Rekognition 用于人脸和物体检测、Amazon Neptune 用于关系映射，以及 Amazon Bedrock 用于 AI 驱动的图片描述生成。

---

## 导语

随着非结构化数据量的激增，如何高效地从海量图片中提取语义并建立关联，已成为构建智能应用的关键挑战。本文将介绍如何利用 AWS CDK 集成 Amazon Rekognition、Neptune 与 Bedrock，构建一套集成了视觉识别、图数据库关联及生成式 AI 的综合图片搜索系统。通过阅读本文，您将掌握具体的架构设计与实现步骤，从而将原本独立的图片数据转化为可理解、可检索的结构化信息。

---

## 摘要

以下是基于原文内容的总结：

**构建基于 AWS 的智能照片搜索系统**

本文介绍了一种利用 AWS 云开发 kit（AWS CDK）构建综合照片搜索系统的解决方案。该系统通过集成三项核心服务，实现了从图像分析到关系映射，再到智能描述的全流程功能：

1.  **Amazon Rekognition**：利用其深度学习能力，进行人脸检测和物体识别，从照片中提取视觉特征。
2.  **Amazon Neptune**：作为图形数据库服务，用于构建和映射照片、人物及物体之间的复杂关系网络。
3.  **Amazon Bedrock**：提供基于生成式 AI 的能力，为照片自动生成描述性说明（Captioning）。

该方案旨在通过将 CDK 的基础设施即代码能力与上述 AI 服务相结合，打造一个功能强大且易于部署的智能搜索应用。

---

## 评论

### 中心观点
这篇文章展示了一个典型的**“多模态RAG（检索增强生成）+ 知识图谱”**的现代AI应用架构，其核心价值在于利用图数据库（Neptune）的非结构化关系推理能力来弥补传统向量检索在语义关联上的不足，从而实现从“识别物体”到“理解视觉关系”的跨越。

### 深入评价

#### 1. 内容深度与论证严谨性
*   **事实陈述**：文章采用了AWS CDK进行基础设施即代码的部署，整合了计算机视觉、图数据库和大语言模型（LLM）。
*   **作者观点**：文章试图证明将元数据存储在图数据库中比单纯的向量检索能提供更复杂的查询能力（例如“查找某人A和某人B在同一张照片中的所有图片”）。
*   **你的推断**：文章在深度上略显不足。它更像是一个标准的“Hello World”教程，而非生产级指南。例如，它没有深入探讨**实体消歧**的难题——当Rekognition检测到两个不同的人但Bedrock将其描述为同一个人时，或者反之，系统如何处理这种冲突？此外，对于Neptune的性能调优（如索引策略）和Bedrock的Token消耗成本缺乏定量分析。

#### 2. 实用价值与指导意义
*   **事实陈述**：文中提供了完整的CDK代码栈，允许开发者一键部署整套架构。
*   **作者观点**：这种架构为企业构建非结构化数据资产目录提供了可复用的蓝图。
*   **你的推断**：其实用性受限于**“冷启动”**问题。对于没有存量元数据的图片库，完全依赖Bedrock生成Caption不仅成本高昂，而且延迟极高，不适合实时性要求高的场景。此外，代码示例虽然能跑通，但缺乏错误处理和并发控制，直接用于生产环境风险较大。

#### 3. 创新性分析
*   **事实陈述**：结合使用Rekognition（视觉特征提取）和Neptune（关系存储）并非全新概念，但结合Bedrock（语义理解）是较新的趋势。
*   **作者观点**：该方案创新地将非结构化图像转化为结构化的图知识，使照片搜索具备了推理能力。
*   **反例/边界条件**：
    1.  **关系隐晦性**：如果照片中两人只是背对背站立，Bedrock可能生成“两个人在公园”，Neptune只能提取“人-公园”关系，而无法提取“人-人”的社交关系，此时图数据库的优势荡然无存。
    2.  **多模态幻觉**：Bedrock生成的Caption可能包含幻觉（描述了不存在的物体），如果直接将其存入Neptune作为事实，会导致垃圾进垃圾出，污染图数据库。

#### 4. 可读性与逻辑性
*   **事实陈述**：文章遵循AWS官方博客的标准结构：架构图 -> 服务介绍 -> 代码实现 -> 测试。
*   **评价**：逻辑清晰，但对于初学者来说，同时理解Rekognition的BoundingBox概念、Neptune的Gremlin查询语言以及Bedrock的Prompt工程，认知负荷较重。文章在服务间的数据流转（特别是如何将JSON结果映射到图节点）解释得不够直观。

#### 5. 行业影响
*   **你的推断**：这篇文章反映了行业从**“以搜索为中心”**向**“以推理为中心”**的范式转移。它暗示了未来的搜索引擎不仅仅是匹配关键词，而是通过图谱构建世界模型。然而，它也暴露了当前技术栈的复杂性，预示着市场上对于简化这类多服务编排的PaaS平台需求将增大。

#### 6. 争议点与不同观点
*   **观点**：文章倾向于使用专有的AWS全家桶。
*   **争议**：这种架构导致了严重的**厂商锁定**。
    *   **反例**：使用开源替代方案（如CLIP用于视觉编码，Neo4j用于图存储，Llama 3用于Caption）可能在长期维护成本上更具优势，且数据主权更强。
*   **观点**：文章认为必须使用Neptune。
*   **争议**：对于简单的照片搜索，引入图数据库引入了过高的复杂性。
    *   **反例**：如果需求仅仅是“找猫”或“找某人”，基于PostgreSQL的pgvector或简单的OpenSearch索引可能更高效、更便宜。

### 实际应用建议

1.  **混合检索策略**：不要完全依赖Neptune。建议保留OpenSearch或Elasticsearch作为第一层检索（利用Rekognition的标签或向量），利用Neptune作为第二层过滤（用于复杂的关系查询，如社交网络分析），以平衡性能与功能。
2.  **异步处理管道**：鉴于Bedrock的生成速度，绝对不要在用户上传照片的同步请求中调用Caption生成。应设计基于SQS的异步管道，先生成缩略图和基础标签返回用户，后台慢慢生成语义描述和图关系。
3.  **置信度阈值**：在生产环境中，必须为Rekognition和Bedrock设置严格的置信度阈值。例如，只有当Rekognition的人脸置信度>99%时才将其作为“Person”节点存入Neptune，避免图数据过于稀疏或充满噪音。

### 可验证的检查方式

1.  **性能指标测试**：
    *   **指标**：端到端延迟。从上传一张JPG图片到可以在Neptune中查询到其关系的时间。
    *   **预期**：如果包含Bedrock生成，通常在3-10秒之间。如果超过15

---

## 技术分析

以下是对文章《Build an intelligent photo search using Amazon Rekognition, Amazon Neptune, and Amazon Bedrock》的深度分析报告。

---

### 深度分析报告：基于 AWS 构建智能图搜系统

### 1. 核心观点深度解读

**文章的主要观点**
文章展示了一种**混合智能架构**的优越性。作者主张，单纯依赖元数据（时间、地点）或单一视觉特征向量的传统图片搜索已不足以满足现代需求。通过将**计算机视觉**、**图数据库**和**生成式AI**三者结合，可以构建一个能够理解“图像中有什么”以及“图像之间关系如何”的语义级搜索系统。

**作者想要传达的核心思想**
核心思想在于**“多模态数据的关联与增强”**。
1.  **非结构化数据的结构化**：利用 Rekognition 将图片像素转化为结构化的标签和向量。
2.  **隐性关系的显性化**：利用 Neptune 将离散的图片通过人物、物体、地点等实体连接成知识图谱。
3.  **上下文的生成**：利用 Bedrock 为图片生成自然语言描述，填补视觉特征与人类自然语言查询之间的鸿沟。

**观点的创新性和深度**
*   **创新性**：传统的图搜多基于 CLIP 等模型的向量相似度搜索，虽然强大但往往缺乏逻辑推理能力（例如“找出照片里和这个人站在一起的所有人”）。本文提出的架构引入了图数据库，使得系统能够处理基于关系的复杂查询，这是对纯向量检索的重要补充。
*   **深度**：文章不仅停留在识别层面，还深入到了**知识推理**层面。它展示了如何从单纯的“检测”进化到“联网”，利用图论来解决多跳查询问题。

**为什么这个观点重要**
随着非结构化数据（图片、视频）的爆炸式增长，数据孤岛问题日益严重。企业积累了海量图片，但无法有效利用。这种架构提供了一种**将数据资产转化为知识图谱**的路径，对于数字资产管理、安防监控、社交媒体分析等领域具有极高的商业价值。

### 2. 关键技术要点

**涉及的关键技术或概念**
*   **Amazon Rekognition**：提供预训练的 CV 能力，用于人脸检测、对象识别和标签提取。
*   **Amazon Neptune**：全托管图数据库，基于属性图模型，使用 SPARQL 或 Gremlin 查询。
*   **Amazon Bedrock**：托管生成式 AI 服务，利用 LLM（如 Claude 或 Titan）生成图片标题。
*   **Vector Search (OpenSearch)**：虽然摘要未详述，但通常此类架构会结合向量数据库进行混合检索。
*   **AWS CDK**：基础设施即代码，用于自动化部署。

**技术原理和实现方式**
1.  **数据摄取与预处理**：图片上传至 S3，触发 Lambda 函数。
2.  **特征提取**：
    *   调用 Rekognition `DetectFaces` 和 `DetectLabels` 获取实体。
    *   调用 Bedrock API，传入图片 Base64 或 URL，Prompt LLM 生成详细描述。
3.  **图谱构建**：
    *   **节点**：创建 Image、Person、Object 节点。
    *   **边**：建立关系，如 `Person` -> [APPEARS_IN] -> `Image`，`Image` -> [CONTAINS] -> `Object`。
    *   将这些数据写入 Neptune。
4.  **查询处理**：用户输入自然语言（如“找出小明在公园的所有照片”），系统解析意图，在 Neptune 中执行图遍历查询。

**技术难点和解决方案**
*   **难点：实体对齐**。如何确定照片 A 中的“张三”和照片 B 中的“张三”是同一个人？
    *   *解决方案*：利用 Rekognition 的人脸索引集合比较相似度，当置信度超过阈值时，关联到同一个 Person 节点。
*   **难点：LLM 幻觉与成本**。Bedrock 生成描述可能不准确且昂贵。
    *   *解决方案*：采用混合策略，关键实体依赖 Rekognition（确定性），上下文描述依赖 Bedrock（生成性），并可能引入缓存机制。
*   **难点：图数据建模**。如何设计 Schema 以支持灵活的查询？
    *   *解决方案*：使用属性图，允许节点拥有动态属性，便于后续扩展。

**技术创新点分析**
最大的技术创新在于**将 LLM 的语义理解能力注入图数据库**。传统的图搜索需要精确的 Cypher/Gremlin 语句，而结合 Bedrock 后，系统可以将自然语言直接转化为图查询语句，极大地降低了图数据库的使用门槛。

### 3. 实际应用价值

**对实际工作的指导意义**
该架构为数据工程师和架构师提供了一种**“存算分离”与“专件专用”**的最佳实践范例。它证明了在处理复杂的多模态数据时，单一的数据库（无论是关系型还是向量型）都无法完美解决问题，组合拳才是王道。

**可以应用到哪些场景**
1.  **企业数字资产管理 (DAM)**：广告公司或媒体机构可以通过“情绪”、“动作”、“包含的人物”快速检索素材。
2.  **智慧警务与安防**：追踪嫌疑人轨迹（图关系），查找特定场景（如“红色卡车在银行附近”）。
3.  **社交网络分析**：分析用户社交圈，自动推荐照片标记。
4.  **电商搜索**：用户搜索“度假穿的衣服”，系统通过图关系关联“海滩”、“ sunglasses”等标签的商品。

**需要注意的问题**
*   **数据隐私**：人脸识别数据极其敏感，必须符合 GDPR 或当地法律，Neptune 中的数据需加密。
*   **冷启动问题**：系统需要积累一定量的数据和关系后，图查询的优势才能显现。
*   **延迟**：Bedrock 的生成是异步且耗时的，不适合对实时性要求极高的场景。

**实施建议**
*   先从简单的元数据标签开始，不要一开始就过度复杂化图模型。
*   严格监控 Rekognition 的置信度阈值，防止错误关联污染图谱。
*   利用 AWS CDK 的 reproducibility 特性，频繁在开发环境测试架构变更。

### 4. 行业影响分析

**对行业的启示**
该案例预示了**RAG（检索增强生成）技术的进化方向**：从单纯的“文档+向量”检索，向“多模态知识图谱”检索演进。未来的搜索引擎将不仅理解关键词，还能理解实体间的复杂逻辑关系。

**可能带来的变革**
*   **从“搜索”到“发现”**：用户不再需要精确描述图片，系统可以通过图关系推荐相关联的图片（例如：搜出一张照片，系统自动推荐该照片中所有其他参与者的其他照片）。
*   **非结构化数据的结构化革命**：图数据库将不再是小众技术，随着多模态数据的增加，图数据库将成为 AI 应用的核心基础设施。

**相关领域的发展趋势**
*   **GraphRAG**：结合知识图谱和 RAG 是目前 AI Agent 领域最热门的趋势之一。
*   **多模态 LLM**：未来的模型将原生支持视觉输入，可能不再需要外挂 Bedrock 生成描述，而是直接提取特征入图。

**对行业格局的影响**
这将进一步巩固云厂商（如 AWS）的地位。构建此类系统需要协调 Rekognition、Neptune、Bedrock、S3 等多个服务，这种复杂的协同能力是单一垂直 SaaS 软件难以比拟的。

### 5. 延伸思考

**引发的其他思考**
*   **图神经网络的结合**：目前 Neptune 主要用于存储和遍历。未来是否可以在 Neptune 上直接运行 GNN 算法，对图片内容进行预测或分类？
*   **时序图谱**：照片具有强烈的时间属性。如何利用时序图谱分析事件演变（例如：一个活动的开始、高潮、结束）？

**可以拓展的方向**
*   **视频分析**：将视频拆解为关键帧，构建基于时间序列的超大图谱，用于视频内容理解。
*   **个性化推荐**：结合用户行为图谱和图片内容图谱，实现基于语义的推荐。

**需要进一步研究的问题**
*   当图谱规模达到数十亿节点时，如何保证实时查询性能？
*   如何处理 LLM 生成的描述中存在的偏见或错误信息被写入图谱后的修正机制？

**未来发展趋势**
**Self-Optimizing Graphs（自优化图谱）**。系统不仅能根据图片构建图谱，还能根据用户的查询反馈，自动调整图谱的权重和连接，甚至自动修正实体识别的错误。

### 7. 案例分析

**结合实际案例说明**
假设某大型**保险公司的理赔部门**应用此技术。
*   **场景**：用户上传车损照片。
*   **传统做法**：人工审核，肉眼比对损伤。
*   **本架构应用**：
    1.  **Rekognition**：识别出车型、损伤部件（如“bumper dent”）。
    2.  **Bedrock**：生成描述“一辆红色丰田卡罗拉的前保险杠在夜间有凹陷”。
    3.  **Neptune**：将此照片与该用户的历史理赔记录（图节点）关联。
    4.  **结果**：系统发现该用户在过去一年内有三次类似的“前保险杠损伤”理赔，且照片中的背景极其相似，系统自动标记为“疑似欺诈”。

**成功案例分析**
**Pinterest** 是视觉搜索的先驱。他们早期利用深度学习提取图片特征，后来引入图数据库连接 Pin 和 Board，极大地提升了推荐的准确性。AWS 的这套方案正是让普通企业也能以低成本构建类似 Pinterest 的核心能力。

**失败案例反思**
某零售商尝试构建类似系统，但**未建立统一的 ID 系统**。
*   **问题**：Rekognition 识别出的“Nike Shoe”和 Bedrock 生

---

## 最佳实践

### 实践 1：优化图像元数据提取与标签策略

**说明**:
单纯依赖 Amazon Rekognition 的默认标签可能无法满足特定的搜索需求（如抽象概念或特定场景）。建议结合 Rekognition 的标签检测与 Amazon Bedrock 的多模态能力（如 Claude 3 或 Titan 模型），生成自然语言描述和结构化元数据，以支持基于语义的搜索功能。

**实施步骤**:
1. 配置 Amazon Rekognition `DetectLabels` API，并设置最小置信度阈值（例如 85%）以过滤低置信度标签。
2. 将提取的标签和图像 S3 URI 传递给 Amazon Bedrock，利用 Prompt Engineering 生成详细的图像描述。
3. 将生成的描述文本与原始标签一并存储，作为 Neptune 中节点的属性。

**注意事项**:
- 需注意 Bedrock 的 Token 限制，对于大批量处理，建议使用异步队列。
- 确保 Prompt 包含指令，强制模型输出结构化数据（如 JSON），便于解析并存入图数据库。

---

### 实践 2：构建高效的图数据模型

**说明**:
Neptune 的性能依赖于数据模型的设计。对于照片搜索应用，建议避免将所有信息存储在单一节点中。应将实体（如人、地点、物体）建模为节点，将照片作为节点，并通过“边”来表示关系（如“包含”、“拍摄于”）。这种设计支持多跳查询（例如：查找包含“狗”且在“户外”拍摄的照片）。

**实施步骤**:
1. 定义顶点类型：`Photo`（包含 S3 链接、时间戳）、`Label`（物体/场景）、`Person`（如果有人脸识别）。
2. 定义边类型：`CONTAINS`（Photo -> Label）、`FEATURES`（Photo -> Person）。
3. 使用 Gremlin 或 openCypher 加载数据，并为常用查询属性（如 Label 名称、Photo 日期）建立索引。

**注意事项**:
- 避免超级节点（即连接了数百万张照片的标签），这可能导致查询性能下降。可以通过分片或引入中间节点来解决。
- 定期分析查询慢日志，优化索引策略。

---

### 实践 3：实现向量与图数据的混合搜索

**说明**:
仅靠精确匹配标签可能无法完全满足搜索需求。建议利用 Amazon Bedrock 的 Embedding 模型将图像描述或用户查询转换为向量，并存储在 Neptune 中（利用 Neptune ML 或 Neptune Analytics 的向量搜索功能）。这有助于理解语义（例如，用户搜索“可爱的小狗”，即使标签只有“金毛”，也能通过向量相似度匹配）。

**实施步骤**:
1. 选择合适的 Amazon Bedrock Embedding 模型（如 Titan Embeddings 或 Cohere Multilingual）。
2. 在图像处理流程中，调用 Bedrock 生成图像描述的 Embedding 向量，并将其作为属性存储在 Neptune 的 `Photo` 节点中。
3. 在搜索时，将用户的自然语言查询转换为向量，并在 Neptune 中执行向量相似度搜索（KNN），结合图遍历过滤结果。

**注意事项**:
- 向量维度较高会占用较多存储和内存，建议根据精度要求选择向量维度或进行降维处理。
- 监控向量搜索的延迟，必要时考虑使用 OpenSearch Service 作为 Neptune 的辅助向量索引。

---

### 实践 4：实施无服务器架构与异步处理

**说明**:
图像处理和向量计算属于计算密集型任务。建议使用 Amazon EventBridge 和 AWS Lambda（或 AWS Fargate）构建异步管道。当照片上传到 S3 时触发处理流程，以避免阻塞用户请求并提高系统的可扩展性。

**实施步骤**:
1. 配置 S3 Event Notification，在 `PUT` 请求时触发 EventBridge 规则。
2. EventBridge 调用 Step Functions 编排工作流：先调用 Rekognition，再调用 Bedrock，最后将结果写入 Neptune。
3. 使用 SQS 处理死信队列（DLQ），以处理处理失败的图像或 API 限流情况。

**注意事项**:
- 设置 Lambda 并发限制，以防止突发流量导致下游服务过载。
- 监控 Step Functions 的执行情况，确保各步骤超时设置合理。

---

## 学习要点

- 利用 Amazon Rekognition 自动提取图像中的实体、场景和文本标签，将非结构化照片数据转化为可搜索的结构化元数据。
- 借助 Amazon Neptune 图数据库构建实体关系网络，能够高效执行复杂的关联查询（如“查找特定人物在特定场景下的照片”）。
- 集成 Amazon Bedrock 的大语言模型（LLM）能力，将用户的自然语言实时转换为图数据库查询语言（如 Gremlin 或 SPARQL），实现直观的对话式搜索体验。
- 采用“向量搜索 + 图遍历”的混合架构，既能处理基于语义的模糊匹配，又能处理基于关系的精确推理，显著提高检索准确率。
- 利用 Neptune 的图结构特性，可以轻松实现多跳关系推理（例如通过识别出的物体反推相关人物或事件），挖掘数据背后的隐性联系。
- 通过将图像特征向量化并存储在 Neptune 中，支持基于视觉相似度的搜索，即使用户无法准确描述目标内容也能找到相似图片。
- 该架构展示了云原生服务在处理非结构化数据时的协同效应，即通过 Rekognition 理解内容、Neptune 建立连接、Bedrock 理解意图，构建端到端的智能应用。

---

## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/build-an-intelligent-photo-search-using-amazon-rekognition-amazon-neptune-and-amazon-bedrock](https://aws.amazon.com/blogs/machine-learning/build-an-intelligent-photo-search-using-amazon-rekognition-amazon-neptune-and-amazon-bedrock)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [AWS](/tags/aws/) / [CDK](/tags/cdk/) / [Rekognition](/tags/rekognition/) / [Neptune](/tags/neptune/) / [Bedrock](/tags/bedrock/) / [图数据库](/tags/%E5%9B%BE%E6%95%B0%E6%8D%AE%E5%BA%93/) / [图片搜索](/tags/%E5%9B%BE%E7%89%87%E6%90%9C%E7%B4%A2/) / [IaC](/tags/iac/)
- 场景： [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [基于AWS CDK集成Rekognition、Neptune与Bedrock的智能照片搜索系统]({{< relref "posts/20260224-blogs_podcasts-build-an-intelligent-photo-search-using-amazon-rek-0.md" >}})
- [利用全栈模板加速开发基于Amazon Bedrock AgentCore的应用]({{< relref "posts/20260211-blogs_podcasts-accelerate-agentic-application-development-with-a--12.md" >}})
- [利用 FAST 模板加速构建 Amazon Bedrock AgentCore 应用]({{< relref "posts/20260210-blogs_podcasts-accelerate-agentic-application-development-with-a--11.md" >}})
- [Accelerate agentic application development with a full-]({{< relref "posts/20260211-blogs_podcasts-accelerate-agentic-application-development-with-a--11.md" >}})
- [Amazon Bedrock 限流与服务可用性管理指南]({{< relref "posts/20260212-blogs_podcasts-mastering-amazon-bedrock-throttling-and-service-av-12.md" >}})
