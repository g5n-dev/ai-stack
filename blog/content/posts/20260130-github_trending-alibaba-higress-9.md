---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-01-30T17:16:52+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "LLM", "Istio", "Envoy", "WASM", "MCP 协议"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "Higress 是由阿里巴巴开源的、基于 Go 语言开发的**云原生 AI 原生 API 网关**。该项目目前拥有超过 7,400 颗星标，旨在为现代云原生应用和 AI 大模型应用提供统一的流量入口和管理平台。 以下是 Higress 的核心内容总结： **1. 基础架构与定位** Higress 建立在 **Isti"
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
- **星标**: 7,415 (+9 stars today)
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

Higress 是一款基于 Istio 和 Envory 构建的 AI 原生 API 网关，旨在为云原生应用及大模型（LLM）提供统一的流量管理入口。它不仅兼容 Kubernetes Ingress 等传统微服务路由能力，更针对 AI 场景集成了模型调用、MCP 服务器托管及 WASM 插件扩展功能。本文将梳理其核心架构与组件，并重点介绍如何利用它来管理混合流量与集成 AI 代理工具。

---
## 摘要

Higress 是由阿里巴巴开源的、基于 Go 语言开发的**云原生 AI 原生 API 网关**。该项目目前拥有超过 7,400 颗星标，旨在为现代云原生应用和 AI 大模型应用提供统一的流量入口和管理平台。

以下是 Higress 的核心内容总结：

**1. 基础架构与定位**
Higress 建立在 **Istio** 和 **Envoy** 之上，扩展了 WebAssembly (WASM) 插件能力。它将控制平面（配置管理）与数据平面（流量处理）分离。配置变更通过 xDS 协议传播，具备毫秒级延迟和零连接中断的特性，特别适用于 AI 长连接流式响应等场景。

**2. 三大核心功能**
Higress 的设计涵盖了从传统微服务到前沿 AI 应用的广泛需求：
*   **AI 网关**：提供统一 API 接入 30 多家大语言模型（LLM）提供商。核心功能包括协议转换、可观测性、缓存以及安全防护（通过 `ai-proxy`、`ai-statistics` 等插件实现）。
*   **MCP 服务器托管**：托管模型上下文协议（MCP）服务器，使 AI 智能体能够便捷地调用外部工具和服务（例如地图搜索等）。
*   **Kubernetes Ingress**：作为 K8s Ingress 控制器使用，兼容 nginx-ingress 注解，处理传统的微服务路由。

**总结**：Higress 是一款将标准 API 网关能力与 AI 特性深度融合的下一代网关，既支持微服务治理，也专为 LLM 应用和 Agent 工具调用提供了优化支持。

---
## 评论

**总体判断**

Higress 是目前云原生网关领域中将“AI 原生”理念落地最彻底的开源项目之一。它成功地将传统流量治理与 LLM（大语言模型）应用所需的特殊协议处理相结合，不仅是一个高性能的 K8s Ingress 控制器，更是构建 AI Agent 基础设施的关键连接器。

**深入评价依据**

**1. 技术创新性：深耕 WASM 与 AI 协议的深度融合**
*   **事实**：Higress 基于 Istio 和 Envoy 构建，并明确强调 **WebAssembly (WASM)** 插件能力是其核心扩展机制。同时，它集成了 **MCP (Model Context Protocol)** 服务器托管功能。
*   **推断**：传统网关（如 Nginx）扩展依赖 C/Lua 模块，开发门槛高且不安全。Higress 利用 WASM 的沙箱隔离特性，允许开发者使用 Go/Python/JavaScript 等高级语言编写插件，实现了“热更新”而不影响主进程稳定性。更关键的是，它敏锐地捕捉到了 AI 时代的痛点——LLM 的流式输出和 Token 计费与传统 HTTP 请求截然不同。Higress 在网关层直接处理 SSE（Server-Sent Events）流式截断、Token 计数与限流，这种将 AI 业务逻辑下沉到网关层的“AI Native”架构，是其最大的技术差异化亮点。

**2. 实用价值：解决 AI 落地“最后一公里”的连接问题**
*   **事实**：仓库描述指出其具备 **AI Gateway** 功能、**MCP Server Hosting** 以及传统的 **Kubernetes Ingress** 能力。
*   **推断**：在微服务架构中，企业常面临维护多套网关（K8s Ingress + 服务网格 + AI 代理）的困境。Higress 提供了一站式解决方案，既兼容 K8s 标准的 Ingress 资源，又能作为 AI 服务的统一入口。特别是其对 MCP 协议的支持，解决了 AI Agent 调用外部工具时的连接与鉴权难题。对于企业而言，这极大地降低了大模型接入现有业务系统的复杂度，避免了为每个 AI 应用单独开发鉴权、限流和熔断逻辑的重复劳动。

**3. 代码质量与架构：云原生标准与可扩展性**
*   **事实**：项目由阿里巴巴主导，语言为 **Go**，架构明确分离了控制平面与数据平面。
*   **推断**：Go 语言在云原生基础设施领域是事实标准，保证了编译后的二进制文件易于在容器中分发。基于 Envoy 作为数据平面，意味着 Higress 继承了 Envoy 在 C++ 层面的高性能（L3/L4 处理）和低延迟优势。控制面接管 Istio 的部分功能，使得配置下发更加轻量。从文档来看（DeepWiki 提及架构、开发指南等），项目结构清晰，文档覆盖面广，符合成熟开源项目的规范，具备较高的可维护性。

**4. 社区活跃度：背靠大厂，但需警惕独立性**
*   **事实**：星标数 **7,415**（对于基础架构类项目，这是一个相当健康的数字，表明其已被广泛认知）。
*   **推断**：作为阿里云开源产品，其更新频率和核心功能维护有保障。这类项目通常伴随着阿里云的商业化版本（Higress 云原生网关），这意味着企业级特性会持续迭代。然而，社区活跃度的关键在于外部贡献者的占比。目前来看，其生态主要围绕阿里系技术栈，虽然功能强大，但相比 K8s Ingress-nginx 或 APISIX，其第三方插件生态的丰富度仍需时间积累。

