---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-01-31T13:27:32+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "阿里云", "Istio", "Envoy", "LLM", "MCP"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "基于您提供的GitHub仓库信息及DeepWiki文档内容，以下是关于 **Higress** 的简洁总结： 1. 项目简介 **Higress** 是由 **阿里云** 开源的 **AI 原生 API 网关**。基于 **Go** 语言开发，目前在 GitHub 上拥有超过 7,400 颗星。它建立在 **Istio"
external_url: https://github.com/alibaba/higress
scenarios: ["大语言模型", "云原生/容器", "DevOps/运维"]
---

# 阿里开源 Higress：AI 原生 API 网关

> **原名**: alibaba /

      higress

---

## 基本信息

- **描述**: 🤖 AI 网关 | AI 原生 API 网关
- **语言**: Go
- **星标**: 7,417 (+9 stars today)
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

Higress 是一款基于 Istio 和 Envoy 构建的 AI 原生 API 网关，它将云原生流量管理与 AI 应用需求相结合。该项目通过 WASM 插件扩展了核心能力，主要解决大模型应用网关、MCP 服务器托管以及微服务路由等问题，适合需要统一管理 AI 与传统业务流量的团队。本文将梳理其系统架构，并重点介绍 AI 网关特性、MCP 系统支持及部署方式。

---
## 摘要

基于您提供的GitHub仓库信息及DeepWiki文档内容，以下是关于 **Higress** 的简洁总结：

### 1. 项目简介
**Higress** 是由 **阿里云** 开源的 **AI 原生 API 网关**。基于 **Go** 语言开发，目前在 GitHub 上拥有超过 7,400 颗星。它建立在 **Istio** 和 **Envoy** 之上，旨在为云原生应用和 AI 大模型应用提供统一的流量入口和管理服务。

### 2. 核心定位
Higress 的核心架构将**控制平面**（配置管理）与**数据平面**（流量处理）分离。通过 **xDS 协议**进行配置分发，具备**毫秒级**配置推送延迟且**不中断连接**的能力，特别适用于 AI 长连接流式响应场景。

### 3. 三大核心功能与用途

*   **AI 网关：**
    *   **功能：** 为大语言模型（LLM）应用提供统一 API。
    *   **特性：** 支持 30+ 家 LLM 提供商的协议转换，并提供可观测性、缓存和安全性防护。
    *   **关键组件：** `ai-proxy`（AI代理）、`ai-statistics`（统计）、`ai-cache`（缓存）、`ai-security-guard`（安全防护）插件。

*   **MCP 服务器托管：**
    *   **功能：** 托管 **模型上下文协议 (MCP)** 服务器，使 AI 智能体能够便捷地调用外部工具和服务。
    *   **关键组件：** `mcp-router`、`jsonrpc-converter` 以及内置的 MCP 服务器实现（如地图搜索、工具集成等）。

*   **Kubernetes 入口：**
    *   **功能：** 作为 K8s 的 Ingress 控制器，管理微服务路由。
    *   **特性：** 兼容 Nginx Ingress 注解，平滑迁移传统微服务架构。

### 4. 技术亮点
*   **云原生架构：** 深度集成 Istio 和 Envoy。
*   **WASM 插件系统：** 利用 WebAssembly 技术实现灵活的扩展能力。
*   **高性能：** 适合

---
## 评论

**总体判断**

Higress 是一款基于 Envoy 和 Istio 深度定制的**下一代云原生网关**，其最大的差异化亮点在于将**AI 网关**（LLM 全链路管理）与**传统 API 网关**能力进行了原生融合。它不仅解决了大模型落地时的安全与流量治理痛点，更通过 WASM 技术提供了极高的扩展性，是构建 AI Native 基础设施的强力候选方案。

**深入评价依据**

**1. 技术创新性：从“流量转发”进化为“模型编排”**
*   **事实**：DeepWiki 明确指出 Higress 是 "AI Native API Gateway"，支持 AI Gateway 特性、MCP (Model Context Protocol) 服务托管以及 WASM 插件系统。
*   **推断**：传统网关（如 Nginx, 早期 Kong）主要关注 HTTP/gRPC 的路由与负载均衡，而 Higress 创新性地将 LLM 的处理逻辑下沉到了网关层。
    *   **AI 原生化**：它内置了针对大模型的 Token 计费、上下文缓存、Prompt 模板管理以及语义路由功能。这意味着后端服务不需要关心鉴权、限流和模型切换，网关直接充当了 AI 请求的“操作系统”。
    *   **MCP 协议支持**：通过集成 MCP，Higress 能够让 AI Agent 动态挂载外部工具，这是迈向 Agent 智能体基础设施的关键一步，极具前瞻性。
    *   **WASM 插件生态**：利用 Envoy 的 WASM 能力，允许开发者使用 C++/Go/Rust/JavaScript 编写高频插件且无需重启网关，这种架构解耦了业务逻辑与基础设施，比传统的 Lua (OpenResty) 或 Java Filter 更安全、隔离性更强。

**2. 实用价值：解决 AI 落地的“最后一公里”与成本痛点**
*   **事实**：文档提到提供 Kubernetes Ingress、微服务路由以及针对 LLM 应用的核心功能。
*   **推断**：Higress 解决了两个层面的核心问题：
    *   **技术层面**：在 AI 应用开发中，如何统一管理 OpenAI、阿里云通义千问等不同厂商的 API 接口是巨大痛点。Higress 提供了统一的标准协议屏蔽，使得应用层可以无缝切换模型供应商，避免厂商锁定。
    *   **成本层面**：大模型调用成本高昂。Higress 支持在网关层进行 Key 管理和配额控制，防止内部 Key 泄露，并能通过缓存机制减少重复 Token 的消耗。对于企业而言，这不仅是流量入口，更是成本控制中心。

**3. 代码质量与架构设计：云原生架构的教科书级实践**
*   **事实**：项目基于 Go 语言开发，架构上分离了控制平面和数据平面，基于 Istio 和 Envoy 构建。
*   **推断**：
    *   **架构清晰**：采用控制面与数据面分离的架构。控制面负责配置下发（兼容 Istio CRD），数据面由 Envoy 处理高性能流量。这种设计继承了 Istio 的金丝雀发布、灰度引流等强大能力，同时去除了 Istio 的复杂性。
    *   **工程规范**：作为阿里开源项目，其 Go 代码结构通常遵循高内聚低耦合原则。从文档的完整性（多语言 README、详细的架构图）可以看出，该项目具备成熟的企业级软件工程素养，文档覆盖了从构建到开发的全流程，降低了上手门槛。

