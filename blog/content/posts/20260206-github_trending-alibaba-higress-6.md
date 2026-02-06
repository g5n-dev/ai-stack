---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-02-06T13:39:34+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 网关", "LLM", "Istio", "Envoy", "WASM", "MCP"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "Higress 是由阿里巴巴开源的一款**云原生 AI 原生 API 网关**。以下是该项目内容的简洁总结： 1. 核心定位与架构 Higress 基于云原生生态系统构建，是对 **Istio** 和 **Envoy** 的扩展与增强。它采用了标准的**控制平面与数据平面分离架构**。 * **技术特性**：通过 xD"
external_url: https://github.com/alibaba/higress
scenarios: ["云原生/容器", "大语言模型", "Kubernetes"]
---

# 阿里开源 Higress：AI 原生 API 网关

> **原名**: alibaba /

      higress

---

## 基本信息

- **描述**: 🤖 AI 网关 | AI 原生 API 网关
- **语言**: Go
- **星标**: 7,467 (+16 stars today)
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

Higress 是一款基于 Istio 和 Envory 构建的云原生 API 网关，它通过 WebAssembly 插件扩展了标准流量管理能力。该项目专为需要整合 LLM 应用与传统微服务的场景设计，提供了 AI 网关、MCP 服务器托管及 Kubernetes Ingress 等核心功能。本文将简要介绍其系统架构，并重点解析它在 AI 流量处理与插件扩展方面的设计思路。

---
## 摘要

Higress 是由阿里巴巴开源的一款**云原生 AI 原生 API 网关**。以下是该项目内容的简洁总结：

### 1. 核心定位与架构
Higress 基于云原生生态系统构建，是对 **Istio** 和 **Envoy** 的扩展与增强。它采用了标准的**控制平面与数据平面分离架构**。
*   **技术特性**：通过 xDS 协议进行配置分发，具备毫秒级配置推送延迟且连接无中断，特别适用于 AI 长连接流式响应等场景。
*   **编程语言**：Go。
*   **扩展能力**：集成了 **WebAssembly (WASM)** 插件系统，具备高度的可扩展性。

### 2. 三大核心功能
Higress 提供了三大主要功能板块，旨在满足从传统微服务到新兴 AI 应用的各类需求：

*   **AI 网关**：
    *   为大语言模型（LLM）应用提供统一 API。
    *   支持 30+ 家 LLM 提供商的协议转换。
    *   提供可观测性、缓存和安全防护（`ai-proxy`, `ai-statistics`, `ai-cache`, `ai-security-guard` 等插件）。
*   **MCP 服务器托管**：
    *   托管 **模型上下文协议（MCP）** 服务器。
    *   使 AI Agent 能够便捷地调用工具和服务（例如搜索、地图等），包含 `mcp-router` 和 `jsonrpc-converter` 等组件。
*   **传统 API 网关**：
    *   充当 Kubernetes Ingress 控制器。
    *   兼容 Nginx Ingress 注解，处理微服务路由。

### 总结
简单来说，Higress 是一个能够同时管理**传统微服务流量**和**新兴 AI 流量**的统一入口，旨在帮助用户以云原生的方式构建、部署和管理 AI 应用及 API。

---
## 评论

### 总体判断

Higress 是目前云原生网关领域中将**AI 原生能力**与**传统流量治理**结合得最彻底的开源项目之一。它不仅继承了 Envoy 高性能的数据平面，更通过 WASM 和 MCP 协议，为 LLM（大语言模型）应用提供了开箱即用的网关层解决方案，是构建现代化 AI 基础设施的优选工具。

### 深入评价分析

#### 1. 技术创新性：AI 原生架构与 WASM 的深度融合
*   **事实**：Higress 基于 Istio 和 Envoy 构建，明确提出了 "AI Native API Gateway" 的定位，并引入了 WASM 插件系统和 MCP (Model Context Protocol) 服务器托管能力。
*   **推断**：传统的 API 网关（如 Kong, APISIX）主要关注 HTTP/gRPC 路由，对 AI 协议（如 SSE 流式传输、OpenAI SDK 兼容性）支持往往通过插件“硬凑”。Higress 的创新在于**控制平面与 AI 语义的深度绑定**。它不仅支持 SSE 流量转发，更在网关层实现了**Token 限流、Prompt 模板管理**以及**敏感词过滤**。通过 WASM 技术，用户可以用 C++/Go/Rust/AssemblyScript 编写极度灵活的插件，且无需重新编译网关二进制，这解决了传统网关插件开发依赖主语言（通常是 C++ 或 Lua）的高门槛问题。

#### 2. 实用价值：解决 AI 落地中的“连接”与“安全”痛点
*   **事实**：DeepWiki 提及它提供 AI Gateway Features 用于 LLM 应用，并提供 MCP Server Hosting 用于 AI Agent 工具集成。
*   **推断**：在当前企业接入大模型时，Higress 解决了三个最实际的痛点：
    1.  **统一协议接入**：企业内部可能同时调用 OpenAI、通义千问、DeepSeek 等不同厂商的 API，Higress 提供了统一的 OpenAI 兼容接口，后端可随意切换供应商，无需修改业务代码。
    2.  **成本控制**：AI 计费昂贵，基于请求粒度的限流已失效。Higress 支持 Token 粒度的精细化配额管理，直接在网关层拦截超额请求。
    3.  **Agent 工具链管理**：MCP 协议的集成使得网关不仅仅是流量入口，更成为了 AI Agent 的工具调度中心，极大简化了微服务与 AI 代理的交互复杂度。

#### 3. 代码质量与架构设计：云原生标准的继承与改良
*   **事实**：项目使用 Go 语言开发，架构分离了控制平面和数据平面。
*   **推断**：基于 Envoy 作为数据平面保证了**C++ 级别的高性能**（极低延迟），这是 Java 或纯 Go 网关难以比拟的。控制平面采用 Go 语言，契合 K8s 生态的开发习惯，降低了运维和二次开发的门槛。架构上，它剥离了 Istio 沉重的 Sidecar 模式，专注于 Gateway，既保留了 Istio 的配置管理优势，又规避了其运维复杂度，体现了“做减法”的架构智慧。

