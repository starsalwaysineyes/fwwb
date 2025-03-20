<template>
  <div class="home-page">
    <section class="hero">
      <div class="hero-content">
        <h1>AI语音合成教学软件</h1>
        <p>利用AI技术提升教学效果，定制专属教学声音</p>
        <div class="hero-buttons">
          <router-link to="/voice-samples" class="btn">开始使用</router-link>
          <a href="#features" class="btn btn-secondary">了解功能</a>
        </div>
      </div>
      <div class="hero-image">
        <!-- 此处可放置一个合适的示意图 -->
        <div class="placeholder-image">AI语音合成示意图</div>
      </div>
    </section>

    <section id="features" class="features">
      <h2>核心功能</h2>
      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon">🎙️</div>
          <h3>声音样本库</h3>
          <p>预设标准声音、上传音频文件或现场录制，轻松创建个性化声音</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">🔊</div>
          <h3>个性化语音讲解</h3>
          <p>输入文本内容，选择声音样本，一键生成自然流畅的语音讲解</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">🗣️</div>
          <h3>标准语言输出</h3>
          <p>输出普通话、英文等标准发音，可控制语速、语气和节奏</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">📚</div>
          <h3>课件制作下载</h3>
          <p>上传教学课件，一键生成有声课件，轻松下载分享</p>
        </div>
      </div>
    </section>

    <section class="benefits">
      <h2>应用场景</h2>
      <div class="benefits-list">
        <div class="benefit-item">
          <h3>提高教学效果</h3>
          <p>通过灵活的语言风格和个性化的语音讲解，提高学生学习体验和教学效果</p>
        </div>
        <div class="benefit-item">
          <h3>语言学习辅助</h3>
          <p>帮助语言学习者练习发音和语言节奏，提供自然流畅的语音样本</p>
        </div>
        <div class="benefit-item">
          <h3>辅助特定教育</h3>
          <p>为视障或阅读困难的学生提供文本到语音的服务，帮助他们更好地获取信息</p>
        </div>
        <div class="benefit-item">
          <h3>促进教育公平</h3>
          <p>在缺乏教师资源的地区创建虚拟教师，提供标准化的教学内容</p>
        </div>
      </div>
    </section>

    <section class="cta">
      <h2>立即开始使用</h2>
      <p>体验AI语音合成带来的全新教学方式</p>
      <router-link to="/voice-samples" class="btn">开始使用</router-link>
    </section>
  </div>
</template>

<script setup>
// 首页逻辑代码
</script>

<style scoped>
.home-page {
  max-width: 100%;
}

.hero {
  display: flex;
  align-items: center;
  margin-bottom: 4rem;
}

.hero-content {
  flex: 1;
}

.hero-content h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  color: #1890ff;
}

.hero-content p {
  font-size: 1.25rem;
  margin-bottom: 2rem;
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
  width: 400px;
  height: 300px;
  background-color: #f0f0f0;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 8px;
  color: #999;
  font-size: 1.25rem;
}

.features, .benefits {
  margin-bottom: 4rem;
}

.features h2, .benefits h2 {
  text-align: center;
  margin-bottom: 2rem;
  font-size: 2rem;
  color: #1890ff;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.feature-card {
  background-color: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: transform 0.3s;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.feature-card h3 {
  font-size: 1.25rem;
  margin-bottom: 1rem;
  color: #1890ff;
}

.benefits-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.benefit-item {
  background-color: #f5f7fa;
  border-left: 4px solid #1890ff;
  padding: 1.5rem;
  border-radius: 0 8px 8px 0;
}

.benefit-item h3 {
  margin-bottom: 0.5rem;
  color: #1890ff;
}

.cta {
  text-align: center;
  background-color: #f0f8ff;
  padding: 3rem;
  border-radius: 8px;
}

.cta h2 {
  font-size: 2rem;
  margin-bottom: 1rem;
  color: #1890ff;
}

.cta p {
  font-size: 1.25rem;
  margin-bottom: 2rem;
  color: #666;
}

@media (max-width: 768px) {
  .hero {
    flex-direction: column;
    text-align: center;
  }
  
  .hero-content {
    margin-bottom: 2rem;
  }
  
  .hero-buttons {
    justify-content: center;
  }
  
  .placeholder-image {
    width: 100%;
    max-width: 300px;
    height: 200px;
  }
}
</style> 