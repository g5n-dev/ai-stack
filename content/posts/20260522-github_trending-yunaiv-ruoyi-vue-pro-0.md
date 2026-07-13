---
title: "RuoYi-Vue-Pro：Spring Boot + Vue3 企业级后台管理系统"
date: 2026-05-22T21:33:49+08:00
draft: false
entry_kind: "auto"
tags: ["RuoYi", "Spring", "Vue3", "企业级", "后台管理", "Java", "开源", "全栈"]
categories: ["后端", "前端"]
source: github_trending
description: "ruoyi-vue-pro 是一款基于 Spring Boot 的开源企业级管理平台，采用模块化结构，提供用户权限、工作流、电商、IoT 等常用业务模块，帮助团队快速构建和迭代后台系统。本文将重点解析项目整体架构、核心模块实现以及本地启动与二次开发的实战要点。"
external_url: https://github.com/YunaiV/ruoyi-vue-pro
scenarios: ["后端开发", "前端开发", "全栈开发"]
---

# RuoYi-Vue-Pro：Spring Boot + Vue3 企业级后台管理系统

> **原名**: YunaiV /

      ruoyi-vue-pro

---

## 基本信息

- **描述**: 您好，这段内容本身已经是中文了，无需翻译。

如果您是想让我将其翻译成**英文**，请告诉我，我非常乐意为您翻译。

如果您确实需要其他帮助，请说明您的具体需求。谢谢！
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

ruoyi-vue-pro 是一款基于 Spring Boot 的开源企业级管理平台，采用模块化结构，提供用户权限、工作流、电商、IoT 等常用业务模块，帮助团队快速构建和迭代后台系统。本文将重点解析项目整体架构、核心模块实现以及本地启动与二次开发的实战要点。

---
## 评论

#### 总体判断

RuoYi-Vue-Pro是一个功能完备、架构相对清晰的企业级后台管理系统，基于Spring Boot与Vue技术栈构建，在开源社区拥有较高认可度（37k+星标），适合作为企业业务系统快速开发的起点，但需评估其技术债务与长期维护成本。

#### 技术架构与实现质量

从项目结构来看，采用Maven多模块组织方式，模块划分为yudao-dependencies（依赖管理）、yudao-framework（核心框架，含security子模块）、yudao-server（业务服务）三层，架构分层基本合理。独立封装安全模块体现了关注点分离原则，版本号统一管理也是良好的工程实践。核心依赖为Spring Boot + MyBatis Plus + Vue + Element UI，这是一套成熟且文档完善的技术组合，适合国内企业项目场景。

#### 适用场景

该系统适用于以下场景：一是中小型企业的后台管理功能快速搭建，尤其是需要RBAC权限管理、多租户支持等通用能力的项目；二是作为学习企业级Java Web开发的参考项目，其代码结构展示了Spring Boot生态中常见的分层与模块化实践；三是业务系统原型验证阶段，可基于其扩展模块（商城、CRM、ERP等）快速构建MVP。微信小程序支持使其具备全栈交付能力。

#### 局限性

需要指出的是，37k+星标主要反映的是关注度而非项目成熟度。功能“大而全”可能导致核心代码与扩展模块耦合度较高，特定业务场景下的深度定制可能面临侵入式修改。此外，描述中列举的“AI大模型”“IoT物联网”等功能属于扩展能力，其实现深度与稳定性需实际验证。该项目采用自研框架（yudao-framework）而非纯标准Spring生态，长期维护依赖作者个人投入，存在一定的技术锁定风险。

#### 验证方式

建议通过以下方式验证：一是直接运行官方提供的Demo环境，评估功能完整性与用户体验；二是检查GitHub Issues的响应速度与问题解决率，判断社区活跃度与维护质量；三是抽取权限模块或工作流模块进行代码审查，确认其设计是否符合实际业务需求。

---
## 技术分析

#### 架构概述

##### 模块化设计
项目采用多模块 Maven 结构，父 POM 负责统一版本管理与公共依赖，子模块按功能划分为 **yudao‑framework**（安全、工具、通用组件）、**yudao‑server**（业务启动入口）以及 **yudao‑module‑\***（系统、用户、权限、工作流、电商、CRM、ERP、MES、IM、AI、IoT 等独立业务模块）。模块之间通过 Spring Boot 的自动装配和依赖注入解耦，业务模块可根据实际需求选择性引入，避免整体体积臃肿。

