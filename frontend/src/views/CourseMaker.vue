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
        <el-table-column label="操作" width="250">
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
          >
            <el-button type="primary">点击上传</el-button>
            <template #tip>
              <div class="el-upload__tip">
                支持.pptx, .ppt格式文件
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
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

// 课件列表数据
const courseList = ref([
  {
    id: 1,
    title: '示例课件1',
    createTime: '2024-03-20 10:00:00',
    status: 'draft'
  },
  {
    id: 2,
    title: '示例课件2',
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
  voiceId: ''
})

// 语音选项
const voiceOptions = [
  { value: '1', label: '女声1' },
  { value: '2', label: '男声1' },
  { value: '3', label: '女声2' }
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
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogType.value = 'edit'
  Object.assign(courseForm, row)
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
    '确定要删除该课件吗？',
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

const handleUploadSuccess = (response) => {
  ElMessage.success('上传成功')
}

const beforeUpload = (file) => {
  const isPPT = file.type === 'application/vnd.openxmlformats-officedocument.presentationml.presentation' ||
                file.type === 'application/vnd.ms-powerpoint'
  if (!isPPT) {
    ElMessage.error('只能上传PPT文件!')
    return false
  }
  return true
}

const handleSubmit = () => {
  if (!courseForm.title) {
    ElMessage.warning('请输入课件标题')
    return
  }
  ElMessage.success(dialogType.value === 'create' ? '创建成功' : '更新成功')
  dialogVisible.value = false
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
</style> 