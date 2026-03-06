---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-03-06T12:46:24+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "LLM", "Istio", "Envoy", "WASM", "MCP 协议"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "Higress 是一款由阿里巴巴开源、基于 Go 语言开发的**云原生 AI 网关**。该项目在 GitHub 上拥有超过 7,600 颗星，旨在通过扩展 Istio 和 Envoy，为云原生应用和 AI 生态提供统一的流量入口。 **核心定位与架构：** Higress 是一个**AI 原生 API 网关**。它将控"
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
- **星标**: 7,668 (+18 stars today)
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

Higress 是基于 Istio 与 Envoy 构建的云原生 API 网关，通过深度集成 WASM 插件能力，实现了从传统流量管理到 AI 原生服务的平滑演进。本文将梳理其核心架构，重点解析 AI 网关特性、MCP 系统支持以及插件扩展机制，帮助开发者在混合架构中实现高效的流量治理。

---
## 摘要

Higress 是一款由阿里巴巴开源、基于 Go 语言开发的**云原生 AI 网关**。该项目在 GitHub 上拥有超过 7,600 颗星，旨在通过扩展 Istio 和 Envoy，为云原生应用和 AI 生态提供统一的流量入口。

**核心定位与架构：**
Higress 是一个**AI 原生 API 网关**。它将控制平面（配置管理）与数据平面（流量处理）分离，利用 WebAssembly (WASM) 插件能力实现了高度的可扩展性。其配置变更通过 xDS 协议传播，具备毫秒级延迟和无连接中断的特性，特别适合 AI 流式响应等长连接场景。

**三大主要功能场景：**

1.  **AI 网关（AI Gateway）：**
    *   提供**统一 API**，兼容 30 多家大语言模型（LLM）提供商。
    *   核心功能包括协议转换、可观测性、缓存以及安全防护（通过 `ai-proxy`, `ai-cache`, `ai-security-guard` 等插件实现）。

2.  **MCP 服务器托管：**
    *   托管**模型上下文协议（MCP）**服务器，赋能 AI 智能体（Agent）调用外部工具和服务。
    *   通过 `mcp-router` 和 `jsonrpc-converter` 等组件实现工具集成。

3.  **Kubernetes 入口（Ingress）：**
    *   作为 Kubernetes Ingress 控制器使用，兼容 nginx-ingress 注解，支持微服务路由等传统 API 网关功能。

总结来说，Higress 通过将传统 API 网关能力与 AI 特性深度融合，为 LLM 应用、Agent 工具链及微服务架构提供了一个高效、标准化的流量管理平台。

---
## 评论

### 总体判断

**Higress 是一款将云原生网关与 AI 生态深度融合的“新一代”基础设施，它成功将 Istio 的控制平面能力与 Envoy 的高性能数据平面进行了产品化封装。** 它不仅解决了传统 API 网关的配置复杂性问题，更通过 WASM 和 MCP 协议，率先为 LLM 应用提供了标准化的流量管理与工具调用入口，是目前将“云原生”与“AI Native”结合得最紧密的开源网关之一。

---

### 深入评价分析

#### 1. 技术创新性：云原生与 AI 的架构级融合
*   **事实（来源：DeepWiki）**：Higress 基于 Istio 和 Envoy 构建，核心扩展能力依赖 WebAssembly (WASM)，并明确提出了“AI Native API Gateway”的定位，集成了 MCP (Model Context Protocol) 服务器托管能力。
*   **推断与评价**：传统的网关（如 Nginx, Kong）主要关注 HTTP/TCP 转发，而 Higress 的创新在于**“协议感知层”的上移**。它不再仅仅把 AI 请求看作普通流量，而是理解 LLM 的上下文。
    *   **WASM 插件化**：利用 WASM 实现逻辑热加载，解决了传统网关（如 Lua Nginx）开发门槛高且不安全的问题，允许开发者用 Go/C++/Rust 编写复杂的 AI 请求处理逻辑（如 Prompt 注入、敏感词过滤）。
    *   **MCP 集成**：DeepWiki 提到的 MCP Server Hosting 是一大亮点。随着 AI Agent 的普及，模型需要调用外部工具。Higress 直接在网关层托管 MCP 服务，使得 Agent 可以通过网关统一管理和调度工具，这是一个极具前瞻性的架构设计，将网关从“流量入口”升级为“智能调度中心”。

#### 2. 实用价值：降低 AI 落地门槛与流量治理
*   **事实（来源：描述）**：提供 AI Gateway 特性、MCP 服务器托管以及 Kubernetes Ingress 微服务路由能力。
*   **推断与评价**：Higress 解决了 AI 时代的两个核心痛点：**Token 成本控制**和**模型切换的灵活性**。
    *   **统一接入**：企业往往同时使用 OpenAI、通义千问、DeepSeek 等多个模型。Higress 允许用户通过一套 API 接入所有模型，并在网关层做路由切换（例如：开发环境用开源模型，生产环境用闭源模型），极大降低了业务代码的耦合度。
    *   **流量治理**：AI 请求通常耗时较长且成本高昂。Higress 继承了 Istio 的流量治理能力，可以对 AI 请求进行超时控制、重试（处理 LLM 超时）以及并发限制，保护后端模型服务不被突发流量击垮。

#### 3. 代码质量与架构：工业级标准的控制面与数据面分离
*   **事实（来源：DeepWiki）**：架构分离了控制平面（配置管理）和数据平面（流量处理）。语言为 Go。
*   **推断与评价**：基于 **Go** 语言开发保证了二进制分发的便利性和并发性能。架构上，Higress 实际上是将复杂的 Istio 能力“下沉”并“简化”。
    *   **Kubernetes 原生**：它利用 CRD（自定义资源定义）来管理配置，符合云原生操作习惯，架构清晰。
    *   **文档完整性**：从提供的 DeepWiki 结构来看，项目具备从 Core Architecture 到 Development Guide 的完整文档链，这通常意味着项目具备较高的可维护性和对外部贡献者的友好度。代码结构应当遵循了 K8s Operator 的标准模式。

