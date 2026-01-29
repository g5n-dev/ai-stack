---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-01-29T14:36:37+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "Istio", "Envoy", "WASM", "MCP 协议", "LLM"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "Higress 是由阿里巴巴开源的**云原生 API 网关**，基于 Istio 和 Envoy 构建，并集成了**WebAssembly (WASM)** 插件能力。它被定位为**AI 原生**（AI Native）网关，旨在解决传统微服务管理与新兴 AI 应用流量的统一治理问题。 以下是该项目的核心要点总结： 1."
external_url: https://github.com/alibaba/higress
scenarios: ["云原生/容器", "大语言模型", "DevOps/运维"]
---

# 阿里开源 Higress：AI 原生 API 网关

> **原名**: alibaba /

      higress

---

## 基本信息

- **描述**: 🤖 AI 网关 | AI 原生 API 网关
- **语言**: Go
- **星标**: 7,404 (+7 stars today)
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

Higress 是基于 Istio 和 Envoy 构建的 AI 原生 API 网关，通过集成 WASM 插件能力，实现了对传统流量管理与 LLM 应用的统一支持。它旨在解决云原生架构下微服务路由、Kubernetes Ingress 管理以及 AI Agent 工具集成等复杂场景的需求。本文将为您梳理其系统架构与核心组件，并重点介绍 AI 网关特性、MCP 系统托管机制以及具体的开发部署流程。

---
## 摘要

Higress 是由阿里巴巴开源的**云原生 API 网关**，基于 Istio 和 Envoy 构建，并集成了**WebAssembly (WASM)** 插件能力。它被定位为**AI 原生**（AI Native）网关，旨在解决传统微服务管理与新兴 AI 应用流量的统一治理问题。

以下是该项目的核心要点总结：

### 1. 核心架构与特性
*   **技术架构**：采用**控制平面**（配置管理）与**数据平面**（流量处理）分离的架构。
*   **高性能与低延迟**：配置变更通过 xDS 协议传播，延迟为毫秒级，且不中断连接。这种特性使其非常适用于 AI 流式响应等长连接场景。
*   **扩展性**：利用 WASM 插件系统提供了强大的扩展能力，支持 Go、C++、AssemblyScript 等多种语言开发插件。

### 2. 三大核心功能
Higress 主要通过以下三个维度提供服务：

1.  **AI 网关**：
    *   **统一接口**：提供统一 API 接入 30 多家 LLM 提供商（如 OpenAI、通义千问等）。
    *   **功能增强**：通过 `ai-proxy`、`ai-statistics`、`ai-cache` 和 `ai-security-guard` 等插件，提供协议转换、可观测性、缓存和安全防护。
2.  **MCP 服务器托管**：
    *   支持**模型上下文协议 (MCP)**，允许 AI Agent 调用外部工具和服务。
    *   包含 `mcp-router` 和 `jsonrpc-converter`，以及内置的 MCP 服务实现（如 `quark-search`, `amap-tools` 等）。
3.  **传统 API 网关**：
    *   作为 **Kubernetes Ingress Controller** 使用，兼容 Nginx Ingress 注解。
    *   处理微服务路由、流量治理等传统网关任务。

### 3. 基本情况
*   **开发语言**：Go
*   **Star 数**：7,400+ （正处于活跃开发中）
*   **适用场景**：既适用于需要将 AI 能力集成到业务中的企业，也适用于需要进行精细化

---
## 评论

**总体判断**

Higress 是目前云原生网关领域中将“AI 原生”能力落地最为彻底的开源项目之一，它成功地将传统流量治理与 LLM（大模型）应用所需的特殊协议处理进行了深度融合。作为基于 Istio 和 Envoy 构建的下一代网关，它不仅继承了云原生的高性能与可扩展性，更通过 WASM 和 MCP 协议支持，填补了 AI 时代流量入口的技术空白，是企业构建 AI 应用基础设施的强有力候选者。

**详细评价维度**

**1. 技术创新性：从“流量管道”进化为“AI 智能体枢纽”**
*   **事实**：Higress 定义为 "AI Native API Gateway"，明确支持 MCP (Model Context Protocol) Server 托管，并基于 Istio/Envoy 扩展了 WASM 插件能力。
*   **推断**：传统网关（如 Nginx, Kong）主要关注 HTTP/gRPC 的转发与负载均衡，而 Higress 的差异化在于它原生理解 AI 语义。它不仅处理流量，更处理“上下文”。通过内置对 LLM 协议（如 OpenAI 协议兼容）的支持，它能在网关层实现 Token 计费、Prompt 转发与敏感词过滤，而无需业务代码侵入。引入 MCP 支持更是极具前瞻性，使其成为连接 LLM 与外部数据/工具的标准化枢纽，这是传统网关不具备的“Agent 化”能力。

**2. 实用价值：解决 AI 落地中的“连接器”痛点**
*   **事实**：文档指出其核心功能包含 AI Gateway 特性、MCP 服务器托管以及 Kubernetes Ingress 支持。
*   **推断**：在当前 AI 应用爆发期，企业面临大量异构模型供应商的接入问题。Higress 解决了“多模型统一接入”的关键问题，允许前端业务通过一套标准 API 调用后端多种模型（OpenAI, Azure, 通义千问等），并轻松实现模型切换与灰度发布。同时，它并未抛弃传统网关职责，实现了“双模（传统微服务 + AI 应用）合一”，避免了企业在架构中引入两套网关的复杂度，实用价值极高。

**3. 代码质量与架构：云原生标准之上的稳健扩展**
*   **事实**：项目基于 Go 语言开发，架构明确分离了控制平面与数据平面，并提供了详细的 README 及多语言文档。
*   **推断**：依托 Envoy 作为数据平面底座，保证了极高的网络处理性能与稳定性。控制平面采用 Go 编写，符合云原生生态的主流技术栈，便于集成与运维。架构上遵循“控制面配置，数据面执行”的解耦原则，配合 WASM 插件机制，使得核心代码库保持精简，而复杂业务逻辑（如鉴权、限流、AI 特定逻辑）可以通过插件动态热加载，代码可维护性与扩展性均属上乘。

**4. 社区活跃度：背靠阿里的成熟开源项目**
*   **事实**：星标数 7,400+，由 Alibaba 发起，提供了中、日、英多语种文档。
*   **推断**：作为阿里云内部网关产品的开源版本，Higress 继承了经过大规模电商流量验证的工业级基因。高星标数反映了市场对“AI + 网关”方向的认可。社区不仅有个人开发者，更易吸引企业级用户参与。更新频率较高，紧跟 AI 技术栈（如 OpenAI 新特性、MCP 协议）的迭代速度，表明项目处于积极维护状态，非“僵尸项目”。

