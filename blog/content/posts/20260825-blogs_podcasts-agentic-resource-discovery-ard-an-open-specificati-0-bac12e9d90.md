---
title: "Agentic Resource Discovery (ARD): An open specification for agent discovery"
date: 2026-08-25T19:46:16+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "Amazon Bedrock AgentCore", "Announcements", "Intermediate (200)", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:2205d2402053975667501717274152f03db4d85666bc53598e24108a7da3eb54"
source_payload_sha256: "sha256:05de73f4dba3b3b4086c0e5ed0c66bf27f10a3c47be8e925e72560fc86828d9c"
observation_id: obs_bac12e9d90c3435ed86bb74e3c604a99961c0fe48aed88416fececa9664b14fd
event_id: evt_6182a16cdcb8c4ac6dea4e84376f109eb684f0a1a21816ebf03b11b8f7109ba6
revision_id: rev_b59fad962470ebbf38bc5ffcdf0d323b7a14f812176ba20d213b58ce9a8715d9
source_published_at: 2026-08-24T16:22:03Z
first_seen_at: 2026-08-26T14:06:24.203318Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 75
interpretation_sha256: "sha256:9ef780878e9241ee4deeb2708c81be2c4b0f89447c5971e085e50e7dbf760d5c"
description: "该内容介绍一种集中式资源目录，用于登记、审批和检索 AI 代理、MCP 服务器等工具，并阐述一项开放规范（ARD），旨在实现跨环境的统一发现。"
external_url: https://aws.amazon.com/blogs/machine-learning/agentic-resource-discovery-ard-an-open-specification-for-agent-discovery
parent_observation_id: null
last_seen_at: 2026-08-26T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/agentic-resource-discovery-ard-an-open-specification-for-agent-discovery](https://aws.amazon.com/blogs/machine-learning/agentic-resource-discovery-ard-an-open-specification-for-agent-discovery)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么  
该内容介绍一种集中式资源目录，用于登记、审批和检索 AI 代理、MCP 服务器等工具，并阐述一项开放规范（ARD），旨在实现跨环境的统一发现。

### 用在哪里  
适用于在多云、本地或 SaaS 环境中管理大量 AI 代理和工具的企业，帮助团队统一管理、审查并让用户或代理快速定位可用资源。

### 可以推断的  
推测：随着代理和工具数量的增长，跨平台统一发现的需求将推动更多组织采用类似的开放规范。  
推测：采用审批工作流与细粒度授权的目录方案，有助于满足企业在安全与合规方面的要求。

## 来源摘要/节选

> How AWS Agent Registry and the Agentic Resource Discovery (ARD) specification enable cross-environment discovery for your agents
>
> As organizations scale their use of artificial intelligence (AI) agents and tools, finding the right resource becomes the hard part. Teams build Model Context Protocol (MCP) servers, deploy agents, and create specialized tools, but without a central catalog, those resources stay siloed. Developers locate a resource, vet it, connect it, and maintain that connection manually. Worse, configuring an agent for one AI client doesn’t make it available to another.
>
> This was manageable when a team wired up a handful of tools. It doesn’t scale to a growing number of agents, MCP servers, skills, and APIs now spread across public registries and private enterprise estates.
>
> AWS Agent Registry: A centralized, searchable catalog
>
> AWS Agent Registry gives your organization a centralized catalog for agents, MCP servers, tools, agent skills, and custom resources. It’s built around two core concepts:
>
> Registries. A registry is a catalog you create in your AWS account with its own authorization configuration and approval settings. You can run a single org-wide registry or separate registries by resource type, stage, or team. With cross-account sharing, a registry can serve your entire AWS Organization.
>
> Registry Records. A record represents an individual resource, capturing metadata that describes what it is, what it does, and how to reach it.
>
> The workflow is straightforward
>
> Create a registry: An administrator creates a registry, configures approval settings, and sets up authorization using either AWS Identity and Access Management (IAM) or a JSON Web Token (JWT) from your corporate identity provider.
>
> Publish records: A publisher describes their MCP servers, agents, or tools as records and submits them for approval.
>
> Curate records and approve: A curator reviews pending records, approves or rejects them, and deprecates records no longer in use.
>
> Discover approved resources: Consumers, whether human users or AI agents, search the registry for the resources they need.
>
> What makes it enterprise-ready
>
> Curation: An approval workflow ensures only records that meet your security, compliance, and quality bar are discoverable. Administrators can remove a record from discovery at any time.
>
> Hybrid search: Semantic understanding combined with keyword matching, so both natural-language queries and exact name lookups return relevant results.
>
> MCP-native access: The registry is available at a remote MCP endpoint, so any MCP-compatible client can search and use it directly.
>
> Flexible authorization: Control access with IAM credentials or JWTs from your corporate identity provider.
>
> The multi-environment challenge
>
> AWS Agent Registry solves discovery within your AWS environment. But most enterprises don’t operate in one place. Agents and tools are deployed across multiple clouds, on-premises infrastructure, SaaS platforms, and enterprise applications, each with its own registry, naming convention, and metadata schema.
>
> When each environment uses its own format for describing agentic resources, bringing it all together requires bespoke connectors for every pair of registries that need to interoperate. A shared specification changes that equation: if every registry describes resources in the same format and exposes discovery through a common protocol, publishers describe once and consumers discover everywhere.
>
> Enter: Agentic Resource Discovery (ARD)
>
> ARD is an open standard, not a product or a single registry. It’s available under the Apache License 2.0 at agenticresourcediscovery.org and on GitHub. AWS contributed feedback during the spec’s development.
>
> Think of ARD as enabling federation across registries analogous to how the Domain Name System (DNS) enables name resolution across networks. An organization can deploy agents across environments, and each environment’s catalog surfaces these resources in a common protocol, behind an endpoint. For combined discovery, any registry can index across them using an understanding of the shared common protocol. Thus, local registries can federate through ARD without requiring bilateral agreements or proprietary connectors.
>
> How ARD can complement AWS Agent Registry
>
> We see ARD as a natural complement to the AWS Agent Registry model:
>
> Federate without migrating: Organizations with agentic infrastructure spread across clouds, on-premises, and SaaS could expose those resources in one consistent format. We expect ARD to enable cross-environment discovery while keeping control local.
>
> Discover globally, control locally: ARD’s design mirrors the control model AWS customers expect: the organization that publishes a catalog controls what’s in it, who can see it, and when to revoke access. We expect the existing access controls of AWS Agent Registry to remain at the enforcement point, with ARD serving as the interoperability layer.
>
> Enable public discovery: With ARD as a shared protocol, any organization can publish a catalog on its own domain, making it discoverable by any ARD-compatible client. We expect ARD to open cross-organizational discovery paths for Agent Registry customers.
>
> Learn more
>
> Read the ARD specification to understand the catalog and registry model.
>
> Explore the reference implementations on GitHub.
>
> Check out the AWS Agent Registry documentation.
>
> Read more about the launch in AWS Agent Registry now in preview.
>
> This is only the beginning. We’d love your feedback as AWS Agent Registry and our support for open discovery standards evolve.
>
> About the authors
>
> Jeffrey Damick
>
> Jeffrey is a Principal Software Engineer at Amazon Web Services, where he works on Amazon Route 53 and large-scale DNS and networking technologies. His recent work focuses on the intersection of DNS and artificial intelligence, exploring how established Internet infrastructure can support the discovery and communication of AI agents. This work includes evolving foundational Internet protocols and standards to enable scalable, open discovery of agents and their capabilities.
>
> Bhargav Talluri
>
> Bhargav is a Senior Manager, Product Management at AWS, where he leads the product roadmap for Amazon Route 53, Agent identity and discovery in AWS Agent Registry, and the Amazon Domains Registrar business. In addition to managing the product portfolio for Authoritative &amp; Recursive DNS and Security products, he focuses on building the infrastructure that gives AI agents stable, verifiable identities on the open web from DNS-based discovery to cross-ecosystem federation via open standards.
>
> Anubhav Mangal
>
> Anubhav is a Principal Product Manager at Amazon Web Services with Amazon Bedrock AgentCore, where he owns discovery of governance of agentic resources and AWS Agent Registry. He was formerly Sr. Manager, Product Management at AWS Marketplace. He has spent his career in technology and consulting across India and the US. He has a Masters in Computer Science and a Masters in Business Administration. Outside of work, he enjoys reading fiction, hiking, baking, and follows soccer and Formula One.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。