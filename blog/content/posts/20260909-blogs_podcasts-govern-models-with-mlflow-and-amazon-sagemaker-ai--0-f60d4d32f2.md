---
title: "Govern models with MLflow and Amazon SageMaker AI Model Registry sync: Part 2"
date: 2026-09-09T12:44:34+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "生成式 AI", "机器学习", "Amazon SageMaker AI", "Announcements", "Intermediate (200)", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:1a7f6d4ce25a81e03b29ab77065731a80cb14d26d07caa2b4ac3cb8e4688b82b"
source_payload_sha256: "sha256:ed71fbf953fc7b28f8a0b59d5d435d4e4892cc76ddc04bdb47e59b55678df877"
observation_id: obs_f60d4d32f299f7cfa5512c3face1db8b16a85975844847720e6a557bedd6750e
event_id: evt_8bb226062a56e02ef260441d4f28e2c51539b8dcab4a92a0cca1d06db0843213
revision_id: rev_32ff7a95addbc7a59ac35f7939504cc6345a3f85ea4d2863845d7b845927b3ce
source_published_at: 2026-09-08T17:03:50Z
first_seen_at: 2026-09-09T04:42:41.458289Z
timestamp_confidence: feed
lineage_relation: original
parent_observation_id: null
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 77
interpretation_sha256: "sha256:9796083addcb5326765fc55ab5de0cd1564f0bf9e0bcd056abdea9a4c7bd981e"
description: "该内容演示了在多个 AWS 账户之间利用托管 MLflow 与 SageMaker 模型注册表进行模型治理的两种跨账户拓扑（中心辐射式和混合式），并说明了从模型审批到通过 CI/CD 部署的完整流程。"
external_url: https://aws.amazon.com/blogs/machine-learning/govern-models-with-mlflow-and-amazon-sagemaker-ai-model-registry-sync-part-2
last_seen_at: 2026-09-09T04:42:41.458289Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/govern-models-with-mlflow-and-amazon-sagemaker-ai-model-registry-sync-part-2](https://aws.amazon.com/blogs/machine-learning/govern-models-with-mlflow-and-amazon-sagemaker-ai-model-registry-sync-part-2)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么  
该内容演示了在多个 AWS 账户之间利用托管 MLflow 与 SageMaker 模型注册表进行模型治理的两种跨账户拓扑（中心辐射式和混合式），并说明了从模型审批到通过 CI/CD 部署的完整流程。

### 用在哪里  
适用于拥有多个开发账户并需要在治理账户中统一管理、审批模型的组织，尤其是对工作负载隔离和合规性有严格要求的机器学习平台。

### 可以推断的  
推测：在大型机器学习团队中，跨账户治理能够提供更细粒度的权限控制和安全隔离。  
推测：实现此类治理需要在账户间预先配置 IAM 角色、资源共享策略以及跨账户的 S3 访问策略。

## 来源摘要/节选

> Governing models across accounts is the natural next step once automatic model registration is in place. In Part 1 we introduced how managed MLflow on Amazon SageMaker AI synchronizes registered models into the SageMaker AI Model Registry. We walked through a single-account setup where AWS Identity and Access Management (IAM) condition keys separate the data scientist and governance officer personas. Larger organizations, however, separate development from production at the account level. They run multiple development accounts and a central governance function. In regulated environments, they also impose a hard requirement that development workloads cannot write into production-grade accounts.
>
> In this post, we extend the same building blocks to two cross-account governance topologies. The first is a hub-and-spoke pattern that centralizes governance by sharing one MLflow app across development accounts with AWS Resource Access Manager (AWS RAM). The second is a hybrid pattern for regulated environments that keeps development accounts fully isolated from the governance hub. We close by showing how an approved model moves from the registry to a deployed endpoint through continuous integration and continuous delivery (CI/CD), and we compare the topologies to help you choose one. Working notebooks are available in the accompanying GitHub repository.
>
> The personas
>
> Part 1 introduced the data scientist (works in a Jupyter notebook, interacts only with MLflow) and the governance officer (works in the Amazon SageMaker Studio Models UI). Cross-account topologies add two more. The administrator performs the one-time cross-account setup: AWS RAM shares, bucket policies, and destination groups, using the console or CLI. In the hybrid topology, a model owner in each development account approves models locally before they are promoted to the hub. Each topology that follows is organized by these persona workflows.
>
> Prerequisites
>
> Before starting this walkthrough, make sure you have the following:
>
> Completion of Part 1. Familiarity with automatic model registration, the lifecycle staging construct, and IAM condition key gates from Part 1.
>
> Two AWS accounts, a development (spoke) account and a governance (hub) account. Configure a named AWS Command Line Interface (AWS CLI) profile for each (for example, mlops-spoke and mlops-hub). For setup details, see the Account and profile setup (REPO_LINK#account-and-profile-setup) section in the accompanying repository.
>
> The accompanying AWS CloudFormation stack deployed into both accounts. The template (cfn/sagemaker-studio-mlflow.yaml (REPO_LINK)) provisions a SageMaker AI Studio domain, user profile, execution role, and a Managed MLflow app with AutoModelRegistrationEnabled. Deploy one stack per account. See Provision the environment (REPO_LINK#provision-the-environment-cloudformation) in the repository README for the exact commands.
>
> For the full provisioning walkthrough, including CloudFormation deployment, reading stack outputs, and setting environment variables, refer to the accompanying repository (REPO_LINK).
>
> Topology 1: Hub-and-spoke central governance
>
> For larger organizations with multiple teams, it is common to have multiple separate development accounts with a central governance account. This topology provides workload isolation for development within each development account, with shared services offered through a centralized account hosting the MLflow app and the central Model Registry. The centralized hub account shares the MLflow app with one or more spoke (development) accounts using AWS RAM. This pattern extends the approach described in Centralize model governance with SageMaker Model Registry and AWS RAM sharing.
>
> The following figure illustrates the workflow:
>
> The hub creates an AWS RAM resource share for the MLflow app and the spoke accepts the invitation. Using external principals lets the share work even when the accounts are not in the same organization.
>
> A data scientist in the spoke registers a model against the shared MLflow app. With automatic registration, you get the Model Package Group and version in the hub account, created synchronously with the register call.
>
> The hub attaches a resource policy to the group and shares it back to the spoke with the AllowDeploy managed permission, so the spoke can describe and deploy the model.
>
> The governance officer validates the synced metrics and lineage and approves the model centrally in the hub.
>
> The approval event triggers a CI/CD pipeline, and a machine learning (ML) engineer deploys the approved model to an Amazon SageMaker endpoint in the spoke account.
>
> Figure 1: Hub-and-spoke topology with centralized governance
>
> Administrator: Set up cross-account access (one-time)
>
> The administrator prepares the hub and the sharing before either persona starts working. Prerequisite: model artifacts live in the hub’s MLflow artifact store, an S3 bucket in the hub account. Cross-account S3 access is needed on both sides:
>
> Resource side: a bucket policy on the hub artifact bucket granting the spoke account s3:GetObject, s3:PutObject, s3:ListBucket, and s3:GetBucketLocation. Without it, the data scientist’s log_model call fails with an S3 access error before registration happens.
>
> Identity side: the spoke execution role needs s3:GetObject on the hub bucket for deploy-time artifact reads. AmazonSageMakerFullAccess covers buckets whose name contains sagemaker. If the spoke role is scoped tighter, add the hub bucket explicitly.
>
> With the prerequisite in place, the administrator:
>
> Creates an AWS RAM resource share for the hub MLflow app, which the spoke accepts.
>
> After the first registration, attaches a resource policy to the synced Model Package Group and RAM-shares it back to the spoke with the AllowDeploy managed permission.
>
> In the hub AWS RAM console both shares show as Active:
>
> Figure 2: The MLflow app resource share shown as Active in the hub AWS RAM console
>
> Figure 3: The Model Package Group resource share shown as Active in the hub AWS RAM console
>
> Data scientist: Register from the spoke, in a notebook
>
> The workflow is identical to Part 1, with one difference: the notebook points the MLflow tracking URI at the hub app’s Amazon Resource Name (ARN). Automatic registration creates the Model Package Group and version in the hub, synchronously with the register call. The candidate appears in the hub registry pending approval, with the metrics, evaluation card, and lineage from the spoke’s run, as shown in the following figure:
>
> Figure 4: The synced candidate in the hub registry, pending approval with metrics and lineage
>
> Two points to plan for. First, automatic registration appends a short hash suffix to the group name, so my-model becomes my-model-&lt;hash&gt;. Discover the group with list_model_package_groups(NameContains=...), and reference it cross-account by its full ARN rather than its name. Second, lineage is recorded in the hub, because the sync executes there. The governance officer sees the full lineage graph in the hub’s Studio, but lineage entities are not shared back to the spoke by the AWS RAM share. Cross-account lineage sharing is not automatic.
>
> Governance officer: Approve centrally, in the hub Studio UI
>
> The governance officer works in the hub’s Studio Models view, one control point for candidates from every spoke. They review the synced metrics and lineage, promote to production, and set the approval status to Approved. The following figure shows the current lifecycle status of the registered version in the SageMaker AI Model Registry.
>
> Figure 5: Lifecycle status of the registered version in the SageMaker AI Model Registry
>
> What happens after approval is covered in the From approval to deployment section.
>
> Topology 2: Hub-and-spoke hybrid governance
>
> Some regulated organizations treat the hub as a production-grade account and do not want data scientists writing into it, even indirectly. For these customers, we recommend a hybrid topology that keeps each development account self-contained.
>
> The following figure illustrates the workflow:
>
> A data scientist registers a model against the development account’s own MLflow app.
>
> Automatic sync registers it into the development Model Registry, local to that account. The hub is untouched.
>
> The development account’s model owner reviews and approves the model in the development registry, which triggers the copy workflow.
>
> The workflow copies the approved model into the hub cross-account: it replicates the model artifacts into a hub-owned bucket, rewrites the inference specification, and registers the package in the hub’s shared destination group.
>
> The governance officer in the hub re-validates the copied model and approves it as the central governance record.
>
> An ML engineer deploys the locally approved model to an endpoint in the spoke, typically through a CI/CD pipeline. No cross-account artifact is needed at deploy time.
>
> Figure 6: Hub-and-spoke topology with hybrid governance
>
> Administrator: Expose the hub destination group (one-time)
>
> The hub administrator creates a destination Model Package Group, attaches a resource policy allowing the development account to CreateModelPackage into it, and RAM-shares it with the AllowRegister managed permission. The administrator also creates (or designates) a hub-owned artifact bucket that the copy workflow writes model artifacts into. The bucket policy grants the development account s3:PutObject and s3:ListBucket so the copy can run under the development account’s role. The AWS managed framework images used in this post are public per-Region, so no container image replication is needed. If your container image lives in a private repository in the development account, replicate the image to the hub or add an Amazon Elastic Container Registry (Amazon ECR) repository policy.
>
> Data scientist: Register in the development account, in a notebook
>
> Identical developer experience to Part 1, entirely inside the development account: the data scientist registers a model in the development MLflow app, which automatically syncs the registered model into the development Model Registry. The hub is untouched.
>
> Development account model owner: Approve locally
>
> The model owner reviews the candidate in the development registry and approves it. This local approval is the trigger for promotion to the hub, as shown in the following figure:
>
> Figure 7: The development account model owner approving a model version locally
>
> Approval-triggered copy, then governance officer re-validates in the hub
>
> The approval triggers a workflow (an Amazon EventBridge rule on the Model Package state change in production) that copies the approved package into the hub. The copy step replicates the model artifacts into a hub-owned bucket, rewrites the inference specification to point at the hub copy, and recreates the package in the hub with a pointer back to the source. The result is self-contained: the hub package has no runtime dependency on the development account.
>
> The copy step performs three actions. It replicates the model artifacts from the development bucket into the hub-owned bucket, and rewrites the inference specification so it points at the hub copy. Finally, it registers the package in the hub destination group with CustomerMetadataProperties recording the source package ARN and account. The result is self-contained: the hub package has no runtime dependency on the development account. See the repository for the actual implementation.
>
> The governance officer sees the copied package in the hub’s Studio, with provenance metadata pointing back to the source, re-validates it, and approves it independently. An example of the metadata a governance officer can see is shown in the following figure.
>
> Figure 8: The copied package in the hub with provenance metadata pointing to the source
>
> From approval to deployment
>
> Across both topologies, the approval in the registry is the gate, not the deployment itself. The approval status change emits an event to Amazon EventBridge, and you consume that event to trigger a CI/CD deployment pipeline: an Amazon EventBridge rule matching ModelApprovalStatus: Approved starts a pipeline that creates or updates the endpoint from the approved Model Package.
>
> Where the pipeline runs and where the endpoint lands are organizational choices. A common arrangement runs the pipeline in a shared-services account and deploys into a dedicated deployment account. Simpler setups run both in the development (spoke) account, which is what the accompanying samples demonstrate. Whichever account deploys needs read access to the model artifacts. In the central topology, that means the hub artifact bucket (see the preceding administrator prerequisite). In the hybrid topology, the hub copy is already self-contained.
>
> One consideration when introducing a separate deployment account: model lineage stays in the account where the sync recorded it. Plan your governance reviews around the hub (or development) registry rather than expecting lineage to follow the model into the deployment account.
>
> Choosing a topology
>
> The topologies trade account isolation against operational simplicity. The following table includes the single-account setup from Part 1 for comparison.
>
> Consideration
>
> Single-account (Part 1)
>
> Hub-and-spoke central
>
> Hub-and-spoke hybrid
>
> Accounts
>
> One
>
> Hub plus spokes
>
> Hub plus spokes
>
> Who writes to the hub
>
> Not applicable
>
> Spoke, through the shared MLflow app
>
> No one. Only approved copies
>
> Governance boundary
>
> IAM role
>
> Account plus AWS RAM
>
> Account plus approval-triggered copy
>
> Best fit
>
> Small teams, early projects
>
> Central governance with shared tooling
>
> Regulated environments needing hub isolation
>
> Operational cost
>
> Lowest
>
> Moderate
>
> Highest
>
> Across the three, the building blocks are the same: automatic registration produces the synchronized metadata, the staging construct expresses the lifecycle, and IAM condition keys and resource tags enforce the approval gate. What changes is where the account boundary sits and how a model crosses it.
>
> Clean up
>
> To avoid ongoing charges, remove the resources created during this walkthrough. The accompanying repository includes cleanup scripts for each topology that automate most of these steps.
>
> If you prefer to clean up manually, remove resources in the following order to respect dependencies:
>
> Delete the Amazon SageMaker AI endpoint and endpoint configuration in the spoke account. The endpoint incurs per-instance-hour charges while running.
>
> Delete the Amazon SageMaker AI model created in the spoke for deployment.
>
> Remove the AWS RAM resource shares. Delete the Model Package Group share (hub → spoke) and the MLflow app share (hub → spoke). In the spoke account, the corresponding shared resources disappear automatically after the share is deleted.
>
> Delete Model Package versions and the Model Package Group in the hub account. Remove all versions first, then delete the group.
>
> Delete the MLflow registered model in the hub’s MLflow app.
>
> Remove the cross-account bucket policy on the hub’s artifact-store bucket, or delete the bucket if it was created solely for this walkthrough.
>
> Delete the CloudFormation stacks in both accounts to remove the Amazon SageMaker AI domains, MLflow apps, execution roles, and artifact-store buckets.
>
> If stack deletion stalls on the Studio domain, delete any running Studio applications and spaces in the domain first, then retry.
>
> Conclusion
>
> Cross-account governance builds on the same automatic model registration introduced in Part 1: the sync produces synchronized metadata, the staging construct expresses the lifecycle, and IAM condition keys and resource tags enforce the approval gate. The hub-and-spoke central topology gives governance officers one control point for candidates from every development account, at the cost of allowing spokes to write into the hub through the shared MLflow app. The hybrid topology removes even that write path for regulated environments: development accounts stay self-contained, and only approved, self-contained copies cross into the hub. In both cases, approval events flow to Amazon EventBridge, where a CI/CD pipeline turns the governance decision into a deployment.
>
> To get started, review the documentation for automatic model registration, then work through the cross-account notebooks in the GitHub repository.
>
> For more information, refer to the following resources:
>
> Amazon SageMaker AI
>
> Automatically register SageMaker AI models with SageMaker Model Registry
>
> Staging Construct for your Model Lifecycle
>
> Centralize model governance with SageMaker Model Registry and AWS RAM sharing
>
> AWS re:Post for Amazon SageMaker
>
> Acknowledgement
>
> Special thanks to Rahul Kharse and Siamak Nariman for their contribution.
>
> About the authors
>
> Melanie, PhD, is a Senior Generative AI Specialist Solutions Architect at AWS based in Sydney, Australia, where her focus is on working with customers to build solutions leveraging state-of-the-art AI and machine learning tools. She has been actively involved in multiple Generative AI initiatives across APJ, harnessing the power of Large Language Models (LLMs). Prior to joining AWS, Dr. Li held data science roles in the financial and retail industries.
>
> Paolo Di Francesco
>
> Paolo is a Senior Solutions Architect at Amazon Web Services (AWS). He holds a PhD in Telecommunications Engineering and has experience in software engineering. He is passionate about machine learning and is currently focusing on using his experience to help customers reach their goals on AWS, in particular in discussions around MLOps. Outside of work, he enjoys playing football and reading.
>
> Ram Vittal
>
> Ram is a GenAI/ML Specialist SA at AWS. He has over 3 decades of experience architecting and building distributed, hybrid, and cloud applications. He is passionate about building secure, scalable, reliable GenAI/ML solutions to help customers with their cloud adoption and optimization journey to improve their business outcomes. In his spare time, he rides motorcycle and walks with his sheep-a-doodle!

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。