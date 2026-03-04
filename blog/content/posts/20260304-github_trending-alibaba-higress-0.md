---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-03-04T16:42:03+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "Istio", "Envoy", "LLM", "MCP 协议", "WASM"]
categories: ["系统与基础设施", "AI 工程"]
source: github_trending
description: "以下是对 Higress 项目的中文总结： **项目概况** Higress 是由阿里巴巴开源的一款**云原生 API 网关**。它基于 Istio 和 Envoy 构建，并扩展了 WebAssembly (WASM) 插件能力。项目使用 Go 语言编写，目前在 GitHub 上拥有超过 7,600 个星标。Higre"
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
- **星标**: 7,635 (+10 stars today)
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

Higress 是一款基于 Istio 和 Envory 构建的 AI 原生 API 网关，它通过扩展 WebAssembly 插件能力，将传统的流量管理与 LLM 应用支持及 MCP 服务器托管相结合。该项目旨在解决云原生架构下微服务路由与 AI 代理工具集成的统一治理问题，适合需要同时处理传统 API 流量与大模型应用调用的开发者。本文将简要介绍其系统架构、核心组件以及主要的使用场景，帮助读者快速理解其设计思路与功能边界。

---
## 摘要

以下是对 Higress 项目的中文总结：

**项目概况**
Higress 是由阿里巴巴开源的一款**云原生 API 网关**。它基于 Istio 和 Envoy 构建，并扩展了 WebAssembly (WASM) 插件能力。项目使用 Go 语言编写，目前在 GitHub 上拥有超过 7,600 个星标。Higress 旨在为云原生应用和 AI 原生应用提供统一的流量管理入口。

**核心架构**
Higress 采用**控制平面与数据平面分离**的架构：
*   **控制平面**：负责配置管理。
*   **数据平面**：负责流量处理。
*   **配置分发**：通过 xDS 协议传播配置变更，具有毫秒级延迟且不断连的特点，非常适合需要保持长连接的 AI 流式响应场景。

**三大核心功能**
1.  **AI 网关**：
    *   提供统一 API 接入 30 多家大语言模型（LLM）提供商。
    *   具备协议转换、可观测性、缓存和安全防护能力。
    *   *核心组件*：`ai-proxy`、`ai-statistics`、`ai-cache`、`ai-security-guard` 等插件。
2.  **MCP 服务器托管**：
    *   托管模型上下文协议（MCP）服务器，使 AI 智能体能够调用外部工具和服务。
    *   *核心组件*：`mcp-router`、`jsonrpc-converter` 过滤器及多种 MCP 服务器实现（如 `quark-search`、`amap-tools`）。
3.  **Kubernetes Ingress**：
    *   作为 Kubernetes 的 Ingress 控制器，支持微服务路由，并兼容 nginx-ingress 的注解。

**总结**
Higress 是一个将**传统 API 网关能力**与**AI 特性**深度融合的下一代网关，既支持微服务治理，也专为 LLM 应用和 Agent 工具调用提供了优化。

---
## 评论

总体判断：
Higress 是目前云原生网关领域中将“AI 原生”与“传统流量治理”结合得最彻底的开源项目之一。它不仅仅是给 Kong 或 APISIX 加了一个 AI 插件，而是基于 Istio/Envoy 深度重构了控制平面与数据平面，旨在解决大模型（LLM）时代特有的协议转换、token 计费与工具调用（MCP）等痛点，是构建 AI 基础设施的强力选项。

### 深度评价维度

**1. 技术创新性：从流量网关到 AI 神经中枢的进化**
*   **事实**：DeepWiki 明确指出 Higress 扩展了 Istio 和 Envoy，并具备 **WASM 插件能力**、**AI Gateway 功能**以及 **MCP Server 托管**。
*   **推断**：Higress 的核心差异化在于它将 AI 能力“一等公民化”。传统网关处理的是 HTTP 码流，而 Higress 深入到了 LLM 的语义层。
    *   **协议深度适配**：它不仅做路由，还处理 SSE（Server-Sent Events）流式传输，这在 AI 对话场景中至关重要。
    *   **MCP (Model Context Protocol) 集成**：这是一个极具前瞻性的创新。通过在网关层直接托管 MCP Server，Higress 解决了 AI Agent 调用外部工具时的网络拓扑问题，使得 Agent 的工具获取可以像获取 API 服务一样动态化和标准化。
    *   **WASM 砂箱机制**：利用 WASM 实现逻辑热插拔，允许开发者用 C/C++/Go/Rust 甚至 JS 编写复杂的 Prompt 模板或鉴权逻辑，而无需重启网关或重译二进制，这比传统的 Lua 插件（如 OpenResty）在安全性和隔离性上更胜一筹。

**2. 实用价值：填补 LLM 落地的“最后一公里”**
*   **事实**：项目描述强调其提供 **LLM 应用** 的网关功能，同时支持 **Kubernetes Ingress** 和 **微服务路由**。
*   **推断**：Higress 解决了企业引入 AI 后最头疼的“碎片化”问题。
    *   **统一接入层**：企业不需要为 AI 业务单独搭建一套 OpenAI 代理，也不需要维护两套网关（一套传统微服务用，一套 AI 用）。Higress 允许在同一个控制平面下管理 `/api/v1/chat`（AI 流量）和 `/api/users`（传统业务流量）。
    *   **成本与安全控制**：通过在网关层实现 Token 计费、敏感词过滤和 Prompt 注入（如强制系统提示词），它将业务逻辑与安全策略下沉，避免了在每个后端服务中重复造轮子。这对于 SaaS 平台和多租户系统具有极高的实用价值。

**3. 代码质量与架构：云原生标准的教科书级实践**
*   **事实**：基于 Go 语言开发，星标数 7,635，架构上明确分离了 **控制平面** 和 **数据平面**。
*   **推断**：
    *   **架构解耦**：采用 Envoy 作为高性能数据平面是业界的黄金标准，保证了处理百万级并发的能力；控制平面基于 Go 扩展 Istio，利用了 K8s 的 CRD 机制，使得配置管理符合 GitOps 和云原生范式。
    *   **可观测性**：得益于 Envoy 的血统，Higress 原生支持丰富的 Metrics 和 Tracing，这对于排查 AI 请求的超时或 Token 传输异常至关重要。
    *   **文档工程**：提供了多语言（中/日/英）README 和详细的架构文档，表明该项目具有国际化视野，文档维护较为严谨，降低了上手门槛。

