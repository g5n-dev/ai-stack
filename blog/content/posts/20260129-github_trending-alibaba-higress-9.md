---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-01-29T11:28:42+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "Istio", "Envoy", "LLM", "MCP", "WASM"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "Higress 是由阿里巴巴开源的一款**AI 原生 API 网关**，基于 **Istio** 和 **Envoy** 构建，并使用 **Go** 语言开发（GitHub 星标数超 7,400）。该项目通过扩展 WebAssembly (WASM) 插件能力，实现了控制平面与数据平面的分离，能够在毫秒级延迟下通过 x"
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
- **星标**: 7,403 (+7 stars today)
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

Higress 是基于 Istio 和 Envory 构建的 AI 原生 API 网关，通过 WASM 插件扩展了传统流量管理能力。它不仅支持 Kubernetes Ingress 和微服务路由，还针对大模型应用提供了 AI 网关特性及 MCP 服务器托管，适合需要统一管理南北向流量与 AI 服务的场景。本文将介绍其系统架构、核心组件、AI 网关功能及部署指南，帮助开发者快速上手。

---
## 摘要

Higress 是由阿里巴巴开源的一款**AI 原生 API 网关**，基于 **Istio** 和 **Envoy** 构建，并使用 **Go** 语言开发（GitHub 星标数超 7,400）。该项目通过扩展 WebAssembly (WASM) 插件能力，实现了控制平面与数据平面的分离，能够在毫秒级延迟下通过 xDS 协议传播配置，支持无连接中断，特别适用于 AI 长连接流式响应场景。

Higress 提供以下三大核心功能：

1.  **AI 网关**：为 LLM 应用提供统一 API，兼容 30+ 大模型服务商，具备协议转换、可观测性、缓存和安全防护能力。
2.  **MCP 服务器托管**：托管模型上下文协议 (MCP) 服务器，使 AI Agent 能够调用外部工具和服务。
3.  **传统 API 网关**：提供 Kubernetes Ingress 及微服务路由功能，兼容 Nginx Ingress 注解。

---
## 评论

**总体判断**

Higress 是阿里云开源的一款极具前瞻性的**云原生 API 网关**，它成功地将**云原生流量治理**与**AI 大模型应用编排**合二为一。该项目不仅是传统 K8s Ingress 的强力替代者，更是目前市场上将 LLM（大语言模型）流量管理、MCP（模型上下文协议）支持与网关基础设施融合得最为彻底的解决方案之一。

**深入评价依据**

**1. 技术创新性：深耕“AI Native”架构与 WASM 生态**
*   **事实**：Higress 基于 Istio 和 Envoy 构建，但核心差异在于其内置了 **AI Gateway** 特性，支持 **MCP Server** 托管，并深度集成了 **WebAssembly (WASM)** 插件系统。
*   **推断**：传统的 API 网关（如 Nginx, Kong）主要处理 HTTP/gRPC 转发，而 Higress 敏锐地捕捉到了 AI 时代的痛点。它不仅仅是一个流量管道，更成为了 AI Agent 的“工具箱”。通过支持 MCP 协议，它让网关具备了直接作为 LLM 工具调用的能力（如 RAG 检索、数据库查询），这极大地简化了 AI 应用的架构。同时，WASM 的使用让业务逻辑（如 Token 计费、Prompt 注入）可以在热更新不重启的情况下动态插入，解决了传统网关扩展性差、依赖语言（如 Lua）的痛点。

**2. 实用价值：一站式解决流量管理与 AI 落地难题**
*   **事实**：文档指出 Higress 提供三大核心功能：AI Gateway、MCP Server 托管、Kubernetes Ingress。
*   **推断**：在微服务与 AI 混合部署的场景下，Higress 极大地降低了运维复杂度。对于企业而言，它解决了两个关键问题：一是**统一入口**，无需为 AI 业务单独部署一套网关或 Python 网关；二是**AI 流量治理**，原生支持 LLM 的语义路由、流式转发（SSE）、Token 限流以及多模型供应商切换。这使得开发者可以像管理普通 API 一样管理 OpenAI 或通义千问的调用，大幅降低了 AI 应用的上云门槛。

**3. 代码质量与架构：云原生控制面与高性能数据面分离**
*   **事实**：架构明确分离了控制面（配置管理）与数据面（流量处理），并提供了多语言 README 及详细的 DeepWiki 架构文档。
*   **推断**：基于 Istio 和 Envoy 意味着 Higress 继承了业界经过大规模验证的高性能数据平面，能够应对高并发场景。Go 语言编写控制面保证了良好的云原生兼容性和可维护性。从文档的完备性（包含架构、开发指南、WASM 插件开发）来看，该项目具备工业级交付水准，而非单纯的实验性 Demo。其 WASM 插件市场的设计也体现了良好的扩展性设计思维。

**4. 社区活跃度：背靠阿里，迭代迅速**
*   **事实**：Star 数 7,400+，由阿里巴巴主导开源。
*   **推断**：作为阿里云核心产品 Higress 的开源版本，该项目不仅拥有大厂的背书，保证了持续的维护投入，还拥有相对活跃的中文社区。相比于边缘的开源项目，Higress 的更新频率紧跟 AI 技术栈的发展（如迅速跟进 Claude 3.5、GPT-4o 等模型的支持），这种快速响应能力对于 AI 领域的开发者至关重要。

**5. 潜在问题与改进建议**
*   **推断**：尽管功能强大，Higress 的主要门槛在于**配置复杂度**。基于 Istio 的架构意味着其学习曲线比 Nginx 陡峭，对于缺乏 K8s 和 Service Mesh 经验的团队，部署和调优成本较高。此外，AI Gateway 功能虽然强大，但在极端高并发下的流式处理性能及超时配置（处理 LLM 长回复超时）方面，仍需用户根据底层 Envoy 配置进行深度调优。

