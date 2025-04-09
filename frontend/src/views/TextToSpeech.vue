<template>
  <div class="text-to-speech-page">
    <h1>文本转语音</h1>
    <p class="page-desc">
      输入文本，选择语音样本，点击生成按钮将播放转换后的语音
    </p>

    <div class="tts-container">
      <div class="text-input-section">
        <div class="card">
          <div class="card-title">输入文本</div>
          <div class="text-length">
            <span>字数: {{ textLength }}</span>
            <span :class="{ 'warning': textLength > 2000 || textLength < 800 }">
              (建议800~2000字)
            </span>
          </div>
          <textarea
            class="form-textarea"
            placeholder="请输入需要转换为语音的文本内容..."
            v-model="inputText"
            @input="calculateTextLength"
          ></textarea>
          <div class="text-tools">
            <button class="btn btn-secondary" @click="clearText">清空文本</button>
            <button class="btn btn-secondary" @click="pasteFromClipboard">从剪贴板粘贴</button>
            <button class="btn btn-secondary" @click="showFileUploadModal = true">从文件导入</button>
          </div>
        </div>
      </div>

      <div class="speech-controls-section">
        <div class="card">
          <div class="card-title">语音设置</div>
          
          <div class="form-group">
            <label class="form-label">选择声音样本</label>
            <select class="form-input" v-model="selectedVoice">
              <option value="">--请选择声音--</option>
              <option v-for="voice in voices" :key="voice.id" :value="voice.id">
                {{ voice.name }} ({{ voice.language }}, {{ voice.gender }})
              </option>
            </select>
          </div>
          
          <div class="controls-grid">
            <div class="form-group">
              <label class="form-label">语速</label>
              <div class="range-control">
                <input type="range" min="0.5" max="2" step="0.1" v-model="speechRate">
                <span>{{ speechRate }}x</span>
              </div>
            </div>
            
            <div class="form-group">
              <label class="form-label">音量</label>
              <div class="range-control">
                <input type="range" min="0" max="1" step="0.1" v-model="volume">
                <span>{{ Math.round(volume * 100) }}%</span>
              </div>
            </div>
            
            <div class="form-group">
              <label class="form-label">语调</label>
              <div class="range-control">
                <input type="range" min="0.5" max="1.5" step="0.1" v-model="pitch">
                <span>{{ pitch }}</span>
              </div>
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">语气风格</label>
            <div class="style-options">
              <div 
                v-for="style in speechStyles" 
                :key="style.value" 
                class="style-option" 
                :class="{ 'active': selectedStyle === style.value }"
                @click="selectedStyle = style.value"
              >
                {{ style.label }}
              </div>
            </div>
          </div>
          
          <div class="generation-controls">
            <div class="checkbox-control">
              <input type="checkbox" id="autoPlay" v-model="autoPlay" />
              <label for="autoPlay">生成后自动播放</label>
            </div>
            
            <button @click="generateSpeech" :disabled="!canGenerate" class="primary-btn">
              <span v-if="!canGenerate">请输入文本并选择语音</span>
              <span v-else>播放文本转语音结果</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="result-section" v-if="hasGeneratedSpeech">
      <div class="card">
        <div class="card-title">生成结果</div>
        
        <div class="audio-player">
          <div class="player-controls">
            <button class="player-btn" @click="togglePlay">
              <span class="player-icon">{{ isPlaying ? '⏸️' : '▶️' }}</span>
            </button>
            <div class="progress-bar-container">
              <div class="progress-bar">
                <div class="progress" :style="{ width: `${playProgress}%` }"></div>
              </div>
              <div class="time-display">
                <span>{{ formatTime(currentTime) }}</span>
                <span>{{ formatTime(duration) }}</span>
              </div>
            </div>
          </div>
          
          <div class="player-extra-controls">
            <button class="btn btn-secondary" @click="downloadAudio">
              下载音频
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 文件上传模态框 -->
    <div class="modal" v-if="showFileUploadModal">
      <div class="modal-content">
        <div class="modal-header">
          <h2>从文件导入文本</h2>
          <button class="btn-close" @click="showFileUploadModal = false">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label class="form-label">选择文本文件</label>
            <div class="file-upload">
              <input type="file" id="text-file" accept=".txt,.doc,.docx,.pdf" class="file-input">
              <label for="text-file" class="file-label">
                <span>选择文件</span>
                <small>(支持 .txt, .doc, .docx, .pdf)</small>
              </label>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="showFileUploadModal = false">取消</button>
          <button class="btn" @click="importTextFromFile">导入</button>
        </div>
      </div>
    </div>

    <!-- 音频元素 -->
    <audio ref="audioPlayer" @timeupdate="updateProgress" @ended="audioEnded"></audio>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { assetManager } from '../components/AssetManager'