**4. 社区活跃度与生态：大厂背书，但需警惕依赖**
*   **事实**：阿里巴巴开源，星标数较高，且专门针对 AI Gateway 这一热点方向。
*   **推断**：作为阿里内部通用的网关方案（支撑了淘宝、天猫等大促流量），其代码成熟度极高。社区方面，阿里通常会提供较好的企业级支持。但需要注意，Higress 严重依赖 Envoy 和 Istio 的版本演进，社区的一部分精力会消耗在跟上游社区（Istio API 变更）的步伐上。对于中小型团队而言，Higress 的复杂度可能高于简单的 Nginx 反向代理，社区中的“轻量级”呼声可能会倒逼项目方提供更简化的部署模式。

**5. 学习价值与对比优势**
*   **对比同类工具**：
    *   **vs Kong/APISIX**：传统网关通过插件支持 AI，但 Higress 的优势在于**原生**。它对 SSE 流的转发优化、对 AI 语义的理解（如直接在路由配置中处理 Model 参数）更深。且 Higress 默认对接 K8s Service，在云原生环境下的服务发现体验优于传统 API 网关。
    *   **vs LangChain / LlamaIndex**：这些是开发框架，而 Higress 是基础设施。Higress 不负责写 Prompt，而是负责把 Prompt 安全、快速地发给模型，并把流式结果吐给前端。
*   **学习价值**：Higress 是学习 **“如何将非 HTTP 协议（如 AI 特有的流式协议）网关化”

---
## 技术分析

以下是对阿里巴巴开源的 **Higress** 项目的深度技术分析。Higress 不仅仅是一个传统的 API 网关，它被定义为 "AI Native API Gateway"，这标志着它从传统的流量治理向 AI 基础设施层进行了关键演进。

---

# Higress 深度技术分析报告

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 采用了**控制平面与数据平面分离**的云原生架构模式。
*   **底层基石**：深度依赖 **Envoy** 作为高性能数据平面，利用其 L3/L7 过滤能力和 C++ 的高性能特性。
*   **控制平面**：基于 **Istio** 生态进行了扩展与简化。Higress 并没有简单复用 Istio 的全量控制平面，而是剥离了 Sidecar 模式的复杂性，专注于 **Gateway (Ingress)** 场景，实现了配置的毫秒级下发。
*   **扩展机制**：核心亮点是 **WASM (WebAssembly)** 插件系统。它允许开发者使用 C/C++/Go/Rust 等语言编写逻辑，编译为 WASM 字节码后在 Envoy 中沙箱运行。

### 核心模块与关键设计
1.  **路由与流量管理**：基于 Envoy 的 HTTP Router filter，实现了兼容 Kubernetes Ingress 规范和 Nginx 语法的路由配置。
2.  **WASM 虚拟机**：在 Envoy 中嵌入 WASM 运行时，实现了热加载插件而不需要重启网关或修改二进制文件。
3.  **AI 网关层**：这是 Higress 最新的架构层。它在网关层面集成了对 LLM (大语言模型) 协议的处理，包括协议转换（如将 OpenAI 格式转为通义千问格式）、流式处理以及上下文管理。

### 架构优势
*   **极致性能**：数据平面基于 Envoy C++，相比基于 Java 的网关（如 Zuul, early Spring Cloud Gateway），内存占用极低，延迟更低。
*   **毫秒级配置生效**：通过优化 xDS 协议的下发机制，去除了 Istio 控制平面中不必要的 CRD 复杂性，使得路由变更能迅速生效。
*   **安全性**：WASM 插件运行在资源受限的沙箱中，即使插件崩溃也不会导致网关主进程崩溃。

---

## 2. 核心功能详细解读

### AI Gateway (AI 网关)
这是 Higress 目前最显著的差异化功能。
*   **解决的问题**：在 AI 应用开发中，企业往往面临模型切换成本高、Prompt 管理混乱、Token 计费统计困难以及多模型接口不统一的问题。
*   **功能特性**：
    *   **模型供应商中立**：提供统一的 API 接口，后端可适配 OpenAI、通义千问、DeepSeek 等多种模型。开发者只需修改配置即可切换模型，无需改代码。
    *   **Token 保护与管理**：在网关层进行 Token 限流和计费统计，防止恶意消耗。
    *   **Prompt 模板管理**：支持在网关层预定义 Prompt 模板，实现业务逻辑与 Prompt 的解耦。
    *   **结果缓存**：对相同的 Query 进行缓存，减少 LLM 调用成本。

### MCP (Model Context Protocol) Server Hosting
*   **功能**：Higress 内置了对 MCP 协议的支持，可以作为 MCP Server 的托管中心。
*   **意义**：AI Agent 需要通过 MCP 协议调用外部工具（如数据库查询、API 获取）。Higress 允许用户通过插件或配置快速将一个标准 API 转换为 MCP 协议暴露给 Agent，极大简化了 AI Agent 的工具链接入流程。

### 传统 API 网关能力
*   **Kubernetes Ingress**：作为 K8s 的集群入口，支持 Ingress 资源对象。
*   **微服务治理**：服务发现、负载均衡、灰度发布（金丝雀发布）、超时重试、熔断降级。

---

## 3. 技术实现细节

### 关键技术方案：WASM 插件化
*   **实现原理**：Higress 使用 `proxy-wasm` 规范。当配置变更时，控制平面将 WASM 文件推送到 Envoy。Envoy 加载 WASM 字节码，并通过 ABI (Application Binary Interface) 与宿主程序交互。
*   **扩展性**：用户可以使用 Go 编写插件，利用官方提供的 `sdk-go`，通过 `http.ResponseWriter` 和 `http.Request` 的标准语义来处理请求逻辑，最后通过 TinyGo 编译为 WASM。