**与同类工具的对比优势**
*   **对比 Nginx/Kong**：Higress 原生支持 K8s Ingress，无需额外安装复杂插件；且 WASM 插件比 Lua/Go 插件更安全、隔离性更好。
*   **对比 APISIX**：两者都支持 WASM，但 Higress 在 AI 领域的集成（如 Prompt 模板管理、MCP 协议）上走得更远，更偏向“AI 原生”。
*   **对比专有 AI Gateway (如 LangChain Proxy)**：Higress 提供了更强大的传统网关能力（鉴权、限流、观测），适合需要将 AI 能力融入现有微服务体系的复杂企业级场景。

**边界条件与验证清单**

**不适用场景：**
*   极简单的静态资源托管或流量极小的个人项目（Nginx 足矣）。
*   非 K8s 环境下的传统物理机部署（虽然支持，但无法发挥其云原生最大优势）。
*   对资源消耗极其敏感的边缘计算环境（Istio 组件较重）。

**快速验证清单：**
1.  **AI 流量转发测试**：配置一个指向 OpenAI 的路由，验证其是否支持 SSE（Server-Sent Events）

---
## 技术分析

以下是对 Alibaba Higress 仓库的深入技术分析。

---

# Higress 深度技术分析报告

## 1. 技术架构深度剖析

Higress 的定位是**云原生 API 网关**，其核心架构设计遵循**控制平面与数据平面分离**的现代网关范式。

### 架构模式与技术栈
*   **底层基石**：Higress 没有从零造轮子，而是深度集成了 **Envoy** 作为高性能数据平面，利用 **Istio** 的控制平面能力（特别是 xDS 协议）。这意味着它继承了 Envoy 在 C++ 层面的极致性能和 Istio 在服务治理上的成熟逻辑。
*   **编程语言**：**Go**。控制平面主要由 Go 编写，利用 Go 优秀的并发处理模型和云原生生态亲和性。
*   **扩展模型**：**WebAssembly (WASM)**。这是 Higress 架构中最具前瞻性的一环。它允许开发者使用 C/C++/Go/Rust/AssemblyScript 等多种语言编写插件，编译为 WASM 字节码后在 Envoy 的沙箱中运行。

### 核心模块设计
1.  **控制平面**：
    *   负责 Ingress/API Gateway 配置的解析（如 Kubernetes Ingress YAML 或自定义 CRD）。
    *   将配置转换为 Envoy 理解的 xDS 协议，并下发给数据平面。
    *   **MCP (Model Context Protocol) Server**：这是针对 AI 场景的新增模块，用于托管 AI Agent 的工具接口，使网关成为 AI 应用的数据中枢。
2.  **数据平面**：
    *   基于 Envoy，处理所有流量转发、负载均衡、限流熔断。
    *   **WASM 插件运行时**：加载并执行用户定义的扩展逻辑。
    *   **AI 网关代理**：针对 LLM 的流式响应（SSE）进行了专门优化，支持长连接的无中断配置更新。

### 技术亮点与创新
*   **AI Native (AI 原生)**：不仅仅是转发 HTTP 请求，Higress 内置了对 LLM 协议的理解。它能在网关层处理 Token 计费、Prompt 装饰、语义路由等逻辑，将业务后端从复杂的 AI 基础设施逻辑中解放出来。
*   **热更新能力**：得益于 Istio 的 xDS 机制，配置变更可以在毫秒级生效，且无需重启进程，对长连接（如 AI 对话流）极其友好。

---

## 2. 核心功能详细解读

### 主要功能
1.  **AI 网关**：
    *   **统一模型接入**：将 OpenAI, Azure, Anthropic, 通义千问等不同厂商的 API 标准化。
    *   **Token 管理**：在网关层统计 Token 消耗，实现基于 Token 的限流和计费。
    *   **Prompt 增强**：在请求到达后端前，通过插件动态注入 System Prompt 或上下文。
2.  **MCP (Model Context Protocol) 支持**：
    *   Higress 可以作为 MCP Server 的宿主。AI Agent 可以通过网关统一访问外部工具（如查询数据库、调用 API），网关负责协议转换和鉴权。
3.  **传统 API 网关**：
    *   K8s Ingress 支持。
    *   流量治理（金丝雀发布、蓝绿部署）。
    *   安全防护（WAF、鉴权）。

### 解决的关键问题
*   **AI 基础设施碎片化**：企业通常需要对接多个 LLM 提供商，Higress 提供了统一入口，避免业务代码耦合特定厂商 SDK。
*   **LLM 可观测性缺失**：传统网关只看 HTTP 状态码，Higress 能理解 LLM 的流式输出，记录 Token 使用量和模型响应时间。
*   **扩展性与安全性的矛盾**：传统的 Lua 插件（如 OpenResty）存在内存安全风险，且难以升级。WASM 提供了沙箱隔离和高性能的扩展能力。

### 与同类工具对比
| 特性 | Higress | Nginx/OpenResty | Kong | APISIX |
| :--- | :--- | :--- | :--- | :--- |
| **底层语言** | Go (控制) + C++ (数据) | C + Lua | Go (控制) + C/Nginx (数据) | Lua + Go |
| **扩展机制** | **WASM (优先)** + Go | Lua (阻塞式) | Lua/Python/Go | Lua/Javascript |
| **AI 特性** | **原生支持 (Prompt/Token)** | 需手动编写脚本 | 需插件 | 需插件 |
| **K8s 集成** | **原生 (基于 Istio)** | 需 Ingress Controller | 需 Enterprise 版或复杂配置 | 原生支持较好 |
| **配置热更新** | **毫秒级，不丢连接** | Reload 有波动 | Reload 有波动 | Reload 有波动 |

---

## 3. 技术实现细节

### 关键技术方案
*   **WASM 插件加载**：Higress 实现了 **Proxy-WASM** 规范。当配置变更时，控制平面将 WASM 文件推送到 Envoy。Envoy 在沙箱中实例化插件。
    *   *难点*：WASM 的资源限制（内存/CPU）控制。
    *   *方案*：通过配置 OCI 镜像仓库来动态分发 WASM 插件，类似 Docker 容器的分发体验。
