---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-03-07T12:41:04+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "Istio", "Envoy", "LLM", "MCP", "WASM"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "Higress 是阿里巴巴开源的一款**云原生 API 网关**，基于 Istio 和 Envoy 构建，并深度集成了**AI 原生能力**。它采用 Go 语言开发，目前在 GitHub 上拥有超过 7,600 颗星。 以下是 Higress 的核心要点总结： **1. 产品定位** Higress 是一个**AI 原"
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
- **星标**: 7,680 (+17 stars today)
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

Higress 是阿里巴巴开源的基于 Istio 和 Envoy 构建的 AI 原生 API 网关。它专为处理大模型流量与微服务治理而设计，通过 WASM 插件提供了统一的流量入口与 AI 代理工具集成能力。本文将介绍其核心架构、AI 网关特性以及 MCP 系统支持，帮助开发者理解如何利用该系统构建高效的云原生应用网关。

---
## 摘要

Higress 是阿里巴巴开源的一款**云原生 API 网关**，基于 Istio 和 Envoy 构建，并深度集成了**AI 原生能力**。它采用 Go 语言开发，目前在 GitHub 上拥有超过 7,600 颗星。

以下是 Higress 的核心要点总结：

**1. 产品定位**
Higress 是一个**AI 原生 API 网关（AI Native API Gateway）**。它通过扩展 WebAssembly (WASM) 插件能力，将传统的 API 网关功能与 AI 应用的特定需求相结合。

**2. 架构特点**
*   **控制与数据分离：** 架构上分为控制平面（配置管理）和数据平面（流量处理）。
*   **高性能配置：** 配置变更通过 xDS 协议传播，延迟仅为毫秒级，且连接不中断。这使其非常适合处理 AI 流式响应等长连接场景。

**3. 三大核心功能与用途**
*   **AI 网关：**
    *   提供统一 API 接入 30 多家大语言模型（LLM）提供商。
    *   支持协议转换、可观测性、缓存和安全防护。
    *   *核心组件：* `ai-proxy`, `ai-statistics`, `ai-cache`, `ai-security-guard`。
*   **MCP 服务器托管：**
    *   托管模型上下文协议（MCP）服务器，使 AI Agent 能够调用外部工具和服务。
    *   *核心组件：* `mcp-router`, `jsonrpc-converter` 以及内置服务器实现（如地图搜索等工具）。
*   **Kubernetes Ingress：**
    *   作为 K8s 入口控制器，兼容 nginx-ingress 注解，支持微服务路由。

---
## 评论

**总体评价**

Higress 是一款极具前瞻性的“AI 原生”网关，它成功将云原生流量治理与 AI 大模型应用所需的推理网关能力合二为一。作为阿里巴巴开源的基于 Istio 和 Envoy 的下一代网关，它不仅继承了云原生的高性能与可扩展性，更通过 WASM 技术和内置的 AI 特性，精准击中了当前企业构建 LLM（大语言模型）应用时的痛点，是连接传统微服务与未来 AI 服务的优秀基础设施。

**详细评价依据**

**1. 技术创新性：云原生与 AI 的深度融合**
*   **事实**：Higress 基于 Envoy 和 Istio 构建，并深度集成了 WebAssembly (WASM) 插件系统。它明确提出了“AI Gateway”的定位，内置了对 MCP (Model Context Protocol) 服务托管的支持。
*   **推断**：Higress 的核心差异化在于“统一”。传统网关（如 Nginx/Kong）处理 AI 流力不从心，而专用 AI 网关往往缺乏云原生流量治理能力。Higress 利用 WASM 的沙箱隔离和高性能特性，允许开发者用 Go/C++/Rust 编写插件来动态扩展 AI 逻辑（如 Token 计费、敏感词过滤），无需重启网关。这种将“MCP Server Hosting”直接集成进网关的设计，极大地简化了 AI Agent 的工具调用链路，属于架构上的重大创新。

**2. 实用价值：解决 AI 落地“最后一公里”的流量难题**
*   **事实**：README 中指出其核心功能包括 AI Gateway 特性、MCP 服务器托管以及传统的 K8s Ingress 和微服务路由。
*   **推断**：在实际场景中，企业接入 LLM 面临三大挑战：**密钥安全**（不能将 OpenAI Key 暴露给前端）、**成本控制**（Token 计费与限流）和**模型切换**（在通义千问和 DeepSeek 间切换）。Higress 作为 AI 网关，天然位于客户端和 LLM 供应商之间，能够统一处理这些横切面关注点。它使得企业可以在不修改业务代码的情况下，通过配置实现对 AI 流量的精细化管理，实用价值极高，特别适用于正在从传统微服务架构向 AI 架构转型的团队。

**3. 代码质量与架构设计：控制与数据分离的教科书级实践**
*   **事实**：DeepWiki 提到其架构分离了控制平面（配置管理）和数据平面（流量处理）。项目由阿里巴巴主导，拥有 7k+ 星标。
*   **推断**：基于 Istio 和 Envoy 意味着其在数据平面具有极高的并发处理性能和稳定性。Go 语言编写控制平面保证了开发效率。Higress 在设计上遵循了云原生的标准规范，架构清晰。其 WASM 插件系统的设计体现了良好的可扩展性原则，将核心逻辑与业务定制解耦。文档方面，提供了中日英三语 README 及详细的 DeepWiki，表明项目对开发者体验和文档完整性有较高要求。

**4. 社区活跃度与生态位：阿里背书的强劲势头**
*   **事实**：星标数 7,680（持续增长中），且明确由阿里巴巴团队维护。
*   **推断**：在开源网关领域，这是一个非常活跃的项目。阿里内部庞大的业务场景（如淘宝、天猫的流量洪峰及 AI 应用）为其提供了最好的“练兵场”，确保了代码的健壮性。相比纯粹的学术项目，Higress 更具工业级落地的可靠性。社区方面，由于切中了 AI 和云原生两大热点，吸引了大量寻求 AI 网关解决方案的开发者，生态正处于快速扩张期。

