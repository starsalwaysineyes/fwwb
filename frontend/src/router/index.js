import { createRouter, createWebHistory } from 'vue-router'

// 路由懒加载
const Home = () => import('../views/Home.vue')
const VoiceSamples = () => import('../views/VoiceSamples.vue')
const TextToSpeech = () => import('../views/TextToSpeech.vue')
const CourseMaker = () => import('../views/CourseMaker.vue')
const VoiceReplace = () => import('../views/VoiceReplace.vue')

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
      meta: { title: '首页' }
    },
    {
      path: '/voice-samples',
      name: 'voice-samples',
      component: VoiceSamples,
      meta: { title: '声音样本库' }
    },
    {
      path: '/text-to-speech',
      name: 'text-to-speech',
      component: TextToSpeech,
      meta: { title: '文本转语音' }
    },
    {
      path: '/course-maker',
      name: 'course-maker',
      component: CourseMaker,
      meta: { title: '课件制作' }
    },
    {
      path: '/voice-replace',
      name: 'voice-replace',
      component: VoiceReplace,
      meta: { title: '声音置换与字幕' }
    },
    // 404路由
    {
      path: '/:pathMatch(.*)*',
      redirect: '/'
    }
  ]
})

// 全局前置守卫
router.beforeEach((to, from, next) => {
  // 设置页面标题
  document.title = `${to.meta.title || '首页'} - AI语音合成教学软件`
  next()
})

export default router 