// 状态数据
const inputText = ref('')
const textLength = ref(0)
const selectedVoice = ref('')
const speechRate = ref(1)
const volume = ref(0.8)
const pitch = ref(1)
const selectedStyle = ref('standard')
const autoPlay = ref(true)
const showFileUploadModal = ref(false)

// 音频播放状态
const hasGeneratedSpeech = ref(false)
const isPlaying = ref(false)
const audioUrl = ref('')
const playProgress = ref(0)
const currentTime = ref(0)
const duration = ref(0)
const audioPlayer = ref(null)

// 预设声音样本列表
const voices = ref([
  { id: 1, name: '标准男声', language: '中文', gender: '男', type: 'preset' },
  { id: 2, name: '标准女声', language: '中文', gender: '女', type: 'preset' },
  { id: 3, name: '英语男声', language: '英文', gender: '男', type: 'preset' },
  { id: 4, name: '英语女声', language: '英文', gender: '女', type: 'preset' },
  { id: 5, name: '专业讲解', language: '中文', gender: '男', type: 'preset' }
])

// 语气风格选项
const speechStyles = [
  { label: '标准', value: 'standard' },
  { label: '专业', value: 'professional' },
  { label: '活力', value: 'energetic' },
  { label: '柔和', value: 'gentle' },
  { label: '情感', value: 'emotional' }
]

// 计算属性
const canGenerate = computed(() => {
  return inputText.value.trim().length > 0 && selectedVoice.value
})

// 方法
function calculateTextLength() {
  textLength.value = inputText.value.length
}

function clearText() {
  inputText.value = ''
  textLength.value = 0
}

async function pasteFromClipboard() {
  try {
    const text = await navigator.clipboard.readText()
    inputText.value = text
    calculateTextLength()
  } catch (error) {
    console.error('无法访问剪贴板:', error)
    alert('无法从剪贴板粘贴文本，可能是浏览器权限问题')
  }
}

function importTextFromFile() {
  // 实际应用中，这里会解析上传的文件内容
  alert('导入文本文件功能示例')
  showFileUploadModal.value = false
  // 模拟导入文本
  inputText.value = '这是从文件导入的示例文本内容。根据需求，文本长度应该在800~2000字之间，可以包含各种内容。这个示例只是一个简短的演示。'
  calculateTextLength()
}

function generateSpeech() {
  if (!canGenerate.value) return
  
  // 在实际应用中，这里会调用API生成语音
  console.log('生成语音', {
    text: inputText.value,
    voiceId: selectedVoice.value,
    rate: speechRate.value,
    volume: volume.value,
    pitch: pitch.value,
    style: selectedStyle.value
  })
  
  // 获取选中的声音样本
  const selectedVoiceObj = voices.value.find(v => v.id === parseInt(selectedVoice.value))
  
  // 根据选择的声音，获取对应的音频文件
  // 从assets/text2wav目录中读取标准男声.wav
  const audioPath = `/assets/text2wav/标准男声.wav`
  
  // 设置音频URL
  audioUrl.value = audioPath
  
  // 立即显示结果区域
  hasGeneratedSpeech.value = true
  
  // 设置音频元素
  if (audioPlayer.value) {
    audioPlayer.value.src = audioPath
    
    // 加载音频完成后的事件处理
    audioPlayer.value.onloadedmetadata = () => {
      duration.value = audioPlayer.value.duration
      
      // 如果设置了自动播放，就播放音频
      if (autoPlay.value) {
        togglePlay()
      }
    }
    
    // 加载音频错误时的处理
    audioPlayer.value.onerror = () => {
      console.error(`无法加载音频: ${audioPath}`)
      alert(`无法播放音频文件，请检查是否存在该文件`)
    }
    
    // 开始加载音频
    audioPlayer.value.load()
  }
}