**5. 学习价值：理解下一代网关的演进方向**
*   **事实**：提供了详细的 **WASM Plugin System** 和 **Development Guide**。
*   **推断**：对于开发者而言，Higress 是学习“可编程网关”的绝佳范例。通过研究其源码，可以深入理解如何利用 WASM 技术在不重启网关的情况下动态扩展业务逻辑（如自定义鉴权、请求改写）。此外，观察其如何处理 AI 请求的超时、重试以及与 Prompt 模板的结合，能为开发者设计 AI 原生应用提供宝贵的架构参考。

**6. 潜在问题与改进建议**
*   **问题**：基于 Envoy 和 Istio 的架构虽然强大，但配置复杂度（Complexity）天然高于简单的 Nginx 反向代理。
*   **建议**：对于非 K8s 环境或边缘计算场景，Higress 的资源占用可能较重。建议项目方提供更精简的“边缘模式”部署包。此外，AI 部分目前多针对 OpenAI 格式适配，建议加强对国产大模型（如通义千问、文心一言）原生协议的深度适配支持，而不仅仅是通用 HTTP 转发。

**7. 对比优势**
*   **对比 Nginx/Ingress-nginx**：Higress 支持动态配置且无需 Reload，WASM 插件开发比 C 模块更安全、更灵活。
*   **对比 Kong/APISIX**：Higress 深度集成了 K8s 服务网格生态（Istio），在服务发现和南北向流量统一治理上更具云原生优势，且 AI 功能是内置而非通过插件拼凑。
*   **对比云厂商

---
## 技术分析

# Higress 技术深度分析报告

基于提供的 GitHub 仓库信息及阿里云 Higress 的通用技术背景，以下是对该项目的全面深入分析。

---

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 采用了**云原生**技术栈，核心构建于 **Istio** 和 **Envoy** 之上。这种选择决定了其“控制平面与数据平面分离”的架构模式。
*   **底层引擎**：使用 Envoy 作为高性能数据平面，负责处理实际的流量（L7 路由、负载均衡、执行插件）。
*   **控制平面**：基于 Istio 进行扩展，接管了 Istio 的 Ingress Gateway 功能，并进行了简化和增强，使其更适合 API 网关的场景。
*   **编程语言**：**Go**。控制平面使用 Go 开发，利用其高并发和云原生生态优势；插件支持 C++ (Envoy 原生)、Go (通过 Proxy-WASM) 和多语言 WASM。

### 核心模块与关键设计
1.  **AI 网关模块**：这是 Higress 最具差异化的模块。它不仅仅是流量转发，还集成了针对大语言模型（LLM）的协议转换（如将 OpenAI 协议转为通义千问协议）、Token 计费与流式处理。
2.  **WASM 插件系统**：通过 **Proxy-WASM** 标准，允许用户使用 Go/C++/Rust 等语言编写插件，并动态加载到 Envoy 中。这解决了传统 Envoy 插件（C++ Filter）开发门槛高、编译复杂、需要重启网关的痛点。
3.  **MCP (Model Context Protocol) 服务器托管**：针对 AI Agent 场景，Higress 内置了对 MCP 协议的支持，能够作为工具提供方，将后端 API 暴露给 AI Agent 调用，解决了 AI 应用与后端服务集成的连接问题。

### 技术亮点与创新点
*   **AI Native (AI 原生)**：Higress 是业界较早明确提出“AI 网关”概念的通用网关。它将 AI 服务的特性（如流式响应 SSE、上下文缓存、Key 管理）内置到网关层面，而不是作为事后补充。
*   **热更新能力**：基于 xDS 协议的配置下发和 WASM 插件的动态加载，实现了配置和业务逻辑的毫秒级生效，且不断连。这对于 AI 长连接场景至关重要。

### 架构优势分析
*   **低延迟**：数据平面 Envoy 采用 C++ 零拷贝技术，配合 WASM 的沙箱隔离（性能损耗控制在可接受范围内），提供了极高的转发性能。
*   **生态兼容**：完全兼容 K8s Ingress 和 Istio API，降低了从传统架构迁移的门槛。

---

## 2. 核心功能详细解读

### 主要功能与使用场景
1.  **AI 流量治理**：
    *   **统一接入**：将不同 LLM 提供商（OpenAI, Anthropic, 通义千问等）的 API 统一封装。
    *   **Token 管理**：基于 Token 消耗量的实时限流和计费统计。
    *   **提示词管理**：在网关层进行 Prompt 模板注入或敏感词过滤。
2.  **MCP 系统集成**：
    *   作为 AI Agent 的“工具箱”，将企业内部 API 转换为 MCP 协议，使得 Agent 能够安全、受控地调用企业数据。
3.  **传统 API 网关**：
    *   K8s Ingress Controller、金丝雀发布、负载均衡、认证鉴权。

### 解决的关键问题
*   **AI 服务的碎片化**：企业对接多个大模型时，SDK 各异，Higress 提供了统一的接入层。
*   **AI 应用的可观测性与安全**：传统网关只能看到 HTTP 流量，看不到 Token 级别的消耗。Higress 填补了这一空白，提供了针对 AI 语义的监控和审计。

### 与同类工具对比
| 特性 | Higress | Kong | APISIX | Nginx |
| :--- | :--- | :--- | :--- | :--- |
| **AI 原生支持** | **强 (内置 LLM 路由/MCP)** | 弱 (需插件) | 弱 (需插件) | 无 |
| **WASM 支持** | **强 (默认支持, Go 生态好)** | 有 (主要针对 JS/Go) | 有 | 实验性/复杂 |
| **K8s 集成** | **强 (基于 Istio)** | 强 (Kong Ingress) | 强 | 需配合 Ingress Controller |
| **架构基础** | Envoy + Istio | Nginx/OpenResty | etcd + Lua (APISIX) / Go | C++ |

### 技术实现原理
*   **流式转发**：在处理 SSE (Server-Sent Events) 时，Higress 在 Envoy 层进行流式缓冲和转发，确保不阻塞数据流，同时支持在流式数据中插入元数据（如计费 ID）。
*   **协议转换**：通过 WASM 插件拦截 HTTP 请求/响应，修改 JSON Body 结构，实现例如 OpenAPI 格式到其他厂商格式的动态转换。

