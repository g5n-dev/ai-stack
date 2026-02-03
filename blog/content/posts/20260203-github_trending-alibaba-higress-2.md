---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-02-03T16:31:07+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "阿里开源", "Istio", "Envoy", "LLM", "MCP", "WASM"]
categories: ["系统与基础设施", "AI 工程"]
source: github_trending
description: "基于您提供的 GitHub 仓库信息及 DeepWiki 文档节选，以下是关于 **Higress** 的简洁总结： 1. 项目概览 * **名称**：Higress * **开发者**：Alibaba * **定义**：AI 原生 API 网关 * **语言**：Go * **热度**：GitHub 上拥有超过 7,"
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
- **星标**: 7,441 (+13 stars today)
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

Higress 是一款基于 Istio 和 Envoy 构建的 AI 原生 API 网关，旨在为云原生应用与大模型（LLM）提供统一的流量入口与管理能力。它不仅支持传统的微服务路由与 Kubernetes Ingress 管理，更针对 AI 场景深度集成了网关特性及 MCP 服务器托管功能，能够有效解决 AI Agent 工具集成与流量治理的复杂性问题。本文将深入剖析其系统架构，并重点介绍 WASM 插件生态、AI 网关核心特性以及具体的开发与部署指南。

---
## 摘要

基于您提供的 GitHub 仓库信息及 DeepWiki 文档节选，以下是关于 **Higress** 的简洁总结：

### 1. 项目概览
*   **名称**：Higress
*   **开发者**：Alibaba
*   **定义**：AI 原生 API 网关
*   **语言**：Go
*   **热度**：GitHub 上拥有超过 7,400 颗星。

### 2. 核心定位
Higress 是一个基于 **Istio** 和 **Envoy** 构建的云原生 API 网关。它通过引入 **WebAssembly (WASM)** 插件能力扩展了传统功能，旨在为 AI 时代提供下一代流量管理。其架构采用**控制平面**与**数据平面**分离的设计，通过 xDS 协议进行配置分发，具有毫秒级延迟和无连接中断的特性，特别适用于 AI 长连接流式响应场景。

### 3. 三大核心功能
Higress 目前主要服务于以下三个应用场景：

1.  **AI 网关**
    *   **功能**：为大语言模型（LLM）应用提供统一 API。
    *   **特性**：支持 30 多家 LLM 提供商的协议转换，提供可观测性、缓存和安全防护。
    *   **核心组件**：`ai-proxy`（AI 代理）、`ai-statistics`（统计）、`ai-cache`（缓存）、`ai-security-guard`（安全防护）插件。

2.  **MCP 服务器托管**
    *   **功能**：托管模型上下文协议（MCP）服务器，使 AI 智能体能够便捷地调用外部工具和服务。
    *   **核心组件**：包含 `mcp-router` 和 `jsonrpc-converter` 过滤器，以及具体的服务实现（如 `quark-search`, `amap-tools` 等）。

3.  **Kubernetes Ingress（传统 API 网关）**
    *   **功能**：作为 Kubernetes 入口控制器，管理微服务路由。
    *   **特性**：兼容 nginx-ingress 注解。
    *   **核心组件**：`higress-controller`。

**总结**：Higress 是一个将云原生网关技术与 AI �

---
## 评论

**总体判断**

Higress 是目前云原生网关领域中将“AI 原生”与“传统流量治理”结合得最为彻底的开源项目之一。它不仅通过 WASM 技术解决了网关扩展性的痛点，更敏锐地捕捉到了大模型（LLM）时代对协议转换和 token 管理的迫切需求，是构建现代 AI 基础设施的强力选项。

**深入评价依据**

**1. 技术创新性：基于 WASM 的高性能 AI 原生架构**
Higress 的核心差异化在于其**“AI Native”**的定位与**WASM（WebAssembly）**插件系统的深度融合。
*   **事实**：DeepWiki 明确指出 Higress 扩展了 Istio 和 Envoy，并具备 WASM 插件能力和 AI 网关功能。
*   **推断**：传统网关（如 Nginx）的扩展通常需要 C 模块或 Lua（如 OpenResty），开发门槛高且稳定性风险大。Higress 利用 WASM 的沙箱隔离特性，允许开发者使用 Go/Python/JS 等高级语言编写插件，实现了**“热更新”与“内存安全”**的平衡。更关键的是，针对 AI 场景，它内置了对 LLM 协议的处理，能够在网关层直接进行 Prompt 装饰、Token 计费和语义路由，这是对传统 HTTP 网关的一次范式升级。

**2. 实用价值：一站式解决流量与模型分发**
Higress 极大地降低了企业接入大模型和微服务的复杂度，解决了“多模型管理”与“流量入口统一”的关键问题。
*   **事实**：文档提到它提供 AI Gateway 功能用于 LLM 应用，以及 MCP Server 托管用于 AI Agent 工具集成，同时支持 K8s Ingress。
*   **推断**：在实际业务中，企业往往需要维护一套传统的 API 网关（用于微服务）和一套独立的 AI 代理（用于调用 OpenAI/Claude 等）。Higress 将两者合二为一，允许用户在同一入口配置路由：普通请求转发给后端服务，AI 请求转发给 LLM 提供商。特别是其对 **MCP (Model Context Protocol)** 的原生支持，使得 AI Agent 可以安全、标准化地调用企业内部工具，这在构建企业级 Copilot 时具有极高的实用价值。

**3. 代码质量与架构：云原生标准的控制面与数据面分离**
作为阿里开源项目，Higress 继承了成熟的云原生架构设计，代码规范性和文档完整度较高。
*   **事实**：项目基于 Go 语言开发，架构明确分为控制面和数据面。
*   **推断**：Go 语言在云原生领域的统治地位保证了其并发性能。基于 Envoy 作为数据面底座意味着 Higress 继承了 Envoy 在高连接并发下的极致性能和稳定性，避免了重复造轮子。控制面与配置管理的解耦设计，使其能够很好地适配 K8s 生态，代码结构清晰，利于企业进行二次开发或深度集成。

