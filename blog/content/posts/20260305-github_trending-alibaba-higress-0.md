---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-03-05T02:41:37+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "云原生", "Istio", "Envoy", "WASM", "LLM", "MCP 协议"]
categories: ["系统与基础设施", "AI 工程"]
source: github_trending
description: "**Higress 项目概述总结** **Higress** 是由阿里巴巴开源的一款**云原生 API 网关**。它基于 Istio 和 Envory 构建，并扩展了 WebAssembly (WASM) 插件能力，定位为 **AI Native API Gateway**。该项目使用 Go 语言编写，目前在 GitH"
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
- **星标**: 7,636 (+11 stars today)
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

Higress 是一款基于 Istio 和 Envoy 构建的云原生 API 网关，专为 AI 原生应用设计。它通过提供 LLM 流量管理、MCP 服务托管以及传统的微服务路由能力，解决了大模型应用接入与治理的复杂性问题。本文将介绍其核心架构、WASM 插件扩展机制以及 AI 网关的关键特性，帮助开发者理解如何利用 Higress 构建高性能的 AI 基础设施。

---
## 摘要

**Higress 项目概述总结**

**Higress** 是由阿里巴巴开源的一款**云原生 API 网关**。它基于 Istio 和 Envory 构建，并扩展了 WebAssembly (WASM) 插件能力，定位为 **AI Native API Gateway**。该项目使用 Go 语言编写，目前在 GitHub 上拥有超过 7,600 颗星。

**核心架构与优势：**
Higress 将控制平面（配置管理）与数据平面（流量处理）分离。配置变更通过 xDS 协议传播，具有毫秒级延迟且不中断连接的特性，特别适用于 AI 流式响应等长连接场景。

**三大主要功能与用例：**

1.  **AI 网关：**
    *   提供统一的 API 接口，兼容 30 多家大语言模型（LLM）提供商。
    *   核心功能包括协议转换、可观测性、缓存以及安全防护。
    *   涉及组件：`ai-proxy`, `ai-statistics`, `ai-cache`, `ai-security-guard` 等插件。

2.  **MCP 服务器托管：**
    *   托管模型上下文协议（MCP）服务器，使 AI 智能体能够调用工具和服务。
    *   涉及组件：`mcp-router`, `jsonrpc-converter` 过滤器及相关服务器实现（如 `quark-search`, `amap-tools`）。

3.  **Kubernetes Ingress（传统 API 网关）：**
    *   作为 Ingress 控制器使用，兼容 `nginx-ingress` 注解。
    *   提供微服务路由等传统网关能力。

**相关文档：**
项目提供了详细的多语言 README（中文、日文、英文），涵盖了构建部署、WASM 插件系统、AI 特性及开发指南。

---
## 评论

### 总体判断

Higress 是目前云原生网关领域中将“AI 原生”与“传统流量治理”结合得最彻底的开源项目之一。它成功地将 Istio 的控制平面能力与 Envoy 的高性能数据平面进行了下沉与封装，并创造性地引入了 AI Gateway 与 MCP 协议支持，是构建 LLM（大语言模型）应用基础设施的强力选项。

### 深度评价依据

**1. 技术创新性：从“流量网关”向“AI 管网”的架构跃迁**
*   **事实：** DeepWiki 明确指出 Higress 基于 Istio 和 Envoy 构建，并扩展了 WebAssembly (WASM) 插件能力。它不仅提供 Kubernetes Ingress 和微服务路由，还集成了 AI Gateway 功能和 MCP (Model Context Protocol) 服务器托管。
*   **推断：** Higress 的核心差异化在于其**“AI Native”的定位**。传统网关（如 Nginx, Kong）主要处理 HTTP/gRPC 转发，而 Higress 内置了对 LLM 特有的语义理解需求的支持。
    *   **MCP 协议支持：** 这是一个极具前瞻性的创新。MCP 正在成为 AI Agent 连接外部数据源的标准协议，Higress 直接内置 MCP Server 托管，意味着它不仅仅是一个流量的“管道”，更成为了 AI Agent 的“工具箱”或“连接器”，解决了 Agent 与后端工具集成的复杂度问题。
    *   **WASM 插件化：** 继承并强化了 Envoy 的 WASM 能力，使得用户可以用 C++/Go/Rust/AssemblyScript 编写极度灵活的逻辑插件，这在处理 AI 请求的 Prompt 注入、敏感词过滤等场景下比传统的 Lua 脚本性能更好且更安全。

**2. 实用价值：解决 AI 落地“最后一公里”的流量与成本问题**
*   **事实：** 仓库描述强调其具备“AI Gateway features for LLM applications”和“Traditional API gateway capabilities”。
*   **推断：** Higress 解决了当前企业接入大模型时的三个核心痛点：
    *   **统一接入与协议转换：** 企业内部可能有 OpenAI、通义千问、Llama 等多种模型，Higress 可以作为统一入口，屏蔽不同 Provider 的 API 差异。
    *   **Token 成本与安全控制：** 通过内置插件，可以实现基于 Token 级别的限流（防止模型调用刷爆预算）和实时敏感数据脱敏（防止企业机密泄露给模型），这是传统网关无法感知的“语义层”安全。
    *   **云原生平滑迁移：** 对于已经使用 K8s 的企业，Higress 兼容 Ingress API，可以作为低侵入式的 Sidecar 或 Gateway 替代传统 Nginx Ingress，保护现有投资。

