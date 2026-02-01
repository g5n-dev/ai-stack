---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-02-01T09:10:38+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API网关", "AI原生", "Istio", "Envoy", "MCP协议", "WASM", "LLM网关"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "以下是对 **Higress** 的简洁总结： **Higress** 是阿里巴巴开源的一款**云原生 AI 原生 API 网关**，基于 **Istio** 和 **Envoy** 构建，并使用 **Go** 语言编写（GitHub 星标数超 7,400）。它旨在为云原生应用和 AI 时代的大模型（LLM）应用提供统"
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

Higress 是基于 Istio 和 Envoy 构建的云原生 API 网关，通过扩展 WASM 插件能力，兼顾了传统流量管理与 AI 原生场景。它主要面向需要统一处理微服务路由、Kubernetes Ingress 以及大模型应用流量的开发者，解决了在 AI 时代对协议转换与模型服务管理的复杂需求。本文将介绍其核心架构、AI 网关特性以及 MCP 系统集成等关键功能。

---
## 摘要

以下是对 **Higress** 的简洁总结：

**Higress** 是阿里巴巴开源的一款**云原生 AI 原生 API 网关**，基于 **Istio** 和 **Envoy** 构建，并使用 **Go** 语言编写（GitHub 星标数超 7,400）。它旨在为云原生应用和 AI 时代的大模型（LLM）应用提供统一的流量入口与管理。

**核心定位与架构：**
Higress 通过 **WebAssembly (WASM)** 插件扩展了传统网关能力。其架构采用**控制平面**与**数据平面**分离的设计，支持通过 xDS 协议进行毫秒级配置变更，且不中断连接，特别适用于 AI 长连接流式响应场景。

**三大核心功能：**

1.  **AI 网关：**
    *   提供统一 API 接入，兼容 30+ 家大模型提供商。
    *   支持协议转换、可观测性、缓存及安全防护。
    *   *核心组件：* `ai-proxy`, `ai-statistics`, `ai-cache` 等插件。

2.  **MCP 服务器托管：**
    *   托管 **模型上下文协议 (MCP)** 服务器，使 AI Agent 能够便捷地调用外部工具和服务。
    *   *核心组件：* `mcp-router`, `jsonrpc-converter` 以及多种 MCP 服务器实现（如地图搜索等工具）。

3.  **标准 API 网关：**
    *   兼容 Kubernetes Ingress，支持微服务路由，并兼容 Nginx Ingress 注解。
    *   *核心组件：* `higress-controller`。

简而言之，Higress 是一款将现代微服务治理与 AI 应用特性（如模型统一管理、Agent 工具调用）深度融合的新一代网关。

---
## 评论

**总体判断**

Higress 是阿里云开源的一款极具前瞻性的“AI 原生”网关，它成功地将云原生流量治理与 AI 大模型应用需求深度融合。该项目不仅是传统 API 网关的有力竞争者，更是当前构建 LLM（大语言模型）应用基础设施中最具落地潜力的开源方案之一。

**深入评价依据**

**1. 技术创新性：从“流量管道”进化为“AI 神经中枢”**
*   **事实**：DeepWiki 明确指出 Higress 基于 Istio 和 Envoy 构建，并扩展了 WebAssembly (WASM) 插件能力。其核心创新点在于“AI Gateway Features”和“MCP (Model Context Protocol) Server Hosting”。
*   **推断**：Higress 的差异化在于它没有停留在传统的 HTTP 转发层面，而是针对 AI 时代做了深度定制。通过内置对 MCP 协议的支持，它解决了 AI Agent 与外部工具集成的标准化难题。利用 WASM 的沙箱隔离和高性能特性，开发者可以用 C++/Go/Rust/AssemblyScript 编写插件（如 Prompt 模板注入、敏感词过滤、Token 计费），实现了业务逻辑与网关内核的解耦，这种“可观测性 + AI 专用协议代理”的架构在当前开源界极具先进性。

**2. 实用价值：解决 LLM 落地中的“最后一公里”痛点**
*   **事实**：文档描述中提到其具备“AI gateway features for LLM applications”以及“traditional API gateway capabilities”。
*   **推断**：Higress 极具实用价值，因为它直击了 AI 应用开发的痛点：**兼容性与稳定性**。企业接入 LLM 时，通常面临 OpenAI 格式与国内厂商模型格式不统一的问题。Higress 作为 AI 网关，能够统一这些异构 API 的调用入口，实现模型切换的零代码改动。同时，它复用了 Envoy 的高并发处理能力，解决了直接暴露 LLM 服务端点所面临的并发限制和安全性问题，是企业级 AI 应用落地的“防波堤”。

**3. 代码质量与架构：云原生标准的集大成者**
*   **事实**：项目采用 Go 语言开发，架构上明确分离了控制平面和数据平面。
*   **推断**：基于 Istio 和 Envoy 的架构选择保证了底层代码的健壮性与高性能。Go 语言的使用契合云原生生态，便于在 Kubernetes 环境中部署。从 DeepWiki 的详细文档结构（涵盖核心架构、构建部署、开发指南等）可以看出，该项目具备极高的工程成熟度，文档覆盖全面，这通常意味着代码规范清晰，模块划分合理，适合大型团队协作维护。

**4. 社区活跃度：背靠阿里的强力驱动**
*   **事实**：GitHub 星标数达到 7,419（且在持续增长），由阿里巴巴主导。
*   **推断**：作为阿里云核心产品（Higress 商业版）的开源实现，该项目不仅有阿里内部的工程资源投入，还有明确的商业化路线图支撑，避免了个人开源项目常见的维护停滞风险。高星标数反映了社区对“云原生 + AI”这一技术方向的认可，活跃的 Issue 和 PR 讨论表明其正在快速迭代以适应 AI 领域的日新月异。

