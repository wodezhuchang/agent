"""
校园校小助工作流状态定义（增强版）
包含智能追问、答案溯源、相关推荐、办事导航等创新功能
"""
from typing import Optional, List, Literal
from pydantic import BaseModel, Field


# ==================== 全局状态 ====================
class GlobalState(BaseModel):
    """全局状态定义"""
    # 基础字段
    user_query: str = Field(default="", description="用户原始问题")
    user_role: str = Field(default="student", description="用户角色: student/teacher/staff")
    
    # 知识库相关
    knowledge_result: str = Field(default="", description="知识库检索结果")
    knowledge_score: float = Field(default=0.0, description="知识库检索相似度得分")
    knowledge_has_result: bool = Field(default=False, description="知识库是否有结果")
    
    # 意图识别
    intent_type: str = Field(default="campus_consult", description="意图类型")
    web_jump_url: str = Field(default="", description="网页跳转URL")
    web_jump_name: str = Field(default="", description="网页跳转名称")
    
    # 联网搜索
    web_search_result: str = Field(default="", description="联网搜索结果")
    source_content: str = Field(default="", description="用于优化的来源内容")
    source_type: str = Field(default="web_search", description="来源类型")
    
    # ===== 创新功能字段 =====
    # 智能追问
    need_clarify: bool = Field(default=False, description="是否需要追问澄清")
    clarify_questions: List[str] = Field(default=[], description="追问问题列表")
    query_clarity: str = Field(default="clear", description="问题清晰度: clear/vague/ambiguous")
    
    # 答案溯源
    source_info: dict = Field(default={}, description="信息来源详情")
    confidence_level: str = Field(default="medium", description="答案可信度: high/medium/low")
    reference_links: List[dict] = Field(default=[], description="参考链接列表")
    
    # 相关推荐
    related_questions: List[str] = Field(default=[], description="相关问题推荐")
    quick_actions: List[dict] = Field(default=[], description="快捷操作按钮")
    
    # 办事导航
    is_service_request: bool = Field(default=False, description="是否为办事请求")
    guide_steps: List[dict] = Field(default=[], description="办事步骤清单")
    required_materials: List[str] = Field(default=[], description="所需材料清单")
    service_location: str = Field(default="", description="办理地点")
    
    # 最终输出
    response_content: str = Field(default="", description="最终回复内容")
    need_jump: bool = Field(default=False, description="是否需要跳转")


# ==================== 图入参出参 ====================
class GraphInput(BaseModel):
    """工作流输入"""
    user_query: str = Field(..., description="用户提问内容")
    user_role: str = Field(default="student", description="用户角色: student/teacher/staff")


class GraphOutput(BaseModel):
    """工作流输出（增强版）"""
    # 基础输出
    response_content: str = Field(..., description="回复内容")
    need_jump: bool = Field(default=False, description="是否需要网页跳转")
    jump_url: str = Field(default="", description="跳转URL")
    jump_name: str = Field(default="", description="跳转网页名称")
    
    # 创新功能输出
    need_clarify: bool = Field(default=False, description="是否需要追问")
    clarify_questions: List[str] = Field(default=[], description="追问问题列表")
    source_info: dict = Field(default={}, description="信息来源详情")
    confidence_level: str = Field(default="medium", description="答案可信度")
    related_questions: List[str] = Field(default=[], description="相关问题推荐")
    quick_actions: List[dict] = Field(default=[], description="快捷操作按钮")
    is_service_guide: bool = Field(default=False, description="是否为办事指南")
    guide_steps: List[dict] = Field(default=[], description="办事步骤")


# ==================== 节点1: 知识库检索 ====================
class KnowledgeSearchInput(BaseModel):
    """知识库检索节点输入"""
    user_query: str = Field(..., description="用户提问")


class KnowledgeSearchOutput(BaseModel):
    """知识库检索节点输出"""
    knowledge_result: str = Field(default="", description="检索到的知识内容")
    knowledge_score: float = Field(default=0.0, description="相似度得分")
    knowledge_has_result: bool = Field(default=False, description="是否有有效结果")


# ==================== 节点2: 智能追问（新增） ====================
class SmartClarifyInput(BaseModel):
    """智能追问节点输入"""
    user_query: str = Field(..., description="用户提问")
    knowledge_result: str = Field(default="", description="知识库检索结果")
    knowledge_has_result: bool = Field(default=False, description="知识库是否有结果")


class SmartClarifyOutput(BaseModel):
    """智能追问节点输出"""
    need_clarify: bool = Field(default=False, description="是否需要追问")
    clarify_questions: List[str] = Field(default=[], description="追问问题列表")
    query_clarity: str = Field(default="clear", description="问题清晰度")
    clarified_query: str = Field(default="", description="澄清后的问题")


