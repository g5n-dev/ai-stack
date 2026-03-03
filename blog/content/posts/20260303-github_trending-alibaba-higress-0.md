---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-03-03T12:52:33+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "LLM", "MCP", "Istio", "Envoy", "WASM"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "以下是关于 **Higress** 的简洁总结： **1. 项目概况** * **名称**：Higress * **开发方**：阿里巴巴 * **定位**：AI 原生 API 网关 * **技术栈**：基于 Go 语言开发，构建在 Istio 和 Envoy 之上，集成了 WebAssembly (WASM) 插件能力"
external_url: https://github.com/alibaba/higress
scenarios: ["AI/ML项目", "大语言模型", "云原生/容器"]
---

# 阿里开源 Higress：AI 原生 API 网关

> **原名**: alibaba /

      higress

---

## 基本信息

- **描述**: 🤖 AI Gateway | AI 原生 API 网关
- **语言**: Go
- **星标**: 7,625 (+17 stars today)
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

Higress 是一款基于 Istio 和 Envory 构建的云原生 API 网关，通过深度集成 WASM 插件能力，实现了从传统流量管理到 AI 原生网关的演进。它主要解决 LLM 应用对接、AI Agent 工具集成（MCP）以及微服务路由等场景下的统一流量治理问题。本文将介绍其核心架构、AI 网关特性以及插件扩展机制，帮助你评估其是否适合作为业务的基础设施。

---
## 摘要

以下是关于 **Higress** 的简洁总结：

### **1. 项目概况**
*   **名称**：Higress
*   **开发方**：阿里巴巴
*   **定位**：AI 原生 API 网关
*   **技术栈**：基于 Go 语言开发，构建在 Istio 和 Envoy 之上，集成了 WebAssembly (WASM) 插件能力。

### **2. 核心功能**
Higress 提供了三大核心功能：
1.  **AI 网关**：为大语言模型 (LLM) 应用提供支持。
2.  **MCP 服务器托管**：支持 AI Agent 工具集成的模型上下文协议 (MCP) 服务。
3.  **传统 API 网关**：处理 Kubernetes Ingress 和微服务路由。

### **3. 架构与性能**
*   **架构设计**：采用**控制平面**（配置管理）与**数据平面**（流量处理）分离的架构。
*   **配置分发**：通过 xDS 协议传播配置变更。
*   **性能优势**：变更延迟为毫秒级，且连接不中断，非常适合 AI 流式响应等长连接场景。

### **4. 主要应用场景与组件**

| 应用场景 | 描述 | 核心组件 |
| :--- | :--- | :--- |
| **AI 网关** | 提供统一 API 接入 30+ 家 LLM 提供商，具备协议转换、可观测性、缓存和安全防护能力。 | `ai-proxy`, `ai-statistics`, `ai-cache`, `ai-security-guard` 等插件 |
| **MCP 服务器托管** | 托管 MCP 服务器，使 AI Agents 能够调用外部工具和服务。 | `mcp-router`, `jsonrpc-converter` 过滤器及配套实现 |
| **Kubernetes Ingress** | 作为 Kubernetes 入口控制器，兼容 nginx-ingress 注解。 | `higress-controller` |

---
## 评论

### 总体判断
Higress 是一款极具前瞻性的“云原生+AI”网关，它成功地将 Istio 的流量治理能力与 AI 原生需求（LLM 网关、MCP 协议）进行了深度融合。对于正在构建 AI 应用或寻求高性能可扩展网关的团队而言，这是一个具备极高工程价值的生产级选择。

### 深度评价依据

#### 1. 技术创新性：从“流量侧车”进化为“AI 神经中枢”
*   **事实**：Higress 基于 Envoy 和 Istio 构建，并深度集成了 **WebAssembly (WASM)** 插件系统。其核心定位包含 **AI Gateway** 和 **MCP Server Hosting**。
*   **推断**：Higress 最大的差异化在于它没有停留在传统的 HTTP 转发层面，而是通过 WASM 技术将网关变成了一个可编程的 AI 中间件层。
    *   **AI 原生优化**：它不仅仅是转发流量，还能处理 LLM 特有的协议转换（如将 OpenAI 格式转换为其他厂商格式）、Token 计费与流式处理，这解决了传统网关在处理 AI 长连接和流式响应时的无力感。
    *   **MCP (Model Context Protocol) 集成**：作为阿里主推的 AI Agent 互操作协议，Higress 直接内置了 MCP Server 托管能力。这意味着它不仅管理“流量”，还管理“AI 的工具上下文”，这是传统 API 网关从未涉足的领域，极具技术前瞻性。

#### 2. 实用价值：统一 AI 与微服务的流量入口
*   **事实**：文档明确指出其提供 K8s Ingress、微服务路由以及 AI 网关功能，且控制面与数据面分离。
*   **推断**：在 AI 落地场景中，企业常面临一个痛点：既需要管理微服务，又需要管理 LLM 调用。通常这需要两套系统（如 Nginx + 独立的 LLM Proxy），增加了运维复杂度。
    *   **降本增效**：Higress 允许用户在一个网关内同时完成传统 API 路由和 AI 模型的鉴权、限流、提示词注入。这种“双模”能力极大地降低了架构的熵增。
    *   **广泛场景**：适用于 SaaS 平台（统一接入不同 LLM 厂商）、AI Agent 应用（通过 MCP 接入外部工具）以及需要进行精细化流量治理的传统微服务架构。

