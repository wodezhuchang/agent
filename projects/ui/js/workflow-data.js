/*!
 * 校园校小助 UI - 工作流数据结构
 * 定义工作流的节点、连接和配置
 */

const WORKFLOW_DATA = {
  // 工作流基本信息
  info: {
    name: '校园校小助智能问答工作流',
    version: '1.0.0',
    description: '基于知识库优先、联网备选的校园智能问答系统',
    totalNodes: 10,
    totalEdges: 15
  },

  // 节点定义
  nodes: [
    {
      id: 'knowledge_search',
      name: '知识库检索',
      type: 'task',
      icon: '🔍',
      description: '优先检索校园专属知识库，获取匹配内容和相似度得分',
      inputs: ['user_query'],
      outputs: ['knowledge_result', 'knowledge_score', 'knowledge_has_result'],
      config: null,
      integrations: ['知识库'],
      file: 'nodes/knowledge_search_node.py'
    },
    {
      id: 'intent_recognition',
      name: '意图识别',
      type: 'agent',
      icon: '🧠',
      description: '分析用户提问意图，判断是校园咨询、网页跳转、办事导航还是其他需求',
      inputs: ['user_query', 'knowledge_result'],
      outputs: ['intent_type', 'web_jump_url', 'web_jump_name', 'is_service_request'],
      config: 'config/intent_recognition_llm_cfg.json',
      integrations: ['大语言模型'],
      file: 'nodes/intent_recognition_node.py'
    },
    {
      id: 'smart_clarify',
      name: '智能追问',
      type: 'agent',
      icon: '💬',
      description: '分析用户问题的清晰度，当问题模糊时主动追问澄清',
      inputs: ['user_query', 'knowledge_result'],
      outputs: ['need_clarify', 'clarify_questions', 'query_clarity'],
      config: 'config/smart_clarify_llm_cfg.json',
      integrations: ['大语言模型'],
      file: 'nodes/smart_clarify_node.py'
    },
    {
      id: 'answer_generation',
      name: '答案生成',
      type: 'agent',
      icon: '📝',
      description: '基于知识库内容生成答案，并标注信息来源和可信度',
      inputs: ['user_query', 'knowledge_result', 'knowledge_has_result'],
      outputs: ['response_content', 'source_info', 'confidence_level'],
      config: 'config/answer_generation_llm_cfg.json',
      integrations: ['大语言模型'],
      file: 'nodes/answer_generation_node.py'
    },
    {
      id: 'service_guide',
      name: '办事导航',
      type: 'agent',
      icon: '📋',
      description: '识别办事需求，输出详细的办事步骤、所需材料和注意事项',
      inputs: ['user_query', 'service_type'],
      outputs: ['response_content', 'guide_steps', 'required_materials', 'service_location'],
      config: 'config/service_guide_llm_cfg.json',
      integrations: ['大语言模型'],
      file: 'nodes/service_guide_node.py'
    },
    {
      id: 'web_search',
      name: '联网搜索',
      type: 'task',
      icon: '🌐',
      description: '当知识库无匹配结果时，进行联网实时搜索获取校园相关信息',
      inputs: ['user_query'],
      outputs: ['web_search_result', 'source_content', 'source_type'],
      config: null,
      integrations: ['联网搜索'],
      file: 'nodes/web_search_node.py'
    },
    {
      id: 'jump_confirm',
      name: '跳转确认',
      type: 'task',
      icon: '🔗',
      description: '检测到跳转意图后，输出确认提示，等待用户确认后再执行跳转',
      inputs: ['web_jump_url', 'web_jump_name'],
      outputs: ['response_content', 'need_jump', 'jump_url'],
      config: null,
      integrations: [],
      file: 'nodes/jump_confirm_node.py'
    },
    {
      id: 'response_optimize',
      name: '话术优化',
      type: 'agent',
      icon: '✨',
      description: '优化回复语气和内容，使其贴合校园师生日常交流风格',
      inputs: ['source_content', 'source_type'],
      outputs: ['response_content'],
      config: 'config/response_optimize_llm_cfg.json',
      integrations: ['大语言模型'],
      file: 'nodes/response_optimize_node.py'
    },
    {
      id: 'related_recommend',
      name: '相关推荐',
      type: 'agent',
      icon: '🎯',
      description: '根据用户当前问题推荐相关问题和快捷操作按钮，提升使用效率',
      inputs: ['user_query', 'response_content'],
      outputs: ['related_questions', 'quick_actions'],
      config: 'config/related_recommend_llm_cfg.json',
      integrations: ['大语言模型'],
      file: 'nodes/related_recommend_node.py'
    },
    {
      id: 'no_result',
      name: '无结果回复',
      type: 'agent',
      icon: '💡',
      description: '当知识库和联网搜索都无答案时，生成标准校园友好提示',
      inputs: ['user_query'],
      outputs: ['response_content'],
      config: 'config/no_result_llm_cfg.json',
      integrations: ['大语言模型'],
      file: 'nodes/no_result_node.py'
    }
  ],

  // 连接定义
  edges: [
    // 主流程
    { from: 'knowledge_search', to: 'intent_recognition', label: '' },
    
    // 意图分支
    { from: 'intent_recognition', to: 'jump_confirm', label: 'web_jump' },
    { from: 'intent_recognition', to: 'service_guide', label: 'service_guide' },
    { from: 'intent_recognition', to: 'smart_clarify', label: 'campus_consult' },
    { from: 'intent_recognition', to: 'no_result', label: 'other' },
    
    // 追问分支
    { from: 'smart_clarify', to: 'answer_generation', label: '需要追问' },
    { from: 'smart_clarify', to: 'answer_generation', label: '无需追问' },
    
    // 答案分支
    { from: 'answer_generation', to: 'related_recommend', label: '知识库回答' },
    { from: 'answer_generation', to: 'web_search', label: '联网搜索' },
    
    // 搜索分支
    { from: 'web_search', to: 'response_optimize', label: '有结果' },
    { from: 'web_search', to: 'no_result', label: '无结果' },
    
    // 话术优化
    { from: 'response_optimize', to: 'related_recommend', label: '' },
    
    // 办事导航
    { from: 'service_guide', to: 'related_recommend', label: '' },
    
    // 跳转确认
    { from: 'jump_confirm', to: 'related_recommend', label: '' }
  ],

  // 条件分支定义
  branches: [
    {
      node: 'intent_recognition',
      field: 'intent_type',
      conditions: [
        { value: 'web_jump', label: '网页跳转', to: 'jump_confirm', color: '#3B82F6' },
        { value: 'service_guide', label: '办事导航', to: 'service_guide', color: '#10B981' },
        { value: 'campus_consult', label: '校园咨询', to: 'smart_clarify', color: '#8B5CF6' },
        { value: 'other', label: '其他', to: 'no_result', color: '#6B7280' }
      ]
    },
    {
      node: 'smart_clarify',
      field: 'need_clarify',
      conditions: [
        { value: true, label: '需要追问', to: 'answer_generation', color: '#F59E0B' },
        { value: false, label: '无需追问', to: 'answer_generation', color: '#10B981' }
      ]
    },
    {
      node: 'answer_generation',
      field: 'knowledge_has_result',
      conditions: [
        { value: true, label: '知识库回答', to: 'related_recommend', color: '#10B981' },
        { value: false, label: '联网搜索', to: 'web_search', color: '#3B82F6' }
      ]
    },
    {
      node: 'web_search',
      field: 'web_search_result',
      conditions: [
        { value: 'has_result', label: '有结果', to: 'response_optimize', color: '#10B981' },
        { value: 'no_result', label: '无结果', to: 'no_result', color: '#EF4444' }
      ]
    }
  ],

  // 节点统计
  stats: {
    taskNodes: 3,    // knowledge_search, web_search, jump_confirm
    agentNodes: 7,   // 其他
    totalNodes: 10,
    totalEdges: 15,
    maxBranches: 4   // 意图识别分支
  },

  // Coze 链接配置
  cozeLinks: [
    {
      id: 'coze-ide',
      title: 'Coze IDE',
      description: '打开 Coze 工作流编辑器，进行工作流的开发和调试',
      url: 'https://www.coze.cn',
      icon: '🔧'
    },
    {
      id: 'knowledge-base',
      title: '知识库管理',
      description: '管理校园专属知识库，上传和更新文档内容',
      url: 'https://www.coze.cn/knowledge',
      icon: '📚'
    },
    {
      id: 'api-config',
      title: 'API 配置',
      description: '配置工作流 API，设置访问权限和限流规则',
      url: 'https://www.coze.cn/api',
      icon: '⚙️'
    },
    {
      id: 'workflow-test',
      title: '工作流测试',
      description: '在 Coze 平台测试工作流，查看执行日志',
      url: 'https://www.coze.cn/workflow',
      icon: '🧪'
    }
  ],

  // 配置项定义
  configs: {
    llm: {
      model: 'doubao-seed-2-0-lite-260215',
      temperature: 0.3,
      max_completion_tokens: 2000
    },
    knowledge: {
      top_k: 3,
      min_score: 0.5
    },
    features: {
      web_search_enabled: true,
      jump_enabled: true,
      knowledge_first: true
    }
  }
};

// 导出数据
if (typeof module !== 'undefined' && module.exports) {
  module.exports = WORKFLOW_DATA;
}
