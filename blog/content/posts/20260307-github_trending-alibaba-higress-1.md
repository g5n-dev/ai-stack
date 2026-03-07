---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-03-07T07:40:49+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "阿里开源", "Istio", "Envoy", "LLM", "MCP 协议"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "**Higress 项目总结** **1. 项目概况** Higress 是由阿里云开源的一款**云原生 API 网关**。该项目基于 **Istio** 和 **Envoy** 构建，并创新性地集成了 **WebAssembly (WASM)** 插件能力。它被定义为一款“AI Native”网关，旨在为云原生应用和"
external_url: https://github.com/alibaba/higress
scenarios: ["AI/ML项目", "云原生/容器", "Kubernetes"]
---

# 阿里开源 Higress：AI 原生 API 网关

> **原名**: alibaba /

      higress

---

## 基本信息

- **描述**: 🤖 AI 网关 | AI 原生 API 网关
- **语言**: Go
- **星标**: 7,677 (+17 stars today)
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

Higress 是一款基于 Istio 和 Envory 构建的云原生 API 网关，它通过集成 WASM 插件能力，同时支持传统流量管理与 AI 原生场景。该项目专为需要统一处理微服务路由、Kubernetes Ingress 以及大模型应用流量的开发者设计，能够有效解决异构环境下的服务治理与模型集成问题。本文将介绍其系统架构，并重点解析 AI 网关特性、MCP 系统服务托管以及核心的插件扩展机制。

---
## 摘要

**Higress 项目总结**

**1. 项目概况**
Higress 是由阿里云开源的一款**云原生 API 网关**。该项目基于 **Istio** 和 **Envoy** 构建，并创新性地集成了 **WebAssembly (WASM)** 插件能力。它被定义为一款“AI Native”网关，旨在为云原生应用和 AI 大模型应用提供统一的流量管理入口。

**2. 核心架构**
*   **技术栈**：使用 **Go** 语言编写，分离了控制平面与数据平面。
*   **高性能**：配置变更通过 xDS 协议传播，延迟仅为毫秒级，且支持连接无中断，特别适合 AI 长连接流式响应场景。
*   **兼容性**：作为 Kubernetes Ingress 控制器，兼容 nginx-ingress 注解。

**3. 三大核心功能**
Higress 的应用场景主要涵盖以下三个维度：

*   **AI 网关**
    *   **功能**：为 AI 应用提供统一 API，支持 30+ 家大语言模型（LLM）提供商。
    *   **特性**：具备协议转换、可观测性、缓存以及安全防护能力。
    *   **组件**：包含 `ai-proxy`（代理）、`ai-statistics`（统计）、`ai-cache`（缓存）等插件。

*   **MCP 服务器托管**
    *   **功能**：托管模型上下文协议（MCP）服务器，使 AI Agent 能够便捷地调用外部工具和服务。
    *   **组件**：包含 `mcp-router`、`jsonrpc-converter` 以及 `quark-search`、`amap-tools` 等具体服务实现。

*   **传统 API 网关**
    *   **功能**：处理标准的微服务路由和 Kubernetes Ingress 流量管理。

**4. 项目现状**
*   **GitHub 仓库**：`alibaba/higress`
*   **热度**：拥有超过 7,600 个 Star，活跃度较高（今日 +17）。

---
## 评论

### 总体判断

Higress 是目前云原生网关领域中将**AI 原生能力**与**传统流量治理**结合得最紧密的开源项目之一。它成功将 Istio 的控制平面能力下沉，并通过 WASM 技术实现了极高的扩展性，是构建 LLM 应用网关和生产级 API 网关的优选方案。

### 深入评价分析

**1. 技术创新性：从“流量侧”转向“模型侧”的架构延伸**
*   **事实：** Higress 基于 Istio 和 Envoy 构建，核心差异化在于集成了 AI Gateway 特性和 MCP (Model Context Protocol) Server 托管能力，并支持 WASM 插件。
*   **推断：** 传统网关（如 Nginx, Kong）主要关注 HTTP 请求的路由与负载均衡，而 Higress 创新性地将协议理解延伸到了 LLM 上下文。它不仅是流量的管道，更是 AI 代理的“大脑前庭”。通过内置对 MCP 的支持，它解决了 AI Agent 调用外部工具时的标准化连接问题；利用 WASM，它允许开发者使用 C++/Go/Rust/AssemblyScript 编写高频插件，这种**“热更新 + 低代码扩展”**的架构，比传统的 Lua (OpenResty) 或 Java (Zuul) 插件模型在安全性和隔离性上更具前瞻性。

**2. 实用价值：统一云原生与 AI 场景的流量入口**
*   **事实：** README 明确指出其提供三大核心功能：AI Gateway、MCP Server Hosting、传统 API Gateway（K8s Ingress）。
*   **推断：** Higress 极具实用价值，因为它解决了企业数字化转型中的“分裂”痛点。企业不需要维护一套 K8s Ingress（如 Nginx Ingress）再单独部署一套 AI 代理（如 LangServe）。Higress 允许在同一个控制平面下，既处理微服务间的 gRPC/REST 调用，又处理向 OpenAI/Ollama 的 LLM 请求。特别是其**“MCP Server Hosting”**功能，使得部署 AI 工具变得像部署一个微服务一样简单，极大地降低了 AI 应用的落地门槛。

**3. 代码质量与架构设计：控制平面与数据平面的解耦**
*   **事实：** 架构上明确分离了控制平面（配置管理）和数据平面（基于 Envoy 的流量处理），并提供了多语言 README。
*   **推断：** 作为阿里系开源项目，Higress 继承了阿里巴巴内部高并发流量的治理经验。代码结构清晰，遵循云原生标准。其对 Envoy 的二次开发并非简单的 Fork，而是通过 Istio 进行了标准的控制平面对接，这意味着架构具有良好的可维护性。文档的完整性（中英日三语）也体现了其作为国际化项目的成熟度，降低了开发者的上手成本。

