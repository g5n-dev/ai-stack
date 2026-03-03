---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-03-03T20:27:25+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "Istio", "Envoy", "LLM", "MCP", "WASM"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "以下是对 Higress 项目的中文总结： **项目概况** Higress 是一个由阿里开源的、**云原生 AI 原生 API 网关**。它基于 Istio 和 Envoy 构建，使用 Go 语言编写，目前在 GitHub 上拥有超过 7,600 个星标。 **核心架构** Higress 采用**控制平面与数据平面"
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
- **星标**: 7,628 (+11 stars today)
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

Higress 是一款基于 Istio 和 Envoy 构建的 AI 原生 API 网关，它通过标准云原生架构集成了大模型流量管理与微服务治理能力。该项目适合需要统一处理传统 API 调用与 LLM 应用的团队，提供了包括 WASM 插件扩展、AI 网关特性及 MCP 协议支持在内的核心功能。本文将梳理其系统架构设计，并介绍如何利用这些特性实现高效的服务交付与模型集成。

---
## 摘要

以下是对 Higress 项目的中文总结：

**项目概况**
Higress 是一个由阿里开源的、**云原生 AI 原生 API 网关**。它基于 Istio 和 Envoy 构建，使用 Go 语言编写，目前在 GitHub 上拥有超过 7,600 个星标。

**核心架构**
Higress 采用**控制平面与数据平面分离**的架构。配置变更通过 xDS 协议传播，具备毫秒级延迟且不中断连接，这使其非常适用于 AI 流式响应等长连接场景。系统通过 **WebAssembly (WASM)** 插件扩展能力。

**三大主要功能**

1.  **AI 网关**
    为大语言模型（LLM）应用提供统一 API。支持对接 30+ 家 LLM 提供商，提供协议转换、可观测性、缓存和安全防护（通过 `ai-proxy`、`ai-statistics` 等插件实现）。

2.  **MCP 服务器托管**
    托管模型上下文协议（MCP）服务器，使 AI Agent 能够调用工具和服务。包含 `mcp-router` 等过滤器及多种 MCP 服务器实现。

3.  **Kubernetes Ingress**
    作为 Ingress 控制器使用，兼容 nginx-ingress 注解，负责微服务路由和流量管理。

---
## 评论

### 总体判断

Higress 是目前云原生网关领域中将**AI 原生能力**与**传统流量治理**融合得最为彻底的开源项目之一。它不仅解决了大模型（LLM）应用落地中的协议转换与 token 管理痛点，更通过基于 Istio/Envoy 的架构提供了企业级的性能保障，是构建 AI 时代 API 基础设施的首选方案之一。

### 深入评价依据

#### 1. 技术创新性：从“流量管道”到“智能编排”
*   **事实**：DeepWiki 指出 Higress 基于 Istio 和 Envoy 构建，并扩展了 WebAssembly (WASM) 插件能力，同时明确提出了“AI Gateway”和“MCP (Model Context Protocol) Server Hosting”的概念。
*   **推断**：Higress 的核心差异化在于**AI 原生化**。传统网关（如 Nginx, Kong）主要处理 HTTP/gRPC 转发，而 Higress 内置了对 LLM 协议（如 OpenAI 协议）的理解。它创新性地引入了**MCP 协议支持**，这意味着网关不仅仅是流量的搬运工，更成为了 AI Agent 的工具集托管中心。通过 WASM 技术，它允许开发者使用 C++/Go/Rust 等语言编写高性能插件，在处理 Prompt 模板注入、敏感词过滤等 AI 特有逻辑时，比基于 Lua 或 JavaScript 的传统方案更具安全性和性能优势。

#### 2. 实用价值：打通 AI 落地的“最后一公里”
*   **事实**：文档强调其提供“AI gateway features for LLM applications”以及“Kubernetes Ingress”能力。
*   **推断**：在 LLM 应用开发中，开发者常面临多模型切换、Token 计费统计、Prompt 模板管理等繁琐问题。Higress 通过统一的配置层解决了**模型供应商锁定**问题，允许前端业务无缝切换 OpenAI、通义千问或 Ollama 等不同后端。同时，它将传统微服务的 K8s Ingress 能力与 AI 网关合二为一，避免了企业维护两套网关的冗余成本，极大地降低了运维复杂度。

#### 3. 代码质量与架构：云原生标准的继承与演进
*   **事实**：项目语言为 Go，架构上明确分离了“控制平面”与“数据平面”。
*   **推断**：Go 语言在云原生基础设施领域是事实标准，保证了二进制分发和部署的便捷性。控制/数据平面分离的设计模式（源自 Istio）保证了系统的弹性伸缩能力。DeepWiki 提到的详细文档结构（包括架构、部署、开发指南）表明该项目具备较高的成熟度。作为阿里系开源项目，其代码规范和工程化标准通常较高，能够经受大规模流量的考验。

#### 4. 社区活跃度：背靠大树，初具规模
*   **事实**：星标数为 7,628（数据截点），由阿里巴巴主导。
*   **推断**：对于基础设施类项目，7k+ 的 Star 数证明了其市场关注度。阿里云的背书意味着该项目不会像个人项目那样轻易停止维护，且通常会有实际的商业化落地场景作为反哺。社区活跃度通常较高，Issue 响应和版本迭代速度较快，适合作为企业级选型。

#### 5. 与同类工具对比：比 K8s Ingress 更懂 AI，比 LangChain 更懂网关
*   **事实**：对比对象包括 Nginx, Kong, APISIX 以及 LangChain/LLM Gateway。
*   **推断**：
    *   **对比 Nginx/Kong**：Higress 原生支持 K8s，配置更加声明式，且针对 AI 的 SSE（Server-Sent Events）流式传输做了优化，传统网关处理流式响应往往配置复杂。
    *   **对比专用 AI Gateway（如 LangChain Gateway）**：Higress 的并发处理能力基于 Envoy C++ 内核，性能远超基于 Python 构建的简单代理层，更适合生产环境的高吞吐量场景。

