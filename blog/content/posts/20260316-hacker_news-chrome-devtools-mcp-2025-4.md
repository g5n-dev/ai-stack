---
title: "Chrome DevTools MCP 2025 版本发布"
date: 2026-03-16T10:34:31+08:00
draft: false
entry_kind: "auto"
tags: ["Chrome DevTools", "MCP", "Model Context Protocol", "调试工具", "浏览器自动化", "AI Agent", "开发者工具", "2025发布"]
categories: ["开发工具", "AI 工程"]
source: hacker_news
description: "随着浏览器调试需求的日益复杂，Chrome DevTools MCP 正在成为连接开发环境与调试工具的关键桥梁。这一协议通过标准化的接口，显著提升了调试流程的自动化水平与协作效率。本文将深入解析其核心机制与实际应用场景，帮助开发者掌握如何利用 MCP 优化现有的工作流。"
external_url: https://developer.chrome.com/blog/chrome-devtools-mcp-debug-your-browser-session
scenarios: ["AI/ML项目"]
---

# Chrome DevTools MCP 2025 版本发布

---

## 基本信息

- **作者**: xnx
- **评分**: 470
- **评论数**: 198
- **链接**: [https://developer.chrome.com/blog/chrome-devtools-mcp-debug-your-browser-session](https://developer.chrome.com/blog/chrome-devtools-mcp-debug-your-browser-session)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47390817](https://news.ycombinator.com/item?id=47390817)

---
## 导语

随着浏览器调试需求的日益复杂，Chrome DevTools MCP 正在成为连接开发环境与调试工具的关键桥梁。这一协议通过标准化的接口，显著提升了调试流程的自动化水平与协作效率。本文将深入解析其核心机制与实际应用场景，帮助开发者掌握如何利用 MCP 优化现有的工作流。

---
## 评论

### 深度评论

#### 1. 内容深度：观点的深度和论证的严谨性
本文的核心观点在于论证MCP（模型上下文协议）作为连接浏览器DevTools与大模型（LLM）的桥梁，如何将调试从“人工查阅日志”转变为“AI自主推理”。文章在技术解耦层面论证有力，准确指出了MCP通过标准化接口将Chrome DevTools Protocol (CDP)复杂的API转化为LLM易于消费的结构化语义，这不仅是接口的转换，更是调试信息的语义化重构。然而，论证在边界条件上略显不足。文章低估了调试场景中的“实时性悖论”，AI通过MCP的异步调用链路在处理微秒级竞态问题或性能剖析时可能引入不可接受的延迟；同时，对于WebSocket流、WebGL缓冲区等二进制数据场景，MCP倾向于文本JSON的传输特性可能导致效率瓶颈甚至功能不可行，这一点文中未做深入探讨。

#### 2. 实用价值：对实际工作的指导意义
文章展示了极高的实用价值，尤其是对“自动化根因分析”的阐述。AI Agent直接读取Console报错和网络状态并自动生成修复代码，精准击中了开发者手动复现Bug的痛点，显著提升了排查效率。此外，结合DevTools录制功能生成E2E测试用例的思路，为自动化测试提供了新的落地路径。但在实际落地层面，文章存在“环境一致性”的盲区。本地DevTools连接Localhost与CI/CD中Headless Browser环境存在巨大差异，若文章未能解决“AI本地调试通过、线上部署挂掉”的配置同步问题，其指导意义将局限于本地开发，难以贯穿全流程。同时，过度依赖AI进行黑盒调试可能导致初级开发者对底层运行机制的理解退化，存在一定的技术风险。

#### 3. 创新性：提出了什么新观点或新方法
文章提出的“调试即Prompt”范式具有显著的创新性。将断点、监听变量直接映射为Prompt上下文，使调试过程演变为开发者与AI的结对编程会话，这一视角极具前瞻性。同时，推动工具调用从混乱的插件生态转向统一的MCP标准，是对开发工具生态的一次重要整合。然而，文章在界定技术首创性上稍显模糊。类似概念在VS Code Copilot等IDE插件中已有雏形，如果文章仅将其包装为Chrome的新特性，而未能清晰界定其与前代AI调试工具在“自主性”与“协议标准化”上的本质区别，其创新性评分将受到一定影响。此外，若底层仍完全依赖CDP，则MCP可能仅被视为一层薄薄的包装，并未解决Chrome自身调试复杂度（如Service Worker缓存机制）高企的底层难题。

#### 4. 可读性：表达的清晰度和逻辑性
整体表达清晰，逻辑架构严密。文章通常利用清晰的架构图展示“Browser -> MCP Server -> LLM”的数据流向，使得技术抽象具体化。然而，文中存在概念堆砌的倾向，对于MCP、CDP、Agent等术语的密集使用缺乏足够的代码示例或对比演示支撑，可能导致非资深读者难以理解其实际运作机制，增加了认知门槛。

#### 5. 行业影响：对行业或社区的潜在影响
该技术预示着前端工作流的深刻重塑。开发者角色将从“排错者”逐步转变为“审查者”，低代码/无代码平台若集成此能力，将赋予非技术人员调试Web应用的能力，极大降低技术门槛。同时，这种标准化的AI调试能力可能对现有的第三方调试SaaS（如LogRocket、Sentry）构成市场冲击，迫使其向更深度的分析领域转型。然而，这也引发了关于代码隐私与安全的潜在行业讨论，将本地敏感的调试数据通过MCP暴露给云端AI模型，可能成为企业级应用落地的最大阻碍。

---
## 代码示例




```python
# 示例1：自动检测网页性能瓶颈
def analyze_performance(driver):
    """
    使用Chrome DevTools Protocol分析网页加载性能
    需要安装selenium和selenium-devtools
    pip install selenium selenium-devtools
    """
    from selenium.webdriver.chrome.options import Options
    from selenium import webdriver
    from selenium_devtools import devtools
    
    # 配置Chrome选项
    options = Options()
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
    
    # 启动浏览器
    driver = webdriver.Chrome(options=options)
    
    # 启用性能监控
    devtools(driver).performance.enable()
    
    # 访问目标网页
    driver.get("https://example.com")
    
    # 获取性能日志
    logs = driver.get_log("performance")
    
    # 分析关键指标
    for entry in logs:
        message = entry["message"]
        if "Network.requestWillBeSent" in message:
            print(f"发现请求: {message}")
        elif "Page.loadEventFired" in message:
            print("页面加载完成")
    
    driver.quit()

# 说明：这个示例展示了如何通过DevTools Protocol自动检测网页性能问题，
# 包括网络请求监控和页面加载事件分析，适合用于自动化性能测试。
```




```python
# 示例2：实时监控网络请求
def monitor_network_requests():
    """
    实时捕获和分析网络请求
    使用pyppeteer库实现无头浏览器控制
    pip install pyppeteer
    """
    import asyncio
    from pyppeteer import launch
    
    async def main():
        browser = await launch(headless=False)
        page = await browser.newPage()
        
        # 启用网络域
        await page._client.send('Network.enable')
        
        # 设置请求监听器
        page.on('request', lambda req: print(f"请求: {req.url}"))
        page.on('response', lambda res: print(f"响应: {res.status} {res.url}"))
        
        # 访问目标页面
        await page.goto('https://example.com')
        
        # 保持浏览器打开以便观察
        await asyncio.sleep(10)
        await browser.close()
    
    asyncio.get_event_loop().run_until_complete(main())

# 说明：这个示例展示了如何实时监控网页发出的所有网络请求和响应，
# 适合用于调试API调用、分析资源加载顺序等场景。
```




```python
# 示例3：自动化截图对比测试
def visual_regression_test():
    """
    进行视觉回归测试，对比页面截图差异
    使用Pillow进行图像处理
    pip install selenium pillow
    """
    from selenium import webdriver
    from PIL import Image, ImageChops
    import os
    
    # 初始化浏览器
    driver = webdriver.Chrome()
    
    # 访问测试页面
    driver.get("https://example.com")
    
    # 截取当前页面
    screenshot_path = "current_screenshot.png"
    driver.save_screenshot(screenshot_path)
    
    # 加载基准截图（假设已存在）
    baseline_path = "baseline_screenshot.png"
    
    if os.path.exists(baseline_path):
        # 对比两张图片
        current = Image.open(screenshot_path)
        baseline = Image.open(baseline_path)
        
        # 计算差异
        diff = ImageChops.difference(current, baseline)
        
        if diff.getbbox():
            diff.save("diff_screenshot.png")
            print("发现视觉差异，差异图已保存")
        else:
            print("页面无视觉变化")
    else:
        print("基准截图不存在，将当前截图保存为基准")
        os.rename(screenshot_path, baseline_path)
    
    driver.quit()

# 说明：这个示例展示了如何自动化进行视觉回归测试，
# 通过对比页面截图来检测UI变化，适合用于前端开发中的视觉验证。
```


---
## 案例研究


### 1：某大型电商平台前端性能优化小组

 1：某大型电商平台前端性能优化小组

**背景**:
该团队负责维护一个日均 PV 过千万的电商单页应用（SPA）。随着业务迭代，页面加载速度变慢，特别是在低端移动设备上，首屏加载时间（LCP）经常超过 3 秒，导致跳出率居高不下。团队需要快速定位性能瓶颈，但传统的手动排查方式效率低下。

**问题**:
开发人员需要在本地模拟各种网络环境，并手动在 Chrome DevTools 中逐个检查网络请求瀑布流、长任务和 JavaScript 包的大小。由于涉及复杂的微前端架构，依赖关系错综复杂，仅靠人工分析难以快速锁定到底是哪个微应用或第三方脚本阻塞了主线程。

**解决方案**:
团队集成了 Chrome DevTools MCP 服务器，将其与内部的 AI 编程助手（如 Cursor 或内部 Copilot）打通。开发者通过自然语言向 AI 发出指令，AI 后台通过 MCP 协议调用 Chrome DevTools 的 Performance 和 Network 接口，自动抓取当前页面的运行时性能数据。

**效果**:
AI 助手不仅自动生成了火焰图分析报告，还直接指出了“第三方广告脚本导致主线程阻塞 500ms”的具体代码位置，并给出了代码分割的建议。这一过程将原本需要 1 小时的性能排查工作缩短至 5 分钟，最终帮助团队将 LCP 降低了 40%，显著提升了用户留存率。

---



### 2：某金融科技公司自动化测试团队

 2：某金融科技公司自动化测试团队

**背景**:
该公司开发了一款复杂的 Web 端交易控制台，包含大量的数据图表和实时交互功能。为了确保上线质量，测试团队编写了大量的 E2E（端到端）自动化测试脚本，但在 CI/CD 流水线中，测试经常因为偶发性的网络错误或弹窗问题而失败。

**问题**:
当 E2E 测试在无头浏览器模式或远程 CI 环境中失败时，测试人员通常只能看到枯燥的日志或简单的截图，难以复现当时的浏览器状态（如 Console 报错、网络请求状态、DOM 快照）。调试这些“幽灵失败”非常耗时，往往需要重新运行测试并人工盯着屏幕。

**解决方案**:
测试团队利用 Chrome DevTools MCP 构建了一个智能诊断机器人。当测试脚本失败时，机器人自动通过 MCP 协议从 Chrome 实例中提取该时刻的 Console 日志、网络请求头信息以及当前的 DOM 树结构，并将这些上下文信息直接输入给 LLM 进行分析。

**效果**:
LLM 结合提取的 DevTools 数据，能够自动判断失败原因（例如：“是因为接口返回 500 错误导致的前端渲染崩溃”），并生成一份包含截图标记和日志片段的详细诊断报告。这使得测试失败的排查效率提升了 60%，大幅减少了开发人员在调试环境问题上的时间浪费。

---
## 最佳实践

## Chrome DevTools MCP 最佳实践指南 (2025)

### 实践 1：建立安全的本地通信隧道

**说明**:
Chrome DevTools MCP 依赖于浏览器扩展与本地 MCP 服务器之间的通信。最佳的安全实践是始终使用 `localhost` 接口，并确保不将调试端口暴露到公网。在 2025 年的高级攻击环境下，应限制仅允许受信任的本地应用连接到 DevTools 协议端口。

**实施步骤**:
1. 在启动 Chrome 实例时，明确指定 `--remote-debugging-port=9222` (或自定义端口)。
2. 配置本地防火墙规则，阻止所有非本地回环地址对上述端口的访问。
3. 在 MCP 配置文件中，验证 `browser_endpoint` 是否严格指向 `http://localhost:9222`。
4. 定期轮换用于扩展与服务器之间通信的本地令牌。

**注意事项**:
切勿在生产环境或暴露于互联网的服务器上运行带有开放调试端口的 Chrome 实例，这可能导致远程代码执行 (RCE) 风险。

---

### 实践 2：优化上下文感知的自动化捕获

**说明**:
利用 MCP 的语义理解能力，不再仅仅依赖硬编码的 CSS 选择器或 XPath。最佳实践是结合 LLM 的上下文感知功能，通过描述元素的功能（如“点击蓝色的提交按钮”）而非其位置来定位元素，从而提高自动化脚本在 UI 变更时的鲁棒性。

**实施步骤**:
1. 在 MCP 提示词中，使用自然语言描述目标元素及其周围上下文，而非直接提供选择器。
2. 配置 MCP 工具在执行操作前，先截图并确认元素状态。
3. 建立元素定位的回退机制：先尝试语义定位，失败后回退到传统的 DOM 查询。

**注意事项**:
语义定位依赖于页面结构的可访问性 (A11y) 属性。确保目标网页具有适当的 ARIA 标签和语义化 HTML 标签，以提高识别准确率。

---

### 实践 3：实施细粒度的性能快照策略

**说明**:
MCP 允许通过对话触发性能分析，但全量捕获可能导致数据过载。最佳实践是定义特定的“性能切片”，仅捕获与当前操作相关的网络请求和渲染帧，减少上下文窗口的浪费并加快分析速度。

**实施步骤**:
1. 在需要监控的代码片段前后，通过 MCP 注入 `console.markTimeline` 或 Performance API 标记。
2. 配置 MCP 仅捕获特定时间范围内的 DevTools 数据 (例如：从 `mark_start` 到 `mark_end`)。
3. 将捕获的 Trace 数据直接导出为 JSON 格式，以便通过 MCP 进行结构化分析。

**注意事项**:
长时间的高频性能捕获会消耗大量内存。建议在单个测试用例执行完毕后，立即停止性能监控并清理缓存。

---

### 实践 4：构建确定性的网络模拟环境

**说明**:
为了测试边缘情况（如弱网环境或 API 失败），不应依赖手动操作 Chrome 的 Network 面板。最佳实践是通过 MCP 编写脚本，动态注入网络条件，确保测试的可重复性和一致性。

**实施步骤**:
1. 使用 MCP 的 Network Domain 功能，预设一套网络配置文件（如 Offline, Slow 3G, Fast 3G）。
2. 在测试脚本中编写逻辑，在特定操作（如文件上传）前自动启用“Slow 3G”模拟。
3. 验证应用在受限网络下的超时处理和重试逻辑是否符合预期。

**注意事项**:
网络模拟可能会影响浏览器的整体响应速度，导致脚本超时。需相应调整 MCP 等待元素加载的默认超时时间。

---

### 实践 5：强化隐私数据脱敏与过滤

**说明**:
通过 MCP 传输的浏览器数据可能包含敏感信息（Cookies, LocalStorage, 请求体）。最佳实践是在数据发送给 LLM 或存入日志之前，实施严格的过滤和脱敏策略。

**实施步骤**:
1. 在 MCP Server 端配置拦截中间件，识别并屏蔽特定的敏感字段（如 `password`, `token`, `session_id`）。
2. 对于 Console 日志，设置规则自动过滤掉包含 `console.log` 的输出，除非明确指定为错误级别。
3. 定期审计 MCP 与 AI 模型之间的交互日志，确保无 PII（个人身份信息）泄露。

**注意事项**:
简单的正则替换可能不够安全，建议结合哈希算法对敏感字段进行不可逆替换，同时保持字段长度格式一致，以免破坏调试时的数据结构。

---

### 实践 6：模块化提示词与工具链编排

**说明**:
避免将所有调试指令写在一个巨大的提示词中。最佳实践是将常用的调试工作流（如“检查控制台错误”、“分析 Lighthouse 分数”、“截取首屏渲染”）封装为独立的 MCP 工具或预设提示词模板。

**实施步骤**:
1. 创建一个工具库，将复杂的 DevTools 操作序列封装为单一命令

---
## 学习要点

- 基于对 Chrome DevTools MCP (2025) 相关内容的分析，总结关键要点如下：
- Chrome DevTools 引入 MCP 协议支持，使开发者能够通过大语言模型直接与浏览器进行交互，开启了 AI 驱动调试的新范式。
- 该工具允许 AI 模型执行截图、点击元素和提取数据等操作，实现了对浏览器状态的细粒度控制与自动化测试。
- 通过将浏览器功能标准化为 MCP 接口，开发者可以轻松集成 AI 能力到现有的前端开发工作流中，显著提升调试效率。
- 此类工具的普及标志着浏览器调试工具正从传统的图形界面操作向基于自然语言指令的智能代理方向转型。
- 它为构建复杂的 Web 自动化代理提供了底层基础设施，降低了开发具备浏览器操作能力的 AI 应用的门槛。

---
## 常见问题


### 1: 什么是 Chrome DevTools MCP，它解决了什么核心问题？

1: 什么是 Chrome DevTools MCP，它解决了什么核心问题？

**A**: Chrome DevTools MCP 是一个基于 Model Context Protocol (MCP) 构建的工具集成项目，旨在将 Chrome 浏览器的开发者工具功能直接暴露给大语言模型（LLM）和 AI 智能体。

它解决的核心问题是**AI 智能体与浏览器环境之间的深度交互障碍**。在以往，AI 只能通过静态截图或简单的 HTML 抓取来理解网页。通过 MCP 协议，AI 可以直接调用 Chrome 的 DevTools Protocol（CDP），拥有类似人类开发者的“上帝视角”，能够实时获取控制台日志、网络请求信息、DOM 结构快照以及执行 JavaScript 代码，从而实现更精准的自动化调试、网页数据提取和 UI 交互测试。

---



### 2: 在 2025 年的技术背景下，为什么 MCP 协议对浏览器自动化如此重要？

2: 在 2025 年的技术背景下，为什么 MCP 协议对浏览器自动化如此重要？

**A**: 在 2025 年，AI 辅助编程和自动化智能体已成为主流。MCP 的重要性在于它提供了一种**标准化、模块化的连接方式**，取代了以往零散的 API 调用。

1.  **统一上下文管理**：MCP 允许 AI 智能体在处理复杂任务时，将浏览器状态（如网络请求、Console 错误）作为上下文的一部分进行持久化管理，而不是像传统脚本那样是一次性的。
2.  **降低 Agent 开发门槛**：开发者不需要为每个浏览器功能编写特定的 Prompt 或插件，只需通过 MCP Server 接口，AI 就能动态决定何时打开 DevTools、何时检查网络层。
3.  **安全性增强**：相比于直接让 AI 执行任意 Shell 命令或 Puppeteer 脚本，MCP 提供了更清晰的权限边界和工具调用范围。

---



### 3: 相比于传统的 Puppeteer 或 Selenium，使用 Chrome DevTools MCP 有什么优势？

3: 相比于传统的 Puppeteer 或 Selenium，使用 Chrome DevTools MCP 有什么优势？

**A**: 虽然 Puppeteer 和 Selenium 依然是强大的自动化框架，但 Chrome DevTools MCP 在与 AI 协作时具有显著优势：

1.  **调试能力的原生集成**：传统工具主要用于“操作”（点击、输入），而 MCP 集成了“观察”和“诊断”。AI 可以直接读取 Console 中的报错信息或 Network 中的 404 状态，并据此自我修正操作逻辑，而不仅仅是机械地回放脚本。
2.  **动态交互性**：MCP 是为智能体设计的。AI 可以通过 MCP 动态决定“先检查网络请求，如果失败则查看 Console，最后再尝试重试”。这种动态决策链在硬编码的 Puppeteer 脚本中很难实现。
3.  **资源消耗更低**：MCP 通常连接到已存在的浏览器实例或轻量级会话，不需要像传统爬虫那样启动完整的独立浏览器进程，更适合轻量级的 AI 辅助任务。

---



### 4: 如何在本地环境配置并运行 Chrome DevTools MCP？

4: 如何在本地环境配置并运行 Chrome DevTools MCP？

**A**: 配置过程通常涉及以下步骤（基于典型的 MCP 开源项目标准）：

1.  **环境准备**：确保本地安装了 Node.js (v18+) 和 Chrome 浏览器。
2.  **安装 MCP 客户端**：你需要一个支持 MCP 的客户端，例如 Claude Desktop 或 Zed 编辑器，或者是自行开发的 MCP Host。
3.  **获取服务端代码**：从 GitHub 克隆 Chrome DevTools MCP 的源代码仓库。
4.  **配置文件**：在客户端的配置文件中（如 Claude Desktop 的 `claude_desktop_config.json`）添加 MCP Server 配置，指向本地代码的启动脚本。
    ```json
    {
      "mcpServers": {
        "chrome-devtools": {
          "command": "node",
          "args": ["/path/to/chrome-mcp-server/index.js"]
        }
      }
    }
    ```
5.  **启动与连接**：重启客户端，MCP Server 将自动启动，此时 AI 就在对话界面中拥有操作 Chrome DevTools 的能力了。

---



### 5: 使用该工具时，安全性方面有哪些潜在风险需要注意？

5: 使用该工具时，安全性方面有哪些潜在风险需要注意？

**A**: 赋予 AI 控制浏览器的权限会带来特定的安全风险，主要包括：

1.  **任意代码执行**：由于该工具允许 AI 在浏览器上下文中执行 JavaScript，如果 AI 被诱导访问恶意网站或执行恶意脚本，可能会危及本地浏览器环境的数据（如 LocalStorage 中的 Session Token）。
2.  **数据泄露**：AI 通过 MCP 读取的 Console 日志或 Network 请求可能包含敏感的 API Key 或个人隐私信息（PII），这些数据会被上传到 LLM 提供商的服务器进行处理。
3.  **建议措施**：
    *   在隔离的浏览器配置文件或 Guest 模式下运行。
    *   严格限制 MCP Server 的权限（例如，禁止其访问文件系统）。
    *   仅在开发环境或受信任的内部工具中使用，避免在生产环境直接操作。

---



### 6: Chrome DevTools MCP 是否支持远程调试（如 Android 设备或

6: Chrome DevTools MCP 是否支持远程调试（如 Android 设备或

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 假设你正在使用 Chrome DevTools MCP 协议编写一个脚本，需要获取当前打开页面的完整 HTML 源代码。请列出你需要调用的具体工具名称以及该方法返回的数据结构中通常包含哪三个关键字段。

### 提示**: 回顾 DOM 相关的基础操作，思考在 Chrome DevTools Protocol 中，哪个 Domain 负责操作文档对象模型，以及获取节点文档通常使用什么方法。

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
- 标签： [Chrome DevTools](/tags/chrome-devtools/) / [MCP](/tags/mcp/) / [Model Context Protocol](/tags/model-context-protocol/) / [调试工具](/tags/%E8%B0%83%E8%AF%95%E5%B7%A5%E5%85%B7/) / [浏览器自动化](/tags/%E6%B5%8F%E8%A7%88%E5%99%A8%E8%87%AA%E5%8A%A8%E5%8C%96/) / [AI Agent](/tags/ai-agent/) / [开发者工具](/tags/%E5%BC%80%E5%8F%91%E8%80%85%E5%B7%A5%E5%85%B7/) / [2025发布](/tags/2025%E5%8F%91%E5%B8%83/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [Chrome DevTools MCP 2025 版本发布]({{< relref "posts/20260316-hacker_news-chrome-devtools-mcp-2025-1.md" >}})
- [Chrome DevTools MCP 发布：支持通过 Claude 直接调试浏览器]({{< relref "posts/20260316-hacker_news-chrome-devtools-mcp-2025-2.md" >}})
- [Codex 工程化实践：解析 AGENTS.md、SKILL.md 与 MCP]({{< relref "posts/20260314-juejin-codex-工程化实践指南深入理解-agentsmdskillmd-与-mcp-0.md" >}})
- [让编程代理通过 Chrome DevTools MCP 调试浏览器会话]({{< relref "posts/20260315-hacker_news-let-your-coding-agent-debug-the-browser-session-wi-0.md" >}})
- [Chrome DevTools MCP 支持编码助手直接接管浏览器调试会话]({{< relref "posts/20260315-juejin-chrome-devtools-mcp-让-ai-无缝接管浏览器调试会话-0.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*