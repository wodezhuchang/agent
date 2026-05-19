"""
相关推荐节点
基于用户问题推荐相关问题和快捷操作
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
    RelatedRecommendInput,
    RelatedRecommendOutput
)


def related_recommend_node(
    state: RelatedRecommendInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> RelatedRecommendOutput:
    """
    title: 相关推荐
    desc: 基于用户问题智能推荐相关问题和快捷操作按钮
    integrations: 大语言模型
    """
    ctx = runtime.context
    
    # 读取配置文件
    cfg_path = config.get("metadata", {}).get("llm_cfg", "")
    if not cfg_path:
        cfg_path = config.get("configurable", {}).get("llm_cfg", "config/related_recommend_llm_cfg.json")
    
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
        intent_type=state.intent_type,
        response_hint=state.response_content[:300] if state.response_content else ""
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
        max_completion_tokens=llm_config.get("max_completion_tokens", 800)
    )
    
    # 解析结果
    result_text = response.content if isinstance(response.content, str) else str(response.content)
    
    try:
        # 提取JSON
        if "```json" in result_text:
            json_str = result_text.split("```json")[1].split("```")[0].strip()
        elif "{" in result_text:
            start = result_text.index("{")
            end = result_text.rindex("}") + 1
            json_str = result_text[start:end]
        else:
            json_str = result_text
        
        result_data = json.loads(json_str)
        
        return RelatedRecommendOutput(
            related_questions=result_data.get("related_questions", []),
            quick_actions=result_data.get("quick_actions", [])
        )
    except Exception:
        # 解析失败，返回默认推荐
        return RelatedRecommendOutput(
            related_questions=[
                "校园卡如何办理？",
                "图书馆开放时间",
                "选课流程是什么？"
            ],
            quick_actions=[
                {"name": "教务系统", "action": "jump", "url": "https://jwc.example.edu.cn"},
                {"name": "图书馆", "action": "jump", "url": "https://library.example.edu.cn"}
            ]
        )