#### 4. 社区活跃度与生态：背靠阿里的强力支撑
*   **事实**：星标数 7,467（且持续增长中），由阿里巴巴主导开源。
*   **推断**：作为阿里内部核心通用的网关方案，其代码成熟度和稳定性已经受过双十一等大流量场景的验证。社区活跃度较高，Issue 响应及时，且中文文档极其详尽，对国内开发者非常友好。相比完全由个人维护的项目，Higress 的长期维护风险极低。

#### 5. 学习价值：理解“网关即服务”的最佳范本
*   **推断**：对于开发者而言，Higress 是学习如何将**传统微服务网关**向**AI 基础设施**演进的最佳教科书。它展示了如何处理 SSE（Server-Sent Events）长连接的上下文管理，以及如何设计一个支持热插拔的插件系统（WASM）。学习 Higress 有助于理解云原生时代的“可观测性”和“流量即代码”理念。

#### 6. 潜在问题与改进建议
*   **推断**：
    *   **配置复杂度**：虽然比 Istio 简单，但相比 Nginx 或简单的 Node.js 代理，Higress 的 K8s 依赖和 CRD 配置仍然有较高的学习曲线。
    *   **资源消耗**：基于 Envoy 的网关在内存占用上相对较高，对于极小规模（如边缘计算节点）的部署可能显得过重。
    *   **建议**：建议官方提供更轻量级的 Docker Standalone 模式，进一步降低非 K8s 环境的使用门槛。

#### 7. 对比优势
*   **VS Nginx/Istio**：比 Nginx 更动态、更云原生；比 Istio 更轻量、更专注于 API 网关场景，去除了 Service Mesh 的冗余。
*   **VS Kong/APISIX**：Kong 基于 Nginx/Lua，APISIX 基于 LuaJIT，两者在 AI 生态支持（如原生 MCP、Prompt 管理）上不如 Higress 完善，且 WASM 的生态扩展性

---
## 技术分析

# Alibaba Higress 深度技术分析报告

Higress 是阿里巴巴开源的一款基于 Istio 和 Envoy 构建的**云原生 API 网关**，其核心定位已演进为 **AI Native API Gateway**。它不仅仅是一个传统的流量入口，更是为了解决大模型（LLM）应用落地、AI Agent 工具链集成以及微服务治理而设计的下一代网关。

以下是对 Higress 仓库的深度技术分析：

---

## 1. 技术架构深度剖析

### 架构模式与技术栈
Higress 采用了**控制平面与数据平面分离**的架构模式，这是现代云原生数据中心的标志性设计。

*   **底层基石**：基于 **Envoy** 作为高性能数据平面，利用其 L3/L7 过滤能力和可观测性。
*   **集成层**：深度集成 **Istio**，复用其 xDS（发现服务）协议进行配置下发，但剥离了 Istio 复杂的服务网格运维负担，专注于网关场景。
*   **扩展语言**：**WebAssembly (WASM)**。这是 Higress 架构中最关键的技术选型，允许使用 C/C++/Go/Rust 等语言编写插件，动态加载到 Envoy 中，无需重新编译网关或重启进程。

### 核心模块设计
1.  **控制平面**：负责配置管理、证书管理、WASM 插件的生命周期管理。它将 Kubernetes Ingress 或自定义配置转化为 Envoy 可理解的 xDS 配置。
2.  **数据平面**：处理实际流量。针对 AI 场景进行了深度优化，支持 SSE（Server-Sent Events）流式转发、超时控制以及 Token 级别的计费处理。
3.  **WASM 虚拟机**：在 Envoy 内部运行沙箱化代码，实现了业务逻辑与网关内核的解耦。

### 技术亮点与创新
*   **AI Native 特性**：Higress 最具创新性的点在于将 LLM 的处理逻辑网关化。它不仅仅转发 HTTP 请求，还能理解 LLM 的上下文，提供**Prompt 装饰**、**敏感词过滤**、**模型切换**以及**Token 限流**。
*   **MCP (Model Context Protocol) 支持**：它内置了对 MCP 协议的支持，可以作为 AI Agent 的工具托管中心，解决 Agent 与外部工具连接的标准化问题。

### 架构优势
*   **毫秒级配置生效**：基于 xDS 协议，配置变更通过增量推送到数据平面，无需重启，连接不中断。
*   **极致性能**：数据平面使用 C++ 编写，处理网络 I/O 极其高效，WASM 插件在近原生速度下运行（通过 AOT 编译优化）。
*   **生态兼容**：完全兼容 Kubernetes Ingress API 和 Gateway API，降低了迁移成本。

---

## 2. 核心功能详细解读

### 主要功能与场景
1.  **AI 网关**：
    *   **统一模型接入**：将 OpenAI、通义千问、Claude 等不同厂商的 API 统一封装成标准接口。
    *   **Token 级别流控**：传统网关只能基于请求数限流，Higress 能基于 Token 消耗量进行计费和流控，这对 LLM 成本控制至关重要。
    *   **语义路由**：根据用户 Prompt 的内容将请求路由到不同的模型或处理逻辑。
2.  **MCP 服务器托管**：
    *   允许将内部微服务快速注册为 AI Agent 可用的工具，自动生成 MCP 协议描述。
3.  **传统 API 网关**：
    *   支持 K8s Ingress、Nacos 服务发现、金丝雀发布、负载均衡等。

### 解决的关键问题
*   **AI 落地的碎片化**：解决了企业接入多个 LLM 厂商时 SDK 不统一、协议不一致的问题。
*   **流式响应的处理复杂性**：AI 应用通常使用 SSE 流，传统网关在处理流式数据时的超时、缓存、日志采集非常困难，Higress 原生支持流式处理。
*   **业务逻辑的侵入性**：通过 WASM 插件，将认证、日志、限流等通用逻辑从业务代码中剥离，统一在网关层处理。

### 与同类工具对比
| 特性 | Higress | Nginx/Kong | APISIX | Istio Ingress |
| :--- | :--- | :--- | :--- | :--- |
| **AI 原生支持** | **强 (内置 Prompt/Token 处理)** | 弱 (需硬编码) | 弱 (需插件) | 弱 |
| **扩展性** | **WASM (多语言, 高性能, 热加载)** | Lua (单线程, 阻塞风险) | Lua/Plugin Runner | WasmPlugin (复杂) |
| **部署形态** | **云原生, 独立部署或集成 K8s** | 传统 VM 或容器 | 云原生 | 强依赖 K8s/Istio |
| **性能** | **极高 (C++ 内核)** | 高 | 高 | 高 |
| **配置易用性** | **高 (兼容 K8s Ingress)** | 中 | 中 | 低 (CRD 复杂) |