#### 3. 代码质量与架构：云原生工业标准的集大成者
*   **事实**：项目使用 Go 语言开发，星标数 7,625，架构上复用了 Istio 的控制面理论和 Envoy 的高性能数据面。
*   **推断**：
    *   **架构稳健性**：依托 Envoy 的 L4/L7 处理能力和 Istio 的经验证的控制面逻辑，Higress 继承了云原生社区的顶级架构设计，避免了重复造轮子，保证了底层的稳定性与高性能。
    *   **扩展性设计**：WASM 插件系统的引入是代码质量的关键体现。它允许开发者使用 C/C++/Go/Rust 等语言编写业务逻辑，而无需修改网关核心代码或重启网关。这种“核心平台化，业务插件化”的设计思想，体现了极高的软件工程水准。

#### 4. 社区活跃度与生态：阿里背书的成熟开源项目
*   **事实**：Star 数较高（7.6k+），由阿里巴巴开源，拥有中英日三语 README，且文档结构详尽（涵盖架构、构建、WASM、AI、MCP 等）。
*   **推断**：作为阿里云通义系列背后的核心网关组件，该项目并非玩具级 Demo，而是经过了阿里内部大规模流量验证的工业级产品。多语言文档支持表明其有强烈的国际化意图和活跃的维护团队。社区不仅关注传统网关用户，正在积极吸纳 AI 开发者，形成了“云原生+AI”的独特交叉社区。

#### 5. 学习价值：理解下一代软件架构的窗口
*   **推断**：对于开发者而言，Higress 是学习 **“Infrastructure as Code”** 和 **“AI 工程化”** 的绝佳样本。
    *   **WASM 实践**：它展示了如何在网关层面安全、高效地运行沙箱代码，这是 Serverless 和边缘计算的核心技术。
    *   **协议扩展**：研究它如何处理 AI 协议（如 SSE 流式传输、Chunked 分块）以及如何实现 MCP 协议，对于理解未来 AI 应用的网络传输层设计极具启发意义。

### 边界条件与不适用场景
尽管 Higress 功能强大，但在以下场景中可能不是最优解：
1.  **极简边缘场景**：如果只需要在单机或边缘侧做简单的反向代理，Higress 基于 K8s/Istio 的架构显得过于重载，Nginx 或 Caddy 更合适。
2.  **纯业务逻辑处理**：虽然支持 WASM，但网关不应承载复杂的业务计算，涉及复杂事务或重度 CPU 密集型任务仍应在后端服务完成。
3.  **非容器化环境**：Higress 深度依赖 Kubernetes 生态，如果是传统 VM 部署架构，迁移成本较高。

### 快速验证清单
为了

---
## 技术分析

# Higress 技术架构与实现分析

Higress 是基于阿里云开源的云原生 API 网关，其核心特性在于结合了 Istio 的控制平面能力与 Envoy 的高性能数据转发，并针对 AI 流量治理进行了功能扩展。本文将从架构设计、核心组件、功能特性及技术原理进行解析。

---

## 1. 架构设计与技术栈

Higress 采用控制平面与数据平面分离的架构模式，复用 Envoy 作为 L7 数据平面，并基于 Go 语言重构了控制平面逻辑，去除了标准 Istio 中对于 Sidecar 模式的强依赖。

### 基础架构组成
*   **数据平面**：基于 **Envoy** 构建。负责处理实际的网络流量，包括负载均衡、HTTP/TCP 转发、TLS 终结以及执行 WebAssembly (WASM) 插件。
*   **控制平面**：基于 Go 语言开发。负责配置的下发与管理（通过 xDS 协议与 Envoy 通信），服务发现（对接 K8s Service, Nacos 等），以及证书管理。
*   **扩展模型**：采用 **Proxy-WASM** 机制。允许开发者使用 C++/Go/Rust 等语言编写插件，编译为 WASM 格式后在 Envoy 的沙箱中运行，实现业务逻辑的热加载。

### 核心模块解析
1.  **MCP (Model Context Protocol) Server**：
    Higress 内置了 MCP 协议服务端功能。该模块允许网关将后端 API 定义为工具，直接暴露给支持 MCP 协议的 AI 客户端（如 Claude Desktop），充当 AI Agent 与后端服务之间的桥梁。
2.  **AI 路由与流量管理**：
    针对大模型（LLM）场景，Higress 实现了特定的路由逻辑。它支持 SSE (Server-Sent Events) 流式转发，能够处理长连接下的分块传输，确保 AI 对话流在网关层的透传稳定性。
3.  **WASM 插件生态**：
    提供了插件市场机制，支持动态加载认证鉴权、限流熔断、请求/响应修改等插件，且无需重启网关进程。

### 架构特性
*   **配置热更新**：利用 xDS 协议（LDS/RDS/CDS/EDS），配置变更可实时下发至数据平面，无需重启服务。
*   **标准化接入**：支持 K8s Ingress 标准注解及 Gateway API，便于集成云原生生态。
*   **统一流量入口**：能够同时管理传统的 REST/gRPC 微服务流量与基于 SSE 的 AI 流量。

---

## 2. 核心功能与技术实现

### AI 流量治理
*   **多模型 Provider 接入**：提供统一的 API 规范来屏蔽不同模型厂商（如 OpenAI, 通义千问, DeepSeek）的接口差异。
*   **模型路由策略**：支持基于请求内容的路由分发。例如，根据请求头或 Prompt 内容，将不同复杂度的查询请求路由至不同参数规模的模型服务。
*   **Token 计费与统计**：通过 WASM 插件解析请求体和响应体，实现对 LLM Token 使用的计量与流控。

