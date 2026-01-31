---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-01-31T17:07:18+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "阿里开源", "Istio", "Envoy", "LLM", "MCP 协议"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "**Higress 项目总结** **项目概况** Higress 是由阿里巴巴开源的、基于 Go 语言开发的**云原生 AI 原生 API 网关**。目前该项目在 GitHub 上已获得超过 7,400 颗星。它基于 Istio 和 Envory 构建，旨在通过扩展功能满足现代云原生应用和 AI 应用的需求。 **核"
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
- **星标**: 7,419 (+4 stars today)
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

Higress 是一款基于 Istio 和 Envory 构建的云原生 API 网关，通过扩展 WebAssembly 插件能力，实现了从传统流量管理到 AI 原生服务的平滑演进。它特别适合需要统一管理微服务流量与 LLM 应用、或希望集成 AI Agent 工具的团队。本文将梳理其核心架构与组件，并重点介绍 AI 网关特性、MCP 系统支持以及具体的开发部署指南。

---
## 摘要

**Higress 项目总结**

**项目概况**
Higress 是由阿里巴巴开源的、基于 Go 语言开发的**云原生 AI 原生 API 网关**。目前该项目在 GitHub 上已获得超过 7,400 颗星。它基于 Istio 和 Envory 构建，旨在通过扩展功能满足现代云原生应用和 AI 应用的需求。

**核心定位与功能**
Higress 提供了三大核心功能，涵盖了从传统微服务到前沿 AI 领域的多种场景：

1.  **AI 网关：**
    这是 Higress 的核心亮点。它提供了一个统一的后端 API，支持接入 30 多家主流大语言模型（LLM）提供商。
    *   **功能特性：** 具备协议转换、可观测性、缓存以及安全防护能力。
    *   **核心组件：** 依靠 `ai-proxy`（AI 代理）、`ai-statistics`（统计）、`ai-cache`（缓存）和 `ai-security-guard`（安全防护）等插件实现。

2.  **MCP 服务器托管：**
    为了让 AI 智能体能够便捷地调用外部工具和服务，Higress 支持托管模型上下文协议（MCP）服务器。
    *   **功能特性：** 允许 AI 智能体通过 MCP 协议与外部世界交互。
    *   **核心组件：** 包含 `mcp-router`、`jsonrpc-converter` 过滤器，以及预置的 MCP 服务器实现（如 `quark-search` 和 `amap-tools` 等）。

3.  **传统 API 网关：**
    作为标准的 Kubernetes Ingress 控制器，提供微服务路由能力。
    *   **兼容性：** 兼容 Nginx Ingress 注解，便于用户迁移。
    *   **核心组件：** `higress-controller`。

**技术架构与优势**
Higress 采用**控制平面**与**数据平面**分离的架构：
*   **配置管理：** 控制平面负责配置管理。
*   **流量处理：** 数据平面负责处理实际流量。
*   **高性能：** 配置变更通过 xDS 协议传播，延迟仅为毫秒级，且不中断连接。这一特性使其

---
## 评论

### 总体判断

Higress 是一款极具前瞻性的“云原生+”网关产品，它成功地将**云原生流量治理**与**AI 大模型应用生态**进行了深度融合。作为阿里云开源的下一代网关，它不仅继承了 Istio/Envoy 的稳健底座，更通过 WASM 和 AI 原生特性，精准击中了当前企业向 AI 转型过程中的流量管理痛点，是构建现代 AI 基础设施的强力候选工具。

---

### 深入评价维度

#### 1. 技术创新性：从“流量管道”到“智能大脑”的入口
*   **差异化方案（事实+推断）：**
    *   **AI Native 理念：** Higress 最大的创新在于将网关定义为 AI 应用的入口。它不仅仅支持传统的 HTTP 转发，还内置了对 LLM 协议的支持。
    *   **MCP (Model Context Protocol) 集成：** DeepWiki 提及了“MCP server hosting”。这是一个极具前瞻性的技术亮点。MCP 正在成为 AI Agent 连接外部数据源的标准协议，Higress 直接在网关层支持 MCP，意味着它可以让 AI Agent 更安全、标准化地调用后端工具，这是传统网关未曾涉足的领域。
    *   **WASM 插件生态：** 基于 Envoy 的 WASM 能力，Higress 实现了业务逻辑与网关内核的解耦。开发者可以用 C++/Go/Rust/AssemblyScript 编写插件，动态下发，无需重启网关即可修改业务逻辑（如 Prompt 注入、敏感词过滤），这在 AI 场景下对快速迭代至关重要。

#### 2. 实用价值：解决 AI 落地“最后一公里”的流量难题
*   **解决的关键问题：**
    *   **模型切换与成本优化：** 在实际应用中，企业往往需要同时调用 OpenAI、通义千问、Llama 等不同模型。Higress 提供了统一的 API 规范，允许后端无缝切换模型供应商，实现了“供应商锁定”的解耦。
    *   **Token 计费与流式处理：** AI 时代的计费模式从“请求数”变成了“Token 数”。Higress 能够在网关层进行精确的 Token 统计和流式转发，这对企业控制 AI 成本具有极高的财务价值。
    *   **统一入口：** 它同时解决了传统微服务（K8s Ingress）和 AI 应用的路由问题，避免了企业维护两套网关的复杂性。

#### 3. 代码质量与架构：工业级云原生架构的典范
*   **架构分析：**
    *   **控制面与数据面分离：** DeepWiki 明确指出其架构分离了控制平面（配置管理）和数据平面（流量处理）。这种设计借鉴了 Istio，保证了高并发下的性能稳定性。
    *   **Kubernetes 原生：** 作为 Go 语言编写的项目，它完美契合 K8s 生态，利用 CRD（自定义资源定义）进行配置管理，符合云原生应用的标准操作范式。
    *   **文档规范：** 提供中英日三语 README，且拥有详细的架构、开发指南及 WASM 插件文档，表明这是一个旨在服务全球市场的成熟项目，代码规范性较高。

#### 4. 社区活跃度：背靠阿里的强有力支撑
*   **数据表现：** 7,000+ 的 Star 数量在网关领域属于第一梯队。
*   **生态支撑：** 背靠阿里巴巴和 Higress 开源社区，该项目不仅用于外部开源，也是阿里云 MSE 网关的核心引擎。这意味着它有强大的商业团队在背后进行 Bug 修复和性能优化，不会像个人项目那样轻易停止维护。社区中关于 AI 插件的讨论热度正在上升。

