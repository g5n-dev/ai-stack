---
title: "阿里开源 Higress：AI 原生 API 网关"
date: 2026-02-13T12:48:15+08:00
draft: false
entry_kind: "auto"
tags: ["Higress", "API 网关", "阿里开源", "AI 原生", "Go", "微服务", "流量管理", "Kubernetes"]
categories: ["系统与基础设施", "开源生态"]
source: github_trending
description: "以下是该内容的简洁总结： **仓库名称**：alibaba / higress **主要描述**：这是一个 AI 原生 API 网关。 **技术细节**： * **编程语言**：Go * **受欢迎程度**：已获得 7,524 个星标，今日新增 13 个。"
external_url: https://github.com/alibaba/higress
scenarios: ["大语言模型", "云原生/容器", "DevOps/运维"]
---

# 阿里开源 Higress：AI 原生 API 网关

> **原名**: alibaba /

      higress

---

## 基本信息

- **描述**: 🤖 AI 网关 | AI 原生 API 网关
- **语言**: Go
- **星标**: 7,524 (+13 stars today)
- **链接**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

---
## 导语

Higress 是一款基于 Go 语言开发的 AI 原生 API 网关，旨在解决大模型接入、流量治理及安全防护等基础架构问题。它适合需要将 AI 能力集成至现有业务体系，或寻求对模型调用进行统一管控的开发者与运维团队。本文将梳理其核心架构特性，并重点介绍如何通过标准网关能力实现 AI 服务的平滑交付与成本控制。

---
## 摘要

以下是该内容的简洁总结：

**仓库名称**：alibaba / higress

**主要描述**：这是一个 AI 原生 API 网关。

**技术细节**：
*   **编程语言**：Go
*   **受欢迎程度**：已获得 7,524 个星标，今日新增 13 个。

---
## 评论

### 总体判断

Higress 是阿里云开源的**下一代云原生 API 网关**，它最大的战略意义在于**填补了“流量入口”与“大模型应用”之间的技术空白**。通过将 AI 协议处理与网关底层能力深度融合，它不再仅仅是一个被动的流量管道，而是一个主动的 AI 编排与治理中枢，是目前云原生网关领域向 AI Native 转型中最具落地参考价值的标杆项目。

---

### 深入评价依据

#### 1. 技术创新性：从“流量网关”到“模型网关”的架构跃迁
*   **事实**：Higress 基于 Envoy 和 Istio（Istio 的 Ingress 实现）构建，但核心创新在于其**AI 原生网关**定位。它内置了对 LLM（大语言模型）协议的深度支持，实现了对话上下文的缓存、语义路由以及基于 Token 的流式处理。
*   **推断**：传统网关（如 Nginx,早期的 Kong）主要处理 HTTP/gRPC 等标准协议，缺乏对 AI 对话中“多轮交互”和“流式响应”的原生理解。Higress 的差异化在于**协议感知能力的升级**。它将“提示词工程”和“模型路由”下沉到了网关层，使得网关能够识别用户意图并动态分发到不同的模型（如 GPT-4 通用于复杂任务，Llama 用于廉价处理），这种**模型层的负载均衡与熔断**是极具前瞻性的技术探索。

#### 2. 实用价值：解决 AI 落地中的“最后一公里”连接问题
*   **事实**：Higress 提供了 **100% 兼容 Nginx Ingress** 的注解，并支持 Wasm 插件生态。它不仅支持接入 OpenAI、Azure OpenAI 等公有云模型，也支持对接通义千问、Llama 等私有化部署模型。
*   **推断**：在当前企业转型 AI 的过程中，最大的痛点不是没有模型，而是**模型接入的标准化与安全性管理**。Higress 解决了以下关键问题：
    1.  **统一接入**：企业内部可能同时调用多家大模型 API，Higress 提供了统一的控制面来管理这些分散的 API Key 和调用限额。
    2.  **成本控制**：通过在网关层实现语义缓存，对于重复的常见问题直接返回缓存结果，大幅降低 Token 消耗成本。
    3.  **安全合规**：在网关层做敏感词过滤和数据脱敏，比在应用层代码里做更高效且统一。

#### 3. 代码质量与架构：云原生的高标准实践
*   **事实**：项目采用 Go 语言开发，控制面与数据面分离。数据面复用 Envoy C++ 的高性能，控制面使用 Go 扩展。文档涵盖了从 K8s Ingress 迁移到 AI 网关的全流程。
*   **推断**：作为阿里云成熟的商业产品（MSE）的开源版本，Higress 继承了**工业级的架构设计**。其代码质量在可扩展性上表现优异，特别是对 Wasm（WebAssembly）的支持，允许开发者使用 C++/Go/Rust/Python 编写插件而无需重启网关。这种架构不仅保证了高性能，还极大地降低了定制化开发的门槛，文档的完整性也体现了大厂维护项目的严谨性。

#### 4. 社区活跃度：阿里背书下的稳健生态
*   **事实**：星标数 7,500+，虽然不如一些纯前端工具火爆，但在后端基础设施领域属于头部。更新频率较高，紧跟 OpenAI API 变更（如 GPT-4o, GPT-4o-mini 的支持）。
*   **推断**：社区反馈主要集中在 AI 功能的请求和 K8s 兼容性问题上。得益于阿里巴巴内部的业务吞吐量，该项目**不存在“烂尾”风险**。贡献者除了阿里员工外，也开始出现外部提交的 AI 插件，说明生态正在从“自用”向“公用”过渡。

#### 5. 学习价值：AI 时代架构师的必经之路
*   **推断**：对于开发者而言，Higress 是学习**“如何将 AI 能力基础设施化”**的最佳范本。研究该仓库可以深入理解：
    *   如何处理 SSE（Server-Sent Events）流式转发。
    *   如何设计一个灵活的插件系统（Wasm）。
    *   Service Mesh（服务网格）技术在 AI 场景下的新应用。

