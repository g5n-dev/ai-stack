"""
AI Stack Technology Graph Data
技术栈图谱数据 - 定义5层技术栈结构和节点关系
"""

from typing import List, Dict, Optional
import json

# 5层技术栈定义
# 1. 编程语言层 (language)
# 2. 框架层 (framework)
# 3. 模型层 (model)
# 4. 应用层 (application)
# 5. 场景层 (scenario)

TECH_LAYERS = {
    "language": {
        "name": "编程语言",
        "level": 1,
        "color": "#4db6ac"
    },
    "framework": {
        "name": "框架层",
        "level": 2,
        "color": "#26a69a"
    },
    "model": {
        "name": "模型层",
        "level": 3,
        "color": "#d97706"
    },
    "application": {
        "name": "应用层",
        "level": 4,
        "color": "#8b5cf6"
    },
    "scenario": {
        "name": "场景层",
        "level": 5,
        "color": "#ec4899"
    }
}

# 编程语言节点
LANGUAGE_NODES = [
    {"id": "python", "name": "Python", "layer": "language", "category": "language"},
    {"id": "typescript", "name": "TypeScript", "layer": "language", "category": "language"},
    {"id": "javascript", "name": "JavaScript", "layer": "language", "category": "language"},
    {"id": "go", "name": "Go", "layer": "language", "category": "language"},
    {"id": "rust", "name": "Rust", "layer": "language", "category": "language"},
    {"id": "java", "name": "Java", "layer": "language", "category": "language"},
    {"id": "cpp", "name": "C++", "layer": "language", "category": "language"},
    {"id": "swift", "name": "Swift", "layer": "language", "category": "language"},
]

# 框架节点
FRAMEWORK_NODES = [
    # Python框架
    {"id": "pytorch", "name": "PyTorch", "layer": "framework", "category": "ml", "lang": "python"},
    {"id": "tensorflow", "name": "TensorFlow", "layer": "framework", "category": "ml", "lang": "python"},
    {"id": "django", "name": "Django", "layer": "framework", "category": "web", "lang": "python"},
    {"id": "fastapi", "name": "FastAPI", "layer": "framework", "category": "web", "lang": "python"},
    {"id": "flask", "name": "Flask", "layer": "framework", "category": "web", "lang": "python"},
    {"id": "langchain", "name": "LangChain", "layer": "framework", "category": "ai", "lang": "python"},
    {"id": "transformers", "name": "Transformers", "layer": "framework", "category": "ai", "lang": "python"},

    # JavaScript/TypeScript框架
    {"id": "react", "name": "React", "layer": "framework", "category": "frontend", "lang": "typescript"},
    {"id": "vue", "name": "Vue", "layer": "framework", "category": "frontend", "lang": "javascript"},
    {"id": "nextjs", "name": "Next.js", "layer": "framework", "category": "frontend", "lang": "typescript"},
    {"id": "nuxt", "name": "Nuxt", "layer": "framework", "category": "frontend", "lang": "typescript"},
    {"id": "svelte", "name": "Svelte", "layer": "framework", "category": "frontend", "lang": "typescript"},

    # Go框架
    {"id": "gin", "name": "Gin", "layer": "framework", "category": "backend", "lang": "go"},
    {"id": "echo", "name": "Echo", "layer": "framework", "category": "backend", "lang": "go"},

    # Rust框架
    {"id": "axum", "name": "Axum", "layer": "framework", "category": "backend", "lang": "rust"},
    {"id": "actix", "name": "Actix", "layer": "framework", "category": "backend", "lang": "rust"},
]

# 模型节点
MODEL_NODES = [
    {"id": "llm", "name": "大语言模型", "layer": "model", "category": "nlp", "icon": "auto_awesome"},
    {"id": "cv", "name": "计算机视觉", "layer": "model", "category": "vision", "icon": "visibility"},
    {"id": "nlp", "name": "自然语言处理", "layer": "model", "category": "nlp", "icon": "chat"},
    {"id": "diffusion", "name": "扩散模型", "layer": "model", "category": "generative", "icon": "gradient"},
    {"id": "multimodal", "name": "多模态模型", "layer": "model", "category": "multimodal", "icon": "view_in_ar"},
    {"id": "embedding", "name": "向量嵌入", "layer": "model", "category": "embedding", "icon": "scatter_plot"},
]

