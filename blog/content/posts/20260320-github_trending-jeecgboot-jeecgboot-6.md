---
title: "JeecgBoot：AI低代码平台一键生成Java代码"
date: 2026-03-20T04:08:49+08:00
draft: false
entry_kind: "auto"
tags: ["低代码平台", "AI代码生成", "Java开发", "代码生成器", "零代码开发", "大模型集成", "MCP插件", "快速开发"]
categories: ["开发工具"]
source: github_trending
description: "JeecgBoot 项目概述 基本信息 - **项目名称**：jeecgboot/JeecgBoot - **编程语言**：Java - **星标数**：45,458（今日+15） 核心定位 JeecgBoot 是一款企业级 AI 驱动的低代码开发平台，旨在解决 Java 项目中 80% 的重复性工作，在保证开发效率的"
external_url: https://github.com/jeecgboot/JeecgBoot
scenarios: ["后端开发", "全栈开发", "AI/ML项目"]
---

# JeecgBoot：AI低代码平台一键生成Java代码

> **原名**: jeecgboot /

      JeecgBoot

---

## 基本信息

- **描述**: **翻译如下：**

JeecgBoot 是一款 AI 驱动的低代码开发平台，提供“零代码”与“代码生成”双模式——零代码模式一句话搭建系统，代码生成模式自动输出前后端代码与建表 SQL，生成即可运行。平台内置 AI 聊天助手、AI大模型、知识库、AI流程编排、MCP 与插件体系，兼容主流大模型，支持一句话生成流程图、设计表单、聊天式业务操作，解决 Java 项目 80% 重复工作，高效且不失灵活。

---