---

## 3. 技术实现细节

### 关键技术方案
*   **xDS 协议优化**：Higress 控制平面与 Envoy 数据平面通过 xDS (v2/v3) 通信。为了应对大规模配置，Higress 对 xDS 增量推送进行了优化，减少了配置变更时的资源消耗。
*   **WASM 虚拟机**：集成了 **Wasmtime** 或 **V8** 引擎。为了解决 WASM 的内存隔离问题，Higress 实现了精细的内存管理和插件沙箱限制，防止单个插件崩溃导致整个网关进程挂掉。

### 代码组织与设计模式
*   **Kubernetes Operator 模式**：控制平面大量使用 K8s CRD (Custom Resource Definition) 来定义网关配置（如 `Ingress`, `Gateway`, `WasmPlugin`）。
*   **插件过滤器链**：在数据平面，插件被组织成 Filter Chain。每个 WASM 插件被挂载到 Envoy 的 HTTP Filter 生命周期中。

### 性能优化与扩展性
*   **多线程并发**：Envoy 本身是多线程架构，Higress 充分利用了这一点。但在 WASM 插件中，由于内存隔离，需要注意避免锁竞争或共享状态，Higress 推荐使用 Redis 等外部存储做状态共享。
*   **配置懒加载**：在处理大量路由规则时，Higress 支持路由表的优化查找算法，避免线性遍历带来的性能下降。

### 技术难点与解决方案
*   **难点**：WASM 插件的性能损耗。
*   **方案**：Higress 社区持续优化 WASM 的 Host Interface，并提倡将复杂逻辑（如 SQL 查询）下沉到后端服务，网关仅做轻量级逻辑处理。
*   **难点**：AI 流式响应的中间修改。
*   **方案**：实现了流式数据的流式处理管道，而非全量缓冲后再转发，降低了首字节延迟（TTFB）。

---

## 4. 适用场景分析

### 适合的项目
*   **大模型应用 (RAG/Agent)**：需要对接多个 LLM 厂商，且需要对 API 调用进行统一鉴权、限流和 Prompt 注入的场景。
*   **微服务网关**：基于 Kubernetes 的云原生架构，需要高性能 API 网关的企业。
*   **SaaS 平台**：需要为不同租户提供隔离的 API Key 管理和流量统计。

### 最有效的情况
*   当你需要**在不修改后端业务代码**的情况下，为 AI 应用增加统一的鉴权、计费或协议转换能力时。
*   当你需要将企业内部服务快速**暴露给 AI Agent**（通过 MCP 协议）时。

### 不适合的场景
*   **极低延迟的纯内存转发**：如果业务对延迟极其敏感（如高频交易），WASM 插件的开销和 Envoy 的复杂度可能不如纯 Nginx + C Module。
*   **非 K8s 环境**：虽然支持 Docker 部署，但 Higress 的强大功能主要依托于 K8s 体系，在虚拟机或物理机部署的运维成本较高。

### 集成方式
*   **Ingress 模式**：替换 K8s 原生 Ingress Controller。
*   **Sidecar 模式**：虽然不如 Istio 原生常用，但理论上可以作为 Service Mesh 的数据平面组件。

---

## 5. 发展趋势展望

### 技术演进方向
*   **更深度的 AI 集成**：从简单的协议转换，向语义缓存、Prompt 优化建议、甚至向量检索网关（连接 Vector DB）演进。
*   **WASM 生态标准化**：推动网关插件标准的统一，使得一个 WASM 插件可以在 Higress、Istio、Kong 等不同网关间通用。

### 社区反馈与改进空间
*   **文档与易用性**：对于初学者，WASM 插件的开发调试环境搭建仍有一定门槛，IDE 支持和调试工具需进一步完善。
*   **资源消耗**：相比 Nginx，Envoy + WASM 的内存占用较高，在超大规模（百万级 QPS）场景下的资源调优是持续课题。

### 与前沿技术结合
*   **eBPF**：未来可能在底层网络路径上结合 eBPF 进行更早的流量拦截或观测，进一步提升性能。
*   **Service Mesh (Istio) 深度融合**：随着 Istio 的 Ambient Mesh 模式的发展，Higress 可能会探索无 Sidecar 的 API 网关形态。

---

## 6. 学习建议

### 适合的开发者水平
*   **中级**：熟悉 Go 语言，了解 Docker 和 Kubernetes 基础。
*   **高级**：深入理解 HTTP 协议、微服务架构、WASM 概念及 Envoy 原理。

### 学习路径
1.  **基础篇**：学习如何使用 Docker Compose 或 Helm Chart 部署 Higress，配置基本的路由转发。
2.  **进阶篇**：学习编写 WASM 插件（推荐使用 Go），实现一个简单的 Header 修改或鉴权插件。
3.  **架构篇**：阅读源码中的 `pkg` 目录，理解控制平面如何通过 xDS 驱动 Envoy，以及 Ingress 资源如何转换为路由配置。

### 实践建议
*   尝试搭建一个包含 OpenAI 接口的代理服务，体验 Higress 的 AI 网关特性。
*   使用官方的 `wasm-go-sdk` 开发一个自定义插件，并在本地热加载测试。

---

## 7. 最佳实践建议

### 如何正确使用

---
## 代码示例




```python
# 示例1：使用 Higress 进行流量路由
def higress_routing_example():
    """
    场景：根据请求头将流量路由到不同版本的服务
    例如：将 10% 的流量路由到新版本服务（金丝雀发布）
    """
    from higress import Gateway, RouteRule
    
    # 创建网关实例
    gateway = Gateway()
    
    # 定义路由规则
    rule = RouteRule(
        match={
            "headers": {
                "x-canary": "true"  # 匹配带特定头的请求
            }
        },
        route={
            "cluster": "service-v2",  # 新版本服务
            "timeout": "5s"
        }
    )
    
    # 添加默认路由规则
    default_rule = RouteRule(
        route={
            "cluster": "service-v1",  # 默认旧版本
            "timeout": "5s"
        }
    )
    
    # 应用路由配置
    gateway.add_route(rule)
    gateway.add_route(default_rule)
    
    return gateway
```




