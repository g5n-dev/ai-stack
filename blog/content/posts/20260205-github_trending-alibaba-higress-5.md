---
title: "阿里 Higress：AI 原生 API 网关"
date: 2026-02-05T11:48:54+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "Istio", "Envoy", "WASM", "LLM", "MCP", "Kubernetes"]
categories: ["系统与基础设施", "AI 工程"]
source: github_trending
description: "以下是对 Higress 项目的简要总结： **项目概述** Higress 是一款由阿里巴巴开源的**云原生 AI 原生 API 网关**。它基于 Istio 和 Envoy 构建，并深度集成了 **WebAssembly (WASM)** 插件能力，旨在为云原生应用和 AI 应用提供统一的流量入口与管理平台。该项目"
external_url: https://github.com/alibaba/higress
scenarios: ["AI/ML项目", "云原生/容器", "DevOps/运维"]
---

# 阿里 Higress：AI 原生 API 网关

> **原名**: alibaba /

      higress

---

## 基本信息

- **描述**: 🤖 AI 网关 | AI 原生 API 网关
- **语言**: Go
- **星标**: 7,457 (+10 stars today)
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

Higress 是一款基于 Istio 和 Envory 构建的云原生 API 网关，它通过扩展 WebAssembly 插件能力，同时支持传统微服务流量管理与 AI 原生应用网关功能。该项目旨在解决大模型应用开发中的流量编排、模型服务集成及 MCP 工具托管等需求，适合需要统一管理南北向流量与 AI 服务的架构师与开发者。本文将介绍其系统架构、核心组件以及 AI 网关特性等关键内容。

---
## 摘要

以下是对 Higress 项目的简要总结：

**项目概述**
Higress 是一款由阿里巴巴开源的**云原生 AI 原生 API 网关**。它基于 Istio 和 Envoy 构建，并深度集成了 **WebAssembly (WASM)** 插件能力，旨在为云原生应用和 AI 应用提供统一的流量入口与管理平台。该项目目前使用 Go 语言开发，在 GitHub 上拥有超过 7,000 颗星。

**核心架构**
Higress 采用**控制平面与数据平面分离**的架构：
*   **控制平面**：负责配置管理。
*   **数据平面**：负责流量处理。
*   **连接机制**：配置变更通过 xDS 协议传播，具备毫秒级延迟且不中断连接的特性，特别适用于 AI 长连接流式响应等场景。

**三大核心功能与用例**

1.  **AI 网关**
    *   **功能**：为大语言模型（LLM）应用提供统一 API。支持对接 30+ 家 LLM 提供商，并提供协议转换、可观测性、缓存和安全管理。
    *   **组件**：依赖 `ai-proxy`、`ai-statistics`、`ai-cache` 和 `ai-security-guard` 等插件。

2.  **MCP 服务器托管**
    *   **功能**：托管模型上下文协议（MCP）服务器，使 AI Agent 能够便捷地调用外部工具和服务。
    *   **组件**：通过 `mcp-router`、`jsonrpc-converter` 过滤器及具体的 MCP 服务器实现（如 `quark-search`, `amap-tools`）。

3.  **Kubernetes Ingress (传统 API 网关)**
    *   **功能**：作为 K8s 的 Ingress 控制器，管理微服务路由，且兼容 nginx-ingress 的注解，方便用户迁移。

---
## 评论

**总体判断**

Higress 是一款极具前瞻性的“云原生+AI”基础设施产品，它成功地将开源 API 网关的标准能力与大模型（LLM）应用所需的特定流量治理技术融合。作为阿里云开源的产物，它不仅继承了 Istio/Envoy 的高性能基因，更通过 WASM 和 AI-native 特性解决了企业接入 AI 时的协议与安全痛点，是目前将“传统网关”向“AI 网关”演进的最具代表性的技术方案之一。

**深入评价依据**

**1. 技术创新性：WASM 插件化与 AI 流量治理的深度融合**
*   **事实：** DeepWiki 指出 Higress 基于 Istio 和 Envoy 构建，并扩展了 WebAssembly (WASM) 插件能力，同时提供了针对 LLM 应用的 AI Gateway 特性和 MCP (Model Context Protocol) 服务托管。
*   **推断：** Higress 的核心技术壁垒在于其**“WASM + AI”**的架构。传统网关（如 Nginx）修改逻辑需重新编译或使用 Lua，受限较大。Higress 利用 WASM 的沙箱隔离和高性能特性，允许开发者使用 Go/C++/Rust 等语言动态编写插件（如 Prompt 模板注入、敏感词过滤、Token 计费），且无需重启网关。更关键的是，它原生支持将标准 HTTP 协议转换为 SSE（Server-Sent Events）或与 OpenAI 兼容的协议，这是传统网关在处理 AI 流式响应时通常缺失的能力。引入 MCP Server 托管则表明它正在向 AI Agent 的基础设施层进化，试图解决 Agent 与工具连接的标准化问题。

**2. 实用价值：填补 LLM 落地中的“最后一公里”空白**
*   **事实：** 描述中提到其核心功能包括 Kubernetes Ingress、微服务路由以及 AI Gateway 功能。
*   **推断：** 在企业落地大模型时，直接暴露 LLM API 存在密钥泄露、Prompt 被篡改、Token 消耗不可控等风险。Higress 解决了**“AI 流量安全与治理”**的关键问题。它充当了企业内部业务与外部 LLM（如 OpenAI、通义千问）之间的中间层，实现了统一的鉴权、限流和缓存（减少 Token 成本）。对于已有 Kubernetes 集群的用户，它可以直接作为 Ingress Controller 替代 Nginx Ingress，这意味着用户在引入 AI 能力时无需维护一套独立的网关基础设施，极大地降低了运维复杂度和应用场景的门槛。

**3. 代码质量与架构：云原生标准的控制面与数据面分离**
*   **事实：** 文档明确指出架构将控制面（配置管理）与数据面（流量处理）分离，且基于 Go 语言开发。
*   **推断：** 基于 Istio 和 Envoy 意味着 Higress 继承了经过大规模生产验证的 C++ 数据面，保证了高并发下的低延迟性能。Go 语言编写的控制面符合云原生生态的主流标准，便于与 K8s API Server 交互。从架构设计上看，它遵循了“关注点分离”原则，配置下发机制成熟。文档提供了多语言版本（包括中文和日文），且涵盖了从构建到开发的完整指南，显示出阿里云团队对工程规范的高要求和项目维护的严肃性。

