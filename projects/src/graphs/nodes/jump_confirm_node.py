"""
跳转确认节点（增强版）
识别到跳转意图后，输出跳转确认提示
"""
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context

from graphs.state import GlobalState


def jump_confirm_node(
    state: GlobalState,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> dict:
    """
    title: 跳转确认
    desc: 检测到跳转意图后，输出确认提示，等待用户确认后再执行跳转
    integrations: 无
    """
    ctx = runtime.context
    
    # 生成跳转确认提示
    confirm_message = f"🔗 我检测到您可能需要访问【{state.web_jump_name}】\n\n"
    confirm_message += f"📍 跳转地址：{state.web_jump_url}\n\n"
    confirm_message += "请回复\"确认\"或\"跳转\"来访问该页面，或告诉我您还需要其他帮助。"
    
    return {
        "response_content": confirm_message,
        "need_jump": True,
        "jump_url": state.web_jump_url,
        "jump_name": state.web_jump_name
    }