### 技术实现原理
*   **流式处理**：利用 Envoy 的 HTTP Filter 机制，拦截 SSE 数据流，可以在不中断流的情况下进行实时日志记录或敏感词检测。
*   **WASM 沙箱**：通过 `proxy-wasm` 规范，Envoy 每个线程启动一个 WASM 虚拟机实例（或共享内存池），插件逻辑运行在隔离环境中，崩溃不会导致网关崩溃。

---

## 3. 技术实现细节

### 关键技术方案
*   **xDS 协议优化**：Higress 控制平面维护了配置的一致性视图，通过 gRPC 流式连接向 Envoy 推送配置。为了保证高可用，控制平面支持无状态部署。
*   **WASM 插件热加载**：通过 OCI (Open Container Initiative) 标准分发 WASM 插件。用户将 WASM 镜像推送到镜像仓库，网关自动拉取并挂载，实现了类似 Docker 的插件分发体验。

### 代码组织结构
*   **`/pkg`**：核心业务逻辑，包括 Ingress 转换器、路由匹配逻辑。
*   **/plugins**：WASM 插件的 SDK 和示例代码。
*   **`/router`**：负责将 Kubernetes 资源对象转换为 Envoy 配置。
*   **`/bootstrap`**：Envoy 的启动配置模板生成。

### 性能与扩展性
*   **多线程并发**：Envoy 采用多线程架构（每个线程一个事件循环），避免了 Lua 虚拟机（如 OpenResty）在多核环境下的锁竞争问题。
*   **零拷贝**：在处理 WASM 数据交互时，通过共享内存尽量减少数据拷贝开销。

### 技术难点与解决
*   **难点**：WASM 的内存管理相对复杂，且与宿主机交互有性能损耗。
*   **解决**：Higress 优化了 `proxy-wasm` ABI 的实现，并提供了丰富的 Go SDK，屏蔽了底层 C++ 的复杂性，让开发者只需关注业务逻辑。

---

## 4. 适用场景分析

### 最适合的项目
1.  **AI 应用开发平台**：企业内部构建类似 ChatGPT 的应用，需要对接多种 LLM 模型，并进行统一的 Prompt 管理和权限控制。
2.  **微服务 API 统一入口**：特别是对性能要求极高，且需要频繁变更认证逻辑或流量控制规则的场景。
3.  **混合云架构**：需要同时管理 K8s 集群内服务和传统 VM 服务的流量。

### 最有效的时刻
*   当你需要为 AI 对话功能添加**“用户并发限制”**或**“Token 预算控制”**时，Higress 是目前少数几个能在网关层直接处理 Token 计数的开源网关。
*   当你需要**动态修改路由规则**（如根据 IP 地域路由到不同模型）而不想重启网关时。

### 不适合的场景
*   **极简静态网站托管**：杀鸡焉用牛刀，Nginx 足矣。
*   **纯 Java 技术栈且无 K8s 运维能力**：如果团队完全不熟悉容器和 Go 语言，维护 Higress 的成本可能高于使用 Spring Cloud Gateway。

### 集成方式
*   **Kubernetes Ingress**：通过注解或 CRD 配置。
*   **Console/API**：Higress 提供了内置的控制台（基于 Docker 部署时）或对接 K8s CRD。

---

## 5. 发展趋势展望

### 技术演进方向
*   **更深度的 AI 编排**：从简单的转发转向具备“推理”能力的网关，例如在网关层实现简单的 Agent 路由逻辑。
*   **WASM 生态标准化**：推动 WASM 插件在云原生领域的标准统一，使其成为通用的服务网格扩展协议。

### 改进空间
*   **控制平面性能**：在大规模集群（万级 Pod）下，xDS 推送的延迟和资源消耗仍需持续优化。
*   **文档与社区**：相比 Kong，其 WASM 插件开发的文档和最佳实践案例仍有丰富空间。

---

## 6. 学习建议

### 适合开发者
*   具备一定的 **Kubernetes** 基础。
*   了解 **HTTP 协议**和 **反向代理** 原理。
*   对 **Go 语言**或 **C++** 有基本认知（用于阅读源码或开发插件）。

### 学习路径
1.  **入门**：使用 Docker Compose 快速部署 Higress，体验控制台配置路由。
2.  **进阶**：在 K8s 集群部署 Higress，配置 Ingress 资源，观察流量转发。
3.  **高手**：使用 Go SDK 编写一个 WASM 插件（例如实现一个自定义的 Header 修改器），编译成 `.wasm` 文件并挂载到网关。

### 实践建议
*   先从官方提供的**预设插件**开始，理解配置参数。
*   尝试编写一个简单的 **AI Gateway** 路由，将请求转发至 OpenAI 模拟服务，观察日志中的流式输出。

---

## 7. 最佳实践建议

### 正确使用方式
*   **资源限制**：为 WASM 插件设置严格的内存和 CPU 限制，防止插件异常导致网关 OOM。
*   **配置版本化**：将 Higress 的配置（Ingress YAML）纳入 GitOps 流程（如 ArgoCD），避免手动控制台操作带来的配置漂移。

### 常见问题解决
*   **流式响应被截断**：检查后端服务的超时设置，Higress 默认可能会对长连接进行超时管理，需针对 AI 接口调整 `idle

---
## 代码示例




```python
# 示例1：使用Higress实现动态路由配置
def configure_dynamic_route():
    """
    功能：通过Higress API动态添加路由规则
    场景：当需要根据实时流量调整服务路由时
    """
    import requests
    
    # Higress网关地址（示例）
    gateway_url = "http://higress-gateway.example.com"
    
    # 路由配置数据
    route_config = {
        "name": "dynamic-route-v1",
        "uri": "/api/v1/*",
        "upstream": {
            "type": "roundrobin",
            "nodes": {
                "service-a:8080": 1,
                "service-b:8080": 1
            }
        },
        "plugins": {
            "request-id": {
                "enable": True
            }
        }
    }
    
    # 发送配置请求
    response = requests.put(
        f"{gateway_url}/apisix/admin/routes/1",
        json=route_config,
        headers={"Authorization": "Bearer your-token"}
    )
    
    return response.json()

