<template>
  <div class="voice-replace">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>声音置换与字幕</span>
          <el-button type="primary" @click="openUploadDialog">上传视频</el-button>
        </div>
      </template>

      <!-- 视频列表 -->
      <el-table :data="videoList" style="width: 100%">
        <el-table-column prop="title" label="视频标题" />
        <el-table-column prop="duration" label="时长" width="120" />
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
      
      <div class="empty-tip" v-if="videoList.length === 0">
        <el-empty description="暂无视频，请上传视频文件">
          <el-button type="primary" @click="openUploadDialog">上传视频</el-button>
        </el-empty>
      </div>
    </el-card>

    <!-- 上传视频对话框 -->
    <el-dialog
      v-model="uploadDialogVisible"
      title="上传视频"
      width="50%"
    >
      <el-form :model="uploadForm" label-width="100px">
        <el-form-item label="视频标题">
          <el-input v-model="uploadForm.title" placeholder="请输入视频标题"/>
        </el-form-item>
        <el-form-item label="视频文件">
          <el-upload
            class="video-uploader"
            action="#"
            :auto-upload="false"
            :on-change="handleFileChange"
            :on-exceed="handleExceed"
            :limit="1"
            :file-list="fileList"
          >
            <el-button type="primary">选择视频文件</el-button>
            <template #tip>
              <div class="el-upload__tip">
                支持mp4, mov等格式视频文件，最大50MB
              </div>
            </template>
          </el-upload>
          
          <!-- 上传进度条 -->
          <div v-if="isUploading || uploadFinished" class="upload-progress-container">
            <div class="upload-progress-bar">
              <div class="upload-progress-inner" :style="{ width: `${uploadProgress}%` }"></div>
            </div>
            <div class="upload-progress-info">
              <span v-if="!uploadFinished">{{ uploadProgress }}%</span>
              <span v-else class="upload-success-icon">✓</span>
            </div>
          </div>
          
          <!-- 文件上传状态 -->
          <div v-if="uploadFinished" class="upload-file-info">
            <div class="upload-file-name">
              <i class="el-icon-document"></i>
              <span>{{ uploadedFileName }}</span>
            </div>
            <div class="upload-status">
              <span class="upload-success-text">上传成功</span>
            </div>
          </div>
        </el-form-item>
        <el-form-item label="默认语音">
          <el-select v-model="uploadForm.defaultVoice" placeholder="选择默认语音">
            <el-option
              v-for="item in voiceOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
          <el-button type="primary" plain style="margin-left: 10px" @click="handleTestVoice">测试语音</el-button>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="uploadDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleUploadSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="编辑语音和字幕"
      width="80%"
      top="5vh"
    >
      <div class="editor-container">
        <!-- 视频预览 -->
        <div class="video-preview">
          <video
            v-if="currentVideo.url"
            :src="currentVideo.url"
            controls
            class="video-player"
            ref="videoPlayer"
            @timeupdate="handleTimeUpdate"
          ></video>
          <div v-else class="video-placeholder">
            请上传视频文件
          </div>
          <div class="current-subtitle" v-if="currentSubtitle">
            <div class="subtitle-text">{{ currentSubtitle.text }}</div>
            <div class="subtitle-voice">
              当前语音：{{ getVoiceName(currentSubtitle.voiceId) }}
            </div>
          </div>
        </div>

        <!-- 字幕编辑 -->
        <div class="subtitle-editor">
          <div class="editor-header">
            <h3>字幕编辑</h3>
            <div class="editor-actions">
              <el-button type="success" @click="handleApplyVoiceToAll">应用语音到全部</el-button>
              <el-button type="primary" @click="handleAutoGenerate">自动生成字幕</el-button>
            </div>
          </div>
          <el-table 
            :data="subtitleList" 
            style="width: 100%" 
            height="350"
            :highlight-current-row="true"
            @current-change="handleSubtitleRowChange"
          >
            <el-table-column prop="time" label="时间" width="120" />
            <el-table-column prop="text" label="字幕文本">
              <template #default="scope">
                <el-input
                  v-model="scope.row.text"
                  type="textarea"
                  :rows="2"
                  placeholder="请输入字幕文本"
                />
              </template>
            </el-table-column>
            <el-table-column prop="voice" label="语音" width="220">
              <template #default="scope">
                <div class="voice-selector">
                  <el-select v-model="scope.row.voiceId" placeholder="选择语音">
                    <el-option
                      v-for="item in voiceOptions"
                      :key="item.value"
                      :label="item.label"
                      :value="item.value"
                    />
                  </el-select>
                  <el-button size="small" @click="previewSubtitleVoice(scope.row)" :icon="VideoPlay"></el-button>
                </div>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="120">
              <template #default="scope">
                <el-button size="small" type="danger" @click="deleteSubtitle(scope.$index)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
          <div class="editor-footer">
            <el-button type="primary" @click="addSubtitle">添加字幕</el-button>
            <el-button type="success" @click="previewWithReplacedVoice">预览效果</el-button>
          </div>
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSave">保存</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 预览对话框 -->
    <el-dialog
      v-model="previewDialogVisible"
      title="声音置换预览"
      width="70%"
      center
      destroy-on-close
      @closed="closePreview"
    >
      <div class="preview-content">
        <div class="video-container">
          <video
            v-if="previewVideo.url"
            :src="previewVideo.url"
            controls
            class="preview-player"
            ref="previewVideoRef"
          ></video>
          
          <!-- 字幕覆盖在视频上 -->
          <div class="subtitle-overlay" v-if="isSubtitlesLoaded">
            <div class="subtitle-box" v-if="currentPreviewSubtitle">
              {{ currentPreviewSubtitle }}
            </div>
          </div>
          
          <!-- 加载中提示 -->
          <div class="subtitle-loading-overlay" v-if="!isSubtitlesLoaded">
            <div class="subtitle-loading">加载字幕中...</div>
          </div>
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="closePreview">关闭</el-button>
          <el-button type="success" @click="handleDownload">下载</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { VideoPlay, VideoPause } from '@element-plus/icons-vue'

