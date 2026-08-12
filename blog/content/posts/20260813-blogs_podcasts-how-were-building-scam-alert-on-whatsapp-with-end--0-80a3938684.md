---
title: "How We’re Building Scam Alert on WhatsApp With End-to-End Encryption and Verifiability Guarantees"
date: 2026-08-13T06:05:42+08:00
draft: false
entry_kind: "auto"
tags: ["机器学习", "Security & Privacy", "WhatsApp", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:b2e45466e72e3ea8ffc760082197a83cf2111311826e862eb2c0afb784c85a02"
source_payload_sha256: "sha256:f283e6035828f6ea4f7a80651030ff5c62d9045f37561267bb9bec7f8f9d3ef7"
observation_id: obs_80a3938684c737f3727477f8b741495cb83c3cc75a65d73f677ff6f4ace9a4af
event_id: evt_96681d4fcc07e9af68dd0806c16f89ae7e13d03e58f5fff590301a9ea046656b
revision_id: rev_2897cbe2ef367918bc9ea172751aba64bdd42f167508dc932146273e31ee07f6
source_published_at: 2026-08-12T13:00:28Z
first_seen_at: 2026-08-12T22:02:41.295206Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: true
source_truncation_reason: "crawler_feed_content_limit"
source_support: 1.0
source_title_chars_original: 97
interpretation_sha256: "sha256:9146edf54f371f83d473f3c88d1820b54fcf9a9e9c4d4d5ad5ee1acc67073600"
description: "WhatsApp推出可选的Scam Alert功能，在用户设备上运行轻量机器学习模型，对来自非联系人的消息进行本地诈骗概率评估，并在聊天界面显示警告，用户可自行决定是否阻止或上报。"
external_url: https://engineering.fb.com/2026/08/12/security/how-were-building-scam-alert-whatsapp
parent_observation_id: null
last_seen_at: 2026-08-12T22:02:41.295206Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://engineering.fb.com/2026/08/12/security/how-were-building-scam-alert-whatsapp](https://engineering.fb.com/2026/08/12/security/how-were-building-scam-alert-whatsapp)
- **发布域名**: engineering.fb.com

## 要点解读

### 这是什么
WhatsApp推出可选的Scam Alert功能，在用户设备上运行轻量机器学习模型，对来自非联系人的消息进行本地诈骗概率评估，并在聊天界面显示警告，用户可自行决定是否阻止或上报。

### 用在哪里
该功能适用于在使用WhatsApp时希望获得防诈骗提示的用户，尤其是与陌生人聊天时，可帮助判断信息是否可疑并采取相应行动。

### 可以推断的
- 推测：模型主要依赖文字结构和语言特征进行分类，暂不涉及图像、音频等多媒体内容的检测。  
- 推测：由于所有推断和日志记录均在本地完成，功能在无网络或弱网络环境下仍能保持防护效果。

## 来源摘要/节选

> WhatsApp is committed to helping people stay safe while protecting the privacy of their messages. As scam tactics evolve — from impersonation to social engineering to AI-generated lures — we’re always evolving as well, so that our protections stay ahead of scammers while protecting people’s personal messages with end-to-end encryption.
>
> Today, we’re sharing an early look at Scam Alert, a new, optional feature that runs an on-device machine learning model to alert a user about potential scam messages. No message content leaves the device for classification or is auto-reported to WhatsApp, Meta, or anyone else. The feature complements end-to-end encryption while enabling a user-controlled, optional scam alert when the model believes there’s a likely scam.
>
> Before we make this feature available to all WhatsApp users, we are publishing this early technical overview alongside the feature’s limited rollout in Beta, and will continue working with our Bug Bounty community to stress-test this system. To help validate our implementation, we welcome feedback from the broader security research community.
>
> Design Principles
>
> Recent advances in on-device machine learning models make it possible to run accurate text classification entirely on mobile hardware without the performance, battery, or model-size tradeoffs that previously made on-device classification less practical. Scam Alert is well-suited to this approach: The model is small enough to run on-device, simple enough to publish for independent review, and effective without server-side components. The architecture we chose reflects a set of deliberate choices about what this system can and cannot do.
>
> To that end, we designed Scam Alert to meet the following principles that adhere to the core guarantees of end-to-end encryption:
>
> On-device only: The model and the message data it processes all remain on the device.
>
> No automatic reporting: WhatsApp is unable to initiate sharing of any user data without the user’s action. The only way message content, or even the fact a scam was detected, reaches our servers is if the user explicitly chooses to report it, which is consistent with how user reporting works on WhatsApp.
>
> User control: Scam Alert is a user-controlled tool that provides additional information to the user, and the user can turn it off or on at any time.
>
> How Scam Alert Works
>
> Scam Alert is optional. Once the user turns it on, Scam Alert downloads a machine learning model to the device, where it runs inferences to classify whether incoming messages from non-contacts match known scam patterns. The model is trained on patterns observed in scam conversations from reports that users have sent to us. It performs probabilistic classification based on conversational structure and linguistic signals. No content is automatically reported to WhatsApp, Meta, or any third party.
>
> If the model identifies a message as a likely scam attempt, the user sees a warning in the chat, which is not visible to the other person. From there, the user can decide what to do: block, report, or continue the conversation. If they decide that a warning is incorrectly flagged, the user can mark the chat as trusted, in which case the warning is removed and Scam Alert will not flag that chat again. If a user marks that they trust a chat, they can also opt in to share the last 5 messages received with WhatsApp to help improve the feature’s accuracy.
>
> Foundational Safeguards
>
> To uphold the principles above, we designed Scam Alert with the following foundational requirements and safeguards, with each architecturally enforced and independently verifiable by security researchers through an expanded bug bounty program and by users themselves through in-app logs.
>
> On-Device Processing and Privacy-Preserving Analytics: All inference happens on-device and no message content leaves the user device for classification. The minimal telemetry needed to measure whether the feature is working (i.e., aggregate and anonymous warning counts and user action counts) is processed within a confidential computing environment and sent to WhatsApp as differentially private aggregates. The confidential federated analytics pipeline is built on top of confidential virtual machines (CVMs), a type of Trusted Execution Environment (TEE). We chose this approach so its behavior can be independently verified.
>
> No Targeted Model Delivery: Neither Meta nor WhatsApp can deliver a specific model to a specific user. Every model version, including experimental variants, is published on a public transparency ledger before it is deployed.
>
> Verifiable Model Behavior: We publish model weights so that independent security researchers can verify that we’ve purpose built this for scams only.
>
> The rest of this post details the technical implementation of each requirement.
>
> On-Device Processing and Privacy-Preserving Analytics
>
> As referenced above, all inference happens on-device. But we need to know that the feature itself is working – i.e., it is indeed catching real scams – and know if we need to update it to stay ahead of constantly evolving scams and improve the model over time.
>
> To that end, our approach follows a set of data minimization principles. Message content does not leave the device, and logging is limited by design to only the signals that are needed to measure whether the feature is working as intended. Even those signals are processed within a confidential computing environment built on TEEs, which ensures that processing occurs in a secure environment that no one, including Meta and WhatsApp, can access. Our experience building and securing systems like Private Processing has informed the design of this system. Only anonymous, differentially private aggregates are made available to Meta and WhatsApp. Differential privacy works by adding carefully calibrated noise to provide a mathematical guarantee that adding or removing any single person’s data has a negligible effect on the anonymous, aggregated numbers. Hence these aggregates show how the feature performs across the population while telling us nothing about any individual.
>
> For Scam Alert, that data is limited to two categories of approximate, aggregate counts:
>
> Warning Counts – how many times the on-device model surfaced a scam warning. This tells us whether the model is triggering at the right rate, which is essential for measuring precision and catching regressions across model versions.
>
> User Action Counts – when a user sees a warning, they can trust the sender or block and report. We log which action category was taken as an aggregate count. This tells us whether users find the warnings accurate, which is essential for measuring false positive rate.
>
> Confidential Federated Analytics
>
> To anonymize these warning and user action counts, we built a confidential federated analytics pipeline designed around the following privacy and security guarantees, each architecturally enforced and externally verifiable:
>
> On-Device Data Minimization: For Scam Alert, raw signals do not leave the device. The client aggregates them locally into counts and sends only those aggregated counts. These metrics are sent at randomized times, contain no device identifiers and limit any timestamp information to coarse time intervals. This ensures that neither the act of transmitting these metrics nor the metrics themselves can be used to identify a user.
>
> Confidential Processing: These metrics are processed within TEEs, secure hardware environments built on CPU-based confidential virtualization technologies, which allow attestation of software based in a hardware root of trust. Before any data is transmitted, the client checks these attestations and confirms them against a third-party log of acceptable binaries. Data is encrypted between the client and the TEE, so that no one in between, including Meta, WhatsApp, or any third-party relay, can access it.
>
> Secure Aggregation: Individual device metrics are not readable by Meta, WhatsApp, or anyone outside the TEE. They are merged into running aggregates, and only aggregated statistics, above a minimum cohort size and with differential privacy noise applied, are made available to Meta or WhatsApp. For Scam Alert, the device sends pre-aggregated counts directly to TEE for secure aggregation.
>
> Enforceable Guarantees: Before any data is transmitted, the client verifies that the code running in the TEE matches what was published on the third-party ledger and that the privacy parameters (such as differential privacy ε and δ, and k-anonymity thresholds) meet locally enforced guardrails. If verification fails or the privacy parameters are insufficient, the client refuses to transmit data. Any attempt to modify the processing guarantees either causes the system to fail closed or is publicly discoverable.
>
> Encrypted Recovery Checkpoints: Because the pipeline aggregates data over long periods, the system periodically saves encrypted checkpoints of its in-progress aggregates, so that a crash does not force a measurement to restart from scratch. These checkpoints contain only the partial aggregate counts already being computed, and they are encrypted: the keys never leave the TEEs, so only confidential federated analytics TEEs running the same attested binary can decrypt a checkpoint, and neither Meta nor WhatsApp can read it. Checkpoints are retained only for the bounded period needed to recover.
>
> Non-targetability: An attacker cannot target a particular user without attempting to compromise the entire system. All metrics are routed through an OHTTP relay that strips the requester’s IP address, and authenticated using anonymous credentials so that the system can verify that metrics come from a legitimate WhatsApp client without knowing which one. This limits the impact of small-scale attacks by ensuring that they cannot be used to target the data of a specific user.
>
> Verifiable Transparency: we will provide in-app capabilities for users to review what data was shared with the confidential federated analytics pipeline, the privacy parameters applied (such as differential privacy ε and δ, and k-anonymity thresholds), and details of how each secure session was established. We will be publishing the CVM image binary powering the pipeline, along with the source code of its privacy-relevant components, so that security researchers can independently verify that the published code is exactly what runs in the TEE. We will be expanding our Bug Bounty program to include the confidential federated analytics pipeline and will publish a detailed engineering white paper on its design.
>
> The foundations of this pipeline were established in Meta’s peer-reviewed federated analytics work, publicly outlined in “PAPAYA Federated Analytics Stack: Engineering Privacy, Scalability and Practicality” (USENIX NSDI 2025). Here, we describe how Scam Alert applies and extends that foundation.
>
> How Confidential Federated Analytics Works
>
> The pipeline works as follows:
>
> On-Device Data Collection: Data is collected and stored in a dedicated local store, isolated from other application data. The confidential federated analytics system can only access data that the application has explicitly made available to it. Hardcoded privacy guardrails enforce data lifetime, scope, and access. For Scam Alert, this is only counts of warning events and user actions.
>
> Job Selection: At randomized intervals, when the device is idle and subject to a self-enforced daily resource limit, the client connects to the application server via OHTTP. The client authenticates using anonymous credentials that prove it is a legitimate WhatsApp client without revealing which one, and fetches the list of active jobs for the pipeline. For each job, the client checks whether the privacy parameters (ε, δ, and k-anonymity thresholds) meet locally enforced guardrails, whether the device has new metrics to send, and whether participating would exceed its daily limits. The client can reject any job that does not meet these criteria.
>
> Local Transformation: For jobs the client accepts, it retrieves the relevant data from local storage and performs the requested on-device aggregation by converting raw signals into anonymous counts over the specified time period (e.g., daily warning counts, daily user action counts). Only the aggregated counts are transmitted; the raw signals remain on the device and are automatically deleted after a retention period.
>
> Attestation, Authentication, and Session Establishment: The client establishes a Remote Attestation + Transport Layer Security (RA-TLS) session with the orchestrator TEE. The attestation quote contains measurements of the orchestrator, which the client cross-checks against a third-party transparency ledger to ensure it is connecting only to code that satisfies our verifiable transparency guarantee. The client authenticates using anonymous credentials and the connection is routed via a third-party OHTTP relay that strips the requester’s IP address. The relay cannot read the metrics, as they are encrypted end-to-end between the device and the TEE.
>
> Orchestrator TEE — Ephemeral Processing: The encrypted metrics arrive at a stateless orchestrator hosted on a TEE. The orchestrator validates that the privacy configuration from the client matches the job’s configuration, batches metrics from multiple devices, and forwards the batched metrics to the appropriate aggregator TEE. For Scam Alert, these metrics are pre-aggregated counts.
>
> Aggregator TEE — Secure Aggregation: The aggregator TEE merges incoming metrics into running histograms. Individual metrics are discarded after aggregation. Periodically, the aggregator enforces k-anonymity thresholds to suppress results with too few contributors and applies differential privacy noise. The number and timing of releases are limited to ensure the overall privacy budget (ε, δ) is not exceeded across all releases. Only the noisy, thresholded aggregates are sent to WhatsApp.
>
> Datastore: Only differentially private, anonymous aggregates, such as total warning counts and action rates across all users, leave the TEE boundary. These aggregates contain no message content, no per-user data, and no conversation-level signals. They are used solely to measure whether the feature is working as intended.
>
> The confidential federated analytics pipeline is built so that, by the time any totals reach WhatsApp, the counts have been aggregated across many users and had differential privacy noise added – so we only ever see approximate counts of how many warnings were shown and how many were acted on. We will not know what the messages was, who sent or received them, or which conversation triggered a warning.
>
> Threat Model and Defense-in-Depth
>
> This confidential federated analytics pipeline operates in a highly adversarial environment. Our threat model accounts for three categories of attacker: third-party or supply chain vendors with access to system components, malicious or compromised insiders with access to infrastructure, and external actors attempting to exploit the pipeline’s attack surface.
>
> External actors attempt to intercept or extract unaggregated data in transit or during processing.
>
> Data in transit is encrypted between the device and the TEE and routed through a third-party OHTTP relay. The relay’s role is limited to stripping the client’s IP address – it cannot decrypt, inspect, or modify the data itself. Because this data is already not visible to the third-party, a compromised relay cannot access the data or associate datasets with a specific user. During processing, data is protected by TEE code isolation, with entry points limited to a small set of reviewed components.
>
> Insiders with infrastructure access attempt to access unaggregated data within the TEE.
>
> The TEE prohibits remote shell access, including from the host machine. Neither Meta engineers nor networked systems can gain access to the CVM shell at runtime. Software is built exclusively from checked-in source code and artifacts, where any change requires multiple engineers to modify the build artifacts or build pipeline. All code changes are auditable, enabling both continuous internal audits and external security researchers to inspect our binaries. Unaggregated data is never readable outside the TEE; when stored, it is encrypted under keys released only to a TEE running the same attested binary, and retained only for a bounded period before being merged into running aggregates and discarded.
>
> Attackers with physical or remote access interfere with the TEE to bypass confidential processing guarantees.
>
> Because TEE guarantees are not absolute, we apply defense-in-depth: encrypted DRAM, CVM hardening, enhanced host monitoring, and OHTTP relay routing that prevents directing a specific user’s data to a specific machine. A targeted attack would require compromising the entire system in a way that is publicly discoverable through verifiable transparency.
>
> No Targeted Model Delivery
>
> The model is downloaded from a CDN, not hardcoded into the app, so that improvements in accuracy and coverage of emerging scam tactics can reach people without requiring a forced app upgrade. And to that end, we are also ensuring that there is no path to deliver a different model to a specific user.
>
> Every model version — including its SHA-256 hash — is published on a third-party append-only transparency ledger before it is served to anyone. An append-only ledger is a public log where entries can be added but never modified or deleted, ensuring a tamper-evident history that researchers can inspect.
>
> We designed the model download system around three guarantees:
>
> Auditability: Every model version is publicly recorded on a third-party append-only transparency ledger before it is served to any user. The ledger is tamper-evident, so entries can be added but never modified or deleted. Delivering a targeted model would require publishing it on a ledger that anyone can inspect, making the attempt publicly discoverable. To check the ledger, users can download their in-app transparency log and use the namespace and epoch in the report to confirm, using the following format: https://akd-auditor.cloudflare.com/namespaces/&lt;namespace&gt;/audits/&lt;epoch&gt;.
>
> Anonymous Download Requests: The model download endpoint has no way to determine which user is requesting a model. All download requests are authenticated using anonymous credentials and routed through an OHTTP relay that strips the requester’s IP address, and the request payload contains no identity selectors. The model assets themselves are served by a CDN, which delivers only publicly published files and has no role in choosing which model a device uses, so it cannot be used to target a specific user.
>
> Non-targetability: No one can deliver a specific model to a specific user, even through experimentation. The client randomizes the timing of download requests, and experiment group assignment happens entirely on the device: the client assigns itself to a group using locally generated randomness, so the server cannot steer a specific user to a specific model variant.
>
> How Model Download and Verification Works
>
> Model Publication: When a new model version is ready for deployment, the server computes SHA-256 hashes of model weights, tokenizers, and other assets, and constructs a manifest — a JSON document containing these hashes, the model version, and a timestamp. The manifest digest (SHA-256 of the manifest) is submitted to a third-party signer (Cloudflare) for signing using Ed25519 keys. Meta does not hold the signing key. The signed manifest digest is then published to the third-party append-only transparency ledger, and the model assets are uploaded to the CDN.
>
> Anonymous Download Request: The client connects to the model download endpoint via OHTTP, authenticating with anonymous credentials. The OHTTP relay strips the client’s IP address — the relay can see the IP but cannot decrypt the request, and the server can see the request but only the relay’s IP. The server returns the manifest, the digital signature, and CDN URLs for the model assets.
>
> Client-Side Verification: Before using any downloaded model, the client performs a multi-step verification. First, it computes the manifest digest and verifies the digital signature against hardcoded Cloudflare Ed25519 public keys — confirming the manifest was signed by Cloudflare, not forged by Meta or any other party. Next, it cross-references the manifest digest with the transparency ledger and enforces freshness checks to prevent replay attacks with stale entries. Finally, it downloads the model assets from the CDN and verifies that the SHA-256 hash of each asset matches the manifest. If any step fails, the client refuses to load the model.
>
> Model Loaded on Device: Only after all verification steps pass does the client install and use the model.
>
> Private Experimentation
>
> Before rolling out a new model version globally, we must evaluate its accuracy and effectiveness by testing model variants with subsets of users. This experimentation must not create a path for targeting (ie delivering a specific model to a specific user). The model download flow is designed to prevent this:
>
> Client-Side Group Assignment: the download response includes the available model configurations, fetched at randomized intervals via the same anonymous OHTTP and ACS flow. Using a locally generated random seed, the client assigns itself to a group and selects which model to use from those configurations. The server cannot influence which model variant a specific user receives.
>
> Experiment Configuration Tamper Checks: The client enforces integrity checks on experiment configurations. Group properties cannot be modified after publication, experiment sizes can only be expanded (never reduced), and groups must meet a minimum size threshold, preventing an attacker from narrowing a group to target individual users.
>
> Experiment Models on the Ledger: Every experiment model variant is published to the transparency ledger before being served, with the same signing and verification flow as production models. No model — whether production or experimental — reaches a device without being publicly recorded.
>
> Anonymized Experiment Metrics: performance metrics from different experiment groups are measured through the same confidential federated analytics pipeline described earlier in this blog. If an experiment group is too small to meet k-anonymity thresholds after aggregation, the TEE suppresses the data entirely.
>
> Because the entire verification and experimentation flow runs on the client, security researchers can examine the app binary to confirm these checks are performed.
>
> Verifiable Model Behavior
>
> We outlined above how neither Meta nor WhatsApp can deliver a specific model to a specific user, and how the confidential federated analytics pipeline preserves privacy. But neither answers a more fundamental question: how can anyone verify that the model is built only to identify potential scam messages, unless its behavior can be independently examined?
>
> We designed the model verification system around two guarantees:
>
> User Visibility: Users have direct, on-device access to what the model did — which messages were scanned, what the outcome was, and which model version was used.
>
> Independent Verifiability: As referenced previously, external researchers can obtain the exact model that runs on user devices, verify its integrity against the transparency ledger, and analyze its behavior independently.
>
> How Model Transparency Works
>
> Published Model Artifacts: Every model version’s hashes are recorded in the signed manifest on the same third-party transparency ledger used to verify model delivery. The transparency ledger is public, so anyone can inspect it to verify which model versions are being served and confirm that every version, including experimental variants, is publicly recorded.
>
> Client-Side Transparency Logs: On the device itself, users can enable transparency logs that record which messages were flagged by the on-device machine learning model. Users can see this by going to Account &gt; Request Info &gt; Scam Alert Activity. Included in the transparency logs are the outcome of each analysis (whether the model flagged the message and whether the warning was shown), and which model version was used. These logs give users direct, granular visibility into how the system operates on

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。