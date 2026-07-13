---
title: "RuoYi-Vue Pro：36K星的后台权限管理系统"
date: 2026-04-21T17:17:43+08:00
draft: false
entry_kind: "auto"
tags: ["后台管理系统", "Java", "Spring Boot", "Vue", "RBAC权限", "工作流", "开源项目", "SaaS多租户"]
categories: ["开发工具"]
source: github_trending
description: "项目简介 仓库名称 YunaiV/ruoyi‑vue‑pro，基于 Spring Boot + MyBatis Plus + Vue & Element 构建的后台管理系统，配套微信小程序端。官方推荐版本，对原有 RuoYi‑Vue 全面重构。 编程语言：Java 星标数：36,637（+37 today） 技术栈 -"
external_url: https://github.com/YunaiV/ruoyi-vue-pro
scenarios: ["后端开发", "Web应用开发", "数据库"]
---

# RuoYi-Vue Pro：36K星的后台权限管理系统

> **原名**: YunaiV /

      ruoyi-vue-pro

---

## 基本信息

- **描述**: 您好！我注意到您提供的这段内容**已经是中文**了（简体中文）。

这段内容是关于 **RuoYi-Vue Pro** 后台管理系统的推广文案，描述了其技术栈（Spring Boot + MyBatis Plus + Vue & Element）和功能特性（RBAC权限、数据权限、工作流、三方登录、支付、短信等）。

请问您是否：
1. **想要翻译成英文**？
2. **有其他语言的原文**需要翻译成中文？

请提供需要翻译的内容，我会为您准确翻译并保持原文格式和语气。😊
- **语言**: Java
- **星标**: 36,637 (+37 stars today)
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

RuoYi-Vue Pro 是一款基于 Spring Boot + MyBatis Plus + Vue & Element 构建的企业级后台管理系统，采用模块化设计，提供了 RBAC 权限管理、数据权限控制、工作流引擎、三方登录、支付、短信等开箱即用的功能。该项目适用于需要快速搭建企业级应用后台的开发者，能够显著减少从零开发常见业务模块的时间成本。本文将围绕项目架构、核心功能模块以及本地部署流程进行介绍，帮助读者快速上手并落地实践。

---
## 摘要

#### 项目简介
仓库名称 YunaiV/ruoyi‑vue‑pro，基于 Spring Boot + MyBatis Plus + Vue & Element 构建的后台管理系统，配套微信小程序端。官方推荐版本，对原有 RuoYi‑Vue 全面重构。
编程语言：Java
星标数：36,637（+37 today）

#### 技术栈
- 后端：Spring Boot、MyBatis Plus、Flowable 工作流
- 前端：Vue.js、Element UI
- 数据库：支持 MySQL、PostgreSQL 等主流关系库
- 生态：微信小程序、三方登录、支付、短信等集成

#### 核心功能
- RBAC 动态权限 + 数据权限，支持细粒度控制
- SaaS 多租户，可按租户独立数据隔离
- 工作流引擎（Flowable），实现审批、流转等业务流程
- 商城模块：商品、订单、支付、物流完整闭环
- 企业资源管理：CRM、ERP、MES 系统集成
- IM 即时通讯，支持单聊、群聊、消息推送
- AI 大模型接入，提供智能问答、语义分析等能力
- IoT 物联网：设备接入、状态监控、指令下发
- 其他能力：短信验证码、第三方登录（微信、QQ、GitHub 等）、文件存储、报表统计

#### 架构特点
- 模块化设计，业务模块按需加载，易于扩展
- 基于 Spring Boot 自动配置，开箱即用，提供统一错误处理、日志、监控
- 前端采用 Vue + Element，统一 UI 规范，支持主题定制
- 支持 Docker、K8s 部署，提供 CI/CD 流程示例

#### 社区与贡献
- 开源免费，Star 超 36k，持续迭代更新
- 官方文档完善，提供详细示例与视频教程
- 活跃社区，贡献者众多，功能插件不断丰富

---
## 评论

#### 总体判断

RuoYi-Vue-Pro 是一个功能高度集成的企业级后台管理系统脚手架，技术栈成熟、功能覆盖面广，适合作为快速启动项目的技术框架。但其代码质量、架构设计深度和长期维护性需要项目负责人自行评估。

#### 技术依据

从源码结构看，该项目采用标准的三层架构，Spring Boot 提供核心框架，MyBatis Plus 处理持久层，前端使用 Vue + Element UI。这一组合是国内企业开发的主流选型，技术风险相对可控。

