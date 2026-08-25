---
title: "【Flutter 性能踩坑小记】相册选个图卡了"
date: 2026-08-25T18:53:08+08:00
draft: false
entry_kind: "auto"
tags: ["掘金", "工程实践", "来源转写"]
categories: ["AI 工程"]
source: "juejin"
content_mode: "evidence_backed_rewrite"
publication_tier: "B"
source_capture_mode: "full_article"
source_snapshot_sha256: "sha256:757e294a07ec3717c0df2df9ea1049b3cf308d874bf2833448dffe87acc3d830"
source_payload_sha256: "sha256:811a48e764ff22acb829da3a073e612720ddf75b781f5236f80e8c9c32889b43"
source_published_at: 2026-08-25T09:59:34Z
timestamp_confidence: feed
extractor_version: "source-contract-v2"
discovery_method: "article_html"
source_completeness: "complete"
parent_snapshot_sha256: "sha256:3e1cc183a470726654aea0d57c04ba275f15a8399da461d09185388cc2515d2f"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 23
description: "核心结论 该问题根因并非图片解码耗时，而是 Dart 单线程事件循环被高频通知队列阻塞。WebSocket 未读数更新每秒触发多次全局 ，导致 UI 层的缩略图渲染通知被挤压到队列后方。实测场景中，Picker 返回后缩略图出现前的空档期达 17 秒，而同一时段未读数已跳动 10 次。"
external_url: https://juejin.cn/post/7677803387144388617
observation_id: obs_7aae3d4266a2e4aa14e76965b6b51c2b044669486225197a0759efd12ae2da44
revision_id: rev_898fde8382f9193bb96fe9d318e7b611e3bccc8e09e8396c66dc9eb185de356f
event_id: evt_9df8debcb1e69ffa5b1a470ccaefa70d1cd95e17767b39452970c2631a1dbf40
lineage_relation: original
parent_observation_id: null
first_seen_at: 2026-08-25T10:49:19.976553Z
last_seen_at: 2026-08-25T10:53:08Z
---

## 转写说明

> 本文基于已校验的公开原文进行结构化转写与事实梳理，非原文转载。
> 转写保留可核验的技术事实，并将工程建议与来源观点明确分开。

