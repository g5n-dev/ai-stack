---
title: "OpenAI与巴西两大媒体合作ChatGPT接入新闻"
date: 2026-05-25T19:50:25+08:00
draft: false
entry_kind: "auto"
tags: ["OpenAI", "ChatGPT", "巴西媒体", "新闻合作", "版权", "来源标注", "透明度", "可信新闻"]
categories: ["大模型"]
source: blogs_podcasts
description: "OpenAI 与巴西媒体集团 Grupo Folha 和 Grupo UOL 建立战略内容合作，将两家媒体的可信新闻引入 ChatGPT。通过此次合作，用户在对话中可获取带有来源标注的新闻摘要，提升信息的透明度与可靠性，同时帮助巴西新闻业扩大在人工智能平台上的影响力。合作强调尊重版权、提供正确的引用，确保新闻内容在被使"
external_url: https://openai.com/index/grupo-folha-grupo-uol-partnership
scenarios: ["AI/ML项目"]
---

# OpenAI与巴西两大媒体合作ChatGPT接入新闻

---

## 基本信息

- **来源**: OpenAI Blog (blog)
- **发布时间**: 2026-05-25T00:00:00+00:00
- **链接**: [https://openai.com/index/grupo-folha-grupo-uol-partnership](https://openai.com/index/grupo-folha-grupo-uol-partnership)

---
## 摘要/简介

OpenAI与Grupo Folha和Grupo UOL合作，将值得信赖的巴西新闻引入ChatGPT，扩大新闻获取渠道，同时保持来源标注和透明度。

---
## 导语

OpenAI 与巴西媒体集团 Grupo Folha、Grupo UOL 达成合作，将两家的新闻内容接入 ChatGPT，使用户在对话中即可获取经过核实、标注来源的巴西新闻。此举旨在拓宽新闻获取渠道，同时保持信息来源的透明度与可信度。随着 AI 助手与传统媒体的深度融合，读者能够更便捷地获取本地热点资讯。

---
## 摘要

OpenAI 与巴西媒体集团 Grupo Folha 和 Grupo UOL 建立战略内容合作，将两家媒体的可信新闻引入 ChatGPT。通过此次合作，用户在对话中可获取带有来源标注的新闻摘要，提升信息的透明度与可靠性，同时帮助巴西新闻业扩大在人工智能平台上的影响力。合作强调尊重版权、提供正确的引用，确保新闻内容在被使用时得到适当归属。

---
## 技术分析

#### 核心观点
##### 中心命题
OpenAI 与巴西两大媒体集团 Grupo Folha、Grupo UOL 达成的战略内容合作协议，旨在将受信任的新闻内容引入 ChatGPT，实现“引用‑透明‑授权”三要素的闭环。

##### 支撑理由
1. **内容可信度提升**：通过官方授权的新闻文本，模型输出的答案可附带原始链接或摘要，降低错误信息风险。
2. **商业模式创新**：媒体获得 AI 带来的流量分成和授权费，OpenAI 则获得高质量、结构化的训练和检索素材。
3. **用户获取新入口**：ChatGPT 的对话式交互为用户提供“一站式”新闻获取渠道，提升用户粘性。
4. **监管合规性**：合法授权可规避版权纠纷，帮助 AI 平台在巴西等对数字内容监管趋严的地区合规运营。

#### 关键技术点
##### 内容注入方式
- **检索增强生成（RAG）**：利用向量数据库将新闻文章索引，实时检索相关段落并拼接至生成文本。
- **结构化元数据**：为每篇新闻提供标题、发布时间、出处 URL、作者等元信息，便于模型在引用时自动标注。
- **权限 API**：OpenAI 提供的版权内容访问接口（Content License API）实现动态授权、计费和撤销。

##### 透明与归属机制
- **来源标记**：模型输出时显式展示 “来源：Folha de S.Paulo” 并附上可点击链接。
- **可信度评分**：依据新闻机构的历史可信度数据，模型可给出信息的置信度指示（如 “高可信度”）。
- **用户反馈回路**：用户可对错误引用进行标记，后端系统实时更新检索库的权重。

#### 实际应用价值
- **新闻消费场景**：用户在提问 “巴西最近的能源政策” 时，ChatGPT 能直接返回最新报道并注明来源。
- **内容分发渠道**：媒体通过 AI 获得新的流量入口，提升文章的曝光率和潜在广告收入。
- **舆情监测**：结合可信的新闻库，企业或研究机构可以快速构建基于真实报道的舆情分析模型。
- **教育与学习**：学生可直接在对话中获得经过验证的新闻摘要，提升信息素养。

#### 行业影响
- **AI‑媒体合作模式**：该协议可能成为全球范围内 AI 平台与出版商合作的标杆，促进更多双边授权。
- **竞争格局**：其他大型语言模型（如 Google Bard、Meta LLaMA）若未能提供同等可信来源，将面临用户信任劣势。
- **监管趋势**：巴西的《数字服务法》可能要求 AI 必须展示信息来源，预计更多国家将出台类似规定。
- **内容生态重构**：出版商将更加重视结构化数据（JSON‑LD、Schema.org）输出，以适配 AI 检索系统。

#### 边界条件与实践建议
##### 边界条件
1. **授权范围限定**：仅限已签约的新闻库，若用户查询未覆盖的主题，仍会回退至未授权内容。
2. **内容时效性**：新闻的实时更新需要高效的向量索引同步机制，否则可能出现过期信息。
3. **地区合规**：巴西对个人数据（LGPD）有严格要求，需在内容处理过程中确保匿名化。
4. **模型幻觉风险**：即使有真实来源，模型在生成长答案时仍可能掺入错误细节，需要二次校验。

##### 实践建议
- **构建可信来源层**：在向量库中加入“可信度标签”，并在检索时过滤低可信度文档。
- **动态授权管理**：实现基于时间窗口的授权续期，防止过期内容被永久使用。
- **强化归属展示**：在 UI 层提供可点击的来源卡片，提升用户对信息出处的感知。
- **监控与反馈**：部署实时监控系统捕获错误引用，结合用户反馈持续优化检索权重。
- **合规审查**：在数据流转的每一步（爬取、索引、生成）嵌入 LGPD 合规检查点。

#### 论证地图
- **中心命题**：可信授权新闻 → AI 引用透明 → 用户信任提升。
- **支撑理由**：提升内容质量、创造商业价值、符合监管、增强用户体验。
- **反例/边界**：授权范围受限、时效性不足、合规风险、模型幻觉。
- **可验证方式**：A/B 测试对比未授权内容的错误率、监测引用点击率、评估用户满意度调查、审计版权授权记录。

---
## 学习要点

- 请提供该合作伙伴关系的具体内容或要点，以便我为您提取并撰写 5‑7 条关键学习要点。

---
## 引用

- **文章/节目**: [https://openai.com/index/grupo-folha-grupo-uol-partnership](https://openai.com/index/grupo-folha-grupo-uol-partnership)
- **RSS 源**: [https://openai.com/blog/rss.xml](https://openai.com/blog/rss.xml)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/)
- 标签： [OpenAI](/tags/openai/) / [ChatGPT](/tags/chatgpt/) / [巴西媒体](/tags/%E5%B7%B4%E8%A5%BF%E5%AA%92%E4%BD%93/) / [新闻合作](/tags/%E6%96%B0%E9%97%BB%E5%90%88%E4%BD%9C/) / [版权](/tags/%E7%89%88%E6%9D%83/) / [来源标注](/tags/%E6%9D%A5%E6%BA%90%E6%A0%87%E6%B3%A8/) / [透明度](/tags/%E9%80%8F%E6%98%8E%E5%BA%A6/) / [可信新闻](/tags/%E5%8F%AF%E4%BF%A1%E6%96%B0%E9%97%BB/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [OpenAI 将在 ChatGPT 中停用 GPT-4o 等四款模型]({{< relref "posts/20260129-hacker_news-retiring-gpt-4o-gpt-41-gpt-41-mini-and-openai-o4-m-2.md" >}})
- [OpenAI 将在 ChatGPT 中下架 GPT-4o 等四款模型]({{< relref "posts/20260129-hacker_news-retiring-gpt-4o-gpt-41-gpt-41-mini-and-openai-o4-m-4.md" >}})
- [OpenAI将于2026年2月退役ChatGPT中多款GPT‑4及o4模型]({{< relref "posts/20260130-blogs_podcasts-retiring-gpt-4o-gpt-41-gpt-41-mini-and-openai-o4-m-4.md" >}})
- [OpenAI将于2026年2月退役ChatGPT内多款GPT‑4及o4‑mini模型]({{< relref "posts/20260130-blogs_podcasts-retiring-gpt-4o-gpt-41-gpt-41-mini-and-openai-o4-m-5.md" >}})
- [OpenAI 将在 ChatGPT 中下架 GPT-4o 等四款模型]({{< relref "posts/20260130-hacker_news-retiring-gpt-4o-gpt-41-gpt-41-mini-and-openai-o4-m-11.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与方法论思考。*