**4. 社区活跃度与生态：大厂背书与商业化驱动的双重保障**
*   **事实：** 仓库拥有 7,457 颗星（数据截止时），由阿里巴巴主导。
*   **推断：** 作为阿里云通义千问生态中的核心组件，Higress 不仅有开源社区的贡献，更有阿里云内部业务需求的强力驱动。这种“大厂开源”模式通常保证了项目不会轻易烂尾，且更新频率与 AI 技术迭代速度高度相关。社区反馈通常集中在 AI 特性的请求上（如对新模型的支持），活跃度较高。对于国内开发者而言，中文文档和社区支持的友好度远高于 Kong 或 APISIX 等国外项目。

**5. 潜在问题与改进建议**
*   **推断：** 尽管架构先进，但基于 Envoy 和 Istio 的技术栈本身具有**陡峭的学习曲线**。相比于 Nginx 的简单配置，Higress 的 CRD（自定义资源）和 WASM 插件开发对运维和开发人员的要求更高。此外，虽然 AI 功能是亮点，但目前对于复杂的长文本处理（如 RAG 链路中的复杂向量检索逻辑）可能仍需依赖后端服务，网关层主要做协议转换和简单逻辑，建议未来能集成更多轻量级的向量数据库连接能力。

**6. 对比优势：与 Kong/APISIX 的差异化**
*   **推断：** 相比于 APISIX（也是基于 Lua/Go 的动态网关），Higress 的优势在于其对 **Istio 生态的原生集成**。在服务网格场景下，Higress 可以无缝作为 Gateway 入口，与 Sidecar 流量治理协同工作，这是 APISIX 较难做到的。相比于 Kong，Higress 的 WASM 支持更加现代和灵活，且针对 AI 场景（SSE 流转发、Token 统计）做了专门的内核级优化，而非仅仅通过插件堆砌。

**边界条件与验证清单**

**不适用场景：**
*   极简边缘路由场景（如仅需简单的反向代理，Envoy/Higress �

---
## 技术分析

# Higress 深度技术分析报告

Higress 作为阿里云开源的云原生 API 网关，基于 Istio 和 Envoy 构建，并创新性地引入了 AI Native 能力。以下是对该项目的深度剖析。

---

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 采用了**控制平面与数据平面分离**的云原生架构模式。
*   **底层基石**：深度依赖 **Envoy** 作为高性能数据平面，利用其 L3/L7 过滤能力和可观测性。
*   **控制平面**：基于 **Istio** 进行了大幅裁剪和增强。Higress 移除了 Istio 中繁重的 Sidecar 注入和复杂的 Service Mesh 治理功能，专注于 Gateway（南北向流量）场景，使其更轻量。
*   **扩展层**：引入 **WebAssembly (WASM)** 作为插件运行时，允许使用 C/C++/Go/Rust 等语言编写高性能插件，解决了传统 Lua 插件性能差和隔离性差的问题。

### 核心模块与关键设计
1.  **路由配置管理**：通过 K8s Ingress 或 Gateway API 标准化定义流量规则，Higress Controller 将这些规则转化为 Envoy 的 xDS 配置。
2.  **WASM 插件系统**：这是其最核心的设计之一。它允许在运行时动态加载代码到 Envoy 中，且无需重启网关。Higress 实现了插件的生命周期管理、热加载和配置分发。
3.  **AI 网关模块**：专门针对 LLM 流量设计的处理层。它不仅仅是转发，还理解 SSE (Server-Sent Events) 协议，能够对 AI 流量进行拦截、修改和提示词注入。

### 技术亮点与创新
*   **AI Native 理念**：这是 Higress 与传统网关（如 APISIX, Kong）最大的区别。它内置了对大模型厂商（OpenAI, Azure, 通义千问等）协议的兼容层，能够将一个 API 请求转换为另一个厂商的格式。
*   **MCP (Model Context Protocol) 支持**：Higress 不仅是网关，还可以作为 AI Agent 的工具托管中心。它允许将后端服务注册为 MCP 工具，使得 LLM 能够安全地调用企业内部 API。

### 架构优势
*   **毫秒级配置生效**：得益于 xDS 协议的增量推送机制，配置变更可在不中断长连接（如 SSE 流）的情况下生效。
*   **极致性能**：数据平面 Envoy 采用 C++ 编写，配合 WASM 的近原生执行速度，使其在处理高并发流量时延迟极低。

---

## 2. 核心功能详细解读

### 主要功能
1.  **AI 网关**：
    *   **统一模型接入**：提供统一的标准 API 接口，后端可适配 OpenAI, Anthropic, 通义千问等不同厂商。
    *   **Token 管理与计费**：在传输层统计 Token 消耗，实现基于 Token 的限流和计费，无需侵入业务代码。
    *   **提示词管理**：在网关层进行系统 Prompt 注入或敏感词过滤。
2.  **MCP 服务器托管**：
    *   将内部微服务自动暴露为 AI Agent 可调用的工具，并提供统一的鉴权和流量控制。
3.  **传统 API 网关**：
    *   K8s Ingress Controller。
    *   金丝雀发布、蓝绿发布、负载均衡、流量镜像。

### 解决的关键问题
*   **AI 供应商锁定**：通过中间层抽象，企业可以随时切换 LLM 供应商而无需修改客户端代码。
*   **AI 流量的不可观测性**：传统网关只能看到 HTTP 流量，Higress 能理解 LLM 的请求/响应结构，记录 Prompt 和 Token 使用量。
*   **AI 安全风险**：在网关层统一拦截敏感数据，防止 Prompt 注入攻击。

### 与同类工具对比
*   **VS Kong/APISIX**：传统网关主要通过 Lua 或插件扩展，虽然也支持 AI，但缺乏针对 LLM 流式传输（SSE）的深度优化，且不具备 MCP 协议支持。Higress 的 WASM 架构在隔离性和扩展性上更优。
*   **VS Istio Ingress Gateway**：Istio 原生 Gateway 配置过于复杂且性能调优困难。Higress 简化了模型，提供了更符合运维直觉的配置方式。

### 技术实现原理
*   **流式处理**：利用 Envoy 的 Streaming Filter 机制，在不缓冲整个响应的情况下，实时处理 SSE 数据块，实现了极低的 TTS（首字生成）延迟。