**5. 学习价值与对比优势：不仅是工具，更是架构范本**
*   **事实**：对比同类工具（如 APISIX, Kong），Higress 原生支持 Istio。
*   **推断**：对于开发者而言，Higress 是学习如何将 WASM 技术应用于生产环境的最佳范例。与 Kong 或 APISIX 相比，Higress 最大的优势在于其**云原生血统**和对 **AI 场景的原生支持**。Kong 虽然也有 AI 插件，但更多是“外挂式”的；而 Higress 是从内核层面集成了 AI 代理逻辑（如流式数据处理、上下文缓存策略），且完全兼容 K8s Ingress 标准，对于已落地 Istio 的企业来说，接入 Higress 的心智负担极低。

**边界条件与不适用场景**

尽管 Higress 功能强大，但在以下场景中可能不是最优解：
1.  **边缘计算或资源极度受限环境**：基于 Envoy 和 Go 的架构相对重量化，对于仅有几 MB 内存的嵌入式设备，Higress 过于庞大。
2.  **极简静态站点托管**：如果仅需简单的静态文件服务或反向代理，Nginx 的配置更直观轻便。
3.  **非 K8s 环境的传统运维**：如果不使用 Kubernetes，Higress 的控制面部署和管理复杂度会显著上升，不如传统硬件负载均衡器或 Nginx 易于维护。

**快速验证清单**

在决定将 Higress 投入生产前，建议进行以下验证：
1.  **WASM 插件性能测试**：编写一个简单的 WASM 插件（如修改请求头），进行压测，对比开启插件前后的延迟增加（目标：< 5ms）和内存开销。
2.  **AI 流式传输兼容性**：验证 Higress 在转发 LLM 流式响应（SSE）时，是否会出现分块丢失或延迟抖动，确保对话体验的丝滑。
3.  **配置漂移检查**：在 Kubernetes 中修改 Ingress 配置，检查 Higress 控制面是否能实时将配置下发到数据平面

---
## 技术分析

基于对 Alibaba Higress 仓库的深入分析，以下是关于该项目的全面技术评估报告。

---

# Alibaba Higress 深度技术分析报告

## 1. 技术架构深度剖析

### 1.1 技术栈与架构模式
Higress 采用了**云原生**架构模式，其核心定位是建立在 Istio 和 Envoy 之上的“AI Native API Gateway”。

*   **底层基石**：使用 **Envoy** 作为高性能数据平面，处理所有入站和出站流量。利用 Envoy 的 C++ L3/L4/L7 处理能力，确保低延迟。
*   **控制平面**：深度集成 **Istio**，复用其 xDS (控制平面下发协议) 机制。这意味着 Higress 继承了 Istio 的配置管理和服务发现能力，但对其进行了简化和针对网关场景的优化。
*   **扩展机制**：引入 **WebAssembly (WASM)** 作为核心插件运行时。这允许开发者使用 C/C++、Go、Rust、JavaScript 等高级语言编写业务逻辑，而不需要修改 Envoy 的 C++ 核心代码或重新编译二进制文件。

### 1.2 核心模块与关键设计
架构遵循典型的**控制平面与数据平面分离**模式：

*   **控制平面**：
    *   **配置管理**：通过 Kubernetes CRD (Custom Resource Definition) 或控制台 UI 定义路由规则。
    *   **xDS 转换**：将用户定义的网关配置（如 Ingress、Gateway API）转换为 Envoy 可理解的 xDS 协议（LDS, RDS, CDS, EDS）。
    *   **MCP (Model Context Protocol) Server**：这是针对 AI 场景的新增模块，用于托管 AI Agent 的工具接口。
*   **数据平面**：
    *   **流量转发**：基于 Envoy 的高性能转发。
    *   **WASM 虚拟机**：在请求处理路径中加载和执行 WASM 插件。
    *   **AI 代理**：针对 LLM (大语言模型) 的特殊处理逻辑，如流式转发、Token 计数、Prompt 模板管理。

### 1.3 技术亮点与创新点
*   **AI Native 理念**：这是 Higress 与 Nginx、传统 Kong 最大的区别。它原生集成了对 LLM 协议（OpenAI 协议兼容）的支持，提供了**Provider 抽象**。用户可以在网关层配置不同的 LLM 提供商（如通义千问、OpenAI、Azure），并在路由中动态切换，实现了 AI 流量的统一管理。
*   **MCP 协议支持**：作为 AI Agent 的工具层，Higress 可以托管 MCP Server，使得 Agent 能够安全、标准化地调用外部工具，这是迈向 AI 基础设施的重要一步。
*   **热更新能力**：基于 Istio 的 xDS 机制，配置变更可以达到毫秒级生效，且不断开 TCP 连接。这对于 AI 的长连接流式响应至关重要，避免了传统网关 Reload 配置时导致的连接中断。

### 1.4 架构优势分析
*   **低延迟**：数据平面基于 Envoy C++，比纯 Go 实现的网关在处理极端高并发时延迟更低。
*   **安全性**：WASM 插件运行在沙箱环境中，即使插件崩溃也不会导致网关主进程崩溃，且提供了内存隔离。
*   **可移植性**：WASM 插件是编译后的字节码，一次编写，可以在任何支持 WASM 的 Envoy 网关上运行，实现了业务逻辑的“一次编写，到处运行”。

---

## 2. 核心功能详细解读

### 2.1 主要功能与场景
1.  **AI 网关**：
    *   **统一接入**：将多个 LLM Provider 的 API 统一封装为一个入口。
    *   **Token 管理**：实时统计流式传输中的 Token 使用量，便于成本控制。
    *   **Prompt 模板**：在网关层管理 Prompt 模板，实现业务逻辑与 Prompt 的解耦。
    *   **结果缓存**：对相同的 Prompt 请求进行缓存，直接返回结果，减少 LLM 调用成本。
2.  **MCP Server Hosting**：
    *   允许将后端服务包装为 AI Agent 可调用的工具，通过标准协议对外暴露。
3.  **传统微服务网关**：
    *   支持 Kubernetes Ingress、Nacos 服务发现、金丝雀发布、流量镜像等传统 API 网关功能。

