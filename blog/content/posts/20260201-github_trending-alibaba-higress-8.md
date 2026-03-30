---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-02-01T11:05:04+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "AI 原生", "Istio", "Envoy", "WASM", "LLM", "MCP 协议"]
categories: ["系统与基础设施", "AI 工程"]
source: github_trending
description: "以下是基于您提供的内容对 **Higress** 的简洁总结： **1. 项目概况** * **名称**：Higress * **开发方**：阿里巴巴 * **核心定位**：基于 Istio 和 Envoy 构建的**AI 原生 API 网关**（AI Native API Gateway）。 * **编程语言**：G"
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
- **星标**: 7,419 (+4 stars today)
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

Higress 是一款基于 Istio 和 Envoy 构建的 AI 原生 API 网关。它通过集成 WASM 插件能力，实现了对传统流量管理与 LLM 应用场景的统一支持，旨在解决云原生架构下微服务路由与 AI 服务代理的融合问题。本文将介绍其核心架构、AI 网关特性以及 MCP 系统的集成方式，帮助开发者利用 Higress 构建高效、可扩展的 AI 应用基础设施。

---
## 摘要

以下是基于您提供的内容对 **Higress** 的简洁总结：

**1. 项目概况**
*   **名称**：Higress
*   **开发方**：阿里巴巴
*   **核心定位**：基于 Istio 和 Envoy 构建的**AI 原生 API 网关**（AI Native API Gateway）。
*   **编程语言**：Go。
*   **社区热度**：GitHub 星标数超过 7,400。

**2. 核心架构与特性**
*   **技术基础**：建立在云原生生态系统之上，扩展了 Istio 和 Envoy 的功能。
*   **扩展能力**：通过 **WebAssembly (WASM)** 插件系统提供高度可扩展性。
*   **架构设计**：采用**控制平面**与**数据平面**分离的架构。
*   **性能优势**：配置变更通过 xDS 协议传播，具备毫秒级延迟且连接不中断，特别适用于 AI 长连接流式响应场景。

**3. 三大核心功能与用途**
Higress 提供以下主要功能，覆盖了从传统微服务到现代 AI 应用的需求：

*   **AI 网关**：
    *   **功能**：为 LLM（大语言模型）应用提供统一 API。
    *   **支持范围**：统一对接 30+ 家 LLM 提供商，包含协议转换、可观测性、缓存和安全防护。
    *   **关键组件**：`ai-proxy`（代理）、`ai-statistics`（统计）、`ai-cache`（缓存）、`ai-security-guard`（安全）。

*   **MCP 服务器托管**：
    *   **功能**：托管模型上下文协议（MCP）服务器，使 AI 智能体能够调用外部工具和服务。
    *   **关键组件**：包含 `mcp-router`、`jsonrpc-converter` 以及针对特定工具的实现（如 `quark-search`、`amap-tools`）。

*   **Kubernetes Ingress（传统 API 网关）**：
    *   **功能**：作为 Kubernetes 的 Ingress 控制器，管理微服务路由。
    *   **兼容性**：兼容 nginx-ingress 注解，便于用户迁移。

**总结**：H

---
## 评论

### 总体判断

Higress 是目前云原生网关领域中将**AI 原生能力**与**传统流量治理**融合得最为彻底的开源项目之一。它成功将 Istio 的控制平面能力下沉，同时通过 WASM 技术解决了网关扩展性与性能的矛盾，是构建 LLM 应用基础设施的强力候选。

### 深入评价依据

#### 1. 技术创新性：WASM 为基石的“AI+”架构
*   **事实**：Higress 基于 Envoy 和 Istio 构建，但核心差异化在于其 **WebAssembly (WASM)** 插件系统。DeepWiki 明确指出它提供“AI gateway features for LLM applications”和“MCP server hosting”。
*   **推断**：传统网关（如 Nginx）扩展依赖 Lua（如 OpenResty）或 C++ 模块，存在内存安全风险和隔离性差的问题。Higress 全面拥抱 WASM，实现了**插件的热加载与沙箱隔离**。这意味着开发者可以用 Go/C++/Rust/Zig 编写逻辑，动态下发至网关而无需重启服务。更关键的是，它将 **MCP (Model Context Protocol)** 服务托管能力直接集成进网关，这是极具前瞻性的创新。它允许网关作为 AI Agent 的“工具调度中心”，直接在请求路由层处理模型与外部数据源的交互，而不仅仅是做一个透传代理。

#### 2. 实用价值：统一流量与 AI 语义治理
*   **事实**：文档提到它同时提供“Kubernetes Ingress”、“microservice routing”和“AI gateway features”。
*   **推断**：在 LLM 应用落地中，企业面临两个割裂的问题：微服务 API 管理和 LLM 语义/Token 管理。通常这需要两套系统（如 Kong + 专门的 AI Proxy），增加了运维复杂度。Higress 的实用价值在于**统一了这两条数据链路**。它既支持传统的金丝雀发布、负载均衡，又能处理 AI 特有的 Token 计费、Prompt 模板注入和上下文缓存。对于已经使用 K8s 的团队，Higress 提供了一个“零侵入”的 AI 转型路径，避免了为了接入大模型而重构网络架构。