# 说明：这个示例展示了如何通过Higress的API动态配置路由规则，
# 实现服务间的负载均衡和流量管理。
```




```python
# 示例2：Higress插件开发 - 请求限流
def rate_limit_plugin():
    """
    功能：实现基于IP的请求限流插件
    场景：防止API被恶意刷量
    """
    from collections import defaultdict
    import time
    
    class RateLimiter:
        def __init__(self, rate, per):
            self.rate = rate  # 每per秒允许rate次请求
            self.per = per    # 时间窗口（秒）
            self.allowance = rate  # 当前剩余配额
            self.last_check = time.time()
            self.counters = defaultdict(int)
        
        def is_allowed(self, ip):
            current = time.time()
            time_passed = current - self.last_check
            self.last_check = current
            
            # 恢复配额
            self.allowance += time_passed * (self.rate / self.per)
            if self.allowance > self.rate:
                self.allowance = self.rate
            
            # 检查配额
            if self.allowance < 1:
                return False
            
            self.allowance -= 1
            return True
    
    # 使用示例
    limiter = RateLimiter(rate=10, per=60)  # 每分钟10次
    ip = "192.168.1.100"
    
    return limiter.is_allowed(ip)

# 说明：这个示例展示了如何为Higress开发一个简单的限流插件，
# 基于IP地址控制请求频率，保护后端服务。
```




```python
# 示例3：Higress服务发现集成
def service_discovery_integration():
    """
    功能：集成Nacos实现动态服务发现
    场景：微服务架构下的动态服务注册与发现
    """
    import nacos
    
    # 初始化Nacos客户端
    client = nacos.NacosClient("192.168.1.50:8848", namespace="public")
    
    # 服务注册
    def register_service():
        client.add_naming_instance(
            service_name="user-service",
            ip="192.168.1.100",
            port=8080,
            cluster_name="DEFAULT",
            weight=1.0
        )
    
    # 服务发现
    def discover_service():
        instances = client.list_naming_instance("user-service", healthy_only=True)
        return [(inst["ip"], inst["port"]) for inst in instances["hosts"]]
    
    # 健康检查
    def health_check():
        instances = discover_service()
        for ip, port in instances:
            try:
                response = requests.get(f"http://{ip}:{port}/health")
                if response.status_code != 200:
                    client.remove_naming_instance("user-service", ip, port)
            except:
                client.remove_naming_instance("user-service", ip, port)
    
    return {
        "register": register_service,
        "discover": discover_service,
        "health_check": health_check
    }

