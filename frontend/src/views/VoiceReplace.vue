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
            action="/api/upload/video"
            :on-success="handleUploadSuccess"
            :before-upload="beforeUpload"
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
    >
      <div class="preview-content">
        <video
          v-if="previewVideo.url"
          :src="previewVideo.url"
          controls
          autoplay
          class="preview-player"
        ></video>
        <div class="subtitle-display">
          <div class="subtitle-box">
            {{ currentPreviewSubtitle }}
          </div>
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="previewDialogVisible = false">关闭</el-button>
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
  uploadDialogVisible.value = true
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
  
  return isVideo && isLt50M
}

const handleExceed = () => {
  ElMessage.warning('最多只能上传一个视频文件')
}

const handleUploadSuccess = (response, file) => {
  ElMessage.success('上传成功')
  // 实际项目中，response会包含上传后的视频URL和其他信息
}

const handleUploadSubmit = () => {
  if (!uploadForm.title) {
    ElMessage.warning('请输入视频标题')
    return
  }
  
  if (fileList.value.length === 0) {
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
    url: URL.createObjectURL(fileList.value[0].raw) // 使用本地Blob URL
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
  previewVideo.url = row.url || 'https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4'
  previewVideo.title = row.title
  currentPreviewSubtitle.value = ''
  previewDialogVisible.value = true
  
  // 模拟字幕显示
  let subtitleIndex = 0
  const subtitleInterval = setInterval(() => {
    if (!previewDialogVisible.value) {
      clearInterval(subtitleInterval)
      return
    }
    
    if (subtitleIndex < subtitleList.value.length) {
      currentPreviewSubtitle.value = subtitleList.value[subtitleIndex].text
      subtitleIndex++
    } else {
      clearInterval(subtitleInterval)
    }
  }, 5000)
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
  gap: 10px;
}

.preview-player {
  width: 100%;
  max-height: 450px;
  object-fit: contain;
}

.subtitle-display {
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 4px;
  min-height: 60px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.subtitle-box {
  background-color: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 10px 20px;
  border-radius: 4px;
  font-size: 16px;
  text-align: center;
  min-width: 60%;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style> 