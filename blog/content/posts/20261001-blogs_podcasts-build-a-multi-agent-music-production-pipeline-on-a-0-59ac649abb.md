---
title: "Build a multi-agent music production pipeline on Amazon Bedrock AgentCore Runtime Instances"
date: 2026-10-01T13:53:37+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "机器学习", "Prompt 工程", "Advanced (300)", "Amazon Bedrock AgentCore", "Technical How-to", "博客与播客"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:00da107fc17a3e35ddc75d4b257bacd4bef8e9df42cbbbc5a58f627e68d28741"
source_payload_sha256: "sha256:ab38c92785cd4be588eb0739036f20db4773a8bbc5d9f4c67ad6fd063d13a7da"
observation_id: obs_59ac649abb99214213a2829dcf3cdcac0e1cacd07ea717051b9fe129a1f607d8
event_id: evt_c7b2b6cbe3c8d324cac9be532af54fc0f414445c4cbd76535a1abdf52245065a
revision_id: rev_c9d618c6746cdc35c8e4e22b339eed9fedc4bad6df34aa4208f303d6a09ed0cf
source_published_at: 2026-09-30T15:21:57Z
first_seen_at: 2026-10-01T06:03:14Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 91
interpretation_sha256: "sha256:8d9f27fa3a519f20c489b26572cafb8861adf72ea2b758fad41a8887bf3a5048"
description: "这是一篇技术实践文章，演示了如何在AWS Bedrock的Runtime Instances上构建多智能体协作流水线，以音乐制作为例，展示了三个专业智能体如何共享计算资源、持久化存储和GPU来协同完成从音频生成到合规检查的完整工作流程。"
external_url: https://aws.amazon.com/blogs/machine-learning/build-a-multi-agent-music-production-pipeline-on-amazon-bedrock-agentcore-runtime-instances
parent_observation_id: null
last_seen_at: 2026-10-01T05:51:00.804599Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/build-a-multi-agent-music-production-pipeline-on-amazon-bedrock-agentcore-runtime-instances](https://aws.amazon.com/blogs/machine-learning/build-a-multi-agent-music-production-pipeline-on-amazon-bedrock-agentcore-runtime-instances)
- **发布域名**: aws.amazon.com

## 要点解读

### 这是什么

这是一篇技术实践文章，演示了如何在AWS Bedrock的Runtime Instances上构建多智能体协作流水线，以音乐制作为例，展示了三个专业智能体如何共享计算资源、持久化存储和GPU来协同完成从音频生成到合规检查的完整工作流程。

### 用在哪里

适用于需要长时间运行、多智能体共享状态和资源的复杂AI应用场景。对于希望在云端部署持续性AI工作流、尤其是需要GPU加速或多智能体协作的开发团队具有参考价值。

### 可以推断的

推测：多智能体系统的部署模式正从短时、无状态的单智能体查询，向需要持久化上下文和资源共享的协作式工作流演进，这意味着基础设施需要支持更长的会话生命周期和跨智能体的数据交换。

推测：在需要GPU加速的AI应用中，将推理任务固定在特定计算实例上，比频繁冷启动的Serverless模式更具成本和性能优势，尤其当任务涉及模型加载或需要复用中间结果时。

## 来源摘要/节选

> As organizations move from single-purpose agents to multi-agent systems, the infrastructure requirements change. A lone agent handling customer queries can run in a serverless environment with short-lived sessions. But when you need three agents collaborating on a creative workflow that spans several days, sharing context and building on each other’s output, serverless sessions that cap at a few hours don’t cut it.
>
> In this post, we walk through deploying a music production pipeline: One agent runs a generative audio model on the instance’s own GPU. The other two open the .wav file it wrote, off a shared volume. By the end, you will have a track you can play. You will also have learned how to create capacity providers, deploy agents from different artifact types, orchestrate agent-to-agent collaboration using shared sessions, and persist workflows across multiple days.
>
> Amazon Bedrock AgentCore offers two compute options for hosting agents. MicroVMs are the serverless option: fast cold starts, session isolation, and consumption-based pricing. Runtime Instances are the new option: AWS managed EC2 infrastructure for persistent, long-running agent workflows. Both use the same runtime APIs, but Instances add multi-day sessions, GPUs, persistent volumes, and the ability to colocate multiple agents on a single instance.
>
> How Runtime Instances differs from MicroVM
>
> Both options support custom frameworks (CrewAI, LangGraph, LlamaIndex, Strands Agents), work with your choice of foundation model, integrate with MCP and A2A, and share the same AgentCore runtime APIs. The difference is in the underlying compute model.
>
> Capability
>
> MicroVM (Serverless)
>
> Runtime Instances
>
> Compute
>
> Fully AWS managed
>
> AWS managed EC2 instances
>
> Session duration
>
> Up to 8 hours
>
> Up to 14 days
>
> Agents per compute
>
> One runtime (microVM) hosts one agent (1:1)
>
> One instance (EC2) can host multiple agents (1:N)
>
> Artifact types
>
> Container image and Amazon S3 source
>
> Container image and Amazon S3 source
>
> GPU access
>
> Not supported
>
> Yes, on a supported instance family
>
> Session persistence
>
> Session-scoped
>
> Persistent storage (Amazon EBS)
>
> Pricing
>
> Consumption-based
>
> EC2 instances run in your account. Use your AWS Savings Plans and On-Demand Capacity Reservations (ODCRs)
>
> Scaling
>
> Scale on demand
>
> Managed by capacity provider
>
> An agent is a workload running within a session. Unlike the MicroVM model, where one runtime hosts one agent, a single Instances session can host multiple agents. When two agent runtimes share the same capacity provider, you can invoke them with the same runtimeSessionId to land both agents on the same EC2 instance. There, they share a filesystem and can collaborate on the same task.
>
> Solution overview
>
> Figure 1: The three-agent pipeline (Compose, Deliver, Screen) sharing one GPU instance and session
>
> We will build a music production system that uses three specialized agents:
>
> Composition agent (Audio AI team): Turns a producer’s request into a musical brief using Claude Sonnet 4.6, then renders the actual audio with a generative music model (ACE-Step, an open-source foundation model (FM) for music generation), running on the instance’s own GPU. Packaged as a container image in Amazon Elastic Container Registry (Amazon ECR).
>
> Delivery agent (Audio Engineering team): Reads the rendered track off the shared filesystem and measures it, then asks Claude Sonnet 4.6 for a delivery chain (EQ, compression, limiting) based on those measurements rather than on the audio itself. Real signal processing applies to the chain, and the result is measured again to confirm it hit the delivery target. Packaged as a container image in Amazon ECR.
>
> Compliance agent (Release Engineering team): Independently re-measures the finished delivery, checks it against the delivery targets the delivery agent claimed, and screens it for harmonic similarity against the studio’s own back catalog. If the screen objects, the agent calls back to the composition agent for a replacement and re-screens. Delivered as a zip file on Amazon Simple Storage Service (Amazon S3).
>
> The workflow: a producer starts a track. The composition agent writes a brief and renders real audio on the instance’s GPU. The delivery agent opens that file, measures it, applies a chain it derived from those measurements, and measures again to prove the result landed on target. The compliance agent then re-measures independently, checks the delivery targets, and screens the audio against the studio’s back catalog. If the screen flags a match, it calls back to the composition agent to generate an alternative. The producer ends up with a playable .wav and three reports explaining every decision.
>
> What makes this possible on Runtime Instances:
>
> Colocation via shared session ID. Each agent has its own runtime, but by invoking them with the same runtimeSessionId on the same capacity provider, AgentCore places them on the same instance with the same volumes mounted. They share a filesystem and can access each other’s outputs.
>
> A GPU you can use. The composition agent runs the ACE-Step foundation model directly on the instance’s NVIDIA L4, rendering 20 seconds of 48 kHz stereo in about 9 seconds. The model and its dependencies live on a persistent volume. Built once for a session, then reused by every invocation in it, including after an overnight stop.
>
> Independent deployment. Each team ships its own artifact on its own cadence. The Audio AI team pushes a new composition image without coordinating with Audio Engineering or Release Engineering, and the other two keep running untouched.
>
> Multi-day persistence. A producer works on composition Monday, stops the session overnight, and resumes delivery Tuesday. The instance idles automatically and resumes the next invoke.
>
> Mixed artifacts. Containers from ECR and code packages from S3 coexist on one capacity provider. Teams choose the packaging that fits their workflow.
>
> Walkthrough
>
> From here on, this post is hands-on. You will prepare your AWS account, then run a three-agent pipeline that renders, generates, and clears a finished track, producing a .wav file you can play. Work through the steps in order. You will start by confirming the prerequisites, then define the three agents (Step 1), create a capacity provider that provisions the GPU instance and its persistent volumes (Step 2), deploy each agent as its own runtime (Step 3), and invoke them with a shared session ID so they can colocate on one instance and hand work to each other (Step 4). Finally, Step 5 shows how any one team can ship a new version of its agent without disturbing the others. The complete sample is in the AgentCore samples GitHub repository.
>
> Prerequisites
>
> Before you begin, make sure you have:
>
> An AWS account, with credentials for a principal that can create infrastructure. This sample creates AWS Identity and Access Management (IAM) roles, an S3 bucket, ECR repositories, and an AgentCore capacity provider and runtimes.
>
> AWS Command Line Interface (AWS CLI) installed and configured.
>
> A virtual private cloud (VPC) with at least one subnet and security group.
>
> Model access enabled in the Amazon Bedrock console for Anthropic Claude Sonnet 4.6.
>
> Finch or another OCI-compatible container tool installed locally.
>
> Python 3.10+ installed.
>
> boto3 ≥ 1.36.0 or botocore ≥ 1.43.72. Older versions lack create_capacity_provider, and deploy.py will fail.
>
> For the complete working code, see the AgentCore samples repository on GitHub.
>
> Step 1: Define your agents
>
> AgentCore Runtime Instances supports any agent framework. In this sample, each agent is a Python application built with Strands Agents.
>
> Two details are commonly misconfigured, and both fail confusingly:
>
> @app.entrypoint
>
> def invoke(payload, context): # the parameter must be NAMED "context"
>
> session_id = getattr(context, "session_id", None) or "local-session"
>
> The SDK dispatches on the parameter name (it checks params[1] == "context"). That is the only way to read the session ID, which the agents need in order to find each other’s files and to call one another.
>
> Second, build the Agent inside the handler, not at module scope:
>
> def build_agent(session_id: str, track_id: str) -&gt; Agent:
>
> return Agent(
>
> name=AGENT_NAME,
>
> model=BedrockModel(model_id=MODEL_ID, region_name=REGION),
>
> system_prompt=SYSTEM_PROMPT,
>
> session_manager=FileSessionManager(
>
> session_id=f"{session_id}-{AGENT_NAME}",
>
> storage_dir=str(track_path(track_id) / f".sessions-{AGENT_NAME}"),
>
> ),
>
> )
>
> A module-level Agent is shared across concurrent requests, and Strands rejects re-entrant invocation with Agent is already processing a request. History lives on the volume through FileSessionManager, which is how a session resumed days later remembers earlier decisions.
>
> Composition agent
>
> The composition agent turns the producer request (prompt) into a musical brief, using Claude Sonnet 4.6, then renders the actual audio with the ACE-Step foundation model:
>
> @app.entrypoint
>
> def invoke(payload, context):
>
> session_id = getattr(context, "session_id", None) or "local-session"
>
> track_id = payload.get("track_id", "demo-track")
>
> if payload.get("mode") == "prepare":
>
> return {"status": "ok", "model_stack": prepare_model_stack()}
>
> ensure_track_dir(track_id)
>
> brief = build_agent(session_id, track_id)(
>
> payload["prompt"], structured_output_model=CompositionBrief
>
> ).structured_output
>
> wav = track_path(track_id) / "composition.wav"
>
> render = render_audio(wav, brief, duration_s=payload.get("duration_s", 30.0))
>
> write_text(track_id, "composition.md", brief.to_markdown(render))
>
> return {"status": "ok", "render": render, "host": host_info(),
>
> "artifacts": [publish(track_id, wav)]}
>
> The mode=prepare call builds the stack onto the volume, a virtualenv with CUDA PyTorch and ACE-Step. The render runs as a subprocess under that volume’s interpreter:
>
> proc = subprocess.run(
>
> [status["python"], status["runner"], "--out", str(out_path),
>
> "--prompt", brief.style_tags, "--duration", str(duration_s)],
>
> capture_output=True, text=True, check=False,
>
> timeout=RENDER_TIMEOUT_S, env=gpu_env(),
>
> )
>
> Delivery agent
>
> The delivery agent reads the rendered track off the shared filesystem and measures it. It uses Claude Sonnet 4.6 to choose EQ bands, compressor settings, and what to leave alone. The digital signal processing (DSP) is then applied. Then the output is measured again, so the plan is checked rather than trusted.
>
> before = audio.measure(str(source)) # ITU-R BS.1770-4
>
> plan = build_agent(session_id, track_id)(
>
> f"Prepare this for {platform} delivery.\n{json.dumps(before.to_dict())}",
>
> structured_output_model=DeliveryPlan,
>
> ).structured_output
>
> data, rate = audio.read_audio(str(source))
>
> bands = [b.model_dump() for b in plan.eq_bands]
>
> if bands:
>
> data = audio.apply_filters(data, rate, bands)
>
> if plan.compressor.enabled:
>
> data, _ = audio.compress(
>
> data, rate,
>
> threshold_db=plan.compressor.threshold_db,
>
> ratio=plan.compressor.ratio,
>
> attack_ms=plan.compressor.attack_ms,
>
> release_ms=plan.compressor.release_ms,
>
> knee_db=plan.compressor.knee_db,
>
> )
>
> data, _ = audio.normalise_loudness(data, rate, plan.target_lufs)
>
> data, _ = audio.limit(data, rate, ceiling_dbtp=plan.target_true_peak_dbtp)
>
> audio.write_audio(str(delivery), data, rate, subtype="PCM_24")
>
> after = audio.measure(str(delivery)) # verify, don't trust
>
> Compliance agent
>
> The compliance agent independently re-measures the finished delivery, checks it against the delivery targets the delivery agent claimed, and screens it for harmonic similarity against the studio’s own back catalog. When it finds a similarity, it raises a flag and calls back to the composition agent for remediation.
>
> client = boto3.client(
>
> "bedrock-agentcore", region_name=REGION,
>
> config=Config(read_timeout=600, retries={"max_attempts": 3, "mode": "standard"}),
>
> )
>
> response = client.invoke_agent_runtime(
>
> agentRuntimeArn=COMPOSITION_RUNTIME_ARN, # injected at deploy time, not hard-coded
>
> qualifier=COMPOSITION_QUALIFIER,
>
> runtimeSessionId=session_id, # the caller's own --- routes to this instance
>
> payload=json.dumps({
>
> "mode": "remediate", "track_id": track_id,
>
> "issue": issue,
>
> "avoid": avoid or {},
>
> }).encode(),
>
> )
>
> body = json.loads(response["response"].read()) # "response", not "body"
>
> Step 2: Create a capacity provider
>
> A capacity provider tells AgentCore what compute infrastructure to provision for your agents. You specify instance types and VPC placement. AgentCore handles provisioning and lifecycle management.
>
> You need two IAM roles, and the distinction matters:
>
> An operator role AgentCore assumes to provision EC2 on your behalf: launching, tagging, and terminating instances and their network interfaces. Attach the managed policy BedrockAgentCoreRuntimeInstancesOperatorRolePolicy.
>
> An execution role your agent process assumes at runtime to call Bedrock and S3. CreateAgentRuntime requires it and fails without it.
>
> Both trust bedrock-agentcore.amazonaws.com.
>
> Now create the capacity provider. Note that names must use underscores (hyphens are not allowed):
>
> control = boto3.client("bedrock-agentcore-control", region_name=REGION)
>
> resp = control.create_capacity_provider(
>
> name="music_production_capacity",
>
> permissionsConfiguration={"capacityProviderOperatorRoleArn": operator_arn},
>
> computeConfiguration={
>
> "ec2Configuration": {
>
> "launchTemplateSource": {
>
> "launchParameters": {
>
> "operatingSystem": "LINUX_X86_64", "instanceRequirements": {"allowedInstanceTypes": ["g6.xlarge"]},
>
> }
>
> },
>
> "vpcConfiguration": {"subnets": subnets, "securityGroups": groups},
>
> "volumes": [
>
> {"ebsConfiguration": {"name": "tracks", "sizeGiB": 20,
>
> "volumeType": "gp3", "encrypted": True&#125;&#125;,
>
> {"ebsConfiguration": {"name": "models", "sizeGiB": 60,
>
> "volumeType": "gp3", "encrypted": True,
>
> "throughput": 500&#125;&#125;,
>
> ],
>
> "rootVolume": {"freeSpaceGiB": 30, "volumeType": "gp3"},
>
> "lifecycleConfiguration": {"idleInstanceTimeout": 600,
>
> "maxLifetime": 86400},
>
> }
>
> },
>
> )
>
> GPU capacity. If you hit InsufficientInstanceCapacity across multiple Availability Zones (AZs) trying to allocate a GPU instance, you can switch to another GPU instance type, like g5.xlarge. Update allowedInstanceTypes accordingly.
>
> Step 3: Deploy agent runtimes
>
> Each agent here gets its own runtime. The runtimes are brought together at invoke time. When two runtimes share a capacity provider and you invoke them with the same runtimeSessionId, AgentCore places both agents on the same EC2 instance, where they share a filesystem and can collaborate on the same task. That’s how the delivery agent reads the .wav the composition agent wrote.
>
> Next, point each runtime at the capacity provider and declare which volumes it mounts:
>
> composition = control.create_agent_runtime(
>
> agentRuntimeName="music_production_composition",
>
> roleArn=execution_arn, # required
>
> agentRuntimeArtifact={"containerConfiguration": {"containerUri": image_uri&#125;&#125;,
>
> protocolConfiguration={"serverProtocol": "HTTP"},
>
> capacityProviderConfiguration={"capacityProviderArn": cp_arn},
>
> filesystemConfigurations=[
>
> {"capacityProviderVolume": {"volumeName": "tracks", "mountPath": "/mnt/tracks"&#125;&#125;,
>
> {"capacityProviderVolume": {"volumeName": "models", "mountPath": "/mnt/models"&#125;&#125;,
>
> ],
>
> lifecycleConfiguration={"idleRuntimeSessionTimeout": 600, "maxLifetime": 86400},
>
> environmentVariables={"AWS_REGION": REGION, "WORKSPACE_DIR": "/mnt/tracks",
>
> "MODELS_DIR": "/mnt/models", "MODEL_ID": MODEL_ID},
>
> )
>
> The compliance agent is the same call with a different artifact, a zip rather than an image, and only the workspace volume:
>
> agentRuntimeArtifact={"codeConfiguration": {
>
> "code": {"s3": {"bucket": bucket, "prefix": key&#125;&#125;,
>
> "runtime": "PYTHON_3_12",
>
> "entryPoint": ["compliance_agent.py"],
>
> &#125;&#125;,
>
> Step 4: Orchestrate multi-agent workflows with shared sessions
>
> Now invoke the agents. This is where the three agents become a pipeline: you pass the same runtimeSessionId to each invocation. The first invocation is the slow one because it provisions the instance. Every call after that routes to the instance already running.
>
> client = boto3.client(
>
> "bedrock-agentcore", region_name=REGION,
>
> config=Config(read_timeout=900, retries={"max_attempts": 2, "mode": "standard"}),
>
> )
>
> session_id = f"music-production-{uuid.uuid4()}" # 33-100 characters
>
> def invoke_agent(runtime_arn, payload):
>
> response = client.invoke_agent_runtime(
>
> agentRuntimeArn=runtime_arn, qualifier="DEFAULT",
>
> runtimeSessionId=session_id, payload=json.dumps(payload).encode(),
>
> )
>
> return json.loads(response["response"].read())
>
> invoke_agent(COMPOSITION_ARN, {"mode": "prepare"})
>
> invoke_agent(COMPOSITION_ARN, {"mode": "catalogue", "track_id": track_id, "duration_s": 20})
>
> invoke_agent(COMPOSITION_ARN, {"mode": "compose", "track_id": track_id, "duration_s": 30,
>
> "prompt": "Create an upbeat electronic track with heavy bass and synth melodies."})
>
> invoke_agent(DELIVERY_ARN, {"track_id": track_id, "platform": "spotify",
>
> "prompt": "Prepare this for streaming delivery."})
>
> result = invoke_agent(COMPLIANCE_ARN, {"track_id": track_id,
>
> "prompt": "Screen this delivery for release."})
>
> print(result["outcome"]) # cleared | review_required | not_cleared
>
> Here’s what that produces on a live g6.xlarge in us-east-2:
>
> 1. prepare model stack (GPU instance + torch + weights) 239s
>
> host : ip-172-31-11-83.us-east-2.compute.internal
>
> stack : ready=True in 125s
>
> 2. render back-catalogue 66s
>
> 3. compose (renders audio on the GPU) 25s
>
> rendered : NVIDIA L4 in 8.98s (peak VRAM 7.63 GiB)
>
> audio 20.062s 48000Hz 2ch -7.5 LUFS peak 0.42 dBTP
>
> 4. delivery (real DSP, verified by measurement) 41s
>
> read : composition.wav &lt;- written by another agent
>
> before -7.5 LUFS peak 0.42 dBTP
>
> after -14.0 LUFS peak -3.2 dBTP
>
> targets : loudness met, true peak held
>
> 5. compliance screen 28s
>
> verdict : REVIEW REQUIRED
>
> screen : 2 reference(s), closest catalogue_00.wav distance 0.0665 (review)
>
> -- collocation -- All 5 steps were served by one instance, as intended.
>
> When you call StopRuntimeSession, the instance idles down automatically. No compute charges accrue while idle. When you invoke the session again, AgentCore resumes it, provided it lands in the same Availability Zone. Amazon Elastic Block Store (Amazon EBS) volumes are AZ-locked. If the original AZ is capacity-dry, volumes can’t reattach and persistence is lost. Use an AZ-pinned ODCR or MODELS_SNAPSHOT_ID so a re-placed resume can recover. Sessions can persist for up to 14 days.
>
> Step 5: Update agents independently
>
> One of the strengths of this architecture is independent deployment. When the Audio AI team ships a new version of the composition agent, they update only their runtime:
>
> # Audio AI team pushes new container version
>
> finch build --platform linux/amd64 \
>
> -f Dockerfile.composition \
>
> -t "$ECR/music-production/composition-agent:v2" .
>
> finch push "$ECR/music-production/composition-agent:v2"
>
> control.update_agent_runtime(
>
> agentRuntimeId=composition_id, # all three are required
>
> roleArn=execution_arn,
>
> agentRuntimeArtifact={"containerConfiguration": {"containerUri": new_uri&#125;&#125;,
>
> capacityProviderConfiguration={"capacityProviderArn": cp_arn},
>
> )
>
> The delivery and compliance agents continue running unchanged. No coordination needed, no shared deploy pipeline, no risk of breaking another team’s agent with your update.
>
> Cleaning up
>
> Delete the session first. It’s the most direct way to stop EC2 and Amazon EBS charges. Deleting a session deprovisions the EC2 resources: instance, network interface, and Amazon EBS volume. Deleting the capacity provider also stops and deletes its associated sessions and their persistent storage. However, you must first disassociate every runtime and runtime version from it, and that detachment is asynchronous. Session deletion is the fast path, and the one to reach for if you want to avoid ongoing charges.
>
> data = boto3.client("bedrock-agentcore", region_name=REGION)
>
> data.delete_capacity_provider_session(capacityProviderId=cp_id, sessionId=session_id)
>
> for rid in runtime_ids:
>
> control.delete_agent_runtime(agentRuntimeId=rid)
>
> # Versions detach from the capacity provider asynchronously, so poll here.
>
> control.delete_capacity_provider(capacityProviderId=cp_id)
>
> Then delete the ECR repositories, S3 artifacts, IAM roles, and Amazon CloudWatch log groups.
>
> Conclusion
>
> In this post, we deployed a multi-agent music production system on Amazon Bedrock AgentCore Runtime Instances. Three agents, built by different teams using different packaging formats, collaborated within one session on a single GPU instance, and produced a track you can play.
>
> The architecture demonstrates several patterns that apply beyond music production:
>
> Colocation through shared sessions. Multiple agent runtimes on the same capacity provider share an instance when invoked with the same session ID, which gives them one host: the same GPU, the same local volume, the same process space.
>
> Independent team deployment. Each agent has its own runtime lifecycle. Teams ship on their own cadence without coordination.
>
> Mixed artifact types. Containers and code packages coexist on the same infrastructure. Use whatever packaging fits your team’s workflow.
>
> Multi-day persistence. Stop sessions when work pauses, resume by invoking again. Sessions persist for up to 14 days (resume depends on landing in the same AZ).
>
> Music was a convenient vehicle, but nothing about the architecture is musical. Swap out the render step and the same three-agent shape fits the workloads AWS calls out for GPU Instances: 3D rendering, simulation, model inference, media processing. Or a long-running job where a pipeline produces a large artifact, hands it to a second agent to transform, and has a third check the result before it ships.
>
> To learn more, see the Amazon Bedrock AgentCore documentation. For the complete working code from this post, explore the AgentCore samples repository. For advanced orchestration patterns like Graph, Swarm, or Workflow, see the Strands Agents documentation.
>
> About the authors
>
> Evandro Franco
>
> Evandro is a Sr. Data Scientist working on Amazon Web Services. He is part of the Global GTM team that helps AWS customers overcome business challenges related to AI/ML on top of AWS, mainly on Amazon Bedrock AgentCore and Strands Agents. He has more than 18 years of experience working with technology, from software development, infrastructure, serverless, to machine learning. In his free time, Evandro enjoys playing with his son, mainly building some funny Lego bricks.
>
> Rui Cardoso
>
> Rui is a Sr. Partner Solutions Architect at AWS, specializing in Agentic AI and Physical AI. He works with AWS Partners to take solutions from prototype to production, spanning agentic workloads and accuracy evaluation frameworks for enterprise applications. His focus is helping partners build reliably on well-architected foundations.
>
> Sayee Kulkarni
>
> Sayee is a Software Development Engineer on the Amazon Bedrock AgentCore service. Her team is responsible for building and maintaining the AgentCore Runtime platform, a foundational component that enables customers to leverage agentic AI capabilities. She is driven by delivering tangible customer value, and this customer-centric focus motivates her work. Sayee led the design and launch of AgentCore Runtime Instances, driving the project from architecture through general availability and empowering customers to run persistent, long-running agentic workloads with the flexibility and control to build sophisticated multi-agent systems.
>
> Yanis Telaoumaten
>
> Yanis is a Software Development Engineer on the Amazon Bedrock AgentCore service. His team builds AgentCore Runtime Instances, a platform that lets agents run for days on instances customized to their specific needs. Yanis conceived, designed, and led the implementation of the platform, driving cross-organizational collaboration and clearing roadblocks to ensure a successful delivery.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。