# 校园校小助 UI 技术架构文档

## 1. 技术选型

### 1.1 前端技术栈

**核心框架**：
- HTML5（语义化标签）
- CSS3（现代特性：Flexbox, Grid, CSS Variables）
- JavaScript ES6+（原生，无框架依赖）

**外部库**：
- **Mermaid.js** (v10+): 流程图渲染
  - CDN: `https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js`
  - 用于渲染工作流拓扑图

- **Prism.js**: 代码高亮
  - CDN: `https://cdn.jsdelivr.net/npm/prismjs@1/prism.min.js`
  - 用于配置 JSON 展示

**图标**：
- **Lucide Icons**: 轻量级 SVG 图标
  - CDN: `https://unpkg.com/lucide@latest`
  - 简洁、现代风格

**字体**：
- Google Fonts: Noto Sans SC（中文）
- 本地加载或 CDN

### 1.2 设计系统

**CSS 架构**：
- BEM 命名规范（Block-Element-Modifier）
- CSS Variables 实现主题变量
- 组件化 CSS 结构

**色彩系统**：
```css
:root {
  /* 主色调 */
  --primary: #2563EB;
  --primary-dark: #1E40AF;
  --primary-light: #3B82F6;
  
  /* 辅助色 */
  --success: #10B981;
  --warning: #F59E0B;
  --error: #EF4444;
  
  /* 中性色 */
  --bg-primary: #F8FAFC;
  --bg-secondary: #FFFFFF;
  --sidebar-bg: #1E293B;
  --text-primary: #334155;
  --text-secondary: #64748B;
  --text-light: #94A3B8;
  
  /* 边框 */
  --border: #E2E8F0;
  --border-light: #F1F5F9;
}
```

**间距系统**：
```css
--spacing-xs: 4px;
--spacing-sm: 8px;
--spacing-md: 16px;
--spacing-lg: 24px;
--spacing-xl: 32px;
--spacing-2xl: 48px;
```

**圆角系统**：
```css
--radius-sm: 4px;
--radius-md: 8px;
--radius-lg: 12px;
--radius-xl: 16px;
```

---

## 2. 项目结构

```
ui/
├── index.html                    # 工作流概览页（首页）
├── nodes.html                    # 节点详情页
├── config.html                  # 模块配置页
├── links.html                    # Coze链接页
├── test.html                     # 测试页面
│
├── css/
│   ├── style.css                # 全局样式
│   ├── components.css           # 组件样式
│   └── pages/
│       ├── dashboard.css        # 仪表盘样式
│       ├── nodes.css            # 节点页面样式
│       ├── config.css           # 配置页面样式
│       └── links.css            # 链接页面样式
│
├── js/
│   ├── main.js                  # 主逻辑
│   ├── flowchart.js             # 流程图渲染
│   ├── navigation.js            # 导航逻辑
│   ├── config-manager.js        # 配置管理
│   └── utils.js                 # 工具函数
│
└── assets/
    ├── images/                  # 图片资源
    └── fonts/                   # 本地字体（如需）
```

---

## 3. 核心模块设计

### 3.1 流程图渲染模块 (`flowchart.js`)

**职责**：
- 定义工作流数据结构
- 生成 Mermaid 语法
- 渲染流程图
- 处理交互事件

**数据结构**：
```javascript
const workflowData = {
  nodes: [
    {
      id: 'knowledge_search',
      name: '知识库检索',
      type: 'task',
      description: '检索校园专属知识库',
      inputs: ['user_query'],
      outputs: ['knowledge_result', 'knowledge_score'],
      config: null
    },
    // ... 其他节点
  ],
  edges: [
    {
      from: 'knowledge_search',
      to: 'intent_recognition',
      label: ''
    },
    // ... 其他连接
  ],
  branches: [
    {
      from: 'intent_recognition',
      conditions: [
        { intent: 'web_jump', to: 'jump_confirm' },
        { intent: 'service_guide', to: 'service_guide' },
        { intent: 'campus_consult', to: 'smart_clarify' },
        { intent: 'other', to: 'no_result' }
      ]
    }
  ]
};
```

**API**：
```javascript
class FlowChartRenderer {
  constructor(containerId, config)
  loadData(data)
  render()
  highlightNode(nodeId)
  showNodeDetails(nodeId)
  exportAsSVG()
}
```

### 3.2 配置管理模块 (`config-manager.js`)

**职责**：
- 管理配置文件读取
- 表单数据绑定
- 配置验证
- 本地存储

**API**：
```javascript
class ConfigManager {
  constructor()
  
  // 加载配置
  async loadConfigs()
  
  // 获取配置
  getConfig(key)
  
  // 更新配置
  updateConfig(key, value)
  
  // 保存配置（到 localStorage）
  saveConfigs()
  
  // 导出配置
  exportConfigs()
  
  // 导入配置
  importConfigs(json)
}
```

### 3.3 导航模块 (`navigation.js`)

