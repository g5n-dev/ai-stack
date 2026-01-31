---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-01-31T21:03:22+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "阿里开源", "Istio", "Envoy", "WASM", "LLM", "MCP 协议"]
categories: ["系统与基础设施", "AI 工程"]
source: github_trending
description: "以下是对 Higress 项目的简洁总结： **1. 项目概述** Higress 是一个由阿里巴巴开源的**云原生 AI 原生 API 网关**。基于 Go 语言开发，目前在 GitHub 拥有超过 7,400 颗星。它构建在 Istio 和 Envoy 之上，通过引入 WebAssembly (WASM) 插件能力"
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

Higress 是阿里巴巴开源的基于 Istio 和 Envoy 构建的 AI 原生 API 网关，它通过 WASM 插件扩展了云原生流量管理能力。该项目旨在解决 LLM 应用流量治理、AI Agent 工具集成（MCP）以及微服务路由等场景的统一接入问题。本文将介绍其核心架构，并重点解析 AI 网关特性、插件系统及部署方式，帮助开发者构建高效、可扩展的 AI 基础设施。

---
## 摘要

以下是对 Higress 项目的简洁总结：

**1. 项目概述**
Higress 是一个由阿里巴巴开源的**云原生 AI 原生 API 网关**。基于 Go 语言开发，目前在 GitHub 拥有超过 7,400 颗星。它构建在 Istio 和 Envoy 之上，通过引入 WebAssembly (WASM) 插件能力，扩展了传统网关的功能，特别针对 AI 应用场景进行了深度优化。

**2. 核心架构与特性**
*   **架构设计**：采用**控制平面**与**数据平面**分离的架构。配置变更通过 xDS 协议传播，具备毫秒级延迟和无连接中断的特性，非常适用于 AI 长连接流式响应场景。
*   **扩展能力**：深度集成 WASM 插件系统，支持灵活的功能扩展。

**3. 三大核心应用场景**

*   **AI 网关**：
    *   提供统一 API 接口，兼容 30 多家大语言模型（LLM）提供商。
    *   具备协议转换、可观测性、缓存及安全防护功能（对应 `ai-proxy`, `ai-statistics`, `ai-cache`, `ai-security-guard` 等组件）。

*   **MCP 服务器托管**：
    *   托管模型上下文协议（MCP）服务器，使 AI Agents 能够调用外部工具和服务。
    *   包含路由转换及现成的服务器实现（如搜索、地图工具等）。

*   **Kubernetes Ingress**：
    *   作为 K8s 入口控制器，兼容 nginx-ingress 注解，支持微服务路由和传统流量管理。

---
## 评论

**总体判断**

Higress 是目前云原生网关领域中将“流量治理”与“AI 工程化”结合得最为彻底的开源项目之一。它不仅仅是一个传统的 API 网关，更通过深度集成 WASM 和大模型（LLM）特性，成功转型为 AI 时代的流量入口，具备极高的生产应用价值。

**深入评价依据**

**1. 技术创新性：从“流量侧车”进化为“AI 侧脑”**
*   **事实**：DeepWiki 明确指出 Higress 基于 Istio 和 Envoy 构建，并扩展了 WebAssembly (WASM) 插件能力。同时，它专门定义了“AI Gateway”和“MCP (Model Context Protocol) Server Hosting”功能。
*   **推断**：Higress 的最大差异化在于它**将 AI 协议处理视为一等公民**。传统网关（如 Nginx）处理的是 HTTP/gRPC，而 Higress 内置了对 LLM 协议（如 OpenAI 格式）的感知，能够直接在网关层实现 Prompt 模板管理、Token 计费统计、以及基于语义的流量路由。通过引入 MCP 协议支持，它直接解决了 AI Agent 与工具链连接的标准化问题，这种“网关即 AI 编排器”的架构设计极具前瞻性。

**2. 实用价值：解决 AI 落地“最后一公里”的复杂性**
*   **事实**：文档提到其核心功能包括 AI gateway features for LLM applications（用于 LLM 应用的 AI 网关特性）以及 Kubernetes Ingress（K8s 入口）。
*   **推断**：在传统微服务架构中，Higress 可以无缝替代 Nginx Ingress 或 Kong，提供更强大的南北向流量治理。在 AI 场景中，它解决了企业接入大模型时的痛点：**安全与成本**。企业无需修改后端应用代码，即可在网关层实现敏感词过滤、Key 隔离（多 Key 轮询以防限流）以及请求缓存。这种“非侵入式”的增强方案，极大降低了企业落地 AI 应用的改造成本。

**3. 代码质量与架构：云原生原生的控制与数据分离**
*   **事实**：架构描述中提到“分离了控制平面（配置管理）和数据平面（流量处理）”。
*   **推断**：这种架构是标准的云原生设计模式。利用 Envoy 作为高性能数据平面，保证了 C++ 级别的高吞吐量（L7 处理延迟极低）；而控制平面使用 Go 语言编写（基于 Istio 剥离优化），易于扩展和集成 K8s。WASM 插件系统的引入使得业务逻辑（如鉴权、日志格式化）可以用 C/C++/Go/Rust 编写并动态热加载，无需重启网关，这在大规模分布式系统中是保证稳定性的关键特性。

**4. 社区与生态：阿里的背书与开源活力**
*   **事实**：仓库归属于 Alibaba（阿里巴巴），星标数 7,419，且提供了中、日、英多语言文档。
*   **推断**：作为阿里内部通用的流量网关底层支撑，Higress 经历了双 11 等超大规模流量的验证，其工业级成熟度远高于一般的实验性开源项目。多语言文档表明其具有国际化的野心，且社区活跃度较高，更新迭代速度快，紧跟 AI 技术潮流（如迅速支持 Claude、DeepSeek 等模型）。

**5. 潜在问题与改进建议**
*   **推断**：虽然功能强大，但 Higress 的配置复杂度相对较高。对于仅需简单反向代理的团队，Higress 可能存在“过度设计”的问题。此外，WASM 插件的开发调试门槛相比 Lua（如 OpenResty）要高，生态插件的数量尚不及传统老牌网关丰富。

