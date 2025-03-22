"""
应用启动文件
"""
import os
from backend import create_app

# 根据环境变量选择配置
config_name = os.environ.get('FLASK_CONFIG') or 'default'
app = create_app(config_name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 