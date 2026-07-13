---
title: "Java低代码平台JeecgBoot：AI+零代码双模式"
date: 2026-05-13T22:38:17+08:00
draft: false
entry_kind: "auto"
tags: ["低代码平台", "零代码", "AI生成", "代码生成", "开源项目", "Java", "Vue3", "Spring"]
categories: ["开发工具", "AI 工程"]
source: github_trending
description: "项目简介 JeecgBoot 是企业级 AI 低代码平台，基于 Spring Boot 3.5.5、Vue 3、Spring Cloud Alibaba 2023.0.3.3 构建，支持“零代码 + 低代码”双模式。零代码可在 5 分钟内完成业务系统搭建，低代码模式一键生成前后端代码，帮助开发者快速交付。 核心能力 1"
external_url: https://github.com/jeecgboot/JeecgBoot
scenarios: ["全栈开发", "Web应用开发", "AI/ML项目"]
---

# Java低代码平台JeecgBoot：AI+零代码双模式

> **原名**: jeecgboot /

      JeecgBoot

---

## 基本信息

- **描述**: # 中文优化版本

**AI低代码平台**，支持「低代码 + 零代码」双模式：零代码 5 分钟即可搭建业务系统，低代码模式一键生成前后端代码。内置 AI 应用，支持 AI 聊天、知识库、流程编排、MCP 与插件扩展，全面兼容各类大模型。Skills 能力实现：一句话生成流程图、设计表单、构建系统。引领「AI 生成 → 在线配置 → 代码生成 → 手工合并」的开发新范式，解决 Java 项目 80% 的重复性工作，显著提升开发效率，同时保留足够的灵活性。

---

## 主要调整说明

1. **统一标点符号**：使用中文全角冒号（：）替代半角冒号
2. **调整语句结构**：
   - “一句话画流程图” → “一句话生成流程图”
   - “生成系统” → “构建系统”
   - “解决 Java 项目 80% 的重复工作” → “解决 Java 项目 80% 的重复性工作”
3. **优化表达**：
   - “解决…工作，快速提高效率，又不失灵活性” → “显著提升开发效率，同时保留足够的灵活性”
   - 明确「AI生成→在线配置→代码生成→手工合并」为“开发新范式”
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

JeecgBoot 是一款面向企业的 AI 低代码开发平台，同时支持零代码和低代码两种模式。零代码场景下，5 分钟即可搭建业务系统；低代码模式则能一键生成前后端代码，大幅减少 Java 项目中的重复性工作。平台内置 AI 能力，兼容主流大模型，支持通过自然语言生成流程图、设计表单和构建系统。本文将介绍其核心功能、技术架构以及实际开发中的典型应用场景。

---
## 摘要

#### 项目简介
JeecgBoot 是企业级 AI 低代码平台，基于 Spring Boot 3.5.5、Vue 3、Spring Cloud Alibaba 2023.0.3.3 构建，支持“零代码 + 低代码”双模式。零代码可在 5 分钟内完成业务系统搭建，低代码模式一键生成前后端代码，帮助开发者快速交付。

#### 核心能力
1. **代码生成**：基于 Maven 的代码生成器，自动生成 Java、Vue 等代码。
2. **零代码配置**：可视化表单、流程、报表，通过拖拽完成业务建模。
3. **AI 增强**：内置 AI 聊天、知识库、流程编排、MCP 与插件体系，支持多模型；提供“一句话画流程图、设计表单、生成系统”等 Skills。
4. **灵活性**：生成的代码可直接手工合并，满足企业定制化需求。

#### 技术架构
- 后端：Spring Boot 3.5.5 + MyBatis‑Plus + ShardingSphere
- 前端：Vue 3 + Element Plus + Vite
- 微服务：Spring Cloud Alibaba 2023.0.3.3（Gateway、Nacos、Sentinel）
- AI 引擎：支持 OpenAI、百度文心、阿里通义等多种模型。

#### 价值与定位
JeecgBoot 通过 AI 生成 → 在线配置 → 代码生成 → 手工合并的工作流，解决 Java 项目 80% 重复工作，显著提升开发效率，同时保留代码的可控性和可维护性。项目已在 GitHub 获得约 46,200 星，广泛应用于企业数字化转型。

---
## 评论

#### 总体判断
JeecgBoot 在开源低代码平台中具备较高的成熟度与社区活跃度，适合快速构建中小型企业业务系统。

#### 依据与适用场景
事实：星标 46,225，Java 技术栈，提供零代码 5 分钟搭建业务系统和低代码一键生成前后端代码；官方宣称解决 Java 项目 80% 重复工作。推断：在管理后台、数据采集、审批流等典型业务场景下，可显著缩短交付周期，适合团队快速交付原型或内部工具。

#### 局限与风险
推断：对复杂业务规则或性能要求极高的系统，生成的代码往往需要手工二次改造；AI 生成结果的准确性受模型和提示影响，需人工审查；平台依赖社区维护，长期兼容性需评估。

#### 验证方式
建议：在本地使用脚手架生成 CRUD 模块，运行单元测试和压测，检查生成代码的可读性；对 AI 画图和流程生成进行多轮对话测试，评估准确率和可接受度；对比手工实现与自动生成的差异，评估维护成本。

---
## 技术分析

#### 架构概览

JeecgBoot采用前后端分离的微服务架构（根据仓库结构推断），整体分为三个主要部分：