##### 技术栈
- **后端**：Spring Boot 2.6/2.7 + MyBatis‑Plus 3.5 + Spring Security + JWT
- **前端**：Vue 3 + Element Plus（配套 Vite 构建）
- **数据层**：MySQL（主库）+ Redis（缓存、分布式会话）+ Elasticsearch（搜索）
- **消息**：RabbitMQ / RocketMQ
- **文件**：MinIO / 阿里云 OSS
- **工作流**：Flowable 6.x
- **微服务治理**：Nacos（配置、注册）+ Spring Cloud GateWay（可选）

#### 核心能力

##### 权限与多租户
- **RBAC 动态权限**：基于 Spring Security 的资源‑角色‑用户三层模型，支持菜单、按钮、API 级别的细粒度控制。
- **数据权限**：通过 AOP + MyBatis‑Plus 拦截器实现行级过滤，支持“只看本部门”“只看本人”等规则。
- **SaaS 多租户**：利用 ThreadLocal 保存租户标识，在 SQL 执行前动态切换 schema 或在查询中加入租户过滤列，实现业务数据的完全隔离。

##### 业务流程与工作流
- **Flowable 集成**：提供 BPMN 2.0 流程定义、任务审批、流程历史查询等完整生命周期管理，支持自定义表单与业务回调，便于构建 OA、采购、销售等审批流。

##### 业务功能集成
- **三方登录**：封装微信、钉钉、企业微信等 OAuth2 授权流程。
- **支付/短信**：统一抽象支付宝、微信支付、阿里云短信等渠道，方便切换。
- **电商/CRM/ERP/MES**：已有商品、订单、库存、会员、营销、供应链、生产工单等业务实体与 RESTful 接口。
- **即时通讯**：基于 Netty 的 WebSocket 长连接，提供点对点、群组聊天功能。
- **AI 大模型**：预留调用 OpenAI、百度文心等大模型的 HTTP 客户端，配合业务实现智能客服、内容生成等场景。
- **IoT**：集成 MQTT 客户端与设备影子模型，支持设备注册、状态上报、远程控制。

#### 技术实现要点

##### 后端实现
- **统一响应**：基于 `Result<T>` 包装返回码、消息与数据，便于前端统一处理。
- **全局异常**：使用 `@ControllerAdvice` 统一捕获业务异常、校验异常、权限异常并返回统一错误码。
- **分页插件**：MyBatis‑Plus 的 `PaginationInnerInterceptor` 自动处理分页请求。
- **安全加固**：JWT 短期令牌 + RefreshToken 双 token 机制，支持黑名单失效、登录设备统计。

##### 前端实现
- **菜单路由**：后端动态生成路由 JSON，前端根据角色动态挂载，实现真正的按钮级权限。
- **主题**：Element Plus 支持的深/浅色切换、主题变量统一管理。
- **状态管理**：Pinia 管理全局用户、租户、权限信息，刷新页面后通过 `/user/info` 接口重新同步。

##### 集成与扩展
- **插件化**：业务模块实现 `ModuleInitializer` 接口，Spring 启动时自动扫描并初始化，提供业务扩展点。
- **代码生成**：基于 MyBatis‑Plus Generator，配置模板后可一键生成 CRUD、Vue 表单与列表页面。

#### 适用场景

- 需要快速交付企业内部管理系统（OA、HR、资产、财务）。
- 构建 SaaS 平台，要求多租户数据隔离、租户级别的权限与计费。
- 已有业务系统需要工作流审批、即时消息或 IoT 设备接入。
- 团队熟悉 Spring Boot + Vue，希望采用统一技术栈进行全栈开发。

#### 不适用场景

- 对系统体积、启动时间有极致要求的轻量级微服务（该项目聚合了大量业务模块）。
- 业务模型高度定制化、几乎不使用已有功能的场景（直接基于 Spring Boot 骨架自行实现更轻便）。
- 需要极强实时性能的大数据流处理（如实时数仓、金融高频交易），当前架构未针对此类场景进行专门优化。

#### 学习与落地建议

