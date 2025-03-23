# AI语音合成教学软件

基于Vue.js和Electron构建的AI语音合成教学桌面应用。

## 功能特点

- 声音样本库管理
- 文本转语音功能
- 课件制作与下载
- 声音置换功能

## 开发环境设置

### 安装依赖

```bash
npm install
```

### 运行Vue前端（不含Electron）

```bash
npm run dev
```

### 运行Electron开发环境

```bash
npm run electron:dev
```

### 构建桌面应用

```bash
npm run electron:build
```

## 应用打包

构建完成后，可以在`electron-dist`目录找到打包好的应用程序。

## 图标准备

在发布应用前，请准备以下图标文件：

- Windows: `src/assets/icon.ico`
- macOS: `src/assets/icon.icns`

可以使用在线工具将PNG图像转换为所需的图标格式。

## 技术栈

- Vue.js 3
- Vue Router
- Pinia (状态管理)
- Electron
- Element Plus (UI组件库) 

打包：
   npm run electron:no-sign