```python
# 示例2：Higress 插件配置（限流）
def higress_rate_limit_example():
    """
    场景：为 API 配置限流保护
    例如：限制每个 IP 每分钟最多 100 次请求
    """
    from higress import Plugin, RateLimitConfig
    
    # 创建限流插件配置
    rate_limit = Plugin(
        name="rate-limit",
        config=RateLimitConfig(
            limit_by="ip",      # 按 IP 限流
            queries_per_minute=100,  # 每分钟 100 次
            burst_size=10       # 允许突发 10 个请求
        )
    )
    
    # 应用插件到特定路由
    route_config = {
        "match": {"path": "/api/v1/*"},
        "plugins": [rate_limit]
    }
    
    return route_config
```




```python
# 示例3：Higress 服务发现与负载均衡
def higress_service_discovery_example():
    """
    场景：动态服务发现与负载均衡配置
    例如：从 Nacos 注册中心发现服务实例并配置轮询负载均衡
    """
    from higress import ServiceDiscovery, LoadBalancer
    
    # 配置服务发现
    discovery = ServiceDiscovery(
        type="nacos",  # 使用 Nacos 注册中心
        config={
            "server_addr": "127.0.0.1:8848",
            "namespace": "public",
            "service_name": "user-service"
        }
    )
    
    # 配置负载均衡策略
    lb = LoadBalancer(
        policy="round_robin",  # 轮询策略
        health_check={
            "active": {
                "timeout": "5s",
                "interval": "10s",
                "unhealthy_threshold": 3
            }
        }
    )
    
    # 应用配置
    service_config = {
        "discovery": discovery,
        "load_balancer": lb
    }
    
    return service_config
```


---
## 案例研究


### 1：阿里巴巴淘天集团

 1：阿里巴巴淘天集团

**背景**: 淘天集团拥有海量的业务系统和复杂的微服务架构，涵盖淘宝、天猫等核心电商业务。随着业务向云原生架构全面迁移，传统的基于 Nginx 的 Ingress Controller 在面对大规模流量、复杂的路由逻辑以及频繁的配置变更时，逐渐显露出性能瓶颈和扩展性不足的问题。

**问题**: 在大促场景（如双11）下，网关层面临极高并发挑战。原有网关架构在处理每秒百万级 QPS 时存在延迟抖动，且热配置生效时间较长（通常需要分钟级），无法满足电商业务快速迭代的弹性需求。此外，传统网关对 WASM（WebAssembly）和 gRPC 协议的支持不够完善，限制了新业务的接入效率。

**解决方案**: 阿里巴巴基于开源 Higress 项目，并结合内部业务需求进行了深度定制与优化。Higress 是一个云原生 API 网关，集成了 K8s Ingress 和 API 管理能力。淘天集团利用 Higress 的高性能网络处理能力（基于 C++ 和 Envoy），实现了全链路流量治理。通过 Higress 的热更新技术，实现了配置变更的毫秒级生效，并利用其强大的插件市场（特别是 WASM 插件）来支持鉴权、限流、流量镜像等复杂逻辑。

**效果**: 成功支撑了双11等超大流量场景，网关峰值 QPS 达到数百万级别，P99 延迟显著降低。配置热更新能力使得业务变更效率提升了 90% 以上，实现了从“天级”发布到“分钟级”甚至“秒级”发布的跨越。同时，统一的网关层极大地简化了运维复杂度，降低了服务器资源成本。

---



### 2：杭州某知名互联网科技公司（AI 业务方向）

 2：杭州某知名互联网科技公司（AI 业务方向）

**背景**: 该公司专注于生成式 AI（AIGC）应用开发，推出了多款基于大语言模型（LLM）的智能对话和内容生成工具。其业务架构后端对接多家不同的模型提供商（如 OpenAI、阿里云通义千问、Llama 等），前端则面向 Web 端和移动端用户。

**问题**: 在接入大模型时，面临严重的协议转换难题。不同的模型厂商使用不同的 API 接口标准（如 OpenAI 格式 vs. 标准 HTTP 格式），导致客户端需要维护多套调用逻辑。此外，大模型调用成本高昂，且缺乏统一的流量控制和计费统计手段，难以对 API 进行精细化的权限管理和数据缓存。

**解决方案**: 该技术团队引入 Higress 作为 AI API 网关。利用 Higress 原生支持的 AI 特性，特别是针对 LLM 的协议转换能力，将后端异构的模型接口统一转换为标准的 OpenAI 格式，供前端统一调用。同时，利用 Higress 的插件机制实现了 Token 统计、基于 Prompt 的缓存（减少重复调用成本）以及语义路由（根据用户问题智能分发到不同模型）。

**效果**: 实现了后端模型服务的无感切换和统一接入，前端开发效率提升 50%。通过 Prompt 缓存策略，成功降低了约 30% 的 Token 消耗成本。统一的网关层还提供了清晰的调用监控和日志，帮助团队快速定位模型调用中的异常，极大地提升了系统的稳定性和可观测性。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|----------------|------|-------|
| 性能 | 基于Envoy和Istio，高性能，支持Wasm插件扩展 | 基于OpenResty，性能较高，但扩展性依赖Lua | 基于OpenResty，性能优异，支持动态路由 |
| 易用性 | 提供控制台和Kubernetes集成，配置灵活 | 控制台功能丰富，但配置较复杂 | 控制台简洁，支持动态配置，学习曲线较平缓 |
| 成本 | 开源免费，商业支持需付费 | 开源免费，企业版收费 | 开源免费，企业版收费 |
| 扩展性 | 支持Wasm插件，扩展性强 | 支持Lua插件，扩展性一般 | 支持Lua和Go插件，扩展性较强 |
| 社区 | 阿里背书，社区活跃度中等 | 社区成熟，资源丰富 | 社区活跃，国内支持较好 |

### 优势分析

