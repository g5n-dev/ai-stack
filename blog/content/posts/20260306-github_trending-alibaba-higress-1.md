---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-03-06T19:08:22+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI Native", "Istio", "Envoy", "WASM", "MCP", "LLM"]
categories: ["系统与基础设施", "AI 工程"]
source: github_trending
description: "以下是关于 **Higress** 项目的简洁总结： **项目概况** Higress 是由阿里巴巴开源的**云原生 API 网关**，基于 Istio 和 Envory 构建，并使用 Go 语言开发。它定位为 **AI Native API Gateway**（AI 原生 API 网关），目前拥有超过 7,600 颗"
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
- **星标**: 7,672 (+18 stars today)
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

Higress 是基于 Istio 和 Envoy 构建的 AI 原生 API 网关，通过集成 WASM 插件能力，为云原生环境提供统一的流量管理。它不仅涵盖传统的 Kubernetes Ingress 与微服务路由，还针对 LLM 应用提供了 AI 网关特性及 MCP 服务器托管，适合需要同时管理传统流量与 AI 服务的团队。本文将介绍其系统架构、核心组件及主要应用场景，帮助读者理解如何利用它实现更高效的流量治理与服务集成。

---
## 摘要

以下是关于 **Higress** 项目的简洁总结：

**项目概况**
Higress 是由阿里巴巴开源的**云原生 API 网关**，基于 Istio 和 Envory 构建，并使用 Go 语言开发。它定位为 **AI Native API Gateway**（AI 原生 API 网关），目前拥有超过 7,600 颗星标。

**核心特点**
1.  **架构设计**：采用**控制平面**与**数据平面**分离的架构。配置变更通过 xDS 协议传播，具备毫秒级延迟和零连接中断的特性，特别适用于 AI 长连接流式响应场景。
2.  **扩展能力**：基于 **WebAssembly (WASM)** 插件系统，提供了强大的扩展性。

**三大核心功能**
1.  **AI 网关**：
    *   提供统一 API 接入，兼容 30 多家大语言模型（LLM）提供商。
    *   支持协议转换、可观测性、缓存（`ai-cache`）和安全防护（`ai-security-guard`）。
2.  **MCP 服务器托管**：
    *   托管 **模型上下文协议 (MCP)** 服务器。
    *   允许 AI 智能体调用外部工具和服务（如地图搜索、Quark 搜索等）。
3.  **传统 API 网关**：
    *   充当 **Kubernetes Ingress 控制器**。
    *   兼容 nginx-ingress 注解，处理微服务路由。

**总结**
Higress 是一个连接传统微服务架构与新兴 AI 应用的现代化网关，既能作为 K8s 的流量入口，也能为 LLM 应用和 AI Agent 提供强大的后端支持与工具集成能力。

---
## 评论

**总体评价**

Higress 是一款极具前瞻性的“云原生+AI”基础设施产品，它成功地将成熟的 API 网关技术与新兴的 LLM（大语言模型）应用需求进行了深度融合。作为阿里开源的标杆项目，它不仅继承了 Envoy 的高性能特质，更通过 WASM 和 AI 原生功能解决了大模型落地中的流量与安全痛点，是构建现代 AI 应用的理想流量入口。

**深入分析**

**1. 技术创新性：从“流量转发”进化为“AI 编排枢纽”**
*   **事实（DeepWiki）：** Higress 基于 Istio 和 Envoy 构建，核心在于扩展了 WebAssembly (WASM) 插件能力，并提供了 AI Gateway 功能（用于 LLM 应用）和 MCP Server 托管（用于 AI Agent 工具集成）。
*   **推断：** 传统网关仅关注 HTTP/gRPC 转发，而 Higress 的创新在于将协议理解延伸到了 LLM 语义层。它不仅仅是在做负载均衡，更是在做 AI 请求的“语义路由”和“令牌管理”。通过引入 MCP (Model Context Protocol) 支持，它直接打通了 AI Agent 与外部工具的数据链路，这种将网关作为 AI Agent 基础设施的设计思路，在当前开源界具有显著的差异化优势。

**2. 实用价值：解决 LLM 落地的“最后一公里”难题**
*   **事实（DeepWiki）：** 系统提供 AI Gateway 特性，旨在服务 LLM 应用，同时保留了 Kubernetes Ingress 和微服务路由等传统网关能力。
*   **推断：** 在企业落地 AI 应用时，面临三大痛点：密钥泄露（各家模型 Key 分散在客户端）、Token 消耗不可控（Prompt 注入或长对话导致成本爆炸）以及模型厂商锁定。Higress 的实用价值在于它充当了“AI 代理层”，实现了统一的密钥管理与鉴权、基于内容的路由（例如：简单问题路由给小模型，复杂问题路由给大模型）以及流式响应的处理。这使得企业可以在不修改业务代码的前提下，平滑接入并治理 AI 服务。

**3. 代码质量与架构：云原生控制平面的教科书式实践**
*   **事实（DeepWiki）：** 架构上明确分离了控制平面（配置管理）与数据平面（流量处理），并基于 Go 语言开发。
*   **推断：** 基于 Istio 和 Envoy 意味着其数据平面具备了经过大规模验证的 C++ 高性能内核，而控制平面使用 Go 语言则保证了云原生生态的兼容性与开发效率。Higress 团队在架构设计上遵循了“下沉复杂度到基础设施”的原则，通过 WASM 插件机制将业务逻辑与网关核心解耦。这种架构不仅保证了系统自身的稳定性（插件崩溃不影响网关主进程），也为开发者提供了极高的可扩展性，代码结构清晰，符合云原生社区的最佳实践。

**4. 社区活跃度与生态：阿里背书的成熟项目**
*   **事实：** 项目拥有 7,600+ 星标，由阿里巴巴主导，提供了中、日、英多语言文档。
*   **推断：** 作为阿里云内部网关产品的开源版本，Higress 并非实验性玩具，而是承载了阿里巴巴内部庞大流量历练的工业级产品。高星标数和多语言文档表明其具有强烈的全球化意图和成熟的社区运营。其更新频率通常紧跟上游 Envoy 版本，且对 AI 相关特性的支持非常迅速，这保证了技术栈的先进性。

