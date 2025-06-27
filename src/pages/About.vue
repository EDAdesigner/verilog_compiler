<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from "vue";
import LogicFlow, {
  RectNode,
  RectNodeModel,
  CircleNode,
  CircleNodeModel,
  h,
} from "@logicflow/core";
import "@logicflow/core/dist/index.css";

const container = ref(null);
const fileInputRef = ref(null);
let lf = null;
let nodeIdCounter = 1;
let selectedElementId = null;

// ---------------- RecordNode（无JSX写法） ----------------
class RecordNodeModel extends RectNodeModel {
  initNodeData(data) {
    super.initNodeData(data);
    this.width = 140;
    this.height = 100;
  }
}

class RecordNode extends RectNode {
  getShape() {
    const { x, y, width, height, properties } = this.props.model;
    const style = this.props.model.getNodeStyle();
    const textStyle = this.props.model.getTextStyle();
    const partHeight = height / 4;

    const texts = [
      properties.part1 || "",
      properties.part2 || "",
      properties.part3 || "",
      properties.part4 || "",
    ];

    const children = [];

    // 主矩形交互区域
    children.push(
      h("rect", {
        class: "lf-node-rect",
        x: x - width / 2,
        y: y - height / 2,
        width,
        height,
        rx: 8,
        ...style,
      })
    );

    // 四段文字
    texts.forEach((text, i) => {
      children.push(
        h(
          "text",
          {
            x,
            y: y - height / 2 + partHeight * (i + 0.5),
            textAnchor: "middle",
            alignmentBaseline: "middle",
            fontSize: textStyle.fontSize || 12,
            fill: textStyle.color || "#333",
          },
          text
        )
      );
    });

    return h("g", {}, children);
  }
}

// ---------------- 其他节点定义 ----------------
class NormalNodeModel extends RectNodeModel {
  initNodeData(data) {
    super.initNodeData(data);
    this.width = 100;
    this.height = 60;
    this.anchorsOffset = [
      [-this.width / 2, -15],
      [-this.width / 2, 15],
      [this.width / 2, 0],
    ];
  }
  getNodeStyle() {
    return { ...super.getNodeStyle(), fill: "#4CAF50", stroke: "#388E3C" };
  }
  getAnchorPoints() {
    return this.anchorsOffset;
  }
}
class NormalNode extends RectNode {}

class InputNodeModel extends CircleNodeModel {
  initNodeData(data) {
    super.initNodeData(data);
    this.radius = 30;
    this.anchorsOffset = [[50, 0]];
  }
  getNodeStyle() {
    return { ...super.getNodeStyle(), fill: "#FFEB3B", stroke: "#FBC02D" };
  }
  getAnchorPoints() {
    return this.anchorsOffset;
  }
}
class InputNode extends CircleNode {}

class OutputNodeModel extends CircleNodeModel {
  initNodeData(data) {
    super.initNodeData(data);
    this.radius = 30;
    this.anchorsOffset = [[-50, 0]];
  }
  getNodeStyle() {
    return { ...super.getNodeStyle(), fill: "#2196F3", stroke: "#1976D2" };
  }
  getAnchorPoints() {
    return this.anchorsOffset;
  }
}
class OutputNode extends CircleNode {}

// ---------------- 初始化 LogicFlow ----------------
const initLogicFlow = () => {
  lf = new LogicFlow({
    container: container.value,
    grid: true,
    width: container.value.clientWidth || 1000,
    height: container.value.clientHeight || 600,
    keyboard: true,
    nodeText: { overflowMode: "ellipsis" },
    edgeText: { fontSize: 12, color: "#666" },
    stopScrollGraph: { passive: true },
    stopZoomGraph: { passive: true },
  });

  lf.setTheme({
    anchor: {
      visibility: "visible",
      r: 6,
      fill: "#fff",
      stroke: "#FF5722",
      hover: { fill: "#FF9800", stroke: "#FF5722", r: 8 },
    },
  });

  lf.register({
    type: "record-node",
    model: RecordNodeModel,
    view: RecordNode,
  });
  lf.register({
    type: "normal-node",
    model: NormalNodeModel,
    view: NormalNode,
  });
  lf.register({ type: "input-node", model: InputNodeModel, view: InputNode });
  lf.register({
    type: "output-node",
    model: OutputNodeModel,
    view: OutputNode,
  });

  lf.on("element:click", ({ data }) => {
    if (data.type !== "edge") selectedElementId = data.id;
  });

  lf.on("selection:changed", ({ nodes }) => {
    selectedElementId = nodes?.[0]?.id || null;
  });

  lf.render();
};

// ---------------- 工具按钮功能 ----------------
const addNode = (type) => {
  const id = "node_" + nodeIdCounter++;
  const x = 100 + Math.random() * 700;
  const y = 100 + Math.random() * 400;
  lf.addNode({ id, type, x, y, text: type });
};

