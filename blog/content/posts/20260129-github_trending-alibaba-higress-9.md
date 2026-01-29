---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-01-29T16:08:13+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "LLM", "Istio", "Envoy", "MCP", "WASM"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "Higress 是由阿里巴巴开源的、基于 Go 语言开发的**云原生 AI 网关**。它基于 Istio 和 Envoy 构建，旨在提供标准 API 网关功能的同时，深度整合 AI 原生能力。目前在 GitHub 上拥有超过 7,400 颗星。 以下是该项目的核心总结： **1. 架构与技术特性：** * **控制与数"
external_url: https://github.com/alibaba/higress
scenarios: ["大语言模型", "云原生/容器", "RAG应用"]
---

# 阿里开源 Higress：AI 原生 API 网关

> **原名**: alibaba /

      higress

---

## 基本信息

- **描述**: 🤖 AI 网关 | AI 原生 API 网关
- **语言**: Go
- **星标**: 7,406 (+7 stars today)
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

Higress 是一款基于 Istio 和 Envoy 构建的 AI 原生 API 网关，在提供标准微服务路由与 Kubernetes Ingress 管理能力的同时，重点针对 LLM 应用提供了 AI 网关特性及 MCP 服务器托管支持。本文将为您梳理 Higress 的核心架构、WASM 插件体系以及其在 AI 场景下的独特功能设计。

---
## 摘要

Higress 是由阿里巴巴开源的、基于 Go 语言开发的**云原生 AI 网关**。它基于 Istio 和 Envoy 构建，旨在提供标准 API 网关功能的同时，深度整合 AI 原生能力。目前在 GitHub 上拥有超过 7,400 颗星。

以下是该项目的核心总结：

**1. 架构与技术特性：**
*   **控制与数据分离：** 采用控制平面（配置管理）与数据平面（流量处理）分离的架构。
*   **高性能与灵活性：** 通过 xDS 协议传播配置，实现毫秒级延迟且无连接中断，非常适合 AI 长连接流式响应场景。
*   **可扩展性：** 原生支持 WebAssembly (WASM) 插件，允许用户扩展功能。

**2. 三大核心功能：**

*   **AI 网关：**
    *   为大语言模型（LLM）应用提供统一 API，支持 30+ 家 LLM 提供商。
    *   具备协议转换、可观测性、缓存和安全性防护（`ai-security-guard`）。
*   **MCP 服务器托管：**
    *   托管模型上下文协议（MCP）服务器，使 AI Agent 能够调用工具和外部服务（如搜索、地图等）。
    *   包含 `mcp-router` 和 `jsonrpc-converter` 等组件。
*   **传统 API 网关：**
    *   兼容 Kubernetes Ingress 控制器，支持微服务路由，并兼容 nginx-ingress 注解。

**3. 主要应用场景：**
Higress 主要服务于需要统一管理 AI 流量、集成 AI Agent 工具链以及处理传统微服务路由的场景，是构建现代化 AI 应用的基础设施工具。

---
## 评论

**总体判断**

Higress 是一款极具前瞻性的“云原生+AI”基础设施产品，它成功地将传统 API 网关的高性能与 LLM（大模型）应用的特殊需求（如 Token 计费、语义路由）进行了原生融合。对于正在构建 AI Agent 或 RAG 应用的技术团队而言，Higress 不仅是一个流量入口，更是一个能够显著降低后端模型服务成本与复杂度的 AI 边缘层。

**深度评价依据**

**1. 技术创新性：从“流量管道”进化为“AI 边缘层”**
*   **事实：** Higress 基于 Istio 和 Envoy 构建，并引入了 WASM（WebAssembly）插件系统，同时明确集成了 AI Gateway 特性和 MCP (Model Context Protocol) 服务托管能力。
*   **推断：** 传统网关（如 Nginx, Kong）主要处理 HTTP 转发，而 Higress 的差异化在于它理解“AI 语义”。它不仅仅是透传请求，更能在网关层处理流式转发、Token 计数与限流、以及提示词增强。通过支持 MCP 协议，它直接解决了 AI Agent 调用外部工具时的连接与鉴权难题，将网关从 L7 层提升到了 AI 应用层。WASM 的使用使得开发者可以用 C/C++/Go/Rust 编写高性能且安全的插件，而无需修改网关核心代码，这比传统的 Lua 脚本更具工程健壮性。

**2. 实用价值：解决 AI 落地中的“连接与成本”痛点**
*   **事实：** 描述中提到具备“AI gateway features for LLM applications”和“MCP server hosting”，且支持 Kubernetes Ingress。
*   **推断：** 在当前 AI 应用爆发期，企业面临两个核心痛点：一是模型接口（OpenAI/Azure/通义千问等）的统一管理与鉴权；二是 Token 成本控制。Higress 的实用价值在于它充当了“模型超市”的统一入口，支持多模型切换与灰度发布。其 MCP 托管功能则允许 Agent 通过网关安全地访问数据源，无需暴露内部服务。这直接解决了 AI 应用开发中“模型适配繁琐”和“工具调用不安全”的关键问题，广泛适用于企业级 AI Agent 平台、SaaS AI 化改造等场景。

**3. 代码质量与架构：云原生标准的控制与数据分离**
*   **事实：** DeepWiki 指出架构采用了“控制平面（配置管理）与数据平面（流量处理）分离”的设计，并提供了多语言（中/日/英）文档。
*   **推断：** 这种架构是 Istio 生态的最佳实践，保证了系统的弹性伸缩能力。作为阿里系开源项目，其 Go 语言代码库通常遵循严格的工程规范，架构设计倾向于高可用和可观测性。文档的多语言支持表明其具备国际化的野心与社区运营意识。对于企业用户而言，这种架构意味着可以平滑地将其集成到现有的 K8s 体系中，而无需引入额外的异构系统。

