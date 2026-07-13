---
title: JeecgBoot：AI低代码平台一键生成Java代码
date: 2026-03-20 04:08:49+08:00
draft: false
entry_kind: auto
tags:
- 低代码平台
- AI代码生成
- Java开发
- 代码生成器
- 零代码开发
- 大模型集成
- MCP插件
- 快速开发
categories:
- 开发工具
source: github_trending
description: JeecgBoot 项目概述 基本信息 - **项目名称**：jeecgboot/JeecgBoot - **编程语言**：Java -
  **星标数**：45,458（今日+15） 核心定位 JeecgBoot 是一款企业级 AI 驱动的低代码开发平台，旨在解决 Java 项目中 80% 的重复性工作，在保证开发效率的
external_url: https://github.com/jeecgboot/JeecgBoot
scenarios:
- 后端开发
- 全栈开发
- AI/ML项目
---

# JeecgBoot：AI低代码平台一键生成Java代码

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

Relevant source files

  * [README-AI.md](https://github.com/jeecgboot/JeecgBoot/blob/b7a3da89/README-AI.md)
  * [README.en-US.md](https://github.com/jeecgboot/JeecgBoot/blob/b7a3da89/README.en-US.md)
  * [README.md](https://github.com/jeecgboot/JeecgBoot/blob/b7a3da89/README.md)
  * [jeecg-boot/README.md](https://github.com/jeecgboot/JeecgBoot/blob/b7a3da89/jeecg-boot/README.md)
  * [jeecgboot-vue3/README.md](https://github.com/jeecgboot/JeecgBoot/blob/b7a3da89/jeecgboot-vue3/README.md)

---

## 导语

JeecgBoot 是一款基于 Java 的 AI 低代码开发平台，融合了零代码与代码生成两种开发模式。平台通过内置的 AI 助手和大模型能力，可自动生成前后端代码与建表 SQL，覆盖流程编排、表单设计、聊天式业务操作等常见场景，能够显著减少 Java 项目中的重复编码工作。该项目适合需要快速交付企业内部系统的开发团队，或希望兼顾开发效率与灵活性的技术负责人。本文将围绕其核心功能、技术架构以及实际应用方向展开介绍。

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

## 代码示例

这是JeecgBoot项目的基础启动类，展示了Spring Boot应用的标准结构。在实际JeecgBoot项目中，通常还需要配置@ComponentScan来扫描多个包。
---

---

### Purpose and Scope

This document introduces JeecgBoot as an enterprise-level AI low-code development platform, explaining its core value proposition and position in the enterprise software ecosystem. It provides the conceptual foundation for understanding how JeecgBoot combines code generation, visual development, and AI capabilities into a unified platform.

For detailed technical information:

  * Complete feature list: see [Key Features & Capabilities](/jeecgboot/JeecgBoot/1.1-key-features-and-capabilities)
  * Technology stack details: see [Technology Stack](/jeecgboot/JeecgBoot/1.2-technology-stack)
  * System requirements: see [System Requirements & Environment Setup](/jeecgboot/JeecgBoot/1.3-system-requirements-and-environment-setup)
  * Quick start instructions: see [Quick Start Guide](/jeecgboot/JeecgBoot/1.4-quick-start-guide)
  * Architecture details: see [Architecture](/jeecgboot/JeecgBoot/2-architecture)
  * AI platform capabilities: see [AI Platform (AIGC)](/jeecgboot/JeecgBoot/3-ai-platform-\(aigc\))
  * Low-code features: see [Low-Code Development Platform](/jeecgboot/JeecgBoot/5-low-code-development-platform)

---

### What is JeecgBoot?

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

---

### Core Value Proposition

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

---

### Platform Architecture Modes

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

---

### Repository Organization

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

### JeecgBoot 项目概述

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

### 1. 技术架构深度剖析

**技术栈构成**：JeecgBoot 采用经典的前后端分离架构，后端基于 Spring Boot + MyBatis-Plus + Shiro，前端采用 Vue3 + Ant Design Vue，技术选型成熟稳定。数据库层面支持 MySQL、Oracle、PostgreSQL 等主流关系型数据库，缓存层引入 Redis 实现会话共享与数据缓存。

**架构模式**：平台采用微内核 + 插件化架构设计，核心层提供代码生成、流程引擎、表单设计器等基础能力，通过插件机制扩展 AI 能力、MCP 服务等高级功能。这种设计允许开发者根据业务需求选择性启用功能模块，降低了系统复杂度。

**核心模块划分**：
- `jeecg-boot`：后端核心服务，封装业务逻辑与 API
- `jeecgboot-vue3`：前端工程，基于 Vue3 Composition API 重构
- 代码生成器模块：支持一键生成 Controller、Service、Mapper、Entity
- Online 表单/表单设计器：可视化配置业务表单
- 流程引擎模块：基于 Flowable/Activiti 定制

**架构优势**：分层解耦彻底，前端可通过 HTTP 调用后端任意服务；模块化设计便于按需部署；集成 Shiro+JWT 双认证机制，兼顾安全与性能。

---

### 2. 核心功能详细解读

**零代码模式**：通过可视化配置实现表单、列表、审批流程的快速搭建。Online Coding 功能允许非技术人员通过配置生成 CRUD 页面，显著降低开发门槛。

**代码生成模式**：这是平台的核心竞争力。开发者通过数据库表设计，利用模板引擎（Velocity/Freemarker）自动生成前后端完整代码。生成的代码遵循 JeecgBoot 既定规范，可直接运行并支持二次开发。

**AI 集成能力**：内置 AI 聊天助手和知识库，支持接入主流大模型（GPT、Claude、本地部署模型）。AI Flow 模块支持可视化编排 AI 任务流，实现智能问答、文档生成、流程自动触发等场景。

**解决的痛点**：
- 传统企业系统开发周期长、重复代码多
- 前后端联调成本高
- CRUD 页面开发效率低下
- 业务系统与 AI 能力结合困难

**与同类对比**：相比 Apipost、钉钉宜搭等低代码平台，JeecgBoot 的代码生成模式保留了完整的源代码控制权；对比若依、SpringWind 等后台框架，其 AI 集成深度和可视化能力更突出。

---

### 3. 技术实现细节

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

---

### 4. 适用场景分析

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

---

### 5. 发展趋势展望

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

---

### 6. 学习建议

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

---

### 7. 最佳实践建议

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

---

### 8. 哲学与方法论：第一性原理与权衡

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