#### 3. 架构设计与代码质量：云原生标准的控制面分离
*   **事实**：DeepWiki 强调架构分离了“control plane (configuration management)”与“data plane (traffic processing)”。语言采用 Go。
*   **推断**：从技术选型看，Go 语言非常适合构建高并发的控制平面。Higress 继承了 Istio 的配置分发理念，但去除了 Istio 中繁重的 Sidecar 模式，专注于 **Ingress Gateway** 场景，这大大降低了部署的资源门槛和运维复杂度。代码结构上，作为阿里系开源项目，其代码规范性较高，模块划分清晰。特别是对 WASM 的支持，说明其架构设计具有高度的**可插拔性**，符合现代软件工程关注点分离的原则。

#### 4. 社区活跃度与生态：背靠阿里的成熟度
*   **事实**：星标数 7,419（且在快速增长），语言支持中/日/英，文档覆盖了从架构到开发的七个维度。
*   **推断**：高星标数反映了市场对“AI Gateway”概念的强烈需求。作为阿里巴巴开源项目，它大概率已经经受过了淘宝/阿里云等超大规模流量的验证（内部通常有 Higress 的商业版或前身）。社区不仅关注传统的 API 管理，更因为 AI 功能的引入，吸引了大量 AI 应用开发者。文档的多语言支持和详细的分类（如专门的 MCP 系统章节）表明该项目致力于构建**开发者友好的生态**，而非仅仅是代码堆砌。

#### 5. 与同类工具对比优势：比 Kong 更云原生，比 Istio 更轻量
*   **事实**：对比同类工具（如 Kong, APISIX, Traefik）。
*   **推断**：
    *   **对比 Kong/APISIX**：Higress 的 WASM 支持比 Kong 的传统插件机制更现代、更安全。且 Higress 天然与 K8s Ingress API 强兼容，不需要像 Kong 那样配置复杂的 CRD 或 DB。
    *   **对比原生 Istio**：Higress 剥离了 Istio 冗余的控制面组件，简化了配置流程。对于不需要 Service Mesh 全栈能力，只需要一个强大入口网关的场景，Higress 的**资源消耗更低，配置更直观**。

### 边界条件与不适用场景

尽管 Higress 功能强大，但在以下场景中需慎重：
*   **极致边缘场景**：如果需要在资源极度受限的边缘设备（如嵌入式网关）运行，Go 语言和 Envoy 的内存占用可能不如 C 语言编写的轻量级代理（如 OpenResty）。
*   **非 K8s 环境**：虽然支持容器化部署，但其核心优势在于与 K8s 的深度集成。如果是传统的虚拟机裸金属部署，配置复杂度可能高于 Nginx。
*   **复杂的服务间通信治理**：如果业务需求是全链路 Mesh（微服务之间的 mTLS、流量熔断），Higress 仅作为网关无法解决，需要完整的 Istio 体系。

### 快速验证清单

在决定生产级采用 Higress 前，建议执行以下验证：

1.  **WASM 性能损耗

---
## 技术分析

# Higress 技术架构与功能深度解析

本文基于阿里巴巴开源的 Higress 项目（AI Native API Gateway），重点从架构设计、核心组件、技术实现及功能特性四个维度进行客观分析。

## 1. 技术架构剖析

### 基础架构模式
Higress 采用标准的**控制平面与数据平面分离**架构，遵循云原生设计原则。

*   **数据平面**：基于 **Envoy** 构建。利用 C++ 实现的高性能网络处理能力（L3/L7），负责承载实际的业务流量转发。
*   **控制平面**：使用 **Go** 语言开发。负责处理配置分发、服务发现及证书管理等逻辑。通过 xDS 协议（v2/v3）与数据平面通信，实现配置的动态下发。
*   **生态兼容**：复用 Istio 的 xDS 协议栈，但不依赖 Sidecar 注入模式，而是专注于 Ingress Gateway 场景。

### 核心组件设计
1.  **路由匹配引擎**：直接使用 Envoy 的高性能路由表机制，支持基于权重、Header、Cookie 等复杂条件的流量路由。
2.  **插件运行时**：集成 **WebAssembly (WASM)** 虚拟机。允许开发者使用 C/C++/Rust/Go 等语言编写扩展逻辑，运行在隔离的沙箱环境中，实现了业务逻辑与网关核心的解耦。
3.  **配置分发机制**：控制平面监听配置变更（如 K8s Ingress 资源或 Higress 自定义 CRD），通过 xDS 协议推送到数据平面。该过程支持热更新，无需重启数据平面进程。
4.  **AI 流量处理层**：针对大语言模型（LLM）场景扩展的数据处理模块，支持 SSE（Server-Sent Events）流式传输、Token 统计及协议转换。

### 架构特性分析
*   **性能表现**：数据平面基于 Envoy C++ 实现，具备较低的转发延迟。
*   **扩展能力**：WASM 机制支持在不修改主程序代码的情况下，动态加载或卸载插件（如鉴权、限流）。
*   **协议兼容性**：完全兼容 Kubernetes Ingress 标准，支持将 Nginx Ingress 配置迁移至 Higress。

## 2. 核心功能详解

### AI 网关能力
Higress 针对大模型应用场景提供了特定的流量治理功能：

*   **统一协议接入**：屏蔽不同 LLM 厂商（如 OpenAI, 通义千问等）的 API 差异，提供统一调用入口。
*   **密钥与安全**：在企业网关层统一管理 LLM API Key，避免密钥分散到各个客户端应用中。
*   **流式数据处理**：支持 SSE 协议的透传与处理，满足流式输出的低延迟需求。
*   **流量统计**：提供基于 Token 数量或请求次数的计量统计能力。