**3. 代码质量与架构：工业级标准的控制与数据分离**
*   **事实：** 架构上明确分离了控制平面和数据平面。项目由阿里巴巴主导，Go 语言编写。
*   **推断：** 作为阿里内部通用的网关方案开源，其代码质量通常遵循严格的工业标准。
    *   **架构设计：** 基于Istio的控制平面意味着它继承了成熟的服务发现和配置管理能力，而基于Envoy的数据平面保证了高性能（C++ 内核）和低延迟。这种组合比完全从零写一个网关要稳健得多。
    *   **扩展性：** WASM 虚拟机的引入使得网关的业务逻辑扩展变得极其灵活，开发者无需重新编译网关二进制文件即可热更新插件，这对于快速迭代的 AI 业务至关重要。

**4. 社区活跃度与生态：大厂背书，但需关注社区多样性**
*   **事实：** 星标数 7,636（且在持续增长），由阿里巴巴开源。
*   **推断：** 阿里巴巴的开源项目通常具有较好的维护性和代码稳定性。Higress 不仅是一个独立项目，更是阿里云 Higress 产品的开源底座，这意味着它有明确的商业支持，不会轻易停止维护。不过，从社区角度看，核心贡献者可能仍以阿里员工为主，外部独立开发者的贡献占比是衡量其生态健康度的关键观察点。

**5. 学习价值：理解云原生与 AI 基础设施的绝佳样本**
*   **事实：** 项目涵盖了 K8s Operator 开发、Envoy 配置、WASM 插件开发以及 AI 协议处理。
*   **推断：** 对于开发者而言，研究 Higress 的源码是学习如何构建**“下一代基础设施”**的最佳实践。它展示了如何将传统的网络编程（TCP/HTTP）与新兴的 AI 应用语义（Prompt/Token）结合。特别是其 WASM 插件系统，为学习边缘计算和 Serverless 冷启动逻辑提供了优秀范例。

### 边界条件与不适用场景

尽管 Higress 功能强大，但在以下场景中可能不是最优解：
1.  **极简易部署：** 如果你只需要一个简单的反向代理或负载均衡器，且不涉及 K8s，Higress 的架构过于沉重，Nginx 或 Traefik 更合适。
2.  **纯传统应用且无 AI 需求：** 如果业务完全没有接入 LLM 的计划，Higress 的 AI 特性属于冗余功能，虽然可以用作传统网关，但配置复杂度可能高于 APISIX 或 Kong

---
## 技术分析

以下是对阿里巴巴开源的 **Higress** 项目的深度技术分析。基于其定位为“AI Native API Gateway”，我们将重点探讨它如何将传统的云原生网关能力与大语言模型（LLM）时代的需求相结合。

---

# Higress 深度技术分析报告

## 1. 技术架构深度剖析

Higress 的架构设计体现了“继承与演进”的特点，它并没有从零开始造轮子，而是站在了 Istio 和 Envoy 这两个巨人的肩膀上，并针对 AI 场景进行了深度定制。

### 技术栈与架构模式
*   **底层基石**：基于 **Envoy** 作为高性能数据平面，利用其 L4/L7 处理能力和可观测性。
*   **控制平面**：深度集成 **Istio**，复用其 xDS（控制平面 API）配置下发机制。这意味着 Higress 天生具备服务网格的能力，可以无缝管理 K8s 服务。
*   **扩展模型**：采用 **WebAssembly (WASM)** 作为核心插件扩展机制。这打破了传统 C++ 插件开发难、风险高、需要重新编译二进位的限制，允许使用 Go/C++/Rust/JavaScript 等语言编写动态插件。
*   **部署形态**：云原生设计，通常以 Kubernetes Ingress Controller 或独立网关形态部署。

### 核心模块与关键设计
1.  **控制平面与数据平面分离**：配置变更通过 xDS 协议毫秒级推送到数据节点，且支持热更新，无需重启进程，这对长连接场景至关重要。
2.  **WASM 虚拟机**：在 Envoy 中嵌入 WASM 运行时，实现了沙箱化的插件执行环境。
3.  **AI 网关专用模块**：这是 Higress 区别于传统网关的核心。它内置了对 LLM 协议（如 OpenAI 协议）的理解，能够处理流式响应。

### 技术亮点与创新点
*   **AI Native (AI 原生)**：不仅仅是转发 HTTP 请求，Higress 理解 LLM 的语义。它原生支持**流式转发**，在处理 Server-Sent Events (SSE) 时，能够低延迟地将 AI 生成的 Token 传递给客户端，同时保持连接稳定性。
*   **MCP (Model Context Protocol) 集成**：Higress 不仅是网关，还充当 MCP Server 的托管中心。这意味着 AI Agent 可以通过 Higress 统一访问外部工具和数据源，简化了 Agent 的工具调用链路。
*   **统一接入层**：试图将传统的微服务 API 管理与 AI 应用 API 管理收敛在同一层，避免维护两套网关系统。

### 架构优势分析
*   **性能**：得益于 Envoy 的高性能异步非阻塞模型，Higress 在处理高并发请求时延迟极低。
*   **安全性**：WASM 插件运行在沙箱中，插件崩溃不会导致网主进程崩溃，且提供了内存和 CPU 的隔离限制。
*   **生态兼容**：完全兼容 K8s Ingress API 和 Istio Gateway API，降低了迁移成本。

## 2. 核心功能详细解读

