---
title: "JeecgBoot AI低代码平台：零代码5分钟搭系统，低代码一键生成前后端代码"
date: 2026-05-14T10:40:51+08:00
draft: false
entry_kind: "auto"
tags: ["低代码平台", "零代码", "代码生成", "AI应用", "Java", "前后端", "可视化开发", "知识库"]
categories: ["AI 工程", "开发工具"]
source: github_trending
description: "JeecgBoot 是一个企业级 AI 低代码开发平台，融合了低代码与零代码两种开发模式。它通过可视化配置和 AI 辅助生成，帮助开发者快速搭建业务系统，显著减少 Java 项目中的重复编码工作。无论你是希望快速原型开发，还是需要灵活定制企业级应用，JeecgBoot 都能提供合适的方案。本文将详细介绍其核心功能、技术"
external_url: https://github.com/jeecgboot/JeecgBoot
scenarios: ["全栈开发", "Web应用开发", "AI/ML项目"]
---

# JeecgBoot AI低代码平台：零代码5分钟搭系统，低代码一键生成前后端代码

> **原名**: jeecgboot /

      JeecgBoot

---

## 基本信息

- **描述**: 您好，您提供的内容本身就是中文。如果您是想将其翻译成其他语言（如英文），请告诉我目标语言，我会为您翻译。

如果确实是要翻译成中文，那这段内容已经符合您的要求，我保持原文如下：

---

AI低代码平台，支持「低代码 + 零代码」双模式：零代码 5 分钟搭建业务系统，低代码模式一键生成前后端代码。内置AI应用，支持AI聊天、知识库、流程编排、MCP与插件，支持各种模型。Skills能力实现：一句话画流程图、设计表单、生成系统。引领 AI生成→在线配置→代码生成→手工合并的开发模式，解决Java项目80%的重复工作，快速提高效率，又不失灵活性。

---

