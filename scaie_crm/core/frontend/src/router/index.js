import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../pages/Dashboard.vue'
import Chat from '../pages/Chat.vue'
import Contacts from '../pages/Contacts.vue'
import Agent from '../pages/Agent.vue'
import Sandbox from '../pages/Sandbox.vue'
import AdminDashboard from '../pages/AdminDashboard.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: AdminDashboard
  },
  {
    path: '/chat',
    name: 'Chat',
    component: Chat
  },
  {
    path: '/contacts',
    name: 'Contacts',
    component: Contacts
  },
  {
    path: '/agent',
    name: 'Agent',
    component: Agent
  },
  {
    path: '/sandbox',
    name: 'Sandbox',
    component: Sandbox
  },
  // Backward-compat alias
  {
    path: '/database',
    redirect: '/contacts'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router