**5. 学习价值：理解流量治理与 AI 编排的窗口**
*   **事实**：项目涵盖了 WASM 插件开发、MCP 协议实现、Envoy 配置管理等多个技术栈。
*   **推断**：对于开发者而言，Higress 是学习如何将“古老”的流量治理技术应用于“新兴”的 AI 领域的绝佳案例。通过研究其 WASM 插件如何拦截并修改 LLM 请求/响应，开发者可以深入理解 HTTP 流量劫持、流式传输（SSE）处理以及 AI Agent 工具调用的底层逻辑。

**边界条件与不适用场景**

尽管 Higress 功能强大，但在以下场景中可能不是最优解：
1.  **极简边缘场景**：如果仅需在单台服务器上做简单的反向代理，Higress 基于 K8s 和 Istio 的架构显得过于重，Nginx 或 OpenResty 更轻量。
2.  **纯业务逻辑处理**：网关应专注于流量和路由，复杂的 AI 推理逻辑或业务计算不应放在网关插件中，以免阻塞关键路径。
3.  **非 K8s 环境的强依赖**：虽然支持 Standalone 模式，但其最大的威力在于 K8s 生态，如果您的基础设施未容器化，维护成本会较高。

**快速验证清单**

在决定采用 Higress 前，建议进行以下验证：

1.  **性能基准测试**：开启 WASM 插件后，使用压测工具对比 Higress 与 Nginx/Kong 的长连接并发处理能力及延迟，确认插件开销是否在可接受范围内。
2.  **AI 流量拦截实验**：配置一个指向 OpenAI 或通义千问

---
## 技术分析

# Higress 深度技术分析报告

基于阿里巴巴开源的 Higress 仓库（AI Native API Gateway），本文将从架构设计、核心功能、技术实现、适用场景及工程哲学等维度进行深入剖析。

---

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 的核心架构建立在 **云原生** 生态之上，采用了典型的 **控制平面与数据平面分离** 的架构模式。

*   **底层基座**：基于 **Envoy** 作为高性能数据平面，利用其 L3/L7 网络处理能力和可观测性。
*   **控制平面**：深度集成 **Istio**，复用 Istio 的 xDS (Discovery Service) 协议进行配置分发。这意味着 Higress 天然具备服务网格的能力，可以无缝管理 K8s Service。
*   **扩展层**：引入 **WebAssembly (WASM)** 作为插件运行时。这是其架构中最关键的一环，允许使用 C/C++/Go/Rust/AssemblyScript 等多种语言编写插件，并在 Envoy 的沙箱中高效运行。
*   **AI 原生层**：在传统网关之上，增加了一层专门针对 LLM（大语言模型）的语义处理层，实现了 Provider 的抽象和工具调用（MCP）的托管。

### 核心模块设计
1.  **Router (路由层)**：不仅支持 HTTP 路由，还针对 AI 语义化路由进行了增强（例如根据 Token 消耗或模型版本路由）。
2.  **WASM Plugin System (插件系统)**：通过 Proxy-WASM 规范，实现了插件的动态加载、热更新和隔离。这是其区别于 Nginx Lua 模块的一大进步。
3.  **AI Gateway (AI 网关)**：实现了 OpenAI 协议的标准化适配。无论后端是通义千问、DeepSeek 还是 Azure OpenAI，对客户端统一暴露 OpenAI 格式接口。
4.  **MCP Server Hosting (模型上下文协议托管)**：作为 AI Agent 的工具调度中心，Higress 能够将后端的 HTTP 服务包装为 MCP 协议供 Agent 调用。

### 架构优势分析
*   **配置热更新**：得益于 Istio 的 xDS 协议，配置变更可以达到毫秒级生效，且不断连。这对于处理 AI 长连接流式响应至关重要，避免了传统网关 Reload 带来的流量损失。
*   **生态兼容性**：通过复用 K8s Ingress 和 Istio Gateway 资源，降低了用户的迁移门槛。

---

## 2. 核心功能详细解读

### AI Gateway：LLM 流量的统一入口
*   **解决的关键问题**：在 AI 应用开发中，切换模型供应商通常意味着修改大量客户端代码。不同厂商的 API 协议（Auth、格式、错误码）各异。
*   **功能实现**：Higress 提供了 **Provider 抽象**。用户只需在网关层配置不同的 API Key 和 Endpoint，业务代码只需调用 Higress 的标准接口。它支持将非 OpenAI 协议（如 HuggingFace, 通义千问）转换为 OpenAI 协议。
*   **高级特性**：**Prompt 模板管理**（在网关层注入 System Prompt）、**Token 计费与限流**（基于 Token 数量而非简单的请求数进行限流，防止成本失控）。

### MCP (Model Context Protocol) Server Hosting
*   **技术原理**：MCP 是连接 AI Agent 与外部数据源的开放标准。Higress 充当了 MCP Host 的角色，允许将内部的 RESTful API 动态注册为 MCP Tools。
*   **价值**：解决了 Agent 调用内部微服务时的安全鉴权和协议转换问题。企业无需暴露内部服务端口，通过 Higress 统一管控 Agent 能访问哪些工具。

### 与同类工具对比
| 特性 | Higress | Nginx/Kong | Traefik |
| :--- | :--- | :--- | :--- |
| **AI 原生支持** | **内置** (Provider转换, Token限流) | 需编写复杂 Lua/Go 插件 | 需要中间件或插件 |
| **扩展性** | **WASM** (多语言, 沙箱, 高性能) | Lua (阻塞式), Go (进程外) | Go (中间件, 耦合度高) |
| **K8s 集成** | **Istio 原生** (CRD 支持) | Ingress Controller | Ingress Controller |
| **配置热更新** | **毫秒级** (xDS) | 秒级/分钟级 (Reload) | 秒级 |

---

## 3. 技术实现细节

