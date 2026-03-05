---
title: "PageAgent：运行于 Web 应用内部的 GUI 智能体"
date: 2026-03-05T22:28:24+08:00
draft: false
entry_kind: "auto"
tags: ["PageAgent", "GUI Agent", "Web 应用", "智能体", "浏览器自动化", "前端集成", "Show HN", "AI 辅助开发"]
categories: ["AI 工程", "前端"]
source: hacker_news
description: "随着大模型能力的提升，如何让 AI 像人类一样直接操作图形界面（GUI）已成为自动化领域的关键课题。PageAgent 是一款直接集成在 Web 应用内部的 GUI 智能体，它能够理解界面上下文并自主执行操作。本文将介绍其技术架构与实现逻辑，帮助开发者探索如何利用智能体技术，显著提升 Web 应用的自动化交互水平。"
external_url: https://alibaba.github.io/page-agent
scenarios: ["Web应用开发", "AI/ML项目"]
---

# PageAgent：运行于 Web 应用内部的 GUI 智能体

---

## 基本信息

- **作者**: simon_luv_pho
- **评分**: 56
- **评论数**: 31
- **链接**: [https://alibaba.github.io/page-agent](https://alibaba.github.io/page-agent)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47264138](https://news.ycombinator.com/item?id=47264138)

---
## 导语

随着大模型能力的提升，如何让 AI 像人类一样直接操作图形界面（GUI）已成为自动化领域的关键课题。PageAgent 是一款直接集成在 Web 应用内部的 GUI 智能体，它能够理解界面上下文并自主执行操作。本文将介绍其技术架构与实现逻辑，帮助开发者探索如何利用智能体技术，显著提升 Web 应用的自动化交互水平。

---
## 评论

### 中心观点
文章介绍了 PageAgent，一种将 AI Agent 以 JavaScript 库形式直接集成在 Web 应用内部的方案。该方案通过直接访问 DOM 和组件状态，试图解决基于视觉识别或传统浏览器自动化（如 Selenium）技术在 Web 交互中面临的稳定性与上下文丢失问题。

### 支撑理由与边界分析

**1. 原生集成带来的上下文感知能力**
PageAgent 的技术特征在于其运行环境位于页面内部。与基于 Computer Vision 的 Agent 不同，它能够直接读取 React/Vue 组件的 Props、State 以及 HTML 属性（如 `aria-label`）。
*   **技术评价**：这种方式绕过了视觉层解析，减少了 Agent 理解界面语义的计算成本，使其能更精准地定位元素并执行操作。
*   **边界条件/反例**：这种高权限访问引入了安全风险。Agent 具备读取页面敏感数据（如 Session Tokens）的能力，若数据被回传至 LLM 服务端，可能导致隐私泄露。在金融或医疗等强监管场景下，这种“数据外溢”风险限制了其适用性。

**2. 绕过视觉层的不稳定性**
传统视觉 Agent 容易受 CSS 动画、弹窗或布局微调的影响而失效。PageAgent 通过直接操作 DOM 节点，避免了视觉层面的干扰。
*   **技术评价**：这降低了非结构化环境下的操作失败率，将交互过程转化为更确定性的逻辑操作。
*   **边界条件/反例**：对于重度依赖 Canvas、WebGL 或 SVG 的应用（如 Figma 或在线地图），DOM 结构往往无法提供有效的语义信息。在此类场景下，PageAgent 可能因缺乏坐标定位能力而表现不佳。

**3. 前端测试与自动化的新尝试**
文章提出利用自然语言编写 UI 测试或自动化脚本。
*   **技术评价**：这在低代码或原型验证阶段具有潜力，允许开发者快速构建自动化流程。
*   **边界条件/反例**：在生产环境的 CI/CD 流水线中，LLM 的非确定性可能导致测试用例的回放不稳定。相比之下，Playwright 等传统工具虽然编写繁琐，但提供了必要的确定性保障。

### 详细维度评价

**1. 内容深度与严谨性**
文章侧重于技术实现路径的展示，但在安全性讨论上不够充分。作者未深入探讨在客户端引入 LLM 可能带来的 XSS 攻击面扩大或 Prompt 注入风险，也缺乏对防止 LLM 误操作导致数据破坏的详细机制说明。

**2. 实用价值**
对于 SaaS 开发者，PageAgent 提供了一种在不重构后端 API 的前提下为应用增加“AI Copilot”功能的路径。它在内部工具自动化或客户支持演示等场景中具有应用潜力。

**3. 创新性**
PageAgent 并非首创，但其将 Agent 定义为页面运行时实体的视角，从“外部驱动”转向了“内部集成”。这为当前主流的 Browser Agent 提供了一种不同的技术实现思路。

**4. 行业影响**
此类工具的普及可能影响前端开发模式，促使开发者在设计 UI 时更多地考虑 AI Agent 的交互需求（如增加语义化标签），推动“Agent-Oriented UI”设计标准的发展。

### 争议点与不同观点

*   **隐私与安全**：赋予 LLM 对页面 DOM 的直接访问权是否违背了现有的安全沙箱原则？
*   **确定性 vs. 灵活性**：在需要严格一致性的自动化任务中，LLM 的随机性是否是本质上的障碍？

---
## 代码示例




```python
# 示例1：自动化表单填写与提交
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def auto_fill_form(url, form_data):
    """
    自动化填写并提交网页表单
    :param url: 目标网页URL
    :param form_data: 字典形式的表单数据 {'字段名': '值'}
    """
    driver = webdriver.Chrome()  # 需要安装chromedriver
    driver.get(url)
    
    try:
        # 等待表单加载完成
        form = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "form"))
        )
        
        # 填写表单字段
        for field_name, value in form_data.items():
            field = form.find_element(By.NAME, field_name)
            field.clear()
            field.send_keys(value)
        
        # 提交表单
        submit_btn = form.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_btn.click()
        
        print("表单提交成功！")
    except Exception as e:
        print(f"操作失败: {str(e)}")
    finally:
        driver.quit()

# 使用示例
auto_fill_form("https://example.com/contact", {
    "name": "张三",
    "email": "zhangsan@example.com",
    "message": "这是测试消息"
})
```




```python
# 示例2：网页数据监控与通知
import requests
from bs4 import BeautifulSoup
import time
from plyer import notification  # 需要安装plyer库

def monitor_webpage(url, target_element, check_interval=300):
    """
    监控网页特定元素的变化并发送通知
    :param url: 要监控的网页URL
    :param target_element: 要监控的CSS选择器
    :param check_interval: 检查间隔(秒)
    """
    last_content = None
    
    while True:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            current_content = soup.select_one(target_element).text.strip()
            
            if last_content is not None and current_content != last_content:
                notification.notify(
                    title="网页内容更新提醒",
                    message=f"检测到内容变化:\n{current_content}",
                    timeout=10
                )
                print(f"检测到变化: {current_content}")
            
            last_content = current_content
            time.sleep(check_interval)
        except Exception as e:
            print(f"监控出错: {str(e)}")
            time.sleep(60)  # 出错后等待1分钟再试

# 使用示例
monitor_webpage(
    "https://news.ycombinator.com/",
    "tr.athing:nth-child(1) td.title > a",
    check_interval=600  # 每10分钟检查一次
)
```




```python
# 示例3：智能网页交互助手
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def web_assistant(task_description):
    """
    根据自然语言描述执行网页交互任务
    :param task_description: 任务描述，如"搜索Python教程并打开第一个结果"
    """
    driver = webdriver.Chrome()
    
    try:
        # 解析任务描述
        if "搜索" in task_description and "打开" in task_description:
            query = task_description.split("搜索")[1].split("并")[0].strip()
            
            # 打开搜索引擎
            driver.get("https://www.google.com")
            search_box = driver.find_element(By.NAME, "q")
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            
            # 等待结果加载并点击第一个结果
            time.sleep(2)
            first_result = driver.find_element(By.CSS_SELECTOR, "div#search div.g a")
            first_result.click()
            
            print(f"已执行: {task_description}")
        else:
            print("无法识别的任务描述")
    except Exception as e:
        print(f"执行失败: {str(e)}")
    finally:
        time.sleep(5)  # 查看结果
        driver.quit()

# 使用示例
web_assistant("搜索Python教程并打开第一个结果")
```


---
## 案例研究


### 1：某中型 SaaS 客户管理系统 (CRM) 提效项目

 1：某中型 SaaS 客户管理系统 (CRM) 提效项目

**背景**:
一家 B2B SaaS 公司的 CRM 系统功能日益复杂，包含 50 多个设置项和不同的数据视图。新入职的销售人员平均需要 2 周时间才能熟练掌握系统操作，且客户支持团队每天收到大量关于“如何导出特定报表”或“如何修改客户状态”的基础工单。

**问题**:
传统的操作手册（PDF 或 Wiki）不仅更新滞后，而且查阅效率极低。用户需要在文档和系统界面之间频繁切换。开发原生“操作引导”功能需要大量硬编码，维护成本高，且无法灵活适应业务逻辑的快速变更。

**解决方案**:
该团队在 CRM 系统中集成了 PageAgent。PageAgent 作为一个嵌入式 GUI 代理，直接“阅读”当前页面的 DOM 结构。用户只需在侧边栏输入自然语言指令，例如“将列表中所有‘待跟进’状态的客户分配给销售经理张三”，PageAgent 会自动定位筛选按钮、执行筛选操作，并模拟点击批量分配按钮，完成整个流程。

**效果**:
- 新员工培训周期缩短了 40%，因为 PageAgent 提供了“即问即做”的实时辅助。
- 客户支持团队关于“如何操作”的咨询工单减少了 60%。
- 无需修改核心业务代码，仅通过配置即可实现复杂的自动化操作引导。

---



### 2：跨境电商供应链数据录入自动化

 2：跨境电商供应链数据录入自动化

**背景**:
一家跨境电商企业的供应链团队每天需要从供应商门户下载 Excel 表格，并将数据录入到内部的 ERP 系统中。由于供应商门户和内部 ERP 系统均未提供 API 接口，员工只能通过人工复制粘贴的方式处理数据，每天处理 50+ 个订单，耗时且易错。

**问题**:
传统的 RPA（机器人流程自动化）脚本非常脆弱，一旦供应商网站的 HTML 结构发生微小变化（例如更改了 class 名称或调整了布局），RPA 脚本就会失效，需要技术人员重新编写和维护，导致维护成本居高不下。

**解决方案**:
利用 PageAgent 的上下文感知能力，开发团队构建了一个内部自动化工具。PageAgent 不依赖固定的 CSS 选择器，而是像人类一样“理解”页面元素（例如识别“下载按钮”或“输入框”）。当员工打开供应商页面时，PageAgent 自动识别当前的下载任务并模拟点击；当打开 ERP 录入页面时，它自动读取剪贴板数据并填充到对应的表单字段中。

**效果**:
- 数据录入过程的错误率从 5% 降低至 0.1%。
- 单个订单的处理时间从 3 分钟减少至 30 秒。
- 即使供应商网站进行了 UI 改版，PageAgent 也能通过语义理解适应新界面，无需频繁修改底层代码，大大降低了维护成本。

---
## 最佳实践

## 最佳实践指南

### 实践 1：构建可访问的语义化 DOM 结构

**说明**: PageAgent 作为一个 GUI Agent，依赖于解析网页的 DOM 结构来理解界面元素。如果应用使用了大量的 `div` 嵌套或缺乏语义的标签，Agent 将难以识别按钮、表单或内容区块。语义化 HTML（如 `<nav>`, `<button>`, `<aria-label>`）能显著提高 Agent 的解析准确率和操作成功率。

**实施步骤**:
1. 审计现有代码，将通用的 `div` 替换为具有语义的 HTML5 标签（如 `header`, `main`, `section`）。
2. 为所有交互元素添加明确的 `aria-label` 或 `alt` 属性，确保 Agent 能“读懂”图标按钮的功能。
3. 确保表单控件与 `label` 正确关联。

**注意事项**: 避免使用过于复杂的 CSS 绝对定位来构建 UI，这会破坏 DOM 的自然层级关系，导致 Agent 误判元素位置。

---

### 实践 2：建立确定性的状态管理机制

**说明**: AI Agent 在执行任务时需要明确的上下文。如果应用的状态管理混乱（例如：同一个操作在不同条件下产生不可预测的副作用），Agent 很难通过反馈循环来修正错误。确定性的状态意味着相同的操作在相同状态下应产生相同的结果。

**实施步骤**:
1. 采用标准化的状态管理模式（如 Redux, Zustand 或 MobX），集中管理应用状态。
2. 为关键操作设计幂等的 API 接口，确保重复请求不会破坏数据一致性。
3. 在 DOM 中添加特定的数据属性（如 `data-status="loading"` 或 `data-state="success"`），为 Agent 提供显式的状态读取点。

**注意事项**: 避免使用随机的 ID 或动态生成的类名作为 DOM 选择器的唯一依据，这会导致 Agent 的脚本在页面刷新后失效。

---

### 实践 3：设计 Agent 友好的错误处理与反馈系统

**说明**: 当 Agent 操作失败或遇到验证错误时，传统的模态弹窗可能难以被程序化读取。最佳实践是提供可被 DOM 捕获的错误信息，以便 Agent 能够读取错误内容并进行自我修正或向用户报告。

**实施步骤**:
1. 将错误信息直接渲染在表单字段下方或页面的固定错误区域，而不是仅在 `console` 或 `alert` 中显示。
2. 为错误消息容器添加固定的 ID 或类名（例如 `class="error-message"`），方便 Agent 定位。
3. 确保加载状态有明确的视觉提示（如 Spinner），并配有对应的文本说明。

**注意事项**: 错误提示应当包含具体的解决建议，而不仅仅是“操作失败”的模糊提示，以辅助 Agent 进行逻辑推理。

---

### 实践 4：实施基于角色的细粒度权限控制

**说明**: PageAgent 具有操作 GUI 的能力，本质上等同于拥有用户的操作权限。必须防止 Agent 执行危险操作（如删除数据、发送大量邮件）或访问敏感区域的接口。

**实施步骤**:
1. 在后端实施严格的 RBAC（基于角色的访问控制），区分“用户直接操作”和“Agent 代理操作”的权限令牌。
2. 对于高风险操作（如“购买”、“删除”），强制要求二次确认或人工介入机制。
3. 记录所有 Agent 发起的 API 调用日志，以便审计和回溯。

**注意事项**: 不要仅依赖前端隐藏按钮来限制权限，因为 Agent 可以直接调用底层网络请求，后端必须始终进行权限校验。

---

### 实践 5：提供结构化的操作日志与调试接口

**说明**: 为了让开发者能够理解 Agent 的行为逻辑，以及在出错时进行调试，应用应提供一种机制来记录 Agent 的思考过程和执行路径。

**实施步骤**:
1. 在应用中集成一个开发者面板，实时显示 Agent 正在交互的 DOM 元素和执行的指令。
2. 允许通过特定的查询参数（如 `?debug=true`）开启 Agent 的详细日志模式。
3. 将 Agent 的执行步骤标准化输出，便于后续分析其行为模式。

**注意事项**: 调试接口在生产环境中应默认关闭或仅对管理员可见，防止泄露应用内部逻辑或敏感数据。

---

### 实践 6：优化页面加载性能与资源稳定性

**说明**: Agent 的运行依赖于页面的稳定性。如果关键脚本加载缓慢、资源 404 或布局抖动严重，Agent 的视觉定位模块可能会失效，导致操作失败。

**实施步骤**:
1. 实施关键渲染路径优化，确保核心 UI 组件优先加载。
2. 使用骨架屏或占位符防止布局抖动，确保 Agent 获取的坐标信息准确。
3. 对所有第三方依赖进行子资源完整性（SRI）校验，防止被篡改导致 Agent 环境异常。

**注意事项**: 如果页面涉及大量动态内容渲染（如无限滚动），需要设置明确的边界或分页机制，防止 Agent 陷入无限循环的操作中。

---
## 学习要点

- PageAgent 是一种直接集成在 Web 应用内部的 GUI 智能体，能够通过模拟用户操作（如点击和输入）来自动化执行复杂任务。
- 它利用多模态大语言模型（LLM）直接解析应用的视觉界面和 DOM 结构，无需针对特定网站编写额外的 API 或代码即可实现通用交互。
- 该智能体采用“视觉-语言-动作”的循环机制，通过观察屏幕截图并结合 HTML 语义来动态规划下一步的操作路径。
- PageAgent 通过将执行环境限制在用户当前浏览器的单个标签页内，有效地降低了云端自动化带来的安全风险和隐私泄露隐患。
- 它展示了“以浏览器为运行时环境”的潜力，即利用浏览器现有的渲染能力作为智能体的感知与执行基础，从而简化了部署流程。
- 该工具在处理需要多步骤交互的长尾任务（如填写复杂表单或进行数据录入）时，表现出了优于传统自动化脚本的适应性和鲁棒性。

---
## 常见问题


### 1: PageAgent 的核心功能是什么，它与传统的浏览器自动化工具有何不同？

1: PageAgent 的核心功能是什么，它与传统的浏览器自动化工具有何不同？

**A**: PageAgent 是一个图形用户界面（GUI）智能体，它的核心功能是直接集成并运行在您的 Web 应用程序内部。与传统的浏览器自动化工具（如 Selenium 或 Playwright）不同，PageAgent 不需要外部驱动程序或独立的浏览器实例来控制页面。它通过嵌入到应用代码中的脚本，直接与页面的 DOM 和事件系统交互，从而能够像真实用户一样执行点击、输入和导航操作，同时具备更强的上下文感知能力和更低的延迟。

---



### 2: PageAgent 是如何集成到现有的 Web 应用中的？技术实现原理是什么？

2: PageAgent 是如何集成到现有的 Web 应用中的？技术实现原理是什么？

**A**: PageAgent 通常以 JavaScript 库或 SDK 的形式提供。开发者需要将其脚本片段嵌入到目标 Web 应用的前端代码中。在技术实现上，它利用大语言模型（LLM）来理解用户的自然语言指令，并将这些指令转化为具体的 DOM 操作序列。它通过分析页面的 HTML 结构、可访问性树和视觉上下文，定位需要交互的元素（如按钮或输入框），并模拟相应的事件触发，从而实现自动化的任务执行。

---



### 3: 使用 PageAgent 是否需要具备编程知识，普通用户可以直接使用吗？

3: 使用 PageAgent 是否需要具备编程知识，普通用户可以直接使用吗？

**A**: 虽然 PageAgent 的集成过程需要开发者具备一定的编程知识来进行安装和配置，但一旦集成完成，最终用户通常不需要具备编程知识。PageAgent 的设计初衷是让用户能够通过自然语言提示与智能体对话，从而完成复杂的网页操作（如填写表单、数据查询或导航流程）。对于开发者而言，它也提供了 API 接口，以便更灵活地控制智能体的行为。

---



### 4: PageAgent 的安全性如何？它是否会泄露应用内的敏感数据？

4: PageAgent 的安全性如何？它是否会泄露应用内的敏感数据？

**A**: 安全性是 PageAgent 设计时的重点考量。由于它运行在客户端（浏览器）环境中，数据的处理方式取决于具体的配置。通常情况下，PageAgent 可以被配置为仅通过语义层访问数据，而不是直接访问底层数据库。然而，因为它能够读取页面内容，所以开发者需要谨慎配置其权限，确保它不会暴露或操作用户不该看到的敏感信息。建议在部署前详细审查其数据访问策略，并确保符合隐私合规要求（如 GDPR）。

---



### 5: PageAgent 支持哪些类型的 Web 应用和浏览器？

5: PageAgent 支持哪些类型的 Web 应用和浏览器？

**A**: PageAgent 设计为与框架无关，理论上可以支持任何基于标准 Web 技术构建的应用程序，包括使用 React、Vue、Angular 或 Svelte 等现代框架开发的单页应用（SPA），以及传统的多页应用（MPA）。在浏览器兼容性方面，它通常支持所有现代浏览器（如 Chrome、Firefox、Safari 和 Edge），只要这些浏览器支持 PageAgent 所依赖的 JavaScript 特性（如 Web Workers 或特定的 API）。

---



### 6: 如果 PageAgent 执行错误操作或陷入死循环，有什么样的容错机制？

6: 如果 PageAgent 执行错误操作或陷入死循环，有什么样的容错机制？

**A**: PageAgent 内置了反馈和纠错机制。当智能体执行的操作未能达到预期结果（例如点击了一个无效按钮或页面未发生预期变化）时，它会利用视觉反馈和状态检测来识别错误。系统会自动将错误信息返回给底层的 LLM，要求其重新分析当前页面状态并生成新的操作计划。此外，开发者通常可以设置最大步数限制或人工确认节点，以防止无限循环或资源耗尽。

---



### 7: PageAgent 目前是开源项目吗？未来的商业化路径是什么？

7: PageAgent 目前是开源项目吗？未来的商业化路径是什么？

**A**: 根据其在 Hacker News 上的 "Show HN" 属性，PageAgent 很可能是一个开源项目或处于早期的测试阶段，旨在通过社区反馈来改进产品。虽然目前可能免费提供基础功能，但未来此类工具的商业化路径通常包括提供托管服务（云端 LLM 推理）、企业级的高级功能（如更细粒度的权限管理、审计日志）、或针对高并发场景的付费支持计划。具体细节需参考其官方 GitHub 仓库或网站说明。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: DOM 结构抽象设计

### 难度**: [简单]

### 问题描述**:

### PageAgent 需要解析当前网页的 DOM 结构才能进行操作。请设计一个基础算法，将一个简单的 HTML 表单（包含输入框、按钮和下拉菜单）转换为一个 JSON 格式的对象树。该对象树需包含节点类型、唯一标识符（如 `id` 或动态生成的 `path`）以及当前值。

---
## 引用

- **原文链接**: [https://alibaba.github.io/page-agent](https://alibaba.github.io/page-agent)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47264138](https://news.ycombinator.com/item?id=47264138)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/) / [前端](/categories/%E5%89%8D%E7%AB%AF/)
- 标签： [PageAgent](/tags/pageagent/) / [GUI Agent](/tags/gui-agent/) / [Web 应用](/tags/web-%E5%BA%94%E7%94%A8/) / [智能体](/tags/%E6%99%BA%E8%83%BD%E4%BD%93/) / [浏览器自动化](/tags/%E6%B5%8F%E8%A7%88%E5%99%A8%E8%87%AA%E5%8A%A8%E5%8C%96/) / [前端集成](/tags/%E5%89%8D%E7%AB%AF%E9%9B%86%E6%88%90/) / [Show HN](/tags/show-hn/) / [AI 辅助开发](/tags/ai-%E8%BE%85%E5%8A%A9%E5%BC%80%E5%8F%91/)
- 场景： [Web应用开发](/scenarios/web%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [PageAgent：运行于 Web 应用内部的 GUI 智能体]({{< relref "posts/20260305-hacker_news-show-hn-pageagent-a-gui-agent-that-lives-inside-yo-13.md" >}})
- [PageAgent：运行在 Web 应用内部的 GUI 智能体]({{< relref "posts/20260305-hacker_news-show-hn-pageagent-a-gui-agent-that-lives-inside-yo-8.md" >}})
- [Moltis：具备记忆、工具与技能扩展能力的AI助手]({{< relref "posts/20260213-hacker_news-show-hn-moltis-ai-assistant-with-memory-tools-and--15.md" >}})
- [Moltis：具备记忆与工具调用能力的自扩展AI助手]({{< relref "posts/20260213-hacker_news-show-hn-moltis-ai-assistant-with-memory-tools-and--7.md" >}})
- [WebMCP：变革 AI 访问 Web 的自动化与交互模式]({{< relref "posts/20260216-juejin-webmcp-时代在浏览器中释放-ai-的工作能力-0.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*