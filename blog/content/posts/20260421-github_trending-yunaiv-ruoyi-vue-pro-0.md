---
title: RuoYi-Vue Pro：基于Spring Boot的多租户后台管理系统
date: 2026-04-21 17:17:43+08:00
draft: false
entry_kind: auto
tags:
- Spring Boot
- 后台管理
- 多租户
- RBAC权限
- Vue
- 工作流
- SaaS
- 企业级
categories:
- 系统与基础设施
- 开源生态
source: github_trending
description: 项目概述 RuoYi‑Vue‑Pro 是由 YunaiV 开发的开源企业级管理平台，采用 Spring Boot + MyBatis Plus
  + Vue & Element 搭建。官方推荐，Star 已超过 36,666（今日+35），主要使用 Java 编写。 核心特性 - **权限体系**：RBAC
  动态权限、数
external_url: https://github.com/YunaiV/ruoyi-vue-pro
scenarios:
- 后端开发
- 全栈开发
- Web应用开发
aliases:
- /posts/20260422-github_trending-yunaiv-ruoyi-vue-pro-0/
- /posts/20260522-github_trending-yunaiv-ruoyi-vue-pro-0/
- /posts/20260528-github_trending-yunaiv-ruoyi-vue-pro-0/
- /posts/20260529-github_trending-yunaiv-ruoyi-vue-pro-0/
- /posts/20260530-github_trending-yunaiv-ruoyi-vue-pro-0/
content_mode: legacy_analysis
publication_tier: LEGACY
source_provenance: legacy_no_snapshot
source_support: 0.0
---

# RuoYi-Vue Pro：基于Spring Boot的多租户后台管理系统

> **原名**: YunaiV /

      ruoyi-vue-pro

---

## 基本信息

- **描述**: 这段内容本身就是中文的，不需要翻译。😊

不过，我注意到原文可能是想表达英文版本或者需要润色。我来提供几种优化版本供您参考：

---

**版本一（保持原语气，略微润色）：**

> 🔥 官方推荐 🔥 RuoYi-Vue 全新 Pro 版本，全面优化重构所有功能。基于 Spring Boot + MyBatis Plus + Vue & Element 实现的后台管理系统 + 微信小程序，支持 RBAC 动态权限、数据权限、SaaS 多租户、Flowable 工作流、三方登录、支付、短信、商城、CRM、ERP、MES、IM、AI 大模型、IoT 物联网等功能。您的 ⭐️ Star ⭐️，是作者前进的动力！

**版本二（更正式商务风格）：**

> 🔥 官方推荐 🔥 RuoYi-Vue Pro 全新发布，全面重构升级。基于 Spring Boot + MyBatis Plus + Vue & Element 的后台管理系统及微信小程序解决方案，具备 RBAC 动态权限、数据权限、SaaS 多租户、Flowable 工作流、三方登录、支付、短信、商城、CRM、ERP、MES、IM、AI 大模型、IoT 物联网等丰富功能。期待您的 ⭐️ Star ⭐️ 支持！

---

请问您是需要润色中文内容，还是有其他语言的原文需要翻译？
- **语言**: Java
- **星标**: 36,666 (+35 stars today)
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

ruoyi-vue-pro 是基于 Spring Boot + MyBatis Plus + Vue & Element 构建的后台管理系统，提供微信小程序支持。内置 RBAC 动态权限、数据权限、SaaS 多租户、Flowable 工作流等模块，适合需要快速搭建后台管理系统的团队。项目还集成了商城、CRM、ERP、IM、AI 大模型、IoT 等扩展功能。

---
## 摘要

#### 项目概述
RuoYi‑Vue‑Pro 是由 YunaiV 开发的开源企业级管理平台，采用 Spring Boot + MyBatis Plus + Vue & Element 搭建。官方推荐，Star 已超过 36,666（今日+35），主要使用 Java 编写。

#### 核心特性
- **权限体系**：RBAC 动态权限、数据权限，支持细粒度控制。
- **多租户**：SaaS 模式下实现租户隔离。
- **工作流**：集成 Flowable，提供业务流程编排。
- **第三方能力**：支持三方登录、支付、短信、邮件等集成。
- **业务场景**：内置电商、CRM、ERP、MES、即时通讯、AI 大模型、物联网等完整业务模块。
- **扩展性**：模块化设计，便于按需拆分或组合。