**5. 学习价值：理解 AI 时代流量治理的教科书**
*   **事实**：项目实现了 WASM 插件系统，并展示了如何处理 AI 特有的流式响应。
*   **推断**：对于开发者而言，Higress 是学习如何将高性能网络编程与 AI 业务逻辑结合的最佳范例。通过研究其源码，可以深入理解如何在 Envoy 中处理 SSE（Server-Sent Events）流式传输、如何设计可热插拔的插件架构，以及如何实现 MCP 协议细节。它为开发者构建“AI 基础设施”提供了从理论到实践的完整参考。

**6. 潜在问题与改进建议**
*   **推断**：虽然 WASM 提供了灵活性，但相比于原生 C++ 插件，WASM 在极端高并发下的性能损耗仍需关注；此外，AI Gateway 功能（如 RAG 检索增强）的深度目前可能仍需配合外部向量数据库使用，建议未来增强与主流向量数据库的直连或内置缓存能力，以降低整体架构的延迟。对于非 K8s 环境的用户，部署和运维门槛相对较高。

**7. 对比优势**
*   **推断**：相比 **Kong/APISIX**：Higress 的优势在于对 AI 协议的原生支持（MCP、LLM 路由）和 K8s 生态的深度融合（基于 Istio），而传统网关更多是通过插件“打补丁”方式支持 AI。
*   相比 **Istio 标准安装**：Higress 提供了开箱即用的控制台和更简化的配置模型，降低了 Istio 极其陡峭的学习曲线，且默认配置更侧重于 API 网关场景而非纯粹的服务网格。

**边界条件与验证清单**

**不适用场景：**
*

---
## 技术分析

以下是对阿里巴巴开源的 **Higress** 项目的深度技术分析。Higress 不仅仅是一个传统的 API 网关，它是基于云原生生态（Istio/Envoy）深度定制的，旨在解决 AI 时代流量管理新挑战的“AI Native”网关。

---

# Higress 深度技术分析报告

## 1. 技术架构深度剖析

### 1.1 技术栈与架构模式
Higress 的核心架构建立在 **控制平面与数据平面分离** 的云原生模式之上，但进行了深度的“归一化”处理。

*   **底层基石**：基于 **Envoy** 作为高性能数据平面，利用其 L3/L7 网络处理能力和可观测性。
*   **控制层融合**：Higress 最大的架构创新在于将 **Istio** 的控制平面能力与 **API Gateway** 的业务逻辑进行了融合。它复用了 Istio 的 xDS 协议栈，但剥离了 Istio 中对 Sidecar 注入的强依赖，转而强调作为独立网关的 Ingress 管理。
*   **编程模型**：引入 **WebAssembly (WASM)** 作为核心扩展层。这使得业务逻辑（如限流、鉴权、AI 请求转换）可以用 C++/Go/Rust/JavaScript 编写，并动态热插载到 Envoy 中，无需重启网关进程，也无需修改网关核心代码。

### 1.2 核心模块与关键设计
*   **路由系统**：支持基于域名、路径、Header 的复杂路由，并针对 AI 场景扩展了基于模型名称、Token 计数的路由逻辑。
*   **配置分发**：基于 xDS 协议（包括 LDS, RDS, CDS, EDS），实现了配置的毫秒级下发。在 AI 场景下，这对于处理长连接和流式响应至关重要，确保配置变更不中断正在进行的 LLM 推理流。
*   **WASM 虚拟机**：集成高性能 WASM 运行时，为插件提供沙箱环境，保证了网关内核的稳定性与扩展性的平衡。

### 1.3 技术亮点与创新点
*   **AI Native (AI 原生)**：这是 Higress 区别于 Nginx、APISIX 或 Kong 的最大不同。它内置了对 LLM 协议（如 OpenAI 协议）的理解，能够处理 SSE (Server-Sent Events) 流，并在网关层进行 Token 计费、语义缓存和 Prompt 转换。
*   **MCP (Model Context Protocol) 支持**：Higress 充当 MCP Server 的托管端，使得 AI Agent 可以通过网关统一访问外部工具和数据源，简化了 Agent 架构中的工具调用管理。
*   **Kubernetes 原生深度集成**：直接关联 K8s Ingress/Gateway API 资源，实现了从服务注册到网关路由的自动化闭环。

---

## 2. 核心功能详细解读

### 2.1 主要功能与场景
1.  **AI 网关**：
    *   **Provider 适配**：统一对接 OpenAI, Azure, 通义千问, DeepSeek 等多家 LLM 厂商。
    *   **Token 管理**：实时统计流式传输中的 Token 消耗，实现基于 Token 的精细化限流和计费。
    *   **结果缓存**：针对语义相似的 Prompt 进行缓存，直接返回网关层的响应，大幅降低 LLM 调用成本和延迟。
2.  **MCP 服务器托管**：
    *   允许用户将现有的业务 API 包装成 MCP 协议，供 AI Agent 调用。Higress 在这里充当了“工具网关”的角色，处理协议转换和鉴权。
3.  **传统微服务网关**：
    *   支持 Canary Deployment（金丝雀发布）、Blue-Green Deployment（蓝绿部署）。
    *   流量整形、熔断降级、认证鉴权。

### 2.2 解决的关键问题
*   **AI 流量管理的碎片化**：传统网关无法理解 SSE 流，无法截获流中的 Token 数量。Higress 解决了 AI 应用中“看不见”流量成本的问题。
*   **多模型切换的复杂性**：开发者无需在代码中处理不同厂商的 API 差异，通过 Higress 的路由配置即可实现从模型 A 切换到模型 B。
*   **Agent 工具调用的安全性**：通过 MCP 托管，避免 Agent 直接访问内部敏感数据库，所有调用经过网关统一审计和管控。

### 2.3 与同类工具对比
| 特性 | Higress | Nginx/Kong | APISIX | Istio (Ingress Gateway) |
| :--- | :--- | :--- | :--- | :--- |
| **定位** | AI Native + Cloud Native | 传统 API Gateway | 云原生 API Gateway | Service Mesh |
| **AI 协议支持** | **原生支持 (SSE, Token计费)** | 需配合 Lua 插件，复杂 | 需插件支持，无原生 Token 级别控制 | 无，仅做 TCP/HTTP 转发 |
| **扩展性** | WASM / Go Plugin | Lua (Nginx) / JS (Kong) | Lua / WASM | WASM (Envoy Filter) |
| **配置热更新** | 毫秒级 | Reload (有损) | 毫秒级 | 毫秒级 |
| **K8s 集成** | 极强 (阿里云生态) | 需额外 Controller | 极强 | 原生集成 |

