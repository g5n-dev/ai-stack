---
title: "若依Vue Pro：Java后台管理系统，支持多租户工作流"
date: 2026-05-30T13:54:44+08:00
draft: false
entry_kind: "auto"
tags: ["后台管理", "多租户", "工作流", "RBAC", "SpringBoot", "Vue", "SaaS", "AI大模型"]
categories: ["后端", "开源生态"]
source: github_trending
description: "项目概述 RuoYi‑Vue‑Pro 是基于 Spring Boot + MyBatis Plus + Vue & Element 构建的开源企业级后台管理系统，并配套微信小程序前端。项目被官方推荐，当前拥有 37,443 颗星（+64 今日），旨在为企业应用提供完整的脚手架，实现快速交付。 核心技术栈 - 后端：Ja"
external_url: https://github.com/YunaiV/ruoyi-vue-pro
scenarios: ["后端开发", "全栈开发", "Web应用开发"]
---

# 若依Vue Pro：Java后台管理系统，支持多租户工作流

> **原名**: YunaiV /

      ruoyi-vue-pro

---

## 基本信息

- **描述**: 🔥 官方推荐 🔥 RuoYi-Vue 全新 Pro 版本，全面优化重构所有功能。基于 Spring Boot + MyBatis Plus + Vue & Element 实现的后台管理系统 + 微信小程序，支持 RBAC 动态权限、数据权限、SaaS 多租户、Flowable 工作流、三方登录、支付、短信、商城、CRM、ERP、MES、IM、AI 大模型、IoT 物联网等功能。您的 ⭐️ Star ⭐️，是作者持续创作的动力！
- **语言**: Java
- **星标**: 37,443 (+64 stars today)
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

ruoyi-vue-pro 是基于 Spring Boot + MyBatis Plus + Vue3 + Element Plus 构建的企业级后台管理系统，提供了完整的权限控制、工作流引擎、多租户等基础功能，并内置了电商、CRM、ERP、物联网等多个业务模块的参考实现。本文将从系统架构、核心模块实现和实战部署三个维度展开分析，帮助开发者快速掌握项目结构并落地到实际业务中。

---
## 摘要

#### 项目概述
RuoYi‑Vue‑Pro 是基于 Spring Boot + MyBatis Plus + Vue & Element 构建的开源企业级后台管理系统，并配套微信小程序前端。项目被官方推荐，当前拥有 37,443 颗星（+64 今日），旨在为企业应用提供完整的脚手架，实现快速交付。

#### 核心技术栈
- 后端：Java、Spring Boot、MyBatis Plus、Flowable 工作流
- 前端：Vue.js、Element UI、微信小程序
- 其他：Redis、ShardingSphere、Maven

#### 主要功能模块
- RBAC 动态权限、数据权限、SaaS 多租户
- 三方登录（OAuth、SSO）、支付、短信、邮件
- 电商（商城、订单、库存）、CRM、ERP、MES
- IM 实时通讯、AI 大模型对接、IoT 设备管理
- 工作流引擎（Flowable）支持审批与流程自动化

#### 架构特点
- 模块化设计，核心框架（yudao‑framework）与业务模块解耦，便于二次开发
- 统一提供权限、数据字典、文件、日志、监控等公共组件
- 支持 Docker、Kubernetes 部署，提供 CI/CD 示例
- 文档完善、社区活跃，帮助开发者快速上手

#### 适用场景
适合中小型企业或团队快速构建内部管理系统、业务平台以及面向用户的移动端/小程序产品。

---
## 评论

RuoYi-Vue-Pro 是一个功能完备、模块化程度高且社区活跃的企业级后台脚手架，适合快速搭建业务系统。

#### 依据
基于 Spring Boot、MyBatis Plus、Vue+Element 的成熟技术栈，提供 RBAC、数据权限、SaaS 多租户、Flowable 工作流等企业常用模块，且已拥有 37k+ 的 star 与持续的版本迭代。

#### 适用场景
适用于企业内部管理系统（OA、CRM、ERP）、SaaS 平台、IoT 设备管理后台以及需要快速原型验证的中小型项目；尤其是对权限控制、工作流和前后端分离有明确需求的团队。

#### 局限
功能丰富的同时导致项目结构庞大，新人上手成本较高；大量默认实现可能不符合特定业务细节，需要二次开发；依赖的第三方服务（如短信、支付）需要自行对接和适配。

#### 验证方式
可在本地通过 Maven 编译后启动 yudao‑server 模块，配合前端 vue 运行，查看登录、权限、工作流等核心功能；项目内置单元测试与集成测试，可通过 mvn test 验证业务逻辑；社区文档和 ISSUE 区提供了常见问题的排查路径。

---
## 技术分析

#### 系统架构概览
- **模块化分层**：项目采用多模块 Maven 结构，根 `pom.xml` 声明全局依赖，子模块 `yudao-framework`、`yudao-server` 等分别承担框架、业务与入口职责，实现代码复用与职责分离。
- **前后端分离**：后端基于 Spring Boot，提供 RESTful API；前端使用 Vue 3 + Element Plus，实现页面渲染与交互。前端通过 WebSocket 与后端保持实时通信，支持数据看板等场景。

