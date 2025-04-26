<template>
  <div class="code-optimization-container">
    <!-- 顶部标题和按钮 -->
    <div class="header">
      <h1 class="title">代码优化</h1>
      <button 
        class="generate-btn"
        @click="optimizeCode"
        :disabled="isOptimizing"
      >
        {{ isOptimizing ? '优化中...' : '开始优化' }}
      </button>
    </div>

    <!-- 主要内容区 -->
    <div class="main-content">
      <!-- 左侧原始代码输入区 -->
      <div class="code-input-section">
        <div class="section-header">
          <h2>原始代码</h2>
          <div class="toolbar">
            <button class="tool-btn" @click="clearCode">清空</button>
            <button class="tool-btn" @click="loadExample">示例</button>
          </div>
        </div>
        <textarea
          v-model="sourceCode"
          class="code-editor" 
          placeholder="请输入需要优化的代码..."
          spellcheck="false"
        ></textarea>
      </div>

      <!-- 右侧优化后代码展示区 -->
      <div class="code-output-section">
        <div class="section-header">
          <h2>优化结果</h2>
          <div class="toolbar">
            <button 
              class="tool-btn" 
              @click="copyOptimizedCode"
              :disabled="!optimizedCode"
            >
              复制代码
            </button>
            <button 
              class="tool-btn"
              @click="downloadCode"
              :disabled="!optimizedCode"
            >
              下载
            </button>
          </div>
        </div>
        <pre class="optimized-code">{{ optimizedCode || statusMessage || '优化后的代码将显示在这里' }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// 响应式数据
const sourceCode = ref('');
const optimizedCode = ref('');
const isOptimizing = ref(false);
const statusMessage = ref('');

// 示例代码
const exampleCode = `// 未优化代码示例
function calculateTotal(items) {
  let total = 0;
  for (let i = 0; i < items.length; i++) {
    total += items[i].price * items[i].quantity;
  }
  return total;
}`;

// 优化代码
const optimizeCode = async () => {
  if (!sourceCode.value.trim()) {
    statusMessage.value = '请输入代码后再优化';
    return;
  }

  isOptimizing.value = true;
  statusMessage.value = '正在优化代码...';
  
  try {
    // 模拟API请求延迟
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // 这里应该是实际的API调用
    // const response = await fetch('/api/optimize-code', {
    //   method: 'POST',
    //   body: JSON.stringify({ code: sourceCode.value }),
    //   headers: { 'Content-Type': 'application/json' }
    // });
    // const data = await response.json();
    
    // 模拟返回的优化后代码
    optimizedCode.value = `// 优化后代码
const calculateTotal = items => 
  items.reduce((total, item) => 
    total + item.price * item.quantity, 0);`;
    
    statusMessage.value = '代码优化成功！';
  } catch (error) {
    console.error('优化失败:', error);
    statusMessage.value = '代码优化失败，请重试';
    optimizedCode.value = '';
  } finally {
    isOptimizing.value = false;
  }
};

// 清空代码
const clearCode = () => {
  sourceCode.value = '';
  statusMessage.value = '';
  optimizedCode.value = '';
};

// 加载示例代码
const loadExample = () => {
  sourceCode.value = exampleCode;
  statusMessage.value = '已加载示例代码';
};

// 复制优化后的代码
const copyOptimizedCode = async () => {
  if (!optimizedCode.value) return;
  
  try {
    await navigator.clipboard.writeText(optimizedCode.value);
    statusMessage.value = '代码已复制到剪贴板';
  } catch (err) {
    console.error('复制失败:', err);
    statusMessage.value = '复制失败，请手动选择复制';
  }
};

// 下载代码
const downloadCode = () => {
  if (!optimizedCode.value) return;
  
  const blob = new Blob([optimizedCode.value], { type: 'text/plain' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = 'optimized-code.js';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};
</script>

<style scoped>
/* 共用样式 */
.code-optimization-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f5f7fa;
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #e4e7ed;
}

.title {
  font-size: 24px;
  color: #303133;
  margin: 0;
}

.generate-btn {
  background-color: #409eff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.generate-btn:hover {
  background-color: #66b1ff;
}

.generate-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.generate-btn:disabled:hover {
  background-color: #409eff;
}

/* 主要内容区样式 */
.main-content {
  display: flex;
  flex: 1;
  gap: 20px;
  height: calc(100% - 70px);
}

/* 两侧区域共用样式 */
.code-input-section,
.code-output-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
  border-bottom: 1px solid #ebeef5;
}

.section-header h2 {
  font-size: 16px;
  color: #606266;
  margin: 0;
}

.toolbar {
  display: flex;
  gap: 10px;
}

.tool-btn {
  background-color: #f5f7fa;
  color: #606266;
  border: 1px solid #dcdfe6;
  padding: 5px 12px;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.3s;
}

.tool-btn:hover {
  color: #409eff;
  border-color: #c6e2ff;
  background-color: #ecf5ff;
}

.tool-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 代码编辑器样式 */
.code-editor {
  flex: 1;
  padding: 15px;
  border: none;
  resize: none;
  font-family: 'Courier New', Courier, monospace;
  font-size: 14px;
  line-height: 1.5;
  color: #333;
  background-color: #f8f8f8;
}

.code-editor:focus {
  outline: none;
  background-color: #fff;
}

/* 优化后代码展示区 */
.optimized-code {
  flex: 1;
  padding: 15px;
  margin: 0;
  overflow: auto;
  font-family: 'Courier New', Courier, monospace;
  font-size: 14px;
  line-height: 1.5;
  color: #333;
  background-color: #f8f8f8;
  white-space: pre-wrap;
  border: none;
}

/* 状态消息样式 */
.status-message {
  color: #909399;
  text-align: center;
  padding: 20px;
}
</style>