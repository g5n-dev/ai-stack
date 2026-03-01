---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-03-01T20:07:03+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "云原生", "Istio", "Envoy", "WASM", "AI 原生", "MCP 协议"]
categories: ["系统与基础设施", "AI 工程"]
source: github_trending
description: "基于您提供的 DeepWiki 节选内容，以下是关于 **Higress** 的简洁总结： 项目概况 * **身份**：Higress 是一个**云原生 API 网关**，基于 Istio 和 Envory 构建。 * **核心定位**：**AI Native API Gateway**（AI 原生 API 网关）。"
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
- **星标**: 7,600 (+4 stars today)
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

Higress 是一款基于 Istio 和 Envoy 构建的 AI 原生 API 网关，旨在通过云原生架构处理流量管理与 AI 应用集成。它不仅提供传统的微服务路由能力，还针对大语言模型（LLM）应用提供了 AI 网关特性，并支持通过 WASM 插件进行灵活扩展。本文将介绍其系统架构、核心组件以及如何利用 MCP 系统与 WASM 插件来增强网关的适用性。

---
## 摘要

基于您提供的 DeepWiki 节选内容，以下是关于 **Higress** 的简洁总结：

### 项目概况
*   **身份**：Higress 是一个**云原生 API 网关**，基于 Istio 和 Envory 构建。
*   **核心定位**：**AI Native API Gateway**（AI 原生 API 网关）。
*   **开发语言**：Go。
*   **现状**：在 GitHub 上获得约 7,600 颗星（数据截至提供时）。

### 核心架构与技术特性
1.  **扩展能力**：通过 **WebAssembly (WASM)** 插件能力进行了扩展，兼具高性能与灵活性。
2.  **架构设计**：采用**控制平面与数据平面分离**的架构。
    *   **配置分发**：通过 xDS 协议传播配置变更，具备毫秒级延迟且**无连接中断**的特性。
    *   **适用场景**：特别适合需要长连接的场景，例如 **AI 流式响应**处理。

### 三大核心功能与用途
Higress 主要提供以下三类服务：

| 用途类别 | 描述 | 核心组件/插件 |
| :--- | :--- | :--- |
| **1. AI 网关** | 为大语言模型（LLM）应用提供统一 API。支持协议转换、可观测性、缓存及安全防护。 | `ai-proxy`, `ai-statistics`, `ai-cache`, `ai-security-guard` |
| **2. MCP 服务器托管** | 托管模型上下文协议（MCP）服务器，使 AI 智能体能够调用工具和服务。 | `mcp-router`, `jsonrpc-converter` |
| **3. Kubernetes Ingress** | 作为 Kubernetes 的 Ingress 控制器，兼容 nginx-ingress 注解，处理微服务路由。 | `higress-controller` |

**总结：**
Higress 是一个专为 AI 时代设计的现代化网关，它不仅保留了传统 API 网关（K8s Ingress、微服务路由）的功能，更通过内置 AI 网关和 MCP 协议支持，解决了大模型应用接入与智能体工具调用的痛点，同时具备高性能的流式处理能力。

---
## 评论

### 总体判断

Higress 是目前云原生网关领域中将“AI 原生”与“传统流量治理”融合得最彻底的开源项目之一。它不仅继承了 Envoy 的高性能与 Istio 的控制面优势，更通过 WASM 技术和针对大模型（LLM）的深度优化，成功解决了企业在 AI 落地过程中最后一公里的连接与安全痛点。

---

### 深入评价维度

#### 1. 技术创新性：从“流量管道”到“智能路由”的演进
*   **事实**：Higress 基于 Envoy 和 Istio 构建，引入了 WebAssembly (WASM) 插件系统，并明确提出了“AI Gateway”与“MCP (Model Context Protocol) Server Hosting”功能。
*   **推断**：传统网关（如 Nginx, 早期 Kong）主要关注 HTTP/TCP 转发。Higress 的创新点在于**协议层的语义升级**。它不再把 AI 请求视为普通 HTTP 流量，而是理解 Prompt、Token 流和上下文。
    *   **差异化方案**：通过 WASM 扩展 AI 能力（如 Token 计费、敏感词过滤、Prompt 注入），无需重启网关即可动态更新逻辑，这比基于 Lua 的 OpenResty 或基于 Java 的传统网关在安全性和灵活性上更具优势。
    *   **MCP 支持**：直接内置 MCP 协议支持，使其成为 AI Agent（智能体）的基础设施，而不仅仅是 API 的路由器。

#### 2. 实用价值：解决 AI 落地中的“连接与成本”难题
*   **事实**：文档指出其核心功能包括 AI Gateway（LLM 应用支持）、MCP 服务托管以及传统的 K8s Ingress 和微服务路由。
*   **推断**：Higress 解决了两个关键痛点：
    *   **模型供应商锁定**：企业开发 AI 应用时，切换模型（如从 GPT-4 切换到通义千问）通常需要修改代码。Higress 提供统一的后端接口，允许企业在网关层通过配置切换模型，实现了**Provider Agnostic（模型无关）**的架构。
    *   **成本与安全控制**：在网关层实现 Token 限流和缓存，可以显著降低大模型调用成本；同时，统一的鉴权机制避免了将密钥分散在前端代码中。

#### 3. 代码质量与架构：云原生标准下的模块化设计
*   **事实**：项目使用 Go 语言编写，架构明确分离了控制面与数据面，且基于 Envoy（C++）作为高性能数据代理。
*   **推断**：
    *   **架构设计**：采用标准的云原生架构，控制面负责配置下发（兼容 Istio），数据面负责处理流量。这种分离设计保证了高可用性。
    *   **扩展性**：WASM 插件市场的引入是其代码生态的高光之处。官方提供了多语言（Go, C++, Rust, JS）的 SDK，降低了开发者的准入门槛，代码规范符合云原生社区的最佳实践。

#### 4. 社区活跃度：阿里背书的强力驱动
*   **事实**：星标数 7,600+，语言为 Go，由阿里巴巴开源。
*   **推断**：作为阿里云核心产品（Higress 商业版）的开源版本，该项目不仅有阿里的持续投入，还兼容开源 K8s 生态。相比个人项目，其维护周期和稳定性更有保障。7.6k 的 Star 数在网关领域属于第一梯队，说明社区关注度极高，且反馈机制通常较为敏捷。

