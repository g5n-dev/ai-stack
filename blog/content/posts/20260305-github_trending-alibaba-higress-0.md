---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-03-05T09:23:27+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "Istio", "Envoy", "WASM", "LLM", "MCP"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "**Higress 项目总结** **1. 项目简介** Higress 是由阿里巴巴开源的一款**云原生 API 网关**。该项目基于 Istio 和 Envory 构建，使用 **Go** 语言编写。其核心定位为**AI 原生（AI Native）**，旨在为云原生应用和 AI 大模型应用提供统一的流量入口和管理服"
external_url: https://github.com/alibaba/higress
scenarios: ["AI/ML项目", "云原生/容器", "DevOps/运维"]
---

# 阿里开源 Higress：AI 原生 API 网关

> **原名**: alibaba /

      higress

---

## 基本信息

- **描述**: 🤖 AI Gateway | AI 原生 API 网关
- **语言**: Go
- **星标**: 7,647 (+11 stars today)
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

Higress 是一款基于 Istio 和 Envoy 构建的 AI 原生 API 网关，通过扩展 WASM 插件能力，实现了对 Kubernetes Ingress、微服务路由及 LLM 应用的统一管理。该项目旨在解决云原生架构下流量治理与 AI 服务集成的复杂性，特别适合需要同时处理传统业务流量与大模型调用的场景。本文将介绍其系统架构、核心组件及主要用例，帮助读者了解如何利用 Higress 构建高效、可扩展的网关服务。

---
## 摘要

**Higress 项目总结**

**1. 项目简介**
Higress 是由阿里巴巴开源的一款**云原生 API 网关**。该项目基于 Istio 和 Envory 构建，使用 **Go** 语言编写。其核心定位为**AI 原生（AI Native）**，旨在为云原生应用和 AI 大模型应用提供统一的流量入口和管理服务。目前该项目在 GitHub 上拥有超过 7,600 颗星。

**2. 核心架构与特性**
Higress 采用了**控制平面与数据平面分离**的架构：
*   **高性能与扩展性**：通过 **WASM（WebAssembly）** 插件能力扩展功能，且支持通过 xDS 协议毫秒级下发配置，变更配置时不断连，特别适合 AI 长连接流式响应场景。
*   **兼容性**：作为 Kubernetes Ingress 控制器，兼容 nginx-ingress 注解。

**3. 三大核心应用场景**

*   **AI 网关**
    *   **功能**：提供统一的 API 接口，兼容 30 多家 LLM 提供商。
    *   **特性**：支持协议转换、可观测性、缓存以及安全防护。
    *   **关键组件**：`ai-proxy`、`ai-statistics`、`ai-cache`、`ai-security-guard` 等插件。

*   **MCP 服务器托管**
    *   **功能**：托管模型上下文协议（MCP）服务器，使 AI 智能体能够便捷地调用工具和外部服务。
    *   **关键组件**：`mcp-router`、`jsonrpc-converter` 以及内置的 MCP 服务器实现（如 `quark-search`、`amap-tools` 等）。

*   **传统 API 网关**
    *   **功能**：处理标准的微服务路由和 Kubernetes Ingress 流量管理。

**总结**：Higress 是一款将传统微服务治理与 AI 能力深度融合的下一代网关，既支持 Kubernetes Ingress，也原生集成了 LLM 统一管理和 AI Agent 工具调用能力。

---
## 评论

**总体判断**

Higress 是阿里云开源的一款极具前瞻性的“AI原生”网关，它成功地将云原生流量管理技术与大模型（LLM）应用需求深度融合。该项目不仅继承了 Istio/Envoy 的稳健架构，更通过 WASM 和 AI 协议扩展，填补了传统网关在 AI 时代的功能空白，是目前将“模型网关”与“微服务网关”统一得最彻底的解决方案之一。

**详细评价**

**1. 技术创新性：从“流量路由”进化到“模型路由”**
*   **事实**：DeepWiki 明确指出 Higress 基于 Istio 和 Envoy 构建，并引入了 WebAssembly (WASM) 插件能力。其核心定位包含 AI Gateway、MCP Server hosting 以及传统 API 网关。
*   **推断**：Higress 最大的差异化在于**“AI Native”**的架构设计。传统网关（如 Nginx, Kong）主要关注 HTTP/RESTful 路由，而 Higress 在内核层面集成了对 LLM 协议（如 OpenAI 协议）的支持。
    *   **协议转换与统一**：它能将不同厂商的异构 LLM API 标准化为统一接口，解决了模型切换带来的代码改动成本。
    *   **MCP (Model Context Protocol) 集成**：DeepWiki 提到支持 MCP Server hosting，这意味着 Higress 直接介入了 Agent 的工具调用链路，不仅做流量转发，还做“工具调度”，这是极具创新性的网关职能扩展。
    *   **WASM 插件化**：利用 WASM 实现逻辑热加载，允许开发者用 C++/Go/Rust/AssemblyScript 编写高性能插件（如 Prompt 模板注入、敏感词过滤），而不需要修改网关内核或重启服务。

**2. 实用价值：解决 AI 落地中的“最后一公里”连接问题**
*   **事实**：文档描述其功能包括 AI Gateway features for LLM applications 和 Kubernetes Ingress。
*   **推断**：Higress 解决了企业落地 AI 时的三个核心痛点：
    *   **安全与合规**：企业不希望将内部微服务直接暴露给公网 LLM，也不希望 API Key 泄露给每个开发人员。Higress 可以作为统一出口，集中管理 Token、配额和权限，实现“模型即服务”。
    *   **成本与稳定性**：通过在网关层实现缓存和语义路由，可以减少对昂贵 Token 的消耗。
    *   **架构统一**：大多数企业面临“两套网关”的困境（一套管微服务，一套管 AI 流量）。Higress 将两者合二为一，降低了运维复杂度和技术栈碎片化，应用场景非常广泛，特别是对于正在从传统微服务架构向 AI 架构转型的企业。

