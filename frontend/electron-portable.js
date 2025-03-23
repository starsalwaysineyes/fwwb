const builder = require('electron-builder');
const path = require('path');

// 定义构建配置
const config = {
  appId: 'com.aivoice.education',
  productName: 'AI语音合成教学软件',
  directories: {
    output: 'electron-dist'
  },
  files: [
    'dist/**/*',
    'main.js',
    'preload.js'
  ],
  win: {
    target: 'portable',
    icon: 'src/assets/icon.ico'
  },
  asar: false, // 禁用asar打包，避免符号链接问题
  compression: 'normal', // 使用标准压缩，不使用最大压缩
  signAndEditExecutable: false, // 禁用签名
  forceCodeSigning: false // 禁用强制代码签名
};

// 执行构建
builder.build({
  targets: builder.Platform.WINDOWS.createTarget(),
  config: config
})
.then(() => {
  console.log('构建成功！');
})
.catch((error) => {
  console.error('构建失败:', error);
}); 