import whisper
import os
import datetime
import time
from zhconv import convert  # 简繁体转换
from tqdm import tqdm
from moviepy import VideoFileClip

# 获取mp4文件列表
def find_files(path, suffix):
    """
    用来获取path下的所有suffix格式文件
    @params:
        path     - Required  : 目标路径 (str)
        suffix   - Required  : 视频文件格式 (str)
    """
    mp4_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.' + suffix):
                mp4_files.append(os.path.abspath(os.path.join(root, file)))
    return mp4_files

def get_video_duration(video_path):
    """
    使用 moviepy 获取视频时长（秒）。
    """
    try:
        clip = VideoFileClip(video_path)
        duration = clip.duration
        clip.close()  
        return duration
    except Exception as e:
        print(f"Error getting duration with moviepy: {e}")
        return None

# 秒转时分秒毫秒
def seconds_to_hmsm(seconds):
    """
    输入一个秒数，输出为H:M:S:M时间格式
    @params:
        seconds   - Required  : 秒 (float)
    """
    hours = str(int(seconds // 3600))
    minutes = str(int((seconds % 3600) // 60))
    seconds = seconds % 60
    milliseconds = str(int(int((seconds - int(seconds)) * 1000)))  # 毫秒留三位
    seconds = str(int(seconds))
    # 补0
    if len(hours) < 2:
        hours = '0' + hours
    if len(minutes) < 2:
        minutes = '0' + minutes
    if len(seconds) < 2:
        seconds = '0' + seconds
    if len(milliseconds) < 3:
        milliseconds = '0' * (3 - len(milliseconds)) + milliseconds
    return f"{hours}:{minutes}:{seconds},{milliseconds}"

def main():
    # 主文件夹
    file_path = r'python_add_subtitle\example'
    mp4_files = find_files(file_path, suffix='mp4')
    
    # 获取模型
    model = whisper.load_model('small')

    for file in tqdm(mp4_files):
        # 字幕文件保存路径
        # xxx.mp4 --> xxx. + srt
        # 如果是其他格式，如mpweg需要改一下，这里因为都是mp4就直接对字符串切片了
        save_file = file[:-3] + "srt"
        # 判断文件是否存在，存在则说明已经有字幕，跳出不识别
        if os.path.exists(save_file):
            time.sleep(0.01)
            continue
        # 获取当前视频识别开始时间
        start_time = datetime.datetime.now()
        print('正在识别：{} --{}'.format('\\'.join(file.split('\\')[2:]), start_time.strftime('%Y-%m-%d %H:%M:%S')))
        # 获取视频时长
        try:  # 添加 try-except 块来处理可能出现的错误
            duration = get_video_duration(file)
            if duration is None:
                print("无法获取视频时长，跳过该视频。")
                continue  # 跳过当前视频
            duration_hmsm = seconds_to_hmsm(duration)  #将浮点型的秒数转换为时间字符串
            print('视频时长：{}'.format(duration_hmsm))
        except Exception as e:
            print(f"处理视频时长时出错: {e}")
            continue #跳过当前视频
    
        # 文字识别
        res = model.transcribe(file, fp16=False, language='Chinese')
    
        # 写入字幕文件
        with open(save_file, 'w', encoding='utf-8') as f:
            i = 1
            for r in res['segments']:
                f.write(str(i) + '\n')
                f.write(seconds_to_hmsm(float(r['start'])) + ' --> ' + seconds_to_hmsm(float(r['end'])) + '\n')
                i += 1
                f.write(convert(r['text'], 'zh-cn') + '\n')  # 结果可能是繁体，转为简体zh-cn
                f.write('\n')
        # 获取当前视频识别结束时间
        end_time = datetime.datetime.now()
        print('完成识别：{} --{}'.format('\\'.join(file.split('\\')[2:]), end_time.strftime('%Y-%m-%d %H:%M:%S')))
        print('花费时间:', end_time - start_time)

if __name__ == "__main__":
    main()