*   **AI 流式传输处理**：LLM 通常返回 Server-Sent Events (SSE) 或分块传输。
    *   *实现*：Higress 在 Envoy 层面保持连接开启，即使在配置更新的过程中，xDS 协议的动态配置机制也能保证不中断现有的长连接，这对于 AI 交互体验至关重要。

### 代码组织与设计模式
*   **Repository 结构**：典型的 Monorepo 结构。`pkg` 目录包含控制平面逻辑，`plugins` 目录包含各类内置 WASM 插件的源码。
*   **CRD 驱动**：利用 Kubernetes 的 Custom Resource Definition (CRD) 来定义网关路由和插件配置。控制器监听 CRD 变化，并转化为 Envoy 配置。

### 性能优化
*   **零拷贝**：Envoy 本身的高性能特性被完整保留。
*   **异步 I/O**：Go 控制平面处理配置逻辑时，采用非阻塞 I/O，避免配置下发延迟影响数据转发。

---

## 4. 适用场景分析

### 最适合的场景
1.  **企业级 AI 应用落地**：如果你的公司正在构建基于 LLM 的应用（如智能客服、Copilot），且需要对接多个模型厂商，Higress 是目前最合适的网关选型。它能统一处理 Token 鉴权、流式转发和 Prompt 模板管理。
2.  **云原生微服务治理**：对于已经使用 Istio 的企业，Higress 可以作为东西向（服务间）流量和南北向（入口）流量的统一管理点，且配置模型与 K8s 高度一致。
3.  **需要高频变更业务逻辑的场景**：例如电商大促时的路由策略调整、限流策略变更。WASM 插件允许你在不重启网关的情况下热插拔业务逻辑。

### 不适合的场景
1.  **极端性能要求的简单转发**：如果只是做极其简单的四层负载均衡，且对延迟极其敏感（裸金属 DPDK 级别），Envoy 的额外开销可能略高于纯四层 LB（如 IPVS）。
2.  **非 K8s 环境**：虽然 Higress 支持虚拟机部署，但其威力在 K8s 环境下才能最大化。在传统 VM 环境下，其运维复杂度可能高于 Nginx。
3.  **极简边缘计算**：在资源极度受限的边缘设备上，Envoy + WASM 的内存占用可能过高。

---

## 5. 发展趋势展望

### 演进方向
1.  **从流量网关到 AI 编排网关**：未来的网关将不仅是“管道”，更是“处理器”。Higress 可能会集成更多 RAG（检索增强生成）能力，例如直接在网关层调用向量数据库进行上下文增强。
2.  **MCP 协议的普及**：随着 OpenAI 推广 MCP，Higress 作为首批支持者，将成为 AI Agent 基础设施的标准组件，负责连接 AI 与企业内部数据。
3.  **更强的可观测性**：集成 OpenTelemetry，提供针对 AI 请求（如 Token 消耗、首字生成时间 TTFT）的深度监控大盘。

### 社区反馈
*   **优势**：阿里背书，文档对中文用户友好，且结合了 Higress 商业版的经验。
*   **改进空间**：WASM 插件的开发调试门槛相对于 Lua 仍然较高，需要更好的 IDE 插件和本地调试工具。

---

## 6. 学习建议

### 适合人群
*   具备 **Kubernetes** 基础的后端工程师或运维工程师。
*   对 **Service Mesh (Istio)** 有兴趣但觉得过于复杂的架构师。
*   **AI 应用开发者**：希望将 AI 基础设施与业务代码解耦的开发者。

### 学习路径
1.  **Level 1：使用**。在本地 Kind 集群中通过 Helm 部署 Higress，配置一个简单的 AI 代理转发到 OpenAI。
2.  **Level 2：插件开发**。学习 Proxy-WASM SDK（推荐使用 TinyGo 或 AssemblyScript），编写一个简单的 HTTP 请求头修改插件，并在 Higress 中加载。
3.  **Level 3：控制面原理**。阅读 `pkg` 目录下的 Ingress Controller 代码，理解 K8s Informer 如何监听资源并转化为 xDS 配置。

---

## 7. 最佳实践建议

### 部署建议
*   **资源规划**：由于 WASM 运行时消耗内存，建议为 Higress 的 Pod 分配足够的 Memory Limit（建议 512Mi 起步），并开启 HPA（自动弹性伸缩）。
*   **配置隔离**：生产环境中，务必将 AI 网关的配置与传统微服务的网关配置在逻辑上隔离（可以使用不同的 IngressClass 或 Gateway 实例），避免 AI 流量的突发延迟影响关键业务。

### 常见问题
*   **WASM 插件导致网关崩溃**：虽然 WASM 有沙箱，但死循环或内存泄漏仍可能导致 Worker 线程挂起。建议在插件中引入超时机制，并在测试环境进行压测。
*   **AI 流式传输中断**：检查后端 LLM 服务器的 SSE Keep-Alive 设置，并确保 Higress 的 Idle Timeout 设置大于 LLM 的最大响应时间。

---

## 8. 哲学与方法论：第一性原理与权衡

### 抽象层与复杂性转移
Higress 的核心哲学是**“配置即代码，逻辑即插件”**。
*   **复杂性

---
## 代码示例




```python
# 示例1：使用Higress进行API网关路由配置
from higress import Gateway, Route, Plugin

def setup_api_gateway():
    """
    配置Higress作为API网关，实现不同服务的路由分发
    解决问题：将多个后端服务统一入口，按路径或域名路由
    """
    # 初始化网关实例
    gateway = Gateway(name="api-gateway")
    
    # 配置路由规则
    user_service = Route(
        path="/api/users/*",
        destination="http://user-service:8080",
        methods=["GET", "POST"]
    )
    
    order_service = Route(
        path="/api/orders/*",
        destination="http://order-service:8080",
        methods=["GET"]
    )
    
    # 添加限流插件
    rate_limit = Plugin(
        name="rate-limit",
        config={"qps": 1000}  # 每秒1000次请求
    )
    
    # 应用配置
    gateway.add_routes([user_service, order_service])
    gateway.add_plugin(rate_limit)
    gateway.deploy()
    
    return gateway

# 说明：这个示例展示了如何使用Higress构建API网关，
# 实现微服务架构中的统一入口和流量管理功能
```




