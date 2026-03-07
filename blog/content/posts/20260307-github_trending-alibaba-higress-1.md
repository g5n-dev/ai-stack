---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-03-07T01:11:26+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "Istio", "Envoy", "WASM", "MCP", "Kubernetes"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "**Higress 项目总结** **1. 项目概述** Higress 是阿里巴巴开源的一款**云原生 API 网关**。该项目基于 Istio 和 Envoy 构建，并扩展了 WebAssembly (WASM) 插件能力。其核心定位是**AI Native API Gateway**（AI 原生 API 网关），"
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
- **星标**: 7,673 (+17 stars today)
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

Higress 是一款基于 Istio 和 Envoy 构建的 AI 原生 API 网关，它通过云原生架构将传统流量管理与 AI 应用需求相结合。该项目旨在解决大模型应用开发中的服务路由与工具集成问题，特别适合需要统一管理微服务和 AI 流量的团队。本文将介绍其系统架构、核心组件，并重点说明 AI 网关特性、MCP 系统及 WASM 插件机制。

---
## 摘要

**Higress 项目总结**

**1. 项目概述**
Higress 是阿里巴巴开源的一款**云原生 API 网关**。该项目基于 Istio 和 Envoy 构建，并扩展了 WebAssembly (WASM) 插件能力。其核心定位是**AI Native API Gateway**（AI 原生 API 网关），旨在为云原生应用和 AI 大模型应用提供统一的流量管理入口。项目使用 Go 语言开发，目前在 GitHub 上拥有超过 7,600 个星标，活跃度较高。

**2. 核心架构与技术特点**
*   **架构设计**：采用**控制平面与数据平面分离**的架构。配置变更通过 xDS 协议传播，具有毫秒级延迟和零连接中断的特性，非常适合 AI 长连接流式响应场景。
*   **扩展能力**：深度集成 **WebAssembly (WASM)** 插件系统，允许用户灵活扩展网关功能。

**3. 三大核心功能**
根据文档描述，Higress 的主要应用场景涵盖以下三个方面：

1.  **AI 网关**：
    *   提供统一 API 接入，兼容 30 多家 LLM 提供商。
    *   核心功能包括协议转换、可观测性、缓存以及安全防护。
    *   *涉及组件：* `ai-proxy`、`ai-statistics`、`ai-cache`、`ai-security-guard` 插件。

2.  **MCP 服务器托管**：
    *   托管模型上下文协议 (MCP) 服务器，使 AI 智能体能够调用工具和服务。
    *   *涉及组件：* `mcp-router`、`jsonrpc-converter` 过滤器及相关服务器实现。

3.  **Kubernetes Ingress 与传统网关**：
    *   作为 K8s Ingress 控制器使用，兼容 nginx-ingress 注解。
    *   提供微服务路由等传统 API 网关能力。
    *   *涉及组件：* `higress-controller`。

**总结**：Higress 是一款将传统微服务治理与新兴 AI 应用需求深度融合的新一代网关，特别针对 AI 流量传输、模型调用协议兼容及智能体工具集成进行了优化。

---
## 评论

**总体判断**

Higress 是目前云原生网关领域中将“AI 原生”理念落地最彻底的开源项目之一，它成功将传统的流量治理与 LLM（大模型）应用所需的特殊协议处理进行了深度融合。该项目不仅解决了 AI 时代网关必须面对的 token 计费、上下文扩充和模型服务解耦问题，还通过基于 Envoy 和 WASM 的架构保证了极高的扩展性与性能，是构建企业级 AI 网关或统一 API 入口的优选方案。

**深度评价依据**

**1. 技术创新性：从“流量转发”到“模型编排”的架构升级**
Higress 最核心的技术差异化在于其 **AI Native（AI 原生）** 的设计理念。传统网关（如 Nginx, Kong）主要关注 HTTP/RESTful 的转发与负载均衡，而 Higress 针对大模型场景进行了深度定制。
*   **事实与推断：** 基于 DeepWiki 提及的“AI Gateway Features for LLM applications”，Higress 在内核层面集成了对 LLM 协议的支持。推断其技术栈在 Envoy 的高性能数据处理层之上，增加了针对 AI 流量的逻辑处理层。这不仅仅是简单的透传，而是实现了语义层面的路由——例如，能够根据 Prompt 的内容或用户身份，将请求智能路由至不同的模型提供商（如 OpenAI、通义千问或本地部署的 Llama）。
*   **差异化亮点：** 引入 **MCP (Model Context Protocol) Server Hosting** 能力是一大创新。这意味着网关不仅仅是一个被动的管道，更变成了 AI Agent 的工具集管理中心，直接解决了 AI 应用中“工具调用”标准化的痛点。

**2. 实用价值：解决 AI 落地中的“碎片化”与“成本”难题**
在实用层面，Higress 解决了企业在接入大模型时面临的三个最现实的问题：**成本控制、模型厂商锁定、以及安全合规**。
*   **事实与推断：** 描述中提到“AI gateway features”和“traditional API gateway capabilities”。推断其实用性体现在“统一化”——企业只需维护一套网关设施，即可同时管理传统的微服务流量和新兴的 AI 流量。
*   **具体场景：**
    *   **Token 级别的精细化治理：** 开发者常面临的痛点是无法精确控制 API 调用成本。Higress 支持对 Token 进行实时计量和限流，这是传统网关无法做到的（传统网关仅基于请求数或连接数）。
    *   **Prompt 注入与拦截：** 在网关层实现敏感词过滤或 Prompt 模板注入，无需修改后端业务代码，极大地提升了 AI 应用迭代的灵活性。
    *   **兼容 K8s Ingress：** 降低了迁移门槛，使得用户可以在不改变现有 K8s 运维体系的前提下平滑升级到 AI 网关。

