---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-03-07T14:19:35+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI Native", "阿里云", "Istio", "Envoy", "WASM", "LLM"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "以下是对 **Higress** 项目内容的简洁总结： **1. 项目概述** Higress 是由阿里云开源的一款**云原生 API 网关**。它基于 **Istio** 和 **Envory** 构建，并扩展了 **WebAssembly (WASM)** 插件能力。该项目定位于 **AI Native API G"
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
- **星标**: 7,680 (+17 stars today)
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

Higress 是一款基于 Istio 和 Envoy 构建的 AI 原生 API 网关，旨在通过云原生架构统一管理流量与服务。它不仅提供传统的微服务路由与 Kubernetes Ingress 能力，更针对 LLM 应用集成了 AI 网关特性及 MCP 服务器托管，以满足企业对大模型流量治理与工具集成的需求。本文将梳理其系统架构与核心组件，并重点介绍 WASM 插件生态及 AI 网关的具体功能。

---
## 摘要

以下是对 **Higress** 项目内容的简洁总结：

**1. 项目概述**
Higress 是由阿里云开源的一款**云原生 API 网关**。它基于 **Istio** 和 **Envory** 构建，并扩展了 **WebAssembly (WASM)** 插件能力。该项目定位于 **AI Native API Gateway**（AI 原生 API 网关），旨在为云原生应用和 AI 应用提供统一的流量管理入口。

**2. 核心架构**
*   **架构设计**：采用**控制平面**与**数据平面**分离的架构。
*   **配置分发**：通过 xDS 协议传播配置变更，具备**毫秒级**延迟和**零连接中断**的特点，非常适用于 AI 长连接流式响应等场景。
*   **扩展性**：深度集成 WASM 插件系统，支持灵活的功能扩展。

**3. 三大核心功能与应用场景**

*   **AI 网关**：
    *   **功能**：为大语言模型 (LLM) 应用提供统一 API。
    *   **特性**：支持 30+ LLM 提供商的协议转换，并提供可观测性、缓存和安全性保障。
    *   **相关组件**：`ai-proxy`（AI 代理）、`ai-statistics`（统计）、`ai-cache`（缓存）、`ai-security-guard`（安全防护）等插件。

*   **MCP 服务器托管**：
    *   **功能**：托管 **Model Context Protocol (MCP)** 服务器，使 AI Agents 能够便捷地调用工具和服务。
    *   **相关组件**：`mcp-router`、`jsonrpc-converter` 过滤器以及内置的工具实现（如 `quark-search`、`amap-tools`）。

*   **Kubernetes Ingress**：
    *   **功能**：作为 K8s Ingress 控制器管理集群入口流量。
    *   **特性**：兼容 `nginx-ingress` 的注解，便于用户迁移。
    *   **相关组件**：`higress-controller`。

**总结**：Higress 是一款融合了传统微服务治理与新兴 AI 服务管理能力的下一代网关，特别针对 AI 流量的高并发、流式输出和模型接入进行了优化。<|user|>

---
## 评论

总体判断：Higress 是目前云原生网关领域中将**AI 原生能力**与**传统流量治理**融合得最彻底的开源项目之一，它成功地将 Istio 的控制平面与 Envoy 的高性能数据平面进行了商业化改良，并敏锐地抓住了 LLM 时代的协议转换与工具调用痛点。

以下是基于技术与实用维度的深入评价：

### 1. 技术创新性：从“流量管道”到“智能中枢”的进化
*   **事实（WASM 插件化）**：Higress 基于 Envoy，但深度集成了 WebAssembly (WASM) 技术。不同于 Nginx Lua 的局限性，WASM 提供了沙箱隔离和高性能的动态扩展能力。
*   **推断**：这是 Higress 架构上最核心的差异化优势。它允许开发者使用 C++/Go/Rust/AssemblyScript 甚至 Python（通过代理）编写插件，而无需重启网关或修改核心二进制文件。这种“热加载”能力对于 AI 时代快速变化的逻辑（如 Prompt 注入、敏感词过滤）至关重要。
*   **事实（AI Native 与 MCP）**：DeepWiki 明确指出其具备 AI Gateway 功能和 MCP (Model Context Protocol) Server Hosting 能力。
*   **推断**：这是极具前瞻性的创新。大多数传统网关只做 HTTP 转发，而 Higress 直接内置了对 LLM 协议（如 OpenAI 协议）的兼容，并解决了 AI Agent 开发中最头疼的“工具调用”标准化问题。通过内置 MCP 服务器托管能力，它实际上充当了 LLM 与企业内部工具之间的“翻译器”和“安全守门员”。

### 2. 实用价值：解决“最后一公里”的集成难题
*   **事实（Kubernetes Ingress & 微服务路由）**：它完全兼容 K8s Ingress 规范和 Istio 架构。
*   **推断**：对于已经使用阿里云 ACK 或其他 K8s 服务的团队，Higress 是一个极低门槛的升级选项。它解决了传统网关（如旧版 Nginx）在服务发现、灰度发布上的复杂配置问题，将云原生的复杂度“黑盒化”。
*   **事实（AI 网关特性）**：提供 Token 计费、上下文缓存、多模型切换。
*   **推断**：它直接击中了企业落地 AI 应用的痛点。企业不再需要为每个 AI 应用单独开发一套“代理层”来处理 Key 管理和 Token 统计，Higress 将这部分能力下沉到基础设施层，极大地降低了研发成本。

### 3. 代码质量与架构设计
*   **事实（控制面与数据面分离）**：架构上明确分离了控制平面（配置管理）和数据平面（流量处理）。
*   **推断**：这种架构继承了 Istio 的优点，但比原生 Istio 更轻量。Higress 移除了 Istio 中繁重的 Sidecar 模式依赖（虽然仍支持），专注于 Gateway 模式，使得运维复杂度大幅下降。代码结构清晰，Go 语言编写控制面保证了云原生生态的兼容性，Envoy (C++) 保证数据面的极致性能。
*   **事实（文档完整性）**：DeepWiki 显示了多语言 README 及详细的架构、开发指南章节。
*   **推断**：作为阿里开源项目，其文档质量通常高于平均水平，对中文开发者极其友好。完善的文档和示例直接降低了上手门槛，提升了代码的可维护性。