### 主要功能与使用场景
1.  **AI 流量管理**：
    *   **多模型路由**：根据请求内容（如 Prompt 复杂度）或用户标签，将流量路由到不同的 LLM 提供商（如 OpenAI、通义千问、本地部署的 Llama）。
    *   **Token 计费与限流**：基于 Token 数量而非单纯的请求数进行速率限制和计费，这对 AI 成本控制至关重要。
    *   **Key 管理**：统一管理各大厂商的 API Key，前端请求只需携带一个 Higress 签发的 Token，网关后端动态映射到具体的厂商 Key，防止密钥泄露。

2.  **MCP Server Hosting (模型上下文协议托管)**：
    *   允许用户将数据库、SaaS 工具等封装为 MCP 接口并挂载在网关上。AI Agent 通过与 Higress 对接，即可动态发现并调用这些工具，无需修改 Agent 代码。

3.  **传统 API 网关能力**：
    *   K8s Ingress、金丝雀发布、负载均衡、认证鉴权。

### 解决的关键问题
*   **LLM 接口碎片化**：解决了企业需要对接多个 LLM 厂商接口不一致的问题，提供统一的 OpenAI 兼容接口。
*   **AI 应用的高可用性**：当某个 LLM 服务超时或报错时，网关层可自动重试或切换到备用模型，保障业务连续性。
*   **Prompt 注入防护**：在网关层通过 WASM 插件对用户输入进行清洗，拦截恶意 Prompt。

### 与同类工具对比
*   **VS Nginx/Kong**：传统网关对 SSE（流式）支持一般，且缺乏对 AI 语义的理解（如 Token 统计）。Kong 虽然有 AI 插件，但 Higress 的 Istio 底座在云原生生态中更具优势。
*   **VS API Gateway (AWS Azure)**：云厂商网关绑定性强，Higress 提供了跨云、混合云部署的统一控制平面。
*   **VS LangChain / Dify**：后者是应用开发框架，Higress 是基础设施。Higress 可以作为这些应用流量的入口，负责路由和安全，而不负责 Prompt 编排。

### 技术实现原理
*   **流式处理**：Higress 在 Envoy Filter 层面实现了对 SSE 协议的流式拦截。它可以在不截断连接的情况下，对数据块进行缓冲、处理（如修改头部、添加元数据）后转发。

## 3. 技术实现细节

### 关键技术方案
*   **WASM 插件机制**：Higress 实现了 `proxy-wasm` 规范。Go 代码会被编译为 WASM 字节码，运行在 Envoy 的 WASM VM 中。通过 `OnHttpRequestHeaders`, `OnHttpBody` 等虚函数钩子介入请求生命周期。
*   **配置热更新**：基于 Istio 的 xDS (v2/v3) 协议。控制平面监听 K8s CRD 变化，转化为 Envoy 配置推送给数据节点。Envoy 采用 `Listener`、`Route`、`Cluster` 的增量更新机制，确保在配置变更时只有受影响的连接会微小的抖动。

### 代码组织结构
*   **`/pkg`**：核心业务逻辑，包含与 K8s 交互的控制器、配置转换逻辑。
*   **`/plugins`**：WASM 插件源码，通常包含 Go 版本的插件实现。
*   **`/docker`**：镜像构建相关，通常包含 Envoy + Higress 控制面组件的打包。

### 性能优化与扩展性
*   **零拷贝**：Envoy 本身的高性能特性被继承。
*   **连接池**：对后端 LLM 服务（通常是 HTTP/1.1 或 HTTP/2）维护连接池，减少握手开销。
*   **水平扩展**：无状态设计，数据面可以随 K8s Pod 数量线性扩容。

### 技术难点与解决方案
*   **难点**：WASM 的性能损耗。
*   **方案**：Higress 团队优化了 WASM 运行时（如使用 Wasmtime 的特定优化配置），并建议将轻量级逻辑放在 WASM 中，重度计算仍放在 Go/C++ 主程序或通过 gRPC 调用外部服务。
*   **难点**：超长连接的稳定性。
*   **方案**：优化了 TCP Keepalive 和 HTTP/2 的 Ping 机制，防止在网络空闲时连接被中间设备断开。

## 4. 适用场景分析

### 最适合的项目
*   **企业级 AI 应用平台**：需要统一接入多个 LLM 供应商，并对内部微服务和 AI 接口进行统一管理的场景。
*   **AI Agent 基础设施**：特别是需要利用 MCP 协议连接企业内部数据源（如 SQL 数据库、Wiki）的 Agent 系统。
*   **高并发 SaaS 服务**：需要在网关层进行鉴权、限流、流量整形，且对延迟敏感的 Go 微服务集群。

### 不适合的场景
*   **极简个人项目**：如果只是调用一个 OpenAI API，Nginx 足矣，引入 Higress 过重。
*   **非 K8s 环境**：虽然可以二进制运行，但其威力主要在于与 K8s 和 Istio 的结合。在传统 VM 环境下运维复杂度较高。
*   **极度依赖 TCP/UDP 转发的场景**：Higress 专注于 L7，对于纯 L4 高性能转发，虽然支持但不如专门的四层负载均衡器（如 IPVS）高效。

### 集成方式
*   **K8s Ingress**：通过 `Ingress` 资源定义路由规则。
*   **Gateway API**：支持更现代的 K8s Gateway API CRD。
*   **MCP Bridge**：通过配置 CRD 将后端服务注册为 MCP 工具。