#### 核心功能
- **RBAC 与数据权限**：Spring Security 与自定义 `SecurityFilter` 结合，基于注解 `@PreAuthorize` 完成菜单、按钮级别的细粒度控制；数据权限通过 MyBatis Plus 的 `DataScopeInterceptor` 实现行级过滤。
- **SaaS 多租户**：在数据库层面使用租户 ID 字段隔离，配合 `TenantFilter` 统一注入，实现租户独立配置、资源隔离与计费。
- **工作流**：集成 Flowable，提供流程设计器、任务审批、实例监控等完整生命周期管理，业务节点可通过 Spring Bean 调用业务逻辑。
- **业务生态**：内置商城、CRM、ERP、IoT、AI 大模型等插件式模块，源码中对应子包如 `yudao-module-mall`、`yudao-module-crm` 等，可按需引入或替换。

#### 技术实现细节
- **后端框架**：Spring Boot 2.7、MyBatis Plus 3.5，配合 `yudao-dependencies` 统一版本管理，避免依赖冲突。
- **安全实现**：JWT + RefreshToken 双令牌机制，`TokenService` 提供 token 生成、刷新与黑名单管理；登录采用短信、邮箱或第三方（QQ、微信）OAuth2。
- **前端工程**：Vue 3 `Composition API` + Vite 构建，路由守卫统一校验 token，Element Plus 组件库提供表格、表单、弹窗等常用 UI。
- **第三方集成**：支付（支付宝、微信）、短信（阿里云、腾讯云）、对象存储（OSS、MinIO）等均通过统一的 `AbstractIntegration` 抽象类实现插件化接入。

#### 适用场景
- **适合**：企业内部管理系统（OA、HRM）、B2C/B2B 电商平台、需要租户隔离的 SaaS 服务、需要复杂审批流的工作流系统、以及需要快速原型验证的创新业务。
- **不适合**：对极低延迟（毫秒级）或超大规模分布式（跨地域多活）有严格要求的实时交易系统；需要完全自定义 UI/UX 的高度品牌化产品（因前端框架相对固定）。

#### 学习与落地建议
- **学习路径**：先通读根 `pom.xml` 与 `yudao-dependencies` 了解依赖版本；再从 `yudao-framework/yudao-spring-boot-starter-security` 入手掌握权限模型；随后阅读 `yudao-server` 中的业务示例（如用户管理、订单模块），逐步扩展至工作流或 AI 插件。
- **落地要点**：① 生产环境请将 MySQL、Redis、OSS 等配置抽取至 `application-prod.yml` 并开启加密；② 部署时建议使用 Docker‑Compose 或 K8s 编排，前端使用 Nginx 静态托管；③ 多租户场景下需关注租户数据的备份与迁移策略；④ 引入新业务插件时，应遵循项目已有的模块化规范，避免对核心框架产生强耦合。

> 注：部分功能（如 AI 大模型、IoT 设备接入）在源码中属于实验性模块，尚未提供完整的生产文档，实际落地前需自行评估稳定性与业务匹配度。

---
## 学习要点

- 采用前后端分离架构，前端基于 Vue 与 Element UI，后端基于 Spring Boot，实现开发与部署解耦（最重要）
- 使用 JWT 实现无状态身份认证，配合 Spring Security 完成统一的权限校验
- 通过 Shiro 或 Spring Security 实现基于 RBAC 的细粒度权限控制，支持数据权限行级过滤
- 采用 MyBatis‑Plus 简化持久层开发，支持自动生成 CRUD 代码，提高开发效率
- 集成 Swagger/knife4j 在线 API 文档，前后端协同更高效
- 提供代码生成器，前端 Vue 组件和后端 Service、Mapper 一键生成，进一步提升开发速度
- 支持 Docker 容器化部署，配合 Maven 多模块结构，便于微服务拆分与扩展

---
## 引用

- **GitHub 仓库**: [https://github.com/YunaiV/ruoyi-vue-pro](https://github.com/YunaiV/ruoyi-vue-pro)
- **DeepWiki**: [https://deepwiki.com/YunaiV/ruoyi-vue-pro](https://deepwiki.com/YunaiV/ruoyi-vue-pro)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [后端](/categories/%E5%90%8E%E7%AB%AF/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [后台管理](/tags/%E5%90%8E%E5%8F%B0%E7%AE%A1%E7%90%86/) / [多租户](/tags/%E5%A4%9A%E7%A7%9F%E6%88%B7/) / [工作流](/tags/%E5%B7%A5%E4%BD%9C%E6%B5%81/) / [RBAC](/tags/rbac/) / [SpringBoot](/tags/springboot/) / [Vue](/tags/vue/) / [SaaS](/tags/saas/) / [AI大模型](/tags/ai%E5%A4%A7%E6%A8%A1%E5%9E%8B/)
- 场景： [后端开发](/scenarios/%E5%90%8E%E7%AB%AF%E5%BC%80%E5%8F%91/) / [全栈开发](/scenarios/%E5%85%A8%E6%A0%88%E5%BC%80%E5%8F%91/) / [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [RuoYi-Vue Pro：基于Spring Boot的多租户后台管理系统]({{< relref "posts/20260422-github_trending-yunaiv-ruoyi-vue-pro-0.md" >}})
- [RuoYi-Vue Pro Java后台管理系统，支持微信小程序集成]({{< relref "posts/20260529-github_trending-yunaiv-ruoyi-vue-pro-0.md" >}})
- [🔥Vue管理后台王者！GitHub爆赞🔥极速开发神器！]({{< relref "posts/20260125-github_trending-zxwk1998-vue-admin-better-9.md" >}})
- [RuoYi-Vue Pro：36K星的后台权限管理系统]({{< relref "posts/20260421-github_trending-yunaiv-ruoyi-vue-pro-0.md" >}})
- [ruoyi-vue-pro Java后台管理系统企业级解决方案]({{< relref "posts/20260528-github_trending-yunaiv-ruoyi-vue-pro-0.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*