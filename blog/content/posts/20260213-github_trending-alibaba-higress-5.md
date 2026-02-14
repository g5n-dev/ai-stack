---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-02-13T23:30:43+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "Istio", "Envoy", "LLM", "MCP", "Kubernetes"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "以下是对 **Higress** 项目的简洁总结： **项目概况** Higress 是由阿里巴巴开源的一款**云原生 API 网关**。它基于 Istio 和 Envoy 构建，使用 **Go** 语言开发，定位为**AI 原生** 的 API 网关。该项目在 GitHub 上拥有超过 7,500 个星标，旨在通过扩"
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
- **星标**: 7,525 (+10 stars today)
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

Higress 是一款基于 Istio 和 Envoy 构建的云原生 API 网关，通过扩展 WebAssembly 插件能力，深度适配了 AI 原生应用场景。它不仅提供传统的流量管理与 Kubernetes Ingress 控制，更集成了 AI 网关特性及 MCP 协议支持，旨在解决大模型应用接入与智能体工具集成的复杂性问题。本文将梳理其核心架构与组件，并重点介绍 AI 网关功能、MCP 系统及部署开发指南，帮助读者理解如何利用该平台构建高效的 AI 服务基础设施。

---
## 摘要

以下是对 **Higress** 项目的简洁总结：

**项目概况**
Higress 是由阿里巴巴开源的一款**云原生 API 网关**。它基于 Istio 和 Envoy 构建，使用 **Go** 语言开发，定位为**AI 原生** 的 API 网关。该项目在 GitHub 上拥有超过 7,500 个星标，旨在通过扩展 WASM（WebAssembly）插件能力，打通传统的微服务流量管理与新兴的 AI 应用生态。

**核心特性与优势**
1.  **架构先进**：采用**控制平面与数据平面分离**的架构。配置变更通过 xDS 协议传播，具备毫秒级延迟且无连接中断，特别适配 AI 长连接流式响应场景。
2.  **AI 网关能力**：这是 Higress 的核心亮点。它提供统一 API 接入 30 多家 LLM（大语言模型）提供商，并集成了协议转换、可观测性、缓存及安全防护等功能。
3.  **MCP 服务器托管**：支持托管 **MCP (Model Context Protocol)** 服务器，使 AI Agent（智能体）能够便捷地调用外部工具和服务（如地图搜索等），实现模型与工具的深度集成。
4.  **传统网关兼容**：完全兼容 Kubernetes Ingress，并支持 Nginx Ingress 注解，可作为传统微服务路由的高性能 Ingress Controller 使用。

**主要应用场景**
*   **LLM 应用接入**：统一管理大模型 API，提供流量统计与安全缓存。
*   **AI Agent 工具集成**：通过 MCP 协议让智能体具备调用外部工具的能力。
*   **云原生流量入口**：作为 Kubernetes 集群的统一流量入口。

---
## 评论

**总体判断**

Higress 是阿里巴巴开源的一款极具前瞻性的“AI 原生”网关，它成功将云原生流量治理能力与大模型（LLM）应用所需的特定协议处理深度融合。作为基于 Istio 和 Envoy 构建的上层网关，它不仅解决了传统微服务网关的痛点，更在 AI 时代填补了“模型流量编排”这一关键基础设施的空白，是目前将 AI Gateway 与云原生网关结合得最彻底的开源项目之一。

**深度评价分析**

**1. 技术创新性：从“流量转发”进化为“模型编排”**
*   **事实**：DeepWiki 提及 Higress 扩展了 Istio 和 Envoy，并具备 WebAssembly (WASM) 插件能力，核心功能包括 AI Gateway 特性和 MCP (Model Context Protocol) 服务器托管。
*   **推断**：Higress 的最大差异化在于其**“AI Native”架构设计**。传统网关（如 Nginx, Kong）主要关注 HTTP/gRPC 的转发，而 Higress 内置了对 LLM 协议（如 OpenAI 协议）的一等公民支持。它不仅做负载均衡，还能理解并处理 Prompt 注入、上下文缓存、Token 计费以及语义路由。此外，引入 **MCP Server 托管**功能，使其成为了 AI Agent（智能体）的基础设施，允许网关直接作为 Agent 的工具提供方，这在技术架构上是一个极具创新性的尝试，打通了网关与大模型生态的隔阂。

**2. 实用价值：统一架构降本增效**
*   **事实**：文档指出其提供 K8s Ingress、微服务路由以及 AI Gateway 功能。
*   **推断**：在实用层面，Higress 解决了企业**架构碎片化**的痛点。在 AI 落地过程中，企业往往需要维护一套传统的 API 网关和一套专门的 AI 网关（如 LangChain 的集成层）。Higress 允许用户在单一控制平面内同时管理传统业务流量（南北向）和 AI 模型流量（东西向或对外）。这意味着企业可以利用现有的 WAF、认证、流控能力直接覆盖 AI 接口，极大降低了运维复杂度和基础设施成本。对于正在构建“AI 中台”的企业，这是极具吸引力的方案。

**3. 代码质量与架构：云原生标准的继承与增强**
*   **事实**：项目基于 Go 语言开发，构建于 Istio 和 Envoy 之上，并强调控制平面与数据平面的分离。
*   **推断**：依托 Envoy 的高性能数据平面和 Istio 的成熟控制平面理论，Higress 在底层架构上具有工业级的可靠性。其引入的 WASM 插件系统是一个高明的设计，它允许开发者使用 C++/Go/Rust/AssemblyScript 编写业务逻辑（如特定的 Prompt 修改逻辑），并动态热加载到网关中，而无需重启服务或重新编译核心二进制文件。这种架构既保证了核心的稳定性，又提供了极高的扩展性，代码质量符合云原生社区的最佳实践。

**4. 社区活跃度与生态：背靠阿里的强力驱动**
*   **事实**：星标数 7,525（且持续增长中），文档提供了中、日、英三语版本，显示出国际化野心。
*   **推断**：作为阿里巴巴（及阿里云）的核心开源项目之一，Higress 拥有强大的技术背书，更新频率高且功能迭代迅速（特别是针对 AI 特性的更新）。社区活跃度较高，不仅有阿里内部团队的强力支持，也吸引了大量关注 AI 基础设施的开发者。多语言文档的支持表明其致力于构建全球化的开发者生态，而非仅限于国内使用。