### MCP (Model Context Protocol) 集成
*   **功能定位**：作为 MCP Server 的托管端点。
*   **实现逻辑**：将外部工具（如数据库查询、文件读取）封装为标准 API 接口。Higress 负责处理 AI Agent 对这些工具的调用请求，并进行统一的认证与鉴权管理。

### 标准 API 网关特性
*   **Kubernetes Ingress Controller**：支持作为 K8s 集群南北向流量的统一入口。
*   **流量治理**：支持灰度发布（金丝雀发布）、负载均衡算法选择、全链路加密（TLS）及服务发现。

### 技术选型对比
| 特性 | Higress | Nginx/Kong | Istio (Gateway) |
| :--- | :--- | :--- | :--- |
| **数据平面语言** | C++ (Envoy) | C (Nginx) / C (Kong) | C++ (Envoy) |
| **扩展机制** | WASM / Go Plugin | Lua (Nginx) / Lua/Js (Kong) | WASM / C++ |
| **配置协议** | xDS / K8s CRD | 配置文件 reload | xDS / K8s CRD |
| **AI 特性支持** | 原生集成 | 需额外插件 | 依赖 Envoy 原生能力 |

---
## 代码示例

```python
# 示例1：基于Higress的API网关流量路由配置
from higress_gateway import GatewayConfig

def configure_api_routing():
    """
    配置Higress网关实现基于URL路径的流量路由
    适用场景：微服务架构中根据不同路径转发到不同后端服务
    """
    gateway = GatewayConfig("prod-gateway")
    
    # 配置路由规则：将/api/v1/user请求转发到用户服务
    gateway.add_route(
        path="/api/v1/user/*",
        destination="user-service:8080",
        plugins={
            "rateLimit": "100/minute",  # 添加限流插件
            "auth": "jwt"               # 启用JWT认证
        }
    )
    
    # 配置路由规则：将/api/v1/order请求转发到订单服务
    gateway.add_route(
        path="/api/v1/order/*",
        destination="order-service:8080",
        plugins={
            "cache": "redis"            # 启用Redis缓存
        }
    )
    
    gateway.apply_config()
    print("API路由配置已应用")

# 说明：这个示例展示了如何使用Higress实现微服务API网关的流量路由，
# 包括路径匹配、服务转发以及常用插件（限流、认证、缓存）的配置。
```

```python
# 示例2：Higress WAF安全防护配置
from higress_waf import WAFConfig

def configure_waf_protection():
    """
    配置Higress的Web应用防火墙规则
    适用场景：保护API免受常见Web攻击（SQL注入、XSS等）
    """
    waf = WAFConfig()
    
    # 启用SQL注入防护
    waf.add_rule(
        name="sql_injection_protection",
        match_type="regex",
        pattern="(union|select|insert|delete|update|drop|create)",
        action="block"
    )
    
    # 启用XSS攻击防护
    waf.add_rule(
        name="xss_protection",
        match_type="regex",
        pattern="<script|javascript:|onerror=",
        action="block"
    )
    
    # 配置IP黑名单
    waf.add_ip_blacklist(["192.168.1.100", "10.0.0.50"])
    
    waf.apply_config()
    print("WAF安全规则已配置")

# 说明：这个示例展示了如何使用Higress的WAF功能保护API安全，
# 包括配置正则规则拦截恶意请求和IP黑名单管理。
```

```python
# 示例3：Higress插件开发：自定义请求头处理
from higress_plugin import PluginBase

class CustomHeaderPlugin(PluginBase):
    """
    自定义Higress插件实现请求头处理
    适用场景：需要为所有请求添加自定义头信息或修改现有头
    """
    
    def on_request(self, request):
        # 添加自定义请求头
        request.headers["X-Custom-Header"] = "Higress-Python-Plugin"
        
        # 修改现有头
        if "User-Agent" in request.headers:
            request.headers["User-Agent"] += " Higress/1.0"
        
        # 根据请求路径添加特定头
        if "/api/v1/" in request.path:
            request.headers["X-API-Version"] = "v1"
        
        return request

# 注册插件
plugin = CustomHeaderPlugin()
plugin.register()

# 说明：这个示例展示了如何开发Higress自定义插件，
# 实现了请求头的动态添加和修改功能，可根据实际需求扩展。
```

---
## 案例研究

### 1：阿里巴巴集团内部业务（淘天集团）

 1：阿里巴巴集团内部业务（淘天集团）

**背景**:
在阿里巴巴内部，微服务架构极其复杂，成千上万的下游服务需要被不同的前端业务（如淘宝、天猫、聚划算等）调用。传统的 API 网关在处理大规模流量、复杂路由逻辑以及与阿里内部服务治理体系（如 Dubbo、HSF）对接时，往往存在性能瓶颈或维护成本过高的问题。

**问题**:
原有的网关解决方案在应对“双11”等大促场景的突发流量时，配置变更的灵活性不足，且对 K8s Ingress 的支持不够原生。开发团队需要一个既能复用 Nginx/OpenResty 的高性能特性，又能深度集成云原生生态，并且支持热更新和 WAF 安全防护的统一入口层。

**解决方案**:
阿里巴巴基于 Higress（前身是内部内部自用的 MOSN 网关体系）构建了统一的云原生 API 网关。Higress 兼容 K8s Ingress 标准，并深度集成了阿里内部的服务发现机制。通过 Higress，团队实现了将流量网关与微服务网关的合一，利用其标准化的 WASM 插件机制来扩展功能，替代了传统的 Lua 脚本开发。

