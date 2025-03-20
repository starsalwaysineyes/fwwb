<template>
  <div class="app-container">
    <header class="app-header">
      <nav class="app-nav">
        <router-link to="/" class="logo">AI语音合成教学软件</router-link>
        <div class="nav-links">
          <router-link to="/">首页</router-link>
          <router-link to="/voice-samples">声音样本库</router-link>
          <router-link to="/text-to-speech">文本转语音</router-link>
          <router-link to="/course-maker">课件制作</router-link>
          <router-link to="/voice-replace">声音置换</router-link>
        </div>
      </nav>
    </header>
    
    <main class="app-main">
      <router-view />
    </main>
    
    <footer class="app-footer">
      <p>© 2025 AI语音合成教学软件</p>
    </footer>
  </div>
</template>

<script setup>
// 这里可以放置应用级别的逻辑
</script>

<style>
/* 全局样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Microsoft YaHei', sans-serif;
  color: #333;
  background-color: #f5f7fa;
}

.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.app-header {
  background-color: #1890ff;
  color: white;
  padding: 0 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.app-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 64px;
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  text-decoration: none;
  color: white;
}

.nav-links {
  display: flex;
  gap: 1.5rem;
}

.nav-links a {
  color: white;
  text-decoration: none;
  font-size: 1rem;
  padding: 0.5rem 0;
  position: relative;
}

.nav-links a::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background-color: white;
  transition: width 0.3s;
}

.nav-links a:hover::after,
.nav-links a.router-link-active::after {
  width: 100%;
}

.app-main {
  flex: 1;
  padding: 2rem;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
}

.app-footer {
  background-color: #1890ff;
  color: white;
  text-align: center;
  padding: 1rem;
  margin-top: auto;
}
</style> 