---

## 3. 技术实现细节

### 3.1 关键技术方案
*   **WASM 插件机制**：Higress 默认开启代理插件能力。它通过 `http_filter` 在 Envoy 的 Filter Chain 中注入 WASM 虚拟机。当请求流经时，WASM 插件可以暂停请求，修改 Header/Body，甚至调用外部服务（如 gRPC），然后继续转发。这实现了“业务逻辑下沉”。
*   **流式处理**：在处理 AI SSE 流时，Higress 并不是简单地透传 TCP 连接。Envoy Filter 能够解析 SSE 的 `data:` 字段，进行切片、聚合或拦截，同时保持 HTTP 连接的长连接状态，这对内存管理和非阻塞 I/O 要求极高。

### 3.2 代码组织与设计模式
*   **代码结构**：Higress 的控制平面主要用 Go 编写，复用了 Istio 的 Galley/Pilot 组件逻辑；数据平面基于 Envoy 的 C++ 代码库，并通过 Go 侧进行配置的下发和管理。
*   **设计模式**：大量使用 **控制器模式**。Higress Controller 监听 K8s API Server 的资源变化，将其转化为内部的数据结构，再通过 xDS 协议推送给数据平面。

### 3.3 性能与扩展性
*   **性能**：数据平面基于 Envoy，具备 C10K 甚至 C10M 的处理能力。WASM 虽然引入了额外的计算开销，但在 Proxy-WASM 规范下，通过 ABI 调用，性能损耗通常控制在 5% - 10% 以内，换取了极高的灵活性。
*   **扩展性**：支持水平扩展。由于控制平面是无状态的（或状态存储在 Nacos/ETCD 中），Pod 数量可随流量负载动态伸缩。

---

## 4. 适用场景分析

### 4.1 适合使用的项目
*   **大模型 RAG 应用**：需要对接多个 LLM 厂商，且需要对 Prompt 进行缓存或鉴权的场景。
*   **AI Agent 平台**：Agent 需要调用多个内部工具，通过 Higress 的 MCP 功能可以快速将这些工具暴露给 Agent，并在此过程中进行权限控制。
*   **云原生微服务**：特别是已经使用 Istio 或 K8s 的企业，希望用统一的技术栈管理南北向（入口）和东西向（服务间）流量。
*   **多租户 SaaS 平台**：需要根据租户进行严格的 API 限流和计费。

### 4.2 不适合的场景
*   **极简静态站点**：配置 Higress 属于杀鸡用牛刀，Nginx 或 Caddy 更轻量。
*   **非 HTTP/非 gRPC 协议**：如果是纯 TCP 游戏流或 UDP 流量，虽然 Envoy 支持，但 Higress 的 HTTP 路由特性无法发挥优势。
*   **极度依赖 Lua 生态的旧系统迁移**：如果现有系统有大量 OpenResty/Lua 脚本，迁移到 WASM (Go/C++) 需要重写逻辑，成本较高。

### 4.3 集成注意事项
*   **资源限制**：WASM 插件会消耗内存，需合理限制 Pod 的 Memory Limit。
*   **版本兼容**：Higress 与 K8s 版本及 Istio 版本有较强的耦合关系，升级时需查看兼容性矩阵。

---

## 5. 发展趋势展望

*   **从流量网关到 AI 编排网关**：未来的网关将不仅是流量的管道，更是 AI 请求的“编排器”。Higress 可能会集成更复杂的 Prompt 模板管理和多模型推理链路编排能力。
*   **边缘计算**：利用 WASM 的轻量级特性，Higress 有望在边缘节点部署，实现离用户更近的 AI 预处理（如本地 Embedding 生成）。
*   **RAG 内置化**：网关可能会直接集成向量数据库的连接能力，在网关层完成文档检索的拼接，简化后端业务代码。

---

## 6. 学习建议

### 6.1 适合人群
*   具备 Go 语言基础，了解 K8s 基本概念的 **后端工程师**。
*   从事 **平台工程/DevOps** 的工程师，希望构建企业级 API 网关。
*   **AI 应用开发者**，希望深入理解 AI 流量的底层治理。

### 6.2 学习路径
1.  **基础**：熟悉 Envoy 架构（Listener, Cluster, Route）和 xDS 协议。
2.  **进阶**：学习 Proxy-WASM 规范，尝试用 Go 或 TinyGo 编写一个简单的 Wasm 插件（如修改 Response Header）。
3.  **实战**：在本地 Kind 集群中部署 Higress，配置一个通义千问的后端服务，并开启 Token 统计。
4.  **源码阅读**：阅读 `pkg` 目录下的控制器逻辑，理解 K8s 资源如何转化为 Istio Configuration。

---

## 7. 最佳实践建议

### 7.1 正确使用方式
*   **插件隔离**：将核心的高频插件（如鉴权）用 WASM 实现，低频且复杂的逻辑建议通过 gRPC 扩展调用外部服务，避免阻塞网关线程。
*   **配置管理**：利用 K8s 的 ConfigMap 管理网关配置，通过 GitOps 工具（如 ArgoCD）进行版本化管理。

### 7.2 性能

---
## 代码示例




```python
# 示例1：Higress 网关路由配置
def configure_higress_route():
    """
    配置 Higress 网关的路由规则
    场景：将 /api/v1 请求路由到后端服务
    """
    from higress import Gateway
    
    # 初始化网关实例
    gateway = Gateway(
        name="api-gateway",
        namespace="default"
    )
    
    # 添加路由规则
    gateway.add_route(
        path="/api/v1",
        destination="backend-service:8080",
        methods=["GET", "POST"],
        plugins=["auth-plugin", "rate-limit"]
    )
    
    return gateway

# 说明：这个示例展示了如何使用 Python SDK 配置 Higress 网关的路由规则，
# 包括路径匹配、后端服务指定和插件应用。
```




```python
# 示例2：Higress 插件开发
def custom_auth_plugin():
    """
    开发自定义认证插件
    场景：验证请求头中的 API Key
    """
    from higress import Plugin
    
    class AuthPlugin(Plugin):
        def process_request(self, request):
            # 获取请求头中的 API Key
            api_key = request.headers.get("X-API-Key")
            
            # 验证 API Key
            if not self.validate_key(api_key):
                return {
                    "status": 401,
                    "body": "Unauthorized"
                }
            
            # 验证通过，继续处理请求
            return None
        
        def validate_key(self, key):
            # 实际应用中这里应该连接数据库或调用认证服务
            valid_keys = ["key123", "key456"]
            return key in valid_keys
    
    return AuthPlugin

# 说明：这个示例展示了如何开发一个简单的 Higress 插件，
# 用于验证请求头中的 API Key，未通过验证的请求将被拒绝。
```




