#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
超简化版的工作流测试脚本
不依赖任何外部包，仅使用 Python 标准库
测试工作流逻辑流程和状态转换
"""

import sys
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field

# ==========================================================
# 模拟状态类
# ==========================================================

@dataclass
class GlobalState:
    """模拟全局状态"""
    user_query: str = ""
    user_role: str = "student"
    
    # 知识库相关
    knowledge_result: str = ""
    knowledge_score: float = 0.0
    knowledge_has_result: bool = False
    
    # 意图识别
    intent_type: str = "campus_consult"
    web_jump_url: str = ""
    web_jump_name: str = ""
    is_service_request: bool = False
    service_type: str = ""
    
    # 联网搜索
    web_search_result: str = ""
    source_content: str = ""
    source_type: str = "web_search"
    
    # 智能追问
    need_clarify: bool = False
    clarify_questions: List[str] = field(default_factory=list)
    query_clarity: str = "clear"
    
    # 答案溯源
    source_info: Dict[str, Any] = field(default_factory=dict)
    confidence_level: str = "medium"
    
    # 相关推荐
    related_questions: List[str] = field(default_factory=list)
    quick_actions: List[Dict[str, Any]] = field(default_factory=list)
    
    # 办事导航
    guide_steps: List[Dict[str, Any]] = field(default_factory=list)
    required_materials: List[str] = field(default_factory=list)
    service_location: str = ""
    
    # 最终输出
    response_content: str = ""
    need_jump: bool = False
    jump_url: str = ""
    jump_name: str = ""
    is_service_guide: bool = False


# ==========================================================
# 模拟节点函数
# ==========================================================

def mock_knowledge_search(state: GlobalState) -> Dict[str, Any]:
    """模拟知识库搜索"""
    print("[知识库搜索] 查询:", state.user_query)
    return {
        "knowledge_result": "测试知识库结果",
        "knowledge_score": 0.85,
        "knowledge_has_result": True
    }


def mock_intent_recognition(state: GlobalState) -> Dict[str, Any]:
    """模拟意图识别"""
    print("[意图识别] 分析:", state.user_query)
    
    # 简单的关键词匹配
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
    
    print("   -> 识别到意图:", intent)
    return {
        "intent_type": intent,
        "web_jump_url": jump_url,
        "web_jump_name": jump_name,
        "is_service_request": intent == "service_guide",
        "service_type": state.user_query
    }


def mock_smart_clarify(state: GlobalState) -> Dict[str, Any]:
    """模拟智能追问"""
    print("[智能追问] 分析问题清晰度")
    # 简单判断：问题长度小于10的需要追问
    need_clarify = len(state.user_query) < 10
    clarify_questions = []
    if need_clarify:
        clarify_questions = [
            "请提供更多细节？",
            "是关于哪个方面的？"
        ]
        print("   -> 需要追问:", clarify_questions)
    else:
        print("   -> 问题清晰，不需要追问")
    
    return {
        "need_clarify": need_clarify,
        "clarify_questions": clarify_questions,
        "query_clarity": "clear" if not need_clarify else "vague",
        "clarified_query": state.user_query
    }


def mock_answer_generation(state: GlobalState) -> Dict[str, Any]:
    """模拟答案生成"""
    print("[答案生成] 正在生成回复...")
    
    if state.knowledge_has_result:
        response = "根据知识库，我为您找到：" + state.knowledge_result
        confidence = "high"
        source_info = {"source": "校园知识库", "type": "knowledge"}
    else:
        response = "抱歉，知识库中没有找到相关信息。"
        confidence = "low"
        source_info = {}
    
    return {
        "response_content": response,
        "source_info": source_info,
        "confidence_level": confidence
    }


def mock_service_guide(state: GlobalState) -> Dict[str, Any]:
    """模拟办事导航"""
    print("[办事导航] 生成办事指南...")
    return {
        "response_content": "**办事指南**\n1. 准备材料\n2. 前往办理地点\n3. 提交申请",
        "guide_steps": [
            {"step": 1, "action": "准备材料", "location": "行政楼"},
            {"step": 2, "action": "前往办理", "location": "服务中心"},
            {"step": 3, "action": "提交申请", "location": "1号窗口"}
        ],
        "required_materials": ["身份证", "学生证"],
        "service_location": "行政楼1楼",
        "is_service_guide": True
    }


def mock_web_search(state: GlobalState) -> Dict[str, Any]:
    """模拟联网搜索"""
    print("[联网搜索] 搜索中...")
    return {
        "web_search_result": "搜索到的网络信息摘要",
        "source_content": "搜索到的网络信息摘要",
        "source_type": "web_search"
    }


def mock_response_optimize(state: GlobalState) -> Dict[str, Any]:
    """模拟回复优化"""
    print("[回复优化] 优化回复中...")
    optimized = "[优化后的回复] " + state.source_content
    return {
        "response_content": optimized
    }


def mock_related_recommend(state: GlobalState) -> Dict[str, Any]:
    """模拟相关推荐"""
    print("[相关推荐] 生成推荐...")
    return {
        "related_questions": [
            "相关问题1",
            "相关问题2",
            "相关问题3"
        ],
        "quick_actions": [
            {"name": "查看更多", "action": "query", "query": "更多信息"},
            {"name": "返回主页", "action": "jump", "url": "/"}
        ]
    }


def mock_no_result(state: GlobalState) -> Dict[str, Any]:
    """模拟无结果回复"""
    print("[无结果] 生成友好提示...")
    return {
        "response_content": "抱歉，我没有找到相关信息。您可以尝试重新提问或咨询校园服务中心。"
    }


def mock_jump_confirm(state: GlobalState) -> Dict[str, Any]:
    """模拟跳转确认"""
    print("[跳转确认] 准备跳转提示...")
    return {
        "response_content": "我检测到您可能需要访问【" + state.web_jump_name + "】\n跳转地址：" + state.web_jump_url + "\n",
        "need_jump": True,
        "jump_url": state.web_jump_url,
        "jump_name": state.web_jump_name
    }


# ==========================================================
# 工作流执行器
# ==========================================================

def update_state(state: GlobalState, updates: Dict[str, Any]) -> None:
    """更新状态"""
    for key, value in updates.items():
        if hasattr(state, key):
            setattr(state, key, value)


def intent_branch(state: GlobalState) -> str:
    """意图分支"""
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
    """追问分支"""
    return "需要追问" if state.need_clarify else "无需追问"


def knowledge_result_branch(state: GlobalState) -> str:
    """知识库结果分支"""
    return "知识库回答" if state.knowledge_has_result else "联网搜索"


def web_search_result_branch(state: GlobalState) -> str:
    """搜索结果分支"""
    return "优化回复" if state.web_search_result else "无结果提示"


def execute_workflow(query: str, user_role: str = "student") -> GlobalState:
    """执行工作流"""
    state = GlobalState(user_query=query, user_role=user_role)
    
    print("\n" + "="*80)
    print("开始执行工作流")
    print("用户:", user_role)
    print("查询:", query)
    print("="*80 + "\n")
    
    # 1. 知识库搜索
    update_state(state, mock_knowledge_search(state))
    
    # 2. 意图识别
    update_state(state, mock_intent_recognition(state))
    
    # 3. 意图分支
    next_step = intent_branch(state)
    
    if next_step == "网页跳转":
        # 网页跳转流程
        update_state(state, mock_jump_confirm(state))
        update_state(state, mock_related_recommend(state))
        
    elif next_step == "办事导航":
        # 办事导航流程
        update_state(state, mock_service_guide(state))
        update_state(state, mock_related_recommend(state))
        
    elif next_step == "校园咨询":
        # 校园咨询流程
        update_state(state, mock_smart_clarify(state))
        # 无论是否需要追问，都继续到答案生成
        update_state(state, mock_answer_generation(state))
        
        # 根据知识库结果分支
        knowledge_branch = knowledge_result_branch(state)
        if knowledge_branch == "知识库回答":
            update_state(state, mock_related_recommend(state))
        else:
            update_state(state, mock_web_search(state))
            search_branch = web_search_result_branch(state)
            if search_branch == "优化回复":
                update_state(state, mock_response_optimize(state))
            else:
                update_state(state, mock_no_result(state))
            update_state(state, mock_related_recommend(state))
            
    else:
        # 其他问题
        update_state(state, mock_no_result(state))
    
    print("\n" + "="*80)
    print("工作流执行完成")
    print("="*80 + "\n")
    
    return state


# ==========================================================
# 测试主函数
# ==========================================================

def print_state_summary(state: GlobalState) -> None:
    """打印状态摘要"""
    print("执行结果摘要:")
    print("-"*60)
    print("回复内容:\n" + state.response_content + "\n")
    
    if state.need_clarify:
        print("需要追问:", state.clarify_questions, "\n")
    
    if state.need_jump:
        print("跳转链接:", state.jump_name, "->", state.jump_url, "\n")
    
    if state.related_questions:
        print("相关问题:", state.related_questions, "\n")
    
    if state.quick_actions:
        print("快捷操作:", state.quick_actions, "\n")
    
    if state.guide_steps:
        print("办事步骤:", state.guide_steps, "\n")
    
    print("-"*60)


def main():
    """主函数"""
    print("""
