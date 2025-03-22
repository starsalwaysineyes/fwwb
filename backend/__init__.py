"""
后端应用初始化
"""
from flask import Flask
from flask_cors import CORS
import os

from .models.database import db
from .config.config import config

def create_app(config_name='default'):
    """
    创建Flask应用
    :param config_name: 配置名称，默认为开发环境
    :return: Flask应用实例
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # 确保上传目录存在
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # 初始化扩展
    CORS(app)
    db.init_app(app)
    
    # 注册蓝图
    from .api.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # 根路由
    @app.route('/')
    def index():
        return {
            "message": "欢迎使用AI语音合成教学软件API服务",
            "status": "running"
        }
    
    # 创建数据库表
    with app.app_context():
        db.create_all()
    
    return app 