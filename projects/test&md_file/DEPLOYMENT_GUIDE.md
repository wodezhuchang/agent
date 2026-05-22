# Coze 平台部署指南

## 校园校小助工作流 - Coze 平台部署说明

### 📋 部署前准备

#### 1. 环境要求
- Python 3.12+
- Coze 平台账号（个人版或企业版）
- 已安装 Coze 开发工具（cozeloop, coze-coding-dev-sdk）

#### 2. 依赖安装
项目已配置以下依赖（在 `pyproject.toml` 中）：
```toml
dependencies = [
    "coze-coding-dev-sdk>0.5.0,<1",
    "coze-coding-utils>=0.2.6,<1",
    "coze-workload-identity>=0.1.4,<1",
    "cozeloop>=0.1.25,<1",
]
```

安装依赖：
```bash
cd c:\Users\yangd\Documents\GitHub\agent\projects
pip install -e .
```

---

## 🚀 部署步骤

### 方式一：通过 Coze IDE 直接部署（推荐）

#### 步骤1: 打开 Coze IDE
1. 登录 [Coze 平台](https://www.coze.cn)
2. 进入工作空间
3. 创建新项目或打开已有项目

#### 步骤2: 导入工作流代码
1. 将项目代码复制到 Coze IDE 中
2. 或通过 Git 仓库导入
3. 确保目录结构完整：
   ```
   project/
   ├── src/
   │   ├── graphs/
   │   │   ├── graph.py          # 工作流主图
   │   │   ├── state.py          # 状态定义
   │   │   └── nodes/            # 节点目录
   │   │       ├── knowledge_search_node.py
   │   │       ├── intent_recognition_node.py
   │   │       ├── smart_clarify_node.py
   │   │       └── ...
   │   └── main.py
   ├── config/
   │   └── *._llm_cfg.json       # 配置文件
   └── pyproject.toml
   ```

#### 步骤3: 配置知识库
1. 在 Coze 平台创建校园知识库
2. 上传校园相关文档（通知、校规、办事指南等）
3. 获取知识库 ID 并配置到节点中

#### 步骤4: 配置大语言模型
在 `config/` 目录下的 JSON 配置文件中设置：
- 模型选择：`doubao-seed-2-0-lite-260215` 或其他可用模型
- 温度参数（temperature）
- 最大令牌数（max_completion_tokens）

示例配置（`config/intent_recognition_llm_cfg.json`）：
```json
{
  "config": {
    "model": "doubao-seed-2-0-lite-260215",
    "temperature": 0.3,
    "max_completion_tokens": 1000
  },
  "sp": "系统提示词...",
  "up": "用户提示词模板..."
}
```

#### 步骤5: 配置联网搜索
在 `config/web_search_llm_cfg.json` 中配置搜索偏好：
- 搜索范围：高校校园、教育类平台
- 过滤无关内容

#### 步骤6: 测试工作流
在 Coze IDE 中：
1. 点击"测试运行"按钮
2. 输入测试问题验证流程
3. 检查日志和输出

#### 步骤7: 发布工作流
1. 点击"发布"按钮
2. 选择发布环境（测试/生产）
3. 配置访问权限
4. 获取 API 地址

---

### 方式二：通过命令行部署

#### 步骤1: 安装部署工具
```bash
pip install coze-cli
```

#### 步骤2: 登录 Coze
```bash
coze login
# 按提示输入账号密码
```

#### 步骤3: 初始化项目
```bash
cd c:\Users\yangd\Documents\GitHub\agent\projects
coze init
```

#### 步骤4: 配置部署
创建 `coze.yaml` 配置文件：
```yaml
project:
  name: 校园校小助
  version: 1.0.0
  
deployment:
  environment: production
  region: cn
  
workflow:
  entry: src.graph:main_graph
  config_dir: config/
```

#### 步骤5: 执行部署
```bash
coze deploy
```

#### 步骤6: 验证部署
```bash
coze test -i '{"user_query":"图书馆开放时间"}'
```

---

## 🔧 配置说明

### 知识库配置

编辑 `config/knowledge_search_llm_cfg.json`：
```json
{
  "knowledge_base_id": "your_knowledge_base_id",
  "top_k": 3,
  "min_score": 0.5
}
```

### 网页跳转配置

在 `config/jump_config.json` 中添加校园网页链接：
```json
{
  "jump_urls": [
    {
      "name": "教务系统",
      "url": "https://jwxt.example.edu.cn",
      "keywords": ["教务", "教务系统", "选课", "成绩"]
    },
    {
      "name": "图书馆",
      "url": "https://lib.example.edu.cn",
      "keywords": ["图书馆", "借书", "续借"]
    }
  ]
}
```

### LLM 模型配置

根据 Coze 平台支持的模型更新配置：
```json
{
  "model": "coze平台支持的模型名称",
  "temperature": 0.3,
  "max_completion_tokens": 2000
}
```

---

## 🌐 网页嵌入

### 获取 API 地址

部署成功后，在 Coze 平台获取：
- Webhook 地址
- API Key

### 前端集成

```javascript
// 调用示例
const response = await fetch('YOUR_DEPLOYED_API_URL', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer YOUR_API_KEY'
  },
  body: JSON.stringify({
    user_query: '图书馆开放时间',
    user_role: 'student'
  })
});

const result = await response.json();
console.log(result.response_content);
```

---

## 🐛 调试与监控

### 查看日志
```bash
# 本地查看日志
tail -f logs/workflow.log

# Coze 平台日志
# 在 Coze IDE 的"日志"面板查看
```

### 常见问题

#### 1. 依赖缺失
```bash
pip install -e .
```

#### 2. 知识库无响应
- 检查知识库 ID 是否正确
- 确认知识库已上传文档
- 检查网络连接

#### 3. 模型调用失败
- 检查 API Key 配置
- 确认模型配额充足
- 查看 Coze 平台状态

---

## 📊 性能优化建议

### 1. 知识库优化
- 定期更新知识库内容
- 优化文档结构和分段
- 调整 `top_k` 和 `min_score` 参数

### 2. 模型选择
- 测试不同模型的响应速度和准确性
- 根据实际场景选择合适模型
- 考虑使用缓存减少 API 调用

### 3. 工作流优化
- 减少不必要的节点调用
- 优化条件判断逻辑
- 使用流式输出提升用户体验

---

## 🔒 安全注意事项

1. **API Key 安全**
   - 不要在代码中硬编码 API Key
   - 使用环境变量或 Coze 环境变量功能

2. **知识库权限**
   - 根据需要设置知识库访问权限
   - 敏感信息脱敏处理

3. **输入验证**
   - 对用户输入进行过滤
   - 防止恶意查询

---

## 📞 获取帮助

- Coze 官方文档：https://www.coze.cn/docs
- 技术支持：联系 Coze 平台客服
- 社区论坛：加入 Coze 开发者社区

---

## ✅ 检查清单

部署前请确认：
- [ ] Python 环境版本 >= 3.12
- [ ] 依赖已正确安装
- [ ] 知识库已创建并上传文档
- [ ] LLM 模型已配置
- [ ] 网页跳转链接已配置
- [ ] 测试用例已通过
- [ ] API Key 已获取
- [ ] 安全配置已完成

---

**祝部署顺利！🎉**
