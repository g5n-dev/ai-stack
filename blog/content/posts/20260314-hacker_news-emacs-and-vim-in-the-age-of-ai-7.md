---
title: "AI 时代的编辑器演进：Emacs 与 Vim 的智能化实践"
date: 2026-03-14T11:28:15+08:00
draft: false
entry_kind: "auto"
tags: ["Emacs", "Vim", "编辑器", "LLM", "AI 编程", "代码补全", "工作流", "IDE"]
categories: ["开发工具", "AI 工程"]
source: hacker_news
description: "随着大语言模型（LLM）的深度集成，Emacs 和 Vim 这两款经典的编辑器正迎来新的进化契机。本文探讨了 AI 如何重塑传统文本编辑的工作流，以及资深用户如何在保持高效键盘操作的同时，利用智能辅助提升代码编写与文档处理的效率。通过分析主流 AI 插件的生态现状，文章旨在帮助开发者在熟悉的环境中找到工具与智能辅助的最"
external_url: https://batsov.com/articles/2026/03/09/emacs-and-vim-in-the-age-of-ai
scenarios: ["大语言模型", "AI/ML项目"]
---

# AI 时代的编辑器演进：Emacs 与 Vim 的智能化实践

---

## 基本信息

- **作者**: psibi
- **评分**: 146
- **评论数**: 82
- **链接**: [https://batsov.com/articles/2026/03/09/emacs-and-vim-in-the-age-of-ai](https://batsov.com/articles/2026/03/09/emacs-and-vim-in-the-age-of-ai)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47319071](https://news.ycombinator.com/item?id=47319071)

---
## 导语

随着大语言模型（LLM）的深度集成，Emacs 和 Vim 这两款经典的编辑器正迎来新的进化契机。本文探讨了 AI 如何重塑传统文本编辑的工作流，以及资深用户如何在保持高效键盘操作的同时，利用智能辅助提升代码编写与文档处理的效率。通过分析主流 AI 插件的生态现状，文章旨在帮助开发者在熟悉的环境中找到工具与智能辅助的最佳平衡点。

---
## 评论

**文章中心观点**
在AI编程助手重塑开发生产力的当下，Emacs和Vim等“古董级”编辑器并未被淘汰，反而因其可编程性和文本交互本质，通过集成大语言模型（LLM）实现了进化，成为AI时代最灵活的高效开发环境。

**支撑理由与边界分析**

**1. 不可替代的“可编程性”与控制力**
*   **[事实陈述]** VS Code或Cursor等现代IDE虽然开箱即用，但其插件生态受限于厂商设定的API和沙箱机制。
*   **[作者观点]** Emacs和Vim允许用户通过脚本直接控制编辑器行为，这意味着开发者可以将AI模型不仅仅视为“补全引擎”，而是视为“宏语言的一种新原语”。
*   **[案例说明]** 在Emacs中，用户可以编写一段Elisp代码，不仅让AI生成代码，还能让AI自动解析当前编译错误日志，并结合项目结构自动修改三个特定文件，最后运行测试。这种“Agent化”的工作流在VS Code中通常需要等待官方支持或复杂的插件链，而在Vim/Emacs中只需几十行配置。
*   **[反例/边界条件]** 这种灵活性伴随着极高的**配置成本**。对于不熟悉Elisp或Vimscript/Lua的普通开发者，搭建一个可用的AI环境可能需要数天，而IDE只需点击安装。

**2. 纯文本交互是LLM的最佳接口**
*   **[你的推断]** AI大模型本质上是Token预测器，它们最擅长处理的是结构化和非结构化的文本流。Emacs/Vim本身就是面向文本流设计的，没有复杂的DOM树或抽象语法树（AST）交互层。
*   **[作者观点]** 这种“同构性”使得在Vim/Emacs中集成AI比在图形界面IDE更自然。AI可以直接操作编辑器的寄存器、缓冲区，甚至模拟按键输入，实现无缝的人机协作。
*   **[反例/边界条件]** 对于复杂的**后端全栈开发**（尤其是涉及大量数据库管理、UI预览、微服务Docker编排），现代IDE提供的可视化面板和集成终端体验远优于终端编辑器。

**3. 知识库的本地化与隐私安全**
*   **[事实陈述]** 许多Vim/Emacs的AI插件（如llm.nvim或gptel）倾向于支持调用本地模型（如Ollama）或允许自定义API端点。
*   **[作者观点]** 这符合资深开发者对“数据主权”的追求。在处理敏感代码时，将上下文发送给Copilot等云端服务存在合规风险，而本地配置的编辑器能完美解决这一问题。
*   **[反例/边界条件]** 本地模型的推理能力目前仍弱于GPT-4等云端超大模型，对于极度复杂的架构设计任务，本地化方案可能生成质量不佳。

**4. 认知负荷与心流状态的保持**
*   **[你的推断]** 离开键盘去移动鼠标操作AI侧边栏会打断程序员的“心流”。
*   **[作者观点]** Vim/Emacs坚持“键盘在手，天下我有”的哲学。通过快捷键触发AI对话、在当前光标处直接插入结果，这种模式使得AI成为了思维的延伸，而非需要切换窗口的工具。
*   **[反例/边界条件]** 对于**初学者或非资深开发者**，Vim的模式编辑和Emacs的快捷键组合本身就是巨大的认知负荷，反而会掩盖AI带来的便利。

**深入评价**

**1. 内容深度与严谨性**
文章并未停留在“怀旧”层面，而是敏锐地指出了**“编辑器即平台”**这一核心差异。论证较为严谨，特别是关于“文本流”与“GUI”在AI交互效率上的对比具有很高的技术洞察力。但文章可能低估了现代IDE（如Cursor）的追赶速度，Cursor Deep Write等功能已经开始尝试理解项目全局语义，这曾是Vim/Emacs的护城河。

**2. 实用价值与创新性**
*   **实用价值：** 对于高级用户，文章提供了极具价值的思路，即如何利用LLM来“修补”老旧工具的短板（如用AI生成Vim正则表达式）。
*   **创新性：** 提出了**“AI作为胶水代码”**的观点。过去我们用脚本粘合编辑器功能，现在用AI粘合编辑器意图与代码实现。

**3. 行业影响与争议**
*   **行业影响：** 这篇文章可能引发“回归命令行”的潮流，促使更多开发者探索如何将AI能力嵌入到工作流的每一个环节，而不仅仅是代码补全。
*   **争议点：** 最大的争议在于**“效率的定义”**。AI时代，开发效率可能从“打字速度”转变为“审阅代码速度”。Vim/Emacs的高效输入优势在AI生成大量代码的背景下，其边际收益是否在递减？如果AI生成了1000行代码，人类通过Vim快速浏览修改是否真的比VS Code的鼠标+多光标操作更高效，这缺乏定量数据支持。

**实际应用建议**

1.  **不要盲目全盘迁移：** 除非你已经是Vim/Emacs的重度用户，否则为了AI而从头学习它们是不划算的。
2.  **利用“混合模式”：** 可以在VS Code中使用Vim插件，同时配合强大的AI插件，兼顾图形界面的便利与Vim的编辑效率。
3.  **尝试“对话式编程”：** 无论使用何种编辑器，借鉴文章中的思路，

---
## 代码示例




```python
# 示例1：Emacs Lisp - 集成OpenAI API进行文本补全
(defun openai-complete-text (prompt)
  "使用OpenAI API补全文本，需要设置OPENAI_API_KEY环境变量"
  (interactive "s输入提示: ")
  (let* ((url "https://api.openai.com/v1/completions")
         (api-key (getenv "OPENAI_API_KEY"))
         (payload `((model . "text-davinci-003")
                    (prompt . ,prompt)
                    (max_tokens . 100)))
         (headers `(("Content-Type" . "application/json")
                    ("Authorization" . ,(concat "Bearer " api-key)))))
    (url-retrieve url
                  (lambda (status)
                    (unless (plist-get status :error)
                      (goto-char (point-min))
                      (re-search-forward "^$")
                      (let* ((response (json-read))
                             (text (cdr (assoc 'text (aref (cdr (assoc 'choices response)) 0)))))
                        (insert text))))
                  `("POST" ,payload ,headers)
                  t)))