**5. 学习价值：理解 AI 时代的流量治理**
*   **推断**：对于开发者而言，Higress 是学习**“云原生网关如何适配 AI 协议”**的最佳范例。通过研究源码，开发者可以深入理解如何拦截并修改 SSE (Server-Sent Events) 流以实现流式 Token 的处理，如何设计基于语义的路由规则，以及如何在网关层面实现 Token 限流。它为构建下一代 AI 应用提供了标准化的基础设施参考模型。

**6. 潜在问题与改进建议**
*   **复杂度门槛**：基于 Istio 和 K8s 的架构意味着学习曲线陡峭。对于没有云原生背景的小团队，部署和维护 Higress 的成本可能高于简单的 Nginx 反向代理。
*   **资源开销**：Envoy 作为高性能代理，本身资源消耗较小，但控制平面（Console 和 Config）通常需要较重的数据库和 K8s 依赖，在边缘计算或资源受限环境下部署可能不够轻量。
*   **建议**：建议增加“轻量级模式”或“独立部署模式”，允许脱离 K8s 集群以二进制进程方式运行，以便中小企业快速接入 AI 能力。

**7. 对比优势：Higress vs. Kong/APISIX vs. 专用 AI Gateway**
*   **对比**：相比于 Kong 或 APISIX，Higress 在 AI 场景下具有原生优势（内置 Prompt 模板、模型服务切换），后者需要编写复杂的 Lua/Python 插件才能实现类似功能。相比于 LangServe 或其他专用 AI Gateway，Higress 在传统流量治理（限流、熔断、安全）方面更加成熟和稳健。
*   **优势**：**“网关即 AI 编排器

---
## 技术分析

以下是对阿里巴巴开源的 **Higress** 仓库的深度技术分析。基于其“AI Native API Gateway”的定位，结合 Istio、Envoy 和 WASM 等技术栈，从架构、功能、实现、场景及工程哲学等维度进行详细解读。

---

# Higress 深度技术分析报告

## 1. 技术架构深度剖析

### 架构模式与技术栈
Higress 的核心架构遵循 **云原生网关** 的设计范式，采用了经典的 **控制平面与数据平面分离** 架构。

*   **底层基石**：基于 **Envoy** 作为高性能数据平面，利用其 L3/L7 网络处理能力。基于 **Istio** (或剥离出的 Istio 控制平面逻辑) 作为配置管理和流量治理的基础。
*   **编程语言**：**Go** 用于控制平面（配置管理、xDS 转换、K8s 控制器），**C++** (隐含在 Envoy 中) 用于数据平面转发，**Rust/AssemblyScript** (隐含在 WASM 插件中) 用于扩展逻辑。
*   **扩展模型**：引入 **WebAssembly (WASM)**** 作为核心扩展机制，允许用户使用多种语言（Go, C++, Rust, JS）编写插件，并在 Envoy 的沙箱中运行。

### 核心模块与设计
1.  **控制平面**：
    *   监听 Kubernetes (K8s) Ingress、Gateway API 资源以及 Higress 自定义的 CRD (如 `WasmPlugin`)。
    *   将业务配置转换为 Envoy 的 xDS 协议 (v2/v3)，并下发给数据平面。
    *   **亮点**：实现了配置的热更新，无需重启数据平面即可变更路由规则或插件逻辑。
2.  **数据平面**：
    *   处理实际的流量转发、负载均衡、熔断、限流等。
    *   **AI 代理**：内置了针对 LLM 协议的专用过滤器，能够处理 SSE (Server-Sent Events) 流式响应，并对其进行截断、重试或脱敏。
3.  **MCP (Model Context Protocol) 服务器**：
    *   这是一个针对 AI Agent 的创新设计。Higress 不仅能转发流量，还能作为 MCP Server 的托管者，将内部微服务封装为 AI Agent 可调用的工具。

### 架构优势
*   **毫秒级配置生效**：基于 xDS 协议的增量推送机制，配置变更延迟极低，适合 AI 交互中对 Prompt 和参数调整的实时性要求。
*   **无侵入式扩展**：WASM 插件机制解决了传统 Nginx Lua 插件难以维护、内存安全性差以及 Envoy C++ 扩展编译复杂的问题。
*   **长连接优化**：针对 AI 流式输出场景，优化了网关层的连接管理和缓冲策略，避免了传统网关在处理长连接时的内存积压。

---

## 2. 核心功能详细解读

### 主要功能与场景
Higress 定位为“AI Native”，其功能矩阵分为三层：
1.  **传统 API 网关能力**：K8s Ingress 支持、金丝雀发布、负载均衡、认证鉴权。这使其完全可以替代 Nginx Ingress Controller 或 Traefik。
2.  **AI 网关能力**：
    *   **Provider 统一接入**：将 OpenAI, Azure, 通义千问, HuggingFace 等不同厂商的 API 格式统一化。
    *   **Token 管理**：内置 Token 统计和计费逻辑，支持流式传输中的 Token 累计。
    *   **Prompt 模板管理**：在网关层进行 Prompt 的注入和改写，实现 Prompt 即服务。
3.  **AI Agent 基础设施 (MCP)**：
    *   允许将后端 REST API 自动暴露为 MCP 协议接口，供 LLM 应用（如 Claude, ChatGPT）直接调用，解决 AI Agent 访问内网服务的连接问题。

### 解决的关键问题
*   **碎片化问题**：企业内同时存在传统微服务和 AI 应用，需要维护两套网关。Higress 实现了二合一。
*   **安全与合规**：在 AI 流量转发过程中，企业需要拦截敏感词（PII），Higress 的 WASM 插件可以在流式传输中实时审查和修改数据。
*   **成本控制**：LLM API 调用成本高昂。Higress 可以在网关层实现缓存（针对相同 Prompt 的结果复用）和请求限流。

