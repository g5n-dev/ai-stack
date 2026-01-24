"""
Application Scenarios Definition
应用场景定义 - 预设的应用场景列表和图标映射
"""

from typing import List, Dict, Optional

# 预设应用场景列表
APPLICATION_SCENARIOS: List[Dict[str, str]] = [
    # Web 开发
    {"id": "web_dev", "name": "Web应用开发", "icon": "web", "category": "web"},
    {"id": "frontend", "name": "前端开发", "icon": "desktop_windows", "category": "web"},
    {"id": "backend", "name": "后端开发", "icon": "dns", "category": "web"},
    {"id": "fullstack", "name": "全栈开发", "icon": "layers", "category": "web"},

    # AI/ML
    {"id": "ai_ml", "name": "AI/ML项目", "icon": "psychology", "category": "ai"},
    {"id": "nlp", "name": "自然语言处理", "icon": "chat", "category": "ai"},
    {"id": "cv", "name": "计算机视觉", "icon": "visibility", "category": "ai"},
    {"id": "data_science", "name": "数据科学", "icon": "analytics", "category": "ai"},
    {"id": "llm", "name": "大语言模型", "icon": "auto_awesome", "category": "ai"},
    {"id": "rag", "name": "RAG应用", "icon": "library_books", "category": "ai"},

    # 基础设施
    {"id": "devops", "name": "DevOps/运维", "icon": "settings", "category": "infra"},
    {"id": "cloud", "name": "云原生/容器", "icon": "cloud", "category": "infra"},
    {"id": "kubernetes", "name": "Kubernetes", "icon": "hub", "category": "infra"},
    {"id": "security", "name": "安全工具", "icon": "shield", "category": "infra"},
    {"id": "monitoring", "name": "监控/日志", "icon": "monitor_heart", "category": "infra"},
    {"id": "database", "name": "数据库", "icon": "storage", "category": "infra"},

    # 工具
    {"id": "cli", "name": "命令行工具", "icon": "terminal", "category": "tools"},
    {"id": "automation", "name": "自动化脚本", "icon": "auto_fix", "category": "tools"},
    {"id": "testing", "name": "测试工具", "icon": "bug_report", "category": "tools"},
    {"id": "documentation", "name": "文档工具", "icon": "description", "category": "tools"},
    {"id": "editor", "name": "编辑器/IDE", "icon": "edit", "category": "tools"},
    {"id": "productivity", "name": "效率工具", "icon": "bolt", "category": "tools"},

    # 其他
    {"id": "mobile", "name": "移动应用", "icon": "phone_android", "category": "other"},
    {"id": "game", "name": "游戏开发", "icon": "sports_esports", "category": "other"},
    {"id": "iot", "name": "物联网", "icon": "sensors", "category": "other"},
    {"id": "blockchain", "name": "区块链", "icon": "currency_bitcoin", "category": "other"},
    {"id": "desktop", "name": "桌面应用", "icon": "laptop", "category": "other"},
    {"id": "embedded", "name": "嵌入式系统", "icon": "memory", "category": "other"},

    # 设计与创意
    {"id": "design", "name": "设计工具", "icon": "palette", "category": "design"},
    {"id": "visualization", "name": "数据可视化", "icon": "bar_chart", "category": "design"},
    {"id": "animation", "name": "动画/3D", "icon": "3d_rotation", "category": "design"},
]

# 按类别分组的场景
SCENARIO_CATEGORIES: Dict[str, List[Dict[str, str]]] = {
    "web": [s for s in APPLICATION_SCENARIOS if s.get("category") == "web"],
    "ai": [s for s in APPLICATION_SCENARIOS if s.get("category") == "ai"],
    "infra": [s for s in APPLICATION_SCENARIOS if s.get("category") == "infra"],
    "tools": [s for s in APPLICATION_SCENARIOS if s.get("category") == "tools"],
    "other": [s for s in APPLICATION_SCENARIOS if s.get("category") == "other"],
    "design": [s for s in APPLICATION_SCENARIOS if s.get("category") == "design"],
}

