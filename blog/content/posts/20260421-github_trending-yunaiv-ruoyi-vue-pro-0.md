---
title: "RuoYi-Vue Pro：Java后台管理系统，支持权限/工作流/商城/ERP等功能"
date: 2026-04-21T15:35:52+08:00
draft: false
entry_kind: "auto"
tags: ["Java", "Spring Boot", "Vue", "后台管理", "RBAC权限", "工作流", "ERP", "SaaS多租户"]
categories: ["后端", "开源生态"]
source: github_trending
description: "项目概述 YunaiV/ruoyi-vue-pro 是官方推荐的全新 Pro 版本，对原有 RuoYi‑Vue 进行全面优化重构。项目基于 Spring Boot + MyBatis Plus + Vue & Element，实现后台管理系统并配套微信小程序，适用于企业级应用快速搭建。 技术栈与语言 - 编程语言：Ja"
external_url: https://github.com/YunaiV/ruoyi-vue-pro
scenarios: ["后端开发", "全栈开发", "Web应用开发"]
---

# RuoYi-Vue Pro：Java后台管理系统，支持权限/工作流/商城/ERP等功能

> **原名**: YunaiV /

      ruoyi-vue-pro

---

## 基本信息

- **描述**: 以下为符合要求的中文内容，保持原文格式与语气：