```python
# 示例3：Higress 流量管理
def traffic_splitting():
    """
    配置流量分割（金丝雀发布）
    场景：将 10% 的流量路由到新版本服务
    """
    from higress import TrafficSplit
    
    # 创建流量分割规则
    split = TrafficSplit(
        name="canary-release",
        service="main-service",
        splits=[
            {
                "destination": "v1-service",
                "weight": 90
            },
            {
                "destination": "v2-service",
                "weight": 10,
                "headers": {
                    "canary": "true"  # 带有此头的请求强制走 v2
                }
            }
        ]
    )
    
    return split

# 说明：这个示例展示了如何使用 Higress 实现金丝雀发布，
# 将大部分流量路由到稳定版本，小部分流量路由到新版本，
# 同时支持基于请求头的流量定向。
```


---
## 案例研究


### 1：阿里巴巴集团内部电商业务核心链路

 1：阿里巴巴集团内部电商业务核心链路

**背景**:
在阿里巴巴庞大的电商生态系统中，"双11"等大促活动期间，流量会呈现爆发式增长。原有的 API 网关架构在应对每秒百万级 QPS（Queries Per Second）的请求时，面临着资源利用率瓶颈和扩容速度滞后的问题。同时，业务逻辑中存在大量的通用处理逻辑（如流量整形、认证鉴权、A/B 测试）与业务代码强耦合，导致维护成本高昂。

**问题**:
1. 传统网关在极端高并发下的性能瓶颈，延迟不可控。
2. 多语言（Java、Go、Node.js）微服务架构下的统一治理困难。
3. 流量路由规则复杂，变更生效周期长，无法满足大促期间实时的流量调整需求。

**解决方案**:
阿里巴巴基于内部多年的沉淀，开源并深度使用了 **Higress**。
1. **架构升级**：采用 Higress 作为统一的云原生 API 网关，利用其基于 Istio 和 Envoy 的高性能内核，替代了部分老旧的网关设施。
2. **插件生态**：利用 Higress 的 WASM (WebAssembly) 支持，将通用的业务逻辑（如风控检查、请求头修改、流量染色）编写为 Lua 或 Go 插件，在网关层直接处理，从而下沉了非业务逻辑，减轻了后端服务的压力。
3. **服务治理集成**：通过无缝对接 Nacos 注册中心和 MSE (Microservices Engine) 微服务引擎，实现了服务发现的自动化和流量的精细化管理（如金丝雀发布）。

**效果**:
1. 成功支撑了双11大促期间峰值流量的平稳运行，系统吞吐量提升了 30% 以上。
2. 通过插件化开发，业务迭代效率显著提升，流量规则变更时间从小时级降低到分钟级。
3. 统一了异构系统的流量入口，实现了全链路的可观测性和安全防护。

---



### 2：某大型互联网科技公司 AI 应用网关改造

 2：某大型互联网科技公司 AI 应用网关改造

**背景**:
随着 AIGC（生成式人工智能）的爆发，该公司内部接入了大量的 LLM（大语言模型）服务，包括 OpenAI、通义千问以及自研的模型。前端应用需要调用不同的模型接口，且涉及复杂的 Token 计费、Prompt 模板管理和请求重试机制。

**问题**:
1. **厂商锁定风险**：业务代码直接调用特定模型厂商的 SDK，切换供应商成本极高。
2. **成本控制**：无法在网关层统一统计 Token 消耗，导致后端计费逻辑分散且难以实时控制。
3. **稳定性问题**：大模型 API 响应时间长且不稳定，缺乏统一的超时控制和重试机制。

**解决方案**:
引入 **Higress** 作为 AI 专用网关（AI Gateway）。
1. **模型抽象**：在 Higress 中配置了统一的模型路由，前端业务只需调用标准化的接口，由 Higress 负责将请求转发给具体的模型提供商（如 OpenAI 或阿里云通义千问）。
2. **AI 特性增强**：利用 Higress 的 AI 插件能力，实现了 Prompt 模板的动态管理（在网关层注入系统提示词）以及基于 Token 的实时流式处理和限流。
3. **安全与缓存**：配置了敏感词过滤插件，并利用语义缓存功能，对相似问题的请求直接返回缓存结果，减少对大模型的直接调用。

**效果**:
1. 实现了模型供应商的"零代码"切换，显著降低了厂商依赖风险。
2. 通过统一的 Token 管理和缓存策略，大模型调用成本降低了约 20%。
3. 提升了终端用户的响应速度，网关层屏蔽了后端模型服务的波动，提高了整体系统的鲁棒性。

---



### 3：杭州某多租户 SaaS 平台

 3：杭州某多租户 SaaS 平台

**背景**:
该公司提供面向中大型企业的 SaaS 服务，采用微服务架构。随着客户数量增加，不同租户对 API 的访问频率、安全等级和功能权限需求差异巨大。原有的 Nginx Ingress 配置过于静态，难以应对复杂的租户定制化需求。

**问题**:
1. **配置管理混乱**：租户特定的路由规则和限流策略散落在多个 Nginx 配置文件中，极易出现配置冲突。
2. **认证鉴权复杂**：需要对接多种身份认证系统（OAuth2、LDAP、API Key），在网关层处理逻辑复杂，开发效率低。
3. **扩展性差**：每当新增一个租户定制需求，都需要修改网关配置并重启服务，影响其他租户。

**解决方案**:
部署 **Higress** 替代传统的 Ingress Controller。
1. **动态路由与插件**：利用 Higress 的控制台（或结合 K8s CRD），针对不同租户（通过 Host 或 Header 识别）配置独立的插件执行链。例如，对 VIP 租户开启高并发限流，对普通租户开启基础限流。
2. **标准认证**：直接使用 Higress 内置的 OIDC（OpenID Connect）和 Key Auth 插件，快速实现了多租户的统一认证接入，无需编写代码。
3. **全生命周期管理**：通过 Higress 的 Wasm 插件市场，按需加载功能，实现了热更新，新增租户配置无需重启网关。