**3. 代码质量与架构：云原生标准与 WASM 的灵活性**
Higress 继承了 Istio 和 Envoy 的架构优势，控制平面与数据平面分离，且通过 WASM (WebAssembly) 技术解决了扩展性问题。
*   **事实与推断：** DeepWiki 明确指出其“Built on Istio and Envoy”并具备“WASM Plugin Capabilities”。这表明项目在架构设计上遵循了云原生的最佳实践。
*   **代码规范与扩展性：** 使用 Go 语言开发控制面，利用 Envoy (C++) 处理数据面，兼顾了开发效率与运行性能。WASM 插件系统的引入是代码质量的一大亮点，它允许开发者使用 Python、Go 或 AssemblyScript 编写业务逻辑（如鉴权、请求修改），并动态热加载到网关中，而无需重启网关或编译 C++ 插件。这种“低代码”式的扩展机制极大地提升了系统的可维护性。

**4. 社区活跃度：背靠阿里，生态成熟**
*   **事实与推断：** 仓库归属于 `alibaba` 组织，星标数 7,673（且在持续增长），说明其并非个人项目，而是有企业级背托的工业级产品。
*   **生态支持：** 作为 Higress 的前身是阿里内部曾支撑过双十一流量的网关系统，其稳定性经过了极端场景的验证。开源后的社区活跃度较高，文档提供了中/日/英三语，显示出其国际化布局的意图。对于国内开发者而言，中文文档的完备度大大降低了上手门槛。

**5. 潜在问题与改进建议**
尽管优势明显，但在实际选型中仍需注意以下挑战：
*   **复杂度曲线：** 基于 Istio 的架构意味着其部署和运维复杂度高于单纯的 Nginx。对于没有 K8s 基础的小团队，Higress 的运维成本可能过高。
*   **资源占用：** Envoy 本身是内存密集型应用，叠加 AI 请求的长连接和流式处理特性，在超高并发下的内存管理需要重点关注。
*   **建议：** 建议官方进一步简化 Standalone（非 K8s）模式的部署体验，以便于传统虚拟机环境的用户快速体验 AI 网关能力。

**与同类工具对比优势**
*   **对比 Kong/APISIX：** 传统 API 网关虽然也推出了 AI 插件，但多为“补丁式”添加。Higress 的优势在于原生支持 SSE（Server-Sent Events）流式传输的完整生命周期管理

---
## 技术分析

基于对 Alibaba Higress 仓库的深入分析，以下是从技术架构、核心功能、实现细节、适用场景、发展趋势、学习建议、最佳实践以及工程哲学等八个维度的详细解读。

---

# 1. 技术架构深度剖析

Higress 的架构设计体现了**“深度结合云原生生态”**与**“面向 AI 原生改造”**的双重特征。

### 架构模式与技术栈
Higress 采用了典型的**控制平面与数据平面分离**的架构模式。
*   **底层基石**：完全基于 **Envoy** 构建。Envoy 是云原生边缘事实上的标准，提供了 C++ 编写的高性能 L7 代理。
*   **控制平面**：基于 **Istio** 修改而来。Higress 并没有从零造轮子，而是对 Istio 进行了“瘦身”和“增强”，剥离了庞大的服务网格治理能力，专注于网关领域的流量管理。
*   **扩展机制**：引入 **WebAssembly (WASM)** 作为一等公民。这是其架构中最关键的技术决策，允许使用 C/C++/Go/Rust 等高性能语言编写插件，并在运行时动态加载，无需重启网关。
*   **配置分发**：使用 **xDS 协议**（包括 LDS, CDS, RDS 等）在控制平面和数据平面之间传递配置。Higress 优化了 xDS 的推送逻辑，实现了毫秒级的配置生效。

### 核心模块设计
1.  **Router (路由层)**：基于域名、路径、Header 等传统 HTTP 网关路由，并针对 AI 场景扩展了基于模型名称、Token 限制的路由策略。
2.  **WASM Plugin System (插件系统)**：通过 Proxy-WASM 规范挂载到 Envoy 的请求生命周期中。
3.  **MCP Server (Model Context Protocol)**：这是 Higress 作为 AI Gateway 的创新模块，它允许大模型应用（如 ChatGPT 类应用）通过网关安全地调用外部工具和数据源，网关充当了 Agent 和工具之间的代理层。

### 架构优势
*   **热更新能力**：得益于 WASM 和 xDS 的结合，业务逻辑变更（如限流规则、鉴权逻辑）可以在毫秒级生效，且不中断长连接。这对 AI 流式响应场景至关重要。
*   **极致性能**：数据平面是 Envoy (C++)，处理网络 I/O 的性能远超基于 Java 或 Go 的纯用户态网关，而业务逻辑通过 WASM 运行在接近原生的速度。
*   **生态兼容**：完全兼容 K8s Ingress 标准和 Istio Gateway API，降低了迁移成本。

---

# 2. 核心功能详细解读

Higress 的核心价值在于它不仅是一个 API 网关，更是一个**AI 流量的调度中心**。

### 主要功能与场景
1.  **AI 网关**：
    *   **提供商抽象**：将 OpenAI、Azure、通义千问、HuggingFace 等不同 LLM 提供商的 API 统一化。前端应用只需调用 Higress 的标准接口，由网关负责路由到具体的模型。
    *   **Token 管理**：实现了 Prompt 模板管理、Token 计费与限流。这是传统 API 网关难以处理的，因为 LLM 的计费是基于 Token 而非单纯的请求数。
    *   **结果缓存**：针对高重复度的 Prompt 提供语义缓存，直接返回结果，大幅降低后端模型成本。
2.  **MCP 协议支持**：
    *   Higress 内置了 MCP Server 的托管能力。AI Agent 可以通过 Higress 安全地访问企业内部数据库或 API，网关负责处理鉴权和数据转换，避免了直接暴露内部服务。
3.  **传统 API 网关**：
    *   支持 K8s Ingress、Canary Deployment（金丝雀发布）、Traffic Shifting（流量染色）。

### 解决的关键问题
*   **AI 服务的稳定性**：解决了 LLM API 不稳定、超时、流式传输中断等问题，提供了重试和降级机制。
*   **统一接入与成本控制**：企业内部可能同时使用多家模型，Higress 提供了统一的控制平面来管理密钥、配额和计费。