// 视频列表数据
const videoList = ref([
  {
    id: 1,
    title: '教学视频示例',
    duration: '00:05:30',
    status: 'completed',
    url: 'https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4'
  },
  {
    id: 2,
    title: '英语口语教程',
    duration: '00:03:45',
    status: 'processing'
  }
])

// 上传相关
const uploadDialogVisible = ref(false)
const uploadForm = reactive({
  title: '',
  defaultVoice: '1'
})
const fileList = ref([])

// 上传进度相关
const uploadProgress = ref(0)
const isUploading = ref(false)
const uploadFinished = ref(false)
const uploadedFileName = ref('')

// 对话框相关
const dialogVisible = ref(false)
const currentVideo = reactive({
  id: 0,
  url: '',
  title: ''
})

// 预览相关
const previewDialogVisible = ref(false)
const previewVideo = reactive({
  url: '',
  title: ''
})
const currentPreviewSubtitle = ref('')
const subtitlesData = ref([]) // 存储字幕数据
const isSubtitlesLoaded = ref(false) // 添加字幕加载状态标志
const previewVideoRef = ref(null) // 添加视频元素引用

// 视频播放器引用
const videoPlayer = ref(null)
const currentTime = ref(0)
const currentSubtitle = ref(null)

// 字幕列表
const subtitleList = ref([
  {
    id: 1,
    time: '00:00:00',
    text: '欢迎观看这个教学视频。',
    voiceId: '1',
    endTime: '00:00:05'
  },
  {
    id: 2,
    time: '00:00:05',
    text: '今天我们要学习语音合成技术的基础知识。',
    voiceId: '1',
    endTime: '00:00:10'
  },
  {
    id: 3,
    time: '00:00:10',
    text: '语音合成技术可以将文本转换为自然的语音输出。',
    voiceId: '2',
    endTime: '00:00:15'
  },
  {
    id: 4,
    time: '00:00:15',
    text: '这种技术在教育领域有广泛的应用前景。',
    voiceId: '1',
    endTime: '00:00:20'
  }
])