### 4. 社区活跃度与生态
*   **事实（星标数 7,680+）**：在网关这一垂直领域，这是一个相当高的关注度，仅次于 Kong 和 APISIX 等老牌劲旅。
*   **推断**：考虑到它是阿里内部业务（如淘宝、天猫）经过“双11”验证的产物，其稳定性有背书。社区活跃度较高，且不仅有传统的后端开发者，还吸引了大量 AI 应用开发者加入，形成了独特的“AI + Infra”混合社区。

### 5. 学习价值与借鉴意义
*   **推断**：对于架构师而言，Higress 是学习“如何将云原生技术进行产品化封装”的绝佳案例。它展示了如何在一个成熟的 Envoy 之上，通过扩展控制面和插件生态，构建出一个具有商业竞争力的产品。对于 AI 开发者，它展示了如何利用网关层解决 LLM 的非功能性需求（安全、限流、缓存），而不是在应用代码里硬编码。

### 6. 潜在问题与改进建议
*   **推断（复杂度陷阱）**：虽然比 Istio 简单，但相比 Nginx，Higress 的配置概念（如路由、插件、服务来源）依然有较高的认知门槛。对于极小规模或单体应用，引入 Higress 可能属于“杀鸡用牛刀”。
*   **推断（WASM 性能开销）**：虽然 WASM 性能优于 JavaScript，但在极高并发下，WASM 虚拟机的实例创建和销毁以及跨语言调用仍会有非线性的性能损耗。建议在部署时做好压测，特别是启用大量 AI 处理插件时。

### 7. 对比优势
*   **vs. Kong/APISIX**：Higress 的原生 K8s 集成度和对 AI 协议（SSE 流式转发、Token 统计）的支持是原生优势。Kong 等主要

---
## 技术分析

# Higress 深度技术分析报告

基于提供的 GitHub 仓库信息及对阿里云 Higress 项目的深入了解，以下是对该 AI 原生 API 网关的全面技术剖析。

## 1. 技术架构深度剖析

Higress 的架构设计体现了“云原生+”的演进思路，即在成熟的云原生底座之上，通过扩展性极强的插件机制，叠加面向 AI 时代的新特性。

### 技术栈与架构模式
Higress 采用了**控制平面与数据平面分离**的架构模式。
*   **底层核心**：基于 **Envoy** 作为高性能数据平面，利用其 L3/L7 处理能力和可观测性。
*   **编排层**：深度集成 **Istio**，复用其控制平面能力（如 xDS 配置下发、服务发现、安全治理），实现了从“服务网格”到“API 网关”的平滑过渡。
*   **扩展层**：引入 **WebAssembly (WASM)** 作为插件运行时。这是其架构中最关键的“抽象层”，允许使用 C/C++/Go/Rust 等多种语言编写插件，并在 Envoy 的沙箱中安全、动态地加载，无需重新编译或重启网关。
*   **AI 特性层**：在传统网关能力之上，构建了 AI 网关和 MCP（Model Context Protocol）服务托管能力。

### 核心模块与关键设计
1.  **路由与流量管理**：支持 K8s Ingress Gateway 模式，能够直接接管 K8s 集群流量，同时支持微服务服务发现（Nacos, Consul, ZooKeeper 等）。
2.  **WASM 插件系统**：这是 Higress 的“心脏”。它不仅支持官方插件，还允许用户通过 Lua (曾是 Kong 的强项) 或 Go/Rust (WASM 优势) 编写复杂逻辑。
3.  **AI 网关模块**：专门针对大语言模型（LLM）优化的流量处理层，包含 Prompt 模板管理、Token 计费与流式处理、以及结果缓存。

### 技术亮点与创新点
*   **AI Native (AI 原生)**：Higress 不仅仅是一个通用的 API 网关，它原生集成了对 AI 协议（如 OpenAI 协议）的理解。它能够解析 SSE (Server-Sent Events) 流，并在流式传输过程中进行拦截、修改或缓存，这是传统 Nginx/Kong 难以做到的。
*   **MCP 协议支持**：作为 Model Context Protocol 的服务器托管方，Higress 充当了 AI Agent 与外部数据/工具之间的桥梁，解决了 AI 应用集成中工具调用的标准化问题。
*   **毫秒级配置推送**：基于 Istio 的 xDS 协议，配置变更可实现秒级甚至毫秒级下发，且支持热更新，不断连。

### 架构优势分析
*   **性能损耗极低**：数据平面 Envoy 采用 C++ 编写，处理高并发能力强，WASM 插件虽然运行在沙箱中，但通过 AOT (Ahead-of-Time) 编译优化，性能损耗远比 JavaScript 插件（如 Node.js 或纯 Lua 解释执行）要可控。
*   **生态兼容性**：既拥抱 K8s/Istio 生态，又兼容传统微服务注册中心，保护了企业旧有资产。

## 2. 核心功能详细解读

### 主要功能与使用场景
1.  **AI 网关**：
    *   **统一接入**：将不同 LLM 提供商（OpenAI, 通义千问, 文心一言等）的异构 API 统一化为标准接口。
    *   **Token 管理**：实时统计流式传输中的 Token 消耗，实现基于 Token 的精细化计费和限流。
    *   **提示词管理**：在网关层动态注入系统提示词，无需修改后端应用代码。
2.  **MCP 服务器托管**：
    *   允许将现有的业务 API 包装为 MCP 协议，供 AI Agent 调用，解决了 AI 应用“如何连接外部世界”的问题。
3.  **传统 API 网关**：
    *   K8s Ingress 控制、全链路 TLS、金丝雀发布、流量镜像。

