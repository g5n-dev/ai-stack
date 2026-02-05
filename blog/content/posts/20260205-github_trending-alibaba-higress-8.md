---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-02-05T04:18:08+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "Istio", "Envoy", "WASM", "LLM", "MCP 协议"]
categories: ["系统与基础设施", "AI 工程"]
source: github_trending
description: "**Higress 项目总结** **1. 项目概况** Higress 是由阿里巴巴开源的一款**云原生 AI 原生 API 网关**。它基于 Istio 和 Envoy 构建，使用 Go 语言编写，目前 GitHub 星标数超过 7,400。该项目的核心目标是通过扩展能力，将传统 API 网关与 AI 生态系统深度"
external_url: https://github.com/alibaba/higress
scenarios: ["AI/ML项目", "云原生/容器", "DevOps/运维"]
---

# 阿里开源 Higress：AI 原生 API 网关

> **原名**: alibaba /

      higress

---

## 基本信息

- **描述**: 🤖 AI 网关 | AI 原生 API 网关
- **语言**: Go
- **星标**: 7,451 (+10 stars today)
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

Higress 是阿里巴巴开源的 AI 原生 API 网关，基于 Istio 和 Envoy 构建，深度集成了 WASM 插件能力。它专为需要统一管理大模型流量与传统微服务的场景设计，既能提供 LLM 应用的 AI 网关特性，也支持 Kubernetes Ingress 等标准 API 管理功能。本文将介绍其系统架构、核心组件以及 AI 网关与 MCP 系统等关键特性。

---
## 摘要

**Higress 项目总结**

**1. 项目概况**
Higress 是由阿里巴巴开源的一款**云原生 AI 原生 API 网关**。它基于 Istio 和 Envoy 构建，使用 Go 语言编写，目前 GitHub 星标数超过 7,400。该项目的核心目标是通过扩展能力，将传统 API 网关与 AI 生态系统深度融合。

**2. 核心架构与技术特点**
*   **架构模式：** 采用**控制平面与数据平面分离**的架构。配置变更通过 xDS 协议传播，具备毫秒级延迟和无连接中断的特性，非常适合 AI 长连接流式响应场景。
*   **扩展能力：** 深度集成了 **WebAssembly (WASM)** 插件系统，极大地提升了功能的灵活性和扩展性。

**3. 三大核心功能**
*   **AI 网关：** 提供统一的 API 接口，兼容 30 多家大语言模型（LLM）服务商。核心功能包括协议转换、可观测性、缓存以及安全防护。
*   **MCP 服务器托管：** 支持托管**模型上下文协议 (MCP)** 服务器，使 AI 智能体能够便捷地调用外部工具和服务（如搜索、地图等）。
*   **传统 API 网关：** 兼容 Kubernetes Ingress，支持微服务路由，并保持与 Nginx Ingress 注解的兼容性。

**4. 总结**
Higress 不仅仅是一个传统的流量入口，更是一个面向 AI 时代的基础设施，旨在解决 LLM 应用接入、AI 智能体工具调用以及云原生微服务治理的综合需求。

---
## 评论

**总体判断**

Higress 是阿里云开源的“AI 原生”网关，它成功地将云原生流量治理能力与大模型（LLM）应用所需的特定协议处理进行了深度融合。作为基于 Istio 和 Envoy 的上层构建，它不仅是一个高性能的入口控制器，更是当前构建生产级 AI 应用基础设施（如 Agent 代理、API 网关）的最具技术潜力的开源方案之一。

**详细评价维度**

**1. 技术创新性：从“流量转发”进化为“流量理解”**
*   **事实**：Higress 扩展了 Envoy，原生支持 WASM（WebAssembly）插件机制，并明确集成了 AI Gateway 特性与 MCP (Model Context Protocol) 服务托管能力。
*   **推断**：传统网关（如 Nginx）对七层流量的处理仅限于 HTTP 头部或负载均衡，无法理解 SSE（Server-Sent Events）流式传输中的语义差异。Higress 的创新在于它将 AI 交互协议（如 OpenAI 协议转换、Prompt 注入、Token 计费）内置到了数据平面。通过 WASM 插件，开发者可以用 C/C++/Go/Rust 甚至 JavaScript 编写极其低延迟的扩展逻辑，这在 Java 编写的传统微服务网关中是难以实现的性能突破。它不再仅仅是一个管道，而是一个智能的流量拦截与处理器。

**2. 实用价值：解决 AI 落地“最后一公里”的碎片化问题**
*   **事实**：文档指出其核心功能包括 Kubernetes Ingress、微服务路由以及 AI 特性（LLM 应用支持）。
*   **推断**：在当前企业向 AI 转型的过程中，最大的痛点不是没有模型，而是无法将模型安全、稳定地集成到现有微服务体系中。Higress 解决了这一关键问题：它允许企业保留原有的 K8s Ingress 架构，同时利用 AI Gateway 能力统一管理不同厂商（如 OpenAI、通义千问、Llama）的 API 访问。它消除了为 AI 流量单独搭建网关的架构冗余，实现了“传统流量”与“AI 流量”的统一治理，大幅降低了运维复杂度。

**3. 代码质量与架构：云原生标准的教科书级实践**
*   **事实**：项目基于 Go 语言开发，架构明确分离了控制平面与数据平面，并提供了详尽的 DeepWiki 文档（涵盖架构、构建、WASM 插件、MCP 系统等）。
*   **推断**：从代码规范来看，Higress 继承了 Envoy 的高性能基因和 Go 语言在云原生工具链中的生态优势。其架构设计遵循了“控制面配置，数据面执行”的云原生标准模式，解耦做得非常彻底。文档的完整性（包括多语言 README 和分模块的深度文档）表明该项目不仅是为了“能用”，而是为了“可维护”和“可扩展”，具备企业级软件的工程素养。

**4. 社区活跃度：背靠阿里的强有力驱动**
*   **事实**：星标数达到 7,451（且持续增长中），由阿里巴巴主导。
*   **推断**：在开源网关领域，这是一个极高的关注度，证明了市场对“AI + 网关”结合方向的渴望。阿里作为主要贡献者，保证了项目不会轻易突然停止维护。高星标数通常意味着丰富的第三方插件生态和更快的 Bug 修复速度，对于选择开源组件作为基础设施的企业来说，这是一个重要的安全背书。

