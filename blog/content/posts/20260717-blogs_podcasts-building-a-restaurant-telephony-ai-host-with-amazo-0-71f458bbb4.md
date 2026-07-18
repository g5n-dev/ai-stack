---
title: "Building a restaurant telephony AI host with Amazon Bedrock AgentCore and Amazon Nova 2 Sonic"
date: 2026-07-17T00:45:57+08:00
draft: false
entry_kind: "auto"
tags: ["Amazon API Gateway", "Amazon Bedrock AgentCore", "Amazon DynamoDB", "AWS Fargate", "AWS Lambda", "Elastic Load Balancing", "Expert (400)", "Technical How-to"]
categories: []
source: "blogs_podcasts"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:845e3464ebeac68162339bd31417e056712beb93ce3f362ab2ab227388c37290"
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 93
description: "当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。"
external_url: https://aws.amazon.com/blogs/machine-learning/building-a-restaurant-telephony-ai-host-with-amazon-bedrock-agentcore-and-amazon-nova-2-sonic
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/building-a-restaurant-telephony-ai-host-with-amazon-bedrock-agentcore-and-amazon-nova-2-sonic](https://aws.amazon.com/blogs/machine-learning/building-a-restaurant-telephony-ai-host-with-amazon-bedrock-agentcore-and-amazon-nova-2-sonic)

## 来源摘要/节选

> Restaurants miss an average of 150 phone calls per location every month, and about 60 percent of those are customers trying to place an order or book a table. Most of these calls come in during dinner service, exactly when the host is seating guests, servers are turning tables, and the phone becomes an afterthought. Pulling someone off the floor to answer doesn’t fix the problem. It only makes two experiences worse. Adding an app or a website helps customers who prefer to order online, but it does nothing for the person who only wants to call.
>
> In this post, we show you how to build a voice ordering system that answers a phone number and takes the order from greeting to confirmation. The system uses Amazon Bedrock AgentCore to host and run the agent and Amazon Nova 2 Sonic for real-time speech, connected to a restaurant backend through the Model Context Protocol (MCP). The walkthrough covers deploying the full stack with AWS Cloud Development Kit (AWS CDK) and bridging a phone call into the agent through a Session Initiation Protocol (SIP) gateway on Amazon Elastic Container Service (Amazon ECS) and AWS Fargate. It also warms the agent session while the phone is still ringing, so the caller never hears dead air.
>
> Solution overview
>
> The system has three layers. The telephony layer handles phone-specific concerns. Audio arrives over the phone network rather than a browser, and the system identifies the caller by phone number rather than by a login. A SIP gateway streams that audio to the agent layer over a signed WebSocket connection, where the agent runs the conversation with Amazon Nova 2 Sonic. The agent reaches the backend layer through MCP tools. The backend holds the menu, carts, orders, and locations. Keeping these layers apart means the ordering logic stays independent from the channel that calls it. A new channel like a mobile app or a kiosk can connect to the same agent without rewriting the backend. And because MCP is an open standard for connecting an agent to external tools, the backend can change without touching the agent. The agent supports both text and audio as input and output, handling transcription, turn-taking, and interruptions in a single bidirectional stream.
>
> The solution deploys the following:
>
> On the telephony side, Amazon Chime SDK Voice Connector provides the SIP trunk and toll-free number that accepts inbound calls. Amazon ECS on AWS Fargate runs the SIP gateway behind a Network Load Balancer. For the agent layer, AgentCore Runtime hosts the conversation logic, with each call running in its own microVM for isolation. Amazon Nova 2 Sonic handles the speech-to-speech interaction. AgentCore Gateway exposes the backend APIs as MCP tools the agent can discover and call by name. The backend layer uses Amazon API Gateway to front REST endpoints secured by AWS Identity and Access Management (IAM). AWS Lambda runs the business logic for menus, carts, orders, and location lookups. Amazon DynamoDB stores the data, and Amazon Location Service handles geocoding and route calculation. Amazon Elastic Container Registry (Amazon ECR), AWS CodeBuild, and Amazon Simple Storage Service (Amazon S3) build and store the agent container image.
>
> Architecture diagram
>
> The following diagram shows the solution, which is organized into four sections.
>
> The restaurant’s backend infrastructure deploys first in Section A. Amazon DynamoDB holds the customer, order, menu, cart, and location data, and Amazon Location Service handles addresses and routing. AWS Lambda runs the business logic, and Amazon API Gateway exposes it externally with IAM authorization. Resources deploy in dependency order.
>
> Section B creates the AgentCore Gateway, sets up its IAM permissions, and configures the gateway to expose the backend endpoints as agent-accessible MCP tools. This is the layer that decouples the agent from the backend. Without it, adding or changing a tool would require redeploying the agent itself.
>
> Section C provisions the agent. It creates the Amazon ECR repository and uses Amazon S3 and AWS CodeBuild to build and push the container image. It then deploys AgentCore Runtime. It also deploys the supporting pieces that let the agent personalize each call, including a prompt-renderer Lambda function and a set of AWS Systems Manager Parameter Store entries that hold the prompt templates and a secret used for caller identification.
>
> Section D provisions the phone path. It sets up the Amazon Chime SDK Voice Connector and a toll-free number, a SIP Media Application Lambda that decides what to do with an incoming call, a shared Amazon Virtual Private Cloud (Amazon VPC), and the SIP gateway (drachtio-server), which runs on Amazon ECS on AWS Fargate behind a Network Load Balancer. The gateway bridges the calls between the Chime SDK Voice Connector and AgentCore Runtime.
>
> The numbered callouts in the preceding diagram trace the solution end to end:
>
> A call is initiated to the phone number provisioned by Amazon Chime SDK, either by a customer or forwarded from another line.
>
> Amazon Chime SDK answers the call and invokes AWS Lambda to set up the bridge.
>
> The Lambda creates a session identifier and opens a connection to AgentCore Runtime to warm up the microVM, which avoids a cold start when media streaming begins.
>
> After a successful response from the Lambda, Amazon Chime SDK initiates a bridge action against the Network Load Balancer by sending a SIP invite over TCP port 5060.
>
> The SIP service running on AWS Fargate accepts the invite and allocates a free port in the Real-time Transport Protocol (RTP) service on the same container to receive media on the assigned public IP address.
>
> The RTP service receives the media on the UDP port from the Voice Connector and connects to the AgentCore Runtime WebSocket to begin media translation, using the same session identifier created by the SIP Media Application handler.
>
> AgentCore Runtime invokes an AWS Lambda function to build the system prompt, stored on AWS Systems Manager Parameter Store, based on the session identifier and the customer’s Amazon DynamoDB record.
>
> AgentCore Runtime creates a session with Amazon Nova 2 Sonic and greets the customer over the established connection, following the system prompt instructions.
>
> AgentCore Runtime lists and calls the available tools from AgentCore Gateway using the MCP protocol.
>
> AWS CDK deploys the solution to Amazon S3, triggering AWS CodeBuild to build the container images and store them in Amazon ECR. AgentCore Runtime and AWS Fargate use these images to deploy the agent and the SIP and RTP servers.
>
> Amazon CloudWatch provides centralized monitoring, logging, and alerting across all services, and all data at rest is encrypted using AWS Key Management Service (AWS KMS).
>
> Callouts 1–9 happen during a single phone call, callout 10 covers how the solution deploys the SIP server and AgentCore Runtime, and callout 11 covers how it’s monitored and secured. The following section sets deployment and operations aside and gets closer to the call itself.
>
> Inbound call flow
>
> This section follows one call from the caller’s side from the first ring to the spoken reply. It is the same runtime path as callouts 1–9 in the preceding architecture diagram. The following diagram shows it as a sequence so the order of events is more straightforward to see.
>
> The numbered steps in the preceding diagram correspond to these stages of the call:
>
> The caller dials the toll-free number and Amazon Chime SDK Voice Connector answers.
>
> The Voice Connector invokes the SIP Media Application Lambda, which computes a session identifier for the call.
>
> The Lambda sends a warmup request to AgentCore Runtime, so the agent prepares its session while the phone is still ringing.
>
> The Lambda tells the Voice Connector to bridge the call to the SIP gateway on Amazon ECS on AWS Fargate, passing the session identifier along.
>
> The SIP gateway opens a SigV4-signed WebSocket to AgentCore Runtime using that same session identifier. The call attaches to the warmed session, caller audio flows to the agent, and the agent’s audio flows back to the caller.
>
> The agent runs the conversation with Amazon Nova 2 Sonic and calls backend tools through AgentCore Gateway when it needs menu, cart, order, or location data.
>
> Prerequisites
>
> Before you begin, verify that you have the following in place:
>
> An AWS account.
>
> Amazon Bedrock model access for Amazon Nova 2 Sonic in the AWS Region where you deploy, requested on the model access page in the Amazon Bedrock console.
>
> Amazon Chime SDK PSTN Audio access, with a phone-number quota increase requested in the Amazon Chime SDK console if you have never ordered a number in this account.
>
> Node.js 24.x or later.
>
> AWS Command Line Interface (AWS CLI) 2.x configured with credentials.
>
> git to clone the repository.
>
> AWS CDK bootstrapped in your target account and Region (npx cdk bootstrap aws://&lt;ACCOUNT_ID&gt;/&lt;REGION&gt;).
>
> The agent container is built with Python, but the build runs inside AWS CodeBuild, so you do not need Python on your own machine. Deploy in a Region where Amazon Nova 2 Sonic, Amazon Chime SDK PSTN Audio, and AgentCore Runtime are all available. US East (N. Virginia), us-east-1, is a good place to start.
>
> Deploy the solution with AWS CDK
>
> The full solution is available in the sample repository on GitHub. Clone the repository and change into the project directory.
>
> git clone https://github.com/aws-samples/sample-restaurant-telephony-ai-host-using-amazon-bedrock-agentcore-nova-sonic.git
>
> cd sample-restaurant-telephony-ai-host-using-amazon-bedrock-agentcore-nova-sonic
>
> Run the preflight check. It confirms that Node.js, the AWS CLI, git, the AWS CDK bootstrap, and Amazon Bedrock model access are all in place and reports anything missing.
>
> ./scripts/preflight-check.sh
>
> Then run the deployment script with a deployment prefix. The prefix is added to every resource name, which you can use to deploy the solution more than once in the same account.
>
> ./scripts/deploy-all.sh --deploymentPrefix qsr-tel
>
> The script deploys each AWS CDK stack in order and passes the outputs of one stack to the subsequent stack. It builds the backend first, then adds the AgentCore Gateway in front of the backend APIs. Next, it builds and pushes the agent container image with AWS CodeBuild and deploys the agent on AgentCore Runtime. Finally, it brings up the SIP gateway on Amazon ECS on AWS Fargate and provisions the Amazon Chime SDK Voice Connector and toll-free number. It also seeds sample menu and location data so you can place a real order as soon as it finishes. The build of the agent container takes several minutes the first time, so expect the run to pause while AWS CodeBuild works.
>
> When the script completes, it prints the number to dial:
>
> Your telephony agent is live at +1XXXXXXXXXX. Dial to test.
>
> How the SIP gateway works
>
> The telephony layer has one job. It turns a phone call into a media stream the agent can read and write. This matters because the phone network and the agent speak different protocols. The phone delivers audio as RTP packets over UDP. The agent expects a WebSocket carrying frames in the format Amazon Nova 2 Sonic understands. Without a translation layer in between, the agent would need to know about SIP, codec negotiation, and network-level media routing, all of which would couple it to a single channel. Two components handle that translation.
>
> The Amazon Chime SDK Voice Connector accepts the inbound call and invokes the SIP Media Application Lambda. That Lambda is where the call is steered. It returns an instruction to bridge the call to the SIP gateway and carries the session identifier along so the next hop knows which session this call belongs to.
>
> The SIP gateway runs on Amazon ECS on AWS Fargate. It uses drachtio-server for SIP signaling, with a Node.js bridge for the audio. The gateway answers the call and converts between the audio format the phone network uses and the format Amazon Nova 2 Sonic expects. For high availability (HA), it runs as two tasks across two Availability Zones (AZs), which gives it redundancy and a place to publish a call-count metric to Amazon CloudWatch for scaling. The signaling for the call passes through the Network Load Balancer, but the audio itself flows directly between the Voice Connector and the Fargate task, which keeps the load balancer off the media path.
>
> Warming the agent while the phone rings
>
> A voice call is unforgiving about silence. If a caller connects and hears nothing for a few seconds, the call feels broken even though the system is working. The slow part of starting a call is the one-time setup. The agent has to resolve the system prompt for this caller, open the Amazon Nova 2 Sonic stream, and discover the available MCP tools.
>
> Rather than make the caller wait through that, the SIP Media Application Lambda kicks it off while the phone is still ringing. As soon as the call arrives, the Lambda sends a warmup request to AgentCore Runtime with a session identifier for the call. AgentCore Runtime allocates a microVM and runs the setup during the ringing window. A moment later, when the SIP gateway opens its WebSocket connection using the same session identifier, AgentCore Runtime routes it to that already-warm microVM, and the agent is ready to talk.
>
> The session identifier is what connects the two requests. The Lambda computes it from the call itself, so the warmup request and the later audio connection resolve to the same microVM without any extra state to track. The following diagram shows how this overlaps with the ringing window so the agent is ready when the call connects.
>
> Storing menus, carts, and orders
>
> Five Amazon DynamoDB tables cover the ordering workflow. The Customers table stores profiles, including name, phone, and loyalty information, which the agent uses to recognize a returning caller. The Orders table keeps order history along with the pickup location. The Menu table holds items, prices, and availability, which can differ by location. The Carts table holds in-progress carts and uses a time-to-live value so abandoned carts clean themselves up. The Locations table holds restaurant details such as coordinates, hours, and tax rates that the agent uses for totals and recommendations. DynamoDB on-demand capacity scales with traffic, so there’s no throughput to manage.
>
> Finding a pickup location
>
> Amazon Location Service helps a caller find a convenient pickup spot without typing anything. A phone caller has no browser to share a location, so the agent asks for a ZIP code or a cross-street and uses Amazon Location Service to turn that into coordinates. From there, the backend can do a few things with those coordinates. It can find the nearest restaurants, rank them by driving time rather than straight-line distance so it favors a short detour along the caller’s route, or geocode a specific address. That lets the agent say something a caller can act on, such as “the closest location is on Main Street, about five minutes away,” instead of reading back an internal code.
>
> Processing voice with Amazon Bedrock AgentCore and Amazon Nova 2 Sonic
>
> The agent runs on AgentCore Runtime. Each call runs in its own microVM, so one caller’s session can’t affect another’s. AgentCore Runtime handles scaling and provides the WebSocket connection that carries audio both ways.
>
> Within the agent, the agent framework defines the system prompt, the tools it can call, and the flow of the conversation. Amazon Nova 2 Sonic does the speech work within the call. It recognizes speech across a range of accents and handles the varied audio quality that comes with a phone line. It streams audio in both directions with low latency, and it calls tools asynchronously without stopping the conversation (see Async tool calls in Amazon Nova Sonic), so the caller isn’t left waiting while data is fetched. It also handles interruptions, so a caller can talk over the agent the way people do on human-to-human calls.
>
> One detail is specific to phone calls. A backend lookup can take a few seconds, and Amazon Nova 2 Sonic ends a session that sits idle on the server side for too long. To hold the session open during a slow tool call, the agent sends a silent frame at a short interval. The session stays alive and the caller hears nothing unusual.
>
> Connecting the agent to backend tools with MCP
>
> The agent never calls the backend Lambda functions directly. AgentCore Gateway sits in between and presents the backend endpoints as MCP tools that the agent discovers and calls by name, covering menu lookups, cart operations, order placement, customer and order history, geocoding, and location search. This means the agent doesn’t need to know which Lambda function lives behind a given operation or how to authenticate to it.
>
> That layer is what keeps the design loosely coupled. When the agent calls a tool such as PlaceOrder, the gateway turns it into a REST request to Amazon API Gateway, which routes it to the matching AWS Lambda function. Because the agent talks to named tools rather than to specific functions, you can change a backend handler or add a tool without changing the agent. The same backend can also serve other channels, because they all place orders against the same tools and data.
>
> The following diagram shows how a single tool call travels from the agent to the backend.
>
> Recognizing a caller without a login
>
> A phone caller doesn’t sign in, so the system uses the caller’s phone number as the basis for identity. The system hashes the number with a secret value held on AWS Systems Manager Parameter Store, and the result becomes the session identifier. The raw phone number doesn’t appear in logs or session state. This hashing approach helps meet personally identifiable information (PII) handling requirements by ensuring that sensitive caller information is never stored or transmitted in plain text.
>
> If that identifier matches a known customer, the agent greets the caller by name and can offer their last order. If it doesn’t match, the caller orders as a guest, and the order is still placed and stored. Each order records the channel it came from and whether the caller was a guest, so you can identify telephony orders later.
>
> This recognizes a returning caller without asking for a login, but it’s not identity verification, and the phone-number hash shouldn’t be treated as proof of who is calling. Anyone with access to the same phone can place an order under that identity. A production deployment that needs verified identity can add a step such as a one-time passcode sent through SMS before the agent opens the caller’s account history.
>
> Ordering walkthrough
>
> Dial the number from the deploy output. The agent greets you and asks what you would like. You can speak naturally, ask about the menu, give a ZIP code for pickup, and confirm the order, all by voice. While the caller talks, the agent calls backend tools in the background, so there are no pauses while data loads. The following video shows a typical order from greeting to confirmation.
>
> After the call ends, you can trace the full path in Amazon CloudWatch Logs. The SIP gateway logs show how the call was set up and bridged to the agent. The agent logs show each agent event and tool call as the conversation progressed. Once the order is confirmed, it lands in the DynamoDB Orders table with its total and estimated ready time.
>
> Cost
>
> You pay for the AWS services the system uses. The toll-free per-minute charge and the always-on Fargate tasks are the two largest line items. You can lower both if it fits your needs. A local Direct Inward Dialing number costs less per minute than a toll-free number, and scaling the Fargate tasks down outside business hours cuts the compute charge once you know your traffic. Check the pricing page for each service for current rates, and set up a budget in AWS Cost Explorer to track spend.
>
> Clean up
>
> To avoid ongoing charges, remove the resources when you are done. The always-on Fargate tasks and the toll-free number continue to accrue cost whether or not calls are coming in. The cleanup script deletes the stacks in reverse order so each stack is removed before the ones it depends on.
>
> # Preview what will be deleted without removing anything.
>
> ./scripts/cleanup-all.sh --dry-run
>
> # Delete every stack the deploy created.
>
> ./scripts/cleanup-all.sh
>
> Cleanup is destructive. It releases the toll-free number, deletes the order history in Amazon DynamoDB, removes the secret on AWS Systems Manager Parameter Store, and deletes the container images in Amazon ECR. Back up anything you want to keep first. When the script finishes, confirm in the AWS CloudFormation console that the stacks are gone (see Viewing AWS CloudFormation stack data and resources on the AWS Management Console) and in the Amazon Chime SDK console that the toll-free number has been released (see Managing phone numbers in Amazon Chime SDK).
>
> Conclusion
>
> In this post, we walked through a telephony voice ordering system from deployment to a completed order. The architecture keeps telephony, agent, and backend independent so each piece can evolve on its own. That separation is what makes the system practical to operate, because you can update menu data, swap in a new voice model, or add a channel without coordinating changes across the whole stack.
>
> For the restaurant, this means phone orders flow in without pulling staff away from the counter. Callers get an immediate greeting instead of hold music, the agent confirms each item out loud to reduce mistakes, and the system handles peak hours without extra headcount. Because the agent connects to the backend through MCP tools, you can add capabilities like reservations or loyalty points by registering new tools without changing the agent or the telephony layer.
>
> To get started, clone the sample repository on GitHub and run the preflight check to confirm your environment is ready. From there, replace the seed data in the DynamoDB table definitions with your own menu items, locations, and pricing. Update the system prompt templates in the Parameter Store entries to reflect your restaurant’s name, greeting style, and any ordering rules. Then run the deploy script to bring the system live on your own toll-free number.
>
> About the authors
>
> Sergio Barraza
>
> Sergio is a Senior Technical Account Manager at AWS, helping customers design and optimize cloud solutions. With more than 25 years in software development, he guides customers through AWS service adoption. Outside work, Sergio plays guitar, piano, and drums, and practices Wing Chun Kung Fu.
>
> Salman Ahmed
>
> Salman is a Senior Technical Account Manager at AWS, specializing in helping customers design, implement, and optimize their AWS environments. He combines deep networking expertise with a passion for exploring emerging technologies to help organizations get the most out of their cloud investments. Outside of work, he enjoys photography, traveling, and watching his favorite sports teams.
>
> Ravi Kumar
>
> Ravi is a Senior Technical Account Manager in AWS Enterprise Support who helps customers in the travel and hospitality industry run their cloud operations. He has more than 20 years of IT experience and explores applications of generative AI in cloud computing. Outside of work, Ravi enjoys painting, cricket, and traveling to new places.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。