- 优势1：深度集成Kubernetes和Istio，适合云原生环境。
- 优势2：支持Wasm插件，扩展性和性能优于传统Lua插件。
- 优势3：提供开箱即用的控制台，降低运维复杂度。

### 不足分析

- 不足1：社区生态相对Kong和APISIX较小，第三方插件较少。
- 不足2：文档和案例不如成熟方案丰富，学习成本较高。
- 不足3：商业支持依赖阿里云服务，可能存在厂商锁定风险。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 WASM 的插件扩展与自定义开发

**说明**:
Higress 深度集成了 WASM (WebAssembly) 技术，允许开发者使用 C/C++、Go、Rust 或 JavaScript 等多种语言编写高性能的插件。相比于传统的 Lua 脚本或硬编码方式，WASM 插件提供了更好的隔离性、安全性和开发便利性，且支持热加载，无需重启网关即可生效。

**实施步骤**:
1. 访问 Higress 官方 GitHub 仓库，参考 `wasm-plugins` 目录下的示例代码。
2. 根据业务需求选择合适的语言编写插件逻辑（如使用 Go 编写鉴权逻辑）。
3. 使用 Higress 提供的工具链或 Docker 镜像将代码编译为 WASM 文件（`.wasm`）。
4. 在 Higress 控制台或通过 CRD 配置将 WASM 文件上传并关联到特定的网关路由或全局作用域。

**注意事项**: 
编写 WASM 插件时应注意内存资源的限制，避免在插件中进行无限循环或阻塞操作，以防拖垮网关性能。

---

### 实践 2：服务保护与熔断降级配置

**说明**:
在微服务架构中，后端服务的波动直接影响客户端体验。Higress 继承了 Sentinel 的强大流量控制能力，支持秒级的自动熔断、降级和限流。通过合理配置，可以防止“雪崩效应”，确保核心链路的稳定性。

**实施步骤**:
1. 在网关配置中识别关键的后端服务接口。
2. 配置熔断规则，例如：当某个服务的响应时间超过 500ms 或错误率达到 50% 时，触发熔断。
3. 设置降级策略，定义熔断触发后返回的默认内容（如返回默认 JSON 或静态页面）。
4. 利用 Higress 控制台实时监控熔断状态，并在服务恢复后配置自动恢复探测。

**注意事项**: 
熔断阈值的设置需要基于历史压测数据或线上实际流量进行估算，过于敏感的阈值可能导致正常请求被拦截。

---

### 实践 3：金丝雀发布与流量标签路由

**说明**:
Higress 支持基于 Header、Cookie 或查询参数的高级路由匹配。利用这一特性，可以实现灰度发布，即让特定用户（如内部员工或特定 ID 的用户）访问新版本服务，而其余流量继续访问老版本，从而降低上线的风险。

**实施步骤**:
1. 在服务注册中心（如 Nacos）部署新版本的服务应用，并打上版本标签（如 `v2`）。
2. 在 Higress 中创建或修改路由规则，添加匹配条件。例如，设置 HTTP Header `x-user-group: internal`。
3. 配置路由目标指向带有 `v2` 标签的服务版本。
4. 逐步扩大流量匹配规则（例如从特定用户 ID 扩大到 10% 的随机流量），直至全量切换。

**注意事项**: 
灰度发布期间，必须确保新旧版本的数据兼容性，特别是数据库结构的变更，应遵循“向前兼容”的原则。

---

### 实践 4：全链路安全认证（JWT/OIDC）

**说明**:
Higress 内置了对 JSON Web Token (JWT) 验证和 OpenID Connect (OIDC) 的原生支持。通过在网关层统一处理认证逻辑，可以剥离后端微服务的安全负担，使业务服务专注于业务逻辑，同时确保未授权的流量无法进入内网。

**实施步骤**:
1. 配置鉴权插件，选择“Jwt Auth”或“OIDC”类型。
2. 配置 JWKS (JSON Web Key Set) 端点地址，用于验证签名的公钥。
3. 设置 `from-to` 权限，指定哪些路径需要鉴权，哪些路径（如登录接口）允许匿名访问。
4. 在网关处将用户信息解析后透传给后端服务（例如通过 Header 传递 UserID），以便后服务进行业务逻辑处理。

**注意事项**: 
务必确保 HTTPS 的使用，防止 Token 在传输过程中被窃取。同时，要定期轮换签名密钥。

---

### 实践 5：高精度可观测性与日志集成

**说明**:
Higress 提供了强大的日志扩展能力，不仅支持标准 access log，还支持将日志直接推送到 Kafka、SLS 或其他日志系统。通过结构化的日志输出，配合 Prometheus 监控指标，可以实现从流量入口到后端服务的全链路追踪。

**实施步骤**:
1. 在 Higress 全局配置中开启“日志采集”插件。
2. 配置日志格式，建议使用 JSON 格式以便解析，包含 `upstream_host`、`response_code`、`request_time` 等关键字段。
3. 集成链路追踪（如 SkyWalking 或 Jaeger），在 Higress 中配置 Trace 采样率。
4. 设置告警规则，针对 4

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/2 与 HTTP/3 (QUIC) 协议

**说明**:
Higress 作为高性能网关，利用 HTTP/2 的多路复用特性可以显著减少 TCP 连接建立开销，解决 HTTP/1.1 的队头阻塞问题。HTTP/3 (QUIC) 则进一步解决了 TCP 层的队头阻塞，并在弱网环境下提供更低的连接建立延迟和更好的丢包恢复能力。

**实施方法**:
1. 在监听器配置中，确保协议版本包含 `h2` 和 `HTTP/3`。
2. 配置 TLS 证书，HTTP/2 和 HTTP/3 均依赖 TLS。
3. 调整网关配置，开启 QUIC 协议支持（通常在 `config.yaml` 或特定网关路由插件中设置）。
4. 客户端需支持对应协议（现代浏览器均支持，gRPC 客户端需配置）。

**预期效果**:
在高并发或弱网环境下，请求延迟可降低 20%-40%，并发连接数承载能力提升 30% 以上。

---

### 优化 2：配置全链路超时与重试策略