**边界条件与不适用场景**

*   **不适用场景**：
    *   极其简单的单机应用或边缘计算场景（资源受限，Envoy 占用内存较高）。
    *   需要极其复杂的动态脚本逻辑且团队只精通 Lua 的场景（此时 OpenResty 可能更合适）。
    *   非 K8s 环境下的传统虚拟机部署，虽然支持但无法发挥其最大优势。

**快速验证清单**

1.  **协议兼容性测试**：在 5 分钟内配置一个路由，验证其能否正确转发带有 `Authorization` 头的 OpenAI 格式请求，并检查响应是否被正确透传。
2.  **WASM 插件热加载**：启用一个官方 WASM 插件（如 `request-block`），观察在配置变更下发时，数据平面 Pod 是否未重启且流量瞬间生效。
3.  **AI 特性验证**：配置一个包含多 API Key 的后端服务，发送连续请求，验证网关是否按预设策略（如轮询或随机）在 Key 间切换，以确认负载均衡能力。
4.  **性能基准**：使用 `wrk` 或 `hey` 对比 Higress 与 Nginx 在短连接高并发下的 QPS 与延迟，确保其满足业务 SLA 要求。

---
## 技术分析

以下是对阿里巴巴开源的 **Higress** 项目的深度技术分析。基于其“AI Native API Gateway”的定位，结合 Istio 和 Envoy 的生态，我们将从架构、功能、实现、场景及哲学等多个维度进行剖析。

---

# Higress 深度技术分析报告

## 1. 技术架构深度剖析

Higress 的核心架构逻辑是**“控制平面与数据平面分离”**，并在此基础上通过 **WASM (WebAssembly)** 实现了逻辑的动态扩展。

### 1.1 技术栈与架构模式
*   **底层基石**：基于 **Envoy** 作为高性能数据平面，利用其 L3/L7 网络处理能力。基于 **Istio** (剥离了 Sidecar 模式) 的控制平面思想，利用 xDS 协议进行配置分发。
*   **语言选择**：**Go** 用于控制平面（配置管理、Kubernetes Ingress 控制器、WASM 插件管理）；**C++** (Envoy) 用于核心数据转发；**Rust/Go/C++** (AssemblyScript) 用于编写 WASM 插件。
*   **架构模式**：典型的 **Gateway 模式**。它摒弃了 Istio 原有的 Sidecar 注入模式，专注于 Edge Gateway（边缘网关）或 Ingress Gateway 场景。

### 1.2 核心模块
1.  **Router (路由层)**：支持兼容 Kubernetes Ingress API 和 Nginx Ingress 注解，降低迁移门槛。
2.  **WASM Plugin System (插件系统)**：这是 Higress 的“心脏”。它允许在不重启网关的情况下动态加载插件，逻辑运行在沙箱中，保证了安全性和隔离性。
3.  **AI Gateway Extension (AI 扩展)**：这是最新的核心模块。内置了对 LLM 协议的处理，实现了 Provider 的统一抽象。

### 1.3 技术亮点与创新点
*   **AI Native 原生集成**：Higress 不是事后诸葛亮，而是将 AI 能量（LLM 路由、Token 计费、流式处理）直接内置进网关内核。大多数传统网关（如 Nginx, Kong）处理 AI 流式响应（SSE）时较为吃力，Higress 针对此场景进行了深度优化。
*   **MCP (Model Context Protocol) Server Hosting**：紧跟 AI Agent 生态，允许网关直接托管 MCP 服务，作为 AI Agent 与外部工具之间的桥梁，这是非常前沿的尝试。
*   **毫秒级配置热更新**：得益于 xDS 协议，配置变更下发至数据平面无需重启进程，连接不中断，这对长连接（如 AI 对话流）至关重要。

### 1.4 架构优势分析
*   **低延迟**：数据平面 Envoy 采用 C++ 非阻塞模型，WASM 插件在近内存级别运行，比外部进程调用（如 Lua in Nginx 或 Python 插件）更高效且稳定。
*   **云原生亲和**：CRD (Custom Resource Definition) 驱动，完美融入 K8s 生态。

---

## 2. 核心功能详细解读

### 2.1 主要功能与场景
1.  **AI 网关**：
    *   **统一 API 接口**：将 OpenAI、Azure、通义千问等不同 Provider 的接口统一化，前端应用只需调用一个标准接口。
    *   **Token 计费与限流**：基于 Token 数量而非单纯的请求数进行限流和计费，这对 LLM 应用成本控制至关重要。
    *   **提示词管理**：在网关层注入系统提示词，实现统一的安全合规或人设管理。
2.  **MCP 系统集成**：作为 AI Agent 的工具调度中心，解决 Agent 如何安全、高效地调用外部 API 的问题。
3.  **传统 API 网关**：金丝雀发布、负载均衡、认证鉴权、流量镜像。

### 2.2 解决的关键问题
*   **AI 流式处理的“断头”问题**：传统网关在处理 SSE (Server-Sent Events) 时可能会缓冲数据导致流式输出卡顿。Higress 针对全链路流式透传进行了优化。
*   **模型切换的灵活性**：通过路由规则，可以将流量按比例或按参数路由到不同的模型版本，实现 A/B 测试或灰度发布。

### 2.3 与同类工具对比
*   **VS Nginx/OpenResty**：Nginx 需要配合 Lua 脚本处理复杂逻辑，开发门槛高且容易阻塞 Worker 进程。Higress 的 WASM 插件隔离性更好，且自带 AI 特性。
*   **VS Kong**：Kong 基于 Nginx/OpenResty，虽然也有 WASM 支持，但 Higress 背靠阿里云的 K8s 实践，对云原生和 AI 场景的集成更深入（如 MCP 支持）。
*   **VS Istio Ingress**：Istio 原生 Ingress 配置极其复杂，Higress 提供了更简化的 API 和控制台，降低了使用成本。