**4. 社区活跃度与生态：背靠阿里，快速迭代**
*   **事实：** 星标数 7,677（基于提供的数据），且明确有 DeepWiki 等详细文档支持。
*   **推断：** 虽然在 CNCF 生态中它不如 APISIX 或 Kong 历史悠久，但背靠阿里巴巴和 Higress 开源社区，其迭代速度极快，特别是在 AI 相关功能的更新上。社区活跃度较高，对于国内开发者而言，中文文档的完善度和社区响应速度是其相比国外同类项目的巨大优势。

**5. 学习价值与借鉴意义：WASM 插件化最佳实践**
*   **事实：** 项目包含 WASM Plugin System 和 Development Guide。
*   **推断：** Higress 是学习**“云原生网关 2.0”**架构的极佳范本。开发者可以从中学习如何将 Envoy 的高性能与 WASM 的灵活性结合，以及如何设计一个兼容 K8s Ingress 规范的同时又支持私有协议（如 SSE 流式传输）的网关系统。对于想要构建 PaaS 平台或 Serverless 平台的团队，其控制平面的架构设计具有很高的参考价值。

**6. 潜在问题与改进建议**
*   **推断：** 尽管功能强大，Higress 的部署复杂度相对较高。相比于一个简单的 Nginx 配置，理解 Istio + Envoy + Higress Console 的全链路架构需要较高的学习曲线。此外，虽然 AI 功能新颖，但在极端高并发下的 LLM 流式传输（SSE）性能优化和 Token 计费准确性方面，仍需经过更多生产环境的验证。

**7. 对比优势**
*   **对比 APISIX/Kong：** APISIX 基于 Lua，Kong 基于 Nginx/OpenResty，它们在传统 API 网关领域非常成熟，但在 AI 原生特性（如内置 MCP、LLM 协议转换）上不如 Higress 专注。Higress 的 WASM 支持也比 Lua 插件在多语言支持和沙箱隔离性上更胜一筹。
*   **对比 Envoy Gateway：** Envoy Gateway 是 K8s Gateway API 的标准实现，但主要聚焦于基础的南北向流量。Higress 在此基础上增加了对 AI 场景的深度定制，更适合作为企业级的业务网关而非单纯的集群入口。

### 边界条件与验证清单

**不适用场景：**
*   边缘计算或资源极度受限的嵌入式环境（Envoy 资源占用较高）。

---
## 技术分析

# Higress 深度技术分析报告

基于 Alibaba 开源的 Higress 项目（AI Native API Gateway），以下是从技术架构、核心功能、实现细节、适用场景、发展趋势、学习建议、最佳实践以及工程哲学八个维度的深度分析。

---

## 1. 技术架构深度剖析

Higress 的架构设计体现了**“云原生+”**的演进思路，它不仅仅是 Kong 或 APISIX 的竞品，更是 Istio 生态在 API 网关领域的垂直落地与增强。

### 技术栈与架构模式
*   **底层引擎**：基于 **Envoy** 构建。Envoy 采用 C++ 编写，具备高性能的 L7 处理能力和强大的可观测性。Higress 直接利用 Envoy 作为数据平面，避免了重复造轮子，继承了其高并发和低延迟的优势。
*   **控制平面**：基于 **Istio** 优化。Higress 并没有从零构建控制平面，而是对 Istio 进行了剪裁和优化，去除了 Service Mesh 中繁重的 Sidecar 注入逻辑，保留了核心的 xDS 配置下发机制。
*   **扩展语言**：**Go**（控制平面）与 **WebAssembly (WASM)**（数据平面扩展）。Higress 使用 Go 编写控制逻辑，利用 WASM 作为插件扩展机制，实现了业务逻辑与网关内核的解耦。

### 核心模块与关键设计
1.  **控制平面与数据平面分离**：
    *   配置变更通过 xDS 协议（包括 LDS, RDS, CDS, EDS）毫秒级推送到数据平面。
    *   这种分离架构支持**热更新**，在 AI 流式响应等长连接场景下，配置变更不会导致 TCP 连接中断，这是传统 Nginx reload 模式无法比拟的。
2.  **WASM 插件系统**：
    *   这是 Higress 的核心亮点。通过引入 Proxy-WASM 规范，允许开发者使用 Go、C++、Rust 甚至 JavaScript/TypeScript（AssemblyScript）编写插件。
    *   插件运行在沙箱环境中，动态加载，无需重启网关，且内存隔离保证了网关的稳定性。

### 架构优势分析
*   **性能损耗极低**：数据路径完全由 Envoy (C++) 处理，控制路径逻辑下沉为 WASM，性能接近原生。
*   **生态兼容性**：完全兼容 K8s Ingress API 和 Istio Gateway API，降低了从传统 Ingress Controller 迁移的门槛。

---

## 2. 核心功能详细解读

Higress 的核心定位从“流量网关”进化为“AI 网关”，其功能集紧扣当前 LLM（大语言模型）应用落地的痛点。

### 主要功能与场景
1.  **AI 网关**：
    *   **统一模型接入**：通过一套标准 API 接入 OpenAI、Azure、通义千问、HuggingFace 等不同厂商的模型。
    *   **Token 管理与计费**：自动处理 Prompt 和 Completion 的 Token 统计，支持基于 Token 的流式计费和限流。
    *   **提示词增强**：在网关层动态插入系统提示词，实现统一的安全围栏或上下文注入，无需修改后端应用代码。
2.  **MCP (Model Context Protocol) 服务器托管**：
    *   Higress 内置了对 MCP 协议的支持，能够作为 AI Agent 的工具调度中心。它可以将后端微服务自动暴露为 MCP 工具，让 LLM 能够安全、标准化地调用企业内部 API。
3.  **传统 API 网关能力**：
    *   支持 K8s Ingress、微服务路由、金丝雀发布、负载均衡、认证鉴权（JWT, OIDC, AK/SK）。

### 解决的关键问题
*   **AI 路由的复杂性**：解决了企业需要对接多家 LLM 厂商 SDK 的繁琐问题，统一了接口标准。
*   **流式传输的不可控性**：在 SSE (Server-Sent Events) 流式传输中，传统网关难以进行中间处理。Higress 基于 WASM 可以在流式传输过程中进行实时审核或修改，且不中断连接。
*   **模型切换成本**：通过配置中心即可切换底层模型，实现了“模型无关”的应用层开发。

