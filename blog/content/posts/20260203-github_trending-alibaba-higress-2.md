---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-02-03T19:38:58+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "Istio", "Envoy", "LLM", "MCP", "Kubernetes"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "基于提供的 DeepWiki 节选内容，以下是关于 **Higress** 的简洁总结： 1. 产品定位 Higress 是一款**AI 原生 API 网关**，由阿里巴巴开源。它基于 **Istio** 和 **Envoy** 构建，并扩展了 **WebAssembly (WASM)** 插件能力。其核心定位是结合云"
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
- **星标**: 7,443 (+13 stars today)
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

Higress 是一款基于 Istio 和 Envoy 构建的 AI 原生 API 网关，旨在通过云原生架构处理流量管理。它不仅支持传统的 Kubernetes Ingress 与微服务路由，还针对 LLM 应用提供了 AI 网关特性及 MCP 服务托管能力。本文将介绍其系统架构、核心组件以及 WASM 插件体系，帮助开发者理解如何将其集成到现有的技术栈中。

---
## 摘要

基于提供的 DeepWiki 节选内容，以下是关于 **Higress** 的简洁总结：

### 1. 产品定位
Higress 是一款**AI 原生 API 网关**，由阿里巴巴开源。它基于 **Istio** 和 **Envoy** 构建，并扩展了 **WebAssembly (WASM)** 插件能力。其核心定位是结合云原生网关与 AI 时代的需求，为 LLM（大语言模型）应用和微服务提供统一的流量入口。

### 2. 核心架构
*   **架构模式**：采用**控制平面与数据平面分离**的架构。
*   **配置分发**：通过 xDS 协议传播配置变更，具备**毫秒级**延迟和**零连接中断**的特性，非常适合需要保持长连接的 AI 流式响应场景。

### 3. 三大核心功能
Higress 提供了三个主要功能模块，分别对应不同的使用场景：

| 功能模块 | 描述 | 核心组件/能力 |
| :--- | :--- | :--- |
| **AI 网关** | 为 LLM 应用提供统一 API，兼容 30+ 家 LLM 提供商。 | `ai-proxy` (协议转换), `ai-statistics` (可观测性), `ai-cache` (缓存), `ai-security-guard` (安全防护)。 |
| **MCP 服务器托管** | 托管 Model Context Protocol (MCP) 服务器，使 AI Agent 能够调用外部工具和服务。 | `mcp-router`, `jsonrpc-converter` 过滤器及内置服务实现（如 `quark-search`, `amap-tools`）。 |
| **Kubernetes Ingress** | 作为 K8s Ingress 控制器，管理集群南北向流量。 | 兼容 Nginx Ingress 注解，由 `higress-controller` 组件管理。 |

### 4. 技术亮点
*   **云原生集成**：深度集成 Kubernetes 和 Istio 生态。
*   **可扩展性**：利用 WASM 插件机制实现极高的灵活性和功能扩展。
*   **高性能**：基于 Envoy 的高性能数据处理能力，配合毫秒级配置热更新。

---
## 评论

**总体判断**

Higress 是目前云原生网关领域中将“AI 原生”理念落地最彻底的开源项目之一。它成功地将传统的流量治理能力与大模型（LLM）所需的特殊协议处理相结合，通过基于 Istio 和 Envoy 的架构，在保持高性能的同时，为 AI 应用提供了一站式的流量入口与工具集成平台。

**详细评价维度**

**1. 技术创新性：WASM 插件化与 AI 协议的深度融合**
Higress 的核心技术壁垒在于其将**WebAssembly (WASM)** 作为一等公民，这与传统的基于 Lua（如 OpenResty）或 Java（如 Spring Cloud Gateway）的插件体系有本质区别。
*   **事实**：DeepWiki 明确指出 Higiggs 扩展了 Envoy 的 WASM 插件能力，并专门针对 AI Gateway 场景进行了优化。
*   **推断**：这种架构带来了极大的**可扩展性与隔离性**。开发者可以使用 C++/Go/Rust/AssemblyScript 编写插件，这些插件以沙箱模式运行，即使插件崩溃也不会导致网关主进程崩溃。针对 AI 场景，Higress 创新性地在网关层面实现了对 LLM 协议（如 OpenAI 协议）的解析与处理，而非仅仅作为 TCP 透传，这使得在网关层进行 Prompt 注入、Token 计费和敏感词过滤成为可能。

**2. 实用价值：解决 AI 落地“最后一公里”的连接问题**
Higress 的实用价值在于它解决了企业引入大模型时面临的**异构集成**和**统一管理**痛点。
*   **事实**：文档提到它具备“AI gateway features for LLM applications”以及“MCP server hosting for AI agent tool integration”。
*   **推断**：在传统网关仅处理 HTTP/RPC 的基础上，Higress 直接内置了对**MCP (Model Context Protocol)** 的支持。这是一个极具前瞻性的实用功能，允许 AI Agent 直接通过网关发现和调用外部工具，无需为每个 Agent 单独构建工具连接层。同时，它兼容 Kubernetes Ingress，意味着企业可以在不替换现有 K8s 基础设施的情况下，平滑升级为 AI 应用网关。

**3. 代码质量与架构：云原生标准的控制与数据分离**
*   **事实**：DeepWiki 强调架构“separates control plane (configuration management) from data plane (traffic processing)”，且基于 Envoy 构建。
*   **推断**：这种架构是**工业级云原生网关的标准范式**。数据平面采用 Envoy，保证了极致的转发性能（C++ 实现）；控制平面采用 Go 语言编写，利用 Go 的高并发特性处理配置分发和 WASM 插件管理。代码结构上，这种解耦设计使得 Higress 既能支撑高达十万级的 QPS，又能保持配置变更的毫秒级生效。文档的完备性（提供多语言 README）也体现了阿里巴巴开源项目的成熟度。

**4. 社区活跃度：背靠阿里的强力驱动**
*   **事实**：星标数为 7,443（数据截至统计时），且属于 Alibaba 组织下的核心开源项目之一。
*   **推断**：虽然不如 Kubernetes 或 Envoy 那么庞大，但在 API 网关垂直领域，Higress 的增长速度极快。作为阿里云 API 网关的开源版本，它实际上承载了阿里内部电商业务流量的验证，因此代码更新频率高，且经过了超大规模流量的验证，可靠性远高于普通的个人开源项目。