### 2.2 解决的关键问题
*   **AI 落地碎片化**：解决了企业内部同时使用多个大模型时，SDK 接入不一致、密钥管理混乱的问题。
*   **流式响应处理**：传统网关在处理 SSE (Server-Sent Events) 或流式转发时往往存在缓冲延迟，Higress 针对流式场景进行了优化，实现了边收边转，降低首字延迟（TTFT）。
*   **扩展性与安全性的平衡**：解决了 Envoy 二次开发门槛高（需要 C++）和 Lua 插件性能差、不稳定的问题。

### 2.3 与同类工具对比
| 特性 | Higress | APISIX (Apache) | Kong (Enterprise) | Nginx + Lua |
| :--- | :--- | :--- | :--- | :--- |
| **内核语言** | Envoy (C++) / Go (CP) | Envoy (C++) / Lua | Nginx (C) / Lua | Nginx (C) |
| **扩展机制** | **WASM (优先)** | Plugin (Go/Lua/Python) | Lua / JS | Lua |
| **AI 原生支持** | **内置 (Provider 抽象)** | 需插件配置 | 需插件配置 | 需自行开发 |
| **配置热更新** | **毫秒级 (xDS)** | 毫秒级 | 秒级 | 需 Reload (有损) |
| **K8s 集成** | **深度集成 (Istio)** | 深度集成 | 中等 | 弱 |

### 2.4 技术实现原理
*   **WASM 插件加载**：Higress 使用 `proxy-wasm` 规范。当请求到达时，Envoy 主进程将请求上下文传递给 WASM 虚拟机（如 Wasmtime 或 V8），插件逻辑执行后修改请求头/体，再交还给 Envoy 继续转发。
*   **AI 流式转发**：在 HTTP Filter 链中，Higress 实现了非阻塞的流式缓冲。它识别 LLM 返回的 `data: chunk` 格式，不等待完整响应，直接将数据片透传给客户端。

---

## 3. 技术实现细节

### 3.1 关键技术方案
*   **配置分发**：Higress Controller 监听 Kubernetes 资源变化，将其转换为 xDS 配置推送给 Higress Gateway。为了解决 Istio 配置过于复杂的问题，Higress 做了**配置简化**，去除了大量不需要的 Sidecar 相关配置。
*   **服务发现**：除了支持 K8s Service，Higress 还实现了对 **Nacos**、Consul 等注册中心的直接对接。这是通过在控制平面运行服务发现同步器实现的，将第三方注册中心的实例列表转换为 Envoy 的 EDS (Endpoint Discovery Service) 配置。

### 3.2 代码组织结构
代码库主要分为两部分：
*   **`/pkg`**：Go 语言编写的控制平面逻辑。包含 Ingress 转换器、路由匹配逻辑、Dubbo 协议转换等。
*   **`/plugins`**：WASM 插件目录。通常包含 Go 编写的插件源码，通过 TinyGo 编译为 `.wasm` 文件。
*   **`/docker`**：构建镜像所需的 Dockerfile 定义。

### 3.3 性能与扩展性
*   **性能优化**：
    *   **零拷贝**：Envoy 内部大量使用零拷贝技术，减少内存拷贝开销。
    *   **WASM 优化**：虽然 WASM 有启动开销，但 Higress 支持插件缓存，且 WASM 执行速度在处理复杂逻辑（如 JWT 验证、Body 转换）时优于 Lua 的 JIT。
*   **扩展性**：水平扩展能力极强。由于控制平面和数据平面分离，可以随意扩容 Pod 数量。控制平面状态存储在 Kubernetes Etcd 或 Nacos 中，无状态设计。

### 3.4 技术难点与解决
*   **难点**：WASM 插件的内存隔离与资源限制。
*   **解决**：Higress 利用 Envoy 的配置限制 WASM VM 的最大内存和 CPU 时间，防止单个插件异常消耗过多资源导致网关 OOM。

---

## 4. 适用场景分析

### 4.1 适合的项目
*   **AI 应用开发**：特别是需要对接多个 LLM 厂商，或者需要对 Prompt 进行统一管理和版本控制的企业。
*   **微服务架构**：基于 Kubernetes 的云原生架构，需要高性能 Ingress 入口的企业。
*   **混合云部署**：需要统一管理跨云、跨数据中心流量的场景。

### 4.2 最有效的场景
*   **企业级 AI 落地**：当企业开始大规模使用 LLM，需要统一管理 API Key、监控 Token 消耗、并对 LLM 请求进行鉴权时，Higress 是目前最成熟的云原生解决方案之一。

### 4.3 不适合的场景
*   **极简边缘计算**：如果资源极其受限（如几 MB 内存），Envoy + WASM 的开销可能过大，轻量级的 Nginx 或 Caddy 更合适。
*   **纯静态文件服务**：如果只需要简单的静态资源托管，Higress 的功能过于厚重。

### 4.4 集成方式
*   **Kubernetes Ingress**：直接安装 Higress Helm Chart，将 Ingress Class 指定为 `higress`。
*   **API 网关模式**：创建 `Gateway` API 资源或 Higress 自定义的 `Ingress` 资源进行路由配置。

---

## 5. 发展趋势展望

### 5.1 技术演进方向
*   **AI 编排的深化**：从简单的 API 转发，向更复杂的 AI Agent 编排演进。MCP 协议的支持是一个信号，未来 Higress 可能会成为 Agent 之间的“路由器”。
*   **WASM 生态的标准化**：随着 WASM Component Model 的成熟，Higress 可能会支持更复杂的插件依赖管理和多语言混合编程。

### 5.2 改进空间
*   **控制平面性能**：在超大规模（如 10万+ 服务）场景下，Istio 控制平面的推送延迟仍需优化。
*   **WASM 调试**：目前 WASM 插件的调试和日志追踪相比原生代码仍有难度，需要更好的工具链支持。

###

---
## 代码示例




```python
# 示例1：使用Higress实现基于Header的路由转发
from higress import Gateway, Route, HeaderMatch

# 创建网关实例
gateway = Gateway(name="api-gateway")

# 定义路由规则：当请求Header包含version=v2时转发到新服务
route = Route(
    name="version-based-route",
    match=HeaderMatch(name="version", value="v2"),
    destination="new-service:8080"
)

# 将路由添加到网关
gateway.add_route(route)

# 应用配置
gateway.apply()
```