# 应用节点
APPLICATION_NODES = [
    {"id": "rag", "name": "RAG应用", "layer": "application", "category": "ai", "icon": "library_books"},
    {"id": "agent", "name": "AI Agent", "layer": "application", "category": "ai", "icon": "smart_toy"},
    {"id": "chatbot", "name": "聊天机器人", "layer": "application", "category": "ai", "icon": "forum"},
    {"id": "webapp", "name": "Web应用", "layer": "application", "category": "web", "icon": "web"},
    {"id": "api", "name": "API服务", "layer": "application", "category": "backend", "icon": "api"},
    {"id": "dashboard", "name": "数据仪表板", "layer": "application", "category": "data", "icon": "dashboard"},
    {"id": "automation", "name": "自动化工具", "layer": "application", "category": "tools", "icon": "auto_fix"},
    {"id": "monitoring", "name": "监控系统", "layer": "application", "category": "devops", "icon": "monitor_heart"},
]

# 场景节点 (复用 scenarios.py 的数据)
SCENARIO_NODES = [
    # Web开发
    {"id": "web_dev", "name": "Web应用开发", "layer": "scenario", "category": "web", "icon": "web"},
    {"id": "frontend", "name": "前端开发", "layer": "scenario", "category": "web", "icon": "desktop_windows"},
    {"id": "backend", "name": "后端开发", "layer": "scenario", "category": "web", "icon": "dns"},
    {"id": "fullstack", "name": "全栈开发", "layer": "scenario", "category": "web", "icon": "layers"},

    # AI/ML
    {"id": "ai_ml", "name": "AI/ML项目", "layer": "scenario", "category": "ai", "icon": "psychology"},
    {"id": "nlp_scene", "name": "自然语言处理", "layer": "scenario", "category": "ai", "icon": "chat"},
    {"id": "cv_scene", "name": "计算机视觉", "layer": "scenario", "category": "ai", "icon": "visibility"},
    {"id": "data_science", "name": "数据科学", "layer": "scenario", "category": "ai", "icon": "analytics"},
    {"id": "llm_scene", "name": "大语言模型", "layer": "scenario", "category": "ai", "icon": "auto_awesome"},
    {"id": "rag_scene", "name": "RAG应用", "layer": "scenario", "category": "ai", "icon": "library_books"},

    # 基础设施
    {"id": "devops", "name": "DevOps/运维", "layer": "scenario", "category": "infra", "icon": "settings"},
    {"id": "cloud", "name": "云原生/容器", "layer": "scenario", "category": "infra", "icon": "cloud"},
    {"id": "kubernetes", "name": "Kubernetes", "layer": "scenario", "category": "infra", "icon": "hub"},
    {"id": "security", "name": "安全工具", "layer": "scenario", "category": "infra", "icon": "shield"},
    {"id": "monitoring_scene", "name": "监控/日志", "layer": "scenario", "category": "infra", "icon": "monitor_heart"},
    {"id": "database", "name": "数据库", "layer": "scenario", "category": "infra", "icon": "storage"},

    # 工具
    {"id": "cli", "name": "命令行工具", "layer": "scenario", "category": "tools", "icon": "terminal"},
    {"id": "automation_scene", "name": "自动化脚本", "layer": "scenario", "category": "tools", "icon": "auto_fix"},
    {"id": "testing", "name": "测试工具", "layer": "scenario", "category": "tools", "icon": "bug_report"},
    {"id": "documentation", "name": "文档工具", "layer": "scenario", "category": "tools", "icon": "description"},
    {"id": "editor", "name": "编辑器/IDE", "layer": "scenario", "category": "tools", "icon": "edit"},
    {"id": "productivity", "name": "效率工具", "layer": "scenario", "category": "tools", "icon": "bolt"},

    # 其他
    {"id": "mobile", "name": "移动应用", "layer": "scenario", "category": "other", "icon": "phone_android"},
    {"id": "game", "name": "游戏开发", "layer": "scenario", "category": "other", "icon": "sports_esports"},
    {"id": "iot", "name": "物联网", "layer": "scenario", "category": "other", "icon": "sensors"},
    {"id": "blockchain", "name": "区块链", "layer": "scenario", "category": "other", "icon": "currency_bitcoin"},
    {"id": "desktop", "name": "桌面应用", "layer": "scenario", "category": "other", "icon": "laptop"},
    {"id": "embedded", "name": "嵌入式系统", "layer": "scenario", "category": "other", "icon": "memory"},

    # 设计与创意
    {"id": "design", "name": "设计工具", "layer": "scenario", "category": "design", "icon": "palette"},
    {"id": "visualization", "name": "数据可视化", "layer": "scenario", "category": "design", "icon": "bar_chart"},
    {"id": "animation", "name": "动画/3D", "layer": "scenario", "category": "design", "icon": "3d_rotation"},
]

