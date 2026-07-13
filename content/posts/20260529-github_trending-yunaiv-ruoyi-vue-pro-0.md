---
title: "RuoYi-Vue Pro Java后台管理系统，支持微信小程序集成"
date: 2026-05-29T03:53:47+08:00
draft: false
entry_kind: "auto"
tags: ["Java", "Spring Boot", "后台管理", "Vue", "SaaS多租户", "工作流引擎", "RBAC权限", "微服务"]
categories: ["后端", "系统与基础设施"]
source: github_trending
description: "RuoYi‑Vue‑Pro 是由 YunaiV 开发的一套开源企业级后台管理系统，基于 Spring Boot + MyBatis Plus + Vue & Element 实现，使用 Java 语言，已获约 37,373 个 star。该项目是 RuoYi‑Vue 的全新 Pro 版本，对全部功能进行优化重构并官方推"
external_url: https://github.com/YunaiV/ruoyi-vue-pro
scenarios: ["后端开发", "Web应用开发", "全栈开发"]
---

# RuoYi-Vue Pro Java后台管理系统，支持微信小程序集成

> **原名**: YunaiV /

      ruoyi-vue-pro

---

## 基本信息

- **描述**: 您好！我注意到您提供的这段文字**已经是中文**了，不需要翻译。

如果您需要我将其他**英文内容翻译成中文**，请提供相应的英文原文，我很乐意为您翻译。

---

**您提供的文本内容如下：**

> 🔥 官方推荐 🔥 RuoYi-Vue 全新 Pro 版本，优化重构所有功能。基于 Spring Boot + MyBatis Plus + Vue & Element 实现的后台管理系统 + 微信小程序，支持 RBAC 动态权限、数据权限、SaaS 多租户、Flowable 工作流、三方登录、支付、短信、商城、CRM、ERP、MES、IM、AI 大模型、IoT 物联网等功能。你的 ⭐️ Star ⭐️，是作者生发的动力！

这段文字格式和语气都很好，可以直接使用。需要我帮您做其他调整吗？
- **语言**: Java
- **星标**: 37,373 (+35 stars today)
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

RuoYi-Vue-Pro 是一个基于 Spring Boot + MyBatis Plus + Vue & Element 的企业级后台管理系统，采用前后端分离架构。它内置了 RBAC 权限管理、SaaS 多租户、Flowable 工作流等企业核心功能，并集成了支付、短信、IM 等常用服务。该项目适合需要快速搭建企业管理系统或业务中台的开发团队，覆盖了从系统管理到业务功能再到微服务治理的完整技术链路。

---
## 摘要

RuoYi‑Vue‑Pro 是由 YunaiV 开发的一套开源企业级后台管理系统，基于 Spring Boot + MyBatis Plus + Vue & Element 实现，使用 Java 语言，已获约 37,373 个 star。该项目是 RuoYi‑Vue 的全新 Pro 版本，对全部功能进行优化重构并官方推荐。系统采用模块化架构，核心特性包括 RBAC 动态权限、数据权限、SaaS 多租户、Flowable 工作流、三方登录、支付、短信、商城、CRM、ERP、MES、即时通讯、AI 大模型以及 IoT 物联网等，能够一站式支撑系统管理、流程自动化、电商、物联网与 AI 业务等企业场景。文档详细覆盖系统架构设计、核心框架、业务模块实现以及部署运维，为企业快速构建和迭代业务系统提供完整解决方案。

---
## 评论

#### 总体判断
该系统在开源社区拥有约 37k 星标，官方推荐并保持活跃更新，表明其在企业后台管理领域具备较高的认可度和社区支持。基于 Spring Boot、MyBatis Plus 与 Vue+Element 的技术栈组合，具备完整的 RBAC、数据权限、SaaS 多租户以及 Flowable 工作流等企业常用模块。因此，从技术成熟度与功能完整性来看，RuoYi‑Vue‑Pro 可作为快速构建中大型业务管理系统的首选脚手架，适合对安全性、可扩展性和多业务模块有明确需求的项目。

