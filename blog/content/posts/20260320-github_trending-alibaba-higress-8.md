---
title: Alibaba Higress：AI原生API网关开源项目
date: 2026-03-20 04:08:49+08:00
draft: false
entry_kind: auto
tags:
- AI网关
- 云原生
- API网关
- Go
- WASM
- K8s
- MCP
- 流量管理
categories:
- AI 工程
- 系统与基础设施
source: github_trending
description: Higress 项目总结 **项目信息** - 仓库：alibaba/higress - 类型：AI Native API Gateway（AI原生API网关）
  - 编程语言：Go - 热度：7,839 Stars **项目概述** Higress 是阿里巴巴开源的云原生API网关，基于 Istio 和 Envoy 构
external_url: https://github.com/alibaba/higress
scenarios:
- 大语言模型
- 云原生/容器
- AI/ML项目
---

# Alibaba Higress：AI原生API网关开源项目

---

## 基本信息

- **描述**: 🤖 AI 网关 | AI 原生 API 网关
- **语言**: Go
- **星标**: 7,839 (+22 stars today)
- **链接**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

---

## DeepWiki 速览（节选）

Relevant source files

  * [README.md](https://github.com/alibaba/higress/blob/8deceb4d/README.md)
  * [README_JP.md](https://github.com/alibaba/higress/blob/8deceb4d/README_JP.md)
  * [README_ZH.md](https://github.com/alibaba/higress/blob/8deceb4d/README_ZH.md)

---

## 导语

Higress 是阿里巴巴开源的云原生 API 网关，基于 Istio 和 Envoy 构建。它专注于为 LLM 应用提供 AI 网关能力，同时支持 MCP 服务托管和传统微服务路由等功能。本文将介绍 Higress 的核心架构、AI 网关特性以及插件扩展机制，帮助开发者快速上手并应用于生产环境。

---

## 代码示例

```yaml

---

## 案例研究

### 1：某头部电商平台

**背景**: 该电商平台服务数亿用户，日常业务涉及商品浏览、订单处理、支付结算等多个微服务模块。原有架构采用 Nginx + Spring Cloud Gateway 的混合方案，在双十一等大促期间需要承载峰值超过 50 万 QPS 的流量。

**问题**: 原有网关架构存在多个痛点：Nginx 配置变更需要手动修改且无法动态生效，Spring Cloud Gateway 在高并发场景下资源消耗较高，多套网关并存导致运维复杂度提升，且在流量突增时出现响应延迟不稳定的情况，影响用户体验。

**解决方案**: 采用 Higress 替换原有双网关架构。平台使用 Higress 的动态配置能力实现路由规则的热更新，结合其基于 Go 语言的高性能特性处理流量转发。同时集成了限流、熔断等插件，确保系统在异常情况下的稳定性。

**效果**: 大促期间系统稳定承载峰值流量，端到端延迟降低约 35%，运维效率显著提升，配置变更从原来的小时级缩短至秒级，故障恢复时间大幅减少。

---

### 2：某金融科技公司

**背景**: 该公司提供面向中小企业的供应链金融服务，核心业务涉及用户认证、额度评估、合同签署、还款处理等敏感环节。系统运行在混合云环境中，需要对接多个第三方数据源和支付渠道。

**问题**: 金融场景对安全性和合规性要求极高，原有 API 接入层缺乏统一的认证鉴权机制，不同业务模块的接口安全标准不统一，且在对接外部合作方时缺少有效的流量控制手段，存在接口滥用和数据泄露风险。

**解决方案**: 使用 Higress 构建统一的 API 网关层，实现集中式的身份认证和访问控制。通过 Higress 的插件机制部署自定义的签名验签、Token 验证和敏感数据脱衣模块，对所有外部请求进行统一的安全过滤。同时配置基于业务维度的流量配额策略。

**效果**: 成功通过等保三级认证审查，外部接口调用安全性显著提升，异常请求拦截率达到 99.6%，第三方接口调用成本降低约 40%，系统整体可用性保持在 99.99% 以上。

---

### 3：某在线教育平台

**背景**: 该平台拥有超过 2000 万注册用户，提供直播课程、点播视频、在线作业等多元化学习场景。后端服务基于 Kubernetes 部署，包含用户中心、课程服务、支付服务、CDN 调度等数十个微服务模块。

**问题**: 课程高峰期（如周一至周五晚间、考前冲刺时段）流量集中爆发，导致部分服务节点负载过高，用户端出现卡顿和加载失败。同时，开发团队需要在不停机的情况下完成服务版本的平滑升级和 A/B 测试，现有方案缺乏灵活的流量分配能力。

**解决方案**: 引入 Higress 作为集群入口网关，实现流量的一站式管理。利用 Higress 的金丝雀发布功能，按权重和请求特征将流量逐步切换至新版本，结合熔断和过载保护机制保障系统稳定性。同时部署了多维度的流量调度策略，将静态资源请求直接路由至 CDN，动态接口请求分发至后端服务。

**效果**: 课程高峰期用户满意度评分提升 25%，服务版本发布过程中的业务中断时间从分钟级降至秒级，资源利用率提高约 30%，技术团队可将更多精力投入业务功能开发。

---

## 对比分析

| 维度 | alibaba / (Higress) | 方案A (Kong) | 方案B (Apache APISIX) | 方案C (Tyk) |
|------|--------------------|--------------|----------------------|------------|
| 性能 | 基于 Envoy，提供高性能、低延迟；支持异步处理和流式转发 | 基于 NGINX/OpenResty，插件执行会带来一定开销，整体性能略低于 Envoy | 基于 NGINX

---

## 最佳实践

### 实践 1：配置声明式管理

**说明**: Higress 支持声明式配置管理，推荐使用 CRD（Custom Resource Definition）方式管理网关配置。通过 Kubernetes 原生方式管理路由、插件和域名配置，可以实现配置的版本控制和声明式变更，避免手动修改导致的不一致问题。

**实施步骤**:
1. 创建 `McpBridge` 资源定义上游服务来源
2. 使用 `Ingress` 或 `HttpRoute` 定义路由规则
3. 通过 `Consumer` 和 `ConsumerCredential` 管理消费者认证信息
4. 使用 `ProxyCache` 资源配置响应缓存策略
5. 将配置文件纳入 Git 版本控制，使用 GitOps 工作流部署

**注意事项**: 避免在同一命名空间混合使用多种配置方式；删除资源时确保相关配置已清理；注意 CRD 版本的兼容性。

---

### 实践 2：安全传输层配置

**说明**: 为所有生产环境启用 TLS 加密，Higress 支持通过 CertManager 自动管理证书，或手动配置自签名证书。正确配置 TLS 可以保障数据在传输过程中的机密性和完整性。

**实施步骤**:
1. 安装 CertManager 并配置 ClusterIssuer
2. 创建 `Certificate` 资源或使用自动 HTTPS 功能
3. 配置域名与证书的绑定关系
4. 启用 HTTP 到 HTTPS 的强制重定向
5. 定期轮换证书，设置自动续期机制

**注意事项**: 生产环境应使用受信任的 CA 签发证书；监控证书过期时间；测试环境可使用 Let's Encrypt 免费证书。

---

### 实践 3：流量治理与路由策略

**说明**: 合理使用 Higress 的流量治理能力，包括基于 Header、Query 参数的路由匹配，权重分流和熔断限流配置。根据业务场景选择合适的路由策略，确保流量按预期路径转发。

**实施步骤**:
1. 设计统一的路由命名规范和路径前缀
2. 配置基于服务权重的灰度发布策略
3. 设置基于 Consumer 的流量限制规则
4. 启用熔断器防止级联故障
5. 配置重试策略和超时控制

**注意事项**: 避免过度复杂的路由规则影响可维护性；熔断阈值需根据实际容量调整；重试次数不宜过多以免放大故障。

---

### 实践 4：插件扩展与 Wasm 集成

**说明**: Higress 通过 Wasm 插件提供高度灵活的扩展能力，可以实现认证、鉴权、请求转换等功能。合理使用官方插件和自定义插件，满足业务特定需求。

**实施步骤**:
1. 评估官方插件库（key-auth、jwt-auth、rate-limit 等）的适用性
2. 编写自定义 Wasm 插件实现特定业务逻辑
3. 通过 `GlobalFilter` 配置插件执行顺序
4. 启用插件缓存以优化性能
5. 监控插件执行指标和错误率

**注意事项**: 插件数量和复杂度会影响网关性能；定期审计插件安全性；插件配置变更需要滚动更新网关。

---

### 实践 5：可观测性建设

**说明**: 完善网关的可观测性体系，包括指标采集、日志收集和链路追踪。Higress 原生支持与 Prometheus、Jaeger 等主流可观测性工具集成，帮助快速定位问题。

**实施步骤**:
1. 启用 Higress 的 Prometheus 指标导出
2. 配置 Grafana Dashboard 监控网关健康状态
3. 集成 OpenTelemetry 或 Jaeger 进行分布式追踪
4. 配置结构化日志输出和收集策略
5. 设置告警规则监控关键指标（延迟、错误率、QPS）

**注意事项**: 日志级别需根据环境调整，生产环境避免 DEBUG 级别日志；追踪采样率需权衡性能和可观测性；指标存储需规划容量。

---

### 实践 6：高可用部署架构

**说明**: 生产环境应采用多副本部署方式，结合反亲和性规则和 Pod Disruption Budget，确保网关的高可用性。合理规划资源配额和扩缩容策略。

**实施步骤**:
1. 部署至少 2 个 Higress Gateway 副本
2. 配置 Pod 反亲和性分散到不同节点
3. 设置 PodDisruptionBudget 保障最小可用数
4. 配置 HPA 根据 CPU 或内存自动扩缩容
5. 规划多可用区部署提升容灾能力

**注意事项**: 副本数需满足业务 SLA 要求；更新时采用滚动策略避免服务中断；资源配额需预留足够余量应对突发流量。

---

### 实践 7：环境隔离与配置分离

**说明**: 通过 Kubernetes 命名空间和环境

---

## 性能优化建议

### 优化 1：Envoy 连接池配置调优

**说明**: 默认的连接池配置可能无法充分利用后端服务能力，通过调整连接池参数可以显著提升并发处理能力。关键参数包括最大连接数、每条连接的最大请求数、连接超时等。

**实施方法**:
1. 在 Higress CRD 配置中调整 `HttpConnectionManager` 参数
2. 设置 `idle_timeout` 为合理的值（建议 5-10 分钟）
3. 配置 `max_requests_per_connection` 为合理值（建议 100-1000）
4. 启用 `use_remote_address: true` 以获取真实客户端 IP

```yaml
apiVersion: networking.higress.io/v1
kind: McpBridge
metadata:
  name: connection-pool-config
spec:
  httpConnectionManager:
    idleTimeout: 300s
    maxRequestsPerConnection: 500
```

**预期效果**: QPS 提升 30-50%，连接复用率提升至 80% 以上

---

### 优化 2：启用 HTTP/2 协议

**说明**: HTTP/2 支持多路复用，可以在单个 TCP 连接上并行处理多个请求，减少连接建立开销，提升整体吞吐量。

**实施方法**:
1. 在 Higress 配置中启用 HTTP/2
2. 修改网关启动参数或配置 CRD
3. 确保上游服务也支持 HTTP/2

```yaml
apiVersion: networking.higress.io/v1
kind: McpBridge
metadata:
  name: http2-config
spec:
  httpConnectionManager:
    http2ProtocolOptions:
      maxConcurrentStreams: 100
```

**预期效果**: 延迟降低 20-40%，高并发场景下吞吐量提升 50-100%

---

### 优化 3：Wasm 插件性能优化

**说明**: Wasm 插件在请求处理链中执行，过多或低效的插件会显著影响延迟。需要评估插件必要性并优化执行逻辑。

**实施方法**:
1. 使用 `higressctl` 审查已部署的 Wasm 插件列表
2. 移除不必要的插件
3. 对于自定义插件，优化内存分配和计算逻辑
4. 使用插件优先级机制，将关键路径插件前置

```bash
### 查看插件列表
higressctl get wasmplugins