# 节点间关系定义
# 格式: (源节点ID, 目标节点ID, 关系强度)
RELATIONS = [
    # 语言 -> 框架
    ("python", "pytorch", 1.0),
    ("python", "tensorflow", 1.0),
    ("python", "django", 1.0),
    ("python", "fastapi", 1.0),
    ("python", "flask", 1.0),
    ("python", "langchain", 1.0),
    ("python", "transformers", 1.0),
    ("typescript", "react", 1.0),
    ("typescript", "nextjs", 1.0),
    ("typescript", "svelte", 1.0),
    ("javascript", "vue", 1.0),
    ("javascript", "react", 0.5),
    ("go", "gin", 1.0),
    ("go", "echo", 1.0),
    ("rust", "axum", 1.0),
    ("rust", "actix", 1.0),

    # 框架 -> 模型
    ("pytorch", "llm", 1.0),
    ("pytorch", "cv", 1.0),
    ("pytorch", "nlp", 1.0),
    ("pytorch", "diffusion", 1.0),
    ("pytorch", "multimodal", 1.0),
    ("pytorch", "embedding", 1.0),
    ("tensorflow", "llm", 1.0),
    ("tensorflow", "cv", 1.0),
    ("tensorflow", "nlp", 1.0),
    ("transformers", "llm", 1.0),
    ("transformers", "nlp", 1.0),
    ("transformers", "multimodal", 1.0),
    ("langchain", "llm", 1.0),
    ("langchain", "embedding", 1.0),

    # 模型 -> 应用
    ("llm", "rag", 1.0),
    ("llm", "agent", 1.0),
    ("llm", "chatbot", 1.0),
    ("nlp", "rag", 1.0),
    ("nlp", "chatbot", 1.0),
    ("cv", "webapp", 0.5),
    ("embedding", "rag", 1.0),
    ("multimodal", "agent", 0.8),
    ("diffusion", "webapp", 0.5),

    # 框架 -> 应用 (直接关联)
    ("react", "webapp", 1.0),
    ("vue", "webapp", 1.0),
    ("nextjs", "webapp", 1.0),
    ("django", "webapp", 1.0),
    ("django", "api", 1.0),
    ("fastapi", "api", 1.0),
    ("fastapi", "webapp", 1.0),
    ("flask", "api", 1.0),
    ("flask", "webapp", 1.0),
    ("gin", "api", 1.0),
    ("echo", "api", 1.0),
    ("axum", "api", 1.0),
    ("actix", "api", 1.0),

    # 应用 -> 场景
    ("webapp", "web_dev", 1.0),
    ("webapp", "frontend", 1.0),
    ("webapp", "backend", 1.0),
    ("webapp", "fullstack", 1.0),
    ("api", "backend", 1.0),
    ("api", "fullstack", 1.0),
    ("rag", "rag_scene", 1.0),
    ("rag", "ai_ml", 1.0),
    ("rag", "nlp_scene", 1.0),
    ("agent", "ai_ml", 1.0),
    ("agent", "llm_scene", 1.0),
    ("chatbot", "ai_ml", 1.0),
    ("chatbot", "llm_scene", 1.0),
    ("dashboard", "data_science", 1.0),
    ("dashboard", "visualization", 1.0),
    ("automation", "automation_scene", 1.0),
    ("automation", "productivity", 1.0),
    ("monitoring", "monitoring_scene", 1.0),
    ("monitoring", "devops", 1.0),
]

