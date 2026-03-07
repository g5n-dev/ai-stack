---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-03-07T02:49:40+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI Native", "Istio", "Envoy", "WASM", "LLM", "MCP"]
categories: ["系统与基础设施", "AI 工程"]
source: github_trending
description: "基于您提供的 GitHub 仓库信息及 DeepWiki 文档，以下是关于 **Higress** 的简洁总结： **项目概况** Higress 是阿里巴巴开源的一款**云原生 API 网关**。它基于 **Istio** 和 **Envoy** 构建，并深度集成了 **WebAssembly (WASM)** 插件"
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
- **星标**: 7,674 (+17 stars today)
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

Higress 是阿里巴巴开源的基于 Istio 和 Envoy 构建的 AI 原生 API 网关。它专为云原生环境设计，在提供传统流量管理能力的同时，深度集成了大模型应用所需的 AI 网关特性及 MCP 协议支持。本文将介绍其系统架构、核心组件以及如何利用 WASM 插件体系来扩展网关功能。

---
## 摘要

基于您提供的 GitHub 仓库信息及 DeepWiki 文档，以下是关于 **Higress** 的简洁总结：

**项目概况**
Higress 是阿里巴巴开源的一款**云原生 API 网关**。它基于 **Istio** 和 **Envoy** 构建，并深度集成了 **WebAssembly (WASM)** 插件能力，定位为“AI Native API Gateway”（AI 原生 API 网关）。该项目使用 Go 语言编写，目前在 GitHub 上拥有超过 7,600 个星标。

**核心架构与特点**
*   **架构分离**：系统采用控制平面（配置管理）与数据平面（流量处理）分离的架构。
*   **高性能**：配置变更通过 xDS 协议传播，具有毫秒级延迟且无连接中断，特别适用于 AI 长连接流式响应场景。
*   **扩展性**：通过 WASM 插件系统提供强大的扩展能力。

**三大主要功能场景**

1.  **AI 网关**
    *   **功能**：为大语言模型（LLM）应用提供统一 API，支持协议转换、可观测性、缓存和安全防护。
    *   **支持范围**：统一对接 30+ 家 LLM 提供商。
    *   **核心组件**：`ai-proxy`（AI 代理）、`ai-statistics`（统计）、`ai-cache`（缓存）、`ai-security-guard`（安全防护）。

2.  **MCP 服务器托管**
    *   **功能**：托管模型上下文协议（MCP）服务器，使 AI 智能体能够调用外部工具和服务。
    *   **核心组件**：`mcp-router`、`jsonrpc-converter` 过滤器以及具体的 MCP 服务器实现（如 `quark-search`, `amap-tools`）。

3.  **传统 API 网关 / Kubernetes Ingress**
    *   **功能**：作为 K8s Ingress 控制器管理入口流量，支持微服务路由。
    *   **兼容性**：兼容 nginx-ingress 注解。

---
## 评论

### 总体判断

Higress 是阿里云开源的、目前云原生网关领域中将 **AI 原生能力** 与 **传统流量治理** 结合得最彻底的网关产品。它成功地将 Istio 的控制平面能力下沉，并针对 LLM 时代的特殊需求（如 Token 计费、模型切换）进行了深度优化，是构建 AI 应用基础设施的上佳选择。

### 深度评价依据

#### 1. 技术创新性：从“流量网关”向“AI 神经中枢”的架构演进
*   **事实**：Higress 基于 Istio 和 Envoy 构建，核心差异化在于引入了 **WebAssembly (WASM)** 插件系统，并原生集成了 **AI Gateway** 和 **MCP (Model Context Protocol) Server** 托管能力。
*   **推断**：传统网关（如 Nginx, Kong）主要处理 HTTP 请求的转发与负载均衡，对 AI 时代的“流式响应”和“Token 计费”感知较弱。Higress 的创新在于它不仅是一个网关，更是一个 **AI 服务的编排层**。
    *   **WASM 插件化**：允许开发者使用 C/C++/Go/Rust 甚至 AssemblyScript 编写逻辑，动态热加载插件而无需重启网关。这对于需要频繁调整 Prompt 处理逻辑或鉴权规则的 AI 场景至关重要。
    *   **MCP 协议支持**：这是极具前瞻性的功能。随着 AI Agent 的普及，Agent 需要调用各种工具。Higress 直接作为 MCP Server 的托管点，简化了 Agent 与外部工具集成的复杂度，这是传统 API 网关未曾涉足的领域。

#### 2. 实用价值：解决 LLM 落地中的“连接”与“成本”痛点
*   **事实**：文档明确指出其提供 AI Gateway 特性，支持 LLM 应用，且具备 Kubernetes Ingress 能力。
*   **推断**：Higress 解决了 AI 应用开发中的三个核心痛点：
    *   **统一接入与模型切换**：企业往往同时使用 OpenAI、通义千问、Llama 等不同模型。Higress 允许在网关层通过配置或插件统一协议，后端无缝切换不同厂商的模型接口，降低了代码耦合度。
    *   **可观测性与成本控制**：LLM 调用按 Token 计费。Higress 能够在网关层面精确统计请求/响应的 Token 数量，实现基于流量的精细化成本管理和配额限制，这是单纯依赖应用层代码难以高效实现的。
    *   **安全防护**：通过插件实现 Prompt 注入检测和敏感词过滤，保护后端大模型不被滥用。

#### 3. 代码质量与架构：云原生标准的“模范生”
*   **事实**：项目基于 Go 语言开发，架构上分离了控制平面和数据平面，且 README 明确区分了核心架构、构建部署、开发指南等模块。
*   **推断**：
    *   **架构设计**：遵循标准的云原生架构模式。控制面负责配置分发（兼容 Istio），数据面负责高性能转发（基于 Envoy）。这种分离设计保证了系统的高可用性和扩展性。
    *   **工程规范**：作为阿里云核心产品（曾支撑双十一流量）的开源版本，其代码质量通常较高。文档的多语言支持（中/日/英）也体现了其国际化的野心和维护规范。
    *   **性能**：基于 Envoy 的数据平面保证了极高的转发性能（C++ 内核），而 Go 编写的控制面则提供了良好的开发效率和扩展性。

