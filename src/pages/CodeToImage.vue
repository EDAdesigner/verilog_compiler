<template>
  <div class="code-to-image-container">
    <!-- 顶部标题和按钮 -->
    <div class="header">
      <h1 class="title">代码生成图片</h1>
      <button
        class="generate-btn"
        @click="generateImage"
        :disabled="isGenerating"
      >
        {{ isGenerating ? "生成中..." : "开始生成" }}
      </button>
    </div>

    <!-- 主要内容区 -->
    <div class="main-content">
      <!-- 左侧代码输入区 -->
      <div class="code-input-section">
        <div class="section-header">
          <h2>代码输入</h2>
          <div class="toolbar">
            <button class="tool-btn" @click="clearCode">清空</button>
            <button class="tool-btn" @click="loadExample">示例</button>
          </div>
        </div>
        <textarea
          v-model="codeInput"
          class="code-editor"
          placeholder="请输入您的代码..."
          spellcheck="false"
        ></textarea>
      </div>

      <!-- 右侧图片展示区 -->
      <div class="image-output-section">
        <div class="section-header">
          <h2>生成结果</h2>
          <div class="toolbar">
            <button
              class="tool-btn"
              @click="downloadImage"
              :disabled="!generatedImage"
            >
              下载
            </button>
            <button
              class="tool-btn"
              @click="copyImage"
              :disabled="!generatedImage"
            >
              复制
            </button>
          </div>
        </div>
        <div class="image-preview">
          <img
            v-if="generatedImage"
            :src="generatedImage"
            alt="生成的图片"
            class="result-image"
          />
          <div v-else class="placeholder">
            <svg class="icon" viewBox="0 0 24 24">
              <path
                d="M19 5v14H5V5h14m0-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-4.86 8.86l-3 3.87L9 13.14 6 17h12l-3.86-5.14z"
              />
            </svg>
            <p>{{ statusMessage || "生成的图片将显示在这里" }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";

// 配置
const API_BASE_URL = "http://localhost:8000";
const IMAGE_BASE_URL = `${API_BASE_URL}/output`;

// 响应式数据
const codeInput = ref("");
const generatedImage = ref("");
const isGenerating = ref(false);
const statusMessage = ref("");

// 示例代码
const exampleCode = `module unbalanced_add4(a, b, c, d, out);
    input a, b, c, d;
    output out;
    assign out = (((a + b) + c) + d);
endmodule
`;

// 生成图片
const generateImage = async () => {
  if (!codeInput.value.trim()) {
    statusMessage.value = "请输入代码后再生成";
    return;
  }

  isGenerating.value = true;
  statusMessage.value = "正在生成图片...";
  generatedImage.value = "";

  try {
    const formData = new FormData();
    // 去除所有换行符
    const codeWithoutNewlines = codeInput.value.trim().replace(/[\r\n]+/g, " ");
    formData.append("verilog_code", codeWithoutNewlines);
    formData.append("language", "verilog");
    formData.append("format", "png");
    formData.append("style", "monokai");
    formData.append("scale", "1.2");

    console.log("处理后的代码:", codeWithoutNewlines);

    const response = await axios.post(`${API_BASE_URL}/verilog`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
      timeout: 15000,
    });

    console.log("API原始响应:", response.data); // 调试日志

    // 处理图片路径（兼容多种后端返回格式）
    if (response.data?.png_file) {
      let finalUrl = "";
      const rawPath = response.data.png_file;

      // 情况1：已经是完整URL
      if (rawPath.startsWith("http")) {
        finalUrl = rawPath;
      }
      // 情况2：Windows绝对路径
      else if (rawPath.match(/^[a-zA-Z]:[\\\/]/)) {
        const fileName = rawPath.split(/[\\\/]/).pop();
        finalUrl = `${IMAGE_BASE_URL}/${fileName}`;
      }
      // 情况3：Linux绝对路径或相对路径
      else {
        const cleanPath = rawPath.replace(/^.*output[\\\/]/, "");
        finalUrl = `${IMAGE_BASE_URL}/${cleanPath.replace(/\\/g, "/")}`;
      }

      generatedImage.value = finalUrl;
      statusMessage.value = "图片生成成功";

      console.log("生成的图片URL:", generatedImage.value);
      verifyImageUrl(generatedImage.value); // 立即验证URL有效性
    } else if (response.data?.image_url) {
      generatedImage.value = response.data.image_url;
      statusMessage.value = "图片生成成功";
    } else if (response.data?.image_data) {
      generatedImage.value = `data:image/png;base64,${response.data.image_data}`;
      statusMessage.value = "图片生成成功";
    } else {
      throw new Error("API返回格式不符合预期，缺少图片数据字段");
    }
  } catch (error) {
    handleError(error);
  } finally {
    isGenerating.value = false;
  }
};