#### 依据与适用场景
- **事实**：GitHub 仓库使用 Java（Spring Boot）并提供完整的前后端分离源码；星标数量、文档完整度以及持续提交记录表明项目维护活跃；README 中列出的 RBAC、动态权限、数据权限、SaaS 多租户、支付、短信、商城、CRM、ERP、MES、IM、AI、IoT 等十余个业务模块，均为开源实现的常见需求。
- **推断**：由于采用微内核+插件化结构，新增业务模块通常可通过继承或覆盖已有服务快速集成，这在需求快速迭代的项目中能显著降低开发成本；Spring Security 与 MyBatis‑Plus 的组合在处理细粒度权限与复杂查询时已有大量生产案例，性能与安全风险相对可控。
- **适用场景**：需要统一后台管理、统一身份认证、跨部门数据隔离的企业内部系统；面向多租户的 SaaS 平台；业务流程较为固定、需集成 BPM（如 Flowable）的审批或工单系统；以及在已有 Spring 生态的团队中进行快速原型和交付的项目。

#### 局限与验证方式
- **局限**：项目整体采用约定优于配置的方式，某些默认实现可能不符合特定行业合规（如金融或医疗）的审计要求；随着业务模块增多，整体包体积与启动时间会上升，需要在生产环境进行性能调优；部分高级特性（如 AI 大模型、IoT）仍处于示例阶段，未经过大规模生产验证。
- **验证方式**：在正式采用前，可通过以下步骤验证系统是否满足项目需求：①拉取最新代码，检查关键模块（如 security、flowable）是否有未关闭的 issue 或安全漏洞；②在本地使用 Docker‑Compose 部署完整套件，测试启动耗时、内存占用以及基础 CRUD 响应时间；③针对数据权限和多租户场景，编写自动化测试用例验证隔离效果；④对比项目文档与实际源码，确认所需功能是否完整实现；⑤在非生产环境进行小范围业务灰度上线，观察实际运行情况与日志告警。

通过上述事实与推断的区分以及针对性验证，可在保持开发效率的同时降低因框架约束带来的潜在风险。

---
## 技术分析

#### 架构概览
##### 模块化设计
- 采用 Maven 多模块结构，主模块 `yudao-server` 包含业务实现，`yudao-framework` 提供公共组件。
- 安全、缓存、数据库等通用能力通过 `yudao-spring-boot-starter-security` 等 starter 统一封装。

##### 前后端分离
- 后端基于 Spring Boot，使用 MyBatis Plus 简化 CRUD。
- 前端使用 Vue2 + Element UI，提供统一管理界面。

#### 核心能力
##### 权限体系
- RBAC 动态角色、数据权限、菜单权限细粒度控制；通过 Spring Security + JWT 实现无状态认证。

##### 多租户 & SaaS
- 支持基于字段或库级别的租户隔离，提供租户配置、计费、计量等业务模型。

##### 工作流 & 业务流
- 集成 Flowable，实现流程设计、审批、任务分发；业务单据与流程实例关联。

##### 生态扩展
- 预置三方登录（微信、QQ 等）、支付、短信、商城、CRM、ERP、MES、IM、AI 大模型、IoT 设备接入模块。

#### 技术实现
##### 持久层
- MyBatis Plus 提供自动填充、逻辑删除、分页插件；结合 Druid 连接池提升查询效率。

##### 缓存 & 会话
- Redis 常用作 Token 存储、分布式锁、热点数据缓存；Spring Data Redis 统一封装。

##### 接口治理
- 基于 Spring MVC 的统一异常处理、参数校验（Jakarta Validation）；可选 Swagger 文档生成。

##### 第三方集成
- 支付宝/微信支付 SDK、阿里云/腾讯云短信 SDK、阿里云 OSS、微信公众号 OAuth2 等均已封装为独立模块。

#### 适用与不适用场景
##### 适用
- 中小型企业快速搭建后台管理、SaaS 平台、工作流审批系统、IoT 数据采集与展示、AI 能力接入的原型或正式产品。

