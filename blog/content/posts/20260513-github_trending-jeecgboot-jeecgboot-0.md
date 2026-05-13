---
title: "JeecgBoot：AI低代码平台，零代码与低代码双模式支持"
date: 2026-05-13T21:11:45+08:00
draft: false
entry_kind: "auto"
tags: ["低代码平台", "零代码", "AI开发", "Java", "代码生成", "Vue3", "Spring Boot", "知识库"]
categories: ["开发工具", "AI 工程"]
source: github_trending
description: "JeecgBoot是一个企业级AI增强的低代码开发平台，基于Spring Boot 3.5.5、Vue 3和Spring Cloud Alibaba构建。该平台旨在通过AI技术与低代码开发相结合，解决Java项目中的重复工作，提升开发效率。 核心定位 平台定位为“AI低代码平台”，支持“低代码+零代码”双模式开发。零代"
external_url: https://github.com/jeecgboot/JeecgBoot
scenarios: ["后端开发", "全栈开发", "AI/ML项目"]
---

# JeecgBoot：AI低代码平台，零代码与低代码双模式支持

> **原名**: jeecgboot /

      JeecgBoot

---

## 基本信息

- **描述**: 您好，您提供的内容已经是中文了。可能是您希望将其转换为**繁体中文**，或者原文原本是英文？

如果您需要，我可以将此内容转换为繁体中文：

---

AI低程式碼平臺，支援「低程式碼 + 零程式碼」雙模式：零程式碼 5 分鐘搭建業務系統，低程式碼模式一鍵生成前後端代碼。內建AI 應用，支援AI聊天、知識庫、流程編排、MCP與插件，支援各種模型。Skills能力實現：一句話畫流程圖、設計表單、生成系統。引領 AI生成→線上配置→代碼生成→手工合併的開發模式，解決Java專案80%的重複工作，快速提高效率，又不失靈活性。

---

如果您是想将其他语言（比如英文）的内容翻译成中文，请提供原始文本，我会为您翻译。
- **语言**: Java
- **星标**: 46,225 (+27 stars today)
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

JeecgBoot是一款面向企业级应用的AI低代码开发平台，采用“低代码+零代码”双模式运行。它通过AI能力与可视化工具的结合，实现从需求描述到代码生成的完整流程，帮助开发团队减少重复工作、提升交付效率。该平台适合需要快速构建内部系统或原型项目的Java开发团队。本文将围绕平台的核心功能、技术架构以及典型应用场景展开说明。

---
## 摘要

JeecgBoot是一个企业级AI增强的低代码开发平台，基于Spring Boot 3.5.5、Vue 3和Spring Cloud Alibaba构建。该平台旨在通过AI技术与低代码开发相结合，解决Java项目中的重复工作，提升开发效率。

#### 核心定位

平台定位为“AI低代码平台”，支持“低代码+零代码”双模式开发。零代码模式允许用户在5分钟内通过可视化配置快速搭建业务系统，无需编写代码；低代码模式则通过一键生成前后端代码的方式，加速开发流程。这种双模式设计兼顾了易用性和灵活性，既满足快速原型开发需求，也支持复杂业务场景的定制化开发。

#### AI能力集成

平台内置AI应用功能，支持AI聊天、知识库构建、流程编排以及MCP（Model Context Protocol）与插件扩展。在模型支持方面，平台具有广泛的兼容性，可对接各种大语言模型。Skills能力是平台的一大特色，用户可以通过自然语言描述实现一句话画流程图、设计表单、生成系统等功能，降低了使用门槛。

#### 开发模式创新

JeecgBoot引领了一种新型开发模式：AI生成→在线配置→代码生成→手工合并。通过这一流程，平台能够自动化处理项目中约80%的重复性工作，包括代码模板生成、业务逻辑填充、界面自动化构建等环节。开发者仍保留手工调整的灵活性，可以对生成的代码进行二次开发和优化，实现了自动化与个性化的平衡。

#### 技术架构

作为Java生态下的企业级解决方案，JeecgBoot采用主流的Spring Boot作为后端框架，前端使用Vue 3构建现代化用户界面，并通过Spring Cloud Alibaba实现微服务架构支持。这种技术选型确保了平台在企业级应用场景中的稳定性、可扩展性和生态兼容性。

---
## 评论

#### 总体判断

JeecgBoot 是一个功能覆盖面较广的企业级低代码平台，融合了低代码、零代码和 AI 能力，在开源 Java 低代码领域具有较高的知名度和社区活跃度。该项目在技术实现上采用经典的前后端分离架构，支持通过可视化配置快速搭建业务系统，同时保留了代码生成机制以满足定制化需求。从其定位来看，目标用户群体主要是需要快速交付企业内部管理系统的开发团队或独立开发者。

#### 事实与推断

该仓库目前星标数为 46,225，这是 GitHub 上的公开数据，表明项目在开源社区具有一定的认可度。描述中提到支持零代码和低代码双模式、内置 AI 应用（聊天、知识库、流程编排等）以及 Skills 能力（流程图生成、表单设计、代码生成），这些功能点在其官方文档中有具体说明。