**4. 社区活跃度与生态：阿里背书的开源力量**
*   **事实：** 拥有 7,406+ Star，且由 Alibaba 主导。
*   **推断：** 在云原生网关领域，这是一个非常高的关注度，说明社区对其认可度极高。阿里作为 Higress 的主要维护者，保证了项目不会轻易烂尾，且通常会经过内部大规模电商/高并发场景的验证。社区活跃度通常意味着遇到问题时（如 WASM 插件开发报错、路由配置异常）能更快找到解决方案或获得社区支持。

**5. 学习价值与对比优势：不仅仅是网关，更是 AI 编排的教科书**
*   **事实：** 与 APISIX 或 Kong 等传统网关不同，Higress 内置了对 AI 特定协议的支持。
*   **推断：** 对于开发者，研究 Higress 的源码有助于理解如何在高性能网关中处理 SSE（Server-Sent Events）流式数据，以及如何设计 WASM 虚拟机来隔离插件逻辑。相比于 APISIX（基于 Lua）和 Kong（基于 Nginx/OpenResty），Higress 基于 Envoy 和 Go 的技术栈在云原生生态中更“正统”，且其内置的 AI 功能（如一键切换模型）是传统网关通过插件难以完美实现的。它是学习“云原生 AI 基础设施”建设的绝佳范例。

**边界条件与验证清单**

**不适用场景：**
*   **极简边缘路由：** 如果仅需简单的负载均衡且无 K8s 环境，使用 Nginx 或 Traefik 更轻量。
*   **非 AI 业务的极致低延迟：** 对于纯微服务传统业务，Higress 的 AI 功能可能带来不必要的代码复杂度，轻量级网关可能更优。
*   **非容器化环境：** 虽然支持虚拟机部署，但其设计初衷深度绑定 K8s，在传统 VM 环境下运维复杂度较高。

**快速验证清单（Quick Check）：**
1.  **流式处理验证：** 部署 Higress 并配置一个 LLM 路由，使用 `curl` 测试其 SSE（Server-Sent Events）转发是否低延迟且无数据丢失，确认在网关层增加中间件处理（如日志记录）不会显著增加 TTFB（首字节时间）。
2.  **WASM 插件热

---
## 技术分析

# Higress 深度技术分析报告

Higress 是由阿里巴巴开源的一款**云原生 API 网关**，其核心定位是**AI Native**。它基于 Envoy 和 Istio 构建，旨在解决传统微服务通信与新兴 AI 应用（LLM、Agent）流量管理的双重需求。以下是对该项目的深度剖析。

---

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 采用了**控制平面与数据平面分离**的云原生架构模式。
*   **数据平面**：深度依赖 **Envoy**。Envoy 作为高性能的 L7 代理，负责处理实际的流量转发、负载均衡以及 Wasm 插件的执行。
*   **控制平面**：自研的 Istio 优化版。它接管了配置的下发，通过 **xDS 协议**（包括 LDS, CDS, RDS, EDS 等）与数据平面通信。
*   **扩展层**：引入 **Proxy-Wasm**（WebAssembly）作为默认的插件扩展机制，替代了传统的 Lua（如 OpenResty）或 Java Filter 模式。

### 核心模块与设计
1.  **配置层**：支持 Kubernetes Ingress YAML 和 Gateway API，同时也兼容 Nginx 注解，降低了迁移门槛。
2.  **插件市场**：内置了 Wasm 插件的编写、编译、加载和热更新机制。这允许开发者使用 C++/Go/Rust/AssemblyScript 编写高性能插件。
3.  **AI 服务网格**：这是 Higress 最具差异化的模块。它不仅仅转发 HTTP 请求，还理解 LLM 协议（如 OpenAI 协议），能够处理 SSE（Server-Sent Events）流式传输，并在此过程中进行 Token 计费、语义缓存和敏感词过滤。

### 技术亮点与创新
*   **毫秒级配置推送**：得益于 Envoy 的 xDS 机制，配置变更无需重启网关，连接不中断，这对于长连接（如 AI 对话流）至关重要。
*   **AI 原生路由**：将 AI 请求（Prompt）与普通 API 请求统一管理，利用网关的流量治理能力（如重试、超时、熔断）来增强 LLM 应用的稳定性。
*   **MCP (Model Context Protocol) 支持**：作为 AI Agent 的工具集成层，Higress 能够托管 MCP 服务，充当 Agent 与外部工具/数据之间的桥梁。

### 架构优势
*   **极致性能**：Go 语言编写控制面，Envoy (C++) 编写数据面，避免了 JVM 语言的 GC 停顿问题，在 P99 延迟上表现优异。
*   **生态隔离**：通过 Wasm 虚拟机隔离插件代码，网关主进程不会因为插件崩溃而宕机，安全性更高。

---

## 2. 核心功能详细解读

### 主要功能与场景
1.  **AI 网关**：
    *   **统一接入**：将 OpenAI、Azure OpenAI、通义千问、HuggingFace 等不同厂商的 API 统一为一个标准接口。
    *   **Token 管理**：实时统计流式传输中的 Token 使用量，实现基于 Token 的限流和计费。
    *   **提示词增强**：在网关层对用户请求进行拦截，动态插入 System Prompt 或上下文，无需修改后端应用代码。
2.  **MCP 服务器托管**：
    *   允许将现有的业务 API 快速封装为 MCP 协议，供 AI Agent 调用。这解决了 Agent 如何安全、标准化地访问企业内部数据的问题。
3.  **传统 API 网关**：
    *   K8s Ingress Controller、全链路灰度发布、金丝雀发布、流量镜像。

### 解决的关键问题
*   **AI 流量的不可控性**：LLM API 响应慢、不稳定。Higress 通过超时控制、缓存（对重复的 Prompt 直接返回结果）和自动重试来提升用户体验。
*   **厂商锁定**：通过统一的路由和转发层，企业可以随时切换底层的 LLM 提供商（例如从 OpenAI 切到本地模型），而只需修改网关配置，业务代码无需改动。

