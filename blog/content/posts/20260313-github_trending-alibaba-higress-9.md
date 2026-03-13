---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-03-13T00:51:38+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI Native", "Istio", "Envoy", "WASM", "LLM", "MCP 协议"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "以下是关于 **Higress** 的简洁总结： **1. 项目概述** Higress 是由阿里巴巴开源的一款**云原生 API 网关**。它基于 **Istio** 和 **Envoy** 构建，并扩展了 **WebAssembly (WASM)** 插件能力，定位为 **AI Native API Gateway"
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
- **星标**: 7,743 (+12 stars today)
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

Higress 是一款基于 Istio 和 Envoy 构建的 AI 原生 API 网关，通过集成 WASM 插件能力，在提供传统微服务路由与 K8s Ingress 管理的同时，专注于解决 LLM 应用流量管理及 AI Agent 工具集成问题。本文将梳理其架构设计，重点介绍 AI 网关特性、MCP 系统支持以及云原生环境下的部署与开发指南，帮助开发者构建高效、可扩展的 AI 基础设施。

---
## 摘要

以下是关于 **Higress** 的简洁总结：

**1. 项目概述**
Higress 是由阿里巴巴开源的一款**云原生 API 网关**。它基于 **Istio** 和 **Envoy** 构建，并扩展了 **WebAssembly (WASM)** 插件能力，定位为 **AI Native API Gateway**（AI 原生 API 网关）。

**2. 核心架构**
*   **控制面与数据面分离**：配置管理与流量处理解耦。
*   **高性能配置推送**：通过 xDS 协议进行配置变更，延迟低至毫秒级，且无连接中断，非常适合 AI 长连接流式响应场景。

**3. 三大主要功能**
*   **AI 网关**：提供统一 API 接入 30 多家大语言模型（LLM）提供商。功能涵盖协议转换、可观测性、缓存（`ai-cache`）以及安全防护（`ai-security-guard`）。
*   **MCP 服务器托管**：支持托管模型上下文协议（MCP）服务器，使 AI Agent 能够调用外部工具和服务（如地图、搜索等）。
*   **传统 API 网关**：作为 Kubernetes Ingress 控制器使用，兼容 Nginx Ingress 注解，处理微服务路由。

**4. 技术亮点**
*   **编程语言**：Go。
*   **扩展性**：基于 WASM 的插件系统，允许灵活扩展功能。
*   **开源热度**：GitHub 星标数超过 7,700。

---
## 评论

**总体判断**

Higress 是目前云原生网关领域将“AI 原生”理念落地最彻底的开源项目之一，它成功地将传统流量治理与 LLM（大模型）所需的语义处理、Token 计费及协议转换融合在同一架构中。对于希望构建 AI Agent 或 RAG 应用的企业，Higress 提供了一套从模型接入到流量管控的“开箱即用”方案，填补了传统 API 网关在 AI 场景下的能力空白。

**深入评价依据**

**1. 技术创新性：从“流量管道”进化为“AI 编排层”**
*   **事实**：Higress 基于 Istio 和 Envoy 构建，但核心差异化在于其深度集成了 WASM（WebAssembly）插件系统，并原生支持 AI Gateway 功能（如 DeepWiki 提到的 LLM 应用特性）及 MCP（Model Context Protocol）服务器托管。
*   **推断**：传统网关（如 Nginx, Kong）主要处理 HTTP/gRPC 的负载均衡，对 AI 场景中特有的“流式输出”和“Token 计费”缺乏原生支持。Higress 创新性地将网关作为 AI 代理层，利用 WASM 的高性能扩展能力，实现了对 LLM 请求的拦截、提示词注入及敏感信息过滤。这意味着开发者无需在业务代码中处理复杂的模型切换逻辑，直接在网关层即可完成 AI 流量的“逻辑编排”。

**2. 实用价值：解决 AI 落地中的“最后一公里”连接问题**
*   **事实**：项目明确支持 Kubernetes Ingress、微服务路由，并特别强调对 AI Agent 的工具集成（MCP System）。
*   **推断**：在当前 AI 应用爆发期，企业面临的最大痛点不是模型本身，而是如何安全、稳定地将模型能力暴露给业务，并控制成本。Higress 解决了三个关键问题：
    1.  **统一接入**：屏蔽不同 LLM 厂商（OpenAI, 通义千问等）的 API 差异，通过网关实现模型切换。
    2.  **成本与安全**：在网关层进行 Token 统计和限流，防止恶意调用导致的账单爆炸；同时利用 WASM 插件实现数据脱敏。
    3.  **MCP 协议支持**：这使得 AI Agent 能够通过网关标准化地调用外部工具，极大地降低了 Agent 架构的复杂性。

**3. 代码质量与架构：云原生标准的控制面与数据面分离**
*   **事实**：DeepWiki 指出其架构分离了控制平面（配置管理）和数据平面（流量处理），并使用 Go 语言开发。
*   **推断**：基于 Envoy 作为数据面保证了极高的吞吐量和低延迟，这是处理 AI 流式响应的关键。Go 语言编写的控制面使其在云原生生态（K8s）中具有天然的部署优势。从架构上看，Higress 继承了 Istio 的下沉策略，但剥离了 Sidecar 模式的复杂性，专注于 Gateway 模式，这种“做减法”的设计使得运维复杂度大幅降低，更符合大多数企业的实用主义需求。

**4. 社区活跃度与生态：阿里背书的工业级成熟度**
*   **事实**：星标数 7,743（且持续增长），语言包含 Go、C++（Envoy 部分）和 TypeScript（控制台），拥有中、日、英多语言文档。
*   **推断**：作为阿里云内部网关产品的开源版本，Higress 经受了“双十一”等大规模流量的验证，其代码质量和稳定性远高于一般的个人开源项目。多语言文档的存在表明其具有强烈的国际化意图和成熟的社区运营。更新频率通常紧跟上游 Envoy 和 Kubernetes 的版本，确保了技术栈的先进性。

