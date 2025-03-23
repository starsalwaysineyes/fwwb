import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/main.css'

// 导入Element Plus
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'

const app = createApp(App)

app.use(router)
// 注册Element Plus
app.use(ElementPlus, {
  locale: zhCn
})

app.mount('#app') 