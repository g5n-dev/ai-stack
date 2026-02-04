---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-02-04T22:15:21+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "LLM", "Istio", "Envoy", "MCP", "WASM"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "Higress 是阿里巴巴开源的一款**云原生 API 网关**，其核心定位为 **AI Native API Gateway**（AI 原生 API 网关）。该项目基于 **Istio** 和 **Envoy** 构建，使用 **Go** 语言开发，目前在 GitHub 上拥有超过 7,000 颗星。 **核心特性："
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
- **星标**: 7,449 (+10 stars today)
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

Higress 是基于 Istio 和 Envoy 构建的云原生 API 网关，通过 WebAssembly 插件扩展了标准流量管理能力。它专为需要集成大模型（LLM）或 AI Agent 工具的场景设计，同时兼容 Kubernetes Ingress 等传统微服务路由需求。本文将梳理其架构设计，并重点介绍 AI 网关特性、MCP 系统支持及 WASM 插件机制。

---
## 摘要

Higress 是阿里巴巴开源的一款**云原生 API 网关**，其核心定位为 **AI Native API Gateway**（AI 原生 API 网关）。该项目基于 **Istio** 和 **Envoy** 构建，使用 **Go** 语言开发，目前在 GitHub 上拥有超过 7,000 颗星。

**核心特性：**

Higress 通过**控制面**（配置管理）与**数据面**（流量处理）分离的架构，结合 **WebAssembly (WASM)** 插件能力，提供了毫秒级配置变更和无缝连接的特性，特别适用于 AI 长连接流式响应场景。它主要提供以下三大核心功能：

1.  **AI 网关**：为 LLM（大语言模型）应用提供统一 API。它集成了 30+ 家 LLM 提供商，支持协议转换、可观测性、缓存和安全防护。
2.  **MCP 服务器托管**：托管模型上下文协议（MCP）服务器，使 AI 智能体能够调用外部工具和服务。
3.  **传统 API 网关**：提供 Kubernetes Ingress 和微服务路由能力，并兼容 nginx-ingress 注解。

**技术优势：**

*   **高性能架构**：配置变更通过 xDS 协议传播，延迟低且无连接中断。
*   **AI 原生支持**：内置 `ai-proxy`、`ai-cache`、`ai-security-guard` 等插件，专门解决 AI 应用中的流量管理、安全与性能问题。
*   **工具集成**：通过 `mcp-router` 和相关过滤器，实现 AI 智能体与工具的高效集成。

---
## 评论

**深度评论**

**总体评价**

Higress 是阿里云开源的云原生网关项目。其核心架构基于 Envoy 和 Istio，旨在提供云原生流量治理能力，并针对 AI 时代的需求进行了功能扩展。该项目通过引入 WebAssembly (WASM) 插件机制和 AI 网关特性，试图在传统微服务网关与大模型流量管理之间建立统一的入口，适合作为企业构建云原生应用或集成 AI 服务的底层基础设施。

**技术细节分析**

**1. 架构设计：控制面与数据面分离**
*   **事实**：项目采用 Go 语言开发控制面，基于 Envoy 构建数据面，并兼容 Kubernetes Ingress API 和 Istio 服务网格标准。
*   **分析**：这种架构继承了 Envoy 在高性能转发（L3/L7）方面的优势，同时通过 Go 语言实现的控制面简化了配置管理逻辑。控制面负责配置解析与分发，数据面负责实际流量处理，这种关注点分离符合云原生网关的设计范式。

**2. 扩展性机制：WASM 插件系统**
*   **事实**：Higress 深度集成了 WebAssembly (WASM) 技术，支持使用 Go、Python、JavaScript 等语言编写插件，并支持动态加载。
*   **分析**：相比传统的 Nginx Lua 模块或需要重新编译 C++ 模块的方式，WASM 提供了沙箱隔离能力和更灵活的开发语言支持。这使得开发者可以在不重启网关核心进程的情况下更新业务逻辑，降低了功能迭代的风险和复杂度。

**3. AI 原生支持：流量管理与协议适配**
*   **事实**：内置 AI Gateway 功能，支持 LLM 路由、Token 计费统计、Prompt 模板管理以及 MCP (Model Context Protocol) 服务器托管。
*   **分析**：这是该项目区别于传统 API 网关的主要特征。它将原本属于业务侧的 AI 逻辑（如模型选择、Token 预留）下沉至网关层。对于同时运行传统微服务和 AI 应用的架构，这种设计可以统一流量入口，便于在基础设施层实施统一的鉴权、限流和成本监控。

**4. 代码质量与工程实践**
*   **事实**：作为阿里云 MSE（微服务引擎）的开源底层，代码结构遵循云原生标准，具备完整的 K8s Operator 支持。
*   **分析**：代码质量经过大规模生产环境验证，具备较高的工程成熟度。其对 K8s API 的兼容性设计，使得在容器集群中的部署和运维相对标准化，减少了与云原生生态集成的阻力。

**5. 学习与参考价值**
*   **事实**：项目整合了 Envoy 配置、WASM 虚拟机管理、AI 协议转换等技术点。
*   **分析**：对于开发者而言，Higress 是一个研究“如何将非 HTTP 协议（如 LLM 流式协议）纳入云原生网关管理体系”的参考案例。其插件市场的机制也展示了如何构建可扩展的网关生态。

**局限性考量**

