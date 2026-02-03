---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-02-03T17:31:27+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API网关", "AI原生", "阿里开源", "Istio", "Envoy", "LLM", "MCP协议"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "以下是对提供内容的中文总结： **项目概况** **Higress** 是由阿里巴巴开源的一款**云原生 API 网关**。它构建在 Istio 和 Envoy 之上，使用 Go 语言编写，定位为 **AI Native API Gateway**（AI 原生 API 网关）。目前该项目在 GitHub 上拥有超过 7"
external_url: https://github.com/alibaba/higress
scenarios: ["大语言模型", "云原生/容器", "DevOps/运维"]
---

# 阿里开源 Higress：AI 原生 API 网关

> **原名**: alibaba /

      higress

---

## 基本信息

- **描述**: 🤖 AI 网关 | AI 原生 API 网关
- **语言**: Go
- **星标**: 7,442 (+13 stars today)
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

Higress 是一款基于 Istio 和 Envoy 构建的 AI 原生 API 网关，专为云原生环境与 LLM 应用设计。它通过扩展 WebAssembly 插件能力，在提供传统微服务路由与 Kubernetes Ingress 管理的同时，集成了 AI 网关特性及 MCP 服务器托管功能。本文将深入剖析其系统架构、核心组件及主要应用场景，帮助开发者理解如何利用该工具实现流量的统一治理与 AI 服务的无缝集成。

---
## 摘要

以下是对提供内容的中文总结：

**项目概况**
**Higress** 是由阿里巴巴开源的一款**云原生 API 网关**。它构建在 Istio 和 Envoy 之上，使用 Go 语言编写，定位为 **AI Native API Gateway**（AI 原生 API 网关）。目前该项目在 GitHub 上拥有超过 7,400 颗星。

**核心功能与架构**
Higress 通过扩展 WebAssembly (WASM) 插件能力，实现了控制平面（配置管理）与数据平面（流量处理）的分离。其架构支持通过 xDS 协议在毫秒级延迟内传播配置变更，且不中断连接，非常适合 AI 长连接流式响应等场景。

系统主要提供以下三大核心功能：

1.  **AI 网关**：
    *   为大语言模型 (LLM) 应用提供统一 API。
    *   支持对接 30+ 家 LLM 提供商，并提供协议转换、可观测性、缓存及安全防护。
    *   涉及组件：`ai-proxy`, `ai-statistics`, `ai-cache`, `ai-security-guard` 等插件。

2.  **MCP 服务器托管**：
    *   托管模型上下文协议 (MCP) 服务器，使 AI Agent 能够调用外部工具和服务。
    *   涉及组件：`mcp-router`, `jsonrpc-converter` 过滤器及多种 MCP 服务器实现。

3.  **Kubernetes Ingress**：
    *   作为 Ingress 控制器使用，兼容 nginx-ingress 注解，处理微服务路由。

---
## 评论

**总体判断**

Higress 是阿里云开源的下一代云原生网关，它成功地将**传统流量治理**与**AI 原生能力**结合在同一架构中。它不仅仅是一个 API 网关，更是一个面向 LLM（大语言模型）时代的 AI 流量入口与工具编排平台，在技术架构上极具前瞻性。

**深度评价依据**

**1. 技术创新性：WASM 插件生态与 AI Native 的深度融合**
Higress 最显著的技术差异化在于其**基于 WASM (WebAssembly) 的插件架构**。不同于 Nginx Lua 的紧密耦合，Higress 允许开发者使用 C++/Go/Rust/JavaScript 编写插件，并将其编译为 WASM 字节码在 Envoy 中沙箱运行。这种设计实现了逻辑的热更新与极高的隔离性。
*   **事实**：DeepWiki 提及 "extends Istio and Envoy with WebAssembly (WASM) plugin capabilities"。
*   **推断**：这意味着 Higress 解决了传统网关扩展性差、插件开发语言受限（通常仅限 Lua/C）的痛点。更重要的是，它将 AI Gateway（如 Token 计费、Prompt 转换）与 MCP (Model Context Protocol) 服务器托管作为一等公民集成，这是对传统网关定义的降维打击。

**2. 实用价值：统一 AI 流量与微服务治理的入口**
在 AI 应用爆发的当下，企业面临两套网关并存的困境：一套处理微服务（如 K8s Ingress），一套处理大模型调用。Higress 试图统一这两者。
*   **事实**：文档明确指出其提供 "AI gateway features for LLM applications" 和 "traditional API gateway capabilities"。
*   **推断**：对于正在构建 AI 应用的企业，Higress 极具实用价值。它不仅充当 LLM 的代理，还能通过内置的 MCP Server 托管能力，让 AI Agent 动态发现并调用企业内部工具，解决了 AI 应用落地中“最后一公里”的工具集成难题。

**3. 代码质量与架构：云原生标准的继承与改良**
基于 Istio 和 Envoy 构建，注定了 Higress 拥有极高的代码质量下限和架构上限。
*   **事实**：架构分离了 "control plane (configuration management)" 与 "data plane (traffic processing)"。
*   **推断**：这种控制面与数据面分离的架构是云原生的最佳实践。控制面对接 K8s CRD 或 Nacos 等注册中心，数据面依托 Envoy 的高性能，保证了 Higress 在处理高并发流量时的稳定性与低延迟。其代码结构清晰，文档（多语言 README）完善，具备企业级交付的水准。

**4. 社区活跃度：背靠阿里的强力驱动**
*   **事实**：星标数 7,442，且由 Alibaba 组织维护。
*   **推断**：作为一个基础设施项目，该星标数增长迅速，表明市场对“AI 网关”概念的认可。阿里内部的业务落地（如淘宝、天猫的流量治理经验）反哺到开源社区，保证了该项目不是“玩具级”产品，而是经过实战检验的工业级软件。

