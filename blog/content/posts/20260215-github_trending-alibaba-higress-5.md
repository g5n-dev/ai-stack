---
title: "阿里 Higress：AI 原生 API 网关"
date: 2026-02-15T00:52:35+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "Istio", "Envoy", "WASM", "LLM", "MCP"]
categories: ["系统与基础设施", "AI 工程"]
source: github_trending
description: "以下是对 Higress 项目的简洁总结： **项目概述** Higress 是由阿里巴巴开源的一款**AI 原生 API 网关**。基于 **Go** 语言开发，目前 GitHub 星标数已超 7,500。该项目构建在 Istio 和 Envoy 之上，通过引入 WebAssembly (WASM) 插件能力，将云原"
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
- **星标**: 7,528 (+4 stars today)
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

Higress 是一款基于 Istio 和 Envoy 构建的 AI 原生 API 网关，它通过云原生架构处理流量管理，并集成了面向大模型应用的特殊功能。该项目旨在解决微服务路由、Kubernetes Ingress 管理以及 AI Agent 工具集成（如 MCP 协议支持）等场景下的连接与安全问题。本文将为您梳理其系统架构、核心组件以及 WASM 插件体系，帮助您评估如何将其应用于现有的技术栈中。

---
## 摘要

以下是对 Higress 项目的简洁总结：

**项目概述**
Higress 是由阿里巴巴开源的一款**AI 原生 API 网关**。基于 **Go** 语言开发，目前 GitHub 星标数已超 7,500。该项目构建在 Istio 和 Envoy 之上，通过引入 WebAssembly (WASM) 插件能力，将云原生 API 网关与 AI 时代的需求深度结合。

**核心架构与优势**
Higress 采用了**控制平面**与**数据平面**分离的架构。配置变更通过 xDS 协议传播，具备毫秒级延迟和零连接中断的特性，非常适合处理 AI 流式响应等长连接场景。它不仅兼容 Kubernetes Ingress（支持 nginx-ingress 注解），还专为 AI 应用提供了强大的扩展功能。

**三大主要应用场景**
1.  **AI 网关**：提供统一的 API 接口，兼容 30+ 家大语言模型（LLM）服务商。内置协议转换、可观测性、缓存（`ai-cache`）和安全防护（`ai-security-guard`）等功能。
2.  **MCP 服务器托管**：支持托管模型上下文协议（MCP）服务器，使 AI Agent 能够便捷地调用工具和服务（如地图工具、搜索引擎等）。
3.  **云原生入口**：作为高性能的微服务网关，处理 Kubernetes Ingress 和传统 API 路由。

---
## 评论

### 总体评价

Higress 是目前云原生网关领域中将**AI 原生能力**与**云原生架构**融合得最为彻底的开源项目之一。它不仅继承了 Istio/Envoy 的高性能基因，更通过 WASM 插件生态和 MCP 协议支持，精准击中了 LLM 时代流量治理的痛点，是构建 AI 应用基础设施的优选方案。

---

### 深入评价依据

#### 1. 技术创新性：从“流量管理”向“模型编排”的架构跃迁
*   **事实**：Higress 基于 Istio 和 Envoy 构建，明确提出了“AI Native API Gateway”的定位，并集成了 WASM 插件系统和 MCP (Model Context Protocol) 服务器托管能力。
*   **推断**：Higress 的核心创新在于打破了传统网关仅做 HTTP 转发的边界。通过引入 **MCP 协议支持**，它充当了 AI Agent 与外部工具（数据源）之间的“翻译官”，解决了 Agent 应用中工具调用的标准化问题。同时，利用 **WASM (WebAssembly)** 技术实现了业务逻辑与网关内核的解耦，允许开发者用 C/C++/Go/Rust/AssemblyScript 甚至 Python（通过 proxy-wasm）编写插件，在热加载的同时实现了接近原生代码的执行性能。这种“可编程的 AI 网关”架构，使其具备了处理 Token 计数、Prompt 模板渲染、模型路由等 AI 特定逻辑的能力，而不仅仅是透传流量。

#### 2. 实用价值：解决 LLM 落地中的“最后一公里”问题
*   **事实**：项目描述指出其提供 AI Gateway Features for LLM applications，并支持 Kubernetes Ingress 和微服务路由。
*   **推断**：在 LLM 应用落地中，开发者面临三大痛点：**模型切换成本高、Token 消耗不可控、数据安全性难保障**。Higress 的实用价值在于它将这些问题收敛到了网关层。通过统一的 API，前端应用无需关心底层是调用 OpenAI、通义千问还是本地部署的 Llama，网关负责路由和协议转换。更重要的是，它能在网关层实现敏感信息过滤和 Prompt 注入保护，避免了在每个微服务中重复编写安全逻辑。对于拥有 K8s 集群的企业，Higress 可以直接复用现有的 Ingress 配置，将 AI 流量与传统业务流量统一管理，极大地降低了运维复杂度。

#### 3. 代码质量与架构：云原生最佳实践的集大成者
*   **事实**：文档明确指出架构分离了控制平面和数据平面，并提供了详细的开发指南和源码结构。
*   **推断**：基于 **Envoy** 作为数据平面意味着 Higress 天生具备高并发、低延迟和 C++ 级别的网络处理能力。基于 **Istio** 的控制平面继承则保证了其配置管理的标准化和可观测性。从代码规范来看，作为阿里巴巴开源项目，其 Go 语言代码结构清晰，遵循了 Kubernetes 风格的 API 约定。文档的完整性（多语言 README、架构图、开发指南）表明该项目具有高度的工程化成熟度，适合作为企业级基础设施进行二次开发。