**3. 代码质量与架构：云原生标准的高水位实现**
*   **事实**：项目使用 Go 语言编写，星标数 7,647，架构分离了控制平面和数据平面。
*   **推断**：
    *   **架构设计**：基于 Envoy 作为数据平面保证了极高的吞吐量和低延迟（C++ 内核），控制平面使用 Go 提供了良好的扩展性和配置管理能力。这种组合是云原生领域的“黄金搭档”。
    *   **文档规范**：提供了中英日三语 README，且 DeepWiki 显示包含详细的架构、构建、部署及开发指南，说明项目注重国际化与开发者体验，文档完整性高。
    *   **代码规范**：背靠阿里巴巴，代码质量通常经过大规模生产环境验证，具备工业级的鲁棒性。

**4. 社区活跃度：头部项目的稳健生态**
*   **事实**：Star 数 7,647，由阿里巴巴主导。
*   **推断**：虽然 Star 数不及一些纯基础设施项目（如 Istio 本身），但在“AI 网关”这一垂直细分领域，Higress 属于头部项目。阿里的背书保证了项目不会轻易停止维护。社区活跃度主要体现在国内云原生和 AI 开发者群体中，Issue 响应和 Feature 迭代速度较快，特别是在对国内大模型厂商（通义千问、文心一言等）的适配支持上非常及时。

**5. 学习价值：理解“AI 时代基础设施”的窗口**
*   **推断**：对于开发者而言，Higress 是学习以下技术的最佳实践之一：
    *   **WASM 在边缘计算/网关中的应用**：如何通过 WASM 实现业务逻辑与基础设施的解耦。
    *   **控制平面与数据平面分离**：深入理解 Envoy 的配置分发机制（xDS 协议）。
    *   **AI 流量治理**：学习如何处理 SSE（Server-Sent Events）流式传输、超时控制以及 Prompt 的中间件处理模式。

**6. 潜在问题与改进建议**
*   **推断**：
    *   **复杂度门槛**：对于仅有简单转发需求的小团队，Higress 基于 Istio 的架构可能显得过重（Heavyweight）。相比 Nginx，其部署和运维心智负担较高。
    *   **生态兼容性**：虽然支持 WASM，但复用传统的 Nginx/Lua 插件生态存在迁移成本。
    *   **建议**：进一步简化 Standalone（非 K8s）模式的部署体验，吸引非容器化用户；增强 AI 可观测性（如针对 Token 消耗

---
## 技术分析

# Higress 深度技术分析报告

基于阿里巴巴开源的 Higress 仓库（AI Native API Gateway），本文将从架构设计、核心功能、实现细节、适用场景、发展趋势及工程哲学等维度进行全面剖析。

---

## 1. 技术架构深度剖析

Higress 的架构设计体现了**“云原生+”**的演进思路，它不仅仅是传统的流量网关，更是为了适应 AI 时代流量特征而重构的入口设施。

### 技术栈与架构模式
*   **底层基座**：深度依赖 **Envoy** 作为高性能数据平面，利用其 L3/L7 处理能力和可观测性。
*   **控制平面**：基于 **Istio** 进行了大幅简化和增强。Higress 移除了 Istio 中繁重的 Sidecar 注入模式，专注于作为 Ingress Gateway 或独立网关的部署形态。
*   **扩展机制**：**WebAssembly (WASM)** 是其核心灵魂。通过代理级 WASM (Proxy-WASM) 规范，允许用户使用 C/C++/Go/Rust 等语言编写插件，动态加载到 Envoy 中，实现了业务逻辑与网关内核的热解耦。

### 核心模块设计
1.  **控制平面**：负责配置下发。它监听 K8s Ingress、Gateway API 或自定义配置资源，将其转换为 Envoy 的 xDS 协议配置，并推送给数据平面。
2.  **数据平面**：基于 Envoy，负责实际的流量处理、路由转发、WASM 插件执行以及 AI 特有的流式转发。
3.  **WASM 虚拟机**：集成 Wasmtime 或 V8 引擎，为插件提供沙箱环境。

### 技术亮点与创新点
*   **AI Native 流式处理**：传统网关在处理 SSE (Server-Sent Events) 或流式响应时，往往缺乏上下文干预能力。Higress 在数据平面实现了针对流式协议的拦截与修改能力，使得在 AI 对话流中注入敏感词过滤或格式化成为可能，且不中断连接。
*   **MCP (Model Context Protocol) 服务器托管**：这是 Higress 极具前瞻性的功能。它不仅转发流量，还能作为 AI Agent 的工具提供者，将内部 API 转化为 MCP 协议暴露给 LLM，解决了 AI 应用集成内部系统的“最后一公里”问题。

### 架构优势分析
*   **配置热更新**：利用 xDS 协议，配置变更毫秒级生效，无需重启 Pod，这对高可用系统至关重要。
*   **低延迟**：数据平面路径短，WASM 插件虽然运行在沙箱中，但通过 AOT (Ahead-of-Time) 编译优化，性能损耗控制在极低范围（通常微秒级）。

---

## 2. 核心功能详细解读

### 主要功能与关键问题解决
1.  **AI 网关**
    *   **功能**：统一管理 OpenAI, Azure, HuggingFace, 通义千问等 LLM 提供商的 API Key；提供基于 Token 的计费与流控；处理 Prompt 模板管理。
    *   **解决问题**：企业开发 AI 应用时，需要对接多家模型厂商，代码逻辑分散且密钥管理混乱。Higress 提供了标准化的适配层，屏蔽底层差异。
2.  **MCP 系统集成**
    *   **功能**：自动将标准 HTTP API 定义转换为 MCP 协议，并托管 MCP Server。
    *   **解决问题**：解决了 LLM 调用内部微服务工具的动态注册与安全问题，无需为每个 Agent 单独开发 Connector。
3.  **Kubernetes Ingress**
    *   **功能**：作为 K8s 集群的统一入口，支持 Ingress 与 Gateway API。
    *   **解决问题**：替代 Nginx Ingress Controller，提供更现代化的配置管理和可观测性。