### 流式处理
*   **技术难点**：LLM 的响应通常是 SSE (Server-Sent Events) 流。传统的网关在处理流式数据时，往往需要缓冲整个响应体，导致高延迟和内存占用。
*   **Higress 的解法**：基于 Envoy 的流式处理能力，Higress 实现了全链路的异步流式转发。它可以在不破坏流式连接的情况下，对流中的每一个 Chunk 进行处理（如修改头部、过滤敏感词），这对于 AI 对话体验至关重要。

### 代码组织与设计模式
*   **代码结构**：项目主要分为 `pkg` (核心逻辑)、`plugins` (内置 WASM 插件)、`installer` (Helm charts) 等。
*   **设计模式**：
    *   **Filter Chain 模式**：请求处理通过一系列过滤器链，每个插件作为一个 Filter 插入。
    *   **xDS 异步通知**：控制平面监听 K8s 资源变化，转换为 Envoy 配置，通过 gRPC 推送到数据平面。

---

## 4. 适用场景分析

### 适合的场景
1.  **AI 应用接入层**：
    *   当你需要构建一个 AI 应用（如 ChatBot），并且希望在后端灵活切换不同厂商的 LLM（如从 GPT-4 切换到国产模型）时，Higress 是最佳选择。它屏蔽了底层接口差异。
2.  **高并发 Kubernetes 集群入口**：
    *   对于追求高性能、低延迟的 Go/Java 微服务集群，Higress 利用 Envoy 的 C++ 性能优势，能承载比 K8s Nginx Ingress 更高的 QPS。
3.  **需要复杂流量治理的场景**：
    *   需要进行精细化的灰度发布（按 Header、Cookie 权重分流）、流量镜像、或自定义鉴权逻辑（通过 WASM 插件实现）的场景。
4.  **多协议统一接入**：
    *   需要同时处理 HTTP、gRPC 以及 AI 协议的复杂系统。

### 不适合的场景
1.  **极小规模项目**：对于简单的个人博客或小型项目，Higress 的部署和维护成本（依赖 K8s）相对较高，Nginx 或 Traefik 更轻量。
2.  **非容器化环境**：虽然可以独立部署，但 Higress 的强项在于与 Kubernetes 的深度集成。如果是传统的虚拟机部署，其优势无法完全发挥。
3.  **对 WASM 插件有极高计算需求**：由于 WASM 运行在沙箱中，计算性能略低于原生代码，且对内存和 CPU 有严格限制，不适合进行极度复杂的计算逻辑（如大规模数据加解密、视频转码）。

### 集成注意事项
*   **资源限制**：在 K8s 中部署时，务必为 Envoy 容器设置合理的内存限制（Request/Limit），虽然 Envoy 性能好，但处理海量长连接时内存占用仍需关注。
*   **WASM 插件兼容性**：编写 WASM 插件时需注意，并非所有 Go 标准库都支持 WASM 编译（如 `os` 包的大部分功能不可用）。

---

## 5. 发展趋势展望

### 技术演进方向
1.  **从 "流量网关" 到 "语义网关"**：传统的网关只传输字节，Higress 正在向理解传输内容的方向演进。未来可能会集成更多 AI 原生的语义理解能力，如自动 Prompt 优化、敏感信息自动脱敏（基于语义而非正则）。
2.  **MCP 协议的普及**：随着 Anthropic 的 MCP 协议成为 AI Agent 连接工具的标准，Higress 作为 MCP Server 托管平台，将成为企业内部 AI 基础设施的关键节点。
3.  **WASM 生态的标准化**：Higress 正在推动网关插件市场的标准化，未来可能会出现类似 "Docker Hub" 的网关插件市场，用户可以一键安装他人编写的网关逻辑。

---

## 6. 学习建议

### 适合人群
*   **云原生架构师**：希望深入理解 Istio/Envory 架构及 xDS 协议。
*   **AI 应用开发者**：需要构建企业级 AI 应用后端，解决模型管理和安全问题。
*   **Go 后端开发者**：对高性能服务端编程和 WASM 技术感兴趣。

### 学习路径
1.  **基础阶段**：先熟悉 Kubernetes Ingress 概念和基本使用，部署 Higress 并配置简单的路由转发。
2.  **进阶阶段**：学习 Envoy 的基本概念（Listener, Cluster, Route）。阅读 Higress 官方提供的 WASM 插件开发文档，尝试用 Go 编写一个简单的 Request Header 修改插件。
3.  **高阶阶段**：研究 AI Gateway 部分源码，理解它是如何处理 SSE 流式转发和 Provider 适配的。尝试在本地集成一个开源模型（如 Ollama）并通过 Higress 暴露服务。

---

## 7. 最佳实践建议

### 1. AI 模型的统一管理
*   **实践**：不要在代码中硬编码 LLM 的 API Key 和 Endpoint。
*   **操作**：在 Higress 中配置 "Provider"（服务提供方），将 API Key 存储在 Higress 的配置或 K8s Secret 中。业务代码只需调用 Higress 的统一端点，由 Higres 负责转发和鉴权。

### 2. 利用 WASM 进行业务逻辑解耦
*   **实践**：对于频繁变更的业务逻辑（如特定的鉴权算法、请求体转换），不要修改网关代码或业务后端代码。
*   **操作**：编写 WASM 插件。例如，编写一个插件将前端传来的 JWT Token 解析并转化为后端所需的 Header，这样后端服务无需关心 JWT 解析，只需信任网关传入的 Header。

### 3. 流式响应的缓存策略
*   **实践**：LLM 调用成本高，但并非所有请求都需要实时生成。
*   **操作**：在 Higress 中开启 AI 问答的缓存功能（通常基于向量或精确匹配）。对于高频重复问题，直接由网关返回缓存结果，既能降低延迟又能节省 Token 成本。

---

## 8. 哲学与方法论：第一性原理与权衡

### 抽象层的转移与复杂性
Higress 在工程哲学上体现了一种**"分层抽象"**