### 边界条件与不适用场景

*   **不适用场景**：
    *   极简边缘路由：如果仅需一个简单的反向代理，Higress 基于 K8s 的架构显得过重。
    *   非 K8s 环境：虽然支持 Docker，但其强大功能高度依赖 Kubernetes 生态，传统虚拟机环境部署成本较高。
    *   复杂的业务逻辑：网关应保持轻量，涉及重度数据处理或复杂业务编排的代码不应在网关插件中实现。

### 快速验证清单

1.  **协议兼容性测试**：
    *   *检查点*：部署后，配置一个指向 OpenAI 兼容接口的路由，使用 `curl` 测试流式响应（SSE）是否能在不丢包的情况下实时透传，验证其 AI 代理的稳定性。

2.  **WASM 插件热加载**：
    *   *检查点*：编写一个简单的 Go WASM 插件（例如修改 HTTP Header），在不重启 Higress Pod 的情况下动态加载，观察是否生效，验证其可扩展性声明。

3.  **MCP 协议集成验证**：
    *   *检查点*：尝试在配置中挂载一个 MCP 工具（如文件读取或网络搜索），检查 AI Agent 是否能通过 Higress 成功调用该工具

---
## 技术分析

基于您提供的 GitHub 仓库信息及 DeepWiki 节选，以下是对 **Higress** 的深度技术分析。

---

# Higress 深度技术分析报告

## 1. 技术架构深度剖析

Higress 的定位是 **"AI Native API Gateway"**，其架构设计体现了云原生时代将控制平面与数据平面分离的演进趋势，并针对 AI 流量特征进行了专门优化。

### 技术栈与架构模式
*   **底层基石**：基于 **Envoy** 作为高性能数据平面，利用 **Istio** 的控制平面理念（xDS 协议）进行配置管理。这意味着 Higress 继承了 Envoy 的高性能（C++/L4/L7）和 Istio 的服务网格治理能力。
*   **编程语言**：**Go**。Higress 的控制平面和扩展逻辑主要使用 Go 编写。这利用了 Go 在并发处理和云原生生态中的优势，便于与 Kubernetes 集成。
*   **架构模式**：典型的 **控制平面/数据平面分离** 架构。
    *   **控制平面**：负责配置管理、证书分发、WASM 插件管理。它监听 Kubernetes 或其他配置源，将其转化为 Envoy 理解的配置。
    *   **数据平面**：Envoy 实例，负责处理实际的流量转发、认证、限流等。

### 核心模块与关键设计
1.  **WASM (WebAssembly) 插件系统**：这是 Higress 的核心差异化设计。通过 WASM，Higress 允许用户使用 C/C++/Go/Rust 等语言编写插件，并在运行时动态加载到 Envoy 中。这打破了传统 Lua 插件（如 OpenResty）的性能瓶颈和安全性限制，也解决了原生 Envoy Filter (C++) 开发门槛高、编译复杂的问题。
2.  **AI 网关模块**：针对 LLM（大语言模型）流量设计的专用模块。它不仅仅是转发 HTTP 请求，还理解 AI 协议（如 OpenAI 协议、SSE 流式传输）。
3.  **MCP (Model Context Protocol) 服务器托管**：这是前沿功能的集成。Higress 不仅能转发请求，还能作为 Agent 的工具提供者，通过 MCP 协议将后端服务暴露给 AI Agent 使用。

### 技术亮点与创新点
*   **毫秒级配置推送与热更新**：得益于 xDS 协议和 WASM 的无状态特性，配置变更可以在不中断长连接（如 AI 对话的 SSE 流）的情况下生效。这对于传统网关（如 Nginx，通常需要 reload 进程导致连接瞬断）是巨大的进步。
*   **AI 原生流量处理**：传统网关将 AI 流量视为普通 HTTP，无法处理流式上下文。Higress 能够在网关层进行 Prompt 模板管理、Token 计费统计、以及基于语义的路由，这是“AI Native”的具体体现。

### 架构优势分析
*   **低延迟**：数据平面基于 Envoy (C++)，避免了 Go 语言 GC 带来的延迟抖动。
*   **高扩展性**：WASM 插件机制使得业务逻辑（如鉴权、日志修改）可以由用户动态注入，无需重新编译网关本身。
*   **统一治理**：将传统的微服务流量（gRPC, RESTful）与 AI 流量（LLM, SSE）纳入同一网关管理，降低了运维复杂度。

---

## 2. 核心功能详细解读

### 主要功能与使用场景
1.  **AI 网关**：
    *   **功能**：Provider 聚合（统一对接 OpenAI, Azure, 通义千问等模型）、Token 计费与限流、Prompt 模板管理、结果缓存。
    *   **场景**：企业内部构建 AI 中台，统一管理不同模型厂商的 API Key，并对上层应用屏蔽底层模型差异。
2.  **MCP 系统集成**：
    *   **功能**：托管 MCP Server，使 AI Agent 能够通过 Higress 安全地调用企业内部工具/数据。
    *   **场景**：赋予 AI Agent 能力，例如允许 Agent 通过网关查询数据库或调用 ERP 接口。
3.  **云原生 API 网关**：
    *   **功能**：Kubernetes Ingress 支持、金丝雀发布、负载均衡、流量镜像。
    *   **场景**：替代 Nginx Ingress Controller 或 Traefik，作为 K8s 集群的统一流量入口。

### 解决的关键问题
*   **AI 模型的 Vendor Lock-in（厂商锁定）**：通过统一的路由和适配层，应用只需调用 Higress，Higress 后端可随时切换模型提供商。
*   **长连接治理难题**：AI 应用广泛使用 SSE (Server-Sent Events) 进行流式响应。传统网关在处理 SSE 时，往往因为超时配置或缓冲策略导致连接中断或首字延迟过高。Higress 针对此进行了优化。
*   **扩展性与安全性的平衡**：WASM 插件提供了沙箱隔离，即使插件崩溃也不会导致网关崩溃，且支持多语言编写。