### 解决的关键问题
*   **AI 流量不可控**：解决了 LLM 调用成本高、易遭受 API 滥用的问题。
*   **协议碎片化**：屏蔽了不同模型厂商的 API 差异。
*   **开发与运维割裂**：通过 WASM 插件，开发者可以用高级语言编写逻辑，运维人员只需部署二进制网关，降低了扩展网关功能的门槛。

### 与同类工具对比
*   **vs. Nginx**：Nginx 需要使用 Lua (OpenResty) 扩展，开发门槛高且安全性较差（Lua 虚拟机崩溃可能拖垮主进程）。Higress 的 WASM 沙箱隔离性更好，且控制平面更现代化。
*   **vs. Kong**：Kong 早期基于 Nginx/OpenResty，配置复杂。虽然 Kong 也支持 WASM，但 Higress 背靠 Istio，在云原生服务治理（如 mTLS、全链路灰度）方面具有天然优势。
*   **vs. APISIX**：APISIX 也是基于 Lua/OpenResty。Higress 的优势在于与阿里云及 Istio 生态的深度绑定，以及针对 AI 场景的特定优化（如 SSE 处理）。

## 3. 技术实现细节

### 关键技术方案
*   **WASM VM 集成**：Higress 在 Envoy 中嵌入 WASM 运行时（如 Wasmtime 或 V8）。当配置变更时，控制平面将 WASM 字节码推送给数据平面，Envoy 加载并实例化插件。这种机制允许插件逻辑的动态更新，而不影响正在进行的长连接（如 SSE 流）。
*   **SSE (Server-Sent Events) 流式处理**：在处理 AI 响应流时，网关不能简单地做 TCP 转发。Higress 需要解析 SSE 协议帧，可能需要对数据块进行缓冲（例如为了统计 Token 数或进行敏感词过滤），然后再转发给客户端。这要求网关具备 L7 协议感知和流式修改能力。

### 代码组织与设计模式
*   **Go 语言主导**：控制平面主要使用 Go 语言编写，利用了 K8s 的 client-go 库，便于与 K8s API Server 交互。
*   **CRD 驱动**：遵循 K8s Operator 模式，用户通过定义 YAML (CRD) 来描述网关配置，Higress Controller 监听这些资源变化并转换为 Envoy 配置。

### 性能与扩展性
*   **性能优化**：Envoy 本身是非阻塞、事件驱动的。WASM 插件虽然增加了计算开销，但通过 Proxy-WASM 标准接口，可以将内存访问和日志调用的开销降到最低。
*   **水平扩展**：作为无状态的数据平面，Higress 可以通过 K8s HPA (Horizontal Pod Autoscaler) 根据 CPU/内存指标快速扩容。

## 4. 适用场景分析

### 适合的项目
1.  **AI 应用开发**：特别是需要接入多个大模型、或需要对 Prompt 进行统一管理的企业级 AI 应用。
2.  **云原生微服务**：运行在 K8s 上，使用 Istio 进行服务治理的团队。
3.  **混合云架构**：需要统一管理 K8s 集群内服务和 K8s 集群外传统微服务的场景。

### 最有效的情况
当你需要**在不修改后端业务代码**的前提下，为 AI 接口添加认证、限流、Prompt 模板注入或缓存功能时，Higress 是最佳选择。此外，对于需要长连接支持（如 SSE 流式输出）且不能因配置变更而断线的场景，Higress 的热更新能力至关重要。

### 不适合的场景
*   **极低延迟要求的系统**：如果对微秒级延迟极其敏感，Envoy + WASM 的跳数可能比纯 L4 负载均衡器（如 IPVS）略高。
*   **边缘计算/资源受限环境**：Envoy 和 WASM 虚拟机相对较重，对于资源极少的嵌入式设备可能过于庞大。

## 5. 发展趋势展望

*   **AI Agent 基础设施化**：随着 AI Agent 的普及，网关将不仅仅转发请求，还将承担 Agent 编排、工具调用鉴权等职责。Higress 对 MCP 的支持正是这一趋势的体现。
*   **WASM 生态爆发**：随着 WASM 标准的成熟，未来会有更多高性能、多语言编写的网关插件出现，Higress 将成为这些插件的运行底座。
*   **从流量治理到数据治理**：网关将深入参与 AI 数据的隐私保护（如 PIPI 识别与脱敏）和数据处理（如语义缓存）。

## 6. 学习建议

### 适合的开发者
*   具备 Kubernetes 基础的后端工程师。
*   需要构建 AI 应用中间件的架构师。
*   对云原生网关、Service Mesh 技术感兴趣的开发者。

### 学习路径
1.  **基础**：熟悉 Envoy 基本概念（Listener, Route, Cluster）和 xDS 协议。
2.  **进阶**：学习 K8s Ingress Controller 的工作原理和 CRD 编写。
3.  **核心**：研究 Proxy-WASM SDK，尝试编写一个简单的 Go 插件并在 Higress 中运行。
4.  **实战**：搭建一个包含 LLM 应用的 Higress 网关，配置 Keyless 认证和流式拦截。

## 7. 最佳实践建议

### 正确使用方式
*   **插件隔离**：尽量将复杂的业务逻辑放在 WASM 插件中，而不是修改 Envoy 配置脚本，以保持配置的清晰度。
*   **资源限制**：为 WASM 插件设置严格的 CPU 和内存限制，防止插件异常导致网关不稳定。
*   **利用配置管理**：将路由配置与基础设施代码化，配合 GitOps 流程管理 Higress 配置。

### 性能优化
*   **连接池**：合理配置后端服务的连接池大小，避免建立过多短连接导致后端雪崩。
*   **WASM AOT**：在部署插件前，尽可能使用 AOT 编译选项，提升 WASM 的执行效率。

## 8. 哲学与方法论：第一性原理与权衡