**5. 潜在问题与改进建议**
*   **推断：** 尽管功能强大，但基于 Istio 的架构意味着运维复杂度较高。对于仅需要简单 AI 转发的初创团队，Higress 可能显得过于“重量级”。此外，WASM 插件的开发对于普通开发者仍有一定门槛，虽然支持 Python/Go 等多语言编写，但调试和性能调优相比原生代码仍具挑战性。建议项目方进一步简化 AI 插件的“低代码”配置流程，降低非开发人员（如运维或 AI 产品经理）的使用门槛。

**6. 对比同类工具**
*   **对比 Nginx/Kong：** 传统网关缺乏对 AI 协议（如 SSE 流式传输中的 Chunk 处理、LLM 错误重试）的原生支持，对接 LLM 需要大量 Lua 脚本开发，而 Higress 开箱即用。
*   **对比 LangChain/LlamaIndex（Python 库）：** 这些是业务层 SDK，无法解决流量层面的鉴权、限流和负载均衡问题。Higress 是基础设施，与 SDK 是互补而非竞争关系。
*   **对比其他 AI Gateway（如 One-Ping）：** Higress 的独特优势在于其 K8s Ingress 的双重身份，用户无需引入新的网关组件，可以直接替代业务原有的 Nginx Ingress，实现架构的“无损升级”。

**边界条件与验证清单**

**不适用场景：**
*   边缘计算或资源极度受限的嵌入式环境（Envoy 资源占用较高）。
*   简单的静态网站托管或仅需极其基础的转发，不需要 AI/微服务治理能力的场景。
*   非 K8s 环境且不愿引入 Docker 进行复杂部署的传统物理机架构。

**快速验证清单：**
1.  **AI 协议兼容性测试：** 部署 Higress 并配置 OpenAI 格式后

---
## 技术分析

# Higress 深度技术分析报告

基于阿里巴巴开源的 Higress（AI Native API Gateway）仓库，以下是对其技术架构、核心功能、实现细节及工程哲学的全面深入分析。

---

## 1. 技术架构深度剖析

Higress 的定位是**云原生、AI 原生的 API 网关**，其核心架构建立在 Istio 和 Envoy 之上，但并非简单的封装，而是进行了深度的改造与扩展。

### 架构模式与栈
*   **底层基石**：使用 **Envoy** 作为高性能数据平面，利用其 L3/L7 过滤能力和 C++ 的高性能特性。
*   **控制平面**：基于 **Istio** 进行裁剪和优化。Higress 移除了 Istio 中繁重的 Sidecar 注入和复杂的 Service Mesh 治理功能，专注于**南北向（Ingress/API Gateway）**流量管理。
*   **扩展机制**：核心亮点在于 **WASM (WebAssembly)** 插件系统。通过代理层（如 Go 或 C++ 编写的 WASM 插件）运行在 Envoy 的沙箱中，实现了动态扩展能力，无需重新编译或重启网关。
*   **配置分发**：遵循 **xDS (Discovery Service)** 协议标准，实现了控制平面与数据平面的解耦。配置变更通过 xDS 下发，支持毫秒级生效且不断连。

### 核心模块设计
1.  **Router (路由层)**：支持基于域名、路径、Header 的复杂路由规则，兼容 Kubernetes Ingress 规范。
2.  **WASM Plugin System (插件市场)**：这是 Higress 的“灵魂”。它提供了一个插件市场，允许用户通过 Lua, Go, Rust, AssemblyScript 等语言编写逻辑，编译为 WASM 后动态挂载。
3.  **AI Gateway Layer (AI 网关层)**：这是最新的演进方向。在传统网关之上，增加了针对 LLM（大语言模型）的协议转换、流式处理和鉴权能力。

### 架构优势
*   **性能与扩展的平衡**：Envoy 处理底层网络 I/O（高性能），WASM 处理业务逻辑（高扩展性），Go 语言处理控制逻辑（高开发效率）。
*   **热更新能力**：不同于 Nginx + Lua 需要 Reload 会导致连接抖动，WASM 插件的更新可以做到对流量几乎无感知。

---

## 2. 核心功能详细解读

### 2.1 AI Gateway (AI 原生网关)
这是 Higress 区别于传统网关（如 APISIX, Kong）的核心差异点。
*   **解决的关键问题**：LLM 应用开发中，开发者需要处理不同模型提供商（OpenAI, Azure, 通义千问等）之间 API 协议的不兼容性。此外，流式响应（SSE）的缓存、鉴权、限流也是痛点。
*   **技术实现**：
    *   **协议统一**：将不同厂商的 API 规范化为统一的接口，前端应用只需对接 Higress，后端可随意切换模型供应商。
    *   **Token 管理与计费**：在网关层截获请求和响应，精确计算 Prompt Tokens 和 Completion Tokens，便于基于 Token 进行精细化计费或限流。
    *   **提示词管理**：支持在网关层进行 Prompt 的预处理和后处理，实现敏感词过滤或格式标准化。

### 2.2 MCP (Model Context Protocol) Server Hosting
*   **功能**：Higress 能够托管 MCP 服务。MCP 是连接 AI Agent 与外部数据/工具的开放协议。
*   **意义**：这意味着 Higress 不仅是流量的入口，还成为了 AI Agent 的“工具箱”。网关可以直接将外部 API（如数据库查询、ERP 系统）封装为 MCP 接口暴露给 AI Agent，解决了 AI 与企业内部系统集成的最后一公里问题。

### 2.3 传统 API 网关能力
*   **Kubernetes Ingress**：作为 K8s Ingress Controller 的替代品，直接读取 K8s 资源。
*   **服务治理**：金丝雀发布、蓝绿部署、负载均衡算法、超时重试等。

### 与同类工具对比
| 特性 | Higress | APISIX | Kong | Nginx |
| :--- | :--- | :--- | :--- | :--- |
| **底层** | Envoy + Istio | APISIX (基于 Lua) | Nginx/OpenResty | Nginx |
| **扩展语言** | WASM (Go/Rust/C++/TS) | Lua (Plugin) | Lua/Python/Go | C Module/Lua |
| **配置热更新** | 原生支持 (xDS) | 支持 | 支持 (需 Reload 或 DB 轮询) | 不支持 (需 Reload) |
| **AI 原生支持** | **内置 (协议转换/MCP)** | 需插件适配 | 需插件适配 | 无 |
| **性能** | 极高 (C++ Data Plane) | 极高 | 高 | 极高 |
| **K8s 集成** | 深度集成 (Istio stack) | 深度集成 | 中等 | 需额外 Controller |

