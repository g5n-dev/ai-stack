---
title: "Build an explainable next-best-product recommendation system for banking on AWS"
date: 2026-07-25T12:31:13+08:00
draft: false
entry_kind: "auto"
tags: ["Advanced (300)", "Amazon SageMaker AI", "AWS Glue", "Technical How-to", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:bd99804b6636a6769b863b7a7902095d4fcc73395117ccdb26f41424cf6480c5"
source_payload_sha256: "sha256:1362fc901a66853609402178932ff2410867318dbffd45d257ac0a23264ee65a"
observation_id: obs_af4a9a88db710c3f635710f26c3856c4209f9f3be2678ef2b6531206b30d5375
event_id: evt_dd0b61de9eb1cb5023eaa7e85cb2ad03fb549e5c21fe2df6a80f6965c3012ebb
revision_id: rev_4ffc3d7c7e820854a2dcc5e0b233a3ba191043b16b30153fe9b833c7f7d6f953
source_published_at: 2026-07-24T15:42:11Z
first_seen_at: 2026-07-25T04:46:53Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: true
source_truncation_reason: "crawler_feed_content_limit"
source_support: 1.0
source_title_chars_original: 79
description: "当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。"
external_url: https://aws.amazon.com/blogs/machine-learning/build-an-explainable-next-best-product-recommendation-system-for-banking-on-aws
parent_observation_id: null
last_seen_at: 2026-07-28T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/build-an-explainable-next-best-product-recommendation-system-for-banking-on-aws](https://aws.amazon.com/blogs/machine-learning/build-an-explainable-next-best-product-recommendation-system-for-banking-on-aws)

## 来源摘要/节选

> Building a deep learning-based explainable next-best-product recommendation system helps banking institutions predict which product a customer needs next. Banks hold vast amounts of customer data, including transaction histories, product ownership records, demographic profiles, and behavioral patterns. Translating this data into actionable, personalized product recommendations remains a significant challenge. Traditional rule-based systems and collaborative filtering approaches often fail to capture the complex temporal patterns in customer product adoption journeys.
>
> In this post, we present the architecture and design decisions behind a Next-Best-Product (NBP) recommendation system using Amazon SageMaker AI and PyTorch. We explain the reasoning behind a multi-tower neural network architecture, how learned attention provides per-customer explainability, and how AWS services work together to take this solution from research to production. This is an architectural overview, not a step-by-step deployment guide. Whether you are building recommendation systems for financial services or other domains with heterogeneous customer data, the architectural patterns described here can help you design more accurate and interpretable models.
>
> Prerequisites
>
> To follow along with the architectural patterns and code examples in this post, you need:
>
> An AWS account with permissions for SageMaker AI, Amazon Simple Storage Service (Amazon S3), AWS Glue, and Amazon CloudWatch
>
> This solution requires an AWS Identity and Access Management (IAM) execution role with access to the following AWS services. Create policies with least-privilege permissions scoped to only the resources needed for this solution.
>
> SageMaker AI – Create, describe, start, stop, and delete training jobs, processing jobs, batch transform jobs, models, endpoints, endpoint configurations, pipelines, experiments, and monitoring schedules. InvokeEndpoint for real-time inference.
>
> Amazon S3 – Read and write access to the data bucket. Create and delete bucket. List, upload, download, and delete objects.
>
> AWS Glue – Create, run, and delete ETL jobs. Create and delete crawlers. Create and delete Data Catalog databases and tables.
>
> CloudWatch – Read and write access to log groups, log streams, and metrics. Delete log groups during cleanup.
>
> IAM – Create and delete roles. Attach and detach policies. PassRole (restricted to the named execution role ARN, scoped to sagemaker.amazonaws.com and glue.amazonaws.com).
>
> For guidance on writing least-privilege IAM policies for SageMaker AI, see Identity-based policy examples for SageMaker AI.
>
> Familiarity with Python 3.11+ and PyTorch
>
> Required packages to create this recommender system:
>
> Python 3.11+
>
> PyTorch 2.9+
>
> Pandas 2.3+
>
> NumPy 2.3+
>
> scikit-learn 1.7+
>
> Dask 2025.11+
>
> We recommend using a virtual environment and scanning dependencies for known vulnerabilities using tools like pip-audit before deployment.
>
> Basic understanding of deep learning concepts (embeddings, recurrent networks, attention mechanisms)
>
> Note: Deploying this solution creates billable AWS resources including SageMaker AI training jobs (ml.g5.12xlarge GPU instances), SageMaker AI endpoints, Amazon S3 storage, and AWS Glue jobs. Follow the clean up instructions at the end of this post to avoid ongoing charges.
>
> Solution overview
>
> The solution uses a multi-tower deep learning architecture with four specialized neural network towers, each processing a different aspect of customer data. The towers are fused using a learned attention mechanism that provides both high accuracy and per-customer explainability.
>
> The following diagram illustrates the high-level architecture of the solution.
>
> The architecture addresses a common challenge in banking: predicting which product a customer is most likely to purchase next from multiple product categories (such as credit cards, deposits, insurance, loans, and mortgages), while providing explainable results that satisfy regulatory requirements.
>
> Tech stack
>
> The following table summarizes the technology choices and their roles in the solution.
>
> Component
>
> Technology
>
> Purpose
>
> ETL &amp; Data Processing
>
> AWS Glue (PySpark)
>
> Serverless Spark-based ETL for data unification, service mapping, feature engineering at scale
>
> Deep Learning Framework
>
> PyTorch
>
> Dynamic computation graphs, research-to-production flexibility, native GPU support
>
> Feature Engineering
>
> Pandas, Dask, PyArrow
>
> ML-specific feature engineering (sequence creation, windowed aggregations)
>
> ML Utilities
>
> scikit-learn
>
> Label encoding, standard scaling, train/test split, evaluation metrics
>
> Training Compute
>
> SageMaker AI (ml.g5.12xlarge)
>
> 192 GB RAM, 4× NVIDIA A10G GPUs
>
> Data Storage
>
> Amazon S3
>
> Snappy-compressed Parquet files for raw, intermediate, and processed data
>
> Data Catalog
>
> AWS Glue Data Catalog
>
> Schema management, table metadata, crawlers for auto-discovery
>
> Model Registry
>
> SageMaker AI model registry
>
> Versioned model artifacts, approval workflows
>
> Inference
>
> SageMaker AI Batch Transform / endpoint
>
> Batch and near-real-time predictions
>
> Orchestration
>
> Amazon SageMaker Pipelines
>
> End-to-end ML pipeline orchestration
>
> Monitoring
>
> CloudWatch
>
> Training metrics, inference latency, model drift detection
>
> Why PyTorch?
>
> This solution uses PyTorch for dynamic computation graphs (needed for variable-length sequences with pack_padded_sequence), rapid iteration across multiple architectural phases, and native integration with SageMaker AI training jobs and inference containers.
>
> Why Parquet on Amazon S3?
>
> The solution stores data as Snappy-compressed Parquet on Amazon Simple Storage Service (Amazon S3). Parquet’s columnar format enables column pruning (reading a fraction of a wide file), predicate pushdown (skipping irrelevant row groups), 3-5× compression over CSV, and type preservation without re-parsing on every read.
>
> Why AWS Glue for ETL?
>
> The project uses AWS Glue jobs running on PySpark for serverless, auto scaling data processing. AWS Glue provides native Spark integration, the DynamicFrame API for flexible schemas, automatic Data Catalog registration, job bookmarks for incremental processing, and pay-per-DPU cost efficiency.
>
> Data pipeline architecture
>
> The data pipeline consists of two stages: an AWS Glue ETL job for data unification, followed by an Amazon SageMaker Processing job for ML-specific feature engineering.
>
> Data unification with AWS Glue
>
> Banking data typically arrives from multiple source systems with inconsistent schemas. The AWS Glue ETL job normalizes schemas, maps raw transaction types to unified service categories, combines all data into a single chronological record per customer, and engineers temporal features. The processed output is written as Parquet to Amazon S3 and registered in the AWS Glue Data Catalog.
>
> ML-specific feature engineering with Amazon SageMaker Processing
>
> After the AWS Glue job produces the unified history, an Amazon SageMaker Processing job creates product adoption sequences per customer, computes time-windowed transaction aggregations (across 7, 30, 60, 180, and 365-day windows) using Dask for parallelism, and pads sequences to a fixed length for model input.
>
> Handling large scale data
>
> For large datasets that exceed available memory, the solution uses a parallel chunked processing strategy with PyArrow for metadata inspection, ProcessPoolExecutor for parallel chunk processing, explicit garbage collection between batches, and incremental merging to avoid memory spikes.
>
> import gc
>
> from concurrent.futures import ProcessPoolExecutor
>
> chunksize = 5_000_000
>
> n_workers = 4
>
> for batch_start in range(0, total_chunks, n_workers):
>
> with ProcessPoolExecutor(max_workers=n_workers) as executor:
>
> futures = [
>
> executor.submit(process_chunk_range, input_path, output_path, i, start_row, end_row)
>
> for i in range(batch_start, min(batch_start + n_workers, total_chunks))
>
> ]
>
> for future in futures:
>
> future.result()
>
> gc.collect() # Force garbage collection between batches
>
> Note: When working with real customer data, see the Security considerations section for guidance on PII handling, regulatory compliance, and data governance.
>
> Model architecture
>
> The model uses a multi-tower approach where each tower specializes in processing one type of customer data, followed by an attention-based fusion mechanism.
>
> Why multi-tower over a single network?
>
> Different types of customer data have fundamentally different structures. Sequences are ordered lists of discrete IDs. Transactions are numerical aggregations. Demographics are a mix of categorical and numerical features. Behavioral segments are categorical codes.
>
> Forcing all these through the same layers wastes model capacity. Instead, the architecture uses four specialized towers, each designed for its data type:
>
> Tower
>
> Input Type
>
> Architecture
>
> Output
>
> Sequence Tower
>
> Product adoption history (padded to fixed length)
>
> nn.Embedding → 2-layer GRU → Fusion with active product count
>
> 64-dim vector
>
> Transaction Tower
>
> Time-windowed transaction features
>
> 2-layer MLP (128 → 64) with ReLU and Dropout
>
> 64-dim vector
>
> Customer Tower
>
> Demographics, income, family, account features
>
> 2-layer MLP (128 → 64) with ReLU and Dropout
>
> 64-dim vector
>
> Behavioral Tower
>
> Segmentation codes, loyalty, usage patterns
>
> 2-layer MLP (128 → 64) with ReLU and Dropout
>
> 64-dim vector
>
> Sequence Tower: Capturing temporal patterns
>
> The Sequence Tower processes the customer’s product adoption history using a 2-layer Gated Recurrent Unit (GRU). This is the core architectural component because it captures the order in which customers adopt products, not just which products they own.
>
> class SequenceTower(nn.Module):
>
> def __init__(self, num_products, embedding_dim=32, hidden_dim=64, dropout=0.2):
>
> super().__init__()
>
> self.embedding = nn.Embedding(num_products + 1, embedding_dim, padding_idx=0)
>
> self.gru = nn.GRU(
>
> input_size=embedding_dim, hidden_size=hidden_dim,
>
> num_layers=2, batch_first=True, dropout=dropout
>
> )
>
> self.active_count_layer = nn.Sequential(
>
> nn.Linear(1, hidden_dim // 2), nn.ReLU(), nn.Dropout(dropout)
>
> )
>
> self.fusion = nn.Sequential(
>
> nn.Linear(hidden_dim + hidden_dim // 2, hidden_dim),
>
> nn.ReLU(), nn.Dropout(dropout)
>
> )
>
> def forward(self, sequence, seq_length, active_count):
>
> embedded = self.embedding(sequence)
>
> packed = nn.utils.rnn.pack_padded_sequence(
>
> embedded, seq_length.cpu().clamp(min=1),
>
> batch_first=True, enforce_sorted=False
>
> )
>
> _, hidden = self.gru(packed)
>
> seq_features = hidden[-1]
>
> active_features = self.active_count_layer(active_count)
>
> return self.fusion(torch.cat([seq_features, active_features], dim=1))
>
> Why GRU over LSTM?
>
> GRU has two gates (reset, update) versus LSTM’s three (input, forget, output), resulting in approximately 33% fewer parameters. For short sequences (20 items or fewer), GRU performs comparably to LSTM while training faster. The update gate’s interpolation mechanism also creates a natural residual-like gradient path.
>
> Why pack_padded_sequence?
>
> Customer sequences have variable lengths. Packing tells the GRU to ignore padding tokens, preventing the model from learning noise from zero-padded positions.
>
> Tower Attention Mechanism: Learned fusion with explainability
>
> Instead of simple concatenation, the architecture uses a learned attention mechanism to fuse tower outputs. This is what provides per-customer explainability without requiring post-hoc interpretation methods like SHAP or LIME.
>
> class TowerAttentionMechanism(nn.Module):
>
> def __init__(self, hidden_dim=64, num_heads=4, dropout=0.1):
>
> super().__init__()
>
> self.tower_attention = nn.MultiheadAttention(
>
> embed_dim=hidden_dim, num_heads=num_heads,
>
> dropout=dropout, batch_first=True
>
> )
>
> self.context_weighting = nn.Sequential(
>
> nn.Linear(hidden_dim * 4, 4), nn.Softmax(dim=1)
>
> )
>
> def forward(self, tower_outputs):
>
> stacked = torch.stack(tower_outputs, dim=1) # [batch, 4, 64]
>
> attended, _ = self.tower_attention(stacked, stacked, stacked)
>
> stacked = stacked + attended # Residual connection
>
> concat = torch.cat(tower_outputs, dim=1) # [batch, 256]
>
> tower_weights = self.context_weighting(concat) # [batch, 4]
>
> weighted_outputs = [
>
> tower_outputs[i] * tower_weights[:, i:i+1]
>
> for i in range(4)
>
> ]
>
> return weighted_outputs, tower_weights
>
> The tower weights are per-customer. A customer with rich transaction history gets a high transaction tower weight, while a new customer with few transactions but clear demographics gets a high customer tower weight. This adaptivity improves accuracy and provides natural explainability for relationship managers and regulators.
>
> Context-Aware Fusion: Residual blocks for stable training
>
> The weighted tower outputs pass through a fusion network with residual connections. Residual connections help with gradient flow during training and allow the network to learn identity mappings when additional depth is not needed.
>
> class ContextAwareFusion(nn.Module):
>
> def __init__(self, hidden_dim=64, dropout=0.2):
>
> super().__init__()
>
> self.initial_projection = nn.Linear(hidden_dim * 4, hidden_dim)
>
> self.fusion1 = nn.Sequential(
>
> nn.Linear(hidden_dim, hidden_dim * 2), nn.LayerNorm(hidden_dim * 2),
>
> nn.ReLU(), nn.Dropout(dropout), nn.Linear(hidden_dim * 2, hidden_dim)
>
> )
>
> self.layer_norm1 = nn.LayerNorm(hidden_dim)
>
> self.fusion2 = nn.Sequential(
>
> nn.Linear(hidden_dim, hidden_dim), nn.ReLU(), nn.Dropout(dropout)
>
> )
>
> self.layer_norm2 = nn.LayerNorm(hidden_dim)
>
> def forward(self, weighted_outputs):
>
> concat = torch.cat(weighted_outputs, dim=1)
>
> projected = self.initial_projection(concat)
>
> out1 = self.layer_norm1(projected + self.fusion1(projected)) # Residual
>
> out2 = self.layer_norm2(out1 + self.fusion2(out1)) # Residual
>
> return out2
>
> Feature Importance Module: Built-in explainability
>
> Banking regulators require model explainability. Rather than relying on post-hoc methods, the architecture includes a Feature Importance Module that produces per-customer importance scores summing to 1.0 as part of the forward pass.
>
> class FeatureImportanceModule(nn.Module):
>
> def __init__(self, hidden_dim=64):
>
> super().__init__()
>
> self.feature_contribution = nn.Sequential(
>
> nn.Linear(hidden_dim, 4), nn.Softmax(dim=1)
>
> )
>
> def forward(self, fused_features, tower_weights):
>
> feature_importance = self.feature_contribution(fused_features)
>
> return feature_importance * tower_weights
>
> This produces outputs like: “For this customer, 40% of the recommendation was driven by their product sequence, 30% by transaction patterns, 20% by demographics, 10% by behavioral segment.” Relationship managers can use this to tailor their conversations with each customer.
>
> Training strategy
>
> The following table summarizes the training configuration and the rationale behind each choice.
>
> Parameter
>
> Value
>
> Rationale
>
> Optimizer
>
> Adam (lr=0.001, weight_decay=1e-5)
>
> Adaptive per-parameter learning rates, light L2 regularization
>
> Loss
>
> CrossEntropyLoss
>
> Standard for multi-class classification, numerically stable
>
> LR Scheduler
>
> ReduceLROnPlateau (factor=0.5, patience=3)
>
> Automatically halves LR when validation loss plateaus
>
> Gradient Clipping
>
> max_norm=1.0
>
> Prevents gradient explosion with GRU and attention
>
> Early Stopping
>
> patience=5
>
> Stops training when validation loss stops improving
>
> Batch Size
>
> 32
>
> Fits comfortably in A10G’s VRAM
>
> Data Split
>
> 80% train / 10% validation / 10% test
>
> Standard split for reproducibility
>
> All random seeds are fixed (PyTorch, NumPy, CUDA) for full reproducibility across training runs.
>
> The training process uses SageMaker AI with ml.g5.12xlarge instances. The SageMaker AI Python SDK provides a PyTorch Estimator that packages the training code, provisions GPU instances, runs training, and stores model artifacts to Amazon S3 automatically.
>
> from sagemaker.pytorch import PyTorch
>
> estimator = PyTorch(
>
> entry_point='train.py',
>
> source_dir='src/',
>
> role=role,
>
> instance_count=1,
>
> instance_type='ml.g5.12xlarge',
>
> framework_version='2.5.0',
>
> py_version='py311',
>
> hyperparameters={
>
> 'epochs': 50,
>
> 'batch_size': 32,
>
> 'learning_rate': 0.001,
>
> },
>
> )
>
> Evaluation metrics
>
> The model is evaluated using metrics that directly map to business value:
>
> Metric
>
> What It Measures
>
> Business Relevance
>
> Top-1 Accuracy
>
> Exact prediction accuracy
>
> “Did the model predict the exact right product?”
>
> Top-3 Accuracy
>
> Correct product in top 3
>
> “Is the right product in the short list for the relationship manager?”
>
> Top-5 Accuracy
>
> Correct product in top 5
>
> “Is it in the recommendation carousel?”
>
> MRR (Mean Reciprocal Rank)
>
> Average reciprocal rank of correct product
>
> “How high up is the correct product on average?”
>
> Weighted F1
>
> Per-class precision/recall balance
>
> “Does the model predict all product types well?”
>
> The production model achieved strong performance across all metrics, with the correct product consistently appearing in the top-3 recommendations. The feature importance module confirmed that the sequence tower (product adoption history) contributes the most signal, followed by transaction patterns, customer demographics, and behavioral segmentation.
>
> Inference and deployment
>
> The inference pipeline supports both batch scoring and real-time predictions using SageMaker AI.
>
> For batch scoring, SageMaker AI Batch Transform processes the entire customer base nightly, generating top-k recommendations with explainability scores for each customer. Results are stored as JSON on Amazon S3 for consumption by CRM systems and relationship manager dashboards.
>
> For real-time predictions, a SageMaker AI real-time endpoint serves on-demand recommendations when a customer logs into the mobile banking app or a relationship manager opens a customer profile.
>
> Each recommendation includes:
>
> Product ID and probability score.
>
> Feature importance breakdown: percentage contribution from each tower.
>
> Confidence indicator: based on probability distribution entropy.
>
> def generate_batch_recommendations(model, dataloader, top_k=5):
>
> with torch.no_grad():
>
> for batch in dataloader:
>
> outputs, feature_importance = model(
>
> batch['sequence'], batch['seq_length'],
>
> batch['active_count'], batch['transaction'],
>
> batch['customer'], batch['behavioral']
>
> )
>
> probabilities = F.softmax(outputs, dim=1).cpu().numpy()
>
> # Generate top-k recommendations with explainability scores
>
> For guidance on securing endpoints with IAM authentication, rate limiting, and virtual private cloud (VPC) isolation, see the Security considerations section.
>
> Note: The code snippets in this post illustrate architectural patterns and are not production-ready. For production, add input validation (tensor shapes, NaN checks, sequence length bounds etc.), error handling, and inference logging. Configure Amazon SageMaker Model Monitor to alert on input distribution drift.
>
> Key design decisions
>
> Why multi-tower over a single network? A single network would need to simultaneously learn how to process sequences, aggregate transactions, encode demographics, and interpret behavioral segments. Separate towers let each specialize in its data type, then the attention-based fusion learns how to combine them optimally per customer.
>
> Why GRU for production over Transformers? Transformers excel on long sequences (100+). For sequences of 20 items or fewer, GRU is sufficient, provides clearer interpretability than transformer attention maps, avoids quadratic attention computation, and produces a smaller model (~5 MB compared to ~15 MB).
>
> Why learned tower weights instead of concatenation? With concatenation, the model treats all towers equally for every customer. With learned attention weights, the model adapts per customer: a customer with rich transaction history gets high transaction tower weight, while a new customer gets high demographic tower weight.
>
> Why time-windowed transaction features? Different time windows capture different signals: 7 days captures immediate intent, 30 days captures monthly patterns, 180 days captures seasonal patterns, and 365 days captures annual patterns. A customer who suddenly increases transaction frequency in the last 7 days has different intent than one with steady activity over 365 days.
>
> Operational considerations
>
> All random seeds are fixed across PyTorch, NumPy, and CUDA for deterministic training. Model artifacts, hyperparameters, and data versions are tracked through Amazon SageMaker Experiments.
>
> Amazon SageMaker Model Monitor detects data drift (changes in input feature distributions), model drift (degradation in prediction quality), and potential bias (over-reliance on demographic features).
>
> The Amazon SageMaker Pipelines workflow retrains the model monthly with the latest customer data. The pipeline automates the full workflow: data processing, training, evaluation, and conditional deployment (deploying only if metrics improve over the current production model).
>
> Security considerations
>
> When deploying this solution with real banking data, implement least-privilege IAM roles scoped to only the required SageMaker AI, Amazon S3, AWS Glue, and CloudWatch actions.
>
> Encrypt data at rest using AWS Key Management Service (AWS KMS) customer managed keys on S3 buckets and SageMaker AI training volumes, and enforce TLS for all data in transit via S3 bucket policies.
>
> Deploy training jobs and endpoints in private VPC subnets with no internet gateway, use VPC endpoints (AWS PrivateLink) for AWS service communication, and set enable_network_isolation=True on training jobs.
>
> Secure inference endpoints with AWS Signature Version 4 signing, and consider Amazon Cognito and Amazon API Gateway for consumer authentication and rate limiting.
>
> For data governance, assess regulatory obligations (PCI-DSS, GDPR, CCPA), implement data minimization, and define retention policies.
>
> Enable AWS CloudTrail for API audit logging and S3 versioning for model artifact integrity.
>
> For complete implementation guidance, see the SageMaker AI security documentation.
>
> Clean up
>
> To avoid ongoing AWS charges, delete the following resources after you finish evaluating this solution.
>
> SageMaker AI endpoints and endpoint configurations.
>
> SageMaker AI models and training job output in Amazon S3.
>
> Amazon SageMaker Processing job output in Amazon S3.
>
> SageMaker AI Batch Transform jobs and configurations.
>
> Amazon SageMaker Pipelines definitions.
>
> Amazon SageMaker Model Monitor schedules.
>
> Amazon SageMaker Experiments trials and experiment data.
>
> Amazon S3 buckets containing training data, model artifacts, and batch transform results.
>
> AWS Glue ETL jobs and Data Catalog resources.
>
> CloudWatch log groups created by SageMaker AI and AWS Glue.
>
> You can delete these resources through the AWS Management Console or using the AWS Command Line Interface (AWS CLI).
>
> Warning: Deleting these resources is irreversible. Before proceeding:
>
> Export any model artifacts or evaluation results you need to retain.
>
> Verify that deletion aligns with your data retention policies and regulatory requirements.
>
> Delete all S3 object versions if versioning is enabled.
>
> Remove IAM roles and policies created for this solution.
>
> Deleting S3 buckets permanently removes all training data, model artifacts, and batch transform results.
>
> Conclusion
>
> This post showed how to build a Next-Best-Product recommendation system for banking using PyTorch and SageMaker AI. The multi-tower architecture with learned attention fusion achieves high prediction accuracy while providing the explainability required by banking regulators.
>
> The key takeaways are:
>
> Specialized towers for different data types outperform monolithic architectures for heterogeneous banking data.
>
> GRU-based sequence processing captures temporal product adoption patterns that flat feature aggregation misses.
>
> Learned tower attention provides both accuracy gains and per-customer explainability without post-hoc interpretation methods.
>
> SageMaker AI provides the end-to-end infrastructure for training, model management, and inference at scale.
>
> You can adapt this multi-tower architecture to your own product catalog and customer data. To get started, explore the SageMaker AI documentation. For additional examples of PyTorch on AWS, see PyTorch on AWS. If you would like help building a recommendation system for your organization, contact an AWS representative.
>
> About the authors
>
> Ayush Singh Chauhan
>
> Ayush is an Associate AI/ML Delivery Consultant with 4+ years of experience solving customer business problems across AI/ML, Agentic AI, and Generative AI domains.
>
> Nisha Gambhir
>
> Nisha is a Senior AI/ML &amp; Cloud Architect based out of India. She is passionate about helping customers design, architect and

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。