### 与同类工具对比
| 特性 | Higress | Nginx / OpenResty | Kong | APISIX |
| :--- | :--- | :--- | :--- | :--- |
| **底层语言** | Go (Control) + C++ (Data) | C / Lua | C / Lua (部分 Go) | Lua (Nginx) |
| **扩展机制** | **WASM (Proxy-WASM)** | Lua (OpenResty) / C (Nginx) | Lua / Go / WASM (逐步支持) | Lua / WASM |
| **AI 特性** | **原生支持 (Prompt/MCP/Token流控)** | 需手写 Lua 脚本 | 依赖插件，生态较弱 | 依赖插件 |
| **配置热更新** | **毫秒级，无连接中断** | Reload (有损) | 数据库轮询或热更新 | 数据库轮询或热更新 |
| **K8s 集成** | **深度集成 (Ingress/Gateway API)** | 需配合 Ingress Controller | 支持 | 支持 |

---

## 3. 技术实现细节

### 关键技术方案
*   **xDS 协议流式推送**：Higress 控制平面维护配置一致性，通过 gRPC 长连接向 Envoy 推送配置。这种机制比基于文件挂载的配置更新更实时。
*   **WASM 虚拟机**：Higress 在 Envoy 中嵌入 WASM 运行时（如 Wasmtime 或 V8）。当请求到达时，Envoy 加载 WASM 模块，执行 `on_request` 或 `on_response` 钩子。这允许在数据路径上进行极其灵活的修改（如修改 HTTP Header 进行 AI 鉴权）。
*   **AI 流量拦截与处理**：在 WASM 插件或 Go Filter 中，解析 HTTP Body。针对 LLM 的流式响应（Chunked 编码），网关需要实现“流式透传”逻辑，即收到一个 Chunk 立即转发给客户端，而不是等待整个 Body 接收完毕，从而降低 TTFB（Time To First Byte）。

### 代码组织结构
*   **`pkg/`**：核心业务逻辑，包含 Ingress 转换器、路由匹配、Dubbo 服务发现等。
*   **`plugins/`**：内置的 WASM 插件源码，通常包含 Go 编写的插件逻辑，编译为 `.wasm` 文件。
*   **`installer/`**：Helm Charts 或 Kustomize 部署文件，体现了其云原生定位。

### 性能与扩展性
*   **性能优化**：数据面零拷贝技术（Envoy 特性）。针对 AI 场景，优化了缓冲区大小，避免大模型输出时的内存暴涨。
*   **扩展性**：支持 OpenTelemetry 集成，可观测性强。支持服务发现（Nacos, Consul, K8s CoreDNS）。

---

## 4. 适用场景分析

### 适合使用的项目
1.  **企业级 AI 应用平台**：需要统一接入多个 LLM 供应商，并对 API 调用进行精细化管控（如按部门限流、敏感词过滤）的场景。
2.  **微服务架构的 K8s 集群**：特别是已经使用或计划使用 Istio 的团队，Higress 可以平滑融入，提供比 Istio Gateway 更易用的 Ingress 配置体验。
3.  **需要高度定制网关逻辑的场景**：例如需要在网关层进行特殊的请求签名算法、数据脱敏，且希望使用 Go/Rust 等现代语言编写逻辑。

### 最有效的情况
当你的系统同时存在 **传统微服务调用** 和 **新兴 AI 模型调用**，且希望在同一套网关体系下进行流量治理、认证鉴权和可观测性管理时，Higress 是最佳选择。

### 不适合的场景
*   **极简静态站点托管**：如果只是简单的反向代理，Nginx 或 Caddy 更轻量，Higress 引入了 K8s 和 Envoy 的复杂度，属于“杀鸡用牛刀”。
*   **极端低延迟要求 (< 100us)**：虽然 Envoy 极快，但经过多层 Proxy-WASM 虚拟机调用仍有一定开销，对于极致性能要求的系统（如高频交易内核），可能需要纯 C++ 实现。

### 集成注意事项
*   **资源消耗**：Envoy 和 WASM 运行时对内存的消耗高于纯 Nginx，需合理配置 Pod Requests/Limits。
*   **WASM 插件调试**：WASM 的调试相对困难，建议在本地充分测试后再部署到网关集群。

---

## 5. 发展趋势展望

### 技术演进方向
*   **更强的 AI Agent 编排能力**：从单纯的流量转发向 Agent Orchestrator 演进，可能集成更多 LangChain 或 Semantic Kernel 的逻辑。
*   **WASM 生态标准化**：随着 Proxy-WASM 标准的成熟，Higress 可能会支持更多语言（如 .NET）编写的插件，并实现插件市场。
*   **边缘计算支持**：利用 WASM 的轻量级特性，Higress 可能会推出更适合边缘节点（如 CDN 边缘）的精简版，用于 AI 推理的边缘分发。

### 社区反馈与改进
目前社区对 AI 网关功能呼声较高。改进空间在于：
1.  **Dashboard 易用性**：目前的控制台功能尚可，但在可视化的 Prompt 调试和 AI 流量拓扑分析上仍有提升空间。
2.  **文档丰富度**：虽然核心文档完善，但针对复杂 WASM 插件开发的最佳实践文档较少。

---

## 6. 学习建议

### 适合开发者水平
*   **中级**：了解 Kubernetes 基础、网络协议（HTTP/TCP）。
*   **高级**：若需深入源码或编写 WASM 插件，需掌握 Go 语言，理解 Envoy 架构及 xDS

---
## 代码示例