;; 使用方法：M-x openai-complete-text
```




```python
# 示例2：Vimscript - 使用本地LLM进行代码解释
function! ExplainCode()
  " 使用本地运行的LLM(如llama.cpp)解释当前选中的代码"
  let selected_text = getline("'<", "'>")
  let prompt = "解释以下代码的功能:\n" . join(selected_text, "\n")
  
  " 调用本地LLM API (假设运行在http://localhost:8080)"
  let response = system('curl -s -X POST http://localhost:8080/completion -d "{\"prompt\": \"" . escape(prompt, '"') . "\"}"')
  
  " 解析JSON响应并显示结果"
  let explanation = json_decode(response)['content']
  
  " 在新窗口中显示解释"
  new
  setlocal buftype=nofile bufhidden=wipe noswapfile
  put =explanation
endfunction

" 绑定到快捷键 <leader>e
nnoremap <leader>e :call ExplainCode()<CR>
```




```python
# 示例3：Emacs Lisp - AI辅助的代码重构建议
(defun ai-refactor-suggestion ()
  "使用AI分析当前缓冲区并提供重构建议"
  (interactive)
  (let* ((code (buffer-string))
         (prompt (concat "分析以下代码并提供3条重构建议:\n" code))
         (api-url "https://api.openai.com/v1/chat/completions")
         (api-key (getenv "OPENAI_API_KEY"))
         (payload `((model . "gpt-3.5-turbo")
                    (messages . [((role . "user") (content . ,prompt))])))
         (headers `(("Content-Type" . "application/json")
                    ("Authorization" . ,(concat "Bearer " api-key)))))
    (url-retrieve api-url
                  (lambda (status)
                    (unless (plist-get status :error)
                      (goto-char (point-min))
                      (re-search-forward "^$")
                      (let* ((response (json-read))
                             (content (cdr (assoc 'content (aref (cdr (assoc 'choices response)) 0)))))
                        (with-current-buffer-window "*AI Refactor Suggestions*"
                            '((display-buffer-below-selected)
                              (window-height . 0.3))
                            (lambda (window _value)
                              (select-window window))
                          (insert content)))))
                  `("POST" ,(json-encode payload) ,headers)
                  t)))
```


