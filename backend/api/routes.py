"""
API路由定义
"""
from flask import Blueprint, request, jsonify, current_app
import os
import uuid
import werkzeug
import json
from werkzeug.utils import secure_filename

# 导入工具函数
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from utils.ppt_utils import get_ppt_notes, get_ppt_text, add_audio_to_ppt
from utils.subtitle_utils import find_files, get_video_duration, seconds_to_hmsm

# 创建蓝图
api_bp = Blueprint('api', __name__)

# 允许的文件类型
ALLOWED_AUDIO_EXTENSIONS = {'mp3', 'wav', 'ogg'}
ALLOWED_PPT_EXTENSIONS = {'ppt', 'pptx'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mov', 'wmv'}
ALLOWED_TEXT_EXTENSIONS = {'txt', 'doc', 'docx', 'pdf'}

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

# 文件上传处理函数
def save_uploaded_file(file, subfolder=''):
    if file and allowed_file(file.filename, 
                           ALLOWED_AUDIO_EXTENSIONS.union(
                               ALLOWED_PPT_EXTENSIONS).union(
                                   ALLOWED_VIDEO_EXTENSIONS).union(
                                       ALLOWED_TEXT_EXTENSIONS)):
        filename = secure_filename(file.filename)
        # 生成唯一文件名
        unique_filename = f"{uuid.uuid4()}_{filename}"
        upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], subfolder)
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, unique_filename)
        file.save(file_path)
        return file_path, unique_filename
    return None, None

# 状态检查端点
@api_bp.route('/status', methods=['GET'])
def status():
    return jsonify({
        "status": "online",
        "version": "1.0.0"
    })

# 文本转语音端点
@api_bp.route('/tts', methods=['POST'])
def text_to_speech():
    if not request.is_json:
        return jsonify({"error": "请求必须是JSON格式"}), 400
    
    data = request.get_json()
    text = data.get('text')
    voice_id = data.get('voice_id', 'default')
    settings = data.get('settings', {})
    
    if not text:
        return jsonify({"error": "缺少文本内容"}), 400
    
    # 这里应该调用TTS服务，目前返回模拟数据
    # TODO: 实现实际的TTS服务调用
    
    # 模拟处理时间
    import time
    time.sleep(1)
    
    # 生成唯一的文件名
    output_filename = f"{uuid.uuid4()}.mp3"
    output_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'tts', output_filename)
    
    # 确保目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # 在实际应用中，这里会保存生成的音频文件
    # 目前我们只是返回一个模拟的URL
    
    return jsonify({
        "success": True,
        "message": "文本转语音成功",
        "audio_url": f"/static/uploads/tts/{output_filename}",
        "duration": 60,  # 模拟60秒的音频
        "text": text,
        "voice_id": voice_id,
        "settings": settings
    })

# 音频文件上传端点
@api_bp.route('/upload/audio', methods=['POST'])
def upload_audio():
    if 'file' not in request.files:
        return jsonify({"error": "没有文件"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "未选择文件"}), 400
    
    if file and allowed_file(file.filename, ALLOWED_AUDIO_EXTENSIONS):
        file_path, unique_filename = save_uploaded_file(file, 'audio')
        if file_path:
            return jsonify({
                "success": True,
                "message": "音频上传成功",
                "file_path": file_path,
                "filename": unique_filename,
                "audio_url": f"/static/uploads/audio/{unique_filename}"
            })
    
    return jsonify({"error": "不支持的文件类型"}), 400

# 文本文件上传端点
@api_bp.route('/upload/text', methods=['POST'])
def upload_text():
    if 'file' not in request.files:
        return jsonify({"error": "没有文件"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "未选择文件"}), 400
    
    if file and allowed_file(file.filename, ALLOWED_TEXT_EXTENSIONS):
        file_path, unique_filename = save_uploaded_file(file, 'text')
        if file_path:
            # 这里应该解析文本内容
            # 目前简单地读取文本文件内容（仅支持.txt）
            text_content = ""
            if file_path.endswith('.txt'):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text_content = f.read()
                except Exception as e:
                    return jsonify({
                        "success": True,
                        "message": f"文本上传成功，但读取内容失败: {str(e)}",
                        "file_path": file_path,
                        "filename": unique_filename
                    })
            
            return jsonify({
                "success": True,
                "message": "文本上传成功",
                "file_path": file_path,
                "filename": unique_filename,
                "text_content": text_content
            })
    
    return jsonify({"error": "不支持的文件类型"}), 400

