---
title: "JeecgBoot：5分钟搭建系统的Java低代码平台"
date: 2026-05-14T08:10:10+08:00
draft: false
entry_kind: "auto"
tags: ["低代码", "Java", "零代码", "AI平台", "代码生成", "开源", "企业级", "快速开发"]
categories: ["开发工具", "AI 工程"]
source: github_trending
description: "JeecgBoot 是一款企业级 AI 低代码开发平台，采用 Java 技术栈，支持低代码与零代码双模式。它通过可视化配置和 AI 辅助生成，能在几分钟内完成业务系统搭建，同时一键生成前后端代码，大幅降低重复性工作。平台内置 AI 聊天、知识库、流程编排等能力，适用于企业信息化系统和内部工具的快速开发。本文将介绍其核心"
external_url: https://github.com/jeecgboot/JeecgBoot
scenarios: ["Web应用开发", "全栈开发", "后端开发"]
---

# JeecgBoot：5分钟搭建系统的Java低代码平台

> **原名**: jeecgboot /

      JeecgBoot

---

## 基本信息

- **描述**: 您好，您提供的原文本身就是中文。我将对其进行润色和优化，使其表达更加流畅专业：

---

**AI低代码平台，支持「低代码 + 零代码」双模式：**

- **零代码**：5分钟快速搭建业务系统
- **低代码**：一键生成前后端代码

**内置AI应用，支持：**

- AI聊天
- 知识库
- 流程编排
- MCP与插件
- 支持各种模型

**Skills能力实现：**

- 一句话画流程图
- 设计表单
- 生成系统

**引领全新开发模式：** AI生成 → 在线配置 → 代码生成 → 手工合并

有效解决Java项目80%的重复工作，快速提升效率，同时保留足够的灵活性。

---

**主要优化内容：**

1. 将信息分层呈现，增强可读性
2. 使用项目符号清晰区分各项功能
3. 将开发流程单独强调，突出核心价值
4. 调整结尾表述，使逻辑更通顺

如需其他风格或用途的版本（如营销文案、技术文档等），请告诉我！
- **语言**: Java
- **星标**: 46,240 (+27 stars today)
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

JeecgBoot 是一款企业级 AI 低代码开发平台，采用 Java 技术栈，支持低代码与零代码双模式。它通过可视化配置和 AI 辅助生成，能在几分钟内完成业务系统搭建，同时一键生成前后端代码，大幅降低重复性工作。平台内置 AI 聊天、知识库、流程编排等能力，适用于企业信息化系统和内部工具的快速开发。本文将介绍其核心功能、技术架构和实际应用场景。

---
## 评论

JeecgBoot 是一个具备较高成熟度的 Java 低代码平台，从星标数 46,240 和活跃的社区维护来看，该项目在开源低代码领域拥有可观的用户基础和技术积累。

#### 技术架构与核心能力

该平台采用前后端分离架构，前端基于 Vue3，后端基于 Spring Boot/MyBatis-Plus，这套技术选型在企业级应用开发中属于主流方案，开发者无需额外学习特定框架即可快速上手。低代码模式通过可视化配置和代码生成机制，支持一键生成 CRUD 功能的实体类、Controller、Service、Mapper 等前后端代码，这一能力在处理标准化的管理后台时能够显著减少重复编码工作。零代码模式则通过表单设计和流程配置实现业务搭建，适合非技术用户快速构建原型或简单业务系统。平台声称支持 AI 生成代码与在线配置的结合，引入 MCP 协议和插件机制扩展集成能力，但其 AI 功能的实际稳定性和生产环境适用性需进一步验证。

#### 适用场景

该平台最适合以下场景：一是企业内部管理系统、OA、CRM 等后台管理类项目，当业务模型相对标准、表单流程可控时，低代码模式可大幅提升开发效率；二是快速原型验证阶段，零代码配置可快速产出可运行系统用于需求确认；三是技术团队规模有限但需要快速交付的项目，低代码生成的代码结构可作为基础框架减少从零搭建的工作量。

#### 局限与风险

需要注意的是，平台声称能“解决 Java 项目 80% 的重复工作”，这一说法属于推断性表述，实际效果高度依赖业务场景的适配度。对于复杂业务逻辑、非标准交互或深度定制化需求，低代码生成的代码往往需要大量手工调整，反而可能增加维护成本。AI 功能作为近年新增能力，其生成质量和可靠性尚缺乏充分的社区验证，生产环境使用前建议进行充分测试。此外，随着前端技术演进，Vue3 版本的维护更新频率和生态兼容性也需要持续关注。