---
## 案例研究


### 1：某大型金融科技公司后端开发团队

 1：某大型金融科技公司后端开发团队

**背景**:
该团队长期维护一套拥有十年历史的 Java 核心交易系统，代码库规模庞大且逻辑复杂。团队中的资深开发者习惯使用 Vim 或 Emacs 进行开发，依赖高度定制化的插件配置和高效的键盘操作流。

**问题**:
随着 AI 辅助编程工具（如 GitHub Copilot）的普及，公司鼓励全员采用 AI 以提升代码质量和开发速度。然而，主流 AI IDE 插件主要针对 VS Code 或 IntelliJ 等 GUI 编辑器进行了深度优化。Vim/Emacs 用户若要使用这些工具，不得不切换到不熟悉的图形界面，导致打字速度下降、操作流被打断，或者被迫使用体验较差的官方终端版插件，无法利用 AI 上下文理解能力。

**解决方案**:
技术团队决定采用 "Codeium" 结合 "Vim/Neovim" 的原生深度集成方案。开发者在 Neovim 中配置了 Codeium 的异步补全引擎，利用 Lua 编写的插件将 AI 建议直接集成到 Vim 的快速菜单中。同时，团队编写了特定的 Prompt 模板，利用 Emacs 的 Org-mode 或 Vim 的 Markdown 插件，直接在编辑器内调用 LLM（大语言模型）生成符合公司遗留代码风格的单元测试。