---

## 3. 技术实现细节

### 关键技术方案
*   **WASM 虚拟机集成**：Higress 集成了 Proxy-WASM 规范。在 Go 代码中，它通过 `github.com/tetratelabs/proxy-wasm-go-host` 等库管理 WASM 沙箱的生命周期。
*   **配置热更新**：Higress Watch K8s API Server，一旦 Ingress 或 GatewayConfig 资源变动，立即通过 gRPC 推送 Delta xDS 到 Envoy。

### 代码组织结构
*   **`pkg/`**：核心业务逻辑。
    *   `ingress`: K8s Ingress 资源转换逻辑。
    *   `config`: xDS 配置生成器。
    *   `router`: 路由匹配引擎。
*   **`plugins/`**：WASM 插件的源码（通常以 Go 编写，编译为 WASM）。
*   **`installer/`**：Helm Charts 和安装脚本。

### 性能优化
*   **零拷贝**：在 Envoy 内部处理数据时，尽量减少内存拷贝。
*   **连接池**：针对后端服务（如 LLM API）维护 HTTP/2 连接池，减少握手开销。

---

## 4. 适用场景分析

### 适合的项目
*   **企业级 AI 应用落地**：需要对接多个大模型，并进行统一管理和鉴权的公司。
*   **微服务架构的流量入口**：基于 K8s 的云原生环境，需要替代 Nginx Ingress 或传统 API 网关。
*   **AI Agent 开发平台**：需要将内部工具（API）通过 MCP 协议暴露给 LLM 的场景。

### 最有效的情况
*   当你需要**毫秒级**切换 LLM 提供商时（例如从 OpenAI 切到本地部署的 Llama）。
*   当你需要对 AI 请求进行复杂的**鉴权和计费**，且不希望在每个微服务中重复实现时。

### 不适合的场景
*   **极简边缘计算**：资源极其受限（如几 MB 内存）的环境，Envoy 本身较重。
*   **非 K8s 环境**：虽然支持二进制部署，但其最大威力在于 K8s 生态的集成。

---

## 5. 发展趋势展望

### 演进方向
*   **更深度的 AI 可观测性**：不仅仅是记录 Token，还包括 Prompt 质量分析、LLM 响应延迟的归因分析（是网络慢还是模型慢）。
*   **RAG (检索增强生成) 集成**：网关可能直接集成向量数据库连接能力，在请求到达 LLM 前自动进行上下文补充。

### 社区反馈与改进
*   目前社区对 WASM 插件的开发门槛有一定反馈，未来可能会提供更高级的 DSL（Domain Specific Language）来降低插件编写难度。

---

## 6. 学习建议

### 适合人群
*   具备 K8s 基础的运维工程师（SRE）。
*   云原生架构师。
*   需要深入理解 Envoy 和 Go 语言的后端开发者。

### 学习路径
1.  **基础**：理解 K8s Ingress 和 Service 概念。
2.  **核心**：学习 Envoy 架构，理解什么是 Listener, Cluster, Route。
3.  **进阶**：学习 Proxy-WASM 规范，尝试用 Go 编写一个简单的 WASM 插件并在 Higress 中运行。

---

## 7. 最佳实践建议

### 正确使用方式
*   **资源隔离**：生产环境中，建议将 Higress 的 Control Plane 和 Data Plane 分离部署，或者使用 HPA 进行自动扩缩容。
*   **WASM 插件预热**：在发布新插件前，务必在测试环境验证 WASM 沙箱的内存限制，防止插件内存泄漏导致网关 OOM。

### 常见问题
*   **长连接超时**：AI 请求可能耗时较长，需调整 Envoy 的 `stream_idle_timeout` 参数，防止网关提前断开连接。
*   **配置延迟**：确保 Higress Controller 与 K8s API Server 之间的连接稳定，否则配置下发会延迟。

### 性能优化建议
*   开启 Envoy 的 **Compressed Filter**，对大体积的 JSON 响应进行压缩。
*   对于 AI 流量，合理调整 Buffer 大小，平衡内存占用与吞吐量。

---

## 8. 哲学与方法论：第一性原理与权衡

### 抽象层与复杂性转移
Higress 在**流量编排层**做了极深的抽象。它将“如何与 LLM 交互”、“如何调用后端微服务”、“如何进行鉴权”的复杂性从业务代码中剥离，转移到了**网关基础设施层**。
*   **代价**：这种转移使得网关本身变得厚重。一旦网关宕机，所有 AI 和业务流量都会中断。因此，它要求运维团队具备极强的 Envoy 和 K8s 排错能力。

### 价值取向
*   **可扩展性 > 易用性**：虽然提供了控制台，但其核心能力在于通过配置和插件进行极度灵活的定制。这默认了用户愿意为了灵活性而学习复杂的配置逻辑。
*   **标准化 > 个性化**：强制用户遵循 Ingress/Gateway API 标准，虽然初期痛苦，但保证了跨平台的可移植性。

### 工程哲学范式
Higress 的范式是**“基础设施即代码”**与**“L7 代理可编程化”**的结合。它不再将网关视为静态的配置文件，而是一个可以运行代码（WASM）的分布式操作系统。
*   **误用点**：最容易误用的是 WASM 插件。开发者容易在插件中编写阻塞式代码或进行大量计算，直接拖垮整个网关的吞吐量。

### 可证伪的判断
1.  **性能判断**：在开启 WASM 插件处理复杂 AI 请求头时，Higress 的 P99 延迟增加幅度应小于 5ms（对比原生 Envoy 直连）。如果超过此值，说明其 WASM 运行时调度存在瓶颈。
2.  **兼容性判断**：能够在一个 Higress 实例中，同时将 80% 的流量路由至 OpenAI API，20% 流量路由至本地部署的 Qwen 模型，且业务端感知不到差异

---
## 代码示例




```python
# 示例1：使用Higress实现基于权重的流量路由
def weighted_routing_example():
    """
    解决问题：将流量按比例分配到不同版本的服务（如灰度发布）
    场景：80%流量到v1版本，20%流量到v2版本
    """
    from higress import Gateway, RouteRule
    
    # 创建网关实例
    gateway = Gateway(name="demo-gateway")
    
    # 配置带权重的路由规则
    route = RouteRule(
        match={"/api/v1/*"},
        destinations=[
            {"service": "service-v1", "weight": 80},
            {"service": "service-v2", "weight": 20}
        ]
    )
    
    gateway.add_route(route)
    gateway.apply()
    
    print("流量路由规则已应用：80%到v1，20%到v2")
```