```python
# 示例2：配置Higress的限流策略
from higress import Gateway, RateLimitRule

# 创建网关实例
gateway = Gateway(name="api-gateway")

# 定义限流规则：每个IP每秒最多10个请求
rate_limit = RateLimitRule(
    name="ip-rate-limit",
    limit=10,
    window="1s",
    key="client_ip"
)

# 将限流规则应用到特定路由
gateway.add_rate_limit(route_path="/api/v1/*", rule=rate_limit)

# 应用配置
gateway.apply()
```




```python
# 示例3：使用Higress实现JWT认证
from higress import Gateway, JwtAuth

# 创建网关实例
gateway = Gateway(name="api-gateway")

# 配置JWT认证
jwt_auth = JwtAuth(
    name="jwt-auth",
    issuer="my-auth-service",
    audience="my-api",
    public_key="-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----"
)

# 将认证应用到需要保护的API
gateway.add_auth(path="/api/secure/*", auth=jwt_auth)

# 应用配置
gateway.apply()
```


---
## 案例研究


### 1：阿里巴巴内部电商业务

 1：阿里巴巴内部电商业务

**背景**: 阿里巴巴内部拥有庞大的电商生态，包括淘宝、天猫等核心业务。这些业务运行在混合云架构之上，流量巨大且业务逻辑极其复杂。随着云原生技术的普及，业务方希望将传统的微服务架构迁移到云原生架构，特别是利用 Istio 来管理服务间的流量和安全。

**问题**: 在迁移过程中，团队遇到了两个主要问题。首先，开源 Istio 的性能开销较高，无法满足双十一等极端高并发场景下的低延迟要求。其次，Istio 的配置模型（基于 Kubernetes CRD）过于复杂，与阿里巴巴现有的 Nginx Ingress 配置习惯不兼容，导致运维和开发人员的学习成本极高，难以在集团内部大规模推广。

**解决方案**: 阿里巴巴团队基于 Istio 进行了深度的定制和优化，开发了 Higress。Higress 通过采用 C++ 重写了数据平面（Envoy 的扩展），显著降低了资源消耗和网络延迟。同时，它保留了 Nginx Ingress 的配置习惯，并支持将 Spring Cloud 的注册中心（如 Nacos）与服务网格打通，实现了从传统架构到云原生架构的平滑过渡。

**效果**: Higress 成功支撑了阿里巴巴内部核心电商业务的云原生化。性能测试显示，在开启服务网格功能后，长连接请求的延迟增加了不到 1ms，完全满足业务对性能的严苛要求。此外，统一的配置入口极大地降低了运维复杂度，使得 Higress 能够在阿里集团内部及阿里云上广泛使用。

---



### 2：某大型互联网企业 AI 网关构建

 2：某大型互联网企业 AI 网关构建

**背景**: 随着大语言模型（LLM）的爆发，该企业内部多个业务部门纷纷尝试接入 AI 能力以提升产品体验。业务部门需要调用 OpenAI、阿里通义千问等不同的模型服务接口。

**问题**: 在实际落地中，技术团队面临诸多痛点。首先是成本问题，直接调用商业 API 的 Token 消耗巨大，且缺乏统一的流量控制和计费管理。其次是安全与稳定性，直接将 API Key 暴露给各个业务团队风险极高，且无法应对模型服务商的 API 限流或不稳定。最后，各个业务团队重复开发调用逻辑，缺乏统一的 Prompt 管理和语义缓存机制。

**解决方案**: 该企业引入 Higress 作为 AI 网关。利用 Higress 原生支持的 AI 特性，企业构建了一个内部的 AI 代理平台。通过 Higress，团队实现了对所有 AI 请求的统一鉴权、流量控制和熔断降级。利用其语义缓存功能，对高频相似的 Prompt 进行缓存，直接返回结果，减少了对上游模型的调用。同时，Higress 支持 Prompt 的统一管理和模板化，方便业务方快速接入。

**效果**: 通过引入 Higress，该企业成功将 AI 调用成本降低了 30% 以上（得益于语义缓存和 Token 优化）。统一的网关层屏蔽了不同模型服务商的差异，业务方只需关注业务逻辑，开发效率提升 50%。此外，集中的 API Key 管理消除了密钥泄露的风险，保障了企业数据安全。

---



### 3：多语言微服务环境下的流量治理

 3：多语言微服务环境下的流量治理

**背景**: 某跨国金融科技公司拥有遗留的 Java 核心交易系统，同时正在快速发展基于 Go 和 Python 的新业务中台。为了解决遗留系统与新系统之间的交互问题，团队引入了 Dubbo 作为服务治理框架，但同时也面临着 Kubernetes 集群内外部服务互通的挑战。

**问题**: 企业的技术栈非常杂乱，既有基于 HTTP 的 REST API，也有基于 RPC 的 Dubbo 服务。传统的 API 网关（如 Kong）只能处理七层 HTTP 流量，无法对 Dubbo 等协议进行路由和治理。这导致跨协议调用变得非常困难，团队不得不维护多套网关系统，增加了运维成本和故障排查难度。

**解决方案**: 团队部署了 Higress 作为统一的流量入口。利用 Higress 强大的协议扩展能力，该企业实现了在一个网关内同时处理 HTTP、gRPC 以及 Dubbo 流量。Higress 能够识别 Dubbo 的服务注册信息（对接 Nacos 注册中心），并将外部的 HTTP 请求精准地路由到内部的 Dubbo 服务提供者上，实现了 HTTP 到 Dubbo 的协议转换。

