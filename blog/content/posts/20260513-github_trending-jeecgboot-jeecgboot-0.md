---
title: "Java AI低代码平台JeecgBoot：零代码5分钟搭建"
date: 2026-05-13T16:01:55+08:00
draft: false
entry_kind: "auto"
tags: ["低代码", "零代码", "Java", "AI开发", "代码生成器", "SpringBoot", "Vue3", "企业级"]
categories: ["开发工具", "后端"]
source: github_trending
description: "JeecgBoot是一个基于Spring Boot 3.5.5、Vue 3和Spring Cloud Alibaba 2023.0.3.3构建的企业级AI增强低代码开发平台，采用「低代码+零代码」双模式设计，支持AI应用集成，能够自动化处理大量重复性开发工作。 核心特性 该平台提供三种主要开发方法：基于Maven的代码"
external_url: https://github.com/jeecgboot/JeecgBoot
scenarios: ["后端开发", "全栈开发", "Web应用开发"]
---

# Java AI低代码平台JeecgBoot：零代码5分钟搭建

> **原名**: jeecgboot /

      JeecgBoot

---

## 基本信息

- **描述**: 您好，您提供的这段内容本身已经是中文（简体中文）。

以下是该内容的格式化呈现：

---

**AI低代码平台**

支持「低代码 + 零代码」双模式：

- **零代码**：5 分钟搭建业务系统
- **低代码**：一键生成前后端代码

**内置AI 应用**：

- AI 聊天
- 知识库
- 流程编排
- MCP 与插件
- 支持各种模型

**Skills 能力实现**：

- 一句话画流程图
- 设计表单
- 生成系统

**引领开发新模式**：

AI 生成 → 在线配置 → 代码生成 → 手工合并

解决 Java 项目 80% 的重复工作，快速提高效率，又不失灵活性。

---

如果您是想翻译成**繁体中文**或其他语言，请告诉我，我随时为您服务。
- **语言**: Java
- **星标**: 46,225 (+28 stars today)
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

这是一个企业级AI低代码开发平台，采用Java技术栈。它同时支持低代码和零代码两种开发模式，零代码模式下可以通过可视化配置快速搭建业务系统，低代码模式则能一键生成前后端代码。项目内置了AI聊天、知识库、流程编排等多项智能能力，并支持多种大模型接入。开发者可以通过自然语言描述需求，自动生成流程图、表单和系统框架。该平台主要面向需要快速交付企业级应用的开发团队，能够显著减少Java项目中的重复编码工作，同时保留足够的灵活性供手工调整和扩展。

---
## 摘要

JeecgBoot是一个基于Spring Boot 3.5.5、Vue 3和Spring Cloud Alibaba 2023.0.3.3构建的企业级AI增强低代码开发平台，采用「低代码+零代码」双模式设计，支持AI应用集成，能够自动化处理大量重复性开发工作。

#### 核心特性

该平台提供三种主要开发方法：基于Maven的代码生成器、可视化在线配置，以及AI辅助开发。通过这些方法，开发者可以快速构建业务系统，其中零代码模式允许用户在5分钟内搭建业务系统，低代码模式则能一键生成前后端代码。

#### AI能力

内置AI应用支持AI聊天、知识库、流程编排、MCP与插件功能，并兼容各种模型。Skills能力可以实现一句话画流程图、设计表单、生成系统等功能，引领AI生成→在线配置→代码生成→手工合并的全新开发模式。

#### 技术优势

JeecgBoot能够解决Java项目80%的重复工作，在快速提高效率的同时保留灵活性。作为企业级平台，它提供了完整的技术栈支持，包括详细的功能列表、系统要求和快速启动指南等文档资源。

#### 应用价值

该平台在GitHub上拥有约46,225颗星标（每天约28颗新增），表明其在开发者社区中具有较高的关注度和实用性。

---
## 评论

#### 总体判断

