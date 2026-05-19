"""
联网搜索节点
当知识库无答案时，进行联网搜索兜底
"""
import os
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import SearchClient

from graphs.state import (
    WebSearchInput,
    WebSearchOutput
)


def web_search_node(
    state: WebSearchInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> WebSearchOutput:
    """
    title: 联网搜索
    desc: 当知识库无匹配结果时，进行联网实时搜索获取校园相关信息
    integrations: 联网搜索
    """
    ctx = runtime.context
    
    # 初始化搜索客户端
    search_client = SearchClient(ctx=ctx)
    
    try:
        # 构建搜索查询，偏向教育类和校园相关信息
        # 在查询中添加"校园""大学"等关键词以获取更相关的结果
        search_query = f"{state.user_query} 校园 大学"
        
        # 执行搜索，获取带AI摘要的结果
        response = search_client.web_search_with_summary(
            query=search_query,
            count=5  # 获取前5条结果
        )
        
        # 提取搜索结果
        if response and response.summary:
            return WebSearchOutput(
                web_search_result=response.summary,
                source_content=response.summary,
                source_type="web_search"
            )
        elif response and response.web_items:
            # 如果没有摘要，拼接搜索结果片段
            snippets = []
            for i, item in enumerate(response.web_items[:3]):
                if item.snippet:
                    snippets.append(f"{i+1}. {item.snippet}")
            
            if snippets:
                result_text = "\n".join(snippets)
                return WebSearchOutput(
                    web_search_result=result_text,
                    source_content=result_text,
                    source_type="web_search"
                )
        
        # 无搜索结果
        return WebSearchOutput(
            web_search_result="",
            source_content="",
            source_type="web_search"
        )
        
    except Exception as e:
        # 搜索失败，返回空结果
        return WebSearchOutput(
            web_search_result="",
            source_content="",
            source_type="web_search"
        )
