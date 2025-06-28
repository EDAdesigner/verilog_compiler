<template>
  <div class="sidebar">
    <div class="sidebar-bg"></div>
    <div class="sidebar-content">
      <div class="sidebar-header">
        <div class="app-logo" style="font-size: 28px; line-height: 36px">
          🔌
        </div>
        <h2 class="app-title">逻辑综合工具设计</h2>
      </div>

      <div class="menu-items">
        <div
          v-for="(item, index) in menuItems"
          :key="index"
          class="menu-item"
          :class="{ active: activeRoute === item.path }"
          @click="navigateTo(item.path)"
        >
          <div class="menu-icon">
            <span class="icon" v-html="item.icon"></span>
          </div>
          <span class="menu-text">{{ item.text }}</span>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, computed } from "vue";
import { useRouter, useRoute } from "vue-router";

const router = useRouter();
const route = useRoute();

const menuItems = ref([
  {
    text: "主页",
    path: "/",
    icon: "&#xe608;", // 使用Unicode图标或SVG
  },
  {
    text: "电路网表图绘制",
    path: "/code-to-image",
    icon: "&#xe62c;",
  },
  {
    text: "高阶优化",
    path: "/code-optimization",
    icon: "&#xe68f;",
  },
  {
    text: "调度算法",
    path: "/asap",
    icon: "&#xe611;",
  },
  {
    text: "ILP求解调度",
    path: "/ilp",
    icon: "&#xe602;",
  },
  {
    text: "电路编辑",
    path: "/about",
    icon: "&#xe6e5;",
  },
]);

const activeRoute = computed(() => route.path);

const navigateTo = (path) => {
  router.push(path);
};
</script>

<style scoped>
/* 在线链接服务仅供平台体验和调试使用，平台不承诺服务的稳定性，企业客户需下载字体包自行发布使用并做好备份。 */
@font-face {
  font-family: "iconfont"; /* Project id 4900944 */
  src: url("//at.alicdn.com/t/c/font_4900944_t9wvoi5416.woff2?t=1751038265379")
      format("woff2"),
    url("//at.alicdn.com/t/c/font_4900944_t9wvoi5416.woff?t=1751038265379")
      format("woff"),
    url("//at.alicdn.com/t/c/font_4900944_t9wvoi5416.ttf?t=1751038265379")
      format("truetype");
}
/* 基础样式 */
.sidebar {
  position: fixed;
  left: 0;
  top: 0;
  width: 280px;
  height: 100vh;
  z-index: 100;
  overflow: hidden;
  transition: all 0.3s ease;
  font-family: "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
}

.sidebar-bg {
  position: absolute;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #20222b 0%, #1a1c24 100%);
  box-shadow: 4px 0 15px rgba(0, 0, 0, 0.1);
}

.sidebar-content {
  position: relative;
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 20px 0;
}

/* 头部样式 */
.sidebar-header {
  display: flex;
  align-items: center;
  padding: 0 24px 20px;
  margin-bottom: 10px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.app-logo {
  width: 36px;
  height: 36px;
  background: #1890ff;
  border-radius: 8px;
  margin-right: 12px;
}

.app-title {
  color: #fff;
  font-size: 18px;
  font-weight: 600;
  margin: 0;
}

/* 菜单项样式 */
.menu-items {
  flex: 1;
  overflow-y: auto;
  padding: 0 12px;
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  margin: 4px 0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: rgba(255, 255, 255, 0.8);
}

.menu-item:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
}

.menu-item.active {
  background: rgba(24, 144, 255, 0.2);
  color: #fff;
  box-shadow: 0 2px 8px rgba(24, 144, 255, 0.2);
}

.menu-item.active .menu-icon {
  color: #1890ff;
}

/* 图标样式 */
.menu-icon {
  width: 20px;
  height: 20px;
  margin-right: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgba(255, 255, 255, 0.6);
  transition: all 0.3s ease;
  font-family: "iconfont"; /* 使用自定义字体图标 */
}

.menu-text {
  font-size: 14px;
  font-weight: 500;
}

/* 滚动条样式 */
.menu-items::-webkit-scrollbar {
  width: 6px;
}

.menu-items::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 3px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .sidebar {
    width: 220px;
  }

  .sidebar-header {
    padding: 0 16px 16px;
    flex-direction: column;
    align-items: flex-start;
  }

  .app-logo {
    margin-bottom: 10px;
  }
}
</style>