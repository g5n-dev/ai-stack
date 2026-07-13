---
title: 阿里开源 Higress：AI 原生 API 网关
date: 2026-03-12 22:57:34+08:00
draft: false
entry_kind: auto
tags:
- Higress
- API网关
- AI原生
- 阿里云
- Istio
- Envoy
- LLM
- MCP协议
categories:
- 系统与基础设施
- 开源生态
source: github_trending
description: '**Higress：基于 Istio 与 Envoy 的云原生 AI 网关** **1. 项目概述** Higress 是由阿里云开源的一款**云原生
  API 网关**。它基于 Envoy 和 Istio 构建，通过扩展 WebAssembly (WASM) 插件能力，旨在为 AI 原生应用、微服务架构及 Kubern'
external_url: https://github.com/alibaba/higress
scenarios:
- 云原生/容器
- 大语言模型
- Kubernetes
---

# 阿里开源 Higress：AI 原生 API 网关

---

## 基本信息

- **描述**: 🤖 AI 网关 | AI 原生 API 网关
- **语言**: Go
- **星标**: 7,743 (+7 stars today)
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

Higress 是基于 Istio 和 Envoy 构建的 AI 原生 API 网关，它通过 WebAssembly 插件扩展了云原生流量管理能力。该项目旨在解决大模型应用接入、AI Agent 工具集成以及微服务路由等场景下的统一治理问题。本文将梳理其系统架构，并重点介绍 AI 网关特性、MCP 系统托管机制以及 WASM 插件体系。

---

## 摘要

**Higress：基于 Istio 与 Envoy 的云原生 AI 网关**

**1. 项目概述**
Higress 是由阿里云开源的一款**云原生 API 网关**。它基于 Envoy 和 Istio 构建，通过扩展 WebAssembly (WASM) 插件能力，旨在为 AI 原生应用、微服务架构及 Kubernetes 集群提供统一的流量管理入口。该项目采用 Go 语言开发，目前 GitHub 星标数已超过 7,700。

**2. 核心架构**
Higress 采用**控制平面与数据平面分离**的架构设计：
*   **控制平面**：负责配置管理。
*   **数据平面**：负责流量处理。
*   **通信机制**：配置变更通过 **xDS 协议**传播，具有毫秒级延迟且无连接中断的特性。这使得它特别适用于 AI 流式响应等需要保持长连接的场景。

**3. 三大核心功能**
*   **AI 网关**
    *   **功能**：为大语言模型（LLM）应用提供统一 API，支持协议转换、可观测性、缓存及安全防护。
    *   **组件**：涵盖 `ai-proxy`（代理）、`ai-statistics`（统计）、`ai-cache`（缓存）和 `ai-security-guard`（安全守卫）等插件。
    *   **兼容性**：整合了 30+ 家 LLM 提供商。
*   **MCP 服务器托管**
    *   **功能**：托管**模型上下文协议 (MCP)** 服务器，使 AI Agent 能够便捷地调用外部工具和服务。
    *   **组件**：包含 `mcp-router` 和 `jsonrpc-converter` 过滤器，以及预置的 MCP 服务器实现（如 `quark-search`、`amap-tools`）。
*   **Kubernetes Ingress**
    *   **功能**：作为 K8s Ingress 控制器使用。
    *   **兼容性**：兼容 nginx-ingress 注解，支持微服务路由。

**总结**
Higress 不仅是一个传统的 API 网关，更是一个深度集成 AI 能力的基础设施。它通过 WASM 插件提供了极高的扩展性，能够同时满足现代化 AI 应用（LLM 接入、Agent 工

---

## 评论

**总体判断**

Higress 是目前云原生网关领域中将“AI 原生”理念落地最为彻底的开源项目之一。它不仅成功解决了传统 API 网关在处理 LLM（大语言模型）流量时的成本与协议适配痛点，更通过将 Istio 的控制面能力下沉，提供了一套兼具云原生弹性与 AI 应用特性的统一流量入口方案。

**深入评价分析**

**1. 技术创新性：从“流量搬运”到“流量理解与生成”的跨越**
*   **事实**：DeepWiki 提及 Higress 基于 Istio 和 Envoy 构建，并扩展了 WebAssembly (WASM) 插件能力，明确提出了“AI Gateway”和“MCP (Model Context Protocol) Server Hosting”功能。
*   **推断**：Higress 的核心差异化在于其 **“AI Native”** 架构。传统网关（如 Nginx, Kong）主要关注 L7 负载均衡，对 AI 流量是“盲”的。Higress 创新性地在网关层集成了 LLM 的语义理解能力，支持 Prompt 模板管理、Token 计费与流式响应处理。此外，引入 **MCP 协议支持**极具前瞻性，这使得网关不仅仅是数据的管道，更成为了 AI Agent（智能体）的工具调度中心，允许网关直接托管 Agent 所需的工具接口，这是对传统网关定位的重大突破。

