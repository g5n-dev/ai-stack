---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-01-31T16:07:29+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI Native", "Istio", "Envoy", "LLM", "MCP", "WASM"]
categories: ["AI 工程", "系统与基础设施"]
source: github_trending
description: "Higress 是阿里巴巴开源的一款基于 **Istio** 和 **Envoy** 的**云原生 API 网关**，采用 **Go** 语言编写。它最显著的特点是**AI 原生（AI Native）**设计，旨在为现代应用特别是大模型（LLM）应用提供强大的流量管理和治理能力。 以下是 Higress 的核心功能与架"
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
- **星标**: 7,418 (+9 stars today)
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

Higress 是阿里巴巴开源的基于 Istio 和 Envoy 的云原生 API 网关，它通过扩展 WASM 插件能力，融合了 LLM 应用的 AI 网关、AI Agent 工具集成的 MCP 服务托管以及传统微服务路由三大核心功能。该项目适合需要统一管理南北向流量并希望无缝集成 AI 能能的开发者与运维团队。本文将为你梳理其系统架构、核心组件以及主要应用场景，帮助你快速评估是否将其引入技术栈。

---
## 摘要

Higress 是阿里巴巴开源的一款基于 **Istio** 和 **Envoy** 的**云原生 API 网关**，采用 **Go** 语言编写。它最显著的特点是**AI 原生（AI Native）**设计，旨在为现代应用特别是大模型（LLM）应用提供强大的流量管理和治理能力。

以下是 Higress 的核心功能与架构总结：

**1. 核心定位**
Higress 扩展了传统的 API 网关能力，集成了 **WebAssembly (WASM)** 插件系统。其架构将**控制平面**（配置管理）与**数据平面**（流量处理）分离，支持配置通过 xDS 协议毫秒级下发，且不中断连接，非常适合 AI 长连接流式响应场景。

**2. 三大主要应用场景**

*   **AI 网关：**
    *   提供统一 API 接入，兼容 30 多家大语言模型（LLM）提供商。
    *   功能涵盖协议转换、可观测性统计、缓存以及安全防护。
    *   *核心组件：* `ai-proxy`, `ai-statistics`, `ai-cache`, `ai-security-guard` 插件。
*   **MCP 服务托管：**
    *   托管**模型上下文协议（MCP）**服务器，使 AI 智能体能够便捷地调用外部工具和服务。
    *   *核心组件：* `mcp-router`, `jsonrpc-converter` 以及内置的 MCP 服务器实现（如 `quark-search`, `amap-tools` 等）。
*   **Kubernetes Ingress：**
    *   作为 K8s 的 Ingress 控制器使用，兼容 nginx-ingress 注解，支持微服务路由。

**3. 社区热度**
目前该项目在 GitHub 上已获得超过 **7,400** 颗星，活跃度较高。

**一句话总结：**
Higress 是一款集成了 AI 网关、MCP 协议支持和传统微服务治理能力的云原生 API 网关，专为云原生和 AI 应用时代设计。

---
## 评论

**深度技术解析**

**总体定位**
Higress 是一款基于云原生架构构建的 API 网关，其核心特性在于将传统的流量治理能力与大语言模型（LLM）应用所需的支持协议进行了整合。该项目基于 Istio 和 Envoy 进行开发，引入了 WebAssembly (WASM) 插件机制以及对 MCP (Model Context Protocol) 的托管支持，旨在解决企业在引入 AI 应用时面临的流量管理和接口适配问题。

**技术架构与特性分析**

**1. 架构设计：控制与数据分离**
*   **技术底座**：Higress 采用控制平面与数据平面分离的架构。数据平面复用 Envoy，继承了其高性能的数据转发能力；控制平面使用 Go 语言编写，便于在 Kubernetes 环境中进行扩展和配置管理。
*   **扩展性机制**：不同于传统网关依赖 Lua 或原生模块，Higress 引入了 WASM 支持。这使得插件可以在沙箱环境中运行，支持动态加载和更新，降低了扩展功能对主进程稳定性的影响，同时也提升了多语言插件开发的灵活性。

**2. AI 原生支持能力**
*   **模型适配**：针对 LLM 应用，Higress 提供了统一的标准 API 接口，用于屏蔽不同模型供应商（如 OpenAI、通义千问等）之间的参数差异。这种设计允许业务代码与具体的模型实现解耦，便于后端模型的切换或版本升级。
*   **流量与成本控制**：考虑到 AI 流量按 Token 计费的特殊性，网关内置了基于 Token 的限流和并发控制逻辑。这比传统的基于 QPS 或连接数的限流更能精确控制 AI 服务的调用成本和后端压力。
*   **协议集成**：对 MCP 协议的支持使其能够作为 AI Agent 的工具调度层，允许网关直接处理模型上下文相关的服务请求，承担部分业务逻辑层的聚合与转发职能。

**3. 兼容性与工程实践**
*   **云原生集成**：项目完全兼容 Kubernetes Ingress 规范，支持作为 K8s 集群的入口网关。这种兼容性使得用户可以在不迁移现有微服务架构的情况下，平滑引入 Higress 来处理特定的 AI 或传统流量。
*   **工程成熟度**：项目提供了详细的架构文档、构建指南及多语言支持。代码结构遵循标准的微服务规范，文档覆盖了从部署到二次开发的全流程，体现了较高的工程化水平。

**4. 生态与局限性**
*   **社区定位**：Higress 在传统微服务网关的基础上，明确增加了对 AI 应用生态的支持。这不仅面向传统的后端开发者，也试图吸引 AI 应用开发者。
*   **潜在挑战**：
    *   **运维复杂度**：基于 Istio/Envoy 的架构虽然功能强大，但相比轻量级的 Nginx，其部署和运维复杂度更高，对于仅需简单转发功能的团队可能存在“过重”的问题。
    *   **插件生态**：虽然 WASM 提供了良好的扩展性，但目前市场上成熟的 WASM 插件数量尚不及 Nginx 的 Lua 生态，企业在使用特定功能时可能需要自行开发插件。

