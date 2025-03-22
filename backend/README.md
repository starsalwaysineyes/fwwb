# AI语音合成教学软件后端

这是基于Flask的AI语音合成教学软件后端服务。

## 功能特点

- 文本转语音API
- 声音样本管理
- PPT文件处理
- 视频处理支持
- 用户管理系统

## 安装与设置

### 前提条件

- Python 3.8+
- pip（Python包管理器）

### 安装步骤

1. 克隆项目到本地

2. 安装依赖
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. 设置环境变量（可选）
   ```bash
   # Windows
   set FLASK_CONFIG=development
   
   # Linux/Mac
   export FLASK_CONFIG=development
   ```

4. 运行应用
   ```bash
   python run.py
   ```

应用将在 http://localhost:5000 启动。

## API文档

### 文本转语音

**POST** `/api/tts`

请求体:
```json
{
  "text": "要转换的文本内容",
  "voice_id": "样本ID",
  "settings": {
    "speed": 1.0,
    "pitch": 1.0,
    "volume": 1.0
  }
}
```

### 上传音频

**POST** `/api/upload/audio`

表单数据:
- `file`: 音频文件

### 上传PPT

**POST** `/api/upload/ppt`

表单数据:
- `file`: PPT文件

### 添加音频到PPT

**POST** `/api/ppt/add_audio`

请求体:
```json
{
  "ppt_path": "PPT文件路径",
  "audio_path": "音频文件路径",
  "page_number": 1,
  "x": 50,
  "y": 150,
  "width": 100,
  "height": 100,
  "auto_play": true,
  "volume": "loud"
}
```

### 获取视频时长

**POST** `/api/video/duration`

表单数据:
- `file`: 视频文件

## 开发指南

### 项目结构

```
backend/
  ├── api/
  │   └── routes.py      # API路由
  ├── config/
  │   └── config.py      # 配置文件
  ├── models/
  │   └── database.py    # 数据库模型
  ├── static/
  │   └── uploads/       # 上传文件存储
  ├── templates/         # HTML模板
  ├── __init__.py        # 应用初始化
  ├── app.py             # 应用入口
  ├── run.py             # 启动脚本
  └── requirements.txt   # 依赖列表
```

### 环境变量

- `FLASK_CONFIG`: 配置环境 (development, testing, production)
- `SECRET_KEY`: 应用密钥
- `DATABASE_URL`: 数据库连接URL
- `TTS_SERVICE_URL`: TTS服务URL

## 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull请求 