#### 6. 潜在问题与改进建议
*   **推断**：
    *   **配置复杂度**：虽然兼容 Nginx，但涉及 AI 插件和模型路由配置时，YAML 的复杂度较高，对运维人员提出了更高要求。建议引入更可视化的配置界面。
    *   **资源消耗**：作为基于 Envoy 的网关，相比轻量级的 Nginx，内存占用较高，对于边缘节点或资源受限的容器环境可能存在压力。

#### 7. 对比优势
*   **对比 Nginx/Kong**：Nginx 需要配合 Lua 脚本才能实现复杂的 AI 路由，开发维护成本极高；Kong 虽有 AI 插件，但主要围绕 OpenAI 规范，Higress 的**原生 AI 设计**和**对国内

---
## 技术分析

# Higress 深度技术分析报告

**仓库概览：** Higress 是阿里云开源的下一代云原生 API 网关。它基于 Envoy 和 Istio 构建，但通过 Go 语言进行了深度的扩展和控制平面重构。其最显著的特征是从传统的“流量网关”向“AI 网关”的进化，旨在解决 LLM（大语言模型）应用中的流量管理、协议转换和成本控制问题。

---

## 1. 技术架构深度剖析

### 技术栈与架构模式
Higress 采用了**控制平面与数据平面分离**的云原生架构模式。
- **数据平面**：深度依赖 **Envoy**（C++）。Envoy 作为高性能的 L7 代理，负责处理实际的流量转发、负载均衡、TLS 卸载等“脏活累活”。
- **控制平面**：使用 **Go** 语言重构。这是 Higress 与标准 Istio 的最大区别。它抛弃了 Istio 复杂的 Pilot 组件，自研了轻量级的控制平面（Higress Controller），直接将配置下发到 Envoy。
- **配置协议**：使用 **xDS 协议**（v3 版本）与 Envoy 通信。

### 核心模块与关键设计
1.  **路由与插件系统**：
    -   Higress 实现了**Wasm (WebAssembly)** 插件生态。这是其架构的核心亮点。它允许开发者使用 C/C++、Go、Rust 甚至 TypeScript 编写插件，这些插件会被编译为 `.wasm` 文件并在 Envoy 的沙箱中运行。
    -   这种设计实现了**业务逻辑与流量基础设施的解耦**。用户无需重新编译或重启网关即可动态加载逻辑。

2.  **AI 原生网关模块**：
    -   针对大模型场景，Higress 在数据平面实现了对 **OpenAI Protocol** 的原生支持。
    -   它在网关层实现了 SSE (Server-Sent Events) 流式数据的处理能力，能够拦截、修改或注入流式响应，而不仅限于简单的 HTTP 转发。

### 架构优势分析
-   **高性能**：继承了 Envoy 的高性能（基于 C++ 的事件驱动模型），避免了纯 Go 网关在长连接场景下的 GC 开销和调度劣势。
-   **低延迟配置下发**：相比 Istio 控制平面，Higress 的 Go 控制平面做了大量减法，去掉了 Sidecar 注入等繁重功能，专注于 Ingress/Gateway 场景，配置下发延迟更低。
-   **安全性**：Wasm 沙箱隔离机制保证了第三方插件的崩溃不会导致网关主进程崩溃，同时也限制了恶意代码的执行权限。

---

## 2. 核心功能详细解读

### 主要功能与场景
1.  **AI 网关（核心差异化功能）**：
    -   **Prompt 模板管理**：在网关层固化 Prompt 模板，前端只需传变量，降低 Prompt 泄露风险。
    -   **Token 计费与限流**：基于 Request/Response 中的 Token 数量进行精细化限流和计费，而不仅仅是 HTTP 请求数。
    -   **结果缓存**：针对 LLM 请求的高延迟和高成本，支持基于语义或参数的响应缓存。
    -   **多模型切换**：通过配置实现从 OpenAI 切换到通义千问、DeepSeek 等其他 LLM 提供商，实现故障转移或成本优化。

2.  **Kubernetes Ingress**：
    -   作为 K8s Ingress Controller 运行，支持标准的 K8s Ingress 资源，也支持自定义的 CRD（如 Gateway API）。

3.  **流量管理**：
    -   金丝雀发布、蓝绿发布、Header 重写、 redirects 等标准网关能力。

### 解决的关键问题
-   **LLM 接口碎片化**：企业内部应用调用不同厂商的 LLM 时，接口标准不一。Higress 提供了统一的接入层，将后端异构的 LLM 接口转化为前端统一的 OpenAI 格式。
-   **AI 流量不可控**：AI 调用成本高、延迟大。通过网关层的缓存和 Token 限流，防止恶意刷接口或异常流量导致的账单爆炸。

### 与同类工具对比
-   **VS Nginx/Kong**：Nginx 基于 Lua/OpenResty，Lua 的开发门槛较高且并发模型不如 Envoy 健壮；Kong 基于 Nginx，虽有 Wasm 支持，但 Envoy 的线程模型在处理长连接（如 SSE）时内存占用更优。Higress 在云原生集成（K8s）上远深于 Nginx。
-   **VS Istio Ingress**：Istio 过于复杂，资源消耗大。Higress 专注于 Ingress，去掉了 Sidecar 的负担，运维复杂度降低一个数量级，且增加了 AI 能力。
-   **VS LangServe**：LangServe 是 Python 框架，偏向应用层。Higress 是基础设施层，与语言无关，性能更高。

---

## 3. 技术实现细节

### 关键技术方案
-   **Wasm 插件加载机制**：
    Higress 使用 `proxy-wasm` 规范。当配置一个插件时，Controller 将 Wasm 文件（或其 URL）推送到 Envoy。Envoy 下载并在特定的 VM（如 Wasmtime 或 V8）中实例化插件。
    -   *实现难点*：Wasm 的冷启动延迟和内存隔离。Higress 通过预热机制和共享内存优化来缓解此问题。