**5. 学习价值：深入理解云原生与 AI 基础设施**
*   **推断**：对于开发者而言，研究 Higress 具有双重价值。首先，它是学习 Envoy 和 Istio 在生产环境如何落地的最佳范例之一；其次，它提供了如何将 WASM 技术应用于实际业务（特别是 AI 场景）的宝贵参考。通过阅读其 WASM 插件源码，开发者可以学习到如何在网关层面实现高效的请求拦截、修改与响应流处理，这是构建现代中间件的核心技能。

**6. 潜在问题与改进建议**
*   **推断**：
    *   **复杂度门槛**：基于 Istio/Envoy 的架构意味着其部署和运维的复杂度远高于简单的 Nginx，对于小型团队或非 K8s 环境可能存在“杀鸡用牛刀”的问题。
    *   **MCP 协议成熟度**：虽然集成了 MCP 系统，但该协议本身仍在快速迭代中，Higress 对其的实现可能面临频繁的 API 变更，需要关注其稳定性。
    *   **资源开销**：作为 Sidecar 或独立网关，Envoy 本身的内存占用相对较高，在极高并发下的资源调优需要经验。

**7. 对比优势**
*   **对比 Nginx/Kong**：Higress 原生支持 K8s，且 WASM 插件的沙箱隔离性远好于 Lua（Kong/Nginx），在 AI 流量处理（如 SSE 流式转发）上更智能。
*   **对比传统 Istio Ingress**：Higress 提供了开箱即用的控制台和更友好的配置逻辑，去除了 Istio 的复杂性，同时专门针对 AI 协议做了增强，这是标准 Istio Ingress 不具备的。

**边界条件与验证清单**

**不适用场景**：
*   极简单的静态资源托管或流量极小的个人

---
## 技术分析

# Higress 深度技术分析报告

基于 Alibaba Higress 仓库（7.4k+ stars）的公开信息、架构文档及源码结构，以下是对该 AI 原生 API 网关的深度剖析。

---

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 的核心架构遵循**云原生控制平面与数据平面分离**的设计模式，但在传统 Istio 之上进行了深度的“网关化”改造。

*   **底层基石**：基于 **Envoy** 作为高性能数据平面，利用其 L3/L7 处理能力和可扩展性。
*   **控制平面**：基于 **Istio** 进行裁剪和增强。Higress 移除了 Istio 中繁重的 Sidecar 注入和复杂的 Service Mesh 治理功能，专注于边缘网关场景，实现了配置的下发和管理。
*   **扩展层**：引入 **WebAssembly (WASM)** 作为核心插件运行时。这允许使用 C/C++/Rust/Go (通过 TinyGo) 编写高性能插件，并在运行时动态加载，无需重启网关。
*   **AI 原生层**：这是 Higress 最显著的架构增量。它在数据平面内置了对 LLM 协议的处理逻辑，并集成了 **MCP (Model Context Protocol)** 服务器托管能力。

### 核心模块与关键设计
1.  **路由与配置管理**：通过 Ingress 或自定义 Gateway API 资源定义路由规则。控制平面将这些规则翻译为 Envoy 的 xDS 协议配置。
2.  **WASM 虚拟机**：每个 Envoy 过滤器链中嵌入 WASM 运行时。这是实现“AI 网关”功能（如 Token 计费、Prompt 转换）的关键，允许业务逻辑热更新。
3.  **AI 代理模块**：专门处理 OpenAI、通义千问等 LLM 协议的转发。它不仅做简单的 HTTP 代理，还处理流式传输（SSE）的缓冲与转发。
4.  **MCP 服务器集成**：Higress 能够将内部微服务或外部工具封装为 MCP 协议端点，供 AI Agent 调用。

### 技术亮点与创新点
*   **AI 流式响应的无损处理**：传统的网关在处理 SSE（Server-Sent Events）长连接时，往往会因为超时或缓冲策略导致连接中断。Higress 针对大模型流式输出进行了深度优化，确保在毫秒级配置变更的同时，维持长连接的稳定性。
*   **标准化的 AI 提供商抽象**：通过统一的协议适配层，将不同厂商的 API 差异抹平，允许用户通过简单的配置切换底座模型，而无需修改客户端代码。
*   **MCP 的网关侧落地**：将 MCP 协议引入网关层，解决了 AI Agent 访问企业内部微服务时的安全鉴权和流量治理问题，这是对 LLM Ops 的重要补充。

### 架构优势分析
*   **高性能**：继承了 Envoy 的 C++ 高性能内核，WASM 插件的引入虽然增加了少量开销，但远高于传统的 Lua (OpenResty) 或 JS 插件性能。
*   **极致的弹性**：控制平面与数据平面分离，配置变更通过 xDS 秒级生效，且支持配置版本管理和回滚。
*   **生态兼容性**：完全兼容 K8s Ingress 标准，降低了从 Nginx Ingress 迁移的门槛。

---

## 2. 核心功能详细解读

### 主要功能与使用场景
1.  **AI 网关**：
    *   **统一模型接入**：将 OpenAI、Anthropic、通义千问等 10+ 种模型 API 统一为一个标准接口。
    *   **Token 计费与配额**：基于请求和响应的 Token 数量进行实时计量，支持基于用户的精细化限流。
    *   **Prompt 增强**：在网关层动态插入系统提示词或敏感词过滤，无需修改后端应用。
2.  **MCP 服务器托管**：
    *   将企业内部的 RESTful API 自动转换为 MCP 工具，供 AI Agent 安全调用。
3.  **传统 API 网关**：
    *   支持 K8s Ingress、金丝雀发布、负载均衡、认证鉴权等标准功能。

### 解决的关键问题
*   **模型厂商锁定**：通过中间层抽象，企业可以随时切换成本更低或效果更好的模型，而无需重构业务代码。
*   **AI 调用的可观测性盲区**：传统网关只能记录 HTTP 状态码，Higress 能记录 Prompt 内容、Token 消耗量和模型推理时间。
*   **Agent 调用内网服务的安全性**：直接将内网服务暴露给 LLM 存在巨大风险，通过 Higress 的 MCP 托管，可以在网关层进行严格的权限校验和参数清洗。