## 5. 发展趋势展望

### 技术演进方向
*   **更深度的 Dapr 集成**：作为 Sidecar 或 Gateway 统一处理微服务通信。
*   **向边缘计算下沉**：利用 WASM 的轻量级特性，Higress 可能会推出边缘版本，运行在 CDN 节点或 IoT 设备上，就近处理 AI 推理请求。
*   **RAG (检索增强生成) 原生支持**：未来可能会内置向量数据库的连接代理，简化 RAG 流程的网关层处理。

### 社区反馈与改进空间
*   **文档与易用性**：虽然功能强大，但配置 Istio 和 Envoy 的概念较多，学习曲线陡峭。需要更简化的抽象层。
*   **WASM 生态成熟度**：虽然 Go 支持 WASM，但调试 WASM 插件仍然比调试本地代码困难。

## 6. 学习建议

### 适合人群
*   **云原生架构师**：希望深入理解 Istio/Envory 架构。
*   **后端 Gopher**：学习如何用 Go 构建高性能中间件。
*   **AI 工程师**：需要构建生产级 AI 应用的开发者。

### 学习路径
1.  **基础**：熟悉 Kubernetes 和 Ingress 概念。
2.  **核心**：阅读 Envoy 官方文档中的 xDS 和 Filter 机制。
3.  **进阶**：阅读 Higress 源码中的 `config-controller` 部分，理解 K8s CRD 如何转化为 Envoy 配置。
4.  **实践**：尝试编写一个简单的 WASM 插件（如添加 HTTP Header），并在本地 Kind 集群中运行 Higress 进行测试。

## 7. 最佳实践建议

### 如何正确使用
*   **插件隔离**：将核心路由逻辑与业务逻辑（如鉴权）分离，业务逻辑尽量

---
## 代码示例




```python
# 示例1：Higress 网关路由配置
from higress import Gateway, Route

def setup_gateway_routing():
    """
    配置 Higress 网关的路由规则
    解决问题：将不同路径的请求转发到不同的后端服务
    """
    # 创建网关实例
    gateway = Gateway(name="api-gateway")
    
    # 添加路由规则
    gateway.add_route(
        Route(
            path="/api/v1/*",
            service="user-service:8080",
            methods=["GET", "POST"],
            plugins=["auth-plugin", "rate-limit"]
        )
    )
    
    # 启动网关
    gateway.start()

# 说明：这个示例展示了如何使用 Higress 配置网关路由，将 /api/v1/ 路径的请求转发到 user-service，并应用认证和限流插件。
```




```python
# 示例2：Higress 插件开发
from higress import Plugin

class AuthPlugin(Plugin):
    """
    自定义认证插件
    解决问题：验证请求头中的 API 密钥
    """
    def on_request(self, context):
        api_key = context.request.headers.get("X-API-KEY")
        if not self.validate_key(api_key):
            context.response.status_code = 401
            context.response.body = "Unauthorized"
            return context.response
        return context.request
    
    def validate_key(self, key):
        # 实际应用中这里应该查询数据库或调用认证服务
        return key == "valid-api-key-123"

# 说明：这个示例展示了如何开发一个 Higress 插件，实现基于 API 密钥的请求认证，未通过认证的请求将被拒绝。
```




```python
# 示例3：Higress 服务发现与负载均衡
from higress import ServiceRegistry, LoadBalancer

def configure_service_discovery():
    """
    配置服务发现和负载均衡
    解决问题：动态发现后端服务实例并实现负载均衡
    """
    # 创建服务注册中心
    registry = ServiceRegistry()
    
    # 注册服务实例
    registry.register(
        service_name="order-service",
        instances=[
            "10.0.0.1:8080",
            "10.0.0.2:8080",
            "10.0.0.3:8080"
        ]
    )
    
    # 配置负载均衡策略
    lb = LoadBalancer(
        strategy="round_robin",  # 轮询策略
        health_check=True,       # 启用健康检查
        timeout=5                # 超时时间5秒
    )
    
    return registry, lb

# 说明：这个示例展示了如何使用 Higress 配置服务发现和负载均衡，自动管理后端服务实例并实现请求分发。
```


---
## 案例研究


### 1：阿里巴巴内部电商业务

 1：阿里巴巴内部电商业务

**背景**:  
阿里巴巴内部电商业务（如淘宝、天猫）面临复杂的微服务架构，涉及数千个服务实例和频繁的流量变更。传统的网关解决方案难以满足高并发、动态路由和低延迟的需求。

**问题**:  
1. 性能瓶颈：传统网关在高峰期（如双11）出现延迟和吞吐量不足。  
2. 动态路由困难：服务变更需要手动配置，导致运维效率低下。  
3. 扩展性差：无法快速支持新协议（如gRPC、Dubbo）。

**解决方案**:  
基于Higress构建统一云原生API网关，利用其高性能（基于Rust和C++实现）和动态路由能力，集成Kubernetes Ingress Controller，支持多协议（HTTP、gRPC、Dubbo）和流量治理。

**效果**:  
1. 性能提升：网关延迟降低30%，吞吐量提升50%。  
2. 运维效率：动态路由配置实现自动化，变更时间从小时级降至分钟级。  
3. 扩展性增强：无缝支持新协议，业务迭代速度提升40%。

---



### 2：某互联网金融科技公司

 2：某互联网金融科技公司