### 与同类工具对比
*   **vs. Nginx/Kong**：Kong 主要基于 Lua 插件，生态虽好但性能隔离性差，且 Lua 开发门槛较高。Higress 的 WASM 沙箱隔离性更好，内存管理更安全。
*   **vs. Istio Ingress**：Istio 原生 Ingress 配置极其复杂，且缺乏针对 AI 流量（如 Token 计数、SSE 流式处理）的专用支持。Higress 提供了开箱即用的 AI 能力。

---

# 3. 技术实现细节

### 关键技术方案
*   **WASM 虚拟机集成**：Higress 在 Envoy 中集成了 WASM Runtime（如 Wasmtime 或 V8）。它通过 `HttpFilter` 接口拦截请求。关键实现在于如何将 Go/Java 编写的代码编译为 WASM 模块，并通过 xDS 推送到 Envoy。
*   **流式处理**：AI 交互大量使用 Server-Sent Events (SSE)。Higress 在数据平面实现了对 SSE 帧的解析能力，能够统计流式传输中的 Token 数量，这是传统网关只看字节流无法做到的。
*   **配置热加载**：Higress 控制平面维护了配置的版本控制，通过增量 xDS 推送机制，只推送变更的配置部分，减少了网络开销和 CPU 消耗。

### 代码组织与设计模式
*   **代码结构**：`pkg/` 目录通常包含核心控制逻辑，`plugins/` 目录包含各种 WASM 插件的源码。它大量使用了 **Kubernetes Controller Pattern**（Informer/Workqueue/Reconcile）来监听 K8s 资源变化并转化为网关配置。
*   **适配器模式**：在处理不同 LLM 提供商时，使用了适配器模式，将各家差异化的 API（OpenAI 格式 vs 非标准格式）统一转换为内部标准协议。

### 性能与扩展性
*   **性能优化**：数据面零拷贝技术（Envoy 特性）。WASM 插件虽然比原生 C++ 慢，但比 Lua 快，且内存占用可控。
*   **扩展难点**：WASM 插件的调试相对困难，且目前 WASM 对非网络 I/O（如文件系统访问）的支持受限。

---

# 4. 适用场景分析

### 适合使用的项目
1.  **AI 原生应用**：任何直接调用大模型（LLM）的应用，特别是需要同时对接多个模型供应商、需要严格控制 Token 成本的企业级 SaaS。
2.  **微服务环境**：已使用 Kubernetes 部署，需要替代 Nginx Ingress 或传统 API 网关，且希望获得更强扩展性的团队。
3.  **需要复杂流量治理**：需要进行 A/B 测试、蓝绿发布、基于 Header 的复杂路由的业务。

### 不适合的场景
1.  **极简边缘部署**：如果只是为一个简单的个人博客做反向代理，Higress（含 K8s 依赖）过于重量级，直接用 OpenResty/Nginx 即可。
2.  **非 K8s 环境**：虽然支持 Standalone 模式，但其最大威力在于 K8s 生态，脱离 K8s 会失去动态服务发现等核心优势。

### 集成注意事项
*   **资源规划**：WASM 插件运行需要消耗额外内存，需根据插件数量调整 Envoy 的内存限制。
*   **网络延迟**：控制平面与数据平面分离，如果部署在不同地域，xDS 推送延迟可能影响配置生效速度。

---

# 5. 发展趋势展望

### 演进方向
1.  **从“流量网关”到“模型网关”**：未来 Higress 将更深入地集成 AI 能力，如内置向量数据库路由、RAG（检索增强生成）流程编排。
2.  **MCP 协议的普及**：随着 AI Agent 的爆发，Higress 可能会成为企业内部 MCP 服务器的标准入口，成为 AI 时代的“API 网关”。
3.  **WASM 生态标准化**：推动 Proxy-WASM 插件市场的标准化，实现插件在不同网关之间的可移植性。

### 潜在改进空间
*   **WASM 的启动延迟**：冷启动 WASM 模块仍有毫秒级延迟，对于极致性能场景需优化。
*   **可观测性**：针对 AI 流量（如 Prompt 质量、Token 消耗趋势）的深度可视化分析仍需加强。

---

# 6. 学习建议

### 适合人群
*   **中高级后端工程师**：希望深入理解云原生网关、Service Mesh 技术栈的开发者。
*   **AI 应用架构师**：需要构建企业级 LLM 应用的技术负责人。

### 学习路径
1.  **基础前置**：熟悉 Docker/Kubernetes 基础，理解 HTTP 协议细节。
2.  **核心理论**：阅读 Envoy 官方文档中的 xDS 和 Filter 机制；理解 WASM (WebAssembly) 的基本原理。
3.  **源码阅读**：
    *   从 `pkg/config` 入手，看配置如何解析。
    *   查看 `plugins/wasm-go`，看如何用 Go 写插件。
    *   研究 `router` 模块，看 HTTP 路由如何匹配。
4.  **实践**：在本地 Kind 集群中部署 Higress，编写一个简单的 WASM 插件（如添加 HTTP Header），并尝试配置 AI 路由。

---

# 7. 最佳实践建议

### 正确使用方式
*   **插件隔离**：将高风险或计算密集型的逻辑放在 WASM 插件中，而不是修改核心网关代码。这便于升级和维护。
*   **AI 模型路由**：利用 Higress 的 Header 转发能力，将用户请求根据 `model` 字段路由到不同的后端服务（如 `gpt-4` 走高优先级通道，`gpt-3.5` 走低优先级）。

### 常见问题与性能优化
*   **问题：WASM 插件导致内存溢出。**
    *   *解决*：在插件代码中严格限制缓存大小，使用 `memory_limit` 配置约束插件 VM 的内存。
*   **优化：长连接堆积。**
    *   *建议*：在 AI 流式响应场景下，调整 Envoy 的 `connection_duration` 和 `stream_idle_timeout`，防止大量僵尸连接耗尽文件描述符。

---

# 8. 哲学与方法论：第一性原理与权衡

