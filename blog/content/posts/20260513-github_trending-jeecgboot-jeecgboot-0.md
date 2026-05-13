---
title: "JeecgBoot：Java项目AI低代码平台，零代码5分钟搭系统"
date: 2026-05-13T18:22:31+08:00
draft: false
entry_kind: "auto"
tags: ["低代码", "AI增强", "代码生成", "Java", "Vue3", "企业级", "SaaS", "敏捷开发"]
categories: ["开发工具", "AI 工程"]
source: github_trending
description: "JeecgBoot是一个基于Spring Boot 3.5.5、Vue 3和Spring Cloud Alibaba 2023.0.3.3构建的企业级AI增强低代码开发平台，采用Java语言开发，目前在GitHub上拥有超过46,000颗星标。 该平台提供“低代码+零代码”双模式开发能力。零代码模式允许用户在5分钟内通"
external_url: https://github.com/jeecgboot/JeecgBoot
scenarios: ["全栈开发", "后端开发", "Web应用开发"]
---

# JeecgBoot：Java项目AI低代码平台，零代码5分钟搭系统

> **原名**: jeecgboot /

      JeecgBoot

---

## 基本信息

- **描述**: AI低代码平台，支持「低代码 + 零代码」双模式：零代码 5 分钟搭建业务系统，低代码模式一键生成前后端代码。 内置AI 应用，支持AI聊天、知识库、流程编排、MCP与插件，支持各种模型。Skills能力实现：一句话画流程图、设计表单、生成系统。 引领 AI生成→在线配置→代码生成→手工合并的开发模式，解决Java项目80%的重复工作，快速提高效率，又不失灵活性。
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

JeecgBoot是一款企业级AI低代码开发平台，支持“低代码+零代码”双模式并行。平台通过可视化配置与AI智能生成相结合，显著提升Java业务系统的开发效率，降低技术门槛。本指南将系统介绍JeecgBoot的核心功能、技术架构、典型应用场景与最佳实践，助力开发者快速掌握并高效落地。

---
## 摘要

JeecgBoot是一个基于Spring Boot 3.5.5、Vue 3和Spring Cloud Alibaba 2023.0.3.3构建的企业级AI增强低代码开发平台，采用Java语言开发，目前在GitHub上拥有超过46,000颗星标。

该平台提供“低代码+零代码”双模式开发能力。零代码模式允许用户在5分钟内通过可视化配置快速搭建业务系统，无需编写代码；低代码模式则支持一键生成前后端代码，适用于复杂业务场景。这种双模式设计既保证了开发效率，又保留了足够的灵活性，满足不同开发需求。

JeecgBoot的AI能力是其核心特色。平台内置AI应用，支持AI聊天、知识库构建、流程编排、MCP与插件扩展，并兼容各种大语言模型。通过Skills功能，开发者可以用自然语言描述需求，实现一句话生成流程图、设计表单、自动生成系统等功能。平台引领“AI生成→在线配置→代码生成→手工合并”的开发模式，据称可解决Java项目80%的重复工作，显著提升开发效率。

该平台提供三种主要的开发方式：一是基于Maven的代码生成器，支持快速生成标准化的前后端代码；二是可视化开发环境，支持流程设计、表单配置等低代码操作；三是AI辅助开发，通过自然语言处理实现需求理解和代码自动生成。

JeecgBoot的目标是成为企业级应用开发的统一平台，通过整合代码生成、视觉化开发和AI能力，降低开发门槛，加速业务系统交付，同时保持对复杂业务场景的适配能力。

---
## 评论

#### 总体判断

基于公开信息（星标 46k、Java 语言、零代码+低代码双模式、AI 集成）判断，JeecgBoot 在企业内部管理系统快速原型和中小规模业务系统搭建上具备显著效率优势，尤其适合需要快速交付但对前端自定义要求不高的团队。

#### 技术依据与适用场景

