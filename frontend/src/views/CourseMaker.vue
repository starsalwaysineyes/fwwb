<template>
  <div class="course-maker">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>课件制作</span>
          <el-button type="primary" @click="handleCreateCourse">新建课件</el-button>
        </div>
      </template>
      
      <!-- 课件列表 -->
      <el-table :data="courseList" style="width: 100%">
        <el-table-column prop="title" label="课件标题" />
        <el-table-column prop="createTime" label="创建时间" width="180" />
        <el-table-column prop="status" label="状态" width="120">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="300">
          <template #default="scope">
            <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button size="small" type="primary" @click="handlePreview(scope.row)">预览</el-button>
            <el-button size="small" type="success" @click="handleExport(scope.row)">导出</el-button>
            <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 新建/编辑课件对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'create' ? '新建课件' : '编辑课件'"
      width="60%"
    >
      <el-form :model="courseForm" label-width="100px">
        <el-form-item label="课件标题">
          <el-input v-model="courseForm.title" placeholder="请输入课件标题" />
        </el-form-item>
        <el-form-item label="课件描述">
          <el-input
            v-model="courseForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入课件描述"
          />
        </el-form-item>
        <el-form-item label="上传PPT">
          <el-upload
            class="upload-demo"
            action="/api/upload"
            :on-success="handleUploadSuccess"
            :before-upload="beforeUpload"
            :file-list="fileList"
          >
            <el-button type="primary">点击上传</el-button>
            <template #tip>
              <div class="el-upload__tip">
                支持.pptx, .ppt格式文件，大小3M~20M
              </div>
            </template>
          </el-upload>
        </el-form-item>
        <el-form-item label="语音设置">
          <el-select v-model="courseForm.voiceId" placeholder="请选择语音">
            <el-option
              v-for="item in voiceOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
          <el-button type="primary" plain style="margin-left: 10px" @click="handleTestVoice">测试语音</el-button>
        </el-form-item>
        <el-form-item label="语速设置">
          <el-slider 
            v-model="courseForm.speed" 
            :min="0.5" 
            :max="2.0" 
            :step="0.1" 
            :marks="{0.5:'慢', 1.0:'正常', 1.5:'快', 2.0:'很快'}"
          ></el-slider>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 课件预览对话框 -->
    <el-dialog
      v-model="previewVisible"
      title="课件预览"
      width="80%"
      top="5vh"
    >
      <div class="preview-container">
        <div class="slide-container">
          <div class="slide-controls">
            <el-button type="primary" :icon="ArrowLeft" @click="prevSlide" :disabled="currentSlide <= 0"></el-button>
            <span>{{ currentSlide + 1 }} / {{ slides.length }}</span>
            <el-button type="primary" :icon="ArrowRight" @click="nextSlide" :disabled="currentSlide >= slides.length - 1"></el-button>
          </div>
          <div class="slide-view">
            <div v-if="slides.length > 0" class="slide">
              <img :src="slides[currentSlide]" alt="slide" />
            </div>
            <div v-else class="slide-placeholder">
              <p>无可用预览</p>
            </div>
          </div>
        </div>
        <div class="audio-container">
          <div class="audio-title">{{ currentCourse?.title }} - 语音讲解</div>
          <div class="audio-controls">
            <el-button type="primary" :icon="VideoPlay" @click="playAudio" :disabled="isPlaying">播放</el-button>
            <el-button type="warning" :icon="VideoPause" @click="pauseAudio" :disabled="!isPlaying">暂停</el-button>
            <el-progress :percentage="audioProgress" :format="formatProgress"></el-progress>
          </div>
          <div class="audio-text">
            <p>当前幻灯片解说文本：</p>
            <div class="text-content">{{ currentSlideText }}</div>
          </div>
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="previewVisible = false">关闭</el-button>
          <el-button type="success" @click="handleDownload">下载课件</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowLeft, ArrowRight, VideoPlay, VideoPause } from '@element-plus/icons-vue'