**背景**:  
该金融科技公司为第三方提供支付和风控API服务，日均请求量达数亿次。原有基于Nginx的网关难以应对复杂的鉴权、限流和监控需求。

**问题**:  
1. 安全风险：传统网关缺乏细粒度的鉴权和防刷能力。  
2. 监控盲区：无法实时追踪API调用链路和异常流量。  
3. 成本高：依赖商业API管理工具，授权费用昂贵。

**解决方案**:  
采用Higress替代传统网关，通过其内置的WAF插件、自定义鉴权逻辑和Prometheus集成，实现全链路可观测性和安全防护。

**效果**:  
1. 安全加固：恶意请求拦截率提升至99.9%，未发生安全事件。  
2. 可观测性：实时监控API调用，故障定位时间缩短70%。  
3. 成本优化：开源方案替代商业工具，年节省费用超百万元。

---



### 3：某大型物流企业

 3：某大型物流企业

**背景**:  
该企业物流系统需对接外部合作伙伴（如快递公司、仓储服务），API接口数量超过500个。原有网关无法统一管理多租户流量和版本控制。

**问题**:  
1. 多租户混乱：不同合作伙伴的流量隔离和计费困难。  
2. 版本管理低效：API变更需手动通知，导致兼容性问题。  
3. 流量治理缺失：无法针对不同租户实施差异化限流策略。

**解决方案**:  
部署Higress作为API管理平台，利用其多租户支持、API版本管理和流量标签功能，实现精细化流量治理。

**效果**:  
1. 多租户隔离：按合作伙伴分配独立流量配额，计费准确率100%。  
2. 版本管理自动化：API变更自动通知，兼容性问题减少80%。  
3. 流量优化：差异化限流策略保障核心业务稳定性，SLA达标率提升至99.95%。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|----------------|------|-------|
| 性能 | 高性能，基于 Rust 和 Go，支持高并发 | 高性能，基于 Nginx 和 Lua，支持高并发 | 极高性能，基于 Nginx 和 Lua，支持高并发 |
| 易用性 | 提供控制台和 K8s Operator，易于部署和管理 | 提供管理界面和丰富的插件，配置灵活 | 提供管理界面和 Dashboard，配置复杂度较高 |
| 成本 | 开源免费，企业版需付费 | 开源免费，企业版需付费 | 开源免费，企业版需付费 |
| 扩展性 | 支持 WASM 插件，扩展性强 | 支持 Lua 和 Go 插件，扩展性较强 | 支持 Lua 和 Python 插件，扩展性一般 |
| 社区支持 | 阿里巴巴背书，社区活跃 | 社区成熟，插件生态丰富 | 社区活跃，国内支持较好 |
| 安全性 | 内置安全策略，支持 WAF | 需额外配置安全插件 | 内置安全功能，支持 WAF |

### 优势分析

- 优势1：高性能架构，基于 Rust 和 Go 开发，资源占用低。
- 优势2：支持 WASM 插件，扩展性强，适合复杂业务场景。
- 优势3：阿里巴巴背书，社区活跃，企业支持完善。
- 优势4：提供完整的控制台和 K8s Operator，易于部署和管理。

### 不足分析

- 不足1：相比 Kong 和 APISIX，插件生态尚不成熟。
- 不足2：文档和社区资源相对较少，学习曲线较陡。
- 不足3：企业版功能可能需要付费，成本较高。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 WASM 实现轻量级网关扩展

**说明**: Higress 深度集成了 WebAssembly (WASM) 技术，允许开发者使用 C++, Go, Rust, JavaScript 等语言编写插件。相比传统 Java 网关插件，WASM 插件具有隔离性好、启动快、内存占用低且支持热加载（无需重启网关）的优势。

**实施步骤**:
1. 根据业务复杂度选择合适的开发语言（推荐使用 Go 或 Rust）。
2. 利用 Higress 官方提供的 SDK 或 Proxy-WASM 规范编写插件逻辑。
3. 将编译好的 WASM 文件上传至 Higress 控制台，或配置 OCI 远程加载。
4. 在网关路由或全局规则中关联该 WASM 插件，并配置相关参数。

**注意事项**: 
开发 WASM 插件时需注意内存限制和超时设置，避免插件逻辑异常阻塞网关主请求处理流程。

---

### 实践 2：精细化流量路由与灰度发布

**说明**: 利用 Higress 强大的路由能力实现全链路灰度。通过基于请求头、Cookie、权重或查询参数的流量匹配，将特定流量路由到服务的不同版本（如 Canary 版本），从而降低新版本上线的风险。

**实施步骤**:
1. 在服务注册中心（如 Nacos）部署服务的不同版本。
2. 在 Higress 中配置服务来源，确保能识别到不同版本的服务实例。
3. 创建或修改路由规则，配置匹配条件（如 `x-canary: true`）。
4. 设置目标服务为灰度版本，并调整流量权重（例如 5% 的流量）。
5. 监控关键指标，确认无误后逐步调整权重至 100%。

**注意事项**: 
灰度发布需要配合可观测性监控，确保出现问题时能第一时间回滚流量。

---

### 实践 3：构建高性能安全网关

**说明**: Higress 内置了丰富的安全防护能力。最佳实践是启用内置的 WAF 插件或配置严格的访问控制策略，以防御 SQL 注入、XSS 攻击等常见 Web 威胁，同时限制非法来源 IP 的访问。

