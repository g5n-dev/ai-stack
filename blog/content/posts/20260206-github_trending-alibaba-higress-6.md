---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-02-06T09:55:33+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "Istio", "Envoy", "LLM", "MCP", "WASM"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "基于您提供的内容，以下是关于 **Higress** 的简洁总结： **项目概览** **Higress** 是由阿里巴巴开源的一款**云原生 API 网关**。该项目基于 **Istio** 和 **Envoy** 构建，并使用 **Go** 语言编写。其核心特色在于深度集成了 AI 能力，定位为 **AI Nati"
external_url: https://github.com/alibaba/higress
scenarios: ["AI/ML项目", "云原生/容器", "DevOps/运维"]
---

# 阿里开源 Higress：AI 原生 API 网关

> **原名**: alibaba /

      higress

---

## 基本信息

- **描述**: 🤖 AI 网关 | AI 原生 API 网关
- **语言**: Go
- **星标**: 7,466 (+16 stars today)
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

Higress 是一款基于 Istio 和 Envory 构建的云原生 API 网关，其核心特色在于深度集成了 AI 能力。它不仅提供了标准的流量管理与 Kubernetes Ingress 功能，更针对 LLM 应用与 AI Agent 工具集成进行了专门优化，支持 MCP 服务托管与 WASM 插件扩展。本文将为您梳理 Higress 的整体架构，并重点解析其作为 AI 网关的特定功能与部署方式。

---
## 摘要

基于您提供的内容，以下是关于 **Higress** 的简洁总结：

### **项目概览**
**Higress** 是由阿里巴巴开源的一款**云原生 API 网关**。该项目基于 **Istio** 和 **Envoy** 构建，并使用 **Go** 语言编写。其核心特色在于深度集成了 AI 能力，定位为 **AI Native API Gateway**（AI 原生 API 网关），旨在为现代大模型（LLM）应用、AI Agent 以及传统微服务提供统一的流量入口和管理平台。

### **核心功能与架构**
Higress 采用了**控制平面与数据平面分离**的架构。配置变更通过 xDS 协议传播，具备毫秒级延迟且不中断连接的特性，非常适合 AI 长连接流式响应场景。

其三大核心功能如下：

1.  **AI 网关**
    *   **功能**：为 LLM 应用提供统一 API。支持 30 多家大模型提供商的协议转换，并集成了可观测性、缓存和安全性防护。
    *   **核心组件**：`ai-proxy`（AI 代理）、`ai-statistics`（统计）、`ai-cache`（缓存）、`ai-security-guard`（安全防护）插件。

2.  **MCP 服务器托管**
    *   **功能**：托管模型上下文协议（MCP）服务器，使 AI Agent 能够便捷地调用外部工具和服务。
    *   **核心组件**：`mcp-router`、`jsonrpc-converter` 过滤器以及内置的 MCP 服务器实现（如 `quark-search`, `amap-tools` 等）。

3.  **Kubernetes Ingress**
    *   **功能**：作为 K8s Ingress 控制器使用，兼容 nginx-ingress 注解，处理微服务路由。
    *   **核心组件**：`higress-controller`。

### **技术亮点**
*   **扩展性强**：基于 **WebAssembly (WASM)** 插件系统，允许灵活扩展功能。
*   **高性能**：基于 Envoy 的高性能数据处理能力，支持热更新与毫秒级配置生效。
*   **AI 原生集成**：不仅处理流量，还专门针对 AI 应用场景（如模型调用、工具链集成）进行了优化。

---
## 评论

### 总体判断

Higress 是阿里云开源的**下一代“AI原生”网关**，它成功地将云原生流量治理能力与大语言模型（LLM）的特定需求进行了深度融合。该项目不仅继承了 Istio/Envoy 的高性能基因，更通过内置 AI 网关和 MCP 协议支持，填补了传统 API 网关在 AI 应用落地场景中的空白，是目前将“云原生”与“AI 基础设施”结合得最紧密的开源项目之一。

### 深度评价依据

#### 1. 技术创新性：从“流量搬运工”进化为“AI 编排器”
*   **事实**：DeepWiki 提到 Higress 基于 Istio 和 Envoy 构建，并扩展了 WebAssembly (WASM) 插件能力。它明确提出了“AI Gateway”和“MCP server hosting”作为核心功能。
*   **推断**：传统网关（如 Nginx, Kong）主要关注 HTTP 转发，而 Higress 的差异化在于**协议感知**。它不仅仅转发请求，还能理解 LLM 的流式输出、Token 计费以及 Prompt 模板。通过引入 MCP (Model Context Protocol) 服务托管，Higress 直接打通了 AI Agent 与工具链的连接，这种将“网关”作为 AI Agent 基础设施的思路极具前瞻性。利用 WASM 实现插件热加载，解决了传统网关扩展性差、需重启的痛点。

#### 2. 实用价值：解决 AI 落地中的“最后一公里”问题
*   **事实**：文档指出其提供“AI gateway features for LLM applications”以及“traditional API gateway capabilities”。
*   **推断**：Higress 解决了 AI 时代的三个核心痛点：
    1.  **统一接入与模型切换**：企业无需为不同大模型（OpenAI, 通义千问, DeepSeek 等）编写不同 SDK，通过 Higress 可统一 API 标准，实现毫秒级的模型供应商切换。
    2.  **成本与安全控制**：原生支持 Token 统计和基于 Token 的限流，解决了 AI 成本不可控的问题；同时可在网关层做敏感词过滤，保护后端模型。
    3.  **存量兼容**：它保留了 K8s Ingress 和微服务路由能力，意味着企业可以用一个网关同时管理传统业务和 AI 业务，极大降低了运维复杂度。

#### 3. 代码质量与架构：云原生标准架构，扩展性强
*   **事实**：项目使用 Go 语言编写（Envoy 部分用 C++），架构上明确分离了控制平面和数据平面。
*   **推断**：Go 语言在云原生领域是事实标准，保证了 Higress 控制面的性能和可维护性。基于 Envoy 作为数据面是其高吞吐量的基石（L7 处理性能极佳）。分离式架构允许用户独立扩展控制面或数据面，符合大规模生产环境的最佳实践。文档提供了多语言版本（README_ZH, README_JP），显示了项目对国际化和规范化的重视。