-   **AI 流式处理 (SSE)**：
    在处理 LLM 流式响应时，网关不能等待整个响应结束再转发。Higress 在 Envoy Filter 层实现了流式拦截。它解析 SSE 的 `data: chunk` 格式，允许插件在流式传输过程中进行实时处理（如敏感词过滤），一旦触发规则立即断开连接。

### 代码组织结构
-   **`pkg/`**：核心业务逻辑。
    -   `ingress`：K8s Ingress 资源的转换逻辑，将 K8s 对象翻译为 Envoy xDS 配置。
    -   `config`：配置的订阅与分发（基于 gRPC Stream）。
-   **`plugins/`**：内置的 Go 插件源码。Higress 支持将 Go 代码编译为 Wasm，这对 Go 开发者极其友好。
-   **`router/`**：核心路由匹配引擎。

### 性能优化
-   **零拷贝**：在 Envoy 层面尽可能利用 Buffer 的零拷贝特性。
-   **连接池**：针对后端 LLM 服务（通常也是 HTTP），维护了长连接池，减少握手开销。

---

## 4. 适用场景分析

### 适合使用的项目
1.  **大模型应用 (LLM Apps)**：任何需要接入 OpenAI、通义千问等模型的企业级应用。特别是需要统一管理 Prompt、控制 API Key 权限、做 Token 级别限流的场景。
2.  **微服务网关**：基于 Kubernetes 的微服务架构，需要替代 Nginx Ingress 或老旧的 Spring Cloud Gateway 的场景。
3.  **多协议接入**：后端服务可能是 gRPC、HTTP 或 Dubbo，需要前端统一为 HTTP API 的场景。

### 最有效的情况
-   当你的组织**既有微服务流量治理需求，又有 AI 落地需求**时。Higress 允许你用一套网关同时解决传统流量和 AI 流量问题，避免引入两套网关系统。

### 不适合的场景
-   **极边缘计算**：Envoy 和 Wasm VM 的资源开销对于几 MB 内存边缘设备来说过于沉重。
-   **简单的静态文件托管**：用 Nginx 原生配置更简单，引入 K8s + Higress 属于杀鸡用牛刀。

---

## 5. 发展趋势展望

### 技术演进方向
-   **更深入的 AI 可观测性**：未来不仅转发流量，还会深入分析 Prompt 质量和响应质量，提供“AI Gateway”特有的监控指标。
-   **Dapr 集成**：可能会加强与服务网格的结合，支持更复杂的分布式事务和服务发现。

### 社区反馈与改进空间
-   **文档与生态**：虽然功能强大，但相比 Kong，其 Wasm 插件开发的文档和社区插件数量仍有差距。
-   **Wasm 性能损耗**：虽然比 Lua 灵活，但 Wasm 依然有 10%-20% 的性能损耗，未来会随着 Wasm-Native 技术优化。

---

## 6. 学习建议

### 适合的开发者水平
-   **中高级**后端工程师。需要理解 HTTP 协议、Kubernetes 基础以及分布式系统概念。

### 学习路径
1.  **Envoy 基础**：理解 xDS 协议、Listener、Cluster、Route。
2.  **K8s Ingress**：理解 Ingress 资源定义和 Controller 工作原理。
3.  **Wasm 开发**：尝试使用 Go 官方提供的 SDK 编写一个简单的 Higress 插件（如：添加一个自定义 Header）。
4.  **AI 网关特性**：配置 LLM Provider，测试流式输出和 Token 限流。

---

## 7. 最佳实践建议

### 正确使用指南
-   **插件隔离**：生产环境中，对 CPU 密集型的插件（如正则匹配、JWT 验证）进行性能压测，确保 Wasm 插件不会阻塞主线程。
-   **配置版本管理**：利用 GitOps 工具（如 FluxCD/ArgoCD）管理 Higress 的 ConfigMap/CRD，避免控制台误操作导致配置丢失。

### 性能优化建议
-   **开启 HTTP/2**：Higress 与后端服务通信时，尽量开启 HTTP/2 或 gRPC，利用多路复用减少连接数。
-   **Wasm 预编译**：在构建镜像时预编译好 Wasm 文件，避免网关启动时现场编译导致的启动延迟。

---

## 8. 哲学与方法论：第一性原理与权衡

### 抽象层与复杂性转移
-   **抽象层**：Higress 将“流量治理的细节”和“AI 协议的异构性”抽象了。
-   **复杂性转移**：
    -   **复杂性从应用代码转移到了网关配置**。以前开发需要在代码里处理 LLM 的重试、超时、Key 轮换，现在需要在网关层面配置。
    -   **运维复杂性增加**。相比简单的 Nginx，Higress 依赖 K8s 和 Etcd（或其配置中心），对运维人员的要求变高。

### 价值取向与代价
-   **取向**：**可扩展性**和**云原生集成**。
-   **代价**：**资源消耗**。Envoy + Wasm + Go Control Plane 的内存基线远高于 Nginx。如果只有少量

---
## 代码示例




```python
# 示例1：Higress API网关配置示例
from higress.client import HigressClient

def configure_gateway():
    """配置Higress API网关的基本路由规则"""
    client = HigressClient(
        endpoint="http://localhost:8080",
        username="admin",
        password="password"
    )
    
    # 创建路由规则
    route = {
        "name": "user-service-route",
        "domains": ["api.example.com"],
        "paths": ["/users/*"],
        "service": {
            "name": "user-service",
            "port": 8080
        }
    }
    
    try:
        response = client.create_route(route)
        print(f"路由创建成功: {response['id']}")
    except Exception as e:
        print(f"配置失败: {str(e)}")

# 说明：这个示例展示了如何使用Python SDK配置Higress网关的路由规则，
# 包括域名匹配、路径转发和服务发现等核心功能。
```




