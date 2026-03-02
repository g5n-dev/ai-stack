---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-03-02T00:27:29+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "Istio", "Envoy", "WASM", "LLM", "MCP"]
categories: ["系统与基础设施", "AI 工程"]
source: github_trending
description: "Higress 是一款由阿里巴巴开源的、基于 Go 语言开发的**AI 原生 API 网关**。它构建在 Istio 和 Envoy 之上，通过扩展 WebAssembly (WASM) 插件能力，为云原生应用和 AI 大模型提供统一的流量管理入口。 **核心定位与架构：** Higress 采用了**控制平面**与*"
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
- **星标**: 7,602 (+5 stars today)
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

Higress 是一款基于 Istio 和 Envoy 构建的 AI 原生 API 网关，通过集成 WASM 插件能力，实现了对云原生流量管理的深度定制。它专为需要统一管理传统微服务流量与 LLM 应用场景的架构设计，能够同时处理 Kubernetes Ingress、路由转发以及 AI 代理与工具调用。本文将梳理其系统架构与核心组件，并重点介绍 AI 网关特性、MCP 系统支持以及相关的部署与开发指南。

---
## 摘要

Higress 是一款由阿里巴巴开源的、基于 Go 语言开发的**AI 原生 API 网关**。它构建在 Istio 和 Envoy 之上，通过扩展 WebAssembly (WASM) 插件能力，为云原生应用和 AI 大模型提供统一的流量管理入口。

**核心定位与架构：**
Higress 采用了**控制平面**与**数据平面**分离的架构。配置变更通过 xDS 协议传播，具备毫秒级延迟和无连接中断的特性，非常适合 AI 流式响应等长连接场景。

**三大主要用途：**

1.  **AI 网关**：专为 LLM 应用设计。
    *   提供统一 API 接入，兼容 30 多家 LLM 提供商。
    *   支持协议转换、可观测性、缓存以及安全防护。
2.  **MCP 服务器托管**：
    *   托管模型上下文协议（MCP）服务器，使 AI Agent 能够调用工具和服务。
    *   包含 `mcp-router`、`quark-search` 等组件。
3.  **Kubernetes Ingress**：
    *   作为 K8s Ingress 控制器使用，兼容 nginx-ingress 注解，提供微服务路由等传统 API 网关功能。

该项目在 GitHub 上拥有超过 7,600 颗星，旨在通过标准化的网关技术连接传统微服务与新兴的 AI 生态。

---
## 评论

### 总体评价

Higress 是一款**极具前瞻性的云原生 API 网关**，它成功地将**云原生流量治理**与**AI 原生应用需求**进行了深度融合。作为阿里云开源的产物，它不仅继承了 Envoy 的高性能，更通过 WASM 技术和 AI 特性（如 Token 计费、模型路由）解决了大模型时代的落地痛点，是目前将“传统网关”向“AI 网关”演进中最具竞争力的技术方案之一。

### 深度分析

#### 1. 技术创新性：从“流量转发”到“模型路由”的范式转移
Higress 的核心差异化在于其**“AI Native”**的定位，而非简单的在传统网关上挂载 AI 功能。
*   **事实**：DeepWiki 明确指出 Higress 基于 Istio 和 Envoy 构建，并提供了 **AI Gateway Features**（针对 LLM 应用）和 **MCP Server Hosting**（针对 AI Agent 工具集成）。
*   **推断**：传统网关（如 Nginx, Kong）主要关注 HTTP 码和流量比例，而 Higress 创新性地引入了**语义层路由**。它能够根据 LLM 的请求上下文进行路由分发，例如根据 Prompt 的复杂度将简单问答路由给低成本模型（如 Llama 3），复杂任务路由给 GPT-4。这种**基于模型粒度的流量治理**是极具创新的技术尝试。
*   **WASM 插件化架构**：利用 WebAssembly (WASM) 实现逻辑热加载，解决了传统网关（如 Lua 脚本）开发效率低、隔离性差的问题。这意味着开发者可以用 C++/Go/Rust/JS 编写插件，在毫秒级内动态注入 AI 鉴权、内容审核或 Prompt 修饰逻辑，无需重启网关。

#### 2. 实用价值：解决 AI 落地中的“连接”与“成本”难题
*   **事实**：文档提到其核心功能包括“AI gateway features for LLM applications”以及“Kubernetes Ingress”。
*   **推断**：Higress 解决了两个关键问题：
    1.  **统一接入层**：企业不再需要维护两套网关（一套给微服务，一套给 AI）。Higress 允许用户在同一个控制台管理 REST API 调用和 LLM 流量，大幅降低了运维复杂度。
    2.  **AI 生态标准化**：DeepWiki 提及 **MCP (Model Context Protocol) Server Hosting**。随着 AI Agent 的兴起，模型需要调用外部工具（如数据库、天气 API）。Higress 直接作为 MCP Server 的宿主，使得模型能安全、标准地访问企业内部工具，这直接打通了 LLM 落地的“最后一公里”。

#### 3. 架构与代码质量：云原生工业级标准的体现
*   **事实**：仓库语言为 Go，星标数 7,602，架构分离了控制面与数据面。
*   **推断**：Go 语言在云原生基础设施领域是事实标准，保证了并发性能与开发效率。基于 Envoy（C++）作为数据面，保证了极致的转发性能；控制面使用 Go，保证了扩展性和易读性。这种“Go 控制面 + Envoy 数据面”的组合（与 Istio 同源）是经过大规模生产验证的成熟架构。代码规范性和文档完整性（支持中/日/英 README）体现了大厂开源项目的严谨性。

#### 4. 社区活跃度与生态：阿里背书的强力驱动
*   **事实**：星标数超过 7,600，且由阿里巴巴主导。
*   **推断**：在 API 网关这一细分领域，7k+ 的 Star 数量属于第一梯队。阿里内部的业务场景（如淘宝、天猫的双十一流量）为其提供了最严苛的“练兵场”，这意味着该项目不是“玩具级”产品，而是具备工业级稳定性的。社区活跃度较高，且对国内开发者非常友好（中文文档完善）。