### 关键技术方案
*   **WASM 虚拟机集成**：Higress 在 Envoy 中集成了 WASM 运行时。通过 `http_filters` 配置，将请求处理权交给 WASM 模块。这允许开发者用 Go 编写业务逻辑，编译为 `.wasm` 文件后推送到网关运行。
*   **流式处理**：在处理 LLM 流式响应（SSE）时，Higress 在 Envoy 的 Streaming Filter 层进行操作。它能够拦截流式数据包，进行实时日志记录、敏感词过滤或内容审查，而不会阻塞整个流的传输。

### 性能优化
*   **零拷贝**：Envoy 本身的高性能特性被完整保留。
*   **异步处理**：WASM 插件中的阻塞操作（如调用外部鉴权服务）通过 Envoy 的异步 API 处理，避免阻塞主事件循环。

### 代码组织结构
*   **`/pkg`**：核心业务逻辑，包括 config 解析、路由匹配。
*   **`/plugins`**：内置 WASM 插件的源码（如 Keyless Auth, Request Block）。
*   **`/installer`**：针对 K8s 的 Helm Charts 和 Operator 逻辑。

---

## 4. 适用场景分析

### 最适合的场景
1.  **AI 应用中台**：企业内部有多个大模型应用（如客服、代码助手），需要统一管理 API Key、监控 Token 消耗、限制不同部门的配额。
2.  **微服务 API 网关**：特别是已经使用 Istio 的云原生架构，Higress 可以作为 Ingress Gateway 直接下沉接管流量，无需引入额外的网关层。
3.  **AI Agent 开发**：需要将企业内部 API 暴露给 LLM Agent，利用 Higress 的 MCP Hosting 功能做安全隔离和协议转换。

### 不适合的场景
1.  **极简静态站点托管**：杀鸡焉用牛刀，Nginx 或 Caddy 更轻量。
2.  **非 K8s 环境的边缘计算**：虽然支持 Docker，但其强大依赖于 K8s 和 Istio 的生态，在纯虚拟机环境下部署复杂度较高。
3.  **极致低延迟（微秒级）的纯四层转发**：Envoy 本身有开销，直接使用 IPVS 或 LVS 可能更合适。

### 集成注意事项
*   **资源消耗**：WASM 插件运行会消耗额外的内存和 CPU，在高并发下需监控 Pod 资源。
*   **配置复杂度**：虽然提供了 Console，但深度定制需要理解 Istio 的 CRD 和 Envoy 的配置逻辑。

---

## 5. 发展趋势展望

*   **从流量管控向语义管控演进**：未来的网关不仅要看 HTTP Header，还要理解 Payload 中的 JSON 意图。Higress 可能会引入更轻量的本地向量检索能力，实现基于语义的路由。
*   **MCP 生态的深化**：随着 AI Agent 的普及，Higress 有望成为企业内部 "MCP Hub"，管理所有对外暴露的工具。
*   **更多 AI 模型的原生适配**：除了文本，对多模态（图片、音频）流量的处理和转换支持。

---

## 6. 学习建议

### 适合人群
*   具备 **Go 语言** 基础的开发者。
*   熟悉 **Kubernetes** 和 **Docker** 的运维/SRE 工程师。
*   对 **云原生网关** 和 **Service Mesh** 感兴趣的架构师。

### 学习路径
1.  **基础**：先理解 Envoy 是什么（xDS, Listener, Cluster, Filter）。
2.  **入门**：在本地 Kind 集群中通过 Helm 安装 Higress，跑通第一个 AI 转发示例。
3.  **进阶**：阅读官方内置的 Go WASM 插件源码，尝试编写一个自定义的 Header 修改插件。
4.  **高级**：研究其与 Istio 控制平面的交互，理解如何通过 CRD 控制网关行为。

---

## 7. 最佳实践建议

### 正确使用方式
*   **分离关注点**：将业务逻辑尽量放在后端服务，网关层仅处理通用的鉴权、限流、协议转换和路由。避免在 WASM 插件中编写复杂业务代码，导致网关难以维护。
*   **利用配置版本管理**：将 Higress 的配置（Ingress/Gateway 等）存入 Git，实现 GitOps 流程。

### 常见问题解决
*   **流式响应中断**：检查 WASM 插件中是否错误地终止了流，或者 Buffer 设置过大。
*   **WASM 插件加载失败**：确保编译架构与 Higress 运行时架构一致（通常为 `wasm32`）。

### 性能优化建议
*   **按需加载 WASM**：并非所有路由都需要加载所有插件，利用 Route 级别的插件配置，减少不必要的计算开销。
*   **连接池调优**：针对 AI 请求长连接的特点，适当调整 Envoy 的 Upstream 连接池大小和 Idle Timeout。

---

## 8. 哲学与方法论：第一性原理与权衡

### 抽象层与复杂性转移
Higress 在 **"流量基础设施"** 与 **"应用业务逻辑"** 之间建立了一个标准的抽象层。
*   **复杂性转移**：它将 **协议适配**（如 OpenAI 格式转换）和 **服务治理**（如限流、熔断）的复杂性从应用代码中剥离，转移到了网关层。
*   **代价**：这种转移要求运维团队具备更高的云原生技能。以前是开发改代码解决问题，现在可能是运维改网关配置解决问题，这改变了组织内的责任边界。

### 默认价值取向
*   **标准化与互操作性**：Higress 牺牲了一定的灵活性（如 Nginx 的自由脚本），换取了 **Istio 标准化** 的控制能力。它默认认为 "声明式配置" 优于 "命令式脚本"。
*   **安全隔离**：通过 WASM 沙箱，它默认认为 "插件崩溃不应导致网关崩溃"，这比 Lua 脚本更安全，但牺牲了部分运行时性能。

### 工程哲学与误用风险
*   **范式**：**"Ingress as Code"**。它试图将所有流量

---
## 代码示例