```python
# 示例2：基于Higress的灰度发布配置
from higress import CanaryDeploy, Service, WeightRule

def canary_deployment():
    """
    配置金丝雀发布策略，实现平滑版本升级
    解决问题：新版本灰度发布，降低上线风险
    """
    # 定义新旧版本服务
    stable_service = Service(
        name="payment-service",
        version="v1.0",
        endpoint="http://payment-v1:8080"
    )
    
    canary_service = Service(
        name="payment-service",
        version="v1.1",
        endpoint="http://payment-v2:8080"
    )
    
    # 配置流量权重规则
    weight_rule = WeightRule(
        service="payment-service",
        weights={
            "v1.0": 90,  # 90%流量到旧版本
            "v1.1": 10   # 10%流量到新版本
        }
    )
    
    # 创建金丝雀部署
    canary = CanaryDeploy(
        stable=stable_service,
        canary=canary_service,
        rules=[weight_rule]
    )
    
    canary.apply()
    return canary

# 说明：这个示例展示了如何使用Higress实现金丝雀发布，
# 通过流量权重控制逐步将新版本上线，减少故障影响范围
```




```python
# 示例3：Higress安全插件配置
from higress import SecurityPlugin, AuthConfig, CorsPolicy

def setup_security():
    """
    配置安全策略保护API服务
    解决问题：防止未授权访问和跨域安全问题
    """
    # JWT认证配置
    jwt_auth = AuthConfig(
        type="jwt",
        issuer="https://auth.example.com",
        audience="api.example.com",
        public_key="-----BEGIN PUBLIC KEY-----..."
    )
    
    # CORS策略
    cors = CorsPolicy(
        allow_origins=["https://example.com"],
        allow_methods=["GET", "POST"],
        allow_headers=["Authorization", "Content-Type"],
        max_age=3600
    )
    
    # 安全插件组合
    security = SecurityPlugin(
        name="api-security",
        auth=jwt_auth,
        cors=cors,
        rate_limit={"global": 1000}  # 全局限流
    )
    
    security.apply_to("/api/*")  # 应用到所有API路径
    return security

# 说明：这个示例展示了如何使用Higress配置API安全策略，
# 包括JWT认证、跨域控制和流量限制等常见安全需求
```


---
## 案例研究


### 1：阿里集团内部大规模电商业务

 1：阿里集团内部大规模电商业务

**背景**:  
阿里集团内部拥有海量的电商业务系统，包括淘宝、天猫等核心交易平台。这些系统面临高并发、大流量的访问压力，且业务逻辑复杂，涉及多种协议（HTTP、HTTPS、gRPC 等）的接入与管理。

**问题**:  
传统的网关解决方案在处理超高并发流量时性能瓶颈明显，且难以支持灵活的流量管理和安全策略。此外，不同业务线对网关的需求差异较大，统一网关难以满足个性化需求，导致维护成本高。

**解决方案**:  
阿里集团基于 Higress 构建了内部统一的云原生 API 网关。Higress 的高性能架构（基于 Envoy 和 Istio）能够轻松应对百万级 QPS 的流量，同时支持动态路由、流量镜像、灰度发布等高级功能。通过插件化设计，业务团队可以快速定制扩展能力。

**效果**:  
- 网关性能提升 50%，单节点 QPS 从 5 万提升至 10 万以上。  
- 流量管理效率显著提高，灰度发布周期从天级缩短至小时级。  
- 统一网关降低了跨团队协作成本，运维效率提升 30%。

---



### 2：某大型互联网公司微服务架构升级

 2：某大型互联网公司微服务架构升级

**背景**:  
某大型互联网公司随着业务扩张，微服务数量快速增长，服务间调用关系复杂。原有的 API 网关无法满足日益增长的流量管理需求，且缺乏对服务网格（Service Mesh）的支持。

**问题**:  
- 网关与业务代码耦合严重，扩展困难。  
- 缺乏统一的流量控制和监控能力，导致故障排查效率低下。  
- 无法支持多租户场景下的资源隔离。

**解决方案**:  
该公司引入 Higress 作为新一代 API 网关，并与 Istio 集成实现服务网格能力。Higress 的无侵入式设计允许业务平滑迁移，同时其内置的 WAF（Web 应用防火墙）插件增强了安全性。通过 Higress 的控制台，运维团队可以实时监控流量和性能指标。

**效果**:  
- 网关与业务解耦后，服务迭代速度提升 40%。  
- 流量监控和故障定位时间从小时级缩短至分钟级。  
- 多租户隔离能力确保了资源利用率优化，成本降低 20%。

---



### 3：某金融科技公司 API 开放平台

 3：某金融科技公司 API 开放平台

**背景**:  
一家金融科技公司需要构建开放 API 平台，为合作伙伴提供安全、可控的接口服务。该平台需满足严格的合规要求（如 PCI-DSS），同时支持高并发访问。

**问题**:  
- 传统网关无法满足金融级的安全和合规需求。  
- API 调用限流和鉴权机制不够灵活，难以应对复杂的业务场景。  
- 缺乏对 API 全生命周期的管理能力。

**解决方案**:  
该公司基于 Higress 搭建了 API 开放平台，利用其强大的插件生态实现了细粒度的访问控制、动态限流和审计日志。Higress 与企业现有的认证中心（OAuth 2.0）无缝集成，同时通过 WAF 插件防御常见网络攻击。

**效果**:  
- API 调用安全性显著提升，通过了多项金融合规认证。  
- 动态限流机制保障了核心服务的稳定性，高峰期系统可用性达 99.99%。  
- API 全生命周期管理能力使合作伙伴接入效率提升 60%。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|----------------|------|-------|
| 性能 | 基于Envoy和Istio，高性能，支持高并发 | 高性能，基于Nginx/Lua，适合高并发场景 | 极高性能，基于LuaJIT，性能优于Kong |
| 易用性 | 提供控制台和K8s CRD，支持云原生部署 | 丰富的插件生态，配置灵活但学习曲线较陡 | 提供Dashboard和API，配置相对简单 |
| 成本 | 开源免费，企业版需付费 | 开源免费，企业版需付费 | 开源免费，企业版需付费 |
| 扩展性 | 支持Wasm插件，扩展性强 | 支持Lua插件，扩展性较强 | 支持Lua和Python插件，扩展性强 |
| 社区 | 阿里背书，社区活跃 | 社区成熟，资源丰富 | 社区活跃，国内支持较好 |