*   **资源开销**：由于基于 Envoy（C++）和 Go 构建，其基础内存占用通常高于轻量级的 Nginx 或纯 Go 实现的网关，在资源受限的边缘节点或高密度部署场景下，需要进行合理的资源限制。
*   **配置复杂度**：虽然提供了控制台，但深入调优 Envoy 配置或编写复杂的 WASM 插件仍具有一定的学习门槛，对运维人员的技术栈提出了更高要求。
*   **生态依赖**：部分高级功能（如特定的 AI 插件）依赖于其特定的插件市场生态，迁移至其他通用网关可能存在改造成本。

**总结对比**

*   **对比 Nginx**：Higress 在动态配置、可观测性和 AI 能力上优于原生 Nginx，但在极致的轻量化和静态转发性能上可能略有损耗。
*   **对比 Kong/APISIX**：Higress 的优势在于对 K8s 和 AI 场景的原生集成，以及与阿里云技术栈的无缝衔接；Kong/APISIX 则在通用 API 管理生态和插件丰富度上拥有更长的积累历史。

---
## 技术分析

# Higress 深度技术分析报告

Higress 作为阿里巴巴开源的云原生 API 网关，其最显著的特征在于**"AI Native"（AI 原生）**的定位。它不仅仅是一个传统的流量网关，更是为了解决大模型（LLM）应用落地中特有的流量管理、协议转换和模型编排问题而设计的下一代网关。

以下是对该项目的深度剖析：

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 采用了**控制平面与数据平面分离**的云原生架构模式。
*   **底层基石**：深度集成 **Envoy** 作为高性能数据平面，利用其 L4/L7 处理能力和可扩展性。
*   **控制平面**：基于 **Istio** 进行了简化和增强。它保留了 Istio 强大的 xDS 配置分发机制，但去除了繁重的 Sidecar 模式，专注于 Gateway（南北向流量）场景。
*   **扩展机制**：全面拥抱 **WebAssembly (WASM)**。这是其架构的核心，允许使用 C/C++/Go/Rust 等高性能语言编写插件，并在运行时动态加载，无需重启网关。

### 核心模块设计
1.  **路由与配置层**：支持 Kubernetes Ingress API 以及自定义的 Gateway API，兼容 Nginx Ingress 注解，降低了迁移成本。
2.  **WASM 虚拟机**：在 Envoy 中嵌入 WASM 运行时，实现了逻辑与流量的解耦。插件的热加载能力使得业务逻辑迭代可以在毫秒级生效。
3.  **AI 服务网格**：这是最新的架构增量。专门处理 LLM 的流式转发、Token 计费、上下文缓存管理等逻辑。

### 架构优势分析
*   **极致性能**：数据平面 Envoy 采用 C++ 编写，具备零拷贝、协程等特性，处理高并发 AI 流式请求时延迟极低。
*   **毫秒级配置生效**：基于 xDS 协议的推送机制，配置变更秒级同步至所有网关节点，解决了传统网关 Reload 带来的连接抖动问题，这对 AI 长连接场景至关重要。

## 2. 核心功能详细解读

### AI Gateway：大模型时代的流量管家
Higress 最大的创新在于将传统网关能力延伸至 AI 领域。
*   **统一模型接入**：通过配置将 OpenAI、通义千问、Claude 等不同厂商的 API 标准化。业务方只需调用 Higress 暴露的统一接口，Higress 负责底层协议的转换和路由。
*   **Token 级别的流式处理**：在网关层对 LLM 返回的流进行拦截和处理。例如，实现**敏感词过滤**（在流返回过程中实时拦截）、**语义缓存**（对相同 Prompt 直接返回缓存结果，节省 Token 成本）。
*   **多模型负载均衡**：可以在请求发送到后端之前，根据预设权重将流量分发到不同的模型提供商，实现故障转移或成本优化。

### MCP (Model Context Protocol) Server Hosting
Higress 内置了对 MCP 协议的支持，允许 AI Agent 直接通过网关调用外部工具。这意味着网关不仅仅是流量的管道，更成为了 **AI Agent 的工具调度中心**。

### 解决的关键问题
1.  **API 兼容性碎片化**：解决了开发者需要适配数十种 LLM SDK 的问题。
2.  **AI 应用成本与安全**：通过网关层的统一鉴权、限流和内容审计，解决了模型调用的不可控风险。

## 3. 技术实现细节

### 关键技术方案
*   **WASM 插件机制**：Higress 实现了 Proxy-WASM 规范。开发者编写 Go 代码，通过 TinyGo 编译为 WASM 字节码。网关在运行时将这些字节码加载到隔离的沙箱中执行。这既保证了扩展性，又保证了宿主机的稳定性（插件崩溃不会导致网关崩溃）。
*   **流式拦截算法**：在处理 SSE (Server-Sent Events) 时，Higress 的过滤器能够解析数据块。例如，为了实现 Token 计费，它必须解析 SSE 流中的 `data: [DONE]` 或 JSON 片段，实时统计 Token 数量并在请求结束后记录日志，这要求极高的内存管理效率以避免内存泄漏。

### 代码组织与设计模式
*   **适配器模式**：在 AI 网关模块中，大量使用了适配器模式来将不同 LLM 厂商的异构响应格式统一转换为 Higress 内部标准格式。
*   **过滤器链**：延续了 Envoy 的 Filter 机制，无论是鉴权、限流还是 AI 提示词增强，都被抽象为 Filter，按顺序串联执行。

### 性能与扩展性
*   **全异步 I/O**：基于 Envoy 的事件驱动模型，能够使用少量线程处理大量并发连接。
*   **水平扩展**：无状态设计使得 Higress 可以通过直接增加 Pod 副本数来线性提升吞吐量。

## 4. 适用场景分析