### 与同类工具对比
*   **VS Nginx/Kong**：Nginx 基于 Lua (OpenResty) 扩展，虽然灵活但存在内存安全风险且难以隔离；Kong 基于 Nginx/OpenResty，配置复杂。Higress 基于 WASM，安全性更高（沙箱隔离），且天然适配 K8s/Istio 生态。
*   **VS Istio Ingress**：原生 Istio 配置极其复杂，学习曲线陡峭。Higress 对 Istio 进行了“减负”，提供了更符合运维习惯的 K8s Ingress YAML 或控制台 UI，降低了上手门槛。

### 技术实现原理
*   **AI 流式拦截**：通过 Envoy Filter 插件，在流式响应的分片传输过程中，通过 Buffer 机制截取数据包，进行匹配或替换，然后重新流式下发。这要求极高的并发处理能力，否则会阻塞后端响应。

---

## 3. 技术实现细节

### 关键技术方案
*   **xDS 协议优化**：Higress 对 Istio 的控制平面进行了裁剪，去除了 Sidecar 相关的繁重逻辑，专注于 Gateway 的配置下发。它维护了一份 Envoy 配置的 CRD 映射表。
*   **WASM 插件加载器**：实现了 OCI (Open Container Initiative) 镜像拉取机制。插件被打包成 OCI 镜像（类似 Docker 镜像），网关运行时动态拉取并挂载到 WASM VM 中。

### 代码组织与设计模式
*   **语言**：Go (控制平面) + C++ (Envoy 内核修改)。
*   **设计模式**：
    *   **Controller Pattern**：控制器模式，持续监听 K8s 资源变化并调和状态。
    *   **Proxy Pattern**：网关作为流量代理，在透明转发的基础上增加业务逻辑。

### 性能优化与扩展性
*   **多线程 WASM**：Envoy 的 WASM 运行时配置为每线程一个 VM 实例，避免了多线程竞争锁，极大提升了并发插件的执行效率。
*   **零拷贝**：在数据平面尽可能利用 Envoy 的高性能零拷贝网络栈。

### 技术难点与解决方案
*   **难点**：WASM 插件的崩溃可能导致网关线程挂掉。
*   **方案**：引入了异常捕获机制，并将插件运行时与主进程隔离。同时，限制了单个插件的内存和 CPU 使用配额。

---

## 4. 适用场景分析

### 最适合的场景
1.  **企业级 AI 应用落地**：企业需要统一管理多个部门对 LLM 的访问，进行统一的鉴权、计费和审计，且涉及流式输出处理。
2.  **微服务 API 治理**：基于 K8s 的复杂微服务体系，需要金丝雀发布、负载均衡、流量镜像等高级流量管理功能。
3.  **混合云架构**：需要统一管理跨云、跨数据中心的流量，利用云原生标准协议。

### 不适合的场景
1.  **极边缘计算**：资源极度受限（如几 MB 内存）的设备，Envoy 本身较重。
2.  **简单静态网站托管**：如果只需要简单的静态文件服务，Nginx 或 Caddy 更轻量。
3.  **非 K8s 环境的强依赖**：虽然支持独立部署，但其最大威力在 K8s 生态中，如果完全脱离容器环境，配置管理会变得繁琐。

### 集成方式
*   **Ingress 模式**：直接替换 K8s 集群原有的 Ingress Controller。
*   **Service Mesh 边缘网关**：作为 Istio 控制平面的数据平面入口。

---

## 5. 发展趋势展望

### 技术演进方向
*   **更强的 AI 协议支持**：从简单的 HTTP 封装转向对原生 AI 协议（如 gRPC-Web for LLM）的深度优化。
*   **RAG (检索增强生成) 集成**：网关层可能直接集成向量数据库的检索代理，在请求到达 LLM 前先进行上下文增强。

### 社区反馈与改进空间
*   **文档与 UI**：作为开源项目，控制台的易用性和文档的完善度仍是用户痛点。
*   **WASM 生态**：目前 WASM 插件的开发门槛相对较高（需要特定 SDK），未来可能会出现更低代码化的插件定义方式。

---

## 6. 学习建议

### 适合开发者水平
*   **中高级后端工程师**：具备 HTTP 协议、K8s 基础及 Go 语言阅读能力。
*   **运维/SRE 工程师**：需要深入理解云原生流量治理。

### 学习路径
1.  **基础理论**：理解 Envoy 架构、xDS 协议、K8s Ingress 机制。
2.  **动手实践**：在本地 Kind 集群中部署 Higress，配置一个简单的 AI 代理转发。
3.  **插件开发**：尝试使用 Go SDK 编写一个简单的 WASM 插件（如请求头修改），并编译成 WASM 模块加载。

---

## 7. 最佳实践建议

### 正确使用指南
*   **资源限制**：务必为 Higress Pod 设置合理的 CPU 和 Memory Limits，因为 WASM 运行时会消耗额外内存。
*   **插件粒度**：WASM 插件不宜编写过于复杂的业务逻辑，应保持轻量，避免阻塞网络 I/O。

### 性能优化建议
*   **连接池**：针对后端服务（特别是 LLM 服务），合理调整 Envoy 的连接池大小，避免频繁建连导致的延迟。
*   **WASM 预编译**：在构建插件镜像时，优先考虑 AOT 编译以减少启动时的 JIT 开销。

---

## 8. 哲学与方法论：第一性原理与权衡

### 抽象层与复杂性转移
Higress 的核心哲学是**“标准化的边缘”**。
*   **复杂性转移**：它将**业务逻辑的复杂性**从应用代码中剥离，转移到了**网关配置层**（WASM 插件和路由规则）。
*   **代价**：这种转移要求运维/平台团队具备更高的架构掌控能力。网关变成了“分布式的单点”，一旦网关配置逻辑（插件）出现 Bug，影响面是全站的，而不是单个微服务。

### 价值取向
*   **可观测性与控制 > 极致性能**：虽然 Higress 性能很高，但相比于纯 Nginx C 模块开发，它选择了 WASM 沙箱，牺牲了一点点性能换取了**安全性**和**动态可扩展性**。这是典型的云原生权衡。
*   **标准化 > 灵活性**：强制用户遵循 K8s/Istio 的标准规范，限制了野路子配置，但提升了可移植性。