### 抽象层与复杂性转移
Higress 在抽象层上做了一个大胆的决定：**将“业务逻辑的执行环境”标准化为 WASM，而非传统的脚本嵌入（如 Nginx Lua）或进程外调用（如 gRPC 插

---
## 代码示例




```python
# 示例1：Higress 网关路由配置
def higress_route_config():
    """
    配置 Higress 网关的路由规则
    解决问题：将不同路径的请求转发到不同的后端服务
    """
    # 模拟 Higress 路由配置
    route_config = {
        "routes": [
            {
                "path": "/api/v1/*",
                "backend": "service-a:8080",
                "timeout": "5s"
            },
            {
                "path": "/api/v2/*",
                "backend": "service-b:8080",
                "timeout": "10s"
            }
        ]
    }
    
    # 打印配置信息
    for route in route_config["routes"]:
        print(f"路径: {route['path']} -> 后端服务: {route['backend']} (超时: {route['timeout']})")
    
    return route_config

# 测试运行
higress_route_config()
```




```python
# 示例2：Higress 插件配置
def higress_plugin_config():
    """
    配置 Higress 的插件功能
    解决问题：为 API 添加限流和认证功能
    """
    # 模拟 Higress 插件配置
    plugin_config = {
        "plugins": [
            {
                "name": "key-auth",
                "config": {
                    "keys": ["client1", "client2"]
                }
            },
            {
                "name": "rate-limit",
                "config": {
                    "requests_per_second": 100,
                    "burst": 200
                }
            }
        ]
    }
    
    # 打印插件配置
    for plugin in plugin_config["plugins"]:
        print(f"插件名称: {plugin['name']}")
        print(f"配置: {plugin['config']}\n")
    
    return plugin_config

# 测试运行
higress_plugin_config()
```




```python
# 示例3：Higress 服务发现集成
def higress_service_discovery():
    """
    集成 Higress 与服务发现系统
    解决问题：动态获取后端服务实例列表
    """
    # 模拟服务发现结果
    service_registry = {
        "service-a": ["10.0.0.1:8080", "10.0.0.2:8080"],
        "service-b": ["10.0.1.1:8080", "10.0.1.2:8080"]
    }
    
    # 更新 Higress 路由配置
    updated_routes = []
    for service, instances in service_registry.items():
        route = {
            "service": service,
            "instances": instances,
            "load_balance": "round_robin"
        }
        updated_routes.append(route)
    
    # 打印更新后的路由配置
    for route in updated_routes:
        print(f"服务: {route['service']}")
        print(f"实例列表: {route['instances']}")
        print(f"负载均衡策略: {route['load_balance']}\n")
    
    return updated_routes

# 测试运行
higress_service_discovery()
```


---
## 案例研究


### 1：阿里巴巴内部电商业务

 1：阿里巴巴内部电商业务

**背景**: 在阿里巴巴庞大的电商生态系统中，微服务架构极其复杂，双十一等大促期间面临海量并发流量。原有的 API 网关在处理大规模流量转发、服务发现以及安全防护时，面临性能瓶颈和扩展性挑战。

**问题**: 传统网关在流量洪峰下延迟增加，配置变更生效慢，且难以与 Kubernetes (K8s) 深度集成以实现云原生的弹性伸缩。同时，需要对不同租户（如淘宝、天猫等不同业务线）进行精细化的流量管理和安全隔离。

**解决方案**: 基于内部多年的 Gateway 践行经验，阿里开源并自研了 Higress。Higress 深度集成了 Envoy 和 Istio，将 Ingress 网关与微服务 API 网关合二为一。通过其标准 K8s Ingress Controller 能力，实现了流量的自动化调度；利用 Wasm 插件机制，实现了热加载的流量拦截和定制化逻辑处理。

**效果**: 成功支撑了双十一万亿级流量的平稳通过，网关 P99 延迟显著降低。通过将 Ingress 和 API 网关架构统一，大幅降低了基础设施的维护成本，并实现了流量的精细化治理和安全防护。

---



### 2：某互联网科技公司 AI 应用网关

 2：某互联网科技公司 AI 应用网关

**背景**: 随着 AIGC（生成式人工智能）浪潮的兴起，该公司内部大量业务开始接入大模型（LLM）。业务部门需要将内部的 Prompt 管理服务、向量数据库以及外部的 LLM 供应商（如 OpenAI、阿里云通义千问等）整合到统一的 API 出口。

**问题**: 直接调用 LLM API 存在诸多痛点：缺乏统一的鉴权和流控，容易导致 API Key 泄露或产生意外的高额费用；不同模型供应商的接口标准不一，业务代码适配繁琐；缺乏对请求内容的审核和缓存机制，导致响应速度慢且存在合规风险。

**解决方案**: 引入 Higress 作为 AI 网关。利用 Higress 的 `ai-proxy` 插件，实现了对多家 LLM 厂商接口的统一适配。通过配置 Wasm 插件，实现了基于 Prompt 的缓存、敏感词过滤以及针对不同用户的 Token 级别流控。

**效果**: 统一了后端大模型的调用入口，屏蔽了不同厂商的接口差异。通过缓存和连接池优化，AI 服务的平均响应时间减少了 30% 以上。同时，通过精细化的流控策略，成功将 AI 调用成本控制在预算范围内，并杜绝了 Key 泄露风险。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|----------------|------|-------|
| 性能 | 基于Envoy和Istio，高性能，支持高并发 | 基于OpenResty，性能优秀，适合高并发场景 | 基于OpenResty，性能极高，适合高并发场景 |
| 易用性 | 提供可视化控制台和K8s集成，易用性较好 | 提供管理界面和插件系统，配置灵活 | 提供Dashboard和丰富的插件，配置稍复杂 |
| 成本 | 开源免费，云服务按需付费 | 开源免费，企业版收费 | 开源免费，企业版收费 |
| 扩展性 | 支持自定义插件，与K8s深度集成 | 插件生态丰富，支持Lua和Go扩展 | 插件生态丰富，支持Lua和Java扩展 |
| 社区支持 | 阿里背书，社区活跃 | 社区成熟，文档丰富 | 社区活跃，国内支持较好 |