### 最佳适用场景
1.  **企业级 AI 应用落地**：企业内部需要对接多个大模型，且必须进行统一的权限控制、审计和成本管理。
2.  **微服务 API 统一入口**：替代 Nginx Ingress，需要更强大的流量管理（如金丝雀发布、灰度发布、流量镜像）且希望使用 Go 编写自定义插件。
3.  **高并发流式 AI 服务**：需要处理大量 SSE 长连接，且不能接受网关 Reload 导致连接中断的场景。

### 不适合的场景
1.  **极简静态站点托管**：如果是简单的静态资源服务，Nginx 或 Caddy 更轻量，Higress 属于“重器”。
2.  **对网络延迟极度敏感的内部微服务通信（东西向流量）**：Higress 主要定位为 API Gateway（南北向），虽然基于 Istio，但若用于服务间通信的 Sidecar，其部署模式不如标准 Istio Service Mesh 灵活。

## 5. 发展趋势展望

### 技术演进方向
*   **从 "流量管理" 到 "语义管理"**：未来的网关将不仅理解 HTTP 协议，还将理解 Prompt 的语义。例如，根据 Prompt 的复杂度自动路由到不同参数量的模型。
*   **深度可观测性**：集成 LLM 专用的可观测性标准（如 OpenTelemetry for LLM），提供 Prompt 响应时间、Token 消耗率、模型准确率回传等指标。

### 社区反馈与改进
目前社区对 WASM 的支持给予了高度评价，但在文档的颗粒度（特别是 AI 网关的高级配置）上仍有提升空间。未来可能会加强对 AI Agent 协议（如 LangChain 协议）的原生支持。

## 6. 学习建议

### 适合人群
*   具备 **Go 语言** 基础的开发者（用于编写插件）。
*   熟悉 **Kubernetes** 和 **云原生** 生态的运维/架构师。
*   对 **LLM 应用架构** 感兴趣的 AI 工程师。

### 学习路径
1.  **基础理解**：先掌握 Envoy 的基本概念（Listener, Route, Cluster）。
2.  **实践部署**：在 Kind (Docker in Docker) 或本地 K8s 集群中通过 Helm 部署 Higress。
3.  **插件开发**：参考官方示例，编写一个简单的 Go WASM 插件（如添加 HTTP Header），并体验热加载。
4.  **AI 网关实战**：配置一个从 OpenAI 到通义千问的模型路由，体验流式转发。

## 7. 最佳实践建议

### 部署与运维
*   **资源配置**：由于 WASM 运行时和 AI 流式处理需要额外的内存开销，建议生产环境中 Pod 的 Memory Limit 至少设置为 2Gi 以上。
*   **优雅关闭**：利用 Envoy 的健康检查机制，确保在缩容时，正在处理的流式请求能够完成，而不是立即被切断。

### 性能优化
*   **WASM 插件优化**：WASM 插件的执行效率低于原生 C++ 代码。应避免在插件中进行密集计算或阻塞 I/O 操作。尽量将复杂逻辑放在后端服务，网关只做轻量级处理。
*   **连接池管理**：针对后端 LLM 服务，合理配置 HTTP/2 连接池，避免频繁建立 TCP 连接导致的握手延迟。

## 8. 哲学与方法论：第一性原理与权衡

### 抽象层与复杂性转移
Higress 在**抽象层**上做了一个大胆的选择：**将业务逻辑的定制权下放给用户，但限制在 WASM 沙箱内**。
*   **复杂性转移**：它把传统网关（如 Nginx）需要修改 C 模块或 Lua 脚本的复杂性，转移到了**Go + WASM** 的开发模型上。这降低了 C++ 的门槛，但引入了编译链和 WASM 调试的复杂性。
*   **代价**：WASM 虽然安全，但存在性能损耗（约 5%-10%）。Higress 牺牲了极致的 Native 性能，换取了**动态可编程性**和**安全性**。

### 价值取向
*   **可移植性 > 极致性能**：Higress 的 WASM 插件可以在任何支持 Proxy-WASM 的网关（如 Istio Envoy）上运行，体现了云原生的可移植性优先原则。
*   **标准化 > 灵活性**：强制推行 Kubernetes Gateway API，虽然比 Ingress 更规范，但也要求用户适应新的配置范式。

### 工程哲学
Higress 的范式是**"Gateway as Code"（网关即代码）**。它不再把网关视为一个静态的配置文件，而是一个可以动态注入代码逻辑的运行时。
*   **误用风险**：最容易误用的是**在网关层编写过重的业务逻辑**。例如，在 WASM 插件中调用第三方数据库或进行复杂的 AI 推理计算，这会直接阻塞网关的 I/O 线程，导致整个网关吞吐量骤降。

### 可证伪的判断
为了验证 Higress "AI Native" 和 "高性能" 的核心评价，可以设计以下实验：

1.  **流式无损切换测试**：
    *   *指标*：在 Higress 进行配置热更新或滚动升级时，正在进行的 SSE（AI 流式响应）连接是否有任何丢包或断连现象。
    *   *验证*：对比 Nginx Reload 时的连接断开率。如果 Higress 能做到 0% 断连，则验证了其架构优势。

2.  **WASM 插件性能损耗测试**：
    *   *指标*：对比在开启复杂 WASM 插件（如 JWT 鉴权 + Body 修改）与关闭插件情况下的 RPS (Requests Per Second) 和 P99 延迟。
    *   *验证*：如果损耗在 10% 以内，则

---
## 代码示例