🔥 官方推荐 🔥 RuoYi-Vue 全新 Pro 版本，优化重构所有功能。基于 Spring Boot + MyBatis Plus + Vue & Element 实现的后台管理系统 + 微信小程序，支持 RBAC 动态权限、数据权限、SaaS 多租户、Flowable 工作流、三方登录、支付、短信、商城、CRM、ERP、MES、IM、AI 大模型、IoT 物联网等功能。你的 ⭐️ Star ⭐️，是作者生发的动力！
- **语言**: Java
- **星标**: 36,635 (+37 stars today)
- **链接**: [https://github.com/YunaiV/ruoyi-vue-pro](https://github.com/YunaiV/ruoyi-vue-pro)
- **DeepWiki**: [https://deepwiki.com/YunaiV/ruoyi-vue-pro](https://deepwiki.com/YunaiV/ruoyi-vue-pro)

---
## DeepWiki 速览（节选）

# Overview

Relevant source files

  * [.gitignore](https://github.com/YunaiV/ruoyi-vue-pro/blob/342b1ab7/.gitignore)
  * [README.md](https://github.com/YunaiV/ruoyi-vue-pro/blob/342b1ab7/README.md?plain=1)
  * [pom.xml](https://github.com/YunaiV/ruoyi-vue-pro/blob/342b1ab7/pom.xml)
  * [yudao-dependencies/pom.xml](https://github.com/YunaiV/ruoyi-vue-pro/blob/342b1ab7/yudao-dependencies/pom.xml)
  * [yudao-framework/pom.xml](https://github.com/YunaiV/ruoyi-vue-pro/blob/342b1ab7/yudao-framework/pom.xml)
  * [yudao-framework/yudao-spring-boot-starter-security/pom.xml](https://github.com/YunaiV/ruoyi-vue-pro/blob/342b1ab7/yudao-framework/yudao-spring-boot-starter-security/pom.xml)
  * [yudao-server/pom.xml](https://github.com/YunaiV/ruoyi-vue-pro/blob/342b1ab7/yudao-server/pom.xml)

## Purpose and Scope

RuoYi-Vue-Pro is a comprehensive, open-source enterprise management platform built on Spring Boot, designed to accelerate business application development through a modular architecture and extensive built-in functionality. The system provides a complete foundation for building enterprise applications including system administration, workflow automation, e-commerce, IoT device management, AI services integration, CRM, and ERP capabilities.

This document provides a high-level overview of the system's architecture, module organization, and core capabilities. For detailed information on specific subsystems:

  * System architecture patterns and design principles: see [System Architecture](/YunaiV/ruoyi-vue-pro/2-system-architecture)
  * Framework components and utilities: see [Core Framework](/YunaiV/ruoyi-vue-pro/3-core-framework)
  * Business module implementations: see sections [4](/YunaiV/ruoyi-vue-pro/4-system-module) through [9](/YunaiV/ruoyi-vue-pro/9-ai-integration-system)
  * Deployment and operations: see [Development and Operations](/YunaiV/ruoyi-vue-pro/10-development-and-operations)

**Sources:** [README.md1-115](https://github.com/YunaiV/ruoyi-vue-pro/blob/342b1ab7/README.md?plain=1#L1-L115) [pom.xml31-33](https://github.com/YunaiV/ruoyi-vue-pro/blob/342b1ab7/pom.xml#L31-L33)

* * *

## Architectural Philosophy

RuoYi-Vue-Pro follows a **microkernel architecture** where `yudao-server` acts as a lightweight container that aggregates business modules as optional dependencies. The system is designed with a "minimal by default, expand as needed" philosophy—by default, only core modules (`yudao-module-system` and `yudao-module-infra`) are enabled, with all other modules commented out to improve build speed during development.

**Sources:** [yudao-server/pom.xml16-116](https://github.com/YunaiV/ruoyi-vue-pro/blob/342b1ab7/yudao-server/pom.xml#L16-L116) [pom.xml10-29](https://github.com/YunaiV/ruoyi-vue-pro/blob/342b1ab7/pom.xml#L10-L29) [README.md31-33](https://github.com/YunaiV/ruoyi-vue-pro/blob/342b1ab7/README.md?plain=1#L31-L33)

* * *

## Maven Project Structure

The project follows a multi-module Maven structure with clear separation of concerns across four main layers:

### Dependency Management Layer

**`yudao-dependencies`** serves as a centralized Bill of Materials (BOM) that manages versions for 120+ dependencies, ensuring consistency across all modules. This includes Spring Boot (2.7.18), Spring Framework (5.3.39), MyBatis-Plus (3.5.15), Flowable (6.8.0), and numerous integration libraries.

Dependency Category| Key Libraries| Purpose  
---|---|---  
Core Framework| Spring Boot 2.7.18, Spring Security 5.8.16| Application foundation  
Database| MyBatis-Plus 3.5.15, Druid 1.2.27, Dynamic DataSource 4.5.0| Data access and multi-DB support  
Caching| Redisson 3.52.0| Redis client with advanced features  
Workflow| Flowable 6.8.0| BPMN process engine  
Message Queue| RocketMQ 2.3.5| Asynchronous messaging  
Chinese DB| DM8 8.1.3, KingBase 8.6.0, OpenGauss 5.1.0| Domestic database support  
IoT| TDengine 3.7.9| Time-series data storage  
Payment| Alipay SDK 4.40.607, WeChat Java SDK 4.7.9| Payment gateway integration  
Utilities| Hutool 5.8.42, Guava 33.5.0, MapStruct 1.6.3| Helper libraries  
  
**Sources:** [yudao-dependencies/pom.xml16-83](https://github.com/YunaiV/ruoyi-vue-pro/blob/342b1ab7/yudao-dependencies/pom.xml#L16-L83) [yudao-dependencies/pom.xml85-685](https://github.com/YunaiV/ruoyi-vue-pro/blob/342b1ab7/yudao-dependencies/pom.xml#L85-L685)

### Framework Layer

**`yudao-framework`** contains 20+ Spring Boot starter modules that encapsulate cross-cutting concerns, following Spring Boot's auto-configuration pattern:

**Sources:** [yudao-framework/pom.xml12-31](https://github.com/YunaiV/ruoyi-vue-pro/blob/342b1ab7/yudao-framework/pom.xml#L12-L31) [yudao-dependencies/pom.xml117-476](https://github.com/YunaiV/ruoyi-vue-pro/blob/342b1ab7/yudao-dependencies/pom.xml#L117-L476)

### Business Module Layer

Business modules follow an **API/BIZ pattern** for clean separation between interfaces and implementations:

Module Pattern| API Module| BIZ Module| Purpose  
---|---|---|---  
System| N/A| `yudao-module-system`| Core system administration (always required)  
Infrastructure| N/A| `yudao-module-infra`| Infrastructure services (always required)  
Workflow| `yudao-module-bpm-api`| `yudao-module-bpm-biz`| Flowable integration (optional)  
Payment| `yudao-module-pay-api`| `yudao-module-pay-biz`| Payment gateway abstraction (optional)  
IoT| `yudao-module-iot-api`| `yudao-module-iot-biz`| Device management (optional)  
AI| `yudao-module-ai-api`| `yudao-module-ai-biz`| LLM services (optional)  
Mall| Multiple sub-modules| `yudao-module-product`, `yudao-module-trade`, `yudao-module-promotion`, `yudao-module-statistics`| E-commerce (optional)  
  
**Sources:** [pom.xml16-28](https://github.com/YunaiV/ruoyi-vue-pro/blob/342b1ab7/pom.xml#L16-L28) [yudao-server/pom.xml24-116](https://github.com/YunaiV/ruoyi-vue-pro/blob/342b1ab7/yudao-server/pom.xml#L24-L116)

### Application Layer

**`yudao-server`** is intentionally minimal—it contains only application configuration and the Spring Boot entry point. All business logic resides in modules, making the server a pure "assembly container."

**Sources:** [yudao-server/pom.xml15-20](https://github.com/YunaiV/ruoyi-vue-pro/blob/342b1ab7/yudao-server/pom.xml#L15-L20) [README.md290-306](https://github.com/YunaiV/ruoyi-vue-pro/blob/342b1ab7/README.md?plain=1#L290-L306)

* * *

## Core Capabilities by Domain

The system provides functionality across multiple business domains, organized as independently deployable modules:

**Sources:** [README.md107-285](https://github.com/YunaiV/ruoyi-vue-pro/blob/342b1ab7/README.md?plain=1#L107-L285)

* * *

## Technology Foundation

### Backend Stack

Layer| Technology| Version| Purpose  
---|---|---|---  
**Runtime**|  Java| 8 (master) / 17/21 (master-jdk17)| JVM platform  
**Framework**|  Spring Boot| 2.7.18| Application framework  
**Security**|  Spring Security + OAuth2| 5.8.16| Authentication & authorization  
**Database**|  MySQL / PostgreSQL / Oracle / DM8 / KingBase| 5.7+ / 9+ / 11g+| Primary data storage  
**ORM**|  MyBatis-Plus| 3.5.15| Database access with auto-CRUD  
**Cache**|  Redis + Redisson| 5.0+ / 3.52.0| Session, cache, locks  
**Workflow**|  Flowable| 6.8.0| BPMN 2.0 process engine  
**Job Scheduler**|  Quartz| 2.3.2| Scheduled tasks  
**Message Queue**|  RocketMQ / Kafka / RabbitMQ| 2.3.5 / - / -| Async messaging  
**API Docs**|  Knife4j (Swagger)| 4.5.0| REST API documentation  
**Monitoring**|  Spring Boot Admin + SkyWalking| 2.7.15 / 8.12.0| APM and tracing  
  
**Sources:** [yudao-dependencies/pom.xml16-83](https://github.com/YunaiV/ruoyi-vue-pro/blob/342b1ab7/yudao-dependencies/pom.xml#L16-L83) [README.md310-331](https://github.com/YunaiV/ruoyi-vue-pro/blob/342b1ab7/README.md?plain=1#L310-L331)

### Multi-Database Support

The system supports deployment on multiple database platforms through unified SQL scripts and driver abstraction:

  * **International:** MySQL, PostgreSQL, Oracle, SQL Server, MariaDB
  * **Domestic (信创):** DM8 (达梦), 

[...truncated...]

---
## 摘要

#### 项目概述
YunaiV/ruoyi-vue-pro 是官方推荐的全新 Pro 版本，对原有 RuoYi‑Vue 进行全面优化重构。项目基于 Spring Boot + MyBatis Plus + Vue & Element，实现后台管理系统并配套微信小程序，适用于企业级应用快速搭建。

#### 技术栈与语言
- 编程语言：Java
- 核心框架：Spring Boot、MyBatis Plus、Vue、Element UI

#### 核心功能
- RBAC 动态权限、数据权限
- SaaS 多租户
- Flowable 工作流
- 三方登录、支付、短信、商城
- CRM、ERP、MES、即时通讯（IM）、AI 大模型、IoT 物联网等业务模块

#### 架构特点
采用模块化设计，提供系统管理、流程自动化、电子商务、物联网设备管理、AI 服务集成等完整企业基础功能，帮助开发者缩短项目交付周期并易于二次开发。

#### 社区与活跃度
截至目前，项目已获得 36,635 个星标，日均增长约 37 星，属于活跃度高、文档完善的开源项目。GitHub 仓库提供系统架构、核心框架、业务模块、部署运维等详细章节，便于深入学习和扩展。

---
## 评论

#### 总体判断

RuoYi-Vue-Pro是一个功能完备、社区活跃度高的企业级后台管理框架，适合需要快速搭建中后台系统的开发团队其实用主义选择。

#### 依据

从公开信息来看，该项目采用Spring Boot + MyBatis Plus + Vue & Element的技术栈组合，这些都是目前国内Java企业应用中的主流技术选型。根据GitHub页面显示，星标数达到36,635，表明其在开源社区获得了相当规模的关注与认可。README中列出的功能模块涵盖权限管理、工作流、多租户、第三方集成等多个企业级应用常见场景。从项目结构看，采用模块化设计，框架代码与业务代码分离，这种架构方式有助于后续维护与扩展。

需要指出的是，README中罗列的功能点数量众多，包括商城、CRM、ERP、MES、IM、AI大模型、IoT物联网等，这些功能的具体实现深度与生产可用性需要进一步验证，不能仅凭功能清单判断为完整的企业级解决方案。

#### 适用场景

该框架最适合以下场景：中小企业内部管理系统快速原型开发；需要对已有系统进行后台管理模块补充的技术团队；熟悉SSM/MyBatis技术栈的开发者进行后台管理平台搭建；对UI美观度要求不高、更侧重功能完整性的项目。由于集成了SaaS多租户能力，对于需要多租户隔离的应用也具有一定参考价值。

#### 局限

推断而言，过度的功能集成可能导致系统复杂度提升，学习成本相应增加；大量依赖的第三方服务（如支付、短信）需要额外配置与调试；项目声称支持的功能模块众多，但实际生产环境的稳定性与性能表现需要团队自行验证；Vue2 + Element UI的技术选型相对于Vue3 + Vite方案在长期维护上可能面临技术债务。

#### 验证方式

建议通过以下方式验证其实用价值：克隆代码库检查核心模块代码质量与注释完整性；部署本地演示环境测试权限管理、工作流等核心功能；针对具体业务需求进行针对性开发测试；评估依赖版本的维护活跃度与社区响应情况。

---
## 技术分析

#### 架构概述
##### 模块划分
已知事实：项目采用 Maven 多模块结构，主要包括 `yudao-dependencies`、`yudao-framework`、`yudao-server` 等层级；`pom.xml` 中声明了 Spring Boot、MyBatis Plus、Vue 等依赖。
推断：`yudao-framework` 负责提供通用组件和安全 starter，`yudao-server` 聚合业务模块，`yudao-ui` 前端独立部署并通过 HTTP 与后端交互。

##### 技术栈
已知事实：后端基于 Spring Boot 2.x，持久层使用 MyBatis Plus，前端使用 Vue 3 + Element Plus。
推断：前端构建可能采用 Vite 或 Webpack，后端安全方案或基于 Spring Security + OAuth2 实现单点登录与 Token 校验。

#### 核心能力
##### 权限与安全
已知事实：提供 RBAC 动态权限、数据权限、动态角色等功能。
推断：权限校验在 Filter/Interceptor 层实现，结合 Spring Security 的方法级安全注解完成细粒度控制；前端根据后端返回的菜单树动态渲染侧边栏。

##### 多租户与 SaaS
已知事实：内置 SaaS 多租户模型，支持租户数据隔离。
推断：租户字段通过 MyBatis Plus 的公共字段填充机制统一注入，查询时自动拼接租户 ID，实现业务层面的租户隔离。

##### 工作流与业务编排
已知事实：集成 Flowable 工作流引擎，提供流程设计、审批节点。
推断：工作流通过 REST API 与业务服务解耦，流程变量采用 JSON 存储，流程实例状态变更后触发业务回调。

##### 生态集成
已知事实：支持微信小程序、三方登录、支付、短信、商城、CRM、ERP、MES、IM、AI 大模型、IoT。
推断：每项集成均为独立模块或 Spring Boot Starter，按需引入；AI 大模型可能通过 HTTP 调用外部模型服务，IoT 采用 MQTT 或 CoAP 协议接入。

#### 技术实现细节
##### 后端实现
已知事实：`pom.xml` 中声明了 `spring-boot-starter-web`、`spring-boot-starter-security`、`mybatis-plus-boot-starter`、`flowable-spring-boot-starter` 等。
推断：使用 MyBatis Plus 的分页插件、乐观锁字段及自动填充实现审计和租户；统一异常处理通过 `@ControllerAdvice` 返回统一错误码。

##### 前端实现
已知事实：Vue 项目使用 Element Plus UI，提供动态路由、菜单权限控制。
推断：路由守卫根据后端返回的权限路由生成侧边栏，使用 Pinia 状态管理，axios 统一封装请求并附加 token。

##### 基础设施与部署
已知事实：项目提供 Docker Compose 与 Helm Chart 示例，支持 Docker 镜像构建。
推断：前端可使用 Nginx 托管静态资源，后端通过 Spring Boot 内嵌 Tomcat 或 Undertow 部署，亦可切换为 Netty 以提升并发。

#### 适用与不适用场景
##### 适用场景
- 快速搭建企业内部管理系统（OA、CRM、ERP）。
- 需要多租户 SaaS 平台且对数据权限有细粒度要求。
- 需要业务流程（审批、工作流）和第三方支付/短信等业务集成。
- 采用前后端分离、支持移动端（H5、微信小程序）同步管理后台的项目。

##### 不适用场景
- 对前端 UI 有高度定制化需求或使用 React/Angular 替代 Vue 的项目。
- 超大规模（千万级用户）且对微服务拆分、分布式事务要求极高的系统。
- 对国产化（信创）有特殊要求，需要完全自研安全框架时，需要额外改造。

#### 学习与落地建议
##### 学习路径
1. 阅读 `yudao-framework` 中的安全 starter 与权限模型，理解 RBAC 与数据权限的实现思路。
2. 通过 `yudao-server` 中的示例业务（如用户、角色、部门）掌握 MyBatis Plus 的 CRUD、分页、填充机制。
3. 对照 Flowable 的 XML 流程文件与后端 Service，学习业务流程与业务代码的解耦方式。
4. 使用 Docker Compose 本地一键部署，先跑通前后端，再逐步替换为生产环境配置。

##### 落地要点
- 在引入新模块前，先在 dev 分支验证兼容性，避免因依赖冲突导致启动失败。
- 对租户字段进行统一管理，避免硬编码 `tenant_id`，建议在全局拦截器或 AOP 中统一注入。
- 前端权限路由需与后端返回的菜单保持同步，最好使用统一的权限模型生成工具。
- 业务高峰期关注 MyBatis Plus 的慢查询日志，必要时使用读写分离或分库分表。

（全文约 870 字）

---
## 学习要点

- 前后端分离架构采用 Vue3 + Vite + TypeScript 前端配合 Spring Boot + MyBatis‑Plus 后端，实现开发解耦和高效协作。
- 基于 RBAC 模型的细粒度权限控制覆盖页面、按钮和接口，显著提升系统安全性。
- 采用 JWT 实现无状态认证并支持 Token 自动刷新，确保跨域访问的可扩展性。
- 提供可视化代码生成器，一键生成 CRUD、树形结构和分页等常用业务代码，大幅加快开发进度。
- 使用 Element Plus 作为 UI 组件库，统一样式并快速构建美观的管理界面。
- 动态路由与菜单根据用户权限实时生成侧边栏，提高系统的灵活性和可维护性。
- 集成多租户和国际化支持，满足企业级复杂业务场景的需求。

---
## 引用

- **GitHub 仓库**: [https://github.com/YunaiV/ruoyi-vue-pro](https://github.com/YunaiV/ruoyi-vue-pro)
- **DeepWiki**: [https://deepwiki.com/YunaiV/ruoyi-vue-pro](https://deepwiki.com/YunaiV/ruoyi-vue-pro)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [后端](/categories/%E5%90%8E%E7%AB%AF/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Java](/tags/java/) / [Spring Boot](/tags/spring-boot/) / [Vue](/tags/vue/) / [后台管理](/tags/%E5%90%8E%E5%8F%B0%E7%AE%A1%E7%90%86/) / [RBAC权限](/tags/rbac%E6%9D%83%E9%99%90/) / [工作流](/tags/%E5%B7%A5%E4%BD%9C%E6%B5%81/) / [ERP](/tags/erp/) / [SaaS多租户](/tags/saas%E5%A4%9A%E7%A7%9F%E6%88%B7/)
- 场景： [后端开发](/scenarios/%E5%90%8E%E7%AB%AF%E5%BC%80%E5%8F%91/) / [全栈开发](/scenarios/%E5%85%A8%E6%A0%88%E5%BC%80%E5%8F%91/) / [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [JeecgBoot：集成AI低代码平台与代码生成器的Java开发框架]({{< relref "posts/20260129-github_trending-jeecgboot-jeecgboot-3.md" >}})
- [JeecgBoot：AI 驱动的低代码平台，支持零代码与代码生成双模式]({{< relref "posts/20260317-github_trending-jeecgboot-jeecgboot-2.md" >}})
- [JeecgBoot：AI 驱动的低代码平台，支持零代码搭建与代码生成]({{< relref "posts/20260318-github_trending-jeecgboot-jeecgboot-2.md" >}})
- [🚀 Halo：强大开源建站神器！GitHub 趋势榜首选 ⭐]({{< relref "posts/20260126-github_trending-halo-dev-halo-4.md" >}})
- [JeecgBoot：AI低代码平台集成代码生成器与知识库]({{< relref "posts/20260130-github_trending-jeecgboot-jeecgboot-3.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*