**前端层**基于Vue3生态，使用Vite作为构建工具，整合Element Plus UI组件库和Pinia状态管理。jeecgboot-vue3目录包含完整的前端实现。

**后端层**基于Spring Boot框架（根据Java语言特性和常见Java生态推断），采用Maven进行依赖管理。jeecg-boot目录承载核心业务逻辑。

**数据层**支持MySQL、PostgreSQL等主流关系型数据库（根据ORM配置推断），同时提供Redis缓存支持。

#### 核心能力分析

**低代码开发能力**：平台提供在线表单设计器、流程设计器和报表设计器，支持可视化配置业务模块。根据仓库描述，可实现"零代码5分钟搭建业务系统"，这表明平台封装了大量通用业务逻辑模板。

**AI集成能力**：内置AI应用框架，支持对话式交互、知识库检索、流程编排以及MCP协议扩展。这一能力使其区别于传统低代码平台，理论上可实现"一句话生成流程图、设计表单"等高级功能。

**代码生成引擎**：低代码模式下可一键生成前后端代码，生成的代码结构规范，便于后续手工调整和扩展。这种"生成-配置-合并"的开发模式旨在平衡开发效率与代码可控性。

#### 技术实现特点

**模块化设计**：仓库采用多模块Maven结构，将公共组件、业务模块、代码生成器等独立管理。这种设计便于按需引入和版本控制。

**插件化扩展**：支持通过插件机制扩展功能模块，AI能力以插件形式集成。这种设计提升了平台的灵活性和可维护性。

**前后端代码模板**：代码生成器预设了前后端代码模板，生成的代码遵循一定规范，降低了团队学习成本。

#### 适用与不适用场景

**适用场景**：
- 内部管理系统快速原型开发
- 标准化业务流程的中台系统搭建
- 中小型企业的信息化系统建设
- 需要快速交付的后台管理模块

**不适用场景**：
- 对性能要求极高的实时交易系统（低代码平台固有开销）
- 高度定制化的复杂业务逻辑（平台抽象可能限制灵活性）
- 超大并发量场景（架构设计以功能开发为主）
- 需要深度前端定制的交互型应用

#### 学习与落地建议

**学习路径**：建议从官方文档入手，重点掌握在线设计器的使用方法和代码生成器的配置选项。AI功能的实际效果需要根据具体模型能力评估。

**落地要点**：
1. 评估业务复杂度与平台能力的匹配度
2. 建立团队内部的代码规范，明确哪些生成代码需要优化
3. 预留手工代码合并的缓冲区，避免过度依赖自动生成
4. 关注平台社区活跃度和版本迭代频率，确保长期维护可行性

**风险提示**：作为开源项目，商业化项目落地时需评估社区支持力度和技术债务风险。

---
## 学习要点

- JeecgBoot 是基于 Spring Boot 的低代码开发平台，提供前后端分离的整体解决方案
- 支持在线表单、报表、权限、流程等业务功能可视化配置，大幅降低开发成本
- 集成 MyBatis‑Plus、Shiro、JWT 等技术，实现高效持久层和统一身份认证
- 前端采用 Vue、Element UI、Axios 等，实现响应式管理后台界面
- 提供代码生成器，可根据数据库表结构自动生成前后端代码，加速开发迭代
- 支持微服务架构，可通过 Spring Cloud Alibaba 进行分布式部署和弹性扩展
- 拥有丰富的插件生态和详细文档，便于二次开发和社区贡献

---
## 引用

- **GitHub 仓库**: [https://github.com/jeecgboot/JeecgBoot](https://github.com/jeecgboot/JeecgBoot)
- **DeepWiki**: [https://deepwiki.com/jeecgboot/JeecgBoot](https://deepwiki.com/jeecgboot/JeecgBoot)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [低代码平台](/tags/%E4%BD%8E%E4%BB%A3%E7%A0%81%E5%B9%B3%E5%8F%B0/) / [零代码](/tags/%E9%9B%B6%E4%BB%A3%E7%A0%81/) / [AI生成](/tags/ai%E7%94%9F%E6%88%90/) / [代码生成](/tags/%E4%BB%A3%E7%A0%81%E7%94%9F%E6%88%90/) / [开源项目](/tags/%E5%BC%80%E6%BA%90%E9%A1%B9%E7%9B%AE/) / [Java](/tags/java/) / [Vue3](/tags/vue3/) / [Spring](/tags/spring/)
- 场景： [全栈开发](/scenarios/%E5%85%A8%E6%A0%88%E5%BC%80%E5%8F%91/) / [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [JeecgBoot：集成AI低代码平台与代码生成器的Java开发框架]({{< relref "posts/20260129-github_trending-jeecgboot-jeecgboot-3.md" >}})
- [Vue3低代码平台DSL转Vue3组件代码生成机制解析]({{< relref "posts/20260313-juejin-ai-驱动的-vue3-应用开发平台-深入探究六双向代码转换之dsl到vue代码生成-2.md" >}})
- [JeecgBoot：AI 驱动的低代码平台，支持零代码与代码生成双模式]({{< relref "posts/20260317-github_trending-jeecgboot-jeecgboot-2.md" >}})
- [JeecgBoot：AI 驱动的低代码平台，支持零代码搭建与代码生成]({{< relref "posts/20260318-github_trending-jeecgboot-jeecgboot-2.md" >}})
- [JeecgBoot：集成AI低代码与代码生成器的企业级开发平台]({{< relref "posts/20260129-github_trending-jeecgboot-jeecgboot-7.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*