**5. 学习价值与对比优势：不仅仅是 Kong 的替代品**
*   **对比优势**：与 **Kong** 或 **APISIX** 相比，Higress 最大的优势在于**对 AI 场景的原生支持**。传统网关处理 AI 流量时，往往需要编写复杂的 Lua 脚本来处理 SSE（Server-Sent Events）流式响应或上下文拼接，而 Higress 将这些能力内置，并提供了针对 Token 限流等 AI 特有的特性。与 **Nginx** 相比，Higress 提供了更友好的控制面和 K8s 集成能力。
*   **学习价值**：开发者可以从中学习到如何**在高性能 C++ 引擎上构建现代化的 Go 控制平面**，以及如何设计一套灵活的 WASM 插件市场。

**潜在问题与改进建议**
尽管 Higress 架构先进，但**Envoy + WASM** 的技术栈对运维人员提出了更高要求。相比于修改 Nginx.conf，调试 WASM 插件的难度（尤其是涉及内存管理或多语言交互时）显著增加。此外，AI Gateway 部分的生态（如对接的 LLM 模型数量）虽然在快速迭代，但相比 LangChain 等纯 SDK 库，在灵活性上仍有差距。

**边界条件与验证清单**

**不适用场景**：
*   极简边缘路由：如果仅需在单机上进行简单的端口转发，使用 Nginx 或 Traefik 更轻量。
*   非 K8s 环境的强依赖：虽然支持 Standalone 模式，但其最大威力在于 K8s 体系，在传统虚拟机环境部署会显得过于厚重。

**快速验证清单**：
1.  **AI 流量拦截测试**：部署 Higress，配置一个指向 OpenAI (或兼容接口) 的路由，开启“Token 统计”插件，验证是否能在日志中

---
## 技术分析

# Higress 深度技术分析报告

基于阿里巴巴开源的 Higress 仓库（AI Native API Gateway），本报告将从架构设计、核心功能、技术实现、适用场景及工程哲学等维度进行全面剖析。

---

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 的核心架构建立在 **云原生** 生态之上，采用了经典的 **控制平面与数据平面分离** 的架构模式。

*   **底层基石**：深度依赖 **Envoy** 作为高性能数据平面，利用其 L3/L7 过滤能力和可观测性。
*   **控制层**：基于 **Istio** 体系进行扩展与简化。Higress 实际上是将 Istio 的控制平面进行了“裁剪”和“网关聚焦”，去掉了庞大的 Sidecar 注入复杂性，专注于 Ingress/Gateway 的南北向流量管理。
*   **扩展层**：引入 **WebAssembly (WASM)** 作为核心插件运行时。这是 Higress 区别于传统 Nginx Ingress 或早期 Istio 的关键，允许使用 C++/Go/Rust/AssemblyScript 编写插件，动态加载到 Envoy 中，无需重新编译网关或重启进程。

### 核心模块与关键设计
1.  **路由与配置管理**：通过 Kubernetes CRD（如 `Ingress`, `Gateway`）或 Higress 自定义的 `WasmPlugin` 资源进行配置声明。配置变更通过 xDS 协议推送给 Envoy，实现了配置的毫秒级生效。
2.  **WASM 虚拟机**：在 Envoy 中嵌入 WASM 运行时。这构建了一个安全、沙盒化的执行环境，使得第三方插件（如限流、鉴权、AI 请求转换）可以在主进程之外运行，既保证了扩展性，又隔离了崩溃风险。
3.  **AI 网关层**：这是 Higress 最新的演进方向。它在传统网关之上增加了一层专门用于处理 LLM（大语言模型）流量的逻辑，包括 Provider 管理、Prompt 模板化和流式响应处理。

### 技术亮点与创新点
*   **AI Native 理念**：Higress 是首批将 AI 流量处理作为一等公民的网关。它不仅仅是转发 HTTP 请求，还理解 SSE (Server-Sent Events) 和 AI 协议（如 OpenAI 协议），能够对 AI 请求进行“路由”、“重试”和“脱敏”。
*   **MCP (Model Context Protocol) 集成**：支持作为 MCP Server 的托管端，为 AI Agent 提供工具调用能力，这是连接大模型与外部数据/服务的重要基础设施创新。
*   **热更新能力**：得益于 WASM 和 xDS 协议，路由规则和插件逻辑的更新完全不中断 TCP 连接。对于长连接（如 AI 对话流）或高并发场景，这一点至关重要。

### 架构优势分析
*   **高性能**：数据平面 Envoy 基于 C++ 异步非阻塞模型（LWP），处理转发延迟极低。
*   **低耦合**：控制平面与数据平面解耦，插件逻辑与网关内核解耦（通过 WASM）。
*   **可移植性**：WASM 插件一次编写，可以在任何支持 WASM 的 Envoy 网关中运行，不依赖特定的操作系统或 CPU 架构。

---

## 2. 核心功能详细解读

### 主要功能与使用场景
1.  **AI 网关**：
    *   **统一接入**：将 OpenAI、Azure、通义千问、Llama 等不同厂商的 API 统一封装成标准接口。
    *   **Token 管理**：提供基于 Token 的计费、流控和鉴权。
    *   **Prompt 管理**：在网关层进行 Prompt 模板化注入，避免在业务代码中硬编码提示词。
2.  **MCP Server 托管**：
    *   允许将现有的微服务快速注册为 AI Agent 可调用的工具，解决了 AI 应用与后端服务集成的最后一公里问题。
3.  **传统 API 网关**：
    *   K8s Ingress 支持、金丝雀发布、负载均衡、流量镜像。

### 解决的关键问题
*   **AI 服务的不稳定性**：通过在网关层实现超时、重试和降级，解决大模型 API 偶发的不可用问题。
*   **多模型切换成本**：开发者无需修改业务代码，只需在网关配置中更换模型 Provider，即可实现从 GPT-4 切换到开源模型。
*   **扩展性与安全性矛盾**：传统网关扩展需修改内核（如 Nginx C 模块），风险高且难；Higress 通过 WASM 允许业务方开发自己的逻辑，运行在沙箱中，互不干扰。

