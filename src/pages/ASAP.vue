<template>
  <div class="code-optimization-container">
    <!-- 顶部标题和按钮 -->
    <div class="header">
      <h1 class="title">ASAP/ALAP调度分析</h1>
      <div style="display: flex; align-items: center; gap: 16px">
        <select
          v-model="scheduleType"
          style="
            height: 32px;
            border-radius: 4px;
            border: 1px solid #dcdfe6;
            padding: 0 8px;
          "
        >
          <option value="ASAP">ASAP调度</option>
          <option value="ALAP">ALAP调度</option>
        </select>
        <input
          v-if="scheduleType === 'ALAP'"
          v-model.number="deadline"
          type="number"
          min="1"
          style="
            width: 80px;
            height: 32px;
            margin-left: 8px;
            border-radius: 4px;
            border: 1px solid #dcdfe6;
            padding: 0 8px;
          "
          placeholder="调度周期数"
        />
        <button
          class="generate-btn"
          @click="runSchedule"
          :disabled="isOptimizing"
        >
          {{ isOptimizing ? "调度中..." : "开始调度" }}
        </button>
      </div>
    </div>

    <!-- 主要内容区 -->
    <div class="main-content">
      <!-- 左侧BLIF输入区 -->
      <div class="code-input-section">
        <div class="section-header">
          <h2>BLIF代码输入</h2>
          <div class="toolbar">
            <button class="tool-btn" @click="clearCode">清空</button>
            <button class="tool-btn" @click="loadExample">示例</button>
          </div>
        </div>
        <textarea
          v-model="sourceCode"
          class="code-editor"
          placeholder="请输入BLIF格式代码..."
          spellcheck="false"
        ></textarea>
      </div>

      <!-- 右侧调度结果展示区 -->
      <div class="code-output-section">
        <div class="section-header">
          <h2>调度结果</h2>
        </div>
        <pre class="optimized-code">{{
          scheduleResult || statusMessage || "调度结果将显示在这里"
        }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

// 响应式数据
const sourceCode = ref("");
const scheduleResult = ref("");
const isOptimizing = ref(false);
const statusMessage = ref("");
const deadline = ref(5);
const scheduleType = ref("ASAP");

const exampleCode = `.model test
.inputs a b c
.outputs y
.names a b n1
11 1
.names n1 c y
1- 1
-1 1
`;

const clearCode = () => {
  sourceCode.value = "";
  statusMessage.value = "";
  scheduleResult.value = "";
};

const loadExample = () => {
  sourceCode.value = exampleCode;
  statusMessage.value = "已加载示例BLIF代码";
};

const runSchedule = async () => {
  if (!sourceCode.value.trim()) {
    statusMessage.value = "请输入BLIF代码后再调度";
    return;
  }
  isOptimizing.value = true;
  statusMessage.value = "正在调度...";
  scheduleResult.value = "";
  try {
    await new Promise((resolve) => setTimeout(resolve, 500));
    const blifData = readBlifString(sourceCode.value);
    const networkData = processGateNetwork(blifData);
    if (!networkData) {
      scheduleResult.value = "数据处理失败";
      return;
    }
    let resultStr = "";
    if (scheduleType.value === "ASAP") {
      const asapResult = ASAP(networkData);
      resultStr += printScheduleResult(networkData, asapResult, "ASAP");
    } else {
      const alapResult = ALAP(networkData, deadline.value);
      resultStr += printScheduleResult(networkData, alapResult, "ALAP");
    }
    scheduleResult.value = resultStr;
    statusMessage.value = "调度完成！";
  } catch (e) {
    scheduleResult.value = "调度出错：" + e.message;
  } finally {
    isOptimizing.value = false;
  }
};

// 解析BLIF字符串
function readBlifString(content) {
  const lines = content.split("\n").map((line) => line.trim());
  const blifData = { model: "", inputs: [], outputs: [], names: [] };
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (line === "" || line.startsWith("#")) continue;
    if (line.startsWith(".model")) blifData.model = line.split(" ")[1];
    else if (line.startsWith(".inputs"))
      blifData.inputs = line.substring(7).trim().split(" ").filter(Boolean);
    else if (line.startsWith(".outputs"))
      blifData.outputs = line.substring(8).trim().split(" ").filter(Boolean);
    else if (line.startsWith(".names")) {
      const variables = line.substring(6).trim().split(" ");
      const nameData = {
        inputs: variables.slice(0, -1),
        output: variables[variables.length - 1],
        truth_table: "",
        gate_type: "",
      };
      i++;
      let expressions = [];
      let truthRows = [];
      while (i < lines.length && !lines[i].startsWith(".")) {
        if (lines[i] !== "") {
          const row = lines[i].trim().split(" ")[0];
          truthRows.push(row);
          let termExpr = [];
          for (let j = 0; j < row.length; j++) {
            if (row[j] === "1") termExpr.push(nameData.inputs[j]);
            else if (row[j] === "0") termExpr.push(`!${nameData.inputs[j]}`);
          }
          if (termExpr.length > 0) expressions.push(termExpr.join(" and "));
        }
        i++;
      }
      i--;
      if (nameData.inputs.length === 1) {
        if (truthRows.length === 1 && truthRows[0] === "0")
          nameData.gate_type = "not";
      } else {
        if (
          truthRows.length === 1 &&
          truthRows[0].indexOf("0") === -1 &&
          truthRows[0].indexOf("-") === -1
        )
          nameData.gate_type = "and";
        else if (truthRows.every((row) => row.indexOf("0") === -1))
          nameData.gate_type = "or";
        else nameData.gate_type = "complex";
      }
      nameData.truth_table = expressions.join(" or ");
      blifData.names.push(nameData);
    }
  }
  return blifData;
}