// 课件列表数据
const courseList = ref([
  {
    id: 1,
    title: '人工智能导论',
    createTime: '2024-03-20 10:00:00',
    status: 'completed',
    slides: [
      'https://via.placeholder.com/800x450.png?text=AI+Introduction+Slide+1',
      'https://via.placeholder.com/800x450.png?text=AI+Introduction+Slide+2',
      'https://via.placeholder.com/800x450.png?text=AI+Introduction+Slide+3'
    ],
    slidesText: [
      '人工智能是计算机科学的一个分支，它关注于创造能够模拟人类智能行为的机器。',
      '机器学习是人工智能的一个子领域，它使用数据和算法来模仿人类学习过程。',
      '深度学习是机器学习的一种特殊形式，基于人工神经网络结构。'
    ]
  },
  {
    id: 2,
    title: '语音合成技术介绍',
    createTime: '2024-03-20 11:00:00',
    status: 'processing'
  }
])

// 对话框相关
const dialogVisible = ref(false)
const dialogType = ref('create')
const courseForm = reactive({
  title: '',
  description: '',
  voiceId: '',
  speed: 1.0,
  pptFile: null
})

// 预览相关
const previewVisible = ref(false)
const currentCourse = ref(null)
const currentSlide = ref(0)
const isPlaying = ref(false)
const audioProgress = ref(0)
const fileList = ref([])

// 计算属性
const slides = computed(() => currentCourse.value?.slides || [])
const currentSlideText = computed(() => {
  if (!currentCourse.value?.slidesText) return ''
  return currentCourse.value.slidesText[currentSlide.value] || ''
})

// 语音选项
const voiceOptions = [
  { value: '1', label: '女声1 (标准普通话)' },
  { value: '2', label: '男声1 (标准普通话)' },
  { value: '3', label: '女声2 (温柔风格)' },
  { value: '4', label: '男声2 (磁性风格)' },
  { value: '5', label: '英语女声' },
  { value: '6', label: '英语男声' }
]

// 状态相关方法
const getStatusType = (status) => {
  const statusMap = {
    draft: 'info',
    processing: 'warning',
    completed: 'success'
  }
  return statusMap[status] || 'info'
}

const getStatusText = (status) => {
  const statusMap = {
    draft: '草稿',
    processing: '处理中',
    completed: '已完成'
  }
  return statusMap[status] || '未知'
}

// 事件处理方法
const handleCreateCourse = () => {
  dialogType.value = 'create'
  courseForm.title = ''
  courseForm.description = ''
  courseForm.voiceId = ''
  courseForm.speed = 1.0
  fileList.value = []
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogType.value = 'edit'
  Object.assign(courseForm, row)
  dialogVisible.value = true
}

const handlePreview = (row) => {
  currentCourse.value = row
  currentSlide.value = 0
  audioProgress.value = 0
  isPlaying.value = false
  previewVisible.value = true
}

const handleExport = (row) => {
  ElMessageBox.confirm(
    '确定要导出该课件吗？将生成带语音讲解的完整PPT文件。',
    '导出确认',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'info'
    }
  ).then(() => {
    ElMessage.success('导出成功，正在下载...')
    // 模拟下载
    setTimeout(() => {
      ElMessage.success('下载完成')
    }, 2000)
  })
}

const handleDelete = (row) => {
  ElMessageBox.confirm(
    '确定要删除该课件吗？此操作不可恢复。',
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    ElMessage.success('删除成功')
  })
}

const handleUploadSuccess = (response, file) => {
  courseForm.pptFile = file
  ElMessage.success('上传成功')
}

const beforeUpload = (file) => {
  const isPPT = file.type === 'application/vnd.openxmlformats-officedocument.presentationml.presentation' ||
                file.type === 'application/vnd.ms-powerpoint'
  const isLt20M = file.size / 1024 / 1024 < 20
  const isGt3M = file.size / 1024 / 1024 > 3
  
  if (!isPPT) {
    ElMessage.error('只能上传PPT文件!')
    return false
  }
  
  if (!isLt20M) {
    ElMessage.error('文件大小不能超过20MB!')
    return false
  }
  
  if (!isGt3M) {
    ElMessage.warning('建议文件大小不小于3MB，以确保内容完整')
  }
  
  return isPPT && isLt20M
}

