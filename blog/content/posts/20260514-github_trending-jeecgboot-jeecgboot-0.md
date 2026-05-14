---
title: "JeecgBoot Java低代码平台：AI辅助前后端代码生成"
date: 2026-05-14T04:30:22+08:00
draft: false
entry_kind: "auto"
tags: ["低代码平台", "代码生成", "Java", "Vue3", "微服务", "AI辅助开发", "Spring Cloud", "开发效率"]
categories: ["开发工具", "AI 工程"]
source: github_trending
description: "项目定位 JeecgBoot是一款企业级AI增强的低代码开发平台，基于Spring Boot 3.5.5、Vue 3和Spring Cloud Alibaba 2023.0.3.3构建。平台旨在通过“AI生成→在线配置→代码生成→手工合并”的开发模式，解决Java项目80%的重复工作，在快速提高开发效率的同时保持灵活性"
external_url: https://github.com/jeecgboot/JeecgBoot
scenarios: ["全栈开发", "后端开发", "AI/ML项目"]
---

# JeecgBoot Java低代码平台：AI辅助前后端代码生成

> **原名**: jeecgboot /

      JeecgBoot

---

## 基本信息

- **描述**: # 英译版本 / English Translation

以下是英文翻译：

---

AI Low-Code Platform, supporting "Low-Code + No-Code" dual modes: Build business systems in 5 minutes with No-Code, and generate frontend and backend code with one click using Low-Code mode. Built-in AI applications supporting AI chat, knowledge base, process orchestration, MCP and plugins, compatible with various models. Skills capabilities: Draw flowcharts, design forms, and generate systems with a single sentence. Leading the development paradigm of AI Generation → Online Configuration → Code Generation → Manual Merging, solving 80% of repetitive work in Java projects, dramatically improving efficiency while maintaining flexibility.

---

如果您需要其他语言的翻译，或对这段中文进行润色/优化，请告诉我！
- **语言**: Java
- **星标**: 46,235 (+27 stars today)
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

JeecgBoot 是一个基于 Java 的企业级 AI 低代码平台，提供“低代码+无代码”双开发模式。无代码模式支持通过可视化拖拽快速搭建业务系统，低代码模式则能一键生成前后端代码，减少重复编码工作。平台内置 AI 助手，支持流程图绘制、表单设计和自然语言生成系统等功能，兼容多种大模型。

本文将介绍 JeecgBoot 的核心功能、技术架构以及实际应用场景，帮助开发者快速评估其在项目中的适用性。

---
## 摘要

#### 项目定位

JeecgBoot是一款企业级AI增强的低代码开发平台，基于Spring Boot 3.5.5、Vue 3和Spring Cloud Alibaba 2023.0.3.3构建。平台旨在通过“AI生成→在线配置→代码生成→手工合并”的开发模式，解决Java项目80%的重复工作，在快速提高开发效率的同时保持灵活性。

#### 核心特性

该平台支持“低代码+零代码”双模式运营。零代码模式下，用户可在5分钟内通过可视化操作搭建业务系统，无需编写代码；低代码模式则提供一键生成前后端代码的能力，大幅降低开发门槛。

平台内置AI应用模块，支持AI聊天、知识库、流程编排、MCP与插件等功能，并兼容多种大语言模型。AI能力体现在多个方面：通过一句话即可生成流程图、设计表单、生成系统框架，真正实现“所言即所得”的智能开发体验。

#### 技术架构

作为纯Java技术栈项目，JeecgBoot采用主流的微服务架构，核心技术包括Spring Boot后端框架、Vue 3前端框架以及Spring Cloud Alibaba微服务组件。平台提供三大开发路径：代码生成、可视化配置和AI智能开发，满足不同技术能力团队的需求。

#### 开源现状

截至目前，该项目在GitHub上已获得46,235个星标，显示出极高的社区关注度和市场认可度。丰富的功能特性与活跃的社区支持使其成为企业级低代码平台的重要选择之一。

---
## 评论