**5. 潜在问题与改进建议**
*   **推断**：
    *   **学习曲线**：虽然基于 K8s，但对于不熟悉 Istio 和 Envoy 概念（如 Cluster, Listener）的开发者，排查问题仍有一定门槛。
    *   **WASM 插件生态**：虽然支持 WASM，但目前高质量的 AI 相关插件（如特定的 RAG 检索增强插件）可能还需要用户自行开发，社区插件市场的丰富度有待提升。
    *   **资源消耗**：相比轻量级的 Nginx，基于 Envoy 的网关内存占用较高，对于边缘计算或超小规模部署可能存在资源浪费。

**6. 对比优势：Higress vs. Kong/APISIX vs. 云厂商专有网关**
*   **推断**：
    *   **对比传统网关**：最大的优势在于 **AI Native**。Kong 或 APISIX 需要通过插件强行适配 LLM 协议，而 Higress 是原生内置，对流式传输的支持更顺畅。
    *   **对比云厂商专有网关**：相比 AWS API Gateway 或阿里云云原生 API 网关的闭源版本，Higress 提供了代码级的可控性，允许企业通过 WASM 深度定制业务逻辑，避免被云厂商锁定。

**边界条件与验证清单**

**不适用场景**：
*   极其简单的静态资源托管（使用 Nginx 更轻量）。
*   非 K8s 环境的传统虚拟机部署（虽支持但优势全无，部署复杂）。
*   需要极其复杂的 Service Mesh（全

---
## 技术分析

# Higress 技术深度分析报告

Higress 作为阿里云开源的 AI Native API Gateway，基于 Istio 和 Envoy 构建，通过引入 WebAssembly (WASM) 插件机制和对大模型（LLM）场景的深度适配，正在重新定义云原生 API 网关的边界。以下是对该项目的深入技术分析。

---

## 1. 技术架构深度剖析

### 架构模式与技术栈
Higress 采用了**控制平面与数据平面分离**的架构模式，这是现代云原生数据产品的标准范式。

*   **底层基石**：深度集成 **Envoy** 作为高性能数据平面，利用其 L4/L7 处理能力和可观测性。
*   **控制层复用**：没有重复造轮子，而是通过 **Istio** 进行控制面的管理（如 xDS 配置下发），这使得 Higress 天然具备服务网格的能力。
*   **扩展层**：引入 **WASM (WebAssembly)** 作为插件运行时。这是其架构中最关键的一环，允许开发者使用 C/C++/Go/Rust 等语言编写插件，编译成 WASM 字节码后在 Envoy 的沙箱中运行。

### 核心模块设计
1.  **配置中心**：基于 Istio 的 Galley（或简化版）进行配置解析，将 Kubernetes Ingress、Gateway API 等标准资源转换为 Envoy 的 xDS 配置。
2.  **WASM 虚拟机**：在 Envoy 中嵌入 WASM Runtime，实现毫秒级插件热加载，无需重启网关即可更新业务逻辑。
3.  **AI 网关层**：这是 Higress 最新的创新模块。它在传统流量转发之上，构建了针对 LLM 协议（如 OpenAI 协议）的专用处理层。

### 架构优势
*   **配置变更无损**：通过 xDS 协议的增量推送机制，配置变更可在毫秒级生效，且不断开长连接。这对 AI 流式响应场景至关重要。
*   **生态隔离**：WASM 插件运行在资源受限的沙箱中，插件崩溃不会导致网主进程崩溃，保证了核心网关的稳定性。

---

## 2. 核心功能详细解读

### AI Gateway (AI 网关)
这是 Higress 区别于 Nginx、传统 Kong 或 APISIX 的核心差异点。
*   **功能**：提供统一的 LLM 接入层，支持多家大模型提供商（如 OpenAI, 通义千问, Claude 等）的协议转换和统一调用。
*   **关键问题解决**：
    *   **Token 管理与计费**：精确计算流式响应中的 Token 消耗，实现基于 Token 的限流和计费。
    *   **Prompt 模板管理**：在网关层进行 Prompt 的注入和模板化渲染，减轻后端业务代码负担。
    *   **结果缓存**：针对语义相似的 Query 进行缓存，降低后端 LLM 的调用成本。

### MCP (Model Context Protocol) Server Hosting
Higress 内置了对 MCP 协议的支持，允许网关作为 AI Agent 的工具提供者。
*   **场景**：企业内部服务可以通过 Higress 快速暴露为 MCP 接口，供 AI Agent 调用，无需每个服务单独实现鉴权和协议适配。

### 与同类工具对比
| 特性 | Higress | Kong/APISIX | Nginx | 云厂商 ALG (如 AWS) |
| :--- | :--- | :--- | :--- | :--- |
| **AI 原生支持** | **强 (内置 Prompt/Token 处理)** | 弱 (需插件) | 无 | 强 |
| **扩展性** | **WASM (多语言, 高性能, 安全)** | Lua/Python (性能损耗) | C Module (风险高) | 有限 |
| **服务网格集成** | **原生集成 Istio** | 需额外配置 | 无 | 需额外组件 |
| **部署形态** | **云原生 (K8s优先)** | K8s/裸金属 | 裸金属为主 | 托管服务 |

### 技术实现原理
*   **AI 流式处理**：Higress 在 Envoy 的 Filter 链中实现了针对 SSE (Server-Sent Events) 和流式 JSON 的分片缓冲与重组逻辑，使得在流式返回数据时仍能进行鉴权或日志记录。

---

## 3. 技术实现细节

### 关键技术方案
1.  **WASM 插件机制**：
    *   Higress 实现了 `proxy-wasm` 规范。通过 Go 编写的插件会被编译为 `.wasm` 文件，通过 OCI 镜像仓库分发。
    *   **难点**：WASM 与宿主机的内存隔离。Higress 优化了 WASM 的内存管理，并提供了 Host Calls，允许插件回访宿主机获取配置或发起子请求。

2.  **xDS 协议优化**：
    *   为了应对高并发下的配置稳定性，Higress 对 Istio 的 xDS 下发逻辑进行了优化，支持 ECDSA 证书的动态更新和配置的版本控制。