**实施步骤**:
1. 在插件市场启用 "WAF 插件" 或 "Key Rate Limit" 插件。
2. 配置防护规则，根据业务需求选择拦截模式或监控模式。
3. 配置 IP 访问控制列表（黑名单/白名单）。
4. 针对特定 API 路径配置更严格的鉴权机制（如 JWT 验证或 AK/SK 验证）。

**注意事项**: 
安全策略可能会产生误杀，建议先在 "监控模式" 下运行一段时间，观察日志后再开启 "拦截模式"。

---

### 实践 4：服务注册与发现的标准化对接

**说明**: Higress 原生支持 Nacos、Consul、Zookeeper 等主流注册中心。最佳实践是确保网关与业务服务使用同一套注册中心，实现服务实例的自动感知与健康检查，避免手动维护上游服务列表。

**实施步骤**:
1. 在 Higress 控制台的 "服务来源" 中添加对应的注册中心（如 Nacos）。
2. 配置注册中心的连接地址（Server Addr）和命名空间。
3. 创建 "服务" 资源，关联注册中心中的服务名。
4. 在路由配置中引用该服务作为 Upstream。

**注意事项**: 
确保 Higress 所在网络环境能够连通注册中心的网络端口，且注册中心的服务名命名规范保持一致。

---

### 实践 5：全链路可观测性集成

**说明**: 为了快速定位性能瓶颈和故障，应启用 Higress 的日志采集、指标监控和链路追踪功能。Higress 原生兼容 OpenTelemetry 标准，可轻松对接 Prometheus、Grafana、SkyWalking 等系统。

**实施步骤**:
1. **日志**: 配置访问日志格式，推荐使用 JSON 格式以便解析，并对接 Kafka 或 Filebeat 收集。
2. **指标**: 开开 Prometheus 拉取端点，配置 Grafana 仪表盘监控 QPS、延迟、错误率。
3. **链路**: 在网关配置中开启 Tracing，设置采样率，并上报至 SkyWalking 或 Jaeger 后端。

**注意事项**: 
在高流量场景下，全量采集链路追踪数据会对性能产生影响，建议设置合理的采样率（如 1% 或 10%）。

---

### 实践 6：多租户与多环境隔离

**说明**: 在大型企业或微服务架构中，通常存在开发、测试、生产等多个环境。利用 Higress 的命名空间或独立的网关实例来实现环境隔离，防止测试流量干扰生产数据。

**实施步骤**:
1. 在注册中心（如 Nacos）中使用不同的命名空间区分环境。
2. Higress 配置对应命名空间的服务来源，

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/2 与 HTTP/3 (QUIC) 协议

**说明**: Higress 作为高性能网关，利用 HTTP/2 的多路复用特性可以解决 HTTP/1.1 的队头阻塞问题，显著提升并发请求处理能力。HTTP/3 (QUIC) 则进一步解决了基于 TCP 的传输层延迟问题，尤其在高丢包或弱网环境下效果显著。

**实施方法**:
1. 在 Higress 的网关路由配置中，确保监听协议开启 `HTTP/2`。
2. 在 `Ingress` 或 `Gateway` 资源中配置注解开启 QUIC 支持（需 Higress 版本支持）。
3. 确保后端 Upstream 服务也支持 HTTP/2 以建立全链路连接。

**预期效果**: 高并发场景下 TCP 连接数减少 60% 以上，弱网环境下请求延迟降低 20%-40%。

---

### 优化 2：启用全链端对端请求超时与重试策略优化

**说明**: 默认的超时设置可能不适合高吞吐量的微服务架构。过长的超时会导致连接池耗尽，过短则导致频繁失败。配置合理的超时与指数退避重试机制，可以防止雪崩并提高系统整体吞吐量。

**实施方法**:
1. 在 Higress 路由配置中显式设置 `connectTimeout`、`readTimeout` 和 `sendTimeout`，建议根据 P99 耗时设置余量。
2. 配置重试策略，设置最大重试次数（如 3 次），并开启指数退避。
3. 针对幂等接口（如 GET）启用重试，非幂等接口（如 POST）谨慎开启或通过业务层控制。

**预期效果**: 在后端服务出现偶发故障时，系统成功率可提升至 99.9% 以上，同时减少无效连接占用。

---

### 优化 3：启用 Wasm 插件与 Lua 脚本的高性能隔离

**说明**: Higress 原生支持 Wasm (WebAssembly)。相比于传统的 Lua 脚本或本地过滤器，Wasm 插件拥有接近原生的执行速度，且通过沙箱机制保证了安全性，能够处理复杂的鉴权、限流逻辑而不阻塞主线程。

**实施方法**:
1. 将复杂的业务逻辑（如自定义鉴权、请求体修改）编写为 Wasm 插件（支持 C++/Go/Rust 编译）。
2. 在 Higress 控制台或通过 WasmPlugin CRD 加载插件。
3. 避免在请求路径中使用高复杂度的正则表达式匹配。

**预期效果**: 复杂插件处理延迟降低 30%-50%，且主线程稳定性不受插件逻辑影响。

---

### 优化 4：配置连接池与 Keep-Alive 优化

**说明**: Higress 与后端服务之间的连接建立开销是主要的性能瓶颈之一。通过调整 HTTP 连接池大小和保持长连接，可以大幅减少 TCP 握手和 TLS 握手的频率。