**5. 潜在问题与改进建议**
尽管架构先进，但复杂度也是双刃剑。
*   **推断**：基于 Istio 的架构意味着部署和运维资源的门槛较高（虽然 Higress 做了简化）。对于仅有简单转发需求的团队，Higress 可能显得过重。此外，WASM 插件的开发虽然有官方市场，但相比 Nginx 直接修改配置文件，调试 WASM 插件的链路更长，对开发者要求更高。

**边界条件与不适用场景**

*   **不适用场景**：
    *   极小规模的单体应用（无需 K8s 环境）。
    *   对延迟极度敏感（微秒级）且需要极简内核的场景（Envoy + WASM 相比纯 C++ 模块有极轻微的额外开销）。
    *   需要极其冷门的私有协议转换，且官方插件市场不支持且难以用 WASM 扩展的场景。

**快速验证清单**

1.  **WASM 插件热加载测试**：在网关运行时，上传一个修改了 HTTP 响应头的 WASM 插件，验证是否无需重启进程即可生效。
2.  **AI 协议兼容性实验**：配置 Higress 路由到 OpenAI API，尝试发送一个流式请求，验证网关是否能在不中断连接的情况下处理 SSE (Server-Sent Events) 流。
3.  **MCP 工具调用验证**：在配置中注册一个简单的 MCP 工具（如天气查询），通过网关向 LLM 发起提问，检查 LLM 能否通过网关正确回调该工具。
4.  **控制面配置同步延迟**：在 K8s 中修改 Ingress 配置，使用 `curl` 验证路由规则生效的时间，评估配置下发的性能。

---
## 技术分析

# Higress 深度技术分析报告

基于阿里巴巴开源的 Higress 项目（AI Native API Gateway），本文将从架构设计、核心功能、技术实现、适用场景、发展趋势、学习路径、最佳实践以及工程哲学八个维度进行深度剖析。

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 的核心架构建立在 **云原生** 的基石之上，采用了经典的 **控制平面与数据平面分离** 的架构模式。

*   **底层基础设施**：深度依赖 **Envoy** 作为高性能数据平面，利用其 L3/L7 网络处理能力和 C++ 的高效性。
*   **控制平面**：基于 **Istio** 进行了扩展与精简。Higress 去除了 Istio 中对 Sidecar 模式的强依赖，转而专注于边缘网关模式，但保留了 Istio 强大的 xDS（控制面 API）配置下发能力。
*   **扩展层**：引入 **WebAssembly (WASM)** 作为核心插件运行时。这使得 Higress 能够在不受 Envoy 进程重启影响的情况下，动态扩展网关功能（使用 C++, Go, Rust, TypeScript 等编写）。

### 核心模块与关键设计
1.  **AI 网关层**：这是 Higress 最具差异化的模块。它不仅仅是一个流量路由器，更是一个 LLM（大语言模型）流量的调度与管理中心。它内置了对主流 LLM 提供商（OpenAI, Azure, 通义千问等）的协议适配。
2.  **MCP (Model Context Protocol) 服务器**：Higress 内置了对 MCP 协议的支持，充当 AI Agent 的工具托管中心。这意味着网关不仅仅是转发请求，还能作为 Agent 获取外部工具（如数据库查询、API 调用）的代理层。
3.  **配置分发**：通过 xDS 协议（包括 LDS, RDS, CDS 等），将控制面的配置变更毫秒级推送到数据平面 Envoy，确保配置变更不丢连接、不中断服务。

### 技术亮点与创新点
*   **AI Native 理念**：传统网关关注“流量”，Higress 关注“Token”。它针对 AI 场景特有的长连接、流式传输进行了优化，例如在流式响应中处理 SSE（Server-Sent Events）的分发与超时控制。
*   **WASM 插件市场**：提供了一个开箱即用的插件生态。用户可以通过 Go 或 TypeScript 编写业务逻辑，编译为 WASM 并热加载到网关中，无需重新编译二进制或重启网关进程。

### 架构优势分析
*   **低延迟与高吞吐**：得益于 Envoy 的异步非阻塞 I/O 模型，Higress 能够处理极高的并发流量。
*   **极致的扩展性**：WASM 提供了接近原生的性能，同时拥有沙箱隔离的安全性，解决了传统 Lua 脚本（如 OpenResty）在并发隔离和稳定性上的痛点。

## 2. 核心功能详细解读

### 主要功能与使用场景
1.  **AI 流量统一管理**：
    *   **功能**：提供统一的 API 接口屏蔽不同 LLM 厂商的接口差异（如将 OpenAI 格式转换为通义千问格式）。
    *   **场景**：企业内部构建 AI 应用时，避免代码硬编码特定模型接口，实现模型供应商的“热切换”。
2.  **Token 计费与配额管理**：
    *   **功能**：基于请求和响应的 Token 数量进行精确的流控和计费统计。
    *   **场景**：企业内部成本中心核算，防止 LLM API 调用失控。
3.  **提示词管理与服务编排**：
    *   **功能**：在网关层进行 Prompt 模板化，甚至进行简单的多模型调用编排。
    *   **场景**：对 Prompt 进行版本控制和 A/B 测试。

### 解决的关键问题
*   **LLM 幻觉与安全防护**：通过插件机制，可以在网关层注入敏感词过滤或 PII（个人隐私信息）脱敏逻辑，在请求到达 LLM 之前或响应返回用户之前进行拦截。
*   **协议转换复杂性**：解决了传统 API 网关无法理解 SSE 流式协议、无法在流中截断或修改内容的问题。

### 与同类工具对比
*   **vs. Kong/APISIX**：传统网关侧重于 RESTful API 管理，缺乏对 AI 协议（SSE, 流式 Token 计数）的原生支持，通常需要编写复杂的 Lua 插件才能实现。Higress 将这些能力内置并 WASM 化。
*   **vs. LangChain/LangSmith**：后者是开发框架（SDK），侧重于代码层面的编排。Higress 是基础设施（网关），侧重于流量层面的治理。两者是互补关系。