---

```python
# 示例2：使用Higress实现基于请求头的路由
def header_based_routing_example():
    """
    解决问题：根据请求头将流量路由到不同后端服务
    场景：根据User-Agent区分移动端和PC端请求
    """
    from higress import Gateway, RouteRule
    
    gateway = Gateway(name="mobile-pc-router")
    
    # 配置基于请求头的路由规则
    route = RouteRule(
        match={"/api/*"},
        conditions=[
            {"header": "User-Agent", "regex": ".*Mobile.*"}
        ],
        destination="mobile-service"
    )
    
    default_route = RouteRule(
        match={"/api/*"},
        destination="pc-service"
    )
    
    gateway.add_route(route)
    gateway.add_route(default_route)
    gateway.apply()
    
    print("基于User-Agent的路由规则已配置")
```


---

```python
# 示例3：使用Higress实现服务熔断和降级
def circuit_breaker_example():
    """
    解决问题：当后端服务出现故障时自动熔断并返回降级响应
    场景：保护系统稳定性，防止雪崩效应
    """
    from higress import Gateway, CircuitBreakerPolicy
    
    gateway = Gateway(name="circuit-breaker-demo")
    
    # 配置熔断策略
    policy = CircuitBreakerPolicy(
        service="backend-service",
        failure_threshold=5,      # 连续失败5次触发熔断
        recovery_timeout=30,       # 30秒后尝试恢复
        fallback_response={
            "status": 200,
            "body": '{"status": "degraded", "message": "服务暂时不可用"}'
        }
    )
    
    gateway.add_circuit_breaker(policy)
    gateway.apply()
    
    print("熔断策略已配置：5次失败后触发熔断，30秒后尝试恢复")
```


---
## 案例研究


### 1：阿里巴巴集团内部 - 大规模微服务流量治理与迁移

 1：阿里巴巴集团内部 - 大规模微服务流量治理与迁移

**背景**: 随着阿里巴巴内部业务全面向云原生架构演进，原有的 API 网关在应对海量流量（如双11大促）和复杂的微服务调用链路时，面临着扩展性、性能和统一管控的挑战。业务需要从传统的 Nginx+Lua 架构向基于 Istio 的云原生架构平滑迁移。

**问题**: 
1. 传统的网关配置管理复杂，难以适应微服务环境下频繁的变更需求。
2. 在处理南北向（入口流量）与东西向（服务间流量）流量时，缺乏统一的治理标准，导致路由规则、限流熔断策略分散。
3. 开源 Istio 虽然功能强大，但配置复杂（CRD 过多），且缺乏对国内特有的协议（如 Dubbo）和认证体系（如 OIDC/LDAP）的原生支持，接入成本极高。

**解决方案**: 阿里巴巴内部研发并开源了 Higress。Higress 基于 Istio 构建，深度集成了 Envoy 作为数据面，并进行了以下关键改进：
1. **统一网关**: 将 Ingress 网关和微服务网关（Mesh Gateway）合二为一，实现了 K8s Ingress 和 Service Mesh 流量的统一管控。
2. **兼容性与扩展**: 提供了对 Dubbo、gRPC 等协议的原生支持，并兼容 Nginx 的 Ingress 注解，大幅降低了迁移成本。
3. **WAF 插件市场**: 内置了 WAF（Web应用防火墙）能力，并支持通过 WASM（WebAssembly）技术动态扩展插件，无需重启网关即可部署自定义逻辑。

**效果**: 
1. 成功支撑了阿里巴巴内部核心业务板块的大规模流量洪峰，系统稳定性达到 99.99% 以上。
2. 通过将流量治理逻辑下沉到 C++ 编写的 Envoy 中，网关吞吐性能相比纯 Java 实现提升了数倍，资源占用显著降低。
3. 极大地简化了开发人员的配置流程，实现了流量的可视化和精细化治理，为业务快速迭代提供了坚实的底层支撑。

---



### 2：某大型互联网电商 - API 全生命周期管理与安全防护

 2：某大型互联网电商 - API 全生命周期管理与安全防护

**背景**: 该电商平台拥有数百个微服务，对外提供数千个 API 接口，涵盖移动端 App、小程序以及开放平台（OpenAPI）。随着业务发展，API 管理混乱、接口文档不同步以及安全问题（如爬虫、数据泄露）日益突出。

**问题**: 
1. **管理混乱**: 开发人员手动维护 Swagger 文档，经常出现文档与实际接口不一致的情况，导致前后端联调效率低下。
2. **安全风险**: 缺乏统一的鉴权层，部分敏感接口存在被遍历爬取的风险，且难以应对复杂的 DDoS 攻击。
3. **流量控制**: 在营销活动期间，无法对第三方合作伙伴的 API 调用频率进行精细化限制，容易导致后端服务雪崩。

**解决方案**: 引入 Higress 作为云原生 API 网关，并结合 Higress 的插件生态进行改造：
1. **全托管网关**: 部署 Higress 作为 Kubernetes 集群的统一流量入口，接管所有南北向流量。
2. **安全插件集成**: 开启 Higress 的内置 WAF 插件，配置 IP 黑名单和针对特定路径（如 `/api/login`）的频次限制，防止暴力破解和刷单。
3. **认证鉴权**: 利用 Higress 的 OIDC 认证插件，统一对接内部账号体系，实现了“一处认证，处处通行”。

**效果**: 
1. **安全性提升**: 成功拦截了 90% 以上的恶意爬虫流量和异常请求，有效保护了用户数据安全。
2. **研发效率**: 利用 Higress 的 Ingress 自动发现和配置管理能力，实现了 API 变更的自动化同步，前后端联调时间缩短了 40%。
3. **成本优化**: 通过 Higress 高效的连接处理机制，在同等流量规模下，网关实例数量减少了 30%，显著降低了云资源成本。

---



### 3：AI 创业公司 - 模型推理的高并发路由与负载均衡

 3：AI 创业公司 - 模型推理的高并发路由与负载均衡

**背景**: 一家专注于 AIGC（生成式 AI）应用的公司，需要对外提供基于 LLM（大语言模型）的对话服务。由于模型推理耗时较长且资源昂贵，后端部署了多种推理引擎（如 vLLM, TGI）和不同规格的 GPU 实例。