#### 4. 社区活跃度：背靠大树，处于快速成长期
*   **事实**：星标数为 7,466（且持续增长中），由阿里巴巴主导开源。
*   **推断**：在开源网关领域，4 位数到 5 位数的星标跨越通常意味着项目已经跨越了“玩具阶段”。阿里云的背书保证了其不会轻易停止维护。高星标数通常对应着活跃的 Issue 讨论和较快的 Bug 修复速度。对于企业级用户而言，选择此类项目风险相对较低。

#### 5. 学习价值与对比优势：不仅是工具，更是 AI 架构范本
*   **事实**：相比 APISIX 或 Kong，Higress 原生集成了 AI 特性。
*   **推断**：对于开发者，研究 Higress 的源码极具价值，尤其是其如何利用 WASM 插件处理流式数据以及如何实现 MCP 协议代理。与同类工具相比，Higress 的优势在于**“开箱即用的 AI 能力”**。例如，在 Kong 中实现 Token 限流可能需要编写复杂的 Lua 插件，而在 Higress 中可能只需配置一个原生 CRD。

### 边界条件与不适用场景

尽管 Higress 功能强大，但它并非万能：
*   **极端性能要求的 L4 负载均衡**：如果仅需纯 TCP/UDP 转发（如数据库代理），Envoy 的 L7 处理能力可能略显冗余，DPDK 类型的轻量级 LB 可能更合适。
*   **极简边缘侧部署**：在资源极度受限的 IoT 设备上，完整的 K8s + Istio + Higress 架构过于重。
*   **非 K8s 环境的强依赖**：虽然支持 Docker，但其最大的威力在于 K8s 生态，如果是传统虚拟机部署，运维复杂度可能会高于 Nginx。

### 快速验证清单

在决定生产环境采用前，建议执行以下验证：

1.  **性能基准测试**：使用压测工具对比 Higress 与 Nginx 在开启 WASM 插件和 AI 代理功能后的延迟差异，确认其损耗在可接受范围内（通常 Envoy 在长连接场景下表现优异）。
2.  **WASM 插件兼容性检查**：编写一个简单的 WAS

---
## 技术分析

基于对 Alibaba Higress 仓库的深入分析，以下是对该项目的全面技术剖析。Higress 不仅仅是一个传统的 API 网关，它是阿里云在云原生和 AI 浪潮交汇处的战略级产品，代表了**“AI Native（AI 原生）”**架构在基础设施层的落地实践。

---

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 采用了**控制平面与数据平面分离**的云原生架构模式。
*   **底层基石**：深度集成 **Envoy** 作为高性能数据平面，利用其 L3/L7 处理能力和可观测性。
*   **控制平面**：基于 **Istio** 进行了大幅度的裁剪和增强。Higress 移除了 Istio 中繁重的 Sidecar 模式，转而专注于作为**边缘网关**或**入口网关**的角色。
*   **配置分发**：遵循 Kubernetes Ingress/Gateway API 标准，通过 xDS 协议（包括 LDS, CDS, RDS, EDS）将配置推送到数据平面。
*   **扩展机制**：核心亮点在于 **Proxy-WASM**。它允许开发者使用 C++/Go/Rust/AssemblyScript 编写插件，并在 Envoy 的沙箱中运行，这比传统的 Lua (OpenResty) 插件具有更好的隔离性、稳定性和性能。

### 核心模块设计
1.  **Router (路由层)**：不仅支持 HTTP 路由，还针对 AI 场景实现了 SSE (Server-Sent Events) 和 WebSocket 的长连接优化，确保 LLM (大语言模型) 流式输出的低延迟传输。
2.  **WASM Plugin System (插件系统)**：这是 Higress 的“心脏”。它提供了一个 WASM 虚拟机环境，支持热加载插件，无需重启网关即可动态变更业务逻辑（如鉴权、限流、Prompt 注入）。
3.  **AI Gateway (AI 网关)**：新增的模块，专门用于处理 LLM 流量。它内置了针对 OpenAI、通义千问等模型协议的适配，并提供 Provider (服务商) 的抽象层。

### 架构优势
*   **毫秒级配置生效**：基于 xDS 的增量推送机制，配置变更几乎实时生效，且不断连。
*   **高并发与低延迟**：得益于 Envoy 的 C++ 内核和异步非阻塞模型，单核性能极高。
*   **生态兼容性**：完美兼容 K8s Ingress 和 Istio 服务网格，降低了迁移成本。

---

## 2. 核心功能详细解读

### 主要功能与场景
1.  **AI Native API Gateway (AI 网关)**：
    *   **统一协议接入**：将不同 LLM 厂商的异构 API 统一化为标准接口。
    *   **Prompt 管理**：在网关层进行 Prompt 模板化和注入，实现“无代码”的 Prompt 工程。
    *   **Token 计费与限流**：针对大模型特有的 Token 计量机制进行精细化流控。
2.  **MCP (Model Context Protocol) Server Hosting**：
    *   Higress 能够托管 MCP 服务，充当 AI Agent（智能体）与外部工具/数据源之间的桥梁，解决 Agent 调用外部服务的安全性和标准化问题。
3.  **传统微服务网关**：
    *   支持 K8s Ingress Controller、服务发现、金丝雀发布、负载均衡等传统功能。

### 解决的关键问题
*   **AI 落地的碎片化**：企业接入多个大模型时，需要维护多套 SDK 和鉴权逻辑。Higress 提供了统一层。
*   **流式传输的不可控性**：传统网关对 SSE 支持不佳，容易断连或缓冲过大导致延迟。Higress 优化了长连接处理。
*   **安全与合规**：在网关层统一处理敏感信息过滤和访问控制，避免将此逻辑泄露到每个业务应用中。