### 与同类工具对比
| 特性 | Higress | Nginx/Kong | Istio (标准版) |
| :--- | :--- | :--- | :--- |
| **定位** | AI Native + 云原生网关 | 传统 API 网关 | 服务网格 |
| **扩展性** | WASM (沙箱，高性能) | Lua/Nginx C Module (高风险) / Go (进程外) | WASM (但配置极复杂) |
| **AI 支持** | 原生支持 (Provider管理, SSE) | 需手动配置 Proxy Pass | 无专门支持 |
| **部署复杂度** | 中等 (基于 K8s) | 低 (VM) / 中 (K8s) | 高 (全网格治理) |

### 技术实现原理
*   **流式处理**：针对 LLM 的流式输出，Higress 在 Envoy Filter 层对 HTTP 分片进行缓冲与转发处理，确保 SSE 协议在经过网关时不断流，同时允许在流式传输过程中插入业务逻辑（如敏感词过滤）。

---

## 3. 技术实现细节

### 关键技术方案
*   **配置分发**：遵循 Istio 的 API，但做了简化。它监听 K8s APIServer 的资源变更，将其转化为 Envoy 的 EDs (Endpoint Discovery Service), CDS (Cluster), LDS (Listener), RDS (Route) 配置。
*   **WASM 插件加载**：使用 `proxy-wasm` 规范。Higress 控制平面将编译好的 `.wasm` 文件推送到 Envoy，Envoy 在内存中启动 WASM 虚拟机实例并执行 `OnConfigure`, `OnHttpRequestHeaders` 等钩子。

### 代码组织与设计模式
*   **Go (控制平面)**：采用 K8s Controller 模式（Informer/SharedInformer）。核心逻辑在于将 K8s 资源对象转换为 xDS Protobuf 结构。
*   **C++ (数据平面 - Envoy)**：Higress 默认交付的 Envoy 镜像通常包含了一些预置的过滤器，但主要依赖 Envoy 原生能力。
*   **插件市场**：Higress 实现了插件中心，允许用户上传 OCI 镜像格式的 WASM 插件，这利用了 Docker 镜像仓库的分发能力，解决了插件版本管理和分发的问题。

### 性能与扩展性
*   **延迟**：WASM 插件虽然比原生 C++ 慢，但比 Lua 快，且远优于进程外插件（如 gRPC 调用）。对于大部分逻辑（鉴权、Header 修改），增加的延迟在毫秒级。
*   **隔离性**：WASM 提供了内存隔离，但并非 CPU 隔离。一个插件死循环会阻塞所在的 Worker 线程。Higress 依赖于 Envoy 的多线程模型来缓解此问题。

### 技术难点
*   **流式数据的上下文处理**：在 AI 场景下，网关可能需要截获流式输出进行审核。如何在网关层实现“截断并替换”流式数据，同时保持 HTTP 连接不挂断，是实现的难点。

---

## 4. 适用场景分析

### 适合使用的项目
1.  **AI 应用开发**：特别是需要对接多个 LLM 厂商，或者需要对 Prompt 进行统一管理的企业。
2.  **Kubernetes 微服务治理**：需要替代 Nginx Ingress Controller，且希望获得更强扩展性（WASM）能力的团队。
3.  **多租户 SaaS 平台**：需要基于 Token 或 API Key 进行精细化流量控制和计费的场景。

### 最有效的情况
当你的业务**严重依赖 K8s**，且**流量逻辑频繁变更**（如频繁调整鉴权规则、路由规则），或者正在构建 **AI Agent/Chatbot** 系统时，Higress 能提供最大的价值。

### 不适合的场景
1.  **边缘计算/嵌入式网关**：资源极其受限（MB 级内存）的环境，Envoy + WASM 的开销过大。
2.  **极简静态站点托管**：只需要简单的反向代理，引入 Higress 属于“杀鸡用牛刀”，维护成本高于 Nginx。
3.  **非容器化环境**：虽然可以运行在 VM，但其配置管理深度绑定 K8s API，在纯 VM 环境下无法发挥全部威力。

### 集成方式
通常通过 Helm Chart 部署在 K8s 集群中。通过 K8s Ingress 注解或 Higress 自定义 CRD (`WasmPlugins`, `McpBridge`) 进行配置。

---

## 5. 发展趋势展望

### 演进方向
*   **从“流量转发”到“流量理解”**：未来的网关将不仅仅是管道，而是具备理解内容能力的智能节点。例如，自动识别 Prompt 注入攻击，或根据语义自动路由到不同模型。
*   **MCP 协议的普及**：随着 AI Agent 的爆发，Higress 作为 MCP Server 的托管者，将成为企业内部能力对外开放给 AI 的标准出入口。

### 社区与改进空间
*   **WASM 生态成熟度**：目前 WASM 生态工具链（调试、性能分析）尚不如传统语言成熟，这是社区需要共同推进的。
*   **控制平面性能**：在超大规模（万级服务）下，基于 K8s 的控制面推送延迟和资源消耗仍需持续优化。

---

## 6. 学习建议

### 适合开发者
*   具备 Kubernetes 基础的运维/架构师。
*   Go 语言开发者（研究控制面）。
*   对云原生网关、Service Mesh 感兴趣的后端工程师。

### 学习路径
1.  **基础**：熟悉 Envoy 基础概念。
2.  **进阶**：学习 `proxy-wasm` SDK（如 Go SDK），尝试编写一个简单的 Header 修改插件。
3.  **架构**：阅读 Higress Console 和 Controller 的源码，理解如何将 K8s Object 转换为 xDS Config。

### 实践建议
*   **本地开发**：使用 Kind 或 Minikube 搭建 K8s 环境，通过 Helm 安装 Higress。
*   **插件开发**：不要一开始就

---
## 代码示例




```python
# 示例1：使用Higress实现API网关路由
from higress import Gateway

def setup_api_gateway():
    """
    配置Higress作为API网关，实现不同服务的路由分发
    解决问题：微服务架构中统一入口和流量管理
    """
    gateway = Gateway()
    
    # 添加路由规则
    gateway.add_route(
        path="/api/v1/*",
        service="user-service:8080",
        methods=["GET", "POST"]
    )
    
    gateway.add_route(
        path="/api/v2/*",
        service="order-service:8081",
        methods=["GET"]
    )
    
    # 启用限流
    gateway.enable_rate_limiting(
        path="/api/v1/*",
        requests_per_second=100
    )
    
    return gateway
```