// 语音选项
const voiceOptions = [
  { value: '1', label: '女声1 (标准普通话)' },
  { value: '2', label: '男声1 (标准普通话)' },
  { value: '3', label: '女声2 (温柔风格)' },
  { value: '4', label: '男声2 (磁性风格)' },
  { value: '5', label: '英语女声' },
  { value: '6', label: '英语男声' }
]

// 获取语音名称
const getVoiceName = (voiceId) => {
  const voice = voiceOptions.find(v => v.value === voiceId)
  return voice ? voice.label : '未知语音'
}

// 状态相关方法
const getStatusType = (status) => {
  const statusMap = {
    processing: 'warning',
    completed: 'success',
    error: 'danger'
  }
  return statusMap[status] || 'info'
}

const getStatusText = (status) => {
  const statusMap = {
    processing: '处理中',
    completed: '已完成',
    error: '错误'
  }
  return statusMap[status] || '未知'
}

// 事件处理方法
const openUploadDialog = () => {
  uploadForm.title = ''
  uploadForm.defaultVoice = '1'
  fileList.value = []
  uploadProgress.value = 0
  isUploading.value = false
  uploadFinished.value = false
  uploadedFileName.value = ''
  uploadDialogVisible.value = true
}

// 处理文件选择事件
const handleFileChange = (file) => {
  if (file && file.raw) {
    // 检查文件类型和大小
    if (beforeUpload(file.raw)) {
      // 开始模拟上传
      simulateUploadProgress()
    }
  }
}

const beforeUpload = (file) => {
  const isVideo = file.type.startsWith('video/')
  const isLt50M = file.size / 1024 / 1024 < 50
  
  if (!isVideo) {
    ElMessage.error('请上传视频文件!')
    return false
  }
  
  if (!isLt50M) {
    ElMessage.error('视频大小不能超过 50MB!')
    return false
  }
  
  // 提取文件名（不含扩展名）作为标题
  const fileName = file.name.split('.').slice(0, -1).join('.')
  if (!uploadForm.title) {
    uploadForm.title = fileName
  }
  
  // 保存文件名用于显示
  uploadedFileName.value = file.name
  
  return true
}

// 模拟上传进度
const simulateUploadProgress = () => {
  isUploading.value = true
  uploadProgress.value = 0
  uploadFinished.value = false
  
  const interval = setInterval(() => {
    if (uploadProgress.value < 100) {
      uploadProgress.value += 2
    } else {
      clearInterval(interval)
      uploadFinished.value = true
      isUploading.value = false
      ElMessage.success('上传成功')
    }
  }, 100)
}

const handleExceed = () => {
  ElMessage.warning('最多只能上传一个视频文件')
}

const handleUploadSuccess = (response, file) => {
  // 不再使用，由模拟上传取代
}

const handleUploadSubmit = () => {
  if (!uploadForm.title) {
    ElMessage.warning('请输入视频标题')
    return
  }
  
  if (!uploadFinished.value && !isUploading.value) {
    ElMessage.warning('请上传视频文件')
    return
  }
  
  ElMessage.success('视频上传成功，开始处理')
  uploadDialogVisible.value = false
  
  // 模拟添加新视频
  const newVideo = {
    id: Date.now(),
    title: uploadForm.title,
    duration: '00:02:30', // 模拟视频时长
    status: 'processing',
    // 使用固定的示例视频URL
    url: 'https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4'
  }
  
  videoList.value.unshift(newVideo)
  
  // 模拟处理完成
  setTimeout(() => {
    const index = videoList.value.findIndex(v => v.id === newVideo.id)
    if (index !== -1) {
      videoList.value[index].status = 'completed'
    }
  }, 3000)
}