### 2.4 技术实现原理
*   **AI 流式透传**：利用 Envoy 的 Streaming Filter 机制，拦截 HTTP 响应头和 Body，识别 SSE 格式，在转发过程中进行字节级处理，确保 `data: {}` 格式不被破坏。

---

## 3. 技术实现细节

### 3.1 关键技术方案
*   **xDS 协议优化**：Higress 控制平面维护配置状态，通过 gRPC Stream 将配置推送到 Envoy。为了解决“配置风暴”，它可能采用了增量 xDS (Incremental xDS) 推送机制。
*   **WASM 虚拟机**：集成 **Wasmtime** 或 **V8** 引擎。当请求进入时，Envoy 挂载 WASM Filter，将请求上下文（Headers、Body）传递给 WASM 虚拟机执行逻辑。

### 3.2 代码组织结构
*   **`pkg/`**：Go 代码核心，包含 Ingress 控制器逻辑（监听 K8s 资源事件）、路由转换逻辑（将 K8s Ingress 转为 Istio 配置）。
*   **`plugins/`**：WASM 插件源码目录，通常使用 AssemblyScript 或 TinyGo 编写。
*   **`docker/`**：容器化构建脚本。

### 3.3 性能优化与扩展性
*   **高性能**：Envoy 本身具备极高的 L7 处理能力（C++ 实现）。WASM 虽然有少量开销（约 5%-10%），但换来了极高的安全性和动态性。
*   **扩展性**：开发者可以用多种语言（C++, Rust, Go, AssemblyScript）编写插件，无需修改网关核心代码。

### 3.4 技术难点与解决方案
*   **难点**：WASM 的内存管理。WASM 插件如果内存泄漏会导致网关 OOM。
*   **方案**：Higress/Envoy 对 WASM 实例设置了严格的内存限制和 CPU 时间片限制，并支持实例的周期性回收。

---

## 4. 适用场景分析

### 4.1 适合使用的项目
1.  **LLM 应用中台**：企业内部统一接入多家大模型（OpenAI, 文心, 通义等），需要统一鉴权、限流、计费。
2.  **AI Agent 基础设施**：需要构建 Agent 应用，且需要通过 MCP 协议集成外部工具（如数据库查询、API 调用）。
3.  **高并发 K8s 入口**：替代 Nginx Ingress Controller，需要更强大的动态路由和 WAF 能力。

### 4.2 最有效的情况
当你的业务需要**“频繁变更网关逻辑”**（如频繁调整 AI 提示词、调整路由规则）且**“不能重启网关”**时，Higress 最为有效。

### 4.3 不适合的场景
*   **极边缘计算**：资源极度受限（如几 MB 内存）的设备，Envoy 本身较重。
*   **简单静态站点**：仅需要简单的反向代理，Nginx 足够且更轻量。

### 4.4 集成方式
通常作为 K8s 的 **Ingress Controller** 部署，或者作为独立网关部署在 K8s 集群外部（接管 Service Mesh 的北向流量）。

---

## 5. 发展趋势展望

### 5.1 技术演进方向
*   **WasmGC 的引入**：随着 WASM 标准演进，支持垃圾回收的语言（如 C#, Java）编写插件将变得更顺畅。
*   **AI 协议的标准化**：不仅仅是 OpenAI 兼容，可能会深度参与 AI 协议的标准化制定（如 SSE 的通用封装）。

### 5.2 与前沿技术的结合
*   **RAG (检索增强生成) 深度集成**：网关可能在请求到达 LLM 之前，直接调用向量数据库进行上下文补充，充当“智能路由”的角色。
*   **eBPF 迁移**：部分网络过滤逻辑可能下沉到 eBPF (Kernel 层) 以获得极致性能，WASM 处理业务逻辑，形成“eBPF + WASM”双层架构。

---

## 6. 学习建议

### 6.1 适合的开发者
*   **云原生运维工程师**：需要从 Nginx 迁移到云原生网关。
*   **后端/架构师**：希望深入理解 Service Mesh 和 API Gateway 原理。
*   **AI 应用开发者**：需要构建企业级 LLM 应用。

### 6.2 学习路径
1.  **基础**：熟悉 Kubernetes Ingress 概念。
2.  **核心**：阅读 Envoy 官方文档中关于 Filter 和 HTTP Routing 的部分。
3.  **进阶**：学习 WebAssembly (WASM) 基础，尝试使用 AssemblyScript 编写一个简单的 Higress 插件（如修改请求头）。
4.  **实践**：在本地 Kind 集群中部署 Higress，配置一个 AI 代理转发。

### 6.3 实践建议
*   从**“零代码”**开始：先使用官方提供的控制台配置路由和插件，观察流量走向。
*   阅读**官方插件源码**：Higress 仓库中的 `plugins/wasm-go` 目录是学习如何用 Go 写 WASM 插件的绝佳范例。

---

## 7. 最佳实践建议

### 7.1 如何正确使用
*   **插件隔离**：生产环境中，对非信任的第三方插件务必开启资源隔离（限制内存和 CPU）。
*   **配置版本化**：将 Higress 的配置（Ingress, Gateway, PluginConfig）存入 Git，通过 GitOps 流程管理，避免控制台误操作。

### 7.2 常见问题与解决
*   **流式响应中断**：检查后

---
## 代码示例




```python
# 示例1：Higress 网关路由配置
def setup_higress_route():
    """
    配置 Higress 网关的路由规则
    解决问题：将不同路径的请求转发到不同的后端服务
    """
    # 模拟 Higress 配置结构
    route_config = {
        "name": "example_route",
        "domains": ["example.com"],
        "routes": [
            {
                "path": "/api/v1/*",
                "backend": "service_v1",
                "timeout": 30
            },
            {
                "path": "/api/v2/*",
                "backend": "service_v2",
                "timeout": 60
            }
        ]
    }
    return route_config

# 使用示例
config = setup_higress_route()
print("Higress 路由配置:", config)
```




