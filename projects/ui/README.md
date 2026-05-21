# 校园校小助 UI 管理界面

校园校小助智能问答工作流的 Web 管理界面，用于可视化展示工作流结构、节点配置和 Coze 平台链接。

## 🎯 功能特性

- **工作流可视化**：使用 Mermaid.js 渲染工作流拓扑图
- **节点管理**：查看所有节点的功能、输入输出和配置
- **模块配置**：配置 LLM 模型、知识库参数和功能开关
- **Coze 链接**：快速访问 Coze 平台相关功能
- **工作流测试**：输入测试问题，查看工作流执行过程

## 📁 文件结构

```
ui/
├── index.html          # 工作流概览页（首页）
├── nodes.html          # 节点详情列表
├── config.html         # 模块配置页面
├── links.html          # Coze 平台链接
├── test.html           # 工作流测试页面
├── css/
│   └── style.css       # 全局样式文件
└── js/
    ├── workflow-data.js  # 工作流数据结构
    ├── flowchart.js     # 流程图渲染模块
    └── main.js         # 主逻辑文件
```

## 🚀 快速开始

### 方式一：直接打开

在浏览器中直接打开 `index.html` 文件：

```bash
# Windows
start index.html

# macOS
open index.html

# Linux
xdg-open index.html
```

### 方式二：本地服务器

使用 Python 或 Node.js 启动本地服务器：

```bash
# Python 3
python -m http.server 8000

# Node.js (npx)
npx http-server
```

然后访问：http://localhost:8000

### 方式三：部署到服务器

将 `ui` 文件夹部署到 Web 服务器：

```bash
# Nginx 配置示例
location /ui {
    alias /var/www/campus-assistant/ui;
    index index.html;
}
```

## 📱 页面说明

### 1. 工作流概览 (`index.html`)

展示工作流的完整拓扑图，包括：
- 10 个功能节点的可视化展示
- 节点间连接的流向
- 条件分支的虚线表示
- 统计数据卡片（节点数、连接数、分支数）

### 2. 节点列表 (`nodes.html`)

以卡片形式展示所有节点，每个节点包含：
- 节点名称和类型
- 功能描述
- 输入/输出字段
- 配置文件路径
- 集成技能
- 查看详情按钮

点击任意节点卡片可查看详细信息。

### 3. 模块配置 (`config.html`)

提供三个配置Tab：

**LLM 配置**
- 模型名称
- Temperature
- Max Tokens
- 系统提示词

**知识库配置**
- Top K 参数
- 最小相似度分数
- 知识库 ID

**功能开关**
- 知识库优先模式
- 联网搜索
- 网页跳转
- 智能追问
- 相关推荐

配置保存在浏览器 localStorage 中。

### 4. Coze 链接 (`links.html`)

快速链接到 Coze 平台：
- Coze IDE（工作流编辑器）
- 知识库管理
- API 配置
- 工作流测试

### 5. 工作流测试 (`test.html`)

交互式测试界面：
- 选择用户角色（学生/教师）
- 预设问题快速填充
- 自定义问题输入
- 实时执行日志
- 响应结果展示

## 🎨 技术栈

- **HTML5** + **CSS3** + **JavaScript** (原生 ES6+)
- **Mermaid.js** - 流程图渲染
- **Google Fonts** - Noto Sans SC 字体
- **无框架依赖** - 纯前端实现

## 🔧 自定义配置

### 修改 Coze 链接

编辑 `js/workflow-data.js` 中的 `cozeLinks` 数组：

```javascript
cozeLinks: [
  {
    id: 'coze-ide',
    title: 'Coze IDE',
    description: '工作流编辑器',
    url: 'https://console.coze.cn',
    icon: '🔧'
  },
  // 添加更多链接...
]
```

### 修改节点数据

编辑 `js/workflow-data.js` 中的 `nodes` 数组：

```javascript
nodes: [
  {
    id: 'node_id',
    name: '节点名称',
    type: 'task|agent',  // 节点类型
    icon: '🔍',
    description: '节点描述',
    inputs: ['input1', 'input2'],
    outputs: ['output1'],
    config: 'config/file.json',  // 配置文件
    integrations: ['LLM']
  }
]
```

### 修改工作流连接

编辑 `edges` 和 `branches` 数组来调整工作流拓扑。

## 📊 工作流结构

### 节点类型

- **Task（任务节点）**：执行特定任务，如知识库检索、联网搜索
- **Agent（AI代理节点）**：使用大语言模型进行推理和生成

### 流程说明

```
用户提问
   ↓
知识库检索 → 意图识别
                  ↓
    ┌─────────────┼─────────────┐
    ↓             ↓             ↓
  网页跳转    办事导航      校园咨询
    ↓             ↓             ↓
  跳转确认    办事指南      智能追问
    ↓             ↓             ↓
    └─────────────┼─────────────┘
                  ↓
            相关推荐
                  ↓
                结束
```

## 🌐 浏览器兼容性

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- 不支持 IE

## 📄 许可证

本项目遵循原有项目许可证。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📞 支持

如有问题，请查看：
- [项目主 README](../README.md)
- [部署指南](../DEPLOYMENT_GUIDE.md)
- [Coze 官方文档](https://www.coze.cn/docs)

---

**版本**：1.0.0  
**更新日期**：2026-05-21  
**作者**：AI Assistant
