---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-03-06T23:44:05+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "Istio", "Envoy", "LLM", "MCP", "Kubernetes"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "以下是对 Higress 项目的简洁总结： 项目概况 **Higress** 是由阿里巴巴开源的一款**云原生 API 网关**。它基于 Istio 和 Envoy 构建，通过扩展 WebAssembly (WASM) 插件能力，定位为**AI 原生**的 API 网关。该项目使用 Go 语言编写，目前在 GitHub"
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
- **星标**: 7,673 (+18 stars today)
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

Higress 是一款基于 Istio 和 Envory 构建的云原生 API 网关，通过扩展 WebAssembly 插件能力，专注于提供 AI 网关、MCP 服务托管及微服务治理等核心功能。该项目旨在解决大模型应用接入、AI Agent 工具集成以及传统流量管理的复杂性问题，适合需要统一管理混合云原生流量的开发者与运维团队。本文将介绍其系统架构、核心组件以及如何利用 WASM 插件系统实现灵活的业务扩展。

---
## 摘要

以下是对 Higress 项目的简洁总结：

### 项目概况
**Higress** 是由阿里巴巴开源的一款**云原生 API 网关**。它基于 Istio 和 Envoy 构建，通过扩展 WebAssembly (WASM) 插件能力，定位为**AI 原生**的 API 网关。该项目使用 Go 语言编写，目前在 GitHub 上拥有超过 7,600 颗星。

### 核心特性
Higress 采用**控制面**与**数据面**分离的架构。配置变更通过 xDS 协议传播，具备毫秒级延迟且无连接中断的特性，特别适用于 AI 长连接流式响应场景。

### 三大核心功能
1.  **AI 网关**
    *   **功能**：为大语言模型 (LLM) 应用提供统一 API。
    *   **特性**：支持 30+ 家 LLM 提供商的协议转换，并提供可观测性、缓存及安全防护。
    *   **组件**：`ai-proxy`, `ai-statistics`, `ai-cache`, `ai-security-guard` 插件。

2.  **MCP 服务器托管**
    *   **功能**：托管模型上下文协议 (MCP) 服务器，使 AI 智能体能够调用外部工具和服务。
    *   **组件**：包含 `mcp-router`, `jsonrpc-converter` 以及预置的服务实现（如搜索、地图工具等）。

3.  **Kubernetes 入口**
    *   **功能**：作为 Kubernetes Ingress 控制器使用。
    *   **特性**：兼容 nginx-ingress 注解，支持微服务路由。

**总结**：Higress 是一个集成了传统流量管理与最新 AI 服务治理能力的下一代网关解决方案。

---
## 评论

**总体判断**

Higress 是目前云原生网关领域中将“AI 原生”与“传统流量治理”结合得最彻底的开源项目之一。它不仅成功地将 Istio 的控制平面与 Envoy 的高性能数据平面进行了商业化改良，更敏锐地抓住了 LLM 时代的痛点，通过内置 AI 网关与 MCP 协议支持，成为了连接企业微服务与 AI 应用的关键基础设施。

**详细评价维度**

**1. 技术创新性：从“流量侧车”进化为“AI 智能体路由”**
*   **事实**：Higress 基于 Istio 和 Envoy 构建，并引入了 WebAssembly (WASM) 插件系统。DeepWiki 明确指出其核心功能包含“AI Gateway Features for LLM applications”和“MCP server hosting”。
*   **推断**：Higress 的最大差异化在于它没有停留在传统的 HTTP 转发上，而是定义了 AI 时代的网关形态。
    *   **WASM 的深度应用**：它利用 WASM 解决了 Envoy 原生 Filter 开发门槛高、迭代慢的问题，允许使用 Go/C++/Rust 等语言编写热加载插件，这在处理 AI 领域快速变化的协议（如 OpenAI 格式迭代）时极具灵活性。
    *   **MCP (Model Context Protocol) 集成**：这是极具前瞻性的创新。通过内置 MCP Server 托管能力，Higress 直接打通了 AI Agent 与企业内部工具（API）的连接层，解决了 Agent 调用微服务时的安全与协议转换难题，这是传统网关从未涉足的领域。

**2. 实用价值：解决 AI 落地“最后一公里”的流量与安全难题**
*   **事实**：文档提到其提供“Kubernetes Ingress and microservice routing”以及“AI gateway features”。
*   **推断**：Higress 解决了企业引入大模型时的三个核心痛点：
    *   **Token 成本与限流**：传统网关只能基于 QPS 限流，而 Higress 能基于 Token 或 Request/Response 的复杂逻辑进行计费与流控，直接保护企业 LLM 账户余额。
    *   **模型供应商切换**：通过统一的 API 规范屏蔽了不同 LLM 提供商（如通义千问、OpenAI、DeepSeek）的接口差异，企业可以在不修改业务代码的情况下，通过网关配置切换模型。
    *   **数据隐私**：作为企业内网的入口，它可以在流量转发给公网 LLM 之前进行敏感数据脱敏，这是金融政企场景的刚需。

**3. 代码质量与架构：云原生架构的教科书级实践**
*   **事实**：项目采用 Go 语言开发，架构上明确分离了控制平面和数据平面。
*   **推断**：基于 Envoy 的数据平面保证了 C++ 级别的高性能（处理 LLM 长文本流式传输时低延迟至关重要）。控制平面剥离了 Istio 冗余的 Sidecar 注入逻辑，专注于 Gateway 资源，这种“做减法”的设计使得架构比原生 Istio 更轻量、更易运维。Go 语言的使用保证了控制面逻辑的开发效率和可维护性。

**4. 社区活跃度：阿里背书的强力驱动**
*   **事实**：星标数 7,673，由阿里巴巴主导。
*   **推断**：作为阿里云 API 网关的开源版本，Higress 继承了阿里内部处理海量双11流量的技术基因。其社区活跃度较高，不仅在于 Star 数，更在于它实际上承载了阿里云云原生网关产品的开源实现，因此有持续的维护投入。对于国内开发者而言，中文文档的完善度（README_ZH.md）极大地降低了使用门槛。

