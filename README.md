## TODO

- [ ] 对应模型和接口（TTS、ocr、音频转文字、数据集）一周

- [ ] 封装调用（封装成函数）2 周

- [ ] UI 界面（绑 button，加字母）1 周

- [ ] 文档和 ppt

- [ ] 演示视频

- [ ] 假装请人试听打分（MOS评分）

  

### TTS

[49K 下载！最强开源语音克隆TTS：本地部署实测，2秒复刻你的声音_f5-tts官网-CSDN博客](https://blog.csdn.net/u010522887/article/details/143247877)

> 支持三种形式：
>
> - TTS：标准的单音色语音克隆；
> - Podcast：多音色克隆：有声读物制作者的福音；
> - Multi-Style：多种说话情绪，例如 Shouting…
> - 实操只需 2 秒音频即可合成超拟人的语音，推理速度优于前段时间和大家分享的：
>   - [FishSpeech 实测，免费语音克隆神器，5分钟部署实战](https://zhuanlan.zhihu.com/p/713552916)
>   - [CosyVoice 实测，阿里开源语音合成模型，3s极速语音克隆，5分钟部署实战](https://blog.csdn.net/u010522887/article/details/141010689)



## 实现

### **（1）声音样本库：**

> 可以预设一些标准声音，也可以通过上传音频文件，或现场录制，如录制老师的声音；音频文件和现场录制建议为5s到30s的单独人声。

#### 预设声音

- edge-tts [edge-tts](https://github.com/rany2/edge-tts)
- [EmotiVoice: EmotiVoice 😊: 多语音和提示控制的 TTS 引擎](https://github.com/netease-youdao/EmotiVoice)
- [GPT-SoVITS: 1 分钟的语音数据也可以用来训练一个好的 TTS 模型！（少量语音克隆)](https://github.com/RVC-Boss/GPT-SoVITS)

#### 上传音频、现场录制（）

用克隆音色，快速响应拟合音色并**保存**？

[CosyVoice2实现音色保存及推理_cosyvoice2 预训练音色-CSDN博客](https://blog.csdn.net/doupoa/article/details/145733331)

[CosyVoice2.0](https://funaudiollm.github.io/cosyvoice2/)

### **（2）个性化语音讲解：**

> 上传或输入一段文本教学内容，长度在800~2000字，选择声音样本库的声音进行语音讲解；

多个音色如何快速切换？

是否需要保存某个已经完成音色模仿的实例？

使用cosyvoice2实现快速学习音色，音色的本地读取加载。

是否存在保留状态的方法，实现某个音色进行学习后的存储？-》使用cosyvoice2，有参考博客 or 假装我们做了存储，实则是提前加载好的（假装读取）。

### **3）标准语言输出：**

> 根据给定的文本内容，长度在800~2000字，输出普通话、英文等标准发音。扩展性要求，可控制语速、语气和节奏等

#### 拓展性要求

语速：edgetts，sogits，emotvoice均可以

语气，节奏(?):emotvoice，cosyvoice2

综上：使用cosyvoice2疑似可以解决所有问题。

### **4）课件制作下载**

> 上传一个小型的教学课件(比如一个PPT)，大小在3M~20M，通过选择声音样本库声音，完成有声课件的制作，可下载；

python实现内容提取，预设两种使用场景：

1：需要自动播报正文-》提取正文并添加自动播放音频

2：需要自动播报备注-》提取备注并自动添加播放音频

#### Python实现提取ppt正文&备注

>[使用Python快速提取PPT中的文本内容_python提取ppt文本-CSDN博客](https://blog.csdn.net/Eiceblue/article/details/136532235)

### **5）可选功能：**声音置换及加字幕功能，导入一段音视频，通过更换声音，实现变声，同步展示字幕。

加字幕：音频转文字，一键生成字幕项目。

#### 音频转文字（生成字幕文件）

>[buxuku/VideoSubtitleGenerator: 批量为本地视频生成字幕文件，并可将字幕文件翻译成其它语言， 跨平台支持 window, mac 系统](https://github.com/buxuku/VideoSubtitleGenerator)
>
>一键生成字幕，保存在视频同目录，可以后续通过合成方式完成合成（演示时无需合成，只需挂载播放）

>确保ffmpeg配置完整
>确保输入视频为mp4格式，时长不宜太长。



变声器：[Releases · RVC-Project/Retrieval-based-Voice-Conversion-WebUI](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/releases)

缺点：训练音色需要推荐至少十分钟数据。

？

通过零样本TTS实现小于1分钟音频模拟音色后输出10分钟新的音频数据喂给变声器，从而实现。

## 【提交材料】

### （1）项目概要介绍;

### （2）项目简介 PPT;

### （3）项目详细方案;

### （4）项目演示视频;

### （5）团队自愿提交的其他补充材料。







首页-动画-声音样本库-介绍页面-播放标准男生和标准女生-添加声音样本-模拟上传文件-模拟现场录制-播放录制的声音-文本转语音-设计输入文本（2份）-播放声音用上传和标准分别测试一个听得出语气的，一个慢情感，一个快专业

课件制作-预览-导出课件（弹出选地址保存）

声音置换-上传视频-响应大约10秒，预览视频-假装下载、



展示指标-有人在试听的侧面照-展示回访问卷调查，显示收到回访结果数量，结果分布，根据结果分布计算出xx指标，参考github-cosyvoice2的指标介绍

收尾动画-人员介绍、队伍编号-over



准备材料（文本、文件）

准备问卷

缝合软件

拍素材

剪视频

做ppt

写材料









