<template>
  <div class="home-container">
    <!-- 顶部标题 -->
    <div class="header">
      <h1 class="title">AI开发者工具箱</h1>
      <button class="cta-button" @click="navigateTo('/code-to-image')">
        开始探索
      </button>
    </div>

    <!-- 主要内容区 -->
    <div class="content-wrapper">
      <div class="cards-container">
        <!-- 代码生成图片 -->
        <div
          class="feature-card"
          @click="navigateTo('/code-to-image')"
          @mouseover="hoverFeature(1)"
          @mouseleave="resetHover"
        >
          <div class="icon" :class="{ animated: hoveredFeature === 1 }">✨</div>
          <h3>代码生成图片</h3>
          <p>将您的代码片段转换为美观的图片，方便分享和展示</p>
        </div>

        <!-- 代码优化 -->
        <div
          class="feature-card"
          @click="navigateTo('/code-optimization')"
          @mouseover="hoverFeature(2)"
          @mouseleave="resetHover"
        >
          <div class="icon" :class="{ animated: hoveredFeature === 2 }">⚡</div>
          <h3>代码优化</h3>
          <p>AI驱动的代码优化建议，让您的代码更高效</p>
        </div>

        <!-- BLIF调度分析 -->
        <div
          class="feature-card"
          @click="navigateTo('/asap')"
          @mouseover="hoverFeature(3)"
          @mouseleave="resetHover"
        >
          <div class="icon" :class="{ animated: hoveredFeature === 3 }">🧮</div>
          <h3>BLIF调度分析</h3>
          <p>支持ASAP/ALAP调度，适合数字电路课程实验</p>
        </div>

        <!-- 流程图编辑器 -->
        <div
          class="feature-card"
          @click="navigateTo('/about')"
          @mouseover="hoverFeature(4)"
          @mouseleave="resetHover"
        >
          <div class="icon" :class="{ animated: hoveredFeature === 4 }">🗺️</div>
          <h3>流程图编辑器</h3>
          <p>可视化流程图绘制与导出，支持自定义节点</p>
        </div>

        <!-- ILP调度分析 -->
        <div
          class="feature-card"
          @click="navigateTo('/ilp')"
          @mouseover="hoverFeature(5)"
          @mouseleave="resetHover"
        >
          <div class="icon" :class="{ animated: hoveredFeature === 5 }">📊</div>
          <h3>ILP调度分析</h3>
          <p>整数线性规划调度，适合复杂任务分配与优化</p>
        </div>

        <!-- 试试手气 -->
        <div
          class="feature-card"
          @click="rotateCard"
          :style="isRotated ? funCardStyle : {}"
        >
          <div class="icon" :class="{ rotated: isRotated }">🎲</div>
          <h3>试试手气</h3>
          <p v-if="!isRotated">点击发现惊喜</p>
          <p v-else class="fun-message">{{ funMessages[currentMessage] }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import { useRouter } from "vue-router";
import * as echarts from "echarts";
import "echarts-wordcloud";

const router = useRouter();

const hoveredFeature = ref(0);
const isRotated = ref(false);
const currentMessage = ref(0);
const wordCloudChart = ref(null);

const funMessages = [
  "你今天看起来很棒！",
  "代码写累了？休息一下吧",
  "发现一个隐藏功能！",
  "AI正在学习你的习惯",
  "试试我们的其他工具",
  "祝你Bug-Free！",
  "灵感一闪，代码如诗！",
  "今天适合写代码，也适合摸鱼~",
];

// 彩色背景池
const funBgColors = [
  "linear-gradient(135deg,#f7b42c 0%,#fc575e 100%)",
  "linear-gradient(135deg,#43cea2 0%,#185a9d 100%)",
  "linear-gradient(135deg,#ffecd2 0%,#fcb69f 100%)",
  "linear-gradient(135deg,#a1c4fd 0%,#c2e9fb 100%)",
  "linear-gradient(135deg,#fbc2eb 0%,#a6c1ee 100%)",
];
const funCardStyle = ref({});

const navigateTo = (path) => {
  router.push(path);
};

const hoverFeature = (index) => {
  hoveredFeature.value = index;
};

const resetHover = () => {
  hoveredFeature.value = 0;
};

const rotateCard = () => {
  isRotated.value = !isRotated.value;
  if (isRotated.value) {
    currentMessage.value = Math.floor(Math.random() * funMessages.length);
    funCardStyle.value = {
      background: funBgColors[Math.floor(Math.random() * funBgColors.length)],
      color: "#fff",
      transition: "background 0.5s",
    };
    setTimeout(() => {
      isRotated.value = false;
      funCardStyle.value = {};
    }, 2200);
  }
};

// 词云数据
const wordCloudData = [
  { name: "Vue", value: 10000 },
  { name: "React", value: 8000 },
  { name: "JavaScript", value: 9500 },
  { name: "TypeScript", value: 8500 },
  { name: "ECharts", value: 7000 },
  { name: "Node.js", value: 7500 },
  { name: "Webpack", value: 6500 },
  { name: "Vite", value: 6000 },
  { name: "AI", value: 9000 },
  { name: "机器学习", value: 5500 },
  { name: "深度学习", value: 5000 },
  { name: "前端开发", value: 8000 },
  { name: "后端开发", value: 7500 },
  { name: "数据可视化", value: 7000 },
  { name: "算法", value: 6500 },
];

let chartInstance = null;

const initWordCloud = () => {
  if (!wordCloudChart.value) return;
  chartInstance = echarts.init(wordCloudChart.value);
  const option = {
    backgroundColor: "transparent",
    tooltip: { show: true },
    series: [
      {
        type: "wordCloud",
        shape: "circle",
        left: "center",
        top: "center",
        width: "100%",
        height: "100%",
        sizeRange: [12, 40],
        rotationRange: [-45, 45],
        rotationStep: 15,
        gridSize: 10,
        drawOutOfBound: false,
        textStyle: {
          fontFamily: "Microsoft YaHei",
          fontWeight: "bold",
          color: function () {
            const colors = [
              "#409EFF",
              "#67C23A",
              "#E6A23C",
              "#F56C6C",
              "#909399",
              "#c23531",
              "#2f4554",
              "#61a0a8",
              "#d48265",
              "#91c7ae",
            ];
            return colors[Math.floor(Math.random() * colors.length)];
          },
        },
        emphasis: {
          focus: "self",
          textStyle: {
            shadowBlur: 10,
            shadowColor: "#333",
          },
        },
        data: wordCloudData,
      },
    ],
  };
  chartInstance.setOption(option);
};

const resizeChart = () => {
  chartInstance?.resize();
};

onMounted(() => {
  initWordCloud();
  window.addEventListener("resize", resizeChart);
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", resizeChart);
  chartInstance?.dispose();
});
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  width: 100%;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #e3f0ff 0%, #f8fbff 100%);
}