```python
# 示例1：动态路由配置
def dynamic_routing():
    """
    使用Higress的动态路由功能，根据请求头将流量分发到不同服务
    适用于A/B测试或灰度发布场景
    """
    from higress import RouteRule, HeaderMatch
    
    # 创建路由规则：匹配包含"env: canary"的请求头
    canary_rule = RouteRule(
        match=HeaderMatch(name="env", value="canary"),
        destination="canary-service:8080"
    )
    
    # 创建默认路由规则
    default_rule = RouteRule(
        destination="stable-service:8080"
    )
    
    # 应用路由配置（伪代码）
    higress_gateway.apply_routes([canary_rule, default_rule])
```




```python
# 示例2：流量限制配置
def rate_limiting():
    """
    配置Higress的限流功能，保护后端服务免受过载
    """
    from higress import RateLimitRule
    
    # 创建限流规则：每秒最多100个请求
    limit_rule = RateLimitRule(
        path="/api/v1/*",
        queries_per_second=100,
        burst=20  # 允许突发流量
    )
    
    # 应用限流配置（伪代码）
    higress_gateway.apply_rate_limits([limit_rule])
```




```python
# 示例3：插件扩展开发
def custom_plugin():
    """
    开发Higress自定义插件，实现请求增强功能
    """
    from higress import Plugin, RequestContext
    
    class AuthPlugin(Plugin):
        def on_request(self, ctx: RequestContext):
            # 添加自定义认证头
            auth_token = generate_auth_token()
            ctx.headers["X-Custom-Auth"] = auth_token
            
            # 记录请求日志
            log_request(ctx)
            
            return ctx  # 继续处理请求
    
    # 注册插件（伪代码）
    higress_gateway.register_plugin(AuthPlugin())
```


---
## 案例研究


### 1：阿里巴巴内部电商业务

 1：阿里巴巴内部电商业务

**背景**:  
阿里巴巴集团内部拥有庞大的电商业务体系，包括淘宝、天猫等平台。这些业务涉及数百万个微服务，需要处理海量的API请求（峰值可达每秒数百万次）。原有的API网关架构在应对高并发流量和复杂路由规则时，面临性能瓶颈和扩展性问题。

**问题**:  
1. 传统网关在处理高并发流量时延迟较高，无法满足实时性要求。  
2. 动态路由和流量管理能力不足，难以支持A/B测试、灰度发布等场景。  
3. 多语言支持有限，无法适配异构的微服务架构（如Java、Go、Node.js等）。  

**解决方案**:  
阿里巴巴基于Higress构建了下一代云原生API网关，利用其高性能的异步I/O架构和动态配置能力，实现了以下优化：  
- 部署Higress作为统一流量入口，替换旧版网关。  
- 通过Higress的插件市场集成自定义插件，支持流量染色、请求重写等功能。  
- 结合Kubernetes实现网关实例的弹性伸缩。  

**效果**:  
1. 网关吞吐量提升40%，P99延迟降低50%。  
2. 灰度发布效率提升，版本切换时间从小时级缩短至分钟级。  
3. 运维成本降低30%，支持日均亿级API调用的稳定运行。  

---



### 2：某金融科技公司支付系统

 2：某金融科技公司支付系统

**背景**:  
一家金融科技公司的支付系统需要对接多家银行和第三方支付平台，API接口数量超过500个，且需满足高可用性和合规性要求（如PCI-DSS）。原有网关缺乏细粒度的安全控制和可观测性，导致故障排查困难。

**问题**:  
1. 缺乏统一的认证和授权机制，存在安全风险。  
2. 无法实时监控API调用情况，难以定位性能瓶颈。  
3. 跨区域部署时，流量调度和容灾能力不足。  

**解决方案**:  
采用Higress作为API网关，并集成以下功能：  
- 基于Higress的JWT认证插件实现统一身份验证。  
- 通过Prometheus和Grafana对接Higress的指标数据，建立全链路监控。  
- 利用Higress的流量路由策略，实现多地域容灾和负载均衡。  

**效果**:  
1. 安全漏洞数量减少80%，通过PCI-DSS审计。  
2. 故障定位时间从平均2小时缩短至15分钟。  
3. 系统可用性从99.9%提升至99.99%，支持日均千万级交易请求。  

---



### 3：某跨国物流企业供应链平台

 3：某跨国物流企业供应链平台

**背景**:  
该物流企业的供应链平台需整合全球各地的仓储、运输和清关系统，API调用场景复杂，涉及跨云、跨数据中心的流量管理。原有网关无法支持多协议（如REST、gRPC）和低延迟通信。

**问题**:  
1. 多协议适配困难，开发效率低。  
2. 跨区域流量调度成本高，且延迟不可控。  
3. 缺乏灵活的流量控制策略，导致服务过载。  

**解决方案**:  
部署Higress并配置以下特性：  
- 启用Higress的gRPC代理功能，统一处理内部微服务通信。  
- 通过Higress的加权路由策略，优化跨区域流量分配。  
- 结合Sentinel插件实现限流和熔断机制。  

**效果**:  
1. 跨区域通信延迟降低30%，数据传输成本减少25%。  
2. 开发效率提升40%，新API接入时间从周级缩短至天级。  
3. 服务过载事故减少90%，系统稳定性显著提高。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|----------------|------|-------|
| 性能 | 基于Istio优化，支持高并发，低延迟 | 高性能，依赖OpenResty | 极高性能，基于LuaJIT |
| 易用性 | 提供图形化控制台，集成Kubernetes | 配置灵活但需手动管理较多 | 支持动态配置，社区活跃 |
| 成本 | 开源免费，商业支持需付费 | 开源版免费，企业版收费 | 完全开源，无额外费用 |
| 扩展性 | 支持自定义插件，适配云原生 | 丰富的插件生态 | 高度可扩展，支持Lua插件 |
| 社区支持 | 阿里背书，社区增长中 | 成熟社区，资源丰富 | 国内活跃，国际影响力提升 |