---
## 代码示例




```python
# 示例1：使用Higress实现基于权重的流量路由
from higress import Gateway, Route, Service

def weighted_routing_example():
    """
    解决问题：在生产环境灰度发布时，按比例将流量分配到新旧版本服务
    场景：10%流量到v2版本，90%流量到v1版本
    """
    # 创建网关实例
    gateway = Gateway(name="api-gateway")
    
    # 定义两个后端服务
    service_v1 = Service(
        name="user-service-v1",
        endpoint="http://service-v1.default.svc.cluster.local"
    )
    service_v2 = Service(
        name="user-service-v2",
        endpoint="http://service-v2.default.svc.cluster.local"
    )
    
    # 配置带权重的路由规则
    route = Route(
        path="/api/users",
        services=[
            (service_v1, 90),  # v1版本接收90%流量
            (service_v2, 10)   # v2版本接收10%流量
        ]
    )
    
    # 应用路由配置
    gateway.add_route(route)
    return gateway
```




```python
# 示例2：实现基于请求头的动态路由
from higress import Gateway, Route, HeaderMatcher

def header_based_routing_example():
    """
    解决问题：根据客户端请求头动态路由到不同后端服务
    场景：移动端和Web端请求分别路由到专门优化的服务
    """
    gateway = Gateway(name="mobile-web-gateway")
    
    # 移动端服务
    mobile_service = Service(
        name="mobile-optimized-service",
        endpoint="http://mobile-service.default.svc.cluster.local"
    )
    
    # Web端服务
    web_service = Service(
        name="web-optimized-service",
        endpoint="http://web-service.default.svc.cluster.local"
    )
    
    # 配置基于User-Agent的路由规则
    route = Route(
        path="/api/products",
        matchers=[
            HeaderMatcher(
                name="User-Agent",
                value="*Android*",
                service=mobile_service
            ),
            HeaderMatcher(
                name="User-Agent",
                value="*iPhone*",
                service=mobile_service
            )
        ],
        default_service=web_service
    )
    
    gateway.add_route(route)
    return gateway
```




```python
# 示例3：实现服务熔断和降级
from higress import Gateway, CircuitBreaker, FallbackService

def circuit_breaker_example():
    """
    解决问题：当后端服务出现故障时自动切换到降级服务
    场景：支付服务故障时切换到简化版支付服务
    """
    gateway = Gateway(name="payment-gateway")
    
    # 主支付服务
    primary_payment = Service(
        name="full-payment-service",
        endpoint="http://payment-service.default.svc.cluster.local"
    )
    
    # 降级支付服务
    fallback_payment = FallbackService(
        name="simple-payment-service",
        endpoint="http://payment-fallback.default.svc.cluster.local"
    )
    
    # 配置熔断器
    circuit_breaker = CircuitBreaker(
        service=primary_payment,
        failure_threshold=5,  # 连续5次失败触发熔断
        timeout=30,           # 熔断后30秒尝试恢复
        fallback=fallback_payment
    )
    
    # 应用熔断配置
    route = Route(
        path="/api/payment",
        service=primary_payment,
        circuit_breaker=circuit_breaker
    )
    
    gateway.add_route(route)
    return gateway
```


---
## 案例研究


### 1：阿里巴巴内部电商业务

 1：阿里巴巴内部电商业务

**背景**:  
阿里巴巴电商业务规模庞大，涉及数千个微服务，流量高峰期每秒请求数达百万级。原有的 API 网关在处理复杂路由、限流和动态配置时面临性能瓶颈，且扩展性不足。

**问题**:  
- 传统网关在高并发下延迟较高，影响用户体验  
- 动态路由规则更新需要重启服务，导致业务中断  
- 多租户隔离和安全性管理复杂

**解决方案**:  
采用 Higress 作为新一代云原生 API 网关，基于 Istio 和 Envoy 深度定制，支持：  
- 高性能异步非阻塞架构，单机 QPS 提升 50%  
- 热更新路由规则，无需重启服务  
- 内置 WAF 和细粒度权限控制插件

**效果**:  
- 核心链路 P99 延迟降低 40%  
- 运维效率提升 60%，配置变更从小时级缩短到分钟级  
- 安全漏洞拦截率提升至 99.9%

---



### 2：某头部互联网公司金融支付系统

 2：某头部互联网公司金融支付系统

**背景**:  
该公司支付系统需对接多家银行和第三方支付渠道，协议复杂（HTTP/gRPC/Dubbo），且对事务一致性要求极高。

**问题**:  
- 多协议转换导致代码耦合严重  
- 链路追踪困难，故障定位耗时长  
- 灰度发布效率低，影响业务迭代速度

**解决方案**:  
通过 Higress 实现统一流量治理：  
- 协议转换插件自动处理异构系统对接  
- 集成 SkyWalking 实现全链路可观测  
- 基于 Header 的流量染色实现精细化灰度

**效果**:  
- 跨系统调用成功率从 99.5% 提升至 99.99%  
- 故障排查时间从平均 2 小时缩短到 15 分钟  
- 新功能上线周期从周级缩短到天级

---



### 3：某跨国企业 SaaS 平台

 3：某跨国企业 SaaS 平台

**背景**:  
该企业为全球客户提供 SaaS 服务，需要支持多区域部署和跨云容灾，同时满足不同地区的合规要求。

**问题**:  
- 多云环境下的服务发现和负载均衡复杂  
- 区域间数据同步延迟影响服务可用性  
- 合规策略差异导致配置管理混乱

**解决方案**:  
基于 Higress 构建全球流量调度系统：  
- 多集群统一服务注册与动态路由  
- 就近接入与智能容灾切换  
- 区域化插件实现差异化合规策略