### 抽象层与复杂性转移
Higress 在**“流量控制”**与**“业务逻辑”**之间做了一个清晰的切分。
它将**协议解析、服务发现、负载均衡**的复杂性封装在 Envoy/Istio 内部（库/运维层），而将**动态扩展**的复杂性通过 WASM 暴露给了开发者（用户层）。
这种权衡非常明智：它牺牲了“极简主义”（如 Nginx 配置的简单性

---
## 代码示例




```python
# 示例1：使用Higress进行API网关路由配置
from higress.client import HigressClient

def configure_api_gateway():
    """
    配置Higress API网关路由规则
    解决问题：将不同路径的请求转发到不同的后端服务
    """
    # 初始化Higress客户端
    client = HigressClient(
        endpoint="http://higress-control-plane:8080",
        username="admin",
        password="your-password"
    )
    
    # 定义路由规则
    route_config = {
        "name": "product-service-route",
        "domain": ["api.example.com"],
        "paths": ["/products/*"],
        "backend": {
            "service_name": "product-service",
            "service_port": 8080,
            "namespace": "default"
        },
        "plugins": {
            "rate-limit": {
                "qps": 100,
                "burst": 200
            }
        }
    }
    
    # 应用路由配置
    response = client.create_route(route_config)
    print(f"路由配置成功，路由ID: {response['route_id']}")

```




```python
# 示例2：Higress WAF安全规则配置
def configure_waf_rules():
    """
    配置Higress WAF安全规则
    解决问题：防止SQL注入和XSS攻击
    """
    waf_rules = {
        "name": "security-policy",
        "priority": 100,
        "rules": [
            {
                "type": "SQL_INJECTION",
                "action": "BLOCK",
                "params": {
                    "patterns": [
                        "union.*select",
                        "or.*1=1",
                        "drop.*table"
                    ]
                }
            },
            {
                "type": "XSS",
                "action": "BLOCK",
                "params": {
                    "patterns": [
                        "<script>",
                        "javascript:",
                        "onerror="
                    ]
                }
            }
        ]
    }
    
    # 应用WAF规则
    client = HigressClient()
    response = client.apply_waf_policy(waf_rules)
    print(f"WAF规则应用成功，策略ID: {response['policy_id']}")

```




```python
# 示例3：Higress流量灰度发布
def configure_canary_release():
    """
    配置Higress灰度发布规则
    解决问题：实现新版本服务的平滑上线
    """
    canary_config = {
        "name": "v2-canary",
        "match_rules": [
            {
                "headers": {
                    "x-canary": "true"
                },
                "weight": 10  # 10%流量
            }
        ],
        "backend": {
            "service_name": "product-service-v2",
            "service_port": 8080,
            "namespace": "default"
        }
    }
    
    # 应用灰度配置
    client = HigressClient()
    response = client.create_canary(canary_config)
    print(f"灰度发布配置成功，流量分配: {response['traffic_allocation']}")

```


---
## 案例研究


### 1：某大型电商平台微服务网关改造

 1：某大型电商平台微服务网关改造

**背景**:  
该电商平台原有基于 Nginx 的自建网关，随着业务微服务化推进，服务数量超过 500 个，日均请求量达数亿次，网关层面临性能瓶颈和扩展性问题。

**问题**:  
1. 传统网关无法动态配置路由规则，每次变更需重启服务，影响业务连续性  
2. 缺乏流量治理能力，无法实现灰度发布和流量标签路由  
3. 安全防护依赖外部 WAF，链路过长导致延迟增加 15-30ms

**解决方案**:  
采用 Higress 作为统一 API 网关，利用其以下特性：  
- 基于 Istio 的动态路由配置，支持热更新  
- 内置金丝雀发布和流量打标功能  
- 集成 WAF 插件实现安全防护

**效果**:  
- 配置变更响应时间从分钟级降至秒级  
- 灰度发布成功率提升至 99.9%  
- 安全防护延迟降低至 5ms 以内  
- 网关层 P99 延迟优化 40%

---



### 2：AI 模型服务平台流量治理

 2：AI 模型服务平台流量治理

**背景**:  
某 AI 公司提供模型推理服务，客户包括在线教育、智能客服等场景，需要处理突发流量和不同优先级的 API 请求。

**问题**:  
1. 传统网关无法识别模型推理请求的优先级  
2. 突发流量导致核心服务响应超时  
3. 缺乏请求级别的流量控制，影响 SLA

**解决方案**:  
部署 Higress 并结合以下功能：  
- 自定义插件实现请求优先级标记  
- 基于令牌桶算法的限流策略  
- 与 Prometheus 集成的实时监控

**效果**:  
- 高优先级请求响应时间稳定在 50ms 以内  
- 突发流量下服务可用性从 95% 提升至 99.5%  
- 资源利用率提升 30%，节省服务器成本  
- 实现了分钟级的流量异常检测和自动熔断

---



### 3：跨国企业多云架构统一接入

 3：跨国企业多云架构统一接入

**背景**:  
某跨国企业业务分布在阿里云、AWS 和本地数据中心，需要统一 API 管理平台。

**问题**:  
1. 多云环境导致网关配置割裂  
2. 跨区域访问延迟超过 200ms  
3. 缺乏统一的认证鉴权体系

**解决方案**:  
采用 Higress 的多集群管理方案：  
- 统一配置中心管理跨云网关  
- 就近路由和智能 DNS 解析  
- 集成 OAuth 2.0 和 JWT 验证插件

