<template>
  <div class="layout-container">
    <TheSidebar />
    <RouterView class="main-content" />
  </div>
</template>

<script setup>
import { RouterView } from "vue-router";
import TheSidebar from "./components/TheSidebar.vue";
</script>

<style scoped>
.layout-container {
  position: relative;
  z-index: 2;
  height: 100vh;
  background-color: #f5f7fa;
  display: flex; /* 添加flex布局 */
}

::-webkit-scrollbar {
  display: none;
}

.main-content {
  flex: 1; /* 占据剩余空间 */
  padding: 16px;
  overflow-y: auto; /* 允许内容滚动 */
  display: flex; /* 添加flex布局 */
  flex-direction: column; /* 垂直方向排列 */
  align-items: center; /* 水平居中 */
  margin-left: 264px; /* 侧边栏宽度 */

}

/* 添加内容容器样式，限制最大宽度 */
.main-content > * {
  width: 100%;
  padding: 0 20px; /* 添加内边距 */
}
</style>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box; /* 添加盒模型计算方式 */
}

.overlay_center,
.overlay_top_left,
.overlay_top_center,
.overlay_top_right,
.overlay_bottom_left,
.overlay_bottom_center {
  position: absolute;
  z-index: 9999;
}

.overlay_center {
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  margin: auto;
}

.overlay_top_left {
  top: 0;
  left: 0;
}

.overlay_top_center {
  top: 0;
  left: 0;
  right: 0;
  margin: auto;
}

.overlay_top_right {
  top: 0;
  right: 0;
}

.overlay_bottom_left {
  bottom: 0;
  left: 0;
  margin: auto;
}

.overlay_bottom_center {
  bottom: 0;
  left: 0;
  right: 0;
  margin: auto;
}

.popupMask {
  position: fixed;
  left: 0;
  top: 0;
  height: 100%;
  width: 100%;
  z-index: 9999;
}
</style>