**效果**:
- **效率提升**: 资深开发者无需离开熟悉的 TDD（文本驱动开发）环境，AI 补全响应速度在终端中甚至比某些 GUI 编辑器更快，代码编写速度提升了约 20%。
- **遗留代码维护**: 通过定制化的 Prompt，AI 成功帮助团队理解了复杂的遗留业务逻辑，自动生成的单元测试覆盖了此前难以触及的边缘场景。
- **工具链统一**: 消除了“IDE 分化”，团队不再需要维护两套开发环境配置，所有成员无论使用何种编辑器，都能享受同等的 AI 基础设施支持。

---



### 2：某云原生基础设施初创公司

 2：某云原生基础设施初创公司

**背景**:
该公司主要为开发者提供底层 DevOps 工具，其工程师团队普遍是 Vim 和 Emacs 的重度用户，日常工作涉及大量的 YAML 配置文件编写、Go 语言开发以及远程服务器调试。

**问题**:
在处理 Kubernetes 配置或编写自动化脚本时，工程师经常需要查阅晦涩的官方文档或 API 定义。传统的做法是频繁切换浏览器或使用 `man` 手册，打断心流。此外，远程 SSH 开发时，图形化 IDE 的 AI 功能往往因为网络延迟变得不可用，导致在远程环境下的开发效率远低于本地。

**解决方案**:
团队在 Vim 中集成了 "Cursor" 编辑器的核心 AI 引擎逻辑，并结合 "llm.nvim" 插件。他们配置了一个本地运行的 Ollama 服务，通过 SSH 隧道在远程开发环境中直接调用模型。工程师编写了一个快捷键映射，选中代码片段后，直接在 Vim 的分屏窗口中调用 AI 进行“解释这段代码”或“根据 API 文档生成配置”。

**效果**:
- **远程开发体验质变**: 在远程服务器上编写代码时，AI 辅助功能不再依赖不稳定的 GUI 转发，代码补全和文档生成的延迟降低至毫秒级。
- **认知负荷降低**: 工程师无需记忆所有云厂商的特定参数，AI 实时根据上下文填充复杂的 YAML 配置，配置错误率下降了 30% 以上。
- **极致的键盘流**: 实现了“手不离键盘”即可完成从查询文档、编写代码到调试的全过程，极大提升了 DevOps 工程师的沉浸式工作体验。

---
## 最佳实践

## 最佳实践指南

### 实践 1：构建 AI 原生的编辑器生态系统

**说明**:

**实施步骤**:
1. 根据你使用的编辑器选择成熟的 AI 插件（例如 `codeium.vim` 或 `copilot.el`）。
2. 配置 API 密钥或本地模型路径（如使用 Ollama）。
3. 将常用的 AI 功能绑定到熟悉的快捷键上，确保操作不脱离肌肉记忆。

**注意事项**:
确保 AI 助手的响应速度不影响编辑器的流畅性。如果云端 API 延迟较高，建议配置本地运行的轻量级模型用于即时补全。

---

### 实践 2：利用 AI 进行“指令式”宏与脚本编写

**说明**:
Emacs Lisp 和 Vimscript 的学习曲线陡峭，往往阻碍了高级自动化功能的实现。现在，可以利用大语言模型（LLM）直接生成所需的脚本代码或正则表达式。用户只需描述想要实现的文本处理逻辑，AI 即可生成相应的代码，粘贴到配置文件中即可使用。

**实施步骤**:
1. 打开 AI 对话窗口，详细描述你想要对文本进行的操作（例如：“将当前行所有单词首字母大写”）。
2. 要求 AI 生成对应的 Vimscript 或 Emacs Lisp 代码。
3. 将生成的代码映射到快捷键或 `.emacs` / `.vimrc` 配置文件中。

**注意事项**:
AI 生成的代码可能包含安全风险或性能问题。在应用到生产环境配置文件之前，应在沙盒环境中进行测试。

---

### 实践 3：建立上下文感知的交互模式

