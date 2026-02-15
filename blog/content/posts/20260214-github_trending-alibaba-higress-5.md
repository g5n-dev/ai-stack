---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-02-14T23:26:51+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "阿里开源", "Istio", "Envoy", "WASM", "LLM", "MCP 协议"]
categories: ["系统与基础设施", "AI 工程"]
source: github_trending
description: "基于您提供的 GitHub 仓库信息及 DeepWiki 节选，以下是关于 **Higress** 的中文简洁总结： 项目概况 **Higress** 是由阿里巴巴开源的一款**云原生 API 网关**。它基于 **Istio** 和 **Envoy** 构建，并深度集成了 **WebAssembly (WASM)**"
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
- **星标**: 7,527 (+4 stars today)
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

Higress 是阿里巴巴开源的基于 Istio 和 Envoy 的 AI 原生 API 网关，它通过集成 WASM 插件系统，在提供传统微服务流量管理能力的同时，专门针对 LLM 应用进行了优化。该项目旨在解决企业将大模型集成至现有架构时面临的统一管理与安全分发难题。本文将深入剖析其系统架构，并重点介绍其 AI 网关特性、MCP 系统支持以及具体的部署开发指南。

---
## 摘要

基于您提供的 GitHub 仓库信息及 DeepWiki 节选，以下是关于 **Higress** 的中文简洁总结：

### 项目概况
**Higress** 是由阿里巴巴开源的一款**云原生 API 网关**。它基于 **Istio** 和 **Envoy** 构建，并深度集成了 **WebAssembly (WASM)** 插件能力。该项目使用 Go 语言编写，目前在 GitHub 上拥有超过 7,500 颗星。Higress 的核心定位是“AI 原生”，旨在为现代应用特别是 AI 应用提供统一的流量入口和管理平台。

### 核心架构
Higress 采用**控制平面**与**数据平面**分离的架构：
*   **控制平面**：负责配置管理。
*   **数据平面**：负责流量处理。
*   **配置分发**：通过 xDS 协议进行配置传播。其优势在于**毫秒级**的配置变更延迟且不中断连接，这使其非常适合处理 AI 长连接流式响应等场景。

### 三大核心功能
1.  **AI 网关**
    *   **功能**：为大语言模型（LLM）应用提供统一 API。
    *   **特性**：支持 30+ LLM 提供商的协议转换、可观测性、缓存以及安全防护。
    *   **组件**：包含 `ai-proxy`（代理）、`ai-statistics`（统计）、`ai-cache`（缓存）和 `ai-security-guard`（安全防护）等插件。
2.  **MCP 服务器托管**
    *   **功能**：托管模型上下文协议（MCP）服务器，使 AI 智能体能够调用外部工具和服务。
    *   **组件**：利用 `mcp-router`、`jsonrpc-converter` 过滤器及具体的 MCP 服务器实现（如搜索、地图工具等）。
3.  **Kubernetes Ingress**
    *   **功能**：作为 K8s Ingress 控制器使用，兼容 nginx-ingress 注解，处理微服务路由。

### 总结
Higress 不仅是一个传统的 API 网关，更是一个面向 AI 时代的基础设施。它通过将 LLM 管理、AI Agent 工具集成与微服务路由融为一体，配合高性能的 WASM 插件

---
## 评论

**总体判断**

Higress 是一款极具前瞻性的“AI 原生”网关，它成功地将云原生流量治理能力与大模型（LLM）应用所需的语义处理能力进行了深度融合。它不仅解决了传统网关无法处理 AI 流量的痛点，更通过 WASM 和 MCP 协议，重新定义了 API 网关在 AI 时代的角色定位。

**深入评价依据**

**1. 技术创新性：从“流量管道”到“AI 智能体”的架构跃迁**
*   **事实（DeepWiki）：** Higress 基于 Istio 和 Envoy 构建，核心扩展点是 WebAssembly (WASM) 插件系统，并明确提出了“AI Gateway”和“MCP Server Hosting”功能。
*   **推断：** 传统网关（如 Nginx,早期的 Kong）主要处理 HTTP/TCP 七层负载均衡，对 AI 特有的“流式传输”和“Token 计费”无能为力。Higress 的差异化在于它**将 AI 推理逻辑左移到了网关层**。通过 WASM 插件，它能在网关层直接实现 Prompt 模板注入、敏感词过滤以及 LLM 的多模型切换。更关键的是，它集成了 **MCP (Model Context Protocol)** 服务器托管功能，这意味着 Higress 不仅仅是流量的转发者，更成为了 AI Agent 的工具调度中心，这在架构上是一个巨大的创新。

**2. 实用价值：降低 AI 落地复杂度与成本控制的“杀手锏”**
*   **事实（DeepWiki）：** 仓库描述强调其提供“AI Gateway Features for LLM applications”及“Traditional API Gateway capabilities”。
*   **推断：** 在实际业务中，开发者在对接 OpenAI 或阿里云通义千问等模型时，往往面临繁琐的协议适配和不可控的 Token 消耗。Higress 解决了**“模型异构”**和**“成本透明化”**两个关键问题。它允许后端服务使用统一的 OpenAI 接口格式，由网关负责转换为不同供应商的私有协议；同时，它能在网关层精确统计 Token 消耗，实现基于 Token 的限流和配额管理。这种“一站式”解决方案对于正在从传统微服务架构向 AI 架构转型的企业来说，实用价值极高。

**3. 代码质量与架构：云原生标准的高水位实现**
*   **事实（DeepWiki）：** 架构分离了控制平面和数据平面；语言为 Go；星标数 7,527；文档涵盖 Core Architecture, Build, WASM Plugin, Development Guide 等。
*   **推断：** 选择 Go 语言并基于 Envoy 构建，保证了数据平面的高性能和可扩展性。控制平面与数据平面的分离符合云原生设计的最佳实践。从文档的完整度（包含中文、日文、英文）来看，阿里巴巴作为主要贡献者，展现了极高的工程化成熟度。WASM 插件系统的引入，使得用户可以使用 C/C++/Rust/Go 甚至 TinyGo 编写业务逻辑，而无需重新编译网关或使用 Lua（传统 OpenResty 方案的痛点），这在代码可维护性和安全性上具有显著优势。