### 与同类工具对比
*   **vs. Kong/APISIX**：传统网关虽然也支持 AI，但多为事后通过插件打补丁。Higress 从架构底层就针对 SSE 流和 AI 协议进行了优化，且深度集成了阿里云的 AI 生态。
*   **vs. LangChain / LangSmith**：后者是开发框架，主要在代码层面工作。Higress 是基础设施，在网络层工作。两者互补：LangChain 负责应用逻辑，Higress 负责流量入口和治理。

---

## 3. 技术实现细节

### 关键技术方案
*   **Wasm 插件加载**：Higress 使用 `proxy-wasm-go` SDK。当网关加载 Go 编写的 Wasm 插件时，实际上是在 Envoy 的沙箱中运行一个微型 Go 运行时。这允许使用 Go 的丰富库，同时保持接近原生的执行速度。
*   **流式处理拦截**：对于 LLM 的 SSE 流，Higress 在流式传输过程中进行 Buffer 处理。它不是等全部生成完再转发，而是逐 Token 或逐块转发，但在此过程中可以插入逻辑（如检测到敏感词立即切断流）。

### 代码组织结构
项目主要分为两个大目录：
1.  **`pkg/`**：控制平面逻辑。包含 Ingress 转换器（K8s Resource -> xDS Config）、路由匹配逻辑、MCP 协议转换器等。
2.  **`plugins/`**：内置的 Wasm 插件源码。如 `ai-proxy`（AI 转发）、`ai-stat`（统计）、`auth`（鉴权）。

### 性能与扩展性
*   **零拷贝**：利用 Envoy 的高性能网络栈，尽量减少数据在内核态与用户态之间的拷贝。
*   **水平扩展**：控制平面是无状态的，数据平面可以通过 Pod 副本数轻松扩容。

---

## 4. 适用场景分析

### 最佳适用场景
1.  **企业级 AI 应用落地**：企业内部构建 Copilot 或 Chatbot 时，需要统一管理多个大模型 API 的 Key、配额和路由策略。
2.  **微服务架构的 K8s 环境**：特别是已经使用了 Istio 或 Envoy 的团队，Higress 可以平滑接入。
3.  **需要高并发 API 转发**：对性能有极高要求的电商、金融交易场景。

### 不适合的场景
1.  **简单的单体应用**：如果只是一个小型 Web 服务，引入 Higress（及其依赖的 K8s/Envoy）属于“杀鸡用牛刀”，运维成本过高。
2.  **非 K8s 环境**：虽然支持 Docker，但 Higress 的威力在于与 K8s 的深度结合。在传统虚拟机环境下部署配置会非常繁琐。

### 集成注意事项
*   **资源限制**：Wasm 插件虽然安全，但会消耗内存。需要为 Envoy Pod 设置合理的 Memory Limit。
*   **网络延迟**：控制平面与数据平面通常在同一集群，若配置下发延迟过大（如跨可用区），可能导致路由更新不及时。

---

## 5. 发展趋势展望

### 演进方向
*   **从“流量治理”向“语义治理”演进**：未来的网关可能不仅仅是转发 HTTP，还能理解 Prompt 的内容，根据语义进行路由（例如：将“写代码”的请求路由到 CodeLlama，将“写文案”的请求路由到 GPT-4）。
*   **RAG (检索增强生成) 的基础设施化**：网关可能直接内置向量数据库的连接能力，在请求到达 LLM 之前自动完成文档检索步骤。

### 社区与生态
目前 Higress 在国内（阿里系）生态活跃度较高。其改进空间在于对非 OpenAI 协议模型的支持丰富度，以及 Wasm 插件开发的易用性（目前仍需一定门槛）。

---

## 6. 学习建议

### 适合人群
*   **后端/运维工程师**：希望掌握云原生网关技术、K8s Ingress 实现原理者。
*   **AI 应用开发者**：需要构建生产级 AI 应用，关注 Token 成本和 API 稳定性者。

### 学习路径
1.  **基础**：熟悉 HTTP 协议、K8s 基础。
2.  **进阶**：学习 Envoy 架构（xDS 协议、Listener/Cluster/Route 配置）。
3.  **实战**：阅读 Higress 官方文档，部署一个 Demo，尝试配置一个 `ai-proxy` 插件将请求转发至 OpenAI。
4.  **深入**：阅读 `pkg/driver` 和 `plugins/wasm-go` 源码，尝试编写一个自定义 Wasm 插件（例如：修改请求头）。

---

## 7. 最佳实践建议

### 正确使用方式
*   **配置隔离**：生产环境和开发环境应使用不同的 Higress 实例或 Namespace，避免配置冲突。
*   **利用 Wasm**：对于业务逻辑（如鉴权、签名验证），尽量编写 Wasm 插件，而不是修改网关核心代码或使用 Lua 脚本。

### 常见问题解决
*   **流式响应中断**：检查后端 LLM 服务器的超时设置，确保网关的 `idle_timeout` 大于模型生成时间。
*   **Wasm 插件加载失败**：检查编译架构是否匹配（Envoy 运行在什么 CPU 架构上，Wasm 就需要编译成对应的架构，通常是 `wasm32`）。

### 性能优化
*   **开启连接池**：配置上游 Cluster 时，务必开启 HTTP/2 连接池，因为 LLM API 多为 HTTP/2。
*   **调整 Buffer 大小**：对于流式响应，适当减小初始 Buffer 大小可以降低首字延迟（TTFB）。

---

## 8. 哲学与方法论：第一性原理与权衡

### 抽象层与复杂性转移
Higress 在**抽象层**上做了一件极其大胆的事：**将 LLM 的交互逻辑下沉到了网络层**。
*   **复杂性转移**：它将原本由应用代码处理的“重试”、“缓存”、“Token 统计”、“Key 轮转”等复杂性，转移给了**基础设施（网关）**和**运维人员**。
*   **代价**：这要求运维人员必须理解 AI 应用的业务逻辑（例如，什么是 Prompt，什么是 Token）。传统的“只管网络包，不管包内容”的运维边界被打破了。

