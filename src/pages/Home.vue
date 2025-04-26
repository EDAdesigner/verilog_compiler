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
        <!-- 第一行三个功能卡片 -->
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

        <div class="feature-card" @click="rotateCard">
          <div class="icon" :class="{ rotated: isRotated }">🎲</div>
          <h3>试试手气</h3>
          <p v-if="!isRotated">点击发现惊喜</p>
          <p v-else class="fun-message">{{ funMessages[currentMessage] }}</p>
        </div>

        <!-- 第二行词云卡片 -->
        <div class="word-cloud-card">
          <h3>技术热词</h3>
          <div ref="wordCloudChart" class="word-cloud-chart"></div>
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

const buttonText = ref("开始探索");
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
];

// 词云数据
const wordCloudData = [
  { name: 'Vue', value: 10000 },
  { name: 'React', value: 8000 },
  { name: 'JavaScript', value: 9500 },
  { name: 'TypeScript', value: 8500 },
  { name: 'ECharts', value: 7000 },
  { name: 'Node.js', value: 7500 },
  { name: 'Webpack', value: 6500 },
  { name: 'Vite', value: 6000 },
  { name: 'AI', value: 9000 },
  { name: '机器学习', value: 5500 },
  { name: '深度学习', value: 5000 },
  { name: '前端开发', value: 8000 },
  { name: '后端开发', value: 7500 },
  { name: '数据可视化', value: 7000 },
  { name: '算法', value: 6500 },
];

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
  }
};

// 初始化词云图表
let chartInstance = null;

const initWordCloud = () => {
  if (!wordCloudChart.value) return;
  
  chartInstance = echarts.init(wordCloudChart.value);
  
  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      show: true
    },
    series: [{
      type: 'wordCloud',
      shape: 'circle',
      left: 'center',
      top: 'center',
      width: '100%',
      height: '100%',
      sizeRange: [12, 40],
      rotationRange: [-45, 45],
      rotationStep: 15,
      gridSize: 10,
      drawOutOfBound: false,
      textStyle: {
        fontFamily: 'Microsoft YaHei',
        fontWeight: 'bold',
        color: function () {
          const colors = [
            '#409EFF', '#67C23A', '#E6A23C', '#F56C6C', '#909399',
            '#c23531', '#2f4554', '#61a0a8', '#d48265', '#91c7ae'
          ];
          return colors[Math.floor(Math.random() * colors.length)];
        }
      },
      emphasis: {
        focus: 'self',
        textStyle: {
          shadowBlur: 10,
          shadowColor: '#333'
        }
      },
      data: wordCloudData
    }]
  };

  chartInstance.setOption(option);
};

const resizeChart = () => {
  chartInstance?.resize();
};

onMounted(() => {
  initWordCloud();
  window.addEventListener('resize', resizeChart);
});

onBeforeUnmount(() => {
  window.removeEventListener('resize', resizeChart);
  chartInstance?.dispose();
});
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  width: 100%;
  display: flex;
  flex-direction: column;
  background-color: #f5f7fa;
}

.header {
  width: 100%;
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
}

.title {
  font-size: 28px;
  margin: 0;
  background: linear-gradient(90deg, #409eff, #67c23a);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.cta-button {
  background-color: #409eff;
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 25px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.cta-button:hover {
  background-color: #66b1ff;
  transform: translateY(-2px);
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
}

.content-wrapper {
  flex: 1;
  width: 100%;
  display: flex;
  justify-content: center;
  padding: 30px 20px;
}

.cards-container {
  max-width: 1200px;
  width: 100%;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: auto auto;
  gap: 30px;
}

.feature-card {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  padding: 30px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 330px;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.12);
}

.feature-card h3 {
  color: #409eff;
  margin: 15px 0 10px;
  font-size: 18px;
}

.feature-card p {
  color: #606266;
  font-size: 14px;
  line-height: 1.5;
  margin: 0;
}

.icon {
  font-size: 40px;
  transition: all 0.3s ease;
  margin-bottom: 10px;
}

.animated {
  animation: bounce 0.5s ease infinite alternate;
}

.rotated {
  transform: rotate(360deg);
}

.fun-message {
  color: #67c23a;
  font-weight: 500;
}

.word-cloud-card {
  grid-column: 1 / -1;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  padding: 30px;
  display: flex;
  flex-direction: column;
  height: 350px;
}

.word-cloud-card h3 {
  color: #409eff;
  margin: 0 0 15px;
  text-align: center;
  font-size: 18px;
}

.word-cloud-chart {
  width: 100%;
  height: 100%;
  flex: 1;
}

@keyframes bounce {
  from {
    transform: translateY(0);
  }
  to {
    transform: translateY(-10px);
  }
}

@media (max-width: 992px) {
  .cards-container {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .header {
    padding: 20px;
  }
  
  .cards-container {
    grid-template-columns: 1fr;
  }
  
  .feature-card {
    height: auto;
    min-height: 200px;
  }
  
  .word-cloud-card {
    height: 300px;
  }
}
</style>