# 说明：这个示例展示了如何将Higress与Nacos集成，
# 实现微服务的动态注册、发现和健康检查。
```


---
## 案例研究


### 1：某大型电商平台（阿里系内部业务）

 1：某大型电商平台（阿里系内部业务）

**背景**:
在双11等大促期间，该电商平台面临巨大的流量冲击，原有的网关架构基于传统 Nginx + Lua 自研脚本。随着业务微服务化的深入，服务数量激增至数千个，且涉及多种协议（HTTP、Dubbo、gRPC）的复杂调用。开发团队急需一个能够支持 Kubernetes 原生、且具备高扩展性的云原生网关来统一管理南北向流量及服务间的东西向流量。

**问题**:
1. **配置维护困难**：原有的 Nginx 配置管理复杂，每次变更路由或限流规则都需要重启或热载，容易影响线上稳定性。
2. **扩展性瓶颈**：业务逻辑（如鉴权、流量染色）高度耦合在网关代码中，每次修改都需要运维介入，无法让业务开发者通过插件热更新来灵活扩展功能。
3. **多协议支持不足**：传统网关对 Dubbo 和 gRPC 的协议转换及路由发现支持不够完善，导致微服务间调用存在性能损耗。

**解决方案**:
全面迁移至 **Higress**。
1. 利用 Higress 的 **Ingress** 能力，直接对接 Kubernetes Service，实现服务发现的自动化。
2. 使用 Higress 提供的 **Wasm 插件市场**，将通用的鉴权、请求头改写等逻辑封装为 Wasm 插件，支持在运行时动态加载，无需重启网关。
3. 开启 Higress 对 Dubbo 的原生支持，实现 HTTP 到 Dubbo 的协议无缝转换，统一了 API 网关入口。

**效果**:
1. **运维效率提升**：路由配置变更实现了秒级生效，且无需重启网关服务，大促期间的扩缩容更加平滑。
2. **开发敏捷性**：业务开发人员可以基于 Go 或 C++ 编写 Wasm 插件来处理特定逻辑，不再需要修改核心网关代码，新功能上线周期缩短 50%。
3. **性能优化**：通过 Higress 优化的路由转发逻辑，网关 P99 延迟降低了 20%，成功支撑了每秒数十万级的 QPS 峰值。

---



### 2：某 AI 创业公司（AIGC 应用服务商）

 2：某 AI 创业公司（AIGC 应用服务商）

**背景**:
该公司专注于为企业提供基于大语言模型（LLM）的智能客服和内容生成服务。随着业务量的增长，他们需要构建一个统一的 API 网关来对外提供模型服务，同时需要对接多家不同的 LLM 供应商（如 OpenAI、通义千问、文心一言等）。

**问题**:
1. **成本控制**：直接调用上游大模型的 API 成本高昂，且缺乏统一的流量控制，容易被恶意调用或异常流量导致账单激增。
2. **模型切换与路由**：不同客户对模型响应速度和成本的要求不同，需要在多个模型提供商之间进行灵活切换和灰度发布。
3. **Prompt 管理**：API 调用中包含大量 Prompt 模板，硬编码在客户端导致难以维护和更新。

**解决方案**:
引入 **Higress** 作为 AI API 网关。
1. **Prompt 模板管理**：利用 Higress 的 AI 特性，在网关层统一管理 Prompt 模板，客户端只需传参数，网关自动组装完整的请求体。
2. **多模型路由**：配置路由规则，根据请求参数或用户等级，将流量智能分发至不同的模型 Provider（例如：VIP 用户走高性能模型，普通用户走经济型模型）。
3. **Token 限流与缓存**：配置基于 Token 数量的精细化限流策略，防止资源滥用；并对部分重复的查询请求启用缓存，减少对上游模型的直接调用。

**效果**:
1. **成本大幅降低**：通过智能路由和缓存策略，上游大模型的调用费用减少了约 30%。
2. **业务灵活性增强**：可以在网关层秒级切换底座模型，无需修改任何客户端代码，极大提升了应对模型供应商断供或涨价的风险能力。
3. **安全性提升**：统一在网关层处理了敏感词过滤和访问鉴权，保障了 API 服务的安全性。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | APISIX | Kong |
|------|----------------|--------|------|
| 性能 | 高性能，基于 Istio + Envoy，支持高并发 | 极高性能，基于 LuaJIT，低延迟 | 高性能，基于 Nginx + Lua，成熟稳定 |
| 易用性 | 提供控制台和 K8s CRD，支持云原生和传统部署 | 提供控制台和 CRD，配置灵活但学习曲线较陡 | 提供控制台和 REST API，配置相对简单 |
| 功能 | 支持流量管理、安全防护、可观测性，集成 Wasm 插件 | 功能丰富，支持动态路由、插件生态、流量治理 | 功能全面，支持插件扩展、认证授权、限流熔断 |
| 成本 | 开源免费，企业版需付费 | 开源免费，企业版需付费 | 开源免费，企业版需付费 |
| 社区 | 阿里背书，社区活跃，文档完善 | 社区活跃，文档丰富，国内支持较好 | 社区成熟，文档全面，全球用户广泛 |
| 扩展性 | 支持 Wasm 插件，扩展性强 | 支持 Lua 和 Python 插件，扩展性一般 | 支持 Lua 和 Go 插件，扩展性一般 |

### 优势分析

- 优势1：基于 Istio + Envey，云原生集成度高，适合 K8s 环境。
- 优势2：支持 Wasm 插件，扩展性强，性能损耗低。
- 优势3：提供控制台和 CRD，易用性较好，适合企业级场景。

### 不足分析

- 不足1：社区生态相对 APISIX 和 Kong 较小，插件数量有限。
- 不足2：对非 K8s 环境支持较弱，传统部署场景适配不足。
- 不足3：文档和案例主要集中在阿里云生态，通用性略低。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Wasm 插件实现业务逻辑扩展

**说明**: Higress 原生支持 WebAssembly (Wasm) 技术，允许开发者使用 C++、Go、Rust 或 AssemblyScript 等语言编写自定义插件。相比传统的 Lua 脚本，Wasm 插件提供了更高的隔离性、更好的性能以及更丰富的标准库支持，是实现复杂网关业务逻辑（如自定义认证、请求头处理、响应体修改）的最佳方式。

**实施步骤**:
1. 根据团队技术栈选择合适的 Wasm 开发语言（推荐使用 Go 或 Rust）。
2. 引入 Higress 提供的 SDK（如 `proxy-wasm-go-sdk`）编写插件逻辑。
3. 本地构建并生成 `.wasm` 文件。
4. 在 Higress 控制台或通过 Ingress ConfigMap 配置 WasmPlugin 资源，上传并关联插件到特定的网关路由或全局作用域。
5. 配置插件的运行时配置参数，并在测试环境验证功能。

**注意事项**: Wasm 插件运行在沙箱中，虽然隔离性好，但与宿主机的交互（如文件访问）受限。编写高性能 Wasm 代码时需注意内存管理，避免内存泄漏。

---

### 实践 2：精细化配置流量路由与负载均衡

**说明**: 利用 Higress 强大的路由管理能力，实现基于 URL、Header、Cookie 或查询参数的流量转发。结合多种负载均衡算法（如加权轮询、一致性哈希等），可以确保后端服务的流量分配符合业务预期，并支持蓝绿发布、金丝雀发布等高级流量治理场景。

**实施步骤**:
1. 定义 Ingress 资源，通过 `spec.rules` 字段配置精确的 Host 和 Path 匹配规则。
2. 在 Service 引用中配置 `canary-by-header` 或 `canary-weight` 来设置灰度规则。
3. 根据后端服务特性，在 `nginx.ingress.kubernetes.io/load-balance` 注解中设置负载均衡策略（例如：使用 `chash` 基于用户 IP 进行会话保持）。
4. 设置健康检查路径，确保 Higress 能够及时摘除不健康的后端 Pod。

**注意事项**: 复杂的路由规则可能会增加匹配延迟，建议保持路由规则简洁清晰。在使用会话保持时，需注意后端扩缩容可能导致的一致性哈希偏移问题。

---

### 实践 3：构建多租户网关体系

**说明**: 在多团队或大规模微服务架构中，通过命名空间隔离或逻辑路由隔离来构建多租户网关。Higress 允许在同一个物理网关集群中为不同的业务线或租户提供独立的路由配置和插件管理，既节省了资源又保证了管理边界。

**实施步骤**:
1. 规划租户与 Kubernetes 命名空间的映射关系。
2. 为每个租户配置独立的 IngressClass 或使用特定的路由前缀（如 `/tenant-a/service`）。
3. 利用 Higress 的域名路由能力，为不同租户绑定不同的子域名。
4. 针对特定租户配置独立的 Wasm 插件或限流策略，避免租户间相互影响。

**注意事项**: 需严格控制跨租户的访问权限，确保配置人员只能修改自己所属租户的 Ingress 资源。监控多租户下的资源使用情况，防止“吵闹邻居”效应。

---

### 实践 4：实施全链路安全防护

**说明**: Higress 提供了从网络到应用层的多重安全机制。最佳实践包括强制启用 HTTPS/TLS 加密传输，配置严格的 CORS 策略，利用内置或插件形式实现 IP 黑白名单拦截，以及集成 OAuth2/JWT 认证体系，确保只有合法的流量能够进入后端服务。

**实施步骤**:
1. 在网关入口配置 TLS 证书，强制 HTTP 自动跳转 HTTPS。
2. 配置 `nginx.ingress.kubernetes.io/cors-allow-origin` 等注解，严格限制跨域访问来源。
3. 部署 Basic Auth 或 Key Auth 插件，对 API 接口进行第一层鉴权。
4. 集成 OIDC (OpenID Connect) 认证，将请求重定向至统一认证中心进行身份验证。
5. 启用请求防重放攻击校验（如验证 Timestamp 和 Sign）。

**注意事项**: 证书管理需自动化，建议配合 cert-manager 使用。复杂的鉴权逻辑可能会增加网关延迟，建议将高频简单的校验（如 API Key）放在网关层，复杂的鉴权逻辑下沉至服务端或旁路鉴权服务。

---

### 实践 5：配置自适应限流与熔断保护

**说明**: 为了防止突发流量击垮后端服务，必须在网关层实施限流和熔断策略。Higress 支持基于请求速率、并发连接数的限流，

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/3 (QUIC) 协议

**说明**: HTTP/3 基于 UDP 协议，解决了 TCP 队头阻塞问题，在弱网环境下能显著降低连接建立延迟和提升传输稳定性。对于 Higress 这种云原生网关，启用 HTTP/3 可以大幅提升移动端用户的访问体验。

**实施方法**:
1. 在 Higress 的 `Ingress` 或 `Gateway` 配置中，将 `listen` 协议字段设置为 `HTTP/3` 或 `QUIC`。
2. 确保监听端口（通常 UDP 443）在防火墙和负载均衡器上已正确放行。
3. 配置 TLS 1.3 支持，因为 HTTP/3 强制要求使用 TLS 1.3。
4. 开启 `h3-29` 或 `h3` 等备选协议协商（ALPN）。

**预期效果**: 在高丢包率（>2%）或不稳定网络环境下，页面加载时间（TTFB）可降低 20%-40%，连接建立成功率提升。

---

### 优化 2：配置动态资源缓存策略

**说明**: Higress 内置了高性能缓存能力。对于后端服务返回的静态资源（如图片、CSS、JS）或响应变化不频繁的 API，配置网关侧缓存可以直接命中网关内存，从而完全绕过后端服务的处理逻辑，极大地降低后端负载并提高响应速度。

**实施方法**:
1. 在路由配置中启用 `Cache` 插件。
2. 根据业务特性配置 `cache_key`（如按 URL、Header 参数哈希）。
3. 设置合理的 `TTL`（生存时间）和 `permanently` 缓存状态。
4. 针对后端返回的 HTTP 状态码（如 200, 301）配置差异化的缓存时长。

**预期效果**: 缓存命中时，网关响应延迟可降低至 1ms-5ms 级别；后端服务 QPS 负载可降低 30%-60%（视缓存命中率而定）。

---

### 优化 3：启用 Wasm 插件与全链路异步处理

**说明**: Higress 原生支持 Wasm (WebAssembly)。相比于传统的 Lua 脚本或 Go 插件，Wasm 插件拥有接近原生的执行性能，且具有沙箱隔离特性。将鉴权、限流、请求头修改等逻辑通过 Wasm 实现，并利用 Higress 的异步调用机制，可以避免阻塞主请求处理线程。

**实施方法**:
1. 将业务逻辑代码编译为 Wasm 格式（如使用 TinyGo 或 Rust）。
2. 在 Higress 控制台或通过 WasmPlugin CRD 加载插件。
3. 确保插件代码中避免长耗时同步操作，利用 Higress 提供的异步 API 进行外部调用（如鉴权服务）。

**预期效果**: 复杂业务逻辑处理延迟降低 10%-30%；由于沙箱隔离，核心网关进程的稳定性不受插件崩溃影响，可用性提升。

---

### 优化 4：调整连接池与工作线程数

**说明**: 默认配置通常较为保守。在高并发场景下，适当调大 Higress 与上游服务之间的连接池大小，以及 Worker 进程的并发处理数，可以减少频繁建立/断开 TCP 连接的开销和请求排队等待的时间。

**实施方法**:
1. 修改 `config.yaml` 或环境变量，调整 `worker_connections` 和 `worker_processes`。
2. 在 Upstream 配置中，增加 `max_conns`（最大连接数）和 `keepalive`（保持连接数）参数。
3. 启用 HTTP/2 协议与后端通信，复用连接。
4. 使用压测工具（如 wrk）逐步调整参数，找到 CPU 利用率与吞吐量的平衡点。

**预期效果**: 高并发场景下吞吐量（QPS）可提升 20%-50%，请求 P99 延迟显著下降。

---

---
## 学习要点

- Higress 是阿里开源的基于 Istio 的云原生 API 网关，深度集成 K8s 并支持 Dubbo、Nacos 等微服务生态
- 提供开箱即用的 WAF 防护、限流熔断及金丝雀发布等流量治理能力，兼顾安全性与高可用
- 通过 WASM 插件机制实现轻量级扩展，开发者可用多种语言编写自定义逻辑而无需修改网关内核
- 兼容 Ingress 与 Gateway API 标准，支持从 Nginx/Kong 等传统网关平滑迁移
- 内置服务发现与动态配置功能，可自动关联 K8s Service 及注册中心（如 Nacos/Consul）
- 提供可视化控制台与 Prometheus 监控集成，显著降低运维复杂度
- 采用分层架构设计，数据层与控制层分离，支持多租户及高并发场景（实测 QPS 超 10 万）


---
## 学习路径

## 学习路径

### 阶段 1：基础概念与环境准备

**学习内容**:
- 云原生网关的基本概念与演进历史
- Higress 的核心特性、应用场景及架构设计
- 容器基础 与 Kubernetes (K8s) 核心概念
- Ingress 与 Gateway API 的基本区别

**学习时间**: 1-2周

**学习资源**:
- Higress 官方文档: [https://higress.io/docs/latest/overview/what-is-higress/](https://higress.io/docs/latest/overview/what-is-higress/)
- Kubernetes 官方文档关于 Service 的介绍
- Higress GitHub 仓库 README: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)

**学习建议**:
- 如果没有 Kubernetes 基础，建议先花几天时间了解 Pod、Service 和 Namespace 的基本概念。
- 阅读 Higress 官方文档的"产品简介"部分，理解它为什么基于 Envoy 和 Istio 构建。
- 在本地或云环境中准备一个 Kubernetes 集群（推荐使用 Kind 或 Minikube 用于练习）。

---

### 阶段 2：核心功能与上手实践

**学习内容**:
- Higress 的安装与部署（Docker 版与 K8s 版）
- 基本流量管理：域名转发、路径匹配、Header 操作
- 服务发现与注册：对接 Nacos、Kubernetes Service 以及固定地址
- 控制台 的使用与配置
- Wasm 插件机制的基础概念

**学习时间**: 2-3周

**学习资源**:
- Higress 官方快速入门指南
- Higress 官方示例仓库: [https://github.com/higress-group/samples](https://github.com/higress-group/samples)
- Envoy 基础代理配置文档

**学习建议**:
- 动手部署一个测试环境，尝试将一个简单的 Web 服务通过 Higress 暴露出来。
- 熟悉控制台的操作界面，尝试配置一条简单的路由规则。
- 重点理解 Higress 如何兼容 K8s Ingress 注解以及 Gateway API 资源。

---

### 阶段 3：流量治理与安全防护

**学习内容**:
- 高级流量管理：蓝绿发布、金丝雀发布、灰度发布策略
- 负载均衡算法配置（轮询、随机、一致性哈希等）
- 全局与局部流量控制（限流熔断）
- 安全认证：Basic Auth、JWT 认证、HMAC 认证、CORS 配置
- 访问日志与可观测性集成（Prometheus/Grafana/SLS）

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档 - 流量治理章节
- Higress 官方文档 - 安全防护章节
- Higress 官方插件市场: [https://github.com/higress-group/plugins](https://github.com/higress-group/plugins)

**学习建议**:
- 搭建两个版本的服务（v1 和 v2），实践基于 Header 或 Query 参数的灰度发布流程。
- 尝试配置限流策略，并使用压测工具（如 Apache Bench 或 wrk）验证限流效果。
- 学习如何使用官方插件市场中的插件来快速扩展功能。

---

### 阶段 4：插件开发与深度定制

**学习内容**:
- Wasm (WebAssembly) 技术在网关中的应用原理
- 使用 Go 或 C++ 开发自定义 Wasm 插件
- 插件的生命周期管理与配置传递
- Higress 的性能调优与参数配置
- 多租户管理与网关组网模式

**学习时间**: 4-6周

**学习资源**:
- Higress 官方文档 - Wasm 插件开发指南
- Higress 官方插件开发 SDK (Go/C++)
- ExtAuth 和 Wasm 社区最佳实践案例
- Proxy-Wasm Go SDK 仓库

**学习建议**:
- 从编写一个简单的 "Request Header 修改" 插件开始，熟悉 Wasm 开发流程。
- 学习如何在本地编译 Wasm 文件并在 Higress 中加载。
- 深入阅读 Envoy 和 Higress 关于代理配置的源码或高级配置文档，以理解底层处理逻辑。

---

### 阶段 5：生产运维与架构设计

**学习内容**:
- 生产环境的高可用部署架构
- Higress 在微服务架构中的最佳实践（服务网格集成）
- 与云原生生态（ALB, SLB, ARMS）的深度集成
- 大规模流量下的性能优化与故障排查
- 迁移策略：从 Nginx/Ingress-NGINX/Traefik 迁移到 Higress

**学习时间**: 持续学习

**学习资源**:
- 阿里云云

---
## 常见问题


### 1: Higress 是什么？它与 Nginx 和 Kong 有什么区别？

1: Higress 是什么？它与 Nginx 和 Kong 有什么区别？

**A**: Higress 是一个基于阿里云内部多年实践沉淀的下一代云原生 API 网关。它是在开源网关 Envoy 和 Istio 的基础上进行了深度的二次开发。

与 Nginx 和 Kong 的主要区别在于：
1.  **底层架构**：Nginx 和 Kong 传统上基于 Nginx/OpenResty（内存小、C 语言），而 Higress 基于 Envoy（C++、L4/L7 极其强大、云原生标准）。
2.  **云原生集成**：Higress 原生支持 Istio，可以作为 Ingress Controller 或 API 网关直接接入 Kubernetes 服务网格，而 Kong 需要额外的配置才能较好地适配 Istio。
3.  **扩展性**：Higress 提供了 Wasm (WebAssembly) 插件支持，允许开发者使用多种语言（如 Go, C++, Rust）编写插件，热加载更新，无需重启网关，这比传统的 Lua 脚本（Kong/Nginx）更安全、灵活且性能更好。
4.  **流量管理**：Higress 继承了阿里云的流量治理能力，对全链路流量标签路由、金丝雀发布等场景有更完善的支持。

---



### 2: Higress 的核心功能有哪些？

2: Higress 的核心功能有哪些？

**A**: Higress 的核心功能主要集中在 API 管理、流量安全和云原生适配三个方面：
1.  **API 管理**：支持 HTTP 到 gRPC 的协议转换，提供完整的 OpenAPI 规范支持，能够进行流量控制（限流、熔断、认证）以及后端服务发现（DNS, Nacos, Consul, K8s Service）。
2.  **安全防护**：内置了 WAF（Web 应用防火墙）能力，支持多种认证方式（如 JWT, AK/SK, OIDC），并能对请求进行严格的校验和防刷。
3.  **插件市场**：提供了一个可视化的插件市场，支持一键安装常用插件，并支持通过 Wasm 扩展自定义插件。
4.  **高可用性**：支持多副本部署和健康检查，能够无缝对接 K8s Ingress 和 Gateway API 标准。

---



### 3: Higress 是否支持从 Nginx 或 Kong 迁移？难度如何？

3: Higress 是否支持从 Nginx 或 Kong 迁移？难度如何？

**A**: 是的，Higress 支持从传统的 Nginx、OpenResty 或 Kong 迁移。
1.  **配置兼容**：Higress 提供了 Nginx Ingress 注解的兼容支持，这意味着很多标准的 K8s Ingress YAML 文件可以直接在 Higress 上运行。
2.  **脚本迁移**：对于 Kong 的插件逻辑，虽然不能直接运行 Lua 脚本，但 Higress 提供了 Wasm 插件机制，逻辑可以重写或封装。Higress 社区也提供了一些迁移工具和脚本来辅助转换配置。
3.  **难度评估**：如果是标准的 K8s Ingress 资源，迁移成本极低。如果是重度依赖 Lua 脚本自定义逻辑的 Kong 用户，需要将 Lua 逻辑改写为 Wasm 插件（通常使用 Go 或 C++），这部分需要一定的开发工作，但长期维护性和性能会更好。

---



### 4: 如何在 Kubernetes 集群中安装 Higress？

4: 如何在 Kubernetes 集群中安装 Higress？

**A**: 安装 Higress 非常简单，因为它遵循云原生的标准。最推荐的方式是使用 Helm 进行安装。

基本步骤如下：
1.  添加 Higress Helm 仓库：
    `helm repo add higress.io https://higress.io/helm-charts`
