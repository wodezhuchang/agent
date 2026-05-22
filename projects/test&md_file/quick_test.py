#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试脚本 - 验证工作流逻辑
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List

@dataclass
class GlobalState:
    user_query: str = ""
    user_role: str = "student"
    intent_type: str = "campus_consult"
    knowledge_has_result: bool = False
    web_search_result: str = ""
    need_clarify: bool = False
    clarify_questions: List[str] = field(default_factory=list)
    response_content: str = ""
    need_jump: bool = False
    jump_url: str = ""
    jump_name: str = ""
    related_questions: List[str] = field(default_factory=list)
    quick_actions: List[Dict[str, Any]] = field(default_factory=list)
    guide_steps: List[Dict[str, Any]] = field(default_factory=list)


def update_state(state: GlobalState, updates: Dict[str, Any]) -> None:
    for key, value in updates.items():
        if hasattr(state, key):
            setattr(state, key, value)


def mock_knowledge_search(state: GlobalState) -> Dict[str, Any]:
    print("  [1] 知识库搜索: " + state.user_query)
    return {
        "knowledge_result": "测试知识库结果",
        "knowledge_score": 0.85,
        "knowledge_has_result": True
    }


def mock_intent_recognition(state: GlobalState) -> Dict[str, Any]:
    print("  [2] 意图识别...")
    query_lower = state.user_query.lower()
    if "教务" in query_lower or "系统" in query_lower:
        intent = "web_jump"
        jump_url = "/jwxt"
        jump_name = "教务系统"
    elif "办理" in query_lower or "补办" in query_lower:
        intent = "service_guide"
        jump_url = ""
        jump_name = ""
    elif any(key in query_lower for key in ["图书馆", "食堂", "考试", "选课"]):
        intent = "campus_consult"
        jump_url = ""
        jump_name = ""
    else:
        intent = "other"
        jump_url = ""
        jump_name = ""
    print("    -> 识别到意图: " + intent)
    return {
        "intent_type": intent,
        "web_jump_url": jump_url,
        "web_jump_name": jump_name
    }


def mock_smart_clarify(state: GlobalState) -> Dict[str, Any]:
    print("  [3] 智能追问...")
    need_clarify = len(state.user_query) < 10
    clarify_questions = ["请提供更多细节？"] if need_clarify else []
    if need_clarify:
        print("    -> 需要追问")
    else:
        print("    -> 问题清晰")
    return {
        "need_clarify": need_clarify,
        "clarify_questions": clarify_questions
    }


def mock_answer_generation(state: GlobalState) -> Dict[str, Any]:
    print("  [4] 答案生成...")
    return {
        "response_content": "根据知识库，我为您找到：测试结果"
    }


def mock_service_guide(state: GlobalState) -> Dict[str, Any]:
    print("  [3] 办事导航...")
    return {
        "response_content": "办事指南：1.准备材料 2.前往办理 3.提交申请",
        "guide_steps": [{"step": 1, "action": "准备材料"}]
    }


def mock_related_recommend(state: GlobalState) -> Dict[str, Any]:
    print("  [5] 相关推荐...")
    return {
        "related_questions": ["相关问题1", "相关问题2"]
    }


def mock_jump_confirm(state: GlobalState) -> Dict[str, Any]:
    print("  [3] 跳转确认...")
    return {
        "response_content": "检测到您要访问：" + state.web_jump_name,
        "need_jump": True,
        "jump_url": state.web_jump_url,
        "jump_name": state.web_jump_name
    }


def mock_no_result(state: GlobalState) -> Dict[str, Any]:
    print("  [X] 无结果...")
    return {
        "response_content": "抱歉，我没有找到相关信息"
    }


def execute_workflow(query: str):
    print("\n" + "="*70)
    print("测试查询: " + query)
    print("="*70)
    
    state = GlobalState(user_query=query)
    
    # 流程执行
    update_state(state, mock_knowledge_search(state))
    update_state(state, mock_intent_recognition(state))
    
    if state.intent_type == "web_jump":
        update_state(state, mock_jump_confirm(state))
        update_state(state, mock_related_recommend(state))
    elif state.intent_type == "service_guide":
        update_state(state, mock_service_guide(state))
        update_state(state, mock_related_recommend(state))
    elif state.intent_type == "campus_consult":
        update_state(state, mock_smart_clarify(state))
        update_state(state, mock_answer_generation(state))
        update_state(state, mock_related_recommend(state))
    else:
        update_state(state, mock_no_result(state))
    
    print("\n结果:")
    print("  回复: " + state.response_content[:100])
    if state.need_jump:
        print("  跳转: " + state.jump_name + " -> " + state.jump_url)
    if state.need_clarify:
        print("  追问: " + str(state.clarify_questions))
    if state.related_questions:
        print("  推荐: " + str(state.related_questions))
    if state.guide_steps:
        print("  步骤: " + str(len(state.guide_steps)) + "步")
    
    return state


def main():
    print("校园校小助 - 工作流逻辑测试")
    print("="*70)
    
    test_queries = [
        "图书馆开放时间是什么时候？",
        "我想打开教务系统",
        "我想办理学生证补办",
        "考试",
        "今天天气怎么样？"
    ]
    
    all_ok = True
    for i, query in enumerate(test_queries, 1):
        print("\n" + "-"*70)
        print(f"测试 {i}/{len(test_queries)}")
        try:
            state = execute_workflow(query)
            print("  [OK]")
        except Exception as e:
            print(f"  [FAIL] {str(e)}")
            all_ok = False
    
    print("\n" + "="*70)
    print("测试完成:", "全部通过" if all_ok else "有失败")
    print("="*70)


if __name__ == "__main__":
    main()