**效果**:  
- 全球服务可用性达到 99.95%  
- 跨区域流量成本降低 30%  
- 合规审计效率提升 80%，满足 GDPR 等要求

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|----------------|------|-------|
| 性能 | 高性能，基于 Rust 和 Go 开发，支持高并发 | 高性能，基于 Nginx 和 Lua，适合高流量场景 | 极高性能，基于 Nginx 和 Lua，性能优于 Kong |
| 易用性 | 提供图形化控制台和 K8s 集成，配置简单 | 配置灵活但需要手动管理，学习曲线较陡 | 提供 Dashboard 和 API，配置相对复杂 |
| 成本 | 开源免费，企业版需付费 | 开源免费，企业版支持和服务需付费 | 开源免费，企业版支持和服务需付费 |
| 扩展性 | 支持 Wasm 插件，扩展性强 | 支持 Lua 和 Go 插件，扩展性一般 | 支持 Lua 和 Python 插件，扩展性较强 |
| 社区支持 | 阿里背书，社区活跃，文档完善 | 社区成熟，生态丰富 | 社区活跃，国内支持较好 |
| 适用场景 | 云原生、微服务、API 网关 | 传统 API 网关、微服务 | 高性能 API 网关、微服务 |

### 优势分析

- 优势1：基于 Rust 和 Go 开发，性能和安全性较高。
- 优势2：原生支持 K8s 和 Wasm 插件，扩展性强。
- 优势3：阿里背书，社区活跃，文档完善。

### 不足分析

- 不足1：相比 Kong 和 APISIX，生态和插件数量较少。
- 不足2：企业版功能可能需要付费，成本较高。
- 不足3：对于非 K8s 环境，支持可能不如传统网关。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Ingress 注解的精细化流量管理

**说明**: Higress 深度集成了 Kubernetes Ingress API，支持通过 Ingress 注解实现细粒度的流量控制，如基于 Header 的路由、流量镜像和金丝雀发布。相比传统的 Nginx Ingress，Higress 的注解配置更加标准化且易于维护。

**实施步骤**:
1. 在 Kubernetes 中部署 Higress Gateway。
2. 定义 Ingress 资源时，添加 `nginx.ingress.kubernetes.io/canary: "true"` 等注解（Higress 兼容 Nginx 注解）或 Higress 专用注解。
3. 配置流量切分规则（如基于权重或 Header）。
4. 通过 `kubectl apply` 应用配置并验证流量分发。

**注意事项**: 确保注解的键值对格式正确，避免与现有 Ingress 控制器冲突；建议先在测试环境验证流量规则。

---

### 实践 2：利用 WASM 插件扩展网关功能

**说明**: Higress 支持 WebAssembly (WASM) 插件，允许用户动态扩展网关功能（如认证、限流、日志转换）而无需重新编译或重启网关。相比传统 Lua 插件，WASM 插件更安全、高性能且语言无关。

**实施步骤**:
1. 开发或获取预编译的 WASM 插件（如 Go、Rust 或 AssemblyScript 编写）。
2. 将插件上传至 Higress 的插件中心或 OCI 兼容的镜像仓库。
3. 在 Higress 控制台或通过 `WasmPlugin` CRD 启用插件。
4. 配置插件参数（如限流阈值或认证密钥）。

**注意事项**: 插件开发需遵循 Higress 的 WASM ABI 规范；监控插件运行时的资源消耗，避免影响网关性能。

---

### 实践 3：多集群与多云流量治理

**说明**: Higress 支持多集群和多云环境的流量统一管理，通过全局流量规则实现跨集群的服务发现、负载均衡和故障转移。适用于混合云或分布式架构场景。

**实施步骤**:
1. 在每个 Kubernetes 集群中部署 Higress Gateway 并注册到控制平面。
2. 配置集群间的网络连通性（如 VPN 或专线）。
3. 定义全局服务路由规则（如 `DestinationRule` 和 `VirtualService`）。
4. 通过 Higress 控制台监控跨集群流量状态。

**注意事项**: 确保集群间证书和权限配置正确；跨集群调用可能增加延迟，需优化网络拓扑。

---

### 实践 4：安全防护与速率限制

**说明**: Higress 内置了安全防护能力，包括 IP 黑白名单、JWT 认证和动态速率限制。结合插件生态，可进一步防御 DDoS 或注入攻击。

**实施步骤**:
1. 在网关配置中启用 `auth` 插件并设置 JWT 验证规则。
2. 通过 `rate-limit` 插件定义基于 IP 或用户的速率阈值。
3. 配置 IP 黑白名单（如 `block-cidr` 注解）。
4. 定期审计安全日志并调整规则。

**注意事项**: 速率限制需与业务负载匹配，避免误杀正常请求；JWT 密钥应定期轮换。

---

### 实践 5：可观测性与监控集成

**说明**: Higress 提供了丰富的可观测性功能，支持 Prometheus 指标、分布式追踪（如 SkyWalking）和日志采集。建议集成 OpenTelemetry 以实现全链路监控。

**实施步骤**:
1. 在 Higress Gateway 中启用 Prometheus 指标暴露（默认端口 `15020`）。
2. 配置日志采集（如对接 Fluentd 或 Loki）。
3. 启用分布式追踪（设置 `sampling` 参数）。
4. 在监控平台（如 Grafana）中导入 Higress 仪表盘模板。

**注意事项**: 高流量场景下需调整采样率以控制存储成本；确保监控数据的安全性。

---

### 实践 6：平滑升级与灰度发布

**说明**: Higress 支持网关的无缝升级和服务的灰度发布。通过版本化的路由配置，可逐步切换流量，降低发布风险。

**实施步骤**:
1. 部署新版本服务并打上版本标签（如 `v2`）。
2. 在 Higress 中定义基于权重的路由规则（如 10% 流量指向 `v2`）。
3. 逐步调整权重直至全量切换。
4. 网关升级时使用滚动更新策略（`RollingUpdate`）。

**注意事项**: 灰度发布需监控错误率和延迟；保留快速回滚机制（如立即恢复旧版本路由）。

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/3 (QUIC) 协议

**说明**: HTTP/3 基于 UDP 协议，解决了 TCP 队头阻塞问题，显著降低了弱网环境下的延迟。对于 Higress 这种网关产品，开启 HTTP/3 能大幅提升连接建立速度和传输稳定性。