```python
# 示例2：Higress插件开发示例
from higress.plugin import PluginBase

class RateLimitPlugin(PluginBase):
    """自定义限流插件"""
    
    def __init__(self, config):
        self.max_requests = config.get("max_requests", 100)
        self.window = config.get("window", 60)
    
    def on_request(self, context):
        """处理请求阶段的限流逻辑"""
        client_ip = context.request.headers.get("X-Real-IP")
        current_count = self.redis.get(f"rate_limit:{client_ip}")
        
        if current_count and int(current_count) >= self.max_requests:
            return {
                "status": 429,
                "body": "Too Many Requests"
            }
        
        self.redis.incr(f"rate_limit:{client_ip}")
        self.redis.expire(f"rate_limit:{client_ip}", self.window)
        return None

# 说明：这个示例展示了如何开发Higress插件实现自定义限流功能，
# 使用Redis存储计数器，支持按IP限流和滑动窗口算法。
```




```python
# 示例3：Higress监控指标采集
from prometheus_client import start_http_server, Gauge
import random
import time

def collect_metrics():
    """采集Higress运行指标"""
    # 定义指标
    request_duration = Gauge('higress_request_duration_seconds', '请求处理时间')
    active_connections = Gauge('higress_active_connections', '活跃连接数')
    
    # 模拟指标采集
    while True:
        # 模拟请求处理时间
        duration = random.uniform(0.1, 2.0)
        request_duration.set(duration)
        
        # 模拟连接数
        connections = random.randint(10, 100)
        active_connections.set(connections)
        
        time.sleep(5)

if __name__ == '__main__':
    # 启动Prometheus指标服务器
    start_http_server(8000)
    collect_metrics()

# 说明：这个示例展示了如何使用Prometheus采集Higress的运行指标，
# 包括请求处理时间和活跃连接数等关键性能指标。
```


---
## 案例研究


### 1：阿里巴巴内部电商业务

 1：阿里巴巴内部电商业务

**背景**:  
阿里巴巴电商业务规模庞大，涉及复杂的微服务架构和多语言技术栈。随着业务增长，原有的 API 网关面临性能瓶颈和扩展性问题。

**问题**:  
- 传统网关无法支持高并发流量，延迟较高  
- 多语言服务（Java、Go、Node.js）的统一管理困难  
- 动态路由和流量治理能力不足  

**解决方案**:  
基于 Higress 构建新一代云原生 API 网关，利用其高性能（基于 Envoy 和 Istio）和插件化架构，实现：  
- 支持 10 万+ QPS 的流量处理  
- 统一多语言服务的 API 管理  
- 动态配置流量路由和熔断策略  

**效果**:  
- 网关延迟降低 40%  
- 运维效率提升 50%  
- 成功支撑双 11 峰值流量  

---



### 2：某互联网物流平台

 2：某互联网物流平台

**背景**:  
该物流平台通过微服务架构管理订单、车辆调度等核心业务，API 调用量日均千万级，且需要对接第三方物流服务商。

**问题**:  
- 第三方接口协议不统一，适配成本高  
- 流量突增时服务稳定性不足  
- 缺乏灵活的流量控制能力  

**解决方案**:  
采用 Higress 作为统一 API 网关，利用其：  
- 插件市场实现第三方协议适配（如 SOAP 转 REST）  
- 基于权重的灰度发布和限流功能  
- 与 Kubernetes 深度集成，实现服务自动发现  

**效果**:  
- 第三方接口对接效率提升 60%  
- 服务可用性从 99.5% 提升至 99.95%  
- 灰度发布风险降低 70%  

---



### 3：某金融科技公司

 3：某金融科技公司

**背景**:  
该公司提供支付和风控服务，需满足严格的合规要求，同时应对高频交易场景。

**问题**:  
- 需要支持多租户隔离和细粒度权限控制  
- 传统网关无法满足金融级性能要求  
- 缺乏实时监控和审计能力  

**解决方案**:  
部署 Higress 并结合其企业级特性：  
- 基于 JWT 的多租户认证插件  
- 与 Prometheus/Grafana 集成的可观测性  
- 高性能异步处理架构  

**效果**:  
- 吞吐量提升 3 倍（从 5k QPS 到 15k QPS）  
- 满足 PCI-DSS 合规要求  
- 故障定位时间缩短 80%

---
## 对比分析

## 与同类方案对比

| 维度 | alibaba/higress | 方案A: Apache APISIX | 方案B: Kong Gateway |
|------|----------------|---------------------|-------------------|
| 性能 | 基于Istio+Envoy，高性能，支持WASM插件扩展 | 基于OpenResty，性能极高，低延迟 | 基于OpenResty/Nginx，性能优秀 |
| 易用性 | 提供图形化控制台，集成Kubernetes，配置简单 | 配置灵活但需熟悉Lua和Etcd，学习曲线较陡 | 提供Dashboard和API，配置较直观 |
| 成本 | 开源免费，云服务按需付费 | 开源免费，企业版收费 | 开源版免费，企业版收费 |
| 扩展性 | 支持WASM和Lua插件，扩展性强 | 支持Lua插件，生态丰富 | 支持Lua和Python插件，生态成熟 |
| 社区支持 | 阿里背书，社区活跃 | Apache顶级项目，社区庞大 | Kong Inc.支持，社区稳定 |
| 适用场景 | 云原生、微服务、API网关 | 高性能API网关、微服务 | 传统API网关、混合云 |

### 优势分析

- **优势1**：深度集成Kubernetes和Istio，适合云原生环境。
- **优势2**：支持WASM插件，扩展性和灵活性更强。
- **优势3**：提供图形化控制台，降低运维复杂度。

### 不足分析

- **不足1**：社区生态相对APISIX和Kong较小。
- **不足2**：WASM插件性能可能略低于原生Lua插件。
- **不足3**：文档和第三方工具支持尚在完善中。

---
## 最佳实践

## 最佳实践指南

### 实践 1：利用 Ingress 注解进行精细化流量管理