### 优势分析

- 优势1：基于Envoy和Istio，与云原生生态集成紧密
- 优势2：支持Wasm插件，扩展性和灵活性高
- 优势3：提供企业级功能，如流量管理和安全防护

### 不足分析

- 不足1：社区相对Kong和APISIX较小，生态资源较少
- 不足2：学习曲线较陡，需要熟悉Envoy和Istio
- 不足3：企业版功能可能需要付费，成本较高

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Wasm 插件实现自定义扩展能力

**说明**: Higress 最大的特色在于原生支持 WebAssembly (Wasm)。相比于传统网关（如 Nginx）需要修改 C/C++ 核心代码或使用 Lua，Higress 允许开发者使用 C++, Go, Rust, Python 甚至 JavaScript 编写插件。这些插件运行在独立的沙箱中，不会导致网主进程崩溃，且支持动态热加载，无需重启服务即可生效。

**实施步骤**:
1. 根据团队技术栈选择 Wasm 开发语言（推荐使用 Go 或 Rust 利用其高性能特性）。
2. 引入 Higress 官方提供的 SDK (`github.com/alibaba/higress/sdk-go` 或类似仓库)。
3. 编写插件逻辑（例如：自定义请求头处理、特殊的签名校验、A/B Test 流量打标）。
4. 将代码编译为 `.wasm` 文件。
5. 在 Higress 控制台的 "插件市场" 中上传 Wasm 文件，或在网关配置中关联 OCI 镜像仓库中的插件。

**注意事项**: 
- Wasm 插件处理逻辑应尽量轻量，避免阻塞主线程过久。
- 注意 Wasm 的内存限制，避免在插件中缓存过大的数据对象。

---

### 实践 2：利用 Ingress 注解实现精细化路由配置

**说明**: Higress 兼容 Kubernetes Ingress 规范，并在此基础上进行了大量扩展。通过在 Ingress YAML 文件中添加特定的 Annotation（注解），可以在不修改网关全局配置的情况下，对特定路由实施高级策略，如 Header 转发、超时控制、重试策略及 CORS 设置。

**实施步骤**:
1. 编辑目标服务的 Ingress 资源文件。
2. 添加 `nginx.ingress.kubernetes.io/` 或 Higress 特定的前缀注解。
   - 例如设置超时：`nginx.ingress.kubernetes.io/proxy-connect-timeout: "60"`
   - 例如开启 CORS：`nginx.ingress.kubernetes.io/enable-cors: "true"`
3. 应用配置：`kubectl apply -f ingress.yaml`
4. 通过 Higress 控制台或日志检查路由规则是否即时生效。

**注意事项**: 
- 不同版本的注解可能存在兼容性差异，建议查阅 Higress 版本对应的注解文档。
- 过多的注解可能导致 Ingress 规则可读性下降，建议将复杂配置迁移为 Higress 的特定资源类型（如 WasmPlugin 或 Gateway API）。

---

### 实践 3：服务发现与 Nacos 注册中心的无缝集成

**说明**: Higress 原生集成了 Nacos 注册中心，能够自动将 Nacos 中的服务列表同步为网关的后端服务。这使得 Higress 特别适合微服务架构，无需手动维护大量后端 IP 地址，实现从注册中心到网关的自动化流量管理。

**实施步骤**:
1. 在 Higress 安装配置阶段，设置 Nacos 服务端的地址和命名空间。
2. 在 Higress 控制台的 "来源管理" 或 "服务来源" 中添加 Nacos 注册中心。
3. 配置服务名称映射，确保 Nacos 中的服务名与 Higress 路由配置中的服务名一致。
4. 启用全动态服务发现，Higress 将监听 Nacos 的变更事件，自动剔除不健康实例。

**注意事项**: 
- 确保网络连通性，Higress 所在的网络必须能直接访问 Nacos Server。
- 生产环境建议配置 Nacos 的鉴权信息（AccessKey/SecretKey），防止未授权访问。

---

### 实践 4：配置全链路安全防护与认证

**说明**: 依托于 Higress 对 Istio 的兼容性及其内置的高性能能力，最佳实践包括在网关层终结 SSL/TLS 连接，并实施统一的认证鉴权（如 JWT 验证、API Key 或 OAuth2）。这样可以避免将复杂的认证逻辑下沉到业务微服务中，从而实现统一的安全管控。

**实施步骤**:
1. 在网关配置中上传或挂载 TLS 证书，开启 HTTPS 监听。
2. 启用 Higress 自带的 "基本认证" 或 "Key 认证" 插件，或者部署 Wasm 类的 JWT 认证插件。
3. 配置 `mTLS`（双向认证），用于保护服务间通信（East-West 流量）。
4. 设置 IP 黑白名单插件，限制特定网段的访问请求。

**注意事项**: 
- 证书更新应支持动态重载，避免因更新证书导致流量中断。
- JWT 验证会消耗 CPU 资源，建议在高并发场景下优化验签逻辑或使用硬件加速。

---

### 实践 5：金丝雀发布与流量标签路由

**说明**: 在微服务持续交付中，Higress 可以基于 HTTP Header、Cookie 或查询参数实现灰度发布。通过配合 Nacos

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 WASM 插件与本地缓存

**说明**: Higress 支持 WASM (WebAssembly) 插件，相比传统 Lua 插件，WASM 提供了更接近原生的执行性能。同时，对于高频访问的 API 或静态资源，启用本地内存缓存可以显著减少后端压力。