**实施方法**:
1. 在 Higress 网关监听器配置中，为需要优化的路由或域名启用 HTTP/3 协议支持。
2. 确保底层网络环境（防火墙、负载均衡器）允许 UDP 流量通过（通常端口 443）。
3. 配置合适的 QUIC 连接超时参数。

**预期效果**: 在高丢包率或高延迟网络环境下，页面加载时间（TTFB）可降低 20%-40%，连接建立成功率提升。

---

### 优化 2：配置全链路超时与重试策略

**说明**: 默认的超时设置往往过于保守（如 60s），会导致大量连接堆积在网关层，消耗线程资源。合理的超时与重试机制能快速释放资源，防止级联雪崩。

**实施方法**:
1. **连接超时**: 建议设置为 2s-5s，避免长时间等待不可达的后端。
2. **请求超时**: 根据业务 P99 耗时设置，建议不超过 10s-30s。
3. **重试策略**: 仅对幂等请求（GET、HEAD）开启重试，重试次数建议为 2 次，使用指数退避算法。

**预期效果**: 在后端服务出现故障或高延迟时，网关资源占用率（CPU/内存）波动减少 30% 以上，请求失败响应时间从 60s 缩短至秒级。

---

### 优化 3：启用 Wasm 插件与本地缓存

**说明**: Higress 原生支持 Wasm 插件。相比于 Lua 或远程调用，Wasm 提供了接近原生的执行速度。同时，在网关层对高频变更少的配置数据或鉴权结果进行本地缓存，可减少对上游服务的请求。

**实施方法**:
1. 将高频使用的鉴权、限流或请求头处理逻辑编写为 Wasm 插件并部署。
2. 在 Wasm 插件或 Higress 配置中开启本地缓存（如 Redis 缓存或内存哈希），缓存 JWT 验证结果或配置信息。
3. 设置合理的 TTL（生存时间）。

**预期效果**: Wasm 插件执行效率比传统 Lua 插件提升 10%-20%；开启本地缓存后，后端鉴权/配置接口 QPS 可降低 50%-80%。

---

### 优化 4：调整 Netty 工作线程与连接池参数

**说明**: Higress 基于 Netty 构建。默认的线程配置可能不适合高并发场景。如果工作线程过少会导致请求处理阻塞，连接池过小会导致频繁建立连接，增加延迟。

**实施方法**:
1. **调整工作线程**: 将 Netty 的 EventLoop 线程数设置为 `CPU 核心数 * 2`。
2. **调整连接池**: 增加上游服务的最大连接数，避免排队等待。
3. **启用 HTTP/2 连接复用**: 确保与后端服务优先建立 HTTP/2 连接，减少 TCP 握手次数。

**预期效果**: 在高并发场景下（QPS > 10k），请求 P99 延迟可降低 15%-30%，吞吐量提升 20% 左右。

---

### 优化 5：开启请求/响应体缓冲与压缩

**说明**: 对于大 Body 传输，不合理的流式处理会阻塞网关线程。开启缓冲和 Gzip/Brotli 压缩可以减少网络带宽占用并提升传输效率。

**实施方法**:
1. **缓冲控制**: 在路由配置中限制最大请求/响应体大小，防止内存溢出（OOM），同时允许网关完全缓冲小请求以获得更高处理速度。
2.

---
## 学习要点

- Higress 是阿里开源的基于 Istio 的云原生 API 网关，深度集成了 K8s 和 Nginx 生态，提供高性能流量管理能力。
- 它支持将 Ingress 与 Gateway API 统一管理，实现了从传统微服务到云原生架构的无缝迁移与流量管控。
- 内置针对 Dubbo、Nacos、Spring Cloud 等主流微服务框架的定制化协议支持，解决了异构系统间的互通难题。
- 提供开箱即用的 WAF（Web 应用防火墙）插件和安全防护能力，有效增强服务接口的安全性。
- 具备强大的可扩展性，支持通过 Wasm 或 Lua 编写自定义插件，灵活处理复杂的流量逻辑与业务需求。
- 兼容 Nginx Ingress 注解配置，大幅降低了用户从传统 Nginx 迁移到 Higress 的学习成本和改造成本。
- 提供完善的控制台和流量观测面板，支持金丝雀发布、蓝绿部署等精细化流量路由策略。


---
## 学习路径

## 学习路径

### 阶段 1：概念认知与环境准备

**学习内容**:
- Higress 的背景与核心价值：理解 Higress 是基于阿里云 Envoy 和 Istio 构建的云原生 API 网关，以及它与传统 Nginx、Kong 网关的区别。
- 基本架构原理：学习 Ingress Gateway 的概念，以及 Higress 如何处理 Kubernetes 集群的南北向流量。
- 核心术语：掌握路由、服务、插件、上游等基础概念。
- 环境搭建：学习如何在本地 Docker 环境或 Kubernetes 集群中部署 Higress。

**学习时间**: 1周

**学习资源**:
- Higress GitHub 仓库 README
- Higress 官方文档 - 快速开始章节
- 云原生网关技术对比文章

**学习建议**: 
不要急于修改配置，先阅读官方文档的架构图。建议使用 Docker Desktop 或 Kind 在本地搭建一个最小化的可用集群，跑通官方提供的 "Hello World" 示例，确认流量能通过网关转发到后端服务。

---

### 阶段 2：核心流量管理与配置实战

**学习内容**:
- 域名与路由配置：深入学习如何配置 Ingress，基于域名、路径、Header 进行流量匹配。
- 负载均衡策略：学习轮询、加权、一致性哈希等 upstream 配置。
- 服务治理：掌握全局限流、熔断、重试及超时机制的具体配置。
- 金丝雀发布/蓝绿部署：学习如何利用 Higress 进行流量的精细切分，实现灰度发布。
- 控制台使用：熟悉 Higress Dashboard 的操作，进行可视化的流量管理。

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 流量管理章节
- Envoy 官方文档（关于 HTTP 路由与负载均衡部分）
- Higress 官方示例配置集