```python
# 示例1：基于Higress的API网关配置
def higress_api_gateway_config():
    """
    配置Higress作为API网关，实现路由转发和流量控制
    解决问题：统一管理多个微服务的API入口
    """
    config = {
        "name": "user-service-gateway",
        "routes": [
            {
                "path": "/api/v1/users/*",
                "service": "user-service:8080",
                "plugins": {
                    "rate-limit": "100req/min",  # 限流配置
                    "auth": "jwt"               # JWT认证
                }
            },
            {
                "path": "/api/v1/orders/*",
                "service": "order-service:8081",
                "plugins": {
                    "cors": "*",                # 跨域配置
                    "cache": "redis"            # Redis缓存
                }
            }
        ]
    }
    return config

# 说明：这个示例展示了如何使用Higress配置API网关，实现路由转发、限流、认证和缓存等核心功能
```




```python
# 示例2：Higress插件开发 - 自定义请求头处理
def custom_header_plugin():
    """
    开发Higress插件处理自定义请求头
    解决问题：在网关层统一添加或修改请求头
    """
    def handle_request(request):
        # 添加自定义请求头
        request.headers["X-Request-ID"] = generate_uuid()
        request.headers["X-Client-IP"] = get_client_ip(request)
        
        # 验证必要请求头
        if "X-Auth-Token" not in request.headers:
            return unauthorized_response()
            
        return request
    
    def handle_response(response):
        # 添加响应头
        response.headers["X-Response-Time"] = calculate_duration()
        return response
    
    return {
        "name": "custom-header-plugin",
        "onRequest": handle_request,
        "onResponse": handle_response
    }

# 说明：这个示例展示了如何开发Higress插件，在请求和响应阶段添加自定义HTTP头
```




```python
# 示例3：Higress流量灰度发布配置
def canary_release_config():
    """
    配置Higress实现服务的灰度发布
    解决问题：平滑升级服务，降低发布风险
    """
    config = {
        "service": "product-service",
        "versions": [
            {
                "name": "v1-stable",
                "weight": 90,  # 90%流量
                "endpoints": ["product-v1:8080"]
            },
            {
                "name": "v2-canary",
                "weight": 10,  # 10%流量
                "endpoints": ["product-v2:8080"],
                "match_rules": {
                    "headers": {
                        "X-Canary": "true"  # 带此头的请求强制走v2
                    }
                }
            }
        ],
        "monitoring": {
            "metrics": ["latency", "error_rate"],
            "threshold": {
                "error_rate": 0.01  # 错误率超过1%自动回滚
            }
        }
    }
    return config

# 说明：这个示例展示了如何使用Higress配置灰度发布，实现按权重或规则的流量分配，并配置自动回滚机制
```


---
## 案例研究


### 1：识货 APP

 1：识货 APP

**背景**:
识货是虎扑旗下的一款电商导购平台，拥有庞大的用户群体和复杂的业务场景。随着业务的快速发展，识货原有的基于 Nginx 的网关架构在维护性和扩展性上面临挑战，特别是在处理复杂的流量路由和灰度发布需求时。

**问题**:
1. **配置管理复杂**：原有的 Nginx 配置管理缺乏标准化，随着业务规则增多，配置文件难以维护，容易出错。
2. **流量治理能力不足**：难以灵活支持按权重、参数或 Header 进行的灰度发布（金丝雀发布），导致新功能上线风险较高。
3. **云原生转型需求**：为了配合整体架构向 Kubernetes (K8s) 的云原生转型，需要一款能够原生融入 K8s 生态的 API 网关。

**解决方案**:
识货团队决定将流量网关从 Nginx 迁移到 Higress。Higress 基于阿里云的 Envoy 集群构建，深度集成了 K8s Ingress API。利用 Higress，团队实现了：
1. 将 K8s Ingress 资源直接转化为网关路由配置，实现了配置的自动化管理。
2. 利用 Higress 的高级路由功能，实现了基于 Header 和权重的精细化灰度流量切分。
3. 通过 Higress 对 Dubbo 和 gRPC 协议的支持，打通了微服务间的通信瓶颈。

**效果**:
1. **运维效率提升**：网关配置的变更实现了自动化和标准化，运维效率提升了 50% 以上，且消除了人为配置错误导致的事故。
2. **发布安全性增强**：成功实现了平滑的灰度发布能力，新版本上线可以控制极小比例的流量进行验证，极大降低了上线风险。
3. **性能优化**：在处理高并发流量时，Higress 展现出了优异的性能，延迟相比旧架构有所降低。

---



### 2：深势科技

 2：深势科技

**背景**:
深势科技致力于将人工智能与生物计算相结合，进行药物研发。其科学计算平台对底层基础设施的稳定性、安全性以及对外部 API 的调用效率有极高的要求。

**问题**:
1. **API 认证与鉴权繁琐**：平台需要对外开放大量 API 接口供科研人员调用，原有的网关在处理复杂的鉴权逻辑（如 AK/SK 校验）时扩展性差。
2. **全链路可观测性缺失**：在微服务架构下，当 API 调用出现延迟或失败时，难以快速定位是网关问题还是后端服务问题。
3. **第三方服务集成困难**：业务中需要集成多种外部 AI 模型服务，调用链路管理混乱。

**解决方案**:
深势科技引入 Higress 作为统一的 API 出入口。
1. **插件化鉴权**：利用 Higress 的 Lua/Wasm 插件市场，定制了符合企业内部规范的鉴权插件，无缝对接了内部的账号体系。
2. **日志与监控集成**：利用 Higress 原生对接阿里云日志服务 (SLS) 和 Prometheus 的能力，建立了完整的 API 访问日志和监控大盘。
3. **服务聚合与负载均衡**：通过 Higress 的后端服务发现功能，实现了对多个 AI 模型实例的负载均衡和健康检查，确保了高可用性。

**效果**:
1. **安全性提升**：实现了细粒度的 API 访问控制，未授权的访问请求被有效拦截。
2. **故障排查提速**：通过统一的日志和监控，开发人员可以在 1 分钟内定位到 API 请求的瓶颈所在，排查效率显著提升。
3. **系统稳定性增强**：在后端服务出现波动时，Higress 的自动摘除机制保证了整体服务的连续性，提升了平台的可靠性。

---
## 对比分析