function togglePlay() {
  if (!audioPlayer.value) return
  
  if (isPlaying.value) {
    audioPlayer.value.pause()
    isPlaying.value = false
  } else {
    // 播放音频
    audioPlayer.value.play().catch(error => {
      console.error('播放音频失败:', error)
      
      // 检查是否是文件不存在的问题
      if (audioPlayer.value.error && audioPlayer.value.error.code === 4) {
        alert('音频文件不存在或无法访问。请确保assets/text2wav/标准男声.wav文件存在')
      }
      
      // 模拟播放（仅在开发环境中使用）
      if (import.meta.env.DEV) {
        simulatePlayback()
      }
    })
    isPlaying.value = true
  }
}

function updateProgress() {
  if (!audioPlayer.value) return
  
  currentTime.value = audioPlayer.value.currentTime
  if (duration.value > 0) {
    playProgress.value = (currentTime.value / duration.value) * 100
  }
}

function audioEnded() {
  isPlaying.value = false
  playProgress.value = 0
  currentTime.value = 0
}

function downloadAudio() {
  // 实际应用中，这里会下载生成的音频文件
  alert('下载音频示例：在实际应用中，这里会下载生成的音频文件')
}

function formatTime(seconds) {
  const min = Math.floor(seconds / 60)
  const sec = Math.floor(seconds % 60)
  return `${min}:${sec < 10 ? '0' + sec : sec}`
}

// 模拟播放进度（仅用于演示）
function simulatePlayback() {
  let simulatedTime = 0
  const simulatedDuration = 60 // 模拟60秒的音频
  duration.value = simulatedDuration
  
  const interval = setInterval(() => {
    if (!isPlaying.value) {
      clearInterval(interval)
      return
    }
    
    simulatedTime += 1
    currentTime.value = simulatedTime
    playProgress.value = (simulatedTime / simulatedDuration) * 100
    
    if (simulatedTime >= simulatedDuration) {
      clearInterval(interval)
      audioEnded()
    }
  }, 1000)
}

onMounted(() => {
  calculateTextLength()
})
</script>

<style scoped>
.text-to-speech-page {
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

.tts-container {
  display: grid;
  grid-template-columns: 3fr 2fr;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.text-input-section, .speech-controls-section {
  display: flex;
  flex-direction: column;
}

.text-length {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  color: #666;
}

.text-length .warning {
  color: #ff4d4f;
  margin-left: 0.5rem;
}

.form-textarea {
  min-height: 300px;
}

.text-tools {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
  flex-wrap: wrap;
}

.controls-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.range-control {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.range-control input {
  flex: 1;
}

.range-control span {
  width: 2.5rem;
  text-align: right;
  font-weight: 500;
}

.style-options {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.style-option {
  padding: 0.5rem 1rem;
  background-color: #f5f7fa;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.style-option.active {
  background-color: #1890ff;
  color: white;
}

.generation-controls {
  margin-top: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.checkbox-control {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.result-section {
  margin-top: 2rem;
}

.audio-player {
  padding: 1rem;
  border-radius: 8px;
  background-color: #f5f7fa;
}

.player-controls {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.player-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.5rem;
  width: 3rem;
  height: 3rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #1890ff;
  color: white;
  border-radius: 50%;
}

.progress-bar-container {
  flex: 1;
}

.progress-bar {
  height: 0.5rem;
  background-color: #e8e8e8;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.progress {
  height: 100%;
  background-color: #1890ff;
  width: 0%;
}

.time-display {
  display: flex;
  justify-content: space-between;
  font-size: 0.85rem;
  color: #666;
}

.player-extra-controls {
  display: flex;
  justify-content: flex-end;
}

/* 文件上传模态框样式 沿用之前的样式 */

@media (max-width: 768px) {
  .tts-container {
    grid-template-columns: 1fr;
  }
  
  .controls-grid {
    grid-template-columns: 1fr;
  }
  
  .player-controls {
    flex-direction: column;
  }
  
  .player-btn {
    align-self: center;
  }
}

.primary-btn {
  background-color: #1890ff;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s;
}

.primary-btn:hover {
  background-color: #0c77e3;
}

.primary-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style> 