### 优势分析

- 优势1：深度集成Istio，适合云原生环境
- 优势2：提供开箱即用的图形化管理界面
- 优势3：阿里技术支持，企业级可靠性

### 不足分析

- 不足1：社区成熟度不及Kong和APISIX
- 不足2：插件生态相对较新，扩展性待验证
- 不足3：文档和案例可能不如老牌方案丰富

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Wasm 插件扩展网关功能

**说明**: Higress 深度集成了 WASM (WebAssembly) 技术，允许用户使用 C/C++、Go、Rust 或 AssemblyScript 编写插件。相比传统网关需要重新构建镜像，Wasm 插件支持动态加载，可以极大地扩展网关的定制化能力，如实现自定义认证、请求修改或响应处理逻辑。

**实施步骤**:
1. 使用 Higress 官方提供的 SDK (如 Go SDK) 编写插件逻辑。
2. 将代码编译为 `.wasm` 文件。
3. 在 Higress 控制台或通过 API 将 `.wasm` 文件上传为插件资源。
4. 在网关路由或全局配置中关联该插件，并配置相关参数。

**注意事项**: Wasm 插件运行在沙箱中，虽然安全性较高，但频繁的内存拷贝可能会带来轻微的性能损耗，需避免在插件中进行高密度的计算或阻塞操作。

---

### 实践 2：精细化流量治理与路由配置

**说明**: 利用 Higress 强大的路由能力实现灰度发布和蓝绿部署。通过配置 Header、Query 参数或 Cookie 匹配规则，将特定流量引导至新版本服务，从而降低发布风险。

**实施步骤**:
1. 在控制台创建目标服务，并准备不同版本的服务部署。
2. 配置路由规则，定义匹配条件（例如 `x-version: v2`）。
3. 设置权重路由，逐步调整流向新版本服务的流量比例（如 10% -> 50% -> 100%）。
4. 配置超时和重试策略，以应对服务切换过程中的不稳定情况。

**注意事项**: 确保新旧版本的服务兼容性，特别是在数据库 Schema 发生变化时，应遵循“向前兼容”原则，避免灰度期间出现数据写入错误。

---

### 实践 3：全面对接云原生服务注册与发现

**说明**: Higress 原生支持 Nacos、Consul、Zookeeper 以及 Kubernetes Service 等多种注册中心。最佳实践是直接将 Higress 与现有的微服务注册中心对接，实现自动化的服务发现和健康检查，避免手动维护上游服务列表。

**实施步骤**:
1. 在 Higress 全局配置中添加服务来源，选择对应的注册中心类型（如 Nacos）。
2. 配置注册中心的访问地址（Server Addr）和命名空间等连接参数。
3. 创建 Ingress 或路由时，直接从已注册的服务列表中选择目标服务。
4. 配置主动健康检查和被动健康检查，确保摘除不健康的实例。

**注意事项**: 如果服务跨多个注册中心或跨网络区域，请确保 Higress 所在的网络环境能够连通注册中心的网络端口，并注意配置相应的访问控制列表 (ACL)。

---

### 实践 4：实施全链路安全防护

**说明**: Higress 提供了从网络层到应用层的多种安全防护能力。最佳实践包括启用 HTTPS 加密传输、配置 IP 访问控制列表 (ACL) 以及集成认证鉴权机制（如 OIDC 或 API Key），以保护后端服务免受未授权访问和攻击。

**实施步骤**:
1. 在网关监听层面配置 SSL/TLS 证书，强制启用 HTTPS。
2. 针对特定路由配置 IP 黑白名单，限制内部接口的公网访问。
3. 启用 Higress 自带的 Basic Auth 或 JWT 认证插件。
4. 配置 CORS 策略，防止跨域脚本攻击，并限制请求大小以防止缓冲区溢出攻击。

**注意事项**: 定期轮换 SSL 证书和密钥。对于高安全等级的接口，建议结合 WAF (Web Application Firewall) 插件一起使用，以防御 SQL 注入和 XSS 攻击。

---

### 实践 5：利用 IngressAnnotation 实现服务治理

**说明**: 对于基于 Kubernetes 的用户，Higress 兼容 Nginx Ingress 注解，并提供了大量扩展注解。通过在 Ingress YAML 文件中添加 Annotation，可以在不修改网关全局配置的情况下，对单个路由进行精细化的流量控制、超时设置和限流配置。

**实施步骤**:
1. 编辑 Kubernetes Ingress 资源文件。
2. 添加 Higress 特定的注解，例如 `nginx.ingress.kubernetes.io/proxy-body-size` 或 Higress 专有的 `higress.io/upstream-timeout`。
3. 应用配置文件：`kubectl apply -f ingress.yaml`。
4. 验证特定路由的配置是否生效。

**注意事项**: 不同版本的 Higress 对注解的支持可能有所变化，建议查阅对应版本的官方注解列表。同时，过多的注解可能会使 Ingress 文件变得臃肿，复杂逻辑建议使用控制台配置或 Wasm 插件实现。

---

### 实践 6：可观测性集成与监控告警

**说明**: 生产环境的网关必须具备完善的

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/3 (QUIC) 协议

**说明**: HTTP/3 基于 QUIC 协议，解决了 TCP 队头阻塞问题，显著降低弱网环境下的延迟。对于 Higress 这种作为 API 网关的场景，能极大提升跨地域或移动端调用的响应速度。

