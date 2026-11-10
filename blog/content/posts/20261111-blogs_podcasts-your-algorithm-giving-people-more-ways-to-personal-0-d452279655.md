---
title: "Your Algorithm: Giving People More Ways to Personalize Facebook Recommendations"
date: 2026-11-11T01:50:22+08:00
draft: false
entry_kind: "auto"
tags: ["大语言模型", "ML Applications", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:c7ca1e8671aa4e70feeba99aa394bdfaf2dc1143fb2138c5548fb8417f723d39"
source_payload_sha256: "sha256:95553d6a94b25256d42e88779a266468ace298cab95ab74843a03ee6585cf5f1"
observation_id: obs_d45227965598a9a1d43b518eccc62090ab7239daf9681654c84b65358a17f703
event_id: evt_b346359e5c38ef1ed1a206a93d6ad869dd460530f49bbddfc88673c72296a993
revision_id: rev_7e116e23ea5fc50cb68027e110843bd6629db51f46a4a2ed7f904a71e22d5595
source_published_at: 2026-11-10T17:00:49Z
first_seen_at: 2026-11-10T17:49:17.328142Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 79
interpretation_sha256: "sha256:d41174d4f7cefe7288dc215b2fd2f348968bd64d88a3e1612f8a26839e0b9edd"
description: "Your algorithm 是 Facebook 用于个性化推荐的 AI 工具套件：用户可用自然语言添加、移动或删除兴趣，系统结合大语言模型与行为信号，实时调整 Feed 和 Reels 的内容排序。"
external_url: https://engineering.fb.com/2026/11/10/ml-applications/your-algorithm-giving-people-more-ways-to-personalize-facebook-recommendations
parent_observation_id: null
last_seen_at: 2026-11-10T17:49:17.328142Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://engineering.fb.com/2026/11/10/ml-applications/your-algorithm-giving-people-more-ways-to-personalize-facebook-recommendations](https://engineering.fb.com/2026/11/10/ml-applications/your-algorithm-giving-people-more-ways-to-personalize-facebook-recommendations)
- **发布域名**: engineering.fb.com

## 要点解读

### 这是什么
Your algorithm 是 Facebook 用于个性化推荐的 AI 工具套件：用户可用自然语言添加、移动或删除兴趣，系统结合大语言模型与行为信号，实时调整 Feed 和 Reels 的内容排序。

### 用在哪里
它应用于 Facebook 的 Feed 与 Reels 推荐流程，覆盖兴趣画像、偏好管理、内容检索、重排序和设备端展示。用户可通过统一的兴趣页面控制推荐倾向，系统则通过分层过滤、额外内容加载和缓存失效让修改更快生效。

### 可以推断的
- 推测：让用户直接描述偏好，可能降低其通过长期点击行为间接训练推荐系统的成本。
- 推测：将显式偏好贯穿检索、排序与交付环节，可能有助于减少不同推荐入口之间的偏好理解差异。

## 来源摘要/节选

> Your algorithm is a suite of AI-powered tools that makes Facebook recommendations more transparent and steerable, with a single editable view of the interests that shape Feed and Reels.
>
> We’re sharing how Your algorithm turns people’s natural language preferences into responsive recommendations, and how LLMs are tailored to specific tasks within the system.
>
> Traditionally, the recommendation systems behind what people see on Facebook have learned from implicit engagement signals. While this allows them to scale well, it also means they adapt slowly and capture little nuance. But what if people could interact directly with the algorithms that rank and recommend what they see to instantly make their recommendations more personal and customized?
>
> Your algorithm is an end-to-end system that addresses the limitations of adaptability and nuance in recommendations. This new suite of AI-powered tools lets people on Facebook state, in their own words, what they want to see in their Feed and Reels. By tasking a collection of large language models (LLMs) with understanding, storing, and tracking people’s stated preferences along with their user behavior, we’ve created a recommendation system that responds to people’s preferences and adjusts the content they see.
>
> An Overview of the Your Algorithm System Architecture
>
> The Your algorithm page has three parts (Figure 1):
>
> At the top, a one-sentence Lately Summary that describes recent viewing activity.
>
> Below it are two lists:
>
> “Interested In,” prefilled with interests inferred from past activity.
>
> “Not Interested In,” capturing topics the user has explicitly marked as not interested, or has X-ed out or hidden on Facebook.
>
> People can use the interface to add interests (using natural language), move them between lists, or remove them. Every change applies responsively to both Feed and Reels, and will further update as the person gives feedback on individual posts.
>
> Figure 1: The Your algorithm page.
>
> Your algorithm system has several components that cover the full lifecycle of a preference, from inferring and validating it to applying it in ranking and delivery (Figure 2).
>
> Profile generation builds the initial interest profile.
>
> Preference management validates each change, enriches it with the signals ranking needs, and saves it to a single store that both Feed and Reels read, ensuring that the preferences shown on the page are the same ones used in ranking.
>
> Ranking applies the “Interested In” and “Not Interested In” lists throughout the funnel.
>
> Delivery optimization helps each change take effect more responsively.
>
> Figure 2: An overview of the Your algorithm system.
>
> From Preferences Into Recommendations
>
> Turning a stated preference into recommendations poses three distinct problems. An interest added to Interested In needs to deliver relevant content quickly, without crowding out everything else. An interest added to Not Interested In needs to hold reliably, even though topics are fuzzy and any single filter misses some matches. And both need to take effect responsively, even when the next recommendations were cached before the change.
>
> Your algorithm addresses each problem with dedicated logic across the recommendation funnel, from retrieval through reranking to the device (Figure 3).
>
> Interested In: Surfacing New Interests Without Flooding
>
> Each interest in Interested In drives four dedicated retrieval sources. Two find matching content directly (through search and through clusters of closely related topics), and two extend reach through the content graph and item-to-item similarity. Retrieving explicitly for each interest ensures enough relevant candidates for downstream ranking.
>
> This is important because, without it, content about a brand-new interest might never enter the ranking pipeline at all. Candidates that pass a relevance check, which compares the meaning of the interest with each candidate, receive a promotion in late-stage ranking so they can compete alongside other content. A control layer in reranking then determines where they appear.
>
> Responsiveness alone is not the goal. Our approach emphasizes balance over volume: A new interest should show up, not take over. The control layer spaces out recommendations for the same interest and caps each interest’s daily contribution. Retrieval also fetches candidates for only one interest per request, so every interest gets a turn. New interests receive extra weight for a limited period. After that, the recommendation system learns from how people engage with that content.
>
> Not Interested In: Layered Filtering at Every Stage
>
> Interests in Not Interested In are enforced at several stages based on different signals to achieve high precision and recall. During ranking, the same embedding-based comparison used in the relevance check removes candidates too close to an interest in Not Interested In, and demotion rules push down near matches. After ranking, the LLM reranker reviews the final list. On the device, cache invalidation, described below, removes matching candidates that are already queued for display.
>
> Not every entry in Not Interested In is about a topic. Quality-related requests, such as reducing AI-generated or sexually suggestive content, map to dedicated demotion signals rather than topic matching. When a request names a creator, that creator’s content is filtered out directly.
>
> Responsiveness Optimization
>
> Even with ranking tuned to respond to preferences, there is still room to improve how responsively a change reaches what people see. Content for a new preference is not picked up until the next fetch request, and content already cached on the device was ranked before the preference was set.
>
> We added two delivery mechanisms to close these gaps. When a new interest is added to Interested In, the system sends an extra fetch request outside the normal fetch cycle, called a supplementary tail load, to retrieve fresh recommendations so matching content appears quickly. When an interest is added to Not Interested In, cache invalidation handles candidates ranked before the change. The client obtains the new interest’s clusters and drops any cached content that matches them before it is displayed.
>
> Figure 3: Where Your algorithm preferences act in the content ranking funnel.
>
> LLMs Across the Preference Lifecycle: From Profile to Final Check
>
> LLMs play a role at several key points in a preference’s life in Your algorithm. They generate the initial profile that people see on a first visit, validate each change as it is made, and give the final recommendations a last check against interests in Not Interested In (Figure 2). Each use comes with its own constraints, including latency, serving capacity, and safety, and evaluating them requires a new approach as well.
>
> Profile generation provides the starting content for a first visit: the inferred interests and the Lately Summary. An LLM turns interest signals, which are refreshed regularly, into a set of inferred interests with clear, readable topic names. These are prefilled in the Interested In list and reflect past viewing across Facebook Feed and Reels. The LLM also writes the Lately Summary, a sentence that highlights ongoing interests. Together, they provide a recognizable starting point that is easy to review and correct.
>
> Every edit on the Your algorithm page passes through preference management. When an interest is added or moved, an LLM checks that the phrase is a coherent topic, detects duplicates, and maps it to a clean topic name. This step runs on a smaller model that is efficient to serve at scale. The validated interest is then enriched with the signals ranking needs, such as an embedding and search keywords, and saved to the shared preference store. The LLM is only one layer of validation. The system also has a dedicated component that performs integrity and safety checks.
>
> Once recommendations are ranked, LLM reranking provides a last check against interests in Not Interested In. The ranking funnel matches interests to candidates using embeddings, which are fast but coarse. To catch what they miss, a fine-tuned LLM reviews the ranked list and removes content it judges to be related to an interest recently added to Not Interested In. A key insight was that a small model fine-tuned to return only the items to remove was faster and more reliable than a general-purpose model judging each item individually.
>
> Evaluating these LLM calls required its own approach. Standard offline metrics cannot tell whether a Lately Summary is accurate or whether the reranker removed the right candidates, so a separate LLM acts as a judge, grading each call’s output against expected behavior. This provides an objective, repeatable way to compare prompts and models before launch.
>
> The Future of Your Algorithm
>
> Your algorithm creates a more transparent and personalized recommendation experience, informed by both behavior and stated intent. But there are important opportunities remaining, such as better interpreting ambiguous input and making recommendations respond even more precisely to each request. We are also exploring additional entry points so that preferences can be shaped from more places.
>
> Acknowledgments
>
> This work reflects critical contributions from a cross-functional v-team across Meta (in alphabetical order):
>
> Adi Gupta, Aryan Porwal, Bernabe Soto, Chao Yang, Chen Chen, Chen Kovacs, Chengxi Li, Chih-Wei Chang, Clare Yip, Cuong Nguyen, Dahni Ma, Daniel Thiyagu, Danny Kanoff, David Yuan, Devin Ding, Devon Pan, Eric Landgrebe, Feng Zhang, George Lu, Grace Yang, Hai-Son Dang, Haisen Hong, Hongyi Shi, Hongyi Wu, Howard Lu, Huijun Qian, Igor Vodov, Iordanis Fostiropoulos, Jakara Mato, Jasmine Neisser, Jason Liu, Jason Song, Jean-Pascal Billaud, Jeffrey Lin, Jeffrey Santelli, Jian Chen, Jianyu Wang, Jiaye Pan, Jinho Hwang, Joe Sena, Jordan Reich, Kanghua Wu, Khoi Pham, Kim Trang Leaf, Kris Katsanevas, Kuo-Feng Hsu, Kushal Adhvaryu, Liyu Wang, Manish Khettry, Matthew Miao, Mayoor Rai, Momo Jiao, Nakul Tirumalai, Patrick Boocock, Patrick Cullen, Qi Guo, Qichao Que, Queenie Li, Ratish Nair, Sanyogeeta Lawande, Satvik Eltepu, Sean Chen, Shijie Xie, Shuai Zhang, Shuoyan Yin, Smruthi Gowtham, Tsung-Yi Huang, Tyler Pell, Wanting Jiang, Wanyu Li, Weiwei Jiang, Xiangyu Xu, Xin Wang, Xinyang Feng, Yanchen Wang, Yibo Zhu, Yihao Li, Yihui Saw, Yinjie Huang, Yu-Wei Wu, Yuchen Shao, Yue Wang, Yue Zhang, Yuhan Yang, Yuqi Shen, Zhen Hang Jiang, Zhiyu Liu, Zhongwei Teng, Zijiang Yang, Zoe Zu
>
> We also thank the following leaders for their sponsorship and strong leadership support (in alphabetical order):
>
> Ashish Gandhe, Helen Kong, Hongjie Bai, Meng Wu, Yaping Zhang, Yisong Song, Zellux Wang, Zhe Wang
>
> The post Your Algorithm: Giving People More Ways to Personalize Facebook Recommendations appeared first on Engineering at Meta.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。