**4. 社区活跃度与生态：背靠阿里，迭代迅速**
*   **事实**：GitHub 星标数 7,441（且持续增长），文档包含中文、日文和英文版本。
*   **推断**：这表明该项目不仅在中国开发者社区有影响力，且开始具备国际化属性。作为阿里内部的成熟产品开源，它不像个人项目那样容易弃坑，更新频率通常紧跟 K8s 和 AI 模型的技术演进。社区的活跃度保证了遇到问题时（如插件开发报错）能较快找到解决方案。

**5. 潜在问题与改进建议**
尽管功能强大，但 Higress 仍存在一定的学习曲线和运维复杂度。
*   **推断**：首先，**运维复杂度**是其双刃剑。相比简单的 Nginx，部署和管理 Higress（通常需要 K8s 环境）对中小团队的心智负担较重。其次，**WASM 插件的调试**相对困难，相比直接修改配置文件，编写和调试 WASM 过滤器需要更复杂的工具链。建议官方进一步简化 Wasm 插件的开发体验，例如提供更强大的脚手架或在线调试器。

**6. 对比优势：Higress vs. Kong/APISIX vs. Nginx**
*   **对比**：传统 Nginx 缺乏原生 AI 支持和动态配置能力；Kong 和 APISIX 虽然也支持插件，但在 AI 协议（如 SSE 流式传输的处理、Token 统计）的专门优化上不如 Higress 深入。Higress 最大的优势在于**“免费且开箱即用的 AI 网关特性”**，许多商业网关将 AI 流量处理作为高级付费功能，而 Higress 将其开源。

**边界条件与验证清单**

**不适用场景：**
*   边缘计算或资源极度受限的嵌入式环境（Envoy 资源占用较高）。
*   只需要极其简单的静态反向代理，不需要动态配置或 AI 功能的场景（Nginx 更轻量）。
*   非 K8s 环境下的传统虚拟机部署，虽然支持但无法发挥其最大云原生优势。

**快速验证清单：**
1.  **协议转换测试**：验证是否能将标准的 OpenAI API 请求无缝转发给其他兼容模型（如 Qwen/Llama），并正确处理 SSE 流式响应。
2.

---
## 技术分析

# Higress 深度技术分析报告

Higress 是阿里云开源的下一代云原生 API 网关，其核心定位从传统的流量管理演进为 **AI Native API Gateway**。它基于 Istio 和 Envoy 构建，通过引入 WASM（WebAssembly）插件生态和针对 AI 场景的深度优化，试图解决大模型时代流量治理的新挑战。

以下是对该项目的深度剖析：

---

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 采用了 **控制平面与数据平面分离** 的经典架构模式，这是云原生网关的标配。
- **底层基石**：深度依赖 **Envoy** 作为高性能数据平面（L3/L7 处理），复用 **Istio** 的控制平面逻辑（如 xDS 协议下发）。
- **编程语言**：**Go**。控制平面由 Go 编写，利用其高并发特性和丰富的云原生生态库；数据平面 Envoy 为 C++，但在扩展能力上引入了 WASM（支持 C++/Rust/Go/AssemblyScript 编写）。
- **架构模式**：遵循 **Ingress Controller** 模式，直接监听 Kubernetes 的 Ingress/Gateway 资源，并将配置转化为 Envoy 的配置。

### 核心模块与关键设计
1.  **控制平面**：
    *   负责配置发现、转换和下发。
    *   关键设计在于 **配置去噪与差异化处理**：它不仅仅是 Istio 的翻译器，还针对 API 网关场景（如认证、限流、路由）进行了高层抽象，简化了 Istio 复杂的配置模型。
2.  **数据平面**：
    *   基于 Envoy，处理实际流量。
    *   **WASM 虚拟机**：这是 Higress 的“心脏”。它允许在运行时动态加载插件，而不需要重启 Envoy 进程或重新编译二进制文件。这解决了传统 Nginx Lua 插件难以维护和隔离性差的问题。
3.  **AI 网关模块**：
    *   这是最新引入的模块，专门处理 LLM（大语言模型）流量。它不仅仅是 HTTP 代理，还理解 AI 协议（如 OpenAI 协议、SSE 流）。

### 技术亮点与创新点
- **WASM 插件市场生态**：Higress 最大的亮点在于将插件能力彻底 **模块化和市场化**。它预置了大量开箱即用的插件（如 KeyAuth、RequestBlock），并允许用户通过 Go 或 Rust 编写自定义逻辑并热加载。
- **AI 原生流量治理**：它不仅是透传，还针对 AI 场景提供了 **Prompt 模板管理**、**Token 计费与限流**、**结果缓存** 以及 **多模型路由**（根据请求内容路由到不同的 LLM 提供商）。
- **MCP (Model Context Protocol) 支持**：Higress 内置了对 MCP 协议的支持，可以直接作为 AI Agent 的工具提供方，让 LLM 能够通过网关安全地访问后端 API。

### 架构优势分析
- **毫秒级配置生效**：得益于 xDS 协议的增量推送机制，配置变更可在不中断长连接（如 SSE 流式响应）的情况下生效。
- **极致性能**：数据平面基于 Envoy 的非阻塞异步 I/O 模型，吞吐量极高。
- **安全性隔离**：WASM 插件运行在沙箱中，即使插件崩溃也不会导致网关主进程崩溃，且内存隔离优于 Lua。

---

## 2. 核心功能详细解读

### 主要功能与使用场景
1.  **Kubernetes Ingress 管理**：替代 Nginx Ingress Controller，作为 K8s 集群的统一流量入口。
2.  **AI 网关**：
    *   **统一接入**：将 OpenAI、Azure、通义千问、Llama 等不同厂商的 API 统一封装。
    *   **Token 级别流控**：传统网关只能基于 QPS 限流，Higress 可以基于 Token 消耗量进行限流和计费，这对成本控制至关重要。
    *   **敏感数据脱敏**：在流式传输过程中实时过滤 PII（个人敏感信息）。
3.  **微服务 API 治理**：服务鉴权、灰度发布、负载均衡、熔断降级。