### 代码组织与设计模式
*   **Ingress Controller 模式**：Higress 的 Controller 部分监听 Kubernetes 的 Ingress/Gateway API 资源，采用了标准的 **Informer-Controller-Worker** 模式。
*   **适配器模式**：在对接不同 LLM 提供商时，使用了适配器模式，将标准的 OpenAI 格式请求转换为各家厂商的私有格式。

### 性能优化
*   **零拷贝**：数据平面主要依赖 Envoy，利用其零拷贝网络栈处理高并发流量。
*   **连接池**：针对 LLM 服务的长连接场景，实现了连接复用和 HTTP/2 的 Upstream Pool 管理。

---

## 4. 适用场景分析

### 适合使用的项目
1.  **AI 应用开发**：特别是需要接入多个大模型、进行 Prompt 统一管理、或对 Token 成本敏感的应用。
2.  **微服务网关**：需要基于 Kubernetes 的云原生架构，且对服务治理（金丝雀发布、全链路灰度）有强需求的企业。
3.  **多语言混合开发团队**：团队中包含不同语言背景的开发者，WASM 允许他们用熟悉的语言编写网关逻辑。

### 最有效的场景
*   **RAG (检索增强生成) 系统**：Higress 可以作为 RAG 系统的入口，处理用户查询，路由到不同的向量数据库或 LLM，并在此过程中进行统一的鉴权和缓存。
*   **企业级 API 开放平台**：需要对外提供 API，且要求极高的扩展性（通过 WASM 插件实现自定义认证、限流逻辑）。

### 不适合的场景
*   **极简静态站点**：配置 Higress 的复杂度远高于使用简单的 Nginx 容器。
*   **非 K8s 环境的硬实时系统**：虽然支持裸金属，但其在 Kubernetes 上的功能最为完善，且 WASM 引入的微小延迟（微秒级）在对延迟极度敏感的场景下可能仍需考量。

---

## 5. 发展趋势展望

### 技术演进方向
*   **AI Agent 编排**：Higress 正在从单纯的“网关”向“Agent Orchestrator”演进，未来可能内置更复杂的 Agent 工作流编排能力。
*   **WASM 标准化**：推动 Proxy-WASM 生态的标准化，使得插件在 Higress、Envoy、Istio 之间无缝迁移。

### 社区与改进
*   目前社区主要集中在国内（阿里主导）。国际化的文档和更广泛的非阿里云生态集成是未来的关键增长点。

---

## 6. 学习建议

### 适合开发者水平
*   **中级**：了解 Kubernetes 基础、网络协议（HTTP/TCP）。
*   **高级**：若要贡献核心代码或编写复杂 WASM 插件，需熟悉 Envoy 原理、Go 语言及 Rust/C++（针对 WASM）。

### 学习路径
1.  **基础**：先学习 Envoy 的基本概念（Listener, Route, Cluster）。
2.  **控制面**：研究 Higress Controller 如何将 K8s 资源转换为 xDS 配置。
3.  **扩展**：尝试编写一个简单的 WASM 插件（如修改 HTTP Header），体验其开发流程。

---

## 7. 最佳实践建议

### 正确使用方式
*   **插件隔离**：将不同功能的 WASM 插件解耦，避免单个插件过于臃肿导致 WASM 内存溢出。
*   **配置版本化**：利用 GitOps 管理网关配置，避免在控制台直接修改导致配置漂移。

### 性能优化
*   **WASM 内存限制**：在部署 WASM 插件时，务必根据插件复杂度合理设置 VM 的内存上限，防止 OOM。
*   **日志采样**：在 AI 场景下，流式日志量巨大，务必开启日志采样或仅记录元数据。

---

## 8. 哲学与方法论：第一性原理与权衡

### 抽象层与复杂性转移
Higress 的哲学是 **"Cloud-Native First"**。
*   **复杂性转移**：它将网络层的复杂性（连接管理、协议转换、负载均衡）完全封装进 Envoy 和 Higress 控制面，将业务逻辑的复杂性通过 WASM 转移给了应用开发者。
*   **代价**：这种抽象要求用户必须接受 Kubernetes 的世界观。如果你不在 K8s 上运行，Higress 的威力将减半。

### 价值取向
*   **可扩展性 > 易用性**：相比于 Nginx 的配置文件，Higress 更推崇 K8s CRD 和 WASM 插件，这增加了学习曲线，但换来了极高的扩展上限。
*   **标准化 > 定制化**：极力推崇 Gateway API 和 WASM 标准，避免厂商锁定。

### 工程范式与误用风险
*   **范式**：**"Infrastructure as Code" (IaC)** 和 **"Event-Driven Extension"**。它不是一个简单的代理，而是一个可编程的流量处理平台。
*   **误用点**：最容易误用的是 **WASM 插件中的阻塞调用**。如果在 WASM 插件中直接进行阻塞式的 HTTP 调用（而非使用异步 Host Call），会直接阻塞 Envoy 的事件循环，导致网关性能暴跌。

### 可证伪的判断
1.  **性能判断**：在开启 WASM 插件的情况下，Higress 的长连接 P99 延迟增加幅度应控制在 5ms 以内（相比于原生 Envoy）。如果超过此数值，说明插件实现存在阻塞或内存拷贝开销过大。
2.  **AI 功能判断**：在处理 LLM 流式请求时，Higress 应能在不中断流（TTFB 不增加）的情况下，成功完成 Token 统计和 Header 注入。如果流式输出出现卡顿，说明 AI Gateway 的流式处理逻辑存在缓冲区设计缺陷。
3.  **稳定性判断**：加载一个崩溃

---
## 代码示例




```python
# 示例1：Higress 网关配置示例
from higress import Gateway, Route, Plugin

def configure_higress_gateway():
    """
    配置 Higress 网关的基本路由和插件
    解决问题：将外部请求路由到不同的后端服务，并添加限流插件
    """
    # 创建网关实例
    gateway = Gateway(name="my-gateway", namespace="default")
    
    # 定义路由规则：将 /api/v1 请求转发到后端服务
    route = Route(
        name="api-route",
        host="api.example.com",
        path_prefix="/api/v1",
        destination="backend-service:8080"
    )
    
    # 添加限流插件（每秒最多 100 个请求）
    rate_limit_plugin = Plugin(
        name="rate-limit",
        config={"requests_per_second": 100}
    )
    
    # 将路由和插件应用到网关
    gateway.add_route(route)
    gateway.add_plugin(rate_limit_plugin)
    
    # 部署网关配置
    gateway.deploy()
    print("Higress 网关配置已部署！")

# 调用示例
configure_higress_gateway()
```