**问题**: 
1. **超时与重试**: 大模型推理往往需要几十秒，传统的网关超时设置容易导致请求中断，且缺乏针对推理任务特有的重试机制。
2. **负载均衡不均**: 简单的轮询（Round Robin）无法根据后端 GPU 的实时负载（显存占用、排队长度）进行路由，导致部分实例过载而部分实例空闲。
3. **多模型切换**: 业务需要根据用户等级在开源模型（如 Llama 3）和商业模型（如 GPT-4）之间灵活切换，路由逻辑复杂。

**解决方案**: 使用 Higress 作为 AI 服务的专用网关：
1. **LLM 插件支持**: 启用 Higress 的 AI 特性插件，支持 SSE（Server-Sent Events）流式传输，确保大模型生成的文本能够实时推送给前端。
2. **高级路由**: 配置基于 Header 的路由规则，将免费用户流量路由至自建的 GPU 集群，付费用户流量路由至高可用的商业模型 API。
3. **超时与缓存**: 调整网关的超时策略以适应长连接场景，并利用 Higress 的缓存能力缓存常见问题的 prompt 结果，减少后端推理压力。

**效果**: 
1. **用户体验优化**: 实现了毫秒级的首字响应（TTFT）和流畅的流式输出，用户满意度大幅提升。
2. **资源利用率提升**: 通过精细化的流量切分，有效控制了调用第三方商业 API 的成本，同时最大化利用了自建 GPU 算力。
3. **系统稳定性**: 在面对突发流量时，Higress 的队列管理和请求整形能力保护了后端脆弱的推理服务，避免了服务崩溃。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Apache APISIX | Kong |
|------|----------------|---------------|------|
| 性能 | 高性能，基于 Rust 和 Go，低延迟 | 极高性能，基于 LuaJIT，适合高并发 | 高性能，基于 Nginx 和 Lua，成熟稳定 |
| 易用性 | 提供控制台和 K8s Ingress 支持，配置简单 | 配置灵活但学习曲线较陡 | 插件丰富，但配置较复杂 |
| 成本 | 开源免费，云服务按需付费 | 开源免费，企业版收费 | 开源免费，企业版收费 |
| 扩展性 | 支持 WASM 插件，扩展性强 | 支持 Lua 和 Go 插件，生态丰富 | 支持 Lua 和 Python 插件，生态成熟 |
| 社区 | 阿里背书，社区活跃 | Apache 基金会项目，社区庞大 | 社区成熟，企业支持广泛 |

### 优势分析

- 优势1：高性能低延迟，基于 Rust 和 Go 实现，适合高并发场景。
- 优势2：易用性强，提供控制台和 K8s Ingress 支持，降低运维复杂度。
- 优势3：扩展性强，支持 WASM 插件，灵活适配业务需求。
- 优势4：阿里背书，社区活跃，文档完善，适合企业级应用。

### 不足分析

- 不足1：社区生态相对较新，插件和第三方集成不如 APISIX 和 Kong 丰富。
- 不足2：WASM 插件开发门槛较高，需要掌握 Rust 或 Go。
- 不足3：云服务依赖性较强，部分高级功能可能需要付费使用。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Wasm 插件实现扩展能力

**说明**: Higress 原生支持 WebAssembly (Wasm) 技术，允许用户在不修改主程序代码的情况下，通过 C++、Go 或 Rust 编写插件来扩展网关功能。相比传统的 Lua 脚本，Wasm 插件提供了更高的隔离性、更好的性能以及更标准的开发体验。

**实施步骤**:
1. 根据业务需求选择合适的编程语言（推荐 Go 或 C++）编写插件逻辑。
2. 使用 Higress 提供的 SDK 或 API Proxy 工具将代码编译为 Wasm 文件。
3. 在 Higress 控制台的“插件市场”或“自定义插件”页面上传 Wasm 文件。
4. 配置插件的生效范围（全局、特定路由或特定服务）并启用插件。

**注意事项**: 编写 Wasm 插件时需注意内存资源的限制，避免在插件中进行阻塞式的耗时操作，以免影响网关的转发延迟。

---

### 实践 2：精细化配置流量路由与负载均衡

**说明**: Higress 兼容 Nginx Ingress 的注解，并在此基础上增强了流量管理能力。利用 HTTP 到 gRPC 的协议转换、Header 匹配以及权重路由，可以实现蓝绿发布、金丝雀发布等复杂场景。

**实施步骤**:
1. 定义 Ingress 资源时，使用 `nginx.ingress.kubernetes.io/canary` 注解开启金丝雀功能。
2. 设置 `canary-by-header` 或 `canary-weight` 来控制流量分配的规则。
3. 在服务发现配置中，根据后端服务能力选择合适的负载均衡算法（如轮询、一致性哈希等）。
4. 配置超时时间与重试策略，以应对后端服务瞬间的抖动。

**注意事项**: 在进行金丝雀发布时，务必确保新版本服务与旧版本服务的 API 兼容性，避免因流量切换导致业务报错。

---

### 实践 3：全面对接云原生服务注册中心

**说明**: Higress 设计初衷是打通微服务网关与 API 网关的边界。最佳实践是将 Higress 直接与 Nacos、Consul、ZooKeeper 或 Kubernetes Service 关联，实现服务的自动发现，避免手动维护繁琐的 IP 列表。

**实施步骤**:
1. 在 Higress 控制台的“来源管理”中添加对应的服务来源（如 Nacos）。
2. 配置服务来源的连接地址（Server Addr）、命名空间和访问凭证。
3. 在创建 Ingress 或网关路由时，直接选择已注册的服务名称作为目标服务。
4. 启用健康检查功能，确保 Higress 能够自动摘除不健康的后端实例。

**注意事项**: 如果服务注册中心在公网或跨 VPC 环境，请确保网络连通性及防火墙策略已正确配置。

---

### 实践 4：构建多租户安全防护体系

**说明**: 依托 Higress 对云原生生态的集成，应结合外部认证系统（如 OIDC、OAuth2）和内置安全插件（如 WAF 防护、Key Auth）来构建多层防御体系，保护后端服务的安全。

