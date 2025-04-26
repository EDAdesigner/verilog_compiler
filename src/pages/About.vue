<template>
  <div class="about-container">
    <!-- 顶部标题 -->
    <div class="header">
      <h1 class="title">关于我们</h1>
    </div>

    <!-- 主要内容区 -->
    <div class="main-content">
      <div class="about-card">
        <div class="about-section">
          <h2 class="section-title">团队介绍</h2>
          <div class="section-content">
            <p>我们是一支由资深开发者和AI专家组成的团队，致力于通过技术创新提升开发效率。</p>
            <p>团队成员来自国内外知名科技公司，拥有丰富的工程实践经验和前沿技术研究背景。</p>
          </div>
        </div>

        <div class="about-section">
          <h2 class="section-title">产品理念</h2>
          <div class="section-content">
            <p>我们相信：代码应该简洁高效，工具应该智能易用。</p>
            <p>通过AI技术赋能开发者，让重复工作自动化，让复杂问题简单化。</p>
          </div>
        </div>

        <div class="about-section">
          <h2 class="section-title">联系我们</h2>
          <div class="section-content contact-info">
            <div class="contact-item">
              <span class="contact-icon">📧</span>
              <span>Email: contact@aidevtools.com</span>
            </div>
            <div class="contact-item">
              <span class="contact-icon">🌐</span>
              <span>Website: www.aidevtools.com</span>
            </div>
            <div class="contact-item">
              <span class="contact-icon">🏢</span>
              <span>地址: 上海市浦东新区张江高科技园区</span>
            </div>
          </div>
        </div>

        <div class="about-section">
          <h2 class="section-title">技术栈</h2>
          <div class="tech-stack">
            <span class="tech-tag">Vue 3</span>
            <span class="tech-tag">TypeScript</span>
            <span class="tech-tag">Node.js</span>
            <span class="tech-tag">Python</span>
            <span class="tech-tag">TensorFlow</span>
            <span class="tech-tag">Docker</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// 不需要响应式数据，纯展示型组件
</script>

<style scoped>
/* 更新后的样式 */
.about-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f5f7fa;
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #e4e7ed;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto 20px;
}

.title {
  font-size: 24px;
  color: #303133;
  margin: 0;
}

/* 主要内容区样式 - 修改后 */
.main-content {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center; /* 改为center实现垂直居中 */
  padding: 20px;
  width: 100%;
}

.about-card {
  width: 100%;
  max-width: 800px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  padding: 40px; /* 增加内边距 */
  margin: auto; /* 确保居中 */
}

/* 其余样式保持不变 */
.about-section {
  margin-bottom: 30px;
}

.section-title {
  font-size: 18px;
  color: #409eff;
  margin-bottom: 15px;
  padding-bottom: 8px;
  border-bottom: 1px solid #ebeef5;
}

.section-content {
  font-size: 15px;
  line-height: 1.8;
  color: #606266;
}

.section-content p {
  margin: 10px 0;
}

.contact-info {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.contact-icon {
  font-size: 18px;
}

.tech-stack {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.tech-tag {
  background-color: #ecf5ff;
  color: #409eff;
  padding: 5px 12px;
  border-radius: 4px;
  font-size: 13px;
  border: 1px solid #d9ecff;
}
</style>