.header {
  width: 100%;
  padding: 28px 20px 20px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
}

.title {
  font-size: 32px;
  margin: 0;
  background: linear-gradient(90deg, #4f8cff, #67c23a 80%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  font-weight: 800;
  letter-spacing: 2px;
  text-shadow: 0 2px 8px rgba(79, 140, 255, 0.08);
  user-select: none;
}

.cta-button {
  background: linear-gradient(90deg, #4f8cff 0%, #6fc3ff 100%);
  color: #fff;
  border: none;
  padding: 12px 32px;
  border-radius: 25px;
  font-size: 18px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(79, 140, 255, 0.1);
  transition: all 0.3s;
  animation: cta-breath 2.5s infinite alternate;
}

@keyframes cta-breath {
  from {
    box-shadow: 0 4px 12px rgba(79, 140, 255, 0.1);
  }
  to {
    box-shadow: 0 8px 24px rgba(79, 140, 255, 0.18);
  }
}

.cta-button:hover {
  background: linear-gradient(90deg, #357ae8 0%, #4f8cff 100%);
  transform: translateY(-2px) scale(1.04);
  box-shadow: 0 8px 24px rgba(79, 140, 255, 0.18);
}

.content-wrapper {
  flex: 1;
  width: 100%;
  display: flex;
  justify-content: center;
  padding: 30px 20px;
}

.cards-container {
  max-width: 1100px;
  width: 100%;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 32px;
  justify-content: center;
  align-items: center;
  margin: 0 auto;
  /* 居中容器 */
}

.feature-card {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(79, 140, 255, 0.07);
  padding: 34px 24px 28px 24px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 260px;
  border: 1.5px solid #e3eaf2;
  position: relative;
  overflow: hidden;
}

.feature-card:hover {
  transform: translateY(-7px) scale(1.03);
  box-shadow: 0 12px 32px rgba(79, 140, 255, 0.13);
  border-color: #4f8cff;
}

.feature-card h3 {
  color: #357ae8;
  margin: 18px 0 10px;
  font-size: 20px;
  font-weight: 700;
}

.feature-card p {
  color: #606266;
  font-size: 15px;
  line-height: 1.6;
  margin: 0;
}

.icon {
  font-size: 44px;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  margin-bottom: 12px;
  display: inline-block;
  user-select: none;
}

.animated {
  animation: bounce 0.7s ease-in-out infinite alternate;
}

.rotated {
  animation: rotate 0.7s linear;
}

@keyframes bounce {
  from {
    transform: translateY(0);
  }
  to {
    transform: translateY(-12px);
  }
}

@keyframes rotate {
  0% {
    transform: rotate(0);
  }
  100% {
    transform: rotate(360deg);
  }
}

.fun-message {
  color: #fff;
  font-weight: 600;
  font-size: 16px;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.12);
  margin-top: 10px;
}

.word-cloud-card {
  grid-column: 1 / -1;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(79, 140, 255, 0.07);
  padding: 30px;
  display: flex;
  flex-direction: column;
  height: 350px;
  border: 1.5px solid #e3eaf2;
}

.word-cloud-card h3 {
  color: #357ae8;
  margin: 0 0 15px;
  text-align: center;
  font-size: 18px;
  font-weight: 700;
}

.word-cloud-chart {
  width: 100%;
  height: 100%;
  flex: 1;
}

@media (max-width: 1200px) {
  .cards-container {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 800px) {
  .cards-container {
    grid-template-columns: 1fr;
  }
  .feature-card,
  .word-cloud-card {
    min-height: 180px;
    padding: 18px 10px;
  }
}
</style>