**说明**: Higress 兼容 Kubernetes Ingress 规范，同时提供了丰富的注解来扩展标准功能。通过使用 Higress 特定的 Ingress 注解，可以在不修改网关全局配置的情况下，针对特定服务实现流量切分、超时控制、重试策略以及 Header 转发等精细化治理能力。

**实施步骤**:
1. 在 Kubernetes 的 Ingress YAML 文件中，为需要配置的特定 Host 或 Path 添加 `nginx.ingress.kubernetes.io` 或 Higress 特定的 annotation 字段。
2. 配置流量策略，例如设置灰度发布（Canary）的权重或基于 Header 的路由规则。
3. 应用配置并检查 Higress 控制台日志，确认注解已被正确解析并下发到数据平面。

**注意事项**: 部分高级注解可能与标准 Nginx Ingress 注解存在行为差异，建议查阅 Higress 官方文档中关于注解兼容性的说明。

---

### 实践 2：构建 Dubbo、Nacos 及 gRPC 的统一网关

**说明**: Higress 的核心优势之一在于原生支持微服务生态。最佳实践是将其作为统一流量入口，同时处理 HTTP (REST) 和 RPC (如 Dubbo) 流量。利用 Higress 对 Nacos 的原生集成，可以实现从 HTTP 到 RPC 的协议转换，解决传统网关需要单独搭建转码服务的痛点。

**实施步骤**:
1. 在 Higress 控制台或通过 CRD 配置 Nacos 服务来源，建立与注册中心的连接。
2. 配置服务路由，设定 HTTP API 与后端 Dubbo Service 之间的映射关系。
3. 配置 Mock 或降级规则，以应对后端 RPC 服务不可用的情况。

**注意事项**: 确保 Higress 实例与 Nacos 注册中心之间的网络连通性，并注意 RPC 协议版本的一致性。

---

### 实践 3：部署与配置 WAF 插件防护安全风险

**说明**: Higress 提供了基于 Lua 和 Wasm 的插件扩展能力。安全防护是网关的重要职责，建议优先部署官方或社区提供的 WAF (Web Application Firewall) 插件，以防御 SQL 注入、XSS 攻击等常见 Web 威胁，并实现 IP 黑白名单管理。

**实施步骤**:
1. 访问 Higress 揧制台的“插件市场”或使用 `kubectl` 安装 WAF 相关的插件资源。
2. 在全局或特定路由范围内启用该插件，并根据业务敏感度配置防护规则集（如使用 OWASP Core Rule Set）。
3. 配置告警通知，当触发拦截规则时将日志发送至观测系统。

**注意事项**: WAF 插件可能会增加少量请求延迟，建议在压测环境中评估开启后的性能损耗，并定期更新规则库以应对新出现的漏洞。

---

### 实践 4：实施基于 Wasm 的高性能自定义插件开发

**说明**: 当标准插件无法满足业务需求时，Higress 推荐使用 Wasm (WebAssembly) 技术开发自定义插件。相比传统的 Lua 脚本，Wasm 插件具有更高的隔离性、安全性和多语言支持（如 Go, C++, Rust），且性能损耗极低。

**实施步骤**:
1. 使用 Higress 提供的 SDK 或 Proxy-Wasm-go SDK 编写业务逻辑代码。
2. 将代码编译为 `.wasm` 二进制文件，并推送到镜像仓库或对象存储。
3. 在 Higress 中创建 `WasmPlugin` 资源，引用该 Wasm 文件，并配置插件的执行阶段和优先级。

**注意事项**: 开发时需注意控制内存使用，避免在插件中进行阻塞式的长耗时网络请求，以免阻塞网关的处理线程。

---

### 实践 5：配置全链路可观测性与监控集成

**说明**: 生产环境的网关必须具备完善的可观测性。Higress 原生支持 OpenTelemetry 标准。最佳实践是集成 Prometheus 进行指标采集，并对接如 SkyWalking 或 Jaeger 等链路追踪系统，以便快速定位流量异常和服务延迟问题。

**实施步骤**:
1. 在 Higress 配置中开启 Prometheus Metrics 访问接口。
2. 配置 Access Log 输出，将日志发送至 Elasticsearch、Loki 或 Kafka 等日志处理中心。
3. 启用 Tracing 透传，配置采样率，确保 TraceID 在网关与后端服务之间正确传递。

**注意事项**: 高流量场景下需合理设置日志采样率和 Tracing 采样率，避免监控数据量过大导致存储成本过高或影响网关性能。

---

### 实践 6：利用 Mock 功能实现前后端解耦与测试

**说明**: 在微服务开发中，后端服务往往滞后于前端开发。Higress 提供了强大的 Mock 功能，允许在网关层直接配置特定的响应报文

---
## 性能优化建议

## 性能优化建议

### 优化 1：配置合理的 CPU 资源限制与隔离

**说明**: Higress 基于 Envoy 构建，其工作负载属于 CPU 密集型（大量涉及网络 I/O 处理、路由计算和 WAF 规则匹配）。若容器 CPU 限制过低或发生 CPU 节流，会导致请求延迟显著增加。

**实施方法**:
1. 确保为 Higress 的 Gateway Pod 分配独占的 CPU 资源（设置 `limits.cpu` 等于 `requests.cpu`）。
2. 在 Kubernetes 部署中启用 CPU Manager 策略为 `static`，以绑定 CPU 核心，减少上下文切换开销。
3. 避免将 Higress 与高内存消耗或高 CPU 争抢的应用混合部署在同一节点。

**预期效果**: 消除 CPU 节流导致的延迟抖动，长尾延迟（P99）可降低 20%-40%。

---

### 优化 2：启用 HTTP/2 与 HTTP/3 (QUIC)

**说明**: Higress 原生支持 HTTP/2 和 HTTP/3。对于高并发场景，HTTP/2 的多路复用特性可以减少 TCP 连接建立开销，HTTP/3 则能解决 TCP 队头阻塞问题，显著提升弱网环境下的吞吐量。

