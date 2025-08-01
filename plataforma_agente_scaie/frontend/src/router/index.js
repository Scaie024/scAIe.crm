import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import Contacts from '../views/Contacts.vue'
import Chat from '../views/Chat.vue'
import Agent from '../views/Agent.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/contacts',
    name: 'Contacts',
    component: Contacts
  },
  {
    path: '/chat',
    name: 'Chat',
    component: Chat
  },
  {
    path: '/agent',
    name: 'Agent',
    component: Agent
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router