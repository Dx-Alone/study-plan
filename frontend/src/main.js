import { createApp } from 'vue'
import AppWrapper from './AppWrapper.vue'
import router from './router'
import './assets/styles.css'

// 导入Markdown主题样式
import './assets/markdown-themes/github.css'
import './assets/markdown-themes/vue.css'
import './assets/markdown-themes/academic.css'

const app = createApp(AppWrapper)
app.use(router)
app.mount('#app')