# PPT文件上传与处理端点
@api_bp.route('/upload/ppt', methods=['POST'])
def upload_ppt():
    if 'file' not in request.files:
        return jsonify({"error": "没有文件"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "未选择文件"}), 400
    
    if file and allowed_file(file.filename, ALLOWED_PPT_EXTENSIONS):
        file_path, unique_filename = save_uploaded_file(file, 'ppt')
        if file_path:
            # 提取PPT内容
            notes_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'json', f"{unique_filename}_notes.json")
            text_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'json', f"{unique_filename}_text.json")
            
            os.makedirs(os.path.dirname(notes_path), exist_ok=True)
            
            try:
                get_ppt_notes(file_path, notes_path)
                get_ppt_text(file_path, text_path)
                
                with open(notes_path, 'r', encoding='utf-8') as f:
                    notes_data = json.load(f)
                
                with open(text_path, 'r', encoding='utf-8') as f:
                    text_data = json.load(f)
                
                return jsonify({
                    "success": True,
                    "message": "PPT上传成功并已提取内容",
                    "file_path": file_path,
                    "filename": unique_filename,
                    "notes": notes_data,
                    "text": text_data
                })
            except Exception as e:
                return jsonify({
                    "success": True,
                    "message": f"PPT上传成功，但内容提取失败: {str(e)}",
                    "file_path": file_path,
                    "filename": unique_filename
                })
    
    return jsonify({"error": "不支持的文件类型"}), 400

# 添加音频到PPT端点
@api_bp.route('/ppt/add_audio', methods=['POST'])
def add_audio_to_ppt_endpoint():
    if not request.is_json:
        return jsonify({"error": "请求必须是JSON格式"}), 400
    
    data = request.get_json()
    ppt_path = data.get('ppt_path')
    audio_path = data.get('audio_path')
    page_number = data.get('page_number')
    
    if not all([ppt_path, audio_path, page_number]):
        return jsonify({"error": "缺少必要参数"}), 400
    
    # 确保文件存在
    if not os.path.exists(ppt_path) or not os.path.exists(audio_path):
        return jsonify({"error": "文件不存在"}), 404
    
    try:
        page_number = int(page_number)
    except ValueError:
        return jsonify({"error": "页码必须是数字"}), 400
    
    # 创建输出文件名
    filename = os.path.basename(ppt_path)
    save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'output', f"audio_{filename}")
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    # 设置可选参数
    x = data.get('x', 50)
    y = data.get('y', 150)
    width = data.get('width', 100)
    height = data.get('height', 100)
    auto_play = data.get('auto_play', True)
    volume = data.get('volume', 'loud')
    
    # 调用添加音频函数
    result = add_audio_to_ppt(
        ppt_path, audio_path, page_number, save_path,
        x, y, width, height, auto_play, volume
    )
    
    if result:
        return jsonify({
            "success": True,
            "message": "音频已添加到PPT",
            "output_path": save_path,
            "download_url": f"/static/uploads/output/audio_{filename}"
        })
    else:
        return jsonify({"error": "添加音频失败"}), 500

# 视频处理端点
@api_bp.route('/video/duration', methods=['POST'])
def video_duration():
    if 'file' not in request.files:
        return jsonify({"error": "没有文件"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "未选择文件"}), 400
    
    if file and allowed_file(file.filename, ALLOWED_VIDEO_EXTENSIONS):
        file_path, unique_filename = save_uploaded_file(file, 'video')
        if file_path:
            duration = get_video_duration(file_path)
            if duration is not None:
                formatted_duration = seconds_to_hmsm(duration)
                return jsonify({
                    "success": True,
                    "message": "视频时长获取成功",
                    "duration": duration,
                    "formatted_duration": formatted_duration,
                    "file_path": file_path,
                    "filename": unique_filename
                })
            else:
                return jsonify({"error": "无法获取视频时长"}), 500
    
    return jsonify({"error": "不支持的文件类型"}), 400

# 声音样本管理端点
@api_bp.route('/voice/samples', methods=['GET'])
def list_voice_samples():
    # 模拟数据，实际应从数据库或文件系统获取
    samples = [
        {"id": "1", "name": "标准男声", "type": "preset", "language": "中文", "gender": "男", "style": "标准", "preview_url": "/static/samples/male1.mp3"},
        {"id": "2", "name": "标准女声", "type": "preset", "language": "中文", "gender": "女", "style": "标准", "preview_url": "/static/samples/female1.mp3"},
        {"id": "3", "name": "英语男声", "type": "preset", "language": "英文", "gender": "男", "style": "专业", "preview_url": "/static/samples/male2.mp3"},
        {"id": "4", "name": "英语女声", "type": "preset", "language": "英文", "gender": "女", "style": "柔和", "preview_url": "/static/samples/female2.mp3"},
        {"id": "5", "name": "专业讲解", "type": "preset", "language": "中文", "gender": "男", "style": "专业", "preview_url": "/static/samples/male3.mp3"}
    ]
    return jsonify({"samples": samples})

