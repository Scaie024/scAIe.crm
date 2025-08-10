<template>
  <div class="dashboard">
    <div class="bg-blue-600 text-white p-6 rounded-lg mb-6">
      <h1 class="text-2xl font-bold">Dashboard de Operaciones</h1>
      <p class="text-blue-100">KPIs y métricas clave de ventas automatizadas</p>
    </div>
    
    <!-- KPIs Principales -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
      <div class="bg-white p-6 rounded-lg shadow">
        <div class="flex items-center">
          <div class="p-3 rounded-lg bg-blue-100 text-blue-600 mr-4">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
            </svg>
          </div>
          <div>
            <p class="text-gray-500 text-sm">Total Contactos</p>
            <p class="text-2xl font-bold">{{ stats.total || 0 }}</p>
          </div>
        </div>
      </div>
      
      <div class="bg-white p-6 rounded-lg shadow">
        <div class="flex items-center">
          <div class="p-3 rounded-lg bg-green-100 text-green-600 mr-4">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
          <div>
            <p class="text-gray-500 text-sm">Clientes Interesados</p>
            <p class="text-2xl font-bold">{{ stats.interest_level_distribution?.interesado || 0 }}</p>
          </div>
        </div>
      </div>
      
      <div class="bg-white p-6 rounded-lg shadow">
        <div class="flex items-center">
          <div class="p-3 rounded-lg bg-yellow-100 text-yellow-600 mr-4">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
            </svg>
          </div>
          <div>
            <p class="text-gray-500 text-sm">Contactados</p>
            <p class="text-2xl font-bold">{{ stats.interest_level_distribution?.contactado || 0 }}</p>
          </div>
        </div>
      </div>
      
      <div class="bg-white p-6 rounded-lg shadow">
        <div class="flex items-center">
          <div class="p-3 rounded-lg bg-red-100 text-red-600 mr-4">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
          <div>
            <p class="text-gray-500 text-sm">No Interesados</p>
            <p class="text-2xl font-bold">{{ stats.interest_level_distribution?.no_interesado || 0 }}</p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Gráficos y métricas -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
      <!-- Tasa de conversión -->
      <div class="card">
        <div class="p-5">
          <h3 class="text-lg font-semibold mb-4">Tasa de Conversión</h3>
          <div class="h-64 flex items-center justify-center">
            <div class="text-center">
              <div class="text-4xl font-bold text-primary-600 mb-2">
                {{ conversionRate }}%
              </div>
              <p class="text-gray-500">De contactos a clientes interesados</p>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Distribución de intereses -->
      <div class="card">
        <div class="p-5">
          <h3 class="text-lg font-semibold mb-4">Distribución de Niveles de Interés</h3>
          <div class="h-64 flex items-center justify-center">
            <div class="w-full">
              <div class="flex items-center mb-3" v-for="level in interestLevels" :key="level.name">
                <div class="w-24 text-sm text-gray-600">{{ level.name }}</div>
                <div class="flex-1 ml-2">
                  <div class="h-3 bg-gray-200 rounded-full overflow-hidden">
                    <div 
                      class="h-full rounded-full" 
                      :class="{
                        'bg-success-500': level.name === 'Interesado',
                        'bg-warning-500': level.name === 'Contactado',
                        'bg-primary-500': level.name === 'Nuevo',
                        'bg-danger-500': level.name === 'No Interesado',
                        'bg-gray-500': level.name === 'Confirmado'
                      }"
                      :style="{ width: level.percentage + '%' }"
                    ></div>
                  </div>
                </div>
                <div class="w-10 text-right text-sm font-medium">{{ level.count }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Actividad reciente -->
    <div class="card mb-6">
      <div class="p-5">
        <h3 class="text-lg font-semibold mb-4">Actividad Reciente</h3>
        <div class="space-y-4">
          <div v-for="activity in recentActivities" :key="activity.id" class="flex items-start border-b border-gray-100 pb-4 last:border-0 last:pb-0">
            <div class="flex-shrink-0 mt-1">
              <div class="w-8 h-8 rounded-full bg-primary-100 flex items-center justify-center">
                <svg v-if="activity.type === 'contact'" class="w-4 h-4 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                </svg>
                <svg v-else-if="activity.type === 'message'" class="w-4 h-4 text-success-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
                </svg>
                <svg v-else class="w-4 h-4 text-warning-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                </svg>
              </div>
            </div>
            <div class="ml-3 flex-1">
              <p class="text-sm font-medium text-gray-900">{{ activity.title }}</p>
              <p class="text-sm text-gray-500">{{ activity.description }}</p>
              <p class="text-xs text-gray-400 mt-1">{{ activity.time }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import api from '../services/api.js'

export default {
  name: 'Dashboard',
  setup() {
    const stats = ref({
      total_contacts: 0,
      total_conversations: 0,
      interest_level_distribution: {}
    })
    
    const addingContact = ref(false)
    const newContact = ref({
      name: '',
      phone: '',
      email: '',
      company: '',
      interest_level: 'nuevo'
    })
    
    // Calcular tasa de conversión
    const conversionRate = computed(() => {
      if (!stats.value.total_contacts) return 0
      const interested = stats.value.interesado || 0
      return Math.round((interested / stats.value.total_contacts) * 100)
    })
    
    // Load dashboard data
    const loadDashboardData = async () => {
      try {
        // Load agent stats
        const agentStats = await api.getAgentStats()
        stats.value = agentStats
      } catch (error) {
        console.error('Error loading dashboard data:', error)
      }
    }
    
    // Agregar nuevo contacto
    const addContact = async () => {
      if (addingContact.value) return
      
      addingContact.value = true
      try {
        await api.createContact(newContact.value)
        
        // Reset form
        newContact.value = {
          name: '',
          phone: '',
          email: '',
          company: '',
          interest_level: 'nuevo'
        }
        
        // Reload stats
        await loadDashboardData()
        
        // Mostrar mensaje de éxito
        alert('Cliente agregado exitosamente')
      } catch (error) {
        console.error('Error adding contact:', error)
        alert('Error al agregar cliente: ' + (error.message || 'Error desconocido'))
      } finally {
        addingContact.value = false
      }
    }
    
    // Funciones auxiliares
    const getPercentage = (value) => {
      const total = stats.value.total_contacts || 1
      return Math.round((value / total) * 100)
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
    
    const formatInterestLevel = (level) => {
      const translations = {
        interesado: 'Interesado',
        contactado: 'Contactado',
        no_interesado: 'No Interesado',
        nuevo: 'Nuevo',
        confirmado: 'Confirmado'
      }
      return translations[level] || level
    }
    
    // Load data on component mount
    onMounted(() => {
      loadDashboardData()
    })
    
    return {
      stats,
      addingContact,
      newContact,
      conversionRate,
      addContact,
      getPercentage,
      getInterestBarClass,
      formatInterestLevel
    }
  }
}

// Necesitamos importar computed desde vue
</script>

<style scoped>
/* Add any additional styles here if needed */
</style>