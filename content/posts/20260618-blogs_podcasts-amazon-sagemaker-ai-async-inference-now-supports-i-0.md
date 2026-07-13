---
title: "SageMaker异步推理可直接发送推理负载无需S3"
date: 2026-06-18T04:08:43+08:00
draft: false
entry_kind: "auto"
tags: ["异步推理", "内联负载", "S3", "API 调用", "AWS", "推理优化", "机器学习部署", "云服务"]
categories: ["AI 工程", "系统与基础设施"]
source: blogs_podcasts
description: "Amazon SageMaker AI 异步推理现已支持直接在请求体中携带推理负载。调用 InvokeEndpointAsync API 时，用户无需先把输入数据上传至 Amazon S3，直接将负载嵌入请求体即可完成推理。此举简化了工作流程，降低了调用延迟，尤其适合中小规模的输入数据。平台仍保留原有的 S3 存储方式"
external_url: https://aws.amazon.com/blogs/machine-learning/amazon-sagemaker-ai-async-inference-now-supports-inline-request-payloads
scenarios: ["后端开发"]
---

# SageMaker异步推理可直接发送推理负载无需S3

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-06-17T20:56:36+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/amazon-sagemaker-ai-async-inference-now-supports-inline-request-payloads](https://aws.amazon.com/blogs/machine-learning/amazon-sagemaker-ai-async-inference-now-supports-inline-request-payloads)

---
## 摘要/简介

今天，我们宣布为 Amazon SageMaker AI 异步推理推出内联负载支持。客户现在可以直接在 InvokeEndpointAsync API 的请求正文中发送推理负载，无需再在每次调用前将输入数据上传到 Amazon Simple Storage Service (Amazon S3)。

---
## 导语

Amazon SageMaker AI 为异步推理新增内联负载功能，调用方现在可以直接在 InvokeEndpointAsync 请求正文中提交推理数据，无需预先上传至 Amazon S3。此改进简化了模型部署工作流，降低调用延迟和运维成本，帮助开发者更快将机器学习模型投入生产。对需要在实时或批量场景下频繁发起推理请求的团队，这一特性提供了更直观、更高效的 API 使用方式。

---
## 摘要

Amazon SageMaker AI 异步推理现已支持直接在请求体中携带推理负载。调用 InvokeEndpointAsync API 时，用户无需先把输入数据上传至 Amazon S3，直接将负载嵌入请求体即可完成推理。此举简化了工作流程，降低了调用延迟，尤其适合中小规模的输入数据。平台仍保留原有的 S3 存储方式，用户可依据数据大小和业务需求自由选择。该功能已正式上线，使用时只需在 API 调用时提供原始或 Base64 编码的负载，无需额外代码改动。

---
## 技术分析

#### 核心观点
Amazon SageMaker AI 异步推理现已支持在 `InvokeEndpointAsync` 请求体中直接携带推理载荷（inline payload），无需提前将数据上传至 S3。该功能简化了客户端调用链路，降低了延迟和运营成本，同时保持了原有的异步处理能力和弹性扩展特性。

##### 关键技术点
- **Inline Payload 接口**：在 `InvokeEndpointAsync` 请求的 `InputData` 字段直接写入二进制或文本载荷，最大可支持约 256 KB（具体上限取决于账户配额）。
- **无需预置 S3 对象**：相较于传统流程（上传 → 引用 S3 URI），新方式省略了对象写入和路径管理步骤。
- **异步语义保持**：仍通过异步队列调度推理任务，支持超时、重试、Dead‑Letter Queue 等配置。
- **兼容性**：已有的 S3 引用方式继续可用，用户可根据载荷大小自行选择上传或内联。

##### 实际应用价值
1. **降低调用延迟**：省去上传 S3 的网络往返，尤其在模型推理需要快速响应的场景（如实时推荐、异常检测）中收益明显。
2. **简化开发与运维**：客户端只需构造请求体，无需维护 S3 bucket、路径映射及清理逻辑。
3. **成本节约**：S3 存储与请求费用下降，尤其在大量小请求的批处理或交互式推理时。
4. **更灵活的工作流**：结合事件驱动的 Lambda、Step Functions，可实现“即时请求‑即时响应”模式，提升整体系统弹性。

##### 行业影响
- **开发者体验提升**：减少对外部存储的依赖，使云原生机器学习工作流更易于在边缘、移动端等受限环境中部署。
- **推动无服务器 AI**：与 AWS Lambda、AppSync 等服务深度结合，促进 AI 即服务（AIAAS）方案的快速落地。
- **竞争格局**：其他云厂商若未提供类似的内联载荷功能，可能在易用性和响应速度上被拉开差距。

##### 边界条件与实践建议
- **载荷大小限制**：超出上限的 payload 仍需使用 S3 上传，否则会返回 `PayloadTooLarge` 错误。建议在调用前进行大小检查。
- **错误处理差异**：内联方式在网络中断时更容易出现请求体被截断，需要在客户端实现幂等重试机制。
- **安全合规**：直接携带数据的请求会经过 API Gateway，需确保使用 TLS 并配置 IAM 角色最小权限。
- **监控与日志**：结合 CloudWatch Metrics 监控 `AsyncInvoke` 的成功率和延迟，结合 S3 访问日志审计大文件上传。
- **混合策略**：对大模型输入或需要持久化的数据，继续使用 S3；对小体积、时延敏感的请求，切换至 inline payload，实现成本与性能的平衡。

#### 论证地图
##### 中心命题
Inline payload 支持让 SageMaker 异步推理在保持弹性扩展的前提下，实现更低的请求延迟和更简化的调用模型。

##### 支撑理由
1. **网络往返削减**：一次 HTTP 请求即可完成推理调用，省去上传 S3 的额外 RTT。
2. **运维简化**：无需维护 S3 bucket 权限、生命周期策略及对象清理，降低管理成本。
3. **成本结构优化**：S3 读写费用下降，特别在高频小请求场景中费用节省明显。
4. **兼容性保留**：旧有 S3 引用路径仍然可用，用户可平滑迁移，无需一次性改造全部服务。

##### 反例或边界条件
- 当推理输入超过 256 KB 时，仍必须使用 S3，否则会触发 `PayloadTooLarge`。
- 在网络不稳定或高延迟环境下，直接携带大量数据可能导致请求超时，增加重试压力。
- 某些合规场景要求审计日志必须记录所有持久化数据，内联载荷的瞬时特性可能不符合审计要求，需要额外日志记录机制。

##### 可验证方式
- **功能测试**：在相同模型和输入条件下，分别使用 S3 引用和 inline payload 测量端到端延迟，对比差异。
- **容量上限验证**：构造接近 256 KB 的 payload，观察返回错误并确认错误信息与官方文档一致。
- **成本分析**：使用 CloudWatch Cost Explorer 对比同一时间段内 S3 请求费用与 API 调用费用，量化节约比例。
- **安全审计**：检查 IAM Policy 是否仅授予 `sagemaker:InvokeEndpointAsync` 必要权限，并验证 TLS 加密是否生效。
- **错误恢复测试**：模拟网络中断，检查客户端重试机制是否能够成功恢复并避免重复计费。

---
## 学习要点

- 支持在 API 请求中直接携带推理载荷，无需预先上传至 S3，显著简化工作流程并降低延迟。
- 可处理更大的载荷大小突破了原有的 S3 对象大小限制，适合复杂输入场景。
- 减少了对中间存储的依赖，降低了运营成本并提升了数据安全性。
- 与现有的 SageMaker 功能（如自动伸缩、模型监控）无缝集成，保持功能完整性。
- 提供可选的回调 URL，实现异步通知，进一步提升异步推理的灵活性。
- 统一的请求体格式让开发者无需学习新的 SDK 调用方式，降低学习成本。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/amazon-sagemaker-ai-async-inference-now-supports-inline-request-payloads](https://aws.amazon.com/blogs/machine-learning/amazon-sagemaker-ai-async-inference-now-supports-inline-request-payloads)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [异步推理](/tags/%E5%BC%82%E6%AD%A5%E6%8E%A8%E7%90%86/) / [内联负载](/tags/%E5%86%85%E8%81%94%E8%B4%9F%E8%BD%BD/) / [S3](/tags/s3/) / [API 调用](/tags/api-%E8%B0%83%E7%94%A8/) / [AWS](/tags/aws/) / [推理优化](/tags/%E6%8E%A8%E7%90%86%E4%BC%98%E5%8C%96/) / [机器学习部署](/tags/%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0%E9%83%A8%E7%BD%B2/) / [云服务](/tags/%E4%BA%91%E6%9C%8D%E5%8A%A1/)
- 场景： [后端开发](/scenarios/%E5%90%8E%E7%AB%AF%E5%BC%80%E5%8F%91/)

### 相关文章

- [Amazon SageMaker AI异步推理支持内联负载功能]({{< relref "posts/20260617-blogs_podcasts-amazon-sagemaker-ai-async-inference-now-supports-i-0.md" >}})
- [Amazon SageMaker AI 2025回顾：弹性训练计划与推理性价比提升]({{< relref "posts/20260221-blogs_podcasts-amazon-sagemaker-ai-in-2025-a-year-in-review-part--1.md" >}})
- [Amazon SageMaker AI 2025：弹性训练与推理优化]({{< relref "posts/20260223-blogs_podcasts-amazon-sagemaker-ai-in-2025-a-year-in-review-part--6.md" >}})
- [2025年Amazon SageMaker AI回顾：灵活训练计划与推理性价比提升]({{< relref "posts/20260223-blogs_podcasts-amazon-sagemaker-ai-in-2025-a-year-in-review-part--7.md" >}})
- [2025年Amazon SageMaker AI回顾：弹性训练计划与推理性价比优化]({{< relref "posts/20260224-blogs_podcasts-amazon-sagemaker-ai-in-2025-a-year-in-review-part--9.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*