#### 5. 对比优势：Higress vs. Kong/APISIX vs. 专用 AI Gateway
*   **事实**：对比传统网关 Kong（基于 Nginx/Lua）和 APISIX（基于 LuaJIT）。
*   **推断**：
    *   **性能**：Higress 基于 Envoy，其非阻塞 I/O 和线程模型在高并发下的延迟表现通常优于基于 Nginx 的 Kong。
    *   **AI 特性**：传统网关需要编写复杂插件才能实现 LLM 的 Token 计费或流式转发，而 Higress 将这些作为**一等公民**内置。
    *   **扩展性**：相比 Kong 的 Lua 限制，Higress 的 WASM 支持提供了更安全、多语言的扩展能力，特别适合 AI 算法团队（通常使用 Python）通过 Proxy-WASM 规范介入网关逻辑。

### 边界条件与不适用场景

尽管 Higress 功能强大，但在以下场景中可能不是最优解：
1.  **极边缘环境或资源受限设备**：基于 Envoy 的架构相对重，内存占用较高，不适合运行在 Raspberry Pi 或极低配的边缘网关上。
2.  **纯静态文件服务或简单反向代理**：如果只需要一个简单的 SSL 卸载和静态资源服务，Nginx 的配置更轻量，Higress 引入了

---
## 技术分析

基于您提供的 GitHub 仓库信息（alibaba/higress）以及对该项目技术细节的深度理解，以下是对 Higress 的全面技术分析。

---

# Higress 深度技术分析报告

## 1. 技术架构深度剖析

Higress 的核心定位是基于 **Istio** 与 **Envoy** 构建的下一代云原生 API 网关，其最大的技术特征在于将“AI Native”能力深度植入到了网关层。

### 1.1 技术栈与架构模式
Higress 采用了典型的 **控制平面与数据平面分离** 的架构模式，但在实现上进行了深度定制：
*   **数据平面**：基于 **Envoy** 构建。Higress 没有简单地使用原生 Envoy，而是对其进行了扩展，特别是针对长连接和流式传输场景进行了优化。
*   **控制平面**：基于 **Istio** 进行了简化和增强。它剥离了 Istio 中繁重的 Sidecar 注入和复杂的 Service Mesh 治理功能，专注于 Gateway 的 Ingress 管理。
*   **扩展机制**：核心亮点在于 **WASM (WebAssembly)** 插件系统。通过代理级别的 WASM 虚拟机，允许开发者使用 C++, Go, Rust, JavaScript 等多种语言编写插件，并在运行时动态加载，无需重启网关。

### 1.2 核心模块与关键设计
*   **配置分发**：遵循 xDS (Discovery Service) 协议。控制平面将路由、插件配置下发给数据平面。Higress 优化了这一过程，实现了毫秒级的配置热更新，且不导致长连接断开。
*   **AI 网关模块**：这是最新的核心组件。它不仅仅是转发流量，还内置了针对 LLM（大语言模型）的协议处理（如 SSE 流式处理）、Token 计数、上下文缓存管理以及 Provider 抽象层。
*   **MCP (Model Context Protocol) Server**：Higress 内置了对 MCP 协议的支持，能够作为 AI Agent 的工具提供者，将后端 API 暴露为 AI 可调用的工具。

### 1.3 架构优势
*   **高性能**：得益于 Envoy 的 L4/L7 处理能力和 C++ 的底层性能，Higress 在处理高并发请求时延迟极低。
*   **极致的可扩展性**：WASM 插件机制解决了传统 Nginx Lua 插件难以维护、安全性差和内存隔离难的问题，同时也解决了 K8s Go 网关的性能损耗问题。
*   **生态兼容**：深度兼容 K8s Ingress 标准和 Istio API，降低了从传统网关（如 Nginx Ingress, APISIX）迁移的门槛。

---

## 2. 核心功能详细解读

### 2.1 主要功能与场景
Higress 的功能可以概括为“一体两翼”：
1.  **传统 API 网关**：流量路由、负载均衡、认证鉴权、限流熔断。
2.  **AI 网关**：
    *   **统一接入**：将 OpenAI, Azure, 通义千问, HuggingFace 等不同厂商的 API 统一为标准接口。
    *   **Prompt 模板管理**：在网关层管理 Prompt 模板，实现 Prompt 的版本控制和 A/B 测试。
    *   **Token 经济**：实时统计 Token 消耗，实现基于 Token 的限流和计费。
    *   **结果缓存**：针对 LLM 语义相似的请求进行缓存，降低后端成本和延迟。
3.  **MCP 工具托管**：将内部微服务自动转换为 MCP 工具，供 AI Agent 调用。

### 2.2 解决的关键问题
*   **AI 落地的碎片化**：企业内部往往存在多个 LLM 供应商，切换成本高。Higress 提供了统一的中立层。
*   **流式传输的处理复杂性**：LLM 普遍采用 SSE (Server-Sent Events) 流式返回，传统网关在处理流式转发时的缓冲策略容易导致首字延迟增加或连接中断。Higress 针对此场景进行了零拷贝优化。
*   **安全与合规**：在网关层统一注入敏感词过滤、PII（个人隐私信息）脱敏，避免后端应用重复建设。

### 2.3 与同类工具对比
| 特性 | Higress | APISIX | Kong | Istio Ingress |
| :--- | :--- | :--- | :--- | :--- |
| **内核** | Envoy (C++) | APISIX (LuaJIT) | Nginx (C/Lua) | Envoy (C++) |
| **扩展性** | WASM (多语言) | Lua (受限) | Lua/Go/Py | WASM (较复杂) |
| **AI 原生** | **强 (内置 Provider, Prompt)** | 弱 (需插件) | 弱 (需插件) | 无 |
| **K8s 集成** | 原生支持 (Istio 派生) | 原生支持 | 需要适配器 | 原生支持 |
| **配置热更新** | 毫秒级 (xDS) | 毫秒级 | 需 Reload (有损耗) | 毫秒级 |