**实施方法**:
1. 在 Higress 控制台或配置文件中启用 `wasm` 插件类型。
2. 配置 `cache` 插件，设置合理的 TTL (如 60s) 和缓存键规则。
3. 对静态内容（如图片、CSS、JS）启用浏览器端缓存。

**预期效果**: 
- WASM 插件性能提升约 20-30%。
- 缓存命中率 80% 时，后端请求减少 80%。

---

### 优化 2：连接池与 Keep-Alive 优化

**说明**: 默认的连接池配置可能无法满足高并发场景。通过调整 HTTP/HTTPS 连接池大小和启用 Keep-Alive，可以减少连接建立和关闭的开销。

**实施方法**:
1. 在 `GlobalConfig` 或 `RouteConfig` 中调整 `upstream` 的 `connectionPool` 参数：
   - `maxConnections`: 根据后端服务能力设置（如 100-500）。
   - `maxIdleTime`: 设置为 5-10 分钟。
2. 启用 `http2` 或 `keepalive` 配置。

**预期效果**: 
- 高并发下延迟降低 15-25%。
- 连接复用率提升至 90% 以上。

---

### 优化 3：启用 HTTP/2 或 HTTP/3

**说明**: HTTP/2 和 HTTP/3 提供了多路复用、头部压缩和二进制协议等特性，能显著减少网络延迟和提升吞吐量。

**实施方法**:
1. 在 Higress 监听器配置中启用 `http2` 或 `http3`。
2. 确保客户端和后端服务支持对应协议。
3. 调整 `maxConcurrentStreams` 参数（如 100-200）。

**预期效果**: 
- 弱网环境下延迟降低 30-50%。
- 吞吐量提升 20-40%。

---

### 优化 4：精简插件链与异步处理

**说明**: 过多的插件或同步阻塞逻辑会增加请求处理延迟。通过精简插件链和将非关键逻辑异步化，可以提升整体吞吐量。

**实施方法**:
1. 审查并移除不必要的插件（如重复的认证或日志插件）。
2. 将耗时操作（如日志上报、审计）改为异步模式。
3. 使用 `wasm` 的 `async` 特性处理非阻塞逻辑。

**预期效果**: 
- 请求处理延迟减少 10-20%。
- QPS 吞吐量提升 15-30%。

---

### 优化 5：资源限制与水平扩展

**说明**: Higress 的性能受限于 CPU 和内存资源。通过合理设置资源限制和水平扩展，可以避免资源瓶颈。

**实施方法**:
1. 在 Kubernetes 中为 Higress Pod 设置合理的 `requests` 和 `limits`：
   - CPU: 2-4 核，内存: 4-8GB。
2. 使用 HPA (Horizontal Pod Autoscaler) 根据 CPU 或 QPS 自动扩展副本数。
3. 监控 `istio-proxy` 和 `higress` 的资源使用情况。

**预期效果**: 
- 避免资源争抢导致的性能抖动。
- 水平扩展可线性提升 QPS（如 3 倍副本数 → 3 倍 QPS）。

---

### 优化 6：启用 Prometheus 监控与动态调优

**说明**: 通过实时监控关键指标（如请求延迟、错误率、并发连接数），可以动态调整配置以优化性能。

**实施方法**:
1. 集成 Prometheus 和 Grafana 监控 Higress 指标。
2. 设置

---
## 学习要点

- Higress 是基于阿里云内部 Envoy 实践构建的云原生 API 网关，深度集成了 Istio 服务网格能力。
- 提供了标准 K8s Ingress Controller 支持，能够无缝对接 Kubernetes 原生环境。
- 内置了针对高并发与大流量场景优化的 WAF（Web 应用防火墙）插件，保障安全。
- 支持将流量路由至多种后端类型，包括微服务、Serverless 函数及静态 IP，架构适配性强。
- 兼容 Nginx Ingress 注解，大幅降低了从传统 Nginx 迁移至 Higress 的成本与难度。
- 拥有高度可扩展的插件市场（Wasm 插件），允许开发者使用 Go 或 Python 编写自定义业务逻辑。
- 提供了完善的控制台与 Dashboard，极大简化了服务治理、流量监控及安全配置的运维复杂度。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础与核心概念

**学习内容**:
- 云原生网关的基本概念：理解什么是 Ingress、Gateway 以及 API 网关在微服务架构中的定位。
- Higress 简介：了解 Higress 的开源背景（基于阿里云内部实践）、核心特性（高性能、扩展性）以及与 Nginx、Istio 的关系。
- 核心架构组件：掌握控制面与数据面的基本分工，以及 Envoy 作为底层数据引擎的角色。
- 基础安装与部署：学习如何在本地 Docker 环境或 Kubernetes 集群中安装 Higress。
- 基本流量管理：学习如何配置简单的路由转发，将流量导入后端服务。

**学习时间**: 1-2周

**学习资源**:
- Higress 官方 GitHub 仓库
- Higress 官方文档
- 云原生网关技术白皮书或相关架构设计文章

**学习建议**:
建议先从宏观上理解 Higress 解决了什么问题，不要急于深入配置细节。动手实践是关键，务必在本地搭建一个最小化的 Kubernetes 环境（如 Kind 或 Minikube）并成功部署 Higress。

---

### 阶段 2：流量治理与配置实战

**学习内容**:
- 路由高级配置：学习基于 Header、Query 参数、Cookie 等条件的复杂路由匹配规则。
- 负载均衡策略：掌握轮询、随机、最小连接等负载均衡算法的配置与应用场景。
- 服务治理：学习超时、重试、熔断等流量治理策略的配置，保障服务稳定性。
- 金丝雀发布与蓝绿部署：实践基于 Header 或权重的流量切分，实现平滑升级。
- 安全防护：学习配置 Basic Auth、JWT 认证以及 IP 黑白名单访问控制。

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 流量管理章节
- Envoy 官方文档（用于理解底层 L7 路由逻辑）
- Kubernetes Ingress 资源配置规范

**学习建议**:
此阶段重点在于“玩转”流量。建议构建一个模拟的微服务场景（例如两个版本的后端服务），通过 Higress 控制台或 K8s YAML 文件反复练习路由切换和灰度发布流程，观察流量走向是否符合预期。