**2. 实用价值：解决 LLM 落地的“最后一公里”成本与安全问题**
*   **事实**：描述中强调其提供“AI gateway features for LLM applications”及“traditional API gateway capabilities”。
*   **推断**：Higress 解决了企业接入大模型时的两个关键痛点：**成本与安全**。
    *   **成本优化**：通过在网关层实现多模型提供商（如 OpenAI, 通义千问等）的统一适配与切换，企业无需修改业务代码即可在不同模型间流转，利用竞价策略降低 API 调用成本。
    *   **安全与合规**：它充当了业务后端与公网 AI 服务之间的防火墙，可以在流量流出企业内网前进行敏感词过滤或 Prompt 注入防御。同时，它保留了 K8s Ingress 的传统功能，意味着企业可以用一个网关同时管理微服务流量和 AI 流量，极大地降低了运维复杂度。

**3. 代码质量与架构：云原生标准的高水位实现**
*   **事实**：项目基于 Go 语言开发，Star 数 7,743，架构上明确分离了控制面与数据面。
*   **推断**：背靠阿里巴巴，Higress 继承了集团内部治理大规模微服务流量（如双十一场景）的工程实践。其架构设计遵循了云原生的“控制面/数据面”分离标准，利用 Envoy 作为高性能数据平面保证了 C++ 的高吞吐，而控制面使用 Go 开发则保证了开发效率和可扩展性。WASM 插件系统的引入是代码质量的一个亮点，它允许开发者使用多种语言（C++, Go, Rust, JS）编写业务逻辑而无需重新编译网关，这极大地提升了系统的可维护性和定制化能力。

**4. 社区活跃度：从自用到开源的成熟期**
*   **事实**：Star 数量接近 8k，且 README 提供了中、日、英多语言版本。
*   **推断**：多语言文档表明该项目具有国际化的社区野心。作为阿里云开源的商业化产品（通常有对应的云产品 Higress），其代码更新频率和稳定性通常较高。相比纯个人项目，这类企业级开源项目通常有专门的 SRE 团队维护，Issue 响应和 Bug 修复速度有保障，但也可能存在企业内部逻辑与开源社区需求不同步的风险。

**5. 学习价值：理解“网关即服务”的最佳范本**
*   **事实**：项目涵盖了 Ingress 管理、WASM 插件开发、AI 协议扩展及 MCP 系统实现。
*   **推断**：对于开发者而言，Higress 是学习 **“如何将传统基础设施软件 AI 化”** 的绝佳案例。它展示了如何在 Envoy 这种高性能基础设施上扩展非 HTTP/1.1 协议（如 SSE 流式传输），以及如何设计插件系统以支持动态的逻辑扩展。研究其 MCP Server Hosting 的实现，有助于理解未来 AI Agent 时代的基础设施架构演变。

**6. 潜在问题与改进建议**
*   **推断**：
    *   **复杂度门槛**：基于 Istio 和 Envoy 的架构虽然强大，但对于没有云原生基础的小团队来说，运维和调试（尤其是 Envoy 的配置和 WASM 插件的调试）成本依然较高。
    *   **性能损耗**：在网关层进行 AI 请求的 Prompt 处理和 Token 计数，虽然方便，但在极高并发下可能会增加网关的 CPU 负担，需要权衡是在网关处理还是下沉到 Sidecar。
    *   **建议**：建议进一步简化 WASM 插件的开发体验，提供更可视化的 AI 流量编排界面，以降低非开发人员的使用门槛。

**7. 对比优势**
*   **对比 Kong/APISIX**：传统网关插件生态丰富，但对 AI 协议（SSE、不同厂商的 API 格式差异）支持较弱，通常需要编写复杂的 Lua/Go 插件来实现 Token 统计，而 Higress 将这些能力

---

## 技术分析

基于阿里巴巴开源的 Higress 仓库（AI Gateway | AI Native API Gateway），本文将从架构设计、核心功能、技术实现、适用场景、发展趋势及工程哲学等维度进行全面剖析。