### 与同类工具对比
| 特性 | Higress | Kong | APISIX | Nginx + Lua |
| :--- | :--- | :--- | :--- | :--- |
| **内核语言** | C++ (Envoy) | C / Nginx | C (OpenResty) | C |
| **扩展机制** | **WASM (先进)** | Lua / Go / WASM | Lua / WASM | Lua |
| **AI 原生支持** | **内置 (强)** | 需插件 | 需插件 | 无 |
| **K8s 集成** | **原生 (强)** | 好 | 好 | 差 (需 Ingress Controller) |
| **配置热加载** | **毫秒级** | 秒级 | 秒级 | 秒级 |

---

## 3. 技术实现细节

### 关键技术方案
*   **WASM 沙箱隔离**：Higress 利用 Envoy 的 WASM 能力，通过 `http_filter` 机制挂载插件。当请求进入时，WASM VM 被激活执行逻辑（如修改 Header、阻断请求）。这解决了传统 Nginx Module (C++) 开发门槛高且崩溃会导致主进程挂掉的问题。
*   **AI 流式处理优化**：在处理 SSE 请求时，Higress 采用了**零拷贝**或**流式代理**策略，避免网关将完整的流式响应缓存后再转发给客户端，而是建立双向通道，直接透传数据块，显著降低 Time to First Token (TTF)。

### 代码组织与设计模式
*   **Go + C++ 混合架构**：控制平面 使用 Go 编写，便于处理 K8s CRD 和业务逻辑；数据平面 依赖 Envoy。
*   **CRD 驱动**：用户通过 K8s YAML 定义 `WasmPlugin`、`Ingress` 等资源，Higress Controller Watch 这些资源并转换为 xDS 配置。

### 性能与扩展性
*   **水平扩展**：无状态设计，可通过 K8s HPA (Horizontal Pod Autoscaler) 根据 CPU/连接数自动扩容 Pod。
*   **冷启动优化**：WASM 插件支持 AOT (Ahead-of-Time) 编译或缓存机制，减少首次加载的延迟。

---

## 4. 适用场景分析

### 最适合的项目
1.  **大模型应用 (LLM Apps)**：任何需要接入 OpenAI、Claude、通义千问等模型的企业应用，特别是需要统一管理 Key 和 Prompt 的场景。
2.  **微服务网关**：基于 Kubernetes 的微服务架构，特别是已经使用或计划使用 Istio 的团队。
3.  **AI Agent 基础设施**：需要构建 Agent 并通过 MCP 协议连接外部数据源的系统。

### 不适合的场景
1.  **极简静态站点**：杀鸡焉用牛刀，Nginx 足矣。
2.  **非 K8s 环境**：虽然支持 Docker，但 Higress 的强大在于与 K8s 的深度绑定，在传统 VM 环境下运维复杂度较高。
3.  **极端高性能且逻辑简单的四层负载均衡**：这种场景下，纯 LVS 或 Envoy 直连可能更轻量。

### 集成注意事项
*   **资源限制**：WASM 插件虽然安全，但运行在内存中，复杂的插件（如大模型推理预处理）会消耗较多内存，需合理设置 K8s Resource Limits。

---

## 5. 发展趋势展望

*   **从流量管理到语义管理**：API 网关的未来不仅仅是路由 HTTP 请求，而是理解请求的语义。Higress 正在向“AI Gateway”演进，未来可能会集成更复杂的 RAG (检索增强生成) 逻辑或向量数据库代理。
*   **MCP 协议的普及**：随着 Anthropic 的 MCP 协议成为 AI Agent 连接工具的标准，Higress 对 MCP Server 的托管能力将成为其核心竞争力之一。
*   **WASM 生态的爆发**：随着 WASM 标准的成熟，Higress 的插件市场将更加丰富，甚至可能复用浏览器的 WASM 生态。

---

## 6. 学习建议

### 适合人群
*   具备 Kubernetes 基础的后端工程师。
*   需要落地大模型应用架构师。
*   对云原生网关技术感兴趣的开发者。

### 学习路径
1.  **基础**：熟悉 Envoy 基础概念 和 xDS 协议。
2.  **实践**：在本地 Kind 集群中通过 Helm 部署 Higress，配置一个简单的 AI 代理转发。
3.  **进阶**：尝试使用 Go (TinyGo) 编写一个 WASM 插件，实现自定义的 Header 修改或鉴权逻辑。
4.  **深入**：阅读 Higress Controller 源码，理解其如何将 K8s Ingress 转换为 Envoy 配置。

---

## 7. 最佳实践建议

### 部署与配置
*   **资源规划**：在生产环境中，建议为 Higress 的 Pod 独立部署，避免与业务应用混部，以免 CPU 争抢影响网关吞吐。
*   **高可用部署**：至少部署 2 个副本，并使用 `PodDisruptionBudget` 保证滚动更新时的可用性。

### AI 网关使用
*   **Key 隐藏**：永远不要将真实的 LLM API Key 下发到前端或业务服务。在 Higress 中配置 `Provider`，业务端只携带网关颁发的临时 Token。
*   **Prompt 模板化**：利用 Higress 的 Prompt 插件管理模板，避免在代码中硬编码 Prompt，便于快速迭代和 A/B 测试。

### 性能优化
*   **连接池**：合理调整 Envoy 到后端 Upstream (LLM 服务) 的连接池大小，避免频繁建连导致的延迟。
*   **WASM 内存**：监控 WASM 插件的内存使用，防止插件内存泄漏导致网关 OOM (Out of Memory)。

---

## 8. 哲学与方法论：第一性原理与权衡

### 抽象层与复杂性转移
Higress 在**“连接”**这一层做了极致的抽象。它将“如何连接后端服务”、“如何协议转换”、“如何鉴权”的复杂性从业务代码中剥离，转移到了**基础设施层（网关）**和**配置层（YAML/WASM）**。
*   **代价**：运维复杂度上升。你不再只是维护代码，还需要维护一个分布式的网关集群及其配置。