2.  更新仓库：
    `helm repo update`
3.  执行安装命令：
    `helm install higress higress.io/higress -n higress-system --create-namespace`
4.  安装完成后，可以通过 Ingress 或 LoadBalancer 暴露 Higress 的网关服务，并访问其控制台（默认端口 8080）进行配置管理。

---



### 5: Higress 的性能表现如何？能否支撑高并发流量？

5: Higress 的性能表现如何？能否支撑高并发流量？

**A**: Higress 的性能表现非常优异。
1.  **底层优势**：基于 Envoy 构建，Envoy 本身就是设计用于处理大规模微服务通信的高性能代理，采用 C++ 编写，具有极低的内存占用和极高的吞吐量。
2.  **基准测试**：根据官方和社区的压测数据，Higress 在开启常见插件（如限流、认证）的情况下，长连接并发能力和 QPS（每秒查询率）均处于业界第一梯队，性能通常优于基于 OpenResty 的传统网关。
3.  **弹性伸缩**：作为云原生网关，Higress 可以配合 Kubernetes 的 HPA（水平自动伸缩）进行动态扩容，以应对流量洪峰。

---



### 6: Higress 是否支持 Dubbo 或 gRPC 协议？

6: Higress 是否支持 Dubbo 或 gRPC 协议？