# ==================== 节点3: 意图识别 ====================
class IntentRecognitionInput(BaseModel):
    """意图识别节点输入"""
    user_query: str = Field(..., description="用户提问")
    user_role: str = Field(default="student", description="用户角色")


class IntentRecognitionOutput(BaseModel):
    """意图识别节点输出"""
    intent_type: str = Field(..., description="意图类型: campus_consult/web_jump/service_guide/other")
    web_jump_url: str = Field(default="", description="跳转URL")
    web_jump_name: str = Field(default="", description="跳转网页名称")
    is_service_request: bool = Field(default=False, description="是否为办事请求")
    service_type: str = Field(default="", description="办事类型")


# ==================== 节点4: 办事导航（新增） ====================
class ServiceGuideInput(BaseModel):
    """办事导航节点输入"""
    user_query: str = Field(..., description="用户提问")
    service_type: str = Field(default="", description="办事类型")
    user_role: str = Field(default="student", description="用户角色")


class ServiceGuideOutput(BaseModel):
    """办事导航节点输出"""
    response_content: str = Field(default="", description="办事指南回复内容")
    guide_steps: List[dict] = Field(default=[], description="办事步骤清单")
    required_materials: List[str] = Field(default=[], description="所需材料清单")
    service_location: str = Field(default="", description="办理地点")
    estimated_time: str = Field(default="", description="预计办理时间")
    tips: List[str] = Field(default=[], description="注意事项")


# ==================== 节点5: 答案生成 ====================
class AnswerGenerationInput(BaseModel):
    """答案生成节点输入"""
    user_query: str = Field(..., description="用户提问")
    knowledge_result: str = Field(default="", description="知识库内容")
    knowledge_has_result: bool = Field(default=False, description="知识库是否有结果")
    source_type: str = Field(default="knowledge", description="来源类型")


class AnswerGenerationOutput(BaseModel):
    """答案生成节点输出"""
    response_content: str = Field(..., description="生成的回复内容")
    source_info: dict = Field(default={}, description="信息来源详情")
    confidence_level: str = Field(default="medium", description="答案可信度")


# ==================== 节点6: 相关推荐（新增） ====================
class RelatedRecommendInput(BaseModel):
    """相关推荐节点输入"""
    user_query: str = Field(..., description="用户提问")
    intent_type: str = Field(default="", description="意图类型")
    response_content: str = Field(default="", description="已生成的回复")


class RelatedRecommendOutput(BaseModel):
    """相关推荐节点输出"""
    related_questions: List[str] = Field(default=[], description="相关问题推荐")
    quick_actions: List[dict] = Field(default=[], description="快捷操作按钮")


# ==================== 节点7: 联网搜索 ====================
class WebSearchInput(BaseModel):
    """联网搜索节点输入"""
    user_query: str = Field(..., description="用户提问")


class WebSearchOutput(BaseModel):
    """联网搜索节点输出"""
    web_search_result: str = Field(default="", description="搜索结果摘要")
    source_content: str = Field(default="", description="用于优化的来源内容")
    source_type: str = Field(default="web_search", description="来源类型")
    reference_links: List[dict] = Field(default=[], description="参考链接")


# ==================== 节点8: 话术优化 ====================
class ResponseOptimizeInput(BaseModel):
    """校园话术优化节点输入"""
    user_query: str = Field(..., description="用户提问")
    source_content: str = Field(..., description="来源内容")
    source_type: str = Field(default="web_search", description="来源类型")


class ResponseOptimizeOutput(BaseModel):
    """校园话术优化节点输出"""
    response_content: str = Field(..., description="优化后的回复内容")


# ==================== 节点9: 无结果回复 ====================
class NoResultInput(BaseModel):
    """无结果回复节点输入"""
    user_query: str = Field(..., description="用户提问")


class NoResultOutput(BaseModel):
    """无结果回复节点输出"""
    response_content: str = Field(..., description="友好提示回复")


# ==================== 节点10: 跳转确认 ====================
class JumpConfirmInput(BaseModel):
    """跳转确认节点输入"""
    web_jump_url: str = Field(..., description="跳转URL")
    web_jump_name: str = Field(..., description="跳转网页名称")
    user_query: str = Field(default="", description="用户提问")


class JumpConfirmOutput(BaseModel):
    """跳转确认节点输出"""
    response_content: str = Field(..., description="跳转确认提示")
    need_jump: bool = Field(default=True, description="需要跳转")
    jump_url: str = Field(default="", description="跳转URL")
    jump_name: str = Field(default="", description="跳转网页名称")