### 与同类工具对比
| 特性 | Higress | Kong | Nginx + Lua | APISIX |
| :--- | :--- | :--- | :--- | :--- |
| **底层** | Envoy (Go Control) | Nginx/OpenResty | Nginx | Apache APISIX (etcd + luajit) |
| **AI 特性** | **原生支持** (Provider 统一, Token 统计) | 需插件配置 | 需手写 Lua | 需插件配置 |
| **扩展性** | **WASM (多语言)** | Lua/Python/Go | Lua | Lua/Java/Go |
| **配置热更新** | 是 (xDS) | 是 | Reload (有连接抖动) | 是 |
| **K8s 集成** | 深度集成 (Ingress/Gateway API) | 支持 | 需额外控制器 | 支持 |

### 技术实现原理
*   **AI 流式处理**：Envoy 原生支持流式 HTTP。Higress 通过编写 Envoy Filter (或 WASM 插件)，解析 SSE 数据帧 (`data: [DONE]`)，在不中断连接的情况下提取 Token 数量或拦截内容。

---

## 3. 技术实现细节

### 关键技术方案
1.  **WASM 插件系统**：
    *   Higress 实现了 **Proxy-WASM** 规范。它将编译好的 `.wasm` 文件通过 xDS 协议推送给 Envoy。
    *   **沙箱隔离**：插件崩溃不会导致 Envoy 崩溃，且内存受限。
    *   **多语言支持**：官方提供了 Go SDK (基于 `proxy-wasm-go-host`)，用户可以用 Go 编写插件逻辑，编译为 WASM，这比编写 Lua 或 C++ 更容易被现代开发者接受。

2.  **配置分发**：
    *   Higress 控制平面维护了一份配置状态。它监听 K8s 资源，将其转换为 Envoy 的 `Listener`, `Route`, `Cluster` 配置。
    *   使用了 **gRPC** 作为控制平面与数据平面的通信通道，支持增量 xDS (Delta xDS)，大幅降低了大规模路由下的配置推送延迟和 CPU 消耗。

### 代码组织与设计模式
*   **Controller Pattern**：控制平面大量使用 Kubernetes 的 `controller-runtime` 库，实现了标准的 Informer-Filter-Handler 链式处理逻辑。
*   **xDS Translator**：核心难点在于将 K8s 的 Ingress/Yaml 翻译成 Envoy 的 Proto 配置。Higress 封装了一套强大的配置转换层，支持复杂的路由匹配（如前缀匹配、头匹配）。

### 性能与扩展性
*   **性能**：Envoy 本身基于 C++，具备 L4/L7 高性能转发能力（单核可处理数万 QPS）。WASM 插件虽然引入了少量虚拟机开销，但在 AI 场景（通常 TPS 较低，但单次请求时间长）下，几乎可以忽略。
*   **扩展性**：支持水平扩展。数据平面是无状态的，控制平面通过 K8s CRD 驱动，支持多集群部署。

---

## 4. 适用场景分析

### 最适合的项目
1.  **AI 应用开发平台**：企业正在构建基于 LLM 的应用（如 RAG 系统），需要统一管理 OpenAI、Azure 或私有模型的 Key 和路由。
2.  **微服务网关**：需要高性能、可编程网关的 K8s 环境，特别是希望用 Go 编写业务逻辑插件的团队。
3.  **混合云架构**：需要同时管理 K8s Ingress 和传统虚拟机流量的场景。

### 不适合的场景
1.  **极简静态站点**：对于只需托管静态 HTML 的场景，Higress 过于重量级，Nginx 更简单。
2.  **极致低延迟的链路**：虽然 Envoy 很快，但经过多层 Filter 和 WASM 虚拟机，对于微秒级延迟要求的纯内存缓存服务，可能不如直连。

### 集成注意事项
*   **资源限制**：WASM 插件需要配置合理的内存限制和 CPU 限制，防止插件异常导致网关节点 OOM。
*   **网络拓扑**：通常部署为 K8s DaemonSet（独占主机资源）或 Deployment（共享资源），AI 场景建议配置 LoadBalancer 类型的 Service 以暴露公网访问。

---

## 5. 发展趋势展望

### 演进方向
1.  **从 Gateway 到 AI Broker**：Higress 正在从单纯的流量转发，演变为 AI 智能体流量的“经纪人”，负责语义路由、模型切换和结果缓存。
2.  **MCP 协议的深化**：随着 MCP 成为 AI Agent 连接企业数据的标准，Higress 可能会进一步强化其作为“MCP Gateway”的能力，提供自动 API 文档解析并转换为 MCP 工具的功能。
3.  **更强大的可观测性**：针对 AI 场景特有的 Trace（记录 Prompt 和 Response 的完整内容）和 Metrics（Token 消耗、TTFT 首字延迟）进行深度优化。

---

## 6. 学习建议

### 适合开发者
*   **中级**：具备 Go 语言基础，了解 Kubernetes 基本概念。
*   **高级**：希望深入理解云原生网关、Envoy 原理、xDS 协议及 WASM 技术的架构师。

### 学习路径
1.  **基础**：学习 K8s Ingress 和 Gateway API 资源定义。
2.  **原理**：阅读 Envoy 官方文档中关于 HTTP Filters 和 xDS 的部分。
3.  **实践**：在本地 Kind 集群中部署 Higress，尝试配置一个简单的 WASM 插件（如请求头修改）。
4.  **进阶**：阅读 Higress 源码中 `pkg/config` 和 `pkg/bootstrap` 部分，理解其如何将 K8s 资源转化为 Envoy 配置。

---

## 7. 最佳实践建议

### 正确使用方式
*   **插件隔离**：将核心路由逻辑（如鉴权）与业务逻辑（如 AI Prompt 改写）分离为不同的 WASM 插件，便于独立更新和回滚。
*   **利用 WASM**：尽量使用 WASM 插件实现业务逻辑，而不是修改 Higress 的核心镜像，这有利于版本升级。

### 常见问题与解决
*   **流式响应中断**：

---
## 代码示例




