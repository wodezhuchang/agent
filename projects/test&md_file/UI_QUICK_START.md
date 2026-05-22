# 快速参考指南

## 🎉 UI 界面创建完成！

已成功创建校园校小助的 Web 管理界面，包含以下内容：

### 📁 文件清单

#### 文档文件
```
ui/
├── README.md              ← UI 使用说明
├── start.bat             ← Windows 快速启动脚本
└── start.sh              ← macOS/Linux 启动脚本
```

#### HTML 页面
```
ui/
├── index.html            ← 工作流概览页（首页）
├── nodes.html            ← 节点详情列表
├── config.html           ← 模块配置页面
├── links.html            ← Coze 平台链接
└── test.html             ← 工作流测试页面
```

#### CSS 样式
```
ui/css/
└── style.css            ← 全局样式文件（约 800 行）
```

#### JavaScript
```
ui/js/
├── workflow-data.js      ← 工作流数据结构定义
├── flowchart.js          ← Mermaid 流程图渲染
└── main.js               ← 主逻辑和交互
```

#### 需求文档
```
projects/.trae/documents/
├── PRD.md                ← 产品需求文档
└── TECH_ARCHITECTURE.md  ← 技术架构文档
```

---

## 🚀 如何使用

### 方法 1：快速启动（推荐）

**Windows 用户：**
```bash
cd c:\Users\yangd\Documents\GitHub\agent\projects\ui
start.bat
```

**macOS/Linux 用户：**
```bash
cd ~/Documents/GitHub/agent/projects/ui
chmod +x start.sh
./start.sh
```

### 方法 2：直接打开

双击 `ui/index.html` 文件在浏览器中打开。

### 方法 3：本地服务器

```bash
cd c:\Users\yangd\Documents\GitHub\agent\projects\ui
python -m http.server 8080
```
然后访问：http://localhost:8080

---

## 📱 页面功能

### 1️⃣ 工作流概览 (`index.html`)

**功能：**
- ✅ 显示完整工作流拓扑图（Mermaid 流程图）
- ✅ 展示统计数据（10个节点、15条连接、4个分支）
- ✅ 快捷操作入口卡片
- ✅ 图例说明

**亮点：**
- 点击节点可查看详情
- 支持缩放和平移
- 条件分支用虚线标注

### 2️⃣ 节点列表 (`nodes.html`)

**功能：**
- ✅ 以卡片网格展示所有 10 个节点
- ✅ 显示节点类型（Task/Agent）
- ✅ 展示输入/输出字段
- ✅ 点击查看完整详情

**节点类型：**
- 🧠 Agent 节点（AI 代理）：7个
- 🔍 Task 节点（任务）：3个

### 3️⃣ 模块配置 (`config.html`)

**功能：**
- ✅ Tab 切换：LLM / 知识库 / 功能开关
- ✅ LLM 配置：模型、温度、令牌数
- ✅ 知识库配置：Top K、最小分数
- ✅ 功能开关：5个可控制的功能

**数据持久化：**
- 配置保存在浏览器 localStorage
- 刷新页面自动恢复

### 4️⃣ Coze 链接 (`links.html`)

**功能：**
- ✅ 4 个 Coze 平台快速链接
- ✅ 点击直接跳转到目标页面
- ✅ 显示完整 URL 地址

**链接列表：**
- 🔧 Coze IDE（工作流编辑器）
- 📚 知识库管理
- ⚙️ API 配置
- 🧪 工作流测试

### 5️⃣ 工作流测试 (`test.html`)

**功能：**
- ✅ 选择用户角色（学生/教师）
- ✅ 预设问题快速填充
- ✅ 自定义问题输入
- ✅ 实时执行日志显示
- ✅ 模拟响应结果展示

**预设问题：**
- 图书馆开放时间
- 打开教务系统
- 学生证补办
- 简短问题（测试追问）
- 其他问题

---

## 🎨 界面特点

