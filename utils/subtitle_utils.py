"""
字幕处理相关工具函数
"""

import os
from moviepy import VideoFileClip

def find_files(path, suffix):
    """
    用来获取path下的所有suffix格式文件
    @params:
        path     - Required  : 目标路径 (str)
        suffix   - Required  : 文件格式 (str)
    @return:
        文件路径列表 (list)
    """
    files = []
    for root, dirs, files_list in os.walk(path):
        for file in files_list:
            if file.endswith('.' + suffix):
                files.append(os.path.abspath(os.path.join(root, file)))
    return files

def get_video_duration(video_path):
    """
    使用 moviepy 获取视频时长（秒）
    @params:
        video_path - Required  : 视频文件路径 (str)
    @return:
        视频时长（秒） (float)
    """
    try:
        clip = VideoFileClip(video_path)
        duration = clip.duration
        clip.close()
        return duration
    except Exception as e:
        print(f"获取视频时长时发生错误: {e}")
        return None

def seconds_to_hmsm(seconds):
    """
    输入一个秒数，输出为H:M:S:M时间格式
    @params:
        seconds   - Required  : 秒 (float)
    @return:
        格式化的时间字符串，如: 00:01:23,456 (str)
    """
    hours = str(int(seconds // 3600))
    minutes = str(int((seconds % 3600) // 60))
    seconds_value = seconds % 60
    # 使用round函数修复浮点数精度问题
    milliseconds = str(int(round((seconds_value - int(seconds_value)) * 1000)))
    seconds_str = str(int(seconds_value))
    
    # 补0
    if len(hours) < 2:
        hours = '0' + hours
    if len(minutes) < 2:
        minutes = '0' + minutes
    if len(seconds_str) < 2:
        seconds_str = '0' + seconds_str
    if len(milliseconds) < 3:
        milliseconds = '0' * (3 - len(milliseconds)) + milliseconds
    
    return f"{hours}:{minutes}:{seconds_str},{milliseconds}" 