项目声称支持 RBAC 动态权限、数据权限、SaaS 多租户、Flowable 工作流引擎等企业级功能。这些特性在 README 中有明确列举，部分功能存在对应的模块代码。然而需要说明的是，这些功能的实现完整度、测试覆盖率和生产环境适配情况，需要使用者自行审查源码或进行实际验证。

项目采用 starter 机制封装通用功能模块，试图实现模块解耦。这种做法在降低使用门槛方面有一定价值，但也可能导致业务逻辑与框架代码耦合度较高，影响后续定制化开发的灵活性。

#### 适用场景

该系统适合以下场景：需要快速搭建后台管理原型或 MVP 的项目；对功能丰富度有较高要求、希望开箱即用的团队；作为学习企业级 Java Web 开发完整流程的参考项目。由于集成了商城、CRM、ERP、IoT 等模块，在中小型信息化项目建设中具有较好的实用价值。

#### 局限与风险

基于事实信息推断，该项目存在以下潜在局限：代码注释和文档详尽程度可能不足以支撑大规模团队协作；高度封装的特性可能在复杂业务场景下成为定制化障碍；开源协议为 GPL，这意味着二次开发后的闭源发布可能面临法律风险。

#### 验证方式建议

建议在生产环境采用前，进行以下验证：审查核心模块代码实现逻辑；通过压测验证系统性能上限；评估社区活跃度和 issue 响应速度；确认所使用模块的许可证兼容性。

---
## 技术分析

#### 架构概述
##### 模块划分
已知：项目采用 Maven 多模块结构，主模块包括 `yudao-dependencies`、`yudao-framework`、`yudao-spring-boot-starter-security`、`yudao-server` 等。推断：各模块职责明确，`yudao-framework` 承载通用组件（如日志、异常、统一响应），`yudao-spring-boot-starter-security` 实现安全与鉴权，`yudao-server` 聚合业务功能。模块之间通过依赖管理实现解耦，既可作为单体部署，也可拆分出微服务。

##### 技术栈概览
已知：后端基于 Spring Boot + MyBatis Plus，前端使用 Vue + Element UI。推断：采用前后端分离模式，后端提供 RESTful 接口，前端通过 axios 调用；可能使用 JWT 或 Spring Security Session 实现无状态认证；Flowable 用于业务流程编排。

#### 核心能力
##### 权限与安全
已知：实现 RBAC 动态权限、数据权限。推断：权限模型基于 Spring Security 的 Filter 链，配合自定义注解实现细粒度控制；数据权限可能通过 MyBatis Plus 的拦截器或 AOP 实现行级过滤。

##### 多租户与 SaaS
已知：支持 SaaS 多租户。推断：租户标识（tenant_id）可能放在请求头或 ThreadLocal 中，后端通过拦截器统一注入，支持租户数据隔离和租户级别的配置。

##### 工作流与业务编排
已知：集成 Flowable 工作流。推断：提供流程设计器（可能为 Flowable Modeler）或自定义 UI，配合业务表单实现审批、流转等场景；流程实例与业务数据通过业务键（businessKey）关联。

##### 前端与交互
已知：Vue + Element UI。推断：采用 Vue CLI/Vite 构建，使用 Vue Router 动态路由、Vuex/Pinia 状态管理；页面模板基于 Element 的组件库，实现响应式布局、表单验证、权限按钮控制。

##### 第三方集成
已知：支持三方登录、支付、短信、商城、CRM、ERP、MES、IM、AI 大模型、IoT。推断：集成方式多为 SDK 接入（如微信、支付宝、阿里云短信）或 RESTful 对接；AI 大模型可能通过 HTTP 调用外部推理服务；IoT 可能使用 MQTT 或 CoAP 协议接入设备。

#### 技术实现细节
##### 后端实现
已知：Spring Boot、MyBatis Plus、Flowable、Maven 多模块。推断：采用 Spring Boot Starter 机制，MyBatis Plus 的 Wrapper 进行动态 SQL；可能使用 `@EnableTransactionManagement` 管理事务，使用 `spring-boot-starter-validation` 做参数校验。

##### 前端实现
已知：Vue、Element UI。推断：使用 Vue 3 Composition API；路由守卫配合后端返回的权限码进行动态渲染；通过 axios 拦截器统一添加 Token 与租户标识。

##### 插件化与扩展
推断：业务模块以 Spring Boot Starter 形式提供，可通过添加依赖快速启用；可能采用自定义注解 + AOP 实现统一日志、审计、限流等横切关注点。