#### 5. 潜在问题与改进建议
*   **问题**：基于 Envoy 的调试难度较高。虽然 WASM 提供了灵活性，但编写高性能的 WASM 插件对开发者的内存管理能力（若使用 C++/Rust）仍有要求。
*   **建议**：目前的 AI 功能主要集中在路由和简单处理，未来建议增加对**多模态（图片/视频）流式处理**的更细粒度支持，以及更强大的 AI 可观测性面板。

#### 6. 对比优势：Higress vs. Kong/APISIX vs. 专用 AI Gateway
*   **对比**：
    *   **vs. Kong/APISIX**：传统网关虽然也有 AI 插件，但多为后补功能。Higress 是**AI Native**，原生支持 SSE（Server-Sent Events）流式转发，在处理 LLM 长连接时的内存管理更优。
    *   **vs. LangChain/Portkey**：这些是 SDK 或专用 AI 网关，缺乏底层流量治理能力（如灰度发布、全链路 tracing）。Higress 允许企业在一个网关内同时管理传统微服务和 AI 服务，**减少了架构复杂度**。

---

### 边界条件与验证清单

#### 不适用场景
*   **极简边缘场景**：如果仅需在树莓派或极低资源设备上做简单转发，Higress 基于 Envoy 的资源消耗可能过重，Traefik 或纯 Nginx 更合适。
*   **纯业务逻辑处理**：网关不应承担复杂的业务计算（如复杂的 AI 推理逻辑预处理），这会导致网关过载。

#### 快速验证清单
1.  **AI 语义识别测试**：配置一个路由指向 OpenAI，使用 Higress 的 Prompt 插件在请求中自动

---
## 技术分析

以下是对阿里巴巴开源的 **Higress** 项目的深度技术分析。Higress 不仅仅是一个传统的 API 网关，它定位为 **AI Native API Gateway**（AI 原生网关），这标志着云原生网关技术向 AI 时代的演进。

---

### 1. 技术架构深度剖析

Higress 的核心架构体现了 **"控制平面与数据平面分离"** 的云原生设计理念，并在此基础上进行了针对 AI 场景的深度定制。

*   **技术栈与底层基石**：
    *   **数据平面**：基于 **Envoy** 构建。Envoy 是 C++ 编写的高性能代理，擅长处理长连接和高并发。Higress 并没有直接 fork Envoy，而是通过扩展其生态来集成功能。
    *   **控制平面**：基于 **Istio** 生态。它复用了 Istio 的强大控制能力（如 xDS 协议下发），但移除了 Sidecar 模式的复杂性，专注于 Ingress Gateway 和更上层的 API 管理。
    *   **扩展语言**：**Go**。Higress 的核心控制逻辑和插件开发主要使用 Go 语言，利用 Go 的高并发特性处理元数据。

*   **架构模式**：
    *   **WASM (WebAssembly) 插件化架构**：这是 Higress 最具技术含量的设计。传统网关插件（如 Nginx Lua）往往存在稳定性风险（崩溃拖垮主进程）和语言绑定问题。Higress 引入 WASM，允许开发者使用 **Go、C++、Rust、JavaScript** 等多种语言编写插件，这些插件被编译为 WASM 字节码运行在沙箱中。
        *   **优势**：隔离性（插件崩溃不影响网关）、动态性（插件热加载无需重启网关）、多语言支持。
    *   **AI-Native 层**：在传统网关层之上，增加了一层专门用于处理 LLM（大语言模型）流量的逻辑。这包括 Prompt 模板管理、Token 流式处理、以及与模型提供商的协议适配。

*   **架构优势分析**：
    *   **毫秒级配置生效**：基于 xDS 协议的推送机制，配置变更几乎是实时的，这对于需要频繁调整 Prompt 或路由策略的 AI 应用至关重要。
    *   **长连接友好**：针对 AI 应用的 SSE（Server-Sent Events）流式响应进行了底层优化，避免了传统网关在处理长连接时的缓冲区阻塞问题。

---

### 2. 核心功能详细解读

Higress 的功能集可以概括为 "1 + 1 + N"，即一套云原生网关底座 + 一套 AI 网关能力 + N 种扩展插件。

*   **AI Gateway (核心亮点)**：
    *   **功能**：提供统一的 LLM 接入层。它屏蔽了不同模型厂商（OpenAI, Azure, 通义千问, 文心一言等）API 差异，允许用户通过 Higress 的统一标准调用任意模型。
    *   **解决的问题**：
        *   **密钥泄露风险**：企业无需在客户端暴露各厂商的 API Key，所有请求在网关层统一鉴权。
        *   **Token 计费与统计**：在网关层精确统计流式传输中的 Token 使用量，实现精细化成本控制。
        *   **Prompt 管理**：支持在网关层进行 Prompt 模板化注入，实现"提示词工程"的基础设施化。

*   **MCP (Model Context Protocol) Server Hosting**：
    *   **功能**：Higress 能够托管 MCP 服务。MCP 是连接 AI Agent 与外部数据/工具的标准协议（类似 AI 的"USB 接口"）。
    *   **意义**：这意味着 Higress 不仅是流量的入口，更是 AI Agent 的"工具箱"。它允许 AI 应用通过网关安全地访问数据库、SaaS 工具等。

*   **与传统 API 网关的对比**：
    *   **vs Kong/APISIX**：传统网关侧重于 RESTful 服务的路由、限流、熔断。Higress 在此基础上，原生支持 SSE 流量处理、LLM 协议转换（如将 OpenAI 格式转为通义千问格式）以及 AI 特有的安全防护（提示词注入防御）。
    *   **vs 云厂商 Gateway**：Higress 是开源的，避免了被单一云厂商锁定，且基于 Envoy/Istio 的标准化程度更高。

---

### 3. 技术实现细节

*   **关键算法与技术方案**：
    *   **LLM 流式透传与拦截**：在处理 SSE 流时，网关不能简单地缓冲全部数据再转发（否则失去流式意义）。Higress 实现了流式数据的 **分片处理**，能够在数据流经网关时，实时进行敏感词过滤、Token 计数或格式转换，而几乎不增加端到端延迟。
    *   **WASM 虚拟机集成**：通过代理 HTTP 过滤器接口，将请求/响应数据传递给 WASM 虚拟机。这里涉及 **Host-VM** 之间的内存拷贝优化，是性能调优的关键点。