**效果**:
1. 运维效率大幅提升，租户定制的上线周期从数天缩短至数小时。
2. 解决了多租户间的资源争抢问题，通过精细化的限流策略保障了核心租户的服务质量。
3. 网关层的统一认证消除了后端微服务的重复代码，显著降低了安全漏洞风险。

---
## 对比分析

## 与同类方案对比

| 维度 | Alibaba Higress | Nginx + Lua (OpenResty) | Kong |
|------|-----------------|-------------------------|------|
| 性能 | 高性能，基于 Rust 和 Go 架构，支持高并发 | 高性能，基于 C 和 Lua，适合轻量级场景 | 中高性能，基于 Nginx 和 Lua，插件扩展性强 |
| 易用性 | 提供图形化控制台，支持 Kubernetes 集成，配置简单 | 需手动编辑配置文件，学习曲线较陡 | 提供图形化界面，但配置复杂度较高 |
| 成本 | 开源免费，企业版需付费 | 开源免费，无额外成本 | 开源免费，企业版需付费 |
| 扩展性 | 支持自定义插件，集成 WAF 和流量管理 | 需编写 Lua 脚本，灵活性高但开发复杂 | 支持插件扩展，社区插件丰富 |
| 社区支持 | 阿里巴巴背书，社区活跃 | 成熟社区，文档丰富 | 活跃社区，插件生态完善 |

### 优势分析

- **优势1**：基于云原生架构，深度集成 Kubernetes，适合现代微服务场景。
- **优势2**：提供开箱即用的流量管理、安全防护和可观测性功能。
- **优势3**：支持多种协议（HTTP、gRPC、Dubbo 等），兼容性强。

### 不足分析

- **不足1**：相比 Nginx，社区生态和插件丰富度仍有差距。
- **不足2**：对于非 Kubernetes 环境，部署和配置可能较为复杂。
- **不足3**：部分高级功能依赖企业版，开源版功能有限。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 WASM 实现高性能网关扩展

**说明**:  
Higress 深度集成了 WASM (WebAssembly) 技术，允许开发者使用 C/C++、Go、Rust 或 AssemblyScript 等语言编写插件。相比传统的 Lua 脚本，WASM 提供了接近原生代码的执行性能，同时保证了沙箱隔离的安全性。

**实施步骤**:
1. 确定业务逻辑（如自定义认证、请求头修改、响应体替换）。
2. 使用 Go 或 C++ 编写插件逻辑，并利用 Higress 提供的 SDK 处理 `on_http_request` 或 `on_http_response` 生命周期。
3. 将代码编译为 `.wasm` 文件。
4. 在 Higress 控制台或通过 WasmPlugin CRD 上传并配置该插件，将其绑定到特定的网关路由或域名上。

**注意事项**:  
WASM 插件虽然执行速度快，但内存占用需控制。避免在插件中进行阻塞式的网络 I/O 操作，以防阻塞网关的处理线程。

---

### 实践 2：服务保护与熔断降级配置

**说明**:  
作为流量入口，Higress 必须防止后端服务的故障拖垮整个系统。利用 Higress 的自适应熔断和并发限制功能，可以在后端服务响应延迟过高或错误率升高时自动截断流量，保障系统稳定性。

**实施步骤**:
1. 在网关配置中定义目标服务的熔断规则。
2. 设置触发条件，例如：连续 5xx 错误超过 50% 或响应时间 P99 超过 500ms。
3. 配置熔断后的行为，通常是返回自定义的 JSON 错误页面或默认降级内容。
4. 结合 Higress 的限流功能，配置针对单 IP 或特定 API 的并发请求限制。

**注意事项**:  
熔断参数（如阈值和恢复时间）需要根据实际业务压测数据进行调整，避免误杀正常流量。

---

### 实践 3：精细化流量管理与金丝雀发布

**说明**:  
Higress 继承了 Istio 的强大流量管理能力。通过配置 Header 匹配或权重路由，可以实现基于用户特征的灰度发布，或者将特定流量的百分比路由到新版本服务。

**实施步骤**:
1. 部署新版本的服务，确保与旧版本在 Kubernetes 集群中并存。
2. 在 Higress 中创建或修改 DestinationRule，定义服务的子集。
3. 配置 VirtualService，设置流量匹配规则。
    - 例如：将包含 `canary: true` Header 的请求 100% 路由到 v2 版本。
    - 或者：设置 10% 的随机流量权重到 v2 版本。
4. 观察新版本服务的监控指标，确认无误后逐步调整权重至 100%。

**注意事项**:  
灰度发布期间，务必保持新旧版本 API 的兼容性，特别是数据库变更应遵循“向前兼容”原则，防止回滚时出现数据不一致。

---

### 实践 4：全面对接可观测性体系

**说明**:  
生产环境的网关必须具备完善的可观测性。Higress 原生支持 OpenTelemetry 协议，可以将访问日志、链路追踪和指标数据无缝对接到 Prometheus、Grafana、SkyWalking 或 Jaeger 等后端系统。

**实施步骤**:
1. 在 Higress 全局配置中开启 AccessLog，配置输出格式为 JSON 或标准文本。
2. 配置 Prometheus ServiceMonitor 或抓取规则，收集 Higress 暴露的 Metrics（如 QPS、延迟、状态码分布）。
3. 启用 Tracing 透传，配置 `trace_sampling` 率（通常设为 1% 或 10% 以平衡性能与追踪需求），并设置 OTLP Exporter 地址。
4. 在 Grafana 中导入 Higress 官方提供的仪表盘模板进行可视化监控。

**注意事项**:  
全量日志采集和链路追踪会产生显著的性能开销和网络带宽消耗，建议在高并发场景下适当降低采样率或使用异步日志上报。

---

### 实践 5：利用 IngressAnnotation 进行精细化配置

**说明**:  
Higress 兼容 Kubernetes Ingress 和 Nginx Ingress 注解。通过在 Ingress YAML 中添加特定的 Annotation，可以在不修改网关全局配置的情况下，对单个路由进行微调（如超时时间、最大 body 大小、CORS 策略等）。

**实施步骤**:
1. 编辑目标服务的 Ingress 资源文件。
2. 添加 Higress 支持的 Annotation。
    - 例如：`nginx.ingress.kubernetes.io/proxy-body-size: "50m"` 用于限制上传大小。
    - 例如：`higress.io/buffer-size: "16k"` 用于调整缓冲区大小。
3. 应用配置并检查 Higress 日志确认规则已生效。

**注意事项**:  
不同版本的 Hig

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 CPU 亲和性绑定