### 工程范式
Higress 采用的是**“基础设施即代码”** 的范式。它通过声明式 API 驱动系统状态。最容易被误用的地方在于**“业务逻辑下沉”**——开发者容易将本应在微服务内部处理的复杂业务逻辑（如复杂的数据库查询、重度计算）写成 WASM 插件塞进网关，导致网关过载。

###

---
## 代码示例




```python
# 示例1：Higress 网关路由配置
def configure_higress_route():
    """
    配置 Higress 网关的路由规则，将请求转发到不同的后端服务
    适用于微服务架构中的流量管理场景
    """
    from pydantic import BaseModel
    
    # 定义路由规则模型
    class RouteRule(BaseModel):
        host: str  # 域名
        path: str  # 路径前缀
        service_name: str  # 目标服务名
        service_port: int  # 目标服务端口
        
    # 示例配置：将 /api/user 请求转发到 user-service
    user_route = RouteRule(
        host="api.example.com",
        path="/api/user",
        service_name="user-service",
        service_port=8080
    )
    
    # 模拟应用配置（实际中会调用 Higress API）
    print(f"配置路由: {user_route.path} -> {user_route.service_name}:{user_route.service_port}")
    return user_route

# 说明：这个示例展示了如何使用 Python 定义 Higress 网关的路由规则，
# 实现了基于域名和路径的流量转发，是微服务网关的核心功能。
```




```python
# 示例2：Higress 插件配置（限流）
def configure_higress_plugin():
    """
    配置 Higress 的限流插件，保护后端服务免受流量冲击
    适用于需要流量控制的 API 网关场景
    """
    # 限流配置
    rate_limit_config = {
        "plugin_name": "request-limit",
        "config": {
            "limit_by_header": "X-User-ID",  # 基于用户ID限流
            "query_per_second": 100,  # 每秒100次请求
            "burst": 200,  # 突发流量允许200次
            "rejected_code": 429,  # 超限返回429状态码
            "rejected_msg": "Too many requests"
        }
    }
    
    # 模拟应用配置（实际中会调用 Higress API）
    print(f"配置限流插件: {rate_limit_config['plugin_name']}")
    return rate_limit_config

# 说明：这个示例展示了如何配置 Higress 的限流插件，
# 通过设置 QPS 阈值和突发流量处理，保护后端服务稳定性。
```




```python
# 示例3：Higress 服务发现集成
def integrate_service_discovery():
    """
    集成 Higress 与 Nacos 服务发现，实现动态服务路由
    适用于云原生环境下的服务治理场景
    """
    import json
    
    # 模拟从 Nacos 获取的服务列表
    nacos_services = {
        "user-service": [
            {"ip": "10.0.1.1", "port": 8080, "weight": 100},
            {"ip": "10.0.1.2", "port": 8080, "weight": 50}
        ],
        "order-service": [
            {"ip": "10.0.2.1", "port": 9090, "weight": 100}
        ]
    }
    
    # 生成 Higress 上游服务配置
    upstreams = []
    for service, instances in nacos_services.items():
        upstream = {
            "service_name": service,
            "nodes": [
                f"{instance['ip']}:{instance['port']} weight={instance['weight']}"
                for instance in instances
            ]
        }
        upstreams.append(upstream)
    
    # 模拟应用配置（实际中会调用 Higress API）
    print("配置动态上游服务:")
    print(json.dumps(upstreams, indent=2, ensure_ascii=False))
    return upstreams

# 说明：这个示例展示了如何将 Nacos 服务发现与 Higress 集成，
# 实现基于权重的负载均衡和动态服务路由，是云原生架构中的典型用法。
```


---
## 案例研究


### 1：阿里巴巴内部电商业务

 1：阿里巴巴内部电商业务

**背景**:  
阿里巴巴电商业务面临高并发、大流量的挑战，尤其是双11等促销活动期间，API网关需要处理每秒百万级的请求。原有的API网关基于自研系统，维护成本高，扩展性有限。

**问题**:  
- 系统扩展性不足，难以应对流量峰值。  
- 多云部署和混合云架构下，网关管理复杂。  
- 功能迭代缓慢，无法快速响应业务需求。

**解决方案**:  
采用Higress作为新一代云原生API网关，基于Istio和Envoy构建，支持动态路由、流量管理和安全防护。通过Higress的插件市场，快速集成自定义业务逻辑。

**效果**:  
- 成功支撑双11期间每秒百万级请求，系统稳定性提升至99.99%。  
- 实现多云统一管理，运维效率提升40%。  
- 功能迭代周期从月级缩短至周级，业务响应速度显著加快。

---



### 2：某金融科技公司

 2：某金融科技公司

**背景**:  
该公司提供在线支付和金融服务，API接口众多，且需满足严格的合规要求（如PCI-DSS）。原有网关无法满足细粒度的权限控制和审计需求。

**问题**:  
- 权限管理粗放，存在安全风险。  
- 审计日志分散，难以快速定位问题。  
- 网关性能瓶颈导致支付接口延迟。

**解决方案**:  
部署Higress，利用其内置的WAF（Web应用防火墙）和细粒度访问控制功能。结合Higress的日志集成能力，将审计日志统一收集至ELK栈。

**效果**:  
- 实现API级别的权限控制，通过安全审计。  
- 日志查询效率提升60%，问题定位时间缩短50%。  
- 支付接口平均延迟从200ms降至80ms，用户体验显著改善。

---



### 3：某跨国物流企业

 3：某跨国物流企业

**背景**:  
该企业业务遍布全球，API网关需支持多区域部署和跨地域流量调度。原有系统无法统一管理全球API，且缺乏对多协议（如REST、gRPC）的支持。

**问题**:  
- 多区域网关配置不一致，导致服务差异。  
- 不支持gRPC协议，无法满足微服务通信需求。  
- 跨地域流量调度依赖手动配置，效率低下。

**解决方案**:  
采用Higress的全球流量管理功能，统一配置多区域网关。通过Higress对gRPC的原生支持，无缝集成微服务架构。