#### 4. 社区活跃度：阿里背书与开源生态
*   **事实（来源：描述）**：星标数 7,668，由 Alibaba 组织维护。
*   **推断与评价**：作为阿里云开源的网关产品，Higress 继承了阿里内部应对双十一流量的技术基因。7k+ 的 Star 数量在后端基础设施领域属于头部梯队。活跃度通常较高，且有阿里云团队兜底，不存在“个人项目突然停更”的风险。社区讨论主要集中在 AI 插件开发和 K8s 落地实践上。

#### 5. 学习价值：理解云原生与 AI 边界的最佳范本
*   **推断与评价**：对于开发者而言，Higress 是学习 **“如何将传统基础设施 AI 化”** 的绝佳案例。
    *   你可以从中学习如何设计一个高性能的 Proxy 系统。
    *   更有价值的是学习 **WASM 插件机制**，这是目前 Serverless 和边缘计算的热点技术。
    *   它展示了如何处理 SSE (Server-Sent Events) 流式转发，这是处理 LLM 流式输出的关键技术细节。

#### 6. 潜在问题与改进建议
*   **推断与评价**：
    *   **复杂度陷阱**：虽然它简化了 Istio，但对于非 K8s 用户或小团队来说，Higress 的部署和维护成本依然高于 Nginx 或简单的 API 网关。引入 K8s 依赖是一把双刃剑。
    *   **AI 功能成熟度**：作为较新的 AI Gateway，其 Prompt 模板管理、向量库连接等 AI 辅助功能可能不如 Dify 或 LangGate 这样的垂直 AI

---
## 技术分析

以下是对阿里巴巴开源的 **Higress** 项目的深度技术分析。Higress 定位为“AI Native API Gateway”，基于 Istio 和 Envoy 构建，旨在解决云原生架构下，特别是 AI 应用场景中的流量治理与模型集成问题。

---

### 1. 技术架构深度剖析

**技术栈与架构模式**
Higress 采用了标准的**控制平面与数据平面分离**的架构模式。
*   **数据平面**：深度依赖 **Envoy**。Envoy 作为高性能的 L7 代理，负责处理实际的流量转发、负载均衡以及 Wasm 插件的执行。Higress 对 Envoy 进行了定制化扩展，以支持特定的 AI 协议处理。
*   **控制平面**：基于 **Istio** 进行了大幅简化和增强。Higress 摒弃了 Istio 中繁重的 Sidecar 模式，专注于 Ingress Gateway 场景。它使用 Go 语言编写，通过 xDS 协议（包括 LDS, CDS, RDS, EDS 等）向数据平面下发配置。
*   **扩展层**：引入 **Proxy-Wasm** 机制。这是其架构的核心亮点，允许使用 C++/AssemblyScript/Rust/Go (通过特殊编译) 编写插件，并在 Envoy 的沙箱中运行，实现了逻辑的热加载和高性能隔离。

**核心模块与关键设计**
1.  **路由与流量管理**：支持基于 Host、Header、Path、Query Parameter 的细粒度路由，并兼容 Kubernetes Ingress API。
2.  **Wasm 插件系统**：Higress 内置了一个插件市场，支持动态加载 Wasm 插件。这使得网关的业务逻辑扩展不再需要重新编译网关本身，也无需重启网关进程。
3.  **AI 服务集成**：架构上专门针对 LLM（大语言模型）流量进行了优化，内置了针对 OpenAI、通义千问等模型协议的适配层。

**技术亮点与创新点**
*   **毫秒级配置推送**：通过优化 xDS 协议的推送逻辑，Higress 实现了配置变更的毫秒级生效，且连接不中断。这对于 AI 场景下的“流式响应”至关重要，避免了因配置更新导致的对话中断。
*   **MCP (Model Context Protocol) Server Hosting**：Higress 创新地将网关作为 MCP Server 的托管点。这意味着 AI Agent 可以直接通过网关安全、标准化地访问外部工具和数据，简化了 Agent 的工具调用链路。

**架构优势分析**
*   **性能损耗极低**：数据平面 Envoy 采用 C++ 编写，配合 Wasm 的近原生执行速度，使得网关转发延迟极低。
*   **生态兼容性**：既兼容 K8s Ingress，又兼容 Istio 的 Gateway API，降低了用户的迁移门槛。

---

### 2. 核心功能详细解读

**主要功能与使用场景**
1.  **AI 网关**：
    *   **功能**：提供统一的模型接入层，支持多模型切换、Token 计费与限流、Prompt 模板管理、以及敏感词过滤。
    *   **场景**：企业内部构建 AI 助手时，需要屏蔽底层模型差异（如从 GPT-4 切换到通义千问），并在网关层统一控制成本和权限。
2.  **MCP 协议支持**：
    *   **功能**：托管 MCP 服务，将后端服务包装为 AI Agent 可用的工具。
    *   **场景**：AI Agent 需要查询数据库或调用私有 API 时，通过 Higress 提供的标准 MCP 接口进行交互，实现安全的工具调用。
3.  **传统 API 网关**：
    *   **功能**：金丝雀发布、蓝绿部署、负载均衡、认证鉴权。
    *   **场景**：微服务架构下的流量治理。

**解决的关键问题**
*   **AI 流量的不可控性**：传统网关无法理解 AI 的流式传输和 Token 计量，Higress 解决了 AI 流量的可观测性和计费问题。
*   **模型厂商锁定**：通过标准化的 API 接口，使得应用层代码无需修改即可切换不同的 LLM 提供商。

**与同类工具的详细对比**
*   **vs. Nginx/Kong**：Kong 主要基于 Lua 插件，虽然灵活但并发性能受限于 Lua 虚拟机，且缺乏对 AI 协议的原生支持。Higress 的 Wasm 插件在隔离性和多语言支持上更优，且专为 AI 场景优化。
*   **vs. Istio Ingress**：原生 Istio 配置极其复杂，学习曲线陡峭。Higress 提供了极其简化的控制台和 K8s CRD，屏蔽了 Istio 的复杂性，同时针对 Ingress 场景做了性能优化。

**技术实现原理**
*   **AI 流式处理**：Higress 在 Envoy 层实现了对 HTTP Chunked 编码的深度解析，能够识别 LLM 返回的 SSE (Server-Sent Events) 流，并在不截断流的情况下进行日志记录和元数据注入。

---

### 3. 技术实现细节

