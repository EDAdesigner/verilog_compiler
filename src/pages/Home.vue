<template>
  <div class="home-container">
    <!-- 顶部标题 -->
    <div class="header">
      <h1 class="title">逻辑综合工具设计</h1>
      <button class="cta-button" @click="navigateTo('/code-to-image')">
        开始探索
      </button>
    </div>

    <!-- 主要内容区 -->
    <div class="content-wrapper">
      <div class="cards-container">
        <!-- 电路网表图绘制 -->
        <div
          class="feature-card"
          @click="navigateTo('/code-to-image')"
          @mouseover="hoverFeature(0)"
          @mouseleave="resetHover"
        >
          <div class="icon" :class="{ animated: hoveredFeature === 0 }">🖼️</div>
          <h3>电路网表图绘制</h3>
          <p>将您的电路代码一键生成美观的网表图片，便于分析与展示。</p>
          <button
            v-if="hoveredFeature === 0"
            class="enter-btn"
            @click.stop="navigateTo('/code-to-image')"
          >
            进入
          </button>
        </div>

        <!-- 高阶优化 -->
        <div
          class="feature-card"
          @click="navigateTo('/code-optimization')"
          @mouseover="hoverFeature(1)"
          @mouseleave="resetHover"
        >
          <div class="icon" :class="{ animated: hoveredFeature === 1 }">⚡</div>
          <h3>高阶优化</h3>
          <p>AI驱动的代码优化建议，让您的代码更高效、更优雅。</p>
          <button
            v-if="hoveredFeature === 1"
            class="enter-btn"
            @click.stop="navigateTo('/code-optimization')"
          >
            进入
          </button>
        </div>

        <!-- 调度算法 -->
        <div
          class="feature-card"
          @click="navigateTo('/asap')"
          @mouseover="hoverFeature(2)"
          @mouseleave="resetHover"
        >
          <div class="icon" :class="{ animated: hoveredFeature === 2 }">🧮</div>
          <h3>调度算法</h3>
          <p>支持ASAP/ALAP等多种调度算法，适合数字电路课程实验。</p>
          <button
            v-if="hoveredFeature === 2"
            class="enter-btn"
            @click.stop="navigateTo('/asap')"
          >
            进入
          </button>
        </div>

        <!-- ILP求解调度 -->
        <div
          class="feature-card"
          @click="navigateTo('/ilp')"
          @mouseover="hoverFeature(3)"
          @mouseleave="resetHover"
        >
          <div class="icon" :class="{ animated: hoveredFeature === 3 }">📊</div>
          <h3>ILP求解调度</h3>
          <p>整数线性规划调度，适合复杂任务分配与优化。</p>
          <button
            v-if="hoveredFeature === 3"
            class="enter-btn"
            @click.stop="navigateTo('/ilp')"
          >
            进入
          </button>
        </div>

        <!-- 电路编辑 -->
        <div
          class="feature-card"
          @click="navigateTo('/about')"
          @mouseover="hoverFeature(4)"
          @mouseleave="resetHover"
        >
          <div class="icon" :class="{ animated: hoveredFeature === 4 }">🗺️</div>
          <h3>电路编辑</h3>
          <p>可视化电路流程图绘制与导出，支持自定义节点。</p>
          <button
            v-if="hoveredFeature === 4"
            class="enter-btn"
            @click.stop="navigateTo('/about')"
          >
            进入
          </button>
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
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const hoveredFeature = ref(-1);
const isRotated = ref(false);
const currentMessage = ref(0);

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
  hoveredFeature.value = -1;
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

.enter-btn {
  margin-top: 18px;
  background: linear-gradient(90deg, #4f8cff 0%, #6fc3ff 100%);
  color: #fff;
  border: none;
  padding: 7px 28px;
  border-radius: 18px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  box-shadow: 0 2px 8px 0 rgba(79, 140, 255, 0.08);
  transition: all 0.2s;
  opacity: 0.95;
}

.enter-btn:hover {
  background: linear-gradient(90deg, #357ae8 0%, #4f8cff 100%);
  box-shadow: 0 4px 16px 0 rgba(79, 140, 255, 0.15);
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