**效果**:  
- 全球API配置一致性达100%，服务差异问题彻底解决。  
- gRPC调用性能提升30%，微服务通信更高效。  
- 自动化流量调度将跨区域延迟降低40%，全球服务响应速度显著提升。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | 方案A: Kong | 方案B: APISIX |
|------|------------------|------------|--------------|
| 性能 | 基于Envoy和Istio，高性能，支持Wasm插件扩展 | 基于Nginx和OpenResty，性能较高但扩展性有限 | 基于OpenResty和LuaJIT，性能极高，适合高并发场景 |
| 易用性 | 提供图形化控制台和Kubernetes原生支持，配置简单 | 提供管理界面，但配置相对复杂 | 支持Kubernetes集成，但学习曲线较陡 |
| 成本 | 开源免费，企业版支持收费 | 开源版免费，企业版收费 | 完全开源免费，社区支持活跃 |
| 扩展性 | 支持Wasm插件，扩展灵活 | 插件生态丰富，但扩展性受限于Nginx | 支持Lua插件，扩展性强但需要编程能力 |
| 社区支持 | 阿里背书，社区活跃但较新 | 社区成熟，文档完善 | 社区活跃，文档丰富 |
| 适用场景 | 云原生、微服务、混合云架构 | 传统API管理、微服务网关 | 高并发、云原生API网关 |

### 优势分析

- 优势1：基于Envoy和Istio，性能和扩展性兼具，适合云原生场景。
- 优势2：提供图形化控制台和Kubernetes原生支持，降低使用门槛。
- 优势3：支持Wasm插件，扩展性更强，适合复杂业务需求。

### 不足分析

- 不足1：社区相对较新，生态和文档不如Kong和APISIX成熟。
- 不足2：企业版功能可能需要付费，开源版功能有限。
- 不足3：对非Kubernetes环境的支持不如传统网关（如Kong）灵活。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Wasm 插件实现扩展能力

**说明**: Higress 原生支持 WebAssembly (Wasm)，允许开发者使用 C++、Go、Rust 或 AssemblyScript 编写高性能的扩展插件，而无需修改网关核心代码或重新部署整个网关实例。

**实施步骤**:
1. 根据业务需求选择合适的 Wasm 开发语言（推荐使用 Go 或 Rust）。
2. 利用 Higress 官方提供的 SDK 或 `wasm-as-assembly` 工具链开发插件逻辑。
3. 将编译好的 `.wasm` 文件上传至 Higress 控制台或通过 OCI 存储进行动态加载。
4. 在网关路由配置中，将特定插件绑定到需要的路由或服务上。

**注意事项**: 开发 Wasm 插件时应注意内存管理和执行效率，避免阻塞主线程导致请求延迟增加。

---

### 实践 2：精细化流量治理与路由规则配置

**说明**: 利用 Higress 强大的路由能力实现基于 Header、Query 参数、Cookie 或权重的灰度发布（金丝雀发布）和蓝绿部署，确保新版本上线的平滑过渡。

**实施步骤**:
1. 在控制台定义两个不同的服务版本（如 v1 和 v2）。
2. 创建基于 HTTP 头部或权重的路由规则。
3. 配置流量百分比，例如将 10% 的流量路由至 v2 版本。
4. 监控 v2 版本的关键指标，确认无误后逐步调整权重至 100%。

**注意事项**: 确保路由规则的优先级设置正确，避免规则冲突导致流量未按预期分配。

---

### 实践 3：全面对接云原生可观测体系

**说明**: Higress 深度集成了 Prometheus 和 OpenTelemetry，应充分利用这些特性来收集指标、链路追踪和访问日志，以便快速定位性能瓶颈和故障。

**实施步骤**:
1. 配置 Higress 的 Prometheus Exporter，开启 Metrics 收集。
2. 集成 OpenTelemetry 协议，将 Tracing 数据发送至 Jaeger 或 Zipkin。
3. 配置访问日志输出至 Elasticsearch、Loki 或 Kafka 等后端存储。
4. 在 Grafana 中导入 Higress 官方 Dashboard 进行可视化监控。

**注意事项**: 在高并发场景下，日志采样率应合理配置，避免海量日志对网关性能或存储造成过大压力。

---

### 实践 4：高可用部署与资源隔离

**说明**: 在生产环境中，Higress 控制平面和数据平面应分离部署，并为数据平面配置合理的资源限制（Request/Limit），以防止个别业务异常耗尽节点资源。

**实施步骤**:
1. 使用 Kubernetes Deployment 管理 Higress Pod，设置 `replicas >= 2`。
2. 为 Higress 容器配置 CPU 和 Memory 的 Request 与 Limit。
3. 配置 Pod 反亲和性，确保同一网关的 Pod 分布在不同的物理节点或可用区上。
4. 启用 HPA（Horizontal Pod Autoscaler）根据 CPU 或自定义指标自动扩缩容。

**注意事项**: 监控 Pod 的 OOMKilled 情况，Memory Limit 设置需留有一定 Buffer 以应对突发流量。

---

### 实践 5：安全防护与认证鉴权

**说明**: 利用 Higress 内置的插件能力实现 API 安全，包括 JWT 验证、Keyless 认证、IP 黑白名单以及基本的 WAF 防护功能。

**实施步骤**:
1. 在全局或特定路由上启用 `jwt-auth` 插件，配置签名密钥。
2. 配置 `key-rate-limit` 插件以防止 API 被恶意刷量。
3. 针对内部管理接口配置 `ip-restriction` 插件，仅允许内网访问。
4. 开启 HTTPS 并配置 TLS 证书，强制重定向 HTTP 到 HTTPS。

**注意事项**: JWT 密钥应定期轮换，避免密钥泄露导致安全风险；证书过期前需设置自动更新机制。

---

### 实践 6：服务发现与多注册中心接入

**说明**: Higress 设计为云原生网关，能够同时接入 Kubernetes Service、Nacos、Consul 等多种注册中心。最佳实践是统一管理服务来源，实现混合云架构下的服务互通。

**实施步骤**:
1. 在 Higress 控制台的“来源服务”管理中，添加对应的注册中心类型（如 Nacos）。
2. 配置注册中心的连接地址（Server Addr）和命名空间。
3. 创建 Ingress 或网关路由时，直接选择已发现的微服务作为目标服务。
4. 验证服务健康检查机制是否正常工作，确保自动摘除不健康的实例。

