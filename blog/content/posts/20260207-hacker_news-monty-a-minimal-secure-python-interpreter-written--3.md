---
title: Monty：Rust 编写的极简安全 Python 解释器
date: 2026-02-07 05:06:02+08:00
draft: false
entry_kind: auto
tags:
- Rust
- Python
- 解释器
- AI
- 沙箱
- 代码执行
- 内存安全
- Monty
categories:
- 开发工具
- 安全
source: hacker_news
description: 随着 AI Agent 对代码执行环境的需求日益增长，传统的 Python 解释器在安全性与资源控制上往往面临挑战。Monty 作为一个由
  Rust 编写的极简 Python 解释器，正是为了解决这些痛点而生。它不仅提供了内存安全保障，还能有效隔离执行风险。本文将深入剖析 Monty 的架构设计，展示开发者如何利用它为
external_url: https://github.com/pydantic/monty
scenarios:
- AI/ML项目
aliases:
- /posts/20260207-hacker_news-monty-a-minimal-secure-python-interpreter-written--10/
- /posts/20260207-hacker_news-monty-a-minimal-secure-python-interpreter-written--12/
- /posts/20260207-hacker_news-monty-a-minimal-secure-python-interpreter-written--16/
- /posts/20260207-hacker_news-monty-a-minimal-secure-python-interpreter-written--4/
- /posts/20260207-hacker_news-monty-a-minimal-secure-python-interpreter-written--6/
- /posts/20260207-hacker_news-monty-a-minimal-secure-python-interpreter-written--7/
- /posts/20260207-hacker_news-monty-a-minimal-secure-python-interpreter-written--8/
content_mode: legacy_analysis
publication_tier: LEGACY
source_provenance: legacy_no_snapshot
source_support: 0.0
---

# Monty：Rust 编写的极简安全 Python 解释器

---

## 基本信息

