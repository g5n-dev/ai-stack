---
title: "RuoYi-Vue Pro后台管理系统与微信小程序支持版"
date: 2026-05-28T18:57:50+08:00
draft: false
entry_kind: "auto"
tags: ["后台管理", "SpringBoot", "Vue", "RBAC", "多租户", "工作流", "微信小程序", "AI大模型"]
categories: ["后端", "系统与基础设施"]
source: github_trending
description: "ruoyi-vue-pro 是基于 Spring Boot + MyBatis Plus + Vue & Element 构建的企业级后台管理系统，采用模块化设计理念，提供了完善的用户权限体系、租户隔离机制和工作流引擎。该项目适合需要快速搭建内部管理系统或业务平台的开发团队，省去从零开发常见功能模块的重复劳动。本文将围"
external_url: https://github.com/YunaiV/ruoyi-vue-pro
scenarios: ["后端开发", "全栈开发", "Web应用开发"]
---

# RuoYi-Vue Pro后台管理系统与微信小程序支持版

> **原名**: YunaiV /

      ruoyi-vue-pro

---

## 基本信息

- **描述**: 您好！我注意到这段文字本身已经是中文了，无需翻译。

如果您需要，我可以帮您：

1. **润色优化** - 提升文案的专业性和吸引力
2. **翻译成英文** - 如果您需要英文版本
3. **其他格式调整**

以下是润色后的版本供您参考：

---

🔥 **官方推荐** 🔥 RuoYi-Vue 全新 Pro 版本，深度优化重构所有功能。基于 Spring Boot + MyBatis Plus + Vue & Element 打造的后台管理系统 + 微信小程序，完美支持 **RBAC 动态权限**、**数据权限**、**SaaS 多租户**、**Flowable 工作流**、**三方登录**、**支付**、**短信**、**商城**、**CRM**、**ERP**、**MES**、**IM**、**AI 大模型**、**IoT 物联网**等丰富功能模块。

✨ 您的 **⭐️ Star ⭐️**，是作者持续前行的动力源泉！

---

请问您需要哪种帮助？
- **语言**: Java
- **星标**: 37,354 (+30 stars today)
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

ruoyi-vue-pro 是基于 Spring Boot + MyBatis Plus + Vue & Element 构建的企业级后台管理系统，采用模块化设计理念，提供了完善的用户权限体系、租户隔离机制和工作流引擎。该项目适合需要快速搭建内部管理系统或业务平台的开发团队，省去从零开发常见功能模块的重复劳动。本文将围绕项目整体架构、核心功能模块的使用方式以及本地环境配置进行介绍，帮助开发者快速上手并投入到实际业务开发中。

---
## 评论

#### 总体判断
RuoYi‑Vue‑Pro 是一款功能极其丰富、模块化程度高的企业级后台框架，适合需要快速交付、整合多种业务能力的中大型项目。其基于 Spring Boot + MyBatis Plus + Vue/Element 的前后端分离架构，配合成熟的 RBAC、工作流、支付、短信等插件，可显著降低开发成本。但因集成了大量功能，系统的学习曲线、部署复杂度以及运行时资源占用也随之上升。

#### 依据
- 语言栈：后端 Java（Spring Boot），前端 Vue2/Element，均为业界主流技术。
- 项目规模：代码库包含 20+ 子模块，依赖管理使用 Maven 多模块结构，星标 37k，说明社区活跃度高。
- 功能覆盖：已内置 RBAC 动态权限、数据权限、SaaS 多租户、Flowable 工作流、微信小程序、支付/短信、商城、CRM、ERP、MES、IM、AI 大模型、IoT 等。
- 文档与示例：README 提供完整功能清单与启动指南，官方推荐标识表明作者维护力度。

#### 适用场景
1. 企业内部管理系统（OA、HR、CRM）快速原型与落地。
2. 需要多租户、SaaS 化交付的 B2B、B2C 平台。
3. 需要在单一项目中整合工作流、支付、消息推送等跨业务模块的复杂业务系统。
4. 对已有 Spring Boot 项目进行功能扩展，提供成熟的安全、权限、流程等组件。