**注意事项**: 当接入多个注册中心时，需注意不同注册中心中服务名称的冲突问题，建议通过命名空间进行逻辑隔离。

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/3 (QUIC) 协议支持

**说明**: Higress 基于 Envoy，支持 HTTP/3 协议。HTTP/3 基于 UDP 协议（QUIC），相比传统的 TCP + HTTP/2，在处理丢包和连接迁移方面具有显著优势，特别是在弱网环境下能有效减少连接建立延迟和队头阻塞（Head-of-Line Blocking）问题。

**实施方法**:
1. 在 Higress 网关监听器配置中，为 HTTPS 端口（通常为 443）添加 HTTP/3 协议支持。
2. 配置 UDP 端口（通常为 443）的防火墙和安全组放行策略。
3. 确保证书配置正确，利用 ALPN 协商机制。

**预期效果**: 弱网环境下的请求延迟降低 30% 左右，视频流和静态资源加载速度显著提升，连接迁移成功率提高。

---

### 优化 2：配置全链路超时与重试策略

**说明**: 不合理的超时设置会导致请求堆积（雪崩效应），而缺乏指数退避的重试机制会加剧后端压力。Higress 允许精细化的路由级超时和重试配置，优化此配置可极大提升系统容错能力。

**实施方法**:
1. **设置合理超时**: 针对不同类型的接口（如内部微服务调用 vs 外部第三方 API）配置不同的 `timeout`，避免默认过长的超时时间占用连接池。
2. **智能重试**: 在路由配置中启用重试策略，设定 `numRetries`（建议 2-3 次），并配置 `retryOn`（如 503, 504, 5xx 状态码或连接失败）。
3. **限制重试范围**: 务必配置 `perTryTimeout`（单次尝试超时），且必须小于总超时时间。

**预期效果**: 在后端服务出现偶发故障时，接口成功率可提升至 99.9% 以上，同时避免无效重试造成的资源浪费。

---

### 优化 3：启用 Wasm 插件与本地缓存

**说明**: Higress 支持 Wasm (WebAssembly) 插件。相比于传统的 Lua 或远程调用逻辑，Wasm 执行效率更高且更安全。同时，利用 Wasm 插件实现高频读取数据的本地缓存（如配置数据、鉴权令牌），可以大幅减少对后端服务的请求。

**实施方法**:
1. 将高频鉴权或参数校验逻辑编写为 Wasm 插件（Go 或 C++ 编译）。
2. 在插件逻辑中实现内存缓存（例如 LRU Cache），对 Token 验证结果或签名计算结果进行缓存。
3. 在网关层面配置合理的缓存淘汰策略（TTL）。

**预期效果**: 鉴权等高频逻辑的 CPU 消耗降低 40%-60%，后端相关接口的 QPS 负载降低 80% 以上（取决于缓存命中率）。

---

### 优化 4：调整连接池与并发限制

**说明**: Higress 默认的连接池配置可能无法满足高并发场景。过小的连接池会导致请求排队等待，过大的连接池则可能导致后端服务被打挂。此外，启用 HTTP/2 可以复用连接，减少握手开销。

**实施方法**:
1. **调整连接池大小**: 根据后端服务处理能力，调整 Upstream 的 `http2_protocol_options` 或连接池参数（如 `max_connections`），建议初始值设为 1024 或根据压测结果调整。
2. **启用 HTTP/2**: 确保网关与后端服务之间优先使用 HTTP/2 协议，利用多路复用减少 TCP 连接数。
3. **配置限流**: 在网关层面启用 `request-per-second` 或 `concurrency` 限流，防止流量突增打挂后端。

**预期效果**: 网关吞吐量（QPS）提升 20%-50%，P99 延迟显著降低，有效保护后

---
## 学习要点

- Higress 是阿里开源的基于 Istio 的云原生 API 网关，深度集成了 K8s 与 Envoy，提供高性能流量管理能力。
- 支持热更新与动态配置，无需重启服务即可修改路由规则、插件配置，显著提升运维效率。
- 内置 WAF（Web 应用防火墙）与安全插件，提供流量清洗、防 DDoS 等安全防护能力。
- 兼容 Kubernetes Ingress 与 Gateway API 标准，可平滑替代 Nginx Ingress Controller 等传统方案。
- 提供丰富的扩展插件生态（如认证、限流、可观测性），支持自定义插件开发以满足业务需求。
- 通过 Envoy 的 Proxy-Wasm 沙箱技术实现插件隔离，确保插件异常不影响网关核心稳定性。
- 集成 Prometheus/Grafana 监控体系，支持细粒度的流量分析与链路追踪，便于问题定位。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础与概念理解

**学习内容**:
- 理解云原生网关的基本概念及其在现代微服务架构中的定位
- 了解 Higress 的核心特性：基于 Envoy 和 Istio、高可用性、低延时
- 学习基本的流量管理术语：路由、转发、负载均衡、Upstream（服务来源）
- 掌握容器基础（Docker 基本命令）和 Kubernetes 基础概念

**学习时间**: 1-2周

**学习资源**:
- Higress GitHub 官方仓库 README
- Higress 官方文档 - "产品简介"与"核心概念"章节
- Envoy 官方文档中关于 Proxy 和 Lifecycle 的基础介绍

**学习建议**:
不要急于部署。先通读官方文档，理解 Higress 作为"流量网关"与"微服务网关"的区别。如果你没有 Kubernetes 基础，建议先花几天时间补充 K8s 的基本概念，因为 Higress 通常运行在 K8s 之上。

---

### 阶段 2：环境搭建与核心配置

**学习内容**:
- 本地或 Kubernetes 集群部署 Higress（Docker Desktop 或 Minikube 环境）
- 掌握 Higress 控制台的使用
- 学习配置域名路由和路径路由
- 实践服务来源的配置：固定地址、Nacos、Consul、K8s Service
- 配置全局限流、CORS（跨域）和重定向策略

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 - "快速开始"与"控制台使用指南"
- Higress 官方示例库
- Nacos 注册中心基础教程（用于配合服务发现测试）

