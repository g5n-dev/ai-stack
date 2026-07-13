---
title: 阿里开源 Higress：AI 原生 API 网关
date: 2026-03-07 22:28:45+08:00
draft: false
entry_kind: auto
tags:
- API 网关
- Higress
- AI 原生
- Istio
- Envoy
- WASM
- MCP
- Kubernetes
categories:
- 系统与基础设施
- 开源生态
source: github_trending
description: Higress 是阿里巴巴开源的一款**云原生 AI 原生 API 网关**。该项目基于 Go 语言开发，在 GitHub 上拥有超过 7,600
  颗星。它通过扩展 Istio 和 Envoy，并结合 WebAssembly (WASM) 插件能力，旨在为云原生应用和 AI 大模型应用提供统一的流量管理入口。
  **核心
external_url: https://github.com/alibaba/higress
scenarios:
- AI/ML项目
- 云原生/容器
- Kubernetes
---

# 阿里开源 Higress：AI 原生 API 网关

---

## 基本信息

- **描述**: 🤖 AI 网关 | AI 原生 API 网关
- **语言**: Go
- **星标**: 7,682 (+10 stars today)
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

Higress 是一款基于 Istio 和 Envory 构建的 AI 原生 API 网关，它通过云原生架构将传统流量管理与 LLM 应用支持相结合。该项目旨在解决微服务路由、Kubernetes Ingress 管理以及 AI Agent 工具集成等复杂场景下的统一接入问题。本文将梳理其系统架构与核心组件，并重点介绍 WASM 插件机制及 AI 网关特性的具体实现。

---

## 摘要

Higress 是阿里巴巴开源的一款**云原生 AI 原生 API 网关**。该项目基于 Go 语言开发，在 GitHub 上拥有超过 7,600 颗星。它通过扩展 Istio 和 Envoy，并结合 WebAssembly (WASM) 插件能力，旨在为云原生应用和 AI 大模型应用提供统一的流量管理入口。

**核心架构与特性：**

Higress 采用**控制平面与数据平面分离**的架构。配置变更通过 xDS 协议传播，具备毫秒级延迟且不中断连接，特别适用于 AI 流式响应等长连接场景。

**三大主要应用场景：**

1.  **AI 网关：**
    *   提供统一 API 接入，支持 30 多家主流 LLM 提供商。
    *   具备协议转换、可观测性、缓存和 AI 安全防护等功能（依赖 `ai-proxy`、`ai-statistics` 等插件）。
2.  **MCP 服务器托管：**
    *   托管模型上下文协议 (MCP) 服务器，使 AI Agents 能够便捷地调用工具和服务（如搜索、地图等）。
3.  **Kubernetes Ingress：**
    *   作为标准的 K8s Ingress 控制器运行，兼容 Nginx Ingress 注解，支持微服务路由。

---

## 评论

### 总体判断

Higress 是一款**极具前瞻性的云原生网关产品**，它成功地将**云原生流量治理**与**AI 原生应用需求**深度融合。作为阿里云开源的标杆项目，它不仅继承了 Istio/Envoy 的稳健底座，更通过 WASM 和 AI 特性的集成，为开发者提供了一个**“传统网关 + AI 网关 + MCP 服务器”**的统一入口，是构建 LLM 应用基础设施的理想选择。

---

### 深入评价维度

