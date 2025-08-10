<template>
  <div class="bg-white rounded-lg shadow p-6">
    <h2 class="text-xl font-bold mb-4 text-gray-800">Distribución de Nivel de Interés</h2>
    
    <div v-if="distribution && Object.keys(distribution).length > 0" class="space-y-4">
      <div v-for="(count, level) in distribution" :key="level">
        <div class="flex justify-between text-sm mb-1">
          <span class="text-gray-600 capitalize">{{ formatLevel(level) }}</span>
          <span class="font-medium">{{ count }} ({{ getPercentage(count) }}%)</span>
        </div>
        <div class="w-full bg-gray-200 rounded-full h-2">
          <div 
            class="h-2 rounded-full" 
            :class="getLevelColor(level)"
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
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'InterestDistribution',
  props: {
    distribution: {
      type: Object,
      default: () => ({})
    },
    total: {
      type: Number,
      default: 0
    }
  },
  setup(props) {
    const getPercentage = (value) => {
      return props.total > 0 ? Math.round((value / props.total) * 100) : 0
    }
    
    const getLevelColor = (level) => {
      const colors = {
        interesado: 'bg-green-500',
        contactado: 'bg-blue-500',
        no_interesado: 'bg-red-500',
        nuevo: 'bg-gray-500',
        confirmado: 'bg-purple-500'
      }
      return colors[level] || 'bg-gray-500'
    }
    
    const formatLevel = (level) => {
      const translations = {
        interesado: 'Interesado',
        contactado: 'Contactado',
        no_interesado: 'No Interesado',
        nuevo: 'Nuevo',
        confirmado: 'Confirmado'
      }
      return translations[level] || level
    }
    
    return {
      getPercentage,
      getLevelColor,
      formatLevel
    }
  }
}
</script>