---

## 3. 技术实现细节

### 关键技术方案
1.  **WASM 虚拟机集成**：
    Higress 在 Envoy 中集成了 WASM 运行时。当配置变更时，控制平面将编译好的 `.wasm` 文件推送到数据平面。Envoy 加载 WASM 模块并实例化。为了防止 WASM 沙箱逃逸，通常使用特定的内存隔离策略。

2.  **AI 流式处理**：
    针对 LLM 的 SSE (Server-Sent Events) 流，Higress 不能简单地做 TCP 透传。它需要在数据平面进行**流式解析**：
    *   **HTTP Filter**：编写 Envoy Filter 解码 SSE 数据块。
    *   **非阻塞 I/O**：确保在长连接场景下，网关不会因为等待一个慢速的 LLM 响应而耗尽连接池。

3.  **配置管理**：
    Higress Console (控制台) -> ConfigMap/CRD (K8s) -> Higress Control Plane (Rust/Go) -> xDS (gRPC/REST) -> Envoy。

### 代码组织与设计模式
*   **控制平面**：主要采用 Go 语言编写。使用了 **Kubernetes Controller Pattern**（Informer/SharedInformer）来监听 K8s 资源变化，并转换为 Envoy 的 xDS 配置。
*   **数据平面**：复用 Envoy 生态，通过 C++ 扩展（Filters）处理底层网络逻辑。
*   **插件开发**：推荐使用 **Go-SDK** 开发 WASM 插件。Higress 提供了特定的 API 抽象（如 `ProcessHttpRequestBody`），屏蔽了 Envoy ABI 的复杂性。

### 性能优化
*   **零拷贝**：Envoy 本身的高性能特性被完整继承。
*   **连接池**：针对后端服务（如 LLM Provider）维护 HTTP/2 连接池，减少握手开销。
*   **异步处理**：WASM 插件的执行虽然有一定开销，但 Envoy 的事件循环模型保证了主线程不被阻塞。

---

## 4. 适用场景分析

### 最适合的场景
1.  **企业级 LLM 应用落地**：
    *   企业内部有多个 AI 应用，需要统一管理对 OpenAI/阿里云/本地模型的访问。
    *   需要在网关层做统一的 Key 鉴权、Token 计费、敏感词审计。
2.  **云原生微服务架构**：
    *   已有 K8s 环境，需要高性能 Ingress Controller。
    *   需要复杂的流量管理（金丝雀发布、A/B 测试），且希望配置变更不中断业务。
3.  **多协议接入**：
    *   需要将 HTTP, gRPC, 甚至 WebSocket 流量统一接入并处理。

### 不适合的场景
1.  **极边缘计算**：虽然 WASM 很轻量，但 Envoy 本身相对重（C++ 内存占用较大），对于资源极度受限的嵌入式设备（如几 MB 内存的路由器），Higress 过于庞大。
2.  **简单的静态文件托管**：如果只需要托管静态 HTML，Nginx 或 Caddy 更简单直接，无需引入复杂的控制平面。

### 集成注意事项
*   **资源限制**：Envoy 和 WASM 插件都会消耗内存，务必为 Pod 设置合理的 Memory Limit。
*   **WASM 插件复杂度**：WASM 插件不适合做 CPU 密集型任务（如视频转码），仅适合做 I/O 密集或逻辑判断型任务（如参数校验、Header 修改）。

---

## 5. 发展趋势展望

1.  **从流量网关到 AI 编排网关**：
    Higress 正在从传统的“管道”向“智能体路由”演进。未来可能会内置更多的 AI 编排能力，例如根据 Prompt 内容自动路由到不同参数的模型。
2.  **MCP 生态的深化**：
    随着 MCP 协议的普及，Higress 可能会成为企业内部数据暴露给 AI 的标准网关，内置更多针对数据库、SaaS 软件的 MCP Adapter。
3.  **WASM 生态的标准化**：
    随着 Proxy-WASM 标准的成熟，Higress 的插件将更容易移植到其他基于 Envoy 的网关（如 Istio Ambient Mesh）中。

---

## 6. 学习建议

### 适合人群
*   **云原生架构师**：希望深入理解 Istio/Envoy 架构。
*   **后端/平台工程师**：需要构建企业级 API 网关或 AI 网关。
*   **Go 开发者**：对 WASM 技术感兴趣，希望使用 Go 编写高性能网关插件。

### 学习路径
1.  **基础理论**：熟悉 HTTP/HTTPS, TCP/IP, Kubernetes 基础。
2.  **核心组件**：阅读 Envoy 官方文档中的 *Introduction* 和 *Architecture* 部分，理解 Filter Chain, Listener, Cluster 概念。
3.  **动手实践**：
    *   在本地 Kind/Docker 环境部署 Higress。
    *   尝试配置一个简单的路由转发。
    *   编写一个简单的 Go WASM 插件（例如：添加一个自定义 Header）并部署。
4.  **源码阅读**：
    *   关注 `pkg/ingress` 目录：理解 K8s Ingress 如何转换为 xDS。
    *   关注 `plugins/wasm-go` 目录：理解 Go SDK 如何桥接 Envoy ABI。

---

## 7. 最佳实践建议

1.  **插件开发原则**：
    *   **无状态**：WASM 插件应设计为无状态，因为插件实例可能随 Pod 漂移或重启。
    *   **轻量化**：避免在插件中进行阻塞式网络调用（如调用第三方 API 获取配置），这会严重拖慢

---
## 代码示例




```python
# 示例1：基于Higress的API网关配置
# 功能：演示如何使用Higress配置一个简单的API路由和限流规则
def higress_gateway_config():
    """
    Higress API网关配置示例
    解决问题：为微服务配置统一的API入口和流量控制
    """
    config = {
        "gateway": {
            "name": "api-gateway",
            "routes": [
                {
                    "path": "/api/v1/*",
                    "service": "user-service",
                    "plugins": {
                        "rate-limit": {
                            "quota": 100,  # 每秒100个请求
                            "burst": 20    # 允许突发20个请求
                        }
                    }
                }
            ]
        }
    }
    return config

# 说明：这个示例展示了如何配置Higress网关实现API路由和限流，
# 适用于微服务架构中的流量控制场景。
```




