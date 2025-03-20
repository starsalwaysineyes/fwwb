<template>
  <div class="voice-samples-page">
    <h1>声音样本库</h1>
    <p class="page-desc">管理和创建您的声音样本，用于生成个性化语音</p>

    <div class="toolbar">
      <button class="btn" @click="showAddSampleModal = true">
        <span>添加声音样本</span>
      </button>
      <div class="search-box">
        <input type="text" class="form-input" placeholder="搜索声音样本..." v-model="searchQuery">
      </div>
    </div>

    <div class="sample-types">
      <div class="type-selector" :class="{ active: activeType === 'all' }" @click="activeType = 'all'">
        全部
      </div>
      <div class="type-selector" :class="{ active: activeType === 'preset' }" @click="activeType = 'preset'">
        预设声音
      </div>
      <div class="type-selector" :class="{ active: activeType === 'custom' }" @click="activeType = 'custom'">
        自定义声音
      </div>
    </div>

    <!-- 声音样本列表 -->
    <div class="samples-grid">
      <!-- 预设样本项 -->
      <div v-for="sample in filteredSamples" :key="sample.id" class="sample-card">
        <div class="sample-card-header">
          <span class="sample-name">{{ sample.name }}</span>
          <span class="sample-type">{{ sample.type === 'preset' ? '预设' : '自定义' }}</span>
        </div>
        <div class="sample-card-body">
          <div class="sample-avatar">
            {{ sample.name.charAt(0) }}
          </div>
          <div class="sample-info">
            <div class="info-item">
              <span class="info-label">语言:</span>
              <span class="info-value">{{ sample.language }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">性别:</span>
              <span class="info-value">{{ sample.gender }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">风格:</span>
              <span class="info-value">{{ sample.style }}</span>
            </div>
          </div>
        </div>
        <div class="sample-card-footer">
          <button class="btn-icon" @click="playSample(sample)">
            <span class="icon">▶️</span>
          </button>
          <button class="btn-icon" @click="editSample(sample)" v-if="sample.type !== 'preset'">
            <span class="icon">✏️</span>
          </button>
          <button class="btn-icon delete" @click="confirmDelete(sample)" v-if="sample.type !== 'preset'">
            <span class="icon">🗑️</span>
          </button>
        </div>
      </div>

      <!-- 空状态提示 -->
      <div v-if="filteredSamples.length === 0" class="empty-state">
        <p>没有找到匹配的声音样本</p>
        <button class="btn" @click="showAddSampleModal = true">添加声音样本</button>
      </div>
    </div>

    <!-- 添加声音样本模态框 -->
    <div class="modal" v-if="showAddSampleModal">
      <div class="modal-content">
        <div class="modal-header">
          <h2>添加声音样本</h2>
          <button class="btn-close" @click="showAddSampleModal = false">×</button>
        </div>
        <div class="modal-body">
          <div class="tabs">
            <div class="tab" :class="{ active: activeTab === 'upload' }" @click="activeTab = 'upload'">
              上传音频
            </div>
            <div class="tab" :class="{ active: activeTab === 'record' }" @click="activeTab = 'record'">
              现场录制
            </div>
          </div>

          <div class="tab-content">
            <!-- 上传音频标签页 -->
            <div v-if="activeTab === 'upload'" class="upload-tab">
              <div class="form-group">
                <label class="form-label">样本名称</label>
                <input type="text" class="form-input" v-model="newSample.name" placeholder="输入样本名称">
              </div>
              <div class="form-group">
                <label class="form-label">选择语言</label>
                <select class="form-input" v-model="newSample.language">
                  <option value="中文">中文</option>
                  <option value="英文">英文</option>
                  <option value="其他">其他</option>
                </select>
              </div>
              <div class="form-group">
                <label class="form-label">选择性别</label>
                <select class="form-input" v-model="newSample.gender">
                  <option value="男">男</option>
                  <option value="女">女</option>
                  <option value="中性">中性</option>
                </select>
              </div>
              <div class="form-group">
                <label class="form-label">声音风格</label>
                <select class="form-input" v-model="newSample.style">
                  <option value="标准">标准</option>
                  <option value="活力">活力</option>
                  <option value="柔和">柔和</option>
                  <option value="专业">专业</option>
                </select>
              </div>
              <div class="form-group">
                <label class="form-label">上传音频文件</label>
                <div class="file-upload">
                  <input type="file" id="audio-file" accept="audio/*" class="file-input">
                  <label for="audio-file" class="file-label">
                    <span>选择文件</span>
                    <small>(建议5-30秒的单独人声录音)</small>
                  </label>
                </div>
              </div>
            </div>

            <!-- 现场录制标签页 -->
            <div v-if="activeTab === 'record'" class="record-tab">
              <div class="form-group">
                <label class="form-label">样本名称</label>
                <input type="text" class="form-input" v-model="newSample.name" placeholder="输入样本名称">
              </div>
              <div class="form-group">
                <label class="form-label">选择语言</label>
                <select class="form-input" v-model="newSample.language">
                  <option value="中文">中文</option>
                  <option value="英文">英文</option>
                  <option value="其他">其他</option>
                </select>
              </div>
              <div class="form-group">
                <label class="form-label">选择性别</label>
                <select class="form-input" v-model="newSample.gender">
                  <option value="男">男</option>
                  <option value="女">女</option>
                  <option value="中性">中性</option>
                </select>
              </div>
              <div class="form-group">
                <label class="form-label">声音风格</label>
                <select class="form-input" v-model="newSample.style">
                  <option value="标准">标准</option>
                  <option value="活力">活力</option>
                  <option value="柔和">柔和</option>
                  <option value="专业">专业</option>
                </select>
              </div>
              <div class="recorder">
                <div class="recorder-status">
                  {{ isRecording ? '正在录制...' : '准备录制' }}
                  <span v-if="isRecording" class="recording-time">{{ recordingTime }}s</span>
                </div>
                <div class="recorder-controls">
                  <button class="btn" @click="startRecording" :disabled="isRecording">
                    开始录制
                  </button>
                  <button class="btn btn-danger" @click="stopRecording" :disabled="!isRecording">
                    停止录制
                  </button>
                  <button class="btn btn-secondary" @click="playRecording" :disabled="!hasRecording">
                    播放录音
                  </button>
                </div>
                <div class="recorder-wave">
                  <!-- 录音波形可视化区域 -->
                  <div class="wave-placeholder"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="showAddSampleModal = false">取消</button>
          <button class="btn" @click="addSample">添加</button>
        </div>
      </div>
    </div>

    <!-- 删除确认模态框 -->
    <div class="modal" v-if="showDeleteModal">
      <div class="modal-content">
        <div class="modal-header">
          <h2>确认删除</h2>
          <button class="btn-close" @click="showDeleteModal = false">×</button>
        </div>
        <div class="modal-body">
          <p>您确定要删除声音样本 "{{ sampleToDelete?.name }}" 吗？此操作无法撤销。</p>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="showDeleteModal = false">取消</button>
          <button class="btn btn-danger" @click="deleteSample">删除</button>
        </div>
      </div>
    </div>

    <!-- 音频播放器 -->
    <audio ref="audioPlayer"></audio>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

// 数据模型
const samples = ref([
  { id: 1, name: '标准男声', type: 'preset', language: '中文', gender: '男', style: '标准', audioUrl: '/samples/male.mp3' },
  { id: 2, name: '标准女声', type: 'preset', language: '中文', gender: '女', style: '标准', audioUrl: '/samples/female.mp3' },
  { id: 3, name: '英语男声', type: 'preset', language: '英文', gender: '男', style: '标准', audioUrl: '/samples/en-male.mp3' },
  { id: 4, name: '英语女声', type: 'preset', language: '英文', gender: '女', style: '标准', audioUrl: '/samples/en-female.mp3' },
  { id: 5, name: '专业讲解', type: 'preset', language: '中文', gender: '男', style: '专业', audioUrl: '/samples/professional.mp3' }
])

// 界面状态
const searchQuery = ref('')
const activeType = ref('all')
const activeTab = ref('upload')
const showAddSampleModal = ref(false)
const showDeleteModal = ref(false)
const sampleToDelete = ref(null)
const isRecording = ref(false)
const recordingTime = ref(0)
const hasRecording = ref(false)
const audioPlayer = ref(null)

// 新样本数据
const newSample = ref({
  name: '',
  language: '中文',
  gender: '男',
  style: '标准'
})

// 过滤后的样本
const filteredSamples = computed(() => {
  let result = samples.value

  // 按类型过滤
  if (activeType.value !== 'all') {
    result = result.filter(sample => sample.type === activeType.value)
  }

  // 按搜索关键词过滤
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(sample => 
      sample.name.toLowerCase().includes(query) || 
      sample.language.toLowerCase().includes(query) || 
      sample.style.toLowerCase().includes(query)
    )
  }

  return result
})

// 方法
function playSample(sample) {
  if (audioPlayer.value && sample.audioUrl) {
    audioPlayer.value.src = sample.audioUrl
    audioPlayer.value.play()
  } else {
    alert('播放示例：这里会播放对应的声音样本')
  }
}

function editSample(sample) {
  alert(`编辑示例：这里会打开编辑 ${sample.name} 的界面`)
}

function confirmDelete(sample) {
  sampleToDelete.value = sample
  showDeleteModal.value = true
}

function deleteSample() {
  if (sampleToDelete.value) {
    samples.value = samples.value.filter(s => s.id !== sampleToDelete.value.id)
    showDeleteModal.value = false
    sampleToDelete.value = null
  }
}

function addSample() {
  // 示例添加逻辑
  const id = Math.max(...samples.value.map(s => s.id)) + 1
  samples.value.push({
    id,
    ...newSample.value,
    type: 'custom',
    audioUrl: null
  })
  
  // 重置表单
  newSample.value = {
    name: '',
    language: '中文',
    gender: '男',
    style: '标准'
  }
  
  showAddSampleModal.value = false
  activeTab.value = 'upload'
  hasRecording.value = false
}

function startRecording() {
  isRecording.value = true
  recordingTime.value = 0
  
  // 模拟录制计时
  const timer = setInterval(() => {
    recordingTime.value++
    if (recordingTime.value >= 30) {
      clearInterval(timer)
      stopRecording()
    }
  }, 1000)
  
  // 实际应用中，这里会调用浏览器的录音API
  console.log('开始录制声音样本')
}

function stopRecording() {
  isRecording.value = false
  hasRecording.value = true
  
  // 实际应用中，这里会停止录音并处理录制好的音频
  console.log('停止录制声音样本')
}

function playRecording() {
  // 实际应用中，这里会播放刚刚录制的声音
  alert('播放示例：这里会播放刚录制的声音样本')
}
</script>

<style scoped>
.voice-samples-page {
  padding-bottom: 2rem;
}

h1 {
  margin-bottom: 0.5rem;
  color: #1890ff;
}

.page-desc {
  color: #666;
  margin-bottom: 2rem;
}

.sample-types {
  display: flex;
  margin-bottom: 2rem;
  border-bottom: 1px solid #e8e8e8;
}

.type-selector {
  padding: 0.75rem 1.5rem;
  cursor: pointer;
  position: relative;
  color: #666;
}

.type-selector.active {
  color: #1890ff;
  font-weight: 500;
}

.type-selector.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background-color: #1890ff;
}