### 设计风格
- **主题**：科技感 + 简洁专业
- **主色**：蓝色 (#2563EB)
- **强调色**：绿色、橙色、红色
- **字体**：Noto Sans SC（中文优化）

### 交互特性
- 流畅的页面切换动画
- 卡片悬浮效果
- 节点点击高亮
- 响应式布局（支持移动端）
- 平滑滚动和过渡

### 技术亮点
- ✅ 纯前端实现（无框架依赖）
- ✅ 使用 Mermaid.js 渲染流程图
- ✅ 语义化 HTML 结构
- ✅ CSS Variables 主题系统
- ✅ ES6+ JavaScript
- ✅ 浏览器兼容性好

---

## 🔧 自定义配置

### 修改 Coze 链接

编辑 `ui/js/workflow-data.js`：

```javascript
cozeLinks: [
  {
    id: 'your-link',
    title: '你的链接名称',
    description: '链接描述',
    url: 'https://your-url.com',
    icon: '🔗'  // emoji 图标
  }
]
```

### 修改节点信息

编辑 `ui/js/workflow-data.js` 中的 `nodes` 数组：

```javascript
{
  id: 'node_id',
  name: '节点名称',
  type: 'task|agent',
  icon: '🔍',
  description: '节点描述',
  inputs: ['input1', 'input2'],
  outputs: ['output1'],
  config: 'config/file.json',
  integrations: ['LLM']
}
```

### 修改样式主题

编辑 `ui/css/style.css` 中的 CSS Variables：

```css
:root {
  --primary: #2563EB;        /* 主色 */
  --success: #10B981;        /* 成功色 */
  --warning: #F59E0B;        /* 警告色 */
  --sidebar-bg: #1E293B;    /* 侧边栏背景 */
}
```

---

## 📊 工作流拓扑

```
[知识库检索] → [意图识别]
                   ↓
      ┌───────────┼───────────┐
      ↓           ↓           ↓
  [跳转确认]  [办事导航]  [智能追问]
      ↓           ↓           ↓
      └───────────┴─────┬─────┘
                        ↓
                  [答案生成]
                        ↓
            ┌───────────┴───────────┐
            ↓                       ↓
      [相关推荐]              [联网搜索]
            ↑                       ↓
            └───────────┬───────────┘
                        ↓
                  [话术优化]
                        ↓
                  [相关推荐] → [END]
```

---

## 💡 常见问题

### Q: 为什么流程图不显示？

**A:** 确保已加载 Mermaid.js。检查浏览器控制台是否有错误。

### Q: 配置保存后刷新页面丢失？

**A:** 配置保存在 localStorage 中。检查浏览器是否禁用了 localStorage。

### Q: 如何部署到服务器？

**A:** 将整个 `ui` 文件夹上传到 Web 服务器，确保服务器支持 SPA（单页应用）路由。

### Q: 能集成到现有的 Coze 项目吗？

**A:** 可以。这个 UI 是独立的前端项目，可以部署在任何静态托管服务上。

---

## 🌟 下一步建议

1. **查看文档**
   - 阅读 `ui/README.md` 了解详细功能
   - 查看 `PRD.md` 了解产品需求
   - 查看 `TECH_ARCHITECTURE.md` 了解技术架构

2. **本地测试**
   - 启动 UI 界面
   - 测试所有功能
   - 检查流程图渲染

3. **自定义开发**
   - 修改 Coze 链接
   - 调整配色主题
   - 添加新功能

4. **部署上线**
   - 部署到测试服务器
   - 配置域名
   - 集成到校园网站

---

## 📞 获取帮助

- 查看完整文档：[`ui/README.md`](ui/README.md)
- 查看产品需求：[`.trae/documents/PRD.md`](.trae/documents/PRD.md)
- 查看技术架构：[`.trae/documents/TECH_ARCHITECTURE.md`](.trae/documents/TECH_ARCHITECTURE.md)
- Coze 官方文档：https://www.coze.cn/docs

---

**祝使用愉快！🎉**
