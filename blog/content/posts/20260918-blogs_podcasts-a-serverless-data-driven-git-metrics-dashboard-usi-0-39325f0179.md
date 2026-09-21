---
title: "A serverless, data-driven Git metrics dashboard using Amazon Quick Sight"
date: 2026-09-18T12:52:29+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "机器学习", "Advanced (300)", "Amazon Quick Sight", "Technical How-to", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:b5546fdf0381cbdeaca577d075421bd5081ce424d8bc634c44150c7ec83a0514"
source_payload_sha256: "sha256:71820669b97f8dbd24e4889b49cfeafc5747783262c5d55642354b7bb6090b84"
observation_id: obs_39325f0179a7e74752bf843e04ec8e7e89a972f32506c598811dfa73a45ccfb0
event_id: evt_d5e01de2aa5da02f72daab3fce59a6e9ae1b857035505377785c351ef5801ecd
revision_id: rev_703586c4cd88b2596d203ecc5569eae0299c29dae321ef09dc6b95a1653491e5
source_published_at: 2026-09-17T15:42:31Z
first_seen_at: 2026-09-18T05:01:01Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 72
description: "当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。"
external_url: https://aws.amazon.com/blogs/machine-learning/a-serverless-data-driven-git-metrics-dashboard-using-amazon-quick-sight
parent_observation_id: null
last_seen_at: 2026-09-21T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/a-serverless-data-driven-git-metrics-dashboard-using-amazon-quick-sight](https://aws.amazon.com/blogs/machine-learning/a-serverless-data-driven-git-metrics-dashboard-using-amazon-quick-sight)
- **发布域名**: aws.amazon.com

## 来源摘要/节选

> Git activity is one of the richest signals engineering teams produce that can provide continuous observability into development analytics. The challenge is extracting these Git metrics at scale, which has traditionally required hand-rolled extract, transform, and load (ETL) jobs, dedicated infrastructure, and ongoing maintenance.
>
> Further, with modern development tools becoming more prevalent, teams need a clear way to measure whether these tools are making developers faster, or if the investment is not paying off. The AWS AI-Driven Development Lifecycle (AI-DLC) framework makes a simple point: If you’re using AI coding tools, you need numbers to back it up. Set a baseline, track what changes, and keep watching. Otherwise, you’re flying blind. You won’t know whether AI is speeding things up, only padding the commit counts, or quietly introducing quality issues you did not expect.
>
> In this post, we introduce a serverless approach that automates Git metrics collection from GitHub and GitLab to surface live analytics using Amazon Quick Sight. Whether you’re tracking sprint velocity, assessing release readiness, or you need visibility into team patterns, this solution provides near-real-time insights into your Git platform activities. The serverless design abstracts infrastructure management while staying low-cost at scale.
>
> Solution overview
>
> This solution implements an automated, event-driven pipeline that collects repository metrics from GitHub and GitLab APIs automatically on schedule. It then processes them through a serverless orchestration workflow and persists the results in Amazon Simple Storage Service (Amazon S3) for graphical visualization using interactive Amazon Quick Sight dashboards.
>
> The key capabilities include:
>
> Intelligent change detection – A dedicated detector function monitors GitHub events API and GitLab activity feeds to determine whether changes like commits, pull requests, issues, repository creation or deletion occurred since the last collection. If no changes are detected, the processing is skipped entirely.
>
> Adaptive chunking – For organizations managing more than 20 repositories, the solution automatically partitions the workload into parallel chunks and processes them concurrently using AWS Step Functions Map states.
>
> Full and incremental loads – On first execution, the system performs a full load of all repository metadata. Subsequent runs use incremental logic, collecting only data that has changed. A full refresh is automatically triggered every 24 hours to maintain data accuracy.
>
> Configurable scheduling – How often metrics get collected is up to you. It’s an AWS CloudFormation parameter that accepts both rate() and cron() expressions, so you can set whatever schedule fits.
>
> The solution aligns with the AI-DLC framework’s observability pillar by providing continuous, automated measurement of development activity. You can establish velocity baselines before adopting AI tools, track changes during rollout, and quantify improvements over time.
>
> Architecture
>
> The architecture uses six core AWS services to build a fully managed, event-driven pipeline:
>
> Amazon EventBridge Scheduler: A scheduled rule starts the workflow at the interval you configured. It runs the collection cycle automatically without any external triggers or manual intervention.
>
> AWS Step Functions: A Step Functions state machine orchestrates the entire collection workflow. It first invokes the change detector to determine whether new activity has occurred. Based on the result, it decides between a full load and an incremental load. A full load collects all repository metadata from scratch on the first run and every 24 hours thereafter. An incremental load collects only data that changed since the last run, which reduces API calls and execution time. The workflow then evaluates the number of active repositories. If the count exceeds the chunking threshold (default: 20), it partitions the repositories into equal-sized chunks and processes them concurrently using a Step Functions Map state. Each chunk is handled by a separate AWS Lambda invocation. If the count is below the threshold, a single direct invocation collects all repositories. The workflow includes comprehensive retry logic with exponential backoff for transient API failures.
>
> AWS Lambda:
>
> Change detector – github-change-detector: This Lambda function queries the activity feeds to determine the load type. It monitors six categories of events: push events, pull requests, issue creation and updates, repository creation, repository deletion, and contributor changes. If no relevant events are found since the last check, the workflow terminates early.
>
> Metrics collector – github-metrics-collector: This Lambda function performs the actual data collection. It operates in three modes: collect_all for direct processing, collect_chunk for processing a subset of repositories during parallel execution, and aggregate for combining the chunk results.
>
> AWS Secrets Manager: Git tokens are stored securely in Secrets Manager. Both Lambda functions retrieve tokens at runtime, so that credentials are never hard coded or passed as environment variables.
>
> Amazon S3: Collected metrics are stored on Amazon S3 with versioning and server-side encryption enabled. The output includes a structured JSON file containing the full API response with nested repository details, and a flattened CSV file optimized for analytics. Both files include fields such as repository name, total commits, open and closed pull requests, open and closed issues, number of contributors, primary language, last activity timestamp, and repository creation date. S3 serves as the durable, cost-effective data store for all historical metrics.
>
> Amazon Quick Sight: Reads the collected CSV data from the S3 data store or through Amazon Athena for SQL-based queries. It loads the data into SPICE (Super-fast, Parallel, In-memory Calculation Engine), a fast in-memory layer, to build interactive dashboards. You can build visualizations for summary metrics, pull request (PR) trends, development activity over time, per-repository drilldowns, and contributor analysis.
>
> The following figure provides an overview of the solution architecture using the listed services.
>
> Figure 1: Architecture overview
>
> Before moving on to the step-by-step walkthrough, let us look at the prerequisites required for you to follow along.
>
> Prerequisites
>
> An active AWS account with permissions to create CloudFormation stacks, Lambda functions, S3 buckets, AWS Identity and Access Management (IAM) roles, Step Functions state machines, Amazon EventBridge rules, and Secrets Manager secrets.
>
> AWS Command Line Interface (AWS CLI) v2.
>
> A GitHub or GitLab account with repositories to monitor, and the ability to generate Personal Access Tokens.
>
> An active Amazon Quick Sight subscription on either Standard or Enterprise edition for dashboard creation.
>
> Least-privilege permissions for deploying the required resources: cloudformation:, s3:, lambda {CreateFunction,UpdateFunctionCode, UpdateFunctionConfiguration,GetFunction, PutFunctionConcurrency}, states:{CreateStateMachine,UpdateStateMachine,DescribeStateMachine}, events:{PutRule,PutTargets,DescribeRule}, sqs:{CreateQueue,GetQueueAttributes, SetQueueAttributes}, sns:{CreateTopic,GetTopicAttributes,SetTopicAttributes}, kms:{CreateKey, CreateAlias, PutKeyPolicy, EnableKeyRotation}, secretsmanager:{CreateSecret,GetSecretValue}, and iam:{CreateRole, PutRolePolicy, AttachRolePolicy, PassRole}.
>
> Clone the solution from this GitHub repository. Navigate to the cloned directory, subsequent steps reference file paths relative to this root.
>
> Walkthrough
>
> In this section, we elaborate the steps that you can follow to deploy a sample dashboard in your test environment.
>
> Step 1: Create personal access tokens
>
> Before deploying the infrastructure, you need API tokens for each Git platform you plan to monitor.
>
> For GitHub:
>
> Navigate to GitHub, Settings, Developer settings, Personal access tokens and choose Tokens (classic).
>
> Choose Generate new token (classic). Under scopes, select only the minimum required permissions: repo (read-only access to repository metadata, commits, and pull requests) and read:org (read-only access to organization membership). Copy the generated token and store it securely.
>
> For GitLab:
>
> Navigate to GitLab, Settings and Access Tokens.
>
> Create a new token with scopes and copy the generated token.
>
> The following image shows the GitHub developer settings page where you can generate the new tokens:
>
> Figure 2: GitHub developer settings page to generate new personal access tokens
>
> Step 2: Store tokens in AWS Secrets Manager
>
> Store each token as a secret in AWS Secrets Manager using the AWS CLI. See the following sample commands:
>
> # Store GitHub token
>
> aws secretsmanager create-secret \
>
> --name git-dashboard/github-token \
>
> --description "GitHub Personal Access Token for Git Dashboard" \
>
> --secret-string "ghp_YOUR_TOKEN_HERE" \
>
> --region us-east-1
>
> # Store GitLab token
>
> aws secretsmanager create-secret \
>
> --name git-dashboard/gitlab-token \
>
> --description "GitLab Personal Access Token for Git Dashboard" \
>
> --secret-string "glpat-YOUR_TOKEN_HERE" \
>
> --region us-east-1
>
> Step 3: Deploy the CloudFormation stack
>
> Download this sample CloudFormation template to follow along and deploy the solution in your non-production environment.
>
> Option 1: Deploy using the AWS CLI. Replace placeholder values enclosed in angle brackets (&lt;…&gt;) with your actual AWS account ID, Region, and the secret ARNs from Step 2:
>
> aws cloudformation create-stack \
>
> --stack-name git-metrics-pipeline \
>
> --template-body file://infrastructure/template.yaml \
>
> --parameters \
>
> ParameterKey=BucketName,ParameterValue=git-metrics-&lt;ACCOUNT_ID&gt;-&lt;REGION&gt; \
>
> ParameterKey=ScheduleExpression,ParameterValue="rate(10 minutes)" \
>
> ParameterKey=ChunkingThreshold,ParameterValue=20 \
>
> ParameterKey=GitHubTokenSecretArn,ParameterValue=&lt;YOUR_GITHUB_SECRET_ARN&gt; \
>
> ParameterKey=GitLabTokenSecretArn,ParameterValue=&lt;YOUR_GITLAB_SECRET_ARN&gt; \
>
> ParameterKey=EnabledPlatforms,ParameterValue="github,gitlab" \
>
> --capabilities CAPABILITY_NAMED_IAM
>
> Option 2: Deploy using the AWS Management Console.
>
> Navigate to the AWS CloudFormation console.
>
> Choose Create stack, With new resources (standard).
>
> Upload the template, fill in parameters, and choose Submit.
>
> Stack reaches CREATE_COMPLETE status in 3-5 minutes. It creates the following resources: an S3 bucket with versioning and encryption enabled, two Lambda functions (Python 3.13 runtime), an IAM execution role with least-privilege permissions, a Step Functions state machine, an Amazon EventBridge schedule rule, and associated IAM roles.
>
> The following image shows the sample Create stack parameters and configuration:
>
> Figure 3: CloudFormation console showing the Create stack configuration page
>
> Step 4: Upload the Lambda deployment package
>
> The CloudFormation template deploys placeholder code for the Lambda functions. Update them with the actual logic using the pre-built deployment package from the cloned repository. The file lambda-package.zip is located in the deployment/ directory of the repository you cloned in the prerequisites. Replace &lt;YOUR_BUCKET_NAME&gt; in the following commands with the S3 bucket name created by your CloudFormation stack:
>
> # Upload package to S3
>
> aws s3 cp deployment/lambda-package.zip s3://&lt;YOUR_BUCKET_NAME&gt;/lambda/lambda-package.zip
>
> # Update Detector Lambda
>
> aws lambda update-function-code \
>
> --function-name github-change-detector \
>
> --s3-bucket &lt;YOUR_BUCKET_NAME&gt; \
>
> --s3-key lambda/lambda-package.zip
>
> # Update Collector Lambda
>
> aws lambda update-function-code \
>
> --function-name github-metrics-collector \
>
> --s3-bucket &lt;YOUR_BUCKET_NAME&gt; \
>
> --s3-key lambda/lambda-package.zip
>
> Step 5: Execute and validate
>
> Trigger the workflow manually to verify end-to-end functionality. Replace &lt;ACCOUNT_ID&gt; with your 12-digit AWS account ID and &lt;REGION&gt; with your deployment AWS Region (for example, us-east-1):
>
> aws stepfunctions start-execution \
>
> --state-machine-arn arn:aws:states:&lt;REGION&gt;:&lt;ACCOUNT_ID&gt;:stateMachine:github-metrics-workflow \
>
> --input '{}'
>
> Monitor the execution in the AWS Step Functions console. A successful run produces a SUCCEEDED status within a few minutes. Verify that response.json file appears in your S3 bucket under the output/ prefix.
>
> Step 6: Connect Amazon Quick Sight to S3 data store to create your dashboards
>
> Create a manifest file named manifest.json pointing to your S3 bucket and JSON file. See Supported formats for Amazon S3 manifest files for file format information. Replace &lt;ACCOUNT_ID&gt; and &lt;REGION&gt; with your values. Use the following sample manifest:
>
> {
>
> "fileLocations": [
>
> {
>
> "URIs": [
>
> "s3://&lt;Your_Bucket_Name&gt;-&lt;REGION&gt;/output/response.json"
>
> ]
>
> }
>
> ],
>
> "globalUploadSettings": {
>
> "format": "JSON",
>
> "delimiter": ",",
>
> "textqualifier": "'",
>
> "containsHeader": "true"
>
> }
>
> }
>
> Go to the Amazon Quick Sight console.
>
> Navigate to Data, Data sources, and choose Create data source.
>
> Figure 4: Amazon Quick Sight console to create a new data source
>
> Choose Amazon S3 and Next.
>
> Provide a Data source name, upload your manifest file, and choose Connect.
>
> Figure 5: Upload your manifest JSON file to connect to your S3 data source
>
> Note: If you receive a permission error stating that Amazon Quick Sight does not have access to the S3 bucket, you must first authorize Quick Sight to access your S3 resources. Navigate to Quick Sight, choose your account name, select Manage Quick Sight, then choose Security &amp; permissions. Under Quick Sight access to AWS services, choose Manage, select Amazon S3, and add your metrics bucket. For detailed instructions, see Managing Amazon Quick Sight permissions to AWS resources.
>
> Navigate to Data, Datasets, and then choose Create dataset. Choose your Data source name and Select.
>
> Figure 6: Amazon Quick Sight console to create a new dataset
>
> Figure 7: Choose your S3 data source to create a dataset
>
> The Data source details window opens. Choose Visualize.
>
> Figure 8: S3 data source details window
>
> This creates a new analysis under Analyses. Choose the Git-QS-Datasource analysis.
>
> Figure 9: Analyses console page showing your newly created analysis
>
> Create the interactive dashboard visualizations by changing the visual type and choosing fields such as total commits, pull requests, issues, PR merge trends, and active compared to stale repositories.Note: Sample code to create a dashboard is available in the accompanying GitHub repository.
>
> The following images show a sample dashboard with sample data around Repository Portfolio Analysis including total number of repositories, total commits, pull requests submitted, issues tracked, and so on.
>
> Figure 10: Sample Amazon Quick Sight dashboard with dummy data
>
> Figure 11: Metrics summary showing multiple fields for a particular period
>
> Step 7: Optionally configure alerts
>
> Set up Amazon CloudWatch alarms to monitor pipeline health. For example, create an alarm that triggers when Step Functions execution failures exceed zero in a one-hour window, sending a notification to an Amazon Simple Notification Service (Amazon SNS) topic for your operations team.
>
> Clean up
>
> To avoid ongoing charges, remove all resources when you no longer need the solution:
>
> Step 1: Empty and delete the S3 bucket.
>
> aws s3 rm s3://git-metrics-amzn-s3-demo-bucket --recursive
>
> aws s3 rb s3://git-metrics-amzn-s3-demo-bucket
>
> Step 2: Delete the CloudFormation stack.
>
> aws cloudformation delete-stack --stack-name git-metrics-pipeline
>
> aws cloudformation wait stack-delete-complete --stack-name git-metrics-pipeline
>
> # Verify the stack has been deleted
>
> aws cloudformation describe-stacks \
>
> --stack-name git-metrics-pipeline \
>
> --query "Stacks[0].StackStatus"
>
> Step 3: Delete the secrets from Secrets Manager.
>
> aws secretsmanager delete-secret --secret-id git-dashboard/github-token --force-delete-without-recovery
>
> aws secretsmanager delete-secret --secret-id git-dashboard/gitlab-token --force-delete-without-recovery
>
> Step 4: Remove Quick Sight datasets and Analyses (if created) from the Quick Sight console.
>
> After these steps, no resources from this solution remain in your account, and no further charges will accrue.
>
> Conclusion
>
> In this post, we demonstrated how to build a fully serverless Git analytics solution that automatically collects development activity data from GitHub and GitLab, persists it in Amazon S3, and visualizes it through interactive Amazon Quick Sight dashboards. The result is a lightweight, low-cost engineering intelligence solution with near-zero operational maintenance. Engineering managers gain sprint status visibility, product managers gain release confidence, and developers gain contribution awareness, all without managing any infrastructure. For teams adopting modern development agents, this solution also aligns with the AI-Driven Development Lifecycle (AI-DLC) methodology. It provides the continuous measurement layer needed to set baselines, track velocity shifts, and quantify real return on investment (ROI). Metrics such as commits per sprint, PR throughput, review cycle time, and contributor diversity help determine whether AI tools are driving meaningful delivery improvements.
>
> Getting started
>
> To deploy this solution in your AWS account, clone the sample starter kit repository and follow the provided instructions. To learn more about the components used in this solution, see the following resources:
>
> AI-Driven Development Lifecycle (AI-DLC) guide.
>
> AWS CloudFormation User Guide.
>
> Amazon Athena User Guide.
>
> AWS Secrets Manager User Guide.
>
> Interactive dashboards in Amazon Quick Sight.
>
> REST API documentation for GitHub and GitLab.
>
> About the authors
>
> Saurabh Singhal
>
> Saurabh is a Technical Account Manager at Amazon Web Services (AWS) with over 16 years of experience in DevOps and cloud enterprise solutioning. He is an active member of the Next-Gen Developer Experience, Machine Learning/AI, and CloudOps field communities at AWS, where he helps customers accelerate their cloud transformation journey through strategic technical guidance and operational best practices.
>
> Kirti Dhabhai
>
> Kirti is a Technical Account Manager at AWS and has 10+ years of experience as cloud consultant. She manages strategic Global System Integrators (GSIs) and Partners operating on AWS Enterprise Support. She is a member of the internal Security &amp; Cloud Operations field community with focus areas in threat detection &amp; incident response, infrastructure security, and observability on AWS cloud.
>
> Ashish Jain
>
> Ashish is a Senior Technical Account Manager at AWS, committed to accelerate the cloud innovation for AWS Global Enterprise customers. He has 20+ years of industry experience across systems engineering, automations, Microsoft workloads, cloud operations &amp; infrastructure management and customer advocacy. He is passionate about cloud technologies and strives to use them toward his customers’ success on AWS cloud.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。