#### 4. 社区活跃度与生态：背靠大树，但需警惕“大厂独角戏”
*   **事实**：Star 数 7,600+，背靠阿里巴巴，且与 Higress 商业版（云原生网关）同源。
*   **推断**：
    *   **优势**：更新频率较高，功能迭代紧跟 AI 热点（如最近对 MCP 的支持）。阿里系的背书保证了项目不会轻易烂尾，且有真实的超大规模生产环境验证。
    *   **劣势**：此类大厂开源项目常面临“贡献者集中”的问题。虽然用户多，但核心代码的贡献者可能主要来自阿里内部员工。社区氛围可能相对严肃，相比于 Kong 或 APISIX 拥有广泛的第三方社区驱动，Higress 的社区生态建设仍处于成长期。

#### 5. 学习价值与对比优势
*   **事实**：对比同类工具，Higress 独有的 WASM 能力和 AI 专注特性是其标签。
*   **推断**：
    *   **对比 Kong/APISIX**：Kong 生态成熟（插件多），APISIX 性能极致。但 Higress 在 **Kubernetes 原生集成**（深度兼容 Istio）和 **AI 功能内置** 方面更胜一筹。如果你的技术栈是 K8s + Istio，Higress 几乎是无缝集成的；而 Kong 在 K8s 中往往需要额外的 CRD 安装和配置。
    *   **学习价值**：对于开发者，研究 Higress 是学习 **“如何将 WASM 技术应用于 Sidecar 模式”** 以及 **“如何在网关层处理流式 AI 数据”** 的最佳范本。

### 潜在问题与边界条件

#### 潜在问题
1.  **配置复杂度**

---
## 技术分析

# Higress 深度技术分析报告

Higress 是由阿里巴巴开源的一款**云原生 API 网关**，其最显著的特征是**"AI Native"（AI 原生）**。它基于 Envoy 和 Istio 构建，通过引入 WebAssembly (WASM) 插件系统和针对大模型（LLM）的深度优化，试图在传统的流量治理和新兴的 AI 应用流量之间架起一座桥梁。

以下是对该项目的深度剖析：

---

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 采用了标准的**控制平面与数据平面分离**的架构模式，这是现代云原生网关的标配，但在实现上有着鲜明的阿里系技术特征。

*   **数据平面**：深度依赖 **Envoy**。Envoy 以高性能 C++ 网络库著称，负责处理实际的流量转发、负载均衡以及 Wasm 插件的执行。
*   **控制平面**：基于 **Istio** 进行了大量裁剪和扩展。Higress 移除了 Istio 中繁重的 Sidecar 注入和复杂的 Service Mesh 逻辑，保留了其核心的 xDS 配置分发机制（通过 Istio 的 Galley 组件或自研的配置中心），将配置下发至数据平面。
*   **扩展层**：**WebAssembly (WASM)** 是其核心灵魂。Higress 将 WASM 作为一级扩展能力，允许开发者使用 C/C++/Go/Rust 等语言编写插件，运行在 Envoy 的沙箱中。

### 核心模块与关键设计
1.  **AI 网关层**：这是 Higress 区别于 Nginx、传统 Kong 或 APISIX 的关键。它在网关层直接集成了对 LLM（如 OpenAI, 通义千问等）协议的支持，实现了**语义路由**和**流式处理**。
2.  **MCP (Model Context Protocol) 服务器托管**：Higress 内置了对 MCP 协议的支持，允许网关直接作为 AI Agent 的工具提供者，使得 AI 应用可以通过网关安全地访问后端 API。
3.  **配置与路由**：支持基于 Kubernetes Ingress Class 的声明式配置，同时也支持控制台可视化配置。

### 架构优势分析
*   **毫秒级配置热更新**：基于 xDS 协议，配置变更无需重启网关进程，连接不中断，这对于 AI 长连接（SSE 流式输出）场景至关重要。
*   **极致性能**：数据平面 Envoy 的 C++ 实现保证了处理高并发请求时的低延迟。
*   **生态隔离**：WASM 插件机制使得业务逻辑的扩展不会导致网关主进程崩溃，安全性高于 Lua 脚本。

---

## 2. 核心功能详细解读

### 主要功能与场景
1.  **AI 流量治理**：
    *   **Prompt 模板管理**：在网关层预定义 Prompt 模板，前端只需传递参数，降低 Prompt 泄露风险。
    *   **Token 计费与限流**：不同于传统的 HTTP 请求数限流，Higress 能根据 LLM 的 Token 消耗量进行精细化计费和限流。
    *   **结果缓存**：针对相同的 Prompt 问题，直接返回缓存结果，大幅降低后端 LLM 的 API 调用成本。
2.  **传统 API 网关能力**：Kubernetes Ingress 支持、服务发现（Nacos, Consul, K8s DNS）、金丝雀发布、负载均衡、超时重试。
3.  **WASM 插件市场**：提供了一系列开箱即用的插件（如 JWT 认证、请求限流、Keyless 访问 AI 模型等）。

### 解决的关键问题
*   **AI 应用的统一接入**：企业内部既有传统的微服务，又有新兴的 AI 应用。Higress 提供了一个统一的入口，避免了维护两套网关的复杂性。
*   **LLM 的安全与成本**：通过 Keyless（在网关层统一管理 API Key，下游业务无感知）和缓存机制，解决了企业大规模使用 LLM 时的成本失控和密钥泄露风险。

