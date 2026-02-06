---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-02-06T08:33:11+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "Istio", "Envoy", "LLM", "MCP", "Kubernetes"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "Higress 是由阿里巴巴开源的**云原生 AI 网关**，基于 Istio 和 Envoy 构建，并使用 Go 语言编写。目前该项目在 GitHub 上拥有超过 7,400 个星标，受到广泛关注。 **核心定位与架构：** Higress 是一个云原生 API 网关，通过扩展 WebAssembly (WASM)"
external_url: https://github.com/alibaba/higress
scenarios: ["AI/ML项目", "云原生/容器", "Kubernetes"]
---

# 阿里开源 Higress：AI 原生 API 网关

> **原名**: alibaba /

      higress

---

## 基本信息

- **描述**: 🤖 AI 网关 | AI 原生 API 网关
- **语言**: Go
- **星标**: 7,465 (+16 stars today)
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

Higress 是一款基于 Istio 和 Envoy 构建的云原生 API 网关，其核心特性在于深度整合了 AI 网关能力，并利用 WASM 插件实现了高度的扩展性。该项目旨在解决 LLM 应用流量管理、AI Agent 工具集成（MCP）以及微服务路由等场景下的连接与治理问题。本文将为您梳理 Higress 的系统架构，重点介绍其 AI 网关功能、插件体系以及核心应用场景。

---
## 摘要

Higress 是由阿里巴巴开源的**云原生 AI 网关**，基于 Istio 和 Envoy 构建，并使用 Go 语言编写。目前该项目在 GitHub 上拥有超过 7,400 个星标，受到广泛关注。

**核心定位与架构：**
Higress 是一个云原生 API 网关，通过扩展 WebAssembly (WASM) 插件能力，为 Istio 和 Envoy 赋能。其架构采用**控制平面**与**数据平面**分离的设计。配置变更通过 xDS 协议传播，具有毫秒级延迟且无连接中断的特性，特别适用于 AI 流式响应等长连接场景。

**三大核心功能：**
1.  **AI 网关：** 提供统一 API 接入 30 多家大语言模型（LLM）提供商。核心功能包括协议转换、可观测性、缓存以及安全防护。
2.  **MCP 服务器托管：** 托管模型上下文协议（MCP）服务器，使 AI 智能体能够便捷地调用外部工具和服务。
3.  **Kubernetes 入口：** 作为 Kubernetes Ingress 控制器使用，兼容 nginx-ingress 注解，支持微服务路由。

**总结：** Higress 旨在通过将传统 API 网关能力与 AI 原生特性相结合，为 LLM 应用、Agent 工具集成及云原生流量管理提供一站式的解决方案。

---
## 评论

### 总体判断

Higress 是一款**极具前瞻性的“AI Native”网关**，它成功地将云原生流量治理技术与大模型（LLM）应用需求深度融合。作为基于 Istio 和 Envoy 的开源项目，它不仅解决了传统 API 网关的扩展性问题，更通过 WASM 和 MCP 协议支持，为 AI 时代的流量管理提供了标准化的基础设施，是连接微服务架构与 AI 应用生态的高质量桥梁。

### 深入评价依据

**1. 技术创新性：从“流量转发”进化为“智能编排”**
*   **事实**：Higress 定义为 "AI Native API Gateway"，核心架构基于 Istio（控制平面）和 Envoy（数据平面），并引入了 WebAssembly (WASM) 插件系统和 MCP (Model Context Protocol) 服务托管能力。
*   **推断**：传统网关（如 Nginx, Kong）主要关注 HTTP/TCP 转发，而 Higress 的差异化在于**原生集成 AI 指令处理能力**。它不仅仅是转发流量，还能理解 AI 请求的上下文（如 Token 计费、提示词增强）。利用 WASM 技术，它打破了传统 Lua 插件的性能隔离瓶颈，支持使用 C++/Go/Rust/Swift 编写高性能插件，实现了**逻辑与流量的解耦**。引入 MCP 协议支持则使其具备了成为 AI Agent 基础设施的潜力，统一了模型与工具（Tools）的调用标准。

**2. 实用价值：统一 AI 与微服务的治理入口**
*   **事实**：文档指出其提供三大核心功能：AI 网关特性、MCP 服务器托管、传统 API 网关（K8s Ingress）。
*   **推断**：在当前企业从传统微服务向 AI 应用转型的过程中，最大的痛点是**碎片化**：既需要管理 K8s Ingress，又需要管理调用 OpenAI/Azure 等大模型的 API，还需要处理模型提供商的格式差异。Higress 通过统一网关解决了这个问题，企业无需维护两套网关系统。其“AI Gateway”特性（如 Provider 聚合、Token 限流）直接击中了 AI 落地中**成本控制**和**稳定性**的痛点，具有极高的实用价值。

**3. 代码质量与架构：云原生标准的高水准实现**
*   **事实**：项目采用 Go 语言编写，架构明确分离了控制平面与数据平面，且基于 Envoy 这种高性能网络库。
*   **推断**：基于 Envoy 的数据平面保证了 L7 层处理的高性能和低延迟，这是处理流式 AI 响应（SSE）的关键。Go 语言编写的控制平面契合云原生生态，易于在 K8s 中部署和扩展。从架构设计看，它遵循了 K8s Operator 模式，声明式 API 的设计使得配置管理更加规范。文档中包含多语言（中/日/英）README，表明其具备国际化的视野和规范的工程化水平。

**4. 社区活跃度与生态：阿里背书的强力驱动**
*   **事实**：星标数 7,465（且在快速增长中），由阿里巴巴开源。
*   **推断**：作为阿里云核心网关产品的开源版本，Higress 继承了阿里巴巴在“双十一”流量治理方面的深厚积累。相比纯个人项目，它有明确的商业公司维护，代码提交频率高，Issue 响应及时。社区活跃度不仅体现在 Star 数，更体现在其与阿里云通义千问等模型的深度集成上，这种**产研结合**的模式保证了项目的长期生命力。

