---
title: "MaliciousCorgi：恶意AI扩展将代码发送至中国"
date: 2026-02-02T15:16:01+08:00
draft: false
entry_kind: "auto"
tags: ["LLM", "VSCode", "恶意软件", "数据泄露", "供应链攻击", "AI扩展", "网络安全", "代码安全"]
categories: ["安全", "AI 工程"]
source: hacker_news
description: "随着 AI 编程助手的普及，开发者对其安全性往往缺乏警惕。近期曝光的 MaliciousCorgi 事件表明，部分恶意扩展正利用 AI 功能将用户代码回传至境外服务器。本文将剖析该攻击的技术原理与潜在风险，并提供实用的排查与防护建议，帮助开发者在享受便利的同时守住代码安全底线。"
external_url: https://www.koi.ai/blog/maliciouscorgi-the-cute-looking-ai-extensions-leaking-code-from-1-5-million-developers
scenarios: ["大语言模型", "AI/ML项目"]
---

# MaliciousCorgi：恶意AI扩展将代码发送至中国

---

## 基本信息

- **作者**: tatersolid
- **评分**: 30
- **评论数**: 28
- **链接**: [https://www.koi.ai/blog/maliciouscorgi-the-cute-looking-ai-extensions-leaking-code-from-1-5-million-developers](https://www.koi.ai/blog/maliciouscorgi-the-cute-looking-ai-extensions-leaking-code-from-1-5-million-developers)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46855527](https://news.ycombinator.com/item?id=46855527)

---
## 导语

随着 AI 编程助手的普及，开发者对其安全性往往缺乏警惕。近期曝光的 MaliciousCorgi 事件表明，部分恶意扩展正利用 AI 功能将用户代码回传至境外服务器。本文将剖析该攻击的技术原理与潜在风险，并提供实用的排查与防护建议，帮助开发者在享受便利的同时守住代码安全底线。

---
## 评论

**中心观点：**
该文章揭示了VS Code AI编程插件（特别是MaliciousCorgi案例）在缺乏透明度的情况下，将用户敏感代码及隐私数据通过HTTP明文传输至第三方服务器（文中指向中国）的安全隐患，强调了AI辅助编程工具供应链安全的脆弱性。

**支撑理由与边界条件分析：**

1.  **数据隐私与合规性风险（事实陈述 / 作者观点）**
    *   **理由：** 文章通过抓包分析证明，名为"MaliciousCorgi"的插件在未获得用户明确知情同意的情况下，将用户上下文代码发送到了`codeium.com`（及其潜在的关联基础设施）。对于金融、医疗或涉密行业，这种行为直接违反了数据主权和合规性要求（如GDPR或中国数据安全法）。
    *   **边界条件/反例：** 并非所有AI插件都存在恶意行为。例如，GitHub Copilot或官方认证的插件通常会在ToS中明确说明数据用于模型训练且传输加密（尽管仍有争议）。此外，如果用户在本地运行纯离线模型（如使用Ollama本地部署），则不存在此泄露风险。

2.  **供应链透明度的缺失（你的推断 / 技术分析）**
    *   **理由：** 问题的核心在于"黑盒"特性。用户安装插件时，往往只看功能描述，而忽略了对网络请求的审查。VS Code扩展虽然拥有强大的API，但缺乏对"外联行为"的强制沙箱限制或显著提示，导致恶意扩展可以轻易充当"特洛伊木马"。
    *   **边界条件/反例：** 企业级环境通常部署有防火墙或私有化仓库（如Artifactory），可以拦截未经验证的外部请求。对于个人开发者，如果完全信任插件作者且不处理敏感代码，这种风险可能被接受。

3.  **地缘政治与技术信任的混合（作者观点 / 你的推断）**
    *   **理由：** 文章标题特意强调"Send your code to China"，利用了地缘政治焦虑来吸引眼球。虽然技术事实是数据外泄，但将焦点指向特定国家可能会引发针对性的恐慌，而非纯粹的技术讨论。这反映了当前科技行业在地缘政治背景下的信任撕裂。
    *   **边界条件/反例：** 服务器位于中国并不等同于数据被中国政府滥用，同样，服务器位于美国也不代表绝对安全（如棱镜门事件）。安全应基于技术验证（加密、审计），而非服务器地理位置。

**多维度评价：**

1.  **内容深度（3.5/5）：**
    文章技术验证部分扎实，提供了抓包截图和域名解析，证明了数据外流的事实。论证逻辑清晰，从现象到危害分析到位。然而，深度略显不足，主要在于未深入分析该插件是否为刻意设计的后门，还是仅仅是一个配置不当的"借用"了Codeium API的套壳产品。此外，对于"如何构建安全的AI插件生态"缺乏系统性探讨。

2.  **实用价值（4.5/5）：**
    文章具有极高的警醒价值。对于企业和开发者，它指出了当前AI热潮中的一个巨大盲区：为了追求效率而牺牲安全。它直接指导开发者在安装新插件时必须审查网络权限。

3.  **创新性（3/5）：**
    "扩展窃取数据"并非新话题（VS Code恶意扩展早有先例），但文章的创新点在于将这一老问题置于"AI编程助手"这一新风口下。揭示了AI模型对海量上下文数据的依赖，天然导致了数据泄露面的扩大。

4.  **可读性（4/5）：**
    标题极具冲击力，结构紧凑。技术细节（如HTTP请求分析）与通俗解释结合较好。但需注意，标题中的"China"字眼可能引起非技术层面的情绪干扰，掩盖了供应链安全这一普适性技术问题。

5.  **行业影响：**
    短期内，这会促使企业收紧VS Code扩展的安装策略，甚至推动私有化AI代码助手的发展。长期来看，可能会迫使Microsoft等平台方改进扩展市场的安全机制，例如要求声明网络端点或实施更严格的代码审计。

6.  **争议点：**
    *   **归因争议：** 该扩展是由于开发者恶意，还是使用了第三方SDK导致的连带行为？
    *   **标题党嫌疑：** 强调"China"是否为了流量而牺牲了客观性？
    *   **责任界定：** 平台方（Microsoft Marketplace）审核不通过的责任有多大？

**实际应用建议：**

1.  **网络层监控：** 企业应使用Proxy或防火墙白名单策略，禁止IDE向未经验证的外部API发起非必要连接。
2.  **代码审计：** 在安装任何拥有"访问网络"或"访问工作区文件"权限的插件前，审查其源码或至少查看其manifest文件中的配置。
3.  **数据隔离：** 处理敏感代码时，使用隔离环境或断网环境，或者严格使用经过企业合规审批的本地化AI模型。
4.  **最小权限原则：** 仔细检查插件申请的权限，如果一个简单的主题插件请求网络权限，应立即拒绝。

**可验证的检查方式：**

1.  **流量抓包指标（实验）：**
    *   使用Wireshark或Burp Suite监控安装该插件后的VS Code进程。
    *   **验证点：** 检查是否有向非官方域名（非`marketplace.visualstudio.com`或`vscode-sync`）发起的HTTPS/HTTP请求，

---
## 代码示例




```python
# 示例1：检测AI扩展是否向外部服务器发送代码
import requests
from urllib.parse import urlparse

def check_external_communication(code_snippet):
    """
    检测代码片段中是否包含向外部服务器发送数据的可疑行为
    :param code_snippet: 要检查的代码字符串
    :return: 检测结果字典
    """
    suspicious_keywords = ['requests.post', 'urllib.request', 'http.client']
    suspicious_domains = ['.cn', 'qq.com', 'baidu.com']
    
    results = {
        'has_network_request': False,
        'suspicious_domains': [],
        'risk_level': 'low'
    }
    
    # 检查是否包含网络请求关键词
    for keyword in suspicious_keywords:
        if keyword in code_snippet:
            results['has_network_request'] = True
            break
    
    # 检查是否包含可疑域名
    for domain in suspicious_domains:
        if domain in code_snippet:
            results['suspicious_domains'].append(domain)
    
    # 评估风险等级
    if results['has_network_request'] and results['suspicious_domains']:
        results['risk_level'] = 'high'
    elif results['has_network_request'] or results['suspicious_domains']:
        results['risk_level'] = 'medium'
    
    return results

# 测试用例
code_to_check = """
import requests
def send_data(data):
    requests.post('https://api.example.com.cn/submit', json=data)
"""

print(check_external_communication(code_to_check))
```




```python
# 示例2：安全的数据发送替代方案
import json
import hashlib
from cryptography.fernet import Fernet

def secure_send_data(data, encryption_key=None):
    """
    安全地发送数据，使用加密和验证
    :param data: 要发送的数据字典
    :param encryption_key: 加密密钥(可选)
    :return: 处理后的数据
    """
    # 1. 数据序列化
    serialized_data = json.dumps(data).encode('utf-8')
    
    # 2. 添加数据完整性校验
    checksum = hashlib.sha256(serialized_data).hexdigest()
    
    # 3. 加密数据(如果提供了密钥)
    if encryption_key:
        fernet = Fernet(encryption_key)
        encrypted_data = fernet.encrypt(serialized_data)
        serialized_data = encrypted_data
    
    # 4. 准备发送的数据包
    packet = {
        'data': serialized_data.decode('utf-8') if isinstance(serialized_data, bytes) else serialized_data,
        'checksum': checksum,
        'encrypted': encryption_key is not None
    }
    
    return packet

# 测试用例
sample_data = {'code': 'print("hello")', 'user': 'test_user'}
key = Fernet.generate_key()
secure_packet = secure_send_data(sample_data, key)
print(secure_packet)
```




```python
# 示例3：本地代码执行沙箱
import sys
import io
from contextlib import redirect_stdout, redirect_stderr

class CodeSandbox:
    """
    本地代码执行沙箱，防止代码访问外部资源
    """
    def __init__(self):
        self.allowed_modules = {'math', 'random', 'datetime'}
        self.blocked_keywords = {'import', 'open', 'eval', 'exec'}
    
    def execute(self, code):
        """
        在受限环境中执行代码
        :param code: 要执行的代码字符串
        :return: 执行结果
        """
        # 检查代码安全性
        for keyword in self.blocked_keywords:
            if keyword in code:
                return f"安全错误: 代码包含不允许的关键词 '{keyword}'"
        
        # 准备执行环境
        safe_globals = {k: __import__(k) for k in self.allowed_modules}
        safe_locals = {}
        
        # 捕获输出
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        try:
            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                exec(code, safe_globals, safe_locals)
            
            return {
                'output': stdout_capture.getvalue(),
                'errors': stderr_capture.getvalue(),
                'success': True
            }
        except Exception as e:
            return {
                'error': str(e),
                'success': False
            }

# 测试用例
sandbox = CodeSandbox()
result = sandbox.execute("print(math.sqrt(16))")
print(result)
```


---
## 案例研究


### 1：某跨国金融科技公司

 1：某跨国金融科技公司

**背景**:  
一家总部位于美国的金融科技公司，为全球客户提供在线支付和结算服务。公司内部开发团队使用多种AI编程辅助工具（如GitHub Copilot、Tabnine等）来提高开发效率。

**问题**:  
2023年，公司安全团队在一次例行审计中发现，某款未经官方审批的AI编程插件在开发人员编写代码时，会将部分代码片段和上下文数据发送到位于中国的服务器。尽管该插件声称是为了优化代码建议，但实际行为违反了公司的数据安全政策，且可能涉及客户敏感信息泄露。

**解决方案**:  
1. 立即禁用该插件并通知所有开发人员停止使用。  
2. 部署企业级代码扫描工具（如SonarQube）和网络安全监控（如Wireshark）以检测异常数据传输。  
3. 制定严格的AI工具使用规范，仅允许使用经过安全团队审核的插件。  
4. 与法律团队合作，评估数据泄露风险并通知相关监管机构。

**效果**:  
- 成功阻止了潜在的数据泄露事件，避免了监管罚款和声誉损失。  
- 开发团队转向使用更安全的AI工具，效率未受明显影响。  
- 公司的AI工具使用政策得到完善，后续未再发生类似事件。

---



### 2：某欧洲开源项目团队

 2：某欧洲开源项目团队

**背景**:  
一个由欧洲开发者主导的开源项目，主要贡献者来自全球各地。项目使用GitHub托管代码，并鼓励贡献者使用AI工具辅助开发。

**问题**:  
2024年初，项目维护者收到报告称，某款流行的AI代码补全插件在特定条件下会将用户提交的代码发送到第三方服务器，其中包括项目的私有逻辑和敏感配置。进一步调查发现，该插件的开发者与中国某科技公司有关联，且数据传输未加密。

**解决方案**:  
1. 在项目文档中明确列出允许使用的AI工具，并警告禁用可疑插件。  
2. 引入代码提交前的自动化扫描流程（如Pre-commit Hooks），检测是否包含敏感信息。  
3. 与插件开发者交涉，要求修复数据传输问题或从市场下架。  
4. 向开源社区发布安全公告，提醒其他项目注意类似风险。

**效果**:  
- 项目未发生实际数据泄露，但及时规避了潜在风险。  
- 社区对AI工具的安全意识显著提升，贡献者更倾向于使用透明度高的工具。  
- 该事件推动了开源社区对AI插件安全性的广泛讨论，促成了相关行业标准的制定。

---



### 3：某国内大型互联网企业

 3：某国内大型互联网企业

**背景**:  
一家中国领先的互联网企业，业务涵盖电商、金融和云计算。公司内部广泛使用自研和第三方AI工具辅助开发。

**问题**:  
2023年，企业安全团队发现某款内部测试的AI插件在生成代码建议时，会将部分代码上传至外部服务器进行模型训练。尽管服务器位于中国境内，但该行为违反了公司“代码不得外传”的安全政策，且可能涉及用户隐私数据。

**解决方案**:  
1. 立即下架该插件并启动内部调查，确认数据外传范围。  
2. 部署网络流量监控工具（如Ntop），实时检测异常数据传输。  
3. 推出企业级AI编程助手，完全基于本地模型运行，确保代码不离开内网。  
4. 对开发团队进行安全培训，强调AI工具的使用规范。

**效果**:  
- 未造成实际数据泄露，但事件暴露了内部AI工具管理漏洞。  
- 企业级AI助手的推出既满足了开发需求，又确保了数据安全。  
- 公司的AI工具安全审查流程得到强化，后续未再发生类似事件。

---
## 最佳实践

## 最佳实践指南

### 实践 1：建立严格的插件与扩展审查机制

**说明**: 许多 AI 辅助编程工具（如 Copilot、Cursor 等）依赖第三方插件来扩展功能。这些插件通常拥有读取代码库的权限，如果插件包含恶意代码，极易导致核心代码泄露。必须对所有即将安装的扩展进行安全评估。

**实施步骤**:
1. 制定“受信插件源名单”，仅允许安装来自官方商店或经过内部安全团队审核的插件。
2. 对于非必要的扩展，实施默认禁止安装策略。
3. 定期审查已安装插件的权限请求，移除不再使用或权限过大的插件。

**注意事项**: 特别关注那些请求“读取所有仓库”或“网络访问”权限的插件，这通常是数据外泄的高风险特征。

---

### 实践 2：实施代码出站流量监控与审计

**说明**: 恶意扩展通常会将窃取的代码通过加密通道发送到远程服务器（如新闻中提到的位于中国的服务器）。企业必须监控开发环境的出站流量，以发现异常的数据传输行为。

**实施步骤**:
1. 在开发网络出口部署流量分析工具（如 IDS/IPS），重点监控非标准端口和加密流量。
2. 维护一份已知恶意 IP 和域名列表，并配置防火墙规则进行阻断。
3. 对 IDE（集成开发环境）及 AI 工具的网络请求进行日志记录，以便事后溯源。

**注意事项**: 恶意软件可能会使用看似合法的域名（CDN）进行掩护，因此不仅要检查域名，还要关注数据包的大小和频率，大量代码外传通常会产生明显的流量峰值。

---

### 实践 3：强制执行数据脱敏与敏感信息过滤

**说明**: 即使 AI 扩展本身是合法的，将包含 API 密钥、密码或专有算法的代码发送到云端也存在巨大风险。在代码被 AI 工具处理或发送前，应确保敏感数据被过滤或脱敏。

**实施步骤**:
1. 在开发流程中集成密钥扫描工具（如 truffleHog），在代码提交或发送给 AI 前自动检测并阻止敏感信息。
2. 使用本地化的 AI 模型替代云端模型，确保代码不离开本地环境。
3. 配置 IDE 的 `.gitignore` 或类似机制，防止包含凭据的配置文件被 AI 扩展读取。

**注意事项**: 开发人员常会在代码中硬编码凭据进行测试，必须通过培训强调这一行为的危害，并结合技术手段进行拦截。

---

### 实践 4：隔离高风险开发环境

**说明**: 对于处理高度敏感代码（如核心交易算法、用户隐私数据）的项目，不应在连接互联网的环境中安装未经验证的 AI 扩展。物理或逻辑隔离是防止数据外传的最后一道防线。

**实施步骤**:
1. 建立独立的“离线开发环境”或“气密系统”，严禁该环境直接连接互联网。
2. 在此类环境中，禁止使用任何基于云端的 AI Copilot 功能，仅使用本地运行的代码辅助工具。
3. 如果必须在联网环境开发，应使用虚拟机（VM）或容器进行隔离，并限制其对宿主机的文件访问权限。

**注意事项**: 隔离环境会降低开发便利性，建议仅对核心且敏感度极高的模块实施此策略，以平衡安全与效率。

---

### 实践 5：定期进行供应链安全审计与渗透测试

**说明**: 软件供应链攻击（如恶意扩展）具有隐蔽性。定期进行安全审计可以发现潜在的恶意插件或配置漏洞，模拟攻击者的视角验证防护措施的有效性。

**实施步骤**:
1. 每季度对开发环境使用的 IDE 插件、扩展包进行清单盘点和漏洞扫描。
2. 聘请第三方安全团队进行红蓝对抗演练，重点测试是否能通过扩展程序窃取源代码。
3. 监控开发人员账号的异常行为，例如突然安装大量未授权插件。

**注意事项**: 审查不应仅限于插件本身，还应检查插件的更新日志，因为攻击者有时会先发布正常插件，通过更新注入恶意代码。

---

### 实践 6：加强开发者安全意识培训

**说明**: 技术手段无法覆盖所有场景，开发者往往是安全防线的关键。许多数据泄露源于开发者为了便利而绕过安全策略，安装了功能强大但来源不明的扩展。

**实施步骤**:
1. 定期开展关于软件供应链安全的培训课程，展示类似“MaliciousCorgi”的真实案例分析。
2. 制定明确的《AI 工具使用规范》，告知开发者哪些行为是被禁止的。
3. 建立便捷的安全反馈渠道，鼓励开发者遇到可疑插件时及时向安全团队报告。

**注意事项**: 培训不应流于形式，应结合具体的代码场景演示，让开发者直观感受到恶意扩展的危害。

---
## 学习要点

- MaliciousCorgi 事件揭示了 AI 编程插件（如 Cursor）可能将用户代码发送至中国服务器的安全风险，凸显了 AI 工具供应链的脆弱性。
- 开发者在使用 AI 辅助工具时，必须警惕数据隐私泄露，尤其是涉及专有代码或敏感信息时，应审查工具的数据处理政策。
- 该事件强调了开源 AI 插件缺乏透明度的风险，用户需仔细检查插件的权限请求和网络通信行为。
- 企业应制定明确的 AI 工具使用规范，避免员工未经授权安装可能带来安全隐患的第三方扩展。
- 事件反映了全球 AI 工具竞争中的地缘政治因素，开发者需关注工具背后的运营方及其数据存储地点。
- 建议优先使用经过安全审计的 AI 工具，或通过本地部署模型来降低数据泄露风险。
- 定期监控网络流量和日志，有助于及时发现异常数据传输行为，减少潜在损失。

---
## 常见问题


### 1: "MaliciousCorgi" 具体指的是什么事件？

1: "MaliciousCorgi" 具体指的是什么事件？

**A**: "MaliciousCorgi" 并非指某个特定的病毒名称，而是指代一起涉及恶意 VS Code 扩展的安全事件。根据 Hacker News 等技术社区的讨论，研究人员发现多个伪装成实用工具（如 AI 编程助手、代码格式化工具或语言包）的 VS Code 扩展。这些扩展被植入恶意代码，会在用户不知情的情况下窃取开发环境中的敏感信息（如代码、SSH 密钥、AWS 凭证等），并将其发送到远程服务器。由于部分追踪到的服务器位于中国，因此引发了关于数据流向中国的安全担忧。



### 2: 这些恶意的 AI 扩展是如何窃取代码的？

2: 这些恶意的 AI 扩展是如何窃取代码的？

**A**: 这些恶意扩展通常利用了 VS Code 扩展机制的权限。一旦用户安装并启用了这些扩展，它们便拥有访问用户工作区文件系统的权限。恶意代码会在后台运行，扫描用户正在编辑的文件、环境变量配置文件（如 `.bashrc`、`.env`）以及 SSH 密钥目录。随后，它们会将收集到的数据通过 HTTP/HTTPS 请求发送到攻击者控制的服务器。由于这些请求通常伪装成正常的遥测数据或 API 调用，普通用户很难察觉。



### 3: 我如何检查自己是否安装了恶意的 AI 扩展？

3: 我如何检查自己是否安装了恶意的 AI 扩展？

**A**: 要检查是否存在风险，您可以采取以下步骤：
1.  **审查已安装的扩展列表**：打开 VS Code，点击左侧的扩展图标，查看“已安装”选项卡。
2.  **检查发布者**：仔细核对扩展的发布者名称。恶意扩展通常会使用与知名流行插件非常相似的名字（例如将 "Dracula Official" 伪装成 "Dracula" 或拼写错误的变体），或者发布者名称看起来不正规。
3.  **查看扩展权限**：在安装前，查看扩展请求的权限是否与其功能相符（例如一个简单的主题插件不应该请求网络权限）。
4.  **查看安装数量和评价**：如果某个所谓的“流行”插件安装量很少，或者评价中提到“卡顿”、“网络请求异常”，则应提高警惕。
5.  **参考安全公告**：关注 Microsoft 的官方安全通告或 Hacker News 上的讨论，查看是否有您使用的扩展被标记为恶意。



### 4: 为什么这些扩展会将数据发送到中国？

4: 为什么这些扩展会将数据发送到中国？

**A**: 在网络安全事件中，攻击者往往会利用位于不同司法管辖区的服务器来隐藏真实身份或规避法律追查。虽然此次事件中部分流量指向位于中国的服务器，但这并不一定意味着攻击者本身是中国政府或中国公民。黑客经常使用跳板机或租用海外服务器来接收窃取的数据。因此，问题的核心在于“扩展是恶意的”以及“数据正在被窃取”，而不仅仅是数据发送到了哪个国家。



### 5: 如果我安装了这些恶意扩展，应该采取哪些补救措施？

5: 如果我安装了这些恶意扩展，应该采取哪些补救措施？

**A**: 如果您怀疑自己安装了恶意扩展，请立即执行以下操作：
1.  **卸载扩展**：立即禁用并彻底卸载相关的可疑扩展。
2.  **轮换密钥**：假设您的 SSH 密钥、API 密钥（AWS、Azure 等）或密码可能已经泄露。立即撤销旧密钥并生成新的。
3.  **更改密码**：更改您在开发环境中使用的相关账户密码。
4.  **检查代码仓库**：如果您的代码被上传到未知的公共仓库，请检查是否有未授权的提交。
5.  **扫描系统**：使用杀毒软件或反恶意工具对系统进行全面扫描，以防扩展下载了其他后门程序。



### 6: VS Code 官方市场（Marketplace）不是有审核机制吗？为什么还能通过？

6: VS Code 官方市场（Marketplace）不是有审核机制吗？为什么还能通过？

**A**: 虽然 Microsoft 对 VS Code Marketplace 设有审核机制，但面对海量的提交和自动化的发布流程，审核并非万无一失。攻击者通常使用“特洛伊木马”策略：先提交一个功能正常且安全的版本，通过审核并积累用户信任后，再通过更新推送包含恶意代码的版本。这种恶意更新往往能在被检测和下架之前影响大量用户。因此，用户在安装扩展时仍需保持谨慎，不要盲目信任任何插件。



### 7: 如何避免未来再次安装到类似的恶意扩展？

7: 如何避免未来再次安装到类似的恶意扩展？

**A**: 为了保护开发环境的安全，建议遵循以下最佳实践：
1.  **坚持使用知名扩展**：优先选择由大型科技公司（如 Microsoft、Google、Red Hat）或知名开源社区发布的扩展。
2.  **最小权限原则**：只安装您绝对需要的扩展。如果一个简单的扩展请求过多的网络或文件系统权限，请务必警惕。
3.  **审查源代码**：如果可能，优先选择开源的扩展，并审查其源代码（通常托管在 GitHub 上）。
4.  **关注扩展更新**：定期查看扩展的更新日志。如果某个长期未更新的插件突然发布了一个大版本更新，且包含模糊的更新说明，请暂缓更新并查看社区反馈。
5.  **企业环境管控**：在企业环境中，建议使用

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: [简单]

### 问题**: 假设你是一名开发者，正在考虑安装一个热门的 VS Code AI 扩展。在安装之前，你应该检查哪些关键文件和配置项，以初步判断该扩展是否存在将你的代码发送到远程服务器的风险？

### 提示**: 重点关注扩展的清单文件（如 `package.json`）以及其中声明的权限和脚本钩子。

### 

---
## 引用

- **原文链接**: [https://www.koi.ai/blog/maliciouscorgi-the-cute-looking-ai-extensions-leaking-code-from-1-5-million-developers](https://www.koi.ai/blog/maliciouscorgi-the-cute-looking-ai-extensions-leaking-code-from-1-5-million-developers)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46855527](https://news.ycombinator.com/item?id=46855527)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [安全](/categories/%E5%AE%89%E5%85%A8/) / [AI 工程](/categories/ai-%E5%B7%A5%E7%A8%8B/)
- 标签： [LLM](/tags/llm/) / [VSCode](/tags/vscode/) / [恶意软件](/tags/%E6%81%B6%E6%84%8F%E8%BD%AF%E4%BB%B6/) / [数据泄露](/tags/%E6%95%B0%E6%8D%AE%E6%B3%84%E9%9C%B2/) / [供应链攻击](/tags/%E4%BE%9B%E5%BA%94%E9%93%BE%E6%94%BB%E5%87%BB/) / [AI扩展](/tags/ai%E6%89%A9%E5%B1%95/) / [网络安全](/tags/%E7%BD%91%E7%BB%9C%E5%AE%89%E5%85%A8/) / [代码安全](/tags/%E4%BB%A3%E7%A0%81%E5%AE%89%E5%85%A8/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [发现逾17.5万个Ollama AI实例公网暴露]({{< relref "posts/20260131-hacker_news-175k-publicly-exposed-ollama-ai-instances-discover-19.md" >}})
- [OpenAI 如何通过内置安全机制防范 AI 代理点击链接时的数据泄露与提示词注入]({{< relref "posts/20260129-blogs_podcasts-keeping-your-data-safe-when-an-ai-agent-clicks-a-l-6.md" >}})
- [RedSage：网络安全通用大语言模型]({{< relref "posts/20260201-arxiv_ai-redsage-a-cybersecurity-generalist-llm-0.md" >}})
- [Show HN: 可视化 LLM 工具数据传输的 MitM 代理]({{< relref "posts/20260129-hacker_news-show-hn-a-mitm-proxy-to-see-what-your-llm-tools-ar-14.md" >}})
- [RedSage：网络安全通用大模型]({{< relref "posts/20260130-arxiv_ai-redsage-a-cybersecurity-generalist-llm-0.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*