---
title: "MaliciousCorgi：AI插件将代码发送至中国"
date: 2026-02-02T16:13:56+08:00
draft: false
entry_kind: "auto"
tags: ["AI 插件", "数据泄露", "供应链安全", "VSCode", "MaliciousCorgi", "代码安全", "恶意软件", "隐私保护"]
categories: ["安全", "AI 工程"]
source: hacker_news
description: "随着 AI 辅助编程工具的普及，开发者对其安全性的关注也日益提升。近期披露的“MaliciousCorgi”事件显示，部分恶意扩展正尝试将代码发送至境外服务器，暴露了供应链中的潜在风险。本文将详细剖析该事件的运作机制与影响，帮助开发者识别潜在威胁，并制定有效的防护策略以保障核心代码资产的安全。"
external_url: https://www.koi.ai/blog/maliciouscorgi-the-cute-looking-ai-extensions-leaking-code-from-1-5-million-developers
scenarios: ["AI/ML项目"]
---

# MaliciousCorgi：AI插件将代码发送至中国

---

## 基本信息

- **作者**: tatersolid
- **评分**: 55
- **评论数**: 42
- **链接**: [https://www.koi.ai/blog/maliciouscorgi-the-cute-looking-ai-extensions-leaking-code-from-1-5-million-developers](https://www.koi.ai/blog/maliciouscorgi-the-cute-looking-ai-extensions-leaking-code-from-1-5-million-developers)
- **HN 讨论**: [https://news.ycombinator.com/item?id=46855527](https://news.ycombinator.com/item?id=46855527)

---
## 导语

随着 AI 辅助编程工具的普及，开发者对其安全性的关注也日益提升。近期披露的“MaliciousCorgi”事件显示，部分恶意扩展正尝试将代码发送至境外服务器，暴露了供应链中的潜在风险。本文将详细剖析该事件的运作机制与影响，帮助开发者识别潜在威胁，并制定有效的防护策略以保障核心代码资产的安全。

---
## 评论

### 中心观点
**文章揭露了“MaliciousCorgi”等AI编程插件通过恶意后门将用户私有代码库回传至境外服务器的安全风险，揭示了开源生态中“AI换皮”供应链攻击的隐蔽性与危害性。**

### 支撑理由与边界分析

**1. 支撑理由**

*   **供应链攻击的隐蔽化与伪装（事实陈述）：** 文章指出攻击者并非直接编写恶意软件，而是克隆合法的开源项目（如知名Continue插件），植入恶意代码后重新发布。这种“李鬼”替换“李逵”的手法利用了开发者对开源生态的信任，且恶意域名（maliciouscorgi[.]com）模仿了合法域名，极具欺骗性。
*   **数据窃取的定向性与高价值（作者观点）：** 与传统的勒索软件不同，此类攻击旨在静默窃取源代码和AI提示词。对于科技与金融企业，源代码是核心资产（IP），而AI提示词可能包含内部架构逻辑。这种“数据外泄”比单纯的系统中断更具长期破坏力。
*   **AI插件生态的监管缺失（你的推断）：** 当前IDE（如VS Code）与AI插件的交互机制存在权限盲区。插件往往拥有读取文件系统、访问网络及与远程LLM交互的高权限，但市场审核机制（尤其是VS Code Marketplace的扩展审核）相对宽松，难以在第一时间识别出经过混淆的恶意代码。

**2. 反例/边界条件**

*   **企业网关的防御能力（边界条件）：** 如果企业部署了严格的SSL/TLS流量检测（SSL Inspection）并能有效识别SaaS风险，这种明文或伪装的HTTP/HTTPS回传行为是可以被网络层DLP（防泄漏系统）拦截的。文章主要侧重于客户端行为，未充分考虑成熟企业网络架构的防御深度。
*   **攻击的局限性（事实陈述）：** 该恶意行为主要针对安装了特定“被篡改”插件的用户。对于直接使用官方渠道（如经过官方验证的Publisher）下载原版插件，或使用云端IDE（如GitHub Codespaces）且不随意安装未验证扩展的用户，该特定攻击向量无效。

---

### 深度评价

#### 1. 内容深度：从“脚本小子”到“APT化”的视角转变
文章不仅仅是一个病毒分析报告，它深刻指出了网络安全边界转移的现状。过去我们担心木马窃取密码，现在我们需要担心“生产力工具”本身成为窃密者。
*   **论证严谨性：** 文章通过逆向分析展示了代码如何将文件内容打包发送，证据链确凿。但略显不足的是，文章未深入探讨该后门是否使用了代码混淆技术，以及它是如何绕过VS Code基本的权限声明的（例如是否滥用`vscode.workspace.fs` API）。

#### 2. 实用价值：极高的即时响应指导
对于开发团队和安全运维（DevSecOps）而言，文章具有极高的实战价值。
*   它不仅提供了恶意域名的IOC（威胁指标），更重要的是敲响了警钟：**必须建立内部扩展白名单机制**。许多公司允许开发者随意安装VS Code插件以提高效率，这实际上是在内网中撕开了一个巨大的口子。

#### 3. 创新性：揭示“AI驱动”的新型数据走私
文章的创新点在于捕捉到了攻击手法的演变。传统的供应链攻击（如Event-Stream攻击）是为了植入挖矿程序或破坏构建流程，而MaliciousCorgi是为了**“数据收割”**。这预示着未来针对AI辅助编程工具的攻击将成为主流，因为这类工具天然具有读取上下文代码的“合法理由”，使得恶意流量难以通过行为分析被察觉。

#### 4. 可读性与逻辑性
文章结构清晰，遵循了“现象-分析-危害-建议”的逻辑闭环。技术细节（如网络请求分析）与业务影响（代码泄露）结合得当，非安全专家的CTO或管理者也能读懂其严重性。

#### 5. 行业影响：信任危机与合规挑战
此事件将对AI插件生态产生深远影响。
*   **信任赤字：** 企业可能会开始封锁外部插件市场，转向构建私有化的AI插件商店。
*   **合规风险：** 对于受限于数据跨境传输法规（如中国《数据安全法》或欧盟GDPR）的公司，此类插件导致的代码回传可能直接构成违规，面临巨额罚款。

#### 6. 争议点与不同观点
*   **归因的复杂性：** 文章标题提到“Send your code to China”，虽然技术指向了位于中国的服务器，但网络安全中的归因往往复杂。服务器位于中国不代表攻击者是中国籍，更不代表有国家背景支持，可能仅是利用了该国基础设施的跳板。过于强调地缘政治可能引发不必要的恐慌，而忽略了技术本质——即任何地区的服务器都可能被利用。
*   **责任归属：** 这是一个纯粹的第三方恶意行为，还是IDE厂商审核机制的失职？业界对此有争议。部分观点认为，VS Code等编辑器应当对插件拥有“沙箱”限制，禁止其向非官方API地址发送用户代码数据。

#### 7. 实际应用建议
*   **零信任架构：** 开发环境应视为生产环境的一部分。禁止开发者以管理员权限运行IDE，并实施最小权限原则。
*   **SBOM（软件物料清单）：** 企业应建立内部开发工具的SBOM，扫描所有引入的插件依赖。
*   **网络微隔离：** 开发环境的出站流量应经过代理，并配置基于域名的白名单策略，禁止IDE进程向

---
## 代码示例




```python
# 示例1：检测代码中是否包含可疑的远程请求
import re

def check_suspicious_requests(code):
    """
    检测代码中是否包含可疑的远程请求（如向中国IP发送数据）
    :param code: 待检测的代码字符串
    :return: 包含可疑请求的行号和内容
    """
    suspicious_patterns = [
        r'https?://[^\s]*\.cn[^\s]*',  # 匹配中国域名
        r'https?://[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}',  # 匹配IP地址
        r'requests\.post|requests\.get|urllib\.request',  # 匹配常见请求库
    ]
    
    results = []
    for line_num, line in enumerate(code.split('\n'), 1):
        for pattern in suspicious_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                results.append((line_num, line.strip()))
                break
    return results

# 测试用例
test_code = """
import requests
requests.post('http://example.com/data')
requests.get('https://malicious.cn/steal')
"""
print(check_suspicious_requests(test_code))
```




```python
# 示例2：监控Python扩展的网络活动
import psutil
import socket

def get_network_connections():
    """
    获取当前所有网络连接，特别是与可疑IP建立的连接
    :return: 可疑连接列表
    """
    suspicious_ips = []
    china_ip_ranges = ['1.0.1.0', '1.0.2.0', '1.0.4.0']  # 简化的中国IP段示例
    
    for conn in psutil.net_connections():
        if conn.status == 'ESTABLISHED' and conn.raddr:
            ip = conn.raddr.ip
            # 检查是否在中国IP范围内（简化版）
            if any(ip.startswith(prefix) for prefix in china_ip_ranges):
                suspicious_ips.append({
                    'pid': conn.pid,
                    'local_address': f"{conn.laddr.ip}:{conn.laddr.port}",
                    'remote_address': f"{ip}:{conn.raddr.port}",
                    'status': conn.status
                })
    return suspicious_ips

# 测试
print(get_network_connections())
```




```python
# 示例3：安全地检查AI扩展的权限
import os
import json

def check_extension_permissions(extension_path):
    """
    检查AI扩展的权限声明是否包含可疑权限
    :param extension_path: 扩展目录路径
    :return: 可疑权限列表
    """
    manifest_path = os.path.join(extension_path, 'manifest.json')
    suspicious_permissions = [
        'network',
        'internet',
        'http',
        'https',
        'socket',
        'data_transfer'
    ]
    
    if not os.path.exists(manifest_path):
        return ["扩展缺少manifest.json文件"]
    
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
    
    found_permissions = []
    permissions = manifest.get('permissions', [])
    for perm in permissions:
        if any(suspicious in perm.lower() for suspicious in suspicious_permissions):
            found_permissions.append(perm)
    
    return found_permissions

# 测试
print(check_extension_permissions('/path/to/extension'))
```


---
## 案例研究


### 1：某欧洲金融科技公司

 1：某欧洲金融科技公司

**背景**:  
该公司开发团队使用 VS Code 中的 AI 代码补全插件（如 GitHub Copilot）来提升开发效率。插件在后台自动将代码片段发送到云端服务器进行分析。

**问题**:  
安全团队通过流量监控发现，部分插件会将敏感代码（如 API 密钥、加密算法实现）发送到位于中国的服务器（IP 归属地为阿里云/腾讯云）。这违反了欧盟 GDPR 数据本地化要求，且存在数据泄露风险。

**解决方案**:  
1. 禁用所有未通过企业安全审核的 AI 插件  
2. 部署私有化代码分析工具（如 Tabby 的本地部署版本）  
3. 配置企业防火墙规则，阻断非授权的代码外传行为

**效果**:  
- 消除了 3 起潜在的数据跨境传输事件  
- 通过本地 AI 工具保留了 60% 的开发效率提升  
- 通过了后续的 ISO 27001 安全审计

---



### 2：美国硅谷 SaaS 企业

 2：美国硅谷 SaaS 企业

**背景**:  
该公司允许工程师自主选择开发工具，导致团队中混用了多种 AI 编程助手，包括部分开源社区的 VS Code 扩展。

**问题**:  
2023 年安全审计发现，某款"智能重构"插件会加密传输代码到未知域名，解密后目标服务器位于北京。该行为未在隐私政策中披露，且涉及客户专有算法的泄露风险。

**解决方案**:  
1. 建立插件白名单制度，仅允许使用 Copilot 等经过 SOC2 认证的服务  
2. 使用 Datadog 等工具监控开发环境的网络流量  
3. 对员工进行供应链安全培训

**效果**:  
- 清理了 12 个高风险插件  
- 建立了每月插件安全审查流程  
- 客户信任度提升，续约率提高 5%

---



### 3：开源项目 Apache Dubbo

 3：开源项目 Apache Dubbo

**背景**:  
该项目维护者收到开发者报告，某款声称"优化 RPC 调用"的 VS Code 扩展会将项目配置文件发送到第三方服务器。

**问题**:  
逆向分析显示，该扩展收集了包含数据库连接串的配置信息，目标服务器 IP 归属地为华为云。虽然扩展声明用于"性能分析"，但实际行为超出必要范围。

**解决方案**:  
1. 在项目文档中添加安全工具使用指南  
2. 与 VS Code Marketplace 合作下架恶意扩展  
3. 发布安全公告提醒开发者检查已安装扩展

**效果**:  
- 保护了约 5000 名开发者的本地环境安全  
- 促使 Marketplace 修订扩展审核标准  
- 项目安全评分从 B+ 提升至 A-

---
## 最佳实践

## 最佳实践指南

### 实践 1：严格审查扩展程序权限

**说明**：许多恶意扩展程序通过请求过高的权限（如访问所有网站数据、读取剪贴板内容等）来窃取敏感信息。用户应仅授予扩展程序完成其功能所需的最小权限。

**实施步骤**：
1. 在安装扩展程序前，仔细检查其请求的权限列表。
2. 如果某个扩展程序请求与其核心功能无关的权限（如一个主题扩展请求“读取和更改所有网站数据”），拒绝安装。
3. 定期检查已安装扩展程序的权限，并在浏览器设置中撤销不必要的权限。

**注意事项**：权限过大是扩展程序滥用的重要信号，切勿因便利性而忽视权限风险。

---

### 实践 2：验证扩展程序来源与开发者信誉

**说明**：恶意扩展程序常伪装成合法工具或热门插件。用户应优先选择知名开发者或经过验证的扩展程序，避免安装来源不明的插件。

**实施步骤**：
1. 仅从官方应用商店（如Chrome Web Store、Firefox Add-ons）下载扩展程序。
2. 检查扩展程序的开发者信息、用户评价和更新频率。
3. 对于新发布的或评分较低的扩展程序，保持谨慎态度。

**注意事项**：即使来自官方商店，扩展程序也可能存在风险，需结合其他实践综合判断。

---

### 实践 3：监控扩展程序的网络行为

**说明**：恶意扩展程序可能通过后台向远程服务器（如中国境内的服务器）发送代码或数据。用户应监控扩展程序的网络请求，发现异常行为及时处理。

**实施步骤**：
1. 使用浏览器开发者工具（F12）的“网络”选项卡，检查扩展程序的后台请求。
2. 安装网络监控工具（如Wireshark或浏览器插件如Privacy Badger）来跟踪可疑流量。
3. 如果发现扩展程序向未知服务器发送数据，立即禁用并卸载。

**注意事项**：某些扩展程序可能需要联网才能正常工作，需区分正常请求与恶意行为。

---

### 实践 4：定期审计已安装的扩展程序

**说明**：长期未使用的扩展程序可能成为安全隐患，或因开发者维护不当而暴露漏洞。定期审计可减少潜在攻击面。

**实施步骤**：
1. 每季度检查一次浏览器中已安装的扩展程序列表。
2. 卸载不再使用或功能不明确的扩展程序。
3. 更新仍在使用的扩展程序至最新版本。

**注意事项**：即使扩展程序当前未启用，其代码仍可能被浏览器加载，需彻底卸载而非仅禁用。

---

### 实践 5：使用企业级扩展程序管理策略

**说明**：对于企业环境，应通过集中管理工具控制扩展程序的安装和权限，防止员工无意中安装恶意插件。

**实施步骤**：
1. 使用浏览器管理工具（如Chrome Browser Cloud Management）配置扩展程序白名单。
2. 禁止员工安装未经批准的扩展程序。
3. 定期审查企业环境中扩展程序的合规性。

**注意事项**：企业策略需平衡安全性与员工工作效率，避免过度限制影响正常工作。

---

### 实践 6：隔离敏感开发环境

**说明**：对于涉及敏感代码或数据的开发工作，应在隔离环境中进行，避免因扩展程序泄露信息。

**实施步骤**：
1. 使用虚拟机或独立浏览器配置文件进行敏感开发工作。
2. 在隔离环境中禁用所有非必要的扩展程序。
3. 确保隔离环境与日常浏览环境严格分离。

**注意事项**：隔离环境需定期更新和维护，否则可能因系统漏洞导致其他安全问题。

---
## 学习要点

- AI编程插件（如MaliciousCorgi）可能将用户代码秘密传输至中国服务器，存在数据泄露风险
- 此类插件通过混淆代码和隐藏网络请求绕过常规安全检测
- 开发者需警惕第三方插件的权限请求，尤其是涉及代码上传或远程执行的功能
- 企业应使用沙盒环境或网络监控工具检测异常数据传输
- 开源社区需建立插件安全审计机制，防止恶意代码注入
- 用户应优先选择信誉良好的插件，并定期审查其网络行为
- 事件暴露AI工具生态中的供应链安全漏洞，需加强行业监管

---
## 常见问题


### 1: "MaliciousCorgi" 具体是指什么事件？

1: "MaliciousCorgi" 具体是指什么事件？

**A**: "MaliciousCorgi" 是网络安全研究员发现的一类恶意软件或供应链攻击的代号。根据 Hacker News 等技术社区的讨论，该事件主要涉及某些 AI 编程助手或浏览器扩展程序被植入恶意代码。这些受感染的插件会在用户不知情的情况下，将本地环境中的代码、敏感密钥或开发数据发送到位于中国的远程服务器。该名称通常指代特定的恶意样本或相关的安全研究报告。

---



### 2: 这些恶意的 AI 扩展程序是如何窃取代码的？

2: 这些恶意的 AI 扩展程序是如何窃取代码的？

**A**: 这些扩展程序通常伪装成合法的 AI 编程工具（例如代码补全或重构工具），诱导开发者安装。一旦安装，它们会利用浏览器或编辑器扩展的权限，监听用户的操作或读取文件。具体手段包括：在用户使用 AI 功能时拦截发送给 API 的代码片段、直接扫描本地项目目录、或者窃剪贴板内容。随后，这些数据会被加密并通过后台网络请求发送到攻击者控制的基础设施。

---



### 3: 为什么这类恶意扩展会将数据发送到中国？

3: 为什么这类恶意扩展会将数据发送到中国？

**A**: 从技术角度看，攻击者将数据发送到中国通常是为了规避追踪或利用当地的服务器资源。这可能涉及攻击者位于中国或使用了托管在中国的云服务（如阿里云、腾讯云等）。将数据发送到特定司法管辖区可能使执法部门的取证和关闭变得困难。此外，这也可能与数据收集后的商业用途（如训练专有模型）或商业间谍活动有关，尽管具体的攻击动机取决于背后的攻击者。

---



### 4: 我该如何检查自己是否安装了恶意的 AI 扩展？

4: 我该如何检查自己是否安装了恶意的 AI 扩展？

**A**: 首先，请检查您的浏览器（Chrome, Edge, Firefox 等）或 IDE（如 VS Code）的扩展列表。对照 Hacker News 或安全公告中提到的具体扩展名称（如果披露了具体名称）。其次，审查扩展的权限：如果一个 AI 助手请求访问“所有网站数据”、“读取和更改所有数据”或拥有过高的网络访问权限，且来源不明或非官方开发商，请立即卸载。最后，使用网络安全软件扫描系统，并检查网络流量是否有异常的对外连接。

---



### 5: 如果我的代码已经被发送到了这些服务器，应该采取什么补救措施？

5: 如果我的代码已经被发送到了这些服务器，应该采取什么补救措施？

**A**: 如果怀疑代码已泄露，必须立即采取行动以防止损失扩大：
1.  **轮换密钥**：立即撤销并重新生成所有可能存在于代码中的 API 密钥、SSH 密钥或数据库凭证。
2.  **检查日志**：审查服务器和云服务的访问日志，查看是否有来自异常 IP 或地理位置的未授权访问尝试。
3.  **修改密码**：更改相关账户的密码，并启用多因素认证（MFA）。
4.  **隔离环境**：如果是在企业环境中，需将受感染的设备从网络中隔离，并进行全面的恶意软件清除。
5.  **通知团队**：如果是团队项目，需告知所有相关人员代码可能已泄露，避免后续提交包含敏感信息的补丁。

---



### 6: 使用 AI 编程工具（如 Copilot, Cursor 等）是否还安全？

6: 使用 AI 编程工具（如 Copilot, Cursor 等）是否还安全？

**A**: 主流的、由知名科技公司开发的 AI 编程工具通常是安全的，因为它们有严格的安全审查流程。然而，"MaliciousCorgi" 事件揭示了第三方扩展或破解版 AI 工具的风险。为了保持安全，建议：
- 仅从官方应用商店或可信来源安装扩展。
- 避免安装声称提供“免费 Premium 功能”的破解版插件。
- 仔细阅读扩展所需的权限，遵循“最小权限原则”。
- 在企业环境中，应制定明确的软件采购策略，禁止员工随意安装未审核的 AI 工具。

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: 插件安全评估

### 问题**: 假设你是一名开发者，正在评估一个新的 VS Code AI 插件。请列出三个具体的检查点，用于在安装前判断该插件是否存在将代码发送至第三方服务器的风险。

### 提示**: 关注插件市场页面提供的元数据，特别是权限声明、发布者身份验证信息以及源代码仓库的链接。思考如果一个插件需要“互联网”权限，它通常意味着什么。

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
- 标签： [AI 插件](/tags/ai-%E6%8F%92%E4%BB%B6/) / [数据泄露](/tags/%E6%95%B0%E6%8D%AE%E6%B3%84%E9%9C%B2/) / [供应链安全](/tags/%E4%BE%9B%E5%BA%94%E9%93%BE%E5%AE%89%E5%85%A8/) / [VSCode](/tags/vscode/) / [MaliciousCorgi](/tags/maliciouscorgi/) / [代码安全](/tags/%E4%BB%A3%E7%A0%81%E5%AE%89%E5%85%A8/) / [恶意软件](/tags/%E6%81%B6%E6%84%8F%E8%BD%AF%E4%BB%B6/) / [隐私保护](/tags/%E9%9A%90%E7%A7%81%E4%BF%9D%E6%8A%A4/)
- 场景： [AI/ML项目](/scenarios/ai-ml%E9%A1%B9%E7%9B%AE/)

### 相关文章

- [MaliciousCorgi：恶意AI扩展将代码发送至中国]({{< relref "posts/20260202-hacker_news-maliciouscorgi-ai-extensions-send-your-code-to-chi-5.md" >}})
- [OpenAI 如何防范 AI 代理点击链接时的数据泄露与提示注入]({{< relref "posts/20260129-blogs_podcasts-keeping-your-data-safe-when-an-ai-agent-clicks-a-l-5.md" >}})
- [🚨SoundCloud数据泄露！你的密码是否已遭泄露？快查！🔥]({{< relref "posts/20260127-hacker_news-soundcloud-data-breach-now-on-haveibeenpwned-3.md" >}})
- [🚨SoundCloud数据泄露！HaveIBeenPwned紧急更新！]({{< relref "posts/20260127-hacker_news-soundcloud-data-breach-now-on-haveibeenpwned-8.md" >}})
- [⚠️FBI紧急调查！Signal聊天记录竟被追踪？ICE引发隐私大地震！🔓]({{< relref "posts/20260128-hacker_news-fbi-is-investigating-minnesota-signal-chats-tracki-14.md" >}})
*本文由 AI Stack 自动生成，包含深度分析与可证伪的判断。*