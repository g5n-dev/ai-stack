---
title: "JeecgBoot：AI低代码平台，低代码零代码双模式"
date: 2026-05-13T12:26:22+08:00
draft: false
entry_kind: "auto"
tags: ["低代码", "零代码", "代码生成", "Java", "AI应用", "知识库", "流程编排", "开发效率"]
categories: ["开发工具"]
source: github_trending
description: "JeecgBoot 是一个基于 Java 的企业级 AI 低代码开发平台，同时提供零代码和低代码两种开发模式。零代码模式允许用户在5分钟内通过可视化操作搭建业务系统，而低代码模式则能够一键生成前后端代码，大幅提升开发效率。该平台内置 AI 能力，支持聊天、知识库、流程编排等功能，适合需要快速交付项目或希望减少重复编码工"
external_url: https://github.com/jeecgboot/JeecgBoot
scenarios: ["Web应用开发", "全栈开发", "后端开发"]
---

# JeecgBoot：AI低代码平台，低代码零代码双模式

> **原名**: jeecgboot /

      JeecgBoot

---

## 基本信息

- **描述**: AI低代码平台，支持「低代码 + 零代码」双模式：零代码 5 分钟搭建业务系统，低代码模式一键生成前后端代码。内置AI应用，支持AI聊天、知识库、流程编排、MCP与插件，支持各种模型。Skills能力实现：一句话画流程图、设计表单、生成系统。引领 AI生成→在线配置→代码生成→手工合并的开发模式，解决Java项目80%的重复工作，快速提高效率，又不失灵活性。
- **语言**: Java
- **星标**: 46,218 (+28 stars today)
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

JeecgBoot 是一个基于 Java 的企业级 AI 低代码开发平台，同时提供零代码和低代码两种开发模式。零代码模式允许用户在5分钟内通过可视化操作搭建业务系统，而低代码模式则能够一键生成前后端代码，大幅提升开发效率。该平台内置 AI 能力，支持聊天、知识库、流程编排等功能，适合需要快速交付项目或希望减少重复编码工作的 Java 开发团队。本文将介绍 JeecgBoot 的核心特性、技术架构以及典型应用场景。

---
## 评论

#### 总体判断

JeecgBoot是一款成熟度较高的Java低代码平台，在同类型开源项目中拥有较大的用户基数和社区活跃度。其“双模式”设计理念——零代码快速搭建与低代码深度定制相结合——在理论上能够覆盖从简单表单到复杂业务系统的多种开发需求。内置AI能力的整合是近年来低代码平台演进的方向之一，JeecgBoot在这方面进行了探索。不过，“解决Java项目80%重复工作”这一表述更接近营销定位，实际效果需要结合具体业务场景评估。

#### 事实依据

以下信息来自仓库公开数据：仓库使用Java语言开发，星标数为46,218，表明其在GitHub上具有较高的关注度。官方描述明确了平台支持可视化表单设计、流程编排、报表生成，以及前后端代码一键生成等功能。从技术栈来看，前端基于Vue3、后端基于SpringBoot的组合符合当前企业级Java开发的主流选择。仓库中包含多个README文件和模块划分，说明项目结构相对完整。

#### 适用场景

该平台适合以下场景：企业内部管理系统的快速原型开发与迭代；中小企业信息化建设中标准业务流程的快速落地；开发团队需要快速生成增删改查类业务模块以缩短项目周期；需要对现有系统进行功能扩展但缺乏足够前端开发资源的情况。对于需要深度定制复杂业务逻辑、对性能要求极高、或依赖特定技术栈的项目，需要进一步评估。

#### 局限性

从技术特性推断，低代码平台在处理高度定制化需求时往往存在瓶颈。当业务逻辑超出可视化配置范围时，仍需编写代码，这与“低代码”而非“无代码”的定位相符。AI生成代码的质量、上下文理解能力以及对特定业务场景的适配程度，目前缺乏公开的量化评估数据。平台的学习曲线取决于团队对Java生态和Vue前端的熟悉程度，并非完全零门槛。

#### 验证方式

建议从以下维度进行评估：本地部署官方Demo，实际操作表单设计和流程配置；针对目标业务场景，使用平台的代码生成功能，审查生成代码的结构与可维护性；查阅官方文档中关于AI功能的使用案例和限制说明；参考社区反馈和Issue处理效率，了解项目维护的持续性。

---
## 技术分析

#### 架构分析

从仓库结构来看，JeecgBoot 采用经典的前后端分离架构。**已知事实**：主仓库下包含 `jeecg-boot`（后端模块）和 `jeecgboot-vue3`（前端模块）两个子项目。后端基于 Spring Boot 体系构建，前端采用 Vue3 + TypeScript，这表明其遵循标准的 B/S 分层模型。**推断**：模块化设计允许企业根据需求选择性部署，前端独立仓库也便于前后端团队并行开发和版本管理。

核心架构层面，JeecgBoot 引入了 AI 能力层作为差异化设计，这一层负责与各种大语言模型交互，实现自然语言驱动的功能生成。根据仓库描述，平台支持 MCP（Model Context Protocol）协议和插件化扩展，这意味着 AI 能力并非硬编码，而是通过标准化的协议实现解耦。

#### 核心能力