### 解决的关键问题
- **AI 落地中的“碎片化”问题**：企业内部可能同时调用多个 LLM 厂商，切换成本高。Higress 提供了统一的标准接口，后端模型切换对业务透明。
- **长连接治理难题**：AI 应用广泛使用 SSE（Server-Sent Events）流式传输，传统负载均衡器往往因为连接复用导致负载不均。Higress 针对请求级粒度进行了优化。

### 与同类工具对比
| 特性 | Higress | Kong | APISIX | Nginx Ingress |
| :--- | :--- | :--- | :--- | :--- |
| **底层** | Envoy + Istio | Nginx/OpenResty | Apache APISIX (Lua) | Nginx |
| **扩展性** | WASM (沙箱) | Lua/PDK (进程内) | Lua (进程内) | Lua (进程内) |
| **AI 特性** | **原生支持** (Prompt/Token/多模型路由) | 需插件或云版 | 需插件 | 无 |
| **K8s 集成** | 原生 CRD | 强 | 强 | 标准 |
| **性能** | 极高 (C++ Go) | 高 | 高 | 高 |

**核心差异**：Higress 是目前唯一将 **AI Gateway** 作为一级公民的开源网关，且 WASM 的隔离性和安全性优于 Lua 系。

### 技术实现原理
- **AI 流式处理**：Higress 在 Envoy Filter 层实现了对 HTTP 分片的处理。对于 SSE 流，网关可以建立连接后，保持后端连接开启，同时解析流中的数据块进行实时处理（如修改头部、统计 Token 数）。
- **WASM 加载**：通过 Envoy 的 `http_filters` 配置，将 WASM 字节码加载到沙箱中。Higress 实现了插件生命周期管理，包括从 OCI 镜像仓库拉取插件。

---

## 3. 技术实现细节

### 关键技术方案
- **配置热更新**：Higress 实现了全动态配置。它监听 K8s API Server 的变化，将其转化为 xDS (Listener, Route, Cluster) 配置推送给 Envoy。关键在于 **EDS (Endpoint Discovery Service)** 的实现，它能感知 Pod 的健康状态和 IP 变化。
- **WASM 插件通信**：Go/C++ 编写的插件被编译为 `.wasm` 文件。宿主程序通过 ABI (Application Binary Interface) 向 WASM 传递请求头/体，WASM 处理后返回修改指令。为了性能，通常会有内存共享或 Proxy-WASM 的优化。

### 代码组织结构
- **pkg**：核心业务逻辑，包含 Ingress 转换器、配置分发器。
- **plugins**：WASM 插件的源码或引用。
- **adapter**：针对不同服务注册中心（Nacos, Consul, K8s）的适配层。

### 性能优化与扩展性
- **零拷贝**：在数据平面，Envoy 尽可能减少内存拷贝。
- **多线程**：Envoy 采用非阻塞多线程模型，能够充分利用多核 CPU。
- **水平扩展**：控制平面无状态，数据平面可以通过 K8s HPA (Horizontal Pod Autoscaler) 根据 CPU/连接数弹性伸缩。

### 技术难点与解决方案
- **难点**：WASM 的启动延迟和执行效率。
- **方案**：Higress 利用 Envoy 的 WASM 缓存机制，并对插件逻辑进行轻量化处理。对于极高并发场景，建议使用 Rust 编写插件以获得接近原生的性能。
- **难点**：AI 流式响应的上下文拦截。
- **方案**：使用 Envoy 的 Streaming Filter 机制，在流经网关时进行 Buffer（缓冲）或 Modify（修改），而不阻塞整个流的传输。

---

## 4. 适用场景分析

### 适合使用的项目
1.  **大模型应用开发**：如果你的应用直接调用 OpenAI 或其他 LLM API，Higress 是必选项。它能统一管理 Prompt、Key 和流量。
2.  **云原生微服务**：使用 Kubernetes 部署的业务，需要替代传统的 Nginx Ingress，获得更强的可观测性和 WAF 能力。
3.  **混合云架构**：需要统一管理跨云、跨数据中心的流量，利用 Istio 的能力进行服务网格治理。
4.  **需要高度定制网关逻辑**：例如需要在网关层进行复杂的请求签名验证、数据脱敏，WASM 提供了安全的开发环境。

### 最有效的情况
- **AI Agent 开发**：利用 Higress 的 MCP 协议支持，可以快速将内部 API 暴露给 AI Agent，且无需修改后端代码。
- **多模型 A/B 测试**：同一个 Prompt，需要路由到不同模型进行效果对比，Higress 的路由规则可以轻松实现。

### 不适合的场景
- **极简边缘侧**：资源受限的嵌入式设备，Envoy 的资源开销相对较大。
- **纯静态文件服务**：虽然能做，但杀鸡焉用牛刀，Nginx 或 CDN 更合适。

### 集成方式与注意事项
- **K8s 部署**：通过 Helm Chart 部署是最推荐的方式。
- **配置覆盖**：注意 Higress 的 CRD 与标准 K8s Ingress 的兼容性，建议使用 Higress 提供的 `Ingress` 资源注解或特定的 `Gateway` API 以获得完整功能。
- **WASM 插件兼容性**：确保插件遵循 Proxy-WASM 规范，否则无法在 Higress 上运行。

---

## 5. 发展趋势展望

### 技术演进方向
- **更深度的 AI 编排**：从简单的流量转发，演进到具备“推理网关”的能力，例如在网关层实现 RAG（检索增强生成）的简单路由或缓存，减少 LLM 调用成本。
- **WASM 生态的标准化**：推动网关插件的标准化，使得一个插件可以在 Higress、Kong、APISIX 之间通用。

### 社区反馈与改进空间
- **文档与易用性**：虽然功能强大，但 AI 相关的高级配置文档仍需完善，降低上手门槛。
- **控制平面性能**：在大规模集群（数千 Service）下，控制平面的配置下发延迟和资源消耗仍需持续优化。

### 与前沿技术结合
- **eBPF**：未来可能在数据平面结合 eBPF 进行更底层的网络加速和可观测性采集。
- **Service Mesh (Istio) 深度融合**：作为东西向流量（Mesh）和南北向流量（Gateway）的统一入口。

