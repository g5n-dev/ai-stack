---
title: "Computational tools for society’s most complex challenges"
date: 2026-10-03T04:47:36+08:00
draft: false
entry_kind: "auto"
tags: ["机器学习", "Profile", "Faculty", "Transportation", "Logistics", "Autonomous vehicles", "Traffic management", "Robotics"]
categories: []
source: "blogs_podcasts"
content_mode: "interpreted_brief"
publication_tier: "C+"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:0620b15fa4e66b972f3e451b1349942cd0e4ae515bd5b73071d5558953821887"
source_payload_sha256: "sha256:f3f263fed66ec574aba3b04e5d6bf88e0d6b5230ace13485de2faa59a6999703"
observation_id: obs_bebca6424b0efee5984cc8767b7bb73b56d347a483516fbb5ca0dd84cef87475
event_id: evt_4aadf4aac8dce0967c36ac49f8d2c1f04681a33a73f108aaea83fdf37e48e741
revision_id: rev_22c0b97b3f53d2f6f04c59ae2ffc2fe3ab48571c836600402e7417daf9f2cb67
source_published_at: 2026-10-02T19:30:00Z
first_seen_at: 2026-10-02T20:58:53Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 57
interpretation_sha256: "sha256:38f8d414068cde606ec840a3dfdf12356052a3f75016de0cb5deee404b08981b"
description: "这是一篇关于 MIT 副教授 Cathy Wu 的访谈/博客，讲述她如何借助机器学习与强化学习改进交通系统的研究路径与最新突破。"
external_url: https://news.mit.edu/2026/computational-tools-for-societys-most-complex-challenges-cathy-wu-1002
parent_observation_id: null
last_seen_at: 2026-10-03T00:00:00Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://news.mit.edu/2026/computational-tools-for-societys-most-complex-challenges-cathy-wu-1002](https://news.mit.edu/2026/computational-tools-for-societys-most-complex-challenges-cathy-wu-1002)
- **发布域名**: news.mit.edu

## 要点解读

### 这是什么
这是一篇关于 MIT 副教授 Cathy Wu 的访谈/博客，讲述她如何借助机器学习与强化学习改进交通系统的研究路径与最新突破。

### 用在哪里
适合交通规划人员、城市管理者、AI/机器学习研究者，以及关注可持续交通与政策制定的学生与从业者参考。

### 可以推断的
推测：该方法若在大规模城市网络中验证，或能推广至能源调度、物流等其他复杂系统工程。  
推测：通过挑选能够顺利学习的子问题进行训练，可提升强化学习在实际场景中的成功率。

## 来源摘要/节选

