---
title: "How Decathlon runs demand forecasting at scale with Chronos-2"
date: 2026-08-29T02:43:35+08:00
draft: false
entry_kind: "auto"
tags: ["生成式 AI", "机器学习", "Amazon SageMaker", "Customer Solutions", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:55627cbc159c92226aeb41daf91f3df4953a2bac24424bb792d2bd407b5b6882"
source_payload_sha256: "sha256:2af1ab67645abd50aa3a595062cd4941e9d96d76e0f22de84dc6bf0c69bf2a48"
observation_id: obs_7625e7226ac0a816ad72721ec4c5f9ea2e93abbdfb23fec89e479619170b821d
event_id: evt_98a64dc1e2aa37466b9fd3f7afad558451e6c8a6fd41107de8b4ad95b1160f56
revision_id: rev_7c3c9eb8af4553b3dd492d48f3885f82e0fef12fb3746d08e715f474899aef13
source_published_at: 2026-08-28T16:22:30Z
first_seen_at: 2026-08-28T18:41:19.364201Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 61
interpretation_sha256: "sha256:c78a87cf15d3e2d239a89aa2bbb4d9bb3765b870d8f2294c1001bdc11db53bf4"
description: "Decathlon 采用时间序列基础模型 Chronos-2 构建需求预测系统，替代原有的深度学习与传统统计方法混合方案，以更低运维成本实现跨区域、多品类的销量预测。"
external_url: https://aws.amazon.com/blogs/machine-learning/how-decathlon-runs-demand-forecasting-at-scale-with-chronos-2
parent_observation_id: null
last_seen_at: 2026-08-28T18:41:19.364201Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/how-decathlon-runs-demand-forecasting-at-scale-with-chronos-2](https://aws.amazon.com/blogs/machine-learning/how-decathlon-runs-demand-forecasting-at-scale-with-chronos-2)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么
Decathlon 采用时间序列基础模型 Chronos-2 构建需求预测系统，替代原有的深度学习与传统统计方法混合方案，以更低运维成本实现跨区域、多品类的销量预测。

### 用在哪里
适用于零售供应链的批量预测场景，为采购计划和长期库容规划提供 12 周与 52 周两种预测周期，支持欧洲、亚洲、拉美等多地区的数万种产品。

### 可以推断的
推测：时间序列基础模型在零售预测任务中已具备替代定制化模型的潜力，预训练加轻量微调的范式可显著降低企业 AI 落地的工程复杂度。  
推测：该方案对其他拥有类似业务规模和产品多样性的零售企业具有参考价值，尤其是在需要统一框架处理差异化需求信号的场景。

## 来源摘要/节选

> This post is co-written with Vianney Bruned, Filippo Giruzzi, Belkiss Saidi, and Carlos Ramirez from Decathlon.
>
> Decathlon is one of the world’s largest sporting goods retailers, with more than 100,000 teammates and 400 million users worldwide. The company relies on accurate demand forecasting at scale to support the availability of the appropriate products in each store at the time customers need them. After evaluating multiple time series foundation models (TSFMs), Decathlon selected Chronos-2 as a core component of their forecasting stack.
>
> In this post, we share the architecture Decathlon uses to run Chronos-2 at scale on AWS, the business impact on Decathlon’s supply chain operations, and practical lessons learned for other companies that want to adopt foundation models for forecasting.
>
> Decathlon’s forecasting challenge
>
> Accurate demand forecasting is the backbone of retail supply chain operations. For Decathlon, this challenge is amplified by the sheer scale and diversity of their business: tens of thousands of products spanning over 80 sports, sold across multiple continents with highly seasonal demand patterns. A pair of ski gloves and a surfboard have fundamentally different demand signals, yet both must be forecasted accurately to avoid stockouts or overstock.
>
> Decathlon’s forecasting system predicts the weekly sales quantity of all products on two critical horizons. The first is a 12-week replenishment window used by purchase planners to order goods from industrial partners. The second is a 52-week strategic horizon for long-term stock projection and capacity planning. The forecasting system runs weekly across both horizons. It’s deployed across multiple supply zones, including Europe, India, China, South East Asia (SEA), Latin America (LATAM), and soon the Middle East and Africa. Each zone covers up to 25,000 products.
>
> Previous approach and its limitations
>
> Decathlon’s demand forecasting system evolved over several years:
>
> 2021–2024: A hybrid approach using Amazon SageMaker AI DeepAR for the short-term forecast horizon (weeks 1–16) and Holt-Winters exponential smoothing for the longer-term horizon (weeks 17–52). DeepAR was retrained weekly to adapt to recent trend shifts.
>
> 2024 onwards: Introduction of Temporal Fusion Transformer (TFT) with covariates, offering improved long-horizon accuracy.
>
> While these approaches served Decathlon well, they came with operational overhead: the system required weekly re-training and could not easily scale to new regions without extra engineering effort. The team needed a solution that could deliver higher accuracy with lower operational complexity.
>
> Why Chronos-2: Model evaluation and selection
>
> The rise of time series foundation models (FMs) promised pre-trained models that could outperform classical approaches without training from scratch on domain-specific data. But a critical question remained: would these models work on Decathlon’s specific retail datasets?
>
> To answer this, Decathlon designed a rigorous, large-scale benchmark on its own retail data, evaluating multiple TSFMs against its production baseline.
>
> Benchmark design
>
> Evaluation: 101 rolling cutoffs spanning nearly 2 years (week 48 of 2022 to week 44 of 2024).
>
> Scale: Approximately 25,000 unique products per cutoff (39,000 unique product time series across the full evaluation period).
>
> Horizon: 12-week and 52-week horizons at weekly frequency.
>
> Primary metric: Weighted Absolute Percentage Error (WAPE) at 12-week and 52-week horizons, supplemented by root mean square error (RMSE), bias, and pairwise winning rates.
>
> For full benchmark results including comparisons across multiple TSFMs, see Decathlon’s detailed analysis on Medium.
>
> Key findings
>
> Decathlon evaluated multiple TSFMs in both zero-shot and fine-tuned configurations. In Decathlon’s published benchmark results, Chronos-2 fine-tuned consistently outperformed all other evaluated models across both horizons. Even in zero-shot mode, it matched or surpassed the fully trained production baseline. Fine-tuning further reduced forecast error by several percentage points.
>
> Zero-shot viability: Several TSFMs exceeded or approached the performance of Decathlon’s existing production model (retrained weekly) without any domain-specific training.
>
> Fine-tuning delivered significant gains: Even with a low-frequency fine-tuning schedule (once every 6 months), fine-tuning significantly improved performance. Chronos-2 fine-tuned showed the lowest error across both short-term (12-week) and long-term (52-week) horizons.
>
> Computational efficiency: Chronos-2 can run on both CPUs and GPUs, and met the benchmark’s efficiency requirement of under 2 minutes of inference per cutoff for 25,000 products.
>
> Beyond raw accuracy, Chronos-2’s native covariate support through its group attention mechanism was a key differentiator. Unlike most TSFMs that require workarounds, Chronos-2 natively incorporates covariates. The combination of leading accuracy, architectural elegance for covariate handling, and efficient fine-tuning made Chronos-2 the clear choice for Decathlon’s production stack.
>
> Solution architecture
>
> Decathlon’s production deployment of Chronos-2 on AWS is designed to be efficient, cost-efficient, and reliable.
>
> The following diagram shows the high-level architecture of the demand forecasting pipeline. A PySpark data preparation pipeline assembles the input time series. Every 6 months, a fine-tuning job built on AutoGluon adapts Chronos-2 to the latest data and registers the resulting model in an MLflow model registry. In the intervening weeks, this step is skipped. The inference pipeline fetches the latest registered model and runs weekly batch forecasts, and a PySpark exposition pipeline delivers the forecasts to downstream consumers.
>
> Figure 1: High-level architecture of Decathlon’s demand forecasting pipeline on AWS
>
> Infrastructure and deployment pattern
>
> Component
>
> Details
>
> Compute
>
> Amazon Elastic Compute Cloud (Amazon EC2) m6i.8xlarge (CPU-based inference), g5.4xlarge (GPU-based fine-tuning)
>
> Execution mode
>
> Weekly batch inference
>
> Inference runtime
>
> ~40 seconds for 7,000 time series (LATAM), ~75 seconds for 15,000 time series (SEA)
>
> Batch size
>
> ~12,000 time series per execution
>
> Model
>
> Chronos-2 fine-tuned with LoRA through AutoGluon
>
> Fine-tuning cadence
>
> Every 6 months
>
> Regions served
>
> SEA, LATAM (Middle East and Africa planned)
>
> The architecture uses Amazon EC2 instances for batch inference, triggered by Databricks jobs. Data pipelines are orchestrated through Airflow on Decathlon’s existing data platform. The fine-tuning process uses Low-Rank Adaptation (LoRA) through the AutoGluon Chronos integration, allowing efficient adaptation to Decathlon’s domain without full model re-training. The model is fine-tuned automatically every 6 months on the latest data, and the different models are logged and versioned per supply zone with specific hyperparameters through MLflow.
>
> Chronos-2 technical overview
>
> Chronos-2 is an encoder-only transformer closely following the T5 encoder design. It’s available in multiple variants, including the base model (amazon/chronos-2) with 120M parameters and a small model (autogluon/chronos-2-small) with 28M parameters. Unlike the original Chronos, which quantized values into discrete tokens, Chronos-2 applies robust scaling to each series. It then splits each series into non-overlapping patches that are mapped to real-valued embeddings through a residual network. Forecasts are produced as continuous quantiles by a quantile head. The key architectural innovation is the alternating attention pattern. Each transformer block alternates between time attention (along the temporal axis within a single series) and group attention (across series within a group at each patch index).
>
> The following diagram illustrates this design. Related time series and their covariates are grouped together. Information is exchanged both along time within each series and across the series in a group, allowing native multivariate forecasting with covariates.
>
> Figure 2: Chronos-2 architecture for native multivariate forecasting with covariates
>
> Getting started with Chronos-2
>
> As of this writing, Chronos-2 models have been downloaded over 120 million times from Hugging Face and are available for Amazon SageMaker AI customers through AutoGluon-Cloud or Amazon SageMaker JumpStart.
>
> The following code adapted from the Chronos-2 quickstart notebook on GitHub, demonstrates how to run inference with covariate support. In production, Decathlon uses the AutoGluon Chronos integration for fine-tuning and inference orchestration with a slightly different API:
>
> import pandas as pd
>
> from chronos import BaseChronosPipeline, Chronos2Pipeline
>
> # Load the Chronos-2 pipeline
>
> pipeline: Chronos2Pipeline = BaseChronosPipeline.from_pretrained(
>
> "amazon/chronos-2",
>
> device_map="cpu"
>
> )
>
> # Historical data
>
> df = pd.read_csv("sales.csv") # columns: item_id, timestamp, sales, price, store_count
>
> # Data available during the forecast horizon
>
> future_df = pd.read_csv("future.csv") # columns: item_id, timestamp, price, store_count
>
> prediction_length = 52
>
> forecast = pipeline.predict_df(df, future_df, target="sales", prediction_length=prediction_length)
>
> Fine-tuning with AutoGluon
>
> Decathlon uses AutoGluon-TimeSeries to fine-tune and serve Chronos-2. With AutoGluon, you can streamline the end-to-end machine learning workflow, from data preparation to model training and deployment. Using its TimeSeries module’s high-level API, you can handle data formatting, covariate management, and fine-tuning with LoRA in a few lines of code:
>
> # pip install autogluon.timeseries
>
> from autogluon.timeseries import TimeSeriesDataFrame, TimeSeriesPredictor
>
> tsdf = TimeSeriesDataFrame.from_data_frame(df, id_column="item_id", timestamp_column="timestamp")
>
> future_tsdf = TimeSeriesDataFrame.from_data_frame(future_df, id_column="item_id", timestamp_column="timestamp")
>
> predictor = TimeSeriesPredictor(
>
> prediction_length=52, # forecast horizon
>
> target="sales", # column to forecast
>
> known_covariates_names=["price", "store_count"], # features known in the future
>
> )
>
> predictor.fit(
>
> tsdf,
>
> hyperparameters={
>
> "Chronos2": {
>
> "model_path": "amazon/chronos-2",
>
> "fine_tune": True, # Turn on fine-tuning; if False the model is used in zero-shot mode
>
> }
>
> },
>
> )
>
> predictor.predict(tsdf, known_covariates=future_tsdf)
>
> Results and business impact
>
> Decathlon measured the impact of the Chronos-2 deployment along three dimensions: forecast accuracy, business outcomes, and operational efficiency.
>
> Forecast accuracy improvements
>
> Decathlon’s deployment of Chronos-2 fine-tuned has delivered significant accuracy gains across both regions and horizons, in comparison with the previously used legacy forecasting tool:
>
> Region
>
> Horizon
>
> Previous WAPE
>
> Chronos-2 WAPE
>
> WAPE Reduction
>
> SEA
>
> 12 weeks
>
> 39%
>
> 28%
>
> 11 pp
>
> LATAM
>
> 12 weeks
>
> 53%
>
> 38%
>
> 15 pp
>
> SEA
>
> 52 weeks
>
> 44%
>
> 38%
>
> 6 pp
>
> LATAM
>
> 52 weeks
>
> 55%
>
> 46%
>
> 9 pp
>
> pp = percentage points
>
> Business impact
>
> Each percentage point of WAPE improvement at the 12-week horizon translates to:
>
> 0.3 days of inventory savings, reducing working capital and warehousing costs.
>
> 0.3 points of product availability, fewer stockouts on shelves.
>
> 0.4 points of sales increase for each point of availability gained, which is approximately 0.12 points of sales per WAPE point (average across all zones).
>
> With 11–15 points of WAPE improvement at the replenishment horizon, the compounding effect on inventory efficiency, availability, and revenue is substantial.
>
> Operational efficiency
>
> Beyond accuracy, the migration to Chronos-2 reduced operational overhead across several dimensions:
>
> Metric
>
> Before (TFT)
>
> After (Chronos-2)
>
> Deployment time new region
>
> ~6 months (three people)
>
> 2–3 months (data scientist, ML engineer, data analyst)
>
> Inference runtime
>
> 10 min (10k series) to 15 min (25k series) including re-training
>
> ~40s (7K series) to ~75s (15K series)
>
> Fine-tuning frequency
>
> Weekly
>
> Every 6 months
>
> Engineering complexity
>
> High (multi-seed training and inference)
>
> Low (single model, LoRA fine-tuning, no GPU constraint)
>
> The reduction in deployment time from 6 months to 2–3 months is particularly impactful for Decathlon’s expansion into new markets. With Chronos-2, the team can deploy forecasting capabilities to a new region by running fine-tuning on local historical data with no architecture redesign required.
>
> Production timeline
>
> Chronos-2 is already in production for the South East Asia and Latin America supply zones, which are the regions the preceding results are drawn from. Decathlon is now extending the solution across its remaining supply zones, with full multi-zone production rollout targeted for 2026 and the Middle East and Africa regions as the next expansion targets.
>
> Conclusion and lessons learned
>
> Decathlon’s journey demonstrates that time series foundation models, and Chronos-2 in particular, are ready for production-grade retail demand forecasting. By combining a rigorous model evaluation process with efficient fine-tuning with LoRA, Decathlon achieved 11–15 points of WAPE improvement at the 12-week horizon. At the same time, the team reduced deployment time from 6 months to 2–3 months per region. For retailers evaluating foundation models for forecasting, Decathlon’s experience offers a practical blueprint.
>
> Lessons learned
>
> Benchmark on your own data: Global leaderboards are useful for shortlisting candidates, but model rankings can differ significantly on domain-specific data. In Decathlon’s case, some models that ranked higher globally performed worse on retail distribution datasets. Testing across 25,000 products and 101 cutoffs also revealed that Chronos-2’s straightforward fine-tuning with AutoGluon was a decisive advantage, turning a strong zero-shot model into the clear leader.
>
> Fine-tuning unlocks the full potential: Even infrequent fine-tuning (every 6 months) with Low-Rank Adaptation (LoRA) measurably improves accuracy over zero-shot inference. The combination of a strong pre-trained foundation with domain adaptation is the winning formula.
>
> Start with a focused approach, iterate: Decathlon began with a single fine-tuned model in production and is progressively adding covariates. This pragmatic approach reduces risk while delivering value early.
>
> Foundation models democratize forecasting: Running Chronos-2 on a single m6i.8xlarge CPU instance with inference times of 40–75 seconds for 7,000–15,000 time series makes forecasting at this scale accessible without GPU infrastructure. At approximately $0.03 per weekly inference run, the compute cost is negligible.
>
> Next steps
>
> Looking ahead, Decathlon plans to deploy a Mixture of Experts (MoE) ensembling approach in production. Their benchmarks show that combining multiple TSFMs consistently outperforms the single best expert, with other models still winning on roughly 40 percent of products. The team is also expanding to Middle East and Africa regions and integrating external data such as price or weather as covariates. In addition, they are exploring Chronos-2’s cross-learning capabilities for cold-start products.
>
> To explore Chronos-2 for your own forecasting use cases or to learn more about Chronos-2, visit the Amazon Science blog post, the research paper, or try the quickstart notebook. For fine-tuning with AutoGluon, see the AutoGluon Chronos tutorial.
>
> About the authors
>
> Vianney Bruned
>
> Vianney is a Staff Data Scientist at Decathlon, leading the demand forecasting team. He specializes in time series forecasting and machine learning for supply chain optimization.
>
> Filippo Giruzzi
>
> Filippo is a Machine Learning Engineer at Decathlon. He works on time series foundation models and worldwide deployment of the demand forecasting solution.
>
> Belkiss Saidi
>
> Belkiss is a Machine Learning Engineer at Decathlon. She works on time series foundation models and model ensembling strategies for demand forecasting.
>
> Carlos Ramirez
>
> Carlos is a Machine Learning Engineer at Decathlon. He architects scalable and advanced ML pipelines to extend demand forecasting models into sales forecasting pipelines.
>
> Ioan Catana
>
> Ioan is a Senior Artificial Intelligence and Machine Learning Specialist Solutions Architect at AWS. He helps customers develop and scale their ML solutions and generative AI applications in the AWS Cloud. Ioan has over 25 years of experience, mostly in software architecture design and cloud engineering.
>
> Abdul Fatir Ansari
>
> Abdul is a Senior Applied Scientist at Amazon Web Services, specializing in machine learning and forecasting, with a focus on foundation models for structured data, such as time series. He received his PhD from the National University of Singapore, where his research centered on deep generative models for images and time series.
>
> Oleksandr Shchur
>
> Oleksandr is a Senior Applied Scientist at Amazon Web Services, where he works on time series forecasting in AutoGluon. Before joining AWS, he completed a PhD in Machine Learning at the Technical University of Munich, Germany, doing research on probabilistic models for event data. His research interests include machine learning for temporal data and generative modeling.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。