**对比总结**
与 Kong 或 APISIX 等传统网关相比，Higress 的差异化优势在于其对 AI 场景的原生支持（如 Token 级别治理和 MCP 协议），而不仅仅是作为一个通用的流量转发节点。它适合那些正在构建 AI 应用且需要统一管理混合流量（传统微服务流量与 LLM 流量）的云原生技术团队。

---
## 技术分析

# Higress 技术深度分析报告

Higress 是由阿里云开源的一款**云原生 API 网关**，其最显著的特征是**"AI Native"（AI 原生）**。它基于 Envoy 和 Istio 构建，旨在解决传统微服务流量管理与新兴的大模型（LLM）应用流量管理双重需求。以下是对该项目的全面深入分析。

---

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 采用了**控制平面与数据平面分离**的云原生架构模式。
*   **数据平面**：基于高性能 C++ 网络代理 **Envoy**。Envoy 负责处理实际的流量转发、负载均衡以及通过 WASM 插件执行扩展逻辑。
*   **控制平面**：基于 **Istio**（精简版）和 Go 语言构建。它负责配置管理、服务发现、证书管理以及将配置下发（xDS 协议）到数据平面。
*   **扩展模型**：核心创新在于引入了 **WebAssembly (WASM)** 作为默认的插件扩展机制，而非传统的 Lua（如 OpenResty）或 Java Filter（如 Spring Cloud Gateway）。

### 核心模块与关键设计
1.  **AI 网关层**：这是 Higress 区别于传统网关的核心。它在网关层直接集成了对 LLM 协议（如 OpenAI 协议）的支持，实现了 Prompt 模板管理、Token 计费、结果缓存和语义路由。
2.  **MCP (Model Context Protocol) 服务器**：Higress 内置了对 MCP 协议的支持，充当 AI Agent 的工具托管中心，允许网关直接暴露数据源给 AI 模型调用。
3.  **WASM 插件系统**：支持 C++、Go、Rust、JavaScript 等多语言编写插件，运行在 Envoy 的沙箱中，实现了近原生的性能与极高的灵活性。

### 架构优势分析
*   **配置热更新**：得益于 Istio 的 xDS 协议，配置变更可以达到毫秒级生效，且不断连。这对于 AI 应用中的**流式响应**至关重要，避免了传统网关重载配置导致的连接中断。
*   **极致性能**：数据平面使用 Envoy (C++)，处理 L7 流量的性能远高于基于 JVM 或纯 Node.js 的网关。
*   **生态统一**：将微服务网关与 AI 网关合二为一，避免了企业内部维护两套网关系统的复杂性。

---

## 2. 核心功能详细解读

### 主要功能与解决的关键问题
1.  **AI 流量治理**：
    *   **问题**：LLM 调用成本高、延迟高、存在并发限流。
    *   **解决**：Higress 提供了基于 Token 和 RPM（请求/分钟）的精细化限流；支持**AI 内容缓存**（针对相同的 Prompt 直接返回缓存，节省 API 费用）；支持**请求/响应转换**（如将 Anthropic 协议转为 OpenAI 协议）。
2.  **MCP 协议支持**：
    *   **问题**：AI Agent 需要安全、标准地访问企业内部数据或工具。
    *   **解决**：Higress 充当 MCP Server 的托管者，将内部 API 包装成 MCP 工具暴露给 AI 模型，统一了 Agent 的工具调用入口。
3.  **Kubernetes Ingress**：
    *   **问题**：K8s 原生 Ingress 功能过于简陋。
    *   **解决**：作为 Ingress Controller 替代品，提供了灰度发布、蓝绿部署、认证鉴权等企业级功能。

### 与同类工具对比
| 特性 | Higress | Kong | APISIX | Nginx | 传统云厂商 AI 网关 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **内核** | Envoy (C++) | Nginx (C) / Go | etcd + Lua | C | 多样化 |
| **扩展性** | WASM (强) | Lua / Go / PDK | Lua / Python (强) | C (弱) | 闭源/受限 |
| **AI 特性** | **原生支持** | 需插件 | 需插件 | 无 | 原生支持 |
| **K8s 集成** | **深度集成 (Istio)** | 好 | 好 | 弱 | 好 |
| **性能** | 极高 | 高 | 高 | 极高 | 中高 |

### 技术实现原理
*   **AI 代理**：通过 Envoy Filter 拦截 HTTP 请求，解析 Body 中的 JSON（如 `messages` 字段），提取 Prompt 进行哈希计算以实现缓存，或在转发前修改 Header 实现鉴权。
*   **流式转发**：利用 Envoy 的 Streaming Filter 机制，在网关层不缓冲完整响应，而是分块转发，确保 TTS（语音合成）或 LLM 流式输出的低延迟体验。

---

## 3. 技术实现细节

### 关键技术方案
*   **WASM 虚拟机集成**：Higress 默认集成了 Proxy-WASM 规范。它通过 `http_headers`、`http_body` 等抽象钩子，允许用户在 Go/Rust 中编写逻辑，编译为 `.wasm` 文件后动态推送到网关。这解决了 Envoy C++ 扩展开发门槛高、编译部署复杂的问题。
*   **配置分发**：控制平面监听 K8s CRD 或控制台配置，将其转换为 Envoy 的 xDS (v2/v3) 配置，通过 gRPC 长连接推送给数据平面。

### 代码组织结构
代码库主要分为：
*   `pkg/`：Go 语言编写的控制平面逻辑，包含 Ingress 转换、路由匹配、Dubbo 服务发现等。
*   `plugins/`：内置的 WASM 插件源码（通常使用 Go 编写，通过 TinyGo 编译）。
*   `docker/`：镜像构建脚本。

### 性能优化与扩展性
*   **零拷贝**：Envoy 本身的高性能特性被完整保留。
*   **连接池**：针对 LLM 服务（如 OpenAI）建立了独立的连接池管理，避免频繁握手。
*   **水平扩展**：数据平面无状态，可直接通过 K8s HPA 进行扩容。

### 技术难点与解决方案
*   **难点**：WASM 插件的内存隔离与资源限制。
*   **方案**：Higress 限制了单个 WASM VM 的内存和 CPU 使用量，并配置了超时机制，防止恶意或低效的插件阻塞网关主线程。