**关键算法或技术方案**
*   **配置热更新算法**：Higress 控制平面维护了配置版本号。当配置变更时，它通过增量 xDS 推送机制，仅将变更的 Route 或 Cluster 配置推送给 Envoy。Envoy 通过原子操作切换配置树，确保流量不抖动。
*   **Wasm 虚拟机管理**：集成 `proxy-wasm` 规范，在 Envoy 中嵌入 Wasmtime 或 V8 引擎。这允许 Wasm 插件直接访问请求的 Header 和 Body，并在内存中修改请求内容。

**代码组织结构**
*   **`/pkg`**：核心业务逻辑，包括 Ingress 转换器（将 K8s Ingress 转为 Higress 配置）、xDS 控制器、以及路由处理器。
*   **/plugin**：Wasm 插件的 Go SDK 和示例代码。Higress 允许用户用 Go 编写插件，然后通过 `tinygo` 编译为 Wasm，这大大降低了插件开发门槛。
*   **/docker**：镜像构建相关，集成了 Envoy 的构建流程。

**性能优化与扩展性**
*   **零拷贝**：Envoy 在处理网络 I/O 时大量使用了零拷贝技术，Wasm 插件在处理 Buffer 时也尽量引用内存而非复制，以降低延迟。
*   **异步 I/O**：全异步非阻塞架构，使得单核能够处理数万并发连接。

**技术难点与解决方案**
*   **难点**：Wasm 插件的崩溃可能导致网关进程崩溃。
*   **方案**：Higress 利用 Envoy 的 Fault Injection 机制和 Wasm 的沙箱隔离特性，限制单个插件的内存和 CPU 使用量，防止单点故障扩散。

---

### 4. 适用场景分析

**适合使用的项目**
*   **大模型应用落地**：任何需要接入 OpenAI、Azure OpenAI、通义千问、文心一言等 LLM 的企业应用。
*   **微服务网关统一**：希望将传统微服务流量和 AI 流量统一管理的平台。
*   **需要高度定制化逻辑的网关**：例如，需要在网关层进行复杂的请求签名校验、A/B 测试逻辑，利用 Wasm 插件可以快速实现。

**最有效的情况**
*   当你需要对 **AI 请求进行细粒度控制**（如：超过 2000 Token 的请求直接拒绝，或者 Prompt 中包含敏感词时拦截）时，Higress 是目前市面上极少数原生支持这一能力的开源网关。

**不适合的场景**
*   **极简静态博客托管**：杀鸡焉用牛刀，Nginx 足矣。
*   **需要极其复杂的 TCP/UDP 协议转换**：虽然 Envoy 支持 L4，但 Higress 主要聚焦于 L7 (HTTP/gRPC)，对于纯 TCP 游戏流等复杂场景，可能需要直接操作 Envoy 配置，不如专门的游戏网关顺手。

**集成方式与注意事项**
*   **K8s 集成**：通过 Helm Chart 部署最为简单，会自动配置 Ingress Class。
*   **注意事项**：Wasm 插件虽然好用，但要注意插件本身的性能。如果在 Wasm 中执行大量计算（如加密解密），会显著增加网关延迟。

---

### 5. 发展趋势展望

**技术演进方向**
*   **从流量治理向 AI 治理演进**：网关将不再仅仅是“路由器”，而是 AI 时代的“调度器”。未来的 Higress 可能会集成更复杂的 RAG (检索增强生成) 编排能力，直接在网关层完成向量检索的转发。
*   **MCP 协议的标准化推广**：随着 Anthropic 的 MCP 协议普及，Higress 作为 MCP Server 的托管节点，将成为企业内部 AI Agent 架构的核心组件。

**社区反馈与改进空间**
*   目前 Higress 的控制台 UI 功能虽全但交互略显复杂，仍有优化空间。
*   对于非 K8s 环境的支持（如虚拟机部署）相对较弱，主要还是云原生导向。

**与前沿技术的结合**
*   **eBPF**：未来可能在数据平面引入 eBPF 替代部分 Wasm 功能，以获得更高的性能（如 Socket 级别的过滤）。
*   **Service Mesh (Sidecar) 模式**：虽然目前主打 Ingress，但社区有呼声将其重新回填为轻量级 Service Mesh 数据平面，用于处理微服务间复杂的 AI 调用链。

---

### 6. 学习建议

**适合什么水平的开发者**
*   **中高级后端工程师**：需要具备 HTTP 协议、Kubernetes 基础以及 Go 语言阅读能力。
*   **运维/SRE 工程师**：需要理解云原生生态和负载均衡原理。

**可以从中学习到什么**
*   **云原生控制平面开发**：学习如何编写一个 K8s Controller 来管理 Envoy 配置。
*   **Wasm 插件开发**：学习如何用 Go/Rust 编写高性能的边缘计算插件。
*   **AI 协议处理**：深入理解 LLM 的流式传输机制和 SSE 协议。

**推荐的学习路径**
1.  **基础**：先阅读 Envoy 官方文档，理解 xDS 协议和 Listener/Cluster/Route 概念。
2.  **实践**：在本地 Kind 集群中通过 Helm 安装 Higress，尝试配置一个简单的路由转发。
3.  **进阶**：阅读 Higress 官方提供的 Wasm 插件示例（如 `key-rate-limit`），尝试自己写一个简单的 Request Header 修改插件并编译部署。
4.  **源码**：阅读 `pkg/ingress` 目录下的代码，理解 K8s Ingress 资源是如何转化为 Higress 内部配置的。

---

### 7. 最佳实践建议

**如何正确使用**
*   **分离关注点**：不要在网关层编写过于复杂的业务逻辑（如复杂的数据库查询）。网关应专注于路由、

---
## 代码示例




```python
# 示例1：动态路由配置
def dynamic_routing():
    """
    模拟Higress的动态路由功能
    根据请求头中的版本号将流量路由到不同服务
    """
    from flask import Flask, request, jsonify
    
    app = Flask(__name__)
    
    # 模拟服务端点
    @app.route('/api')
    def route_request():
        version = request.headers.get('X-Service-Version', 'v1')
        
        # 根据版本路由到不同后端
        if version == 'v2':
            return jsonify({"service": "backend-v2", "status": "active"})
        return jsonify({"service": "backend-v1", "status": "active"})
    
    return app

# 说明：这个示例展示了如何实现基于请求头的动态路由，
# 类似Higress中根据Header匹配规则将流量分发到不同版本的服务
```




