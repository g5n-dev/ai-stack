---
title: "ruoyi-vue-pro：Java后台管理系统，支持RBAC/工作流/多租户"
date: 2026-05-22T20:14:43+08:00
draft: false
entry_kind: "auto"
tags: ["Java", "Vue", "RBAC", "工作流", "多租户", "SaaS", "AI大模型", "IoT"]
categories: ["开发工具", "后端"]
source: github_trending
description: "项目概述 RuoYi‑Vue‑Pro 是 RuoYi‑Vue 的全新 Pro 版，基于 Spring Boot、MyBatis Plus、前端 Vue + Element，采用模块化设计，重构并优化全部功能，提供 RBAC 动态权限、数据权限、SaaS 多租户、Flowable 工作流、三方登录、支付、短信、商城、CR"
external_url: https://github.com/YunaiV/ruoyi-vue-pro
scenarios: ["后端开发", "全栈开发", "前端开发"]
---

# ruoyi-vue-pro：Java后台管理系统，支持RBAC/工作流/多租户

> **原名**: YunaiV /

      ruoyi-vue-pro

---

## 基本信息

- **描述**: 🔥 官方推荐 🔥 RuoYi-Vue 全新的 Pro 版本，已对所有功能进行优化重构。基于 Spring Boot + MyBatis Plus + Vue & Element 实现的后台管理系统 + 微信小程序，支持 RBAC 动态权限、数据权限、SaaS 多租户、Flowable 工作流、三方登录、支付、短信、商城、CRM、ERP、MES、IM、AI 大模型、IoT 物联网等功能。您的 ⭐️ Star ⭐️，是作者继续前行的动力！
- **语言**: Java
- **星标**: 37,241 (+30 stars today)
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

RuoYi-Vue-Pro 是基于 Spring Boot + MyBatis Plus + Vue 实现的全栈企业级管理平台，采用前后端分离架构。系统内置 RBAC 动态权限、数据权限、SaaS 多租户、Flowable 工作流等企业核心功能，并集成三方登录、支付、短信、商城、CRM、ERP、MES 等业务模块。适合需要快速搭建后台管理系统的开发团队或企业，本文将围绕项目整体架构、核心功能模块以及实战部署进行介绍。

---
## 摘要

#### 项目概述

RuoYi‑Vue‑Pro 是 RuoYi‑Vue 的全新 Pro 版，基于 Spring Boot、MyBatis Plus、前端 Vue + Element，采用模块化设计，重构并优化全部功能，提供 RBAC 动态权限、数据权限、SaaS 多租户、Flowable 工作流、三方登录、支付、短信、商城、CRM、ERP、MES、即时通讯、AI 大模型、物联网等企业级特性。项目使用 Java 语言，GitHub 星标 37,241（+30 今日）。

#### 技术栈

* 后端：Spring Boot、MyBatis Plus、Flowable
* 前端：Vue.js、Element UI
* 数据库：支持主流关系型数据库（MySQL、PostgreSQL 等）
* 中间件：Redis、RabbitMQ、Kafka 等（可选）

#### 核心能力

1. **权限体系**：RBAC 动态权限、数据权限，细粒度控制。
2. **多租户**：SaaS 模式下的租户隔离和资源管理。
3. **工作流**：基于 Flowable 的业务流程建模与执行。
4. **业务模块**：商城、CRM、ERP、MES、IM、AI 大模型、IoT 设备管理。
5. **集成服务**：第三方登录、支付、短信、文件存储等。

#### 架构与模块

项目采用分层+模块化结构，核心框架（yudao‑framework）提供安全、异常、日志、工具等 starter，业务模块（yudao‑server）实现具体业务功能。文档详细描述系统架构设计、模块划分、部署运维等。

#### 目标与价值

旨在为企业快速搭建后台管理系统、微服务应用提供开箱即用的完整解决方案，帮助团队缩短开发周期，降低维护成本。

---
## 评论

#### 总体判断
该项目是一款功能高度集成的企业级后台框架，核心基于 Spring Boot + MyBatis Plus + Vue/Element，拥有 37k+ 的星标数，说明社区关注度高、版本迭代活跃。凭借预设的 RBAC、数据权限、SaaS 多租户、工作流等模块，开发者在快速构建业务原型或中小型平台时可以获得显著的时间收益。

#### 依据与适用场景
- **技术栈成熟**：Spring Boot 与 MyBatis Plus 已被大量生产项目验证，Vue+Element 前端生态完善，适合需要前后端分离的团队。
- **功能覆盖广**：官方宣传的权限、支付、短信、商城、CRM、ERP、MES、IM、AI 大模型、IoT 等均已在代码中实现或预留接口，能够在单一仓库内快速集成多业务线。
- **社区活跃**：Star 数量和持续的 commit 记录表明作者在维护、问题响应和功能迭代上较为积极，文档和示例相对完整（主要中文），适合中文团队快速上手。
- **适用场景**：企业内部管理系统、SAAS 多租户平台、原型快速验证、需要整合多种业务模块（如电商+CRM）的小型或中型项目。