const handleEdit = (row) => {
  currentVideo.id = row.id
  currentVideo.title = row.title
  currentVideo.url = row.url || 'https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4'
  dialogVisible.value = true
  
  // 如果是首次编辑且没有字幕，自动请求生成字幕
  if (row.id === 2) {
    setTimeout(() => {
      handleAutoGenerate()
    }, 500)
  }
}

const handlePreview = (row) => {
  // 使用演示视频
  const videoPath = '/assets/vedio/演示视频.mp4'
  previewVideo.url = videoPath
  previewVideo.title = row.title || '演示视频'
  currentPreviewSubtitle.value = ''
  previewDialogVisible.value = true
  
  // 重置字幕状态
  subtitlesData.value = []
  isSubtitlesLoaded.value = false
  
  // 加载SRT字幕
  loadSubtitlesFromSRT()
}

// 解析SRT字幕格式
const parseSRT = (srtContent) => {
  try {
    console.log('开始解析SRT内容，原始内容长度:', srtContent.length)
    const subtitles = []
    // 处理不同操作系统的换行符
    const normalizedContent = srtContent.replace(/\r\n/g, '\n')
    const chunks = normalizedContent.trim().split('\n\n')
    console.log(`分割后得到${chunks.length}个字幕块`)
    
    for (const chunk of chunks) {
      try {
        const lines = chunk.split('\n')
        if (lines.length >= 3) {
          const index = parseInt(lines[0].trim())
          const timeInfo = lines[1].trim()
          // 保留字幕的原始格式，不合并行
          const textLines = lines.slice(2)
          const text = textLines.join('\n').trim()
          
          // 检查时间格式是否正确
          if (!timeInfo.includes(' --> ')) {
            console.warn('时间格式异常:', timeInfo)
            continue
          }
          
          // 解析时间信息 "00:00:00,000 --> 00:00:03,000"
          const times = timeInfo.split(' --> ')
          if (times.length === 2) {
            const startTime = parseTimeString(times[0])
            const endTime = parseTimeString(times[1])
            
            if (isNaN(startTime) || isNaN(endTime)) {
              console.warn('时间解析异常:', times[0], times[1])
              continue
            }
            
            // 添加日志用于排查
            if (index <= 5 || index % 50 === 0) {
              console.log(`字幕#${index}: ${startTime}s --> ${endTime}s "${text.replace(/\n/g, '\\n').substring(0, 30)}${text.length > 30 ? '...' : ''}"`)
            }
            
            subtitles.push({
              index,
              startTime,
              endTime,
              text
            })
          }
        } else {
          console.warn('字幕块格式异常:', chunk)
        }
      } catch (err) {
        console.error('解析字幕块失败:', err, chunk)
      }
    }
    
    console.log(`成功解析了${subtitles.length}条字幕`)
    return subtitles
  } catch (error) {
    console.error('解析字幕文件失败:', error)
    return []
  }
}

// 将SRT格式的时间字符串转换为秒数
const parseTimeString = (timeStr) => {
  try {
    // 格式: "00:00:00,000"
    const cleanTimeStr = timeStr.trim().replace(',', '.')
    const parts = cleanTimeStr.split(':')
    if (parts.length === 3) {
      const hours = parseInt(parts[0])
      const minutes = parseInt(parts[1])
      const seconds = parseFloat(parts[2])
      return hours * 3600 + minutes * 60 + seconds
    }
    return 0
  } catch (error) {
    console.error('解析时间字符串失败:', timeStr, error)
    return 0
  }
}

