"""
知识库检索节点
优先检索校园专属知识库，获取匹配内容
"""
import os
from typing import Any
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import KnowledgeClient, Config

from graphs.state import GlobalState


def knowledge_search_node(
    state: GlobalState,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> dict:
    """
    title: 知识库检索
    desc: 优先检索校园专属知识库，返回匹配内容和相似度得分
    integrations: 知识库
    """
    ctx = runtime.context
    
    # 初始化知识库客户端
    knowledge_client = KnowledgeClient(ctx=ctx)
    
    # 执行语义搜索
    try:
        # 搜索知识库，top_k=3获取最相关的3条结果
        # 注意：在Coze平台部署时，知识库会通过上下文自动绑定
        # 本地测试时，需要在Coze IDE中配置知识库绑定
        response = knowledge_client.search(
            query=state.user_query,
            top_k=3,
            min_score=0.5
        )
        
        # 检查是否有有效结果
        if response.code == 0 and response.chunks:
            # 取相似度最高的结果
            best_chunk = response.chunks[0]
            content = best_chunk.content if best_chunk.content else ""
            score = best_chunk.score if best_chunk.score else 0.0
            
            # 判断是否有有效结果（得分>0.6且内容非空）
            has_result = len(content.strip()) > 0 and score >= 0.6
            
            return {
                "knowledge_result": content,
                "knowledge_score": score,
                "knowledge_has_result": has_result
            }
        else:
            # 无结果或检索失败
            return {
                "knowledge_result": "",
                "knowledge_score": 0.0,
                "knowledge_has_result": False
            }
            
    except Exception as e:
        # 异常处理，返回无结果
        return {
            "knowledge_result": "",
            "knowledge_score": 0.0,
            "knowledge_has_result": False
        }