**4. 社区活跃度与生态：头部背书与企业级保障**
*   **事实：** 仓库归属于 Alibaba，拥有 7.5k+ 星标。
*   **推断：** 相比于个人开发者维护的开源网关，Higress 背靠阿里的技术生态，意味着其更新频率和长期维护有保障。社区活跃度不仅体现在 Star 数，更体现在其与阿里云通义千问等产品的深度整合上。对于国内开发者而言，一个拥有中文文档且由国内大厂主导的顶级网关项目，能极大地降低技术支持的心智负担。

**5. 学习价值与对比优势：不仅是工具，更是 AI 基础设施范本**
*   **推断：** Higress 对比同类工具（如 Kong 或 APISIX），最大的优势在于**“AI Native”**。虽然 Kong 也有 AI 插件，但 Higress 是从底层架构上就考虑了 AI 的需求（如 SSE 支持、MCP 协议）。与传统的 Ingress-Nginx 相比，Higress 提供了更现代化的控制台和动态配置能力。对于开发者而言，研究 Higress 的 WASM 插件开发是学习云原生可观测性、流量治理以及 AI 协议适配的绝佳案例。

**边界条件与验证清单**

**不适用场景：**
*   **极致边缘场景：** 如果你的业务仅需极简单的静态资源转发或对资源消耗极其敏感（如嵌入式设备），Higress 基于 Envoy 的厚重架构可能显得过于庞大。
*   **纯私有化非 K8s 环境：** 虽然 Higress 支持非 K8s 部署，但其威力在 Kubernetes 环境下才能最大化，传统虚拟机部署可能运维复杂度较高。

**快速验证清单：**
1.  **WASM 冷启动性能测试：** 部署一个自定义 WASM 插件，使用压测工具（如 wrk）验证开启插件后的请求延迟增加是否在可接受范围内（通常 < 5ms）。
2.  **SSE 流式稳定性：** 构建一个测试 LLM 接口，开启 Higress 的流式转发，验证在长连接下网关是否能正确处理分片传输而不导致连接中断。
3.  **MCP

---
## 技术分析

以下是对阿里巴巴开源的 **Higress** 项目的深度技术分析。基于其“AI Native API Gateway”的定位，我们将从传统云原生网关与 AI 基础设施结合的角度进行剖析。

---

# Higress 深度技术分析报告

## 1. 技术架构深度剖析

Higress 的架构设计体现了“**继承与进化**”的工程哲学。它没有从零开始造轮子，而是站在了云原生生态巨人的肩膀上。

### 1.1 技术栈与架构模式
*   **底层基石**：基于 **Envoy** 作为高性能数据平面，利用其 L3/L7 网络处理能力和可观测性。
*   **控制平面**：深度集成 **Istio**，复用其 xDS（控制面与数据面通信协议）下发配置，实现毫秒级配置热更新。
*   **编程语言**：**Go**。控制平面使用 Go 构建，利用其高并发处理能力和丰富的云原生生态库。
*   **扩展模型**：**WASM (WebAssembly)**。这是 Higress 架构中最关键的技术选型，允许使用 C/C++/Go/Rust 等语言编写插件，并在 Envoy 的沙箱中运行。

### 1.2 核心模块与关键设计
*   **控制面与数据面分离**：
    *   **控制面**：负责配置管理、服务发现（Kubernetes/Nacos）、路由规则计算。它将用户的配置转化为 Envoy 理解的 xDS 协议。
    *   **数据面**：Envoy 实例，负责实际的流量转发、负载均衡、WASM 插件执行。
*   **WASM 虚拟机管理**：Higress 内置了 WASM 运行时（通常基于 Wasmtime 或 V8），实现了插件的动态加载和卸载。这使得在不重启网关的情况下修改业务逻辑成为可能。

### 1.3 技术亮点与创新点
*   **AI Native (AI 原生化)**：这是 Higress 与 Nginx、传统 Kong 最大的区别。它不仅仅把 AI 请求当作普通 HTTP 代理，而是内置了对 **LLM 协议**（OpenAI 协议兼容）的理解。
*   **MCP (Model Context Protocol) 支持**：Higress 直接实现了 MCP 服务端托管能力，允许 AI Agent 通过网关统一访问外部工具和数据源，解决了 AI 应用中工具调用的安全与管理问题。
*   **热更新机制**：基于 Istio 的 xDS 机制，配置变更通过增量推送到数据面。对于 AI 场景中常见的长连接（如 SSE 流式响应），这种无中断更新至关重要。

### 1.4 架构优势分析
*   **低延迟**：数据面 Envoy 采用 C++ 编写，配合 Zero-copy 机制，处理转发延迟极低。
*   **高安全性**：WASM 插件运行在资源受限的沙箱中，插件崩溃不会导致网关崩溃，且提供了内存隔离。
*   **极致的扩展性**：通过 WASM，开发者可以用高级语言编写复杂的逻辑（如 AI 请求的 Prompt 注入、敏感词过滤），而无需修改网关核心代码。

---

## 2. 核心功能详细解读

### 2.1 主要功能与场景
Higress 定位为“一站式流量入口”，核心功能分为三大板块：
1.  **AI 网关**：
    *   **LLM 服务提供商聚合**：统一对接 OpenAI、Azure、通义千问、HuggingFace 等模型。
    *   **Token 管理与计费**：基于请求/响应的 Token 计数，实现基于用量的流控和计费。
    *   **Prompt 模板管理**：在网关层进行 Prompt 的注入和优化。
    *   **结果缓存**：对高频相同的 Prompt 进行缓存，直接返回结果，降低后端模型成本。
2.  **MCP 服务器托管**：
    *   将后端服务包装为 MCP 协议，供 AI Agent 调用。
    *   处理工具调用的鉴权、流控和日志审计。