#### 总体判断
JeecgBoot 是目前国内活跃度较高的企业级低代码平台，兼具零代码和低代码双模式，46 k+星标和持续更新的生态表明其在社区和商业项目中拥有一定的认可度。技术实现基于 Spring Boot + Vue3，集成 AI 生成能力，适合快速构建 CRUD 为主的中后台系统。

#### 依据与技术要点
- **事实**：采用 Java 主流技术栈，前端基于 Vue3，后端提供 REST、Swagger、ShardingSphere 等组件；内置代码生成、在线表单、流程引擎等功能。
- **推断**：AI 能力（如对话、流程图生成）基于大模型封装，理论上能降低页面和接口的重复编写成本，但对复杂业务规则仍需手工介入。

#### 适用场景
- 需要快速交付内部管理系统或运维平台的中小企业。
- 业务模型相对固定、以增删改查为主且对 UI 要求不高的项目。
- 团队成员熟悉 Spring/Spring Boot、Vue，能够在生成代码基础上进行二次开发。

#### 局限与风险
- **事实**：官方强调“解决 80% 重复工作”，但并未提供量化基准，实际效率提升取决于业务复杂度。
- **推断**：随着项目规模增长，生成代码的维护成本可能上升，尤其在多租户、细粒度权限等高级特性上需要额外扩展。
- AI 生成功能依赖外部模型服务，网络或模型更新会影响可用性。

#### 验证方式
1. **原型验证**：在本地搭建最小化示例，使用零代码模式快速生成 CRUD 页面，评估表单布局、校验规则的灵活性。
2. **代码审计**：抽取生成的 Controller、Service、Mapper，对比是否符合团队代码规范，检测是否存在隐藏的潜在安全风险（如 SQL 注入、权限绕过）。
3. **性能基准**：在高并发场景下，使用 JMeter 或 Gatling 模拟请求，观察生成的代码在数据库连接池、缓存使用上的表现。
4. **社区反馈**：检索 GitHub Issues、Stack Overflow 以及国内技术社区的实际项目案例，获取真实用户的维护经验和痛点。

通过上述步骤可较为客观地判断 JeecgBoot 是否满足特定项目的技术要求和交付周期。

---
## 技术分析

#### 架构特点

该平台采用经典的前后端分离架构，前端基于 Vue3 生态构建，后端采用 Spring Boot 框架。从仓库结构来看，主要包含 `jeecg-boot`（后端模块）和 `jeecgboot-vue3`（前端模块）两个核心部分。这种模块化设计便于前后端独立开发和部署，同时为后续的微服务拆分奠定了基础。

##### 微服务支持能力

从已有信息推断，后端采用 Spring Cloud Alibaba 技术栈的可能性较大，预计包含 Nacos（配置中心与服务发现）、Sentinel（流量控制）等组件。这使得系统能够支持分布式部署场景，满足中大型企业的业务需求。

#### 核心能力实现

##### AI 驱动的代码生成

内置的代码生成器是该平台的核心竞争力，能够根据数据库表结构一键生成前后端代码，覆盖 Controller、Service、Mapper 以及 Vue 页面代码。这一机制有效减少了 CRUD 操作的重复劳动。

##### 零代码业务配置

提供可视化的表单设计和流程编排能力，用户无需编写代码即可搭建业务表单、配置审批流程。从描述来看，还支持"一句话画流程图"等 AI 辅助功能，降低了业务人员的使用门槛。

##### 多模型 AI 集成

平台支持接入多种 AI 模型，具备聊天机器人、知识库、流程编排等 AI 应用能力，并支持 MCP（Model Context Protocol）协议和插件扩展，显示出较强的 AI 能力开放性。

#### 技术实现亮点

从已有信息判断，后端主要采用 MyBatis-Plus 作为 ORM 框架，提供便捷的 CRUD 操作支持。前端则使用 Element Plus 组件库，结合 Vue3 的 Composition API 实现响应式界面。代码生成器采用模板引擎技术，通过预定义模板适配不同业务场景。

#### 适用场景