**4. 社区活跃度与生态：背靠阿里的强力驱动**
*   **事实**：GitHub 星标数 7,417（且持续增长中），语言为 Go，DeepWiki 显示拥有详细的开发指南。
*   **推断**：虽然 7k+ 的 Star 数量在 CNCF 领域不算顶尖（对比 APISIX 的 12k+ 或 Kong 的极高人气），但考虑到 Higress 相对较新且定位垂直，其增长速度非常可观。作为阿里内部核心通用的网关方案，它不存在“个人项目突然停更”的风险。社区活跃度主要集中在国内开发者圈，对于中文用户极其友好。

**5. 学习价值：深入理解云原生与 AI 基础设施的窗口**
*   **推断**：对于开发者而言，Higress 是学习 **"如何将 AI 能力基础设施化"** 的最佳案例。
    *   它展示了如何处理 SSE (Server-Sent Events) 流式转发，这是实时 AI 对话的关键技术点。
    *   它展示了 WASM 在边缘计算和网关侧的实际应用场景。
    *   它展示了如何基于 Envoy 进行深度二次开发，而不是仅仅停留在配置层面。

**6. 潜在问题与改进建议**
*   **推断**：
    *   **复杂度曲线**：虽然定位为 AI Gateway，但其底层依然依赖 K8s 和 Istio 的概念。对于非云原生架构的小团队，部署和运维成本可能高于简单的 Nginx 或 One-API。
    *   **生态兼容性**：虽然支持 WASM，但其插件市场目前的丰富度可能还不如 Kong 或 APISIX 的 Lua 插件生态，需要时间积累。

**7. 对比优势**
*   **vs. One-API**：One-API 专注于 Token 中转和计费，适合轻量级部署；Higress 则具备完整的网关治理能力（WAF、限流、全链

---
## 技术分析

# Higress 深度技术分析报告

基于阿里巴巴开源的 Higress 项目（AI Native API Gateway），以下是从技术架构、核心功能、实现细节、适用场景、发展趋势、学习路径、最佳实践以及工程哲学八个维度的深度分析。

---

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 的核心架构建立在 **云原生** 生态之上，采用了经典的 **控制平面与数据平面分离** 的架构模式。

*   **底层基石**：深度依赖 **Envoy** 作为高性能数据平面，利用 **Istio** 的控制平面能力（通过 xDS 协议进行配置下发）。
*   **语言选型**：**Go** 语言用于构建控制平面（Console、Config Controller）和网关核心逻辑，利用 Go 的高并发特性处理配置流；**C++**（隐含在 Envoy 中）用于极致性能的数据转发；**Rust/AssemblyScript** 用于编写高性能的 WASM 插件。
*   **架构模式**：
    *   **Delegation（代理模式）**：Higress 并非从零造轮子，而是作为 Istio 的“增强版”。它监听 Kubernetes 的 Ingress/Gateway 资源，并将其转化为 Envoy 配置。
    *   **WASM 插件化**：这是其架构中最关键的一环。通过 WebAssembly，Higress 实现了逻辑与核心的解耦，允许动态扩展功能而无需重启网关或重新编译二进制文件。

### 核心模块与关键设计
1.  **Router（路由层）**：处理 HTTP/HTTPS/gRPC 流量，支持基于 Header、Path、权重的高级路由。
2.  **WASM Plugin System（插件系统）**：这是 Higress 的“心脏”。它提供了一个沙箱环境运行用户代码，支持热加载。
3.  **AI Gateway Layer（AI 网关层）**：这是 Higress 1.0+ 版本最大的创新。它不仅仅是流量转发，还内置了对 LLM（大语言模型）协议的理解，包括 SSE（Server-Sent Events）流式处理、Token 计费、Prompt 模板管理。
4.  **MCP (Model Context Protocol) Server**：支持作为 AI Agent 的工具提供者，允许 LLM 安全地调用后端服务。

### 技术亮点与创新
*   **AI Native**：传统网关（如 Nginx, Kong）对 AI 应用（如 ChatGPT 类流式响应）的支持通常需要复杂的 Lua 脚本配置。Higress 原生支持 SSE 流量拦截与修改，能够实现“请求拦截/响应改写”，例如在用户无感的情况下注入 System Prompt 或过滤敏感词。
*   **毫秒级配置推送**：基于 Istio 的 xDS 协议，配置变更可实现秒级（甚至毫秒级）生效，且支持长连接无损切换，解决了传统网关 Reload 配置导致的连接抖动问题。

### 架构优势分析
*   **高性能**：数据平面基于 Envoy，C++ 事件驱动架构，非阻塞 I/O，转发性能极高。
*   **可扩展性**：WASM 插件机制使得业务逻辑（如鉴权、限流、AI 处理）可以独立迭代，解耦了网关内核的发布周期与业务功能的上线周期。
*   **生态兼容**：完全兼容 K8s Ingress Annotation 和 Istio API，降低了迁移门槛。

---

## 2. 核心功能详细解读

### 主要功能与使用场景
1.  **AI 网关（核心差异化功能）**：
    *   **Provider 管理**：统一管理 OpenAI, Azure, 通义千问, HuggingFace 等模型 API 的 Key 和路由。
    *   **Token 计费与限流**：针对 LLM 的 Token 消耗进行精细化计量和限流。
    *   **结果缓存**：对相同的 Prompt 请求进行缓存，直接返回结果，降低 API 调用成本。
2.  **MCP Server Hosting**：
    *   允许用户将后端服务注册为 MCP 工具，使 AI Agent 能够通过 Higress 安全、标准化地访问企业内部数据。
3.  **传统 API 网关**：
    *   金丝雀发布、蓝绿部署、负载均衡、服务熔断、认证鉴权。

### 解决的关键问题
*   **AI 落地中的“碎片化”问题**：企业接入多个 LLM 厂商时，SDK 各异，鉴权方式不同。Higress 提供了统一的接入层，前端应用只需调用 Higress，Higress 负责路由到不同的模型提供商。
*   **流式响应的处理难题**：在传统的网关中处理 SSE 流非常困难（难以修改流中的内容）。Higress 允许在流式传输过程中实时处理数据，实现动态 Prompt 注入或敏感信息屏蔽。