#### 局限与风险（推断）
- **单体仓库庞大**：功能过多导致代码体量巨大，单个模块的演进可能相互耦合，长期维护需要严格的模块化和代码规范；小团队可能面临学习曲线陡峭的问题。
- **定制成本**：若业务需求与预设模块差异大，需要深度修改底层框架，可能抵消“快速启动”的优势。
- **国际化支持**：大部分文档和社区讨论为中文，非中文团队在排查问题或二次开发时可能受限。
- **性能与扩展性**：未提供针对高并发或大规模微服务的专项优化，实际生产环境仍需依据业务流量进行调优。

#### 验证方式
1. **本地部署**：克隆仓库，配置 MySQL/PostgreSQL 与 Redis，使用 Maven/Gradle 编译后端，Node.js 编译前端，检查启动日志与页面访问是否正常。
2. **功能抽检**：选取 RBAC、数据权限、工作流等核心模块，按照官方文档执行增删改查、权限流转，验证实现是否符合预期。
3. **代码审查**：使用 SonarQube、Checkstyle 或 IDEA 插件检查代码质量、依赖安全漏洞；重点关注自定义业务代码与框架代码的耦合度。
4. **压测模拟**：在本地或测试服务器使用 JMeter 或 Gatling 对关键接口（如登录、权限校验）进行并发压测，观察响应时延与错误率，评估是否满足预期的性能基线。
5. **社区反馈**：浏览 GitHub Issues、Pull Requests 及 Gitee（或国内社区）讨论，了解近期用户反馈的稳定性与升级兼容性问题。

通过上述步骤可在不投入大规模团队资源的情况下，对该框架的可用性、适配度以及潜在风险形成较为客观的判断。

---
## 技术分析

#### 系统架构概览

RuoYi-Vue-Pro 采用单体+模块化分层结构，后端以 Spring Boot 为根基，按功能划分为 yudao‑framework（公共组件、基础设施）、yudao‑server（业务实现）以及可选的 yudao‑module‑*（如工作流、支付、CRM 等）。前端使用 Vue2/Element UI，配合独立微信小程序项目，实现前后端分离。

##### 模块化设计

- **yudao‑dependencies**：统一版本管理，确保依赖兼容。
- **yudao‑framework**：封装 Security、MyBatis‑Plus、日志、异常、工具类等。
- **yudao‑module‑*（按需引入）**：如 flowable、pay、sms、shop、crm、erp、iot、ai 等，业务模块可独立开关。

##### 技术栈

- 后端：Spring Boot 2.7.x、MyBatis‑Plus 3.5、Shiro/Shiro‑JWT、Redis、Spring Cache、Spring Task、Flowable 6.x、Spring Cloud（部分用于微服务示例）。
- 前端：Vue 2.6、Vue Router、Vuex、Element UI 2.x、Vant（小程序）。
- 数据库：MySQL 8、PostgreSQL、H2（开发）。
- 中间件：ShardingSphere‑JDBC（可选）、Nacos/Apollo（配置中心）。

#### 核心功能与实现

##### 权限管理

采用 RBAC + 数据权限两层模型。Security 模块在请求入口进行 JWT 校验、动态路由生成；数据权限通过 MyBatis‑Plus 的 DataScope 拦截器实现细粒度过滤。

##### 多租户与 SaaS

基于字段级租户隔离，配合租户数据源路由实现 SaaS 多租户。租户配置、计费、套餐等业务逻辑均封装在独立模块。

##### 工作流与业务集成

集成 Flowable，提供 BPMN 2.0 流程设计、任务分配、表单绑定。业务回调通过 Spring Event 机制与业务表同步。

##### 微信小程序与前端

小程序基于 Vant Weapp，提供登录、商品、订单等模板。前端采用 Vue + Element，实现增删改查、图表、导入导出、权限按钮等常用后台功能。

##### AI 与 IoT 集成

AI 模块封装 ChatGPT、文心一言等大模型接口，提供对话、生成能力。IoT 模块通过 MQTT/CoAP 协议接入设备，提供设备管理、实时数据、告警等基础功能。

#### 技术实现亮点

##### 后端：Spring Boot + MyBatis‑Plus

- MyBatis‑Plus 的自动 CRUD、逻辑删除、分页插件显著降低代码量。
- 使用 `spring-boot-starter-validation` 统一参数校验，异常统一封装为 `Result` 包装。
- 通过 `yudao-common` 中的工具类（如 `BeanUtil`、`StrUtil`）保持代码风格统一。

##### 前端：Vue + Element UI

- 基于 `vue-element-admin` 进行二次封装，抽取 `common/`、`api/`、`views/` 目录结构。
- 通过 `router.beforeEach` 实现权限拦截，配合后端返回的动态菜单实现细粒度按钮控制。
- 使用 `axios` 统一请求封装，支持请求重试、统一错误提示。

##### 安全性与扩展性

- Shiro 鉴权 + JWT Token，支持无状态会话与在线踢人。
- 采用 Spring `@Async`、线程池实现异步任务，提升吞吐量。
- 通过 `spring-boot-starter-aop` 与自定义注解实现业务日志、审计。