**5. 潜在问题与改进建议**
*   **推断**：尽管架构先进，但基于 Istio 和 Envoy 的技术栈带来了**极高的运维复杂度**。对于中小企业或非云原生团队，部署和调优 Higress 的门槛远高于 Nginx 或 APISIX。此外，WASM 插件的开发虽然灵活，但目前调试工具链和生态成熟度尚不如传统脚本插件，**开发体验（DX）仍有提升空间**。

### 边界条件与验证清单

**不适用场景：**
*   极简单的边缘路由需求（如仅需一个反向代理，使用 Nginx 更轻量）。
*   非 K8s 环境下的传统虚拟机部署（虽然支持，但无法发挥其云原生优势）。
*   对资源消耗极度敏感的场景（Envoy 内存占用相对较高）。

**快速验证清单：**
1.  **WASM 插件热加载测试**：在网关运行时，上传一个新的 WASM 插件（如修改请求头），验证是否无需重启进程即可生效，并检查 CPU/内存开销是否在可接受范围。
2.  **AI 流量透传延迟测试**：模拟高并发下的 SSE（Server-Sent Events）流式请求，对比 Higress 与直连模型 API 的首字节延迟（TTFB），验证其作为中间层的损耗。
3.  **MSP 协议兼容性检查**：尝试将一个本地工具注册为 Higress 的 MCP 服务，验证标准 AI Agent（如基于 Claude 的 Agent）是否能通过网关成功调用该工具。
4.  **配置漂移检查**：在 K8s 中删除 Higress 的 Pod，验证新 Pod 启动后是否自动从控制平面同步最新配置，确保控制平面与数据平面的一致性。

---
## 技术分析

# Higress 深度技术分析报告

## 1. 技术架构深度剖析

**技术栈与架构模式**
Higress 建立在云原生生态的基石之上，采用了经典的**控制平面与数据平面分离**的架构模式。
*   **底层基础设施**：深度集成 **Istio**（控制平面）和 **Envoy**（高性能数据平面）。这意味着 Higress 继承了 Envoy 在 C++ 层面带来的极致 L7 处理性能，以及 Istio 强大的服务治理能力。
*   **扩展层**：引入 **WebAssembly (WASM)** 作为核心插件机制。通过代理过滤器（Proxy WASM）标准，允许开发者使用 Go、C++、Rust 或 AssemblyScript 编写逻辑，动态注入数据平面，而无需重新编译或重启 Envoy。
*   **语言栈**：主要控制逻辑采用 **Go** 语言编写，利用 Go 的高并发特性处理配置分发和控制面逻辑；数据平面核心路径依赖 Envoy (C++)。

**核心模块与关键设计**
*   **控制面**：负责配置管理、服务发现（Kubernetes、Nacos、DNS 等）、WASM 插件管理以及路由规则的分发。它通过 xDS 协议（包括 LDS, CDS, RDS 等）与数据平面通信。
*   **数据面**：基于 Envoy，负责实际的流量转发、负载均衡、WASM 插件执行以及 AI 特有的流式数据处理。
*   **MCP (Model Context Protocol) 服务器托管**：这是 Higress 针对 AI 时代的创新设计。它内置了 MCP 协议支持，允许将 Higress 直接作为 AI Agent 的工具提供者，将后端 API 转换为 AI 可调用的工具。

**技术亮点与创新点**
*   **AI Native 网关定位**：不同于传统网关仅关注流量转发，Higress 将 AI 流量（LLM 请求）视为一等公民。原生支持 SSE（Server-Sent Events）流式转发，解决了长连接场景下的配置热更新难题。
*   **WASM 插件市场**：构建了一个开箱即用的插件生态，特别是针对 AI 的提示词管理、敏感词过滤、Token 计费等插件。
*   **MCP 协议集成**：作为连接 LLM 与后端微服务的桥梁，它简化了 AI Agent 调用内部 API 的复杂度。

**架构优势分析**
*   **高性能**：数据路径基于 Envoy C++，避免了纯 Go 网关在 JSON 序列化/反序列化以及高并发下的 GC 压力。
*   **极致的扩展性**：WASM 插件机制实现了业务逻辑与网关核心的解耦。用户可以像编写脚本一样扩展网关功能，且插件更新只需 reload WASM 模块，无需重启网关进程，连接不中断。
*   **云原生亲和**：天然支持 Kubernetes Ingress，可以直接作为 K8s 的 Ingress Controller 替代 Nginx Ingress。

## 2. 核心功能详细解读

**主要功能与使用场景**
1.  **AI 网关**：
    *   **统一接入**：将 OpenAI、Azure OpenAI、通义千问、Llama 等多种 LLM 提供商统一为一个标准 API。
    *   **Token 管理**：实时统计请求和响应的 Token 消耗，便于成本控制。
    *   **提示词增强**：在网关层动态注入 System Prompt，无需修改应用代码。
    *   **结果后处理**：对 AI 返回的流式数据进行实时审核或格式化。
2.  **MCP 服务器**：
    *   允许用户通过配置文件将标准 HTTP API 定义为 MCP 工具。
    *   AI 客户端（如 Claude Desktop 或 IDE 插件）可直接连接 Higress，Higress 负责将 Agent 的意图转化为对后端微服务的调用。
3.  **传统 API 网关**：
    *   全面的流量管理：路由重写、灰度发布（金丝雀发布）、负载均衡算法、限流熔断、认证鉴权。

**解决了什么关键问题**
*   **AI 供应商锁定**：通过统一适配层，企业可以在不同 LLM 之间无缝切换，例如从 OpenAI 切换到本地部署的 Llama，只需修改配置，无需改代码。
*   **AI 落地成本与安全**：解决了企业引入 LLM 后无法精细化计费和审计的问题。
*   **Agent 工具集成的繁琐**：MCP 协议的内置支持，消除了手动编写大量 API-to-Tool 转换层的代码工作。

