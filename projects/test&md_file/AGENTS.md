# 校园校小助智能对话工作流（增强版）

## 项目概述
- **名称**: 校园校小助
- **功能**: 基于知识库优先、联网备选的校园智能问答系统，集成智能追问、办事导航、答案溯源、相关推荐等创新功能

## 核心特性

### 1. 应答优先级机制
- **第一优先级**: 校园专属知识库检索
- **第二优先级**: 联网搜索兜底
- **无结果处理**: 标准校园友好话术

### 2. 创新功能（新增）
| 功能 | 描述 | 价值 |
|-----|------|-----|
| **智能追问** | 问题模糊时主动追问澄清（如校区、时间） | 提高问答准确率 |
| **办事导航** | 生成详细办事步骤、材料清单、注意事项 | 减少跑腿次数 |
| **相关推荐** | 推荐相关问题、快捷操作按钮 | 提升使用效率 |
| **答案溯源** | 标注信息来源和可信度 | 增强信任度 |

### 3. 网页跳转交互
- 自动识别跳转意向关键词
- 用户确认后才执行跳转
- 支持自定义校园网页链接

### 4. 校园场景适配
- 贴合师生日常交流风格
- 简洁易懂、正式温和
- 拒绝无关娱乐、商业内容

---

## 节点清单

| 节点名 | 文件位置 | 类型 | 功能描述 | 分支逻辑 | 配置文件 |
|-------|---------|------|---------|---------|---------|
| knowledge_search | `nodes/knowledge_search_node.py` | task | 检索校园知识库 | - | - |
| intent_recognition | `nodes/intent_recognition_node.py` | agent | 识别用户意图 | 根据意图分流 | `config/intent_recognition_llm_cfg.json` |
| smart_clarify | `nodes/smart_clarify_node.py` | agent | 智能追问澄清 | 需要追问→END，否则→继续 | `config/smart_clarify_llm_cfg.json` |
| answer_generation | `nodes/answer_generation_node.py` | agent | 答案生成与溯源 | 根据知识库结果分支 | `config/answer_generation_llm_cfg.json` |
| service_guide | `nodes/service_guide_node.py` | agent | 办事导航生成 | - | `config/service_guide_llm_cfg.json` |
| web_search | `nodes/web_search_node.py` | task | 联网搜索校园信息 | - | - |
| response_optimize | `nodes/response_optimize_node.py` | agent | 优化回复话术风格 | - | `config/response_optimize_llm_cfg.json` |
| related_recommend | `nodes/related_recommend_node.py` | agent | 相关问题推荐 | - | `config/related_recommend_llm_cfg.json` |
| no_result | `nodes/no_result_node.py` | agent | 无结果友好提示 | - | `config/no_result_llm_cfg.json` |
| jump_confirm | `nodes/jump_confirm_node.py` | task | 网页跳转确认提示 | - | - |

**类型说明**: task(普通节点) / agent(大模型节点) / condition(条件分支)

---

## 子图清单

暂无子图

---

## 技能使用

### 知识库技能
- **节点**: `knowledge_search_node`
- **用途**: 优先检索校园专属知识库
- **配置**: top_k=3, min_score=0.5

### 联网搜索技能
- **节点**: `web_search_node`
- **用途**: 知识库无答案时的兜底搜索
- **配置**: 偏向校园、教育类资讯

### 大语言模型技能
- **节点**: 意图识别、智能追问、答案生成、办事导航、话术优化、相关推荐、无结果回复
- **模型**: doubao-seed-2-0-lite-260215
- **用途**: 意图识别、内容生成、话术优化、智能追问

---

## 工作流流程图（增强版）

```
[开始]
   ↓
[知识库检索]
   ↓
[意图识别] ← 优先判断意图
   ↓
<意图分支>
   ├─ web_jump → [跳转确认] → [相关推荐] → [结束]
   ├─ service_guide → [办事导航] → [相关推荐] → [结束]
   ├─ campus_consult → [智能追问] → <追问判断>
   │                                       ├─ 需要追问 → [结束]（返回追问问题）
   │                                       └─ 无需追问 → [答案生成] → <知识库结果判断>
   │                                                                     ├─ 有结果 → [相关推荐] → [结束]
   │                                                                     └─ 无结果 → [联网搜索] → <搜索结果判断>
   │                                                                                             ├─ 有结果 → [话术优化] → [相关推荐] → [结束]
   │                                                                                             └─ 无结果 → [无结果回复] → [结束]
   └─ other → [无结果回复] → [结束]
```

