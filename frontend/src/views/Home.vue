<template>
  <div class="home-page">
    <div class="compact-layout">
      <section class="hero">
        <div class="hero-content">
          <h1>AI语音合成教学软件</h1>
          <p>利用AI技术提升教学效果，定制专属教学声音</p>
          <div class="hero-buttons">
            <router-link to="/voice-samples" class="btn">开始使用</router-link>
          </div>
        </div>
        <div class="hero-image">
          <!-- 此处可放置一个合适的示意图 -->
          <img src="../assets/images/voice.png" alt="AI语音合成示意图" class="placeholder-image">
        </div>
      </section>

      <section class="features">
        <h2>核心功能</h2>
        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-icon">🎙️</div>
            <h3>声音样本库</h3>
            <p>预设标准声音、上传或录制个性化声音</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">🔊</div>
            <h3>个性化语音讲解</h3>
            <p>文本内容一键转换为自然流畅的语音</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">🗣️</div>
            <h3>标准语言输出</h3>
            <p>多语言支持，可控制语速和语气</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">📚</div>
            <h3>课件制作下载</h3>
            <p>上传教学课件，一键生成有声课件</p>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
// 首页逻辑代码
</script>

<style scoped>
.home-page {
  max-width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.compact-layout {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.hero {
  display: flex;
  align-items: center;
  padding: 0 1rem;
}

.hero-content {
  flex: 1;
}

.hero-content h1 {
  font-size: 2.2rem;
  margin-bottom: 0.5rem;
  color: #1890ff;
}

.hero-content p {
  font-size: 1.1rem;
  margin-bottom: 1rem;
  color: #666;
}

.hero-buttons {
  display: flex;
  gap: 1rem;
}

.hero-image {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.placeholder-image {
  width: 300px;
  height: 200px;
  background-color: #f0f0f0;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 8px;
  color: #999;
  font-size: 1.1rem;
}

.features {
  padding: 0 1rem;
}

.features h2 {
  text-align: center;
  margin-bottom: 1.5rem;
  font-size: 1.8rem;
  color: #1890ff;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
}

.feature-card {
  background-color: white;
  border-radius: 8px;
  padding: 1.2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: transform 0.3s;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-icon {
  font-size: 2rem;
  margin-bottom: 0.7rem;
}

.feature-card h3 {
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
  color: #1890ff;
}

.feature-card p {
  font-size: 0.9rem;
  color: #666;
}

.btn {
  display: inline-block;
  background-color: #1890ff;
  color: white;
  padding: 0.6rem 1.5rem;
  border-radius: 4px;
  text-decoration: none;
  font-weight: 500;
  transition: background-color 0.3s;
}

.btn:hover {
  background-color: #40a9ff;
}

@media (max-width: 992px) {
  .features-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .hero {
    flex-direction: column;
    text-align: center;
  }
  
  .hero-content {
    margin-bottom: 1.5rem;
  }
  
  .hero-buttons {
    justify-content: center;
  }
  
  .placeholder-image {
    width: 100%;
    max-width: 250px;
    height: 150px;
  }
}

@media (max-width: 576px) {
  .features-grid {
    grid-template-columns: 1fr;
  }
}
</style> 