**职责**：
- 侧边栏菜单管理
- 页面路由（基于 hash）
- 面包屑导航

**API**：
```javascript
class NavigationManager {
  constructor()
  init()
  navigateTo(page)
  setActiveItem(itemId)
  updateBreadcrumb(path)
}
```

---

## 4. 页面详细设计

### 4.1 工作流概览页 (`index.html`)

**布局**：
```
┌─────────────────────────────────────────────┐
│  Header                                      │
├─────────┬───────────────────────────────────┤
│ Sidebar │  Content                          │
│         │  ┌─────────────────────────────┐ │
│ • 工作流 │  │  流程图展示（Mermaid）      │ │
│   概览  │  │                              │ │
│         │  └─────────────────────────────┘ │
│ • 节点  │  ┌──────────┬──────────┬──────┐ │
│   列表  │  │ 节点数    │ 连接数   │ 分支 │ │
│         │  │  10      │   15     │  4   │ │
│ • 配置  │  └──────────┴──────────┴──────┘ │
│   管理  │  ┌─────────────────────────────┐ │
│         │  │  快捷入口卡片                │ │
│ • Coze  │  │  • 测试工作流               │ │
│   链接  │  │  • 查看配置                  │ │
│         │  │  • Coze IDE                 │ │
│         │  └─────────────────────────────┘ │
└─────────┴───────────────────────────────────┘
```

**核心元素**：
1. **流程图容器**：`div#flowchart-container`
2. **统计卡片**：3个数字卡片
3. **快捷入口**：卡片列表

**Mermaid 配置**：
```javascript
mermaid.initialize({
  startOnLoad: false,
  theme: 'base',
  themeVariables: {
    primaryColor: '#2563EB',
    primaryTextColor: '#FFFFFF',
    primaryBorderColor: '#1E40AF',
    lineColor: '#94A3B8',
    secondaryColor: '#F1F5F9',
    tertiaryColor: '#F8FAFC'
  },
  flowchart: {
    htmlLabels: true,
    curve: 'basis'
  }
});
```

### 4.2 节点详情页 (`nodes.html`)

**布局**：
```
┌─────────────────────────────────────────────┐
│  Header                                      │
├─────────┬───────────────────────────────────┤
│ Sidebar │  Content                          │
│         │  ┌─────────────────────────────┐ │
│ • 工作流 │  │  节点列表（卡片网格）        │ │
│   概览  │  │  ┌────┐ ┌────┐ ┌────┐      │ │
│         │  │  │节点│ │节点│ │节点│      │ │
│ • 节点  │  │  │ 1 │ │ 2 │ │ 3 │      │ │
│   列表  │  │  └────┘ └────┘ └────┘      │ │
│         │  │  ┌────┐ ┌────┐ ...        │ │
│ • 配置  │  │  │节点│ │节点│              │ │
│   管理  │  │  │ 4 │ │ 5 │              │ │
│         │  │  └────┘ └────┘              │ │
│ • Coze  │  └─────────────────────────────┘ │
│   链接  │                                    │
└─────────┴───────────────────────────────────┘
```

**节点卡片内容**：
```
┌──────────────────────────┐
│ 🧠 intent_recognition    │  ← 图标 + ID
├──────────────────────────┤
│ 意图识别                  │  ← 中文名称
│ 识别用户提问意图          │  ← 描述
├──────────────────────────┤
│ 类型: Agent              │
│ 配置: intent_llm_cfg.json│
├──────────────────────────┤
│ 输入: user_query         │  ← 字段列表
│ 输出: intent_type        │
├──────────────────────────┤
│ [查看配置] [查看代码]     │  ← 操作按钮
└──────────────────────────┘
```

### 4.3 配置管理页 (`config.html`)

**布局**：
```
┌─────────────────────────────────────────────┐
│  Header                                      │
├─────────┬───────────────────────────────────┤
│ Sidebar │  Content                          │
│         │  ┌─────────────────────────────┐ │
│ • 工作流 │  │  Tab: LLM | 知识库 | 跳转   │ │
│   概览  │  ├─────────────────────────────┤ │
│         │  │  表单内容区                  │ │
│ • 节点  │  │                              │ │
│   列表  │  │  LLM 配置表单                │ │
│         │  │  ├─ 模型选择 (select)        │ │
│ • 配置  │  │  ├─ Temperature (range)    │ │
│   管理  │  │  ├─ Max Tokens (number)     │ │
│         │  │  └─ System Prompt (textarea)│ │
│ • Coze  │  │                              │ │
│   链接  │  ├─────────────────────────────┤ │
│         │  │  [保存配置]                  │ │
└─────────┴───────────────────────────────────┘
```

**Tab 切换**：
- LLM 配置
- 知识库配置
- 网页跳转配置
- 功能开关

### 4.4 Coze 链接页 (`links.html`)