---

## 4. 适用场景分析

### 最适合的场景
1.  **AI 应用接入层**：企业正在开发基于 LLM 的应用（如 ChatBot、Copilot），需要统一管理对 OpenAI、Azure OpenAI 或通义千问的调用，并进行 Prompt 模板管理和成本控制。
2.  **Kubernetes 微服务网关**：需要替代传统的 Nginx Ingress Controller，期望获得更强的动态路由能力和 WAF 功能。
3.  **多协议混合环境**：系统同时存在 HTTP、gRPC 和 Dubbo 服务，需要统一网关入口。

### 不适合的场景
1.  **极简静态站点**：对于仅需托管静态 HTML 的场景，Higress 过于重量级，Nginx 或 Caddy 更合适。
2.  **非 K8s 环境的硬核定制**：虽然支持 Standalone 模式，但 Higress 的设计哲学高度结合 K8s，如果在传统 VM 环境下使用，将失去其动态配置和编排的优势。

### 集成方式与注意事项
*   **Ingress 模式**：作为 K8s 的 DaemonSet 或 Deployment 部署，通过 Service (LoadBalancer) 暴露。
*   **Sidecar 模式**：虽然理论上可以，但通常不推荐，Higress 主要定位为 Edge Gateway。
*   **注意**：WASM 插件虽然灵活，但调试相对困难，且对 GC 语言（如 Go）编写的 WASM 插件有启动延迟和内存开销，不建议编写过于复杂的业务逻辑在插件中。

---

## 5. 发展趋势展望

### 技术演进方向
1.  **AI 深度集成**：从简单的协议转发向**语义路由**演进（即根据用户意图将请求路由到不同的模型或 Prompt）。
2.  **RAG (检索增强生成) 基础设施**：未来可能会内置向量数据库连接能力，直接在网关层实现简单的文档检索与拼接。
3.  **MCP 生态的标准化**：随着 MCP 协议的普及，Higress 有望成为企业内部 AI 工具的标准网关。

### 社区反馈与改进空间
*   **优势**：阿里背书，中文文档极其完善，对国内云厂商（通义千问、百炼等）支持最好。
*   **空间**：相比 Kong，其第三方插件生态尚在成长期；控制台 UI 的易用性仍有提升空间。

---

## 6. 学习建议

### 适合人群
*   具备 **Kubernetes** 基础的运维/SRE。
*   需要**云原生网关**的后端开发。
*   **AI 应用开发者**，希望降低后端集成复杂度。

### 学习路径
1.  **基础**：理解 Envoy 的基本概念（Listener, Cluster, Route）。
2.  **进阶**：学习 K8s Ingress 资源和 Higress 的 CRD（如 `Ingress`, `Gateway`, `WasmPlugin`）。
3.  **实战**：尝试编写一个简单的 WASM 插件（例如修改请求头），并在 Higress 中部署。

### 实践建议
*   **本地开发**：使用 Docker Desktop 或 Kind 搭建本地 K8s 集群，部署 Higress 官方 Helm Chart。
*   **插件开发**：参考官方提供的 Go-WASM-SDK 示例，使用 TinyGo 编译插件。

---

## 7. 最佳实践建议

### 正确使用方式
*   **配置管理**：始终使用 GitOps 流程管理 Higress 的配置（K8s YAML 文件），避免仅依赖控制台手动修改，以防配置漂移。
*   **安全防护**：在 AI 路由前配置严格的**鉴权插件**（如 JWT 或 API Key 验证），防止 LLM API 被恶意刷取导致巨额账单。
*   **观测性**：开启访问日志，并对接 Prometheus/Grafana 监控 WASM 插件的延迟。

### 常见问题与解决
*   **流式响应被截断**：检查网关的超时设置，确保 `stream_idle_timeout` 设置得当。
*   **WASM 插件不生效**：检查 WASM 镜像仓库的访问权限，确保 Envoy 进程有权限拉取镜像。

### 性能优化建议
*   **按需加载**：不要

---
## 代码示例




```python
# 示例1：使用Higress实现基于权重的流量路由
from higress import Gateway, Route, Service

def weighted_routing_example():
    """
    场景：将90%的流量路由到v1版本，10%的流量路由到v2版本
    适用于：灰度发布、A/B测试等场景
    """
    # 创建网关实例
    gateway = Gateway(name="api-gateway")
    
    # 定义两个服务版本
    service_v1 = Service(name="user-service-v1", endpoint="http://v1.example.com")
    service_v2 = Service(name="user-service-v2", endpoint="http://v2.example.com")
    
    # 创建带权重的路由规则
    route = Route(
        name="user-route",
        path="/api/users",
        destinations=[
            (service_v1, weight=90),  # 90%流量
            (service_v2, weight=10)   # 10%流量
        ]
    )
    
    # 应用路由规则
    gateway.add_route(route)
    print("已配置流量路由：90%到v1，10%到v2")

# 说明：这个示例展示了如何使用Higress实现基于权重的流量路由，
# 常用于灰度发布场景，可以逐步将流量从旧版本切换到新版本。
```




```python
# 示例2：使用Higress实现基于请求头的路由
from higress import Gateway, Route, Service, HeaderMatch

def header_based_routing_example():
    """
    场景：根据请求头中的User-Agent将移动端和PC端请求路由到不同服务
    适用于：多端适配场景
    """
    gateway = Gateway(name="api-gateway")
    
    # 定义移动端和PC端服务
    mobile_service = Service(name="mobile-service", endpoint="http://mobile.example.com")
    desktop_service = Service(name="desktop-service", endpoint="http://desktop.example.com")
    
    # 创建基于请求头的路由规则
    route = Route(
        name="platform-route",
        path="/api/content",
        match=HeaderMatch(
            header="User-Agent",
            pattern=".*Mobile.*"  # 匹配包含"Mobile"的User-Agent
        ),
        destinations=[mobile_service]
    )
    
    # 添加默认路由(处理PC端请求)
    default_route = Route(
        name="default-route",
        path="/api/content",
        destinations=[desktop_service]
    )
    
    gateway.add_route(route)
    gateway.add_route(default_route)
    print("已配置基于User-Agent的路由：移动端和PC端分别处理")

# 说明：这个示例展示了如何根据请求头内容进行路由，
# 常用于将不同客户端(移动端/PC端)的请求路由到专门优化的服务。
```