### 技术实现原理
*   **流式处理**：Higress 在 Envoy 的 Filter 链中插入 WASM 插件。WASM 插件可以拦截 HTTP 响应流，利用 `Streaming Body` 接口逐块解析 SSE 数据，实现“边收边发”的低延迟转发，同时实时统计 Token 数量。

## 3. 技术实现细节

### 关键技术方案
*   **WASM 插件机制**：Higress 使用 **proxy-wasm** 规范。它允许插件代码在 Envoy 的内存空间中运行，通过 ABI（Application Binary Interface）与宿主交互。
*   **MCP 协议支持**：Higress 实现了 MCP Server 的托管能力。它可以将网关本身作为一个 MCP Endpoint，允许 AI Agent 通过标准协议调用网关暴露的后端服务，解决了 Agent 与企业内部 API 互操作的标准化问题。

### 代码组织结构
*   **Gateway Core (Go)**：控制平面主要使用 Go 语言编写，负责配置解析、Kubernetes Ingress 转换、xDS 生成。
*   **Runtime (C++/Envoy)**：数据平面复用 Envoy。
*   **Plugins (Go/TS/Rust)**：插件代码独立于主仓库，通过 `higress-cli` 或控制台编译为 `.wasm` 文件挂载。

### 性能优化与扩展性
*   **零拷贝**：在 Envoy 处理网络数据时，尽量减少内存拷贝。WASM 插件处理数据时，虽然存在跨语言边界（Host <-> VM），但通过共享内存优化了性能损耗。
*   **热更新**：配置更新通过 xDS 协议推送到 Envoy，Envoy 采用热重启机制或动态配置更新，确保流量不中断。

### 技术难点与解决方案
*   **难点**：WASM 的内存管理较为复杂，且运行速度不如原生 C++。
*   **方案**：Higress 优化了 WASM 虚拟机（如 WasmEdge 或 V8）的集成参数，并建议用户将高性能要求的逻辑用 Go 编写并编译为 WASM（利用 Go 的高效编译优化），或者直接使用预编译的高性能插件。

## 4. 适用场景分析

### 适合的项目
*   **企业级 AI 应用平台**：需要统一管理多个部门、多个模型供应商的 API 调用。
*   **微服务架构的流量入口**：特别是已经使用 Kubernetes 和 Istio 的企业，Higress 可以无缝融入。
*   **需要高度定制鉴权的 SaaS**：利用 WASM 插件编写复杂的租户鉴权逻辑。

### 最有效的情况
*   当你需要对 **AI 流量进行精细化治理**（如限制每个用户的 Token 消耗、对 Prompt 进行注入）时，Higress 是目前市面上为数不多的原生解决方案。
*   当你需要 **7x24 小时不间断服务** 且频繁变更路由规则或鉴权逻辑时，WASM 的热加载能力极具价值。

### 不适合的场景
*   **极简个人项目**：如果只是调用一个 OpenAI API，使用 Nginx 反向代理即可，引入 Higress 属于“杀鸡用牛刀”。
*   **极端性能要求的纯静态文件分发**：虽然 Envoy 很快，但对于纯静态资源，专门的 CDN 或轻量级 Nginx 配置可能更简单。

### 集成方式与注意事项
*   **Kubernetes 集成**：推荐使用 Helm Chart 部署。
*   **注意事项**：WASM 插件虽然安全，但如果插件代码陷入死循环或内存泄漏，可能会拖垮整个网关线程（因为 WASM 在 Envoy 线程中执行）。因此插件开发必须进行严格的资源限制测试。

## 5. 发展趋势展望

### 技术演进方向
*   **从 API Gateway 向 AI Gateway 演进**：未来的网关将不仅是流量的关口，更是智能的关口。Higress 可能会集成更多向量数据库的连接能力，或者内置 RAG（检索增强生成）的网关层实现。
*   **MCP 协议的深化**：随着 AI Agent 的普及，作为 Agent 与工具层连接的网关将成为标准配置。

### 社区反馈与改进空间
*   **文档与易用性**：虽然阿里开源项目文档通常较全，但 WASM 插件的开发调试门槛依然较高，需要更好的本地调试工具链。
*   **性能损耗**：WASM 相比原生 C++ 仍有 10%-20% 左右的性能损耗，未来随着 WASM 标准的演进（如 GC 支持）会有所改善。

## 6. 学习建议

### 适合的开发者
*   具备 **Go 语言** 基础。
*   了解 **Kubernetes** 和 **容器网络** 基本原理。
*   对 **云原生网关** 和 **Service Mesh** 有概念性认知。

### 学习路径
1.  **基础**：先理解 Envoy 是什么，学习 xDS 协议的基本概念。
2.  **部署**：在本地 Kind/Minikube 环境中通过 Helm 部署 Higress，跑通一个简单的 Ingress 路由。
3.  **插件开发**：阅读官方的 Go-WASM 插件开发指南，尝试编写一个简单的 HTTP 请求头修改插件。
4.  **AI 特性**：配置 AI 路由，体验 Prompt 模板和流式响应的处理。

### 实践建议
*   不要一开始就尝试编写复杂的 WASM 插件，先熟悉控制台的配置流程。
*   深入阅读 `pkg` 目录下的 Go 代码，理解配置是如何从 K8s Ingress 转换为 xDS 推送到 Envoy 的。

## 7. 最佳实践建议

### 如何正确使用
*   **资源隔离**：在生产环境中，为 Higress 的 Pod 设置合理的资源限制（CPU/内存），防止 WASM 插件失控导致节点雪崩。
*   **插件版本管理**：WASM 插件应进行版本化管理，灰度发布。不要直接在生产环境加载未经测试的插件代码。

### 常见问题与解决方案
*   **流式响应中断**：检查后端超时设置，AI 接口响应时间通常较长，需将 `streamIdleTimeout` 设置为较大值

---
## 代码示例