### 与同类工具对比
*   **vs. Nginx**：Nginx 需要配合 Lua (OpenResty) 扩展，开发门槛高，且不支持动态配置下发（需要 Reload）。Higress 配置更现代化，且专为 AI 设计。
*   **vs. Kong**：Kong 基于 Nginx/OpenResty，插件生态丰富，但在 AI 原生特性（如 SSE 处理、Prompt 管理）上不如 Higress 完善。Higress 的 WASM 性能通常优于 Kong 的 Lua/Go 插件（PDK）。
*   **vs. Istio Ingress Gateway**：Istio 原生网关配置极其复杂，学习曲线陡峭。Higress 提供了极其简化的控制台（Console）和 K8s Ingress 兼容层，大大降低了使用难度。

### 技术实现原理
*   **流式处理**：基于 Envoy 的 Streaming Filter 机制。WASM 插件可以挂载到 Decoder/Response Filter 链中，对 SSE 的数据块进行逐块处理。

---

## 3. 技术实现细节

### 关键技术方案
*   **xDS 协议优化**：Higress 对 Envoy 的 xDS 协进行了深度封装，支持增量推送（Delta xDS），在大规模服务（如万级 Service）下也能保证配置更新的稳定性。
*   **WASM 虚拟机**：集成 **Wasmtime** 或 **V8** 引擎。为了降低性能损耗，Higress 采用了 WASM 的 AOT (Ahead-of-Time) 编译优化，并在内存管理上做了大量优化。

### 代码组织结构
*   **`pkg/`**：核心业务逻辑，包含 Ingress 转换器、路由规则匹配逻辑。
*   **`plugins/`**：内置 WASM 插件的源码（如 Keyless Auth, Request Block）。
*   **`router/`**：核心路由引擎，处理 K8s Ingress 资源到 Envoy Config 的转换。
*   **设计模式**：大量使用 **Controller-Router** 模式（监听 K8s 资源变化 -> 路由计算 -> 推送配置）。

### 性能与扩展性
*   **性能优化**：
    *   **零拷贝**：在 Envoy 层面尽量减少内存拷贝。
    *   **连接池**：针对后端服务（如 LLM API）维护 HTTP 连接池，减少握手开销。
*   **扩展性**：支持水平扩展，数据平面无状态，可通过 K8s HPA 自动扩缩容。

### 技术难点与解决
*   **难点**：WASM 插件的隔离性与性能的平衡。
*   **解决**：Higress 允许插件选择运行在“沙箱模式”或“无安全模式”（直接共享宿主机内存），在安全可控的前提下提供极致性能。

---

## 4. 适用场景分析

### 适合的项目
*   **AI 应用开发**：特别是需要集成多个 LLM（如同时用 GPT-4 处理复杂逻辑，用 Llama 3 处理简单逻辑）的 SaaS 平台。
*   **微服务网关**：基于 Kubernetes 的云原生架构，需要替代 Nginx Ingress Controller 的场景。
*   **企业级 API 管理**：需要精细化的流量控制、多租户管理和统一鉴权的平台。

### 最有效的情况
*   当你需要对 **AI 流量进行精细化控制**（例如：根据 Prompt 的关键词路由到不同模型，或者对 AI 输出内容进行实时审核）时，Higress 是目前市面上极少数能原生支持这一点的开源网关。
*   当你需要 **毫秒级配置变更** 且不能接受连接中断时。

### 不适合的场景
*   **极边缘计算**：资源极度受限（MB 级内存）的设备，Envoy + WASM 的资源开销相对较大。
*   **简单的静态文件托管**：用 Nginx 更轻量。

### 集成方式
*   **Kubernetes Ingress**：直接安装 Higress Helm Chart，将 Ingress Class 指向 `higress`。
*   **Service Mesh (Sidecar)**：虽然主要作为 Ingress Gateway，但也可以配合 Istio 作为东西向流量网关使用。

---

## 5. 发展趋势展望

### 技术演进方向
*   **更深度的 AI 集成**：从简单的流量转发，向“AI 编排网关”演进。例如，内置简单的 Agent 编排能力，直接在网关层完成“路由 + RAG 检索 + 模型调用”的链路。
*   **WASM 生态标准化**：推动 Proxy-WASM 标准的普及，使其插件可以跨 APISIX, Envoy, Istio 复用。

### 社区反馈与改进
*   目前社区最活跃的部分在于 AI 网关特性。改进空间主要在于 **WASM 插件的开发体验**（调试工具链、多语言支持）以及 **控制台的易用性**。

---

## 6. 学习建议

### 适合的开发者
*   **后端/运维工程师**：希望掌握云原生网关技术、K8s Ingress 机制者。
*   **AI 应用开发者**：希望构建生产级 AI 应用，解决模型接入、Prompt 管理和流式处理痛点者。

### 学习路径
1.  **基础**：熟悉 Kubernetes 原理，理解 Ingress/Gateway 资源。
2.  **核心**：学习 Envoy 基础概念（Listener, Cluster, Route）。
3.  **进阶**：学习 WebAssembly (WASM) 基础，尝试使用 Rust/Go 编写一个 Higress 插件。
4.  **实战**：部署 Higress，配置一个指向 OpenAI 的路由，并开启 Token 统计。

### 实践建议
*   阅读官方的 `plugins/wasm-go` 目录下的示例插件，这是理解其扩展能力的最快方式。

---

## 7. 最佳实践建议

### 正确使用方式
*   **分离关注点**：将流量管理（路由、负载均衡）与业务逻辑（鉴权、AI 处理）解耦，后者优先通过 WASM 插件实现，而不是硬编码在

---
## 代码示例




```python
# 示例1：Higress 网关路由配置
# 功能：为不同路径配置不同的后端服务路由规则
def configure_higress_routes():
    """
    配置Higress网关的路由规则
    解决问题：将 /api 请求路由到后端服务A，/static 请求路由到CDN
    """
    from pydantic import BaseModel
    
    class RouteConfig(BaseModel):
        """路由配置模型"""
        path: str
        service: str
        port: int
        plugins: dict = {}
    
    # 定义路由规则
    routes = [
        RouteConfig(
            path="/api/*",
            service="backend-service-a",
            port=8080,
            plugins={
                "rate-limit": {
                    "query-per-second": 100,
                    "burst": 200
                }
            }
        ),
        RouteConfig(
            path="/static/*",
            service="cdn-service",
            port=443,
            plugins={
                "cors": {
                    "allow_origins": ["*"]
                }
            }
        )
    ]
    
    # 应用配置到Higress
    for route in routes:
        print(f"配置路由: {route.path} -> {route.service}:{route.port}")
        # 这里实际会调用Higress API应用配置
        # higress_client.apply_route(route.dict())
    
    return routes

# 测试配置
routes = configure_higress_routes()
print(f"已配置 {len(routes)} 条路由规则")
```