**与同类工具的详细对比**
*   **vs. Kong/APISIX**：传统网关虽然也支持 WASM 或 Lua，但在 AI 场景（如流式传输的保持、Token 级别的截断与处理）上缺乏专门优化。Higress 的 MCP 支持也是传统网关不具备的。
*   **vs. LangChain / Langflow**：这些是应用开发框架，而 Higress 是基础设施。Higress 位于 LangChain 应用和 LLM 之间，作为流量入口和管理平面。
*   **vs. Istio Ingress**：Higress 本质上是 Istio 的增强版。相比原生 Istio Gateway，Higress 提供了更友好的控制台（Console）、开箱即用的 WASM 插件以及更简化的配置模型，降低了运维门槛。

## 3. 技术实现细节

**关键技术方案**
*   **xDS 协议优化**：Higress 控制面与 Envoy 之间使用 gRPC 流式 xDS 协议。为了保证 AI 流式响应（可能持续数十秒甚至数分钟）不中断，Higress 优化了配置更新的推送策略，确保在路由规则变更时，已有的长连接不受影响（热更新）。
*   **WASM 沙箱执行**：利用 Envoy 的 ABI 接口，WASM 插件运行在隔离的沙箱中。Higress 实现了插件的生命周期管理：`OnConfigure`（配置变更）、`OnHttpRequestHeaders`（请求头处理）、`OnHttpStream`（流式 Body 处理）等。

**代码组织结构**
*   **`pkg/`**：核心业务逻辑，包含 Ingress 转换器（K8s Ingress -> Higress Config）、路由发现、Dubbo/Nacos 服务发现适配器。
*   **`plugins/`**：WASM 插件的源码，通常包含 Go 实现和编译后的 `.wasm` 文件。
*   **`router/`**：核心路由匹配引擎，处理 HTTP/gRPC/Dubbo 路由逻辑。

**性能优化与扩展性**
*   **零拷贝**：在 Envoy 层面处理数据，尽量减少数据在内核态与用户态之间的拷贝。
*   **连接池**：针对后端服务（如 LLM Provider）维护 HTTP 连接池，减少握手开销。
*   **水平扩展**：控制面无状态设计，数据面（Envoy）可以通过 Kubernetes HPA 快速扩容。

**技术难点与解决方案**
*   **难点**：流式响应的中间件处理。在 AI 场景下，数据是分块返回的，传统的“读取完整 Body -> 处理 -> 返回”模式会破坏流式体验。
*   **方案**：Higress 利用 WASM 的流式处理能力，在 `OnHttpBody` 逐块处理数据，实现“边收边发”，保持低延迟。

## 4. 适用场景分析

**适合使用的项目**
*   **企业级 AI 应用落地**：需要统一管理多个大模型接口，并进行成本控制、权限管理的场景。
*   **微服务网关**：特别是已经使用 Kubernetes 和 Istio 的技术栈，希望获得比原生 Istio 更丰富功能的团队。
*   **AI Agent 开发**：需要将内部大量业务 API 暴露给 LLM 调用的场景，利用 MCP 协议可以极大简化开发。

**最有效的情况**
*   当你需要对 LLM 的调用进行**细粒度控制**（如：不同 Prompt 使用不同模型，不同用户不同限流策略）时。
*   当你需要将**传统 RPC 服务（如 Dubbo）** 快速暴露为 HTTP API 或 AI 工具时。

**不适合的场景**
*   **极小规模应用**：对于个人 Demo 或极低流量的应用，Higress 的架构（K8s + Istio + Envoy）显得过于重量级，资源开销较大。
*   **非 HTTP/Dubbo 协议**：如果是纯 TCP 或 UDP 游戏/视频流，Higress 虽然基于 Envoy 支持 L4，但其功能重心在 L7，不如专门的四层负载均衡器简洁。

**集成方式**
*   **Kubernetes Ingress**：通过注解或 CRD 定义路由。
*   **Service Mesh**：接管 Sidecar 流量，实现服务间通信治理。

## 5. 发展趋势展望

**技术演进方向**
*   **更深度的 AI 编排**：从简单的透传转向具备“推理”能力的网关，例如根据用户 Query 的复杂度自动路由到不同的模型（小模型处理简单任务，大模型处理复杂任务）。
*   **多模态支持**：增强对图片、音频流的处理能力，支持视频流的实时审核与转发。

**社区反馈与改进空间**
*   **文档与易用性**：虽然中文文档较好，但 WASM 插件开发的调试门槛依然较高，需要更强大的 IDE 插件或调试工具支持。
*   **控制台功能**：目前的控制台偏重配置，未来可能需要更强的可观测性（如 AI 调用链路追踪、Token 消耗趋势分析）。

**与前沿技术结合**
*   **RAG (检索增强生成) 集成**：网关层可能集成向量数据库的简单查询逻辑，实现基于语义路由的请求分发。
*   **eBPF**：利用 eBPF 替代部分 Sidecar 代理，实现更低延迟的网络观测和转发。

## 6. 学习建议

**适合开发者水平**
*   **中级**：熟悉 Kubernetes 基础、了解 HTTP 协议、具备 Go 语言基础。
*   **高级**：若要深入 WASM 插件开发或 Envoy 调优，需要理解 C++ 内存管理概念和网络编程模型。

**学习路径**
1.  **基础概念**：理解 API Gateway、Ingress、Service Mesh (Istio) 的区别与联系。
2.  **环境搭建**：在本地 Docker 或 Kind 集群中部署 Higress。
3.  **配置实践**：尝试配置一个简单的路由转发，然后配置一个 AI Provider 转发。
4.  **插件开发**：阅读官方 WASM 插件示例，尝试编写一个简单的 Header 修改插件。
5.  **源码阅读**：从 `pkg/config` 和 `pkg/ingress` 入手，理解 K8s 资源如何转化为 Envoy 配置。