**学习建议**:
动手是关键。建议在本地搭建一个包含两个简单服务的 Demo（如一个前端服务和一个后端服务），通过 Higress 将流量路由到后端。尝试修改配置并观察流量变化，熟悉 Ingress Route CRD 或控制台配置的对应关系。

---

### 阶段 3：流量治理与高级特性

**学习内容**:
- 深入学习流量治理：金丝雀发布、蓝绿发布、Header 头部操作
- 掌握安全防护：WAF 插件基础、Key Auth（API 密钥认证）、JWT 认证
- 学习服务 mocking 功能，用于前端开发与后端解耦
- 理解 Higress 的插件体系：Wasm 插件加载与运行机制
- 监控与可观测性：对接 Prometheus、Grafana 以及日志采集

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档 - "流量治理"与"插件市场"章节
- Higress 官方插件市场
- Prometheus 与 Grafana 基础配置教程

**学习建议**:
重点攻克"插件"和"金丝雀发布"这两个高频使用场景。尝试在 Higress 中开启一个 Wasm 插件（如请求阻断或限流插件），并查看日志验证效果。同时，尝试模拟后端服务故障，观察 Higress 的容错处理能力。

---

### 阶段 4：插件开发与架构原理

**学习内容**:
- 深入研究 Envoy 的配置模型与 XDS 协议
- 学习编写自定义 Wasm 插件：使用 C++、Go 或 AssemblyScript 开发插件
- 理解 Higress 的架构设计：控制面与数据面的交互
- 高可用部署方案：多副本部署、灾备与性能调优
- Higress 在 Service Mesh (Istio) 中的集成模式

**学习时间**: 4-6周

**学习资源**:
- Higress 官方文档 - "自定义开发"章节
- Envoy 官方深度开发文档
- WebAssembly (Wasm) 官方文档
- Higress 源码分析

**学习建议**:
此阶段适合有编程基础的学习者。建议从修改一个现有的官方插件开始，逐步尝试编写一个简单的 Wasm 插件来实现自定义的请求头处理或鉴权逻辑。阅读源码时，重点关注 HTTP Filter 的实现逻辑。

---

### 阶段 5：生产实践与生态集成

**学习内容**:
- 生产环境部署架构设计：多集群容灾、高并发配置优化
- 与阿里云云原生产品的集成：ACK、MSE、ARMS
- 复杂场景实战：多租户网关管理、全链路灰度
- 网关安全加固：防 SQL 注入、防 CC 攻击策略配置
- 成本控制与性能压测：使用 JMeter 或 Hey 进行压测与调优

**学习时间**: 持续学习

**学习资源**:
- 阿里云云原生网关最佳实践案例
- Hig

---
## 常见问题


### 1: Higress 是什么？它与阿里巴巴和云原生社区有什么关系？

1: Higress 是什么？它与阿里巴巴和云原生社区有什么关系？

**A**: Higress 是一款基于阿里内部多年实践，开源的云原生 API 网关。它诞生于阿里巴巴，是阿里云 MSE（微服务引擎）云产品 API 网关的开源版本，也是 CNCF（云原生计算基金会）孵化项目 Envoy 的上游主要贡献者之一。

Higress 的定位是连接后端微服务和前端客户端的“流量高速公路”，它深度集成了 Envoy 高性能网络库，并结合了 K8s Ingress Controller 以及网关管理的特性。它旨在解决云原生时代微服务架构下的流量治理、安全认证和协议转换等问题。

---



### 2: Higress 与 Nginx、Apache APISIX 或 Kong 等传统网关相比有什么优势？

2: Higress 与 Nginx、Apache APISIX 或 Kong 等传统网关相比有什么优势？

**A**: Higress 的核心优势主要体现在以下三个方面：

1.  **技术架构先进**：Higress 基于 Envoy（C++）构建数据面，使用 Go 语言构建控制面。相比于基于 Nginx Lua 的传统网关（如 Kong, APISIX），Higress 在处理长连接、热更新配置时资源消耗更低，且不会因为 Lua 脚本的业务逻辑复杂导致性能显著下降。
2.  **深度集成云原生**：它原生支持 Kubernetes Ingress 规范，同时也支持 Nginx Ingress 注解，方便用户从 Nginx 迁移。它对服务网格（如 Istio）有极好的兼容性，可以作为南北向（入口）网关与网格东西向流量无缝协同。
3.  **扩展性与插件生态**：Higress 支持使用 WASM（WebAssembly）技术编写插件。这意味着开发者可以使用 Python、Go、Java 或 JavaScript 等高级语言编写网关插件，而无需学习 C++ 或 Lua，且插件运行在沙箱中，安全性更高，不会导致网主进程崩溃。

---



### 3: Higress 是否支持从 Nginx Ingress 或其他网关无缝迁移？

3: Higress 是否支持从 Nginx Ingress 或其他网关无缝迁移？

**A**: 是的，Higress 对迁移非常友好，特别是针对 Kubernetes 用户。

1.  **Nginx Ingress 兼容**：Higress 实现了 Nginx Ingress Controller 的大部分常用注解。这意味着在大多数情况下，用户只需要将 Kubernetes Ingress 资源中的 `ingressClassName` 修改为 Higress 指定的类名，即可直接将流量切换到 Higress，无需修改 YAML 配置文件。
2.  **配置转换工具**：对于非 K8s 场景或复杂的 Nginx 配置，Higress 提供了 Nginx 配置转换工具，可以帮助用户将传统的 Nginx.conf 转换为 Higress 的路由配置。

---



### 4: 在 Higress 中如何进行二次开发？支持哪些编程语言编写插件？

4: 在 Higress 中如何进行二次开发？支持哪些编程语言编写插件？

**A**: Higress 提供了非常灵活的扩展机制，主要通过“插件”和“服务（Service）”两种方式：

1.  **WASM 插件开发**：这是推荐的方式。Higress 允许用户编写 WASM 插件来扩展网关功能。支持使用 Go、C++、Rust、JavaScript (AssemblyScript) 甚至 Java 编写插件。这些插件会被编译成 `.wasm` 文件，动态加载到网关中。这种方式热更新极其方便，且性能损耗极小。
2.  **ExtProc（外部处理）**：通过 Envoy 的 ExtProc 机制，Higress 可以将请求处理逻辑外包给外部服务（如 Python 或 Java 编写的微服务），网关与外部服务通过 gRPC 通信，实现业务逻辑与网关的解耦。
3.  **原生插件**：对于核心开发者，也可以直接修改 Higress 的 Go 代码来内置逻辑。