#### 验证方式

建议从以下维度评估该平台是否满足项目需求：使用平台的在线演示或本地部署版本，实际操作表单设计和代码生成流程，检验生成的代码结构是否符合团队编码规范；针对具体业务场景评估零代码模式的覆盖度，确认是否存在功能盲区；查阅社区的 Issues 和 Pull Requests 了解问题响应速度和技术支持的活跃程度。

---
## 技术分析

#### 系统架构

JeecgBoot 采用经典的前后端分离架构，这也是当前企业级应用的主流选择。

**后端层面**，基于 Spring Boot 框架构建，采用了模块化设计思想。仓库结构显示存在 `jeecg-boot` 这样的核心模块，这种组织方式便于功能扩展和业务拆分。RESTful API 作为前后端通信的约定，为前端提供了标准化的数据接口。这种架构的优势在于前后端团队可以独立开发、测试和部署，通过接口契约保持协作的确定性。

**前端层面**，使用了 Vue3 作为核心框架，仓库中的 `jeecgboot-vue3` 目录证实了这一点。Vue3 相比 Vue2 在性能、TypeScript 支持和组合式 API 上都有显著提升，选择 Vue3 说明项目在技术前瞻性上有一定考量。前后端分离的架构使得页面交互和业务逻辑可以更好地解耦，也为后续迁移到其他前端框架保留了可能性。

**数据流层面**，推测采用了典型的三层架构：Controller 层处理请求路由、Service 层承载业务逻辑、Mapper 层对接数据库。这种分层模式虽然传统，但在企业级应用中具有维护成本低、人员上手快、职责清晰等优势。

#### 核心能力

**代码生成机制**是该平台最核心的能力。从描述来看，平台能够根据数据模型或配置一键生成增删改查的后端接口和前端页面，这在企业系统开发中确实能覆盖大量重复性工作。代码生成器的本质是将规范化的业务模板与用户输入的元数据结合，输出符合团队规范的源代码。

**零代码配置模式**允许用户通过可视化界面快速搭建业务系统。这类功能通常依赖元数据驱动设计——用户通过表单设计器定义数据模型，系统自动生成对应的数据库表结构、API 接口和 UI 组件。这种模式的局限在于配置灵活性与生成代码质量之间的平衡。

**AI 能力集成**是近期的技术亮点。平台支持 AI 对话、知识库检索、流程编排以及 MCP（Model Context Protocol）协议，这些能力使其从传统代码生成工具向智能化开发助手演进。描述中提到的"一句话画流程图、设计表单"暗示系统接入了大语言模型来处理自然语言指令并转化为系统配置。

#### 技术实现

从技术栈判断，后端依赖 Spring Boot + MyBatis-Plus 的组合是比较确定的。MyBatis-Plus 在 CRUD 操作上的封装能够显著减少数据库访问层的代码量，这与低代码平台的理念高度契合。数据库层面虽然没有明确说明，但 MySQL 和 PostgreSQL 都是 Java 生态中常见的选择。

前端的 Vue3 技术栈搭配了 Vue Router 和 Pinia（或其他状态管理方案），这从前端工程化角度是合理的配置。组件库层面，推测使用了 Element Plus 或 Ant Design Vue 这类成熟的企业级 UI 框架，因为低代码平台需要大量可复用的表单组件和布局组件。

代码生成器的实现可能采用了模板引擎技术，如 FreeMarker 或 Velocity。这类工具能够将静态模板与动态数据结合，生成符合项目规范的 Java 类、SQL 脚本和 Vue 组件。AI 能力的实现则很可能对接了 OpenAI API 或其他大模型服务，通过 prompt 工程将自然语言转换为系统可执行的配置。

#### 适用与不适用场景

**适用场景**包括：中小型企业的内部管理系统，如 OA、CRM、后勤管理等标准化程度较高的业务；快速原型验证阶段的产品开发，需要在短时间内产出可运行的演示版本；团队技术储备以 Java 为主但希望提升开发效率的场景。JeecgBoot 的代码生成能力对于这类项目能将开发周期压缩 30%-50%，这是基于其覆盖 CRUD 场景的代码占比推断得出的结论。

