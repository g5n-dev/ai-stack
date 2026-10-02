---
title: "Add secure Web Search to Claude Desktop with Amazon Bedrock AgentCore"
date: 2026-10-02T23:51:49+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "Advanced (300)", "Amazon Bedrock", "Amazon Bedrock AgentCore", "Technical How-to", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:775b2426450f5329220d0ca6e7e93f573b8d477e7e732e6e30c3da0199801ad1"
source_payload_sha256: "sha256:2026eec9ff7ef41d4ba6a07c494e41068b58c2daac0446b886f624985d88a6b6"
observation_id: obs_236dbb8238cdf625118730f1fcaab635d506047f0e13b256b9809f63993bc86d
event_id: evt_05bf1fcc65dc6a78a760429c3098ef191e2f804e2bbf25ec8c17711d329596bf
revision_id: rev_31c68a42e61aa7786ef26b34b7806ffdf91d43af916b18d46fe808904f78dcae
source_published_at: 2026-10-02T15:46:05Z
first_seen_at: 2026-10-02T16:01:57Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 69
interpretation_sha256: "sha256:d66324249872ed69b54ef50edc450cae8290d0419c42ea7d476e217ff877b379"
description: "该内容介绍如何通过 Amazon Bedrock AgentCore Gateway 将 Web Search 能力接入 Claude Desktop，并使用基于 JWT 的认证机制保障通信安全，整个认证链路涉及 IAM Identity Center、Amazon Cognito 等 AWS 服务。"
external_url: https://aws.amazon.com/blogs/machine-learning/add-secure-web-search-to-claude-desktop-with-amazon-bedrock-agentcore
parent_observation_id: null
last_seen_at: 2026-10-02T15:48:39.627944Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/add-secure-web-search-to-claude-desktop-with-amazon-bedrock-agentcore](https://aws.amazon.com/blogs/machine-learning/add-secure-web-search-to-claude-desktop-with-amazon-bedrock-agentcore)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么
该内容介绍如何通过 Amazon Bedrock AgentCore Gateway 将 Web Search 能力接入 Claude Desktop，并使用基于 JWT 的认证机制保障通信安全，整个认证链路涉及 IAM Identity Center、Amazon Cognito 等 AWS 服务。

### 用在哪里
适用于已在 AWS 环境部署 Claude Desktop、需要模型获取实时信息但要求所有流量保持在 AWS 边界内的企业用户，尤其是已有 IAM Identity Center 单点登录体系的组织。

### 可以推断的
推测：在企业 AI 应用场景中，安全与合规是关键约束，认证流程越贴近现有身份体系，落地成本越低。  
推测：Web Search 作为托管服务提供，意味着运维工作量转移至云厂商，用户只需关注集成与业务逻辑。

## 来源摘要/节选

> Claude Desktop on Amazon Bedrock provides powerful AI assistance, but without integrated web search, responses are limited to the model’s training knowledge cutoff. When you need current information, such as recent documentation updates, live pricing, or weather updates, the model can’t retrieve it on its own.
>
> Amazon Bedrock AgentCore is a platform to build, connect, and optimize agents at scale, with any framework or model. With AgentCore Gateway, a capability of Amazon Bedrock AgentCore, you can close this knowledge cutoff gap by connecting Claude Desktop to Web Search. Web Search is a fully managed, Model Context Protocol (MCP)-compatible web search capability backed by an Amazon web index that spans tens of billions of documents. All query traffic stays within AWS infrastructure, with no external API keys to manage and no queries leaving your boundary.
>
> With Claude Desktop, you can use managed MCP servers to connect to an AgentCore Gateway with the Web Search target enabled. In this post, we walk through the steps to set up this integration and use JSON Web Token (JWT)-based inbound authentication to secure the communication.
>
> Architecture
>
> Many enterprises running on AWS use AWS IAM Identity Center for single sign-on (SSO) access to their AWS accounts. In this walkthrough, we use AWS IAM Identity Center as the authentication source for the AgentCore Gateway. With this setup, Claude Desktop on Amazon Bedrock can invoke Web Search through a trusted, enterprise-managed identity flow. This approach aligns with existing organizational identity governance. No separate credentials or third-party identity providers are required.
>
> To bridge AWS IAM Identity Center with the AgentCore Gateway JWT-based authentication, we use Amazon Cognito as a federation layer with the OAuth 2.0 authorization code grant flow. IAM Identity Center handles user authentication through Security Assertion Markup Language (SAML). Amazon Cognito issues JWTs, and the AgentCore Gateway validates them on each request. The entire authentication chain stays within AWS.
>
> The following sequence diagram illustrates this authentication flow.
>
> Figure 1: User authentication and authorization sequence diagram
>
> Prerequisites
>
> To follow along with the steps in this post, you need the following:
>
> An AWS account with permissions to create AWS Identity and Access Management (IAM) roles and Amazon Bedrock AgentCore resources.
>
> Admin access to your management account in AWS Organizations (for AWS IAM Identity Center configuration).
>
> AWS IAM Identity Center preconfigured for SSO access to AWS accounts.
>
> Claude Desktop set up with Amazon Bedrock as the inference provider.
>
> The AWS Command Line Interface (AWS CLI) v2 installed and configured.
>
> Python 3.10 or later.
>
> The Boto3 SDK updated to the latest version.
>
> Web Search on Amazon Bedrock AgentCore is currently available in the US East (N. Virginia) AWS Region (us-east-1), Europe (Ireland) Region (eu-west-1), and Asia Pacific (Tokyo) Region (ap-northeast-1). Verify that your gateway is created in one of these Regions.
>
> Configuration
>
> The configuration involves setting up the authentication chain (AWS IAM Identity Center to Amazon Cognito to JWT) and then wiring the AgentCore Gateway into Claude Desktop. We walk through each step in the following section.
>
> Step 1: Create an Amazon Cognito user pool
>
> In your target AWS account, create an Amazon Cognito user pool that will serve as the OpenID Connect (OIDC) token issuer for the AgentCore Gateway.
>
> export AWS_REGION=&lt;your-region&gt;
>
> # Create User Pool
>
> aws cognito-idp create-user-pool \
>
> --pool-name "agentcore-websearch-pool" \
>
> --region $AWS_REGION \
>
> --auto-verified-attributes email \
>
> --schema '[{"Name":"email","Required":true,"Mutable":true,"AttributeDataType":"String"}]' \
>
> --username-attributes email \
>
> --username-configuration "CaseSensitive=false" \
>
> --mfa-configuration "OFF"
>
> # Note the Pool ID
>
> export USER_POOL_ID=$(aws cognito-idp list-user-pools --max-results 10 \
>
> --region $AWS_REGION \
>
> --query "UserPools[?Name=='agentcore-websearch-pool'].Id" --output text)
>
> echo "User Pool ID: $USER_POOL_ID"
>
> # Create a domain (must be globally unique)
>
> aws cognito-idp create-user-pool-domain \
>
> --domain "&lt;your-unique-prefix&gt;" \
>
> --user-pool-id $USER_POOL_ID \
>
> --region $AWS_REGION
>
> Save these values for later steps:
>
> User Pool ID: $USER_POOL_ID.
>
> Domain: &lt;your-unique-prefix&gt;.auth.&lt;region&gt;.amazoncognito.com.
>
> Audience: urn:amazon:cognito:sp:&lt;user-pool-id&gt;.
>
> ACS URL: https://&lt;your-unique-prefix&gt;.auth.&lt;region&gt;.amazoncognito.com/saml2/idpresponse.
>
> Step 2: Configure IAM Identity Center SAML application
>
> In your AWS Organizations management account, create a SAML application that federates with Cognito:
>
> Open IAM Identity Center console.
>
> Choose Applications, Add application, I have an application I want to set up, SAML 2.0, and then Next.
>
> Fill in the following details:
>
> Display name: AgentCore Web Search.
>
> Select Manually type your metadata value.
>
> ACS URL: https://&lt;your-unique-prefix&gt;.auth.&lt;region&gt;.amazoncognito.com/saml2/idpresponse.
>
> Audience: urn:amazon:cognito:sp:&lt;user-pool-id&gt;.
>
> Download the SAML metadata XML file and choose Submit.
>
> After the application is created, edit the attribute mappings and insert the following values:
>
> Subject, ${user:subject}, Format: Persistent.
>
> Email, ${user:email}, Format: Basic.
>
> Assign the users or groups that would have access to Web Search.
>
> Step 3: Wire SAML IdP into Cognito
>
> Back in the target account, register IAM Identity Center as a SAML identity provider in your Cognito user pool:
>
> # Add IAM Identity Center as SAML IdP
>
> METADATA=$(cat /path/to/downloaded-metadata.xml)
>
> aws cognito-idp create-identity-provider \
>
> --user-pool-id $USER_POOL_ID \
>
> --provider-name "IAMIdentityCenterIdP" \
>
> --provider-type SAML \
>
> --provider-details "{\"MetadataFile\": $(echo "$METADATA" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))')}" \
>
> --attribute-mapping '{"email": "email"}' \
>
> --region $AWS_REGION
>
> Step 4: Create Cognito app client for Amazon Bedrock AgentCore
>
> Create an app client with a client secret. Claude Desktop uses this client to initiate the OAuth flow, which authenticates the user through IAM Identity Center and obtains a JWT for the AgentCore Gateway:
>
> aws cognito-idp create-user-pool-client \
>
> --user-pool-id $USER_POOL_ID \
>
> --client-name "agentcore-websearch-client" \
>
> --generate-secret \
>
> --supported-identity-providers "IAMIdentityCenterIdP" \
>
> --callback-urls '["http://localhost:53280/callback"]' \
>
> --allowed-o-auth-flows code \
>
> --allowed-o-auth-scopes "openid" "email" "profile" \
>
> --allowed-o-auth-flows-user-pool-client \
>
> --region $AWS_REGION
>
> Note the Client ID and Client Secret from the output. These are your application client ID and secret.
>
> Step 5: Configure AgentCore Gateway with Web Search tool
>
> In this step, we create a new AgentCore Gateway with Inbound Auth Type as JSON Web Tokens (JWT). For this configuration, we use the Cognito user pool ID and application client ID that were created in the prior steps.
>
> Run the following Python script to create the gateway with the required configurations, replacing all placeholders with actual values from your environment.
>
> import boto3
>
> import json
>
> import time
>
> session = boto3.Session(region_name="your-region")
>
> iam_client = session.client("iam")
>
> gateway_client = session.client("bedrock-agentcore-control")
>
> ACCOUNT_ID = "your-target-aws-account-id"
>
> ROLE_NAME = "websearch-gateway-role"
>
> GATEWAY_NAME = "websearch-gateway"
>
> COGNITO_DISCOVERY_URL = "https://cognito-idp.&lt;your-region&gt;.amazonaws.com/&lt;user-pool-id&gt;/.well-known/openid-configuration"
>
> COGNITO_CLIENT_ID = "&lt;cognito-application-client-id&gt;"
>
> # --- Step 1: Create IAM execution role ---
>
> trust_policy = {
>
> "Version": "2012-10-17",
>
> "Statement": [{
>
> "Effect": "Allow",
>
> "Principal": {"Service": "bedrock-agentcore.amazonaws.com"},
>
> "Action": "sts:AssumeRole",
>
> "Condition": {
>
> "StringEquals": {"aws:SourceAccount": ACCOUNT_ID}
>
> }
>
> }]
>
> }
>
> permissions_policy = {
>
> "Version": "2012-10-17",
>
> "Statement": [
>
> {
>
> "Sid": "GetGateway",
>
> "Effect": "Allow",
>
> "Action": "bedrock-agentcore:GetGateway",
>
> "Resource": f"arn:aws:bedrock-agentcore:us-east-1:{ACCOUNT_ID}:gateway/*"
>
> },
>
> {
>
> "Sid": "GetConfigBundle",
>
> "Effect": "Allow",
>
> "Action": "bedrock-agentcore:GetConfigurationBundleVersion",
>
> "Resource": f"arn:aws:bedrock-agentcore:us-east-1:{ACCOUNT_ID}:configuration-bundle/*"
>
> },
>
> {
>
> "Sid": "InvokeWebSearch",
>
> "Effect": "Allow",
>
> "Action": "bedrock-agentcore:InvokeWebSearch",
>
> "Resource": "arn:aws:bedrock-agentcore:us-east-1:aws:tool/web-search.v1"
>
> }
>
> ]
>
> }
>
> try:
>
> iam_client.create_role(
>
> RoleName=ROLE_NAME,
>
> AssumeRolePolicyDocument=json.dumps(trust_policy),
>
> Description="Execution role for web search AgentCore gateway",
>
> )
>
> print(f"✓ Role '{ROLE_NAME}' created.")
>
> except iam_client.exceptions.EntityAlreadyExistsException:
>
> print(f"✓ Role '{ROLE_NAME}' already exists, reusing.")
>
> iam_client.put_role_policy(
>
> RoleName=ROLE_NAME,
>
> PolicyName="websearch-gateway-policy",
>
> PolicyDocument=json.dumps(permissions_policy),
>
> )
>
> print(f"✓ Inline policy attached to '{ROLE_NAME}'.")
>
> # --- Step 2: Create the gateway ---
>
> response = gateway_client.create_gateway(
>
> name=GATEWAY_NAME,
>
> description="AgentCore gateway with managed Web Search connector",
>
> roleArn=f"arn:aws:iam::{ACCOUNT_ID}:role/{ROLE_NAME}",
>
> protocolType="MCP",
>
> protocolConfiguration={
>
> "mcp": {
>
> "supportedVersions": ["2025-03-26"],
>
> }
>
> },
>
> authorizerType="CUSTOM_JWT",
>
> authorizerConfiguration={
>
> "customJWTAuthorizer": {
>
> "discoveryUrl": COGNITO_DISCOVERY_URL,
>
> "allowedClients": [COGNITO_CLIENT_ID],
>
> }
>
> },
>
> )
>
> gateway_id = response["gatewayId"]
>
> gateway_url = response.get("gatewayUrl")
>
> print(f"✓ Gateway created: {gateway_id}")
>
> print(f" URL: {gateway_url}")
>
> # --- Step 3: Wait for gateway to become READY ---
>
> print(" Waiting for gateway to reach READY status...", end="", flush=True)
>
> for i in range(40): # up to ~10 minutes
>
> resp = gateway_client.get_gateway(gatewayIdentifier=gateway_id)
>
> status = resp.get("status")
>
> if status == "READY":
>
> print(f" READY (after {(i+1)*15}s)")
>
> break
>
> elif status == "FAILED":
>
> print(f"\n✗ Gateway entered FAILED status.")
>
> reasons = resp.get("statusReasons", [])
>
> for r in reasons:
>
> print(f" Reason: {r}")
>
> exit(1)
>
> print(".", end="", flush=True)
>
> time.sleep(15)
>
> else:
>
> print(f"\n✗ Gateway did not reach READY within 10 minutes (last status: {status})")
>
> exit(1)
>
> # --- Step 4: Attach the managed Web Search connector target ---
>
> gateway_client.create_gateway_target(
>
> gatewayIdentifier=gateway_id,
>
> name="web-search-tool",
>
> description="Managed Web Search connector",
>
> targetConfiguration={
>
> "mcp": {
>
> "connector": {
>
> "source": {"connectorId": "web-search"},
>
> "configurations": [{"name": "WebSearch", "parameterValues": {&#125;&#125;],
>
> }
>
> }
>
> },
>
> credentialProviderConfigurations=[
>
> {"credentialProviderType": "GATEWAY_IAM_ROLE"}
>
> ],
>
> )
>
> print("✓ Web search target attached.")
>
> print()
>
> print("=" * 60)
>
> print(f" Gateway ID: {gateway_id}")
>
> print(f" Gateway URL: {gateway_url}")
>
> print(f" Auth: CUSTOM_JWT (Cognito)")
>
> print(f" Target: web-search (managed connector)")
>
> print("=" * 60)
>
> You now have an AgentCore Gateway with Web Search tool, with JWT-based inbound authorization.
>
> Step 6: Configure Claude Desktop
>
> Use the steps in the Claude Desktop configuration documentation to access the configuration window for Claude Desktop with Amazon Bedrock. After you open it, choose Connectors and Extensions, then choose Add server, and then choose Blank.
>
> The following screenshot shows the configuration window with these options.
>
> Figure 2: Claude Desktop connector configuration window
>
> Enter the following details:
>
> Name: websearchtool.
>
> Transport: Streamable HTTP.
>
> URL: Enter the gateway resource URL for the AgentCore Gateway created in Step 5.
>
> OAuth: Bring your own client.
>
> Client ID: Enter the client ID for the app client created in Step 4.
>
> Client Secret: Enter the client secret for the app client created in Step 4.
>
> Authorization Server: Enter ["https://&lt;your-unique-prefix&gt;.auth.&lt;region&gt;.amazoncognito.com/oauth2/authorize"].
>
> Scope: openid.
>
> Callback host: localhost.
>
> Callback port: 53280.
>
> When you’re done, choose sign in and test. This should open a browser for you to authenticate, redirecting you to your AWS IAM Identity Center SSO login. Enter your credentials to authenticate. If successful, you should see a message such as, “Authorization complete. You can close this tab and return to Claude.”
>
> Back in Claude Desktop, you should see a successful MCP registration message like in the following image.
>
> Figure 3: Successful MCP server registration in Claude Desktop
>
> Claude Desktop will now discover the WebSearchTool through the MCP tools/list call. It invokes the tool automatically whenever the model needs current information from the web.
>
> Testing and validation
>
> In your preferred interface (for example, Chat or Cowork), send a query that requires Claude Desktop to retrieve the latest results. You should see a tool execution approval box, indicating that Claude has successfully discovered the Web Search tool. On approval, you should see the web search results included in the response.
>
> Figure 4: Web Search tool execution approval dialog
>
> The dialog shows the query Claude wants to run and offers three options: Deny, Allow for this task, or Allow once. On approval, Web Search results are included in the response.
>
> Clean up
>
> If you created resources while following along, perform the following steps to delete them:
>
> # Delete the gateway target
>
> aws bedrock-agentcore-control delete-gateway-target --gateway-identifier &lt;gateway-id&gt; --target-id &lt;target-id&gt; --region $AWS_REGION
>
> # Delete the gateway (only if it was created for this walkthrough)
>
> aws bedrock-agentcore-control delete-gateway --gateway-identifier &lt;gateway-id&gt; --region $AWS_REGION
>
> # Delete the IAM policy (only if it was created for this walkthrough)
>
> aws iam delete-role-policy --role-name websearch-gateway-role --policy-name websearch-gateway-policy
>
> # Delete the IAM role (only if it was created for this walkthrough)
>
> aws iam delete-role --role-name websearch-gateway-role
>
> # Delete the Cognito application client
>
> aws cognito-idp delete-user-pool-client --user-pool-id $USER_POOL_ID --client-id &lt;client-id&gt; --region $AWS_REGION
>
> # Delete the Cognito identity provider
>
> aws cognito-idp delete-identity-provider --user-pool-id $USER_POOL_ID --provider-name IAMIdentityCenterIdP --region $AWS_REGION
>
> # Delete the Cognito pool domain
>
> aws cognito-idp delete-user-pool-domain --user-pool-id $USER_POOL_ID --domain &lt;your-unique-prefix&gt; --region $AWS_REGION
>
> # Delete the cognito pool
>
> aws cognito-idp delete-user-pool --user-pool-id $USER_POOL_ID --region $AWS_REGION
>
> Finally, in the IAM Identity Center console in the management account, delete the SAML application you created in Step 2.
>
> Conclusion
>
> In this post, we walked through integrating Web Search on AgentCore with Claude Desktop. While this walkthrough uses AWS IAM Identity Center as the identity provider, the same pattern works with any SAML or OIDC-compatible identity provider. You can substitute your existing IdP by configuring it as a federation source in Amazon Cognito. This approach closes the web search gap without introducing third-party dependencies, and all queries stay within your AWS boundary.
>
> To get started, follow the steps above to set up the integration in your own environment. For advanced gateway configurations, see the AgentCore Gateway Developer Guide. To learn more about Web Search, see the Web Search documentation.
>
> About the author
>
> Jishnu Dasgupta
>
> Jishnu is a Solutions Architect at AWS who specializes in manufacturing and automotive domain. His focus areas are building, migrating and modernizing applications on AWS. He leverages his expertise and experience to help AWS customers build optimized, scalable and fit to purpose architecture on AWS.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。