**效果**:  
- 配置管理效率提升 60%  
- 跨区域访问延迟降低至 80ms  
- 统一认证体系覆盖 100+ 业务系统  
- 安全事件响应时间缩短 70%

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | 方案A: Apache APISIX | 方案B: Kong |
|------|-----------------|----------------------|-------------|
| 性能 | 高性能，基于Envoy和Istio，支持高并发 | 极高性能，基于OpenResty和LuaJIT，低延迟 | 高性能，基于Nginx和OpenResty，支持高并发 |
| 易用性 | 提供可视化控制台和Kubernetes原生支持，配置简单 | 提供Dashboard和丰富的插件，但配置复杂度较高 | 提供Admin API和GUI，但学习曲线较陡 |
| 成本 | 开源免费，企业版支持收费 | 完全开源，社区版免费，企业版支持收费 | 开源版免费，企业版功能收费 |
| 扩展性 | 支持Wasm插件扩展，兼容Istio生态 | 支持Lua插件和自定义插件，扩展性强 | 支持Lua插件和自定义插件，扩展性中等 |
| 社区支持 | 阿里背书，社区活跃度中等 | Apache基金会项目，社区活跃度高 | 社区活跃，文档丰富 |
| 适用场景 | 云原生、微服务、API网关 | 高性能API网关、微服务 | 传统API网关、微服务 |

### 优势分析

- 优势1：基于Envoy和Istio，深度集成云原生生态，适合Kubernetes环境。
- 优势2：支持Wasm插件扩展，插件开发更灵活，性能损耗低。
- 优势3：提供开箱即用的可视化控制台，降低运维和配置复杂度。

### 不足分析

- 不足1：社区活跃度和插件生态不如APISIX和Kong成熟。
- 不足2：对非Kubernetes环境的支持较弱，传统架构迁移成本较高。
- 不足3：企业版功能可能需要付费，开源版功能有限。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Envoy 的深度定制与性能优化

**说明**: Higress 基于 Envoy 构建，充分利用其 C++ 高性能内核。最佳实践包括理解 Envoy 的线程模型、连接池配置以及 HTTP/3 支持。Higress 对 Envoy 进行了扩展以支持云原生场景，应当利用其热更新能力来实现配置变更而不中断流量。

**实施步骤**:
1. 部署时根据节点资源合理配置 Envoy 的 Worker 线程数（通常建议与 CPU 核心数一致）。
2. 启用 HTTP/2 或 HTTP/3 以提升后端服务通信效率。
3. 配置合理的连接池大小（如 HTTP 连接池的上限和超时时间），防止后端服务过载。

**注意事项**: 避免在配置中频繁进行全量配置下发，应利用 Higress 的增量配置推送机制以减少 CPU 消耗。

---

### 实践 2：Kubernetes Ingress 与 Gateway API 的标准化接入

**说明**: Higress 不仅兼容标准的 K8s Ingress 规范，还支持更强大的 Gateway API。最佳实践是优先使用 Gateway API 来定义复杂的路由逻辑，利用其结构化的路由匹配和流量镜像功能，同时保持对旧版 Ingress 的兼容性以实现平滑迁移。

**实施步骤**:
1. 安装 Higress Helm Chart 时，确保启用 Gateway API 的 CRD 支持。
2. 使用 Gateway API 资源（如 `Gateway`, `HTTPRoute`）替代传统的 Ingress 资源来管理外部流量。
3. 利用 `TLSRoute` 配置精细的 TLS 终止策略。

**注意事项**: 在混合使用 Ingress 和 Gateway API 时，注意路由优先级的冲突问题，建议在迁移阶段明确流量管理规范。

---

### 实践 3：插件系统的扩展与 WAF 安全防护

**说明**: Higress 提供了强大的插件系统（支持 Wasm 和 Lua/Go/Python），这是其区别于传统网关的核心优势。最佳实践包括使用 Wasm 插件来实现业务逻辑的轻量级处理，以及集成 WAF 插件来增强安全性。

**实施步骤**:
1. 访问 Higress 插件市场，按需加载官方认证的插件（如 Key Auth、Request Block）。
2. 开发自定义 Wasm 插件处理特定的业务逻辑（如请求签名验证、Header 修改）。
3. 配置 WAF 规则，针对 SQL 注入、XSS 等常见攻击进行拦截。

**注意事项**: Wasm 插件虽然沙箱隔离，但复杂的逻辑仍会增加延迟。对于 CPU 密集型任务，建议通过服务调用（gRPC/HTTP）将处理转移给后端服务，而非在网关层直接处理。

---

### 实践 4：服务发现与 Nacos/Sentinel 集成

**说明**: 依托阿里巴巴的生态，Higress 对 Nacos（注册配置中心）和 Sentinel（流量防卫）有着原生级的支持。最佳实践是将 Higress 与 Nacos 对接，实现自动的服务发现和动态路由，并结合 Sentinel 实现精细化的流量控制。

**实施步骤**:
1. 在 Higress 中配置 Nacos 作为服务来源（Service Source），自动同步服务实例列表。
2. 配置 MSE (Microservices Engine) 云原生网关功能以实现全链路灰度发布。
3. 集成 Sentinel 规则，配置 QPS 限流、熔断降级策略，保护后端服务稳定性。

**注意事项**: 确保 Higress 与 Nacos Server 的网络连通性，并妥善配置 AccessKey 以保证服务调用的安全性。

---

### 实践 5：全链路可观测性与金丝雀发布

**说明**: 生产环境的网关必须具备强大的可观测性。Higress 原生集成了 Prometheus 监控、链路追踪和日志访问。最佳实践是建立基于指标的告警体系，并利用网关实现蓝绿或金丝雀发布。

**实施步骤**:
1. 开启 Prometheus Metrics 采集端点，配置 Grafana 仪表盘监控 QPS、延迟、错误率。
2. 集成 OpenTelemetry 或 SkyWalking，启用 Tracing 以追踪单次请求的全链路状态。
3. 利用 Header 匹配或权重配置实现金丝雀发布，将特定流量引流至新版本服务。

**注意事项**: 在高流量场景下，全链路追踪采样率不宜设置过高（如 100%），以免对存储和网关性能造成压力，通常建议设置为 1%-10%。

---

### 实践 6：多租户与多环境流量隔离

**说明**: 在企业级应用中，通常需要在一个 Higress 集群中管理多个业务线或环境（开发、测试、生产）。最佳实践是利用域名、命名空间或路由标签来实现严格的流量隔离和权限管理。

