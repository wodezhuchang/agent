/*!
 * 校园校小助 UI - 主逻辑
 */

// 全局状态
const AppState = {
  currentPage: 'overview',
  sidebarOpen: false
};

// 初始化应用
document.addEventListener('DOMContentLoaded', () => {
  initNavigation();
  initFlowChart();
  initCards();
  initConfigForms();
  initSmoothScroll();
});

// 导航初始化
function initNavigation() {
  const currentPath = window.location.pathname;
  const pageName = currentPath.split('/').pop().replace('.html', '') || 'index';
  
  // 设置当前页面
  AppState.currentPage = pageName;
  
  // 高亮当前导航项
  const navLinks = document.querySelectorAll('.sidebar__link');
  navLinks.forEach(link => {
    const linkPage = link.getAttribute('data-page');
    if (linkPage === pageName) {
      link.classList.add('sidebar__link--active');
    }
  });
  
  // 移动端侧边栏切换
  const menuToggle = document.querySelector('.menu-toggle');
  if (menuToggle) {
    menuToggle.addEventListener('click', () => {
      AppState.sidebarOpen = !AppState.sidebarOpen;
      document.querySelector('.sidebar').classList.toggle('sidebar--open', AppState.sidebarOpen);
    });
  }
}

// 流程图初始化
function initFlowChart() {
  const container = document.getElementById('flowchart-container');
  if (!container) return;
  
  // 延迟加载 Mermaid
  setTimeout(() => {
    loadMermaidAndRender();
  }, 300);
}

async function loadMermaidAndRender() {
  // 检查是否已加载
  if (typeof mermaid !== 'undefined') {
    renderFlowChart();
    return;
  }
  
  // 动态加载 Mermaid
  const script = document.createElement('script');
  script.src = 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js';
  script.onload = renderFlowChart;
  document.head.appendChild(script);
}

function renderFlowChart() {
  const container = document.getElementById('flowchart-container');
  if (!container) return;
  
  mermaid.initialize({
    startOnLoad: false,
    theme: 'base',
    themeVariables: {
      primaryColor: '#2563EB',
      primaryTextColor: '#FFFFFF',
      primaryBorderColor: '#1E40AF',
      lineColor: '#94A3B8',
      secondaryColor: '#EFF6FF',
      tertiaryColor: '#F8FAFC'
    }
  });
  
  const mermaidCode = generateWorkflowDiagram();
  
  container.innerHTML = `<pre class="mermaid">${mermaidCode}</pre>`;
  
  mermaid.run({
    querySelector: '.mermaid'
  });
}

function generateWorkflowDiagram() {
  let code = 'graph TD\n\n';
  
  // 节点定义
  code += '    %% 节点定义\n';
  WORKFLOW_DATA.nodes.forEach(node => {
    const color = node.type === 'agent' ? '#10B981' : '#2563EB';
    code += `    ${node.id}["<b>${node.icon} ${node.name}</b><br/><small>${node.type.toUpperCase()}</small>"]\n`;
  });
  
  code += '\n    %% 连接定义\n';
  
  // 连接定义
  WORKFLOW_DATA.edges.forEach(edge => {
    const branch = WORKFLOW_DATA.branches.find(b => b.node === edge.from);
    
    if (branch && edge.label) {
      // 条件分支用虚线和标签
      code += `    ${edge.from} -.->|"${edge.label}"| ${edge.to}\n`;
    } else {
      // 普通连接用实线
      code += `    ${edge.from} --> ${edge.to}\n`;
    }
  });
  
  return code;
}

// 卡片交互
function initCards() {
  // 节点卡片点击
  document.querySelectorAll('.node-card').forEach(card => {
    card.addEventListener('click', () => {
      const nodeId = card.getAttribute('data-node');
      if (nodeId && window.showNodeDetail) {
        window.showNodeDetail(nodeId);
      }
    });
  });
  
  // Coze 链接卡片点击
  document.querySelectorAll('.link-card').forEach(card => {
    card.addEventListener('click', (e) => {
      // 不阻止默认行为，让链接正常跳转
    });
  });
}