**说明**:
默认的超时设置可能不适合所有业务场景。过长的超时会导致请求堆积（线程或协程长时间挂起），耗尽网关资源；过短则可能导致误报。合理的超时与退避重试机制能保障系统整体稳定性，防止雪崩。

**实施方法**:
1. **连接超时**: 建议设置为 2-5 秒，避免长时间无法建立连接。
2. **请求超时**: 根据后端服务 P99.9 耗耗设置，通常建议 10-30 秒。
3. **路由配置**: 在 Higress 路由规则中明确配置 `timeout` 字段。
4. **重试策略**: 配置指数退避重试，限制最大重试次数（如 2-3 次），仅对幂等请求（GET、HEAD）开启重试。

**预期效果**:
减少因后端慢响应导致的资源耗尽风险，提升系统可用性至 99.9% 以上，降低平均响应延时波动。

---

### 优化 3：启用 Wasm 插件的高效隔离与缓存

**说明**:
Higress 支持 Wasm 插件扩展业务逻辑。Wasm 运行时（如 Wasmtime 或 WASM Edge）的性能直接影响请求处理时延。不当的内存隔离或频繁的编译加载会拖累网关性能。优化 Wasm 运行时配置和利用 AOT（Ahead-of-Time）编译至关重要。

**实施方法**:
1. 使用 Wasm 的 AOT 编译版本（如果运行时支持），减少解释执行开销。
2. 合理控制 Wasm 虚拟机的内存限制，防止内存溢出导致 OOM 杀死网关进程。
3. 避免在插件请求处理路径中进行重量级计算或阻塞 I/O，尽量使用异步非阻塞模式。
4. 复用 Wasm 虚拟机实例，避免每次请求都创建新的 VM。

**预期效果**:
Wasm 插件执行延迟可降低 10%-50%，显著降低 CPU 开销，提升网关单核 RPS（每秒请求数）。

---

### 优化 4：优化后端服务连接池与健康检查

**说明**:
网关与后端服务之间的连接管理是性能瓶颈之一。过小的连接池会导致排队等待，过大的连接池会浪费资源。同时，快速剔除不健康的后端实例能避免无效请求转发。

**实施方法**:
1. **连接池调优**: 根据后端服务处理能力，调整 `maxRequestsPerConnection` 或连接池大小。对于短连接业务，适当增大连接池；对于长连接（如 gRPC），复用连接。
2. **健康检查**: 配置主动健康检查，设置合理的 `interval`（间隔）和 `timeout`。
3. **熔断降级**: 配置熔断器，当后端错误率或延迟超过

---
## 学习要点

- Higress 是阿里开源的基于 Istio 的云原生 API 网关，深度集成了 K8s 与 Dubbo/Nacos 等微服务生态
- 提供开箱即用的流量管理能力，支持 HTTP/gRPC/Dubbo 协议及金丝雀发布、蓝绿部署等高级路由策略
- 内置 WAF 安全防护模块，可抵御 SQL 注入、XSS 等常见 Web 攻击，并支持自定义安全规则
- 通过插件市场扩展功能，开发者可使用 Go/Wasm/Python 编写自定义插件，实现灵活的流量处理逻辑
- 兼容 Ingress/Gateway API 标准，支持从 Nginx/Kong 等传统网关平滑迁移，降低迁移成本
- 具备高性能代理能力，单核可处理数万 QPS，延迟在毫秒级，适合高并发生产环境
- 提供可视化控制台与 Prometheus 监控集成，简化网关运维与流量观测工作


---
## 学习路径

## 学习路径

### 阶段 1：入门基础与核心概念

**学习内容**:
- 云原生网关基础：理解 API 网关在微服务架构中的定位、作用以及流量管理的重要性。
- Higress 概览：了解 Higress 的开源背景（基于阿里云 Gateway 产品）、其与 Istio 和 Envoy 的关系，以及 Higress 的核心特性（如高可用、低延时）。
- 基础架构：掌握 Higress 的核心组件，包括控制面和数据面 的基本分工。
- 部署与安装：学习如何在 Kubernetes (K8s) 集群中使用 Helm 或 kubectl 部署 Higress，以及如何使用 Docker 进行本地快速体验。

**学习时间**: 1-2周

**学习资源**:
- Higress 官方 GitHub 仓库 (README 文档)
- Higress 官方网站文档 (快速开始部分)
- Kubernetes 基础操作教程

**学习建议**:
- 在开始前，建议先复习 Docker 和 Kubernetes 的基本操作，特别是 Pod、Service 和 Ingress 的概念。
- 动手实践是关键，务必在本地或测试环境的 K8s 集群中成功跑通一个 Hello World 示例。
- 对比学习：如果熟悉 Nginx 或传统 Ingress Controller，可以对比其配置方式，理解 Higress 的差异。

---

### 阶段 2：流量治理与路由配置

**学习内容**:
- 路由配置：深入学习如何配置域名路由、路径匹配、Header 匹配等 HTTP 路由规则。
- 服务发现：掌握如何将 Higress 与注册中心（如 Nacos, Consul, K8s Service）对接，实现后端服务的自动发现。
- 负载均衡策略：学习轮询、随机、一致性哈希等负载均衡算法的配置与应用场景。
- 流量管理：掌握金丝雀发布、蓝绿发布、Header 重写/重定向、超时与重试机制。
- Ingress 与 Gateway API：学习如何通过 Kubernetes Ingress 或 Gateway API CRD 资源来管理 Higress 配置。

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 流量管理章节
- Envoy Route Configuration 官方文档 (用于理解底层原理)
- Higress 官方示例库

**学习建议**:
- 尝试模拟真实的业务场景，例如将一个简单的 Web 应用接入 Higress，并配置基于 Header 的灰度发布。
- 重点理解 "Wasm 插件" 的概念，这是 Higress 的核心扩展能力之一，虽然深入开发在下一阶段，但需在此阶段了解如何安装和启用现成的插件。
- 遇到配置问题时，学会查看 Higress 的日志和 Pod 状态进行排查。

---

### 阶段 3：安全防护与可观测性

