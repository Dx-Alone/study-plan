import { createRouter, createWebHistory } from 'vue-router'
import Home from '../App.vue'
import NoteDetail from '../components/NoteDetail.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/note/:phaseId/:noteId',
    name: 'NoteDetail',
    component: NoteDetail,
    props: true
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 