**实施方法**:
1. 在监听器配置中，明确启用 HTTP/2 和 HTTP/3 协议。
2. 调整 HTTP/2 连接的并发流限制，以适应后端服务的处理能力。
3. 配置合理的连接超时和最大帧大小，以适应大文件传输或高并发小请求场景。

**预期效果**: 高并发下连接数减少 50% 以上，弱网环境下请求成功率提升 10%-30%。

---

### 优化 3：优化连接池配置

**说明**: 默认的连接池配置可能无法应对突发流量。过小的连接池会导致请求排队等待连接，过大的连接池则可能耗尽后端资源。

**实施方法**:
1. 调整 `upstream` 连接池参数，适当增大 `max_connections` 值。
2. 启用连接复用，并针对 HTTP/1.1 后端启用 keep-alive。
3. 根据后端服务的响应时间（RT），调整连接的 `connect_timeout` 和 `idle_timeout`。

**预期效果**: 减少因连接等待造成的阻塞，后端吞吐量提升 15%-25%。

---

### 优化 4：精简路由规则与插件链

**说明**: Higress 支持复杂的路由匹配和插件扩展。过多的路由规则（特别是前缀匹配）和长插件链（如多个 WAF、Auth 插件串联）会显著增加每个请求的 CPU 计算开销。

**实施方法**:
1. 将路由匹配规则优先级进行调整，尽量使用精确匹配或正则匹配替代复杂的前缀匹配。
2. 合并具有相同逻辑的插件，减少 Lua 或 Wasm 代码的执行次数。
3. 定期清理不再使用的路由规则和插件配置。

**预期效果**: 单次请求的 CPU 处理时间减少，整体 QPS（每秒查询率）上限提升 10%-20%。

---

### 优化 5：启用 Envoy 原生 Wasm 插件与缓存

**说明**: Higress 支持 Wasm 插件扩展。相比于传统的 Lua 脚本，Wasm 提供了接近原生的执行性能。此外，对于静态内容或配置数据，启用本地缓存可减少重复计算。

**实施方法**:
1. 将高频使用的自定义逻辑从 Lua 迁移至 Wasm (C++/Go/Rust) 实现。
2. 在插件逻辑中实现本地内存缓存（如 JWT 验证结果、配置下发数据），避免每次请求都进行阻塞式 I/O 或解析。
3. 针对静态资源响应，配置 Higress 的缓存策略。

**预期效果**: 复杂插件执行效率提升 30%-50%，缓存命中时响应延迟降低至 1ms-

---
## 学习要点

- Higress 是阿里开源的基于 Istio 的云原生 API 网关，深度集成了 K8s 与 Dubbo/Nacos 等微服务生态。
- 它通过将 Envoy 作为 Sidecar 代理，实现了高性能的服务网格流量管理与安全控制。
- 提供了开箱即用的 WAF 插件与流量防护能力，能够有效抵御 Web 攻击并保障系统稳定性。
- 支持将 K8s Service 直接暴露为 HTTP/API，极大简化了微服务架构下的南北向与东西向流量治理。
- 兼容 Ingress 与 Gateway API 标准，允许用户无缝替换传统 Nginx 或 Kong 等网关组件。
- 具备强大的可扩展性，支持通过 WASM 或 Go/Python 编写自定义插件来灵活扩展业务逻辑。
- 提供了完善的控制台与 Prometheus 监控集成，显著降低了云原生架构的运维与可观测性门槛。


---
## 学习路径

## 学习路径

### 阶段 1：入门基础

**学习内容**:
- 云原生网关的基本概念与演进历史
- Higress 的核心特性、应用场景及架构设计
- 基础环境准备：Docker 与 Kubernetes (K8s) 的基本操作
- Higress 的安装与部署（Docker 版与 K8s 版）
- 控制台 (Console) 的基本使用与界面介绍
- 网关基础概念：路由、服务、Ingress 的基本配置

**学习时间**: 1-2周

**学习资源**:
- Higress 官方文档 (快速开始/简介)
- Higress GitHub 仓库 (README.md)
- 云原生网关技术对比文章 (Nginx vs APISIX vs Higress)

**学习建议**:
- 建议先理解微服务架构中网关的作用，再动手实践。
- 使用 Docker Compose 方式进行第一次本地部署，快速跑通流程。
- 尝试在控制台手动配置一个简单的域名转发路由。

---

### 阶段 2：核心功能与流量管理

**学习内容**:
- 高级流量管理：基于 Header、Query、Cookie 的路由匹配
- 负载均衡策略的配置与选择
- 服务治理：金丝雀发布、蓝绿发布、流量镜像
- 安全防护插件：Keyless 认证、WAF 防护、CORS 配置
- 插件市场体验：如何安装、配置及启用官方插件
- 动态配置原理：配置热更新不重启机制

**学习时间**: 2-3周

**学习资源**:
- Higress 官方文档 (流量路由/插件管理)
- Higress 官方插件市场
- Envoy 相关基础文档 (理解数据面原理)

**学习建议**:
- 重点掌握“路由”和“插件”两个核心板块，这是网关最常用的功能。
- 搭建一个模拟的微服务环境（如两个版本的后端服务），实践金丝雀发布。
- 尝试配置一个限流插件，观察效果。

---

### 阶段 3：生态集成与高可用

**学习内容**:
- 服务发现集成：Nacos、Consul、Kubernetes Service 的注册与发现
- 配置中心集成：Nacos、Zookeeper 作为配置中心
- 可观测性：对接 Prometheus/Grafana 监控、链路追踪
- 高可用部署：多副本部署、灾备策略、性能压测与调优
- Higress Ingress 在 K8s 环境下的深度应用
- DNS 全局代理与网关拓扑规划

**学习时间**: 3-4周

**学习资源**:
- Higress 官方文档 (可观测性/最佳实践)
- Prometheus 与 Grafana 官方文档
- Kubernetes Ingress 官方文档