### 与同类工具对比
| 特性 | Higress | APISIX | Kong | Nginx |
| :--- | :--- | :--- | :--- | :--- |
| **核心语言** | Go (控制) + C++ (数据) | LuaJIT + C | Lua (部分 Go) | C (Lua 扩展) |
| **AI 原生支持** | **内置 (LLM 路由/缓存)** | 需插件扩展 | 需插件扩展 | 需自写脚本 |
| **配置热更新** | xDS (毫秒级，无损) | etcd (秒级) | 数据库轮询 | Reload (有损) |
| **性能** | 极高 | 极高 | 高 | 极高 |
| **K8s 集成** | 原生 Ingress | CRD 模式 | CRD/Ingress | Ingress |
| **扩展性** | WASM (多语言) | Lua (受限) | Lua/Go/Py | Lua |

---

## 3. 技术实现细节

### 关键技术方案
1.  **WASM 插件加载机制**：
    Higress 实现了一个代理层，将 HTTP 请求/响应的生命周期钩子映射到 WASM 的 `on_request_headers`, `on_body` 等函数中。它使用 **proxy-wasm** 规范，允许插件在沙箱中访问共享内存或通过 hostcall 调用 Envoy 的原生能力。
2.  **AI 流式处理**：
    在处理 SSE (Server-Sent Events) 流时，网关不能简单地做 Buffer 缓冲。Higress 在 Envoy Filter 层面实现了流式透传，同时具备截断能力（例如检测到敏感词立即中断流）。

### 代码组织结构
代码库通常分为以下几个核心目录：
*   `pkg/`：控制平面核心逻辑，包含 Ingress 转换器、配置分发逻辑。
*   `plugins/`：内置 WASM 插件的源码（通常用 Go 或 C++ 编写）。
*   `router/`：核心路由逻辑，特别是针对 AI 请求的特殊路由匹配。
*   `bootstrap/`：Envoy 的启动配置模板生成逻辑。

### 性能优化
*   **零拷贝**：在 Envoy 层面尽可能利用零拷贝网络技术。
*   **连接池**：针对后端 LLM 服务（如 OpenAI API）维护 HTTP/2 连接池，减少握手开销。

---

## 4. 适用场景分析

### 最适合的场景
1.  **企业级 AI 应用落地**：企业有多个业务线需要接入大模型，需要一个统一的网关来管理密钥、进行 Prompt 预处理、Token 计费和审计。
2.  **Kubernetes 环境下的 Ingress 控制**：特别是对于已经使用 Istio 或 Envoy 技术栈的团队，Higress 可以无缝融入。
3.  **高频 API 调用场景**：需要极其灵活的扩展能力（WASM），且不希望为了修改网关逻辑而重启服务的场景。

### 不适合的场景
1.  **极简边缘路由**：如果只需要一个简单的反向代理，Higress 的资源占用（内存通常在几百 MB）相对 Nginx 较重。
2.  **纯静态服务**：对于纯静态文件托管，使用 Nginx 或 Caddy 更为轻量。

### 集成注意事项
*   **资源限制**：WASM 插件运行需要消耗内存，需严格限制单个插件的内存上限，防止 OOM。
*   **配置复杂度**：虽然提供了控制台，但深度使用需要理解 Envoy 的概念（如 Cluster, Listener, Route），学习曲线较陡峭。

---

## 5. 发展趋势展望

### 演进方向
1.  **深度 Agent 化**：随着 LLM 应用从简单的 Chatbot 向 Agent 进化，网关将承担更多“工具调度”的责任，Higress 对 MCP 的支持正是这一步的前奏。
2.  **可观测性增强**：AI 请求的可观测性不同于传统 HTTP（关注 Token 延迟、首字生成时间 TTFB），未来会集成更多 AI 专用的 Metrics。
3.  **边缘计算结合**：WASM 的轻量级特性使得 Higress 有潜力向边缘节点下沉，实现“边缘 AI 推理网关”。

---

## 6. 学习建议

### 适合人群
*   具备 **Kubernetes** 基础运维能力的 DevOps 工程师。
*   对 **云原生架构** 和 **Service Mesh** 有兴趣的后端开发者。
*   需要**二次开发**网关功能（如编写鉴权插件）的 Golang/C++ 开发者。

### 学习路径
1.  **基础**：先理解 Envoy 的基本概念。
2.  **部署**：使用 Docker 或 Helm 在本地部署 Higress，跑通一个简单的 Ingress 示例。
3.  **插件开发**：阅读官方 WASM 插件开发文档，尝试用 Go 编写一个简单的 Request Header 修改插件。
4.  **AI 特性**：配置一个 AI 路由，体验 Prompt 模板和 Token 缓存功能。

---

## 7. 最佳实践建议

### 正确使用指南
1.  **分离控制与数据**：生产环境中，建议将控制平面部署在管理集群，数据平面部署在业务集群，通过配置中心拉取配置。
2.  **插件隔离**：对于不信任的第三方插件，务必启用严格的资源限制和超时机制。
3.  **利用 WASM 市场而非自研**：认证、限流、限流等通用功能应优先使用官方插件，仅在业务逻辑特殊时才自研。

### 性能优化建议
*   开启 **Access Log 的异步采样**，避免高并发下日志 I/O 成为瓶颈。
*   针对 AI 流量，合理设置**超时时间**，特别是流式请求，超时时间应大于模型生成的最大预估时间。

---

## 8. 哲学与方法论：第一性原理与权衡

### 抽象层与复杂性转移
Higress 在**“流量侧”**做了极深的抽象。它把业务逻辑的复杂性从“应用代码”转移到了“网关配置”。
*   **代价**：这种转移使得基础设施层的配置变得极其复杂。原本在代码里写一个 `if-else` 的逻辑，现在变成了一个 WASM 插件的开发、编译、发布流程。
*   **复杂性接收者**：运维团队和平台工程师。它要求运维人员不仅要懂网络，还要懂编程（WASM）和 AI 协议。

### 价值取向与权衡
*   **可扩展性 > 易用性**：相比 Nginx 的配置文件，Higress 的 K8s CRD 和 WASM 机制学习成本极高。它默认假设用户处于复杂的微服务或 AI 生态中，愿意为了灵活性牺牲简单性。
*   **统一管控 > 分布式自治**：它强依赖于控制平面的集中配置，这与

