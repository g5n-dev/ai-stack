---
title: 阿里开源 Higress：AI 原生 API 网关
date: 2026-03-05 11:00:06+08:00
draft: false
entry_kind: auto
tags:
- Higress
- API 网关
- AI 原生
- LLM
- Istio
- Envoy
- WASM
- MCP
categories:
- 系统与基础设施
- 开源生态
source: github_trending
description: 以下是对 **Higress** 项目的中文总结： **Higress** 是阿里巴巴开源的一款**云原生 API 网关**，基于 Istio
  和 Envory 构建，并扩展了 WebAssembly (WASM) 插件能力。它定位为 **AI Native API Gateway（AI 原生 API
  网关）**，旨在
external_url: https://github.com/alibaba/higress
scenarios:
- AI/ML项目
- 云原生/容器
- DevOps/运维
---

# 阿里开源 Higress：AI 原生 API 网关

---

## 基本信息

- **描述**: 🤖 AI 网关 | AI 原生 API 网关
- **语言**: Go
- **星标**: 7,649 (+11 stars today)
- **链接**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

---

## DeepWiki 速览（节选）

Relevant source files

  * [README.md](https://github.com/alibaba/higress/blob/8deceb4d/README.md)
  * [README_JP.md](https://github.com/alibaba/higress/blob/8deceb4d/README_JP.md)
  * [README_ZH.md](https://github.com/alibaba/higress/blob/8deceb4d/README_ZH.md)

---

## 导语

Higress 是基于 Istio 和 Envoy 构建的 AI 原生 API 网关，它通过 WebAssembly 插件扩展了云原生流量管理能力。该项目专为需要统一管理传统微服务与 LLM 应用的场景设计，提供了包括 AI 网关特性、MCP 服务器托管及 Kubernetes Ingress 在内的核心功能。本文将介绍其系统架构、控制面与数据面的分离设计，以及如何利用 WASM 插件系统实现灵活的流量治理与模型集成。

---

## 摘要

以下是对 **Higress** 项目的中文总结：

**Higress** 是阿里巴巴开源的一款**云原生 API 网关**，基于 Istio 和 Envory 构建，并扩展了 WebAssembly (WASM) 插件能力。它定位为 **AI Native API Gateway（AI 原生 API 网关）**，旨在为现代应用尤其是大模型（LLM）应用提供强大的流量管理和处理能力。

以下是核心要点总结：

**1. 核心架构与特性：**
*   **技术栈**：使用 Go 语言编写，底层基于 Envoy，控制面基于 Istio。
*   **高性能与灵活性**：架构上分离了**控制面**（配置管理）和**数据面**（流量处理）。配置变更通过 xDS 协议传播，延迟低至毫秒级且不断连，特别适合 AI 流式响应等长连接场景。
*   **可扩展性**：通过 WASM 插件系统提供强大的扩展能力。

**2. 三大主要功能：**

*   **AI 网关**：
    *   **功能**：提供统一的 API 接口，兼容 30 多家 LLM 提供商。
    *   **核心组件**：包括 `ai-proxy`（协议转换）、`ai-statistics`（可观测性）、`ai-cache`（缓存）和 `ai-security-guard`（安全防护）等插件，用于处理大模型请求的协议转换、监控、缓存及安全。

*   **MCP 服务器托管**：
    *   **功能**：托管模型上下文协议（MCP）服务器，使 AI 智能体能够便捷地调用外部工具和服务。
    *   **核心组件**：利用 `mcp-router`、`jsonrpc-converter` 过滤器及具体的 MCP 服务实现（如 `quark-search`、`amap-tools`）。

*   **传统 API 网关**：
    *   **功能**：作为 Kubernetes Ingress 控制器使用，支持微服务路由。
    *   **兼容性**：兼容 nginx-ingress 注解，方便用户迁移。

**3. 项目现状：**
该项目目前在 GitHub 上拥有超过 7,600 颗星，活跃度较高。

---

## 评论

总体判断
Higress 是目前云原生网关领域中将 AI 原生能力与流量管理结合得最彻底的开源项目之一，它成功地将 Istio 的控制平面能力下沉，同时通过 WASM 技术解决了传统网关扩展性差的痛点。对于寻求构建统一 AI 网关与微服务网关架构的团队来说，这是一个极具前瞻性且工程化成熟度极高的选择。

核心评价依据

**1. 技术创新性：WASM 插件生态与 AI 原生深度集成**
*   **事实**：DeepWiki 明确指出 Higress 基于 Istio 和 Envoy 构建，并引入了 WebAssembly (WASM) 插件系统。它不仅提供传统的 API 网关功能，还内置了 AI Gateway 特性和 MCP (Model Context Protocol) 服务器托管能力。
*   **推断**：Higress 的最大差异化在于其“AI Native”的定位。传统的 API 网关（如 Kong 或 APISIX）在处理 LLM 流量时，往往需要通过 Lua 或 Go 插件硬编码 Token 计数或上下文拼接逻辑，扩展性差且不安全。Higress 利用 WASM 的沙箱特性，允许开发者使用 C++/Go/Rust 甚至 TypeScript 编写高性能插件，实现了“热更新”与“多语言支持”。此外，直接集成 MCP 协议支持，使其成为了连接 AI Agent 与工具链的关键基础设施，这在目前的开源网关中是非常稀缺的。

**2. 实用价值：统一架构降低运维复杂度**
*   **事实**：文档描述其核心功能包括“AI gateway features for LLM applications”、“MCP server hosting”以及“traditional API gateway capabilities including Kubernetes Ingress”。
*   **推断**：在 AI 落地场景中，企业常面临两套网关并存的困境：一套管微服务（如 Nginx/Ingress），一套管大模型流量（如 LangChain 代理）。Higress 的价值在于将这两者合二为一。它不仅能处理标准的南北向流量，还能针对 LLM 的特殊需求（如流式输出处理、Token 限流、模型路由）进行精细化管理。这种“All-in-One”的架构显著降低了基础设施的冗余度和运维成本，特别适合正在从传统微服务架构向 AI 架构转型的企业。

**3. 代码质量与架构：控制与数据分离的云原生设计**
*   **事实**：Higress 使用 Go 语言开发，架构上明确分离了控制平面和数据平面。它基于 Envoy 这一业界公认的高性能数据平面，并针对 K8s 环境进行了深度优化。
*   **推断**：选择 Go 语言结合 Envoy，是云原生基础设施的黄金组合，保证了系统的高并发处理能力（得益于 Envoy 的 C++ 性能）和开发效率（得益于 Go 的并发模型）。从架构设计看，Higress 继承了 Istio 的流量管理理念，但剥离了 Istio 过于沉重的 Sidecar 模式，使其更适合作为边界网关或 K8s Ingress Controller 使用。这种设计既保证了底层代码的健壮性，又通过 WASM 提供了极高的可扩展性，代码结构清晰，符合云原生社区的最佳实践。

**4. 社区活跃度与背书：阿里的技术护城河**
*   **事实**：该项目由 Alibaba 开源，星标数达到 7,649（且在持续增长），并提供了中、日、英多语言文档。
*   **推断**：作为阿里集团内部淘系业务通用的网关设施，Higress 经受了“双十一”级别流量的验证，这意味着其核心稳定性和性能指标远超一般的开源实验性项目。高星标数和多语言文档表明其拥有一个国际化的开发者社区，且阿里巴巴的持续投入保证了项目不会轻易烂尾。对于企业级用户而言，这种大厂背书是采用该技术栈的重要信心来源。

**5. 潜在问题与改进建议**
*   **推断**：虽然 WASM 性能优异，但其开发门槛相比简单的 Nginx 配置或脚本编写要高，对于不熟悉低级语言（如 C/Rust）的运维人员存在一定学习曲线。此外，作为 AI 网关，其对 LLM 供应商的适配丰富度（是否支持国产大模型、私有化部署模型的鉴权）仍需在实际部署中验证。建议在引入前，重点评估其 WASM 插件市场的成熟度以及团队对 Go/C++ 语言的掌控能力。

边界条件与不适用场景
*   **超低延迟场景**：对于极端追求微秒级延迟的纯四层负载均衡，Linux 内核态方案（如 Cilium/eBPF）可能比基于 Envoy 的用户态方案更优。
*   **简单静态站点**：如果仅需托管简单的静态博客或小型站点，Nginx 或 Caddy 的配置更为轻量，无需引入 K8s 生态的复杂度。

---

## 技术分析

基于 Alibaba 开源的 Higress 仓库（AI Native API Gateway），本文将从架构设计、核心功能、技术实现、适用场景、发展趋势及工程哲学等维度进行深入剖析。