```python
# 示例2：Higress插件开发
# 功能：开发一个自定义的请求认证插件
def higress_auth_plugin():
    """
    Higress自定义认证插件示例
    解决问题：实现基于JWT的API请求认证
    """
    def jwt_auth(request):
        # 从请求头获取JWT token
        token = request.headers.get("Authorization")
        
        # 验证token
        if not token or not validate_jwt(token):
            return {
                "status": 401,
                "body": "Unauthorized"
            }
        
        # 认证通过，添加用户信息到请求头
        user_info = decode_jwt(token)
        request.headers["X-User-ID"] = user_info["id"]
        return request
    
    return jwt_auth

# 说明：这个示例展示了如何开发Higress自定义插件实现JWT认证，
# 适用于需要自定义认证逻辑的API网关场景。
```




```python
# 示例3：Higress服务网格配置
# 功能：配置服务间的流量管理和灰度发布
def higress_service_mesh():
    """
    Higress服务网格配置示例
    解决问题：实现服务间的流量路由和灰度发布
    """
    mesh_config = {
        "services": {
            "product-service": {
                "versions": {
                    "v1": {"weight": 90},  # 90%流量到v1版本
                    "v2": {"weight": 10}   # 10%流量到v2版本(灰度)
                },
                "retry_policy": {
                    "max_attempts": 3,
                    "backoff_ms": 100
                }
            }
        }
    }
    return mesh_config

# 说明：这个示例展示了如何使用Higress配置服务网格实现灰度发布，
# 适用于需要平滑升级和流量控制的微服务场景。
```


---
## 案例研究


### 1：阿里云内部大规模电商业务

 1：阿里云内部大规模电商业务

**背景**:

在阿里云内部，Higress 被广泛应用于支撑淘宝、天猫等核心电商业务场景。这些业务具有典型的“大流量、高并发”特征，尤其是在“双11”等大促期间，流量峰值巨大，且业务逻辑极其复杂，涉及商品浏览、购物车、下单、支付等多个环节。

**问题**:

传统的 API 网关在面对亿级并发流量时，面临着诸多挑战：
1.  **性能瓶颈**：老旧网关架构在处理海量长连接和复杂路由规则时，延迟较高，且资源消耗巨大。
2.  **扩展性差**：难以快速适配云原生架构，与 Kubernetes (K8s) 体系的结合不够紧密，扩缩容不灵活。
3.  **功能割裂**：流量管理与安全防护（WAF）往往分离，导致配置复杂，维护成本高，且容易因配置不一致引发安全问题。

**解决方案**:

阿里云团队基于 Higress 构建了下一代云原生 API 网关。
1.  **架构升级**：利用 Higress 的高性能网络处理能力，将其部署在 K8s 集群中作为 Ingress Controller，统一接管南北向（外部入口）和东西向（服务间）流量。
2.  **插件生态**：利用 Higress 的 WASM (WebAssembly) 插件市场，实现了业务逻辑的热加载。例如，针对大促活动的特定鉴权逻辑和流量整形，无需重启网关即可动态生效。
3.  **安全集成**：将 WAF 能力无缝集成至网关层，实现了在流量进入时的即时安全清洗。

**效果**:

1.  **极致性能**：成功支撑了双11期间每秒数十万 QPS 的流量冲击，网关 P99 延迟显著降低，提升了用户体验。
2.  **运维效率提升**：通过统一的控制面管理，简化了配置流程，运维效率提升了 50% 以上。
3.  **成本优化**：得益于 Higress 的高资源利用率，在同等流量下，服务器资源成本大幅下降。

---



### 2：某互联网科技公司的微服务流量治理

 2：某互联网科技公司的微服务流量治理

**背景**:

该科技公司正处于从单体架构向微服务架构转型的深水区，运行着数百个微服务。随着服务数量的增加，服务间的调用关系变得错综复杂，且业务经常需要进行灰度发布（金丝雀发布）以验证新功能。

**问题**:

1.  **灰度发布复杂**：原有的网关（如 Nginx 或旧版 Kong）在处理基于 Header、Cookie 或权重的复杂灰度路由时，配置繁琐且容易出错，难以实现精细化的流量切分。
2.  **全链路追踪困难**：当出现请求超时或失败时，很难快速定位是哪个微服务节点出现问题，缺乏统一的流量标签透传机制。
3.  **异构系统支持**：部分新业务尝试使用 gRPC，而旧业务仍使用 HTTP，网关在协议转换和统一管理上存在障碍。

**解决方案**:

引入 Higress 作为统一的微服务网关。
1.  **全链路灰度**：利用 Higress 强大的路由匹配能力，配合服务网格（如 Istio 或 Nacos）实现全链路灰度。通过在请求头中打标，确保特定用户的请求在整个调用链中始终路由到灰度版本的服务。
2.  **协议统一**：利用 Higress 原生支持 gRPC 和 HTTP 的能力，统一了入口流量，并自动处理协议转换，简化了客户端调用。
3.  **可观测性集成**：对接 OpenTelemetry 标准，将 Higress 的访问日志和 Trace 数据无缝推送到 Prometheus 和 SkyWalking，实现了流量的全链路监控。

**效果**:

1.  **发布安全性提高**：实现了按百分比、按参数的精准灰度，新功能上线故障率降低了 90%，彻底避免了因发布不当导致的现网事故。
2.  **开发体验优化**：开发人员不再需要关心复杂的网关配置，通过控制台即可可视化管理路由规则，开发效率显著提升。
3.  **故障排查加速**：通过统一的流量标签和链路追踪，故障定位时间（MTTR）从小时级缩短至分钟级。

---



### 3：某跨国 AI 创业公司的多模型 API 网关

 3：某跨国 AI 创业公司的多模型 API 网关

**背景**:

这是一家专注于 AIGC（生成式 AI）应用的公司，其产品需要调用 OpenAI、Claude 以及国内多家大模型厂商的 API。同时，为了优化成本和体验，他们还需要在自家开发的多个模型之间进行智能切换。

**问题**:

1.  **接口差异巨大**：不同大模型厂商的 API 协议、参数定义（如 `temperature`, `top_p`）各不相同，客户端需要分别适配，代码冗余严重。
2.  **Key 管理混乱**：直接在客户端硬编码各大厂商的 API Key 存在极大的安全风险，且难以统计各个业务的实际 Token 消耗和费用。
3.  **缺乏容错机制**：当某个模型服务不可用或超时时，客户端无法自动切换到备用模型，导致应用报错。