---

## 后续功能拓展点位

### 已预留接口
1. **知识库批量更新**: 支持分类分区管理（学习类、生活类、办事类、活动类）
2. **自定义开关**: 可手动开启/关闭联网搜索、网页跳转功能
3. **网页链接管理**: 预留新增、修改、删除接口
4. **快捷操作按钮**: quick_actions 数组支持自定义扩展

### 计划功能
1. 校园日程提醒
2. 校内报修功能
3. 成绩查询对接
4. 语音对话支持
5. 班级专属资讯
6. 校园地图导航
7. 个性化问候（基于时间/角色）
8. 多轮对话上下文管理

---

## 网页嵌入对接说明

### 输出格式（增强版）
```json
{
  "response_content": "回复内容（Markdown格式）",
  "need_clarify": false,
  "clarify_questions": ["追问问题1", "追问问题2"],
  "need_jump": false,
  "jump_url": "",
  "jump_name": "",
  "related_questions": ["相关问题1", "相关问题2"],
  "quick_actions": [
    {"name": "按钮名称", "action": "jump|query|service", "url": "...", "query": "..."}
  ],
  "guide_steps": [
    {"step": 1, "action": "操作说明", "location": "地点", "department": "部门"}
  ]
}
```

### 前端接入示例
```javascript
// 1. 调用工作流API
const result = await fetch('/api/chat', {
  method: 'POST',
  body: JSON.stringify({ 
    user_query: userInput,
    user_role: 'student'  // 可选：student/teacher
  })
}).then(r => r.json());

// 2. 显示追问（如果有）
if (result.need_clarify) {
  showClarifyQuestions(result.clarify_questions);
  return;
}

// 3. 显示回复内容
displayMessage(result.response_content);

// 4. 显示办事指南步骤（如果有）
if (result.guide_steps?.length > 0) {
  renderGuideSteps(result.guide_steps);
}

// 5. 显示快捷操作按钮
if (result.quick_actions?.length > 0) {
  renderQuickActions(result.quick_actions);
}

// 6. 显示相关问题推荐
if (result.related_questions?.length > 0) {
  renderRelatedQuestions(result.related_questions);
}

// 7. 处理跳转（如果需要）
if (result.need_jump) {
  showJumpConfirm(result.jump_name, result.jump_url);
}
```

### 跳转交互
- 当 `need_jump=true` 时，前端可通过 `jump_url` 和 `jump_name` 执行跳转
- 跳转前已通过文字提示获得用户确认

### 对话上下文
- 支持多轮对话，保留历史聊天语境
- 通过 GraphInput 传递用户问题和角色

---

## 使用示例

### 示例1: 办事导航
```json
输入: {"user_query": "我想办理学生证补办，需要什么材料？", "user_role": "student"}
输出: {
  "response_content": "📋 **办事指南**\n\n📌 **办理步骤：**\n1. 下载并填写《学生证补办申请表》...\n\n📦 **所需材料：**\n• 本 人一寸免冠彩色证件照1张\n• ...",
  "guide_steps": [...],
  "related_questions": ["学生证补办需要多少钱？", "学生证补办多久能办好？"],
  "quick_actions": [
    {"name": "下载申请表", "action": "jump", "url": "/forms/student_card.docx"},
    {"name": "在线提交", "action": "service", "url": "/service/student_card"}
  ]
}
```

### 示例2: 智能追问
```json
输入: {"user_query": "图书馆开放时间"}
输出: {
  "need_clarify": true,
  "clarify_questions": [
    "请问你想查询哪个校区的图书馆开放时间呢？",
    "请问你是想查询工作日还是节假日的开放时间呢？"
  ]
}
```

### 示例3: 网页跳转
```json
输入: {"user_query": "我想打开教务系统"}
输出: {
  "response_content": "🔗 我检测到您可能需要访问【教务系统】",
  "need_jump": true,
  "jump_name": "教务系统",
  "related_questions": ["教务系统怎么查询期末成绩", "忘记教务系统密码怎么办"],
  "quick_actions": [
    {"name": "立即跳转教务系统", "action": "jump", "url": "/jwxt"}
  ]
}
```
