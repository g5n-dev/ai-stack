---
title: "AgentCore Gateway授权码流程连接MCP服务器教程"
date: 2026-04-06T16:10:46+08:00
draft: false
entry_kind: "auto"
tags: ["MCP服务器", "Amazon Bedrock", "OAuth2.0", "授权码流程", "AI代理", "Gateway", "安全认证", "JWT"]
categories: ["AI 工程", "系统与基础设施"]
source: blogs_podcasts
description: "概述 Amazon Bedrock AgentCore Gateway 是亚马逊提供的集中管理平台，用于统一配置 AI Agent 对外部工具和 MCP 服务器的访问。通过在 Gateway 中定义 OAuth 2.0 授权方式，Agent 可以在不暴露凭证的前提下，安全地调用受保护的 MCP 接口。 配置流程 1."
external_url: https://aws.amazon.com/blogs/machine-learning/connecting-mcp-servers-to-amazon-bedrock-agentcore-gateway-using-authorization-code-flow
scenarios: ["AI/ML项目", "命令行工具"]
---

# AgentCore Gateway授权码流程连接MCP服务器教程

---

## 基本信息

- **来源**: AWS Machine Learning Blog (blog)
- **发布时间**: 2026-04-06T14:41:46+00:00
- **链接**: [https://aws.amazon.com/blogs/machine-learning/connecting-mcp-servers-to-amazon-bedrock-agentcore-gateway-using-authorization-code-flow](https://aws.amazon.com/blogs/machine-learning/connecting-mcp-servers-to-amazon-bedrock-agentcore-gateway-using-authorization-code-flow)

---
## 摘要/简介

# 中文翻译

Amazon Bedrock AgentCore Gateway 提供了一个集中层，用于管理 AI 代理如何连接到组织内的各种工具和 MCP 服务器。在本文中，我们将逐步介绍如何配置 AgentCore Gateway 以使用授权码流程（Authorization Code flow）连接到受 OAuth 保护的 MCP 服务器。

---
## 导语

Amazon Bedrock AgentCore Gateway为AI代理提供了统一的管理层，用于协调与组织内各类工具和MCP服务器的连接。对于需要OAuth保护的MCP服务器，正确配置授权码流程是确保安全访问的关键步骤。本文将通过具体步骤指导读者完成AgentCore Gateway的配置，使读者能够掌握从环境准备到连接验证的完整配置流程。

---
## 摘要

#### 概述
Amazon Bedrock AgentCore Gateway 是亚马逊提供的集中管理平台，用于统一配置 AI Agent 对外部工具和 MCP 服务器的访问。通过在 Gateway 中定义 OAuth 2.0 授权方式，Agent 可以在不暴露凭证的前提下，安全地调用受保护的 MCP 接口。

#### 配置流程
1. **在 Gateway 创建 MCP 服务器入口**
   - 选择 “MCP Server” 类型，填写服务器基础 URL。
   - 在 “Authentication” 选项中，选择 **Authorization Code** 流程。

2. **在 OAuth 提供方（你的 MCP 服务器）注册客户端**
   - 获取 `client_id`、`client_secret`。
   - 配置回调地址为 Gateway 提供的 `redirect_uri`（必须 HTTPS）。
   - 设定所需的 `scope`（如 `mcp:read`、`mcp:write`）。

3. **实现授权码端点**
   - `/authorize`：返回登录页或直接返回授权码（取决于交互方式）。
   - `/token`：用授权码换取 `access_token` 与可选的 `refresh_token`。
   - 确保 token 采用 JWT 并签名，以便 Gateway 验证。

4. **在 Gateway 完成 OAuth 参数配置**
   - 填入 `authorization_endpoint`、`token_endpoint`、`client_id`、`client_secret`。
   - 设定 token 校验方式（JWT 验证或内联检查）。
   - 如使用 PKCE，可开启相应选项。

5. **启动并测试**
   - 在 Gateway 发起一次模拟请求，浏览器会重定向至 `/authorize`，完成登录后返回授权码，随后自动换取 token 并向 MCP 服务器发起实际调用。
   - 通过 Gateway 日志或调试页面确认 token 被正确传递。

#### 关键点
- 所有网络交互必须走 **HTTPS**，防止 token 被窃取。
- `client_secret` 必须安全存储，建议使用 AWS Secrets Manager。
- Access Token 建议使用短期（如 15 分钟）并配合 Refresh Token 实现续期。
- 若 MCP 服务器本身不支持标准 OAuth，可在外层包装一个轻量 OAuth 代理服务。
- 启用 Gateway 的审计日志，记录每次授权和调用情况，便于安全审计。

#### 小结
通过在 Amazon Bedrock AgentCore Gateway 中配置 Authorization Code 流程，AI Agent 能够在不泄露凭证的前提下，以标准化的 OAuth 安全机制访问外部 MCP 服务器，实现组织级别的统一鉴权与访问控制。

---
## 评论

#### 中心观点

AgentCore Gateway通过Authorization Code flow为MCP服务器提供企业级OAuth认证能力，这一设计将AI agent的安全接入从点对点模式升级为集中管控模式。

#### 支撑理由

事实陈述：Authorization Code flow是OAuth 2.0框架中最适用于后端服务授权的模式，通过短期授权码交换访问令牌，避免令牌在前端暴露。AgentCore Gateway位于请求链路的中转层，负责令牌验证和请求路由，这意味着每个MCP服务器的认证逻辑无需嵌入agent代码。

作者观点：文章强调配置的声明式特性——通过JSON或YAML声明OAuth端点、客户端凭据和作用域，Gateway自动处理重定向和令牌刷新。作者认为这降低了安全配置的认知负担，使开发者专注于业务逻辑。

我的推断：Gateway模式的价值在于统一审计。所有流向MCP服务器的请求均经过同一入口，这意味着企业可以集中记录访问日志、实施细粒度策略，而无需在每个MCP服务器单独配置安全层。

#### 边界条件

此方案的有效性依赖三个前提：OAuth授权服务器必须支持Authorization Code flow；MCP服务器需接受Bearer令牌而非自定义头；Gateway需与授权服务器保持网络可达性。对于仅有API密钥认证能力的MCP服务器，此方案不适用。

#### 实践启发

部署时需区分网关层与业务层的职责边界。网关负责令牌验证和请求转发，但不应缓存业务敏感数据于Gateway层。令牌刷新策略应在配置中显式声明，避免生产环境出现静默认证失败。

---
## 技术分析

#### 核心观点

AgentCore Gateway 通过统一的入口层，集中管理 AI Agent 对外部工具和 MCP 服务器的访问。采用 OAuth 2.0 Authorization Code 流程，使 Agent 能够在不暴露凭证的前提下安全地调用受保护的资源，从而实现统一鉴权、细粒度权限控制以及全链路审计。

#### 关键技术点

##### 1. AgentCore Gateway 架构

- **集中代理**：所有 Agent 与 MCP 之间的交互都经过 Gateway，避免在每个 Agent 侧实现复杂的 OAuth 逻辑。
- **路由与策略**：基于声明式配置，Gateway 根据工具名、作用域或租户标签动态路由请求，并执行细粒度访问策略。
- **会话保持**：Gateway 维护每个授权会话的上下文，支持令牌刷新和跨请求的状态同步。

##### 2. Authorization Code 流程实现

1. **授权请求生成**：Gateway 构造符合 RFC 7636 的 PKCE 参数，指向 MCP 服务器的 `/authorize` 端点。
2. **回调处理**：MCP 服务器将 `code` 通过重定向 URI 返回给 Gateway，Gateway 使用后端通道完成 code 换取 `access_token` 与 `refresh_token`。
3. **令牌注入**：Gateway 在转发工具调用请求时自动在 HTTP Header 中注入 `Authorization: Bearer <token>`，对上层 Agent 完全透明。
4. **刷新机制**：依据令牌的 `expires_in`，Gateway 在后台自动使用 `refresh_token` 更新，保证长时间运行的 Agent 不会因 token 失效而中断。

##### 3. OAuth 客户端安全配置

- **密钥存储**：使用 AWS Secrets Manager 或 HashiCorp Vault 存储 `client_secret`，并在 Gateway 启动时通过 IAM 角色注入。
- **范围约束**：仅授予 Agent 实际需要的 scopes，避免过度权限。
- **PKCE 强制**：对所有公共客户端启用 PKCE，阻止授权码拦截攻击。
- **TLS 强制**：所有外部请求必须基于 HTTPS，防止令牌在传输层泄露。

#### 实际应用价值

- **统一鉴权**：不同业务线或租户的 MCP 服务器可共用同一套身份提供商，简化 SSO 集成。
- **安全审计**：Gateway 记录每一次授权请求和令牌使用日志，便于合规审计。
- **弹性伸缩**：Gateway 支持水平扩展，后端通过 AWS Lambda/ECS 部署，能够处理大量并发 Agent 请求。

#### 行业影响

- **生态标准化**：推动 AI Agent 与外部工具交互的 OAuth 规范成为行业事实标准，降低供应商锁定。
- **企业采纳**：在金融、医疗等强监管行业，集中式授权满足数据治理与合规要求，加速 AI 落地。
- **多 Agent 协作**：通过统一网关，跨组织、跨域的多 Agent 任务可实现细粒度授权，提升复杂工作流的可行性。

#### 边界条件与实践建议

##### 边界条件

- **不支持 OAuth 的 MCP**：若目标服务器仅实现 API‑Key 或 Basic 认证，Gateway 需要额外适配器或转为客户端凭证流。
- **高延迟网络**：Authorization Code 流程涉及多次 HTTP 往返，若网络 RTT 超过 500 ms，需考虑令牌缓存或本地代理。
- **一次性刷新令牌**：当 MCP 对 `refresh_token` 采用一次性策略时，Gateway 必须每次刷新后重新发起授权，而不是复用旧 token。

##### 实践建议

1. **分层配置**：在 GitOps 环境中使用声明式配置文件管理 Gateway 路由、OAuth 客户端信息与安全策略。
2. **最小权限原则**：为每个 MCP 创建专属 OAuth 客户端，仅授予必需 scopes，并通过 IAM 角色限制 Gateway 对密钥的访问。
3. **监控与告警**：部署 CloudWatch 指标（如 `AuthCodeExchanges`, `TokenRefreshErrors`）并设置异常阈值，及时发现潜在攻击。
4. **灾难恢复**：定期备份 OAuth 配置，支持跨区域复制，确保 Gateway 失效时仍能恢复授权会话。

#### 论证地图

##### 中心命题

AgentCore Gateway 通过标准化的 Authorization Code 流程，实现对受保护 MCP 服务器的统一、安全、可审计的接入。

##### 支撑理由

- 集中管理降低 Agent 侧实现复杂度。
- OAuth 2.0 提供业界认可的授权安全模型。
- Gateway 的会话保持和自动刷新保证长时任务可靠性。
- 统一的审计日志满足合规需求。

##### 反例或边界条件

- MCP 服务器不支持 OAuth（需自定义适配器）。
- 使用单向刷新令牌导致频繁重新授权（影响实时性）。
- 极端网络分区导致授权回调超时（需要降级策略）。

##### 可验证方式

- **单元测试**：使用 Mock OAuth Server 验证 Authorization Code 交换与 token 刷新逻辑。
- **集成测试**：在隔离环境中部署 Gateway + MCP，验证 Agent 实际调用成功率。
- **安全审计**：检查日志中 token 使用记录是否符合配置的 scopes 与有效期。
- **性能基准**：在 1 k 并发 Agent 场景下测量授权时延与系统吞吐量，确保满足 SLA。

---
## 学习要点

- 在 Amazon Bedrock AgentCore Gateway 中为 MCP 服务器注册 OAuth2 客户端，并使用 Authorization Code 流程获取访问令牌，以实现安全的身份验证。
- 配置的 Redirect URI 必须与 MCP 服务器接收授权码的端点完全一致，否则授权流程会失败。
- 使用短生命周期访问令牌并实现自动刷新，以确保 MCP 服务器在令牌失效后仍能持续与网关通信。
- 在授权请求中指定最小必需的 OAuth2 作用域，仅授予 MCP 服务器执行所需 Bedrock AgentCore 操作的权限。
- 通过 HTTPS 访问授权端点并验证 TLS 证书，防止令牌在传输过程中被窃取或篡改。
- 将客户端 ID 和密钥安全存储在 AWS Secrets Manager 等服务中，并定期轮换以降低泄露风险。
- 启用 CloudWatch 日志和监控，追踪令牌发放和请求使用情况，及时发现异常行为。

---
## 引用

- **文章/节目**: [https://aws.amazon.com/blogs/machine-learning/connecting-mcp-servers-to-amazon-bedrock-agentcore-gateway-using-authorization-code-flow](https://aws.amazon.com/blogs/machine-learning/connecting-mcp-servers-to-amazon-bedrock-agentcore-gateway-using-authorization-code-flow)
- **RSS 源**: [https://aws.amazon.com/blogs/machine-learning/feed/](https://aws.amazon.com/blogs/machine-learning/feed/)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/)
- 标签： [MCP服务器](/tags/mcp%E6%9C%8D%E5%8A%A1%E5%99%A8/) / [Amazon Bedrock](/tags/amazon-bedrock/) / [OAuth2.0](/tags/oauth2.0/) / [授权码流程](/tags/%E6%8E%88%E6%9D%83%E7%A0%81%E6%B5%81%E7%A8%8B/) / [AI代理](/tags/ai%E4%BB%A3%E7%90%86/) / [Gateway](/tags/gateway/) / [安全认证](/tags/%E5%AE%89%E5%85%A8%E8%AE%A4%E8%AF%81/) / [JWT](/tags/jwt/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [命令行工具](/scenarios/%E5%91%BD%E4%BB%A4%E8%A1%8C%E5%B7%A5%E5%85%B7/)

### 相关文章

- [Iberdrola enhances IT operations using Amazon Bedrock A]({{< relref "posts/20260210-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-1.md" >}})
- [利用全栈模板加速开发基于Amazon Bedrock AgentCore的应用]({{< relref "posts/20260211-blogs_podcasts-accelerate-agentic-application-development-with-a--12.md" >}})
- [Iberdrola enhances IT operations using Amazon Bedrock A]({{< relref "posts/20260211-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-1.md" >}})
- [Iberdrola enhances IT operations using Amazon Bedrock A]({{< relref "posts/20260211-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-2.md" >}})
- [Iberdrola 利用 Amazon Bedrock 和 AgentCore 优化 ServiceNow 运]({{< relref "posts/20260212-blogs_podcasts-iberdrola-enhances-it-operations-using-amazon-bedr-10.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*