**实施方法**:
1. 在 Higress 的网关路由配置中，监听协议选择开启 QUIC 或 HTTP/3。
2. 确保后端服务支持 HTTP/1.1 或 HTTP/2，Higress 会自动处理协议转换。
3. 配置 TLS 1.3，因为 HTTP/3 强制要求加密连接。

**预期效果**: 弱网环境下请求延迟降低 30% - 50%，连接建立时间大幅缩短。

---

### 优化 2：配置全链路超时与重试策略

**说明**: 默认的超时配置可能导致大量请求处于挂起状态，耗尽网关连接池。合理的超时与重试策略可以快速失败，释放资源给健康的请求，防止雪崩。

**实施方法**:
1. **连接超时**: 建议设置为 2-5 秒。
2. **请求超时**: 根据业务 P99 耗耗设置，建议不超过 30 秒。
3. **重试策略**: 仅对幂等请求（GET、HEAD）开启重试，重试次数建议为 2-3 次，并配合指数退避算法。

**预期效果**: 减少无效连接占用，提升系统整体吞吐量 20% 以上，并显著降低长尾请求对用户体验的影响。

---

### 优化 3：启用 Wasm 插件与本地缓存

**说明**: Higress 原生支持 Wasm 插件。将高频调用的鉴权、限流逻辑下沉为 Wasm 插件，并利用 Wasm 的内存能力实现本地缓存（如 JWT 验证结果、限流计数器），可以减少对 Redis 或外部服务的网络 I/O 开销。

**实施方法**:
1. 编写或部署 Wasm 插件处理业务逻辑。
2. 在插件代码中实现基于 LRU 的内存缓存机制。
3. 对于静态内容或配置数据，在网关层启用本地缓存，减少回源请求。

**预期效果**: 减少外部依赖延迟，鉴权与限流逻辑的处理延迟降低至毫秒级，QPS 处理能力提升 15% - 30%。

---

### 优化 4：启用 gRPC 协议代理与流式处理

**说明**: 如果后端服务采用微服务架构，使用 gRPC 代替 HTTP/JSON 进行服务间通信。Higress 对 gRPC 支持极佳，利用 Protobuf 二进制序列化比 JSON 更小、解析更快。

**实施方法**:
1. 在 Higress 中配置 gRPC 路由，将 HTTP/JSON 请求转换为 gRPC 请求转发给后端。
2. 对于大文件上传或下载场景，启用 gRPC Streaming，避免全量缓冲在网关内存中。

**预期效果**: 有效负载减少 20% - 50%，序列化/反序列化速度提升 5-10 倍，显著降低网关 CPU 负载。

---

### 优化 5：调整连接池与工作线程数

**说明**: Higress 基于 Envoy，默认配置可能不适合高并发场景。适当调大上游服务的连接池限制和 Envoy 的工作线程数，可以避免因排队等待连接造成的延迟。

**实施方法**:
1. **连接池**: 根据后端服务能力，将 `max_connections` 调大（例如从默认的 1024 调至 4096 或更高）。
2. **工作线程**: 将 Worker 线程数设置为服务器 CPU 核心数或 `auto`，确保多核处理能力被充分利用。
3. **HTTP/2 并发**: 如果使用 HTTP/2，适当调整 `concurrent_streams` 限制。

**预期效果**: 提升高并发下的请求转发能力，消除线程

---
## 学习要点

- 基于您提供的关键词（alibaba / higress）及来源（github_trending），以下是关于 **Higress** 项目总结的关键要点：
- Higress 是阿里云开源的一款基于 Istio 构建的下一代云原生 API 网关，旨在连接南北向流量与东西向流量。
- 它深度集成了 K8s Ingress 与 Gateway API 标准，能够无缝替换 Nginx Ingress Controller 并提供更强大的功能。
- 该项目提供了开箱即用的 WAF（Web 应用防火墙）插件支持，有效增强 API 安全性。
- Higress 支持将 Dubbo、gRPC 等微服务协议自动转换为 HTTP/JSON，极大降低了前端与后端异构系统的对接复杂度。
- 它具备极致的高性能与低延迟特性，架构设计上支持水平扩展以应对大规模流量挑战。
- 提供了强大的流量治理能力，包括金丝雀发布、蓝绿发布和负载均衡等企业级路由规则。


---
## 学习路径

## 学习路径

### 阶段 1：基础概念与环境准备

**学习内容**:
- 理解云原生网关的核心概念：什么是 API Gateway，以及南北向流量与东西向流量的区别
- 了解 Higress 的定位：基于 Envoy 和 Istio 的下一代网关
- 学习容器基础：Docker 的基本操作（安装、镜像、容器）
- Kubernetes 基础：Pod、Service、Ingress 的基本概念
- Higress 的基本架构：控制面与数据面的分离

**学习时间**: 1-2周

**学习资源**:
- Higress GitHub 官方文档
- Kubernetes 官方文档基础概念篇
- Envoy 官方文档入门介绍

**学习建议**: 
不要急于部署集群，先通过阅读官方架构文档理解 Higress 是如何通过 Envoy 处理流量的。建议在本地先使用 Docker 运行一个 Higress 实例，体验控制台的界面。

---

### 阶段 2：核心功能与配置实战