#### 适用场景
##### 适用
- 需要快速搭建企业级后台管理系统的团队（尤其适用于内部管理系统、CRM、ERP 等）。
- 对权限、租户、工作流有明确需求的项目。
- 希望前后端分离、具备高可扩展性的项目。

##### 不适用
- 对前端技术栈有特定限制（如仅限 React 或 Angular）的团队。
- 对微服务拆分要求极高、需要独立部署每个业务模块的项目（当前结构更倾向单体或模块化单体）。
- 对实时性要求极高的 IoT 场景（需要额外的高并发、低延迟架构改进）。

#### 学习与落地建议
##### 学习路径
1. **阅读整体结构**：先从根目录的 `pom.xml` 与 `README.md` 入手，了解模块划分与依赖关系。
2. **核心模块深挖**：`yudao-framework` 与 `yudao-spring-boot-starter-security` 是理解权限与安全的关键，建议先弄清其中的 Filter、Interceptor、SecurityConfig 实现。
3. **工作流**：查看 Flowable 配置与已有的流程定义（如 BPMN 文件），了解业务键绑定方式。
4. **前端**：从 `src/views` 与 `src/router` 开始，熟悉路由守卫和权限按钮的渲染逻辑。
5. **实战演练**：在本地完成一次完整的登录、角色分配、数据权限过滤的闭环测试。

##### 落地注意点
- **版本兼容**：确认 JDK、Maven、Node 与项目声明的版本匹配，避免因环境差异导致的构建错误。
- **租户隔离**：在业务表中显式添加 `tenant_id` 并在后端统一拦截，确保查询时自动注入。
- **安全审计**：建议开启 Spring Security 的审计日志，记录登录、权限变更、关键业务操作。
- **性能调优**：MyBatis Plus 的分页插件与缓存（Redis）应配合使用，防止大表全表扫描。
- **部署方式**：初期可采用单体 Jar 部署，后期若业务模块独立演进，可将 `yudao-server` 拆分为多个微服务并使用 Spring Cloud 或 K8s 进行管理。

---
## 学习要点

- 能否提供更多关于 ruoyi‑vue‑pro 的具体功能或项目描述，以便提炼出 5‑7 条关键要点？

---
## 引用

- **GitHub 仓库**: [https://github.com/YunaiV/ruoyi-vue-pro](https://github.com/YunaiV/ruoyi-vue-pro)
- **DeepWiki**: [https://deepwiki.com/YunaiV/ruoyi-vue-pro](https://deepwiki.com/YunaiV/ruoyi-vue-pro)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/)
- 标签： [后台管理系统](/tags/%E5%90%8E%E5%8F%B0%E7%AE%A1%E7%90%86%E7%B3%BB%E7%BB%9F/) / [Java](/tags/java/) / [Spring Boot](/tags/spring-boot/) / [Vue](/tags/vue/) / [RBAC权限](/tags/rbac%E6%9D%83%E9%99%90/) / [工作流](/tags/%E5%B7%A5%E4%BD%9C%E6%B5%81/) / [开源项目](/tags/%E5%BC%80%E6%BA%90%E9%A1%B9%E7%9B%AE/) / [SaaS多租户](/tags/saas%E5%A4%9A%E7%A7%9F%E6%88%B7/)
- 场景： [后端开发](/scenarios/%E5%90%8E%E7%AB%AF%E5%BC%80%E5%8F%91/) / [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/) / [数据库](/scenarios/%E6%95%B0%E6%8D%AE%E5%BA%93/)

### 相关文章

- [🚀 Halo：强大开源建站神器！GitHub 趋势榜首选 ⭐]({{< relref "posts/20260126-github_trending-halo-dev-halo-4.md" >}})
- [vue-pure-admin：基于 Vue3+Vite+TS 的后台管理系统]({{< relref "posts/20260129-github_trending-pure-admin-vue-pure-admin-6.md" >}})
- [⚡️ pure-admin：开源最强Vue3管理后台！🔥]({{< relref "posts/20260127-github_trending-pure-admin-vue-pure-admin-6.md" >}})
- [🔥Vue3后台天花板！pure-admin 震撼来袭！⚡️]({{< relref "posts/20260128-github_trending-pure-admin-vue-pure-admin-6.md" >}})
- [JeecgBoot：集成AI低代码平台与代码生成器的Java开发框架]({{< relref "posts/20260129-github_trending-jeecgboot-jeecgboot-3.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*