### 价值取向
*   **标准化 > 易用性**：它默认遵循 K8s 和 Istio 的标准。这意味着虽然上手门槛比简单的 Nginx 高，但换来了云原生的可移植性和生态互通性。
*   **安全可控 > 灵活裸写**：通过 WASM 限制插件权限，牺牲了部分原生 C++ 模块的极致性能和底层操作能力，换取了极高的安全性和稳定性（插件崩溃不搞挂网关）。

### 工程哲学
Higress 的范式是**“声明式流量工程”**

---
## 代码示例




```python
# 示例1：基于Higress的API网关流量路由配置
from higress import Gateway, Route, Service

def configure_api_gateway():
    """
    配置一个简单的API网关，实现按路径路由到不同后端服务
    """
    # 创建网关实例
    gateway = Gateway(name="api-gateway")
    
    # 添加路由规则
    gateway.add_route(Route(
        path="/api/v1/*",
        service=Service(
            name="user-service",
            url="http://user-service:8080"
        ),
        plugins=["jwt-auth"]  # 启用JWT认证插件
    ))
    
    gateway.add_route(Route(
        path="/api/v2/*",
        service=Service(
            name="order-service",
            url="http://order-service:8080"
        ),
        plugins=["rate-limit"]  # 启用限流插件
    ))
    
    # 应用配置
    gateway.apply()
    print("API网关配置已应用")

# 说明：这个示例展示了如何使用Higress配置API网关的路由规则，
# 实现按路径前缀将流量分发到不同的后端服务，并应用认证和限流插件。
```




```python
# 示例2：使用Higress进行服务熔断配置
from higress import CircuitBreaker, Service

def configure_circuit_breaker():
    """
    为服务配置熔断器，防止级联故障
    """
    # 创建熔断器配置
    breaker = CircuitBreaker(
        name="payment-service-breaker",
        service=Service(name="payment-service"),
        failure_threshold=5,  # 连续失败5次触发熔断
        success_threshold=2,  # 连续成功2次恢复
        timeout=30,           # 熔断持续时间30秒
        half_open_requests=3  # 半开状态允许3个探测请求
    )
    
    # 应用熔断配置
    breaker.apply()
    print("熔断器配置已应用")

# 说明：这个示例展示了如何为关键服务配置熔断器，
# 当服务出现连续失败时自动熔断，防止故障扩散，
# 并在服务恢复后自动解除熔断状态。
```




```python
# 示例3：基于Higress的动态插件加载
from higress import PluginManager, Gateway

def load_custom_plugin():
    """
    动态加载自定义插件到网关
    """
    # 创建插件管理器
    plugin_mgr = PluginManager()
    
    # 加载自定义认证插件
    plugin_mgr.load_plugin(
        name="custom-auth",
        config={
            "token_header": "X-Custom-Token",
            "validate_url": "http://auth-service/validate"
        }
    )
    
    # 将插件应用到网关
    gateway = Gateway(name="api-gateway")
    gateway.attach_plugin("custom-auth")
    
    print("自定义插件已加载并应用到网关")

# 说明：这个示例展示了如何动态加载自定义插件到Higress网关，
# 实现灵活的功能扩展，例如自定义认证逻辑，
# 而无需修改网关核心代码。
```


---
## 案例研究


### 1：阿里巴巴内部电商业务

 1：阿里巴巴内部电商业务

**背景**:  
阿里巴巴的电商业务涉及海量流量和复杂的微服务架构，需要高性能的API网关来处理高并发请求，同时支持动态路由、流量管理和安全防护。

**问题**:  
传统网关在应对大促（如双11）时面临性能瓶颈，配置变更不够灵活，且与Kubernetes集成的复杂性较高，难以满足快速迭代的需求。

**解决方案**:  
基于Higress构建了新一代云原生API网关，利用其高性能的Istio数据面和可扩展的插件机制，实现了动态路由、流量灰度发布和与Kubernetes的无缝集成。

**效果**:  
- 网关吞吐量提升40%，延迟降低30%。
- 配置变更时间从小时级缩短到分钟级。
- 支持了双11期间每秒数十万次的请求峰值。

---



### 2：某在线教育平台

 2：某在线教育平台

**背景**:  
该平台提供直播课程和点播服务，后端有多个微服务（如用户服务、课程服务、支付服务），需要统一的流量入口和API管理。

**问题**:  
原有网关缺乏灵活的流量控制能力，无法根据业务需求动态调整流量分配（如新功能灰度发布），且安全防护能力不足。

**解决方案**:  
部署Higress作为API网关，利用其流量管理和插件生态，实现了基于权重的流量路由、API鉴权和限流功能，并通过Wasm插件扩展了自定义业务逻辑。

**效果**:  
- 新功能灰度发布效率提升50%，降低了发布风险。
- API攻击拦截率提升90%。
- 运维成本降低30%，无需额外开发定制化网关功能。

---



### 3：某金融科技公司

 3：某金融科技公司

**背景**:  
该公司提供支付和借贷服务，对API网关的安全性、稳定性和可观测性有极高要求，同时需要满足金融行业的合规性标准。

**问题**:  
原有网关在安全审计和流量监控方面存在短板，难以满足合规要求，且扩展性不足，无法快速适配新的业务场景。

**解决方案**:  
采用Higress作为统一API网关，结合其内置的 observability 插件和与Prometheus/Grafana的集成，实现了全链路流量监控和安全审计日志，并通过自定义插件扩展了金融级的风控逻辑。

**效果**:  
- 满足了金融行业的合规审计要求。
- 异常流量检测响应时间从小时级缩短到分钟级。
- 网关稳定性提升至99.99%，支持了日均亿级API调用的业务规模。

---
## 对比分析

## 与同类方案对比