**零代码能力**体现在可视化表单设计和流程编排上。用户通过拖拽式配置即可完成业务表单构建，内置的审批流程引擎支持常见的流转逻辑。**低代码能力**则是其核心竞争力：一键生成前后端代码。用户完成数据模型设计后，系统自动生成 CRUD 接口、Vue 页面及权限配置代码，覆盖了企业管理系统 80% 的重复性编码工作。

AI 集成是第三个关键能力。平台内置 AI 聊天界面，支持接入多种大模型；知识库功能允许企业上传私有文档；Skills 能力可实现"一句话生成流程图"、"一句话设计表单"等场景化操作。**推断**：这些 AI 能力主要服务于开发效率提升，而非端到端的业务自动化。

#### 技术实现

从语言标签可见，后端完全采用 Java 技术栈。**已知事实**：Spring Boot 是基础框架，代码生成器基于 FreeMarker 模板引擎实现。**推断**：持久层可能采用 MyBatis-Plus 或通用 Mapper，权限管理大概率基于 Shiro 或 Spring Security。

前端技术选型紧随主流：Vue3 Composition API + TypeScript + Vite 构建工具。组件库层面，从 Vue2 向 Vue3 的迁移说明项目在持续跟进技术演进。**技术亮点**：平台封装了大量企业级组件（数据表格、表单验证、文件上传等），这降低了业务开发门槛，但也意味着前端开发者需要熟悉这套组件体系。

#### 适用与不适用场景

**适用场景**：企业内部管理系统（OA、CRM、ERP 基础模块）、管理后台类项目、政务系统、创业公司 MVP 快速原型开发。这些场景的共同特征是数据结构相对标准、CRUD 操作密集、界面以表格和表单为主。

**不适用场景**：实时交互要求高的应用（如在线协作工具）、复杂计算密集型系统、移动端原生应用、高并发互联网产品。JeecgBoot 的定位本质是"快速构建标准业务"，而非应对高性能或复杂交互需求。**推断**：对于需要深度定制化 UI 或特殊业务流程的项目，低代码的约束反而会成为限制。

#### 学习与落地建议

**学习路径建议**：首先通读官方文档和 README-AI.md 了解设计理念；随后本地启动前后端项目，跟随 Quick Start 完成一个简单模块的创建；重点研究代码生成规则和扩展点，这决定了后续定制化开发的天花板。

**落地注意事项**：一是需求评估阶段需判断业务复杂度是否落在平台能力范围内；二是团队需理解"生成代码 + 手工合并"的工作模式，避免全盘低代码或全盘手写两个极端；三是 AI 功能依赖大模型 API，需提前评估成本和数据安全要求。**推断**：生产环境部署时，建议对生成的代码进行 review，建立团队内部的代码规范约束。

---
## 学习要点

- 基于 Spring Boot + Vue3 的前后端分离低代码平台，提供完整的微服务架构支持
- 通过可视化配置实现 CRUD、列表、表格等常用功能，大幅提升开发效率
- 内置强大的代码生成器，支持一键生成前后端代码及 API 文档
- 提供完善的权限管理、角色、菜单、数据字典等企业级功能，开箱即用
- 采用模块化设计，业务模块可独立部署，满足微服务拆分需求
- 兼容国产化环境（如国产数据库、操作系统），适合信创项目
- 社区活跃、文档丰富，支持在线演示和持续迭代升级

---
## 引用

- **GitHub 仓库**: [https://github.com/jeecgboot/JeecgBoot](https://github.com/jeecgboot/JeecgBoot)
- **DeepWiki**: [https://deepwiki.com/jeecgboot/JeecgBoot](https://deepwiki.com/jeecgboot/JeecgBoot)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/)
- 标签： [低代码](/tags/%E4%BD%8E%E4%BB%A3%E7%A0%81/) / [零代码](/tags/%E9%9B%B6%E4%BB%A3%E7%A0%81/) / [代码生成](/tags/%E4%BB%A3%E7%A0%81%E7%94%9F%E6%88%90/) / [Java](/tags/java/) / [AI应用](/tags/ai%E5%BA%94%E7%94%A8/) / [知识库](/tags/%E7%9F%A5%E8%AF%86%E5%BA%93/) / [流程编排](/tags/%E6%B5%81%E7%A8%8B%E7%BC%96%E6%8E%92/) / [开发效率](/tags/%E5%BC%80%E5%8F%91%E6%95%88%E7%8E%87/)
- 场景： [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/) / [全栈开发](/scenarios/%E5%85%A8%E6%A0%88%E5%BC%80%E5%8F%91/) / [后端开发](/scenarios/%E5%90%8E%E7%AB%AF%E5%BC%80%E5%8F%91/)

### 相关文章

- [JeecgBoot：AI低代码平台集成代码生成器与知识库]({{< relref "posts/20260130-github_trending-jeecgboot-jeecgboot-3.md" >}})
- [JeecgBoot：集成AI低代码与代码生成器的企业级开发平台]({{< relref "posts/20260129-github_trending-jeecgboot-jeecgboot-7.md" >}})
- [JeecgBoot：AI 驱动的低代码平台，支持零代码与代码生成双模式]({{< relref "posts/20260317-github_trending-jeecgboot-jeecgboot-2.md" >}})
- [JeecgBoot：AI 驱动的低代码平台，支持零代码搭建与代码生成]({{< relref "posts/20260318-github_trending-jeecgboot-jeecgboot-2.md" >}})
- [JeecgBoot开源低代码平台：集成AI应用与代码生成器]({{< relref "posts/20260131-github_trending-jeecgboot-jeecgboot-3.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*