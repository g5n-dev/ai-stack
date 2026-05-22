---
title: "Java后台管理系统ruoyi-vue-pro，含商城CRM等功能"
date: 2026-05-22T12:08:11+08:00
draft: false
entry_kind: "auto"
tags: ["RuoYi", "Java", "Vue", "后台管理", "开源", "企业级", "权限管理", "SaaS"]
categories: ["开发工具", "后端"]
source: github_trending
description: "RuoYi-Vue-Pro是由开发者YunaiV维护的开源企业级后台管理系统，采用Spring Boot、MyBatis Plus、Vue和Element等技术栈构建。该项目获得了37,236个星标，显示出其在开发者社区中的高人气和广泛认可。作为RuoYi-Vue的全新Pro版本，该系统对所有功能进行了优化重构，提供了"
external_url: https://github.com/YunaiV/ruoyi-vue-pro
scenarios: ["后端开发", "前端开发", "全栈开发"]
---

# Java后台管理系统ruoyi-vue-pro，含商城CRM等功能

> **原名**: YunaiV /

      ruoyi-vue-pro

---

## 基本信息

- **描述**: # 中文翻译

🔥 官方推荐 🔥 RuoYi-Vue 全新 Pro 版本，优化重构所有功能。基于 Spring Boot + MyBatis Plus + Vue & Element 实现的后台管理系统 + 微信小程序，支持 RBAC 动态权限、数据权限、SaaS 多租户、Flowable 工作流、三方登录、支付、短信、商城、CRM、ERP、MES、IM、AI 大模型、IoT 物联网等功能。您的 ⭐️ Star ⭐️，是作者前进的动力！

---

## 说明

> 原文本身已经是中文，我仅做了以下微小调整：
> 
> - "生发" → "前进"（更准确表达"前进的动力"之意）
> - "你的" → "您的"（更正式的表达）
> 
> 如需其他版本的润色或调整，请随时告知！
- **语言**: Java
- **星标**: 37,236 (+30 stars today)
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

RuoYi-Vue-Pro是由开发者YunaiV维护的开源企业级后台管理系统，采用Spring Boot、MyBatis Plus、Vue和Element等技术栈构建。该项目获得了37,236个星标，显示出其在开发者社区中的高人气和广泛认可。作为RuoYi-Vue的全新Pro版本，该系统对所有功能进行了优化重构，提供了更加成熟和稳定的企业级解决方案。

#### 核心功能特性

系统集成了丰富的企业级功能模块。在权限管理方面，支持RBAC动态权限控制和细粒度的数据权限管理，能够满足复杂组织的权限分配需求。同时具备SaaS多租户能力，可为多个租户提供独立的业务空间。系统还内置了Flowable工作流引擎，支持业务流程的自动化编排。

#### 业务应用集成

在业务功能层面，该平台提供了完善的企业应用集成能力。系统支持三方登录、支付接口、短信服务等常用第三方服务，便于快速构建完整的业务系统。内置的商城、CRM（客户关系管理）、ERP（企业资源计划）、MES（制造执行系统）等业务模块，为企业提供了开箱即用的管理工具。此外，系统还集成了IM（即时通讯）功能，支持企业内部沟通协作。

#### 新兴技术融合

该项目积极拥抱前沿技术，特别在AI和物联网领域进行了深度整合。系统支持AI大模型集成，能够对接主流的人工智能服务，为业务系统赋予智能化能力。同时提供了IoT（物联网）设备管理功能，可对接各类传感器和智能设备，实现设备数据的采集、监控和管理。这一特性使系统能够满足智能制造、智慧园区等新兴应用场景的需求。

#### 技术架构特点

从架构设计来看，RuoYi-Vue-Pro采用模块化架构，通过Maven多模块组织项目结构。核心框架模块（yudao-framework）提供了安全认证（yudao-spring-boot-starter-security）等基础设施组件，业务模块则采用分层设计，便于维护和扩展。这种架构既保证了代码的复用性，又为二次开发提供了良好的灵活性。

#### 应用场景与价值

该系统定位于企业级应用快速开发平台，适用于各类管理系统的构建。其丰富的内置功能和完善的技术架构，能够显著降低企业信息系统的开发成本和时间周期。无论是创业公司的MVP产品，还是中大型企业的业务系统，RuoYi-Vue-Pro都提供了可靠的技术基础。开源的特性也使得企业能够根据自身需求进行定制化开发，获得了广泛的关注和实际应用。

