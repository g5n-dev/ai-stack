---
title: "The Inference Engineering Masterclass — Philip Kiely & Ali Taha, Baseten"
date: 2026-08-04T07:21:57+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "生成式 AI", "Prompt 工程", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:ba72a583d616898c4fbcb5ab8a130f858bb6f7649b72a2fd6f6ab6bd069d57d3"
source_payload_sha256: "sha256:21bc847f8952fec9d046cc53a2e82f51b1ce6c2a1a861137bb94956f01c466c4"
observation_id: obs_20eb9da94f2bded7e24f9a9c7d3624e8ddc45336085efade74fdb52b726c7b67
event_id: evt_7147bc784e40688f4115b33ec1f79adf5b5b90dec40636e630c501ddfe28497f
revision_id: rev_6ed23b4a8e09342342eef339051c72becadb56765811797a60ea9bd03555470f
source_published_at: 2026-08-03T21:44:03Z
first_seen_at: 2026-08-03T23:19:37.619453Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: true
source_truncation_reason: "crawler_feed_content_limit"
source_support: 1.0
source_title_chars_original: 72
interpretation_sha256: "sha256:178e1306cf6beefa8f89833e8e996a0a5f06a82f653723e38aea9202fc2e57a8"
description: "这是一期播客节目，邀请了 Baseten 的工程师讨论推理工程的核心问题，即如何将训练好的模型转化为可在生产环境中快速、可靠且低成本运行的 API。"
external_url: https://www.latent.space/p/inference-eng
parent_observation_id: null
last_seen_at: 2026-08-03T23:19:37.619453Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://www.latent.space/p/inference-eng](https://www.latent.space/p/inference-eng)
- **发布域名**: www.latent.space

## 要点解读

### 这是什么
这是一期播客节目，邀请了 Baseten 的工程师讨论推理工程的核心问题，即如何将训练好的模型转化为可在生产环境中快速、可靠且低成本运行的 API。

### 用在哪里
适合想了解模型部署后端优化的工程师，以及需要掌握推理系统工程知识的技术人员。

### 可以推断的
推测：节目内容可能涉及大量实践经验，适合需要解决实际推理性能问题的人员参考。推理工程作为一个新兴领域，相关讨论可能对从业者了解行业趋势有所帮助。

## 来源摘要/节选