# 节点描述
NODE_DESCRIPTIONS = {
    # 语言层
    "python": "简洁优雅的通用编程语言，AI/ML领域首选",
    "typescript": "带类型的JavaScript，大型项目必备",
    "javascript": "Web开发的基石语言",
    "go": "高性能并发编程语言，云原生时代的C语言",
    "rust": "内存安全的高性能系统编程语言",
    "java": "企业级应用开发的经典选择",
    "cpp": "高性能计算和系统编程",
    "swift": "Apple生态的现代编程语言",

    # 框架层
    "pytorch": "深度学习研究框架，动态图先驱",
    "tensorflow": "工业级ML框架，生产环境首选",
    "django": "全功能Python Web框架，大而全",
    "fastapi": "现代异步Python Web框架，性能卓越",
    "flask": "轻量级Python微框架",
    "langchain": "LLM应用开发框架，Agent编排利器",
    "transformers": "HuggingFace预训练模型库",
    "react": "组件化前端框架，声明式UI",
    "vue": "渐进式JavaScript框架，易学易用",
    "nextjs": "React全栈框架，SSR/SSG解决方案",
    "nuxt": "Vue全栈框架",
    "svelte": "编译时框架，无虚拟DOM",
    "gin": "高性能Go Web框架",
    "echo": "简洁的Go Web框架",
    "axum": "基于Tokio的异步Rust Web框架",
    "actix": "高性能Rust Web框架",

    # 模型层
    "llm": "GPT、Claude等大型语言模型，理解与生成文本",
    "cv": "图像识别、目标检测、图像生成等视觉模型",
    "nlp": "文本分析、情感分析、命名实体识别",
    "diffusion": "Stable Diffusion等图像生成模型",
    "multimodal": "图文、音视频等多模态理解模型",
    "embedding": "文本向量表示，语义搜索基础",

    # 应用层
    "rag": "检索增强生成，结合知识库的问答系统",
    "agent": "自主决策的AI智能体，任务规划与执行",
    "chatbot": "对话式AI助手",
    "webapp": "Web应用程序",
    "api": "RESTful/GraphQL API服务",
    "dashboard": "数据可视化仪表板",
    "automation": "自动化脚本和工具",
    "monitoring": "系统监控与告警",

    # 场景层 (描述从scenarios.py复用)
    "web_dev": "构建响应式网站、单页应用和Web服务",
    "frontend": "用户界面开发、组件库和前端框架",
    "backend": "服务器端逻辑、API开发和微服务架构",
    "fullstack": "同时处理前端和后端开发的完整解决方案",
    "ai_ml": "人工智能和机器学习项目开发",
    "nlp_scene": "文本分析、语言模型和文本处理应用",
    "cv_scene": "图像识别、目标检测和视觉处理",
    "data_science": "数据分析、统计建模和数据挖掘",
    "llm_scene": "LLM应用开发、提示工程和模型微调",
    "rag_scene": "检索增强生成、知识库问答系统",
    "devops": "CI/CD、部署自动化和系统运维",
    "cloud": "Docker、Kubernetes和云原生应用",
    "kubernetes": "K8s集群管理、容器编排和服务网格",
    "security": "安全扫描、漏洞检测和防护工具",
    "monitoring_scene": "系统监控、日志收集和分析平台",
    "database": "数据库管理、ORM和数据持久化",
    "cli": "CLI工具、终端应用和命令行界面",
    "automation_scene": "任务自动化、工作流和批处理脚本",
    "testing": "单元测试、集成测试和质量保证",
    "documentation": "文档生成、静态站点和知识库",
    "editor": "代码编辑器、IDE和开发工具",
    "productivity": "提高开发效率的实用工具集",
    "mobile": "iOS、Android和跨平台移动应用",
    "game": "游戏引擎、游戏开发和游戏工具",
    "iot": "IoT设备、传感器和边缘计算",
    "blockchain": "智能合约、DApp和区块链工具",
    "desktop": "跨平台桌面应用和GUI程序",
    "embedded": "嵌入式开发、固件和硬件接口",
    "design": "UI/UX设计、原型和设计系统",
    "visualization": "图表、仪表板和数据展示",
    "animation": "3D渲染、动画和图形效果",
}