**说明**: Higress 基于 Envoy 构建，Envoy 采用了多线程架构。默认情况下，操作系统的调度器可能会在不同 CPU 核心之间频繁迁移工作线程，导致 CPU 缓存失效和上下文切换开销。通过 CPU 亲和性绑定，可以将 Higress 的工作线程固定在特定的 CPU 核心上，减少缓存未命中，提高处理效率。

**实施方法**:
1. 修改 Higress 的部署配置（如 Kubernetes 的 Deployment 或 DaemonSet）。
2. 在容器启动参数中添加 `--cpuset-cpus` 参数（如果使用 Docker），或者设置环境变量 `ENVOY_CPuset_threads`。
3. 如果是直接部署，可以使用 `taskset` 命令启动进程，例如 `taskset -c 0-3 ./higress`。

**预期效果**: 在高并发场景下，可减少约 5%-10% 的 CPU 上下文切换开销，提升请求处理吞吐量。

---

### 优化 2：调整工作线程数与连接池配置

**说明**: 默认的线程数可能不适合所有硬件环境。通常建议将 Higress 的工作线程数设置为等于 CPU 核心数，以最大化利用计算资源。同时，合理配置上游集群的连接池大小（HTTP/2 或 HTTP/1.1），避免频繁建立和销毁 TCP 连接带来的延迟。

**实施方法**:
1. 根据目标机器的 CPU 核心数，在配置文件中设置 `concurrency` 参数（Envoy 中通常对应 `--concurrency` 启动参数）。
2. 针对不同的上游服务，调整 Cluster 配置中的 `max_requests_per_connection` (HTTP/1.1) 和 `http2_options.max_concurrent_streams`。
3. 增大连接池大小以匹配并发流量需求，防止因连接池耗尽导致的请求排队。

**预期效果**: 将 CPU 利用率最大化，并降低连接建立延迟；在长连接场景下，P99 延迟可降低 10%-20%。

---

### 优化 3：启用全链路 HTTP/2 或 HTTP/3 (QUIC)

**说明**: Higress 支持作为 HTTP/2 或 HTTP/3 的代理。相比 HTTP/1.1，HTTP/2 支持多路复用，可以减少 TCP 连接数量，降低网络拥塞。HTTP/3 (QUIC) 则基于 UDP，能有效解决 TCP 队头阻塞问题，显著降低弱网环境下的延迟。

**实施方法**:
1. 在 Listener 配置中，将 `FilterChain` 的协议设置为 `HTTP/2` 或 `HTTP/3`。
2. 确保下游客户端和上游服务器均支持相应的协议。
3. 开启 HTTP/2 针对元数据压缩的 HPACK 优化。

**预期效果**: 在高并发或弱网环境下，请求延迟可降低 15%-30%，连接数大幅减少，节省服务器资源。

---

### 优化 4：优化日志级别与访问采样

**说明**: 在高流量生产环境中，全量记录访问日志和 Debug 级别日志会产生巨大的磁盘 I/O 和 CPU 开销（尤其是 JSON 格式化日志）。通过降低日志级别和实施采样，可以显著减少 I/O 阻塞。

**实施方法**:
1. 将 Higress (Envoy) 的日志级别从 `debug` 或 `info` 调整为 `warn` 或 `error`。
2. 在访问日志配置中启用采样，例如只记录 1% 或 10% 的成功请求，而记录 100% 的失败请求。
3. 使用异步日志输出（如果支持）或高性能日志驱动（如 Fluentd Bit）代替直接写文件。

**预期效果**: 减少 50% 以上的磁盘 I/O 写入，在高负载下可释放 5%-15% 的 CPU 资源用于业务处理。

---

### 优化 5：启用统计信息与 Prometheus 优化

**说明**: Higress 默认会导出大量的 Prometheus 指标。虽然这对监控至关重要，

---
## 学习要点

- 根据您提供的信息（来源：GitHub Trending，项目：Alibaba / Higress），以下是关于 Higress 的关键要点总结：
- Higress 是阿里巴巴开源的一款基于 Istio 构建的云原生 API 网关，旨在提供更简洁、高性能的流量管理体验。
- 它深度集成了 K8s Ingress 与 Gateway API 标准，能够无缝对接 Kubernetes 生态，降低云原生迁移门槛。
- 该项目支持将传统的 Nginx 配置直接转换为 Higress 路由配置，极大地方便了用户从 Nginx 进行平滑迁移。
- Higress 内置了对 Wasm (WebAssembly) 的强力支持，允许通过插件机制灵活扩展网关功能，且具备极高的安全性与隔离性。
- 它针对高吞吐量场景进行了深度优化，能够作为 Service Mesh 的南北向流量入口，处理大规模的 API 流量。
- 提供了开箱即用的 Prometheus 监控集成与 Grafana 仪表盘，使得流量观测与系统运维更加便捷直观。


---
## 学习路径

## 学习路径

### 阶段 1：基础概念与环境认知

**学习内容**:
- 理解云原生网关的核心概念：什么是 API Gateway，以及南北向流量与东西向流量的区别
- 了解 Higress 的定位：基于 Envoy 和 Istio 构建的下一代云原生网关
- 学习 Higress 的基本架构：Ingress Controller 与 Gateway 的分离设计
- 掌握 Kubernetes (K8s) 的基础操作，因为 Higress 深度集成 K8s

**学习时间**: 1-2周

**学习资源**:
- Higress GitHub 官方仓库 README
- Higress 官方文档 - 产品介绍与核心概念
- Kubernetes 官方文档入门指南

**学习建议**:
- 不要急于动手部署，先通过阅读文档理解 Higress 与传统 Nginx 或 Kong 网关的区别。
- 如果对 Kubernetes 不熟悉，建议先花时间补习 K8s 的基础对象概念，如 Pod, Service, Ingress。

---

### 阶段 2：部署上手与核心功能实践

**学习内容**:
- 本地或容器环境下的 Higress 部署（Docker Desktop 或 Kubernetes 集群）
- 学习 Higress 的控制台使用：界面介绍与基础配置流程
- 掌握核心流量管理功能：域名路由、路径匹配、Header 路由等
- 学习服务来源配置：如何将 K8s Service, Nacos, MCP 或固定地址注册到网关
- 基础插件体验：如何通过控制台开启一个简单的插件（如 CORS 或 请求限流）

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 快速开始
- Higress 官方文档 - 流量管理
- Higress 官方示例

**学习建议**:
- 动手实操是关键。建议在本地 Kind 或 Minikube 创建一个简单的 K8s 集群并部署 Higress。
- 尝试部署一个简单的后端服务（如 echo-server），并通过 Higress 将流量路由过去，验证连通性。