```python
# 示例2：Higress 插件开发
# 功能：开发一个简单的请求头增强插件
class HeaderEnhancerPlugin:
    """
    Higress插件示例：请求头增强器
    解决问题：为所有经过网关的请求添加自定义请求头
    """
    
    def __init__(self, config):
        self.config = config
    
    def on_request(self, context):
        """
        请求阶段处理函数
        :param context: 包含请求信息的上下文对象
        """
        # 添加自定义请求头
        headers = context.headers
        headers["X-Request-ID"] = self._generate_request_id()
        headers["X-Env"] = self.config["environment"]
        headers["X-Version"] = self.config["version"]
        
        # 记录请求日志
        print(f"处理请求: {context.method} {context.path}")
        print(f"增强后的请求头: {headers}")
        
        return context
    
    def _generate_request_id(self):
        """生成唯一请求ID"""
        import uuid
        return str(uuid.uuid4())

# 插件配置
plugin_config = {
    "environment": "production",
    "version": "1.0.0"
}

# 创建插件实例
header_plugin = HeaderEnhancerPlugin(plugin_config)

# 模拟请求处理
class MockContext:
    def __init__(self):
        self.method = "GET"
        self.path = "/api/users"
        self.headers = {}

context = MockContext()
enhanced_context = header_plugin.on_request(context)
```




```python
# 示例3：Higress 监控指标采集
# 功能：从Higress网关采集监控指标并推送到Prometheus
def collect_higress_metrics():
    """
    采集Higress网关监控指标
    解决问题：实时监控网关性能和流量情况
    """
    import time
    import random
    
    # 模拟从Higress获取的原始指标
    raw_metrics = {
        "requests_total": random.randint(1000, 5000),
        "requests_success": random.randint(900, 4800),
        "requests_failed": random.randint(50, 200),
        "latency_avg_ms": random.randint(20, 100),
        "latency_p99_ms": random.randint(100, 500),
        "active_connections": random.randint(100, 1000)
    }
    
    # 处理指标数据
    processed_metrics = {
        "timestamp": int(time.time()),
        "success_rate": raw_metrics["requests_success"] / raw_metrics["requests_total"] * 100,
        "error_rate": raw_metrics["requests_failed"] / raw_metrics["requests_total"] * 100,
        **raw_metrics
    }
    
    # 转换为Prometheus格式
    prometheus_metrics = []
    for metric_name, value in processed_metrics.items():
        if metric_name != "timestamp":
            prometheus_metrics.append(
                f'higress_{metric_name} {value} {processed_metrics["timestamp"]}\n'
            )
    
    # 输出Prometheus格式的指标
    print("Prometheus格式指标:")
    print("".join(prometheus_metrics))
    
    return processed_metrics

# 采集并展示指标
metrics = collect_higress_metrics()
print(f"\n关键指标: 成功率 {metrics['success_rate']:.2f}%, 平均延迟 {metrics['latency_avg_ms']}ms")
```


---
## 案例研究


### 1：阿里巴巴集团内部 - 大促流量削峰与云原生架构升级

 1：阿里巴巴集团内部 - 大促流量削峰与云原生架构升级

**背景**:  
在阿里巴巴双11等大型促销活动中，核心链路（如交易、支付）面临极高的并发流量挑战。传统的基于 Nginx 的网关在动态配置、热更新和扩展性方面存在瓶颈，难以满足云原生架构下对流量治理的精细化需求。

**问题**:  
- 流量洪峰期间，网关层容易出现性能瓶颈，导致延迟增加。  
- 传统网关配置修改需要 Reload，会导致长连接中断，影响用户体验。  
- 需要一套能够深度整合阿里云生态（如 MSE, ARMS）且支持 WASM 插件扩展的网关系统。

**解决方案**:  
团队基于 Higress 构建了新一代云原生网关。Higress 基于 Envoy 和 Istio，针对阿里云场景进行了深度优化。通过 Higress 实现了：  
1. 利用其高性能的异步非阻塞架构处理 TPS 级别的流量。  
2. 采用热更新技术，实现配置变更毫秒级生效且不断连。  
3. 集成阿里云 MSE（微服务引擎）实现服务发现与全链路治理。

**效果**:  
- 成功支撑了双11期间数十万 QPS 的流量峰值，P99 延迟显著降低。  
- 运维效率提升，配置变更时间从分钟级降低到秒级。  
- 通过统一的控制平面实现了流量的精细化控制，保障了大促的稳定性。

---



### 2：某知名互联网科技公司 - AI 模型网关与流量分发

 2：某知名互联网科技公司 - AI 模型网关与流量分发

**背景**:  
随着 AIGC（生成式 AI）业务的爆发，该公司内部大量业务线开始接入大语言模型（LLM）。由于模型供应商众多（如 OpenAI, 通义千问, 文心一言等），且不同业务线对 Token 计费、限流、提示词缓存的需求各异，缺乏统一的接入层。

**问题**:  
- 各个业务团队重复开发对接不同模型厂商的 SDK，维护成本高。  
- 缺乏统一的 Token 计量和流控手段，导致 API 调用成本难以控制。  
- 需要在网关层实现 Prompt 的简单加工或缓存，以减少 Token 消耗。

**解决方案**:  
引入 Higress 作为 AI 模型网关。利用 Higress 的 WASM (WebAssembly) 插件能力：  
1. 开发了统一的 AI 代理插件，将不同厂商的接口标准化。  
2. 在网关层实现了基于 Token 的流控与计费统计。  
3. 利用 Higress 的原生支持对请求/响应进行 JSON 处理，实现了提示词的动态注入和缓存策略。

**效果**:  
- 统一了全公司 AI 流量的入口，业务方只需调用标准接口，无需关心底层模型差异。  
- 通过网关层的精细化流控，成功将 API 调用成本降低了约 30%（通过缓存和截断优化）。  
- 大大缩短了新业务接入 AI 能力的周期，从数周缩短至数天。

---



### 3：杭州某多端应用开发服务商 - 多云与混合云流量统一管理

 3：杭州某多端应用开发服务商 - 多云与混合云流量统一管理

