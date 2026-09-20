---
title: "Enhancing industrial safety AI with synthetic data on Amazon SageMaker AI"
date: 2026-09-20T19:28:27+08:00
draft: false
entry_kind: "auto"
tags: ["生成式 AI", "机器学习", "Prompt 工程", "Advanced (300)", "Amazon SageMaker AI", "Technical How-to", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:58312df46bc86cae719a5135beeb0dfa1c064fd9b253bd06489f2b6c9808ca7f"
source_payload_sha256: "sha256:6f11ebc347d82fc25f87dfc7da4426b162d85a8a9539679cf2bb32211878e770"
observation_id: obs_01e55e86316d216e5b1b25a250acfd96677ac81c1d17b8345122bdab7c2cd218
event_id: evt_ff74653f9fa55165add617fd4e67bbde24a9ad5f899bf271ce7794347430c040
revision_id: rev_8fb6180085e01c399819a7b42d947ffe11c4c02ba4b4555b92ea2ded1619ac5e
source_published_at: 2026-09-17T15:28:08Z
first_seen_at: 2026-09-20T11:26:30.285088Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: true
source_truncation_reason: "crawler_feed_content_limit"
source_support: 1.0
source_title_chars_original: 73
interpretation_sha256: "sha256:9338b6fe167ca6600eb408c0c7db6121e50bf483b7528a94edcf05597920fb9f"
description: "该内容介绍一种基于Amazon SageMaker AI和Amazon Rekognition的合成数据增强方案，可在保留背景的图像中自动插入人物并生成标注，用于训练工业安全场景的人员检测模型。"
external_url: https://aws.amazon.com/blogs/machine-learning/enhancing-industrial-safety-ai-with-synthetic-data-on-amazon-sagemaker-ai
parent_observation_id: null
last_seen_at: 2026-09-20T11:26:30.285088Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/enhancing-industrial-safety-ai-with-synthetic-data-on-amazon-sagemaker-ai](https://aws.amazon.com/blogs/machine-learning/enhancing-industrial-safety-ai-with-synthetic-data-on-amazon-sagemaker-ai)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么
该内容介绍一种基于Amazon SageMaker AI和Amazon Rekognition的合成数据增强方案，可在保留背景的图像中自动插入人物并生成标注，用于训练工业安全场景的人员检测模型。

### 用在哪里
适用于农业、建筑、采矿和制造等行业中，基于重型机械的安全监测系统开发；尤其是需要在边缘设备上实现实时、低误报的人员检测。

### 可以推断的
- 推测：该方法能够在不进行危险拍摄的情况下获取高风险场景的训练样本，从而提升模型在真实事故中的表现。  
- 推测：通过高置信阈值和去重处理，生成的伪标签足以用于训练轻量化检测模型，满足边缘部署的算力限制。

## 来源摘要/节选

> Industrial safety AI refers to the use of technologies like computer vision and predictive analytics to find and stop workplace dangers. Synthetic data augmentation is emerging as a practical solution to one of the hardest problems in industrial safety AI: the scarcity of training images depicting people in dangerous proximity to heavy machinery. Industries deploying autonomous equipment (for example, agriculture, construction, mining, and manufacturing) need reliable person-detection models. However, the highest-risk scenarios (for example, a worker standing in a blind spot, a child near a moving implement) are precisely the ones that are rarest in real-world datasets. They are also the most dangerous to stage for data collection.
>
> In this post, we show how to use a synthetic data augmentation pipeline built on Amazon SageMaker AI and Amazon Rekognition to generate photo-realistic training images with automated labels. Our experiments showed up to 160 percent improvement in person detection mAP50 (mean Average Precision at an Intersection over Union threshold of 0.5) without manual annotation or hazardous photography sessions.
>
> The challenge: Training data scarcity for safety-critical edge cases
>
> Industrial companies developing AI-powered safety systems for heavy machinery face a critical bottleneck. They need thousands to millions of training images showing people in dangerous positions near equipment to train object detection models that can help prevent accidents. However, this data is extremely difficult to obtain:
>
> Safety and ethics: Deliberately placing people, including vulnerable populations such as children, near active machinery for photography is unsafe, unethical, and often impractical.
>
> Rarity of real events: The hazardous scenarios that matter most (a person standing on tracks, climbing on equipment, or in the path of a vehicle) are the rarest in naturally collected datasets. This creates severe class imbalance.
>
> Cost and scale: Manual data collection and annotation can cost an estimated $3–$5 per image and scales poorly, with annotation teams typically processing on the order of 2,000 images per day.
>
> Edge deployment constraints: Detection models must run on edge devices co-located with equipment (cameras mounted on tractors, forklifts, or railcars), constraining model size to lightweight architectures where every training example matters disproportionately.
>
> These challenges leave edge-deployed models with insufficient training signal for person detection in the exact scenarios where detection failures have the most severe consequences.
>
> Solution architecture
>
> This section describes our end-to-end synthetic data augmentation pipeline, which operates in two stages: photo-realistic image generation and automated labeling.
>
> Overview of the two-stage synthetic data generation framework
>
> Our solution is an end-to-end synthetic data augmentation pipeline that generates labeled training images without manual annotation. The pipeline operates in two stages:
>
> Photo-realistic synthetic image generation – A diffusion-based model (Qwen-Image-Edit-2509) hosted on Amazon SageMaker AI inserts synthetic people into real scene images while preserving background, lighting, and scale.
>
> Automated labeling – The Amazon Rekognition DetectLabels API automatically generates bounding-box annotations for the inserted people, alleviating manual annotation.
>
> In our approach, we edit real images rather than generating entirely synthetic scenes from scratch. This preserves background fidelity, avoids domain gap, and allows existing equipment annotations to remain valid. Domain gap is the performance drop that occurs when a model trained on one data distribution, such as fully synthetic scenes, is applied to real-world images. The diffusion model’s scene understanding produces contextually coherent insertions with realistic lighting and proportions.
>
> Stage 1: Photo-realistic synthetic image generation
>
> We deploy the Qwen-Image-Edit-2509 diffusion model on Amazon SageMaker AI using an ml.g5.12xlarge instance (4× NVIDIA A10G GPUs, 96 GB total VRAM). The model receives a structured prompt specifying:
>
> Object to insert: A person with randomized gender for demographic diversity.
>
> Placement strategy: Hazardous positioning relative to equipment (for example, on tracks, on top of equipment, hanging from edges, or standing in a vehicle’s path).
>
> Constraints: No distortion of existing elements, sharp focus, and realistic integration with the scene.
>
> The model edits real images containing equipment but no people as substrates, inserting synthetic people while preserving the original scene context, lighting, and scale. This in-place editing approach avoids the domain gap issues that plague fully synthetic scene generation.
>
> Stage 2: Automated labeling with Amazon Rekognition
>
> Each generated image is processed through the Amazon Rekognition DetectLabels API with a minimum confidence threshold of 80 percent. Detected bounding boxes are deduplicated by using non-maximum suppression (NMS) with IoU threshold &gt; 0.5 and converted to YOLO format. These pseudo-labels (machine-generated annotations produced automatically in place of human labeling) are merged with existing equipment annotations from the original image.
>
> This automated labeling alleviates manual annotation for synthetic images while maintaining label quality sufficient for training edge-deployed detectors. The synthetic images and their automated annotations are combined with real training data to form the final training set. Pre- and post-processing steps (image filtering, image resizing, prompt assembly, and label processing) allow the pipeline to run as an automated workflow.
>
> Implementation details
>
> This section covers the model deployment configuration, the synthetic image generation methodology, and the automated annotation pipeline.
>
> Technical setup and configuration
>
> The Qwen-Image-Edit-2509 model is deployed on Amazon SageMaker AI with the following configuration:
>
> Instance type: ml.g5.12xlarge (4× NVIDIA A10G GPUs, 96 GB total VRAM).
>
> Model size: approximately 60 GB unquantized weights distributed across 4 GPUs.
>
> Inference steps: 25.
>
> CFG scale: 4.0.
>
> Minimum image dimension: 512 px.
>
> Generation time: ~166 seconds per image.
>
> The model requires a custom device map that distributes its 60 transformer layers across the available GPUS. For efficient inference, we recommend avoiding cross device communication. Deploy on a single gpu with sufficient VRAM, such as the NVIDIA H100 GPU provided by ml.p5.4xlarge instances, or employ weight quantization techniques. We project that inference cost per image will drop around 10x using such hardware, but this measurement is not yet validated.
>
> Synthetic human insertion methodology
>
> The pipeline selects real training images that contain locomotives but no people as editing substrates. For each image, the diffusion model receives a structured prompt. Here is an example prompt structure:
>
> PROMPT_TEMPLATE = """ Add one realistic person (gender: {gender}) to this image. Position the person in a hazardous place or position such as on the tracks, standing on top of the train, hanging on to the edge, etc.
>
> Verify the person is:
>
> - Accurately scaled and proportioned relative to other objects. Train cars are between 15-20 feet tall. A person should never be larger than a train car.
>
> - Naturally integrated into the scene's depth, perspective, and lighting.
>
> - Clearly visible and not blurred
>
> Lighting and atmosphere instructions:
>
> - Simulate lighting appropriate for {time_of_day} time, with consistent shadows and highlights.
>
> - Reflect the ambient condition of {ambient_condition} in the scene's atmosphere, visibility, and color tones.
>
> - Avoid artificial shine or polished textures. Machinery and surfaces should appear natural, with realistic textures (e.g., dust, dirt, faded paint).
>
> - Colors should be realistic and muted, not overly saturated.
>
> - Avoid glossy or polished finishes.
>
> Do not modify or distort any existing elements in the input image. The person must not appear larger or smaller than expected based on the scene's scale. Do not change any numbers, text, logos, or symbols on machinery or objects from the input image.
>
> Visual quality requirements:
>
> - Maintain sharp focus across the entire depth of the image, avoiding shallow depth-of-field effects.
>
> - Avoid: garbled face, floating or incomplete body parts, over-saturation, low resolution, grainy textures, pixelation, under/overexposure, poor color balance, washed-out tones, artifacts, color banding, outdated effects, unrealistic elements, poor compositing, visual noise, flickering, or background blur.
>
> - Verify: high realism, consistent geometry, natural integration of all elements, uniform sharpness across foreground and background, high-definition rendering with crisp details. """
>
> Our experiments revealed a critical finding: prompt-guided placement is the single most important factor for downstream detection performance. Instructing the model to place people in domain-relevant hazardous positions doubled person detection mAP50, while placing people in the background actually degraded performance.
>
> Amazon Rekognition integration for automated annotation
>
> Each generated image is processed through the Amazon Rekognition DetectLabels API. The model computes bounding boxes for humans using the query words: person, human, man, woman, boy, girl, child, adult, people. This automates label creation at scale. We use:
>
> Minimum confidence threshold: 80 percent.
>
> Post-processing: Non-maximum suppression (NMS) with IoU threshold &gt; 0.5.
>
> Label format: Bounding boxes converted to YOLO format and merged with existing equipment annotations.
>
> Dataset composition
>
> We used an OpenImages subset as a publicly shareable analog to our customer’s industrial equipment dataset:
>
> Real training images: approximately 3,200 images from OpenImages containing trains (as a proxy for heavy machinery).
>
> Synthetic augmentation: Up to 1,000 additional images with synthetically inserted people.
>
> Test set: Real OpenImages images only (no synthetic data), filtered to contain at least one locomotive.
>
> Task: 2-class detection (person and train) with severe class imbalance.
>
> Results and performance improvements
>
> We evaluated the impact of synthetic data augmentation across three dimensions: prompt placement strategy, synthetic data volume, and model capacity.
>
> Evaluation methodology
>
> We evaluated our pipeline using YOLO11 as a representative edge-deployable detector family, trained on Amazon SageMaker AI with PyTorch 2.1.0. Models were trained with image size 640, early stopping (patience 50), and a maximum of 500 epochs.
>
> Key finding 1: Domain-relevant placement doubles detection performance
>
> Our prompt ablation study with YOLO11-nano compared four synthetic data conditions against a real-data-only baseline. We used 1,000 synthetic images in each scenario. The following table shows key performance metrics for each scenario.
>
> Condition
>
> Person mAP50
>
> Person Recall
>
> Person Precision
>
> Agg mAP50 (Person and Train)
>
> Baseline (real only)
>
> 0.051
>
> 0.170
>
> 0.338
>
> 0.517
>
> Hazardous placement
>
> 0.106
>
> 0.234
>
> 0.409
>
> 0.558
>
> Hazardous + scene variation
>
> 0.088
>
> 0.128
>
> 0.492
>
> 0.547
>
> Background placement
>
> 0.046
>
> 0.219
>
> 0.217
>
> 0.527
>
> Background + scene variation
>
> 0.051
>
> 0.085
>
> 0.421
>
> 0.532
>
> Takeaway: What the model generates (a person in a domain-relevant position) matters far more than how the scene is varied around it (for example, ambient condition or time of day). Hazardous placement doubled person mAP50 (from 0.051 to 0.106), while background placement slightly degraded it.
>
> Key finding 2: Optimal synthetic volume is a hyperparameter
>
> To explore the impact of synthetic data volume on detection performance, we swept the number of synthetic images from 250-1,000 while keeping the person placement condition and model size constant (hazardous placement with no scene variation, YOLO11-nano). The following table shows key performance metrics for each scenario:
>
> Synthetic Images
>
> Person mAP50
>
> Person Recall
>
> Agg mAP50 (Person and Train)
>
> 0 (baseline)
>
> 0.051
>
> 0.170
>
> 0.517
>
> 250
>
> 0.069
>
> 0.170
>
> 0.540
>
> 500
>
> 0.092
>
> 0.213
>
> 0.556
>
> 750 (best)
>
> 0.134
>
> 0.213
>
> 0.597
>
> 1,000
>
> 0.106
>
> 0.234
>
> 0.558
>
> Takeaway: In our experiments, performance peaked at 750 synthetic images with 160 percent improvement in person mAP50 over baseline (from 0.051 to 0.134). Beyond this point, accumulated generation artifacts (for example, garbled faces and over-saturation) introduced noise that degraded both localization confidence and detection coverage. Treat synthetic data volume as a hyperparameter to validate, not maximize.
>
> Key finding 3: Match model capacity to dataset size
>
> To explore the impact of model capacity, we swept YOLO11 across five model scales with 1,000 synthetic images (hazardous placement with no scene variation):
>
> Model
>
> Parameters
>
> Person mAP50
>
> Person Recall
>
> Agg mAP50 (Person and Train)
>
> Nano (baseline)
>
> 2.6M
>
> 0.051
>
> 0.170
>
> 0.517
>
> Nano + synth
>
> 2.6M
>
> 0.106
>
> 0.234
>
> 0.558
>
> Small + synth
>
> 9.4M
>
> 0.135
>
> 0.170
>
> 0.591
>
> Medium + synth
>
> 20.1M
>
> 0.135
>
> 0.340
>
> 0.604
>
> Large + synth
>
> 25.3M
>
> 0.142
>
> 0.244
>
> 0.584
>
> XLarge + synth
>
> 56.9M
>
> 0.093
>
> 0.149
>
> 0.551
>
> Takeaway: YOLO11-medium achieved the best aggregate performance (0.604 mAP50) and the highest person recall (0.340), doubling recall compared to the baseline. The 57M-parameter XLarge model regressed below the Nano+synth result, demonstrating that with only approximately 4,200 training images, there is insufficient data to regularize a model of that capacity.
>
> Significance for safety-critical applications
>
> The combined pipeline improvements are particularly significant for safety:
>
> Person recall doubled from 17 percent to 34 percent with medium-capacity model, meaning the system detected twice as many people in hazardous positions.
>
> Aggregate detection maintained: Train mAP50 remained stable (0.73–0.79 range) across all conditions.
>
> Edge-deployable: All improvements achieved with a 20M-parameter model suitable for real-time inference on edge hardware.
>
> Cost and efficiency benefits
>
> The synthetic data pipeline delivers significant cost, safety, and speed advantages over manual data collection. In the following sections, we compare the two approaches, outline scalability benefits, and summarize time-to-deployment improvements.
>
> Synthetic generation compared to manual collection and annotation
>
> Beyond per-image cost savings, the pipeline provides structural advantages that compound as teams scale their training data efforts. The following table compares the synthetic data augmentation pipeline with the manual approach across five different dimensions.
>
> Factor
>
> Manual Approach
>
> Synthetic Pipeline
>
> Per-image cost
>
> $3–$5 (collection + annotation)
>
> $0.33 assuming ~166s GPU inference ($7.09/hour for ml.g5.12xlarge instance) + Amazon Rekognition DetectLabels API call ($0.001/image)
>
> Safety risk
>
> Requires staging dangerous scenarios
>
> Alleviated physical risk
>
> Annotation labor
>
> Manual bounding box drawing
>
> Fully automated through Amazon Rekognition
>
> Rare scenarios
>
> Years of natural occurrence
>
> Unlimited generation on demand
>
> Scalability
>
> ~2,000 images/day with teams
>
> Bounded only by compute budget
>
> Scalability advantages
>
> Unlimited scenario generation: Produce training images for a wide range of hazardous position configurations that can be described in a text prompt.
>
> Modular prompt structure: You can replace placement instructions for your specific domain (construction, agriculture, warehousing) while reusing the generation and pseudo-labeling infrastructure.
>
> Cloud-native architecture: Built entirely on managed AWS services, requiring no custom infrastructure.
>
> Time-to-deployment improvements
>
> By alleviating manual data collection and annotation, the pipeline shortens the path from identifying a training data gap to having labeled images ready for model training. This reduces the timeline from weeks or months to hours. The infrastructure is reusable: After set up, generating additional training data for new scenarios requires only new prompt templates.
>
> Getting started
>
> The code for this solution is available in our GitHub repository. To deploy the solution in your own environment, follow the instructions in the following sections.
>
> Repository structure
>
> The GitHub repository contains the following directories and files:
>
> ├── data_prep/ # Data preparation scripts
>
> │ ├── download_openimages.py # Download images from public OpenImages Amazon S3 mirror
>
> │ └── create_yolo_dataset.py # Convert to YOLO format
>
> ├── qwen_image_edit/ # Synthetic data generation
>
> │ ├── config.py # SDA_S3_BUCKET config
>
> │ ├── prompts.py # Prompt templates
>
> │ ├── recognition.py # Amazon Rekognition pseudo-labeling
>
> │ ├── s3_io.py # Amazon S3 image I/O, resizing, resume cache
>
> │ ├── model.py # Qwen pipeline loading (single- or multi-GPU) + inference
>
> │ ├── generate_synthetic.py # Batch generation CLI
>
> │ ├── launch_generation.py # Launch generation as an Amazon SageMaker AI job
>
> │ ├── requirements.txt # Generation job dependencies (installed by the DLC)
>
> │ └── generate.ipynb # Demo notebook (single GPU or multi-GPU via a flag)
>
> ├── yolo_training/ # Model training
>
> │ ├── train.py # Amazon SageMaker AI training script (supports --seed)
>
> │ ├── launch_training.py # Launch Amazon SageMaker AI training jobs
>
> │ └── requirements.txt # Training dependencies
>
> ├── evaluation/ # Evaluation &amp; analysis
>
> │ ├── extract_per_class.py # Per-class mAP breakdown (person vs train)
>
> │ ├── run_eval.py # Run YOLO validation with plots
>
> │ ├── compare_results.py # Side-by-side visual comparison (2- or 3-way)
>
> │ ├── find_missed_detections.py # Find/annotate missed detections
>
> │ ├── download_testdata.py # Download test set from Amazon S3
>
> │ └── README.md # Evaluation workflow docs
>
> ├── scripts/ # Instance / repo setup
>
> │ ├── setup_instance.py # Bootstrap an Amazon SageMaker AI notebook instance
>
> │ ├── upload_repo.sh # Sync the repo to Amazon S3 for notebook instances
>
> │ └── pyproject.toml # Notebook-instance generation dependencies
>
> ├── .gitignore # Ignores datasets/, caches, model weights, etc.
>
> ├── .python-version # Pins Python to 3.11 (for pyenv/uv)
>
> ├── CODE_OF_CONDUCT.md # Community code of conduct
>
> ├── CONTRIBUTING.md # Contribution guidelines
>
> ├── LICENSE # MIT-0 license
>
> ├── README.md # Project overview, setup, and full usage walkthrough
>
> ├── pyproject.toml # Root project dependencies (uv-managed)
>
> └── uv.lock # Locked dependency versions for the root pyproject.toml
>
> Prerequisites
>
> Before you start, you will need:
>
> Python 3.11 (&gt;=3.11,&lt;3.12) and uv. We have tested with this Python version, but others might work.
>
> An AWS account with credentials configured (aws configure, environment variables, or an AWS Identity and Access Management (IAM) role).
>
> A GPU with 40 GB+ VRAM for the image-editing step (single H100/B200), or a multi-GPU instance such as ml.g5.12xlarge (4× A10G) for the sharded path. The pipeline is set up to run on Amazon SageMaker AI.
>
> Amazon SageMaker AI GPU service quota. New accounts have a quota of 0 for GPU training instances (for example, ml.g5.12xlarge). Request an increase in the AWS Service Quotas console before launching jobs. Otherwise, jobs will fail or sit pending.
>
> Amazon Rekognition access (rekognition:DetectLabels): A billable AWS service used to auto-label the synthetic people.
>
> Hugging Face access to download the Qwen/Qwen-Image-Edit-2509 model weights (downloaded automatically on first run).
>
> Usage
>
> Follow instructions for steps 1–6 of the Usage section in README.md:
>
> From the README’s Usage section:
>
> Download OpenImages Data: Create an Amazon Simple Storage Service (Amazon S3) bucket, then run data_prep/download_openimages.py to copy Train-class images (train/validation/test splits) from the public OpenImages Amazon S3 mirror into your bucket. Images only, no labels yet.
>
> Stage Annotation CSVs: Copy the four OpenImages annotation CSVs (cached locally by step 1) up to s3://&lt;amzn-s3-demo-bucket&gt;/datasets/openimages/annotations/, because steps 3 and 4 read them from there.
>
> Create YOLO Dataset: Run data_prep/create_yolo_dataset.py to reorganize the downloaded images into YOLO’s images/ and labels/ directory structure and generate data.yaml / data-with-synthetic.yaml, using the staged CSVs to build labels.
>
> Generate Synthetic Data: Use qwen_image_edit/generate_synthetic.py (interactively through generate.ipynb, as a batch script, or launched as an Amazon SageMaker AI job by using launch_generation.py) to add synthetic people to train images with Qwen-Image-Edit-2509 and pseudo-label them with Amazon Rekognition. Produces a complete augmented dataset under --dataset-prefix with its own data.yaml.
>
> Train YOLO Model: Run yolo_training/launch_training.py twice: once on the step-3 baseline prefix (original images only) and once on the step-4 output prefix (original + synthetic), to produce a baseline and a synthetic-augmented model.
>
> Evaluate: Use the scripts in evaluation/ (download_testdata.py, run_eval.py, extract_per_class.py, compare_results.py) to validate both trained models on the held-out test set and compare whether synthetic augmentation improved detection.
>
> The pipeline is designed to be domain-agnostic. Whether your use case involves construction sites, agricultural equipment, manufacturing floors, or warehouse operations, the same architecture applies with domain-specific prompt templates.
>
> Clean up
>
> After you’re done experimenting, remove the following resources to avoid ongoing charges. Amazon SageMaker AI training and processing jobs and Amazon Rekognition API calls are billed only while they run, and they stop accruing cost automatically. However, a few resources persist until you delete them:
>
> Stop or delete any running Amazon SageMaker AI notebook instance (step 4’s interactive generate.ipynb path).
>
> Delete the Amazon S3 bucket contents (and the bucket) if no longer needed. All datasets, annotation CSVs, synthetic images/labels, and training outputs live under the bucket you created in step 1.
>
> Remove the Amazon SageMaker AI execution role (optional). IAM roles have no cost on their own, so this step is about hygiene/security rather than billing.
>
> Conclusion
>
> We presented a practical, end-to-end pipeline for synthetic data augmentation that addresses the critical training data scarcity challenge in industrial safety AI. The pipeline combines diffusion-based image editing on Amazon SageMaker AI with automated pseudo-labeling through Amazon Rekognition to generate photo-realistic, labeled training images without manual annotation or hazardous staging.
>
> Our controlled experiments yielded three actionable guidelines:
>
> Prompt for domain-relevant placement: Spatial positioning of synthetic objects relative to equipment is the dominant factor for detection improvement. Visual diversity (weather, lighting) is secondary.
>
> Validate synthetic volume: More synthetic data isn’t always better. Detection performance peaks at an optimal synthetic-data volume. Beyond that point, accumulated generation artifacts introduce noise that degrades the model.
>
> Match model capacity to data budget: With limited total training data, mid-sized edge models outperform both smaller and larger alternatives.
>
> The result: a 160 percent improvement in person detection mAP50 and doubled recall for an edge-deployable model, achieved without manual annotation labor or dangerous data collection sessions.
>
> To get started with this solution, visit our GitHub repository. To learn more about the services used in this post, see the following resources:
>
> Amazon SageMaker AI
>
> Amazon SageMaker AI documentation
>
> Amazon Rekognition
>
> Amazon Rekognition documentation
>
> About the authors
>
> Dimitri Voytan
>
> Dimitri is an Applied Scientist with AWS Professional Services. He is interested in applying machine learning and generative AI to solve challenging business problems. Before joining Amazon, he has worked in applying advanced machine learning techniques to geophysical problems.
>
> Hasan Shojaei
>
> Hasan is a Principal Data Scientist with AWS Professional Services, where he helps customers across different industries such as sports, energy, financial services, and manufacturing solve their business

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。