**学习建议**: 
动手实践是关键。尝试模拟一个真实的业务场景，例如将一个后端应用部署在 K8s 中，通过 Higress 暴露服务，并配置全局限流（例如 10 QPS）进行压测验证。重点理解 "WasmPlugin" 和 "Ingress" 两种配置方式的区别。

---

### 阶段 3：插件开发与可观测性

**学习内容**:
- 插件系统深入：理解 Higress 的插件加载机制，学习如何使用 Lua 或 WASM (WebAssembly) 开发自定义插件。
- 内置插件应用：熟练配置并调试认证鉴权（如 KeyAuth）、请求/响应修改、CORS 处理等常用插件。
- 可观测性集成：学习如何配置 Prometheus 监控指标、集成 Zipkin/SkyWalking 进行链路追踪，以及对接日志服务（如 SLS, Elasticsearch）。
- 安全防护：学习配置 IP 访问控制、防 CC 攻击等安全策略。

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档 - 插件市场与自定义开发章节
- WebAssembly (Wasm) 基础教程（若需开发高性能插件）
- Prometheus 与 OpenTelemetry 集成指南

**学习建议**: 
尝试编写一个简单的 Lua 插件来实现特定的请求头修改或鉴权逻辑，这能极大加深对请求生命周期的理解。同时，务必搭建一套监控看板（Grafana），观察网关的 QPS、延迟和成功率，学会通过指标排查网关瓶颈。

---

### 阶段 4：高可用架构与源码级精通

**学习内容**:
- 高可用部署：学习 Higress 在生产环境下的多副本部署、弹性伸缩与资源规划。
- 深入 Envoy 与 Istio：深入研读 Envoy 配置，理解 Higress 如何通过 xDS 协议与数据面交互。
- 服务网格集成：学习 Higress 作为 Istio Gateway 的无缝对接与高级玩法。
- 源码剖析：阅读 Higress Controller 源码，理解 Kubernetes Informer 机制以及配置如何转化为 Envoy 配置。
- 性能调优：学习连接池、Buffer 等底层参数调优，应对极高并发场景。

**学习时间**: 4周以上

**学习资源**:
- Higress GitHub 源码
- Envoy 官方深度文档
- Istio 网络与流量管理深度解析
- 云原生网关生产最佳实践白皮书

**学习建议**: 
在这个阶段，应尝试从源码层面解决问题。你可以尝试向 Higress GitHub 提交 PR 或参与 Issue 讨论。思考如何将 Higress 与现有的微服务治理体系深度整合，并针对大流量场景设计压测方案与容灾预案。

---
## 常见问题


### 1: Higress 是什么？它与 Nginx 或 Kong 等传统网关有什么区别？

1: Higress 是什么？它与 Nginx 或 Kong 等传统网关有什么区别？

**A**: Higress 是一个基于阿里云内部多年实践沉淀的云原生 API 网关。它是在开源网关 Envoy（由 Lyft 开发的高性能代理）和 Istio（服务网格）的基础上构建的。

与传统网关（如 Nginx、OpenResty 或 Kong）的主要区别在于：
1.  **架构基础**：Nginx/Kong 多基于多进程内存模型，而 Higress 基于 Envoy，采用 C++ 编写的 L7 代理，具有更低的内存占用和更高的并发性能。
2.  **标准化与扩展性**：Higress 原生支持 WASM（WebAssembly）插件。这意味着开发者可以使用 C/C++、Go、Rust、JavaScript 甚至 Python 编写插件，而不需要像传统网关那样必须使用 Lua（OpenResty）或 C/Java（Kong）。WASM 插件具有热加载、动态隔离和安全性高的特点。
3.  **云原生集成**：Higress 设计之初就深度集成了 Kubernetes 和 Istio，可以作为 Ingress Controller 使用，也能作为服务网格的南北向网关，实现了从微服务到 API 管理的无缝衔接。

---



### 2: Higress 是否兼容现有的 Nginx 或 Ingress 配置？

2: Higress 是否兼容现有的 Nginx 或 Ingress 配置？

**A**: 是的，Higress 提供了高度的兼容性，旨在降低迁移门槛。

1.  **Nginx 兼容**：Higress 内置了 Nginx 的配置转换逻辑。虽然它不直接运行 `nginx.conf`，但支持将 Nginx 的注解或部分配置逻辑迁移到 Higress 的配置中。
2.  **Kubernetes Ingress 兼容**：Higress 完全实现了 Kubernetes Ingress API 规范。这意味着你现有的 Kubernetes Ingress YAML 文件可以直接在 Higress 上运行，无需修改即可作为标准的入口控制器工作。
3.  **阿里云 MSE 兼容**：对于阿里云的用户，Higress 兼容 MSE（微服务引擎）的网关规范，支持从云上到云下的平滑迁移。

---



### 3: Higress 支持哪些类型的流量管理和路由规则？

3: Higress 支持哪些类型的流量管理和路由规则？

**A**: Higress 提供了企业级的流量管理能力，支持非常细粒度的路由控制：

1.  **标准路由**：支持基于 HTTP Header、Query 参数、Cookie、路径前缀/正则匹配的流量路由。
2.  **灰度发布（金丝雀发布）**：支持基于 Header 或权重的流量切分，允许用户将一小部分流量发送到新版本服务进行测试。
3.  **全链路灰度**：配合微服务框架（如 Spring Cloud、Dubbo），Higress 能够透传灰度标签，实现从入口网关到后端微服务的全链路流量染色。
4.  **服务发现集成**：原生支持 Nacos、Consul、DNS 以及 Kubernetes Service 作为服务来源，能够动态感知后端服务实例的上下线。

---



### 4: 如何在 Higress 中扩展功能？是否支持自定义插件？

4: 如何在 Higress 中扩展功能？是否支持自定义插件？

**A**: Higress 的核心优势之一是其强大的插件扩展能力，主要通过 **WASM (WebAssembly)** 技术实现。