// 验证图片URL是否可访问
const verifyImageUrl = async (url) => {
  try {
    const response = await fetch(url, { method: "HEAD" });
    if (!response.ok) {
      throw new Error(`HTTP状态: ${response.status}`);
    }
    console.log("图片URL验证成功");
  } catch (err) {
    console.error("图片URL验证失败:", err);
    statusMessage.value = `警告: 生成的图片URL可能无效 (${err.message})`;
    // 不清除generatedImage，让用户仍可尝试访问
  }
};

// 错误处理
const handleError = (error) => {
  console.error("请求失败详情:", {
    error: error.message,
    config: error.config,
    response: error.response?.data,
  });

  if (error.response) {
    // 处理422验证错误
    if (error.response.status === 422) {
      const details = error.response.data.detail || [];
      statusMessage.value = details
        .map((d) => `${d.loc?.join(".")}: ${d.msg}`)
        .join("\n");
    } else {
      statusMessage.value = `服务器错误 ${error.response.status}: ${
        error.response.data?.message || "无详细错误信息"
      }`;
    }
  } else if (error.code === "ECONNABORTED") {
    statusMessage.value = "请求超时，请稍后重试";
  } else {
    statusMessage.value = `请求失败: ${error.message || "未知错误"}`;
  }
};

// 清空代码
const clearCode = () => {
  codeInput.value = "";
  generatedImage.value = "";
  statusMessage.value = "";
};

// 加载示例代码
const loadExample = () => {
  codeInput.value = exampleCode;
  statusMessage.value = "已加载示例代码";
};

// 下载图片
const downloadImage = async () => {
  if (!generatedImage.value) return;

  try {
    // 处理Base64数据
    if (generatedImage.value.startsWith("data:")) {
      const link = document.createElement("a");
      link.href = generatedImage.value;
      link.download = `verilog-${Date.now()}.png`;
      link.click();
      statusMessage.value = "下载已开始";
      return;
    }

    // 处理远程URL
    const response = await fetch(generatedImage.value);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);

    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `verilog-${new Date().toISOString().slice(0, 10)}.png`;
    document.body.appendChild(link);
    link.click();
    setTimeout(() => {
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    }, 100);

    statusMessage.value = "下载已开始";
  } catch (err) {
    console.error("下载失败:", err);
    statusMessage.value = `下载失败: ${err.message}`;
  }
};

// 复制图片
const copyImage = async () => {
  if (!generatedImage.value) return;

  try {
    // 检查剪贴板API支持
    if (!navigator.clipboard?.write) {
      throw new Error("浏览器不支持图片复制");
    }

    let blob;
    // 处理Base64数据
    if (generatedImage.value.startsWith("data:")) {
      const res = await fetch(generatedImage.value);
      blob = await res.blob();
    }
    // 处理远程URL
    else {
      const response = await fetch(generatedImage.value);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      blob = await response.blob();
    }

    await navigator.clipboard.write([new ClipboardItem({ [blob.type]: blob })]);

    statusMessage.value = "图片已复制到剪贴板";
  } catch (err) {
    console.error("复制失败:", err);
    statusMessage.value = `复制失败: ${err.message}`;

    // 提供备用方案提示
    if (!err.message.includes("不支持")) {
      statusMessage.value += " (请使用右键菜单保存图片)";
    }
  }
};

// 图片加载错误处理
const handleImageError = () => {
  statusMessage.value = `图片加载失败！请检查:
  • 直接访问URL: ${generatedImage.value}
  • 后端服务是否正常运行
  • 控制台查看详细错误`;

  console.error("图片加载失败，当前URL:", generatedImage.value);
};
</script>

<style scoped>
.code-to-image-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #e3f0ff 0%, #f8fbff 100%);
  padding: 24px;
}

/* 顶部标题和按钮样式 */
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
.image-output-section {
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

/* 图片预览区样式 */
.image-preview {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f7faff;
}

.placeholder {
  text-align: center;
  color: #909399;
}

.placeholder .icon {
  width: 60px;
  height: 60px;
  fill: #b3d4fc;
  margin-bottom: 10px;
}

.placeholder p {
  margin: 0;
  font-size: 15px;
}

.result-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(79, 140, 255, 0.1);
}
</style>