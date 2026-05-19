"""
校园校小助工作流主图编排（增强版）
实现智能追问、办事导航、答案溯源、相关推荐等创新功能
"""
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime

from graphs.state import (
    GlobalState,
    GraphInput,
    GraphOutput
)

# 导入节点函数
from graphs.nodes.knowledge_search_node import knowledge_search_node
from graphs.nodes.smart_clarify_node import smart_clarify_node
from graphs.nodes.intent_recognition_node import intent_recognition_node
from graphs.nodes.answer_generation_node import answer_generation_node
from graphs.nodes.service_guide_node import service_guide_node
from graphs.nodes.web_search_node import web_search_node
from graphs.nodes.response_optimize_node import response_optimize_node
from graphs.nodes.related_recommend_node import related_recommend_node
from graphs.nodes.no_result_node import no_result_node
from graphs.nodes.jump_confirm_node import jump_confirm_node


# ==================== 条件判断函数 ====================

def intent_branch(state: GlobalState) -> str:
    """
    title: 意图分支判断
    desc: 根据意图类型决定后续流程
    """
    intent = state.intent_type
    
    if intent == "web_jump":
        return "网页跳转"
    elif intent == "service_guide":
        return "办事导航"
    elif intent == "campus_consult":
        return "校园咨询"
    else:
        return "其他"


def clarify_branch(state: GlobalState) -> str:
    """
    title: 追问分支判断
    desc: 根据是否需要追问决定后续流程
    """
    if state.need_clarify:
        return "需要追问"
    else:
        return "无需追问"


def knowledge_result_branch(state: GlobalState) -> str:
    """
    title: 知识库结果分支
    desc: 根据知识库检索结果决定是直接回答还是联网搜索
    """
    if state.knowledge_has_result:
        return "知识库回答"
    else:
        return "联网搜索"


def web_search_result_branch(state: GlobalState) -> str:
    """
    title: 联网搜索结果分支
    desc: 判断联网搜索是否有有效结果
    """
    if state.web_search_result and len(state.web_search_result.strip()) > 0:
        return "优化回复"
    else:
        return "无结果提示"


# ==================== 输出映射函数 ====================

def get_output(state: GlobalState) -> GraphOutput:
    """
    title: 输出映射函数
    desc: 将全局状态映射到输出schema
    """
    return GraphOutput(
        response_content=state.response_content,
        need_jump=state.need_jump,
        jump_url=state.jump_url if state.jump_url else state.web_jump_url,
        jump_name=state.jump_name if state.jump_name else state.web_jump_name,
        need_clarify=state.need_clarify,
        clarify_questions=state.clarify_questions,
        source_info=state.source_info,
        confidence_level=state.confidence_level,
        related_questions=state.related_questions,
        quick_actions=state.quick_actions,
        is_service_guide=state.is_service_request,
        guide_steps=state.guide_steps
    )


# ==================== 主图编排 ====================

# 创建状态图
builder = StateGraph(
    GlobalState,
    input_schema=GraphInput,
    output_schema=GraphOutput
)

# ===== 添加节点 =====

# 1. 知识库检索
builder.add_node("knowledge_search", knowledge_search_node)

# 2. 意图识别（优先判断）
builder.add_node(
    "intent_recognition",
    intent_recognition_node,
    metadata={
        "type": "agent",
        "llm_cfg": "config/intent_recognition_llm_cfg.json"
    }
)

# 3. 智能追问（仅校园咨询场景）
builder.add_node(
    "smart_clarify",
    smart_clarify_node,
    metadata={
        "type": "agent",
        "llm_cfg": "config/smart_clarify_llm_cfg.json"
    }
)

# 4. 答案生成（含溯源信息）
builder.add_node(
    "answer_generation",
    answer_generation_node,
    metadata={
        "type": "agent",
        "llm_cfg": "config/answer_generation_llm_cfg.json"
    }
)

# 5. 办事导航（创新功能）
builder.add_node(
    "service_guide",
    service_guide_node,
    metadata={
        "type": "agent",
        "llm_cfg": "config/service_guide_llm_cfg.json"
    }
)

# 6. 联网搜索
builder.add_node("web_search", web_search_node)

# 7. 话术优化
builder.add_node(
    "response_optimize",
    response_optimize_node,
    metadata={
        "type": "agent",
        "llm_cfg": "config/response_optimize_llm_cfg.json"
    }
)

# 8. 相关推荐（创新功能）
builder.add_node(
    "related_recommend",
    related_recommend_node,
    metadata={
        "type": "agent",
        "llm_cfg": "config/related_recommend_llm_cfg.json"
    }
)

# 9. 无结果回复
builder.add_node(
    "no_result",
    no_result_node,
    metadata={
        "type": "agent",
        "llm_cfg": "config/no_result_llm_cfg.json"
    }
)

# 10. 跳转确认
builder.add_node("jump_confirm", jump_confirm_node)

# ===== 设置入口点和边 =====

# 入口点：知识库检索
builder.set_entry_point("knowledge_search")

# 知识库检索 → 意图识别（优先判断意图）
builder.add_edge("knowledge_search", "intent_recognition")

# 意图识别 → 条件分支
builder.add_conditional_edges(
    source="intent_recognition",
    path=intent_branch,
    path_map={
        "网页跳转": "jump_confirm",
        "办事导航": "service_guide",
        "校园咨询": "smart_clarify",
        "其他": "no_result"
    }
)

# 智能追问 → 条件分支
builder.add_conditional_edges(
    source="smart_clarify",
    path=clarify_branch,
    path_map={
        "需要追问": "answer_generation",
        "无需追问": "answer_generation"
    }
)

# 答案生成 → 判断是否需要联网搜索
builder.add_conditional_edges(
    source="answer_generation",
    path=knowledge_result_branch,
    path_map={
        "知识库回答": "related_recommend",
        "联网搜索": "web_search"
    }
)

# 办事导航 → 相关推荐
builder.add_edge("service_guide", "related_recommend")

# 联网搜索 → 结果判断
builder.add_conditional_edges(
    source="web_search",
    path=web_search_result_branch,
    path_map={
        "优化回复": "response_optimize",
        "无结果提示": "no_result"
    }
)

# 话术优化 → 相关推荐
builder.add_edge("response_optimize", "related_recommend")

# 相关推荐 → END
builder.add_edge("related_recommend", END)

# 无结果回复 → END
builder.add_edge("no_result", END)

# 跳转确认 → 相关推荐
builder.add_edge("jump_confirm", "related_recommend")

# 设置输出映射（必须在编译之前）
builder.set_finish(get_output)

# 编译图
main_graph = builder.compile()