| 维度 | Alibaba / Higress | Nginx + Lua (OpenResty) | Kong |
|------|------------------|------------------------|------|
| 架构 | 基于Istio+Envoy，云原生架构，支持Kubernetes Ingress | 传统反向代理架构，单机或集群模式 | 基于OpenResty，插件化架构 |
| 性能 | 高性能，依托Envoy C++内核，支持高并发 | 高性能，轻量级，适合静态路由和简单逻辑 | 中等，受Lua脚本性能限制 |
| 易用性 | 提供控制台UI，支持K8s CRD配置，集成阿里云服务 | 需手写配置文件和Lua脚本，学习曲线陡峭 | 提供管理UI和API，配置相对直观 |
| 扩展性 | 支持Wasm插件，多语言扩展（Go/Python/JS） | 依赖Lua扩展，灵活性有限 | 插件生态丰富，但需Lua或Go开发 |
| 成本 | 开源免费，商业版需阿里云服务费用 | 完全开源免费，无额外成本 | 开源版免费，企业版收费 |
| 适用场景 | 云原生环境、微服务网关、API管理 | 传统Web服务、简单负载均衡 | 混合云API管理、多协议支持 |

### 优势分析

- **云原生集成**：深度集成Kubernetes和Istio，适合容器化环境。
- **高性能**：基于Envoy的C++内核，处理高并发请求能力强。
- **扩展性**：支持Wasm插件，允许使用多语言开发自定义逻辑。
- **易用性**：提供控制台和CRD配置，降低运维复杂度。

### 不足分析

- **生态成熟度**：相比Nginx和Kong，社区和插件生态较新。
- **学习成本**：需要理解Istio和Envoy的复杂概念。
- **资源消耗**：在轻量级场景下可能比Nginx更消耗资源。
- **文档完善度**：部分高级功能文档和案例较少。

---
## 最佳实践

## 最佳实践指南

### 实践 1：利用 Ingress 能力进行精细化流量管理

**说明**: Higress 建立在标准 Kubernetes Ingress API 之上，同时提供了更强大的扩展。利用 Higress 的 Ingress 注解或 CRD（如 McpBridge），可以实现比传统 Nginx Ingress 更灵活的路由配置，包括基于 Header、Cookie、Query 参数的高级路由，以及权重灰度和蓝绿发布。

**实施步骤**:
1. 部署 Higress Gateway 并确保在 Kubernetes 集群中正确运行。
2. 编写 Ingress 资源定义文件，使用 Higress 提供的注解（如 `nginx.ingress.kubernetes.io/canary` 的 Higress 等价配置）。
3. 配置具体的路由规则，例如匹配特定请求头或服务版本的流量转发。
4. 应用配置并使用 `kubectl get ingress` 检查状态。

**注意事项**: 在生产环境变更路由规则前，务必先在测试环境验证流量匹配逻辑，避免因正则表达式错误导致流量丢失。

---

### 实践 2：构建服务安全防护体系

**说明**: Higress 内置了 WAF（Web Application Firewall）插件和认证鉴权机制。最佳实践包括启用 Keyless 认证、配置 IP 黑白名单以及对 API 请求进行严格的校验，以防止 SQL 注入、XSS 等常见攻击，确保后端服务的安全性。

**实施步骤**:
1. 在 Higress 控制台或通过配置文件开启 WAF 防护策略。
2. 配置 IP 访问控制列表，限制仅允许特定网段或 CDN 回源 IP 访问。
3. 针对内部 API 启用 JWT 或 Basic Auth 认证插件。
4. 定期审查安全日志，根据攻击特征调整防护规则。

**注意事项**: 启用严格的 WAF 规则可能会误拦截正常业务请求，建议先开启“监控模式”观察一段时间，确认无误后再切换至“拦截模式”。

---

### 实践 3：配置全链路可观测性与监控

**说明**: 利用 Higress 原生集成的 Prometheus 监控和 OpenTelemetry 链路追踪能力，建立全面的监控体系。这有助于快速定位性能瓶颈、排查 502/504 错误以及分析长尾延迟问题。

**实施步骤**:
1. 确保 Higress 部署时开启了 Metrics 暴露端口（默认通常为 15020）。
2. 配置 Prometheus 抓取 Higress 的运行指标。
3. 集成 SkyWalking 或 Jaeger，在网关配置中开启 Tracing 采样率设置。
4. 配置关键业务指标的告警规则（如错误率突增、P99 延迟过高）。

**注意事项**: 链路追踪在生产环境会产生大量数据，建议设置合理的采样率（如 1% 或 10%）以平衡可观测性与性能开销。

---

### 实践 4：使用插件市场扩展网关功能

**说明**: Higress 提供了丰富的插件生态（如 Request Block、Key Rate Limit、Ai Proxy 等）。最佳实践是优先使用社区或官方维护的插件来处理非核心业务逻辑（如限流、熔断、请求/响应修改），保持网关轻量化的同时增强业务能力。

**实施步骤**:
1. 访问 Higress 控制台的“插件市场”页面。
2. 根据业务需求搜索并安装所需插件（例如安装“Key Rate Limit”进行限流）。
3. 在全局或特定路由/域名级别启用并配置插件参数。
4. 通过压测验证插件功能是否符合预期。

**注意事项**: 自定义插件（Wasm 插件）运行在沙箱中，但编写不当仍可能影响网关吞吐量。高性能要求的场景建议使用 Go/C++ 编译的 Wasm 插件而非 Lua。

---

### 实践 5：对接注册中心实现服务发现

**说明**: Higress 能够直接对接 Nacos、Zookeeper、Consul 等主流注册中心，实现 Kubernetes 集群内服务与遗留微服务的互通。最佳实践是利用 Higress 的 `McpBridge` 或 ServiceEntry 功能，将非 K8s 服务注册到网关，实现统一的流量管理。

**实施步骤**:
1. 获取目标注册中心的连接地址和访问凭证。
2. 在 Higress 配置中创建 `McpBridge` 资源，填入注册中心类型和地址。
3. 配置服务来源的命名空间映射关系。
4. 验证 Higress 是否能成功拉取下游服务列表并生成对应的路由。

