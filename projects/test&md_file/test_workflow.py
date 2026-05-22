#!/usr/bin/env python3
"""
本地测试脚本：模拟 Coze 环境测试校园校小助工作流
这个文件不依赖 cozeloop 等平台专用包，仅测试核心工作流逻辑
"""

import sys
import os
from typing import Dict, Any, Optional

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# 先导入 state，因为 graph 需要它
from graphs.state import GlobalState, GraphInput, GraphOutput

# 创建 mock 版本的 graph，避免平台依赖
def create_mock_graph():
    """创建简化版工作流图用于测试"""
    from langgraph.graph import StateGraph, END
    
    # 定义简化的节点
    def mock_knowledge_search(state: GlobalState) -> Dict[str, Any]:
        """模拟知识库搜索"""
        print(f"🔍 [知识库搜索] 查询: {state.user_query}")
        return {
            "knowledge_result": "测试知识库结果",
            "knowledge_score": 0.85,
            "knowledge_has_result": True
        }
    
    def mock_intent_recognition(state: GlobalState) -> Dict[str, Any]:
        """模拟意图识别"""
        print(f"🧠 [意图识别] 分析: {state.user_query}")
        
        # 简单的关键词匹配
        query_lower = state.user_query.lower()
        if "教务" in query_lower or "系统" in query_lower:
            intent = "web_jump"
            jump_url = "/jwxt"
            jump_name = "教务系统"
        elif "办理" in query_lower or "补办" in query_lower:
            intent = "service_guide"
        elif any(key in query_lower for key in ["图书馆", "食堂", "考试", "选课"]):
            intent = "campus_consult"
        else:
            intent = "other"
        
        print(f"   → 识别到意图: {intent}")
        return {
            "intent_type": intent,
            "web_jump_url": jump_url if intent == "web_jump" else "",
            "web_jump_name": jump_name if intent == "web_jump" else "",
            "is_service_request": intent == "service_guide",
            "service_type": state.user_query
        }
    
    def mock_smart_clarify(state: GlobalState) -> Dict[str, Any]:
        """模拟智能追问"""
        print(f"🤔 [智能追问] 分析问题清晰度")
        # 简单判断：问题长度小于10的需要追问
        need_clarify = len(state.user_query) < 10
        clarify_questions = []
        if need_clarify:
            clarify_questions = [
                "请提供更多细节？",
                "是关于哪个方面的？"
            ]
            print(f"   → 需要追问: {clarify_questions}")
        else:
            print(f"   → 问题清晰，不需要追问")
        
        return {
            "need_clarify": need_clarify,
            "clarify_questions": clarify_questions,
            "query_clarity": "clear" if not need_clarify else "vague",
            "clarified_query": state.user_query
        }
    
    def mock_answer_generation(state: GlobalState) -> Dict[str, Any]:
        """模拟答案生成"""
        print(f"📝 [答案生成] 正在生成回复...")
        
        if state.knowledge_has_result:
            response = f"根据知识库，我为您找到：{state.knowledge_result}"
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
        print(f"📋 [办事导航] 生成办事指南...")
        return {
            "response_content": "📋 **办事指南**\n1. 准备材料\n2. 前往办理地点\n3. 提交申请",
            "guide_steps": [
                {"step": 1, "action": "准备材料", "location": "行政楼"},
                {"step": 2, "action": "前往办理", "location": "服务中心"},
                {"step": 3, "action": "提交申请", "location": "1号窗口"}
            ],
            "required_materials": ["身份证", "学生证"],
            "service_location": "行政楼1楼",
            "estimated_time": "2个工作日",
            "tips": ["建议提前预约"]
        }
    
    def mock_web_search(state: GlobalState) -> Dict[str, Any]:
        """模拟联网搜索"""
        print(f"🌐 [联网搜索] 搜索中...")
        return {
            "web_search_result": "搜索到的网络信息摘要",
            "source_content": "搜索到的网络信息摘要",
            "source_type": "web_search"
        }
    
    def mock_response_optimize(state: GlobalState) -> Dict[str, Any]:
        """模拟回复优化"""
        print(f"✨ [回复优化] 优化回复中...")
        optimized = f"[优化后的回复] {state.source_content}"
        return {
            "response_content": optimized
        }
    
    def mock_related_recommend(state: GlobalState) -> Dict[str, Any]:
        """模拟相关推荐"""
        print(f"🎯 [相关推荐] 生成推荐...")
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
        print(f"💡 [无结果] 生成友好提示...")
        return {
            "response_content": "抱歉，我没有找到相关信息。您可以尝试重新提问或咨询校园服务中心。"
        }
    
    def mock_jump_confirm(state: GlobalState) -> Dict[str, Any]:
        """模拟跳转确认"""
        print(f"🔗 [跳转确认] 准备跳转提示...")
        return {
            "response_content": f"🔗 我检测到您可能需要访问【{state.web_jump_name}】\n📍 跳转地址：{state.web_jump_url}\n",
            "need_jump": True,
            "jump_url": state.web_jump_url,
            "jump_name": state.web_jump_name
        }
    
    # 条件判断函数
    def intent_branch(state: GlobalState) -> str:
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
        return "需要追问" if state.need_clarify else "无需追问"
    
    def knowledge_result_branch(state: GlobalState) -> str:
        return "知识库回答" if state.knowledge_has_result else "联网搜索"
    
    def web_search_result_branch(state: GlobalState) -> str:
        return "优化回复" if state.web_search_result else "无结果提示"
    
    # 构建图
    builder = StateGraph(GlobalState, input_schema=GraphInput, output_schema=GraphOutput)
    
    # 添加节点
    builder.add_node("knowledge_search", mock_knowledge_search)
    builder.add_node("intent_recognition", mock_intent_recognition)
    builder.add_node("smart_clarify", mock_smart_clarify)
    builder.add_node("answer_generation", mock_answer_generation)
    builder.add_node("service_guide", mock_service_guide)
    builder.add_node("web_search", mock_web_search)
    builder.add_node("response_optimize", mock_response_optimize)
    builder.add_node("related_recommend", mock_related_recommend)
    builder.add_node("no_result", mock_no_result)
    builder.add_node("jump_confirm", mock_jump_confirm)
    
    # 设置入口
    builder.set_entry_point("knowledge_search")
    
    # 添加边
    builder.add_edge("knowledge_search", "intent_recognition")
    
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
    
    builder.add_conditional_edges(
        source="smart_clarify",
        path=clarify_branch,
        path_map={
            "需要追问": "answer_generation",
            "无需追问": "answer_generation"
        }
    )
    
    builder.add_conditional_edges(
        source="answer_generation",
        path=knowledge_result_branch,
        path_map={
            "知识库回答": "related_recommend",
            "联网搜索": "web_search"
        }
    )
    
    builder.add_edge("service_guide", "related_recommend")
    
    builder.add_conditional_edges(
        source="web_search",
        path=web_search_result_branch,
        path_map={
            "优化回复": "response_optimize",
            "无结果提示": "no_result"
        }
    )
    
    builder.add_edge("response_optimize", "related_recommend")
    builder.add_edge("related_recommend", END)
    builder.add_edge("no_result", END)
    builder.add_edge("jump_confirm", "related_recommend")
    
    # 编译图
    return builder.compile()

