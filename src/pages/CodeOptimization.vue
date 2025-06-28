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
        {{ isOptimizing ? "优化中..." : "开始优化" }}
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
            <button
              class="tool-btn"
              :disabled="!optimizedCode"
            >
              跳转至编辑器
            </button>
          </div>
        </div>
        <pre class="optimized-code">{{
          optimizedCode || statusMessage || "优化后的代码将显示在这里"
        }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";

// 配置
const API_BASE_URL = "/api";

// 响应式数据
const sourceCode = ref("");
const optimizedCode = ref("");
const isOptimizing = ref(false);
const statusMessage = ref("");

// 示例代码
const exampleCode = `module unbalanced_add4(a, b, c, d, out);
    input a, b, c, d;
    output out;
    assign out = (((a + b) + c) + d);
endmodule
`;

// 优化代码（请求同代码转图片，只是取 .dot 字段内容）
const optimizeCode = async () => {
  if (!sourceCode.value.trim()) {
    statusMessage.value = "请输入代码后再优化";
    return;
  }

  isOptimizing.value = true;
  statusMessage.value = "正在优化代码...";
  optimizedCode.value = "";

  try {
    const formData = new FormData();
    // 去除所有换行符
    const codeWithoutNewlines = sourceCode.value
      .trim()
      .replace(/[\r\n]+/g, " ");
    formData.append("verilog_code", codeWithoutNewlines);

    console.log("处理后的代码:", codeWithoutNewlines);

    // 这里改为代理路径
    const response = await axios.post(`${API_BASE_URL}/verilog`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
      timeout: 15000,
    });

    console.log("API原始响应:", response.data); // 调试日志

    // 处理 .dot 文件路径（兼容多种后端返回格式）
    let dotPath = response.data?.dot_file;
    // 兼容 files 字段
    if (!dotPath && response.data?.files?.dot_file) {
      dotPath = response.data.files.dot_file;
    }

    if (dotPath) {
      let dotUrl = "";
      if (dotPath.startsWith("http")) {
        dotUrl = dotPath;
      } else {
        const fileName = dotPath.split(/[\\\/]/).pop();
        dotUrl = `http://localhost:8000/output/${fileName}`;
      }
      // 获取 dot 文件内容
      const dotRes = await axios.get(dotUrl);
      optimizedCode.value = dotRes.data;
      statusMessage.value = "代码优化成功！";
    } else if (response.data?.dot_content) {
      optimizedCode.value = response.data.dot_content;
      statusMessage.value = "代码优化成功！";
    } else if (typeof response.data === "string") {
      optimizedCode.value = response.data;
      statusMessage.value = "代码优化成功！";
    } else {
      throw new Error("API返回格式不符合预期，缺少dot内容字段");
    }
  } catch (error) {
    console.error("优化失败:", error);
    statusMessage.value = `代码优化失败: ${error.message || "未知错误"}
${error.stack || ""}
${JSON.stringify(error, null, 2)}`;
    if (error.config) {
      statusMessage.value += `\n\n请求配置:\n${JSON.stringify(
        error.config,
        null,
        2
      )}`;
    }
    if (error.response) {
      statusMessage.value += `\n\n响应内容:\n${JSON.stringify(
        error.response,
        null,
        2
      )}`;
    }
    optimizedCode.value = "";
  } finally {
    isOptimizing.value = false;
  }
};

// 清空代码
const clearCode = () => {
  sourceCode.value = "";
  statusMessage.value = "";
  optimizedCode.value = "";
};

// 加载示例代码
const loadExample = () => {
  sourceCode.value = exampleCode;
  statusMessage.value = "已加载示例代码";
};

// 复制优化后的代码
const copyOptimizedCode = async () => {
  if (!optimizedCode.value) return;

  try {
    await navigator.clipboard.writeText(optimizedCode.value);
    statusMessage.value = "代码已复制到剪贴板";
  } catch (err) {
    console.error("复制失败:", err);
    statusMessage.value = "复制失败，请手动选择复制";
  }
};

// 下载为 .dot 文件
const downloadCode = () => {
  if (!optimizedCode.value) return;

  const blob = new Blob([optimizedCode.value], { type: "text/plain" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "optimized-code.dot";
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
  background: linear-gradient(135deg, #e3f0ff 0%, #f8fbff 100%);
  padding: 24px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1.5px solid #e0e6ed;
  background: transparent;
}

.title {
  font-size: 26px;
  color: #2d3a4b;
  margin: 0;
  letter-spacing: 1px;
  font-weight: 700;
}

.generate-btn {
  background: linear-gradient(90deg, #4f8cff 0%, #6fc3ff 100%);
  color: #fff;
  border: none;
  padding: 10px 28px;
  border-radius: 22px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  box-shadow: 0 2px 8px 0 rgba(79, 140, 255, 0.08);
  transition: all 0.2s;
}

.generate-btn:hover:not(:disabled) {
  background: linear-gradient(90deg, #357ae8 0%, #4f8cff 100%);
  box-shadow: 0 4px 16px 0 rgba(79, 140, 255, 0.15);
}

.generate-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 主要内容区样式 */
.main-content {
  display: flex;
  flex: 1;
  gap: 28px;
  height: calc(100% - 80px);
}

/* 两侧区域共用样式 */
.code-input-section,
.code-output-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 4px 24px 0 rgba(79, 140, 255, 0.07);
  overflow: hidden;
  border: 1.5px solid #e3eaf2;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 28px;
  border-bottom: 1.5px solid #e0e6ed;
  background: #f7faff;
}

.section-header h2 {
  font-size: 17px;
  color: #357ae8;
  margin: 0;
  font-weight: 600;
}

.toolbar {
  display: flex;
  gap: 12px;
}

.tool-btn {
  background: #f0f6ff;
  color: #357ae8;
  border: 1px solid #b3d4fc;
  padding: 6px 18px;
  border-radius: 18px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.tool-btn:hover {
  background: #e3f0ff;
  color: #1a5fd0;
  border-color: #7bb6fa;
}

.tool-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 代码编辑器样式 */
.code-editor {
  flex: 1;
  padding: 18px;
  border: none;
  resize: none;
  font-family: "JetBrains Mono", "Fira Mono", "Consolas", monospace;
  font-size: 16px;
  line-height: 1.7;
  color: #222e3a;
  background: #f7faff;
  border-radius: 0 0 14px 14px;
  transition: background 0.2s;
}

.code-editor:focus {
  outline: 2px solid #4f8cff;
  background: #fff;
}

/* 优化后代码展示区 */
.optimized-code {
  flex: 1;
  padding: 18px;
  margin: 0;
  overflow: auto;
  font-family: "JetBrains Mono", "Fira Mono", "Consolas", monospace;
  font-size: 16px;
  line-height: 1.7;
  color: #1a2b3c;
  background: #f7faff;
  white-space: pre-wrap;
  border: none;
  border-radius: 0 0 14px 14px;
}

/* 状态消息样式 */
.status-message {
  color: #909399;
  text-align: center;
  padding: 20px;
}
</style>