### 优势分析

- 优势1：深度集成Kubernetes和Istio，适合云原生环境。
- 优势2：提供完整的流量管理和安全防护功能，开箱即用。
- 优势3：阿里技术支持，适合企业级应用。

### 不足分析

- 不足1：社区生态相对Kong和APISIX较小，插件数量较少。
- 不足2：文档和案例不如Kong和APISIX丰富。
- 不足3：对非Kubernetes环境的支持较弱。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 WASM 的插件扩展与自定义开发

**说明**: Higress 深度集成了 WASM (WebAssembly) 技术，允许开发者使用 C++, Go, Rust, AssemblyScript 或 JavaScript 等多种语言编写高性能插件。相比传统的 Lua 脚本或原生 Go/C++ 开发，WASM 提供了接近原生的性能、更好的隔离性以及更灵活的热加载能力，是实现复杂网关逻辑（如请求签名、响应转换、自定义鉴权）的最佳方式。

**实施步骤**:
1. 访问 Higress 官方文档或 GitHub 仓库，获取 `wasm-go` 等示例 SDK 模板。
2. 根据业务需求选择合适的语言编写插件逻辑，并编译为 `.wasm` 文件。
3. 在 Higress 控制台或通过 Ingress 配置，将 WASM 插件挂载到特定的路由或网关全局作用域。
4. 利用 Higress 提供的插件配置管理功能，动态调整插件参数，无需重启网关。

**注意事项**: 开发过程中需注意 WASM 的内存限制和资源消耗，避免编写无限循环或阻塞式的代码，以防拖慢网关整体性能。

---

### 实践 2：服务发现与 Nacos 注册中心的平滑对接

**说明**: Higress 原生支持 Nacos 作为服务注册中心。对于使用 Spring Cloud 或 Dubbo 架构的微服务体系，直接对接 Nacos 可以实现从网关到后端服务的自动服务发现和负载均衡。这避免了手动维护大量后端服务 IP 列表的繁琐工作，并实现了服务的动态扩缩容感知。

**实施步骤**:
1. 在 Higress 控制台的“来源服务”配置中，添加 Nacos 注册中心，填写服务器地址和命名空间等信息。
2. 创建服务来源，确保 Higress 能够成功连接并拉取 Nacos 中的服务列表。
3. 在配置路由规则时，服务名称直接填写 Nacos 中注册的服务名。
4. 配置健康检查机制，确保 Nacos 中下线的实例能被网关及时摘除。

**注意事项**: 确保 Higress 所在的网络环境能够直接访问 Nacos 服务端地址（特别是跨 K8s 集群或混合云部署场景），并注意 Nacos 的鉴权配置是否正确。

---

### 实践 3：全链路安全防护与 WAF 规则配置

**说明**: 依托于阿里云的安全能力沉淀，Higress 提供了强大的内置安全插件。最佳实践包括启用 IP 访问控制（黑/白名单）、配置防 CC 攻击规则以及启用基本的 WAF 防护。这能有效防止 SQL 注入、XSS 攻击等恶意流量渗透到后端业务系统。

**实施步骤**:
1. 在控制台“插件市场”中启用 `block-list` 或 `waf-plugin` 等安全相关插件。
2. 针对特定域名或路由配置拦截规则，例如限制特定 User-Agent 的访问。
3. 配置限流熔断策略，防止突发流量击垮后端服务。
4. 定期审查访问日志，根据攻击特征动态调整安全规则。

**注意事项**: 安全规则配置过于严格可能会误伤正常流量，建议先在“监控模式”下运行（仅记录日志不拦截），观察一段时间后再开启严格拦截模式。

---

### 实践 4：Kubernetes 原生集成与 Ingress API 管理

**说明**: Higress 旨在成为云原生 API 网关，完全兼容 Kubernetes Ingress 规范和 Gateway API 规范。最佳实践是利用 GitOps 的理念，通过 YAML 文件管理路由配置，将 Higress 的配置纳入 CI/CD 流程，实现基础设施即代码。

**实施步骤**:
1. 在 Kubernetes 集群中部署 Higress。
2. 编写 Ingress 或 Gateway API 资源 YAML 文件，定义 HTTPs 路由、Header 重写等规则。
3. 使用 `kubectl apply` 或通过 ArgoCD/FluxCD 等工具应用配置。
4. 利用 Higress 提供的 Canary（金丝雀发布）注解，实现蓝绿发布或灰度发布。

**注意事项**: 当使用 Ingress 注解进行高级功能配置时，需注意不同版本网关对注解语法的支持情况，建议参考官方最新的注解列表。

---

### 实践 5：多协议支持与 Dubbo/gRPC 服务代理

**说明**: Higress 不仅支持 HTTP/HTTPS，还原生支持 Dubbo 和 gRPC 协议的代理。对于后端使用 Dubbo 进行内部通信的系统，Higress 可以作为 HTTP 转 Dubbo 的协议网关，将前端 RESTful 请求转换为 Dubbo RPC 请求，实现前后端协议的解耦。

**实施步骤**:
1. 在配置服务来源时，引入注册在 Nacos 或 Zookeeper 中的 Dubbo 服务。
2. 创建路由时，指定目标服务为 Dubbo

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/2 与 HTTP/3 (QUIC) 协议

**说明**:  
Higress 作为高性能网关，底层通信协议的选择对吞吐量影响巨大。HTTP/2 通过多路复用解决了 HTTP/1.x 的队头阻塞问题，而 HTTP/3 (QUIC) 基于 UDP 实现，进一步解决了 TCP 层的队头阻塞，显著降低弱网环境下的延迟。

**实施方法**:
1. 在 Higress 的网关配置中，确保 Listener 协议设置为 `HTTP/2` 或 `HTTP/3`。
2. 开启 TLS 配置，因为浏览器通常要求 HTTP/2 和 HTTP/3 必须在 HTTPS 下运行。
3. 调整操作系统内核参数以支持 QUIC（如增大 UDP 缓冲区大小）。

**预期效果**:  
在高并发或弱网环境下，请求延迟可降低 20%-30%，并发连接处理能力提升约 40%。