// 处理门电路网络
function processGateNetwork(blifData) {
  if (!blifData) return null;
  const inputs = blifData.inputs;
  const outputs = blifData.outputs;
  const gates = blifData.names.map((nameData) => ({
    inputs: nameData.inputs,
    output: nameData.output,
    gate_type: nameData.gate_type,
  }));
  const intermediates = gates
    .map((gate) => gate.output)
    .filter((output) => !outputs.includes(output));
  return { inputs, outputs, intermediates, gates };
}

// ASAP调度
function ASAP(data) {
  if (!data) return null;
  const schedule = {};
  [...data.inputs, ...data.intermediates, ...data.outputs].forEach((node) => {
    schedule[node] = -1;
  });
  data.inputs.forEach((input) => {
    schedule[input] = 0;
  });
  const areInputsScheduled = (gate) => {
    return gate.inputs.every((input) => schedule[input] !== -1);
  };
  let changed;
  do {
    changed = false;
    data.gates.forEach((gate) => {
      if (schedule[gate.output] === -1 && areInputsScheduled(gate)) {
        const maxInputLevel = Math.max(
          ...gate.inputs.map((input) => schedule[input])
        );
        schedule[gate.output] = maxInputLevel + 1;
        changed = true;
      }
    });
  } while (changed);
  const maxLevel = Math.max(...Object.values(schedule));
  const levels = Array.from({ length: maxLevel + 1 }, () => []);
  Object.entries(schedule).forEach(([node, level]) => {
    if (level >= 0) {
      levels[level].push(node);
    }
  });
  return { schedule, levels, maxLevel };
}

// ALAP调度
function ALAP(data, deadline) {
  if (!data) return null;
  const schedule = {};
  [...data.inputs, ...data.intermediates, ...data.outputs].forEach((node) => {
    schedule[node] = -1;
  });
  data.inputs.forEach((input) => {
    schedule[input] = 0;
  });
  data.outputs.forEach((output) => {
    schedule[output] = deadline;
  });
  for (const output of data.outputs) {
    const outputGate = data.gates.find((g) => g.output === output);
    if (outputGate) {
      const minRequiredLevel = getMinRequiredLevel(outputGate, data.gates);
      if (minRequiredLevel > deadline) {
        return null;
      }
    }
  }
  const areOutputsScheduled = (gate, gates) => {
    const dependentGates = gates.filter((g) => g.inputs.includes(gate.output));
    if (dependentGates.length === 0) {
      return schedule[gate.output] !== -1;
    }
    return dependentGates.every((g) => schedule[g.output] !== -1);
  };
  let changed;
  do {
    changed = false;
    [...data.gates].reverse().forEach((gate) => {
      if (
        schedule[gate.output] === -1 &&
        areOutputsScheduled(gate, data.gates)
      ) {
        const dependentGates = data.gates.filter((g) =>
          g.inputs.includes(gate.output)
        );
        if (dependentGates.length === 0 && schedule[gate.output] === -1) {
          schedule[gate.output] = deadline;
        } else {
          const minDependentTime = Math.min(
            ...dependentGates.map((g) => schedule[g.output])
          );
          schedule[gate.output] = minDependentTime - 1;
        }
        changed = true;
      }
    });
  } while (changed);
  const levels = Array.from({ length: deadline + 1 }, () => []);
  Object.entries(schedule).forEach(([node, level]) => {
    if (level >= 0 && level <= deadline) {
      levels[level].push(node);
    }
  });
  return { schedule, levels, maxLevel: deadline };
}

function getMinRequiredLevel(gate, gates) {
  const memo = new Map();
  function dfs(currentGate) {
    if (memo.has(currentGate.output)) {
      return memo.get(currentGate.output);
    }
    let maxInputLevel = 0;
    for (const input of currentGate.inputs) {
      const inputGate = gates.find((g) => g.output === input);
      if (inputGate) {
        maxInputLevel = Math.max(maxInputLevel, dfs(inputGate));
      }
    }
    const result = maxInputLevel + 1;
    memo.set(currentGate.output, result);
    return result;
  }
  return dfs(gate);
}

// 输出调度结果
function printScheduleResult(data, scheduleResult, scheduleType) {
  if (!scheduleResult) return `${scheduleType}调度失败或无结果\n`;
  let out = "";
  out += `${scheduleType}调度结果：\n`;
  out += `Input :${data.inputs.join(", ")}  Output :${data.outputs.join(
    ", "
  )}\n`;
  out += `Total ${scheduleResult.maxLevel} Cycles\n`;
  scheduleResult.levels.forEach((nodes, level) => {
    if (level === 0) return;
    const andGates = [];
    const orGates = [];
    const notGates = [];
    nodes.forEach((node) => {
      const gate = data.gates.find((g) => g.output === node);
      if (gate) {
        switch (gate.gate_type) {
          case "and":
            andGates.push(node);
            break;
          case "or":
            orGates.push(node);
            break;
          case "not":
            notGates.push(node);
            break;
        }
      }
    });
    if (andGates.length > 0 || orGates.length > 0 || notGates.length > 0) {
      const andStr = `{${andGates.join(",")}}`;
      const orStr = `{${orGates.join(",")}}`;
      const notStr = `{${notGates.join(",")}}`;
      out += `Cycle ${level}: ${andStr},${orStr},${notStr}\n`;
    }
  });
  return out;
}
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

/* 下拉框和输入框样式 */
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