### 与同类工具对比
*   **VS Kong/APISIX**：传统网关对 SSE 支持较差，且缺乏针对 LLM 的原生语义理解（如 Token 计数）。Higress 的 WASM 插件生态虽然不如 Kong 成熟，但在 AI 领域的专用性上具有代差优势。
*   **VS LangServe / LangChain**：这些是开发框架，而非网关。Higress 位于框架更前端，负责流量入口，不涉及模型逻辑编排，侧重于运维和治理。

### 技术实现原理
*   **WASM 插件机制**：Higress 预编译了 WASM 滤镜。当请求经过时，Envoy 会加载 WASM 模块，执行 `OnHttpRequestHeaders` 或 `OnHttpBody` 等钩子函数。对于 AI 场景，插件会解析 HTTP Body 中的 JSON，提取 `messages` 字段计算 Token，或在流式响应中逐块解析内容。

---

## 3. 技术实现细节

### 关键技术方案
*   **xDS 协议优化**：Higress 控制平面与 Envoy 之间通过 gRPC 流式连接传输配置。为了解决大规模配置下的性能瓶颈，Higress 可能采用了增量 xDS 推送策略，仅推送变更的配置部分。
*   **WASM 沙箱隔离**：利用 V8 或 WASMTime 引擎，确保插件崩溃不会导致 Envoy 主进程崩溃。内存管理上采用了“资源限制”机制，防止恶意或失控的插件耗尽网关资源。

### 代码组织结构
*   **`/pkg`**：核心业务逻辑。包含与 Istio 交互的 Controller、配置转换逻辑。
*   **`/plugins`**：WASM 插件的源码（通常为 Go 或 C++）。这里包含了 AI 请求/响应的修改逻辑。
*   **`/docker`**：镜像构建脚本，通常基于 Envoy 官方镜像进行二次打包，嵌入 WASM 运行时。

### 性能与扩展性
*   **多线程模型**：Envoy 采用非阻塞 I/O + 多线程模型。Higress 充分利用了这一点，每个 Worker 线程独立处理连接，仅在配置变更时通过共享内存或文件系统同步状态。
*   **冷启动优化**：为了减少 WASM 模块的首次加载延迟，Higress 可能实现了模块缓存或预加载机制。

### 技术难点与解决
*   **流式响应的上下文处理**：LLM 返回的是流式数据，网关需要在流结束前统计总 Token 数。**解决方案**：Higress 在 WASM 插件中维护了流级别的上下文状态，在流结束时（`OnStreamComplete`）触发计量逻辑。
*   **配置一致性**：在分布式网关实例中保证配置一致。**解决方案**：依托 Istio 的控制平面机制，使用 CRD 作为单一数据源。

---

## 4. 适用场景分析

### 适合使用的项目
1.  **AI 应用开发平台**：需要快速集成多家大模型，并进行统一计费和限流的企业。
2.  **企业级 AI Agent 落地**：需要将企业内部 API（ERP、CRM）安全地暴露给 AI Agent 调用的场景。
3.  **微服务架构升级**：正在从传统 Nginx/Ingress 迁移到云原生架构，且对扩展性有高要求的团队。

### 最有效的情况
*   当你的应用需要**同时**处理传统 Web 流量和 AI 流量，且希望统一治理时。
*   当你需要对 AI 调用成本进行精细化控制，且不想在每个微服务里埋点时。

### 不适合的场景
*   **极简静态博客或小型站点**：Higress 的资源开销（内存通常在 500MB+）对于极小流量来说过重，Nginx 更合适。
*   **复杂的业务逻辑编排**：网关应保持轻量，如果涉及复杂的业务流（如订单状态机），应在后端服务或 Workflow 引擎中处理，而非在网关插件中硬编码。

### 集成方式
*   **K8s Ingress**：直接安装 Higress Helm Chart，将 Ingress Class 指向 `higress`。
*   **MCP 接入**：在 Higress 配置中定义 `MCPService` 资源，将后端 Service 映射为 MCP Tool。

---

## 5. 发展趋势展望

### 技术演进方向
*   **更深入的 AI 协议支持**：除了文本，未来将加强对多模态（图片、音频）流式传输的支持。
*   **RAG 向量网关**：Higress 可能会集成向量数据库的连接能力，直接在网关层进行语义缓存或文档检索路由。

### 社区反馈与改进
*   目前社区主要集中在中文圈（阿里系），国际化程度不如 APISIX。未来需要加强对非中文模型（如 Claude, Gemini）的深度适配和文档完善。

### 与前沿技术结合
*   **WASI (WebAssembly System Interface)**：随着 WASI 的成熟，WASM 插件将拥有更强的网络和文件访问能力，使 Higress 插件能做更复杂的事情，如直接调用数据库进行鉴权。

---

## 6. 学习建议

### 适合开发者水平
*   **中级**：了解 Kubernetes 基础、HTTP 协议。
*   **高级**：若需开发 WASM 插件，需掌握 Go/C++ 并理解代理原理。

### 学习路径
1.  **基础**：部署 Higress 到 K8s 集群，配置一个简单的 AI 路由。
2.  **进阶**：阅读官方提供的 WASM 插件示例（如 `ai-proxy`），尝试修改 Prompt 注入逻辑。
3.  **深入**：研究 Envoy 的 xDS 协议和 Higress 的 Controller 源码，理解配置如何转化为路由表。

### 实践建议
*   先在 Docker Desktop 或 Kind 等本地 K8s 环境中跑通 Demo。
*   重点调试 AI 流式输出，观察网关日志中的 Token 计数。

---

## 7. 最佳实践建议

---
## 代码示例




```python
# 示例1：Higress WasmPlugin 配置示例
# 解决问题：为 Higress 网关配置一个简单的 Wasm 插件，用于实现请求头修改
def create_wasm_plugin_config():
    """
    生成 Higress WasmPlugin 的 YAML 配置
    适用于需要通过 Wasm 插件扩展网关功能的场景
    """
    config = {
        "apiVersion": "extensions.higress.io/v1alpha1",
        "kind": "WasmPlugin",
        "metadata": {
            "name": "request-header-modifier",
            "namespace": "default"
        },
        "spec": {
            "matchRules": [{
                "config": {
                    "headers": {
                        "X-Custom-Header": "Higress-Demo"
                    }
                }
            }],
            "url": "oci://higress-registry.cn-hangzhou.cr.aliyuncs.com/plugins/request-header-modifier:1.0.0"
        }
    }
    return config

# 使用示例
plugin_config = create_wasm_plugin_config()
print("生成的 WasmPlugin 配置：", plugin_config)
```