#### 技术栈
- 后端：Spring Boot、MyBatis‑Plus、Spring Security、Flowable、Redis、RabbitMQ 等。
- 前端：Vue.js、Element UI、axios、Vite。
- 数据库：兼容 MySQL、PostgreSQL 等主流关系型数据库。

#### 架构与文档
项目采用分层+插件化的架构，包含核心框架（yudao‑framework）和业务模块（yudao‑server），各模块均有独立的 pom.xml，便于依赖管理和持续集成。官方提供详细的系统架构、模块划分、部署运维等文档，支持快速二次开发。

#### 总结
RuoYi‑Vue‑Pro 通过“一站式”方案帮助企业快速构建后台管理、商城、CRM、ERP、IoT、AI 等业务系统，兼具高可扩展性与丰富的企业级功能，是开发者首选的开源项目之一。

---
## 评论

这是一套功能覆盖极广的企业级后台管理框架，适合需要快速落地后台系统的团队选用。其技术栈为常见的Spring Boot + MyBatis Plus + Vue生态，RBAC、数据权限、SaaS多租户、工作流等模块均为开箱即用，开发团队无需从零搭建权限体系或租户隔离逻辑，可显著缩短项目启动周期。

#### 依据

从项目结构和依赖声明来看，框架采用多模块Maven工程组织，yudao-framework封装了安全认证、数据权限等通用能力，yudao-server承载业务实现。这种分层方式符合企业级应用的常见实践，便于后期在通用层统一升级。官方声称支持支付、短信、商城、CRM、IoT等场景，说明其业务模型较为抽象，实际落地仍需根据具体业务进行定制。星标数36,666反映了较高的社区关注度，间接说明项目在开源社区中有一定认可度，但星标数量不代表代码质量或生产适用性。

#### 适用场景

- 内部管理系统快速搭建，如OA、CRM、ERP的原型或初期版本
- 需要RBAC或数据权限管理的多角色业务系统
- SaaS化产品的基础框架，支持租户隔离
- 工作流驱动型业务，如审批流、工单系统
- 团队希望以单体形式先行交付，后期再考虑微服务拆分

#### 局限与风险

需要注意的是，框架功能丰富也意味着一定的学习成本和定制复杂度。对于功能简单的轻量级应用，引入整套框架可能导致过度设计。此外，模块之间的耦合度需在使用前评估，若后期需要替换某个核心组件（如安全框架或ORM层），迁移成本可能较高。官方集成了大量第三方服务（支付、短信、AI等），实际项目中未必全部用到，按需裁剪需要一定经验。

#### 验证方式

建议从GitHub拉取源码，查看关键模块的单元测试覆盖率和代码注释完整度；在本地运行示例项目，观察启动速度和基础功能响应；结合团队现有技术栈评估集成难度；最后以真实业务场景进行一次端到端的原型验证，确认框架的扩展点是否满足预期需求。

---
## 技术分析

#### 系统架构与模块组织

##### 多层模块化架构
项目采用Maven多模块设计，将依赖管理、框架封装和业务实现分离。yudao-dependencies统一管理版本号，确保各模块依赖一致性。yudao-framework层封装安全认证、数据权限、通用工具等基础能力，业务层仅需关注具体功能实现。这种分层方式降低了模块间耦合度，便于团队协作和功能复用。

##### 前后端分离架构
前端基于Vue生态构建，配合Element Plus组件库提供现代化管理界面。通过API与后端交互，实现前后端独立部署和迭代。

#### 核心能力分析

##### 权限管理体系
系统实现了RBAC动态权限控制和细粒度数据权限管理。动态权限允许在运行时调整用户角色和菜单权限，数据权限可控制用户可见数据范围。从安全模块的独立封装（yudao-spring-boot-starter-security）来看，权限逻辑采用了Spring Security框架进行统一认证授权。