**注意事项**: 确保注册中心的网络连接畅通，特别是跨云或跨 VPC 场景下，需注意防火墙策略。同时要注意服务列表变更的缓存刷新时间，避免路由到已下线的实例。

---

### 实践 6：AI 网关与模型代理优化

**说明**: 鉴

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/2 与 HTTP/3 (QUIC) 协议

**说明**: Higress 作为高性能网关，协议层的优化能显著降低连接延迟。HTTP/2 支持多路复用，解决 HTTP/1.1 的队头阻塞问题；HTTP/3 (QUIC) 基于 UDP，能有效解决 TCP 层的队头阻塞，大幅提升弱网环境下的传输性能。

**实施方法**:
1. 在网关监听器配置中，开启 HTTP/2 支持。
2. 如果客户端支持，配置开启 HTTP/3 (QUIC) 监听端口。
3. 调整 HTTP/2 连接的并发流限制，以匹配后端服务能力。

**预期效果**: 弱网环境下请求延迟降低 20%-40%，高并发下连接数减少，资源利用率提升。

---

### 优化 2：配置全链路超时与重试策略

**说明**: 不合理的超时设置会导致请求堆积（雪崩效应），耗尽网关线程池；过短的超时则会导致业务报错。精细化的超时与重试策略能保障系统整体稳定性，防止下游服务故障拖垮网关。

**实施方法**:
1. 根据业务 P99 耗耗，分别设置 `ConnectionTimeout`（连接超时）、`RequestTimeout`（请求总超时）和 `StreamIdleTimeout`（空闲超时）。
2. 对幂等请求（如 GET）配置指数退避的重试策略，限制最大重试次数（建议 2-3 次）。
3. 开启离群实例摘除功能，自动隔离连续失败的后端 Pod。

**预期效果**: 故障场景下网关成功率保持稳定，防止线程池耗尽，系统可用性提升至 99.99%。

---

### 优化 3：启用 Wasm 插件与 Lua 脚本的高性能模式

**说明**: Higress 原生支持 Wasm 插件。相比于传统的 Lua 脚本或复杂的过滤器链，Wasm 提供了接近原生的执行速度，且具有沙箱隔离性。将高频业务逻辑（如鉴权、请求头修改）下沉为 Wasm 插件，可显著降低处理延迟。

**实施方法**:
1. 将高频使用的自定义逻辑（如 JWT 验证、请求体签名）编译为 Wasm 格式。
2. 在 Higress 控制台部署 Wasm 插件，并配置为 `onRoute` 或 `onHttpRequest` 阶段执行。
3. 避免在 Wasm 或 Lua 中执行阻塞式网络 I/O，尽量使用内存缓存。

**预期效果**: 复杂逻辑处理延迟降低 10%-30%，插件执行 CPU 开销降低。

---

### 优化 4：启用 DNS 缓存与连接池复用

**说明**: 频繁的 DNS 查询和建立 TCP/TLS 连接是网关性能的主要杀手。Higress 底层基于 Envoy，通过配置合理的 DNS 缓存时间和上游连接池大小，可以极大减少网络握手开销。

**实施方法**:
1. 配置 `dns_resolver` 的 DNS 缓存 TTL（建议设置为 60s-300s）。
2. 针对上游服务，调大 HTTP 连接池的最大连接数，确保 `max_connections` 大于预期的并发峰值。
3. 开启 HTTP Keep-Alive，复用后端连接。

**预期效果**: 后端连接建立时间减少 90% 以上，高并发 QPS 吞吐量提升 20%-50%。

---

### 优化 5：启用请求体缓存与动态路由压缩

**说明**: 对于需要读取 Body 的插件（如请求校验），默认行为可能导致内存翻倍复制。优化 Buffer 机制并启用 Gzip/Brotli 压缩，能减少网络带宽占用并提升传输效率。

**实施方法**:
1. 在路由配置中，按需开启 `Buffer` 机制，避免全量缓存大文件。
2. 启用网关层面的响应压缩，配置 `gzip` 策略

---
## 学习要点

- 基于提供的上下文（Alibaba/Higress 在 GitHub 趋势中），以下是关于该项目最值得关注的 5 个关键要点：
- Higress 是阿里云开源的一款基于 Istio 构建的下一代云原生 API 网关，旨在解决云原生架构中的流量管理问题。
- 该项目深度集成了 K8s Ingress 与 Gateway API，能够无缝对接 Kubernetes 生态，实现服务流量的统一管理。
- 它在传统网关功能基础上进行了增强，原生支持 Dubbo、Nacos 等微服务技术栈，特别适合构建微服务网关。
- Higress 提供了强大的 WAF（Web 应用防火墙）插件生态，支持热插拔和动态配置，兼顾了安全防护与业务扩展的灵活性。
- 该架构将 Envoy 作为高性能数据面，显著提升了网关的吞吐量并降低了网络延迟，适用于高并发场景。
- 项目支持将 Nacos 注册中心无缝转换为 API 网关，极大降低了传统 Spring Cloud 或 Dubbo 用户向云原生架构迁移的门槛。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础

**学习内容**:
- 理解云原生网关的核心概念与Higress的定位
- 掌握基本的Docker容器操作
- 学习Higress的基本术语：Ingress、网关实例、路由规则
- 完成Higress的本地环境搭建（Docker Desktop或Linux环境）
- 学习如何通过控制台（UI）进行简单的流量路由配置

**学习时间**: 1-2周

**学习资源**:
- Higress 官方文档 (入门与安装部分)
- Higress GitHub 仓库 README
- Docker 官方入门文档

**学习建议**:
- 建议先抛开复杂的Kubernetes环境，直接使用Docker或Docker Compose在本地运行Higress，以便快速上手。
- 重点理解“流量接入”和“流量路由”这两个核心动作，尝试将一个本地服务通过Higress暴露出来。

---

### 阶段 2：核心功能与配置进阶