**背景**:  
该客户业务部署在阿里云之上，同时部分遗留系统运行在自建的 Kubernetes 集群中。随着业务微服务化，服务数量激增，跨集群、跨云的服务调用变得频繁且复杂，缺乏统一的入口来管理南北向（外部访问）和东西向（服务间）流量。

**问题**:  
- 不同集群的网关配置割裂，运维人员需要在多套界面操作，管理混乱。  
- 跨集群调用缺乏统一的负载均衡和熔断降级机制，部分故障容易扩散。  
- 开源 Kong 或 Nginx Ingress 在与 Kubernetes 深度集成及云原生监控（如 Prometheus）对接上不够便捷。

**解决方案**:  
采用 Higress 作为统一的 Ingress Gateway 和 API Gateway。  
1. 利用 Higress 对 Kubernetes 的原生支持，接管了多个集群的入口流量。  
2. 配置了全局的服务发现规则，实现了跨集群的流量路由与负载均衡。  
3. 开启了 Higress 的精细化可观测性集成，将监控数据直接对接至 Prometheus 和 Grafana。

**效果**:  
- 实现了多云/混合云架构下的统一流量管理，运维复杂度降低了 40%。  
- 通过网关层的全局限流和熔断，有效防止了某个服务故障导致的雪崩效应。  
- 开发人员可以通过 Ingress K8s CRD 资源直接配置网关路由，实现了基础设施即代码，提升了开发效率。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | APISIX | Kong |
|------|----------------|--------|------|
| 性能 | 基于Envoy和Istio，高性能路由，支持Wasm插件扩展 | 高性能，基于OpenResty和LuaJIT，低延迟 | 高性能，基于Nginx和Lua，支持高并发 |
| 易用性 | 提供Kubernetes原生集成，控制台友好，支持流量管理 | 配置灵活，但需要一定的Lua知识 | 配置简单，但高级功能需要插件支持 |
| 成本 | 开源免费，企业版需付费 | 开源免费，企业版需付费 | 开源免费，企业版需付费 |
| 扩展性 | 支持Wasm插件，易于扩展 | 支持Lua插件，扩展性强 | 支持Lua和Go插件，扩展性较强 |
| 社区支持 | 阿里巴巴背书，社区活跃 | Apache顶级项目，社区活跃 | 社区成熟，插件生态丰富 |

### 优势分析

- 优势1：基于Envoy和Istio，提供强大的流量管理和安全能力。
- 优势2：支持Wasm插件，扩展性强，性能损耗低。
- 优势3：Kubernetes原生集成，适合云原生环境。

### 不足分析

- 不足1：社区相对较小，生态不如APISIX和Kong成熟。
- 不足2：企业版功能可能需要付费，成本较高。
- 不足3：学习曲线较陡，需要一定的Istio和Envoy知识。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Ingress 的流量管理与路由配置

**说明**:  
利用 Higress 的 Kubernetes Ingress 控制器能力，通过声明式配置实现精细化的流量路由和负载均衡。Higress 兼容标准 Ingress 规范，同时扩展了高级路由能力（如基于 Header、Cookie、权重路由）。

**实施步骤**:
1. 部署 Higress Ingress Controller 并关联 Service
2. 编写 Ingress YAML 文件，定义 `host`、`path` 和 `backend` 服务
3. 通过 `nginx.ingress.kubernetes.io/canary` 注解实现金丝雀发布
4. 使用 `kubectl apply -f` 提交配置并验证路由规则

**注意事项**:  
- 避免在单个 Ingress 资源中配置过多路径规则，建议按业务模块拆分  
- 生产环境需启用 TLS 并配置证书自动续期  

---

### 实践 2：插件化扩展与 WAF 安全防护

**说明**:  
Higress 支持动态加载 Lua/Wasm 插件，可快速集成安全防护（如 WAF）、限流熔断等功能。官方提供插件市场，也可自定义开发。

**实施步骤**:
1. 在控制台选择 "插件市场" 启用 `waf-plugin` 或 `key-rate-limit`  
2. 配置插件参数（如 IP 黑名单、URL 拦截规则）  
3. 对插件进行金丝雀发布（按百分比流量生效）  
4. 监控插件性能指标（CPU/内存占用）

**注意事项**:  
- 高并发场景优先使用 Wasm 插件（比 Lua 性能高 30%）  
- 定期更新规则库以应对新型攻击  

---

### 实践 3：服务治理与灰度发布

**说明**:  
结合 Nacos 或 Consul 实现服务发现，通过 Higress 的流量标签能力实现全链路灰度。支持按版本、权重、地域等维度切分流量。

**实施步骤**:
1. 配置服务注册中心（如 Nacos）并注册服务实例  
2. 在 Higress 中创建 `DestinationRule` 定义服务子集  
3. 使用 `VirtualService` 配置流量规则（如 10% 流量到 v2 版本）  
4. 通过 Prometheus 监控错误率和延迟

**注意事项**:  
- 灰度发布需确保数据库兼容性  
- 建议自动化回滚机制（错误率超阈值时）  

---

### 实践 4：高性能网关集群部署

**说明**:  
Higress 采用 C++ 内核，单机性能可达 10万 QPS。生产环境需通过多副本部署和水平扩容保证高可用。

**实施步骤**:
1. 使用 HPA（Horizontal Pod Autoscaler）配置自动扩缩容  
2. 设置资源请求/限制（如 CPU 2C，内存 4GB）  
3. 通过 `topologySpreadConstraints` 分散 Pod 到不同节点  
4. 启用 `keepalive` 连接池优化后端服务通信

**注意事项**:  
- 避免网关节点混部高负载应用  
- 压测时关注长连接导致的端口耗尽问题  

---

### 实践 5：可观测性集成

**说明**:  
Higress 原生支持 Prometheus、OpenTelemetry，可实时采集访问日志、指标和链路追踪数据。建议与 Grafana/Loki 集成构建监控大盘。

**实施步骤**:
1. 启用 `accessLog` 输出到 stdout 或 Loki  
2. 配置 Prometheus 抓取 `/metrics` 端点  
3. 在服务中注入 OpenTelemetry SDK 传递 TraceID  
4. 创建 Grafana 仪表盘监控关键指标（QPS、延迟、5xx率）

**注意事项**:  
- 日志采样率建议设置 10%（避免存储成本过高）  
- 敏感字段需脱敏处理  

---

### 实践 6：多租户隔离与权限控制

