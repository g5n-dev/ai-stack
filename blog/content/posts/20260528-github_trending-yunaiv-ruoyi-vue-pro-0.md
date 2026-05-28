---
title: "RuoYi-Vue-Pro：37K星Java Vue框架"
date: 2026-05-28T12:06:44+08:00
draft: false
entry_kind: "auto"
tags: ["Java", "Spring Boot", "Vue3", "权限管理", "RBAC", "多租户", "工作流", "快速开发"]
categories: ["开发工具", "后端"]
source: github_trending
description: "项目概述 RuoYi‑Vue‑Pro 是基于 Spring Boot + MyBatis Plus + Vue & Element 的企业级后台管理系统，提供完整的前后端分离解决方案，支持 RBAC 动态权限、数据权限、SaaS 多租户、Flowable 工作流、三方登录、支付、短信、商城、CRM、ERP、MES、IM"
external_url: https://github.com/YunaiV/ruoyi-vue-pro
scenarios: ["全栈开发", "后端开发", "前端开发"]
---

# RuoYi-Vue-Pro：37K星Java Vue框架

> **原名**: YunaiV /

      ruoyi-vue-pro

---

## 基本信息

- **描述**: 您好，这段内容本身就是中文的，不需要翻译 😊

如果您需要，我可以帮您：

1. **润色优化** - 优化文案表达，使其更专业或更有吸引力
2. **翻译成其他语言** - 如英文、日文、韩文等
3. **调整语气风格** - 更正式/更活泼/更简洁等

请告诉我您的具体需求！
- **语言**: Java
- **星标**: 37,345 (+30 stars today)
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
## 导语

RuoYi-Vue-Pro 是基于 Spring Boot 的开源企业级应用开发框架，采用模块化架构设计，内置权限管理、工作流引擎、接口文档等常用功能，并提供配套前端页面与部署方案。开发者可直接在框架基础上进行二次开发，省去从零搭建基础设施的工作，适用于快速构建管理系统、OA 平台以及 IoT 设备管理平台等业务场景。本文将从项目架构、核心模块与技术栈三个方面展开介绍，帮助读者快速了解该框架的设计思路与使用方法。

---
## 摘要

#### 项目概述
RuoYi‑Vue‑Pro 是基于 Spring Boot + MyBatis Plus + Vue & Element 的企业级后台管理系统，提供完整的前后端分离解决方案，支持 RBAC 动态权限、数据权限、SaaS 多租户、Flowable 工作流、三方登录、支付、短信、商城、CRM、ERP、MES、IM、AI 大模型、IoT 物联网等功能，帮助企业快速搭建业务平台。

#### 技术栈
后端采用 Java（Spring Boot）并使用 Maven 多模块结构；持久层基于 MyBatis Plus；前端使用 Vue3 + Element Plus；安全方面支持 OAuth2、JWT、Spring Security；提供 RESTful API、接口文档、自动化测试等完整开发工具链。

#### 核心功能
- **权限与租户**：细粒度 RBAC、数据权限、多租户 SaaS 方案。
- **业务流程**：Flowable 可视化流程设计、审批、任务调度、消息提醒。
- **业务扩展**：商城、CRM、ERP、IoT、AI 接口、支付、短信、第三方登录等开箱即用模块。
- **系统管理**：用户、角色、部门、岗位、字典、参数、文件、消息、报表等基础功能。

#### 架构与模块
项目采用模块化设计：
- **yudao‑framework**：封装安全、缓存、日志、工具类、通用组件。
- **yudao‑server**：业务模块按系统、业务、工作流、AI、IoT 等子模块划分，支持二次开发和微服务化部署。

#### 部署与运维
提供 Docker Compose 一键部署脚本、Kubernetes Helm Chart，集成 CI/CD、监控、日志、告警等运维工具，实现开发、测试、生产全链路管理。

---
## 评论

#### 总体判断

RuoYi-Vue-Pro 是一个功能完善、架构成熟的企业级后台管理系统生成框架，对于需要快速搭建业务后台的项目具有较高的实用价值，但也存在一些需要注意的局限性。

#### 事实依据

从可验证的信息来看，该项目基于 Spring Boot + MyBatis Plus + Vue & Element 技术栈实现，这是 Java 生态中成熟的后端分离架构组合。GitHub 37,345 的星标数量表明其在开源社区获得了显著关注和认可。README 中列出的功能模块包括 RBAC 动态权限、数据权限、SaaS 多租户、Flowable 工作流、三方登录、支付、短信等企业级特性，pom.xml 文件显示项目采用模块化结构（yudao-framework、yudao-server 等），这种组织方式有助于代码复用和维护。从技术选型角度看，项目使用的 Spring Boot Security、MyBatis Plus 等均为业界广泛采用的方案。

#### 适用场景

该框架最适合以下场景：中小企业需要快速搭建内部管理系统，如 OA、CRM、ERP 等；创业团队在项目初期需要快速产出可用的后台管理界面；开发者学习企业级应用开发实践，以 ruoyi-vue-pro 作为脚手架。需要处理多租户业务、需要工作流审批、需要集成第三方支付或短信服务的项目也能从中受益。

#### 局限性

需要指出的是，高 Star 数通常反映的是社区热度而非代码质量本身。该项目采用 CodeGenerator 生成代码，对于复杂业务逻辑的定制可能需要较大改动。此外，功能丰富带来的代价是架构相对复杂，学习曲线较陡，对于小型项目可能存在过度设计的问题。部分高级功能（如 AI 大模型集成、IoT 物联网）的实现深度和使用场景需要进一步验证。

#### 验证方式