## 与同类方案对比

| 维度 | Higress | Nginx | Kong |
|------|---------|-------|------|
| 性能 | 基于Istio和Envoy，高性能，支持动态配置 | 高性能，但静态配置限制灵活性 | 高性能，但插件可能增加延迟 |
| 易用性 | 提供控制台和Kubernetes集成，易于管理 | 配置复杂，需手动编辑配置文件 | 提供管理界面，但配置较复杂 |
| 成本 | 开源免费，云服务按需付费 | 开源免费，但需自行维护 | 开源版免费，企业版收费 |
| 扩展性 | 支持Wasm插件，扩展性强 | 模块化扩展，但需重新编译 | 插件生态丰富，但依赖社区 |
| 社区支持 | 阿里背书，社区活跃 | 成熟社区，资源丰富 | 活跃社区，企业支持 |

### 优势分析

- 优势1：深度集成Kubernetes和Istio，适合云原生环境。
- 优势2：支持Wasm插件，扩展性和灵活性高。
- 优势3：提供开箱即用的控制台，降低运维复杂度。

### 不足分析

- 不足1：社区和生态相对Nginx和Kong较新，资源较少。
- 不足2：依赖Istio和Envoy，学习曲线较陡。
- 不足3：云服务功能可能受限于阿里云生态。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Ingress 的流量管理与路由配置

**说明**:  
Higress 基于 Kubernetes Ingress API 提供了强大的流量管理能力。通过合理配置 Ingress 资源，可以实现基于域名、路径、Header 等条件的精确路由，并支持蓝绿发布、金丝雀发布等高级流量管理功能。

**实施步骤**:
1. 定义 Ingress 资源时，明确指定 `spec.rules` 中的 `host` 和 `path` 字段。
2. 使用 `nginx.ingress.kubernetes.io/canary` 注解实现金丝雀发布。
3. 通过 `nginx.ingress.kubernetes.io/canary-weight` 控制流量分配比例。

**注意事项**:  
- 确保 Higress Ingress Controller 已正确部署并监听 Ingress 资源变化。
- 测试路由规则时，建议先在非生产环境验证流量分配逻辑。

---

### 实践 2：插件系统的扩展与定制

**说明**:  
Higress 提供了灵活的插件系统，支持 Lua、WASM 等多种语言开发自定义插件。通过插件可以扩展 Higress 的功能，例如添加自定义认证、日志记录或流量修改逻辑。

**实施步骤**:
1. 编写插件逻辑（如 Lua 脚本或 WASM 模块）。
2. 将插件文件上传到 Higress 的插件目录或通过 ConfigMap 挂载。
3. 在 Higress 控制台或通过 API 启用插件并配置参数。

**注意事项**:  
- 插件开发需遵循 Higress 的插件规范，避免与核心功能冲突。
- 生产环境部署前，需充分测试插件的性能和稳定性。

---

### 实践 3：高可用部署与弹性伸缩

**说明**:  
Higress 支持水平扩展和负载均衡，适合高并发场景。通过合理配置副本数和资源限制，可以确保服务的稳定性和弹性。

**实施步骤**:
1. 使用 Kubernetes Deployment 部署 Higress，设置 `replicas` 参数（建议至少 3 副本）。
2. 配置 `resources` 字段限制 CPU 和内存使用。
3. 结合 HPA（Horizontal Pod Autoscaler）实现自动扩缩容。

**注意事项**:  
- 监控 Higress 的资源使用情况，避免因资源不足导致性能下降。
- 确保后端服务也能承受 Higress 扩容后的流量压力。

---

### 实践 4：安全防护与访问控制

**说明**:  
Higress 提供了多种安全机制，包括 IP 黑白名单、请求限流、JWT 认证等。合理配置这些功能可以有效防御恶意攻击和未授权访问。

**实施步骤**:
1. 通过 `nginx.ingress.kubernetes.io/whitelist-source-range` 注解配置 IP 白名单。
2. 使用 `nginx.ingress.kubernetes.io/limit-rps` 注解设置请求限流。
3. 启用 JWT 认证插件并配置密钥。

**注意事项**:  
- 定期更新安全策略，避免规则过时或失效。
- 限流阈值需根据实际业务量调整，避免误伤正常流量。

---

### 实践 5：监控与日志集成

**说明**:  
Higress 支持与 Prometheus、Grafana 等监控工具集成，同时可以输出访问日志到 Elasticsearch 或其他日志系统。完善的监控和日志体系有助于快速定位问题。

**实施步骤**:
1. 部署 Prometheus 并配置 Higress 的 ServiceMonitor。
2. 在 Grafana 中导入 Higress 官方提供的仪表盘模板。
3. 配置 Higress 的日志输出格式（如 JSON），并对接日志收集系统。

**注意事项**:  
- 确保监控数据的存储和查询性能满足需求。
- 日志字段需包含关键信息（如请求 ID、响应时间等），便于排查问题。

---

### 实践 6：多集群与混合云部署

**说明**:  
Higress 支持多集群和混合云部署，可以通过统一的控制平面管理分布在不同环境中的流量。这种模式适合需要跨地域或跨云厂商的场景。

**实施步骤**:
1. 在每个集群中部署 Higress，并配置统一的控制平面。
2. 使用 `IngressClass` 或标签区分不同集群的流量。
3. 通过 DNS 或全局负载均衡器（GSLB）实现流量调度。

**注意事项**:  
- 确保集群间的网络连通性和安全性。
- 定期同步配置，避免因配置不一致导致流量异常。

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/3 (QUIC) 协议支持

**说明**: Higress 基于 Envoy 代理构建，Envory 对 HTTP/3 及其底层 QUIC 传输协议有着良好的原生支持。HTTP/3 解决了 TCP 队头阻塞问题，能显著改善弱网环境下的连接建立速度和吞吐量，对于跨地域或移动端 API 调用性能提升明显。

