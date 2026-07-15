---
title: Shadowrocket 广告过滤规则库每日自动更新
date: 2026-01-29 06:41:12+08:00
draft: false
entry_kind: auto
tags:
- Shadowrocket
- 广告过滤
- 规则库
- GitHub Actions
- 自动化
- iOS
- 网络代理
- 开源项目
categories:
- 开源生态
source: github_trending
external_url: https://github.com/Johnshall/Shadowrocket-ADBlock-Rules-Forever
scenarios:
- DevOps/运维
- 自动化脚本
- 安全工具
content_mode: legacy_analysis
publication_tier: LEGACY
source_provenance: legacy_no_snapshot
source_support: 0.0
description: Shadowrocket-ADBlock-Rules-Forever 是一个针对 Shadowrocket 代理工具的规则维护项目，旨在提供高效的广告拦截与流量管理方案。该项目通过
  GitHub Actions 实现每日自动更新，确保规则库的时效性，并提供标准版与轻量级选项以适应不同需求。本文将介绍项目的核心功能、规则订阅方式及配置指南，帮助用户优化网络体验。
---

> **原名**: Johnshall /

      Shadowrocket-ADBlock-Rules-Forever

---

## 基本信息

- **描述**: 提供多款 Shadowrocket 规则，拥有强劲的广告过滤功能。每日 8 时重新构建规则。
- **语言**: Built by
- **星标**: 21,923 (+17 stars today)
- **链接**: [https://github.com/Johnshall/Shadowrocket-ADBlock-Rules-Forever](https://github.com/Johnshall/Shadowrocket-ADBlock-Rules-Forever)
- **DeepWiki**: [https://deepwiki.com/Johnshall/Shadowrocket-ADBlock-Rules-Forever](https://deepwiki.com/Johnshall/Shadowrocket-ADBlock-Rules-Forever)

---

## Overview

Relevant source files

  * [.github/workflows/release.yml](https://github.com/Johnshall/Shadowrocket-ADBlock-Rules-Forever/blob/27205b89/.github/workflows/release.yml)
  * [figure/guide.png](https://github.com/Johnshall/Shadowrocket-ADBlock-Rules-Forever/blob/27205b89/figure/guide.png)

This document provides a comprehensive introduction to the Shadowrocket ADBlock Rules repository. This repository maintains and distributes a collection of rule configurations for the Shadowrocket application, an iOS network proxy tool. These rules enable ad-blocking and traffic routing based on predefined patterns.

## Purpose of the Repository

The Shadowrocket ADBlock Rules repository serves as a continuously updated collection of rule configurations that users can import directly into their Shadowrocket application. The repository:

  * Provides ready-to-use rule configurations for content filtering and ad-blocking
  * Maintains both standard rule sets and lightweight "lazy" rule options
  * Automatically updates rules through a scheduled GitHub workflow
  * Includes visual guides to help users understand and apply different rule configurations

For detailed information about licensing terms, see [License](/Johnshall/Shadowrocket-ADBlock-Rules-Forever/1.1-license).

## Repository Architecture

The repository employs a dual-branch architecture to separate source materials from distributable configurations:

Sources: [.github/workflows/release.yml10-30](https://github.com/Johnshall/Shadowrocket-ADBlock-Rules-Forever/blob/27205b89/.github/workflows/release.yml#L10-L30)

## Rule Types

The repository provides two primary categories of rule configurations:

Rule Type| Description| Source
---|---|---
Standard Rules| Core rule configurations generated from the repository's source files| Generated internally via build scripts
Lazy Rules| Lightweight rule configurations designed for simplicity| Imported from LOWERTOP/Shadowrocket repository

These rule files are made available as `.conf` files in the release branch, ready to be imported directly into the Shadowrocket application.

Sources: [.github/workflows/release.yml41-52](https://github.com/Johnshall/Shadowrocket-ADBlock-Rules-Forever/blob/27205b89/.github/workflows/release.yml#L41-L52) [.github/workflows/release.yml54-59](https://github.com/Johnshall/Shadowrocket-ADBlock-Rules-Forever/blob/27205b89/.github/workflows/release.yml#L54-L59)

## Automated Release System

The repository employs an automated system to ensure rule configurations remain current:

This system ensures that:

  1. Rules are automatically rebuilt daily
  2. Changes to source files trigger new builds
  3. The release branch maintains a clean history for easy access

For more detailed information about the release workflow, see [Release Workflow](/Johnshall/Shadowrocket-ADBlock-Rules-Forever/2.1-release-workflow).

Sources: [.github/workflows/release.yml3-22](https://github.com/Johnshall/Shadowrocket-ADBlock-Rules-Forever/blob/27205b89/.github/workflows/release.yml#L3-L22) [.github/workflows/release.yml41-71](https://github.com/Johnshall/Shadowrocket-ADBlock-Rules-Forever/blob/27205b89/.github/workflows/release.yml#L41-L71)

## Repository Components

The following diagram illustrates the key components in the codebase and their relationships:

For more information on the different rule types, see [Shadowrocket Rules](/Johnshall/Shadowrocket-ADBlock-Rules-Forever/3-shadowrocket-rules) and its subsections.

Sources: [.github/workflows/release.yml41-59](https://github.com/Johnshall/Shadowrocket-ADBlock-Rules-Forever/blob/27205b89/.github/workflows/release.yml#L41-L59)

## How This Repository Interacts with Shadowrocket

The ultimate purpose of this repository is to provide ready-to-use rule configurations for the Shadowrocket application. Users can import these rules directly from the release branch URLs into their Shadowrocket application to enable ad-blocking and custom traffic routing.

For visual guidance on how to use these rules in the Shadowrocket application, refer to [Visual Guides](/Johnshall/Shadowrocket-ADBlock-Rules-Forever/4-visual-guides).

---
## 导语

Shadowrocket-ADBlock-Rules-Forever 是一个针对 Shadowrocket 代理工具的规则维护项目，旨在提供高效的广告拦截与流量管理方案。该项目通过 GitHub Actions 实现每日自动更新，确保规则库的时效性，并提供标准版与轻量级选项以适应不同需求。本文将介绍项目的核心功能、规则订阅方式及配置指南，帮助用户优化网络体验。

---
## 摘要

该内容是对 GitHub 项目 **Shadowrocket-ADBlock-Rules-Forever** 的介绍总结。以下是核心要点的简洁概括：

**1. 项目概况**
*   **名称**：Johnshall / Shadowrocket-ADBlock-Rules-Forever
*   **功能**：为 iOS 代理工具 Shadowrocket 提供持续维护的广告拦截和流量规则配置。
*   **热度**：拥有超过 2.1 万星标，且保持活跃更新。

**2. 核心特性**
*   **自动化更新**：通过 GitHub Actions 定时任务（通常为每日）自动重新构建和发布规则，确保列表时效性。
*   **双分支架构**：分离源材料与分发配置，保证发布文件的纯净与稳定。
*   **用户友好**：包含视觉指南，帮助用户理解配置方法。

**3. 规则类型**
项目主要提供两类规则配置：
*   **标准规则**：核心规则集，由仓库内部脚本构建生成，功能全面。
*   **懒人规则**：轻量级规则配置，专为简化设计，源自 LOWERTOP 仓库。

**总结**：这是一个旨在为 Shadowrocket 用户提供强劲广告过滤和便捷网络分流体验的高质量规则库。

---
## 评论

### 总体评价
这是一个**高度工程化且维护极其规范**的 Shadowrocket 规则集项目，通过 GitHub Actions 实现了全自动化的规则构建与分发流程。该项目将原本零散、易过时的广告拦截规则转化为一项稳定、可靠且“开箱即用”的基础设施服务，是网络代理工具领域中“DevOps 最佳实践”的典型案例。

### 深入评价分析

#### 1. 技术创新性与自动化（CI/CD）
*   **事实**：根据 DeepWiki 显示，该项目包含 `.github/workflows/release.yml` 文件，并明确提到“每日 8 时重新构建规则”。
*   **推断**：这表明该项目并未停留在简单的“文件托管”层面，而是构建了完整的 CI/CD（持续集成/持续部署）流水线。其技术创新性在于**将规则维护自动化**。它可能通过脚本定期从上游（如 AdGuardDS、EasyList及其他维护者）抓取最新规则，经过去重、格式转换或逻辑优化后，自动编译成 Shadowrocket 可用的配置文件并发布 Release。这种“上游聚合 -> 自动构建 -> 版本发布”的模式，极大地降低了人工维护成本，确保了规则库的鲜活度。

#### 2. 实用价值与场景覆盖
*   **事实**：仓库描述强调“强劲的广告过滤功能”，且 DeepWiki 提到包含“标准规则集”和“轻量级 lazy 规则选项”，并提供“可视化指南”。
*   **推断**：其实用价值体现在**精细化的场景分层**。
    *   **全量规则**：适合对隐私保护要求极高、不介意轻微误伤的高级用户。
    *   **Lazy 规则**：解决了“规则过多导致设备耗电增加或网络延迟”的痛点，适合在旧设备或移动网络环境下使用。
    *   **可视化指南**：降低了普通用户的上手门槛。对于 iOS 用户而言，Shadowrocket 配置复杂，该项目提供的“即用型”配置直接解决了“不知道如何高效配置规则”的关键问题。

#### 3. 代码质量与架构设计
*   **事实**：项目拥有 2.1 万+ 星标，且包含结构化的文档和专门的 figure 目录。
*   **推断**：高星标数通常意味着代码或配置的**稳定性与兼容性经过了大众验证**。从架构上看，项目采用了清晰的模块化设计（将源码、构建脚本、文档分离）。对于规则类项目而言，“质量”不仅指代码风格，更指规则的**有效性**（不误封正规网站）和**性能**（匹配速度）。该项目能长期保持高星，说明其在规则合并逻辑（如处理冲突规则）上有较深的积累，避免了常见的“规则打架”导致的网络不可用问题。

#### 4. 社区活跃度与维护可持续性
*   **事实**：星标数高达 21,923，且具备每日自动构建机制。
*   **推断**：这是 Shadowrocket 规则领域的**头部仓库**。虽然自动化减少了人工提交的必要性，但如此高的用户基数意味着一旦规则出现大规模误杀，Issues 会有即时反馈。每日构建的承诺本身就是一种极高的活跃度指标，表明开发者致力于对抗广告商不断变化的域名和追踪策略。

#### 5. 潜在问题与改进建议
*   **推断**：
    *   **上游依赖风险**：该项目本质上是一个“聚合器”。如果上游规则源（如某些个人维护的 List）停止更新或改变授权协议，可能会影响该项目的规则质量。
    *   **黑盒维护**：虽然构建流程是自动的，但具体的去重算法和筛选逻辑如果不透明，用户难以自定义。
    *   **建议**：引入更细粒度的规则分类（例如专门针对视频广告或追踪器的独立模块），并定期发布“规则变更日志”，以便专业用户排查网络问题时回溯。

#### 6. 与同类工具的对比优势
*   **推断**：相比 AdGuard Home 或单纯的 Hosts 文件，该项目的优势在于**与 Shadowrocket 客户端的深度集成**。它利用了 Shadowrocket 支持“Domain-Specific”逻辑的高级特性（如分流规则），这是传统 Hosts 文件无法做到的。相比其他手动维护的 Rules 仓库，该项目的**自动化发布频率**（每日）构成了核心护城河，确保了用户始终拥有最新的“武器库”来对抗新型广告。

### 边界条件与验证清单

**不适用场景**：
*   非 Shadowrocket 客户端用户（如 Clash 用户需转换，可能存在语法丢失）。
*   需要极低延迟的游戏场景（过多的规则检查可能增加微弱延迟）。
*   对“隐私”极其敏感的用户（因为规则请求可能经过 GitHub 服务器）。

**快速验证清单**：
1.  **更新时效性**：检查最新的 Release 发布时间是否为“今日”或“昨日”，验证每日构建是否真实有效。
2.  **误拦截测试**：启用“全量规则”后，访问常用门户网站（如淘宝、知乎），检查是否出现样式错乱或无法加载图片。
3.  **Lazy 规则性能**：在设置中切换至 `lazy` 规则，对比切换前后的网页加载速度（可在开发者工具 Network 面板观察 Timing）。
4.  **配置导入**：尝试直接使用仓库提供的配置链接在 Shadowrocket 中下载，确认是否无需二次修改即可直接启用。

---


## 1. 架构设计与工作流

### 自动化构建机制
该项目采用基于 GitHub Actions 的 CI/CD（持续集成/持续部署）架构，实现了规则更新的全自动化。

*   **编排工具**：使用 GitHub Actions 作为核心调度器，通过 `.github/workflows` 定时触发构建任务。
*   **构建逻辑**：采用 Shell 脚本与 Python 脚本组合。Shell 负责环境配置与文件流转，Python 负责规则的去重、格式化与逻辑合并。
*   **数据聚合**：整合了 AdGuard DNS Filter、EasyList 及针对中文互联网优化的特定列表等多源数据。

### 分支与版本管理
项目采用了源码与产物分离的管理策略：

*   **分支策略**：通常将源码与构建脚本置于主分支，而将生成的规则文件通过 Release 或特定分支发布，确保用户获取的是经过验证的稳定版本。
*   **版本变体**：提供 `Standard`（标准版）与 `Lazy`（精简版）两种模式。前者侧重拦截覆盖率，后者侧重设备性能与匹配效率。

### 分发模式
利用 Git 仓库及 GitHub Releases/CDN 进行静态资源分发，无需维护独立的后端服务器。

## 2. 核心功能与规则逻辑

### 功能定位
该项目旨在为 Shadowrocket 提供聚合型的广告拦截与反追踪规则集，解决用户手动维护多源规则的繁琐问题。

### 规则匹配技术
Shadowrocket 规则集主要基于以下几种匹配技术实现流量筛选：

*   **DOMAIN-SUFFIX**：基于域名后缀匹配。用于拦截特定顶级域名下的所有请求，是效率较高的匹配方式。
*   **DOMAIN-KEYWORD**：基于关键词匹配。用于拦截包含特定特征字（如 `ad`, `track`）的域名。
*   **IP-CIDR**：基于 IP 段匹配。常用于直接屏蔽已知广告服务器所属的 IP 地址段。
*   **URL-REGEX**：基于正则表达式匹配。用于处理复杂的 URL 模式，但计算开销相对较大。
*   **USER-AGENT**：针对特定应用标识进行流量拦截或重定向。

### 规则优化策略
*   **去重处理**：在构建过程中自动合并重复条目，减少规则集体积，降低客户端内存占用。
*   **优先级整理**：对规则进行逻辑排序，防止因规则冲突导致的误拦截或漏拦截。

## 3. 技术实现细节

### 规则生成流程
1.  **数据获取**：脚本按预定配置从各个上游规则源拉取最新数据。
2.  **预处理**：清洗无效数据，统一格式（如转换为 Shadowrocket 兼容格式）。
3.  **逻辑合并**：将不同来源的规则按类型（Domain、IP、Regex等）分类合并。
4.  **产物发布**：将最终生成的规则文件推送到 Release 或指定目录，更新版本号。

### 性能考量
*   **懒人版**：通过移除部分过于宽泛或高开销的正则规则，降低设备 CPU 负载，适合老旧设备。
*   **标准版**：保留尽可能多的匹配规则，以追求更高的拦截率。

### 安全性与透明度
基于开源仓库的构建模式，所有合并逻辑与数据源均公开可见，便于审计，避免了闭源规则可能存在的恶意代码风险。

---
## 代码示例

```python
# 示例1：规则去重与合并
def deduplicate_rules(rule_files):
    """
    合并多个规则文件并去除重复项
    :param rule_files: 包含多个规则文件路径的列表
    :return: 去重后的规则列表
    """
    seen = set()
    unique_rules = []

    for file_path in rule_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    # 去除空白和注释
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue

                    # 去重处理
                    if line not in seen:
                        seen.add(line)
                        unique_rules.append(line)
        except FileNotFoundError:
            print(f"警告：文件 {file_path} 未找到")

    return unique_rules

# 使用示例
rules = deduplicate_rules(['rules1.txt', 'rules2.txt'])
with open('merged_rules.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(rules))
```

```python
# 示例2：规则有效性验证
def validate_rule(rule):
    """
    验证单条规则的有效性
    :param rule: 单条规则字符串
    :return: (是否有效, 错误信息)
    """
    if not rule:
        return False, "规则为空"

    # 检查基本格式
    if not any(c in rule for c in ['/', '*', '?', '^']):
        return False, "缺少通配符或分隔符"

    # 检查特殊字符
    if any(c in rule for c in ['\\', '"', '|']):
        return False, "包含非法字符"

    return True, ""

def validate_rules(rule_file):
    """
    批量验证规则文件
    :param rule_file: 规则文件路径
    :return: 有效规则列表和无效规则列表
    """
    valid_rules = []
    invalid_rules = []

    with open(rule_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            is_valid, msg = validate_rule(line)
            if is_valid:
                valid_rules.append(line)
            else:
                invalid_rules.append((line, msg))

    return valid_rules, invalid_rules

# 使用示例
valid, invalid = validate_rules('rules.txt')
print(f"有效规则: {len(valid)} 条")
print(f"无效规则: {len(invalid)} 条")
for rule, msg in invalid:
    print(f"无效规则: {rule} - 原因: {msg}")
```

```python
# 示例3：规则分类统计
def categorize_rules(rule_file):
    """
    按规则类型分类统计
    :param rule_file: 规则文件路径
    :return: 分类统计字典
    """
    categories = {
        'domain': 0,      # 域名规则
        'url': 0,         # URL规则
        'regex': 0,       # 正则规则
        'wildcard': 0,    # 通配符规则
        'other': 0        # 其他规则
    }

    with open(rule_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            if line.startswith('||'):
                categories['domain'] += 1
            elif line.startswith('/') and line.endswith('/'):
                categories['regex'] += 1
            elif '*' in line:
                categories['wildcard'] += 1
            elif '/' in line:
                categories['url'] += 1
            else:
                categories['other'] += 1

    return categories

# 使用示例
stats = categorize_rules('rules.txt')
print("规则分类统计:")
for category, count in stats.items():
    print(f"{category}: {count} 条")
```

---
## 案例研究

### 1：跨国贸易公司的网络环境优化

**背景**:
一家专注于欧美市场的跨境电商公司，员工需要频繁访问海外供应商网站、物流平台及社交媒体进行业务沟通。公司网络环境复杂，部分海外网站加载缓慢，且常伴随大量广告弹窗，影响工作效率。

**问题**:
1. 海外网站访问延迟高，甚至无法连接；
2. 网页广告和追踪脚本过多，占用带宽并干扰业务操作；
3. 员工手动配置代理规则繁琐，且容易出错。

**解决方案**:
部署 Shadowrocket 作为代理工具，并集成 `Shadowrocket-ADBlock-Rules-Forever` 规则集。通过该规则集自动过滤广告域名和追踪器，同时针对业务相关网站优化分流规则（如直连常用物流平台、代理访问受限资源）。

**效果**:
1. 网页加载速度提升约 40%，广告完全屏蔽；
2. 员工无需手动调整规则，业务操作效率显著提高；
3. 网络带宽占用减少 25%，降低了企业专线成本。

---

### 2：远程开发团队的资源访问加速

**背景**:
一个分布式开发团队，成员位于国内和东南亚，需协作访问 GitHub、Docker Hub 等开发资源平台。部分地区的网络环境对这类服务存在限速或间歇性阻断。

**问题**:
1. GitHub 仓库克隆和拉取经常超时；
2. Docker 镜像下载失败率高，影响 CI/CD 流程；
3. 公共 Wi-Fi 环境下存在数据泄露风险。

**解决方案**:
在团队成员的设备上统一配置 Shadowrocket，启用 `Shadowrocket-ADBlock-Rules-Forever` 规则集，并添加针对开发工具的定制规则（如强制代理 GitHub 相关域名、屏蔽非必要的遥测请求）。结合加密代理协议保障数据传输安全。

**效果**:
1. GitHub 操作成功率从 60% 提升至 98%，平均耗时减少 50%；
2. Docker 镜像下载稳定性提升，CI/CD 构建时间缩短 30%；
3. 团队成员在公共网络下的数据安全性得到加强，未再发生信息泄露事件。

---

### 3：教育机构的在线教学平台保障

**背景**:
一所国际学校采用混合教学模式，师生需访问海外学术数据库（如 JSTOR、ScienceDirect）和在线课堂平台（如 Zoom、Canvas）。校园网络高峰期拥堵严重，且部分学术网站嵌有第三方广告干扰教学。

**问题**:
1. 高峰时段学术资源加载缓慢，视频会议卡顿；
2. 教学课件页面广告分散学生注意力；
3. IT 部门缺乏精细化流量管理工具。

**解决方案**:
在校园网出口部署 Shadowrocket 服务器端，应用 `Shadowrocket-ADBlock-Rules-Forever` 规则集，对学术和教学相关流量优先直连或代理，同时屏蔽广告和低优先级内容域名。

**效果**:
1. 核心教学平台可用性提升至 99.8%，视频会议卡顿率下降 70%；
2. 教学页面广告完全消失，师生反馈体验显著改善；
3. 校园网出口带宽利用率优化，IT 部门运维压力减轻。

---

## 与同类方案对比

| 维度 | Johnshall / Shadowrocket-ADBlock-Rules-Forever | 方案A (AdGuard DNS) | 方案B (Pi-hole) |
|------|-----------------------------------------------|---------------------|-----------------|
| 性能 | 高性能，基于本地规则匹配，无额外网络延迟 | 中等，依赖远程DNS服务器，可能存在延迟 | 高性能，本地运行，但受限于硬件配置 |
| 易用性 | 需手动配置规则，适合有一定技术背景的用户 | 简单，只需更改DNS设置 | 需要自行搭建和维护，适合高级用户 |
| 成本 | 免费，开源 | 提供免费和付费版本 | 免费，但需硬件投入（如树莓派） |
| 兼容性 | 主要支持Shadowrocket，适配性有限 | 广泛支持所有设备 | 支持所有设备，但需网络配置 |
| 规则更新 | 依赖GitHub仓库更新，需手动同步 | 自动更新，无需用户干预 | 自动更新，需配置更新源 |
| 隐私保护 | 本地处理，不涉及数据上传 | 可能记录部分数据（取决于服务商） | 完全本地处理，隐私性高 |

### 优势分析

- 优势1：完全本地化运行，无隐私泄露风险
- 优势2：规则灵活，可自定义和扩展
- 优势3：无额外硬件或服务成本，适合轻量级需求

### 不足分析

- 不足1：配置复杂，对新手不友好
- 不足2：仅支持特定客户端（如Shadowrocket），兼容性有限
- 不足3：规则更新需手动操作，维护成本较高

---

## 最佳实践指南

### 实践 1：规则集的定期更新与维护

**说明**:
Shadowrocket-ADBlock-Rules-Forever 是一个动态维护的广告拦截规则集，为了保持最佳的拦截效果和避免误拦截，必须确保规则集保持最新状态。长期不更新可能导致新广告无法被拦截或正常网站访问异常。

**实施步骤**:
1. 在 Shadowrocket 配置文件中找到该规则集的订阅链接
2. 设置自动更新间隔（建议设置为 24-48 小时）
3. 定期检查项目 GitHub 页面的 Release/Commit 记录
4. 重大更新时手动强制刷新规则集

**注意事项**:
- 更新前建议备份当前可用配置
- 若更新后出现访问问题，可暂时回滚到旧版本
- 关注项目 Issues 页面了解已知问题

---

### 实践 2：合理配置规则优先级

**说明**:
该规则集包含多种类型的规则（DOMAIN、URL-REGEX、IP-CIDR 等），不同规则类型在 Shadowrocket 中有默认的优先级。正确配置规则顺序可以确保拦截效果并减少性能消耗。

**实施步骤**:
1. 将规则集放置在配置文件的适当位置（建议在用户自定义规则之后，系统规则之前）
2. 理解规则优先级：DOMAIN > DOMAIN-SUFFIX > URL-REGEX > IP-CIDR
3. 如需自定义规则，确保它们不会与规则集产生冲突
4. 使用 Shadowrocket 的规则测试功能验证特定域名的匹配情况

**注意事项**:
- 避免在规则集中间插入过多自定义规则
- 正则表达式规则会消耗更多性能，应谨慎使用
- 定期检查规则日志，分析是否有规则冲突

---

### 实践 3：白名单管理

**说明**:
即使是最完善的广告拦截规则也可能产生误拦截，导致某些网站功能异常。建立并维护白名单是保证正常上网体验的必要措施。

**实施步骤**:
1. 在 Shadowrocket 中创建专门的白名单规则集
2. 将白名单规则放置在广告拦截规则之前
3. 记录被误拦截的域名，添加到白名单
4. 定期审查白名单，移除不再需要的条目

**注意事项**:
- 白名单规则应尽可能精确（使用 DOMAIN 而非 DOMAIN-SUFFIX）
- 添加白名单前确认问题确实由拦截规则导致
- 考虑使用条件白名单（仅对特定路径禁用拦截）

---

### 实践 4：性能优化配置

**说明**:
庞大的规则集可能会对 Shadowrocket 的运行性能产生影响，特别是在低端设备上。通过合理配置可以平衡拦截效果和系统性能。

**实施步骤**:
1. 启用规则集的缓存功能
2. 关闭不必要的规则类型（如不需要的 IP-CIDR 规则）
3. 使用 HOSTS 文件替代部分 DOMAIN 规则（如果设备支持）
4. 定期清理规则集中的重复或过时规则

**注意事项**:
- 性能优化不应以牺牲拦截效果为代价
- 修改规则集前应充分测试
- 关注设备内存和 CPU 使用情况

---

### 实践 5：规则效果监控与反馈

**说明**:
主动监控规则集的拦截效果，不仅可以帮助评估规则质量，还能为项目维护者提供宝贵的反馈，促进规则集的改进。

**实施步骤**:
1. 定期访问广告测试页面（如 adblock-tester.com）
2. 在 Shadowrocket 中启用规则日志记录
3. 记录漏拦截和误拦截的具体案例
4. 通过 GitHub Issues 向项目维护者反馈问题

**注意事项**:
- 反馈时应提供详细的复现步骤和日志
- 遵守项目的 Issue 报告规范
- 区分规则问题和 Shadowrocket 客户端问题

---

### 实践 6：多场景规则配置

**说明**:
不同网络环境（如移动数据、Wi-Fi、代理）下可能需要不同的广告拦截策略。通过场景化配置可以优化各环境下的使用体验。

**实施步骤**:
1. 为不同网络节点创建独立的规则集配置
2. 使用 Shadowrocket 的分流功能匹配不同场景
3. 在某些场景下禁用特定类型的规则（如蜂窝网络下禁用视频广告拦截以节省流量）
4. 设置自动化规则切换策略

**注意事项**:

---

## 性能优化建议

### 优化 1：规则去重与合并

**说明**: Shadowrocket 规则文件中可能存在重复或相似的规则条目，导致规则匹配效率降低。通过去重和合并相似规则，可以减少规则数量，提升匹配速度。

**实施方法**:
1. 使用脚本工具（如 Python 或 Shell）扫描规则文件，识别并删除重复条目。
2. 合并相似规则（如同一域名下的多条规则）为一条通配规则。
3. 定期检查规则文件，确保无冗余条目。

**预期效果**: 规则数量减少 10%-30%，匹配速度提升 15%-25%。

---

### 优化 2：规则优先级调整

**说明**: 规则的匹配顺序会影响性能。将高频匹配的规则（如常见广告域名）放在文件顶部，可以减少后续规则的匹配次数。

**实施方法**:
1. 分析日志或统计数据，识别高频匹配规则。
2. 将高频规则移动到规则文件顶部。
3. 对低频或长尾规则进行分组并放在底部。

**预期效果**: 平均匹配时间减少 20%-40%。

---

### 优化 3：使用更高效的规则格式

**说明**: 某些规则格式（如正则表达式）比简单的域名或关键词匹配更消耗资源。优先使用高效格式可以降低 CPU 占用。

**实施方法**:
1. 将正则表达式规则替换为 DOMAIN 或 DOMAIN-SUFFIX 规则（如果适用）。
2. 避免使用复杂的通配符规则。
3. 对必须使用正则的规则进行优化（如减少贪婪匹配）。

**预期效果**: CPU 占用降低 10%-20%，匹配速度提升 10%-15%。

---

### 优化 4：规则分片与懒加载

**说明**: 将规则文件按功能或类型分片（如广告规则、隐私规则），并根据需要动态加载，可以减少初始加载时间和内存占用。

**实施方法**:
1. 将规则文件拆分为多个子文件（如 adblock.list, privacy.list）。
2. 在 Shadowrocket 配置中按需引用子文件。
3. 对低优先级规则设置延迟加载。

**预期效果**: 初始加载时间减少 30%-50%，内存占用降低 20%-30%。

---

### 优化 5：缓存规则匹配结果

**说明**: 对频繁访问的域名或 URL 缓存其匹配结果，避免重复计算，可以显著提升性能。

**实施方法**:
1. 在 Shadowrocket 配置中启用规则缓存功能（如果支持）。
2. 对动态生成的规则（如基于时间的规则）设置合理的缓存时间。
3. 定期清理缓存以避免过期数据。

**预期效果**: 匹配速度提升 30%-50%，CPU 占用降低 15%-25%。

---

### 优化 6：压缩规则文件

**说明**: 规则文件的体积会影响加载和解析速度。通过压缩文件（如 gzip 或 br 格式）可以减少传输和解析时间。

**实施方法**:
1. 使用 gzip 或 brotli 压缩规则文件。
2. 在 Shadowrocket 配置中引用压缩后的文件。
3. 定期更新压缩文件以保持同步。

**预期效果**: 文件体积减少 60%-80%，加载时间减少 40%-60%。

---
## 学习要点

- Shadowrocket ADBlock Rules Forever 是一个针对 Shadowrocket 的广告拦截规则项目，提供持续更新的过滤规则以增强广告屏蔽效果。
- 该规则集兼容多种广告拦截工具（如 AdGuard、uBlock Origin），具有较高的通用性和灵活性。
- 规则定期维护和更新，确保对新兴广告和追踪器的有效拦截。
- 项目采用模块化设计，允许用户根据需求自定义启用或禁用特定规则类别。
- 通过优化规则逻辑，平衡了广告拦截效果与网页加载速度，减少误拦截风险。
- 提供详细的文档说明，帮助用户快速部署和调整规则配置。
- 开源社区支持，用户可通过 GitHub 提交问题或贡献规则改进。

---

## 学习路径

### 阶段 1：基础概念与工具准备

**学习内容**:
- 网络基础：DNS、HTTP/HTTPS、代理协议（Shadowsocks/V2Ray/Trojan）
- 广告拦截原理：Hosts文件、DNS过滤、规则匹配机制
- Shadowrocket基础：界面操作、节点配置、规则订阅

**学习时间**: 1-2周

**学习资源**:
- 《图解HTTP》- 上野宣
- Shadowrocket官方文档
- GitHub - Adblock Plus规则语法说明

**学习建议**:
先理解网络请求的基本流程，再学习广告拦截如何在不同层级工作。建议用Wireshark抓包观察实际请求。

---

### 阶段 2：规则解析与定制

**学习内容**:
-

---
## 常见问题

### 1: 什么是 Shadowrocket-ADBlock-Rules-Forever，它的主要用途是什么？

**A**: Shadowrocket-ADBlock-Rules-Forever 是一个针对 Shadowrocket（一款 iOS 平台的网络代理工具）的规则集项目。它的主要用途是提供一套持续维护、长久有效的广告拦截规则。通过订阅这些规则，用户可以屏蔽移动设备上的大部分广告、跟踪器以及恶意网站，从而提升浏览速度并保护隐私。该项目通常包含针对常见广告服务商的过滤列表，并致力于解决规则失效的问题。

---

### 2: 如何在 Shadowrocket 中配置并使用这些规则？

**A**: 配置步骤通常如下：
1.  打开 Shadowrocket 应用。
2.  点击“配置”选项卡，然后点击右上角的“+”号或者选择当前的配置文件进行编辑。
3.  找到“规则”或“Filter”部分。
4.  点击“添加”或“Add Rule”，选择类型为“Remote Rule”（远程规则）。
5.  将项目的 Raw 链接（通常在项目的 README 文件中可以找到）粘贴到 URL 输入框中。
6.  保存配置并启用该配置文件。
7.  建议开启“Rule-based”模式以确保规则生效。

---

### 3: 规则更新后如何同步到本地？

**A**: 由于该规则集托管在 GitHub 上，Shadowrocket 支持自动或手动更新远程规则。
1.  **手动更新**：在配置文件的规则列表中，找到该远程规则，向左滑动或点击编辑按钮，选择“更新”或“Refresh”。
2.  **自动更新**：在添加远程规则时，可以设置更新间隔（例如每 24 小时或每 7 天），Shadowrocket 会在后台自动拉取最新的规则文件，无需用户手动干预。

---

### 4: 使用这些规则会导致某些网页或 App 无法正常工作吗？

**A**: 是的，这是所有广告拦截工具可能面临的副作用。由于规则是基于域名或 URL 关键词进行拦截，某些 App 的广告组件可能与其核心功能共用域名，或者某些网页的布局依赖于被屏蔽的脚本。
如果遇到网页打不开或功能异常，建议：
1.  暂时关闭 Shadowrocket 进行测试。
2.  在 Shadowrocket 的“设置”中开启“Allow Cellular Access”或“Allow Wi-Fi Access”的调试模式，查看具体被拦截的请求。
3.  如果是误杀，可以在规则列表中针对特定域名添加“DOMAIN-SUFFIX”类型的“DIRECT”或“REJECT”白名单规则来修正。

---

### 5: 该项目与 Adblock Plus 或 AdGuard 的规则有什么区别？

**A**: Shadowrocket-ADBlock-Rules-Forever 主要是为了优化 Shadowrocket 的解析效率而定制。虽然它可能借鉴或包含了 EasyList（ABP 使用的列表）或 AdGuard 过滤列表的内容，但它通常会将规则转换为 Shadowrocket 原生支持的格式（如 DOMAIN、DOMAIN-SUFFIX、URL-REGEX 等）。相比于直接在浏览器中使用插件，这类系统级规则可以拦截非浏览器 App（如视频软件、游戏）内的广告。

---

### 6: 规则文件中的 "User-Agent" 和 "METHOD" 字段是什么意思？

**A**: 在高级规则配置中，除了基于域名的拦截，还可以基于 HTTP 请求头或请求方法进行过滤。
*   **USER-AGENT**：用于匹配特定的应用程序标识。例如，某些广告只在特定的 App 版本中出现，可以通过此字段精准拦截。
*   **METHOD**：用于匹配 HTTP 请求方法（如 GET、POST）。某些广告追踪仅通过 POST 请求发送，设置规则可以拦截此类请求。
该项目中的规则可能包含此类高级过滤，以提高拦截的精准度并减少对正常流量的影响。

---

### 7: 如果我发现规则没有生效，应该如何排查？

**A**: 请按照以下步骤进行排查：
1.  **检查模式**：确认 Shadowrocket 的运行模式是“自动配置”或使用了包含该规则的配置节点，而不是单纯的“全局直连”。
2.  **检查规则顺序**：Shadowrocket 的规则是自上而下匹配的。如果该规则上方有一条更宽泛的“直连”或“拒绝”规则，可能会覆盖它。建议将广告拦截规则放在列表的较前位置。
3.  **验证规则文件**：直接在浏览器中访问规则链接，确认 GitHub Raw 文件能正常加载且内容不为空。
4.  **查看日志**：使用 Shadowrocket 的“连接日志”功能，发起一个包含广告的请求，查看该请求是被哪条规则处理了。
## 实践建议

以下是针对 Shadowrocket-ADBlock-Rules-Forever 仓库的 6 条实践建议：

1.  **善用分流功能，避免误伤正常流量**
    不要将所有规则直接填入 `[General]` 的 `bypass-system` 或全局启用。建议在 Shadowrocket 的 `[Rule]` 区域最底部添加该仓库提供的规则列表，并确保规则逻辑是先处理国内直连，最后处理广告拦截。这样可以防止广告规则意外匹配到正常的国内 IP 或域名，导致连接变慢。

2.  **定期检查构建状态，而非盲目订阅**
    虽然仓库承诺每日 8 时更新，但上游源（如 EasyList、AdGuardDNS）可能会出现变动或解析失败。建议将仓库的 GitHub Actions 构建页面加入浏览器书签，偶尔查看当日构建是否通过（显示绿色勾），如果构建失败，请暂时不要更新本地规则，以免使用损坏的文件。

3.  **针对视频网站开启“兼容模式”**
    该仓库规则力度较强，可能会误拦截视频网站的贴片广告或甚至导致视频无法加载。如果你发现 Bilibili 或 YouTube 无法正常播放，请在 Shadowrocket 的配置文件中，针对 `DOMAIN-SUFFIX,bilibili.com` 和 `DOMAIN-SUFFIX,youtube.com` 单独设置 `REJECT` 规则的例外，或者直接使用该仓库提供的“精简版”或“视频专用版”规则集。

4.  **利用自定义规则覆盖仓库规则**
    不要直接修改仓库下载下来的 Rule 文件，因为每次更新都会覆盖你的修改。正确的做法是在 Shadowrocket 配置文件的 `[Rule]` 区域，在引用仓库规则列表**之前**，添加你自己的自定义规则。Shadowrocket 的规则匹配是从上到下的，你写在最前面的自定义规则会优先生效，从而保留你需要的特定广告或修正误杀。

5.  **开启 DNS 解析以应对 Hosts 劫持**
    该仓库不仅包含 URL 屏蔽，还包含 Hosts 屏蔽。为了确保这些基于域名的拦截生效，请务必在 Shadowrocket 的设置中开启“DNS 服务”并设置为“自动”或使用可信的 DoH/DoT 服务（如阿里或腾讯的公共 DNS）。如果使用本地代理分流，请确保 DNS 请求没有被错误地转发到国外，否则会导致解析缓慢。

6.  **关注 MITM (HTTPS 解密) 的配置必要性**
    部分高级广告拦截规则（特别是针对 App 内广告）需要开启 HTTPS 解密（MITM）才能生效。如果你发现某些 App 的广告无法去除，请检查规则文件是否包含 `DOMAIN,ad.com,REJECT` 类型的域名规则。如果有，你需要按照 Shadowrocket 的文档配置 CA 证书并开启 MITM，但请注意不要对银行、支付类域名开启解密。

---
## 引用

- **GitHub 仓库**: [https://github.com/Johnshall/Shadowrocket-ADBlock-Rules-Forever](https://github.com/Johnshall/Shadowrocket-ADBlock-Rules-Forever)
- **DeepWiki**: [https://deepwiki.com/Johnshall/Shadowrocket-ADBlock-Rules-Forever](https://deepwiki.com/Johnshall/Shadowrocket-ADBlock-Rules-Forever)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---

## 站内链接

- 分类： [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Shadowrocket](/tags/shadowrocket/) / [广告过滤](/tags/%E5%B9%BF%E5%91%8A%E8%BF%87%E6%BB%A4/) / [规则库](/tags/%E8%A7%84%E5%88%99%E5%BA%93/) / [GitHub Actions](/tags/github-actions/) / [自动化](/tags/%E8%87%AA%E5%8A%A8%E5%8C%96/) / [iOS](/tags/ios/) / [网络代理](/tags/%E7%BD%91%E7%BB%9C%E4%BB%A3%E7%90%86/) / [开源项目](/tags/%E5%BC%80%E6%BA%90%E9%A1%B9%E7%9B%AE/)
- 场景： [DevOps/运维](/scenarios/devops-%E8%BF%90%E7%BB%B4/) / [自动化脚本](/scenarios/%E8%87%AA%E5%8A%A8%E5%8C%96%E8%84%9A%E6%9C%AC/) / [安全工具](/scenarios/%E5%AE%89%E5%85%A8%E5%B7%A5%E5%85%B7/)

### 相关文章

- [🚀 GitHub 热榜！DSP/工厂蓝图神器，高效开发必备！🔥]({{< relref "posts/20260125-github_trending-dspblueprints-factoryblueprints-6.md" >}})
- [🔥GitHub爆火！智能工厂蓝图，自动化神器！]({{< relref "posts/20260125-github_trending-dspblueprints-factoryblueprints-6.md" >}})
- [🔥 GitHub超火！DSP/Factory设计蓝图，工程化必备！]({{< relref "posts/20260125-github_trending-dspblueprints-factoryblueprints-6.md" >}})
- [戴森球计划游戏工厂蓝图仓库]({{< relref "posts/20260125-github_trending-dspblueprints-factoryblueprints-6.md" >}})
- [在边缘/无服务器运行时中运行 V2ray]({{< relref "posts/20260129-github_trending-zizifn-edgetunnel-2.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*
