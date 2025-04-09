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
      width="70%"
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
          <div class="upload-container">
            <input 
              type="file" 
              ref="fileInput" 
              style="display: none" 
              accept=".ppt,.pptx" 
              @change="handleFileChange" 
            />
            <el-button type="primary" @click="triggerFileInput">点击上传</el-button>
            <div class="el-upload__tip">
              支持.pptx, .ppt格式文件，大小1M~20M
            </div>
          
            <!-- 自定义上传进度条 -->
            <div v-if="uploadStatus.showProgress" class="custom-upload-progress">
              <div class="progress-bar">
                <div class="progress-inner" :style="{width: uploadStatus.percent + '%'}"></div>
              </div>
              <div class="progress-info">
                <span v-if="!uploadStatus.success">{{ uploadStatus.percent }}%</span>
                <span v-else class="success-icon">✓</span>
              </div>
            </div>
            
            <!-- 文件信息 -->
            <div v-if="uploadStatus.success" class="file-info">
              <div class="file-name">{{ uploadedFileName }}</div>
              <div class="file-status">上传成功</div>
            </div>
          </div>
        </el-form-item>
        <el-form-item v-if="currentCourse?.slides?.length" label="PPT预览">
          <div class="ppt-preview">
            <div class="preview-slides">
              <div class="slide-controls">
                <el-button 
                  type="primary" 
                  size="small" 
                  :icon="ArrowLeft" 
                  @click="prevPreviewSlide" 
                  :disabled="currentPreviewSlide <= 0 || !currentCourse?.slides?.length"
                ></el-button>
                <span v-if="currentCourse?.slides?.length">
                  {{ currentPreviewSlide + 1 }} / {{ currentCourse.slides.length }}
                </span>
                <span v-else>0 / 0</span>
                <el-button 
                  type="primary" 
                  size="small" 
                  :icon="ArrowRight" 
                  @click="nextPreviewSlide" 
                  :disabled="!currentCourse?.slides?.length || currentPreviewSlide >= currentCourse.slides.length - 1"
                ></el-button>
              </div>
              <div class="slide-preview">
                <template v-if="currentCourse?.slides?.length">
                  <img 
                    :src="currentCourse.slides[currentPreviewSlide]" 
                    :alt="`幻灯片预览 ${currentPreviewSlide + 1}`"
                    @load="handleImageLoad(currentPreviewSlide)"
                    @error="handleImageError(currentPreviewSlide)"
                    v-show="!imageStates[currentPreviewSlide]?.loading && !imageStates[currentPreviewSlide]?.error"
                  />
                  <div v-if="imageStates[currentPreviewSlide]?.loading" class="image-loading">
                    <el-icon class="el-icon--loading"></el-icon>
                    <span style="margin-top: 10px">加载中...</span>
                  </div>
                  <div v-if="imageStates[currentPreviewSlide]?.error" class="image-error">
                    <el-icon><circle-close /></el-icon>
                    <span style="margin-top: 10px">图片加载失败</span>
                    <span style="margin-top: 5px; font-size: 12px">请确认PPT已正确处理并生成预览图片</span>
                  </div>
                </template>
                <div v-else class="image-error">
                  <span>无可用预览</span>
                </div>
              </div>
            </div>
            <div class="preview-text">
              <p class="preview-text-title">当前页内容：</p>
              <div class="preview-text-content">
                {{ currentCourse.slidesText[currentPreviewSlide] || '无内容' }}
              </div>
            </div>
          </div>
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
      :before-close="handleClosePreview"
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
              <img 
                :src="slides[currentSlide]" 
                :alt="`幻灯片 ${currentSlide + 1}`"
                @load="handlePreviewImageLoad(currentSlide)"
                @error="handlePreviewImageError(currentSlide)"
                v-show="!previewImageStates[currentSlide]?.loading && !previewImageStates[currentSlide]?.error"
              />
              <div v-if="previewImageStates[currentSlide]?.loading" class="image-loading">
                <el-icon class="el-icon--loading"></el-icon>
                <span style="margin-top: 10px">加载中...</span>
              </div>
              <div v-if="previewImageStates[currentSlide]?.error" class="image-error">
                <el-icon><circle-close /></el-icon>
                <span style="margin-top: 10px">图片加载失败</span>
                <span style="margin-top: 5px; font-size: 12px">请确认PPT已正确处理并生成预览图片</span>
              </div>
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
import { ArrowLeft, ArrowRight, VideoPlay, VideoPause, CircleClose } from '@element-plus/icons-vue'

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
const currentPreviewSlide = ref(0)
const isPlaying = ref(false)
const audioProgress = ref(0)
const fileList = ref([])
const fileInput = ref(null) // 文件上传输入引用
const uploadedFileName = ref('') // 已上传的文件名