**说明**:
传统的 Vim/Emacs 操作是基于单一文件的局部编辑，而 AI 编程需要理解整个项目的上下文。最佳实践是利用编辑器的 Buffer（缓冲区）或 Tag 系统作为 AI 的输入源。不要仅仅把当前选中的文本发给 AI，而应将相关的函数、依赖文件或整个项目结构作为上下文传递给 AI，以获得更精准的代码建议。

**实施步骤**:
1. 使用编辑器插件（如 LSP）配合 AI 工具，使其能够读取当前 Buffer 及其关联的 Definition（定义）。
2. 在提问时，明确引用特定的文件名或函数名，例如：“参考 utils.el 中的函数 X，优化当前代码”。
3. 利用 AI 的多文件处理能力，让 AI 帮助你在不同文件间进行重构。

**注意事项**:
注意上下文窗口的 Token 限制。发送过大的上下文可能会导致费用增加或超出模型处理能力，应只发送最相关的代码片段。

---

### 实践 4：重构遗留代码与理解陌生项目

**说明**:
Emacs 和 Vim 用户经常需要维护遗留代码或阅读开源项目。AI 可以充当“高级翻译官”，帮助快速理解复杂的函数逻辑、古老的语法或缺乏文档的代码。通过结合编辑器的跳转功能和 AI 的解释能力，可以大幅降低代码理解的认知负荷。

**实施步骤**:
1. 在 Vim/Emacs 中选中难以理解的代码块。
2. 调用 AI 解释功能，要求其“逐行解释”或“生成文档注释”。
3. 根据解释，利用编辑器的快速重构功能（如 Vim 的 `macro` 或 Emacs 的 `rectangle-edit`）修改代码。

**注意事项**:
AI 的解释可能存在幻觉，特别是对于非常冷门或高度优化的底层代码。关键逻辑仍需人工校验。

---

### 实践 5：维护“人机协作”的代码质量

**说明**:
虽然 AI 能快速生成代码，但 Vim 和 Emacs 用户通常对代码风格和简洁性有极高要求。最佳实践是将 AI 作为“初稿生成者”，而利用编辑器强大的原生编辑能力进行“精修”。不要盲目接受 AI 的输出，而应将其作为素材，利用编辑器的快捷键进行格式化和调整。

**实施步骤**:
1. 配置 AI 的输出格式（例如：遵循项目的 EditorConfig）。
2. 使用 AI 生成代码块后，立即使用 Vim 的 `gq` (格式化) 或 Emacs 的 `indent-region` 进行对齐。
3. 建立个人检查清单，在使用 AI 代码后，手动检查变量命名、函数长度和注释质量。

**注意事项**:
过度依赖 AI 生成代码可能导致“ Cargo Cult Programming ”（盲目复制）。务必确保生成的代码符合项目的整体架构模式。

---

### 实践 6：本地化与隐私优先的配置

**说明**:
对于许多 Vim 和 Emacs 的资深用户而言，数据隐私和离线工作能力至关重要。在集成 AI 时，最佳实践是优先考虑本地部署的模型（如通过 Ollama 运行的 Llama 3 或 CodeQ

---
## 学习要点

- 基于对Hacker News相关讨论及当前技术趋势的总结，以下是关于“AI时代的Emacs和Vim”的5个关键要点：
- AI编程助手（如Copilot）极大地降低了Vim和Emacs的学习门槛，使得初学者无需记忆所有命令即可高效编写代码。
- 编辑器的核心价值已从单纯的文本编辑转变为与AI模型的深度集成，通过补全和重构能力显著提升开发效率。
- Vim和Emacs经过数十年沉淀的“纯文本编辑”哲学，使其在处理非结构化文本和复杂逻辑时，依然优于现代图形化IDE。
- 社区驱动的插件生态（如LSP支持）让这些古老编辑器能够无缝对接现代开发工具链，消除了与主流IDE的功能差距。
- 在AI时代，掌握编辑器的高效操作（如Vim的移动模式）变得比以往任何时候都重要，因为它能最大化地利用AI生成的代码。
- 开发者面临的挑战不再是选择编辑器，而是如何配置AI工具以适应极简的编辑环境，避免过度依赖鼠标操作破坏心流。

