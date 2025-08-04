<template>
  <div class="dashboard">
    <div class="bg-gradient-to-r from-blue-600 to-indigo-700 text-white p-4 rounded-t-lg mb-6">
      <h1 class="text-2xl font-bold">Dashboard de Operaciones</h1>
      <p class="text-blue-100">KPIs y métricas clave de ventas automatizadas</p>
    </div>
    
    <!-- KPIs Principales -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
      <div class="bg-white rounded-lg shadow p-6 hover:shadow-md transition-shadow duration-200">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-blue-100 text-blue-600 mr-4">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
            </svg>
          </div>
          <div>
            <p class="text-gray-500 text-sm">Total Contactos</p>
            <p class="text-2xl font-bold">{{ stats.total_contacts || 0 }}</p>
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-lg shadow p-6 hover:shadow-md transition-shadow duration-200">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-green-100 text-green-600 mr-4">
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
      
      <div class="bg-white rounded-lg shadow p-6 hover:shadow-md transition-shadow duration-200">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-purple-100 text-purple-600 mr-4">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
            </svg>
          </div>
          <div>
            <p class="text-gray-500 text-sm">Conversaciones Activas</p>
            <p class="text-2xl font-bold">{{ stats.total_conversations || 0 }}</p>
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-lg shadow p-6 hover:shadow-md transition-shadow duration-200">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-yellow-100 text-yellow-600 mr-4">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
          <div>
            <p class="text-gray-500 text-sm">Tasa de Conversión</p>
            <p class="text-2xl font-bold">{{ conversionRate }}%</p>
          </div>
        </div>
      </div>
    </div>
    
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Panel para agregar clientes -->
      <div class="bg-white rounded-lg shadow">
        <div class="border-b p-4">
          <h2 class="text-lg font-bold text-gray-800">Agregar Nuevo Cliente</h2>
        </div>
        <div class="p-4">
          <form @submit.prevent="addContact" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Nombre completo *</label>
              <input 
                v-model="newContact.name" 
                type="text" 
                required
                class="w-full border rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Nombre del cliente"
              >
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Teléfono *</label>
              <input 
                v-model="newContact.phone" 
                type="tel" 
                required
                class="w-full border rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="+52 55 1234 5678"
              >
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
              <input 
                v-model="newContact.email" 
                type="email" 
                class="w-full border rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="cliente@ejemplo.com"
              >
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Empresa</label>
              <input 
                v-model="newContact.company" 
                type="text" 
                class="w-full border rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Nombre de la empresa"
              >
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Nivel de Interés</label>
              <select 
                v-model="newContact.interest_level" 
                class="w-full border rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="nuevo">Nuevo</option>
                <option value="contactado">Contactado</option>
                <option value="interesado">Interesado</option>
                <option value="confirmado">Confirmado</option>
                <option value="no_interesado">No Interesado</option>
              </select>
            </div>
            
            <div class="pt-2">
              <button 
                type="submit" 
                :disabled="addingContact"
                class="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition duration-200 flex items-center justify-center"
              >
                <svg v-if="addingContact" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span>{{ addingContact ? 'Agregando...' : 'Agregar Cliente' }}</span>
              </button>
            </div>
          </form>
        </div>
      </div>
      
      <!-- Estadísticas de nivel de interés -->
      <div class="bg-white rounded-lg shadow">
        <div class="border-b p-4">
          <h2 class="text-lg font-bold text-gray-800">Distribución de Clientes</h2>
        </div>
        <div class="p-4">
          <div v-if="stats.interest_level_distribution && Object.keys(stats.interest_level_distribution).length > 0" class="space-y-4">
            <div v-for="(count, level) in stats.interest_level_distribution" :key="level">
              <div class="flex justify-between text-sm mb-1">
                <span class="text-gray-600 capitalize">{{ formatInterestLevel(level) }}</span>
                <span class="font-medium">{{ count }} ({{ getPercentage(count) }}%)</span>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-2">
                <div 
                  class="h-2 rounded-full" 
                  :class="getInterestBarClass(level)"
                  :style="{ width: getPercentage(count) + '%' }"
                ></div>
              </div>
            </div>
          </div>
          
          <div v-else class="text-center py-8 text-gray-500">
            <svg class="w-12 h-12 mx-auto text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
            </svg>
            <p class="mt-2">No hay datos de distribución</p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Acciones rápidas -->
    <div class="bg-white rounded-lg shadow mt-6">
      <div class="border-b p-4">
        <h2 class="text-lg font-bold text-gray-800">Acciones Rápidas</h2>
      </div>
      <div class="p-4">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button 
            @click="$router.push('/database')"
            class="flex flex-col items-center justify-center p-6 bg-green-50 hover:bg-green-100 rounded-lg transition-colors duration-200"
          >
            <div class="bg-green-100 text-green-600 rounded-full w-12 h-12 flex items-center justify-center mb-3">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4"></path>
              </svg>
            </div>
            <h3 class="font-medium text-gray-800">Administrar Base de Datos</h3>
            <p class="text-sm text-gray-600 mt-1 text-center">Ver y gestionar todos los clientes</p>
          </button>
          
          <button 
            @click="$router.push('/chat')"
            class="flex flex-col items-center justify-center p-6 bg-blue-50 hover:bg-blue-100 rounded-lg transition-colors duration-200"
          >
            <div class="bg-blue-100 text-blue-600 rounded-full w-12 h-12 flex items-center justify-center mb-3">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
              </svg>
            </div>
            <h3 class="font-medium text-gray-800">Chat de Pruebas</h3>
            <p class="text-sm text-gray-600 mt-1 text-center">Probar el agente de ventas</p>
          </button>
          
          <div class="flex flex-col items-center justify-center p-6 bg-purple-50 rounded-lg">
            <div class="bg-purple-100 text-purple-600 rounded-full w-12 h-12 flex items-center justify-center mb-3">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
              </svg>
            </div>
            <h3 class="font-medium text-gray-800">Integraciones</h3>
            <p class="text-sm text-gray-600 mt-1 text-center">WhatsApp, Facebook, etc.</p>
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
      const interested = stats.value.interest_level_distribution?.interesado || 0
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