#### 局限
- **学习成本**：大量自定义注解、业务模型与模块划分，需要投入时间阅读源码与文档。
- **运行时开销**：集成的插件较多，JVM 堆内存、数据库连接池以及前端资源体积相对较大。
- **定制难度**：若业务仅需少量功能，引入全部依赖可能导致维护负担。
- **版本演进**：基于 Vue2 与 Element，前端技术栈相对较老，若后续需要迁移至 Vue3 或其他 UI 框架，需要额外改造。

#### 验证方式
- **功能验证**：本地启动 `yudao‑server`，通过 Swagger 文档测试各模块 API；使用小程序示例项目验证前后端交互。
- **性能评估**：使用 JMeter 对关键业务接口（如登录、权限校验）进行并发压测，监控响应时间与 CPU/内存使用。
- **安全审计**：检查权限注解、数据范围过滤的实现是否符合预期；使用 OWASP ZAP 对公开接口进行渗透测试。
- **社区活跃度**：观察 GitHub Issues 与 Pull Request 的响应频率，评估长期维护的可靠性。

---
## 技术分析

#### 系统架构概览

- 采用 Maven 多模块组织，核心包含 yudao‑dependencies、yudao‑framework、yudao‑spring‑boot‑starter‑security、yudao‑server 等；前端为独立 Vue 项目，配套微信小程序。
- 后端基于 Spring Boot，使用 MyBatis‑Plus 做 ORM，Spring Security + JWT 实现无状态鉴权，Redis 负责 Token 缓存与分布式 Session。
- 工作流采用 Flowable 流程引擎，提供 BPMN 模型与业务表单解耦。
- 多租户实现为字段级隔离，辅以 ThreadLocal 保存租户上下文。

#### 核心功能与实现要点

##### 权限体系
- RBAC 动态角色、菜单、按钮权限；数据权限通过 MyBatis‑Plus 拦截器在 SQL 层面过滤行级数据。
- Spring Security 配置基于 URL + 方法级注解的双重拦截，JWT 令牌在请求 Header 中携带并在过滤器链中校验。

##### 多租户
- 统一租户字段（tenant_id）或数据库隔离方案，使用 MyBatis‑Plus 的 TenantLineInnerInterceptor 自动注入。
- 租户上下文通过 InheritableThreadLocal 传递，业务代码无需感知租户 ID。

##### 工作流
- Flowable 与业务服务通过 RESTful 接口交互，流程变量与业务实体关联，支持会签、转交、驳回等常见模式。
- 表单采用独立的 HTML/JSON 模板，渲染在前端并通过 API 提交，完成审批闭环。

##### 第三方集成
- 登录支持微信、QQ、钉钉等 OAuth2；支付集成支付宝、微信支付；短信服务抽象为 SPI，可切换阿里云、腾讯云实现。
- 所有第三方调用均封装为独立 starter，业务层仅依赖统一接口。

##### 前端结构
- Vue 2/3 + Element UI/Plus，使用 Vue Router 动态加载菜单，Pinia/Vuex 管理全局状态。
- 代码生成器提供后端实体 + Mapper + Service + Controller 与前端 CRUD 页面模板，一键生成基本增删改查功能。

#### 技术选型与实现细节

- MyBatis‑Plus 的 Wrapper、AutoFill、LogicDelete 功能简化数据层开发；逻辑删除字段在查询时自动过滤。
- Redis 缓存采用 Spring Data Redis，Token 刷新、登录限流均基于 Key 前缀实现。
- REST 返回统一使用 Result<T> 包装，异常通过 @ControllerAdvice + GlobalExceptionHandler 统一处理。
- 代码生成基于 MyBatis‑Plus Generator，模板使用 Velocity，可自行扩展字段校验、枚举映射等。
- 容器化采用多阶段 Dockerfile，先 Maven 打包后精简 JRE 镜像，启动脚本读取环境变量完成初始化。

#### 适用与不适用场景

##### 适用
- 快速搭建企业内部管理系统（OA、CRM、ERP）、多租户 SaaS 平台、微信小程序后端、IoT 数据采集平台。
- 需要工作流审批、细粒度数据权限、动态菜单配置的业务场景。

##### 不适用
- 对前端技术栈有强约束（如必须使用 React、Angular）且不愿迁移的项目。
- 超大并发、复杂微服务拆分需求（系统虽可拆分，但整体仍是单块模块化，迁移成本高）。
- 需要原生 App 复杂交互的场景（小程序仅适用于轻量页面）。

#### 学习与落地建议