def run_test_query(query: str, user_role: str = "student"):
    """运行单个测试查询"""
    print(f"\n{'='*80}")
    print(f"🎯 测试查询: {query}")
    print(f"👤 用户角色: {user_role}")
    print(f"{'='*80}\n")
    
    try:
        # 创建 graph
        graph = create_mock_graph()
        
        # 创建输入
        input_data = GraphInput(user_query=query, user_role=user_role)
        
        # 运行
        print("🚀 开始执行工作流...\n")
        result = graph.invoke(input_data.model_dump())
        
        # 显示结果
        print(f"\n{'='*80}")
        print("📊 工作流执行结果:")
        print(f"{'='*80}\n")
        
        if isinstance(result, dict):
            # 打印结果的主要字段
            print(f"📝 回复内容:\n{result.get('response_content', 'N/A')}\n")
            
            if result.get('need_clarify'):
                print(f"❓ 需要追问: {result.get('clarify_questions', [])}\n")
            
            if result.get('need_jump'):
                print(f"🔗 跳转链接: {result.get('jump_name', '')} -> {result.get('jump_url', '')}\n")
            
            if result.get('related_questions'):
                print(f"💡 相关问题: {result.get('related_questions')}\n")
            
            if result.get('quick_actions'):
                print(f"⚡ 快捷操作: {result.get('quick_actions')}\n")
            
            if result.get('guide_steps'):
                print(f"📋 办事步骤: {result.get('guide_steps')}\n")
        else:
            print(f"结果类型: {type(result)}")
            print(f"结果: {result}")
        
        return result
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """主测试函数"""
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║              🎓 校园校小助 - 工作流本地测试环境                      ║
║         （模拟 Coze 平台环境，测试工作流核心逻辑）                   ║
╚═══════════════════════════════════════════════════════════════════╝
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
        print(f"\n📋 测试用例 {i}/{len(test_cases)}: {test['name']}")
        result = run_test_query(test['query'], test['role'])
        results.append({
            "test": test,
            "result": result,
            "success": result is not None
        })
        
        # 暂停一下，方便看输出
        if i < len(test_cases):
            input("\n按 Enter 键继续下一个测试...")
    
    # 总结
    print(f"\n{'='*80}")
    print("📈 测试总结:")
    print(f"{'='*80}")
    success_count = sum(1 for r in results if r['success'])
    print(f"总计: {len(results)} 个测试")
    print(f"成功: {success_count} 个")
    print(f"失败: {len(results) - success_count} 个")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    main()