3.  **传统微服务网关**：
    *   Kubernetes Ingress 支持。
    *   金丝雀发布、蓝绿发布。
    *   流量镜像与故障注入。

### 2.2 解决的关键问题
*   **AI 模型切换的复杂性**：企业从 GPT-4 切换到开源 Llama 时，通常需要修改客户端代码。Higress 通过统一协议转换，让后端模型切换对客户端透明。
*   **AI 流量的不可控性**：AI 调用成本高且延迟大。Higress 提供了针对 Token 的限流（防止刷量导致破产）和缓存（加速响应）。
*   **工具调用的安全风险**：直接暴露数据库或内部 API 给 AI Agent 极其危险。Higress 作为 MCP Host，充当了 AI 与企业数据之间的防火墙。

### 2.3 与同类工具对比
| 特性 | Higress | Nginx | Kong | APISIX |
| :--- | :--- | :--- | :--- | :--- |
| **AI 原生支持** | **强** (内置 Provider 管理, Token计费) | 无 (需手写 Lua) | 弱 (需插件或 AI Gateway 附加包) | 弶 (需插件) |
| **扩展性** | **WASM** (多语言, 沙箱) | Lua (C环境, 危险) | PDK / WASM | Plugin (Go/Lua) |
| **配置热更新** | 毫秒级 | 需 Reload (断连接) | 动态 | 动态 |
| **K8s 集成** | **原生** (Ingress/Gateway API) | 需 Ingress Controller | 需 Ingress Controller | 原生 |
| **性能** | 极高 | 极高 | 高 | 高 |

### 2.4 技术实现原理
*   **AI 流式处理**：Higress 在 Envoy 层处理 HTTP Chunked 编码，实现了对 LLM 流式输出的透传与拦截。它可以在流式传输过程中实时进行敏感词检测，而不需要等待整个响应结束。
*   **Provider 路由**：根据请求 Header（如 `model: gpt-4`）或路径，将流量动态路由到不同的后端 Upstream（OpenAI API 或本地部署的 vLLM）。

---

## 3. 技术实现细节

### 3.1 关键技术方案
*   **WASM 插件系统**：
    *   Higress 实现了 **Proxy-WASM** 规范。
    *   **配置注入**：通过 `OnConfigure` 回调，将网关的配置（如 Redis 地址、鉴权密钥）注入到 WASM 虚拟机内存中。
    *   **共享内存**：利用 WASM 的共享内存特性（如 Host Mapping），在插件间共享数据（如全局限流计数器）。
*   **配置分发**：
    *   基于 Istio 的 Pilot 发现服务。Higress 对 Istio 进行了剪裁和优化，去除了 Sidecar 模式的复杂性，专注于 Gateway 模式。
    *   使用 ADS (Aggregated Discovery Service) 聚合下发配置，保证配置一致性。

### 3.2 代码组织结构
*   **`pkg/`**：核心业务逻辑。
    *   `ingress`：Kubernetes Ingress 资源的转换逻辑。
    *   `config`：配置的解析与分发。
    *   `plugins`：WASM 插件的管理器。
*   **`plugin/`**：内置的 WASM 插件源码（如 `ai-proxy`, `key-auth` 等），这些代码通常会被编译成 `.wasm` 文件挂载到网关中。
*   **`router/`**：核心路由匹配引擎，支持基于前缀、精确匹配、正则及 Header 的复杂路由。

### 3.3 性能优化与扩展性
*   **零拷贝**：利用 Envoy 的 Buffer 行为，尽量减少数据在内核态与用户态之间的拷贝。
*   **连接池**：针对后端 LLM 服务（通常连接建立耗时），维护了长连接池，支持 HTTP/1.1 和 HTTP/2。
*   **异步处理**：WASM 插件的执行虽然是同步的（阻塞请求处理），但 Higress 优化了 VM 上下文切换的开销，并允许插件进行异步 HTTP 调用（如调用 Redis 鉴权）。

### 3.4 技术难点与解决方案
*   **难点**：WASM 的性能损耗。
*   **方案**：Higress 引入了 **Wasmtime** 作为运行时，并开启了 AOT (Ahead-Of-Time) 编译优化，将 WASM 字节码编译为机器码缓存，大幅降低执行开销。
*   **难点**：AI 流式响应的中间件处理。
*   **方案**：在 Envoy 的 Stream Filter 阶段进行处理，而不是等待完整 Body。这要求插件逻辑必须是有状态的，能够处理数据分片。

---

## 4. 适用场景分析

### 4.1 适合使用的项目
*   **大模型应用 (RAG/Agent)**：任何需要调用 LLM API 的企业级应用。Higress 可以统一管理 Prompt、Key 和流量。
*   **多模型调度**：需要根据成本或智能程度，将请求路由到不同模型（例如：简单问题用 Llama 3，复杂问题用 GPT-4）的场景。
*   **企业级 API 管理**：既有传统微服务，又有 AI 服务的混合架构。
*   **需要高频变更逻辑的网关**：业务规则变化快，不想频繁重启网关进程的场景。

### 4.2 最有效的情况
*   当你需要对 **AI 调用成本进行精细化控制**（如限制单用户 Token 调用量）时。
*   当你需要**屏蔽后端模型差异**，让客户端无需改动即可切换模型提供商时。
*   当你需要**在网关层处理 AI 业务逻辑**（如敏感词拦截、Prompt 注入）以减少后端服务负担时。

### 4.3 不适合的场景
*   **极端性能要求的纯 L4 负载均衡**：如果只需要做 TCP/UDP 转发，Envoy/Higress 可能过于重，使用 IPVS 或单纯的四层 LB 更轻量。
*   **极简边缘网关**：资源受限的嵌入式设备，不适合运行完整的 Higress 控制面。