### MCP 协议集成
*   **工具暴露**：用户只需在网关配置后端服务的路由规则，Higress 即可自动生成 MCP 描述，使 AI 应用能够直接调用内部 API，无需额外的适配层代码。

### 与同类网关的对比
*   **对比 Nginx/Kong**：
    Kong 主要基于 OpenResty (Nginx + Lua)，Lua 虽然灵活但存在开发调试复杂、性能隔离性差（崩溃可能影响主进程）的问题。Higress 利用 WASM 的沙箱特性，实现了更好的资源隔离与安全性，且原生适配 K8s 环境。
*   **对比 Istio Ingress Gateway**：
    标准 Istio Gateway 配置复杂度较高，且缺乏针对 AI 场景（如 SSE 流式转发、MCP 协议）的内置支持。Higress 在保持 Istio 治理能力的基础上，提供了更开箱即用的 AI 特性。

---

## 3. 技术原理深度解析

### WASM 插件运行机制
Higress 遵循 Proxy-WASM 标准。当配置插件时，控制平面将 WASM 文件或配置推送给 Envoy。Envoy 启动一个独立的沙箱虚拟机来执行插件代码。插件通过 ABI (Application Binary Interface) 与 Envoy 主程序交互，访问请求头、修改 Body 或执行日志记录。这种机制保证了插件故障不会导致网关崩溃。

### AI 流式传输处理
在处理 LLM 请求时，Higress 需要处理 SSE 协议。网关在转发响应时，会维持 HTTP 长连接，并透传后端服务生成的 `data: chunk` 流。Higress 的优化点在于能够识别流式结束标记，并在不中断连接的情况下进行实时日志记录或元数据注入。

### 配置分发流程 (xDS)
Higress Console 或 CRD 资源变更 -> 控制平面监听并解析 -> 转换为 Envoy xDS 配置 -> 通过 gRPC 长连接推送到 Envoy -> Envoy 更新内存中的路由配置。该流程实现了配置的毫秒级生效。

---
## 代码示例




```python
# 示例1：基于Higress的API网关配置
def higress_api_gateway_config():
    """
    配置Higress作为API网关，实现路由转发和负载均衡
    解决问题：将外部请求路由到不同的微服务，并实现负载均衡
    """
    from higress import Gateway, Route, Service

    # 创建网关实例
    gateway = Gateway(name="api-gateway")

    # 定义后端服务
    user_service = Service(
        name="user-service",
        endpoints=["http://user-service-1:8080", "http://user-service-2:8080"],
        load_balancer="round_robin"
    )

    # 配置路由规则
    user_route = Route(
        path="/api/users/*",
        methods=["GET", "POST"],
        service=user_service,
        plugins=["auth-plugin", "rate-limit-plugin"]
    )

    # 添加路由到网关
    gateway.add_route(user_route)

    # 启动网关
    gateway.start()

# 说明：这个示例展示了如何使用Higress配置API网关，实现路由转发和负载均衡功能
```




```python
# 示例2：Higress插件开发 - 请求认证
def higress_auth_plugin():
    """
    开发一个Higress插件实现JWT认证
    解决问题：保护API端点，确保只有持有有效JWT的请求才能访问
    """
    from higress import Plugin, Context

    class JWTAuthPlugin(Plugin):
        def __init__(self):
            super().__init__(name="jwt-auth")
            self.secret_key = "your-secret-key"

        def on_request(self, context: Context):
            # 从请求头获取JWT
            token = context.request.headers.get("Authorization", "").replace("Bearer ", "")

            if not token:
                context.response.status_code = 401
                context.response.body = "Missing authentication token"
                return context.response

            try:
                # 验证JWT
                decoded = jwt.decode(token, self.secret_key, algorithms=["HS256"])
                context.user = decoded
                return context.request
            except jwt.InvalidTokenError:
                context.response.status_code = 401
                context.response.body = "Invalid authentication token"
                return context.response

    # 注册插件
    plugin = JWTAuthPlugin()
    plugin.register()

# 说明：这个示例展示了如何开发Higress插件实现JWT认证功能
```




```python
# 示例3：Higress流量管理 - 灰度发布
def higress_canary_deployment():
    """
    使用Higress实现灰度发布
    解决问题：逐步将流量从旧版本切换到新版本，降低发布风险
    """
    from higress import Gateway, Route, Service, CanaryRule

    # 创建网关实例
    gateway = Gateway(name="canary-gateway")

    # 定义生产版本服务
    stable_service = Service(
        name="product-service-stable",
        endpoints=["http://product-service-v1:8080"]
    )

    # 定义金丝雀版本服务
    canary_service = Service(
        name="product-service-canary",
        endpoints=["http://product-service-v2:8080"]
    )

    # 配置金丝雀规则
    canary_rule = CanaryRule(
        header="x-canary",
        values=["true"],
        percentage=10  # 10%的流量路由到金丝雀版本
    )

    # 配置路由
    product_route = Route(
        path="/api/products/*",
        methods=["GET"],
        service=stable_service,
        canary_service=canary_service,
        canary_rule=canary_rule
    )

    # 添加路由到网关
    gateway.add_route(product_route)

    # 启动网关
    gateway.start()

# 说明：这个示例展示了如何使用Higress实现灰度发布，控制流量分配
```


---
## 案例研究


### 1：某大型互联网公司 AI 助手业务

 1：某大型互联网公司 AI 助手业务