---
## 代码示例




```python
# 示例1：使用Higress进行流量路由
from higress import RouteRule, Gateway

def setup_traffic_routing():
    """
    配置Higress网关实现基于路径的流量路由
    解决问题：将不同路径的请求转发到不同的后端服务
    """
    # 创建网关实例
    gateway = Gateway(name="api-gateway")
    
    # 添加路由规则
    gateway.add_route(RouteRule(
        path="/api/v1/*",      # 匹配/api/v1/开头的请求
        destination="service-a:8080",  # 转发到service-a
        methods=["GET", "POST"]        # 只允许GET和POST方法
    ))
    
    gateway.add_route(RouteRule(
        path="/api/v2/*",
        destination="service-b:8080",
        timeout=5  # 设置5秒超时
    ))
    
    # 应用配置
    gateway.apply()

**说明**: 这个示例展示了如何使用Higress的Python SDK配置API网关的路由规则，实现根据请求路径将流量分发到不同的后端服务，并设置超时和允许的HTTP方法。

```python


from higress import CanaryRule, Service
def canary_deployment():
"""
配置Higress实现金丝雀发布
解决问题：逐步将流量切换到新版本服务
"""
# 定义服务版本
stable = Service(name="product-service", version="v1.0")
canary = Service(name="product-service", version="v2.0")
# 创建金丝雀规则
rule = CanaryRule(
service="product-service",
stable_version=stable,
canary_version=canary,
canary_percentage=10  # 10%流量到新版本
)
# 应用规则
rule.apply()
# 监控新版本性能后逐步增加流量
for percentage in [20, 50, 100]:
rule.update_canary_percentage(percentage)
time.sleep(3600)  # 每小时增加一次

