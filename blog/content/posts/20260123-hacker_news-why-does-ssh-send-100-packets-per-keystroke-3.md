---
title: "Why does SSH send 100 packets per keystroke?"
date: 2026-01-23T10:27:51+08:00
draft: false
tags: []
source: hacker_news
external_url: https://eieio.games/blog/ssh-sends-100-packets-per-keystroke/
---

## ➜ 故事信息

**标题**: Why does SSH send 100 packets per keystroke?

**作者**: eieio

**评分**: 287

**评论数**: 196

**链接**: [https://eieio.games/blog/ssh-sends-100-packets-per-keystroke/](https://eieio.games/blog/ssh-sends-100-packets-per-keystroke/)

## ➜ AI 总结

SSH 并非每次击键都发送 100 个数据包。这通常是以下原因导致的：

1.  **窗口大小更新**：终端频繁调整窗口大小时，会发送大量伪终端请求。
2.  **TCP 延迟与 Nagle 算法**：小数据包（如击键）与 TCP 确认信号（ACK）交互不良，导致数据积压和突发传输。
3.  **应用层设计**：SSH 协议将加密通道内的逻辑数据（如窗口变化）与实际数据分开处理，增加了额外流量。

这通常是网络协议栈或终端环境的配置问题，而非 SSH 本身的标准行为。

## ➜ AI 评论

这篇文章具有极高的**技术价值**，主要体现在以下三个方面：

1.  **深度与洞察力：** 文章从“一次击键触发100个数据包”这一反常现象入手，层层剥茧，深入到TCP协议栈的底层逻辑。它不仅解释了网络延迟与TCP窗口更新机制（如“ACK延迟”与“Nagle算法”的冲突）的相互作用，还揭示了“糊涂窗口综合症（SWS）”这一经典网络问题的具体表现，展现了深厚的技术功底。
2.  **实用性与排障思维：** 作者展示了如何使用`tcpdump`等工具进行网络抓包分析，将理论协议与实际数据流完美结合。对于后端开发、运维及网络工程师而言，这篇文章提供了极佳的实战案例，极具参考意义。
3.  **创新性：** 虽然讨论的是经典协议，但其从微观视角（单次击键）审视宏观性能瓶颈的切入点非常新颖，通过生动的实验打破了常规认知的盲区。

**总结：** 这是一篇兼具理论深度与实战指导意义的佳作，能帮助读者深刻理解网络行为背后的原理。