- 事实：项目采用 Spring Boot + MyBatis-Plus + Vue3，技术栈成熟；提供代码生成、在线表单、流程编排和 AI 聊天/知识库等模块；GitHub 星标数量说明社区活跃度相对较高。
- 推断：零代码模式可通过可视化配置实现 CRUD 基本功能，降低前期学习成本；AI 生成的流程图和表单可在需求变更频繁的场景下加速迭代；代码生成 + 手工合并的混合模式在保持灵活性的同时减少重复编码。
- 适用场景：企业内部管理系统（MIS、OA、CRM 基础版）、快速原型验证、需要在短周期内交付的中小型项目。

#### 局限与验证方式

- 局限（基于推断）：对复杂业务规则、深度定制的 UI/UX 以及高性能高并发场景，原生生成的代码可能需要大量手工改造；AI 能力的实际效果受模型选型和提示词质量影响，需在实际业务中进行评估。
- 验证方式：可在测试环境使用零代码模块搭建一个完整业务流程，观察生成的代码结构和可维护性；再用低代码模式生成实体和接口，跑通单元测试和压力测试，评估后期二次开发的成本。

整体而言，JeecgBoot 是一个兼具社区支持和功能完整性的低代码方案，适合作为快速交付的起点，但在大规模或高度定制化项目中需谨慎评估后续改造工作量。

---
## 技术分析

#### 系统架构
##### 模块划分
- **后端**（jeecg-boot）：业务 API、工作流引擎、代码生成、AI 调度模块采用分层结构（Controller → Service → Mapper → Model）。
- **前端**（jeecgboot-vue3）：基于 Vue3 + Vite + Element Plus，提供可视化表单/流程设计器、仪表盘、权限页面，通过 Axios 调用后端 RESTful 接口。

##### 技术栈
已知事实：项目语言为 Java，描述中提及“前后端代码”。
推断：后端核心为 Spring Boot（或 Spring Cloud）+ MyBatis‑Plus + Shiro + JWT；微服务注册/配置可能使用 Nacos + Sentinel；前端采用 Vue3 + Pinia + Element Plus。

#### 核心能力
##### 零代码/低代码双模式
- **零代码**：拖拽式表单、列表视图，一键生成 CRUD 页面，5 分钟完成业务系统搭建。
- **低代码**：在线建模生成实体、流程、服务端代码；支持自定义模板和插件扩展。

##### AI 能力
- 内置 AI 对话、知识库检索、流程编排；支持 MCP（Model‑Communication‑Protocol）与插件化模型接入。
- Skills：语音/文本描述生成流程图、表单布局、完整系统结构，实现“一句需求 → 可视化模型 → 代码”。

##### 代码生成与扩展
- 基于 MyBatis‑Plus、Vue 代码模板自动生成 Controller、Service、Mapper、Vue 页面、路由、权限字段。
- 支持自定义生成规则，满足复杂业务场景；插件市场提供第三方组件集成。

#### 技术实现要点
##### 后端实现
已知事实：提供代码生成服务和 AI 调度。
推断：使用 Spring Boot Starter + MyBatis‑Plus 代码生成器；工作流可能基于 Flowable/Activiti；安全采用 Shiro/JWT；接口统一返回 Result<T> 结构。

##### 前端实现
- 表单/流程设计器基于 JSON Schema + Vue 动态渲染；状态管理使用 Pinia；路由通过 Vue Router 动态生成；权限控制与后端 RBAC 同步。

##### AI 集成
- AI 模块通过 HTTP/gRPC 调用外部 LLM（如 OpenAI、百度文心），封装为统一 MCP 接口；支持插件式模型切换，满足企业私有化部署需求。

#### 适用与不适用场景
##### 适用场景
- 企业内部管理系统（MIS）、审批/报销、CRM、ERP 原型；需要快速交付的中小项目；已有 Spring Boot 后端的团队希望前后端代码统一生成。