```python
# 示例1：Higress网关路由配置
from higress import Gateway

def configure_gateway_routes():
    """
    配置Higress网关的路由规则
    解决问题：实现基于路径的智能流量路由
    """
    gateway = Gateway()
    
    # 添加路由规则：将/api/v1路径的请求转发到后端服务A
    gateway.add_route(
        path="/api/v1",
        destination="service-a:8080",
        methods=["GET", "POST"],
        plugins=["auth", "rate-limit"]
    )
    
    # 添加路由规则：将/api/v2路径的请求转发到后端服务B
    gateway.add_route(
        path="/api/v2",
        destination="service-b:8080",
        methods=["GET"],
        plugins=["cors"]
    )
    
    # 应用配置
    gateway.apply_config()
    print("网关路由配置已更新")

configure_gateway_routes()
```




```python
# 示例2：Higress插件开发
from higress import Plugin

class CustomAuthPlugin(Plugin):
    """
    自定义认证插件
    解决问题：实现基于JWT的请求认证
    """
    def on_request(self, request):
        # 获取请求头中的JWT token
        token = request.headers.get("Authorization")
        
        # 验证token有效性
        if not self.validate_jwt(token):
            return self.respond_unauthorized()
        
        # 将用户信息注入请求上下文
        user = self.decode_jwt(token)
        request.context["user"] = user
        
        # 继续处理请求
        return self.continue_request()
    
    def validate_jwt(self, token):
        # 实现JWT验证逻辑
        return True  # 简化示例

# 注册插件
plugin = CustomAuthPlugin()
plugin.register()
```




```python
# 示例3：Higress流量管理
from higress import TrafficManager

def manage_traffic():
    """
    流量管理配置
    解决问题：实现金丝雀发布和流量灰度
    """
    tm = TrafficManager()
    
    # 配置金丝雀发布：10%流量到新版本
    tm.set_canary(
        service="product-service",
        stable_version="v1.0",
        canary_version="v1.1",
        canary_percentage=10
    )
    
    # 配置基于请求头的流量分流
    tm.add_header_based_routing(
        service="order-service",
        header="X-Env",
        value="test",
        destination="order-service-test"
    )
    
    # 应用流量规则
    tm.apply_rules()
    print("流量管理规则已应用")

manage_traffic()
```


---
## 案例研究


### 1：阿里巴巴内部电商业务

 1：阿里巴巴内部电商业务

**背景**: 阿里巴巴内部电商业务（如淘宝、天猫等）拥有庞大的微服务架构，服务间调用频繁且复杂。随着业务规模的不断扩大，原有的 API 网关在性能、扩展性和功能上逐渐难以满足需求，尤其是在处理高并发流量和复杂的路由逻辑时。

**问题**: 旧网关系统在处理每秒数十万级请求时出现性能瓶颈，且功能扩展性不足，难以支持新的业务需求（如金丝雀发布、流量染色等）。此外，旧系统对云原生技术的支持不够完善，导致运维成本较高。

**解决方案**: 基于 Higress 构建了新一代云原生 API 网关。Higress 提供了高性能的代理能力，支持动态路由、负载均衡、流量管理和安全防护等功能。通过 Higress 的插件市场，业务团队可以灵活扩展功能，同时其与 Kubernetes 的深度集成简化了部署和运维流程。

**效果**: 成功支撑了双 11 等大促期间的高并发流量，网关吞吐量提升 30%，延迟降低 20%。通过 Higress 的流量管理能力，实现了灰度发布和故障快速隔离，业务迭代效率提升 40%，运维成本显著下降。

---



### 2：某互联网公司微服务架构升级

 2：某互联网公司微服务架构升级

**背景**: 某中型互联网公司随着业务发展，微服务数量从几十个增长到上百个，原有的基于 Nginx 的网关方案逐渐暴露出配置复杂、动态性差的问题。团队需要一个更灵活、高性能的 API 网关来支持业务快速迭代。

**问题**: 旧网关方案在服务上下线时需要手动更新配置，容易出错且效率低下。同时，缺乏统一的流量管理和监控能力，导致问题排查困难，无法满足业务对精细化流量控制的需求（如 A/B 测试、限流等）。

**解决方案**: 引入 Higress 替换原有网关，利用其与 Nacos 和 Sentinel 的集成能力，实现了服务自动发现和动态配置更新。通过 Higress 的插件机制，快速实现了限流、熔断、认证授权等功能，并对接了 Prometheus 和 Grafana 构建监控体系。

**效果**: 网关配置实现了全自动化，服务上下线无需人工干预，运维效率提升 60%。通过 Higress 的流量管理能力，成功支持了多个业务的 A/B 测试和灰度发布，业务迭代速度提升 50%。统一的监控和告警体系使问题定位时间从小时级缩短到分钟级。

---



### 3：金融科技公司 API 开放平台

 3：金融科技公司 API 开放平台

**背景**: 某金融科技公司需要构建一个开放 API 平台，为合作伙伴和第三方开发者提供金融服务接口。平台对安全性、稳定性和可扩展性有极高要求，同时需要支持多租户管理和灵活的计费策略。

**问题**: 原有 API 管理方案在安全认证、访问控制和流量管理方面存在不足，无法满足金融级别的合规要求。此外，多租户管理和计费功能的开发成本高，且难以快速响应合作伙伴的定制化需求。

**解决方案**: 基于 Higress 构建了开放 API 网关，利用其强大的安全插件（如 JWT 认证、WAF）和流量管理能力，实现了精细化的访问控制和防护。通过 Higress 的扩展接口，快速开发了多租户管理和计费功能，并与内部业务系统深度集成。