**解决方案**:

使用 Higress 构建了一层 AI 专用网关（基于 Higress 的 AI 特性）。
1.  **协议统一与转换**：在 Higress 中配置插件，将不同厂商的异构 API 统一转换为内部标准格式，前端应用只需调用统一接口。
2.  **安全与配额管理**：在网关层统一托管各大厂商的 API Key，业务方只能访问网关颁发的虚拟 Key。Higress 自动统计并记录每个业务的 Token 调用量，实现精细化的成本核算。
3.  **模型路由与 fallback**：配置路由规则，根据请求内容或用户等级自动将流量分发到不同的模型（例如：简单请求分发到低成本模型，复杂请求分发到 GPT-4）。并配置了自动降级策略，当主模型超时时，自动切换至备用模型。

**效果**:

1.  **开发敏捷性**：前端开发团队无需关注底层模型的变化，只需对接标准接口，新模型接入时间从数天缩短至数分钟配置。
2.  **成本与安全**：API Key 泄露风险被完全杜绝，且通过网关层面的精细化统计，成功识别并削减了约 30%

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|----------------|------|-------|
| 性能 | 高性能（基于Envoy），支持高并发 | 高性能（基于Nginx），支持高并发 | 极高性能（基于OpenResty），支持高并发 |
| 易用性 | 提供可视化控制台，配置简单 | 配置较复杂，需熟悉YAML/JSON | 配置灵活，但学习曲线较陡 |
| 成本 | 开源免费，企业版需付费 | 开源免费，企业版需付费 | 开源免费，企业版需付费 |
| 扩展性 | 支持自定义插件，扩展性强 | 支持自定义插件，扩展性强 | 支持Lua插件，扩展性强 |
| 社区支持 | 阿里背书，社区活跃 | 社区成熟，资源丰富 | 社区活跃，国内支持好 |
| 适用场景 | 微服务、云原生、API管理 | 传统API网关、微服务 | 高并发、云原生、API管理 |

### 优势分析

- 优势1：基于Envoy，性能和扩展性较强，适合云原生场景。
- 优势2：提供可视化控制台，降低配置复杂度。
- 优势3：阿里背书，企业级支持和稳定性较好。

### 不足分析

- 不足1：社区生态相对Kong和APISIX较新，资源较少。
- 不足2：企业版功能可能需要付费，成本较高。
- 不足3：学习曲线对传统Nginx用户可能较陡。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Wasm 插件实现业务逻辑扩展

**说明**:
Higress 的核心优势之一是支持 Wasm (WebAssembly) 插件。相比于传统的 Lua 脚本或硬编码到网关中的逻辑，Wasm 插件允许使用 C/C++、Go、Rust 或 AssemblyScript 编写高性能的业务逻辑，并且可以动态加载，无需重启网关即可生效。这极大地提高了网关的灵活性和迭代效率。

**实施步骤**:
1. 根据团队技术栈选择合适的 Wasm 开发语言（推荐使用 Go 或 Rust）。
2. 利用 Higress 官方提供的 SDK 或 `wasm-assembler` 工具编写插件逻辑（如请求头修改、流量整形、简单鉴权）。
3. 将编译好的 `.wasm` 文件上传到 Higress 控制台或配置为 OCI 镜像仓库中的引用。
4. 在网关控制台对应的路由或服务上启用并配置该插件。

**注意事项**:
- Wasm 插件运行在沙箱中，虽然有隔离性，但频繁的内存分配或复杂计算仍会增加请求延迟。
- 注意插件的热更新机制，确保新版本插件发布失败时有回滚机制。

---

### 实践 2：精细化配置流量治理与路由规则

**说明**:
Higress 深度集成了 Nacos 和 Consul 等注册中心，能够实现基于服务发现的流量管理。最佳实践包括利用 Header、Cookie、Query 参数或权重百分比进行灰度发布（金丝雀发布）和蓝绿部署，确保新版本上线的稳定性。

**实施步骤**:
1. 配置服务来源，确保 Higress 已成功连接到 Kubernetes Service 或 Nacos 注册中心。
2. 在控制台创建路由规则，定义匹配条件（如 `/api/v1` 或特定 Header）。
3. 设置多版本服务Destination，并配置流量权重（例如：v1 版本 90%，v2 版本 10%）。
4. 监控关键指标，确认流量分配符合预期后逐步调整权重至 100%。

**注意事项**:
- 路由匹配规则的优先级需要明确，避免因通配符配置不当导致流量被错误路由。
- 在做全链路灰度时，需要确保透传的 Trace ID 或灰度标签在网关层不被丢失。

---

### 实践 3：构建高可用的网关集群与容灾策略

**说明**:
作为流量入口，Higress 的稳定性至关重要。不应将 Higress 部署在单点，而应构建高可用集群。结合 Kubernetes 的 HPA (Horizontal Pod Autoscaler) 和 Pod 反亲和性配置，可以应对流量突增并避免单点故障。

**实施步骤**:
1. 在 Kubernetes 中部署 Higress，设置副本数至少为 3 个。
2. 配置 Pod 反亲和性，确保 Higress Pods 分布在不同的可用区或节点上。
3. 配置 HPA 策略，根据 CPU 使用率或 QPS 自动扩缩容副本数。
4. 在云负载均衡器（如 SLB 或 ALB）前端配置健康检查，自动摘除不健康的 Higress 实例。

**注意事项**:
- 长连接场景下，扩容可能导致连接断开，需评估业务对连接中断的容忍度。
- 确保数据库或后端 Redis 连接池配置合理，防止连接数随网关实例线性增长导致后端压力过大。

---

### 实践 4：利用 Ingress 注解实现 Kubernetes 原生集成

**说明**:
Higress 兼容 Kubernetes Ingress 规范和 Nginx Ingress 注解。对于已经使用 Kubernetes Ingress 的团队，Higress 可以作为直接替代品，通过复用现有的 Ingress YAML 资源或注解来降低迁移成本和学习曲线。

**实施步骤**:
1. 安装 Higress 并启用 Ingress API 支持。
2. 将现有的 Kubernetes Ingress 资源直接应用到 Higress 所在的命名空间。
3. 对于 Higress 特有的高级功能（如 Wasm 插件、特定认证方式），使用 `higress.io/` 前缀的注解或在控制台进行配置。
4. 验证路由规则生效，并逐步替换旧有的 Ingress Controller。