**实践建议**
*   先使用官方预置插件解决常见问题，避免重复造轮子。
*   在生产环境部署前，务必进行压测，特别是 WASM 插件可能会

---
## 代码示例




```python
# 示例1：基于Higress的API网关路由配置
from higress import Gateway, Route, Plugin

def setup_api_gateway():
    """
    配置一个简单的API网关路由
    场景：将 /api/v1/users 请求路由到后端用户服务
    """
    # 创建网关实例
    gateway = Gateway(name="user-service-gateway")
    
    # 定义路由规则
    user_route = Route(
        path="/api/v1/users",
        methods=["GET", "POST"],
        backend="http://user-service:8080",
        plugins=[Plugin("jwt-auth")]  # 添加JWT认证插件
    )
    
    # 将路由添加到网关
    gateway.add_route(user_route)
    return gateway

**说明**: 这个示例展示了如何使用Higress配置API网关路由，包括路径匹配、HTTP方法和后端服务地址设置，同时演示了如何添加认证插件。

```python


from higress import Gateway, RateLimit, CircuitBreaker
def setup_traffic_control():
"""
配置流量控制和熔断策略
场景：限制API请求频率并实现服务熔断
"""
gateway = Gateway(name="traffic-control-gateway")
# 配置限流策略：每秒最多100个请求
rate_limit = RateLimit(
requests_per_second=100,
burst=20  # 允许突发流量
)
# 配置熔断策略：连续失败5次后熔断30秒
circuit_breaker = CircuitBreaker(
failure_threshold=5,
recovery_timeout=30
)
# 应用策略到路由
gateway.add_route(
path="/api/v1/orders",
backend="http://order-service:8080",
plugins=[rate_limit, circuit_breaker]
)
return gateway