**布局**：
```
┌─────────────────────────────────────────────┐
│  Header                                      │
├─────────┬───────────────────────────────────┤
│ Sidebar │  Content                          │
│         │  ┌─────────────────────────────┐ │
│ • 工作流 │  │  Coze 平台链接卡片          │ │
│   概览  │  │  ┌────────┐ ┌────────┐     │ │
│         │  │  │ Coze   │ │ 知识库 │     │ │
│ • 节点  │  │  │ IDE    │ │ 管理   │     │ │
│   列表  │  │  └────────┘ └────────┘     │ │
│         │  │  ┌────────┐ ┌────────┐     │ │
│ • 配置  │  │  │ API    │ │ 工作流 │     │ │
│   管理  │  │  │ 配置   │ │ 测试   │     │ │
│         │  │  └────────┘ └────────┘     │ │
│ • Coze  │  └─────────────────────────────┘ │
│   链接  │                                    │
└─────────┴───────────────────────────────────┘
```

**链接卡片内容**：
```
┌──────────────────────────────┐
│ 🔧 Coze IDE                  │
├──────────────────────────────┤
│ 打开 Coze 工作流编辑器        │
│ 进行工作流的开发和调试        │
├──────────────────────────────┤
│ URL: console.coze.cn         │
├──────────────────────────────┤
│ [打开链接]                   │
└──────────────────────────────┘
```

---

## 5. 数据流设计

### 5.1 工作流数据流

```
用户访问页面
     ↓
JavaScript 加载
     ↓
读取内置工作流数据（nodes + edges）
     ↓
调用 FlowChartRenderer.render()
     ↓
Mermaid.js 渲染 SVG 流程图
     ↓
显示在页面中
```

### 5.2 配置数据流

```
用户修改配置
     ↓
表单 onChange 事件
     ↓
更新 ConfigManager 内存数据
     ↓
保存到 localStorage
     ↓
可选：导出为 JSON 文件
```

---

## 6. 性能优化

### 6.1 资源加载

**CSS/JS 加载策略**：
```html
<!-- 非阻塞加载 -->
<link rel="stylesheet" href="css/style.css" media="print" onload="this.media='all'">
<script src="js/main.js" defer></script>
```

**Mermaid 延迟加载**：
```javascript
// 仅在需要时加载 Mermaid
if (document.querySelector('.mermaid')) {
  import('https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs')
    .then(mermaid => {
      mermaid.initialize({...});
      mermaid.run();
    });
}
```

### 6.2 首屏优化

**关键渲染路径**：
1. 内联关键 CSS（首屏样式）
2. 延迟加载非关键资源
3. 使用 `loading="lazy"` 加载图片

**骨架屏**：
```html
<div class="skeleton-flowchart">
  <div class="skeleton-line"></div>
  <div class="skeleton-node"></div>
</div>
```

---

## 7. 浏览器兼容

**目标浏览器**：
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- 不支持 IE

**兼容性策略**：
- 使用 CSS Variables
- ES6+ 语法（无需转译，现代浏览器）
- 渐进增强

---

## 8. 安全考虑

### 8.1 前端安全

- 无后端，纯静态页面
- 配置数据存储在 localStorage
- 不包含敏感信息
- 外部链接使用 `rel="noopener noreferrer"`

### 8.2 Coze 链接

- 所有链接指向 Coze 官方域名
- 提供新窗口打开

---

## 9. 部署方案

### 9.1 部署结构

```
/ui
  ├── index.html
  ├── nodes.html
  ├── config.html
  ├── links.html
  ├── test.html
  ├── css/
  │   └── style.css
  └── js/
      └── main.js
```

### 9.2 部署方式

**方式一：静态服务器**
```bash
# Nginx
server {
    location /ui/ {
        alias /var/www/campus-assistant/ui/;
        index index.html;
    }
}
```

**方式二：Coze 平台**
- 上传到 Coze IDE
- 作为静态资源访问

**方式三：GitHub Pages**
```yaml
# .github/workflows/deploy.yml
name: Deploy to GitHub Pages
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy
        run: |
          cp -r ui/* docs/
```

---

## 10. 开发规范

### 10.1 代码规范

**HTML**：
- 语义化标签
- ARIA 属性
- 适当的文档结构

**CSS**：
- BEM 命名
- 注释规范
- 变量化配置

**JavaScript**：
- ES6+ 语法
- JSDoc 注释
- 模块化组织

### 10.2 Git 规范

**分支策略**：
- main: 生产代码
- feature/ui: UI 开发
- fix/bugfix: 修复

**提交规范**：
```
feat: 新功能
fix: 修复
docs: 文档
style: 样式
refactor: 重构
```

---

## 11. 测试策略

### 11.1 手动测试清单

- [ ] 所有页面导航正常
- [ ] 流程图正确渲染
- [ ] 节点详情显示完整
- [ ] 配置表单可编辑
- [ ] 链接可点击跳转
- [ ] 响应式布局正常

### 11.2 浏览器测试

- Chrome（推荐）
- Firefox
- Safari
- Edge

---

**文档版本**：v1.0
**创建日期**：2026-05-21
**作者**：AI Assistant
