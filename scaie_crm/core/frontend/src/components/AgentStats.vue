<template>
  <div class="bg-white rounded-lg shadow p-6">
    <h2 class="text-xl font-bold mb-4 text-gray-800">Estadísticas del Agente</h2>
    
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
      <div class="border rounded-lg p-4">
        <div class="text-gray-500 text-sm mb-1">Contactos Creados</div>
        <div class="text-2xl font-bold text-blue-600">{{ stats.contacts_created }}</div>
      </div>
      <div class="border rounded-lg p-4">
        <div class="text-gray-500 text-sm mb-1">Conversaciones Activas</div>
        <div class="text-2xl font-bold text-green-600">{{ stats.active_conversations }}</div>
      </div>
      <div class="border rounded-lg p-4">
        <div class="text-gray-500 text-sm mb-1">Tasa de Conversión</div>
        <div class="text-2xl font-bold text-purple-600">{{ stats.conversion_rate }}%</div>
      </div>
    </div>
    
    <div class="mb-6">
      <h3 class="font-medium mb-3">Nivel de Interés de Contactos</h3>
      <div class="space-y-3">
        <div v-for="(value, level) in interestStats" :key="level">
          <div class="flex justify-between text-sm mb-1">
            <span class="text-gray-600 capitalize">{{ level.replace('_', ' ') }}</span>
            <span class="font-medium">{{ value }} ({{ getPercentage(value) }}%)</span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div 
              class="h-2 rounded-full" 
              :class="getInterestBarClass(level)"
              :style="{ width: getPercentage(value) + '%' }"
            ></div>
          </div>
        </div>
      </div>
    </div>
    
    <div>
      <h3 class="font-medium mb-3">Actividad Reciente del Agente</h3>
      <div class="space-y-3">
        <div v-for="(activity, index) in recentActivities" :key="index" class="flex items-start border-b pb-3 last:border-0 last:pb-0">
          <div class="bg-blue-100 text-blue-600 rounded-full w-8 h-8 flex items-center justify-center mr-3 flex-shrink-0">
            <svg v-if="activity.type === 'contact'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
            </svg>
            <svg v-if="activity.type === 'conversation'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
            </svg>
          </div>
          <div class="flex-1">
            <p class="text-sm font-medium">{{ activity.title }}</p>
            <p class="text-gray-600 text-xs">{{ activity.description }}</p>
            <p class="text-gray-400 text-xs">{{ activity.time }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  name: 'AgentStats',
  setup() {
    const stats = ref({
      contacts_created: 24,
      active_conversations: 12,
      conversion_rate: 32
    })
    
    const interestStats = ref({
      interesado: 18,
      contactado: 22,
      no_interesado: 8,
      nuevo: 15,
      confirmado: 5
    })
    
    const recentActivities = ref([
      {
        type: 'contact',
        title: 'Nuevo contacto calificado',
        description: 'Contacto creado automáticamente con nivel de interés: Interesado',
        time: 'Hace 5 minutos'
      },
      {
        type: 'conversation',
        title: 'Conversación activa',
        description: 'Usuario mostró interés en el taller de eficiencia con IA',
        time: 'Hace 12 minutos'
      },
      {
        type: 'contact',
        title: 'Nivel de interés actualizado',
        description: 'Contacto actualizado de Contactado a Interesado',
        time: 'Hace 25 minutos'
      }
    ])
    
    const getPercentage = (value) => {
      const total = Object.values(interestStats.value).reduce((sum, val) => sum + val, 0)
      return total > 0 ? Math.round((value / total) * 100) : 0
    }
    
    const getInterestBarClass = (level) => {
      const classes = {
        interesado: 'bg-green-500',
        contactado: 'bg-blue-500',
        no_interesado: 'bg-red-500',
        nuevo: 'bg-gray-500',
        confirmado: 'bg-purple-500'
      }
      return classes[level] || 'bg-gray-500'
    }
    
    return {
      stats,
      interestStats,
      recentActivities,
      getPercentage,
      getInterestBarClass
    }
  }
}
</script>