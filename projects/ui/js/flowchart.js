/*!
 * 校园校小助 UI - 流程图渲染模块
 * 使用 Mermaid.js 渲染工作流拓扑图
 */

class FlowChartRenderer {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.mermaidContainer = null;
    this.initialized = false;
    
    if (!this.container) {
      console.error('FlowChart container not found:', containerId);
      return;
    }
    
    this.init();
  }

  async init() {
    // 等待 Mermaid 加载
    if (typeof mermaid === 'undefined') {
      await this.loadMermaid();
    }
    
    mermaid.initialize({
      startOnLoad: false,
      theme: 'base',
      themeVariables: {
        primaryColor: '#2563EB',
        primaryTextColor: '#FFFFFF',
        primaryBorderColor: '#1E40AF',
        lineColor: '#94A3B8',
        secondaryColor: '#EFF6FF',
        tertiaryColor: '#F8FAFC',
        background: '#FFFFFF',
        mainBkg: '#2563EB',
        nodeBorder: '#1E40AF',
        clusterBkg: '#F1F5F9',
        clusterBorder: '#CBD5E1',
        titleColor: '#334155',
        edgeLabelBackground: '#FFFFFF'
      },
      flowchart: {
        htmlLabels: true,
        curve: 'basis',
        rankSpacing: 60,
        nodeSpacing: 40,
        padding: 20
      },
      securityLevel: 'loose'
    });
    
    this.initialized = true;
  }

  loadMermaid() {
    return new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.src = 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js';
      script.onload = resolve;
      script.onerror = reject;
      document.head.appendChild(script);
    });
  }

  generateMermaidCode() {
    let mermaidCode = 'graph TD\n';
    
    // 添加样式类定义
    mermaidCode += '    %% 节点样式\n';
    
    // 节点定义
    WORKFLOW_DATA.nodes.forEach(node => {
      const style = this.getNodeStyle(node.type);
      mermaidCode += `    ${node.id}["<b>${node.icon} ${node.name}</b><br/><small>${node.type.toUpperCase()}</small>"]\n`;
    });
    
    mermaidCode += '\n    %% 连接定义\n';
    
    // 连接定义（排除条件分支，用虚线表示）
    WORKFLOW_DATA.edges.forEach(edge => {
      const branch = WORKFLOW_DATA.branches.find(b => b.node === edge.from);
      
      if (branch && edge.label) {
        // 条件分支用虚线
        mermaidCode += `    ${edge.from} -.->|"${edge.label}"| ${edge.to}\n`;
      } else {
        // 普通连接用实线
        mermaidCode += `    ${edge.from} --> ${edge.to}\n`;
      }
    });
    
    return mermaidCode;
  }

  getNodeStyle(type) {
    const styles = {
      task: 'fill:#EFF6FF,stroke:#2563EB,stroke-width:2px,rx:8',
      agent: 'fill:#ECFDF5,stroke:#10B981,stroke-width:2px,rx:8',
      condition: 'fill:#FFFBEB,stroke:#F59E0B,stroke-width:2px,rx:8'
    };
    return styles[type] || styles.task;
  }

  async render() {
    if (!this.initialized) {
      await this.init();
    }
    
    const mermaidCode = this.generateMermaidCode();
    
    // 创建渲染容器
    this.container.innerHTML = `
      <div class="flowchart-wrapper">
        <pre class="mermaid">${mermaidCode}</pre>
      </div>
    `;
    
    // 渲染 Mermaid
    try {
      await mermaid.run({
        querySelector: '.mermaid'
      });
      
      // 添加交互事件
      this.addInteractions();
    } catch (error) {
      console.error('Mermaid render error:', error);
      this.container.innerHTML = `
        <div class="flowchart-error">
          <p>流程图渲染失败</p>
          <button onclick="flowChart.render()" class="btn btn--primary">重试</button>
        </div>
      `;
    }
  }

  addInteractions() {
    const svg = this.container.querySelector('.mermaid svg');
    if (!svg) return;
    
    // 为节点添加交互
    svg.querySelectorAll('.node').forEach(node => {
      node.style.cursor = 'pointer';
      node.addEventListener('click', (e) => {
        const nodeId = node.getAttribute('id')?.replace('flowchart-', '');
        if (nodeId) {
          this.onNodeClick(nodeId);
        }
      });
      
      node.addEventListener('mouseenter', () => {
        node.style.filter = 'brightness(1.1)';
      });
      
      node.addEventListener('mouseleave', () => {
        node.style.filter = '';
      });
    });
  }

  onNodeClick(nodeId) {
    // 高亮显示
    this.highlightNode(nodeId);
    
    // 显示详情（如果存在详情面板）
    const detailPanel = document.getElementById('node-detail-panel');
    if (detailPanel) {
      this.showNodeDetail(nodeId, detailPanel);
    }
    
    // 触发自定义事件
    window.dispatchEvent(new CustomEvent('nodeSelected', { detail: { nodeId } }));
  }

  highlightNode(nodeId) {
    const svg = this.container.querySelector('.mermaid svg');
    if (!svg) return;
    
    // 移除所有高亮
    svg.querySelectorAll('.node').forEach(node => {
      node.style.opacity = '0.3';
      node.style.filter = '';
    });
    
    // 高亮选中节点
    const selectedNode = svg.querySelector(`[id="flowchart-${nodeId}"]`);
    if (selectedNode) {
      selectedNode.style.opacity = '1';
      selectedNode.style.filter = 'drop-shadow(0 0 8px rgba(37, 99, 235, 0.5))';
      
      // 滚动到视口
      selectedNode.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
    
    // 高亮相关连接
    svg.querySelectorAll('.edge').forEach(edge => {
      const edgeNode = edge.parentElement;
      const edgePath = edge.querySelector('path');
      if (edgePath) {
        const markers = edgePath.getAttribute('marker-end');
        if (markers) {
          const relatedNodeId = edge.getAttribute('id')?.split('-').pop();
          if (relatedNodeId === nodeId) {
            edgePath.style.stroke = '#2563EB';
            edgePath.style.strokeWidth = '3';
          }
        }
      }
    });
  }

  resetHighlight() {
    const svg = this.container.querySelector('.mermaid svg');
    if (!svg) return;
    
    svg.querySelectorAll('.node').forEach(node => {
      node.style.opacity = '1';
      node.style.filter = '';
    });
    
    svg.querySelectorAll('path').forEach(path => {
      path.style.strokeWidth = '';
      path.style.stroke = '';
    });
  }

  showNodeDetail(nodeId, panel) {
    const node = WORKFLOW_DATA.nodes.find(n => n.id === nodeId);
    if (!node) return;
    
    panel.innerHTML = `
      <div class="detail-header">
        <span class="detail-icon">${node.icon}</span>
        <div class="detail-title">
          <h3>${node.name}</h3>
          <code>${node.id}</code>
        </div>
        <span class="detail-type detail-type--${node.type}">${node.type}</span>
      </div>
      <div class="detail-body">
        <p class="detail-description">${node.description}</p>
        
        <div class="detail-section">
          <h4>输入字段</h4>
          <div class="detail-tags">
            ${node.inputs.map(inp => `<span class="tag tag--input">${inp}</span>`).join('')}
          </div>
        </div>
        
        <div class="detail-section">
          <h4>输出字段</h4>
          <div class="detail-tags">
            ${node.outputs.map(out => `<span class="tag tag--output">${out}</span>`).join('')}
          </div>
        </div>
        
        ${node.config ? `
          <div class="detail-section">
            <h4>配置文件</h4>
            <code class="detail-config">${node.config}</code>
          </div>
        ` : ''}
        
        ${node.integrations.length > 0 ? `
          <div class="detail-section">
            <h4>集成技能</h4>
            <div class="detail-tags">
              ${node.integrations.map(int => `<span class="tag tag--integration">${int}</span>`).join('')}
            </div>
          </div>
        ` : ''}
      </div>
      <div class="detail-footer">
        <a href="#" class="btn btn--secondary btn--sm">查看代码</a>
      </div>
    `;
    
    panel.classList.add('active');
  }
}

// 创建全局实例
let flowChart = null;

document.addEventListener('DOMContentLoaded', () => {
  // 延迟初始化，确保 DOM 完全加载
  setTimeout(() => {
    flowChart = new FlowChartRenderer('flowchart-container');
  }, 100);
});