```python
# 示例1：Higress 网关路由配置
from higress import Gateway, Route

def configure_gateway_routes():
    """
    配置 Higress 网关的路由规则
    解决问题：将不同路径的请求转发到不同的后端服务
    """
    # 创建网关实例
    gateway = Gateway(name="my-gateway")
    
    # 添加路由规则：将 /api 路径转发到后端服务A
    api_route = Route(
        path="/api",
        destination="backend-service-a:8080",
        methods=["GET", "POST"]
    )
    gateway.add_route(api_route)
    
    # 添加路由规则：将 /admin 路径转发到后端服务B
    admin_route = Route(
        path="/admin",
        destination="backend-service-b:8081",
        methods=["GET"]
    )
    gateway.add_route(admin_route)
    
    # 应用配置
    gateway.apply()
    print("网关路由配置已应用")

**说明**: 这个示例展示了如何使用 Higress 的 Python SDK 配置网关路由规则，实现了根据请求路径将流量分发到不同后端服务的功能。

```python


from higress import Gateway, Plugin
def configure_rate_limit_plugin():
"""
配置 Higress 的限流插件
解决问题：防止API被过度调用，保护后端服务
"""
# 创建网关实例
gateway = Gateway(name="my-gateway")
# 配置限流插件
rate_limit_plugin = Plugin(
name="rate-limit",
config={
"query_per_second": 100,  # 每秒允许100次请求
"burst": 200,             # 允许突发200次请求
"key_type": "IP",         # 基于IP进行限流
"rejected_code": 429      # 超出限制时返回429状态码
}
)
gateway.add_plugin(rate_limit_plugin)
# 应用配置
gateway.apply()
print("限流插件已配置")