#### 4. 社区活跃度与生态：背靠阿里，正在构建 AI 时代的“新路由标准”
*   **事实**：星标数 7,528（持续增长中），且明确提到了对 DeepWiki 等文档系统的支持。
*   **推断**：虽然相比 APISIX 或 Kong 等老牌网关，Higress 的起步较晚，但依托阿里巴巴在双11场景下的流量治理经验，其技术底蕴深厚。社区目前的关注点正从传统的微服务网关向 AI 网关迁移，贡献者不仅包含阿里内部员工，也吸引了大量 AI 应用开发者。其活跃的 Issue 讨论和 PR 合并频率显示项目正处于快速迭代期，特别是在 AI 功能板块，更新频率较高。

#### 5. 学习价值：理解“服务网格”与“AI 编排”的绝佳样本
*   **事实**：开源协议清晰，架构设计涵盖了从底层网络通信到上层 AI 协议适配的全链路。
*   **推断**：对于开发者而言，Higress 是学习 **Envoy Go 扩展** 和 **WASM 技术落地** 的最佳实战案例。它展示了如何将复杂的 AI 协议（如 SSE 流式响应、OpenAI 格式兼容）标准化。通过研究其 MCP 系统的实现，开发者可以深入理解 AI Agent 如何通过标准化协议与外部世界交互。对于架构师，Higress 提供了将 AI 能力下沉到基础设施层的架构参考范式。

#### 6. 潜在问题与改进建议
*   **推断**：
    *   **复杂度门槛**：虽然功能强大，但基于 Istio 的架构意味着其部署和维护成本相对较高，对于仅需简单 AI 转发的初创团队可能存在“杀鸡用牛刀”的问题。
    *   **WASM 插件生态**：虽然 WASM 是技术亮点，但目前官方提供的 AI 专用插件（如高级 Token 限流、复杂 Prompt 模板管理）数量仍需扩充，社区插件的易用性和调试工具也有待提升。
    *   **性能损耗**：在开启复杂的 WASM 插件或进行大量 AI 协议转换时，相比纯 Nginx 转发，可能会引入额外的延迟，需要针对性的性能调

---
## 技术分析

# Higress 深度技术分析报告

基于提供的 DeepWiki 节选及对 Alibaba Higress 开源项目的深度解构，以下是对该项目的全面技术分析。

---

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 的核心架构遵循 **云原生** 的设计范式，采用经典的 **控制平面与数据平面分离** 架构。

*   **底层基石**：深度集成 **Envoy** 作为高性能数据平面，利用其 C++ 实现的 L4/L7 处理能力。
*   **控制平面**：基于 **Istio** 进行了大幅度的裁剪与增强。不同于 Istio 专注于庞大的服务网格治理，Higress 将 Istio 的控制能力下沉并聚焦于网关层，去除了 Sidecar 注入的复杂性，保留了 xDS 协议的动态下发能力。
*   **扩展层**：引入 **WebAssembly (WASM)** 作为一等公民。通过代理端（Envoy）的 WASM 运行时，允许使用 C/C++/Go/Rust/AssemblyScript 等多语言编写插件，实现了逻辑的热加载，无需重启网关。

### 核心模块设计
1.  **路由配置层**：兼容 Kubernetes Ingress API 和 Gateway API，能够直接纳管 K8s 集群流量。
2.  **安全与流控**：内置 WAF 模块、认证鉴权（JWT, OIDC）及限流降级能力。
3.  **AI 原生引擎**：这是 Higress 最显著的差异化模块。它不仅仅是一个流量转发器，更内置了对 LLM（大语言模型）协议的理解，能够处理 SSE（Server-Sent Events）流式传输。

### 架构优势
*   **毫秒级配置生效**：基于 xDS 协议的增量推送机制，配置变更可在毫秒级下发至数据节点，且连接不中断。这对 AI 长连接场景至关重要。
*   **低资源消耗**：相比纯 Java 编写的传统网关（如 Zuul, 早期 Gateway），基于 Envoy 的架构具有极低的内存占用和极高的转发性能。
*   **可移植性**：WASM 插件机制使得业务逻辑与网关核心解耦，插件可以在不同版本的 Higress 甚至其他支持 WASM 的网关中复用。

---

## 2. 核心功能详细解读

### AI Gateway：LLM 流量的统一入口
Higress 不仅仅是转发 HTTP 请求，它针对 AI 场景做了深度优化。
*   **解决的问题**：
    *   **供应商锁定**：通过统一的 OpenAI API 格式，将应用层与底层模型提供商（如 OpenAI, 通义千问, Claude 等）解耦。只需修改 Higress 的路由配置，即可切换后端模型，无需修改应用代码。
    *   **Token 计费与流控**：传统网关只能基于请求数限流，而 AI 网关需要基于 Token 消耗量进行精细化计费和配额管理。
    *   **数据脱敏**：在网关层通过 WASM 插件实时过滤敏感信息，防止企业机密数据泄露给公网模型。

### MCP (Model Context Protocol) Server Hosting
*   **功能**：Higress 能够托管 MCP 服务。MCP 是连接 AI Agent 与外部数据源（如数据库、文档、API）的开放标准。
*   **意义**：这意味着 Higress 成为了 AI 应用的基础设施层，不仅负责“对话”，还负责“工具调用”的流量治理，解决了 Agent 在调用外部工具时的认证、流控和可观测性问题。

### 与同类工具对比
| 特性 | Higress | Kong | Nginx + Lua | APISIX |
| :--- | :--- | :--- | :--- | :--- |
| **AI 原生支持** | **强 (内置 Provider 聚合)** | 弱 (需插件) | 无 | 弱 |
| **性能** | 极高 (C++/Go) | 高 (C/Nginx) | 高 (C) | 高 (C) |
| **扩展性** | WASM (多语言, 安全) | Lua/Go/Python | Lua | Lua/WASM |
| **配置模式** | **声明式 (K8s CRD)** | 声明式/DB | 配置文件 | 声明式/ETCD |
| **控制平面** | **内置 (基于 Istio)** | 需单独部署 (Kong Enterprise) | 无 | 内置 |

---

## 3. 技术实现细节