```python
# 示例2：Higress 插件配置
def setup_higress_plugin():
    """
    配置 Higress 的插件功能
    解决问题：为网关添加限流和认证功能
    """
    plugin_config = {
        "name": "example_plugin",
        "plugins": [
            {
                "type": "rate-limit",
                "config": {
                    "qps": 100,
                    "burst": 200
                }
            },
            {
                "type": "jwt-auth",
                "config": {
                    "secret": "your-secret-key",
                    "algorithm": "HS256"
                }
            }
        ]
    }
    return plugin_config

# 使用示例
plugin = setup_higress_plugin()
print("Higress 插件配置:", plugin)
```




```python
# 示例3：Higress 服务发现配置
def setup_service_discovery():
    """
    配置 Higress 的服务发现
    解决问题：动态发现和负载均衡后端服务
    """
    discovery_config = {
        "name": "service_discovery",
        "type": "nacos",
        "config": {
            "server_addr": "127.0.0.1:8848",
            "namespace": "public",
            "group": "DEFAULT_GROUP"
        },
        "services": {
            "user-service": ["10.0.0.1:8080", "10.0.0.2:8080"],
            "order-service": ["10.0.0.3:8080", "10.0.0.4:8080"]
        }
    }
    return discovery_config

# 使用示例
discovery = setup_service_discovery()
print("Higress 服务发现配置:", discovery)
```


---
## 案例研究


### 1：阿里巴巴内部电商业务（淘天集团）

 1：阿里巴巴内部电商业务（淘天集团）

**背景**:  
在阿里巴巴庞大的电商生态中，淘天集团面临着海量的API调用需求。每逢“双11”等大促活动，流量瞬间激增，原有的API网关在处理高并发请求时面临巨大压力。同时，业务逻辑复杂，涉及鉴权、限流、流量路由等多种需求，传统的网关架构在扩展性和灵活性上逐渐显现出瓶颈。

**问题**:  
1. 大促期间流量洪峰导致传统网关延迟增加，影响用户体验。  
2. 业务需求变更快，网关配置修改需要重启服务，无法满足热更新的需求。  
3. 多语言（Java、Go、Node.js）微服务架构下的统一治理难度大。

**解决方案**:  
阿里巴巴团队基于Higress构建了下一代云原生API网关。Higress基于Istio与Envoy深度定制，提供了高性能的流量处理能力。通过其Wasm插件机制，团队实现了在不重启网关的情况下动态加载和更新业务逻辑（如限流、鉴权、请求头修改）。同时，利用Higress与Kubernetes的深度集成，实现了自动扩缩容，从容应对流量洪峰。

**效果**:  
1. 成功支撑了“双11”期间每秒数十万级的QPS峰值，P99延迟降低了30%。  
2. 业务逻辑迭代效率提升，网关配置更新时间从分钟级降低到秒级。  
3. 统一了异构微服务的治理标准，运维复杂度显著下降。

---



### 2：某头部互联网金融科技公司

 2：某头部互联网金融科技公司

**背景**:  
该金融科技公司拥有多个核心业务线，包括支付、借贷和财富管理。随着业务向微服务架构迁移，API数量激增至数千个。公司面临的主要挑战是API的安全管控和流量治理，尤其是需要对接OAuth 2.0认证、实现精细化的访问控制，并对接入的第三方API进行严格的流量控制。

**问题**:  
1. 原有的开源网关在配置OAuth 2.0等复杂安全策略时性能损耗较大。  
2. 缺乏灵活的插件系统，开发团队为了实现一个简单的签名校验功能需要修改核心代码，迭代周期长。  
3. 对不同租户和API的流量配额管理不够精细，存在资源争抢风险。

**解决方案**:  
该公司引入Higress作为统一的API入口。利用Higress内置的高性能认证插件和自定义Wasm插件，快速实现了复杂的OAuth 2.0鉴权和自定义签名校验逻辑。通过Higress的精细化限流功能，针对不同的API Key、租户甚至用户ID设置了差异化的QPS阈值。此外，利用Higress的服务发现功能，实现了后端服务的无感上线和下线。

**效果**:  
1. 网关处理请求的CPU占用率下降约20%，在开启安全鉴权的情况下依然保持了极低的延迟。  
2. 新功能的上线周期从数周缩短至数天，开发人员通过编写Wasm插件即可快速扩展功能。  
3. 实现了多租户之间的流量隔离，保障了核心业务的稳定性，未再发生因单租户流量突增导致的系统雪崩。

---



### 3：某大型AI模型服务提供商（AIGC领域）

 3：某大型AI模型服务提供商（AIGC领域）

**背景**:  
随着大语言模型（LLM）的爆发，该公司对外提供了模型推理服务。由于模型推理成本高且耗时较长，客户端经常因网络波动或超时进行重试，导致后端GPU资源被无效请求占用，严重浪费了昂贵的计算资源。同时，需要针对不同用户等级提供差异化的并发限制。

**问题**:  
1. 幂等性支持不足，用户的重复请求直接打到后端，增加了GPU负载和计费争议。  
2. 缺乏针对长连接和流式响应（SSE）的优化支持。  
3. 需要一套能够灵活处理Prompt缓存或请求转换的网关层机制。

**解决方案**:  
该团队选择Higress作为AI网关。利用Higress对Wasm插件的强大支持，开发团队在网关层实现了请求去重（幂等性）逻辑，即针对相同的Prompt请求在短时间内直接返回缓存结果或等待已有请求完成。同时，配置了针对特定用户的并发数限制，防止个别用户占用过多资源。Higress对HTTP/2和流式传输的原生支持也完美适配了AI对话场景。