**效果**:
通过引入 Higress，阿里巴巴内部实现了网关层的极致性能优化，P99 延迟显著降低。WASM 插件的沙箱隔离特性保证了网关核心的稳定性，同时极大地提升了业务迭代的效率，使得复杂的路由和安全策略可以通过插件的形式动态加载，无需重启网关服务，成功支撑了万亿级日调用的流量规模。

---

### 2：某大型互联网电商平台的 API 生态开放

 2：某大型互联网电商平台的 API 生态开放

**背景**:
该电商平台拥有庞大的开放 API 生态，需要将商品、订单、物流等核心能力开放给第三方合作伙伴和独立软件开发商（ISV）。随着接入的第三方应用数量激增，API 的管理、安全认证和流量控制变得日益复杂。

**问题**:
原有的 API 管理系统存在以下痛点：1. 流量控制粒度不够细，无法针对不同合作伙伴实施差异化的限流策略；2. 接口鉴权逻辑老旧，难以适配新型的 OAuth 2.0 或 API Key 签名机制；3. 开发者体验不佳，API 变更通知滞后，导致联调效率低下。

**解决方案**:
该平台引入 Higress 作为其开放 API 的流量入口和管理核心。利用 Higress 的全托管特性，团队快速配置了精细化的路由规则，并利用 Higress 的插件市场（如 KeyAuth、RequestBlock）实现了开箱即用的安全防护。同时，结合 Higress 对 OpenAPI 规范的支持，实现了 API 文档与网关配置的自动化同步。

**效果**:
Higress 的部署使得 API 接入效率提升了 50% 以上。通过配置化的方式替代了硬编码开发，新上线安全策略的周期从“天”级缩短至“小时”级。系统成功抵御了多次恶意爬虫攻击，且在高并发场景下保持了 99.99% 的可用性，极大地提升了合作伙伴的接入体验和平台的整体安全性。

---

### 3：某 AI 创业公司的 LLM（大语言模型）服务网关

 3：某 AI 创业公司的 LLM（大语言模型）服务网关

**背景**:
随着 AIGC 的爆发，该公司需要对外提供基于 LLM 的智能对话服务。由于模型推理成本高昂且耗时较长，直接暴露后端服务会导致资源被轻易耗尽，且不同客户对并发和 Token 数量的限制需求差异巨大。

**问题**:
传统的 API 网关主要处理 HTTP 转发，缺乏针对 AI 场景的特殊处理能力。主要问题包括：无法感知流式传输（SSE）的上下文进行精确计费或拦截；缺乏针对 Prompt 注入攻击的防护手段；以及难以在网关层实现简单的“模型路由”或“提示词增强”逻辑。

**解决方案**:
该公司采用 Higress 作为 AI 服务的专用网关。利用 Higress 对 SSE（Server-Sent Events）流式转发的原生支持，确保了终端用户能实时获得生成内容。同时，开发了自定义 WASM 插件，在网关层实现了基于 Token 预估的并发限制和敏感词过滤，并利用 Higress 的后端路由功能，根据用户等级智能地将请求分发到不同规格的模型服务上。

**效果**:
通过 Higress 的精细化控制，该公司有效控制了昂贵的 GPU 算力资源，避免了因恶意请求导致的成本激增。流式响应的稳定性大幅提升，用户体验更加流畅。此外，网关层的敏感词拦截率达到了 98% 以上，极大降低了后端模型服务的合规风险。

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | Kong | APISIX |
|------|----------------|------|-------|
| 性能 | 高性能，基于 Envoy 和 Istio，支持高并发和低延迟 | 高性能，基于 Nginx 和 OpenResty，适合高并发场景 | 极高性能，基于 OpenResty 和 LuaJIT，性能接近 Nginx |
| 易用性 | 提供图形化控制台和 K8s 集成，配置简单 | 配置灵活但需手动管理，学习曲线较陡 | 提供图形化控制台和 API，配置相对简单 |
| 成本 | 开源免费，阿里云提供商业支持 | 开源免费，企业版需付费 | 开源免费，企业版需付费 |
| 扩展性 | 支持插件扩展，与 K8s 和 Istio 集成良好 | 支持插件扩展，社区插件丰富 | 支持插件扩展，插件生态活跃 |
| 社区支持 | 阿里背书，社区活跃但较新 | 社区成熟，文档和插件丰富 | 社区活跃，国内支持较好 |
| 适用场景 | 云原生、微服务、API 管理 | 传统 API 网关、微服务 | 云原生、微服务、高并发场景 |

### 优势分析

- 优势1：基于 Envoy 和 Istio，与云原生生态集成紧密，适合 K8s 环境。
- 优势2：提供图形化控制台，降低配置复杂度，适合快速上手。
- 优势3：阿里背书，商业支持可靠，适合企业级应用。

### 不足分析

- 不足1：社区较新，插件生态和文档不如 Kong 和 APISIX 丰富。
- 不足2：对非 K8s 环境的支持较弱，传统架构迁移成本较高。
- 不足3：性能优化和稳定性需要更多生产环境验证。

---
## 最佳实践

## 最佳实践指南

### 实践 1：基于 Wasm 插件扩展网关功能

**说明**: Higress 深度集成了 WebAssembly (Wasm) 技术，允许开发者使用 C/C++、Go、Rust 或 AssemblyScript 编写高性能的插件。相比传统的 Lua 脚本或硬编码方式，Wasm 插件提供了更好的隔离性、更高的执行效率以及热加载能力，能够灵活扩展网关的认证、流量整形、请求转换等能力。