从技术实现角度推断，该项目使用 Java 作为后端主语言、Vue3 作为前端框架，这与仓库结构中的模块划分（jeecg-boot 为后端、jeecgboot-vue3 为前端）相吻合。其提到的“一键生成前后端代码”功能，基于 Java 生态的代码生成工具（如 MyBatis-Plus、JHipster 等）的成熟实践，这一实现路径在技术上是可行的，但实际生成代码的质量和可维护性需要通过项目验证。

#### 适用场景

JeecgBoot 更适合以下场景：企业内部管理系统的快速原型开发；标准 CRUD 业务为主的后台管理系统；团队规模较小且需要快速交付的项目；对前端界面要求相对标准化、不追求高度自定义的场合。此外，对于希望借助 AI 能力降低配置难度的用户，其内置的 AI 功能可以提供一定的辅助作用。

#### 局限性

该平台存在以下局限需要客观认识。首先，复杂的业务逻辑和高度定制化的需求仍然需要手写代码实现，低代码平台无法完全替代传统开发。其次，前端技术栈锁定为 Vue3，若团队技术栈不匹配则存在学习成本和迁移成本。再次，低代码平台的固有挑战在于灵活性和效率之间的平衡，当业务需求偏离平台预设模式时，定制成本可能反而高于传统开发。最后，作为开源项目，其长期维护的可持续性取决于社区活跃度，需关注版本更新频率和问题响应速度。

#### 验证方式

建议通过以下方式验证平台是否适合自身需求：在本地环境完成基础部署和运行；使用零代码模式搭建一个简单的业务模块，评估配置体验和结果可用性；使用低代码模式生成一个包含增删改查功能的模块，检查生成代码的可读性和可扩展性；针对 AI 功能部分，实际测试其响应效果和稳定性。

---
## 技术分析

#### 架构概览
##### 模块划分
- **jeecg‑boot**：后端主体，采用多模块 Maven 项目，划分为 common、system、generator、workflow 等子模块，承载业务逻辑、权限、代码生成、流程引擎等核心功能。
- **jeecgboot‑vue3**：前端，采用 Vue3 + Element Plus，提供可视化表单、流程图、仪表盘等页面；前后端通过 RESTful API 与 WebSocket 交互。
- **AI 与插件层**：独立 AI 模块（AI 聊天、知识库、流程编排），通过 MCP（Model Control Protocol）与外部模型（GPT、Claude、文心等）对接，插件体系支持二次扩展。

##### 技术栈推断
基于项目结构与社区常见实践，推测后端使用 Spring Boot + MyBatis + Shiro/Spring Security + JWT；代码生成基于 Velocity/Freemarker 模板；工作流可能集成 Flowable/Activiti；缓存/消息队列使用 Redis、RocketMQ（未在官方文档明确列出，但为实现高并发所需的常见组合）。

#### 核心能力
##### 零代码/低代码双模式
- **零代码**：通过可视化拖拽在 5 分钟内完成表单、列表、审批流等业务页面的搭建，业务人员可直接上线使用。
- **低代码**：在页面配置完成后，一键生成前后端源码（Entity、Service、Controller、Vue 组件），开发者在生成代码基础上进行业务定制。

##### 代码生成机制
系统维护元数据模型（数据库表结构、业务对象属性），根据预设模板生成 CRUD、API、Swagger 文档、权限配置等。生成流程为“在线配置 → 模板渲染 → 代码输出 → 手工合并”，兼顾效率与灵活性。

##### AI 能力集成
- **AI 聊天**：集成大模型实现自然语言交互，可用于需求澄清、报表生成。
- **知识库**：对接向量库或传统文档库，支持语义检索。
- **流程编排 & Skills**：MCP 把模型输出转化为流程节点或表单布局，实现“一句话画流程图、设计表单、生成系统”。插件体系允许接入自定义模型或特定领域的 LLM。

#### 技术实现细节
##### 动态表单与流程引擎
可视化设计器生成 JSON 描述文件，运行时通过解析 JSON 动态渲染前端组件并在后端生成相应业务处理逻辑。流程引擎负责状态流转、节点审批与事件触发。

##### 插件与扩展机制
插件以 Jar 包形式部署，提供统一接口（IJeecgPlugin），平台在启动时扫描并加载。AI 插件遵循 MCP 协议，可热插拔切换底层模型。

#### 适用与不适用场景
##### 适用
- 中小型企业内部管理系统、审批流、报表系统，需求变化频繁但业务逻辑相对标准。
- 快速原型验证、业务概念验证（POC），帮助团队在数天内交付可运行 Demo。
- 需要 AI 辅助需求梳理、自动生成表单/流程的创新项目。

##### 不适用
- 对实时性、并发量要求极高的金融交易、实时游戏等场景，低代码的运行时解释成本难以满足。
- 业务模型极度复杂、领域模型需要深度定制的系统，生成代码的可维护性可能低于手写代码。
- 需要细粒度微服务治理、超大规模分布式架构的项目，平台默认的单体/模块化结构不一定匹配。