**不适用场景**需要特别注意。首先，复杂业务流程或高度定制化的系统，低代码平台生成的代码在灵活性和可维护性上难以与精心设计的架构相比。其次，对性能要求苛刻的应用，生成代码通常包含通用逻辑而非针对性优化。第三，需要深度前端交互的项目，如数据可视化大屏或复杂编辑器，零代码模式的组件库可能无法满足需求。第四，技术栈异构的团队，该平台强依赖 Java 后端和 Vue3 前端，改造成本较高。

#### 学习与落地建议

团队在决定采用前，建议从以下维度进行评估。首先是**需求匹配度测试**，选取团队正在开发或即将启动的一个中等规模模块，按照平台的工作流从建模到生成代码完整走一遍，评估输出质量是否符合团队的代码规范。其次是**扩展性验证**，测试在生成代码基础上进行二次开发时的体验，确认不会陷入"想改但不敢改"的困境。第三是**AI 能力试用**，目前 AI 功能是差异化卖点，需要实际测试其生成效果和响应稳定性。

学习路径上，建议先掌握平台的元数据建模方式和代码生成配置，因为这是所有高级功能的基础。然后了解其内置的表单设计器和流程引擎的使用方法。最后在有余力时研究 AI 能力的接入方式和 prompt 优化技巧。部署层面，该平台作为开源项目，虽然提供了文档和社区支持，但生产环境落地可能需要额外考虑监控、运维等工程化配套，这些是平台本身之外的隐性成本。

---
## 学习要点

- 基于 Spring Boot + Vue3 的前后端分离低代码平台，可实现企业级应用的快速开发。
- 提供在线表单、在线报表、代码生成器等可视化开发工具，大幅降低开发和维护成本。
- 内置完整的 RBAC 权限管理和细粒度数据权限控制，保障系统安全。
- 支持多种关系型数据库（MySQL、Oracle、SQLServer 等）与主流前端框架（Vue、Element UI）适配。
- 采用插件化、模块化架构，便于二次开发和功能扩展。
- 集成微服务治理能力（服务注册、配置中心、熔断等），适配分布式与云原生场景。
- 拥有活跃的开源社区、持续迭代和详尽文档，提供可靠的技术支持。

---
## 引用

- **GitHub 仓库**: [https://github.com/jeecgboot/JeecgBoot](https://github.com/jeecgboot/JeecgBoot)
- **DeepWiki**: [https://deepwiki.com/jeecgboot/JeecgBoot](https://deepwiki.com/jeecgboot/JeecgBoot)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [低代码](/tags/%E4%BD%8E%E4%BB%A3%E7%A0%81/) / [Java](/tags/java/) / [零代码](/tags/%E9%9B%B6%E4%BB%A3%E7%A0%81/) / [AI平台](/tags/ai%E5%B9%B3%E5%8F%B0/) / [代码生成](/tags/%E4%BB%A3%E7%A0%81%E7%94%9F%E6%88%90/) / [开源](/tags/%E5%BC%80%E6%BA%90/) / [企业级](/tags/%E4%BC%81%E4%B8%9A%E7%BA%A7/) / [快速开发](/tags/%E5%BF%AB%E9%80%9F%E5%BC%80%E5%8F%91/)
- 场景： [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/) / [全栈开发](/scenarios/%E5%85%A8%E6%A0%88%E5%BC%80%E5%8F%91/) / [后端开发](/scenarios/%E5%90%8E%E7%AB%AF%E5%BC%80%E5%8F%91/)

### 相关文章

- [Java低代码平台JeecgBoot：AI+零代码双模式]({{< relref "posts/20260513-github_trending-jeecgboot-jeecgboot-0.md" >}})
- [JeecgBoot：AI 驱动的低代码平台，支持零代码与代码生成双模式]({{< relref "posts/20260317-github_trending-jeecgboot-jeecgboot-2.md" >}})
- [JeecgBoot：AI 驱动的低代码平台，支持零代码搭建与代码生成]({{< relref "posts/20260318-github_trending-jeecgboot-jeecgboot-2.md" >}})
- [JeecgBoot开源低代码平台：集成AI应用与代码生成器]({{< relref "posts/20260131-github_trending-jeecgboot-jeecgboot-3.md" >}})
- [JeecgBoot：集成AI低代码平台与代码生成器的Java开发框架]({{< relref "posts/20260129-github_trending-jeecgboot-jeecgboot-3.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*