JeecgBoot是一款成熟度较高的企业级AI低代码平台，在Java生态中积累了超过46k星标，具备完整的“低代码+零代码+AI”三合一开发模式。对于需要快速构建内部管理系统的团队而言，它提供了相对完整的技术方案；但对追求极致定制化或高性能的场景，仍需审慎评估其局限。

#### 技术依据

从事实层面看，JeecgBoot基于Spring Boot生态构建，提供了成熟的前后端代码生成器、在线表单设计、流程引擎以及权限管理模块。其Vue3前端版本支持响应式页面配置，后端采用微服务架构设计，具备一定的扩展能力。该项目持续维护多年，社区积累了一定的插件生态，包括报表、接口管理、打印等常用功能。这些均为可验证的技术事实。

从推断角度看，平台宣称的“解决80%重复工作”可能适用于标准化CRUD场景，但实际比例取决于业务复杂度与开发团队的熟悉程度。AI能力（如流程图生成、代码补全）尚处于辅助定位，不应视为替代人工设计的核心价值。

#### 适用场景

该平台最适合以下场景：企业内部管理系统（如OA、CRM、项目管理）的快速交付；创业团队在MVP阶段需要快速验证业务逻辑；技术团队资源有限但需要构建相对规范的后台系统。此外，对于需要快速搭建原型的政务、教育类项目也有一定适用性。

#### 局限性

需要注意的是，当业务逻辑复杂度较高或存在大量定制需求时，低代码模式可能反而增加开发成本。前端深度定制仍需掌握Vue3技术栈。平台的部分高级功能依赖商业组件，开源版本存在一定限制。在高并发、大数据量场景下，基础配置可能需要额外的性能调优。

#### 验证方式

建议通过官方在线Demo体验零代码搭建流程，使用代码生成器生成实际业务模块并检查代码质量与可维护性。可参考GitHub仓库的Issue处理速度和社区活跃度，评估项目长期维护的可靠性。

---
## 技术分析

#### 架构概览

基于仓库结构分析，JeecgBoot采用典型的B/S分层架构。后端基于Spring Boot生态构建，前端采用Vue3框架，形成经典的MVC分离模式。主仓库采用多模块Maven项目结构，包含`jeecg-boot`（后端）和`jeecgboot-vue3`（前端）两个核心子项目。从目录组织看，系统支持微服务部署，具备良好的服务拆分能力。

#### 核心能力分析

**低代码与零代码双模式**是其核心定位。零代码模式通过可视化配置实现业务系统快速搭建，降低技术门槛；低代码模式则通过代码生成机制（一键生成前后端代码）提升开发效率，两者形成互补。**AI能力集成**是JeecgBoot的差异化亮点，内置AI聊天、知识库、流程编排功能，支持MCP协议与插件扩展，并具备"一句话画流程图、设计表单、生成系统"等智能化能力。

#### 技术实现特点

后端技术栈以Java为核心，依托Spring Boot、MyBatis-Plus等成熟框架，数据库层面支持主流关系型数据库。前端采用Vue3配合Element Plus UI组件库，实现响应式界面。从技术选型看，系统兼顾企业级稳定性与开发效率。**AI集成**方面，系统支持多种大模型接入，这表明其具备模型无关性设计，可灵活对接不同AI服务提供商。

#### 适用场景分析

基于其功能特性推断，以下场景较为适用：企业内部管理系统的快速开发，如OA、CRM、ERP等标准化程度较高的业务系统；创业团队或中小企业的MVP阶段开发，可借助零代码模式快速验证业务可行性；需要快速交付的政务或公共服务平台开发。此外，对于需要AI能力加持的智能应用场景（如智能客服、知识库问答），JeecgBoot提供了开箱即用的解决方案。

#### 不适用场景分析