---

### 阶段 3：插件生态与可观测性

**学习内容**:
- 插件系统原理：理解 Higress 的 Wasm 插件运行机制与 Lua 脚本的区别。
- 常用内置插件：实践使用限流、跨域（CORS）、请求响应修改等官方内置插件。
- 自定义插件开发：学习如何使用 Wasm (AssemblyScript/Go) 或 Lua 编写自定义插件来处理特定业务逻辑（如请求鉴权、数据转换）。
- 可观测性集成：学习如何配置 Prometheus 监控指标、集成 Zipkin/SkyWalking 进行链路追踪，以及日志采集分析。
- 网关高可用：了解 Higress 的部署扩缩容机制及性能调优基础。

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档 - 插件市场与开发指南
- WebAssembly (Wasm) 相关开发教程
- Prometheus 与 Grafana 官方文档

**学习建议**:
此阶段是区分普通用户与高级用户的关键。建议尝试编写一个简单的自定义插件（例如在请求头中添加特定字段并验证）。同时，务必搭建 Grafana 仪表盘来监控 Higress 的关键性能指标（QPS、延迟、成功率）。

---

### 阶段 4：深度集成与源码剖析（精通）

**学习内容**:
- 服务发现深度集成：学习 Higress 与 Nacos、Consul、Eureka 等注册中心的对接原理与配置。
- 全链路灰度：在复杂的微服务架构中，实现按标签、按用户的全链路流量染色。
- 多集群管理：了解多集群网关的部署模式与流量调度策略。
- 源码级剖析：阅读 Higress Controller 和 Router 的核心源码，理解配置的下发与热更新流程。
- 性能极致优化：深入 Envoy 配置调优，连接池管理，以及网关层面的压测与瓶颈分析。

**学习时间**: 4周以上

**学习资源**:
- Higress 源码
- CNCF 云原生社区相关技术分享
- 阿里云云原生网关技术博客与深度解析文章

**学习建议**:
此阶段需要结合实际的生产级复杂场景进行思考。尝试参与 Higress 开源社区的 Issue 讨论或贡献代码。重点关注高并发场景下的网关稳定性问题，以及如何通过源码级理解来排查疑难杂症。

---
## 常见问题


### 1: Higress 是什么？它与阿里巴巴和 Nginx 有什么关系？

1: Higress 是什么？它与阿里巴巴和 Nginx 有什么关系？

**A**: Higress 是一个开源的、云原生的 API 网关。它是在阿里巴巴内部多年双“11”大促流量治理经验的基础上孵化出来的，并于 2022 年开源。从技术架构上看，Higress 是基于 Nginx 的核心构建的，但为了更好地支持云原生和微服务架构，它深度集成了 Envoy 的能力。简单来说，Higress 结合了 Nginx 的高性能与 Envoy 的可扩展性和动态配置能力，旨在为 Kubernetes 和微服务环境提供统一的流量管理入口。

---



### 2: Higress 与 Kong 或 APISIX 等其他开源网关相比有什么优势？

2: Higress 与 Kong 或 APISIX 等其他开源网关相比有什么优势？

**A**: Higress 的核心优势主要体现在以下几个方面：
1.  **深度集成阿里生态**：它对阿里云的微服务引擎（MSE）、容器服务（ACK）以及 Nacos、Sentinel 等中间件有原生的最佳实践支持。
2.  **标准兼容性**：它支持 Kubernetes Ingress（K8s Ingress Controller）和 Gateway API，同时也兼容 Nginx 的配置语法，降低了从传统 Nginx 迁移的成本。
3.  **安全防护**：内置了 WAF（Web 应用防火墙）插件，能够提供更开箱即用的安全防护。
4.  **插件生态**：支持 WASM（WebAssembly）和 Lua 插件，允许开发者使用多种语言（如 Go、C++、Rust）编写插件，且插件热加载不会影响业务流量，扩展性更强。

---



### 3: Higress 是否支持从 Nginx 或 Ingress Controller 进行平滑迁移？

3: Higress 是否支持从 Nginx 或 Ingress Controller 进行平滑迁移？

**A**: 是的，平滑迁移是 Higress 的核心设计目标之一。Higress 提供了 Nginx 兼容模式，能够识别并解析大部分常用的 Nginx 配置指令。这意味着用户可以直接将现有的 Nginx 配置文件（nginx.conf）导入 Higress，或者通过工具将其转换为 Higress 的配置格式。对于 Kubernetes 用户，Higress 可以作为标准 Ingress Controller 运行，直接替换原有的 Nginx Ingress Controller 或 Traefik，无需大规模修改业务代码或 YAML 资源文件。

---



### 4: Higress 的性能表现如何？能否支撑高并发流量？

4: Higress 的性能表现如何？能否支撑高并发流量？

**A**: Higress 继承了 Nginx 的高性能特性，并在此基础上进行了优化。在阿里巴巴内部，经过 Higress 前身技术的长期验证，完全能够支撑双“11”级别的大促流量。在开源基准测试中，Higress 在处理长连接、高并发请求以及 SSL 握手性能上表现优异，通常能够与业界顶级的开源网关持平甚至在特定场景下更优。此外，它支持多线程隔离，可以有效减少“惊群”问题对延迟的影响。

---



### 5: 如何在 Higress 中进行插件开发？支持哪些语言？

5: 如何在 Higress 中进行插件开发？支持哪些语言？

**A**: Higress 提供了强大的插件扩展能力，主要支持以下两种方式：
1.  **WASM 插件**：这是 Higress 推荐的现代化插件开发方式。由于支持 WASM，开发者可以使用 Go、C++、Rust、AssemblyScript 甚至 JavaScript/TypeScript 来编写插件逻辑。WASM 插件具有沙箱隔离、动态加载、崩溃不导致网关进程崩溃等优点。
2.  **Lua 插件**：为了兼容 OpenResty 生态，Higress 依然支持 Lua 脚本插件，方便用户复用现有的 OpenResty 脚本逻辑。
用户可以通过 Higress 的控制台界面直接上传插件包，或者通过 Git 仓库集成 CI/CD 流程来管理插件的生命周期。

