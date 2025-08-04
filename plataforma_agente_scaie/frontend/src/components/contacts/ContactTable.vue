<template>
  <div class="overflow-x-auto">
    <table class="min-w-full divide-y divide-gray-200">
      <thead class="bg-gray-50">
        <tr>
          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nombre</th>
          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Teléfono</th>
          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Empresa</th>
          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nivel de Interés</th>
          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Fecha de Creación</th>
          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Acciones</th>
        </tr>
      </thead>
      <tbody class="bg-white divide-y divide-gray-200">
        <tr v-for="contact in contacts" :key="contact.id" class="hover:bg-gray-50">
          <td class="px-6 py-4 whitespace-nowrap">
            <div class="text-sm font-medium text-gray-900">{{ contact.name }}</div>
          </td>
          <td class="px-6 py-4 whitespace-nowrap">
            <div class="text-sm text-gray-900">{{ contact.phone }}</div>
          </td>
          <td class="px-6 py-4 whitespace-nowrap">
            <div class="text-sm text-gray-900">{{ contact.email || 'No proporcionado' }}</div>
          </td>
          <td class="px-6 py-4 whitespace-nowrap">
            <div class="text-sm text-gray-900">{{ contact.company || 'No proporcionado' }}</div>
          </td>
          <td class="px-6 py-4 whitespace-nowrap">
            <span 
              class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full" 
              :class="getInterestLevelClass(contact.interest_level)"
            >
              {{ getInterestLevelText(contact.interest_level) }}
            </span>
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
            {{ formatDate(contact.created_at) }}
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
            <button 
              @click="$emit('view', contact)"
              class="text-blue-600 hover:text-blue-900 mr-3"
            >
              Ver
            </button>
            <button 
              @click="$emit('edit', contact)"
              class="text-green-600 hover:text-green-900"
            >
              Editar
            </button>
          </td>
        </tr>
      </tbody>
    </table>
    
    <div v-if="contacts.length === 0" class="text-center py-8 text-gray-500">
      <svg class="w-12 h-12 mx-auto text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
      </svg>
      <p class="mt-2">No se encontraron contactos</p>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'ContactTable',
  props: {
    contacts: {
      type: Array,
      default: () => []
    }
  },
  emits: ['view', 'edit'],
  setup() {
    const getInterestLevelClass = (level) => {
      const classes = {
        'interesado': 'bg-green-100 text-green-800',
        'contactado': 'bg-blue-100 text-blue-800',
        'no_interesado': 'bg-red-100 text-red-800',
        'nuevo': 'bg-gray-100 text-gray-800',
        'confirmado': 'bg-purple-100 text-purple-800'
      }
      return classes[level] || 'bg-gray-100 text-gray-800'
    }
    
    const getInterestLevelText = (level) => {
      const texts = {
        'interesado': 'Interesado',
        'contactado': 'Contactado',
        'no_interesado': 'No Interesado',
        'nuevo': 'Nuevo',
        'confirmado': 'Confirmado'
      }
      return texts[level] || 'Sin clasificar'
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      return date.toLocaleDateString()
    }
    
    return {
      getInterestLevelClass,
      getInterestLevelText,
      formatDate
    }
  }
}
</script>