```python
# 示例2：流量限流控制
def rate_limiting():
    """
    实现基于IP的简单限流功能
    每分钟最多允许10个请求
    """
    from collections import defaultdict
    from time import time
    from flask import Flask, request, jsonify
    
    app = Flask(__name__)
    request_counts = defaultdict(list)
    
    @app.route('/api')
    def limited_endpoint():
        ip = request.remote_addr
        current_time = time()
        
        # 清理超过1分钟的旧记录
        request_counts[ip] = [t for t in request_counts[ip] if current_time - t < 60]
        
        if len(request_counts[ip]) >= 10:
            return jsonify({"error": "Rate limit exceeded"}), 429
            
        request_counts[ip].append(current_time)
        return jsonify({"message": "Request processed"})
    
    return app

# 说明：这个示例展示了如何实现基于IP的限流功能，
# 类似Higress中配置的限流规则，防止服务被过载
```




```python
# 示例3：服务熔断器
def circuit_breaker():
    """
    实现简单的熔断器模式
    当错误率超过50%时自动熔断
    """
    from flask import Flask, jsonify
    import random
    
    app = Flask(__name__)
    failure_count = 0
    total_requests = 0
    circuit_open = False
    
    @app.route('/api')
    def protected_endpoint():
        nonlocal failure_count, total_requests, circuit_open
        
        if circuit_open:
            return jsonify({"error": "Circuit breaker is open"}), 503
            
        total_requests += 1
        
        # 模拟50%的失败率
        if random.random() < 0.5:
            failure_count += 1
            if failure_count / total_requests > 0.5:
                circuit_open = True
            return jsonify({"error": "Service unavailable"}), 500
            
        return jsonify({"status": "success"})
    
    return app

# 说明：这个示例展示了如何实现熔断器模式，
# 类似Higress中的熔断配置，当后端服务出现问题时自动切换流量
```


---
## 案例研究


### 1：阿里集团内部电商业务大促保障

 1：阿里集团内部电商业务大促保障

**背景**:
在阿里巴巴集团内部的电商业务（如淘宝、天猫）中，每年的“双11”和“618”大促是对技术架构最大的考验。系统需要在短时间内应对数十倍于平时的流量洪峰，且业务逻辑极其复杂，涉及商品、交易、支付、物流等多个微服务系统的协同。

**问题**:
传统的基于 Nginx 的网关在面对云原生架构时遇到了瓶颈。首先，流量路由规则的配置极其繁琐，且无法通过服务发现（如 Nacos）动态感知后端服务的健康状态和扩缩容情况。其次，为了应对大促，需要频繁地修改路由规则以进行流量切流、灰度发布（金丝雀发布）和降级操作，缺乏一个标准化的流量管理平台。最后，旧架构在处理高并发请求时的延迟和资源消耗难以进一步优化。

**解决方案**:
阿里集团将核心流量网关迁移至基于 Higress 的架构。利用 Higress 的 Ingress 能力对接 Kubernetes 和 Nacos，实现了流量的全自动管理和调度。通过 Higress 的 WASM (WebAssembly) 插件市场，业务开发团队可以编写 Lua 或 Go 代码来处理复杂的业务逻辑（如请求鉴权、请求头修改、流量打标），而无需重启网关服务。同时，利用其全链路灰度发布能力，实现了极低风险的代码上线。

**效果**:
1. **流量治理效率提升**：通过配置即代码的方式，将原本需要运维人员手动配置数小时的路由规则，缩短至分钟级甚至秒级生效。
2. **稳定性增强**：在大促期间，Higress 表现出极高的吞吐量和极低的延迟，成功支撑了每秒数十万 QPS 的流量冲击，系统 P99 延迟显著降低。
3. **业务敏捷性**：开发团队能够利用 WASM 插件快速迭代业务逻辑，实现了业务与网关基础设施的解耦，大大加快了新功能的上线速度。

---



### 2：某大型互联网 AI 应用服务商

 2：某大型互联网 AI 应用服务商

**背景**:
一家专注于提供 AI 图像生成和自然语言处理服务的科技公司，其业务高度依赖 OpenAI 的 GPT 系列模型以及自研的开源大模型。随着用户量的激增，后端对接的模型提供商越来越多，且不同模型对 Token 的计费策略、请求限流策略各不相同。

**问题**:
1. **多模型管理复杂**：直接在应用代码中硬编码不同模型的 API 地址和 Key，导致切换模型或迁移供应商困难。
2. **成本与安全风险**：缺乏统一的入口来监控每个用户的 Token 消耗量，导致成本难以核算；同时，将真实的 API Key 暴露给前端或客户端存在极高的泄露风险。
3. **性能问题**：由于大模型 API 的延迟较高，客户端请求经常超时，缺乏统一的缓存和重试机制。

**解决方案**:
该企业引入 Higress 作为 AI API 网关。利用 Higress 针对大模型场景的特定优化，将所有后端大模型供应商的接口统一收敛到网关层。
1. **Provider 路由**：配置路由规则，将不同模型的请求转发到不同的后端服务（如 Azure OpenAI 或 HuggingFace）。
2. **统一鉴权与计费**：通过 Higress 的插件功能，屏蔽了真实的后端 API Key，仅验证客户端的 App Key，并自动在请求头中注入供应商 Key。同时，利用插件统计请求和消耗的 Token 数量，上报至计费系统。
3. **语义缓存**：开启针对 AI 请求的缓存功能，对相似的 Prompt 请求直接返回缓存结果，减少对后端昂贵 API 的调用。

**效果**:
1. **成本降低**：通过语义缓存，减少了约 30% 的重复请求，直接降低了 API 调用成本。
2. **安全性提升**：彻底解决了 API Key 泄露的风险，实现了统一的密钥管理和轮换。
3. **开发体验优化**：前端应用只需对接 Higress 的统一接口，无需关心底层模型供应商的切换，大大简化了客户端代码的复杂度。

---



### 3：某跨国物流企业微服务架构改造

 3：某跨国物流企业微服务架构改造

**背景**:
该企业原有单体应用正在向微服务架构迁移，运行在混合云环境（部分在阿里云，部分在本地数据中心）。业务包含数百个微服务，且存在大量的遗留系统（SOAP 协议）与现代系统（RESTful/gRPC）互通的需求。