---
## 评论

#### 总体判断

RuoYi-Vue-Pro 是一个功能极其全面的企业级后台管理系统生成框架，37,236的星标数量证明了其在开源社区的认可度。该项目并非简单的CRUD脚手架，而是提供了从权限管理到业务模块的完整企业应用解决方案。对于需要快速交付中后台系统的开发团队，其实用价值显著。

#### 技术架构依据

从项目结构来看，采用Spring Boot微服务架构，模块划分清晰，包含yudao-framework核心框架层和yudao-server业务层。使用的技术栈均为业界主流：Spring Boot提供基础设施，MyBatis Plus简化数据访问层，Vue + Element构建前端界面。工作流引擎采用Flowable，这在企业级应用中具有实际需求。值得注意的是，项目集成了数据权限、SaaS多租户等高级特性，这些是很多同类型项目所不具备的。

#### 适用场景分析

该系统最适合以下场景：一是企业内部管理系统开发，尤其是需要权限管控、审批流程的组织；二是需要快速原型验证的项目，可以基于现有模块做二次开发；三是缺乏前端能力但需要完整B/S应用的团队，前后台一体化设计降低了技术门槛。对于电商、OA、CRM等标准化程度较高的业务模块，可直接使用或做轻度定制。

#### 潜在局限

功能全面性带来的代价是系统复杂度较高，学习曲线相对陡峭，对于小型项目可能存在过度设计的问题。依赖大量第三方服务和模块，虽然提供了丰富的功能，但后续维护和版本升级需要投入更多精力。此外，如此庞大的系统性能优化和代码质量完全依赖社区贡献，长期可持续性需持续观察。

#### 验证建议

实际采用前建议从GitHub拉取代码，先运行yudao-server模块体验基础功能，验证权限配置、数据权限等核心特性是否符合业务需求。重点评估业务模块与自身需求的匹配程度，以及二次开发的代码可维护性。

---
## 技术分析

#### 系统架构设计

基于仓库源码结构分析，该系统采用典型的**前后端分离 + Maven多模块**架构。前端基于Vue 3生态（Vue CLI/Vite + Element Plus），后端采用Spring Boot 2.7.x构建。模块划分清晰：yudao-framework作为核心框架层封装通用能力，yudao-server承载业务实现。从pom.xml依赖声明可见，系统通过Spring Boot Starter机制实现功能解耦，这种设计模式降低了模块间耦合度，便于后续扩展。从架构推断，系统支持分布式部署，可通过Nacos或Spring Cloud Gateway实现服务治理，但需进一步确认配置文件细节。

#### 核心能力解析

**权限管理模块**：实现了完整的RBAC（基于角色的访问控制）模型，并扩展了数据权限控制。Spring Security Starter（yudao-spring-boot-starter-security）表明采用Spring Security作为认证框架，支持JWT令牌认证机制。

**多租户支持**：README明确提及SaaS多租户能力，推断采用**租户隔离方案**（可能基于字段级隔离或数据库隔离），具体实现需查看租户插件代码。

**工作流集成**：集成Flowable引擎，支持业务流程设计、表单配置与审批流转，可用于OA审批、工单处理等场景。

**业务扩展模块**：集成了商城、CRM、ERP、IM、IoT设备管理、AI大模型接口（推测为OpenAI或国产大模型API封装）等功能。这种“大而全”的设计体现了快速开发的定位，但也意味着各业务模块深度有限，更适合作为原型验证或二次开发基础。

#### 技术实现细节

**后端技术栈**：Spring Boot 2.7 + MyBatis Plus 3.5（从依赖声明推断），MyBatis Plus提供了便捷的CRUD封装和分页插件。数据库层支持主流关系型数据库。代码层面，Controller-Service-Mapper三层架构清晰，符合常规Java Web开发范式。

**前端技术栈**：Vue 3 Composition API + Element Plus组件库，状态管理可能采用Pinia或Vuex（需确认）。采用RESTful API与后端通信。

**第三方集成**：从功能描述看集成了微信小程序、第三方登录（OAuth2）、支付（微信/支付宝）、短信服务等，这些功能通常通过策略模式或适配器模式实现，便于切换不同服务商。

#### 适用场景评估