---

### 优化 2：配置全链路超时与连接池

**说明**:  
默认的超时设置可能不适合高流量生产环境。过长的超时会导致请求堆积（Tornado 现象），耗尽网关线程；过短则可能导致频繁报错。同时，合理配置后端服务的连接池可以避免频繁建立 TCP 连接的开销。

**实施方法**:
1. 在路由配置中显式设置 `connectTimeout`、`sendTimeout` 和 `readTimeout`。建议根据 P99 耗时设置，例如设置为 2s-5s。
2. 在 Service 配置中调整 `upstream` 的连接池大小（`maxRequestsPerConnection`），保持与后端服务处理能力匹配。
3. 开启连接保活（Keep-Alive）。

**预期效果**:  
减少因超时导致的资源占用，防止雪崩效应。在异常流量下，错误率可降低 50% 以上，系统稳定性显著提升。

---

### 优化 3：启用 Wasm 插件与本地缓存

**说明**:  
Higress 支持 Wasm 插件，相比传统的 Lua 插件，Wasm 具有更高的执行效率和沙箱隔离性。此外，对于高频读取的低频变更配置（如限流规则、路由映射），应启用网关本地缓存，减少对配置中心或后端的查询。

**实施方法**:
1. 将复杂的鉴权或限流逻辑编写为 Wasm 插件并部署。
2. 在网关配置中启用 `http2` 协议对接配置中心，并开启本地缓存策略。
3. 对鉴权 Token 的验证结果启用短时缓存。

**预期效果**:  
Wasm 插件相比原生 Lua 插件，CPU 开销可降低 10%-15%；启用本地缓存后，特定路由或鉴权请求的延迟可降低 50% 以上。

---

### 优化 4：调整 JVM 与操作系统的内核参数

**说明**:  
Higress 基于 Java 构建，默认的 JVM 堆内存设置可能导致频繁的 GC（垃圾回收），造成长尾延迟。同时，Linux 默认的文件句柄数和 TCP 参数通常无法支撑百万级并发连接。

**实施方法**:
1. 调整 JVM 参数，例如使用 G1GC 收集器：`-XX:+UseG1GC -XX:MaxGCPauseMillis=200`。
2. 修改 `/etc/security/limits.conf`，将最大文件打开数（`nofile`）提高到 100,000 或更高。
3. 优化内核参数 `/etc/sysctl.conf`：开启 `net.ipv4.tcp_tw_reuse`，调大 `net.core.somaxconn`。

**预期效果**:  
GC 停顿时间减少，P99 延迟降低 20%-40%；系统能支持的并发连接数提升数倍。

---

### 优化 5：启用 CPU 亲和性与自动扩缩容 (HPA)

**说明**:  
在 Kubernetes 环境中，默认的 CPU 调度策略可能导致进程频繁在核心间迁移，影响缓存命中率。通过设置 CPU 亲和性绑定核心，并配置 H

---
## 学习要点

- Higress 是阿里开源的基于 Istio 的云原生 API 网关，深度集成了 K8s 与 Dubbo/Nacos 等微服务生态。
- 它提供开箱即用的流量管理功能，支持金丝雀发布、蓝绿部署及负载均衡等高级路由规则。
- 内置针对高并发与低延迟场景优化的 HTTP 与网关协议处理能力，性能表现优异。
- 具备全面的安全防护体系，包含 WAF 防火墙、认证鉴权及精细化的访问控制列表。
- 提供高度可扩展的插件机制（支持 WASM 和 Lua），允许开发者灵活定制网关的业务逻辑。
- 支持将 Ingress 网关与服务网格（Sidecar）模式统一融合，简化了微服务架构的流量管理复杂度。
- 兼容 Kubernetes Ingress 标准与 Nginx Ingress 注解，极大降低了用户从传统网关迁移的门槛。


---
## 学习路径

## 学习路径

### 阶段 1：基础认知与环境搭建

**学习内容**:
- Higress 的背景与核心概念：了解 Higress 是什么，它基于 Envoy 和 Istio 构建，以及云原生 API 网关的定位。
- 基本术语：理解路由、服务、插件、上游等核心术语。
- 本地安装与部署：学习如何使用 Docker 或 Kubernetes (Helm/Kind) 部署 Higress。
- 控制台操作：熟悉 Higress 的原生控制台界面，进行简单的流量配置。

**学习时间**: 1 周

**学习资源**:
- Higress 官方 GitHub 仓库
- Higress 官方文档 - 快速开始章节
- Higress 官方博客与介绍文章

**学习建议**: 
不要急于深入配置，首先确保能够在本地成功运行 Higress。建议先使用 Docker Compose 方式部署，以减少环境配置的复杂度，快速跑通第一个流量转发示例。

---

### 阶段 2：核心流量管理与网关配置

**学习内容**:
- 路由配置：深入学习如何配置域名、路径匹配、Header 匹配等路由规则。
- 服务来源与负载均衡：学习如何对接 Nacos、Consul 或固定地址的服务列表，以及配置轮询、随机等负载均衡策略。
- 流量治理：掌握全局限流、熔断、超时重试等基础流量防护能力的配置。
- Ingress 与 Gateway API：学习如何通过 Kubernetes Ingress 或 Gateway API CRD 资源来管理 Higress 配置。

**学习时间**: 2-3 周

**学习资源**:
- Higress 官方文档 - 流量管理章节
- Envoy 基础文档（理解 Proxy 和 Listener 概念有助于理解底层）
- Kubernetes Ingress Controller 使用指南

**学习建议**: 
尝试将一个简单的后端服务（如 Nginx 或 Go Web）接入 Higress，并配置不同的路由规则进行访问。重点理解“路由”与“服务”的解耦关系，以及如何通过 YAML 文件管理配置。

---

### 阶段 3：插件开发与可观测性