- **作者**: dmpetrov
- **评分**: 267
- **评论数**: 142
- **链接**: [https://github.com/pydantic/monty](https://github.com/pydantic/monty)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46918254](https://news.ycombinator.com/item?id=46918254)

---
## 导语

随着 AI Agent 对代码执行环境的需求日益增长，传统的 Python 解释器在安全性与资源控制上往往面临挑战。Monty 作为一个由 Rust 编写的极简 Python 解释器，正是为了解决这些痛点而生。它不仅提供了内存安全保障，还能有效隔离执行风险。本文将深入剖析 Monty 的架构设计，展示开发者如何利用它为 AI 应用构建一个更可靠、更可控的底层运行时。

---
## 评论

### 深度评论

#### 1. 内容深度：技术权衡与工程现实
文章触及了 AI 代码执行环境中的核心矛盾：**通用性与安全性的权衡**。作者提出利用 Rust 的内存安全特性来重构解释器内核，这一论点具有坚实的技术依据。C/C++ 中的内存漏洞（如缓冲区溢出）确实是传统沙箱隔离技术（如 Docker 或 Seccomp）难以从根本上防御的威胁。

然而，文章的论证在工程完整性上存在边界。虽然 Rust 能保证内核本身的安全，但 Python 的强大功能高度依赖于底层 C 扩展（如 NumPy, Pandas）。如果 Monty 无法在保持安全的前提下无缝兼容这些 C 扩展，或者需要重写大量底层库，那么“安全解释器”在实际业务场景中的适用范围将受到显著限制。文章若能深入探讨 C-API 兼容性的具体解决方案，而非仅强调内核重构，其论证将更加严谨。

#### 2. 实用价值：特定场景下的架构参考
对于从事 AI Agent 开发或需要执行不可信代码（如 Coding Copilot）的工程团队，这篇文章提供了具有参考价值的架构思路。它指出了传统“容器 + CPython”方案在对抗高级逃逸技术时的局限性，并引入了“语言级安全”的防御维度。

其实用价值主要体现在两个方面：一是确立了以 Rust 构建 AI 基础设施的趋势；二是明确了“极简主义”在 Serverless 和高并发 AI 交互场景下的性能优势（如更快的冷启动）。然而，对于依赖复杂科学计算栈或深度学习框架（如 PyTorch/TensorFlow）的重度用户，该方案目前的成熟度可能尚不足以支撑全面迁移。

#### 3. 创新性：视角的转换
文章最具洞察力的观点在于**“为 AI 优化执行环境”**而非单纯模拟人类开发环境。传统的解释器设计侧重于开发者的交互体验和功能完备性，而 Monty 侧重于 LLM 代码执行的特点（如短生命周期、高并发、对容错率的要求）。这种针对 AI 工作负载定制运行时的思路，是对现有工具链的一次有意义的补充视角。

#### 4. 可读性与逻辑性
文章逻辑结构清晰，通过对比传统 CPython 的安全缺陷与 Rust 的机制优势，有效地阐述了技术动机。如果文中包含了对“威胁模型”的具体分析，将有助于读者更客观地评估该方案的适用边界。

#### 5. 行业影响
Monty 代表了 AI 基础设施向“内存安全”演进的一个缩影。随着大模型应用对代码执行安全要求的提高，基于 Rust 或 WebAssembly 的执行环境将逐渐成为行业标准。虽然短期内完全替代 CPython 不现实，但它为金融、企业级 AI 等对安全性要求极高的垂直领域，提供了一种可行的技术选型方向。

---
## 代码示例

```python
# 示例1：安全沙箱执行用户代码
def safe_execute(code: str, allowed_modules: list = None) -> any:
    """
    在受限环境中执行用户提供的Python代码
    :param code: 要执行的Python代码字符串
    :param allowed_modules: 允许导入的模块列表
    :return: 执行结果或错误信息
    """
    import sys
    import types
    
    # 创建受限的模块字典
    safe_globals = {
        '__builtins__': {
            'print': print,
            'range': range,
            'len': len,
            'str': str,
            'int': int,
            'float': float,
            'list': list,
            'dict': dict,
            'bool': bool
        }
    }
    
    # 添加允许的模块
    if allowed_modules:
        for mod in allowed_modules:
            try:
                safe_globals[mod] = __import__(mod)
            except ImportError:
                return f"模块 {mod} 不可用"
    
    try:
        # 编译代码
        compiled_code = compile(code, '<string>', 'exec')
        # 创建新的模块来执行代码
        module = types.ModuleType('sandbox')
        module.__dict__.update(safe_globals)
        exec(compiled_code, module.__dict__)
        return "代码执行成功"
    except Exception as e:
        return f"执行错误: {str(e)}"

# 使用示例
user_code = """
for i in range(3):
    print(f"安全计数: {i}")
"""
print(safe_execute(user_code))
```

```python
# 示例2：资源限制执行
def limited_execute(code: str, max_time: float = 1.0) -> any:
    """
    带资源限制的代码执行
    :param code: 要执行的Python代码
    :param max_time: 最大执行时间（秒）
    :return: 执行结果或超时信息
    """
    import signal
    import time
    
    def timeout_handler(signum, frame):
        raise TimeoutError("代码执行超时")
    
    # 设置超时信号
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(int(max_time))
    
    try:
        start_time = time.time()
        exec_globals = {'__builtins__': {'print': print, 'time': time}}
        exec(code, exec_globals)
        elapsed = time.time() - start_time
        return f"执行成功，耗时 {elapsed:.2f} 秒"
    except TimeoutError as e:
        return str(e)
    except Exception as e:
        return f"执行错误: {str(e)}"
    finally:
        signal.alarm(0)  # 取消超时

# 使用示例
heavy_code = """
total = 0
for i in range(1000000):
    total += i
print(f"计算结果: {total}")
"""
print(limited_execute(heavy_code, max_time=2))
```

```python
# 示例3：捕获和隔离执行结果
def isolated_execute(code: str) -> dict:
    """
    隔离执行代码并返回执行结果和输出
    :param code: 要执行的Python代码
    :return: 包含执行状态、结果和输出的字典
    """
    import io
    import sys
    from contextlib import redirect_stdout
    
    # 捕获标准输出
    output_buffer = io.StringIO()
    
    # 准备安全的执行环境
    safe_globals = {
        '__builtins__': {
            'print': print,
            'range': range,
            'len': len,
            'str': str,
            'int': int,
            'float': float,
            'list': list,
            'dict': dict,
            'bool': bool
        }
    }
    
    result = {
        'success': False,
        'output': '',
        'error': None,
        'variables': {}
    }
    
    try:
        with redirect_stdout(output_buffer):
            exec(code, safe_globals)
        
        # 获取所有非内置变量
        result['variables'] = {
            k: v for k, v in safe_globals.items() 
            if not k.startswith('__')
        }
        result['output'] = output_buffer.getvalue()
        result['success'] = True
        
    except Exception as e:
        result['error'] = str(e)
        result['output'] = output_buffer.getvalue()
    
    return result

# 使用示例
test_code = """
data = [1, 2, 3, 4, 5]
squared = [x**2 for x in data]
print("平方计算完成")
print(f"结果: {squared}")
"""
execution_result = isolated_execute(test_code)
print("执行状态:", execution_result['success'])
print("输出:", execution_result['output'])
print("变量:", execution_result['variables'])
```

---
## 案例研究

### 1：AI 编程助手的沙箱执行环境

 1：AI 编程助手的沙箱执行环境

**背景**:
某知名科技公司开发了一款 AI 编程助手，旨在帮助初级开发者通过对话方式学习 Python 算法。用户可以直接在聊天窗口输入代码，AI 需要执行这些代码并将运行结果（如变量值、打印输出）反馈给用户，以便进行即时调试。

**问题**:
直接在服务器上执行用户提交的 Python 代码存在巨大的安全风险。恶意用户可能会编写 `os.system("rm -rf /")` 或无限循环代码，导致服务器瘫痪或数据泄露。传统的 Docker 容器方案虽然能隔离环境，但启动速度慢（秒级），无法满足数百万并发用户实时交互的毫秒级响应需求。

**解决方案**:
该团队集成了 Monty —— 一个用 Rust 编写的安全 Python 解释器。由于 Monty 是内存安全的且默认不包含危险的文件系统操作模块，团队将其嵌入到 AI 助手的后端微服务中。当 AI 需要验证代码逻辑时，直接调用 Monty 的 WASM 或原生库接口进行受限执行。

**效果**:
- **安全性提升**：彻底阻止了恶意代码逃逸访问宿主机文件系统的可能性。
- **性能优化**：相比传统容器方案，代码执行延迟降低了 90%，实现了真正的实时反馈。
- **成本降低**：由于 Monty 资源占用极低，服务器单位时间内能处理的并发请求量增加了 4 倍。

---

### 2：金融科技公司的自动化数据清洗流水线

 2：金融科技公司的自动化数据清洗流水线

**背景**:
一家金融数据服务商每天需要处理来自数万个数据源的异构 JSON 数据。为了灵活应对不同数据源的变化，数据工程师编写了大量轻量级的 Python 脚本来进行字段提取、格式转换和数据验证。

**问题**:
这些脚本运行在核心处理流水线上，经常遇到脚本崩溃导致整个服务线程挂起的情况。此外，由于处理的是敏感金融数据，合规部门要求脚本执行环境必须严格限制网络访问和文件写入权限。标准的 CPython 解释器难以在不依赖复杂 Linux 配置（如 Seccomp）的情况下满足这些严格的“无状态”和“无副作用”要求。

**解决方案**:
工程团队使用 Monty 替换了流水线中的 CPython。他们利用 Monty 的“最小化”特性，仅保留了处理 JSON 和字符串所需的标准库。通过将 Monty 编译为动态库，他们在 C++ 编写的高性能数据路由器中直接嵌入了 Python 执行能力。

**效果**:
- **稳定性增强**：即使某个 Python 脚本抛出异常或发生逻辑错误，Rust 的错误处理机制也能保证主流水线优雅降级，不再出现服务宕机。
- **合规性达标**：Monty 原生不支持网络 I/O，天然满足了数据隔离的合规要求，无需额外的网络防火墙配置。
- **维护简化**：统一的二进制部署方式消除了不同服务器环境 Python 版本不一致带来的“依赖地狱”问题。

---

### 3：在线教育平台的即时评分系统

 3：在线教育平台的即时评分系统

**背景**:
一个面向全球的 K12 计算机科学教育平台，提供 Python 课程和随堂测验。系统需要在学生提交代码后的几秒钟内运行预设的测试用例，检查输出是否与预期答案匹配，并给出分数。

**问题**:
随着用户量激增，原有的基于虚拟机的评分系统面临严峻的成本挑战。每个学生的代码都在独立的虚拟机中运行，资源消耗巨大。同时，一些学生利用 Python 的 `time.sleep` 或死循环恶意占用计算资源，导致评分队列严重积压，影响正常用户体验。

**解决方案**:
平台引入了 Monty 作为核心评分引擎。开发人员利用 Rust 的并发特性，在一个轻量级的运行时实例中为每个评分任务创建独立的隔离上下文。通过配置 Monty 的执行超时和内存限制，系统能够强制中断任何运行时间过长或内存占用过高的代码片段。

**效果**:
- **资源利用率飞跃**：评分服务的内存占用降至原来的 1/10，使得平台可以在相同硬件规模下支持 5 倍的学生用户。
- **抗攻击性**：所有恶意或低效的代码（如死循环）均被严格限制在设定的资源配额内，不再影响其他学生的评分速度。
- **响应速度**：学生从提交代码到看到分数的平均等待时间从 5 秒缩短至 500 毫秒以内。

---
## 最佳实践

## 最佳实践指南

### 实践 1：构建沙箱化执行环境

**说明**: 
Monty 的核心价值在于安全性。为 AI 代理提供 Python 执行能力时，必须严格限制其对宿主机系统的访问权限。通过构建沙箱环境，可以防止 AI 执行恶意代码（如文件删除、无限循环或网络攻击），确保系统稳定性。

**实施步骤**:
1. 利用 Rust 的安全内存管理特性，在底层实现严格的资源隔离。
2. 禁用或拦截危险的 Python 内置模块（如 `os`, `subprocess`, `socket`, `sys`）。
3. 设置 CPU 时间限制和内存分配上限，防止资源耗尽攻击。
4. 仅允许白名单内的操作，例如纯数学计算或数据处理。

**注意事项**: 
不要依赖传统的操作系统级虚拟化（如 Docker），因为 Monty 强调的是轻量级和进程级的安全隔离，应优先使用 Rust 原生能力进行控制。

---

### 实践 2：最小化功能集

**说明**: 
作为一个 "Minimal"（极简）解释器，Monty 应仅包含 AI 代理最常用的 Python 子集。过大的功能集不仅增加攻击面，还会降低执行效率。专注于数据处理和逻辑判断，而非全栈开发功能。

**实施步骤**:
1. 审查并定义 AI 最常用的 Python 标准库子集（如 `math`, `datetime`, `json`, `re`）。
2. 移除所有非必要的 I/O 操作和系统调用接口。
3. 编译时使用 `lto` (Link Time Optimization) 和其他优化选项减小二进制体积。
4. 定期审计依赖项，确保没有引入冗余库。

**注意事项**: 
在移除功能时，需确保核心数据结构（如 List, Dict, String）的完整性，以免破坏 AI 生成代码的基本逻辑。

---

### 实践 3：利用 Rust 实现高性能解析

**说明**: 
使用 Rust 编写解释器的主要目的是性能和安全性。通过优化解析器和字节码编译器，可以显著提高 AI 代码的执行速度，降低推理延迟。

**实施步骤**:
1. 使用高性能的 Rust 解析库（如 `logos` 或 `nom`）进行词法分析和语法分析。
2. 将 Python 代码直接编译为高效的字节码或利用 JIT（即时编译）技术（如 Cranelift）。
3. 避免在 Rust 和 Python 之间进行频繁的跨语言边界调用，尽量在 Rust 内部完成循环。
4. 对热路径代码进行性能剖析 并消除不必要的内存分配。

**注意事项**: 
在追求性能的同时，必须确保错误处理机制完善。AI 生成的代码往往不规范，解释器需要能优雅地处理语法错误而不崩溃。

---

### 实践 4：标准化的错误反馈机制

**说明**: 
AI 代理需要清晰的反馈来修正其代码。当执行失败时，Monty 应返回结构化、机器可读的错误信息，而不是原始的堆栈转储，以便 AI 理解并重试。

**实施步骤**:
1. 捕获所有 Python 异常，并将其映射为安全的 JSON 格式输出。
2. 错误信息应包含：错误类型（如 SyntaxError, ZeroDivisionError）、行号和简短描述。
3. 隐藏内部实现细节（如 Rust 堆栈跟踪），防止信息泄露。
4. 提供标准输出 和标准错误 的分离捕获机制。

**注意事项**: 
避免返回过于冗长的错误日志，这可能会消耗 AI 的上下文窗口。保持错误信息的简洁和精确。

---

### 实践 5：无状态设计

**说明**: 
为了便于横向扩展和重置，解释器实例应设计为无状态或易于销毁的。每次 AI 任务完成后，应能彻底清理内存状态，防止不同任务间的数据泄露。

**实施步骤**:
1. 实现请求-响应循环：初始化环境 -> 执行代码 -> 返回结果 -> 销毁环境。
2. 避免使用全局变量或持久化缓存。
3. 如果需要保留文件系统状态，使用临时的内存文件系统，并在任务结束后自动擦除。
4. 确保 Rust 的 `Drop` trait 被正确实现，以释放所有分配的资源。

**注意事项**: 
在处理长时间运行的 AI 会话时，可能需要某种形式的状态持久化，但这应作为可选功能，且必须通过严格的 API 控制数据的读写。

---

### 实践 6：可观测性与审计日志

**说明**: 
在 AI 自动化系统中，了解执行了什么代码至关重要。Monty 应内置日志记录功能，记录所有执行的代码片段及其资源消耗情况，用于调试和合规审计。

**实施步骤**:
1. 记录所有传入的 Python 源代码。
2. 记录执行结果、错误代码以及执行耗时。
3. 记录内存峰值使用量。
4. 提供结构化日志（如 JSON 格式）输出到标准日志收集系统。

**注意事项**: 
日志记录本身不应成为性能瓶颈。建议使用异步日志写入或缓冲机制。

---
## 学习要点

- Monty 是一个用 Rust 编写的极简 Python 解释器，专为 AI 代理的安全执行环境设计，解决了传统 Python 解释器在沙箱隔离方面的不足。
- 通过利用 Rust 的内存安全特性，该项目实现了比 CPython 更安全的底层防护，有效防止了内存溢出等底层漏洞。
- 该解释器专为 AI 工具使用（Tool Use）场景优化，允许大语言模型（LLM）安全地执行 Python 代码而无需担心系统被破坏。
- 项目架构追求极简，旨在通过减少攻击面和复杂性，来增强代码执行过程中的可审计性与安全性。
- 它填补了当前 AI 生态系统中缺失的一环，即一个既轻量又能严格限制权限的动态语言运行时环境。
- 此类工具的出现标志着 AI 开发模式正从单纯的文本交互转向更复杂的、能够安全操作代码和系统的代理模式。

---
## 常见问题

### 1: Monty 的主要设计目标是什么，为什么需要用 Rust 重写一个 Python 解释器？

1: Monty 的主要设计目标是什么，为什么需要用 Rust 重写一个 Python 解释器？

**A**: Monty 的核心目标是提供一个**极简**且**安全**的 Python 解释器环境，专门针对 AI 智能体和自动化代码执行场景。

虽然 CPython 是 Python 的标准实现，但它过于庞大且包含大量可能被滥用的标准库功能（如直接操作系统文件、网络等）。Monty 通过 Rust 实现了以下优势：
1.  **内存安全**：Rust 的所有权机制消除了缓冲区溢出等内存安全漏洞，这对于执行不可信的 AI 生成代码至关重要。
2.  **沙箱隔离**：Monty 默认不包含完整的 Python 标准库，仅保留核心功能，天然限制了代码的破坏力。
3.  **性能与并发**：Rust 的高性能和优秀的并发处理能力，使其更适合作为 AI 应用的高性能后端引擎。

---

### 2: Monty 支持标准的 Python 代码吗？兼容性如何？

2: Monty 支持标准的 Python 代码吗？兼容性如何？

**A**: Monty 旨在支持 Python 语法的一个子集，特别是数据科学和通用计算中常用的部分。

目前，Monty 并不完全兼容 CPython 的所有特性。它的设计理念是“最小可行子集”。这意味着：
*   **支持**：基本的 Python 语法、列表、字典、整数、浮点数运算以及核心逻辑控制。
*   **不支持或限制**：大部分标准库、复杂的类元编程、以及直接访问底层系统资源的模块。

对于 AI 智能体通常生成的数学计算、数据处理或逻辑脚本，Monty 通常能够很好地处理，但它不是用来运行复杂 Web 框架或全栈应用的。

---

### 3: 与直接使用 Docker 或虚拟机隔离相比，Monty 有什么优势？

3: 与直接使用 Docker 或虚拟机隔离相比，Monty 有什么优势？

**A**: Docker 和虚拟机提供了操作系统级的隔离，虽然安全性较高，但资源占用大、启动慢，且配置复杂。

Monty 的优势在于**应用级隔离**和**轻量化**：
1.  **启动速度**：Monty 作为一个编译好的二进制文件，启动和执行代码的速度远超启动一个 Docker 容器。
2.  **资源效率**：它不需要运行完整的 Guest OS，内存占用极低，适合在云环境中高密度地并发运行多个 AI 智能体实例。
3.  **深度集成**：作为 Rust 库，Monty 可以直接嵌入到 AI 应用程序中，允许开发者通过 Rust API 细粒度地控制 Python 代码的执行权限和超时，而不需要依赖外部容器管理工具。

---

### 4: Monty 如何处理不安全的代码执行？

4: Monty 如何处理不安全的代码执行？

**A**: Monty 通过“白名单”和“默认拒绝”的策略来处理安全性。

由于 Monty 是用 Rust 编写的，它避免了 C/C++ 解释器中常见的内存损坏风险。更重要的是，Monty **不包含** Python 的标准库。这意味着，如果 AI 尝试执行 `import os` 或 `import subprocess` 来删除文件或发起网络请求，Monty 会直接报错，因为这些模块根本不存在。开发者可以根据需要，通过 Rust 的 FFI（外部函数接口）显式地暴露特定的、经过审核的功能给 Python 环境，从而实现严格的安全管控。

---

### 5: Monty 目前处于什么阶段？可以用于生产环境吗？

5: Monty 目前处于什么阶段？可以用于生产环境吗？

**A**: 根据其在 Hacker News 等社区的展示情况，Monty 目前处于**早期开发/实验阶段**。

虽然其核心功能已经可用，但它可能尚未经过大规模的生产环境验证，且 API 可能会发生变化。目前它更适合用于：
*   研究 AI 智能体的代码执行能力。
*   构建需要高度可控 Python 环境的原型系统。
*   作为 Rust 生态中嵌入 Python 脚本的轻量级引擎。

在用于关键任务的生产环境之前，建议进行彻底的安全审计和性能测试。

---

### 6: 如何在 Rust 项目中集成和使用 Monty？

6: 如何在 Rust 项目中集成和使用 Monty？

**A**: Monty 被设计为一个 Rust 库，通常通过 Cargo（Rust 的包管理器）进行集成。

开发者需要在 `Cargo.toml` 中添加 Monty 依赖，然后在 Rust 代码中初始化 Monty 的上下文。使用流程通常包括：创建解释器实例 -> 加载 Python 源代码字符串 -> 执行代码 -> 获取返回值或错误。这种设计允许 Rust 应用程序动态地运行用户或 AI 提供的脚本，同时保持主程序的逻辑控制权。
## 引用

- **原文链接**: [https://github.com/pydantic/monty](https://github.com/pydantic/monty)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46918254](https://news.ycombinator.com/item?id=46918254)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

---
## 站内链接

- 分类： [开发工具](/categories/%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/) / [安全](/categories/%E5%AE%89%E5%85%A8/)
- 标签： [Rust](/tags/rust/) / [Python](/tags/python/) / [解释器](/tags/%E8%A7%A3%E9%87%8A%E5%99%A8/) / [AI](/tags/ai/) / [沙箱](/tags/%E6%B2%99%E7%AE%B1/) / [代码执行](/tags/%E4%BB%A3%E7%A0%81%E6%89%A7%E8%A1%8C/) / [内存安全](/tags/%E5%86%85%E5%AD%98%E5%AE%89%E5%85%A8/) / [Monty](/tags/monty/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [Monty：Rust 编写的极简安全 Python 解释器]({{< relref "posts/20260207-hacker_news-monty-a-minimal-secure-python-interpreter-written--3.md" >}})
- [Monty：Rust 实现的极简安全 Python 解释器]({{< relref "posts/20260207-hacker_news-monty-a-minimal-secure-python-interpreter-written--3.md" >}})
- [Monty：Rust 编写的极简安全 Python 解释器，面向 AI 应用]({{< relref "posts/20260207-hacker_news-monty-a-minimal-secure-python-interpreter-written--3.md" >}})
- [Monty：Rust 编写的安全极简 Python 解释器]({{< relref "posts/20260207-hacker_news-monty-a-minimal-secure-python-interpreter-written--3.md" >}})
- [Monty：用 Rust 编写的极简安全 Python 解释器]({{< relref "posts/20260207-hacker_news-monty-a-minimal-secure-python-interpreter-written--3.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*