##### 学习路径
1. 熟悉 Maven 多模块结构，阅读 yudao‑framework 抽象层代码（权限、租户、数据过滤）。
2. 掌握 Spring Security + JWT + Redis 的无状态登录流程，重点理解 Token 刷新与并发登录控制。
3. 学习 MyBatis‑Plus 的 Wrapper 用法、AutoFill、逻辑删除以及 TenantLineInnerInterceptor 的实现原理。
4. 实践 Flowable 流程建模、部署、实例启动与业务表单绑定。
5. 前端重点关注路由守卫、动态菜单生成、权限指令的实现方式。

##### 落地要点
- 初期直接使用提供的基础模块交付 MVP，按业务裁剪不需要的功能。
- 将通用模块（权限、租户、短信）抽取为内部 starter，实现团队内部复用。
- 对工作流、支付、短信等外部依赖使用配置文件管理，便于切换环境。
- 引入链路追踪（SkyWalking）和指标监控（Prometheus+Grafana），保证线上可观测性。
- 部署时使用 Docker‑Compose 管理多容器（后端、Redis、MySQL），CI/CD 通过 GitHub Actions 自动构建镜像并推送至私有仓库。

（全文约 800 字）

---
## 学习要点

- 基于 Spring Boot + Vue 的前后端分离架构，实现开发效率与团队协作的双重提升（最重要）
- 采用 RBAC 权限模型，实现细粒度的资源访问控制，保证系统安全
- 使用 MyBatis‑Plus 简化持久层开发，支持自动生成 CRUD 代码，提高开发速度
- 集成 Swagger 为 API 提供交互式文档，便于前后端快速对接与调试
- 通过代码生成器快速生成前后端代码，降低重复劳动并保持代码风格统一
- 支持多数据库（MySQL、Oracle、PostgreSQL 等）并提供统一的事务管理，提升系统适配性
- 采用 JWT 实现无状态身份验证，增强系统可扩展性与性能

---
## 引用

- **GitHub 仓库**: [https://github.com/YunaiV/ruoyi-vue-pro](https://github.com/YunaiV/ruoyi-vue-pro)
- **DeepWiki**: [https://deepwiki.com/YunaiV/ruoyi-vue-pro](https://deepwiki.com/YunaiV/ruoyi-vue-pro)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [后端](/categories/%E5%90%8E%E7%AB%AF/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [后台管理](/tags/%E5%90%8E%E5%8F%B0%E7%AE%A1%E7%90%86/) / [SpringBoot](/tags/springboot/) / [Vue](/tags/vue/) / [RBAC](/tags/rbac/) / [多租户](/tags/%E5%A4%9A%E7%A7%9F%E6%88%B7/) / [工作流](/tags/%E5%B7%A5%E4%BD%9C%E6%B5%81/) / [微信小程序](/tags/%E5%BE%AE%E4%BF%A1%E5%B0%8F%E7%A8%8B%E5%BA%8F/) / [AI大模型](/tags/ai%E5%A4%A7%E6%A8%A1%E5%9E%8B/)
- 场景： [后端开发](/scenarios/%E5%90%8E%E7%AB%AF%E5%BC%80%E5%8F%91/) / [全栈开发](/scenarios/%E5%85%A8%E6%A0%88%E5%BC%80%E5%8F%91/) / [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/)

### 相关文章

- [RuoYi-Vue Pro：基于Spring Boot的多租户后台管理系统]({{< relref "posts/20260422-github_trending-yunaiv-ruoyi-vue-pro-0.md" >}})
- [🔥Vue管理后台王者！GitHub爆赞🔥极速开发神器！]({{< relref "posts/20260125-github_trending-zxwk1998-vue-admin-better-9.md" >}})
- [RuoYi-Vue Pro：36K星的后台权限管理系统]({{< relref "posts/20260421-github_trending-yunaiv-ruoyi-vue-pro-0.md" >}})
- [RuoYi-Vue-Pro：Spring Boot + Vue3 企业级后台管理系统]({{< relref "posts/20260522-github_trending-yunaiv-ruoyi-vue-pro-0.md" >}})
- [OpenClaw群聊机器人并发上下文隔离与并行回复实现解析]({{< relref "posts/20260218-juejin-openclaw怎么做到不串台能并行还总回对群-含源码解析-openclaw系列第1期-1.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*