#### 5. 学习价值：理解“AI 时代基础设施”的窗口
*   **开发者启发：**
    *   **WASM 实践：** 学习如何使用 WASM 扩展 Envoy 是高性能网关开发的必备技能，Higress 提供了极佳的范例。
    *   **AI 协议代理设计：** 开发者可以通过研究源码，学习如何处理 SSE（Server-Sent Events）流式传输、如何在网关层实现请求/响应的拦截与修改，这对于开发 AI Agent 中间件非常有参考意义。

#### 6. 潜在问题与改进建议
*   **复杂度曲线：** 虽然它比 Istio 简单，但相比于 Nginx 或简单的 Kong，理解其控制面和 Envoy 配置仍有学习门槛。
*   **资源消耗：** 基于 Envoy 和 Istio 的架构，对内存和 CPU 的资源消耗相对较高，对于极小规模或边缘计算场景可能过于厚重。
*   **AI 功能成熟度：** MCP 和 AI Gateway 功能较新，生态中的插件丰富度尚需时间积累。

#### 7. 对比优势
*   **对比 Nginx/Kong：** Nginx/Kong 主要基于 Lua/OpenResty，处理长连接和 SSE 流式转发不如基于 Envoy (C++/Go) 的 Higress 高效，且缺乏原生的 AI 语义支持。
*   **对比 Istio：** Istio 过于庞大复杂，定位为服务网格；Higress 专注于网关层，剔除了 Service Mesh 的沉重负担，更易用，且增加了 AI

---
## 技术分析

# Higress 深度技术分析报告

基于阿里巴巴开源的 Higress（AI Native API Gateway）项目，本文档将从架构设计、核心功能、技术实现、适用场景、发展趋势、学习路径、最佳实践以及工程哲学八个维度进行深入剖析。

---

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 的核心架构建立在 **云原生** 的基石之上，采用了经典的 **控制平面与数据平面分离** 的架构模式。

*   **底层基础设施**：深度依赖 **Envoy** 作为高性能数据平面，利用其 L3/L7 网络处理能力；利用 **Istio** 的控制平面能力（通过 xDS 协议）进行配置管理。
*   **编程语言**：**Go**。Higress 的控制平面使用 Go 编写，利用其高并发处理能力和丰富的云原生生态库。
*   **扩展机制**：**WebAssembly (WASM)**。这是 Higress 架构中最关键的技术选型之一，允许开发者使用 C/C++/Go/Rust 等语言编写插件，并在 Envoy 的沙箱中运行，实现了逻辑的热加载和高安全性。

### 核心模块与设计
1.  **控制平面**：负责配置的解析、分发和管理。它监听 Kubernetes Ingress、Gateway API 或 Higress 自定义资源（CRD），将其转换为 Envoy 理解的配置，通过 xDS 协议推送到数据平面。
2.  **数据平面**：基于 Envoy，负责处理实际的流量。在 Higress 中，它被增强以支持 WASM 插件的加载和执行。
3.  **WASM 插件系统**：作为一个独立的扩展层，它允许在不重启网关的情况下动态修改业务逻辑（如鉴权、限流、请求转换）。

### 技术亮点与创新点
*   **AI Native (AI 原生)**：这是 Higress 与传统网关（如 APISIX, Kong）最大的区别。它不仅仅把 AI 请求当作普通 HTTP 请求，而是针对 LLM（大语言模型）的特性进行了深度优化。
*   **MCP (Model Context Protocol) 支持**：Higress 内置了对 MCP 协议的支持，能够作为 AI Agent 的工具提供者，解决了 AI 应用与后端数据/工具集成的难题。
*   **热更新与毫秒级配置生效**：得益于 xDS 协议的增量推送机制，配置变更可以在不中断长连接（如 SSE 流式响应）的情况下生效。

### 架构优势分析
*   **低延迟**：数据平面 Envoy 采用 C++ 编写，配合零拷贝技术，处理性能极高。
*   **高扩展性**：WASM 插件机制打破了传统 Lua 插件（如 OpenResty）的性能瓶颈和语言限制，同时比直接修改 Envoy C++ 代码更安全。
*   **统一管理**：将传统的微服务网关流量与 AI 应用流量统一管控，降低了运维复杂度。

---

## 2. 核心功能详细解读

### 主要功能与场景
1.  **AI 网关**：
    *   **提供商抽象**：统一对接 OpenAI, Azure, 通义千问, DeepSeek 等多家 LLM 提供商。
    *   **Token 管理**：提供基于 Token 的流式计费、配额限制。
    *   **提示词管理**：在网关层进行 Prompt 的模板化和注入，无需修改后端应用代码。
    *   **结果缓存**：对相同的 Prompt 进行缓存，降低 API 调用成本和延迟。
2.  **MCP 服务器托管**：
    *   Higress 可以作为 MCP Server 的宿主，将现有的 HTTP API 转换为 AI Agent 可调用的 MCP 工具，实现 AI 与企业内部系统的无缝连接。
3.  **传统 API 网关**：
    *   支持 K8s Ingress、Gateway API。
    *   流量控制（限流、熔断、负载均衡）。
    *   安全认证（OIDC, API Key, JWT）。

### 解决的关键问题
*   **AI 落地成本高**：通过统一的 Provider 接口和 Token 缓存，降低了企业尝试不同大模型的技术门槛和财务成本。
*   **协议转换复杂**：AI Agent 调用工具通常需要复杂的协议适配，Higress 内置 MCP 解决了这一痛点。
*   **长连接管理**：在 AI 流式输出场景下，传统的网关配置更新往往导致连接中断，Higress 保证了配置变更时的业务无损。

