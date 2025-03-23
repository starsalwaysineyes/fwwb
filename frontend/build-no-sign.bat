@echo off
echo 正在执行无签名构建...

:: 设置环境变量
set CSC_IDENTITY_AUTO_DISCOVERY=false
set USE_HARD_LINKS=false
set ELECTRON_BUILDER_LOGGING=debug
set NODE_OPTIONS=--max-old-space-size=4096

:: 先构建Vue应用
call npm run build

:: 使用无签名脚本构建
call node no-sign-build.js

echo 构建完成！请查看electron-dist目录下的输出文件。
pause 