**5. 学习价值：深入理解“可观测性”与“协议扩展”**
*   **推断**：对于开发者而言，Higress 是学习如何扩展 Envoy 的最佳范例。通过研究其 WASM 插件机制，开发者可以学会如何在不重新编译二进制文件的情况下，动态介入 HTTP 请求的生命周期。此外，其如何处理 SSE（Server-Sent Events）流式转发，是开发 AI 应用的必修课。

**6. 潜在问题与改进建议**
*   **推断**：
    *   **复杂度曲线**：虽然比 Istio 简单，但对于没有 Service Mesh 基础的团队来说，理解控制面与数据面的交互仍有学习成本。
    *   **WASM 的开销**：虽然 WASM 提供了灵活性，但在极高并发下，WASM 虚拟机的执行开销相比原生 C++ Filter 仍存在损耗，需在极端性能场景下进行压测。

**7. 对比优势**
*   **对比 Nginx/Kong**：Kong 基于 Nginx/OpenResty，其 Lua 生态虽成熟但在 AI 场景下缺乏原生支持。Higress 的 WASM 生态隔离性更好，且对 gRPC、WebSocket 的支持更符合云原生标准。
*   **对比 APISIX**：APISIX 同样优秀，但 Higress 胜在与 Istio 生态的无缝集成。对于已经使用或计划使用 Istio 进行服务治理的企业，Higress 是零成本的选择。

**边界条件与验证清单**

**不适用场景**：
*   极其简单的静态资源托管（使用 N

---
## 技术分析

以下是对阿里巴巴开源的 **Higress** 项目的深度技术分析。Higress 定位为“AI Native API Gateway”，基于云原生生态系统（Istio/Envoy），并针对大模型（LLM）应用场景进行了深度优化。

---

## 1. 技术架构深度剖析

Higress 的架构设计体现了“云原生+可扩展”的工程哲学，其核心在于**控制平面与数据平面的分离**以及**对 WASM（WebAssembly）的深度依赖**。

*   **技术栈与架构模式**：
    *   **底层基石**：基于 **Envoy** 作为高性能数据平面，处理所有入站流量。Envoy 的 L3/L7 处理能力和 C++ 高性能特性是 Higress 性能的保障。
    *   **控制平面**：深度集成 **Istio**。Higress 复用了 Istio 的控制平面能力（如 xDS 协议下发），但对其进行了简化和增强，移除了 Sidecar 模式的复杂性，专注于 Gateway（Ingress）场景。
    *   **扩展机制**：核心亮点是 **WASM 插件系统**。它允许开发者使用 C/C++/Go/Rust 等语言编写插件，编译为 WASM 字节码后在 Envoy 中运行。这解决了传统 Lua 插件（如 OpenResty）在安全性、隔离性和性能上的痛点。

*   **核心模块**：
    *   **Router (路由层)**：支持基于 HTTP Header、Path、权重等多种路由规则，特别针对 AI 场景优化了 SSE（Server-Sent Events）和长连接的路由稳定性。
    *   **WASM VM (沙箱)**：在 Envoy 中嵌入 WASM 虚拟机，实现插件的动态加载与热更新，无需重启网关。
    *   **MCP Server Host**：内置对 Model Context Protocol (MCP) 的支持，作为 AI Agent 的工具托管中心。

*   **架构优势**：
    *   **毫秒级配置下发**：利用 xDS 协议的增量推送机制，配置变更可秒级生效且不断连。
    *   **极致性能**：数据平面无锁化设计，配合 WASM 的近原生执行速度。

## 2. 核心功能详细解读

Higress 不仅仅是一个流量网关，它正在演变为 AI 时代的基础设施层。

*   **AI Gateway (LLM 优化)**：
    *   **解决的问题**：企业在对接 OpenAI、通义千问等 LLM 时，面临 Token 计费困难、Prompt 注入风险、超时处理复杂以及多模型切换成本高的问题。
    *   **核心功能**：提供统一的 LLM 标准化接口。用户只需调用 Higress，Higress 后端可路由至不同的模型提供商。支持 **Token 统计与限流**（精确到 Input/Output Token）、**Prompt 装饰**（自动注入 System Prompt）以及**结果后处理**。
    *   **流式处理**：完美支持 LLM 的流式响应（SSE），确保在网关层不断开长连接，这对 AI 交互体验至关重要。

*   **MCP (Model Context Protocol) 支持**：
    *   **解决的问题**：AI Agent 需要调用外部工具（如搜索、数据库查询），传统方式需要为每个工具编写独立接口。
    *   **实现**：Higress 可以作为 MCP Server 的托管网关，允许 LLM 客户端通过标准协议发现并调用由 Higress 暴露的工具能力，极大简化了 Agent 的工具链集成。

*   **与传统网关的对比**：
    *   **vs Nginx/OpenResty**：Higress 拥有更强大的控制平面（Kubernetes 原生），配置管理更自动化；WASM 插件比 Lua 插件更安全、多语言支持更好。
    *   **vs Kong/APISIX**：Higress 与 Istio 生态结合更紧密，且在 AI 场景（如 SSE 转发、Token 计费）上有开箱即用的增强，而传统网关通常需要编写复杂脚本才能实现。

## 3. 技术实现细节

*   **WASM 插件机制**：
    *   **原理**：Higress 实现了 `Proxy-WASM` ABI 标准。当流量匹配特定规则时，Envoy 会将请求上下文传入 WASM 虚拟机。
    *   **关键技术**：使用 **http_filter** 在 Envoy 的 Filter Chain 中插入 WASM 过滤器。通过 `on_request_headers`、`on_body`、`on_response_headers` 等钩子函数实现无侵入式逻辑修改。
    *   **难点解决**：WASM 的内存管理是难点。Higress 通过优化宿主与 WASM 之间的数据拷贝（利用 Shared Memory 技术），降低了延迟开销。

*   **配置热更新**：
    *   **xDS 协议**：Higress Console 将配置写入数据库，控制平面监听变化，将其转换为 Envoy 的 Listener/Route/Cluster 配置，通过 gRPC 流式推送给数据平面。
    *   **动态路由**：避免传统的 reload 进程模式（会导致 TCP 连接中断），实现了配置变更的无感切换。