### 与同类工具对比
| 特性 | Higress | Kong | APISIX | Istio Ingress |
| :--- | :--- | :--- | :--- | :--- |
| **AI 原生支持** | **强 (内置 Token 管理, 多模型兼容)** | 弱 (需插件) | 弱 (需插件) | 无 |
| **WASM 支持** | **强 (默认集成, 多语言支持)** | 中 (需要企业版或复杂配置) | 中 (支持但生态较小) | 弱 (主要依赖 EnvoyFilter) |
| **易用性** | **高 (控制台 UI 友好, 开箱即用)** | 高 | 中 | 低 (学习曲线陡峭) |
| **性能** | **极高 (基于 Envoy)** | 高 | 高 | 极高 |

---

## 3. 技术实现细节

### 关键技术方案
1.  **配置热加载**：
    *   Higress 的控制平面监听 K8s CRD 或配置中心变化，将其翻译为 Envoy 的 xDS 配置。
    *   **难点**：xDS 协议非常复杂，版本控制困难。Higress 通过维护一套内部的高抽象配置模型，自动处理版本兼容性和增量更新。
2.  **WASM 虚拟机集成**：
    *   集成了 **Wasmtime** 或 **V8** 引擎。
    *   **实现原理**：Envoy 主进程通过 `in-tree` WASM 过滤器加载 `.wasm` 二进制文件。WASM 插件通过 ABI (Application Binary Interface) 与 Envoy 交互，访问请求头、Body 和路由信息。
    *   **优化**：为了减少 WASM 的冷启动开销，Higress 实现了插件的缓存和预编译机制。

### 代码组织与设计模式
*   **代码结构**：典型的 Go 云原生项目结构。`pkg/` 目录下包含核心逻辑（如 `config` 用于配置分发，`router` 用于路由构建）。
*   **设计模式**：
    *   **Controller 模式**：使用 K8s Controller-Runtime 模式监听资源变化，并协调状态。
    *   **责任链模式**：在请求处理阶段，WASM 插件形成过滤器链，每个插件处理完逻辑后决定是否放行。

### 性能与扩展性
*   **性能**：数据路径不走 Go 代码，完全在 Envoy (C++) 中完成，避免了 Go GC 带来的延迟抖动。
*   **扩展性**：通过 WASM，用户可以像写脚本一样扩展网关功能，而不需要修改网关内核代码，也不需要重新编译。

---

## 4. 适用场景分析

### 适合使用的项目
1.  **AI 应用开发与中台**：
    *   如果你的应用直接调用 OpenAI 或其他 LLM API，Higress 是绝佳的中间层。它可以在不修改应用代码的情况下，通过配置切换模型供应商，实现成本优化（如切换到更便宜的模型）。
2.  **Kubernetes 多集群/微服务管理**：
    *   作为 K8s Ingress Controller 的替代品，特别是当你需要比 Nginx Ingress 更强大的动态路由和流量管理能力，但又不想引入 Istio 那么重的复杂性时。
3.  **需要高频变更业务逻辑的场景**：
    *   例如复杂的鉴权逻辑、Header 修改、请求/响应体转换。使用 WASM 插件可以秒级生效，无需重启网关。

### 最有效的情况
*   **企业级 AI 落地**：当企业需要统一管理所有部门对 AI 模型的访问，进行统一计费、审计和 Prompt 注入时。
*   **高并发流式 AI 交互**：需要处理大量 SSE 长连接，且不能因为网关配置变更而断线。

### 不适合的场景
*   **极简静态站点托管**：Nginx 或 Caddy 更轻量，配置更简单。
*   **非 K8s 环境的物理机部署**：虽然支持，但 Higress 的设计哲学深度绑定 K8s 和云原生生态，在物理机上部署会丧失其动态配置的优势。

---

## 5. 发展趋势展望

### 技术演进方向
1.  **从流量网关到 AI 编排网关**：未来的 API 网关将不仅仅是“路由器”，更是“AI 编排器”。Higress 可能会内置更多 Agent 编排能力，如自动重试、语义缓存（基于向量相似度的缓存）。
2.  **MCP 协议的深度整合**：随着 AI Agent 的爆发，MCP 协议可能成为连接 LLM 与工具的标准。Higress 有望成为企业内部 MCP 服务的标准托管平台。

### 社区与改进
*   **WASM 生态建设**：目前 WASM 插件的开发门槛相对较高（需要了解 WASM ABI），未来可能会出现更高级的 DSL（如 TypeScript 直接编译）或低代码插件市场。
*   **可观测性增强**：针对 AI 请求的 Trace（不仅仅是 HTTP Trace），记录 Token 消耗、模型版本、Prompt 指纹等，将是未来的重点。

---

## 6. 学习建议

### 适合的开发者
*   **后端/运维工程师**：希望深入理解云原生、Service Mesh、Envoy 原理的开发者。
*   **AI 应用工程师**：需要构建生产级 AI 应用的开发者，希望掌握如何通过网关层解决模型切换、安全和流控问题。

### 学习路径
1.  **基础层**：理解 Envoy 的基本概念（Listener, Cluster, Route）。阅读 *Envoy 官方文档*。
2.  **协议层**：了解 xDS 协议（v2/v3）的工作原理。
3.  **实践层**：
    *   在本地 Kind/Docker 集群部署 Higress。
    *   尝试编写一个简单的 WASM 插件（推荐使用 Go 的 `proxy-wasm-go-sdk`），实现一个简单的 Header 修改或鉴权功能。
4.  **进阶层**：研究 Higress 的 Router 代码，看它如何将 K8s Ingress 资源转换为 Envoy 配置。

### 实践建议
*   **动手写 WASM**：不要只看文档，尝试写一个插件来统计 API 的响应时间，并输出到日志中。这是理解 Higress 扩展能力的最快方式。

---

## 7. 最佳实践建议