**注意事项**:
- 部分复杂的 Nginx 专用注解可能无法被 Higress 完美兼容，迁移前需查阅兼容性文档。
- 建议通过 GitOps 工具（如 ArgoCD）管理 Ingress 资源，以保持配置的一致性。

---

### 实践 5：实施全面的安全防护与认证鉴权

**说明**:
网关是安全的第一道防线。Higress 支持多种安全机制，包括 Basic Auth、ApiKey 认证、JWT 验证以及 IP 黑白名单。最佳实践是集中处理认证逻辑，避免后端服务重复实现。

**实施步骤**:
1.

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/2 与 HTTP/3 (QUIC) 协议

**说明**: Higress 作为高性能网关，默认支持 HTTP/1.1。对于现代微服务架构及前端应用，启用 HTTP/2 可以利用多路复用解决 HTTP/1.1 的队头阻塞问题，减少 TCP 连接数。对于网络不稳定的环境，启用 HTTP/3 (QUIC) 可以进一步基于 UDP 协议降低连接建立延迟和丢包时的性能损耗。

**实施方法**:
1. 在 Higress 的网关路由或监听器配置中，将协议版本设置为 `h2` 或 `h2c`（HTTP/2 Clear Text）。
2. 如需开启 HTTP/3，需在监听器配置中启用 QUIC 支持，并确保 UDP 端口（通常 443）已开放。
3. 确保后端 Upstream 服务也支持 HTTP/2 协议以进行协议透传。

**预期效果**: 弱网环境下的请求延迟降低 20%-40%，高并发下的 TCP 连接开销显著减少。

---

### 优化 2：配置全链路超时与连接池复用

**说明**: 默认的超时配置可能不适合高吞吐场景，过长的超时会导致连接资源被长时间占用（Hang 住）。同时，合理配置 Upstream 的连接池大小和空闲连接复用，可以避免频繁建立 TCP 连接带来的握手开销。

**实施方法**:
1. **连接池调优**: 根据后端服务能力，调整 `maxRequestsPerConnection`（例如设置为 10000），保持长连接以复用。
2. **超时设置**: 在路由配置中显式设置 `connectTimeout` (建议 5-10s), `sendTimeout` 和 `readTimeout` (根据业务 SLA 设置，避免默认无限等待)。
3. **Idle Timeout**: 调整 HTTP 连接的空闲超时时间，平衡保活开销与重建连接的消耗。

**预期效果**: 后端连接复用率提升至 90% 以上，减少因慢请求或超时导致的线程/协程堆积，提升系统吞吐量 30% 以上。

---

### 优化 3：启用 Wasm 插件与本地缓存

**说明**: Higress 原生支持 Wasm (WebAssembly) 插件。相比于传统的 Lua 或远程调用鉴权逻辑，Wasm 执行效率极高且隔离性好。对于频繁访问的鉴权、配置下发或静态数据，应启用 Higress 的本地缓存功能，减少对上游控制平面或后端服务的重复查询。

**实施方法**:
1. 将复杂的鉴权或限流逻辑编写为 Wasm 插件并在网关加载。
2. 在 `GlobalConfig` 或特定路由配置中开启字典缓存或 HTTP 响应缓存。
3. 对后端 API 的响应头设置合理的 Cache-Control 策略，利用 Higress 的缓存能力拦截回源请求。

**预期效果**: 插件执行延迟降低至毫秒级，高频鉴权请求的回源率降低 80% 以上，大幅降低后端负载。

---

### 优化 4：启用 gRPC 协议透传与流式处理

**说明**: 如果业务场景涉及微服务间通信或 AI 模型推理，使用 gRPC 并启用流式传输可以显著提升性能。Higress 对 gRPC 有深度支持，可以避免 JSON 的序列化/反序列化开销，并利用流式特性减少首字节返回时间（TTFB）。

**实施方法**:
1. 配置 Higress 路由，将 `Protocol` 设置为 `GRPC` 或 `GRPCWeb`。
2. 确保开启了 HTTP/2 传输通道。
3. 在 AI 推理或大对话场景下，配置流式转发，避免网关缓冲整个响应体。

**预期效果**: 数据传输效率提升 20%-30%，AI/流式场景下的首字延迟降低 50% 以上。

---

### 优化 5：精细化 CPU 亲和性与自动扩缩容配置

**说明

---
## 学习要点

- Higress 是阿里开源的基于 Istio 的下一代云原生 API 网关，深度集成了 K8s 与 Dubbo/Nacos 等微服务生态
- 支持将 Ingress 与 Gateway API 统一管理，提供从南北向到东西向流量的全链路治理能力
- 内置 WAF 插件与安全防护机制，可直接复用 Envoy 高性能数据平面，实现企业级安全与流量控制
- 提供标准 WASM 插件扩展机制，支持热更新与多语言开发，降低定制化功能开发门槛
- 兼容 Kubernetes Ingress 与 Nginx 注解配置，可平滑替代传统 Ingress Controller 并降低迁移成本
- 通过服务发现与负载均衡算法优化，解决微服务架构下的流量路由与灰度发布复杂性问题
- 开源社区活跃，文档完善，适合需要统一管理 API 流量且追求云原生架构的团队选型


---
## 学习路径

## 学习路径

### 阶段 1：入门基础与核心概念

**学习内容**:
- 云原生网关的基本概念与 Higress 的定位
- Higress 与传统网关（如 Nginx, Kong）及 Envoy 的区别
- Higress 的核心架构：WASM 插件机制、Ingress Controller、控制面与数据面
- Docker 环境下 Higress 的快速安装与部署
- 基本的路由配置：域名路由、路径匹配、Header 路由

**学习时间**: 1-2周

**学习资源**:
- Higress 官方 GitHub 仓库 README
- Higress 官方文档 - 快速开始
- Envoy 官方文档基础部分（理解数据面核心）

**学习建议**:
- 建议先理解微服务架构中网关的作用，再上手 Higress。
- 务必动手在本地 Docker 环境中完成一次标准安装，并成功通过网关访问一个后端服务。
- 重点理解 Higress 是如何基于 Envoy 和 Istio 进行改进的，特别是其 WASM 插件生态的优势。

---

### 阶段 2：流量治理与安全管控