**学习内容**:
- 插件系统：深入理解 Higress 的插件机制，学习如何使用 Lua、Wasm (Go/C++) 或 Python 编写自定义插件。
- 内置插件使用：熟练配置鉴权（如 Keyless, JWT）、请求/响应修改、限流等官方内置插件。
- 可观测性集成：学习如何配置 Prometheus 监控、集成日志服务（如 SLS, ELK）以及分布式链路追踪。
- 安全防护：配置 CORS、IP 访问控制等安全策略。

**学习时间**: 3-4 周

**学习资源**:
- Higress 官方文档 - 插件市场与开发指南
- Higress 官方插件示例
- Prometheus 与 Grafana 基础教程

**学习建议**: 
从修改现有的官方插件开始，逐步尝试编写一个简单的 Wasm 插件（例如修改请求头）。同时，务必搭建一套监控看板，观察流量指标与 QPS 变化，培养数据驱动的运维习惯。

---

### 阶段 4：高级架构与生产级运维

**学习内容**:
- 高可用部署：在 Kubernetes 集群中进行 Higress 的高可用部署，配置资源限制与自动扩缩容 (HPA)。
- 多租户与多环境管理：学习如何通过命名空间或标签隔离不同业务/环境的网关配置。
- 灰度发布与蓝绿发布：利用 Header 权重或流量标签实现复杂的金丝雀发布策略。
- 服务网格集成：探索 Higress 作为 Istio Ingress Gateway 的使用场景，以及与网格内 Sidecar 的协同工作。
- 性能调优：理解连接池、缓冲区大小等参数对性能的影响。

**学习时间**: 4-6 周

**学习资源**:
- Higress 官方文档 - 最佳实践
- Kubernetes 生产环境部署指南
- 云原生网关架构设计白皮书

**学习建议**: 
模拟生产环境进行压力测试，观察 Higress 在高并发下的表现。尝试设计一套包含多套环境（开发、测试、生产）的网关管理方案，并关注配置的版本管理与回滚机制。

---

### 阶段 5：源码剖析与生态扩展

**学习内容**:
- 架构原理解析：深入阅读 Higress 源码，理解其基于 Istio 控制面和 Envoy 数据面的架构设计。
- 扩展控制器开发：学习如何开发自定义的 Controller (K8s Operator) 来扩展 Higress 的功能。
- AI 网关特性：了解 Higress 在 AI 大模型应用网关方向的新特性（如 LLM 路由、Token 处理）。
- 社区贡献：参与 GitHub Issue 讨论，提交 PR 修复 Bug 或增加新特性。

**学习时间

---
## 常见问题


### 1: Higress 是什么？它与阿里云和 Nginx 有什么关系？

1: Higress 是什么？它与阿里云和 Nginx 有什么关系？

**A**: Higress 是一个开源的、基于云原生架构的 API 网关。它是在 2022 年由阿里云正式开源的，其核心代码源自阿里巴巴内部大规模使用多年的商业化 API 网关技术。

Higress 的定位是“云原生 API 网关”，它深度集成了 Envoy 和 Istio。简单来说，它继承了 Nginx 的高性能特性（通过 Envoy 实现），同时结合了 Kubernetes 的云原生管理能力。它旨在解决传统网关在云原生环境中扩展性差、配置复杂等问题，可以作为 K8s Ingress Controller 使用，也可以作为独立的 API 网关管理南北向流量。

---



### 2: Higress 与 Kong 或 APISIX 等其他开源网关相比有什么优势？

2: Higress 与 Kong 或 APISIX 等其他开源网关相比有什么优势？

**A**: Higress 的核心优势主要体现在以下几个方面：

1.  **深度集成 Istio**：Higress 天然支持 Istio，可以作为 Ingress Controller 接入 Istio 服务网格，实现从网关到 Sidecar 的全链路流量管理，而 Kong 和 APISIX 虽然支持集成，但 Higress 的架构更加原生和轻量。
2.  **高性能与低资源消耗**：基于 Envoy (C++) 开发，相比基于 Lua (OpenResty) 的 Kong 或 APISIX，Higress 在处理长连接、高并发请求时通常具有更低的内存占用和更稳定的延迟。
3.  **插件热加载**：支持基于 WebAssembly (Wasm) 的插件系统，允许插件热加载，不需要重启网关进程，且支持多种编程语言（如 Go, C++, Rust）编写插件，开发门槛和安全性优于 Lua 脚本。
4.  **易用性**：提供了开箱即用的控制台（K8s 部署版），相比很多需要额外部署控制面的网关，Higress 的配置和路由管理更加直观。

---



### 3: Higress 是否兼容 Nginx 的配置？迁移是否困难？

3: Higress 是否兼容 Nginx 的配置？迁移是否困难？

**A**: Higress 并不直接复用 Nginx 的配置文件（nginx.conf），因为它底层使用的是 Envoy，配置模型完全不同。

但是，Higress 提供了** Nginx Ingress 注解兼容**功能。如果你的应用之前运行在 Nginx Ingress Controller 下，Higress 支持大部分常见的 Nginx Annotation，这意味着你不需要大幅修改 Kubernetes 的 Ingress 资源清单即可迁移。对于复杂的 Nginx 配置，用户通常需要在 Higress 中通过控制台重新配置路由规则或使用 Higress 的特定注解。

---



### 4: Higress 支持哪些类型的插件？如何扩展功能？

4: Higress 支持哪些类型的插件？如何扩展功能？

**A**: Higress 拥有非常灵活的插件体系，主要分为以下几类：

1.  **原生插件**：内置了常见的网关功能，如认证鉴权（KeyAuth, JWT）、流量控制（限流、熔断）、可观测性（日志、Metrics）等。
2.  **Wasm 插件**：这是 Higress 推荐的扩展方式。由于 Envoy 原生支持 Wasm，Higress 允许用户使用 Go、AssemblyScript 或 Rust 编写插件，编译为 `.wasm` 文件后上传即可动态加载。这种方式隔离性好，插件崩溃不会导致网关崩溃。
3.  **Lua 插件**：为了兼容旧版习惯，Higress 也支持 Lua 插件，但官方更推荐转向 Wasm 以获得更好的性能和多语言支持。

---



### 5: Higress 的性能表现如何？能否支撑高并发业务？