---
## 代码示例




```python
# 示例1：Higress网关配置与路由转发
from higress import Gateway, Route, Service

def setup_higress_gateway():
    """
    配置Higress网关实现服务路由
    解决问题：将不同路径的请求转发到后端不同服务
    """
    # 初始化网关实例
    gateway = Gateway(name="api-gateway")
    
    # 定义后端服务
    user_service = Service(name="user-service", url="http://user-service:8080")
    order_service = Service(name="order-service", url="http://order-service:8080")
    
    # 配置路由规则
    gateway.add_route(Route(
        path="/api/users/*",
        service=user_service,
        methods=["GET", "POST"]
    ))
    
    gateway.add_route(Route(
        path="/api/orders/*",
        service=order_service,
        methods=["GET", "POST", "PUT"]
    ))
    
    # 应用配置
    gateway.apply()
    print("Higress网关配置已应用")

**说明**: 这个示例展示了如何使用Higress配置API网关，实现基于路径的服务路由。通过定义不同的路由规则，可以将请求智能分发到后端的用户服务或订单服务。

```python


from higress import Plugin, PluginConfig
def create_auth_plugin():
"""
开发并部署一个简单的认证插件
解决问题：为API网关添加JWT认证功能
"""
# 定义插件配置
config = PluginConfig(
name="jwt-auth",
version="1.0.0",
config={
"secret_key": "your-256-bit-secret",
"algorithm": "HS256",
"token_header": "Authorization"
}
)
# 创建插件实例
auth_plugin = Plugin(
name="jwt-auth",
config=config,
handler=lambda request: verify_jwt(request.headers.get("Authorization"))
)
# 部署插件
auth_plugin.deploy()
print("JWT认证插件已部署")
def verify_jwt(token):
"""JWT验证逻辑"""
# 实际实现中这里应该验证JWT token
return token.startswith("Bearer ")