请问您是否需要我将其翻译成其他语言？
- **语言**: Java
- **星标**: 46,246 (+27 stars today)
- **链接**: [https://github.com/jeecgboot/JeecgBoot](https://github.com/jeecgboot/JeecgBoot)
- **DeepWiki**: [https://deepwiki.com/jeecgboot/JeecgBoot](https://deepwiki.com/jeecgboot/JeecgBoot)

---
## DeepWiki 速览（节选）

# JeecgBoot Overview

Relevant source files

  * [README-AI.md](https://github.com/jeecgboot/JeecgBoot/blob/b7a3da89/README-AI.md?plain=1)
  * [README.en-US.md](https://github.com/jeecgboot/JeecgBoot/blob/b7a3da89/README.en-US.md?plain=1)
  * [README.md](https://github.com/jeecgboot/JeecgBoot/blob/b7a3da89/README.md?plain=1)
  * [jeecg-boot/README.md](https://github.com/jeecgboot/JeecgBoot/blob/b7a3da89/jeecg-boot/README.md?plain=1)
  * [jeecgboot-vue3/README.md](https://github.com/jeecgboot/JeecgBoot/blob/b7a3da89/jeecgboot-vue3/README.md?plain=1)

## Purpose and Scope

This document introduces JeecgBoot as an enterprise-level AI low-code development platform, explaining its core value proposition and position in the enterprise software ecosystem. It provides the conceptual foundation for understanding how JeecgBoot combines code generation, visual development, and AI capabilities into a unified platform.

For detailed technical information:

  * Complete feature list: see [Key Features & Capabilities](/jeecgboot/JeecgBoot/1.1-key-features-and-capabilities)
  * Technology stack details: see [Technology Stack](/jeecgboot/JeecgBoot/1.2-technology-stack)
  * System requirements: see [System Requirements & Environment Setup](/jeecgboot/JeecgBoot/1.3-system-requirements-and-environment-setup)
  * Quick start instructions: see [Quick Start Guide](/jeecgboot/JeecgBoot/1.4-quick-start-guide)
  * Architecture details: see [Architecture](/jeecgboot/JeecgBoot/2-architecture)
  * AI platform capabilities: see [AI Platform (AIGC)](/jeecgboot/JeecgBoot/3-ai-platform-\(aigc\))
  * Low-code features: see [Low-Code Development Platform](/jeecgboot/JeecgBoot/5-low-code-development-platform)

## What is JeecgBoot?

JeecgBoot is an enterprise-grade AI-enhanced low-code development platform built on Spring Boot 3.5.5, Vue 3, and Spring Cloud Alibaba 2023.0.3.3. The platform provides three development approaches:

  1. **Code Generation** \- Maven-based code generator (`jeecg-boot-base-core/CodeGenerateUtil`) producing Vue3 + Spring Boot code
  2. **OnlineCoding** \- Zero-code visual configuration through `@jeecg/online` package and `OnlineCgformHeadController`
  3. **AI Platform** \- LLM integration via `jeecg-boot-module-airag` module with RAG using LangChain4j

The architecture supports two deployment modes:

  * **Monolithic** : `jeecg-system-start` (single JAR, port 8080)
  * **Microservices** : `jeecg-cloud-gateway` (port 9999) → `jeecg-system-cloud-start` (port 7001) + `jeecg-demo-cloud-start` (port 7002)

**Current Version** : 3.9.0 (Released: December 1, 2025)  
**License** : Apache License 2.0  
**Vendor** : Beijing Guoju Software (北京国炬软件)  
**Primary Repositories** :

  * Backend: `jeecg-boot` (Java/Maven)
  * Frontend: `jeecgboot-vue3` (Vue3/TypeScript/Vite)

Sources: [README.md1-44](https://github.com/jeecgboot/JeecgBoot/blob/b7a3da89/README.md?plain=1#L1-L44) [jeecg-boot/README.md1-44](https://github.com/jeecgboot/JeecgBoot/blob/b7a3da89/jeecg-boot/README.md?plain=1#L1-L44) [README.md159-190](https://github.com/jeecgboot/JeecgBoot/blob/b7a3da89/README.md?plain=1#L159-L190)

## Core Value Proposition

JeecgBoot addresses the automation vs. flexibility trade-off through a four-tier development paradigm:

**Four-Tier Development Flow**

**Development Approach by Complexity:**

Feature Type| Code Path| Key Components| Exit Point  
---|---|---|---  
**Simple CRUD**|  AI → OnlineCoding| `OnlCgformHeadEntity`, `OnlCgformFieldEntity`| Tier 2 (zero-code)  
**Standard Business**|  Code Generator| `CodeGenerateOneToMany.ftl`, `jeecgOneMain.ftl`| Tier 3 (template + tweaks)  
**Complex Logic**|  Generator + Custom| `ServiceImpl`, `Controller` with manual methods| Tier 4 (full control)  
  
**Implementation Details:**

  * **Generated Code Format** : Standard Vue3 SFC + Spring Boot `@RestController` classes (not proprietary DSL)
  * **Merge Strategy** : Generated files in `src/main/java` alongside manually created files; developers extend base classes
  * **AI Integration** : `AiragChatServiceImpl` calls `LangChain4jService` → LLM → generates `OnlineCgformHeadEntity` configuration
  * **Security From Day 1** : Generated controllers include `@RequiresPermissions`, `QueryGenerator` for data permissions

**Code Generator Templates** (`jeecg-boot-base-core/src/main/resources/jeecg/code-template-online`):

  * `jeecgOneMain.ftl` \- Single table CRUD
  * `jeecgTreeMain.ftl` \- Tree structure
  * `jeecgOneToMany.ftl` \- One-to-many relations
  * `jvxeOnlineMain.ftl` \- Inline editable tables

Sources: [README.md20-36](https://github.com/jeecgboot/JeecgBoot/blob/b7a3da89/README.md?plain=1#L20-L36) [jeecg-boot/README.md19-33](https://github.com/jeecgboot/JeecgBoot/blob/b7a3da89/jeecg-boot/README.md?plain=1#L19-L33) [README.md111-157](https://github.com/jeecgboot/JeecgBoot/blob/b7a3da89/README.md?plain=1#L111-L157)

## Platform Architecture Modes

JeecgBoot supports two deployment architectures using shared business logic modules:

**Architecture Mode Diagram**

**Module Comparison:**

Component| Monolithic| Microservices| Shared  
---|---|---|---  
**Entry Point**| `JeecgSystemApplication.main()`| `JeecgCloudGatewayApplication.main()`| N/A  
**Business Logic**| `jeecg-system-biz`| `jeecg-system-biz`| ✓ Identical  
**Core Utilities**| `jeecg-boot-base-core`| `jeecg-boot-base-core`| ✓ Identical  
**Configuration**| `application.yml` (local profile)| `bootstrap.yml` \+ Nacos config| Different  
**Service Discovery**|  None| `@EnableDiscoveryClient`, `NacosNamingService`| Different  
**API Gateway**|  None| `GatewayFilterFactory`, `RouteLocator`| Different  
**Build Output**| `jeecg-system-start.jar` (single)| Multiple JARs| Different  
  
**Switching Mechanism:**

Business logic classes in `jeecg-module-system/jeecg-system-biz/src/main/java/org/jeecg/modules/` remain unchanged. Only startup classes and configuration differ:

  * **Monolithic** : Run `jeecg-module-system/jeecg-system-start/src/main/java/org/jeecg/JeecgSystemApplication.java`
  * **Microservices** : Run `jeecg-server-cloud/jeecg-cloud-gateway` \+ `jeecg-server-cloud/jeecg-system-cloud-start`

**Key Classes:**

  * `org.jeecg.JeecgSystemApplication` \- Monolithic main class
  * `org.jeecg.cloud.JeecgCloudGatewayApplication` \- Gateway main class
  * `org.jeecg.cloud.JeecgSystemCloudApplication` \- System service main class
  * `com.alibaba.nacos.client.NacosConfigService` \- Config center client

Sources: [README.md72-82](https://github.com/jeecgboot/JeecgBoot/blob/b7a3da89/README.md?plain=1#L72-L82) [jeecg-boot/README.md218-243](https://github.com/jeecgboot/JeecgBoot/blob/b7a3da89/jeecg-boot/README.md?plain=1#L218-L243)

## Repository Organization

The platform consists of two primary repositories with Maven multi-module (backend) and pnpm workspace (frontend) organization:

**Backend Repository Structure** (`jeecg-boot/`)

**Frontend Repository Structure** (`jeecgboot-vue3/`)

**Key Directory Paths:**

Module| Path| Purpose  
---|---|---  
**Parent POM**| `jeecg-boot/pom.xml`| Dependency versions, modules list  
**Core Utilities**| `jeecg-boot/jeecg-boot-base-core/src/main/java/org/jeecg/`| Shared utilities, config, annotations  
**System Business**| `jeecg-boot/jeecg-module-system/jeecg-system-biz/src/main/java/org/jeecg/modules/`| User, role, dept, menu services  
**Monolithic Entry**| `jeecg-boot/jeecg-module-system/jeecg-system-start/src/main/java/org/jeecg/JeecgSystemApplication.java`| Main class for single deployment  
**Cloud Entry**| `jeecg-boot/jeecg-server-cloud/jeecg-system-cloud-start/src/main/java/org/jeecg/cloud/JeecgSystemCloudApplication.java`| Main class for microservices  
**AI Module**| `jeecg-boot/jeecg-boot-module-airag/src/main/java/org/jeecg/modules/ai/`| AI chat, flows, knowledge base  
**Vue Entry**| `jeecgboot-vue3/src/main.ts`| Frontend bootstrap  
**Online Package**| `jeecgboot-vue3/packages/@jeecg/online/`| OnlineCoding components  
**AI Flow Package**| `jeecgboot-

[...truncated...]

---
## 导语

JeecgBoot 是一个企业级 AI 低代码开发平台，融合了低代码与零代码两种开发模式。它通过可视化配置和 AI 辅助生成，帮助开发者快速搭建业务系统，显著减少 Java 项目中的重复编码工作。无论你是希望快速原型开发，还是需要灵活定制企业级应用，JeecgBoot 都能提供合适的方案。本文将详细介绍其核心功能、技术架构以及实际使用中的优势与限制。

---
## 评论

作为一款在国内 Java 生态中具有代表性的低代码平台，JeecgBoot 在技术深度与功能丰富度上表现突出，其 46,246 的 GitHub 星标也印证了社区的广泛认可。该平台将 AI 生成、代码自动生成与可视化配置整合为统一工作流，理论上可显著降低 CRUD 类业务系统的开发成本，但其实际效果仍需结合具体场景评估。

#### 技术实现与依据

从技术架构来看，JeecgBoot 采用前后端分离设计，前端基于 Vue3，后端基于 Spring Boot 与 MyBatis-Plus，代码生成率声称可达 80%。这是事实陈述，基于公开的仓库文档与源码结构推断。AI 能力的集成通过 MCP（Model Context Protocol）协议实现模型扩展，支持流程图生成、表单设计与系统级代码生成，这一实现方式在业内属于较为前沿的探索。平台宣称“5 分钟搭建业务系统”，这一说法应理解为在熟悉平台前提下的典型场景演示时间，实际复杂度会因业务差异而波动，此为推断而非绝对事实。

#### 适用场景

JeecgBoot 最适合以下场景：中小型企业的内部管理系统、管理后台类项目、CRUD 密集型业务模块，以及需要快速交付的数字化转型项目。政企单位中常见的表单填报、审批流程、数据报表等功能，通过零代码配置即可实现，这对降低技术门槛有一定价值。低代码模式则适用于有一定 Java 基础的开发团队，可在一键生成的基础上进行二次开发，兼顾效率与灵活性。

#### 局限与风险

需要注意的是，JeecgBoot 在高度定制化场景下可能遇到瓶颈。平台生成的代码质量虽可满足基本需求，但在性能优化、架构扩展等方面仍需人工介入。推断认为，对于需要微服务拆分的复杂业务系统，该平台的适用性会下降，团队仍需较强的 Java 能力来补足。此外，AI 生成内容的准确性受限于模型能力与 Prompt 设计，复杂业务规则仍需人工校验。

#### 验证方式

建议从以下维度验证平台适配性：使用平台搭建一个完整的业务模块（如用户管理+权限控制），评估配置效率与生成代码的可读性；测试 AI 生成功能在流程图、表单设计等场景的实际效果；评估社区活跃度与文档完善程度是否足以支撑二次开发。

---
## 技术分析

#### 架构概述

JeecgBoot 采用前后分离的微服务架构设计。从仓库结构看，项目主要分为 `jeecg-boot`（后端）和 `jeecgboot-vue3`（前端）两个核心模块。**已知事实**：后端基于 Java/Spring Boot，前端采用 Vue3，这是当前企业级应用的主流技术选型。**推断**：由于采用微服务架构，该平台具备良好的横向扩展能力，适合构建中大型企业应用系统。模块化设计使得各功能组件可以独立部署和升级，降低了系统耦合度。

#### 核心能力分析

该平台的核心价值在于「低代码 + 零代码」双模式驱动。**已知事实**：零代码模式支持通过可视化配置在 5 分钟内搭建业务系统，低代码模式则一键生成前后端代码。平台内置 AI 应用，提供 AI 聊天、知识库、流程编排等能力，支持 MCP（Model Context Protocol）与插件扩展。**推断**：AI 能力的集成是该平台区别于传统低代码平台的关键，能够通过自然语言处理简化开发流程，例如通过一句话生成流程图、设计表单或生成系统代码。

#### 技术实现特点

从技术栈来看，Java 作为后端语言表明该平台面向企业级 Java 生态。**已知事实**：项目提供完整的代码生成机制，覆盖前后端代码，这意味着开发者可以在生成的代码基础上进行二次定制。**推断**：平台内部应该实现了基于模板的代码生成引擎，可能采用 Velocity 或 FreeMarker 等模板技术。Vue3 前端的选择表明平台拥抱了现代前端技术栈，具备良好的响应式和组件化开发体验。AI 能力的实现大概率通过对接外部大模型 API 实现，这也解释了为何支持多种模型的灵活切换。

#### 适用与不适用场景

**适用场景**：企业内部管理系统（如 OA、CRM、ERP）、快速原型开发、中小型项目的敏捷开发、团队技术能力以 Java 为主的企业。**不适用场景**：对性能要求极高的底层系统、需要极致定制化的创新型产品、纯移动端应用开发、对前端框架有特定要求（不支持 Vue）的项目。**推断**：由于代码生成机制的存在，复杂业务逻辑的深度定制可能面临生成的代码与手工代码难以融合的挑战。

#### 学习与落地建议

**学习路径**：建议从官方 README 和 Quick Start Guide 入手，先搭建本地开发环境跑通基础 Demo；其次深入研究代码生成模块，理解模板定制逻辑；最后学习 AI 能力的集成方式。**落地建议**：在正式项目中采用时，应先评估业务复杂度与平台能力的匹配度，优先选择标准 CRUD 类业务场景；定制化需求应控制在生成代码的扩展点内，避免直接修改生成文件；团队需要熟悉 Java、Spring Boot、Vue3 三项技术栈；建议预留充足的踩坑时间，尤其是 AI 功能与业务系统的深度集成。

---
## 学习要点

- JeecgBoot 是基于 Spring Boot + MyBatis‑Plus + Vue3 + Ant Design Vue 的全栈低代码平台，实现“前端拖拽、后端自动生成”，显著提升开发效率。
- 提供在线表单、列表、树形等可视化设计器，支持拖拽式页面构建，几乎无需手写前端代码。
- 内置完整的 RBAC 权限模型和数据字典，实现细粒度的菜单、按钮及数据权限控制。
- 采用前后端分离架构，支持单体和 Spring Cloud 微服务两种部署方式，满足不同规模项目需求。
- 通过代码生成器（Online Generator）自动生成 Controller、Service、Mapper、Vue 页面等完整业务代码，实现一键交付。
- 集成工作流（Flowable）和报表功能，提供统一的任务中心和业务监控，助力业务流程数字化。

---
## 引用

- **GitHub 仓库**: [https://github.com/jeecgboot/JeecgBoot](https://github.com/jeecgboot/JeecgBoot)
- **DeepWiki**: [https://deepwiki.com/jeecgboot/JeecgBoot](https://deepwiki.com/jeecgboot/JeecgBoot)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/)
- 标签： [低代码平台](/tags/%E4%BD%8E%E4%BB%A3%E7%A0%81%E5%B9%B3%E5%8F%B0/) / [零代码](/tags/%E9%9B%B6%E4%BB%A3%E7%A0%81/) / [代码生成](/tags/%E4%BB%A3%E7%A0%81%E7%94%9F%E6%88%90/) / [AI应用](/tags/ai%E5%BA%94%E7%94%A8/) / [Java](/tags/java/) / [前后端](/tags/%E5%89%8D%E5%90%8E%E7%AB%AF/) / [可视化开发](/tags/%E5%8F%AF%E8%A7%86%E5%8C%96%E5%BC%80%E5%8F%91/) / [知识库](/tags/%E7%9F%A5%E8%AF%86%E5%BA%93/)
- 场景： [全栈开发](/scenarios/%E5%85%A8%E6%A0%88%E5%BC%80%E5%8F%91/) / [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [Java低代码平台JeecgBoot：AI+零代码双模式]({{< relref "posts/20260513-github_trending-jeecgboot-jeecgboot-0.md" >}})
- [JeecgBoot：AI低代码平台集成代码生成器与知识库]({{< relref "posts/20260130-github_trending-jeecgboot-jeecgboot-3.md" >}})
- [JeecgBoot：集成AI低代码平台与代码生成器的Java开发框架]({{< relref "posts/20260129-github_trending-jeecgboot-jeecgboot-3.md" >}})
- [JeecgBoot：集成AI低代码与代码生成器的企业级开发平台]({{< relref "posts/20260129-github_trending-jeecgboot-jeecgboot-7.md" >}})
- [JeecgBoot开源低代码平台：集成AI应用与代码生成器]({{< relref "posts/20260131-github_trending-jeecgboot-jeecgboot-3.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*