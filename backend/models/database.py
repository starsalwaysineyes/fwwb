"""
数据库模型定义
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

def generate_uuid():
    return str(uuid.uuid4())

class User(db.Model):
    """用户模型"""
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联
    voice_samples = db.relationship('VoiceSample', backref='owner', lazy=True)
    tts_requests = db.relationship('TTSRequest', backref='user', lazy=True)

class VoiceSample(db.Model):
    """声音样本模型"""
    __tablename__ = 'voice_samples'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(20), nullable=False, default='custom')  # male, female, custom
    file_path = db.Column(db.String(255), nullable=False)
    preview_url = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 外键
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    # 关联
    tts_requests = db.relationship('TTSRequest', backref='voice_sample', lazy=True)

class TTSRequest(db.Model):
    """TTS请求记录模型"""
    __tablename__ = 'tts_requests'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    text = db.Column(db.Text, nullable=False)
    output_path = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending, processing, completed, failed
    settings = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    # 外键
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    voice_sample_id = db.Column(db.String(36), db.ForeignKey('voice_samples.id'), nullable=False)

class PPTFile(db.Model):
    """PPT文件模型"""
    __tablename__ = 'ppt_files'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    notes_path = db.Column(db.String(255), nullable=True)
    text_path = db.Column(db.String(255), nullable=True)
    output_path = db.Column(db.String(255), nullable=True)
    total_slides = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 外键
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    # 关联
    slides = db.relationship('PPTSlide', backref='ppt_file', lazy=True)

class PPTSlide(db.Model):
    """PPT幻灯片模型"""
    __tablename__ = 'ppt_slides'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    slide_number = db.Column(db.Integer, nullable=False)
    text_content = db.Column(db.Text, nullable=True)
    notes_content = db.Column(db.Text, nullable=True)
    audio_path = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 外键
    ppt_id = db.Column(db.String(36), db.ForeignKey('ppt_files.id'), nullable=False)
    tts_request_id = db.Column(db.String(36), db.ForeignKey('tts_requests.id'), nullable=True) 