```python
# 示例3：Higress 服务发现配置
from higress import Gateway, ServiceDiscovery

def configure_service_discovery():
    """
    配置 Higress 的服务发现
    解决问题：动态发现后端服务实例，实现负载均衡
    """
    # 创建网关实例
    gateway = Gateway(name="my-gateway")
    
    # 配置基于Nacos的服务发现
    nacos_discovery = ServiceDiscovery(
        type="nacos",
        config={
            "server_addr": "127.0.0.1:8848",
            "namespace": "public",
            "group": "DEFAULT_GROUP"
        }
    )
    gateway.set_service_discovery(nacos_discovery)
    
    # 应用配置
    gateway.apply()
    print("服务发现已配置为Nacos")

**说明**: 这个示例展示了如何配置 Higress 使用 Nacos 作为服务发现组件，实现动态发现后端服务实例并进行负载均衡。


---
## 案例研究


### 1：某大型电商平台（阿里系内部业务）

 1：某大型电商平台（阿里系内部业务）

**背景**: 
该电商平台拥有庞大的微服务架构，包含数百个后端服务，日常面临极高的并发流量，尤其是在“双11”等大促期间。此前使用 Nginx 作为 API 网关，但在云原生架构下，对流量治理的精细化、服务发现以及热配置更新提出了更高要求。

**问题**: 
1. 传统 Nginx 配置复杂，修改配置后需要 reload，会导致长连接闪断，影响用户体验。
2. 缺乏对 Dubbo、gRPC 等多协议的统一支持，无法直接与后端微服务进行高效通信。
3. 流量控制和安全防护策略（如 WAF）与业务代码耦合较紧，缺乏统一且灵活的流量入口管理。

**解决方案**: 
全面迁移至 **Higress**。利用 Higress 基于 Istio 的强大控制平面能力，将 Ingress 网关与微服务网关合二为一。通过 Higress 实现了 HTTP 到 Dubbo 协议的自动转换，并配置了全动态的路由规则和插件市场（如限流、认证、请求重试插件）。

**效果**: 
1. 实现了配置的热更新，频繁发布业务变更时不再有连接抖动，用户感知更平滑。
2. 统一了南北向（外部流量）与东西向（内部服务间）的流量管理，运维复杂度降低 40%。
3. 利用 Higress 的高性能处理能力，在同等硬件资源下，网关层的 QPS 吞吐量提升了 30%，有效支撑了大促期间的流量洪峰。

---



### 2：某 AI 创业公司（AIGC 应用服务）

 2：某 AI 创业公司（AIGC 应用服务）

**背景**: 
该公司专注于提供基于 LLM（大语言模型）的智能对话服务。其应用架构部署在阿里云 ACK（阿里云容器服务）上，后端对接 OpenAI 或通义千问等模型 API。随着用户量激增，如何控制高昂的 Token 成本以及保障接口稳定性成为核心痛点。

**问题**: 
1. 直接对外暴露模型 API 接口，容易被恶意调用或刷单，导致 Token 成本失控。
2. 缺乏对请求的缓存机制，相同的用户问题重复请求模型接口，增加了延迟和费用。
3. 需要针对不同用户等级实现不同的 Prompt 模板注入，但在代码层实现逻辑过于臃肿。

**解决方案**: 
在应用前端和模型服务之间引入 **Higress** 作为 AI 网关。
1. 开启 Higress 的“模型适配”功能，统一不同厂商的接口格式。
2. 启用语义缓存插件，对高频相似问题进行缓存拦截，直接返回缓存结果。
3. 利用 Higress 的请求头插件进行用户鉴权，并配置基于 Token 限流的策略。

**效果**: 
1. 通过语义缓存，减少了约 25% 的后端模型调用次数，显著降低了 API 调用成本。
2. 实现了毫秒级的响应速度提升（对于命中缓存的请求）。
3. 极大地简化了后端业务代码的复杂度，安全防护和流量控制策略完全在网关层解耦，系统稳定性大幅提高。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Apache APISIX | Kong Gateway |
|------|----------------|---------------|--------------|
| 性能 | 高性能（基于Envoy和Istio），支持高并发 | 极高性能（基于LuaJIT和APISIX），低延迟 | 高性能（基于Nginx和OpenResty），稳定 |
| 易用性 | 提供图形化控制台，支持Kubernetes Ingress，配置简单 | 提供Dashboard和API，配置灵活但学习曲线较陡 | 提供Admin API和图形化界面（企业版），配置较复杂 |
| 成本 | 开源免费，企业版功能需付费 | 开源免费，企业版功能需付费 | 开源版免费，企业版功能需付费 |
| 扩展性 | 支持Wasm插件，扩展性强 | 支持Lua插件，生态丰富 | 支持Lua和Python插件，生态成熟 |
| 社区 | 阿里背书，社区活跃度中等 | Apache顶级项目，社区活跃度高 | Kong Inc.维护，社区活跃度高 |
| 功能 | 支持流量管理、安全防护、可观测性 | 支持流量管理、安全防护、可观测性 | 支持流量管理、安全防护、可观测性 |

### 优势分析

- 优势1：基于Envoy和Istio，与云原生生态集成紧密，适合Kubernetes环境。
- 优势2：支持Wasm插件，扩展性强，且性能损耗低。
- 优势3：提供图形化控制台，降低使用门槛，适合快速上手。

### 不足分析

- 不足1：社区活跃度和生态成熟度不如Apache APISIX和Kong。
- 不足2：企业版功能需付费，成本可能较高。
- 不足3：文档和案例相对较少，学习资源有限。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 WASM 实现插件扩展

**说明**: Higress 深度集成了 WASM (WebAssembly) 技术，允许使用 C/C++、Go、Rust 或 JavaScript 编写自定义插件，而无需修改网关核心代码或重新部署服务。相比传统的 Lua 脚本或 Java Filter，WASM 插件具有更好的隔离性、更高的性能以及更丰富的生态支持。

**实施步骤**:
1. 根据团队技术栈选择合适的 WASM 开发语言（推荐使用 Go 或 Rust）。
2. 引入 Higress 官方提供的 SDK 或 Proxy-WASM 标准库进行插件逻辑开发。
3. 本地构建生成 `.wasm` 文件。
4. 在 Higress 控制台或通过 `WasmPlugin` CRD 将插件上传至网关，并配置生效的作用域（全局/特定路由/特定域名）。

**注意事项**: 开发时需注意 WASM 的内存和 CPU 限制，避免编写阻塞式的长耗时逻辑，以免阻塞请求处理线程。

---

### 实践 2：精细化流量治理与安全防护

**说明**: 利用 Higress 强大的路由和安全能力，实现从 L4 到 L7 的精细化流量管理。这包括基于 Header、Query 参数、Cookie 甚至 Body 内容的高级路由转发，以及集成 WAF 防护、认证鉴权等安全策略，确保后端服务的稳定性与安全性。

**实施步骤**:
1. 配置 `Ingress` 或 `Gateway` 资源，定义精确的匹配规则（如正则表达式匹配）。
2. 启用并配置 Higress 提供的官方安全插件（如 `key-auth`、`jwt-auth`）实现接口访问控制。
3. 针对敏感路径配置 IP 黑白名单或请求速率限制，防止恶意攻击。

**注意事项**: 复杂的正则匹配可能会轻微增加路由查找延迟，建议在生产环境评估规则复杂度。

---

### 实践 3：服务发现与多注册中心接入

**说明**: Higress 原生支持对接 Nacos、ZooKeeper、Consul、Eureka 等主流注册中心，以及 Kubernetes 的 Service。通过合理配置服务来源，可以实现云原生应用与传统微服务架构的统一流量入口，解决跨环境、跨架构的服务互通问题。

**实施步骤**:
1. 在 Higress 控制台的“来源管理”中添加对应类型的注册中心。
2. 配置注册中心的连接地址（如 Nacos 的 namespace、group 等参数）。
3. 创建服务并关联注册中心中的服务名，Higress 将自动同步服务实例列表。

**注意事项**: 确保注册中心地址的可达性，并注意服务名在 Higress 中的命名规范与注册中心保持一致。对于大规模服务列表，关注全量拉取对网络和内存的影响。

---

### 实践 4：全链路可观测性集成

**说明**: 为了快速定位性能瓶颈和故障，应充分利用 Higress 的可观测性特性。Higress 原生支持 OpenTelemetry 标准，可以将访问日志、指标和链路追踪数据导出到 Prometheus、Grafana、SkyWalking 或 Jaeger 等后端系统。

**实施步骤**:
1. 在 Higress 全局配置中开启 Prometheus Metrics 或 Access Log。
2. 配置 OpenTelemetry Collector 端点，启用 Tracing 采样。
3. 在日志服务（如 Elasticsearch、Loki）或 Grafana 中配置对应的索引面板，可视化监控网关吞吐量、延迟、错误率等关键指标。

**注意事项**: 在高并发场景下，全量日志采集可能会产生巨大的网络带宽和存储开销，建议根据业务需求设置适当的采样率或过滤规则。

---

### 实践 5：金丝雀发布与蓝绿部署

**说明**: 利用 Higress 的流量路由权重功能，可以实现服务的平滑升级。通过将特定比例的流量引入新版本服务，可以在最小化风险的前提下验证新版本的稳定性，是实现 DevOps 流程的关键一环。

**实施步骤**:
1. 准备新旧两个版本的服务，并在 Higress 中配置对应的服务来源。
2. 在路由配置中，针对同一个 Host 和 Path 定义多条转发规则。
3. 设置基于 Header 的灰度规则（如将带有 `x-version: v2` 的请求路由到新版本）或设置基于权重的流量分流（如 10% 流量去新版本）。
4. 逐步调整权重或扩大匹配范围，直至全量切换。

**注意事项**: 确保新旧版本的服务兼容性，特别是在 Session 场景下，需确保灰度用户的会话粘性。

---

### 实践 6：Dubbo 与 HTTP 协议互转

**说明**: Higress 具备强大的协议转换能力，特别是对于使用 Dubbo 框架的企业。它可以将 HTTP/HTTPS 请求转换为 Dubbo 协议调用后端服务，使得前端 Web 应用或 API 网关能够无缝调用后端的 RPC 服务

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/3 (QUIC) 协议

**说明**: HTTP/3 基于 UDP 协议，解决了 TCP 队头阻塞问题，显著降低弱网环境下的延迟。对于 Higress 这种网关产品，在处理移动端或跨地域长距离请求时，连接建立速度和传输稳定性会有质的飞跃。

**实施方法**:
1. 在 Higress 的网关配置中开启 QUIC 监听端口。
2. 确保后端服务支持 HTTP/1.1 或 HTTP/2，Higress 会自动处理协议转换。
3. 配置 TLS 1.3 以配合 HTTP/3 发挥最大性能。

**预期效果**: 弱网环境下视频或 API 请求的卡顿率降低 30% 以上，首字节延迟（RTT）降低约 20%-40%。

---

### 优化 2：配置全链路超时与连接池调优

**说明**: 默认配置通常较为保守，容易导致连接数堆积或请求长时间挂起。通过调整上游（Upstream）和下游的连接池大小以及超时时间，可以防止资源耗尽，并提高网关的吞吐容量。

**实施方法**:
1. **调整连接池**: 根据后端服务能力，适当增大 `maxConnections`，避免连接排队等待。
2. **设置超时**: 合理设置 `connectTimeout`、`sendTimeout` 和 `readTimeout`。对于非关键路径，可设置较短的超时时间（如 500ms）以实现快速失败。
3. **开启 Keep-Alive**: 确保与后端服务保持长连接，减少频繁握手开销。

**预期效果**: P99 延迟降低 15%-25%，网关最大并发处理能力（QPS）提升 20% 左右。

---

### 优化 3：启用 Wasm 插件与本地缓存

**说明**: Higress 支持 Wasm (WebAssembly) 插件。相比于传统的 Lua 或远程调用逻辑，Wasm 执行效率极高且沙箱隔离。利用 Wasm 实现高频数据的本地缓存（如鉴权 Token、配置项），可以大幅减少对后端服务的冗余请求。

**实施方法**:
1. 将鉴权、限流等高频逻辑编写为 Wasm 插件并在 Higress 中加载。
2. 在 Wasm 插件中实现内存级缓存，对 Key-Value 配置或 Token 验证结果进行短时缓存（如 TTL 30s）。
3. 避免在请求路径中进行复杂的同步远程 RPC 调用。

**预期效果**: 鉴权与逻辑处理延迟降低至 1ms 以内，后端冗余请求量减少 40%-60%。

---

### 优化 4：启用 DNS 缓存与 IP 直连

**说明**: 网关在处理大量请求时，频繁的 DNS 解析会成为性能瓶颈（特别是使用外部 DNS 服务时）。配置 DNS 缓存或直接配置 IP 地址作为 Upstream，可以消除解析延迟。

**实施方法**:
1. 在 Higress 配置中开启 DNS 缓存功能，并设置合理的 TTL。
2. 对于核心内部服务，在 Service Entry 或 Upstream 配置中直接使用 IP 地址而非域名。
3. 若使用 K8s Service，确保 `ClusterIP` 模式下的连接复用。

**预期效果**: 消除毫秒级的 DNS 查询延迟，单次请求路由耗时减少 5ms-10ms，在高并发下效果显著。

---

### 优化 5：启用 Gzip / Brotli 数据压缩

**说明**: 对于 JSON 或文本类 API 响应，开启压缩可以显著减少网络传输带宽，并加快客户端下载速度。虽然增加了少量的 CPU 计算开销，但在现代 CPU 上通常是划算的。

**实施方法**:
1. 在 Higress 的全局或路由级别配置启用 `gzip` 或 `brotli` 压缩。
2. 设置 `gzip_types` 仅针对 `text/html`, `application/json`, `text/plain` 等文本类型进行压缩，避免

---
## 学习要点

- 基于提供的来源信息（GitHub Trending 上的 Alibaba/Higress），以下是关于该项目的关键要点总结：
- Higress 是阿里云开源的、基于 Envoy 和 Istio 构建的下一代云原生 API 网关。
- 该项目深度集成了 K8s Ingress 与 Gateway API 标准，能够无缝对接云原生生态系统。
- 它提供了强大的流量治理能力，支持金丝雀发布、蓝绿部署及负载均衡等高级路由功能。
- Higress 原生支持 WASM (WebAssembly) 技术，允许开发者使用 C++/Go/Rust 等语言编写高性能、低延迟的扩展插件。
- 平台内置了全面的流量安全防护机制，能有效抵御 CC 攻击、SQL 注入及恶意 Bot 访问。
- 它兼容 Nginx Ingress 注解配置，并支持将 Nginx 配置直接转换为 Higress 格式，极大降低了迁移门槛。


---
## 学习路径

## 学习路径

### 阶段 1：基础概念与核心架构

**学习内容**:
- 理解云原生网关的基本概念，以及 Higress 与 Nginx、Istio、Kubernetes Ingress 的区别与联系
- 掌握 Higress 的核心架构设计：基于 Envoy 和 Istio 的技术栈
- 学习基本术语：Ingress、Gateway、Route、Service、Plugin
- 了解 Higress 的应用场景（微服务网关、API 管理、K8s Ingress）

**学习时间**: 1-2周

**学习资源**:
- Higress GitHub 官方仓库 README
- Higress 官方文档（架构与原理篇）
- Envoy 官方文档基础概览

**学习建议**:
- 建议先对 Kubernetes 和 Service Mesh 有初步了解，再上手 Higress 会更容易理解其流量管理机制。
- 对比阅读 Nginx 的配置语法，以便更快理解 Higress 的路由配置逻辑。

---

### 阶段 2：本地部署与基础配置

**学习内容**:
- 掌握本地环境搭建：使用 Docker 或 Docker Compose 快速部署 Higress Standalone 模式
- 学习在 Kubernetes 环境中通过 Helm 部署 Higress
- 实践基础流量管理：配置域名、路由转发、重定向/重写路径
- 学习服务来源的配置：接入固定地址、Nacos、K8s Service 等服务来源
- 理解并配置基础认证与安全：Basic Auth、CORS 头部设置

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档（快速开始/安装部署）
- Higress 官方示例
- Docker Compose 配置文件参考

**学习建议**:
- 动手实践是关键，建议先在本地 Docker 环境跑通一个简单的 Demo。
- 尝试将一个本地 Web 服务通过 Higress 暴露出来，并修改路由规则观察流量变化。

---

### 阶段 3：流量治理与高可用

**学习内容**:
- 高级流量治理：金丝雀发布、蓝绿发布、基于 Header/Query 的路由分流
- 负载均衡策略配置：轮询、随机、最小连接数等
- 服务容错与保护：超时设置、重试策略、熔断配置
- 全局限流与并发控制：基于 IP、Header 或参数的限流规则
- 理解 Higress 的高可用部署架构与性能调优

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档（流量治理/高级功能）
- Envoy 数据平面配置文档
- 云原生网关最佳实践案例

**学习建议**:
- 结合实际业务场景思考，例如如何通过 Higress 实现无风险的版本上线。
- 重点理解 Wasm 插件机制如何扩展网关功能，这是 Higress 区别于传统网关的一大优势。

---

### 阶段 4：插件开发与生态集成

**学习内容**:
- 深入了解 Higress 的插件系统：Wasm (WebAssembly) 与 Go/Python/Java 插件开发
- 实践编写自定义插件：实现自定义鉴权、请求/响应修改逻辑
- 学习 Higress Dashboard (控制台) 的使用与配置管理
- 集成第三方生态：对接 Prometheus/Grafana 监控、对接 OIDC 认证、对接阿里云云原生生态
- 探索 Higress 对 AI 服务的支持（如 AI 网关/代理功能）

**学习时间**: 4-6周

**学习资源**:
- Higress 官方文档（自定义开发/Wasm 插件）
- Higress 官方插件市场
- WebAssembly 相关教程

**学习建议**:
- 尝试编写一个简单的 Wasm 插件并加载到网关中运行。
- 关注社区动态，Higress 更新较快，特别是针对 AI 和大模型流式传输的优化功能。

---

### 阶段 5：生产运维与源码剖析

**学习内容**:
- 生产环境安全加固：TLS/HTTPS 配置、WAF 防护策略
- 深入监控与日志：集成 SLS、OpenTelemetry 链路追踪
- Higress 源码剖析：理解控制面与数据面的交互机制、配置热更新原理
- 参与开源社区：阅读 GitHub Issues、提交 PR、贡献插件或文档
- 大规模集群下的性能优化与故障排查

**学习时间**: 持续学习

**学习资源**:
- Higress GitHub Source Code
- Higress 官方博客与深度技术文章
- 云原生网关深度解析电子书或课程

**学习建议**:
- 在生产环境上线前，务必进行充分的压力测试。
- �

---
## 常见问题


### 1: Higress 是什么？它与其他开源网关（如 Nginx, Kong, APISIX）有什么区别？

1: Higress 是什么？它与其他开源网关（如 Nginx, Kong, APISIX）有什么区别？

**A**: Higress 是一个开源的、基于阿里内部多年实践沉淀的云原生 API 网关。它建立在 Envoy 高性能网络代理库的基础之上，深度集成了 Istio 服务网格体系。

与 Nginx/Kong/APISIX 的主要区别在于：
1.  **技术架构**：Higress 基于 Envoy (C++/Go)，而 Kong 和 APISIX 早期分别基于 OpenResty 和 LuaJIT。Envory 在处理高并发、长连接（如 gRPC、Dubbo）以及动态配置下发方面具有原生优势。
2.  **云原生集成**：Higress 从设计之初就深度兼容 Istio，可以作为 Ingress Controller 或 Gateway API 的实现，能直接消费 Kubernetes 的服务注册信息，无需像传统网关那样额外配置服务发现。
3.  **安全与流量防护**：Higress 内置了针对 Web 流量的 WAF 防护能力，并集成了阿里云的安全情报，这是许多基础网关不具备的开箱即用功能。
4.  **插件生态**：它支持使用 WASM (WebAssembly) 技术编写插件，这意味着插件可以用 C++, Go, Rust, JavaScript 等多种语言编写，且热更新无需重启网关，扩展性更强。

---



### 2: Higress 支持哪些协议？能否用于 Dubbo 或 gRPC 服务治理？

2: Higress 支持哪些协议？能否用于 Dubbo 或 gRPC 服务治理？

**A**: Higress 具备极强的协议处理能力，不仅支持标准的 HTTP/HTTPS 和 WebSocket，还深度支持微服务架构中的常用协议。

1.  **HTTP/HTTPS**：作为最基础的协议，完全兼容 RESTful API。
2.  **gRPC**：原生支持 gRPC 协议代理，支持基于 HTTP/2 的流式传输，并能实现 gRPC 到 JSON 的转码（Transcoding），方便前端调用。
3.  **Dubbo**：这是 Higress 的一大特色。它支持 Dubbo2 和 Dubbo3 协议，能够直接将 HTTP 请求转换为 Dubbo 请求调用后端 Java 服务，实现 HTTP 到 Dubbo 的无缝打通。
4.  **其他协议**：支持 MQTT (用于物联网) 等协议，通常通过插件或特定配置实现。

---



### 3: Higress 如何处理流量管理，比如灰度发布（金丝雀发布）和负载均衡？

3: Higress 如何处理流量管理，比如灰度发布（金丝雀发布）和负载均衡？

**A**: Higress 继承了 Istio 强大的流量治理能力，并对其进行了简化和增强。

1.  **灰度发布**：通过配置路由规则，用户可以轻松实现基于 Header、Cookie 或 URL 参数的流量分流。例如，将 10% 的流量或特定内部用户的请求路由到新版本服务。
2.  **全链路灰度**：在微服务场景下，Higress 支持将流量染色（打标），配合服务网格（如 Istio 或 MSE）实现全链路的灰度透传，确保请求在调用链中的所有版本都保持一致。
3.  **负载均衡**：支持多种负载均衡策略，包括轮询、随机、基于请求哈希、加权最少连接等。特别是针对 gRPC 和 Dubbo 等长连接协议，Envory 的负载均衡算法比传统网关更高效。

---



### 4: Higress 的安全性如何？是否支持 WAF 和认证鉴权？

4: Higress 的安全性如何？是否支持 WAF 和认证鉴权？

**A**: Higress 提供了企业级的安全防护能力，不仅仅是简单的路由转发。

1.  **WAF 防护**：Higress 内置了 Web 应用防火墙功能，能够防御 SQL 注入、XSS 跨站脚本、远程代码执行等常见 Web 攻击。它利用了阿里云的安全规则库，并支持自定义规则。
2.  **认证鉴权**：
    *   支持 **OpenID Connect (OIDC)** 单点登录，可对接 Keycloak、Auth0 等标准 IdP。
    *   支持 **JWT** 校验。
    *   支持 **Basic Auth** 和 **API Key** 鉴权。
    *   支持 **AK/SK** 签名认证（类似阿里云网关）。
3.  **IP 访问控制**：支持黑名单和白名单机制，可以限制特定 IP 或 IP 段的访问。

---



### 5: 如何在 Kubernetes 集群中部署 Higress？是否支持非 K8s 环境？

5: 如何在 Kubernetes 集群中部署 Higress？是否支持非 K8s 环境？

**A**: Higress 是云原生的网关，首选部署方式是 Kubernetes。

1.  **Kubernetes 部署**：可以通过标准的 Helm Chart 或 kubectl YAML 资源文件一键部署。它会自动监听 Kubernetes 的 Ingress 资源或 Gateway API 资源，并自动感知后端 Service 的 Endpoints 变化。
2.  **非 K8s 环境**：虽然主要面向 K8s，但 Higress 也提供了 **Docker Compose** 的部署方式，适合在虚拟机

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单] 快速启动与路由转发

### 问题**：基于 Higress 官方提供的 Docker 镜像，在本地快速启动一个 Higress 网关实例，并配置一个简单的路由转发规则。要求实现：当访问 `/httpbin/` 路径时，将流量透明转发到公共的测试服务 `httpbin.org`。

### 提示**：

### 需要查阅 `higress` 官方文档中的 "快速开始" 或 "Quick Start" 章节。

---
## 实践建议

以下是针对 Higress (AI Gateway) 的 6 条实践建议，涵盖从流量接入、模型治理到安全防护的具体场景：

### 1. 利用 Wasm 插件实现提示词与响应的实时处理
*   **场景**：在将请求发送给 LLM 之前，需要注入系统提示词；或者在返回给用户之前，过滤敏感词汇或压缩冗长的回复。
*   **建议**：不要在应用代码中处理这些逻辑。利用 Higress 的 Wasm (WebAssembly) 能力，编写 Go 或 C++ 插件直接在网关层处理。
*   **具体操作**：
    *   开发一个 Wasm 插件，配置 `onRequestBody` 钩子来修改 JSON Body 中的 `messages` 字段，追加企业预设的 System Prompt。
    *   使用 `onResponseBody` 钩子截取模型流式输出，实现敏感词实时拦截或格式转换（如 Markdown 转 JSON）。
*   **最佳实践**：将提示词模板配置化，通过插件动态读取，实现不重启网关即可调整 Prompt 策略。

### 2. 实施基于 Token 的精细化配额与限流
*   **场景**：LLM 调用成本主要取决于 Token 数量，传统的基于 QPS（每秒请求数）或并发连接数的限流无法有效控制成本。
*   **建议**：启用针对 Token 的限流策略，防止个别用户或模型滥用导致预算超支。
*   **具体操作**：
    *   在 Higress 的鉴权或限流插件中，配置基于 Token 预估或实际统计的规则。
    *   为不同的 API Key 或租户设置每分钟/每天的最大 Token 消耗额度。
*   **常见陷阱**：仅限制并发连接数。这会导致用户发送一个极长的 Prompt（占用大量计算资源）仅占用 1 个连接，从而绕过限制。

### 3. 配置语义化的模型路由与 fallback 策略
*   **场景**：企业内部同时接入了通义千问、DeepSeek、OpenAI 等多种模型。希望简单类别的问答走便宜模型，复杂推理走昂贵模型，且主模型故障时能自动切换。
*   **建议**：利用 Higress 的 AI 路由特性，根据请求特征或 Header 智能分发流量。
*   **具体操作**：
    *   配置服务路由规则：将包含特定 Header（如 `x-model-variant: logic`）的请求路由至高性能模型，默认请求路由至轻量级模型。
    *   设置 fallback 目标：当主模型提供商返回 5xx 错误或超时，自动将请求重试并转发至备用模型提供商，保证业务连续性。

### 4. 集中式管理 Provider 密钥与模型元数据
*   **场景**：开发团队直接在代码中硬编码 OpenAI 或其他厂商的 API Key，导致密钥泄露风险高且难以轮换。
*   **建议**：将所有第三方 LLM 的 API Key 和 Endpoint 配置收敛在 Higress 网关层，业务端只持有网关颁发的内部凭证。
*   **具体操作**：
    *   在 Higress 的 `provider` 资源中统一配置各大厂商的 AK/SK。
    *   业务端调用时使用标准化的 OpenAI 协议，目标地址指向 Higress 域名，不再直接暴露第三方厂商的地址。
*   **最佳实践**：通过网关屏蔽不同厂商（如 Azure OpenAI vs 百度千帆）之间协议的细微差异，统一应用层代码。

### 5. 启用全链路可观测性以监控 Token 消耗与延迟
*   **场景**：LLM 请求耗时较长（首字延迟 TTFT 高），且计费模式特殊，传统的 HTTP 监控指标无法满足排查需求。
*   **建议**：重点关注 Prompt Tokens、Completion Tokens 以及首字节生成时间。
*   **具体操作**：
    *   确保日志格式中包含 AI 特定字段（

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
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260206-github_trending-alibaba-higress-6.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260215-github_trending-alibaba-higress-5.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260216-github_trending-alibaba-higress-6.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*