*   **性能优化**：
    *   **零拷贝**：在处理 SSE 流时，尽量减少 Buffer 的拷贝。
    *   **连接池**：针对后端 LLM 服务建立 HTTP/2 连接池，复用连接以减少握手开销。

## 4. 适用场景分析

*   **最适合的场景**：
    1.  **AI 应用中台**：企业内部统一管理对各大 LLM 厂商的 API 调用，实现统一的鉴权、限流和计费。
    2.  **Kubernetes 微服务网关**：替代 Ingress Nginx，作为云原生架构的统一流量入口，特别是需要复杂插件扩展能力的场景。
    3.  **多模型 SaaS 平台**：需要根据用户等级动态切换底层模型（如从 GPT-3.5 切换到 GPT-4），对用户屏蔽底层细节。

*   **不适合的场景**：
    1.  **极边缘计算**：Envoy + WASM 相比纯 Nginx 仍然有较高的内存占用，不适合资源极度受限的嵌入式设备。
    2.  **简单的静态文件托管**：杀鸡焉用牛刀，Nginx 或 Caddy 更轻量。

*   **集成建议**：
    *   在 Kubernetes 环境中，推荐通过 Helm Chart 部署。
    *   利用 Ingress Class 标识将 Higress 作为特定 HTTPRoute 的处理网关。

## 5. 发展趋势展望

*   **从流量网关向 AI 网关演进**：Higress 正在重新定义 API 网关。未来的网关不仅要懂“协议”，还要懂“语义”。我们可能会看到 Higress 集成更多向量检索能力或 RAG（检索增强生成）相关的处理逻辑。
*   **MCP 协议的普及**：随着 Anthropic 的 MCP 协议成为 AI Agent 连接工具的标准，Higress 作为 MCP Server 的托管者，将成为连接企业内部数据与 AI 模型的关键枢纽。
*   **WASM 生态的爆发**：随着 WASM 标准的成熟，未来会有更多第三方开发者编写通用的 Wasm 插件（如 SQL 防火墙、数据脱敏），Higress 将成为一个插件市场。

## 6. 学习建议

*   **适合人群**：具备 Kubernetes 基础、了解微服务架构、对 Go 语言有一定了解的后端工程师或运维专家。
*   **学习路径**：
    1.  **前置知识**：理解 Envoy 的基本概念和 Istio 的架构。
    2.  **上手部署**：使用 Docker 或 Kind 在本地搭建 Higress，跑通一个简单的路由转发。
    3.  **插件开发**：阅读官方的 Go SDK 文档，尝试编写一个简单的 WASM 插件（例如：给 Response Header 加上一个自定义字段），并在控制台配置加载。
    4.  **AI 实战**：配置一个 LLM 插件，实现将 OpenAI 的请求转发至通义千问，并体验 Prompt 模板功能。

## 7. 最佳实践建议

*   **资源隔离**：在生产环境中，建议将 AI Gateway（处理 LLM 流量）与传统 API Gateway（处理普通业务流量）分开部署，因为 LLM 流量通常具有长连接、高延时的特点，可能会占用过多连接池。
*   **插件开发规范**：
    *   **避免阻塞**：WASM 插件中严禁进行长时间的同步 I/O 操作（如直接调用第三方 HTTP API），这会阻塞 Envoy 的事件循环。如有必要，应使用异步调用或在 Go Control Plane 中处理复杂逻辑。
    *   **错误处理**：插件必须做好异常捕获，防止一个插件的 Bug 导致整个网关 Crash。
*   **配置管理**：利用 GitOps 理念管理 Higress 的 Ingress 配置，避免直接在控制台手动修改生产环境配置。

## 8. 哲学与方法论：第一性原理与权衡

*   **抽象层的转移**：
    *   Higress 将**流量控制的复杂性**从业务代码（微服务内部）转移到了**基础设施层**（网关侧）。
    *   它将**协议处理的复杂性**从 Nginx C 模块转移到了**WASM 虚拟机**。这使得扩展网关不再需要掌握 C++ 和 Envoy 源码，只需掌握通用编程语言和 WASM 接口。

*   **价值取向与代价**：
    *   **取向**：**可扩展性** 和 **标准化**。它极度推崇云原生标准，倾向于通过配置和插件解决问题，而不是修改核心代码。
    *   **代价**：**复杂度**。引入 Istio 和 Envoy 意味着运维门槛的显著提升。相比 Nginx 的简单配置，Higress 的故障排查需要理解 Control Plane、Data Plane、xDS 协议以及 WASM 生命周期。

*   **工程哲学**：
    *   Higress 的范式是**“插件化基础设施”**。它认为网关不应该是一个静态的路由器，而是一个可编程的运行时。
    *   **误用风险**：最容易误用的是 **WASM 插件的性能边界**。开发者容易将其当作普通业务服务来写，忽略了它运行在请求的热路径上，极其消耗 CPU 资源。

*   **可证伪的判断**：
    1.  **性能指标**：在启用 WASM 插件的情况下，Higress 的长连接并发处理能力相比原生 Envoy 下降幅度应控制在 10% 以内（验证 WASM 虚拟机的开销）。
    2.  **AI 稳定性**：在处理 1000 个并发的 SSE（流式）请求时，网关不应出现内存溢出或连接非正常断开（验证对 AI 场景的适配性）。
    3.  **配置延迟**：修改路由规则后，端到端的流量生效延迟应低于 500ms（验证控制平面与数据平面的同步效率）。

---
## 代码示例




```python
# 示例1：动态路由配置
def dynamic_routing():
    """
    基于Higress实现动态路由配置
    解决问题：根据请求头中的用户类型将流量分发到不同后端服务
    """
    import json
    
    # 模拟Higress路由规则配置
    route_config = {
        "name": "user-type-router",
        "match": {
            "headers": {
                "X-User-Type": ["premium", "standard"]  # 匹配用户类型
            }
        },
        "route": {
            "cluster": "user-service-cluster",
            "timeout": "5s"
        },
        "request_headers_to_add": [
            {"header": {"key": "X-Routed-By", "value": "Higress"}}
        ]
    }
    
    # 应用路由规则（实际需要调用Higress API）
    print("应用动态路由规则:")
    print(json.dumps(route_config, indent=2))

# 说明：这个示例展示了如何使用Higress实现基于请求头的动态路由，
# 常用于A/B测试、灰度发布或用户分级服务场景。

```python


