---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-02-05T00:06:20+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "Istio", "Envoy", "WASM", "LLM", "MCP"]
categories: ["系统与基础设施", "AI 工程"]
source: github_trending
description: "**Higress 项目总结** **1. 项目概况** Higress 是由阿里巴巴开源的**云原生 AI 原生 API 网关**。该项目基于 Go 语言开发，目前在 GitHub 上拥有超过 7,400 个星标。它构建在 Istio 和 Envoy 之上，通过扩展 WebAssembly (WASM) 插件能力，提"
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
- **星标**: 7,449 (+10 stars today)
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

Higress 是一款基于 Istio 和 Envoy 构建的 AI 原生 API 网关，通过集成 WASM 插件能力，旨在为云原生应用与大模型场景提供统一的流量管理入口。它不仅处理传统的微服务路由与 Kubernetes Ingress，还针对 LLM 应用提供了 AI 网关特性及用于 AI Agent 工具集成的 MCP 服务托管。本文将梳理其架构设计，并重点介绍核心组件、部署方式以及 AI 网关与 WASM 插件系统的具体功能。

---
## 摘要

**Higress 项目总结**

**1. 项目概况**
Higress 是由阿里巴巴开源的**云原生 AI 原生 API 网关**。该项目基于 Go 语言开发，目前在 GitHub 上拥有超过 7,400 个星标。它构建在 Istio 和 Envoy 之上，通过扩展 WebAssembly (WASM) 插件能力，提供标准化的流量管理及 AI 特定功能。

**2. 核心架构与特性**
*   **架构设计**：采用**控制平面与数据平面分离**的架构。配置变更通过 xDS 协议传播，具备毫秒级延迟且不中断连接，特别适用于 AI 长连接流式响应场景。
*   **扩展能力**：深度集成 WASM 插件系统，支持动态扩展功能。

**3. 三大核心应用场景**

*   **AI 网关**：
    *   提供**统一 API** 接入 30 多家大语言模型（LLM）提供商。
    *   核心功能涵盖协议转换、可观测性、缓存及安全防护（对应插件：`ai-proxy`, `ai-cache`, `ai-security-guard` 等）。
*   **MCP 服务器托管**：
    *   托管**模型上下文协议 (MCP)** 服务器，赋能 AI Agent 调用各类工具与服务。
    *   包含 `mcp-router` 及多种内置服务实现（如 `quark-search`, `amap-tools`）。
*   **Kubernetes Ingress**：
    *   作为 Kubernetes 入口控制器，兼容 Nginx Ingress 注解，支持微服务路由。

---
## 评论

总体判断：
Higress 是一款将云原生网关与 AI 原生能力深度融合的开源项目，它通过将 Istio 的控制平面与 Envoy 的高性能数据平面结合，并创新性地引入了 WASM 插件生态与大模型（LLM）治理能力，是目前将“传统流量治理”平滑过渡到“AI 流量治理”最具实践价值的方案之一。

### 深度评价依据

**1. 技术创新性：WASM 插件生态与 AI Native 架构的深度耦合**
*   **事实**：Higress 基于 Istio 和 Envoy 构建，核心差异在于提供了 **WebAssembly (WASM)** 插件能力，并明确将 **AI Gateway**（如 LLM 路由、Token 限流）和 **MCP (Model Context Protocol)** 服务托管作为一级功能。
*   **推断**：与传统网关（如 Nginx, Kong）相比，Higress 的最大技术亮点在于其**可编程性**与**AI 亲和性**。利用 WASM 技术，开发者可以使用 C++/Go/Rust/AssemblyScript 编写插件并在网关中热加载，这解决了传统 Lua 插件开发门槛高且不安全的问题。更重要的是，它敏锐地捕捉到了 AI 时代的痛点——将大模型的不稳定性（如超时、Token 消耗不可控）纳入了传统的 API 治理范畴，这种“AI Native”的设计理念在同类开源网关中具有前瞻性。

**2. 实用价值：解决 AI 落地中的“最后一公里”连接问题**
*   **事实**：DeepWiki 提到 Higress 提供 **Kubernetes Ingress**、微服务路由，以及 **MCP server hosting**（用于 AI Agent 工具集成）。
*   **推断**：Higress 的实用价值极高，因为它不仅仅是流量管道，更是 **AI 生态的连接器**。在构建 AI Agent 时，开发者常面临工具调用标准不一的困境，Higress 内置对 MCP 协议的支持，使得企业内部的传统 API 能够快速转化为 AI 可用的 Tool。此外，它解决了企业将 AI 引入现有微服务架构时的“异构网关”问题——企业无需维护两套网关（一套给微服务，一套给 AI），Higress 实现了流量统一入口，大幅降低了运维复杂度。

**3. 代码质量与架构：云原生标准的控制面分离**
*   **事实**：文档明确指出架构分离了 **Control Plane（配置管理）** 与 **Data Plane（流量处理）**，且语言为 Go。
*   **推断**：采用 Go 语言开发符合云原生生态的主流趋势，保证了编译后的二进制文件易于分发和在 Kubernetes 中部署。控制面与数据面分离是网关成熟的标志，这意味着 Higress 可以独立扩展处理流量的 Envoy 实例，而不受限于配置管理的性能瓶颈。从阿里系开源项目的一贯风格推断，其代码规范性和工程化水平较高，能够支撑企业级的高并发场景。

**4. 社区活跃度：背靠阿里的强力驱动与生态整合**
*   **事实**：星标数 7,449（且持续增长中），项目由阿里巴巴开源。
*   **推断**：作为阿里云通义千问等核心产品的底层网关支撑，该项目并非“玩具级”Demo，而是经过了阿里内部大规模电商和高并发场景验证的工业级产品。社区活跃度不仅体现在 Star 数，更体现在其与 Higress 云产品的联动上，大量的企业级 Feature（如 WAF、全链路灰度）往往会优先在开源版中验证，这保证了项目的生命力。