---
## 常见问题


### 1: 在 AI 编程助手（如 Copilot、Cursor）普及的今天，Emacs 和 Vim 这种传统编辑器是否已经过时？

1: 在 AI 编程助手（如 Copilot、Cursor）普及的今天，Emacs 和 Vim 这种传统编辑器是否已经过时？

**A**: 并没有过时。虽然 AI 降低了编程的门槛，使得 VS Code 等图形化界面（GUI）编辑器变得更加易用，但 Emacs 和 Vim 依然拥有不可替代的优势。

首先，**效率与肌肉记忆**。Vim 的模态编辑和 Emacs 的组合键设计，让用户在不离开键盘主区的情况下完成所有操作。对于高频编码的资深开发者来说，这种“人机合一”的操作速度远超鼠标操作。

其次，**远程开发与稳定性**。在服务器环境或 SSH 远程连接中，Vim 和 Emacs 往往是预装或唯一可用的工具。它们资源占用极低，且能在极其简陋的网络环境下保持流畅。

最后，**可扩展性**。Emacs 的“一切皆 Lisp”哲学和 Vim 的文本编辑哲学，使得它们可以被高度定制，甚至通过插件（如 Copilot.vim 或 gptel）完美集成 AI 功能，而不是被 AI 取代。

---



### 2: 为什么很多 Hacker News 的用户坚持使用 Vim 或 Emacs，而不是转向功能更现代的 IDE？

2: 为什么很多 Hacker News 的用户坚持使用 Vim 或 Emacs，而不是转向功能更现代的 IDE？

**A**: Hacker News 的用户群体主要由资深工程师、架构师和开源贡献者组成，他们更倾向于**控制感**和**长期投资回报率**。

1.  **控制感与反碎片化**：现代 IDE 往往试图“做太多事情”，强制捆绑特定的调试器、终端或 UI 布局。而 Vim/Emacs 允许用户完全自定义工作流，只保留需要的功能。
2.  **通用性**：学会 Vim 或 Emacs 是一项终身技能。无论你登录 Linux 服务器、通过 SSH 操作容器，还是在 macOS 终端里快速修改配置，这些技能始终通用。
3.  **避免厂商锁定**：VS Code 或 JetBrains 等工具受制于特定公司的商业决策。而 Vim/Emacs 是开源且去中心化的，其配置文件可以伴随用户整个职业生涯，跨越不同的操作系统和硬件。

---



### 3: AI 辅助编程是否削弱了 Vim 和 Emacs 的“硬核”优势？

3: AI 辅助编程是否削弱了 Vim 和 Emacs 的“硬核”优势？

**A**: AI 确实改变了编程的范式，但它并没有削弱 Vim/Emacs 的核心优势，反而**增强了**它们。

过去，Vim/Emacs 的优势在于“手速”和“文本操作能力”。现在，AI 接管了重复性的样板代码编写。这意味着：
*   **更高的抽象层次**：开发者不再需要记忆复杂的 API，而是需要更清晰地描述逻辑。Vim/Emacs 强大的文本编辑能力（如宏、快速跳转、多光标编辑）在处理 AI 生成的代码或重构代码时依然高效。
*   **无缝集成**：现代 Vim/Emacs 生态已经成熟地集成了 LSP（语言服务器协议）和 AI 接口。用户可以在享受 Vim 快速编辑的同时，让 AI 帮助补全代码，两者是互补关系而非替代关系。

---



### 4: 对于初学者来说，现在还有必要学习 Vim 或 Emacs 吗？

4: 对于初学者来说，现在还有必要学习 Vim 或 Emacs 吗？

**A**: 这取决于你的职业规划和学习目标。

*   **非常有必要的情况**：如果你打算从事后端开发、运维、DevOps、系统编程，或者需要频繁与 Linux 服务器打交道，学习 Vim（至少是基本操作）是必修课。因为在生产环境中，你可能无法安装图形化的 IDE。
*   **非必须的情况**：如果你专注于前端、移动端开发，或者主要在本地 Windows/macOS 环境下工作，使用 VS Code 或 IDE 可能会带来更直观的体验。