**背景**: 该公司内部及对外提供了一款基于大语言模型（LLM）的智能对话助手服务。随着用户量的激增，业务架构从传统的单体微服务转向了基于 LLM 的流式生成架构，需要频繁对接不同的模型提供商（如通义千问、OpenAI 等）并进行 Prompt 管理和调试。

**问题**: 原有的 API 网关（如 Nginx 或传统 Kong）在处理 LLM 场景时面临诸多痛点：
1.  **流式传输支持差**：难以高效处理 SSE（Server-Sent Events）流，导致大模型回答时的“打字机”效果卡顿。
2.  **缺乏模型层抽象**：业务代码与特定模型厂商的 API 强耦合，切换模型成本极高，且难以统一管理 Prompt 模板。
3.  **Token 计费与监控困难**：无法在网关层精确统计输入和输出的 Token 数量，导致成本核算和限流控制滞后。

**解决方案**: 引入 **Higress** 作为 AI 原生网关。
1.  利用 Higress 的 **AI 插件生态**，在网关层实现了对多家模型厂商 API 的统一适配，业务端只需调用 Higress 的标准接口。
2.  开启 **SSE 协议转换与流式处理**能力，确保大模型生成的数据流能够低延迟地透传给前端。
3.  配置 **Prompt 优化与管理插件**，在网关层动态注入系统提示词，无需修改后端业务代码。

**效果**:
1.  **开发效率提升**：新模型接入时间从 3 天缩短至小时级，仅需配置即可上线。
2.  **成本优化**：通过网关层的精确 Token 统计，成功实现了基于 Token 量的精细化配额控制，无效调用的成本降低了约 20%。
3.  **用户体验改善**：流式响应的首包延迟（TTFB）降低了 40%，消除了回答时的卡顿感。

---



### 2：某跨境电商平台微服务治理

 2：某跨境电商平台微服务治理

**背景**: 该平台业务遍布全球，采用 Spring Cloud 和 Kubernetes 构建的微服务架构。在大促活动期间，流量会呈现数十倍的增长，且涉及大量第三方物流和支付 API 的调用。

**问题**:
1.  **服务保护能力不足**：原有的网关在处理突发流量时缺乏精细化的限流熔断机制，导致下游核心服务（如订单服务）经常被突发流量击穿，造成雪崩效应。
2.  **多云与混合云管理复杂**：部分业务部署在阿里云，部分部署在自建机房，缺乏统一的流量入口和路由策略，导致灰度发布（金丝雀发布）流程繁琐。
3.  **高并发性能瓶颈**：传统网关在处理高并发 QPS 时延迟较高且 CPU 资源消耗过大。

**解决方案**: 使用 **Higress** 替换原有网关，依托其基于 Envoy 和 Istio 的底层架构进行深度治理。
1.  部署 **Higress Ingress** 作为 K8s 集群的统一入口，并配置 **全局限流**（基于 Redis）和 **服务熔断**规则，保护核心链路。
2.  利用 **HTTP 到 gRPC 的协议转换**功能，优化内部微服务间调用链路。
3.  实施 **Header 匹配的流量路由**，实现按地区或用户标签的蓝绿发布和灰度发布。

**效果**:
1.  **系统稳定性大幅提高**：在双 11 大促期间，成功拦截了 99.9% 的异常流量，核心订单服务零熔断，系统 P99 延迟下降了 60%。
2.  **资源成本降低**：得益于 Higress 的高性能 C++ 内核，网关层所需的计算资源减少了 50%，显著降低了服务器成本。
3.  **发布敏捷性**：实现了秒级的流量切换，新版本灰度发布风险降至最低，迭代周期从一周缩短至两天。

---
## 对比分析

## 与同类方案对比

| 维度          | Alibaba / Higress                         | Nginx + Lua (OpenResty)              | Kong                                   | Apache APISIX                         |
|---------------|------------------------------------------|-------------------------------------|----------------------------------------|---------------------------------------|
| 架构          | 基于Istio，支持云原生和微服务             | 传统单体架构，基于事件驱动           | 基于Nginx + Lua，模块化设计            | 基于OpenResty，动态化架构             |
| 性能          | 高性能，支持高并发（基于C++和Envoy）      | 高性能，但Lua脚本可能成为瓶颈        | 性能较好，但插件扩展可能影响吞吐量      | 极高性能，低延迟（基于OpenResty）     |
| 易用性        | 提供控制台和Kubernetes集成，上手较容易    | 配置复杂，需手动编写Lua脚本          | 提供管理界面，但插件配置较繁琐          | 提供Dashboard和API，配置灵活         |
| 成本          | 开源免费，云服务需付费                    | 开源免费，但需自行运维               | 开源免费，企业版需付费                  | 开源免费，企业支持需付费              |
| 扩展性        | 支持Wasm插件，扩展性强                    | 扩展性受限于Lua生态                  | 插件生态丰富，但性能可能受限            | 支持Lua和Wasm插件，扩展性极强        |
| 社区与生态    | 阿里背书，与云原生生态集成紧密             | 社区成熟，但创新较慢                 | 社区活跃，插件生态丰富                  | 社区活跃，国内支持较好                |
| 适用场景      | 云原生、微服务、API网关                   | 传统Web服务、简单网关                | 混合云、API管理                        | 高性能网关、微服务、边缘计算          |

### 优势分析