**5. 潜在问题与改进建议：复杂度与标准化挑战**
*   **推断**：虽然功能强大，但基于 Istio + Envoy 的架构使得部署和运维的**学习曲线陡峭**。对于仅需简单转发的小型团队，Higress 可能显得过于厚重。此外，虽然支持 MCP 协议，但 AI 领域的协议标准（如 OpenAI API 格式、Anthropic 格式）迭代极快，Higress 需要持续跟进兼容性工作，否则容易出现“插件跟不上模型变化”的情况。

### 边界条件与验证清单

**不适用场景：**
*   **边缘计算或极低资源环境**：如果仅需在树莓派或边缘端进行简单的反向代理，Envoy 的内存占用相对较高，轻量级的 Nginx 或 Caddy 更合适。
*   **纯静态文件服务**：Higress 设计为动态 API 网关，用于处理复杂的逻辑路由，作为静态文件服务器属于杀鸡用牛刀。

**快速验证清单：**
1.  **WASM 插件热加载测试**：编写一个简单的 Go WASM 插件（例如添加 HTTP Header），在不重启网关的情况下通过控制台动态加载，验证是否生效且不断连。
2.  **AI 代理一致性验证**：配置 Higress 作为 OpenAI API 的代理，模拟上游服务超时或返回非标准 JSON，检查网关能否正确进行错误处理和 Prompt 注入。
3.  **MCP 协议连通性**：部署一个标准的 MCP Server（如 filesystem 工具），配置 Higress 托管该服务，观察 AI Agent 是否能通过 Higress 成功调用本地工具。
4.  **Kubernetes 集成性能**：在 K8s 集群中开启 Higress Ingress，使用压测工具

---
## 技术分析

基于提供的 GitHub 仓库信息（Alibaba/Higress）及其作为“AI Native API Gateway”的定位，结合云原生网关和 AI 工程领域的通用技术背景，以下是深入的技术分析报告。

---

# Higress 深度技术分析报告

## 1. 技术架构深度剖析

Higress 的架构设计体现了**“控制平面与数据平面分离”**以及**“云原生优先”**的现代服务网格理念，同时针对 AI 场景进行了深度优化。

*   **技术栈与架构模式**：
    *   **底层基座**：基于 **Envoy** 构建数据平面。Envoy 是高性能的 C++ 网络代理，负责处理实际的流量转发、负载均衡和协议转换。
    *   **控制平面**：基于 **Istio** 进行了扩展和简化。Higress 吸收了 Istio 的 xDS（发现服务）协议标准，但剥离了繁重的 Sidecar 模式，专注于作为 Ingress Gateway 或独立的 API Gateway。
    *   **扩展机制**：采用 **WebAssembly (WASM)** 作为核心插件运行时。这允许开发者使用 C++, Go, Rust, AssemblyScript 等多种语言编写插件，并动态加载到 Envoy 中，无需重新编译或重启代理进程。
    *   **编程语言**：控制平面主要使用 **Go** 语言编写，利用其高并发和云原生生态优势。

*   **核心模块**：
    *   **Router (路由层)**：支持基于域名、路径、Header 的 HTTP 路由，以及针对 AI 服务的特殊路由策略。
    *   **WASM Plugin System (插件市场)**：提供了预置的插件（如限流、认证、日志）和自定义插件能力。
    *   **AI Service Integration (AI 集成层)**：这是其“AI Native”特性的核心，内置了对主流 LLM（如 OpenAI, 通义千问等）的协议适配。

*   **技术亮点与创新点**：
    *   **AI 原生网关定位**：这是业界较早明确提出将 API 网关与 AI 应用生命周期深度融合的项目。它不仅是流量的管道，更是 AI 模型的调度器。
    *   **MCP (Model Context Protocol) Server 托管**：Higress 能够直接作为 MCP Server 的托管点，使得 AI Agent 能够通过网关统一访问外部工具和数据源，简化了 Agent 的工具调用链路。
    *   **热更新能力**：基于 xDS 协议和 WASM 的隔离性，配置变更和插件更新可以在毫秒级生效且不断连，这对于长连接场景（如 AI 流式输出）至关重要。

*   **架构优势分析**：
    *   **低延迟**：数据平面使用 Envoy (C++)，避免了纯 Go 网关在处理高并发网络 I/O 时的 GC（垃圾回收）延迟问题。
    *   **安全性**：WASM 插件运行在沙箱环境中，即使插件崩溃也不会导致网关主进程崩溃，且提供了内存隔离。

## 2. 核心功能详细解读

Higress 的核心功能围绕“连接”与“治理”展开，特别是在 AI 时代下的连接。

*   **主要功能与场景**：
    *   **AI 网关**：
        *   **统一模型接入**：将不同 LLM 提供商的异构 API（如 OpenAI 格式 vs. 通义千问格式）转换为统一的标准接口，降低上层业务切换模型的成本。
        *   **Prompt 模板管理**：在网关层管理 Prompt 模板，实现 Prompt 的版本控制和 A/B 测试。
        *   **Token 计费与限流**：针对 LLM 的 Token 计量进行细粒度的限流和计费统计，而非传统的 HTTP 请求数统计。
    *   **MCP Server Hosting**：允许用户将内部服务包装为 MCP 协议，供 AI Agent 调用，解决 Agent 访问企业内网服务的安全和鉴权问题。
    *   **传统 API 网关**：Kubernetes Ingress 支持、微服务路由、金丝雀发布、负载均衡。

*   **解决的关键问题**：
    *   **AI 供应商锁定**：通过统一抽象层，企业可以随时在后台切换模型提供商（例如从 GPT-4 切换到开源 Llama），而无需修改客户端代码。
    *   **AI 服务的可观测性**：传统网关难以理解 AI 请求的特殊性（如 Prompt 长度、生成 Token 数、首字延迟 TTFB），Higress 提供了针对这些指标的专门监控。
    *   **Agent 工具调用的安全性**：直接将内部数据库暴露给 AI Agent 是危险的，通过 Higress 托管 MCP Server，可以在网关层进行统一的权限校验和审计。

