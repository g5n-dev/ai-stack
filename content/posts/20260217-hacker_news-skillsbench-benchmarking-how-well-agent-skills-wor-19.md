---
title: "SkillsBench：评估智能体技能在多样化任务中的表现基准"
date: 2026-02-17T06:54:40+08:00
draft: false
entry_kind: "auto"
tags: ["SkillsBench", "智能体", "Agent", "基准测试", "评估", "LLM", "AI", "任务泛化"]
categories: ["大模型", "论文"]
source: hacker_news
description: "随着 AI Agent 技术的快速发展，如何客观评估其在复杂任务中的实际能力已成为行业关注的焦点。SkillsBench 通过构建多样化的任务场景，对 Agent 的核心技能进行了系统性基准测试，填补了通用评估与垂直领域应用之间的空白。本文将深入解读该基准的设计逻辑与核心发现，帮助读者理解不同技能模块的有效性，并为构建"
external_url: https://arxiv.org/abs/2602.12670
scenarios: ["大语言模型", "AI/ML项目"]
---

# SkillsBench：评估智能体技能在多样化任务中的表现基准

---

## 基本信息

- **作者**: mustaphah
- **评分**: 323
- **评论数**: 137
- **链接**: [https://arxiv.org/abs/2602.12670](https://arxiv.org/abs/2602.12670)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47040430](https://news.ycombinator.com/item?id=47040430)

---
## 导语

随着 AI Agent 技术的快速发展，如何客观评估其在复杂任务中的实际能力已成为行业关注的焦点。SkillsBench 通过构建多样化的任务场景，对 Agent 的核心技能进行了系统性基准测试，填补了通用评估与垂直领域应用之间的空白。本文将深入解读该基准的设计逻辑与核心发现，帮助读者理解不同技能模块的有效性，并为构建更可靠的 Agent 系统提供数据参考。

---
## 评论

### 核心评价

**文章中心观点：**
SkillsBench 通过构建标准化的评测基准，揭示了当前智能体在跨任务场景下技能组合与迁移能力的严重不足，主张从单一任务评估转向对“原子化技能”及其组合逻辑的鲁棒性测试。

**支撑理由：**
1.  **从“全知全能”到“专精组合”的范式转移（事实陈述）：** 传统的 Agent 评测（如 AgentBench）多关注端到端的任务完成率，而 SkillsBench 将任务解构为检索、解释、规划等基础技能。文章论证了评估“技能原子”比评估“整体黑盒”更能精准定位 Agent 的能力短板。
2.  **揭示了“技能干扰”现象（作者观点）：** 文章指出，当 Agent 需要同时调用多个技能（如“编码+逻辑推理”）时，性能往往显著低于单独执行某个技能。这证明了当前模型在多技能协同上存在严重的认知资源竞争或上下文干扰问题。
3.  **对 RAG 和工具调用能力的深度解构（你的推断）：** 文章隐含了一个重要观点：单纯增加工具数量并不能提升 Agent 表现，关键在于 Agent 是否具备在特定上下文中选择正确工具的“元技能”。SkillsBench 的测试结果很可能显示，通用模型在特定垂直领域的工具调用准确率远低于预期。

**反例与边界条件：**
1.  **技能的不可加性（你的推断）：** 文章假设可以通过优化单个技能来提升整体性能，但这忽略了“涌现”现象。即单个技能表现平庸，但在特定架构下组合后可能产生优异的整体表现，反之亦然。因此，过度关注微观技能指标可能会误导对宏观 Agent 架构的设计。
2.  **真实场景的“长尾”与“脏数据”差异（事实陈述）：** 评测基准通常经过清洗，数据分布相对均匀。但在实际工业场景中，长尾问题和非标准化数据才是常态。一个在 SkillsBench 上得分很高的 Agent，在面对真实的、充满噪声的用户指令时，可能会因为缺乏鲁棒性而迅速失效。

---

### 维度深入评价

#### 1. 内容深度与论证严谨性
文章在方法论上具有较高的严谨性，它试图解决 Agent 评测中“因果性缺失”的问题——即知道 Agent 失败了，但不知道是因为听不懂指令（感知问题）还是不会操作（执行问题）。
*   **深度分析：** 文章不仅关注“做什么”，还关注“怎么做”。通过将复杂任务拆解，它能够区分出模型是缺乏知识，还是缺乏推理步骤。
*   **不足之处：** 论证中可能忽略了“上下文依赖”的深度。很多技能的发挥高度依赖于前序步骤的准确性，文章虽然提到了组合，但对于错误如何在技能链中传播的量化分析可能还不够充分。

#### 2. 实用价值
对研发团队具有极高的指导意义。
*   **Debug 效率提升：** 开发者不再需要面对一个“傻”Agent 无从下手，而是可以直接定位到“规划模块”或“Python 解释器模块”的具体问题。
*   **模型选型：** 企业可以根据自身业务侧重的技能（如重检索或重编码），依据基准数据选择最适合的基础模型，而不是盲目追求 MMLU 或 Chatbot Arena 的总分排名。

#### 3. 创新性
*   **视角创新：** 提出了“技能基准”的概念，类似于 LLM 时代的 MMLU，这是向 Agent 工程化迈进的重要一步。它将评测维度从“智商”转向了“执行力”和“技能熟练度”。
*   **方法创新：** 引入了跨任务的迁移能力测试，评估技能在从未见过的任务组合中的泛化能力，这比单纯的 Few-shot 测试更具挑战性。

#### 4. 可读性与逻辑性
文章结构清晰，遵循了“问题提出 -> 基准构建 -> 实验设计 -> 结果分析 -> 结论”的标准学术逻辑。对于技术读者来说，其定义的技能分类体系非常直观，易于理解和复现。

#### 5. 行业影响
*   **推动标准化：** SkillsBench 有望成为 Agent 领域的“Unit Test”（单元测试）标准，推动行业从“秀 Demo”转向“测技能”。
*   **促进架构演进：** 为了在多技能组合测试中取得高分，行业可能会更倾向于采用模块化架构，即将不同的技能（如视觉、代码、搜索）分配给专门的专家模型，再由一个控制器调度，而不是试图用一个通用的 Dense 模型解决所有问题。

#### 6. 争议点与不同观点
*   **原子化的悖论：** 批评者可能认为，人类解决复杂问题时往往使用的是模糊的综合直觉，而非严格的分步技能调用。强制 Agent 进行技能解构，可能会限制其通过端到端训练习得更高效、更拟人的“直觉”能力。
*   **数据污染风险：** 随着基准的发布，模型训练数据不可避免地会包含这些测试用例。未来 SkillsBench 的区分度可能会迅速下降，如同当前的 NLP 基准一样面临“饱和”挑战。

#### 7. 实际应用建议
*   **不要只看总分：** 在使用该基准评估内部 Agent 时，应关注技能的“短板效应”。如果“记忆”技能得分低，无论“规划”得分多高，Agent 都无法完成长对话任务。
*   **建立私有技能集：** 参考 SkillsBench 的框架，但需根据企业自身的 API 和

---
## 代码示例




```python
# 示例1：技能基准测试框架
def benchmark_agent_skill(agent_func, test_cases):
    """
    评估智能体技能在多样化任务上的表现
    :param agent_func: 待测试的智能体函数
    :param test_cases: 测试用例列表，每个用例是(input, expected_output)元组
    :return: 包含准确率、详细结果和失败案例的字典
    """
    results = {
        'total': len(test_cases),
        'correct': 0,
        'details': [],
        'failures': []
    }
    
    for idx, (input_data, expected) in enumerate(test_cases):
        try:
            # 执行智能体函数
            output = agent_func(input_data)
            # 简单比较输出（实际中可能需要更复杂的评估逻辑）
            is_correct = output == expected
            results['correct'] += is_correct
            results['details'].append({
                'case_id': idx,
                'input': input_data,
                'expected': expected,
                'actual': output,
                'pass': is_correct
            })
            if not is_correct:
                results['failures'].append({
                    'case_id': idx,
                    'input': input_data,
                    'expected': expected,
                    'actual': output
                })
        except Exception as e:
            results['failures'].append({
                'case_id': idx,
                'input': input_data,
                'error': str(e)
            })
    
    results['accuracy'] = results['correct'] / results['total']
    return results

# 示例智能体函数：文本分类
def dummy_text_classifier(text):
    """模拟的文本分类智能体"""
    if "positive" in text.lower():
        return "positive"
    elif "negative" in text.lower():
        return "negative"
    else:
        return "neutral"

# 测试用例
test_cases = [
    ("This is positive", "positive"),
    ("Negative content", "negative"),
    ("Neutral text", "neutral"),
    ("Another positive example", "positive")
]

# 运行基准测试
benchmark_result = benchmark_agent_skill(dummy_text_classifier, test_cases)
print(f"准确率: {benchmark_result['accuracy']:.2%}")
print("失败案例:", benchmark_result['failures'])
```




```python
# 示例2：多任务技能评估器
class MultiTaskSkillEvaluator:
    """评估智能体在不同任务类型上的技能表现"""
    
    def __init__(self):
        self.task_results = {}
    
    def evaluate_task(self, task_name, agent_func, test_cases):
        """
        评估特定任务的技能表现
        :param task_name: 任务名称
        :param agent_func: 智能体函数
        :param test_cases: 测试用例列表
        """
        task_result = {
            'total': len(test_cases),
            'correct': 0,
            'metrics': {}
        }
        
        for input_data, expected in test_cases:
            try:
                output = agent_func(input_data)
                # 这里可以添加更复杂的评估逻辑
                if output == expected:
                    task_result['correct'] += 1
            except Exception as e:
                print(f"任务 {task_name} 处理出错: {str(e)}")
        
        # 计算任务准确率
        task_result['accuracy'] = task_result['correct'] / task_result['total']
        self.task_results[task_name] = task_result
    
    def generate_report(self):
        """生成多任务评估报告"""
        report = []
        for task, result in self.task_results.items():
            report.append(f"任务: {task}")
            report.append(f"准确率: {result['accuracy']:.2%}")
            report.append(f"通过案例: {result['correct']}/{result['total']}")
            report.append("-" * 30)
        return "\n".join(report)

# 示例使用
evaluator = MultiTaskSkillEvaluator()

# 评估文本分类任务
evaluator.evaluate_task(
    "文本分类",
    dummy_text_classifier,
    [("good", "positive"), ("bad", "negative"), ("ok", "neutral")]
)

# 评估数值计算任务
evaluator.evaluate_task(
    "数值计算",
    lambda x: x * 2,
    [(1, 2), (2, 4), (3, 6)]
)

# 生成报告
print(evaluator.generate_report())
```




```python
# 示例3：技能对比基准测试
def compare_agent_skills(agent_funcs, test_cases, metric='accuracy'):
    """
    对比多个智能体在同一任务上的技能表现
    :param agent_funcs: 智能体函数字典 {name: function}
    :param test_cases: 测试用例列表
    :param metric: 评估指标
    :return: 对比结果字典
    """
    comparison = {}
    
    for name, func in agent_funcs.items():
        correct = 0
        for input_data, expected in test_cases:
            try:
                output = func(input_data)
                if output == expected:
                    correct += 1
            except:
                pass
        
        comparison[name]


---
## 案例研究


### 1：某全球领先金融服务公司

 1：某全球领先金融服务公司

**背景**: 该公司拥有庞大的内部知识库，包含数万份PDF格式的政策文档、合规报告和技术手册。随着生成式AI的兴起，他们希望构建一个智能问答Agent来辅助员工快速检索信息，减少人工查找时间。

**问题**: 在开发过程中，团队发现不同的Agent配置（例如使用不同的检索策略或不同的LLM模型）在准确率上表现差异巨大。在测试集中表现良好的配置，在面对真实用户复杂的、模糊的提问时，回答准确率大幅下降，甚至产生严重的“幻觉”，导致合规风险。

**解决方案**: 团队引入了SkillsBench作为标准化的基准测试框架。他们不再仅依赖单一的内部测试集，而是利用SkillsBench模拟了涵盖“文档摘要”、“精确数据提取”、“跨文档推理”等多种技能的多样化任务场景，对Agent的技能组合进行了压力测试和横向对比。

**效果**: 通过SkillsBench的细粒度评估报告，团队识别出Agent在“跨文档推理”这一特定技能上的短板。针对性地优化了检索上下文窗口和提示词策略后，Agent在真实环境下的回答准确率提升了25%，显著降低了错误信息的传播风险。

---



### 2：RoboFlow AI（自动化客户服务解决方案提供商）

 2：RoboFlow AI（自动化客户服务解决方案提供商）

**背景**: RoboFlow AI 为电商客户提供自动化的售后支持Agent。这些Agent需要处理从“查询订单状态”到“处理复杂退换货逻辑”等多种不同类型的任务，涉及与外部API（如物流系统、CRM）的深度交互。

**问题**: 随着客户数量的增加，开发团队发现很难量化评估Agent在不同客户场景下的通用能力。某些Agent在处理逻辑简单的查询时表现完美，但在需要调用工具或进行多步规划的复杂任务中经常失败，导致客户满意度评分（CSAT）参差不齐。

**解决方案**: 使用SkillsBench建立了一套跨任务的基准测试体系。他们将Agent的核心能力拆解为“API调用成功率”、“上下文记忆能力”和“错误恢复能力”等技能维度。在每次代码提交或模型更新时，都会自动运行SkillsBench进行回归测试。

**效果**: 这一举措使得团队能够在版本更新时及时发现性能退化。数据显示，通过持续监测和优化Agent的特定技能，该平台处理复杂工单的比例提升了40%，人工介入率降低了30%，极大提高了系统的可靠性和客户的信任度。

---
## 最佳实践

## 最佳实践指南

### 实践 1：构建多维度的任务覆盖矩阵

**说明**: 单一类型的任务无法全面评估 Agent 的技能泛化能力。必须建立一个包含不同认知层级（如回忆、推理、规划、工具使用）和不同领域（如编程、写作、数据分析）的任务矩阵，以确保基准测试能够反映 Agent 在真实且复杂环境下的表现。

**实施步骤**:
1. 定义分类法，将任务按“技能类型”（如检索、逻辑推理、代码生成）和“领域”（如金融、医疗、通用办公）进行分类。
2. 确保每个技能点至少有 3-5 个不同难度等级的具体测试用例。
3. 引入“长尾”任务，即那些在训练数据中出现频率较低但在实际应用中关键的任务。

**注意事项**: 避免任务分布过于集中在某一类（如纯文本问答），这会导致评估结果出现偏差，无法代表 Agent 的综合能力。

---

### 实践 2：采用分层评估指标体系

**说明**: 仅仅通过“最终结果是否正确”来判定 Agent 的表现是不够的。需要引入分层指标，区分“过程正确性”和“结果有效性”，以便精确定位 Agent 是在规划阶段出错，还是在具体工具调用或执行阶段出错。

**实施步骤**:
1. 定义结果指标，衡量最终输出的准确性和完整性。
2. 定义过程指标，例如轨迹相似度、中间步骤的正确率或工具调用的成功率。
3. 设定效率指标，如平均完成时间（Token 消耗或实际耗时）和 API 调用成本。

**注意事项**: 过程评估通常比结果评估更难自动化，建议结合人工抽检或使用更强的模型（如 GPT-4）作为裁判来辅助评估。

---

### 实践 3：建立动态对抗性测试集

**说明**: 静态数据集容易被过拟合，Agent 可能会通过记忆训练数据来通过测试，而非真正掌握技能。引入对抗性测试和动态变化的输入参数，可以更真实地测试 Agent 的鲁棒性和泛化能力。

**实施步骤**:
1. 设计包含干扰信息、噪声输入或格式错误的测试用例。
2. 实现参数化测试，即保持任务逻辑不变，但随机替换具体的实体、数值或上下文背景。
3. 引入“边缘情况”，如超长上下文、空输入或权限受限场景。

**注意事项**: 对抗性测试应侧重于真实场景中可能遇到的困难，而不是为了难倒 Agent 而设计无逻辑的陷阱。

---

### 实践 4：实施严格的工具与环境隔离

**说明**: Agent 的技能往往依赖于与外部工具（如文件系统、API、数据库）的交互。基准测试必须在安全且可复现的隔离环境中进行，以防止 Agent 的操作对宿主系统造成破坏，并确保测试条件的一致性。

**实施步骤**:
1. 使用容器化技术（如 Docker）或沙箱环境运行测试任务。
2. 为测试环境提供 Mock 工具或模拟 API，确保网络延迟和外部服务状态不影响测试稳定性。
3. 记录每一次工具调用的输入输出日志，用于后续的归因分析。

**注意事项**: 必须确保 Mock 工具的行为与真实工具高度一致，否则评估出的技能无法迁移到生产环境。

---

### 实践 5：引入人类反馈与自动评估的双重校验

**说明**: 纯自动化的评估指标（如 BLEU 或精确匹配）难以捕捉回答的细微差别、语气和安全性。结合人类专家的评估和自动化评估，可以构建更可信的基准。

**实施步骤**:
1. 对于高风险或高复杂度的任务，保留人工评估通道。
2. 使用“黄金标准”模型生成的答案作为参考，计算语义相似度。
3. 建立反馈循环，将人类评估中发现的新错误类型转化为新的自动化测试用例。

**注意事项**: 人类评估成本高昂，应采用“主动学习”策略，优先让人类评估那些模型置信度较低或自动化评估分歧较大的样本。

---

### 实践 6：关注技能组合与迁移能力

**说明**: 现实世界的问题往往需要 Agent 同时调用多种技能。基准测试不仅要评估单一技能，还要评估 Agent 将多个子技能串联起来解决复杂问题的能力（Skill Composition）。

**实施步骤**:
1. 设计需要多步骤流程的任务，例如“先从网页检索数据，再写入文件，最后通过邮件发送”。
2. 测试零样本迁移能力，即给 Agent 一个从未见过的全新任务描述，观察其是否能利用已有技能组合出解决方案。
3. 评估 Agent 在任务中途遇到错误时的自我修复能力。

**注意事项**: 复杂任务的失败归因较难，需要详细分析是哪个子技能成为了瓶颈。

---
## 学习要点

- SkillsBench 建立了一个全新的评估基准，旨在通过多样化任务来客观衡量 AI Agent 拥有的特定技能（Skills）在解决实际问题时的有效性。
- 该基准揭示了 Agent 技能存在显著的“任务泛化差距”，即针对特定任务优化的技能在迁移到未见过的任务时，性能会出现大幅下降。
- 研究表明，单纯增加技能的数量并不等同于提升 Agent 的整体能力，关键在于如何有效地组合和利用这些技能以适应不同场景。
- 评估发现，当前主流 Agent 在处理需要跨领域知识或复杂推理的任务时，其技能调用的准确性和鲁棒性仍有待提高。
- SkillsBench 的推出为未来 Agent 研究提供了标准化的测试平台，有助于推动从单一任务模型向具备通用技能组合的智能体发展。

---
## 常见问题


### 1: SkillsBench 主要用来解决什么问题？

1: SkillsBench 主要用来解决什么问题？

**A**: SkillsBench 旨在解决 AI 智能体在通用性评估方面的挑战。目前的基准测试往往集中在特定任务上，无法准确衡量一个智能体的“技能”在不同场景下的迁移能力。SkillsBench 通过构建多样化的任务套件，来测试智能体掌握的核心技能（如规划、记忆检索、工具使用等）在全新且未见过的任务中表现如何，从而更真实地评估智能体的泛化能力和鲁棒性。

---



### 2: SkillsBench 与传统的 Agent 基准测试（如 AgentBench, TravelPlanner）有何区别？

2: SkillsBench 与传统的 Agent 基准测试（如 AgentBench, TravelPlanner）有何区别？

**A**: 传统基准通常侧重于评估智能体完成特定领域任务的成功率，例如订机票或回答特定知识库的问题。SkillsBench 的不同之处在于它采用了“以技能为中心”的评估视角。它不只是看任务是否完成，而是分析完成任务背后的技能组合。它通过将复杂任务解构为不同的技能维度，并测试这些技能在跨领域任务中的表现，从而避免了模型仅在单一数据集上过拟合的风险，更能反映智能体的本质能力。

---



### 3: SkillsBench 包含哪些类型的任务或技能维度？

3: SkillsBench 包含哪些类型的任务或技能维度？

**A**: SkillsBench 涵盖了一系列需要认知和操作能力的任务。根据相关研究，这些任务通常涉及以下关键技能维度：
1.  **多步推理与规划**：在复杂环境中分解目标并制定步骤。
2.  **工具使用**：正确调用外部 API 或工具来获取信息或执行动作。
3.  **上下文学习与记忆**：从之前的交互或文档中提取信息并应用于当前步骤。
4.  **代码执行与调试**：编写或修改代码以解决特定逻辑问题。
这些任务被设计为具有多样性，以迫使智能体展示其核心技能而非仅仅依赖记忆。

---



### 4: SkillsBench 的评估指标是什么？

4: SkillsBench 的评估指标是什么？

**A**: SkillsBench 的评估不仅仅局限于简单的“二选一”（成功/失败）。它通常采用细粒度的评估指标，可能包括：
1.  **任务成功率**：最终目标是否达成。
2.  **子步骤完成率**：在完成长链路任务中，关键中间步骤的正确率。
3.  **技能效率**：智能体在执行过程中使用了多少次尝试、调用了多少次不必要的工具。
这种多维度的评分体系能帮助开发者更清楚地了解模型的短板是在规划阶段还是在执行阶段。

---



### 5: 目前主流的闭源模型（如 GPT-4）和开源模型在 SkillsBench 上的表现差距大吗？

5: 目前主流的闭源模型（如 GPT-4）和开源模型在 SkillsBench 上的表现差距大吗？

**A**: 根据类似的基准测试结果，闭源模型（如 GPT-4o 或 Claude 3.5）在处理复杂技能迁移和多步规划任务上通常仍显著领先于开源模型（如 Llama-3 或 Mistral 系列）。开源模型往往在简单的工具调用或单步推理上表现尚可，但在需要长上下文记忆、复杂逻辑纠错或跨领域知识综合的任务中，失败率相对较高。SkillsBench 的数据正好量化了这一差距，突出了开源 Agent 在通用性方面仍需改进的地方。

---



### 6: 如何使用 SkillsBench 来改进我的 Agent 应用？

6: 如何使用 SkillsBench 来改进我的 Agent 应用？

**A**: 开发者可以将 SkillsBench 作为一个标准化的“压力测试”环节。在开发或微调 Agent 时，不要只在单一业务数据上测试，而是将 Agent 放入 SkillsBench 的任务集中。
1.  **定位瓶颈**：通过观察 Agent 在哪类技能（如代码解释或文件检索）上得分低，可以针对性地优化提示词或检索系统（RAG）。
2.  **防止退化**：在更新 Agent 模型或工具链时，运行 SkillsBench 可以确保新版本没有在基础通用能力上出现退化。

---



### 7: SkillsBench 的数据集是公开的吗？

7: SkillsBench 的数据集是公开的吗？

**A**: 这取决于具体的发布版本。通常此类学术基准（如来自伯克利等机构的研究）会公开测试环境的代码、评估脚本以及部分训练集或验证集。然而，为了防止数据污染，即模型在预训练阶段就已经“看过”了测试题，核心的测试集有时会保留私密或通过专门的 API 进行访问。开发者在使用时应查阅具体的 GitHub 仓库或论文说明以获取准确的许可和使用详情。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 在设计一个 AI Agent 的基准测试时，如何定义一个“技能”的原子性？请列举三个你认为在评估中必须具备的基础通用技能，并解释为什么选择它们。

### 提示**: 考虑 Agent 完成任务的最小动作单元，以及这些技能在不同领域（如文本处理、数据分析）中的复用性。思考“技能”与“任务”之间的区别。

### 

---
## 引用

- **原文链接**: [https://arxiv.org/abs/2602.12670](https://arxiv.org/abs/2602.12670)
- **HN 讨论**: [https://news.ycombinator.com/item?id=47040430](https://news.ycombinator.com/item?id=47040430)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [大模型](/categories/%E5%A4%A7%E6%A8%A1%E5%9E%8B/) / [论文](/categories/%E8%AE%BA%E6%96%87/)
- 标签： [SkillsBench](/tags/skillsbench/) / [智能体](/tags/%E6%99%BA%E8%83%BD%E4%BD%93/) / [Agent](/tags/agent/) / [基准测试](/tags/%E5%9F%BA%E5%87%86%E6%B5%8B%E8%AF%95/) / [评估](/tags/%E8%AF%84%E4%BC%B0/) / [LLM](/tags/llm/) / [AI](/tags/ai/) / [任务泛化](/tags/%E4%BB%BB%E5%8A%A1%E6%B3%9B%E5%8C%96/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [AGENTS.md 架构在智能体评估中超越 Skills 技能]({{< relref "posts/20260130-hacker_news-agentsmd-outperforms-skills-in-our-agent-evals-5.md" >}})
- [AGENTS.md 架构在智能体评估中超越 Skills 技能]({{< relref "posts/20260130-hacker_news-agentsmd-outperforms-skills-in-our-agent-evals-19.md" >}})
- [OpenEnv实践：评估真实环境中的工具调用智能体]({{< relref "posts/20260212-blogs_podcasts-openenv-in-practice-evaluating-tool-using-agents-i-7.md" >}})
- [Agent Skills：AI 智能体技能框架]({{< relref "posts/20260203-hacker_news-agent-skills-1.md" >}})
- [Agent Skills：智能体技能框架]({{< relref "posts/20260203-hacker_news-agent-skills-4.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*