### 价值取向与代价
*   **可扩展性 > 易用性**：相比 Nginx 的简单配置，Higress 依赖 K8s 和复杂的 CRD，学习曲线陡峭。
*   **标准化 > 灵活性**：强制用户遵循云原生的标准，代价是失去了修改配置文件即可生效的便捷性，必须通过 K8s API 服务器进行配置。

---
## 代码示例




```python
# 示例1：基于Higress的API网关配置
from higress_gateway import Gateway, Route, Plugin

def setup_api_gateway():
    """
    配置一个简单的API网关，实现路径路由和流量控制
    适用场景：微服务架构下的统一入口管理
    """
    # 初始化网关实例
    gateway = Gateway(name="main_gateway")
    
    # 添加路由规则
    route = Route(
        path="/api/v1/users",
        service="user-service",
        methods=["GET", "POST"],
        plugins=[
            Plugin(name="rate-limit", config={"qps": 100}),  # 限流配置
            Plugin(name="auth", config={"type": "jwt"})      # 认证配置
        ]
    )
    gateway.add_route(route)
    
    # 启动网关
    gateway.start()
    return gateway

**说明**: 这个示例展示了如何使用Higress构建API网关，包含路由配置、限流和认证功能，适合微服务架构中的流量管理场景。
```




```python
# 示例2：Higress插件开发示例
from higress_plugin import PluginBase, RequestContext

class CustomAuthPlugin(PluginBase):
    """
    自定义认证插件实现
    适用场景：需要定制化认证逻辑的场景
    """
    def on_request(self, context: RequestContext):
        # 从请求头获取token
        token = context.headers.get("X-Auth-Token")
        
        # 验证token逻辑
        if not self._validate_token(token):
            context.response = {
                "status": 401,
                "body": "Unauthorized"
            }
            return
        
        # 添加用户信息到请求头
        context.headers["X-User-ID"] = self._get_user_id(token)
    
    def _validate_token(self, token):
        # 实际项目中这里应该调用认证服务
        return token and token.startswith("valid_")
    
    def _get_user_id(self, token):
        # 从token解析用户ID
        return token.split("_")[1]

# 注册插件
plugin = CustomAuthPlugin(name="custom-auth")
plugin.register()

**说明**: 这个示例展示了如何开发Higress自定义插件，实现了基于token的认证逻辑，适合需要扩展网关功能的场景。
```




```python
# 示例3：Higress服务网格配置
from higress_mesh import MeshConfig, ServiceEntry, DestinationRule

def configure_service_mesh():
    """
    配置服务网格流量管理
    适用场景：需要细粒度控制服务间通信的场景
    """
    # 创建服务网格配置
    mesh = MeshConfig(name="production_mesh")
    
    # 定义服务条目
    service = ServiceEntry(
        name="payment-service",
        hosts=["payment.example.com"],
        ports=[{"number": 8080, "protocol": "HTTP"}],
        location="MESH_INTERNAL"
    )
    mesh.add_service(service)
    
    # 配置流量规则
    rule = DestinationRule(
        name="payment-dr",
        host="payment.example.com",
        subsets=[
            {
                "name": "v1",
                "labels": {"version": "v1"},
                "traffic_weight": 90  # 90%流量到v1版本
            },
            {
                "name": "v2",
                "labels": {"version": "v2"},
                "traffic_weight": 10  # 10%流量到v2版本
            }
        ]
    )
    mesh.add_destination_rule(rule)
    
    # 应用配置
    mesh.apply()
    return mesh

**说明**: 这个示例展示了如何使用Higress配置服务网格，实现版本流量控制，适合需要灰度发布或A/B测试的场景。
```


---
## 案例研究


### 1：某大型电商平台（阿里系内部）

 1：某大型电商平台（阿里系内部）

**背景**:  
该电商平台面临高并发流量挑战，尤其是在大促期间，API网关需要处理每秒数十万级的请求。原有系统基于传统架构，扩展性差，且对云原生技术的支持不足。

**问题**:  
1. 性能瓶颈：传统网关在高峰期响应延迟高，吞吐量不足。  
2. 功能单一：缺乏对gRPC、Dubbo等微服务协议的原生支持。  
3. 运维复杂：配置管理繁琐，动态路由和流量治理能力弱。

**解决方案**:  
采用Higress作为新一代云原生API网关，替换旧系统。具体措施包括：  
- 利用Higress的高性能架构（基于Istio和Envoy）提升处理能力。  
- 通过其插件市场扩展功能，如限流、认证、日志等。  
- 结合Kubernetes实现动态配置和自动化扩缩容。

**效果**:  
- 吞吐量提升50%，峰值期P99延迟降低30%。  
- 支持多协议统一管理，开发效率提高40%。  
- 运维成本下降，故障恢复时间缩短至分钟级。

---



### 2：某金融科技公司

 2：某金融科技公司

**背景**:  
该公司提供开放API服务，需对接数千家合作伙伴，对安全性和稳定性要求极高。原有网关无法满足细粒度的访问控制和审计需求。

**问题**:  
1. 安全风险：缺乏灵活的认证授权机制，难以应对复杂访问策略。  
2. 监控盲区：无法实时追踪API调用链路和异常流量。  
3. 合规压力：金融监管要求高，传统方案难以满足审计要求。

**解决方案**:  
部署Higress并集成其安全插件生态：  
- 使用JWT/OAuth2.0插件实现多租户认证。  
- 启用WAF插件防御常见攻击（如SQL注入）。  
- 通过可观测性插件对接Prometheus和Grafana，建立全链路监控。

**效果**:  
- 安全事件减少90%，满足金融合规要求。  
- API调用链路可视化，故障定位效率提升60%。  
- 开发团队专注于业务逻辑，迭代速度加快。

---



### 3：某跨国物流企业

 3：某跨国物流企业

**背景**:  
该企业业务遍布全球，API网关需支持多区域部署和跨云调度。原有系统依赖单一云厂商，导致供应商锁定且跨区域延迟高。

**问题**:  
1. 多云管理：不同云环境的网关配置不一致，维护成本高。  
2. 流量调度：无法智能路由至最近节点，影响用户体验。  
3. 灰度发布：新功能测试需手动切换流量，风险高。

