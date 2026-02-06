---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-02-06T22:08:51+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API网关", "AI原生", "LLM", "Istio", "Envoy", "WASM", "MCP协议"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "**Higress 项目总结** **项目概况：** Higress 是由阿里巴巴开源的**云原生 API 网关**，基于 Go 语言开发。它建立在 Istio 和 Envoy 之上，定位为一款 **AI Native（AI 原生）** 的 API 网关。目前该项目在 GitHub 上拥有约 7,470 个星标。 **"
external_url: https://github.com/alibaba/higress
scenarios: ["AI/ML项目", "大语言模型", "云原生/容器"]
---

# 阿里开源 Higress：AI 原生 API 网关

> **原名**: alibaba /

      higress

---

## 基本信息

- **描述**: 🤖 AI 网关 | AI 原生 API 网关
- **语言**: Go
- **星标**: 7,470 (+8 stars today)
- **链接**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

---
## DeepWiki 速览（节选）

# Overview

Relevant source files

  * [README.md](https://github.com/alibaba/higress/blob/8deceb4d/README.md)
  * [README_JP.md](https://github.com/alibaba/higress/blob/8deceb4d/README_JP.md)
  * [README_ZH.md](https://github.com/alibaba/higress/blob/8deceb4d/README_ZH.md)



## Purpose and Scope

This document provides a comprehensive overview of Higress, an AI Native API Gateway built on Istio and Envoy. It covers the system's architecture, core components, and primary use cases. For detailed information about specific subsystems, refer to the Core Architecture (page 2), Build and Deployment (page 3), WASM Plugin System (page 4), AI Gateway Features (page 5), MCP System (page 6), and Development Guide (page 7) sections.

## What is Higress

Higress is a cloud-native API gateway that extends Istio and Envoy with WebAssembly (WASM) plugin capabilities. The system provides three core functions: AI gateway features for LLM applications, MCP server hosting for AI agent tool integration, and traditional API gateway capabilities including Kubernetes Ingress and microservice routing.

The architecture separates control plane (configuration management) from data plane (traffic processing). Configuration changes propagate through the xDS protocol with millisecond latency and no connection disruption, making it suitable for long-connection scenarios such as AI streaming responses.

**Primary Use Cases:**

Use Case| Description| Core Components  
---|---|---  
**AI Gateway**|  Unified API for 30+ LLM providers with protocol translation, observability, caching, and security| `ai-proxy`, `ai-statistics`, `ai-cache`, `ai-security-guard` plugins  
**MCP Server Hosting**|  Host Model Context Protocol servers enabling AI agents to call tools and services| `mcp-router`, `jsonrpc-converter` filters + MCP server implementations (`quark-search`, `amap-tools`, `all-in-one`)  
**Kubernetes Ingress**|  Ingress controller with compatibility for nginx-ingress annotations| `higress-controller`, Ingress/Gateway API translation to Istio configs  
**Microservice Gateway**|  Service discovery from multiple registries (Nacos, Consul, ZooKeeper, Eureka)| `McpBridgeReconciler`, registry-specific watchers  
  
**Production Validation:**

Higress originated at Alibaba to address Tengine reload issues affecting long-connection services and insufficient gRPC/Dubbo load balancing. Within Alibaba Cloud, it supports core AI applications including Tongyi Qianwen (通义千问), Tongyi Bailian model studio, and PAI platform. The system handles hundreds of thousands of requests per second with 99.99% availability guarantees.

Sources: [README.md30-52](https://github.com/alibaba/higress/blob/8deceb4d/README.md#L30-L52)

## Core Architecture

Higress implements a control plane and data plane separation derived from Istio's architecture. The control plane watches Kubernetes resources and generates Envoy configurations distributed via xDS protocol. The data plane processes traffic through Envoy proxies extended with WASM plugins.

### System Components and Binaries

**Component Deployment Diagram:**


**Binary and Process Mapping:**

Binary| Source Entry Point| Deployment Location| Primary Functions  
---|---|---|---  
`higress-controller`| [cmd/higress/main.go1-100](https://github.com/alibaba/higress/blob/8deceb4d/cmd/higress/main.go#L1-L100)| Single pod in `higress-system`| Resource watching, `IngressController`, `WasmPluginController`, `McpBridgeReconciler`, service discovery management  
`pilot-discovery`| Istio upstream (patched)| Same pod as controller| xDS server implementation, configuration distribution on ports 15010 (gRPC), 15012 (gRPC-TLS), 15017 (webhook)  
`higress-gateway`| Envoy binary + extensions| DaemonSet or Deployment| Data plane proxy, WASM VM (V8), HTTP/HTTPS listeners on ports 80/443, admin API on 15021  
`hgctl`| [cmd/hgctl/main.go1-50](https://github.com/alibaba/higress/blob/8deceb4d/cmd/hgctl/main.go#L1-L50)| Local CLI tool| MCP server management, local development (`hgctl agent`, `hgctl mcp add`)  
  
**Key Process Communication:**

The controller and pilot run in the same pod and communicate via localhost gRPC on port 15051. The controller implements multiple Kubernetes controllers (`pkg/ingress/kube/`) that watch different resource types and update an in-memory cache (`pkg/ingress/kube/common/cache.go`). The cache state is pushed to pilot, which converts it to xDS configurations (Listener Discovery Service, Route Discovery Service, Cluster Discovery Service, Endpoint Discovery Service) and streams them to all gateway instances.

Sources: [README.md32](https://github.com/alibaba/higress/blob/8deceb4d/README.md#L32-L32) Diagram 2 from provided architecture diagrams

### Configuration Flow and Controller Architecture

**Configuration Update Sequence:**


**Controller Registry and Responsibilities:**

The controller implements the informer pattern for multiple resource types:

Controller| Source Location| Watched Resource| Generated Configs  
---|---|---|---  
`IngressController`| [pkg/ingress/kube/ingress/ingress.go1-500](https://github.com/alibaba/higress/blob/8deceb4d/pkg/ingress/kube/ingress/ingress.go#L1-L500)| `Ingress` (v1)| `VirtualService`, `DestinationRule`, `Gateway`  
`IngressController` (v1beta1)| [pkg/ingress/kube/ingress/ingressv1beta1.go1-400](https://github.com/alibaba/higress/blob/8deceb4d/pkg/ingress/kube/ingress/ingressv1beta1.go#L1-L400)| `Ingress` (v1beta1)| Legacy Ingress support  
`KIngressController`| [pkg/ingress/kube/kingress/kingress.go1-300](https://github.com/alibaba/higress/blob/8deceb4d/pkg/ingress/kube/kingress/kingress.go#L1-L300)| Knative `Ingress`| Knative-specific routing  
`WasmPluginController`| [pkg/ingress/kube/wasmplugin/wasmplugin.go1-400](https://github.com/alibaba/higress/blob/8deceb4d/pkg/ingress/kube/wasmplugin/wasmplugin.go#L1-L400)| `WasmPlugin` CRD| `EnvoyFilter` with WASM config  
`McpBridgeReconciler`| [pkg/ingress/kube/mcpbridge/reconciler.go1-300](https://github.com/alibaba/higress/blob/8deceb4d/pkg/ingress/kube/mcpbridge/reconciler.go#L1-L300)| `McpBridge` CRD| Registry watcher lifecycle  
`ConfigMapController`| [pkg/ingress/kube/configmap/1-100](https://github.com/alibaba/higress/blob/8deceb4d/pkg/ingress/kube/configmap/#L1-L100)| `higress-config` ConfigMap| `EnvoyFilter` for global settings  
  
The central cache (`pkg/ingress/kube/common/cache.go`) maintains in-memory state for all Istio resources and provides atomic updates to prevent partial configuration states. Configuration changes propagate to pilot within milliseconds, significantly faster than nginx-ingress reload times (reported 10x improvement).

Sources: [README.md108-116](https://github.com/alibaba/higress/blob/8deceb4d/README.md#L108-L116) Diagram 2 from provided architecture diagrams

## Key Capabilities

### AI Gateway Features

AI gateway functionality is implemented through a pipeline of WASM plugins that process requests and responses for LLM providers. The plugins support protocol translation, observability, caching, and security.

**AI Plugin Pipeline:**

Plugin| Source Location| Request Phase| Response Phase  
---|---|---|---  
`ai-proxy`| [plugins/wasm-go/extensions/ai-proxy/main.go1-500](https://github.com/alibaba/higress/blob/8deceb4d/plugins/wasm-go/extensions/ai-proxy/main.go#L1-L500)| Protocol detection, provider selection, request transformation| Response transformation, SSE stream processing  
`ai-statistics`| [plugins/wasm-go/extensions/ai-statistics/main.go1-400](https://github.com/alibaba/higress/blob/8deceb4d/plugins/wasm-go/extensions/ai-statistics/main.go#L1-L400)| Extract request attributes (user, model, tokens)| Extract response tokens, latency, write metrics/logs/traces  
`ai-cache`| [plugins/wasm-go/extensions/ai-cache/main.go1-300](https://github.com/alibaba/higress/blob/8deceb4d/plugins/wasm-go/extensions/ai-cache/main.go#L1-L300)| Check cache (semantic search)| Store response in Redis  
`ai-security-guard`| [plugins/wasm-go/ext

[...truncated...]

---
## 导语

Higress 是一款基于 Istio 和 Envoy 构建的 AI 原生 API 网关，它通过云原生架构将流量管理与大模型应用需求相结合。该项目不仅提供标准的微服务路由与 K8s Ingress 管理，还针对 LLM 应用集成了 AI 网关特性及 MCP 服务器托管能力，旨在解决企业在智能化转型中的流量治理与工具集成问题。本文将为您梳理其系统架构、核心组件及主要适用场景，帮助您评估该技术方案。

---
## 摘要

**Higress 项目总结**

**项目概况：**
Higress 是由阿里巴巴开源的**云原生 API 网关**，基于 Go 语言开发。它建立在 Istio 和 Envoy 之上，定位为一款 **AI Native（AI 原生）** 的 API 网关。目前该项目在 GitHub 上拥有约 7,470 个星标。

**核心定义：**
Higress 是一个扩展了 **WebAssembly (WASM)** 插件能力的云原生 API 网关。其架构将**控制平面**（配置管理）与**数据平面**（流量处理）分离。通过 xDS 协议，配置变更可毫秒级生效且无连接中断，特别适用于 AI 流式响应等长连接场景。

**三大核心功能与用例：**

1.  **AI 网关：**
    *   提供统一 API 接入 30 多家大语言模型（LLM）提供商。
    *   功能涵盖协议转换、可观测性、缓存及安全防护。
    *   *核心组件：* `ai-proxy`、`ai-statistics`、`ai-cache`、`ai-security-guard` 等插件。

2.  **MCP 服务器托管：**
    *   托管模型上下文协议（MCP）服务器，使 AI 智能体能够调用工具和外部服务。
    *   *核心组件：* `mcp-router`、`jsonrpc-converter` 过滤器及相关服务器实现。

3.  **Kubernetes Ingress：**
    *   作为 Kubernetes 入口控制器使用，兼容 nginx-ingress 注解。
    *   *核心组件：* `higress-controller`。

**总结：**
Higress 旨在为微服务架构和 AI 应用提供一站式的流量管理解决方案，兼具传统 API 网关的稳定性与 AI 时代的原生特性。

---
## 评论

**总体判断**

Higress 是一款极具前瞻性的“云原生+AI”基础设施产品，它成功地将传统 API 网关的高性能与 AI 时代所需的 LLM 管理、模型路由和 MCP 协议支持融合在一起。对于正在构建 AI 原生应用或寻求统一流量管理的企业而言，这是一个兼具技术深度与实用价值的优选方案。

**深入评价依据**

**1. 技术创新性：从“流量管道”进化为“AI 智能体枢纽”**
*   **事实：** 仓库描述明确其为 "AI Native API Gateway"，且基于 Istio 和 Envoy 构建。DeepWiki 提到它集成了 WASM 插件系统，并创新性地引入了 **MCP (Model Context Protocol) 服务器托管**功能。
*   **推断：** 传统网关（如 Nginx, 早期 Kong）主要关注 HTTP 转发。Higress 的差异化在于它不再仅仅是一个流量管道，而是成为了 AI 智能体的“中枢神经系统”。通过内置对 MCP 协议的支持，它解决了 AI Agent 调用外部工具（数据源）时的标准化连接问题，这比单纯的 LLM 转发更进了一步。此外，基于 Envoy + WASM 的架构使其在保持 C++ 高性能的同时，拥有了 Go/Python 的扩展灵活性，这种“控制面 Go + 数据面 Envoy + 逻辑面 WASM”的组合是当前云原生网关的最优解之一。

**2. 实用价值：解决 AI 落地中的“碎片化”与“成本”痛点**
*   **事实：** 核心功能包括 AI Gateway 特性（LLM 应用）、MCP 服务器托管以及 Kubernetes Ingress。
*   **推断：** Higress 解决了企业从微服务向 AI 服务转型时的架构割裂问题。企业通常需要维护一套传统的 API 网关（K8s Ingress）和一套专门用于 LLM 的网关（用于 Token 计费、Key 轮转）。Higress 将两者合二为一，允许用户在同一入口管理传统流量和 AI 流量。其实用性还体现在对多模型的支持上，开发者可以在网关层轻松实现从 OpenAI 切换到通义千问或开源模型（如 Llama），而无需修改业务代码，这种“模型解耦”能力在当前供应商锁定风险较高的环境下极具吸引力。

**3. 代码质量与架构：云原生工业标准的集大成者**
*   **事实：** 语言为 Go，星标数 7,470，架构明确分离了控制面与数据面。
*   **推断：** 由阿里巴巴主导的项目，其代码质量通常遵循严格的工业级标准。基于 Istio 的控制面意味着它继承了云原生生态的黄金标准（服务发现、证书管理），而基于 Envoy 的数据面则保证了极致的转发性能。DeepWiki 中详尽的文档结构（涵盖架构、构建、WASM、AI 特性等）表明该项目具有极高的成熟度，并非实验性玩具，而是生产就绪的产品。Go 语言的使用也降低了控制面逻辑的维护门槛，便于企业内部二次开发。

**4. 社区活跃度与生态：背靠阿里，连接 CNCF 生态**
*   **事实：** 拥有 7k+ 星标，提供中/日/英多语言文档。
*   **推断：** 作为阿里云开源的核心组件，Higress 享有阿里云技术栈的天然流量扶持和持续投入。多语言文档显示了其国际化的野心。虽然其社区活跃度可能不如 Envoy 或 Kong 那样历史悠久，但它在“AI + Cloud Native”这一细分赛道上处于领跑地位。对于国内开发者而言，中文社区的响应速度和阿里专家的介入是其巨大的生态优势。

**5. 学习价值与潜在问题**
*   **事实：** 提供了 WASM 插件系统和开发指南。
*   **推断：**
    *   **学习价值：** 开发者可以从中学习如何将复杂的业务逻辑（如 AI Token 计数、Prompt 注入）下沉到网关层，以及如何利用 WASM 技术实现网关的动态热插拔扩展，而不需要重启服务。
    *   **潜在问题：** 尽管功能强大，Higress 的架构相对厚重（依赖 Istio 和 Envoy），对于仅需简单转发的小型团队或边缘计算场景，可能存在“杀鸡用牛刀”的运维复杂度。此外，AI 领域迭代极快，网关对新模型特性（如 Sora 的视频流传输、复杂的长文本上下文管理）的支持可能存在滞后性。

**边界条件与验证清单**

**不适用场景：**
*   边缘设备或资源极度受限的嵌入式环境。
*   仅需极简单反向代理，且无 AI 调用需求的小型单体应用。
*   追求极致轻量级（如仅基于 OpenResty 的 Lua 脚本）的定制化场景。

**快速验证清单：**
1.  **WASM 插件验证：** 编写一个简单的 WASM 插本（如修改 HTTP Header），验证是否能在不重启 Higress 的情况下热加载，以测试其扩展性。
2.  **AI 流量路由：** 配置一条路由规则，根据请求头中的 `model` 参数，将流量动态分发至 OpenAI 和阿里云通义千问接口，检查响应延迟增加是否在可接受范围内（通常应 < 10ms）。
3.  **Prompt

---
## 技术分析

# Higress 深度技术分析报告

基于阿里巴巴开源的 Higress 仓库（AI Native API Gateway），本文将从架构设计、核心功能、技术实现、适用场景、发展趋势、学习路径、最佳实践以及工程哲学八个维度进行深入剖析。

---

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 的核心架构建立在 **云原生** 生态之上，采用了典型的 **控制平面与数据平面分离** 的架构模式。

*   **底层基础设施**：深度依赖 **Envoy** 作为高性能数据平面，利用其 L3/L7 过滤能力和可观测性。
*   **控制平面**：基于 **Istio** 进行了大幅简化和增强。虽然 Istio 功能强大，但作为 API 网关过于重载，Higress 剥离了 Sidecar 注入等非网关核心功能，专注于 Ingress 和 Gateway 的职责。
*   **扩展模型**：**WebAssembly (WASM)** 是其架构的灵魂。它允许使用 C/C++/Go/Rust 等语言编写插件，动态加载到 Envoy 中，实现了业务逻辑与网关核心的解耦，且无需重启网关即可更新逻辑。

### 核心模块设计
1.  **Router (路由层)**：兼容 Kubernetes Ingress API 和 Gateway API，支持基于权重、Header、Cookie 的复杂路由。
2.  **WASM Plugin System (插件系统)**：这是 Higress 的“护城河”。它提供了一个插件市场，允许用户通过配置下发 WASM 代码，在请求的生命周期（路由前、鉴权后、响应前）插入逻辑。
3.  **AI Native Layer (AI 原生层)**：这是最新且最重要的模块。它不仅仅是代理流量，还理解 AI 协议。
    *   **Provider 抽象**：统一了 OpenAI, Azure, Qwen, Tongyi 等各家 LLM 的接口差异。
    *   **语义路由**：能够根据 Prompt 的内容将请求路由到不同的模型或后端。

### 架构优势分析
*   **毫秒级配置生效**：得益于 Istio 的 xDS 协议（包括 LDS, CDS, RDS, EDS），配置变更可以秒级推送到数据平面，且连接不中断。这对于 AI 长连接（SSE/Streaming）至关重要。
*   **极致性能**：数据平面 Envoy 采用 C++ 编写，具备 L4/L7 极高的处理吞吐量。相比 Nginx Lua 模型，WASM 在隔离性和安全性上更具优势，且性能损耗在可接受范围内（通过 AOT 编译优化）。
*   **生态融合**：原生支持 Kubernetes 服务发现，无需像 Nginx 那样手动配置 upstream。

---

## 2. 核心功能详细解读

### AI Gateway：大模型时代的流量管家
这是 Higress 区别于传统网关（如 APISIX, Kong）的核心竞争力。

*   **解决的关键问题**：
    *   **协议转换与统一**：屏蔽不同 LLM 厂商 API 参数（如 `temperature`, `top_p`）的差异，提供统一的 OpenAI 兼容接口。
    *   **Token 计费与限流**：传统网关只能基于 QPS 限流，AI 网关可以根据 Token 数量或请求/响应的 Token 比率进行精细化限流和计费。
    *   **提示词管理**：支持在网关层预设 System Prompt，实现 Prompt 的版本控制和灰度发布，无需修改后端应用代码。
    *   **结果缓存**：对相同的 Prompt 进行缓存（利用 Redis 等），直接返回结果，大幅降低后端 LLM 调用成本。

### MCP (Model Context Protocol) Server Hosting
Higress 能够托管 MCP Server，充当 AI Agent 的“工具箱”。
*   **功能**：将后端服务（如数据库查询、天气查询）封装为标准的 MCP 协议，供 AI Agent 调用。
*   **价值**：解决了 Agent 连接外部工具时的安全认证和标准化问题。

### 与同类工具对比
| 特性 | Higress | APISIX / Kong | Nginx + Lua |
| :--- | :--- | :--- | :--- |
| **AI 原生支持** | **内置 (Provider 聚合, Token管理)** | 需通过插件实现，功能较弱 | 需大量自研 |
| **扩展性** | **WASM (多语言, 高安全, 动态)** | Lua/Python/Java (进程级隔离较弱) | Lua (侵入性强) |
| **配置热更新** | **毫秒级 (xDS)** | 毫秒级 | 秒级 (Reload 连接中断) |
| **K8s 集成** | **原生 (Ingress/Gateway API)** | 较好 | 弱 (需 Ingress Controller) |

---

## 3. 技术实现细节

### 关键技术方案：WASM 的工程化落地
Higress 并没有直接使用 Envoy 原生的 WASM 能力（配置复杂），而是开发了一套 **Wasm Plugin Marketplace** 机制。
*   **实现原理**：用户编写 Go 代码（通过 SDK 编写），编译为 `.wasm` 文件。Higress 控制平面将文件上传到 OCI 仓库（如 Docker Registry），数据平面通过 `filter.config` 拉取并挂载到 Envoy 的 VM 中。
*   **Host Interaction**：通过 `proxy-wasm` 规范，WASM 插件可以读取请求头、修改 Body、调用外部服务（gRPC/HTTP），甚至共享内存。

### 性能优化与扩展性
*   **零拷贝**：在 Envoy 内部处理数据时，尽量减少内存拷贝。WASM 插件处理时也利用了共享内存视图。
*   **多线程模型**：Envoy 的多线程模型充分利用了多核 CPU，WASM 插件在每个 Worker 线程中独立运行（虽然不是共享状态，但保证了无锁并发）。
*   **连接池**：对后端 LLM 服务（如 OpenAI API）实现了 HTTP 连接复用，减少握手开销。

### 技术难点与解决
*   **流式响应处理**：LLM 返回通常是 SSE (Server-Sent Events) 格式的流。网关在转发流时，必须处理分片、超时和缓冲。Higress 通过 Envoy 的 Streaming Filter 机制，实现了对流的透传和拦截（例如在流结束时统计 Token 数）。
*   **配置一致性**：在分布式网关实例中，如何保证所有节点的配置一致？Higress 使用 Istio 的控制平面机制，通过 xDS 协议保证配置最终一致性。

---

## 4. 适用场景分析

### 最适合的场景
1.  **企业级 AI 应用落地**：企业内部需要接入多个大模型（通义千问、DeepSeek、OpenAI），希望统一入口，进行鉴权、限流和 Prompt 管理。Higress 是目前的最佳选择。
2.  **微服务 API 网关**：基于 Kubernetes 的微服务体系，需要高性能、可扩展的网关，且开发团队具备 Go 或 Rust 能力，希望编写自定义业务逻辑。
3.  **多租户 SaaS 平台**：需要为不同租户提供独立的 API Key 或路由策略，利用 Higress 的路由匹配能力可以轻松实现。

### 不适合的场景
1.  **极简静态资源服务**：如果只需要简单的反向代理，Nginx 足够且更轻量，Higress 的 K8s 依赖和架构过于重。
2.  **非 K8s 环境的复杂传统架构**：虽然支持 Linux 部署，但 Higress 的强项在于与服务发现结合，在传统虚拟机环境下，配置管理复杂度可能高于收益。

### 集成注意事项
*   **资源规划**：WASM 插件运行会消耗额外的内存和 CPU，建议对网关实例进行资源限制和压测。
*   **观察性**：务必对接 Prometheus + Grafana + SkyWalking，利用 Higress 内置的 Tracing 能力，否则排查 AI 流量问题将非常困难。

---

## 5. 发展趋势展望

### 演进方向
1.  **从网关到 AI 编排**：Higress 正在从单纯的流量转发，向具备一定逻辑编排能力的 AI Gateway 演进。未来可能会集成更复杂的 Agent 工作流编排（如 LangChain 的部分功能下沉到网关）。
2.  **MSP 协议的深化**：随着 AI Agent 的爆发，MCP 协议可能成为标准，Higress 作为 MCP Server 的托管平台，将成为企业知识库对外暴露的标准入口。

### 社区与生态
*   **插件市场**：Higress 的插件市场正在丰富，未来可能会出现更多针对特定 AI 场景（如自动重试、降级、敏感词过滤）的商业化或开源插件。
*   **WASM 生态**：随着 WASM 组件模型（Component Model）的成熟，Higress 可能会支持更复杂的 WASM 应用，甚至将网关本身模块化。

---

## 6. 学习建议

### 适合人群
*   **云原生架构师**：希望深入理解 Istio/Envory 架构。
*   **后端工程师**：需要处理 AI 流量、微服务路由，且希望掌握 Go + WASM 技术栈。
*   **AI 应用开发者**：需要构建生产级 LLM 应用的工程师。

### 学习路径
1.  **基础**：熟悉 Envoy 基础概念和 Kubernetes Ingress 机制。
2.  **入门**：在本地 Kind 集群中部署 Higress，配置一个简单的 AI 路由（转发到 OpenAI）。
3.  **进阶**：学习 Higress Go SDK，编写一个简单的 WASM 插件（例如：添加一个自定义 Header），并在控制台上传。
4.  **高级**：研究源码中的 `router` 和 `wasm` 模块，理解 xDS 配置如何下发，以及 WASM VM 如何与 Host 交互。

---

## 7. 最佳实践建议

### 正确使用指南
*   **利用 Provider 抽象**：不要在代码里硬编码 LLM 厂商的地址。在 Higress 中配置 Provider，应用层只需调用统一的 `/v1/chat/completions` 接口。
*   **渐进式路由**：先设置默认路由，再根据 Prompt 特征（如包含“绘图”关键词）设置特定路由，实现智能分流。

### 常见问题与坑
*   **WASM 插件 panic**：WASM 插件中的未捕获 panic 会导致请求 500。务必在插件顶层使用 `defer recover()`，并利用 Higress 的日志接口记录错误。
*   **超时设置**：AI 请求耗时较长。务必在路由配置中将 `timeout` 设置得足够大，或者针对流式请求禁用超时。

### 性能优化
*   **开启 Brotli 压缩**：对于非流式的文本响应，开启压缩可显著减少带宽。
*   **全链路 Tracing**：AI 调用链路长，必须开启

---
## 代码示例




```python
# 示例1：基于Higress的API网关配置
def higress_api_gateway_config():
    """
    配置Higress作为API网关，实现路由转发和负载均衡
    解决问题：将不同路径的请求路由到不同的后端服务
    """
    config = {
        "routes": [
            {
                "path": "/api/v1/*",  # 匹配所有v1版本的API请求
                "backend": "service-a:8080",  # 转发到service-a
                "plugins": {
                    "rate-limit": {
                        "queries_per_second": 100  # 限流100 QPS
                    }
                }
            },
            {
                "path": "/api/v2/*",  # 匹配所有v2版本的API请求
                "backend": "service-b:8080",  # 转发到service-b
                "plugins": {
                    "jwt-auth": {
                        "secret": "your-secret-key"  # JWT认证
                    }
                }
            }
        ]
    }
    return config

# 说明：这个示例展示了如何配置Higress作为API网关，实现：
# 1. 基于路径的路由分发
# 2. 后端服务的负载均衡
# 3. 限流和认证等流量控制功能
# 实际使用时需要将配置应用到Higress集群中
```




```python
# 示例2：Higress插件开发示例
from higress import Plugin

class CustomAuthPlugin(Plugin):
    """
    自定义认证插件
    解决问题：实现基于自定义Header的API认证
    """
    def on_request(self, request):
        # 获取请求头中的认证信息
        auth_header = request.headers.get("X-Custom-Auth")
        
        # 验证认证信息
        if not self.validate_auth(auth_header):
            return {
                "status": 401,
                "body": "Unauthorized"
            }
        
        # 认证通过，添加用户信息到请求头
        request.headers["X-User-Id"] = self.get_user_id(auth_header)
        return request
    
    def validate_auth(self, auth_header):
        # 实现具体的认证逻辑
        return auth_header == "valid-token"
    
    def get_user_id(self, auth_header):
        # 从认证信息中提取用户ID
        return "user-123"

# 说明：这个示例展示了如何开发Higress插件：
# 1. 继承Plugin基类
# 2. 实现on_request方法处理请求
# 3. 自定义认证逻辑
# 4. 修改请求头传递用户信息
# 实际使用时需要将插件编译并部署到Higress
```




```python
# 示例3：Higress流量管理配置
def higress_traffic_management():
    """
    配置Higress的流量管理功能
    解决问题：实现灰度发布和流量切换
    """
    config = {
        "services": {
            "product-service": {
                "versions": {
                    "v1": {
                        "weight": 80,  # 80%流量到v1版本
                        "endpoints": ["v1-service-1", "v1-service-2"]
                    },
                    "v2": {
                        "weight": 20,  # 20%流量到v2版本(灰度)
                        "endpoints": ["v2-service-1"]
                    }
                }
            }
        },
        "canary": {
            "match": {
                "headers": {
                    "canary": "true"  # 带有canary头的请求全部走v2
                }
            },
            "route": "product-service:v2"
        }
    }
    return config

# 说明：这个示例展示了如何配置Higress的流量管理：
# 1. 基于权重的流量分配(80/20)
# 2. 多版本服务管理
# 3. 基于请求头的金丝雀发布
# 4. 灰度发布策略配置
# 实际使用时需要将配置应用到Higress集群中
```


---
## 案例研究


### 1：阿里巴巴内部电商业务转型

 1：阿里巴巴内部电商业务转型

**背景**:  
阿里巴巴内部电商业务原有架构基于传统的 Nginx + Lua 自研网关，随着业务复杂度增加，维护成本高，且云原生转型需求迫切。

**问题**:  
- 自研网关与 Kubernetes 生态兼容性差，难以实现服务网格的统一管理  
- 动态路由更新依赖配置文件重载，影响线上稳定性  
- 多语言（Java/Go/Node.js）服务治理策略不统一

**解决方案**:  
采用 Higress 作为下一代云原生网关，通过以下方式实现：  
1. 基于 Istio 控制平面实现服务网格集成  
2. 利用 WASM 插件机制支持多语言扩展（如 Python 鉴权逻辑）  
3. 通过 OpenAPI 标准化对接内部服务注册中心（Nacos）

**效果**:  
- 配置热更新生效时间从分钟级降至秒级  
- 网关资源占用降低 40%（相比原有 Nginx 集群）  
- 支持日均 10 亿+ 流量请求，P99 延迟优化 25%  

---



### 2：某头部直播平台流量治理

 2：某头部直播平台流量治理

**背景**:  
该平台原有网关系统在促销活动期间面临突发流量冲击，且灰度发布能力不足，导致新功能回滚频繁。

**问题**:  
- 传统网关无法按用户画像进行精细化流量分流  
- 限流策略依赖固定阈值，缺乏动态调整能力  
- 多集群容灾切换需人工介入，耗时超过 30 分钟

**解决方案**:  
部署 Higress 集群并实现：  
1. 基于用户标签的动态路由规则（如按会员等级分流）  
2. 集成 Prometheus 实时监控，自动调整限流参数  
3. 通过 HTTP-to-gRPC 协议转换统一后端服务接口

**效果**:  
- 新功能灰度发布成功率提升至 98%  
- 大促期间自动扩缩容响应时间缩短至 15 秒  
- 跨地域容灾切换实现自动化，耗时降至 2 分钟以内  

---



### 3：金融科技企业 API 生态建设

 3：金融科技企业 API 生态建设

**背景**:  
某金融科技企业需向合作伙伴开放 200+ 个 API 接口，原有网关缺乏统一的开发者管理工具。

**问题**:  
- API 文档与实际实现不一致导致集成问题频发  
- 缺乏细粒度的访问控制（如按调用频率/时间窗口限制）  
- 无法对第三方调用进行全链路追踪

**解决方案**:  
基于 Higress 构建 API 网关平台：  
1. 集成 OpenAPI 规范自动生成文档  
2. 开发 WASM 插件实现动态密钥认证和调用配额管理  
3. 对接 Jaeger 实现跨服务调用链可视化

**效果**:  
- 合作伙伴集成周期缩短 60%  
- 异常调用检测准确率提升至 99.2%  
- 单个 API 平均开发成本降低 3 人天/月

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|----------------|------|-------|
| 性能 | 高性能（基于Envoy和Istio优化） | 高性能（基于OpenResty/Nginx） | 极高性能（基于OpenResty/LuaJIT） |
| 易用性 | 提供控制台和Kubernetes CRD，支持Wasm插件 | 插件生态丰富，配置灵活 | 配置复杂，学习曲线较陡 |
| 成本 | 开源免费，商业支持需付费 | 开源免费，企业版收费 | 开源免费，商业支持需付费 |
| 扩展性 | 支持Wasm插件，扩展性强 | 支持Lua插件，社区插件丰富 | 支持Lua和Python插件，扩展性一般 |
| 社区活跃度 | 阿里背书，社区活跃 | 社区成熟，用户基数大 | 社区活跃，国内用户多 |
| 适用场景 | 云原生、微服务、API网关 | 传统API网关、微服务 | 高并发API网关、微服务 |

### 优势分析

- **性能优势**：基于Envoy和Istio优化，性能接近原生Envoy，适合高并发场景。
- **云原生集成**：深度集成Kubernetes和Istio，支持服务网格和API网关一体化。
- **Wasm支持**：支持WebAssembly插件，扩展性强，插件开发语言灵活。
- **阿里生态**：与阿里云产品无缝集成，适合阿里云用户。

### 不足分析

- **社区成熟度**：相比Kong和APISIX，社区和插件生态尚在发展阶段。
- **文档完善度**：文档和案例较少，学习资源有限。
- **商业支持**：商业支持和服务体系不如Kong和APISIX成熟。
- **兼容性**：与部分传统架构的兼容性可能不如Kong。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Wasm 插件扩展网关功能

**说明**: Higress 基于 Envoy 构建，原生支持 WebAssembly (Wasm)。相比传统 Lua 脚本或 C++ 插件，Wasm 插件具有更高的安全性、隔离性以及跨平台能力。利用 Wasm 插件机制，可以动态加载自定义逻辑（如自定义认证、流量整形、日志定制等），而无需重新构建网关镜像或重启服务。

**实施步骤**:
1. 确定业务逻辑需求，判断是否适合通过 Wasm 实现（如复杂的 Header 修改、对接外部认证系统）。
2. 使用 C++、Go 或 Rust 编写 Wasm 插件代码，并利用 Higress 提供的 SDK 处理请求生命周期。
3. 将编译好的 `.wasm` 文件上传至 Higress 控制台或配置为 OCI 镜像仓库引用。
4. 在网关规则或路由配置中，将特定插件关联到需要的路由或服务上。

**注意事项**: Wasm 插件运行在沙箱中，虽然隔离性好，但频繁的内存拷贝（Host 与 Wasm 之间）可能会引入微小的性能延迟，需关注高并发下的延迟表现。

---

### 实践 2：精细化流量管理与流量标签

**说明**: Higress 继承了 Istio 的流量管理能力，并进行了简化。最佳实践是充分利用 Request Headers 或 URL 参数进行流量打标，结合 `VirtualDestination` 和 `ServiceEntry` 实现基于标签的蓝绿发布、金丝雀发布或 A/B 测试，而不是仅仅依赖简单的权重路由。

**实施步骤**:
1. 在服务调用链中注入特定的流量标签 Header（例如 `x-user-segment: beta`）。
2. 在 Higress 中定义 DestinationRule，将服务实例划分为不同的子集。
3. 配置 VirtualHost 或 RouteRule，根据 Header 匹配规则将流量导向特定的 Subset。
4. 使用 Higress 控制台或 K8s YAML 进行灰度验证，逐步扩大流量比例。

**注意事项**: 确保流量标签的传递性，确保全链路透传，避免在微服务调用链中丢失标签导致路由回退。

---

### 实践 3：配置全链路安全认证与鉴权

**说明**: 默认暴露的服务容易遭受攻击。最佳实践是在网关层统一处理认证与鉴权，避免将未鉴权的流量直接透传给后端业务服务。Higress 支持多种鉴权方式，包括基于 JWT、Key Auth 以及对接外部 OAuth2/OIDC 服务。

**实施步骤**:
1. 在全局或特定路由上启用 `JWTRule` 或 `KeyAuth` 配置，验证请求中的 Token 或 API Key。
2. 对于复杂场景，配置 `ExternalAuth`（如 gRPC 或 HTTP 外部鉴权服务），将请求上下文发送给独立的鉴权微服务进行判断。
3. 结合 `Allow` 和 `Deny` 列表策略，限制访问来源 IP 或特定路径。

**注意事项**: 外部鉴权服务的性能至关重要，建议设置合理的超时时间和缓存策略，防止鉴权服务拖垮整个网关的吞吐量。

---

### 实践 4：服务保护与熔断降级策略

**说明**: 在微服务架构中，级联故障是常见风险。Higress 允许在网关层配置熔断、限流和并发控制，作为保护后端服务的第一道防线。最佳实践是针对不同优先级的服务设置不同的资源阈值。

**实施步骤**:
1. 针对读多写少的服务配置 `LocalRateLimit`（本地限流），利用 Token Bucket 算法控制 QPS。
2. 针对后端不稳定的服务，配置 `RetryPolicy`（重试策略）和 `CircuitBreaker`（熔断策略），当连续错误达到阈值时自动熔断。
3. 设置超时时间，防止客户端长时间挂起占用连接资源。

**注意事项**: 限流配置应基于后端服务的真实承载能力（TPS99）进行测算，并预留一定的 Buffer；重试策略需配合幂等性设计，避免产生脏数据。

---

### 实践 5：对接云原生服务注册发现

**说明**: Higress 设计为云原生网关，能够直接与 Kubernetes Service、Nacos、Consul 等注册中心对接。最佳实践是放弃硬编码 IP 列表，转而使用服务发现机制，实现服务的动态扩缩容感知。

**实施步骤**:
1. 在 Higress 配置中启用对应的 Service Registry（如 Nacos 或 Consul）。
2. 创建 `ServiceIngress` 或配置路由时，直接引用服务名称。
3. 配置健康检查机制，确保 Higress 能及时剔除不健康的实例。

**注意事项**: 如果使用非 K8s 原生注册中心（如 Nacos），需确保 Higress 与注册中心网络连通，并关注服务列表变更的同步延迟。

---

### 实

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/3 (QUIC) 协议支持

**说明**: Higress 基于 Envoy，天然支持 HTTP/3 协议。HTTP/3 基于 UDP 协议，解决了 TCP 队头阻塞问题，在弱网环境下能显著降低连接建立延迟和丢包重传开销，提升吞吐量。

**实施方法**:
1. 在 Higress 网关的监听器配置中，为需要优化的路由或端口启用 HTTP/3 协议。
2. 配置 UDP 端口（通常端口 443）的防火墙放行策略。
3. 确保客户端支持 HTTP/3 协议进行握手。

**预期效果**: 在高丢包率或高延迟网络环境下，请求响应时间（RTT）可降低 30%-50%，连接建立成功率显著提升。

---

### 优化 2：配置全链路超时与重试策略

**说明**: 默认的超时配置可能导致大量连接长时间挂起，耗尽网关线程池。精细化的超时与退避重试策略能快速释放资源，防止雪崩，同时保证后端服务抖动时的最终成功率。

**实施方法**:
1. 在路由配置中明确设置 `connectTimeout`、`requestTimeout` 和 `streamIdleTimeout`。
2. 配置指数退避的重试策略，限制每请求最大重试次数（建议 2-3 次）。
3. 开启针对 5xx 错误的自动重试，并关闭对非幂等请求（如 POST）的重试（除非业务允许）。

**预期效果**: 减少无效连接占用资源，在依赖服务故障时，网关自身吞吐量下降幅度控制在 10% 以内，整体请求成功率提升至 99.9%。

---

### 优化 3：启用 Wasm 插件的高效隔离与缓存

**说明**: Higress 支持 Wasm 插件扩展。不当的插件配置（如每次请求都重复加载代码或进行复杂计算）会严重拖累 Latency。利用 Wasm 的内存隔离特性及 Proxy-Wasm 的 ABI 特性进行优化至关重要。

**实施方法**:
1. 将插件中不随请求变化的初始化逻辑（如配置解析、正则编译）移至 `on_configure` 或 `on_vm_start` 阶段，避免在 `on_request` 阶段重复执行。
2. 对于高频调用的插件逻辑，尽量使用 HostCall 的内存共享机制，减少跨边界的数据拷贝。
3. 限制 Wasm VM 的内存堆大小，防止内存溢出导致 OOM。

**预期效果**: 复杂插件处理延迟可降低 20%-40%，显著减少 P99 延迟抖动。

---

### 优化 4：启用连接池复用与 Keep-Alive 优化

**说明**: 频繁建立 TCP/TLS 连接是性能杀手。通过调整上游服务连接池参数，保持长连接复用，可以大幅减少握手开销。

**实施方法**:
1. 根据后端服务负载能力，适当调大 `maxConnections` 参数（避免默认值过小导致排队）。
2. 启用 HTTP/1.1 Keep-Alive 或 HTTP/2 连接复用。
3. 配置合理的 `idleTimeout`，平衡后端连接回收与复用率。

**预期效果**: 后端连接建立耗时减少 90% 以上，网关 CPU 利用率在相同 QPS 下可降低 10%-15%。

---

### 优化 5：实施精细化日志采样与异步上报

**说明**: 在高并发场景下，同步打印详细的 Access Log 会产生大量的磁盘 I/O 等待，阻塞网络处理线程。

**实施方法**:
1. 配置日志采样策略（如仅记录 10% 的正常流量，100% 记录错误流量）。
2. 使用异步日志 Driver（如 OpenTelemetry 的异步 Processor）或对接 Kafka/Fluentd 进行日志转发。
3. 关闭不必要的 Debug 级别日志。

**预期效果**: I/O Wait 时间显著降低，在高并发压测下

---
## 学习要点

- Higress 是阿里开源的基于 Istio 的云原生 API 网关，深度集成了 K8s 与 Nginx Ingress 生态。
- 它提供一站式的流量管理，支持 HTTP、HTTPS、gRPC、Dubbo 等多种协议及流量路由与负载均衡。
- 内置强大的安全防护能力，包括 WAF 防火墙、认证鉴权及针对开源协议 CVE 的漏洞扫描。
- 具备高性能的插件扩展市场（Wasm 插件），支持低代码或全代码方式灵活扩展网关功能。
- 能够将传统的 Nginx Ingress 配置无损迁移，并兼容 K8s Ingress 资源定义，降低迁移门槛。
- 提供精细化的服务治理能力，如全链路灰度发布、流量回放及超时熔断等企业级特性。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础与核心概念

**学习内容**:
- **云原生网关基础**: 理解什么是 API 网关，以及 Higress 在微服务架构中的定位与作用（流量入口、南北向流量管理）。
- **Higress 架构原理**: 学习 Higress 的核心组件（Ingress Controller、Gateway Runtime）及其基于 Envoy 和 Istio 的技术架构。
- **基础部署**: 掌握如何在 Kubernetes (K8s) 集群中通过 Helm 或 YAML 文件快速安装和部署 Higress。
- **基本流量路由**: 学习如何配置 K8s Ingress 资源或 Higress 的 Gateway API Route，实现简单的域名转发和路径匹配。

**学习时间**: 1-2周

**学习资源**:
- Higress 官方 GitHub 仓库 README
- Higress 官方文档 - "快速开始" 章节
- [阿里云云原生 API 网关产品介绍](https://www.aliyun.com/product/higress)

**学习建议**:
建议先对 Kubernetes 和容器网络有基础了解。在本地搭建一个 Kind 或 Minikube 环境进行实操，不要只看文档，务必亲自跑通第一个 "Hello World" 路由示例。

---

### 阶段 2：核心功能与流量治理

**学习内容**:
- **服务发现与注册**: 学习如何将 Higress 与 Nacos、Consul 或 K8s Service 进行集成，实现后端服务的自动发现。
- **全栈流量管理**: 深入学习 HTTP 路由、重定向、重写、流量镜像以及 Header 操作。
- **安全防护**: 掌握如何配置域名 HTTPS 证书、实现 Basic Auth（基础认证）、Key Auth 以及 IP 黑白名单访问控制。
- **插件系统入门**: 了解 Higress 的插件机制，尝试使用官方预设插件（如请求限流、CORS 处理等）。

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - "网关管理" 与 "流量管理"
- Higress 官方插件市场
- Envoy 官方文档中关于 HTTP Filters 的部分（辅助理解底层原理）

**学习建议**:
尝试构建一个包含两个微服务的简单 K8s 应用，通过 Higress 管理它们之间的流量。重点练习金丝雀发布和蓝绿发布的配置流程，这是网关最常用的场景之一。

---

### 阶段 3：高阶应用与 WAF 防护

**学习内容**:
- **WAF 安全防护**: 深入学习 Higress 内置的 Web 应用防火墙功能，配置防御 SQL 注入、XSS 等常见 Web 攻击。
- **负载均衡策略**: 研究高级负载均衡算法（如加权轮询、最小连接数）和健康检查机制。
- **服务 mocking 与降级**: 学习如何在后端服务不可用时使用 Higress 进行 Mock 响应或服务降级，保障系统稳定性。
- **多租户与多环境**: 掌握在同一个 Higress 实例中隔离不同环境（开发、测试、生产）的流量配置。

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - "安全防护" 专题
- Higress GitHub Discussions 中的最佳实践案例
- 云原生社区关于 WAF 2.0 的技术文章

**学习建议**:
此阶段重点在于"稳"和"安"。建议模拟故障场景（如后端 Pod 挂掉），观察 Higress 的健康检查和摘流逻辑是否符合预期。同时，尝试编写一个简单的 Lua 或 Wasm 插件来扩展功能。

---

### 阶段 4：插件开发与性能优化

**学习内容**:
- **自定义插件开发**: 学习如何使用 Go 或 C++ 开发 Wasm 插件，或者使用 Lua/Java 开发 Higress 插件，实现定制化的业务逻辑（如自定义鉴权、请求体修改）。
- **多协议支持**: 了解如何配置 Dubbo、gRPC 等非 HTTP 协议的代理转发。
- **高可用与性能调优**: 学习 Higress 的部署架构优化，包括网关副本的自动扩缩容（HPA）、长连接配置优化、以及与 Prometheus/Grafana 集成的监控指标分析。
- **Dubbo 服务治理**: 如果涉及 Java 体系，深入学习 Higress 对 Dubbo 服务的多版本路由和参数路由控制。

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档 - "自定义插件开发"
- Higress GitHub 源码 (参考 example-plugins)
- WebAssembly (Wasm) 官方教程

**学习建议**:
如果你有开发背景，建议从阅读官方插件的源码开始，尝试修改并编译一个自己的插件。如果是运维方向，重点关注 Prometheus �

---
## 常见问题


### 1: Higress 是什么？它与 Kuma、Istio 等 Service Mesh（服务网格）产品有什么区别？

1: Higress 是什么？它与 Kuma、Istio 等 Service Mesh（服务网格）产品有什么区别？

**A**: Higress 是一款基于阿里内部多年实践，开源的云原生 API 网关。它深度集成了 Envoy 和 Istio，旨在解决云原生架构下的流量治理问题。

它与 Kuma、Istio 的主要区别在于定位和架构：
1.  **定位不同**：Higress 的核心定位是“API 网关”，而 Kuma 和 Istio 的核心定位是“服务网格”。虽然 Higress 也具备服务网格的部分流量治理能力，但它更侧重于南北向流量（入口流量）的管理，以及连接后端微服务和云函数。
2.  **架构与性能**：Higress 基于 Istio 进行了大量优化，去除了对 Sidecar（边车）的强依赖，支持独立部署模式。这使得它在作为 API 网关时，相比传统的 Istio Ingress Gateway 或 Kuma，具有更高的性能和更低的资源消耗。
3.  **易用性**：Higress 提供了开箱即用的控制台（Console）和 Wasm 插件市场，相比 Istio 原生复杂的 CRD 配置，Higress 在路由配置、插件加载和监控对接上更加便捷，特别适合需要快速交付 API 管理能力的场景。

---



### 2: Higress 是否兼容 Nginx 或 Ingress Nginx 的配置？迁移成本高吗？

2: Higress 是否兼容 Nginx 或 Ingress Nginx 的配置？迁移成本高吗？

**A**: Higress 在设计上充分考虑了从 Nginx 和 Ingress Nginx 迁移的用户体验，兼容性较高。

1.  **Ingress API 兼容**：Higress 原生支持 Kubernetes Ingress API。这意味着你现有的 Kubernetes Ingress YAML 文件通常可以直接在 Higress 环境中运行，无需修改即可实现基础的域名和路径路由。
2.  **Nginx 语法支持**：虽然 Higress 底层使用 Envoy，但它提供了对 Nginx 配置语法的部分支持（通过注解或配置转换工具），或者支持直接导入 Nginx 的配置逻辑。
3.  **迁移成本**：对于基础的负载均衡、SSL/TLS 卸载和路由转发，迁移成本极低。主要的工作量可能在于将 Nginx 的 Lua 脚本迁移为 Higress 支持的 Wasm 插件（Wasm 插件可以使用 C++/Go/Rust/AssemblyScript 编写，比 Lua 具有更好的隔离性和性能）。

---



### 3: Higress 支持哪些协议？能否处理 gRPC 或 Dubbo 流量？

3: Higress 支持哪些协议？能否处理 gRPC 或 Dubbo 流量？

**A**: Higress 是一款全功能的云原生网关，支持 HTTP/1.1、HTTP/2、HTTP/3 (QUIC)、gRPC 以及常见的 RPC 协议（如 Dubbo、Dubbo3）。

1.  **gRPC 支持**：Higress 原生支持 gRPC 协议的代理和路由。你可以基于 gRPC 的 Service 定义路由规则，并支持 gRPC-Web（允许浏览器直接调用 gRPC 服务）。
2.  **Dubbo 支持**：得益于阿里在 Dubbo 生态的深厚积累，Higress 对 Dubbo 协议（特别是 Triple 协议）提供了原生支持。它可以将 HTTP/JSON 请求转换为 Dubbo 请求，实现 HTTP 到 Dubbo 的协议转换，这对于微服务架构中多协议共存的企业非常有价值。

---



### 4: Higress 的插件机制是如何工作的？是否支持自定义插件？

4: Higress 的插件机制是如何工作的？是否支持自定义插件？

**A**: Higress 采用了基于 **Wasm (WebAssembly)** 的插件扩展机制，这是其核心亮点之一。

1.  **工作原理**：Wasm 插件运行在沙箱环境中，可以被动态加载到 Envoy 代理中。相比传统的 Lua 脚本或 C++ 扩展，Wasm 插件具有更好的安全性（隔离性）、动态性（无需重启网关即可热加载/更新插件）和多语言支持性。
2.  **自定义插件**：用户完全可以开发自定义插件。Higress 提供了多种语言的 SDK（Go, C++, Rust, AssemblyScript 等）。你可以编写业务逻辑（如鉴权、请求头修改、流量限流等），编译为 `.wasm` 文件，然后通过 Higress 控制台或 K8s CRD 上传并配置生效。
3.  **插件市场**：Higress 社区还维护了一个插件市场，提供了常见的开箱即用插件，如 JWT 鉴权、Keyless 认证、请求重试等。

---



### 5: 在生产环境中，Higress 的性能表现如何？是否支持高可用部署？

5: 在生产环境中，Higress 的性能表现如何？是否支持高可用部署？

**A**: Higress 专为高性能和高可用生产环境设计。

1.  **性能表现**：由于底层基于 Envio C++ 实现，Higress 的单核转发性能非常高，延迟极低。在官方基准测试中，其吞吐量通常优于基于 Java 或 Go 的传统网

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单] 环境搭建与基础流量转发

### 问题描述**:

### 请在本地 Docker 环境中快速部署 Higress，并配置一个简单的路由规则。要求将访问 `http://localhost:8080/foo` 的流量转发到后端模拟服务（例如 httpbin.org）的 `/get` 接口，并通过终端或浏览器验证转发成功。

### 参考提示**:

---
## 实践建议

基于 Higress 作为 "AI Native API Gateway" 的定位，结合其作为云原生 API 网关的特性，以下是 6 条针对实际使用场景的实践建议：

### 1. 利用内置的 AI 插件实现零代码 LLM 集成
*   **场景**：需要快速接入大模型（如 OpenAI, Azure, 通义千问等）进行验证或生产使用，而不希望编写额外的后端服务代码。
*   **建议**：直接使用 Higress 控制台中的 AI 插件配置（如 `ai-proxy`）。通过配置 `provider`、`apiToken` 和模型名称，即可在网关层完成协议转换。
*   **最佳实践**：在插件配置中开启**对话历史记录压缩**功能。对于不支持长上下文的模型，网关可以在转发请求前自动截断或总结历史对话，节省 Token 并降低延迟。
*   **常见陷阱**：不要在插件配置中硬编码 API Key。请使用 Higress 的资源凭证或 K8s Secret 进行管理，避免密钥泄露到 Git 仓库或日志中。

### 2. 实施基于 Token 计数的精细化限流
*   **场景**：大模型 API 的调用成本主要取决于 Token 消耗量，传统的 QPS（每秒请求数）或并发数限制无法有效控制成本。
*   **建议**：启用 Higress 针对 AI 请求的特定限流策略。配置基于 `Token` 或 `Request Count` 的后端限流。
*   **最佳实践**：针对不同的用户或 API Key 设置不同的 Token 预配额。例如，免费用户每分钟限制 10k Tokens，付费用户限制 100k Tokens，以此实现基于商业逻辑的流量控制。
*   **常见陷阱**：忽略流式传输中的 Token 计算延迟。流式请求是分块返回的，确保限流策略是基于预估的 Prompt Token 或请求头中的元数据，而非等待响应结束才统计，否则会导致突发流量下的超卖。

### 3. 构建语义缓存层以降低 API 成本
*   **场景**：业务中存在大量重复或相似的问题（如常见客服问答），每次都请求 LLM 成本高且延迟高。
*   **建议**：利用 Higress 的缓存插件，结合向量化数据库（如 Redis 向量搜索）或配置本地缓存策略，对相似问题的回答进行缓存。
*   **最佳实践**：设置合理的缓存键。对于 AI 请求，缓存键不应仅是 URL，而应包含请求体的摘要或向量化指纹，确保语义相同的请求能命中缓存，同时设置较短的 TTL（过期时间）以保证信息的时效性。
*   **常见陷阱**：盲目缓存所有状态码为 200 的响应。如果 LLM 返回了部分错误但状态码正常的 JSON，缓存该结果会导致后续用户持续收到错误回答。建议仅对完整且结构正确的响应进行缓存。

### 4. 配置模型供应商的故障转移
*   **场景**：单一的大模型供应商可能出现服务不可用或限流，导致业务中断。
*   **建议**：在 Higress 的路由或服务配置中设置多模型供应商备份。例如，主线路使用 OpenAI GPT-4，备份线路使用通义千问或 Azure OpenAI。
*   **最佳实践**：结合 Higress 的**主动健康检查**与**被动重试**机制。当主供应商的 API 响应时间超过阈值或返回 5xx 错误时，网关应自动将流量切换至备用供应商，且对客户端透明。
*   **常见陷阱**：未处理不同供应商间的协议差异。虽然 Higress 做了统一，但不同模型的参数（如 `temperature`, `top_p`）范围可能不同，在切换时需注意参数映射，避免因参数越界导致备用接口调用失败。

### 5. 优化流式传输的网关超时配置
*   **场景**：AI 生成式回答通常耗时较长，且采用流式（SSE/Stream）返回，默认的网关超时配置往往会中断连接。
*

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API网关](/tags/api%E7%BD%91%E5%85%B3/) / [AI原生](/tags/ai%E5%8E%9F%E7%94%9F/) / [LLM](/tags/llm/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [WASM](/tags/wasm/) / [MCP协议](/tags/mcp%E5%8D%8F%E8%AE%AE/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260130-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260203-github_trending-alibaba-higress-2.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*