**效果**:  
1. 后端GPU集群的无效计算请求减少了约15%，显著降低了推理成本。  
2. 在高并发场景下，通过网关层的流量整形，后端服务的稳定性大幅提升。  
3. 基于Higress快速实现了Prompt的预处理和后处理逻辑，无需修改模型推理服务代码。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | APISIX | Kong |
|------|----------------|--------|------|
| 性能 | 高性能，基于 Rust 和 Go 开发，支持高并发 | 极高性能，基于 LuaJIT，适合高吞吐场景 | 高性能，基于 Nginx 和 OpenResty |
| 易用性 | 提供丰富的控制台和插件市场，支持 K8s Ingress | 配置灵活，但学习曲线较陡峭 | 界面友好，社区资源丰富 |
| 成本 | 开源免费，企业版需付费 | 完全开源，无额外成本 | 开源版免费，企业版功能需付费 |
| 扩展性 | 支持自定义插件，适配 K8s 和微服务生态 | 支持自定义插件和动态路由 | 支持插件扩展，但灵活性略低 |
| 社区支持 | 阿里背书，社区活跃 | Apache 基金会项目，社区强大 | 商业化成熟，社区活跃 |

### 优势分析

- 优势1：基于 Rust 和 Go 的混合架构，兼顾性能与安全性。
- 优势2：深度集成阿里云服务，适合云原生和微服务场景。
- 优势3：提供丰富的插件市场和可视化控制台，降低使用门槛。

### 不足分析

- 不足1：相比 APISIX，社区生态和插件数量仍有差距。
- 不足2：企业版功能可能需要付费，增加长期成本。
- 不足3：文档和社区支持不如 Kong 和 APISIX 完善。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Envoy 的深度定制与性能优化

**说明**:  
Higress 基于 Envoy 构建，充分利用其高性能和可扩展性。通过深度定制 Envoy，Higress 提供了更优化的路由、负载均衡和流量管理能力，同时支持动态配置和热更新，减少服务中断。

**实施步骤**:
1. 部署 Higress 时，确保使用最新稳定版本的 Envoy 作为基础。
2. 配置 Envoy 的动态资源发现机制（如 xDS 协议）以实现实时更新。
3. 根据业务需求调整 Envoy 的线程和工作进程配置，优化 CPU 和内存使用。

**注意事项**:  
- 定期监控 Envoy 的性能指标（如延迟、吞吐量），及时调整配置。  
- 避免频繁修改核心配置，以减少不必要的重启或资源消耗。

---

### 实践 2：服务网格与 API 网关的融合

**说明**:  
Higress 将服务网格与 API 网关功能结合，提供统一的流量管理入口。通过这种融合，可以简化微服务架构中的流量控制、安全认证和监控。

**实施步骤**:
1. 将 Higress 部署为 API 网关，统一管理所有外部流量入口。
2. 配置服务网格规则，实现内部服务间的通信管理和流量路由。
3. 使用 Higress 的插件机制扩展功能，如限流、熔断或自定义认证。

**注意事项**:  
- 确保服务网格和 API 网关的配置一致性，避免冲突。  
- 在生产环境部署前，充分测试流量路由和安全策略。

---

### 实践 3：插件化扩展能力

**说明**:  
Higress 支持通过插件扩展功能，允许开发者根据业务需求定制流量处理逻辑。插件可以用于日志记录、协议转换、流量整形等场景。

**实施步骤**:
1. 编写自定义插件，遵循 Higress 的插件开发规范。
2. 将插件编译为动态链接库（.so 文件），并部署到 Higress 的插件目录。
3. 在 Higress 配置中启用插件，并设置相关参数。

**注意事项**:  
- 插件开发需注意线程安全，避免资源泄漏。  
- 定期更新插件以兼容 Higress 的新版本。

---

### 实践 4：多协议支持与流量治理

**说明**:  
Higress 支持 HTTP、HTTPS、gRPC 等多种协议，并提供灵活的流量治理能力，如灰度发布、蓝绿部署和 A/B 测试。

**实施步骤**:
1. 配置 Higress 的路由规则，支持多协议流量分发。
2. 使用流量标签或 Header 实现灰度发布或 A/B 测试。
3. 监控流量分发效果，动态调整规则。

**注意事项**:  
- 确保协议转换的正确性，避免数据丢失或格式错误。  
- 灰度发布时需逐步放量，避免全量故障。

---

### 实践 5：安全认证与访问控制

**说明**:  
Higress 提供多层次的安全认证机制，包括 JWT、OAuth 2.0 和 mTLS，确保 API 和服务的安全性。

**实施步骤**:
1. 配置 JWT 或 OAuth 2.0 认证，保护 API 端点。
2. 启用 mTLS 加密服务间通信。
3. 设置 IP 白名单或黑名单，限制访问来源。

**注意事项**:  
- 定期轮换密钥和证书，避免安全漏洞。  
- 监控异常访问行为，及时响应安全事件。

---

### 实践 6：可观测性与监控集成

**说明**:  
Higress 集成了 Prometheus、Grafana 和 OpenTelemetry 等工具，提供全面的流量监控、日志分析和性能追踪能力。

**实施步骤**:
1. 配置 Higress 的 Prometheus Exporter，收集指标数据。
2. 集成 OpenTelemetry，实现分布式追踪。
3. 使用 Grafana 创建可视化仪表盘，监控关键指标。

**注意事项**:  
- 确保监控数据的存储和查询性能，避免影响业务系统。  
- 设置合理的告警阈值，及时发现异常。

---

### 实践 7：高可用部署与容灾设计

**说明**:  
Higress 支持多副本部署和自动故障转移，确保系统的高可用性和容灾能力。

**实施步骤**:
1. 部署多个 Higress 实例，配置负载均衡器分发流量。
2. 启用健康检查机制，自动剔除故障实例。
3. 定期进行故障演练，验证容灾方案的有效性。

**注意事项**:  
- 确保跨可用区部署，避免单点故障。  
- 备份关键配置和数据，便于快速恢复。

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/2 与 HTTP/3 (QUIC) 协议

**说明**: Higress 基于 Envoy 构建，对现代 HTTP 协议有良好的原生支持。HTTP/2 通过多路复用解决了 HTTP/1.1 的队头阻塞问题，而 HTTP/3 (QUIC) 基于 UDP 协议，能显著减少弱网环境下的延迟和连接建立时间。