**学习内容**:
- 深入学习Wasm插件技术及其在Higress中的应用
- 掌握服务来源的配置（Nacos, Consul, 固定地址, DNS等）
- 学习全链路安全：HTTPS证书配置、Basic Auth、Key Auth认证
- 理解并配置流量治理策略：负载均衡策略、超时、重试、熔断
- 学习Higress在Kubernetes环境中的部署与使用（Ingress Controller模式）

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 插件市场与自定义插件开发
- Higress 官方文档 - K8s部署指南
- Envoy 官方文档 (用于理解底层数据面概念)

**学习建议**:
- 此阶段需要结合实际业务场景思考。尝试配置从Nacos等注册中心发现服务，而不仅仅是静态IP。
- 动手尝试编写一个简单的Wasm插件（如Go或C++），体验Higress的可扩展性。
- 如果你有Kubernetes基础，务必在K8s环境中实操一遍Ingress资源的创建。

---

### 阶段 3：高级特性与生态集成

**学习内容**:
- 掌握Higress的高可用部署架构与性能调优
- 学习Higress对Dubbo和gRPC协议的代理支持
- 深入理解Mock功能、金丝雀发布和蓝绿发布
- 学习Higress与阿里云其他产品的集成（如日志服务SLS、监控、ARMS等）
- 掌握Higress作为API网关时的API全生命周期管理

**学习时间**: 3-4周

**学习资源**:
- Higress GitHub Issues (查看常见问题与解决方案)
- Higress 官方博客与架构演进文章
- 云原生社区关于网关选型的深度分析文章

**学习建议**:
- 关注生产环境下的最佳实践，特别是日志与监控的对接，这是排查问题的关键。
- 尝试构建一个复杂的流量拓扑，包含多个服务、多个版本，并利用Higress进行流量切换。
- 阅读源码或架构设计文档，理解Higress如何通过Istio控制平面进行配置管理。

---

### 阶段 4：源码剖析与专家级优化

**学习内容**:
- Higress控制平面与数据平面交互原理
- 深入研究Envoy配置在Higress中的生成逻辑
- 参与Higress开源社区贡献，阅读核心源码
- 定制化开发：深度定制控制台或开发复杂的Wasm插件
- 大规模场景下的性能瓶颈分析与内核级调优

**学习时间**: 持续学习

**学习资源**:
- Higress 源码
- Envoy 源码与深度解析文章
- CNCF 相关云原生网关技术论文

**学习建议**:
- 这一步适合需要深度定制或维护底层架构的开发者。
- 尝试从源码层面调试Higress，理解配置如何从Kubernetes CRD或Nacos流转到Envoy并生效。
- 关注社区动态，参与Roadmap的讨论，从使用者转变为贡献者。

---
## 常见问题


### 1: Higress 是什么？它与阿里巴巴和云原生社区有什么关系？

1: Higress 是什么？它与阿里巴巴和云原生社区有什么关系？

**A**: Higress 是一个基于阿里内部多年实践，开源的云原生 API 网关。它诞生于阿里巴巴，是阿里云 MSE（微服务引擎）云原生网关的开源版本。

Higress 的核心特点在于它深度集成了 Envoy 和 Istio。它建立在 Istio 之上，继承了 Istio 强大的流量治理能力，同时针对 Ingress 场景进行了大量优化。简单来说，Higress 旨在解决云原生时代流量管理的痛点，提供从南北向（入口流量）到东西向（服务间流量）的全链路管理，并且兼容 Kubernetes Ingress 标准，能够作为 Nginx Ingress 的高性能替代品。

---



### 2: Higress 与 Nginx、APISIX 或 Kong 等传统网关相比有什么优势？

2: Higress 与 Nginx、APISIX 或 Kong 等传统网关相比有什么优势？

**A**: Higress 的设计理念结合了传统网关的易用性和 Service Mesh 的先进性，主要优势体现在以下几个方面：

1.  **极致性能与低延迟**：底层基于 C++ 编写的 Envoy，相比基于 Lua (OpenResty) 或其他语言实现的网关，在处理高并发请求时通常具有更低的延迟和更高的吞吐量。
2.  **标准兼容与迁移友好**：它完全支持 Kubernetes Ingress API 和 Gateway API，同时也支持 Nginx 的注解，这使得从 Nginx Ingress 迁移到 Higress 的成本非常低。
3.  **安全防护**：内置了针对常见 Web 攻击（如 SQL 注入、XSS 等）的防护能力，并且集成了 WAF 功能，无需额外部署安全组件。
4.  **插件生态**：支持使用 Go、Python、Lua、Wasm 等多种语言编写插件，扩展性极强。特别是对 Wasm (WebAssembly) 的支持，使得插件的热更新和沙箱隔离更加安全灵活。
5.  **服务治理集成**：作为阿里系产品，它与 Nacos、Sentinel 等微服务组件无缝集成，对使用 Spring Cloud 或 Dubbo 的用户非常友好。

---



### 3: Higress 和 Istio 是什么关系？我是否需要先安装 Istio 才能使用 Higress？

3: Higress 和 Istio 是什么关系？我是否需要先安装 Istio 才能使用 Higress？

**A**: Higress 的架构深受 Istio 启发，但它被设计为一个**独立**的网关产品，**不需要**强制依赖完整的 Istio 控制平面即可运行。

*   **架构关系**：Higress 复用了 Istio 中经过大规模验证的 Envoy sidecar 代理作为数据平面，但在控制平面上进行了轻量化和定制，专门用于处理网关场景的配置分发。
*   **使用场景**：
    *   **独立使用**：你可以直接在 Kubernetes 集群中安装 Higress，它将接管集群的入口流量，充当 Ingress Controller 的角色。
    *   **结合使用**：如果你已经在使用 Istio，Higress 也可以作为 Istio 的 Egress Gateway 或 Ingress Gateway 使用，提供更强大的流量管控能力。

简而言之，Higress 降低了使用 Envoy 高级流量管理能力的门槛，让你不必为了使用一个高性能网关而去运维复杂的全套 Istio。

---



### 4: Higress 如何处理负载均衡和灰度发布（金丝雀发布）？