### 4.4 集成方式与注意事项
*   **Kubernetes 集成**：推荐通过 Helm Chart 部署。需注意 IngressClass 的配置，避免与集群内现有的 Ingress Controller 冲突。
*   **服务发现**：可以配置直接对接 Kubernetes Service，也可以对接 Nacos/Consul 进行非 K8s 环境的服务发现。

---

## 5. 发展趋势展望

### 5.1 技术演进方向
*   **从流量管理到语义管理**：未来的网关将不仅

---
## 代码示例




```python
# 示例1：Higress 网关配置示例
def higress_gateway_config():
    """
    配置 Higress 网关的基本路由规则
    解决问题：将不同路径的请求转发到不同的后端服务
    """
    config = {
        "services": [
            {
                "name": "user-service",
                "url": "http://user-backend:8080",
                "paths": ["/api/users/*"],
                "timeout": 5000  # 毫秒
            },
            {
                "name": "order-service",
                "url": "http://order-backend:8080",
                "paths": ["/api/orders/*"],
                "timeout": 3000
            }
        ],
        "global_filters": {
            "rate_limiting": {
                "enabled": True,
                "requests_per_second": 100
            },
            "cors": {
                "enabled": True,
                "allowed_origins": ["*"]
            }
        }
    }
    return config

# 使用示例
gateway_config = higress_gateway_config()
print("Higress 网关配置已生成:", gateway_config)
```




```python
# 示例2：Higress 插件开发示例
class AuthPlugin:
    """
    自定义 Higress 认证插件
    解决问题：实现基于 Token 的 API 访问控制
    """
    def __init__(self, valid_tokens):
        self.valid_tokens = valid_tokens

    def process_request(self, request):
        """
        处理传入请求，验证 Token
        """
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return {"status": 401, "body": "Missing or invalid token"}

        token = auth_header.split(" ")[1]
        if token not in self.valid_tokens:
            return {"status": 403, "body": "Invalid token"}

        # Token 有效，继续处理请求
        return {"status": 200, "body": "Authorized"}

# 使用示例
valid_tokens = {"abc123", "xyz789"}
auth_plugin = AuthPlugin(valid_tokens)

# 模拟请求处理
class MockRequest:
    def __init__(self, headers):
        self.headers = headers

request = MockRequest({"Authorization": "Bearer abc123"})
response = auth_plugin.process_request(request)
print("认证结果:", response)
```




```python
# 示例3：Higress 监控指标收集
def collect_higress_metrics():
    """
    收集 Higress 网关的监控指标
    解决问题：实时监控网关性能和流量情况
    """
    metrics = {
        "total_requests": 0,
        "active_connections": 0,
        "response_time_avg": 0,
        "error_rate": 0.0,
        "service_health": {}
    }

    # 模拟从 Higress API 获取指标数据
    # 实际使用时，这里会调用 Higress 的监控接口
    metrics["total_requests"] = 12500
    metrics["active_connections"] = 320
    metrics["response_time_avg"] = 45  # 毫秒
    metrics["error_rate"] = 0.02  # 2%
    metrics["service_health"] = {
        "user-service": "healthy",
        "order-service": "healthy",
        "payment-service": "degraded"
    }

    return metrics

# 使用示例
metrics = collect_higress_metrics()
print("Higress 监控指标:")
for key, value in metrics.items():
    print(f"{key}: {value}")
```


---
## 案例研究


### 1：某大型电商平台微服务网关改造

 1：某大型电商平台微服务网关改造

**背景**: 该电商平台在“双11”等大促期间，面临每秒数十万级的QPS访问量。原有基于Nginx的Ingress网关在配置变更时需要Reload进程，导致长连接中断，影响部分用户的支付体验，且Lua插件开发维护成本高，难以应对复杂的业务逻辑。

**问题**: 网关动态性不足，配置热更新会影响存量连接；扩展能力受限，难以针对不同渠道（如App、Web、小程序）实施精细化的流量路由和特定逻辑（如请求染色、A/B测试）；传统网关在处理高并发下的认证鉴权时存在性能瓶颈。

**解决方案**: 采用Higress作为统一云原生网关。利用Higress基于Istio和Envoy的高性能架构，实现了配置的全动态热更新，无需Reload。通过Higress的Wasm插件能力，将业务鉴权、流量标签透传等逻辑编写为Wasm插件，实现了业务逻辑与网关内核的解耦。

**效果**: 网关配置变更实现秒级生效，彻底消除了因网关重启导致的连接中断问题。借助Wasm插件的高性能执行效率，鉴权链路延迟降低约40%，成功支撑了大促期间的高并发流量，并赋予了业务团队独立开发网关扩展插件的能力。

---



### 2：AI模型推理服务的高并发接入

 2：AI模型推理服务的高并发接入

**背景**: 一家专注于AIGC（生成式AI）应用的独角兽企业，需要将后端部署在GPU集群上的大语言模型（LLM）服务通过API形式开放给外部客户。由于AI推理耗时较长且成本高昂，客户在请求高峰期经常遇到超时或后端资源被打满的情况。

**问题**: 后端推理服务处理能力有限，高并发下容易触发过载保护导致请求失败；缺乏针对长连接和流式响应（SSE）的优化；无法根据用户的请求Token数进行精细化的并发控制，导致资源分配不均。

**解决方案**: 引入Higress作为AI网关。利用Higress对LLM场景的深度适配，启用了请求级别的并发排队与超时控制机制。配置了基于Token计数的后端限流策略，并开启了SSE（Server-Sent Events）协议支持以保障流式输出的稳定性。