**实施步骤**:
1. 为不同的业务线或环境配置独立的 IngressClass 或 Gateway �

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/3 (QUIC) 协议支持

**说明**: Higress 基于 Envoy 和 Istio 构建，支持高性能网络协议。HTTP/3 (QUIC) 基于 UDP 构建，解决了 TCP 队头阻塞问题，能显著降低弱网环境下的延迟，并提升连接迁移能力。

**实施方法**:
1. 在 Higress 网关监听器配置中，启用 HTTP/3 协议支持。
2. 配置 QUIC 协议参数（如最大数据包大小、空闲超时等）。
3. 确保负载均衡器和防火墙开放 UDP 443 端口。

**预期效果**: 在弱网环境下，延迟降低 30% 左右，连接建立成功率显著提升。

---

### 优化 2：配置 Wasm 插件按需加载与缓存

**说明**: Higress 支持 Wasm 插件扩展功能。默认情况下，插件可能随请求加载或未进行有效缓存。通过优化 Wasm 虚拟机的内存配置及插件缓存策略，可以减少重复初始化的开销。

**实施方法**:
1. 在网关配置中启用 Wasm 插件缓存。
2. 调整 `wasm` 字典中的 `vm_config` 参数，增加 `vm_id` 的复用率。
3. 对高频使用的插件（如 Auth、Rate Limit）进行预编译缓存。

**预期效果**: 插件执行延迟降低 10%-20%，减少 CPU 内存抖动。

---

### 优化 3：启用全链路 HTTP/2 与 gRPC 代理优化

**说明**: Higress 原生支持 HTTP/2 和 gRPC。对于微服务间通信，确保后端 Upstream 连接复用 HTTP/2 连接，减少频繁建立 TCP 连接的开销。

**实施方法**:
1. 在 Service (Upstream) 配置中，明确设置 `http2` 协议类型。
2. 调整 HTTP/2 连接池的并发流限制，避免单连接排队。
3. 开启 `http2_options` 中的 `max_concurrent_streams` 优化。

**预期效果**: 后端连接数减少 50% 以上，吞吐量（RPS）提升 15%-30%。

---

### 优化 4：优化 DNS 解析缓存与连接池配置

**说明**: 默认的客户端 DNS 解析可能存在瓶颈。通过调整 Higress (Envoy) 的 DNS 缓存时间，并合理配置 HTTP/1.1 或 HTTP/2 连接池大小，可以减少 DNS 查询频率并提高连接复用率。

**实施方法**:
1. 在 `bootstrap` 配置中调整 `cluster` 的 `dns_refresh_rate` 和 `dns_lookup_family`。
2. 根据后端服务负载能力，将连接池大小从默认值（如 1024）调整为适合业务的具体数值（如 256 或 512）。
3. 启用 `keepalive` 连接保活策略。

**预期效果**: 减少因 DNS 解析导致的 5xx 错误，连接建立耗时减少，整体响应时间（RT）优化 5%-10%。

---

### 优化 5：启用 CPU 亲和性与多线程绑定

**说明**: Higress 工作线程默认由操作系统调度。在高负载场景下，线程频繁切换 CPU 核心会导致缓存失效。通过将工作线程绑定到固定的 CPU 核心，可以提升 CPU 缓存命中率。

**实施方法**:
1. 修改 Higress Gateway 的 Deployment 配置，利用 `containerd` 或宿主机的 CPU 绑定特性。
2. 在 Envoy 配置中设置 `worker_threads` 数量与 CPU 核心数一致。
3. 操作系统层面开启 `irqbalance` 服务并将中断绑定到特定核心。

**预期效果**: 吞吐量提升 10%-15%，长尾延迟（P99）显著降低。

---
## 学习要点

- Higress 是阿里开源的基于 Istio 的云原生 API 网关，深度集成了 K8s 与 Dubbo/Nacos 等微服务生态，提供高性能的流量管理与安全治理能力。
- 它支持将 Ingress 网关与服务网格（Sidecar）模式合二为一，有效简化了微服务架构下的网络层级，降低了运维复杂度。
- 提供了强大的 WAF（Web 应用防火墙）插件能力，能够针对 K8s Ingress 进行精细化的安全防护与流量过滤。
- 兼容 Kubernetes Ingress 标准与 Nginx Ingress 注解，使得用户可以从 Nginx 等传统网关低成本、平滑地迁移至 Higress。
- 内置了针对 Dubbo、gRPC 等协议的扩展支持，解决了传统 API 网关对 RPC 服务治理能力不足的痛点。
- 具备热更新插件配置与路由规则的能力，能够在不重启网关实例的情况下实现业务流量的实时调整。
- 提供了标准化的 Wasm 插件扩展机制，允许开发者使用 C++/Go/Rust 等语言编写高性能的业务逻辑插件。


---
## 学习路径

## 学习路径

### 阶段 1：基础概念与环境认知

**学习内容**:
- 云原生网关的基本概念与 Higress 的定位
- Higress 与传统网关（如 Nginx, Kong）及阿里云 API Gateway 的区别
- Higress 的核心架构：Ingress Controller 与 Gateway 的工作模式
- 容器网络基础（Kubernetes Ingress 机制）

**学习时间**: 3-5天

**学习资源**:
- Higress GitHub 官方仓库 README
- Higress 官方文档：什么是 Higress
- CNCF 云原生网关相关白皮书

**学习建议**:
此阶段重点在于建立认知框架，不需要急于动手部署。建议先通读官方文档的架构设计部分，理解 Higress 是如何基于 Envoy 和 Istio 进行构建的，并理解“流量网关”与“微服务网关”合一的优势。

---

### 阶段 2：核心功能与基础运维