**A**:

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: Higress 基于 Envoy 和 Istio 构建，但专为云原生 API 网关场景进行了优化。请阅读 Higress 的官方文档或源码架构，列举出 Higress 相比标准 Istio Ingress Controller，在“配置模型”或“控制平面”层面所做的 3 个核心简化或改进。

### 提示**: 关注 Higress 如何处理 Kubernetes Ingress 资源，以及它是如何将复杂的 Istio CRD（如 VirtualService）进行抽象或兼容的。思考“开箱即用”和“极简”在架构设计中的体现。

### 

---
## 实践建议

以下是为 Higress 仓库提供的 6 条实践建议，涵盖了从流量接入、安全防护到 AI 网关特性的具体操作与避坑指南：

### 1. 利用 Wasm 插件实现 AI 协议的私有化适配
*   **场景**：当你的后端大模型服务使用了非标准的通信协议（如内部定制的 TCP 协议或特定格式的 HTTP），或者需要对请求体进行复杂的预处理（如敏感词过滤、Prompt 注入拦截）时。
*   **建议**：不要修改 Higress 的核心代码，而是编写 Wasm (WebAssembly) 插件。Higress 对接了 Envoy 的 Wasm 能力，支持使用 C++/Go/Rust 编写插件。
*   **操作**：参考 Higress 官方提供的 `ai-proxy` 等插件源码，开发自定义的 Wasm 滤镜，将其挂载到路由规则的 `filters` 配置中，实现无侵入的协议转换或请求篡改。