##### 不适用
- 高并发实时聊天、毫秒级交易系统、跨语言异构微服务治理、需要 Service Mesh 或云原生深度定制的场景。

#### 学习与落地建议
##### 学习路径
1. 阅读根目录 `README.md` 了解整体结构。
2. 逐层阅读 `yudao-framework` 的安全 starter 源码，理解 RBAC 与 JWT 实现。
3. 通过 `yudao-server` 的业务示例（如用户、角色、菜单）快速上手。
4. 研究 Flowable 集成方式，结合流程模型器进行自定义流程。

##### 落地建议
- 初期可裁剪不需要的模块，仅保留权限、租户、工作流核心；后续按业务需求逐步引入商城、AI 等。
- 使用 Docker‑Compose 编排 MySQL、Redis、Nacos 等依赖，提升开发、测试、部署一致性。
- 在正式项目中对安全、接口幂等、事务隔离进行专项加固，避免直接使用默认配置。

---
## 学习要点

- 采用前后端分离架构，前端基于 Vue3 + Vite，后端基于 Spring Boot，实现高效协同开发和部署。
- 实现基于 RBAC 的细粒度权限控制，支持页面、按钮、数据列级别的权限管理。
- 内置代码生成器，支持前后端代码一键生成，显著提升开发效率。
- 集成 Swagger/Knife4j 自动生成 API 文档，便于接口管理和前后端对接。
- 使用 MyBatis-Plus 简化持久层，提供分页、逻辑删除等常用功能，降低数据库操作复杂度。
- 前端采用 Element Plus UI 组件库，提供丰富的业务组件和响应式布局，开箱即用。
- 项目结构清晰，模块化分层（common、system、generator 等），便于团队协作和后期维护。

---
## 引用

- **GitHub 仓库**: [https://github.com/YunaiV/ruoyi-vue-pro](https://github.com/YunaiV/ruoyi-vue-pro)
- **DeepWiki**: [https://deepwiki.com/YunaiV/ruoyi-vue-pro](https://deepwiki.com/YunaiV/ruoyi-vue-pro)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [后端](/categories/%E5%90%8E%E7%AB%AF/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [Java](/tags/java/) / [Spring Boot](/tags/spring-boot/) / [后台管理](/tags/%E5%90%8E%E5%8F%B0%E7%AE%A1%E7%90%86/) / [Vue](/tags/vue/) / [SaaS多租户](/tags/saas%E5%A4%9A%E7%A7%9F%E6%88%B7/) / [工作流引擎](/tags/%E5%B7%A5%E4%BD%9C%E6%B5%81%E5%BC%95%E6%93%8E/) / [RBAC权限](/tags/rbac%E6%9D%83%E9%99%90/) / [微服务](/tags/%E5%BE%AE%E6%9C%8D%E5%8A%A1/)
- 场景： [后端开发](/scenarios/%E5%90%8E%E7%AB%AF%E5%BC%80%E5%8F%91/) / [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/) / [全栈开发](/scenarios/%E5%85%A8%E6%A0%88%E5%BC%80%E5%8F%91/)

### 相关文章

- [RuoYi-Vue Pro：36K星的后台权限管理系统]({{< relref "posts/20260421-github_trending-yunaiv-ruoyi-vue-pro-0.md" >}})
- [RuoYi-Vue Pro：基于Spring Boot的多租户后台管理系统]({{< relref "posts/20260422-github_trending-yunaiv-ruoyi-vue-pro-0.md" >}})
- [ruoyi-vue-pro Java后台管理系统企业级解决方案]({{< relref "posts/20260528-github_trending-yunaiv-ruoyi-vue-pro-0.md" >}})
- [RuoYi-Vue-Pro：Spring Boot + Vue3 企业级后台管理系统]({{< relref "posts/20260522-github_trending-yunaiv-ruoyi-vue-pro-0.md" >}})
- [JeecgBoot：集成AI低代码平台与代码生成器的Java开发框架]({{< relref "posts/20260129-github_trending-jeecgboot-jeecgboot-3.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*