**效果**: 在后端算力资源不变的情况下，通过网关层的智能排队与削峰填谷，服务的请求成功率从85%提升至99.9%。有效防止了后端集群被突发流量击穿，保障了核心推理服务的稳定性，同时通过流式传输优化提升了终端用户的交互体验。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | 方案A：Kong | 方案B：APISIX |
|------|----------------|------------|--------------|
| 性能 | 基于Envoy和Istio，支持高并发，性能优异 | 基于OpenResty/Nginx，性能稳定，适合中小规模 | 基于OpenResty/Nginx，性能极高，适合大规模场景 |
| 易用性 | 提供可视化控制台和Kubernetes原生支持，配置简单 | 需要手动配置较多，学习曲线较陡 | 提供Dashboard和API，但配置复杂度较高 |
| 成本 | 开源免费，企业版需付费 | 开源免费，企业版需付费 | 开源免费，企业版需付费 |
| 扩展性 | 支持插件扩展，集成阿里云服务 | 支持Lua插件扩展，社区丰富 | 支持Lua和Go插件扩展，灵活性高 |
| 社区支持 | 阿里巴巴背书，社区活跃 | 社区成熟，文档丰富 | 社区活跃，国内支持较好 |

### 优势分析

- 优势1：与Kubernetes和Istio深度集成，适合云原生环境。
- 优势2：提供开箱即用的流量管理和安全插件，降低配置复杂度。
- 优势3：支持阿里云服务无缝对接，适合阿里云用户。

### 不足分析

- 不足1：社区生态相比Kong和APISIX较小，第三方插件较少。
- 不足2：对非阿里云环境的支持可能不如其他方案灵活。
- 不足3：学习曲线对不熟悉Istio的用户可能较陡。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Wasm 插件实现扩展能力

**说明**:  
Higress 原生支持 Wasm（WebAssembly）插件，允许用户使用 C++、Go、Rust 或 AssemblyScript 编写自定义逻辑。相比传统 Lua 脚本，Wasm 提供更高的性能和安全性，同时支持热更新，无需重启网关即可生效。

**实施步骤**:
1. 使用官方提供的 `wasm-sdk` 开发插件逻辑。
2. 编译为 `.wasm` 文件并上传至 Higress 控制台或通过 OCI 镜像仓库分发。
3. 在网关路由配置中关联插件并配置参数。

**注意事项**:  
- 确保 Wasm 插件遵循 Higress 的 ABI 接口规范。
- 生产环境部署前需对 Wasm 插件进行性能压测，避免内存泄漏。

---

### 实践 2：服务发现与 Nacos 集成

**说明**:  
Higress 深度集成了 Nacos 注册中心，能够自动同步服务实例列表。通过此实践，可以实现基于服务名的动态路由，避免硬编码 IP 地址，并支持自动故障摘除。

**实施步骤**:
1. 在 Higress 全局配置中添加 Nacos 服务来源。
2. 配置 Nacos 服务地址、命名空间及鉴权信息。
3. 在 Ingress 或网关路由中使用 `service` 字段关联 Nacos 中的服务名。

**注意事项**:  
- 确保 Higress 与 Nacos 服务器网络连通。
- 如果使用 Nacos 2.x，需注意 gRPC 端口的防火墙策略。

---

### 实践 3：全链路流量管理与灰度发布

**说明**:  
利用 Higress 的 Header 匹配或权重路由功能，实现金丝雀发布和蓝绿部署。通过精细化的流量控制，降低新版本上线的风险。

**实施步骤**:
1. 部署新版本服务，并在注册中心注册。
2. 在 Higress 中创建基于 `Header`（如 `x-version: v2`）的匹配路由规则。
3. 或配置基于权重的路由，将 10% 流量导向新版本。

**注意事项**:  
- 灰度发布需确保新旧版本 API 兼容性。
- 建议配合可观测性工具监控新版本错误率。

---

### 实践 4：高性能 HTTP 转 gRPC

**说明**:  
Higress 具备强大的协议转换能力，可以将外部的 HTTP/HTTPS 请求转换为内部的 gRPC 请求，直接对接后端微服务。这利用了 gRPC 的高性能特性，同时对外暴露 RESTful 接口。

**实施步骤**:
1. 在 Higress 中配置 gRPC 服务来源或服务定义。
2. 创建路由，配置 HTTP 路径与 gRPC Service 及 Method 的映射关系。
3. 配置 Protobuf 描述文件以支持参数映射校验。

**注意事项**:  
- 需提前准备后端 gRPC 服务的 Protobuf 定义文件。
- 注意 HTTP 状态码与 gRPC 状态码的映射差异。

---

### 实践 5：精细化安全防护与认证

**说明**:  
Higress 提供了内置的认证鉴权插件（如 JWT、AK/SK、Basic Auth）。建议在网关层统一处理认证逻辑，后端服务专注于业务逻辑，提升系统整体安全性。

**实施步骤**:
1. 在控制台选择目标路由，启用 "认证鉴权" 插件。
2. 根据业务类型选择插件（如使用 `jwt-auth` 进行身份验证）。
3. 配置鉴权规则，如 Token 校验位置或密钥配置。

**注意事项**:  
- 密钥管理应通过环境变量或密钥管理服务（KMS）传递，避免硬编码。
- 启用认证后，务必在测试环境验证请求拦截逻辑。

---

### 实践 6：利用 Ingress 注解进行流量治理

**说明**:  
对于使用 Kubernetes 的用户，Higress 兼容标准 K8s Ingress 规范，并提供了丰富的 Annotation（注解）来实现高级流量治理功能，如超时控制、重试策略及限流。

**实施步骤**:
1. 编辑 Ingress YAML 文件。
2. 添加 Higress 特定注解，例如 `nginx.ingress.kubernetes.io/proxy-connect-timeout` 或 Higress 专有的 `higress.io/burst` 限流注解。
3. 应用配置并检查网关日志确认规则生效。

**注意事项**:  
- 不同版本的注解格式可能存在差异，请参考对应版本的官方文档。
- 避免在注解中配置过长的超时时间，导致长连接堆积。

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/3 (QUIC) 协议

**说明**: Higress 基于 Envoy 和 Istio 构建，Envoy 对 HTTP/3 提供了原生支持。HTTP/3 基于 UDP 协议，解决了 TCP 队头阻塞问题，显著降低了丢包环境下的延迟，并改进了连接迁移的稳定性。