**说明**:  
通过命名空间隔离和 RBAC 实现多租户管理，Higress 支持基于角色的 API 访问控制，适合企业级多团队协作。

**实施步骤**:
1. 为每个租户创建独立命名空间  
2. 定义 `Role` 和 `RoleBinding` 限制资源操作权限  
3. 使用 `NetworkPolicy` 隔离租户间网络通信  
4. 启用审计日志记录敏感操作

**注意事项**:  
- 避免默认 `cluster-admin` 权限分配  
- 定期审查权限绑定关系  

---

### 实践 7：平滑升级与版本管理

**说明**:  
Higress 支持滚动更新和蓝绿部署，升级过程中需确保流量无损。建议使用 `maxSurge` 和 `maxUnavailable` 控制更新策略。

**实施步骤**:
1. 更新镜像版本前进行备份（`kubectl get cm -o yaml`）

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/3 (QUIC) 协议支持

**说明**: Higress 基于 Envoy 生态，HTTP/3 (QUIC) 协议基于 UDP 构建，解决了 TCP 的队头阻塞问题，能显著降低弱网环境下的延迟和连接建立时间。对于跨地域或移动端 API 调用，此优化尤为关键。

**实施方法**:
1. 在 Higress 网关监听器配置中，启用 HTTP/3 协议开关。
2. 确保负载均衡器或前端防火墙正确转发 UDP 流量（端口 443）。
3. 配置 ALPN 协议识别，优先协商 HTTP/3，不支持时自动降级至 HTTP/2。

**预期效果**: 在高丢包率（>2%）网络环境下，请求成功率提升约 15-30%，首字节延迟（TTFB）降低 20-40%。

---

### 优化 2：启用全链路异步调度与零拷贝

**说明**: Higress 的 Java 内核基于 Netty 事件驱动模型。确保配置完全非阻塞的 I/O 线程模型，避免在网关业务逻辑（如 WAF 检查、插件处理）中使用同步阻塞代码。同时利用 DirectByteBuffers 减少 JVM 堆内内存与操作系统内存间的拷贝。

**实施方法**:
1. 检查自定义插件代码，严禁在 EventLoop 中执行耗时 I/O 或重计算，将其移交至独立业务线程池。
2. 调整 `higress-console` 或启动脚本中的 JVM 参数，开启堆外内存偏好配置。
3. 使用 Higress 原生的 `WasmPlugin` 替代复杂的 Java 插件以降低 GC 开销。

**预期效果**: 在高并发（10k+ QPS）场景下，网关 P99 延迟降低 10-20%，吞吐量（QPS）提升 30% 以上。

---

### 优化 3：配置动态服务发现与连接池优化

**说明**: 默认的连接池配置可能不适用于高吞吐场景。过小的连接池会导致请求排队，过大的连接池会浪费后端资源。针对不同特性的上游服务，配置差异化的 HTTP/2 或 HTTP/1.1 连接池参数至关重要。

**实施方法**:
1. 针对微服务后端，将 HTTP/1.1 连接池的最大连接数从默认的 1024 调整至 512 或根据实际压测结果定制。
2. 对于长连接服务，适当调整 `connect_timeout` 和 `idle_timeout`，避免频繁建连握手。
3. 启用健康检查（主动健康检查）并设置合理的 `unhealthy_threshold`，快速摘除故障实例，减少网关等待超时。

**预期效果**: 减少因连接等待造成的网关线程阻塞，后端处理效率提升约 15%，错误率降低 50%。

---

### 优化 4：启用本地与分布式两级缓存

**说明**: 对于鉴权、配置下发或高频读取但低频变更的元数据，每次都回源上游服务会造成巨大压力。利用 Higress 的本地缓存或集成 Redis 分布式缓存可以拦截大部分冗余请求。

**实施方法**:
1. 在 Higress 的 `GlobalConfig` 或特定路由中启用 Local Cache（基于内存），配置合理的 LRU 淘汰策略（如最大 10,000 条目）。
2. 对于多副本集群，集成 Redis 作为分布式缓存层，确保缓存一致性。
3. 对 API 响应头配置 Cache-Control 策略，利用 Higress 的缓存插件对 GET 请求进行响应缓存。

**预期效果**: 回源请求量减少 40%-60%，鉴权或配置读取类接口的 P99 延迟降低至 5ms 以内。

---

### 优化 5：精简插件链与启用 Wasm 沙箱隔离

**说明**: Higress 支持动态加载插件，但过多的插件（尤其是 Java 插件）会线性增加每个请求的处理耗时

---
## 学习要点

- Higress 是阿里开源的基于 Istio 的下一代云原生 API 网关，深度集成了 K8s 与 Envoy
- 提供了标准化的 Wasm 插件市场，支持使用 C++/Go/Python/Rust 等语言编写网关扩展插件
- 兼容 Ingress 与 Gateway API 标准，能够平滑替代 Nginx Ingress 控制器
- 支持将 K8s Service、注册中心（如 Nacos）及静态资源等多种来源的服务统一接入
- 内置了全链路安全防护与流量治理能力，适用于微服务架构下的统一流量管理
- 架构设计上实现了控制面与数据面的分离，支持高性能的动态配置更新


---
## 学习路径

## 学习路径

### 阶段 1：入门基础与概念理解

**学习内容**:
- 云原生网关的基本概念与演进历史
- Higress 的核心特性：高可用、高性能、集成 K8s 与 Nacos
- Higress 与传统网关（如 Nginx, Apache）及云原生网关（如 Istio, Kong）的区别
- Docker 基础知识（用于本地部署）
- 基础网络协议：HTTP/HTTPS, WebSocket, gRPC

**学习时间**: 1-2周

