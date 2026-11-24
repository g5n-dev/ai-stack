---
title: "AI-driven technique could help engineers design analog chips faster and with less expense"
date: 2026-11-23T17:01:46+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "AI Agent", "生成式 AI", "机器学习", "Research", "Computer chips", "Electronics", "Artificial intelligence"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:c2b6c78f35b8aae608aed58ec73ff38a06348b39b4f340777ae763b60ade7e40"
source_payload_sha256: "sha256:cb01e99c04e73122da83179200b9f96b0caef953e5b5e210e6dc17b899ccd964"
observation_id: obs_e652a8cea9964851948030d342a17563b038e04a13384a585f834044ebe4a8c0
event_id: evt_3ef167f3b69295da5784015cc92d831b3823a08b69c443e6aeb620b5c7207292
revision_id: rev_a820b531224dffc9e019fe4c810737ace4142222dcd4f43b195acd8fa3871926
source_published_at: 2026-11-23T05:00:00Z
first_seen_at: 2026-11-23T09:13:15Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 89
interpretation_sha256: "sha256:50516f26bc4a6ceda95e6921dbdc49b4744a06e4e26bcdde08d8cf1e63b1ddcf"
description: "MIT 研究人员提出 SLIC，通过多轮强化学习和可验证奖励，训练小型语言模型自动设计模拟集成电路，并让模型依据仿真反馈持续优化方案。"
external_url: https://news.mit.edu/2026/ai-driven-technique-could-help-engineers-design-analog-chips-faster-and-less-expensive-1123
parent_observation_id: null
last_seen_at: 2026-11-24T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://news.mit.edu/2026/ai-driven-technique-could-help-engineers-design-analog-chips-faster-and-less-expensive-1123](https://news.mit.edu/2026/ai-driven-technique-could-help-engineers-design-analog-chips-faster-and-less-expensive-1123)
- **发布域名**: news.mit.edu

## 要点解读

### 这是什么
MIT 研究人员提出 SLIC，通过多轮强化学习和可验证奖励，训练小型语言模型自动设计模拟集成电路，并让模型依据仿真反馈持续优化方案。

### 用在哪里
该方法可用于通信、电源管理，以及机器人、医疗监护器和工业传感器中的芯片设计，帮助工程师减少人工调参和原型制作时间。它也能在本地运行，使用企业的机密电路数据，同时降低对云端模型的依赖。

### 可以推断的
- 推测：本地部署与可解释的迭代过程，可能更容易获得注重数据保护和定制化能力的芯片团队关注。
- 推测：若实际设计结果能稳定满足性能与能效目标，这类方法可能成为模拟电路设计流程中的辅助工具。

## 来源摘要/节选