============================================================
          校园校小助 - 超简化工作流测试环境                
     （纯 Python 标准库，零外部依赖，测试工作流逻辑流程）
============================================================
    """)
    
    # 测试用例
    test_cases = [
        {
            "name": "场景1: 校园咨询（图书馆）",
            "query": "图书馆开放时间是什么时候？",
            "role": "student"
        },
        {
            "name": "场景2: 网页跳转（教务系统）", 
            "query": "我想打开教务系统",
            "role": "student"
        },
        {
            "name": "场景3: 办事导航（补办学生证）",
            "query": "我想办理学生证补办",
            "role": "student"
        },
        {
            "name": "场景4: 简短问题（测试智能追问）",
            "query": "考试",
            "role": "student"
        },
        {
            "name": "场景5: 其他问题",
            "query": "今天天气怎么样？",
            "role": "student"
        }
    ]
    
    # 运行测试
    results = []
    for i, test in enumerate(test_cases, 1):
        print("\n测试用例 " + str(i) + "/" + str(len(test_cases)) + ": " + test['name'])
        print("-"*80)
        
        try:
            state = execute_workflow(test['query'], test['role'])
            print_state_summary(state)
            results.append({
                "test": test,
                "success": True,
                "state": state
            })
        except Exception as e:
            print("测试失败:", str(e))
            import traceback
            traceback.print_exc()
            results.append({
                "test": test,
                "success": False,
                "error": str(e)
            })
        
        # 暂停一下，方便看输出
        if i < len(test_cases):
            try:
                input("\n按 Enter 键继续下一个测试...")
            except EOFError:
                pass
    
    # 总结
    print("\n" + "="*80)
    print("测试总结:")
    print("="*80)
    success_count = sum(1 for r in results if r['success'])
    print("总计:", len(results), "个测试")
    print("成功:", success_count, "个")
    print("失败:", len(results) - success_count, "个")
    
    for r in results:
        status = "OK" if r['success'] else "FAIL"
        print(status + " " + r['test']['name'])
    
    print("="*80 + "\n")


if __name__ == "__main__":
    # 设置输出编码
    if sys.platform == "win32":
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    main()