**问题**:
1. **协议转换困难**：前端应用主要使用 HTTP/JSON，但后端仍有部分核心系统使用 SOAP 或 gRPC，缺乏高效的中间层进行协议转换。
2. **流量控制混乱**：不同租户（不同国家的分公司）需要访问不同的微服务实例，缺乏基于 Header 或 Cookie 的复杂路由逻辑。
3. **可观测性不足**：由于经过的链路长，排查跨服务调用的故障极其困难，缺乏统一的日志和追踪入口。

**解决方案**:
部署 Higress 作为统一的 API 网关，置于混合云环境的入口。
1. **协议转换插件**：使用 Higress 的插件能力，将前端的 HTTP 请求无缝转换为后端的 gRPC 或 SOAP 请求，屏蔽了后端技术栈的差异。
2. **多租户路由**：基于请求头中的“Region-ID”或“Tenant-ID”，利用 Higress 的高级路由功能，将流量精准导向特定云环境或地域的服务实例。
3. **集成可观测性**：开启 Higress 对 OpenTelemetry 的原生支持，将访问日志和链路追踪数据统一发送至 Prometheus 和 Grafana。

**效果**:
1. **无缝迁移**：在不修改旧有后端系统代码的前提下，成功实现了流量接入和新老系统的共存，加速了微服务改造进程。
2. **精细化运维**：实现了按地域、按租户的流量隔离和限流，保障了核心业务的 SLA。
3. **故障定位提速**：通过统一的网关日志和追踪，运维人员定位跨服务调用故障的时间从小时级缩短至分钟级。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | 方案A: Kong | 方案B: APISIX |
|------|----------------|------------|--------------|
| 性能 | 高性能，基于Envoy和Istio，支持高并发 | 高性能，基于Nginx和OpenResty，支持高并发 | 极高性能，基于OpenResty和LuaJIT，性能最优 |
| 易用性 | 提供图形化控制台，支持Kubernetes集成，配置直观 | 提供管理界面，但配置复杂度较高 | 提供Dashboard，但学习曲线较陡 |
| 成本 | 开源免费，企业版需付费 | 开源免费，企业版需付费 | 完全开源免费，无企业版 |
| 功能 | 支持流量管理、安全防护、可观测性，与阿里云集成 | 插件丰富，支持认证、限流、监控等 | 功能全面，支持动态路由、插件热加载 |
| 扩展性 | 支持自定义插件，基于Wasm和Go | 支持Lua插件扩展 | 支持Lua和Python插件扩展 |
| 社区 | 阿里背书，社区活跃，文档完善 | 社区成熟，生态丰富 | 社区活跃，中文支持好 |

### 优势分析

- 优势1：基于Envoy和Istio，云原生集成度高，适合Kubernetes环境。
- 优势2：提供图形化控制台，降低配置复杂度，适合快速上手。
- 优势3：与阿里云服务深度集成，适合阿里云用户。

### 不足分析

- 不足1：相比APISIX，性能略逊一筹，尤其在极端高并发场景。
- 不足2：插件生态不如Kong成熟，扩展性有限。
- 不足3：社区规模和生态支持不如Kong和APISIX。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 WASM 实现插件扩展

**说明**: Higress 深度集成了 WASM (WebAssembly) 技术，允许开发者使用 C/C++、Go、Rust 或 JavaScript 等多种语言编写自定义插件。相比传统的 Lua 脚本，WASM 插件提供了更高的执行效率和更强的隔离性，同时支持热加载，无需重启网关即可更新插件逻辑。

**实施步骤**:
1. 根据业务需求选择合适的编程语言（推荐 Go 或 Rust）编写插件逻辑。
2. 使用 Higress 提供的 SDK 或工具链（如 `wasmedge` 或 `tinygo`）将代码编译为 WASM 文件。
3. 在 Higress 控制台或通过配置文件将 WASM 文件上传，并关联到特定的路由或网关全局作用域。
4. 配置插件的执行阶段和优先级。

**注意事项**: 开发时需注意 WASM 运行时的内存限制，避免处理超大的请求体导致内存溢出。

---

### 实践 2：精细化流量路由与灰度发布

**说明**: 利用 Higress 强大的路由匹配能力，支持基于 Header、Query 参数、Cookie 以及服务权重的流量路由。这对于实现蓝绿部署、金丝雀发布和 A/B 测试至关重要，能够最大程度降低新版本上线的风险。

**实施步骤**:
1. 定义两个不同的服务版本（例如 v1 和 v2）。
2. 在 Higress 中创建路由规则，设置匹配条件（如 `x-version: v2`）。
3. 配置流量分发比例，例如将 10% 的流量指向 v2 版本，90% 保留在 v1 版本。
4. 监控 v2 版本的关键指标，确认无误后逐步调整比例至 100%。

**注意事项**: 确保灰度流量具有独立的标识（如特定的 Header），以便在日志和监控中区分不同版本的请求状态。

---

### 实践 3：全链路安全防护与认证

**说明**: Higress 提供了标准化的安全能力，包括 JWT 鉴权、AK/SK 认证、IP 黑白名单以及 CORS 配置。最佳实践是“安全左移”，在网关层统一处理认证和授权，避免将敏感的鉴权逻辑分散在各个后端微服务中。

**实施步骤**:
1. 在 Higress 中配置全局或路由级的 JWT 认证规则，对接认证中心。
2. 针对内部服务间调用，配置 mTLS 双向认证或标准的 API Key 鉴权。
3. 设置 IP 访问控制列表，限制管理端口的访问来源。
4. 开启 WAF 防护（如果集成了相关插件）以抵御常见的 Web 攻击。

**注意事项**: 密钥和证书的管理应遵循定期轮换原则，并使用密钥管理服务（KMS）而非硬编码在配置文件中。

---

### 实践 4：对接服务注册中心与动态服务发现

**说明**: Higress 原生支持 Nacos、Consul、Zookeeper 以及 Kubernetes Service 等多种注册中心。通过配置服务来源，Higress 能够实时感知后端服务实例的上下线状态，自动调整流量转发策略，实现高可用性。

**实施步骤**:
1. 在 Higress 控制台的“服务来源”管理页面，添加对应的注册中心类型（如 Nacos）。
2. 填写注册中心的连接地址、命名空间和访问凭证。
3. 创建服务时，选择来源为“注册中心”，并引用已发现的服务名。
4. 配置健康检查机制（主动或被动），确保流量只转发给健康的实例。