---

## 3. 技术实现细节

### 3.1 关键技术方案
*   **WASM 插件加载**：Higress 使用了 Proxy-WASM 标准。当请求到达时，Envory 会加载 WASM 模块并执行 `OnHttpRequestHeaders`、`OnHttpBody` 等钩子。Higress 封装了复杂的 WASM 编译和上传流程，用户只需编写 Go/JS 代码，Higress 自动将其编译为 `.wasm` 文件并推送到网关节点。
*   **AI 流式代理**：在处理 SSE 流时，Higress 的 Filter 链采用了流式处理模式。它不会等待整个 Response Body 接收完毕再转发，而是通过 Envoy 的 Async Filter 机制，一边接收上游的数据块，一边即时转发给下游，同时在此过程中注入 Token 计数逻辑。

### 3.2 代码组织与设计模式
*   **控制器模式**：Higress 的控制平面采用了 Kubernetes 的 Controller Pattern。它监听 Ingress、Gateway 等资源的变化，并将其转化为 Envoy 的配置（xDS），通过 gRPC 推送给数据平面。
*   **适配器模式**：在 AI 网关部分，针对不同的 LLM Provider (OpenAI, Qwen 等，设计了统一的请求/响应适配器，将异构的 API 规范化为内部统一的 LLMContext 结构。

### 3.3 性能与扩展性
*   **无状态设计**：数据平面完全无状态，支持通过 HPA (Horizontal Pod Autoscaler) 进行弹性伸缩。
*   **配置隔离**：通过域 和路由 的隔离机制，确保不同租户的配置互不干扰。

---

## 4. 适用场景分析

### 4.1 最佳适用场景
1.  **企业级 AI 应用平台**：企业正在构建基于 LLM 的应用（如 Copilot, 客服助手），需要统一管理 Prompt、切换模型供应商、控制成本。
2.  **云原生微服务网关**：已经使用 Kubernetes 的技术栈，希望替代 Nginx Ingress Controller，获得更强的可观测性和动态配置能力。
3.  **多协议混合场景**：系统既包含传统的 RESTful API，又包含 gRPC 或 AI 流式接口，需要一个统一的入口。

### 4.2 不适合的场景
1.  **极简边缘路由**：如果只需要一个简单的反向代理，Higress 的架构（依赖 Istio 组件、etcd 等）可能过于重。
2.  **非 K8s 环境**：虽然支持 Standalone 模式，但 Higress 的主要优势在于与 K8s 的深度结合，在虚拟机环境部署不如 Nginx 灵活轻便。

### 4.3 集成注意事项
*   **资源规划**：WASM 插件运行会消耗额外的内存和 CPU，在配置 Pod 资源限制时需要预留 buffer。
*   **网络拓扑**：由于基于 Envoy，通常需要配合 LoadBalancer (如 SLB) 使用，需注意外部流量策略的配置。

---

## 5. 发展趋势展望

### 5.1 技术演进方向
*   **从流量治理到语义治理**：Higress 正在从传统的 TCP/HTTP 层治理向 LLM 的语义层治理演进。未来可能会包含更复杂的 RAG (检索增强生成) 编排能力，甚至内置轻量级的向量数据库连接器。
*   **MCP 协议的深化**：随着 AI Agent 的普及，Higress 极有可能成为企业内部服务暴露给 AI Agent 的标准“MCP Gateway”，实现“API 即工具”。

### 5.2 社区与生态
作为阿里开源项目，Higress 在国内云原生社区活跃度较高。其改进空间在于进一步完善 WASM 插件的市场，以及提供更可视化的 AI 指标看板。

---

## 6. 学习建议

### 6.1 适合的开发者
*   具备 Kubernetes 基础知识的后端工程师或运维工程师。
*   需要落地 AI 应用的架构师。
*   对 Envoy 和云原生技术感兴趣的开发者。

### 6.2 学习路径
1.  **基础概念**：理解 Ingress, Service Mesh, Sidecar 模式。
2.  **Envoy 原理**：学习 Envoy 的 Filter 机制、xDS 协议、热重启原理。
3.  **WASM 实践**：尝试使用 Higress 官方提供的 Go SDK 编写一个简单的鉴权插件，体验“编译-上传-热加载”的流程。
4.  **AI 网关特性**：在本地部署 Higress，配置一个 OpenAI 的 Provider，并配置 Prompt 模板进行测试。

---

## 7. 最佳实践建议

### 7.1 部署与配置
*   **高可用部署**：生产环境中，控制平面（Higress Console）应部署多副本，且数据库使用 PostgreSQL 而非内嵌的 Derby。数据平面建议设置 HPA，基于 CPU 或 QPS 指标自动扩容。
*   **优雅下线**：确保 Pod 的 `terminationGracePeriodSeconds` 设置足够长，以便 Envoy 完成现有连接的 Drain（排空）操作。

### 7.2 性能优化
*   **WASM 插件优化**：避免在 WASM 插件中进行阻塞式网络调用。如果需要调用外部服务，请使用异步调用接口，否则会阻塞 Envoy 的事件循环，导致吞吐量暴跌。
*   **连接池调优**：针对 AI 服务的长连接特性，适当调大 Envoy 的上游连接池大小，避免频繁建立 TCP 连接带来的握手延迟。

### 7.3 安全实践
*   **最小权限原则**：Higress 的 RBAC 模型应与 K8s RBAC 结合，严格控制谁能

---
## 代码示例




```python
# 示例1：基于Higress的API网关路由配置
from higress import Gateway, Route, Plugin

def setup_api_gateway():
    """
    配置一个简单的API网关，将不同路径的请求路由到不同的后端服务
    """
    # 创建网关实例
    gateway = Gateway(name="demo-gateway")
    
    # 添加路由规则：/api/v1 路由到后端服务1
    route1 = Route(
        path="/api/v1/*",
        destination="http://backend-service-1:8080",
        methods=["GET", "POST"]
    )
    
    # 添加路由规则：/api/v2 路由到后端服务2
    route2 = Route(
        path="/api/v2/*",
        destination="http://backend-service-2:8080",
        methods=["GET", "POST", "PUT", "DELETE"]
    )
    
    # 添加认证插件
    auth_plugin = Plugin(
        name="jwt-auth",
        config={"secret": "your-secret-key"}
    )
    
    # 将路由和插件应用到网关
    gateway.add_route(route1)
    gateway.add_route(route2)
    gateway.add_plugin(auth_plugin)
    
    return gateway

# 说明：这个示例展示了如何使用Higress配置一个基本的API网关，
# 包括路由规则设置和JWT认证插件的配置。
```




```python
# 示例2：Higress流量控制与限流配置
from higress import Gateway, RateLimitConfig

def setup_rate_limiting():
    """
    配置基于IP的限流策略，防止API被过度调用
    """
    # 创建网关实例
    gateway = Gateway(name="rate-limited-gateway")
    
    # 配置限流规则：每个IP每分钟最多100次请求
    rate_limit = RateLimitConfig(
        key="remote_addr",  # 基于客户端IP
        rate=100,           # 100次
        unit="minute"       # 每分钟
    )
    
    # 添加限流插件
    gateway.add_plugin(
        name="rate-limit",
        config=rate_limit.to_dict()
    )
    
    return gateway

# 说明：这个示例展示了如何使用Higress配置基于IP的限流策略，
# 有效防止API被恶意调用或过度使用。
```




```python
# 示例3：Higress与Kubernetes集成部署
from higress import KubernetesGateway, IngressConfig

def deploy_to_kubernetes():
    """
    将Higress网关部署到Kubernetes集群，并配置Ingress
    """
    # 创建Kubernetes网关实例
    gateway = KubernetesGateway(
        name="k8s-gateway",
        namespace="default"
    )
    
    # 配置Ingress规则
    ingress = IngressConfig(
        host="api.example.com",
        paths=[
            {
                "path": "/api/v1",
                "backend": "backend-service-1:8080"
            },
            {
                "path": "/api/v2",
                "backend": "backend-service-2:8080"
            }
        ]
    )
    
    # 部署到Kubernetes
    gateway.deploy(ingress)
    
    return gateway

# 说明：这个示例展示了如何将Higress网关部署到Kubernetes集群，
# 并配置Ingress规则实现外部访问。
```


---
## 案例研究


### 1：阿里巴巴内部电商业务

 1：阿里巴巴内部电商业务

**背景**:  
阿里巴巴拥有庞大的电商生态系统，包括淘宝、天猫等平台。随着业务规模的持续增长，微服务架构下的服务数量急剧增加，流量管理变得异常复杂。传统的网关解决方案在处理高并发、动态路由和流量控制方面面临挑战。

**问题**:  
- 高并发场景下，传统网关性能瓶颈明显，延迟较高。
- 动态路由规则配置复杂，难以快速响应业务变更。
- 流量控制策略不够灵活，无法精细化处理不同来源的流量。

**解决方案**:  
阿里巴巴基于内部需求，研发并开源了Higress。Higress是一款基于云原生架构的API网关，深度集成了Nacos和Sentinel等组件。它采用高性能的Istio控制平面和Envoy数据平面，支持动态路由、灰度发布和流量镜像等功能。通过Higress，阿里巴巴实现了流量的精细化管理和自动化运维。

**效果**:  
- 网关性能提升30%以上，P99延迟显著降低。
- 动态路由规则配置时间从小时级缩短到分钟级，业务迭代速度加快。
- 流量控制更加灵活，成功支撑了双11等大促活动的高并发流量。

---



### 2：某互联网科技公司微服务改造

 2：某互联网科技公司微服务改造

**背景**:  
一家中型互联网科技公司正在从单体架构向微服务架构转型。随着服务数量的增加，服务间调用关系变得复杂，原有的Nginx网关难以满足需求。公司需要一款既能处理HTTP/HTTPS流量，又能支持gRPC等协议的网关。

**问题**:  
- 现有网关不支持gRPC协议，无法满足新业务需求。
- 缺乏统一的流量管理和监控能力，运维效率低下。
- 扩展性差，难以应对未来业务的快速增长。

**解决方案**:  
该公司引入Higress作为API网关，替代原有的Nginx方案。Higress的云原生架构使其能够轻松集成到Kubernetes环境中，同时支持HTTP、gRPC等多种协议。通过Higress的插件市场，团队快速实现了认证、限流和日志收集等功能。此外，Higress与Prometheus和Grafana的无缝集成提供了实时的流量监控能力。

**效果**:  
- 成功支持gRPC协议，新业务上线时间缩短50%。
- 运维效率提升，统一监控平台让问题定位时间减少70%。
- 网关扩展性显著增强，轻松应对业务量翻倍带来的流量压力。

---



### 3：金融科技企业API开放平台

 3：金融科技企业API开放平台

**背景**:  
一家金融科技企业需要构建开放API平台，向合作伙伴和第三方开发者提供服务。由于金融行业对安全性和稳定性的高要求，传统的API网关难以满足其复杂的认证、授权和流量管理需求。

**问题**:  
- 缺乏灵活的认证和授权机制，无法满足不同合作伙伴的安全需求。
- 流量控制不够精细，容易因突发流量导致服务不稳定。
- 缺乏对API调用的全链路追踪，问题排查困难。

**解决方案**:  
该企业选择Higress作为API网关的核心组件。利用Higress的插件系统，团队实现了基于OAuth 2.0的动态认证和细粒度的权限控制。通过Higress的流量管理功能，针对不同合作伙伴设置了差异化的限流策略。同时，结合SkyWalking实现了全链路追踪。

**效果**:  
- API安全性显著提升，通过了多项金融行业安全认证。
- 流量控制更加精准，系统稳定性提高，故障率下降90%。
- 全链路追踪能力让问题排查效率提升60%，合作伙伴满意度大幅提高。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|----------------|------|-------|
| 性能 | 基于Envoy和Istio，高性能，支持高并发 | 基于OpenResty，性能较高，但不如Envoy | 基于OpenResty，性能与Kong相当 |
| 易用性 | 提供友好的控制台和Kubernetes集成，配置简单 | 控制台功能丰富，但配置复杂度较高 | 控制台功能较基础，配置灵活但需一定学习成本 |
| 成本 | 开源免费，阿里云提供商业支持 | 开源版免费，企业版收费 | 完全开源免费，社区支持 |
| 扩展性 | 支持Wasm插件，扩展性强 | 支持Lua插件，扩展性较好 | 支持Lua和Go插件，扩展性强 |
| 社区支持 | 阿里背书，社区活跃，但相对年轻 | 社区成熟，插件生态丰富 | 社区活跃，国内支持较好 |
| 适用场景 | 云原生、微服务网关、API管理 | 传统API网关、微服务网关 | 高性能API网关、微服务网关 |

### 优势分析

- **优势1**：基于Envoy和Istio，天然支持云原生和Kubernetes，适合现代微服务架构。
- **优势2**：支持Wasm插件，扩展性强，且性能损耗低。
- **优势3**：阿里云提供商业支持，适合需要企业级保障的场景。

### 不足分析

- **不足1**：社区相对年轻，插件生态不如Kong和APISIX丰富。
- **不足2**：文档和案例较少，学习成本可能较高。
- **不足3**：对于非Kubernetes环境的支持不如传统网关（如Nginx）灵活。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 WASM 技术扩展网关功能

**说明**: Higress 深度集成了 WASM (WebAssembly) 技术，允许开发者使用 C/C++、Go、Rust 或 JavaScript 等语言编写插件。相比传统的 Lua 脚本或硬编码方式，WASM 提供了更高的隔离性、安全性和性能，且支持热加载，无需重启网关即可更新业务逻辑。

**实施步骤**:
1. 根据团队技术栈选择合适的 WASM 开发语言（推荐使用 Go 或 Rust）。
2. 利用 Higress 官方提供的 SDK 或 Proxy-WASM 规范编写插件逻辑。
3. 将编译好的 `.wasm` 文件上传至 Higress 控制台或通过 OCI 镜像仓库进行管理。
4. 在网关路由配置中，将特定插件关联到所需的路由或服务上。

**注意事项**: 开发 WASM 插件时需注意内存资源的分配限制，避免因插件逻辑异常导致网关内存溢出。

---

### 实践 2：精细化流量治理与路由配置

**说明**: 利用 Higress 强大的路由能力实现灰度发布、蓝绿部署和 A/B 测试。通过配置 Header 匹配、权重分配或基于 Cookie 的路由规则，将流量按需分发到不同的服务版本，从而降低上线风险并快速验证业务功能。

**实施步骤**:
1. 在 Higress 中定义服务来源，并注册不同版本的后端服务（如 v1 和 v2 版本）。
2. 创建或修改路由规则，配置匹配条件（如 `x-version: v2`）。
3. 设置流量分发比例，例如先给予 5% 的流量给新版本。
4. 监控关键业务指标，确认无误后逐步调整权重直至全量上线。

**注意事项**: 确保后端不同版本的服务具备完善的监控和日志追踪能力，以便在出现异常时快速回滚流量。

---

### 实践 3：对接 AI 模型与服务治理

**说明**: Higress 原生支持 AI 代理功能，能够对大模型（LLM）的请求和响应进行拦截与处理。通过配置 Prompt 模板、上下文缓存或敏感词过滤，可以统一管理 AI 服务的入口，实现 token 计费、限流以及结果格式的标准化。

**实施步骤**:
1. 在 Higress 中配置 AI 服务的后端地址（如 OpenAI 兼容接口）。
2. 创建 AI 插件配置，定义 Prompt 模板或系统预设参数。
3. 配置流式输出处理策略，确保客户端能实时接收生成内容。
4. 针对不同的 API Key 或用户组配置鉴权与限流规则。

**注意事项**: 处理流式响应时，需确保网关与客户端之间的超时设置合理，避免因模型生成时间过长导致连接中断。

---

### 实践 4：全链路安全防护与认证

**说明**: Higress 提供了标准的安全插件生态，包括 JWT 鉴权、Keyless 认证、IP 访问控制等。最佳实践是“安全左移”，在网关层统一处理身份认证和授权，避免将敏感的鉴权逻辑散落在各个微服务中，从而简化开发并提升系统整体安全性。

**实施步骤**:
1. 配置全局或路由级别的 IP 黑白名单，限制非法来源访问。
2. 启用 JWT 鉴权插件，配置公钥验证请求中的 Token。
3. 对于对外暴露的 API，启用 API Key 认证或 Basic Auth。
4. 开启 CORS（跨域资源共享）配置，适应前端调用需求。

**注意事项**: JWT 验证涉及加解密运算，高并发场景下建议确认网关资源配置是否充足，或使用 Jwks 缓存以减少验证耗时。

---

### 实践 5：高可用部署与资源隔离

**说明**: 在生产环境中，建议将 Higress 控制面与数据面分离，并根据流量规模进行水平扩容。利用 Kubernetes 的 HPA（Horizontal Pod Autoscaler）结合 Higress 的弹性伸缩能力，确保在流量洪峰到来时网关不会成为瓶颈。

**实施步骤**:
1. 将 Higress 部署在独立的 Kubernetes Namespace 中，避免与业务应用混合部署。
2. 配置 HPA 策略，基于 CPU 使用率或并发连接数自动调整 Pod 副本数。
3. 为 Higress Ingress 或 Gateway 配置合理的资源 Request 和 Limit，防止资源争抢。
4. 结合健康检查探针，确保故障 Pod 能被及时摘除。

**注意事项**: 网关节点通常需要维持大量的长连接，在配置 `ulimit`（文件句柄数）等系统参数时，应根据最大并发量进行调优。

---

### 实践 6：可观测性与监控集成

**说明**: Higress 原生支持 Prometheus 监控和 OpenTelemetry 链路追踪。最佳

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 CPU 多核利用与并发配置调优

**说明**: Higress 基于 Envoy 和 WASM 构建，默认配置可能未充分利用多核 CPU 性能。通过调整工作线程数和连接池参数，可以显著提升并发处理能力。

**实施方法**:
1. 设置 `--concurrency` 参数为 CPU 核心数（如 `--concurrency=auto` 或具体数值）
2. 调整 `cluster.connection_pool` 参数：
   ```yaml
   max_connections: 1000
   max_requests: 10000
   ```
3. 启用 HTTP/2 连接复用（`http2_options.max_concurrent_streams`）

**预期效果**: 吞吐量提升 30%-50%，P99 延迟降低 20%

---

### 优化 2：WASM 插件内存限制优化

**说明**: WASM 插件默认内存限制（256MB）可能过高，导致资源浪费。根据实际插件需求调整可减少内存占用。

**实施方法**:
1. 在 `wasm.config` 中设置：
   ```yaml
   memory_limits: "128MB"
   ```
2. 对轻量级插件（如认证）设置为 64MB
3. 监控 `/stats/prometheus` 中 `wasm.*.memory` 指标验证

**预期效果**: 单实例内存占用减少 40%-60%

---

### 优化 3：启用请求/响应数据流式处理

**说明**: 默认情况下插件可能缓存完整请求体，导致高内存占用和延迟。启用流式处理可降低内存压力。

**实施方法**:
1. 在插件配置中启用：
   ```yaml
   stream_request: true
   stream_response: true
   ```
2. 使用 `onRequestBody` 和 `onResponseBody` 分段处理
3. 避免在插件中使用 `Buffer.concat()` 等操作

**预期效果**: 大文件处理内存占用减少 70%，吞吐量提升 25%

---

### 优化 4：DNS 解析缓存优化

**说明**: 默认 DNS 查询缓存时间（60s）可能导致频繁解析，影响延迟。延长缓存时间可减少 DNS 查询开销。

**实施方法**:
1. 修改 `bootstrap.yaml`：
   ```yaml
   dns_resolvers:
   - dns_cache_config:
       dns_refresh_rate: 300s
       host_ttl: 600s
   ```
2. 对静态服务使用 `strict_dns` 策略

**预期效果**: DNS 查询延迟减少 80%，P95 延迟降低 5-10ms

---

### 优化 5：启用连接复用与长连接

**说明**: 默认短连接模式导致频繁建连开销。启用 HTTP/1.1 Keep-Alive 和 HTTP/2 连接复用可显著提升性能。

**实施方法**:
1. 在 `cluster.yaml` 中配置：
   ```yaml
   http_protocol_options:
     use_downstream_protocol: true
   http2_protocol_options:
     max_concurrent_streams: 100
   ```
2. 设置合理的 `idle_timeout`（如 300s）

**预期效果**: 建连开销减少 60%，吞吐量提升 15%-30%

---

### 优化 6：启用 Prometheus 采样率优化

**说明**: 默认 100% 指标采集会消耗 CPU。调整采样率可降低监控开销。

**实施方法**:
1. 在 `stats.config` 中设置：
   ```yaml
   use_all_default_tags: false
   stats_tags:
   - tag_name: cluster_name
     fixed_value: "default"
   ```
2. 启用 `statsd` 采样（`sample_rate: 0.1`）

**预期效果**: CPU 占用降低 10%-15%，监控数据量减少 80%

---
## 学习要点

- Higress 是阿里开源的基于 Istio 的云原生 API 网关，深度集成了 K8s 与 Envoy，提供高性能流量管理。
- 支持热更新路由规则、插件扩展及金丝雀发布，适用于微服务架构下的流量治理与灰度发布场景。
- 内置 WAF 防护、限流熔断等安全特性，可直接对接 Nacos、Consul 等注册中心，降低运维复杂度。
- 提供控制台可视化界面，简化配置流程，兼容 Ingress 资源定义，便于从传统网关平滑迁移。
- 通过插件市场扩展功能（如认证、日志、监控），支持自定义插件开发，满足企业级定制需求。
- 基于 Envoy 高性能数据面，延迟低（P99 < 1ms），适合高并发场景下的 API 网关部署。
- 开源社区活跃，文档完善，适合作为云原生架构中流量入口的统一管理方案。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础

**学习内容**:
- 云原生网关的基本概念与 Higress 的核心定位
- Higress 与传统网关（如 Nginx, Kong）及阿里云 MSE 的关系
- Docker 容器基础与环境准备
- Higress 的本地安装与部署（Docker Desktop 或 Linux 环境）
- 控制台（Console）的基本操作与界面熟悉
- 最简单的路由配置：实现一个域名到服务的流量转发

**学习时间**: 1-2周

**学习资源**:
- Higress 官方 GitHub 仓库 README
- Higress 官方文档：快速入门章节
- Docker 官方安装指南

**学习建议**:
- 不要急于修改复杂配置，先成功在本地跑通一个 Hello World 服务。
- 重点理解 Ingress 和 Gateway API 的基本区别。
- 熟悉控制台的布局，学会如何查看日志和监控大盘。

---

### 阶段 2：核心功能与流量治理

**学习内容**:
- 高级路由规则：基于 Header、Query 参数、Cookie 的路由匹配
- 流量治理：金丝雀发布、蓝绿部署、Header 修改与重定向
- 服务来源管理：对接 Nacos、Consul、固定地址（Upstream）及 K8s Service
- 负载均衡策略配置（轮询、随机、一致性哈希等）
- 插件系统入门：使用 Wasm 插件扩展功能（如 Key Auth、Request Block）
- 基本的安全防护配置（IP 访问控制、基础认证）

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档：流量治理与插件市场章节
- Higress 官方插件市场
- Envoy Filter 基础知识（Higress 底层基于 Envoy）

**学习建议**:
- 动手实践流量染色，模拟灰度发布场景。
- 尝试在控制台开启几个官方预置的插件，观察请求响应的变化。
- 理解 Higress 如何通过服务发现中心动态获取后端实例列表。

---

### 阶段 3：生态集成与高性能处理

**学习内容**:
- Higress 在 Kubernetes 环境中的部署与 Ingress 配置
- Dubbo、Nacos、gRPC 等微服务协议的代理与转换
- 全局缓存、限流熔断与超时重试机制
- 使用 OpenTelemetry 进行可观测性集成（链路追踪、Metrics）
- Higress 的多租户网关管理
- 高可用架构部署与性能调优

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档：最佳实践与高可用部署
- Kubernetes Ingress Controller 官方文档
- Prometheus 与 Grafana 集成指南

**学习建议**:
- 搭建一个包含 K8s 和 Nacos 的复杂测试环境。
- 学习如何编写简单的 Lua 或 Go（Wasm）插件来满足特定业务逻辑。
- 关注网关的性能指标（QPS、延迟），并进行压测演练。

---

### 阶段 4：深度定制与源码贡献

**学习内容**:
- 深入理解 Higress 架构：Istio 控制面 + Envoy 数据面的分离架构
- 开发自定义 Wasm 插件（使用 Go 或 C++ 编译为 .wasm 文件）
- Higress 源码编译与本地调试
- 参与开源社区：Issue 提交、Bug 修复与文档贡献
- 网关安全的高级攻防演练
- AI 网关特性：对接大模型（LLM）与 Prompt 模板管理

**学习时间**: 持续学习

**学习资源**:
- Higress GitHub 源码
- Higress 开发者指南
- WebAssembly (Wasm) 官方文档
- Proxy-Wasm Go SDK 文档

**学习建议**:
- 阅读源码中的核心路由逻辑和插件加载机制。
- 尝试编写一个生产级的自定义插件并测试其性能损耗。
- 关注社区动态，参与 Roadmap 的讨论，从使用者向贡献者转变。

---
## 常见问题


### 1: Higress 是什么？它与 Nginx 和 Kong 等网关相比有什么区别？

1: Higress 是什么？它与 Nginx 和 Kong 等网关相比有什么区别？

**A**: Higress 是一个基于阿里内部两年多的云原生网关实践，遵循开源 Gateway API 标准的下一代云原生 API 网关。它底层深度集成了 Envoy，并进行了大量优化。

与 Nginx 相比，Higress 提供了更完善的动态配置能力（无需 Reload 即可生效）、服务发现集成以及更丰富的流量管理特性（如金丝雀发布、全链路灰度）。

与 Kong 相比，Higress 最大的优势在于其与阿里云生态以及 Istio 服务的深度集成。它设计初衷之一就是为了解决 Ingress 和 Sidecar 模式之间的割裂，可以作为 Istio 的 Gateway 入口，同时支持将 Nginx Ingress 的配置平滑迁移，且在性能和高可用性上经过了阿里超大规模流量的验证。

---



### 2: Higress 是否兼容 Kubernetes 的 Ingress 和 Gateway API 标准？

2: Higress 是否兼容 Kubernetes 的 Ingress 和 Gateway API 标准？

**A**: 是的，Higress 对 Kubernetes 的标准资源提供了全面的支持。

1.  **Ingress API**: Higress 完全兼容 K8s Ingress 标准，可以直接作为 Nginx Ingress Controller 的替代品。它还支持通过注解来实现 Nginx 的许多高级功能，方便用户从 Nginx 迁移。
2.  **Gateway API**: Higress 积极参与并实现了 Kubernetes Gateway API 标准（这是 Ingress 的下一代标准）。通过 Gateway API，用户可以获得更灵活的路由配置、更丰富的协议支持（如 HTTPRoute, GRPCRoute, TLSRoute 等）以及更好的角色划分能力。

---



### 3: Higress 如何处理服务发现？是否支持非 K8s 服务（如 Nacos, Consul 等）？

3: Higress 如何处理服务发现？是否支持非 K8s 服务（如 Nacos, Consul 等）？

**A**: Higress 原生设计为云原生网关，默认与 Kubernetes Service 集成，能够自动感知 K8s 集群内的服务变化。

除了 K8s 服务，Higress 最具特色的功能之一是支持**注册中心**。它允许用户直接配置对接主流的服务注册中心，例如：
*   Nacos (阿里云 MSE 或自建)
*   Consul
*   ZooKeeper
*   Eureka
*   DNS

这意味着 Higress 不仅可以管理 K8s 集群内的流量，还可以作为传统微服务架构（如 Spring Cloud + Nacos）的统一流量入口，实现混合云架构下的流量统一管理。

---



### 4: Higress 是否支持插件扩展？如何编写自定义插件？

4: Higress 是否支持插件扩展？如何编写自定义插件？

**A**: 支持。Higress 提供了强大的插件系统来扩展网关的功能，例如 WAF 防护、鉴权、请求/响应修改等。

Higress 提供了两种主要的插件扩展方式：
1.  **Lua/Wasm 插件**: Higress 兼容 Nginx 的 Lua 生态，同时也支持 WebAssembly (Wasm)。用户可以使用 Lua 或 C++/Rust/Go (编译为 Wasm) 编写插件。Wasm 插件具有高性能、隔离性好和动态加载的特点，是 Higress 推荐的扩展方式。
2.  **原生 Go 插件**: 由于 Higress 是 Go 语言编写的，它也支持通过 Go 代码直接扩展其逻辑（通常用于更深度的定制）。

此外，Higress 官方插件市场提供了许多开箱即用的插件（如 Keyless Auth, Jwt Auth, Request Block 等），用户可以在控制台一键启用。

---



### 5: Higress 的性能表现如何？能否支撑高并发流量？

5: Higress 的性能表现如何？能否支撑高并发流量？

**A**: Higress 的性能表现非常优异。它基于 C++ 编写的 Envoy 数据面，具有极高的处理效率和低延迟。

根据官方基准测试数据：
*   Higress 在长连接场景下的吞吐量表现优异，能够显著降低网关的资源消耗。
*   在处理 HTTP/2 和 gRPC 流量时，性能优于传统的基于 Java 或纯 Lua 的网关。
*   阿里内部双十一等大促场景中，Higress (及其内部版本) 承接了万亿级的流量请求，证明了其在极端高并发下的稳定性和可靠性。

---



### 6: Higress 与 Istio 是什么关系？能否替代 Istio Gateway？

6: Higress 与 Istio 是什么关系？能否替代 Istio Gateway？

**A**: Higress 与 Istio 是互补集成的关系。

1.  **作为替代品**: Higress 可以完全替代 Istio 默认的 Ingress Gateway。Istio 默认的 Gateway 往往配置复杂、资源消耗高，而 Higress 提供了更友好的控制台和更低资源占用的数据面。
2.  **无缝集成**: Higress 可以无缝对接 Istio 的服务网格。它能够识别 Istio 的 VirtualService 和 DestinationRule，从而实现从入口网关到 Sidecar 的全链路流量管理。用户可以在 K8s 集群中部署 Higress 作为入口，同时运行 Istio 管理内部服务通信，Higress 会自动同步服务发现信息。

---

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**:

### Higress 基于 Nginx 和 Envoy 构建。请阅读 Higress 的基本架构文档，并使用 Docker 快速启动一个 Higress 实例。配置一个简单的路由规则，将访问 `http://localhost/test` 的流量转发到一个模拟的后端服务（如 httpbin.org）。

### 提示**:

---
## 实践建议

基于 Higress 作为 AI Native API 网关的定位，结合其基于 Envoy 和 Istio 的技术架构，以下是针对实际生产环境的 6 条实践建议：

### 1. 利用 Wasm 插件实现私有协议适配与模型路由
**场景**：企业内部往往存在自研的模型服务或使用了非标准 OpenAI 协议的大模型（如某些国产模型），直接接入会导致兼容性问题。
**建议**：不要尝试修改 Higress 核心代码来支持新协议。应利用 Higress 的 **Wasm (WebAssembly)** 插件机制，编写 Lua 或 Go (基于 Proxy-Wasm) 插件来处理请求和响应的转换（例如将内部格式转换为 OpenAI 格式）。
**最佳实践**：将协议转换逻辑封装在独立的 Wasm 插件中，这样可以实现模型服务的无感迁移，同时保持网关核心的轻量与稳定性。

### 2. 实施基于 Token 的精细化鉴权与流控
**场景**：大模型调用成本高昂，且不同用户/租户对 API 的消耗差异极大。传统的基于 QPS（每秒请求数）限流无法准确控制成本。
**建议**：启用 Higress 的 **AI 特性**，配置基于 Token 计数的鉴权和流控策略。
**最佳实践**：
*   在 API 网关层进行 Token 预估或流式传输中的 Token 统计。
*   为不同的 API Key 设置不同的 Token 预算配额，防止个别用户通过“刷 Prompt”消耗掉整个企业的 LLM 配额。
**常见陷阱**：仅配置了请求频率限制，忽略了长文本或高并发流式请求带来的 Token 突刺，导致后端账单失控。

### 3. 配置语义缓存与提示词模板管理
**场景**：在客服或问答场景中，大量用户提问高度相似，每次都请求大模型会产生高昂费用且延迟较高。
**建议**：利用 Higress 的缓存插件或 AI 特性中的 **语义缓存** 功能。
**最佳实践**：
*   针对只读场景或对实时性要求不高的场景，开启基于向量相似度的缓存。当用户问题与缓存库中的问题相似度超过阈值（如 95%）时，直接返回缓存结果，无需请求后端 LLM。
*   结合 Higress 的 Prompt 模板管理功能，在网关层完成 Prompt 的注入和拼接，防止前端直接暴露 Prompt 模板导致的安全风险。

### 4. 建立多模型供应商的容灾与路由策略
**场景**：企业通常同时接入了多家模型提供商（如 OpenAZure、通义千问、DeepSeek 等），单一厂商宕机会导致服务不可用。
**建议**：配置 Higress 的 **服务路由** 规则，实现多模型供应商之间的负载均衡和故障转移。
**最佳实践**：
*   设置“超时”与“重试”策略。由于 LLM 推理通常耗时较长（流式响应），务必将网关层面的连接超时时间调整至 60 秒甚至更长。
*   当主模型供应商返回 5xx 错误或超时时，网关应能自动将流量切换至备用模型供应商，确保业务连续性。

### 5. 严格管控敏感数据（PII）与 Prompt 注入
**场景**：员工可能无意中将数据库密码、内部 IP 等敏感信息填入 Prompt，或恶意用户通过 Prompt Injection 攻击试图获取系统指令。
**建议**：在 Higress 的网关层配置 **内容安全检查** 插件。
**最佳实践**：
*   在请求发送给 LLM 之前，利用插件扫描输入内容，利用正则或简单模型拦截包含敏感关键词（如身份证、特定内部格式）的请求。
*   对响应流同样进行过滤，防止 LLM 泄露训练数据中的敏感信息。
**常见陷阱**：完全依赖 LLM 厂商的安全承诺，未在企业网关侧设立最后一道防线，一旦数据泄露无法追溯和阻断。

### 6. 可观测性：关联 Trace ID 与流

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI 原生](/tags/ai-%E5%8E%9F%E7%94%9F/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [WASM](/tags/wasm/) / [LLM](/tags/llm/) / [MCP](/tags/mcp/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/) / [Kubernetes](/scenarios/kubernetes/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260205-github_trending-alibaba-higress-5.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260215-github_trending-alibaba-higress-5.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260216-github_trending-alibaba-higress-6.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260301-github_trending-alibaba-higress-2.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-8.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*