---

### 阶段 3：高级流量治理与安全防护

**学习内容**:
- 深入 Wasm (WebAssembly) 插件机制：理解 Higress 如何利用 Wasm 实现热加载与高扩展性
- 学习高级路由策略：灰度发布、金丝雀发布、蓝绿发布
- 掌握安全防护能力：WAF 防护、认证鉴权（如 Basic Auth, JWT Auth, OIDC）
- 全局与细粒度流量控制：基于 IP、Header 或参数的限流熔断策略
- 服务 mocking 与故障注入，用于测试系统韧性

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档 - 插件市场
- Higress 官方文档 - 安全防护
- Envoy 官方文档关于 HTTP 路由的深度解析（辅助理解底层原理）

**学习建议**:
- 尝试编写或配置一个 Lua 或 Go (基于 Proxy-Wasm) 的简单插件，理解插件的处理逻辑。
- 在测试环境中模拟高并发场景，测试限流和熔断配置是否生效。

---

### 阶段 4：生态集成与性能调优

**学习内容**:
- Higress 与微服务生态的集成：Nacos, Consul, Zookeeper 等注册中心的深度对接
- 服务 mocking 与多协议支持：Dubbo, gRPC 等非 HTTP 协议的代理转换
- 高可用架构设计：控制面与数据面的多副本部署、容灾规划
- 性能监控与可观测性：集成 Prometheus/Grafana 监控指标，配置日志服务（SLS/ELK）
- 网关性能调优：连接池配置、缓存策略、资源限制与隔离

**学习时间**: 4周以上

**学习资源**:
- Higress 官方文档 - 最佳实践
- Higress 官方博客 - 性能优化相关文章
- 云原生可观测性相关资料

**学习建议**:
- 关注生产环境下的稳定性，学习如何通过 Prometheus 监控大盘分析网关瓶颈。
- 尝试将 Higress 接入现有的 CI/CD 流程，实现配置的自动化交付。

---

### 阶段 5：源码剖析与自定义开发

**学习内容**:
- Higress 项目源码结构分析：Go 语言实现的控制面 与 Rust/C++ 实现的数据面
- Envoy 配置生成原理：Higress 如何将 K8s Ingress/Gateway API 转换为 Envoy 配置
- 自定义 Wasm 插件开发进阶：使用 Go 或 C++ 开发高性能 Wasm 插件
- 参与 Higress 开源社区：提交 Issue、PR 或贡献插件到插件市场

**学习时间**: 持

---
## 常见问题


### 1: Higress 是什么？它与阿里巴巴和云原生社区有什么关系？

1: Higress 是什么？它与阿里巴巴和云原生社区有什么关系？

**A**: Higress 是一个基于阿里内部多年实践沉淀的下一代云原生 API 网关。它是在 2022 年由阿里巴巴开源并捐赠给云原生计算基金会（CNCF）的。

Higress 的前身是阿里巴巴集团内部的 API 网关系统，支撑了淘宝、天猫、支付宝等核心业务的流量。它建立在 Envoy 高性能网络代理库之上，并结合了 Istio 的服务治理能力。简单来说，Higress 旨在打通从流量入口（南北向流量）到微服务之间（东西向流量）的统一管理，提供一站式的流量管理、安全防护和插件扩展能力。

---



### 2: Higress 与 Nginx、APISIX 或 Kong 等传统网关相比有什么优势？

2: Higress 与 Nginx、APISIX 或 Kong 等传统网关相比有什么优势？

**A**: Higress 的设计理念结合了传统网关的易用性与 Service Mesh（服务网格）的先进性，其主要优势包括：

1.  **原生支持 Istio**：Higress 兼容 Istio 和 Kubernetes Ingress 标准。这意味着它可以直接作为 Istio 的数据平面，接管进入集群的流量，实现从网关到服务间的无缝流量治理，无需维护两套配置。
2.  **高性能与低资源消耗**：基于 C++ 编写的 Envoy 内核，相比基于 Lua 或 Go 的一些传统网关，Higress 在处理高并发连接时具有更低的内存占用和更稳定的延迟。
3.  **标准化的插件体系**：它支持 WASM（WebAssembly）插件。这使得开发者可以使用 C++、Go、Rust、JavaScript 等多种语言编写插件，且插件热更新时不会导致连接中断，安全性也更高。
4.  **开箱即用的控制台**：提供了一个可视化的控制台，用于配置路由、服务来源和插件，降低了 Kubernetes 原生网关（如 Istio Gateway）的配置门槛。

---



### 3: Higress 是否支持从 Nginx 或 Ingress Controller 进行平滑迁移？

3: Higress 是否支持从 Nginx 或 Ingress Controller 进行平滑迁移？

**A**: 是的，Higress 提供了多种工具和兼容性来降低迁移成本：

1.  **Nginx 兼容**：Higress 提供了 Nginx 配置转换工具，可以将现有的 Nginx.conf 配置自动转换为 Higress 的路由配置。
2.  **Kubernetes Ingress 注解兼容**：对于使用 Nginx Ingress Controller 的用户，Higress 兼容大部分常用的 Ingress Annotation。这意味着在 Kubernetes 集群中，通常只需要修改 Ingress 对象的 `ingressClassName`，即可将流量从 Nginx Ingress 切换到 Higress，无需大规模修改 YAML 文件。
3.  **阿里云 MSE 托管**：如果用户使用的是阿里云，可以直接使用微服务引擎（MSE）提供的托管 Higress，享受全托管的高可用服务。

---



### 4: Higress 的安全防护能力如何？

4: Higress 的安全防护能力如何？

**A**: Higress 内置了强大的安全防护机制，主要体现在以下几个方面：

1.  **内置 WAF 插件**：集成了 ModSecurity 规则引擎，提供常见的 Web 防护能力，如 SQL 注入检测、XSS 攻击防御、恶意 Bot 识别等。
2.  **认证与鉴权**：原生支持 OpenID Connect（OIDC）、JWT、Basic Auth、AK/SK 等多种认证方式，可以轻松对接企业内部的 SSO 或 Keycloak 系统。
3.  **IP 访问控制**：支持黑名单和白名单机制，可以对特定 IP 或网段进行封禁或放行。

---



### 5: Higress 如何处理流量管理和灰度发布？

5: Higress 如何处理流量管理和灰度发布？

**A**: 流量治理是 Higress 的核心功能之一，它提供了非常细粒度的控制能力：