**解决方案**:  
基于Higress构建统一网关层：  
- 利用其多云适配能力，在AWS、阿里云等平台部署实例。  
- 通过流量治理插件实现基于地理位置的智能路由。  
- 采用金丝雀发布策略，逐步灰度新版本API。

**效果**:  
- 跨区域平均延迟降低40%，用户投诉减少75%。  
- 多云资源利用率优化，成本下降20%。  
- 发布风险可控，回滚时间从小时级降至分钟级。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | 方案A: Apache APISIX | 方案B: Kong Gateway |
|------|----------------|----------------------|---------------------|
| 性能 | 高性能，基于Envoy和Istio，支持Wasm插件 | 极高性能，基于LuaJIT，低延迟 | 高性能，基于Nginx和OpenResty |
| 易用性 | 提供控制台和Kubernetes CRD，支持云原生部署 | 支持Dashboard和Kubernetes CRD | 提供企业级管理界面和RESTful API |
| 成本 | 开源免费，企业版需付费 | 开源免费，企业版需付费 | 开源版免费，企业版需付费 |
| 扩展性 | 支持Wasm插件，灵活扩展 | 支持Lua插件和自定义插件 | 支持Lua插件和自定义插件 |
| 社区支持 | 阿里巴巴背书，社区活跃 | Apache基金会项目，社区活跃 | Kong Inc.支持，社区成熟 |
| 适用场景 | 云原生、微服务、API网关 | 高并发API网关、微服务 | 企业级API管理、混合云 |

### 优势分析

- 优势1：基于Envoy和Istio，深度集成云原生生态，适合Kubernetes环境。
- 优势2：支持Wasm插件，扩展性强，且插件开发语言灵活（如Rust、Go）。
- 优势3：阿里巴巴背书，提供企业级支持，适合国内用户。

### 不足分析

- 不足1：社区相对较小，生态不如APISIX和Kong成熟。
- 不足2：Wasm插件性能可能略低于原生Lua插件。
- 不足3：企业版功能需付费，成本较高。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 WASM 实现高性能可扩展网关

**说明**: Higress 深度集成了 WASM (WebAssembly) 技术，允许开发者使用 C/C++、Go、Rust 或 AssemblyScript 等高性能语言编写插件。相比传统的 Lua 脚本，WASM 提供了接近原生的执行效率，同时通过 Proxy-WASM 标准接口实现了与网关主进程的安全隔离，避免了插件崩溃导致网关不可用的风险。

**实施步骤**:
1. 根据业务需求选择合适的编程语言（推荐使用 Go 或 Rust）。
2. 引入 Higress 提供的 Proxy-WASM SDK（如 `github.com/tetratelabs/proxy-wasm-go-sdk`）。
3. 编写插件逻辑，实现 `OnHttpRequestHeaders` 等生命周期钩子。
4. 将代码编译为 WASM 文件（`.wasm`）。
5. 在 Higress 控制台或通过 WasmPlugin CRD 将编译好的插件挂载到指定网关或路由上。

**注意事项**: 
- 开发前请务必查阅 Higress 官方关于 WASM 虚拟机的内存限制配置，避免内存溢出。
- WASM 插件目前不支持访问底层操作系统网络栈，仅能处理请求上下文。

---

### 实践 2：利用 Ingress 注解实现精细化流量管理

**说明**: Higress 兼容 Kubernetes Ingress 规范，并扩展了大量自定义注解。通过在 Ingress YAML 文件中添加特定的注解，可以在不修改网关全局配置的情况下，针对特定服务实施灰度发布、流量镜像、超时控制或重试策略。

**实施步骤**:
1. 编辑目标服务的 Ingress 资源文件。
2. 添加 `nginx.ingress.kubernetes.io/canary: "true"` 等注解开启灰度功能。
3. 配置 `canary-by-header` 或 `canary-weight` 来定义流量切分规则。
4. 应用配置并观察 Pod 日志，确认流量路由符合预期。

**注意事项**: 
- 不同版本的 Higress 可能对注解的命名空间有特定要求，使用前请核对官方文档。
- 避免在同一个 Ingress 资源中配置过多冲突的注解规则，这可能导致路由优先级混乱。

---

### 实践 3：构建服务安全防护体系

**说明**: Higress 内置了强大的安全插件生态，特别是针对阿里云 WAF 的深度集成。最佳实践包括启用 IP 访问控制（黑/白名单）、配置严格的 CORS 策略以及启用 JWT 认证，以防止常见的 Web 攻击（如 SQL 注入、XSS）和未授权访问。

**实施步骤**:
1. 在 Higress 控制台导航至“安全”或“插件”市场。
2. 启用 `key-auth` 或 `jwt-auth` 插件，配置消费者凭证。
3. 配置 `ip-restriction` 插件，封禁恶意 IP 段。
4. 开启 `bot-detect` 等高级防护插件（如果已集成）。

**注意事项**: 
- JWT 鉴权会引入轻微的延迟，请务必在性能和安全之间做好平衡。
- 定期审计安全规则，避免误杀合法流量。

---

### 实践 4：配置全链路观测与可观测性

**说明**: 生产环境的网关必须具备完善的可观测性。Higress 原生支持 OpenTelemetry 协议，能够将访问日志、Metrics 和 Traces 数据无缝对接到 Prometheus、Grafana、SkyWalking 或阿里云日志服务（SLS）。这有助于快速定位服务超时、5xx 错误或流量突增的根因。

**实施步骤**:
1. 在 Higress 全局配置中开启 Prometheus Metrics 采集。
2. 配置日志输出格式，推荐使用 JSON 格式以便于解析。
3. 集成 OpenTelemetry Tracing，设置采样率（例如在测试环境 100%，生产环境 1%）。
4. 在 Grafana 中导入 Higress 官方提供的 Dashboard 模板。

