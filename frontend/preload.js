// 预加载脚本，用于安全地将Node.js功能暴露给渲染进程
const { contextBridge, ipcRenderer } = require('electron')

// 暴露最小化的API给渲染进程
contextBridge.exposeInMainWorld('electronAPI', {
  // 发送消息到主进程
  send: (channel, data) => {
    // 白名单频道，提高安全性
    let validChannels = ['toMain', 'saveFile', 'openFile']
    if (validChannels.includes(channel)) {
      ipcRenderer.send(channel, data)
    }
  },
  // 接收来自主进程的消息
  receive: (channel, func) => {
    let validChannels = ['fromMain', 'fileData']
    if (validChannels.includes(channel)) {
      ipcRenderer.on(channel, (event, ...args) => func(...args))
    }
  }
})

// 添加版本信息到window对象
contextBridge.exposeInMainWorld('versions', {
  node: () => process.versions.node,
  electron: () => process.versions.electron
})

// 添加一些常用的全局变量
window.addEventListener('DOMContentLoaded', () => {
  const replaceText = (selector, text) => {
    const element = document.getElementById(selector)
    if (element) element.innerText = text
  }

  for (const dependency of ['chrome', 'node', 'electron']) {
    replaceText(`${dependency}-version`, process.versions[dependency])
  }
}) 