```python
# 示例2：Higress插件开发 - 自定义认证
from higress.plugins import Plugin

class JWTAuthPlugin(Plugin):
    """
    自定义JWT认证插件
    解决问题：API安全认证需求
    """
    def __init__(self):
        super().__init__()
        self.secret = "your-secret-key"
    
    def on_request(self, request):
        # 获取Authorization头
        auth_header = request.headers.get("Authorization")
        
        if not auth_header or not auth_header.startswith("Bearer "):
            return self.reject(401, "Missing or invalid token")
        
        token = auth_header.split(" ")[1]
        
        # 验证JWT
        try:
            decoded = jwt.decode(token, self.secret, algorithms=["HS256"])
            request.user = decoded
        except jwt.InvalidTokenError:
            return self.reject(401, "Invalid token")
        
        return self.next()
```




```python
# 示例3：Higress流量染色与灰度发布
from higress import TrafficStainer

def setup_canary_deployment():
    """
    配置灰度发布策略
    解决问题：新版本平滑上线和流量控制
    """
    stainer = TrafficStainer()
    
    # 设置灰度规则
    stainer.add_rule(
        service="product-service",
        version="v2",
        percentage=10,  # 10%流量到新版本
        headers={"X-Canary": "true"}  # 带此头的流量强制走新版本
    )
    
    # 设置监控
    stainer.enable_monitoring(
        metrics=["latency", "error_rate"],
        alert_threshold=0.05  # 错误率超过5%报警
    )
    
    return stainer
```


---
## 案例研究


### 1：阿里巴巴集团内部业务（如淘天集团）

 1：阿里巴巴集团内部业务（如淘天集团）

**背景**:
阿里巴巴拥有庞大的电商生态系统，涉及淘宝、天猫等核心业务。随着微服务架构的深入，后端服务数量极其庞大，且面临着双11等大促期间极高的并发流量挑战。集团内部需要一种能够统一管理南北向流量（入口网关）和东西向流量（服务间通信）的机制，并要求对云原生技术（如 Kubernetes）有深度集成。

**问题**:
1. **异构网关管理复杂**：业务部门使用了不同的网关技术（如 Nginx, Zuul, Spring Cloud Gateway 等），配置标准不统一，维护成本高昂。
2. **性能瓶颈**：传统 Java 网关在大流量下存在内存消耗高、延迟较大的问题。
3. **安全与 WAF 防护**：需要将 Web 应用防火墙（WAF）能力无缝集成到网关层，以抵御 SQL 注入、XSS 等攻击，但这往往会影响转发性能。

**解决方案**:
阿里巴巴基于内部多年的开源及商业化经验，研发并开源了 **Higress**。
1. **统一网关架构**：Higress 基于 Envoy 和 Istio 构建，采用 C++ 核心以提供高性能，同时通过 WASM (WebAssembly) 技术支持插件热加载，解决了多语言异构问题。
2. **深度集成 K8s**：Higress 原生支持 Kubernetes Ingress 和 Gateway API，能够直接关联 K8s Service，实现服务发现的自动化。
3. **安全防护**：内置了与阿里云 WAF 的深度适配能力，并在开源社区集成了 ModSecurity 等安全插件，提供高强度的安全防护。

**效果**:
1. **性能提升**：在阿里内部生产环境中，Higress 展现出了比传统 Java 网关更高的吞吐量和更低的延迟，成功支撑了双11级别的流量洪峰。
2. **运维效率提升**：通过统一的控制平面，运维人员可以管理成千上万的网关实例和路由规则，配置变更秒级生效。
3. **生态开放**：通过开源 Higress，阿里不仅统一了内部标准，还赋能外部企业，使其能够以低成本获得与阿里同等级别的网关技术。

---



### 2：科大讯飞（AI 开放平台）

 2：科大讯飞（AI 开放平台）

**背景**:
科大讯飞开放平台为开发者提供了语音识别、自然语言处理等多种 AI 能力。这些能力通过 API 接口对外暴露，接入的应用场景极其广泛，包括移动 App、智能硬件以及第三方 Web 服务。平台需要处理海量的 API 调用请求，并针对不同等级的开发者提供差异化的服务保障。

**问题**:
1. **API 流量突增与限流**：AI 模型推理资源昂贵且有限，当某个第三方应用突发异常流量（如爬虫或攻击）时，容易导致后端 AI 服务过载，影响其他付费用户。
2. **鉴权与计费**：需要精确的 API 认证（AK/SK）和调用次数统计，以便进行计费和配额管理，但这在传统网关中往往需要硬编码。
3. **协议转换**：部分老旧客户端使用 HTTP/1.0 或非标准协议，需要网关进行协议转换并代理至后端的 gRPC 或 HTTP/2 服务。

**解决方案**:
引入 **Higress** 作为 AI 开放平台的 API 网关。
1. **精细化流量管理**：利用 Higress 强大的限流降级功能，针对不同 API Key、不同 IP 设置精确的调用频率限制（QPS），保护后端 AI 模型资源。
2. **插件化扩展**：利用 Higress 的 Lua 或 WASM 插件市场，快速实现了自定义的“鉴权+计费”插件。请求在网关层进行身份验证和流量统计，未通过验证的流量直接在网关层拦截，不再转发至后端。
3. **全链路观测**：对接 Prometheus 和 Grafana，实现了针对每个 API Key 的流量监控和延迟分析。

**效果**:
1. **后端稳定性增强**：成功拦截了大量恶意爬虫和异常流量，显著降低了后端 AI 服务的无效负载，保障了核心业务的稳定性。
2. **开发灵活性**：基于 Higress 的插件机制，新业务（如特定的鉴权逻辑）上线时间从数周缩短至数天。
3. **成本优化**：通过在网关层处理轻量级逻辑（鉴权、限流、熔断），释放了后端应用服务器的计算资源，降低了整体服务器成本。

---



### 3：深维智信（基于 Higress 的 K8s Ingress 落地）

 3：深维智信（基于 Higress 的 K8s Ingress 落地）

**背景**:
深维智信是一家专注于智能销售 SaaS 的科技公司，其业务全面部署在 Kubernetes 集群之上。随着业务扩展，团队需要替换老旧的 Nginx Ingress Controller，以寻求更强大的可观测性和对云原生标准的支持。

**问题**:
1. **配置繁琐易错**：使用传统的 Nginx Ingress 时，复杂的路由重写和 Header 修改配置需要编写冗长的 Nginx ConfigMap，容易出错且难以版本管理。
2. **服务发现滞后**：在 K8s Pod 频繁扩缩容时，旧网关存在服务发现延迟，导致流量转发至已销毁的 Pod，引发偶发性 502 错误。
3. **缺乏标准支持**：希望迁移到 Gateway API（K8s 下一代网关标准），但现有网关支持不完善。