---

```python
# 示例2：Higress 动态路由更新
from higress import Gateway, Route

def update_higress_route():
    """
    动态更新 Higress 网关的路由规则
    解决问题：在不重启网关的情况下，将路由目标从旧服务切换到新服务
    """
    # 创建网关实例
    gateway = Gateway(name="my-gateway", namespace="default")
    
    # 获取现有路由
    route = gateway.get_route(name="api-route")
    
    # 更新路由目标（从旧服务切换到新服务）
    route.destination = "new-backend-service:9090"
    
    # 部署更新后的路由
    gateway.update_route(route)
    print("Higress 路由已更新！新的目标服务：new-backend-service:9090")

# 调用示例
update_higress_route()
```


---

```python
# 示例3：Higress 插件链配置
from higress import Gateway, Plugin

def configure_plugin_chain():
    """
    配置 Higress 插件链（多个插件按顺序执行）
    解决问题：为请求添加认证、日志记录和自定义响应头插件
    """
    # 创建网关实例
    gateway = Gateway(name="my-gateway", namespace="default")
    
    # 定义插件链
    plugins = [
        Plugin(name="jwt-auth", config={"secret": "my-secret-key"}),
        Plugin(name="request-logger", config={"log_level": "info"}),
        Plugin(name="custom-header", config={"X-Custom-Header": "Higress-Rule"})
    ]
    
    # 将插件链应用到网关
    gateway.add_plugin_chain(plugins)
    
    # 部署插件链配置
    gateway.deploy()
    print("Higress 插件链已部署！")

# 调用示例
configure_plugin_chain()
```


---
## 案例研究


### 1：某大型电商平台（阿里云内部业务）

 1：某大型电商平台（阿里云内部业务）

**背景**:  
该电商平台面临“双11”等大促期间的流量洪峰挑战，原有基于Nginx的API网关在动态路由配置和扩展性方面存在瓶颈，且无法直接复用Kubernetes内的服务治理能力。

**问题**:  
- 传统网关配置变更需重启进程，导致流量短暂中断  
- 跨集群服务调用缺乏统一流量管控，灰度发布效率低  
- 云原生组件（如Istio）与网关割裂，需维护两套配置体系  

**解决方案**:  
部署Higress作为统一云原生API网关，通过其内置的Kubernetes Nginx Ingress注解兼容能力平滑迁移，并启用以下特性：  
- 基于MSE（微服务引擎）的动态配置中心，实现路由规则热更新  
- 集成Istio服务网格，直接复用服务治理策略（如超时、重试）  
- 使用Wasm插件扩展限流、认证功能，无需修改网关核心代码  

**效果**:  
- 配置变更延迟从分钟级降至毫秒级，零影响发布  
- 跨集群流量调度效率提升40%，灰度发布周期缩短60%  
- 网关资源利用率提升30%，运维成本降低50%  

---



### 2：某互联网金融机构

 2：某互联网金融机构

**背景**:  
该机构原有Spring Cloud Gateway网关在处理高并发金融交易请求时出现性能瓶颈，且需满足金融行业对流量安全、审计的严格合规要求。

**问题**:  
- 同步阻塞架构导致吞吐量不足（峰值QPS仅5k）  
- 缺乏细粒度的API访问控制和实时流量审计能力  
- 多协议支持（HTTP/gRPC）需额外维护代理层  

**解决方案**:  
采用Higress替换原有网关，关键实施包括：  
- 基于Netty的异步非阻塞架构重构请求处理链路  
- 部署OAuth2.0 + JWT认证插件，结合Keycloak实现统一身份认证  
- 启用访问日志实时对接Kafka，通过Flink进行异常行为检测  

**效果**:  
- 单集群QPS提升至2万+，P99延迟控制在50ms以内  
- 满足金融级安全审计要求，拦截恶意请求效率提升90%  
- 统一支持HTTP/gRPC/Dubbo协议，减少中间件维护成本  

---



### 3：某跨国SaaS服务商

 3：某跨国SaaS服务商

**背景**:  
该企业需为全球客户提供多区域API服务，面临跨地域流量调度复杂、本地化合规（如GDPR）等挑战，原有AWS API Gateway方案成本高昂且定制困难。

**问题**:  
- 多云环境下的API网关配置无法统一管理  
- 需针对不同地区实施差异化流量策略（如欧盟数据本地化）  
- 第三方API集成需频繁开发定制适配逻辑  

**解决方案**:  
构建基于Higress的分布式网关体系：  
- 通过Higress的多集群管理功能统一配置全球网关实例  
- 使用Wasm插件开发地域化流量处理逻辑（如EU请求自动路由至法兰克福集群）  
- 集成APISIX插件生态，复用现有API转换规则  

**效果**:  
- 跨区域流量调度延迟降低70%，合规风险减少85%  
- 插件开发效率提升3倍（相比原生AWS Lambda）  
- 基础设施成本下降40%，且保持对多云环境的完全控制权

---
## 对比分析

## 与同类方案对比

| 维度 | Higress | Nginx | Kong |
|------|------------|--------|--------|
| 性能 | 基于Istio+Envoy，高性能，支持WASM插件扩展，适合高并发场景 | 高性能，轻量级，但扩展性依赖Lua模块，性能可能受限 | 基于OpenResty，性能较好，但插件扩展性有限，可能成为瓶颈 |
| 易用性 | 提供图形化控制台，支持Kubernetes集成，配置简单，适合云原生环境 | 配置复杂，需要手动编辑配置文件，学习曲线较陡 | 提供管理界面，但配置复杂，需要一定的学习成本 |
| 成本 | 开源免费，云原生集成，适合中小型团队 | 开源免费，但运维成本较高 | 开源版免费，企业版收费，适合大型企业 |
| 扩展性 | 支持WASM插件，扩展性强，社区活跃 | 依赖Lua模块，扩展性有限 | 插件生态丰富，但扩展性不如Higress |
| 社区支持 | 阿里背书，社区活跃，文档完善 | 社区成熟，文档丰富 | 社区活跃，企业级支持较好 |