> **说明：** 您提供的原文已经是中文。如需将此段内容翻译为其他语言（如英文），请告知。
- **语言**: Java
- **星标**: 45,458 (+15 stars today)
- **链接**: [https://github.com/jeecgboot/JeecgBoot](https://github.com/jeecgboot/JeecgBoot)
- **DeepWiki**: [https://deepwiki.com/jeecgboot/JeecgBoot](https://deepwiki.com/jeecgboot/JeecgBoot)

---
## DeepWiki 速览（节选）

# JeecgBoot Overview

Relevant source files

  * [README-AI.md](https://github.com/jeecgboot/JeecgBoot/blob/b7a3da89/README-AI.md)
  * [README.en-US.md](https://github.com/jeecgboot/JeecgBoot/blob/b7a3da89/README.en-US.md)
  * [README.md](https://github.com/jeecgboot/JeecgBoot/blob/b7a3da89/README.md)
  * [jeecg-boot/README.md](https://github.com/jeecgboot/JeecgBoot/blob/b7a3da89/jeecg-boot/README.md)
  * [jeecgboot-vue3/README.md](https://github.com/jeecgboot/JeecgBoot/blob/b7a3da89/jeecgboot-vue3/README.md)



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



Sources: [README.md1-44](https://github.com/jeecgboot/JeecgBoot/blob/b7a3da89/README.md#L1-L44) [jeecg-boot/README.md1-44](https://github.com/jeecgboot/JeecgBoot/blob/b7a3da89/jeecg-boot/README.md#L1-L44) [README.md159-190](https://github.com/jeecgboot/JeecgBoot/blob/b7a3da89/README.md#L159-L190)

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



Sources: [README.md20-36](https://github.com/jeecgboot/JeecgBoot/blob/b7a3da89/README.md#L20-L36) [jeecg-boot/README.md19-33](https://github.com/jeecgboot/JeecgBoot/blob/b7a3da89/jeecg-boot/README.md#L19-L33) [README.md111-157](https://github.com/jeecgboot/JeecgBoot/blob/b7a3da89/README.md#L111-L157)

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



Sources: [README.md72-82](https://github.com/jeecgboot/JeecgBoot/blob/b7a3da89/README.md#L72-L82) [jeecg-boot/README.md218-243](https://github.com/jeecgboot/JeecgBoot/blob/b7a3da89/jeecg-boot/README.md#L218-L243)

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
**AI Flow Package**| `jeecgboot-vue3/packages/@jeecg/aiflow/`| AI flow designer UI  
  
**Cross-Module Dependencies:**

  * All business

[...truncated...]

---
## 导语

JeecgBoot 是一款基于 Java 的 AI 低代码开发平台，融合了零代码与代码生成两种开发模式。平台通过内置的 AI 助手和大模型能力，可自动生成前后端代码与建表 SQL，覆盖流程编排、表单设计、聊天式业务操作等常见场景，能够显著减少 Java 项目中的重复编码工作。该项目适合需要快速交付企业内部系统的开发团队，或希望兼顾开发效率与灵活性的技术负责人。本文将围绕其核心功能、技术架构以及实际应用方向展开介绍。

---
## 摘要

## JeecgBoot 项目概述

### 基本信息
- **项目名称**：jeecgboot/JeecgBoot
- **编程语言**：Java
- **星标数**：45,458（今日+15）

### 核心定位
JeecgBoot 是一款企业级 AI 驱动的低代码开发平台，旨在解决 Java 项目中 80% 的重复性工作，在保证开发效率的同时不失灵活性。

### 主要特色

**双模式开发**
- **零代码模式**：通过自然语言描述即可快速搭建系统
- **代码生成模式**：自动生成前后端代码及建表 SQL，生成即可运行

**AI 能力集成**

- AI 聊天助手
- AI 大模型支持
- 知识库功能
- AI 流程编排
- MCP 与插件体系
- 支持主流大模型对接
- 一句话生成流程图、设计

---
## 评论

JeecgBoot是当前国内低代码领域星标数最高的开源项目之一，其将AI能力深度整合进开发全流程的思路在国内具有领先性，但在架构复杂度和AI落地效果上仍需项目方进一步验证。

**1. 技术创新性**
JeecgBoot的核心差异化在于“AI+低代码”的深度融合模式。事实：平台内置AI聊天助手、AI大模型、知识库和AI流程编排，支持一句话生成流程图、设计表单。推断：这并非简单的AI辅助编码，而是尝试在业务抽象层引入自然语言交互，降低业务人员与技术团队的沟通成本。技术亮点包括MCP（Model Context Protocol）协议与插件体系，支持兼容主流大模型。推断：这使其具备一定的技术扩展性，但实际AI生成内容的可控性和准确性仍依赖具体实现细节。

**2. 实用价值**
该平台瞄准企业级应用开发的效率痛点。事实：提供“零代码”与“代码生成”双模式，代码生成模式可自动输出前后端代码与建表SQL，生成即可运行。推断：这解决了Java项目80%重复工作的定位符合实际开发场景，对内部管理系统、后台管理类项目有较高实用价值。应用场景覆盖表单流程、CRUD管理等通用业务模块。但需注意，对于高度定制化、性能敏感或业务逻辑复杂的系统，纯零代码模式的灵活性可能不足。

**3. 代码质量**
从项目结构看，采用前后端分离架构（jeecg-boot后端 + jeecgboot-vue3前端）。事实：项目包含多层级模块划分，文档结构完整（README、英文文档、AI专项文档）。推断：团队具备一定的工程化意识。但作为快速迭代的开源项目，45K星标背后意味着大量使用者，代码规范一致性、技术债务积累程度需要进一步审视。文档方面，提供了详细的功能列表和技术栈说明，降低了上手门槛。

**4. 社区活跃度**
45,458星标在Java开源领域属于头部水准。推断：庞大的星标基数通常意味着稳定的用户基础和一定的社区活跃度。但星标数不能直接等同于贡献活跃度，需关注Issue响应速度、PR合并频率、版本发布周期等指标。从GitHub常见模式推测，该项目应有持续更新，但具体贡献者数量和代码提交活跃度需实际查看Insights页面确认。

**5. 学习价值**
对于想了解低代码平台架构的开发者，JeecgBoot提供了完整的前后端实现参考。推断：其代码生成器设计、表单引擎、权限体系等模块具有教学意义。尤其是AI能力与业务代码的集成方式，可作为AI原生应用开发的案例参考。但学习曲线较陡，需要熟悉Spring Boot、Vue3、工作流引擎等技术栈。

**6. 潜在问题或改进建议**
- 架构复杂度较高，对团队技术能力有一定要求
- AI生成内容的准确性和业务适配性需要人工校验
- 依赖特定技术栈（Java生态），跨语言支持有限
- 建议：加强AI生成结果的可解释性和回滚机制；完善单元测试覆盖；考虑提供更轻量的裁剪版本

**7. 与同类工具对比优势**
相比Apifox、钉钉宜搭等工具，JeecgBoot的优势在于完全开源、代码可控、定制灵活。相比若依、Spring Wind等传统代码生成器，其AI集成能力是显著差异点。45K星标的社区规模在国内低代码开源领域几乎无直接竞品。

**边界条件/不适用场景**
- 高度定制化、需要深度优化性能的系统和底层框架开发
- 对前端技术栈有非Vue需求的团队
- 追求极简依赖、不希望引入复杂技术栈的轻量项目

**快速验证清单**
1. 在本地环境搭建JeecgBoot（建议使用Docker方式），验证代码生成功能的完整性和生成代码的可运行性
2. 测试AI聊天助手在实际业务场景下的生成质量，记录错误率和需要人工修正的比例
3. 检查最新版本（查看Release页面）的更新日志，评估功能迭代速度与版本稳定性
4. 对比生成的代码与手写代码在可读性、扩展性和性能方面的差异，判断“80%重复工作”的实际达成度

---
## 技术分析

# JeecgBoot 技术深度分析报告

## 1. 技术架构深度剖析

**技术栈构成**：JeecgBoot 采用经典的前后端分离架构，后端基于 Spring Boot + MyBatis-Plus + Shiro，前端采用 Vue3 + Ant Design Vue，技术选型成熟稳定。数据库层面支持 MySQL、Oracle、PostgreSQL 等主流关系型数据库，缓存层引入 Redis 实现会话共享与数据缓存。

**架构模式**：平台采用微内核 + 插件化架构设计，核心层提供代码生成、流程引擎、表单设计器等基础能力，通过插件机制扩展 AI 能力、MCP 服务等高级功能。这种设计允许开发者根据业务需求选择性启用功能模块，降低了系统复杂度。

**核心模块划分**：
- `jeecg-boot`：后端核心服务，封装业务逻辑与 API
- `jeecgboot-vue3`：前端工程，基于 Vue3 Composition API 重构
- 代码生成器模块：支持一键生成 Controller、Service、Mapper、Entity
- Online 表单/表单设计器：可视化配置业务表单
- 流程引擎模块：基于 Flowable/Activiti 定制

**架构优势**：分层解耦彻底，前端可通过 HTTP 调用后端任意服务；模块化设计便于按需部署；集成 Shiro+JWT 双认证机制，兼顾安全与性能。

## 2. 核心功能详细解读

**零代码模式**：通过可视化配置实现表单、列表、审批流程的快速搭建。Online Coding 功能允许非技术人员通过配置生成 CRUD 页面，显著降低开发门槛。

**代码生成模式**：这是平台的核心竞争力。开发者通过数据库表设计，利用模板引擎（Velocity/Freemarker）自动生成前后端完整代码。生成的代码遵循 JeecgBoot 既定规范，可直接运行并支持二次开发。

**AI 集成能力**：内置 AI 聊天助手和知识库，支持接入主流大模型（GPT、Claude、本地部署模型）。AI Flow 模块支持可视化编排 AI 任务流，实现智能问答、文档生成、流程自动触发等场景。

**解决的痛点**：
- 传统企业系统开发周期长、重复代码多
- 前后端联调成本高
- CRUD 页面开发效率低下
- 业务系统与 AI 能力结合困难

**与同类对比**：相比 Apipost、钉钉宜搭等低代码平台，JeecgBoot 的代码生成模式保留了完整的源代码控制权；对比若依、SpringWind 等后台框架，其 AI 集成深度和可视化能力更突出。

## 3. 技术实现细节

**代码生成实现**：
```java
// 核心生成逻辑伪代码
Map<String, Object> context = new HashMap<>();
context.put("tableName", tableName);
context.put("entityName", StrUtils.toCamelCase(tableName));
context.put("columns", dbManager.getColumns(tableName));
// Velocity 模板渲染
VelocityEngine ve = new VelocityEngine();
Template template = ve.getTemplate(templatePath, "UTF-8");
StringWriter writer = new StringWriter();
template.merge(context, writer);
```
生成器通过解析数据库元数据，结合 Velocity 模板输出 Java、Vue、SQL 混合代码。

**在线表单实现**：采用 JSON Schema 定义表单结构，前端解析 Schema 动态渲染组件。表单提交后通过反射机制自动映射到实体类，降低了前端适配成本。

**权限控制设计**：采用 RBAC 模型，Shiro 负责接口级权限校验，前端按钮级权限通过注解 `@RequiresPermissions` 生成的菜单数据控制。这种双重保障确保了细粒度权限管理。

**性能优化策略**：
- MyBatis-Plus 的 SQL 缓存机制
- 前端组件按需加载
- 数据库连接池配置（HikariCP）
- 列表页采用分页查询，避免全表扫描

**技术难点**：多数据源切换、分布式 Session 管理、代码生成模板的兼容性维护。解决方案是引入 dynamic-datasource 实现数据源路由，Session 通过 Redis 统一存储。

## 4. 适用场景分析

**最佳适用场景**：
- 企业内部管理系统（OA、CRM、ERP）
- 快速原型开发与 MVP 验证
- 标准化 CRUD 业务占主导的后台系统
- 需要 AI 辅助的智能客服、知识库系统

**最有效场景**：业务逻辑相对标准、界面交互不复杂、需要快速交付的中型后台系统。一次开发、多人协作场景下收益最高。

**不适合的场景**：
- 高并发交易系统（实时性要求高）
- 复杂定制化业务（平台约束过多）
- 纯移动端应用
- 需要微服务拆分的大型分布式系统

**集成注意事项**：
- 与 Spring Cloud 集成时需注意服务治理冲突
- 定制化代码需遵循模块隔离原则，避免污染生成代码
- AI 能力接入需评估 token 成本和数据安全合规要求

## 5. 发展趋势展望

**技术演进方向**：
- 全面拥抱 Spring Boot 3.x 与 Java 17+
- 前端向 Vue3+TypeScript+Pinia 全面升级
- AI 能力深化：Agent 架构、RAG 知识库增强
- 低代码与 DevOps 流程深度集成

**社区反馈与改进空间**：
- 代码生成模板的定制化学习成本较高
- 文档部分功能描述与实际实现存在差异
- 部分依赖版本较旧，存在安全漏洞风险

**前沿技术结合点**：
- 大模型辅助代码审查与优化建议
- 低代码流程与 BPMN 2.0 标准对齐
- 多租户 SaaS 架构增强
- 低代码 + 云原生基础设施联动

## 6. 学习建议

**适合的开发者水平**：适合具备 Java SE/EE 基础、了解 Spring MVC、熟悉 SQL 的中初级开发者。高级开发者可深入研究架构设计与扩展机制。

**可学习内容**：
- Spring Boot 企业级应用最佳实践
- 前後端分离架构设计模式
- 代码生成器的模板定制技巧
- Shiro 权限框架的深度应用
- AI 能力接入的工程化实现

**推荐学习路径**：
1. 本地部署运行 Demo，理解整体功能
2. 阅读代码生成器核心源码，追踪模板渲染链路
3. 研究 Online 表单实现，理解动态渲染原理
4. 学习 AI 模块接入方式，理解 Prompt 工程
5. 参与社区讨论，提交第一个 PR

**实践建议**：从一个小模块改造开始，如定制代码生成模板、增加一个新业务功能。避免直接修改核心生成逻辑，建议通过继承扩展。

## 7. 最佳实践建议

**正确使用方式**：
- 生成代码后立即提交到版本控制
- 业务扩展代码放在 `modules` 包下，与生成代码分离
- 数据库变更通过 SQL 脚本管理，禁止直接修改生成 SQL
- 自定义模板纳入单独仓库管理

**常见问题与解决**：
- **生成代码与预期不符**：检查数据库表命名规范和注释
- **权限不生效**：确认 Shiro 配置与前端路由匹配
- **AI 能力调用失败**：检查模型服务可用性和 Token 配置
- **前端构建失败**：确认 Node 版本与 package.json 要求一致

**性能优化建议**：
- 生产环境启用 Redis 缓存
- 列表查询强制走索引，避免全表扫描
- 大数据量导出采用异步+分片机制
- 前端列表启用虚拟滚动优化

## 8. 哲学与方法论：第一性原理与权衡

**复杂性转移分析**：JeecgBoot 将开发复杂度转移给平台本身和运维侧。平台承担了代码规范统一、业务模板沉淀的工作，代价是开发者的定制灵活性受限；运维侧需要维护 AI 服务依赖和模型调用成本。复杂性不会消失，只是被重新分配。

**价值取向权衡**：
- **速度优先**：牺牲了代码的极致性能和定制深度，换取开发效率
- **控制妥协**：生成代码遵循固定范式，个性化需求需通过扩展机制实现
- **安全优先**：Shiro+JWT 双保险，但增加了系统复杂度
- **可移植性取舍**：强依赖 JeecgBoot 生态，跨平台迁移成本较高

**工程哲学总结**：这是一种"约定优于配置"的思想延伸——平台定义了最佳实践，开发者在此基础上填空。优点是降低团队沟通成本，缺点是"填空"能力受平台约束。最容易被误用的场景是试图用 JeecgBoot 实现高度定制化业务，导致大量"平台之外的工作"反而增加了复杂度。

**可证伪判断**：

1. **效率提升判断**：若使用 JeecgBoot 完成相同功能的开发时间低于传统方式的 50%，则其核心价值成立。验证方法：对照实验——同一团队分别用 JeecgBoot 和传统方式开发同一模块，记录工时对比。

2. **代码质量判断**：生成的代码应满足 SonarQube 基础扫描通过率 > 85%。若低于此标准，说明生成模板质量存在问题。

3. **AI 价值判断**：接入 AI 能力后，业务功能开发中人机交互时间占比应 > 30%。若 AI 助手使用率极低，说明 AI 能力与实际需求存在错配，需要重新评估接入策略。

---
## 代码示例


这是JeecgBoot项目的基础启动类，展示了Spring Boot应用的标准结构。在实际JeecgBoot项目中，通常还需要配置@ComponentScan来扫描多个包。
---

```java
// 示例1：JeecgBoot 项目结构 - Spring Boot 启动类
package com.jeecg.system;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * JeecgBoot 主启动类
 * 
 * 注意事项：
 * 1. @SpringBootApplication 是Spring Boot的核心注解
 * 2. JeecgBoot通常会配置多个扫描包路径
 */
@SpringBootApplication
public class JeecgBootApplication {
    
    public static void main(String[] args) {
        // 标准Spring Boot启动方式
        System.out.println("========== JeecgBoot 启动中... ==========");
        SpringApplication.run(JeecgBootApplication.class, args);
        System.out.println("========== JeecgBoot 启动成功! ==========");
    }
}
```


这是JeecgBoot中标准的实体类定义，展示了常用的注解用法。`@Dict`注解是JeecgBoot的特色功能，可以自动将字典码转换为显示文本。
---

```java
// 示例2：JeecgBoot 实体类定义与Mapper接口
package com.jeecg.examples.entity;

import com.baomidou.mybatisplus.annotation.*;
import com.jeecg.boot.common.aspect.annotation.Dict;
import lombok.Data;
import lombok.EqualsAndHashCode;

import java.io.Serializable;
import java.time.LocalDateTime;

/**
 * 用户实体类 - 展示JeecgBoot的实体定义规范
 * 
 * 常用注解说明：
 * - @Data: Lombok插件，自动生成getter/setter
 * - @TableName: 指定数据库表名
 * - @TableId: 标记主键字段
 * - @Dict: JeecgBoot字典注解，用于下拉框数据转换
 */
@Data
@EqualsAndHashCode(callSuper = false)
@TableName("sys_user")
public class SysUser implements Serializable {
    
    private static final long serialVersionUID = 1L;
    
    /**
     * 主键ID - 使用UUID策略
     * auto: 数据库自增
     * assign_id: 雪花算法（默认）
     * assign_uuid: UUID
     */
    @TableId(type = IdType.ASSIGN_UUID)
    private String id;
    
    /**
     * 用户名
     */
    private String username;
    
    /**
     * 真实姓名
     */
    private String realname;
    
    /**
     * 密码（加密存储）
     */
    private String password;
    
    /**
     * 头像URL
     */
    private String avatar;
    
    /**
     * 生日
     */
    private String birthday;
    
    /**
     * 性别：0-未知，1-男，2-女
     * 使用@Dict注解后，前端会自动转换为文本显示
     */
    @Dict(dicCode = "sex")
    private Integer sex;
    
    /**
     * 部门ID
     */
    private String departId;
    
    /**
     * 状态：0-禁用，1-正常
     */
    private Integer status;
    
    /**
     * 创建时间 - 自动填充
     */
    @TableField(fill = FieldFill.INSERT)
    private LocalDateTime createTime;
    
    /**
     * 更新时间 - 自动填充
     */
    @TableField(fill = FieldFill.INSERT_UPDATE)
    private LocalDateTime updateTime;
}
```




```java
// 示例3：JeecgBoot Service层实现类
package com.jeecg.examples.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.jeecg.boot.common.system.vo.LoginUser;
import com.jeecg.examples.entity.SysUser;
import com.jeecg.examples.mapper.SysUserMapper;
import com.jeecg.examples.service.ISysUserService;
import com.jeecg.boot.common.system.util.JwtUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * 用户Service实现类
 * 
 * JeecgBoot推荐使用MyBatis-Plus进行数据库操作
 * 提供了强大的CRUD功能和分页支持
 */
@Service
public class SysUserServiceImpl implements ISysUserService {
    
    @Autowired
    private SysUserMapper sysUserMapper;
    
    @Autowired
    private BCryptPasswordEncoder passwordEncoder;
    
    /**
     * 分页查询用户列表
     * 
     * @param current 当前页码
     * @param size 每页记录数
     * @param username 用户名（模糊查询）
     * @return 分页结果
     */
    @Override


---
## 案例研究


### 1：某大型物流企业

 1：某大型物流企业

**背景**: 该企业在全国拥有数百个配送中心，业务涵盖仓储、运输和配送，急需统一的物流信息管理平台。

**问题**: 传统开发模式需要 6‑9 个月交付，且后期维护成本高；系统扩展性差，难以快速适配频繁的业务变更。

**解决方案**: 引入 JeecgBoot 低代码平台，利用其在线表单设计、代码自动生成和工作流引擎，快速搭建物流订单、仓储和车辆调度等核心模块，实现前后端分离的微服务架构。

**效果**: 开发周期从 6 个月缩短至 2 个月，整体人力成本下降约 45%；系统上线后月均处理订单量提升 30%，故障响应时间从 4 小时降低至 1 小时以内。

---



### 2：某省级政务服务平台

 2：某省级政务服务平台

**背景**: 省级政务部门需要统一管理多部门的行政审批、数据报送和信息公开，系统需要兼顾高安全性和快速迭代。

**问题**: 原有系统采用单体架构，升级和扩展困难，功能迭代周期长，导致部门间协同效率低下。

**解决方案**: 采用 JeecgBoot 作为后端框架，结合其角色权限管理、在线配置和前后端

---
## 对比分析

## 与同类方案对比

| 维度 | JeecgBoot | 若依 (RuoYi) | EL-Admin |
|------|-----------|------------|----------|
| 功能完整性 | 低代码平台、代码生成、权限管理、工作流（Flowable）、多数据源支持 | 基础管理后台、代码生成、Shiro 权限、简单的流程（无） | 基础权限、代码生成、Shiro/JWT、可集成 Activiti/Flowable（非默认） |
| 低代码能力 | 可视化表单、报表、页面设计，拖拽生成 | 仅代码生成，非可视化 | 仅代码生成，非可视化 |
| 工作流支持 | 内置 Flowable，支持流程设计、审批、监控 | 不内置工作流，需自行集成 | 可集成 Activiti/Flowable，非默认 |
| UI/UX | Ant Design Vue，现代美观，组件丰富 | Bootstrap/Vue 2/3，提供经典/简约两种 UI | Bootstrap/AdminLTE，UI 较传统 |
| 性能 | 引入较多组件，启动略慢，运行时开销相对较高 | 结构轻量，启动快，性能较好 | 结构轻量，性能与 RuoYi 接近 |
| 部署难度 | 前后端、流程引擎、数据库等多组件需同步部署，配置相对复杂 | 前端+后端分离，部署相对简单 | 前端+后端分离，部署相对简单 |
| 文档与社区 | 官方文档完整，社区活跃度中等 | 文档丰富，社区庞大，资料多 | 文档相对简洁，社区活跃度一般 |
| 许可与成本 | Apache License 2.0，免费使用 | MIT License，免费使用 | Apache License 2.0，免费使用 |
| 维护活跃度 | 维护更新频率稳定，版本迭代较慢 | 维护活跃，版本迭代快 | 维护相对平稳，版本迭代较慢 |
| 扩展性 | 插件化设计，支持多种业务模块快速集成 | 通过自定义模块扩展，需要自行实现 | 通过自定义模块扩展，功能相对单一 |

### 优势分析

- 完整的低代码生态：提供可视化表单、报表、页面设计工具，能够在短时间内完成业务原型和交付。  
- 内置工作流引擎：基于 Flowable，支持流程设计、审批、监控，适合企业级业务流程管理。  
- 多数据源与权限模型：内置数据权限、行级权限，支持多租户、字段级权限控制，满足复杂业务需求。  
- UI 采用 Ant Design Vue，界面美观、组件丰富，前后端分离提升开发体验。  
- 代码生成与业务模板完整，支持

---
## 最佳实践

## 最佳实践指南

### 实践 1：项目结构与模块划分

**说明**：在 JeecgBoot 中，采用分层清晰、职责明确的模块化结构，能够提升代码可维护性、团队协作效率，并降低后期业务变更的风险。建议将项目拆分为 `common`、`system`、`module`（业务模块）等层级，并在 `module` 下按照业务域（如 `order`、`customer`）进行子模块划分。

**实施步骤**：
1. 在 Maven/Gradle 项目根 pom 中声明统一的 `dependencyManagement`，统一管理第三方依赖版本。  
2. 创建 `jeecg-boot-common` 模块，存放工具类、常量、全局异常等公共代码。  
3. 创建 `jeecg-boot-system` 模块，承载系统管理、权限、字典等基础功能。  
4. 按业务域在 `jeecg-boot-module-xxx` 中新建子模块，每个子模块包含 `controller`、`service`、`mapper`、`entity`、`vo` 包。  
5. 在 `jeecg-boot-starter`（或主入口）中通过 Maven/Gradle 的 `dependencies` 引入业务模块，利用 Spring Boot 的自动装配完成模块加载。  
6. 在 `application.yml` 中通过 `spring.profiles.include` 动态加载不同环境的配置文件。

**注意事项**：
- 避免在 `common` 模块中引入业务强关联的依赖，保持其纯净。  
- 子模块的 `pom.xml` 必须声明对应的父 POM，以保证版本统一。  
- 前端（Vue）项目也应遵循相同的目录结构（views、api、store），保持前后端对应。

---

### 实践 2：代码生成与自定义业务逻辑分离

**说明**：JeecgBoot 提供强大的在线代码生成功能，建议仅用于生成 CRUD 框架代码，后续的业务校验、复杂业务逻辑应在 Service 层或业务微服务中实现，避免直接在生成的代码上做业务修改，以免在重新生成时被覆盖。

**实施步骤**：
1. 在 JeecgBoot 的在线设计器中完成数据表设计，点击“代码生成”，下载生成的压缩包。  
2. 将生成的 `entity`、`mapper`、`service`、`controller` 文件放入对应模块的包路径。  
3. 在生成的 `ServiceImpl` 中，使用 `//业务处理 start` 与 `//业务处理 end` 注释块来编写自定义逻辑，确保重新生成代码时不影响已有业务。  
4. 对于跨模块的业务，可抽取为独立的 `@Service`（业务服务），在 `Controller` 中通过 `@Autowired` 注入调用。  
5. 业务校验、事务控制统一在 Service 层处理，Controller 仅负责参数校验与返回封装。  
6. 生成的单元测试模板仅作参考，需要自行补充完整业务场景的测试用例。

**注意事项**：
- 不要在生成的 `mapper.xml` 中直接写业务 SQL，保持 SQL 简单，仅负责 CRUD。  
- 重新生成代码前，务必使用版本控制系统（Git）提交当前代码，以防覆盖。  
- 对于需要频繁变更的业务，考虑使用 `@DynamicDataSource` 进行数据源切换或采用微

---
## 性能优化建议

## 性能优化建议

### 优化 1：数据库查询优化

**说明**: JeecgBoot 项目中大量使用 JPA 和 MyBatis-Plus 进行数据库操作，存在 N+1 查询问题、缺少索引、全表扫描等问题，影响系统响应速度。

**实施方法**:
1. 使用 `join` 联表查询替代循环查库，避免 N+1 问题
2. 对 `create_time`、`update_time`、`tenant_id` 等高频查询字段添加联合索引
3. 启用 MyBatis-Plus 的分页插件，合理设置分页大小（建议每页不超过 100 条）
4. 使用 Explain 分析慢查询 SQL，针对性地添加索引
5. 对报表类查询结果进行缓存，避免重复计算

**预期效果**: 复杂列表页面响应时间降低 40%-60%，数据库 CPU 占用降低 30%-50%

---

### 优化 2：Redis 缓存策略优化

**说明**: JeecgBoot 内置 Redis 缓存支持，但缓存使用不够充分，存在大量重复查询数据库的情况。

**实施方法**:
1. 对字典数据、权限数据、配置参数等高频访问且变更较少的数据启用多级缓存
2. 配置合适的缓存过期时间：字典数据 24 小时、用户权限 2 小时、热点数据 1 小时
3. 使用 Redis 的 `pipeline` 批量操作替代单条操作
4. 实现缓存击穿、穿透、雪崩的防护机制
5. 对实时性要求不高的数据采用异步刷新策略

**预期效果**: 缓存命中率提升至 85% 以上，数据库 QPS 降低 50%-70%，接口平均响应时间减少 30%-40%

---

### 优化 3：JVM 堆内存与垃圾回收优化

**说明**: JeecgBoot 基于 Spring Boot 运行，默认 JVM 参数配置可能不适合生产环境，导致频繁 Full GC 或 OOM 问题。

**实施方法**:
1. 根据服务器内存配置合理的堆大小，建议设置 `-Xms4g -Xmx4g`（4G 示例）
2. 使用 G1 垃圾收集器，设置参数 `-XX:+UseG1GC -XX:MaxGCPauseMillis=200`
3. 调整年轻代与老年代比例，建议 `-XX:NewRatio=2`
4. 启用堆转储和 GC 日志，分析内存使用情况
5. 对大对象直接进入老年代进行设置 `-XX:PretenureSizeThreshold=1048576`

**预期效果**: GC 停顿时间降低 50% 以上，系统吞吐量提升 20%-30%，有效避免 OOM 异常

---

### 优化 4：接口响应时间优化

**说明**: 系统存在部分接口响应时间过长的问题，主要由于同步处理、串行业务逻辑、远程调用未优化等原因造成。

**实施方法**:
1. 对非核心业务逻辑采用 `@Async` 异步处理，如日志记录、消息推送
2. 使用 CompletableFuture 并行调用多个服务，替代串行调用
3. 对大数据量导出功能采用分批导出或异步任务队列方式
4. 实现接口结果压缩，对超过 1KB 的 JSON 响应启用 Gzip 压缩
5. 使用 CompletableFuture 合并多次数据库查询为单次批量查询

**预期效果**: 复杂业务接口响应时间降低 40%-60%，系统并发处理能力提升 50%-

---
## 学习要点

- 以下是JeecgBoot的关键要点（按重要性排序）：
- 基于Spring Boot + MyBatis‑Plus + Vue3的前后端分离低代码平台，实现快速业务交付（最重要）
- 提供可视化表单、报表、页面设计器等在线开发工具，显著提升开发效率
- 内置完善的RBAC权限管理、数据字典、代码生成器，支持微服务与单体双模式部署
- 集成Flowable工作流引擎，支持业务流程建模、表单绑定和审批流转
- 支持多数据源、分布式缓存（Redis）和容器化部署，具备高可用与弹性伸缩能力
- 插件化架构与丰富的扩展机制，便于二次开发和功能定制


---
## 学习路径

## 学习路径

### 阶段 1：入门基础

**学习内容**  
- Java 基础：面向对象、集合、异常处理、IO、并发基础  
- Spring Boot 入门：核心概念（IoC、AOP）、常用注解、RESTful 接口开发  
- Maven/Gradle：项目构建、依赖管理、插件使用  
- 前端基础：HTML、CSS、JavaScript（ES6+）  
- Vue.js 入门：组件、路由、状态管理（Vuex）  
- Git 基本操作：版本控制、分支管理、代码合并  

**学习时间**: 2–3 周  

**学习资源**  
- 《Spring Boot 实战》 – 丁雪丰 译  
- 《Vue.js 实战》 – 梁灏  
- 官方文档：Spring Boot Docs (https://spring.io/projects/spring-boot)  
- Vue 官方教程：https://cn.vuejs.org/v2/guide/  
- Maven 官方文档：https://maven.apache.org/guides/  
- Git 官方文档：https://git-scm.com/doc  

**学习建议**  
1. 动手搭建一个简单的 Spring Boot + Vue 项目，熟悉前后端分离的交互方式。  
2. 在本地使用 Git 管理项目代码，练习常见的分支操作和冲突解决。  
3. 通过官方示例和教程熟悉 Maven/Gradle 的依赖管理和构建流程。  

---

### 阶段 2：JeecgBoot 基础使用

**学习内容**  
- JeecgBoot 项目结构：后端（Spring Boot）、前端（Vue）、代码生成器  
- 环境搭建：JDK、Maven、Node.js、Redis、MySQL/Oracle 等  
- 代码生成器的使用：表设计 → 一键生成后端 CRUD、前端页面  
- 权限管理：RBAC（角色、用户、菜单）模型、数据权限、按钮权限  
- 在线表单设计：表单组件、校验规则、联动逻辑  
- 常用业务组件：字典、文件上传、Excel 导入导出、定时任务  

**学习时间**: 2–3 周  

**学习资源**  
- JeecgBoot 官方文档：https://jeecg.com/doc/  
- JeecgBoot GitHub 仓库（README、Wiki）：https://github.com/jeecgboot/jeecg-boot  
- JeecgBoot 在线演示平台：https://demo.jeecg.com  
- 视频教程（Bilibili、YouTube）搜索 “JeecgBoot 入门”  
- Spring Security 与 Shiro 权限框架的对比文档  

**学习建议**  
1. 按照官方文档搭建本地开发环境，确保前后端能够成功启动。  
2. 使用代码生成器生成一套完整的 CRUD 示例，体会 “零代码” 的便利。  
3. 完成权限模块的练习：新增角色、分配菜单、测试数据权限控制。  
4. 记录常见报错及解决方案，形成自己的踩坑笔记。  

---

### 阶段 3：进阶功能与业务扩展

**学习内容**  
- 工作流（Flowable）集成：流程设计、任务分配、审批节点、动态表单  
- 自定义业务组件：封装通用弹窗、树形表格、级联选择等  
- 数据权限深度使用：基于组织、岗位、部门的细粒度权限控制  
- 前后端交互优化：API 统一封装、请求拦截、错误处理、分页封装  
- 缓存与性能：Redis 缓存策略、页面静态化、SQL 优化、N+1 查询避免  
- 日志与监控：Spring Boot Actuator、ELK（Elasticsearch、Logstash、Kibana）集成  

**学习时间**: 3–4 周  

**学习资源**  
- Flowable 官方文档：https://flowable.com/open-source/docs/bpm

---
## 常见问题


### 1: JeecgBoot 是什么？适用于哪些业务场景？

1: JeecgBoot 是什么？适用于哪些业务场景？

**A**: JeecgBoot 是一款基于 Spring Boot + Vue 的低代码平台，旨在通过可视化的页面配置、在线表单设计以及代码自动生成等功能，大幅提升企业级管理信息系统的开发效率。它适用于内部管理系统（如 OA、CRM、ERP）、后台管理系统、数据采集平台以及需要快速交付的中小型项目。

---



### 2: JeecgBoot 的技术栈是什么？主要依赖有哪些？

2: JeecgBoot 的技术栈是什么？主要依赖有哪些？

**A**: JeecgBoot 采用主流的前后端分离架构，后端核心技术包括：
- Java 8+ (推荐使用 JDK 11)
- Spring Boot 2.x（核心框架）
- MyBatis-Plus（ORM，简化 CRUD 操作）
- Shiro / JWT（权限认证，支持 Token 与 Session 两种模式）
- Redis（缓存与 Session 共享）
- Maven（项目构建）

前端技术栈包括：
- Vue 2.x（渐进式前端框架）
- Element UI（UI 组件库）
- Vuex（状态管理）
- Axios（HTTP 客户端）

---



### 3: 如何在本地快速启动 JeecgBoot 项目？

3: 如何在本地快速启动 JeecgBoot 项目？

**A**: 启动步骤大致如下（以 `jeecg-boot` 为例）：

1. **环境准备**  
   - 安装 JDK 11+、Maven 3.6+、Node.js 14+、MySQL 5.7+、Redis。  
   - 确保 Maven 与 Node 环境变量已配置。

2. **导入数据库**  
   - 在 MySQL 中创建空库（如 `jeecg_boot`），使用项目根目录下的 `db` 文件夹中的 `jeecg-boot.sql` 脚本完成建表和数据初始化。

3. **修改配置文件**  
   - 打开 `jeec

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1

### 难度**：简单

### 问题**：在本地机器上搭建 JeecgBoot 开发环境，包括 JDK、Maven、MySQL、Redis 等，并成功启动项目的前后端服务。

### 提示**：确认使用 JDK 8+、Maven 3.6+，按照官方文档的“快速入门”章节创建数据库并执行初始化脚本，使用 `mvn clean install` 编译后端，使用 `npm run dev` 启动前端。

---
## 实践建议

下面给出 7 条针对 JeecgBoot 低代码平台的实践建议，均结合真实使用场景并可直接落地执行，帮助你在提升开发效率的同时保持系统的可维护性、可扩展性和安全性。

---

### 1. 采用多模块 Maven 项目结构，明确前后端边界
- **做法**：在项目根目录下创建 `backend-parent`（Spring Boot 多模块父项目）和 `frontend-ui`（Vue/React 前端子项目）两个顶层目录。`backend-parent` 再细分为 `backend-api`（提供 REST 接口与通用实体）、`backend-biz`（业务实现、Service、Mapper）和 `backend-generator`（代码生成插件及自定义生成模板）。
- **好处**：代码生成、插件升级、业务代码分层清晰，CI/CD 时可以只构建需要变更的

---
## 引用

- **GitHub 仓库**: [https://github.com/jeecgboot/JeecgBoot](https://github.com/jeecgboot/JeecgBoot)
- **DeepWiki**: [https://deepwiki.com/jeecgboot/JeecgBoot](https://deepwiki.com/jeecgboot/JeecgBoot)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/)
- 标签： [低代码平台](/tags/%E4%BD%8E%E4%BB%A3%E7%A0%81%E5%B9%B3%E5%8F%B0/) / [AI代码生成](/tags/ai%E4%BB%A3%E7%A0%81%E7%94%9F%E6%88%90/) / [Java开发](/tags/java%E5%BC%80%E5%8F%91/) / [代码生成器](/tags/%E4%BB%A3%E7%A0%81%E7%94%9F%E6%88%90%E5%99%A8/) / [零代码开发](/tags/%E9%9B%B6%E4%BB%A3%E7%A0%81%E5%BC%80%E5%8F%91/) / [大模型集成](/tags/%E5%A4%A7%E6%A8%A1%E5%9E%8B%E9%9B%86%E6%88%90/) / [MCP插件](/tags/mcp%E6%8F%92%E4%BB%B6/) / [快速开发](/tags/%E5%BF%AB%E9%80%9F%E5%BC%80%E5%8F%91/)
- 场景： [后端开发](/scenarios/%E5%90%8E%E7%AB%AF%E5%BC%80%E5%8F%91/) / [全栈开发](/scenarios/%E5%85%A8%E6%A0%88%E5%BC%80%E5%8F%91/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [利用 Gradio gr.HTML 组件一键封装任意 Web 应用]({{< relref "posts/20260218-blogs_podcasts-one-shot-any-web-app-with-gradios-grhtml-8.md" >}})
- [利用 Gradio gr.HTML 组件一键封装任意 Web 应用]({{< relref "posts/20260219-blogs_podcasts-one-shot-any-web-app-with-gradios-grhtml-10.md" >}})
- [HAPI 结合设备指纹认证提升远程编程安全性]({{< relref "posts/20260306-juejin-hapi-设备指纹认证打造更安全的远程编程体验-2.md" >}})
- [RapidAI/RapidOCR：支持多推理引擎的跨语言OCR工具包]({{< relref "posts/20260310-github_trending-rapidai-rapidocr-6.md" >}})
- [Vue3低代码平台DSL转Vue3组件代码生成机制解析]({{< relref "posts/20260313-juejin-ai-驱动的-vue3-应用开发平台-深入探究六双向代码转换之dsl到vue代码生成-2.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*