**实施方法**:
1. 在 Higress 网关的监听器配置中，为 HTTPS 端口（通常是 443）添加 HTTP/3 协议栈。
2. 配置 UDP 端口（通常也是 443）的防火墙和安全组放行策略。
3. 在网关配置中开启 Alt-Svc 诱导，引导浏览器或客户端升级到 HTTP/3。
4. 调整 QUIC 协议参数（如最大并发流限制）以适配高并发场景。

**预期效果**: 在高丢包率或高延迟网络环境下，请求延迟降低 20%-40%，连接建立失败率显著下降。

---

### 优化 2：配置全链路 HTTP/2 与连接复用

**说明**: Higress 与后端服务之间的通信效率直接影响吞吐量。默认的 HTTP/1.1 每次请求都会消耗较多的头部开销，且连接复用率不如 HTTP/2。开启后端 HTTP/2 可以利用多路复用技术，减少后端连接数，降低后端服务器的资源消耗（CPU/内存）。

**实施方法**:
1. 在服务来源或路由配置中，显式指定后端协议为 HTTP/2 (gRPC 也同理)。
2. 启用 Higress 到后端 Upstream 的连接池配置，适当调大 HTTP/2 的最大并发流数。
3. 开启请求级别的连接复用，避免频繁握手。

**预期效果**: 后端连接数减少 50% 以上，后端服务 CPU 负载降低 10%-20%，长尾请求延迟减少。

---

### 优化 3：启用本地与分布式缓存

**说明**: 对于读多写少的 API 或静态内容，启用网关层缓存可以极大减少回源请求。Higress 支持将响应数据缓存于本地内存或对接外部分布式缓存（如 Redis）。这能直接拦截大量重复请求，保护后端业务。

**实施方法**:
1. 在特定的路由规则中启用缓存开关。
2. 根据业务特点配置缓存 Key 的生成规则（如忽略特定 Query 参数）。
3. 设置合理的 TTL（生存时间）与缓存状态码（如仅缓存 200 和 304）。
4. 若数据量较大，可配置 Higress 对接 Redis 作为分布式缓存层，避免网关 Pod 重启导致缓存失效。

**预期效果**: 缓存命中时，后端请求量减少 90% 以上（视命中率而定），API 响应延迟降低至 1ms-5ms 级别。

---

### 优化 4：优化 WAF 与插件执行链路

**说明**: Higress 拥有强大的插件扩展能力（WAF、Auth、限流等）。然而，复杂的 Lua 或 WASM 插件逻辑会增加 CPU 指令周期。特别是在高并发下，正则匹配、复杂的鉴权逻辑会成为瓶颈。

**实施方法**:
1. **插件按需加载**: 仅在必要的域名或路由上启用特定插件，避免全局生效带来的性能损耗。
2. **规则优化**: 检查 WAF 规则，优化低效的正则表达式，移除冗余的拦截规则。
3. **优先级调整**: 将轻量级插件（如静态鉴权）置于执行链前端，快速拒绝非法请求；将重量级插件（如日志上报）置于异步处理或链路后端。
4. 考虑使用 WASM 插件替代部分 Lua 插件以获得接近原生的执行性能。

**预期效果**: 处理单个请求的 CPU 指令数减少 15%-30%，网关 P99 延迟明显降低

---
## 学习要点

- 基于对 Alibaba Higress 项目特性的分析，总结关键要点如下：
- Higress 是阿里巴巴开源的一款基于 Istio 的云原生 API 网关，深度集成了 K8s Ingress 与 Gateway API 标准。
- 该项目将 K8s 的 Ingress Controller 控制平面与 Envoy 高性能数据平面进行了有机结合与优化。
- 它提供了强大的流量治理能力，支持金丝雀发布、蓝绿部署、负载均衡以及超时重试等全链路管理。
- Higress 兼容 Nginx Ingress 注解，并支持从 Nginx 平滑迁移，降低了传统网关用户的迁移成本。
- 内置了对 Dubbo、Nacos 以及 gRPC 等微服务生态的广泛支持，解决了服务间通信的协议转换问题。
- 提供了开箱即用的 WAF（Web 应用防火墙）插件能力，能够有效防范 SQL 注入、XSS 等常见 Web 安全威胁。


---
## 学习路径

## 学习路径

### 阶段 1：基础认知与快速上手

**学习内容**:
- **云原生网关概念**: 理解 API 网关在微服务架构中的位置，以及 Ingress（入口网关）和 Gateway（API 网关）的区别。
- **Higress 架构概览**: 了解 Higress 基于 Istio 和 Envoy 的技术架构，以及其“高可用、高性能、热更新”的特性。
- **环境搭建**: 学习如何在本地 Docker 环境或 Kubernetes 集群中快速安装和部署 Higress。
- **基础流量管理**: 掌握如何通过控制台（Console）或 K8s YAML 配置简单的路由转发，将流量导入后端服务。

**学习时间**: 1-2周