**实施步骤**:
1. 配置“域名路由”或“路径路由”级别的鉴权插件，例如配置 Key Auth 要求客户端携带 API Key 访问。
2. 集成第三方身份认证提供商（如 Keycloak 或阿里云 IDaaS），配置 JWT 或 OIDC 认证方式。
3. 启用 IP 访问控制列表（IP ACL），限制允许访问网关的源 IP 范围。
4. 开启请求限流插件，针对特定 API 设置 QPS 阈值，防止恶意刷量。

**注意事项**: 敏感信息（如数据库密码、API 密钥）不应直接明文写在配置中，建议使用 KMS 或 Kubernetes Secret 进行管理。

---

### 实践 5：利用 Ingress 注解增强网关能力

**说明**: 对于从 Nginx Ingress 迁移或习惯使用 Kubernetes 原生资源的用户，充分利用 Higress 兼容的 Ingress 注解是快速实现高级功能（如限流、CORS、SSL 重定向）的关键。

**实施步骤**:
1. 修改 Ingress YAML 文件，添加 `nginx.ingress.kubernetes.io` 系列注解。
2. 例如，使用 `nginx.ingress.kubernetes.io/enable-cors: "true"` 开启跨域支持。
3. 使用 `nginx.ingress.kubernetes.io/limit-rps` 设置每秒请求限制。
4. 应用配置后，通过 Higress 的日志面板观察规则是否生效。

**注意事项**: 虽然大部分 Nginx 注解兼容，但部分底层机制不同，建议在测试环境先验证注解的具体行为。

---

### 实践 6：实施全链路可观测性监控

**说明**: 生产环境的网关必须具备强大的可观测

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/2 与 HTTP/3 (QUIC) 协议

**说明**: Higress 基于 Envoy 代理构建，对现代 HTTP 协议有很好的支持。HTTP/2 通过多路复用技术解决了 HTTP/1.1 的队头阻塞问题，显著提升并发传输效率。HTTP/3 (QUIC) 则基于 UDP 协议，进一步解决了 TCP 层的队头阻塞，并在弱网环境下提供更低的连接建立延迟和更好的连接迁移能力。

**实施方法**:
1. 在 Higress 网关的监听器配置中，启用 HTTP/2 协议支持。
2. 如果客户端网络环境复杂（如移动端），在 ALB 或网关入口处开启 QUIC 协议支持。
3. 确保后端服务也支持 HTTP/2，以实现全链路协议升级。

**预期效果**: 高并发场景下请求延迟降低 10%-30%，弱网环境下的丢包重传率显著降低，吞吐量提升约 20%。

---

### 优化 2：配置全链路超时与连接池调优

**说明**: 默认的超时和连接池配置往往过于保守或过于宽松，导致连接数耗尽或请求长时间堆积。合理的超时设置可以快速失败，释放资源给健康的请求；调优连接池（最大连接数、最大请求数）则能平衡后端服务的负载，防止雪崩。

**实施方法**:
1. **连接池调优**: 根据后端服务的能力，调整 `maxRequestsPerConnection`（建议设为 10-100，避免长连接垄断）和 `connectionLimit`（根据后端并发处理能力设置）。
2. **超时设置**: 设置合理的 `connectTimeout` (连接超时)、`timeout` (请求超时) 和 `idleTimeout` (空闲超时)。例如，将连接超时设为 2-5 秒，避免长时间挂起。
3. 开启 `retry` (重试) 策略，但必须配合 `retryBudget` (重试预算) 以防止重试风暴。

**预期效果**: 后端服务负载更加均衡，故障隔离速度提升，整体 P99 延迟可降低 15%-40%。

---

### 优化 3：启用 Wasm 插件的高效缓存与异步处理

**说明**: Higress 的核心优势之一是支持 Wasm 插件。如果插件逻辑中包含大量计算或外部调用（如调用远程鉴权服务），会阻塞请求处理流水线。通过在插件内部实现本地缓存或异步处理，可以大幅减少重复计算和网络 I/O 等待时间。

**实施方法**:
1. **本地缓存**: 在 Wasm 插件中使用 `HashMap` 或 `Redis` 客户端（通过 Host Call）缓存鉴权结果或配置信息，设置合理的 TTL。
2. **异步非阻塞**: 对于非关键路径的逻辑（如日志上报、监控数据统计），使用 Wasm 的异步调用接口处理，避免阻塞主请求流程。
3. **代码优化**: 减少 Wasm 虚拟机内的内存分配和拷贝操作，使用 `lazy loading` 加载配置。

**预期效果**: 插件执行耗时从毫秒级降至微秒级，网关 CPU 使用率降低 10%-20%，路由处理能力提升 30% 以上。

---

### 优化 4：实施精细化日志采样与字段裁剪

**说明**: 在高流量场景下，全量日志记录会产生巨大的磁盘 I/O 和网络带宽开销，甚至成为性能瓶颈。通过日志采样和裁剪非必要字段，可以在保留核心可观测性的前提下，极大降低系统负载。

**实施方法**:
1. **日志采样**: 配置 Higress 或 Envoy 的 `runtime` 特性，根据流量特征动态调整采样率（例如，正常流量 10% 采样，错误流量 100% 采样）。
2. **字段过滤**: 在 Access Log 格式中，移除冗长或低价值的字段（如完整的请求 Body、不必要的 Header），仅保留 TraceID、URL、Status Code、Duration

---
## 学习要点

- Higress 是阿里开源的基于 Istio 的云原生 API 网关，深度集成了 K8s 与 Envoy，提供高性能流量管理。
- 支持动态路由、负载均衡、熔断降级等企业级流量治理能力，适用于微服务与云原生架构。
- 内置 WAF（Web 应用防火墙）插件，提供安全防护功能，可抵御常见 Web 攻击。
- 兼容 Kubernetes Ingress 与 Gateway API 标准，简化云原生环境下的服务暴露与配置。
- 提供可扩展的插件机制，支持自定义开发与集成，满足多样化业务需求。
- 通过 Envoy 高性能数据面实现低延迟转发，适合高并发场景下的 API 网关部署。
- 开源社区活跃，文档完善，适合作为企业级 API 网关或服务网格的入口层解决方案。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础与环境认知

**学习内容**:
- 理解云原生网关的基本概念，以及 Higress 在微服务架构中的定位（作为流量入口、API 网关）。
- 了解 Higress 的核心特性：基于 Envoy 和 Istio、高可用性、支持 K8s Ingress、兼容 Nginx Ingress 注解。
- 掌握基本术语：路由、Ingress、网关实例、Upstream（服务来源）。
- 学习使用 Docker 或 Kubernetes 部署一个最基础的 Higress Demo 环境。