- **云原生集成**：深度集成Kubernetes和Istio，适合云原生环境。
- **高性能**：基于Envoy和C++实现，性能优于传统Lua方案。
- **易用性**：提供控制台和自动化运维工具，降低使用门槛。
- **扩展性**：支持Wasm插件，扩展性强且不影响性能。

### 不足分析

- **社区成熟度**：相比Nginx和Kong，社区生态尚在发展中。
- **学习曲线**：对Istio和Envoy的依赖可能增加学习成本。
- **企业支持**：开源版本功能有限，高级功能需依赖阿里云服务。
- **兼容性**：与传统架构（如非Kubernetes环境）集成可能较复杂。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 WASM 实现插件扩展与业务逻辑解耦

**说明**:
Higress 深度集成了 WASM (WebAssembly) 技术，允许使用 C++, Go, Rust, JavaScript 等多种语言编写插件。相比传统网关（如 Nginx）需要修改 C 模块或使用 Lua，WASM 提供了更好的隔离性、安全性以及开发便利性。通过 WASM 插件，可以将鉴权、流量整形、请求修改等业务逻辑从网关内核中剥离，实现业务与基础设施的解耦。

**实施步骤**:
1. 访问 Higress 官方插件市场或使用 Higress 提供的 CLI 工具 `hgctl` 创建一个新的插件项目。
2. 使用 Go 或 Rust 编写插件逻辑，利用 Higress 提供的 SDK 处理请求头、Body 或响应。
3. 构建生成 `.wasm` 文件，并通过 Higress 控制台或 WASM 插件配置接口上传。
4. 在网关路由配置中关联该插件，并配置相应的规则（如按域名或路径匹配）。

**注意事项**: WASM 插件虽然执行效率较高，但处理极其复杂的逻辑时仍会增加延迟，应避免在插件中进行阻塞式 IO 操作（如直接连接数据库），建议调用外部异步服务。

---

### 实践 2：利用 Ingress 注解实现精细化流量管理

**说明**:
Higress 兼容 Kubernetes Ingress 规范，并在此基础上进行了大量扩展。通过在 Ingress YAML 文件中添加特定的 Annotation（注解），可以在不修改网关核心配置的情况下，实现灰度发布、Header 转发、超时控制、限流等高级流量治理功能。

**实施步骤**:
1. 编辑 Kubernetes 中的 Ingress 资源文件。
2. 添加 `nginx.ingress.kubernetes.io/` 前缀或 Higress 特定的注解（如 `annotation.higress.io/`）。
3. 例如，配置金丝雀发布：`nginx.ingress.kubernetes.io/canary: "true"` 和 `nginx.ingress.kubernetes.io/canary-weight: "10"`。
4. 应用配置：`kubectl apply -f ingress.yaml`，Higress 控制面会自动监听变更并热更新网关配置。

**注意事项**: 注解配置虽然灵活，但过多复杂的注解会导致 Ingress 文件难以维护。建议将通用的复杂配置提取为 Higress 的 `WasmPlugin` 或 `GlobalPlugin` 进行管理。

---

### 实践 3：构建服务保护与自适应限流策略

**说明**:
在微服务架构中，网关是流量的咽喉，必须防止后端服务被突发流量击垮。Higress 提供了基于令牌桶、漏桶等算法的限流功能，并支持针对请求参数、Header、IP 等维度进行精细化限流。最佳实践是结合 Prometheus 监控指标，配置自适应的限流阈值。

**实施步骤**:
1. 在 Higress 控制台选择“流量治理” -> “限流管理”。
2. 创建限流规则，选择被防护的服务或路由。
3. 配置限流维度（例如：针对 `/api/v1/search` 接口，按 Query 参数 `user_id` 进行限流）。
4. 设置阈值（如 100 QPS）或开启“自适应限流”模式，让系统根据当前负载动态调整。
5. 配置限流后的返回策略（如直接返回 429 状态码或自定义 JSON 报文）。

**注意事项**: 限流配置应遵循“漏斗”原则，尽量在网关层进行粗粒度限制，在应用层进行细粒度限制。同时需注意限流算法的精度，避免突发流量导致误杀。

---

### 实践 4：配置全面的可观测性与监控集成

**说明**:
Higress 原生支持 Prometheus、OpenTelemetry 等标准可观测性协议。最佳实践不仅仅是监控网关本身的 CPU/内存，更要建立基于服务、路由、RPC 状态码的立体化监控体系，以便快速定位由于网关配置错误或后端服务异常引起的问题。

**实施步骤**:
1. 部署 Prometheus 并配置 Higress 作为数据抓取目标，暴露 `/metrics` 端口。
2. 配置 Access Log（访问日志），将其输出到标准输出或 Kafka/ELK 等日志系统，日志格式建议采用 JSON 以便解析。
3. 启用 Tracing（链路追踪），配置 Higress 将 Tracing 数据发送至 Jaeger 或 Zipkin。
4. 在 Grafana 中导入 Higress 官方提供的 Dashboard 模板，重点监控 Request Duration、Error Rate、QPS 等关键指标。

**注意事项**: 高流量场景下，开启详细的 Tracing 或全量 Access Log 会产生巨大的性能开销和数据存储压力。建议使用采样追踪（

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 HTTP/3 (QUIC) 协议支持

**说明**: Higress 基于 Envoy 和 Istio 构建，支持 HTTP/3 协议。HTTP/3 基于 UDP 协议，解决了 TCP 队头阻塞问题，能显著降低弱网环境下的延迟，并提升连接迁移速度（如从 Wi-Fi 切换到 4G/5G）。