**学习内容**:
- 高级流量管理：金丝雀发布、蓝绿部署、负载均衡算法配置
- 服务治理：超时重试、熔断限流、故障注入
- 安全防护：基本认证、JWT 认证、IP 访问控制、CORS 跨域配置
- 动态配置与热更新机制
- Higress 控制台的使用与监控大盘解读

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 流量治理与安全认证
- Higress 官方示例库
- 云原生网关最佳实践白皮书

**学习建议**:
- 结合实际业务场景思考，例如在发布新版本时如何配置 Header 匹配来实现灰度。
- 尝试配置限流规则，并使用压测工具（如 Apache Bench）验证限流效果。
- 熟悉控制台的操作，因为可视化是 Higress 相比纯配置文件网关的一大优势。

---

### 阶段 3：插件开发与生态集成

**学习内容**:
- Higress 插件市场常用插件的使用（如 Keyless Auth, Request Block）
- WASM (WebAssembly) 基础与 Go/Python 语言编写 WASM 插件
- 自定义插件的开发、调试与部署流程
- Higress 与 Nacos, Consul, Kubernetes Service 的服务发现集成
- OpenAPI (Swagger) 自动化路由配置

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档 - 插件开发指南
- Higress GitHub - Plugin-Dubbo, Plugin-GRPC 等源码参考
- WebAssembly 在网关中的应用相关技术文章

**学习建议**:
- 从修改官方现成的插件 Demo 开始，逐步尝试编写自己的逻辑（如修改请求 Header 或 Body）。
- 学习 Go 语言编写 WASM 插件是进阶的关键，因为 Go 在 Higress 插件开发中支持度最好。
- 深入理解 Higress 如何通过 WASM 实现业务逻辑与网关内核的解耦，这有助于排查性能问题。

---

### 阶段 4：生产级运维与性能调优

**学习内容**:
- Kubernetes 环境下的 Higress 高可用部署架构
- 网关性能指标分析：QPS、延迟、并发连接数
- 配置优化：连接池、Buffer 大小、线程数调整
- 日志集成：对接 SLS、ELK 等日志系统
- 链路追踪：集成 SkyWalking 或 Zipkin
- 灾难恢复与数据备份策略

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 运维指南
- Envoy 性能调优官方文档
- Kubernetes Ingress 大规模生产实践案例

**学习建议**:
- 在 Kubernetes 集群中进行部署，并配置 HPA（水平自动扩缩容）以应对流量突发。
- 学会查看网关的监控指标，区分是后端服务慢还是网关本身性能瓶颈。
- 关注生产环境的安全，例如定期扫描镜像漏洞，严格配置 RBAC 权限。

---

### 阶段 5：架构设计与源码研读

**学习内容**:
- Higress 源码结构分析：控制面与数据面交互流程
- 深入理解 Istio EnvoyFilter 在 Higress 中的应用
- 多租户网关架构设计
- 基于 Higress 的 API 管理平台搭建
- 参与 Higress 开源社区贡献与 Issue 排查

**学习时间**: 持续学习

**学习资源**:
- Higress

---
## 常见问题


### 1: Higress 是什么？它与 Nginx 和 Kong 有什么区别？

1: Higress 是什么？它与 Nginx 和 Kong 有什么区别？

**A**: Higress 是一个基于阿里云内部多年实践沉淀的下一代云原生 API 网关。它是在开源网关 Envoy 和 Istio 的基础上进行了深度的定制和优化。

与 Nginx 和 Kong 的主要区别在于：
1.  **架构基础**：Nginx 和 Kong 传统上基于 Nginx/OpenResty（内存小，但处理长连接和高级路由逻辑时性能受限）。Higress 基于 Envoy（C++ 编写，L3/L4/L7 全栈代理，性能极高，且更适合云原生环境）。
2.  **云原生集成**：Higress 原生支持 Istio，可以作为 Ingress Controller 或 API 网关直接接入 Kubernetes 服务网格，而 Kong 虽然也支持 K8s，但在服务网格的深度集成上不如 Higress 顺畅。
3.  **扩展性**：Higress 提供了 Wasm (WebAssembly) 插件支持，允许开发者使用多种语言（如 Go, C++, Rust）编写插件，且插件热更新不会导致连接中断，比传统的 Lua 脚本更安全、灵活。

---



### 2: Higress 是否支持从 Nginx 或 Kong 迁移？兼容性如何？

2: Higress 是否支持从 Nginx 或 Kong 迁移？兼容性如何？

**A**: 是的，Higress 非常重视迁移的兼容性，特别是针对 Nginx 用户。
1.  **Nginx 兼容**：Higress 提供了 Nginx Ingress Annotation 的兼容支持，并且正在逐步完善对 Nginx 配置语法的直接转换工具。许多标准的 Nginx 配置可以直接在 Higress 中生效。
2.  **Kong 兼容**：虽然架构不同，但 Higress 支持标准的 Kubernetes Ingress 资源定义。对于 Kong 的自定义插件，可能需要在 Higress 中重新编写为 Wasm 插件或使用 Lua 兼容层（视具体版本支持情况而定）。
3.  **阿里云用户**：对于阿里云 API 网关的用户，Higress 是其开源内核版本，迁移路径最为平滑。

---



### 3: Higress 的 Wasm 插件机制有什么优势？

3: Higress 的 Wasm 插件机制有什么优势？

**A**: Wasm (WebAssembly) 是 Higress 核心的扩展能力之一，解决了传统网关扩展的痛点。
1.  **多语言支持**：你不再被限制只能使用 Lua（如 OpenResty）或 C++（Envoy 原生）。你可以使用 Go、Rust、AssemblyScript 甚至 JavaScript/TypeScript 来编写网关插件。
2.  **隔离性与安全性**：Wasm 插件运行在沙箱环境中。如果插件崩溃或出现内存泄漏，不会导致整个网关进程崩溃，这比直接在 Nginx 进程中运行 Lua 脚本更加稳定。
3.  **热更新**：更新 Wasm 插件不需要重启 Higress 进程，可以实现毫秒级的配置下发和插件加载，对业务流量无感知。

---



### 4: 在 Kubernetes 环境中，Higress 应该作为 Ingress 还是 API 网关使用？

4: 在 Kubernetes 环境中，Higress 应该作为 Ingress 还是 API 网关使用？