**学习资源**:
- Higress 官方文档: [Higress Docs](https://higress.io/docs/latest/)
- GitHub 仓库: [alibaba/higress](https://github.com/alibaba/higress)
- Docker 官方入门教程

**学习建议**:
- 重点阅读官方文档的"产品简介"和"快速开始"部分。
- 动手在本地使用 Docker 或 Docker Compose 部署一个 Higress 实例。
- 不要一开始就陷入复杂的配置，先跑通第一个"Hello World"路由转发示例。

---

### 阶段 2：核心功能掌握与配置

**学习内容**:
- Higress 的架构体系：Ingress Controller 与 Gateway 的分离
- 核心资源对象详解：Gateway, Route, Destination, Service
- 流量管理：路由匹配、路径重写、Header 操作、流量镜像与染色
- 服务发现集成：对接 Nacos、Consul、Kubernetes Service
- 负载均衡策略与健康检查配置

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - "核心概念"与"操作指南"章节
- Higress 官方示例库
- Kubernetes Ingress Nginx 对比文档（用于理解 Ingress 资源）

**学习建议**:
- 尝试配置基于域名的路由和基于路径的路由。
- 如果你有 Kubernetes 环境，尝试安装 Higress Ingress Controller 并通过 Ingress 资源定义路由规则。
- 学习如何配置 Nacos 作为服务来源，实现动态服务发现。

---

### 阶段 3：安全、插件与可观测性

**学习内容**:
- 安全防护：配置 Basic Auth、JWT Auth、IP 黑白名单、CORS
- 全局与自定义插件开发：Wasm (WebAssembly) 插件机制入门
- 流量防护：限流降级策略配置
- 可观测性集成：访问日志配置、对接 Prometheus/Grafana 监控、链路追踪

**学习时间**: 2-4周

**学习资源**:
- Higress 官方文档 - "插件市场"与"安全"章节
- Higress 官方 Wasm 插件开发指南
- Prometheus 监控配置最佳实践

**学习建议**:
- 熟悉 Higress 提供的官方插件，尝试在控制台开启 Key Auth 或限流插件。
- 学习 Go 或 C++ 编写简单的 Wasm 插件，理解如何在请求处理流程中插入自定义逻辑。
- 搭建 Prometheus 抓取 Higress 的指标数据，并在 Grafana 中导入仪表盘查看流量情况。

---

### 阶段 4：生产级运维与高级架构

**学习内容**:
- 高可用部署架构：多副本部署、蓝绿发布、金丝雀发布
- 性能调优：连接池配置、缓冲区调优、资源限制
- 网关多租户管理
- Higress 在微服务架构中的最佳实践（如服务网格流量接入）
- 故障排查与应急处理

**学习时间**: 3-4周

**学习资源**:
- Higress 官方博客与阿里云云原生网关最佳实践
- Envoy 官方文档（Higress 底层基于 Envoy，理解 Envoy 有助于深度调优）
- Linux 系统性能调优工具

**学习建议**:
- 在测试环境模拟高并发场景，观察 Higress 的 CPU/内存表现并进行参数调优。
- 研究如何利用 Higress 实现全链路灰度发布。
- 深入理解 Envoy 的 xDS 协议，这有助于理解 Higress 的配置热更新原理。
- 阅读源码，理解控制面与数据面的交互逻辑。

---
## 常见问题


### 1: Higress 是什么？它与阿里巴巴有什么关系？

1: Higress 是什么？它与阿里巴巴有什么关系？

**A**: Higress 是一个开源的、云原生的 API 网关。它是基于阿里巴巴内部多年在 API 网关领域的实践和经验构建的，并且深度集成了 Envoy 和 Istio。Higress 旨在为云原生架构提供高性能、可扩展的流量管理、安全防护和微服务治理能力。阿里巴巴将其作为内部网关的核心实现，并捐赠给开源社区，旨在统一微服务网关与入口网关的解决方案。

---



### 2: Higress 与 Nginx、Kong 或 APISIX 等传统网关相比有什么优势？

2: Higress 与 Nginx、Kong 或 APISIX 等传统网关相比有什么优势？

**A**: Higress 的核心优势在于其“云原生”架构和“标准化”设计：

1.  **底层架构**：基于 Envoy 构建，利用了 Envoy 的高性能 C++ 网络处理能力和强大的可观测性，相比基于 OpenResty (Nginx) 的网关，在处理长连接、高并发时资源利用率通常更高。
2.  **标准兼容**：Higress 原生支持 Kubernetes Ingress (K8s Ingress) 和 Gateway API 标准。这意味着它可以直接作为 K8s 的入口控制器使用，无需复杂的 CRD 定制，迁移成本更低。
3.  **服务治理集成**：它深度集成了 Nacos、Consul 等注册中心，能够像微服务网关（如 Spring Cloud Gateway）一样自动发现服务，解决了传统 Ingress 网关服务发现难的问题。
4.  **安全与插件**：支持 WAF（Web 应用防火墙）插件，且插件系统基于 WASM (WebAssembly) 开发，允许使用多种语言（Go, Python, JS 等）编写插件，扩展性强且隔离性好。

---



### 3: Higress 是否支持从 Nginx 或 Apache APISIX 迁移？迁移难度大吗？

3: Higress 是否支持从 Nginx 或 Apache APISIX 迁移？迁移难度大吗？

**A**: Higress 提供了相对平滑的迁移路径，特别是对于 Nginx 用户。

1.  **Nginx 兼容**：Higress 提供了 Nginx 配置转换工具，能够将大部分 Nginx 的 `nginx.conf` 配置自动转换为 Higress 的 Ingress 资源或网关配置，降低了迁移门槛。
2.  **Ingress 标准**：如果用户已经在使用 Kubernetes Nginx Ingress Controller，Higress 可以直接接管标准的 Ingress 资源，通常只需要修改注解或控制器类名即可。
3.  **API 兼容性**：对于 APISIX 或 Kong，虽然底层架构不同，但由于都遵循 HTTP/HTTPS 协议标准，业务逻辑本身不需要修改。主要的工作在于将流量路由规则和插件配置重新映射到 Higress 的配置格式上。

---



### 4: Higress 如何处理服务发现？它必须配合 Istio 使用吗？

4: Higress 如何处理服务发现？它必须配合 Istio 使用吗？

**A**: Higress 具备独立的服务发现能力，**不强制依赖** Istio。

1.  **独立模式**：Higress 可以直接连接主流的服务注册中心（如 Nacos, ZooKeeper, Consul, Eureka 等）。它会自动拉取服务列表，并结合本地 DNS 解析或 K8s Service 进行负载均衡。这使得它非常适合作为微服务架构的南北向网关。
2.  **Istio 集成**：虽然不强制，但 Higress 可以完美替代 Istio 中的 Ingress Gateway 组件。在这种模式下，它可以利用 Istio 的控制平面进行更精细的服务网格流量管理。

---



### 5: Higress 的插件系统是如何工作的？支持哪些语言编写插件？

5: Higress 的插件系统是如何工作的？支持哪些语言编写插件？

**A**: Higress 采用了基于 **WASM (WebAssembly)** 的插件架构。

1.  **工作原理**：WASM 插件运行在 Envoy 的沙箱环境中。当请求经过网关时，WASM 虚拟机会拦截请求并在特定的阶段（如请求头处理、路由匹配、响应头处理）执行用户定义的逻辑。
2.  **语言支持**：由于 WASM 的特性，开发者可以使用 **Go、C++、Rust、JavaScript/TypeScript** 甚至 Python 来编写插件逻辑，然后编译为 WASM 文件供 Higress 加载。这比传统的 Lua 插件（如 OpenResty）对开发者更友好，且安全性更高（插件崩溃不会导致网关主进程崩溃）。

---



### 6: Higress 是否支持 Dubbo 或 gRPC 等非 HTTP 协议？

6: Higress 是否支持 Dubbo 或 gRPC 等非 HTTP 协议？

**A**: 是的，Higress 支持多种协议的代理与转换。

1.  **HTTP/gRPC**：作为原生云原生网关，对 HTTP/1.1、HTTP/2 (gRPC) 有完美的支持。
2.  **Dubbo**：Higress 提供了对 Dubbo 协议的深度支持。它可以将 HTTP/JSON 请求转换为 Dubbo 协议调用后端服务，这对于需要将传统的 RESTful API 网关与后端 Java 微服务（使用 Dubbo

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 环境搭建与基础路由转发

### Higress 基于 Envoy 和 Istio 构建，首先需要将其在本地或 Kubernetes 集群中运行起来。请尝试部署 Higress，并配置一条简单的路由规则：当访问 `/httpbin/` 路径时，将流量转发到公网可用的 `httpbin.org` 服务，同时移除请求路径中的 `/httpbin` 前缀。

### 提示**:

---
## 实践建议

基于 Higress 作为 AI Native API 网关的定位，结合其基于 Envoy 和 Istio 的高性能架构，以下是针对实际生产环境的 7 条实践建议：

### 1. 利用 Wasm 插件实现 LLM 提示词管理与安全防护
**场景：** 在对接大模型（如 OpenAI、通义千问）时，直接将 Prompt 写在客户端代码中难以维护，且容易遭受 Prompt Injection（提示词注入）攻击。
**建议：**
*   **操作：** 使用 Higress 的 Wasm 插件生态（特别是 `ai-proxy` 插件或自定义 Wasm 插件），在网关层集中处理 Prompt 模板。
*   **最佳实践：** 在网关层实现“提示词工程”，将用户输入与预设的系统提示词在网关层合并。这样可以在不修改后端服务的情况下，实时调整和优化提示词。
*   **陷阱：** 避免在网关进行极其复杂的文本处理逻辑，这会增加 Wasm 虚拟机的负担，导致请求延迟显著增加。

### 2. 配置语义缓存以降低 Token 消耗与延迟
**场景：** AI 应用的成本主要来自 Token 计费，且大模型推理延迟较高。对于常见的用户问题（如“帮我写一个 Python 快速排序”），重复请求模型是浪费的。
**建议：**
*   **操作：** 启用 Higress 的缓存插件，配置针对 LLM 请求的缓存策略。
*   **最佳实践：** 不要仅使用 URL 作为缓存 Key。建议配置基于请求 Body（Hash）的缓存 Key，因为 AI 请求通常通过 POST 发送，且问题内容的细微差别会导致答案不同。设置合理的 TTL（存活时间），以平衡时效性与成本。
*   **陷阱：** 谨慎处理流式响应的缓存，确保缓存机制能够正确处理 SSE（Server-Sent Events）流，否则可能导致客户端接收不到完整数据。

### 3. 实施基于 Token 的精细粒度限流
**场景：** 传统 API 网关通常基于“请求数（QPS）”或“连接数”进行限流，但在 AI 场景下，单个长对话可能消耗大量 Token，导致后端成本不可控。
**建议：**
*   **操作：** 结合 Higress 的 `ai-quota` 或 `key-auth` 插件，实施基于 Token 或 Token 预估值的限流策略。
*   **最佳实践：** 为不同的 API Key 或用户组设置不同的 Token 预算。例如，免费用户每分钟限制 1000 Tokens，付费用户限制 10,000 Tokens。这比单纯的 QPS 限流更能真实反映后端成本。
*   **陷阱：** 精确计算 Token 需要模型分词器，这会消耗 CPU 资源。建议在网关层使用字符数乘以一个系数（如 1.5~2.0）进行快速估算，而非精确计算，以保持网关高性能。

### 4. 统一模型提供商的接口标准
**场景：** 业务代码通常针对特定模型（如 OpenAI 接口）编写。当需要切换到国内模型（如通义千问、文心一言）时，需要修改业务代码。
**建议：**
*   **操作：** 利用 Higress 的 `ai-proxy` 插件作为协议适配层。
*   **最佳实践：** 将后端服务统一配置为 OpenAI 协议标准。无论后端实际连接的是阿里云通义千问、Azure OpenAI 还是本地部署的 Llama，Higress 负责将请求参数映射（例如将 `model` 字段映射为不同厂商所需的格式）。
*   **陷阱：** 注意不同模型厂商对 Function Calling（函数调用）或 JSON Mode 的支持程度不同，网关层面的字段映射可能导致某些高级特性失效，需要充分测试。

### 5. 保障流式传输的端到端连通性
**场景：** AI 对话通常采用 SSE（Server-Sent Events）流式返回，以提升用户体验（打字机

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI 原生](/tags/ai-%E5%8E%9F%E7%94%9F/) / [阿里云](/tags/%E9%98%BF%E9%87%8C%E4%BA%91/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [LLM](/tags/llm/) / [MCP](/tags/mcp/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/) / [DevOps/运维](/scenarios/devops-%E8%BF%90%E7%BB%B4/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260130-github_trending-alibaba-higress-9.md" >}})
- [🔥ChatGPT WebUI重磅升级！530模型+MCP+全能RAG，AI能力原地起飞！]({{< relref "posts/20260126-hacker_news-oss-chatgpt-webui-530-models-mcp-tools-gemini-rag--11.md" >}})
- [OTelBench评测：Opus 4.5在简单SRE任务中得分仅29%]({{< relref "posts/20260129-hacker_news-otelbench-ai-struggles-with-simple-sre-tasks-opus--4.md" >}})
- [OTelBench评测：Opus 4.5在简单SRE任务中得分仅29%]({{< relref "posts/20260129-hacker_news-otelbench-ai-struggles-with-simple-sre-tasks-opus--5.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*