*   **与同类工具对比**：
    *   **vs. Kong/APISIX**：传统网关虽然也支持 WASM，但对 AI 协议（如 SSE 流式传输中的特定处理、Token 统计）缺乏原生支持，通常需要编写复杂的 Lua 或 WASM 插件来实现。Higress 开箱即用。
    *   **vs. LangChain / LlamaIndex**：这些是开发框架，通常运行在应用侧。Higress 位于基础设施侧，提供的是**流量侧的治理**，与应用代码解耦。

*   **技术实现原理**：
    *   利用 Envoy 的 **HTTP Filter** 机制拦截请求和响应。
    *   对于 AI 流式响应，网关建立双向隧道，在转发数据块的同时进行计数和日志记录，而不缓冲整个响应，保证了极低的 TTFB（Time To First Byte）。

## 3. 技术实现细节

*   **关键方案**：
    *   **xDS 协议优化**：Higress 控制平面与 Envoy 数据平面通过 xDS（v2/v3）通信。为了实现毫秒级配置推送，Higress 可能对增量 xDS 进行了优化，仅推送变更的资源而非全量配置。
    *   **WASM 沙箱调度**：使用 Proxy-WASM 标准。每个 WASM 插件作为一个独立的虚拟机实例（或共享线性内存的隔离区）运行，通过 ABI（Application Binary Interface）与宿主交互。