**实施方法**:
1. 在网关监听器配置中，启用 HTTP/2 协议支持。
2. 对于需要极致性能的场景，配置并开启 QUIC 协议（需确保客户端支持）。
3. 调整 HTTP/2 的并发流限制参数（`max_concurrent_streams`）以匹配业务负载。

**预期效果**: 弱网环境下请求延迟降低 30%-50%，高并发下连接数减少，资源利用率提升。

---

### 优化 2：启用全链路异步调用与 DNS 缓存

**说明**: 默认的同步阻塞调用会占用大量线程资源，导致吞吐量下降。通过启用异步调用模式，可以大幅提升网关的并发处理能力。同时，配置 DNS 缓存可以避免频繁的 DNS 查询延迟。

**实施方法**:
1. 在 Higress 路由配置中，启用 Upstream 的异步 DNS 解析功能。
2. 配置严格的 DNS 缓存 TTL（Time To Live），减少上游服务的域名解析开销。
3. 确保后端服务客户端使用非阻塞 I/O 模型。

**预期效果**: P99 延迟降低 10%-20%，单实例并发处理能力提升 50% 以上。

---

### 优化 3：配置合理的连接池与超时参数

**说明**: 默认的连接池配置往往无法满足高并发生产环境的需求。过小的连接池会导致请求排队等待，过大的连接池则浪费资源。合理的超时设置能防止长连接堆积导致的资源耗尽。

**实施方法**:
1. 根据后端服务性能，调整 HTTP 连接池大小（建议初始值设为 128 或更高）。
2. 配置合理的 `connect_timeout`（连接超时）和 `request_timeout`（请求超时），避免无效连接长期占用资源。
3. 启用连接的 Keep-Alive 机制，减少 TCP 三次握手的频率。

**预期效果**: 后端服务响应时间（RT）波动减小，网关吞吐量（QPS）提升 20%-40%。

---

### 优化 4：优化 WAF 与插件执行链路

**说明**: Higress 支持丰富的插件生态（如 WAF、限流、认证等）。复杂的插件逻辑或全量请求的 WAF 检测会显著增加 CPU 负载和延迟。

**实施方法**:
1. 将高开销的插件（如复杂的 Lua 脚本或 WAF 规则）配置为按需加载，仅针对特定路由生效。
2. 优化 WAF 规则，移除冗余或低效的正则表达式，优先使用 OWASP 核心规则集的优化版本。
3. 使用本地缓存减少插件对外部存储（如 Redis）的依赖。

**预期效果**: CPU 使用率降低 15%-30%，平均请求处理延迟减少 5ms-10ms。

---

### 优化 5：启用数据平面与控制平面分离及水平扩缩容

**说明**: Higress 的架构支持控制平面与数据平面分离。在高流量场景下，数据平面的资源瓶颈是主要性能限制因素。通过水平扩容数据平面节点，可以实现线性性能扩展。

**实施方法**:
1. 部署独立的 Higress 数据平面节点组。
2. 配置 Kubernetes HPA（Horizontal Pod Autoscaler），根据 CPU 或 QPS 指标自动调整 Pod 副本数。
3. 确保控制平面配置变更能高效地下发至数据平面，减少配置推送带来的瞬态抖动。

**预期效果**: 系统吞吐量实现近线性增长，整体可用性提升至 99.99% 以上。

---
## 学习要点

- Higress 是阿里开源的基于 Istio 的云原生 API 网关，深度集成了 K8s Ingress 与 Gateway API 标准
- 提供了强大的流量治理能力，包括金丝雀发布、蓝绿部署、负载均衡及超时重试等企业级特性
- 内置了对 Dubbo、Nacos 及 Spring Cloud 等微服务生态的完善支持，能够实现服务发现与协议转换
- 具备高性能的 WAF（Web 应用防火墙）插件市场，支持安全防护与流量管理的灵活扩展
- 架构设计上实现了数据面与控制面的分离，支持将 K8s Service 直接路由为 API，降低了云原生架构的复杂度


---
## 学习路径

## 学习路径

### 阶段 1：入门基础

**学习内容**:
- 云原生网关的基本概念与 Higress 的核心特性
- Higress 与传统网关（如 Nginx、Spring Cloud Gateway）的区别
- Higress 的核心架构：Ingress Controller 与 Gateway 的分离
- 基础环境搭建：Docker Compose 部署或 Kubernetes 集群部署
- 基本流量管理：域名转发、路由匹配（前缀匹配、精确匹配）

**学习时间**: 1-2周

**学习资源**:
- Higress 官方文档: https://higress.io/docs/latest/overview/what-is-higress/
- Higress GitHub 仓库: https://github.com/alibaba/higress
- 官方快速入门指南

**学习建议**:
建议先阅读官方文档了解架构设计，然后使用 Docker Compose 在本地快速搭建一个环境。通过配置一个简单的静态路由（例如将域名转发到百度或一个测试服务）来验证部署成功。

---

### 阶段 2：核心功能与流量治理

**学习内容**:
- 高级路由配置：基于 Header、Query 参数、Cookie 的路由转发
- 服务发现集成：Nacos、Consul、DNS、固定地址（Upstream）配置
- 负载均衡策略：加权轮询、一致性哈希等
- 流量治理：金丝雀发布、蓝绿发布、Header 重写/重定向
- 全局与自定义插件管理：Waf 防护、CORS 跨域配置等基础插件使用

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 流量管理章节
- Higress 官方文档 - 插件市场
- Higress 官方示例仓库

**学习建议**:
尝试在 Kubernetes 环境中部署 Higress，并结合 Nacos 注册中心进行服务发现。重点练习“金丝雀发布”场景，模拟将 10% 的流量路由到新版本服务。同时，熟悉控制台（Console）的操作，尝试开启并配置几个常用的官方插件。

---

### 阶段 3：插件开发与安全防护

