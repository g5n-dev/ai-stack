---
title: "Build a no-code ML workflow with Snowflake, Amazon SageMaker Canvas and Amazon Quick – Part 1: Setting up your Snowflake environment"
date: 2026-08-21T05:45:57+08:00
draft: false
entry_kind: "auto"
tags: ["生成式 AI", "机器学习", "Advanced (300)", "Amazon SageMaker Canvas", "Technical How-to", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:48a5d73c52e06f971c99798621fc7f5c886ef23fbdecaf21ffff70532d2380a1"
source_payload_sha256: "sha256:5387d8b4d5f1c2d629654f401c5acbd619a388200c9090465ac84c90710604e4"
observation_id: obs_b1d4c6cfcf5ba4873c1d5ab7628a5dc106404025cc7e19fd4bbb681fcb3db11c
event_id: evt_62672c4e762ce06979451b49e277b4bfc238cbaeee58e613f84292595b769d86
revision_id: rev_acad36d754a9e217ccfbf7f8269514ece6e07e02ddad66a73adb9b83e1d10482
source_published_at: 2026-08-20T21:23:38Z
first_seen_at: 2026-08-20T21:43:08.569476Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 132
interpretation_sha256: "sha256:8e468784d33653efaf77b316926558881bdd749e5b8084eaca1522ad7a8e7dfd"
description: "这部分内容说明如何在 Snowflake 中完成初始环境准备，以便后续使用可视化机器学习工具直接对仓库数据进行建模和预测，属于无代码机器学习工作流系列的第一阶段。"
external_url: https://aws.amazon.com/blogs/machine-learning/build-a-no-code-ml-workflow-with-snowflake-amazon-sagemaker-canvas-and-amazon-quick-part-1-setting-up-your-snowflake-environment
parent_observation_id: null
last_seen_at: 2026-08-20T21:43:08.569476Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/build-a-no-code-ml-workflow-with-snowflake-amazon-sagemaker-canvas-and-amazon-quick-part-1-setting-up-your-snowflake-environment](https://aws.amazon.com/blogs/machine-learning/build-a-no-code-ml-workflow-with-snowflake-amazon-sagemaker-canvas-and-amazon-quick-part-1-setting-up-your-snowflake-environment)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么  
这部分内容说明如何在 Snowflake 中完成初始环境准备，以便后续使用可视化机器学习工具直接对仓库数据进行建模和预测，属于无代码机器学习工作流系列的第一阶段。

### 用在哪里  
面向在云数据仓库里拥有大量业务数据、但缺少专职机器学习工程师的团队，尤其是业务分析师、产品负责人和运营人员需要快速获取预测结果并共享洞察的场景。

### 可以推断的  
推测：后续章节会演示将可视化建模工具连接到 Snowflake、训练欺诈检测模型并把评分结果输出到交互式仪表盘。  
推测：该方案旨在让业务人员自行完成数据准备和模型迭代，降低对专门数据科学资源的依赖，从而显著压缩从需求到洞察的时间。

## 来源摘要/节选

> Healthcare, retail, and life sciences organizations generate massive quantities of operational data in cloud data warehouses like Snowflake. While these systems store and scale information efficiently, transforming that data into meaningful predictions remains a challenge. Traditional machine learning (ML) approaches require specialized teams, long development cycles, and heavy engineering support, creating delays and limiting experimentation for the business users who understand the data best.
>
> A no-code ML workflow changes that dynamic.
>
> With Amazon SageMaker Canvas, you can explore datasets, prepare features, build predictive models, and generate insights visually without writing code and without depending on data science resources. Business analysts, product owners, and operational teams can accelerate decision-making while maintaining enterprise security and governance.
>
> This is Part 1 of a three-part series. Part 1 covers setting up your AWS account and Snowflake environment. Part 2 connects Amazon SageMaker Canvas to Snowflake to prepare data and build a fraud detection model. Part 3 sends predictions to Amazon Quick to create interactive dashboards and share insights with stakeholders.
>
> Business challenge
>
> This solution was inspired by a real healthcare organization that had accumulated years of operational data in Snowflake including sales transactions, product movement, patient interactions, and regional performance metrics. While the data foundation was robust, turning that data into predictive insights remained a challenge.
>
> Business teams wanted to forecast demand across multiple product categories, understand seasonal and regional consumption patterns, and surface ML-driven insights directly within business intelligence (BI) dashboards to support faster decisions. However, the organization lacked sufficient data science capacity to support these needs. Every new forecasting or analytics request required engineering or ML specialists, resulting in long development cycles and limited experimentation.
>
> This created a clear gap: business users understood the questions and the data but didn’t have a practical way to build and iterate on predictive models themselves. Additionally, after predictions were generated, organizations needed a way to visualize and share these insights with stakeholders through interactive dashboards. Rather than introducing yet another complex ML pipeline, the organization needed an approach that could bring machine learning closer to business teams. That approach had to work natively with existing Snowflake data, visualize predictions through familiar BI tools, and reduce dependency on specialized resources without compromising governance or security.
>
> These requirements naturally pointed toward a no-code machine learning approach integrated with visualization capabilities as the next step.
>
> Solution overview
>
> To bridge the gap between data-rich environments and insight-starved business teams, this post walks you through a no-code ML workflow built on Amazon SageMaker Canvas. Rather than replacing your existing data infrastructure, this approach extends the value of your Snowflake investments by making machine learning accessible to non-technical users and connecting predictions directly to visualization tools.
>
> Amazon SageMaker Canvas provides an intuitive, visual interface that connects directly to Snowflake, so you can prepare data, build machine learning models, and generate forecasts. After you train your model, deploy it to Amazon SageMaker Endpoint directly from the Canvas model details page, with no infrastructure configuration required. When the endpoint status shows In service, generate predictions on your Snowflake transaction data. To visualize results in Amazon Quick, use batch predictions in Canvas to output the scored dataset to Amazon Simple Storage Service (Amazon S3). Amazon Quick visualizes these insights through interactive dashboards, making ML-driven forecasts accessible to stakeholders across your organization without custom pipelines or data-science intervention.
>
> Figure 1: End-to-end architecture showing data flow from Snowflake through Amazon SageMaker Canvas to Amazon Quick Sight dashboards
>
> This architecture delivers key benefits:
>
> Democratized access to ML through self-service model building without coding expertise.
>
> Simplified data preparation with over 300 visual transformations powered by Data Wrangler while maintaining enterprise governance.
>
> Accelerated time-to-insight by reducing model development from months to hours.
>
> Training on the managed infrastructure of Amazon SageMaker.
>
> Interactive visualization of predictions through Amazon Quick Sight dashboards.
>
> Support for multiple ML problem types including regression, classification, and time-series forecasting to address diverse business questions from a single solution.
>
> Technical implementation
>
> This section walks through the hands-on steps to configure your Snowflake environment with sample fraud detection data.
>
> Prerequisites
>
> Make sure that you have the following prerequisites.
>
> An AWS account.
>
> Snowflake account. For steps to create a Snowflake account, refer to Create a Snowflake Free Trial Account.
>
> Snowflake database setup
>
> To create a Snowflake database, in the left-side panel of the Snowflake console, choose the plus sign (+), and then choose SQL worksheet.
>
> A blank SQL file opens. Copy and paste the following SQL commands into the worksheet and choose Run.
>
> -- Create database and warehouse
>
> USE ROLE accountadmin;
>
> CREATE OR REPLACE WAREHOUSE HOL_WH WITH WAREHOUSE_SIZE='X-SMALL';
>
> CREATE OR REPLACE DATABASE FRAUD;
>
> -- Use the database
>
> USE DATABASE FRAUD;
>
> -- Create the final fraud table with proper data types
>
> CREATE OR REPLACE TABLE FRAUD.PUBLIC.FRAUD_TABLE (
>
> id NUMBER,
>
> trans_date_trans_time TIMESTAMP_NTZ(9),
>
> cc_num NUMBER,
>
> merchant VARCHAR,
>
> category VARCHAR,
>
> amt NUMBER(38,2),
>
> first VARCHAR,
>
> last VARCHAR,
>
> gender VARCHAR,
>
> street VARCHAR,
>
> city VARCHAR,
>
> state VARCHAR,
>
> zip NUMBER,
>
> lat NUMBER(38,15),
>
> long NUMBER(38,14),
>
> city_pop NUMBER(38,0),
>
> job VARCHAR,
>
> dob DATE,
>
> trans_num VARCHAR,
>
> unix_time NUMBER,
>
> merch_lat NUMBER(38,15),
>
> merch_long NUMBER(38,14),
>
> is_fraud NUMBER
>
> );
>
> -- Generate sample fraud detection data for 2020
>
> INSERT INTO FRAUD.PUBLIC.FRAUD_TABLE
>
> WITH raw_data AS (
>
> SELECT
>
> ROW_NUMBER() OVER (ORDER BY SEQ4()) as id,
>
> DATEADD(minute, UNIFORM(0, 525600, RANDOM()), '2020-01-01 00:00:00'::TIMESTAMP_NTZ) as trans_date_trans_time,
>
> UNIFORM(1, 1000, RANDOM()) as cc_num,
>
> CONCAT('merchant_', UNIFORM(1, 500, RANDOM())) as merchant,
>
> CASE UNIFORM(1, 14, RANDOM())
>
> WHEN 1 THEN 'grocery_pos'
>
> WHEN 2 THEN 'gas_transport'
>
> WHEN 3 THEN 'shopping_net'
>
> WHEN 4 THEN 'shopping_pos'
>
> WHEN 5 THEN 'food_dining'
>
> WHEN 6 THEN 'entertainment'
>
> WHEN 7 THEN 'personal_care'
>
> WHEN 8 THEN 'health_fitness'
>
> WHEN 9 THEN 'travel'
>
> WHEN 10 THEN 'kids_pets'
>
> WHEN 11 THEN 'home'
>
> WHEN 12 THEN 'misc_net'
>
> WHEN 13 THEN 'misc_pos'
>
> ELSE 'other'
>
> END as category,
>
> ROUND(UNIFORM(1, 1000, RANDOM()) + UNIFORM(0, 99, RANDOM())/100, 2) as amt,
>
> CONCAT('FirstName', UNIFORM(1, 1000, RANDOM())) as first,
>
> CONCAT('LastName', UNIFORM(1, 1000, RANDOM())) as last,
>
> CASE UNIFORM(0, 1, RANDOM()) WHEN 0 THEN 'M' ELSE 'F' END as gender,
>
> CONCAT(UNIFORM(1, 9999, RANDOM()), ' Main St') as street,
>
> CASE UNIFORM(1, 10, RANDOM())
>
> WHEN 1 THEN 'New York' WHEN 2 THEN 'Los Angeles' WHEN 3 THEN 'Chicago'
>
> WHEN 4 THEN 'Houston' WHEN 5 THEN 'Phoenix' WHEN 6 THEN 'Philadelphia'
>
> WHEN 7 THEN 'San Antonio' WHEN 8 THEN 'San Diego' WHEN 9 THEN 'Dallas'
>
> ELSE 'San Jose'
>
> END as city,
>
> CASE UNIFORM(1, 10, RANDOM())
>
> WHEN 1 THEN 'NY' WHEN 2 THEN 'CA' WHEN 3 THEN 'IL' WHEN 4 THEN 'TX'
>
> WHEN 5 THEN 'AZ' WHEN 6 THEN 'PA' WHEN 7 THEN 'TX' WHEN 8 THEN 'CA'
>
> WHEN 9 THEN 'TX' ELSE 'CA'
>
> END as state,
>
> UNIFORM(10000, 99999, RANDOM()) as zip,
>
> ROUND(UNIFORM(25.0, 49.0, RANDOM()) + UNIFORM(0, 999999, RANDOM())/1000000, 15) as lat,
>
> ROUND(UNIFORM(-125.0, -65.0, RANDOM()) + UNIFORM(0, 99999999999999, RANDOM())/100000000000000, 14) as "LONG",
>
> UNIFORM(10000, 5000000, RANDOM()) as city_pop,
>
> CONCAT('Job_Title_', UNIFORM(1, 100, RANDOM())) as job,
>
> DATEADD(year, -UNIFORM(18, 80, RANDOM()), '2020-12-01'::DATE) as dob,
>
> CONCAT('trans_', LPAD(ROW_NUMBER() OVER (ORDER BY SEQ4()), 10, '0')) as trans_num,
>
> DATEDIFF(second, '1970-01-01', DATEADD(minute, UNIFORM(0, 44640, RANDOM()), '2020-12-01 00:00:00'::TIMESTAMP_NTZ)) as unix_time,
>
> ROUND(UNIFORM(25.0, 49.0, RANDOM()) + UNIFORM(0, 999999, RANDOM())/1000000, 15) as merch_lat,
>
> ROUND(UNIFORM(-125.0, -65.0, RANDOM()) + UNIFORM(0, 99999999999999, RANDOM())/100000000000000, 14) as merch_long
>
> FROM TABLE(GENERATOR(ROWCOUNT =&gt; 139538))
>
> )
>
> SELECT
>
> id, trans_date_trans_time, cc_num, merchant, category, amt,
>
> first, last, gender, street, city, state, zip, lat, "LONG",
>
> city_pop, job, dob, trans_num, unix_time, merch_lat, merch_long,
>
> CASE
>
> WHEN category IN ('shopping_net', 'misc_net') AND amt &gt; 700
>
> AND UNIFORM(0, 100, RANDOM()) &lt; 85 THEN 1
>
> WHEN category = 'travel' AND amt &gt; 800
>
> AND UNIFORM(0, 100, RANDOM()) &lt; 80 THEN 1
>
> WHEN amt &gt; 900 AND EXTRACT(HOUR FROM trans_date_trans_time) BETWEEN 0 AND 4
>
> AND UNIFORM(0, 100, RANDOM()) &lt; 75 THEN 1
>
> WHEN category IN ('shopping_net', 'misc_net', 'travel') AND amt &gt; 400 AND amt &lt;= 700
>
> AND UNIFORM(0, 100, RANDOM()) &lt; 12 THEN 1
>
> WHEN EXTRACT(HOUR FROM trans_date_trans_time) BETWEEN 0 AND 3
>
> AND UNIFORM(0, 100, RANDOM()) &lt; 3 THEN 1
>
> ELSE 0
>
> END as is_fraud
>
> FROM raw_data;
>
> Then select each subsection separately and run them one by one by choosing Run.
>
> After the queries run successfully, confirm the setup by running the following verification queries.
>
> SELECT COUNT(*) as total_records FROM FRAUD_TABLE;
>
> SELECT TOP 10 * FROM FRAUD_TABLE;
>
> SELECT is_fraud, COUNT(*) as count FROM FRAUD_TABLE GROUP BY is_fraud;
>
> Gather the information needed to connect from Snowflake to Amazon SageMaker Canvas. The connection requires the Snowflake organization account name, which combines the Snowflake organization name and account name with a hyphen. Run the SQL query in the worksheet to determine the organization account name.
>
> SELECT CURRENT_ORGANIZATION_NAME()||'-'||CURRENT_ACCOUNT_NAME() AS organizaton_account_name;
>
> Conclusion
>
> In this first part of the three-part series, you explored the business challenge facing organizations with data-rich Snowflake environments and introduced a no-code ML workflow. You created a Snowflake database, loaded sample fraud detection data, and retrieved the connection details needed for the next steps.
>
> In Part 2, you connect Amazon SageMaker Canvas to Snowflake data, prepare and transform the dataset using visual tools, and build a fraud detection model.
>
> References
>
> Part 2 – Build a no-code ML workflow with Snowflake, Amazon SageMaker Canvas and Amazon Quick – Part 2: Data preparation and model building with Amazon SageMaker Canvas
>
> Part 3 – Build a no-code ML workflow with Snowflake, Amazon SageMaker Canvas and Amazon Quick – Part 3: Visualizing insights with Amazon Quick Sight
>
> About the authors
>
> Anu Kaggadasapura Nagaraja
>
> Anu is a Healthcare and Life Sciences (HCLS) Solutions Architect II at AWS with more than six years of experience specializing in AI, generative AI, and machine learning. She helps organizations across multiple industries build scalable, cloud-driven solutions. Anu focuses on AI innovation through modern data platforms, agentic AI architectures, and emerging cloud technologies. Outside of work, Anu enjoys playing badminton and hiking.
>
> Aysha Siddiqui
>
> Aysha is a Solutions Architect at Amazon Web Services, where she partners with enterprise customers to design scalable, resilient cloud architectures. She is passionate about AI/ML and generative AI, and focuses on helping organizations move these workloads from experimentation to production. Outside of work, she enjoys traveling and perfecting her matcha-making skills.
>
> Shruti Tambe
>
> Shruti is a Solutions Architect at AWS, where she helps SMB customers to build and scale their products on cloud. She works with organizations on cloud architecture design, modernization, and AI adoption to drive meaningful business outcomes. In her free time, Shruti enjoys hiking and running.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。