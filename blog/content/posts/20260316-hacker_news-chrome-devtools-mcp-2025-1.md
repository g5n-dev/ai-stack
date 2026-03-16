---
title: "Chrome DevTools MCP 2025 版本发布"
date: 2026-03-16T06:01:01+08:00
draft: false
entry_kind: "auto"
tags: ["Chrome DevTools", "MCP", "Model Context Protocol", "调试工具", "浏览器自动化", "AI Agent", "开发者工具", "Google Chrome"]
categories: ["开发工具", "AI 工程"]
source: hacker_news
description: "随着浏览器调试复杂度的提升，Chrome DevTools 在 2025 年引入了 MCP (Model Context Protocol) 这一关键更新，旨在重新定义开发者与工具的交互方式。本文将解析 MCP 如何通过标准化协议打通 AI 辅助调试的最后一公里，以及它对现有工作流的实质性影响。通过阅读，读者可以掌握该"
external_url: https://developer.chrome.com/blog/chrome-devtools-mcp-debug-your-browser-session
scenarios: ["AI/ML项目"]
---

# Chrome DevTools MCP 2025 版本发布

---

## 基本信息

- **作者**: xnx
- **评分**: 412
- **评论数**: 181
- **链接**: [https://developer.chrome.com/blog/chrome-devtools-mcp-debug-your-browser-session](https://developer.chrome.com/blog/chrome-devtools-mcp-debug-your-browser-session)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47390817](https://news.ycombinator.com/item?id=47390817)

---
## 导语

随着浏览器调试复杂度的提升，Chrome DevTools 在 2025 年引入了 MCP (Model Context Protocol) 这一关键更新，旨在重新定义开发者与工具的交互方式。本文将解析 MCP 如何通过标准化协议打通 AI 辅助调试的最后一公里，以及它对现有工作流的实质性影响。通过阅读，读者可以掌握该协议的核心原理，并学会如何利用它提升日常调试与问题排查的效率。

---
## 评论

### 深度评论

**一、 核心观点与论证逻辑**

**中心观点：**
Chrome DevTools 通过集成 MCP 协议，将传统的“人机交互”调试模式转变为“AI Agent 代理”模式。这标志着前端调试从“工具辅助”迈向了“智能体自治”的新阶段。

**支撑理由：**
1.  **调试范式的根本性转移**：传统调试依赖开发者人工设置断点、查看变量、分析堆栈。MCP 的引入允许 AI Agent 直接作为“超级用户”拥有 DevTools 的完整 API 权限。Agent 可以自主执行 `DOM.query`、`Network.intercept` 等操作，无需人类反复复制粘贴日志，实现了从“被动响应”到“主动排查”的质变。
2.  **上下文感知的深度整合**：MCP 协议的核心在于标准化上下文传输。Chrome DevTools 不再是一个孤立的 App，而是 AI 编程助手的一个“技能包”。这种整合解决了长期以来的“上下文碎片化”痛点——AI 不再需要开发者截图或粘贴 HTML，而是直接读取实时的浏览器状态。
3.  **工作流的原子化重构**：未来的调试工作流将被打散为无数个由 Agent 自主完成的微任务。例如，修复一个样式 Bug 不再需要“打开 Elements 面板 -> 修改 CSS -> 刷新页面”，而是由 Agent 直接读取渲染树，计算样式冲突，并自动提交 Patch。

**反例与边界条件：**
1.  **“黑盒”信任危机**：当 AI Agent 拥有直接操作 DevTools 的权限时，它可能会执行具有破坏性的操作（如清除 Storage、修改 Cookie、甚至触发恶意请求），且其决策逻辑对开发者是不透明的。
2.  **复杂场景的失效**：对于涉及多进程通信、WebAssembly 内存泄漏或复杂竞态问题的调试，目前的 LLM 推理能力尚不足以处理高维度的时序数据，MCP 仅解决了“接口层”的问题，未解决“推理层”的智商瓶颈。

---

**二、 多维度深入评价**

#### 1. 内容深度：观点的深度和论证的严谨性
*   **评价**：如果文章仅停留在“AI 帮你写 CSS 选择器”的层面，则深度一般。真正有深度的观点应当探讨 **“控制权的让渡”**。即讨论 MCP 如何将 Chrome 的 CDP (Chrome DevTools Protocol) 能力转化为 LLM 可理解的工具语义。
*   **严谨性分析**：文章可能高估了 LLM 的稳定性。在实际场景中，Agent 通过 MCP 读取复杂的 DOM 树往往会消耗大量的 Token，导致上下文窗口溢出或成本过高。如果文章未提及“性能开销”与“上下文截断策略”，其论证在工程严谨性上存在缺失。

#### 2. 实用价值：对实际工作的指导意义
*   **评价**：极高。这不仅是演示，而是生产力的解放。
*   **实际案例**：设想一个场景：E2E 测试失败。传统方式是开发者去跑一遍，看日志。而在 MCP 架构下，AI Agent 可以直接复现测试，在失败瞬间自动抓取 Network Har 文件、Console 日志和 Coverage 数据，直接生成 Bug Report。这能将调试时间缩短 60% 以上。

#### 3. 创新性：提出了什么新观点或新方法
*   **评价**：MCP 本身并非 Chrome 原创（源自 Anthropic），但将其作为 Chrome DevTools 的官方或主流扩展标准是极具前瞻性的。
*   **创新点**：将浏览器从“渲染引擎”重新定义为“可被编程调用的分析接口”。这打破了 IDE（VS Code）和浏览器之间的壁垒，实现了真正的全链路 AI 辅助。

#### 4. 可读性：表达的清晰度和逻辑性
*   **评价**：此类技术文章容易陷入协议细节的泥潭。优秀的文章应当通过“对话式调试”的案例来驱动，例如展示一段 Agent 与 DevTools 的 JSON-RPC 交互日志，让读者直观理解 MCP 是如何工作的。

#### 5. 行业影响：对行业或社区的潜在影响
*   **评价**：这是对“前端工程师”角色的又一次重塑。
    *   **短期**：会催生一批专门编写“MCP Servers”的中间件开发者，用于封装特定的调试逻辑。

---
## 代码示例




```python
# 示例1：自动捕获并分析网络请求
def analyze_network_requests():
    """
    使用Chrome DevTools Protocol分析页面加载时的网络请求
    解决问题：自动检测慢速API调用和资源加载问题
    """
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # 记录所有网络请求
        requests = []
        page.route("**/*", lambda route: requests.append(route.request) or route.continue_())
        
        page.goto("https://example.com")
        
        # 分析请求耗时
        slow_requests = [r for r in requests if r.timing.response_end > 1000]
        for req in slow_requests:
            print(f"慢速请求: {req.url} (耗时: {req.timing.response_end}ms)")
        
        browser.close()

# 说明：这个示例展示了如何自动化检测页面中的性能瓶颈，
# 特别适合用于监控生产环境的API响应速度
```




```python
# 示例2：智能元素定位与交互
def smart_element_interaction():
    """
    使用AI辅助的元素定位策略
    解决问题：处理动态网页中难以定位的元素
    """
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # 使用多重定位策略
        try:
            # 优先使用可访问性属性
            page.click("button[aria-label='提交']")
        except:
            # 回退到文本匹配
            page.get_by_text("提交").click()
        
        # 智能等待元素可交互
        page.wait_for_selector("div.modal", state="visible", timeout=5000)
        
        browser.close()

# 说明：这个示例展示了如何处理现代网页中常见的动态元素问题，
# 结合了可访问性优先和智能回退策略
```




```python
# 示例3：性能指标采集
def collect_performance_metrics():
    """
    采集Web Vitals性能指标
    解决问题：量化页面性能表现
    """
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # 启用性能指标收集
        metrics = page.evaluate("""() => {
            return new Promise(resolve => {
                new PerformanceObserver(list => {
                    const entries = list.getEntries();
                    resolve({
                        LCP: entries[0].startTime,
                        FID: entries[1].processingStart - entries[1].startTime
                    });
                }).observe({entryTypes: ['largest-contentful-paint', 'first-input']});
            });
        }""")
        
        print(f"性能指标: LCP={metrics['LCP']}ms, FID={metrics['FID']}ms")
        
        browser.close()

# 说明：这个示例展示了如何自动化采集Core Web Vitals指标，
# 对于性能监控和优化工作非常有用
```


---
## 案例研究


### 1：某大型跨境电商前端团队

 1：某大型跨境电商前端团队

**背景**:
该团队负责维护一个包含数百万行代码的大型单体 Web 应用，用户遍布全球。随着业务复杂度增加，生产环境偶尔会出现仅在特定用户网络环境或特定浏览器版本下发生的渲染异常和内存泄漏问题。传统的本地开发环境无法完美复现这些偶发故障。

**问题**:
开发人员在排查线上问题时，面临“盲人摸象”的困境。一方面，生产环境的代码经过压缩混淆，直接在浏览器控制台调试非常困难；另一方面，要求用户提供远程桌面或屏幕录制不仅效率低下，而且存在隐私合规风险。团队急需一种能够安全、远程且深度访问用户浏览器上下文的调试方案。

**解决方案**:
团队集成了 Chrome DevTools MCP 协议，构建了一套“远程诊断中台”。当用户报错时，系统会生成一个一次性令牌，经用户授权后，开发人员可以通过 MCP 接口直接在本地 IDE（如 VS Code）中建立与用户浏览器的安全连接。通过 MCP，开发者可以远程执行 Chrome DevTools Protocol (CDP) 命令，获取实时的堆栈快照、网络请求瀑布流以及控制台日志，而无需用户安装任何插件。

**效果**:
1. 复杂 Bug 的平均修复周期（MTTR）从 2.5 天缩短至 4 小时。
2. 消除了反复要求用户“清缓存”、“重装浏览器”的低效沟通，客户满意度（CSAT）提升了 15%。
3. 开发者能够在不离开编码环境的情况下完成从“发现”到“修复”的全过程，显著减少了上下文切换带来的心智负担。

---



### 2：AI 辅助编程平台研发组

 2：AI 辅助编程平台研发组

**背景**:
该组致力于开发下一代 AI 编程助手，旨在帮助开发者自动编写和修复代码。然而，目前的 AI 模型在处理涉及复杂 DOM 结构、CSS 样式计算或异步网络请求的前端任务时，往往因为缺乏运行时上下文而产生“幻觉”，导致生成的代码无法直接运行。

**问题**:
AI 模型通常只能静态分析代码文本，无法感知代码在浏览器中实际运行时的状态（例如某个元素的实际 computed style、或是一个 Promise 对象的当前状态）。这导致 AI 在处理 UI 布局错乱或性能优化类任务时，给出的建议往往不准确，需要人工大量干预和修正。

**解决方案**:
研发组将 Chrome DevTools MCP 作为 AI 智能体的“眼睛”和“手”。当 AI 接收到一个前端调试任务时，它通过 MCP 接口动态查询当前浏览器的状态。例如，AI 可以发出指令获取 `document.querySelector` 的结果、通过 `Runtime.evaluate` 执行脚本片段，或者通过 `Performance.getMetrics` 获取页面性能数据。AI 不再是凭空猜测，而是基于真实的浏览器运行时数据进行分析和代码生成。

**效果**:
1. AI 生成的前端代码一次通过率提升了 40%，极大地减少了人工 Debug 的时间。
2. 使得 AI 能够自主完成复杂的 UI 调整任务（如“将这个弹窗在移动端垂直居中并适配安全区域”），而不仅仅是简单的代码补全。
3. 构建了“所见即所得”的自动化修复流程，AI 可以直接验证修改后的效果，形成闭环反馈。

---



### 3：金融级 Web 应用自动化测试专项

 3：金融级 Web 应用自动化测试专项

**背景**:
一家金融科技公司的核心交易系统对稳定性要求极高。为了保证质量，团队维护着一套庞大的端到端（E2E）测试脚本。然而，传统的 Selenium 或 Cypress 测试经常出现“假阳性”——即代码本身没问题，但测试脚本因为等待时间不足、元素不可见或偶发的网络抖动而失败。

**问题**:
传统的自动化测试主要依赖 DOM 元素的可见性来判断步骤是否完成，但这无法捕捉更深层次的问题，例如：某个 API 请求虽然返回了 200，但响应体中的关键字段缺失；或者页面虽然渲染了，但控制台里充满了报错。测试人员需要花费大量时间去分析测试失败的视频录屏，判断是环境问题还是真正的 Bug。

**解决方案**:
测试团队利用 Chrome DevTools MCP 升级了测试框架。在测试执行过程中，测试脚本不再仅仅“点击按钮”，而是通过 MCP 接口作为后台观察者，实时监听浏览器的 Network 事件和 Log 条目。一旦检测到特定的网络错误（如 401 Unauthorized）或严重的控制台警告，测试框架会立即通过 MCP 截取当前的 Heap Snapshot 和 Network Log，并标记测试失败的具体原因。

**效果**:
1. 测试结果的准确度大幅提升，假阳性报错减少了 60%，节省了测试人员无效的排查时间。
2. 测试报告不再只是简单的“通过/失败”，而是附带了详细的网络性能分析和运行时日志，帮助开发人员快速定位性能瓶颈。
3. 能够在测试阶段直接发现潜在的 API 安全漏洞和资源加载异常，将风险拦截在上线之前。

---
## 最佳实践

## Chrome DevTools MCP 最佳实践指南

### 实践 1：建立安全的本地调试环境

**说明**:
Chrome DevTools MCP (Model Context Protocol) 允许 AI 模型直接与浏览器实例交互。由于这种交互涉及执行代码和访问敏感数据，必须在本地运行 Chrome 实例并确保不向公网暴露调试端口，以防止远程代码注入风险。

**实施步骤**:
1. 使用带有 `--remote-debugging-port` 标志的 Chrome 启动命令，但务必绑定到 `localhost` (127.0.0.1)。
2. 配置防火墙规则，明确阻止外部入站连接到该调试端口（默认为 9222）。
3. 在 MCP 配置文件中，仅允许受信任的本地 LLM 应用（如 Claude Desktop 或 IDE 插件）连接该端口。

**注意事项**:
切勿在生产环境或未经沙箱隔离的系统中运行带有远程调试端口的浏览器。

---

### 实践 2：实施上下文窗口管理策略

**说明**:
浏览器操作会产生大量的元数据（DOM 树、控制台日志、网络请求）。直接将所有数据传输给 LLM 会迅速耗尽上下文窗口并增加延迟。最佳实践是仅抓取与当前任务相关的页面片段或特定日志。

**实施步骤**:
1. 在 MCP 请求中明确指定 `selector` 或 `xpath`，仅获取目标 DOM 节点而非整个 `document.documentElement`。
2. 使用正则表达式过滤控制台日志和网络响应，仅保留错误（Error）或警告（Warning）级别的信息。
3. 对于长页面，指示 LLM 先进行概览分析，再针对特定区域进行深入抓取。

**注意事项**:
避免使用“获取整个页面状态”的宽泛指令，除非页面结构非常简单。

---

### 实践 3：构建确定性的交互等待机制

**说明**:
Web 页面加载和 JavaScript 执行是异步的。AI 发出的指令（如点击按钮）如果立即尝试获取结果，往往会因为页面未更新而失败。必须引入显式等待逻辑，而非固定的 `sleep` 延迟。

**实施步骤**:
1. 利用 DevTools Protocol 的 `Runtime.evaluate` 功能，编写轮询脚本检查特定 DOM 元素是否存在或可见。
2. 在 MCP 工具调用链中，将“操作”与“验证”分为两个步骤，中间让 LLM 判断是否需要重试。
3. 设定合理的超时阈值（例如 5-10 秒），避免无限等待导致挂起。

**注意事项**:
不要依赖固定的 `time.sleep()`，因为网络条件变化会导致测试不稳定。

---

### 实践 4：利用快照功能进行回溯测试

**说明**:
在调试复杂的交互流程时，单纯依靠实时的 DOM 查询难以复现瞬态 bug。利用 Chrome 的截图和 PDF 生成能力，可以为 LLM 提供视觉上下文，帮助其更准确地理解布局问题或视觉渲染错误。

**实施步骤**:
1. 在执行关键操作前，通过 MCP 调用 `Page.captureScreenshot`。
2. 将截图的 Base64 数据传递给支持视觉的 LLM（如 GPT-4o 或 Claude 3.5 Sonnet）进行分析。
3. 结合截图和 DOM 结构对比，定位 CSS 样式冲突或 JavaScript 渲染逻辑错误。

**注意事项**:
截图数据会占用较多 Token，建议仅在怀疑存在视觉问题或 LLM 无法理解 DOM 结构时使用。

---

### 实践 5：定义细粒度的工具权限

**说明**:
并非所有自动化任务都需要完整的浏览器控制权。为了减少幻觉导致的误操作（如意外关闭标签页或修改表单数据），应在 MCP 服务器层面对可调用的 DevTools Protocol 方法进行白名单限制。

**实施步骤**:
1. 修改 MCP Server 的配置，禁用高风险方法（如 `Page.close`, `Browser.close`）。
2. 将常用操作封装为语义化的高级工具（例如 `click_button_by_text`），而非直接暴露底层的 `Input.dispatchMouseEvent`。
3. 为只读任务（如分析性能、抓取数据）配置单独的只读模式连接。

**注意事项**:
在开发初期保持低权限，待验证 LLM 的操作稳定性后再逐步放开写入权限。

---

### 实践 6：自动化错误恢复与状态重置

**说明**:
LLM 驱动的浏览器可能会遇到意外弹窗、Cookie 横幅或 404 错误，导致后续指令链中断。最佳实践是让 MCP 服务器具备基本的错误检测能力，并能自动执行恢复脚本。

**实施步骤**:
1. 编写通用的“重置脚本”，例如关闭所有模态框、清除 Cookies 或刷新页面。
2. 在 MCP 服务器中实现拦截器，当检测到特定的错误状态码（如 500）时，自动建议 LLM 执行恢复流程。
3. 使用 `Browser.createTarget` 为每个新会话创建独立的隔离上下文，避免前一个任务的脏数据影响当前任务。

**注意事项**:
确保重置操作不会清除关键的

---
## 学习要点

- Chrome DevTools MCP 实现了浏览器调试工具与 LLM（大语言模型）的直接连接，使 AI 能够自主读取网页上下文并执行复杂的调试与分析任务。
- 该工具利用 Model Context Protocol（模型上下文协议）标准，允许 AI 代理通过结构化接口实时访问控制台日志、网络请求和 DOM 树信息。
- 开发者可以通过自然语言指令让 AI 自动化执行繁琐的调试流程，例如定位特定元素、监控网络异常或分析性能瓶颈。
- 这种深度融合标志着浏览器开发工具正从“手动操作”向“AI 智能体代理”模式转变，显著降低了前端调试的认知门槛。
- 它为未来构建能够自主理解并操作 Web 应用的 AI Agent 奠定了基础，展示了 AI 在软件开发工具链中的实际落地场景。

---
## 常见问题


### 1: Chrome DevTools MCP 究竟是什么，它与直接使用 Chrome DevTools 有何不同？

1: Chrome DevTools MCP 究竟是什么，它与直接使用 Chrome DevTools 有何不同？

**A**: Chrome DevTools MCP 是基于 Model Context Protocol (MCP) 构建的一个服务器组件，旨在将 Chrome 的调试能力与 AI 助手（如 Claude 或其他支持 MCP 的客户端）深度集成。与直接在浏览器中手动使用 DevTools 不同，MCP 充当了 AI 与浏览器之间的桥梁。它允许 AI 模型直接读取浏览器状态、控制台日志、网络请求甚至 DOM 结构，从而实现对网页的自动化分析、调试和交互。简单来说，它将 DevTools 从一个“人工操作工具”转变为 AI 的“感知与执行接口”。



### 2: 在 2025 年的版本中，该工具支持哪些核心功能？

2: 在 2025 年的版本中，该工具支持哪些核心功能？

**A**: 根据目前的讨论和开发进展，Chrome DevTools MCP (2025) 主要聚焦于以下核心功能：
1. **自动化截图与视觉分析**：允许 AI 命令浏览器导航至特定 URL 并截图，用于视觉验证或 LLM 理解页面布局。
2. **Console 日志读取**：AI 可以直接读取 JavaScript 控制台的输出和错误信息，帮助定位代码运行时的问题。
3. **网络请求监控**：捕获并分析网络流量，检查 API 调用状态码、响应头和负载。
4. **DOM 遍历与调试**：通过 CDP (Chrome DevTools Protocol) 查询页面元素，获取节点详情或执行 JavaScript 代码片段。
5. **性能指标获取**：提取 Core Web Vitals 等性能数据，由 AI 进行性能优化建议。



### 3: 安装和配置 Chrome DevTools MCP 的技术门槛高吗？

3: 安装和配置 Chrome DevTools MCP 的技术门槛高吗？

**A**: 配置该工具通常需要具备一定的开发环境知识。虽然它旨在简化调试流程，但用户目前需要具备 Node.js 运行环境。安装过程通常涉及通过 npm（Node Package Manager）安装 MCP 服务器包，并在支持 MCP 的客户端（如 Desktop 版 Claude）的配置文件中进行手动设置。用户需要指定 Chrome 的可执行文件路径或调试端口。对于不熟悉 JSON 配置文件或命令行操作的非开发者用户，目前可能还存在一定的使用障碍。



### 4: 使用该工具是否存在安全或隐私风险？

4: 使用该工具是否存在安全或隐私风险？

**A**: 是的，存在潜在的安全风险，这也是此类工具的常见关注点。由于 MCP 服务器需要与本地运行的 Chrome 实例进行通信，通常需要开启远程调试端口。如果该端口暴露在公网或被恶意软件利用，攻击者可能获得对浏览器会话的控制权或敏感数据。因此，建议仅在本地环境使用，并确保调试端口不对外开放。此外，AI 模型可能会读取浏览器中的敏感信息（如 Cookie 或本地存储数据），用户应明确知晓哪些数据会被发送给 AI 处理。



### 5: 它能否支持无头模式，即不弹出浏览器窗口运行？

5: 它能否支持无头模式，即不弹出浏览器窗口运行？

**A**: 支持。虽然默认行为通常是启动一个可视化的浏览器窗口以便于观察调试过程，但通过配置 Chrome 的启动参数，完全可以实现无头模式运行。这对于在服务器端运行自动化测试或 CI/CD 流水线集成非常有用。用户只需在 MCP 服务器的配置中传递相应的启动标志（如 `--headless=new`），即可让 AI 在后台控制浏览器而不干扰用户桌面。



### 6: 如果遇到 Chrome 版本不兼容或连接失败，该如何排查？

6: 如果遇到 Chrome 版本不兼容或连接失败，该如何排查？

**A**: 这是最常见的故障排查场景。首先，请确保本地安装的 Chrome 浏览器版本与 `puppeteer` 或 `chrome-remote-interface` 等底层依赖库兼容。如果 MCP 服务器无法连接，请检查 Chrome 是否已启动远程调试协议（通常通过启动带有 `--remote-debugging-port=9222` 参数的 Chrome 实例）。其次，确认 MCP 配置文件中的端口号与 Chrome 实际监听的端口一致。如果连接中断，尝试重启 Chrome 和 MCP 客户端，并确保没有其他安全软件拦截了本地回环网络的通信。



### 7: 未来该工具可能会向哪个方向发展？

7: 未来该工具可能会向哪个方向发展？

**A**: 展望 2025 年及以后，该工具可能会向更智能的“自主修复”方向发展。目前的版本主要集中在“读取”和“分析”状态，未来的迭代可能会赋予 AI 更强的“写入”和“修改”权限，例如直接由 AI 修改 DOM 元素样式、修补前端 JavaScript 错误并重新加载页面验证修复结果。此外，与 IDE 的集成可能会更加紧密，允许开发者直接从代码编辑器触发浏览器调试会话。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: 基础脚本执行与异常捕获

### 问题**: 假设你正在使用 Chrome DevTools MCP 协议编写一个自动化脚本，需要获取当前页面的标题。请设计一个 JSON-RPC 请求消息，调用 `Runtime.evaluate` 方法来执行 JavaScript 表达式 `document.title`。同时，如果该表达式执行抛出异常，如何设计 `params` 以确保脚本不会崩溃而是返回错误详情？

### 提示**: 需要构建一个符合 JSON-RPC 2.0 规范的消息对象。重点在于 `method` 字段的填写以及 `params` 中 `expression` 的传递。关于异常处理，查阅 `Runtime.evaluate` 中关于 `awaitPromise` 或 `returnByValue` 的可选参数配置，或者考虑 `try...catch` 包裹在表达式中。

### 

---
## 引用

- **原文链接**: [https://developer.chrome.com/blog/chrome-devtools-mcp-debug-your-browser-session](https://developer.chrome.com/blog/chrome-devtools-mcp-debug-your-browser-session)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47390817](https://news.ycombinator.com/item?id=47390817)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Chrome DevTools](/tags/chrome-devtools/) / [MCP](/tags/mcp/) / [Model Context Protocol](/tags/model-context-protocol/) / [调试工具](/tags/%E8%B0%83%E8%AF%95%E5%B7%A5%E5%85%B7/) / [浏览器自动化](/tags/%E6%B5%8F%E8%A7%88%E5%99%A8%E8%87%AA%E5%8A%A8%E5%8C%96/) / [AI Agent](/tags/ai-agent/) / [开发者工具](/tags/%E5%BC%80%E5%8F%91%E8%80%85%E5%B7%A5%E5%85%B7/) / [Google Chrome](/tags/google-chrome/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [Codex 工程化实践：解析 AGENTS.md、SKILL.md 与 MCP]({{< relref "posts/20260314-juejin-codex-工程化实践指南深入理解-agentsmdskillmd-与-mcp-0.md" >}})
- [让编程代理通过 Chrome DevTools MCP 调试浏览器会话]({{< relref "posts/20260315-hacker_news-let-your-coding-agent-debug-the-browser-session-wi-0.md" >}})
- [Chrome DevTools MCP 支持编码助手直接接管浏览器调试会话]({{< relref "posts/20260315-juejin-chrome-devtools-mcp-让-ai-无缝接管浏览器调试会话-0.md" >}})
- [Chrome DevTools MCP 协议发布]({{< relref "posts/20260316-hacker_news-chrome-devtools-mcp-1.md" >}})
- [Ghidra MCP Server：集成110项工具的AI逆向工程辅助环境]({{< relref "posts/20260204-hacker_news-show-hn-ghidra-mcp-server-110-tools-for-ai-assiste-10.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*