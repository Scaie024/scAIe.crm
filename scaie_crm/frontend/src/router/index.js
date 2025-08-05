import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../pages/Dashboard.vue'
import Chat from '../pages/Chat.vue'
import Contacts from '../pages/Contacts.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/chat',
    name: 'Chat',
    component: Chat
  },
  {
    path: '/database',
    name: 'Database',
    component: Contacts
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router