**学习内容**:
- 安全认证：学习如何在网关层实现鉴权，包括 Basic Auth、JWT 验证、API Key 以及 OAuth2.0 集成。
- 访问控制：掌握 IP 黑白名单、CORS 跨域配置以及对特定 API 的限流熔断策略。
- 可观测性集成：学习如何配置 Prometheus 监控指标、集成 Tracing (如 SkyWalking, Zipkin) 以及配置访问日志输出。
- 全局配置：理解全局 TLS/HTTPS 证书管理、Upstream Keep-alive 等全局网络设置。

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 安全与可观测性章节
- Prometheus 与 Grafana 基础教程
- SkyWalking 或 Zipkin 使用指南

**学习建议**:
- 安全方面，建议先从简单的 Basic Auth 和 IP 访问控制做起，再尝试对接企业级的 IdP (Identity Provider)。
- 搭建一套简单的监控体系（Grafana + Prometheus），观察 Higress 的 QPS、延迟和成功率等关键指标。
- 尝试配置一个全链路追踪，观察请求从网关进入到后端服务的完整调用链。

---

### 阶段 4：插件开发与高级定制

**学习内容**:
- Wasm (WebAssembly) 原理：深入理解 Wasm 为什么适合网关扩展，以及 Wasm 在 Envoy 中的运行机制。
- Go 插件开发：学习使用 Higress 提供的 Go SDK 开发自定义 Wasm 插件，实现自定义的请求/响应处理逻辑。
- 插件生命周期管理：学习如何插件的配置热更新、版本管理以及调试技巧。
- 高级服务治理：探索更复杂的治理场景，如服务熔断降级、全链路灰度以及多集群容灾。
- 性能调优：了解 Higress 的性能瓶颈，学习如何通过配置调整（如连接池、缓冲区大小）来优化吞吐量。

**学习时间**: 3-4周

**学习资源**:

---
## 常见问题


### 1: Higress 是什么？它与阿里巴巴和云原生社区有什么关系？

1: Higress 是什么？它与阿里巴巴和云原生社区有什么关系？

**A**: Higress 是一个基于阿里内部多年实践沉淀的下一代云原生 API 网关。它是在 2022 年由阿里巴巴开源并捐赠给云原生社区的项目。Higress 的前身是阿里巴巴内部广泛使用的 HSF Gateway 和 Tengine Gateway。它建立在 Envoy 和 Istio 之上，旨在提供标准、高效、云原生的入口流量管理，同时兼容 Kubernetes Ingress 以及传统的 Nginx Ingress 注解，是阿里云云原生网关的开源版本。

---



### 2: Higress 与 Nginx、APISIX 或 Kong 等传统网关相比有什么核心优势？

2: Higress 与 Nginx、APISIX 或 Kong 等传统网关相比有什么核心优势？

**A**: Higress 的核心优势主要体现在以下几个方面：
1.  **技术架构先进**：底层基于 C++ 编写的高性能 Envoy 代理，相比基于 Lua (OpenResty) 的网关（如 Kong、APISIX），在处理高并发和长连接（如 Dubbo、gRPC）时内存占用更低，性能更稳定。
2.  **深度集成 Istio**：Higress 天然支持 Istio，可以作为 Ingress Controller 接入服务网格，实现从南北向（入口流量）到东西向（服务间流量）的统一管理，这是许多传统网关不具备的。
3.  **安全与插件生态**：它支持 WAF（Web 应用防火墙）功能，并且兼容 Nginx Ingress 注解，降低了用户从传统 Nginx 迁移的成本。同时，它支持 WASM（WebAssembly）插件，允许使用多种语言（如 Go、Python、JS）编写业务逻辑，扩展性更强。

---



### 3: Higress 是否支持从 Nginx 或 Kong 平滑迁移？迁移成本高吗？

3: Higress 是否支持从 Nginx 或 Kong 平滑迁移？迁移成本高吗？

**A**: 是的，Higress 非常重视迁移的平滑性，并设计了专门的工具来降低成本。
1.  **Nginx 兼容**：Higress 实现了 Kubernetes Ingress Nginx 注解的兼容。这意味着你现有的 Kubernetes Ingress YAML 文件通常不需要修改或只需少量修改即可直接在 Higress 上运行。
2.  **配置转换工具**：对于使用 Nginx 原生配置文件的用户，Higress 提供了 `nginx2higress` 工具，可以将 Nginx 的 `nginx.conf` 自动转换为 Higress 的配置。
3.  **协议支持**：除了 HTTP，Higress 还原生支持 Dubbo 和 gRPC，这对于使用微服务架构（特别是 Java 生态）的用户来说，比仅支持 HTTP 的网关更具吸引力。

---



### 4: Higress 如何处理流量管理和安全防护？

4: Higress 如何处理流量管理和安全防护？

**A**: Higress 提供了企业级的流量管理和安全能力：
1.  **流量管理**：支持基于 Header、Cookie、URL 参数等条件的灰度发布（金丝雀发布）和蓝绿发布。支持流量镜像，将生产流量复制到测试环境进行验证。
2.  **安全防护**：内置了基础的安全能力，并集成了 WAF 插件，可以防御 SQL 注入、XSS 等常见 Web 攻击。支持 IP 黑白名单、JWT 认证以及 OIDC（OpenID Connect）单点登录集成。
3.  **全链路路由**：支持根据 HTTP Header 或参数进行标签路由，这在微服务调用链路中非常关键。

---



### 5: Higress 支持 Dubbo 服务吗？它是如何做到的？

5: Higress 支持 Dubbo 服务吗？它是如何做到的？

**A**: 支持。这是 Higress 区别于许多开源 API 网关的一大特色。Higress 原生支持 Apache Dubbo（包括 Dubbo2 和 Dubbo3 协议）。
它通过将 HTTP 请求转换为 Dubbo 协议，实现了 HTTP 转 Dubbo 的反向代理能力。这使得前端应用（如 Web 或移动端）可以直接通过 HTTP/HTTPS 调用后端的 Java Dubbo 服务，而无需在中间加一层转换层，大大简化了异构系统间的调用架构。

---



### 6: Higress 的插件机制是怎样的？我可以用 Python 或 Go 写插件吗？