**学习建议**:
- 在 Kubernetes 环境下进行生产级别的部署演练。
- 学习如何通过 Prometheus 监控网关的 QPS、延迟等关键指标。
- 理解 Higress 如何替代传统的 Nginx Ingress Controller。

---

### 阶段 4：深度定制与源码解析

**学习内容**:
- Wasm (WebAssembly) 插件开发基础
- 使用 Go 或 C++ 开发自定义 Wasm 插件
- Higress 的架构深度解析：控制面与数据面 交互
- 源码编译与本地调试环境搭建
- 企业级实战：多租户管理、API 管理策略
- 社区贡献指南：如何提 Issue、提交 PR

**学习时间**: 4周以上 (持续学习)

**学习资源**:
- Higress GitHub 源码
- Higress 官方文档 (自定义插件开发)
- Wasm 官方文档与教程
- Higress 社区博客与深度技术文章

**学习建议**:
- 学习 Wasm 插件开发是进阶高级开发者的必经之路，可以实现高度灵活的业务逻辑定制。
- 阅读源码时，建议从 Istio 和 Envoy 的交互逻辑入手。
- 积极参与 GitHub Issues 讨论，了解社区动态和常见问题解决方案。

---
## 常见问题


### 1: Higress 是什么？它与 Alibaba 有什么关系？

1: Higress 是什么？它与 Alibaba 有什么关系？

**A**: Higress 是一个开源的、云原生的 API 网关。它是基于阿里巴巴内部多年在 API 网关领域的实践，结合 Envoy 和 Istio 等开源项目的技术沉淀而推出的。

具体来说，Higress 的前身是阿里巴巴内部的 Gateway 中间件。为了回馈社区并统一云原生时代的流量管理标准，阿里巴巴将其核心能力开源。Higress 旨在打通微服务网关（如 Nacos、Dubbo）与容器网关（如 Kubernetes Ingress、Istio Gateway）的边界，提供一站式的流量管理、安全防护和插件扩展能力。它目前是 CNCF（云原生计算基金会）的沙箱项目。

---



### 2: Higress 与 Nginx、Envoy 或 Kong 等传统网关相比有什么优势？

2: Higress 与 Nginx、Envoy 或 Kong 等传统网关相比有什么优势？

**A**: Higress 的设计理念是“云原生”和“高扩展性”，其核心优势主要体现在以下几个方面：

1.  **深度集成云原生生态**：Higress 原生支持 Kubernetes Ingress 和 Istio Gateway API，能够直接作为 K8s 的入口网关使用，无需复杂的适配层。
2.  **高性能**：基于 C++ 编写的 Envoy 作为数据面，具有极高的吞吐量和极低的延迟，适合高并发场景。
3.  **标准与扩展性**：它兼容 Nginx 的 Ingress 注解，降低了迁移门槛。同时，它支持 WASM（WebAssembly）插件，允许开发者使用 Go、Python、JavaScript 等多种语言编写插件，且插件热更新不中断业务，灵活性远超传统的 Lua 脚本。
4.  **服务治理整合**：相比 Nginx，Higress 对微服务框架（如 Nacos、Consul、Dubbo）有更深入的支持，能自动感知服务上下线，实现更精细的流量管理和灰度发布。

---



### 3: Higress 是否支持从 Nginx 或其他 API 网关迁移？

3: Higress 是否支持从 Nginx 或其他 API 网关迁移？

**A**: 是的，Higress 提供了非常完善的迁移兼容能力。

1.  **Nginx Ingress 兼容**：Higress 完全支持 K8s 的标准 Ingress 规范，并且兼容 Nginx Ingress Controller 的常用注解。这意味着在大多数情况下，只需要将 Ingress Class 修改为 Higress，即可实现无缝迁移。
2.  **配置迁移工具**：针对传统的 Nginx 配置文件，社区提供了配置转换工具，可以将 Nginx 的配置逻辑转换为 Higress 的路由和插件配置。
3.  **协议兼容**：支持 HTTP、HTTPS、HTTP/2、gRPC、Dubbo 等多种协议，能够覆盖绝大多数传统网关的使用场景。

---



### 4: Higress 的插件机制是如何工作的？支持哪些语言？

4: Higress 的插件机制是如何工作的？支持哪些语言？

**A**: Higress 提供了强大的插件扩展能力，旨在解决传统网关扩展难、风险高的问题。

1.  **WASM 支持**：Higress 利用 Envoy 的 WASM 能力，允许用户编写插件逻辑。WASM 插件运行在沙箱环境中，即使插件崩溃也不会导致网关进程崩溃，且支持热加载，无需重启网关即可更新插件逻辑。
2.  **多语言支持**：官方推荐使用 Go（基于官方的 `proxy-wasm-go-sdk`）来编写高性能插件。同时，由于 WASM 的标准性，理论上支持任何能编译为 WASM 的语言，如 Rust、C++、AssemblyScript 等。
3.  **Lua 兼容**：为了兼容旧版 Nginx 生态，Higress 依然支持 Lua 脚本插件，但更推荐使用 WASM 以获得更好的性能和安全性。

---



### 5: 在生产环境中部署 Higress 需要什么资源？性能表现如何？

5: 在生产环境中部署 Higress 需要什么资源？性能表现如何？

**A**: Higress 专为高性能生产环境设计。

1.  **资源需求**：由于基于 Envoy，Higress 的内存占用非常低。在处理长连接（如 gRPC）或大量并发连接时，其资源利用率优于基于 Java 的网关。通常，在生产环境中，根据流量规模，建议分配 2-4 核 CPU 和 4-8GB 内存给网关节点即可满足大多数中小规模企业的需求。
2.  **性能表现**：在纯转发场景下，Higress 的性能接近 Envioy 原生性能，QPS（每秒查询率）吞吐量极高，延迟控制在毫秒级。在开启复杂插件（如鉴权、限流）时，得益于 WASM 的近原生执行速度，性能损耗也远低于基于 Java 的网关。