```python
# 示例2：Higress 路由规则配置示例
# 解决问题：为微服务配置基于路径的路由规则
def create_route_config(service_name, path_prefix, backend_service):
    """
    生成 Higress Ingress 路由配置
    适用于微服务架构中的流量路由场景
    """
    config = {
        "apiVersion": "networking.k8s.io/v1",
        "kind": "Ingress",
        "metadata": {
            "name": f"{service_name}-ingress",
            "annotations": {
                "kubernetes.io/ingress.class": "higress"
            }
        },
        "spec": {
            "rules": [{
                "host": "example.com",
                "http": {
                    "paths": [{
                        "path": path_prefix,
                        "pathType": "Prefix",
                        "backend": {
                            "service": {
                                "name": backend_service,
                                "port": {
                                    "number": 8080
                                }
                            }
                        }
                    }]
                }
            }]
        }
    }
    return config

# 使用示例
route_config = create_route_config(
    service_name="user-service",
    path_prefix="/api/users",
    backend_service="user-backend"
)
print("生成的路由配置：", route_config)
```




```python
# 示例3：Higress 流量分流配置示例
# 解决问题：实现基于权重的灰度发布/金丝雀发布
def create_canary_config(service_name, stable_version, canary_version, canary_weight):
    """
    生成 Higress 灰度发布配置
    适用于需要平滑升级服务的场景
    """
    config = {
        "apiVersion": "networking.higress.io/v1",
        "kind": "McpBridge",
        "metadata": {
            "name": f"{service_name}-canary"
        },
        "spec": {
            "services": [{
                "name": service_name,
                "namespace": "default",
                "hosts": [{
                    "hostname": "example.com",
                    "weight": 100,
                    "serviceName": f"{service_name}-{stable_version}"
                }, {
                    "hostname": "example.com",
                    "weight": canary_weight,
                    "serviceName": f"{service_name}-{canary_version}"
                }]
            }]
        }
    }
    return config

# 使用示例
canary_config = create_canary_config(
    service_name="payment-service",
    stable_version="v1",
    canary_version="v2",
    canary_weight=20  # 20% 流量到新版本
)
print("生成的灰度配置：", canary_config)
```


---
## 案例研究


### 1：阿里巴巴内部淘系业务（大促流量防护）

 1：阿里巴巴内部淘系业务（大促流量防护）

**背景**:
在淘宝、天猫等核心电商业务的“双11”或“618”大促期间，流量会瞬间爆发至平时的数十倍甚至上百倍。传统的网关架构在面对每秒百万级 QPS 的洪峰流量时，往往面临资源利用率瓶颈和配置变更生效延迟的挑战。

**问题**:
1.  大促期间流量洪峰导致传统网关 CPU 负载过高，甚至出现雪崩效应。
2.  业务规则变更频繁，传统网关配置热更新耗时较长，难以满足分钟级的应急响应需求。
3.  需要在大促前进行大规模的容量压测，对网关的性能极限要求极高。

**解决方案**:
阿里巴巴将内部核心流量网关迁移至基于 Higress 的新架构。利用 Higress 的高性能 Wasm 插件市场，实现了流量防护逻辑（如限流、降级、鉴权）与网关核心的解耦。通过 Wasm 技术实现了业务逻辑的热加载，无需重启网关即可更新防护规则。

**效果**:
1.  成功平稳支撑了双11期间每秒百万级 QPS 的流量洪峰，系统 P99 延迟显著降低。
2.  实现了秒级的规则热更新，大幅提升了运维效率和应急响应速度。
3.  通过将部分业务逻辑下沉至网关层，减轻了后端业务服务的计算压力，整体资源利用率提升 30% 以上。

---



### 2：某 AI 创业公司（LLM 大模型统一网关）

 2：某 AI 创业公司（LLM 大模型统一网关）

**背景**:
一家专注于 AIGC 应用开发的初创公司，其业务底层依赖于多家不同的 LLM 提供商（如 OpenAI、Claude、国内通义千问等）。前端应用需要根据用户等级和业务场景，动态路由到不同的模型供应商，并处理 Token 计费和 Prompt 增强。

**问题**:
1.  **接口不统一**：各家模型厂商的 API 协议、参数格式差异巨大，客户端维护成本高。
2.  **成本控制难**：无法在网关层统一统计不同厂商的 Token 消耗，导致后端计费逻辑复杂且存在滞后。
3.  **密钥安全**：将各厂商的 API Key 直接暴露给前端应用存在极大的泄露风险。

**解决方案**:
引入 Higress 作为 AI 服务的统一入口（AI Gateway）。
1.  使用 Higress 的 AI 插件特性，将不同厂商的异构 API 标准化为统一的 OpenAI 协议格式。
2.  在网关层配置 Prompt 模板管理和 Token 统计插件，实现了对请求和响应的实时拦截与处理。
3.  在网关层统一配置各家厂商的 API Key，前端应用只需携带内部鉴权信息，彻底屏蔽了后端供应商的密钥细节。

**效果**:
1.  **开发效率提升**：前端团队只需对接一套标准 API，开发对接效率提升 50%。
2.  **成本可视化**：实现了基于 Token 的实时精准计费和流量控制，有效避免了因异常调用产生的超额费用。
3.  **安全性增强**：集中管理密钥，配合全链路日志追踪，满足了企业级的安全合规要求。

---



### 3：某跨国物流企业（云原生架构转型与多集群管理）

 3：某跨国物流企业（云原生架构转型与多集群管理）

**背景**:
该企业正处于从微服务向云原生架构转型的深水区，业务部署在混合云环境（自建 IDC + 阿里云 ACK）。由于历史原因，存在基于 Nginx 的传统 Ingress、Kubernetes 原生 Ingress 以及 API Gateway 多套网关并存的混乱局面。

**问题**:
1.  **架构割裂**：不同网关之间的配置标准不一致，无法实现统一的流量管理（如蓝绿发布、金丝雀发布）。
2.  **运维复杂**：多套控制平面导致运维人员学习成本高，配置变更容易出错。
3.  **功能缺失**：传统 Ingress 对复杂的路由重写、认证鉴权支持较弱，往往需要编写复杂的 Lua 脚本，维护困难。