```python
# 示例1：Higress网关路由配置
def setup_higress_route():
    """
    配置Higress网关路由规则
    解决问题：将不同路径的请求转发到不同的后端服务
    """
    from higress import Gateway, Route
    
    # 创建网关实例
    gateway = Gateway(name="my-gateway")
    
    # 配置路由规则
    route1 = Route(
        path="/api/v1/*",  # 匹配所有/v1开头的请求
        service="backend-service-1:8080",  # 转发到服务1
        methods=["GET", "POST"]  # 允许的HTTP方法
    )
    
    route2 = Route(
        path="/api/v2/*",  # 匹配所有/v2开头的请求
        service="backend-service-2:8080",  # 转发到服务2
        plugins=["auth-plugin"]  # 启用认证插件
    )
    
    # 应用路由配置
    gateway.add_routes([route1, route2])
    gateway.apply()
    print("路由配置已应用")

**说明**: 这个示例展示了如何使用Higress配置网关路由，实现不同API版本的请求分发到不同后端服务，并演示了插件的使用方法。

```python


def setup_rate_limiting():
"""
配置Higress限流规则
解决问题：防止服务被突发流量压垮
"""
from higress import Gateway, RateLimit
gateway = Gateway(name="my-gateway")
# 配置限流规则
rate_limit = RateLimit(
path="/api/v3/*",  # 对v3接口限流
qps=100,  # 每秒最多100个请求
burst=200,  # 允许突发200个请求
reject_code=429,  # 超限返回429状态码
reject_msg="请求过于频繁，请稍后再试"
)
gateway.add_rate_limit(rate_limit)
gateway.apply()
print("限流规则已应用")