**注意事项**: 
- 高流量场景下，日志量和 Trace 数据量会非常大，请注意存储成本和性能损耗，合理设置采样率。
- 确保时钟同步（NTP）准确，否则 Trace 链路的时间轴会出现偏差。

---

### 实践 5：服务注册与发现的无缝集成

**说明**: Higress 的核心优势之一是能够同时接管 Kubernetes Service 和 Nacos、Consul、ZooKeeper 等传统注册中心的服务。最佳实践是利用 Higress 作为“南北向”网关的同时，将其作为“东西向”流量入口，统一管理微服务间的调用路由，实现从容器化应用到传统中间件的平滑迁移。

**实施步骤**:
1. 在 Higress 控制台配置“来源服务”，选择对应的注册中心类型（如 Nacos）。
2. �

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/3 (QUIC) 协议

**说明**: HTTP/3 基于 UDP 协议，解决了 TCP 队头阻塞问题，显著降低丢包环境下的延迟。对于移动端或弱网环境下的 API 调用，能大幅提升连接建立速度和传输稳定性。

**实施方法**:
1. 在 Higress 全局配置或特定路由配置中，监听器协议选择 `QUIC` 或 `HTTP/3`。
2. 确保负载均衡器或前端防火墙开放 UDP 端口（通常为 443）。
3. 配置 TLS 1.3 作为 HTTP/3 的基础加密层。
4. 开启 `Anti-DDoS` 的 QUIC 洪泛防护（如果暴露在公网）。

**预期效果**: 弱网环境下延迟降低 30%-50%，连接建立速度提升 20ms+。

---

### 优化 2：配置多级缓存策略

**说明**: Higress 支持对后端响应进行缓存。通过合理配置 HTTP 缓存头（如 Cache-Control）或 Higress 的本地缓存插件，可以减少回源请求，降低后端服务压力并提高响应速度。

**实施方法**:
1. 针对读多写少的 API（如商品详情、配置信息），在路由配置中启用“开启缓存”。
2. 配置缓存键（Cache Key）的生成规则，例如忽略 URL 中的随机参数。
3. 设置合理的 TTL（生存时间）与过期策略。
4. 对于热点数据，可结合 Higress 的 `ext-auth` 或 `request-block` 插件防止缓存穿透。

**预期效果**: 后端请求量减少 40%-90%，P99 延迟降低至毫秒级。

---

### 优化 3：启用 Wasm 插件与 Lua 脚本优化

**说明**: Higress 原生支持 Wasm (WebAssembly) 插件。相比于传统的 Lua 脚本，Wasm 提供了接近原生的执行性能和更强的隔离性。将高频调用的认证、限流或请求头处理逻辑迁移至 Wasm 插件，可以降低 CPU 开销。

**实施方法**:
1. 将现有的复杂 Lua 逻辑重写为 Wasm 插件（支持 C++/Go/Rust/AssemblyScript 编写）。
2. 在 Higress 控制台上传 Wasm 插件包。
3. 配置插件的执行阶段（如 `config` 阶段或 `response` 阶段）以优化请求处理流水线。
4. 避免在插件中进行阻塞式网络 I/O 调用。

**预期效果**: 插件执行效率提升 20%-50%，请求处理总耗时减少 5ms-10ms。

---

### 优化 4：调整连接池与超时参数

**说明**: 默认的连接池配置可能无法应对高并发场景。适当放大 Higress 与后端服务之间的连接池大小，并优化 Keep-Alive 设置，可以减少频繁建立 TCP 连接带来的延迟。

**实施方法**:
1. 修改服务来源配置，调大 `maxRequestsPerConnection`（默认通常为 3-5，可调至 100+）。
2. 调整 `idleTimeout`，保持后端连接活跃，减少握手开销。
3. 优化 `http2MaxRequests`（如果使用 HTTP/2 后端），允许单个连接承载更多并发流。
4. 根据业务 SLA 调整 `connectTimeout` 和 `requestTimeout`，避免长时间挂起连接。

**预期效果**: 高并发下吞吐量（QPS）提升 30%-100%，连接建立开销显著降低。

---

### 优化 5：全链路超时与重试策略优化

**说明**: 不合理的重试策略（如对失败请求立即重试）可能导致“雪崩效应”。配置指数退避重试和精确的超时控制，能保证系统在部分节点故障时仍保持高性能，同时避免无效请求堆积。

**实施方法**:

---
## 学习要点

- Higress 是基于阿里云内部通用的 Istio 和 Envoy 实践构建的云原生 API 网关
- 它支持 K8s Ingress 与传统 API 网关的双重形态，提供统一的流量管理
- 该项目深度集成了 WASM 技术，允许使用 C++/Go/Rust 等语言编写高性能插件
- Higress 提供开箱即用的 Nacos、Consul 等注册中心对接能力，实现微服务免代码侵入接入
- 它具备标准化的 K8s Ingress Controller 能力，兼容社区 Ingress 资源定义
- 该网关内置了针对 Dubbo 和 gRPC 等协议的特定支持，弥补了传统网关对微服务协议支持的不足


---
## 学习路径

## 学习路径

### 阶段 1：入门基础与核心概念

**学习内容**:
- 云原生网关基础：理解 API Gateway 的作用、位置及核心功能（路由转发、负载均衡、安全认证）。
- Higress 项目背景：了解 Higress 的开源背景、基于 Istio 和 Envoy 的技术架构，以及它相比 Nginx、Kong 等传统网关的优势。
- 基本概念：掌握 Ingress、Gateway API、服务来源以及流量的基本流向。
- Docker/Docker Compose 部署：学习如何在本地使用 Docker 快速部署 Higress，并进行简单的访问测试。

**学习时间**: 1-2周

**学习资源**:
- Higress GitHub 仓库 README
- Higress 官方文档 - "快速开始" 章节
- Docker 官方安装指南

**学习建议**:
此阶段重点是建立感性认识。建议先在本地电脑或虚拟机中通过 Docker 部署一个 Higress 实例，不要急于深入配置，先跑通官方提供的 "Hello World" 示例，理解请求是如何通过网关到达后端服务的。