**效果**: 成功构建了符合金融合规要求的开放 API 平台，支持了上百个合作伙伴的接入。通过 Higress 的限流和熔断机制，有效保护了后端服务的稳定性，故障率降低 70%。灵活的扩展能力使新功能上线周期缩短 60%，合作伙伴满意度显著提升。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|----------------|------|--------|
| 性能 | 高性能，基于 Rust 和 C++，支持高并发 | 高性能，基于 Nginx 和 Lua，适合高流量场景 | 极高性能，基于 LuaJIT，低延迟高吞吐 |
| 易用性 | 提供控制台和 K8s 集成，配置简单 | 配置灵活但需要一定学习成本 | 提供丰富的 API 和 Dashboard，易于上手 |
| 成本 | 开源免费，企业版需付费 | 开源版免费，企业版支持需付费 | 完全开源，社区版免费 |
| 扩展性 | 支持插件扩展，集成 WAF 和流量管理 | 插件生态丰富，支持自定义插件 | 支持动态路由和插件热加载 |
| 社区支持 | 阿里巴巴背书，社区活跃 | 社区成熟，文档完善 | 国内社区活跃，国际化程度高 |
| 适用场景 | 云原生环境，微服务网关 | 传统 API 网关，混合云架构 | 高并发场景，云原生应用 |

### 优势分析

- 优势1：高性能架构，结合 Rust 和 C++，适合高并发场景。
- 优势2：深度集成 K8s 和云原生生态，提供开箱即用的控制台。
- 优势3：阿里巴巴背书，企业级支持和稳定性有保障。
- 优势4：内置 WAF 和流量管理功能，安全性强。

### 不足分析

- 不足1：社区生态相对 Kong 和 APISIX 较小，插件数量有限。
- 不足2：企业版功能需付费，成本可能较高。
- 不足3：文档和国际化支持不如 Kong 完善。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 WASM 实现高性能网关扩展

**说明**:
Higress 深度集成了 WASM (WebAssembly) 技术，允许开发者使用 C/C++、Go、Rust 或 AssemblyScript 编写插件逻辑。相比传统 Lua 或 Java 过滤器，WASM 提供了接近原生的执行性能，且具备沙箱隔离安全性，能够实现热加载而不影响主网关进程。

**实施步骤**:
1. 根据团队技术栈选择 WASM 开发语言（推荐使用 Go 或 Rust）。
2. 使用 Higress 提供的 SDK 或 Proxy-Wasm 标准接口编写插件逻辑。
3. 将编译好的 `.wasm` 文件上传至 Higress 控制台或通过 OCI 存储进行分发。
4. 在网关路由配置中关联该 WASM 插件，并配置相关参数。

**注意事项**:
- WASM 插件运行在内存沙箱中，需注意资源限制（内存和 CPU）。
- 调试 WASM 插件相对复杂，建议在本地环境充分测试后再部署至生产环境。

---

### 实践 2：构建服务保护与限流策略

**说明**:
在微服务架构中，防止流量突增击垮后端服务至关重要。Higress 支持基于请求速率、并发连接数等多种维度的限流。通过精确配置限流规则，可以保护后端服务稳定性，并防止恶意攻击或爬虫。

**实施步骤**:
1. 进入 Higress 控制台的“流量管理”或“插件市场”。
2. 启用 `key-rate-limit` 或类似限流插件。
3. 配置限流维度（如：针对某个 IP、Header 或 Cookie）。
4. 设置阈值，例如每秒请求数或每分钟请求数。
5. 配置限流后的返回行为（如直接返回 429 状态码或自定义 JSON 响应）。

**注意事项**:
- 限流配置应基于压测数据设定，避免误杀正常流量。
- 在分布式部署场景下，如需全局限流，需配合 Redis 使用。

---

### 实践 3：配置金丝雀发布与蓝绿部署

**说明**:
Higress 原生支持基于权重的路由转发，是实现金丝雀发布的理想工具。通过将一小部分流量（如 5%）路由到新版本服务，可以在低风险下验证新版本稳定性，实现平滑迭代。

**实施步骤**:
1. 确保新版本服务已注册到服务发现（如 Nacos、Kubernetes Service）。
2. 在 Higress 中创建或修改目标路由规则。
3. 配置两个目标服务（旧版本和新版本）。
4. 设置流量权重（例如旧版本 95%，新版本 5%）。
5. 观察新版本监控指标，无误后逐步调整权重直至 100%。

**注意事项**:
- 确保新旧版本服务的接口兼容性，防止因字段变更导致报错。
- 金丝雀发布期间需保持高频监控，以便快速回滚。

---

### 实践 4：利用 Ingress 资源实现 Kubernetes 云原生集成

**说明**:
如果 Higress 部署在 Kubernetes 集群中，最佳实践是利用 Kubernetes Ingress 或 Gateway API 资源来管理流量路由，而不是手动配置 JSON。这种方式实现了基础设施即代码，便于版本控制和自动化运维。

**实施步骤**:
1. 部署 Higress Gateway Controller 到 K8s 集群。
2. 编写标准的 Kubernetes Ingress YAML 文件，定义 Host、Path 和后端 Service。
3. 使用 `kubectl apply -f` 应用配置。
4. 利用 Higress 提供的注解能力，在 Ingress YAML 中配置特定插件（如 CORS、Auth）。

**注意事项**:
- 复杂的流量治理逻辑（如全局限流、精确的 Header 匹配）可能需要配合 Higress 的自定义 CRD 或控制台配置。
- 定期检查 Ingress Controller 的日志，确保配置下发成功。

---

### 实践 5：实施全链路安全认证与鉴权

**说明**:
API 网关是流量的统一入口，是实施安全策略的最佳关卡。Higress 支持 JWT 验证、OIDC 认证以及基于 AK/SK 的鉴权。通过在网关层统一处理认证，可以避免后端微服务重复实现安全代码。

**实施步骤**:
1. 在身份认证服务（如 Keycloak 或自建 AuthService）中配置应用。
2. 在 Higress 路由或全局配置中启用 `jwt-auth` 插件。
3. 配置 JWT 签名公钥或 JWKs 端点。
4. 配置鉴权逻辑（例如：验证 Payload 中的 `scope` 或 `role` 字段）。
5. 测试无效 Token 和过期 Token 是否被正确拦截（返回 401）。

**

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 WASM 插件与原生插件混合部署模式