### 正确使用方式
1.  **分离关注点**：
    *   **基础设施层**：K8s + Higress（负责 TLS、路由、流量治理）。
    *   **业务逻辑层**：WASM 插件（负责特定的 Auth、Header 转换）。
    *   **应用层**：后端服务（只负责业务逻辑，不关心鉴权和流量切换）。

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
    gateway = Gateway(name="api-gateway")
    
    # 添加路由规则：将 /api/v1 路径的请求转发到 service-a
    gateway.add_route(
        path="/api/v1/*",
        destination="service-a:8080",
        methods=["GET", "POST"]
    )
    
    # 添加路由规则：将 /api/v2 路径的请求转发到 service-b
    gateway.add_route(
        path="/api/v2/*",
        destination="service-b:8080",
        methods=["GET"]
    )
    
    # 应用配置
    gateway.apply()
    print("Higress 路由配置已成功应用")

# 说明：这个示例展示了如何使用 Higress 配置网关路由规则，实现不同路径请求的智能转发。
```




```python
# 示例2：Higress 流量控制与限流
def configure_rate_limit():
    """
    配置 Higress 的限流策略
    解决问题：保护后端服务免受流量洪峰影响
    """
    from higress import RateLimitPolicy
    
    # 创建限流策略
    policy = RateLimitPolicy(
        name="api-rate-limit",
        # 每秒最多 100 个请求
        requests_per_second=100,
        # 突发流量允许 20 个请求
        burst=20
    )
    
    # 将限流策略应用到特定路由
    policy.apply_to_route("/api/v1/*")
    
    print("限流策略已配置：每秒最多 100 个请求，突发流量允许 20 个请求")

# 说明：这个示例展示了如何使用 Higress 配置限流策略，保护后端服务免受流量洪峰影响。
```




```python
# 示例3：Higress 插件开发与部署
def deploy_custom_plugin():
    """
    开发并部署自定义 Higress 插件
    解决问题：实现自定义的请求处理逻辑
    """
    from higress import Plugin
    
    # 定义插件逻辑
    def custom_auth_plugin(request):
        # 检查请求头中的认证信息
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return {"status": 401, "body": "Unauthorized"}
        
        # 验证 token
        token = auth_header.split(" ")[1]
        if not validate_token(token):
            return {"status": 403, "body": "Forbidden"}
        
        # 认证通过，继续处理请求
        return {"status": 200, "body": "Authorized"}
    
    # 创建并部署插件
    plugin = Plugin(
        name="custom-auth",
        handler=custom_auth_plugin,
        # 插件应用于所有路由
        apply_to="*"
    )
    plugin.deploy()
    
    print("自定义认证插件已部署")

def validate_token(token):
    """简单的 token 验证函数"""
    return token == "valid-token"