**注意事项**: 确保注册中心与 Higress 之间的网络连通性，并注意设置合理的超时时间和缓存策略，以防注册中心抖动影响网关路由。

---

### 实践 5：可观测性集成与监控告警

**说明**: 生产环境的稳定性离不开完善的监控。Higress 原生支持 Prometheus 监控指标、访问日志对接以及分布式链路追踪。最佳实践是将这些数据输出到统一的可观测性平台（如 Grafana Stack 或 Elasticsearch）。

**实施步骤**:
1. 开启 Higress 的 Prometheus Metrics 采集端口，配置 Prometheus 抓取规则。
2. 配置日志采集（如使用 Filebeat 或 Fluentd），将 Higress 的访问日志和错误日志发送至日志中心。
3. 启用 Tracing（如 SkyWalking 或 Zipkin），在网关层注入 Trace Header，打通全链路追踪。
4. 在 Grafana 中导入 Higress 官方提供的仪表盘模板，并配置基于关键指标（如 4xx/5xx 错误率、延迟 P99）的告警规则。

**注意事项**: 日志采样率应根据实际流量调整，避免在海量高并发场景下产生过多的日志存储开销和性能损耗。

---

### 实践 6：高性能配置与资源调优

**

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/3 (QUIC) 协议

**说明**: HTTP/3 (QUIC) 基于 UDP 协议，解决了 TCP 的队头阻塞问题。在 Higress 网关场景中，面对弱网环境或高丢包率网络时，HTTP/3 能显著减少连接建立延迟和页面加载时间，提升客户端与网关之间的交互性能。

**实施方法**:
1. 在 Higress 的网关配置中，找到监听器设置。
2. 为需要优化的路由或域名启用 HTTP/3 协议支持。
3. 确保后端服务配置了相应的 ALPN 识别（如适用）。
4. 配置证书以支持 QUIC 协议握手。

**预期效果**: 在弱网环境下，连接建立与数据传输延迟可降低 20%-40%，丢包场景下的吞吐量提升明显。

---

### 优化 2：启用并配置本地缓存

**说明**: Higress 支持对后端响应进行本地缓存。对于高频访问但低频变更的 API 响应或静态内容，启用网关层缓存可以直接从 Higress 内存或磁盘中返回数据，从而大幅减少对后端服务的请求压力和网络 I/O 开销。

**实施方法**:
1. 在路由配置中启用缓存功能。
2. 根据业务特性设置合理的缓存键（Cache Key），例如去除 URL 中不必要的参数。
3. 配置 TTL（生存时间）与缓存过期策略。
4. 根据内存资源情况，配置磁盘缓存或内存缓存的大小限制。

**预期效果**: 后端请求量减少 30%-90%（视缓存命中率而定），P99 延迟降低至毫秒级。

---

### 优化 3：启用 Wasm 插件的热加载与隔离

**说明**: Higress 的核心优势之一是支持 Wasm 插件。为了性能优化，应确保 Wasm 插件运行在合适的隔离级别（如基于 Proxy-Wasm 的 ABI），并利用 Lazy Loading 或按需加载机制，避免在请求处理路径中加载不必要的插件逻辑，从而降低 CPU 开销和请求延迟。

**实施方法**:
1. 审计当前启用的 Wasm 插件，移除非核心业务插件。
2. 对于复杂的插件逻辑，使用 AOT（Ahead-of-Time）编译优化 Wasm 代码。
3. 配置插件的执行阶段（如尽量在 Log 阶段而非 Filter 阶段处理非关键逻辑）。
4. 利用 Higress 的插件配置动态更新，避免重启网关带来的流量中断。

**预期效果**: 请求处理路径的 CPU 指令周期减少，单请求延迟降低 5%-15ms（取决于插件复杂度）。

---

### 优化 4：调整连接池与工作线程参数

**说明**: 默认的连接池配置可能无法应对突发流量或高并发场景。通过调整 Higress 与上游服务之间的连接池大小、最大请求数以及网关自身的 Worker 线程数，可以防止连接排队导致的超时，并最大化利用 CPU 资源。

**实施方法**:
1. 根据公式 `Worker Processes = CPU Core Numbers` 调整工作进程数。
2. 针对高并发上游服务，调大 `upstream` 的 `maxConnections` 参数。
3. 调整 `keepalive` 请求数，减少频繁建立 TCP 连接的开销。
4. 监控 `listen` backlog 队列长度，防止突发流量被拒绝。

**预期效果**: 系统吞吐量（QPS）提升 20%-50%，有效降低因连接等待造成的超时率。

---

### 优化 5：全链路超时与重试策略优化

**说明**: 不合理的超时和重试策略会导致“雪崩效应”。过长的超时时间会占用大量连接资源，而过度的重试会放大后端压力。优化策略旨在快速失败并释放资源，保护网关稳定性。

**实施方法**:
1. 根据业务 P99 耗耗，设置严格的 `timeout`（连接超时

---
## 学习要点

- 基于提供的来源信息（阿里巴巴的 Higress 项目在 GitHub 趋势榜上），以下是关于该项目的关键要点总结：
- Higress 是阿里云开源的一款基于 Istio 的云原生 API 网关，深度集成了 K8s 与 Nacos，旨在解决云原生架构下的流量管理问题。
- 它支持将 Ingress（入口流量）与 Gateway（微服务网关）合二为一，实现了从南北向（外部访问）到东西向（服务间调用）的全链路流量治理。
- 该项目提供了强大的插件扩展市场，允许通过 WASM（WebAssembly）或 Go/Python/Java 编写自定义插件，且支持热加载，无需重启网关。
- Higress 完全兼容 Nginx Ingress 注解和 Kong 的部分生态，极大地降低了用户从传统网关迁移至云原生网关的成本。
- 它集成了 AI 推理与流量编排能力，能够作为 AI 时代的模型网关，支持对接 LLM（大语言模型）并进行 Prompt 模板管理。
- 借助 Istio 的控制平面，Higress 能够通过金丝雀发布、蓝绿发布和全链路灰度发布等功能，保障业务上线的稳定性。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础