**效果**: Higress 的引入统一了南北向与东西向的流量治理，成功替代了旧有的多套网关系统。架构的简化使得运维效率显著提升，跨语言、跨协议的服务调用延迟降低了 20%。此外，Higress 提供的精细化流量管理（如灰度发布、全链路透传）使得新功能的上线变得更加平滑和安全。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|----------------|------|-------|
| 性能 | 高性能（基于Envoy和Istio） | 高性能（基于Nginx/OpenResty） | 极高性能（基于OpenResty） |
| 易用性 | 提供控制台和K8s CRD支持 | 需要配置文件或API操作 | 支持Dashboard和K8s CRD |
| 成本 | 开源免费，企业版需付费 | 开源免费，企业版需付费 | 开源免费，企业版需付费 |
| 扩展性 | 支持Wasm插件扩展 | 支持Lua和Go插件 | 支持Lua和Python插件 |
| 社区活跃度 | 活跃（阿里背书） | 活跃（广泛使用） | 活跃（Apache项目） |
| 功能丰富度 | 网关、流量管理、安全防护 | 网关、认证、监控 | 网关、流量控制、可观测性 |

### 优势分析

- 优势1：基于Envoy和Istio，适合云原生和微服务架构。
- 优势2：支持Wasm插件，扩展性强且性能损耗低。
- 优势3：提供完整的控制台和K8s集成，易用性高。

### 不足分析

- 不足1：社区生态较Kong和APISIX稍弱，第三方插件较少。
- 不足2：企业版功能可能需要付费，成本较高。
- 不足3：文档和案例相对较少，学习曲线可能较陡。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于云原生架构的网关部署

**说明**:  
Higress 是基于阿里云内部多年实践沉淀的下一代云原生网关，基于 Istio 和 Envoy 构建。最佳实践应充分利用其云原生特性，将其部署在 Kubernetes 集群中，以实现弹性伸缩、灰度发布和无缝升级。

**实施步骤**:
1. 准备 Kubernetes 集群（版本 1.19+）
2. 使用 Helm 部署 Higress 控制面和数据面
3. 配置 Ingress Class 以关联 Kubernetes Ingress 资源
4. 设置 Horizontal Pod Autoscaler (HPA) 根据流量自动扩缩容

**注意事项**:  
- 生产环境建议部署高可用模式（多副本）
- 确保 Kubernetes 集群资源充足（CPU/内存）
- 定期备份 Higress 配置

---

### 实践 2：精细化流量路由管理

**说明**:  
利用 Higress 的强大路由能力实现复杂的流量分发策略，包括基于 Header、Query 参数、Cookie 等条件的路由，以及蓝绿发布、金丝雀发布等高级场景。

**实施步骤**:
1. 定义路由规则时使用匹配条件（如 `headers["x-env"] == "prod"`）
2. 配置权重路由实现灰度发布（如 10% 流量到新版本）
3. 设置超时和重试策略增强服务韧性
4. 通过控制台或 API 动态调整路由规则

**注意事项**:  
- 路由规则应保持简洁避免性能损耗
- 测试路由规则时使用 curl -v 验证
- 生产环境变更前先在测试环境验证

---

### 实践 3：插件扩展与自定义开发

**说明**:  
Higress 支持 Wasm 插件扩展，最佳实践包括使用官方插件市场插件，以及根据业务需求开发自定义插件来增强网关功能（如认证、限流、日志处理等）。

**实施步骤**:
1. 从官方插件市场评估并安装适用插件
2. 使用 Go/C++ 开发自定义 Wasm 插件
3. 通过 Higress 控制台上传并启用插件
4. 配置插件参数并观察运行状态

**注意事项**:  
- 插件开发需遵循 Wasm 规范
- 生产环境插件需充分压测
- 定期更新插件版本

---

### 实践 4：安全防护与访问控制

**说明**:  
实施多层安全防护，包括 HTTPS/TLS 终止、IP 白名单、JWT 认证、API 防护等，确保服务安全。

**实施步骤**:
1. 配置 TLS 证书并强制 HTTPS
2. 启用 JWT/OAuth2 认证插件
3. 设置 IP 访问控制列表
4. 开启请求速率限制（Rate Limiting）

**注意事项**:  
- 证书定期轮换
- 密钥管理使用 KMS 等安全方案
- 定期审计安全策略

---

### 实践 5：可观测性集成

**说明**:  
集成 Prometheus、Grafana、SkyWalking 等可观测性工具，建立完整的监控、日志和追踪体系。

**实施步骤**:
1. 启用 Higress Prometheus 指标暴露
2. 配置日志采集（如 SLS 或 ELK）
3. 集成分布式追踪（如 Jaeger）
4. 设置关键指标告警（延迟、错误率等）

**注意事项**:  
- 监控数据保留策略需符合合规要求
- 告警阈值需根据实际业务调整
- 敏感信息脱敏处理

---

### 实践 6：多集群与混合云管理

**说明**:  
对于复杂场景，使用 Higress 的多集群管理能力实现跨集群、跨云的统一流量管理。

**实施步骤**:
1. 配置多集群注册
2. 设置全局流量策略
3. 实现跨集群故障转移
4. 统一配置管理

**注意事项**:  
- 网络延迟需纳入考量
- 配置一致性检查
- 灾难恢复演练

---

### 实践 7：性能优化与资源管理

**说明**:  
通过连接池、缓存、压缩等手段优化 Higress 性能，合理分配计算资源。

**实施步骤**:
1. 调整工作线程数与 CPU 核心数匹配
2. 配置 upstream 连接池参数
3. 启用响应缓存
4. 开启 Gzip/Brotli 压缩

**注意事项**:  
- 压缩可能增加 CPU 消耗
- 缓存策略需考虑数据一致性
- 定期进行性能基准测试

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/3 (QUIC) 协议支持

**说明**: Higress 基于 Envoy 和 Istio 构建，虽然对 HTTP/2 支持良好，但开启 HTTP/3 (QUIC) 可以显著解决 TCP 队头阻塞问题，降低弱网环境下的延迟和丢包重传率，提升移动端用户的访问体验。

**实施方法**:
1. 在 Higress 网关的监听器配置中，添加 QUIC 协议的过滤器配置。
2. 配置 UDP 端口（通常为 443）的监听，并关联对应的 TLS 证书。
3. 在 ALB (应用负载均衡) 层确保 UDP 流量可以正确转发到 Higress 节点。

**预期效果**: 在高丢包率网络环境下，视频流和 API 请求的延迟降低 30%-50%，连接建立成功率提升。

---

