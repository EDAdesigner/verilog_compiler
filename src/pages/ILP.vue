<template>
  <div class="code-optimization-container">
    <!-- 顶部标题和按钮 -->
    <div class="header">
      <h1 class="title">ILP调度分析</h1>
      <button class="generate-btn" @click="runILP" :disabled="isSolving">
        {{ isSolving ? "求解中..." : "开始求解" }}
      </button>
    </div>

    <!-- 主要内容区 -->
    <div class="main-content">
      <!-- 左侧LP输入区 -->
      <div class="code-input-section">
        <div class="section-header">
          <h2>LP模型输入</h2>
          <div class="toolbar">
            <button class="tool-btn" @click="clearCode">清空</button>
            <button class="tool-btn" @click="loadExample">示例</button>
          </div>
        </div>
        <textarea
          v-model="lpCode"
          class="code-editor"
          placeholder="请输入ILP模型（如schedule.lp内容）..."
          spellcheck="false"
        ></textarea>
      </div>

      <!-- 右侧调度结果展示区 -->
      <div class="code-output-section">
        <div class="section-header">
          <h2>调度结果</h2>
        </div>
        <pre class="optimized-code">{{
          ilpResult || statusMessage || "调度结果将显示在这里"
        }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

// 响应式数据
const lpCode = ref("");
const ilpResult = ref("");
const isSolving = ref(false);
const statusMessage = ref("");

// 示例LP代码
const exampleCode = `Min
XA1 + 2XA2 + 3XA3 + 4XA4 + 5XA5
Subject To
\\ 开始时间约束
Xi1 = 1
Xj1 = 1
Xl2 = 1
Xm2 = 1
Xn3 = 1
Xq4 = 1
Xh1 + Xh2 = 1
Xk2 + Xk3 = 1
Xg1 + Xg2 = 1
Xo3 + Xo4 = 1
Xp2 + Xp3 + Xp4 = 1
\\ 顺序依赖约束
2Xk2 + 3Xk3 - Xh1 - 2Xh2 >= 1
2Xk2 + 3Xk3 - Xi1 >= 1
2Xk2 + 3Xk3 - Xg1- 2Xg2 >= 1
4Xo4 + 3Xo3 - 2Xk2 - 3Xk3 >= 1 
2Xp2 + 3Xp3 + 4Xp4 - Xg1 - 2Xg2 >= 1
5XA5 - 2Xp2 - 3Xp3 - 4Xp4 >= 1
5XA5 - 3Xo3 - 4Xo4 >= 1
\\ 资源约束
Xh1 <= 2
Xj1 + Xg1 <= 1
Xi1 <= 1
Xl2 + Xm2 + Xh2 <= 2
Xk2 + Xg2 + Xp2 <= 1
Xn3 + Xo3 <= 2
Xk3 <= 1
Xp3 <= 1
Xo4 <= 2
Xq4 + Xp4 <= 2
Binary
Xi1
Xi2
Xi3
Xi4
Xi5
Xj1
Xj2
Xj3
Xj4
Xj5
Xh1
Xh2
Xh3
Xh4
Xh5
Xg1
Xg2
Xg3
Xg4
Xg5
Xk1
Xk2
Xk3
Xk4
Xk5
Xl1
Xl2
Xl3
Xl4
Xl5
Xm1
Xm2
Xm3
Xm4
Xm5
Xn1
Xn2
Xn3
Xn4
Xn5
Xo1
Xo2
Xo3
Xo4
Xo5
Xp1
Xp2
Xp3
Xp4
Xp5
Xq1
Xq2
Xq3
Xq4
Xq5
XA1
XA2
XA3
XA4
XA5
End
`;

const exampleResult = `<?xml version = "1.0" encoding="UTF-8" standalone="yes"?>
<CPLEXSolution version="1.2">
 <header
   problemName="schedule.lp"
   solutionName="incumbent"
   solutionIndex="-1"
   objectiveValue="5"
   solutionTypeValue="3"
   solutionTypeString="primal"
   solutionStatusValue="101"
   solutionStatusString="integer optimal solution"
   solutionMethodString="mip"
   primalFeasible="1"
   dualFeasible="1"
   MIPNodes="0"
   MIPIterations="0"
   writeLevel="1"/>
 <quality
   epInt="1.0000000000000001e-05"
   epRHS="9.9999999999999995e-07"
   maxIntInfeas="0"
   maxPrimalInfeas="0"
   maxX="1"
   maxSlack="1"/>
 <linearConstraints>
  <constraint name="c1" index="0" slack="0"/>
  ...
 </linearConstraints>
 <variables>
  <variable name="XA1" index="0" value="0"/>
  <variable name="XA2" index="1" value="0"/>
  ...
 </variables>
 <objectiveValues>
  <objective index="0" name="obj1" value="5"/>
 </objectiveValues>
</CPLEXSolution>
`;

const clearCode = () => {
  lpCode.value = "";
  statusMessage.value = "";
  ilpResult.value = "";
};

const loadExample = () => {
  lpCode.value = exampleCode;
  ilpResult.value = "";
  statusMessage.value = "已加载示例LP模型";
};

const runILP = () => {
  if (!lpCode.value.trim()) {
    statusMessage.value = "请输入ILP模型后再求解";
    return;
  }
  isSolving.value = true;
  statusMessage.value = "正在模拟求解...";
  ilpResult.value = "";
  // 实际应为后端请求，这里仅做前端演示
  setTimeout(() => {
    ilpResult.value = exampleResult;
    statusMessage.value = "求解完成！（演示数据）";
    isSolving.value = false;
  }, 1200);
};
</script>

<style scoped>
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

.main-content {
  display: flex;
  flex: 1;
  gap: 28px;
  height: calc(100% - 80px);
}

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

.optimized-code {
  flex: 1;
  padding: 18px;
  margin: 0;
  overflow: auto;
  font-family: "JetBrains Mono", "Fira Mono", "Consolas", monospace;
  font-size: 15px;
  line-height: 1.7;
  color: #1a2b3c;
  background: #f7faff;
  white-space: pre-wrap;
  border: none;
  border-radius: 0 0 14px 14px;
}

.status-message {
  color: #909399;
  text-align: center;
  padding: 20px;
}

select,
input[type="number"] {
  background: #f7faff;
  border: 1.5px solid #b3d4fc;
  border-radius: 8px;
  font-size: 15px;
  color: #357ae8;
  padding: 0 10px;
  height: 32px;
  outline: none;
  transition: border 0.2s;
}

select:focus,
input[type="number"]:focus {
  border-color: #4f8cff;
  background: #fff;
}
</style>