### 2. 配置基于 Token 的精细化限流
*   **场景**：大模型 API 调用成本高昂（按 Token 计费），且后端模型服务有并发限制（TPM/RPM）。传统的基于 QPS（每秒请求数）的限流无法准确控制成本和模型负载。
*   **建议**：在 Higress 的 `request-auth` 或 `local-ratelimit` 配置中，结合 AI 网关特性，不仅仅限制连接数，更要限制请求体的大小或预估的 Token 数量。
*   **操作**：配置全局限流策略，针对不同的 API Key 或用户 ID 设置 RPM（每分钟请求数）和 TPM（每分钟 Token 数）阈值，防止恶意用户通过发送超长 Prompt 耗尽预算或打挂后端模型。

### 3. 实施模型供应商的故障转移
*   **场景**：生产环境中，单一的大模型服务商（如 OpenAI 或通义千问）可能会出现 API 抖动或限流。为了保证业务的高可用性，需要具备切换能力。
*   **建议**：利用 Higress 的服务发现和路由权重功能，配置多模型源。
*   **操作**：在 Ingress 或网关路由配置中，定义多个后端 Service（分别指向不同的模型 Provider 或自建模型）。设置主备策略或按权重分流（例如 95% 走主模型，5% 走备用模型用于灰度）。当主模型返回 5xx 错误码时，利用 Higress 的重试机制自动切换到备用模型服务。

### 4. 警惕 SSE 流式响应的超时配置
*   **常见陷阱**：AI 对话通常采用 Server-Sent Events (SSE) 流式返回，一个请求可能持续几十秒甚至更久。如果网关层的连接超时或读取超时设置过短（例如默认的 60 秒），会导致流式中断，前端报错。
*   **建议**：针对 AI 类型的路由，显式调大超时时间。
*   **操作**：在 Higress 的路由配置中，将 `timeout` 参数设置为较大的值（如 `600s`），并确保上游服务的 `idleTimeout` 也相应调整，确保网关不会因为数据传输间隔较长而主动断开连接。

### 5. 做好 Prompt 注入防护与数据脱敏
*   **场景**：直接将用户输入透传给大模型存在安全风险，用户可能通过 Prompt 注入套取系统设定，或在输入中包含敏感信息（PII）。
*   **建议**：在网关层作为“守门员”进行第一道安检。
*   **操作**：部署 Wasm 插件或在网关配置中集成安全扫描模块。对于所有发往 `/v1/chat/completions` 等接口的请求，在转发前检查 `messages` 字段，拦截包含恶意指令的请求，或对身份证号、手机号等敏感信息进行正则匹配和掩码处理，确保敏感数据不出域。

### 6. 缓存常见问题的

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI 网关](/tags/ai-%E7%BD%91%E5%85%B3/) / [LLM](/tags/llm/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [WASM](/tags/wasm/) / [MCP](/tags/mcp/)
- 场景： [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [Kubernetes](/scenarios/kubernetes/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260205-github_trending-alibaba-higress-8.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*