基于技术架构特征推断，以下场景需谨慎评估：复杂定制化业务逻辑的系统，平台化产品往往在灵活性与标准化之间存在权衡；高并发、高性能要求的互联网级应用，低代码平台在底层优化方面通常存在局限；对技术架构有特殊要求的场景，如需要特定技术栈或非关系型数据库深度集成的情况；长期运维复杂度较高的核心业务系统，可能面临平台升级带来的兼容性风险。

#### 学习与落地建议

**学习路径建议**：首先熟悉后端Spring Boot项目结构和代码生成机制，理解前后端交互规范；重点掌握在线表单和工作流配置能力；最后深入AI功能集成，理解MCP协议和插件开发模式。官方文档和示例项目是较好的入门资源。

**落地实施建议**：评估团队Java和Vue技术能力，确保具备二次开发基础；建议从非核心业务系统开始试点，积累平台使用经验；建立代码规范，明确哪些通过平台生成、哪些需要手工介入；关注平台版本更新，制定合理的升级策略。

**风险提示**：基于46,225星标数（截至分析时点的已知事实）推断，该项目具有较高的社区活跃度，但企业在选型时仍需评估技术债务、长期维护成本以及供应商依赖风险。建议结合具体业务需求和团队实际情况进行综合判断。

---
## 学习要点

- JeecgBoot 是一个基于 Spring Boot + Vue 的开源低代码平台，旨在加速企业级应用开发。
- 平台提供可视化的代码生成器和在线表单设计功能，显著提升开发效率。
- 内置 Shiro、JWT、MyBatis-Plus 等安全与持久层技术，保障系统安全与性能。
- 支持微服务架构，可通过 Docker、Spring Cloud 等方式快速部署与扩展。
- 采用 Ant Design Pro 作为前端 UI，提供现代化、响应式的用户体验。
- 项目在 GitHub Trending 上受到关注，社区活跃并持续更新迭代。
- 提供丰富的业务组件和插件体系，便于二次开发和功能扩展。

---
## 引用

- **GitHub 仓库**: [https://github.com/jeecgboot/JeecgBoot](https://github.com/jeecgboot/JeecgBoot)
- **DeepWiki**: [https://deepwiki.com/jeecgboot/JeecgBoot](https://deepwiki.com/jeecgboot/JeecgBoot)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [低代码](/tags/%E4%BD%8E%E4%BB%A3%E7%A0%81/) / [零代码](/tags/%E9%9B%B6%E4%BB%A3%E7%A0%81/) / [Java](/tags/java/) / [AI开发](/tags/ai%E5%BC%80%E5%8F%91/) / [代码生成器](/tags/%E4%BB%A3%E7%A0%81%E7%94%9F%E6%88%90%E5%99%A8/) / [SpringBoot](/tags/springboot/) / [Vue3](/tags/vue3/) / [企业级](/tags/%E4%BC%81%E4%B8%9A%E7%BA%A7/)
- 场景： [后端开发](/scenarios/%E5%90%8E%E7%AB%AF%E5%BC%80%E5%8F%91/) / [全栈开发](/scenarios/%E5%85%A8%E6%A0%88%E5%BC%80%E5%8F%91/) / [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [JeecgBoot：AI 驱动的低代码平台，支持零代码与代码生成双模式]({{< relref "posts/20260317-github_trending-jeecgboot-jeecgboot-2.md" >}})
- [JeecgBoot：AI 驱动的低代码平台，支持零代码搭建与代码生成]({{< relref "posts/20260318-github_trending-jeecgboot-jeecgboot-2.md" >}})
- [JeecgBoot开源低代码平台：集成AI应用与代码生成器]({{< relref "posts/20260131-github_trending-jeecgboot-jeecgboot-3.md" >}})
- [JeecgBoot：集成AI低代码平台与代码生成器的Java开发框架]({{< relref "posts/20260129-github_trending-jeecgboot-jeecgboot-3.md" >}})
- [JeecgBoot：集成AI低代码与代码生成器的企业级开发平台]({{< relref "posts/20260129-github_trending-jeecgboot-jeecgboot-7.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*