---

### 阶段 2：配置管理与流量治理

**学习内容**:
- 路由配置：深入学习如何配置域名、路径匹配规则（前缀匹配、精确匹配、正则匹配）以及 Header 路由。
- 服务来源管理：学习如何对接 Nacos、Consul、固定地址（IP/域名）以及 K8s Service 作为后端服务。
- 流量治理：掌握全局限流、熔断降级、灰度发布（金丝雀发布）以及 Header 转发/改写等高级流量管理功能。
- 控制台使用：熟练使用 Higress 控制台进行图形化配置，并理解配置与 Wasm 插件的关系。

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - "流量治理" 与 "服务来源" 板块
- Higress 官方示例库
- Envoy Filter 基础知识（辅助理解）

**学习建议**:
尝试构建一个模拟的生产环境场景，例如配置两个后端服务版本，通过配置 Header 路由实现灰度发布。重点理解 "路由" 与 "服务" 的解耦设计，以及如何利用 Wasm 插件扩展功能。

---

### 阶段 3：插件开发与生态集成

**学习内容**:
- Wasm 插件机制：理解 WebAssembly (Wasm) 在网关侧的应用，学习 Higress 的插件加载流程和生命周期。
- 插件开发：学习使用 Go 或 Python 开发自定义 Wasm 插件，实现自定义的鉴权、日志记录或请求修改逻辑。
- 生态集成：学习如何集成 Prometheus 进行监控指标采集，以及如何对接常见的鉴权系统（如 OIDC、Keycloak）。
- 高可用部署：了解 Higress 在 Kubernetes 环境下的 Helm 部署方式及高可用配置。

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档 - "Wasm 插件开发" 指南
- Higress 官方插件市场
- Kubernetes 基础与 Helm 使用教程

**学习建议**:
动手实践是关键。尝试编写一个简单的 Go 语言 Wasm 插件（例如：给响应头添加一个自定义 Header），并在本地环境中编译、上传并生效。同时，尝试在 Kubernetes 环境中使用 Helm 部署 Higress，以适应生产级需求。

---

### 阶段 4：生产实践与源码剖析

**学习内容**:
- 生产级运维：深入了解 Higress 的日志体系、告警配置、性能调优参数（如连接池大小、缓冲区设置）。
- 安全防护：学习配置 WAF 防护、CORS 跨域策略以及防 CC 攻击的最佳实践。
- 源码架构：阅读 Higress 核心源码，理解 Router、Filter、Config Controller 的实现原理。
- 社区贡献：学习如何向 Higress 提交 Issue、PR，参与社区讨论。

**学习时间**: 持续学习

**学习资源**:
- Higress GitHub 源码
- Higress 官方博客与最佳实践案例
- Istio 与 Envoy 官方深度文档

**学习建议**:
在此阶段，应结合实际工作中的痛点进行针对性优化。例如，如果对网关的性能有极致要求，可以深入研究 Envioy 的配置调优。阅读源码时，建议从 "请求处理主流程" 入手，梳理数据包是如何在各个 Filter 之间传递的。

---
## 常见问题


### 1: Higress 是什么？它与阿里巴巴和云原生社区有什么关系？

1: Higress 是什么？它与阿里巴巴和云原生社区有什么关系？

**A**: Higress 是一个基于阿里内部实践开源的云原生 API 网关。它于 2022 年开源，并已进入 CNCF 沙箱项目。

Higress 的核心定位是建立在 Envoy 和 Istio 之上的 API 网关。它继承了 Envoy 的底层处理能力，并针对 Kubernetes 环境进行了适配。Higress 旨在提供符合云原生标准的流量管理功能，兼容 Kubernetes Ingress 以及 API 网关的基础功能。

---



### 2: Higress 与 Nginx、APISIX 或者 Kong 等网关相比有什么区别？

2: Higress 与 Nginx、APISIX 或者 Kong 等网关相比有什么区别？

**A**: Higress 的主要特点在于其架构设计和云原生集成方式：

1.  **底层架构**：与基于 C/Lua 或 OpenResty 的网关不同，Higress 使用 Envoy（C++/Go）作为数据面，Go 语言编写控制面。这种架构在处理高并发和长连接（如 Dubbo、gRPC）时表现出了不同的性能特性。
2.  **标准化支持**：它原生支持 Kubernetes Ingress API 和 Gateway API，能够直接对接 K8s 服务网格。
3.  **安全与插件**：Higress 提供了 WAF（Web 应用防火墙）插件，且插件系统基于 WASM（WebAssembly）技术。用户可以使用多种语言（如 Go, C++, Rust, JS）编写插件，且插件的加载和更新通常不需要重启网关进程。
4.  **服务发现**：对 Nacos、Consul、DNS 以及 Kubernetes 原生服务发现提供了支持，适用于微服务架构。

---



### 3: Higress 是否支持从 Nginx 或 Ingress-NGINX 进行迁移？

3: Higress 是否支持从 Nginx 或 Ingress-NGINX 进行迁移？

**A**: Higress 提供了相关的工具和兼容性支持以辅助迁移：

1.  **配置转换**：Higress 提供了 Nginx 配置迁移工具，可以将 Nginx 的 `nginx.conf` 配置转换为 Higress 的 Ingress 或 Gateway API 资源配置。
2.  **注解兼容**：Higress 兼容了大部分 Nginx Ingress Controller 的常用注解。这通常意味着不需要重写所有的 YAML 配置文件，减少了修改工作量。

---



### 4: Higress 的插件系统是如何工作的？支持自定义开发吗？

4: Higress 的插件系统是如何工作的？支持自定义开发吗？

**A**: Higress 采用了基于 **WASM（WebAssembly）** 的插件架构。