- **原作者**: 大龄秃头程序员
- **原始来源**: [https://juejin.cn/post/7677803387144388617](https://juejin.cn/post/7677803387144388617)
- **原文发布时间**: Tue, 25 Aug 2026 09:59:34 GMT

## 核心结论

该问题根因并非图片解码耗时，而是 Dart 单线程事件循环被高频通知队列阻塞。WebSocket 未读数更新每秒触发多次全局 `notifyListeners()`，导致 UI 层的缩略图渲染通知被挤压到队列后方。实测场景中，Picker 返回后缩略图出现前的空档期达 17 秒，而同一时段未读数已跳动 10 次。

次生问题包括：架构拆分时中介者遗漏部分监听注册、筛选型 Notifier 在 build 中重复创建导致监听器泄漏、iOS 模拟器忽略 `maxWidth` 参数且 Flutter 隐式下采样行为不可靠。

## 能力机制

**全链路埋点法**：沿四层架构在每个跨层边界设置 Entry/Exit 日志，通过统一前缀过滤实现快速定位。调用链从 UI 点击延伸至系统相册调用，再回到 UI 渲染，共覆盖 9 个节点。

**细粒度通知筛选**：实现专用 `ChangeNotifier` 监听目标字段（selectedImages、语音状态等），隔离与 UI 渲染无关的状态变化，避免 WebSocket 未读数等高频事件触发不必要的 rebuild。

**事件节流**：使用 100ms 窗口合并通知，在首帧立即通知保证及时性，窗口内累积变更补发一次保证最终一致性。

**显式图片下采样**：弃用 `Image.file` 的 `cacheWidth` 参数，改用 `ResizeImage` 强制指定解码尺寸，不依赖引擎隐式行为。

## 快速开始

**日志前缀约定**：在 Debug Console 使用 `Check-images-bug` 前缀过滤全链路日志。

**节流实现模板**：

```dart
Timer? _notifyThrottleTimer;
bool _pendingNotify = false;
static const _throttleDuration = Duration(milliseconds: 100);

void _throttledNotifyListeners() {
  if (_notifyThrottleTimer == null) {
    notifyListeners();
    _notifyThrottleTimer = Timer(_throttleDuration, () {
      _notifyThrottleTimer = null;
      if (_pendingNotify && !_disposed) {
        _pendingNotify = false;
        notifyListeners();
      }
    });
  } else {
    _pendingNotify = true;
  }
}
```

**显式下采样写法**：

```dart
Image(
  image: ResizeImage(
    FileImage(File(path)),
    width: 144,
    height: 144,
    allowUpscaling: false,
  ),
  fit: BoxFit.cover,
)
```

Picker 侧设置 `requestFullMetadata: false` 可跳过 EXIF 读取，在模拟器场景节省约 1 秒。

## 适用边界

该方案针对 Dart 单线程模型下的事件队列竞争问题，适用于 Flutter 应用中同时存在高频状态更新（如 WebSocket 推送）与 UI 敏感操作（如图片预览）的场景。

iOS 模拟器配合 HEIC 格式时，`pickMultiImage` 的 `maxWidth` 参数可能不生效，仍返回全尺寸原图。Flutter 3.x 在 `ImageCache` 命中后存在绕过 `instantiateImageCodec` 下采样分支的情况，此时 `cacheWidth` 参数不可靠。

中介者模式拆分类时，必须确保 `addListener` 与 `removeListener` 成对出现，否则会导致通知链路断裂或监听器泄漏。筛选型 Notifier 应作为 `State` 字段管理生命周期，避免在 build 方法中创建。

## 核验清单

架构拆分完成后，检查 `AiChatCoordinator` 的 `_setupCrossControllerListeners` 方法中各子控制器的监听注册数量是否与 `dispose` 中的 `removeListener` 调用数量相等。

检查 `InputBar` 相关 Notifier 是否作为 `State` 字段单例存在，而非每次 build 时新建。若存在泄漏，可观察到同一通知被回调次数递增。

验证 `SessionEventController` 或类似高频通知源是否已实现节流机制。原始每秒 8-12 次通知经节流后应控制在 10 次以内。

验证缩略图加载路径是否使用 `ResizeImage` 显式指定尺寸，而非依赖 `cacheWidth` 参数隐式下采样。解码耗时目标应低于 50ms。

Picker 返回后缩略图出现前的空档期应控制在毫秒级，体感无等待。端到端耗时应控制在 5 秒以内，其中系统相册选图和文件拷贝时间不可控。

## 来源与核验

- [原始文章](https://juejin.cn/post/7677803387144388617)
- 页面事实以原始来源及其引用的官方资料为准；版本、星标和模型能力会随时间变化。
- AI Stack 不公开抓取到的全文快照，只发布独立转写与来源入口。

---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [掘金](/tags/%E6%8E%98%E9%87%91/) / [工程实践](/tags/%E5%B7%A5%E7%A8%8B%E5%AE%9E%E8%B7%B5/) / [来源转写](/tags/%E6%9D%A5%E6%BA%90%E8%BD%AC%E5%86%99/)

### 相关文章

- [6.结构化输出](/posts/20260718-juejin-6%E7%BB%93%E6%9E%84%E5%8C%96%E8%BE%93%E5%87%BA-0-80d50ad8af/)
- [GitHub Copilot for JetBrains 架构拆解：Provider / Endpoint / Skills / Sandbox / Polic](/posts/20260718-juejin-github-copilot-for-jetbrains-%E6%9E%B6%E6%9E%84%E6%8B%86%E8%A7%A3provider-endpoint-0-2a917f4cdc/)
- [从 Token 到 RAG：我这一周搭起的大模型基础认知地图](/posts/20260718-juejin-%E4%BB%8E-token-%E5%88%B0-rag%E6%88%91%E8%BF%99%E4%B8%80%E5%91%A8%E6%90%AD%E8%B5%B7%E7%9A%84%E5%A4%A7%E6%A8%A1%E5%9E%8B%E5%9F%BA%E7%A1%80%E8%AE%A4%E7%9F%A5%E5%9C%B0%E5%9B%BE-0-cd9514ced7/)
- [从零到一手撸 Agent 系列 — 第 1 篇：一个 Coding Agent 是什么？](/posts/20260718-juejin-%E4%BB%8E%E9%9B%B6%E5%88%B0%E4%B8%80%E6%89%8B%E6%92%B8-agent-%E7%B3%BB%E5%88%97-%E7%AC%AC-1-%E7%AF%87%E4%B8%80%E4%B8%AA-coding-agent-%E6%98%AF%E4%BB%80%E4%B9%88-0-b0628f7a64/)
- [从BFF到SSE：我在Vue项目里藏了个“AI翻译官”](/posts/20260719-juejin-%E4%BB%8Ebff%E5%88%B0sse%E6%88%91%E5%9C%A8vue%E9%A1%B9%E7%9B%AE%E9%87%8C%E8%97%8F%E4%BA%86%E4%B8%AAai%E7%BF%BB%E8%AF%91%E5%AE%98-0-9ec70466e8/)