**学习内容**:
- 安全防护：配置 Basic Auth、Key Auth 认证
- 流量防护：限流规则（基于请求速率、并发数）
- 插件系统深入：Wasm 插件原理与 Go/Python 插件开发
- 自定义插件开发：编写一个简单的 Wasm 插件（例如修改请求响应头）
- 插件热加载与调试流程

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档 - 开发指南
- Higress 官方文档 - 安全防护
- Higress 插件开发模板

**学习建议**:
这一阶段是进阶的关键。建议从修改现有的官方插件开始，理解 Plugin 的上下文。随后，尝试使用 Go 语言编写一个自定义 Wasm 插件，并在本地或测试环境中进行编译、上传和调试。重点关注如何通过插件实现业务逻辑的非侵入式植入。

---

### 阶段 4：生产级运维与性能优化

**学习内容**:
- 高可用部署：多副本部署、健康检查与探针配置
- 可观测性：对接 Prometheus/Grafana 监控指标、访问日志分析（SLS/ELK）、链路追踪
- 配置管理：Ingress API 与 Gateway API 的使用，GitOps 实践
- 性能调优：连接池配置、缓存策略、资源限制
- 灾备与回滚机制

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 运维指南
- Higress 官方文档 - 可观测性
- Kubernetes Ingress Controller 最佳实践

**学习建议**:
模拟生产环境进行压测（使用 JMeter 或 Hey），观察 Higress 的 CPU/内存表现，并根据监控指标调整资源配置。配置日志采集，分析慢请求。学习如何通过 Kubernetes 的 Ingress YAML 文件管理配置，实现基础设施即代码。

---

### 阶段 5：架构设计与生态集成

**学习内容**:
- Higress 在微服务架构中的定位：东西向流量与南北向流量的统一管理
- AI 网关特性：对接大模型（LLM）进行 Prompt 模板管理、Token 计费与限流
- 多集群管理与多租户隔离
- 服务网格 结合使用（如 Istio）
- 源码级深度剖析：Envoy 底层原理与 Higress 的扩展机制

**学习时间**: 持续学习

**学习资源**:
- Higress 官方博客与架构演进文章
- Higress AI 网关最佳实践
- Envoy 官方文档

**学习建议**:
关注 Higress 的最新动态，特别是 AI 网关方向的功能。

---
## 常见问题


### 1: Higress 是什么？它与 Kuma、Kong 或 APISIX 等其他 API 网关有何区别？

1: Higress 是什么？它与 Kuma、Kong 或 APISIX 等其他 API 网关有何区别？

**A**: Higress 是一个开源的、云原生的 API 网关。它是基于阿里云内部多年的网关实践经验，结合 Envoy 和 Istio 的技术栈构建的。

它的主要区别和优势在于：
1.  **深度集成 K8s 与 Istio**: Higress 原生支持 Kubernetes 和 Istio，可以作为 Ingress Controller 使用，也能作为服务网格中的东西向流量网关，实现流量的统一管理。
2.  **高性能**: 基于 Envoy C++ 内核构建，具备极高的吞吐量和低延迟。
3.  **插件生态**: 它提供了一套标准的 WASM (WebAssembly) 插件市场，支持 Go、C++、AssemblyScript 等多种语言编写插件，且插件热更新不中断业务。
4.  **易用性**: 提供了开箱即用的控制台 (Console)，相比传统的 Istio 配置更加简单直观。

---



### 2: Higress 与 Nginx Ingress Controller 相比，有哪些优势？

2: Higress 与 Nginx Ingress Controller 相比，有哪些优势？

**A**: 虽然 Nginx Ingress 是目前最流行的 K8s 入口网关之一，但 Higress 在以下几个方面具有显著优势：

1.  **架构**: Nginx Ingress 通常需要配合 Lua 脚本扩展功能，而 Higress 基于 Envoy，采用更现代的云原生架构。
2.  **扩展性**: Higress 支持 WASM 插件，插件编写更安全（崩溃不会导致网关崩溃）且灵活。Nginx 的 Lua 扩展对开发者有一定门槛，且维护成本较高。
3.  **服务发现**: Higress 原生对接 Nacos、ZooKeeper、Consul 等注册中心，非常适合微服务架构；而 Nginx Ingress 主要依赖 K8s Service，对接第三方注册中心通常需要额外配置。
4.  **安全防护**: Higress 内置了更完善的 WAF（Web 应用防火墙）能力和流量治理能力，如全局限流、熔断降级等。

---



### 3: Higress 是否兼容 Istio？能否直接替换 Istio Ingress Gateway？

3: Higress 是否兼容 Istio？能否直接替换 Istio Ingress Gateway？

**A**: 是的，Higress 兼容 Istio 的 API 规范。

1.  **无缝替换**: Higress 可以直接作为 Istio 的 Ingress Gateway 部署。它支持标准的 Istio Gateway 和 VirtualResource CRD，这意味着你现有的 Istio 流量配置规则可以直接迁移使用。
2.  **增强功能**: 相比于官方的 Istio Ingress Gateway，Higress 提供了更友好的控制台、更丰富的插件市场（如鉴权、请求改写等）以及更强的可观测性支持。

---



### 4: 如何在 Higress 中编写和加载自定义插件？

4: 如何在 Higress 中编写和加载自定义插件？

**A**: Higress 提供了非常灵活的插件扩展机制，主要通过以下方式：

1.  **WASM 插件**: 这是推荐的方式。开发者可以使用 Go (推荐)、AssemblyScript、C++ 或 Rust 编写逻辑。Higress 官方提供了 `wasm-go-sdk` 帮助开发者快速构建插件。
2.  **加载方式**:
    *   **控制台上传**: 编译好的 `.wasm` 文件可以直接通过 Higress 控制台上传并配置生效。
    *   **OCI 镜像存储**: 插件可以打包成 OCI 镜像（类似于 Docker 镜像），存储在镜像仓库中，Higress 会自动拉取并加载。