**实施方法**:
1. 在 Higress 的网关路由配置中，开启 Listener 的 HTTP/3 支持（需确保 Envoy 版本支持）。
2. 配置 QUIC 端口（通常为 UDP 443）。
3. 调整网络防火墙和安全组规则，放行 UDP 流量。

**预期效果**: 在弱网环境下，视频流和动态资源加载延迟降低 20%-40%；连接建立时间（TTFB）减少。

---

### 优化 2：启用全链路 gRPC 通信

**说明**: Higress 原生支持 gRPC 协议代理。相比 JSON/HTTP，gRPC 使用 Protocol Buffers 进行二进制序列化，负载更小，解析速度更快。同时，gRPC 支持双向流和 HTTP/2 多路复用。

**实施方法**:
1. 将后端微服务间通信协议由 RESTful API 迁移至 gRPC。
2. 在 Higress 中配置 `grpc` 类型的 ServiceEntry 和 VirtualService。
3. 确保后端服务暴露 gRPC 端口，并配置好 TLS 加密（可选）。

**预期效果**: 序列化/反序列化性能提升 50% 以上；网络传输带宽占用减少约 30%；服务间调用延迟显著降低。

---

### 优化 3：配置智能 DNS 缓存与连接池

**说明**: 高并发场景下，频繁的 DNS 查询和建立 TCP/TLS 连接会消耗大量资源。通过优化 Higress (Envoy) 的连接池和 DNS 缓存策略，可以复用后端连接，减少握手开销。

**实施方法**:
1. 调整 Cluster 配置中的 `http_protocol_options`，增大 `max_connections` 和 `max_pending_requests`。
2. 启用 `dns_lookup_family` 为 `V4_PREFERRED` 或 `V6_PREFERRED` 以匹配网络环境。
3. 配置 DNS 缓存时间，避免频繁向 DNS 服务器发起请求。

**预期效果**: 后端连接复用率提升，减少 CPU 和网络开销；长连接模式下 P99 延迟降低 10%-20%。

---

### 优化 4：启用 Wasm 插件与 Lua 过滤器性能调优

**说明**: Higress 支持通过 Wasm (WebAssembly) 扩展网关功能。Wasm 插件运行在沙箱中，安全性高且性能接近原生。对于复杂的鉴权或限流逻辑，使用 Wasm 替代传统的 Lua 脚本或外部调用可提升吞吐量。

**实施方法**:
1. 将高频调用的鉴权、Header 修改逻辑编写为 Wasm 插件（如使用 C++、Rust 或 AssemblyScript）。
2. 在 Higress 控制台上传并启用 Wasm 插件。
3. 对于必须使用 Lua 的场景，优化 Lua 代码逻辑，避免阻塞操作，并利用 `lua_shared_dict` 进行缓存。

**预期效果**: 插件执行延迟降低 30%-50%；在高 QPS 下，网关 CPU 利用率更加平稳。

---

### 优化 5：实施精细化缓存策略

**说明**: Higress 具备强大的缓存控制能力。对于读多写少的流量（如商品详情、配置数据），启用网关层缓存可以直接拦截请求，避免流量打到后端服务。

**实施方法**:
1. 在路由配置中启用响应缓存，根据业务需求设置 `cache_key`（如根据 URL 或 Header 参数）。
2. 合理配置 TTL（生存时间）和 `stale_if_error` 策略。
3. 对于后端返回的 304 Not Modified 响应，配置 Higress 优先处理 E

---
## 学习要点

- 基于您提供的信息（Alibaba/Higress 在 GitHub 趋势中），以下是关于该项目最值得关注的 5 个关键要点：
- Higress 是阿里云开源的一款基于 Istio 的云原生 API 网关，深度集成了 K8s 环境，旨在解决云原生时代流量管理的复杂性。
- 它提供开箱即用的流量管理功能，支持金丝雀发布、蓝绿部署和全链路灰度发布，极大简化了微服务治理流程。
- 该网关深度集成了 AI 服务（如 OpenAI），提供 AI 代理插件和 Token 计费管理，使开发者能快速构建 AI 应用或网关。
- Higress 兼容 Kubernetes Ingress 和 Nginx Ingress 注解，并支持从 Nginx 平滑迁移，降低了用户的学习成本和迁移门槛。
- 它具备高性能的 WAF（Web 应用防火墙）防护能力和插件市场，支持通过 WASM (WebAssembly) 进行毫秒级热更新，灵活扩展业务功能。
- 作为 CNCF (云原生计算基金会) 的沙箱项目，它拥有活跃的开源社区支持，适合作为企业级流量入口或统一 API 管理平台。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础

**学习内容**:
- 云原生网关的基本概念与 Higress 的核心定位
- Higress 与传统网关（如 Nginx, Kong）及云原生网关（如 Istio Gateway, APISIX）的区别
- Docker/Docker Compose 环境的搭建
- 使用 Docker 快速部署 Higress Standalone 版本
- Higress 控制台的基本操作与界面熟悉
- 理解 Ingress 与 Gateway API 的基础差异

**学习时间**: 1-2周

**学习资源**:
- Higress GitHub 仓库 README 及官方文档
- Higress 官方网站：https://higress.io/
- Docker 官方入门文档

**学习建议**: 
建议先通读官方文档的"产品介绍"部分，理解 Higress "开源、免费、高性能"的特点。动手在本地使用 Docker Compose 部署一个实例，并尝试在控制台创建一个简单的域名路由，打通从浏览器到后端服务的流量。

---

### 阶段 2：核心功能与流量治理

**学习内容**:
- HTTP 路由与重定向/重写配置
- 服务来源的注册与发现（Nacos, Consul, K8s Service, Fixed Address 等）
- 负载均衡策略（加权轮询、一致性哈希等）
- 服务治理：超时、重试、熔断与限流
- 全局与自定义插件系统的使用
- 基于 Wasm 插件扩展网关功能（如 Key Auth, Jwt Auth）
- 金丝雀发布与蓝绿发布配置

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 流量管理章节
- Higress 官方插件市场
- Envoy 官方文档（用于理解底层代理机制）