const handleSubmit = () => {
  if (!courseForm.title) {
    ElMessage.warning('请输入课件标题')
    return
  }
  
  if (!courseForm.voiceId) {
    ElMessage.warning('请选择语音')
    return
  }
  
  ElMessage.success(dialogType.value === 'create' ? '创建成功' : '更新成功')
  dialogVisible.value = false
  
  if (dialogType.value === 'create') {
    // 模拟创建新课件
    const newCourse = {
      id: Date.now(),
      title: courseForm.title,
      createTime: new Date().toLocaleString(),
      status: 'processing'
    }
    courseList.value.unshift(newCourse)
    
    // 模拟处理完成
    setTimeout(() => {
      const index = courseList.value.findIndex(item => item.id === newCourse.id)
      if (index !== -1) {
        courseList.value[index].status = 'completed'
        // 添加模拟幻灯片
        courseList.value[index].slides = [
          'https://via.placeholder.com/800x450.png?text=Slide+1+' + courseForm.title,
          'https://via.placeholder.com/800x450.png?text=Slide+2+' + courseForm.title,
          'https://via.placeholder.com/800x450.png?text=Slide+3+' + courseForm.title
        ]
        courseList.value[index].slidesText = [
          '这是第一张幻灯片的自动生成文本。基于您上传的PPT内容，AI将提取关键信息并转换为语音。',
          '这是第二张幻灯片的自动生成文本。您可以在编辑界面中修改这些文本，以确保语音内容符合您的需求。',
          '这是最后一张幻灯片的自动生成文本。您可以调整语速和语音风格，以获得最佳的教学效果。'
        ]
      }
    }, 3000)
  }
}

// 预览控制
const prevSlide = () => {
  if (currentSlide.value > 0) {
    currentSlide.value--
  }
}

const nextSlide = () => {
  if (currentSlide.value < slides.value.length - 1) {
    currentSlide.value++
  }
}

const playAudio = () => {
  isPlaying.value = true
  
  // 模拟播放进度
  const interval = setInterval(() => {
    audioProgress.value += 1
    if (audioProgress.value >= 100) {
      clearInterval(interval)
      isPlaying.value = false
      
      // 自动播放下一张幻灯片
      if (currentSlide.value < slides.value.length - 1) {
        setTimeout(() => {
          nextSlide()
          audioProgress.value = 0
        }, 1000)
      }
    }
  }, 100)
}

const pauseAudio = () => {
  isPlaying.value = false
}

const formatProgress = (percentage) => {
  const totalSeconds = 30 // 假设每张幻灯片的音频长度为30秒
  const currentSeconds = Math.floor(totalSeconds * percentage / 100)
  const minutes = Math.floor(currentSeconds / 60)
  const seconds = currentSeconds % 60
  return `${minutes}:${seconds.toString().padStart(2, '0')}`
}

const handleDownload = () => {
  ElMessage.success('开始下载，请稍候...')
  setTimeout(() => {
    ElMessage.success('下载完成')
  }, 2000)
}

const handleTestVoice = () => {
  if (!courseForm.voiceId) {
    ElMessage.warning('请先选择语音')
    return
  }
  
  const testText = '这是一段测试语音，用于展示AI语音合成的效果。您可以通过调整语速来改变语音的播放速度。'
  ElMessage.success('开始播放测试语音')
  
  // 在实际项目中，这里应当调用语音合成API
}
</script>

<style scoped>
.course-maker {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.upload-demo {
  width: 100%;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.preview-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.slide-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.slide-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 15px;
}

.slide-view {
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  overflow: hidden;
  background-color: #f5f7fa;
  height: 450px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.slide img {
  max-width: 100%;
  max-height: 450px;
  display: block;
  margin: 0 auto;
}

.slide-placeholder {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  color: #909399;
  font-size: 16px;
}

.audio-container {
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  padding: 15px;
  background-color: #f5f7fa;
}

.audio-title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 10px;
}

.audio-controls {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 15px;
}

.audio-controls .el-progress {
  flex: 1;
  margin-left: 10px;
}

.audio-text {
  background-color: white;
  padding: 10px;
  border-radius: 4px;
}

.text-content {
  padding: 10px;
  background-color: #f0f9ff;
  border-left: 3px solid #1890ff;
  margin-top: 5px;
  font-size: 14px;
  line-height: 1.5;
}
</style> 