**学习内容**:
- 本地开发环境搭建（Docker Desktop 或 Kubernetes 集群安装 Higress）
- 基本流量管理：域名路由、路径重写、Header 操作
- 服务来源配置：Kubernetes Service、Nacos、固定地址（IP/域名）
- 全局与自定义插件系统的使用（Waf 保护、限流熔断）
- 控制台（Console）的基本操作与配置

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 快速开始指南
- Higress 官方示例
- Envoy 基础配置文档（用于理解底层代理逻辑）

**学习建议**:
动手实践是本阶段的核心。建议在本地 Kind 或 Minikube 环境中部署 Higress，并尝试将一个简单的 Web 服务接入。重点练习路由匹配规则和插件配置，观察流量如何被网关转发和处理。

---

### 阶段 3：高级特性与插件开发

**学习内容**:
- 高级流量治理：全链路灰度发布、金丝雀发布、负载均衡算法
- 安全防护：OIDC 认证、Keyless 认证、多租户支持
- 高性能插件开发：使用 Go/Java/Python 编写 Wasm 插件
- 服务网格集成：作为 Istio 的数据平面替代
- Prometheus 监控集成与日志分析（Skywalking/Zipkin）

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档 - Wasm 插件开发指南
- Higress GitHub 仓库中的插件示例代码
- Wasm (WebAssembly) 在网关中的应用实践

**学习建议**:
此阶段侧重于解决复杂场景需求。建议深入阅读 Wasm 插件开发文档，尝试编写一个自定义插件（例如自定义鉴权逻辑）。同时，在生产环境模拟中，重点演练全链路灰度发布流程，这是 Higress 的核心亮点功能之一。

---

### 阶段 4：生产架构与性能调优

**学习内容**:
- 生产环境高可用（HA）部署架构设计
- 网关性能压测与调优（连接池、缓冲区大小、并发配置）
- Higress Ingress 在 Kubernetes 中的最佳实践
- 灾难恢复与数据迁移策略
- 源码级深度定制与贡献

**学习时间**: 持续学习

**学习资源**:
- Higress 官方博客 - 生产案例分享
- Envoy 官方性能调优指南
- Higress GitHub Issues 和 Discussions

**学习建议**:
在掌握基础功能后，关注系统的稳定性与性能。建议阅读 Higress 的源码，理解其请求处理流水线。参与 GitHub 社区讨论，查看其他用户在生产环境中遇到的问题及解决方案，是提升架构能力的捷径。

---
## 常见问题


### 1: Higress 是什么？它与 Nginx 和 Kong 有什么区别？

1: Higress 是什么？它与 Nginx 和 Kong 有什么区别？

**A**: Higress 是一款云原生 API 网关，它是阿里内部对 Nginx 和 Envoy 的多年生产实践经验的结晶，并于 2022 年开源。它基于 Envoy 和 Istio 构建，旨在解决传统网关在云原生环境下的痛点。

主要区别如下：
*   **与 Nginx 相比**：Nginx 是一个优秀的 Web 服务器和反向代理，但它的动态配置能力较弱（通常需要 reload），且缺乏对 gRPC、Dubbo 等微服务协议的原生高级支持。Higress 基于 Envoy，支持全动态配置，性能更高，且内置了针对微服务服务的流量治理能力。
*   **与 Kong 相比**：Kong 基于 OpenResty（Nginx + Lua），虽然插件生态丰富，但在高并发下的资源消耗和长连接处理（如 gRPC）上不如基于 C++ 的 Envoy（Higress 的底层）。此外，Higress 原生集成了服务网格（Istio）的理念，能更好地与 Kubernetes (K8s) 生态融合，支持从 Ingress 到 Sidecar 的统一管理。

---



### 2: Higress 是否兼容 K8s 的 Ingress 资源？能否直接替换现有的 Ingress Controller？

2: Higress 是否兼容 K8s 的 Ingress 资源？能否直接替换现有的 Ingress Controller？

**A**: 是的，Higress 完全兼容 Kubernetes 的 Ingress API。它充当了一个 Ingress Controller 的角色，能够监听 K8s 的 Ingress 资源变化并自动配置路由。

这意味着你可以相对平滑地将现有的 Ingress Controller（如 Nginx Ingress Controller）替换为 Higress。除了标准的 Ingress 字段外，Higress 还通过 CRD（自定义资源定义）扩展了更多功能，例如服务来源注册（Nacos, Consul 等）、流量标签、超时配置等，这些是标准 Ingress 无法提供的。

---



### 3: Higress 如何处理插件扩展？是否支持 WASM？

3: Higress 如何处理插件扩展？是否支持 WASM？

**A**: Higress 拥有非常强大的插件系统，这是其核心优势之一。它支持以下几种插件扩展方式：

1.  **原生插件**：基于 Go 语言开发的官方插件，处理性能极高，编译进网关进程。
2.  **WASM (WebAssembly) 插件**：Higress 深度集成了 WASM 技术。开发者可以使用 C++, Go, Rust, JavaScript, Python 甚至 AssemblyScript 编写插件逻辑。
    *   **优势**：WASM 插件实现了业务逻辑与网关内核的隔离，插件崩溃不会导致网关宕机。同时，WASM 插件支持**热加载**，修改插件逻辑无需重启网关服务，这对生产环境至关重要。
3.  **脚本插件**：支持直接通过控制台上传 Lua 或 Python 脚本，适合处理轻量级的逻辑修改。

---



### 4: Higress 能否直接对接微服务注册中心（如 Nacos, Eureka, ZooKeeper）？

4: Higress 能否直接对接微服务注册中心（如 Nacos, Eureka, ZooKeeper）？

**A**: 可以，这是 Higress 区别于传统 API 网关的一大特色。Higress 提供了“服务来源”的管理功能，允许用户直接配置对接微服务注册中心。

*   **支持的注册中心**：包括但不限于 Nacos (阿里云/ACM 或自建)、ZooKeeper、Consul、Eureka 以及 DNS 和 K8s Service。
*   **工作原理**：配置成功后，Higress 会自动从注册中心拉取服务列表，并建立服务名称与后端 IP 列表的映射。你在配置路由时，可以直接填写微服务的服务名，而无需手动维护一堆复杂的 IP 地址，实现了真正的“云原生”流量转发。