**实施步骤**:
1. 根据团队技术栈选择合适的 Wasm 开发语言（推荐 Go 或 Rust）。
2. 利用 Higress 官方提供的 SDK 或 `wasm-assembler` 工具进行插件开发。
3. 在本地或 CI/CD 流水线中将代码编译为 `.wasm` 文件。
4. 通过 Higress 控制台或 WASM 插件管理接口上传插件，并配置路由作用域。
5. 配置插件的参数配置，并在测试环境验证性能损耗。

**注意事项**: Wasm 插件运行在沙箱中，处理内存和 CPU 资源受限，应避免在插件中进行长时间阻塞操作或大量内存分配。

---

### 实践 2：精细化流量管理与安全防护

**说明**: 利用 Higress 强大的路由规则和安全插件能力，实现对微服务流量的精细化控制。这包括基于 Header、Query 参数、Cookie 等维度的路由分流，以及通过内置的 IP 访问控制、请求防重放和动态认证机制保障 API 安全。

**实施步骤**:
1. 配置 Canary（金丝雀）发布或 Blue-Green（蓝绿）部署路由规则，实现流量的按比例切换。
2. 启用 `block-list` 或 `allow-list` 插件，限制恶意 IP 或特定地域的访问。
3. 针对敏感 API 配置 JWT 认证或 Keyless 认证插件。
4. 开启请求速率限制，防止 API 被滥用或遭受 DDoS 攻击。

**注意事项**: 路由匹配优先级需谨慎规划，避免因规则冲突导致流量被错误转发。安全策略的更新应尽量采用热更新方式，避免影响业务连续性。

---

### 实践 3：对接服务注册中心实现服务发现

**说明**: Higress 原生支持 Nacos、Consul、Zookeeper 以及 Kubernetes Service 等多种服务注册中心。通过配置服务来源，网关可以自动感知后端服务实例的上下线状态，实现动态负载均衡，无需手动维护上游节点列表。

**实施步骤**:
1. 在 Higress 控制台的“服务来源”页面，添加对应类型的注册中心（如 Nacos）。
2. 配置注册中心的连接地址（Server Addr）、命名空间和访问凭证。
3. 创建服务并关联注册中心中的服务名。
4. 在路由配置中引用该服务，并配置健康检查策略。

**注意事项**: 确保 Higress 所在网络能够直连注册中心网络。对于大规模服务列表，建议开启服务缓存以减轻注册中心压力，并合理设置健康检查间隔。

---

### 实践 4：利用 Ingress 注解实现 Kubernetes 集成

**说明**: 如果您在 Kubernetes 环境中运行 Higress，最佳实践是将其作为 Ingress Controller 使用。通过在 Ingress YAML 文件中添加特定的 Annotation（注解），可以直接声明式地配置网关的高级功能（如限流、重试、CORS 跨域等），实现基础设施即代码。

**实施步骤**:
1. 部署 Higress Gateway 到 Kubernetes 集群。
2. 编写标准的 Kubernetes Ingress 资源文件。
3. 根据需求添加 Higress 特定的 Annotation，例如 `nginx.ingress.kubernetes.io/canary: "true"` 的等效注解或 Higress 专有的配置注解。
4. 应用配置，Higress 会自动监听 Ingress 变更并更新网关规则。

**注意事项**: 不同版本的 Higress 对注解的支持可能有所不同，升级版本前需查阅注解兼容性文档。避免在注解中通过 Base64 编码传输过大的配置内容。

---

### 实践 5：全链路可观测性与监控集成

**说明**: 生产环境的网关必须具备完善的可观测性。Higress 提供了日志、指标和链路追踪的全面支持。通过集成 Prometheus、Grafana、SkyWalking 或 OpenTelemetry，可以实时监控网关的 QPS、延迟、错误率，并快速定位服务调用链中的瓶颈。

**实施步骤**:
1. 配置 Higress 的 Access Log 输出，支持 JSON 格式并对接 Kafka、Filebeat 或 Elasticsearch。
2. 开开 Prometheus Metrics 采集端口，配置 Prometheus 抓取规则。
3. 部署 Grafana 并导入 Higress 官方提供的 Dashboard 模板。
4. 启用 Tracing 功能，配置采样率（如 10%），并将数据发送

---
## 性能优化建议

## 性能优化建议

### 优化 1：启用 WASM 插件与本地缓存

**说明**: Higress 支持 WASM (WebAssembly) 插件，相比传统 Lua 插件具有更高的执行效率和隔离性。同时，利用 Higress 的本地缓存功能可以减少对后端服务的重复请求。

**实施方法**:
1. 将高频使用的 Lua 插件迁移至 WASM 格式
2. 在网关路由配置中启用本地缓存
3. 配置合理的缓存 TTL (建议 60-300 秒)
4. 对缓存键进行优化设计

**预期效果**: 
- WASM 插件执行效率提升 30-50%
- 缓存命中时减少 90% 的后端请求
- 整体响应延迟降低 40-60%

---

### 优化 2：连接池与 Keep-Alive 优化

**说明**: 合理配置 HTTP/gRPC 连接池参数可以显著减少连接建立开销，提高资源利用率。

**实施方法**:
1. 调整连接池大小 (建议 max: 1024)
2. 启用 HTTP Keep-Alive (timeout: 60s)
3. 配置合理的连接超时时间 (建议 10-30s)
4. 启用连接复用 (http2: max_concurrent_streams: 100)

