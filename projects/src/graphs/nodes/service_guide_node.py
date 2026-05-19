"""
办事导航节点
识别办事需求，输出分步骤办事指南
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
    ServiceGuideInput,
    ServiceGuideOutput
)


def service_guide_node(
    state: ServiceGuideInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> ServiceGuideOutput:
    """
    title: 办事导航
    desc: 识别办事需求，输出详细的办事步骤、所需材料和注意事项
    integrations: 大语言模型
    """
    ctx = runtime.context
    
    # 读取配置文件
    cfg_path = config.get("metadata", {}).get("llm_cfg", "")
    if not cfg_path:
        cfg_path = config.get("configurable", {}).get("llm_cfg", "config/service_guide_llm_cfg.json")
    
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
        service_type=state.service_type,
        user_role=state.user_role
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
        temperature=llm_config.get("temperature", 0.5),
        max_completion_tokens=llm_config.get("max_completion_tokens", 2000)
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
        
        # 构建回复内容
        guide_steps = result_data.get("guide_steps", [])
        required_materials = result_data.get("required_materials", [])
        service_location = result_data.get("service_location", "")
        estimated_time = result_data.get("estimated_time", "")
        tips = result_data.get("tips", [])
        
        # 生成结构化回复
        response_parts = ["📋 **办事指南**\n"]
        
        # 办理步骤
        if guide_steps:
            response_parts.append("\n📌 **办理步骤：**\n")
            for step in guide_steps:
                step_num = step.get("step", 1)
                action = step.get("action", "")
                location = step.get("location", "")
                response_parts.append(f"{step_num}. {action}")
                if location:
                    response_parts.append(f"   📍 地点：{location}")
        
        # 所需材料
        if required_materials:
            response_parts.append("\n📦 **所需材料：**")
            for material in required_materials:
                response_parts.append(f"  • {material}")
        
        # 办理地点和时间
        if service_location:
            response_parts.append(f"\n🏢 **办理地点：** {service_location}")
        if estimated_time:
            response_parts.append(f"⏱️ **预计时间：** {estimated_time}")
        
        # 注意事项
        if tips:
            response_parts.append("\n💡 **注意事项：**")
            for tip in tips:
                response_parts.append(f"  • {tip}")
        
        response_content = "\n".join(response_parts)
        
        return ServiceGuideOutput(
            response_content=response_content,
            guide_steps=guide_steps,
            required_materials=required_materials,
            service_location=service_location,
            estimated_time=estimated_time,
            tips=tips
        )
    except Exception:
        # 解析失败，返回默认提示
        return ServiceGuideOutput(
            response_content="抱歉，暂未找到该办事流程的详细信息，建议您咨询相关部门获取详细指引。",
            guide_steps=[
                {"step": 1, "action": "请咨询相关部门获取详细流程"}
            ],
            required_materials=["请咨询相关部门确认所需材料"],
            service_location="请咨询相关部门",
            estimated_time="未知",
            tips=["建议提前电话咨询"]
        )