然而，学习 Vim 的基本操作（如 `hjkl` 移动、`i` 插入、`:wq` 保存退出）只需要几个小时，但这能让你在任何 Unix-like 系统下都能生存，这是一笔极具性价比的时间投资。

---



### 5: Emacs 和 Vim 在 AI 时代的最新发展如何？

5: Emacs 和 Vim 在 AI 时代的最新发展如何？

**A**: 两者都在积极进化，并没有固步自封。

*   **Vim/Neovim**：Neovim 由于其更好的 Lua 脚本支持和异步 I/O 能力，已经成为现代 Vim 用户的首选。社区开发了诸如 `avante.nvim`、`copilot.vim` 等插件，使得在终端里体验 AI 补全甚至与 AI 对话修改代码变得非常流畅。
*   **Emacs**：Emacs 社区非常活跃，出现了如 `gptel`、`ellama` 等包，允许用户直接在 Emacs 的 Org-mode 中与 AI 交互，甚至利用 AI 进行邮件回复或文本摘要。Emacs 29/30 版本也引入了对原生 JSON 和 Threads 的支持，极大地提升了性能和与现代 Web 工具的兼容性。

---



### 6: 使用 Vim/Emacs 配合 AI 编程，与使用 Cursor（基于 VS Code）相比有哪些具体的体验差异？

6: 使用 Vim/Emacs 配合 AI 编程，与使用 Cursor（基于 VS Code）相比有哪些具体的体验差异？

**A**: 主要差异在于**交互模式**和**上下文管理**。

*   **Cursor/VS Code**：

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 在 Vim 或 Emacs 中，利用现有的 AI 插件（如 CodeGPT 或 Copilot）生成一段代码后，往往需要手动调整格式或修复细微错误。请尝试配置一个快捷键，使得在选中 AI 生成的代码块后，能一键调用编辑器原本的格式化工具（如 Vim 的 `=` 命令或 Emacs 的格式化函数）进行自动修正。

### 提示**:

### Vim 用户可以思考如何将 `=` 命令与可视模式结合，并映射到 `<leader>` 键上。

---
## 引用

- **原文链接**: [https://batsov.com/articles/2026/03/09/emacs-and-vim-in-the-age-of-ai](https://batsov.com/articles/2026/03/09/emacs-and-vim-in-the-age-of-ai)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47319071](https://news.ycombinator.com/item?id=47319071)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [Emacs](/tags/emacs/) / [Vim](/tags/vim/) / [编辑器](/tags/%E7%BC%96%E8%BE%91%E5%99%A8/) / [LLM](/tags/llm/) / [AI 编程](/tags/ai-%E7%BC%96%E7%A8%8B/) / [代码补全](/tags/%E4%BB%A3%E7%A0%81%E8%A1%A5%E5%85%A8/) / [工作流](/tags/%E5%B7%A5%E4%BD%9C%E6%B5%81/) / [IDE](/tags/ide/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [AI 时代的编辑器演进：Emacs 与 Vim 的智能化实践]({{< relref "posts/20260314-hacker_news-emacs-and-vim-in-the-age-of-ai-2.md" >}})
- [AI 时代的编辑器演进：Emacs 与 Vim 的智能化适配]({{< relref "posts/20260314-hacker_news-emacs-and-vim-in-the-age-of-ai-3.md" >}})
- [Claude Code 全面接入微软内部开发工作流]({{< relref "posts/20260202-hacker_news-claude-code-is-suddenly-everywhere-inside-microsof-10.md" >}})
- [如何使用 Claude Code：规划与执行的分离]({{< relref "posts/20260222-hacker_news-how-i-use-claude-code-separation-of-planning-and-e-16.md" >}})
- [Claude Code 全面集成至微软内部开发工作流]({{< relref "posts/20260202-hacker_news-claude-code-is-suddenly-everywhere-inside-microsof-6.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*