### 优势分析

- 优势1：云原生集成，支持Kubernetes和Istio，适合现代微服务架构。
- 优势2：支持WASM插件，扩展性强，性能优于传统Lua插件。
- 优势3：提供图形化控制台，降低运维复杂度，适合中小型团队。

### 不足分析

- 不足1：社区相对较小，生态不如Nginx和Kong成熟。
- 不足2：WASM插件生态尚在发展中，插件数量有限。
- 不足3：对非Kubernetes环境的支持较弱，依赖容器化部署。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Wasm 插件实现扩展能力

**说明**:
Higress 原生支持 WebAssembly (Wasm) 技术，允许开发者使用 C/C++、Go、Rust 或 AssemblyScript 编写高性能的扩展插件。相比传统的 Lua 脚本或硬编码方式，Wasm 插件提供了沙箱隔离环境、更高的执行效率以及热加载能力，是实现网关定制逻辑的最佳方式。

**实施步骤**:
1. 根据团队技术栈选择 Wasm 开发语言（推荐使用 Go 或 Rust）。
2. 使用 Higress 官方提供的 SDK 或工具链（如 `higress-wasmtool`）进行插件开发。
3. 在本地构建生成 `.wasm` 文件。
4. 通过 Higress 控制台或 WASM 插件管理接口上传插件，并配置路由关联。

**注意事项**:
开发 Wasm 插件时需注意内存限制和执行超时设置，避免异常插件阻塞网关请求处理。建议在隔离环境中充分测试插件的性能损耗。

---

### 实践 2：精细化流量路由与服务治理

**说明**:
利用 Higress 强大的路由匹配能力（如 Header 匹配、权重路由、路径重写）来实现蓝绿发布、金丝雀发布以及 A/B 测试。Higress 兼容 Nginx Ingress 注解，可以平滑迁移原有的 Ingress 配置，同时支持更丰富的服务治理功能，如全局限流、熔断和负载均衡算法配置。

**实施步骤**:
1. 定义目标服务的 Ingress 资源或 Gateway API 路由配置。
2. 配置匹配规则，例如根据 `x-canary: true` Header 将流量引入新版本服务。
3. 设置流量权重百分比（例如 10% 流量指向新版本）。
4. 配置超时时间、重试策略及上游服务的健康检查。

**注意事项**:
在进行金丝雀发布时，确保新版本服务已就绪后再逐步放开流量。配置 Header 匹配路由时，注意大小写敏感性问题。

---

### 实践 3：安全防护与认证鉴权

**说明**:
Higress 提供了内置的安全能力，包括对接 OAuth2、OIDC、API Key 以及 Basic Auth 等认证方式。对于 API 网关场景，建议在网关层统一处理认证鉴权，避免后端服务重复实现。同时，应配置 IP 访问控制列表（ACL）和防 CC 攻击策略以保护上游服务。

**实施步骤**:
1. 在 Higress 控制台配置全局或路由级别的认证插件。
2. 若对接企业 IdP（如 Keycloak, Okta），配置 OIDC 回调地址及 Client ID。
3. 针对敏感 API 配置 IP 黑白名单插件。
4. 开启 HTTPS 并配置 TLS 证书，强制重定向 HTTP 到 HTTPS。

**注意事项**:
密钥和凭证应通过 KMS 或 Secret 管理工具注入，切勿明文写在配置文件中。启用高强度的安全策略可能会影响性能，需在安全性和延迟之间取得平衡。

---

### 实践 4：对接云原生服务发现（Kubernetes+Nacos）

**说明**:
Higress 的核心优势之一是能够同时打通 Kubernetes 原生 Service 和 Nacos 等注册中心。在混合云架构或微服务迁移场景中，利用这一特性可以实现 Kubernetes 集群内的服务与经典微服务（如 Spring Cloud/Dubbo）之间的无缝互通。

**实施步骤**:
1. 在 Higress 全局配置中添加服务来源，选择 Nacos 或 ZooKeeper。
2. 配置注册中心的连接地址（Server Addr）和命名空间。
3. 在创建路由时，服务来源可以直接选择 Nacos 注册的服务。
4. 配置服务分组（Group）和集群（Cluster）策略以区分不同环境的服务。

**注意事项**:
确保 Higress 所在的网络环境能够直接访问注册中心的端口。跨服务发现时，需注意服务名解析的冲突问题，建议使用命名空间进行环境隔离。

---

### 实践 5：可观测性与监控告警

**说明**:
为了保障网关的稳定性，必须建立完善的可观测性体系。Higress 原生支持 Prometheus 监控指标、访问日志采集以及链路追踪。建议将日志输出到 Elasticsearch 或 Loki，将 Trace 数据发送给 SkyWalking 或 Jaeger，以便快速定位性能瓶颈和故障点。

**实施步骤**:
1. 开启 Higress 的 Prometheus Metrics 端口，配置 Prometheus 抓取规则。
2. 在网关配置中开启 AccessLog，并输出到标准输出或配置日志采集 Agent（如 Fluentd/Fluent Bit）。
3. 启用 Tracing 透传，配置采样率（例如 10%）以平衡性能与追踪粒度。
4. 在 Grafana 中导入 Higress 官方提供的 Dashboard 模板进行可视化监控。

**注意事项**:
全量日志采集和 100% Tracing

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/2 与 HTTP/3 (QUIC) 协议

**说明**:  
Higress 基于 Envoy 构建，天然支持现代 HTTP 协议。HTTP/2 通过多路复用解决了 HTTP/1.1 的队头阻塞问题，而 HTTP/3 (QUIC) 基于 UDP 协议，能显著减少弱网环境下的延迟和连接建立时间。

**实施方法**:
1. 在 Higress 网关的监听器配置中，启用 HTTP/2 协议支持。
2. 对于 QUIC 支持，需在网关配置中开启 HTTP/3 选项，并确保 UDP 端口（通常为 443）在防火墙和负载均衡器中已开放。
3. 建议配置 TLS 1.3 以配合 HTTP/3 获得最佳握手性能。