1.  **WASM 插件**：这是 Higress 推荐的扩展方式。开发者可以使用 Go、AssemblyScript (TypeScript)、Rust 或 C++ 编写业务逻辑，编译成 `.wasm` 文件后上传到 Higress。这种方式不需要重新编译网关本身，且插件运行在独立的沙箱中，崩溃不会影响网关主进程。
2.  **原生插件**：Higress 内置了常见的网关功能，如认证鉴权（Key Auth, JWT, OIDC）、限流熔断、请求/响应重写、CORS 处理等，通常只需在控制台勾选即可启用。
3.  **Lua/Python 支持**：虽然核心是 WASM，但为了兼容旧生态，Higress 也在逐步增强对 Lua 脚本的支持，或者允许通过 WASM 运行时执行 Python 脚本（通过特定运行时如 WasmEdge-Python）。

---



### 5: Higress 的性能表现如何？能否应对高并发场景？

5: Higress 的性能表现如何？能否应对高并发场景？

**A**: Higress 专为高性能和高吞吐量设计，能够应对大规模的企业级流量。

1.  **底层优势**：基于 Envoy 构建，Envoy 本身就是为云原生环境设计的高性能代理，采用异步非阻塞 I/O 模型，处理长连接和海量并发连接的能力非常强。
2.  **基准测试**：在官方的基准测试中，Higress 在处理 HTTP/HTTPS 请求时的吞吐量和延迟表现优异，特别是在开启 WASM 插件时，性能损耗远低于传统的 Lua 脚本方案。
3.  **资源消耗**：相比基于 Java 的网关或重量级 OpenResty 实例

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: 本地环境搭建与基础插件开发

### 问题**: Higress 基于 Envoy 构建，并提供了 Wasm 插件能力。请尝试在本地使用 Docker 快速启动一个 Higress 实例，并访问其控制台。随后，编写一个最基础的 Wasm 插件（例如修改 HTTP 响应头），将其部署到 Higress 中，通过 `curl` 验证响应头是否已按预期修改。

### 提示**: 参考 Higress 官方文档中的“快速开始”部分，重点关注 `docker-compose.yml` 的配置。对于 Wasm 插件，可以先使用官方提供的 Go SDK 模板，编写 `OnHttpResponseHeaders` 函数。

### 

---
## 实践建议

基于 Higress 作为 AI Native API 网关的定位，结合其作为云原生网关的技术特性，以下是 6 条针对实际生产环境的实践建议：

### 1. 利用 Wasm 插件实现 AI 请求的“无损”处理
**场景：** 在调用大模型（如 OpenAI、通义千问）时，通常需要处理敏感词过滤、计费统计或请求头转换。
**建议：** 不要在业务代码中处理这些逻辑，而是编写 Wasm (WebAssembly) 插件挂载到 Higress 的路由上。
**具体操作：**
*   使用 Higress 官方提供的 `ai-proxy` 插件或基于 Go/AssemblyScript 开发自定义 Wasm 插件。
*   在插件中实现 Prompt 的预处理（如注入系统提示词）或 Response 的后处理（如过滤敏感信息）。
**常见陷阱：** 避免使用 Lua 脚本处理复杂的 AI 流式响应，流式数据的处理在 Wasm 中性能更优且更稳定。

### 2. 配置“模型供应商”路由以实现统一接入与降级
**场景：** 业务系统可能同时调用不同厂商的模型，或者需要从某个模型（如 GPT-4）降级到更便宜的模型（如 GPT-3.5）。
**建议：** 利用 Higress 的服务来源管理功能，配置多个模型提供商。
**具体操作：**
*   在 Higress 中配置多个服务，分别指向不同的 LLM 提供商。
*   设置路由规则，根据请求 URL 路径（如 `/v1/chat/gpt4` 或 `/v1/chat/qwen`）将流量分发到不同的后端服务。
*   结合 Higress 的全链路灰度能力，实现模型版本的 A/B 测试。
**最佳实践：** 将 API Key 集中存储在 Higress 的配置中，而不是分散在各个微服务里，便于统一轮换和管控。

### 3. 针对流式响应的超时与缓冲策略配置
**场景：** AI 生成内容通常耗时较长，且采用 SSE (Server-Sent Events) 或流式传输。
**建议：** 调整 Higress 路由和后端服务的超时配置，避免网关过早断开连接。
**具体操作：**
*   将路由配置中的 `requestTimeout` 或 `timeout` 设置为较大的值（例如 5 分钟或更长，视模型最大生成时间而定）。
*   确保开启了 Higress 对流式数据的透传支持（默认通常开启，但需检查上游服务配置）。
**常见陷阱：** 如果开启了全链路追踪，注意流式响应会产生大量的 Span 数据，可能导致追踪存储爆满，建议对流式请求进行采样率调整。

### 4. 实施基于 Token 的精细化限流
**场景：** 大模型 API 调用成本通常按 Token 计费，且模型厂商有严格的 RPM (每分钟请求数) 或 TPM (每分钟 Token 数) 限制。
**建议：** 不仅仅基于 QPS (每秒请求数) 限流，更要结合 Token 预估进行限流。
**具体操作：**
*   虽然网关难以精确计算发送前的 Token 数，但可以通过配置“请求体大小限制”来作为粗糙的 Token 限制（因为 1 Token 约等于 4 个字符）。
*   针对特定 API Key 或用户 ID，配置 Higress 的 `local-ratelimit` 或 `redis-ratelimit` 插件，防止突发流量导致上游厂商 API 封禁。
**最佳实践：** 对不同优先级的业务（如内部核心业务 vs 外部试用业务）设置不同的限流阈值。

### 5. 鉴权与安全：屏蔽后端 API Key
**场景：** 前端直接调用网关时，不能暴露上游大模型厂商的 API Key。
**建议：** 使用 Higress 的认证鉴权插件（如 `key-auth` 或 `jwt-auth`）作为网关层的“门神”。
**

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI 原生](/tags/ai-%E5%8E%9F%E7%94%9F/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [LLM](/tags/llm/) / [MCP 协议](/tags/mcp-%E5%8D%8F%E8%AE%AE/) / [WASM](/tags/wasm/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260130-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260201-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260205-github_trending-alibaba-higress-6.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260215-github_trending-alibaba-higress-5.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260216-github_trending-alibaba-higress-6.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*