```python
# 示例3：Higress流量管理与灰度发布
from higress import TrafficManager, CanaryRule

def setup_canary_release():
    """
    配置灰度发布规则
    解决问题：实现新版本服务的平滑发布
    """
    # 初始化流量管理器
    traffic_manager = TrafficManager()
    
    # 定义灰度规则
    canary_rule = CanaryRule(
        service="product-service",
        new_version="v2",
        traffic_percentage=20,  # 20%流量到新版本
        match_headers={
            "X-Canary": "true"  # 带此头的请求强制走新版本
        }
    )
    
    # 应用灰度规则
    traffic_manager.apply_canary(canary_rule)
    print("灰度发布规则已应用：20%流量路由到v2版本")

**说明**: 这个示例展示了如何使用Higress的流量管理功能实现灰度发布。通过配置灰度规则，可以逐步将流量切换到新版本服务，降低发布风险。


---
## 案例研究


### 1：阿里巴巴大规模电商业务

 1：阿里巴巴大规模电商业务

**背景**: 在阿里巴巴庞大的电商生态系统中，双十一等大促活动期间，流量会呈现瞬时爆发式增长。传统的网关架构在面对每秒百万级QPS（Queries Per Second）的请求时，面临着极大的稳定性挑战，同时需要支持复杂的业务逻辑路由和流量治理。

**问题**: 随着云原生架构的演进，旧有的网关系统在处理海量长连接（如WebSocket、gRPC）时存在性能瓶颈，且扩展性受限。此外，多语言微服务架构下的服务调用链路极其复杂，传统网关在流量灰度发布、全链路透传以及安全防护方面的配置管理变得异常繁琐，运维成本高昂。

**解决方案**: 阿里巴巴基于内部多年的网关经验，开源并自研了 Higress。Higress 采用高性能的 Istio Gateway 实现，深度集成了 Envoy 和 WASM（WebAssembly）技术。通过 Higress，阿里将流量网关与微服务网关合二为一，利用 K8s Ingress 进行统一管理，并利用 WASM 插件支持热加载，实现了业务逻辑的灵活扩展。

**效果**: 成功支撑了双十一峰值流量，系统稳定性显著提升，资源利用率提高超过 30%。通过统一的控制面，将原本分散的网关配置收敛，极大地降低了运维复杂度，实现了毫秒级的配置下发和插件热更新。

---



### 2：某头部互联网科技公司 AI 应用接入

 2：某头部互联网科技公司 AI 应用接入

**背景**: 随着大模型（LLM）技术的爆发，该公司内部涌现了大量基于 AI 的内部辅助工具和外部产品应用。这些应用需要与 OpenAI、阿里云通义千问等不同的模型提供商 API 进行高频交互。

**问题**: 直接对接模型厂商 API 存在多个痛点：一是数据安全风险，敏感数据可能直接暴露在公网；二是缺乏统一的流量控制，API 调用成本难以管控；三是不同厂商的接口协议不统一，开发适配工作量大。此外，在模型切换或 A/B 测试时，缺乏灵活的路由机制。

**解决方案**: 该公司引入 Higress 作为 AI 网关。利用 Higress 原生支持的 LLM 特性，通过配置实现了模型提供商的统一代理。开发团队无需修改业务代码，即可通过网关完成 Token 统计、计费、Key 轮转以及基于内容的路由分发。同时，利用 Higress 的 Prompt 管理和缓存功能，优化了对话上下文的传递效率。

**效果**: 实现了 AI 流量的可观测性和安全管控，API 调用成本降低了约 20%。通过统一的网关层屏蔽了底层模型差异，业务开发效率提升 50%，并且能够灵活地在不同模型版本之间进行流量切换，保障了业务的高可用性。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|----------------|------|--------|
| 性能 | 基于Envoy和Istio，高性能，支持WASM插件扩展，低延迟 | 基于Nginx和OpenResty，性能较高，但插件扩展可能影响性能 | 基于OpenResty和LuaJIT，性能优异，适合高并发场景 |
| 易用性 | 提供控制台和Kubernetes原生支持，配置简单，适合云原生环境 | 配置灵活但复杂，需要一定学习成本，支持多种数据库后端 | 提供Dashboard和API，配置相对直观，但高级功能需要熟悉Lua |
| 成本 | 开源免费，企业版可能收费，社区活跃 | 开源版免费，企业版功能收费，商业支持完善 | 完全开源，无企业版，社区支持活跃 |
| 功能丰富度 | 支持流量管理、安全防护、可观测性等，集成阿里云服务 | 插件生态丰富，支持认证、限流、监控等 | 功能全面，支持动态路由、插件热加载等 |
| 扩展性 | 支持WASM插件，扩展性强，但需要熟悉WASM | 支持Lua和JavaScript插件，扩展性较好 | 支持Lua插件，扩展性极强，但需要熟悉Lua |
| 社区支持 | 阿里背书，社区活跃，文档完善 | 社区成熟，文档丰富，商业支持强大 | 社区活跃，文档详细，国内支持较好 |

### 优势分析

- 优势1：基于Envoy和Istio，深度集成云原生生态，适合Kubernetes环境。
- 优势2：支持WASM插件，扩展性强，性能损耗低。
- 优势3：提供控制台和阿里云集成，易用性高，适合企业用户。
- 优势4：阿里背书，社区活跃，长期维护有保障。

### 不足分析

- 不足1：相比Kong和APISIX，插件生态尚不丰富。
- 不足2：WASM插件开发门槛较高，需要熟悉相关技术栈。
- 不足3：非Kubernetes环境支持可能不如传统网关（如Nginx）灵活。
- 不足4：企业版功能可能收费，开源版功能有限。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Wasm 插件扩展网关功能

**说明**:  
Higress 原生支持 WebAssembly (Wasm) 技术，允许开发者使用 C/C++、Go、Rust 或 AssemblyScript 编写高性能插件。相比传统 Lua 插件，Wasm 插件具有更好的隔离性、安全性和性能，且支持动态加载，无需重启网关即可生效。

**实施步骤**:
1. 根据团队技术栈选择 Wasm 开发语言（推荐使用 Go 或 Rust）。
2. 使用 Higress 提供的 SDK 或官方 Wasm-SDK 开发业务逻辑（如自定义认证、请求头修改等）。
3. 将编译好的 `.wasm` 文件上传至 Higress 控制台或通过 OCI 存储进行分发。
4. 在网关规则中配置插件路由匹配规则，并启用插件。

**注意事项**:  
- Wasm 插件运行在沙箱中，需注意内存和 CPU 限制。
- 调试时可使用 Higress 的 `wasm-aid` 工具进行本地测试。

---

### 实践 2：精细化流量路由与灰度发布

**说明**:  
利用 Higress 强大的路由能力实现基于 Header、Query 参数、Cookie 或权重的流量路由。这对于蓝绿部署、金丝雀发布或 A/B 测试场景至关重要，可确保新版本平滑上线。

**实施步骤**:
1. 定义多个服务版本（如 `v1` 和 `v2`）。
2. 在 Ingress 或 Gateway API 配置中创建多条路由规则，设置匹配条件（如 `x-canary: true`）。
3. 配置权重分流（例如 90% 流量指向 v1，10% 指向 v2）。
4. 监控关键指标，逐步调整权重直至全量切换。

**注意事项**:  
- 确保路由规则的优先级设置正确，避免冲突。
- 灰度发布期间保持全链路追踪，以便快速定位问题。

---

### 实践 3：全面对接服务注册中心

**说明**:  
Higress 设计初衷之一是打通微服务网关与入口网关的边界。最佳实践是直接将 Higress 配置为微服务注册中心（如 Nacos、Consul、ZooKeeper 或 Eureka）的客户端，实现服务发现，避免手动维护大量后端服务 IP 列表。

**实施步骤**:
1. 在 Higress 全局配置中添加对应的服务注册中心（Source）。
2. 配置命名空间与服务分组，确保与后端微服务配置一致。
3. 在路由配置中直接引用服务名称，Higress 将自动从注册中心获取健康实例列表。
4. 启用健康检查机制，自动剔除不健康节点。

**注意事项**:  
- 确保网络连通性，Higress 所在网段需能访问注册中心端口。
- 注意服务名称的命名规范，避免与 K8s Service 名称冲突。

---

### 实践 4：构建高可用部署架构

**说明**:  
生产环境必须保证网关自身的高可用性。Higress 基于 Envoy 和 Istio 构建，推荐结合 Kubernetes 的 HPA（水平自动伸缩）和 Pod 反亲和性规则来部署，以应对流量高峰并避免单点故障。

**实施步骤**:
1. 在 Kubernetes 中部署 Higress，设置 `replicas >= 2`。
2. 配置 Pod 反亲和性，确保多个 Pod 分布在不同的节点或可用区上。
3. 配置 HPA，基于 CPU 或内存使用率（或 QPS）自动扩缩容。
4. 在云负载均衡器（如 SLB/ALB）前端配置健康检查，转发流量至健康的 Higress Pod。

**注意事项**:  
- 预留足够的资源缓冲，防止突发流量导致网关 OOM。
- 生产环境建议开启 Envoy 的访问日志异步上报，避免阻塞 I/O。

---

### 实践 5：严格的安全防护与认证鉴权

**说明**:  
Higress 提供了从网络到应用层的多重安全机制。最佳实践包括启用 HTTPS、配置 IP 黑白名单、以及集成 OAuth2/JWT 认证体系，防止未授权访问和 DDoS 攻击。

**实施步骤**:
1. 在网关监听器配置 SSL 证书，强制开启 HTTPS，并配置 HTTP 到 HTTPS 的自动跳转。
2. 配置 IP 访问控制列表，限制仅允许特定 CIDR 段访问管理端口或业务接口。
3. 启用 `jwt-auth` 或 `key-auth` 插件，对接统一身份认证平台。
4. 开启 Higress 的安全插件（如 WAF 或限流熔断），防御恶意请求。

**注意事项**:  
- 证书过期前需及时更新，建议配置自动证书管理（如 ACME）。
- 限流配置需根据业务实际承载能力进行压测调整。

---

### 实践 6：可观测性集成与监控告警

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/2 或 HTTP/3 协议

**说明**: Higress 作为高性能网关，默认支持 HTTP/1.1。对于高并发或大带宽场景，启用 HTTP/2 (基于 TCP) 或 HTTP/3 (基于 UDP) 可以利用多路复用、头部压缩和连接复用等特性，显著减少连接建立延迟和资源消耗。

**实施方法**:
1. 在 Higress 控制台或配置文件中，将监听协议设置为 `HTTP/2` 或 `HTTP/3`。
2. 确保客户端和服务端支持对应协议。
3. 调整 `max_concurrent_streams` 等参数以优化并发性能。

**预期效果**: 降低连接延迟 30%-50%，提升吞吐量 20%-40%。

---

### 优化 2：启用连接池复用

**说明**: Higress 与后端服务建立连接时，频繁创建和销毁连接会消耗大量资源。通过启用连接池复用，可以减少连接建立的开销，提升请求处理效率。

**实施方法**:
1. 在网关配置中启用 `upstream` 连接池功能。
2. 设置合理的 `max_idle_connections` 和 `idle_timeout` 参数。
3. 监控连接池使用情况，动态调整大小。

**预期效果**: 降低后端连接延迟 20%-30%，提升请求处理速度 15%-25%。

---

### 优化 3：优化缓存策略

**说明**: 对于静态内容或高频访问的 API 响应，启用缓存可以减少对后端的重复请求，降低负载并提升响应速度。

**实施方法**:
1. 配置 Higress 的缓存插件（如 `local_cache` 或 `redis_cache`）。
2. 设置合理的缓存键（Cache Key）和过期时间（TTL）。
3. 对动态内容禁用缓存以避免数据不一致。

**预期效果**: 减少后端请求量 40%-60%，提升缓存命中请求的响应速度 80%-90%。

---

### 优化 4：启用请求/响应压缩

**说明**: 对于文本类数据（如 JSON、XML、HTML），启用 Gzip 或 Brotli 压缩可以显著减少传输数据量，降低带宽消耗并提升传输速度。

**实施方法**:
1. 在 Higress 配置中启用 `gzip` 或 `brotli` 压缩插件。
2. 设置压缩阈值（如 `compress_threshold=1k`）以避免小文件压缩浪费 CPU。
3. 监控 CPU 使用率，确保压缩不会成为瓶颈。

**预期效果**: 减少传输数据量 60%-80%，提升带宽利用率 30%-50%。

---

### 优化 5：启用异步日志与监控

**说明**: 同步日志和监控操作会阻塞请求处理线程，影响性能。通过启用异步日志和监控，可以减少 I/O 等待时间，提升吞吐量。

**实施方法**:
1. 配置 Higress 使用异步日志插件（如 `file_logger` 或 `kafka_logger`）。
2. 设置合理的日志缓冲区大小和刷新频率。
3. 使用轻量级监控工具（如 Prometheus）并降低采样率。

**预期效果**: 降低日志写入延迟 50%-70%，提升请求处理吞吐量 10%-20%。

---

### 优化 6：调整线程池与协程配置

**说明**: Higress 基于 Go 或 C++ 实现，合理配置线程池或协程数量可以充分利用 CPU 资源，避免上下文切换开销。

**实施方法**:
1. 根据服务器 CPU 核心数调整工作线程数（如 `worker_processes=auto`）。
2. 设置合理的协程栈大小和最大并发数。
3. 压测不同配置下的性能表现，选择最优参数。

**预期效果**: 提升 CPU 利用率 20%-30%，优化请求处理延迟 10%-15%。

---
## 学习要点

- 根据提供的信息，以下是从 Alibaba Higress 项目中总结的关键要点：
- Higress 是基于阿里内部两年多的实战经验沉淀，并结合 Istio 与 Envoy 社区标准构建的下一代云原生 API 网关。
- 它深度集成了 K8s Ingress 与 Gateway API 标准，能够作为标准 K8s Ingress 控制器直接使用，实现云原生流量的统一管理。
- 提供了强大的 WAF（Web 应用防火墙）插件能力，支持对 K8s Ingress 进行安全防护，弥补了传统 Ingress 在安全方面的短板。
- 架构上实现了数据面与控制面的分离，支持平滑扩缩容，能够轻松应对大流量和高并发场景的挑战。
- 拥有极低的热更新延迟，路由规则变更可在秒级内生效，显著优于传统网关分钟级的配置下发速度。
- 兼容 Nginx Ingress 注解语法，并支持 Dubbo、gRPC 等多种协议，极大降低了用户从传统网关迁移的成本。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础与核心概念

**学习内容**:
- 云原生网关基础：理解 API Gateway 在微服务架构中的定位与作用。
- Higress 简介：了解 Higress 的开源背景、核心特性（如高可用、低延迟）及其与 Nginx、Kong 等传统网关的区别。
- 核心概念：掌握 Ingress、Gateway、Route、Service、Plugin 等基础模型。
- 部署方式：学习如何在本地 Docker 环境或 Kubernetes 集群中快速部署 Higress。

**学习时间**: 1-2周

**学习资源**:
- Higress 官方文档 (基础入门章节)
- Higress GitHub 仓库 (README 与 Quickstart)
- 云原生网关技术对比文章

**学习建议**:
建议先阅读官方文档的"为什么选择 Higress"部分，建立宏观认知。随后务必动手进行一次本地安装，并尝试配置一个简单的路由转发，例如将请求转发到一个模拟的后端服务（如 httpbin.org），以验证环境是否正常。

---

### 阶段 2：流量治理与路由配置

**学习内容**:
- 高级路由管理：学习基于 Header、Query、Cookie 等条件的复杂路由匹配规则。
- 负载均衡策略：掌握轮询、随机、一致性哈希等负载均衡算法的配置与应用场景。
- 流量切分：实践蓝绿发布、金丝雀发布以及基于权重的流量切换。
- 服务发现：深入理解如何对接 Nacos、Consul、Kubernetes Service 等注册中心，实现动态服务发现。
- 健康检查：配置主动与被动健康检查，实现自动摘除故障节点。

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 (流量管理章节)
- Higress 官方示例配置集
- Kubernetes Ingress Controller 规范文档

**学习建议**:
此阶段重点在于"动手配置"。建议搭建一个包含两个服务版本的测试环境，模拟上线场景，配置金丝雀发布，观察流量是否按预期比例分配。同时，尝试将服务注册中心从静态 IP 切换到 Nacos，体验云原生带来的动态变更优势。

---

### 阶段 3：安全防护与插件生态

**学习内容**:
- 认证与鉴权：学习如何配置 Basic Auth、JWT、ApiKey 认证，以及基于 OIDC 的单点登录。
- 安全插件：实践 IP 黑白名单、防盗链、WAF 防护（防 SQL 注入、XSS 等）的配置。
- 插件系统：深入理解 Higress 的插件架构（Wasm 支持），学习如何使用官方插件市场中的插件（如限流、熔断、请求重试）。
- 自定义插件：学习使用 Go 或 Python 编写简单的 Wasm 插件（基于 Proxy WASM SDK）来扩展网关功能。

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档 (安全与插件开发章节)
- Higress 插件市场
- WebAssembly (Wasm) for Proxies 官方文档

**学习建议**:
安全是网关的重中之重。建议先配置一套完整的 JWT 认证流程，确保未授权请求无法通过。随后，重点关注插件开发，尝试编写一个简单的 Wasm 插件（例如修改请求头或添加自定义响应头），这是从"使用者"迈向"开发者"的关键一步。

---

### 阶段 4：可观测性、性能调优与生产实践

**学习内容**:
- 可观测性集成：学习如何集成 Prometheus、Grafana 进行监控大盘展示，以及对接 SkyWalking、Jaeger 进行分布式链路追踪。
- 日志管理：配置访问日志输出至 Elasticsearch、SLS 或 Kafka，并进行日志分析。
- 性能调优：理解 Higress 的配置优化，包括连接池大小、缓冲区设置、以及 Wasm 虚拟机的性能考量。
- 高可用架构：学习 Higress 的高可用部署模式，包括多副本部署、热更新与配置回滚机制。
- 生产环境排错：掌握常见错误日志的分析方法，以及如何利用调试工具定位 502/504 等故障。

**学习时间**: 2-3周

**学习资源**:
- Higress 官方运维手册
- 云原生可观测性最佳实践白皮书
- Higress GitHub Issues (常见问题板块)

**学习建议**:
在此阶段，建议模拟生产环境压力测试（使用 JMeter 或 Hey），观察 Higress 的 QPS 上限与资源消耗情况。重点练习"全链路灰度"的配置，这是企业级落地中最复杂的场景之一。同时，务必熟悉配置回滚操作，以确保生产稳定性。

---
## 常见问题


### 1: Higress 是什么？它与云原生 API 网关有什么关系？

1: Higress 是什么？它与云原生 API 网关有什么关系？

**A**: Higress 是一个基于阿里云内部多年实践沉淀的下一代云原生 API 网关。它是在 2022 年开源的，旨在解决云原生时代流量治理的痛点。Higress 的核心特性是深度集成 Envioy 和 Istio，能够作为 Ingress Controller 或 API 网关使用。它不仅支持传统的南北向流量管理（如 K8s Ingress），还支持东西向流量管理（Service Mesh 中的流量）。简单来说，它是一个集成了 K8s Ingress Controller 和传统 API 网关功能的高性能网关，旨在连接微服务、云函数和后端服务，提供统一的流量入口。

---



### 2: Higress 与 Nginx、APISIX 或 Kong 等传统网关相比有什么优势？

2: Higress 与 Nginx、APISIX 或 Kong 等传统网关相比有什么优势？

**A**: Higress 的主要优势在于其云原生架构和与阿里云技术栈的深度集成：

1.  **技术栈**：Higress 基于 Envoy 构建（C++ 高性能），并使用 Go 语言开发控制面。相比 Nginx Lua 扩展（如 OpenResty/Kong），Envoy 的热更新能力和并发处理性能在云原生场景下更具优势。
2.  **标准化支持**：原生支持 Kubernetes Ingress API 和 Gateway API，能够无缝对接 K8s 生态，而传统网关往往需要额外的适配层。
3.  **安全与防护**：内置了 WAF（Web 应用防火墙）能力，这在开源网关中通常是付费插件或需要单独部署的。
4.  **插件生态**：兼容 Kong 和 Dubbo 的插件生态，降低了迁移成本。同时支持 WASM (WebAssembly) 插件，允许使用多种语言（如 Go, C++, Rust）编写高性能、低耦合的扩展插件。
5.  **服务发现**：原生支持 Nacos、ZooKeeper、Consul 等注册中心，不仅限于 K8s Service，非常适合混合云架构。

---



### 3: Higress 是否支持从其他网关（如 Nginx 或 Kong）迁移？迁移难度大吗？

3: Higress 是否支持从其他网关（如 Nginx 或 Kong）迁移？迁移难度大吗？

**A**: Higress 非常注重迁移的平滑性，设计了专门的工具来降低迁移难度。

1.  **配置兼容**：Higress 提供了 Nginx Ingress 注解的兼容支持，这意味着很多现有的 K8s Ingress YAML 文件可以直接在 Higress 上运行，无需大量修改。
2.  **插件兼容**：Higress 实现了 Kong 的插件规范，因此许多现有的 Lua 插件（Kong 生态）理论上可以经过适配后运行在 Higress 上。
3.  **迁移工具**：官方提供了配置迁移工具，可以帮助用户将传统的 Nginx 配置或 Kong 配置转换为 Higress 的配置格式。
4.  **Dubbo 支持**：对于使用 Dubbo 的传统 Java 微服务架构，Higress 提供了原生的 HTTP 转 Dubbo 的桥接能力，这对于从传统架构向云原生迁移的用户非常友好。

---



### 4: Higress 如何处理插件扩展？必须使用 Lua 吗？

4: Higress 如何处理插件扩展？必须使用 Lua 吗？

**A**: 不，Higress 的一个核心卖点就是摆脱了对 Lua 语言的强依赖。虽然它兼容 Kong 的 Lua 插件，但它更推荐使用 **WASM (WebAssembly)** 技术进行扩展。

1.  **多语言支持**：通过 WASM，开发者可以使用 Go、C++、Rust、JavaScript (AssemblyScript) 甚至 Python 来编写网关插件。
2.  **安全性**：WASM 插件运行在沙箱环境中，插件的崩溃不会导致网关主进程崩溃，这比 Lua 虚拟机具有更好的隔离性和稳定性。
3.  **热更新**：WASM 插件支持动态加载和卸载，更新插件逻辑不需要重启网关服务，实现了真正的业务零中断。
4.  **性能**：WASM 的执行效率接近原生代码，在高并发场景下通常优于 Lua 解释执行。

---



### 5: Higress 的性能表现如何？能否支撑高并发流量？

5: Higress 的性能表现如何？能否支撑高并发流量？

**A**: Higress 的性能表现非常出色，完全能够支撑企业级的高并发流量。

1.  **底层引擎**：Higress 的数据面基于 Envoy。Envoy 是云原生领域事实上的标准数据平面，由 C++ 编写，具有极高的处理效率和低延迟。
2.  **基准测试**：根据官方公布的基准测试数据，Higress 在处理 HTTP/HTTPS 请求时的吞吐量和延迟表现优异，在开启 QPS 限流、WAF 防护等复杂功能时，依然能保持高性能。
3.  **弹性伸缩**：作为云原生网关，Higress 可以利用 Kubernetes 的 HPA（水平自动伸缩）能力，根据流量情况自动增删 Pod 实例，实现弹性扩容。

---



### 6: Higress 是阿里云的商业产品吗？开源版本和云上版本有什么区别？

6: Higress 是阿里云的商业产品吗？开源版本和云上版本有什么区别？

**

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 在本地 Docker 环境中快速部署 Higress，并配置一个简单的路由规则，将访问 `/hello` 的请求转发到一个模拟的后端服务（如 `httpbin.org`）。

### 提示**:

### 查看 Higress 官方文档的 "快速开始" 部分。

---
## 实践建议

基于 Higress 作为 AI Native API 网关的定位，结合其基于 Envoy 和 Istio 的技术架构，以下是 6 条针对实际生产环境的实践建议：

### 1. 利用 Wasm 插件实现 LLM 提示词管理与安全审计
**场景：** 在对接大模型（如 OpenAI、通义千问等）时，直接将 Prompt 写在客户端代码中难以维护，且容易导致 Prompt 注入攻击或敏感数据泄露。
**建议：** 不要在客户端直接发送原始 Prompt。使用 Higress 的 Wasm 插件能力（特别是 `ai-proxy` 插件或自定义 Wasm 插件）在网关层进行 Prompt 的预处理。
**具体操作：**
*   在网关配置预设的 System Prompt（如“你是一个客服助手”）。
*   利用插件拦截请求，在请求体中动态注入上下文信息或格式化 Prompt 模板。
*   配置敏感词过滤策略，拦截包含恶意指令的请求。
**最佳实践：** 将 Prompt 的版本控制集中到网关层，实现模型调用的标准化，避免后端服务直接暴露模型 API Key。

### 2. 配置语义路由以实现多模型供应商的平滑切换
**场景：** 业务初期使用模型 A，后期想切换到模型 B，或者根据用户等级将流量分发到不同成本的模型（如 GPT-4 vs Claude 3 Haiku）。
**建议：** 利用 Higress 的路由匹配能力，将模型供应商抽象为统一的内部服务路径。
**具体操作：**
*   配置路由规则，例如将内部路径 `/v1/chat/completions` 映射到不同的后端 Upstream（OpenAI、Azure 或 Ollama）。
*   使用 Header（如 `X-Model-Provider: azure`）进行流量分流，实现基于权重的灰度发布。
**常见陷阱：** 避免将不同供应商的 API 签名逻辑硬编码在业务代码中。应通过 Higress 统一处理不同厂商的鉴权（Auth）差异，业务层只需调用统一的网关接口。

### 3. 针对流式响应的超时与缓冲策略优化
**场景：** AI 对话通常使用 SSE (Server-Sent Events) 流式返回，标准的网关超时配置可能会导致连接中断。
**建议：** 调整 Higress 的路由超时配置以适应长连接和流式传输。
**具体操作：**
*   将对应路由的 `timeout` 设置为较大的值（或者根据模型最大生成时间动态调整），避免生成一半被网关断开。
*   确保开启并正确配置 Per-Route buffer 限制，防止流式输出时网关内存溢出，同时保证流式数据的低延迟转发。
**最佳实践：** 在网关层启用日志采样，记录流式传输的首字节响应时间（TTFB），以此监控模型服务的响应延迟。

### 4. 实施细粒度的 Token 限流与配额管理
**场景：** 大模型调用成本主要与 Token 数量挂钩，传统的基于 QPS（每秒请求数）的限流无法控制成本。
**建议：** 结合插件实现基于 Token 或请求复杂度的限流。
**具体操作：**
*   虽然网关很难精确计算输出 Token，但可以基于输入 Prompt 的长度进行粗粒度分级限流。
*   针对不同的 API Key 或租户，配置不同的请求带宽限制。
*   对于并发控制，确保启用连接并发限制，防止后端模型服务被突发流量击垮。
**常见陷阱：** 仅限制 QPS 可能会导致用户发送超长 Prompt 耗尽资源。建议结合请求体大小限制来综合防护。

### 5. 混沌工程与故障注入测试
**场景：** 模型 API 服务（如 OpenAI）可能出现 429 (Rate Limit) 或 503 (Service Unavailable) 错误，网关需要具备健壮的降级能力。
**建议：** 在上线前使用 Higress 的故障注入功能模拟后端不可用的情况。
**具体操作：**
*

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [阿里开源](/tags/%E9%98%BF%E9%87%8C%E5%BC%80%E6%BA%90/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [LLM](/tags/llm/) / [MCP](/tags/mcp/) / [WASM](/tags/wasm/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260130-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260201-github_trending-alibaba-higress-8.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*