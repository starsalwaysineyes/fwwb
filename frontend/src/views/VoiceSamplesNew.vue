<!-- 声音样本库页面 -->
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
          <button class="btn-close" @click="closeAddSampleModal">×</button>
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
                  <input type="file" id="audio-file" accept="audio/*" class="file-input" @change="handleFileChange">
                  <label for="audio-file" class="file-label">
                    <span>{{ selectedFileName || '选择文件' }}</span>
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
          <button class="btn btn-secondary" @click="closeAddSampleModal">取消</button>
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
import { ref, computed, onMounted } from 'vue'
import { assetManager } from '../components/AssetManager'

// 数据模型
const samples = ref([
  { id: 1, name: '标准男声', type: 'preset', language: '中文', gender: '男', style: '标准', audioUrl: '/assets/标准男声.wav' },
  { id: 2, name: '标准女声', type: 'preset', language: '中文', gender: '女', style: '标准', audioUrl: '/assets/标准女声.wav' },
  { id: 3, name: '英语男声', type: 'preset', language: '英文', gender: '男', style: '标准', audioUrl: '/assets/英语男声.wav' },
  { id: 4, name: '英语女声', type: 'preset', language: '英文', gender: '女', style: '标准', audioUrl: '/assets/英语女声.wav' }
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
const recordedBlob = ref(null) // 存储录制的音频Blob

// 新样本数据
const newSample = ref({
  name: '',
  language: '中文',
  gender: '男',
  style: '标准'
})

// 文件上传相关
const selectedFileName = ref('')
const selectedFile = ref(null)

// 应用加载时初始化数据
onMounted(async () => {
  await initializeAssetManager();
  await loadSamplesData();
  
  // 确保移除所有专业讲解样本
  removeAllProfessionalSamples();
})

// 初始化资源管理器
async function initializeAssetManager() {
  console.log('初始化资源管理器...');
  await assetManager.init();
  console.log('可用音频文件:', assetManager.getAvailableFiles());
}

// 加载样本数据
async function loadSamplesData() {
  // 1. 先加载配置文件中的样本
  const customSamples = await assetManager.loadSampleConfig();
  
  // 2. 如果配置文件中有样本，则合并到样本列表
  if (customSamples && customSamples.length > 0) {
    const presetSamples = samples.value.filter(s => s.type === 'preset');
    samples.value = [...presetSamples, ...customSamples];
    console.log('从配置文件加载了自定义样本:', customSamples.length);
    return;
  }
  
  // 3. 如果配置文件中没有样本，则扫描assets目录寻找音频文件
  console.log('配置文件中没有样本，开始扫描目录...');
  const files = assetManager.getAvailableFiles();
  
  // 4. 将找到的音频文件创建为样本
  const newSamples = [];
  const maxId = Math.max(...samples.value.map(s => s.id), 0);
  
  for (const file of files) {
    // 检查文件是否已存在于样本列表中
    const audioUrl = assetManager.getFileUrl(file);
    const existingSample = samples.value.find(s => s.audioUrl === audioUrl);
    
    // 排除专业讲解类型的文件
    if (file === '专业讲解.wav') {
      continue;
    }
    
    if (!existingSample) {
      // 从文件名创建样本
      const name = file.replace('.wav', '');
      
      // 排除专业讲解类型的样本
      if (name === '专业讲解') {
        continue;
      }
      
      newSamples.push({
        id: maxId + newSamples.length + 1,
        name: name,
        type: 'custom',
        language: '中文', // 默认值
        gender: '未知',   // 默认值
        style: '标准',    // 默认值
        audioUrl: audioUrl,
        createTime: new Date().toISOString(),
        source: 'auto-scan'
      });
    }
  }
  
  if (newSamples.length > 0) {
    // 添加到样本列表
    samples.value = [...samples.value, ...newSamples];
    console.log(`从目录扫描发现${newSamples.length}个新样本`);
    
    // 保存样本配置
    await saveSamplesConfig();
  }
}

// 保存样本配置
async function saveSamplesConfig() {
  // 筛选自定义样本
  const customSamples = samples.value.filter(s => s.type === 'custom');
  
  if (customSamples.length > 0) {
    // 保存到配置文件
    await assetManager.saveSampleConfig(customSamples);
    console.log(`保存了${customSamples.length}个自定义样本配置`);
  }
}

// 处理文件选择事件
function handleFileChange(event) {
  const file = event.target.files[0]
  if (file) {
    selectedFileName.value = file.name
    selectedFile.value = file
    // 如果用户没有输入样本名称，自动使用文件名(不含扩展名)
    if (!newSample.value.name) {
      newSample.value.name = file.name.split('.').slice(0, -1).join('.')
    }
  } else {
    selectedFileName.value = ''
    selectedFile.value = null
  }
}

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

// 播放样本
function playSample(sample) {
  // 构建音频文件路径，优先使用sample中的audioUrl，如果没有则尝试从assets文件夹加载同名文件
  let audioPath = sample.audioUrl;
  
  if (!audioPath) {
    // 使用样本名称在assets文件夹中查找同名wav文件
    audioPath = assetManager.getFileUrl(`${sample.name}.wav`);
  }
  
  if (audioPlayer.value) {
    audioPlayer.value.src = audioPath;
    audioPlayer.value.onerror = () => {
      console.error(`无法加载音频: ${audioPath}`);
      alert(`无法播放"${sample.name}"的音频样本`);
    };
    audioPlayer.value.onloadeddata = () => {
      audioPlayer.value.play().catch(err => {
        console.error('播放失败:', err);
        alert(`播放"${sample.name}"失败`);
      });
    };
  } else {
    alert('音频播放器未初始化');
  }
}

function editSample(sample) {
  alert(`编辑示例：这里会打开编辑 ${sample.name} 的界面`)
}

function confirmDelete(sample) {
  sampleToDelete.value = sample
  showDeleteModal.value = true
}

async function deleteSample() {
  if (sampleToDelete.value) {
    // 如果有关联的音频文件，先删除文件
    if (sampleToDelete.value.audioUrl) {
      const fileName = sampleToDelete.value.audioUrl.split('/').pop();
      await assetManager.deleteFile(fileName);
    }
    
    // 删除样本数据
    samples.value = samples.value.filter(s => s.id !== sampleToDelete.value.id);
    
    // 保存更新后的样本配置
    await saveSamplesConfig();
    
    showDeleteModal.value = false;
    sampleToDelete.value = null;
  }
}

async function addSample() {
  // 生成新ID
  const id = Math.max(...samples.value.map(s => s.id), 0) + 1;
  
  // 默认不设置audioUrl
  let audioUrl = null;
  let isSuccess = false;
  
  // 根据当前活动的标签页处理文件
  if (activeTab.value === 'upload' && selectedFile.value) {
    // 上传音频文件处理 - 将文件重命名并保存到assets目录
    const fileName = `${newSample.value.name}.wav`;
    audioUrl = assetManager.getFileUrl(fileName);
    
    // 上传文件
    isSuccess = await assetManager.uploadFile(selectedFile.value, fileName);
    
    if (!isSuccess) {
      alert('上传文件失败，请重试');
      return;
    }
  } 
  else if (activeTab.value === 'record' && recordedBlob.value) {
    // 录制音频处理 - 将录制的音频保存到assets目录
    const fileName = `${newSample.value.name}.wav`;
    audioUrl = assetManager.getFileUrl(fileName);
    
    // 在真实应用中，这里会将录制的Blob转换为文件并上传
    const file = new File([recordedBlob.value], fileName, { type: 'audio/wav' });
    isSuccess = await assetManager.uploadFile(file, fileName);
    
    if (!isSuccess) {
      alert('保存录音失败，请重试');
      return;
    }
  }
  
  // 添加新样本
  const newSampleData = {
    id,
    ...newSample.value,
    type: 'custom',
    audioUrl: audioUrl,
    createTime: new Date().toISOString(),
    source: activeTab.value === 'upload' ? 'upload' : 'record'
  };
  
  samples.value.push(newSampleData);
  
  // 保存更新后的样本配置
  await saveSamplesConfig();
  
  // 重置表单
  newSample.value = {
    name: '',
    language: '中文',
    gender: '男',
    style: '标准'
  };
  
  // 重置文件选择
  selectedFileName.value = '';
  selectedFile.value = null;
  const fileInput = document.getElementById('audio-file');
  if (fileInput) {
    fileInput.value = '';
  }
  
  // 重置录音
  recordedBlob.value = null;
  hasRecording.value = false;
  
  showAddSampleModal.value = false;
  activeTab.value = 'upload';
}

function startRecording() {
  isRecording.value = true;
  recordingTime.value = 0;
  
  // 重置之前的录音
  recordedBlob.value = null;
  
  // 模拟录制计时
  const timer = setInterval(() => {
    recordingTime.value++;
    if (recordingTime.value >= 30) {
      clearInterval(timer);
      stopRecording();
    }
  }, 1000);
  
  // 实际应用中，这里会调用浏览器的录音API
  // 例如:
  /*
  navigator.mediaDevices.getUserMedia({ audio: true })
    .then(stream => {
      const mediaRecorder = new MediaRecorder(stream);
      const audioChunks = [];
      
      mediaRecorder.addEventListener('dataavailable', event => {
        audioChunks.push(event.data);
      });
      
      mediaRecorder.addEventListener('stop', () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        recordedBlob.value = audioBlob;
      });
      
      mediaRecorder.start();
      // 存储mediaRecorder引用以便停止时使用
    });
  */
  
  console.log('开始录制声音样本');
}

function stopRecording() {
  isRecording.value = false;
  hasRecording.value = true;
  
  // 实际应用中，这里会停止录音并处理录制好的音频
  // 例如:
  /*
  mediaRecorder.stop();
  stream.getTracks().forEach(track => track.stop());
  */
  
  // 模拟生成录音Blob
  // 在真实应用中，这个Blob会在mediaRecorder的stop事件中生成
  setTimeout(() => {
    // 模拟产生一个空的音频Blob
    recordedBlob.value = new Blob([], { type: 'audio/wav' });
  }, 500);
  
  console.log('停止录制声音样本');
}

function playRecording() {
  // 实际应用中，这里会播放刚刚录制的声音
  if (recordedBlob.value && audioPlayer.value) {
    const url = URL.createObjectURL(recordedBlob.value);
    audioPlayer.value.src = url;
    audioPlayer.value.play()
      .catch(err => {
        console.error('播放录音失败:', err);
        alert('播放录音失败');
      });
  } else {
    alert('没有可播放的录音');
  }
}

function closeAddSampleModal() {
  // 重置表单
  newSample.value = {
    name: '',
    language: '中文',
    gender: '男',
    style: '标准'
  };
  
  // 重置文件选择
  selectedFileName.value = '';
  selectedFile.value = null;
  const fileInput = document.getElementById('audio-file');
  if (fileInput) {
    fileInput.value = '';
  }
  
  // 重置录音
  recordedBlob.value = null;
  hasRecording.value = false;
  
  showAddSampleModal.value = false;
  activeTab.value = 'upload';
}

// 移除所有专业讲解样本
function removeAllProfessionalSamples() {
  // 过滤掉所有名称为"专业讲解"或风格为"专业"的样本
  samples.value = samples.value.filter(sample => 
    !(sample.name === '专业讲解' || sample.style === '专业')
  );
  
  console.log('已移除所有专业讲解样本');
  
  // 保存更新后的样本配置
  saveSamplesConfig();
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

.toolbar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}

.btn {
  background-color: #1890ff;
  color: white;
  border: none;
  padding: 0.5rem 1.25rem;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-secondary {
  background-color: #f5f7fa;
  color: #666;
}

.btn-danger {
  background-color: #ff4d4f;
  color: white;
}

.form-input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  outline: none;
}

.form-input:focus {
  border-color: #1890ff;
}

.form-group {
  margin-bottom: 1rem;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
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