内部管理系统开发是首选场景，包括 OA、CRM、ERP 等企业级应用。适用于业务需求变化频繁、迭代周期紧张的项目。对于技术团队规模有限但需要快速交付 MVP 的创业项目同样具有价值。此外，AI 能力集成使其适合需要智能辅助功能的业务流程自动化场景。

#### 不适用场景

对于性能要求极高的实时交易系统、并发量巨大的互联网平台，该架构可能难以胜任。高度定制化的技术架构需求、复杂的领域特定逻辑（如金融交易规则、医疗影像处理）也不适合采用此类通用低代码平台。追求极致灵活性和完全自主可控的高端项目可能面临平台约束。

#### 学习与落地建议

##### 学习路径

建议先从代码生成机制入手，理解模板引擎的运作原理。再深入研究前端组件库和后端服务架构，掌握整体技术脉络。AI 能力部分可作为进阶内容，根据实际业务需求选择性学习。

##### 落地策略

建议从边缘业务模块或新项目试点开始，逐步积累经验后再向核心系统推广。落地过程中应重点关注代码合并策略和版本管理机制，确保低代码生成的代码与原有代码体系良好融合。同时需建立团队的低代码使用规范，避免过度依赖平台导致的架构耦合。

---
## 学习要点

- JeecgBoot 是一个开源的低代码平台，能够显著提升企业级应用的开发效率。
- 平台采用前后端分离架构，后端基于 Spring Boot，前端使用 Vue 并提供丰富的 UI 组件库。
- 通过代码生成器和在线配置功能，实现业务模型的快速建模和一键生成前后端代码。
- 内置权限管理、工作流、表单设计等企业级功能，支持微服务部署和多数据源切换。
- 项目在 GitHub Trending 上榜，体现了社区活跃度和广泛的开发者关注。
- 采用插件化设计，开发者可以灵活扩展业务模块，保持系统的可维护性与可扩展性。
- 提供完善的中文文档和技术社区支持，便于国内团队快速上手和二次开发。

---
## 引用

- **GitHub 仓库**: [https://github.com/jeecgboot/JeecgBoot](https://github.com/jeecgboot/JeecgBoot)
- **DeepWiki**: [https://deepwiki.com/jeecgboot/JeecgBoot](https://deepwiki.com/jeecgboot/JeecgBoot)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [低代码平台](/tags/%E4%BD%8E%E4%BB%A3%E7%A0%81%E5%B9%B3%E5%8F%B0/) / [代码生成](/tags/%E4%BB%A3%E7%A0%81%E7%94%9F%E6%88%90/) / [Java](/tags/java/) / [Vue3](/tags/vue3/) / [微服务](/tags/%E5%BE%AE%E6%9C%8D%E5%8A%A1/) / [AI辅助开发](/tags/ai%E8%BE%85%E5%8A%A9%E5%BC%80%E5%8F%91/) / [Spring Cloud](/tags/spring-cloud/) / [开发效率](/tags/%E5%BC%80%E5%8F%91%E6%95%88%E7%8E%87/)
- 场景： [全栈开发](/scenarios/%E5%85%A8%E6%A0%88%E5%BC%80%E5%8F%91/) / [后端开发](/scenarios/%E5%90%8E%E7%AB%AF%E5%BC%80%E5%8F%91/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [Java低代码平台JeecgBoot：AI+零代码双模式]({{< relref "posts/20260513-github_trending-jeecgboot-jeecgboot-0.md" >}})
- [Claude Code团队AI插件实践：从新人到全栈自动化的渐进指南]({{< relref "posts/20260426-juejin-告别重复劳动一套插件让-ai-替你写代码修bug做测试上生产-0.md" >}})
- [JeecgBoot：集成AI低代码平台与代码生成器的Java开发框架]({{< relref "posts/20260129-github_trending-jeecgboot-jeecgboot-3.md" >}})
- [JeecgBoot：集成AI低代码与代码生成器的企业级开发平台]({{< relref "posts/20260129-github_trending-jeecgboot-jeecgboot-7.md" >}})
- [构建极简编程代理的技术实践与经验总结]({{< relref "posts/20260201-hacker_news-what-i-learned-building-an-opinionated-and-minimal-17.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*