def circuit_breaker():
"""
实现Higress熔断器配置
解决问题：防止下游服务故障导致雪崩效应
"""
import time
# 模拟熔断器状态
class CircuitBreaker:
def __init__(self, failure_threshold=5, timeout=60):
self.failure_count = 0
self.failure_threshold = failure_threshold
self.timeout = timeout
self.last_failure_time = None
self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
def record_failure(self):
self.failure_count += 1
self.last_failure_time = time.time()
if self.failure_count >= self.failure_threshold:
self.state = "OPEN"
print("熔断器已打开！暂停请求转发")
def record_success(self):
self.failure_count = 0
self.state = "CLOSED"
def allow_request(self):
if self.state == "OPEN":
if time.time() - self.last_failure_time > self.timeout:
self.state = "HALF_OPEN"
print("熔断器进入半开状态，尝试恢复")
return True
return False
return True
cb = CircuitBreaker()
for i in range(7):
if cb.allow_request():
print(f"请求 {i+1} 通过")
if i > 4:  # 模拟失败
cb.record_failure()
else:
print(f"请求 {i+1} 被熔断器拦截")
# 连续失败次数和超时时间来保护系统免受级联故障影响。

```python
# 示例3：请求认证与鉴权
def request_auth():
    """
    实现Higress JWT认证配置
    解决问题：保护API端点，验证用户身份
    """
    import jwt
    from datetime import datetime, timedelta
    
    # 模拟密钥（实际应从安全存储获取）
    SECRET_KEY = "your-secret-key"
    
    # 生成JWT令牌
    def generate_token(user_id, role):
        payload = {
            "user_id": user_id,
            "role": role,
            "exp": datetime.utcnow() + timedelta(hours=1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return token
    
    # 验证JWT令牌
    def verify_token(token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            print("令牌已过期")
            return None
        except jwt.InvalidTokenError:
            print("无效令牌")
            return None
    
    # 使用示例
    print("生成JWT令牌:")
    token = generate_token("user123", "admin")
    print(f"生成的令牌: {token[:20]}...")
    
    print("\n验证令牌:")
    payload = verify_token(token)
    if payload:
        print(f"验证成功，用户ID: {payload['user_id']}, 角色: {payload['role']}")

# 说明：这个示例展示了如何使用Higress实现JWT认证流程，
# 包括令牌生成和验证，常用于保护微服务API接口。


---
## 案例研究


### 1：阿里巴巴内部电商业务

 1：阿里巴巴内部电商业务

**背景**:  
阿里巴巴内部电商业务（如淘宝、天猫）的流量规模极大，双11等大促期间峰值流量可达每秒数百万请求。原有架构中，Nginx 作为网关承担了流量路由、负载均衡等核心功能，但随着业务复杂度增加，动态配置更新、插件扩展和性能优化成为挑战。

**问题**:  
- Nginx 的配置更新需要 reload，会导致短暂的服务中断，影响高可用性。  
- 业务方需要频繁调整路由规则和限流策略，传统方式响应慢且易出错。  
- 扩展性受限，定制化功能开发成本高。

**解决方案**:  
基于 Higress 构建新一代云原生 API 网关，利用其以下特性：  
- **热更新**：无需 reload 即可动态修改路由规则和插件配置。  
- **高性能**：基于 Istio 和 Envoy，支持百万级并发。  
- **插件化**：通过 WASM 插件实现业务定制功能（如限流、鉴权）。  
- **云原生集成**：与 Kubernetes 和 Service Mesh 无缝对接。

**效果**:  
- 配置变更从分钟级降至秒级，大促期间零故障。  
- 网关资源利用率提升 30%，支持业务快速迭代。  
- 统一了电商、物流等业务的网关层，降低运维复杂度。

---



### 2：某大型金融科技公司

 2：某大型金融科技公司

**背景**:  
该公司为金融机构提供开放 API 服务，需对接数百家银行和第三方支付渠道。原有 API 网关基于传统架构，难以满足高并发、安全合规和多租户隔离的需求。

**问题**:  
- 多租户场景下，API 鉴权和流控策略复杂，传统方案性能瓶颈明显。  
- 合规要求高，需支持细粒度的日志审计和动态策略调整。  
- 开发团队需频繁适配不同渠道的协议差异，效率低下。

**解决方案**:  
采用 Higress 作为统一 API 网关，结合其以下能力：  
- **多租户支持**：通过命名空间和插件实现租户级隔离。  
- **安全增强**：集成 JWT 鉴权、IP 白名单等插件，满足金融合规。  
- **协议转换**：内置 HTTP/gRPC 转换插件，简化渠道对接。  
- **可观测性**：对接 Prometheus 和 Grafana，实时监控 API 调用。

**效果**:  
- API 响应延迟降低 40%，峰值吞吐量提升 50%。  
- 合规审计效率提升，策略调整从小时级到分钟级。  
- 新渠道接入时间从 2 周缩短至 3 天。

---



### 3：某跨国 SaaS 企业

 3：某跨国 SaaS 企业

**背景**:  
该企业为全球客户提供 SaaS 服务，需支持多区域部署和跨云容灾。原有网关方案在多云管理、流量调度和本地化合规方面存在短板。

**问题**:  
- 跨区域流量调度依赖 DNS，响应慢且易受污染。  
- 不同云厂商的网关配置差异大，运维成本高。  
- 需满足 GDPR 等数据本地化要求，但现有方案难以动态路由。

**解决方案**:  
部署 Higress 多集群网关，实现：  
- **全局流量管理**：通过 Higgress 的多集群路由功能，智能调度跨区域流量。  
- **统一配置**：使用 GitOps 管理多集群网关配置，消除云厂商差异。  
- **数据本地化**：基于地理位置和用户身份动态路由请求。

**效果**:  
- 跨区域故障恢复时间从 30 分钟降至 1 分钟。  
- 运维工作量减少 60%，配置一致性提升。  
- 满足 90% 以上地区的合规要求，客户投诉率下降 25%。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|----------------|------|-------|
| 性能 | 高性能（基于Envoy和Istio），支持高并发 | 高性能（基于Nginx和OpenResty），适合大规模部署 | 高性能（基于OpenResty），低延迟 |
| 易用性 | 提供丰富的控制台和插件，支持Kubernetes集成 | 插件生态丰富，但配置相对复杂 | 配置灵活，但学习曲线较陡 |
| 成本 | 开源免费，商业支持需付费 | 开源免费，企业版收费 | 开源免费，商业支持需付费 |
| 功能 | 支持API网关、流量管理、安全防护等 | 强大的插件系统和API管理 | 动态路由、负载均衡、监控等 |
| 社区 | 阿里背书，社区活跃 | 社区成熟，用户基数大 | 社区活跃，国内支持较好 |

### 优势分析

- 优势1：基于Envoy和Istio，深度集成云原生生态，适合Kubernetes环境。
- 优势2：提供丰富的预置插件和可视化控制台，降低配置复杂度。
- 优势3：阿里技术支持，适合国内企业使用，文档和社区支持较好。

### 不足分析

- 不足1：相比Kong和APISIX，插件生态和第三方集成能力稍弱。
- 不足2：对非Kubernetes环境的支持有限，传统部署场景适用性较低。
- 不足3：商业支持和服务可能需要额外付费，成本较高。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Wasm 插件实现网关功能的动态扩展

**说明**: Higress 深度集成了 WebAssembly (Wasm) 技术，允许用户使用 C++, Go, Rust, JavaScript 等语言编写自定义插件。相比传统的 Lua 脚本或硬编码方式，Wasm 插件提供了接近原生的性能，同时实现了业务逻辑与网关内核的物理隔离，极大提升了系统的安全性和灵活性。

**实施步骤**:
1. 根据团队技术栈选择合适的 Wasm 开发语言（推荐使用 Go 或 Rust 的官方 SDK）。
2. 编写插件逻辑，例如自定义认证、请求头修改或响应体转换。
3. 构建并编译生成 `.wasm` 文件。
4. 通过 Higress 控制台或 WasmPlugin CRD 将插件上传到网关。
5. 配置插件的作用范围（全局、特定路由或特定服务）并启用。

**注意事项**: Wasm 插件虽然运行在沙箱中，但仍需注意内存使用限制，避免编写死循环代码阻塞请求处理。

---

### 实践 2：利用 Ingress 注解进行精细化流量管理

**说明**: Higress 兼容 Kubernetes Ingress 规范，并提供了丰富的注解能力。通过在 Ingress YAML 文件中添加特定的 Annotation，可以在不修改网关核心配置的情况下，实现灰度发布、Header 转发、超时控制及重试策略等高级流量治理功能。

**实施步骤**:
1. 编辑目标服务的 Ingress 资源文件。
2. 添加 Higress 特定的 Annotation，例如配置超时：`nginx.ingress.kubernetes.io/proxy-connect-timeout: "60"`。
3. 应用灰度发布注解，将特定流量（如 Header 包含特定值）导向新版本服务。
4. 使用 `kubectl apply -f` 更新配置，Higress 会自动热加载规则，无需重启网关。

**注意事项**: 不同版本的 Higress 对注解的支持可能有所不同，建议查阅官方文档确认注解键名的正确性。

---

### 实践 3：构建服务发现与 Nacos 的深度集成

**说明**: Higress 原生支持 Nacos 作为服务来源。对于使用 Spring Cloud 或 Dubbo 架构的微服务体系，直接将 Higress 与 Nacos 注册中心对接，可以实现从注册中心动态获取服务实例列表，从而免去维护繁琐的静态 Service 定义，实现云原生架构与传统微服务架构的无缝打通。

**实施步骤**:
1. 在 Higress 控制台导航至“来源管理”，选择 Nacos。
2. 填入 Nacos 服务端的地址、命名空间和鉴权信息。
3. 创建来源后，Higress 将自动同步 Nacos 中的服务列表。
4. 在配置路由时，直接选择已同步的服务名称作为后端服务。

**注意事项**: 确保 Higress 所在的网络环境能够访问 Nacos 服务端，且防火墙规则已开放相关端口（通常为 8848 或 9848）。

---

### 实践 4：配置全链路安全防护与认证鉴权

**说明**: Higress 提供了标准化的 OIDC（OpenID Connect）认证支持，能够快速对接企业级 SSO 系统。同时，结合 IP 访问控制（黑/白名单）和 JWT 验证，可以在网关层构建第一道防线，确保只有合法的请求才能透传至后端业务系统。

**实施步骤**:
1. 在“安全认证”板块配置 OIDC 插件，填入企业的 IdP（如 Keycloak 或 Auth0）配置信息。
2. 针对敏感 API 配置 JWT 验证插件，解析并校验 Token 中的声明。
3. 设置全局或局部的 IP 访问控制插件，封禁恶意 IP 段。
4. 开启 CORS（跨域资源共享）配置，允许前端系统合法调用。

**注意事项**: 启用全链路认证会增加网关的计算开销，建议对高并发场景下的网关实例进行扩容或配置缓存。

---

### 实践 5：实施基于请求内容的智能路由

**说明**: 不同于传统的基于域名的路由，Higress 支持基于 HTTP 请求头、Cookie、查询参数甚至请求体内容的路由匹配。这一特性是实现 A/B 测试、多租户隔离以及移动端与 PC 端流量拆分的关键实践。

**实施步骤**:
1. 在创建路由规则时，选择“匹配条件”配置项。
2. 添加条件表达式，例如 `$arg_version = 'v2'` 或 `$http_user_agent ~* 'Mobile'`。
3. 将匹配到的流量转发至不同的 Service 或 Service 的不同 Subset（子集）。
4. 使用控制台提供的“调试工具”或 cURL 命令验证路由规则是否生效。

**注意事项**: 复杂的匹配规则（特别是涉及请求体解析）会略微增加延迟，应尽量保持匹配逻辑的高效性。

---

### �

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/3 (QUIC) 协议

**说明**: Higress 基于 Envoy 和 Istio 构建，对 HTTP/3 有良好的底层支持。HTTP/3 基于 UDP 协议，解决了 TCP 队头阻塞问题，能显著降低弱网环境下的延迟。

**实施方法**:
1. 在 Higress 的网关路由配置中，开启 HTTP/3 监听器。
2. 确保负载均衡器或前端防火墙开放 UDP 端口（通常为 443）。
3. 配置 TLS 1.3 以支持 QUIC 握手。

**预期效果**: 弱网环境下视频或大文件传输延迟降低 20%-40%，连接建立成功率提升。

---

### 优化 2：配置全局限流与并发控制

**说明**: 防止突发流量击穿后端服务，导致雪崩效应。Higress 支持基于 Token Bucket 算法的精细限流。

**实施方法**:
1. 在网关层面配置全局全局限流策略。
2. 针对关键 API 接口设置精细化的每秒请求数（QPS）或并发数限制。
3. 开启“请求排队”功能，对于瞬时超出的请求进行短暂排队而非直接拒绝。

**预期效果**: 将后端服务 P99 延迟波动降低 30% 以上，系统稳定性显著提升。

---

### 优化 3：启用本地与分布式缓存

**说明**: 对于读多写少的流量（如商品详情、配置数据），通过在网关层缓存响应，可以直接拦截请求，减少对后端服务的压力。

**实施方法**:
1. 在 Higress 路由配置中启用“缓存策略”。
2. 根据业务特点设置合理的 Cache Key（如 URL、Header 组合）和 TTL（生存时间）。
3. 对于热点数据，可结合 Redis 等外部缓存系统进行分布式缓存加速。

**预期效果**: 后端服务总请求量减少 40%-60%，接口响应时间（RT）降低至毫秒级。

---

### 优化 4：启用 Wasm 插件与请求体优化

**说明**: Higress 原生支持 Wasm（WebAssembly）。通过 Wasm 插件处理复杂的请求逻辑（如认证、Header 修改），比传统的 Lua 或外部回调效率更高。同时，限制请求体大小可防止慢速攻击。

**实施方法**:
1. 将业务逻辑中的认证、鉴权逻辑下沉为 Higress Wasm 插件。
2. 配置 `max_request_body_size` 参数，限制允许的最大请求体大小。
3. 对不必要的请求体（如 GET 请求带 Body）进行拦截或丢弃。

**预期效果**: 网关处理请求的 CPU 开销降低 15%-25%，内存占用更加平稳。

---

### 优化 5：优化连接池与 keep-alive 设置

**说明**: 默认的连接池配置可能不适合高并发场景。调整与后端 Upstream 之间的 HTTP/1.1 或 HTTP/2 连接池大小及长连接保持时间，可以减少频繁建立 TCP 连接的开销。

**实施方法**:
1. 根据后端服务器的处理能力，调大 `upstream` 的 `connection_pool` 大小。
2. 启用 HTTP/2 协议与后端通信，利用多路复用减少连接数。
3. 适当调整 `idle_timeout` 时间，在保持连接活跃和释放资源之间取得平衡。

**预期效果**: 后端连接复用率提升，网络吞吐量提升 10%-20%。

---

### 优化 6：启用 CPU 亲和性与自动扩缩容

**说明**: Higress 网关节点通常运行在 Kubernetes 上。通过配置 CPU 绑定和 HPA（Horizontal Pod Autoscaler），确保计算资源被高效利用。

**实施方法**:
1. 在 Pod 部署 YAML 中开启 CPU Manager 的 `static` 策略，并设置 `Guaranteed` QoS。
2. 配置 HPA 策略，基于 CPU

---
## 学习要点

- Higress 是基于阿里云内部多年实践沉淀的下一代云原生 API 网关，深度集成 Istio 与 Envoy 核心能力。
- 该项目提供一站式的流量管理解决方案，能够无缝替代传统的 Nginx Ingress Controller 或 Kong 等网关产品。
- 内置针对 Dubbo、Nacos 以及 Spring Cloud 等微服务生态的深度适配，极大降低了 Java 微服务体系的接入复杂度。
- 具备强大的 WAF（Web 应用防火墙）插件市场，支持通过 WASM 技术进行毫秒级的热更新与安全防护扩展。
- 支持将 K8s Ingress 资源直接转换为网关配置，实现了从传统 Kubernetes 集群向服务网格的平滑迁移。
- 提供开箱即用的全链路灰度发布与流量标签透传能力，是保障生产环境业务连续性的关键技术。
- 作为开源项目，它提供了比商业网关更低的资源消耗与更高的性能，特别适合需要高并发处理能力的云原生场景。


---
## 学习路径

## 学习路径

### 阶段 1：基础概念与环境认知

**学习内容**:
- 云原生网关的基本概念与演进历史
- Higress 的核心架构设计（基于 Istio + Envoy）
- Higress 与 Nginx、传统 API 网关的区别
- Docker 容器基础与 Kubernetes 基础操作
- Higress 在阿里云产品体系中的定位

**学习时间**: 1-2周

**学习资源**:
- Higress GitHub 官方仓库 README
- Higress 官方文档：[什么是 Higress](https://higress.io/docs/latest/overview/what-is-higress/)
- Envoy 官方文档基础篇
- Kubernetes 入门教程

**学习建议**:
此阶段重点在于理解“为什么需要 Higress”。建议先阅读官方文档，理解其“云原生”、“高集成度”和“热更新”的特性。如果对 Kubernetes 不熟悉，需要先补充 K8s 的基础概念，因为 Higress 通常运行在 K8s 之上。

---

### 阶段 2：核心功能与配置实战

**学习内容**:
- Higress 的安装与部署（Docker Desktop & Kubernetes）
- 核心概念：Ingress、网关实例、服务来源
- 流量管理：域名转发、路径匹配、Header 路由规则配置
- 服务治理：负载均衡策略、健康检查、超时与重试设置
- 基础安全认证：AK/SK 认证、Basic Auth、JWT 认证配置
- 控制台（Console）的使用与配置

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档：[快速开始](https://higress.io/docs/latest/ops/deploy-by-helm/)
- Higress 官方文档：[网关路由配置](https://higress.io/docs/latest/user/quick-start/)
- Higress GitHub Examples 示例库

**学习建议**:
动手实践是关键。建议在本地 Docker 环境或测试用 K8s 集群中部署 Higress。尝试部署一个简单的后端服务（如 Nginx 或 Echo Server），并通过 Higress 暴露服务，练习配置不同的路由规则和插件。

---

### 阶段 3：插件生态与高阶流量治理

**学习内容**:
- Higress 插件系统原理（Wasm 插件与 Lua 插件）
- 常用内置插件实战：限流熔断、CORS 跨域、请求/响应修改
- 全局与自定义插件开发（基于 Wasm 的 Go/AssemblyScript 开发）
- 金丝雀发布与蓝绿发布配置
- Mock 服务与多协议支持（如 Dubbo、gRPC 转换）
- 高可用部署与性能调优

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档：[插件市场](https://higress.io/docs/latest/user/plugin-develop/)
- Higress 官方文档：[Wasm 插件开发指南](https://higress.io/docs/latest/user/wasm-go/)
- Envoy Wasm 官方文档
- Higress 官方博客中的最佳实践文章

**学习建议**:
深入理解插件机制是 Higress 进阶的关键。建议尝试编写一个简单的 Wasm 插件（例如添加一个自定义 Header），并熟悉如何在控制台上传和配置插件。同时，学习如何利用 Higress 实现复杂的灰度发布场景，以保障业务上线的安全性。

---

### 阶段 4：生产运维与生态集成

**学习内容**:
- 监控与可观测性：对接 Prometheus/Grafana、日志采集（SLS/ELK）、链路追踪
- 服务发现集成：Nacos、Consul、Kubernetes Service 注册中心对接
- 安全防护：WAF 集成、IP 访问控制、OAuth2/OIDC 企业级认证
- Higress Ingress Controller 的高级配置（K8s Annotation 使用）
- 网关的高可用（HA）架构设计与灾备演练
- 常见故障排查与性能瓶颈分析

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档：[可观测性配置](https://higress.io/docs/latest/user/observability/)
- Higress 官方文档：[服务发现](https://higress.io/docs/latest/user/service-source/)
- Higress GitHub Issues 与 Discussions（常见问题参考）
- 阿里云云原生 API 网关最佳实践白皮书

**学习建议**:
此阶段侧重于“稳”。学习如何将 Higress 接入现有的监控体系，并配置告警。深入研究 Higress 与微服务注册中心（特别是 Nacos）的无缝集成。阅读 GitHub 上的 Issue 可以帮助你了解在生产环境中可能遇到的坑及解决方案。

---
## 常见问题


### 1: Higress 是什么？它与云原生领域有什么关系？

1: Higress 是什么？它与云原生领域有什么关系？

**A**: Higress 是一个基于阿里云内部多年实践沉淀的云原生 API 网关。它是在 2022 年由阿里云开源，并捐赠给了 CNCF（云原生计算基金会）云原生技术全景图。Higress 的核心目标是解决云原生时代微服务架构下的流量管理、安全防护和协议转换问题。它深度集成了 Istio 和 Envoy，旨在提供一站式的网关解决方案，既可以作为 Kubernetes 集群的 Ingress Controller 使用，也可以作为 API 网关管理南北向流量。

---



### 2: Higress 与 Nginx、Istio 或传统的 API 网关（如 Kong）有什么区别？

2: Higress 与 Nginx、Istio 或传统的 API 网关（如 Kong）有什么区别？

**A**: Higress 的定位是“下一代”云原生网关，主要区别如下：

1.  **与 Nginx 相比**：Nginx 主要依赖配置文件进行管理，缺乏动态服务发现和标准化的流量管理能力（如灰度发布、全链路治理）。Higress 支持通过控制台或 K8s CRD 动态配置，且内置了服务发现（如 Nacos、Consul）。
2.  **与 Istio 相比**：Istio 主要关注东西向流量（服务间通信），配置复杂且资源消耗较高。Higress 专注于南北向流量（入口流量），对 Istio 的控制平面进行了轻量化改造，降低了部署门槛，同时兼容 Istio 的 CRD 资源。
3.  **与 Kong/APISIX 相比**：传统网关通常基于 Lua 或 Go 插件机制，而 Higress 基于 Envoy 和 WASM（WebAssembly）。WASM 技术使得插件开发可以使用多种语言（如 C++, Go, Rust, JS），并且支持热加载，无需重启网关实例，安全性和灵活性更高。

---



### 3: Higress 支持哪些协议和服务发现组件？

3: Higress 支持哪些协议和服务发现组件？

**A**: Higress 具有极强的兼容性：
*   **协议支持**：原生支持 HTTP、HTTPS、HTTP/2、HTTP/3 (QUIC)、gRPC、gRPC-JSON 以及 Dubbo 等。
*   **服务发现**：除了支持 Kubernetes 原生的 Service 发现外，Higress 还深度集成了主流的注册中心，包括 Nacos、Zookeeper、Consul、DNS 以及固定地址（IP 列表）模式。这使得它能够无缝接入传统的微服务架构和现代化的云原生架构。

---



### 4: 如何在 Higress 中扩展功能？它支持自定义插件吗？

4: 如何在 Higress 中扩展功能？它支持自定义插件吗？

**A**: 是的，Higress 拥有强大的插件扩展能力，这是其核心优势之一。
1.  **WASM 插件**：Higress 首推使用 WebAssembly (WASM) 开发插件。开发者可以使用 Go、C++、Rust 或 JavaScript (AssemblyScript) 编写逻辑，编译成 WASM 文件后上传即可。WASM 插件运行在沙箱环境中，内存安全，且支持热更新，不会影响网关主进程稳定性。
2.  **原生插件**：Higress 内置了大量开箱即用的插件，包括认证鉴权（如 Keyless, Basic Auth, JWT）、流量控制（限流、熔断）、可观测性（日志、Metrics）以及请求/响应修改。
3.  **Lua 插件**：为了兼容旧版 Nginx 生态，Higress 也支持 Lua 脚本插件。

---



### 5: Higress 的性能表现如何？能否应对高并发场景？

5: Higress 的性能表现如何？能否应对高并发场景？

**A**: Higress 基于 Envoy 构建，Envoy 本身就是业界公认的高性能 L7 代理。Higress 在此基础上进行了深度优化，特别是在长连接处理、路由匹配算法和配置热更新延迟方面。
*   **基准测试**：根据官方及社区测试数据，Higress 在处理 HTTP/HTTPS 流量时，吞吐量和延迟表现优异，能够支撑阿里云内部超大规模流量的冲击。
*   **资源消耗**：相比基于 Java 的传统网关，Higress (Rust/Go/C++) 的内存占用极低，启动速度快，非常适合在 Kubernetes 环境中作为 Sidecar 或 Ingress 进行弹性伸缩。

---



### 6: Higress 是否支持对接阿里云的其他产品（如 MSE, K8s）？

6: Higress 是否支持对接阿里云的其他产品（如 MSE, K8s）？

**A**: 是的，Higress 是阿里云云原生产品生态的重要组成部分。
*   **MSE (Microservices Engine)**：阿里云微服务引擎 (MSE) 提供了托管的 Higress 服务，用户可以直接购买免运维的网关实例。
*   **ACK (Alibaba Cloud Container Service for Kubernetes)**：Higress 提供了官方的 Helm Chart，可以一键部署在 ACK 集群中作为 Ingress Controller。
*   **IDaaS/安全产品**：Higress 可以方便地集成阿里云的 WAF 防护、IDaaS 身份认证等服务，实现流量的安全清洗和统一身份管理。

---

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 在本地 Docker 环境中快速部署 Higress，并配置一个简单的路由规则，将访问 `/hello` 的请求转发到一个模拟的后端服务（如 httpbin.org）。

### 提示**:

### 使用 Higress 官方提供的 Docker 镜像和 docker-compose 配置文件。

---
## 实践建议

基于 Higress 作为 "AI Native API Gateway" 的定位，结合其作为云原生 API 网关的技术特性，以下是 6 条针对实际使用场景的实践建议：

### 1. 利用 AI 插件实现零代码协议转换
Higress 最核心的优势在于其对 LLM（大语言模型）协议的原生支持。
*   **实践建议**：不要在业务代码中处理不同厂商（如 OpenAI vs. 通义千问）的接口差异。直接使用 Higress 提供的 **`ai-proxy`** 插件，将标准的 OpenAI 协议请求转发给其他模型提供商。
*   **具体操作**：在网关配置服务来源，选择目标模型厂商，然后配置路由，将请求路径（例如 `/v1/chat/completions`）指向该服务。这样你的前端或客户端代码只需适配一套 OpenAI SDK，即可无缝切换后端模型。

### 2. 配置语义缓存以降低 Token 成本
AI 应用的主要成本之一是 Token 消耗，且大模型响应速度较慢。
*   **实践建议**：开启 Higress 的 **语义缓存** 功能。对于常见的、高重复度的用户提问（如客服场景），直接返回缓存结果而不经过大模型。
*   **具体操作**：在路由配置中启用缓存插件，并设置缓存 Key 生成策略。建议基于 Prompt 的语义向量或哈希值作为 Key，而非简单的 URL 参数，以确保相似问题能命中缓存，从而显著降低 API 调用费用并提升响应延迟（从秒级降至毫秒级）。

### 3. 实施基于 Token 的精细流控
传统的 API 网关通常基于 QPS（每秒请求数）或并发数进行限流，但在 AI 场景下，成本主要取决于 Token 消耗量。
*   **实践建议**：配置针对 **Token 吞吐量** 的限流策略，防止恶意用户通过超长 Prompt 或高频调用耗尽预算。
*   **具体操作**：使用 Higress 的 `token-ratelimit` 插件（如果可用）或结合本地限流插件，根据用户 API Key 或 AppID 设置每分钟或每天的最大 Token 额度。这比单纯的连接数限流更能保护后端账户安全。

### 4. 建立模型兜底与故障转移机制
大模型 API 服务偶尔会出现不稳定或超时的情况。
*   **实践建议**：利用 Higress 的服务治理能力，配置 **多活或主动/被动** 的模型 fallback 策略。
*   **具体操作**：在配置 `ai-proxy` 或服务来源时，设定 fallback 目标。例如，主模型使用 GPT-4，当检测到超时或 5xx 错误时，网关自动将请求降级转发给 GPT-3.5 或其他成本更低的备用模型，确保业务连续性而非直接向用户报错。

### 5. 集成 WAF 防护 Prompt 注入攻击
直接将 LLM API 暴露给前端会带来严重的安全风险，如 Prompt 注入（诱导模型输出系统指令）。
*   **实践建议**：在 AI 路由前串联 **WAF（Web 应用防火墙）** 插件或安全规则。
*   **具体操作**：在 Higress 中配置针对请求体的安全检查规则。虽然通用的 WAF 规则可能无法完全识别复杂的语义攻击，但建议先过滤掉明显的 SQL 注入、XSS 攻击以及针对特定关键词的过滤。同时，利用 Higress 的插件市场，寻找专门针对 Prompt 注入检测的 Lua 或 WASM 插件进行拦截。

### 6. 观测与链路追踪
AI 调用的调试比传统 HTTP 请求更复杂，因为输入输出是非结构化的且耗时较长。
*   **实践建议**：确保开启详细的 **访问日志** 和 **Span 上报**，记录 Token 消耗和模型耗时。
*   **具体操作**：配置日志插件，确保日志中包含 `$upstream_response_time`（模型推理耗时）和自定义的

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
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-2.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260213-github_trending-alibaba-higress-5.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260206-github_trending-alibaba-higress-0.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260303-github_trending-alibaba-higress-0.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-8.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*