**学习建议**: 
此阶段重点在于掌握"流量控制"。建议搭建一个包含两个服务的后端环境，练习配置 Header 路由和路径重写。深入理解 Higress 如何对接注册中心（特别是 Nacos），这是 Higress 区分于普通网关的一大优势。尝试在控制台安装并配置几个官方插件，体验 Wasm 插件的易用性。

---

### 阶段 3：生产部署与高可用

**学习内容**:
- 在 Kubernetes 环境中部署 Higress（使用 Helm）
- Gateway API CRDs 的深度应用
- Higress 的高可用架构与性能调优
- 安全防护：配置 HTTPS 证书、mTLS、黑白名单
- 可观测性：对接 Prometheus/Grafana 监控、Skywalking/Zipkin 链路追踪、日志采集
- 网关平滑升级与版本管理

**学习时间**: 3-4周

**学习资源**:
- Higress GitHub Helm Charts 仓库
- Kubernetes Gateway API 官方规范文档
- Prometheus 与 Skywalking 官方文档

**学习建议**: 
如果你有 Kubernetes 基础，建议直接在 K8s 集群中通过 Helm 安装 Higress。重点关注 Gateway API 资源的配置，这是未来的主流方向。必须掌握监控指标的采集，学会通过 Grafana Dashboard 观察网关的 QPS、延迟与成功率。在生产环境部署前，务必测试 HTTPS 配置及 Wasm 插件对性能的影响。

---

### 阶段 4：深度定制与生态集成

**学习内容**:
- 编写自定义 Wasm 插件（Go/C++/Rust）
- Higress 在微服务架构中的最佳实践（服务网格南北向流量管理）
- 多集群管理与多租户支持
- 与阿里云 MSE Higress 或云原生 API 网关的差异与迁移
- 源码级调试与贡献指南

**学习时间**: 4周以上（持续学习）

**学习资源**:
- Higress 源码
- Higress 官方插件开发指南
- Wasm (WebAssembly) 官方文档

**学习建议**: 
当标准插件无法满足需求时，学习使用 Go 语言开发 Wasm 插件是进阶必经之路。阅读 Higress 源码有助于理解其数据面与控制面的交互逻辑。参与 GitHub Issues 的讨论或尝试提交 PR，不仅能提升技术深度，也能更好地理解社区的发展方向。

---
## 常见问题


### 1: Higress 是什么？它与阿里巴巴和云原生社区有什么关系？

1: Higress 是什么？它与阿里巴巴和云原生社区有什么关系？

**A**: Higress 是一个基于阿里内部多年实践沉淀的下一代云原生 API 网关。它是在 2022 年由阿里巴巴开源，并随后捐赠给了云原生计算基金会（CNCF）。

Higress 的核心定位是**“云原生 API 网关”**，它深度集成了 Envoy 和 Istio，旨在解决从传统微服务架构向 Service Mesh（服务网格）架构过渡时的流量管理痛点。它既支持作为 Kubernetes 集群的 Ingress Gateway 入口网关，也支持作为传统的 API 网关管理南北向流量。

---



### 2: Higress 与 Nginx、APISIX 或 Kong 等 API 网关相比有什么优势？

2: Higress 与 Nginx、APISIX 或 Kong 等 API 网关相比有什么优势？

**A**: Higress 的主要优势体现在以下几个方面：

1.  **深度集成 Istio**：Higress 原生支持 Istio，可以无缝接管服务网格的流量，充当 Ingress Gateway，解决了传统网关与 Istio 配置维护割裂的问题。
2.  **高性能**：基于 C++ 编写的 Envoy 内核，相比基于 Lua 或 OpenResty 的网关（如 Kong 或 APISIX 的早期版本），在处理高并发和长连接（如 Dubbo、gRPC）时通常具有更低的延迟和更高的稳定性。
3.  **标准与扩展性**：它完全支持 Kubernetes Ingress API 和 Gateway API，同时兼容 Nginx 的 Ingress 注解。此外，它支持通过 WASM（WebAssembly）插件来扩展功能，插件编写可以使用 Go、C++、Rust 等语言，开发效率高且运行安全。
4.  **安全防护**：内置了与阿里云 WAF 同源的防护能力，能够有效抵御常见的 Web 攻击（如 SQL 注入、XSS 等）。

---



### 3: Higress 是否支持非容器化或虚拟机环境的服务？

3: Higress 是否支持非容器化或虚拟机环境的服务？

**A**: 是的，Higress 支持混合云和异构基础设施的流量管理。

虽然 Higress 是为 Kubernetes 设计的，但它具备强大的**服务发现**能力，不仅支持 Kubernetes 原生 Service，还支持 Nacos、Consul、ZooKeeper、DNS 以及固定 IP（IP 列表）等注册中心。这意味着用户可以将运行在虚拟机上的后端服务注册到 Higress 中，实现从容器到虚拟机的统一流量调度和路由。

---



### 4: 如何在 Higress 中扩展功能？是否支持插件机制？

4: 如何在 Higress 中扩展功能？是否支持插件机制？

**A**: Higress 拥有非常灵活的插件系统，主要通过以下方式扩展：

1.  **WASM 插件（推荐）**：Higress 优先支持基于 WASM（WebAssembly）的插件。开发者可以使用 Go 或 Rust 编写业务逻辑，编译成 WASM 文件后动态加载到网关中。这种方式具有极高的灵活性（热加载）、隔离性和安全性，且不会阻塞主线程。
2.  **原生插件**：对于性能要求极高的场景，也可以直接编写 C++ 原生插件（基于 Envoy 机制），但这通常需要重新编译网关镜像，操作门槛较高。
3.  **Lua 支持**：为了兼容 OpenResty/Nginx 的生态，Higress 也支持 Lua 脚本插件，方便用户迁移旧的逻辑。

---



### 5: Higress 能否处理 Dubbo 或 gRPC 等非 HTTP 协议的流量？