6: Higress 的插件机制是怎样的？我可以用 Python 或 Go 写插件吗？

**A**: Higress 采用了基于 WASM（WebAssembly）的插件架构，这是一个非常灵活和现代化的设计。
1.  **多语言支持**：由于 WASM 的特性，开发者可以使用 Go、C++、Rust、JavaScript (AssemblyScript) 甚至 Python 编写插件逻辑，然后编译为 WASM 文件供 Higress 加载。
2.  **动态加载**：插件支持热加载，不需要重启网关服务即可生效。
3.  **插件市场**：Higress 官方提供了一个插件市场，包含了常见的认证、限流、可观测性等插件，用户可以直接一键安装使用。这解决了传统网关（如 Nginx）必须使用 Lua 编写插件的学习门槛问题。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 基于 Higress 的官方 Docker 镜像，编写一个 `docker-compose.yml` 文件，启动一个包含 Higress 网关的本地环境。要求配置一个简单的 HTTP 路由，将访问 `/example` 的流量转发到 `httpbin.org` 的 `/get` 接口。

### 提示**:

### 需要关注 Higress 容器所需的必要环境变量（如 `ALIYUN_AK_SK` 是否在本地必须）。

---
## 实践建议

以下是针对 Higress（阿里云开源的 AI Native API 网关）的 6 条实践建议：

### 1. 利用 WASM 插件实现 AI 请求的“无损”修改
**场景**：你需要对发送给 LLM（如 GPT-4, 通义千问）的 Prompt 进行注入（例如添加系统预设词）或对返回结果进行脱敏，但不想修改后端服务代码。
**建议**：编写 Go 或 Rust 的 WASM 插件，配置在 `Global` 或 `Route` 级别。利用 Higress 的 `RequestBodyFilter` 和 `ResponseBodyFilter` 生命周期钩子。
**最佳实践**：在插件中针对 `/v1/chat/completions` 等标准 OpenAI 接口路径做 JSON 解析，修改 `messages` 数组。
**常见陷阱**：处理流式响应时，务必正确处理 SSE（Server-Sent Events）的数据帧格式（`data: [JSON]\n\n`），否则客户端会因为解析错误而断开连接。

### 2. 配置“模型提供商”服务以统一管理 Token
**场景**：企业内部同时使用多家大模型（OpenAI, Azure, 通义千问, 文心一言），希望统一入口并避免在客户端暴露多个 API Key。
**建议**：使用 Higress 的 **AI Provider** 功能（或 InferenceRoute 配置），在网关层面集中配置各厂商的 API Key。
**最佳实践**：在路由配置中，将 `model` 参数映射重写。例如，客户端请求 `gpt-3.5`，网关自动映射到供应商的 `qwen-turbo`，实现模型切换对业务代码透明。
**常见陷阱**：注意不同厂商的 Token 计费方式不同，Higress 的原生计费统计主要基于请求量，精确的成本控制需要在插件层进行二次计算。

### 3. 启用基于语义的“超时”与“重试”策略
**场景**：大模型推理耗时较长且不稳定，传统的 HTTP 网关超时配置（如 1 秒）会导致请求直接报错。
**建议**：针对 AI 推理路由，显式调大 `upstream response_timeout`（建议设置为 60s - 120s），并配置特定的重试策略。
**最佳实践**：仅在网络层错误（如 502, 503）或特定的 LLM 报错（如 Rate Limit 429）时进行重试，避免在模型生成内容失败时盲目重试导致产生双倍费用。
**常见陷阱**：在开启流式传输时，如果网关与后端建立连接时间过长，可能会导致连接被操作系统或中间防火墙断开，需确保 TCP Keep-Alive 设置合理。

### 4. 实施细粒度的“提示词”防火墙
**场景**：防止用户通过 Prompt Injection（提示词注入）攻击套取系统的 System Prompt 或执行恶意指令。
**建议**：部署内容审核类 WASM 插件，在请求转发给 LLM 之前拦截。
**最佳实践**：结合本地敏感词库与外部审核 API（如阿里云内容安全），在 `RequestBodyFilter` 阶段检查 `user` 角色的消息内容。如果检测到违规，直接返回 403 并阻断请求，避免消耗昂贵的 Token 配额。
**常见陷阱**：审核逻辑会增加请求延迟，建议对于高并发场景，对审核 API 的调用设置较短的自身超时时间（如 500ms），超时则放行（降级策略），避免阻塞主流程。

### 5. 处理非标准 API 的协议转换
**场景**：你对接的某个国产大模型厂商不支持 OpenAI 标准协议，而你的客户端代码是基于 OpenAI SDK 写的。
**建议**：利用 Higress 的 **Request Rewrite**（请求重写）和 **Response Rewrite**（响应重写）功能，或者编写 WASM 插件进行协议适配。
**最佳实践**：将客户端发来的 OpenAI 格式 JSON 转换为目标厂商所需的格式（例如修改参数名 `max_tokens` -> `max_tokens`

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI 原生](/tags/ai-%E5%8E%9F%E7%94%9F/) / [LLM](/tags/llm/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [WASM](/tags/wasm/) / [MCP 协议](/tags/mcp-%E5%8D%8F%E8%AE%AE/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/) / [DevOps/运维](/scenarios/devops-%E8%BF%90%E7%BB%B4/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [OTelBench评测：Opus 4.5在简单SRE任务中得分仅29%]({{< relref "posts/20260129-hacker_news-otelbench-ai-struggles-with-simple-sre-tasks-opus--4.md" >}})
- [OTelBench评测：Opus 4.5在简单SRE任务中得分仅29%]({{< relref "posts/20260129-hacker_news-otelbench-ai-struggles-with-simple-sre-tasks-opus--5.md" >}})
- [中国开源AI生态的架构选择：超越DeepSeek的构建路径]({{< relref "posts/20260129-blogs_podcasts-architectural-choices-in-chinas-open-source-ai-eco-8.md" >}})
- [中国开源AI生态架构选择：DeepSeek之外的技术路径]({{< relref "posts/20260129-blogs_podcasts-architectural-choices-in-chinas-open-source-ai-eco-9.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*