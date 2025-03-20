<template>
  <div class="voice-replace">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>语音替换</span>
          <el-button type="primary" @click="handleUploadVideo">上传视频</el-button>
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
    </el-card>

    <!-- 编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="编辑语音"
      width="70%"
    >
      <div class="editor-container">
        <!-- 视频预览 -->
        <div class="video-preview">
          <video
            v-if="currentVideo.url"
            :src="currentVideo.url"
            controls
            class="video-player"
          ></video>
          <div v-else class="video-placeholder">
            请上传视频文件
          </div>
        </div>

        <!-- 字幕编辑 -->
        <div class="subtitle-editor">
          <div class="editor-header">
            <h3>字幕编辑</h3>
            <el-button type="primary" @click="handleAutoGenerate">自动生成字幕</el-button>
          </div>
          <el-table :data="subtitleList" style="width: 100%">
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
            <el-table-column prop="voice" label="语音" width="150">
              <template #default="scope">
                <el-select v-model="scope.row.voiceId" placeholder="选择语音">
                  <el-option
                    v-for="item in voiceOptions"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value"
                  />
                </el-select>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSave">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

// 视频列表数据
const videoList = ref([
  {
    id: 1,
    title: '示例视频1',
    duration: '00:05:30',
    status: 'processing'
  },
  {
    id: 2,
    title: '示例视频2',
    duration: '00:03:45',
    status: 'completed'
  }
])

// 对话框相关
const dialogVisible = ref(false)
const currentVideo = reactive({
  url: '',
  title: ''
})

// 字幕列表
const subtitleList = ref([
  {
    time: '00:00:00',
    text: '示例字幕1',
    voiceId: '1'
  },
  {
    time: '00:00:05',
    text: '示例字幕2',
    voiceId: '2'
  }
])

// 语音选项
const voiceOptions = [
  { value: '1', label: '女声1' },
  { value: '2', label: '男声1' },
  { value: '3', label: '女声2' }
]

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
const handleUploadVideo = () => {
  ElMessage.info('上传功能开发中')
}

const handleEdit = (row) => {
  currentVideo.title = row.title
  currentVideo.url = 'https://example.com/video.mp4' // 示例URL
  dialogVisible.value = true
}

const handlePreview = (row) => {
  ElMessage.info('预览功能开发中')
}

const handleExport = (row) => {
  ElMessage.success('导出成功')
}

const handleDelete = (row) => {
  ElMessageBox.confirm(
    '确定要删除该视频吗？',
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

const handleAutoGenerate = () => {
  ElMessage.info('自动生成字幕功能开发中')
}

const handleSave = () => {
  ElMessage.success('保存成功')
  dialogVisible.value = false
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

.editor-container {
  display: flex;
  gap: 20px;
  height: 500px;
}

.video-preview {
  flex: 1;
  background: #f5f7fa;
  border-radius: 4px;
  overflow: hidden;
}

.video-player {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.video-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #909399;
}

.subtitle-editor {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style> 