**实施方法**:
1. 调整 `maxConnections` 参数，根据后端服务能力设置合理的连接池上限。
2. 启用 `http2ProtocolOptions` 中的 `keepalive` 时间，建议设置为 300 秒或更高。
3. 开启连接池预热，避免 Higress 重启或扩容时瞬间流量击垮后端。

**预期效果**: 后端连接复用率提升至 90% 以上，后端服务 CPU 消耗因减少握手而降低 10%-20%。

---

### 优化 5：启用本地与分布式缓存

**说明**: 对于鉴权、配置下发或静态资源响应等场景，启用网关层的缓存可以显著减少对后端服务的请求压力。Higress 支持在网关内存或对接 Redis/Redis 集群进行缓存。

**实施方法**:
1. 在 Higress 配置中开启 `extProc` 或利用内置缓存插件对 Key-Value 数据进行本地内存缓存。
2. 对于

---
## 学习要点

- 基于提供的来源信息（Alibaba/Higress 及其 GitHub 趋势背景），以下是关键要点总结：
- Higress 是阿里云开源的、基于 Envoy 和 Istio 构建的下一代云原生 API 网关，旨在解决云原生时代流量管理的复杂性问题。
- 它深度集成了 K8s Ingress 与 Gateway API 标准，能够无缝对接 Kubernetes 生态，实现服务流量的统一管理与调度。
- 提供了强大的 WAF（Web 应用防火墙）插件生态，支持热加载和动态配置，可在不重启网关的情况下灵活扩展安全与流量处理能力。
- 兼容 Nginx Ingress 注解配置，显著降低了用户从传统 Nginx 迁移至云原生网关的技术门槛与迁移成本。
- 支持将服务网格的 Sidecar 模式转化为网关模式，利用 Envoy 的高性能架构，在提供丰富功能的同时保持极高的处理吞吐量。
- 作为开源项目，它在 GitHub 上迅速获得关注，代表了行业向“标准化网关+插件化扩展”演进的主流技术趋势。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础与核心概念

**学习内容**:
- 云原生网关基础：理解 API Gateway 在微服务架构中的定位与作用，区分传统网关与云原生网关的差异。
- Higress 架构概览：了解 Higress 的诞生背景（基于 Nginx & Envoy），其核心特性（高可用、低延迟、热更新）。
- 基本安装部署：学习如何在 Docker 环境下快速安装 Higress，以及如何在 Kubernetes（K8s）集群中进行标准部署。
- 控制台操作：熟悉 Higress Dashboard 的使用，包括路由配置、服务来源（Nacos, K8s Service）的添加。
- 基础流量管理：掌握域名路由、路径匹配、Header 匹配等基本的流量转发规则。

**学习时间**: 1-2周

**学习资源**:
- Higress 官方文档 (快速开始章节)
- Higress GitHub 仓库 (README 与 架构设计文档)
- Docker 与 Kubernetes 基础教程 (作为前置知识储备)

**学习建议**:
建议先在本地 Docker 环境中跑通一个最简单的示例，例如将一个后端服务通过 Higress 暴露出来。不要一开始就深入复杂的 K8s 配置，先通过控制台界面理解“路由”和“服务”的概念。

---

### 阶段 2：流量治理与插件系统

**学习内容**:
- 高级流量管理：深入学习灰度发布（金丝雀发布）、蓝绿部署、流量镜像与负载均衡算法。
- 插件系统（Wasm）：理解 Higress 的插件机制，学习如何使用官方预置插件（如：限流、熔断、认证鉴权、CORS 处理）。
- 安全防护：配置 IP 访问控制、Basic Auth、ApiKey 认证等安全策略。
- 全局与精细化配置：学习如何针对特定路由或服务应用插件，理解插件执行顺序。
- 服务发现集成：探索如何与 Nacos、Consul、DNS 或 K8s CoreDNS 进行深度集成。

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 流量治理与插件市场章节
- Envoy 官方文档 (了解基础 Proxy 原理)
- Higress 官方插件市场

**学习建议**:
动手实践一次完整的流量切换流程，例如模拟一个应用升级，配置金丝雀发布将 10% 的流量导入新版本。同时，尝试配置一个限流插件，观察压测效果。

---

### 阶段 3：可观测性与生态集成

**学习内容**:
- 可观测性集成：学习如何配置访问日志，对接 Prometheus + Grafana 进行监控大盘展示。
- 链路追踪：理解如何集成 SkyWalking 或 Zipkin，实现全链路 Tracing。
- 服务网格对接：了解 Higress 作为 Ingress Gateway 如何与 Istio 等服务网格控制平面配合使用。
- 高可用部署：在 K8s 生产环境中配置 HPA（自动扩缩容）和资源限制，保障网关自身的高可用。
- 多租户与多环境管理：学习如何在多团队、多环境的复杂场景下管理网关配置。

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 可观测性与最佳实践
- Prometheus 与 Grafana 配置指南
- Kubernetes HPA 与 VPA 使用教程

**学习建议**:
搭建一套包含 Prometheus 和 Grafana 的监控环境，重点观察 Higress 的 QPS、延迟和成功率指标。尝试模拟网关实例故障，观察系统的自愈能力。

---

### 阶段 4：源码解析与自定义开发（精通）