# 录制声音端点
@api_bp.route('/voice/record', methods=['POST'])
def record_voice():
    if 'audio' not in request.files:
        return jsonify({"error": "没有音频文件"}), 400
    
    file = request.files['audio']
    if file.filename == '':
        return jsonify({"error": "未选择文件"}), 400
    
    name = request.form.get('name', '未命名样本')
    language = request.form.get('language', '中文')
    gender = request.form.get('gender', '男')
    style = request.form.get('style', '标准')
    
    if file and allowed_file(file.filename, ALLOWED_AUDIO_EXTENSIONS):
        file_path, unique_filename = save_uploaded_file(file, 'samples')
        if file_path:
            # 这里应该将样本信息保存到数据库
            # TODO: 实现数据库保存
            
            sample_id = str(uuid.uuid4())
            
            return jsonify({
                "success": True,
                "message": "声音样本保存成功",
                "sample": {
                    "id": sample_id,
                    "name": name,
                    "type": "custom",
                    "language": language,
                    "gender": gender,
                    "style": style,
                    "file_path": file_path,
                    "preview_url": f"/static/uploads/samples/{unique_filename}"
                }
            })
    
    return jsonify({"error": "不支持的文件类型"}), 400

# 新增 - 获取课件列表
@api_bp.route('/courses', methods=['GET'])
def list_courses():
    # 模拟数据，实际应从数据库获取
    courses = [
        {
            "id": 1,
            "title": "示例课件1",
            "description": "这是一个示例课件",
            "createTime": "2024-03-20 10:00:00",
            "status": "draft",
            "ppt_path": "/path/to/ppt1.pptx",
            "voice_id": "1"
        },
        {
            "id": 2,
            "title": "示例课件2",
            "description": "这是另一个示例课件",
            "createTime": "2024-03-20 11:00:00",
            "status": "completed",
            "ppt_path": "/path/to/ppt2.pptx",
            "voice_id": "2"
        }
    ]
    return jsonify({"courses": courses})

# 新增 - 创建课件
@api_bp.route('/courses', methods=['POST'])
def create_course():
    if not request.is_json:
        return jsonify({"error": "请求必须是JSON格式"}), 400
    
    data = request.get_json()
    title = data.get('title')
    description = data.get('description', '')
    ppt_path = data.get('ppt_path')
    voice_id = data.get('voice_id')
    
    if not all([title, ppt_path, voice_id]):
        return jsonify({"error": "缺少必要参数"}), 400
    
    # 这里应该将课件信息保存到数据库
    # TODO: 实现数据库保存
    
    # 生成课件ID（实际应用中应由数据库生成）
    course_id = len([1, 2]) + 1  # 模拟自增ID
    
    import datetime
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return jsonify({
        "success": True,
        "message": "课件创建成功",
        "course": {
            "id": course_id,
            "title": title,
            "description": description,
            "createTime": now,
            "status": "draft",
            "ppt_path": ppt_path,
            "voice_id": voice_id
        }
    })

# 新增 - 更新课件
@api_bp.route('/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    if not request.is_json:
        return jsonify({"error": "请求必须是JSON格式"}), 400
    
    data = request.get_json()
    title = data.get('title')
    description = data.get('description', '')
    ppt_path = data.get('ppt_path')
    voice_id = data.get('voice_id')
    
    if not all([title, voice_id]):
        return jsonify({"error": "缺少必要参数"}), 400
    
    # 这里应该更新数据库中的课件信息
    # TODO: 实现数据库更新
    
    import datetime
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return jsonify({
        "success": True,
        "message": "课件更新成功",
        "course": {
            "id": course_id,
            "title": title,
            "description": description,
            "updateTime": now,
            "status": "draft",
            "ppt_path": ppt_path,
            "voice_id": voice_id
        }
    })

# 新增 - 删除课件
@api_bp.route('/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    # 这里应该从数据库中删除课件
    # TODO: 实现数据库删除
    
    return jsonify({
        "success": True,
        "message": f"课件{course_id}已删除"
    })

# 新增 - 生成课件
@api_bp.route('/courses/<int:course_id>/generate', methods=['POST'])
def generate_course(course_id):
    # 这里应该根据课件ID获取相关信息，然后生成带有语音的课件
    # 实际应用中，这可能是一个长时间运行的任务，应该放入队列处理
    
    # 模拟处理时间
    import time
    time.sleep(2)
    
    return jsonify({
        "success": True,
        "message": "课件生成已开始",
        "task_id": str(uuid.uuid4()),
        "status": "processing"
    })

# 新增 - 检查课件生成状态
@api_bp.route('/courses/<int:course_id>/status', methods=['GET'])
def check_course_status(course_id):
    # 这里应该根据课件ID查询其处理状态
    # 实际应用中，应该查询任务队列或数据库
    
    # 模拟课件状态
    import random
    statuses = ["draft", "processing", "completed"]
    status = random.choice(statuses)
    
    progress = random.randint(0, 100) if status == "processing" else (100 if status == "completed" else 0)
    
    return jsonify({
        "success": True,
        "status": status,
        "progress": progress,
        "download_url": "/static/uploads/output/course_1.pptx" if status == "completed" else None
    }) 