> As far back as she can remember, Cathy Wu ’12, MNG ’13 wanted to find ways to solve problems to improve people’s lives. Her parents were Taiwanese immigrants, and her father had a long commute to his job, which took him away from the family. On a tight budget, the rest of the family often stayed home on a street that was too busy for playing outdoors. Wu and her siblings ended up playing a lot of computer games.
>
> Wu says her desire to make the world a better place, her dad’s daily battle against traffic, and the games she played, like “SimCity,” were the seeds of her motivation to design safe, efficient transportation systems.
>
> Wu is an associate professor in the MIT Department of Civil and Environmental Engineering (CEE) and the Institute for Data, Systems, and Society (IDSS), and a principal investigator in the Laboratory for Information and Decision Systems. Her research focuses on using machine learning and reinforcement learning (RL) to advance reliable strategies for improving a range of complex systems, including transportation.
>
> “Designing transportation systems consists of modeling and analyzing dozens, if not hundreds or thousands, of variants, which means that an evidence-driven approach to designing those systems is simply not within reach of today’s tools,” Wu says. “This is the role that RL plays. If successful, it would free transportation researchers and enable their practitioner partners to design the systems they want.”
>
> Wu credits her older sister with instilling in her the desire to improve people’s lives, and Wu’s interest in transportation fits neatly into that ideal.
>
> “I like transportation because it connects everyone. We all use it, we all experience it, we all have issues with it. So, at some level, we’re all interested in the system being better,” she says.
>
> Wu got interested in applying artificial intelligence to transportation while earning her undergraduate degree at MIT, after attending a lecture on autonomous vehicles by the late professor Seth Teller. The lecture, which Teller gave during an Independent Activities Period robotics competition (that Wu actually won), was the event that honed her particular approach to transportation research, Wu says. She began working with Teller, and when he stopped concentrating on autonomous vehicles, he encouraged Wu to transfer to Professor Daniela Rus, who had done research on robotaxis.
>
> “I’m very grateful to the people who helped me explore those interests and helped me become the person I am now,” she says, specifically naming Teller, Rus, and “my friends at Dropbox,” who invited her to do a second internship focused on transportation issues.
>
> After her master’s degree at MIT, Wu went on to earn her PhD at the University of California at Berkeley. During that time, she observed that transportation researchers were spending years developing optimization methods to model and analyze a single new variant of a system. Her approach as a computer scientist working to develop RL and optimization methodologies to address transportation challenges held the promise of exponentially improved efficiency.
>
> In 2018, Wu’s last year of her PhD at UC Berkeley, she successfully applied RL to a traffic problem: automatically analyzing the potential traffic flow impact of autonomous vehicles in a range of different traffic networks. The research went viral.
>
> While this could have been a “the rest is history” moment for Wu, RL turned out to be a flighty friend. Wu worked on RL theory in a postdoc at Microsoft and came back to MIT as faculty drawn, she says, by the sustainability focus of CEE, and IDSS’s emphasis on infusing data science into other disciplines.
>
> Yet over the next two years, Wu’s further attempts to apply RL to traffic problems failed.
>
> “That was stressful,” Wu says, “it was unclear whether the problem was me (the advisor), my students, the traffic domain, or RL itself.”
>
> Still, the earlier research was a proof-of-concept demonstration that RL could be applied to transportation systems.
>
> And in 2022, she and her students identified that RL algorithms are so sensitive that an algorithm that works on one problem may not on even a closely related one. A key result, which Wu says she is proudest of “because it was like the light at the end of a long tunnel of negative results,” came in 2023. She and her team of researchers devised a way to work around the sensitivity of RL. The team found that while RL may not train well on 90 percent of a group of problems, it can train quite well on 10 percent. And by training RL models on those problems that solve and generalize well, the resultant models collectively perform well on a set of related problems, even those that would not have been solved through direct training. The researchers designed an algorithm to determine which problems to use RL to train, and that algorithm improved training efficiency by up to 30 times, meaning that what would normally have required 100 training models may only require three models.
>
> “This work gave me back the confidence that reinforcement learning can play an important role in solving hard optimization problems, including in transportation,” Wu says. “Now, a good chunk of my group works on the topic of contextual RL, which is the setting where RL seeks to solve a space of related problems.”
>
> Wu’s more recent research applies RL to solve a hard transportation optimization problem with important policy implications: the work shows that eco-driving measures in which vehicle speeds are intelligently controlled to reduce excessive stopping and starting could reduce vehicle emissions by between 11 and 22 percent. The system provides evidence that policies instituting such measures could significantly improve system efficiency, and is “a demonstration that RL can be used to inform transportation policy on problems of practical importance,” Wu says.
>
> “I am a big fan of evidence-based policy and believe it’s the basis for a thriving democratic society, yet our societal systems are so complex,” Wu says. “People can bicker forever about what’s better or worse, but I do believe that there are questions we bicker about that can be analyzed systematically using data and have objective answers. A large part of the reason I am in academia is to better understand how technology can support democratic societal decision-making.”
>
> Wu says that much of the work she and her team have done over the last several years has produced algorithms “to streamline the development of solvers for hard optimization problems, whether they are related to transportation or to other systems, such as logistics, supply chains, manufacturing, and resource allocation.
>
> “This alludes to my preferred style of work,” Wu says, “which is called use-inspired basic research,” explaining that such research addresses a practical problem, developing fundamental knowledge that often translates to other practical problems. Her students start by probing consequential problems ranging from safety to congestion to accessibility, identifying where existing methods fall short, and allowing the problems themselves to shape the direction of the research.
>
> At the same time, Wu’s desire to help others on a more personal level plays out in her teaching.
>
> “I love working with students, both in the classroom and research mentoring,” she says. “It makes my day when I am able to teach someone something — when I see that light bulb go on in a student.”
>
> In addition to earning academic honors, including a 2023 National Science Foundation Faculty Early Career Development Award, Wu has also been formally celebrated for her teaching and mentoring, including with the Ole Madsen Mentoring Award in 2025.
>
> What does she tell students confronting extremely complicated problems?
>
> “Be patient. Start small. Societal impact is a lifelong endeavor, not something to be accomplished in a few years,” Wu says. “It will take years to really understand what’s going on and where the real problems are. In the meantime, try to be helpful. Be curious. Ask many questions.”

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 「要点解读」由 AI Stack 依据上方已保存内容整理，不代表来源的完整表述；标注「推测：」的判断来自编辑，不是来源陈述。