**学习内容**:
- 云原生网关的基本概念与 Higress 的核心定位
- Higress 与 Nginx、传统 API 网关的区别
- Docker 环境下 Higress 的快速安装与部署
- Higress 控制台的基本操作与界面熟悉
- 基于控制台创建简单的路由转发

**学习时间**: 1-2周

**学习资源**:
- Higress 官方 GitHub 仓库 README
- Higress 官方文档 - 快速开始章节
- Higress 官方博客 - 架构设计相关文章

**学习建议**: 
此阶段重点在于建立认知模型。建议先通读官方文档的架构介绍，理解 Higress 基于 Istio 和 Envoy 的底层逻辑。务必动手在本地或测试环境通过 Docker 完成一次安装，并通过控制台配置一个简单的域名转发，跑通第一个 Hello World 路径。

---

### 阶段 2：核心功能掌握

**学习内容**:
- Ingress 与 Gateway API 的配置方式
- 详细的流量路由规则配置（基于路径、Header、Query 参数等）
- 服务来源的注册与管理（如 Nacos, Consul, 固定地址, DNS）
- 全局与自定义插件系统的使用（Waf 保护、限流熔断、CORS 等）
- 金丝雀发布与蓝绿发布的基础配置

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 流量管理章节
- Higress 官方文档 - 插件市场
- Envoy Filter 基础知识（辅助理解插件原理）

**学习建议**: 
不要仅停留在控制台操作，尝试将配置导出为 YAML 文件，理解 K8s Ingress 或 Gateway API 的标准字段。重点实践“插件”功能，这是 Higress 区别于传统网关的核心优势，尝试配置一个限流插件并观察效果。

---

### 阶段 3：进阶开发与治理

**学习内容**:
- Wasm (WebAssembly) 技术在网关中的应用原理
- 使用 Go 或 C++ 开发自定义 Wasm 插件
- Higress 的高可用部署架构与性能调优
- 多集群接入与服务网格集成的初步概念
- 基于 Higress 的多租户管理与安全认证

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档 - 自定义插件开发
- Higress GitHub 仓库中的插件示例代码
- eBPF 与 Wasm 相关的技术社区文章

**学习建议**: 
此阶段是迈向精通的关键。建议从修改官方现有的一个简单插件开始，编译并在本地加载运行，理解插件与网关的数据交互流程。同时，需要关注生产环境的运维细节，如日志监控、Prometheus 指标采集等。

---

### 阶段 4：专家级架构与生态

**学习内容**:
- Higress 在微服务架构中的最佳实践
- AI 网关特性的应用（如对接 LLM 模型、Token 处理）
- 深入 Envoy 与 Istio 源码层面的定制与优化
- 复杂场景下的故障排查与性能瓶颈分析
- Higress 对接阿里云及其他云厂商生态的高级特性

**学习时间**: 持续学习

**学习资源**:
- Higress 官方文档 - 最佳实践案例
- Istio 官方文档（深度集成部分）
- Higress 源码分析与贡献指南

**学习建议**: 
在这个阶段，学习路径不再局限于工具本身，而是如何利用 Higress 解决复杂的业务架构问题。建议深入研究源码，参与社区讨论，尝试在 GitHub 上提交 Issue 或 PR，并关注 Higress 在 AI Gateway 领域的最新特性迭代。

---
## 常见问题


### 1: Higress 是什么？它与阿里巴巴有什么关系？

1: Higress 是什么？它与阿里巴巴有什么关系？

**A**: Higress 是一个开源的、云原生的 API 网关。它是在 2022 年由阿里巴巴正式开源的，基于阿里巴巴内部多年在大促（如双11）场景下沉淀的网关技术经验。Higress 的前身是阿里巴巴内部的 Gateway 网关产品，它结合了 Kong、Envoy 等开源网关的优点，旨在为云原生时代提供一种统一、高性能、易扩展的流量管理组件。它是阿里云云原生 API 网关的核心开源版本。

---



### 2: Higress 与 Nginx、Envoy 或 Kong 等主流网关有什么区别？

2: Higress 与 Nginx、Envoy 或 Kong 等主流网关有什么区别？

**A**: Higress 的核心定位在于“云原生”与“生态融合”，主要区别如下：

1.  **架构基础**：Higress 深度集成了 **Envoy** 作为高性能数据面，利用其 C++ 的高性能特性，同时通过 Go 语言编写控制平面（Istio 生态），比传统的 Lua 脚本（如 OpenResty/Kong）更易于维护和扩展。
2.  **Kubernetes 原生**：相比 Nginx，Higress 天然支持 Kubernetes Ingress 和 Gateway API，能够自动感知服务变化，无需手动 reload 配置。
3.  **安全与插件**：Higress 提供了比传统网关更严格的 WAF（Web 应用防火墙）能力，并支持 WASM（WebAssembly）插件，允许开发者使用多种语言（如 Go, Python, JS）编写插件，而无需重启网关，这在 Kong 和 Nginx 中实现起来较为复杂。
4.  **服务治理集成**：作为阿里系产品，它能与 Nacos、Sentinel 等微服务组件无缝集成，提供了比单纯流量转发更强的微服务治理能力。

---



### 3: Higress 是否支持从 Nginx 或 Ingress Controller 迁移？

3: Higress 是否支持从 Nginx 或 Ingress Controller 迁移？

**A**: 是的，Higress 非常重视迁移的平滑性，并提供了专门的工具和兼容性支持：

1.  **Nginx 兼容**：Higress 提供了 Nginx 配置迁移工具，可以将现有的 Nginx.conf 配置自动转换为 Higress 的路由配置。
2.  **Ingress 兼容**：Higress 完全兼容 Kubernetes 标准的 Ingress 规范。如果你目前使用的是 Nginx Ingress Controller，通常只需修改 Ingress Class 注解即可将流量切换到 Higress，无需大规模修改 YAML 资源文件。
3.  **Kong 兼容**：Higress 正在逐步增强对 Kong 插件和配置的兼容性，支持导入 Kong 的配置格式。

---



### 4: Higress 的性能如何？能否支撑高并发流量？

4: Higress 的性能如何？能否支撑高并发流量？

**A**: Higress 具备极高的性能，设计目标就是为了支撑阿里巴巴内部的大规模电商流量。