# 说明：这个示例展示了如何开发并部署自定义 Higress 插件，实现自定义的请求处理逻辑。
```


---
## 案例研究


### 1：阿里集团内部电商业务大促保障

 1：阿里集团内部电商业务大促保障

**背景**:

在双11、618等大型电商促销活动中，阿里内部核心交易链路面临着极其严苛的流量冲击。传统的网关架构在应对每秒数十万甚至百万级 QPS（Queries Per Second）的突发流量时，往往面临资源弹性滞后、配置推送延迟以及长尾请求延迟高等问题。

**问题**:

1.  **弹性能力不足**: 传统基于 Java 的网关在扩容时启动慢，无法应对秒杀级别的瞬时流量激增。
2.  **配置热更新难**: 大促期间流量路由规则变更频繁，传统网关配置 reload 会导致长连接断开，影响用户体验。
3.  **异构系统互通**: 电商系统内部存在多种语言（Go, Java, Python）构建的微服务，传统网关在协议转换和服务治理上存在瓶颈。

**解决方案**:

阿里巴巴基于 Higress（基于 Envoy 和 Istio 构建）对内部流量网关进行了深度改造。

1.  **采用云原生架构**: 利用 Envoy 的高性能 C++ 网络栈和 Istio 的控制平面，实现了极高的吞吐量和极低的资源消耗。
2.  **动态配置管理**: 利用 Higress 的热更新能力，实现了路由规则、限流配置的毫秒级生效，且无需重启网关节点。
3.  **插件生态**: 针对电商场景定制了 WAF 防护、流量负载均衡和请求鉴权插件，并支持 WASM 技术进行动态扩展。

**效果**:

1.  **性能大幅提升**: 成功支撑了峰值流量，P99 延迟显著降低，单核 QPS 性能相比传统网关提升数倍。
2.  **资源成本优化**: 由于 C++ 的高效特性，在处理相同流量下，计算资源占用大幅下降，节省了大量服务器成本。
3.  **稳定性增强**: 实现了配置变更业务无感，保障了大促期间核心链路 99.99% 的可用性。

---



### 2：某头部互联网企业 AI 应用网关落地

 2：某头部互联网企业 AI 应用网关落地

**背景**:

随着大语言模型（LLM）和生成式 AI 的爆发，该企业内部有大量业务线急需接入 AI 能力。然而，直接暴露 AI 模型服务存在巨大的安全风险，且不同模型厂商（如 OpenAI, 通义千问, 文心一言）的接口协议不统一，Token 计费和流控管理极其复杂。

**问题**:

1.  **安全风险**: 直接暴露 API Key 容易导致密钥泄露和资损。
2.  **协议不统一**: 业务方需要针对不同模型厂商写适配代码，开发效率低。
3.  **成本与流控**: 无法针对不同部门或用户进行细粒度的 Token 限流和计费统计。

**解决方案**:

该企业引入 Higress 作为 AI API 网关，利用其原生支持的 AI 特性。

1.  **统一模型接入**: 利用 Higress 的 AI 插件，将不同厂商的异构接口统一为 OpenAI 标准协议，业务端只需修改配置即可切换模型。
2.  **安全与鉴权**: 在网关层统一托管敏感的 API Key，业务方只持有网关颁发的内部 Token，实现了权限的统一管理与隔离。
3.  **内容防护与流控**: 配置了基于 Token 的速率限制，防止恶意刷量导致预算超支；同时配置了敏感词过滤插件，确保输出内容合规。

**效果**:

1.  **开发效率提升**: 业务接入 AI 服务的时间从数天缩短至小时级，无需编写适配代码。
2.  **成本可控**: 通过精细化的 Token 流控，成功拦截了异常流量，将 AI 调用成本控制在预算范围内。
3.  **安全性增强**: 杜绝了 API Key 泄露到前端的风险，实现了企业级的数据安全合规。

---



### 3：某大型物流企业微服务流量治理

 3：某大型物流企业微服务流量治理

**背景**:

该企业拥有庞大的微服务集群，涵盖订单、运输、仓储等数百个服务。随着业务出海，需要在混合云环境（阿里云 + 自建机房）下统一管理东西向流量（服务间调用）和南北向流量（入口网关）。原有的 Spring Cloud Gateway 架构在云原生场景下维护成本高，且缺乏统一的流量观测能力。

**问题**:

1.  **流量治理割裂**: 入口网关与微服务间通信使用两套体系，缺乏统一的灰度发布和全链路透传能力。
2.  **可观测性差**: 调用链路追踪困难，排查跨服务的超时或错误问题极其耗时。
3.  **多语言支持**: 部分边缘计算节点使用 Go 和 C++ 编写，难以融入原有的 Java 微服务治理体系。

**解决方案**:

采用 Higress 作为统一网关，并配合 Istio 进行服务网格治理。

1.  **统一入口**: 使用 Higress 替代原有的 API Gateway，统一接管流量入口，并利用 Higress 对 Istio 的天然兼容，将流量无缝下沉到服务网格。
2.  **全链路灰度**: 基于 Higress 的标签路由能力，实现了从网关入口到后端微服务的全链路金丝雀发布，确保新版本平滑上线。
3.  **协议扩展**: 利用 Higress 对 Dubbo、gRPC 等协议的高性能支持，解决了老旧系统向 HTTP/JSON 迁移的过渡期难题。

**效果**:

1.  **运维简化**: 统一了流量治理技术栈，减少了维护多套网关的复杂度。
2.  **发布稳定性**: 实现了按比例、按请求内容的精准灰度，新版本上线故障率大幅降低。
3.  **可观测性提升**: 结合 OpenTelemetry，实现了流量的统一监控和日志分析，故障定位时间（MTTR）缩短 50% 以上。

---
## 对比分析

## 与同类方案对比

| 维度 | Alibaba Higress | APISIX | Kong |
|------|-----------------|--------|------|
| 性能 | 基于Envoy和Istio，高性能，支持高并发 | 基于OpenResty，性能优异，低延迟 | 基于OpenResty，性能稳定，但略低于APISIX |
| 易用性 | 提供图形化控制台，集成Kubernetes，操作简便 | 配置灵活，但需要一定的学习成本 | 提供管理界面，但高级功能需要配置 |
| 成本 | 开源免费，企业版收费 | 开源免费，企业版收费 | 开源免费，企业版收费 |
| 扩展性 | 支持自定义插件，扩展性强 | 支持Lua插件，扩展性中等 | 支持Lua和Go插件，扩展性较强 |
| 社区支持 | 阿里背书，社区活跃 | 社区活跃，文档丰富 | 社区成熟，资源较多 |

### 优势分析

- 优势1：与Kubernetes和Istio深度集成，适合云原生环境。
- 优势2：提供图形化控制台，降低使用门槛。
- 优势3：阿里技术支持，适合企业级应用。

### 不足分析

- 不足1：社区生态相对较新，不如APISIX和Kong成熟。
- 不足2：部分高级功能可能需要企业版支持。
- 不足3：文档和案例相对较少，学习资源有限。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Envoy 的深度定制与性能优化

**说明**:  
Higress 基于 Envoy 构建，充分利用 Envoy 的高性能网络处理能力，同时针对云原生场景进行了深度定制。通过优化 Envoy 配置和资源分配，可以显著提升网关的吞吐量和响应速度。

**实施步骤**:
1. 根据业务需求调整 Envoy 的线程数和连接池配置。
2. 启用 HTTP/3 或 QUIC 协议以减少延迟。
3. 配置合理的超时和重试策略，避免资源浪费。

**注意事项**:  
- 监控 Envoy 的 CPU 和内存使用情况，避免资源瓶颈。
- 测试配置变更对性能的影响，确保稳定性。

---

### 实践 2：动态路由与流量管理

**说明**:  
Higress 支持灵活的动态路由配置，可以根据请求头、路径、权重等条件将流量分发到不同的服务实例。通过合理的路由策略，可以实现蓝绿发布、金丝雀发布等高级流量管理功能。

**实施步骤**:
1. 定义路由规则，匹配条件（如路径、请求头）。
2. 配置权重路由，逐步切换流量。
3. 结合服务发现机制（如 Nacos）实现动态服务注册。

**注意事项**:  
- 确保路由规则的优先级清晰，避免冲突。
- 在生产环境发布前充分测试路由逻辑。

---

### 实践 3：安全插件与 WAF 集成

**说明**:  
Higress 提供了丰富的安全插件，包括认证、授权、限流和 WAF（Web 应用防火墙）。通过启用这些插件，可以有效防护常见攻击（如 SQL 注入、XSS）并保障服务安全。

**实施步骤**:
1. 启用 Key Auth 或 JWT 认证插件。
2. 配置 IP 黑白名单和访问频率限制。
3. 集成 WAF 插件，定义防护规则。

**注意事项**:  
- 定期更新安全规则库，应对新型威胁。
- 避免过度限流影响正常用户访问。

---

### 实践 4：可观测性与监控集成

**说明**:  
Higress 原生支持 Prometheus、Grafana 和 OpenTelemetry，可以实时监控网关的性能指标（如请求延迟、错误率）。通过日志和追踪工具，快速定位问题。

**实施步骤**:
1. 配置 Prometheus 抓取 Higress 的指标数据。
2. 集成 OpenTelemetry 进行分布式追踪。
3. 设置告警规则，及时响应异常。

**注意事项**:  
- 确保监控数据的存储和查询性能。
- 定期审查告警阈值，避免误报。

---

### 实践 5：高可用部署与容灾

**说明**:  
Higress 支持多副本部署和自动故障转移，通过合理的架构设计可以避免单点故障。结合 Kubernetes 的健康检查机制，确保服务的高可用性。

**实施步骤**:
1. 部署多副本 Higress 实例，配置反亲和性。
2. 启用 Kubernetes 的 Liveness 和 Readiness 探针。
3. 配置负载均衡器（如 SLB）分发流量。

**注意事项**:  
- 定期进行故障演练，验证容灾能力。
- 确保跨可用区的网络延迟在可接受范围内。

---

### 实践 6：插件生态与自定义扩展

**说明**:  
Higress 提供了丰富的插件生态，支持 Lua、Wasm 和 Go 语言扩展。通过开发自定义插件，可以满足特定业务需求（如请求转换、日志定制）。

**实施步骤**:
1. 评估现有插件是否满足需求。
2. 开发自定义插件（如 Wasm 插件）。
3. 测试插件性能，避免拖慢网关。

**注意事项**:  
- 插件开发需遵循 Higress 的规范。
- 避免插件逻辑过于复杂，影响网关性能。

---

### 实践 7：多集群管理与流量调度

**说明**:  
Higress 支持多集群管理，可以实现跨集群的流量调度和服务治理。通过统一配置管理，简化多集群运维复杂度。

**实施步骤**:
1. 配置多集群的 Higress 实例。
2. 定义跨集群的路由规则和流量策略。
3. 使用统一控制平面管理配置。

**注意事项**:  
- 确保跨集群的网络连通性。
- 定期同步配置，避免不一致。

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/2 与 HTTP/3 (QUIC) 协议

**说明**: Higress 作为高性能网关，底层的网络协议对吞吐量影响巨大。HTTP/2 支持多路复用，解决了 HTTP/1.1 的队头阻塞问题；而 HTTP/3 (QUIC) 基于 UDP，进一步解决了 TCP 层的队头阻塞，显著降低弱网环境下的延迟。

**实施方法**:
1. 在 Higress 的网关配置中，确保监听器协议版本包含 `h2` 和 `h3`。
2. 配置 TLS 证书，因为 HTTP/2 和 HTTP/3 通常需要配合 HTTPS 使用。
3. 在 `Ingress` 或 `Gateway` 资源中明确启用 HTTP/3 支持（需确保 Higress 版本支持）。

**预期效果**: 弱网环境下请求延迟降低 30%-50%，并发连接数减少，资源利用率提升。

---

### 优化 2：配置全链路超时与连接池

**说明**: 默认的超时设置可能过长，导致后端服务响应慢时网关连接堆积。合理的超时与连接池配置可以快速失败，防止雪崩，并复用后端连接，减少 TCP 握手开销。

**实施方法**:
1. **连接池**: 调整 `upstream` 的 `maxRequestsPerConnection` 和 `http2MaxRequests`，避免频繁建立连接。
2. **超时设置**: 在路由配置中设置合理的 `connectTimeout` (连接超时)、`timeout` (请求超时) 和 `streamIdleTimeout` (空闲超时)。
3. 使用 `retry` 策略时，务必配合 `timeout` 使用，防止无限重试。

**预期效果**: 后端服务异常时响应速度提升至超时阈值内（如由 60s 降至 5s），连接复用率提升，减少 CPU 和内存消耗约 10%-20%。

---

### 优化 3：启用 Wasm 插件与本地缓存

**说明**: Higress 原生支持 Wasm (WebAssembly)。相比于传统的 Lua 或远程调用，Wasm 插件执行效率更高，安全性更好。同时，对于高频读取的低频变更数据（如配置项、鉴权规则），应在网关层启用本地缓存，减少对后端的请求。

**实施方法**:
1. 将高频使用的鉴权、限流逻辑编译为 Wasm 插件并在 Higress 中加载。
2. 利用 Higress 的 `Dsl` 或 `Wasm` 能力实现本地缓存策略（如缓存 JWT 的公钥或后端响应）。
3. 避免在请求路径中进行阻塞式的远程 HTTP 调用（如调用外部 Auth 服务），改为异步或缓存。

**预期效果**: 插件执行延迟降低至微秒级，通过缓存减少后端请求量 40%-90%，显著提升 P99 延迟表现。

---

### 优化 4：开启 CPU 亲和性与自动扩缩容

**说明**: 网关属于 CPU 密集型任务（涉及大量 TLS 加解密和路由计算）。开启 CPU 亲和性可以减少 CPU 上下文切换缓存失效。同时，根据负载动态调整 Pod 副本数是维持高性能的关键。

**实施方法**:
1. **CPU 亲和性**: 在 Higress 的 Deployment 配置中，利用 Kubernetes 的 CPU Manager 策略，或配置 Envoy 的 `worker_cpu_affinity`。
2. **资源限制**: 确保 `requests` 和 `limits` 设置一致，以启用 Guaranteed QoS，避免 CPU 节流。
3. **HPA**: 配置 Kubernetes Horizontal Pod Autoscaler，基于 CPU 或 QPS 指标自动扩容。

**预期效果**: 上下文切换开销减少，单核吞吐量提升 10%-15%，系统整体稳定性提高。

---

### 优化 5：优化日志采样与异步上报

**说明**: 详细的 Access Log 写入磁盘或远程日志系统是 I/O 密集型操作，会成为性能瓶颈。在高并发场景下

---
## 学习要点

- 基于您提供的关键词 "alibaba / higress" 和来源 "github_trending"，以下是关于 **Higress** 项目的关键要点总结：
- Higress 是阿里云开源的、基于阿里内部多年实践沉淀的下一代云原生 API 网关。
- 该项目深度集成了 K8s Ingress 与 Gateway API 标准，旨在解决云原生时代流量管理的入口标准化问题。
- 它支持将传统的 Nginx Ingress 配置平滑迁移，并兼容 Kong/Dubbo 等生态，降低了用户迁移和集成的门槛。
- Higress 独创性地将 WAF（Web应用防火墙）插件化，提供了开箱即用的安全防护能力，实现了安全与流量的统一治理。
- 内置了对高并发流量的优化处理，继承了阿里双十一场景的稳定性基因，适合作为企业级统一流量入口。
- 提供了强大的扩展插件市场（支持 WASM/Go/Python），允许开发者像搭积木一样灵活扩展网关功能。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础

**学习内容**:
- 云原生网关的基本概念与 Higress 的核心架构
- Higress 与传统网关（如 Nginx, Kong）的区别与优势
- Docker 环境下 Higress 的快速安装与部署
- 基本术语：Ingress、Route、Service、Plugin
- 控制台的基本操作与界面导航

**学习时间**: 1-2周

**学习资源**:
- Higress 官方文档 (https://higress.io/docs/latest/overview/what-is-higress/)
- Higress GitHub 仓库 README (https://github.com/alibaba/higress)
- 云原生网关技术对比文章

**学习建议**: 
建议先从宏观上理解 Higress 作为“云原生 API 网关”的定位。务必动手进行一次本地安装（Docker Desktop 或 Kubernetes 集群），并成功通过控制台配置第一个简单的路由转发，将流量导入一个测试服务。

---

### 阶段 2：核心功能与流量管理

**学习内容**:
- 详细的域名与路由配置（基于 Header、Path、Query 参数的路由规则）
- 服务来源的配置（Nacos, Consul, 固定地址, DNS）
- 负载均衡策略与超时/重试机制配置
- 全局与细粒度的流量控制（限流、熔断、认证）
- WAF（Web 应用防火墙）基础插件的启用与配置
- 金丝雀发布与蓝绿发布实战

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 流量管理章节
- Higress 官方插件市场文档
- Envoy Filter 基础知识（因为 Higress 基于 Envoy）

**学习建议**: 
此阶段重点在于“流量搬运”。尝试搭建一个包含两个版本服务的场景，配置 Header 匹配的路由规则来实现灰度发布。深入理解如何通过配置保护后端服务（例如开启限流防止突发流量击穿后端）。

---

### 阶段 3：插件开发与可观测性

**学习内容**:
- Higress 插件体系架构（Wasm 插件与 Lua 插件）
- 使用 Go 或 Python 开发自定义 Wasm 插件
- 插件的配置参数定义与热加载机制
- 日志与监控体系：对接 Prometheus/Grafana、SkyWalking
- 访问日志的定制与推送（如 Kafka, SLS）
- Higress 的告警配置

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档 - 自定义插件开发指南
- Higress GitHub 仓库中的插件示例代码
- Wasm (WebAssembly) 在网关中的应用案例

**学习建议**: 
不要局限于使用内置插件。尝试编写一个简单的 Go Wasm 插件（例如修改请求 Header 或响应 Body），并在本地构建、部署。同时，关注可观测性，学会如何从监控面板中排查网关本身的性能瓶颈（如延迟、QPS）。

---

### 阶段 4：生产级运维与高级架构

**学习内容**:
- 在 Kubernetes 生产环境中的高可用部署架构
- Higress 的配置管理（GitOps 实践，Kubernetes CRD 应用）
- 多集群容灾与多租户隔离
- 网关的安全性加固（TLS 证书管理、mTLS、OAuth2/OIDC 集成）
- 性能调优（连接池、缓冲区大小、并发数配置）
- 与服务网格（如 Istio）的协同使用

**学习时间**: 4周及以上

**学习资源**:
- Higress 官方博客中的最佳实践案例
- Kubernetes Ingress Controller 运维经验
- Nginx/Envoy 性能调优相关文档

**学习建议**: 
此阶段面向架构师与高级运维人员。重点思考如何保证网关自身的高可用，避免单点故障。建议研究 Higress 在处理高并发（如大促场景）时的配置参数调整，并实践如何将 Higress 无缝集成到现有的 CI/CD 流程中。

---
## 常见问题


### 1: Higress 是什么？它与阿里云和 Nginx 有什么关系？

1: Higress 是什么？它与阿里云和 Nginx 有什么关系？

**A**: Higress 是一款云原生 API 网关。它是基于阿里云内部多年实践沉淀的 Gateway 架构进行开源的产物。

从技术演进上看，Higress 的内核是基于开源网关 **Apache APISIX** 优化的，同时深度集成了 **Nginx** 的高性能网络处理能力。它的主要目标是解决云原生时代流量治理的问题，兼容 Kubernetes Ingress 标准，并支持从传统的 Nginx 配置平滑迁移。简单来说，它结合了 Nginx 的高性能、APISIX 的动态能力以及阿里云的企业级治理经验。

---



### 2: Higress 与 Kong 或 APISIX 等其他开源网关相比有什么优势？

2: Higress 与 Kong 或 APISIX 等其他开源网关相比有什么优势？

**A**: Higress 的核心优势主要体现在以下几个方面：

1.  **深度集成 WASM**: Higress 原生支持 WebAssembly (WASM)，允许开发者使用 C++、Go、Rust 或 Python 等多种语言编写插件，而无需重新编译网关或修改核心代码。这比传统的 Lua 插件开发更灵活、更安全（沙箱隔离）且易于维护。
2.  **服务发现集成**: 它对阿里云服务（如 MSE, Nacos, ACK）以及云原生生态（如 Consul, Eureka）有开箱即用的支持，非常适合微服务架构。
3.  **防护能力**: 继承了阿里云的 WAF 防护能力，提供企业级的安全防护。
4.  **标准化**: 严格遵循 Kubernetes Gateway API 和 Ingress 标准，便于在云原生环境中进行标准化管理。

---



### 3: 我能否将现有的 Nginx 配置直接迁移到 Higress 中？

3: 我能否将现有的 Nginx 配置直接迁移到 Higress 中？

**A**: 可以，Higress 提供了 **Nginx 配置转换工具**。

由于 Higress 底层使用了与 Nginx 兼容的 OpenResty 内核，因此它支持 Nginx 的绝大多数指令。你可以通过 Higress 控制台或提供的工具将现有的 Nginx `nginx.conf` 直接导入，Higress 会自动将其转换为网关的路由规则和插件配置。这使得从传统 Nginx 迁移到云原生网关的成本大大降低。

---



### 4: Higress 的插件系统是如何工作的？支持哪些语言？

4: Higress 的插件系统是如何工作的？支持哪些语言？

**A**: Higress 采用了基于 **Proxy-WASM** 的插件架构。

*   **工作原理**: 插件运行在 WASM 虚拟机中，通过标准的 ABI 接口与 Higress 核心交互。这意味着插件的崩溃不会导致网关进程崩溃，且插件支持热加载，无需重启网关即可更新插件逻辑。
*   **支持语言**: 官方优先推荐使用 **Go** 语言进行插件开发（提供了完善的 Go SDK），同时也支持 C++、Rust、AssemblyScript 等编译为 WASM 的语言。这比强制要求使用 Lua 的传统网关（如 OpenResty/Kong）对开发者更友好。

---



### 5: Higress 是否支持作为 Kubernetes Ingress Controller 使用？

5: Higress 是否支持作为 Kubernetes Ingress Controller 使用？

**A**: 是的，Higress 完全支持作为 Kubernetes 的 Ingress Controller 使用。

它不仅支持标准的 Kubernetes Ingress 资源，还支持更强大的 **Gateway API**（Kubernetes 社区推荐的下一代流量管理标准）。在 Kubernetes 集群中部署 Higress 后，它会自动监听 Service 和 Ingress/Gateway 资源的变化，并动态更新路由规则，实现流量的自动化管理。

---



### 6: Higress 的性能表现如何？是否适合高并发场景？

6: Higress 的性能表现如何？是否适合高并发场景？

**A**: Higress 具备极高的性能，完全适合企业级的高并发场景。

由于底层基于 Nginx/OpenResty，它继承了 Nginx 的高性能事件驱动模型。在官方提供的基准测试中，Higress 在开启较多插件（如限流、认证）的情况下，依然能保持极高的 QPS（每秒查询率）和低延迟。特别是在处理 HTTP/2 和 gRPC 流量时，经过阿里云内部优化的内核表现通常优于标准的开源实现。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: 基础环境搭建与流量转发

### 难度**: [简单]

### 问题描述**:

### 使用 Higress 快速部署一个网关实例，并配置一个简单的路由规则。要求实现将访问 `http://<higress-host>/sample/` 的流量转发到后端的一个模拟服务（如 httpbin.org 或 mock 服务），并观察请求路径的变化。

