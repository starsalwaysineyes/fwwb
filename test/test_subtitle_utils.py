"""
测试字幕工具函数
"""
import os
import sys
import unittest
import tempfile

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.subtitle_utils import find_files, get_video_duration, seconds_to_hmsm

class TestSubtitleUtils(unittest.TestCase):
    def setUp(self):
        # 创建临时目录和文件用于测试
        self.temp_dir = tempfile.mkdtemp()
        
        # 创建测试文件
        self.mp4_files = []
        for i in range(3):
            file_path = os.path.join(self.temp_dir, f"test{i}.mp4")
            with open(file_path, 'w') as f:
                f.write("测试文件内容")
            self.mp4_files.append(file_path)
            
        # 创建其他格式文件
        self.txt_file = os.path.join(self.temp_dir, "test.txt")
        with open(self.txt_file, 'w') as f:
            f.write("测试文本文件")
            
        # 视频文件路径（用于测试视频时长函数）
        self.video_path = "python_add_subtitle/example"  # 应该包含.mp4文件
        
    def test_find_files(self):
        """测试查找文件函数"""
        # 测试查找mp4文件
        found_mp4 = find_files(self.temp_dir, "mp4")
        self.assertEqual(len(found_mp4), 3)
        
        # 测试查找txt文件
        found_txt = find_files(self.temp_dir, "txt")
        self.assertEqual(len(found_txt), 1)
        
        # 测试查找不存在的格式
        found_none = find_files(self.temp_dir, "avi")
        self.assertEqual(len(found_none), 0)
        
    def test_seconds_to_hmsm(self):
        """测试秒转换为时分秒毫秒格式"""
        # 测试整数秒
        self.assertEqual(seconds_to_hmsm(3661), "01:01:01,000")
        
        # 测试带小数的秒
        self.assertEqual(seconds_to_hmsm(3661.5), "01:01:01,500")
        
        # 测试小于1小时的时间
        self.assertEqual(seconds_to_hmsm(125.75), "00:02:05,750")
        
        # 测试小于1分钟的时间
        self.assertEqual(seconds_to_hmsm(45.123), "00:00:45,123")
        
    def test_get_video_duration(self):
        """测试获取视频时长"""
        # 注意：这个测试需要实际的视频文件才能运行
        # 这里我们只测试函数能否正常返回
        # 首先尝试查找一个实际存在的视频文件
        video_files = []
        if os.path.exists(self.video_path):
            video_files = find_files(self.video_path, "mp4")
        
        # 如果找到视频文件，测试时长获取
        if video_files:
            duration = get_video_duration(video_files[0])
            # 检查返回值是否是浮点数或None
            self.assertTrue(duration is None or isinstance(duration, float))
        else:
            print("警告：未找到视频文件，跳过视频时长测试")
            
    def tearDown(self):
        # 删除测试过程中创建的临时文件
        for file_path in self.mp4_files:
            if os.path.exists(file_path):
                os.remove(file_path)
                
        if os.path.exists(self.txt_file):
            os.remove(self.txt_file)
            
        # 删除临时目录
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)

if __name__ == "__main__":
    unittest.main() 