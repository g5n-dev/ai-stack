---
title: "JeecgBoot开源Java低代码平台 Stars超4.6万"
date: 2026-05-14T00:14:09+08:00
draft: false
entry_kind: "auto"
tags: ["低代码平台", "JeecgBoot", "Java开源", "SpringBoot", "Vue3", "AI增强开发", "代码生成器", "企业级应用"]
categories: ["开源生态", "开发工具"]
source: github_trending
description: "JeecgBoot是一个企业级AI增强的低代码开发平台，基于Spring Boot 3.5.5、Vue 3和Spring Cloud Alibaba 2023构建。该平台采用“低代码+零代码”双模式运营：零代码模式可在5分钟内快速搭建业务系统，低代码模式则能一键生成前后端代码，大幅提升开发效率。 平台内置强大的AI应用"
external_url: https://github.com/jeecgboot/JeecgBoot
scenarios: ["Web应用开发", "后端开发", "全栈开发"]
---

# JeecgBoot开源Java低代码平台 Stars超4.6万

> **原名**: jeecgboot /

      JeecgBoot

---

## 基本信息

- **描述**: 您好！我注意到您提供的内容已经是中文了。请问您是否需要：

1. **将此中文内容翻译成英文**或其他语言？
2. 或者您可能有其他语言的原文需要翻译成中文？

如果您能提供原始的外语文本（通常是英文），我将很乐意帮您翻译成中文，同时保持原文的格式和语气。
- **语言**: Java
- **星标**: 46,226 (+27 stars today)
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

JeecgBoot 是一个基于 Java 的企业级低代码开发平台，整合了代码生成、可视化配置和 AI 辅助能力。它旨在降低企业应用开发的技术门槛，帮助团队快速构建业务系统，同时保持对底层代码的完整控制。适合需要快速交付业务系统的技术团队，也适用于希望优化开发效率的企业。本文将围绕平台的核心功能、技术架构以及典型应用场景展开，帮助读者评估其在实际项目中的适用性。

---
## 摘要

JeecgBoot是一个企业级AI增强的低代码开发平台，基于Spring Boot 3.5.5、Vue 3和Spring Cloud Alibaba 2023构建。该平台采用“低代码+零代码”双模式运营：零代码模式可在5分钟内快速搭建业务系统，低代码模式则能一键生成前后端代码，大幅提升开发效率。

平台内置强大的AI应用能力，包括AI聊天、知识库、流程编排、MCP与插件等功能，并支持多种AI模型。用户可通过简单的自然语言指令实现流程图绘制、表单设计和系统生成。JeecgBoot创新性地将开发流程定义为“AI生成→在线配置→代码生成→手工合并”的闭环模式，能够自动化处理Java项目中约80%的重复性工作，在保证开发效率的同时保留必要的灵活性。

作为开源项目，JeecgBoot使用Java作为主要编程语言，目前在GitHub上已获得超过46,000颗星标，显示出较高的社区关注度和实际应用价值。平台适用于企业级应用开发场景，为开发团队提供了从概念设计到代码实现的一站式解决方案。

---
## 评论

#### 总体判断
JeecgBoot 是一款成熟度高、社区规模大的 Java 低代码平台，兼具零代码快速搭建和低代码代码生成，并叠加 AI 功能，适合企业内部管理系统和快速原型交付。

#### 事实依据
- 仓库星标 46,226，表明社区关注度高。
- 技术栈采用 Spring Boot + MyBatis‑Plus 后端、Vue3 前端，结构清晰。
- 官方文档列出“低代码+零代码”双模式、可视化表单、代码生成、流程引擎、AI 聊天与知识库等完整功能。
- 支持多种模型接入（MCP、插件），提供 Docker‑Compose 一键部署。

#### 适用场景
- 5 分钟内完成简单 CRUD 页面搭建的业务系统。
- 团队拥有 Java 后端但缺少前端资源时，可利用低代码生成前后端代码。
- 需要 AI 辅助对话、检索或流程编排的应用。
- 快速原型交付，后期通过手工合并代码进行细节优化。

#### 局限与推断
- 生成的代码受平台约束，复杂 UI 或高频交互需自行改造（推断）。
- AI 功能依赖外部模型，实际对话质量取决于接入模型的能力（推断）。
- 主要面向 Java 生态，非 Java 项目迁移成本较高（推断）。

#### 验证方式
- 使用官方 Docker‑Compose 启动最小化实例，测试零代码表单创建与流程部署。
- 运行代码生成模块，检查生成的 Controller、Service、Mapper 是否符合团队规范。
- 接入本地或云端模型，评估 AI 聊天的响应速度和准确率。
- 对比生成系统在高并发场景下的响应时间，评估性能是否满足业务需求。

#### 小结
若团队以 Java 为主且重视快速交付，JeecgBoot 是值得尝试的低代码方案；引入 AI 能力时需做好模型选型和效果验证，以免在实际业务中产生预期偏差。

---
## 技术分析

#### 架构与目录结构

从仓库结构分析，JeecgBoot采用经典的前后端分离架构。主仓库下包含两个核心子模块：jeecg-boot作为Java后端项目，jeecgboot-vue3作为Vue3前端项目。这种Monorepo组织方式便于统一版本管理但也意味着项目体积较大。官方文档显示系统分为Online开发、报表、打印、大屏等多个功能模块，架构上属于典型的企业应用分层设计，前端通过API与后端交互，后端采用Spring Boot生态。