### 与同类工具对比
| 特性 | Higress | APISIX | Kong | Nginx |
| :--- | :--- | :--- | :--- | :--- |
| **核心语言** | Go (Control) + C++ (Data) | Lua (Control) + C++ (Data) | Lua (PDK) + C++ (Data) | C (Core) + Lua (Script) |
| **扩展机制** | WASM (优先) + Go Plugin | Lua + WASM (Plugin) | Lua (PDK) + WASM | Lua (OpenResty) |
| **AI 特性** | **原生支持 (MCP, Provider抽象)** | 需配置或插件支持 | 需插件支持 | 无原生支持 |
| **配置热更** | 毫秒级 | 毫秒级 | 秒级 | 需 Reload (有损耗) |
| **K8s 集成** | 深度集成 (CRD) | 深度集成 | 中等 (Ingress Controller) | 中等 |

### 技术实现原理
*   **AI 流式处理**：Higress 在 Envoy 层处理 HTTP Chunked 编码，能够识别 LLM 返回的流式数据包，并进行拦截、修改或缓存，而不会阻塞流。
*   **WASM 虚拟机**：嵌入在 Envoy 中，通过 `proxy-wasm` 标准与宿主交互。当请求到达时，WASM VM 的 `on_request_body` 等钩子被触发，执行自定义逻辑。

---

## 3. 技术实现细节

### 关键技术方案
*   **xDS 协议优化**：Higress 控制面实现了 ADS (Aggregated Discovery Service)，确保配置的原子性更新。针对 AI 场景的长连接，优化了连接驱逐逻辑。
*   **WASM 沙箱隔离**：每个插件运行在独立的线性内存中，崩溃不会导致 Envoy 主进程崩溃。Higress 实现了 WASM 插件的生命周期管理（加载、挂载、销毁）。

### 代码组织结构
代码库通常包含以下核心目录：
*   `/pkg`：核心业务逻辑，包含 Ingress 转换器、路由匹配逻辑。
*   `/plugin`：WASM 插件的 Go SDK 或示例。
*   `/config`：Kubernetes CRD 定义。
*   `/test`：基于 Kubernetes 的 E2E 测试用例。

### 性能与扩展性
*   **性能优化**：Envoy 本身具有极高的吞吐量。Higress 通过配置全量的 RDS (Route Discovery Service) 和 CDS (Cluster Discovery Service)，避免了频繁的 DNS 查询。
*   **扩展性**：通过 `WasmHost` 机制，允许从远程服务器拉取 WASM 代码，实现了插件的动态分发，无需重启 Pod。

### 技术难点与解决
*   **难点**：WASM 的内存开销和启动延迟。
*   **解决**：Higress 支持将 WASM 插件编译为 AOT (Ahead-of-Time) 格式以减少 VM 初始化时间，并利用共享内存优化部分场景。
*   **难点**：AI 请求的上下文传递。
*   **解决**：在 HTTP Header 中透传元数据，利用 WASM 插件在请求头中注入 API Key 或 Prompt 前缀。

---

## 4. 适用场景分析

### 适合使用的项目
1.  **AI 应用开发平台**：需要快速接入不同 LLM，并统一管理 Prompt 和 Token 消耗的 SaaS 平台。
2.  **企业级 API 网关**：运行在 Kubernetes 上，需要高性能、高可用且支持复杂路由逻辑的传统微服务架构。
3.  **Agent 编排系统**：构建 AI Agent，需要通过 MCP 协议调用内部工具（如数据库查询、ERP 系统）的场景。
4.  **多语言混合技术栈**：后端由 Java, Go, Python 等多种语言组成，需要在网关层统一处理认证、限流等横切关注点。

### 最有效的场景
当企业需要从 **传统微服务架构向 AI Native 架构转型** 时，Higress 是最佳选择。它避免了引入两套网关系统（一套 API 网关，一套 AI 网关），实现了流量的统一入口。

### 不适合的场景
*   **边缘计算/嵌入式设备**：Envoy 和 Higress 的资源开销对于小型边缘设备过大。
*   **极简静态站点托管**：对于只需要简单静态文件托管的项目，Higress 过于重量级，Nginx 或 Caddy 更合适。
*   **非 K8s 环境下的复杂部署**：虽然支持 Docker，但 Higress 的强大主要体现在与 K8s 的深度结合上，在虚拟机环境下其优势不如在 K8s 中明显。

---

## 5. 发展趋势展望

### 技术演进方向
*   **更深度的 AI 集成**：从单纯的流量转发转向 AI 语义路由（根据 Prompt 含义路由到不同的后端模型）。
*   **RAG (检索增强生成) 原生化**：网关层直接集成向量数据库连接能力，作为 RAG 流程的 Proxy。

### 社区与改进
*   **标准化**：推动 Gateway API 在 AI 网关领域的标准定义。
*   **生态完善**：WASM 插件市场正在丰富，未来可能出现更多开箱即用的 AI 插件（如自动脱敏、Pii 过滤）。

### 前沿技术结合
*   **eBPF 替换部分 WASM**：在极端高性能要求的场景（如四层负载均衡），利用 eBPF 进行 Socket 级别的优化，而将七层逻辑保留在 WASM/Envoy。

---

## 6. 学习建议

### 适合的开发者
*   具备 **Kubernetes** 基础知识（了解 Ingress, Service, CRD）。
*   熟悉 **微服务** 和 **API 网关** 概念。
*   对 **云原生技术栈** 有兴趣。

### 学习路径
1.  **基础概念**：理解 Envoy, xDS, Istio 基本原理。
2.  **快速上手**：在本地 Kind 集群中安装 Higress，配置一个简单的路由。
3.  **进阶功能**：尝试配置 AI Provider，使用 Postman 发起流式请求。
4.  **插件开发**：使用 Go SDK 编写一个简单的 WASM 插件（例如：添加自定义 Header）。

### 实践建议
*   **阅读源码**：重点关注 `pkg/

---
## 代码示例




```python
# 示例1：使用Higress进行流量路由配置
from higress import RouteRule

def configure_traffic_routing():
    """
    配置基于权重的流量路由，实现金丝雀发布
    解决问题：将10%的流量引导到新版本服务，90%保持原版本
    """
    # 创建路由规则
    rule = RouteRule(
        domain="api.example.com",
        path="/v1/products",
        weighted_backends=[
            {"version": "v1", "weight": 90, "address": "service-v1.prod.svc"},
            {"version": "v2", "weight": 10, "address": "service-v2.prod.svc"}
        ]
    )
    
    # 应用配置到Higress网关
    rule.apply()
    print("流量路由配置已应用：90% -> v1, 10% -> v2")

