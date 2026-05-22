# 知识库配置指南

## 🎯 问题说明

很多用户在使用这个项目时，都会遇到一个困惑：
- **提示词说"优先检索知识库"**
- **但代码中没有配置知识库 ID 的地方**
- **不知道知识库导入的代码是否存在**

### ✅ 真实情况

**知识库检索代码确实存在**，位于：
- 文件：`src/graphs/nodes/knowledge_search_node.py`
- 使用了 Coze SDK 的 `KnowledgeClient`

**但是**，之前的代码设计是：
```python
knowledge_client = KnowledgeClient(ctx=ctx)  # 从上下文中自动获取
```

**这导致**：需要通过 Coze 平台界面配置知识库绑定，但很多用户找不到这个配置入口。

---

## 🛠️ 已完成的修复

我们已经修复了这个问题，现在支持**多种方式配置知识库 ID**：

### 1. ✅ 创建了知识库配置文件
文件：`config/knowledge_config.json`

```json
{
  "knowledge_base_id": "这里填入您的知识库ID",
  "knowledge_base_name": "校园校小助知识库",
  "top_k": 3,
  "min_score": 0.5,
  "enabled": true,
  "description": "校园校小助知识库配置"
}
```

### 2. ✅ 更新了知识库检索代码
文件：`src/graphs/nodes/knowledge_search_node.py`

现在支持**三种配置方式**（按优先级）：

#### 方式1️⃣：环境变量（最高优先级）
```bash
# 设置环境变量
export COZE_KNOWLEDGE_BASE_ID=kb_xxxxxxxxxx
```

#### 方式2️⃣：配置文件
编辑 `config/knowledge_config.json`，填入知识库 ID：
```json
{
  "knowledge_base_id": "kb_xxxxxxxxxx"
}
```

#### 方式3️⃣：代码配置（Coze 平台）
在 Coze IDE 中配置知识库绑定

---

## 📋 如何配置知识库 ID

### 步骤1：获取知识库 ID