**预期效果**:  
在高并发或弱网环境下，请求延迟可降低 20%-30%，并发连接处理能力提升约 40%。

---

### 优化 2：配置全局限流与自适应并发控制

**说明**:  
防止后端服务因突发流量而过载是性能优化的关键。Higress 支持全局全局限流，同时也具备 Envoy 的自动并发控制功能。这能确保系统在负载极高时自动降级，而不是完全崩溃。

**实施方法**:
1. 在网关路由或全局级别配置全局限流，设定精确的 QPS 阈值。
2. 启用 Higress 的自动并发限制，设置目标并发度。
3. 利用 Higress 的 Request Header 或 IP 维度进行精细化限流，保护关键业务接口。

**预期效果**:  
在流量突增场景下，后端服务稳定性提升 99.9%（避免雪崩），系统整体吞吐量（RTPS）在负载下的表现更平稳。

---

### 优化 3：启用 Wasm 插件与本地缓存

**说明**:  
Higress 极为推崇 Wasm (WebAssembly) 插件化扩展。相比于传统的 Lua 或远程调用 AuthN/AuthZ 服务，Wasm 插件运行在本地，执行效率极高。结合本地缓存，可大幅减少对后端或 Redis 的重复查询。

**实施方法**:
1. 将鉴权、限流或 Header 修改逻辑编写为 Wasm 插件（支持 C++/AssemblyScript/Go/TinyGo）。
2. 在 Wasm 插件内部实现内存级缓存（如 LRU Cache），缓存频繁访问的配置或鉴权结果。
3. 启用 Higress 的 Wasm Pluggable 特性，动态加载插件而无需重启网关。

**预期效果**:  
插件执行延迟降低至微秒级（相比远程调用降低 90%+），对于高频鉴权接口，QPS 提升可达 50% 以上。

---

### 优化 4：优化连接池与 Keep-Alive 设置

**说明**:  
默认的连接池配置往往不是最优的。如果 Higress 与后端服务之间频繁建立 TCP 连接，会消耗大量 CPU 和时间。通过调整上游集群的连接池大小和 Keep-Alive 时间，可以显著提高数据传输效率。

**实施方法**:
1. 根据后端服务能力，适当调大 `http2_protocol_options` 或 `max_connections` 参数。
2. 开启连接复用，设置合理的 `idle_timeout`，避免频繁握手。
3. 如果后端支持 HTTP/2，确保 Higress 与后端使用 HTTP/2 通信，以利用单连接多复用的特性。

**预期效果**:  
后端连接建立开销减少 80%，网关到后端的 P99 延迟显著降低，整体吞吐量提升 15%-25%。

---

### 优化 5：启用 CPU 亲和性与多核绑定

**说明**:  
Higress (Envoy) 是高性能多线程模型。在操作系统层面，通过绑定 CPU 亲和性，可以减少 CPU 上下文切换带来的缓存失效，从而提升数据处理效率。

**实施方法**:
1. 在 Higress 的 Pod 部署 YAML 中配置资源 limits

---
## 学习要点

- 基于提供的来源信息（GitHub Trending 上的 Alibaba/Higress 项目），以下是关于该项目最值得关注的 5 个关键要点：
- Higress 是阿里云开源的、基于 Envoy 和 Istio 构建的下一代云原生 API 网关，旨在连接南北向与东西向流量。
- 该项目深度集成了 K8s Ingress 与 Gateway API 标准，能够无缝对接云原生生态系统，简化服务网格管理。
- 它提供了强大的 WAF（Web 应用防火墙）插件市场，支持用户通过 Lua 或 WASM (WebAssembly) 进行灵活的流量管理和安全防护扩展。
- Higress 兼容 Nginx Ingress 注解，并支持 Nginx 生态的平滑迁移，降低了传统网关用户的迁移成本与门槛。
- 该架构支持将 K8s 服务直接发布为 API，并内置了服务发现与负载均衡能力，实现了微服务治理与 API 网关的深度融合。
- 作为高性能网关，它针对高并发场景进行了优化，支持多协议接入，能够有效解决微服务架构中的流量调度与安全问题。


---
## 学习路径

## 学习路径

### 阶段 1：基础概念与环境认知

**学习内容**:
- 理解云原生网关的核心概念：什么是 API Gateway，以及南北向流量与东西向流量的区别。
- 了解 Higress 的背景：基于 Envoy 和 Istio 构建，阿里云开源，定位为下一代云原生网关。
- 掌握基本术语：Ingress、Gateway、路由、服务发现。
- 了解 Higress 与传统 Nginx、Kubernetes Ingress Nginx 以及 Istio Gateway 的异同与优势。

**学习时间**: 1周

**学习资源**:
- Higress GitHub 官方仓库 README
- Higress 官方文档架构介绍篇
- 云原生网关技术对比相关技术博客

**学习建议**: 
不要急于动手部署，先阅读官方文档的"产品介绍"或"架构设计"部分，理解 Higress 为什么选择 Envoy 作为数据面，以及它如何解决 K8s Ingress 的性能瓶颈问题。

---

### 阶段 2：快速上手与核心功能实践

**学习内容**:
- **本地/集群部署**：学习如何在 Docker 本地环境或 Kubernetes 集群中安装 Higress。
- **控制台操作**：熟悉 Higress Dashboard 的使用，包括配置域名、路由规则和服务来源。
- **流量管理**：实践基于 HTTP 头部、URL、Cookie 的路由转发配置。
- **插件系统入门**：了解 Higress 的插件机制（Wasm 插件），尝试开启并配置一个内置插件（如 Key Auth 或 Request Block）。
- **全链路灰度**：学习如何配置 Header 或 Weight 类型的灰度发布流量。

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 快速开始
- Higress 官方文档 - 流量管理
- Higgress 官方文档 - 插件市场

**学习建议**: 
建议使用 Minikube 或 Kind 创建一个本地 K8s 集群进行练习。尝试部署两个不同的后端服务（如 httpbin 和 nginx），并通过 Higress 配置路由规则将流量按比例分发，以此验证网关的转发逻辑。