.samples-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

.sample-card {
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.sample-card-header {
  padding: 1rem;
  background-color: #f5f7fa;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.sample-name {
  font-weight: 500;
}

.sample-type {
  font-size: 0.85rem;
  color: #1890ff;
  background-color: rgba(24, 144, 255, 0.1);
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}

.sample-card-body {
  padding: 1.5rem;
  display: flex;
  align-items: center;
}

.sample-avatar {
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #1890ff;
  color: white;
  font-size: 1.5rem;
  border-radius: 50%;
  margin-right: 1rem;
}

.sample-info {
  flex: 1;
}

.info-item {
  margin-bottom: 0.5rem;
  display: flex;
}

.info-label {
  color: #666;
  width: 50px;
}

.info-value {
  font-weight: 500;
}

.sample-card-footer {
  display: flex;
  border-top: 1px solid #e8e8e8;
}

.btn-icon {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.75rem;
  background: none;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-icon:hover {
  background-color: #f5f7fa;
}

.btn-icon.delete:hover {
  background-color: #fff1f0;
}

.icon {
  font-size: 1.25rem;
}

.search-box {
  flex: 1;
  max-width: 300px;
}

.empty-state {
  grid-column: 1 / -1;
  text-align: center;
  padding: 3rem;
  background-color: #f5f7fa;
  border-radius: 8px;
}

.empty-state p {
  margin-bottom: 1rem;
  color: #666;
}

/* 模态框样式 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e8e8e8;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.25rem;
  color: #1890ff;
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #999;
}

.modal-body {
  padding: 1.5rem;
}

.modal-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid #e8e8e8;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

/* 标签页样式 */
.tabs {
  display: flex;
  border-bottom: 1px solid #e8e8e8;
  margin-bottom: 1.5rem;
}

.tab {
  padding: 0.75rem 1.5rem;
  cursor: pointer;
  color: #666;
}

.tab.active {
  color: #1890ff;
  font-weight: 500;
  border-bottom: 2px solid #1890ff;
}

.file-upload {
  position: relative;
  display: inline-block;
  width: 100%;
}

.file-input {
  position: absolute;
  left: 0;
  top: 0;
  opacity: 0;
  width: 100%;
  height: 100%;
  cursor: pointer;
}

.file-label {
  display: block;
  padding: 0.75rem;
  background-color: #f5f7fa;
  border: 1px dashed #d9d9d9;
  border-radius: 4px;
  text-align: center;
  cursor: pointer;
  transition: border-color 0.3s;
}

.file-label:hover {
  border-color: #1890ff;
}

.file-label span {
  display: block;
  margin-bottom: 0.25rem;
  font-weight: 500;
}

.file-label small {
  color: #999;
}

/* 录音机样式 */
.recorder {
  background-color: #f5f7fa;
  border-radius: 8px;
  padding: 1.5rem;
  margin-top: 1rem;
}

.recorder-status {
  text-align: center;
  margin-bottom: 1rem;
  font-weight: 500;
}

.recording-time {
  color: #ff4d4f;
  margin-left: 0.5rem;
}

.recorder-controls {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 1rem;
  justify-content: center;
}

.wave-placeholder {
  height: 60px;
  background-color: #e8e8e8;
  border-radius: 4px;
  position: relative;
  overflow: hidden;
}

.wave-placeholder::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 2px;
  background-color: #1890ff;
}

@media (max-width: 768px) {
  .sample-types,
  .tabs {
    overflow-x: auto;
  }
  
  .type-selector,
  .tab {
    white-space: nowrap;
  }
  
  .toolbar {
    flex-direction: column;
  }
  
  .search-box {
    max-width: 100%;
    margin-top: 1rem;
  }
  
  .recorder-controls {
    flex-wrap: wrap;
  }
}
</style> 