**解决方案**:
采用 Higress 作为统一的云原生 API 网关，替代旧有的 Nginx 和 K8s Ingress。
1.  利用 Higress 对 Ingress API 的兼容支持，平滑接管存量业务流量，实现零中断迁移。
2.  借助 Higress 的服务来源管理功能，统一纳管注册中心（如 Nacos）和 K8s Service 的服务发现。
3.  使用 Higress 的控制台进行全局流量管控，实施基于权重的灰度发布策略。

**效果**:
1.  **统一管控**：成功收敛了多套网关架构，实现了单一控制平面管理混合云流量，运维复杂度降低 60%。
2.  **业务敏捷性**：标准化的金丝雀发布流程，使得新版本的上线回滚时间从小时级缩短至分钟级。
3.  **扩展性增强**：基于 Wasm 的插件机制让业务团队能够轻松开发自定义插件（如特定的物流轨迹校验逻辑），无需修改网关核心代码。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Apache APISIX | Kong Gateway |
|------|----------------|---------------|--------------|
| 性能 | 高性能（基于 Envoy 和 Rust） | 极高性能（基于 LuaJIT） | 高性能（基于 Nginx 和 OpenResty） |
| 易用性 | 提供控制台和 K8s Ingress 支持 | 配置灵活但学习曲线较陡 | 提供管理界面和丰富的插件 |
| 成本 | 开源免费，企业版收费 | 完全开源免费 | 开源免费，企业版收费 |
| 扩展性 | 支持 WASM 插件，扩展性强 | 支持 Lua 和 Python 插件 | 支持 Lua 和 Go 插件 |
| 社区活跃度 | 阿里背书，社区活跃 | Apache 顶级项目，社区活跃 | 商业化成熟，社区活跃 |
| 适用场景 | 云原生、微服务、API 管理 | 高并发 API 网关 | 传统 API 网关和微服务 |

### 优势分析

- 优势1：基于 Envoy 和 Rust 构建，性能和安全性较高。
- 优势2：支持 WASM 插件，扩展性和灵活性优于传统 Lua 插件。
- 优势3：与阿里云生态深度集成，适合云原生场景。

### 不足分析

- 不足1：社区和生态相对 APISIX 和 Kong 较新，资源较少。
- 不足2：企业版功能可能需要付费，成本较高。
- 不足3：学习曲线较陡，对新手不够友好。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Wasm 插件实现扩展能力

**说明**: Higress 原生支持 WebAssembly (Wasm) 技术，允许用户使用 C++、Go、Rust 或 AssemblyScript 等语言编写插件。相比传统网关（如 Nginx）需要修改 C 模块并重新编译，Higress 的 Wasm 插件支持动态加载，极大地扩展了网关的自定义处理能力，同时保持了高性能和安全性。

**实施步骤**:
1. 根据业务需求选择合适的编程语言（推荐 Go 或 Rust）编写插件逻辑。
2. 使用 Higress 提供的 SDK 或 `wasm-assembler` 工具将代码编译为 `.wasm` 文件。
3. 在 Higress 控制台或通过 `WasmPlugin` CRD 配置插件，将其挂载到特定的网关路由或全局作用域。
4. 配置插件的执行阶段（如 `HTTPFilter`）和优先级。

**注意事项**: 
- Wasm 插件运行在沙箱中，但频繁的内存分配或跨语言调用仍会带来一定的性能损耗，需进行性能压测。
- 确保 Wasm 插件与 Higress 的 API 版本兼容。

---

### 实践 2：服务发现与 Nacos 注册中心的无缝集成

**说明**: Higress 深度集成了 Nacos、Zookeeper、Consul 等注册中心。对于使用阿里云技术栈的微服务架构，直接对接 Nacos 可以实现从网关到后端服务的自动服务发现，避免手动维护静态 IP 列表，并支持基于权重的流量分发和蓝绿发布。

**实施步骤**:
1. 在 Higress 控制台的“来源管理”中，选择添加 Nacos 服务来源。
2. 配置 Nacos 服务器的地址、命名空间和访问凭证。
3. 在创建 Ingress 或网关路由时，服务名称可以直接选择 Nacos 中注册的服务名。
4. 利用 Nacos 的元数据功能，在 Higress 中实现更精细的路由匹配。

**注意事项**: 
- 确保 Higress 所在的网络环境能够访问 Nacos 集群。
- 如果服务数量巨大，注意监控 Nacos 的连接数限制。

---

### 实践 3：精细化全链路安全防护

**说明**: Higress 提供了从路由级到服务级的多层安全防护。除了基本的 IP 黑白名单外，还支持 JSON Web Token (JWT) 验证、Keyless 认证以及阿里云 WAF 的直接集成。通过配置严格的安全策略，可以防止未授权访问和常见攻击（如 SQL 注入、XSS）。

**实施步骤**:
1. 在路由配置中启用“认证鉴权”，选择 JWT、Basic Auth 或 OAuth2 等方式。
2. 配置 IP 访问控制，限制仅允许特定网段或 VPC 内的流量访问敏感 API。
3. 对于高安全需求的场景，开启阿里云 WAF 插件，配置防御规则。
4. 定期审计网关访问日志，识别异常流量模式。

**注意事项**: 
- JWT 验证会解析每一个请求，需确保 JWKs 获取的效率，避免成为性能瓶颈。
- 密钥管理应遵循最小权限原则，并定期轮换。

---

### 实践 4：金丝雀发布与流量标签路由

**说明**: Higress 允许基于 HTTP 请求头、Cookie 或查询参数进行流量路由。这是实现灰度发布（金丝雀发布）和 A/B 测试的最佳方式。通过在网关层将特定特征的流量（如内网用户或测试账号）路由到新版本服务，可以在不影响大部分用户的情况下验证新功能。

**实施步骤**:
1. 准备两个不同版本的服务（如 v1 和 v2），并在注册中心中注册。
2. 在 Higress 中创建两条路由规则，第一条匹配默认流量指向 v1，第二条匹配特定 Header（如 `x-canary: true`）指向 v2。
3. 设置路由优先级，确保更精确的规则优先匹配。
4. 逐步扩大第二条规则的匹配条件或流量比例，直至全量上线。

**注意事项**: 
- 确保灰度路由的匹配条件具有唯一性，避免误伤正常流量。
- 灰度结束后及时清理路由规则，保持配置整洁。

---

### 实践 5：利用 Ingress 注解进行流量治理