> We first covered Baseten last year when DeepSeek mania was at peak hype. Now they have raised a monster $13B round and become one of the new cohort of AI Infra decacorns that are (with Nvidia, Intel, and the semis complex) chief beneficiaries of the Inference Inflection.
>
> We return to Baseten at the peak of the 2026 edition of Open Weights debate. Ali has published a viral breakdown of Kimi K3:
>
> And since you last saw him, Philip has spoken at AI Engineer and written the definitive book on Inference Engineering spotted all over SF:
>
> Three years ago, inference engineering barely existed as a category.
>
> Today, it is one of the most critical disciplines in AI. Inference engineering inherently tackles a different question than standard model training: “How do you turn those weights from training into a product that is fast, reliable, and affordable at scale?” Focusing on these creates an entirely new optimization problem.
>
> In one recent GLM-5.2 experiment, quantizing more of the model actually preserved its benchmark quality while increasing throughput by 20%, because the errors introduced in different layers could cancel each other out.
>
> Inference is no longer just the final step after training. It is becoming its own engineering discipline, with its own research problems, infrastructure, and increasingly specialized roles.
>
> In this episode, Baseten’s Philip Kiely and Ali Taha join swyx and Vibhu to explain what actually happens after a new open model is released and what it takes to turn “we generated a token” into a fast, reliable, production-ready API.
>
> We go deep on cache-aware routing, disaggregated prefill and decode, quantization, speculative decoding, KV-cache movement, model parallelism, GPU kernels, and the race to make frontier models up to 10× faster. Philip and Ali explain why inference optimizations can still produce gains of 20%, 100%, or even 200%; how quantization errors can cancel one another out; why identical weights can behave differently across clusters; and how Baseten grafted a Kimi vision encoder onto GLM-5.2 without changing the underlying language model.
>
> The conversation then expands beyond LLMs into NVIDIA Dynamo, mega kernels, Rubin, AI-specific chips, local inference, video generation, diffusion versus autoregressive models, and the enormous compute barrier to generating coherent long-form video. Finally, we explore the convergence of training and inference, continual learning through persistent KV cache, and the emerging loop where models help optimize the infrastructure that runs them.
>
> We discuss:
>
> What happens when a 200,000-token request enters an inference system
>
> Cache-aware routing and reusing previously computed KV cache
>
> Why prefill and decode are increasingly handled by different GPUs
>
> When dedicated deployments become cheaper and more reliable than shared APIs
>
> How speculative decoding uses a smaller model to accelerate a larger one
>
> Tool calling, structured outputs, and what LLMs actually do
>
> What it takes to support a new open model on day zero
>
> Grafting Kimi’s vision encoder onto GLM-5.2
>
> Retrofitting inefficient model layers with components from other architectures
>
> Why models sometimes collapse into repeating the same token
>
> How hardware, kernels, and race conditions create nondeterministic failures
>
> Preserving model fidelity while making inference faster
>
> How quantization errors can cancel each other out
>
> Why inference optimizations still deliver gains of 20%, 100%, and 200%
>
> How optimized serving can make a model up to 10× faster
>
> NVIDIA Dynamo, KV-aware routing, and distributed model serving
>
> Speculative decoding the speculative decoder
>
> Why local AI is about making models less dumb while data-center AI is about making them less slow
>
> Tensor, expert, and pipeline parallelism across GPUs
>
> Hardware-aware model design, auto-tuning, and the case against mega kernels
>
> Rubin and why inference is becoming a systems problem
>
> Whether modern GPUs are evolving into programmable AI ASICs
>
> Why enormous models like Kimi K3 require GB300-class hardware
>
> Why open-source video generation still trails Veo, Kling, and other closed models
>
> The quadratic attention bottleneck behind long-form AI video
>
> Autoregressive video, real-time generation, and compounding quality drift
>
> Why future video systems may combine autoregressive and diffusion architectures
>
> Training for inference and inference for training
>
> Continuous post-training, deployment, evaluation, and improvement loops
>
> How GLM-5.2 helped optimize the kernels serving GLM-5.2 itself
>
> Why faster networking could unlock dramatically faster decoding
>
> Continual learning, KV-cache compaction, and persistent model memory
>
> Show Notes
>
> How to build a day-0 API for Kimi K3
>
> 22580: From GPT2 to Kimi3, Explained
>
> Philip Kiely
>
> LinkedIn: https://www.linkedin.com/in/philipkiely
>
> X: https://x.com/philipkiely
>
> Inference Engineering: https://www.baseten.co/inference-engineering/
>
> Ali Taha
>
> LinkedIn: https://www.linkedin.com/in/aliestaha/
>
> X: https://x.com/waterloointern
>
> Timestamps
>
> 00:00:00 Introduction and the 200K-Token Prompt
>
> 00:03:18 Dedicated Deployments, Speculative Decoding, and Tool Calling
>
> 00:11:26 Launching Production-Ready Open Models
>
> 00:19:06 Model Retrofits, Failure Modes, and Nondeterminism
>
> 00:28:22 Quantization and Canceling Errors
>
> 00:32:15 The Race to 10× Faster Inference
>
> 00:40:48 Dynamo, Speculation, and Local vs. Data-Center AI
>
> 00:50:18 Model Parallelism, Auto-Tuning, and Mega Kernels
>
> 01:00:55 Rubin, GPUs vs. ASICs, and Custom AI Chips
>
> 01:10:03 Giant Models and the Limits of GPU Memory
>
> 01:12:42 AI Video, Quadratic Attention, and Autoregressive Generation
>
> 01:21:47 Audio, Images, and Diffusion Models
>
> 01:27:32 Training, Self-Optimizing Models, and Continual Learning
>
> 01:40:06 Closing Thoughts
>
> Transcript
>
> Introduction: Baseten, Waterloo Intern, and Inference Engineering
>
> Swyx [00:00:00]: Okay, we’re here in the studio with Philip, old friend from Inference Engineering, the book, as well as Baseten and everything that you’ve done, you and I have done before, as well as Ali. Welcome.
>
> Ali [00:00:15]: Pleasure to meet you.
>
> Swyx [00:00:15]: Waterloo intern.
>
> Ali [00:00:16]: Waterloo intern, always.
>
> Swyx [00:00:17]: When did you get “Waterloo intern” as a handle?
>
> Ali [00:00:19]: As a handle? Oh.
>
> Ali [00:00:20]: I think the rebranding happened mid-March. When I saw it was open, I was like, “I have to take it. Up for grabs.”
>
> Philip [00:00:26]: The problem is that Ali is really good at his job and is not gonna be an intern much longer.
>
> Philip [00:00:30]: So we have to figure out who’s gonna get the handle.
>
> Ali [00:00:33]: Well, I’ll pass the torch over to the next intern.
>
> Swyx [00:00:34]: Oh, okay. It can be, like, you just pass it to another Waterloo grad.
>
> Ali [00:00:37]: To another Waterloo intern. No, bruh.
>
> Philip [00:00:39]: Yeah.
>
> Ali [00:00:39]: Intern.
>
> Swyx [00:00:40]: Intern, yeah.
>
> Ali [00:00:40]: And no.
>
> Philip [00:00:41]: You gotta get an intern from Waterloo.
>
> Ali [00:00:42]: Yeah, I’ve gotta get an intern from Waterloo.
>
> Swyx [00:00:44]: Right.
>
> Ali [00:00:44]: But they have to follow the path.
>
> Swyx [00:00:45]: Oh, it could, but it could come from Baseten, so it’s like whoever Baseten gets from Waterloo.
>
> Ali [00:00:48]: Right.
>
> Swyx [00:00:49]: Has the title of Waterloo.
>
> Ali [00:00:50]: It stays in the ecosystem.
>
> Philip [00:00:51]: Exactly.
>
> Ali [00:00:52]: Halfway through the internship, you either get it or you’re out.
>
> Philip [00:00:55]: You should also do, like, a big graduation ceremony where you change the handle.
>
> Ali [00:00:59]: Just say it.
>
> Philip [00:00:59]: For everybody.
>
> Swyx [00:01:00]: You guys are good at ceremonies, clearly. We had a nice launch of the book, very successful. But before we get into all that, I wanna start off with a fun question for you. Okay, you’re an expert inference engineer. What happens when I send a long query, say two hundred thousand tokens into Baseten’s inference? What’s the process of query through GPU model routing, balancing, all that? What is all the stuff that we don’t think about?
>
> Long Context Requests, KV Cache, and Cache-Aware Routing
>
> Philip [00:01:26]: With a long query specifically, the first thing that I’m gonna ask is, “Have you sent me this query before, or at least part of it?” and I really hope you have, because it’s gonna be a lot easier for me and a lot cheaper for you. So the first thing that we’re gonna look at is some cache-aware routing, where we’re going to see, we probably have a number of instances, a number of replicas up serving whatever model you’re hitting. We want to send this one to something with, number one, available prefill workers, and number two, ideally some cached input already there so that we can skip prefill on at least part of these two hundred thousand tokens. If you’re doing two hundred thousand tokens, it’s probably coding or a multi-turn agent or something where you would expect to have that cached. If you don’t, we’re gonna have to send it to a prefill worker. We’ve at least on certain models disaggregated prefill and decode, so you’re going to have one set of GPUs that’s solely going to process the input, create the KV cache, and get you your first token, and then that’s going to be passed over to a separate set of GPUs, which is going to run decode. We’re going to iteratively make those tokens. We’re probably going to have some speculator model in front of that. I’m going to assume that you’re doing coding, and because of that, our speculator model, which assumes you’re doing coding, is gonna have a high draft token acceptance rate. If I’m wrong and you’re asking me to summarize every Harry Potter book, it’s gonna be slower. And then we stream that output to you and account for it, charge you, a couple of pennies and say, “Hey, would you like to send another one?”
>
> Swyx [00:03:04]: Except Baseten doesn’t charge by pennies.
>
> Philip [00:03:07]: Well, yeah, we charge. I’m assuming that we’re talking about the public model APIs. If you are setting up a dedicated deployment, then yeah, it’s not pennies.
>
> Public APIs vs. Dedicated Deployments
>
> Swyx [00:03:18]: Yeah, one of the key differentiators when I was talking with Baseten initially was that people who want very high volume just need to rent by the box, ‘cause then it’s up to you to figure out how to saturate the box.
>
> Ali [00:03:31]: And more often than not, it’s, like, way cheaper if you’re pushing, like, millions of tokens per hour, if you just pay per hour instead of pay per token.
>
> Philip [00:03:37]: Yeah, they do. I think that we’ve increasingly seen a lot of demand for the pay per token APIs, just because everyone wants to try open models, and then once they find a use case that’s really sticky, then they move over to dedicated.
>
> Swyx [00:03:51]: Is there a best practice on when it’s time to swap over?
>
> Philip [00:03:54]: Couple reasons. Yeah, reliability, that’s a big one, right?
>
> Ali [00:03:57]: Like, if they have a very specific use case, they want you to train something specifically for them, like they want their own spec dec, for instance, for their own traffic.
>
> Swyx [00:04:04]: Spec dec is speculative decoding.
>
> Speculative Decoding and Custom Speculators
>
> Ali [00:04:05]: Speculative decoding, yeah.
>
> Swyx [00:04:07]: You have to explain.
>
> Ali [00:04:07]: Sorry. Like, speculative decoding is like, if you have a huge model, right? And so the model is going to be generating one token at a time every single turn, every single forward pass. So we attach, like, this little, like, parasite, like this layer that goes on top of the model, and this model just has to predict. It does three very fast autoregressive forward passes, and it will predict, like, three certain tokens, and then you do one forward stage over the entire original model in order to see if those predictions were correct or not, and then you accept them or you reject them. Now, this draft model is traffic specific, so if you, like, Philip said, if you’re summarizing Harry Potter books, I can train exclusively that draft model on Harry Potter books, and I can guarantee you that I’m gonna accept the three tokens every single time. And so with that case, I increase your decode speed. I wouldn’t be able to provide this to you if you’re a shared endpoint
>
> Swyx [00:04:53]: Yeah
>
> Ali [00:04:53]: ‘cause I have no idea if you’re doing Harry Potter, if you’re doing coding, if you’re doing English. We don’t know. Also, there was a thing in the book that mentioned that if they really cared about a specific threshold, chapter four, I think. Do you remember that?
>
> Philip [00:05:06]: Yeah. The things that you can do is you can set a specific, like, batch sizing, a specific, like, parallelism strategy if you’re trying to optimize for, like, throughput versus latency. You can. Maybe a NVFP4 quant doesn’t pass your benchmarks and you wanna run a model at higher precision, you could do that. There’s just a bunch of reasons why you might wanna have your own endpoint and the biggest one, of course, just being, like, you don’t have to deal with someone else doing a hundred million tokens of benchmarking traffic at the endpoint when you happen to be trying to serve your users.
>
> Swyx [00:05:40]: Yeah. I think one thing that is. That is a classic journey. Like, it’s people is asking the, what happens when you type Google into the browser. Tool calling, is that just, you’re generating JSON or is there more complication beyond that?
>
> Tool Calling, JSON, and Structured Outputs
>
> Ali [00:05:58]: Certain customers that we have, they have their own post-trained models, and so they demand a tool calling that’s not just, like parse a file or go find the weather. It’s something that’s very specific and you have to do post-training on this. And if the post-training on the model is not good or if the quantization after the post-training to get the inference to be fast, the model will struggle reading the JSON file and reading the tool calling. But it doesn’t require its own like sandbox. It’s not like it’s going to use that tool calling to like escape a sandbox or like it doesn’t have to be contained. It can just be a normal dedicated deployment. The challenge with tool calling more and more seems to be that the companies want certain tool calling which is a very sensitive thing to train. And because you’re dealing with all of the JSON outputs, if it doesn’t like close the end of the request in a very certain manner, you end up with a model that did the tool calling and like the thinking and so as a result of that, it didn’t see the result and just hallucinated the result as it decoded. That seems to be the most challenging thing with tool calling, not really the sandboxes model.
>
> Philip [00:06:56]: Yeah, that’s a challenge on the training side and then on the inference side, there’s work that you can do to scope the possible output. So we published this at this point close to two years ago, the solution to this problem which is you make a state machine and you use that to constrain the output to a specific format. So this is the structured output problem. If you remember back
>
> Swyx [00:07:27]: Yeah, the specific grammar is,
>
> Philip [00:07:29]: Yeah, exactly
>
> Swyx [00:07:30]: GML had this thing.
>
> Philip [00:07:31]: Yeah. So it’s like the old-school “make sure this is only JSON”, return only JSON or
>
> Swyx [00:07:38]: Yeah
>
> Philip [00:07:38]: Grandma’s gonna die type of prompts.
>
> Swyx [00:07:39]: Is it BNF grammar? At some point OpenAI had released a thing that was like, yeah, if you want to constrain your output, write BNF grammar, back as NOR.
>
> Philip [00:07:47]: In our inference system, it’s just a specified output format. And you get the guarantee that your output’s gonna be structured along that format. And so applying that to tool calls can like help cut down on. You can still call the wrong tool or call no tool. It doesn’t solve the certainty problem but it at least solves the output structuring problem
>
> Swyx [00:08:10]: Yeah
>
> Philip [00:08:10]: Within tool calls.
>
> Swyx [00:08:12]: And MCP is just another form of tool, right.
>
> Philip [00:08:14]: Yeah, exactly.
>
> Swyx [00:08:15]: As far as there’s no special thing there.
>
> Philip [00:08:16]: The thing I’m always like explaining to people is the LLM is not capable of doing anything. It’s only capable of making suggestions of what to do and then if those suggestions are formatted in a certain way and applied to a system that knows what to do with them, then an action occurs.
>
> Swyx [00:08:32]: Yeah. Part of the fun stuff is, this is solved outside of tool calling too. Like in an agent loop if the output is not correct or you’re right, like reasoning, tool calling was done in the reasoning trace, just be like, “Oh, I don’t know what to do. Let me just try again.” And it might get there after a few tries. And on your point of training, sometimes this is harder in smaller models, so you don’t have the same exact quality output
>
> Ali [00:08:56]: Right.
>
> Swyx [00:08:57]: When you just swap from a big model, right?
>
> Ali [00:08:59]: Yeah. I will say that, before, I think we need to go back to inference engineering proper.
>
> Ali [00:09:04]: But, I had expected that something would replace JSON because it’s hard to stream JSON ‘cause JSON must be complete and you must have open and close brackets and everything. So it’s hard to parse something or validate something while it’s being streamed. So people invented all sorts of things that are like, I forget the name of some of these alternatives, but it’s something like TOML, something like YAML. But JSON seems to be dominant still.
>
> Philip [00:09:30]: The JSON outputs aren’t that long, right? Like you could have a long-- ‘cause tool calls also contain the arguments in them and perhaps for a certain tool you might pass like a very long argument. But my impression of the median tool call is that it’s a relatively small number of tokens, right? So I would expect that speculators are generally fairly good at something as formatted as JSON. And so you would have like a pretty fast decode step there and that the streaming wouldn’t be as valuable, but maybe I’m wrong about that.
>
> Ali [00:10:02]: I think you’re also bounded by the software or that the model is gonna integrate with if the software is built with JSON for the tool calls or if the company that you’- if your customer says that this is how our software works and our tools are interfaced with JSON, you can ask them to like, change their software and say like, “Yeah, this is gonna be better for the model.” but like with the right training shouldn’t be that much of a difference. Also more profitable if it outputs more tokens probably.
>
> Swyx [00:10:25]: Depends on your business model.
>
> Swyx [00:10:27]: It really depends. But I will say that, as a writer with like experience a lot with generated output, I do try to move from text to JSON text which is very long JSON, right? Like there’s paragraphs in every field because I’m trying to structure it, right?
>
> Philip [00:10:44]: Right.
>
> Swyx [00:10:44]: I want you to first make factual statements, then make opinions then make bullet point summaries, have dates, have entity references have your sources for references, all these things. Anyway, so these are things that like I think people who really experiment with structural output have to really care about. But, let’s, let’s recurse up the stack a little bit. Before we started recording, you mentioned something really cool, which is that there’s a lot of engineering that-- inference engineering that goes on when a new model provider releases a new model, right? So let’s call it GLM-5.2, Kimi K3. I had previously assumed, especially if it’s like, well, GLM 5 to 5.1 to GLM-5.2, like that you’ve supported them before. Is it that much work?
>
> What It Takes to Support a New Open Model
>
> Ali [00:11:26]: It’s a lot of work.
>
> Swyx [00:11:28]: Yeah. Okay. So like, a lot of people, all you guys, right whenever a new model launch like, people rush to say like, “Oh, Hugging Face supports this, Fireworks supports this, Spacetime supports this,” and I’m like, “Yeah, of course we support it.” But what goes into that? What goes into
>
> Philip [00:11:40]: I think it’s more than just support it too, right? It benefits the consumer a lot. Like I think it was with Kimi K2.5 or GLM-5.2 the latest, there was an inference war, right? X provider is at 90 tokens a second. The next day we’re at 150. The next
>
> Swyx [00:11:55]: I kinda kicked that off with the GLM-5.2.
>
> Swyx [00:11:58]: I wrote a Twitter article about. It got like half a million views,
>
> Ali [00:12:02]: Based on being number
>
> Swyx [00:12:03]: Yeah
>
> Ali [00:12:04]: Or it’s for something else.
>
> Swyx [00:12:05]: Yeah. Which,
>
> Ali [00:12:06]: Oh my God
>
> Swyx [00:12:07]: Which then got everyone really excited about, hey, how can we, bend tracks a little bit further and,
>
> Philip [00:12:14]: There’s a difference between support the model, as in I can make a token out of this model, and support a model, as in I have a production-ready API from this model.
>
> Philip [00:12:26]: Getting to the point of I can make a token out of this model is not that hard because generally the, open source inference engines, vLLM, SGLang of the world oftentimes even receive weights ahead of time, maintainers do, or the people making the model merge PRs to ensure support. So you generally can, just get it working on the standard open source stack without too much pain in most cases. The challenge is, every inference company is gonna have own proprietary stack. Some open source components, some in-house stuff. And for any arbitrary model, there’s going to be some new stuff. Sometimes you get lucky, like K, two five to two six was, like, pretty similar.
>
> Quantization, Speculators, and Production Readiness
>
> Ali [00:13:16]: Yeah. It was pure continued post-training
>
> Philip [00:13:18]: Yeah
>
> Ali [00:13:18]: If I remember correctly.
>
> Philip [00:13:19]: Even in those cases, there’s still stuff you have to do. You have to redo the quantization work. You’re taking the model from. Generally, these models are not released in NVFP4, and we want them to be in NVFP4 for maximum Blackwell compatibility. So we have to perform that quantization, and, calibrate the quantization to make sure that we’re not causing any regression in the model’s intelligence. And then we also have to train the speculator, as we’ve talked about. Generally, we have. We have ZDR, zero data retention on our model APIs, so we don’t know exactly the traffic that people are sending us, but we know what’s popular. We know that coding use cases are popular. We know that agents, agentic use cases are popular. So we can get public data sets that are representative of that traffic and train general speculators. Now, with speculators today, you need to train the speculator using the base model itself because you’re getting hidden states out of the model from running inference on these specific prompts, and that is the training data you use to create the speculator. So there’s that process which you need the real model weights for. And then there’s of course just the process of, standing up all the infrastructure behind it, loading all this stuff, testing it. And then when there’s a new model with a newer architecture, I think that, like, the DeepSeek models tend to be the most challenging as they have, like, the most novel architectural stuff going on, model after model. But every new model has something. Kimi K2 had. Oh, sorry, GLM-5.2 had
>
> Ali [00:14:53]: Sparse attention.
>
> Philip [00:14:54]: Yeah,
>
> Ali [00:14:54]: Yeah
>
> Philip [00:14:54]: the DSA.
>
> Ali [00:14:55]: Right. Which is brought from DeepSeek.
>
> Philip [00:14:57]: Yeah. And
>
> Ali [00:14:59]: So you can copy-paste then?
>
> Philip [00:15:01]: It kind
>
> Ali [00:15:01]: I don’t know how this works.
>
> Philip [00:15:02]: So, like we had to, like, build support for that into our runtime. And you’re right, like it is really interesting the way that all of these open source labs borrow from each other. For example, like GLM-5.2 doesn’t have vision. So something that, Haley, a guy on our team, if we could take a look at this, he, like, grafted the Kimi vision encoder onto GLM-5.2.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。