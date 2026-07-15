---
title: Amazon Bedrock AgentCore Runtime的WAF安全防护架构
date: 2026-07-08 16:56:13+08:00
draft: false
entry_kind: auto
tags:
- AWS WAF
- VPC安全
- 负载均衡
- Lambda代理
- 安全架构
- SigV4认证
- OAuth认证
- Bedrock
categories:
- 安全
- 系统与基础设施
source: blogs_podcasts
description: 架构概览 通过在公网入口放置面向 Internet 的 ALB（Application Load Balancer），在其上绑定 AWS
  WAF Web ACL，将流量统一先经过 WAF 过滤后，再通过 VPC Interface Endpoint 转发至 Amazon Bedrock AgentCore
  Runtim
external_url: https://aws.amazon.com/blogs/machine-learning/securing-amazon-bedrock-agentcore-runtime-with-aws-waf
scenarios:
- AI/ML项目
content_mode: legacy_analysis
publication_tier: LEGACY
source_provenance: legacy_no_snapshot
source_support: 0.0
---

# Amazon Bedrock AgentCore Runtime的WAF安全防护架构

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-07-08T15:57:33+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/securing-amazon-bedrock-agentcore-runtime-with-aws-waf](https://aws.amazon.com/blogs/machine-learning/securing-amazon-bedrock-agentcore-runtime-with-aws-waf)

---
## 摘要/简介

这篇文章为您展示了两种解决此问题的架构模式。两者均使用面向互联网的 ALB（应用负载均衡器），并通过 AWS WAF 进行流量过滤，然后经由 VPC Interface Endpoint 路由至 AgentCore Runtime。

模式一：在 ALB 和 VPC Endpoint 之间部署 AWS Lambda 代理，使您能够完全控制请求转换逻辑。

模式二：直接从 ALB 定向到 VPC Endpoint ENI IP 地址，完全省去了 Lambda 这一环节。

此外，您还将了解到如何通过资源策略关闭直接访问的后门通道，确保所有流量都必须经过 AWS WAF 检查。

两种模式均已通过端到端测试，支持 SigV4 和 OAuth（Amazon Cognito JWT）两种认证方式。

---
## 摘要

#### 架构概览
通过在公网入口放置面向 Internet 的 ALB（Application Load Balancer），在其上绑定 AWS WAF Web ACL，将流量统一先经过 WAF 过滤后，再通过 VPC Interface Endpoint 转发至 Amazon Bedrock AgentCore Runtime。两种方案均实现只允许 WAF 审查后的请求访问后端，同时通过资源策略封堵直接访问的“后门”。

#### 模式一：Lambda 代理
在 ALB 与 VPC Endpoint 之间插入一个 Lambda 函数。Lambda 可在请求进入 AgentCore 之前完成完整的请求体/头转换、签名校验、业务鉴权等逻辑。此模式适用于需要对请求进行细粒度加工或自定义认证流程的场景，且 Lambda 的执行环境与 VPC Endpoint 安全组配合即可实现细粒度访问控制。

#### 模式二：直接 ENI 路由
将 ALB 的目标直接指向 VPC Endpoint 的弹性网络接口（ENI）IP，绕过 Lambda。此方案省去一次函数调用，降低延迟，但失去在网络层进行请求改写的能力。实现要点是 ALB 目标组使用 IP 类型并指定 Endpoint ENI 地址，同时配合安全组只开放必要端口。

#### 访问控制策略
为 VPC Endpoint 配置资源策略（Resource Policy），显式拒绝所有来源不是 ALB/WAF 的流量。通过条件限制如 `aws:SourceVpce` 或 `aws:SourceIp`，确保即使攻击者获取到 ENI IP 也无法直接访问 AgentCore，所有请求只能经由 WAF 过滤后到达。

#### 验证与兼容性
两种模式均已在真实环境中端到端测试，兼容 AWS SigV4 签名以及 Amazon Cognito JWT（OAuth）两种认证方式。测试结果显示在加入 Lambda 或直接 ENI 路由后，认证流程、签名校验和授权检查均不受影响，满足安全与功能的双重要求。

---
## 评论

#### 核心观点
文章提出的两套模式均通过在公共 ALB 前置 WAF、流量经由 VPC Interface Endpoint 进入 Bedrock AgentCore，实现对 AI 推理入口的“分层过滤”。其中 Pattern 1 在 ALB 与 Endpoint 之间加入 Lambda 代理，可视为“可控拦截层”，而 Pattern 2 则保持最简路径，侧重降低运维复杂度。

#### 支撑理由
- 【事实】ALB 与 WAF 的组合已在 AWS 官方安全最佳实践中被广泛推荐；VPC Interface Endpoint 将流量限制在 AWS 内部网络，避免公网暴露。
- 【作者观点】作者认为 Lambda 代理能够提供细粒度的请求校验、流量审计和自定义响应，从而提升安全可观测性。
- 【推断】从行业趋势看，越来越多的 AI 推理平台要求在模型入口实现零信任访问控制，Lambda 的可编程特性恰好满足此需求。

#### 边界条件
- 【事实】Lambda 有冷启动和执行时长上限（约 15 分钟），对高并发或长时间推理场景可能产生额外时延。
- 【作者观点】作者指出如果业务对响应延迟不敏感，Lambda 代理仍可接受。
- 【推断】在多租户或大规模并发请求时，需额外评估 Lambda 并发配额与费用，否则成本可能超出预期。

#### 实践启发
- 在安全与性能之间权衡，若仅需基础的请求过滤和日志记录，可直接使用 Pattern 2，避免 Lambda 引入的额外开销。
- 若业务需要动态路由、身份验证或自定义响应体，建议在 Pattern 1 中加入幂等的 Lambda 函数并设置合理的超时与重试策略。
- 结合 AWS WAF 的托管规则与自有 IP 黑名单，定期审计规则顺序，防止低优先级规则被高优先级规则覆盖。
- 对成本敏感的项目，可通过 CloudWatch 监控 Lambda 调用次数与平均执行时长，结合 VPC Endpoint 的流量计费，评估整体费用是否在预算范围内。

---
## 技术分析

#### 核心观点
文章提出两套基于 AWS WAF 与 VPC Interface Endpoint 的安全架构，用于保护 Amazon Bedrock AgentCore Runtime 免受外部攻击和误用。核心思路是通过互联网可访问的 ALB 统一入口、使用 AWS WAF 进行请求过滤，再经由 VPC Interface Endpoint 将可信流量导向私有子网，实现 **流量不出公网、过滤在边缘、业务逻辑可插拔** 的多层防御。

##### 关键要点
- **统一入口**：使用 Internet‑facing ALB 接受外部请求，配合 AWS WAF 规则实现恶意 IP、SQL 注入、XSS、地理封锁等防护。
- **私有链路**：VPC Interface Endpoint（PrivateLink）提供从 ALB 到 AgentCore 的加密通道，流量全程在 AWS 内部网络，避免穿越公网。
- **Lambda 代理（可选）**：在 ALB 与 Endpoint 之间插入 Lambda 函数，可对请求进行自定义校验、协议转换或限流，适用于复杂业务逻辑或监管要求的细粒度控制。
- **安全基线**：通过安全组、IAM 端点策略、TLS 加密、VPC Flow Logs 与 CloudWatch 组合，实现可观测、可审计的闭环。

#### 关键技术点
- **AWS WAF**：支持托管规则（OWASP、CrowdSec）和自定义规则，提供实时阻断、日志输出至 CloudWatch，便于事后分析。
- **VPC Interface Endpoint**：使用私有 IP，提供跨 AZ 高可用，所有流量加密，满足金融、医疗等合规场景的“数据不出网”要求。
- **Lambda 代理**：无服务器执行模型，冷启动延迟可通过 Provisioned Concurrency 缓解；可配合 API Gateway 内部触发器做请求签名校验。
- **安全组 & 端点策略**：默认仅允许 ALB 所在的子网访问，其他 CIDR 均被拒绝；IAM 端点策略限定仅授权的 ALB/ Lambda 能调用。
- **日志与监控**：WAF 日志写入 CloudWatch Logs；VPC Flow Logs 捕获端点流量；CloudTrail 记录 API 调用，形成完整审计链。

#### 实际应用价值
- **降低攻击面**：所有入口统一受 WAF 过滤，未匹配规则的请求直接被丢弃，AgentCore 不直接暴露在公网。
- **提升合规性**：PrivateLink 保证数据在 AWS 内部传输，满足 PCI‑DSS、HIPAA 对“网络隔离”和“加密传输”的要求。
- **灵活业务校验**：Lambda 代理可在进入 AgentCore 前执行 JWT 校验、业务限流、数据脱敏等，降低后端业务代码的风险。
- **运维简化**：利用 AWS 托管的 WAF 与 PrivateLink，减少自建防火墙和 VPN 的运维成本，同时支持自动弹性伸缩。

#### 行业影响
- 为 **生成式 AI 工作负载** 的安全防护提供可落地的参考模型，促进 AI 平台在企业内部的快速采纳。
- 推动 **云原生安全** 从传统网络安全向“应用层 + 网络层”双层防护演进，形成以 WAF、PrivateLink、Lambda 为代表的安全服务组合。
- 为 **多租户 AI SaaS** 提供细粒度隔离方案，帮助提供商在共享基础设施上实现“租户级别”的访问控制和数据隔离。

#### 边界条件与实践建议
##### 边界条件
- **WAF 规则冲突**：规则顺序不当可能导致误拦或漏拦，需要定期审计规则优先级。
- **Lambda 冷启动**：高并发场景下冷启动会影响响应时延，建议开启 Provisioned Concurrency 或使用 ALB 的目标组预热。
- **端点配额**：每个 VPC 区域最多 20 个 Interface Endpoint，超出需提前申请或拆分子网。
- **成本**：WAF 按请求计费，大流量业务需评估费用模型；Lambda 调用次数与运行时间亦会产生费用。

##### 实践建议
1. **先部署 Pattern 1**（ALB → WAF → VPC Endpoint），验证无 Lambda 时的防护效果与性能基线。
2. **根据业务需求逐步引入 Lambda 代理**，在不影响主路径的前提下做灰度验证。
3. **开启 WAF 日志并关联 CloudWatch Dashboard**，实时监控被拦截的请求类型与频率。
4. **使用 AWS Firewall Manager** 跨账户统一 WAF 规则，确保合规策略一致性。
5. **在 Lambda 中实现幂等校验**（如去重、签名验证），防止重放攻击。
6. **定期审计端点 IAM 策略**，确保仅授权服务可调用，避免误开放导致的横向移动风险。

#### 论证地图
##### 中心命题
通过 ALB + AWS WAF + VPC Interface Endpoint（可选 Lambda 代理）可在不暴露 AgentCore 公网入口的前提下，实现细粒度访问控制与流量安全。

##### 支撑理由
1. **边缘过滤**：WAF 能阻断常见攻击向量，降低后端负载。
2. **私有连通**：PrivateLink 确保流量不经过公网，防止数据泄漏。
3. **可编程防护**：Lambda 代理提供业务层定制校验，满足合规和业务特定需求。
4. **可观测**：WAF、VPC Flow Logs、CloudTrail 形成完整的审计链，便于事后取证。

##### 反例或边界条件
- 若 WAF 规则配置错误（优先级颠倒、误加白名单），可能导致合法请求被误拦或恶意请求被放行。
- Lambda 代理若出现超时或错误，会阻断业务请求，需要配合熔断和降级策略。
- 端点策略若过于宽松（如允许所有 IP），会削弱 PrivateLink 的隔离价值。

##### 可验证方式
- **渗透测试**：使用 AWS WAF tester 模拟 SQL 注入、XSS、IP 黑名单等攻击，验证阻断率。
- **网络路径验证**：在 VPC Flow Logs 中确认所有业务流量仅通过 Interface Endpoint，未出现公网 IP。
- **日志审计**：检查 CloudTrail 中的 `CreateVpcEndpoint`、`PutRule` 等操作是否符合最小权限原则。
- **性能基准**：对比有无 Lambda 代理的 P99 延迟，评估冷启动对业务的实际影响。

---

通过上述结构化分析，可清晰看到该方案在提升 AI 推理服务安全性的同时，兼顾了灵活性与可观测性，适用于对数据合规和网络隔离有严格要求的行业场景。

---
## 学习要点

- 使用 AWS WAF 的 Web ACL 对 Bedrock AgentCore 入站流量进行精细化控制，阻断已知恶意 IP。
- 通过基于 URI、请求方法、请求头等条件的 WAF 规则过滤异常请求，防止注入和跨站脚本等攻击。
- 启用 WAF 速率限制规则防止暴力破解或突发流量冲击，保障 AgentCore 的可用性。
- 将 WAF 与 CloudFront 或 ALB 集成，实现多层防护并统一监控入口流量。
- 开启 WAF Bot Control 功能识别并阻止自动化脚本对 AgentCore 的滥用行为。
- 利用 WAF 日志结合 CloudWatch 进行实时监控和告警，快速发现并响应安全事件。
- 定期审计和更新 WAF 规则，配合 AWS Config 与 Security Hub 确保合规性管理。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/securing-amazon-bedrock-agentcore-runtime-with-aws-waf](https://aws.amazon.com/blogs/machine-learning/securing-amazon-bedrock-agentcore-runtime-with-aws-waf)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [安全](/categories/%E5%AE%89%E5%85%A8/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [AWS WAF](/tags/aws-waf/) / [VPC安全](/tags/vpc%E5%AE%89%E5%85%A8/) / [负载均衡](/tags/%E8%B4%9F%E8%BD%BD%E5%9D%87%E8%A1%A1/) / [Lambda代理](/tags/lambda%E4%BB%A3%E7%90%86/) / [安全架构](/tags/%E5%AE%89%E5%85%A8%E6%9E%B6%E6%9E%84/) / [SigV4认证](/tags/sigv4%E8%AE%A4%E8%AF%81/) / [OAuth认证](/tags/oauth%E8%AE%A4%E8%AF%81/) / [Bedrock](/tags/bedrock/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [OpenAI 实时访问系统：结合速率限制与额度管理支持 Sora 和 Codex]({{< relref "posts/20260213-blogs_podcasts-beyond-rate-limits-scaling-access-to-codex-and-sor-0.md" >}})
- [OpenAI 实时访问系统：融合速率限制与额度管理保障 Sora 和 Codex 稳定运行]({{< relref "posts/20260213-blogs_podcasts-beyond-rate-limits-scaling-access-to-codex-and-sor-0.md" >}})
- [OpenAI 实时接入系统：结合速率限制与额度管理支撑 Sora 与 Codex]({{< relref "posts/20260213-blogs_podcasts-beyond-rate-limits-scaling-access-to-codex-and-sor-0.md" >}})
- [传统 Nginx 流量层难以适配 AI 服务，需重新设计]({{< relref "posts/20260223-juejin-你的-nginx-在扼杀-ai-服务为什么需要重新设计流量层-0.md" >}})
- [基于Amazon SageMaker AI构建无服务器对话AI代理]({{< relref "posts/20260302-blogs_podcasts-build-a-serverless-conversational-ai-agent-using-c-1.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*