#### 适用场景

##### 适合

- 需要快速交付企业级后台（内部管理系统、OA、CRM、ERP）。
- 多租户 SaaS 平台，尤其是对数据权限要求严格的业务。
- 需要工作流、支付、短信、微信等多业务组件集成的项目。
- 初步尝试 AI 大模型、IoT 接入的原型或概念验证。

##### 不适合

- 超大规模分布式微服务架构（项目整体仍为单体，推荐使用 Spring Cloud 项目分离）。
- 对前端要求高度自定义或使用 Vue3、React 等新技术栈的团队（前端基于 Vue2）。
- 极度追求极致性能或极低资源占用的嵌入式场景（依赖 Spring 全家桶，体积较大）。

#### 学习与落地建议

##### 学习路径

1. **本地运行**：使用 `git clone` + `mvn spring-boot:run` 启动后端，配合 `npm run dev` 启动前端。
2. **阅读模块划分**：从 `yudao-framework` 入手，了解安全、事务、日志的基础实现；随后根据业务需求深入对应 `yudao‑module‑*`。
3. **动手改造**：在已有的 RBAC 基础上添加自定义角色或数据权限；尝试接入自定义 AI 接口或新增设备协议。
4. **部署实践**：学习 Docker‑Compose 或 K8s 部署脚本，尝试将 MySQL、Redis、Nacos 与项目一起容器化。

##### 落地注意

- **依赖冲突**：项目使用 `yudao-dependencies` 统一管理依赖，引入新模块时需检查 `pom.xml` 中版本是否冲突。
- **业务封装**：避免在 Controller 直接写业务逻辑，建议在 Service 层进行业务组合，确保可测试性。
- **安全审计**：默认开启 Shiro JWT，建议在生产环境配合 HTTPS、IP 白名单、登录验证码等提升安全。
- **租户隔离**：多租户字段必须在所有查询中显式使用，或通过 MyBatis‑Plus 的拦截器自动注入，防止跨租户数据泄露。
- **升级成本**：前端基于 Vue2，若未来需要迁移到 Vue3，需要较大重构，建议提前评估业务生命周期。

以上分析基于仓库结构、文档及公开代码片段，部分实现细节（如 AI 接口的内部调用方式）属推断，建议在实际项目中通过源码验证后再做决定。

---
## 学习要点

- 采用前后端分离的 Spring Boot + Vue 架构，实现模块独立开发和部署（最重要）
- 基于 Spring Security + JWT 实现无状态的身份认证和细粒度权限控制
- 完整的 RBAC 模型，支持菜单、按钮级别的权限分配与动态鉴权
- 内置代码生成器，可根据数据库表自动生成前后端 CRUD 代码，显著提升开发效率
- 集成 MyBatis-Plus，提供强大的 ORM、分页和动态 SQL 能力，简化持久层实现
- 支持动态数据源切换和多数据源事务管理，满足复杂业务场景需求

---
## 引用

- **GitHub 仓库**: [https://github.com/YunaiV/ruoyi-vue-pro](https://github.com/YunaiV/ruoyi-vue-pro)
- **DeepWiki**: [https://deepwiki.com/YunaiV/ruoyi-vue-pro](https://deepwiki.com/YunaiV/ruoyi-vue-pro)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [Java](/tags/java/) / [Vue](/tags/vue/) / [RBAC](/tags/rbac/) / [工作流](/tags/%E5%B7%A5%E4%BD%9C%E6%B5%81/) / [多租户](/tags/%E5%A4%9A%E7%A7%9F%E6%88%B7/) / [SaaS](/tags/saas/) / [AI大模型](/tags/ai%E5%A4%A7%E6%A8%A1%E5%9E%8B/) / [IoT](/tags/iot/)
- 场景： [后端开发](/scenarios/%E5%90%8E%E7%AB%AF%E5%BC%80%E5%8F%91/) / [全栈开发](/scenarios/%E5%85%A8%E6%A0%88%E5%BC%80%E5%8F%91/) / [前端开发](/scenarios/%E5%89%8D%E7%AB%AF%E5%BC%80%E5%8F%91/)

### 相关文章

- [RuoYi-Vue Pro：基于Spring Boot的多租户后台管理系统]({{< relref "posts/20260422-github_trending-yunaiv-ruoyi-vue-pro-0.md" >}})
- [RuoYi-Vue Pro：36K星的后台权限管理系统]({{< relref "posts/20260421-github_trending-yunaiv-ruoyi-vue-pro-0.md" >}})
- [🔥Vue管理后台王者！GitHub爆赞🔥极速开发神器！]({{< relref "posts/20260125-github_trending-zxwk1998-vue-admin-better-9.md" >}})
- [JeecgBoot：集成AI低代码平台与代码生成器的Java开发框架]({{< relref "posts/20260129-github_trending-jeecgboot-jeecgboot-3.md" >}})
- [软件工厂与智能体时刻]({{< relref "posts/20260208-hacker_news-software-factories-and-the-agentic-moment-3.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*