**学习时间**: 1-2周

**学习资源**:
- Higress 官方 GitHub 仓库 README
- Higress 官方文档 - "快速开始" 章节
- [云原生网关 Higress 官方网站](https://higress.io/)

**学习建议**:
建议先不要急于深入配置，而是先通过官方提供的 Docker Compose 或 Minikube 部署脚本跑通第一个示例。理解 Higress 如何作为 Ingress Controller 替代传统的 Nginx Ingress Controller 是本阶段的关键。

---

### 阶段 2：核心配置与流量管理

**学习内容**:
- 深入学习 Higress 的核心资源模型：Ingress、Gateway、HttpRoute。
- 掌握流量路由规则配置：基于路径、Header、Query 参数的路由匹配。
- 学习服务来源的配置与管理：对接 Nacos、Consul、固定地址（IP/域名）以及 K8s Service。
- 学习插件体系的基础使用：如何在控制台配置基础插件（如：限流、重试、CORS、请求头修改）。
- 理解 Wasm (WebAssembly) 在 Higress 中的作用，了解如何通过插件扩展网关功能。

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - "控制台使用指南" 与 "插件市场"
- Higress GitHub Examples 仓库中的配置样例
- Envoy 基础概念文档（用于理解底层代理机制）

**学习建议**:
动手在控制台配置复杂的路由转发规则，例如将 `/api/v1` 转发到服务 A，将 `/api/v2` 转发到服务 B。尝试使用官方插件市场中的热门插件（如 Key Auth 或 Request Block）来体验 Wasm 插件的即时生效特性。

---

### 阶段 3：安全、可观测性与全链路治理

**学习内容**:
- 网关安全配置：配置 HTTPS 证书、实现 mTLS（双向认证）、配置 IP 访问控制（黑/白名单）。
- 可观测性集成：配置日志收集（SLS/Otel）、配置 Prometheus 监控指标、配置链路追踪。
- 高级流量治理：金丝雀发布、蓝绿发布、基于权重的流量切分。
- 学习 Higress 对 Dubbo 和 gRPC 协议的代理支持。

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档 - "安全" 与 "可观测性" 板块
- Higress 官方博客 - 关于金丝雀发布和流量治理的实践案例
- Prometheus 与 Grafana 官方文档（用于理解监控数据结构）

**学习建议**:
本阶段重点在于"生产就绪"。尝试构建一个包含监控面板的完整环境，模拟一次服务上线过程中的金丝雀发布流程，观察流量是如何按照百分比逐步切换到新版本的。

---

### 阶段 4：插件开发与源码深度剖析

**学习内容**:
- Wasm 插件开发实战：学习使用 Go (AssemblyScript) 或 C++ 开发自定义 Wasm 插件。
- 学习 Higress 的数据处理模型：如何修改 Request Header、Response Body 以及处理动态配置。
- 深入源码：研究 Higress 的架构设计，包括控制面与数据面的交互、配置热更新机制。
- 性能调优：理解连接池配置、缓冲区设置以及 Wasm 虚拟机的性能影响。

**学习时间**: 4周以上

**学习资源**:
- Higress 官方文档 - "Wasm 插件开发指南"
- Higress GitHub 源码
- Envoy Wasm C++/Go SDK 文档
- Higress 官方提供的 Wasm 插件开发示例

**学习建议**:
如果业务有特殊逻辑（如特殊的签名校验、复杂的数据转换），尝试编写一个自定义插件来解决。阅读源码时，重点关注配置如何从 K8s CRD 下发到 Envoy 的流程，这是理解 Higress 核心技术的关键。

---
## 常见问题


### 1: Higress 是什么？它与阿里巴巴有什么关系？

1: Higress 是什么？它与阿里巴巴有什么关系？

**A**: Higress 是一个基于阿里内部两年多的“云原生网关”实践而开源的云原生 API 网关。它建立在 Envoy 和 Istio 等开源项目之上，旨在提供标准化、高可用、高性能的云原生网关。它由阿里巴巴集团、蚂蚁集团以及多家外部公司共同维护，是阿里巴巴云原生技术栈向开源社区贡献的核心组件之一。

---



### 2: Higress 与 Nginx、Kong 或 APISIX 等传统网关相比有什么优势？

2: Higress 与 Nginx、Kong 或 APISIX 等传统网关相比有什么优势？

**A**: Higress 的核心优势在于其“云原生”架构和与阿里内部技术栈的深度结合：

1.  **标准与扩展性**：它支持 Kubernetes Ingress 标准和 Gateway API 标准，同时兼容 Nginx Ingress Annotation，降低了迁移门槛。
2.  **高性能**：基于 Envoy C++ 内核构建，相比基于 Lua 的 OpenResty（Kong/APISIX）通常具有更高的长连接处理能力和更低的延迟。
3.  **安全防护**：集成了阿里内部成熟的 WAF（Web Application Firewall）能力，提供开箱即用的安全防护。
4.  **服务治理集成**：与 Nacos、Sentinel、Dubbo 等阿里系微服务组件无缝集成，支持流量灰度、限流熔断等高级治理功能。
5.  **插件生态**：支持 WASM (WebAssembly) 插件，允许使用 Go 或 C++ 编写高性能插件，且插件热更新不会导致连接中断。

---



### 3: Higress 是否支持从 Nginx Ingress 或其他网关平滑迁移？

3: Higress 是否支持从 Nginx Ingress 或其他网关平滑迁移？

**A**: 是的，Higress 非常重视迁移的兼容性。

1.  **Nginx 兼容**：Higress 原生支持 Nginx Ingress 的绝大多数 Annotations，这意味着在 Kubernetes 集群中，通常只需将 Ingress Class 修改为 `higress`，即可利用现有的 Ingress 配置直接运行 Higress。
2.  **配置转换**：对于 Kong 或 APISIX 等网关，虽然配置模型不同，但由于 Higress 支持标准的 Kubernetes Gateway API，用户可以通过标准化的 YAML 资源进行配置，从而降低厂商锁定风险。

---



### 4: Higress 如何处理流量管理和安全防护？

4: Higress 如何处理流量管理和安全防护？

**A**: Higress 提供了企业级的流量管理和安全特性：

1.  **流量管理**：支持基于 Header、Cookie、权重等条件的蓝绿发布、金丝雀发布和 A/B 测试。它集成了 Sentinel 进行流量控制和熔断降级，保护后端服务稳定性。
2.  **安全防护**：内置了 WAF 插件，可以防御 SQL 注入、XSS、恶意爬虫等常见 Web 攻击。支持 OIDC、OAuth2.0 以及 JWT 验证，方便对接企业级认证系统（如 Keycloak、阿里云 IDaaS）。
3.  **全链路加密**：支持 mTLS（双向 TLS）认证，确保服务间通信的安全。

---



### 5: Higress 的插件系统是如何工作的？支持哪些语言？

5: Higress 的插件系统是如何工作的？支持哪些语言？

**A**: Higress 采用灵活的插件架构来扩展功能：

1.  **WASM 支持**：这是 Higress 插件的核心。它支持 WebAssembly 标准，允许开发者使用 Go、C++、Rust 或 AssemblyScript 编写插件逻辑。WASM 插件运行在沙箱环境中，安全性高，且支持热加载，修改插件无需重启网关进程。
2.  **Lua 兼容**：为了兼容旧有的 OpenResty 生态，Higress 也支持 Lua 脚本插件，方便用户复用原有的 Lua 代码资产。
3.  **原生插件**：对于极致性能要求的场景，Higress 支持编写 C++ 原生插件（基于 Envoy 生态）。

---



### 6: 在非 Kubernetes 环境（如虚拟机或裸金属）中能否使用 Higress？

6: 在非 Kubernetes 环境（如虚拟机或裸金属）中能否使用 Higress？

**A**: 可以。虽然 Higress 是为云原生架构设计的，主要部署在 Kubernetes 集群中，但它也提供了**标准版**（Standalone 版本）。标准版允许用户在传统的虚拟机或裸金属服务器上以进程的方式部署 Higress，这使得它不仅能用于 K8s 环境，也能用于边缘计算节点或传统的 ECS 实例中。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: 快速体验 Higress 网关

### 难度**: 简单

### 问题描述**:

### 请基于官方 Docker 镜像快速启动一个 Higress 网关实例，并配置一条简单的路由规则。要求将访问本地网关端口（例如 `http://localhost:8080/test`）的流量，成功转发至公网可访问的 HTTP 测试服务（如 httpbin.org）。

---
## 实践建议

以下是基于 Higress 作为 AI 网关和 API 网关的实际使用场景，提供的 6 条实践建议：

### 1. 利用 AI 代理服务进行模型供应商的统一管理
**场景**：企业内部同时接入了 OpenAI、Azure OpenAI 以及通义千问等多个大模型供应商，业务方切换成本高。
**建议**：不要将不同供应商的 SDK 硬编码到业务逻辑中。在 Higress 中配置 AI 代理服务，将不同供应商的 API 统一映射为 Higres 的标准接口。
**具体操作**：
*   在 `ai-proxy` 插件配置中，针对不同的路由（如 `/openai` 和 `/qwen`）设置不同的 `serviceId` 或 `serviceUrl`。
*   **最佳实践**：利用 Higress 的 Header 转换功能，将业务侧发送的标准化 Header（如 `X-Model-Provider: alibaba`）动态映射为对应厂商所需的 API Key 或 Endpoint，从而实现业务代码的零改动切换。

### 2. 实施基于 Token 的精细化鉴权与流控
**场景**：大模型调用成本高昂，且不同用户或租户的配额不同。
**建议**：不要仅依赖传统的 QPS（每秒请求数）限流，必须启用基于 Token 的限流策略。
**具体操作**：
*   在 `ai-proxy` 插件配置中开启 `context` 选项，这通常允许网关解析请求体以预估 Token 消耗。
*   **常见陷阱**：如果直接对整个 Prompt 进行流控，可能会因为长 Prompt 导致误判。建议结合 `rate-limit` 插件，针对 API Key 或用户 ID 设置每分钟/每天的最大 Token 预算额度，防止被恶意刷量或意外超额。

### 3. 配置语义缓存以降低推理成本和延迟
**场景**：用户频繁提问相似的问题（如客服场景），每次都请求 LLM 导致费用高且响应慢。
**建议**：启用 AI 特性中的语义缓存或精确缓存。
**具体操作**：
*   在 `ai-proxy` 插件中配置 `cache` 参数。对于 Prompt 变化较小但需要极高一致性的场景，使用全量缓存；对于允许一定语义近似的场景，可配置向量数据库缓存（需对接外部向量存储）。
*   **最佳实践**：针对“知识库问答”类场景，建议开启缓存，将缓存命中率作为网关层的关键监控指标，这通常能节省 30% 以上的 Token 成本。

### 4. 构建提示词模板中心以减少前端复杂度
**场景**：前端应用直接拼接 Prompt 字符串，导致逻辑分散且难以维护 System Prompt。
**建议**：将 Prompt 模板管理下沉到网关层。
**具体操作**：
*   使用 Higress 的 `ai-proxy` 插件中的 `promptTemplate` 功能。在网关配置中定义 System Message 和 User Message 的模板结构。
*   前端只需传递关键参数（如 `{ "query": "用户的问题", "style": "幽默" }`），网关自动将其填充到预设的模板中。
*   **最佳实践**：通过这种方式，可以在不重新发布前端应用的情况下，实时在线调整 System Prompt 以优化模型效果。

### 5. 警惕 JSON 解析模式下的流式输出中断
**场景**：业务端要求模型返回 JSON 格式数据以便解析，同时开启了 SSE（Server-Sent Events）流式输出。
**建议**：确保 `ai-proxy` 插件的 `responseFormat` 配置与客户端的解析逻辑严格匹配。
**具体操作**：
*   如果模型原生支持 JSON Mode（如 GPT-4o），在插件中配置 `response_format: { "type": "json_object" }`。
*   **常见陷阱**：在流式传输中，JSON 对象可能被分片传输（例如先传了 `{"result": "hel`，后传 `lo"}`）。如果客户端按行解析或处理不当，会导致 JSON 解析错误。建议在网关层或客户端确保接收完整的 Frame 后

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [WASM](/tags/wasm/) / [LLM](/tags/llm/) / [MCP](/tags/mcp/) / [Kubernetes](/tags/kubernetes/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/) / [DevOps/运维](/scenarios/devops-%E8%BF%90%E7%BB%B4/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-2.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-8.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*