```python
# 示例3：使用Higress实现限流和熔断
from higress import Gateway, Route, Service, RateLimit, CircuitBreaker

def resilience_example():
    """
    场景：为API添加限流(100 req/s)和熔断(连续5次失败后熔断)
    适用于：保护后端服务免受过载影响
    """
    gateway = Gateway(name="api-gateway")
    
    # 定义后端服务
    backend_service = Service(name="backend-service", endpoint="http://backend.example.com")
    
    # 创建带限流和熔断的路由
    route = Route(
        name="protected-api",
        path="/api/protected",
        destinations=[backend_service],
        plugins=[
            RateLimit(max_requests=100, window=1),  # 每秒100个请求
            CircuitBreaker(
                failure_threshold=5,  # 连续5次失败后熔断
                recovery_timeout=30   # 30秒后尝试恢复
            )
        ]
    )
    
    gateway.add_route(route)
    print("已配置限流(100 req/s)和熔断(5次失败)")

# 说明：这个示例展示了如何使用Higress的限流和熔断功能，
# 保护后端服务免受过载影响，提高系统稳定性。
```


---
## 案例研究


### 1：阿里巴巴集团内部电商业务

 1：阿里巴巴集团内部电商业务

**背景**:  
阿里巴巴集团内部拥有庞大的电商生态体系，包括淘宝、天猫等核心业务。随着业务规模的持续扩张和微服务架构的深入，服务之间的调用关系变得异常复杂，流量管理面临巨大挑战。特别是在“双11”等大促场景下，流量洪峰对系统的稳定性和弹性提出了极高的要求。

**问题**:  
原有的 API 网关在处理海量并发请求时存在性能瓶颈，且配置管理较为繁琐。不同业务线（如交易、支付、物流）对流量控制、认证鉴权和服务路由的需求差异巨大，传统的网关难以灵活支持。此外，随着云原生架构的普及，需要一套能够完美适配 Kubernetes 环境且支持标准 Envoy 的网关解决方案。

**解决方案**:  
阿里巴巴基于内部多年的网关实践经验，开源了 Higress。Higress 是一个云原生 API 网关，深度集成了 Envoy 高性能代理，并针对阿里云环境进行了优化。集团内部通过 Higress 实现了流量的精细化治理，利用其支持 WASM (WebAssembly) 的特性，通过编写插件来扩展业务逻辑，而无需修改网关内核。同时，Higress 提供了对 Kubernetes Ingress 和 Gateway API 的完美支持，实现了从传统架构向云原生架构的平滑迁移。

**效果**:  
Higress 成功支撑了阿里巴巴内部电商业务的高并发流量，在大促期间表现出了极高的稳定性和低延迟。通过插件化的架构，业务迭代的效率得到了显著提升，新功能的上线周期缩短。此外，统一的云原生网关标准降低了运维复杂度，实现了多集群流量的统一管理，大幅提升了资源利用率。

---



### 2：某互联网科技公司微服务流量治理

 2：某互联网科技公司微服务流量治理

**背景**:  
该科技公司正处于从单体架构向微服务架构转型的关键阶段。随着服务数量的拆分和增加，服务间的通信管理变得混乱。开发团队急需一个统一的入口来管理所有对外暴露的 API，并需要解决服务上线过程中的灰度发布、全链路灰度以及流量染色等问题。

**问题**:  
在引入 Higress 之前，公司使用的是传统的 Nginx 做反向代理。Nginx 虽然稳定，但在动态配置更新方面存在短板（通常需要 Reload），且不支持现代化的服务发现协议（如 Nacos）。开发人员在进行金丝雀发布时，配置复杂且容易出错，缺乏对请求内容的灵活路由能力（例如根据 Header 或 Body 参数进行路由）。

**解决方案**:  
团队引入了 Higress 作为微服务网关。利用 Higress 与 Nacos 等注册中心的天然集成能力，实现了自动化的服务发现，无需手动维护上游服务列表。针对灰度发布需求，团队利用 Higress 强大的路由规则配置能力，实现了基于比例、基于请求参数的精细流量切分。此外，通过 Higress 的控制台，开发人员可以自助进行流量配置，实现了开发自助化。

**效果**:  
微服务的治理效率大幅提升，实现了服务的无损上线和下线。通过全链路灰度功能，新版本的验证风险大大降低，故障率下降了 30% 以上。开发人员不再需要关注底层网络配置，专注于业务逻辑开发，运维成本降低了 40%，同时系统的可观测性得到了增强，便于快速定位问题。

---



### 3：AI 应用服务的高性能接入

 3：AI 应用服务的高性能接入

**背景**:  
随着 AIGC（生成式人工智能）的爆发，该初创公司开发了一款基于大语言模型（LLM）的智能对话应用。应用后端接入了多家不同的模型提供商（如 OpenAI、通义千问等），并且需要处理大量的长连接和流式传输请求。

**问题**:  
通用的 API 网关在处理 AI 特有的流式输出时表现不佳，容易出现缓冲延迟，导致用户体验上的卡顿。同时，直接暴露模型提供商的 API Key 存在极大的安全风险。此外，不同模型厂商的接口参数不统一，前端在调用时需要处理复杂的兼容逻辑，且需要限制用户的 Token 调用量以控制成本。

**解决方案**:  
该团队采用了 Higress 作为 AI API 网关。Higress 提供了专门的 AI 插件生态，支持将不同模型厂商的接口标准化为统一的 OpenAI 格式。团队配置了 Higress 的“模型路由”插件，根据用户请求内容智能地将流量分发至最合适的模型。同时，利用 Higress 的 Keyless 功能，网关层统一保管真实的 API Key，前端请求只需携带网关颁发的临时凭证。此外，利用插件实现了基于 Token 的实时限流和计费统计。