##### 多租户与业务模块
SaaS多租户支持使单个实例可服务多个客户。内置商城、CRM、ERP、MES等功能模块表明该项目面向企业全场景应用，工作流引擎支持业务流程自动化。

##### 新兴技术集成
集成了IM即时通讯、AI大模型交互和IoT设备管理等功能，反映了项目对数字化转型需求的覆盖。

#### 技术实现特点

后端采用Spring Boot作为主框架，结合MyBatis Plus简化持久层开发。pom.xml中的模块划分体现了清晰的技术分层思想。从依赖结构推断，系统使用JWT或Session方式进行身份认证，数据库操作主要依赖MyBatis Plus的CRUD增强功能。

#### 适用场景

适合需要快速搭建企业级后台管理系统的团队，尤其是涉及权限管理、多租户运营和业务流程自动化的场景。技术栈在国内企业应用开发中普及度高，学习曲线相对平缓。36,666星标数量表明项目具有较好的社区活跃度和参考价值。

#### 不适用场景

对于追求极致性能、需要在高并发场景下水平扩展的系统，当前单体为主的设计可能需要重构。对于需要完全自控架构、技术选型受限的企业，直接采用可能带来过度定制化成本。

#### 学习与落地建议

学习路径建议从项目目录结构和README文档入手，理解模块划分和依赖关系后，重点研究权限模块和业务模块的代码实现。落地时需评估团队对Spring Boot和Vue的技术储备，定制开发应遵循模块边界进行扩展，避免直接修改核心框架代码。

---
## 学习要点

- 基于 Vue 3 + Vite 的前端脚手架，提供高效的组件化开发体验
- 前后端分离的微服务架构，支持 Spring Boot 与 Spring Cloud 生态
- 采用 JWT + RBAC 实现细粒度权限控制和动态路由
- 内置代码生成器与 MyBatis‑Plus 自动化 CRUD，显著提升开发效率
- 集成 Swagger/Knife4j 统一 API 文档与全局异常处理机制
- 支持 Docker Compose 一键部署及 CI/CD 流水线集成
- 提供完整的日志、监控与审计功能，实现系统可观测性

---
## 引用

- **GitHub 仓库**: [https://github.com/YunaiV/ruoyi-vue-pro](https://github.com/YunaiV/ruoyi-vue-pro)
- **DeepWiki**: [https://deepwiki.com/YunaiV/ruoyi-vue-pro](https://deepwiki.com/YunaiV/ruoyi-vue-pro)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Spring Boot](/tags/spring-boot/) / [后台管理](/tags/%E5%90%8E%E5%8F%B0%E7%AE%A1%E7%90%86/) / [多租户](/tags/%E5%A4%9A%E7%A7%9F%E6%88%B7/) / [RBAC权限](/tags/rbac%E6%9D%83%E9%99%90/) / [Vue](/tags/vue/) / [工作流](/tags/%E5%B7%A5%E4%BD%9C%E6%B5%81/) / [SaaS](/tags/saas/) / [企业级](/tags/%E4%BC%81%E4%B8%9A%E7%BA%A7/)
- 场景： [后端开发](/scenarios/%E5%90%8E%E7%AB%AF%E5%BC%80%E5%8F%91/) / [全栈开发](/scenarios/%E5%85%A8%E6%A0%88%E5%BC%80%E5%8F%91/) / [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [RuoYi-Vue Pro：36K星的后台权限管理系统]({{< relref "posts/20260421-github_trending-yunaiv-ruoyi-vue-pro-0.md" >}})
- [🔥Vue管理后台王者！GitHub爆赞🔥极速开发神器！]({{< relref "posts/20260125-github_trending-zxwk1998-vue-admin-better-9.md" >}})
- [JeecgBoot开源低代码平台：集成AI应用与代码生成器]({{< relref "posts/20260129-github_trending-jeecgboot-jeecgboot-7.md" >}})
- [JeecgBoot：集成AI低代码与代码生成器的企业级开发平台]({{< relref "posts/20260129-github_trending-jeecgboot-jeecgboot-7.md" >}})
- [JeecgBoot：集成AI低代码与代码生成器的企业级开发平台]({{< relref "posts/20260129-github_trending-jeecgboot-jeecgboot-7.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*
