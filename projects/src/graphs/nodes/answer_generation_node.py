"""
答案生成节点
基于知识库内容生成答案，并标注信息来源和可信度
"""
import os
import json
from jinja2 import Template
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import LLMClient
from langchain_core.messages import SystemMessage, HumanMessage

from graphs.state import (
    AnswerGenerationInput,
    AnswerGenerationOutput
)


def answer_generation_node(
    state: AnswerGenerationInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> AnswerGenerationOutput:
    """
    title: 答案生成
    desc: 基于知识库内容生成答案，并标注信息来源和可信度
    integrations: 大语言模型
    """
    ctx = runtime.context
    
    # 读取配置文件
    cfg_path = config.get("metadata", {}).get("llm_cfg", "")
    if not cfg_path:
        cfg_path = config.get("configurable", {}).get("llm_cfg", "config/answer_generation_llm_cfg.json")
    
    full_cfg_path = os.path.join(
        os.getenv("COZE_WORKSPACE_PATH", ""),
        cfg_path
    )
    
    with open(full_cfg_path, 'r', encoding='utf-8') as f:
        cfg_data = json.load(f)
    
    llm_config = cfg_data.get("config", {})
    sp = cfg_data.get("sp", "")
    up = cfg_data.get("up", "")
    
    # 渲染用户提示词
    up_template = Template(up)
    user_prompt = up_template.render(
        user_query=state.user_query,
        knowledge_result=state.knowledge_result,
        knowledge_has_result=state.knowledge_has_result,
        source_type=state.source_type
    )
    
    # 初始化LLM客户端
    llm_client = LLMClient(ctx=ctx)
    
    # 构建消息
    messages = [
        SystemMessage(content=sp),
        HumanMessage(content=user_prompt)
    ]
    
    # 调用大模型
    response = llm_client.invoke(
        messages=messages,
        model=llm_config.get("model", "doubao-seed-2-0-lite-260215"),
        temperature=llm_config.get("temperature", 0.7),
        max_completion_tokens=llm_config.get("max_completion_tokens", 2000)
    )
    
    # 提取回复内容
    content = response.content if isinstance(response.content, str) else str(response.content)
    
    # 构建来源信息
    if state.knowledge_has_result:
        source_info = {
            "source": "校园知识库",
            "type": "knowledge",
            "reliability": "高",
            "update_time": "定期更新"
        }
        confidence = "high"
    else:
        source_info = {
            "source": "联网搜索",
            "type": "web_search",
            "reliability": "中",
            "update_time": "实时"
        }
        confidence = "medium"
    
    return AnswerGenerationOutput(
        response_content=content,
        source_info=source_info,
        confidence_level=confidence
    )