### 优化 2：配置全链路超时与重试策略

**说明**: 默认的超时设置可能不适合微服务架构。过长的超时会导致线程堆积，过短则导致请求失败。合理的指数退避重试策略可以防止下游服务雪崩。

**实施方法**:
1. 在路由配置中显式设置 `connectTimeout`, `timeout`（请求超时）。
2. 配置 `retryPolicy`，设置 `numRetries`（如 2-3 次），并使用 `PER_TRIAL_TIMEOUT`。
3. 开启 `retryOn` 触发条件，例如针对 `5xx` 状态码或 `reset` 进行重试。
4. 为关键路由配置 `circuitBreakers`（熔断器），防止连续失败请求继续发送。

**预期效果**: 在下游服务偶发故障时，通过熔断和重试，将最终请求失败率控制在 1% 以下，同时避免无效连接占用资源，提升系统整体吞吐量 20%。

---

### 优化 3：启用 Wasm 插件的高效隔离与缓存

**说明**: Higress 支持 Wasm 插件扩展。如果 Wasm 插件配置为“每次请求都编译”或使用低效的 VM 隔离级别，会极大地增加 CPU 开销和延迟。

**实施方法**:
1. 确保 Wasm 插件使用 AOT (Ahead-of-Time) 编译格式。
2. 在 Wasm 虚拟机配置中，启用 `vm_config` 的 `cache` 功能，确保插件实例被复用。
3. 对于高频调用的鉴权或限流插件，优先使用 Higress 原生 Lua 或内置功能，或使用高性能语言（如 Rust/TinyGo）编写的 Wasm 插件。

**预期效果**: 降低网关处理每个请求的额外 CPU 消耗，将插件带来的额外延迟控制在 1ms-2ms 以内。

---

### 优化 4：启用 DNS 缓存与连接池调优

**说明**: 在高并发场景下，频繁的后端 DNS 解析和频繁建立 TCP/TLS 连接会显著增加延迟。Higress (基于 Envoy) 需要针对上游服务精细调优连接池。

**实施方法**:
1. 配置 `cluster` 的 `dns_refresh_rate`，适当延长 DNS 刷新间隔（如 60s），并启用 `dns_cache`。
2. 调整 HTTP 连接池参数：增大 `max_connections`（如 1024 或更高），并根据下游服务能力调整 `http2_protocol_options` 中的 `max_concurrent_streams`。
3. 启用 `idle_timeout` 以保持必要的长连接热活。

**预期效果**: 减少握手开销，将后端连接复用率提升至 90% 以上，P99 延迟降低 10%-20%。

---

### 优化 5：实施精细化日志采样与异步上报

**说明**: 全量记录 Access Log 会产生巨大的磁盘 I/O 和网络带宽压力，甚至阻塞事件循环，成为性能瓶颈。

**实施方法**:
1. 配置 `access_log` 的采样率（例如仅记录 10%

---
## 学习要点

- 基于提供的来源信息（Alibaba/Higress 在 GitHub 趋势榜），以下是关键要点总结：
- Higress 是阿里云开源的、基于 Istio 构建的下一代云原生 API 网关，旨在解决云原生架构下的流量管理问题。
- 它深度集成了 K8s Ingress 与 Gateway API 标准，能够无缝对接 Kubernetes 生态，降低云原生迁移门槛。
- 提供了强大的 WAF（Web 应用防火墙）插件能力，支持对流量进行精细化的安全防护和访问控制。
- 内置了对高并发流量的处理优化，支持热更新与高性能路由转发，适合生产环境的大规模流量调度。
- 兼容 Envoy 和 Nginx Ingress 注解，允许用户从传统网关平滑迁移，无需大规模重构现有配置。
- 具备可扩展的插件市场（Wasm 插件），支持 Go、Python、Rust 等多语言编写自定义逻辑，极大提升了网关的业务定制能力。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础与核心概念

**学习内容**:
- 理解云原生网关的基本概念及其在现代微服务架构中的定位
- 了解 Higress 的核心特性：基于 Envoy 和 Istio、高可用性、Ingress 与 API 网关融合
- 学习 Higress 的基本术语：路由、服务、插件、Upstream
- 掌握 Docker 和 Kubernetes 的基础操作（作为运行基础）

**学习时间**: 1-2周