// 加载SRT字幕
const loadSubtitlesFromSRT = async () => {
  try {
    console.log('开始加载字幕文件...')
    const response = await fetch('/assets/vedio/演示视频.srt')
    if (!response.ok) {
      throw new Error(`无法加载字幕文件: ${response.status} ${response.statusText}`)
    }
    
    const srtContent = await response.text()
    console.log('成功获取字幕文件内容，长度:', srtContent.length)
    
    // 解析SRT字幕
    subtitlesData.value = parseSRT(srtContent)
    
    if (subtitlesData.value.length === 0) {
      throw new Error('字幕解析失败或没有有效字幕')
    }
    
    isSubtitlesLoaded.value = true
    console.log('字幕加载成功，共', subtitlesData.value.length, '条')
    
    // 等待DOM更新并设置视频事件监听
    setTimeout(() => {
      if (previewVideoRef.value) {
        console.log('添加视频时间更新事件监听...')
        previewVideoRef.value.addEventListener('timeupdate', updateSubtitleForPreview)
        
        // 确保视频可以自动播放
        previewVideoRef.value.addEventListener('canplay', () => {
          // 尝试自动播放视频
          previewVideoRef.value.play().catch(error => {
            console.warn('无法自动播放视频:', error)
            // 自动播放失败，等待用户手动播放
          })
        })
      } else {
        console.error('未找到视频元素')
      }
    }, 300)
  } catch (error) {
    console.error('加载字幕出错:', error)
    ElMessage.warning(`字幕加载失败: ${error.message}`)
    isSubtitlesLoaded.value = true // 即使失败也设置为加载完成，以便移除加载提示
  }
}

// 更新预览中的字幕
const updateSubtitleForPreview = (event) => {
  if (!isSubtitlesLoaded.value || subtitlesData.value.length === 0) {
    return
  }
  
  const currentTime = event.target.currentTime
  
  // 查找当前时间应该显示的字幕
  const currentSubtitle = subtitlesData.value.find(
    sub => currentTime >= sub.startTime && currentTime <= sub.endTime
  )
  
  // 只在字幕发生变化时更新
  if (currentSubtitle) {
    if (currentPreviewSubtitle.value !== currentSubtitle.text) {
      console.log(`当前时间${currentTime.toFixed(2)}秒，显示字幕#${currentSubtitle.index}`)
      currentPreviewSubtitle.value = currentSubtitle.text
    }
  } else {
    if (currentPreviewSubtitle.value !== '') {
      console.log(`当前时间${currentTime.toFixed(2)}秒，无匹配字幕`)
      currentPreviewSubtitle.value = ''
    }
  }
}

// 关闭预览时清理事件监听
const closePreview = () => {
  if (previewVideoRef.value) {
    previewVideoRef.value.removeEventListener('timeupdate', updateSubtitleForPreview)
    previewVideoRef.value.pause()
  }
  previewDialogVisible.value = false
  currentPreviewSubtitle.value = ''
  subtitlesData.value = []
  isSubtitlesLoaded.value = false
}

const handleExport = (row) => {
  ElMessageBox.confirm(
    '确定要导出替换声音后的视频和字幕吗？',
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
    '确定要删除该视频吗？此操作不可恢复。',
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    ElMessage.success('删除成功')
    videoList.value = videoList.value.filter(item => item.id !== row.id)
  })
}

const handleAutoGenerate = () => {
  ElMessage.info('正在识别视频语音并生成字幕...')
  
  // 模拟字幕生成
  setTimeout(() => {
    if (currentVideo.id === 2) {
      // 特殊示例：不同的视频生成不同的字幕
      subtitleList.value = [
        { id: 101, time: '00:00:00', text: 'Hello and welcome to this English lesson.', voiceId: '5', endTime: '00:00:05' },
        { id: 102, time: '00:00:05', text: 'Today we\'ll practice some common phrases.', voiceId: '5', endTime: '00:00:10' },
        { id: 103, time: '00:00:10', text: 'Let\'s start with greetings.', voiceId: '5', endTime: '00:00:15' },
        { id: 104, time: '00:00:15', text: 'How are you doing today?', voiceId: '6', endTime: '00:00:20' }
      ]
    }
    
    ElMessage.success('字幕生成成功！')
  }, 2000)
}