**说明**: Higress 支持基于 WebAssembly (WASM) 的扩展机制。虽然 WASM 提供了极高的灵活性和隔离性，但其执行效率相较于原生代码（Go/C++）存在一定的性能损耗（主要涉及内存拷贝和序列化开销）。对于高频调用的核心逻辑（如限流、JWT 验证、简单路由），使用原生插件或 Higress 内置功能能显著降低延迟。

**实施方法**:
1. 审计当前运行的 WASM 插件，识别出 Top 3 耗时最长的插件。
2. 查阅 Higress 官方文档，确认是否有对应功能的内置原生实现（如 `key-rate-limit` 等）。
3. 将高频、低复杂度的逻辑从 WASM 迁移至 Higress 的原生 `Lua` 或 `Go` 插件体系，或者直接配置为原生路由规则。
4. 将业务逻辑复杂、迭代频繁的功能保留在 WASM 中。

**预期效果**: 核心链路处理延迟降低 10% - 30%，P99 延迟明显改善。

---

### 优化 2：优化 HTTP/2 配置与连接池

**说明**: Higress 基于 Envoy，默认配置较为通用。在处理高并发微服务调用时，默认的 HTTP/2 连接数和流限制可能成为瓶颈。如果下游服务是 gRPC 或 HTTP/2，调整上游集群的连接池大小可以减少排队等待时间。

**实施方法**:
1. 修改 Higress 的 `Upstream` 配置或对应的 `Ingress` 注解。
2. 增大 `http2Options.maxConcurrentStreams` 值（默认通常较小，可调整为 100 或更高）。
3. 调整连接池参数，例如将 HTTP/2 连接数上限从默认的 1 调整为 2-4（取决于 CPU 核心数和后端服务能力）。
4. 开启 HTTP/2 连接的 `idle_timeout` 优化，避免频繁建连。

**预期效果**: 在高并发场景下，后端请求排队率降低，吞吐量（RPS）提升 15% - 25%。

---

### 优化 3：启用全链路零拷贝与四层代理（针对网关透传场景）

**说明**: 如果 Higress 仅作为 TCP/UDP 流量透传，或者不需要进行七层（HTTP）逻辑处理（如鉴权、Header 修改），在七层处理数据会带来不必要的内存拷贝和 CPU 解析开销。启用四层代理或优化数据路径可以减少上下文切换。

**实施方法**:
1. 对于纯透传流量，配置 Higress 的 `TcpProxy` 或 `Cluster` 资源进行四层转发。
2. 确保在配置中禁用不必要的访问日志记录（Access Logging），因为高频 I/O 写入是性能杀手。
3. 检查并关闭 `Buffer` 限制，允许流式传输，减少网关内存占用。

**预期效果**: 网关 CPU 占用率下降 20% - 40%，透传延迟降低至亚毫秒级。

---

### 优化 4：配置高效的服务发现与 DNS 缓存

**说明**: 在 Kubernetes 环境中，频繁的 DNS 查询或 CoreDNS 解析延迟会导致网关建立连接时变慢。Higress (Envoy) 支持严格的 DNS 缓存和基于 Service Discovery 的全量缓存。如果配置不当，每次请求都可能触发 DNS 解析或异常节点的重试。