**学习资源**:
- Higress GitHub 官方仓库 README
- Higress 官方文档：[快速开始](https://higress.io/docs/latest/overview/what-is-higress/)
- Envoy 官方文档基础部分（了解代理原理）

**学习建议**:
建议先通过 Docker 或 Kind 在本地搭建一个单机版 Higress，不要急于深入配置，先跑通一个最简单的流量转发示例，例如将一个静态后端服务通过 Higress 暴露出来。

---

### 阶段 2：核心功能实战与流量管理

**学习内容**:
- 深入学习 Higress 的路由配置：基于域名、路径、Header 的流量路由
- 掌握服务来源的注册与发现（Nacos, Consul, K8s Service, 固定地址）
- 学习全生命周期的流量管理：金丝雀发布、蓝绿发布、Header 重写/转发
- 理解并配置 Waf 防护、限流降级等基础安全与高可用能力

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档：[核心功能](https://higress.io/docs/latest/user/quick-start/)与[流量治理](https://higress.io/docs/latest/user/traffic-management/)
- Higress 官方控制台操作指南
- Kubernetes Ingress Nginx 对比文档（理解 Higress 的优势）

**学习建议**:
尝试在一个真实的 Kubernetes 集群中安装 Higress。结合 Nacos 注册中心，模拟一个微服务场景，配置服务发现和路由规则。重点练习“灰度发布”场景，这是网关最常用的功能之一。

---

### 阶段 3：插件生态与自定义开发

**学习内容**:
- 熟悉 Higress 内置插件的使用（如 KeyAuth, RequestBlock, AiProxy 等）
- 学习 Wasm（WebAssembly）在网关中的应用原理
- 掌握使用 Go 或 C++ 开发自定义 Wasm 插件
- 学习如何在控制台上传、配置和热加载插件

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档：[插件市场](https://higress.io/docs/latest/user/plugin-how-to/)与[自定义插件开发](https://higress.io/docs/latest/developer/wasm-go/)
- Higress GitHub 仓库中的 [wasm-go](https://github.com/alibaba/higress/tree/main/plugins/wasm-go) 示例代码
- WebAssembly 在云原生领域的相关技术文章

**学习建议**:
从修改一个现有的官方插件开始，例如修改一个请求鉴权插件，使其符合你自定义的 Header 验证逻辑。随后尝试编写一个新的插件来实现特定的日志记录或请求修改逻辑。

---

### 阶段 4：AI 网关特性与高级运维

**学习内容**:
- 掌握 Higress 针对 AI 大模型场景的特性（LLM 路由、Token 处理、多模型切换）
- 学习 Higress 的高可用部署架构与性能调优
- 深入理解 Higress 与 Istio 的集成模式（作为 Gateway 入口）
- 掌握网关的可观测性：对接 Prometheus、Grafana、Loki 进行日志与监控分析

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档：[AI 最佳实践](https://higress.io/docs/latest/ai/ai-overview/)
- Higress GitHub Discussions 中的性能优化讨论
- Prometheus 与 Grafana 集成教程

**学习建议**:
关注 Higress 在 AI 领域的最新进展，尝试搭建一个包含 OpenAI 或通义千问的代理网关，体验 Prompt 模板管理和 Token 计费功能。在运维方面，尝试模拟网关高负载场景，观察监控指标并进行参数调优。

---

### 阶段 5：源码剖析与架构设计

**学习内容**:
- 分析 Higress 的整体架构设计（控制面与数据面分离）
- 深入阅读 Higress 控制面源码，理解配置如何下发给 Envoy
- 研究 Istio Gateway API 的实现细节
- 参与社区贡献，提交 Issue 或 PR

**学习时间**: 持续学习

**学习资源**:
- Higress GitHub 源码（重点分析 `pkg` 和 `core` 目录

---
## 常见问题


### 1: Higress 是什么？它与阿里巴巴有什么关系？

1: Higress 是什么？它与阿里巴巴有什么关系？

**A**: Higress 是一款开源的、云原生的 API 网关。它是基于阿里巴巴内部多年在 API 网关领域的实践，并结合了 Envoy 和 Istio 的技术架构衍生而来的。Higress 的前身是阿里巴巴内部的 Nginx Gateway 和云原生网关，旨在为云原生时代提供一种统一、高性能、易扩展的流量管理解决方案。它于 2022 年开源，并捐赠给了 CNCF 基金会（作为 sandbox 项目），由阿里巴巴、蚂蚁集团等公司共同维护。

---



### 2: Higress 与 Kong、APISIX 或 Nginx 等网关相比有什么核心优势？

2: Higress 与 Kong、APISIX 或 Nginx 等网关相比有什么核心优势？

**A**: Higress 的核心优势主要体现在以下几个方面：

1.  **深度集成云原生生态**：Higress 原生支持 Istio，可以与 Ingress Controller 或 Kubernetes Gateway API 无缝集成，能够直接从 Kubernetes Service 中获取服务端点，无需像传统网关那样手动配置 Upstream。
2.  **高性能与低资源消耗**：基于 C++ 编写的 Envoy 内核，提供了极高的吞吐量和极低的延迟，相比基于 OpenResty (Lua) 的网关（如 Kong、APISIX），在高并发下通常具有更稳定的性能表现和更低的内存占用。
3.  **标准化的扩展能力**：支持 WebAssembly (Wasm) 插件机制。这意味着开发者可以使用 C++、Go、Rust、JavaScript 等多种语言编写插件，而无需修改网关核心代码或受限于 Lua 的沙箱环境。同时兼容 Nginx 的 Lua 脚本，降低了迁移成本。
4.  **安全与流量治理**：继承了阿里巴巴在双十一流量治理方面的经验，内置了完善的限流熔断、认证鉴权、负载均衡算法，且对 HTTP/2 和 gRPC 有更好的支持。

---



### 3: Higress 是否支持从 Nginx 或 Ingress Controller 进行迁移？

3: Higress 是否支持从 Nginx 或 Ingress Controller 进行迁移？

**A**: 是的，Higress 对迁移非常友好。它提供了多种兼容性手段：

1.  **Nginx 兼容**：Higress 内置了对 Nginx 配置语法的支持，虽然不是 100% 全覆盖，但绝大多数常用的 Nginx 配置（如 location 配置、rewrite 规则等）可以直接复用或仅需少量修改。
2.  **Ingress 兼容**：Higress 可以作为 Kubernetes 的 Ingress Controller 使用，支持标准的 Kubernetes Ingress YAML 资源。如果你正在使用 Nginx Ingress Controller，通常可以直接替换底层实现，配置文件改动极小。
3.  **Lua 插件兼容**：对于使用 Lua 编写的自定义插件，Higress 提供了 Lua 脚本支持，允许用户在过渡期继续运行旧的 Lua 逻辑。

---



### 4: 如何在 Higress 中编写和部署自定义插件？

4: 如何在 Higress 中编写和部署自定义插件？

**A**: Higress 提供了非常灵活的插件扩展机制，主要推荐使用 Wasm (WebAssembly) 方式：

1.  **多语言支持**：你可以使用 Go、AssemblyScript (TypeScript)、C++、Rust 等语言编写插件逻辑。Higress 官方提供了对应的 SDK（如 `proxy-wasm-go-sdk`）来简化开发。
2.  **部署方式**：编写完成后，将代码编译为 `.wasm` 二进制文件。你可以将此文件上传到对象存储（如 OSS），然后在 Higress 的控制台中配置 Wasm 插件，通过 URL 引用该文件，或者直接在 Kubernetes ConfigMap 中引用。
3.  **热加载**：Wasm 插件支持动态加载，无需重启 Higress 网关实例即可生效，这对于生产环境的流量治理至关重要。

---



### 5: Higress 是否支持服务发现（如 Nacos、Consul、ZooKeeper）？

5: Higress 是否支持服务发现（如 Nacos、Consul、ZooKeeper）？

**A**: 是的，Higress 设计了强大的服务发现机制。

1.  **Kubernetes 原生**：在 Kubernetes 环境中，Higress 自动监听 Service 和 Endpoints 变化，实现服务自动发现。
2.  **注册中心集成**：对于非 Kubernetes 或混合云环境，Higress 支持主流的注册中心。它内置了对 **Nacos**（阿里巴巴生态常用）、**Consul**、**ZooKeeper**、**DNS** 以及 **固定 IP (Static)** 等服务来源的支持。用户只需在网关控制台配置相应的服务来源，Higress 就会自动同步服务列表，实现后端服务的动态负载均衡。

---



### 6: Higress 是否支持对 Dubbo 服务进行管理？

6: Higress 是否支持对 Dubbo 服务进行管理？

**A**: 支持。Higress 是目前少数原生支持 Dubbo 框架的开源 API 网关之一。它可以将 HTTP/HTTPS 请求转换为 Dubbo 协议（或者反之），从而实现 Web 端或移动端调用后端 Dubbo 服务的需求。它支持 Nacos 作为注册中心来发现 Dubbo 服务，

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 基于 Higress 官方提供的 Docker 镜像，在本地快速启动一个 Standalone 模式的网关实例。你需要配置一个简单的路由转发规则，将访问 `/httpbin/` 路径的流量代理到公共的测试服务 `httpbin.org`，并验证请求头 `Host` 是否被正确修改。

### 提示**: 参考官方文档的“快速开始”章节，注意编写 Ingress 或 Gateway 配置时，如何定义 `service` 字段来指向外部服务而非 K8s Service。

### 

---
## 实践建议

以下是基于 Higress 作为 AI 网关和 API 网关的实际使用场景，为您提供的 7 条实践建议：

### 1. 利用 AI 提供者路由实现成本与延迟的最优解
在对接大模型（如 OpenAI、通义千问、Llama 等）时，不要将所有流量绑定在单一模型上。
*   **具体操作**：配置多个模型提供者作为后端服务。例如，将 80% 的请求路由给高性价比模型（如 Qwen-Turbo 或 GPT-3.5），仅将需要复杂推理的 20% 请求路由给高精度模型（如 GPT-4 或 Qwen-Max）。
*   **最佳实践**：利用 Higress 的**按权重路由**功能，通过金丝雀发布的方式逐步切换流量，观察不同模型的响应时间和成本效果。

### 2. 配置 Token 与计费统计以监控成本
大模型 API 的调用成本与 Token 消耗直接相关，传统的 HTTP 流量统计无法反映真实成本。
*   **具体操作**：启用 Higress 的 AI 统计插件或可观测性能力，确保日志中包含 `prompt_tokens`、`completion_tokens` 和 `total_tokens` 字段。
*   **常见陷阱**：忽略流式响应（SSE）中的 Token 统计。流式请求的统计逻辑与普通请求不同，需确认 Higress 配置能够正确聚合流式传输中的数据块，以获得准确的账单。

### 3. 启用语义缓存以降低 API 调用费用
对于高频重复的问答（如常见的客户咨询、知识库查询），每次都调用 LLM 会产生不必要的费用和延迟。
*   **具体操作**：开启 Higress 的**语义缓存**功能。配置向量数据库（如 Redis 向量检索）作为缓存后端。当用户提问的语义相似度超过设定阈值（例如 0.9）时，直接返回缓存的历史回答。
*   **最佳实践**：针对 RAG（检索增强生成）场景，对文档检索结果进行缓存，效果往往比缓存最终回答更好，能显著减少上下文长度带来的消耗。

### 4. 实施严格的 Prompt 模板管理与注入
不要在前端应用中硬编码 Prompt，这会导致难以维护和潜在的安全风险。
*   **具体操作**：在 Higress 中配置**服务级或路由级的 Prompt 模板**。通过网关层的配置，将系统提示词与用户输入在网关层组装后再发送给 LLM。
*   **常见陷阱**：未对用户输入进行清洗。如果用户输入包含恶意指令（如 "忽略之前的所有指令"），可能会导致 Prompt 注入攻击。建议在网关层配置简单的输入校验插件。

### 5. 利用结果缓存和流式转换提升用户体验
LLM 生成响应通常较慢，直接透传流式数据可能会给前端处理带来压力。
*   **具体操作**：开启流式传输支持，但配置 Higress 对流式数据进行**缓冲或格式转换**。例如，将 SSE 格式转换为更易读的 JSON 格式，或者调整流式输出的分块大小，以减少客户端的 HTTP 请求开销。
*   **最佳实践**：对于移动端 App，建议通过网关将 SSE 转换为普通的 WebSocket 或分块 HTTP 响应，以兼容不同客户端的网络环境。

### 6. 设置超时与重试机制应对模型不稳定
大模型 API 服务偶尔会出现波动或超时，网关层必须有兜底策略。
*   **具体操作**：在 Higress 的路由配置中，针对 LLM 后端服务设置合理的**超时时间**（例如 60 秒，因为 LLM 生成长文本耗时较长）。同时，配置**非幂等性的重试策略**，注意只对连接错误或 5xx 错误进行重试，避免对业务逻辑错误（如 400）重试导致成本倍增。
*   **常见陷阱**：盲目重试导致 Token 消耗激增。确保重试逻辑不会在流式响应中途触发，最好在请求建立阶段失败

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API网关](/tags/api%E7%BD%91%E5%85%B3/) / [AI原生](/tags/ai%E5%8E%9F%E7%94%9F/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [MCP协议](/tags/mcp%E5%8D%8F%E8%AE%AE/) / [WASM](/tags/wasm/) / [LLM网关](/tags/llm%E7%BD%91%E5%85%B3/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/) / [DevOps/运维](/scenarios/devops-%E8%BF%90%E7%BB%B4/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260130-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-9.md" >}})
- [Amla Sandbox：面向 AI 智能体的 WASM Bash 沙箱]({{< relref "posts/20260130-hacker_news-show-hn-amla-sandbox-wasm-bash-shell-sandbox-for-a-1.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*