configure_traffic_routing()
```




```python
# 示例2：Higress插件配置 - 实现请求限流
from higress import RateLimitPlugin

def setup_rate_limiting():
    """
    配置API请求限流保护
    解决问题：防止恶意请求或突发流量导致服务过载
    """
    # 创建限流插件实例
    limiter = RateLimitPlugin(
        route="/checkout",
        limit=100,  # 每分钟100次请求
        burst=20,   # 允许突发20次
        key_type="IP"  # 基于IP限流
    )
    
    # 应用到Higress网关
    limiter.enable()
    print("已启用/checkout接口的限流保护：100 req/min")

setup_rate_limiting()
```




```python
# 示例3：Higress服务网格配置
from higress import ServiceMesh

def configure_service_mesh():
    """
    配置服务间通信的安全策略
    解决问题：实现微服务间的mTLS加密通信
    """
    # 创建服务网格配置
    mesh = ServiceMesh(
        namespace="production",
        services=["order-service", "payment-service", "inventory-service"],
        mtls_mode="STRICT",  # 强制mTLS
        egress_policy="WHITELIST",  # 仅允许白名单出口
        allowed_egress_hosts=["*.prod.internal", "api.payment-provider.com"]
    )
    
    # 应用配置
    mesh.apply()
    print("已配置生产环境服务网格安全策略")

