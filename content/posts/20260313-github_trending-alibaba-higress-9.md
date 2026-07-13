---
title: 阿里开源 Higress：AI 原生 API 网关
date: 2026-03-13 00:51:38+08:00
draft: false
entry_kind: auto
tags:
- Higress
- API 网关
- AI Native
- Istio
- Envoy
- WASM
- LLM
- MCP 协议
categories:
- 系统与基础设施
- 开源生态
source: github_trending
description: 以下是关于 **Higress** 的简洁总结： **1. 项目概述** Higress 是由阿里巴巴开源的一款**云原生 API 网关**。它基于
  **Istio** 和 **Envoy** 构建，并扩展了 **WebAssembly (WASM)** 插件能力，定位为 **AI Native API Gateway
external_url: https://github.com/alibaba/higress
scenarios:
- AI/ML项目
- 大语言模型
- 云原生/容器
---

# 阿里开源 Higress：AI 原生 API 网关

---

## 基本信息

- **描述**: 🤖 AI 网关 | AI 原生 API 网关
- **语言**: Go
- **星标**: 7,743 (+12 stars today)
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

Higress 作为阿里云开源的 AI Native API Gateway，基于 Istio 和 Envoy 构建，通过引入 WebAssembly (WASM) 插件机制和对大模型（LLM）场景的深度适配，正在重新定义云原生 API 网关的边界。以下是对该项目的深入技术分析。