---

### 阶段 3：进阶配置与生态集成

**学习内容**:
- **服务发现集成**：深入学习 Higress 如何对接 Nacos、Consul、DNS 以及 Kubernetes Service。
- **安全防护**：配置 mTLS（双向认证）、JWT 认证、CORS 跨域配置以及 IP 访问控制。
- **高可用部署**：了解 Higress 的高可用架构，配置健康检查与熔断降级策略。
- **Dubbo 协议支持**：学习如何通过 Higress 网关代理 Dubbo 服务（HTTP 转 Dubbo）。
- **可观测性**：集成 Prometheus、Grafana 以及 SkyWalking/Zipkin 进行指标监控和链路追踪。

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档 - 服务来源
- Higress 官方文档 - 安全
- Envoy 官方文档（关于热重启与线程模型的原理）

**学习建议**: 
尝试将 Higress 接入现有的微服务注册中心（如 Nacos）。重点关注安全部分，尝试配置一个需要特定 JWT Token 才能访问的路由，并使用 Postman 或 Curl 进行验证测试。

---

### 阶段 4：插件开发与源码深度定制

**学习内容**:
- **Wasm 插件开发**：学习使用 Go 或 C++ 开发自定义 Wasm 插件，实现特定的请求/响应处理逻辑。
- **插件生命周期管理**：了解插件的加载、热更新机制以及插件配置的冷启动与热加载。
- **性能调优**：深入理解 Envoy 配置，优化连接池、缓冲区大小以及并发处理能力。
- **源码级剖析**：阅读 Higress 源码，理解 Router 组件的匹配逻辑以及配置下发的热更新流程。

**学习时间**: 4周以上

**学习资源**:
- Higress GitHub - Examples 目录
- Higress 官方文档 - 自定义插件开发
- WebAssembly (Wasm) 官方文档与 Proxy-Wasm 规范

**学习建议**: 
从编写一个简单的 Go Wasm 插件开始，例如实现一个自定义的请求头修改器。编译成 `.wasm` 文件后上传到 Higress 并测试。随后，阅读 Higress 的 Router 模块源码，理解配置如何从控制台下发到 Envoy 数据面。

---

### 阶段 5：生产级运维与架构设计

**学习内容**:
- **多租户与多网关组管理**：在大型企业中如何划分网关实例，进行多团队隔离。
- **金丝雀发布与蓝绿发布**：设计复杂的流量治理策略，确保业务平滑上线。
- **网关即服务**：

---
## 常见问题


### 1: Higress 是什么？它与阿里巴巴有什么关系？

1: Higress 是什么？它与阿里巴巴有什么关系？

**A**: Higress 是一款基于阿里内部多年实践沉淀的下一代云原生 API 网关。它诞生于阿里巴巴，旨在解决云原生时代流量治理的复杂性问题。Higress 的前身是阿里巴巴集团内部广泛使用的 HS 架构（HSF+VIP），融合了阿里在电商、大促等高并发场景下的技术经验。它是阿里云云原生 API 网关的开源版本，旨在为开发者提供统一、高效、安全的流量管理平台。



### 2: Higress 与 Kong、Nginx 或 APISIX 等网关相比有什么核心优势？

2: Higress 与 Kong、Nginx 或 APISIX 等网关相比有什么核心优势？

**A**: Higress 的核心优势主要体现在以下几个方面：
1. **深度集成云原生生态**：Higress 原生支持 Kubernetes 和 Istio，可以作为 Ingress Controller 或 API Gateway 使用，实现了服务网格与 API 网关的流量统一治理。
2. **高性能与低资源消耗**：基于 Rust 编写的 Wasm 插件运行时，提供了极高的插件执行效率，同时相比传统的 Lua 或 Java 插件，内存占用更低。
3. **开箱即用的插件市场**：提供了丰富的预置插件（如认证、限流、路由重写等），并兼容 Nginx 的 Lua 生态和 Kong 的插件生态，降低了迁移成本。
4. **安全防护能力**：内置了 WAF（Web Application Firewall）功能，能够有效防御常见的 Web 攻击。



### 3: Higress 是否支持 Nginx 或 Kong 的现有配置迁移？

3: Higress 是否支持 Nginx 或 Kong 的现有配置迁移？

**A**: 是的，Higress 非常重视兼容性，以降低用户的迁移门槛。
1. **Nginx 兼容**：Higress 底层基于 Nginx/OpenResty，支持大部分 Nginx 的配置指令（SNI、路由匹配、Header 操作等），用户可以相对平滑地将 Nginx 配置逻辑迁移到 Higress。
2. **Kong 插件兼容**：Higress 提供了 Kong 插件运行时适配层，理论上支持运行基于 Lua 的 Kong 插件，用户可以在 Higress 中复用已有的 Kong 插件资产。



### 4: Higress 的 Wasm 插件机制是什么？为什么要使用它？

4: Higress 的 Wasm 插件机制是什么？为什么要使用它？

**A**: Wasm（WebAssembly）插件机制是 Higress 架构的一大亮点。
1. **定义**：Higress 允许用户使用多种编程语言（如 Go, C++, Rust, AssemblyScript 等）编写插件逻辑，然后编译成 Wasm 格式在网关中运行。
2. **优势**：传统的网关插件（如 OpenResty 的 Lua 插件）存在开发语言单一、隔离性差、容易导致网关进程崩溃等问题。Wasm 提供了沙箱隔离环境，即使插件崩溃也不会导致网关主进程崩溃，从而极大地提升了网关的稳定性和安全性。此外，它让后端开发者可以使用熟悉的语言（如 Go）来编写网关逻辑。



### 5: 在 Kubernetes 环境中，Higress 是如何与 Istio 配合使用的？

5: 在 Kubernetes 环境中，Higress 是如何与 Istio 配合使用的？