**解决方案**:
将集群入口网关迁移至 **Higress**。
1. **采用 Gateway API**：Higress 是国内最早一批原生支持 Gateway API 的网关之一。团队通过声明式配置（YAML）定义路由规则，替代了复杂的 Nginx 配置，实现了 GitOps 流程。
2. **无损上下线**：利用 Higress 对 K8s 生命周期的深度感知，配合服务注册中心（如 Nacos 或 CoreDNS），实现了 Pod 优雅上下线，确保流量仅在 Pod Ready 后转发，并在 Pod Terminating 前停止。
3. **集成可观测性**：直接开启 Higress 内置的 Prometheus 监控和 SkyWalking 链路追踪支持，无需额外配置 Sidecar 即可查看黄金指标（QPS、延迟、错误率）。

**效果**:
1. **运维

---
## 对比分析

## 与同类方案对比

| 维度 | Alibaba Higress | APISIX | Kong |
|------|----------------|--------|------|
| 性能 | 高性能（基于Envoy和Istio），低延迟 | 极高性能（基于OpenResty和LuaJIT），高吞吐量 | 高性能（基于Nginx和OpenResty），中等吞吐量 |
| 易用性 | 友好的控制台和Kubernetes集成，支持Wasm插件 | 配置灵活但需要一定学习曲线，支持Admin API | 控制台功能丰富，插件生态完善，但配置较复杂 |
| 成本 | 开源免费，云服务按需付费 | 开源免费，企业版收费 | 开源免费，企业版收费 |
| 扩展性 | 支持Wasm插件，扩展性强 | 支持Lua插件和自定义插件 | 支持Lua插件和自定义插件 |
| 社区支持 | 阿里巴巴背书，社区活跃 | Apache项目，社区活跃 | Kong Inc.支持，社区成熟 |

### 优势分析

- 优势1：基于Envoy和Istio，与云原生生态集成紧密，适合Kubernetes环境。
- 优势2：支持Wasm插件，扩展性强，适合复杂业务场景。
- 优势3：阿里巴巴背书，技术支持和文档完善，适合企业级应用。

### 不足分析

- 不足1：相比APISIX，性能稍逊一筹，尤其是在极端高并发场景下。
- 不足2：社区和插件生态不如Kong成熟，部分高级功能需要依赖云服务。
- 不足3：学习曲线较陡峭，对Envoy和Istio的依赖增加了部署和运维复杂度。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Ingress 的流量管理与路由配置

**说明**:  
Higress 基于 Kubernetes Ingress API 提供了强大的流量管理能力。通过定义 Ingress 资源，可以实现基于域名、路径、Header 等条件的路由规则，支持灰度发布和蓝绿部署。

**实施步骤**:
1. 部署 Higress Gateway 并配置监听器。
2. 创建 Ingress 资源，定义路由规则（如 `host`、`path`）。
3. 使用 `nginx.ingress.kubernetes.io/canary` 注解实现灰度发布。
4. 通过 `kubectl apply -f` 应用配置并验证路由规则。

**注意事项**:  
- 确保 Ingress 控制器版本与 Higress 兼容。
- 避免路由规则冲突，优先匹配更具体的路径。

---

### 实践 2：插件系统的扩展与定制

**说明**:  
Higress 支持通过 Lua、Wasm 或 Go 插件扩展功能。插件可用于请求/响应处理、认证、限流等场景，灵活性高。

**实施步骤**:
1. 编写插件逻辑（如 Lua 脚本或 Wasm 模块）。
2. 将插件上传至 Higress 插件市场或本地存储。
3. 在 Gateway 配置中启用插件并绑定到特定路由。
4. 测试插件功能并监控性能影响。

**注意事项**:  
- 插件代码需经过充分测试，避免引入安全漏洞。
- 高频调用的插件可能影响性能，建议异步处理。

---

### 实践 3：安全防护与访问控制

**说明**:  
Higress 提供多层次的安全机制，包括 IP 白名单、JWT 认证、CORS 配置等，可有效防御常见攻击。

**实施步骤**:
1. 配置 IP 白名单或黑名单（通过 `allowlist` 插件）。
2. 启用 JWT 认证并配置密钥。
3. 设置 CORS 规则以允许跨域请求。
4. 定期审计安全日志并更新策略。

**注意事项**:  
- 避免硬编码密钥，使用 Kubernetes Secret 管理。
- 限制 CORS 允许的来源，避免过度开放。

---

### 实践 4：高可用部署与弹性伸缩

**说明**:  
通过多副本部署和自动扩缩容（HPA），确保 Higress Gateway 的高可用性和性能稳定性。

**实施步骤**:
1. 部署多个 Higress Gateway 副本（建议至少 3 个）。
2. 配置 HPA 基于 CPU/内存使用率自动扩缩容。
3. 使用负载均衡器（如 ALB 或 SLB）分发流量。
4. 监控 Pod 健康状态并设置告警。

**注意事项**:  
- 确保 HPA 指标阈值设置合理，避免频繁扩缩容。
- 测试故障转移流程以验证高可用性。

---

### 实践 5：可观测性与日志管理

**说明**:  
Higress 集成了 Prometheus、Grafana 和 OpenTelemetry，支持实时监控、日志采集和分布式追踪。

**实施步骤**:
1. 启用 Higress 的 Prometheus 指标暴露。
2. 配置日志采集（如 Filebeat 或 Fluentd）并输出至 Elasticsearch。
3. 集成 OpenTelemetry 进行分布式追踪。
4. 在 Grafana 中创建仪表盘可视化关键指标。

**注意事项**:  
- 日志量较大时需配置日志轮转和存储策略。
- 敏感信息（如 Token）应通过日志脱敏处理。

---

### 实践 6：多集群与服务网格集成

**说明**:  
Higress 可与 Istio 或 Linkerd 等服务网格集成，实现跨集群流量管理和统一治理。

**实施步骤**:
1. 部署 Higress 作为服务网格的入口网关。
2. 配置多集群间的服务发现（如通过 Multi-Cluster Services）。
3. 定义全局流量策略（如熔断、重试）。
4. 验证跨集群路由和故障恢复能力。