// 配置表单初始化
function initConfigForms() {
  const configForms = document.querySelectorAll('.config-form');
  
  configForms.forEach(form => {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      saveConfig(form);
    });
  });
  
  // Tab 切换
  const tabs = document.querySelectorAll('.tab-btn');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const tabId = tab.getAttribute('data-tab');
      switchTab(tabId);
    });
  });
}

// 保存配置
function saveConfig(form) {
  const formData = new FormData(form);
  const config = Object.fromEntries(formData.entries());
  
  // 保存到 localStorage
  localStorage.setItem('workflow_config', JSON.stringify(config));
  
  // 显示成功提示
  showNotification('配置已保存', 'success');
}

// Tab 切换
function switchTab(tabId) {
  // 切换按钮状态
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.classList.toggle('active', btn.getAttribute('data-tab') === tabId);
  });
  
  // 切换内容
  document.querySelectorAll('.tab-content').forEach(content => {
    content.classList.toggle('hidden', content.id !== `tab-${tabId}`);
  });
}

// 显示节点详情
window.showNodeDetail = function(nodeId) {
  const node = WORKFLOW_DATA.nodes.find(n => n.id === nodeId);
  if (!node) return;
  
  // 创建详情模态框
  const modal = document.createElement('div');
  modal.className = 'modal';
  modal.innerHTML = `
    <div class="modal__content modal--lg">
      <div class="modal__header">
        <div class="flex items-center gap-md">
          <span style="font-size: 2rem;">${node.icon}</span>
          <div>
            <h2>${node.name}</h2>
            <code class="text-muted">${node.id}</code>
          </div>
        </div>
        <button class="modal__close" onclick="this.closest('.modal').remove()">&times;</button>
      </div>
      <div class="modal__body">
        <p class="mb-lg">${node.description}</p>
        
        <div class="detail-grid">
          <div class="detail-section">
            <h4>类型</h4>
            <span class="tag tag--${node.type}">${node.type}</span>
          </div>
          
          <div class="detail-section">
            <h4>配置文件</h4>
            <code>${node.config || '无'}</code>
          </div>
        </div>
        
        <div class="detail-section">
          <h4>输入字段</h4>
          <div class="flex flex-wrap gap-sm">
            ${node.inputs.map(inp => `<span class="tag tag--input">${inp}</span>`).join('')}
          </div>
        </div>
        
        <div class="detail-section">
          <h4>输出字段</h4>
          <div class="flex flex-wrap gap-sm">
            ${node.outputs.map(out => `<span class="tag tag--output">${out}</span>`).join('')}
          </div>
        </div>
        
        <div class="detail-section">
          <h4>集成技能</h4>
          <div class="flex flex-wrap gap-sm">
            ${node.integrations.map(int => `<span class="tag">${int}</span>`).join('')}
          </div>
        </div>
      </div>
    </div>
  `;
  
  document.body.appendChild(modal);
  
  // 点击背景关闭
  modal.addEventListener('click', (e) => {
    if (e.target === modal) modal.remove();
  });
};

// 通知提示
function showNotification(message, type = 'info') {
  const notification = document.createElement('div');
  notification.className = `notification notification--${type}`;
  notification.innerHTML = `
    <span>${message}</span>
    <button onclick="this.parentElement.remove()">&times;</button>
  `;
  
  document.body.appendChild(notification);
  
  // 自动消失
  setTimeout(() => {
    notification.classList.add('notification--fadeout');
    setTimeout(() => notification.remove(), 300);
  }, 3000);
}

// 平滑滚动
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });
}

// 导出函数供外部使用
window.WorkflowApp = {
  showNodeDetail: window.showNodeDetail,
  switchTab,
  saveConfig,
  generateWorkflowDiagram
};