# 场景名称到详情的映射
SCENARIO_DETAILS: Dict[str, Dict[str, str]] = {
    "Web应用开发": {"description": "构建响应式网站、单页应用和 Web 服务"},
    "前端开发": {"description": "用户界面开发、组件库和前端框架"},
    "后端开发": {"description": "服务器端逻辑、API 开发和微服务架构"},
    "全栈开发": {"description": "同时处理前端和后端开发的完整解决方案"},
    "AI/ML项目": {"description": "人工智能和机器学习项目开发"},
    "自然语言处理": {"description": "文本分析、语言模型和文本处理应用"},
    "计算机视觉": {"description": "图像识别、目标检测和视觉处理"},
    "数据科学": {"description": "数据分析、统计建模和数据挖掘"},
    "大语言模型": {"description": "LLM 应用开发、提示工程和模型微调"},
    "RAG应用": {"description": "检索增强生成、知识库问答系统"},
    "DevOps/运维": {"description": "CI/CD、部署自动化和系统运维"},
    "云原生/容器": {"description": "Docker、Kubernetes 和云原生应用"},
    "Kubernetes": {"description": "K8s 集群管理、容器编排和服务网格"},
    "安全工具": {"description": "安全扫描、漏洞检测和防护工具"},
    "监控/日志": {"description": "系统监控、日志收集和分析平台"},
    "数据库": {"description": "数据库管理、ORM 和数据持久化"},
    "命令行工具": {"description": "CLI 工具、终端应用和命令行界面"},
    "自动化脚本": {"description": "任务自动化、工作流和批处理脚本"},
    "测试工具": {"description": "单元测试、集成测试和质量保证"},
    "文档工具": {"description": "文档生成、静态站点和知识库"},
    "编辑器/IDE": {"description": "代码编辑器、IDE 和开发工具"},
    "效率工具": {"description": "提高开发效率的实用工具集"},
    "移动应用": {"description": "iOS、Android 和跨平台移动应用"},
    "游戏开发": {"description": "游戏引擎、游戏开发和游戏工具"},
    "物联网": {"description": "IoT 设备、传感器和边缘计算"},
    "区块链": {"description": "智能合约、DApp 和区块链工具"},
    "桌面应用": {"description": "跨平台桌面应用和 GUI 程序"},
    "嵌入式系统": {"description": "嵌入式开发、固件和硬件接口"},
    "设计工具": {"description": "UI/UX 设计、原型和设计系统"},
    "数据可视化": {"description": "图表、仪表板和数据展示"},
    "动画/3D": {"description": "3D 渲染、动画和图形效果"},
}


def get_scenario_by_name(name: str) -> Optional[Dict[str, str]]:
    """根据名称获取场景定义"""
    for scenario in APPLICATION_SCENARIOS:
        if scenario["name"] == name:
            return scenario
    return None


def get_scenario_icon(name: str) -> str:
    """获取场景图标"""
    scenario = get_scenario_by_name(name)
    if scenario:
        return scenario.get("icon", "category")
    return "category"


def get_scenario_description(name: str) -> str:
    """获取场景描述"""
    details = SCENARIO_DETAILS.get(name)
    if details:
        return details.get("description", "")
    return ""


def get_all_scenario_names() -> List[str]:
    """获取所有场景名称列表"""
    return [s["name"] for s in APPLICATION_SCENARIOS]


def format_scenarios_for_prompt() -> str:
    """格式化场景列表用于提示词"""
    return "\n".join([f"- {s['name']}" for s in APPLICATION_SCENARIOS])


if __name__ == "__main__":
    # 测试代码
    print("应用场景列表:")
    for scenario in APPLICATION_SCENARIOS:
        print(f"  {scenario['name']}: {scenario['icon']}")
    print(f"\n总计: {len(APPLICATION_SCENARIOS)} 个场景")