---
## 实践建议

以下是基于 Higress 作为 AI 网关和 API 网关的 5-7 条实践建议：

### 1. 利用 AI 代理插件实现模型供应商的统一管理
Higress 最核心的功能之一是能够将后端不同的 LLM 提供商（如 OpenAI, Azure, 通义千问, HuggingFace 等）统一为标准的 OpenAI API 格式。
*   **最佳实践**：在配置路由时，使用 `ai-proxy` 插件将 `/v1/chat/completions` 等标准路径指向不同的后端服务。这样，你的业务代码只需要对接一套 OpenAI SDK，通过切换 Higress 的路由或 Header 即可无缝切换底层模型，无需修改客户端代码。
*   **常见陷阱**：不要在业务代码中硬编码不同厂商的 API 地址。如果直接绕过网关调用厂商接口，后续做模型切换或鉴权统一管理的成本会非常高。

### 2. 配置语义缓存以降低 Token 成本和延迟
大模型推理成本高且耗时，对于常见的问答（如“如何使用 Java 连接数据库”），答案往往是固定的。
*   **最佳实践**：开启 Higress 的语义缓存功能。它基于向量数据库原理，能够识别语义相似而非仅仅文本完全一致的请求。对于高相似度的用户提问，Higress 可以直接返回缓存结果，从而直接绕过大模型服务。
*   **常见陷阱**：注意设置合理的缓存 Key 和过期时间（TTL）。对于时效性要求高的场景（如查询最新新闻），需根据业务需求调整缓存策略，避免返回过时信息。