**注意事项**:  
- 确保集群间网络互通且证书配置正确。
- 避免过度复杂的流量规则，增加运维难度。

---

### 实践 7：性能优化与资源限制

**说明**:  
通过调整 Higress Gateway 的资源配置和连接参数，可显著提升吞吐量和降低延迟。

**实施步骤**:
1. 为 Gateway Pod 设置合理的 CPU/内存限制（如 `limits.cpu: "2"`）。
2. 调整连接池大小（如 `upstreamConnections`）。
3. 启用 HTTP/2 或 gRPC 优化长连接场景。
4. 使用压测工具（如 wrk）验证性能提升效果。

**注意事项**:  
- 资源限制需根据实际负载调整，避免 OOM。
- HTTP/2 需客户端和服务端均支持。

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/2 与 HTTP/3 (QUIC) 协议

**说明**: Higress 作为高性能网关，底层的网络协议对吞吐量和延迟影响巨大。HTTP/2 支持多路复用，解决了 HTTP/1.1 的队头阻塞问题；而 HTTP/3 (QUIC) 基于 UDP，在弱网环境下能显著减少连接建立延迟和丢包重传时间。

**实施方法**:
1. 在 Higress 的网关路由配置中，确保 Listener 协议设置为 HTTP/2。
2. 在网关参数配置中启用 QUIC 支持（需确保网络环境支持 UDP 流量）。
3. 配置客户端或 Upstream 服务端优先使用 HTTP/2 或 HTTP/3 进行通信。

**预期效果**: 在高并发或弱网环境下，请求建立连接的握手延迟可降低 30%-50%，单连接吞吐量提升，有效减少 TCP 连接数带来的资源消耗。

---

### 优化 2：配置全链路超时与连接池调优

**说明**: 默认的超时和连接池配置通常较为保守，无法适应高流量场景。若连接池过小，会导致请求在获取连接时排队等待（即“连接窃取”或“等待连接”），极大地增加 P99 延迟。

**实施方法**:
1. **调大连接池**：根据后端服务（Upstream）的处理能力，调整 `maxRequestsPerConnection` 和 `连接池大小`。例如，将连接数从默认的 1024 提升至 4096 或更高。
2. **精细化管理超时**：设置合理的 `connectTimeout`（连接超时）、`requestTimeout`（请求总超时）和 `streamIdleTimeout`（空闲超时）。避免超时时间过长导致线程积压。
3. 开启 `idleTimeout` 以便及时清理不活跃连接。

**预期效果**: 在高并发压测下，因连接等待导致的 P99 延迟可降低 20%-40%，显著提升网关的并发处理能力（QPS）。

---

### 优化 3：启用 QPS 限流与自适应熔断

**说明**: 当流量突增或下游服务出现故障时，若网关不做保护，会导致大量请求堆积，甚至拖垮整个网关实例。启用限流和熔断可以牺牲少量非核心流量，保证整体系统的稳定性。

**实施方法**:
1. **配置局部限流**：针对特定路由或 API 配置 QPS 阈值，使用 Token Bucket 算法进行精准限流。
2. **开启熔断器**：配置熔断规则（如连续错误 5 次或错误率超过 50%），触发熔断后直接返回预设的降级响应，而不是转发给后端。
3. 利用 Higress 的 Wasm 插件能力编写自定义的限流逻辑（如基于用户 ID 或 IP）。

**预期效果**: 在后端服务故障或流量洪峰时，网关自身的 CPU 和内存使用率保持稳定，防止雪崩效应，系统可用性（SLA）提升至 99.9% 以上。

---

### 优化 4：优化日志与可观测性采集策略

**说明**: 在高吞吐量场景下，全量日志打印和上报会消耗大量 CPU 和 I/O 资源，甚至成为性能瓶颈。默认的详细日志级别和每条请求的 Access Log 采集会显著降低吞吐量。

**实施方法**:
1. **调整日志级别**：将运行时日志级别从 `INFO` 调整为 `WARN` 或 `ERROR`。
2. **采样日志**：配置 Access Log 的采样率（例如仅采集 10% 或 1% 的流量日志），或者仅记录慢请求（例如耗时 > 500ms）的日志。
3. **异步上报**：确保日志和 Metrics 数据通过异步方式发送到远端（如 Prometheus、Loki），阻塞 I/O 操作。

**预期效果**: 网关 CPU 占用率可降低 10%-30%，QPS 吞吐量提升 15%-25

---
## 学习要点

- 基于提供的来源信息（GitHub Trending 上的 Alibaba/Higress），以下是关于该项目的关键要点总结：
- Higress 是阿里云开源的、基于 Envoy 和 Istio 构建的下一代云原生 API 网关，旨在解决云原生时代流量治理的复杂性问题。
- 它深度集成了 K8s Ingress 资源，支持作为标准 Ingress 控制器使用，实现了从传统微服务架构向 Service Mesh 架构的平滑过渡。
- 该项目提供了强大的 WAF（Web 应用防火墙）插件生态和安全防护能力，能够有效抵御 SQL 注入、XSS 等常见 Web 攻击。
- Higress 兼容 Nginx Ingress 注解及主流网关的配置习惯，显著降低了用户从 Nginx 或其他网关迁移的技术门槛和成本。
- 它支持高性能的流量管理，包括金丝雀发布、蓝绿部署和负载均衡策略，确保业务流量的灵活调度与高可用性。
- 通过将网关与 K8s 服务发现及 Nacos 等注册中心打通，实现了服务发现的自动化，简化了微服务间的通信管理。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础与核心概念

**学习内容**:
- 理解云原生网关的基本概念及其在现代微服务架构中的定位
- 了解 Higress 的背景：由阿里巴巴开源，基于 Envoy 和 Istio 构建
- 掌握 Higress 的核心术语：Ingress、网关实例、路由配置、服务来源
- 学习基本的流量管理概念：主机、路径、Header 匹配规则
- 了解 Higress 与 Nginx、传统 API 网关的区别与优势

**学习时间**: 1-2周

**学习资源**:
- Higress 官方 GitHub 仓库 README
- Higress 官方文档：什么是 Higress
- 阿里云云原生 API 网关相关产品介绍页

**学习建议**:
建议先通读官方文档，对网关的流量治理模型有一个宏观的认识。如果对 Kubernetes 不熟悉，需要先补充 K8s Ingress 的基础知识。

---

### 阶段 2：环境搭建与基础配置