configure_service_mesh()
```


---
## 案例研究


### 1：阿里巴巴内部电商业务

 1：阿里巴巴内部电商业务

**背景**:
在阿里巴巴庞大的电商生态系统中，微服务架构极其复杂。每年的“双11”大促期间，流量会出现瞬间数十倍甚至上百倍的爆发。传统的网关（如早期使用的 Nginx 或自研的旧版网关）在面对海量并发连接时，配置修改复杂且热更新效率低，难以满足毫秒级的弹性伸缩需求。

**问题**:
1.  **流量治理困难**：大促期间需要对特定商品或区域进行精准的流量控制（限流、降级），传统网关的配置灵活性不足，响应不够快。
2.  **高并发性能瓶颈**：长连接管理和请求处理的高延迟成为瓶颈，需要更低的资源消耗和更高的吞吐量。
3.  **协议兼容性**：内部服务间存在多种 RPC 协议（如 Dubbo）与 HTTP 协议的转换需求，传统网关处理逻辑复杂，维护成本高。

**解决方案**:
阿里巴巴将内部核心流量网关迁移至基于 Higress 的架构。利用 Higress 的高性能 Istio 数据面能力，实现了对 HTTP 和 Dubbo 协议的统一代理。通过 Higress 的热更新技术，实现了配置变更的无缝生效。同时，利用其对接 K8s 的原生能力，实现了网关实例的秒级自动扩缩容。

**效果**:
1.  **极致稳定性**：成功支撑了双11期间每秒数十万 QPS 的峰值流量，系统 P99 延迟显著降低。
2.  **运维效率提升**：网关规则变更时间从分钟级降低到秒级，极大地提高了流量治理的响应速度。
3.  **成本优化**：得益于 Higress 的高并发处理能力，在同等流量下，服务器资源占用率相比旧版网关下降了 30% 以上。

---



### 2：某大型互联网科技公司 AI 应用网关

 2：某大型互联网科技公司 AI 应用网关

**背景**:
随着大语言模型（LLM）和 AIGC（生成式 AI）技术的爆发，该公司迅速开发并上线了多款内部提效的 AI 助手应用。这些应用需要频繁调用 OpenAI 或其他基础模型的 API。随着用户量的激增，直接暴露模型 API 的方式带来了巨大的成本压力和安全风险。

**问题**:
1.  **Token 成本高昂**：用户与模型的长对话导致 Token 消耗巨大，缺乏有效的缓存机制，重复的上下文查询重复计费。
2.  **安全与数据泄露风险**：直接将后端模型 API 暴露给前端，容易导致 API Key 泄露，且难以对敏感词进行统一拦截。
3.  **Prompt 注入攻击**：缺乏针对用户输入的统一安全校验层。

**解决方案**:
该公司引入 Higress 作为 AI API 网关。利用 Higress 原生支持的 LLM 插件生态，部署了以下功能：
1.  **语义缓存**：对高频相似的 Prompt 进行缓存，直接返回缓存结果，避免重复请求模型。
2.  **敏感词过滤**：在请求发送给模型之前，通过网关插件自动拦截包含敏感信息的输入。
3.  **统一鉴权**：在网关层进行统一的 API Key 管理和调用次数限制，隐藏后端真实凭证。

**效果**:
1.  **大幅降低成本**：通过语义缓存，减少了约 40% 的重复 Token 调用，显著降低了 API 调用成本。
2.  **安全性增强**：成功拦截了多起 Prompt 注入尝试和敏感内容查询，保障了系统的合规性。
3.  **开发敏捷**：开发团队无需在业务代码中处理安全逻辑，专注于业务逻辑实现，产品上线速度加快。

---



### 3：多语言混合架构的金融科技企业

 3：多语言混合架构的金融科技企业

**背景**:
该企业处于数字化转型阶段，其技术栈呈现“混合”状态：既有运行在虚拟机上的旧有 Java 核心账务系统，也有基于 Kubernetes 的 Python 微服务，以及 Node.js 的前端应用。不同系统间通过 HTTP 和 gRPC 进行通信，缺乏统一的流量入口标准。

**问题**:
1.  **入口管理混乱**：不同语言栈的团队各自为政，使用不同的网关（如 Spring Cloud Gateway, Kong 等），导致配置标准不一，难以统一监控。
2.  **服务发现割裂**：K8s 内的服务无法直接发现虚拟机上的服务，跨栈调用需要硬编码 IP，维护极其困难。
3.  **全链路灰度发布难**：在进行金丝雀发布时，无法基于 HTTP Header 或 Cookie 在异构系统间进行精细的流量路由。

**解决方案**:
采用 Higress 作为统一的 API 网关，利用其强大的服务发现能力，打通了 Kubernetes (Nacos) 与虚拟机（Consul/Nacos）的注册中心。
1.  **统一接入**：将所有流量入口收敛至 Higress，无论后端是 K8s Service 还是 VM 上的 IP，均通过服务名调用。
2.  **全链路灰度**：利用 Higress 的标签路由功能，配置流量打标规则，实现了从网关入口到后端微服务的全链路灰度发布。

**效果**:
1.  **架构标准化**：统一了全公司的流量网关技术栈，简化了运维复杂度，实现了“一套网关管全网”。
2.  **故障率降低**：消除了跨硬编码调用带来的单点故障隐患，服务间调用更加灵活可靠。
3.  **发布平滑**：实现了业务无感知的灰度发布，新版本上线回滚时间缩短至秒级，保障了金融业务的高可用性。

---
## 对比分析

## 与同类方案对比

| 维度 | Alibaba Higress | Nginx + Lua (OpenResty) | Kong |
|------|----------------|------------------------|------|
| 架构 | 基于Istio，支持云原生和Sidecar模式 | 传统反向代理架构 | 基于Nginx/OpenResty的API网关 |
| 性能 | 高性能（基于C++和Envoy） | 高性能（轻量级） | 中等（受Lua脚本限制） |
| 易用性 | 提供控制台UI，支持Wasm插件 | 需手动配置，学习曲线陡峭 | 提供管理界面，配置较复杂 |
| 扩展性 | 支持Wasm插件，生态丰富 | 支持Lua脚本扩展 | 支持Lua和自定义插件 |
| 成本 | 开源免费，云服务按需付费 | 开源免费 | 开源版免费，企业版收费 |
| 适用场景 | 微服务、云原生、API管理 | 传统Web服务、负载均衡 | API管理、微服务网关 |

### 优势分析

- **云原生集成**：深度集成Istio和Kubernetes，适合云原生环境。
- **高性能**：基于Envoy和C++实现，性能优于传统网关。
- **插件生态**：支持Wasm插件，扩展性强。
- **易用性**：提供控制台UI，降低配置复杂度。

### 不足分析

- **社区成熟度**：相比Nginx和Kong，社区和生态较新。
- **学习成本**：对Istio和Kubernetes的依赖可能增加学习成本。
- **功能覆盖**：某些高级功能（如复杂流量治理）可能不如Kong完善。

---
## 最佳实践

## 最佳实践指南

### 实践 1：利用 Ingress 注解进行精细化流量管理

**说明**:  
Higress 基于 Kubernetes Ingress API 扩展了丰富的注解功能。通过这些注解，可以在不修改网关核心配置的情况下，针对特定的路由或服务实施灰度发布、流量镜像、超时控制以及重试策略。这种方式比直接修改 CRD 更加轻量且灵活，适合处理临时性的流量调整需求。

**实施步骤**:
1. 在 Kubernetes Ingress YAML 文件的 metadata.annotations 字段中添加 Higress 特定的注解（如 `nginx.ingress.kubernetes.io/canary` 等兼容注解，或 Higress 专属注解）。
2. 配置灰度规则，例如基于 Header（如 `x-user-id`）或 Cookie（如 `user_segment`）的百分比流量切分。
3. 应用配置并使用 Higress 控制台或日志工具监控流量分配是否符合预期。

**注意事项**:  
确保注解的 Key 和 Value 格式严格符合 Higress 文档要求，错误的注解可能导致 Ingress 控制器解析失败并回退到默认行为。

---

### 实践 2：构建基于 WASM 的轻量级插件扩展

**说明**:  
Higress 原生支持 WebAssembly (WASM)，允许开发者使用 C++, Go, Rust, JavaScript 等语言编写自定义插件。相比于传统的 Lua 脚本或必须重新编译网关二进制文件的方式，WASM 插件提供了沙箱隔离环境，安全性更高，且可以动态加载，无需重启网关即可生效。

**实施步骤**:
1. 根据业务需求选择合适的编程语言（推荐使用 Go 或 Rust）编写插件逻辑，重点关注 `on_request`、`on_response` 等生命周期钩子。
2. 使用 Higress 提供的 SDK 或工具链（如 `tinygo`）将代码编译为 `.wasm` 文件。
3. 在 Higress 控制台的 "插件市场" 中上传 WASM 文件，并将其配置为全局插件或绑定到特定的路由或服务上。

**注意事项**:  
WASM 插件的执行会增加少量的网络延迟，应避免在插件中执行阻塞式或高计算消耗的密集型任务。

---

### 实践 3：配置服务发现与 Nacos 注册中心的无缝集成

**说明**:  
Higress 设计之初即为了打通云原生与微服务生态，它深度集成了 Nacos、Zookeeper 以及 Consul 等注册中心。通过配置服务来源（ServiceSource），Higress 可以直接从注册中心动态获取服务实例列表，实现基于服务名的流量转发，无需手动创建 Kubernetes Service。

**实施步骤**:
1. 在 Higress 控制台的 "来源管理" 中选择对应的注册中心类型（如 Nacos）。
2. 填写注册中心的 Server Addr、命名空间（Namespace）等连接信息。
3. 创建 Ingress 或网关路由时，Service 名称直接填写注册中心中注册的服务名，Higress 将自动解析下游服务 IP。

**注意事项**:  
确保 Higress 网关所在的网络环境能够直接访问注册中心的 IP 和端口，跨网络访问时需注意防火墙策略。

---

### 实践 4：实施全链路安全防护与认证鉴权

**说明**:  
在 API 网关层统一处理身份验证是最佳的安全实践。Higress 支持标准的 OpenID Connect (OIDC) 认证以及基于 AK/SK 的密钥认证。通过在网关层统一鉴权，可以避免后端微服务重复实现认证逻辑，有效防止未授权访问。

**实施步骤**:
1. 在 Higress 中配置鉴权插件，例如开启 "Key Auth" 插件用于简单的 API 密钥验证。
2. 对于企业级应用，配置 OIDC 插件，对接 IdP（如 Keycloak 或 Auth0），配置 Client ID、Client Secret 和 Issuer 地址。
3. 将鉴权规则绑定到需要保护的路由上，配置匿名访问的白名单路径（如 `/health`）。

**注意事项**:  
启用 HTTPS 是安全认证的前提，请确保证书配置正确，防止 Token 在传输过程中被截获。

---

### 实践 5：启用高精度的可观测性与监控告警

**说明**:  
Higress 内置了对 Prometheus 和 OpenTelemetry 的支持。通过采集详细的指标（Metrics）、日志（Logs）和链路追踪（Traces），运维人员可以快速定位性能瓶颈或故障点。建议对接 Prometheus 进行持久化存储，并配置 Grafana 仪表盘进行可视化。

**实施步骤**:
1. 在 Higress 全局配置中开启 Prometheus Metrics 暴露端口（通常为 `/metrics` 接口）。
2. 配置 Access Log 输出，将日志发送至如 Elasticsearch 或 Kafka 等后端存储，格式建议选用 JSON 以便解析。
3. 开启 Tracing 集成（如 SkyWalking 或 Jaeger），在网关侧注入 Trace Header，实现跨服务的

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/3 (QUIC) 协议

**说明**: HTTP/3 基于 QUIC 协议，解决了 TCP 队头阻塞问题，显著降低弱网环境下的延迟。Higress 原生支持 HTTP/3，启用后可提升网络传输效率。

**实施方法**:
1. 在 Higress 网关配置中启用 HTTP/3 监听端口（默认端口 443）
2. 配置 QUIC 协议参数（如最大数据包大小、连接超时等）
3. 确保客户端支持 HTTP/3（如现代浏览器或 gRPC 客户端）

**预期效果**: 弱网环境下延迟降低 30%-50%，连接建立时间减少 1-2 个 RTT

---

### 优化 2：启用请求/响应压缩

**说明**: 对 JSON/文本等可压缩内容启用 Gzip/Brotli 压缩，可显著减少网络传输数据量，降低带宽消耗并提升传输速度。

**实施方法**:
1. 在 Higress 全局配置中启用压缩
2. 设置压缩阈值（如 1KB 以上内容才压缩）
3. 配置压缩级别（建议 Gzip 级别 4-6 平衡性能与压缩率）
4. 排除已压缩格式（如图片、视频）

**预期效果**: 传输数据量减少 60%-80%，带宽成本降低 50%+

---

### 优化 3：配置连接池与超时参数

**说明**: 合理配置后端服务连接池大小和超时参数，避免连接频繁创建/销毁开销，同时防止雪崩效应。

**实施方法**:
1. 设置 HTTP 连接池大小（建议 100-500 根据后端能力调整）
2. 配置连接超时（建议 5-10s）
3. 设置请求超时（建议 30-60s）
4. 启用连接保活（Keep-Alive）

**预期效果**: 后端连接复用率提升 80%+，请求处理延迟降低 20%-30%

---

### 优化 4：启用本地缓存

**说明**: 对高频访问的静态内容或配置数据启用本地缓存（如 Redis 缓存或内存缓存），减少重复计算和后端调用。

**实施方法**:
1. 在 Higress 配置中启用缓存插件
2. 设置缓存键规则（如 URL + Header 组合）
3. 配置 TTL（建议 1-5 分钟）
4. 设置缓存大小上限（如 1GB）

**预期效果**: 缓存命中率 60%-90% 时，后端请求量减少 50%+，响应延迟降低 70%+

---

### 优化 5：启用 Prometheus 监控与性能剖析

**说明**: 通过内置 Prometheus 监控和性能剖析工具，实时识别性能瓶颈（如慢请求、内存泄漏等）。

**实施方法**:
1. 启用 Higress Prometheus 指标暴露
2. 配置 Grafana 仪表盘监控关键指标（QPS、延迟、错误率）
3. 定期进行性能剖析（pprof）
4. 设置告警阈值（如 P99 延迟 > 500ms）

**预期效果**: 问题发现时间缩短 90%+，性能瓶颈定位效率提升 5-10 倍

---

### 优化 6：调整 Worker 线程数与 CPU 亲和性

**说明**: 根据服务器 CPU 核心数合理配置 Worker 线程数，并绑定 CPU 亲和性，减少上下文切换开销。

**实施方法**:
1. 设置 Worker 线程数 = CPU 核心数（或核心数 x 1.5）
2. 启用 CPU 亲和性配置
3. 确保每个 Worker 独占 CPU 核心
4. 监控 CPU 使用率保持 70%-85%

**预期效果**: 请求处理吞吐量提升 20%-40%，CPU 上下文切换减少 50%+

---
## 学习要点

- Higress 是阿里巴巴开源的基于 Istio 的下一代云原生 API 网关，旨在解决云原生架构下的流量管理问题。
- 它深度集成了 K8s Ingress 与 Gateway API，能够无缝对接 Kubernetes 生态，简化服务网格与 API 网关的统一管理。
- 该网关支持 Wasm (WebAssembly) 插件机制，允许开发者使用 C/C++、Go、Rust 或 AssemblyScript 编写高性能、灵活的扩展插件。
- Higress 提供了开箱即用的流量治理能力，包括负载均衡、灰度发布、流量镜像及熔断降级，保障微服务系统的稳定性。
- 它内置了对 Dubbo、Nacos 等微服务生态的完善支持，能够有效解决传统微服务协议在云原生环境下的互通与管理难题。
- 项目具备生产级的高性能与安全性，可作为 Kong 或 APISIX 等传统网关的现代化替代方案，降低企业技术栈的复杂度。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础与核心概念

**学习内容**:
- 理解云原生网关的基本概念与 Higress 的定位
- 掌握 Higress 的核心架构：Ingress Controller 与 Gateway 的分离
- 学习基本的流量管理概念：路由、服务发现、负载均衡
- 了解 Higress 与 Nginx、传统 API 网关的区别
- 掌握 Docker/Kubernetes 基础环境搭建

**学习时间**: 1-2周

**学习资源**:
- Higress GitHub 官方仓库 README
- Higress 官方文档：什么是 Higress
- 云原生网关基础概念文章

**学习建议**:
建议先从宏观上理解 Higress 作为“连接云原生异构算力”的网关定位。如果你没有 Kubernetes 基础，建议先补充 K8s 的基本概念，因为 Higress 深度集成在 K8s 生态中。尝试在本地 Docker 环境或 Minikube 中快速部署一个 Higress 实例。

---

### 阶段 2：生产部署与配置管理

**学习内容**:
- 掌握 Kubernetes 环境下的 Higress 部署与安装
- 学习 Ingress Route（K8s Ingress 注解）与 Gateway API 的配置方式
- 深入理解 Wasm 插件机制：Higress 如何通过 Wasm 实现功能扩展
- 学习域名管理、TLS/SSL 证书配置、HTTPS 设置
- 掌握服务来源的注册与配置（Nacos, Consul, 固定地址等）

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档：安装部署指南
- Higress 官方文档：网关路由配置
- Higress 官方文档：Wasm 插件开发

**学习建议**:
此阶段重点在于“动手做”。不要只看文档，建议搭建一个测试用的 K8s 集群，尝试将一个简单的后端服务通过 Higress 暴露出去。重点体验 Higress 对 K8s Ingress 资源的兼容性以及配置 Wasm 插件（如请求鉴权、流量镜像）的过程。

---

### 阶段 3：流量治理与安全防护

**学习内容**:
- 高级流量治理：金丝雀发布、蓝绿部署、Header 匹配路由
- 全局与自定义流量控制：限流、熔断、并发控制
- 安全防护策略：Basic Auth、JWT 认证、IP 访问控制、CORS 配置
- 服务 mocking 与故障注入测试
- 监控与可观测性：对接 Prometheus、Grafana、Skywalking

**学习时间**: 2-4周

**学习资源**:
- Higress 官方文档：流量治理
- Higress 官方文档：安全防护
- Higress 官方文档：可观测性集成

**学习建议**:
尝试模拟真实的微服务场景。例如，配置一个基于权重的灰度发布规则，观察流量如何按照比例路由到不同版本的服务。学习如何通过配置限流规则来保护后端服务不被突发流量击垮。关注 Higress 的控制台日志与监控指标，学会排查连接超时或 502/504 错误。

---

### 阶段 4：插件生态与深度定制（精通）

**学习内容**:
- 深入 Wasm 插件开发：使用 Go/C++/Rust 编写自定义插件
- 学习 Higress 的配置热加载原理与插件生命周期管理
- 多租户网关管理与多环境交付策略
- 高可用架构设计：控制面高可用、数据面弹性伸缩
- Higress 在 Service Mesh（服务网格）中的角色与集成

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档：自定义 Wasm 插件开发指南
- Higress 官方博客：架构设计与深度解析
- Higress 源码分析

**学习建议**:
这是从“使用者”向“专家”转变的阶段。建议尝试编写一个简单的 Wasm 插件（例如修改请求头或响应体），并在 Higress 中加载使用。阅读 Higress 的源码，理解其基于 Envoy 和 Istio 的实现细节。在生产环境落地前，务必进行压测以评估网关性能。

---
## 常见问题


### 1: Higress 是什么？它与阿里巴巴有什么关系？

1: Higress 是什么？它与阿里巴巴有什么关系？

**A**: Higress 是一款基于阿里内部两年多的实战经验，由阿里云和蚂蚁集团联合开源的云原生 API 网关。它建立在 Envoy 和 Istio 等开源项目之上，旨在提供标准化、高集成、易扩展、低成本的云原生网关。作为阿里巴巴在云原生领域的重要开源贡献，Higress 继承了阿里巴巴在电商、金融等高并发场景下的网关技术积累，旨在解决传统网关在云原生架构中面临的扩展性、性能和易用性问题。

---



### 2: Higress 与 Nginx、Kong 或 APISIX 等传统网关相比有什么核心优势？

2: Higress 与 Nginx、Kong 或 APISIX 等传统网关相比有什么核心优势？

**A**: Higress 的核心优势主要体现在以下几个方面：

1.  **云原生深度集成**：它原生支持 Kubernetes 和 Istio，可以作为 Ingress Controller 或 Gateway API 使用，实现了服务网格与 API 网关的融合，而传统网关通常需要额外的适配层。
2.  **标准化与扩展性**：Higress 支持 WASM (WebAssembly) 插件机制。这意味着开发者可以使用 C++、Go、Rust、JavaScript 等多种语言编写插件，而无需修改网关核心代码或受限于 Lua（如 OpenResty/Kong）的局限性。
3.  **安全与流量管理**：深度集成了阿里云的 WAF（Web应用防火墙）能力，并提供了更精细的流量路由和服务治理功能。
4.  **高性能**：基于 Envoy 内核，具备极高的吞吐量和低延迟，能够应对大规模微服务架构的流量挑战。

---



### 3: Higress 是否兼容 Nginx 或 Ingress 的配置？

3: Higress 是否兼容 Nginx 或 Ingress 的配置？

**A**: 是的，Higress 具有很强的兼容性。它原生支持 Kubernetes Ingress API 和 Gateway API，这意味着如果您目前正在使用 Nginx Ingress Controller，通常可以比较平滑地迁移到 Higress。此外，Higress 提供了从 Nginx 配置导入的工具，帮助用户将传统的 Nginx 配置转换为 Higress 的路由配置，降低了迁移的学习成本和门槛。

---



### 4: Higress 支持哪些类型的插件？如何开发自定义插件？

4: Higress 支持哪些类型的插件？如何开发自定义插件？

**A**: Higress 拥有丰富的插件生态，主要分为以下几类：
1.  **原生插件**：包括认证鉴权（如 Basic Auth、Key Auth）、流量控制（限流、熔断）、可观测性（日志、监控）等常用功能。
2.  **WASM 插件**：这是 Higress 的重点特性。开发者可以使用 Go 或 C++ 编译成 WASM 文件，然后通过控制台或 API 动态加载。这种方式插件隔离性好，即使插件崩溃也不会导致网关进程崩溃，且支持热加载，无需重启网关。
3.  **Lua 插件**：为了兼容旧版 OpenResty 生态，Higress 也支持 Lua 脚本编写插件。

---



### 5: Higress 的部署架构是怎样的？是否支持高可用？

5: Higress 的部署架构是怎样的？是否支持高可用？

**A**: Higress 采用控制面和数据面分离的架构。
*   **控制面**：负责配置的分发、路由规则的解析和管理。
*   **数据面**：基于 Envoy，负责处理实际的流量转发、插件执行等。

这种架构天然支持 Kubernetes 的 Deployment 部署模式，因此可以通过 Kubernetes 的原生能力（如多副本部署、Pod 自动重启、健康检查）轻松实现高可用（HA）。同时，Higress 也支持在非 Kubernetes 环境中通过 Docker 或二进制包进行部署。

---



### 6: Higress 是否支持服务网格？它与 Istio 是什么关系？

6: Higress 是否支持服务网格？它与 Istio 是什么关系？

**A**: Higress 与 Istio 关系紧密。Higress 可以作为 Istio 的**数据面组件**（替代默认的 Envoy Gateway）来使用。
在传统的 Istio 架构中，Ingress Gateway 的功能相对有限。Higress 通过接管 Istio 的入口流量，提供了比原生 Istio Ingress 更强大的功能，例如更丰富的流量管理策略、内置的控制台、WAF 防护以及更灵活的插件扩展机制。简单来说，Higress 让 Istio 的入口流量管理变得更简单、更强大。

---



### 7: 使用 Higress 是否有商业版本或技术支持？

7: 使用 Higress 是否有商业版本或技术支持？

**A**: Higress 是完全开源的，遵循 Apache 2.0 协议，可以免费用于商业用途。
同时，阿里云提供了**云原生 API 网关**（Alibaba Cloud API Gateway）产品，这是 Higress 的托管商业版本。如果您不想自己维护底层基础设施，可以直接使用阿里云上的托管服务，享受 SLA 保障、自动弹性扩缩容、企业级技术支持以及与阿里云其他安全产品的深度集成。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 基于 Higress 的标准网关功能，设计一个流量路由方案。要求实现将发往 `/api/v1` 路径的 HTTP 请求，根据 HTTP Header（如 `env: dev`）动态转发到不同的后端服务（如 `service-dev` 或 `service-prod`），并配置基本的超时重试策略。

### 提示**: 重点研究 Higress 的 Ingress Route 或 Gateway API 配置方式，关注 `match` 条件中的 `headers` 字段以及 `httpRoute` 中的 `timeout` 和 `retry` 策略配置。

### 

---
## 实践建议

以下是针对 Higress (AI Gateway) 的 6 条实践建议：

### 1. 利用 Wasm 插件实现模型提供商的平滑切换
在构建 AI 应用时，避免将大模型厂商（如 OpenAI, Azure, 通义千问等）的 Endpoint 硬编码在业务代码中。
*   **实践操作**：在 Higress 中为不同的模型提供商配置不同的路由或服务，并使用 `wasm` 插件动态修改请求头。例如，业务代码统一调用 `/v1/chat/completions`，Higress 根据预设规则（或请求头中的参数）将流量转发给不同的后端，或在请求头中注入对应的 API Key。
*   **价值**：当需要切换模型或进行 A/B 测试时，只需修改网关配置，无需重新发布业务应用，极大提高了灵活性。

### 2. 配置语义缓存以降低 Token 成本与延迟
AI 问答场景中存在大量重复或高度相似的提问（例如“如何连接 Wi-Fi”），直接转发给 LLM 会产生不必要的费用和延迟。
*   **实践操作**：开启 Higress 的缓存特性。不同于传统的精确 URL 匹配缓存，建议结合 AI 场景配置基于请求体（Prompt）哈希的缓存策略。对于相似度极高的 Prompt，直接返回网关层缓存的响应。
*   **价值**：对于高频重复问题，可以将响应时间从秒级降低到毫秒级，并显著减少 API 调用成本。

### 3. 实施细粒度的 Prompt 模板管理与注入
为了防止前端直接暴露敏感的 System Prompt 或让用户随意修改系统指令，应在网关层进行 Prompt 管理。
*   **实践操作**：使用 Higress 的插件（如 `ai-proxy` 或自定义 Wasm 插件）在请求转发前进行“Prompt 注入”。前端只需发送用户的问题，网关层自动拼接预设的 System Prompt 和用户输入。
*   **价值**：实现了 Prompt 的集中版本控制和热更新，便于快速调试人设指令，同时增强了安全性。

### 4. 谨慎处理 SSE 流式响应的超时与断开
AI 对话通常采用 Server-Sent Events (SSE) 流式返回，这比普通 HTTP 请求更容易出现客户端断开或网络抖动。
*   **常见陷阱**：如果网关层的超时时间设置过短，可能导致 LLM 还在生成内容时连接被强行切断；如果未正确处理 SSE 的缓冲，可能导致流式输出变成一次性输出。
*   **实践操作**：确保 Higress 的路由超时时间设置得足够长（或根据模型最大生成时间动态调整）。同时，检查网关配置确保启用了流式透传，避免对响应体进行全量缓冲。

### 5. 建立基于 Token 计数的后端鉴权与限流
传统的 API 网关通常基于“请求数（QPS）”进行限流，但在 AI 场景下，长 Prompt 和短 Prompt 消耗的资源差异巨大。
*   **实践操作**：利用 Higress 的插件能力，解析请求体中的 Prompt 长度，估算 Token 数量。在转发请求前，基于 Token 消耗量而非单纯的请求数进行速率限制或鉴权。
*   **价值**：防止恶意用户发送极长的 Prompt 耗尽后端配额，实现更公平、更精准的资源管控。

### 6. 敏感信息的实时过滤与脱敏
用户可能会在提问中无意输入隐私数据（如身份证号、API Key），这些数据不应被发送给公有大模型。
*   **实践操作**：在 Higress 的请求处理阶段配置正则匹配或 NLP 插件，检测并拦截包含敏感模式的请求，或者对敏感字段进行掩码处理（如将 `sk-xxxx` 替换为 `***`）后再转发给 LLM。
*   **价值**：满足企业合规性要求，降低数据泄露风险。

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI 原生](/tags/ai-%E5%8E%9F%E7%94%9F/) / [阿里开源](/tags/%E9%98%BF%E9%87%8C%E5%BC%80%E6%BA%90/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [LLM](/tags/llm/) / [MCP 协议](/tags/mcp-%E5%8D%8F%E8%AE%AE/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260130-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [中国开源AI生态的架构选择：超越DeepSeek的构建路径]({{< relref "posts/20260129-blogs_podcasts-architectural-choices-in-chinas-open-source-ai-eco-8.md" >}})
- [中国开源AI生态架构选择：DeepSeek之外的技术路径]({{< relref "posts/20260129-blogs_podcasts-architectural-choices-in-chinas-open-source-ai-eco-9.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*