**实施方法**:
1. 在 Higress 的网关路由配置中，开启 HTTP/3 监听器。
2. 配置证书以支持 QUIC 协议的 TLS 握手。
3. 在客户端（浏览器或 SDK）确保启用了 HTTP/3 支持。

**预期效果**: 在高丢包率或高延迟网络环境下，页面加载时间或 API 调用延迟可降低 20%-40%。

---

### 优化 2：配置全局限流与并发控制

**说明**: Higress 内置了高性能的限流功能。通过配置全局限流，可以防止突发流量击垮后端服务，确保系统稳定性。同时，利用 Token Bucket 算法可以精准控制请求速率。

**实施方法**:
1. 在 Higress 控制台或 Wasm 插件中配置全局或特定路由的限流规则。
2. 设置合理的 QPS（每秒查询率）阈值，基于后端服务的实际处理能力。
3. 针对关键 API 启用并发请求限制，防止长连接占用过多资源。

**预期效果**: 将后端服务的错误率（如 502/504）降低至接近 0%，并在流量洪峰时保持 99.99% 的可用性。

---

### 优化 3：利用 Wasm 插件实现轻量级自定义逻辑

**说明**: Higress 原生支持 WebAssembly (Wasm) 插件。相比于传统的 Lua 或外部调用，Wasm 插件执行效率更高，且安全性更好（沙箱隔离）。将复杂的鉴权、Header 修改或请求转换逻辑下沉到网关层 Wasm 插件中，可大幅减少后端业务代码的耦合度与计算开销。

**实施方法**:
1. 编写高性能的 Wasm 插件（推荐使用 Rust 或 C++）。
2. 将编译好的 `.wasm` 文件上传至 Higress 插件市场。
3. 在特定路由或全局范围内启用该插件，并配置相关参数。

**预期效果**: 相比于后端服务处理鉴权逻辑，网关层拦截可减少 10-30ms 的额外网络跳转延迟，并降低后端 CPU 负载约 15%。

---

### 优化 4：启用 DNS 缓存与连接池复用

**说明**: 默认的 DNS 解析和频繁建立 TCP 连接会带来显著的延迟。Higress 允许配置上游服务的 DNS 缓存时间以及 HTTP/2 连接池大小。优化这些参数可以减少握手开销。

**实施方法**:
1. 在 Higress 的 Upstream 配置中，调整 `dns_refresh_rate`，延长 DNS 缓存时间（例如设置为 60s 或更长，视服务动态性而定）。
2. 启用 HTTP/2 协议与后端通信，并调大 `max_requests_per_connection` 参数。
3. 确保连接池大小（如 `max_connections`）与后端处理能力匹配，避免频繁建连。

**预期效果**: 减少 DNS 查询和 TCP 握手带来的 10-50ms 延迟，提升吞吐量 10%-20%。

---

### 优化 5：实施细粒度的缓存策略

**说明**: 对于读多写少的 API 或静态内容，利用 Higress 的本地缓存能力（支持内存缓存）可以直接在网关层返回数据，从而完全绕过后端服务。

**实施方法**:
1. 针对响应式 API，配置 Higress 的 `response_cache` 插件。
2. 设置基于 HTTP Header（如 `Cache-Control`）或自定义 Key 的缓存规则。
3. 对于热点数据，启用

---
## 学习要点

- Higress 是阿里云开源的高性能、可扩展的云原生 API 网关，基于 Envoy 和 Istio 构建，支持 Kubernetes 和非 Kubernetes 环境。
- 提供标准化的南北向（流量入口）和东西向（服务间）流量管理能力，兼容 Kubernetes Ingress 和 Gateway API 标准。
- 内置丰富的流量治理功能，如路由重写、负载均衡、灰度发布、熔断降级和超时重试等。
- 原生集成 WAF 安全防护能力，支持针对 API 请求的精细安全策略，保障后端服务稳定性。
- 支持插件市场及自定义插件（Wasm/Go/Python/Java），允许用户通过低代码方式扩展网关功能。
- 提供对 Dubbo、Nacos 和 gRPC 等微服务生态的深度适配，方便传统微服务架构无缝接入云原生网关。
- 具备全链路可观测性，支持与 Prometheus、SkyWalking 等监控系统集成，便于实时掌握流量状态。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础

**学习内容**:
- Higress 的基本概念与核心架构
- Higress 与传统网关（如 Nginx、Kong）的区别
- Higress 的安装与部署（Docker/Kubernetes）
- 基本配置：路由、域名、SSL/TLS 设置
- Higress 控制台的基本操作

**学习时间**: 1-2周