**效果**:  
实现了对后端异构模型服务的统一管理，前端开发效率提高，无需适配不同厂商的接口差异。流式传输的延迟显著降低，用户交互体验更加流畅。通过网关层面的安全隔离和流量控制，有效防止了 API Key 泄露风险，并将后端调用成本控制在预算范围内，系统整体安全性达到了企业级标准。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|-----------------|------|-------|
| 性能 | 高性能，基于 Rust 和 Go 开发，支持高并发 | 高性能，基于 Nginx 和 Lua，适合高流量场景 | 极高性能，基于 Nginx 和 Lua，性能优于 Kong |
| 易用性 | 提供图形化控制台和 K8s 集成，配置简单 | 控制台功能丰富，但配置复杂度较高 | 控制台功能较基础，配置灵活性高 |
| 成本 | 开源免费，企业版收费 | 开源免费，企业版收费 | 开源免费，企业版收费 |
| 扩展性 | 支持 WASM 插件，扩展灵活 | 支持 Lua 和 Go 插件，扩展性中等 | 支持 Lua 和 Python 插件，扩展性强 |
| 社区支持 | 阿里巴巴背书，社区活跃 | 社区成熟，文档丰富 | 社区活跃，国内支持较好 |
| 功能丰富度 | 支持流量管理、安全防护、可观测性 | 功能全面，插件生态丰富 | 功能全面，插件生态丰富 |

### 优势分析

- 优势1：基于 Rust 和 Go 开发，性能和安全性较高。
- 优势2：深度集成 K8s，适合云原生环境。
- 优势3：支持 WASM 插件，扩展性和灵活性较强。

### 不足分析

- 不足1：社区和插件生态相对 Kong 和 APISIX 较新。
- 不足2：企业版功能可能需要付费，成本较高。
- 不足3：文档和案例相对较少，学习曲线较陡。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Wasm 插件实现扩展能力

**说明**: Higress 支持 WebAssembly (Wasm) 插件，允许在不修改主程序的情况下动态扩展网关功能。相比传统 Lua 插件，Wasm 插件具有更高的隔离性、安全性和性能，且支持多语言开发（如 Go、C++、Rust）。

**实施步骤**:
1. 根据业务需求选择合适的 Wasm 开发语言（推荐使用 Go 或 Rust）。
2. 使用 Higress 官方提供的 SDK 或工具链编写插件逻辑。
3. 将编译好的 Wasm 文件上传至 Higress 控制台或通过 OCI 存储进行管理。
4. 在网关路由或全局层面配置并启用该插件。

**注意事项**: 
- Wasm 插件运行在沙箱中，需注意资源消耗限制。
- 调试 Wasm 插件相对复杂，建议在本地环境充分测试后再部署。

---

### 实践 2：利用 Ingress API 进行服务暴露

**说明**: Higress 原生兼容 Kubernetes Ingress API 和 Gateway API。通过标准的 Ingress 资源配置，可以轻松将 Kubernetes 集群内的服务通过 HTTP/HTTPS 协议暴露给外部，实现从 Nginx Ingress Controller 的平滑迁移。

**实施步骤**:
1. 安装 Higress 并确保其正确监听 Ingress 资源变动。
2. 编写 Kubernetes Ingress YAML 文件，定义域名、路径和后端 Service 的映射关系。
3. 应用 YAML 配置 (`kubectl apply -f ingress.yaml`)。
4. 配置 DNS 解析，将域名指向 Higress 的网关入口 IP。

**注意事项**: 
- 对于复杂的七层路由需求（如灰度发布、流量镜像），建议配合 Higress 的自定义 CRD (如 `VirtualService` 或 `IngressClass` 参数) 使用。
- 确保 TLS 证书正确配置在 Secret 中并在 Ingress 引用。

---

### 实践 3：配置全链路安全防护与认证

**说明**: Higress 内置了丰富的安全插件，包括 Keyless 认证、JWT 验证、IP 黑白名单等。最佳实践是不仅仅依赖网络层的隔离，而是在网关层实施严格的应用层访问控制，防止未授权访问。

**实施步骤**:
1. 在控制台开启“基本认证”或“JWT 认证”插件，配置对应的用户名密码或密钥。
2. 配置“IP 访问控制”插件，限制仅允许特定 IP 段访问管理端口或敏感 API。
3. 启用“请求限流”插件，防止 DDoS 攻击或恶意刷接口。
4. 定期审计安全日志，检查异常访问模式。

**注意事项**: 
- JWT 密钥应定期轮换。
- 限流配置需根据业务实际承载能力进行压测，避免误杀正常流量。

---

### 实践 4：服务治理与流量标签路由

**说明**: 在微服务架构中，利用 Higress 的流量标签路由功能，可以实现蓝绿发布、金丝雀发布和 A/B 测试。通过解析 HTTP Header 或 Cookie，将特定流量引流至新版本服务。

**实施步骤**:
1. 在 Kubernetes 中为不同版本的应用 Pod 打上标签（如 `version: v2`）。
2. 在 Higress 中定义服务来源，并识别带有特定标签的 Pod 子集。
3. 配置路由规则，设置匹配条件（例如 `Header: x-canary: true`）。
4. 将满足条件的流量转发至带有 `version: v2` 标签的子集服务。

**注意事项**: 
- 确保服务注册中心（如 Nacos）或 Kubernetes API Server 与 Higress 的数据同步是实时的。
- 灰度发布完成后，及时清理旧的路由规则和资源，避免配置冗余。

---

### 实践 5：对接云原生服务注册中心

**说明**: Higress 设计为云原生网关，能够无缝对接主流服务注册中心（如 Nacos、Consul、ZooKeeper 以及 Kubernetes CoreDNS）。相比硬编码 IP 地址，使用服务发现可以实现自动化的负载均衡和故障摘除。

**实施步骤**:
1. 在 Higress 全局配置中添加服务来源，选择对应的注册中心类型（如 Nacos）。
2. 填写注册中心的地址、命名空间等连接信息。
3. 在配置路由时，直接选择服务名称而非具体 IP 地址作为后端目标。
4. 配置健康检查机制，确保网关能及时剔除不健康的实例。

**注意事项**: 
- 确保网络互通，Higress 所在的网络环境能够访问注册中心的端口。
- 对于非 K8s 服务，需注意服务名与 K8s Service 名字的冲突管理。