### 3. 实施基于 Token 的精细化流控与降级
AI 流量的成本主要在于 Token 消耗，传统的基于 QPS（每秒请求数）或并发连接数的限流无法准确控制成本。
*   **最佳实践**：使用 Higress 的 `token-ratelimit` 插件。针对不同的 API Key 或用户 ID，设置每分钟或每天的最大 Token 消耗限额。当达到阈值时，可以配置自动降级策略（例如返回简短的预设回复，或者切换到更便宜的小模型）。
*   **常见陷阱**：仅配置 HTTP 请求限流。一个恶意用户可能只发送几个请求，但每个请求包含几百万个 Token，依然会导致巨额账单。

### 4. 善用 Prompt 模板管理与注入
为了确保模型输出的稳定性和安全性，通常需要在用户输入前后加入系统提示词。
*   **最佳实践**：在网关层配置 Prompt 模板。通过 Higress 的 `prompt-manager` 或相关插件，在请求转发给 LLM 之前，自动注入业务设定的 System Prompt（如“你是一个客服助手，请使用 Markdown 格式回复”）。这样可以集中管理 Prompt 逻辑，避免在每个微服务中重复维护。
*   **常见陷阱**：不要在网关层处理过于复杂的动态 Prompt 逻辑（如依赖大量数据库查询的上下文拼接），这会增加网关的延迟。复杂的上下文构建仍建议在业务服务层完成，网关主要负责静态模板注入和格式化。

### 5. 建立敏感词过滤与安全护栏
直接将用户输入传递给大模型存在“提示词注入”和输出有害内容的风险。
*   **最佳实践**：在 Higress 的请求阶段和响应阶段分别配置内容安全插件。例如，拦截包含“忽略之前的指令”等恶意攻击的 Prompt，或者在模型输出包含敏感信息时进行掩码处理。
*   **常见陷阱**：过度依赖简单的字符串匹配。攻击者会使用同音字、特殊字符或 Base64 编码绕过关键词检测。建议结合专业的 AI 安全服务或更高级的语义理解模型进行辅助检测。

### 6. 监控可观测性指标（重点关注 Time-to-Token）
在 AI 应用中，用户体验的瓶颈往往在于首字生成速度（TTFT - Time to First Token）。
*   **最佳实践**：确保 Higress 的可观测性配置（如对接 Prometheus/Grafana）不仅采集 HTTP 状态码和延迟，还要关注上游 LLM 服务的流式输出性能。通过监控 TTFT �

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
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/) / [Kubernetes](/scenarios/kubernetes/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260130-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260205-github_trending-alibaba-higress-6.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260201-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260214-github_trending-alibaba-higress-5.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260217-github_trending-alibaba-higress-6.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*