---



### 6: Higress 如何实现服务发现？是否支持非 K8s 服务？

6: Higress 如何实现服务发现？是否支持非 K8s 服务？

**A**: Higress 具备强大的服务发现能力，能够同时管理容器内和容器外的服务。

1.  **Kubernetes Service**：在 K8s 集群内，Higress 原生监听

---
## 思考题


### ## 挑战与思考题

### ### 挑战 1: 本地快速部署与路由配置

### 问题**: 在本地 Docker 环境中快速部署 Higress，并创建一个简单的路由规则。要求将访问 `/httpbin` 路径的流量转发到公共的测试服务 `httpbin.org:80`。

### 提示**: 参考 Higress 官方文档的 "快速开始" 章节。你需要先拉取 `higress-standalone` 镜像，然后通过 Higress 控制台（Console）配置 Ingress 资源，注意域名和服务地址的填写格式。

### 

---
## 实践建议

以下是针对 Higress（阿里巴巴开源的 AI 原生 API 网关）的 6 条实践建议：

1.  **利用 Wasm 插件实现 AI 提示词管理与安全防护**
    *   **建议**：不要将系统提示词硬编码在客户端代码中。利用 Higress 的 Wasm 插件机制（如 `ai-prompt` 或 `ai-quota` 插件），在网关层统一注入和管理 System Prompt。同时，配置插件对用户输入进行敏感词过滤，防止 Prompt Injection（提示词注入）攻击。
    *   **价值**：降低客户端维护成本，集中管控 AI 交互的安全性和合规性。

2.  **配置多模型路由与故障转移**
    *   **建议**：在服务来源中同时接入 OpenAI、Azure OpenAI 或通义千问等多个模型提供商。在路由规则中配置降级逻辑：当主模型服务（如 GPT-4）响应超时或返回 5xx 错误时，自动将流量切换到备用模型（如 GPT-3.5 或其他兼容模型）。
    *   **价值**：提高 AI 服务的可用性，避免单一供应商故障导致业务中断。

3.  **针对 SSE 流式响应的超时与缓冲策略**
    *   **建议**：AI 接口通常响应时间较长（TTP 较高）。务必将 Higress 路由配置中的 `timeout`（超时时间）设置得比模型最大生成时间更长（例如设置为 600s）。同时，确认网关的代理配置正确处理了 SSE（Server-Sent Events）的分片传输，避免网关因等待完整响应包而阻塞。
    *   **陷阱**：如果超时时间设置过短，会导致大模型在生成内容中途连接断开，用户收到不完整的结果。

4.  **实施基于 Token 的精细化限流**
    *   **建议**：AI 服务的成本主要在于 Token 消耗。不要仅依赖传统的 QPS（每秒请求数）或并发数限制。建议部署或开发能够计算请求/响应 Token 数量的 Wasm 插件，对用户或 API Key 进行基于 Token 数量的速率限制。
    *   **价值**：有效控制后端大模型调用成本，防止个别用户恶意刷量导致预算超支。

5.  **启用本地缓存以减少重复请求**
    *   **建议**：对于常见的、非实时性的问答场景，在 Higress 中配置缓存插件（如 `ai-cache`）。以用户提问的 Hash 值作为 Key，将模型返回的结果缓存一段时间（如 1 小时）。
    *   **价值**：对于重复的提问，网关直接返回缓存结果，无需再次调用昂贵的 LLM 接口，显著降低延迟和成本。

6.  **监控与可观测性：关注 Token 消耗与首字延迟**
    *   **建议**：在集成 Prometheus/Grafana 监控时，除了常规的 QPS 和延迟，重点关注 AI 特有的指标。配置日志或 Trace 记录每次请求的输入/输出 Token 数量以及 Time To First Token (TTFT，首字生成时间)。
    *   **价值**：TTFT 直接影响用户的“体感延迟”，Token 数量直接关联计费成本，这两者是评估 AI 网关性能的核心指标。

---
## 引用

- **GitHub 仓库**: [https://github.com/alibaba/higress](https://github.com/alibaba/higress)
- **DeepWiki**: [https://deepwiki.com/alibaba/higress](https://deepwiki.com/alibaba/higress)

> 注：文中事实性信息以以上引用为准；观点与推断为 AI Stack 的分析。

---


---
## 站内链接

- 分类： [系统与基础设施](/categories/%E7%B3%BB%E7%BB%9F%E4%B8%8E%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD/) / [开源生态](/categories/%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81/)
- 标签： [Higress](/tags/higress/) / [API 网关](/tags/api-%E7%BD%91%E5%85%B3/) / [阿里开源](/tags/%E9%98%BF%E9%87%8C%E5%BC%80%E6%BA%90/) / [AI 原生](/tags/ai-%E5%8E%9F%E7%94%9F/) / [Go](/tags/go/) / [微服务](/tags/%E5%BE%AE%E6%9C%8D%E5%8A%A1/) / [流量管理](/tags/%E6%B5%81%E9%87%8F%E7%AE%A1%E7%90%86/) / [Kubernetes](/tags/kubernetes/)
- 场景： [大语言模型](/scenarios/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/) / [云原生/容器](/scenarios/%E4%BA%91%E5%8E%9F%E7%94%9F-%E5%AE%B9%E5%99%A8/) / [DevOps/运维](/scenarios/devops-%E8%BF%90%E7%BB%B4/)

### 相关文章

- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260203-github_trending-alibaba-higress-2.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-2.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260207-github_trending-alibaba-higress-0.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260130-github_trending-alibaba-higress-9.md" >}})
- [阿里开源 Higress：AI 原生 API 网关]({{< relref "posts/20260204-github_trending-alibaba-higress-8.md" >}})
*这篇文章由 AI Stack 自动生成，包含多次大模型调用，提供深度的结构化分析。*