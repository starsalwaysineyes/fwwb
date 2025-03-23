@echo off
echo 以管理员权限运行Electron构建过程...

:: 设置环境变量
set CSC_IDENTITY_AUTO_DISCOVERY=false
set USE_HARD_LINKS=false
set NODE_OPTIONS=--max-old-space-size=4096

:: 先构建Vue应用
call npm run build

:: 构建Electron应用，指定为便携式应用，不签名
call electron-builder --win portable --publish never

echo 构建完成！请查看electron-dist目录下的输出文件。
pause 