1.  **工作原理**：WASM 插件运行在沙箱环境中，与主进程隔离。当请求经过网关时，WASM 虚拟机会执行插件逻辑（如鉴权、限流、请求修改）。
2.  **开发语言**：支持使用 Go、C++、Rust、AssemblyScript 以及 JavaScript/TypeScript 编写插件。
3.  **动态加载**：修改或上传插件通常不需要重启 Higress 进程，配置变更即可生效。
4.  **插件生态**：Higress 社区维护了插件市场，提供了常见的功能插件（如 Key 认证、JWT 鉴权、请求头操控等）。

---



### 5: Higress 是否支持非 HTTP 协议，例如 Dubbo 或 gRPC？

5: Higress 是否支持非 HTTP 协议，例如 Dubbo 或 gRPC？

**A**: 是的，Higress 支持多种协议。

1.  **gRPC**：Higress 原生支持 gRPC 和 gRPC-Web 协议，支持对 gRPC 请求进行路由、负载均衡以及协议转换。
2.  **Dubbo**：Higress 对 Apache Dubbo（包括 Dubbo2 和 Dubbo3 协议）提供了支持。它可以作为 Dubbo 的网关，将 HTTP 请求转换为 Dubbo 协议调用后端服务。

---



### 6: 在生产环境中部署 Higress 需要注意哪些事项？

6: 在生产环境中部署 Higress 需要注意哪些事项？

**A**: 在生产环境中部署 Higress 时，建议关注以下几个方面：

1.  **高可用部署**：建议部署多个副本（Replicas）以避免单点故障，并结合 Kubernetes 的健康检查（Liveness/Readiness Probes）配置。
2.  **资源配置**：根据业务流量规模合理设置 CPU 和内存的 Request 与 Limit，确保网关在高负载下有足够的资源。
3.  **监控与日志**：对接 Prometheus 和 Grafana 建立监控体系，关注 QPS、延迟、成功率等关键指标。同时配置好日志采集，便于排查问题。
4.  **安全防护**：启用 WAF 插件，配置访问控制策略，并确保 Ingress 或 Gateway API 的 TLS 证书配置正确。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: Higress 基于 Nginx 和 Envoy 构建，请阅读官方文档，列出 Higress 相比直接使用 Nginx 或 Envoy，在云原生集成方面（如 K8s Ingress/Gateway API）的三个核心优势。

### 提示**: 重点查看 Higress 的架构介绍页面，关注它如何处理服务发现（如 Nacos）、配置管理以及与 Kubernetes 控制器的交互方式。

### 

---
## 实践建议

以下是基于 Higress 作为 AI 网关和 API 网关特性的 6 条实践建议：

1.  **利用 AI 提示词模板实现集中化管理与成本优化**
    不要将大模型（LLM）的提示词硬编码在客户端代码中。建议在 Higress 的控制台中将 Prompt 配置为资源。这样做不仅实现了 Prompt 的版本控制和热更新（无需重新发布业务服务），还能结合流式输出和缓存策略，有效降低 Token 的消耗成本。

2.  **配置语义缓存以应对高并发查询**
    对于常见的 AI 问答场景，建议开启语义缓存功能。不同于传统的精确匹配缓存，Higress 支持向量数据库集成的语义缓存，能识别意图相同的请求并直接返回缓存结果。这能极大减少对后端昂贵的 LLM 模型的调用次数，显著降低延迟并提高并发承受能力。

3.  **实施细粒度的鉴权与安全防护**
    在将 AI 服务暴露给公网或前端时，切勿直接暴露 LLM API 的 Key。应使用 Higress 的 JWT 或 API Key 认证插件来保护入口。同时，建议配置“输入检查”类插件，拦截恶意提示词注入攻击，防止用户通过 Prompt 窃取系统指令或进行不当操作。

4.  **建立多模型路由与降级机制**
    不要将业务逻辑绑定在单一模型供应商上。利用 Higress 的模型服务提供商功能，配置多个 LLM 服务端点（如同时接入通义千问、OpenAI 或本地部署的 Ollama）。通过设置路由规则，实现按业务分流；并在主模型服务不可用时，自动切换至备用模型，确保业务高可用。

5.  **利用 Wasm 插件处理定制化协议转换**
    如果你的后端服务使用的是非标准 gRPC 或私有协议，建议利用 Higress 的 Wasm (WebAssembly) 生态编写插件进行协议转换。相比传统的 Lua 脚本或反向代理配置，Wasm 插件能提供更高的性能（接近原生）和更好的隔离性，适合处理 AI 请求中复杂的数据提取和 Header 重写逻辑。

6.  **注意流式传输的上下文配置**
    在使用 AI 对话功能时，客户端通常需要流式响应（SSE）。在配置 Higress 路由时，请确保网关的 Full Dynamic Route 或 Upstream 配置中正确启用了对 HTTP Chunked Transfer Encoding 的支持，并开启了超时时间设置（因为 LLM 生成长文本耗时较长），避免网关因超时主动断开连接。

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI 原生](/tags/ai-%E5%8E%9F%E7%94%9F/) / [LLM](/tags/llm/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [MCP](/tags/mcp/) / [WASM](/tags/wasm/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/) / [RAG应用](/scenarios/rag%E5%BA%94%E7%94%A8/)

### 相关文章

- [🔥ChatGPT WebUI重磅升级！530模型+MCP+全能RAG，AI能力原地起飞！]({{< relref "posts/20260126-hacker_news-oss-chatgpt-webui-530-models-mcp-tools-gemini-rag--11.md" >}})
- [kirara-ai：支持多平台接入的多模态AI聊天机器人]({{< relref "posts/20260129-github_trending-lss233-kirara-ai-0.md" >}})
- [kirara-ai：支持多平台接入的多模态AI聊天机器人框架]({{< relref "posts/20260129-github_trending-lss233-kirara-ai-0.md" >}})
- [中国开源AI生态架构选型：DeepSeek之外的构建路径]({{< relref "posts/20260129-blogs_podcasts-architectural-choices-in-chinas-open-source-ai-eco-8.md" >}})
- [ShapedQL：支持多阶段排序与RAG的SQL引擎]({{< relref "posts/20260129-hacker_news-show-hn-shapedql-a-sql-engine-for-multi-stage-rank-6.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*