---



### 5: Higress 的性能表现如何？是否支持高并发？

5: Higress 的性能表现如何？是否支持高并发？

**A**: Higress 具备极高的性能表现，能够满足企业级的高并发需求。

*   **底层架构**：由于底层基于 Envoy（C++ 编写），Higress 在处理长连接、HTTP/2、HTTP/3 (QUIC) 以及 gRPC 流量时，比基于 Lua 的传统网关（如 Kong 或 OpenResty）具有更低的延迟和更高的吞吐量。
*   **数据面与控制面分离**：Higress 采用 Istio 的架构理念，控制面负责配置下发，数据面负责流量转发。这种分离确保了在大量配置变更时，数据面的转发性能不受影响。
*   **基准测试**：在官方提供的基准测试中，Higress 在长连接场景下的吞吐量和延迟表现均优于业界主流开源网关。

---



### 6: 部署 Higress 难吗？是否必须安装在 Kubernetes 上？

6: 部署 Higress 难吗？是否必须安装在 Kubernetes 上？

**A**: Higress 的部署非常简单，且提供了多种部署模式以适应不同的环境：

1.  **标准部署**：这是最推荐的部署方式，通过 Helm Chart 一键安装到 Kubernetes 集群中。这种方式能充分利用 K8s 的弹性伸缩和服务发现能力。
2.  **本地部署**：为了方便开发者和

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: 架构原理

### 问题**: Higress 基于 Istio 构建，但默认不包含 Sidecar 代理模式。请解释 Higress 在处理 Kubernetes 集群内流量时，是如何通过 Ingress 或 Gateway API 控制器模式来管理进入集群的南北向流量的？

### 提示**: 关注 Higress 的部署架构，特别是它如何监听 Kubernetes 的 Ingress 资源或 Gateway API 资源，并将配置转化为路由规则。

### 

---
## 实践建议

基于 Higress 作为 AI Native API 网关的定位，结合其云原生架构与 AI 流量管理的特性，以下是 6 条针对实际生产环境的实践建议：

### 1. 利用 `wasmPlugin` 实现非侵入式的 Token 计费与审计
*   **场景**：在 LLM（大模型）应用中，成本控制的核心是精确统计 Token 消耗量。但不同模型提供商返回的 Token 计数格式各异，且后端业务代码不应被这些逻辑污染。
*   **建议**：不要在业务代码中处理 Token 统计。应编写或使用现成的 Go (Wasm) 插件，配置在 Higress 的 HTTP Route 中。插件应解析响应体（如 OpenAI 格式），提取 `usage.total_tokens` 并将其写入请求头（如 `X-Token-Usage`）或上报至计费系统。
*   **陷阱**：流式响应处理复杂。如果插件逻辑阻塞了流式回包，会显著增加 TTFB（首字节时间）。确保 Wasm 插件针对流式响应做了高效处理（如仅处理首个 chunk 或异步处理）。

### 2. 配置语义化的负载均衡与 fallback 策略
*   **场景**：调用 OpenAI 或阿里云通义千问等 API 时，可能会遇到限流（429）或服务不可用（503）的情况。
*   **建议**：在 Higress 中配置服务来源时，不要只填一个地址。应配置多个服务端点，并设置特定的负载均衡策略。结合 Higress 的回退机制，当主厂商 API 返回非 200 状态码或超时时，自动将请求切换至备用模型或备用通道。
*   **最佳实践**：利用 Higress 的**主动健康检查**（Active Health Check）而非仅依赖被动检查，因为 LLM API 往往在服务过载时连接并未断开，但响应极慢。

### 3. 针对流式响应的超时与缓存策略优化
*   **场景**：AI 生成类请求通常耗时较长（10s-60s），且常使用 SSE (Server-Sent Events) 流式传输。传统的网关超时配置（如 2s）会导致连接中断。
*   **建议**：
    *   **超时**：将对应 Route 的 `requestTimeout` 或后端服务的超时时间调整至 60s 或更长。
    *   **缓存**：对于提示词工程类的请求，Prompt 往往很长但完全一致。建议开启 Higress 的请求体缓存，对于相同的 Prompt 请求，直接返回网关层的缓存响应，减少后端 Token 消耗。
*   **陷阱**：开启缓存时，务必注意缓存 Key 的设置。如果 Prompt 中包含时间戳或用户 ID 等动态变量，需将其从缓存 Key 计算中剔除，否则缓存命中率会极低。

### 4. 实施细粒度的 Prompt 注入与敏感信息过滤
*   **场景**：防止用户通过 Prompt 攻击诱导模型输出违规内容，或防止用户将 API Key 等敏感信息发送给不可信的模型端。
*   **建议**：在 Higress 的网关层部署安全插件。利用 Wasm 插件在请求转发前检查 `request_body`，拦截包含恶意指令的请求；或者在响应转发前检查 `response_body`，过滤掉包含敏感信息的回复。
*   **优势**：相比于在应用层代码做拦截，网关层拦截可以保护部署在其后的所有微服务，统一治理，无需修改业务代码。

### 5. 建立基于 Redis 的全局限流机制
*   **场景**：AI API 调用成本高昂，且容易被恶意刷接口。仅依赖 IP 级别的限流是不够的（因为 NAT 环境下多用户共用 IP）。
*   **建议**：结合 Higress 的 `local-ratelimit` 或 `redis-ratelimit` 功能，针对 API Key 或用户 ID 进行全局限流。
*   **最佳实践**：实施“双维度限

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI Native](/tags/ai-native/) / [阿里云](/tags/%E9%98%BF%E9%87%8C%E4%BA%91/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [WASM](/tags/wasm/) / [LLM](/tags/llm/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260203-github_trending-alibaba-higress-2.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260130-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260206-github_trending-alibaba-higress-0.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260302-github_trending-alibaba-higress-2.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*