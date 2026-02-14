---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-02-14T16:15:03+08:00
draft: false
entry_kind: "auto"
tags: ["API 网关", "Higress", "AI 原生", "LLM", "Istio", "Envoy", "MCP 协议", "WASM"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "以下是对 Higress 项目的简洁总结： **项目概况** Higress 是一款由阿里巴巴开源的**AI 原生 API 网关**。它基于 Istio 和 Envoy 构建，使用 Go 语言编写，目前 GitHub 星标数超过 7,500。该项目旨在通过云原生技术，为微服务架构和 AI 应用提供统一的流量管理入口。"
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
- **星标**: 7,527 (+10 stars today)
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

Higress 是一款基于 Istio 和 Envoy 构建的 AI 原生 API 网关，旨在为云原生应用与大模型场景提供统一的流量管理入口。它不仅兼容 Kubernetes Ingress 等传统微服务路由需求，更针对 LLM 应用提供了 AI 网关特性及 MCP 服务器托管能力。本文将梳理其系统架构，解析核心组件与 WASM 插件机制，并重点介绍其在 AI 流量处理方面的具体功能与应用场景。

---
## 摘要

以下是对 Higress 项目的简洁总结：

**项目概况**
Higress 是一款由阿里巴巴开源的**AI 原生 API 网关**。它基于 Istio 和 Envoy 构建，使用 Go 语言编写，目前 GitHub 星标数超过 7,500。该项目旨在通过云原生技术，为微服务架构和 AI 应用提供统一的流量管理入口。

**核心架构与特性**
Higress 采用了**控制平面**与**数据平面**分离的架构，支持通过 xDS 协议进行毫秒级配置变更，确保在 AI 流式响应等长连接场景下的稳定性。它利用 WebAssembly (WASM) 插件扩展了核心功能，主要包含以下三大核心能力：

1.  **AI 网关：**
    提供统一的 API 接口，兼容 30 多家大语言模型（LLM）提供商。核心功能包括协议转换、可观测性、缓存以及安全防护，旨在简化 LLM 应用的开发与管理。

2.  **MCP 服务器托管：**
    托管模型上下文协议（MCP）服务器，使 AI 智能体能够方便地调用外部工具和服务。

3.  **传统 API 网关：**
    提供标准的 Kubernetes Ingress 控制器功能，支持微服务路由，并兼容 nginx-ingress 注解。

**总结**
简而言之，Higress 是一个将传统微服务流量管理与新兴 AI 应用需求（如 LLM 统一接入、AI Agent 工具调用）深度融合的下一代网关解决方案。

---
## 评论

**总体评价**

Higress 是一款极具前瞻性的云原生网关，它成功地将**云原生流量治理**与**AI大模型应用编排**合二为一。作为阿里云开源的产物，它不仅继承了 Istio/Envoy 的高性能基因，更通过 WASM 和 MCP 协议填补了传统网关在 AI 时代的功能空白，是目前企业构建“AI Native”基础设施的最优解之一。

**深入分析依据**

**1. 技术创新性：从“流量调度”进化为“模型编排”**
*   **事实**：DeepWiki 明确指出 Higress 基于 Istio 和 Envoy 构建，并引入了 **WebAssembly (WASM)** 插件能力。同时，它集成了 **MCP (Model Context Protocol)** 服务器托管功能，专门针对 LLM 应用提供 AI Gateway 特性。
*   **推断**：Higress 的核心差异化在于它不再仅仅是一个 HTTP 转发器，而是一个**智能化的模型流量调度中心**。通过 WASM，它解决了传统网关（如 Nginx）插件开发门槛高且不安全的问题；通过集成 MCP，它直接解决了 AI Agent 与工具集成的复杂性。它将“Token 计费”、“语义缓存”、“LLM 路由”等业务逻辑下沉到了网关层，这是传统网关不具备的创新。

**2. 实用价值：打通 AI 落地的“最后一公里”**
*   **事实**：文档提到 Higress 提供 AI Gateway 特性用于 LLM 应用，支持 Kubernetes Ingress 和微服务路由，且星标数达到 7.5k+。
*   **推断**：在当前 AI 爆发期，企业面临的最大痛点不是模型本身，而是如何将模型安全、稳定地接入现有业务。Higress 解决了三个关键问题：**统一接入**（一套网关同时管理微服务和 AI 流量）、**成本控制**（通过网关层面的 Token 限流和缓存降低 API 调用成本）以及**数据安全**（在网关层处理敏感信息过滤）。它使得企业无需重构现有微服务架构，即可低成本拥抱 AI。

**3. 架构设计与代码质量：云原生工业级标准**
*   **事实**：项目采用 Go 语言编写，架构上分离了控制平面和数据平面。
*   **推断**：基于 Envoy（数据平面）和 Istio（控制平面）意味着 Higress 在高并发、延迟控制方面经过了生产验证，属于工业级水准。Go 语言的加持使其在云原生生态中具有极佳的可移植性。WASM 的引入体现了优秀的架构扩展性，允许开发者使用 C++/Go/Rust/JS 等多种语言编写插件，而不需要重新编译网关核心，这大大提升了代码的可维护性和生态丰富度。

**4. 社区与生态：阿里背书，标准兼容**
*   **事实**：仓库归属于 Alibaba 组织，拥有 7.5k+ 星标，且提供了中、日、英多语言文档。
*   **推断**：作为阿里云核心产品 Higress 的开源版本，其代码质量和持续迭代能力有强有力保障。多语言文档表明其具有国际化野心和成熟的社区运营。相比于个人项目，Higress 更适合作为企业级标准落地，其与 Kubernetes 生态的深度整合（Ingress 支持）使其成为 K8s 用户的默认首选之一。

**5. 对比优势：降维打击传统 API 网关**
*   **事实**：同类工具通常分为两类：传统网关（如 APISIX, Kong）和 AI 代理（如 LangChain Server）。
*   **推断**：Higress 的优势在于“融合”。传统网关缺乏对 AI 协议（如 SSE 流式传输、OpenAI 协议转换）的原生支持，而 AI 代理工具又缺乏高性能的流量治理能力。Higress 实际上是**“Kong + LangChain Gateway”**的结合体，且性能优于基于 Java/Python 的传统网关。

**边界条件与不适用场景**

*   **边缘计算/嵌入式场景**：Higress 基于 Envoy，资源占用（内存/CPU）相对轻量级 Nginx 仍较高，不适合跑在极度受限的边缘设备上。
*   **简单静态站点**：如果仅需托管简单的静态 HTML 或极其轻量的反向代理，Higress 的配置复杂度（K8s 依赖）可能显得过重。
*   **非 K8s 环境的强依赖者**：虽然支持 Standalone 模式，但其核心优势在于与 K8s 的结合，在传统虚拟机环境下的运维复杂度高于 Nginx/OpenResty。

**快速验证清单**

1.  **AI 协议转换测试**：在配置界面将 OpenAI 格式的请求转发至通义千问/DeepSeek 等其他模型，验证是否支持标准化的 Header 转换和流式响应（SSE）透传。
2.  **WASM 插件热加载**：编写一个简单的 Go WASM 插件（例如添加 HTTP Header），在不重启 Higress Pod 的情况下动态加载，观察是否生效及 CPU 消耗是否在可接受范围。
3.  **Prompt 模板管理**：验证是否可以在网关层配置 Prompt 模板，使得客户端只需发送简短指令，网关自动补全复杂的 System Prompt，测试其灵活性和安全性。

---
## 技术分析

基于对 Alibaba Higress 仓库（特别是其 v1.1+ 版本引入的 AI Gateway 特性）的深入分析，以下是关于其技术特点、架构设计及潜在应用的全面解读。

---

# Higress 深度技术分析报告

## 1. 技术架构深度剖析

Higress 的核心定位是基于 **Istio** 与 **Envoy** 构建的**下一代云原生 API 网关**。它并没有重复造轮子，而是站在巨人的肩膀上，通过将控制面与数据面进行特定裁剪和增强，实现了“AI Native”的愿景。

### 架构模式与栈
*   **底层基石**：使用 **Envoy** 作为高性能数据面（L3/L7 代理），利用其 C++ 高并发处理能力和异步非阻塞模型。
*   **控制面增强**：基于 **Istio** 的控制面架构进行了简化。Higress 移除了 Istio 中繁重的 Sidecar 注入模式，专注于 **Gateway (Ingress)** 模式。它通过 **xDS 协议**（包括 LDS, CDS, RDS 等）将配置秒级下发至数据面。
*   **扩展机制**：引入 **WebAssembly (WASM)** 作为一等公民。这是架构中最关键的一环，允许使用 Go/C++/Rust/JavaScript 编写插件，并在 Envoy 的沙箱中运行，既保证了安全性，又实现了近原子的性能。

### 核心模块与关键设计
1.  **控制面**：
    *   **配置管理**：支持 Kubernetes Ingress YAML、Gateway API 标准以及自定义的 WasmPlugin CRD。
    *   **服务发现**：集成了 Nacos、Zookeeper、Consul 以及 DNS，实现了微服务生态与云原生生态的打通。
2.  **数据面**：
    *   **WASM 虚拟机**：嵌入 WASM 运行时，支持动态加载插件，无需重启网关即可更新业务逻辑。
    *  **AI 代理层**：在标准 HTTP 代理之上，增加了针对 LLM 协议（如 OpenAI Protocol）的特定处理逻辑。

### 技术亮点与创新点
*   **AI Native 网关**：这是 Higress 与传统网关（如 APISIX, Kong）最大的区别。它内置了对 **LLM 流式传输** 的优化，理解 SSE (Server-Sent Events) 协议，并能在网关层进行 Prompt 模板管理、Token 计费和上下文缓存，而不仅仅是透传流量。
*   **MCP (Model Context Protocol) Server Hosting**：Higress 能够作为 MCP Server 的托管点，使得 AI Agent 能够通过网关安全、规范地访问外部工具和数据源，统一了 AI 智能体的工具调用入口。

### 架构优势分析
*   **配置热更新**：基于 xDS 的推模式，配置变更毫秒级生效，且不断连，这对于长连接场景（如 AI 对话流）至关重要。
*   **生态隔离**：WASM 插件与网关核心进程隔离，插件崩溃不会导致网关崩溃，且支持多语言编写，降低了扩展门槛。

---

## 2. 核心功能详细解读

### AI Gateway (AI 网关)
这是 Higress 近期最核心的功能演进。
*   **功能**：提供统一的 LLM 接入层。支持将 OpenAI、Azure OpenAI、通义千问、文心一言等不同厂商的 API 统一封装。支持**Provider 路由**（根据用户需求路由到不同模型厂商）。
*   **解决问题**：
    *   **厂商锁定**：通过统一接口屏蔽不同 LLM 厂商的差异，便于切换模型。
    *   **成本与安全**：在网关层实现 Token 统计和限流，防止 Key 泄露（网关做 Key 转换）。
    *   **Prompt 管理**：将 Prompt 模板配置在网关层，业务端只需传递变量，实现逻辑下沉。

### MCP System (模型上下文协议系统)
*   **功能**：Higress 可以托管 MCP Server。MCP 是连接 AI Agent 与外部数据（如数据库、API）的开放标准。
*   **意义**：将 AI Agent 的“工具调用”能力标准化、网关化。这意味着企业可以通过 Higress 暴露内部 API 给 AI 使用，同时利用网关的鉴权、审计能力管控 AI 的行为。

### 传统 API 网关能力
*   **Kubernetes Ingress**：作为 K8s 集群的流量入口。
*   **微服务治理**：金丝雀发布、蓝绿发布、负载均衡、熔断降级。

### 与同类工具对比
| 特性 | Higress | Kong | APISIX | Nginx |
| :--- | :--- | :--- | :--- | :--- |
| **AI 原生支持** | **强 (内置 Prompt/Token 处理)** | 弱 (需插件) | 弱 (需插件) | 无 |
| **架构基础** | Envoy + Istio | Nginx/OpenResty | etcd + Lua (APISIX) | C++ |
| **WASM 支持** | **原生支持 (Go/C++)** | 支持 (通常需配置) | 支持 | 实验性 |
| **K8s 集成** | **极强 (源自 Istio)** | 强 (Ingress Controller) | 强 | 弱 |
| **扩展语言** | Go (优先), C++, Rust | Lua, Python, Go | Lua, Java, Go | C (模块), Lua (OpenResty) |

---

## 3. 技术实现细节

### 关键技术方案：WASM 插件机制
Higress 推崇使用 Go 编写 WASM 插件。
*   **实现原理**：开发者编写 Go 代码，通过 TinyGo 编译为 WASM 字节码。Higress Control Plane 将字节码推送到 Envoy。
*   **Host ABI**：Higress 在 Envoy 中通过 Proxy-WASM SDK 暴露了 ABI 接口。插件可以访问请求头、Body、响应头，并能调用日志、网络请求等能力。
*   **性能优化**：虽然 WASM 有启动开销，但 Higress 采用了 AOT (Ahead-of-Time) 编译优化和缓存机制，使得插件执行接近原生性能。

### AI 流式处理实现
LLM 的响应通常是 SSE 流。
*   **处理逻辑**：Envoy 接收到 SSE 流后，Higress 的 WASM 插件或内置过滤器可以对流式数据进行**分片处理**。
*   **难点与解决**：在流式传输中修改内容（如敏感词过滤）非常困难，因为数据是分包到达的。Higress 通过流式拦截器，允许在数据块流过时进行缓存、拼接或修改，再发送给客户端，实现了对 AI 输出的实时审核。

### 代码组织结构
*   **`pkg/`**: 核心业务逻辑，包含 xDS 转换器、配置解析器。
*   **`plugins/`**: 内置 WASM 插件的源码，如 `ai-proxy`、`key-auth` 等。
*   **`test/`**: 基于 `golang` 的集成测试框架，验证路由和插件逻辑。

---

## 4. 适用场景分析

### 最佳适用场景
1.  **企业级 AI 应用中台**：
    *   企业内部有多个业务线接入大模型，需要统一的 API 网关来管理 Key、计费、Prompt 模板和流量路由。Higress 是目前最适合这一场景的开源网关。
2.  **云原生微服务架构**：
    *   技术栈深度绑定 Kubernetes，且对服务治理（金丝雀发布、全链路灰度）有高要求的场景。
3.  **需要高度定制扩展能力的场景**：
    *   当业务逻辑复杂，且需要频繁变更网关逻辑（如复杂的鉴权、Header 转换）时，使用 Go 编写 WASM 插件比修改 Nginx C 模块或编写 Lua 脚本更安全、开发效率更高。

### 不适合的场景
1.  **极边缘计算**：由于基于 Envoy 和 WASM，资源消耗（内存和 CPU）相对轻量级 Nginx 略高，不适合在极低内存（如 < 64MB）的边缘设备运行。
2.  **简单的静态文件服务**：杀鸡焉用牛刀，且配置复杂度高于 Nginx 标准。

### 集成方式
*   **Kubernetes**：通过 Helm Chart 部署，通常部署在 `ingress-nginx` 或 `istio-ingress` 的位置。
*   **MCP 集成**：通过配置 YAML 文件定义 MCP Server，将企业内部 API 注册为 AI Agent 的工具。

---

## 5. 发展趋势展望

### 技术演进方向
*   **从流量管理向语义管理演进**：传统网关管理字节，AI 网关管理 Token 和语义。未来 Higress 可能会集成更复杂的向量检索能力（RAG 网关化）或语义缓存。
*   **更深入的 Dapr 集成**：随着分布式应用的发展，Higress 可能会与 Dapr (Distributed Application Runtime) 结合，提供更完善的 Service-to-Service 通信能力。

### 社区反馈与改进空间
*   **文档与易用性**：虽然功能强大，但 AI 相关的高级配置文档目前仍有完善空间，配置复杂度较高。
*   **WASM 调试**：WASM 插件的调试相对困难（相比本地代码），未来社区可能会提供更强大的 IDE 插件或远程调试工具。

---

## 6. 学习建议

### 适合人群
*   **后端/架构师**：希望理解云原生网关、服务网格以及 AI 基础设施架构的开发者。
*   **Go 开发者**：希望使用 Go 扩展网关功能的开发者。
*   **运维工程师**：负责 K8s 集群流量管理的人员。

### 学习路径
1.  **基础理论**：理解 HTTP 代理、反向代理、Kubernetes Ingress 概念。
2.  **核心组件**：学习 Envoy 基础概念以及 Istio 的架构。
3.  **动手实践**：
    *   使用 Docker Compose 或 Minikube 部署 Higress。
    *   配置一个简单的 AI 路由（将 OpenAI 请求转发至通义千问）。
    *   编写一个简单的 Go WASM 插件（例如添加一个自定义 Header）。

---

## 7. 最佳实践建议

### 部署与配置
*   **资源规划**：WASM 插件运行会消耗内存。建议为 Higress Pod 分配足够的内存（建议 > 2Gi），并设置内存限制以防止 OOMKill。
*   **AI 插件配置**：在使用 `ai-proxy` 插件时，务必配置 `context` 缓存策略，避免重复发送相同的 System Prompt 给 LLM 厂商，以降低成本和延迟。

### 性能优化
*   **连接池**：调整 Envoy 的连接池大小

---
## 代码示例




```python
# 示例1：基于Higress的API网关配置
from higress_gateway import GatewayConfig

def configure_api_gateway():
    """
    配置一个简单的API网关，实现请求路由和限流
    解决问题：将外部请求路由到不同的后端服务，并防止流量过载
    """
    gateway = GatewayConfig("my-gateway")
    
    # 添加路由规则：将 /api/v1 请求转发到后端服务A
    gateway.add_route(
        path="/api/v1/*",
        destination="service-a:8080",
        methods=["GET", "POST"]
    )
    
    # 添加限流策略：每秒最多100个请求
    gateway.add_rate_limit(
        path="/api/v1/*",
        requests_per_second=100
    )
    
    # 应用配置
    gateway.apply()
    print("API网关配置已应用")

configure_api_gateway()
```




```python
# 示例2：Higress插件开发 - 请求头增强
from higress_plugin import PluginBase

class HeaderEnhancerPlugin(PluginBase):
    """
    自定义插件：为请求添加自定义头
    解决问题：在请求转发前添加追踪信息或认证信息
    """
    def on_request(self, request):
        # 添加追踪ID
        request.headers["X-Trace-ID"] = generate_trace_id()
        
        # 添加客户端信息
        request.headers["X-Client-IP"] = request.remote_addr
        
        # 添加认证令牌
        request.headers["Authorization"] = f"Bearer {get_token()}"
        
        return request

def generate_trace_id():
    """生成唯一追踪ID"""
    import uuid
    return str(uuid.uuid4())

def get_token():
    """获取认证令牌"""
    return "your_token_here"

# 注册插件
plugin = HeaderEnhancerPlugin()
plugin.register()
```




```python
# 示例3：Higress服务发现配置
from higress_discovery import ServiceRegistry

def configure_service_discovery():
    """
    配置服务发现机制
    解决问题：动态发现和管理后端服务实例
    """
    registry = ServiceRegistry("consul://localhost:8500")
    
    # 注册服务A
    registry.register(
        service_name="service-a",
        service_id="service-a-1",
        address="192.168.1.10",
        port=8080,
        tags=["v1", "stable"]
    )
    
    # 注册服务B
    registry.register(
        service_name="service-b",
        service_id="service-b-1",
        address="192.168.1.11",
        port=8081,
        tags=["v2", "beta"]
    )
    
    # 启用健康检查
    registry.enable_health_check(
        service_name="service-a",
        interval="10s",
        timeout="3s"
    )
    
    print("服务发现配置完成")

configure_service_discovery()
```


---
## 案例研究


### 1：阿里集团内部大规模业务迁移

 1：阿里集团内部大规模业务迁移

**背景**:
在阿里巴巴集团内部的电商业务体系中，存在大量基于 Java 语言构建的传统后端服务。这些服务通常使用 Spring Cloud 或 Dubbo 作为微服务框架，并依赖 Nacos 作为注册配置中心。

**问题**:
随着云原生架构的演进，集团需要将部分业务平滑迁移至 Kubernetes 体系。然而，直接将传统的 Spring Cloud/Dubbo 服务与 K8s 的服务发现机制（CoreDNS）打通存在困难。主要痛点在于：如何让运行在 K8s 之外的 Java 服务（或尚未完全容器化的服务）能够无缝发现并调用 K8s Pod 内的服务，以及如何统一管理南北向（入口网关）与东西向（服务间调用）的流量，避免维护两套 API 网关造成的配置割裂和高昂的运维成本。

**解决方案**:
引入 Higress 作为统一的云原生 API 网关。
1. 利用 Higress 原生支持 Nacos 注册中心的能力，将 Java 服务的注册信息无缝同步到网关。
2. 使用 Higress 的 Ingress 特性对接 K8s Service，实现从传统微服务到 K8s 服务的流量透传。
3. 通过 Higress 的插件市场加载特定协议转换插件，处理 HTTP 与 Dubbo 协议的转换，实现跨协议互通。

**效果**:
实现了传统微服务架构向云原生架构的平滑过渡，业务方无需修改代码即可完成服务发现与流量治理。通过统一网关层，将原本需要分别维护的 Kong/Nginx 与微服务网关合并，网关资源利用率提升了 30%，同时流量路由的配置变更效率提升了一倍。

---



### 2：某 AI 创业公司的高并发推理网关

 2：某 AI 创业公司的高并发推理网关

**背景**:
一家专注于 AIGC（生成式 AI）领域的初创公司，对外提供基于 LLM（大语言模型）的对话及文本生成服务。其后端接入了多个不同的模型供应商（如 OpenAI、通义千问、Llama 本地部署等）。

**问题**:
在业务推广期间，面临两个严峻挑战：
1. **成本控制**：大模型 API 调用成本极高，且第三方供应商存在严格的速率限制（Rate Limit），直接暴露给前端容易导致预算超支或触发限流。
2. **提示词管理**：不同前端应用对同一模型的调用往往需要携带不同的系统提示词，如果硬编码在客户端，更新迭代极其困难。

**解决方案**:
部署 Higress 作为 AI 推理网关。
1. 利用 Higress 提供的 `ai-proxy` 插件，在网关层统一配置多个模型供应商的 API Key 和路由策略。
2. 配置请求头的动态改写插件，根据前端业务类型，自动在请求体中注入或覆盖特定的 Prompt 模板。
3. 启用网关层的缓存与流控策略，对相似的用户查询进行短时缓存去重，减少对后端大模型的无效请求。

**效果**:
成功在网关层屏蔽了后端多模型的差异，前端开发人员只需调用 Higress 的统一接口。通过在网关层统一管理 Prompt，版本迭代时间从小时级缩短到分钟级。同时，利用网关的缓存与流控能力，在流量高峰期有效降低了 20% 的 Token 消耗，保障了服务的高可用性。

---



### 3：多语言混合架构的金融科技公司

 3：多语言混合架构的金融科技公司

**背景**:
某跨国金融科技公司的交易系统采用混合编程语言构建。核心账务服务使用 Go 语言编写（高性能要求），用户管理服务使用 Java (Spring Boot)，而风控规则引擎则使用 Python 开发。

**问题**:
不同语言栈的服务之间缺乏统一的通信标准。Go 服务倾向于使用 gRPC 进行内部通信以获得低延迟，而 Java 和 Python 服务主要暴露 RESTful API。这种差异导致服务间调用非常繁琐，通常需要为每种协议单独开发适配层，且缺乏统一的流量控制和安全认证策略，难以应对复杂的金管局合规要求（如统一的审计日志）。

**解决方案**:
使用 Higress 构建统一的服务网格入口。
1. 配置 Higress 的 gRPC-JSON 转码插件，允许外部的 RESTful 客户端通过标准的 HTTP JSON 格式调用内部的 gRPC 服务，无需修改 Go 服务代码。
2. 在 Higress 全局开启 JWT 认证插件，作为所有服务的统一安全守门员，验证通过后再将请求转发给后端的不同语言服务。
3. 启用 Higress 的日志上报插件，将所有跨语言调用的 Access Log 统一格式化并发送至 Kafka/ES，满足合规审计需求。

**效果**:
解决了异构系统间的通信壁垒，Java 和 Python 服务能够像调用普通 HTTP 接口一样调用 Go 的 gRPC 服务。统一的认证和日志模块使得各业务团队无需关注安全基础设施，专注于业务逻辑开发。系统整体的可观测性大幅提升，排查跨服务调用故障的时间缩短了 50%。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|----------------|------|-------|
| 性能 | 高性能，基于 Envoy 和 Istio，支持高并发 | 高性能，基于 Nginx 和 OpenResty | 高性能，基于 OpenResty 和 LuaJIT |
| 易用性 | 提供可视化控制台，配置简单，支持 K8s 集成 | 配置灵活，但需要一定的学习成本 | 提供丰富的插件和文档，但配置较复杂 |
| 成本 | 开源免费，企业版需付费 | 开源免费，企业版需付费 | 开源免费，企业版需付费 |
| 扩展性 | 支持自定义插件，扩展性强 | 支持自定义插件，但依赖 Lua | 支持自定义插件，基于 Lua 和 Go |
| 社区支持 | 阿里巴巴背书，社区活跃 | 社区成熟，生态丰富 | 社区活跃，国内支持较好 |
| 功能丰富度 | 支持流量管理、安全防护、可观测性 | 功能全面，插件生态丰富 | 功能全面，插件生态丰富 |

### 优势分析

- 优势1：基于 Envoy 和 Istio，与云原生生态集成紧密。
- 优势2：提供可视化控制台，降低配置复杂度。
- 优势3：阿里巴巴技术支持，适合国内企业使用。

### 不足分析

- 不足1：相比 Kong 和 APISIX，插件生态尚不完善。
- 不足2：文档和社区资源相对较少，学习成本较高。
- 不足3：企业版功能有限，可能需要额外开发。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 WASM 实现高性能扩展插件开发

**说明**: Higress 深度集成了 WASM (WebAssembly) 技术，允许开发者使用 C++, Go, Rust, AssemblyScript 或 JavaScript 等多种语言编写插件。相比传统的 Lua 脚本或基于 Java 的 Filter 开发模式，WASM 提供了接近原生的执行性能，并实现了插件与网关核心的强隔离，提升了系统的稳定性。

**实施步骤**:
1. 根据团队技术栈选择合适的 WASM 开发语言（推荐使用 Go 或 Rust 以获得良好的工具链支持）。
2. 引入 Higress 官方提供的 Proxy-WASM Go SDK 或 Rust SDK。
3. 编写插件逻辑，实现 `OnHttpRequestHeaders` 等生命周期钩子。
4. 使用 `tinygo` 或相应的工具链编译生成 `.wasm` 文件。
5. 通过 Higress 控制台或 WASM 插件管理接口上传并配置插件生效范围。

**注意事项**: 编译 Go 代码为 WASM 时必须使用 `tinygo` 编译器，而非标准 Go 编译器；注意 WASM 插件的内存资源限制，避免在插件中处理过大的请求体。

---

### 实践 2：利用 Ingress 注解实现精细化流量管理

**说明**: Higress 兼容 Kubernetes Ingress 规范，并在此基础上扩展了丰富的注解。通过在 Ingress YAML 文件中添加特定的 Annotation，可以在不修改网关全局配置的前提下，对特定路由实施灰度发布、流量镜像、超时控制或重试策略，实现了配置的声明式管理与版本控制。

**实施步骤**:
1. 编辑目标服务的 Kubernetes Ingress 资源文件。
2. 添加 `nginx.ingress.kubernetes.io/canary` 等兼容注解，或 Higress 特有的注解（如 `higress.io/canary-weight`）。
3. 配置灰度规则（例如：基于 Header 的匹配或基于权重的百分比）。
4. 应用更新后的 YAML，通过 `kubectl apply -f` 部署。
5. 监控网关日志与特定服务的流量分布，验证灰度逻辑。

**注意事项**: 不同版本的注解可能存在差异，建议参考 Higress 官方文档中的注解列表；复杂的路由逻辑建议使用 Gateway API 或 Higress 的自定义路由资源 CRD。

---

### 实践 3：构建服务安全防护体系（WAF 与 认证）

**说明**: Higress 内置了强大的安全能力，可以通过配置 WAF (Web Application Firewall) 规则防御常见的 Web 攻击（如 SQL 注入、XSS），同时支持对接主流身份认证系统（如 OIDC、OAuth2 或 API Key）。最佳实践是实施“零信任”原则，在网关层统一处理认证与鉴权，避免将流量暴露给不安全的后端服务。

**实施步骤**:
1. 在 Higress 控制台导航至“安全防护”或“插件管理”页面。
2. 启用 WAF 插件，配置防御规则集（推荐使用默认的中高防护级别）。
3. 配置认证插件，如 `Key Auth` 或 `JWT Auth`，并配置对应的消费者列表。
4. 若需集成企业 SSO，配置 `OIDC` 插件并填写 IdP 的元数据地址。
5. 将安全配置绑定至具体的路由或域名，进行红黑测试验证拦截效果。

**注意事项**: 启用严格的 WAF 规则可能会误伤正常业务请求，建议先开启“监控模式”观察一段时间后再切换至“拦截模式”；密钥管理应使用 Kubernetes Secret 存储而非明文配置。

---

### 实践 4：全链路可观测性集成（Metrics, Logs, Tracing）

**说明**: 为了快速定位性能瓶颈和故障，必须建立完善的可观测性体系。Higress 原生支持 Prometheus 监控指标、集成 OpenTelemetry 进行链路追踪，并支持自定义日志格式。最佳实践是将 Higress 接入现有的 APM (Application Performance Management) 系统，实现从网关到后端服务的全链路监控。

**实施步骤**:
1. **Metrics**: 确保 Higress 开启了 Prometheus Exporter 端口，配置 Prometheus 抓取 Higress 的运行时指标（QPS, 延迟, 状态码）。
2. **Tracing**: 在全局配置中启用 Tracing，配置 OpenTelemetry Collector 地址，确保 `trace_id` 在 HTTP Header 中正确传递。
3. **Logging**: 配置访问日志格式，建议使用 JSON 格式以便解析，并在日志中包含 `upstream_response_time` 等关键字段。
4. 在 Grafana 中导入 Higress 官方提供的 Dashboard 模板进行可视化展示。

**注意事项**: 高流量场景下，开启全量链路追踪会对性能产生较大影响且存储成本高昂，建议采用“概率采样”（如 1% 或 10%）策略；

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/3 (QUIC) 协议支持

**说明**: Higress 基于 Envoy 构建，Envoy 对 HTTP/3 提供了实验性支持。HTTP/3 基于 UDP 协议，解决了 TCP 队头阻塞问题，能显著降低丢包环境下的延迟，并提升连接迁移速度（如切换 Wi-Fi 和 4G 网络）。

**实施方法**:
1. 在 Higress 的网关配置中，监听器（Listener）配置过滤器链。
2. 添加并配置 `Http3` 协议相关的 Listener 配置。
3. 确保端口防火墙允许 UDP 流量通过（通常 HTTP/3 使用 UDP 443 端口）。
4. 配置备用的 HTTP/2 或 HTTP/1.1 监听器，以便在不支持 HTTP/3 的客户端上回退。

**预期效果**: 在弱网环境下，页面加载时间（TTFB）可降低 20%-30%，连接建立成功率提升。

---

### 优化 2：启用 Wasm 插件的隔离与缓存优化

**说明**: Higress 支持通过 Wasm (WebAssembly) 扩展网关功能。默认情况下，Wasm 插件可能在每次请求处理时产生额外的开销。通过配置 Wasm 的预编译和缓存机制，可以减少运行时的编译和初始化延迟。

**实施方法**:
1. 确保使用编译为 WASI 的 Wasm 插件。
2. 在 WasmFilter 配置中，启用 `vm_config` 的缓存策略。
3. 对于不需要每请求都调用的逻辑，使用 `Tick` 或 `CheckRequest` 阶段而非 `OnRequest` 阶段，减少调用频率。
4. 优化 Wasm 代码本身，减少内存分配和拷贝操作。

**预期效果**: Wasm 插件处理延迟可降低 10%-15%，特别是在高并发场景下减少 CPU 开销。

---

### 优化 3：配置全局限流与连接复用

**说明**: 在高并发场景下，后端服务可能因为突发流量崩溃。Higress 提供了全局限流能力。同时，通过优化 HTTP 连接池配置，减少频繁建立 TCP 连接的开销。

**实施方法**:
1. **全局限流**: 在网关路由配置中启用 `local-ratelimit` 或 `global-ratelimit` 插件。基于 IP 或 Header 设置 QPS 阈值。
2. **连接池**: 在 Cluster（集群）配置中调优 `max_connections` 和 `http2_max_requests` 参数。
3. 启用 HTTP/2 或 HTTP/3 连接复用，减少握手次数。

**预期效果**: 保护后端稳定性，将后端无效流量降低至 0；连接复用可将后端建立连接的耗时减少 90% 以上。

---

### 优化 4：启用 DNS 缓存与服务发现优化

**说明**: 默认情况下，网关可能会频繁进行 DNS 查询。如果上游服务域名解析延迟较高，会直接影响请求转发速度。配置 DNS 缓存可以显著减少此类延迟。

**实施方法**:
1. 在 Bootstrap 配置中，调整 `cluster` 的 `dns_refresh_rate` 参数，适当延长刷新间隔（如 60s）。
2. 配置 `dns_lookup_family` 为 `V4_PREFERRED`（除非必须使用 IPv6）。
3. 如果使用 K8s Service 发现，确保 Higress 正确配置了 Service Account 权限，避免频繁的 API Server 调用。

**预期效果**: 消除因 DNS 查询导致的毫秒级延迟（通常 5ms-50ms），提升请求转发的稳定性。

---

### 优化 5：日志与监控采样的分级控制

**说明**: 在极高吞吐量下，全量日志记录和详细的 Metrics 上报会消耗大量 CPU 和磁盘 I/O，成为性能瓶颈。

**实施方法**:
1. **日志采样**: 在 AccessLog 配置中设置 `sampling_percent`（例如 10% 或 1%），仅记录部分请求的

---
## 学习要点

- Higress 是阿里云开源的基于 Istio 的下一代云原生 API 网关，深度集成了 K8s 与 Dubbo/Nacos 等微服务生态。
- 它提供标准 Wasm 插件扩展机制，支持使用 C++/Go/Rust 等语言编写高性能、低耦合的业务逻辑插件。
- 架构上实现了数据面与控制面的分离，支持作为 Ingress Controller 运行，具备极低的网关延迟。
- 兼容 Kubernetes Ingress 与 Gateway API 标准，能够平滑对接云原生环境并简化服务流量管理。
- 内置了针对 AI 服务的特殊优化，提供 AI 代理与提示词（Prompt）管理功能，便于大模型应用的接入与开发。
- 拥有开箱即用的流量治理、安全防护及可观测性能力，有效降低了企业构建现代微服务架构的复杂度。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础与概念认知

**学习内容**:
- **云原生网关基础**: 理解 API 网关在微服务架构中的核心作用（流量入口、安全、路由）。
- **Higress 架构概览**: 了解 Higress 的定位（基于 Envoy 和 Istio），以及它与 Nginx、传统 Kong 网关的区别。
- **核心概念**: 掌握 Ingress、Gateway、Route、Service、Upstream 等基础 K8s 资源对象。
- **基本部署**: 学习如何在本地（Docker Desktop）或 Kubernetes 集群中安装 Higress。

**学习时间**: 1-2周

**学习资源**:
- Higress 官方文档 (架构与快速开始章节)
- Higress GitHub 仓库 (README.md)
- Envoy 官方文档基础概念（了解 Proxy 原理）

**学习建议**:
不要急于配置复杂规则。建议先在本地使用 Docker 启动一个 Higress 实例，通过控制台界面熟悉 UI 操作，理解“域名->路由->服务”的流量转发基本逻辑。

---

### 阶段 2：核心功能与流量治理

**学习内容**:
- **流量路由**: 基于路径、Header、Query 参数的高级路由匹配规则。
- **负载均衡策略**: 学习轮询、随机、一致性哈希等算法的应用场景。
- **服务治理**: 实现超时、重试、熔断等高可用配置。
- **插件体系**: 理解 Higress 的插件机制（Wasm 插件），学习如何使用官方插件（如 Key Auth、Request Block）。
- **全链路灰度**: 学习基于 Header 的流量打标与金丝雀发布。

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 流量治理与插件市场
- Higress 官方示例
- Kubernetes Ingress Nginx 对比文档（理解迁移差异）

**学习建议**:
动手搭建一个模拟的微服务场景（例如：一个商品页调用一个后端服务）。尝试配置路由规则，并故意制造后端服务延迟，测试超时和重试配置是否生效。

---

### 阶段 3：安全防护与协议扩展

**学习内容**:
- **安全认证**: 配置 Basic Auth、API Key、JWT、OAuth2 等认证鉴权机制。
- **HTTPS 配置**: 管理证书、配置 TLS 终止。
- **多协议支持**: 学习 Dubbo、gRPC 协议的代理与转换（Higress 对 Java 生态的强大支持）。
- **跨域与 CORS**: 解决前端跨域访问问题。

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 安全与协议
- Let's Encrypt 自动化证书管理工具
- gRPC 与 Dubbo 官方协议文档

**学习建议**:
重点关注安全插件的使用。尝试配置一个需要 JWT Token 才能访问的路由，并使用 Postman 或 Curl 进行验证。如果你使用 Java，尝试将 Dubbo 服务接入 Higress。

---

### 阶段 4：高性能与插件开发（进阶）

**学习内容**:
- **Wasm 插件开发**: 学习使用 Go 或 C++ 开发自定义 Wasm 插件，实现业务逻辑的动态扩展。
- **高可用部署**: 在生产环境中部署 Higress，关注资源限制、健康检查与滚动更新。
- **性能调优**: 理解 Envoy 的配置调优，连接池管理，长连接保持。
- **服务发现集成**: 深入了解 Nacos、Consul、Kubernetes DNS 等注册中心的集成原理。

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档 - Wasm 插件开发
- Envoy Wasm (Proxy-Wasm) 规范
- Higress 源码分析

**学习建议**:
这是从“使用者”迈向“专家”的关键一步。尝试编写一个简单的 Wasm 插件（例如：在响应头中添加一个自定义 Header），并在 Higress 控制台中上传并启用它。

---

### 阶段 5：生态集成与架构设计（精通）

**学习内容**:
- **AI 网关**: 学习 Higress 在大模型（LLM）场景下的应用，如 Token 限流、Prompt 转发。
- **服务网格 (Istio) 集成**: 理解 Higress 作为 Istio Ingress Gateway 的角色，实现东西向与南北向流量的统一管理。
- **多集群管理**: 设计跨地域、多集群的流量容灾架构。
- **源码级掌控**: 阅读 Higress 控制面与数据面交互源码，具备贡献代码的能力。

**学习时间**: 持续学习

**学习资源**:
-

---
## 常见问题


### 1: Higress 是什么？它与阿里云以及云原生社区有什么关系？

1: Higress 是什么？它与阿里云以及云原生社区有什么关系？

**A**: Higress 是一款基于阿里云内部多年实践沉淀的下一代云原生网关。它建立在 Istio 与 Envoy 等开源项目之上，由阿里云发起，并已捐赠给云原生计算基金会（CNCF）作为沙箱项目。Higress 的定位是作为云原生网关，旨在打通微服务架构与云原生 API 网关的边界，提供统一的流量管理入口。它既支持传统的南北向流量（API 网关场景），也支持东西向流量（服务网格场景），并且深度集成了阿里云的生态，同时也完全兼容标准的 Kubernetes 和 Istio 环境。

---



### 2: Higress 与 Nginx、Istio 以及传统的 API 网关（如 Apache APISIX 或 Kong）有什么区别？

2: Higress 与 Nginx、Istio 以及传统的 API 网关（如 Apache APISIX 或 Kong）有什么区别？

**A**:
*   **与 Nginx 相比**：Higress 基于 Envoy（C++ 实现，高性能）而非 Nginx。Nginx 主要依赖配置文件管理，热更新复杂；而 Higress 提供了标准的 K8s Ingress Controller 和 K8s Gateway API 支持，具备更强的动态配置能力和服务发现集成。
*   **与 Istio 相比**：Istio 主要专注于服务网格（东西向流量）管理，通常使用 Ingress Gateway 作为入口，配置较为复杂（基于 VirtualService 等 CRD）。Higress 在兼容 Istio CRD 的同时，针对 API 网关场景进行了优化，提供了更简化的配置模型（如兼容 Nginx Ingress 注解、原生支持 Dubbo 等），并降低了资源开销。
*   **与 Kong/APISIX 相比**：这些是基于 OpenResty (Nginx+Lua) 的传统网关。Higress 基于 Envoy (C++/Go)，在长连接支持（如 Dubbo、gRPC）、热更新稳定性以及云原生集成（深度整合 K8s Service）方面通常具有架构优势，且 Higress 原生支持 Wasm 插件，插件扩展的安全性更高。

---



### 3: Higress 如何处理插件扩展？是否支持热加载？

3: Higress 如何处理插件扩展？是否支持热加载？

**A**: Higress 采用了**Wasm (WebAssembly)** 技术作为其主要的插件扩展机制。这是 Higress 的一个核心特性。
*   **优势**：传统的 Lua 插件（如 OpenResty）可能会因为插件崩溃导致网关进程崩溃，且插件语言受限。Wasm 插件运行在沙箱环境中，隔离性更好，即使插件崩溃也不会导致网关进程退出。
*   **热加载**：Higress 支持插件的动态热加载，无需重启网关服务即可生效。
*   **多语言支持**：由于 Wasm 的特性，开发者可以使用 C++, Go, Rust, AssemblyScript, JavaScript (QuickJS) 等多种语言编写插件逻辑，大大降低了开发门槛。

---



### 4: Higress 能否直接对接 Kubernetes (K8s) 服务？是否支持 Nginx Ingress 的迁移？

4: Higress 能否直接对接 Kubernetes (K8s) 服务？是否支持 Nginx Ingress 的迁移？

**A**:
*   **K8s 对接**：Higress 原生支持 Kubernetes Ingress 资源和 Gateway API。它可以自动监听 K8s 的 Service 变化，实现基于服务名的自动负载均衡和健康检查，无需手动配置后端 IP 地址。
*   **迁移支持**：Higress 高度兼容 Nginx Ingress 的注解。这意味着，如果你正在使用 Nginx Ingress Controller，通常只需将 Ingress 资源中的 `ingress.class` 修改为 `higress`，大部分现有的配置即可直接在 Higress 上运行，大大降低了迁移成本。

---



### 5: Higress 支持哪些协议？特别是对微服务常用协议的支持如何？

5: Higress 支持哪些协议？特别是对微服务常用协议的支持如何？

**A**: Higress 是一款多协议网关，除了标准的 HTTP/HTTPS 和 WebSocket 之外，它对微服务生态中的协议有非常深入的支持：
*   **Dubbo**：Higress 原生支持 Dubbo 协议（包括 Dubbo2 和 Dubbo3），能够将 HTTP 请求转换为 Dubbo 请求调用后端服务，这对于大量使用 Java 微服务栈的企业非常关键。
*   **gRPC**：完全支持 gRPC 协议，包括 gRPC Web 的代理，使得浏览器端可以直接调用后端的 gRPC 服务。
*   **QUIC/HTTP3**：基于 Envory 的底层能力，Higress 也支持 QUIC 协议，提供更好的网络性能。

---



### 6: 在生产环境中部署 Higress 有什么资源要求？性能表现如何？

6: 在生产环境中部署 Higress 有什么资源要求？性能表现如何？

**A**:
*   **资源要求**：作为基于 Envory 的网关，Higress 的资源消耗相对较低且可控。通常建议为每个 Pod 分配至少 2 核 CPU 和 4GB 内存（具体取决于流量规模和并发连接数，特别是长连接较多时内存需求会增加）。由于 Envory 的高性能特性，单核即可处理极高的 QPS。
*   **性能

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 环境搭建与基础路由验证

### 请参考 Higress 官方文档，在本地或 Kubernetes 环境中完成 Higress 的安装与部署。随后，配置一个最简单的 Ingress 路由规则，将访问特定域名（例如 `example.com`）的流量转发到一个后端服务（如 httpbin.org），并通过 `curl` 命令验证连通性。

### 提示**:

---
## 实践建议

基于 Higress 作为 "AI Native API Gateway" 的定位，结合其作为云原生 API 网关的底层能力，以下是 6 条针对实际使用场景的实践建议：

### 1. 利用 Wasm 插件实现 AI 提示词的动态管理
**场景**：在接入大模型（LLM）时，业务方经常需要调整 System Prompt 或上下文，通常需要修改代码并重新发布服务。
**建议**：使用 Higress 的 Wasm 插件能力（特别是 Go 或 Python 编写的插件）来处理提示词模板。
**操作**：
*   将 Prompt 模板存储在配置中心或数据库中，通过 Wasm 插件在请求网关时动态读取并注入到请求体中。
*   利用插件实现“提示词版本管理”，通过网关 Header 控制切换不同版本的 Prompt，从而实现无需重启服务的 A/B 测试。
**陷阱**：注意 Wasm 插件的内存限制，避免在插件中加载过大的模型上下文导致网关内存溢出。

### 2. 配置“模型供应商”路由实现零停机迁移
**场景**：业务初期使用 OpenAI，后期希望切换至阿里云通义千问或其他私有化模型，或者需要在不同模型间做负载均衡。
**建议**：不要在业务代码中硬编码模型 API 地址。
**操作**：
*   在 Higress 中配置服务来源，将 OpenAI、通义千问等定义为不同的后端服务。
*   使用基于 Header 的路由（例如 `x-model-provider: openai` 或 `x-model-provider: qwen`）将流量动态分发到不同的供应商。
*   结合 Higress 的全链路灰度能力，先切 5% 的流量到新模型进行验证。
**陷阱**：不同厂商的 API 签名认证机制可能不同，需要在 Wasm 插件中处理不同格式的鉴权逻辑转换。

### 3. 实施细粒度的 Token 限流与成本控制
**场景**：AI 接口调用成本主要与 Token 数量成正比，传统的基于 QPS（每秒请求数）或 RPM（每分钟请求数）的限流无法有效控制成本。
**建议**：结合 AI 特性配置更精准的限流策略。
**操作**：
*   虽然网关很难精确计算流出的 Token 数（因为流式传输），但可以通过配置“请求体大小限流”来限制输入 Prompt 的最大长度。
*   针对特定 API Key 或用户 ID，配置每分钟 Token 预估配额。
*   开启 Higress 的日志采集，对接计费系统，通过分析请求和响应体大小统计实际 Token 消耗。
**陷阱**：流式响应下，响应体的记录可能会增加网关的 CPU 负载，建议仅在需要审计或计费的特定路由上开启完整的 Body 日志记录。

### 4. 针对流式响应的超时与缓存策略优化
**场景**：大模型推理通常耗时较长（RAG 场景可能超过 30 秒），且常使用 SSE（Server-Sent Events）流式传输。
**建议**：调整网关的默认超时和缓存配置，防止连接被意外切断。
**操作**：
*   **超时设置**：将涉及 AI 调用的路由超时时间（`requestTimeout`）调整至 60s 甚至更长，并确保后端服务连接池配置支持长连接。
*   **缓存策略**：对于高相似度的用户 Query，可以配置基于请求 Body Hash 的本地缓存。网关直接返回缓存的响应，减少对后端模型的重复调用。
**陷阱**：开启缓存时务必设置合理的 Key 过期时间，并针对对话历史记录较长的场景，确保 Cache Key 包含完整的上下文 ID，否则会导致用户获取到错误的上下文回复。

### 5. 处理 AI 接口的鉴权转换与安全防护
**场景**：企业内部通常使用统一的 API Key 或 JWT 认证，而外部 AI 供应商（如 OpenAI）使用各自的 API Key。直接将外部 Key 暴

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [Higress](/tags/higress/) / [AI 原生](/tags/ai-%E5%8E%9F%E7%94%9F/) / [LLM](/tags/llm/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [MCP 协议](/tags/mcp-%E5%8D%8F%E8%AE%AE/) / [WASM](/tags/wasm/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260130-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260205-github_trending-alibaba-higress-6.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260201-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260206-github_trending-alibaba-higress-0.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-8.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*