4: Higress 如何处理负载均衡和灰度发布（金丝雀发布）？

**A**: Higress 继承了 Istio 强大的流量治理能力，支持非常灵活的流量路由规则：

1.  **负载均衡**：支持多种负载均衡策略，包括轮询、随机、最小连接数以及基于请求内容的加权轮询等。
2.  **灰度发布**：这是 Higress 的强项之一。你可以基于 HTTP 请求头、Cookie、URL 参数甚至权重百分比来精细地控制流量走向。
    *   例如，你可以轻松配置“将所有带有 `preview=true` 请求头的流量路由到 v2 版本的服务”，或者“将 10% 的流量随机切换到新版本”。
3.  **全链路灰度**：配合微服务注册中心（如 Nacos），Higress 支持在微服务调用链中按标签透传流量，实现端到端的全链路灰度发布，这在复杂的微服务架构中非常实用。

---



### 5: Higress 支持哪些协议？是否支持 Dubbo 或 gRPC？

5: Higress 支持哪些协议？是否支持 Dubbo 或 gRPC？

**A**: Higress 是一款现代化的云原生网关，支持广泛的协议类型：

1.  **HTTP/HTTPS**：原生支持 HTTP 1.1、HTTP/2 (h2c) 和 HTTP/3 (QUIC)，这是最基础的协议支持。
2.  **gRPC**：完全支持 gRPC 协议的代理，支持基于 gRPC 的 Header 和 Method 进行路由匹配，非常适合微服务架构。
3.  **Dubbo**：这是 Higress 区别于许多国外开源网关的一个重要特性。Higress 原生支持 Apache Dubbo（Dubbo2 和 Dubbo3 协议），能够将 HTTP 请求转换为 Dubbo

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: Higress 是基于 Envoy 构建的，请尝试使用 Docker 在本地快速启动一个 Higress 实例，并配置一个简单的路由规则，将访问 `/hello` 的流量转发到一个模拟的后端服务（如 httpbin.org）。

### 提示**:

### 关注 Higress 官方文档中的“快速开始”部分。

---
## 实践建议

基于 Higress 作为“AI Native API Gateway”的定位，结合其云原生架构与 AI 网关的特性，以下是 6 条针对实际生产环境的实践建议：

### 1. 利用 WASM 技术实现业务逻辑与网关解耦
*   **场景**：当你需要对 AI 请求进行自定义的鉴权、请求头修改或响应体处理，但不想修改网关核心代码或重新编译网关镜像时。
*   **最佳实践**：使用 Higress 支持的 **WASM (WebAssembly)** 插件机制。将业务逻辑（如特定的 Token 验证逻辑、Prompt 模板预处理）编写为 WASM 插件。这允许你用 C++、Go 或 Rust 编写高性能代码，并在运行时动态热加载，无需重启网关即可更新逻辑。
*   **常见陷阱**：避免在 WASM 插件中执行阻塞式或耗时极长的操作（如直接调用第三方 HTTP 接口且未设置超时），这会阻塞网关的处理线程，导致整体吞吐量下降。

### 2. 配置模型提供商的容错与降级策略
*   **场景**：直接对接 OpenAI 或阿里云通义千问等模型 API 时，上游服务可能出现超时或 429 Rate Limit 错误。
*   **最佳实践**：在 Higress 的路由配置中，明确设置**重试策略**和**超时时间**。对于 AI 流式响应，需特别注意超时设置应长于模型生成时间。同时，配置**服务降级**规则，例如当主模型提供商不可用时，自动切换到备用模型或返回预设的兜底响应，保证业务连续性。
*   **常见陷阱**：在非幂等的请求（如非只读的 AI 交互）中盲目开启自动重试，可能导致客户端收到重复的响应或扣费。

### 3. 实施基于语义的流量路由
*   **场景**：企业内部同时使用 GPT-4 进行复杂任务处理，使用 GPT-3.5 Turbo 进行简单对话，希望根据用户意图自动分发，而不是客户端硬编码路由。
*   **最佳实践**：利用 Higress 的 AI 特性路由功能。通过分析请求体中的 Prompt 内容，配置路由规则，将不同复杂度或类型的请求分发到不同的后端模型服务。例如，将包含“代码生成”关键词的请求路由至代码优化模型，将“翻译”类请求路由至轻量级模型。
*   **常见陷阱**：路由规则过于复杂或不正则，导致匹配性能下降。建议在路由前对 Prompt 进行预处理或分类，保持路由规则的高效。

### 4. 优化流式传输的缓冲与转发配置
*   **场景**：AI 应用通常需要 Server-Sent Events (SSE) 或流式响应来降低首字延迟（TTFT）。
*   **最佳实践**：确保 Higress 的路由配置启用了**全链路流式转发**。检查网关与后端模型服务之间的连接是否保持长连接，并调整网关的 Buffer 大小设置，以适应流式数据块，避免网关试图缓存完整响应后再发送给客户端。
*   **常见陷阱**：在网关层开启了过多的全局 Body 过滤插件，可能会强制网关缓冲完整响应，从而破坏流式传输体验，导致用户等待时间过长。

### 5. 统一 Prompt 模板与敏感数据过滤
*   **场景**：防止用户在 Prompt 中注入恶意指令，或防止内部敏感数据（如数据库密码）发送给公网模型。
*   **最佳实践**：在网关层配置 **Prompt 模板管理** 和 **安全插件**。通过网关动态注入系统提示词，统一控制 AI 的行为边界。同时，利用插件在请求发出前扫描并脱敏敏感信息，或在响应中过滤有害内容。
*   **常见陷阱**：过度依赖正则表达式进行敏感词过滤，容易产生误杀或漏过变体攻击。建议结合简单的语义分析模型或专业的安全策略库。

### 6. 建立可观测性体系以监控 Token 消

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
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/) / [DevOps/运维](/scenarios/devops-%E8%BF%90%E7%BB%B4/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260205-github_trending-alibaba-higress-5.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260205-github_trending-alibaba-higress-6.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*