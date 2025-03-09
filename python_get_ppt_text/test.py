from spire.presentation import *
from spire.presentation.common import *
import json
import aspose.slides as slides

def get_ppt_notes(pptpath,outputpath):
    # 创建 Presentation 类的对象
    pres = Presentation()

    # 加载 PowerPoint 演示文稿
    pres.LoadFromFile(pptpath)

    notes_list = []
    # 循环遍历每个幻灯片
    for i, slide in enumerate(pres.Slides, 1):
        # 获取备注幻灯片
        notes_slide = slide.NotesSlide
        # 获取备注内容
        try:
            notes = notes_slide.NotesTextFrame.Text
            notes_list.append({"page": i, "content": notes})
        except:
            notes_list.append({"page": i, "content": ""})

    # 将备注写入JSON文件
    with open(outputpath, "w", encoding="utf-8") as f:
        json.dump(notes_list, f, ensure_ascii=False, indent=4)
    pres.Dispose()



# 获取幻灯片文本
def get_ppt_text(pptpath,outputpath):
    
    pres = Presentation()
    pres.LoadFromFile(pptpath)
    text_list = []
    
    for i, slide in enumerate(pres.Slides, 1):
        slide_text = []
        for shape in slide.Shapes:
            if isinstance(shape, IAutoShape):
                for paragraph in shape.TextFrame.Paragraphs:
                    slide_text.append(paragraph.Text)
        text_list.append({
            "page": i,
            "content": "\n".join(slide_text)
        })
    
    with open(outputpath, "w", encoding='utf-8') as f:
        json.dump(text_list, f, ensure_ascii=False, indent=4)
    pres.Dispose()



def add_audio_to_ppt(ppt_path, audio_path, page_number, save_path, x=50, y=150, width=100, height=100, auto_play=True, volume="loud"):
    """
    向PPT中插入音频
    :param ppt_path: PPT文件路径
    :param audio_path: 音频文件路径
    :param page_number: 要插入的页码（从1开始）
    :param save_path: 保存路径
    :param x: 音频图标x坐标位置
    :param y: 音频图标y坐标位置
    :param width: 音频图标宽度
    :param height: 音频图标高度
    :param auto_play: 是否自动播放
    :param volume: 音量大小，可选值："loud"（大）, "medium"（中）, "low"（小）, "mute"（静音）
    """
    try:
        # 加载演示文稿
        with slides.Presentation(ppt_path) as presentation:
            # 检查页码是否有效
            if page_number < 1 or page_number > len(presentation.slides):
                raise ValueError(f"页码 {page_number} 无效，PPT总页数为 {len(presentation.slides)}")
            
            # 获取指定页
            slide = presentation.slides[page_number - 1]
            
            # 加载音频文件
            with open(audio_path, "rb") as audio_file:
                # 添加音频帧
                audio_frame = slide.shapes.add_audio_frame_embedded(x, y, width, height, audio_file)
                
                # 设置播放模式
                if auto_play:
                    audio_frame.play_mode = slides.AudioPlayModePreset.AUTO
                else:
                    audio_frame.play_mode = slides.AudioPlayModePreset.ON_CLICK
                
                # 设置音量
                volume_map = {
                    "loud": slides.AudioVolumeMode.LOUD,
                    "medium": slides.AudioVolumeMode.MEDIUM,
                    "low": slides.AudioVolumeMode.LOW,
                    "mute": slides.AudioVolumeMode.MUTE
                }
                audio_frame.volume = volume_map.get(volume.lower(), slides.AudioVolumeMode.MEDIUM)
            
            # 保存演示文稿
            presentation.save(save_path, slides.export.SaveFormat.PPTX)
            return True
    except Exception as e:
        print(f"插入音频时发生错误: {str(e)}")
        return False

if __name__ == "__main__":
    get_ppt_text("./test.ppt","./output/幻灯片文本.json")
    get_ppt_notes("./test.ppt","./output/备注文本.json")
    add_audio_to_ppt("./test.ppt","./sample-3s.wav",3,"./output/test.pptx")