1. **从框架层入手**：先阅读 `yudao‑framework` 中的安全starter、数据权限拦截、租户过滤实现，这部分是整个平台的根基。
2. **模块拆分实验**：挑选一个业务模块（如 `yudao‑module‑mall`）完整跑通，了解业务代码如何组织、API 如何暴露、前端如何调用。
3. **权限模型深入**：结合 RBAC 与数据权限的实现源码，掌握动态菜单生成与行级过滤的实现思路，以便后期根据企业需求进行细粒度调整。
4. **部署容器化**：项目根目录提供 `Dockerfile` 与 `docker‑compose.yml`，可在本地快速搭建 MySQL、Redis、Nacos 等依赖，利用 Kubernetes 或 Docker Swarm 实现生产环境弹性伸缩。
5. **性能监控**：建议引入 Spring Boot Actuator + Micrometer，配合 Prometheus + Grafana，对接口响应、SQL 耗时、缓存命中率进行可视化监控，及时发现业务热点。
6. **持续集成**：使用 Jenkins / GitLab CI 配置 Maven 构建 + Vue 前端打包 + Docker 镜像推送，实现代码提交即自动部署的闭环。

通过上述步骤，可在保持平台已有优势的前提下，平滑落地至实际业务项目，并在后期根据业务演进逐步替换或扩展特定模块。

---
## 学习要点

- RuoYi-Vue-Pro 完整展示了 Spring Boot 与 Vue3 前后端分离的技术栈组合及协同开发模式。
- 项目采用 JWT 与 Shiro 实现无状态身份认证，并基于数据范围的细粒度 RBAC 权限控制实现动态授权。
- 通过 MyBatis‑Plus 与代码生成器一次性生成后端 CRUD 与前端页面，大幅提升开发效率并保持代码一致性。
- 采用模块化分层结构（common、system、generator 等）明确职责，提升项目的可维护性和可扩展性。
- 前端使用 Element Plus UI 框架结合 Vue3 Composition API 与 Vite，实现高效组件化开发与快速热更新。
- 统一异常处理、全局日志记录与 Swagger API 文档生成，提升问题定位和团队协作效率。
- 引入 Nacos 配置中心实现配置集中管理与运行时动态刷新，支持多环境快速部署。

---
## 引用

- **GitHub 仓库**: [https://github.com/YunaiV/ruoyi-vue-pro](https://github.com/YunaiV/ruoyi-vue-pro)
- **DeepWiki**: [https://deepwiki.com/YunaiV/ruoyi-vue-pro](https://deepwiki.com/YunaiV/ruoyi-vue-pro)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [后端](/categories/%E5%90%8E%E7%AB%AF/) / [前端](/categories/%E5%89%8D%E7%AB%AF/)
- 标签： [RuoYi](/tags/ruoyi/) / [Spring](/tags/spring/) / [Vue3](/tags/vue3/) / [企业级](/tags/%E4%BC%81%E4%B8%9A%E7%BA%A7/) / [后台管理](/tags/%E5%90%8E%E5%8F%B0%E7%AE%A1%E7%90%86/) / [Java](/tags/java/) / [开源](/tags/%E5%BC%80%E6%BA%90/) / [全栈](/tags/%E5%85%A8%E6%A0%88/)
- 场景： [后端开发](/scenarios/%E5%90%8E%E7%AB%AF%E5%BC%80%E5%8F%91/) / [前端开发](/scenarios/%E5%89%8D%E7%AB%AF%E5%BC%80%E5%8F%91/) / [全栈开发](/scenarios/%E5%85%A8%E6%A0%88%E5%BC%80%E5%8F%91/)

### 相关文章

- [Java低代码平台JeecgBoot：AI+零代码双模式]({{< relref "posts/20260513-github_trending-jeecgboot-jeecgboot-0.md" >}})
- [🚀若依Vue3重磅发布！前后端分离+企业级神器🔥]({{< relref "posts/20260126-github_trending-yangzongzhuan-ruoyi-vue3-9.md" >}})
- [🔥若依Vue3重磅升级！企业级脚手架，开源黑马！🚀]({{< relref "posts/20260128-github_trending-yangzongzhuan-ruoyi-vue3-4.md" >}})
- [JeecgBoot：集成AI低代码平台与代码生成器的Java开发框架]({{< relref "posts/20260129-github_trending-jeecgboot-jeecgboot-3.md" >}})
- [JeecgBoot：集成AI低代码与代码生成器的企业级开发平台]({{< relref "posts/20260129-github_trending-jeecgboot-jeecgboot-7.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*