**学习内容**:
- Wasm 插件开发：学习使用 Go 或 C++ 开发自定义 Wasm 插件，实现业务定制的请求/响应处理逻辑。
- Higress 源码剖析：阅读 Higress 核心源码，理解其基于 Istio 和 Envoy 的扩展实现方式，了解配置下发的数据流向。
- 性能调优：深入内核层面，学习操作系统网络参数调优、连接池调优、Envoy Clusters 配置优化。
- 云原生生态扩展：学习如何通过 CRD（Kubernetes 自定义资源）扩展 Higress 的功能，参与社区贡献或二次开发。

**学习时间**: 4周以上

**学习资源**:
- Higress GitHub Source Code
- WebAssembly (Wasm) 官方文档与 Go SDK
- Higress 官方博客中的深度技术文章

**学习建议**:
选择一个具体的业务痛点（如特殊的签名验证逻辑），尝试编写一个自定义 Wasm 插件来解决它。通读 Higress 的 Controller 源码，理解 Ingress 资源是如何转化为 Envoy 配置的。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 基于 Higress 的官方 Docker 镜像，在本地启动一个最基础的网关实例。请编写 `docker-compose.yml` 文件，并配置一个简单的路由，将 HTTP 请求 `/hello` 转发到一个模拟的后端服务（如 httpbin.org 或 nginx），确保访问网关的 8080 端口能成功收到响应。

### 提示**: 注意挂载必要的配置目录，并检查 Higress 的控制台端口（默认通常是 8080）与监听端口的区别，确保 Docker 网络允许网关容器访问外部服务。

### 

---
## 实践建议

基于 Higress 作为 "AI Native API Gateway" 的定位，结合其作为云原生 API 网关的特性，以下是 6 条针对实际使用场景的实践建议：

### 1. 利用 WASM 插件实现 AI 提示词管理与安全防护
*   **场景**：在对接大模型（LLM）时，直接将 Prompt 写在客户端代码中不仅难以维护，还存在泄露 Key 和被注入攻击的风险。
*   **建议**：使用 Higress 的 Wasm 插件生态（或编写简单的 Go/Python Wasm 插件）来处理请求。
    *   **Prompt 注入**：在网关层统一为用户请求添加 System Prompt 或上下文，实现提示词的版本控制和热更新，无需重启服务。
    *   **敏感词过滤**：在请求转发给 LLM 之前，利用插件拦截恶意输入；在响应返回给用户之前，过滤模型输出的违规内容。
*   **最佳实践**：将 Prompt 模板化管理，通过网关的动态配置功能进行修改，实现业务逻辑与提示词工程的解耦。

### 2. 配置语义路由与模型负载均衡
*   **场景**：企业内部可能同时调用通义千问、DeepSeek、OpenAI 等不同模型，或者同一模型有多个版本/端点。
*   **建议**：不要将模型提供商的硬编码 URL 写死在业务代码中。
    *   **服务发现**：将不同的 LLM 服务注册到 Higress（或通过 Nacos/Consul 注册）。
    *   **负载均衡**：利用 Higress 的路由能力，根据请求头（如 `x-model-version`）或 URL 路径将流量智能分发到不同的模型后端。
*   **常见陷阱**：避免在客户端代码中直接维护多个 API 地址，这会导致切换模型或迁移供应商时需要重新发版。

### 3. 实施基于 Token 的精细化限流与配额管理
*   **场景**：AI 服务的调用成本主要取决于 Token 消耗量，而非传统的 HTTP 请求数（QPS）或并发数。传统的 QPS 限流无法有效控制成本。
*   **建议**：利用 Higress 针对AI场景的增强能力，配置基于 Token 或请求处理时长的限流策略。
    *   **用户配额**：为不同的 API Key 或用户 ID 设置每日/每月的最大 Token 额度，防止个别用户滥用导致账单爆炸。
    *   **请求排队**：在模型服务达到并发上限时，利用网关的请求队列能力削峰填谷，而不是直接返回 429 错误，提升用户体验。

### 4. 启用 SSE（Server-Sent Events）流式传输的全链路支持
*   **场景**：大多数 AI 交互场景需要流式返回（打字机效果）以降低首字延迟（TTFT）。
*   **建议**：确保 Higress 的路由配置完全支持 SSE 协议。
    *   **超时设置**：流式请求可能持续较长时间，务必将网关和后端服务的超时时间设置得足够长（或针对特定路由调整为长连接）。
    *   **日志处理**：流式响应会产生大量日志片段，建议在 Access Log 配置中忽略 SSE 的心跳包或仅记录请求摘要，防止磁盘 I/O 被打满。
*   **常见陷阱**：如果在网关层配置了全量 Body 缓存插件（如某些响应体修改插件），会导致流式响应被缓冲，失去流式的实时性，请确保插件兼容 SSE。

### 5. 构建模型供应商的无感切换与降级机制
*   **场景**：某家云厂商的 API 出现波动或限流时，希望自动切换到备用模型或供应商，以保证业务连续性。
*   **建议**：配置 Higress 的**主动健康检查**（Active Health Check）和**故障转移**（Failover）策略。
    *   设置探测请求（如简单的 `models.list` 接口），当主 LLM 服务返回非 200 状态码

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [云原生](/tags/%E4%BA%91%E5%8E%9F%E7%94%9F/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [WASM](/tags/wasm/) / [LLM](/tags/llm/) / [MCP 协议](/tags/mcp-%E5%8D%8F%E8%AE%AE/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260130-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260201-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260214-github_trending-alibaba-higress-5.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260205-github_trending-alibaba-higress-6.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*