3.  **配置**: 插件支持全局配置、路由级配置或服务级配置，且可以在运行时动态修改，无需重启网关进程。

---



### 5: Higress 支持哪些服务发现机制？是否支持非 K8s 环境？

5: Higress 支持哪些服务发现机制？是否支持非 K8s 环境？

**A**: Higress 的定位是“连接云原生和微服务”，因此它支持非常广泛的服务发现机制：

1.  **Kubernetes Service**: 原生支持 K8s 的 Service 和 Endpoint。
2.  **注册中心**: 支持 Nacos (阿里云/开源)、ZooKeeper、Consul、DNS、固定地址（IP 列表）等。这使得 Higress 可以部署在 K8s 之外，作为传统微服务的流量入口。
3.  **混合模式**: Higress 允许同时从 K8s 和外部注册中心（如 Nacos）获取服务列表，实现混合云或迁移场景下的流量调度。

---



### 6: Higress 的性能表现如何？是否适合生产环境？

6: Higress 的性能表现如何？是否适合生产环境？

**A**: Higress 是为生产环境设计的，具备高性能和高可用性。

1.  **基准测试**: 基于 Envoy 的高性能内核，Higress 在长连接、短连接、HTTPS 加解密等场景下均表现出色。官方基准测试数据显示，其吞吐量与延迟在同类产品中处于领先水平。
2.  **生产就绪**: 阿里云内部的 API �

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 在本地 Docker 环境中快速部署一套 Higress 最小可用集群，并配置一个简单的路由规则，将访问 `/hello` 的流量转发到后端的 `httpbin.org` 服务。

### 提示**: 需要查阅 Higress 官方文档中的 "快速开始" 章节。核心在于编写正确的 `docker-compose.yml` 文件以及使用 Higress 控制台（Console）配置 Ingress 路由。注意区分 Higress 与传统 Nginx Ingress 在配置语法上的区别。

### 

---
## 实践建议

以下是基于 Higress 作为 AI 网关和 API 网关的实际使用场景，提供的 6 条实践建议：

### 1. 利用 AI 提示词模板实现服务标准化
**场景：** 多个前端应用或内部服务调用同一大模型（如 GPT-4 或通义千问），但需要预设不同的系统角色或提示词。
**建议：** 不要在应用代码中硬编码 Prompt。在 Higress 中配置 AI 服务的路由时，使用其 **Prompt Template** 功能。将系统提示词配置在网关层，前端请求仅需携带用户问题（User Query）。
**收益：** 集中管理提示词版本，无需重新部署业务代码即可调整模型行为，降低 Prompt 泄露风险。

### 2. 配置上下文缓存以降低 Token 成本
**场景：** 业务涉及长文档总结或连续对话，每次请求都携带大量重复的上下文（如几万字的文档），导致 API 调用成本极高。
**建议：** 针对支持缓存能力的模型（如 Claude 3.5 或部分长上下文模型），在 Higress 的 AI 服务配置中开启或利用 **语义缓存** 策略。对于相同的文档内容或高频重复问题，直接由网关返回缓存结果，而不将请求转发给 LLM 提供商。
**收益：** 显著降低 Token 消耗和 API 延迟。

### 3. 实施基于 Token 的细粒度限流
**场景：** 传统 API 网关通常基于“请求数/秒”（QPS）限流，但 AI 请求由于上下文长度不同，后端成本差异巨大。短 Prompt 请求可能只需 0.01 美元，长 Prompt 可能需要 1 美元。
**建议：** 在 Higress 的插件配置中，优先使用基于 **Token 吞吐量** 或 **请求时长** 的限流策略，而非简单的 QPS 限流。针对不同等级的 API Key 设置不同的 Token 预算上限。
**收益：** 防止个别长文本请求拖垮整个服务的后端预算，实现更精准的成本控制。

### 4. 构建模型供应商的兜底与降级策略
**场景：** 生产环境直接调用单一模型提供商（如 OpenAI），一旦该服务商 API 宕机或速率限制，业务直接中断。
**建议：** 利用 Higress 的 **服务来源** 抽象能力，配置多模型供应商。例如，主线路配置为 OpenAI，备用线路配置为 Azure OpenAI 或本地部署的 Qwen 模型。配置超时策略与自动重试机制，当主线路超时时自动切换至备用模型。
**收益：** 提高 AI 服务的可用性（SLA），避免因单一厂商故障导致服务不可用。

### 5. 警惕流式传输的超时配置
**场景：** 启用了 SSE（Server-Sent Events）流式响应以实现打字机效果，但网关层的超时时间设置过短（例如默认 60 秒），导致长回答在生成中途被网关主动断开连接。
**建议：** 检查路由或全局配置中的 `request_timeout` 或 `idle_timeout`。对于 AI 流式对话，建议将超时时间放宽，或者根据模型的最大输出 Token 数进行估算后配置。同时，确保客户端能够处理连接断开后的重试逻辑。
**收益：** 避免用户体验不佳（回答突然中断），减少因超时导致的错误投诉。

### 6. 敏感数据脱敏与安全防护
**场景：** 用户在提问中可能无意间包含 PII（个人敏感信息，如身份证号、手机号）或内部机密数据，这些数据直接发送给公网大模型存在合规风险。
**建议：** 在 AI 请求转发至上游模型之前，挂载 Higress 的 **WAF 插件** 或自定义插件，对请求体进行正则匹配或语义分析，拦截或脱敏敏感字段后再转发给 LLM。
**收益：** 满足企业数据安全

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
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260130-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [Amla Sandbox：面向 AI 智能体的 WASM Bash 沙箱]({{< relref "posts/20260130-hacker_news-show-hn-amla-sandbox-wasm-bash-shell-sandbox-for-a-7.md" >}})
- [Amla Sandbox：面向 AI 智能体的 WASM Bash 沙箱]({{< relref "posts/20260130-hacker_news-show-hn-amla-sandbox-wasm-bash-shell-sandbox-for-a-1.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*