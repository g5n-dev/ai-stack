---
title: 玩转 Linux 机器视觉：手把手带你搞定 Ubuntu 下海康工业相机 C++ SDK
date: 2026-06-17 23:45:46+08:00
draft: false
entry_kind: auto
tags:
- 掘金
categories: []
scenarios: []
source: juejin
description: 当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。
external_url: https://juejin.cn/post/7652201596648914996
aliases: []
content_mode: source_brief
publication_tier: C
source_capture_mode: excerpt
source_snapshot_sha256: sha256:7febc9dd8439a66646111dfda499095d1e7e6434a6a965de2567f64268f19cb0
extractor_version: source-contract-v1
discovery_method: article_html_excerpt
fetch_status: captured
source_completeness: partial
source_is_truncated: true
source_support: 1.0
source_title_chars_original: 44
captured_at: '2026-07-18T04:21:42.569238Z'
source_capture_sha256: sha256:c4c9d70594e7361dd1408a7a5bfb9b538a9e2db1bdfdd9509a6d914e6f8fca24
source_capture_chars_original: 5099
source_publication_excerpt_chars: 793
source_truncation_reason: historical_excerpt_only,historical_publication_excerpt_limit
---

## 基本信息

- **来源**: juejin
- **原始来源**: [https://juejin.cn/post/7652201596648914996](<https://juejin.cn/post/7652201596648914996>)

## 来源摘要/节选

公开展示已截断至最多 800 个字符；请访问原始来源查看完整上下文。

> 拒绝黑屏与掉帧！本文专为 Linux 环境下的机器视觉与 AI 算法工程师打造，一篇文章带你打通 Ubuntu 系统下海康工业相机 MVS 的安装部署、CMake 项目架构配置，并奉上一套稳定、完美对接 OpenCV 的生产级 C++ 封装源码。
> 在工业自动化、无人巡检、机械臂抓取以及各类 Embodied AI（具身智能）场景中，工业相机作为系统的“眼睛”，其取流的稳定性和超低延迟是后续所有 AI 推理（如 YOLO 目标检测、OCR 识别）的基石。
> 由于生产环境多采用
> Ubuntu
> 系统作为边缘计算设备的运行环境，如何在 Linux 下高效、稳定地进行海康工业相机 C++ SDK 的二次开发，成了很多开发者必须面对的课题。今天，我们就来彻底拆解它！
> Ubuntu 环境安装
> 海康机器人官网
> 提供了 Linux 版本的
> MVS \(Machine Vision Suite\)
> 安装包。下载完成后，通常是一个
> .zip
> 压缩包。
> 安装步骤
> 解压后能够拿到不同架构（如 x86\_64 或 aarch64）的
> tar.gz
> 包以及相应的
> deb
> 文件，可以通过
> dpkg
> 命令安装
> deb
> 包，也可以将
> tar.gz
> 解压后直接执行安装脚本：
> sudo
> chmod
> +x setup.sh
> sudo ./setup.sh
> 安装脚本会自动将驱动、动态库和调试工具部署到系统中。默认的安装路径为：
> /opt/MVS
> 在这个目录下，我们需要重点关注以下三个核心路径：
> /opt/MVS/include
> ：存放开发所需的全部头文件，核心是
> MvCameraControl.h
> 。
> /opt/MVS/lib/64
> ：存放 64 位系统的动态链接库（
> libMvCameraControl.so
> ）。
> /opt/MVS/bin
> ：存放 Linux 版的 MVS 客户端程序，用于图形化调试相机。…

## 来源说明

当前只保存了公开页面节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已做哈希绑定的来源证据，不包含基于旧正文或缺失原文的扩展推断。