const handleTimeUpdate = () => {
  if (!videoPlayer.value) return
  
  currentTime.value = videoPlayer.value.currentTime
  
  // 查找对应当前时间的字幕
  const timeStr = formatTime(currentTime.value)
  const subtitle = subtitleList.value.find(sub => {
    const startTime = timeToSeconds(sub.time)
    const endTime = timeToSeconds(sub.endTime)
    return currentTime.value >= startTime && currentTime.value < endTime
  })
  
  currentSubtitle.value = subtitle
}

// 时间格式转换函数
const formatTime = (seconds) => {
  const h = Math.floor(seconds / 3600)
  const m = Math.floor((seconds % 3600) / 60)
  const s = Math.floor(seconds % 60)
  return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`
}

const timeToSeconds = (timeStr) => {
  if (!timeStr) return 0
  const [h, m, s] = timeStr.split(':').map(Number)
  return h * 3600 + m * 60 + s
}

const handleSubtitleRowChange = (row) => {
  if (!row || !videoPlayer.value) return
  
  // 跳转到对应的视频时间点
  const startTime = timeToSeconds(row.time)
  videoPlayer.value.currentTime = startTime
}

const addSubtitle = () => {
  const lastSubtitle = subtitleList.value[subtitleList.value.length - 1]
  const lastEndTime = lastSubtitle ? lastSubtitle.endTime : '00:00:00'
  const newStartTime = lastEndTime
  
  // 计算新的结束时间（开始时间+5秒）
  const startTimeSeconds = timeToSeconds(newStartTime)
  const endTimeSeconds = startTimeSeconds + 5
  const newEndTime = formatTime(endTimeSeconds)
  
  subtitleList.value.push({
    id: Date.now(),
    time: newStartTime,
    text: '',
    voiceId: uploadForm.defaultVoice,
    endTime: newEndTime
  })
}

const deleteSubtitle = (index) => {
  ElMessageBox.confirm(
    '确定要删除该字幕吗？',
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    subtitleList.value.splice(index, 1)
    ElMessage.success('删除成功')
  })
}

const previewSubtitleVoice = (subtitle) => {
  if (!subtitle.text || !subtitle.voiceId) {
    ElMessage.warning('字幕文本或语音未设置')
    return
  }
  
  ElMessage.success(`播放语音: ${subtitle.text.substring(0, 20)}${subtitle.text.length > 20 ? '...' : ''}`)
  // 实际项目中，这里应调用文本到语音的API
}

const handleApplyVoiceToAll = () => {
  ElMessageBox.prompt(
    '请选择要应用到所有字幕的语音',
    '批量设置语音',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      inputType: 'select',
      inputValue: '1',
      inputPlaceholder: '请选择语音',
      inputOptions: voiceOptions.map(option => ({
        value: option.value,
        label: option.label
      }))
    }
  ).then(({ value }) => {
    if (value) {
      subtitleList.value.forEach(subtitle => {
        subtitle.voiceId = value
      })
      ElMessage.success('已应用语音到所有字幕')
    }
  })
}

const previewWithReplacedVoice = () => {
  ElMessage.info('正在生成预览...')
  setTimeout(() => {
    handlePreview({
      id: currentVideo.id,
      title: currentVideo.title,
      url: currentVideo.url
    })
  }, 1000)
}

const handleSave = () => {
  // 验证字幕是否完整
  const emptySubtitles = subtitleList.value.filter(sub => !sub.text)
  if (emptySubtitles.length > 0) {
    ElMessageBox.confirm(
      '有部分字幕文本为空，确定要保存吗？',
      '警告',
      {
        confirmButtonText: '确定保存',
        cancelButtonText: '返回编辑',
        type: 'warning'
      }
    ).then(() => {
      saveSubtitles()
    })
  } else {
    saveSubtitles()
  }
}

const saveSubtitles = () => {
  ElMessage.success('保存成功')
  dialogVisible.value = false
}

const handleDownload = () => {
  ElMessage.success('开始下载，请稍候...')
  setTimeout(() => {
    ElMessage.success('下载完成')
  }, 2000)
}

const handleTestVoice = () => {
  if (!uploadForm.defaultVoice) {
    ElMessage.warning('请先选择语音')
    return
  }
  
  const testText = '这是一段测试语音，用于展示AI语音合成的效果。'
  ElMessage.success('开始播放测试语音')
  
  // 在实际项目中，这里应当调用语音合成API
}
</script>

<style scoped>
.voice-replace {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.empty-tip {
  margin: 20px 0;
}

.editor-container {
  display: flex;
  gap: 20px;
  height: 550px;
}

.video-preview {
  flex: 1;
  background: #f5f7fa;
  border-radius: 4px;
  overflow: hidden;
  position: relative;
  display: flex;
  flex-direction: column;
}

.video-player {
  width: 100%;
  flex: 1;
  object-fit: contain;
  background: #000;
}

.video-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #909399;
}

.current-subtitle {
  padding: 10px;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  font-size: 16px;
  text-align: center;
  width: 100%;
}

.subtitle-text {
  font-weight: bold;
  margin-bottom: 5px;
}

.subtitle-voice {
  font-size: 12px;
  color: #ccc;
}

.subtitle-editor {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.editor-actions {
  display: flex;
  gap: 10px;
}

.editor-footer {
  margin-top: 10px;
  display: flex;
  justify-content: space-between;
}

.voice-selector {
  display: flex;
  align-items: center;
  gap: 5px;
}

.preview-content {
  display: flex;
  flex-direction: column;
}

.video-container {
  position: relative;
  width: 100%;
  max-height: 450px;
  background-color: #000;
}

.preview-player {
  width: 100%;
  max-height: 450px;
  object-fit: contain;
}

.subtitle-overlay {
  position: absolute;
  bottom: 70px;
  left: 0;
  right: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 10;
  pointer-events: none; /* 允许点击穿透到视频 */
  padding: 0 20px;
}

.subtitle-loading-overlay {
  position: absolute;
  bottom: 50px;
  left: 0;
  right: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 10;
}

.subtitle-box {
  background-color: transparent;
  color: white;
  padding: 12px 20px;
  font-size: 22px;
  font-weight: bold;
  line-height: 1.5;
  text-align: center;
  max-width: 90%;
  min-width: 60%;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 1), 
               -2px -2px 4px rgba(0, 0, 0, 1),
               2px -2px 4px rgba(0, 0, 0, 1),
               -2px 2px 4px rgba(0, 0, 0, 1);
  border: none;
  box-shadow: none;
  word-break: break-word;
  white-space: pre-line; /* 保留换行符 */
}

.subtitle-loading {
  background-color: rgba(0, 0, 0, 0.5);
  color: #fff;
  font-size: 14px;
  padding: 5px 10px;
  border-radius: 4px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.upload-progress-container {
  margin-top: 15px;
  margin-bottom: 15px;
  display: flex;
  position: relative;
  width: 100%;
  height: 24px;
}

.upload-progress-bar {
  height: 24px;
  background-color: #f0f0f0;
  border-radius: 12px;
  overflow: hidden;
  flex: 1;
  position: relative;
}

.upload-progress-inner {
  height: 100%;
  background: linear-gradient(90deg, #409eff, #67c23a);
  transition: width 0.3s ease;
  border-radius: 12px;
}

.upload-progress-info {
  position: absolute;
  right: 10px;
  top: 0;
  height: 24px;
  line-height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1;
  color: #fff;
  font-weight: bold;
}

.upload-success-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  background-color: #67c23a;
  color: white;
  border-radius: 50%;
  font-weight: bold;
}

.upload-file-info {
  margin-top: 15px;
  padding: 10px;
  border-radius: 4px;
  background-color: #f9f9f9;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.upload-file-name {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #333;
}

.upload-status {
  display: flex;
  align-items: center;
  gap: 5px;
}

.upload-success-text {
  color: #67c23a;
  font-size: 14px;
  font-weight: 500;
  display: flex;
  align-items: center;
}

.upload-success-text:before {
  content: "✓";
  display: inline-block;
  margin-right: 4px;
  font-weight: bold;
}
</style> 