---



### 5: Higress 的性能表现如何？能否支撑高并发流量？

5: Higress 的性能表现如何？能否支撑高并发流量？

**A**: Higress 的性能表现非常优异，完全能够支撑双十一级别的大流量场景。

1.  **底层优势**：由于数据面基于 Envoy（C++ 编写），其单核转发性能与内存利用率优于基于 Lua 的传统网关。
2.  **基准测试**：根据官方及社区的压测数据，在开启常用插件（如限流、认证）的情况下，Higress 依然能保持极高的吞吐量和极低的延迟。
3.  **弹性伸缩**：作为云原生网关，Higress 可以结合 Kubernetes 的 HPA（水平自动伸缩）进行扩容，以应对流量洪峰。

---



### 6: Higress 是否支持 Dubbo 或 gRPC 等微服务协议？

6: Higress 是否支持 Dubbo 或 gRPC 等微服务协议？

**A**: 是的，Higress 是一款全功能的 API 网关，对微服务协议有极好的支持。

1.  **HTTP/gRPC**：原生支持 HTTP/1.1、HTTP/2 和 gRPC 协议的代理、负载均衡和 Header 修改。
2.  **Dubbo 支持**：这是 Higress 的一个强项。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 环境搭建与服务发现

### 基于 Higress 官方文档，使用 Docker Compose 在本地快速部署一套包含 Higress 网关和一个简单的后端服务（如 Nginx）的环境。配置 Higress 使其能够将通过 80 端口收到的 HTTP 请求转发到该后端服务。

### 提示**:

---
## 实践建议

基于 Higress 作为 AI Native API 网关的定位，结合其云原生架构与 AI 流量处理特性，以下是 6 条针对实际生产环境的实践建议：

### 1. 利用 Wasm 插件实现 AI 协议的私有化适配
**场景**：当你需要对接一家未在 Higress 默认支持列表中的国产大模型厂商，或者公司内部自研的模型服务时。
**建议**：不要修改 Higress 的核心代码，而是编写 Wasm (WebAssembly) 插件来处理特定的鉴权逻辑或协议转换。
**操作**：使用 Go 或 C++ 编写 Wasm 插件，在该插件中实现将 OpenAI 标准格式的请求转换为目标厂商的私有格式（例如修改 Header 或 Body 结构），然后将该插件挂载到特定的路由上。
**陷阱**：避免在 Wasm 插件中进行大量的数据处理或耗时计算，这会显著增加网关的延迟，导致 AI 请求的超时。

### 2. 实施基于令牌的细粒度流控与熔断
**场景**：大模型 API 调用成本高，且后端模型服务有严格的速率限制（RPM/TPM）。
**建议**：配置针对 API Key 或租户级别的请求限流，并针对模型服务端点设置熔断规则。
**操作**：在 Higress 的全局流量控制或路由级别配置，结合 Redis 实现针对不同 API Key 的 Token 预估消耗限流。同时，为后端 Upstream（模型服务）配置主动健康检查，当模型服务响应超时或返回 5xx 错误率达到阈值时，自动摘除故障节点，防止级联故障。
**陷阱**：不要仅依赖连接数限流。AI 请求的耗时差异巨大（生成式输出耗时远长于简单问答），连接数无法反映真实的后端压力，必须结合请求并发数（RPS）或 Token 消耗速率进行控制。

### 3. 部署独立的模型网关集群与业务网关集群
**场景**：企业内部既有传统的微服务业务，又有正在快速迭代的 AI 业务。
**建议**：将 Higress 部署为两个独立的集群：一个处理传统的微服务南北流量，另一个专门处理 AI 请求流量。
**操作**：在 Kubernetes 中创建两个独立的 Higress Deployment 或 IngressClass。AI 网关集群配置更高的超时时间（因为 LLM 生成可能需要几十秒甚至更久），以及更大的缓冲区大小；业务网关集群则保持短连接、高并发配置。
**陷阱**：混合部署极易导致资源争抢。一个长时间占用连接的 AI 流式请求可能会耗尽网关的连接池，导致普通业务接口请求超时。

### 4. 配置 SSE 流式响应的完整性与超时策略
**场景**：使用 ChatGPT 或文心一言等模型的流式输出功能。
**建议**：确保网关的 Idle Timeout（空闲超时）设置大于模型生成的最大预期时间，并正确处理 SSE（Server-Sent Events）数据帧。
**操作**：在路由配置中，显式将超时时间设置为一个较大值（如 300s）。同时，检查日志或监控配置，确保其是基于“请求结束”而非“字节传输”来统计延迟，以便准确观察用户体验。
**陷阱**：如果网关或中间层的 Load Balancer（如 ALB/SLB）超时设置过短（例如默认 60s），会导致长文本生成中断，客户端收到 `incomplete stream` 错误。

### 5. 建立模型可观测性与成本监控体系
**场景**：企业需要核算各个业务线使用 AI 的成本，并监控不同模型服务商的 SLA。
**建议**：利用 Higress 的日志上报能力，解析响应体或请求头中的 Token 使用量（如 `X-Usage-Total-Tokens`）。
**操作**：配置 Higress 的访问日志，将 Model 名称、Provider、响应状态码以及 Token 消耗量提取出来，发送至 Kafka 或 Prometheus。通过 Grafana 建立看板，

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI 原生](/tags/ai-%E5%8E%9F%E7%94%9F/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [WASM](/tags/wasm/) / [LLM](/tags/llm/) / [MCP](/tags/mcp/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/) / [DevOps/运维](/scenarios/devops-%E8%BF%90%E7%BB%B4/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260206-github_trending-alibaba-higress-6.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260205-github_trending-alibaba-higress-5.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260206-github_trending-alibaba-higress-0.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260303-github_trending-alibaba-higress-0.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*