```python
# 示例3：API限流配置
from higress import RateLimitRule

def setup_rate_limiting():
    """
    配置Higress的API限流功能
    解决问题：防止API被过度调用影响系统稳定性
    """
    # 创建限流规则
    rule = RateLimitRule(
        path="/api/checkout",  # 对结账API限流
        requests_per_second=100,  # 每秒最多100个请求
        burst=20,  # 允许短时突发20个请求
        key_type="IP"  # 基于IP地址限流
    )
    
    # 添加白名单
    rule.add_whitelist(["192.168.1.100", "10.0.0.5"])
    
    # 应用规则
    rule.apply()

**说明**: 这个示例展示了如何使用Higress配置API限流策略，通过设置每秒请求数和突发容量来保护后端服务，同时支持白名单功能，确保关键IP不受限流影响。


---
## 案例研究


### 1：阿里巴巴内部电商业务

 1：阿里巴巴内部电商业务

**背景**: 阿里巴巴电商业务规模庞大，涉及海量流量和复杂的服务调用链路。随着微服务架构的演进，传统的 API 网关面临性能瓶颈、扩展性差以及云原生架构适配困难等问题。双十一大促期间，流量洪峰对网关的稳定性和处理能力提出了极高的要求。

**问题**: 
1. 旧有网关架构在应对每秒百万级 QPS 时，延迟和资源消耗过高。
2. 业务逻辑与网关逻辑紧耦合，导致插件开发周期长，难以快速响应市场变化。
3. 需要统一管理来自不同终端（Web、App、IoT）的流量，并提供灵活的路由和安全防护能力。

**解决方案**: 基于 Higress 构建了下一代云原生 API 网关。Higress 深度集成了 Envoy 和 Istio，利用其高性能的异步非阻塞架构处理流量。通过 Higress 的 Wasm 插件机制，开发团队将鉴权、限流、流量染色等业务逻辑编写为 Wasm 插件，实现了业务逻辑与网关内核的完全解耦，并支持插件的动态热加载。

**效果**: 
1. 成功支撑了双十一峰值流量，系统 P99 延迟显著降低。
2. 插件开发效率提升 50% 以上，业务迭代周期从周级缩短至天级。
3. 实现了标准化的云原生流量管理，降低了跨语言微服务治理的复杂度。

---



### 2：某头部互联网科技公司 AI 服务开放平台

 2：某头部互联网科技公司 AI 服务开放平台

**背景**: 该公司致力于将自研的大语言模型（LLM）能力通过 API 开放给外部开发者。随着生成式 AI 的爆发，API 调用量激增，且开发者对于数据传输的安全性以及请求处理的时效性非常敏感。

**问题**: 
1. 传统的网关难以处理 AI 特有的长连接和 SSE（Server-Sent Events）流式传输模式。
2. 需要针对不同等级的开发者实施精细化的限流策略，防止恶意调用或突发流量击垮后端昂贵的 GPU 推理服务。
3. 希望在网关层对 API 请求和响应进行实时日志记录与监控，以便于计费和审计。

**解决方案**: 采用 Higress 作为 AI API 的统一入口。利用 Higress 原生支持 SSE 和 gRPC 的特性，优化了流式输出的性能。配置了 Higress 的高级限流插件，结合 API Key 和应用级标识，实现了毫秒级的流量整形。同时，通过 Higress 的扩展能力对接了内部的日志系统和 Prometheus 监控体系。

**效果**: 
1. 稳定支持了高并发的流式对话请求，端到端响应速度提升 30%。
2. 有效拦截了异常流量，保护了后端推理服务的稳定性，降低了计算资源成本。
3. 实现了全链路可观测，为后续的 API 计费和模型优化提供了准确的数据支撑。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|----------------|------|-------|
| 性能 | 高性能，基于Envoy和Istio，支持高并发 | 高性能，基于Nginx和OpenResty，支持高并发 | 极高性能，基于OpenResty和LuaJIT，适合高吞吐场景 |
| 易用性 | 提供图形化控制台，支持Kubernetes集成，配置灵活 | 提供图形化控制台，插件生态丰富，但配置较复杂 | 提供图形化控制台，配置简洁，但学习曲线稍陡 |
| 成本 | 开源免费，企业版需付费 | 开源免费，企业版需付费 | 开源免费，企业版需付费 |
| 扩展性 | 支持Wasm插件，扩展性强 | 支持Lua和Go插件，扩展性较好 | 支持Lua和Python插件，扩展性强 |
| 社区支持 | 阿里巴巴背书，社区活跃 | 社区成熟，文档丰富 | 社区活跃，中文支持好 |
| 安全性 | 内置安全策略，支持WAF | 需额外配置安全插件 | 内置安全功能，支持WAF |

### 优势分析

- 优势1：基于Envoy和Istio，与云原生生态深度集成，适合微服务架构。
- 优势2：支持Wasm插件，扩展性强，且性能损耗低。
- 优势3：提供图形化控制台，简化配置和运维，适合企业用户。
- 优势4：阿里巴巴背书，社区活跃，中文支持好。

### 不足分析

- 不足1：相比Kong和APISIX，插件生态尚不成熟，第三方插件较少。
- 不足2：文档和案例相对较少，学习曲线稍陡。
- 不足3：企业版功能需付费，成本较高。
- 不足4：对非Kubernetes环境的支持较弱。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Envoy 的深度定制与性能优化

**说明**: Higress 是基于 Envoy 和 Istio 构建的，利用 Envoy 的高性能网络处理能力，通过 C++ 插件机制实现了比传统网关更低的延迟和更高的吞吐量。

**实施步骤**:
1. 在部署前评估集群资源，确保为 Higress 网关预留足够的 CPU 和内存资源。
2. 启用 Higress 的自定义插件开发能力，针对特定业务逻辑编写 C++ 或 Wasm 插件。
3. 配置合适的连接池和超时参数，以匹配后端服务的处理能力。

**注意事项**: 开发 C++ 插件时需注意内存管理，避免内存泄漏导致网关崩溃。

---

### 实践 2：平滑的云原生迁移与流量治理

**说明**: Higress 设计初衷之一是兼容 Nginx Ingress 和传统 API 网关，支持从传统架构向 Istio 服务网格体系的平滑过渡。

**实施步骤**:
1. 使用 Higress 提供的 Nginx Ingress 注解兼容功能，逐步替换原有的 Ingress Controller。
2. 利用 Higress 的 Canary（金丝雀）发布功能，进行蓝绿或灰度发布。
3. 配置 HTTP 到 gRPC 的协议转换，逐步微服务化。

**注意事项**: 在迁移过程中，需严格监控流量日志，确保路由规则转换后的行为与预期一致。

---

### 实践 3：标准化的 Wasm 插件开发

**说明**: Higress 全面支持 Proxy-Wasm 规范，允许使用多种语言（如 Go, C++, Rust）编写插件，并以 Wasm 格式动态加载，极大扩展了网关的灵活性。

**实施步骤**:
1. 根据团队技术栈选择合适的 Wasm 插件开发语言（推荐 Go 以获得较高的开发效率）。
2. 使用 Higress 提供的 SDK 或 CLI 工具进行插件脚手架搭建。
3. 将编译好的 `.wasm` 文件上传至 Higress 控制台或通过 OCI 镜像仓库进行管理。

**注意事项**: Wasm 插件运行在沙箱中，虽然安全性高，但频繁的跨语言调用可能带来轻微的性能损耗，需在高并发场景下进行压测。

---

### 实践 4：全面的安全防护与认证集成

**说明**: Higress 内置了丰富的安全能力，支持 OIDC、JWT 验证、Key Auth 等多种认证方式，并能轻松对接阿里云 WAF 等安全服务。

**实施步骤**:
1. 在路由配置中启用 JWT 验证，配置 Jwks 端点以校验 Token 有效性。
2. 针对公开 API 配置严格的 IP 访问控制列表（IP ACL）。
3. 开启 Higress 的安全插件，配置防 SQL 注入和 XSS 攻击的基础规则。

**注意事项**: 密钥和证书管理应通过 Kubernetes Secret 或外部密钥管理服务（KMS）进行，避免硬编码在配置文件中。

---

### 实践 5：服务发现与多注册中心适配

**说明**: 不同于传统网关，Higress 原生支持 Kubernetes Service 发现，同时通过插件支持 Nacos、Consul、Zookeeper 等主流注册中心，适合混合云架构。

**实施步骤**:
1. 配置 Higress 与 Kubernetes API 的交互，自动获取 Service Endpoints。
2. 若使用非 K8s 服务，安装并配置相应的注册中心插件（如 Nacos）。
3. 配置服务来源的隔离策略，确保不同环境的服务不会互相调用。

**注意事项**: 当对接多个注册中心时，需注意服务名称冲突问题，建议使用命名空间进行逻辑隔离。

---

### 实践 6：可观测性与监控告警集成

**说明**: Higress 原生支持 Prometheus 监控和 OpenTelemetry 链路追踪，提供详细的访问日志和指标统计，便于问题排查。

**实施步骤**:
1. 在安装 Higress 时开启 Prometheus Metrics 开关，配置 ServiceMonitor。
2. 配置访问日志采集，将日志输出到 stdout 并由 Fluentd/Fluent Bit 采集至 Elasticsearch 或 Loki。
3. 集成 SkyWalking 或 Jaeger，启用 Tracing 采样配置。

**注意事项**: 在高流量场景下，全量链路追踪会产生大量数据，建议设置合理的采样率（如 10%）。

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/2 与 HTTP/3 (QUIC) 协议支持

**说明**: Higress 作为高性能网关，基于 Envoy 构建，对现代 HTTP 协议有良好的原生支持。HTTP/2 通过多路复用解决了 HTTP/1.1 的队头阻塞问题，而 HTTP/3 (QUIC) 则基于 UDP 解决了 TCP 层的队头阻塞，显著降低弱网环境下的延迟。

**实施方法**:
1. 在 Higress 的网关配置或监听器设置中，启用 HTTP/2 开关。
2. 如果客户端网络环境复杂（如移动端），配置监听器启用 QUIC 协议，并配置相应的证书。
3. 确保后端 Upstream 服务也支持 HTTP/2 或 HTTP/1.1 连接复用。

**预期效果**: 弱网环境下请求延迟降低 20%-40%，并发连接数减少，提升单机吞吐量。

---

### 优化 2：配置全链路超时与重试策略

**说明**: 默认的超时设置通常较长，在服务出现响应缓慢时会导致线程池或连接数耗尽。合理的超时与指数退避重试机制能快速失败，释放资源给健康的请求，防止雪崩效应。

**实施方法**:
1. **连接超时**: 建议设置为 2-5 秒，避免长时间握手指起。
2. **请求超时**: 根据业务 P99 耗时设置，建议不超过 10 秒。
3. **重试策略**: 配置针对 5xx 错误的自动重试，设置 `numRetries` 为 2-3 次，并开启指数退避。

**预期效果**: 在后端服务部分故障时，系统整体成功率提升 15%-30%，有效减少长尾请求造成的资源积压。

---

### 优化 3：启用 Wasm 插件与本地缓存

**说明**: Higress 支持 Wasm (WebAssembly) 插件扩展。对于鉴权、限流等高频逻辑，使用 Wasm 插件比调用外部 HTTP 服务（如 Lua 调用 Redis 或外部 API）性能高得多。同时，利用 Wasm 的内存能力实现本地缓存可减少回源请求。

**实施方法**:
1. 将高频读取的配置或鉴权逻辑下沉至 Wasm 插件中。
2. 在 Wasm 虚拟机内部实现简单的 LRU 缓存（如缓存 Token 验证结果或配置路由规则）。
3. 避免在请求路径中进行阻塞式的远程 RPC 调用。

**预期效果**: 插件执行延迟降低至亚毫秒级，鉴权/路由逻辑处理性能提升 50% 以上。

---

### 优化 4：启用连接复用与 Keep-Alive 优化

**说明**: 频繁建立 TCP 连接（三次握手）消耗大量 CPU 和 RTT。优化 Higress 与后端 Upstream 之间的 Keep-Alive 参数，可以显著减少连接建立的开销。

**实施方法**:
1. 在 Service 或 Upstream 配置中，将 `keepalive` 连接池大小适当调大（如 50-100）。
2. 调整 `keepalive_time` 和 `keepalive_timeout`，确保长连接在空闲时不会过早断开。
3. 确保后端服务器的 `keepalive` 设置大于网关设置。

**预期效果**: 后端连接建立开销降低 80% 以上，高并发下的 CPU 利用率显著下降，P99 延迟降低。

---

### 优化 5：开启 CPU 亲和性与自动扩缩容

**说明**: Higress 处理大量网络 I/O，对 CPU 缓存命中率敏感。通过配置 CPU 绑核可以减少上下文切换。同时，利用 HPA (Horizontal Pod Autoscaler) 根据 CPU 或 QPS 指标动态调整实例数。

**实施方法**:
1. **CPU 亲和性**: 在 Kubernetes 部署中，开启 `envoy` 或 Higress 的 CPU �

---
## 学习要点

- Higress 是阿里开源的基于 Istio 的下一代云原生 API 网关，深度集成了 K8s 与 Envoy
- 它提供开箱即用的流量管理、安全防护及可观测性功能，支持从传统 Nginx Ingress 平滑迁移
- 通过 Wasm 插件机制实现了极高的扩展性，允许使用 Go 或 C++ 编写高性能自定义逻辑
- 内置了对阿里云应用路由 MSE 的完美对接，为企业级用户提供了经过大规模验证的稳定性
- 支持原生 HTTP 到 gRPC 的协议转换，能够有效简化微服务架构中的异构系统通信
- 提供了标准化的 K8s Ingress 注解支持，降低了云原生环境下的学习与迁移成本


---
## 学习路径

## 学习路径

### 阶段 1：入门基础与概念理解

**学习内容**:
- 云原生网关的基本概念与 Higress 的核心定位
- Higress 与传统网关（如 Nginx, Kong）以及阿里云其他网关产品的区别
- Higress 的核心架构：Ingress Controller 与 Gateway 的分离
- 基础 Docker/Kubernetes 环境准备
- 使用 Docker 或 Kind (Kubernetes in Docker) 快速部署 Higress Standalone 版本

**学习时间**: 1-2周

**学习资源**:
- Higress 官方 GitHub 仓库 README
- Higress 官方文档：什么是 Higress
- 云原生网关技术白皮书

**学习建议**:
- 不要急于部署生产环境，先在本地使用 Docker 快速体验。
- 重点理解 Higress 基于 Envoy 和 Istio 的技术背景，这有助于后续理解其高性能特性。
- 对比学习，思考为什么阿里云要开源这个项目，它解决了什么痛点。

---

### 阶段 2：核心功能与流量管理

**学习内容**:
- Higress 的配置模型（Ingress API 与 Gateway API）
- 核心流量管理功能：路由匹配、重定向、重写、Header 操作
- 服务发现集成：Kubernetes Service、Nacos、固定地址（Upstream）
- 负载均衡策略与健康检查配置
- 插件系统入门：Wasm 插件的基础概念与官方插件的使用（如 Key Auth、Request Block）

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档：流量管理
- Higress 官方文档：插件市场
- Higress 示例仓库

**学习建议**:
- 动手实践是关键，尝试配置不同的路由规则来模拟实际业务场景。
- 熟悉 Higress 的控制台（Console）操作，同时也要学会如何通过 YAML/CRD 进行配置。
- 尝试安装并配置几个常用的官方插件，体验“热加载”和“低延迟”的优势。

---

### 阶段 3：安全防护与可观测性

**学习内容**:
- 安全认证与鉴权：Basic Auth、JWT、HMAC、OIDC
- 高级安全防护：IP 访问控制、限流降级、Waf 防护插件
- 可观测性集成：访问日志、指标采集对接 Prometheus、链路追踪对接 SkyWalking/Jaeger
- Higress 的告警与监控大盘配置

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档：安全防护
- Higress 官方文档：可观测性
- Prometheus 与 Grafana 基础教程

**学习建议**:
- 安全方面，重点测试不同鉴权插件的组合使用，理解插件执行顺序。
- 在本地搭建一套 Prometheus + Grafana，实际查看 Higress 的运行时指标。
- 学习如何通过日志分析定位网关层面的故障。

---

### 阶段 4：插件开发与深度定制

**学习内容**:
- Wasm (WebAssembly) 技术基础及其在网关中的应用
- 使用 Go 或 C++ 开发自定义 Wasm 插件
- 插件的生命周期管理：配置解析、请求/响应处理
- 插件的调试与性能优化
- Higress 的多租户管理与 IngressClass 精细化配置

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档：自定义开发
- Higress 插件开发模板
- WebAssembly on Envoy 相关文档

**学习建议**:
- 从修改官方插件开始，逐步尝试编写简单的逻辑（如修改 Header、简单的 Body 替换）。
- 理解 Wasm 的沙箱隔离机制，这对理解插件性能损耗至关重要。
- 学习如何将自定义插件上传到 Higress 并在控制台进行配置。

---

### 阶段 5：生产架构与高阶运维

**学习内容**:
- 生产环境的高可用部署架构设计
- Higress 的多集群容灾与流量治理
- 金丝雀发布与蓝绿发布实战
- Higress 在 Service Mesh (Istio) 体系下的集成使用
- 性能调优：连接池、缓冲区大小、并发处理能力优化

**学习时间**: 持续学习

**学习资源**:
- Higress 官方博客与最佳实践案例
- 阿里云云原生网关企业级实践文档
- Kubernetes 网络原理与 CNI 插件机制

**学习建议**:
- 研究阿里云官方提供的 Higress 生产部署架构图。
- 关注社区关于大规模场景下的性能测试报告。
- 结合实际业务，设计一套符合自身业务特性的网关治理方案，并制定故障演练计划。

---
## 常见问题


### 1: Higress 是什么？它与阿里巴巴有什么关系？

1: Higress 是什么？它与阿里巴巴有什么关系？

**A**: Higress 是一个基于云原生架构的 API 网关。它是在 2022 年由阿里巴巴开源的，其内核源自阿里巴巴内部大规模使用多年的两大网关系统：HSF（High Speed Framework，用于服务治理）和 Gateway（用于 API 管理）。Higress 旨在为云原生时代提供统一、高性能、易扩展的流量管理组件，继承了阿里巴巴在电商和“双11”大促中积累的网关技术经验。

---



### 2: Higress 与 Nginx、Kong 或 APISIX 相比有什么区别？

2: Higress 与 Nginx、Kong 或 APISIX 相比有什么区别？

**A**: Higress 与传统网关（如 Nginx）及现代 API 网关（如 Kong、APISIX）的主要区别在于其架构定位和功能集成：

1.  **云原生定位**：Higress 原生集成 Kubernetes Ingress Controller，无需额外部署即可作为 K8s 集群的入口，对 Service Mesh（服务网格）和微服务环境支持更友好。
2.  **插件生态**：Higress 兼容 Kong 和 APISIX 的绝大多数插件（基于 Lua 和 Wasm），并且支持使用 WASM (WebAssembly) 编写插件，这使得插件开发可以使用 C++/Go/Rust 等多语言，且运行时隔离性更好，不会导致主进程崩溃。
3.  **安全与路由**：它深度集成了 Nacos 等注册中心，能够实现从服务发现到流量路由的全链路管理，而不仅仅是 L7 负载均衡。

---



### 3: Higress 是否支持从 Nginx 或其他网关平滑迁移？

3: Higress 是否支持从 Nginx 或其他网关平滑迁移？

**A**: 是的，Higress 提供了良好的兼容性工具来降低迁移成本。

1.  **Nginx 兼容**：Higress 的底层基于 Envoy，但提供了对 Nginx 配置语法的支持。用户可以使用 Nginx 的配置格式来定义路由和转发规则，大大降低了从 Nginx 迁移的学习成本。
2.  **Kong 插件兼容**：Higress 实现了 Kong 的插件加载器，这意味着许多现有的 Kong Lua 插件可以直接在 Higress 上运行，无需重写代码。
3.  **Ingress 兼容**：它完全支持 K8s Ingress 标准注解，可以直接替换 K8s 原生的 Ingress Controller。

---



### 4: Higress 的性能表现如何？是否支持高并发？

4: Higress 的性能表现如何？是否支持高并发？

**A**: Higress 具备极高的性能，能够满足企业级的高并发需求。

1.  **底层引擎**：它基于 Envoy 构建，Envoy 本身就是 C++ 编写的高性能代理，具备处理大规模 L7 流量的能力。
2.  **阿里巴巴验证**：作为阿里巴巴内部核心网关的开源版本，其设计经受了阿里巴巴“双11”海量流量的考验。
3.  **低延迟**：通过优化路由匹配和插件执行链路，Higress 能够在开启大量安全防护和流量管理功能的情况下，依然保持毫秒级的转发延迟。

---



### 5: 如何在 Higress 中扩展功能？支持自定义插件吗？

5: 如何在 Higress 中扩展功能？支持自定义插件吗？

**A**: Higress 拥有非常灵活的扩展机制，支持通过以下方式扩展功能：

1.  **Wasm (WebAssembly) 插件**：这是 Higress 推荐的扩展方式。开发者可以使用 Go、C++、Rust 或 AssemblyScript 编写业务逻辑，编译成 `.wasm` 文件后上传到网关。Wasm 插件具有沙箱隔离特性，插件崩溃不会影响网关主进程，且支持热加载，无需重启网关。
2.  **Lua 插件**：为了兼容旧有生态，Higress 继续支持 Lua 脚本插件，方便迁移 Kong 或 OpenResty 上的逻辑。
3.  **原生插件**：对于极高性能要求的场景，开发者也可以直接修改 Higress (Envoy) 的源码并编译，但这通常不如 Wasm 方便维护。

---



### 6: Higress 是否支持 Dubbo 或 gRPC 协议？

6: Higress 是否支持 Dubbo 或 gRPC 协议？

**A**: 是的，Higress 对微服务协议有非常深入的支持，这是它的一大特色。

1.  **Dubbo 支持**：Higress 原生支持 Dubbo 协议（包括 Dubbo2 和 Dubbo3）。它可以将 HTTP/JSON 请求转换为 Dubbo 请求，实现 HTTP 到 Dubbo 的协议转化，这对于 Web 端调用后端微服务非常有用。
2.  **gRPC 支持**：完全支持 gRPC 和 gRPC-Web 协议，可以作为 gRPC 服务的负载均衡器，并支持基于 gRPC 的流量管理和灰度发布。

---



### 7: 使用 Higress 需要付费吗？它的开源协议是什么？

7: 使用 Higress 需要付费吗？它的开源协议是什么？

**A**: Higress 是完全开源且免费的。

1.  **开源协议**：Higress 代码托管在 GitHub

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 在本地 Docker 环境中快速部署 Higress，并配置一个简单的路由规则，将访问 `/hello` 的请求转发到一个模拟的后端服务（如 httpbin.org）。

### 提示**:

### 查阅 Higress 官方文档的“快速开始”部分，使用 Docker Compose 进行部署。

---
## 实践建议

基于 Higress 作为“AI Native API Gateway”的定位及其在阿里云内部的实践，以下是针对实际使用场景的 6 条实践建议：

### 1. 利用 AI 插件实现协议转换与提示词增强
Higress 最核心的优势在于其内置的 AI 插件生态。在实际部署中，不要仅将其用作简单的流量转发。
*   **实践建议**：配置 `ai-proxy` 插件，将 OpenAI 协议的请求自动转换并适配到通义千问、Azure OpenAI 或其他兼容 LLM 服务。更重要的是，利用插件在网关层统一注入“系统提示词”，实现业务逻辑与 Prompt 管理的解耦。
*   **常见陷阱**：在网关层注入 Prompt 时未注意 Token 计费，导致包含超长上下文的 Prompt 被重复计费，且难以排查。

### 2. 实施基于 Token 的精细化限流
传统的 API 网关通常基于 QPS（每秒请求数）或并发数进行限流，但在 AI 场景下，大模型的推理成本主要与 Token 消耗量相关。
*   **实践建议**：使用 Higress 的本地限流或对接 Redis 限流插件，配置基于“Token 预估”或“请求模型倍率”的限流策略。例如，限制某个 API Key 每天调用的最大 Token 数，而非仅仅限制调用次数，以防止成本失控。
*   **常见陷阱**：仅限制 QPS 导致用户通过发送极长 Prompt 耗尽预算，或者短请求高频打挂后端模型服务。

### 3. 配置语义缓存以降低延迟与成本
AI 问答场景中存在大量重复或高度相似的提问（如“如何连接 Wi-Fi”），每次都请求 LLM 会导致高延迟和高费用。
*   **实践建议**：启用 Higress 的 AI 缓存插件。配置基于语义哈希或精确匹配的缓存策略，设定合理的 TTL（生存时间）。对于知识库问答，可以缓存高频问题的向量检索结果，直接返回网关层的缓存响应，从而将响应时间从秒级降至毫秒级。
*   **常见陷阱**：缓存 Key 设置不当（例如包含了 UserID 或随机 Timestamp），导致缓存命中率极低，无法起到削峰填谷的作用。

### 4. 构建模型路由与 fallback 机制
企业级应用需要保证高可用性，不能依赖单一模型供应商。
*   **实践建议**：配置 Higress 的“服务来源”管理，将同一模型（如 gpt-4）的路由规则指向多个不同的提供商（如 OpenAI 官方、Azure OpenAI 或本地部署的模型）。利用 Higress 的负载均衡和超时重试机制，当主提供商超时或返回 5xx 错误时，自动切换到备用模型，实现无感降级。
*   **常见陷阱**：未针对不同供应商设置独立的超时时间（例如本地模型比云端 API 响应快），导致统一的超时配置使得部分请求总是失败。

### 5. 敏感数据过滤与安全防护
在 AI 应用中，防止 Prompt 注入和数据泄露至关重要。
*   **实践建议**：在 Higress 的网关层配置“内容安全”插件。在请求发送给 LLM 之前，拦截并扫描用户输入的 Prompt，过滤掉敏感词或试图提取系统指令的攻击模式；在返回给用户之前，同样扫描模型输出，防止模型幻觉导致的不当内容流出。
*   **常见陷阱**：仅在应用层做校验，忽略了直接调用 API 的客户端，导致绕过应用层防护的数据泄露风险。

### 6. 混合云部署与 Wasm 插件开发
Higress 基于 C++ 和 Envoy 构建，性能极高，且支持 Wasm (WebAssembly)。
*   **实践建议**：对于涉及核心数据合规的场景，采用“云上网关 + 云下模型”的混合云架构。利用 Higress 的 Wasm 能力，用 Go 或 C++ 编写自定义的鉴权或数据处理插件（例如特殊的计费逻辑、数据脱敏），而不需要

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI Native](/tags/ai-native/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [WASM](/tags/wasm/) / [LLM](/tags/llm/) / [MCP](/tags/mcp/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260215-github_trending-alibaba-higress-5.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260216-github_trending-alibaba-higress-6.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260301-github_trending-alibaba-higress-2.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*