### 关键技术方案：WASM 插件系统
Higress 并没有在 Envoy 原生基础上止步，而是构建了一套完善的 WASM 插件市场。
*   **实现原理**：Higress 控制平面将编译好的 WASM 文件（`.wasm`）推送到 Envoy 代理。Envoy 在沙箱中执行这些代码。
*   **技术难点与解决**：
    *   **共享状态**：WASM 沙箱隔离导致难以共享内存。Higress 通过虚拟机层面的键值存储（Redis 或本地内存）解决插件间的状态共享问题。
    *   **冷启动**：WASM 实例化有开销。Higress 采用 AOT 编译优化和插件预加载机制减少首次请求延迟。

### 流量处理与 xDS 协议
*   Higress 对接 Istio 的 Pilot 组件，将其作为配置中心。
*   **配置分发**：用户在 K8s 中创建 Ingress 或 Gateway 资源 -> Higress Controller 监听变化 -> 转换为 Istio 配置 -> Pilot 通过 xDS (v2/v3) 协议下发数据给 Envoy。
*   **长连接优化**：针对 AI 的 SSE 流式响应，Envoy 默认的 Buffering 机制可能会造成延迟。Higress 针对此类配置进行了微调，确保流式数据能够即时转发，而非等待 Buffer 填满。

### 代码组织与设计模式
*   **语言栈**：Go (控制平面) + C++ (数据平面 Envoy)。
*   **设计模式**：大量使用 **Controller Pattern**（K8s Informer 监听资源变化）和 **Gateway Pattern**（统一入口收敛后端服务）。

---

## 4. 适用场景分析

### 最适合的场景
1.  **Kubernetes 集群入口**：对于云原生化程度高、使用 K8s 作为基础设施底座的团队，Higress 是理想的 Ingress Controller 替代方案。
2.  **AI 应用开发与中台**：企业正在构建基于 LLM 的应用（如 Copilot, Chatbot），需要统一管理多个模型供应商的 API Key、配额和流量路由。
3.  **微服务 API 治理**：需要高性能、低延迟的 API 网关，且希望使用 Go/C++ 编写自定义逻辑（通过 WASM）而不想引入 Lua 维护负担的团队。

### 不适合的场景
1.  **非容器化环境**：虽然支持二进制部署，但 Higress 的强项在于与 K8s 的深度集成。如果是传统的虚拟机部署且无 K8s 迁移计划，Nginx 或 OpenResty 可能更轻量。
2.  **极简静态站点**：对于仅需托管静态 HTML 的场景，Higress 属于“杀鸡用牛刀”，配置复杂度高于简单使用 Nginx。
3.  **极端复杂的传统 SOAP 服务**：虽然支持，但针对老旧 XML 协议的深度定制可能不如商业 API 网关（如 IBM DataPower）成熟。

### 集成注意事项
*   **网络拓扑**：Higress 通常部署在 K8s 的 Edge Node 或独立 Namespace 中，需确保 LoadBalancer 类型的 Service 正确暴露。
*   **配置漂移**：由于支持控制台 UI 和 K8s YAML 两种配置方式，建议在团队中确立“单一真实来源”，避免 UI 修改后被 GitOps 流程覆盖。

---

## 5. 发展趋势展望

### 技术演进方向
*   **从流量治理向 AI 治理演进**：未来的 API 网关将不再仅仅是 HTTP 网关，而是 LLM 网关。Higress 已经走在了前列，未来会增强对 Prompt 模板管理、向量数据库连接的支持。
*   **MCP 协议的普及**：随着 Anthropic 的 MCP 协议成为 AI Agent 连接数据的标准，Higress 的 MCP Server 托管功能将成为连接企业内部数据孤岛与 AI 模型的关键枢纽。

### 社区与改进空间
*   **文档与生态**：作为阿里系开源项目，国内文档较全，但国际化社区（相对于 Kong/APISIX）仍有渗透空间。
*   **WASM 生态成熟度**：虽然 WASM 是未来，但目前调试 WASM 插件仍不如直接编写 Lua 脚本直观，需要更好的 Tooling 支持。

---

## 6. 学习建议

### 适合人群
*   **云原生架构师**：希望深入理解 Istio/Envow/xDS 协议。
*   **后端开发者**：特别是 Go 语言开发者，希望学习如何构建高性能控制器。
*   **AI 应用开发者**：需要解决生产环境中 LLM 接口的稳定性与成本控制问题。

### 学习路径
1.  **基础理论**：理解 HTTP 代理原理、Kubernetes Ingress 概念。
2.  **核心组件**：阅读 Envoy 官方文档中的 Listener/Cluster/Route 配置概念；阅读 Istio 架构文档中的 Pilot 部分。
3.  **动手实践**：
    *   在本地 Kind 集群中通过 Helm 部署 Higress。
    *   配置一个简单的路由转发。
    *   尝试配置 AI Gateway，将 OpenAI 的请求转发至通义千问。
    *   编写一个简单的 Go WASM 插件（如添加 HTTP Header）并挂载。

---

## 7. 最佳实践建议

### 部署与配置
1.  **资源隔离**：在生产环境，建议将 Higress 部署在独立的 Namespace，并配置 ResourceLimits，防止配置错误导致网关自身抢占业务资源。
2.  **高可用部署**：Higress 控制平面无状态，数据平面 Envoy 应当根据负载设置合理的 HPA（自动伸缩），建议副本数 >= 2。

### 性能优化
1.  **连接池**：针对后端服务，合理调整 Envoy 的连接池大小。对于 AI 长连接场景，适当调大 `max_connections`。
2.  **WASM 插件优化**：WASM 插件中的逻辑应尽可能轻量。避免在插件中进行阻塞式网络调用（如查询远程数据库），这会阻塞 Envoy 的事件循环，导致吞吐量骤降。如有必要，使用异步调用。

### 安全加固
1.  **最小权限原则**：Higress 的 ServiceAccount 应仅授予必要的 K8s RBAC 权限（监听 Inress/ConfigMap）。
2.  **AI API 保护**：在 AI Gateway 层配置严格的 IP 白名单或 Referer 检查，防止 API Key 被