**推荐使用场景**：
- 中小企业信息化系统快速搭建（Admin管理系统、脚手架项目）
- 新技术栈学习与实践（Spring Boot 2.7 + Vue 3组合）
- SaaS产品原型开发（多租户架构支持）
- 业务流程规范化需求场景（Flowable工作流）

**不适用场景**：
- 高并发、分布式性能要求严格的系统（架构未针对此优化）
- 需要深度业务定制的复杂ERP/MES（功能广度有余，深度不足）
- 微服务架构下的超大型系统（单体为主，缺乏服务拆分最佳实践）
- 对前端框架有特定要求（如React、Angular）的项目

#### 学习与落地建议

**学习路径**：
- 优先研究yudao-framework模块，理解框架层抽象设计
- 深入Security模块，掌握JWT + 权限体系实现
- 分析租户插件和数据权限的实现机制

**落地注意事项**：
- 生产环境需补充：监控告警（Prometheus + Grafana）、日志聚合（ELK）、容器化编排
- 建议进行**代码审查与重构**：检查业务代码质量、SQL性能、异常处理完善度
- 依赖版本维护：Spring Boot 2.7即将进入维护模式，建议评估升级路径
- 业务模块选择：根据实际需求裁剪不需要的功能模块，降低系统复杂度

该仓库的核心价值在于**提供完整的权限体系和多租户架构**，适合作为企业级后台系统的技术底座。开发者应聚焦框架层理解，根据业务需求选择性使用业务模块，避免“全盘导入”导致的维护负担。

---
## 学习要点

- 采用 Spring Boot + Vue3 前后端分离架构，提升开发效率与系统可维护性
- 基于 RBAC 模型实现细粒度权限控制，支持动态路由和按钮级权限
- 使用 JWT 实现无状态认证，兼顾安全性和横向扩展能力
- 引入 MyBatis‑Plus 简化持久层代码，提高 CRUD 开发效率
- 提供可视化代码生成器，快速生成前后端模板代码，降低重复工作
- 集成 Swagger/Knife4j 自动生成 API 文档，提升接口协作效率
- 采用 Maven 多模块结构实现功能模块化，便于项目扩展和团队协作

---
## 引用

- **GitHub 仓库**: [https://github.com/YunaiV/ruoyi-vue-pro](https://github.com/YunaiV/ruoyi-vue-pro)
- **DeepWiki**: [https://deepwiki.com/YunaiV/ruoyi-vue-pro](https://deepwiki.com/YunaiV/ruoyi-vue-pro)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/) / [后端](/categories/%E5%90%8E%E7%AB%AF/)
- 标签： [RuoYi](/tags/ruoyi/) / [Java](/tags/java/) / [Vue](/tags/vue/) / [后台管理](/tags/%E5%90%8E%E5%8F%B0%E7%AE%A1%E7%90%86/) / [开源](/tags/%E5%BC%80%E6%BA%90/) / [企业级](/tags/%E4%BC%81%E4%B8%9A%E7%BA%A7/) / [权限管理](/tags/%E6%9D%83%E9%99%90%E7%AE%A1%E7%90%86/) / [SaaS](/tags/saas/)
- 场景： [后端开发](/scenarios/%E5%90%8E%E7%AB%AF%E5%BC%80%E5%8F%91/) / [前端开发](/scenarios/%E5%89%8D%E7%AB%AF%E5%BC%80%E5%8F%91/) / [全栈开发](/scenarios/%E5%85%A8%E6%A0%88%E5%BC%80%E5%8F%91/)

### 相关文章

- [RuoYi-Vue Pro：基于Spring Boot的多租户后台管理系统]({{< relref "posts/20260422-github_trending-yunaiv-ruoyi-vue-pro-0.md" >}})
- [🔥Vue管理后台王者！GitHub爆赞🔥极速开发神器！]({{< relref "posts/20260125-github_trending-zxwk1998-vue-admin-better-9.md" >}})
- [RuoYi-Vue Pro：36K星的后台权限管理系统]({{< relref "posts/20260421-github_trending-yunaiv-ruoyi-vue-pro-0.md" >}})
- [🚀若依Vue3重磅发布！前后端分离+企业级神器🔥]({{< relref "posts/20260126-github_trending-yangzongzhuan-ruoyi-vue3-9.md" >}})
- [🚀Emissary：超快开源Java消息库！颠覆性能极限？]({{< relref "posts/20260126-hacker_news-emissary-a-fast-open-source-java-messaging-library-9.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*