#### 1. 技术创新性：从“流量转发”到“模型推理编排”
*   **事实**：Higress 基于 Istio 和 Envoy 构建，核心扩展能力依赖于 WebAssembly (WASM)。同时，DeepWiki 明确指出其集成了 AI Gateway 功能和 MCP (Model Context Protocol) 服务器托管能力。
*   **推断**：传统网关（如 Nginx, Kong）主要关注 HTTP/TCP 转发，而 Higress 的创新在于**将“协议理解”提升到了“语义理解”层面**。
    *   **WASM 插件化架构**：这是其最大的技术亮点。不同于 Lua (Nginx) 或 Java (Zuul) 插件，WASM 提供了接近原生的性能且沙箱隔离，允许开发者使用 C++/Go/Rust/AssemblyScript 编写复杂逻辑，特别是针对 AI 请求的 Prompt 注入、敏感词过滤等，无需重启网关即可热更新。
    *   **AI Native 原生集成**：它不仅仅是一个反向代理，更理解 LLM 的流式输出协议。通过内置对 OpenAI 格式的兼容，它可以无缝对接各类大模型，解决了 AI 应用开发中模型切换复杂、Token 计费统计困难等痛点。
    *   **MCP 协议支持**：DeepWiki 提到的 MCP Server Hosting 是一个非常新的技术动向。这意味着 Higress 试图解决 AI Agent 的“工具调用”标准化问题，让网关成为 Agent 连接外部数据源和工具的统一枢纽。

#### 2. 实用价值：统一异构基础设施的关键一环
*   **事实**：README 提到它提供 Kubernetes Ingress、微服务路由以及 AI 网关功能。
*   **推断**：在微服务架构向 AI 应用演进的当下，企业往往面临维护两套网关的困境（一套管微服务，一套管大模型调用）。Higress 的实用价值在于**“融合”**：
    *   **降低运维复杂度**：用一套控制平面统一管理传统的 RPC 调用和新的 AI 推理流量。
    *   **AI 企业的降本增效**：对于 SaaS 企业，Higress 提供了基于 Token 的限流和计费能力，这是传统网关不具备的。它允许企业在网关层做“统一模型供应商切换”，例如当某个云厂商 API 不稳定时，通过网关配置毫秒级切换到备用模型，极大提升了系统的鲁棒性。

#### 3. 代码质量与架构：云原生工程化的典范
*   **事实**：项目使用 Go 语言编写，星标数 7,682，文档包含多语言版本（中/日/英）及详细的架构图。
*   **推断**：
    *   **架构清晰**：控制平面与数据平面分离是标准云原生设计。Higress 在 Envoy 之上做了一层非常薄的抽象，既利用了 Envoy 高性能的 C++ 网络 I/O，又利用 Go 语言在控制逻辑上的开发效率。
    *   **工程规范**：作为阿里系开源项目，其代码结构通常遵循严格的 Go 惯例，接口抽象设计良好。DeepWiki 提到的“Development Guide”和详细的 README 表明项目重视文档和开发者体验，这对于降低上手门槛至关重要。

#### 4. 社区活跃度：头部背书，生态健康
*   **事实**：GitHub 星标数超过 7.6k，背靠阿里巴巴，且 README 拥有日语版本，显示出国际化意图。
*   **推断**：在 API Gateway 领域，这是一个非常高的关注度，仅次于 Kong 和 APISIX。阿里巴巴的背书意味着该项目**不是“玩具级”项目**，而是经过双十一等超大规模流量验证的工业级产品。社区活跃度通常较高，Issue 响应及时，且国内开发者对中文文档的友好度极高，形成了良好的正向循环。

#### 5. 学习价值：理解 WASM 与 AI 流量治理的窗口
*   **推断**：对于开发者而言，Higress 是学习**“如何将 WASM 运用于生产环境”**的最佳案例之一。
    *   你可以研究它是如何通过 `proxy-wasm` 规范在 Go 中编写插件并编译为 `.wasm` 文件的。
    *   它是学习**“AI 网关模式”**（如 Prompt 模板管理、上下文缓存策略）的实战教材。对于想要转型 AI 基础设施开发的工程师，阅读其源码能快速理解 LLM 流式传输在网关层的处理细节。

#### 6. 潜在问题与改进建议
*   **推断**：
    *   **复杂度曲线**：引入 Istio 和 Envoy 使得架构相对重型。对于只有几个后端服务的简单 AI 应用，Higress 可能显得过于厚重，部署和调优的学习成本高于简单的 Nginx 反向代理。
    *   **WASM 的冷启动**：虽然

---

## 技术分析

以下是对阿里巴巴开源的 **Higress** 仓库的深度技术分析。

---

### Higress 深度技术分析报告