const deleteNode = () => {
  if (!selectedElementId) return alert("请先选中节点！");
  lf.deleteElement(selectedElementId);
  selectedElementId = null;
};

const exportJSON = () => {
  const data = lf.getGraphData();
  const blob = new Blob([JSON.stringify(data, null, 2)], {
    type: "application/json",
  });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "logicflow-data.json";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
};

const exportDOT = () => {
  const data = lf.getGraphData();
  let dot = `digraph G {\n`;
  for (const node of data.nodes) {
    const label = node.text?.value || node.type || node.id;
    dot += `  ${node.id} [label="${label}"];\n`;
  }
  for (const edge of data.edges) {
    dot += `  ${edge.sourceNodeId} -> ${edge.targetNodeId};\n`;
  }
  dot += `}`;
  const blob = new Blob([dot], { type: "text/plain" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "logicflow-data.dot";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
};

const importFile = () => fileInputRef.value?.click();

const handleFileChange = async (e) => {
  const file = e.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = async (ev) => {
    try {
      let content = ev.target.result;
      let data;

      if (file.name.endsWith(".json")) {
        data = JSON.parse(content);
      } else if (file.name.endsWith(".dot")) {
        const simplifiedDot = simplifyDot(content);
        data = parseDotWithTopology(simplifiedDot);
      }

      lf.clearData();
      await nextTick();
      lf.render(data);
    } catch (err) {
      console.error("导入失败:", err);
      alert("导入失败: " + err.message);
    }
  };
  reader.readAsText(file);
};

// ---------------- DOT 文件解析 ----------------
function simplifyDot(dotString) {
  const lines = dotString.split("\n");
  let result = [],
    inSubgraph = false;

  for (let line of lines) {
    const trimmed = line.trim();
    if (
      trimmed.startsWith("graph [") ||
      trimmed.startsWith("node [") ||
      trimmed.startsWith("edge [") ||
      trimmed === ""
    )
      continue;
    if (trimmed.startsWith("subgraph")) {
      inSubgraph = true;
      continue;
    }
    if (trimmed === "}") {
      if (inSubgraph) inSubgraph = false;
      continue;
    }
    if (inSubgraph) continue;

    const nodeMatch = trimmed.match(/^(\w+)\s*\[(.*?)\]/);
    if (nodeMatch) {
      const [_, id, attrs] = nodeMatch;
      const labelMatch = attrs.match(/label=("[^"]*"|\{[^}]*\}|[^ \]\[]+)/);
      if (labelMatch) {
        let label = labelMatch[1].replace(/^"(.*)"$/, "$1");
        result.push(`${id} [label="${label}"];`);
      }
      continue;
    }

    if (trimmed.includes("->")) {
      const edge = trimmed.replace(/:(\w+)/g, "").replace(/;?\s*$/, "");
      result.push(`${edge};`);
      continue;
    }

    if (trimmed.startsWith("digraph ")) {
      result.push(trimmed.replace(/\s*\{?\s*$/, " {"));
    }
  }

  return (
    result
      .join("\n")
      .replace(/\n{2,}/g, "\n")
      .trim() + "\n}"
  );
}

// 解析 dot 并自动识别输入输出，节点类型决定样式，中间复杂节点用normal-node，且只显示中间部分作为文本
function parseDotWithTopology(dotText) {
  const lines = dotText.split("\n");
  const nodes = [],
    edges = [],
    graph = {},
    inDegree = {},
    nodeMap = {};

  // 第一遍：解析节点
  for (const line of lines) {
    const nodeMatch = line
      .trim()
      .match(/^([a-zA-Z0-9_]+)\s*\[label="?(.*?)"?\]\s*;?$/);
    if (nodeMatch) {
      const [_, id, rawLabel] = nodeMatch;
      let cleanLabel = rawLabel.replace(/^"|"$/g, "");
      const nodeInfo = { id, label: cleanLabel };

      // 判断是否为 record 四区块形式（改进版）
      if (cleanLabel.startsWith("{{") && cleanLabel.includes("|")) {
        const parts = cleanLabel
          .replace(/^\{\{|\}\}$/g, "") // 去掉最外层大括号
          .split(/\}\|\{|\|/); // 分割区块

        const partProps = {};
        parts.forEach((p, idx) => {
          const pure = p
            .replace(/<[^>]+>/g, "")
            .replace(/[{}]/g, "")
            .trim();
          partProps[`part${idx + 1}`] = pure.replace(/\\n/g, "\n");
        });

        nodeInfo.properties = partProps;
      }

      nodeMap[id] = nodeInfo;
      graph[id] = [];
      inDegree[id] = 0;
    }
  }

  // 第二遍：处理边
  for (const line of lines) {
    const edgeMatch = line
      .trim()
      .match(/^([a-zA-Z0-9_]+)\s*->\s*([a-zA-Z0-9_]+)\s*;?$/);
    if (edgeMatch) {
      const [_, source, target] = edgeMatch;
      if (nodeMap[source] && nodeMap[target]) {
        edges.push({
          sourceNodeId: source,
          targetNodeId: target,
          type: "polyline",
        });
        graph[source].push(target);
        inDegree[target]++;
      }
    }
  }

  // 判断节点类型（输入、输出、普通）
  for (const id in nodeMap) {
    const hasIncoming = edges.some((edge) => edge.targetNodeId === id);
    const hasOutgoing = edges.some((edge) => edge.sourceNodeId === id);

    if (!hasIncoming && hasOutgoing) {
      nodeMap[id].type = "input-node";
    } else if (hasIncoming && !hasOutgoing) {
      nodeMap[id].type = "output-node";
    } else {
      // 中间节点统一用 normal-node
      nodeMap[id].type = "normal-node";
    }
  }

  // 拓扑布局分层（纵向）
  const queue = [],
    levels = [];
  for (const id in inDegree) {
    if (inDegree[id] === 0) queue.push(id);
  }

  while (queue.length) {
    const levelSize = queue.length,
      currentLevel = [];
    for (let i = 0; i < levelSize; i++) {
      const nodeId = queue.shift();
      currentLevel.push(nodeId);
      for (const neighbor of graph[nodeId]) {
        inDegree[neighbor]--;
        if (inDegree[neighbor] === 0) queue.push(neighbor);
      }
    }
    levels.push(currentLevel);
  }

  // 布局位置计算
  const xStep = 200,
    yStep = 120;
  const nodePositions = {};
  levels.forEach((level, levelIndex) => {
    const x = 100 + levelIndex * xStep;
    level.forEach((nodeId, i) => {
      const y = 100 + i * yStep;
      nodePositions[nodeId] = { x, y };
    });
  });

  // 生成最终节点数组
  const finalNodes = Object.values(nodeMap).map((node) => {
    let displayText = node.label;

    // 如果是复杂节点（有 properties），取中间部分 part3 作为显示文本
    if (node.properties && node.properties.part3) {
      displayText = node.properties.part3.trim();
    }

    return {
      id: node.id,
      type: node.type,
      text: displayText,
      properties: node.properties,
      x: nodePositions[node.id].x,
      y: nodePositions[node.id].y,
    };
  });

  return { nodes: finalNodes, edges };
}

onMounted(() => nextTick(initLogicFlow));
onBeforeUnmount(() => lf?.destroy());
</script>






<template>
  <div class="container">
    <div class="toolbar">
      <button @click="addNode('input-node')">添加输入节点</button>
      <button @click="addNode('output-node')">添加输出节点</button>
      <button @click="addNode('normal-node')">添加操作节点</button>
      <button @click="deleteNode">删除选中节点</button>
      <button @click="exportJSON">导出JSON</button>
      <button @click="exportDOT">导出DOT</button>
      <button @click="importFile">导入文件（.json/.dot）</button>
      <input
        ref="fileInputRef"
        type="file"
        accept=".json,.dot"
        style="display: none"
        @change="handleFileChange"
      />
    </div>
    <div ref="container" class="graph-container"></div>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: linear-gradient(135deg, #e3f0ff 0%, #f8fbff 100%);
  padding: 24px;
}
.toolbar {
  padding: 14px 18px;
  background: #f7faff;
  border-bottom: 1.5px solid #e0e6ed;
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
  border-radius: 12px 12px 0 0;
  box-shadow: 0 2px 8px 0 rgba(79, 140, 255, 0.04);
}
.toolbar button {
  padding: 8px 22px;
  background: linear-gradient(90deg, #4f8cff 0%, #6fc3ff 100%);
  color: #fff;
  border: none;
  border-radius: 18px;
  font-weight: 500;
  font-size: 15px;
  cursor: pointer;
  transition: all 0.18s;
  box-shadow: 0 2px 8px 0 rgba(79, 140, 255, 0.08);
}
.toolbar button:hover:not(:disabled) {
  background: linear-gradient(90deg, #357ae8 0%, #4f8cff 100%);
  color: #fff;
  box-shadow: 0 4px 16px 0 rgba(79, 140, 255, 0.13);
  transform: translateY(-1px) scale(1.03);
}
.toolbar button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.graph-container {
  flex: 1;
  border: 1.5px solid #e3eaf2;
  background: #fff;
  border-radius: 0 0 14px 14px;
  box-shadow: 0 4px 24px 0 rgba(79, 140, 255, 0.07);
  margin-bottom: 0;
}
</style>