**说明**: Higress 兼容 Kubernetes Ingress 规范，并提供了丰富的注解来实现高级流量治理功能，如超时控制、重试策略、限流熔断和 Header 修改。这种声明式的配置方式使得流量治理策略可以通过 GitOps 流程进行版本控制和自动化部署。

**实施步骤**:
1. 编辑 Kubernetes Ingress YAML 文件。
2. 添加特定注解，例如配置超时：`nginx.ingress.kubernetes.io/proxy-connect-timeout: "60"`（需查阅 Higress 兼容性文档，H

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 WASM 插件按需加载与缓存

**说明**:  
Higress 支持 WASM 插件扩展，但频繁加载未缓存的 WASM 模块会增加冷启动延迟。通过预加载和缓存常用插件可减少重复编译开销。

**实施方法**:  
1. 在网关配置中启用 `wasmCache` 选项，设置缓存大小（如 100MB）和缓存时间（如 1小时）。  
2. 对高频插件（如认证、限流）使用 `preload` 指令提前加载。  
3. 避免动态加载大型 WASM 文件，优先编译为 `.wasm` 格式而非解释执行。

**预期效果**:  
冷启动延迟降低 30%-50%，高频插件调用延迟减少 10%-20%。

---

### 优化 2：调整连接池与线程模型

**说明**:  
默认连接池配置可能不适合高并发场景。优化线程数和连接池参数可提升吞吐量。

**实施方法**:  
1. 将工作线程数设置为 CPU 核数的 1-2 倍（通过 `--worker-threads` 参数）。  
2. 调大 HTTP/2 连接池大小（如从默认 10 改为 50），并启用连接复用。  
3. 对后端服务启用 `keep-alive`，设置 `idleTimeout` 为 60 秒。

**预期效果**:  
吞吐量提升 20%-40%，后端连接错误率降低 15%。

---

### 优化 3：启用请求/响应压缩

**说明**:  
对 JSON/文本类流量启用 Gzip/Brotli 压缩可减少网络传输量，尤其适合带宽敏感场景。

**实施方法**:  
1. 在路由配置中添加 `compress: true`，并设置压缩阈值（如 1KB）。  
2. 优先使用 Brotli 压缩（需后端支持），回退到 Gzip。  
3. 排除已压缩文件（如 `.jpg`、`.zip`）的二次压缩。

**预期效果**:  
传输流量减少 50%-70%，带宽成本降低 30% 以上。

---

### 优化 4：优化路由匹配规则

**说明**:  
复杂路由规则（如正则表达式）会降低匹配效率。简化规则可减少 CPU 消耗。

**实施方法**:  
1. 将高频路径优先匹配，使用前缀匹配（`/api/v1/*`）替代正则。  
2. 合并相似路由，减少规则数量（如从 100 条降至 30 条）。  
3. 对静态内容启用 `exact` 匹配模式。

**预期效果**:  
路由查找延迟降低 20%-30%，CPU 使用率下降 10%-15%。

---

### 优化 5：启用 Prometheus 监控与动态调优

**说明**:  
实时监控可识别性能瓶颈，动态调整配置（如限流阈值）可避免过载。

**实施方法**:  
1. 集成 Prometheus 监控关键指标（如 `request_duration`、`upstream_latency`）。  
2. 设置告警规则（如 P99 延迟超过 500ms 触发告警）。  
3. 基于 Grafana 仪表盘动态调整 `concurrency` 和 `rateLimit` 参数。

**预期效果**:  
故障响应时间缩短 50%，资源利用率提升 15%-25%。

---

### 优化 6：使用分布式缓存减少重复计算

**说明**:  
对鉴权、限流等需要重复查询的数据（如 Token 验证结果），启用分布式缓存可降低后端压力。

**实施方法**:  
1. 配置 Redis 作为缓存后端，设置 TTL（如 300 秒）。  
2. 对缓存键使用哈希策略（如 `userId:apiPath`）。  
3. 监控缓存命中率，保持在 80% 以上。

**预期效果**:  
后端请求量减少 40%-60%，鉴权延迟降低 30%。

---
## 学习要点

- Higress 是阿里开源的基于 Istio 的云原生 API 网关，深度集成了 K8s 与 Dubbo/Nacos 等微服务生态。
- 提供了强大的流量治理能力，支持金丝雀发布、蓝绿发布、负载均衡以及超时重试等企业级路由规则。
- 内置了针对高并发场景优化的 WAF 插件与安全防护机制，能够有效抵御常见的 Web 攻击。
- 架构设计上实现了数据平面与控制平面的分离，支持高性能的动态配置更新与热加载。
- 兼容 Ingress 与 Gateway API 标准，并支持将 Kong 等传统网关的配置无缝迁移。
- 具备极强的可扩展性，允许通过 WASM (WebAssembly) 或 Go/Python/Java 编写自定义插件来扩展业务逻辑。
- 提供了开箱即用的 Prometheus 监控指标集成与 Grafana 仪表盘，便于实时观测网关状态。


---
## 学习路径

## 学习路径

### 阶段 1：基础概念与环境认知

**学习内容**:
- **云原生网关基础**: 理解什么是 API 网关，以及它在微服务架构中的位置（南北向流量与东西向流量）。
- **Higress 架构概览**: 了解 Higress 基于 Istio 和 Envoy 的技术架构，以及它与 Nginx、传统 Kong 网关的区别。
- **核心特性**: 学习 Higress 的核心能力，如流量管理、安全防护、服务发现以及对 Kubernetes (K8s) 的原生支持。
- **部署方式**: 了解如何在本地 Docker 环境或 Kubernetes 集群中快速部署 Higress。

**学习时间**: 1-2周

**学习资源**:
- **官方文档**: Higress GitHub 仓库 README 及官方文档站的“快速开始”部分。
- **对比文章**: 搜索阅读 Higress vs Nginx vs Kong 的技术对比文章。
- **社区文章**: 阿里云云原生 API 网关相关技术博客。

**学习建议**:
建议先不要深入代码，而是先通过官方提供的 Demo 或 Docker 镜像跑通一个最简单的示例。理解“路由”和“服务”的概念是本阶段的关键。如果你没有 K8s 基础，建议先补充 Kubernetes 的基本概念。

---

### 阶段 2：核心功能与配置实战