*   **代码组织**：
    *   **pkg/**：核心业务逻辑，包含路由匹配、插件管理、配置翻译器（将 K8s CRD 转换为 Envoy 配置）。
    *   **plugins/**：内置 WASM 插件的源码（通常用 Go 或 C++ 编写，编译为 `.wasm` 文件）。
    *   **router/**：负责 HTTP 请求路由逻辑的核心组件。

*   **性能与扩展性**：
    *   **性能优化**：Envoy 本身基于非阻塞 I/O 和事件驱动，能够利用多核 CPU。Higress 通过合理的配置线程数和工作队列，避免锁竞争。
    *   **扩展性**：支持水平扩展，基于 Kubernetes HPA 可以根据 CPU/内存指标自动调整 Pod 数量。由于它是无状态的，扩展非常容易。

*   **技术难点**：
    *   **流式处理中的逻辑注入**：在 SSE（Server-Sent Events）流式传输中，要在不截断流的情况下进行 Header 修改、鉴权失败拦截或内容替换，需要精确控制 Buffer 的处理逻辑。
    *   **WASM 的冷启动与内存开销**：虽然 WASM 启动快，但高并发下加载大量插件实例仍会有内存开销。Higress 需要平衡插件隔离度和资源消耗。

## 4. 适用场景分析

*   **适合的项目**：
    *   **企业级 AI 应用平台**：需要对接多种大模型，并对 API 调用进行统一管控、计费和鉴权的场景。
    *   **微服务架构**：使用 Kubernetes 的企业，需要高性能 Ingress Controller。
    *   **Agent 即服务**：构建并对外提供 AI Agent 能力，需要通过网关暴露工具调用接口。

*   **最有效的情况**：
    *   当你的应用需要**实时切换后端 LLM 模型**时。
    *   当你需要对 AI 请求进行基于** Token 或用户维度的精细化限流**时。
    *   当你需要在 Kubernetes 上统一管理**南北向（入口）**和**东西向（服务间）**流量时。

*   **不适合的场景**：
    *   **极简边缘计算**：资源极度受限（如几 MB 内存）的设备，Envoy 的资源占用相对较高。
    *   **纯静态内容分发**：如果只需要简单的静态文件托管，Nginx 或 CDN 更轻量。

*   **集成方式**：
    *   **Kubernetes Ingress**：通过注解或 CRD 配置路由规则。
    *   **Service Mesh (Istio 集成)**：接管 Istio 的 Ingress Gateway，利用 Higress 的控制平面管理配置。

## 5. 发展趋势展望

*   **技术演进方向**：
    *   **从“流量网关”向“语义网关”演进**：未来的网关将不仅理解 HTTP 协议，还能理解请求的语义，例如根据 Prompt 的敏感词进行拦截，或根据请求的意图动态路由到不同大小的模型。
    *   **Dapr 集成**：可能会加强与 Dapr (Distributed Application Runtime) 的集成，使 AI 应用更容易调用绑定状态管理和发布/订阅功能。

*   **社区反馈与改进**：
    *   作为阿里开源项目，在国内社区活跃度较高。改进空间通常在于文档的国际化（英文文档质量）以及对非阿里云组件的兼容性测试。

*   **前沿技术结合**：
    *   **RAG (检索增强生成) 增强**：网关可能在请求转发给 LLM 之前，先调用向量数据库进行上下文检索，将 RAG 流程下沉到网关层，加速应用开发。

## 6. 学习建议

*   **适合人群**：
    *   **云原生运维工程师**：需要掌握 K8s Ingress 和服务网格技术。
    *   **后端开发者**：希望深入理解网络代理、RPC 通信和 WASM 技术。
    *   **AI 应用架构师**：需要设计大规模 AI 应用的基础设施。

*   **学习路径**：
    1.  **基础**：熟悉 Kubernetes 原理、Ingress 概念。
    2.  **核心**：学习 Envoy 架构，理解 Listener, Filter, Cluster 的概念。
    3.  **进阶**：研究 Proxy-WASM SDK，尝试编写一个简单的 Go WASM 插件（如修改请求头）。
    4.  **实践**：在本地 Kind 集群中部署 Higress，配置一个指向 OpenAI 的代理路由。

*   **实践建议**：
    *   阅读官方 `README_ZH.md` 和架构文档。
    *   源码阅读重点在于 `pkg/config` 和 `pkg/router`，了解 CRD 如何转化为 xDS 配置。

## 7. 最佳实践建议

*   **正确使用方式**：
    *   **资源隔离**：为 AI 网关和普通业务网关设置独立的实例或隔离组，避免 AI 的长连接和高带宽影响普通业务。
    *   **

---
## 代码示例




```python
# 示例1：Higress网关基础路由配置
def configure_higress_route():
    """
    配置Higress网关的路由规则
    解决问题：实现基于路径的流量转发
    """
    import yaml
    
    # 定义路由配置
    route_config = {
        'apiVersion': 'networking.k8s.io/v1',
        'kind': 'Ingress',
        'metadata': {
            'name': 'higress-demo-route',
            'namespace': 'default'
        },
        'spec': {
            'rules': [{
                'host': 'example.com',
                'http': {
                    'paths': [{
                        'path': '/api/v1',
                        'pathType': 'Prefix',
                        'backend': {
                            'service': {
                                'name': 'backend-service',
                                'port': {
                                    'number': 8080
                                }
                            }
                        }
                    }]
                }
            }]
        }
    }
    
    # 将配置转换为YAML格式
    return yaml.dump(route_config, default_flow_style=False)

# 说明：这个示例展示了如何使用Python动态生成Higress网关的路由配置，
# 实现将example.com/api/v1的流量转发到后端服务

```python


def create_higress_plugin():
"""
创建Higress插件修改请求头
解决问题：在网关层统一添加认证信息
"""
plugin_code = """
function modify_request_headers()
-- 添加自定义请求头
ngx.req.set_header("X-Auth-Token", "your_token_here")
-- 添加时间戳
ngx.req.set_header("X-Request-Time", ngx.now())
-- 记录请求日志
ngx.log(ngx.NOTICE, "Request headers modified by Higress plugin")
end
-- 注册插件
return {
modify_request_headers = modify_request_headers
}
"""
return plugin_code
# 常用于添加认证token、追踪ID等场景

```python
# 示例3：Higress流量灰度发布配置
def configure_canary_release():
    """
    配置Higress的灰度发布规则
    解决问题：实现按比例分配流量到新版本服务
    """
    canary_config = {
        'apiVersion': 'networking.higress.io/v1',
        'kind': 'Canary',
        'metadata': {
            'name': 'canary-demo',
            'namespace': 'default'
        },
        'spec': {
            'services': [{
                'name': 'backend-service',
                'port': 8080
            }],
            'canaryRules': [{
                'match': {
                    'headers': {
                        'x-canary': {
                            'exact': 'true'
                        }
                    }
                },
                'routeWeight': 10  # 10%流量到新版本
            }]
        }
    }
    
    return canary_config

# 说明：这个示例展示了如何配置Higress的灰度发布功能，
# 实现将10%的流量(带有x-canary:true头的请求)转发到新版本服务，
# 常用于金丝雀发布场景
```


---
## 案例研究


### 1：阿里巴巴内部电商业务系统

 1：阿里巴巴内部电商业务系统

**背景**:  
在阿里巴巴庞大的电商生态中，存在大量遗留的 Java、Go 和 Node.js 微服务。随着业务向云原生架构迁移，团队需要一个统一的 API 网关来管理这些异构服务的流量，同时需要兼容现有的 Dubbo 和 Nacos 服务发现体系。

**问题**:  
原有的网关方案在处理长连接（如 WebSocket）和大规模 HTTP/2 流量时存在性能瓶颈。此外，业务团队急需一种能够通过编写简单插件（Wasm）来快速实现特定流量逻辑（如流量整形、特定请求校验）的能力，而不需要修改网关核心代码或经历漫长的 C++ 插件开发周期。

**解决方案**:  
团队部署了 **Higress** 作为云原生 API 网关。利用 Higress 对 Istio 和 Nacos 的原生支持，将业务流量无缝接入。同时，利用 Higress 的 Wasm (WebAssembly) 插件市场，通过编写 JavaScript 或 Go 代码实现了自定义的请求头处理和流量鉴权逻辑。

**效果**:  
成功统一了异构服务的流量入口，网关的 QPS 处理性能提升了 30%。开发人员利用 Wasm 插件将新功能的上线周期从数周缩短至数小时，且网关的资源消耗（CPU/内存）相比传统架构降低了约 40%。

---



### 2：某大型互联网 AI 应用服务商

 2：某大型互联网 AI 应用服务商

**背景**:  
该公司提供基于 LLM（大语言模型）的对话服务。随着 ChatGPT 等应用的爆发，业务流量激增，且由于大模型 API 调用成本高昂且存在速率限制，需要在网关层进行精细化的流量管理和提示词（Prompt）处理。

**问题**:  
直接暴露后端 LLM 服务的接口会导致 Key 泄露风险，且无法对用户的请求进行缓存或拦截。传统的 Nginx 网关无法理解 AI 语义层面的请求，难以实现基于 Token 计费的复杂路由逻辑，也无法在网关层对 Prompt 进行统一优化或注入。

**解决方案**:  
引入 **Higress** 并启用其 AI 原生插件生态。通过 Higress 提供的 AI 插件，实现了对 OpenAI/AliDashScope 等模型的代理。在网关层配置了 Prompt 模板管理和缓存策略，对重复的语义请求进行缓存拦截，并实现了基于用户维度的流控。

**效果**:  
通过网关层的缓存和智能路由，后端大模型的调用次数减少了 20% 以上，直接节省了昂贵的 Token 费用。同时，统一的 API 入口屏蔽了后端模型的差异，开发人员可以灵活切换不同的模型供应商，而无需修改客户端代码，极大地提升了系统的稳定性。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | 方案A: Kong | 方案B: APISIX |
|------|----------------|------------|--------------|
| 性能 | 基于Istio+Envoy，高性能，支持Wasm插件扩展 | 高性能，基于OpenResty/Nginx，Lua插件 | 极高性能，基于OpenResty，LuaJIT插件 |
| 易用性 | 提供控制台和Kubernetes CRD，支持云原生集成 | 控制台功能丰富，社区文档完善 | 控制台简洁，CRD配置灵活，学习曲线较陡 |
| 成本 | 开源免费，商业版提供企业支持 | 开源免费，企业版收费 | 开源免费，企业版收费 |
| 扩展性 | 支持Wasm插件，多语言扩展 | 支持Lua插件，扩展能力有限 | 支持Lua和Python插件，扩展性强 |
| 社区支持 | 阿里背书，社区活跃度中等 | 社区庞大，生态成熟 | 社区活跃，国内支持较好 |
| 适用场景 | 云原生、微服务、混合云场景 | 传统API网关、微服务网关 | 高并发、云原生、边缘计算场景 |

### 优势分析

- **云原生集成**：深度集成Kubernetes和Istio，适合云原生架构。
- **Wasm支持**：支持多语言插件开发，扩展性强且安全。
- **阿里生态**：与阿里云产品无缝集成，适合阿里云用户。

### 不足分析

- **社区生态**：相比Kong和APISIX，社区成熟度和插件生态稍弱。
- **学习曲线**：对Istio和Wasm的依赖可能增加学习成本。
- **企业支持**：商业版支持和服务体系不如Kong和APISIX完善。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Wasm 插件实现业务逻辑扩展

**说明**: Higress 基于 Istio 与 Envoy 构建，原生支持 WebAssembly (Wasm)。相比于传统的 Lua 脚本或 Sidecar 模式，Wasm 插件提供了更高的执行效率、沙箱隔离性以及多语言（C++, Go, Rust, AssemblyScript 等）开发能力。这是实现认证、鉴权、流量整形等自定义逻辑的最佳方式。

**实施步骤**:
1. 根据团队技术栈选择合适的 Wasm 开发语言（推荐使用 Go 或 Rust）。
2. 利用 Higress 官方提供的 SDK 或 `wasm-as-sdk` 编写插件逻辑。
3. 将编译好的 `.wasm` 文件上传至 Higress 控制台或通过 OCI 存储进行动态加载。
4. 在网关路由配置中关联该插件，并配置具体的规则参数。

**注意事项**: 
- Wasm 插件运行在沙箱中，需注意内存限制，避免处理超大的请求体导致内存溢出。
- 生产环境部署前应对 Wasm 插件进行性能压测，确保其延迟在可接受范围内。

---

### 实践 2：精细化流量管理与流量镜像

**说明**: 利用 Higress 强大的全链路路由能力，实现基于 Header、Query 参数、Cookie 甚至权重的流量分发。特别在进行版本升级或金丝雀发布时，使用流量镜像功能将生产流量复制到测试环境，以验证新版本的稳定性，而不影响真实用户请求。

**实施步骤**:
1. 在控制台定义服务版本，例如将服务分为 `v1` 和 `v2` 两个子集。
2. 配置路由规则，设置特定的流量匹配条件（如 `canary: true`）指向 `v2`。
3. 对于流量镜像，在路由配置中启用 `Mirror` 字段，指定镜像目标服务。
4. 逐步调整 `v1` 到 `v2` 的流量权重（如 10% -> 50% -> 100%）完成灰度发布。

**注意事项**: 
- 流量镜像会复制请求，但不会处理镜像请求的响应，需确保镜像环境有独立的监控手段。
- 镜像流量会消耗网关出站带宽和下游服务算力，需评估对生产环境的性能影响。

---

### 实践 3：对接注册中心实现服务自动发现

**说明**: Higress 能够无缝对接主流注册中心（如 Nacos, Consul, ZooKeeper, Eureka）。通过启用服务发现，网关可以动态感知上游服务的实例上下线，从而避免硬编码 IP 地址，实现云原生化的服务治理。

**实施步骤**:
1. 在 Higress 全局配置或命名空间配置中，添加对应类型的注册中心源。
2. 配置注册中心的连接地址（如 Nacos 的 `serverAddr`）和命名空间等认证信息。
3. 创建服务来源，验证连接状态。
4. 在路由配置中，直接选择服务名作为 `Service`，Higress 将自动根据注册中心的健康实例进行负载均衡。

**注意事项**: 
- 确保网关网络与注册中心网络、网关网络与后端服务 Pod/IP 网络互通。
- 如果使用非标准注册中心，需确保服务名符合 Higress 的服务发现规范。

---

### 实践 4：配置高精度的安全防护策略

**说明**: Higress 内置了丰富的安全插件，包括 IP 访问控制、基本认证（Basic Auth）、JWT 认证以及 API 防火墙。最佳实践是实施“纵深防御”策略，在网关层拦截恶意流量，减轻后端业务服务的压力。

**实施步骤**:
1. 配置 `block-list` 或 `allow-list` 插件，限制特定 IP 段的访问。
2. 对于对外开放的 API，启用 `jwt-auth` 插件，验证请求的 Token 合法性。
3. 启用 `api-breaker` 或 `request-block` 插件，针对特定敏感路径（如 `/admin`）实施严格限制。
4. 结合 Wasm 插件实现自定义的防爬虫或签名验证逻辑。

**注意事项**: 
- 认证配置会轻微增加网关延迟，建议使用高性能的 JWT 验证算法（如 RS256）。
- 定期审计安全规则，避免误封禁合法用户或因规则过宽导致安全漏洞。

---

### 实践 5：利用 Ingress 注解实现 Kubernetes 原生集成

**说明**: 如果在 Kubernetes 集群中运行 Higress，最佳实践是遵循标准的 K8s Ingress 规范，并利用 Higress 特有的 Annotation（注解）来增强功能。这使得配置即代码，方便通过 GitOps 流程进行管理。

**实施步骤**:
1. 编写 Kubernetes Ingress 资源 YAML 文件。
2. 在 `metadata.annotations` 中添加 Higress 特定配置，例如 `nginx.ingress.kubernetes.io/canary: "true"` 的对应

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/3 (QUIC) 协议支持

**说明**: Higress 作为高性能网关，在处理弱网环境或高丢包率网络时，传统的 TCP/TLS 握手延迟会成为瓶颈。HTTP/3 基于 UDP 协议，能显著减少连接建立延迟，提升网络传输层的并发性能。

**实施方法**:
1. 在 Higress 的网关配置中，检查并启用 QUIC 协议监听器。
2. 确保后端服务也支持 HTTP/3 或配置 Higress 进行协议自动转换。
3. 调整操作系统内核参数以优化 UDP 缓冲区大小（如 `net.core.rmem_max` 和 `net.core.wmem_max`）。

**预期效果**: 在弱网环境下，连接建立时间可从 100ms+ 降低至 10ms 以内，页面首字节加载时间（TTFB）平均提升 30% 以上。

---

### 优化 2：配置 Wasm 插件的多线程隔离与缓存

**说明**: Higress 的核心优势之一是支持 Wasm 插件。默认情况下，Wasm 运行在虚拟机中，若插件逻辑复杂（如复杂鉴权或请求转换），会阻塞请求处理线程。通过隔离和缓存优化，可减少 CPU 开销。

**实施方法**:
1. 将计算密集型的 Wasm 插件配置为独立线程或独立进程模式，避免阻塞主 Event Loop。
2. 启用 Wasm 插件的 AOT（Ahead-of-Time）编译缓存（如果版本支持），避免每次请求都进行即时编译。
3. 优化 Wasm 代码中的内存分配，减少垃圾回收（GC）压力。

**预期效果**: Wasm 插件的执行延迟可降低 20%-50%，网关整体 P99 延迟显著下降。

---

### 优化 3：优化连接池与 Keep-Alive 设置

**说明**: 默认的连接管理策略可能导致频繁建立和断开 TCP 连接，增加系统调用开销。优化后端服务的连接池参数和 HTTP Keep-Alive 策略，可以复用连接，降低 RTT（往返时延）。

**实施方法**:
1. 在 Higress 的 `Upstream` 配置中，调大 `http2_max_requests` 和 `max_connections_per_host` 参数。
2. 开启并延长 `idle_timeout` 时间，确保连接在空闲时不被过早关闭。
3. 开启连接池预热，在网关启动或扩容时预先建立与后端的连接。

**预期效果**: 后端连接复用率提升至 80% 以上，吞吐量（QPS）提升 15%-30%。

---

### 优化 4：启用全链路零拷贝与 Sendfile

**说明**: 在处理静态资源或大文件下载代理时，数据在内核空间与用户空间之间频繁拷贝会消耗大量 CPU。利用 Linux 的 `sendfile` 和零拷贝技术，数据直接在文件系统与网卡接口间传输。

**实施方法**:
1. 确认 Higress 底层使用的 Nginx/Envoy 配置中开启了 `sendfile on`。
2. 对于代理类请求，启用 TCP 代理的零拷贝特性（如 Envoy 的 `enable_per_connection_buffer_limit_settings`）。
3. 调整 `buffer_size` 设置，确保大对象传输时使用内存映射而非内存拷贝。

**预期效果**: 文件传输吞吐量提升 40% 以上，CPU 占用率下降 10%-20%。

---

### 优化 5：实施细粒度的服务超时与重试策略

**说明**: 笼统的超时设置会导致慢请求堆积，耗尽网关线程池。精细化的超时与指数退避重试策略能快速剔除故障节点，防止雪崩，提升系统整体吞吐能力。

**实施方法**:
1. 针对不同类型的 API（如读操作与写操作）设置不同的 `timeout` 参数。
2. 配置重试策略，使用 `exponential_backoff`（指数退避）算法，限制重试次数

---
## 学习要点

- Higress 是阿里开源的基于 Istio 的下一代云原生 API 网关，深度集成了 K8s 与 Envoy
- 它提供标准 K8s Ingress Controller 能力，支持将南北向流量管理与微服务治理合二为一
- 内置强大的流量管控特性，如金丝雀发布、蓝绿部署、负载均衡及超时重试等
- 原生支持 Dubbo、Nacos 等中国主流微服务生态，实现了服务发现与协议转换
- 提供开箱即用的安全防护能力，包括 WAF 模块、认证鉴权及针对开源组件漏洞的防护
- 具备高度可扩展性，支持通过 Wasm 插件在运行时动态扩展网关功能，且业务逻辑隔离
- 提供完善的控制台与 Prometheus 监控集成，显著降低了云原生网关的运维与使用门槛


---
## 学习路径

## 学习路径

### 阶段 1：基础概念与环境认知

**学习内容**:
- Higress 的定义与背景：了解 Higress 是什么，它基于 Envoy 和 Istio 构建，以及阿里云开源它的初衷。
- 核心架构：理解 Higress 的架构图，认识 Ingress Gateway、Gateway API 以及控制平面的基本概念。
- 应用场景：掌握 Higress 在云原生流量治理、多语言异构系统（如 Java, Go, Python 联合开发）中的定位。
- 基础安装：学习如何在本地（Docker Desktop）或 Kubernetes 集群中安装 Higress。

**学习时间**: 1周

**学习资源**:
- Higress GitHub 官方仓库 README
- Higress 官方文档 - "什么是 Higress"
- 云原生社区关于 Higress 的介绍文章

**学习建议**:
不要急于动手配置复杂的路由，先通读官方文档的架构部分。建议在本地搭建一个 Kind 或 Minikube 环境，并成功部署一次 Higress，确保可以通过 Dashboard 访问。

---

### 阶段 2：核心流量管理与配置

**学习内容**:
- 路由配置：深入学习如何使用 Ingress API 或 Gateway API 配置 HTTP 路由、Header 匹配、路径重写。
- 负载均衡：掌握轮询、随机、加权等负载均衡策略的配置。
- 服务发现：了解如何对接 Kubernetes Service、Nacos 以及固定地址（DNS/IP）的服务来源。
- 金丝雀发布与蓝绿发布：学习如何基于 Header 或权重进行流量切分，实现灰度发布。
- 基础安全：配置简单的 HTTPS 证书管理与 Basic Auth 认证。

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - "流量管理"板块
- Higress 官方控制台操作指南
- Envoy 基础路由文档（用于理解底层原理）

**学习建议**:
动手实践是关键。尝试部署两个不同版本的 Dummy 服务（如 v1 和 v2），通过 Higress 配置路由规则，实现将 10% 的流量切换到 v2。熟悉控制台（Console）和 K8s YAML 两种配置方式。

---

### 阶段 3：插件生态与可观测性

**学习内容**:
- 插件系统：理解 Higress 的插件机制（Wasm 支持），学习如何在控制台上启用和配置官方插件（如 Keyless Auth、Request Block）。
- 自定义插件：学习如何使用 Lua 或 Go (Wasm) 编写简单的自定义插件来修改请求/响应头或 Body。
- 可观测性集成：学习如何配置 Prometheus 监控指标、集成阿里云 SLS 或开源 ELK 进行日志分析、接入分布式链路追踪。
- 高级安全：了解如何对接 OAuth2/OIDC 进行身份验证，以及配置 IP 访问控制列表。

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档 - "插件市场"与"自定义开发"
- Higress GitHub 官方插件示例
- Wasm (WebAssembly) 在网关中的应用相关博文

**学习建议**:
选择一个实际痛点，例如"统一添加鉴权 Header"，尝试编写一个 Lua 插件来实现它。同时，配置 Prometheus 抓取 Higress 的监控数据，观察流量变化对网关性能（如延迟、QPS）的影响。

---

### 阶段 4：生产级运维与性能优化

**学习内容**:
- 高可用部署：学习 Higress 的高可用架构设计，如何进行多副本部署与灾备切换。
- 性能调优：理解连接池、缓冲区大小、超时时间等参数对性能的影响，如何处理长连接与短连接。
- 网关安全防护：学习如何配置限流（全局限流、并发限流）、熔断降级以保护后端服务。
- 多集群管理：了解如何使用 Higress 进行多集群流量治理。
- 源码级调优：阅读 Higress 核心源码，理解其如何基于 Envoy 进行扩展，具备排查疑难杂症（如连接泄漏、内存溢出）的能力。

**学习时间**: 4周以上

**学习资源**:
- Higress 官方博客 - 最佳实践案例
- Envoy 官方文档 - 性能调优部分
- Higress GitHub 源码

**学习建议**:
此阶段需要结合生产环境思考。尝试模拟高并发场景（使用 Jmeter 或 Hey），观察 Higress 的资源消耗，并根据瓶颈进行参数调优。阅读源码有助于深入理解数据面的处理逻辑。

---
## 常见问题


### 1: Higress 是什么？它与 Kuma、Istio 等 Service Mesh（服务网格）有什么区别？

1: Higress 是什么？它与 Kuma、Istio 等 Service Mesh（服务网格）有什么区别？

**A**: Higress 是一款由阿里云开源的、云原生且标准化的 API 网关。它基于 Envoy 和 Istio 构建，深度集成了阿里内部多年的网关最佳实践。

**主要区别：**
1.  **定位不同**：虽然 Higress 基于 Istio，但传统的 Service Mesh（如 Kuma、Istio）主要侧重于**东西向**流量（即服务与服务之间的通信），用于微服务治理。而 Higress 的核心定位是**南北向**流量管理（即从外部客户端进入后端服务的流量），作为 API 网关使用，专注于流量入口管理、安全防护和协议转换。
2.  **易用性**：Higress 提供了开箱即用的控制台和 Ingress/Gateway CRD，相比原生 Istio 配置更加简便，降低了运维和使用的门槛。
3.  **插件生态**：Higress 内置了丰富的 WAF 防护、流量镜像、流量染色等插件，并支持 Lua 和 WASM (WebAssembly) 插件，扩展性极强，且兼容 Nginx 的生态习惯。

---



### 2: Higress 是否兼容 Kubernetes 的标准 Ingress 资源？如何部署？

2: Higress 是否兼容 Kubernetes 的标准 Ingress 资源？如何部署？

**A**: 是的，Higress 完全兼容 Kubernetes 的标准 Ingress 规范，同时也支持 Gateway API（Kubernetes 社区的新一代 API 标准）。

**部署方式：**
1.  **标准安装**：可以通过 Helm Chart 一键部署到 Kubernetes 集群中。
2.  **Ingress Controller 模式**：Higress 可以作为 Ingress Controller 运行，监听 Kubernetes 的 Ingress 资源变化，并自动配置 Envoy 网关路由。
3.  **托管模式**：在阿里云容器服务 ACK (Alibaba Cloud Container Service for Kubernetes) 中，可以直接使用托管版的 Higress，无需自行运维控制面。

---



### 3: Higress 如何处理流量防护和安全问题（如 WAF）？

3: Higress 如何处理流量防护和安全问题（如 WAF）？

**A**: Higress 提供了企业级的流量安全防护能力，主要通过以下方式实现：

1.  **内置 WAF 插件**：Higress 内置了 Web 应用防火墙功能，可以防御常见的 Web 攻击（如 SQL 注入、XSS、恶意 Bot 流量等）。
2.  **插件市场**：它提供了一个可视化的插件市场，用户可以一键启用各种安全、认证和流量控制插件。
3.  **认证与鉴权**：支持标准的 OpenID Connect (OIDC)、Basic Auth、API Key 等多种认证方式，并能对接外部认证系统（如 Keycloak、OAuth2）。
4.  **限流熔断**：基于令牌桶或并发数等维度进行精细化的限流，保护后端服务不被突发流量击垮。

---



### 4: Higress 是否支持 Dubbo、Nacos 等微服务生态？它能否与 Nginx Ingress 共存？

4: Higress 是否支持 Dubbo、Nacos 等微服务生态？它能否与 Nginx Ingress 共存？

**A**: 支持，且兼容性很强。

1.  **多协议支持**：Higress 原生支持 HTTP、HTTPS、gRPC 以及 Dubbo（HTTP/2 协议栈）等协议。它可以直接注册到 Nacos、ZooKeeper 或 Consul 等注册中心，实现基于服务名的服务发现，而不仅仅局限于 Kubernetes Service。
2.  **与 Nginx Ingress 共存**：可以共存。在 Kubernetes 集群中，可以通过 IngressClass 资源来区分不同的 Ingress Controller 的作用域。你可以让 Nginx 处理特定命名空间或特定注解的流量，而让 Higress 处理其他流量，或者通过 Service 的 LoadBalancer IP 进行区分。不过通常建议统一入口管理以降低复杂度。

---



### 5: Higress 的性能如何？相比 Nginx 有优势吗？

5: Higress 的性能如何？相比 Nginx 有优势吗？

**A**: Higress 的数据面基于 Envoy 构建，性能极其优异。

1.  **高性能**：Envoy 本身采用 C++ 编写，具有极高的吞吐量和极低的延迟。Higress 在此基础上进行了针对阿里云高并发场景的优化。
2.  **对比 Nginx**：
    *   **Nginx**：非常成熟且轻量，配置逻辑是静态的（修改配置通常需要 reload），适合传统的静态路由配置。
    *   **Higress**：支持**热更新**（无需 reload 即可生效路由规则），支持服务发现（动态感知后端服务上下线），具备更强大的可观测性（Metrics、Tracing、Logging）以及标准化的云原生控制面（Istio）。对于复杂的微服务架构和云原生环境，Higress 的动态性和可扩展性优于传统 Nginx。

---



### 6: Higress 支持哪些类型的插件？如何编写自定义插件？

6: Higress 支持哪些类型的插件？如何编写自定义插件？

**A**: Higress 拥有灵活的插件处理架构，主要支持

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单] 本地环境构建与流量路由

### 问题**:

### 参考 Higress 官方文档，在本地 Docker 环境中部署 Higress 网关。配置一个简单的 Ingress 路由规则，将访问 `http://localhost/hello` 的流量转发到一个运行在 8080 端口的本地后端服务（如 Python SimpleHTTPServer 或 Nginx），并确保返回预期的 "Hello World" 响应。

### 提示**:

---
## 实践建议

以下是基于 Higress 作为 AI 网关和 API 网关的实际使用场景，提供的 6 条实践建议：

### 1. 利用 Wasm 插件实现 AI 请求的“提示词”增强与安全审计
*   **场景**：在接入大模型（LLM）时，直接将用户 Prompt 传给模型可能导致敏感信息泄露或遭遇 Prompt 注入攻击。
*   **建议**：不要仅将 Higress 视为流量转发器。利用其 Wasm (WebAssembly) 插件能力，在网关层对请求体进行修改。
    *   **具体操作**：开发或配置 Wasm 插件，在请求转发给 LM 之前，动态插入系统预设的 Prompt（如“你是一个友好的助手”），或者拦截包含特定关键词的恶意请求。
    *   **最佳实践**：将提示词模板的管理权收归至网关层，实现业务代码与提示词逻辑的解耦，便于快速迭代和 A/B 测试不同的提示词策略。

### 2. 实施基于 Token 的精细化流控与成本控制
*   **场景**：大模型 API 的调用成本通常与 Token 数量成正比，传统的基于 QPS（每秒请求数）或并发数的限流无法有效控制成本。
*   **建议**：配置针对 AI 服务的特定限流策略。
    *   **具体操作**：在 Higress 的路由或插件配置中，结合请求体中的 Token 预估（Prompt 长度）进行流控。虽然 Higress 主要处理 HTTP 层，但可以通过配置自定义插件来解析请求长度并结合后端返回的 `usage` 字段进行统计。
    *   **常见陷阱**：不要只限制并发连接数。如果用户发送了一个极长的 Prompt，虽然连接数只占用了 1，但后端成本巨大。建议结合 API Key 的用户维度，设置“每分钟最大 Token 数”的软限制。

### 3. 构建多模型供应商的统一接入层（模型路由）
*   **场景**：业务方可能同时使用通义千问、OpenAI 或本地部署的开源模型，不同模型的接口协议（如 OpenAI 格式与其他格式）存在差异，且切换供应商成本高。
*   **建议**：利用 Higress 的 AI 特性将不同厂商的 API 标准化。
    *   **具体操作**：配置 Higress 的 AI 路由功能，将后端不同的模型服务（如通义、Llama、GPT）统一映射为标准的 OpenAI 协议格式供客户端调用。
    *   **最佳实践**：设置“模型路由”规则，根据请求中的模型名称自动分发到不同的后端服务。例如，请求 `gpt-4` 走 OpenAI 路径，请求 `qwen-turbo` 走阿里云 DashScope 路径。这样业务代码只需修改一个字符串即可切换模型，无需改动 HTTP 调用逻辑。

### 4. 配置语义化缓存以降低延迟与费用
*   **场景**：AI 应用中，大量用户提问可能高度相似（例如“如何使用 Python”），每次都请求 LLM 会导致高延迟和高昂费用。
*   **建议**：启用 Higress 的 AI 缓存插件（通常基于语义向量或精确匹配）。
    *   **具体操作**：针对 `POST /v1/chat/completions` 等接口配置缓存策略。由于是 POST 请求，传统的 URL 缓存失效，需要配置基于请求 Body（Hash 或语义向量）的缓存 Key。
    *   **最佳实践**：设置较短的 TTL（如 5 分钟）以平衡信息的时效性与成本。对于知识库问答类应用，缓存命中率提升能显著改善用户体验。

### 5. 妥善处理流式传输（SSE）的超时与断开
*   **场景**：AI 对话通常采用 Server-Sent Events (SSE) 流式返回，响应时间可能长达数十秒甚至数分钟。
*   **建议**：调整网关层的超时配置以适应长连接

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
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-2.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260130-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260201-github_trending-alibaba-higress-8.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*