// 上传状态
const uploadStatus = reactive({
  showProgress: false,
  percent: 0,
  success: false
})

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
  currentCourse.value = null
  currentPreviewSlide.value = 0
  
  // 重置上传状态
  uploadStatus.showProgress = false
  uploadStatus.percent = 0
  uploadStatus.success = false
  uploadedFileName.value = ''
  
  // 清空文件输入
  if (fileInput.value) {
    fileInput.value.value = ''
  }
  
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogType.value = 'edit'
  Object.assign(courseForm, row)
  
  // 重置上传状态
  uploadStatus.showProgress = false
  uploadStatus.percent = 0
  uploadStatus.success = false
  uploadedFileName.value = ''
  
  // 清空文件输入
  if (fileInput.value) {
    fileInput.value.value = ''
  }
  
  dialogVisible.value = true
}

const handlePreview = (row) => {
  currentCourse.value = row
  currentSlide.value = 0
  audioProgress.value = 0
  isPlaying.value = false
  previewVisible.value = true
  
  // 从assets目录加载预览图片
  loadPreviewImagesFromAssets(row.title)
    .catch(error => {
      console.error('加载预览图片时出错:', error)
      ElMessage.error('加载预览图片时出错')
    })
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
  currentCourse.value = null
  currentPreviewSlide.value = 0
  
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

// 上传预览控制
const prevPreviewSlide = () => {
  if (currentPreviewSlide.value > 0) {
    currentPreviewSlide.value--
  }
}

const nextPreviewSlide = () => {
  if (currentPreviewSlide.value < currentCourse.value?.slides?.length - 1) {
    currentPreviewSlide.value++
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

const triggerFileInput = () => {
  // 触发文件输入点击
  fileInput.value.click()
}

const handleFileChange = (event) => {
  const file = event.target.files[0]
  if (!file) return

  // 验证文件类型和大小
  const isPPT = file.name.endsWith('.ppt') || file.name.endsWith('.pptx')
  const isLt20M = file.size / 1024 / 1024 < 20
  const isGt1M = file.size / 1024 / 1024 > 1

  if (!isPPT) {
    ElMessage.error('只能上传PPT文件!')
    return
  }

  if (!isLt20M) {
    ElMessage.error('文件大小不能超过20MB!')
    return
  }

  if (!isGt1M) {
    ElMessage.warning('建议文件大小不小于1MB，以确保内容完整')
  }

  // 开始模拟上传
  uploadStatus.showProgress = true
  uploadStatus.percent = 0
  uploadStatus.success = false
  uploadedFileName.value = file.name

  // 模拟上传进度
  const simulateUpload = () => {
    const interval = setInterval(() => {
      uploadStatus.percent += 10
      if (uploadStatus.percent >= 100) {
        clearInterval(interval)
        
        // 上传完成
        uploadStatus.success = true
        
        // 提取文件名（不含扩展名）作为课件标题
        if (!courseForm.title || courseForm.title.trim() === '') {
          const nameWithoutExt = file.name.replace(/\.(pptx|ppt)$/i, '')
          courseForm.title = nameWithoutExt
          console.log('已提取文件名:', nameWithoutExt)
        }
        
        // 保存文件对象到表单
        courseForm.pptFile = file
        
        // 显示上传成功消息
        ElMessage.success('上传成功')
        
        // 从assets目录加载预览图片
        loadPptPreviewImages(file.name)
          .catch(error => {
            console.error('加载预览图片时出错:', error)
            ElMessage.error('加载预览图片时出错')
          })
      }
    }, 300)
  }

  // 启动模拟上传
  simulateUpload()
}

// 添加加载PPT预览图片的函数
const loadPptPreviewImages = async (fileName) => {
  // 获取不带扩展名的文件名
  const nameWithoutExt = fileName.replace(/\.(pptx|ppt)$/i, '')
  
  // 创建预览幻灯片数组
  const previewSlides = []
  const previewTexts = []
  
  try {
    // 尝试加载对应的content.json文件
    const response = await fetch(`/assets/${nameWithoutExt}/content.json`)
    let slideContents = {}
    
    if (response.ok) {
      slideContents = await response.json()
      console.log('成功加载content.json文件:', slideContents)
    } else {
      console.warn('无法加载content.json文件，将使用默认文本')
    }
    
    // 根据实际目录结构获取预览图片
    // 图片命名格式为 "文件名_page_001.png", "文件名_page_002.png" 等
    const totalPages = 6 // 假设最多6页，实际应用中应从服务器获取
    
    for (let i = 1; i <= totalPages; i++) {
      const pageNum = i.toString().padStart(3, '0')
      const imagePath = `/assets/${nameWithoutExt}/${nameWithoutExt}_page_${pageNum}.png`
      previewSlides.push(imagePath)
      
      // 使用content.json中的文本(如果存在)，否则使用默认文本
      const slideText = slideContents[i] || `第${i}页PPT内容 (实际应用中将从PPT中提取文本)`
      previewTexts.push(slideText)
      
      // 设置图片初始加载状态
      imageStates.value[i-1] = { loading: true, error: false }
    }
    
    // 更新预览对象
    currentCourse.value = {
      title: nameWithoutExt,
      slides: previewSlides,
      slidesText: previewTexts
    }
    
    // 重置预览索引
    currentPreviewSlide.value = 0
    
  } catch (error) {
    console.error('加载content.json时出错:', error)
    ElMessage.warning('无法加载幻灯片内容，将使用默认文本')
    
    // 使用默认文本继续处理
    const totalPages = 6
    for (let i = 1; i <= totalPages; i++) {
      const pageNum = i.toString().padStart(3, '0')
      const imagePath = `/assets/${nameWithoutExt}/${nameWithoutExt}_page_${pageNum}.png`
      previewSlides.push(imagePath)
      previewTexts.push(`第${i}页PPT内容 (默认文本)`)
      
      // 设置图片初始加载状态
      imageStates.value[i-1] = { loading: true, error: false }
    }
    
    // 更新预览对象
    currentCourse.value = {
      title: nameWithoutExt,
      slides: previewSlides,
      slidesText: previewTexts
    }
    
    // 重置预览索引
    currentPreviewSlide.value = 0
  }
}

const imageStates = ref({})

const handleImageLoad = (index) => {
  imageStates.value[index] = { loading: false, error: false }
}

const handleImageError = (index) => {
  imageStates.value[index] = { loading: false, error: true }
}

// 从assets目录加载预览图片的函数
const loadPreviewImagesFromAssets = async (title) => {
  if (!title) return
  
  // 创建预览幻灯片数组
  const previewSlides = []
  const previewTexts = []
  
  try {
    // 尝试加载对应的content.json文件
    const response = await fetch(`/assets/${title}/content.json`)
    let slideContents = {}
    
    if (response.ok) {
      slideContents = await response.json()
      console.log('成功加载content.json文件:', slideContents)
    } else {
      console.warn('无法加载content.json文件，将使用默认文本')
    }
    
    // 根据课件标题获取预览图片
    // 图片命名格式为 "标题_page_001.png", "标题_page_002.png" 等
    const totalPages = 6 // 假设最多6页，实际应用中应从服务器获取
    
    for (let i = 1; i <= totalPages; i++) {
      const pageNum = i.toString().padStart(3, '0')
      const imagePath = `/assets/${title}/${title}_page_${pageNum}.png`
      previewSlides.push(imagePath)
      
      // 设置图片初始加载状态
      previewImageStates.value[i-1] = { loading: true, error: false }
      
      // 使用content.json中的文本(如果存在)，否则使用原有或默认文本
      let slideText = ''
      if (slideContents[i]) {
        slideText = slideContents[i]
      } else if (currentCourse.value && currentCourse.value.slidesText && currentCourse.value.slidesText[i-1]) {
        slideText = currentCourse.value.slidesText[i-1]
      } else {
        slideText = `第${i}页幻灯片内容 (自动生成)`
      }
      previewTexts.push(slideText)
    }
    
    // 更新当前课件对象
    currentCourse.value = {
      ...currentCourse.value,
      slides: previewSlides,
      slidesText: previewTexts
    }
    
  } catch (error) {
    console.error('加载content.json时出错:', error)
    ElMessage.warning('无法加载幻灯片内容，将使用默认文本')
    
    // 使用默认文本继续处理
    const totalPages = 6
    for (let i = 1; i <= totalPages; i++) {
      const pageNum = i.toString().padStart(3, '0')
      const imagePath = `/assets/${title}/${title}_page_${pageNum}.png`
      previewSlides.push(imagePath)
      
      // 设置图片初始加载状态
      previewImageStates.value[i-1] = { loading: true, error: false }
      
      // 使用原有文本或默认文本
      let slideText = ''
      if (currentCourse.value && currentCourse.value.slidesText && currentCourse.value.slidesText[i-1]) {
        slideText = currentCourse.value.slidesText[i-1]
      } else {
        slideText = `第${i}页幻灯片内容 (默认文本)`
      }
      previewTexts.push(slideText)
    }
    
    // 更新当前课件对象
    currentCourse.value = {
      ...currentCourse.value,
      slides: previewSlides,
      slidesText: previewTexts
    }
  }
}

const previewImageStates = ref({})

const handlePreviewImageLoad = (index) => {
  previewImageStates.value[index] = { loading: false, error: false }
}

const handlePreviewImageError = (index) => {
  previewImageStates.value[index] = { loading: false, error: true }
}

const handleClosePreview = () => {
  // 清理预览状态
  previewVisible.value = false
  currentSlide.value = 0
  audioProgress.value = 0
  isPlaying.value = false
  previewImageStates.value = {}
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
  position: relative;
}

.slide {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

.slide img {
  max-width: 100%;
  max-height: 450px;
  display: block;
  margin: 0 auto;
  object-fit: contain;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
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

.ppt-preview {
  display: flex;
  flex-direction: column;
  gap: 15px;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  padding: 15px;
  background-color: #f5f7fa;
}

.preview-slides {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.slide-preview {
  height: 400px;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: white;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  overflow: hidden;
  position: relative;
}

.slide-preview img {
  max-width: 100%;
  max-height: 400px;
  object-fit: contain;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.slide-preview .image-loading {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: rgba(255, 255, 255, 0.8);
  color: #606266;
}

.slide-preview .image-error {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: rgba(245, 247, 250, 0.9);
  color: #f56c6c;
  font-size: 14px;
  text-align: center;
  padding: 20px;
}

.preview-text {
  background-color: white;
  padding: 10px;
  border-radius: 4px;
}

.preview-text-title {
  font-weight: bold;
  margin-bottom: 5px;
}

.preview-text-content {
  padding: 10px;
  background-color: #f0f9ff;
  border-left: 3px solid #1890ff;
  font-size: 14px;
  line-height: 1.5;
}

.upload-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 100%;
  max-width: 100%;
}

.custom-upload-progress {
  margin-top: 10px;
  display: flex;
  align-items: center;
  width: 100%;
}

.progress-bar {
  width: 100%;
  height: 24px;
  background-color: #f0f0f0;
  border-radius: 12px;
  overflow: hidden;
  flex: 1;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
}

.progress-inner {
  height: 100%;
  background: linear-gradient(to right, #58a8ff, #409eff);
  transition: width 0.3s ease;
}

.progress-info {
  margin-left: 10px;
  font-size: 14px;
  font-weight: bold;
}

.success-icon {
  color: #67c23a;
  font-size: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  background-color: #f0f9eb;
  border-radius: 50%;
  border: 1px solid #67c23a;
}

.file-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 15px;
  background-color: #f0f9eb;
  border-radius: 4px;
  border: 1px solid #e1f3d8;
  margin-top: 10px;
  width: 100%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.file-name {
  font-size: 14px;
  font-weight: bold;
  color: #606266;
  word-break: break-all;
  max-width: 80%;
  display: flex;
  align-items: center;
}

.file-name::before {
  content: "📄";
  margin-right: 8px;
  font-size: 18px;
}

.file-status {
  font-size: 14px;
  color: #67c23a;
  font-weight: bold;
  display: flex;
  align-items: center;
  background-color: white;
  padding: 5px 10px;
  border-radius: 12px;
  border: 1px solid #e1f3d8;
}

.file-status::before {
  content: "✓";
  font-size: 16px;
  margin-right: 5px;
}
</style> 