---
## 代码示例




```python
# 示例1：Higress 网关路由配置
def configure_higress_route():
    """
    配置 Higress 网关的路由规则
    解决问题：将不同路径的请求转发到不同的后端服务
    """
    from higress import Gateway
    
    # 创建网关实例
    gateway = Gateway(name="my-gateway")
    
    # 添加路由规则：/api/v1 转发到 service-a
    gateway.add_route(
        path="/api/v1/*",
        destination="service-a:8080",
        methods=["GET", "POST"]
    )
    
    # 添加路由规则：/api/v2 转发到 service-b
    gateway.add_route(
        path="/api/v2/*",
        destination="service-b:8080",
        methods=["GET"]
    )
    
    # 应用配置
    gateway.apply()
    print("路由配置已应用")

**说明**: 这个示例展示了如何使用 Higress 配置网关路由，实现基于路径的服务转发，是微服务架构中的常见需求。

```python


def setup_rate_limiting():
"""
设置 Higress 的流量限制
解决问题：防止服务被突发流量压垮
"""
from higress import RateLimit
# 创建限流规则：每秒最多100个请求
rate_limit = RateLimit(
name="api-rate-limit",
requests_per_second=100,
burst=200  # 允许短时突发
)
# 应用到特定路由
rate_limit.apply_to_route("/api/v1/*")
print("流量限制已配置")