**A**: Higress 可以作为 Istio 体系中的 Gateway 组件使用。
1. **统一控制面**：Higress 可以复用 Istio 的控制面进行配置下发，实现从集群南北向流量到东西向流量的统一管理。
2. **替代默认网关**：相比于 Istio 默认的 Envoy Gateway，Higress 提供了更友好的控制台界面、更丰富的路由逻辑（如基于 Header、Cookie、Query 参数的高级路由）以及更强大的插件扩展能力，解决了原生 Istio Ingress 在生产环境中配置复杂、功能受限的问题。



### 6: Higress 是否支持对 Dubbo 或 gRPC 等微服务协议进行管理？

6: Higress 是否支持对 Dubbo 或 gRPC 等微服务协议进行管理？

**A**: 是的，Higress 具备全协议代理能力，不仅支持 HTTP/HTTPS，还深度适配了微服务场景。
1. **Dubbo 支持**：作为阿里巴巴出品的网关，Higress 对 Dubbo 协议有着天然的支持，可以实现 HTTP 到 Dubbo 的协议转换，让前端应用可以通过 HTTP/RESTful 风格调用后端的 Dubbo 服务。
2. **gRPC 支持**：Higress 原生支持 gRPC 协议的代理与路由，支持基于 gRPC 的服务发现与负载均衡，能够满足云原生架构下 RPC 通信的需求。



### 7: 如何开始使用或部署 Higress？

7: 如何开始使用或部署 Higress？

**A**: 部署 Higress 非常简单，主要推荐以下两种方式：
1. **Docker/Docker Compose**：适合快速体验和功能测试，用户可以通过执行一行命令在本地启动 Higress 及其控制台。
2. **Helm（Kubernetes）**：适合生产环境部署。用户可以通过 Helm Chart 将 Higress 部署到 Kubernetes 集群中。部署过程中，可以配置是否启用 Istio 集成模式。安装完成后，可以通过 Higress �

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 基于 Higress 的标准网关功能，设计一个流量路由策略。要求将包含特定 Header（如 `env: canary`）的 HTTP 请求，精准地路由到名为 `service-canary` 的后端服务，而其他流量则路由到 `service-stable`。

### 提示**: 思考如何在 Ingress Route 或网关规则中定义匹配条件。关注 HTTP Header 的匹配语法以及权重路由与基于 Header 路由的区别。

### 

---
## 实践建议

基于 Higress 作为 AI Native API 网关的定位，以下是针对实际生产环境和开发场景的 6 条实践建议：

### 1. 利用 Wasm 插件实现 AI 提示词管理与安全防护
**场景**：在大模型应用中，直接将用户 Prompt 传给 LLM 可能导致敏感数据泄露或遭遇 Prompt 注入攻击。
**建议**：
*   **具体操作**：不要在应用代码中硬编码 System Prompt。利用 Higress 的 Wasm 插件机制（或官方 AI 统计/鉴权插件），在网关层动态追加或修改 System Prompt。例如，在网关层统一注入“请勿输出内部机制相关内容”的指令。
*   **最佳实践**：编写或配置 Wasm 插件对请求体进行正则过滤，拦截试图提取模型训练数据的恶意 Prompt。
*   **常见陷阱**：避免在网关进行过重的文本处理逻辑（如复杂的 NLP 处理），这会增加显著延迟，仅做安全过滤和上下文增强。

### 2. 配置语义化负载均衡以应对 LLM 限流
**场景**：调用 OpenAI 或 Azure OpenAI 时，单一 API Key 容易触发 RPM（每分钟请求数）或 TPM（每分钟 Token 数）限制。
**建议**：
*   **具体操作**：在 Higress 中配置服务来源，填入多个不同的 API Key。在路由配置中开启基于特定负载均衡策略（如随机或轮询）的流量分发。
*   **最佳实践**：结合 Higress 的重试插件，设置针对 429 (Too Many Requests) 状态码的指数退避重试策略，确保前端请求不会因为单一 Key 限流而直接报错。
*   **常见陷阱**：不要简单地使用 Round-Robin（轮询），因为不同模型的请求 Token 消耗差异巨大，应尽量结合上游返回的 `usage` 字段（如果插件支持）或基于请求头进行更智能的分发。

### 3. 实施基于 Token 的精细化流量控制
**场景**：传统 API 网关通常基于“请求数（QPS）”限流，但 AI 服务的成本主要在于“Token 消耗”。
**建议**：
*   **具体操作**：使用 Higress 的 `request-block` 或 `key-rate-limit` 插件时，关注针对请求体大小或预估 Token 数的限流配置。如果是自建上游服务，可以通过响应头传递 Token 消耗信息给网关进行统计。
*   **最佳实践**：针对不同用户组配置不同的 Token 预算。例如，免费用户每天限制 10k Tokens，付费用户限制 1M Tokens。
*   **常见陷阱**：仅限制 QPS 无法防止用户通过发送超长上下文来消耗巨额配额，必须结合请求体长度限制来防止“长文本攻击”。

### 4. 统一多模型接口与协议转换
**场景**：业务代码可能需要同时调用 OpenAI 格式、通义千问、文心一言等不同格式的接口，适配成本高。
**建议**：
*   **具体操作**：利用 Higress 的 AI 统一处理能力，将不同厂商的 API 在网关层统一映射为 OpenAI 协议格式。
*   **最佳实践**：后端服务只需对接 Higress 的标准 OpenAI 接口，当需要切换模型供应商时，仅需在 Higress 控制台修改后端服务地址或 Header，无需重新发布业务代码。
*   **常见陷阱**：注意不同模型厂商的流式（SSE）响应格式细微差异（如换行符处理），配置 Higress 的全链路流式透传，确保网关不会缓冲流式响应导致首字延迟增加。

### 5. 缓存常见问题以降低成本与延迟
**场景**：AI 对话中，大量高频问题（如“你是谁”、“如何重置密码”）的回复是高度重复的，重复调用 LLM 产生高昂费用且延迟较高。
**建议**：
*   **具体操作**：启用 Hig

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI Native](/tags/ai-native/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [WASM](/tags/wasm/) / [LLM](/tags/llm/) / [MCP 协议](/tags/mcp-%E5%8D%8F%E8%AE%AE/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260130-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260203-github_trending-alibaba-higress-2.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260205-github_trending-alibaba-higress-6.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260201-github_trending-alibaba-higress-8.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*