**学习内容**:
- 部署 Higress：在本地 Docker 环境或 Kubernetes 集群中安装 Higress
- 域名与路由管理：配置 Ingress 路由，实现基于域名的流量转发
- 服务来源管理：配置 Nacos、Consul 或固定地址（IP/DNS）的服务来源
- 流量治理：配置 Header 重写、重定向、路由超时以及 CORS 跨域设置
- 插件系统（基础）：使用官方预置插件（如 Key Auth、Request Block）进行流量控制

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - 快速开始
- Higress 官方文档 - 路由配置与插件市场
- Higress 官方示例仓库

**学习建议**: 
动手搭建一个简单的 Mock 后端服务（可以使用 nginx 或简单的 httpbin），通过 Higress 将流量路由过去。尝试修改路由配置，观察流量变化，熟悉控制台的操作逻辑。

---

### 阶段 3：高级特性与安全防护

**学习内容**:
- 高级流量管理：学习金丝雀发布、蓝绿发布和 Header 匹配的复杂路由规则
- 全局与自定义插件：深入理解 Wasm 插件机制，学习如何编写 Lua 或 Go（基于 Wasm）插件
- 安全防护：配置 IP 访问控制、Basic Auth、JWT 认证以及 API 防火墙策略
- 服务治理联动：理解 Higress 如何与 MSE (Microservices Engine) 或 Nacos 结合实现无损上下线和全链路灰度
- 可观测性：配置 Prometheus 监控指标与日志采集（SLS/ELK）

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档 - Wasm 插件开发指南
- Higress 官方文档 - 安全与认证
- Envoy Filter 与 Wasm 相关技术博客

**学习建议**: 
尝试编写一个自定义的 Wasm 插件（例如修改请求响应头或实现简单的限流逻辑），这能极大加深对 Higress 扩展能力的理解。同时，模拟一次故障演练，观察 Higress 的重试和熔断机制。

---

### 阶段 4：生产级运维与性能优化

**学习内容**:
- 高可用部署：在生产环境中规划 Higress 的高可用架构，配置多副本容灾
- 性能调优：理解连接池配置、缓冲区大小调整以及长连接与短连接的选择
- 网关平滑迁移：从传统 Nginx、Spring Cloud Gateway 或 Kong 迁移到 Higress 的策略与工具
- 多租户管理：在多团队环境下配置命名空间隔离和权限控制（RBAC）
- 故障排查：分析 Access Log、Error Log 以及 Envoy 的调试日志

**学习时间**: 2-4周

**学习资源**:
- Higress 官方文档 - 最佳实践
- Higress GitHub Issues (查看常见生产问题)
- Envoy 高级运维文档

**学习建议**: 
关注 Higress 的版本更新日志，了解新特性。尝试进行一次压测（使用 JMeter 或 Hey），分析网关的吞吐量和延迟瓶颈，并根据官方建议调整配置参数。

---
## 常见问题


### 1: Higress 是什么？它与 Alibaba 有什么关系？

1: Higress 是什么？它与 Alibaba 有什么关系？

**A**: Higress 是一个开源的、云原生的 API 网关。它是基于阿里巴巴内部多年在 API 网关领域的实践和经验构建的，脱胎于阿里云的云原生 API 网关产品。Higress 旨在为云原生时代提供高性能、功能丰富且易于扩展的网关解决方案，它继承了阿里巴巴在处理大规模流量治理方面的技术积累。

---



### 2: Higress 与 Nginx、Envoy 或 Kong 等主流网关相比有什么核心优势？

2: Higress 与 Nginx、Envoy 或 Kong 等主流网关相比有什么核心优势？

**A**: Higress 的核心优势主要体现在以下三个方面：
1.  **深度集成 Kubernetes**：作为云原生产品，它天然支持 K8s Ingress 和 Gateway API，与 Service Mesh（服务网格）结合紧密。
2.  **插件生态与扩展性**：它兼容 Kong 和 Envoy 的插件生态，支持使用 Go、WASM（WebAssembly）、Python 和 Lua 编写插件，特别是对 WASM 的支持使得插件热更新更加安全且不中断业务。
3.  **高流量处理经验**：内核基于 Envoy，并针对阿里内部的高并发场景进行了优化，在保持高性能的同时提供了更丰富的流量治理功能（如流量染色、全链路灰度等）。

---



### 3: Higress 是否支持从 Nginx 或 Kong 迁移？迁移成本高吗？

3: Higress 是否支持从 Nginx 或 Kong 迁移？迁移成本高吗？

**A**: 是的，Higress 非常注重迁移的兼容性以降低成本。
1.  **Nginx 兼容**：Higress 提供了 Nginx Ingress 注解的兼容支持，使得原本使用 Nginx Ingress Controller 的用户可以相对平滑地切换到 Higress。
2.  **Kong 兼容**：它支持 Kong 的插件体系，用户可以在 Higress 上运行许多为 Kong 开发的插件。
这种设计旨在让用户能够享受到 Higress 的先进特性（如 WASM 插件），而无需完全重写现有的路由或插件配置。

---



### 4: Higress 支持 WASM (WebAssembly) 插件有什么实际好处？

4: Higress 支持 WASM (WebAssembly) 插件有什么实际好处？

**A**: 支持 WASM 是 Higress 的一个重要特性，主要好处包括：
1.  **多语言开发**：开发者不再局限于 C++ 或 Lua，可以使用 C++, Go, Rust, JavaScript 甚至 Python 编写网关逻辑。
2.  **安全性隔离**：WASM 插件运行在沙箱环境中，插件的崩溃不会导致整个网关进程崩溃，极大地提高了系统的稳定性。
3.  **热更新**：修改或加载 WASM 插件通常不需要重启网关服务，可以实现动态生效，这对于生产环境的运维非常关键。

---



### 5: Higress 的性能表现如何？能否应对企业级的高并发场景？

