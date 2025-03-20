"""
测试PPT工具函数
"""
import os
import sys
import json
import unittest

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.ppt_utils import get_ppt_notes, get_ppt_text, add_audio_to_ppt

class TestPptUtils(unittest.TestCase):
    def setUp(self):
        # 测试用的PPT文件路径
        self.ppt_path = "python_get_ppt_text/test.ppt"
        self.audio_path = "python_get_ppt_text/sample-3s.wav"
        
        # 输出文件路径
        self.output_dir = "test/output"
        os.makedirs(self.output_dir, exist_ok=True)
        self.notes_output = os.path.join(self.output_dir, "测试备注.json")
        self.text_output = os.path.join(self.output_dir, "测试文本.json")
        self.ppt_with_audio = os.path.join(self.output_dir, "测试带音频.pptx")

    def test_get_ppt_notes(self):
        """测试从PPT中提取备注"""
        get_ppt_notes(self.ppt_path, self.notes_output)
        
        # 验证输出文件是否存在
        self.assertTrue(os.path.exists(self.notes_output))
        
        # 验证JSON内容是否正确
        with open(self.notes_output, 'r', encoding='utf-8') as f:
            notes_data = json.load(f)
            
        # 验证结果是一个列表
        self.assertIsInstance(notes_data, list)
        
        # 验证每个元素都有page和content字段
        for item in notes_data:
            self.assertIn('page', item)
            self.assertIn('content', item)
            
    def test_get_ppt_text(self):
        """测试从PPT中提取文本"""
        get_ppt_text(self.ppt_path, self.text_output)
        
        # 验证输出文件是否存在
        self.assertTrue(os.path.exists(self.text_output))
        
        # 验证JSON内容是否正确
        with open(self.text_output, 'r', encoding='utf-8') as f:
            text_data = json.load(f)
            
        # 验证结果是一个列表
        self.assertIsInstance(text_data, list)
        
        # 验证每个元素都有page和content字段
        for item in text_data:
            self.assertIn('page', item)
            self.assertIn('content', item)
            
    def test_add_audio_to_ppt(self):
        """测试向PPT添加音频"""
        result = add_audio_to_ppt(
            self.ppt_path, 
            self.audio_path, 
            1,  # 第一页
            self.ppt_with_audio
        )
        
        # 验证函数返回True表示成功
        self.assertTrue(result)
        
        # 验证输出文件是否存在
        self.assertTrue(os.path.exists(self.ppt_with_audio))
        
    def tearDown(self):
        # 测试完成后可以删除生成的文件
        # 为了保留测试结果以便查看，这里注释掉了删除操作
        """
        if os.path.exists(self.notes_output):
            os.remove(self.notes_output)
        if os.path.exists(self.text_output):
            os.remove(self.text_output)
        if os.path.exists(self.ppt_with_audio):
            os.remove(self.ppt_with_audio)
        """
        pass

if __name__ == "__main__":
    unittest.main() 