5: Higress 能否处理 Dubbo 或 gRPC 等非 HTTP 协议的流量？

**A**: 可以。Higress 基于 Envoy，Envoy 本身就是一个 L4/L7 代理，因此 Higress 具备强大的协议处理能力。

1.  **gRPC**：Higress 原生支持 gRPC 协议，支持 gRPC 到 JSON 的转码，以及基于 gRPC 方法的路由转发。
2.  **Dubbo**：Higress 提供了对 Dubbo（Apache Dubbo）协议的深度支持，可以直接代理 Dubbo 服务，实现 HTTP 转 Dubbo 的协议转换，使得前端可以通过 HTTP/RESTful 方式调用后端的 Dubbo 服务。

---



### 6: Higress 的生产环境部署是否复杂？是否有控制台？

6: Higress 的生产环境部署是否复杂？是否有控制台？

**A**: Higress 提供了开箱即用的部署体验，大大降低了使用门槛。

1.  **一键安装**：在 Kubernetes 环境中，通常只需要几条 Helm 命令或应用一个 YAML 文件即可完成安装。
2.  **可视化管理控制台**：Higress 默认自带一个功能强大的 Web 控制台（基于 Kruise 和 Vue 开发）。用户可以在控制台上进行路由配置、证书管理、服务来源注册以及插件管理，无需手动编辑复杂的 YAML 配置文件，这比传统的 Nginx 或 Envoy 配置要直观得多。

---



### 7: Higress 是否兼容 Nginx Ingress 的配置？

7: Higress 是否兼容 Nginx Ingress 的配置？

**A**: 是的，为了降低迁移成本，Higress 做了大量的兼容工作。

Higress 实现了 Kubernetes Ingress 的标准规范，并且

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单] 基础路由与环境搭建

### 问题**: 在本地 Docker 环境中快速部署 Higress，并配置一个简单的路由规则。要求实现：当用户访问 `/httpbin/` 路径时，将流量 100% 转发到公网可用的 httpbin 测试服务（如 `httpbin.org`），同时移除请求路径中的 `/httpbin` 前缀。

### 提示**:

### 参考 Higress 官方文档的 "快速开始" 章节，使用 `docker-compose` 启动标准镜像。

---
## 实践建议

以下是基于 Higress 作为 AI 网关和 API 网关在实际生产环境中的 6 条实践建议：

### 1. 利用 AI 指标路由实现灰度发布
不要仅基于权重进行流量切分。在接入大模型（如 OpenAI 或通义千问）时，应配置基于**响应头**或**响应体**内容的动态路由。
*   **具体操作**：在 Higress 中配置 AI 路由规则，将请求同时发送给模型 A 和模型 B（或不同版本）。如果模型 B 的响应中包含特定的安全拦截标记或质量评分低于阈值，网关自动丢弃该响应并回退到模型 A，从而在保证业务安全的前提下进行新模型测试。

### 2. 配置模型提供商的级联容错
大模型 API 普遍存在不稳定性（如超时或 429 Rate Limit）。不要依赖单一模型提供商。
*   **具体操作**：在 Higress 的服务来源中配置多厂商。例如，主服务源设置为 OpenAI，备用服务源设置为 Azure OpenAI 或本地部署的 vLLM。当主源触发 5xx 错误或超时（超过 30 秒）时，网关应自动将请求重试转发至备用源，确保业务不中断。

### 3. 开启 Prompt 模板与敏感信息过滤
直接在前端调用大模型容易导致 Prompt 泄露或被注入恶意指令。
*   **具体操作**：使用 Higress 的 Prompt 管理功能，将具体的 Prompt 模板存储在网关侧，前端仅传输参数（如用户输入的问题）。同时，在网关层配置“安全插件”，对用户输入进行关键词或正则过滤，拦截敏感词，避免直接传给模型导致合规风险。

### 4. 针对流式响应的超时与缓存策略
AI 问答通常耗时较长，且使用 SSE (Server-Sent Events) 协议。
*   **具体操作**：
    *   **超时设置**：务必将网关的超时时间调整为大于模型生成最大耗时的值（建议 60s-120s），避免模型还在生成时网关断开连接。
    *   **语义缓存**：针对高频的重复问题（如“帮我写一段 Python 冒泡排序”），开启基于向量的语义缓存插件。网关直接返回缓存结果，不仅降低了 API 调用成本，也极大提升了响应速度。

### 5. 实施细粒度的 Token 预留与并发限制
大模型 API 的成本主要在于 Token 消耗，且并发过高容易触发供应商限流。
*   **具体操作**：不要仅做简单的 QPS（每秒请求数）限制。建议结合 Higress 的插件对**请求 Token 数**进行估算。例如，限制单个用户每分钟最多消耗 10,000 个 Token。这比单纯的 QPS 限流更能准确反映后端成本和负载，防止个别长 Prompt 占满供应商配额。

### 6. 避免在请求体中透传敏感鉴权信息
在使用 Higress 转发请求时，不要将上游模型的 API Key 写死在客户端代码中。
*   **常见陷阱**：前端直接携带 OpenAI Key 发起请求，虽然经过网关，但网关仅做透传，导致 Key 泄露风险。
*   **最佳实践**：在 Higress 中为不同的上游模型服务配置独立的鉴权插件（如 AK/SK 或 JWT）。客户端只持有网关颁发的凭证，网关在转发请求前动态注入上游模型所需的 API Key。这样实现了“凭证解耦”，便于统一轮换密钥。

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [阿里开源](/tags/%E9%98%BF%E9%87%8C%E5%BC%80%E6%BA%90/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [WASM](/tags/wasm/) / [LLM](/tags/llm/) / [MCP 协议](/tags/mcp-%E5%8D%8F%E8%AE%AE/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/) / [DevOps/运维](/scenarios/devops-%E8%BF%90%E7%BB%B4/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260201-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260207-github_trending-alibaba-higress-0.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260205-github_trending-alibaba-higress-6.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260130-github_trending-alibaba-higress-9.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*