**学习内容**:
- 学习如何在 Docker 本地环境或 Kubernetes 集群中部署 Higress
- 掌握 Higress 控制台的使用界面与操作
- 实践配置第一个路由：将 HTTP 请求转发到后端服务
- 学习如何配置服务来源，如 Nacos、Consul、固定地址（IP/域名）、K8s Service
- 理解并配置域名与路径的路由规则

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档：快速开始
- Higress 官方文档：部署指南
- Higress 官方文档：配置指南

**学习建议**:
动手是关键。建议使用 Docker Compose 在本地快速搭建一套环境，尝试部署一个简单的 Web 应用（如 Echo Server），并通过 Higress 暴露服务进行访问。

---

### 阶段 3：流量治理与安全防护

**学习内容**:
- 高级流量管理：基于 Header、Cookie、Query 参数的路由转发
- 金丝雀发布与蓝绿发布配置
- 负载均衡策略配置（轮询、随机、最小连接数等）
- 服务安全：配置 Basic Auth、JWT 认证、IP 黑白名单访问控制
- 流量防护：配置全局限流和并发限流
- 插件系统入门：使用 Wasm 插件扩展功能（如请求/响应头修改）

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档：流量管理
- Higress 官方文档：安全防护
- Higress 官方插件市场

**学习建议**:
结合实际业务场景思考。例如，模拟一个需要灰度发布的场景，配置流量按百分比切流；或者模拟高并发场景，测试限流配置是否生效。

---

### 阶段 4：生态集成与插件开发

**学习内容**:
- 深入理解 Higress 的插件架构（基于 Wasm 和 Go/C++）
- 学习如何编写自定义 Wasm 插件（Go 语言为主）
- 集成服务发现：深度整合 Nacos、Zookeeper、Eureka 等注册中心
- 集成 Prometheus 与 Grafana 进行监控指标观测
- 集成 SkyWalking/Zipkin 进行分布式链路追踪
- Higress 在高可用场景下的部署与性能调优

**学习时间**: 4-6周

**学习资源**:
- Higress 官方文档：自定义开发
- Higress 官方文档：可观测性
- Higress GitHub 仓库中的插件源码示例
- Envoy Wasm 官方开发文档

**学习建议**:
尝试编写一个简单的自定义插件，例如实现一个特定的请求校验逻辑或请求体修改逻辑。同时，关注网关的性能指标，了解如何通过配置 Envoy 的底层参数来优化性能。

---

### 阶段 5：架构设计与源码研读

**学习内容**:
- Higress 在大型企业级微服务架构中的最佳实践与拓扑设计
- 深入研读 Higress 源码：控制面与数据面的交互机制
- 理解 Higress 如何基于 Istio 进行 Gateway 的定制化改造
- 多集群管理与服务网格的深度集成方案
- 参与社区贡献：提交 Issue、PR 或优化文档

**学习时间**: 持续学习

**学习资源**:
- Higress GitHub 源码
- Higress 官方博客与架构设计文章
- Istio 官方文档
- Envoy 官方文档

**学习建议**:
阅读源码是通往专家的必经之路。建议从核心的 Router 组件和插件加载机制入手，调试运行 Higress 的源码环境，观察数据包在网关内部的流转过程。

---
## 常见问题


### 1: Higress 是什么？它与 Nginx 和 Kong 有什么区别？

1: Higress 是什么？它与 Nginx 和 Kong 有什么区别？

**A**: Higress 是一款基于阿里云内部多年实践，开源的云原生 API 网关。它是在 Envoy 和 Istio 的基础上构建的，旨在解决云原生架构下的流量管理问题。

与 Nginx 相比，Higress 更侧重于云原生和微服务场景，支持 Kubernetes Ingress、服务发现以及更丰富的流量治理功能（如金丝雀发布、全链路灰度），且配置方式更加动态化，不需要像 Nginx 那样频繁 Reload。

与 Kong 相比，Higress 的底层基于 Envoy（C++ 高性能），而 Kong 基于 OpenResty（Lua）。Higress 在处理长连接、高并发下的性能表现通常更优，且与 Istio 的控制平面集成更加原生，适合作为服务网格中的南北向流量网关。

---



### 2: Higress 是否兼容 Nginx 的配置或 Ingress 资源？

2: Higress 是否兼容 Nginx 的配置或 Ingress 资源？

**A**: 是的，Higress 具有很强的兼容性。

1.  **Kubernetes Ingress**: Higress 完全支持标准的 Kubernetes Ingress API，可以直接替换集群中的 Nginx Ingress Controller，无需修改现有的 Ingress 资源文件即可生效。
2.  **Nginx 配置**: 虽然 Higress 不直接读取 `nginx.conf`，但它支持通过控制台或 CRD（自定义资源）配置路由规则。对于从 Nginx 迁移的用户，Higress 提供了 Nginx 配置迁移工具，可以帮助用户将 Nginx 的 location 和 upstream 配置逻辑转换为 Higress 的路由配置。

---



### 3: 如何在 Higress 中集成 Dubbo 或 gRPC 服务？

3: 如何在 Higress 中集成 Dubbo 或 gRPC 服务？

**A**: Higress 对微服务协议有非常深入的支持，特别是针对阿里生态常用的 Dubbo 和云原生通用的 gRPC。

1.  **Dubbo**: Higress 原生支持 Dubbo 协议（包括 Dubbo2 和 Dubbo3）。它可以将 HTTP/HTTPS 请求转换为 Dubbo 协议调用，实现 HTTP 到 Dubbo 的服务透传。这使得前端应用可以直接通过 HTTP 调用后端的 Dubbo 服务，无需额外的适配层。
2.  **gRPC**: Higress 原生支持 gRPC 协议代理和 JSON 到 gRPC 的转码功能。你可以配置路由将 HTTP/JSON 请求转发给后端的 gRPC 服务，也可以直接透传 gRPC 流量。

---



### 4: Higress 的插件机制是如何工作的？支持 WAF 吗？

4: Higress 的插件机制是如何工作的？支持 WAF 吗？

**A**: Higress 采用了插件化设计，允许用户在网关层执行自定义逻辑。