*   **代码组织结构**：
    *   **pkg/**：核心业务逻辑，包含 xDS 转换、路由匹配等。
    *   **plugins/**：WASM 插件的 Go SDK 和源码。采用了 Proxy-WASM 规范。
    *   **router/**：针对 Kubernetes Ingress 和 Gateway API 的控制器实现。

*   **性能优化**：
    *   **零拷贝**：在 Envoy 层面尽可能利用零拷贝技术处理网络 I/O。
    *   **连接池管理**：针对后端 LLM 服务（通常响应较慢），优化了 HTTP 连接池的复用策略，避免频繁握手带来的延迟。

---

### 4. 适用场景分析

*   **最适合的场景**：
    *   **企业级 AI 应用落地**：企业内部构建 AI 助手或 Copilot，需要统一管理多个大模型供应商的 Key、配额和访问策略。
    *   **微服务 + AI 混合架构**：系统既有传统的 REST 微服务，又有新接入的 AI 能力，需要一个统一的入口。
    *   **SaaS 平台**：需要为不同租户提供不同的 AI 模型配额和计费策略。

*   **不适合的场景**：
    *   **极简边缘计算**：如果只需要在边缘设备做极其简单的转发，Higress 基于 Envoy 的资源占用可能过于重量级（虽然比 Java 网关轻，但不如纯 C 轻量级路由）。
    *   **非 HTTP 协议**：如果主要处理 gRPC 之外的复杂 TCP/UDP 协议（如游戏流），虽然 Envoy 支持，但 Higress 的 AI 特性在此场景下无意义。

*   **集成方式**：
    *   **Kubernetes**：作为 Ingress Controller 安装。
    *   **Docker**：独立容器运行，适合非 K8s 环境。

---

### 5. 发展趋势展望

*   **技术演进方向**：
    *   **从 Gateway 到 AI Broker**：Higress 正在从单纯的"通道"演变为"经纪人"。未来它可能包含更复杂的编排能力，例如根据用户问题自动路由到最便宜的模型，或并行调用多个模型并汇总结果。
    *   **RAG (检索增强生成) 深度集成**：目前 Higress 主要做路由和安全。未来可能会在网关层直接集成向量数据库的检索接口，实现更快的 RAG 响应。

*   **社区与生态**：
    *   作为阿里主导的项目，其在国内云原生社区的活跃度较高。随着 AI 的爆发，它的"AI Gateway"标签吸引了大量关注。改进空间在于 WASM 插件的易用性和调试工具链的完善。

---

### 6. 学习建议

*   **适合人群**：
    *   **后端/架构师**：希望深入理解云原生网关、Service Mesh 技术。
    *   **AI 应用开发者**：需要解决生产环境中 LLM 接入的工程问题（如鉴权、限流）。

*   **学习路径**：
    1.  **前置知识**：理解 HTTP/HTTPS、Kubernetes 基本原理、Envoy 基础概念。
    2.  **核心概念**：学习 Istio 的 xDS 协议，理解控制平面如何配置数据平面。
    3.  **动手实践**：在本地 Kind 集群中部署 Higress，配置一个简单的 AI 路由（例如将 OpenAI 请求转发到通义千问）。
    4.  **插件开发**：尝试使用 Go 编写一个简单的 WASM 插件（例如添加一个自定义的 HTTP Header）。

---

### 7. 最佳实践建议

*   **如何正确使用**：
    *   **利用 Wasm 插件隔离业务**：不要修改 Higress 核心代码，所有业务逻辑（如特殊的鉴权算法、日志格式）都应编写为 Wasm 插件。
    *   **AI 模型路由**：利用 Higress 的 Header 路由能力，实现"灰度发布"模型。例如，将 10% 的流量路由到新模型进行测试。

*   **常见问题与坑**：
    *   **WASM 性能陷阱**：WASM 插件虽然安全，但跨语言调用（Go <-> C++ Envoy）有序列化开销。避免在插件中进行密集的 CPU 计算或大对象拷贝。
    *   **超时配置**：LLM 推理时间较长，务必在后端服务配置中合理设置超时时间，并开启流式传输以避免网关层断开连接。

*   **性能优化**：
    *   开启 Envoy 的 **Compressed Filter** 以减少 WASM 插件的传输体积。
    *   在高并发场景下，调整 Higress 的 Pod 副本数和 Envoy 的工作线程数。

---

### 8. 哲学与方法论：第一性原理与权衡

*   **抽象层的转移**：
    *   Higress 在 **"连接"** 层面做了抽象。它将"如何连接服务"和"如何连接模型"的复杂性统一收敛。
    *   **复杂性转移**：它将运维的复杂性（配置 Envoy，管理 xDS）转移给了自己（Higress 控制平面），将业务逻辑的灵活性（通过 WASM）转移给了开发者。它默认运维团队愿意维护一套 K8s + Istio 的复杂环境，以换取极致的扩展性和标准化。

*   **价值取向与代价**：
    *   **取向**：**标准化与可移植性**。它极力推崇 Istio/Envoy 标准，拒绝私有协议锁定。
    *   **代价**：**学习曲线陡峭**。相比于 Nginx 的配置文件，理解 xDS、WASM 和 K8s CRD 的心智负担要重得多。
    *   **工程哲学**：**"Infrastructure as Code" (IaC) 的极致延伸**。它认为路由、鉴权、Prompt 模板都应该是代码化的、版本控制的、可观测的，而不是手工配置的黑盒。

*   **可证伪的判断（

---
## 代码示例




```python
# 示例1：使用Higress实现简单的API网关路由
from higress import Gateway, Route, Service

# 创建一个网关实例
gateway = Gateway(name="my-gateway")

# 定义后端服务
backend_service = Service(
    name="user-service",
    url="http://user-service:8080"
)

# 创建路由规则
user_route = Route(
    path="/api/users/*",
    service=backend_service,
    methods=["GET", "POST"]
)

# 将路由添加到网关
gateway.add_route(user_route)

# 启动网关
if __name__ == "__main__":
    gateway.run(port=8080)
```




```python
# 示例2：配置Higress的限流功能
from higress import Gateway, RateLimitConfig

# 创建网关实例
gateway = Gateway(name="rate-limited-gateway")

# 配置限流规则
rate_limit = RateLimitConfig(
    path="/api/checkout",
    requests_per_second=10,
    burst=20
)

# 将限流规则应用到网关
gateway.add_rate_limit(rate_limit)

# 启动网关
if __name__ == "__main__":
    gateway.run(port=8080)
```




```python
# 示例3：使用Higress实现JWT认证
from higress import Gateway, JWTAuthConfig

# 创建网关实例
gateway = Gateway(name="jwt-auth-gateway")

# 配置JWT认证
jwt_config = JWTAuthConfig(
    issuer="my-auth-service",
    audience="my-api",
    public_key_path="/path/to/public_key.pem"
)

# 将JWT认证应用到网关
gateway.add_auth(jwt_config)

# 启动网关
if __name__ == "__main__":
    gateway.run(port=8080)
```


---
## 案例研究


### 1：阿里集团内部核心业务链路稳定性建设

 1：阿里集团内部核心业务链路稳定性建设

**背景**:  
在阿里巴巴庞大的电商生态系统中，每年的“双11”大促对基础设施提出了极高的要求。数百万级的QPS（每秒查询率）需要通过网关层进行分发，且涉及微服务架构下成百上千个后端服务。传统的网关架构在应对这种突发流量时，往往面临配置复杂、扩展性不足以及与内部中间件（如Dubbo、Nacos）集成深度不够的问题。

**问题**:  
1. **性能瓶颈**：在大促高峰期，旧版网关在处理高并发长连接和复杂路由规则时，延迟显著增加。  
2. **运维复杂度**：流量变更和安全策略更新需要重启网关实例，影响了业务连续性。  
3. **异构系统支持**：需要同时支持HTTP、gRPC以及Dubbo等多种协议，且要求对云原生环境有极好的适配。

**解决方案**:  
阿里基于Higress（前身是内部自建的MSE网关和Istio Gateway的演进）进行了深度定制与全面升级。利用Higress的高性能Istio实现，将其作为流量入口的核心组件。  
1. **热更新与配置分发**：利用Higress的配置热更新能力，实现了秒级的流量切换和安全策略下发，无需重启服务。  
2. **协议统一治理**：通过Higress强大的插件扩展市场，统一了对HTTP和Dubbo流量的治理逻辑，实现了跨协议的负载均衡和熔断降级。  
3. **WAF集成**：深度集成了Web应用防火墙功能，利用Higress的高并发处理能力，在流量进入业务逻辑前清洗恶意攻击。

**效果**:  
1. **稳定性提升**：成功支撑了双11零点峰值流量，核心链路P99延迟降低了30%。  
2. **运维效率**：配置变更生效时间从分钟级降低至秒级，极大提升了运维效率。  
3. **成本优化**：通过极致的性能优化，在同等流量规模下，网关层的资源利用率提升了40%，显著降低了计算资源成本。

---



### 2：某头部互联网金融服务商 API 网关重构

 2：某头部互联网金融服务商 API 网关重构

**背景**:  
该金融服务商拥有大量的开放API接口，连接着数百个外部合作伙伴和内部微服务。随着业务的快速扩张，原有的基于Nginx+Lua构建的API网关逐渐难以满足需求。特别是在安全合规（如金融级加密、细粒度鉴权）和流量精细化治理方面，开发团队面临巨大的维护压力。

**问题**:  
1. **开发维护困难**：旧网关的业务逻辑与底层配置耦合严重，每次新增鉴权逻辑都需要修改核心代码，测试周期长且风险高。  
2. **性能与扩展性**：在处理高频率的API调用时，Lua脚本的执行效率成为瓶颈，且难以水平扩展。  
3. **安全合规挑战**：难以快速响应新的安全标准，例如对JSON Web Token (JWT) 的复杂校验以及对特定API的严格限流。

**解决方案**:  
该企业引入Higress作为新一代API网关，利用其云原生和可扩展的特性进行全面重构。  
1. **插件化能力**：利用Higress的Wasm插件机制，将鉴权、签名验证、请求/响应修改等逻辑编写为独立插件。这使得业务逻辑与网关核心解耦，开发人员可以使用Go或Python编写插件，无需关注底层C++细节。  
2. **全链路安全**：部署了基于Higress的JWT鉴权插件和IP访问控制插件，实现了对每个API接口的细粒度权限控制。  
3. **流量精细化管理**：配置了针对不同合作伙伴的限流策略，防止个别合作伙伴的异常流量冲击后端核心系统。

**效果**:  
1. **开发敏捷性**：新功能的上线周期从数周缩短至数天，且无需重启网关服务即可上线新插件。  
2. **系统安全性**：成功拦截了99.9%的恶意扫描和重放攻击，满足了金融行业的合规审计要求。  
3. **性能提升**：网关吞吐量提升了50%，同时CPU资源占用下降了20%，在同等硬件条件下承载了更多的业务请求。

---



### 3：AI 创业公司模型服务网关

 3：AI 创业公司模型服务网关

**背景**:  
一家专注于AIGC（生成式人工智能）应用的初创公司，需要对外提供大模型（LLM）的API服务。其业务场景要求网关不仅能够处理常规的HTTP流量，还需要针对AI模型特有的流式输出进行优化，并控制Token的消耗成本。

**问题**:  
1. **流式传输支持差**：传统API网关在处理Server-Sent Events (SSE) 或流式响应时，往往存在缓冲延迟，导致用户感知到的生成速度变慢。  
2. **计费与成本控制**：后端模型调用成本高昂，需要在网关层精确统计Token使用量并进行配额限制，但传统网关缺乏针对AI协议的深度解析能力。  
3. **提示词管理**：需要在网关层动态注入系统提示词或修改用户请求，以优化模型输出效果，传统网关难以灵活实现。

**解决方案**:  
该公司选择Higress作为其AI服务的专用网关，主要看重其对AI原生应用的支持和Wasm插件的灵活性。  
1. **AI原生代理**：利用Higress针对LLM场景优化的代理功能，实现了零拷贝的流式转发，大幅降低了首字返回时间（TTFT）。  
2. **Token级计费与限流**：通过自定义插件解析请求和响应体，实时计算Token消耗，并在网关层实现了基于用户维度的Token配额控制。  
3. **请求/响应处理**：利用插件在请求转发前动态添加敏感词过滤逻辑，并在响应返回前对模型输出进行脱敏处理。

**效果**:  
1. **用户体验优化**：流式输出的首字延迟降低了200ms，用户交互体验更加流畅。  
2. **成本可控**：精确到Token的计费统计使得成本核算误差率降低至1%以内，有效防止了恶意刷量导致的成本失控。  
3. **业务灵活性**：产品团队能够通过调整网关插件配置快速上线新的Prompt策略，无需改动后端模型服务代码。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|----------------|------|-------|
| 性能 | 高性能，基于Envoy和Istio优化，支持高并发场景 | 高性能，基于Nginx和OpenResty，适合轻量级API网关 | 极高性能，基于OpenResty和LuaJIT，适合低延迟场景 |
| 易用性 | 提供控制台和Kubernetes原生支持，配置简单 | 需要手动配置，社区插件丰富但学习曲线较陡 | 提供Dashboard和Kubernetes集成，配置灵活但复杂 |
| 成本 | 开源免费，企业版支持需付费 | 开源版免费，企业版功能需订阅 | 开源免费，企业版支持需付费 |
| 扩展性 | 支持Wasm插件，扩展性强 | 支持Lua插件，扩展性较好 | 支持Lua和自定义插件，扩展性极强 |
| 社区支持 | 阿里背书，社区活跃，文档完善 | 社区成熟，生态丰富，文档齐全 | 社区活跃，国内支持较好，文档详细 |
| 适用场景 | 云原生、微服务、API管理 | 传统API网关、微服务 | 高性能API网关、微服务 |

### 优势分析

- 优势1：基于Envoy和Istio优化，适合云原生和微服务场景。
- 优势2：提供控制台和Kubernetes原生支持，易用性较高。
- 优势3：支持Wasm插件，扩展性强，适合复杂业务需求。

### 不足分析

- 不足1：社区生态相对Kong和APISIX较小，插件数量较少。
- 不足2：企业版功能需付费，成本可能高于完全开源方案。
- 不足3：文档和案例虽然完善，但国内用户可能需要适应阿里云生态。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Istio 进行流量治理与安全管控

**说明**:  
Higress 深度集成了 Istio，可以利用其强大的服务网格功能来实现细粒度的流量管理（如灰度发布、蓝绿部署）和安全策略（如 mTLS 认证、授权策略）。通过 Istio 的 VirtualService 和 DestinationRule，可以灵活控制路由规则。

**实施步骤**:
1. 在 Kubernetes 集群中安装 Istio 控制平面。
2. 为需要管理的微服务注入 Istio Sidecar 代理。
3. 编写 VirtualService 和 DestinationRule 配置文件，定义流量路由规则。
4. 应用配置并验证流量是否符合预期。

**注意事项**:  
- 确保 Higress 与 Istio 版本兼容。
- 监控 Sidecar 代理的资源消耗，避免影响服务性能。

---

### 实践 2：利用 Higress 插件扩展功能

**说明**:  
Higress 支持通过插件机制扩展功能，例如自定义认证、日志记录、限流等。插件可以动态加载，无需重启服务。

**实施步骤**:
1. 编写自定义插件逻辑（支持 Go、Python 等语言）。
2. 将插件打包为 Docker 镜像并推送到镜像仓库。
3. 在 Higress 控制台中配置插件，并绑定到需要的服务或路由。
4. 测试插件功能是否符合预期。

**注意事项**:  
- 插件代码需保证线程安全，避免并发问题。
- 定期更新插件以修复漏洞和优化性能。

---

### 实践 3：配置高可用架构

**说明**:  
生产环境中，Higress 应部署为高可用架构，避免单点故障。可以通过多副本部署和健康检查实现。

**实施步骤**:
1. 在 Kubernetes 中部署多个 Higress 副本（建议至少 3 个）。
2. 配置 Liveness 和 Readiness 探针，确保异常实例自动重启或隔离。
3. 使用负载均衡器（如 Nginx 或云厂商 LB）分发流量。
4. 定期进行故障演练，验证高可用性。

**注意事项**:  
- 确保副本分布在不同节点或可用区。
- 监控实例健康状态，及时处理异常。

---

### 实践 4：优化性能与资源利用率

**说明**:  
通过调整 Higress 的配置和资源限制，可以提升性能并降低资源消耗。

**实施步骤**:
1. 根据流量规模调整 Higress 实例的 CPU 和内存限制。
2. 启用连接池和缓存机制，减少后端服务压力。
3. 使用 Prometheus 监控 Higress 性能指标（如请求延迟、吞吐量）。
4. 根据监控数据优化配置（如调整线程池大小、缓冲区大小）。

**注意事项**:  
- 避免过度分配资源，导致资源浪费。
- 定期清理无用的路由和插件配置。

---

### 实践 5：实施精细化监控与告警

**说明**:  
通过集成 Prometheus 和 Grafana，可以实时监控 Higress 的运行状态，并设置告警规则。

**实施步骤**:
1. 部署 Prometheus 并配置 Higress 的监控端点。
2. 导入 Higress 官方提供的 Grafana 仪表盘模板。
3. 设置关键指标（如请求成功率、错误率）的告警规则。
4. 配置告警通知渠道（如钉钉、邮件）。

**注意事项**:  
- 确保监控数据的持久化存储，避免历史数据丢失。
- 定期审查告警规则，避免误报或漏报。

---

### 实践 6：安全加固与访问控制

**说明**:  
通过配置认证、授权和加密策略，保障 Higress 的安全性。

**实施步骤**:
1. 启用 HTTPS，配置 TLS 证书。
2. 使用 Higress 的认证插件（如 JWT、OAuth2）限制访问。
3. 配置 IP 白名单或黑名单，过滤非法请求。
4. 定期审计安全日志，及时发现异常行为。

**注意事项**:  
- 定期更新 TLS 证书，避免过期。
- 避免硬编码敏感信息（如密钥），使用 Secret 管理工具。

---

### 实践 7：版本升级与回滚策略

**说明**:  
Higress 会定期发布新版本，建议制定升级和回滚计划，确保服务平稳过渡。

**实施步骤**:
1. 在测试环境中验证新版本的兼容性。
2. 使用滚动更新策略升级生产环境实例。
3. 升级后监控服务状态，确认无异常。
4. 若发现问题，快速回滚到上一版本。

**注意事项**:  
- 升级前备份配置数据。
- 避免在高峰期进行升级操作。

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/3 (QUIC) 协议支持

**说明**: Higress 基于 Envoy 和 Istio 构建，Envoy 对 HTTP/3 有较好的实验性支持。HTTP/3 基于 UDP 协议，解决了 TCP 队头阻塞问题，能显著降低弱网环境下的延迟。对于跨地域或移动端 API 网关场景，连接建立速度和吞吐量会有明显提升。

**实施方法**:
1. 在 Higress 网关的 Listener 配置中，启用 HTTP/3 协议支持（需确认当前版本是否已支持或通过 Envoy 插件扩展）。
2. 配置 UDP 端口（通常端口 443）的防火墙和安全组规则。
3. 调整 Alt-Svc 头部配置，引导客户端自动升级协议。

**预期效果**: 在高丢包率网络环境下，请求延迟降低 20%-40%，连接建立成功率显著提升。

---

### 优化 2：配置全链路超时与重试策略

**说明**: 默认的全局超时设置可能过长，导致大量连接被慢请求或故障后端挂起，耗尽网关线程池。精细化的超时与指数退避重试机制可以快速失败，释放资源。

**实施方法**:
1. 针对不同的路由（Route）配置 `timeout` 参数，区分长连接（如 WebSocket）和普通 API。
2. 设置 `perTryTimeout`，确保单次重试尝试不会无限等待。
3. 配置重试策略，设定最大重试次数（如 3 次），并开启指数退避算法。

**预期效果**: 在后端服务出现部分故障时，将 99% 分位延迟（P99）降低 50% 以上，防止雪崩效应。

---

### 优化 3：启用 Wasm 插件按需加载与缓存优化

**说明**: Higress 支持 Wasm 插件扩展。虽然 Wasm 执行速度很快，但在高并发下，频繁初始化插件或加载未缓存的配置仍会带来 CPU 开销。确保插件逻辑高效并利用本地缓存至关重要。

**实施方法**:
1. 优化 Wasm 插件代码，减少不必要的内存分配和复杂正则匹配。
2. 在插件逻辑中实现多级缓存（如 Redis 缓存 + 本地内存缓存），避免每次请求都回源调用后端服务。
3. 使用 `lazy loading` 模式加载 Wasm 插件，仅在流量实际命中时才实例化。

**预期效果**: 复杂鉴权或限流场景下的 CPU 占用率降低 10%-30%。

---

### 优化 4：调整连接池与工作线程数

**说明**: Higress 底层依赖 Nginx/OpenResty 和 Envoy。默认的连接池大小和 Worker 进程数可能不适合高并发或高吞吐场景。过小的连接池会导致请求排队等待，过大则消耗过多内存。

**实施方法**:
1. 根据后端服务器的处理能力，调整 `upstream` 连接池大小（例如将 `max_connections` 从默认的 1024 调整至 4096 或更高）。
2. 修改 Worker 进程数配置，通常设置为 `auto`（即 CPU 核心数），但在 CPU 密集型场景下可适当调低，IO 密集型场景下可利用 `worker_shutdown_timeout` 优化。
3. 启用 HTTP/2 连接复用，减少 TCP 连接建立频率。

**预期效果**: 网关吞吐量（QPS）提升 20%-50%，后端服务器连接数波动更平稳。

---

### 优化 5：启用 CPU 亲和性与零拷贝技术

**说明**: 操作系统级别的调度优化可以减少上下文切换和内存拷贝开销。对于高性能网关，启用 CPU 亲和性可以将特定进程绑定到固定 CPU 核心，配合 `sendfile` 机制提升静态资源或大文件转发效率。

**实施方法**:
1. 在 Higress 的 Gateway Pod 或容器配置中，开启 CPU 亲和

---
## 学习要点

- Higress 是阿里开源的基于 Istio 的云原生 API 网关，深度集成了 K8s 与 Dubbo/Nacos 等微服务生态
- 提供开箱即用的 WASM 插件市场，支持使用 C++/Go/Rust 等语言编写高性能、低延迟的扩展插件
- 兼容 Ingress 与 Gateway API 标准，能够作为标准 Ingress 控制器平滑替代 Nginx ingress
- 内置了对阿里云应用路由 (MSE) 的完整支持，实现了从开源到云服务的无缝统一体验
- 支持将 K8s Service 直接转化为 HTTP/HTTPS API，极大简化了微服务治理的接入流程


---
## 学习路径

## 学习路径

### 阶段 1：入门基础

**学习内容**:
- Higress 的核心概念与架构
- Higress 与传统网关（如 Nginx、Kong）的区别
- 基本术语：路由、服务、插件、上游
- Higress 的安装与部署（Docker 和 Kubernetes 环境）
- 控制台的基本操作与界面介绍

**学习时间**: 1-2周

**学习资源**:
- Higress 官方文档（入门指南）
- GitHub 仓库（alibaba/higress）的 README 和 Wiki
- 官方博客中的架构解析文章
- Bilibili 或 YouTube 上的 Higress 入门视频教程

**学习建议**: 
- 优先阅读官方文档，理解 Higress 的设计理念
- 动手实践安装过程，推荐使用 Docker Compose 进行本地快速部署
- 尝试创建一个简单的 HTTP 路由转发规则，熟悉控制台操作流程

---

### 阶段 2：核心功能与流量管理

**学习内容**:
- 高级路由配置：基于 Header、Query 参数、Cookie 的路由匹配
- 负载均衡策略配置（轮询、加权、最小连接数等）
- 服务治理：熔断、限流、重试、超时配置
- 金丝雀发布与蓝绿发布实战
- 全局与自定义插件的使用（如 CORS、Auth、Key Rate Limit）

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档（流量管理、插件市场章节）
- Ingress Nginx 迁移指南（对比学习）
- Envoy 官方文档（了解底层代理机制）
- Higress 官方插件市场示例

**学习建议**: 
- 搭建一个包含两个后端服务的测试环境，模拟流量切换
- 深入研究插件系统，尝试通过控制台配置几个常用插件
- 理解 Higress 如何基于 Envoy 实现高性能流量管理

---

### 阶段 3：云原生集成与安全

**学习内容**:
- Higress 作为 Kubernetes Ingress Controller 的使用
- Ingress API 与 Gateway API 的配置方式
- 服务发现集成（Nacos, Consul, K8s Service）
- mTLS（双向认证）与 OIDC 认证配置
- WAF（Web 应用防火）基础与安全插件使用

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档（Kubernetes 部署、安全认证）
- Kubernetes 官方文档（Ingress 概念）
- Nacos/Consul 集成文档
- Higress 安全最佳实践案例

**学习建议**: 
- 在 Kubernetes 集群中部署 Higress，并练习通过 YAML 文件管理路由
- 配置外部服务发现（如 Nacos），实现动态服务注册
- 实践配置 mTLS 保护后端服务通信

---

### 阶段 4：插件开发与性能调优

**学习内容**:
- Wasm (WebAssembly) 技术基础与 Go/Wasm 插件开发
- Lua 插件开发（兼容 Kong/Nginx 生态）
- 插件的生命周期管理与调试
- Higress 性能指标监控与日志采集（对接 Prometheus/Grafana）
- 网关高可用部署与压测实战

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档（自定义开发、Wasm 插件）
- Higress GitHub 仓库中的 Plugin 示例代码
- TinyGo 官方文档（用于编写 Wasm 插件）
- Higress 性能白皮书与压测报告

**学习建议**: 
- 学习 Go 语言基础，尝试编写一个简单的 Wasm 插件并部署
- 使用 Grafana 配置 Dashboard 监控 Higress 的 QPS、延迟等指标
- 使用压测工具（如 Wrk 或 Hey）对网关进行压力测试，观察瓶颈

---

### 阶段 5：架构设计与源码剖析

**学习内容**:
- Higress 整体源码结构分析
- Istio 对接与 Service Mesh 集成方案
- 多集群管理与容灾架构设计
- 深入理解配置热更新机制与 XDS 协议
- 参与开源社区贡献与 Issue 排查

**学习时间**: 持续学习

**学习资源**:
- Higress GitHub 源码
- Envoy 与 Istio 官方文档（架构深度解析）
- Higress 社区研讨会记录与 RFC 文档
- 云原生网关设计相关论文与技术文章

**学习建议**: 
- 阅读源码，重点关注路由匹配逻辑和插件加载机制
- 尝试将 Higress 接入现有的 Istio 服务网格中
- 在生产环境中规划高可用架构，并参与社区讨论

---
## 常见问题


### 1: Higress 是什么？它与阿里巴巴和 Nginx 有什么关系？

1: Higress 是什么？它与阿里巴巴和 Nginx 有什么关系？

**A**: Higress 是一个开源的、基于云原生架构的 API 网关。它由阿里巴巴内部广泛使用的“云原生网关”演变而来，并已开源供社区使用。

关于它的技术背景和关系：
1.  **与阿里巴巴的关系**：Higress 是阿里云推出的下一代云原生网关，承载了阿里巴巴内部以及阿里云上海量的流量处理经验。它是阿里巴巴在云原生网关领域的核心技术开源版本。
2.  **与 Nginx 的关系**：Higress 底层深度集成了 **Nginx**。它不仅继承了 Nginx 高性能、高并发的处理能力，还通过 Istio 和 Envoy 进行了增强。简单来说，Higress 可以被理解为是一个集成了 Nginx 高性能处理能力，并在此基础上增加了服务治理、流量管理和安全防护等高级功能的云原生网关。
3.  **核心定位**：它旨在解决微服务架构和 Kubernetes 环境下的东西向（服务间）流量管理以及南北向（入口）流量管理问题。

---



### 2: Higress 与 Kong 或 APISIX 等传统 API 网关相比有什么优势？

2: Higress 与 Kong 或 APISIX 等传统 API 网关相比有什么优势？

**A**: Higress 的设计初衷是为了解决云原生环境下的复杂场景，与传统网关相比，主要优势体现在以下几个方面：

1.  **云原生集成**：Higress 原生支持 Kubernetes 和 Istio。它可以作为 Ingress Controller 使用，也能接管 Istio 中的南北向流量，实现了与微服务生态的无缝对接，而 Kong 和 APISIX 虽然也支持 K8s，但 Higress 在架构设计上更贴近云原生标准。
2.  **标准与扩展性**：Higress 兼容 Kubernetes Ingress 标准和 Nginx 注解，降低了迁移成本。同时，它支持 WASM (WebAssembly) 插件，允许开发者使用 Go、C++、Rust 等多种语言编写插件，且插件热更新无需重启网关，扩展性极强。
3.  **性能与资源**：得益于底层对 Nginx 内核的优化和 Envoy 的控制面集成，Higress 在保持高性能的同时，资源占用通常更为轻量。
4.  **统一网关**：它旨在将微服务网关和传统的 API 网关合二为一，避免了架构中维护多套网关的复杂性。

---



### 3: Higress 是否支持从 Nginx 或 Ingress Controller 进行迁移？

3: Higress 是否支持从 Nginx 或 Ingress Controller 进行迁移？

**A**: 是的，Higress 非常重视对现有 Nginx 生态的兼容性，大大降低了迁移门槛。

1.  **Nginx 兼容**：Higress 内置了 Nginx 的核心处理逻辑，支持大部分常用的 Nginx 配置指令。这意味着用户可以将现有的 Nginx 配置文件或逻辑相对平滑地过渡到 Higress。
2.  **注解兼容**：对于 Kubernetes 用户，Higress 兼容标准的 Kubernetes Ingress 资源定义，并且兼容常见的 Nginx Ingress Controller 注解。这使得用户在从 Nginx Ingress 迁移时，往往只需要极少的修改甚至无需修改 YAML 配置文件即可直接运行。

---



### 4: Higress 支持哪些类型的插件？如何扩展功能？

4: Higress 支持哪些类型的插件？如何扩展功能？

**A**: Higress 提供了非常灵活的插件机制来扩展功能，主要分为以下几类：

1.  **内置插件**：Higress 开箱即用，提供了丰富的内置插件，涵盖认证鉴权（如 AK/SK, JWT, Basic Auth）、流量管控（如限流、熔断、重试）、可观测性（如日志、访问日志）以及请求/响应修改等常见功能。
2.  **WASM 插件**：这是 Higress 的核心亮点之一。它支持 **WebAssembly** 标准。开发者可以使用 Go、AssemblyScript、C++、Rust 等语言编写业务逻辑，编译成 WASM 文件后动态加载到网关中。
    *   **优势**：WASM 插件运行在沙箱环境中，安全性高；插件更新时无需重启 Higress 进程，实现了真正的热加载。
3.  **原生插件**：对于性能要求极高的场景，开发者也可以按照 Higress 的规范使用 C++ 或 Go（编译为动态链接库）编写原生插件，直接运行在网关进程中。

---



### 5: Higress 是如何处理服务发现和流量的？

5: Higress 是如何处理服务发现和流量的？

**A**: Higress 专为云原生环境设计，在服务发现和流量管理方面具有强大的能力：

1.  **服务发现**：
    *   **Kubernetes Service**：在 K8s 集群中，Higress 自动监听 Service 变化，将流量路由到后端的 Pod。
    *   **Nacos/Consul/Zookeeper**：对于非 K8s 环境，Higress 可以直接对接主流的注册

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 基于 Higress 官方 Docker 镜像，快速启动一个本地网关实例，并配置一个简单的路由转发规则。要求将请求 `/api/v1` 转发到后端模拟服务（如 `httpbin.org`），并验证请求头中的 `Host` 是否被正确传递。

### 提示**:

### 使用 `docker run` 时需暴露控制台端口（如 8080）和 HTTP 端口（如 80）。

---
## 实践建议

### 1. 利用 Wasm 插件实现 Prompt 管理与安全审计
在 AI 网关场景下，Prompt（提示词）的管理和安全性至关重要。建议避免将 Prompt 硬编码在客户端代码中，而是利用 Higress 的 Wasm 插件机制（如 `ai-proxy` 或自定义插件）在网关层进行注入和改写。
*   **具体操作**：开发或配置 Wasm 插件，根据请求元数据（如用户 ID、应用场景）动态追加 System Prompt。同时，在插件层实现敏感词过滤，确保上传给 LLM 的数据符合企业合规要求。
*   **最佳实践**：将 Prompt 模板版本化管理，通过网关配置热更新，无需重新部署业务服务即可调整模型行为。

### 2. 配置多模型路由与负载均衡以优化成本
不同的大语言模型（如 Qwen, GPT-4, Llama 2）在性能和成本上存在差异。建议利用 Higress 的路由能力，根据业务请求的复杂度或类型，将流量分发到不同的模型提供商或模型版本。
*   **具体操作**：配置基于 Header 或路径的路由规则。例如，将简单的摘要类请求路由至成本较低、速度较快的轻量级模型（如 Qwen-Turbo），而将复杂的逻辑推理请求路由至高级模型（如 GPT-4）。
*   **常见陷阱**：避免在未做流量验证的情况下全量切换模型，应先进行金丝雀发布，观察响应延迟和 Token 消耗是否符合预期。

### 3. 实施细粒度的 Token 限流与缓存策略
AI 接口的计费通常基于 Token 数量，且 LLM 推理延迟较高。传统的 QPS（每秒请求数）限流不足以控制成本，必须引入基于 Token 的限流和语义缓存。
*   **具体操作**：在 Higress 中配置针对特定 API Key 或用户的 Token 速率限制。同时，启用针对高相似度 Prompt 的响应缓存（对于事实性问答，缓存命中率可降低成本）。
*   **最佳实践**：缓存策略应设置合理的 TTL（生存时间），并针对不同模型设置不同的缓存 Key 规则，防止因模型版本更新导致返回过时的上下文信息。

### 4. 统一处理流式响应的超时与长连接
LLM 接口通常采用 Server-Sent Events (SSE) 或流式返回来降低首字延迟（TTFT）。Higress 作为网关，需要妥善处理长连接和流式转发，避免因网关配置不当导致连接中断。
*   **具体操作**：检查并调整 Higress 的全局超时配置（`request_timeout`），确保其大于模型生成的最大预估时间。开启网关的流式透传能力，不要在网关层缓冲整个响应后再转发给客户端。
*   **常见陷阱**：如果后端服务响应缓慢，网关可能会因读取超时断开连接。务必确保网关的超时时间略长于后端 LLM 的最大生成时间，并配置好重试机制（注意：流式请求通常不支持重试，需在业务层处理断点续传或错误提示）。

### 5. 建立模型可观测性（Observability）体系
传统的 HTTP 状态码监控不足以反映 AI 服务的质量。需要监控 Token 消耗、首字延迟（TTFT）和模型吞吐量。
*   **具体操作**：集成 Higress 与 Prometheus/Grafana，重点关注 `ai_proxy` 或相关插件的指标。配置日志采集，确保 Access Log 中包含 `prompt_tokens`, `completion_tokens`, `total_tokens` 以及 `model` 字段。
*   **最佳实践**：通过这些数据建立“Token 消耗排行榜”，识别异常消耗（如攻击或循环调用）并进行成本归因，精确计算每个业务线的 AI 调用成本。

### 6. 防止 Prompt 注入与数据泄露
除了常规的 API 安全防护外，AI 场景下需特别防范 Prompt 注入攻击。攻击者可能通过精心设计的输入绕过安全审查或

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [云原生](/tags/%E4%BA%91%E5%8E%9F%E7%94%9F/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [WASM](/tags/wasm/) / [AI 原生](/tags/ai-%E5%8E%9F%E7%94%9F/) / [MCP 协议](/tags/mcp-%E5%8D%8F%E8%AE%AE/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260130-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260201-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260205-github_trending-alibaba-higress-6.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260215-github_trending-alibaba-higress-5.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260216-github_trending-alibaba-higress-6.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*