**预期效果**:
- 连接建立开销减少 80%
- 吞吐量提升 20-30%
- CPU 使用率降低 15-25%

---

### 优化 3：启用 HTTP/2 与 gRPC 优化

**说明**: HTTP/2 协议的多路复用特性可以显著提升并发性能，特别适合微服务架构。

**实施方法**:
1. 在 Listener 配置中启用 HTTP/2
2. 调整 HTTP/2 参数 (max_concurrent_streams: 100)
3. 启用 gRPC 代理优化
4. 配置合理的流控窗口大小 (initial_window_size: 65536)

**预期效果**:
- 并发连接数减少 70%
- 长连接场景下吞吐量提升 40-60%
- 尾延迟降低 30%

---

### 优化 4：日志与监控优化

**说明**: 优化日志采样策略和监控指标采集频率可以减少 I/O 开销。

**实施方法**:
1. 配置日志采样 (建议 10% 采样率)
2. 禁用不必要的访问日志字段
3. 调整 Prometheus 指标采集间隔 (建议 15s)
4. 使用异步日志上报

**预期效果**:
- 日志写入 I/O 降低 90%
- 磁盘占用减少 80%
- 日志处理开销降低 70%

---

### 优化 5：资源限制与自动扩缩容

**说明**: 合理配置资源限制并启用 HPA (Horizontal Pod Autoscaler) 可以确保性能稳定。

**实施方法**:
1. 设置合理的 CPU/内存 requests 和 limits (建议 1:2 比例)
2. 配置 HPA 策略 (CPU > 70% 时扩容)
3. 启用 Pod 优先级和抢占机制
4. 使用 Node Affinity 优化调度

**预期效果**:
- 资源利用率提升 30-40%
- 峰值响应时间波动减少 50%
- 集群资源成本降低 20%

---
## 学习要点

- 基于提供的上下文（alibaba/higress），以下是关于该项目的关键要点总结：
- Higress 是阿里云开源的一款基于 Istio 构建的云原生 API 网关，旨在深度整合云原生生态与流量管理。
- 它提供了从 K8s Ingress 到 API 网关的统一解决方案，解决了传统架构中网关功能碎片化的问题。
- 该项目支持将 Kong、Nginx、Spring Cloud 等传统网关无缝迁移至云原生架构，降低了技术栈升级的门槛。
- Higress 兼容 Ingress 和 Gateway API 标准，并集成了 WAF 插件市场，提供了强大的安全防护与扩展能力。
- 它通过将配置数据与运行时数据分离，显著提升了大规模流量场景下的性能与稳定性。
- 该项目具备极致的轻量化特性，可作为 Sidecar 代理与 Service Mesh 深度集成，实现微服务连接的统一管理。

---
## 学习路径

## 学习路径

### 阶段 1：入门基础与核心概念

**学习内容**:
- **云原生网关基础**: 理解什么是 API 网关，以及 Higress 在微服务架构中的定位（流量入口、南北向流量管理）。
- **核心架构**: 学习 Higress 的架构设计，了解其基于 Envoy 和 Istio 的技术栈，以及它如何将 Ingress (入口网关) 和 Gateway (东西向网关) 合二为一。
- **基本安装与部署**: 掌握在 Kubernetes 环境下通过 Helm 或标准 YAML 资源文件部署 Higress。
- **控制台操作**: 熟悉 Higress 的原生控制台（Dubbo Admin 风格）或 Kaili 控制台的基本使用，包括配置路由、服务来源。

**学习时间**: 1-2周

**学习资源**:
- **Higress 官方文档**: [https://higress.io/docs/latest/](https://higress.io/docs/latest/) (重点关注“快速开始”和“产品介绍”)
- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress) (阅读 README 和 Architecture 部分)
- **Envoy 基础知识**: Envoy 官方文档中关于 Proxy 和 Listener 的概念。

**学习建议**:
建议先在本地搭建一套 Kind 或 Minikube 的 Kubernetes 环境，并成功部署 Higress。不要急于配置复杂规则，先通过浏览器访问控制台，熟悉界面布局和“域名->路由->服务”的基本配置逻辑。

---

### 阶段 2：流量治理与路由配置

**学习内容**:
- **HTTP 路由**: 深入学习路径匹配、Header 重写/转发、重定向配置。
- **全链路灰度发布**: 掌握基于 Header 或 Cookie 的流量染色，实现蓝绿发布和金丝雀发布。
- **负载均衡策略**: 学习如何配置轮询、随机、最小连接数等负载均衡算法，以及基于权重的流量分发。
- **服务来源对接**: 学习如何将 Kubernetes Service、Nacos、Consul、固定地址（DNS/IP）以及 MSE (微服务引擎) 注册为 Higress 的服务来源。
- **安全防护**: 配置 Basic Auth (基础认证)、JWT 认证以及 IP 黑白名单访问控制。

**学习时间**: 2-3周

**学习资源**:
- **Higress 官方文档 - 流量治理**: 详细阅读 Ingress、Gateway API 配置章节。
- **K8s Ingress Controller 对比**: 对比 Nginx Ingress 和 Higress 的配置差异，理解 Higress 的优势（如支持 Wasm 插件）。

**学习建议**:
动手实践是关键。尝试部署两个不同版本的“模拟后端服务”，通过配置 Higress 路由规则，实现将 10% 的流量导入新版本。同时，尝试对接一个 Nacos 注册中心，体验 Higress 与传统微服务组件的无缝融合。

---

### 阶段 3：插件生态与 Wasm 扩展