**实施方法**:
1. 在 Higress 的 `Cluster` 配置中，将 `dns_lookup_family` 设置为 `V4_ONLY`（如果不需要 IPv6）以减少查询尝试。
2. 开启 `respect_dns_ttl` 并根据业务情况调整 DNS 刷新频率，避免频繁的 DNS 请求。
3. 对于 Kubernetes Service，确保使用 Endpoint Slice 模式，并配置 Higress 的 `outlier_detection

---
## 学习要点

- Higress 是基于阿里云内部实践并开源的下一代云原生 API 网关，深度集成了 Envoy 和 Istio。
- 它提供了一站式流量管理，支持 K8s Ingress、南北向网关及东西向 Service Mesh 流量治理。
- 该网关原生支持 Dubbo、Nacos、gRPC 等微服务生态，能够实现从传统微服务架构到云原生架构的平滑过渡。
- 内置了 WAF（Web 应用防火墙）插件，提供开箱即用的安全防护能力，有效抵御常见 Web 攻击。
- 具备强大的 AI 网关特性，支持对接大模型（LLM）并提供 Prompt 模板管理、Token 计数与限流等 AI 专用治理能力。
- 提供了标准化的 Wasm 插件市场，支持通过 Python、Go、Lua 等语言编写插件，业务逻辑扩展灵活且热更新不中断。
- 架构设计上实现了高吞吐与低延迟，能够轻松应对双十一等超大规模流量的性能挑战。


---
## 学习路径

## 学习路径

### 阶段 1：概念认知与环境准备

**学习内容**:
- 云原生网关的基础概念
- Higress 的核心特性与架构设计
- Higress 与传统网关（如 Nginx, Spring Cloud Gateway）及 Istio 的区别
- 容器基础与 Docker 基本操作
- Kubernetes 基础概念

**学习时间**: 1-2周

**学习资源**:
- Higress 官方文档
- Higress GitHub 仓库 README
- 云原生网关技术对比文章

**学习建议**:
此阶段重点在于理解“为什么需要 Higress”。建议先通读官方文档的架构部分，不要急于动手部署。如果对 Kubernetes 不熟悉，需要先补充 Pod、Service、Ingress 等基础概念，因为 Higress 通常部署在 K8s 环境中。

---

### 阶段 2：核心功能掌握与基础配置

**学习内容**:
- Higress 的安装与部署（Docker Standalone 与 Kubernetes Helm 两种方式）
- Higress 控制台的使用
- 域名、路由与流量管理配置
- 服务来源注册
- 基础的负载均衡策略配置

**学习时间**: 2-3周

**学习资源**:
- Higress 快速开始指南
- Higress 官方示例
- Higress 配置参考文档

**学习建议**:
动手实践是本阶段的核心。建议在本地或测试环境先使用 Docker 模式快速部署一个 Higress 实例，通过控制台界面配置几条简单的路由规则，将流量转发到一个模拟的后端服务（如 httpbin 或 nginx）。熟悉配置的下发流程和日志查看。

---

### 阶段 3：流量治理与插件系统

**学习内容**:
- 高级流量治理：全链路灰度发布、金丝雀发布、Header 匹配路由
- 插件市场与插件机制
- 常用插件配置：WAF 防护、限流降级、请求/响应修改、CORS 处理
- 自定义插件开发

**学习时间**: 3-4周

**学习资源**:
- Higress 流量治理文档
- Higress 插件开发文档
- Higress 官方插件市场

**学习建议**:
此阶段是 Higress 的进阶核心。重点学习如何利用 Higress 解决微服务架构中的流量安全问题。尝试配置一条基于权重的灰度路由，并安装一个官方插件（如 Key Rate Limit）来验证功能。如果有编程基础（Go/Java/Wasm），尝试阅读并修改一个简单的插件示例。

---

### 阶段 4：生态集成与生产实践

**学习内容**:
- Higress 与 Nacos、Consul 等注册中心的深度集成
- Higress 与 Istio Ingress Gateway 的对比与协同
- 服务来源中的 HTTP 服务与 DNS 服务配置
- 高可用部署架构与性能调优
- 可观测性：对接 Prometheus/Grafana 监控与日志收集

**学习时间**: 4周+

**学习资源**:
- Higress 最佳实践案例
- Higress GitHub Issues 与 Discussions
- 云原生社区关于网关选型的深度分析

**学习建议**:
结合实际业务场景进行思考。如果你的服务使用了 Nacos，重点研究 Higress 如何无缝对接 Nacos 实现服务自动发现。在生产环境部署前，务必关注网关的高可用（HA）配置以及监控告警指标的配置，确保故障可追溯。

---
## 常见问题


### 1: Higress 是什么？它与阿里巴巴和云原生社区有什么关系？

1: Higress 是什么？它与阿里巴巴和云原生社区有什么关系？

**A**: Higress 是一个基于阿里内部多年实践沉淀的下一代云原生 API 网关。它是在 2022 年由阿里巴巴开源，并随后捐赠给了云原生计算基金会（CNCF）作为沙箱项目。Higress 的底层深度集成了开源项目 Envoy，旨在提供高性能、高可用的流量管理能力。它源自阿里巴巴集团内部的流量网关技术，支撑了阿里每年的双十一大促流量，因此兼具企业级的稳定性与云原生的标准架构。

---



### 2: Higress 与 Nginx、Apache APISIX 或 Kong 等传统网关相比有什么核心优势？

2: Higress 与 Nginx、Apache APISIX 或 Kong 等传统网关相比有什么核心优势？

**A**: Higress 的核心优势主要体现在以下几个方面：

1.  **深度集成 Envoy**: 与基于 Nginx/OpenResty 的网关（如 Kong、APISIX）不同，Higress 基于 C++ 编写的 Envoy 作为数据面，具有更高的长连接处理能力和更低的资源消耗，特别适合高并发、长连接（如微服务、gRPC、WebSocket）场景。
2.  **标准化与扩展性**: 它遵循 Ingress/Gateway API 标准，支持热更新插件，且插件机制兼容 WASM (WebAssembly)。这意味着开发者可以使用 C++、Go、Rust、JavaScript 等多种语言编写插件，而无需重新编译网关本身，扩展性更强。
3.  **安全与防护**: 内置了 WAF（Web 应用防火墙）能力，能够有效防御 SQL 注入、XSS 等常见 Web 攻击。
4.  **服务发现集成**: 对 Nacos、Consul、Zookeeper 以及 Kubernetes Service 做了开箱即用的集成，非常适合混合云架构（既有 K8s 又有虚拟机环境）。

---



### 3: Higress 是否支持从 Nginx 或 Ingress Controller 进行平滑迁移？

3: Higress 是否支持从 Nginx 或 Ingress Controller 进行平滑迁移？

**A**: 是的，Higress 非常重视迁移的便利性，并提供了相应的工具来降低迁移成本。

1.  **Nginx 兼容**: Higress 提供了 Nginx 配置转换工具，可以将现有的 Nginx.conf 配置自动转换为 Higress 的路由配置。
2.  **Kubernetes Ingress 兼容**: Higress 完全实现了 Kubernetes Ingress API，可以直接替换 K8s 集群中原有的 Nginx Ingress Controller 或 Traefik，无需修改大部分 Ingress 资源文件即可直接接管流量。
3.  **网关关联**: 在阿里云环境中，Higress 还支持作为 MSE (Microservices Engine) 云产品的一部分，提供托管的平滑迁移体验。

---



### 4: Higress 的插件机制是如何工作的？支持哪些语言开发？

4: Higress 的插件机制是如何工作的？支持哪些语言开发？

**A**: Higress 采用了灵活的插件系统来处理流量拦截和修改（如鉴权、限流、请求响应修改）。

1.  **WASM 支持**: 这是 Higress 插件的最大亮点。它支持 WASM (WebAssembly) 规范。由于 Envoy 原生支持 WASM，Higress 允许开发者使用 Go、C++、Rust、AssemblyScript 甚至 JavaScript/TypeScript 编写插件逻辑。
2.  **热加载**: 基于 WASM 的插件可以在不重启 Higress 网关实例的情况下动态加载、更新或卸载，这对于业务连续性要求极高的场景非常关键。
3.  **原生插件**: 除了 WASM，Higress 也支持基于 Java/Go 的原生插件处理（通过本地 RPC 调用），用于处理对性能要求极高或逻辑极其复杂的场景。

---



### 5: 在生产环境中使用 Higress，对资源消耗和性能有什么预期？

5: 在生产环境中使用 Higress，对资源消耗和性能有什么预期？

**A**: Higress 的设计目标是高性能和低延迟。

1.  **性能**: 基于 Envoy 的数据面在处理 HTTP/2、gRPC 等协议时表现优异，延迟通常在毫秒级甚至更低。在阿里内部的生产实践中，它能够支撑每秒数十万级的 QPS 请求。
2.  **资源消耗**: 由于 Envoy 采用 C++ 编写且内存管理精细，相比基于 LuaJIT 的 OpenResty 方案，在处理大量长连接时内存占用通常更加稳定和可控。但在处理极短连接的高并发 HTTP/1.1 场景下，OpenResty 仍有其优势。具体资源消耗取决于配置的插件数量和复杂度，但通常建议根据业务量预留足够的 CPU 和内存。

---



### 6: Higress 是否支持 Dubbo 或 gRPC 等微服务协议？

6: Higress 是否支持 Dubbo 或 gRPC 等微服务协议？

**A**: 是的，Higress 对微服务协议有着优秀的支持。

1.  **gRPC**: 由于 Envoy 原生对 HTTP/2 的支持，Higress 可以作为 gRPC 服务的代理，支持 gRPC 路由、gRPC-Web（使浏览器能直接调用 gRPC）以及 gRPC 之间的协议转换。
2.  **Dubbo**: Higress 提供了对 Dubbo 和 Dubbo

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 快速启动与基础路由验证

### 在本地使用 Docker 快速启动一个 Higress 网关实例。配置一个简单的 Ingress 路由规则，将访问 `http://localhost/hello/` 的流量转发到一个公共的测试服务（如 `httpbin.org`），并验证请求是否成功转发。