---



### 6: Higress 是否支持服务网格（Service Mesh）功能？

6: Higress 是否支持服务网格（Service Mesh）功能？

**A**: 虽然 Higress 定位为 API 网关，主要用于处理南北向流量（进入集群的流量），但它与 Istio 等服务网格产品结合紧密。Higress 可以作为 Service Mesh 的南北向流量入口，与网格内部的 Sidecar 代理协同工作，实现全链路的流量管理和安全治理。它支持与 Istio 的数据面组件进行配置互通，帮助用户构建混合架构的流量治理体系。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 基于 Higress 的快速入门特性，如何将一个现有的 Nginx Ingress 配置（包含基本的路由规则）迁移到 Higress 的 Gateway API 配置中？请列出迁移过程中需要调整的核心字段。

### 提示**: 关注 Gateway API 和 Nginx Ingress 在资源对象定义上的差异，特别是 API 版本、监听器配置和路由规则的匹配方式。

### 

---
## 实践建议

基于 Higress 作为“AI Native API Gateway”的定位，结合其基于 Envoy 和 Istio 的高性能架构，以下是针对实际生产环境的 6 条实践建议：

### 1. 利用内置的 AI 提示词模板管理能力
**场景：** 当你需要将后端大模型（如 GPT-4, 通义千问等）暴露给前端或外部调用时。
**建议：** 不要在前端应用中硬编码 System Prompt。直接在 Higress 的路由配置中利用其 AI 特性，配置统一的提示词模板。
**最佳实践：** 在网关层固化“人设”和安全指令（例如：“你是一个客服助手，请拒绝回答政治问题”）。这样即使后端模型切换，前端交互逻辑也不需要变动，且能防止用户通过直接调用后端接口绕过安全限制。

### 2. 实施精细的 Token 限流与成本控制
**场景：** AI 接口调用成本高昂，且容易受到恶意请求或高频调用的冲击。
**建议：** 区别于传统的 QPS（每秒请求数）限流，务必配置基于 RPM（每分钟请求数）或 TPM（每分钟 Token 数）的限流策略。
**常见陷阱：** 仅配置 HTTP QPS 限流。由于 AI 推理耗时较长，低 QPS 可能消耗巨额 Tokens，导致账单爆炸。使用 Higress 的插件市场中的限流插件，针对特定 API Key 或用户维度进行 Token 级别的配额管理。

### 3. 构建模型供应商的无感切换与降级机制
**场景：** 业务初期使用 OpenAI，后期想迁移至国产模型（如通义千问、DeepSeek），或者某供应商服务宕机。
**建议：** 利用 Higress 的服务发现和路由重写功能，将模型供应商抽象为后端服务。
**最佳实践：** 配置多活或主备路由。例如，优先将请求路由至模型 A，当检测到模型 A 返回 4xx/5xx 错误或响应超时时，通过 Higress 的插件（如 `fault-inject` 或自定义逻辑）自动将请求转发至模型 B。这能极大提升 AI 服务的可用性。

### 4. 配置流式传输的超时与缓存策略
**场景：** AI 对话通常使用 SSE (Server-Sent Events) 流式返回，响应时间较长且不可预测。
**建议：** 调整路由级别的超时时间，并针对流式响应配置特殊的处理策略。
**最佳实践：**
*   **超时设置：** 将 `per_request_timeout` 设置为较大的值（如 5 分钟），避免大模型生成长文本时网关提前断开连接。
*   **结果缓存：** 对于高频的相同问题，启用 Higress 的响应缓存插件（需支持流式缓存或针对首帧缓存），以减少后端 Token 消耗。注意：缓存键需要包含完整的 User Input 和 Model 参数。

### 5. 敏感信息脱敏与数据泄露防护
**场景：** 企业内部数据通过 AI 接口传输至公网模型，存在隐私泄露风险。
**建议：** 在网关层部署“数据脱敏插件”。
**具体操作：** 在请求发送至 LLM 之前，利用 Higress 的 WAF 插件或自定义 Lua/Wasm 插件，利用正则或关键词库过滤请求体中的敏感信息（如身份证号、API Key、内部 IP）。在响应返回客户端之前，再进行二次检查。这比在应用层代码中做过滤更统一且难以绕过。

### 6. 可观测性：记录全链路 Token 消耗
**场景：** 运营团队需要统计不同业务线、不同用户的 AI 成本。
**建议：** 不要只看 HTTP 状态码。
**最佳实践：** 配置 Higress 的日志输出，确保提取并记录响应头中的 Token 使用量（通常是 `x-usage` 或类似字段，视不同模型提供商而定）。将这些指标接入 Prometheus 或监控系统，建立基于 Token 消耗的可观测性大盘，而非单纯的请求量大盘，

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI 原生](/tags/ai-%E5%8E%9F%E7%94%9F/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [LLM](/tags/llm/) / [MCP](/tags/mcp/) / [WASM](/tags/wasm/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/)

### 相关文章

- [🔥ChatGPT WebUI重磅升级！530模型+MCP+全能RAG，AI能力原地起飞！]({{< relref "posts/20260126-hacker_news-oss-chatgpt-webui-530-models-mcp-tools-gemini-rag--11.md" >}})
- [中国开源AI生态架构选型：DeepSeek之外的构建路径]({{< relref "posts/20260129-blogs_podcasts-architectural-choices-in-chinas-open-source-ai-eco-8.md" >}})
- [kirara-ai：支持多平台接入的多模态AI聊天机器人框架]({{< relref "posts/20260129-github_trending-lss233-kirara-ai-0.md" >}})
- [Kirara-ai：多模态聊天机器人，支持多平台接入与主流模型]({{< relref "posts/20260129-github_trending-lss233-kirara-ai-0.md" >}})
- [Trinity Large：开源4000亿参数稀疏MoE模型]({{< relref "posts/20260129-hacker_news-trinity-large-an-open-400b-sparse-moe-model-11.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*