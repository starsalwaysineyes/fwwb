const { app, BrowserWindow, dialog } = require('electron')
const path = require('path')
const fs = require('fs')

// 添加错误处理
process.on('uncaughtException', (error) => {
  console.error('未捕获的异常:', error)
  dialog.showErrorBox('应用错误', `发生了一个错误: ${error.message}`)
})

function createWindow() {
  // 创建浏览器窗口
  const mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: false,  // 更安全的设置
      contextIsolation: true,  // 启用上下文隔离
      preload: path.join(__dirname, 'preload.js')
    }
  })

  // 记录日志
  console.log('应用路径:', app.getAppPath())
  console.log('当前工作目录:', process.cwd())
  console.log('预加载脚本路径:', path.join(__dirname, 'preload.js'))

  // 加载应用 - 开发环境使用本地服务器，生产环境使用本地文件
  const isDev = process.env.NODE_ENV === 'development'
  if (isDev) {
    console.log('以开发模式运行')
    mainWindow.loadURL('http://localhost:5173/') // Vite默认端口
    // 打开开发工具
    mainWindow.webContents.openDevTools()
  } else {
    console.log('以生产模式运行')
    const indexPath = path.join(__dirname, 'dist/index.html')
    console.log('加载HTML文件:', indexPath)
    // 检查文件是否存在
    if (fs.existsSync(indexPath)) {
      mainWindow.loadFile(indexPath)
    } else {
      console.error('找不到index.html文件')
      dialog.showErrorBox('加载错误', `找不到文件: ${indexPath}`)
    }
  }
}

// 当Electron完成初始化并准备创建浏览器窗口时调用此方法
app.whenReady().then(() => {
  console.log('Electron应用已准备就绪')
  createWindow()

  app.on('activate', function () {
    // 在macOS上，当点击dock图标且没有其他窗口打开时，
    // 通常会在应用程序中重新创建一个窗口
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

// 当所有窗口关闭时退出应用
app.on('window-all-closed', function () {
  // 在macOS上，除非用户用Cmd + Q确定地退出，
  // 否则绝大部分应用及其菜单栏会保持激活
  if (process.platform !== 'darwin') app.quit()
}) 