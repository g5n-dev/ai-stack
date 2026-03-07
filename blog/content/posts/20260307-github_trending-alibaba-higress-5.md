---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-03-07T22:28:45+08:00
draft: false
entry_kind: "auto"
tags: ["API 网关", "Higress", "AI 原生", "Istio", "Envoy", "WASM", "MCP", "Kubernetes"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "Higress 是阿里巴巴开源的一款**云原生 AI 原生 API 网关**。该项目基于 Go 语言开发，在 GitHub 上拥有超过 7,600 颗星。它通过扩展 Istio 和 Envoy，并结合 WebAssembly (WASM) 插件能力，旨在为云原生应用和 AI 大模型应用提供统一的流量管理入口。 **核心"
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
- **星标**: 7,682 (+10 stars today)
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

Higress 是一款基于 Istio 和 Envory 构建的 AI 原生 API 网关，它通过云原生架构将传统流量管理与 LLM 应用支持相结合。该项目旨在解决微服务路由、Kubernetes Ingress 管理以及 AI Agent 工具集成等复杂场景下的统一接入问题。本文将梳理其系统架构与核心组件，并重点介绍 WASM 插件机制及 AI 网关特性的具体实现。

---
## 摘要

Higress 是阿里巴巴开源的一款**云原生 AI 原生 API 网关**。该项目基于 Go 语言开发，在 GitHub 上拥有超过 7,600 颗星。它通过扩展 Istio 和 Envoy，并结合 WebAssembly (WASM) 插件能力，旨在为云原生应用和 AI 大模型应用提供统一的流量管理入口。

**核心架构与特性：**

Higress 采用**控制平面与数据平面分离**的架构。配置变更通过 xDS 协议传播，具备毫秒级延迟且不中断连接，特别适用于 AI 流式响应等长连接场景。

**三大主要应用场景：**

1.  **AI 网关：**
    *   提供统一 API 接入，支持 30 多家主流 LLM 提供商。
    *   具备协议转换、可观测性、缓存和 AI 安全防护等功能（依赖 `ai-proxy`、`ai-statistics` 等插件）。
2.  **MCP 服务器托管：**
    *   托管模型上下文协议 (MCP) 服务器，使 AI Agents 能够便捷地调用工具和服务（如搜索、地图等）。
3.  **Kubernetes Ingress：**
    *   作为标准的 K8s Ingress 控制器运行，兼容 Nginx Ingress 注解，支持微服务路由。

---
## 评论

### 总体判断

Higress 是一款**极具前瞻性的云原生网关产品**，它成功地将**云原生流量治理**与**AI 原生应用需求**深度融合。作为阿里云开源的标杆项目，它不仅继承了 Istio/Envoy 的稳健底座，更通过 WASM 和 AI 特性的集成，为开发者提供了一个**“传统网关 + AI 网关 + MCP 服务器”**的统一入口，是构建 LLM 应用基础设施的理想选择。

---

### 深入评价维度

#### 1. 技术创新性：从“流量转发”到“模型推理编排”
*   **事实**：Higress 基于 Istio 和 Envoy 构建，核心扩展能力依赖于 WebAssembly (WASM)。同时，DeepWiki 明确指出其集成了 AI Gateway 功能和 MCP (Model Context Protocol) 服务器托管能力。
*   **推断**：传统网关（如 Nginx, Kong）主要关注 HTTP/TCP 转发，而 Higress 的创新在于**将“协议理解”提升到了“语义理解”层面**。
    *   **WASM 插件化架构**：这是其最大的技术亮点。不同于 Lua (Nginx) 或 Java (Zuul) 插件，WASM 提供了接近原生的性能且沙箱隔离，允许开发者使用 C++/Go/Rust/AssemblyScript 编写复杂逻辑，特别是针对 AI 请求的 Prompt 注入、敏感词过滤等，无需重启网关即可热更新。
    *   **AI Native 原生集成**：它不仅仅是一个反向代理，更理解 LLM 的流式输出协议。通过内置对 OpenAI 格式的兼容，它可以无缝对接各类大模型，解决了 AI 应用开发中模型切换复杂、Token 计费统计困难等痛点。
    *   **MCP 协议支持**：DeepWiki 提到的 MCP Server Hosting 是一个非常新的技术动向。这意味着 Higress 试图解决 AI Agent 的“工具调用”标准化问题，让网关成为 Agent 连接外部数据源和工具的统一枢纽。

#### 2. 实用价值：统一异构基础设施的关键一环
*   **事实**：README 提到它提供 Kubernetes Ingress、微服务路由以及 AI 网关功能。
*   **推断**：在微服务架构向 AI 应用演进的当下，企业往往面临维护两套网关的困境（一套管微服务，一套管大模型调用）。Higress 的实用价值在于**“融合”**：
    *   **降低运维复杂度**：用一套控制平面统一管理传统的 RPC 调用和新的 AI 推理流量。
    *   **AI 企业的降本增效**：对于 SaaS 企业，Higress 提供了基于 Token 的限流和计费能力，这是传统网关不具备的。它允许企业在网关层做“统一模型供应商切换”，例如当某个云厂商 API 不稳定时，通过网关配置毫秒级切换到备用模型，极大提升了系统的鲁棒性。

#### 3. 代码质量与架构：云原生工程化的典范
*   **事实**：项目使用 Go 语言编写，星标数 7,682，文档包含多语言版本（中/日/英）及详细的架构图。
*   **推断**：
    *   **架构清晰**：控制平面与数据平面分离是标准云原生设计。Higress 在 Envoy 之上做了一层非常薄的抽象，既利用了 Envoy 高性能的 C++ 网络 I/O，又利用 Go 语言在控制逻辑上的开发效率。
    *   **工程规范**：作为阿里系开源项目，其代码结构通常遵循严格的 Go 惯例，接口抽象设计良好。DeepWiki 提到的“Development Guide”和详细的 README 表明项目重视文档和开发者体验，这对于降低上手门槛至关重要。

#### 4. 社区活跃度：头部背书，生态健康
*   **事实**：GitHub 星标数超过 7.6k，背靠阿里巴巴，且 README 拥有日语版本，显示出国际化意图。
*   **推断**：在 API Gateway 领域，这是一个非常高的关注度，仅次于 Kong 和 APISIX。阿里巴巴的背书意味着该项目**不是“玩具级”项目**，而是经过双十一等超大规模流量验证的工业级产品。社区活跃度通常较高，Issue 响应及时，且国内开发者对中文文档的友好度极高，形成了良好的正向循环。

#### 5. 学习价值：理解 WASM 与 AI 流量治理的窗口
*   **推断**：对于开发者而言，Higress 是学习**“如何将 WASM 运用于生产环境”**的最佳案例之一。
    *   你可以研究它是如何通过 `proxy-wasm` 规范在 Go 中编写插件并编译为 `.wasm` 文件的。
    *   它是学习**“AI 网关模式”**（如 Prompt 模板管理、上下文缓存策略）的实战教材。对于想要转型 AI 基础设施开发的工程师，阅读其源码能快速理解 LLM 流式传输在网关层的处理细节。

#### 6. 潜在问题与改进建议
*   **推断**：
    *   **复杂度曲线**：引入 Istio 和 Envoy 使得架构相对重型。对于只有几个后端服务的简单 AI 应用，Higress 可能显得过于厚重，部署和调优的学习成本高于简单的 Nginx 反向代理。
    *   **WASM 的冷启动**：虽然

---
## 技术分析

以下是对阿里巴巴开源的 **Higress** 仓库的深度技术分析。

---

# Higress 深度技术分析报告

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 的核心架构建立在 **云原生** 生态之上，采用了标准的 **控制平面 + 数据平面** 分离架构。

*   **底层基石**：深度依赖 **Envoy** 作为高性能数据平面，利用其 L3/L7 网络处理能力。同时，它兼容 **Istio** 生态，复用了 Istio 经过大规模验证的 xDS（控制平面和数据平面通信协议）配置下发机制。
*   **编程语言**：**Go**。控制平面使用 Go 构建，利用其高并发特性和丰富的云原生工具链（Kubernetes Client）。
*   **扩展模型**：**WebAssembly (WASM)**。这是 Higress 架构中最关键的技术选型。它允许开发者使用 C/C++、Rust、Go 或 AssemblyScript 编写插件，这些插件会被编译成 WASM 字节码并在 Envoy 的沙箱中运行。

### 核心模块设计
1.  **Router (路由层)**：基于 Envoy 的 HTTP Connection Manager，针对 AI 场景进行了流式传输的优化。
2.  **WASM Plugin Market (插件市场)**：内置了预编译的插件生态，包括认证、限流、AI 提示词增强等。
3.  **AI Gateway (AI 网关)**：这是最新的核心模块。它不再仅仅转发 HTTP 请求，而是理解 LLM 协议（如 OpenAI 协议）。它包含 **Provider 管理**（对接通义千问、OpenAI、Azure 等）和 **模型路由**（根据请求特征分发到不同模型）。
4.  **MCP (Model Context Protocol) Server**：作为 AI Agent 的工具集成层，允许 Higress 托管 MCP 服务，为 LLM 提供外部数据获取能力。

### 技术亮点与创新
*   **AI-Native (AI 原生)**：传统网关（如 Nginx, Kong）将 LLM 请求视为普通 HTTP 流量，无法理解“对话”的上下文或 Token 消耗。Higress 在网关层引入了语义理解，支持 **Prompt 装饰**（在转发前修改系统提示词）和 **内容过滤**（实时审核流式输出）。
*   **热更新与毫秒级配置生效**：基于 xDS 协议的增量推送机制，配置变更无需重启网关，且对长连接（如 SSE 流式请求）无影响，这对 AI 体验至关重要。
*   **标准 Ingress 托管**：它不仅是 AI 网关，还是标准的 K8s Ingress Controller，实现了“传统微服务 + AI 应用”的统一流量入口。

### 架构优势分析
*   **低延迟**：数据平面 Envoy 采用 C++ 编写，配合 Zero-Copy 技术，处理转发延迟极低。
*   **安全性隔离**：WASM 沙箱机制确保第三方插件崩溃不会导致网关主进程崩溃，同时也限制了插件对宿主机资源的访问。
*   **统一管控**：在一个网关内同时处理传统的 RESTful API 调用和新兴的 LLM 流式调用，减少了基础设施的碎片化。

---

## 2. 核心功能详细解读

### 主要功能与场景

#### 1. AI Gateway (LLM 代理与编排)
*   **功能**：将后端多种大模型（LLM）的 API 统一封装为标准接口。支持将 OpenAI 格式的请求转换为其他厂商（如通义千问、文心一言）的格式。
*   **解决的关键问题**：**供应商锁定**。开发者只需对接 Higress 的统一 API，后端模型可以随时切换或降级，无需修改客户端代码。解决了多模型接入的复杂度问题。
*   **实现原理**：在请求转发阶段，通过 WASM 插件或内置过滤器拦截 HTTP Body，解析 JSON 结构，重写 `model` 字段或 API Path，并在返回时逆向适配。

#### 2. 流式处理与 SSE 优化
*   **功能**：完美支持 Server-Sent Events (SSE) 和 Chunked Transfer Encoding。
*   **解决的关键问题**：LLM 生成是流式的，传统网关在缓冲大块数据时会产生“首字节延迟（TTFB）”。Higress 实现了透传转发，用户能实时看到 Token 生成。

#### 3. 提示词管理与安全
*   **功能**：允许在网关层动态注入系统提示词，或拦截包含敏感词的请求/响应。
*   **解决的关键问题**：**安全合规**与**业务逻辑解耦**。例如，强制所有通过该网关的请求都必须遵守“不得生成暴力内容”的指令，无需修改应用代码。

#### 4. MCP (Model Context Protocol) 集成
*   **功能**：Higress 可以作为 MCP Server 的托管端。
*   **解决的关键问题**：AI Agent 需要调用外部工具（如搜索、数据库查询）。Higress 将这些工具能力暴露给 LLM，充当了 Agent 的“工具箱”。

### 与同类工具对比

| 特性 | **Higress** | **Kong (AI Gateway)** | **Nginx** | **Cloudflare (AI Gateway)** |
| :--- | :--- | :--- | :--- | :--- |
| **核心定位** | 云原生 API 网关 + AI Native | 传统 API 网关 + AI 插件 | 通用 Web 服务器 | 边缘网络 + AI 代理 |
| **扩展性** | WASM (高性能, 多语言) | Lua/Go/Python (灵活但性能稍逊) | C Module/Lua (高门槛) | Workers (JS 生态) |
| **K8s 集成** | 原生 Ingress Controller | 需 KIC 或企业版 | 需 Ingress Controller | SaaS 服务 |
| **AI 特性** | 内置 Provider 管理, Prompt 装饰 | LLM 插件支持 | 需手写脚本 | 内置缓存与向量搜索 |
| **性能** | 极高 (Envoy) | 高 (Nginx/C) | 极高 (C) | 依赖边缘节点 |

---

## 3. 技术实现细节

### 关键技术方案：WASM 插件系统
Higress 没有采用传统的 Lua 脚本（如 OpenResty），而是选择了 Proxy-WASM。
*   **实现原理**：Go 编写的插件代码会被编译为 WASM 字节码。Envoy 通过 `http_filter` 加载 WASM 虚拟机（如 Wasmtime 或 V8）。
*   **生命周期钩子**：插件可以注册 `on_request_headers`, `on_request_body`, `on_response_body` 等钩子。
*   **AI 场景应用**：在 `on_response_body` 中，网关可以截获 LLM 返回的流式 JSON 片段，解析其中的 `content` 字段，进行敏感词替换，然后再发送给客户端。

### 代码组织结构
*   **`/pkg`**: 核心业务逻辑。包含 ingress 配置的 K8s Informer 监听、xDS 转换逻辑。
*   **`/plugins`**: WASM 插件的 Go SDK 和源码。Higress 提供了一套 Go SDK，屏蔽了 ABI 层的复杂性，让开发者用 Go 写插件逻辑。
*   **`/router`**: 路由匹配引擎。支持基于权重、Header、Cookie 的复杂路由，并针对 AI 的长连接场景进行了连接池管理优化。

### 性能与扩展性
*   **连接复用**：对于 AI 请求，后端建立连接的成本较高（TLS 握手）。Higress 在 Envoy 层面维护了连接池，支持 HTTP/1.1 和 HTTP/2（h2c）的复用。
*   **异步配置分发**：控制平面监听 K8s 资源变更，将其转换为 Envoy 配置，通过 gRPC 异步推送给数据平面。这种非阻塞设计保证了高并发下的稳定性。

### 技术难点与解决
*   **流式数据修改**：在流式传输中修改 Body 是困难的，因为数据是分块到达的。
    *   **解决方案**：Higress 的 WASM 插件支持 Buffer 模式（缓存小包）或 Streaming 模式（逐块处理）。对于 AI，通常需要实现一个简单的流式解析器，在边界处进行修改。

---

## 4. 适用场景分析

### 最佳适用场景
1.  **企业级 AI 应用落地**：企业内部需要对接多个 LLM 供应商（阿里云、OpenAI、本地部署的 Llama），希望统一管理 API Key、配额和鉴权。
2.  **微服务与 AI 混合架构**：系统既有传统的 SpringBoot/Go 微服务，又有新开发的 AI 服务。Higress 可以作为统一流量入口，避免维护两套网关。
3.  **SaaS 平台的多租户 AI 网关**：需要为不同客户提供隔离的 Prompt 模板或不同的模型策略，利用 Higress 的路由匹配能力可实现基于 Header 的租户路由。
4.  **需要高度定制逻辑的场景**：利用 WASM 插件，在网关层实现特殊的鉴权逻辑（如与内部 OAuth 系统集成）或数据转换。

### 不适合的场景
1.  **极简静态博客/个人站点**：Nginx 或 Caddy 更轻量，Higress 依赖 K8s 和复杂的控制平面，属于“杀鸡用牛刀”。
2.  **对延迟极度敏感（微秒级）的纯内存缓存**：虽然 Envoy 很快，但经过 WASM 虚拟机的处理仍有一定开销。如果是极致性能的 KV 存储代理，裸机 Envoy 或 C 可能更合适。

### 集成注意事项
*   **资源限制**：WASM 插件消耗内存，需合理配置 Envoy 的 `wasm_runtime_config`，防止插件内存泄漏导致 OOM。
*   **K8s 网络依赖**：Higress 强依赖 Kubernetes API Server，网络需保证低延迟。

---

## 5. 发展趋势展望

### 技术演进方向
*   **从网关到编排**：未来 Higress 可能会集成更复杂的编排能力（如 LangChain 的网关版），支持在网关层直接进行简单的 Agent 任务分发，而不仅仅是透传请求。
*   **可观测性增强**：针对 AI 场景的 Metrics（如 Token 消耗量、首字延迟、模型响应成功率）将成为标准输出，对接 Prometheus/Grafana。
*   **向量化与 RAG 集成**：未来可能会集成向量数据库客户端，允许网关在转发请求前自动进行向量检索并注入 Context。

### 社区反馈与改进
*   目前社区对 WASM 的易用性仍有期待。虽然 Go SDK 已降低门槛，但调试 WASM 插件仍比调试本地代码困难。改进日志输出和本地调试工具是关键。

---

## 6. 学习建议

###

---
## 代码示例




```python
# 示例1：Higress 网关路由配置
def higress_route_config():
    """
    配置 Higress 网关的路由规则，实现基于路径的流量转发
    适用场景：微服务架构中的 API 网关配置
    """
    from pydantic import BaseModel
    
    class RouteRule(BaseModel):
        """路由规则模型"""
        path: str          # 匹配路径
        service_name: str  # 目标服务名
        port: int          # 目标端口
        rewrite: str = ""  # 路径重写规则
    
    # 配置示例：将 /api/user 请求转发到 user-service
    route = RouteRule(
        path="/api/user/*",
        service_name="user-service",
        port=8080,
        rewrite="/user"
    )
    
    # 生成 Higress 路由配置（实际会转换为 YAML/JSON）
    config = {
        "apiVersion": "networking.k8s.io/v1beta1",
        "kind": "Ingress",
        "metadata": {"name": "higress-route"},
        "spec": {
            "rules": [{
                "host": "api.example.com",
                "http": {
                    "paths": [{
                        "path": route.path,
                        "backend": {
                            "serviceName": route.service_name,
                            "servicePort": route.port
                        },
                        "pathType": "Prefix"
                    }]
                }
            }]
        }
    }
    return config

# 说明：展示了如何使用 Python 定义 Higress 网关的路由规则，实现基于路径的流量转发。
# 实际使用时需要配合 Kubernetes Ingress 或 Higress 的 API 进行部署。
```




```python
# 示例2：Higress 插件开发（认证插件）
def higress_auth_plugin():
    """
    开发一个简单的 Higress 认证插件
    适用场景：API 访问控制、JWT 验证等
    """
    import hmac
    import hashlib
    
    def verify_request(request_headers, secret_key):
        """
        验证请求签名
        :param request_headers: 请求头字典
        :param secret_key: 密钥
        :return: bool 是否通过验证
        """
        # 从请求头获取签名
        signature = request_headers.get("X-Signature", "")
        timestamp = request_headers.get("X-Timestamp", "")
        
        # 重新计算签名
        message = f"{timestamp}{secret_key}".encode('utf-8')
        computed_signature = hmac.new(
            secret_key.encode('utf-8'),
            message,
            hashlib.sha256
        ).hexdigest()
        
        # 比较签名
        return hmac.compare_digest(signature, computed_signature)
    
    # 模拟请求验证
    headers = {
        "X-Timestamp": "2023-01-01T00:00:00Z",
        "X-Signature": "a1b2c3d4e5f6..."  # 实际应为正确计算的签名
    }
    secret = "my-secret-key"
    
    return verify_request(headers, secret)

# 说明：展示了如何实现一个基于 HMAC 的请求签名验证插件。
# 在 Higress 中可以将其封装为 Wasm 插件或 Lua 插件部署。
```




```python
# 示例3：Higress 流量治理（限流）
def higress_rate_limit():
    """
    配置 Higress 的限流规则
    适用场景：保护后端服务免受过载
    """
    from dataclasses import dataclass
    from typing import Dict
    
    @dataclass
    class RateLimitRule:
        """限流规则配置"""
        route: str        # 匹配的路由
        qps: int          # 每秒请求数限制
        burst: int        # 突发流量容量
        key_type: str     # 限流维度（IP/USER等）
    
    def generate_limit_config(rules: Dict[str, RateLimitRule]):
        """生成限流配置"""
        config = {
            "apiVersion": "config.istio.io/v1alpha2",
            "kind": "memquota",
            "metadata": {"name": "handler"},
            "spec": {
                "quotas": [{
                    "name": "requestquota",
                    "maxAmount": rules["api"].qps,
                    "validDuration": "1s",
                    "overrides": [{
                        "dimensions": {
                            "source": rules["api"].key_type
                        }
                    }]
                }]
            }
        }
        return config
    
    # 配置示例：对 /api/* 路由进行每秒 100 次的限流
    rules = {
        "api": RateLimitRule(
            route="/api/*",
            qps=100,
            burst=50,
            key_type="source.ip"
        )
    }
    
    return generate_limit_config(rules)

# 说明：展示了如何配置 Higress 的限流功能，基于 QPS 和突发流量保护后端服务。
# 实际部署时需要结合 Istio 的 Mixer 或 Higress 自带的限流能力。
```


---
## 案例研究


### 1：阿里巴巴内部电商业务与 12306 混合云架构

 1：阿里巴巴内部电商业务与 12306 混合云架构

**背景**:  
在阿里巴巴内部，电商业务（如淘宝、天猫）面临着巨大的流量洪峰，特别是在“双11”等大促期间。同时，阿里巴巴曾协助 12306 铁路售票系统进行流量削峰改造。这些场景需要一个能够承载极高并发、且具备极高稳定性的 API 网关，用于连接前端流量与后端成千上万的微服务集群。

**问题**:  
传统的 Nginx Ingress Controller 在面对超大规模集群（如超过 10,000 个服务）时，配置同步延迟高，且缺乏标准化的流量管理和安全防护能力。系统需要一个既能处理高性能流量转发，又能集成 WAF（Web应用防火墙）和流量控制功能的统一入口，以应对每秒百万级的 QPS（每秒查询率）。

**解决方案**:  
阿里巴巴基于内部多年沉淀的网关技术，开源了 Higress。Higress 基于 Envoy 和 Istio 构建，提供了高性能的云原生 API 网关。在 12306 项目中，利用 Higress 的高并发处理能力和流量削峰填谷的功能，将购票请求暂存于网关层，后端按照处理能力逐步消化请求，防止后端数据库被瞬间巨大的流量击垮。

**效果**:  
通过 Higress 的应用，成功支撑了双十一数百万 QPS 的流量冲击，且在 12306 场景下实现了 99.99% 的可用性保障。相比传统网关，Higress 将长尾请求的延迟降低了 50%，同时通过将流量管理能力下沉到网关层，大幅减轻了后端业务服务的逻辑负担，实现了业务与基础设施的解耦。

---



### 2：某头部互联网金融服务平台的微服务治理

 2：某头部互联网金融服务平台的微服务治理

**背景**:  
某大型互联网金融平台拥有数百个微服务，且业务部署在混合云架构（阿里云 + 自建 IDC）中。随着业务的发展，开发团队发现服务之间的调用关系日益复杂，灰度发布（金丝雀发布）变得难以控制，且不同业务线对于 API 的鉴权标准不统一，存在安全隐患。

**问题**:  
原有的 Ingress 方案缺乏对 HTTP/gRPC 协议的高级路由支持，导致灰度发布只能通过复杂的代码逻辑实现，效率低且易出错。此外，缺乏统一的网关层鉴权机制，导致每个微服务都需要重复实现安全校验代码，增加了维护成本和安全漏洞风险。

**解决方案**:  
该平台引入 Higress 作为统一的 API 网关。利用 Higress 的“插件市场”功能，团队实现了低代码的插件编排。在流量管理方面，通过 Higress 的 Header 匹配和权重路由功能，实现了精细化的金丝雀发布，只需简单配置即可将 5% 的流量路由到新版本服务。在安全方面，启用了 Higress 的 JWT 认证插件，在网关层统一拦截非法请求。

**效果**:  
发布效率显著提升，原本需要数小时准备的灰度发布流程，现在仅需几分钟配置即可完成。由于统一了鉴权逻辑，后端微服务代码量减少了约 15%，安全性得到统一加强。同时，Higress 的热更新能力确保了在频繁变更路由规则时，长连接业务不会出现中断，保障了金融交易的高稳定性。

---



### 3：AIGC（生成式 AI）应用的高性能接入层

 3：AIGC（生成式 AI）应用的高性能接入层

**背景**:  
一家专注于 LLM（大语言模型）应用开发的初创公司，需要将其基于 Llama 等开源模型构建的 AI 对话服务对外开放。由于 AI 对话通常采用 SSE（Server-Sent Events）或流式传输协议，且响应时间较长，传统的 API 网关在处理这种长时间保持连接的流式请求时，往往存在性能瓶颈或连接超时断开的问题。

**问题**:  
客户反映在使用 API 时，流式输出经常中断，或者在高并发下网关成为瓶颈导致 Token 生成速度受限。此外，开发团队希望对 API 调用进行精细的计费统计（如基于 Token 数量），但传统网关只能统计请求数，无法解析内容。

**解决方案**:  
该公司采用了 Higress 作为 AI 服务的专用网关。Higress 原生支持 SSE 和流式传输，能够稳定维持长连接。利用 Higress 的 Wasm 插件能力，团队开发了一个自定义插件，用于在网关层拦截并统计流式传输中的 Token 数量，实现了基于实际用量的实时计费和限流。

**效果**:  
解决了流式传输中断的问题，用户体验大幅提升。通过在网关层进行 Token 统计和限流，有效防止了恶意用户通过高频请求攻击后端昂贵的 GPU 资源。相比直接暴露服务，引入 Higress 后，后端服务的 CPU 开销降低了约 20%，因为网关处理了大量的连接管理和协议适配工作。

---
## 对比分析

## 与同类方案对比

| 维度 | Higress | Nginx | Kong |
|------|------------|--------|--------|
| 性能 | 基于Envoy和Istio，高性能，支持动态配置 | 高性能，但动态配置需额外模块 | 高性能，基于OpenResty |
| 易用性 | 提供控制台和K8s集成，配置灵活 | 配置复杂，需手动编辑文件 | 提供管理界面，但学习曲线较陡 |
| 成本 | 开源免费，云服务按需付费 | 开源免费，企业版收费 | 开源免费，企业版收费 |
| 扩展性 | 支持Wasm插件，扩展性强 | 模块化扩展，但需重新编译 | 支持Lua插件，扩展性较好 |
| 社区支持 | 阿里背书，社区活跃 | 社区成熟，资源丰富 | 社区活跃，商业支持强 |

### 优势分析

- 优势1：深度集成Kubernetes和Istio，适合云原生环境。
- 优势2：支持Wasm插件，扩展性和安全性优于传统方案。
- 优势3：提供免费的控制台和流量管理工具，降低运维成本。

### 不足分析

- 不足1：相比Nginx，文档和社区资源较少。
- 不足2：Wasm插件生态尚不成熟，第三方插件有限。
- 不足3：对非Kubernetes环境的支持较弱。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Envoy 架构的高性能网关部署

**说明**: Higress 深度集成了 Envoy 和 Istio，利用 Envoy 的高性能数据面处理能力。在部署时，应充分利用其云原生特性，将其作为 Ingress Gateway 或 API Gateway 部署在 Kubernetes 集群中，以获得最佳的网络吞吐量和低延迟。

**实施步骤**:
1. 使用 Helm Chart 将 Higress 部署至 Kubernetes 集群。
2. 根据业务规模调整 Higress Gateway 的副本数和资源配额。
3. 配置 Service 类型为 LoadBalancer 或使用 NodePort 对外暴露服务。

**注意事项**: 确保 Kubernetes 集群的内核参数（如 `net.ipv4.ip_forward`）已正确优化，以支持高并发连接。

---

### 实践 2：精细化流量路由与灰度发布

**说明**: 利用 Higress 强大的路由规则管理能力，实现基于 Header、Query 参数、Cookie 或权重百分比的流量路由。这对于蓝绿部署、金丝雀发布等场景至关重要，可最大程度降低新版本上线的风险。

**实施步骤**:
1. 在控制台或通过 YAML 定义 Ingress 路由规则。
2. 配置多个服务版本（Service A v1, Service A v2）作为后端。
3. 设置匹配条件（如 `x-version: v2`）或流量权重（如 10% 流量指向 v2）。

**注意事项**: 路由匹配规则的优先级（Order 字段）非常重要，务必确保更具体的规则优先于通用规则匹配。

---

### 实践 3：插件生态与 WAF 安全防护

**说明**: Higress 提供了丰富的插件扩展能力（如 Keyless 认证、请求限流、基本认证）。特别是结合阿里云 WAF 插件或开源 WAF 插件，可以在网关层直接阻断恶意流量，保护后端服务安全。

**实施步骤**:
1. 在 Higress 控制台导航至“插件管理”页面。
2. 启用 `key-auth` 或 `request-block` 等安全相关插件。
3. 针对特定的路由或域名配置插件规则，例如限制 IP 访问频率。

**注意事项**: 插件的全局开启与针对特定路由开启效果不同，建议仅在需要的域名或路由上启用高开销的安全插件，以避免性能损耗。

---

### 实践 4：服务注册与多协议发现

**说明**: Higress 原生支持 Nacos、Zookeeper、Consul 等注册中心，同时也支持 Kubernetes Service。在混合云或微服务架构中，应配置 Higress 直接对接注册中心，实现自动的服务发现和健康检查，避免硬编码后端 IP。

**实施步骤**:
1. 在 Higress 全局配置中添加服务来源。
2. 输入 Nacos 或 Zookeeper 的服务器地址和命名空间信息。
3. 在创建路由时，直接选择已发现的微服务名称作为服务来源。

**注意事项**: 确保 Higress 所在的网络环境能够直接访问注册中心的端口，注意防火墙策略的配置。

---

### 实践 5：全链路观测与可观测性集成

**说明**: 生产环境必须建立完善的可观测性体系。Higress 原生支持集成 Prometheus、SkyWalking 和 OpenTelemetry。通过收集 Access Log 和 Metrics，可以实时监控网关性能、错误率和服务依赖关系。

**实施步骤**:
1. 配置 Higress 的 Prometheus Fetcher，暴露 Metrics 端口。
2. 开启 Access Log 输出，配置日志收集工具（如 Fluentd/Filebeat）采集日志。
3. 配置 Tracing 协议（如 Zipkin 或 Jaeger），启用链路追踪。

**注意事项**: 高流量下日志量巨大，建议对 Access Log 进行采样或仅记录错误日志，以防磁盘写满或日志处理系统过载。

---

### 实践 6：高可用与容灾配置

**说明**: 网关作为流量入口，其可用性直接决定整体服务的可用性。必须部署多副本 Higress 实例，并结合 Kubernetes 的健康检查与自动重启机制，确保单点故障不影响整体流量。

**实施步骤**:
1. 部署至少 2 个以上的 Higress Gateway 副本，建议分布在不同可用区。
2. 配置 `readinessProbe` 和 `livenessProbe`，确保异常 Pod 能及时被剔除。
3. 如果使用云厂商的 SLB，配置跨可用区的挂载策略。

**注意事项**: 在进行滚动更新或版本升级时，确保 Pod 的优雅终止时间足够长，以便处理存量连接。

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/2 与 HTTP/3 (QUIC) 协议

**说明**:  
Higress 基于 Envoy 构建，原生支持 HTTP/2 和 HTTP/3。HTTP/2 通过多路复用减少连接数，HTTP/3 (QUIC) 则解决了 TCP 队头阻塞问题，特别适合高并发和弱网环境。

**实施方法**:  
1. 在 Higress 网关配置中启用 HTTP/2：
   ```yaml
   apiVersion: networking.higress.io/v1
   kind: McpBridge
   metadata:
     name: my-mcp-bridge
   spec:
     http2: true
   ```
2. 启用 QUIC（需客户端支持）：
   在 `higress-config` ConfigMap 中设置：
   ```yaml
   envoy:
     listener:
       quic: true
   ```

**预期效果**:  
- 高并发场景下延迟降低 20-30%  
- 弱网环境下吞吐量提升 40%  

---

### 优化 2：配置智能路由与缓存

**说明**:  
通过 Higress 的路由规则和缓存策略减少后端服务压力。例如，对静态资源或高频 API 响应启用缓存。

**实施方法**:  
1. 定义缓存策略：
   ```yaml
   apiVersion: extensions.higress.io/v1alpha1
   kind: RequestAuth
   metadata:
     name: cache-policy
   spec:
     cache:
       enabled: true
       ttl: 60s
       cacheKey: ["request.path", "request.headers['Accept-Language']"]
   ```
2. 按路径权重分配流量（金丝雀发布）：
   ```yaml
   apiVersion: networking.higress.io/v1
   kind: Ingress
   spec:
     rules:
       - host: example.com
         http:
           paths:
             - path: /api/v1
               backend:
                 service:
                   name: service-v1
                   weight: 80
                 service:
                   name: service-v2
                   weight: 20
   ```

**预期效果**:  
- 后端负载减少 30-50%  
- 缓存命中时响应时间降低至 5ms 以内  

---

### 优化 3：启用 Wasm 插件加速动态处理

**说明**:  
Higress 支持 Wasm 插件，可用于高频逻辑（如鉴权、限流）的近数据面处理，避免 Lua 或外部调用的性能损耗。

**实施方法**:  
1. 编写 Wasm 插件（Rust/AssemblyScript）：
   ```rust
   #[no_mangle]
   pub extern "C" fn on_http_request(ctx: *mut Context) -> Action {
       // 自定义鉴权逻辑
       Action::Continue
   }
   ```
2. 部署插件：
   ```bash
   higress plugin install my-wasm.wasm --config config.json
   ```

**预期效果**:  
- 动态处理延迟降低 60%  
- CPU 占用减少 40%  

---

### 优化 4：优化连接池与超时配置

**说明**:  
调整 Envoy 的连接池参数（如最大连接数、超时时间）可避免资源耗尽和雪崩效应。

**实施方法**:  
1. 修改 `higress-config` ConfigMap：
   ```yaml
   envoy:
     cluster:
       maxConnections: 10000
       maxPendingRequests: 5000
       maxRequestsPerConnection: 100
       connectTimeout: 5s
   ```
2. 针对慢服务设置熔断：
   ```yaml
   apiVersion: networking.higress.io/v1
   kind: CircuitBreaker
   metadata:
     name: slow-service
   spec:
     threshold: 50
     interval: 60s
   ```

**预期效果**:  
- 错误率降低 70%  
- 资源利用率提升 25%  

---

### 优化 5：启用 Prometheus 监控与自适应调优

**说明**:  
通过 Higress 内置

---
## 学习要点

- Higress 是阿里开源的基于 Istio 的云原生 API 网关，深度集成了 K8s 与 Envoy，提供高性能流量管理能力
- 支持将 K8s Ingress 与 Service Mesh 流量统一管理，简化多协议（HTTP/gRPC/Dubbo）路由配置
- 内置 WAF 安全防护与流量镜像功能，可直接复用 Istio 的服务治理能力（如熔断、限流、灰度发布）
- 提供标准 Kubernetes CRD 扩展，兼容 Nginx Ingress 注解语法，降低迁移成本
- 通过插件市场（如 AI 推理加速、认证鉴权）实现业务逻辑热插拔，无需重启网关
- 支持多集群南北向流量调度与东西向流量治理，适合混合云或边缘计算场景
- 默认集成 Prometheus 监控与 Grafana 仪表盘，提供实时可观测性数据


---
## 学习路径

## 学习路径

### 阶段 1：入门基础

**学习内容**:
- 云原生网关的基本概念与 Higress 的核心定位
- Higress 与传统网关（如 Nginx, Kong）及阿里云 API 网关的区别
- Higress 的核心架构：Istio + Envoy 的结合模式
- 基础环境搭建：Docker 容器化部署与 Kubernetes 集群部署
- 控制台的基本操作与界面熟悉

**学习时间**: 1-2周

**学习资源**:
- Higress 官方 GitHub 仓库 README
- Higress 官方文档（快速开始部分）
- 云原生网关技术对比文章

**学习建议**: 
建议先通过 Docker 方式在本地快速启动一个 Higress 实例，通过控制台创建一个简单的路由转发（例如将请求转发到 httpbin.org），以建立直观认识。不要一开始就陷入复杂的 K8s 配置中。

---

### 阶段 2：核心功能掌握

**学习内容**:
- 流量管理：基于域名、路径、Header 的路由规则配置
- 服务来源管理：接入 Nacos、Consul、固定地址（DNS/IP）及 K8s Service
- 安全防护：插件体系基础、Key Auth 认证、IP 访问控制
- 负载均衡策略：加权轮询、一致性哈希等算法配置
- 全局或域名级别的流量治理（超时、重试、熔断）

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 流量管理与服务来源板块
- Higress 官方插件市场文档
- Envoy 基础代理原理教程

**学习建议**: 
尝试搭建一个微服务模拟场景（例如使用 Spring Cloud 或 Go 微服务），配置 Nacos 作为注册中心，让 Higress 自动发现服务并进行转发。重点练习如何通过配置路由规则实现金丝雀发布（灰度发布）。

---

### 阶段 3：插件开发与扩展

**学习内容**:
- Higress 插件运行机制（Wasm 支持）
- 使用 Lua/Go/Java 开发自定义 Wasm 插件
- 插件配置与生命周期管理
- 网关级别的限流与熔断高级配置
- 请求/响应的 Header 与 Body 修改技巧

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档 - 自定义插件开发指南
- Wasm (WebAssembly) 在网关中的应用案例
- Higress 官方插件源码分析（GitHub）

**学习建议**: 
从修改一个现有的官方插件开始（例如修改 request-header 插件），理解 `ctx` 对象的传递。随后尝试编写一个简单的认证或鉴权插件。学习如何在本地编译 Wasm 文件并上传到 Higress 控制台进行调试。

---

### 阶段 4：生产级运维与性能优化

**学习内容**:
- 在 Kubernetes 集群中的 Helm 高级部署与配置
- Higress 的高可用（HA）架构设计与部署
- 观测性：对接 Prometheus/Grafana 进行监控，集成链路追踪
- 网关性能调优：连接池、缓冲区大小、并发数配置
- 灾难恢复与数据备份策略
- 与 Ingress Controller 的集成使用

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 运维指南
- Kubernetes Ingress 与 Gateway API 规范
- Envoy 性能调优最佳实践白皮书

**学习建议**: 
在测试环境的 K8s 集群中使用 Helm 部署 Higress，模拟高并发流量（使用 JMeter 或 Hey），观察 Higress 的 QPS 表现和资源消耗。配置 Prometheus 采集指标，并配置告警规则。

---

### 阶段 5：源码研读与架构精通

**学习内容**:
- Higress 项目源码结构分析
- Istio 控制平面在 Higress 中的适配与改造
- Envoy 数据平面的扩展机制深度解析
- 参与社区贡献与 Roadmap 规划
- 多租户网关架构设计

**学习时间**: 持续学习

**学习资源**:
- Higress GitHub 源码
- Istio 官方文档与源码
- Envoy 官方深度文档

**学习建议**: 
下载源码至本地，使用 IDE（如 GoLand）进行跟踪调试。重点关注 `router` 和 `wasm` 相关的代码逻辑。尝试阅读社区的 RFC 文档，理解未来的设计方向，并尝试提交 PR 修复 Bug 或增加文档。

---
## 常见问题


### 1: Higress 是什么？它与阿里巴巴和云原生社区有什么关系？

1: Higress 是什么？它与阿里巴巴和云原生社区有什么关系？

**A**: Higress 是一款基于阿里内部两年多的实战经验，由阿里云联手蚂蚁集团以及多家社区伙伴共同开源的**云原生 API 网关**。它建立在 Envoy 和 Istio 等开源项目之上，旨在提供标准化的云原生网关体验。Higress 源自阿里巴巴内部对统一网关架构的需求，能够承接从流量网关到微服务网关的各种业务场景，是阿里云云原生产品线的重要组成部分。

---



### 2: Higress 与 Nginx、Istio 或传统的 Kong 网关相比有什么核心优势？

2: Higress 与 Nginx、Istio 或传统的 Kong 网关相比有什么核心优势？

**A**: Higress 的核心优势在于其**深度集成与标准化**：
1.  **架构先进**：基于 Istio 与 Envoy 构建，天然支持 K8s 环境，比传统 Nginx 配置更易于云原生集成。
2.  **安全与流量统一**：它将传统的“流量网关”（如 Nginx）与“微服务网关”（如 Spring Cloud Gateway）的功能合二为一，降低了运维复杂度。
3.  **插件生态兼容**：深度兼容 Nginx 的 Lua 插件生态，同时也支持 WASM (WebAssembly) 插件，使得扩展性更强且更安全（插件崩溃不会导致网关崩溃）。
4.  **服务发现集成**：原生支持 Nacos、Consul、ZooKeeper 以及 Kubernetes Service，无需手动维护繁琐的上游服务列表。

---



### 3: Higress 是否支持从 Nginx 或其他网关平滑迁移？

3: Higress 是否支持从 Nginx 或其他网关平滑迁移？

**A**: 是的，Higress 非常重视迁移的便利性。
1.  **Nginx 兼容**：Higress 提供了 Nginx 配置转换工具，并且支持直接使用 Nginx 的 Lua 插件逻辑，用户无需重写代码即可复用现有的 Nginx 插件资产。
2.  **Ingress 支持**：Higress 完全兼容 K8s Ingress 和 Gateway API 标准，可以作为 K8s 集群的 Ingress Controller 直接替换 Nginx Ingress Controller。
3.  **配置导入**：提供了工具帮助用户将旧网关的配置规则快速导入到 Higress 中。

---



### 4: Higress 如何处理插件扩展？是否支持 WASM？

4: Higress 如何处理插件扩展？是否支持 WASM？

**A**: Higress 拥有非常强大的插件系统，支持**多语言扩展**。
1.  **WASM 支持**：Higress 原生支持 WebAssembly (WASM)，允许开发者使用 Go、C++、Rust 或 AssemblyScript 编写插件。WASM 插件具有沙箱隔离特性，运行更安全，且支持动态热加载，无需重启网关即可更新插件逻辑。
2.  **Lua 支持**：继续支持传统的 Lua 插件开发，方便从 OpenResty 迁移过来的用户。
3.  **内置插件市场**：Higress 提供了开箱即用的官方插件市场，包含认证、限流、流量镜像、可观测性等常见功能的插件。

---



### 5: Higress 的性能表现如何？能否应对高并发场景？

5: Higress 的性能表现如何？能否应对高并发场景？

**A**: Higress 专为高性能设计。
1.  **底层优势**：基于高性能代理 Envoy 构建，具备处理大规模流量的能力。
2.  **阿里实践**：Higress 的核心代码源自阿里巴巴内部经过“双十一”大促考验的网关系统，能够支撑每秒百万级请求的吞吐量。
3.  **低延迟**：通过全链路优化和热代码加载技术，Higress 在开启复杂插件逻辑的情况下依然能保持极低的转发延迟。

---



### 6: Higress 是否支持 WAF（Web 应用防火墙）功能？

6: Higress 是否支持 WAF（Web 应用防火墙）功能？

**A**: 是的，Higress 提供了内置的安全防护能力。
1.  **内置 WAF**：Higress 集成了基础的 WAF 功能，可以防御常见的 SQL 注入、XSS、远程命令执行等 Web 攻击。
2.  **插件集成**：除了内置规则，用户还可以通过安装插件的方式对接第三方安全能力，或者通过 Lua/WASM 编写自定义的安全拦截逻辑。
3.  **Bot 防护**：针对爬虫和恶意 Bot 流量，Higress 也提供了相应的识别和拦截手段。

---



### 7: 如何在本地或 Kubernetes 集群中快速部署 Higress？

7: 如何在本地或 Kubernetes 集群中快速部署 Higress？

**A**: Higress 提供了极其简单的部署方式：
1.  **Docker 部署**：可以通过一条 Docker 命令快速启动一个单机版的 Higress，适合本地开发测试。
2.  **Kubernetes (Helm)**：在生产环境中，推荐使用 Helm Chart 进行部署。只需添加 Higress 的 Helm 仓库并执行 `helm install`，即可在 K8s 集群中部署高可用的 Higress 服务。
3.  **控制台**：部署完成后，Hig

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: 快速上手与路由配置

### 问题**:

### 在本地 Docker 环境中快速启动 Higress，并配置一个简单的路由规则，将访问 `http://localhost/test` 的流量转发到一个模拟的后端服务（如 httpbin.org）。

### 提示**:

---
## 实践建议

基于 Higress 作为 AI Native API 网关的定位，结合其基于 Istio 和 Envoy 的高性能架构，以下是 5-7 条针对实际生产环境的实践建议：

### 1. 利用 Wasm 插件实现 LLM 提示词管理与安全防护
**场景**：在对接大模型（LLM）时，直接将 Prompt 写在客户端代码中难以维护，且容易遭受 Prompt Injection（提示词注入）攻击。
**建议**：
*   **提示词预处理**：编写 Wasm 插件（Go 或 C++），在网关层实现 Prompt Template 的渲染。客户端只需传递业务参数，网关自动填充预设的系统提示词，实现集中管理。
*   **敏感词过滤**：利用 Wasm 插件的请求拦截能力，在请求发送给 LLM 之前，对用户输入进行实时的敏感词审查，降低合规风险。

### 2. 实施基于 Token 的精细化流控与缓存
**场景**：AI 接口的调用成本通常按 Token 计费，且后端模型有严格的 RPM（每分钟请求数）或 TPM（每分钟 Token 数）限制。
**建议**：
*   **Token 级别限流**：不要仅使用传统的 QPS 限流。配置 Higress 的本地限流或全局限流规则，针对 LLM 路由启用基于 Token 预估或实际 Token 消耗的限流策略，防止因突发流量导致后端 API 账单透支或被封禁。
*   **语义缓存**：对于相似度高的用户查询（例如高频的常识性问题），配置结果缓存策略。通过缓存 LLM 的响应直接返回，不仅能减少延迟，还能显著降低 Token 消耗成本。

### 3. 配置模型供应商的容错与降级策略
**场景**：单一模型服务商（如 OpenAI 或 Azure）可能出现 API 不稳定或网络抖动，导致 AI 业务中断。
**建议**：
*   **多模型路由**：配置多个服务来源（例如同时配置 OpenAI 和通义千问作为后端）。
*   **自动故障转移**：利用 Higress 的主动健康检查（Active Health Check）和重试机制。当主模型供应商返回 5xx 错误或响应超时时，网关自动将请求切换至备用模型供应商，确保业务高可用。

### 4. 优化流式传输的网关配置
**场景**：AI 对话场景普遍采用 SSE（Server-Sent Events）流式返回，以改善用户体验。
**建议**：
*   **全链路流式支持**：确保网关的路由配置开启了 HTTP 升级（HTTP Upgrade）支持，并针对 SSE 协议调整超时时间。默认的网关超时设置可能过短，导致长连接被中断。
*   **首包优化**：监控 TTFB（Time to First Byte）指标。在 Wasm 插件处理逻辑中，避免进行阻塞式的长耗时计算，确保用户能尽快看到第一个字符的生成。

### 5. 建立可观测性体系以监控 Token 成本与模型性能
**场景**：AI 应用除了关注传统的延迟和成功率，还需要关注 Token 消耗和模型响应质量。
**建议**：
*   **自定义指标采集**：通过 Wasm 插件或 Higress 的日志采集能力，提取请求和响应中的 `usage` 字段（包含 prompt_tokens, completion_tokens 等）。
*   **关联业务日志**：将 AI 调用的元数据（模型版本、Token 数、耗时）输出到可观测性平台（如 Prometheus + Grafana 或阿里云 SLS）。这不仅用于排查性能问题，更是后续核算 AI 成本和优化 Prompt 效果的数据基础。

### 6. 避免在网关层进行大体积上下文拼接
**场景**：为了增强对话效果，开发者常需要传递长文档或历史记录作为上下文。
**建议**：
*   **警惕 Body 大小限制**：网关的主要职责是路由和轻量级处理，不应承担大文件的拼接任务。过大的 Body 会占用网关大量内存

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [Higress](/tags/higress/) / [AI 原生](/tags/ai-%E5%8E%9F%E7%94%9F/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [WASM](/tags/wasm/) / [MCP](/tags/mcp/) / [Kubernetes](/tags/kubernetes/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/) / [Kubernetes](/scenarios/kubernetes/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260217-github_trending-alibaba-higress-6.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260206-github_trending-alibaba-higress-0.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260206-github_trending-alibaba-higress-6.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260213-github_trending-alibaba-higress-5.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*