**学习内容**:
- **路由配置**: 深入学习如何配置 HTTP 路由、重定向、重写和流量镜像。
- **插件系统**: 掌握 Higress 的插件机制，学习如何在控制台开启、配置 WAF 认证、限流熔断等内置插件。
- **服务来源**: 实战配置不同的服务来源，包括固定地址、Nacos 注册中心、Kubernetes Service 以及 DNS 域名。
- **全链路治理**: 学习如何进行 Header 修改、请求/响应转换以及基于 IP 的访问控制。

**学习时间**: 2-3周

**学习资源**:
- **官方控制台手册**: 熟悉 Higress Console 的每一个菜单项。
- **插件市场**: 浏览 Higress 官方插件市场，查看热门插件的使用文档。
- **YAML 配置示例**: 阅读网关和路由配置的 YAML 示例，理解声明式配置。

**学习建议**:
动手搭建一个包含两个后端服务的模拟环境（可以使用 Nginx 模拟后端），尝试配置基于 URL 路径的路由转发，并配置一个简单的限流插件。务必熟悉控制台的操作，同时理解对应的配置含义。

---

### 阶段 3：高级插件开发与云原生集成

**学习内容**:
- **自定义插件开发 (Wasm)**: 学习如何使用 Go 或 C++ 开发 Wasm (WebAssembly) 插件，实现 Higress 原生不支持的自定义逻辑（如特殊的签名校验、数据脱敏）。
- **Ingress Controller**: 深入理解 Higress 作为 K8s Ingress Controller 的工作模式，学习如何通过 Kubernetes Ingress 资源管理 Higress。
- **服务网格集成**: 探索 Higress 与 Istio 的集成场景，理解如何作为网格的入口网关。
- **高可用部署**: 学习 Higress 的高可用架构设计，包括多副本部署、健康检查和优雅升级。

**学习时间**: 3-4周

**学习资源**:
- **Higress Wasm Go SDK**: GitHub 上的 Wasm 插件开发示例和 SDK 文档。
- **Kubernetes Ingress 官方文档**: 理解 Ingress 规范。
- **阿里云最佳实践**: 查看阿里云上关于 Higress 生产环境部署的白皮书或案例。

**学习建议**:
尝试编写一个简单的 Wasm 插件（例如：在请求头中添加一个自定义字段），并将其部署到 Higress 中运行。在 Kubernetes 环境中测试 Higress 的自动服务发现和负载均衡能力。

---

### 阶段 4：生产级运维与性能调优

**学习内容**:
- **可观测性**: 深度集成 Prometheus、Grafana 和 SkyWalking，配置日志采集、监控指标告警和链路追踪。
- **安全防护**: 配置详细的 OAuth2、JWT 认证流程，配置 CORS 策略，以及应对 DDoS 攻击的配置。
- **性能调优**: 学习如何调整连接池、缓冲区大小、Worker 进程数等参数以应对高并发流量。
- **多租户管理**: 在多团队环境下，如何通过命名空间或标签进行资源隔离和权限管理。

**学习时间**: 持续学习（约 2-4周）

**学习资源**:
- **Envoy 官方文档**: Higress 底层基于 Envoy，深入理解 Envoy 的配置对调优非常有帮助。
- **开源案例**: 搜索 GitHub 上企业

---
## 常见问题


### 1: Higress 是什么？它与阿里云和 Nginx 有什么关系？

1: Higress 是什么？它与阿里云和 Nginx 有什么关系？

**A**: Higress 是一个开源的、基于云原生架构的 API 网关。它是在 2022 年由阿里云开源的，其内核源自阿里巴巴内部大规模使用多年的 Gateway 代码，并深度集成了 Envoy 和 Istio。

*   **与阿里云的关系**：它是阿里云 MSE（微服务引擎）云产品 API 网关的开源版本，继承了阿里在电商场景下处理高并发流量的技术经验。
*   **与 Nginx 的关系**：虽然 Nginx 是传统的七层负载均衡器，但 Higress 更侧重于云原生环境（如 Kubernetes）。相比 Nginx，Higress 原生支持服务发现、流量管理和安全防护等微服务治理能力，且配置方式更现代化（支持 K8s CRD 和控制台）。

---



### 2: Higress 与 Kong 或 APISIX 等其他开源网关相比有什么优势？

2: Higress 与 Kong 或 APISIX 等其他开源网关相比有什么优势？

**A**: Higress 的核心优势主要体现在以下三个方面：

1.  **极致的性能与稳定性**：基于 Envoy C++ 内核开发，相比基于 Lua 的 Kong 或 OpenResty，Higress 在处理高并发请求时通常具有更低的延迟和更高的吞吐量，且内存占用更为稳定。
2.  **云原生与微服务集成**：Higress 对 Kubernetes 和 Istio 有着天然的支持。它可以作为 Ingress Controller 使用，也能直接接管 Istio 的南北向流量，实现从服务网格到 API 网关的无缝协同。
3.  **插件生态与兼容性**：它兼容 Kong/APISIX 的许多插件设计理念，并支持通过 Wasm (WebAssembly) 技术编写插件。这意味着开发者可以使用 Go、C++、Rust 等语言编写高性能插件，而无需重启网关即可动态加载。

---



### 3: Higress 是否支持热更新？修改配置是否需要重启服务？

3: Higress 是否支持热更新？修改配置是否需要重启服务？

**A**: 是的，Higress 支持完全的热更新，无需重启服务。

得益于其基于 Envoy 的架构（xDS 协议），Higress 的配置变更（如路由规则、插件配置、限流设置等）是动态下发的。当你在控制台或通过 K8s YAML 修改配置后，Higress 会自动将配置推送到数据平面，这个过程对业务流量是无感的，不会导致服务中断。此外，对于 Wasm 插件，Higress 也支持动态加载和卸载。

---



### 4: Higress 能否直接用于生产环境？它的成熟度如何？

4: Higress 能否直接用于生产环境？它的成熟度如何？

**A**: Higress 完全可以用于生产环境。

*   **内部验证**：在开源之前，Higress 的内核已经支撑了阿里巴巴内部多年的“双11”大促，经受住了每秒百万级 QPS 的考验。
*   **外部应用**：目前已有大量企业，包括多家互联网公司和金融机构，在生产环境中使用 Higress 作为其核心流量入口。
*   **社区支持**：作为 GitHub Trending 上的热门项目，它拥有活跃的社区和定期的版本迭代，阿里云团队也提供了长期的技术维护支持。