**学习资源**:
- [Higress 官方 GitHub 仓库](https://github.com/alibaba/higress) (阅读 README 和架构图)
- [Higress 官方文档 - 快速开始](https://higress.io/docs/latest/overview/what-is-higress/)
- [Higress 官方博客 - 核心特性介绍](https://higress.io/blog/)

**学习建议**: 建议先通过 Docker Desktop 在本地运行 Higress，并使用官方提供的 httpbin 示例服务进行第一次路由配置实验，不要一开始就陷入复杂的 K8s 配置细节。

---

### 阶段 2：核心功能与流量治理

**学习内容**:
- **服务来源管理**: 学习如何配置 Nacos、Consul、K8s Service 以及固定地址（IP/域名）作为服务来源。
- **高级路由策略**: 掌握基于 Header、Query、Cookie 等条件的精准路由匹配，以及路径重写和重定向。
- **全链路安全**: 配置 HTTPS 证书管理，实现域名级别的 TLS 加密；学习如何开启 JWT 认证或 Key Auth 认证插件。
- **插件系统（Wasm）**: 理解 Higress 的插件机制，学习如何在控制台开启常用插件（如限流、CORS 处理、请求/响应修改）。

**学习时间**: 2-3周

**学习资源**:
- [Higress 官方文档 - 流量管理](https://higress.io/docs/latest/user/traffic-management/)
- [Higress 官方文档 - 插件市场](https://higress.io/docs/latest/user/plugin-overview/)
- [Higress 官方样例 - 在 K8s 中部署](https://github.com/higress-group/samples)

**学习建议**: 尝试构建一个包含两个服务的模拟环境（例如用户服务和订单服务），配置路由规则实现按比例分发流量（金丝雀发布灰度），并尝试配置一个简单的限流策略。

---

### 阶段 3：生态集成与高阶应用

**学习内容**:
- **AI 网关特性**: 深入了解 Higress 对 AI/LLM 的支持，学习如何配置大模型路由、Token 处理以及与阿里云通义千问等模型的集成。
- **Dubbo 与 Nacos 深度集成**: 学习如何将 Higress 作为 Dubbo 服务的网关，实现 HTTP 转 Dubbo 协议，以及 Nacos 服务发现的详细配置。
- **Wasm 插件开发**: 学习使用 Go 或 C++ 开发自定义 Wasm 插件，实现业务逻辑的定制化处理。
- **高可用与性能调优**: 了解 Higress 的部署模式，配置健康检查，理解 Envoy 的配置热更新机制。

**学习时间**: 3-4周

**学习资源**:
- [Higress 官方文档 - AI 网关](https://higress.io/docs/latest/user/ai-gateway/)
- [Higress 官方文档 - Dubbo 服务代理](https://higress.io/docs/latest/user/dubbo-proxy/)
- [Higress 官方文档 - 插件开发指南](https://higress.io/docs/latest/developer/wasm-go/)

**学习建议**: 此时建议结合实际业务场景进行思考。如果涉及 AI 应用，重点研究 AI 网关的内容；如果是传统微服务，重点研究 Dubbo 和 Nacos 的无缝对接。尝试编写一个简单的 Wasm 插件来处理特定的请求头。

---

### 阶段 4：生产运维与源码剖析

**学习内容**:
- **监控与可观测性**: 集成 Prometheus、Grafana 和 SkyWalking，配置日志服务（SLS/ELK），分析网关的访问日志和指标。
- **多集群容灾**: 学习如何配置多套 Higress 集群以实现异地多活或主备容灾。
- **源码级理解**: 阅读 Higress Controller 和 Router 的源码，理解配置如何从 K8s CRD 下发至 Envoy 的数据流转过程。
- **社区贡献**: 学习如何向 Higress 提交 Issue

---
## 常见问题


### 1: Higress 是什么？它与阿里巴巴有什么关系？

1: Higress 是什么？它与阿里巴巴有什么关系？

**A**: Higress 是一款基于阿里内部多年实践沉淀的下一代云原生 API 网关。它诞生于阿里巴巴，旨在解决云原生时代流量管理的复杂性。Higress 的前身是阿里巴巴内部广泛使用的 Tengine Gateway 和 Sentinel Gateway 等系统。它于 2022 年开源，结合了 K8s Ingress 网关和微服务网关的功能，旨在提供一套统一、高性能、易扩展的流量管理平台。虽然源自阿里，但它是一个完全开源的项目，遵循 Apache 2.0 协议，由社区共同驱动发展。

---



### 2: Higress 与 Nginx、Envoy 或 APISIX 相比有什么优势？

2: Higress 与 Nginx、Envoy 或 APISIX 相比有什么优势？

**A**: Higress 的核心优势在于其“云原生”基因和“统一”能力。

1.  **底层架构**：与 Nginx 不同，Higress 基于 Envoy（C++ 编写，高性能）作为数据平面，利用了 Envoy 在 L7 路由、负载均衡和可观测性方面的强大能力。
2.  **功能融合**：它试图打通“K8s Ingress”和“微服务网关”的界限。传统的 K8s Ingress（如 Nginx Ingress）通常只负责南北向流量，而微服务网关负责东西向流量和服务治理。Higress 旨在同时处理这两种场景，支持 Dubbo、Nacos 等微服务生态的深度集成，这是 APISIX 或标准 Nginx Ingress 需要额外配置或插件才能实现的。
3.  **安全与防护**：它内置了与阿里云 WAF 同源的安全能力，提供了开箱即用的防护功能。
4.  **扩展性**：支持使用 WASM (WebAssembly) 插件，开发者可以使用 Go、C++、Rust 等语言编写插件，而无需修改网关核心代码或使用 Lua，这比传统的 OpenResty (Nginx+Lua) 方式更安全、更灵活。

---



### 3: Higress 是否支持 Kubernetes？如何作为 Ingress Controller 使用？

3: Higress 是否支持 Kubernetes？如何作为 Ingress Controller 使用？

**A**: 是的，Higress 对 Kubernetes 有着原生的深度支持。它可以直接部署在 K8s 集群中，并作为 Ingress Controller 运行。

1.  **部署方式**：用户可以通过 Helm Chart 一键将 Higress 部署到 K8s 集群中。
2.  **资源管理**：它会自动监听 Kubernetes 的 Ingress、Gateway API 等资源对象，并根据配置自动更新路由规则。
3.  **服务发现**：除了标准的 K8s Service 发现，Higress 还支持注册中心（如 Nacos、Consul、ZooKeeper）的服务发现，这意味着它可以将流量路由到 K8s 集群外的微服务，实现混合云架构下的流量统一管理。

---



### 4: Higress 如何处理服务发现？它支持 Nacos 吗？

4: Higress 如何处理服务发现？它支持 Nacos 吗？

**A**: Higress 在服务发现方面设计得非常灵活，这是它区别于传统 API 网关的一大特点。它不仅支持标准的 Kubernetes Service，还深度集成了主流的微服务注册中心。

1.  **Nacos 支持**：作为阿里系产品，Higress 对 Nacos 有着原生的完美支持。用户可以直接在 Higress 中配置 Nacos 服务地址，Higress 会自动同步 Nacos 中的服务列表，实现基于服务名的路由转发。
2.  **多协议支持**：除了 HTTP，它还支持 Dubbo、gRPC 等 RPC 协议的服务发现和路由，这对于使用 Spring Cloud Alibaba 或 Dubbo 框架的微服务应用来说非常友好，无需将 RPC 协议转换为 HTTP 即可直接透传。

---



### 5: Higress 是否兼容 Istio？能否接管 Istio 的 Gateway？

5: Higress 是否兼容 Istio？能否接管 Istio 的 Gateway？

**A**: 是的，Higress 在设计上考虑了与 Istio 生态的兼容性。

1.  **配置兼容**：Higress 支持Istio 的 API 规范，这意味着基于 Istio Gateway 和 VirtualService 配置的应用，可以相对平滑地迁移到 Higress 上。
2.  **替代方案**：Higress 常被视为 Istio Gateway 的轻量级替代品。Istio 原生的 Gateway 基于 Envoy，但配置复杂、资源消耗较大。Higress 提供了更符合国内开发者习惯的控制台和配置方式，同时保留了 Envoy 的高性能，且去除了 Istio 控制面繁重的 Sidecar 注入需求（如果仅作为网关使用），因此常被用于替代 Istio Ingress Gateway 来降低集群复杂度。

---



### 6: Higress 支持 WASM 插件吗？如何扩展功能？

6: Higress 支持 WASM 插件吗？如何扩展功能？

**A**: 支持 WASM (WebAssembly) 是 Higress 的核心亮点之一。

1.  **插件机制**：Higress 允许用户通过 WASM 技术扩展网关功能。这意味着开发者可以使用 Go

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: 基于环境流量的动态路由

### 难度**: [简单]

### 问题描述**:

### 基于 Higress 的标准网关功能，设计一个流量路由策略。要求将发往 `/api/v1` 路径的请求，根据 HTTP Header 中 `x-env` 的值（`dev` 或 `prod`）分别转发到两个不同的后端服务（Service A 和 Service B）。

---
## 实践建议

以下是针对 Higress（阿里云开源的 AI Native 网关）的 6 条实践建议，涵盖了网关选型、安全防护、模型管理及可观测性等实际场景：

### 1. 利用 Wasm 插件实现 AI 请求的“无损”处理
*   **场景**：需要对大模型的 Prompt 或 Response 进行修改（如敏感词过滤、Prompt 注入优化），但不希望引入额外的网络延迟。
*   **建议**：优先使用 Higress 的 Wasm (WebAssembly) 插件机制，而非传统的 Lua 脚本或外部微服务。Wasm 运行在网关进程内，接近原生代码的执行速度。
*   **最佳实践**：编写 Go 或 C++ 开发的 Wasm 插件来处理 JSON Body 的解析与修改。例如，开发一个插件自动在用户请求中插入“系统提示词”，以规范模型输出格式。
*   **常见陷阱**：在 Wasm 插件中进行耗时过长的计算（如复杂的数据加密或大模型推理），这会阻塞网关的处理线程，导致整体吞吐量下降。

### 2. 实施基于 Token 的精细化流控与计费
*   **场景**：大模型 API 的调用成本主要取决于 Token（词元）消耗量，而非单纯的 HTTP 请求数（RPM）。
*   **建议**：不要仅配置传统的“每秒请求数”限制。应结合 Higress 的本地限流或对接 Redis 限流功能，配置针对特定模型或用户的 Token 速率限制。
*   **最佳实践**：利用 Higress 对 LLM 协议（如 OpenAI 协议）的解析能力，在网关层统计 Token 消耗。对于高消耗用户实施“错峰填谷”策略，或者在用户配额耗尽时直接在网关层返回 429 状态码，避免请求打到后端模型服务商产生额外费用。

### 3. 构建统一的模型服务路由与降级策略
*   **场景**：企业内部同时调用通义千问、OpenAI 以及本地部署的开源模型（如 Llama 3），需要统一入口。
*   **建议**：利用 Higress 的服务路由功能，将不同的模型路径（如 `/v1/chat/completions`）映射到不同的后端服务。更重要的是，配置自动降级规则。
*   **最佳实践**：设置“超时”与“重试”策略。当某个云端模型 API 响应超过 5 秒或返回 5xx 错误时，网关自动将请求透明转发至备用的本地模型或成本更低的模型，确保业务不中断。
*   **常见陷阱**：忽略了流式（SSE）请求的超时设置。大模型响应慢是常态，如果全局超时设置过短（如 30 秒），会导致长文本生成中断。

### 4. 强化 Prompt 注入与 API 安全防护
*   **场景**：AI 网关直接暴露在公网，容易成为攻击目标（如 Prompt 越狱攻击或 Key 泄露）。
*   **建议**：启用 Higress 的安全插件（如结合阿里云 Wasm 插件市场中的安全规则），专门针对 AI 语义进行防护。
*   **最佳实践**：在网关层强制校验 HTTP Header 中的 `Authorization` 字段，严禁前端直接携带真实的 API Key 调用后端。网关应负责做“密钥转换”，将用户的业务 ID 转换为真实的模型 API Key，从而实现权限的统一管理与审计。

### 5. 针对长连接与 SSE 的连接池调优
*   **场景**：AI 对话通常使用 Server-Sent Events (SSE) 流式返回，连接保持时间较长。
*   **建议**：调整 Higress 及其底层 Envoy 的连接超时和最大请求数配置。
*   **最佳实践**：将 `stream_idle_timeout` 设置为较长的值（如 5 分钟），以适应慢速生成的模型响应。同时，开启 HTTP/2 对后端的支持，以减少连接建立的

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI 原生](/tags/ai-%E5%8E%9F%E7%94%9F/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [LLM](/tags/llm/) / [MCP](/tags/mcp/) / [WASM](/tags/wasm/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260206-github_trending-alibaba-higress-0.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260303-github_trending-alibaba-higress-0.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260206-github_trending-alibaba-higress-6.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260215-github_trending-alibaba-higress-5.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*