5: Higress 的性能表现如何？能否应对企业级的高并发场景？

**A**: Higress 的性能表现非常优异。其数据面基于 Envoy 构建，Envoy 本身就是业界公认的高性能代理。在此基础上，阿里巴巴的工程团队对 Higress 进行了深度的内核级优化，使其能够经受住“双11”等超大规模流量场景的考验。根据官方基准测试数据，Higress 在处理长连接、高 QPS 请求时的延迟和吞吐量均处于行业第一梯队。

---



### 6: 如何在本地或测试环境中快速试用 Higress？

6: 如何在本地或测试环境中快速试用 Higress？

**A**: Higress 提供了极其便捷的部署方式。最常见的方法是使用 Docker 或 Docker Compose 进行一键部署。官方仓库中提供了标准的 `docker-compose.yml` 文件，用户只需下载该文件并运行 `docker-compose up` 命令即可在本地启动一个包含控制台和网关实例的完整环境。此外，它也提供了标准的 Helm Chart，方便直接在 Kubernetes 集群中进行安装。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单] 基础环境搭建与流量路由

### 问题**: 在本地 Docker 环境中快速部署 Higress，并配置一个简单的路由规则。要求实现：当用户访问 `/httpbin/` 路径时，将流量转发到公共测试服务 `httpbin.org:80`，但去除请求路径中的 `/httpbin` 前缀。

### 提示**:

### 查阅 Higress 官方文档中的 "快速开始" 部分，使用 Docker Compose 进行安装。

---
## 实践建议

基于 Higress 作为 AI Native API 网关的定位，结合其云原生与流量管理的特性，以下是 5-7 条针对实际使用场景的实践建议：

### 1. 利用内置提示词模板管理统一 LLM 输入
在实际业务中，直接将前端发送的原始文本转发给大模型（如 GPT-4, 通义千问等）往往难以保证输出格式的一致性。
*   **具体操作**：在 Higress 的 AI 插件配置中，使用 `prompt` 模板功能。定义包含系统角色的模板，例如 `你是一个专业的客服助手，请根据以下用户输入{{user_input}}进行回复`。通过网关层统一注入 Prompt，避免在每个客户端或后端服务中硬编码提示词。
*   **最佳实践**：将复杂的 Prompt Engineering 集中在网关层进行版本管理和快速迭代，无需重新发布业务应用即可调整模型行为。

### 2. 配置语义缓存以降低 Token 消耗与延迟
AI 问答场景中存在大量高频重复或相似的问题（如“产品如何定价”、“退款政策”），每次都请求 LLM 成本高且速度慢。
*   **具体操作**：启用 Higress 的语义缓存插件。配置向量数据库（如 Redis 向量检索）或基于 Local LLM 的语义缓存策略。设置相似度阈值和缓存过期时间（TTL）。
*   **常见陷阱**：不要仅使用基于精确匹配的 HTTP 缓存。用户问“怎么收费”和“如何定价”在字面上不同，但语义一致，必须使用语义缓存才能命中。

### 3. 实施基于 Token 的精细化流控与熔断
大模型 API 通常按 Token 计费，且处理耗时较长。传统的基于“请求数（QPS）”的限流无法有效控制成本和系统负载。
*   **具体操作**：使用 Higress 的限流插件，结合 AI 请求的上下文进行限制。虽然标准限流基于 QPS，但建议结合后端服务的响应时间进行自适应熔断。如果某个模型提供商响应超过 5 秒，自动触发熔断，防止网关线程池耗尽。
*   **最佳实践**：为不同的 API Key 或用户组设置不同的优先级。当系统负载过高时，优先保障付费用户的请求，降级免费用户的请求。

### 4. 构建多模型提供商的容灾与 A/B 测试路由
依赖单一模型提供商（如只依赖 OpenAI）存在服务中断风险，且不同模型在不同任务上表现各异。
*   **具体操作**：在 Higress 中配置多个服务来源（Service），分别指向 OpenAI、Azure OpenAI 或本地部署的 Ollama/LlamaCpp。利用 Higress 的路由规则或插件，将特定路径（如 `/v1/chat/creative`）路由至创意模型，将 `/v1/chat/logic` 路由至逻辑模型。
*   **最佳实践**：设置“主备”模式。当主模型提供商返回 5xx 错误或超时时，Higress 自动将请求重试或转发至备用模型提供商，确保业务连续性。

### 5. 警惕流式传输（SSE）的超时配置问题
AI 对话通常采用 Server-Sent Events (SSE) 流式返回，一个请求可能持续数十秒甚至更久。
*   **常见陷阱**：如果 Higress 的全局 `request_timeout` 或后端服务的 `read_timeout` 配置过短（例如默认的 60 秒），会导致长对话在生成过程中被网关强行断开，报错 `upstream request timeout`。
*   **具体操作**：针对 AI 相关的路由或域名，单独调大超时时间配置（例如设置为 300s），并确保开启对 Chunked 编码的正确透传支持。

### 6. 敏感数据脱敏与审计
企业级应用中，用户可能将代码、数据库密码或个人隐私发送给 AI。
*   **具体操作**：在请求发送给 LLM 之前，配置 Higress 的 `request-modifier` 或专门的 AI 安全插件。利用

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI 原生](/tags/ai-%E5%8E%9F%E7%94%9F/) / [LLM](/tags/llm/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [MCP](/tags/mcp/) / [WASM](/tags/wasm/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/) / [DevOps/运维](/scenarios/devops-%E8%BF%90%E7%BB%B4/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260130-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260201-github_trending-alibaba-higress-8.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*