#### 学习与落地建议
##### 学习路径
1. **基础准备**：熟悉 Spring Boot、MyBatis、Spring Security（或 Shiro）以及 Vue3 前端生态（Vue Router、Pinia、Element Plus）。
2. **官方文档**：重点阅读 `jeecg‑boot/README.md` 与 `jeecgboot‑vue3/README.md`，了解项目结构与配置方式。
3. **代码生成实战**：通过平台的 “在线表单设计 → 生成代码 → 本地合并” 流程，手动体验一次完整闭环。
4. **AI 集成**：参考 `README‑AI.md`，配置 MCP 与所选 LLM（OpenAI、Claude 等），实现一个 AI 聊天或自动生成表单的示例。
5. **插件开发**：阅读插件接口 `IJeecgPlugin`，自行实现一个业务校验插件，加深对平台扩展机制的理解。

##### 落地注意事项
- **版本匹配**：后端依赖 Spring Boot 版本需与前端 Vue3 依赖保持兼容，避免运行时冲突。
- **安全审计**：平台默认提供基础的 RBAC，落地生产前需对权限模型、接口鉴权、数据脱敏进行专项审计。
- **代码合并规范**：生成的代码与手写代码应遵循统一的命名与分层规范，建议在 Git 中使用分支管理 “生成代码” 与 “业务定制” 两部分，以便后续升级。
- **性能调优**：在高并发场景下，开启 Redis 缓存、数据库连接池调优，并根据业务需求决定是否将关键业务迁移至手写微服务。
- **社区与支持**：利用官方社区、Issue 跟踪以及 Gitee/GitHub 的 Stars 数量判断活跃度，获取最新的插件与模板更新。

#### 小结
JeecgBoot 通过 **零代码可视化 + 低代码生成 + AI 能力** 的三层架构，显著降低企业内部系统的开发门槛。其技术栈以 **Java（Spring Boot）+ Vue3** 为核心，配合插件化的 AI（MCP）与代码生成引擎，适用于需求多变、业务模型相对标准的中低端项目。对于性能要求极高或业务模型极度复杂的系统，则需评估生成代码的可维护性与平台的约束风险。落地时遵循 “生成‑合并‑审计” 的规范流程，并充分利用社区插件与模板，能够在保持开发效率的同时，确保系统的长期可演进性。

---
## 学习要点

- JeecgBoot 是基于 Spring Boot + Vue 的低代码快速开发平台，提供在线业务建模和代码生成功能，显著提升开发效率。
- 采用前后端分离架构，Vue 前端与 Spring Boot 后端实现模块化、可维护的代码结构。
- 集成 Shiro + JWT 实现细粒度 RBAC 权限控制和 JWT 无状态认证，确保系统安全。
- 内置 Flowable 工作流引擎，支持流程设计、审批和业务流转的自动化配置。
- 支持微服务架构，集成 Nacos、Sentinel 等中间件，实现服务治理、负载均衡和容错。
- 支持多数据库（MySQL、Oracle、SQL Server 等），提供灵活的数据源切换与配置。
- 提供前后端 CRUD 代码生成器，一键生成前后端代码，减少重复编码工作。

---
## 引用

- **GitHub 仓库**: [https://github.com/jeecgboot/JeecgBoot](https://github.com/jeecgboot/JeecgBoot)
- **DeepWiki**: [https://deepwiki.com/jeecgboot/JeecgBoot](https://deepwiki.com/jeecgboot/JeecgBoot)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [低代码平台](/tags/%E4%BD%8E%E4%BB%A3%E7%A0%81%E5%B9%B3%E5%8F%B0/) / [零代码](/tags/%E9%9B%B6%E4%BB%A3%E7%A0%81/) / [AI开发](/tags/ai%E5%BC%80%E5%8F%91/) / [Java](/tags/java/) / [代码生成](/tags/%E4%BB%A3%E7%A0%81%E7%94%9F%E6%88%90/) / [Vue3](/tags/vue3/) / [Spring Boot](/tags/spring-boot/) / [知识库](/tags/%E7%9F%A5%E8%AF%86%E5%BA%93/)
- 场景： [后端开发](/scenarios/%E5%90%8E%E7%AB%AF%E5%BC%80%E5%8F%91/) / [全栈开发](/scenarios/%E5%85%A8%E6%A0%88%E5%BC%80%E5%8F%91/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [JeecgBoot：集成AI低代码平台与代码生成器的Java开发框架]({{< relref "posts/20260129-github_trending-jeecgboot-jeecgboot-3.md" >}})
- [JeecgBoot：AI 驱动的低代码平台，支持零代码与代码生成双模式]({{< relref "posts/20260317-github_trending-jeecgboot-jeecgboot-2.md" >}})
- [JeecgBoot：AI 驱动的低代码平台，支持零代码搭建与代码生成]({{< relref "posts/20260318-github_trending-jeecgboot-jeecgboot-2.md" >}})
- [JeecgBoot：AI低代码平台集成代码生成器与知识库]({{< relref "posts/20260130-github_trending-jeecgboot-jeecgboot-3.md" >}})
- [JeecgBoot：集成AI低代码与代码生成器的企业级开发平台]({{< relref "posts/20260129-github_trending-jeecgboot-jeecgboot-7.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*