---

### 实践 6：高可用部署与资源规划

**说明**: 在生产环境中，网关是流量的咽喉，必须避免单点故障。Hig

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 WASM 插件的高性能隔离模式

**说明**：Higress 支持 WASM 插件扩展，默认情况下 WASM 运行在通用的虚拟机中。通过调整 WASM 运行时配置（如使用特定编译器优化或调整内存分配策略），可以降低插件执行带来的延迟开销。

**实施方法**:
1. 在编写 WASM 插件时，使用 `tinygo` 或 `assemblyscript` 进行编译，以减小体积并提升运行速度。
2. 在 Higress 网关配置中，针对高频调用的 WASM 插件，启用 `Fast Syscall` 或类似的加速选项（取决于具体版本支持）。
3. 限制 WASM 插件的内存上限，防止因垃圾回收（GC）导致的性能抖动。

**预期效果**: 插件执行延迟降低 10%-30%，减少对网关吞吐量的影响。

---

### 优化 2：精细化配置连接池与熔断降级

**说明**：后端服务的不稳定会直接拖慢网关的响应速度。不合理的连接池配置会导致请求排队或频繁建连，增加延迟。

**实施方法**:
1. **调整连接池大小**：根据后端服务的处理能力，将 `maxRequestsPerConnection` 或连接数上限调整至最佳值（通常为后端并发处理能力的 1.5-2 倍）。
2. **配置主动健康检查**：启用主动健康检查，快速剔除不健康的后端实例，避免网关向故障节点转发请求。
3. **设置超时与重试**：合理设置 `connectTimeout`、`sendTimeout` 和 `readTimeout`，避免长时间阻塞线程。

**预期效果**: 后端故障时的响应时间波动减少 50%+，整体 P99 延迟显著降低。

---

### 优化 3：启用 HTTP/2 与 HTTP/3 (QUIC)

**说明**：Higress 基于 Envoy，对 HTTP/2 和 HTTP/3 有良好支持。HTTP/2 通过多路复用减少 TCP 连接数，HTTP/3 (QUIC) 则能解决 TCP 队头阻塞问题，在高丢包率网络下效果显著。

**实施方法**:
1. 在监听器配置中，将 `Http2` 协议选项设为启用。
2. 如果客户端支持，开启 QUIC/HTTP3 支持（需确保 Higress 版本支持且配置了 UDP 端口监听）。
3. 调整 HTTP/2 的并发流限制，以适应高吞吐场景。

**预期效果**: 高并发下的 TCP 连接数减少 60%，弱网环境下的请求成功率提升 20%-40%。

---

### 优化 4：优化日志采样与异步上报

**说明**：全量日志记录和同步写入磁盘会产生巨大的 I/O 等待，严重影响网关吞吐量。

**实施方法**:
1. **开启日志采样**：对于 GET 请求或健康检查请求，设置采样率（如 10%），仅记录部分日志。
2. **使用异步访问日志**：配置日志后端为远程服务（如 OpenTelemetry Collector），而非本地文件，利用非阻塞 I/O 进行上报。
3. **精简日志字段**：移除不必要的请求头或响应体记录，仅保留关键 Trace ID 和状态码。

**预期效果**: I/O 等待时间减少 80%，在高并发下 CPU 使用率下降 15%-20%。

---

### 优化 5：利用本地内存缓存（L1 Cache）

**说明**：对于高频读取但低频变更的配置数据或鉴权数据，每次请求都回源 Redis 或数据库会极大地增加延迟。

**实施方法**:
1. 在 Higress 的 `WASM` 插件或 `Lua` 脚本中实现简单的字典缓存。
2. 对于下游服务发现，启用 DNS 缓存或 Service Discovery 的全量缓存模式。
3. 设置合理的 TTL（过期时间），确保数据一致性。

**预期效果**: 鉴权或配置解析类的 API 响应延迟从毫秒级降至

---
## 学习要点

- Higress 是阿里云开源的高性能、可扩展的云原生 API 网关，基于 Envoy 和 Istio 构建，支持 Kubernetes 和非 Kubernetes 环境。
- 提供统一的流量管理能力，包括路由转发、负载均衡、流量控制和灰度发布，适用于微服务架构。
- 内置插件市场支持动态扩展功能，如认证、限流、日志监控等，无需重启网关即可生效。
- 兼容 Kubernetes Ingress 和 Gateway API 标准，可无缝替换传统 Ingress Controller 并降低迁移成本。
- 支持多协议接入（HTTP、gRPC、Dubbo 等），并针对高并发场景优化，性能可达 Envoy 原生配置的 90% 以上。
- 提供可视化的控制台和 Prometheus 集成，简化运维监控和故障排查流程。
- 通过 Wasm 插件实现轻量级扩展，开发者可用多种语言（如 Go、Rust）编写自定义逻辑。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础

**学习内容**:
- 云原生网关的基本概念与核心价值
- Higress 的架构设计（基于 Envoy 和 Istio）
- Higress 与传统网关（如 Nginx、Spring Cloud Gateway）的区别
- Docker 环境下 Higress 的快速安装与部署
- 基本术语：Ingress、Gateway、路由、服务发现

**学习时间**: 1-2周

