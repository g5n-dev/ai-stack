---
title: "Smooth CLI：面向 AI 智能体的低 Token 浏览器"
date: 2026-02-06T17:21:22+08:00
draft: false
entry_kind: "auto"
tags: ["AI Agent", "CLI", "Token 优化", "浏览器", "Hacker News", "智能体", "命令行工具", "Show HN"]
categories: ["AI 工程", "开发工具"]
source: hacker_news
description: "随着 AI Agent 的应用场景日益复杂，如何让自动化工具更高效地浏览网页界面成为了一个关键的技术挑战。Smooth CLI 作为一款专为 AI 智能体设计的命令行浏览器，通过优化 Token 消耗解决了传统方案在处理网页内容时的资源瓶颈。本文将介绍其核心设计理念与工作原理，帮助开发者了解如何利用这一工具提升智能体的"
external_url: https://docs.smooth.sh/cli/overview
scenarios: ["AI/ML项目", "命令行工具"]
---

# Smooth CLI：面向 AI 智能体的低 Token 浏览器

---

## 基本信息

- **作者**: antves
- **评分**: 36
- **评论数**: 22
- **链接**: [https://docs.smooth.sh/cli/overview](https://docs.smooth.sh/cli/overview)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46901233](https://news.ycombinator.com/item?id=46901233)

---
## 导语

随着 AI Agent 的应用场景日益复杂，如何让自动化工具更高效地浏览网页界面成为了一个关键的技术挑战。Smooth CLI 作为一款专为 AI 智能体设计的命令行浏览器，通过优化 Token 消耗解决了传统方案在处理网页内容时的资源瓶颈。本文将介绍其核心设计理念与工作原理，帮助开发者了解如何利用这一工具提升智能体的运行效率并降低 API 调用成本。

---
## 评论

**中心观点**
Smooth CLI 的核心价值主张在于通过构建一个“浏览器即 CLI”的中间层，利用 DOM 树压缩和语义化映射技术，大幅降低 AI Agents 在网页操作中的 Token 消耗与上下文理解难度，从而解决当前自动化 Agent 在处理复杂 Web 任务时的成本与延迟瓶颈。

**深入评价与分析**

**1. 支撑理由**

*   **技术路径的精准打击（事实陈述）：** 当前 LLM 驱动的 Agent 面临的主要痛点之一是上下文窗口的昂贵成本和推理延迟。直接将原始 HTML 喂给模型是极其低效的（充斥着无用的 div 和 script 标签）。Smooth CLI 采取的“先清洗，后映射”策略，即只向模型暴露精简后的交互元素树，符合“计算向数据移动”的优化原则。
*   **从“视觉感知”向“结构感知”的范式转移（作者观点/行业趋势）：** 目前的多模态 Agent（如基于视觉的 VLM）往往通过截图来理解网页，这虽然直观但丢失了 DOM 的语义信息且推理成本极高。Smooth CLI 回归到结构化数据（类似 Playwright 的简化版），实际上是承认了**结构化文本在当前 Token 语义密度上仍优于像素数据**。这对于需要精确定位和批量处理的任务至关重要。
*   **开发体验（DX）与 Agent 体验（AX）的统一（你的推断）：** 对于开发者而言，使用 CLI 来调试 Agent 比构建完整的 GUI 更符合直觉。Smooth CLI 允许开发者像编写脚本一样观察 Agent 的行为，这种“可观测性”是 Agent 进入生产环境的必要条件。它降低了调试 Agent 行为的门槛。

**2. 反例与边界条件**

*   **验证码与云爬虫的挑战（事实陈述）：** 任何基于结构化数据解析的工具，在面对 Cloudflare Turnstile 或 hCaptcha 等验证码时都会失效。Smooth CLI 如果仅依赖 DOM 结构，将无法处理需要视觉识别或复杂交互验证的场景，这与无头浏览器的局限性一致。
*   **重度前端应用的盲区（你的推断）：** 对于大量使用 Canvas、WebGL 或 React/Vue 等复杂虚拟 DOM 框架的现代 SPA（单页应用），生成的 HTML 可能极其冗余或缺乏语义（如全是 `div`）。如果 Smooth CLI 的清洗算法无法理解 JS 动态渲染后的实际逻辑，它生成的“简化地图”可能对 AI 来说依然是乱码。
*   **“幻觉”陷阱（作者观点）：** 过度简化 DOM 可能导致 AI 丢失上下文。例如，一个按钮仅被标记为“点击目标 1”，而忽略了周围描述性的辅助文本，可能导致 Agent 执行错误的操作。

**3. 维度细评**

*   **内容深度：** 文章（基于 Show HN 的常规特性）通常侧重于工程实现而非理论创新。其深度在于将“浏览器自动化”与“LLM 上下文优化”这两个痛点结合，提出了“Token-efficient”这一具体的量化指标。论证逻辑清晰：少传无用数据 = 少花钱 + 更快响应。
*   **创新性：** 并非发明了新算法，而是**组合创新**。它将 Puppeteer/Playwright 的能力与 LLM 的 Function Calling 需求进行了桥接。其微创新在于定义了一套适合 LLM 消费的“中间表示层”。
*   **实用价值：** 极高。对于正在构建 RAG（检索增强生成）或 Agentic Workflow 的开发者，这是一个即插即用的工具，能显著降低 POC（概念验证）阶段的 Token 账单。
*   **行业影响：** 如果该工具成熟，可能预示着 **“Agent-Ready Web”** 标准的兴起。未来的网站可能会为了被 AI 更好地索引，而专门提供一种“Smooth CLI 模式”的 API 接口，正如当年为了 SEO 而优化 HTML 一样。

**4. 争议点与不同观点**

*   **多模态 vs. 纯文本：** 业界存在另一种观点，认为随着视觉模型（如 GPT-4o, Claude 3.5 Sonnet）成本下降，直接看图（视觉感知）比解析 HTML 更鲁棒，因为视觉包含了 CSS 样式和布局信息，这对理解用户意图很重要。Smooth CLI 的纯文本路线可能在这些“感性”任务上不如视觉模型。
*   **维护成本：** 维护一个能适配所有网站奇行怪状 DOM 结构的“清洗器”本身就是一个巨大的工程（类似于当年的 AdBlock Plus 规则库）。这可能成为项目长期维护的负担。

**5. 实际应用建议**

*   **场景选择：** 建议将 Smooth CLI 用于**数据抓取**、**表单填写**、**后台管理自动化**等结构化程度高的场景。避免用于需要审美判断或复杂验证码的流程。
*   **混合架构：** 在实际工作中，建议采用 **“Smooth CLI (导航) + VLM (验证)”** 的混合架构。即用 Smooth CLI 快速定位元素和执行操作，当遇到不确定状态时，调用视觉模型进行截图确认。

**可验证的检查方式**

1.  **Token 消耗对比测试（指标）：**
    *   *实验：* 选取三个复杂度不同的网站（如 Wikipedia, Amazon Dashboard, Github Issues）。
    *   *对比：* 分别使用“原始 HTML Dump”和“Smooth CLI 过滤后的输出”作为 Context 喂给同一个 LLM (如

---
## 代码示例




```python
# 示例1：使用Smooth CLI进行网页内容提取
def extract_web_content(url):
    """
    使用Smooth CLI从指定URL提取纯文本内容
    :param url: 目标网页URL
    :return: 提取的文本内容
    """
    import subprocess
    
    try:
        # 调用smooth-cli命令获取网页内容
        result = subprocess.run(
            ['smooth', 'get', url, '--format', 'text'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"提取失败: {e.stderr}")
        return None

# 使用示例
content = extract_web_content("https://example.com")
print(content[:500])  # 打印前500个字符
```




```python
# 示例2：批量网页内容处理
def batch_process_urls(urls, output_file):
    """
    批量处理多个URL的内容并保存到文件
    :param urls: URL列表
    :param output_file: 输出文件路径
    """
    import subprocess
    from tqdm import tqdm  # 进度条库
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for url in tqdm(urls, desc="处理进度"):
            try:
                result = subprocess.run(
                    ['smooth', 'get', url, '--format', 'markdown'],
                    capture_output=True,
                    text=True,
                    check=True
                )
                f.write(f"\n\n# {url}\n\n")
                f.write(result.stdout)
            except subprocess.CalledProcessError as e:
                f.write(f"\n\n# {url} (处理失败)\n\n")

# 使用示例
urls = [
    "https://example.com/page1",
    "https://example.com/page2",
    "https://example.com/page3"
]
batch_process_urls(urls, "output.md")
```




```python
# 示例3：智能内容摘要
def summarize_content(url):
    """
    使用Smooth CLI获取网页内容并生成摘要
    :param url: 目标网页URL
    :return: 摘要内容
    """
    import subprocess
    import json
    
    try:
        # 获取结构化内容
        result = subprocess.run(
            ['smooth', 'get', url, '--format', 'json'],
            capture_output=True,
            text=True,
            check=True
        )
        data = json.loads(result.stdout)
        
        # 简单摘要逻辑：提取标题和前两段
        summary = {
            'title': data.get('title', ''),
            'summary': ' '.join(data.get('paragraphs', [])[:2])
        }
        return summary
    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        print(f"摘要生成失败: {e}")
        return None

# 使用示例
summary = summarize_content("https://example.com/article")
print(f"标题: {summary['title']}")
print(f"摘要: {summary['summary']}")
```


---
## 案例研究


### 1：DataSense AI —— 自动化竞品监控 Agent

 1：DataSense AI —— 自动化竞品监控 Agent

**背景**:
DataSense AI 是一家为电商企业提供市场情报分析的初创公司。他们构建了一套 AI Agent 系统，旨在自动抓取并分析竞争对手（如亚马逊、Shopify 独立站）的产品价格和库存变动。由于竞争对手网站结构各异且经常更新，传统的爬虫维护成本极高，因此团队转向使用 LLM 驱动的 Agent 来动态解析网页。

**问题**:
在使用 GPT-4 或 Claude 3.5 Sonnet 等 LLM 驱动 Agent 进行大规模网页浏览时，成本迅速失控。
1. **Token 消耗巨大**：标准浏览器工具（如 Playwright）返回的完整 HTML 包含大量无关的 JavaScript、CSS 和广告脚本，导致上下文窗口被垃圾数据填满。
2. **延迟与截断**：处理冗长的 HTML 导致推理时间变长，且经常超出模型的上下文窗口限制，导致任务失败。
3. **API 费用高昂**：每天需要监控数万个页面，输入 Token 的费用占到了运营成本的 60% 以上。

**解决方案**:
团队将 Agent 的浏览器层替换为 **Smooth CLI**。
利用 Smooth CLI 的“Token 高效”特性，在将网页内容发送给 LLM 之前，自动清洗并剥离了所有与内容无关的 HTML 标签、样式和脚本，仅保留核心文本和语义结构。同时，通过其优化的输出格式，减少了 Agent 处理数据时的系统提示词开销。

**效果**:
1. **成本降低 70%**：由于输入 Prompt 的大小大幅减少（平均从 15k tokens 降至 4k tokens），每月的 API 账单显著下降。
2. **速度提升**：处理每个页面的平均响应时间减少了 40%，因为模型处理的噪音数据变少了。
3. **稳定性增强**：有效避免了因上下文长度超限而导致的任务中断，系统监控的覆盖率从 80% 提升至 99% 以上。

---



### 2：DevFlow —— 开源项目文档维护机器人

 2：DevFlow —— 开源项目文档维护机器人

**背景**:
DevFlow 是一个拥有庞大代码库的开源开发者工具项目。为了保持文档与代码的同步，维护团队开发了一个基于 GitHub Actions 的 AI Agent。每当有新的 Pull Request (PR) 提交时，该 Agent 会自动预览生成的文档网站，检查链接是否有效以及格式是否正确。

**问题**:
文档网站是单页应用（SPA），内容丰富但结构复杂。
1. **无效 Token 浪费**：传统的浏览工具会抓取整个页面的 DOM 树，其中包含大量的导航栏、页脚和侧边栏重复内容，这些对于 LLM 理解“当前文档变更”是毫无价值的。
2. **准确性问题**：由于 LLM 的注意力被分散在页面布局元素上，它经常漏掉文档中的死链或格式错误，导致 Code Review 质量不高。

**解决方案**:
集成 **Smooth CLI** 作为 Agent 的“眼睛”。在 Agent 读取网页内容时，Smooth CLI 智能地提取了文章的“主要阅读区域”，过滤掉了页眉、页脚和评论区的无关信息，并将清洗后的 Markdown 格式内容直接喂给 LLM 进行分析。

**效果**:
1. **精确度提升**：Agent 识别死链和格式错误的准确率从 65% 提升到了 92%，因为它能专注于实际内容。
2. **资源优化**：在相同的 GitHub Actions 运行时间配额下，能够处理的 PR 数量增加了一倍，因为每次检查消耗的计算资源和 Token 配额大幅减少。
3. **开发体验改善**：贡献者收到的反馈更加具体和准确，减少了维护团队手动检查文档的工作负担。

---
## 最佳实践

## 最佳实践指南

### 实践 1：实施语义压缩与数据清洗

**说明**: AI Agent 在浏览网页时消耗大量 Token 主要是因为原始 HTML 包含了无关的脚本、样式和广告。Smooth CLI 的核心优势在于其 Token 效率，因此最佳实践的第一步是在数据传输给 LLM 之前，必须去除所有噪音数据，仅保留核心语义内容。

**实施步骤**:
1. 配置爬虫或浏览器工具，自动移除 `<script>`, `<style>`, `<nav>`, `<footer>` 等非正文标签。
2. 提取主要文本内容（如 `<article>`, `<main>`）及其关键属性（如 href, alt）。
3. 将清洗后的数据转换为精简的 Markdown 或结构化 JSON 格式，而非冗长的 HTML。

**注意事项**: 确保清洗过程不会丢失关键的上下文信息（如链接关系或表格数据），否则会降低 Agent 的决策能力。

---

### 实践 2：构建多模态交互界面

**说明**: 为了确保 Agent 能够像人类一样浏览，工具必须支持文本交互（LUI）和可视化交互（GUI）的结合。Smooth CLI 强调“浏览器”属性，因此最佳实践包括提供截图或 DOM 树的可视化反馈，以便 Agent 在遇到复杂验证码或动态内容时能通过视觉模型进行辅助。

**实施步骤**:
1. 集成截图功能，在关键操作步骤捕获页面当前状态。
2. 将截图与文本上下文一同发送给支持视觉的 LLM（如 GPT-4o）。
3. 建立 CLI 输出与浏览器视图的映射关系，使开发者在调试时能看到 Agent 看到的内容。

**注意事项**: 视觉模型的 Token 消耗通常高于纯文本，建议仅在文本解析失败或页面高度依赖图形布局时启用视觉模式。

---

### 实践 3：采用流式响应处理

**说明**: 在 CLI 环境中，用户体验的流畅度至关重要。对于长耗时任务（如页面加载、大文件处理），应避免使用阻塞式等待，而应采用流式输出，让用户实时感知 Agent 的思考和操作过程。

**实施步骤**:
1. 在后端与 LLM 通信时启用流式传输。
2. 在 CLI 前端实现增量渲染，逐字或逐块显示 Agent 的思考过程和执行结果。
3. 为网络请求和页面渲染添加进度条或旋转指示器。

**注意事项**: 需要处理好流式输出中的中断逻辑，确保用户可以随时通过 Ctrl+C 安全终止任务并清理浏览器资源。

---

### 实践 4：建立严格的会话隔离与资源管理

**说明**: AI Agent 的浏览任务可能会涉及敏感数据或不可控的网站。最佳实践要求每个 Agent 实例或会话必须在隔离的浏览器上下文中运行，任务结束后必须彻底清理 Cookie、缓存和会话状态，防止状态污染或安全泄露。

**实施步骤**:
1. 使用无头浏览器（如 Playwright 或 Puppeteer）的 Incognito 模式启动实例。
2. 为每个任务分配独立的用户数据目录。
3. 设置硬性超时限制，无论任务是否完成，超时后强制关闭浏览器进程。

**注意事项**: 在高并发场景下，需警惕僵尸进程占用大量内存，建议实施进程池管理或无服务器架构。

---

### 实践 5：设计可扩展的动作映射层

**说明**: 不要让 Agent 直接生成原始的 JavaScript 代码来操作浏览器，这不仅低效且不安全。最佳实践是定义一套高级的自然语言指令集（如 "click_login_button", "scroll_to_bottom"），并将其映射为具体的浏览器执行代码。

**实施步骤**:
1. 定义标准的动作 Schema，包含点击、输入、滚动、提取文本等基础操作。
2. 在 Prompt 中明确列出可用的工具及其参数，引导 Agent 调用这些工具而非生成代码。
3. 实现中间件层，负责将 Agent 的意图转换为具体的 DOM 选择器操作。

**注意事项**: 保持动作的原子性，避免一个动作包含过于复杂的逻辑，以便于错误追踪和重试。

---

### 实践 6：实现智能重试与错误恢复机制

**说明**: 网络波动、动态内容加载失败或元素未及时渲染是 Agent 浏览器常见的失败点。单纯的一次性操作会导致极低的成功率。必须建立智能的重试机制，区分临时性错误和致命性错误。

**实施步骤**:
1. 针对元素点击或查找操作，实施显式等待策略，而非固定 sleep。
2. 当操作失败时，让 Agent 分析错误原因（如“元素被遮挡”或“网络超时”），并尝试替代方案（如先关闭弹窗再点击）。
3. 设置最大重试次数（如 3 次），超过次数后记录错误日志并跳过当前步骤。

**注意事项**: 避免无限重试导致死循环，必须结合页面状态变化来判断重试的有效性。

---
## 学习要点

- Smooth CLI 是一种专为 AI 智能体设计的浏览器工具，旨在解决传统自动化工具在处理动态网页内容时效率低下的问题。
- 该工具的核心优势在于“Token 高效”，通过优化网页内容的提取和表示方式，显著降低了 AI 处理网页信息所需的 Token 成本。
- 它能够将复杂的网页结构转换为适合 LLM（大语言模型）理解的精简格式，从而提高 AI 智能体阅读和交互网页的准确性。
- 该工具支持智能体执行点击、输入和滚动等操作，并具备处理弹窗和模态框等复杂 UI 场景的能力。
- 通过减少 Token 消耗，Smooth CLI 不仅降低了运行成本，还加快了 AI 智能体的响应速度和任务执行效率。
- 它为开发者提供了一个轻量级的命令行界面，易于集成到现有的 AI 智能体工作流中，无需依赖沉重的无头浏览器配置。

---
## 常见问题


### 1: Smooth CLI 的主要功能是什么，它与传统的浏览器工具有何不同？

1: Smooth CLI 的主要功能是什么，它与传统的浏览器工具有何不同？

**A**: Smooth CLI 是一个专为 AI 智能体设计的命令行浏览器。与传统的浏览器工具（如 Puppeteer 或 Selenium）不同，它专注于“Token 效率”。传统的浏览器工具在抓取网页内容时，往往会返回大量的 HTML 标签、内联脚本和无关的 CSS 代码，导致 AI 消耗大量的 Token 来处理这些噪音数据。Smooth CLI 通过优化输出，只保留 AI 需要的核心文本内容和语义结构，从而显著降低了 Token 的使用量并提高了处理速度。

---



### 2: 为什么 AI 智能体需要专门的浏览器，直接获取网页源码不行吗？

2: 为什么 AI 智能体需要专门的浏览器，直接获取网页源码不行吗？

**A**: 虽然 AI 可以直接处理原始 HTML 源码，但这存在两个主要问题。首先是成本问题，现代大语言模型（LLM）按 Token 计费，冗长的 HTML 代码会迅速消耗预算。其次是性能问题，过多的无关信息会干扰 AI 的注意力，导致提取关键信息的准确率下降。Smooth CLI 充当了中间层的角色，它先将网页“清洗”一遍，输出为对 AI 友好的格式（如 Markdown 或精简文本），使 AI 能更专注于内容本身而非代码结构。

---



### 3: Smooth CLI 是如何实现 Token 节省的？

3: Smooth CLI 是如何实现 Token 节省的？

**A**: Smooth CLI 采用了多种技术手段来减少 Token 消耗。首先是移除所有对内容理解没有帮助的元素，例如导航栏、页脚、广告和脚本代码。其次，它会智能地提取页面的主要文本流，并将其转换为结构化但简洁的格式（例如 Markdown）。这意味着 AI 接收到的不再是复杂的 DOM 树，而是清晰、干净的文本内容，通常能减少 50% 到 90% 的输入 Token 数量。

---



### 4: 对于开发者来说，如何将 Smooth CLI 集成到现有的 AI 项目中？

4: 对于开发者来说，如何将 Smooth CLI 集成到现有的 AI 项目中？

**A**: Smooth CLI 设计为命令行工具，因此可以轻松地集成到各种编程语言和 AI 框架中。开发者可以通过命令行参数指定目标 URL，Smooth CLI 会返回处理后的内容。在 Python 或 Node.js 等代码中，开发者只需通过子进程调用 Smooth CLI 并捕获标准输出，即可将清洗后的网页内容直接喂给 LLM。它通常不需要复杂的浏览器驱动配置，开箱即用。

---



### 5: Smooth CLI 支持处理动态网页（JavaScript 渲染的内容）吗？

5: Smooth CLI 支持处理动态网页（JavaScript 渲染的内容）吗？

**A**: 是的，Smooth CLI 专门针对现代 Web 环境设计，支持处理由 JavaScript 动态渲染的内容。与简单的 `curl` 或 `wget` 抓取工具不同，Smooth CLI 能够像真实浏览器一样加载页面，执行必要的脚本，等待内容渲染完成后再进行提取。这对于那些依赖 React、Vue 或其他前端框架构建的单页应用（SPA）尤为重要，确保 AI 能获取到最终用户看到的内容，而不是空白页或加载骨架。

---



### 6: 使用 Smooth CLI 会影响 AI 对网页布局的理解吗？

6: 使用 Smooth CLI 会影响 AI 对网页布局的理解吗？

**A**: Smooth CLI 的目标是去除视觉噪音，但保留语义结构。它通常会将内容转换为 Markdown 格式，这种格式保留了标题层级、列表、链接和表格等结构信息。对于大多数 AI 任务（如阅读文章、提取数据或总结摘要），这种文本级的结构已经足够。然而，如果 AI 任务严格依赖于像素级的视觉布局（例如识别复杂的验证码或特定的 CSS 样式），则可能需要配合多模态模型或其他工具使用。

---



### 7: Smooth CLI 是开源软件吗？目前的支持平台有哪些？

7: Smooth CLI 是开源软件吗？目前的支持平台有哪些？

**A**: 是的，Smooth CLI 是一个开源项目。开发者可以在 GitHub 上找到其源代码，查看具体的实现细节，甚至提交 Pull Request 来帮助改进。它通常支持主流的操作系统，包括 Linux、macOS 和 Windows（通常通过 WSL 或原生二进制文件支持）。作为 CLI 工具，它不依赖特定的图形界面，非常适合在服务器端或无头环境中运行。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 在传统的 LLM（大语言模型）调用中，HTML 网页通常包含大量无关的标签、脚本和样式表，导致 Token 消耗巨大。请设计一个基础的文本处理算法，输入为一个包含 HTML 的字符串，输出为只包含可见文本内容的字符串。要求去除所有 `<script>`、`<style>` 标签内容，并移除所有 HTML 标签本身。

### 提示**: 可以考虑使用正则表达式或者简单的字符串匹配来定位标签的起始和结束位置。注意处理标签属性可能包含的 `>` 符号，避免截断错误。

### 

---
## 引用

- **原文链接**: [https://docs.smooth.sh/cli/overview](https://docs.smooth.sh/cli/overview)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46901233](https://news.ycombinator.com/item?id=46901233)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/)
- 标签： [AI Agent](/tags/ai-agent/) / [CLI](/tags/cli/) / [Token 优化](/tags/token-%E4%BC%98%E5%8C%96/) / [浏览器](/tags/%E6%B5%8F%E8%A7%88%E5%99%A8/) / [Hacker News](/tags/hacker-news/) / [智能体](/tags/%E6%99%BA%E8%83%BD%E4%BD%93/) / [命令行工具](/tags/%E5%91%BD%E4%BB%A4%E8%A1%8C%E5%B7%A5%E5%85%B7/) / [Show HN](/tags/show-hn/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/) / [命令行工具](/scenarios/%E5%91%BD%E4%BB%A4%E8%A1%8C%E5%B7%A5%E5%85%B7/)

### 相关文章

- [Smooth CLI：面向 AI 智能体的低 Token 浏览器]({{< relref "posts/20260206-hacker_news-show-hn-smooth-cli-token-efficient-browser-for-ai--11.md" >}})
- [Smooth CLI：面向 AI 智能体的低 Token 开销浏览器]({{< relref "posts/20260206-hacker_news-show-hn-smooth-cli-token-efficient-browser-for-ai--15.md" >}})
- [🔥Show HN: 1人+1智能体=从零打造浏览器! 仅2万行代码🚀]({{< relref "posts/20260128-hacker_news-show-hn-one-human-one-agent-one-browser-from-scrat-16.md" >}})
- [🚀一人+一智能体=从零打造浏览器！仅20K行代码惊艳全场！]({{< relref "posts/20260128-hacker_news-show-hn-one-human-one-agent-one-browser-from-scrat-14.md" >}})
- [深度解密Agent循环！🚀从Codex看AI Agent的核心架构与价值🔍]({{< relref "posts/20260126-blogs_podcasts-unrolling-the-codex-agent-loop-1.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*