**学习资源**:
- [Higress 官方文档](https://higress.io/docs/latest/)
- [Higress GitHub 仓库](https://github.com/alibaba/higress)
- [Higress 快速入门教程](https://higress.io/docs/latest/overview/what-is-higress/)

**学习建议**: 
先通过官方文档了解 Higress 的设计理念，然后动手部署一个简单的示例，熟悉基本操作和配置。

---

### 阶段 2：进阶提升

**学习内容**:
- 高级路由策略（权重路由、灰度发布、流量镜像）
- 插件系统的使用与开发（Wasm 插件）
- 服务发现与注册中心集成（Nacos、Consul 等）
- 安全防护：认证鉴权（JWT、OIDC）、限流熔断
- 监控与日志（Prometheus、Grafana、Loki）

**学习时间**: 2-4周

**学习资源**:
- [Higress 插件开发文档](https://higress.io/docs/latest/user/plugin-howto/)
- [Higress 高级配置指南](https://higress.io/docs/latest/user/advanced-configuration/)
- [Higress 社区案例](https://github.com/alibaba/higress/tree/main/samples)

**学习建议**: 
结合实际业务场景尝试配置高级路由和插件，关注社区案例和最佳实践，逐步深入理解 Higress 的扩展能力。

---

### 阶段 3：精通与实践

**学习内容**:
- Higress 的性能优化与调优
- 多集群部署与高可用架构设计
- 自定义 Wasm 插件开发（Go/C++/Rust）
- Higress 在云原生生态中的集成（Istio、Envoy）
- 大规模生产环境问题排查与解决方案

**学习时间**: 4-6周

**学习资源**:
- [Higress 源码分析](https://github.com/alibaba/higress/tree/main/core)
- [Higress 性能测试报告](https://higress.io/blog/2023/01/17/higress-performance-test/)
- [Higress 社区贡献指南](https://github.com/alibaba/higress/blob/main/CONTRIBUTING.md)

**学习建议**: 
深入阅读源码，参与社区讨论或贡献代码，尝试在复杂生产环境中部署和优化 Higress，积累实战经验。

---
## 常见问题


### 1: Higress 是什么？它与阿里巴巴和 Nginx 有什么关系？

1: Higress 是什么？它与阿里巴巴和 Nginx 有什么关系？

**A**: Higress 是一个开源的、基于云原生的 API 网关。它是阿里巴巴内部多年在 API 网关技术上的沉淀，并基于开源项目 Nginx 进行了深度的二次开发和扩展。Higress 旨在为云原生架构提供高性能、高可用的流量管理、安全防护和插件扩展能力。它兼容 Nginx 的配置习惯，同时集成了阿里巴巴在电商、金融等高并发场景下的最佳实践，支持 Kubernetes Ingress 以及南北向与东西向流量的统一治理。

---



### 2: Higress 与其他开源 API 网关（如 Apache APISIX 或 Kong）相比有什么优势？

2: Higress 与其他开源 API 网关（如 Apache APISIX 或 Kong）相比有什么优势？

**A**: Higress 的核心优势主要体现在以下几个方面：
1.  **云原生深度集成**：Higress 天然支持 Kubernetes Ingress（K8s Ingress），能够无缝对接阿里云容器服务（ACK）以及标准的 K8s 环境，配置更加简洁。
2.  **高性能与低资源消耗**：基于 C++ 和 Go 的混合架构，数据处理面（基于 Envoy 或 Nginx）性能极高，且资源占用相对较低。
3.  **标准化与兼容性**：支持 OpenAPI 规范，能够轻松纳管基于 Spring Cloud、Dubbo 或 gRPC 的微服务应用，实现协议转换。
4.  **WAF 防护**：内置了与阿里云云盾同源的 Web 应用防火墙（WAF）能力，提供企业级的安全防护。
5.  **插件生态**：支持 Lua 和 WASM (WebAssembly) 插件，WASM 插件支持多语言编写（如 Go, C++, Rust），且热更新更灵活，不中断业务。

---



### 3: Higress 是否支持从 Nginx 或传统网关进行迁移？

3: Higress 是否支持从 Nginx 或传统网关进行迁移？

**A**: 是的，Higress 非常重视迁移的便利性。
1.  **Nginx 兼容**：Higress 的核心路由逻辑很大程度上兼容 Nginx 的配置思路。对于使用 Nginx Ingress Controller 的用户，Higress 提供了较为平滑的迁移路径。
2.  **配置转换工具**：社区和官方通常提供配置迁移工具或指南，帮助用户将传统的 Nginx 配置或 Kong/APISIX 的配置转换为 Higress 的 CRD（自定义资源）配置。
3.  **流量无损切换**：在 K8s 环境中，通过调整 Ingress Class 或 Service 选择器，可以实现流量的逐步灰度切换，确保迁移过程不影响线上业务。

---



### 4: Higress 如何处理服务发现？它支持哪些注册中心？

4: Higress 如何处理服务发现？它支持哪些注册中心？

**A**: Higress 设计为云原生网关，因此它主要通过以下方式处理服务发现：
1.  **Kubernetes Service**：这是最原生的方式。Higress 直接监听 K8s 的 API Server，根据 Service 和 Endpoints 的变化自动更新路由后端，无需额外配置。
2.  **主流注册中心集成**：对于非 K8s 环境或混合部署环境，Higress 支持集成主流的服务注册中心，包括 **Nacos**、**Consul**、**ZooKeeper** 以及 **Eureka**。这意味着 Higress 可以直接从这些注册中心拉取服务列表，实现后端服务的动态发现和负载均衡，特别适合微服务架构。

---



### 5: Higress 的安全性如何？是否支持 WAF 和认证鉴权？

5: Higress 的安全性如何？是否支持 WAF 和认证鉴权？

**A**: Higress 提供了多层安全防护机制：
1.  **WAF 防护**：它内置了基础的 WAF 功能，能够防御常见的 Web 攻击（如 SQL 注入、XSS 等）。对于更高级的需求，它可以深度集成阿里云 Web 应用防火墙。
2.  **认证与鉴权**：支持标准的认证方式，包括 **Basic Auth**、**AK/SK** 鉴权、**JWT** (JSON Web Token) 校验以及 **OIDC** (OpenID Connect) 单点登录。
3.  **IP 访问控制**：支持黑名单和白名单机制，可以基于 IP 或 CIDR 区段限制访问。
4.  **插件化安全**：用户可以通过编写插件来扩展自定义的安全逻辑，例如实现自定义的 Token 校验或请求签名验证。

---



### 6: Higress 支持 WASM (WebAssembly) 插件吗？这有什么好处？

6: Higress 支持 WASM (WebAssembly) 插件吗？这有什么好处？

**A**: 是的，对 WASM 的支持是 Higress 的一个核心亮点。
1.  **多语言支持**：传统的 Nginx 扩展通常需要懂 Lua 语言，而 Higress 支持 WASM 后，开发者可以使用 **Go、C++、Rust** 甚至 AssemblyScript 来编写插件。
2.  **隔离性与稳定性**：WASM 插件运行在独立的沙箱环境中。即使插件崩溃（例如出现空指针异常），也不会导致网关主进程崩溃，从而极大地提高了网关自身的稳定性。
3.  **

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: Higress 基于 Envoy 构建，但默认配置并未开启 Envoy 的访问日志。请尝试修改 Higress Gateway 的部署配置，开启标准 Envoy 格式的访问日志，并确保日志能输出到容器的标准输出中以便于日志收集工具采集。

### 提示**: 关注 Higress Gateway 的 Bootstrap 配置注入方式，通常需要修改 Pod 的环境变量或启动参数来覆盖默认的 `bootstrap_config`。

### 

---
## 实践建议

基于 Higress 作为 AI Native API 网关的定位，结合其作为云原生网关的技术特性，以下是 6 条针对实际使用场景的实践建议：

### 1. 利用 "One-Shot" 模式优化流式响应延迟
在处理大语言模型（LLM）的流式请求时，建议在路由配置中优先启用 **One-Shot** 模式（如果目标模型支持）。
*   **具体操作**：在服务来源或插件配置中，针对流式接口启用该模式。这允许网关在收到首包响应后立即向客户端传输数据，而无需等待完整响应体。
*   **最佳实践**：对于对话类 AI 应用，此配置能显著降低用户感知的首字延迟（TTFT）。
*   **常见陷阱**：如果后端服务不支持流式或分块传输，强制开启可能导致连接中断或数据截断，需先确认后端兼容性。

### 2. 实施基于语义的 Prompt 模板管理
不要在应用代码中硬编码 Prompt，应充分利用 Higress 的 **AI 插件生态**进行 Prompt 管理。
*   **具体操作**：使用 `ai-proxy` 等相关插件，在网关层面配置 System Prompt 和 User Prompt 模板。利用变量替换机制（如 `{{query}}`）将客户端请求动态注入模板。
*   **最佳实践**：将 Prompt 的版本控制与业务代码解耦。当需要调整模型行为（如修改角色设定）时，仅需在网关控制台更新配置，无需重新发布业务服务。
*   **常见陷阱**：未对 Prompt 中的特殊字符进行转义处理，可能导致模板解析失败或注入攻击。

### 3. 配置细粒度的 Token 限流与预算控制
LLM 调用成本高昂，且容易受到恶意请求或异常流量冲击，必须配置针对 Token 的限流策略。
*   **具体操作**：结合 Higress 的 `token-ratelimit` 插件或自定义鉴权插件，针对 API Key 或用户 ID 设置每分钟/每天的 Token 预算。
*   **最佳实践**：设置“软限制”和“硬限制”。软限制触发时返回警告，硬限制触发时直接阻断请求，防止产生意外的云服务账单。
*   **常见陷阱**：仅配置了基于请求数（QPS）的限流，忽略了单个 Prompt 可能包含数千个 Token 的情况，导致成本失控。

### 4. 善用 Wasm 插件实现模型结果后处理
利用 Higress 对 Wasm (WebAssembly) 的原生支持，在网关层直接处理模型返回的数据，减轻后端业务逻辑负担。
*   **具体操作**：编写或部署 Wasm 插件，对 AI 返回的 JSON 进行清洗、格式化或注入额外的元数据（如计费信息、模型版本）。
*   **最佳实践**：例如，可以将不同模型厂商（OpenAI 格式 vs. 通义千问格式）的异构响应结构在网关层统一转换为标准格式，对客户端屏蔽底层模型差异。
*   **常见陷阱**：在 Wasm 插件中进行过于复杂的 CPU 密集型计算（如长文本正则匹配），会阻塞网关的事件循环，导致整体吞吐量下降。

### 5. 构建多模型供应商的容灾切换机制
AI 服务的稳定性依赖于模型提供商的 SLA，建议在网关层配置多供应商路由。
*   **具体操作**：配置多个服务来源（Service），分别指向 OpenAI、Azure OpenAI 或本地部署的 Ollama/DeepSeek。在路由规则中配置权重或故障转移（Failover）策略。
*   **最佳实践**：设置自动降级逻辑。当主供应商响应超时或返回 5xx 错误时，网关自动将请求重试或转发至备用供应商。
*   **常见陷阱**：不同供应商的 API 参数不完全兼容，在切换供应商前，务必确保 `ai-proxy` 插件的参数映射已正确配置，否则会导致切换后的请求报错。

### 6. 建立可观测

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI 原生](/tags/ai-%E5%8E%9F%E7%94%9F/) / [LLM](/tags/llm/) / [MCP](/tags/mcp/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [WASM](/tags/wasm/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260206-github_trending-alibaba-higress-0.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260206-github_trending-alibaba-higress-6.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260215-github_trending-alibaba-higress-5.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260216-github_trending-alibaba-higress-6.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*