def get_all_nodes() -> List[Dict]:
    """获取所有节点"""
    all_nodes = []
    all_nodes.extend(LANGUAGE_NODES)
    all_nodes.extend(FRAMEWORK_NODES)
    all_nodes.extend(MODEL_NODES)
    all_nodes.extend(APPLICATION_NODES)
    all_nodes.extend(SCENARIO_NODES)

    # 为每个节点添加描述和完整信息
    for node in all_nodes:
        node["description"] = NODE_DESCRIPTIONS.get(node["id"], f"{node['name']} - 技术节点")
        node["layer_info"] = TECH_LAYERS[node["layer"]]

    return all_nodes


def get_all_links() -> List[Dict]:
    """获取所有连线"""
    links = []
    node_ids = {n["id"]: n for n in get_all_nodes()}

    for source, target, strength in RELATIONS:
        if source in node_ids and target in node_ids:
            links.append({
                "source": source,
                "target": target,
                "strength": strength,
                "source_layer": node_ids[source]["layer"],
                "target_layer": node_ids[target]["layer"],
            })

    return links


def build_graph_data() -> Dict:
    """构建图谱数据，用于导出为JSON"""
    nodes = get_all_nodes()
    links = get_all_links()

    # 为D3.js准备节点数据
    graph_nodes = []
    for node in nodes:
        graph_nodes.append({
            "id": node["id"],
            "name": node["name"],
            "layer": node["layer"],
            "layer_name": TECH_LAYERS[node["layer"]]["name"],
            "level": TECH_LAYERS[node["layer"]]["level"],
            "color": TECH_LAYERS[node["layer"]]["color"],
            "category": node.get("category", ""),
            "icon": node.get("icon", ""),
            "description": node["description"],
        })

    # 为D3.js准备连线数据
    graph_links = []
    for link in links:
        graph_links.append({
            "source": link["source"],
            "target": link["target"],
            "strength": link["strength"],
        })

    return {
        "nodes": graph_nodes,
        "links": graph_links,
        "layers": TECH_LAYERS,
        "stats": {
            "total_nodes": len(graph_nodes),
            "total_links": len(graph_links),
            "nodes_by_layer": {
                layer["name"]: len([n for n in graph_nodes if n["layer"] == layer_id])
                for layer_id, layer in TECH_LAYERS.items()
            }
        }
    }


def export_to_json(path: str = "blog/static/data/tech-stack.json"):
    """导出技术栈数据为JSON文件"""
    from pathlib import Path

    data = build_graph_data()
    output_path = Path(path)

    # 确保目录存在
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return output_path


if __name__ == "__main__":
    # 测试代码
    data = build_graph_data()
    print(f"技术栈图谱数据:")
    print(f"  节点数: {data['stats']['total_nodes']}")
    print(f"  连线数: {data['stats']['total_links']}")
    print(f"  按层分布:")
    for layer_name, count in data['stats']['nodes_by_layer'].items():
        print(f"    {layer_name}: {count} 个")

    # 导出JSON
    json_path = export_to_json()
    print(f"\n已导出数据到: {json_path}")
