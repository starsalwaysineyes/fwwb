"""
Flask应用主文件
"""
from flask import Flask
from flask_cors import CORS
import os

# 导入API路由
from api.routes import api_bp

# 创建Flask应用
app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 配置
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/uploads')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 最大50MB上传限制
app.config['SECRET_KEY'] = 'ai_voice_teaching_app_secret_key'  # 用于会话安全

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 注册蓝图
app.register_blueprint(api_bp, url_prefix='/api')

# 根路由
@app.route('/')
def index():
    return {
        "message": "欢迎使用AI语音合成教学软件API服务",
        "status": "running"
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 