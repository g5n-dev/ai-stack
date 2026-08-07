---
title: "How we built an MCP bridge to give our AgentCore-hosted AI agent access to local MCP tools"
date: 2026-08-06T08:12:05+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "Prompt 工程", "Amazon Bedrock AgentCore", "Expert (400)", "Technical How-to", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:1d6a2d534e3d1f93f0939047ee52fb6f313cadcd38de4d90025d5316631611e5"
source_payload_sha256: "sha256:368427593d3d14cc4e827a763c6f632b8952202b1950728d05e789f31b031dcd"
observation_id: obs_ea850b1a9c912609462a439893945e59b89d629abde9532c3a32b7330d6d6442
event_id: evt_7e34a8d244c347ecf649f2c734fe194a4fe30dbdd325b4a6870bffc1ca83823f
revision_id: rev_62cb956e20ff85b7eef2299b3633fe24fb0350f1491d94be65c61876e92a7ca3
source_published_at: 2026-08-05T18:02:23Z
first_seen_at: 2026-08-06T00:20:36Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 90
interpretation_sha256: "sha256:8c44ef58c46b386a05a231c59a743f54c851d38fa1ae68e7d2e85a28e207a8ec"
description: "这篇文章介绍了一种将云端托管的 AI 代理与本地 MCP 工具连接起来的桥接方案，通过浏览器扩展和本地代理组件转发消息，实现云端客户端对本地工具服务器的调用。"
external_url: https://aws.amazon.com/blogs/machine-learning/how-we-built-an-mcp-bridge-to-give-our-agentcore-hosted-ai-agent-access-to-local-mcp-tools
parent_observation_id: null
last_seen_at: 2026-08-07T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/how-we-built-an-mcp-bridge-to-give-our-agentcore-hosted-ai-agent-access-to-local-mcp-tools](https://aws.amazon.com/blogs/machine-learning/how-we-built-an-mcp-bridge-to-give-our-agentcore-hosted-ai-agent-access-to-local-mcp-tools)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么
这篇文章介绍了一种将云端托管的 AI 代理与本地 MCP 工具连接起来的桥接方案，通过浏览器扩展和本地代理组件转发消息，实现云端客户端对本地工具服务器的调用。

### 用在哪里
适用于需要在云端 AI 代理中调用本地工具的场景，特别是处理本地文件（如 Excel）时。该方案可以让远程 AI 服务在不离开用户设备的情况下访问本地数据和工具。

### 可以推断的
推测：该架构涉及多层消息转发，可能会引入额外的延迟，对实时性要求高的交互场景存在一定限制。
推测：采用 WebSocket 与本地消息机制组合的方式，说明该方案需要浏览器环境的支持，可能不适用于纯命令行或移动端场景。

## 来源摘要/节选

> Our agent runs in the cloud, but our users’ spreadsheets live on their laptops. How do you bridge that gap?
>
> The Model Context Protocol (MCP) is an open source standard introduced by Anthropic in November 2024 to standardize how AI models connect to external data and tools. MCP follows a client-server architecture where an MCP host, an AI application like Amazon Quick or Claude Code, establishes connections to one or more MCP servers. The MCP protocol supports two transport mechanisms: stdio (standard I/O for communication between local processes on the same machine) and streamable HTTP transport (HTTP-based communication between remote servers and clients). A missing piece is when the MCP server exists locally and the MCP client is remote.
>
> This pattern matters for financial managers and analysts who primarily work with Excel and local files. They can use centrally deployed AI agents to act on those files while also drawing context from their browser. This is the same pattern that powers products like Claude Cowork, a cloud agent calling local tools through MCP, but fully self-hosted on AWS with your own model and custom tool servers. Internally, we built a production-grade AI assistant for finance that has seen over 41,000 conversations within a year since launch.
>
> In this post, we recreate what we built internally in a simplified form. Our agent, deployed on Amazon Bedrock AgentCore, uses MCP servers that run on a user’s local machine. We bridge the gap between the remote MCP client and the local MCP server by tunneling MCP messages over WebSocket and native messaging. We discuss additional production hardening measures in the What’s Next section. The complete source code is available on GitHub.
>
> The MCP Bridge Demo extension summarizing a local Excel workbook. The cloud-hosted agent reads the file directly from the user’s machine through the MCP bridge and streams a structured summary back to the side panel
>
> Architecture overview
>
> The AgentCore runtime, a capability of Amazon Bedrock AgentCore, anchors an architecture with four components:
>
> AgentCore runtime: Hosts the Strands agent in the cloud. The agent acts as the MCP client, issuing tool discovery and tool invocation requests.
>
> Browser extension: Provides the chat interface and acts as a bidirectional relay, forwarding MCP messages between the AgentCore runtime (over WebSocket) and the MCP Bridge (over native messaging).
>
> MCP Bridge: A FastMCP proxy running on the user’s local machine, spawned by the browser through the native messaging host registration. It translates between the native messaging envelope format and raw MCP JSON-RPC.
>
> MCP Server: A standard MCP server running locally. Because the bridge is co-located, communication uses the stdio transport.
>
> The following diagram shows the end-to-end message flow. The user sends a message through the extension, which connects to the AgentCore runtime over a presigned WebSocket. When the Strands agent needs to call a tool, it sends an MCP JSON-RPC request wrapped in a JSON envelope back through the WebSocket to the extension. The extension relays the message as-is to the bridge through native messaging. The bridge unwraps the envelope, extracts the JSON-RPC content, and forwards it to the MCP server over stdio. The response travels the reverse path. The bridge wraps the unmodified MCP server response back into an envelope and relays it through the extension to the AgentCore runtime, where the agent consumes the tool result and continues generation.
>
> High-level architecture diagram showing all components. The browser extension and MCP Bridge act as relays that wrap and unwrap JSON messages from the AgentCore runtime and JSON-RPC messages from the MCP server
>
> The following table shows a single tool call as it travels from the agent to the MCP server, with each hop stripping one layer of wrapping:
>
> Hop
>
> Sender → Receiver
>
> Message
>
> 1
>
> Agent -&gt; Extension (WebSocket)
>
> {“type”: “mcpbridge”, “content”: {“type”: “mcp”, “payload”: “”}, “session_id”: “session_123”}
>
> 2
>
> Extension -&gt; Bridge (Native Messaging)
>
> {“type”: “mcp”, “payload”: “”}
>
> 3
>
> Bridge → MCP Server (stdio)
>
> {“jsonrpc”: “2.0”, “id”: 1, “method”: “tools/call”, “params”: {“name”: “read_sheet”, “arguments”: {“file_path”: “budget.xlsx”&#125;&#125;}
>
> How does the Strands agent work in AgentCore runtime
>
> WebSocket connection: The browser extension connects to the AgentCore runtime over a presigned WebSocket URL. On startup, the side panel sends a presign request through the background script to the native bridge, which uses the user’s local AWS credentials and the bedrock-agentcore software development kit (SDK) to generate a SigV4-signed wss:// URL scoped to the deployed runtime ARN (valid for 5 minutes). The side panel opens a WebSocket to that URL. No credentials ever leave the user’s machine or enter the browser. If the connection drops because of URL expiry or network interruption, the side panel automatically requests a fresh presigned URL after 2 seconds and reconnects, making the expiry window invisible to the user during normal use.
>
> MCP initialization: Before discovering tools, the agent performs the standard MCP initialization handshake. It sends an initialize request with the protocol version, waits for the server’s capabilities response, and then sends a notifications/initialized notification. Only after this handshake completes does the server accept tools/list and tools/call requests.
>
> Tool discovery: On each user message, the agent calls tools/list and receives an array of tool schemas. It wraps each schema into a Strands AgentTool whose stream() method sends a tools/call request through the bridge. Tools added to the MCP server are automatically available on the next request with no agent code changes.
>
> Request-response correlation: Each outbound JSON-RPC request from the agent is assigned a unique ID and registered against an asyncio.Future keyed by (session_id, jsonrpc_id). When the response arrives back over the WebSocket, it is matched to the waiting Future and resolved. This allows multiple tool calls to be in flight concurrently without ambiguity.
>
> How does native messaging work
>
> We need the extension to talk to a long-running local process without network permissions or per-message user prompts. Native messaging provides exactly this. Both Chrome and Firefox support native messaging for their extensions. The browser looks for a manifest file at a well-known location on the user’s machine that specifies which binary to launch. The native messaging manifest file for Chrome on macOS is as follows:
>
> # Stored at ~/Library/Application\ Support/Google/Chrome/NativeMessagingHosts/com.example.mcp_bridge.json
>
> {
>
> "name": "com.example.mcp_bridge",
>
> "description": "MCP Bridge - Routes MCP messages to local servers",
>
> "path": "/path/to/mcp-bridge-demo/bridge/run_bridge.sh",
>
> "type": "stdio",
>
> "allowed_origins": [
>
> "chrome-extension://&lt;extension_id&gt;/"
>
> ]
>
> }
>
> On extension startup, the background script calls chrome.runtime.connectNative("com.example.mcp_bridge") to launch the native app locally. The run_bridge.sh script referenced in the manifest activates the Python environment and starts the bridge:
>
> #!/bin/bash
>
> cd "/path/to/mcp-bridge-demo/bridge"
>
> source .venv/bin/activate
>
> exec python3 bridge.py
>
> The native messaging host process stays alive for the lifetime of the connection. Each message is serialized as JSON, UTF-8 encoded, and preceded with a 32-bit message length in little-endian byte order. The maximum size of a single message from the native messaging host is 1 MB (to protect the browser from misbehaving native applications). The maximum size of a message sent to the native messaging host is 64 MiB.
>
> How does the MCP Bridge work
>
> The MCP Bridge acts as a protocol translator between two worlds: Chrome’s native messaging protocol on one side and the MCP standard (JSON-RPC 2.0 over stdio) on the other. On the inbound path, it strips the 4-byte length header from stdin, parses the JSON body, and unwraps the envelope to extract the raw JSON-RPC message. On the outbound path, it does the reverse: wraps the JSON-RPC response in an envelope and writes it back with the length header. The JSON-RPC content itself passes through untouched.
>
> Internally, the bridge runs two concurrent loops connected through a FastMCP proxy. The main loop reads messages from the browser, unwraps them, and places the JSON-RPC content onto an input queue. The FastMCP proxy, started once and kept alive for the bridge’s lifetime, picks messages off this queue, forwards them to the MCP server subprocess over its stdin, and places responses from the server’s stdout onto an output queue. A second background loop reads from the output queue, wraps each response back into an envelope, and writes it to stdout for the browser to receive. This two-loop design decouples the browser’s request timing from the MCP server’s processing speed so the bridge does not block waiting for a slow tool to finish before accepting the next request.
>
> The MCP server itself is a child process spawned by the bridge on startup, configured through a mcp.json file. It stays running for the bridge’s lifetime with no per-request process overhead. Adding a new MCP server is a one-line config change. The bridge handles the plumbing.
>
> # mcp.json
>
> {
>
> "mcpServers": {
>
> "excel": {
>
> "command": "python3",
>
> "args": ["excel_server.py"]
>
> }
>
> }
>
> }
>
> Internal architecture of the MCP Bridge. The MCP Bridge translates messages from the browser extension into the MCP protocol for the MCP server. I/O queues work with a FastMCP proxy server to forward messages to the locally running MCP server and relay messages back to the browser extension
>
> Prerequisites
>
> The following prerequisites are needed to deploy and test the MCP bridge solution. These cover the browser extension, the agent deployed on AgentCore, the MCP Bridge, and a sample Excel MCP server.
>
> AWS account and permissions
>
> AWS account with Bedrock model access enabled (the code uses Claude Opus 4.7). Model availability varies by Region. See the Amazon Bedrock model availability documentation for the current list.
>
> AWS Identity and Access Management (IAM) permissions for Bedrock AgentCore (bedrock-agentcore:*), AWS CloudFormation, IAM role creation, and S3.
>
> AWS Command Line Interface (AWS CLI) configured with credentials (aws sts get-caller-identity to verify).
>
> AWS Cloud Development Kit (AWS CDK) bootstrapped in your target Region (cdk bootstrap).
>
> Tools and software
>
> Python 3.10+.
>
> Node.js 20+ (for the AgentCore command line interface (CLI)).
>
> Google Chrome (Manifest V3 side panel support).
>
> Git.
>
> Install
>
> AgentCore CLI: npm install -g @aws/agentcore.
>
> AWS CDK: npm install -g aws-cdk.
>
> Estimated time and cost
>
> Setup: ~15 minutes (deploy, install extension, and register bridge).
>
> AgentCore runtime: pay-per-invocation (no idle cost).
>
> Bedrock model usage: standard per-token pricing for Claude.
>
> Other components run locally at no additional cost.
>
> Deploying the solution
>
> Clone the repository.
>
> git clone https://github.com/aws-samples/sample-mcp-bridge-agentcore.git
>
> cd mcp-bridge-demo
>
> Install Python dependencies.
>
> chmod +x scripts/setup.sh manifests/install.sh
>
> ./scripts/setup.sh
>
> Create and deploy the agent to AgentCore.
>
> npm install -g @aws/agentcore
>
> cd agent
>
> agentcore create --name McpBridgeAgent --defaults
>
> cd McpBridgeAgent
>
> cp ../agent.py app/McpBridgeAgent/main.py
>
> cp ../mcp_bridge_transport.py app/McpBridgeAgent/
>
> agentcore deploy
>
> Note the runtime Amazon Resource Name (ARN) from the output (or run agentcore status).
>
> Configure the bridge.Edit bridge/bridge_config.json with your runtime ARN:
>
> {
>
> "runtime_arn": "arn:aws:bedrock-agentcore:&lt;region&gt;:&lt;account-id&gt;:runtime/&lt;your-runtime&gt;",
>
> "region": "us-east-1",
>
> "presign_expires": 300
>
> }
>
> The bridge uses your local AWS credentials to generate presigned WebSocket URLs automatically, with no manual token management needed.
>
> Load the Chrome extension.
>
> Navigate to chrome://extensions.
>
> Turn on Developer mode.
>
> Choose Load unpacked, and then select the extension/ directory.
>
> Note the extension ID displayed on the card.
>
> Register the native messaging bridge.
>
> ./manifests/install.sh &lt;your-extension-id&gt;
>
> This creates a launcher script and registers it with Chrome so the browser can spawn the bridge process.
>
> Testing the solution
>
> Restart the browser and choose the extension icon to open the side panel. The extension automatically requests a presigned URL from the bridge, connects to AgentCore, and discovers available MCP tools.
>
> The browser extension connects to the MCP bridge over native messaging and relays MCP messages between the AgentCore-hosted agent and the side panel, as shown in the extension’s DevTools console
>
> Additional queries to experiment with:
>
> "Create a workbook called budget.xlsx with sheets Q1 and Q2"
>
> "Write 'Revenue' in cell A1 of the Q1 sheet in budget.xlsx"
>
> "Read the data from budget.xlsx"
>
> Security considerations
>
> This post prioritizes demonstrating the MCP bridge functionality and therefore limits security measures to the following:
>
> Native messaging origin restriction: Chrome checks the calling extension’s ID against the allowed_origins list in the native messaging manifest and rejects connections from extensions not explicitly listed.
>
> Presigned URL expiration: WebSocket URLs are SigV4-signed and expire after 5 minutes. Credentials remain on the user’s machine and are not sent to the browser.
>
> Process isolation: The extension, bridge, and MCP server each run in separate operating system processes with no shared memory.
>
> The primary exposure surface unique to this architecture is the bridge itself. It accepts instructions from a cloud-hosted agent and runs them locally with the user’s file system permissions. The key principle is that the agent should not have more access than the user explicitly grants, and the user can always see what tools were invoked and with what arguments.
>
> For a production system, in addition to implementing Amazon Bedrock Guardrails for content filtering, we recommend the following additional security measures:
>
> Layer
>
> What to add
>
> Why
>
> Authentication
>
> Require a JSON Web Token (JWT) handshake as the first WebSocket frame. Verify the token (for example, through Amazon Cognito and an HMAC secret in AWS Systems Manager) before accepting messages.
>
> Helps prevent unauthorized use even if a presigned URL is leaked.
>
> Payload signing
>
> Sign every MCP message with Ed25519 (private key on the agent, public key on the bridge). Reject unsigned or tampered payloads.
>
> Makes sure messages were not modified in transit between cloud and local machine.
>
> File system scoping
>
> Configure an explicit allowlist of directories the MCP server can access. Reject paths outside the boundary.
>
> Helps prevent a prompt injection from tricking the agent into reading sensitive files (SSH keys, credentials).
>
> Audit logging
>
> Log every tool invocation (tool name, arguments, timestamp, result status) to a local file.
>
> Provides traceability for what the agent did on the user’s machine.
>
> Clean up
>
> When you’re done experimenting, remove the deployed resources to avoid ongoing charges.
>
> Remove the AgentCore deployment. Tear down the CloudFormation stack, IAM roles, and runtime resources.
>
> cd agent/McpBridgeAgent
>
> agentcore remove all
>
> agentcore deploy
>
> Unregister the native messaging bridge.
>
> rm ~/Library/Application\ Support/Google/Chrome/NativeMessagingHosts/com.example.mcp_bridge.json
>
> Remove the Chrome extension.
>
> Navigate to chrome://extensions.
>
> Choose Remove on the MCP Bridge Demo card.
>
> Delete local files (optional).
>
> rm -rf mcp-bridge-demo/
>
> What’s next
>
> Our internal production solution includes the capabilities that follow. The MCP Bridge acts as the AgentCore-hosted agent’s window into the user’s local system. Combined with the browser extension, the current architecture can be extended to support more use cases.
>
> Browser actions
>
> The browser extension can implement its own browser tools modeled on Playwright MCP’s tool definitions and expose them to the agent to perform actions such as clicking elements, filling forms, navigating pages, and taking screenshots.
>
> Because the extension sits as a message relay between the AgentCore agent and the MCP Bridge, it can intercept tools/list and tools/call MCP messages, inject the browser tools into the tool list, and handle their execution locally.
>
> Local tool automation
>
> The bridge speaks standard MCP JSON-RPC over stdio, so MCP servers that use the stdio transport are compatible without modification. Add an entry to mcp.json. Examples: filesystem access for sandboxed file read/write, Git for repository operations, memory for persistent local knowledge graphs. See awesome-mcp-servers for a directory of available servers.
>
> Packaging the bridge as a standalone binary
>
> For production distribution, we use PyInstaller to package the bridge into a standalone binary that bundles the Python runtime, dependencies, and configuration into a single executable. The native messaging manifest points directly at this binary, so users do not need to install Python or manage virtual environments. The bridge works on first extension launch with no extra setup.
>
> Conclusion
>
> In this post, we built an MCP bridge that connects a cloud-hosted Strands agent on Amazon Bedrock AgentCore to local MCP tool servers running on a user’s machine. Using a browser extension as the relay layer and Chrome’s native messaging as the local transport, we tunneled standard MCP JSON-RPC messages between the cloud and the user’s file system without exposing credentials to the browser or modifying the MCP protocol itself.
>
> With this pattern, you can keep your agent centrally deployed and managed while giving it access to tools that must run locally, such as Excel files, Git repositories, or other locally running MCP servers. The architecture is extensible. You can add new tools with a one-line config change, layer in browser actions through the extension, or package the bridge as a standalone binary for frictionless distribution.
>
> To get started, deploy the sample repository and experiment with your own MCP servers. For more on the services used in this post, explore the Amazon Bedrock AgentCore documentation, the Strands Agents SDK, and the Model Context Protocol specification.
>
> Thanks to Daniel Sheng Sun, Markus Hueck, Nishant Bisen, Shraddha Kabade, and Stacy Kim for their contributions to the internal production system that inspired this post.
>
> About the author
>
> Rohan Lekhwani
>
> Rohan is a Software Engineer at Amazon Devices and Services Finance where he leads Ask Rino, an agentic AI assistant for finance, and built the first MCP server infrastructure within Amazon DaS Finance. He has experience building and scaling agentic AI systems, MCPs, and large-scale conversational AI apps, and previously led the UMass Amherst team to a top-10 finish in the Amazon Alexa Prize, deploying to all US Alexa devices. In his spare time, he likes to run and work on open source projects.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。