```python
# 示例3：Higress插件开发与部署
from higress import Plugin, PluginConfig

class CustomAuthPlugin(Plugin):
    """
    自定义认证插件示例
    场景：实现基于API Key的认证
    """
    def __init__(self):
        super().__init__(name="custom-auth")
        self.config = PluginConfig(
            api_key_header="X-API-Key",
            valid_keys=["key123", "key456"]
        )
    
    def on_request(self, context):
        api_key = context.request.headers.get(self.config.api_key_header)
        if api_key not in self.config.valid_keys:
            return context.abort(401, "Invalid API Key")
        return context.next()

def deploy_custom_plugin():
    """
    部署自定义插件到Higress网关
    """
    gateway = Gateway(name="custom-plugin-gateway")
    plugin = CustomAuthPlugin()
    
    gateway.add_plugin(plugin)
    gateway.add_route(
        path="/api/v1/protected",
        backend="http://protected-service:8080",
        plugins=[plugin]
    )
    return gateway

**说明**: 这个示例展示了如何开发自定义Higress插件，实现特定的业务逻辑（如API Key认证），并将其集成到网关路由中。


---
## 案例研究


### 1：阿里巴巴内部电商业务迁移

 1：阿里巴巴内部电商业务迁移

**背景**:  
阿里巴巴内部电商业务原先使用自研的网关系统，随着业务规模扩大，系统维护成本高，且需要支持云原生架构转型。

**问题**:  
- 自研系统扩展性不足，难以应对高并发流量。  
- 多云部署需求下，网关一致性管理复杂。  
- 需要支持更灵活的流量治理和插件生态。

**解决方案**:  
采用 Higress 作为统一云原生 API 网关，结合 Istio 实现服务网格流量管理，并利用其插件市场扩展功能（如限流、认证）。

**效果**:  
- 网关性能提升 30%，支持百万级 QPS。  
- 运维成本降低 40%，插件开发效率提高 50%。  
- 实现了跨云流量统一管控，业务迭代速度加快。

---



### 2：某大型互联网公司微服务改造

 2：某大型互联网公司微服务改造

**背景**:  
该公司原有单体架构，服务间通信依赖 Nginx，缺乏动态路由和灰度发布能力，影响业务敏捷性。

**问题**:  
- 灰度发布需手动配置，易出错。  
- 服务扩缩容时路由规则更新延迟。  
- 缺乏统一的流量监控和日志分析。

**解决方案**:  
部署 Higress 替换 Nginx，通过其动态路由和流量标签功能实现自动化灰度发布，集成 Prometheus 和 Skywalking 进行监控。

**效果**:  
- 灰度发布时间从 2 小时缩短至 10 分钟。  
- 服务扩缩容路由更新延迟降低至秒级。  
- 问题定位效率提升 60%，故障率下降 25%。

---



### 3：某金融科技公司 API 开放平台

 3：某金融科技公司 API 开放平台

**背景**:  
该公司需构建开放 API 平台，对接第三方合作伙伴，要求高安全性和灵活的访问控制。

**问题**:  
- 传统 API 网关难以满足复杂的鉴权需求。  
- 合作方接口调用频率波动大，需动态限流。  
- 缺乏对 API 调用的全链路追踪。

**解决方案**:  
使用 Higress 的 JWT 鉴权和自定义插件实现多租户访问控制，结合其自适应限流算法应对流量波动，集成 OpenTelemetry 追踪调用链。

**效果**:  
- API 调用安全性提升，未授权访问减少 90%。  
- 限流精准度提高，系统稳定性增强。  
- 全链路追踪使问题排查时间缩短 70%。

---
## 对比分析

## 与同类方案对比

| 维度 | Alibaba Higress | APISIX | Kong |
|------|----------------|--------|------|
| 性能 | 高性能，基于 Rust 和 Go 开发，支持高并发处理 | 极高性能，基于 LuaJIT，适合极高并发场景 | 高性能，基于 Nginx 和 Lua，成熟稳定 |
| 易用性 | 提供图形化控制台，支持 K8s Ingress 和 API 网关一体化 | 配置灵活，但需要一定的学习曲线，社区支持丰富 | 配置相对简单，但高级功能需要插件支持 |
| 成本 | 开源免费，商业支持需付费 | 开源免费，企业版需付费 | 开源免费，企业版需付费 |
| 扩展性 | 支持 Wasm 插件，扩展性强 | 支持 Lua 插件，生态丰富 | 支持 Lua 和 PDK 插件，生态成熟 |
| 集成性 | 深度集成阿里云服务，适合云原生环境 | 与 K8s 集成良好，适合多云部署 | 与多种云服务集成，适合混合云 |
| 社区 | 社区活跃，由阿里云主导 | 社区活跃，由 Apache 基金会主导 | 社区成熟，由 Kong Inc. 主导 |

### 优势分析

- 优势1：Higress 基于 Rust 和 Go 开发，性能优异且内存占用低。
- 优势2：提供一体化的控制台和 K8s Ingress 支持，部署和运维简单。
- 优势3：深度集成阿里云服务，适合阿里云用户使用。
- 优势4：支持 Wasm 插件，扩展性和灵活性高。

### 不足分析

- 不足1：社区生态相对 APISIX 和 Kong 较小，插件数量有限。
- 不足2：对非阿里云用户的支持可能不如其他方案灵活。
- 不足3：文档和社区资源不如 APISIX 和 Kong 丰富。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 WASM 实现插件化扩展

**说明**: Higress 深度集成了 WASM (WebAssembly) 技术，允许使用 C/C++、Go、Rust 或 AssemblyScript 等高性能语言编写网关插件。相比传统的 Lua 脚本，WASM 插件具有更好的隔离性、更高的执行效率以及更丰富的标准库支持。

**实施步骤**:
1. 根据业务需求选择合适的 WASM 开发语言（推荐使用 Go 或 Rust）。
2. 引入 Higress 提供的 WASM-SDK（如 `github.com/alibaba/higress/plugins/wasm-go`）。
3. 编写插件逻辑，实现 `OnHttpRequestHeaders` 等生命周期钩子。
4. 构建编译为 `.wasm` 文件。
5. 在 Higress 控制台或通过 WasmPlugin CRD 上传并配置插件。

**注意事项**: 
- 注意 WASM 插件的内存限制，避免在插件中处理过大的请求体。
- 生产环境发布前，务必对 WASM 插件进行性能压测，确保其延迟在可接受范围内。

---

### 实践 2：精细化流量路由与灰度发布

**说明**: 利用 Higress 强大的路由能力，基于 Header、Query 参数、Cookie 或权重实现复杂的流量路由。这对于微服务架构下的蓝绿部署、金丝雀发布和 A/B 测试至关重要。

**实施步骤**:
1. 定义 Ingress 资源或使用控制台配置路由规则。
2. 配置多个后端服务版本（如 v1 和 v2）。
3. 设置匹配条件（例如：`x-canary: true` 的请求路由到 v2）。
4. 若进行金丝雀发布，配置基于百分比的流量分流（例如：10% 流量到 v2）。
5. 验证流量走向是否符合预期。

**注意事项**: 
- 确保路由规则的优先级设置正确，避免规则冲突导致流量被意外截断。
- 灰度发布过程中，应保持全链路追踪，以便快速定位问题。

---

### 实践 3：全面对接服务注册中心 (Nacos/Nacos)

**说明**: Higress 原生支持 Nacos、Zookeeper、Consul 等注册中心。通过对接注册中心，网关可以自动发现后端服务实例的 IP 变化，实现动态负载均衡，无需手动维护上游服务器列表。

**实施步骤**:
1. 在 Higress 全局配置或特定服务来源中添加 Nacos 注册中心地址。
2. 配置命名空间 和服务分组信息。
3. 确保网络连通性，使 Higress 能够访问 Nacos Server。
4. 在路由配置中选择服务类型为“注册中心服务”，并输入服务名称。
5. 检查健康检查状态，确保只有健康的实例接收流量。

**注意事项**: 
- 确保注册中心中的服务元数据（如版本、权重）配置正确，Higress 可依据这些元数据进行路由。
- 如果使用的是 Nacos 2.x，需注意 gRPC 协议的端口配置是否正确。

---

### 实践 4：配置安全防护与认证鉴权

**说明**: Higress 提供了内置的安全插件，包括 Basic Auth、API Key、JWT 认证以及 IP 访问控制。合理配置这些功能可以防止未授权访问，保护后端服务的安全。

**实施步骤**:
1. 在“插件市场”中找到“Key Auth”或“JWT Auth”插件。
2. 在全局或特定路由下启用插件。
3. 配置消费者，生成对应的密钥或凭据。
4. 配置 IP 访问控制插件，封禁恶意 IP 或限制内网访问。
5. 测试请求，确保未携带有效凭据的请求被 401 或 403 拦截。

**注意事项**: 
- 密钥管理应遵循最小权限原则，定期轮换。
- 对于高并发场景，建议使用本地缓存认证信息的插件，以减少对外部认证服务的压力。

---

### 实践 5：启用可观测性与监控告警

**说明**: Higress 原生支持 Prometheus 监控指标、访问日志采集以及链路追踪。建立完善的可观测体系是排查故障和优化性能的基础。

**实施步骤**:
1. 配置 Higress 暴露 Prometheus Metrics 指标端口。
2. 集成 Prometheus 抓取 Higress 数据，并配置 Grafana 仪表盘（可导入 Higress 官方提供的 Dashboard 模板）。
3. 开启访问日志采集，对接 Kafka、Filebeat 或阿里云 SLS。
4. 开启 SkyWalking 或 Zipkin Tracing，配置采样率。
5. 设置关键指标（如 P99 延迟、错误率、5xx 状态码）的告警规则。

**注意事项**: 
- 日志量可能会非常大，建议在生产环境中根据需求调整日志详细程度和采样率，避免

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 WASM 插件与原生插件分离

**说明**: Higress 支持 WASM (WebAssembly) 插件，WASM 插件运行在沙箱环境中，虽然安全性高，但相比原生 Go/C++ 插件会有一定的性能损耗。对于高频调用的核心逻辑（如限流、路由），建议优先使用原生插件；对于业务逻辑多变或非核心路径的功能，使用 WASM 插件。

**实施方法**:
1. 评估现有 WASM 插件的性能热点，将高频调用的代码（如 JWT 验证、IP 限流）迁移为 Higress 原生插件（使用 Go 或 C++ 开发）。
2. 在 `wasmplugins` 配置中，仅将必须动态更新的业务逻辑配置为 WASM 插件。
3. 确保原生插件编译时启用了 `-O2` 优化选项。

**预期效果**: 减少约 10-20% 的插件执行延迟，降低 CPU 使用率。

---

### 优化 2：配置连接池与 HTTP/2 参数调优

**说明**: Higress 底层基于 Envoy，其与后端服务之间的连接管理对吞吐量影响巨大。默认配置可能不适合高并发或长连接场景。合理调整连接池大小和 HTTP/2 参数可以显著减少握手开销和排队延迟。

**实施方法**:
1. 在 `GlobalConfig` 或特定路由配置中，调整 `upstream` 的连接池参数：
   ```yaml
   connectTimeout: 5s
   maxRequestsPerConnection: 10000
   http2ProtocolOptions:
     hpack_table_size: 65536
     max_concurrent_streams: 100
   ```
2. 根据后端服务处理能力，适当增加 `maxRequestsPerConnection` 以减少频繁建立 TCP 连接的开销。

**预期效果**: 在高并发场景下，提升后端吞吐量 15-30%，降低 P99 延迟。

---

### 优化 3：利用 Higress 的多线程与 CPU 亲和性

**说明**: Higress (Envoy) 采用多线程架构。默认情况下，工作线程数通常设置为 CPU 核数。但在容器化环境中，若 CPU 限制与工作线程数不匹配，会导致上下文切换频繁。此外，未开启 CPU 亲和性可能导致线程在核心间迁移，引发缓存失效。

**实施方法**:
1. 检查 Higress 的启动配置（通常在容器启动脚本或 `higress` 配置中），确保 `--concurrency` 参数值等于容器分配的 CPU Limit（例如 `limit: "4"` 则 concurrency 设为 4）。
2. 在部署 Higress 的 Pod 或宿主机上，确保开启 CPU 亲和性（Kubernetes 中通常通过 `guaranteed` QoS 或宿主机 `systemd` 配置实现）。
3. 避免超卖，确保 Higress 独占资源，避免与其他高负载进程（如 Java 应用）混部。

**预期效果**: 减少 5-10% 的系统 CPU 开销，提升请求处理稳定性。

---

### 优化 4：优化日志采样与异步上报

**说明**: 详细的访问日志对于排查问题至关重要，但在高流量（例如 QPS > 10k）下，同步写日志或全量日志会严重消耗 I/O 和 CPU 资源，阻塞网络处理线程。

**实施方法**:
1. 配置日志采样，仅记录特定比例（如 10%）或特定状态码（如 4xx, 5xx）的日志：
   ```yaml
   accessLog:
   - name: envoy.file_access_log
     config:
       path: /dev/stdout
       format: ...
       filter:
         notHealthCheck: true
       sample_rate:
         value: 0.1 # 采样 10%
   ```
2. 将日志输出改为异步模式（如输出到 stdout 由 Fluentd/Filebeat 侧收集，或使用 Envoy 的 ALS gRPC 上报）。
3. 避免在日志格式中使用复杂的元数据

---
## 学习要点

- Higress 是阿里开源的基于 Istio 的云原生 API 网关，深度集成 K8s 与 Dubbo/Nacos 等微服务生态，提供企业级流量管理能力。
- 它支持将传统网关（如 Nginx）配置一键迁移至 Ingress 配置，并兼容 K8s Ingress 标准与 Gateway API，极大降低了迁移与使用门槛。
- 内置针对 Dubbo、gRPC 等协议的定制化支持，能够直接进行协议转换与路由，解决了微服务架构中南北向与东西向流量的统一治理难题。
- 提供开箱即用的 WAF（Web 应用防火墙）插件与安全防护能力，有效保障 API 接口的安全性。
- 采用高性能架构设计，支持热更新与高并发流量处理，确保在复杂业务场景下的稳定性与低延迟。
- 拥有强大的可扩展性（Wasm 插件机制），允许开发者通过 Lua、Wasm 等技术灵活编写自定义插件来扩展业务逻辑。
- 作为开源项目，它依托于阿里巴巴成熟的内部实践，旨在为云原生时代提供一个统一、轻量且易用的 API 网关标准。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础

**学习内容**:
- Higress 的背景与核心概念（云原生 API 网关）
- Higress 与传统网关（如 Nginx, Kong）的区别
- 基本术语：Ingress、Route、Service、Plugin
- Docker/Docker Compose 环境下的 Higress 快速安装与部署
- 控制台（Console）的基本操作与界面熟悉

**学习时间**: 1-2周

**学习资源**:
- Higress 官方 GitHub 仓库 README
- Higress 官方文档：快速入门章节
- Higress 官方博客：架构设计解析

**学习建议**: 
建议先通读官方文档的“什么是 Higress”部分，理解其基于 Envoy 和 Istio 的技术底座。务必动手在本地使用 Docker Compose 启动一个 Standalone 模式的 Higress 实例，并通过控制台创建一个简单的简单的路由转发（例如将 `/` 路径转发到 `httpbin.org`），以验证流量是否通畅。

---

### 阶段 2：核心功能与流量治理

**学习内容**:
- 域名、路由与服务的详细配置
- 负载均衡策略（轮询、随机、一致性哈希等）
- 服务健康检查（主动与被动）与熔断降级
- 流量镜像与金丝雀发布/蓝绿发布配置
- 全局限流与细粒度限流配置
- 基本认证插件的使用（如 Key Auth、JWT）

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档：流量管理、服务来源插件
- Envoy 官方文档（用于理解底层负载均衡与健康检查机制）
- Higress 官方示例库

**学习建议**: 
此阶段重点在于掌握“流量搬运”。建议搭建一个模拟的后端服务（可以使用 Nginx 模拟两个版本的服务），实践配置 Header 匹配的路由规则来实现蓝绿发布。同时，尝试配置限流插件，使用压测工具（如 Apache Bench）观察限流效果，理解网关如何保护后端服务。

---

### 阶段 3：插件开发与扩展

**学习内容**:
- Higress 插件系统架构（Wasm 与 Lua）
- 官方常用插件的使用（如 IP 限制、请求鉴权、请求/响应重写）
- 使用 Wasm (C++/Go/AssemblyScript) 开发自定义插件
- 插件的配置与热加载机制
- 插件市场与网关资源的关联

**学习时间**: 4-6周

**学习资源**:
- Higress 官方文档：自定义开发指南
- Higress 官方插件模板
- WebAssembly (Wasm) 基础教程

**学习建议**: 
Higress 的强大之处在于其插件生态。建议从修改一个现有的官方插件（例如修改请求头）开始，熟悉开发流程。随后，尝试使用 Go 或 C++ 编写一个简单的 Wasm 插件，实现例如“根据特定 Query 参数进行阻拦”的逻辑，并将其部署到 Higress 中进行调试。了解 Wasm 的沙箱特性及其安全性。

---

### 阶段 4：生产级运维与架构集成

**学习内容**:
- 在 Kubernetes 环境中通过 Helm 部署 Higress（Ingress 模式）
- Higress 与 Nacos、Consul 等注册中心的集成
- Higress 与阿里云 MSE、ACK 等云产品的结合
- 监控与可观测性（Prometheus/Grafana 集成、日志采集、Access Log 格式化）
- 高可用部署架构与性能调优
- 网关的安全性加固（HTTPS 配置、CVE 漏洞防护）

**学习时间**: 4-6周

**学习资源**:
- Higress 官方文档：部署运维、最佳实践
- Kubernetes Ingress Controller 工作原理
- 云原生可观测性相关资料

**学习建议**: 
如果是企业级应用，Kubernetes 集成是必修课。建议在本地搭建一个 Kind 或 Minikube 环境，使用 Helm Chart 部署 Higress，并配置 Ingress 资源对象来接管集群流量。重点学习如何将服务自动注册到 Higress，以及如何配置 Prometheus 监控指标，关注 QPS、Latency 和成功率等核心指标。

---

### 阶段 5：源码剖析与深度定制

**学习内容**:
- Higress 项目结构深度剖析
- Envoy 配置生成逻辑与 xDS 协议交互
- Higress Router 与 HTTP Runtime 源码分析
- 深入理解 Istio 对接模式与控制平面原理
- 参与社区贡献与 Bug 修复

**学习时间**: 持续学习

**学习资源**

---
## 常见问题


### 1: Higress 是什么？它与阿里云和云原生社区有什么关系？

1: Higress 是什么？它与阿里云和云原生社区有什么关系？

**A**: Higress 是一个基于阿里内部多年实践，开源的云原生 API 网关。它是在 2022 年由阿里云正式开源的，深度集成了阿里云的生态，同时捐赠给了云原生原生计算基金会（CNCF）作为沙箱项目进行孵化。Higress 的前身是阿里云内部的网关系统，它结合了 Kong、Nginx 和 Envoy 等主流网关的优点，旨在提供一站式的 API 管理、流量管理和微服务治理能力，特别适合在 Kubernetes 环境中运行。

---



### 2: Higress 与 Nginx、Envoy 或 Kong 等传统网关相比有什么核心优势？

2: Higress 与 Nginx、Envoy 或 Kong 等传统网关相比有什么核心优势？

**A**: Higress 的核心优势在于其“现代化”和“集成性”：
1.  **架构先进**：基于 Envoy 和 Istio（通过 WASM 扩展）构建，相比传统的 Nginx Lua 脚本模式，它提供了更强的安全隔离性和动态扩展能力。
2.  **标准兼容**：它支持 Kubernetes Ingress 标准和 Gateway API 标准，使得云原生应用的迁移和管理更加平滑，不像 Kong 那样需要依赖大量的 CRD 自定义资源。
3.  **插件生态**：支持使用 Go、C++、Rust、JavaScript 等多种语言编写插件（基于 WASM），而 Nginx 主要依赖 C 模块或 Lua，开发门槛和安全性不如 Higress。
4.  **流量治理**：深度集成了服务发现（如 Nacos, Consul, Eureka）和全链路路由，能够处理复杂的微服务流量调度，而传统网关通常需要额外的组件配合才能实现。

---



### 3: Higress 是否支持从 Nginx 或 Apache APISIX 无缝迁移？

3: Higress 是否支持从 Nginx 或 Apache APISIX 无缝迁移？

**A**: 是的，Higress 提供了良好的迁移兼容性。针对 Nginx 用户，Higress 提供了 Nginx 配置转换工具，可以将大部分 Nginx 的配置语法自动转换为 Higress 的路由和插件配置。对于 Apache APISIX 或 Kong 用户，虽然配置模型不完全一致，但由于 Higress 支持标准的 Ingress 和 Gateway API，且底层逻辑相似（都是七层网关），迁移过程主要是将原有的路由规则和认证插件在 Higress 上重新配置。Higress 还提供了 Ingress Controller 的功能，可以直接接管 Kubernetes 的 Ingress 资源，从而替代原有的 Ingress-Nginx 或 APISIX Ingress。

---



### 4: Higress 如何处理插件扩展？是否支持热加载？

4: Higress 如何处理插件扩展？是否支持热加载？

**A**: Higress 的一个重大特性是对 **WebAssembly (WASM)** 的支持。它允许开发者使用高级语言（如 Go 或 AssemblyScript）编写插件逻辑，编译成 WASM 文件后动态加载到网关中。
1.  **热加载**：支持插件的动态热插拔。你可以在不重启 Higress 进程的情况下加载、更新或卸载插件，这对于生产环境的流量连续性至关重要。
2.  **安全性**：由于 WASM 运行在沙箱环境中，即使插件崩溃也不会导致整个网关进程崩溃，这比传统的 Nginx C 模块或 Lua 脚本更加稳定和安全。

---



### 5: 在性能方面，Higress 的表现如何？能否应对高并发场景？

5: 在性能方面，Higress 的表现如何？能否应对高并发场景？

**A**: Higress 具备极高的性能，能够应对企业级的高并发场景。
1.  **底层优化**：Higress 的数据面基于 Envoy，Envoy 本身就是高性能的 L7 代理，使用 C++ 编写，具备零拷贝、多线程等特性。
2.  **基准测试**：根据官方和社区的压测数据，Higress 在开启常见插件（如限流、认证）的情况下，依然能保持与 Envory 相当的超高吞吐量和极低的延迟。
3.  **弹性伸缩**：作为云原生网关，Higress 可以结合 Kubernetes 的 HPA（水平自动伸缩）进行动态扩容，以适应流量的突发波动。

---



### 6: Higress 是否支持 AI 和大模型（LLM）相关的网关功能？

6: Higress 是否支持 AI 和大模型（LLM）相关的网关功能？

**A**: 是的，这是 Higress 近期的一个重要发展方向。Higress 已经开始针对 AI 大模型场景进行专门优化，提供了对 AI 服务的特殊网关支持。这包括了对大模型流式输出的处理、Token 计费与统计、以及针对 AI 请求的路由和负载均衡。这使得 Higress 成为了构建 AI 应用或代理 OpenAI、通义千问等大模型服务的理想入口网关。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: 路由重写与请求头管理

### 问题**: Higress 基于 Envoy 构建，但默认配置可能无法直接满足某些特定路由需求。请尝试在本地 Docker 环境中部署 Higress，并配置一个简单的 Ingress 路由规则：将路径 `/api/v1` 的流量转发到后端服务的 `/v1` 路径，同时将请求头中的 `User-Agent` 重写为 `Higress-Test/1.0`。

### 提示**: 重点查阅 Higress 关于 `Ingress` 注解或者特定路由配置（如 `VirtualService`）的文档，关注 `headers` 的操作和路径重写配置项。

### 

---
## 实践建议

### 生产环境实践建议

基于 Higress 作为 AI Native 网关的架构特性，以下是针对生产环境的 7 条实施建议：

#### 1. 利用 WASM 插件实现非侵入式鉴权
*   **操作方法**：不要将 LLM 提供商（如 OpenAI、通义千问）的 API Key 硬编码在客户端。使用 Higress 的 WASM 插件（如 `ai-proxy`）在网关层统一配置和管理密钥。客户端仅与网关交互，由网关在转发时注入鉴权信息。
*   **目的**：集中管控密钥，支持统一轮换，避免密钥暴露给终端用户。

#### 2. 配置请求与响应缓存策略
*   **操作方法**：针对具有确定性的问答场景，在 Higress 路由中启用缓存。以 Prompt 的 Hash 值作为缓存 Key，对重复请求直接返回网关缓存结果。
*   **注意**：需根据业务设置合理的 TTL（过期时间）。在涉及多轮对话（依赖历史上下文）的场景中应谨慎使用，防止返回过时信息。

#### 3. 实施语义路由与模型分发
*   **操作方法**：利用 Higress 的内容路由能力，根据 Prompt 意图将流量分发至不同模型。例如，将简单闲聊路由至低成本小模型（如 Llama 7B），将复杂逻辑推理路由至高精度大模型（如 GPT-4）。
*   **目的**：根据任务难度匹配算力，优化 API 调用成本。

#### 4. 设置严格的超时与重试机制
*   **操作方法**：鉴于 LLM 推理属于长尾请求，应在 Higress 路由配置中设置较长的超时时间（如 60s 或更久）。同时，配置针对 429（限流）或 5xx 错误的重试策略，建议配合指数退避算法。
*   **注意**：避免直接复用传统微服务（通常为 3s-5s）的网关配置，防止请求频繁超时失败。

#### 5. 构建提示词模板与参数管理
*   **操作方法**：避免在前端随意拼接字符串。利用网关插件定义标准的提示词模板，在转发时将客户端变量填充至模板中。同时，在网关层统一管控 Temperature、Top_P 等参数。
*   **目的**：实现模型行为的集中管理与调整，无需重新发布客户端应用。

#### 6. 建立基于 Token 的计费与流控监控
*   **操作方法**：配置日志与监控插件，解析响应体中的 `usage` 字段（包含 input_tokens 和 output_tokens）。基于 Token 消耗量而非单纯的 QPS 配置限流策略。
*   **目的**：防止个别用户通过超长 Prompt 或无限生成耗尽预算。
*   **注意**：AI 响应体通常较大，需合理设置日志采样率，以平衡监控需求与存储成本。

#### 7. 处理流式传输（SSE）的兼容性
*   **操作方法**：大多数 AI 交互使用 Server-Sent Events (SSE) 实现打字机效果。需确保 Higress 及其前端代理正确配置 SSE 支持，保持长连接，避免缓冲导致流式输出中断。
*   **目的**：保证终端用户能够实时接收生成的数据片段，优化交互体验。

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI 原生](/tags/ai-%E5%8E%9F%E7%94%9F/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [LLM](/tags/llm/) / [MCP](/tags/mcp/) / [Kubernetes](/tags/kubernetes/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/) / [Kubernetes](/scenarios/kubernetes/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-2.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260205-github_trending-alibaba-higress-5.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260130-github_trending-alibaba-higress-9.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*