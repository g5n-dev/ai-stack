---
title: "Manage end-user OAuth consent for AI agents with Amazon Bedrock AgentCore"
date: 2026-09-15T09:29:27+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "生成式 AI", "Amazon Bedrock AgentCore", "Announcements", "Intermediate (200)", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:dd5e085f0a05b1cdc24faa9ff3f12afc75c726f8b6ba5f9a7288011518b2ebad"
source_payload_sha256: "sha256:71ab08f289db44807cf0f5550ceef5ff11a4b9490651bd0853a4d412275dd2b8"
observation_id: obs_e4887ae13cdf3e0d1a57b577c2d965898d8b92d3c1978971eeb1fa95871f6051
event_id: evt_5771761369d6b59ca4c7ba0d2797ddb72d1923f605a65e218ac4575b988d4453
revision_id: rev_894d8eec0a8219a670fa7676316a193df40aefc3ff27cf64391894fa20533714
source_published_at: 2026-09-14T20:35:45Z
first_seen_at: 2026-09-15T01:28:12.253206Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 73
interpretation_sha256: "sha256:914e374c388b30bc89f7ba139674ab1c52be2d1b6471018191de11a62c7fce20"
description: "该内容介绍 Amazon Bedrock AgentCore 提供的托管式 Consent portal，用于自动完成 AI 代理对 GitHub、Slack 等服务的 OAuth 授权流程，包括身份验证、浏览器跳转、会话绑定以及令牌的安全存储，省去自行搭建回调页面和管理会话的负担。"
external_url: https://aws.amazon.com/blogs/machine-learning/manage-end-user-oauth-consent-for-ai-agents-with-amazon-bedrock-agentcore
parent_observation_id: null
last_seen_at: 2026-09-15T01:28:12.253206Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/manage-end-user-oauth-consent-for-ai-agents-with-amazon-bedrock-agentcore](https://aws.amazon.com/blogs/machine-learning/manage-end-user-oauth-consent-for-ai-agents-with-amazon-bedrock-agentcore)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么  
该内容介绍 Amazon Bedrock AgentCore 提供的托管式 Consent portal，用于自动完成 AI 代理对 GitHub、Slack 等服务的 OAuth 授权流程，包括身份验证、浏览器跳转、会话绑定以及令牌的安全存储，省去自行搭建回调页面和管理会话的负担。

### 用在哪里  
适用于在 IDE 或 MCP 客户端（如 Kiro、Claude Code、Cursor、Visual Studio Code）中使用 AI 编程助手的企业场景，帮助管理员统一配置企业 IdP 并让开发者在浏览器中一次性授权所需第三方服务。

### 可以推断的  
推测：在已有基于 JWT 的网关接入和统一 IdP 的环境下，企业引入该 portal 后可显著降低为每位用户单独实现 OAuth 回调的开发和维护成本。  
推测：集中管理令牌后，开发者后续调用工具时无需再次弹出授权窗口，AI 代理的使用流程会更连贯，提升团队协作效率。

## 来源摘要/节选

> AI agents often need to access services such as GitHub and Slack on a user’s behalf. Before an agent can act, the user must authenticate with the provider and explicitly approve the requested access. The application must then securely associate the resulting OAuth grant with the user who authorized it. This process is called session binding.
>
> Previously, customers using the AgentCore Identity (a capability of Amazon Bedrock AgentCore) three-legged OAuth (3LO) flow (also known as OAuth 2.0 authorization code flow) had to build and host their own session binding infrastructure. This included presenting the authorization URL, hosting a public HTTPS callback, authenticating the returning user, managing browser sessions, and calling CompleteResourceTokenAuth to complete the flow.
>
> AgentCore Identity now offers a Consent portal, a managed web experience and session binding endpoint for AgentCore Gateway, a capability of Amazon Bedrock AgentCore. You create a portal for a gateway and share its URL with your users. Users authenticate with your organization’s identity provider (IdP), review the services available to the agent, and grant consent to individual providers. The portal handles the browser redirects and session binding, while AgentCore Identity stores the resulting tokens in its token vault.
>
> This capability is particularly useful for agents accessed through IDE and Model Context Protocol (MCP) clients such as Kiro, Claude Code, Cursor, and Visual Studio Code. Users can grant consent before invoking a tool, and subsequent tool calls can use the token already stored for that user. In this post, we use a software development assistant as an example. We walk through the administrator and end-user experiences on the AWS Management Console and browser, and show how to review the resulting activity in AWS CloudTrail.
>
> Figure 1: The Consent portal authenticates the user with the corporate IdP, uses its IAM execution role to discover configured gateway targets, presents provider connections, completes session binding, and stores per-user tokens in the AgentCore Identity token vault
>
> Example scenario: Give a development assistant access to GitHub
>
> Consider a company named Example Corp that provides its developers with an AI coding assistant through an AgentCore Gateway. The assistant has two targets:
>
> A GitHub target that can list repositories and create issues.
>
> A Slack target that can list public channels and post messages.
>
> Example Corp uses its corporate IdP to authenticate employees. The administrator wants each GitHub and Slack OAuth grant to remain associated with the employee who approved it. Developers can connect either provider independently and return to their IDE without repeated prompts.
>
> The walkthrough follows these two roles:
>
> Administrator: Configures the corporate IdP, GitHub and Slack gateway targets, execution role, and Consent portal, and then sends the portal URL to developers.
>
> End user: Opens the URL, signs in with the corporate IdP, connects GitHub when needed, and can grant Slack access separately.
>
> Prerequisites
>
> Before starting the walkthrough, Example Corp needs:
>
> An AWS account with access to Amazon Bedrock AgentCore.
>
> An AgentCore Gateway configured with JWT inbound authorization.
>
> An IDE or MCP client configured to connect to the same AgentCore Gateway that will be attached to the Consent portal.
>
> Administrative access to the corporate IdP.
>
> A registered GitHub OAuth App and Slack app for a development or test workspace.
>
> Permission to register the AgentCore Identity callback URL in each provider application.
>
> Getting started
>
> The following steps show what the Example Corp administrator configures and what a developer experiences after receiving the portal URL.
>
> Steps for administrator
>
> The administrator completes Steps 1–6 to configure the identity provider, gateway targets, execution role, and Consent portal.
>
> Step 1: Prepare the corporate IdP and gateway connections
>
> Administrator IAM policy
>
> Attach this policy to the administrator identity that performs Steps 1–3. Replace the account ID.
>
> {
>
> "Version": "2012-10-17",
>
> "Statement": [
>
> {
>
> "Sid": "ManageConsentPortalResources",
>
> "Effect": "Allow",
>
> "Action": [
>
> "bedrock-agentcore:CreateConsentPortal",
>
> "bedrock-agentcore:GetConsentPortal",
>
> "bedrock-agentcore:ListConsentPortals",
>
> "bedrock-agentcore:CreateOauth2CredentialProvider",
>
> "bedrock-agentcore:GetOauth2CredentialProvider",
>
> "bedrock-agentcore:ListOauth2CredentialProviders",
>
> "bedrock-agentcore:GetGateway",
>
> "bedrock-agentcore:ListGateways",
>
> "bedrock-agentcore:CreateGatewayTarget",
>
> "bedrock-agentcore:GetGatewayTarget",
>
> "bedrock-agentcore:ListGatewayTargets",
>
> "bedrock-agentcore:UpdateGatewayTarget"
>
> ],
>
> "Resource": "*"
>
> },
>
> {
>
> "Sid": "CreateAndPassExecutionRole",
>
> "Effect": "Allow",
>
> "Action": [
>
> "iam:CreateRole",
>
> "iam:GetRole",
>
> "iam:PutRolePolicy",
>
> "iam:GetRolePolicy",
>
> "iam:PassRole"
>
> ],
>
> "Resource": "arn:aws:iam::111122223333:role/service-role/AmazonBedrockAgentCoreConsentPortal*"
>
> }
>
> ]
>
> }
>
> The AWS Identity and Access Management (IAM) statement covers the Create default role option on the console, which creates a service role named AmazonBedrockAgentCoreConsentPortalDefaultServiceRole-&lt;suffix&gt;. If you supply your own role instead, scope iam:PassRole to that role ARN.
>
> Step 2: Configure the corporate IdP application
>
> In the corporate IdP, create an OpenID Connect (OIDC) web application for the Consent portal.
>
> Enable the authorization code grant and generate a client ID and client secret.
>
> Configure the login scopes, at minimum openid.
>
> Record the OpenID Connect (OIDC) discovery URL. The portal uses the authorization endpoint, token endpoint, and signing keys from this document.
>
> Add a temporary callback URL. You replace it in Step 6, after the portal URL exists.
>
> The IdP must issue a JSON Web Token (JWT) access token that the portal can validate. For example, with Okta, use a custom authorization server with an access policy that permits the application and the authorization code grant. With Auth0, configure an audience when needed so the IdP returns a signed JWT access token instead of an opaque token.
>
> Step 3: Create the IdP credential provider
>
> The portal reads the IdP client ID and client secret from an OAuth2 credential provider.
>
> Open the Amazon Bedrock AgentCore console.
>
> Under Build, choose Identity.
>
> In Outbound Auth, choose Add Outbound Auth, and then choose Add OAuth client.
>
> Enter a name, such as gateway-demo-idp.
>
> Enter the client ID and client secret from the corporate IdP application, and provide the OIDC discovery configuration.
>
> Choose Add OAuth client.
>
> Figure 2: AgentCore Identity uses one credential provider for portal sign-in and separate outbound providers for GitHub and Slack
>
> Step 4: Verify outbound prerequisites
>
> Before creating the Consent portal, confirm:
>
> The GitHub and Slack OAuth applications are registered, and their client secrets are stored in AWS Secrets Manager.
>
> AgentCore Identity has separate outbound OAuth credential providers for GitHub and Slack, and each generated callback URL is registered with the matching provider application.
>
> The GitHub and Slack gateway targets use the authorization code grant, request only the required scopes, and have a Ready status.
>
> The Consent portal execution role selected in Step 5 can read any customer-managed secrets referenced by the outbound credential providers.
>
> After the portal URL is assigned, configure each target’s default return URL in Step 6.
>
> Figure 3: The gateway exposes independent GitHub and Slack targets, each associated with its own outbound OAuth provider
>
> Step 5: Create the Consent portal
>
> On the Identity page, the Consent portals section lists the portals in the account and AWS Region.
>
> Figure 4: The Consent portals section on the AgentCore Identity page. Create a portal only when a gateway uses 3LO that requires user consent
>
> In Consent portals, choose Create portal.
>
> Under Consent portal details, for Name, enter a name such as consent-portal-heqk0. Names accept 1–50 characters, using letters, numbers, hyphens, and underscores.
>
> Optionally enter a Description of up to 512 characters.
>
> For Gateway, select the development assistant’s gateway. The gateway name is visible to end users in the Consent portal, so choose a clear, recognizable name. One Consent portal is allowed per gateway, and the gateway can’t be changed after creation.
>
> Under IdP credential configurations, for IdP Credential Provider, select the OAuth2 credential provider created in Step 3.
>
> Under Scopes, keep the required openid scope. Additional scopes are optional. Choose Add scope only when your IdP or application requires them.
>
> For Audience – optional, keep None unless your gateway specifies audiences. The value is validated against the audiences configured on the AgentCore Gateway.
>
> Expand Permissions. For IAM permissions, choose Create default role to have the console create a service role with the required permissions, or choose Use another role to select an existing role.
>
> Choose Create portal.
>
> Figure 5: While the status is Creating, the portal ARN and execution role are visible but the URL isn’t assigned yet
>
> When provisioning finishes, the status changes to Active, the Consent portal URL appears, and a Launch Consent portal button opens it in a new tab. The URL follows the pattern https://&lt;gateway-name&gt;.consent-portal.bedrock-agentcore.&lt;region&gt;.amazonaws.com.
>
> Figure 6: After the portal becomes Active, the console shows the assigned URL that you share with end users
>
> Step 6: Register callback URLs and send the portal URL
>
> Copy the consent portal URL from the portal details page.
>
> In the corporate IdP application, for example, Amazon Cognito, Okta, or Auth0, replace the temporary callback with &lt;portal-url&gt;/callback. Don’t add a trailing slash. This isn’t the GitHub or Slack application callback. Those applications use the unique AgentCore Identity callbackUrl.
>
> For each 3LO gateway target, set the default return URL to &lt;portal-url&gt;/connect/callback.
>
> Confirm that each outbound provider application contains the AgentCore Identity callback URL returned when its OAuth credential provider was created.
>
> Test the portal URL in a browser.
>
> Send the portal URL to the development team through an approved communication channel.
>
> Callback URL reference
>
> URL
>
> Where it is configured
>
> Purpose
>
> &lt;portal-url&gt;/callback
>
> Corporate IdP application
>
> Returns the user after portal login
>
> &lt;portal-url&gt;/connect/callback
>
> Gateway target as the default return URL
>
> Returns the user to the managed session binding endpoint
>
> AgentCore Identity callbackUrl
>
> Outbound provider application
>
> Sends the provider’s authorization code to AgentCore Identity
>
> After completing the provider callbacks and gateway targets, verify the final administrator configuration before sharing the portal URL.
>
> Steps for end user
>
> The end user completes Step 7 to sign in and connect providers after receiving the portal URL.
>
> Step 7: Sign in and connect providers
>
> Open the portal URL in a browser.
>
> Choose Sign in. The browser redirects to the Example Corp IdP.
>
> Authenticate with the corporate identity. The portal then uses its IAM execution role to retrieve the gateway’s configured targets and their connection state.
>
> On the Connections page, review the GitHub and Slack OAuth clients and their target status.
>
> Choose Connect for GitHub.
>
> Review the scopes on GitHub’s consent page and approve access.
>
> After the browser returns to the portal, verify that GitHub shows Connected while Slack remains Not connected. This demonstrates that grants are independent for each provider.
>
> If the agent needs Slack, choose Connect for Slack, select the workspace, review the requested permissions, and approve the app. Otherwise, leave Slack unconnected until it is needed.
>
> Return to the IDE or MCP client configured to use the same AgentCore Gateway attached to the Consent portal, and retry the applicable GitHub or Slack tool call through that gateway.
>
> The following screenshots capture useful checkpoints for the walkthrough.
>
> Figure 7: The Consent portal discovers the GitHub OAuth client and its target. Both remain Not connected until the user grants access
>
> Figure 8: GitHub displays the scopes and organization access requested by the OAuth application before the user authorizes it
>
> Figure 9: After GitHub returns the authorization result, the portal completes session binding and shows the OAuth client and target as Connected
>
> Figure 10: GitHub remains Connected while Slack is Not connected, demonstrating that users grant consent independently for each outbound provider
>
> Behind the scenes
>
> The portal validates the IdP response and establishes an encrypted browser session.
>
> The portal uses its execution role to list the attached gateway’s 3LO targets.
>
> When the user chooses Connect, the portal calls GetResourceOauth2Token and receives an authorization URL and session URI.
>
> After the provider returns the authorization code to AgentCore Identity, the browser returns to the portal’s managed session binding endpoint.
>
> The portal calls CompleteResourceTokenAuth with the authenticated user context.
>
> When the provider returns a refresh token, AgentCore Identity stores it and automatically uses it to obtain a new access token after the current access token expires. Sometimes no valid refresh token is available, because the provider didn’t issue one or it has expired or been revoked. In that case, the user must return to the Consent portal and reauthorize when the access token can no longer be used. Configure the provider to issue refresh tokens where supported. For example, enable user-to-server token expiration for GitHub or token rotation for Slack.
>
> The next time the developer opens the portal, connected providers remain visible. The developer doesn’t need to approve a provider again unless the grant is revoked, expires, or requires renewed consent. The developer can also choose Disconnect and later connect the provider again.
>
> Review consent activity in AWS CloudTrail
>
> Amazon Bedrock AgentCore records consent operations in AWS CloudTrail. In CloudTrail event history, filter Event source by bedrock-agentcore.amazonaws.com, then review:
>
> GetResourceOauth2Token when the portal starts OAuth authorization for a provider.
>
> CompleteResourceTokenAuth when session binding is completed.
>
> GetWorkloadAccessTokenForJWT when the portal obtains gateway access for the authenticated user.
>
> A GetResourceOauth2Token event identifies the credential provider, requested scopes, OAuth flow, portal execution role, and Region. Sensitive token and state values are redacted.
>
> {
>
> "eventSource": "bedrock-agentcore.amazonaws.com",
>
> "eventName": "GetResourceOauth2Token",
>
> "awsRegion": "ap-southeast-2",
>
> "userIdentity": {
>
> "type": "AssumedRole",
>
> "arn": "arn:aws:sts::111122223333:assumed-role/AmazonBedrockAgentCoreConsentPortalDefaultServiceRole-example/consent-dashboard-example"
>
> },
>
> "requestParameters": {
>
> "workloadIdentityToken": "HIDDEN_DUE_TO_SECURITY_REASONS",
>
> "resourceCredentialProviderName": "gateway-demo-github",
>
> "scopes": ["read:user", "repo"],
>
> "oauth2Flow": "USER_FEDERATION",
>
> "customState": "HIDDEN_DUE_TO_SECURITY_REASONS"
>
> },
>
> "resources": [
>
> {
>
> "accountId": "111122223333",
>
> "type": "AWS::BedrockAgentCore::OAuth2CredentialProvider",
>
> "ARN": "arn:aws:bedrock-agentcore:ap-southeast-2:111122223333:token-vault/default/oauth2credentialprovider/gateway-demo-github"
>
> }
>
> ],
>
> "managementEvent": true
>
> }
>
> For failures, use errorCode and errorMessage with the event time, assumed role, Region, credential provider, and requested scopes to identify the cause.
>
> Clean up
>
> When you no longer need the resources:
>
> Open the Amazon Bedrock AgentCore console and delete the Consent portal.
>
> Remove the portal callback URLs from the corporate IdP application and gateway targets.
>
> Delete the gateway targets that reference the outbound credential providers.
>
> Delete the outbound OAuth credential providers and corporate IdP credential provider if they aren’t used elsewhere.
>
> Delete the portal execution role if no other resource uses it.
>
> Note: Delete the gateway target before deleting its outbound credential provider. A credential provider still referenced by a target can’t be deleted.
>
> Conclusion
>
> The Amazon Bedrock AgentCore Consent portal gives administrators a managed way to configure end-user OAuth consent for an AgentCore Gateway. Administrators connect the corporate IdP, execution role, gateway, and outbound providers, and then share one URL. End users authenticate, review available providers, and grant consent individually. The portal handles the browser flow and managed session binding, while AgentCore Identity protects the resulting user tokens in the token vault.
>
> For end-to-end examples using Microsoft Entra ID and Okta, see the following Amazon Bedrock AgentCore samples on GitHub:
>
> Consent portal with authorization code flow targets
>
> AgentCore Gateway target using the OAuth authorization code flow
>
> To learn more, see Amazon Bedrock AgentCore.
>
> About the authors
>
> Swara Gandhi
>
> Swara is a Senior Solutions Architect on the AWS Identity Solutions team. She works on building secure and scalable end-to-end identity solutions. She is passionate about everything identity, security, and cloud.
>
> Satveer Khurpa
>
> Satveer is a Sr. WW Specialist Solutions Architect, Amazon Bedrock AgentCore at Amazon Web Services, specializing in agentic AI security with a focus on AgentCore Identity and Security. In this role, he uses his expertise in cloud-based architectures to help clients design and deploy secure agentic AI systems across diverse industries. Satveer applies his deep understanding of agentic AI patterns, identity and access management, and defense-in-depth security principles to architect scalable, secure, and responsible agent-based applications, enabling organizations to unlock new business opportunities while maintaining robust security postures for autonomous AI workloads.
>
> Eashan Kaushik
>
> Eashan is a Specialist Solutions Architect AI/ML at Amazon Web Services. He is driven by creating cutting-edge generative AI solutions while prioritizing a customer-centric approach to his work. Before this role, he obtained an MS in Computer Science from NYU Tandon School of Engineering. Outside of work, he enjoys sports, lifting, and running marathons.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。