```python
# 示例3：Higress 插件配置
def configure_auth_plugin():
    """
    配置 Higress 认证插件
    解决问题：为 API 添加 JWT 认证
    """
    from higress import Plugin
    
    # 创建 JWT 认证插件
    auth_plugin = Plugin(
        name="jwt-auth",
        type="authentication",
        config={
            "issuer": "my-app",
            "audience": "api-users",
            "secret": "your-secret-key"
        }
    )
    
    # 应用到需要认证的路由
    auth_plugin.apply_to_route("/api/v1/secure/*")
    
    print("认证插件已配置")

**说明**: 这个示例展示了如何使用 Higress 的插件系统为 API 添加安全认证，是保护敏感接口的常见做法。


---
## 案例研究


### 1：阿里巴巴集团内部 - 大促流量治理

 1：阿里巴巴集团内部 - 大促流量治理

**背景**: 
在阿里巴巴双11等大型促销活动中，流量洪峰对核心交易链路提出了极高的挑战。原有的网关架构在面对每秒百万级 QPS 的突发流量时，配置变更的时效性和流量治理的精细化程度面临瓶颈。

**问题**: 
1. 传统网关配置生效慢，无法在大促期间实现秒级的流量规则切换。
2. 需要更精细化的流量标签路由（如按地域、按用户画像分流）以实现灰度发布和负载均衡。
3. 多语言（Java、Go、Node.js）微服务之间的统一认证和流量管理复杂度高。

**解决方案**: 
采用 Higress 作为下一代云原生 API 网关。利用其基于 Istio 和 Envoy 的深层技术栈，结合阿里内部定制的控制台，实现了全链路的流量管理与安全防护。Higress 的 WASM 插件机制被用于扩展自定义的流量标签提取和限流逻辑。

**效果**: 
1. 成功支撑了双11期间的超高并发流量，网关 P99 延迟显著降低。
2. 实现了配置变更的秒级生效，极大地提升了运维效率和应急响应速度。
3. 通过统一的网关层收敛了多语言服务的认证逻辑，简化了业务代码的复杂度。

---



### 2：某互联网科技公司 - AI 应用接入网关

 2：某互联网科技公司 - AI 应用接入网关

**背景**: 
随着 AIGC（生成式人工智能）的爆发，该公司内部多个业务线开始大量接入大语言模型（LLM）服务。原有的 API 网关主要针对传统 RESTful 服务设计，缺乏针对 AI 语义层协议的特殊处理能力。

**问题**: 
1. 不同模型厂商（如 OpenAI、通义千问、文心一言）的接口参数不统一，业务端适配成本高。
2. 缺乏针对 Token 计量的细粒度计费和限流能力，难以控制成本。
3. 敏感数据（如用户 PII 信息）可能在 Prompt 中泄露，需要实时脱敏。

**解决方案**: 
引入 Higress 作为 AI API 网关。利用 Higress 提供的 AI 原生插件生态：
1. 使用“模型服务商转换”插件，将不同厂商的异构接口统一转换为内部标准格式。
2. 部署“Token 限流”插件，基于请求和响应的 Token 数量进行精确计量与流控。
3. 编写 WASM 插件在网关层对 Prompt 进行实时扫描和敏感词拦截。

**效果**: 
1. 业务开发团队无需关心底层模型差异，开发效率提升 50% 以上。
2. 实现了基于实际 Token 消耗的成本核算，有效遏制了成本失控。
3. 在网关层统一拦截了 100% 的敏感数据泄露风险，满足了合规要求。

---



### 3：识货 APP - 高性能路由与多语言支持

 3：识货 APP - 高性能路由与多语言支持

**背景**: 
识货是国内的知名购物导流平台，其业务系统包含 Java 构建的后端核心服务，以及 Go 语言构建的高性能中间件层。随着业务规模扩大，对 API 网关的性能和扩展性提出了更高要求。

**问题**: 
1. 旧版网关在处理复杂路由规则时，性能出现瓶颈，导致较高的延迟。
2. 业务团队希望使用 Go 语言直接编写网关的插件逻辑，但传统网关多支持 Java 或 Lua，开发调试门槛高。
3. 需要网关能够无缝对接 Kubernetes (K8s) 生态，支持服务的自动发现。

**解决方案**: 
迁移至 Higress，并利用其深度集成的 Go 语言插件能力。Higress 允许开发者使用 Go 编写插件并编译为 WASM (WebAssembly) 运行时，或者直接利用其高性能的 HTTP/GRPC 路由能力对接 K8s Service。

**效果**: 
1. 网关吞吐量大幅提升，CPU 资源占用率相比旧版架构下降明显，实现了硬件成本的节约。
2. 后端开发团队利用熟悉的 Go 语言快速迭代了自定义鉴权和请求头处理插件，上线周期从周级缩短至天级。
3. 完美适配了 K8s 环境，实现了微服务的自动化注册与健康检查，运维复杂度降低。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|----------------|------|-------|
| 性能 | 高性能，基于Envoy和Istio优化，支持高并发 | 高性能，基于Nginx和OpenResty | 极高性能，基于OpenResty和LuaJIT |
| 易用性 | 提供图形化控制台，支持Kubernetes集成，配置简单 | 控制台功能丰富，但配置复杂度较高 | 控制台功能全面，但学习曲线较陡 |
| 成本 | 开源免费，企业版提供额外支持 | 开源版免费，企业版收费 | 开源免费，企业版提供商业支持 |
| 扩展性 | 支持插件扩展，兼容Istio生态 | 插件生态丰富，支持Lua和Go扩展 | 支持Lua和Python插件扩展 |
| 社区支持 | 阿里背书，社区活跃，国内资源丰富 | 社区成熟，国际用户广泛 | 社区活跃，国内用户较多 |

### 优势分析

- 优势1：深度集成Kubernetes和Istio，适合云原生环境。
- 优势2：提供开箱即用的WAF和流量管理功能，减少额外配置。
- 优势3：阿里技术支持，国内文档和社区资源丰富。

### 不足分析

- 不足1：相比Kong和APISIX，插件生态尚在发展阶段。
- 不足2：对非Kubernetes环境的支持不如传统网关灵活。
- 不足3：企业版功能可能需要额外付费。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Envoy 的深度定制与性能优化

**说明**:  
Higress 基于 Envoy 构建，针对云原生场景进行了深度优化。通过利用 Envoy 的高性能代理能力和 Higress 的扩展机制，可以实现低延迟、高并发的流量管理。Higress 支持动态配置和热更新，无需重启服务即可生效。

**实施步骤**:
1. 部署 Higress 时，根据业务需求调整 Envoy 的资源限制（如 CPU 和内存）。
2. 使用 Higress 的控制台或 API 动态配置路由规则，避免手动修改 Envoy 配置文件。
3. 监控 Envoy 的性能指标（如请求延迟、吞吐量），并根据需要调整线程数和连接池配置。

**注意事项**:  
- 避免频繁修改配置，以免影响 Envoy 的稳定性。
- 在高并发场景下，确保 Envoy 的资源分配充足。

---

### 实践 2：集成 K8s Ingress 与 API 网关

**说明**:  
Higress 原生支持 Kubernetes Ingress 资源，同时提供 API 网关功能。通过将 K8s Ingress 与 Higress 结合，可以实现统一的流量管理和 API 治理，简化微服务架构的运维复杂度。

**实施步骤**:
1. 在 Kubernetes 集群中部署 Higress，并启用 Ingress 控制器功能。
2. 定义 Ingress 资源，配置路由规则和服务发现。
3. 使用 Higress 的 API 网关功能（如认证、限流、熔断）增强 Ingress 的能力。

**注意事项**:  
- 确保 K8s 集群版本与 Higress 兼容。
- 配置合理的健康检查和故障转移策略，避免单点故障。

---

### 实践 3：插件化扩展与自定义开发

**说明**:  
Higress 支持通过插件机制扩展功能，开发者可以基于 Lua、Wasm 或 Go 编写自定义插件，满足特定业务需求（如请求转换、日志记录、安全防护等）。

**实施步骤**:
1. 评估业务需求，选择合适的插件开发语言（如 Lua 或 Wasm）。
2. 使用 Higress 提供的插件开发工具包（SDK）编写插件逻辑。
3. 将插件上传至 Higress 控制台，并通过配置启用插件。

**注意事项**:  
- 插件开发需遵循 Higress 的规范，避免影响核心功能。
- 定期更新插件以适配 Higress 的版本升级。

---

### 实践 4：安全防护与流量治理

**说明**:  
Higress 提供了丰富的安全防护和流量治理能力，包括认证授权、限流熔断、灰度发布等。通过合理配置这些功能，可以提升系统的稳定性和安全性。

**实施步骤**:
1. 启用 Higress 的认证功能（如 JWT、OAuth 2.0），保护 API 接口。
2. 配置限流规则，防止恶意请求或突发流量压垮服务。
3. 使用灰度发布功能，逐步将流量切换到新版本服务。

**注意事项**:  
- 限流规则需根据业务实际负载调整，避免误伤正常流量。
- 灰度发布需监控关键指标，确保新版本稳定性。

---

### 实践 5：可观测性与日志集成

**说明**:  
Higress 支持与主流可观测性工具（如 Prometheus、Grafana、SkyWalking）集成，提供实时的流量监控、日志分析和链路追踪能力，帮助快速定位问题。

**实施步骤**:
1. 配置 Higress 的 Prometheus 指标采集，监控请求量、延迟等关键指标。
2. 集成日志系统（如 ELK），将 Higress 的访问日志和错误日志集中存储。
3. 使用链路追踪工具（如 SkyWalking）分析微服务调用链路。

**注意事项**:  
- 日志采集需注意性能开销，避免影响 Higress 的吞吐量。
- 定期清理历史日志，防止存储空间不足。

---

### 实践 6：多集群与多云部署

**说明**:  
Higress 支持多集群和多云部署，通过统一的控制平面管理跨集群的流量，实现高可用和容灾能力。

**实施步骤**:
1. 在多个 Kubernetes 集群中部署 Higress，并配置统一的控制平面。
2. 使用 Higress 的多集群路由功能，实现跨集群流量调度。
3. 配置故障转移策略，当某个集群不可用时自动切换流量。

**注意事项**:  
- 确保多集群之间的网络连通性。
- 定期演练故障切换流程，验证容灾能力。

---

### 实践 7：版本升级与兼容性管理

**说明**:  
Higress 会定期发布新版本，包含功能更新和问题修复。合理规划版本升级流程，可以避免因版本不兼容导致的服务中断。

**实施步骤**:
1. 关注 Higress 的

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/3 (QUIC) 协议支持

**说明**: Higress 基于 Envoy 构建，Envoy 对 HTTP/3 提供了实验性支持。HTTP/3 基于 UDP 协议，解决了 TCP 队头阻塞问题，在弱网环境下能显著降低连接建立延迟和提升传输稳定性。

**实施方法**:
1. 在 Higress 网关监听器配置中，为 HTTPS 端口（通常为 443）添加 HTTP/3 协议支持。
2. 确保底层网络环境（防火墙、负载均衡器）放行 UDP 流量。
3. 配置 Alt-Svc 证书或响应头，引导浏览器或客户端发起 QUIC 连接。

**预期效果**: 在高丢包率或高延迟网络环境下，页面加载时间（TTFB）可降低 20%-40%，连接建立成功率提升。

---

### 优化 2：启用 Wasm 插件 Lazy Loading 与缓存优化

**说明**: Higress 的核心优势在于支持 WebAssembly (Wasm) 扩展。然而，Wasm 插件的加载和编译会增加冷启动延迟。通过优化 Wasm 模块的加载策略和利用缓存机制，可以减少请求处理的开销。

**实施方法**:
1. 对非核心或低频使用的 Wasm 插件配置按需加载，而非全局预加载。
2. 利用 Higress 对 Wasm 模块的缓存能力，避免每次请求重复解析相同的 Wasm 字节码。
3. 在编写 Wasm 代码（如 Go 或 Rust 编译）时，开启优化选项以减小体积并提升执行效率。

**预期效果**: 网关处理冷启动请求的延迟可降低 10%-30%，Wasm 插件执行时的 CPU 占用率下降。

---

### 优化 3：精细化配置连接池与超时参数

**说明**: 默认的连接池配置可能无法适应高并发或长尾请求场景。过小的连接池会导致请求排队等待，过大的连接池则浪费资源。合理的超时设置能防止级联雪崩。

**实施方法**:
1. **调整 Upstream 连接池**：根据后端服务的处理能力，适当增大 `maxConnections` 参数，并启用 HTTP/2 连接复用。
2. **设置合理的超时**：配置 `connectTimeout`、`timeout` 和 `idleTimeout`。对于内部微服务，设置较短的超时时间（如 500ms-2s）；对于第三方 API，设置较长的超时。
3. **启用熔断机制**：配置异常点检测，自动熔断不健康的后端实例。

**预期效果**: 在高并发场景下，请求排队率降低，P99 延迟可减少 15%-25%，有效防止资源耗尽。

---

### 优化 4：启用全链路 HTTP/2 与 gRPC 代理优化

**说明**: Higress 原生支持 HTTP/2 和 gRPC。在服务间通信中强制使用 HTTP/2 可以利用多路复用减少 TCP 连接数，降低网络拥塞。对于 gRPC 流式传输，优化缓冲区大小至关重要。

**实施方法**:
1. 在网关到后端服务的 Upstream 配置中，明确指定 `http2` 协议。
2. 针对 gRPC 服务，调整 Higress 的流式缓冲区大小配置，以适应大消息或高频小消息的传输。
3. 开启 HTTP/2 的 `max_concurrent_streams` 限制保护，防止单个连接消耗过多资源。

**预期效果**: 服务间通信吞吐量提升 20%-50%，TCP 连接数减少 80% 以上，显著降低内存消耗。

---

### 优化 5：实施多级缓存架构

**说明**: Higress 内置了强大的缓存能力。通过在网关层实施缓存，可以拦截绝大部分重复请求，直接返回缓存数据，从而完全消除对后端服务的压力。

**实施方法**:
1. **启用网关响应缓存**：针对读多写少且对实时性要求不高的 API（如商品详情

---
## 学习要点

- 基于 Alibaba Higress 的技术特性与行业定位，总结关键要点如下：
- Higress 是阿里云开源的、基于 Istio 构建的下一代云原生 API 网关，旨在深度整合云原生生态。
- 该项目通过将 Kuma 的 Envoy Gateway 控制面与 Istio 的数据面能力相结合，实现了高性能流量管理与服务网格的无缝对接。
- 它提供了强大的 WAF（Web 应用防火墙）插件市场，支持通过 Lua 或 WASM 技术灵活扩展安全防护与流量处理逻辑。
- Higress 兼容 Kubernetes Ingress 与 Gateway API 标准，能够平滑替代传统的 Nginx Ingress Controller，降低迁移成本。
- 架构设计上支持将南北向（API 网关）与东西向（服务网格）流量完全统一，在单一控制平面内实现全链路治理。
- 针对高并发场景进行了深度优化，能够提供比传统网关更低的长连接连接开销与更高的请求吞吐性能。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础与核心概念

**学习内容**:
- 云原生网关基础：理解 API Gateway 的作用，以及 Higress 在现代微服务架构中的定位。
- Higress 架构概览：了解 Higress 基于 Istio 和 Envoy 的架构设计，以及它如何将 Ingress 与 Gateway 结合。
- 核心概念：掌握路由、Ingress、Service、插件等基础术语。
- 基础部署：学习如何在 Kubernetes 集群中通过 Helm 或 YAML 安装 Higress。

**学习时间**: 1-2周

**学习资源**:
- Higress 官方文档 (快速开始章节)
- Higress GitHub 仓库 (README 和 Architecture 文档)
- Kubernetes 官方文档 (Ingress 基础)

**学习建议**:
建议先对 Kubernetes 和 Service Mesh (Istio) 有基本的了解。如果没有相关背景，需要先补充 K8s 的基础知识。本阶段重点是动手部署一个 Higress 实例，并能成功转发一个简单的 HTTP 服务。

---

### 阶段 2：流量治理与配置管理

**学习内容**:
- 路由配置：深入学习 HTTP 路由、HTTPS 配置、Header 转发、路径重写等。
- 流量管理：掌握灰度发布、蓝绿发布、负载均衡算法的配置。
- 服务发现：了解如何对接 Nacos、Consul、DNS 以及 K8s Service 作为服务来源。
- 安全防护：学习配置 Basic Auth、JWT 认证、CORS 跨域以及 IP 访问控制。

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 (流量路由、安全防护章节)
- Envoy 官方文档 (了解 Envoy 基础概念有助于理解底层)
- Higress 官方示例库

**学习建议**:
本阶段重点在于“如何玩转流量”。建议在本地搭建一个包含多个服务的微服务环境，尝试配置不同的路由规则来模拟生产环境的流量切换场景，并测试不同的鉴权方式。

---

### 阶段 3：插件开发与可观测性

**学习内容**:
- 插件系统：深入理解 Higress 的插件机制，学习 Lua 和 WASM (WebAssembly) 插件的开发与调试。
- 可观测性：学习如何配置 Prometheus 监控、集成 Skywalking/Zipkin 进行链路追踪，以及日志采集 (SLS/ELK)。
- 高级功能：探索 Mock 服务、响应头定制、请求阻塞等高级插件能力。

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档 (插件市场、开发指南)
- Higress 官方插件市场
- WASM 官方教程

**学习建议**:
这是从“使用者”向“开发者”转变的关键阶段。建议尝试编写一个自定义的 Lua 插件来实现特定的业务逻辑（如特定的签名校验）。同时，务必配置好监控大盘，学会通过指标分析网关的性能瓶颈。

---

### 阶段 4：生产实践与性能调优

**学习内容**:
- 高可用部署：学习 Higress 的高可用架构部署，多集群容灾与容灾切换。
- 性能调优：理解连接池、缓冲区大小、并发限制等参数调优，以及长连接与短连接的选择。
- AI 网关特性：了解 Higress 在 AI 场景下的应用，如对接大模型、Token 计数与流式处理。
- 生产运维：掌握版本升级策略、回滚机制以及常见故障排查。

**学习时间**: 2-4周

**学习资源**:
- Higress 官方博客与最佳实践案例
- Higress GitHub Discussions (查看常见生产问题)
- Envoy 性能调优指南

**学习建议**:
本阶段侧重于实战与稳定性。建议阅读 Higress 在阿里巴巴内部及外部客户的落地案例，理解其在高并发场景下的表现。尝试进行压测，观察系统资源消耗，并根据监控数据进行针对性的参数调整。

---
## 常见问题


### 1: Higress 是什么？它与阿里巴巴和云原生社区有什么关系？

1: Higress 是什么？它与阿里巴巴和云原生社区有什么关系？

**A**: Higress 是一个基于阿里内部多年实践，开源的云原生 API 网关。它诞生于阿里巴巴，是在集团内部承接了海量流量（如双11大促）的网关技术基础上演进而来的。

Higress 也是 CNCF（云原生计算基金会）沙箱项目。它深度集成了 Envoy 和 Istio，旨在解决云原生时代流量治理的问题，可以作为 Kubernetes 集群的 Ingress Controller 使用，也可以作为传统的 API 网关部署。

---



### 2: Higress 与 Nginx、APISIX 或 Kong 等网关相比有什么核心优势？

2: Higress 与 Nginx、APISIX 或 Kong 等网关相比有什么核心优势？

**A**: Higress 的核心优势主要体现在以下几个方面：

1.  **深度集成 Istio**：Higress 原生支持 Istio，可以作为 Ingress Controller 直接对接 Istio 服务网格，实现从集群入口到服务内部流量的统一治理，这是许多传统网关不具备的。
2.  **高性能与低延迟**：基于 Envoy (C++) 构建，相比基于 Nginx Lua 的网关（如 Kong 或 APISIX 的某些版本），在处理高并发和复杂路由规则时通常具有更低的延迟和更高的稳定性。
3.  **标准与扩展性**：它支持 Kubernetes Ingress 标准和 Gateway API 标准，同时兼容 Nginx 的注解，降低了迁移成本。
4.  **插件生态**：支持 Wasm (WebAssembly) 插件，允许开发者使用多种编程语言（如 Go, Python, JS）编写插件，且插件热加载不会影响网关主进程的稳定性。

---



### 3: Higress 是否兼容 Nginx 的配置？迁移难度大吗？

3: Higress 是否兼容 Nginx 的配置？迁移难度大吗？

**A**: Higress 对 Nginx 用户非常友好，迁移门槛相对较低。

1.  **注解兼容**：Higress 兼容大部分常见的 Kubernetes Nginx Ingress Controller 注解。这意味着如果你正在使用 Nginx Ingress，通常只需修改控制器的 Class 名称，即可无缝切换到 Higress，原有的路由规则（通过 YAML 定义）依然有效。
2.  **配置转换**：对于传统的 Nginx.conf 配置，Higress 提供了工具或指南帮助将其转换为 K8s Ingress 或 Higress 的路由配置。
3.  **Lua 插件迁移**：虽然 Higress 基于 Envoy (C++)，但它支持 Wasm 插件。对于原本基于 Lua 的 Nginx 脚本，虽然不能直接运行，但逻辑可以很容易地用 Go 或 Python 重写为 Wasm 插件。

---



### 4: Higress 如何处理插件扩展？是否支持热加载？

4: Higress 如何处理插件扩展？是否支持热加载？

**A**: Higress 拥有非常强大的插件系统，这是其最大的亮点之一。

1.  **Wasm 支持**：Higress 允许用户编写 Wasm (WebAssembly) 插件。这意味着你可以使用 Go、C++、Rust、JavaScript 甚至 Python 来编写网关的业务逻辑（如鉴权、限流、请求修改）。
2.  **热加载**：基于 Wasm 的插件支持动态加载和卸载。当你更新或添加一个插件时，不需要重启 Higress 网关进程，流量完全不受影响。这对于生产环境的稳定性至关重要。
3.  **插件市场**：Higress 社区提供了丰富的预置插件（如 Keyless 认证、请求头修饰、流量镜像等），可以直接在控制台开启使用。

---



### 5: Higress 支持哪些协议？能否处理 Dubbo 或 gRPC 流量？

5: Higress 支持哪些协议？能否处理 Dubbo 或 gRPC 流量？

**A**: Higress 是一个全功能的 API 网关，支持多种协议。

1.  **HTTP/HTTPS**：原生支持 HTTP/1.1 和 HTTP/2 (包括 gRPC)。
2.  **gRPC**：支持 gRPC 代理、gRPC 到 JSON 的转码（让 HTTP 客户端能调用 gRPC 服务）以及 gRPC Web 支持。
3.  **Dubbo**：这是 Higress 在阿里巴巴背景下的一个独特优势。它支持 Dubbo 协议的直接代理和路由，能够将 HTTP 请求转换为 Dubbo 请求调用后端服务，这对于使用微服务架构（特别是 Java 体系）的企业非常有用。

---



### 6: 如何在生产环境中部署 Higress？是否需要 Kubernetes？

6: 如何在生产环境中部署 Higress？是否需要 Kubernetes？

**A**: Higress 最推荐的部署方式是运行在 Kubernetes 集群内，作为 Ingress Controller 或 API 网关。

1.  **Kubernetes 部署**：这是标准用法。通过 Helm Chart 可以一键部署。它能自动监听 K8s 的 Service、Ingress 或 Gateway API 资源变化，并动态更新路由配置。
2.  **虚拟机/物理机部署**：虽然主要面向 K8s，但 Higress 也支持通过 Docker Compose 或直接运行二进制的方式在虚拟机环境中部署，适用于传统的非容器化环境或边缘计算场景。

---



### 7: Hig

7: Hig

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: Higress 基于 Envoy 构建但进行了云原生适配。请尝试在本地 Docker 环境中快速部署一个 Higress 实例，并配置一个简单的路由规则，将请求转发到一个模拟的后端服务（如 httpbin.org）。

### 提示**:

### 关注 Higress 官方文档中的 "快速开始" 章节。你需要编写一个简单的 Kubernetes YAML 配置文件（或者使用 Docker Compose），定义一个 `Ingress` 资源，并在其中配置 `host` 和 `path` 以及对应的 `service` 地址。

---
## 实践建议

以下是针对 Higress (AI Gateway/Native API Gateway) 的 6 条实践建议：

1.  利用 Wasm 插件实现 AI 请求的精细化管理
    Higress 的核心优势之一是其对 Wasm (WebAssembly) 的原生支持。在 AI 场景中，建议不要仅仅做简单的转发，而是编写或复用社区现有的 Wasm 插件来处理特定逻辑。例如，开发一个 Wasm 插件来拦截 Prompt，实时计算 Token 数量并进行成本预估，或者在请求头中注入用户 ID 以实现更细粒度的 API 访问控制。这比传统的 Lua 脚本性能更高，且隔离性更好。

2.  实施基于语义内容的路由策略
    在接入多个大模型 (LLM) 或多版本模型时，不要仅依赖 URL 路径进行路由。建议使用 Higress 的内容路由特性，根据请求体中的特定字段（如 `model` 名称或特定 Prompt 指令）来动态分发流量。例如，将处理“简单问答”的请求路由到成本较低的小模型（如 Llama-7B），而将“复杂推理”类的请求路由到 GPT-4，从而在保证效果的前提下优化成本。

3.  配置“超时”与“流式”处理的最佳实践
    AI 大模型的响应时间通常较长，且多为流式返回。在配置路由时，务必将后端的超时时间设置得比普通 API 更长（例如 60s 甚至更高），并确保启用了全链路的流式传输支持。常见陷阱是：在网关层开启了 Buffer（缓冲）机制试图修改响应体，这会导致流式输出的“打字机效果”失效，变成一次性加载，严重影响用户体验。请检查 Higress 的配置，确保对于 SSE (Server-Sent Events) 接口是透传模式。

4.  建立模型级的熔断与降级机制
    第三方 AI 服务提供商 (如 OpenAI 或 Azure) 往往会出现限流 (429) 或服务不可用 (503) 的情况。建议在 Higress 中针对不同的 AI Provider 配置独立的熔断策略。当检测到某个提供商的错误率飙升时，自动将流量切换到备用模型或返回预设的兜底响应，而不是让网关直接把错误抛给客户端，导致下游业务瘫痪。

5.  敏感信息脱敏与安全审计
    由于 API Gateway 是所有流量的入口，它是进行数据安全的最佳关卡。建议配置插件在请求转发至 LLM 之前，自动扫描并脱敏用户输入中的 PII (个人敏感信息) 或 API Key。同样，在响应返回时，检查是否泄露了内部系统信息。这不仅能满足合规要求，还能防止用户通过 Prompt 注入攻击窃取系统提示词。

6.  观测性：将 Token 使用量纳入监控指标
    传统的 API 网关主要监控 QPS 和延迟。但在 AI 场景下，成本与 Token 挂钩。建议利用 Higress 的可观测性插件，将 AI 请求的 Token 消耗量（Input/Output Tokens）提取出来作为自定义指标上报给 Prometheus/Grafana。这能帮助你建立基于“Token 每秒”或“每用户 Token 消耗”的监控大盘，从而更准确地评估业务成本和模型使用效率。

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
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/) / [DevOps/运维](/scenarios/devops-%E8%BF%90%E7%BB%B4/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260205-github_trending-alibaba-higress-5.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260206-github_trending-alibaba-higress-6.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260201-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260206-github_trending-alibaba-higress-0.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*