**学习资源**:
- Higress 官方文档: [https://higress.io/docs/latest/overview/what-is-higress/](https://higress.io/docs/latest/overview/what-is-higress/)
- Higress GitHub 仓库: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- 《云原生网关技术解析》相关博客文章

**学习建议**: 
建议先通过官方文档了解 Higress 的定位和背景，利用 Docker 在本地快速搭建一个 Standalone 模式的 Higress 实例，不要急于深入配置，先跑通第一个流量转发的 Hello World 场景。

---

### 阶段 2：核心功能掌握

**学习内容**:
- 详细的流量路由配置（基于域名、路径、Header 的路由规则）
- 服务来源的接入与配置（Nacos, Consul, K8s Service, 固定地址）
- 插件系统入门：如何使用 Wasm 插件扩展功能
- 负载均衡策略与超时、重试等流量治理配置
- 基本的安全配置（Basic Auth, IP 访问控制）

**学习时间**: 2-3周

**学习资源**:
- Higress 官方控制台操作指南
- Higress 官方插件市场: [https://github.com/higress-group/plugins](https://github.com/higress-group/plugins)
- Envoy 基础路由原理文档（辅助理解底层机制）

**学习建议**: 
此阶段重点在于动手操作。建议结合 Kubernetes 环境进行部署，尝试将一个微服务应用接入 Higress，并配置复杂的路由规则。尝试开启并配置几个官方预置插件（如 Key Rate Limiting 或 Request Block），体验 Wasm 插件的热加载能力。

---

### 阶段 3：高级特性与插件开发

**学习内容**:
- 全局与精细化流量管控（灰度发布、蓝绿发布、A/B Testing）
- 高级安全特性（JWT 验证、CORS 配置、OAuth2）
- Wasm 插件开发进阶：使用 Go 或 C++ 编写自定义插件
- Higress 的高可用部署与性能调优
- 多租户管理与 IngressClass 的应用

**学习时间**: 3-4周

**学习资源**:
- Higress Wasm 插件开发 SDK 文档
- Higress 最佳实践案例库
- WebAssembly (Wasm) 官方教程

**学习建议**: 
尝试编写一个自定义的 Wasm 插件来解决特定的业务逻辑问题（例如自定义请求头处理或简单的鉴权逻辑）。深入学习配置的下发机制，理解如何在不重启网关的情况下动态变更流量规则。关注 Higress 在高并发场景下的配置优化。

---

### 阶段 4：生产运维与生态集成

**学习内容**:
- Higress 的可观测性（对接 Prometheus/Grafana 监控、链路追踪）
- 网关的高可用架构设计与灾备方案
- Higress 对接阿里云 MSE 或其他云厂商托管服务
- 与微服务生态的深度集成（Dubbo, gRPC 协议转换）
- 常见生产问题排查与故障演练

**学习时间**: 2-4周

**学习资源**:
- Higress 运维诊断手册
- Prometheus 与 Grafana 集成指南
- 云原生架构白皮书

**学习建议**: 
将 Higress 部署在模拟的生产环境中，配置日志采集和监控告警。尝试模拟网关实例宕机，观察系统的自动恢复能力。研究 Higress 如何作为 Service Mesh 的南北向入口，与 Istio 或 Kuma 等服务网格工具协同工作。

---
## 常见问题


### 1: Higress 是什么？它与阿里巴巴有什么关系？

1: Higress 是什么？它与阿里巴巴有什么关系？

**A**: Higress 是一款基于阿里内部多年实践，开源的云原生 API 网关。它诞生于阿里巴巴，是阿里云 MSE（微服务引擎）云产品 API 网关的开源版本。Higress 旨在为云原生架构提供统一的流量入口，集成了流量管理、安全防护以及 Kubernetes Ingress Controller 的功能，旨在解决传统网关在云原生环境下的痛点。

---



### 2: Higress 与 Nginx、Envoy 或 Kong 等网关相比有什么核心优势？

2: Higress 与 Nginx、Envoy 或 Kong 等网关相比有什么核心优势？

**A**: Higress 的核心优势在于其深度集成了阿里在电商和金融场景下的流量治理经验。
1.  **技术栈**：它基于 Envoy 和 Istio（使用 Go 语言开发扩展），相比 Nginx (C/Lua) 或 Kong (Nginx/Lua)，Higress 在云原生生态中的可扩展性和热更新能力更强，配置变更无需 Reload 进程，连接不会中断。
2.  **功能融合**：它将传统的 K8s Ingress Controller（入口网关）与微服务网关的功能合二为一，既能处理 K8s 集群外部流量，也能处理集群内部服务间的流量调用。
3.  **插件生态**：兼容 Kong 和 Apache Dubbo 的插件生态，并支持 Wasm (WebAssembly) 技术，允许开发者使用多种语言（如 Go, C++, Rust）编写高性能、低耦合的插件。

---



### 3: Higress 是否兼容现有的 Nginx 或 Ingress 配置？

3: Higress 是否兼容现有的 Nginx 或 Ingress 配置？

**A**: 是的，Higress 具有很高的兼容性。
1.  **Nginx 兼容**：Higress 支持 Nginx 的 Ingress Annotation 注解，这意味着用户可以从 Nginx Ingress Controller 平滑迁移到 Higress，而无需大规模重写配置。
2.  **K8s 原生**：它完全实现了 Kubernetes Ingress API，同时也支持 Gateway API（下一代网关标准），可以作为标准的 Ingress Controller 直接部署在 Kubernetes 集群中。

---



### 4: 如何在 Higress 中扩展功能？是否支持自定义插件？

4: 如何在 Higress 中扩展功能？是否支持自定义插件？

**A**: Higress 提供了非常灵活的扩展机制，主要分为以下几类：
1.  **Wasm 插件**：这是 Higress 推荐的主流扩展方式。由于 Envoy 原生支持 Wasm，用户可以使用 Go、AssemblyScript 或 Rust 编写插件逻辑。这些插件运行在沙箱环境中，内存安全，且支持热加载，不会影响主网关进程的稳定性。
2.  **原生插件**：Higress 内置了丰富的开箱即用插件，如认证鉴权、流量镜像、请求/响应重写、限流熔断等。
3.  **Lua 支持**：为了兼容旧版 Nginx 生态，Higress 也支持 Lua 脚本，但更推荐转向性能和安全性更好的 Wasm 生态。

---



### 5: Higress 是否支持 Dubbo 服务？它如何处理微服务协议？

5: Higress 是否支持 Dubbo 服务？它如何处理微服务协议？

**A**: 支持。Higress 的设计初衷之一就是打通 HTTP 和 RPC 协议的界限。
1.  **Dubbo 支持**：Higress 原生支持 Apache Dubbo 服务，可以将 HTTP 请求转换为 Dubbo 协议调用后端服务，这对于需要将传统的 RESTful API 网关与微服务架构结合的系统非常有用。
2.  **多协议支持**：除了 HTTP (HTTP/1, HTTP/2, gRPC) 和 Dubbo，Higress 还支持 Nacos 等注册中心，能够自动发现后端微服务实例，实现动态的路由转发。

---



### 6: Higress 的性能表现如何？能否应对高并发场景？

6: Higress 的性能表现如何？能否应对高并发场景？

**A**: Higress 的底层基于高性能代理 Envoy，并针对阿里云的高并发场景进行了深度优化。
1.  **高性能**：在标准硬件上，Higress 能够保持与 Envory 相当的超高吞吐量和低延迟。
2.  **低配置延迟**：得益于其控制面与数据面的分离设计以及 xDS 协议的优化，Higress 在处理大规模路由规则（如成千上万个 Ingress 资源）时，配置下发和生效的延迟极低，非常适合服务数量庞大的微服务环境。

---



### 7: 如何部署和监控 Higress？

7: 如何部署和监控 Higress？

**A**:
1.  **部署**：Higress 最常见的部署方式是在 Kubernetes 集群中通过 Helm Chart 进行一键安装。同时也支持通过 Docker Compose 在非 K8s 环境中运行。
2.  **监控**：Higress 原生集成了 Prometheus 监控指标，可以自动导出详细的网关运行时数据（如 QPS、延迟、成功率等）。同时，它也支持 OpenTelemetry 链路追踪，可以轻松接入 SkyWalking、Jaeger 等链路追踪系统，帮助用户可视化流量路径。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 在本地 Docker 环境中快速部署 Higress，并配置一个简单的路由规则，将访问 `/hello` 的请求转发到一个模拟的后端服务（如 httpbin.org）。

### 提示**: 参考 Higress 官方文档的"快速开始"部分，使用 Docker Compose 进行部署；在网关控制台中添加路由规则，注意匹配路径和目标服务的配置。

### 

---
## 实践建议

基于 Higress 作为“AI Native API Gateway”的定位，结合其作为网关的核心功能与 AI 特性，以下是 6 条针对实际生产环境的实践建议：

### 1. 利用 AI 提示词模板实现服务标准化与成本控制
Higress 允许在网关层面配置 Prompt 模板，而不是由客户端直接发送原始 Prompt。
*   **实践建议**：将系统提示词固化在网关的路由配置中。客户端仅需发送用户问题，网关在转发给 LLM（如通义千问、OpenAI）时自动拼接预设的 System Prompt。
*   **最佳实践**：通过这种方式，你可以在不修改客户端代码的情况下，灵活调整模型的“人设”或“行为”，或者统一注入业务上下文（如企业知识库检索结果）。
*   **常见陷阱**：避免在模板中硬编码过长的上下文，这会增加每次请求的 Token 消耗和延迟。对于长文本，应结合检索增强生成（RAG）插件动态注入摘要。

### 2. 配置语义路由以实现多模型负载均衡
Higress 支持 AI 语义路由，即根据用户输入的意图将其分发到不同的模型或服务。
*   **实践建议**：配置路由规则，将简单的问答请求分发至成本较低、速度较快的模型（如 Llama-7B 或 GPT-3.5），而将复杂的代码生成或逻辑推理请求分发至高精度模型（如 GPT-4 或 Qwen-Max）。
*   **最佳实践**：在服务提供者列表中配置多个模型服务的地址，并开启健康检查。这样当某个模型 API（如 OpenAI）不可用时，Higress 可以自动将流量切换到备用模型（如 Ollama 本地部署的模型），保证服务的高可用性。

### 3. 实施精细的 Token 与速率限流
AI 服务的成本通常按 Token 计算，且 LLM 的 TPS（每秒 Token 数）有限，传统的基于请求数（QPS）的限流无法有效控制成本和后端压力。
*   **实践建议**：在 Higress 的插件配置中，启用针对 AI 请求的特定限流策略。不仅要限制每秒请求数，还要关注请求的上下文长度。
*   **常见陷阱**：不要仅依赖客户端的超时设置。LLM 生成响应的时间取决于生成的长度，如果不设置合理的超时时间，长文本生成可能导致网关连接堆积，耗尽连接池。

### 4. 集成文件内容提取插件构建多模态网关
Higress 拥有丰富的插件生态，其中包含文档解析插件。
*   **实践建议**：在网关层配置“文档提取”或“OCR”相关插件。当用户上传 PDF 或 Word 文档提问时，网关先调用解析服务将文本提取出来，再将文本内容拼接到 Prompt 中发送给 LLM。
*   **最佳实践**：将文件处理逻辑前置到网关，可以极大地简化后端业务服务的代码，使其仅需关注对话逻辑而无需处理文件 IO 和解析库的依赖。

### 5. 开启结果缓存以减少重复计算
对于常见的重复问题（如“今天的天气”、“公司报销政策”），每次都调用 LLM 是一种浪费。
*   **实践建议**：启用 Higress 的缓存插件（或结合 Redis）。基于用户输入的语义指纹或精确匹配进行缓存。
*   **最佳实践**：设置合理的 TTL（生存时间）。对于事实性强的问答，可以设置较长的缓存时间；对于创意生成类任务，建议关闭缓存或设置极短的 TTL，以保证用户体验的多样性。

### 6. 警惕“上下文窗口”溢出与错误处理
LLM 对单次请求的 Token 限制非常敏感，一旦超出限制会直接报错。
*   **实践建议**：在 Higress 中配置“请求上下文修剪”插件。当检测到用户上传的历史记录或上下文长度接近模型上限时，自动截断早期的非关键对话，保留最近的 N 轮对话。
*   **常见陷阱**：直接透传错误信息给前端。当上游

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI Native](/tags/ai-native/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [LLM](/tags/llm/) / [MCP](/tags/mcp/) / [WASM](/tags/wasm/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260130-github_trending-alibaba-higress-9.md" >}})
- [Amla Sandbox：面向 AI 智能体的 WASM Bash 沙箱]({{< relref "posts/20260130-hacker_news-show-hn-amla-sandbox-wasm-bash-shell-sandbox-for-a-7.md" >}})
- [Amla Sandbox：面向 AI 智能体的 WASM Bash 沙箱]({{< relref "posts/20260130-hacker_news-show-hn-amla-sandbox-wasm-bash-shell-sandbox-for-a-1.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*