import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import Chat from '../views/Chat.vue'
import Contacts from '../views/Contacts.vue'

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