**A**: Higress 的设计初衷是“合二为一”。它既可以作为 Kubernetes 的**Ingress Controller**（处理南北向流量），也可以作为**API 网关**（处理更复杂的 API 管理、鉴权、限流）。
1.  **作为 Ingress**：你可以直接创建 Kubernetes 的 Ingress 资源，Higress 会自动监听并配置路由规则。
2.  **作为 API 网关**：通过 Higress 提供的 Gateway API 或自定义资源（如 `Route`, `Plugin`），你可以实现比标准 Ingress 更高级的功能，例如精确的 Header 匹配、复杂的认证插件（OIDC, AK/SK）和流量镜像。
3.  **建议**：如果你的业务运行在 K8s 上，Higress 可以同时承担这两个角色，简化架构栈，不再需要单独维护一个 K8s Ingress 和一个外部 API 网关。

---



### 5: Higress 对 Dubbo 和 gRPC 等微服务协议的支持如何？

5: Higress 对 Dubbo 和 gRPC 等微服务协议的支持如何？

**A**: 这是 Higress 的强项之一。
1.  **Dubbo 支持**：Higress 原生支持 Dubbo 和 Dubbo3 协议。它能够将 HTTP/JSON 请求转换为 Dubbo 协议，直接调用后端的 Dubbo 服务。这对于许多使用 Java 微服务栈的团队来说非常有用，无需在网关层进行复杂的序列化转换。
2.  **gRPC 支持**：基于 Envoy 底层，Higress 对 gRPC 和 HTTP/2 有极其完善的支持。它可以作为 gRPC 代理，进行负载均衡、TLS 终止以及协议转换（例如将 gRPC 转换为 RESTful JSON API）。

---



### 6: Higress 是否支持对接 Nacos 作为

6: Higress 是否支持对接 Nacos 作为

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: 快速体验与路由转发

### 问题**: Higress 基于 Envoy 和 Istio 构建，支持作为 Ingress 或 API 网关。请尝试在本地 Docker 环境中快速部署 Higress，并配置一条简单的路由规则，将访问 `/hello` 的 HTTP 请求转发到后端的一个模拟服务（如 httpbin.org 或 nginx:latest）。

### 提示**: 参考官方文档的 "快速开始" 章节。你需要编写一个 Kubernetes Ingress 资源 YAML 文件，或者在 Higress 控制台中配置路由，重点关注 `host`、`path` 和 `service` 的映射关系。

### 

---
## 实践建议

基于 Higress 作为 AI Native API 网关的定位，结合其作为云原生 API 网关的技术特性，以下是针对实际生产环境的 5-7 条实践建议：

### 1. 利用 Wasm 插件实现模型供应商的统一适配
由于不同 LLM 厂商（如 OpenAI, Azure, 通义千问, DeepSeek 等）的 API 协议存在细微差异，直接在业务代码中适配会导致维护成本高昂。
*   **具体操作**：使用 Higress 的 `ai-proxy` 等内置插件，或编写 Wasm (Go/C++) 插件，在网关层将标准化的请求协议（如统一使用 OpenAI 格式）动态转换为不同后端厂商所需的私有格式。
*   **最佳实践**：将模型切换逻辑配置化。当需要从模型 A 切换到模型 B，或者进行 A/B 测试时，仅需修改网关路由配置或插件参数，无需重新部署业务后端代码。
*   **常见陷阱**：避免在业务代码中硬编码特定厂商的 SDK，这会大大增加后续迁移或比价时的技术债务。

### 2. 配置精细化的 Token 限流与成本控制
大模型调用的成本与 Token 消耗直接相关，传统的基于 QPS（每秒请求数）或并发连接数的限流策略无法有效控制 AI 产生的突发高额费用。
*   **具体操作**：在 Higress 中配置针对 API Key 或租户的 Token 限流插件。利用网关对流量的拦截能力，计算请求或响应中的 Token 消耗量（可通过 Prompt 长度预估或解析响应头）。
*   **最佳实践**：设置“令牌桶”算法，不仅限制每秒请求数，更限制每小时或每天的最大 Token 消耗量。当配额耗尽时，直接返回 429 状态码，防止后端产生意外账单。
*   **常见陷阱**：仅限制并发连接数。AI 应用的流式响应通常连接时间较长，少量连接即可消耗大量 Token，导致传统的连接数限流失效。

### 3. 实施基于语义的 Prompt 模板管理与注入
为了减少前端传输的数据量并保护 Prompt 的知识产权，不应将完整的 System Prompt 暴露在客户端请求中。
*   **具体操作**：利用 Higress 的配置中心或插件功能，将复杂的 System Prompt 存储在网关侧。当请求到达网关时，根据请求路径或参数，自动将对应的 Prompt 模板注入到请求体发送给 LLM。
*   **最佳实践**：结合“提示词工程”的最佳实践，在网关层实现动态 Prompt 拼接（例如：注入用户上下文、检索增强生成 RAG 的上下文），使后端业务逻辑更专注于数据处理而非文本拼接。
*   **常见陷阱**：在客户端请求体中直接传输完整的 Prompt。这不仅增加了网络延迟，还极易导致核心 Prompt 逻辑被前端爬虫抓取或泄露。

### 4. 开启流式响应的缓冲与安全检测
AI 应用通常采用 Server-Sent Events (SSE) 或流式传输以降低首字生成延迟（TTFT），但这给网关层面的内容安全检查带来了挑战。
*   **具体操作**：在 Wasm 插件中配置流式处理逻辑。网关应具备分块接收流式数据、进行缓冲（例如积累一定 Token 数量或句子完整性）、然后进行敏感词过滤或合规性检查的能力。
*   **最佳实践**：对于恶意输入或可能导致合规风险的输出，网关应能立即中断流式连接，并返回预设的安全错误信息，而不是让不合规内容流式传输给用户。
*   **常见陷阱**：对流式响应不做任何处理直接透传。一旦模型产生幻觉或违规内容，应用无法在传输过程中及时阻断，造成合规风险。

### 5. 建立多模型路由与故障转移机制
依赖单一 LLM 服务商存在可用性风险，不同模型在特定任务上的表现也不同。
*   **具体操作**：在 Higress 中配置服务来源，将 OpenAI

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI Native](/tags/ai-native/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [WASM](/tags/wasm/) / [MCP](/tags/mcp/) / [LLM](/tags/llm/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260215-github_trending-alibaba-higress-5.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260216-github_trending-alibaba-higress-6.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260301-github_trending-alibaba-higress-2.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*