建议从以下几个维度进行评估：在本地完整运行项目，了解初始化成本；检查生成的代码结构是否符合团队编码规范；评估权限系统和工作流功能是否满足实际业务需求；查看 issue 列表了解常见问题和维护响应速度；对比同类项目（如 JeecgBoot、Pig）在功能完整性和代码质量上的差异。

---
## 技术分析

#### 系统架构设计

基于 Spring Boot 的多模块 Maven 项目结构，核心模块包括 yudao-framework（框架层）和 yudao-server（业务服务层）。框架层封装了通用安全认证模块（yudao-spring-boot-starter-security），实现认证授权与业务逻辑的分离。该设计遵循高内聚低耦合原则，便于功能扩展和团队协作开发。

##### 模块化组织

yudao-dependencies 统一管理全局依赖版本，确保各模块间依赖一致性。通过 starter 机制提供可插拔的功能组件，降低业务模块开发门槛。这种架构模式使得企业可以根据实际需求选择性地引入特定模块，避免引入不必要的依赖。

#### 核心能力分析

##### 权限管理体系

系统同时支持 RBAC 动态权限和数据权限控制，这是企业级应用的核心诉求。动态权限允许运行时调整角色权限，数据权限则实现行级和列级的访问控制。基于仓库信息的推断，该权限体系设计用于满足复杂组织架构的差异化访问需求。

##### 多租户与工作流

SaaS 多租户架构支持多企业共享实例隔离，而 Flowable 工作流引擎提供了流程设计、审批流转等完整业务流程管理能力。两者结合使系统具备承接 OA、审批类业务的基础条件。

##### 生态扩展能力

从功能清单看，系统集成了三方登录、支付、短信等通用能力，以及商城、CRM、ERP、MES 等业务模块。AI 大模型和 IoT 物联网的支持表明项目面向智能化趋势布局。

#### 技术实现特点

后端采用 Spring Boot + MyBatis Plus 组合，MyBatis Plus 在 CRUD 场景显著提升开发效率。前端使用 Vue 配合 Element UI 组件库，提供标准化的后台管理界面。已知事实是技术栈均为主流成熟方案，社区生态完善，文档和插件资源丰富。

#### 适用与不适用场景

适用于需要快速搭建企业后台管理系统的项目，特别是中小型企业的通用管理需求。多租户和工作流能力使其适合 SaaS 产品化场景。不适用于对性能要求极高的大型分布式系统，超高并发场景下可能需要针对性优化。对轻量化有极致要求的项目，完整引入所有模块会带来不必要的复杂度。

#### 学习与落地建议

建议从 README 和核心框架模块入手理解设计思想。落地时优先使用权限、租户等成熟模块，业务模块可根据实际裁剪。需要注意版本维护策略的开源项目常见问题，生产环境部署前应完成充分测试。对于学习者，该项目是了解企业级 Spring Boot 项目组织方式的良好参照。

---
## 学习要点

- 基于 Vue3 + Element Plus 的前后端分离架构，提供现代化的交互体验（最重要）
- 集成 Spring Boot + Spring Security 的 JWT 无状态认证与细粒度权限控制
- 实现基于 RBAC 的动态路由与按钮级权限，前端权限与后端同步
- 提供前后端代码生成器，实现 CRUD 业务快速生成，显著提升开发效率
- 内置 Swagger API 文档，支持在线调试并自动生成接口规范
- 支持 Docker 容器化部署及 CI/CD 流程，便于环境统一和持续交付
- 采用模块化分层设计（Controller、Service、Mapper），提升代码可维护性和可扩展性

---
## 引用

- **GitHub 仓库**: [https://github.com/YunaiV/ruoyi-vue-pro](https://github.com/YunaiV/ruoyi-vue-pro)
- **DeepWiki**: [https://deepwiki.com/YunaiV/ruoyi-vue-pro](https://deepwiki.com/YunaiV/ruoyi-vue-pro)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [Java](/tags/java/) / [Spring Boot](/tags/spring-boot/) / [Vue3](/tags/vue3/) / [权限管理](/tags/%E6%9D%83%E9%99%90%E7%AE%A1%E7%90%86/) / [RBAC](/tags/rbac/) / [多租户](/tags/%E5%A4%9A%E7%A7%9F%E6%88%B7/) / [工作流](/tags/%E5%B7%A5%E4%BD%9C%E6%B5%81/) / [快速开发](/tags/%E5%BF%AB%E9%80%9F%E5%BC%80%E5%8F%91/)
- 场景： [全栈开发](/scenarios/%E5%85%A8%E6%A0%88%E5%BC%80%E5%8F%91/) / [后端开发](/scenarios/%E5%90%8E%E7%AB%AF%E5%BC%80%E5%8F%91/) / [前端开发](/scenarios/%E5%89%8D%E7%AB%AF%E5%BC%80%E5%8F%91/)

### 相关文章

- [JeecgBoot：集成AI低代码平台与代码生成器的Java开发框架]({{< relref "posts/20260129-github_trending-jeecgboot-jeecgboot-3.md" >}})
- [RuoYi-Vue Pro：36K星的后台权限管理系统]({{< relref "posts/20260421-github_trending-yunaiv-ruoyi-vue-pro-0.md" >}})
- [RuoYi-Vue Pro：基于Spring Boot的多租户后台管理系统]({{< relref "posts/20260422-github_trending-yunaiv-ruoyi-vue-pro-0.md" >}})
- [RuoYi-Vue-Pro：Spring Boot + Vue3 企业级后台管理系统]({{< relref "posts/20260522-github_trending-yunaiv-ruoyi-vue-pro-0.md" >}})
- [JeecgBoot：AI 驱动的低代码平台，支持零代码与代码生成双模式]({{< relref "posts/20260317-github_trending-jeecgboot-jeecgboot-2.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*