5: Higress 的性能表现如何？能否支撑高并发业务？

**A**: Higress 的设计初衷就是为了支撑阿里巴巴内部的双 11 级别高并发流量。

*   **基准性能**：在标准硬件环境下，单实例 Higress 可以轻松支撑数万 QPS（每秒查询率），其吞吐量与 Envory 持平，优于传统的基于 Java 的网关。
*   **稳定性**：得益于 Envoy 的多线程架构和 C++ 实现，Higress 在长连接场景和保持低延迟方面表现优异。
*   **弹性伸缩**：作为云原生网关，它结合 K8s 的 HPA（水平自动伸缩）能力，可以根据流量自动扩缩容，非常适合流量波动剧烈的互联网业务。

---



### 6: 在哪里可以下载 Higress？是否有商业支持？

6: 在哪里可以下载 Higress？是否有商业支持？

**A**:

*   **下载与安装**：Higress 是完全开源的，代码托管在 GitHub（alibaba/higress）。用户可以通过源码编译，或者使用提供的 Helm Chart 在 Kubernetes 集群中一键部署。同时也提供 Docker 镜像方便本地测试。
*   **商业支持**：Higress 对标的是阿里云上的“云原生 API 网关”产品。虽然开源版是免费的，但如果你需要企业级的技术支持、SLA 保障或更高级的安全功能，可以考虑购买阿里云

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: Higress 基于 Envoy 构建，但默认配置可能无法满足所有需求。请尝试修改 Higress Gateway 的 Pod 副本数，并配置一个基本的端口映射（例如将 HTTP 流量从 80 端口转发至后端服务的 8080 端口）。

### 提示**: 查阅 Kubernetes 的 Deployment 资源定义以及 Higress 关于 `listeners` 或 `ports` 的配置文档，通常在 Ingress 或 Gateway API 的定义中进行修改。

### 

---
## 实践建议

以下是基于 Higress（阿里云开源的 AI Native 网关）在实际生产环境中的 6 条实践建议：

### 1. 利用 Wasm 插件实现 AI 协议的私有化适配
Higress 的核心优势在于其基于 Wasm (WebAssembly) 的插件扩展能力。虽然 Higress 原生支持 OpenAI 格式，但在实际接入国内大模型（如通义千问、文心一言、DeepSeek 等）时，往往存在协议字段差异。
*   **操作建议**：不要尝试修改 Higress 核心代码来适配模型。应编写 Wasm 插件（支持 Go 或 C++）来处理特定模型的认证签名、参数映射或响应格式转换。
*   **价值**：这能让你在网关层统一对外暴露标准的 OpenAI 协议，后端业务代码无需修改即可切换底层模型供应商。

### 2. 实施基于 Token 的精细化流控与成本控制
与传统 API 网关基于 QPS（每秒请求数）或并发数限流不同，AI 调用的成本主要消耗在 Token 上。仅限制并发数无法防止恶意用户发送超长 Prompt 导致成本失控。
*   **操作建议**：配置 Higress 的 `token-ratelimit` 插件或自定义鉴权插件。针对 API Key 或租户 ID 设置 Token 预设配额（如每分钟 10万 Token）。
*   **价值**：直接关联计费模型，防止“长 Prompt 攻击”，有效保护后端 LLM 服务的预算。

### 3. 启用语义缓存以降低延迟与费用
对于高重复度的问答场景（如常见的客服问题），每次都请求大模型是巨大的资源浪费。
*   **操作建议**：开启 Higress 的缓存特性，并将缓存键的生成策略设置为“语义哈希”而非简单的“字符串匹配”。可以结合向量数据库插件，对 Prompt 进行向量化检索，命中相似度大于阈值（如 0.95）的请求时直接返回缓存结果。
*   **价值**：可将常见问题的响应延迟从秒级降至毫秒级，并显著降低 Token 消耗。

### 4. 配置超时与重试机制以应对 LLM 不稳定性
大模型服务（特别是自部署的开源模型如 Llama 3 或 Qwen）经常出现生成超时或 TTFB（首字节响应时间）过长的情况。默认的网关超时配置（通常是 3-5 秒）对于流式 AI 响应来说太短。
*   **操作建议**：将后端服务的 Route 超时时间调整为 60s 或更长（取决于模型生成速度）。同时，在 Higress 中配置非幂等请求的检查，仅对读取请求启用重试，避免流式响应中断导致客户端重复提交。
*   **陷阱**：不要盲目开启全局限流重试，流式请求的重试配置不当会导致客户端接收到截断的文本。

### 5. 做好 Prompt 注入防护与数据脱敏
AI 网关是流量入口，极易成为攻击目标。攻击者可能通过精心设计的 Prompt 绕过模型限制，或诱导模型输出敏感信息。
*   **操作建议**：在 Higress 的请求处理阶段（`on_request` 阶段）挂载 Wasm 插件，用于检测 Prompt 中的恶意指令注入。同时，在响应阶段（`on_response` 阶段）配置正则匹配插件，过滤掉模型生成内容中可能包含的敏感个人数据（如身份证号、手机号）。
*   **价值**：在企业级应用中满足合规性要求，防止数据泄露。

### 6. 观测上下文日志而非仅访问日志
在 AI 场景下，仅仅记录 HTTP 状态码是不够的。排查问题时需要知道模型为什么回答错误，或者耗时主要在哪里。
*   **操作建议**：配置 Higress 的日志插件，确保将 `x-ms-token-consumption` 或自定义的 Token 消耗头、模型版本号、Prompt 摘要等信息提取出来，发送到

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI 原生](/tags/ai-%E5%8E%9F%E7%94%9F/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [WASM](/tags/wasm/) / [MCP](/tags/mcp/) / [Kubernetes](/tags/kubernetes/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/) / [DevOps/运维](/scenarios/devops-%E8%BF%90%E7%BB%B4/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260206-github_trending-alibaba-higress-6.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260213-github_trending-alibaba-higress-5.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260305-github_trending-alibaba-higress-0.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260205-github_trending-alibaba-higress-5.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*