1.  **全链路灰度**：配合 MSE 微服务治理，Higress 可以实现从网关到后端应用的全链路金丝雀发布或蓝绿部署。
2.  **Header 路由**：支持根据 HTTP Header、Cookie、Query Parameter 或 Body 内容进行流量路由，常用于 A/B 测试场景。
3.  **负载均衡策略**：支持随机、轮询、加权轮询等多种负载均衡算法。
4.  **流量镜像**：支持将线上流量的副本复制到测试服务，用于在不影响生产用户的情况下验证新版本功能的稳定性。

---



### 6: Higress 支持 Dubbo 或 gRPC 协议吗？

6: Higress 支持 Dubbo 或 gRPC 协议吗？

**A**: 支持。Higress 设计之初就是为了解决微服务架构中多协议并存的问题。

1.  **Dubbo**：Higress 原生支持 Dubbo 协议（包括 Dubbo2 和 Dubbo3）。它可以将 HTTP/HTTPS 请求转换为 Dubbo 协议调用，实现 HTTP 网关到后端 Dubbo 服务的连通。它还支持 Dubbo 服务的接口级路由和参数路由。
2.  **gRPC**：完全支持 gRPC 协

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: Higress 基于 Istio 和 Envoy 构建，但针对云原生网关场景进行了优化。请尝试在本地 Docker 环境中快速部署一个 Higress 实例，并配置一个简单的路由规则，将访问 `/hello` 的流量转发到一个模拟的后端服务（如 httpbin.org）。

### 提示**: 参考 Higress 官方文档的"快速开始"章节，重点查看如何使用 Docker Compose 启动网关，以及如何在控制台或通过 Ingress 资源定义路由规则。

### 

---
## 实践建议

以下是针对 Higress（AI Gateway & API Gateway）的 5-7 条实践建议：

### 1. 利用 AI 插件实现模型提供商的“零成本”切换
Higress 的核心优势在于其 AI 原生能力，特别是对 LLM 的统一代理。不要将大模型供应商（如 OpenAI、Azure、通义千问等）的调用地址硬编码在业务代码中。
*   **具体操作**：在 Higress 中配置全局或特定路由的 AI 插件（如 `ai-proxy`）。在插件配置中设置目标模型提供商。当需要切换供应商或从 A 模型切换到 B 模型时，只需修改网关配置，无需重新部署业务后端代码。
*   **最佳实践**：利用 Higress 的**服务来源** 功能，直接对接阿里云或其他云厂商的 API 网关，实现免鉴权配置和更稳定的连接。

### 2. 配置“语义缓存”以降低 Token 成本并降低延迟
对于 AI 应用，Token 消耗是主要成本，且大模型响应延迟较高。很多用户查询（如“如何做红烧肉”）是高度重复的。
*   **具体操作**：启用 Higress 的**语义缓存** 插件。不同于传统的精确匹配缓存，语义缓存能识别相似问题的意图。
*   **陷阱规避**：注意配置缓存 Key 的生成策略（例如基于用户问题向量的相似度阈值）。如果阈值设置过低，可能会返回过于宽泛的答案；设置过高则命中率低。建议从默认阈值开始测试。

### 3. 实施细粒度的 Prompt 模板管理与注入
为了防止前端直接暴露 Prompt 导致的安全问题，或者为了统一调整 Prompt 逻辑，不应在客户端或后端代码中拼接完整的 Prompt。
*   **具体操作**：使用 Higress 的**Prompt 模板**功能。在网关层定义 System Prompt 或 Few-Shot 模板。业务请求只需发送用户问题，网关层自动将其与预设模板合并后再发送给 LLM。
*   **最佳实践**：结合 Higress 的**参数化配置**，针对不同路由（例如“客服助手”路由和“代码助手”路由）挂载完全不同的 Prompt 模板，实现单一网关实例服务于多种 AI 场景。

### 4. 谨慎处理流式传输（SSE）的超时与缓冲
AI 交互通常使用 Server-Sent Events (SSE) 进行流式响应。标准的 API 网关配置可能会因为等待响应结束而超时，或者尝试缓冲整个流导致内存溢出。
*   **具体操作**：确保在路由配置中开启对流式传输的支持，并调整网关的**请求超时** 时间。对于长文本生成，超时时间应设置得比模型最大生成时间更长。
*   **陷阱规避**：检查网关后端的任何中间件（如 WAF 或日志记录组件），确保它们不会尝试“读取完”整个流再转发，这会破坏流式输出的打字机效果。Higress 原生支持流式转发，但需确认自定义插件未阻塞流。

### 5. 基于用户维度的精准限流与配额管理
大模型 API 调用成本高昂，且容易被恶意攻击或爬虫消耗配额。
*   **具体操作**：配置 Higress 的**限流降级** 功能。不要只针对 IP 限流，更要结合 API Key 或 Header 中的 User ID 进行限流。
*   **最佳实践**：设置“请求级限流”（QPS）和“Token 级限流”（TPM/Token Per Minute）相结合。例如，免费用户每分钟只能消耗 1000 Tokens，付费用户则更高。这需要网关能够估算或解析请求体中的 Token 数量（Higress 的 AI 插件通常支持此功能）。

### 6. 混合负载：AI 流量与传统 API 流量的隔离
如果你的系统中既有传统的 RESTful API，又有新增的 AI Gateway 功能，建议进行逻辑隔离。
*   **具体操作**：在 Higress 中

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI 原生](/tags/ai-%E5%8E%9F%E7%94%9F/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [WASM](/tags/wasm/) / [MCP 协议](/tags/mcp-%E5%8D%8F%E8%AE%AE/) / [LLM](/tags/llm/)
- 场景： [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [DevOps/运维](/scenarios/devops-%E8%BF%90%E7%BB%B4/)

### 相关文章

- [中国开源AI生态的架构选择：DeepSeek之外的构建路径]({{< relref "posts/20260129-blogs_podcasts-architectural-choices-in-chinas-open-source-ai-eco-8.md" >}})
- [Kirara-AI：支持多平台接入的多模态聊天机器人框架]({{< relref "posts/20260129-github_trending-lss233-kirara-ai-0.md" >}})
- [kirara-ai：支持多平台接入的多模态AI聊天机器人]({{< relref "posts/20260129-github_trending-lss233-kirara-ai-0.md" >}})
- [Trinity Large：开源4000亿稀疏MoE模型]({{< relref "posts/20260129-hacker_news-trinity-large-an-open-400b-sparse-moe-model-11.md" >}})
- [Trinity Large：开源4000亿稀疏MoE模型]({{< relref "posts/20260129-hacker_news-trinity-large-an-open-400b-sparse-moe-model-13.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*