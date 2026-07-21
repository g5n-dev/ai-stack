---
title: "Monitor Amazon SageMaker Pipelines cross-account with custom Amazon CloudWatch dashboards"
date: 2026-07-16T06:15:26+08:00
draft: false
entry_kind: "auto"
tags: ["Advanced (300)", "Amazon CloudWatch", "Amazon DynamoDB", "Amazon EventBridge", "Amazon SageMaker", "AWS Lambda", "Technical How-to", "博客与播客"]
categories: []
source: "blogs_podcasts"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:08ebe633c433f6732e97e08f3095cb29b617a5b9118c2a9f6db1812c9ab5cda2"
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 89
description: "当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。"
external_url: https://aws.amazon.com/blogs/machine-learning/monitor-amazon-sagemaker-pipelines-cross-account-with-custom-amazon-cloudwatch-dashboards
observation_id: obs_341d7ce40d944dcf5d842849c17726ef46ab40ea75629eebda73298ef27d59ba
revision_id: rev_70d63d5d5d5c1485f6f1578dc44de013587dee7eec41b6e2fa4d22d08f8e9f37
event_id: evt_869668a902c4d7162050bf316d982593189691fea7671087200a263b5dedfb43
lineage_relation: original
parent_observation_id: null
source_published_at: null
first_seen_at: 2026-07-15T22:17:20Z
last_seen_at: 2026-07-20T00:00:00Z
timestamp_confidence: git
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/monitor-amazon-sagemaker-pipelines-cross-account-with-custom-amazon-cloudwatch-dashboards](https://aws.amazon.com/blogs/machine-learning/monitor-amazon-sagemaker-pipelines-cross-account-with-custom-amazon-cloudwatch-dashboards)

## 来源摘要/节选

> Using Amazon SageMaker Pipelines, organizations can automate their machine learning (ML) workloads and distribute them over many AWS accounts and AWS Regions as part of their Machine Learning Operations (MLOps) strategy.
>
> However, monitoring SageMaker Pipelines can become complex when they are distributed across many AWS environments. Developers and operations engineers must manually switch between multiple accounts and Regions to inspect SageMaker Pipeline executions, resulting in operational overhead.
>
> Amazon SageMaker Studio provides monitoring for SageMaker Pipelines within a single account and Region. Organizations can use services like Amazon CloudWatch, AWS Lambda, Amazon DynamoDB, and Amazon EventBridge to build dashboards that track SageMaker Pipelines executions across multiple AWS environments, tailored to their observability requirements.
>
> In this post, we present a solution designed to centralize the monitoring of SageMaker Pipelines across AWS accounts and Regions using Amazon CloudWatch custom dashboards. The accompanying GitHub repository provides a customizable AWS Cloud Development Kit (AWS CDK) example of the required infrastructure.
>
> The solution is designed to provide detailed, near-real time visibility from a single interface into SageMaker Pipelines executions running in many Regions and many accounts to help streamline daily operations. In the next section, we examine in detail the architecture of the solution.
>
> Solution overview
>
> The solution implements an interactive CloudWatch dashboard designed to provide unified visibility into SageMaker Pipelines running across multiple AWS accounts and Regions.
>
> We choose a serverless, event-driven architecture that responds to SageMaker Pipeline events in real time, avoiding the overhead of always-on monitoring systems or polling mechanisms. Using managed or serverless services and native service integrations can also help reduce upfront costs and maintenance effort.
>
> The implementation follows a hub-and-spoke model, which reduces complexity by centralizing the monitoring in the primary account and Region, while lightweight components in each secondary account or Region track SageMaker Pipelines data and forward it to the monitoring hub. The diagram illustrates this architecture.
>
> The solution described in the diagram provides modular components that comprise two main AWS CloudFormation stacks: the Dashboard stack and the Forwarder stack.
>
> The Dashboard stack contains the CloudWatch dashboard, Amazon DynamoDB storage tables, and AWS Lambda functions required for data processing and visualization. It’s deployed only in the primary account and Region that acts as the monitoring hub.
>
> The Forwarder stack is deployed in the monitored accounts that are the source of the SageMaker Pipeline data. These lightweight stacks use Amazon EventBridge to send enriched data to the monitoring hub.
>
> Combined, the two stacks collect, process, and display aggregated information to users through the following workflow:
>
> When a step of a SageMaker Pipeline changes status, Amazon SageMaker AI generates source events. These events include metadata such as the time of the event, the Amazon Resource Name (ARN) of the pipeline and of the pipeline execution, the status of the step, and others.
>
> Amazon EventBridge rules capture such events in real time and send them to AWS Lambda functions for processing.
>
> Lambda functions process the event data, enrich it with additional metadata like status or display name of the SageMaker Pipeline execution, and send it to the local EventBridge bus.
>
> Custom EventBridge rules capture the enriched data and forward it to the monitoring hub account.
>
> AWS Identity and Access Management (IAM) roles and resource policies secure the transmission of cross-account events.
>
> Another EventBridge rule in the monitoring account triggers a Lambda function that ingests the data about each SageMaker Pipeline execution and stores it in DynamoDB tables. The data stored includes, for instance, Region, account ID, creation, start and stop times, display name, and status of each SageMaker Pipeline execution and its individual steps.
>
> Lambda functions power the backend of the dashboard, reading DynamoDB tables and returning formatted HTML.
>
> An Amazon CloudWatch dashboard with custom widgets acts as a user-facing front end without leaving the AWS Management Console. It shows the SageMaker Pipeline executions with the respective account IDs, Regions, creation times, and current status. Users can use Interactive elements to filter data by pipeline name and access detailed information about the steps of a single execution. This information includes step name, type, start and end times, and status.
>
> CloudWatch triggers an alarm in case of anomalous activity from dashboard users. Amazon Simple Notification Service (Amazon SNS) then sends an alert to the subscribers of an SNS topic, which is encrypted using a customer managed AWS Key Management Service (AWS KMS) key. The alarms trigger when the widget calls to the respective Lambda functions exceed the thresholds defined in the Dashboard stack.
>
> This solution aims to provide a single-pane dashboard for cross-account and cross-Region observability of SageMaker Pipelines using a serverless, event-driven hub-and-spoke architecture.
>
> The data originates from SageMaker AI events and API calls, which are transformed to provide a comprehensive view of pipeline execution status. This data is stored in centralized DynamoDB tables and then displayed on a custom CloudWatch dashboard. You can extend the dashboard by using Lambda functions to read and process additional information before storing it in the DynamoDB tables.
>
> In the following section, we show how to deploy the solution.
>
> Prerequisites
>
> You must have the following prerequisites:
>
> One AWS account with two Regions bootstrapped for the AWS CDK. One Region will host the monitoring dashboard. The other Region will generate cross-Region SageMaker Pipelines events that will be displayed in the dashboard.
>
> A second AWS account with at least one bootstrapped Region to generate cross-account events that will be displayed in the dashboard.
>
> AWS credentials as shell environment variables with sufficient permissions to deploy the solution.
>
> Python (version 3.14 or later).
>
> The AWS CDK installed (version 2.1100.1 or later).
>
> The AWS Command Line Interface (AWS CLI) installed (version 2.32.12 or later).
>
> Docker, required for Lambda function packaging.
>
> At least one SageMaker Pipeline in each account and Region combination. If you don’t have existing SageMaker Pipelines, you can create them using SageMaker AI Projects from the SageMaker Studio in an Amazon SageMaker AI domain.
>
> Deploy the solution
>
> After you’ve satisfied the prerequisites, complete the following steps to deploy the solution.
>
> Clone the GitHub repository.
>
> Follow the detailed deployment instructions in the README file to deploy the stacks using the AWS CDK and the AWS CLI.
>
> Navigate to the AWS CloudFormation console in each account and Region. Choose either the DashboardStack or the ForwarderStack stack for more information about the deployments and the created resources.
>
> With the solution deployed, you can now test its functionality. In the following section, we explain how to verify its capabilities.
>
> Test the solution
>
> After deploying the solution, complete the following steps to test the functionalities of the dashboard. You can both create SageMaker Pipelines and launch executions from SageMaker Studio.
>
> On the Amazon CloudWatch console, choose Dashboards in the navigation pane.
>
> Choose the dashboard PipelineMonitoringDashboard.
>
> When prompted, allow the Lambda function to execute. Make sure that it contains customWidget in its name, as per best practices. The dashboard should update to look like the following image.
>
> If there are no recent SageMaker Pipeline executions, launch new executions in the monitored accounts and Regions starting, for simplicity, with the same account and Region of the monitoring dashboard.
>
> Return to the dashboard and reload the results using the refresh button on the top right corner of the widget. You should see new SageMaker Pipeline execution status updates. Make sure to choose a time range containing SageMaker Pipeline executions using the bar at the top of the dashboard.
>
> Choose the Steps details button. Allow the custom widget Lambda function to execute as described in the previous step. The popup will show detailed information about individual SageMaker Pipeline steps as illustrated in the following image.
>
> Use the date range at the top of the dashboard to filter for SageMaker Pipeline executions on custom date ranges. You should see runs only for executions within the chosen time range.
>
> Use the Pipeline name, filter on the top left corner of the widget. Enter the name of one SageMaker Pipeline, then refresh the widget. You should see runs only for SageMaker Pipelines matching the searched name.
>
> Best practices and considerations
>
> When implementing such a monitoring solution, consider the following recommendations to enhance reliability, security, and operational efficiency or to customize it to the needs of your organization.
>
> Flexibility and customization: You can further enrich the custom dashboard by including new data in the Lambda functions that populate the DynamoDB tables and by adding visualization logic. You can also add more filters, metrics, interactive popups or built-in CloudWatch widgets to consolidate and extend monitoring of your ML workloads. Furthermore, you can extend the solution to monitor AWS Step Functions state machine executions, jobs on AWS Batch or AWS Glue, or Amazon EMR clusters that support your ML workloads. In such a situation, consider creating a dedicated EventBridge event bus to isolate monitoring traffic from other events.
>
> Metrics and alarms: Monitor your SageMaker Pipeline through multiple layers: use EventBridge rules for service events, CloudWatch log anomaly detection for ML jobs execution logs, and CloudWatch metrics for resource utilization. Configure additional alarms on logs and metrics, or direct event notifications, to send Amazon SNS alerts to your team.
>
> Dashboard accessibility and customization: Consider different methods to share CloudWatch dashboards for faster accessibility and without passing through the AWS Management Console. Additionally, consider using Amazon managed Grafana as an alternative for data visualization.
>
> Private networking: For organizations with strict security requirements, consider deploying the solution within an Amazon virtual private cloud (VPC) for increased isolation. You can connect VPCs across Regions and accounts using VPC peering connections or AWS Transit Gateway.
>
> Integrate with continuous integration and delivery (CI/CD): For greater reliability, deploy the solution with (CI/CD) pipelines across the environments running your ML workflows. For example, AWS Organizations and the AWS Deployment Framework (ADF) help you deploy consistently and repeatably across your environments.
>
> Clean up
>
> To clean up your resources, for each of the accounts and Regions combinations to which you have deployed, go to the CloudFormation service console, and delete the instances of DashboardStack or ForwarderStack.
>
> Alternatively, you can repeat the same AWS CDK commands you executed before with the same AWS credentials and CLI arguments, respectively, but substituting cdk deploy with cdk destroy.
>
> Also remember to delete the SageMaker projects, resources, and instances of SageMaker AI domain in each account and Region if you created them only to test the solution.
>
> Conclusion
>
> We demonstrated how to set up a solution that helps monitor SageMaker Pipelines across AWS accounts and Regions using an interactive CloudWatch dashboard to improve operational efficiency. It is designed to deliver real-time updates, integrates directly with the AWS Management Console, and uses a fully serverless and event-driven architecture for greater scalability.
>
> To further adapt this solution to meet the standards of your organization, discover how to accelerate your journey on the cloud with the support of AWS Professional Services.
>
> Refer to the following resources to learn more on MLOps best practices:
>
> Implement a secure MLOps platform based on Terraform and GitHub
>
> AIOps modules
>
> Governing the ML lifecycle at scale, Part 1: A framework for architecting ML workloads using Amazon SageMaker
>
> Build an end-to-end MLOps pipeline using Amazon SageMaker Pipelines, GitHub, and GitHub Actions
>
> Build a centralized monitoring and reporting solution for Amazon SageMaker using Amazon CloudWatch
>
> Take also a look at more examples of custom widgets in CloudWatch dashboards to further strengthen the observability of your environments.
>
> About the author
>
> Giorgio Pessot
>
> Giorgio is a Machine Learning Engineer at AWS Professional Services. With a background in computational physics, he specializes in architecting enterprise-grade AI systems at the confluence of mathematical theory, DevOps, and cloud technologies. When he’s not whipping up cloud solutions, you’ll find Giorgio engineering culinary creations in his kitchen.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。