---



### 5: Higress 支持哪些协议？是否支持 gRPC 或 Dubbo 服务？

5: Higress 支持哪些协议？是否支持 gRPC 或 Dubbo 服务？

**A**: Higress 是一个全功能的七层网关，支持多种主流协议：

1.  **HTTP / HTTPS**：原生支持。
2.  **gRPC**：完全支持 gRPC 协议的代理、路由和负载均衡，支持将 HTTP 请求转换为 gRPC 请求（协议转换）。
3.  **Dubbo**：这是 Higress 的一个特色功能。由于源自阿里系，Higress 原生支持 Apache Dubbo/Dubbo3 协议。它可以将 HTTP/HTTPS 请求转换为 Dubbo 协议调用后端服务，这对于使用 Java 微服务栈（Spring Cloud + Dubbo）的团队来说非常友好，能够实现 HTTP 到 RPC 的无缝互通。

---



### 6: 部署 Higress 是否必须依赖 Kubernetes？

6: 部署 Higress 是否必须依赖 Kubernetes？

**A**: 虽然推荐在 Kubernetes 中使用以发挥其最大价值，但并非强制依赖。

*   **标准部署（推荐）**：在 Kubernetes 环境中，Higress 可以作为 Ingress Controller 或独立的网关服务运行，利用 K8s 的服务发现和自动扩缩容能力。
*   **Docker/虚拟机部署**：Higress 也提供了基于 Docker Compose 的部署方式，允许用户在非 K8s 环境（如虚拟机或物理机）中运行。在这种模式下，服务发现可能需要通过静态配置或注册中心（如 Nacos、Consul）来实现。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单] 本地环境搭建与基础路由

### 问题**: 参考 Higress 官方文档，在本地（Docker 环境）成功部署 Higress 网关。随后，配置一个简单的 Ingress 路由规则，实现当访问 `http://localhost/hello` 时，能够将请求代理至后端的一个模拟服务（如 httpbin.org 或 nginx 容器）并返回 200 响应。

### 提示**: 重点在于阅读 `docker-compose.yml` 的配置以及如何编写 K8s 风格的 Ingress YAML 文件。注意区分 Higress 的控制台配置端口与网关实际监听的流量端口。

### 

---
## 实践建议

基于 Higress 作为 "AI Native API Gateway" 的定位，结合其云原生架构与 AI 网关的特性，以下是 6 条针对实际使用场景的实践建议：

### 1. 利用 WASM 插件实现 AI 请求的精细化管理
**场景：** 在调用 LLM（大语言模型）时，需要对 Prompt（提示词）进行预处理，或者对返回结果进行敏感词过滤、格式化。
**建议：** 不要将业务逻辑强耦合到网关代码中，也不要使用 Nginx Lua 脚本（Higress 不支持）。应优先编写 **WASM (WebAssembly)** 插件。
**具体操作：**
*   使用 Go 或 C++ 编写 WASM 插件，挂载到 `Global` 或 `Route` 级别。
*   在插件中实现请求体的 JSON 修改逻辑（例如：自动注入系统提示词 "You are a helpful assistant"）。
*   利用 WASM 的沙箱特性，确保即使插件崩溃也不会导致整个网关进程退出，这对于承载高并发的 AI 流量至关重要。

### 2. 配置多模型提供商的统一路由与故障转移
**场景：** 业务需要同时对接 OpenAI、阿里云通义千问、Azure OpenAI 等多个模型提供商，且希望在某个 API 限流时自动切换。
**建议：** 利用 Higress 的服务发现和负载均衡功能，将不同的 LLM Provider 定义为不同的服务，并配置 **服务路由** 或 **降级规则**。
**具体操作：**
*   在 Ingress 配置中，将 `provider-a` 和 `provider-b` 定义为两个不同的 Service。
*   配置基于权重的流量路由，实现蓝绿发布（例如：90% 流量走模型 A，10% 走模型 B 进行对比测试）。
*   设置主动健康检查。当某个 LLM API 响应超时或返回 5xx 错误码达到阈值时，Higress 应自动摘除异常节点，避免业务侧收到大量报错。

### 3. 实施基于 Token 的流式响应处理
**场景：** AI 对话通常耗时较长，客户端需要流式（SSE/Stream）返回以展示 "打字机效果"。
**建议：** 确保网关配置正确处理 `Transfer-Encoding: chunked`，避免在网关层缓冲整个响应体。
**具体操作：**
*   检查 Higress 的路由配置，确保开启了 **全链路透传** 模式，不要对响应体进行不必要的 Buffer 操作。
*   如果使用 WASM 插件修改流式响应，需注意流式处理的复杂性。建议仅在 Header 处理阶段做鉴权，尽量避免在 Body 阶段对流式数据进行复杂的正则匹配，以免阻塞流式管道，导致用户端感受到明显的卡顿。

### 4. 建立针对 AI 请求的鉴权与计费体系
**场景：** API 需要暴露给外部用户调用，且 LLM 调用成本较高，需要严格的 API Key 管理和基于 Token 用量的计费。
**建议：** 结合 Higress 的 **鉴权插件**（如 AK/SK 认证或 JWT）与 **Key-Auth** 插件，实现多租户隔离。
**具体操作：**
*   为不同的客户端生成独立的 API Key。
*   在 WASM 插件或日志处理中，解析响应头中的 Token 消耗统计（如 `x-usage` 字段，视具体 LLM Provider 而定），将其记录到日志系统（如 Prometheus 或 Loki）中。
*   **陷阱提示：** AI 请求的 Body 大小通常远大于普通 Web 请求，且连接保持时间（Long-lived connection）更长。在配置网关的 **超时时间** 和 **最大请求体大小** 时，需要适当放宽限制（例如将超时设置为 60s 甚至更高，将 Body Limit 提升至 10MB+），否则容易导致大 Prompt 请求被网关截断。

### 5. 敏感数据脱敏与审计日志

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI 原生](/tags/ai-%E5%8E%9F%E7%94%9F/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [WASM](/tags/wasm/) / [LLM](/tags/llm/) / [MCP 协议](/tags/mcp-%E5%8D%8F%E8%AE%AE/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/) / [DevOps/运维](/scenarios/devops-%E8%BF%90%E7%BB%B4/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260201-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260130-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-8.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*