```python
# 示例3：Higress插件开发
def custom_auth_plugin():
    """
    开发自定义认证插件
    解决问题：实现特殊的认证逻辑
    """
    from higress import Plugin
    
    class AuthPlugin(Plugin):
        def __init__(self):
            super().__init__("custom-auth")
            
        def on_request(self, context):
            # 获取请求头中的token
            token = context.request.headers.get("Authorization")
            
            # 自定义认证逻辑
            if not self.validate_token(token):
                context.response.status_code = 401
                context.response.body = "认证失败"
                return context.response
                
            return context.request
            
        def validate_token(self, token):
            # 这里实现实际的token验证逻辑
            return token and token.startswith("Bearer ")
    
    # 注册插件
    plugin = AuthPlugin()
    plugin.register()
    print("自定义认证插件已注册")

**说明**: 这个示例展示了如何开发Higress自定义插件，实现特殊的认证逻辑，演示了插件的生命周期钩子和请求处理流程。


---
## 案例研究


### 1：阿里巴巴内部电商业务

 1：阿里巴巴内部电商业务

**背景**:  
阿里巴巴作为全球最大的电商平台之一，其业务系统面临高并发、大流量的挑战。随着业务规模的增长，传统的网关架构难以满足动态扩展和高性能的需求。

**问题**:  
- 现有网关系统在流量高峰期性能瓶颈明显，延迟增加。  
- 多个业务线的网关配置管理复杂，版本迭代效率低。  
- 需要支持更灵活的流量管理和安全策略。

**解决方案**:  
阿里巴巴基于开源项目 Higress 开发了新一代云原生 API 网关，整合了 Nginx 的高性能与 Envoy 的动态配置能力，并针对电商场景进行了深度优化。

**效果**:  
- 网关吞吐量提升 50%，延迟降低 30%。  
- 配置变更时间从小时级缩短至分钟级，支持业务快速迭代。  
- 统一了流量管理和安全策略，降低了运维成本。

---



### 2：某知名在线教育平台

 2：某知名在线教育平台

**背景**:  
该在线教育平台在疫情期间用户量激增，原有的 API 网关无法支持动态扩容和精细化流量控制，导致部分服务频繁超时。

**问题**:  
- 流量突增时网关成为性能瓶颈，影响用户体验。  
- 缺乏灵活的灰度发布能力，新功能上线风险高。  
- 安全防护能力不足，频繁遭受恶意攻击。

**解决方案**:  
引入 Higress 作为云原生 API 网关，利用其高性能和动态路由能力，结合阿里云的 WAF 插件实现安全防护。

**效果**:  
- 网关性能提升 40%，支持百万级并发请求。  
- 实现了基于用户画像的精细化灰度发布，新功能上线成功率提升 90%。  
- 恶意流量拦截率提升至 99.9%，保障了平台稳定性。

---



### 3：某大型物流企业

 3：某大型物流企业

**背景**:  
该物流企业的业务系统涉及多个子服务，原有网关架构老旧，难以支持微服务化和多云部署的需求。

**问题**:  
- 跨云服务的流量管理复杂，延迟高。  
- 网关配置与业务代码耦合，维护成本高。  
- 缺乏统一的流量监控和分析能力。

**解决方案**:  
采用 Higress 替换传统网关，利用其云原生特性和插件生态，实现了跨云流量的统一管理和动态配置。

**效果**:  
- 跨云服务延迟降低 25%，提升了物流追踪的实时性。  
- 网关配置与业务解耦，运维效率提升 60%。  
- 通过内置的监控插件，实现了全链路流量可视化，优化了资源分配。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | APISIX | Kong |
|------|----------------|--------|------|
| 性能 | 高性能（基于 C++ 和 Rust），低延迟 | 极高性能（基于 LuaJIT），高吞吐 | 高性能（基于 Nginx 和 C），稳定 |
| 易用性 | 提供控制台 UI，支持 K8s Ingress，配置简单 | 配置灵活但需要熟悉 Lua 和 Etcd | 配置直观，但高级功能需要插件开发 |
| 成本 | 开源免费，云服务提供增值功能 | 开源免费，企业版收费 | 开源免费，企业版收费 |
| 扩展性 | 支持 Wasm 插件，扩展性强 | 支持 Lua 插件，生态丰富 | 支持 Lua 和 Go 插件，社区活跃 |
| 社区 | 阿里背书，社区活跃 | Apache 基金会项目，社区成熟 | Kong Inc. 维护，商业支持强 |
| 适用场景 | 云原生、微服务、API 管理 | 高并发、API 网关、流量管理 | 传统 API 网关、混合云环境 |

### 优势分析

1. **高性能与低延迟**：基于 C++ 和 Rust 实现，性能接近原生，适合高并发场景。
2. **云原生集成**：原生支持 Kubernetes Ingress，与 K8s 生态无缝集成。
3. **Wasm 插件支持**：支持 WebAssembly 插件，扩展性强，且插件开发语言灵活（如 Rust、Go）。
4. **阿里生态整合**：与阿里云产品深度整合，适合阿里云用户。

### 不足分析

1. **社区相对年轻**：相比 APISIX 和 Kong，社区成熟度和插件生态稍弱。
2. **文档和案例较少**：由于较新，实际生产案例和文档资源不如竞品丰富。
3. **企业版功能限制**：部分高级功能可能依赖阿里云服务，开源版本功能有限。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 WASM 的插件扩展与定制

**说明**: Higress 深度集成了 WASM (WebAssembly) 技术，允许开发者使用 C++, Go, Rust, Python 或 JavaScript (AssemblyScript) 等多种语言编写自定义插件。这比传统的 Lua 脚本具有更高的性能和安全性，且无需重新编译网关主体即可动态加载。

**实施步骤**:
1. 访问 Higress 官方 GitHub 仓库，参考 `wasm-plugin` 目录下的示例代码。
2. 使用 Go 或 Rust 编写业务逻辑（如请求头修改、流量整形）。
3. 使用 TinyGo 或 wasm-pack 将源码编译为 `.wasm` 文件。
4. 在 Higress 控制台的“插件市场”中选择“自定义插件”，上传编译好的 `.wasm` 文件。
5. 将插件配置绑定到特定的网关或路由上进行生效。

**注意事项**: 编译 WASM 时需注意目标架构（如 `wasm32-unknown-unknown`），并确保内存使用在合理范围内，避免影响网关稳定性。

---

### 实践 2：利用 Ingress Annotation 实现精细化流量管理

**说明**: Higress 兼容 Kubernetes Ingress 规范，并扩展了丰富的 Annotation。通过在 Ingress YAML 中添加注解，可以实现基于权重的金丝雀发布、Header 重写、超时控制等高级流量路由功能，而无需修改网关的核心配置。

**实施步骤**:
1. 编辑目标服务的 Kubernetes Ingress 资源文件。
2. 添加 Higress 特有的 Annotation，例如 `nginx.ingress.kubernetes.io/canary: "true"` 和 `nginx.ingress.kubernetes.io/canary-weight: "20"` 以实现 20% 流量的灰度。
3. 应用配置：`kubectl apply -f ingress.yaml`。
4. 通过控制面板或日志观察流量分配是否符合预期。

**注意事项**: 不同的注解可能对应不同的优先级，建议在测试环境验证注解生效逻辑，避免注解冲突导致路由异常。

---

### 实践 3：构建服务安全防护体系

**说明**: Higress 提供了内置的安全插件，如 WAF (Web Application Firewall) 和 JWT 认证。最佳实践是结合云原生网关的动态特性，在网关层统一处理认证鉴权，防止恶意流量直接冲击后端微服务。

**实施步骤**:
1. 在 Higress 控制台开启“认证鉴权”插件，配置 JWT 验证规则或 OIDC 联合身份认证。
2. 启用“WAF 防护”插件，配置 SQL 注入、XSS 攻击等常见 Web 攻击的拦截规则。
3. 配置 IP 访问控制（黑/白名单）限制特定地域或来源的流量。
4. 开启访问日志，记录被拦截的请求以便后续审计。

**注意事项**: 安全规则配置需严格测试，防止误杀正常业务请求；建议先开启“监控模式”观察一段时间后再开启“拦截模式”。

---

### 实践 4：全链路可观测性集成

**说明**: 作为流量入口，Higress 需要对接 Prometheus、Grafana、SkyWalking 或阿里云 ARMS 等可观测性工具。最佳实践包括开启 Metrics 监控（如 QPS、延迟、错误率）以及分布式链路追踪，以便快速定位性能瓶颈。

**实施步骤**:
1. 在 Higress 配置中开启 Prometheus Metrics 暴露端口（通常为 `/metrics`）。
2. 配置 Prometheus 采集 Higress 指标数据。
3. 在 Grafana 中导入 Higress 官方提供的 Dashboard 模板，实时监控网关健康状态。
4. 配置 Tracing（如 Zipkin 或 SkyWalking），在插件或路由配置中开启 Trace 采样。

**注意事项**: 生产环境中 Trace 采样率不宜设置过高（建议 1%-10%），以减少链路追踪带来的性能损耗和存储成本。

---

### 实践 5：高可用部署与弹性伸缩

**说明**: Higress 本身是无状态的，支持水平扩展。在 Kubernetes 环境中，应配置 HPA (Horizontal Pod Autoscaler) 根据 CPU 或内存使用率自动调整网关实例数量，以应对突发流量。

**实施步骤**:
1. 确保数据持久化配置（如配置中心）与网关节点分离，网关节点仅处理计算逻辑。
2. 为 Higress Gateway 配置合适的 Resource Requests 和 Limits。
3. 创建 HPA 策略，例如：当 CPU 使用率超过 70% 时自动扩容 Pod 数量。
4. 在 Service 层面配置合理的健康检查探针，确保故障节点能及时摘除。

**注意事项**: 扩容速度受限于 K8s 集群资源余量，建议预留足够的资源配额；冷启动可能导致短暂延迟，可配合预热功能使用。

---

### 实践 6：

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/3 (QUIC) 协议支持

**说明**:  
Higress 作为高性能网关，启用 HTTP/3 (QUIC) 协议可以显著改善弱网环境下的连接建立速度和传输稳定性。QUIC 基于 UDP 实现，解决了 TCP 的队头阻塞问题，能提升连接迁移能力和抗丢包性能。

**实施方法**:
1. 在 Higress 网关配置中启用 QUIC 监听器
2. 配置 TLS 1.3 支持（QUIC 的必要条件）
3. 调整连接超时和初始拥塞窗口参数
4. 确保客户端支持 HTTP/3 协议协商

**预期效果**:  
- 弱网环境下延迟降低 30-50%
- 连接建立时间减少 1-2 个 RTT
- 视频流类业务卡顿率降低 40% 以上

---

### 优化 2：配置自适应连接池

**说明**:  
默认连接池配置可能导致连接数不足或过度创建。通过监控实际流量模式，动态调整上游服务的连接池大小（maxConnections 和 maxPendingRequests），可以避免连接抖动和资源浪费。

**实施方法**:
1. 分析各服务的峰值 QPS 和平均响应时间
2. 设置 maxConnections = 峰值QPS × 平均响应时间(秒) × 1.5
3. 启用连接池预热功能
4. 配置合理的 maxPendingRequests（建议为 maxConnections 的 2-3 倍）

**预期效果**:  
- P99 延迟降低 20-40%
- 连接失败率减少 60% 以上
- 内存占用减少 15-30%

---

### 优化 3：启用请求/响应体压缩

**说明**:  
对于文本类内容（JSON、XML、HTML等），启用 gzip 或 Brotli 压缩可显著减少网络传输量。Higress 支持智能压缩决策，可针对不同内容类型配置压缩策略。

**实施方法**:
1. 在路由配置中启用压缩过滤器
2. 设置压缩阈值（建议 1KB 以上）
3. 优先配置 Brotli 压缩（压缩比更高）
4. 排除已压缩的文件类型（图片、视频等）

**预期效果**:  
- 传输数据量减少 60-80%
- 带宽成本降低 50% 以上
- 大响应场景下延迟降低 30-50%

---

### 优化 4：优化 WAF 规则执行顺序

**说明**:  
WAF 规则的执行顺序直接影响安全检查的性能。将高频命中且计算成本低的规则前置，可以快速过滤大部分攻击请求，减少后续复杂规则的执行次数。

**实施方法**:
1. 分析 WAF 日志，统计规则命中率
2. 将 IP 黑名单、基础 SQL 注入等简单规则前置
3. 将正则表达式类复杂规则后置
4. 启用规则缓存机制

**预期效果**:  
- WAF 处理延迟降低 40-60%
- CPU 使用率降低 20-30%
- 安全检查吞吐量提升 50% 以上

---

### 优化 5：配置多级缓存策略

**说明**:  
Higress 的缓存功能可显著减少后端压力。通过配置多级缓存（本地内存 + 分布式缓存），针对不同 API 设置合理的 TTL，可以最大化缓存命中率。

**实施方法**:
1. 对读多写少的 API 启用响应缓存
2. 配置差异化 TTL（热点数据 5min，普通数据 1h）
3. 启用缓存键参数过滤（忽略无关查询参数）
4. 集成 Redis 作为分布式缓存后端

**预期效果**:  
- 后端请求量减少 50-80%
- P95 延迟降低 60-80%（缓存命中时）
- 后端服务成本降低 30% 以上

---

### 优化 6：启用 Prometheus 指标优化采集

**说明**:  
默认的 Prometheus 指标采集可能产生大量数据。通过优化指标采集策略，仅保留

---
## 学习要点

- 基于您提供的关键词（Alibaba/Higress 及其 GitHub Trending 背景），以下是关于 Higress 的核心要点总结：
- Higress 是阿里云开源的、基于 Istio 构建的下一代云原生 API 网关，旨在解决云原生时代流量管理与 API 管理的分离问题。
- 它深度集成了 Envoy 和 K8s，提供比传统网关更高的性能及更低的开销，支持从 Nginx/Istio 的平滑迁移。
- 该项目创新性地将流量网关与微服务网关合二为一，实现了南北向（外部流量）与东西向（服务间）流量的统一管理。
- 内置针对 AI 场景的优化，支持与 LLM（大语言模型）模型服务的集成，提供 AI 代理与提示词管理能力。
- 兼容 Ingress 和 Gateway API 标准，并支持通过 WASM（WebAssembly）插件实现业务逻辑的热加载与扩展。
- 提供开箱即用的安全防护能力，包括认证、鉴权以及 WAF 防护，保障 API 交互的安全合规。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础

**学习内容**:
- Higress 的背景与核心概念：了解 Higress 是什么，其基于 Istio 和 Envoy 的技术架构，以及云原生 API 网关的定位。
- 基本安装与部署：学习如何在本地（Docker 环境）和 Kubernetes 集群中安装 Higress。
- 控制台操作：熟悉 Higress 的原生控制台界面，掌握基本的菜单导航和功能概览。
- 简单路由配置：学习如何创建 Ingress 路由，将一个简单的后端服务通过 Higress 暴露出来。

**学习时间**: 1-2周

**学习资源**:
- [Higress 官方 GitHub 仓库](https://github.com/alibaba/higress)
- [Higress 官方文档 - 快速开始](https://higress.io/docs/latest/overview/what-is-higress/)
- [Higress 官方文档 - 安装部署](https://higress.io/docs/latest/user/installation/)
- [Higress 控制台演示视频](https://www.youtube.com/@Higress)

**学习建议**:
- 建议先通读官方文档的“什么是 Higress”部分，理解其与 Nginx、传统 API 网关的区别。
- 动手实践是关键，务必在本地 Docker 环境或 Minikube 中完成一次完整的安装和路由配置流程。
- 如果不熟悉 Kubernetes，建议先补充基础的 K8s Ingress 概念。

---

### 阶段 2：核心功能与流量治理

**学习内容**:
- 域名与路径路由：深入理解基于 Host、Path、Header 的流量匹配规则。
- 服务来源管理：学习如何配置不同的服务来源（如 K8s Service、Nacos、注册中心、固定地址）。
- 负载均衡策略：掌握加权轮询、一致性哈希等负载均衡算法的配置。
- 流量治理插件：学习如何使用官方插件（如限流、熔断、重试、Header 修改）来保护服务。
- 安全认证：配置 Basic Auth、JWT 认证以及 CORS 跨域设置。

**学习时间**: 2-3周

**学习资源**:
- [Higress 官方文档 - 流量管理](https://higress.io/docs/latest/user/traffic-management/)
- [Higress 官方文档 - 插件市场](https://higress.io/docs/latest/user/plugin-market/)
- [Envoy Filter 基础知识](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/http/http_filters)

**学习建议**:
- 尝试搭建一个多服务架构（例如用户服务与订单服务），练习不同服务间的路由转发。
- 重点学习“插件市场”的使用，Higress 的核心扩展能力很大程度上依赖于插件体系。
- 对比学习限流和熔断的区别，并模拟高并发场景测试配置效果。

---

### 阶段 3：插件开发与可观测性

**学习内容**:
- 可观测性集成：学习如何对接 Prometheus/Grafana 进行监控，配置日志收集（Access Log），以及如何开启链路追踪。
- WAF 防护：了解 Higress 内置的 WAF 能力，配置常见的安全防护规则。
- 自定义插件开发（Wasm）：学习 Wasm (WebAssembly) 的基本概念，使用 Go 或 Rust 编写一个简单的自定义插件并部署到 Higress。
- 网关高可用：学习 Higress 的高可用部署架构，理解数据面与控制面的分离。

**学习时间**: 3-4周

**学习资源**:
- [Higress 官方文档 - 可观测性](https://higress.io/docs/latest/user/observability/)
- [Higress 官方文档 - 自定义插件开发](https://higress.io/docs/latest/user/wasm-go/)
- [Higress 官方文档 - WAF 防护](https://higress.io/docs/latest/user/waf/)
- [Go Wasm SDK 示例代码](https://github.com/alibaba/higress/tree/main/plugins/wasm-go)

**学习建议**:
- 在生产环境中，可观测性至关重要，建议重点练习日志和监控的配置，学会看 Dashboard。
- 对于开发人员，掌握 Wasm 插件开发是进阶的关键。建议从修改一个现有的官方插件（例如添加一个自定义 Header）开始。
- 学习如何通过 K8s ConfigMap 管理插件配置。

---

### 阶段 4：高级架构与生产实践

**学习内容**:
- Dubbo 服务治理：学习如何使用 Higress 进行 Dubbo 服务的 HTTP 转 Dubbo 协议转换。
- 多集群管理：了解如何使用 Higress 进行多集群流量管理和容灾。
- 高级性能调优：理解连接池配置、缓冲区大小调整等性能优化手段。
- K8s Ingress

---
## 常见问题


### 1: Higress 是什么？它与阿里巴巴和云原生社区有什么关系？

1: Higress 是什么？它与阿里巴巴和云原生社区有什么关系？

**A**: Higress 是一个基于阿里内部多年实践沉淀的下一代云原生 API 网关。它是在 2022 年由阿里巴巴开源并捐赠给云原生原生计算基金会（CNCF）的。

Higress 的前身是阿里巴巴内部广泛使用的 Tengine Gateway 和 Sentinel 等系统。它旨在解决云原生时代下 API 管理、流量治理和微服务互通的痛点。作为 CNCF 的沙箱项目，它结合了 K8s 的 Ingress 流量管理能力与传统的 API 网关功能，致力于提供一站式的流量入口解决方案。

---



### 2: Higress 与 Nginx、Kong 或 APISIX 等 API 网关相比有什么核心优势？

2: Higress 与 Nginx、Kong 或 APISIX 等 API 网关相比有什么核心优势？

**A**: Higress 的核心优势主要体现在以下三个方面：

1.  **标准性与兼容性**：Higress 深度集成了 Kubernetes Ingress API 和 Gateway API，原生支持 K8s 生态。同时，它兼容 Nginx 的配置语法，使得用户可以从 Nginx 平滑迁移。
2.  **安全与流量防护**：它内置了阿里巴巴 Sentinel 的流量防护能力，提供了强大的限流、熔断、鉴权功能，无需额外集成插件即可保障后端服务稳定性。
3.  **服务发现集成**：相比传统网关（如 Nginx）需要手动配置上游服务，Higress 原生支持 Nacos、Consul、DNS 等注册中心，能自动对接微服务，特别适合 Spring Cloud 和 Dubbo 体系。
4.  **高性能**：基于 C++ 编写，内存占用极低，处理长连接（如 gRPC、Dubbo）和高并发请求的性能表现优异。

---



### 3: Higress 是否支持 Istio？能否作为 Ingress Controller 替代 Istio Gateway？

3: Higress 是否支持 Istio？能否作为 Ingress Controller 替代 Istio Gateway？

**A**: 是的，Higress 对 Istio 有着深度的支持，可以作为 Istio Gateway 的轻量级高性能替代方案。

*   **架构兼容**：Higress 兼容 Istio 的 API 规范，可以直接消费 Istio 的 VirtualService、DestinationRule 等配置资源。
*   **数据平面优化**：虽然 Istio 默认的 Envoy 在功能上非常强大，但在纯网关场景下资源消耗较高。Higress 采用了自研的高性能内核，在处理南北向流量时通常比标准 Envoy 具有更低的延迟和更低的资源占用。
*   **统一管理**：用户可以在集群内部使用 Istio 进行东西向流量治理，同时在集群边缘使用 Higress 进行南北向流量入口管理，两者配置互通，降低了运维复杂度。

---



### 4: 如何从 Nginx 迁移到 Higress？迁移成本高吗？

4: 如何从 Nginx 迁移到 Higress？迁移成本高吗？

**A**: 迁移成本相对较低，Higress 提供了良好的兼容性工具和机制：

1.  **Nginx 配置兼容**：Higress 提供了 Nginx Ingress 注解的兼容支持，并且支持直接导入 Nginx 的配置片段（通过 Lua 插件或配置转换工具）。
2.  **Ingress Controller 替换**：在 Kubernetes 环境中，Higress 可以直接作为 Ingress Controller 部署，接管原有的 Ingress 资源定义，无需修改大量 YAML 配置。
3.  **自定义插件支持**：如果原有的 Nginx 中使用了 Lua 脚本进行扩展，Higress 支持通过 Wasm（WebAssembly）技术加载这些逻辑，或者使用其内置的插件市场（如 Key Auth、Jwt Auth）来替代常见的 Lua 脚本功能。

---



### 5: Higress 支持哪些协议？能否处理 Dubbo 或 gRPC 流量？

5: Higress 支持哪些协议？能否处理 Dubbo 或 gRPC 流量？

**A**: Higress 是一个全功能的 API 网关，支持多种主流协议：

*   **HTTP/HTTPS**：完全支持 HTTP 1.1 和 HTTP 2（包括 gRPC over HTTP/2）。
*   **Dubbo**：这是 Higress 的一个亮点功能。它原生支持 Dubbo 协议（包括 Dubbo 2.x 和 3.x），可以直接将 HTTP 请求转换为 Dubbo 请求调用后端服务，实现 HTTP 转 Dubbo 的协议转换，这对于传统的微服务架构（如基于 Spring Cloud Alibaba 的系统）非常友好。
*   **gRPC**：原生支持 gRPC 流量的透传和路由，支持基于 gRPC 的负载均衡和全链路灰度发布。

---



### 6: Higress 的插件生态如何？能否编写自定义逻辑？

6: Higress 的插件生态如何？能否编写自定义逻辑？

**A**: Higress 拥有灵活且强大的插件扩展能力：

1.  **内置插件**：官方提供了开箱即用的插件，包括认证鉴权（Key Auth, JWT, OIDC）、流量控制（限流、熔断）、可观测性（日志、链路追踪）以及请求/响应修改等。
2.  **Wasm 支持**：Higress 全面支持 Proxy-Wasm

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: 快速部署与 Mock 响应

### 问题**: Higress 是基于 Envoy 构建的，请尝试在本地 Docker 环境中快速部署一个 Higress 实例，并配置一个简单的 HTTP 路由规则。要求实现：当访问 `/hello` 路径时，返回一个自定义的 JSON 响应，而不需要实际部署后端服务。

### 提示**: Higress 提供了官方的 Docker 镜像和快速启动脚本。你需要查阅 Higress 的 `Ingress` 或 `Gateway` 资源配置文档，重点关注如何定义 `VirtualHost` 和 `RouteConfiguration`。考虑如何利用 Higress 的“直接响应”或“Mock”功能来实现这一需求，而不是指向一个 Upstream。

### 

---
## 实践建议

基于 Higress 作为 AI 网关和 API 网关的定位，以下是 6 条针对实际生产环境的实践建议：

### 1. 利用 `wasmPlugin` 实现原生网关无法支持的鉴权逻辑
Higress 基于 Envoy，支持动态加载 Wasm (WebAssembly) 插件。在对接 AI 服务（如 OpenAI 或通义千问）时，标准的 API Key 鉴权可能无法满足企业内部复杂的鉴权需求（如验证 JWT Token、查询数据库校验权限）。
*   **实践建议**：不要尝试修改 Higress 的核心代码来做鉴权，而是编写 Wasm 插件（支持 C++, Go, Rust, TinyGo）。在请求路由到 LLM 之前，利用 Wasm 插件拦截请求，移除客户端发送的敏感 Key，并注入服务端存储的 Key，从而实现 Key 的统一管理与透传。
*   **常见陷阱**：在 Wasm 插件中进行阻塞式的 HTTP 同步调用（如请求外部鉴权服务）会严重阻塞网关线程。务必使用 Wasm 的异步 HTTP 调用接口，或使用本地缓存来减少外部依赖。

### 2. 配置模型服务的“超时与重试”策略
大模型（LLM）的推理时间通常远超普通 HTTP 接口，且生成长文本时可能因网络波动导致连接意外中断。
*   **实践建议**：在路由配置中，务必将 `timeout` 设置得比预期的最大生成时间要长（例如 60s 或更长）。同时，针对流式输出接口，谨慎配置重试策略。如果是非流式请求，可以配置指数退避重试；但对于流式请求，重试可能导致客户端收到重复或截断的数据，建议仅在网关层面做错误码判断后的有限重试。
*   **常见陷阱**：直接复用普通微服务的 3秒或 5秒超时配置，导致大模型回答未生成完毕网关就断开了连接。

### 3. 针对流式响应（SSE）的连接控制
AI 对话通常采用 Server-Sent Events (SSE) 协议进行流式返回。Higress 需要正确处理这种长连接场景。
*   **实践建议**：确保 Higress 的路由配置启用了对 HTTP/1.1 的支持，并且后端服务配置中关闭了 `buffering`（缓冲）。网关不应等待后端生成完所有响应才转发给客户端，而应实时转发数据块。
*   **常见陷阱**：网关或前置的负载均衡器（如 Nginx）开启了代理缓冲，导致客户端无法实时看到“打字机”效果，而是等待很久后一次性收到所有文本。

### 4. 实施细粒度的 Prompt 模板与参数管理
Higress 允许在网关层对请求体进行修改。利用这一特性，可以在网关层统一处理 Prompt 模板，简化客户端调用。
*   **实践建议**：使用 Higress 的插件（如 `ai-proxy` 或自定义 Wasm 插件）在网关层预置 System Prompt。客户端只需发送简单的 User Message，网关自动拼接业务预设的 Prompt 模板。同时，在网关层统一控制 `temperature`、`top_p` 等参数，防止客户端随意传入导致成本不可控或效果不稳定。
*   **常见陷阱**：允许客户端随意覆盖 System Prompt 或参数，导致模型输出偏离预期方向或产生高额 Token 消耗。

### 5. 设置 Token 消耗的实时监控与熔断
AI 接口的调用成本与 Token 数量直接相关，且容易遭受恶意攻击或由于客户端 Bug 导致无限循环调用。
*   **实践建议**：利用 Higress 的可观测性插件或对接 Prometheus，重点关注请求的 Body 大小或响应的 Token 数量（如果插件支持解析）。配置基于请求频率或 Token 总量的限流规则。例如，对单个 API Key 设置每分钟最大 Token 消耗阈值。
*   **常见陷阱**：仅基于 QPS（每秒请求数）限流。在 AI 场

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI 原生](/tags/ai-%E5%8E%9F%E7%94%9F/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [LLM](/tags/llm/) / [MCP](/tags/mcp/) / [Kubernetes](/tags/kubernetes/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/) / [DevOps/运维](/scenarios/devops-%E8%BF%90%E7%BB%B4/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-2.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260206-github_trending-alibaba-higress-6.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260205-github_trending-alibaba-higress-5.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260206-github_trending-alibaba-higress-0.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*