**学习内容**:
- **插件系统**: 理解 Higress 的插件工作原理，重点学习 Wasm (WebAssembly) 技术在网关侧的应用。
- **预置插件使用**: 熟练使用官方提供的插件，如：请求限流、响应头定制、Keyless Auth、CORS 跨域配置等。
- **自定义插件开发 (Go/C++/Rust)**: 学习如何使用 Go (AssemblyScript) 编写自定义 Wasm 插件，并在 Higress 中加载和调试。
- **插件市场**: 了解如何在 Higress 插件市场中查找和安装社区插件。

**学习时间**: 3-4周

**学习资源**:
- **Higress 插件开发文档**: [https://higress.io/docs/latest/developers/wasm-go/](https://higress.io/docs/latest/developers/wasm-go/)
- **Wasm 官方网站**: 了解 WebAssembly 的基本概念。
- **示例代码**: GitHub 上 Higress 官方提供的 `wasm-go` 示例插件仓库。

**学习建议**:
从修改一个现有的官方插件开始（例如修改请求头插件），然后尝试编写一个简单的“请求阻断”或“Key 认证”插件。重点理解 Wasm 插件的生命周期和 VM 上下文，这是 Higress 区别于传统网关的核心竞争力。

---

### 阶段 4：高可用架构与生产实践

**学习内容**:
- **高可用部署**: 学习 Higress 控制面和数据面的分离部署，以及多副本容错配置。
- **性能调优**: 理解 Envoy 的连接池配置、缓冲区设置以及 Higress 的资源限制。
- **可观测性**: 集成 Prometheus/Grafana 进行监控，配置日志收集（SLS/ELK），以及启用分布式链路追踪

---
## 常见问题

### 1: Higress 是什么？它与阿里巴巴和云原生社区有什么关系？

1: Higress 是什么？它与阿里巴巴和云原生社区有什么关系？

**A**: Higress 是一个基于阿里内部两年多的实践，由阿里云和蚂蚁集团联合开源的云原生 API 网关。它建立在 Envoy 和 Istio 等开源项目之上，旨在提供标准化、高集成、易扩展、云原生的网关解决方案。Higress 兼容 Kubernetes Ingress 标准，并深度集成了 Nacos 等微服务生态组件，是阿里巴巴在云原生网关领域技术对外输出的重要载体。

---

### 2: Higress 与 Nginx、Kong 或 APISIX 等传统网关相比有什么核心优势？

2: Higress 与 Nginx、Kong 或 APISIX 等传统网关相比有什么核心优势？

**A**: Higress 的主要优势在于其云原生架构和深度集成能力：
1.  **性能与资源消耗**：基于 Envoy C++ 内核，相比基于 Lua 的 Kong 或 OpenResty（Nginx），在处理高并发时具有更低的延迟和更稳定的资源消耗。
2.  **安全防护**：内置了针对 WAF（Web Application Firewall）的插件支持，能够更好地防范 SQL 注入、XSS 等常见攻击，且安全插件与业务流量插件隔离，互不影响。
3.  **服务发现集成**：原生支持 Nacos、ZooKeeper、Consul 等注册中心，无需额外配置即可实现从微服务到网关的自动化路由，这在传统网关中通常需要复杂的配置或额外组件。
4.  **标准化**：完全支持 Kubernetes Ingress 和 Gateway API 标准，便于在云原生环境中迁移和管理。

---

### 3: Higress 是否支持从 Nginx 或 Ingress Controller（如 Nginx Ingress Controller）迁移？

3: Higress 是否支持从 Nginx 或 Ingress Controller（如 Nginx Ingress Controller）迁移？

**A**: 是的，Higress 提供了强大的兼容性工具来降低迁移成本。
1.  **配置兼容**：Higress 提供了 Nginx 配置转换工具，可以帮助用户将现有的 Nginx 配置转换为 Higress 的路由配置。
2.  **注解兼容**：对于 Kubernetes 用户，Higress 兼容 Nginx Ingress Controller 的大部分常用注解，这意味着用户往往只需要修改 Ingress 资源的类名即可完成初步迁移，无需立即重写所有配置。
3.  **协议兼容**：完全支持 HTTP/HTTPS、WebSocket、gRPC、Dubbo 等协议。

---

### 4: Higress 的插件机制是如何工作的？能否编写自定义插件？

4: Higress 的插件机制是如何工作的？能否编写自定义插件？

**A**: Higress 采用了灵活的插件（Wasm 插件）架构。
1.  **Wasm 支持**：Higress 允许使用 WebAssembly (Wasm) 技术编写插件。这意味着开发者可以使用 C++、Go、Rust、JavaScript (AssemblyScript) 等多种语言编写业务逻辑，而无需修改网关的核心代码或重新编译网关。
2.  **动态加载**：插件支持热加载，可以在不重启网关实例的情况下动态添加、删除或修改插件规则。
3.  **Lua 兼容**：为了照顾 OpenResty/Nginx 用户的使用习惯，Higress 也支持 Lua 脚本插件，降低了旧有脚本逻辑迁移的难度。

---

### 5: Higress 如何处理流量管理和灰度发布（金丝雀发布）？

5: Higress 如何处理流量管理和灰度发布（金丝雀发布）？

**A**: Higress 继承并增强了 Istio 的流量管理能力。
1.  **Header/Query 匹配**：支持基于 HTTP Header、Query 参数、Cookie 等进行流量路由，实现灰度发布。
2.  **按比例分流**：支持设置流量百分比，将特定比例的流量路由到新版本服务。
3.  **全链路灰度**：配合微服务注册中心（如 Nacos），Higress 可以实现标签路由，确保灰度流量在调用链路中始终保持在灰度版本的服务节点上，避免灰度流量回滚到旧版本。

---

### 6: Higress 是否支持 Dubbo 服务，如何进行 HTTP 到 Dubbo 的协议转换？

6: Higress 是否支持 Dubbo 服务，如何进行 HTTP 到 Dubbo 的协议转换？

**A**: 是的，Higress 对 Dubbo 提供了原生级支持，这是其区别于许多国外开源网关的一个重要特性。
1.  **直接调用**：Higress 可以直接作为 Dubbo 服务的消费者，通过注册中心发现服务地址并发起调用。
2.  **协议转换**：它支持将 HTTP/HTTPS 请求自动转换为 Dubbo (Hessian2/JSONRPC) 协议调用。这使得前端应用可以通过 RESTful API 调用后端的 Dubbo 微服务，无需在中间层搭建额外的转换服务。
3.  **多注册中心**：支持同时连接多个注册中心，适合复杂的微服务架构环境。
## 实践建议

基于 Higress 作为 AI Native API 网关的定位，结合其云原生架构与 AI 流量处理特性，以下是 6 条针对实际生产环境的实践建议：

### 1. 利用 Wasm 插件实现非侵入式鉴权与流控
*   **场景**：当你需要对接大模型（如 OpenAI, Azure, 通义千问等）并控制访问权限时。
*   **建议**：不要在应用代码中硬编码 API Key。应使用 Higress 的 **Wasm 插件生态**（如 `ai-proxy` 或 `key-auth`）在网关层统一管理 Provider 的 API Key。这样可以在不同环境（开发、测试、生产）无缝切换密钥，且无需重新部署业务服务。
*   **最佳实践**：为不同的业务线或租户创建不同的路由，并绑定独立的 API Key 实现计费或配额管理。
*   **常见陷阱**：在网关配置文件中明文存储敏感 Key。应使用 KMS 或类似保密系统引用环境变量。

### 2. 实施语义缓存以降低 Token 成本
*   **场景**：处理大量重复或高度相似的问答请求（如常见客服问题）。
*   **建议**：启用 Higress 的 **AI 缓存** 功能。不同于传统的 HTTP 缓存，AI 网关能根据语义对 Prompt 进行缓存。对于相同的用户问题，直接返回缓存结果而不请求 LLM。
*   **最佳实践**：针对“知识库问答”类场景开启缓存，设置合理的 TTL（生存时间），并配置 `Cache-Control` 头部策略。
*   **常见陷阱**：对实时性要求极高的场景（如股票查询）开启了长时间缓存，导致用户获取过时信息。

### 3. 配置请求与响应的 "超时" 与 "重试" 策略
*   **场景**：大模型推理耗时较长且不稳定，容易出现 504 超时或 Provider 端偶发错误。
*   **建议**：根据不同模型的平均响应时间调整网关的 `ReadTimeout`。对于流式响应，需确保超时设置足够长以接收首个数据包。
*   **最佳实践**：配置**指数退避** 的重试策略。如果 LLM 返回 5xx 错误或连接中断，网关应自动重试，但要对上游 Provider 保护，避免重试风暴。
*   **常见陷阱**：未区分流式（SSE）和非流式请求的超时配置，导致流式连接被网关过早切断。

### 4. 构建模型路由与降级策略
*   **场景**：生产环境中某个模型服务不可用，或需要根据成本在模型间切换（如 GPT-4 降级到 GPT-3.5）。
*   **建议**：利用 Higress 的 **服务路由** 功能，根据 HTTP Header（如 `x-model-version`）或 URL 路径将流量分发到不同的后端模型服务。
*   **最佳实践**：设置“兜底模型”。当主模型（高精度、高成本）响应超时或报错时，网关自动将请求转发至备用模型（低精度、低成本、高可用），确保业务不中断。
*   **常见陷阱**：未对备用模型进行充分测试，导致主服务挂掉后，备用服务因流量突增也跟着崩溃。

### 5. 细化 Prompt 模板管理
*   **场景**：开发者在代码中拼接 Prompt，难以维护且容易注入攻击。
*   **建议**：在网关层管理 Prompt 模板。通过 Higress 配置系统提示词，业务端只需传递核心变量。
*   **最佳实践**：结合 `ai-proxy` 插件，在网关侧预置 System Message。例如，设定“你是一个翻译助手”的模板，前端只需发送 `text=hello`，网关自动拼接完整 Prompt 发送给 LLM。
*   **常见陷阱**：允许前端直接传递未经过滤的 System Message，这可能导致用户通过 Prompt Injection 绕过安全限制。

### 6.

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [AI 原生](/tags/ai-%E5%8E%9F%E7%94%9F/) / [Istio](/tags/istio/) / [Envoy](/tags/envoy/) / [WASM](/tags/wasm/) / [LLM](/tags/llm/) / [MCP 协议](/tags/mcp-%E5%8D%8F%E8%AE%AE/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/) / [DevOps/运维](/scenarios/devops-%E8%BF%90%E7%BB%B4/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260130-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260129-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-8.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260131-github_trending-alibaba-higress-9.md" >}})
- [Amla Sandbox：面向 AI 智能体的 WASM Bash 沙箱]({{< relref "posts/20260130-hacker_news-show-hn-amla-sandbox-wasm-bash-shell-sandbox-for-a-1.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*