##### 不适用场景
- 对前端 UI 交互要求极高（如复杂动画、实时协作）的产品；极低延迟或高并发的交易系统；对非 Java 技术栈（Node、Go）有硬性要求的项目。

#### 学习与落地建议
##### 学习路径
1. 阅读官方文档与 README.md，掌握模块划分与目录结构。
2. 本地运行 jeecg-boot 与 jeecgboot-vue3，了解代码生成流程与 AI 插件配置。
3. 研究代码生成模板（velocity/ftl）与自定义规则，尝试生成自己的业务模块。

##### 落地注意事项
- 业务模型尽量使用平台提供的元数据（表单、流程），避免直接写死业务逻辑。
- AI 能力涉及外部模型费用，建议在概念验证阶段使用免费额度，后期评估成本。
- 权限设计需结合 Shiro/JWT 与前端动态路由，确保细粒度控制。
- 生产环境部署推荐 Docker‑Compose + Nacos，实现微服务弹性伸缩。

---
## 学习要点

- JeecgBoot 是基于 Spring Boot 的低代码开发平台，提供前后端分离的整体解决方案。
- 前端采用 Vue 与 Ant Design，支持可视化拖拽页面设计，提升 UI 开发效率。
- 内置强大的代码生成器，可根据数据库表结构自动生成后端 Controller、Service、Mapper 及前端页面代码。
- 完整集成 Shiro/JWT 鉴权与 RBAC 权限模型，实现细粒度的资源访问控制。
- 支持在线编码（Online Coding）功能，开发者在浏览器中即可编辑、调试并实时预览业务代码。
- 具备多数据源、分布式事务与工作流（Flowable）集成，满足企业级复杂业务需求。
- 采用微服务架构，兼容 Spring Cloud 生态，便于横向扩展和服务治理。

---
## 引用

- **GitHub 仓库**: [https://github.com/jeecgboot/JeecgBoot](https://github.com/jeecgboot/JeecgBoot)
- **DeepWiki**: [https://deepwiki.com/jeecgboot/JeecgBoot](https://deepwiki.com/jeecgboot/JeecgBoot)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [低代码](/tags/%E4%BD%8E%E4%BB%A3%E7%A0%81/) / [AI增强](/tags/ai%E5%A2%9E%E5%BC%BA/) / [代码生成](/tags/%E4%BB%A3%E7%A0%81%E7%94%9F%E6%88%90/) / [Java](/tags/java/) / [Vue3](/tags/vue3/) / [企业级](/tags/%E4%BC%81%E4%B8%9A%E7%BA%A7/) / [SaaS](/tags/saas/) / [敏捷开发](/tags/%E6%95%8F%E6%8D%B7%E5%BC%80%E5%8F%91/)
- 场景： [全栈开发](/scenarios/%E5%85%A8%E6%A0%88%E5%BC%80%E5%8F%91/) / [后端开发](/scenarios/%E5%90%8E%E7%AB%AF%E5%BC%80%E5%8F%91/) / [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [JeecgBoot开源低代码平台：集成AI应用与代码生成器]({{< relref "posts/20260131-github_trending-jeecgboot-jeecgboot-3.md" >}})
- [JeecgBoot：集成AI低代码平台与代码生成器的Java开发框架]({{< relref "posts/20260129-github_trending-jeecgboot-jeecgboot-3.md" >}})
- [JeecgBoot：集成AI低代码与代码生成器的企业级开发平台]({{< relref "posts/20260129-github_trending-jeecgboot-jeecgboot-7.md" >}})
- [JeecgBoot：集成AI低代码与代码生成器的企业级开发平台]({{< relref "posts/20260211-github_trending-jeecgboot-jeecgboot-8.md" >}})
- [JeecgBoot：集成AI低代码与代码生成器的企业级开发平台]({{< relref "posts/20260212-github_trending-jeecgboot-jeecgboot-8.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*