#### 核心能力与技术实现

**低代码生成能力**是该平台的核心卖点。从描述推断，平台应内置了Online表单、Online报表等可视化配置功能，支持通过配置而非编码的方式生成CRUD页面。代码生成器能够一键输出前后端代码，这通常依赖于模板引擎（如Velocity或FreeMarker）配合数据库元数据读取实现。

**AI能力整合**是3.x版本的亮点。平台支持AI聊天、知识库、流程编排以及MCP（Model Context Protocol）与插件机制。Skills模块提供"一句话画流程图、设计表单、生成系统"等能力，这表明平台已将大语言模型能力深度嵌入开发流程。从技术角度，这需要构建Prompt工程、工作流编排以及与多种AI模型适配的接口层。

**技术栈推断**：后端以Spring Boot为基础，结合MyBatis-Plus简化数据库操作；前端采用Vue3Composition API配合Element Plus UI库；代码生成部分可能采用Jinja2或类似模板引擎处理Java、Vue、SQL等多种文件的输出。

#### 适用与不适用场景

**适用场景**包括：需要快速搭建后台管理系统的中小企业；内部管理系统、OA、CRM等标准业务场景；技术团队Java人员充足但前端资源有限的场景；对开发速度要求远高于极致定制化的项目。

**不适用场景**包括：业务逻辑极其复杂、流程高度定制化的核心业务系统；追求极致性能或需要精细前端控制的场景；对前端框架有特定要求（如React、Angular）的团队；需要深度二次开发且对源码可控性要求高的项目。

#### 学习与落地建议

建议采取渐进式引入策略。首先从官方提供的示例项目入手，理解代码生成器的输入输出模式；然后在非核心项目中验证平台能力，重点评估生成的代码质量和可维护性。对于团队，建议安排专人深入学习源码，特别是代码生成器和AI集成模块，便于后续的问题排查和定制开发。落地时需注意：生成的代码应纳入团队代码规范管理；AI功能需评估实际业务价值；版本升级时需关注兼容性变更。

---
## 学习要点

- JeecgBoot 是基于 Spring Boot + Vue 的开源低代码平台，能够通过可视化设计快速生成前后端代码。
- 平台内置代码生成器、在线表单、在线报表等工具，大幅提升开发效率，降低重复编码工作。
- 具备完整的权限管理、用户角色、数据字典等企业级功能，开箱即用。
- 支持微服务架构（Spring Cloud）与 Docker 容器化部署，便于横向扩展和运维。
- 在 GitHub Trending 上持续受关注，说明社区活跃、版本迭代迅速且文档完善。
- 采用模块化设计，提供丰富的插件和 UI 组件（Ant Design Vue），可灵活扩展业务需求。

---
## 引用

- **GitHub 仓库**: [https://github.com/jeecgboot/JeecgBoot](https://github.com/jeecgboot/JeecgBoot)
- **DeepWiki**: [https://deepwiki.com/jeecgboot/JeecgBoot](https://deepwiki.com/jeecgboot/JeecgBoot)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/) / [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/)
- 标签： [低代码平台](/tags/%E4%BD%8E%E4%BB%A3%E7%A0%81%E5%B9%B3%E5%8F%B0/) / [JeecgBoot](/tags/jeecgboot/) / [Java开源](/tags/java%E5%BC%80%E6%BA%90/) / [SpringBoot](/tags/springboot/) / [Vue3](/tags/vue3/) / [AI增强开发](/tags/ai%E5%A2%9E%E5%BC%BA%E5%BC%80%E5%8F%91/) / [代码生成器](/tags/%E4%BB%A3%E7%A0%81%E7%94%9F%E6%88%90%E5%99%A8/) / [企业级应用](/tags/%E4%BC%81%E4%B8%9A%E7%BA%A7%E5%BA%94%E7%94%A8/)
- 场景： [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/) / [后端开发](/scenarios/%E5%90%8E%E7%AB%AF%E5%BC%80%E5%8F%91/) / [全栈开发](/scenarios/%E5%85%A8%E6%A0%88%E5%BC%80%E5%8F%91/)

### 相关文章

- [JeecgBoot：AI 驱动的低代码平台，支持零代码与代码生成双模式]({{< relref "posts/20260317-github_trending-jeecgboot-jeecgboot-2.md" >}})
- [JeecgBoot：AI 驱动的低代码平台，支持零代码搭建与代码生成]({{< relref "posts/20260318-github_trending-jeecgboot-jeecgboot-2.md" >}})
- [JeecgBoot：AI低代码平台集成代码生成器与知识库]({{< relref "posts/20260130-github_trending-jeecgboot-jeecgboot-3.md" >}})
- [JeecgBoot开源低代码平台：集成AI应用与代码生成器]({{< relref "posts/20260131-github_trending-jeecgboot-jeecgboot-3.md" >}})
- [JeecgBoot：AI低代码平台一键生成Java代码]({{< relref "posts/20260320-github_trending-jeecgboot-jeecgboot-6.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*