const fs = require('fs');
const path = require('path');
const { createCanvas } = require('canvas');

// 创建256x256的图标
const canvas = createCanvas(256, 256);
const ctx = canvas.getContext('2d');

// 绘制背景
ctx.fillStyle = '#1890ff';
ctx.fillRect(0, 0, 256, 256);

// 绘制文本
ctx.fillStyle = 'white';
ctx.font = 'bold 100px Arial';
ctx.textAlign = 'center';
ctx.textBaseline = 'middle';
ctx.fillText('AI', 128, 128);

// 保存为PNG
const buffer = canvas.toBuffer('image/png');
fs.writeFileSync(path.join(__dirname, 'icon.png'), buffer);

console.log('图标已创建: temp-icons/icon.png');
console.log('请使用在线工具将此PNG转换为ICO格式，然后替换src/assets/icon.ico'); 