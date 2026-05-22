# Coze Vibe 项目完整使用指南

## 📌 重要：这是 Vibe Coding 项目，不是传统图形化工作流

### 两者的区别

| 传统 Coze 图形化工作流 | Coze Vibe Coding 项目 |
|-------------------|-------------------|
| ✅ 拖拽式节点编辑 | ❌ 代码驱动的工作流 |
| ✅ 可视化流程图 | ✅ 通过代码定义节点连接 |
| ✅ 界面配置知识库 | ✅ 通过配置文件管理 |
| ✅ 图形化 API 配置 | ✅ 代码中配置技能 |
| 📋 适合简单流程 | 📋 适合复杂、灵活的流程 |

---

## 🚀 在 Coze 平台使用本项目的正确方式

### 步骤1：确认您正在使用 Coze Vibe IDE

1. 登录 [Coze 平台](https://www.coze.cn)
2. 进入您的工作空间
3. 确认您看到的是 **Vibe IDE**（代码编辑器界面），而不是传统的图形化工作流编辑器

### 步骤2：导入或创建项目

#### 方式A：直接导入已有代码（推荐）

如果您的项目已经在本地：

1. 在 Coze Vibe IDE 中选择 **「导入项目」** 或 **「打开本地项目」**
2. 导航到：`c:\Users\yangd\Documents\GitHub\agent\projects`
3. 选择整个 `projects` 文件夹导入

#### 方式B：在 Coze IDE 中直接编辑代码

Coze IDE 已经打开了这个项目的话：

1. 在左侧文件浏览器中确认看到以下文件结构：
   ```
   projects/
   ├── src/
   │   ├── graphs/
   │   │   ├── graph.py          # 工作流主图
   │   │   ├── state.py
   │   │   └── nodes/
   │   └── main.py
   ├── config/
   │   └── *.json
   ├── ui/
   └── pyproject.toml
   ```

---

## 📚 如何配置知识库

### 1️⃣ 在 Coze 平台创建知识库

#### 步骤：
1. 在 Coze 平台左侧导航栏，找到 **「知识库」** 或 **「Knowledge Base」**
2. 点击 **「创建知识库」**
3. 输入知识库名称：`校园校小助知识库`
4. 选择知识库类型（推荐：**文档型知识库**）
5. 点击 **「创建」**

### 2️⃣ 上传文档

在创建好的知识库中：

1. 点击 **「上传文档」** 或 **「Add Documents」**
2. 上传您的校园相关文件（支持以下格式）：
   - PDF 文档
   - Word 文档（.doc, .docx）
   - 纯文本文件（.txt）
   - Markdown 文件（.md）
   - PowerPoint（.ppt, .pptx）
   - Excel（.xls, .xlsx）
3. 等待文档解析完成（这个过程可能需要几分钟）

### 3️⃣ 获取知识库 ID

文档上传成功后：

1. 在知识库列表中找到您刚创建的知识库
2. 点击进入详情页
3. 在页面 URL 中找到知识库 ID（格式类似：`kb_xxxxxxxxxx`）
4. 或者在知识库设置页查看 **知识库 ID**
5. 复制这个 ID

### 4️⃣ 配置到项目中

**方式A：通过代码配置**（推荐）

编辑相关节点文件，例如 `knowledge_search_node.py`：

```python
# 在 knowledge_search_node.py 中设置
knowledge_base_id = "kb_您的知识库ID"
```

**方式B：通过 UI 界面配置**

我们创建的 UI 界面可以帮助配置：

1. 在本地打开 `ui/config.html`
2. 切换到 **「知识库」** Tab
3. 在 **「知识库 ID」** 输入框粘贴您的 ID
4. 保存配置（保存到 localStorage）

**方式C：通过配置文件**

如果有 `config/knowledge_config.json`，编辑它：

```json
{
  "knowledge_base_id": "kb_您的知识库ID",
  "top_k": 3,
  "min_score": 0.5
}
```

---

## ⚙️ 如何配置 API 和技能

### 1️⃣ 查看当前项目使用的技能

查看节点文件，了解哪些技能在被使用：

#### 知识库检索技能
文件：`src/graphs/nodes/knowledge_search_node.py`
- 使用 Coze 内置的知识库检索技能
- 无需额外 API Key

#### 大语言模型技能
文件：所有 agent 类型节点
- 配置在 `config/*_llm_cfg.json`
- 使用 Coze 平台提供的模型

#### 联网搜索技能
文件：`src/graphs/nodes/web_search_node.py`
- 使用 Coze 内置的搜索技能
- 无需额外 API Key

### 2️⃣ 配置 LLM 模型

查看 `config/` 目录下的配置文件，例如：

**`config/intent_recognition_llm_cfg.json`**:
```json
{
  "config": {
    "model": "doubao-seed-2-0-lite-260215",
    "temperature": 0.3,
    "max_completion_tokens": 1000
  },
  "sp": "您是校园校小助...",
  "up": "用户问题：{user_query}"
}
```

**可用的 Coze 模型**（根据实际情况选择）：
- `doubao-seed-2-0-lite-260215`
- `doubao-seed-2-0-pro-260215`
- 其他 Coze 支持的模型

### 3️⃣ 在 Coze 平台启用技能

在 Coze Vibe IDE 中：

1. 查看左侧边栏的 **「技能」** 或 **「Skills」** 面板
2. 确认以下技能已启用：
   - ✅ 知识库检索
   - ✅ 联网搜索
   - ✅ 大语言模型
3. 如果某个技能未启用，点击启用按钮

---

## 👁️ 如何查看和测试工作流

### 方式1：使用我们创建的 UI 界面（推荐）

这个界面可以让您直观地看到工作流结构：

```bash
# Windows
cd c:\Users\yangd\Documents\GitHub\agent\projects\ui
start.bat

# macOS/Linux
cd ~/Documents/GitHub/agent/projects/ui
./start.sh
```

然后访问：
- **工作流概览**：`index.html` - 查看完整流程图
- **节点详情**：`nodes.html` - 查看每个节点的功能
- **配置管理**：`config.html` - 配置参数
- **工作流测试**：`test.html` - 模拟测试

### 方式2：在 Coze Vibe IDE 中运行测试

1. 在 Coze IDE 中打开终端
2. 运行测试命令：
   ```bash
   cd c:\Users\yangd\Documents\GitHub\agent\projects
   bash scripts/local_run.sh -m flow
   ```
3. 或者运行我们创建的快速测试：
   ```bash
   python quick_test.py
   ```

### 方式3：使用 Coze IDE 的预览功能

1. 在 Coze IDE 中找到 **「预览」** 或 **「Preview」** 按钮
2. 选择 **「工作流测试」**
3. 输入测试问题，查看执行结果

---

## 🎨 我们创建的 UI 界面如何帮助管理

### UI 功能概览

| 页面 | 功能 | 用途 |
|-----|------|-----|
| `index.html` | 工作流可视化 | 查看节点连接和流程逻辑 |
| `nodes.html` | 节点详情 | 了解每个节点的输入输出和配置 |
| `config.html` | 配置管理 | 配置 LLM 模型、知识库参数、功能开关 |
| `links.html` | Coze 链接 | 快速跳转到 Coze 平台各功能区 |
| `test.html` | 工作流测试 | 模拟输入，查看工作流响应 |

### 使用场景

**场景1：理解工作流结构**
```
用户：我不知道工作流是怎么走的？
解决：打开 index.html，查看完整流程图
```

**场景2：配置知识库 ID**
```
用户：我有了新的知识库 ID，怎么配置？
解决：打开 config.html，在知识库 Tab 中粘贴 ID
```

**场景3：快速跳转到 Coze**
```
用户：我想上传更多知识库文档？
解决：打开 links.html，点击知识库管理链接
```

**场景4：测试工作流**
```
用户：我想看看工作流会怎么回复？
解决：打开 test.html，输入问题模拟测试
```

---

## 🔧 常见问题解决

### Q1：我在 Coze 平台看不到工作流界面？

**A**：这是正常的。Vibe Coding 项目使用代码定义工作流，不是图形化界面。请：
1. 查看我们创建的 UI 界面
2. 或者查看代码文件 `src/graphs/graph.py` 理解流程

### Q2：如何上传知识库文件？

**A**：
1. 在 Coze 平台左侧找「知识库」
2. 创建知识库并上传文档
3. 获取知识库 ID
4. 配置到项目中

### Q3：API 密钥在哪里配置？

**A**：
- Coze 平台的技能（知识库、搜索、LLM）不需要额外 API Key
- 如果需要外部 API，在 Coze IDE 的「设置」→「环境变量」中配置

### Q4：如何在 Coze 平台直接测试工作流？

**A**：
1. 在 Coze IDE 中找到「测试」或「Preview」
2. 或者运行 `python quick_test.py`
3. 或者使用我们的 `ui/test.html`

---

## 📋 检查清单

配置项目前，请确认：

- [ ] 已在 Coze 平台创建知识库
- [ ] 已上传校园相关文档到知识库
- [ ] 已获取知识库 ID
- [ ] 已检查 config/ 目录下的 LLM 配置
- [ ] 已运行测试验证流程正常
- [ ] 已打开我们的 UI 界面了解工作流结构

---

## 🎯 推荐工作流程

1. **首先**：打开我们的 UI 界面 `ui/index.html` 了解工作流结构
2. **然后**：在 Coze 平台创建知识库，上传文档，获取 ID
3. **接着**：通过 UI 的 `config.html` 配置知识库 ID
4. **测试**：使用 `ui/test.html` 或运行 `quick_test.py` 测试
5. **部署**：在 Coze IDE 中部署和发布工作流

---

## 📞 获取更多帮助

- **UI 文档**：查看 `ui/README.md`
- **部署指南**：查看 `DEPLOYMENT_GUIDE.md`
- **Coze 文档**：[Coze 官方文档](https://www.coze.cn/docs)
- **Vibe Coding**：[Coze Vibe 编程指南](https://www.coze.cn/docs/vibe-coding)
