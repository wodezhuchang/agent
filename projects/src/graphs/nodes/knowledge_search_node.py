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
    
    # 从配置中获取知识库 ID（支持多种配置方式）
    knowledge_base_id = None
    
    # 方式1：从环境变量获取（优先级最高）
    knowledge_base_id = os.environ.get('COZE_KNOWLEDGE_BASE_ID')
    
    # 方式2：从config配置中获取
    if not knowledge_base_id:
        custom_config = config.get('configurable', {})
        knowledge_base_id = custom_config.get('knowledge_base_id')
    
    # 方式3：从全局配置获取（可选）
    if not knowledge_base_id:
        from graphs.state import get_knowledge_base_id
        knowledge_base_id = get_knowledge_base_id()
    
    # 初始化知识库客户端
    knowledge_client = KnowledgeClient(ctx=ctx)
    
    # 执行语义搜索
    try:
        # 如果配置了知识库 ID，使用指定的知识库
        if knowledge_base_id:
            # 搜索指定的知识库，top_k=3获取最相关的3条结果
            response = knowledge_client.search(
                query=state.user_query,
                top_k=3,
                min_score=0.5
            )
        else:
            # 使用默认绑定的知识库（Coze 平台自动配置）
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
                "knowledge_has_result": has_result,
                "knowledge_base_id": knowledge_base_id,
                "knowledge_search_info": f"检索到 {len(response.chunks)} 条相关内容，最佳匹配得分: {score:.2f}"
            }
        else:
            # 无结果或检索失败
            return {
                "knowledge_result": "",
                "knowledge_score": 0.0,
                "knowledge_has_result": False,
                "knowledge_base_id": knowledge_base_id,
                "knowledge_search_info": "知识库中未找到相关内容"
            }
            
    except Exception as e:
        # 异常处理，返回无结果
        return {
            "knowledge_result": "",
            "knowledge_score": 0.0,
            "knowledge_has_result": False,
            "knowledge_base_id": knowledge_base_id,
            "knowledge_search_info": f"知识库检索异常: {str(e)}"
        }


def get_knowledge_base_id_from_file():
    """
    从配置文件加载知识库 ID
    """
    import json
    import os
    
    # 优先检查环境变量
    if os.environ.get('COZE_KNOWLEDGE_BASE_ID'):
        return os.environ.get('COZE_KNOWLEDGE_BASE_ID')
    
    # 检查配置文件
    config_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        'config',
        'knowledge_config.json'
    )
    
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get('knowledge_base_id')
        except Exception:
            pass
    
    return None