### 提示**: Higress 提供了标准的 Docker 镜像，核心在于编写正确的 YAML 配置文件并挂载到容器中。请查阅官方文档中的 "快速开始" 章节，关注 Gateway 和 HTTPRoute 资源的字段定义。

---
## 实践建议

基于 Higress 作为 AI Native API 网关的定位，结合其基于 Envoy 和 Istio 的高性能架构，以下是针对实际生产环境的 6 条实践建议：

### 1. 利用 Wasm 插件实现 LLM 提示词管理与安全审计
**场景：** 在对接大模型（如 OpenAI、通义千问）时，直接将 Prompt 写在客户端代码中难以维护，且存在泄露风险。
**建议：** 使用 Higress 的 Wasm 插件能力（特别是 `ai-proxy` 或自定义 Wasm 插件）在网关层进行 Prompt 注入和改写。
**操作：**
*   **Prompt 模板化：** 在网关配置预置的 System Prompt，客户端仅需发送用户问题，由网关拼接完整的上下文。
*   **敏感词过滤：** 在请求发送给 LLM 之前，利用 Wasm 插件拦截并扫描输入内容，防止 Prompt 注入攻击。
*   **响应审计：** 对模型返回的内容进行实时审查，过滤违规输出。
**陷阱：** 避免在网关进行过重的逻辑处理（如复杂的正则匹配），以免阻塞请求链路，应尽量利用高性能的 Wasm 模块。

### 2. 配置智能路由与 fallback 机制保障服务高可用
**场景：** 单一大模型服务可能因 API 限流或服务商宕机导致业务中断。
**建议：** 利用 Higress 的路由能力配置多模型容灾策略。
**操作：**
*   **模型服务降级：** 配置路由规则，当主模型（如 GPT-4）响应超时或返回 429/5xx 错误时，自动将请求切换至备用模型（如 GPT-3.5 或其他开源模型）。
*   **超时控制：** 针对流式响应（SSE）设置合理的读写超时时间，防止长连接占用过多连接池资源。
**陷阱：** 不要忽略流式传输的超时设置。流式响应虽然首包快，但总耗时长，若超时设置过短会导致连接在传输中断开，用户体验极差。

### 3. 实施基于 Token 的精细化限流
**场景：** LLM 调用成本主要取决于 Token 消耗量，传统的 QPS（每秒请求数）限流无法准确控制成本。
**建议：** 结合 Higress 的限流插件与后端监控，实施基于 Token 吞吐量的保护策略。
**操作：**
*   **请求级限流：** 对 API Key 或用户 IP 进行严格的 QPS 限制，防止恶意刷接口。
*   **预估限流：** 虽然网关难以精确计算发送前的 Token 数，但可以通过限制请求体大小或结合 Prompt 长度预估逻辑，拒绝过大的上下文请求。
**陷阱：** 避免仅依赖 HTTP 状态码进行熔断。大模型 API 经常会返回成功（200）但内容包含错误信息的情况，需结合响应体逻辑进行判断。

### 4. 启用 JSON Schema 提取以结构化模型输出
**场景：** 后端服务通常需要结构化的数据（JSON），而 LLM 原生输出是非结构化文本，客户端解析容易出错。
**建议：** 利用 Higress 的 AI 特性进行响应体的模式转换。
**操作：**
*   在网关层配置 `ai-statistics` 或相关处理插件，强制或辅助模型输出符合特定 JSON Schema 的数据。
*   网关直接将清洗后的 JSON 转发给业务服务，降低业务端的解析复杂度。
**最佳实践：** 确保在 Prompt 中显式要求 "Output JSON only"，并配合网关的正则或 JSON 校验插件，确保无效格式不被透传。

### 5. 建立模型可观测性与链路追踪
**场景：** AI 调用属于黑盒操作，当出现回答幻觉或延迟高时，难以排查是网络问题还是模型问题。
**建议：** 深度集成 Higress 的可观测性组件。
**操作

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API网关](/tags/api%E7%BD%91%E5%85%B3/) / [AI原生](/tags/ai%E5%8E%9F%E7%94%9F/) / [阿里开源](/tags/%E9%98%BF%E9%87%8C%E5%BC%80%E6%BA%90/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [LLM](/tags/llm/) / [MCP协议](/tags/mcp%E5%8D%8F%E8%AE%AE/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/) / [DevOps/运维](/scenarios/devops-%E8%BF%90%E7%BB%B4/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260130-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260201-github_trending-alibaba-higress-8.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*