1.  **插件类型**: Higress 支持 Lua（兼容 OpenResty）和 Wasm（WebAssembly）两种插件开发方式。Wasm 是 Higress 重点推荐的方向，因为它具有高性能、沙箱隔离和多语言支持（C++, Go, Rust, Python 等）的优点。
2.  **WAF 支持**: Higress 自带了一些基础的安全防护能力，并且官方提供了 WAF 插件（通常基于 ModSecurity 规则或类似逻辑）。用户可以通过插件市场一键安装 WAF 插件，或者通过编写 Wasm 插件来实现自定义的防火墙规则、IP 访问控制和限流熔断。

---



### 5: Higress 如何保证高可用性和性能？

5: Higress 如何保证高可用性和性能？

**A**: Higress 在架构设计上充分考虑了高性能和高可用：

1.  **底层引擎**: 数据面基于 Envoy，采用 C++ 编写，具有极高的吞吐量和极低的延迟，异步非阻塞 I/O 模型使其能够轻松应对 C10M（千万级并发）问题。
2.  **水平扩展**: 作为 Kubernetes Ingress Controller，Higress 可以通过调整副本数轻松实现水平扩容。结合 HPA（Horizontal Pod Autoscaler），可以根据流量自动调整实例数量。
3.  **热更新**: 配置的修改通过控制平面下发给数据面，Envoy 支持 xDS 协议的热更新，配置变更不需要重启进程，从而做到业务无感。

---



### 6: Higress 与 Istio 是什么关系？必须配合 Istio 使用吗？

6: Higress 与 Istio 是什么关系？必须配合 Istio 使用吗？

**A**: Higress 与 Istio 关系密切，但**不是**强绑定关系。

1.  **独立使用**: Higress 可以作为一个独立的 API 网关或 Kubernetes Ingress Controller 部署，直接接管集群的南北向流量，无需安装 Istio。
2.  **结合使用**: 在已经部署了 Istio 的服务网格中，Higress 可以作为 Istio 的**入口网关**。相比 Istio 默认的 Ingress Gateway，Higress 提供了更友好的控制台、更强的协议转换能力（如 HTTP 转 Dubbo）和更丰富的插件市场。它复用了 Istio 的控制平面能力，但增强了数据面的功能。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 基于 Higress 的官方 Docker 镜像，如何在本地快速启动一个 Standalone 模式的网关，并配置一个简单的路由规则，将访问 `/hello` 的流量转发到后端的 HTTPBin 测试服务？

### 提示**:

### 需要查阅 Higress 的 Docker Hub 或官方文档中的 `docker run` 启动参数。

---
## 实践建议

基于 Higress 作为 "AI Native API Gateway" 的定位，结合其基于 Istio 和 Envoy 的技术架构，以下是 6 条针对实际生产环境的实践建议：

### 1. 利用 AI 插件生态实现零代码集成
Higress 的核心优势在于其内置的 AI 插件市场（如 LLM 路由、Prompt 模板管理、Token 计数等）。
*   **实践建议**：不要将 AI 逻辑硬编码到业务后端中。直接在 Higress 控制台配置 `ai-proxy` 或 `ai-statistics` 插件。
*   **具体操作**：使用 **路由配置** 将不同路径（如 `/v1/chat/gpt4` 和 `/v1/chat/claude`）指向同一个后端服务，但在网关层通过插件动态修改请求头或 Host，从而实现多模型统一接入。
*   **常见陷阱**：在插件中处理耗时逻辑（如超长 Prompt 的实时组装），这会阻塞网关线程。建议将复杂的 Prompt 工程逻辑放在业务侧，网关仅负责路由和简单的 Key/Header 转换。

### 2. 配置模型提供商的 fallback 与降级策略
大模型 API（如 OpenAI 或 Azure OpenAI）经常出现不稳定或限流的情况。
*   **实践建议**：利用 Higress 的 **服务来源** 和 **高可用路由** 能力。
*   **具体操作**：配置多个服务来源（例如，同时配置 OpenAI 官方 API 和一个 Azure OpenAI 的代理端点）。在路由规则中设置自动重试和故障转移，当主提供商返回 429 (Rate Limit) 或 503 时，网关自动切换到备用提供商，对客户端透明。
*   **常见陷阱**：未针对 AI 流量设置合理的超时时间。AI 请求（流式响应）通常比普通 HTTP 请求耗时更长，需将路由的超时设置调整为 60s 甚至更高，并开启对后端的长连接支持。

### 3. 实施细粒度的 Token 与成本控制
AI API 的调用成本主要取决于 Token 消耗量。
*   **实践建议**：启用 Higress 的 **Token 限流** 功能，而非传统的 QPS 限流。
*   **具体操作**：配置针对 API Key 或用户的 Token 速率限制（例如：每分钟最多消耗 10,000 个 Token）。结合 `ai-statistics` 插件，实时监控不同租户的 Token 消耗，防止恶意用户通过发送超长 Prompt 造成成本失控。
*   **常见陷阱**：仅限制并发连接数。由于流式请求连接占用时间长，连接数无法准确反映实际资源消耗，必须基于 Token 或 Request Count 进行限流。

### 4. 谨慎处理 SSE (Server-Sent Events) 流式响应
AI 对话通常采用 SSE 协议进行流式返回，这对网关的缓冲处理有特殊要求。
*   **实践建议**：确保网关在流式转发模式下不进行全量缓冲。
*   **具体操作**：在 Wasm 插件或路由配置中，明确开启流式转发模式。检查 Higress 的日志采样策略，确保对于 SSE 请求，日志记录的是元数据而非完整的响应 Body，否则会导致磁盘写入量激增和网关性能下降。
*   **常见陷阱**：在 SSE 响应路径上添加了修改 Body 的插件（如某些 JSON 替换插件），这可能导致流被中断或格式错乱。仅对 SSE 请求使用不修改响应体的插件。

### 5. 建立基于语义的鉴权与安全防护
传统的 API 网关主要防御 SQL 注入或 DDoS，AI 网关需要防御 Prompt 注入。
*   **实践建议**：使用 Higress 的 Wasm 插件能力集成内容安全检测。
*   **具体操作**：在请求发送给 LLM 之前，挂载一个轻量级的安全检查插件（可以是本地模型或调用审核 API），检查 `messages` 字段中是否包含敏感词或 Prompt 攻击特征。如果检测

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI 原生](/tags/ai-%E5%8E%9F%E7%94%9F/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [LLM](/tags/llm/) / [MCP](/tags/mcp/) / [Kubernetes](/tags/kubernetes/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260130-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260201-github_trending-alibaba-higress-8.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*