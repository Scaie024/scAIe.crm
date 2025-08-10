<template>
  <div class="admin-dashboard">
    <!-- Header -->
    <div class="bg-gradient-to-r from-blue-600 to-indigo-700 text-white p-6 rounded-lg mb-6">
      <h1 class="text-3xl font-bold">Panel de Administración SCAIE</h1>
      <p class="text-blue-100 mt-2">Gestiona tu sistema de agente conversacional</p>
    </div>

    <!-- Métricas principales -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-green-100 text-green-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z"></path>
            </svg>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">Contactos Totales</p>
            <p class="text-2xl font-bold text-gray-900">{{ metrics.totalContacts }}</p>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-blue-100 text-blue-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
            </svg>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">Conversaciones Hoy</p>
            <p class="text-2xl font-bold text-gray-900">{{ metrics.conversationsToday }}</p>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-yellow-100 text-yellow-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
            </svg>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">Tasa de Conversión</p>
            <p class="text-2xl font-bold text-gray-900">{{ metrics.conversionRate }}%</p>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-purple-100 text-purple-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
            </svg>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">Citas Agendadas</p>
            <p class="text-2xl font-bold text-gray-900">{{ metrics.scheduledAppointments }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Gráficas y estado del sistema -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
      <!-- Gráfica de conversaciones -->
      <div class="bg-white rounded-lg shadow p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Conversaciones por Día (Últimos 7 días)</h3>
        <div class="h-64 bg-gray-100 rounded flex items-center justify-center">
          <p class="text-gray-500">Gráfica de conversaciones - Implementar con Chart.js</p>
        </div>
      </div>

      <!-- Estado del sistema -->
      <div class="bg-white rounded-lg shadow p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Estado del Sistema</h3>
        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <span class="text-sm font-medium text-gray-700">Backend API</span>
            <span :class="['inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium', 
                          systemStatus.backend ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800']">
              {{ systemStatus.backend ? 'Activo' : 'Inactivo' }}
            </span>
          </div>
          <div class="flex items-center justify-between">
            <span class="text-sm font-medium text-gray-700">Bot Telegram</span>
            <span :class="['inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium', 
                          systemStatus.telegram ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800']">
              {{ systemStatus.telegram ? 'Activo' : 'Inactivo' }}
            </span>
          </div>
          <div class="flex items-center justify-between">
            <span class="text-sm font-medium text-gray-700">Túnel ngrok</span>
            <span :class="['inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium', 
                          systemStatus.ngrok ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800']">
              {{ systemStatus.ngrok ? 'Activo' : 'Inactivo' }}
            </span>
          </div>
          <div class="flex items-center justify-between">
            <span class="text-sm font-medium text-gray-700">LLM Service</span>
            <span :class="['inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium', 
                          systemStatus.llm ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800']">
              {{ systemStatus.llm ? 'Activo' : 'Inactivo' }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Acciones rápidas -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-6">
      <div class="bg-white rounded-lg shadow p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-3">Gestión de Contactos</h3>
        <p class="text-gray-600 text-sm mb-4">Administra tu base de datos de contactos</p>
        <router-link to="/contacts" class="btn-primary">
          Ver Contactos
        </router-link>
      </div>

      <div class="bg-white rounded-lg shadow p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-3">Sandbox de Pruebas</h3>
        <p class="text-gray-600 text-sm mb-4">Prueba y optimiza tu agente conversacional</p>
        <router-link to="/sandbox" class="btn-primary">
          Ir al Sandbox
        </router-link>
      </div>

      <div class="bg-white rounded-lg shadow p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-3">Configuración del Agente</h3>
        <p class="text-gray-600 text-sm mb-4">Personaliza el comportamiento del agente</p>
        <router-link to="/agent" class="btn-primary">
          Configurar Agente
        </router-link>
      </div>
    </div>

    <!-- Conversaciones recientes -->
    <div class="bg-white rounded-lg shadow">
      <div class="px-6 py-4 border-b border-gray-200">
        <h3 class="text-lg font-semibold text-gray-900">Conversaciones Recientes</h3>
      </div>
      <div class="divide-y divide-gray-200">
        <div v-for="conversation in recentConversations" :key="conversation.id" 
             class="px-6 py-4 hover:bg-gray-50">
          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center">
                  <span class="text-xs font-medium text-gray-700">
                    {{ conversation.contact.name.charAt(0).toUpperCase() }}
                  </span>
                </div>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-900">{{ conversation.contact.name }}</p>
                <p class="text-sm text-gray-500">{{ conversation.lastMessage }}</p>
              </div>
            </div>
            <div class="flex items-center">
              <span :class="['inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium mr-3',
                            conversation.platform === 'telegram' ? 'bg-blue-100 text-blue-800' :
                            conversation.platform === 'whatsapp' ? 'bg-green-100 text-green-800' :
                            'bg-gray-100 text-gray-800']">
                {{ conversation.platform }}
              </span>
              <span class="text-sm text-gray-500">{{ formatTime(conversation.lastActivity) }}</span>
            </div>
          </div>
        </div>
      </div>
      <div class="px-6 py-3 bg-gray-50">
        <router-link to="/conversations" class="text-sm text-blue-600 hover:text-blue-500">
          Ver todas las conversaciones →
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  name: 'AdminDashboard',
  setup() {
    const metrics = ref({
      totalContacts: 0,
      conversationsToday: 0,
      conversionRate: 0,
      scheduledAppointments: 0
    })
    
    const systemStatus = ref({
      backend: true,
      telegram: true,
      ngrok: true,
      llm: true
    })
    
    const recentConversations = ref([])
    
    const formatTime = (timestamp) => {
      const now = new Date()
      const time = new Date(timestamp)
      const diffMs = now - time
      const diffMins = Math.floor(diffMs / 60000)
      
      if (diffMins < 1) return 'Ahora'
      if (diffMins < 60) return `${diffMins}m`
      if (diffMins < 1440) return `${Math.floor(diffMins / 60)}h`
      return `${Math.floor(diffMins / 1440)}d`
    }
    
    const loadMetrics = async () => {
      try {
        const response = await fetch('/api/v1/dashboard/metrics')
        if (response.ok) {
          const data = await response.json()
          metrics.value = data
        }
      } catch (error) {
        console.error('Error cargando métricas:', error)
        // Datos de ejemplo para desarrollo
        metrics.value = {
          totalContacts: 156,
          conversationsToday: 23,
          conversionRate: 34.5,
          scheduledAppointments: 8
        }
      }
    }
    
    const loadSystemStatus = async () => {
      try {
        const response = await fetch('/api/v1/debug/system-status')
        if (response.ok) {
          const data = await response.json()
          systemStatus.value = data
        }
      } catch (error) {
        console.error('Error cargando estado del sistema:', error)
      }
    }
    
    const loadRecentConversations = async () => {
      try {
        const response = await fetch('/api/v1/conversations/recent?limit=5')
        if (response.ok) {
          const data = await response.json()
          recentConversations.value = data
        }
      } catch (error) {
        console.error('Error cargando conversaciones:', error)
        // Datos de ejemplo para desarrollo
        recentConversations.value = [
          {
            id: 1,
            contact: { name: 'Juan Pérez' },
            lastMessage: 'Me interesa el workshop de IA...',
            platform: 'telegram',
            lastActivity: new Date(Date.now() - 300000) // 5 minutos atrás
          },
          {
            id: 2,
            contact: { name: 'María García' },
            lastMessage: '¿Cuánto cuesta el workshop básico?',
            platform: 'whatsapp',
            lastActivity: new Date(Date.now() - 900000) // 15 minutos atrás
          },
          {
            id: 3,
            contact: { name: 'Carlos López' },
            lastMessage: 'Necesito automatizar mi empresa',
            platform: 'web',
            lastActivity: new Date(Date.now() - 1800000) // 30 minutos atrás
          }
        ]
      }
    }
    
    onMounted(() => {
      loadMetrics()
      loadSystemStatus()
      loadRecentConversations()
      
      // Actualizar métricas cada 30 segundos
      setInterval(() => {
        loadMetrics()
        loadSystemStatus()
      }, 30000)
    })
    
    return {
      metrics,
      systemStatus,
      recentConversations,
      formatTime
    }
  }
}
</script>

<style scoped>
.btn-primary {
  @apply inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition duration-200;
}
</style>