> A new technique developed by MIT researchers could help engineers use artificial intelligence to streamline the design and innovation of analog integrated circuits, semiconductor chips that perform vital functions like communication and power management in electronic devices.
>
> In the future, this method could allow engineers to prototype faster, explore a wider range of chip designs, and discover new design schemes that might improve the performance and energy efficiency of robots, medical monitors, or industrial sensors.
>
> Designing analog integrated circuits that meet specific requirements is usually a cumbersome manual process due to the enormous number of possibilities. Frontier generative AI models have shown success in automating the process, but using these resource-intensive, cloud-hosted models could expose proprietary circuit design and semiconductor foundry data to malicious users.
>
> The MIT method, called Small LM Iterating on Circuits, or SLIC (pronounced “slick”), enables engineers to train a small language model to perform analog circuit design as well as or better than a frontier large language model (LLM).
>
> This small model is inexpensive and efficient enough to run on a laptop. Because it’s trained and deployed locally, it can use a company’s circuit design data without raising privacy risks.
>
> When compared to complementary baselines and open-weight frontier LLMs, a small model trained by SLIC more effectively generated designs that achieved the circuit objectives.
>
> “We’ve provided an alternative option to automate analog circuit design. With our technique, engineers can train a small, locally deployable model, using their own confidential data, and then deploy it in their own environment to ensure their assets remain protected,” says Yan Xu, an electrical engineering and computer science (EECS) graduate student and lead author of a paper on this technique.
>
> She is joined on the paper by senior author Ruonan Han, a professor of EECS and a member of the MIT Research Laboratory of Electronics; Zhengqi Gao PhD ’26; Wenjie Lu PhD ’18, a former MIT postdoc who is now a principal research scientist at Analog Devices, Inc.; Xin Zhang, a research manager at IBM Research; Duane S. Boning, the Clarence J. LeBel Professor in EECS and MIT vice provost for international activities; and others at IBM Research and Analog Devices. The research will be presented at the 2026 Conference on Neural Information Processing Systems.
>
> “Through some specialized training and area-specific research, we can use much smaller models that consume far fewer resources to achieve almost the same results as flagship models in analog circuit design,” says Han. “This opens many more possibilities in the design of complex chips, especially if we care about costs, data privacy, and customization.”
>
> Mimicking human learning
>
> Analog integrated circuits enable a device to interact with the physical world. For instance, these circuits boost incoming wireless signals in smartphones and process outputs from sensors that track a car’s engine temperature.
>
> Real-world signals tend to be unpredictable, so engineers must balance a wide and complex array of targets and tradeoffs to maximize analog circuit performance. This has made the design problem especially challenging for AI models.
>
> “To design a circuit, engineers find a good starting point based on their intuition and then, drawing on their knowledge of circuit design, tune a few knobs toward the performance they want,” says Xu. “There is no universal way to solve every circuit design problem.”
>
> Even if a powerful, cloud-based model could design a circuit as well as a human, most companies would be reluctant to send their foundry-specific data to external AI service providers.
>
> With SLIC, the MIT researchers created a training method that teaches a smaller, less expensive, faster language model to design analog integrated circuits that meet user specifications.
>
> The SLIC model uses a few billion parameters, making it several thousand times smaller than frontier models that use trillions of parameters and require enormous amounts of computational resources.
>
> “We tried to mimic the behavior of how a human learns to design a circuit,” Xu says.
>
> They used a technique called multi-turn reinforcement learning with verifiable rewards, where a model works through a multi-step task while adapting to environmental feedback.
>
> When given an analog circuit optimization task, SLIC uses a large LLM to generate several demonstrations of the open source design process. Then SLIC then uses these demonstrations to guide the small model in mimicking this design process.
>
> After the small model gains some initial knowledge about circuit design, SLIC lets it practice by tackling a new design problem on its own.
>
> The model makes an initial guess of the design parameters, performs simulations, evaluates the results, and iteratively refines the design using knowledge it gained about analog circuits.
>
> Once a design achieves the user’s goals, SLIC prioritizes additional marginal gains. This means the model keeps learning to make improvements that boost performance even when several designs meet the user-defined targets.
>
> An interpretable process
>
> Importantly, because SLIC employs models that describe their reasoning using natural language, the user can understand the decisions it makes along the way.
>
> “Although the whole process is automated, the user can see what is going on inside the model. This could help the user gain some new ideas about circuit design, and it also adds a lot of confidence about the decision-making process,” Han says.
>
> An engineer could utilize SLIC by adapting the researchers’ trained model to their data using a fine-tuning process. Or they could employ the SLIC training process to build their own model with company data, allowing for more customization.
>
> “We are seeing an increasing demand for analog chips, but the speed of design has not kept up. This research is trying to bring new capabilities to AI to solve a problem that industry has been stuck on for decades,” Lu says.
>
> When the researchers tested SLIC’s ability to design a circuit that met desired performance metrics, their small model came close to matching the performance of the latest GPT model (GPT-6-Astra). It did this while using a fraction of the computational resources.
>
> The researchers also found that the SLIC model maintained its performance when tackling previously unseen circuit structures and adapting to more advanced technology nodes (design and manufacturing rules) and real commercial processes.
>
> Because SLIC teaches a model the general chip design process, the system is not tied to any company. This makes it a more scalable approach that could be used by many organizations for a range of circuit applications.
>
> “The knowledge the model has gained about circuit design is universal in nature. That is the powerful aspect of this tool,” Han says.
>
> In the future, the researchers want to explore self-improving models that can independently learn to handle more diverse topologies and design targets. They also want to use SLIC to build a multi-agent framework, in which many small language models work on different parts of a complex circuit design task.
>
> “Yan’s work shows that a locally deployable model can learn transferable design behavior and iterate with a circuit simulator to improve a design, which could reduce repetitive manual tuning for engineers. This is the kind of work the MIT-IBM Computing Research Lab makes possible. We see it as opening the door to more sophisticated custom design, including RF and microwave circuits, in the settings where industry actually works,” says Zhang.
>
> This research is funded, in part, by Analog Device, Inc., IBM, and the John L. Ocampo Endowment Fund of MACOM Technology Solutions.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。