const builder = require('electron-builder');
const path = require('path');

console.log('开始无签名构建过程...');

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
    icon: 'src/assets/icon.ico',
    artifactName: '${productName}-${version}.${ext}'
  },
  asar: false, // 禁用asar打包
  compression: 'store', // 使用最低压缩级别，加快构建
  signAndEditExecutable: false, // 禁用签名
  forceCodeSigning: false, // 禁用强制代码签名
  npmRebuild: false // 禁用npm rebuild步骤
};

// 设置日志级别
process.env.ELECTRON_BUILDER_LOGGING = 'debug';

// 执行构建
builder.build({
  targets: builder.Platform.WINDOWS.createTarget(),
  config: config
})
.then(() => {
  console.log('构建成功！查看electron-dist目录获取可执行文件。');
})
.catch((error) => {
  console.error('构建失败:', error);
}); 