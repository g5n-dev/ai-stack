---
title: "Amazon SageMaker AI异步推理支持内联Payload，无需上传S3"
date: 2026-06-17T21:25:32+08:00
draft: false
entry_kind: "auto"
tags: ["异步推理", "内联请求", "AWS", "S3", "机器学习", "API调用", "低延迟", "效率提升"]
categories: ["AI 工程", "系统与基础设施"]
source: blogs_podcasts
description: "Amazon SageMaker AI 异步推理现已支持在请求体中直接携带输入数据（inline payload），使用户无需在调用前先将数据上传至 Amazon S3。通过 InvokeEndpointAsync API，可直接在请求体内发送推理载荷，实现更简化的调用流程，降低延迟并提升效率。"
external_url: https://aws.amazon.com/blogs/machine-learning/amazon-sagemaker-ai-async-inference-now-supports-inline-request-payloads
scenarios: ["后端开发"]
---

# Amazon SageMaker AI异步推理支持内联Payload，无需上传S3

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-06-17T20:56:36+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/amazon-sagemaker-ai-async-inference-now-supports-inline-request-payloads](https://aws.amazon.com/blogs/machine-learning/amazon-sagemaker-ai-async-inference-now-supports-inline-request-payloads)

---
## 摘要/简介

今天，我们宣布Amazon SageMaker AI异步推理支持内联Payload功能。客户现在可以直接在InvokeEndpointAsync API的请求体中发送推理Payload，无需在每次调用前将输入数据上传到Amazon Simple Storage Service (Amazon S3)。

---
## 导语

Amazon SageMaker AI 异步推理现已支持内联请求 Payload。客户无需在每次调用前将输入数据上传至 Amazon S3，可直接在 InvokeEndpointAsync API 的请求体中发送推理负载。此举简化了推理流程，降低了交互延迟，并帮助团队更高效地将机器学习模型部署到生产环境。

---
## 摘要

Amazon SageMaker AI 异步推理现已支持在请求体中直接携带输入数据（inline payload），使用户无需在调用前先将数据上传至 Amazon S3。通过 InvokeEndpointAsync API，可直接在请求体内发送推理载荷，实现更简化的调用流程，降低延迟并提升效率。

---
## 评论

#### 中心观点

Inline payload支持的引入是SageMaker异步推理体验的一次重要简化。这一变化消除了开发者必须预先上传数据到S3的硬性约束，使得调用流程更加直接。从技术实现角度看，这降低了异步推理的使用门槛，尤其适合需要快速验证模型效果或构建轻量级推理管道的场景。

#### 支撑理由

**事实陈述**：此前调用InvokeEndpointAsync API必须指定S3对象位置，推理请求的执行依赖于预先完成的数据上传步骤。这一设计在处理大文件或需要数据复用的场景下是合理的，但对于即时性要求高、数据量适中的场景则显得冗余。

**作者观点**：从API设计原则来看，减少不必要的外部依赖是提升开发者效率的有效手段。Inline payload的加入使得异步推理的调用模式与同步推理更加一致，降低了开发者在不同推理方式间切换时的认知负担。

**你的推断**：这一改动可能反映出AWS在评估客户反馈后，意识到原有设计对部分实时性要求较高的交互场景支持不足。Inline payload的引入有望吸引更多原本倾向于使用同步推理或第三方方案的用户。

#### 边界条件

需要注意的是，inline payload并非适用于所有场景。请求体直接传输意味着payload大小受到API请求上限的约束，对于超大输入数据或需要跨请求复用的场景，S3存储模式仍是更合适的选择。此外，直接在请求中携带数据可能带来安全审计层面的考量，企业在实际部署时需结合自身合规要求进行评估。

#### 实践启发

对于MLOps工程师而言，这一功能为快速原型验证提供了便利。在模型调优迭代阶段，可以直接通过脚本发起异步推理请求，无需额外维护S3上传流程。对于构建事件驱动型推理管道的设计者，inline payload与Lambda等触发器的组合将更加自然。需要提醒的是，生产环境中的payload大小监控和错误处理逻辑仍需妥善设计，以应对因数据体积超限导致的请求失败。

---
## 学习要点

- SageMaker AI 异步推理现已支持直接在请求体中嵌入请求负载，无需先将负载上传到 S3。
- 内联负载大小限制为 6 MB，足以满足大多数中等规模的推理需求。
- 通过省去 S3 读取步骤，请求延迟显著降低，整体工作流更简洁。
- 无需额外的 S3 读取权限，简化了 IAM 角色配置和安全策略。
- 对于超过内联大小限制的负载，仍然可以使用原有的 S3 负载方式，保证兼容性。
- 该功能在所有现有的 SageMaker 端点上开箱即用，模型代码无需任何修改。
- 可通过 AWS SDK、SageMaker CLI 或控制台直接使用，方便快速集成。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/amazon-sagemaker-ai-async-inference-now-supports-inline-request-payloads](https://aws.amazon.com/blogs/machine-learning/amazon-sagemaker-ai-async-inference-now-supports-inline-request-payloads)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [异步推理](/tags/%E5%BC%82%E6%AD%A5%E6%8E%A8%E7%90%86/) / [内联请求](/tags/%E5%86%85%E8%81%94%E8%AF%B7%E6%B1%82/) / [AWS](/tags/aws/) / [S3](/tags/s3/) / [机器学习](/tags/%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0/) / [API调用](/tags/api%E8%B0%83%E7%94%A8/) / [低延迟](/tags/%E4%BD%8E%E5%BB%B6%E8%BF%9F/) / [效率提升](/tags/%E6%95%88%E7%8E%87%E6%8F%90%E5%8D%87/)
- 场景： [后端开发](/scenarios/%E5%90%8E%E7%AB%AF%E5%BC%80%E5%8F%91/)

### 相关文章

- [基于 Union.ai 和 Flyte 在 Amazon EKS 上构建 AI 工作流]({{< relref "posts/20260220-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--9.md" >}})
- [基于 Union.ai 与 Flyte 在 Amazon EKS 上构建 AI 工作流]({{< relref "posts/20260222-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--11.md" >}})
- [基于 Union.ai 和 Flyte 在 Amazon EKS 上构建 AI 工作流]({{< relref "posts/20260223-blogs_podcasts-build-ai-workflows-on-amazon-eks-with-unionai-and--11.md" >}})
- [在 EC2 上使用 Oumi 微调并部署 Llama 至 Amazon Bedrock]({{< relref "posts/20260311-blogs_podcasts-accelerate-custom-llm-deployment-fine-tune-with-ou-4.md" >}})
- [Amazon Quick Flows AI工作流程搭建指南]({{< relref "posts/20260427-blogs_podcasts-automate-repetitive-tasks-with-amazon-quick-flows-0.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*