#### 在 Coze 平台获取：
1. 登录 [Coze 平台](https://www.coze.cn)
2. 进入 **「知识库」** 管理页面
3. 创建或选择您的知识库
4. 在知识库详情页复制 **知识库 ID**（格式：`kb_xxxxxxxxxx`）

#### 在我们的 UI 界面配置（推荐）：
1. 打开 `ui/config.html`
2. 找到「📂 本地知识库测试」卡片
3. 或者在「知识库配置」部分查看配置说明

### 步骤2：填入知识库 ID

#### 方式A：修改配置文件（推荐）
编辑 `config/knowledge_config.json`：
```json
{
  "knowledge_base_id": "kb_您的实际ID",
  "knowledge_base_name": "校园校小助知识库",
  "top_k": 3,
  "min_score": 0.5,
  "enabled": true
}
```

#### 方式B：设置环境变量
```bash
# Windows PowerShell
$env:COZE_KNOWLEDGE_BASE_ID="kb_xxxxxxxxxx"

# macOS / Linux
export COZE_KNOWLEDGE_BASE_ID="kb_xxxxxxxxxx"
```

### 步骤3：验证配置

#### 方法1：使用我们的 UI 界面测试
1. 打开 `ui/config.html`
2. 点击「📄 加载示例知识库」按钮
3. 输入问题测试检索功能

#### 方法2：运行测试脚本
```bash
cd c:\Users\yangd\Documents\GitHub\agent\projects
python quick_test.py
```

#### 方法3：在 Coze IDE 中测试
1. 在 Coze IDE 中运行工作流
2. 输入测试问题
3. 查看执行日志，确认知识库检索是否成功

---

## 🔍 如何确认知识库配置是否生效

### 查看日志输出

知识库检索节点会返回以下信息：
```python
{
    "knowledge_result": "检索到的内容",
    "knowledge_score": 0.85,
    "knowledge_has_result": True,
    "knowledge_base_id": "kb_xxxxxxxxxx",
    "knowledge_search_info": "检索到 3 条相关内容，最佳匹配得分: 0.85"
}
```

### 判断依据

| 情况 | `knowledge_has_result` | 说明 |
|------|------------------------|------|
| 知识库有匹配内容 | `True` | 知识库配置成功 |
| 知识库无匹配内容 | `False` | 知识库已连接，但问题不匹配 |
| 异常或未配置 | `False` | 知识库配置可能有问题 |

---

## 🧪 测试知识库检索

### 使用 UI 界面测试（最简单）

1. **打开配置页面**：
   ```
   双击打开 ui/config.html
   ```

2. **加载示例数据**：
   - 点击「📄 加载示例知识库」按钮
   - 会自动加载校园通知和校规校纪

3. **测试检索**：
   - 在搜索框输入：`图书馆开放时间`
   - 点击「🔍 测试检索」按钮
   - 应该能看到检索结果

### 本地测试 vs Coze 平台测试

| 测试方式 | 优点 | 缺点 |
|---------|------|------|
| **UI 界面测试** | 离线可用，简单直观 | 只是模拟，不能测试真实 Coze 工作流 |
| **Coze IDE 测试** | 测试完整工作流 | 需要部署到 Coze 平台 |
| **本地脚本测试** | 快速验证逻辑 | 需要 Coze SDK 环境 |

---

## ❓ 常见问题

### Q1：知识库 ID 在哪里找？

**答**：
1. 登录 Coze 平台
2. 进入「知识库」管理页面
3. 点击知识库名称进入详情页
4. 在 URL 或设置中找到 ID（格式：`kb_xxxxxxxxxx`）

### Q2：配置了知识库 ID 但检索不到内容？

**可能原因**：
1. **知识库为空**：需要在 Coze 平台上传文档
2. **知识库 ID 错误**：检查 ID 是否正确
3. **问题不匹配**：知识库中没有相关内容
4. **配置未生效**：需要重启 Coze IDE 或清除缓存

**解决方法**：
1. 确认知识库中已有文档
2. 检查 `config/knowledge_config.json` 中的 ID
3. 尝试重新导入项目到 Coze IDE

### Q3：本地测试正常，但 Coze 平台不工作？

**答**：
- 本地测试使用的是本地模拟数据
- Coze 平台需要：
  1. 在 Coze 平台创建并上传知识库
  2. 绑定知识库到工作流
  3. 部署工作流到 Coze 平台

### Q4：可以不用 Coze 平台配置知识库吗？

**答**：
可以！这就是我们创建**本地知识库测试**功能的原因：

1. **UI 界面测试**：
   - 打开 `ui/config.html`
   - 上传自己的文档
   - 本地测试检索功能

2. **局限性**：
   - 本地测试只是模拟，不能直接用于 Coze 工作流
   - 最终还是需要在 Coze 平台配置知识库

---

## 📊 知识库配置流程图

```
开始
  ↓
创建知识库（Coze 平台）
  ↓
上传文档（Coze 平台）
  ↓
获取知识库 ID
  ↓
配置到项目
  ├─ 方式1：环境变量
  ├─ 方式2：配置文件
  └─ 方式3：Coze IDE 绑定
  ↓
测试验证
  ├─ 本地 UI 测试
  └─ Coze 平台测试
  ↓
完成
```

---

## 🎯 最佳实践

### 1. 分阶段测试
- **第一阶段**：使用 UI 界面测试逻辑
- **第二阶段**：在 Coze 平台创建知识库
- **第三阶段**：绑定并测试完整工作流

### 2. 知识库内容管理
- 将文档分类整理（学习类、生活类、办事类）
- 定期更新知识库内容
- 清理过时信息

### 3. 配置检查清单
- [ ] 已在 Coze 平台创建知识库
- [ ] 已上传校园文档
- [ ] 已获取知识库 ID
- [ ] 已配置到 `config/knowledge_config.json`
- [ ] 已测试验证检索功能

---

## 📞 获取帮助

如果配置过程中遇到问题：
1. 查看日志输出
2. 检查配置文件
3. 尝试重新部署
4. 联系技术支持

---

**提示**：使用 UI 界面的「📄 加载示例知识库」功能，可以快速测试知识库检索逻辑，无需连接到真实的 Coze 平台！