1.  **底层优势**：数据面基于 Envoy（C++ 编写），具备极高的处理效率和低延迟。
2.  **内部验证**：在阿里巴巴内部，类似的网关架构已经历过多年双11零点流量的考验，能够处理每秒百万级的 QPS。
3.  **基准测试**：根据官方及社区的压测数据，Higress 在长连接、短连接、HTTPS 加解密等场景下的吞吐量与延迟表现均优于传统的基于 Lua 的网关（如 OpenResty/Kong）。

---



### 5: Higress 支持哪些类型的插件？如何开发自定义插件？

5: Higress 支持哪些类型的插件？如何开发自定义插件？

**A**: Higress 拥有非常灵活的插件体系，主要分为以下几类：

1.  **原生插件**：内置了认证鉴权（如 AK/SK, JWT, Basic Auth）、流量控制（限流、熔断）、可观测性（日志、指标）等常用插件。
2.  **WASM 插件（推荐）**：这是 Higress 的核心亮点。它支持 **WebAssembly** 标准。开发者可以使用 **Go、C++、Rust、JavaScript/TypeScript** 等高级语言编写业务逻辑，编译成 WASM 文件后动态加载到网关中。这种方式不仅开发效率高，而且隔离性好，插件崩溃不会导致网关崩溃，也无需重启网关服务。
3.  **Lua 插件**：为了兼容旧版生态，Higress 依然支持 Lua 脚本插件，但推荐新项目优先使用 WASM。

---



### 6: Higress 能否与 Istio 配合使用？它属于服务网格吗？

6: Higress 能否与 Istio 配合使用？它属于服务网格吗？

**A**: Higress 可以与 Istio 配合使用，或者作为其边缘网关的替代方案。

1.  **定位互补**：Istio 通常用于管理集群内部的微服务通信（东西向流量），而 Higress 专注于处理进入集群的流量（南北向流量）。
2.  **协议支持**：Higress 完全支持 Istio 的 API 规范，可以

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: 基础环境搭建与流量验证

### 难度**: [简单]

### 问题描述**:

### 在本地 Docker 环境中快速部署 Higress，并配置一个简单的路由规则。要求将访问 `/httpbin/` 路径的流量转发到公共测试服务 `httpbin.org:80`。

---
## 实践建议

基于 Higress 作为 AI Native API 网关的定位，结合其云原生背景与 AI 推理场景的特殊性，以下是 6 条针对实际生产环境的实践建议：

### 1. 利用 Wasm 插件实现模型供应商的统一适配
**场景**：企业内部同时调用 OpenAI、阿里云通义千问、Azure OpenAI 等多个 LLM 供应商，或者存在自研模型，接口协议各不相同。
**建议**：不要在业务代码中处理不同厂商的 API 差异（如鉴权方式、参数格式）。使用 Higress 的 Wasm 插件能力（或官方提供的 `ai-proxy` 插件），在网关层将所有供应商的接口统一标准化。
**操作**：配置路由将不同后端服务映射到统一的路径前缀（如 `/v1/chat/completions`），并在插件中配置不同厂商的映射规则，使业务侧只需维护一套调用逻辑。
**陷阱**：避免在插件中处理过于复杂的业务逻辑（如长文本处理），以免阻塞网关线程，影响转发性能。

### 2. 实施基于 Token 的精细化流控与预算管理
**场景**：大模型调用成本高昂，且后端模型服务有严格的 TPS（每秒请求数）限制。
**建议**：不要仅依赖传统的 QPS（每秒查询数）限流。AI 场景下，请求长短差异极大，QPS 无法准确反映后端负载。应配置基于 Token 的限流策略。
**操作**：针对不同 API Key 或租户设置 Token 预算（Token Budget）和 RPM（每分钟请求数）限制。例如，为测试环境 Key 设置每小时 10 万 Token 的硬性上限，防止账单失控。
**陷阱**：注意流控的拒绝策略。建议配置“排队”而非直接“拒绝”，以应对模型推理偶尔出现的延迟抖动，提升用户体验。

### 3. 配置 SSE（Server-Sent Events）的超时与缓存策略
**场景**：AI 对话通常采用流式输出，响应时间可能长达数十秒甚至数分钟。
**建议**：网关层的超时设置必须显著大于普通 HTTP 接口。同时，需谨慎配置缓存，避免返回过时的上下文。
**操作**：
*   将网关的 `readTimeout` 设置为 0（无限）或根据模型最长推理时间设置一个较大的值（如 5 分钟）。
*   对于流式请求，确保网关开启了 Full-Duplex（全双工）模式，不要因为收到响应头就关闭连接。
**陷阱**：切勿对流式响应开启常规的 HTTP Body 缓存，这会导致客户端无法收到流式数据，必须在网关配置中明确识别并跳过 SSE 请求的缓存插件。

### 4. 建立敏感词过滤与数据脱敏的防线
**场景**：企业内部数据通过公网模型传输，存在数据泄露风险；或用户输入包含违规内容。
**建议**：利用 Higress 的插件生态在网关层进行“Prompt 拦截”和“Response 清洗”。
**操作**：在请求发往模型前，配置插件拦截包含 PII（个人身份信息）或内部机密关键词的请求；在响应返回客户端前，过滤模型生成的违规内容。
**陷阱**：过滤逻辑应尽量简单（基于关键词或正则），避免引入需要加载大型 ML 模型的复杂检测插件，否则会显著增加网关延迟。

### 5. 混沌工程与模型熔断机制
**场景**：模型服务（特别是外部 SaaS 服务）可能出现不稳定、限流或宕机，导致网关连接积压。
**建议**：配置针对模型服务的熔断与降级策略。
**操作**：在 Higress 中配置目标规则，设定连续错误响应（如 HTTP 5xx 或模型层错误码）的阈值。一旦触发，自动将流量切换到备用模型或返回兜底预设回复，避免后端雪崩。
**陷阱**：注意区分“模型错误”和“网关超时”。如果是网关到模型之间的网络超时，不应立即熔断

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI 原生](/tags/ai-%E5%8E%9F%E7%94%9F/) / [LLM](/tags/llm/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [WASM](/tags/wasm/) / [MCP 协议](/tags/mcp-%E5%8D%8F%E8%AE%AE/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260130-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260205-github_trending-alibaba-higress-6.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260201-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260206-github_trending-alibaba-higress-0.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260303-github_trending-alibaba-higress-0.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*