<template>
  <div class="database">
    <div class="bg-gradient-to-r from-green-600 to-teal-700 text-white p-4 rounded-t-lg mb-6">
      <h1 class="text-2xl font-bold">Administración de Base de Datos</h1>
      <p class="text-green-100">Gestión completa de clientes y contactos</p>
    </div>
    
    <!-- Estadísticas generales -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
      <div class="bg-white rounded-lg shadow p-4 hover:shadow-md transition-shadow duration-200">
        <div class="text-gray-500 text-sm">Total Contactos</div>
        <div class="text-2xl font-bold">{{ stats.total || 0 }}</div>
      </div>
      <div class="bg-white rounded-lg shadow p-4 hover:shadow-md transition-shadow duration-200">
        <div class="text-gray-500 text-sm">Interesados</div>
        <div class="text-2xl font-bold text-green-600">{{ stats.interesado || 0 }}</div>
      </div>
      <div class="bg-white rounded-lg shadow p-4 hover:shadow-md transition-shadow duration-200">
        <div class="text-gray-500 text-sm">Contactados</div>
        <div class="text-2xl font-bold text-blue-600">{{ stats.contactado || 0 }}</div>
      </div>
      <div class="bg-white rounded-lg shadow p-4 hover:shadow-md transition-shadow duration-200">
        <div class="text-gray-500 text-sm">No Interesados</div>
        <div class="text-2xl font-bold text-red-600">{{ stats.no_interesado || 0 }}</div>
      </div>
    </div>
    
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Panel de búsqueda y acciones -->
      <div class="lg:col-span-2">
        <div class="bg-white rounded-lg shadow mb-6">
          <div class="p-4 border-b">
            <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
              <h2 class="text-lg font-bold text-gray-800">Lista de Clientes</h2>
              <div class="flex flex-col sm:flex-row gap-2">
                <input 
                  v-model="searchQuery"
                  @keyup.enter="searchContacts"
                  type="text" 
                  placeholder="Buscar clientes..." 
                  class="border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-green-500"
                >
                <button 
                  @click="searchContacts"
                  class="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition duration-200 flex items-center"
                >
                  <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                  </svg>
                  Buscar
                </button>
                <button 
                  @click="resetSearch"
                  class="bg-gray-200 text-gray-800 px-4 py-2 rounded-lg hover:bg-gray-300 transition duration-200"
                >
                  Reiniciar
                </button>
              </div>
            </div>
          </div>
          
          <div v-if="loading" class="p-8">
            <div class="flex flex-col items-center justify-center">
              <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-green-600 mb-2"></div>
              <p class="text-gray-600">Cargando clientes...</p>
            </div>
          </div>
          
          <div v-else-if="error" class="p-8">
            <div class="bg-red-50 border border-red-200 rounded-lg p-4">
              <div class="flex">
                <div class="flex-shrink-0">
                  <svg class="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                  </svg>
                </div>
                <div class="ml-3">
                  <h3 class="text-sm font-medium text-red-800">Error al cargar clientes</h3>
                  <div class="mt-2 text-sm text-red-700">
                    <p>{{ error }}</p>
                  </div>
                  <div class="mt-4">
                    <button 
                      @click="loadContacts"
                      class="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded-full shadow-sm text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                    >
                      Reintentar
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div v-else>
            <div class="overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nombre</th>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Teléfono</th>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Empresa</th>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nivel de Interés</th>
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
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <button 
                        @click="editContact(contact)"
                        class="text-blue-600 hover:text-blue-900 mr-3"
                      >
                        Editar
                      </button>
                      <button 
                        @click="deleteContact(contact.id)"
                        class="text-red-600 hover:text-red-900"
                      >
                        Eliminar
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
              
              <div v-if="contacts.length === 0" class="text-center py-8 text-gray-500">
                <svg class="w-12 h-12 mx-auto text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
                </svg>
                <p class="mt-2">No se encontraron clientes</p>
              </div>
            </div>
            
            <div v-if="contacts.length > 0" class="px-4 py-3 flex items-center justify-between border-t">
              <div class="text-sm text-gray-700">
                Mostrando <span class="font-medium">{{ (currentPage - 1) * pageSize + 1 }}</span> a 
                <span class="font-medium">{{ Math.min(currentPage * pageSize, totalContacts) }}</span> de 
                <span class="font-medium">{{ totalContacts }}</span> resultados
              </div>
              <div class="flex space-x-2">
                <button
                  @click="prevPage"
                  :disabled="currentPage === 1"
                  class="px-3 py-1 rounded-md bg-white border border-gray-300 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50"
                >
                  Anterior
                </button>
                <button
                  @click="nextPage"
                  :disabled="currentPage * pageSize >= totalContacts"
                  class="px-3 py-1 rounded-md bg-white border border-gray-300 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50"
                >
                  Siguiente
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Panel de importación -->
      <div class="lg:col-span-1">
        <div class="bg-white rounded-lg shadow p-6 mb-6">
          <h2 class="text-lg font-bold text-gray-800 mb-4">Importar Clientes</h2>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">Seleccionar archivo CSV o JSON</label>
            <input 
              type="file" 
              @change="handleFileSelect"
              accept=".csv,.json"
              class="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:text-sm file:font-semibold file:bg-green-50 file:text-green-700 hover:file:bg-green-100"
            >
            <p class="mt-1 text-sm text-gray-500">
              El archivo debe tener columnas: nombre, teléfono, email, empresa
            </p>
          </div>
          
          <div v-if="selectedFile" class="bg-green-50 p-4 rounded-lg mb-4">
            <h4 class="font-medium text-green-800 mb-2">Archivo seleccionado</h4>
            <p class="text-sm text-green-700">{{ selectedFile.name }}</p>
            <p class="text-xs text-green-600 mt-1">{{ formatFileSize(selectedFile.size) }}</p>
          </div>
          
          <button 
            @click="importContacts"
            :disabled="!selectedFile || importing"
            class="w-full bg-green-600 text-white py-2 px-4 rounded-lg hover:bg-green-700 disabled:opacity-50 flex items-center justify-center"
          >
            <svg v-if="importing" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span>{{ importing ? 'Importando...' : 'Importar Clientes' }}</span>
          </button>
          
          <div v-if="importResult" class="mt-4 p-4 rounded-lg" :class="{
            'bg-green-50 text-green-800': importResult.success,
            'bg-red-50 text-red-800': !importResult.success
          }">
            <h4 class="font-medium mb-2">{{ importResult.success ? 'Importación exitosa' : 'Error en la importación' }}</h4>
            <p class="text-sm">{{ importResult.message }}</p>
            <p v-if="importResult.imported_count !== undefined" class="text-sm mt-1">
              Clientes importados: {{ importResult.imported_count }}
            </p>
          </div>
        </div>
        
        <!-- Estadísticas de nivel de interés -->
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-lg font-bold text-gray-800 mb-4">Distribución de Clientes</h2>
          <div v-if="stats && Object.keys(stats).length > 0" class="space-y-4">
            <div v-for="(value, level) in interestStats" :key="level">
              <div class="flex justify-between text-sm mb-1">
                <span class="text-gray-600 capitalize">{{ formatInterestLevel(level) }}</span>
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
          
          <div v-else class="text-center py-4 text-gray-500">
            <svg class="w-8 h-8 mx-auto text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
            </svg>
            <p class="mt-2 text-sm">No hay datos disponibles</p>
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
  name: 'Database',
  setup() {
    const contacts = ref([])
    const stats = ref({
      total: 0,
      interesado: 0,
      contactado: 0,
      no_interesado: 0
    })
    
    const searchQuery = ref('')
    const currentPage = ref(1)
    const pageSize = ref(10)
    const totalContacts = ref(0)
    const loading = ref(false)
    const error = ref('')
    
    const selectedFile = ref(null)
    const importing = ref(false)
    const importResult = ref(null)
    
    // Computed properties
    const interestStats = computed(() => {
      return {
        interesado: stats.value.interesado || 0,
        contactado: stats.value.contactado || 0,
        no_interesado: stats.value.no_interesado || 0,
        nuevo: stats.value.nuevo || 0,
        confirmado: stats.value.confirmado || 0
      }
    })
    
    // Load contacts
    const loadContacts = async () => {
      loading.value = true
      error.value = ''
      
      try {
        const response = await api.getContacts(currentPage.value, pageSize.value, searchQuery.value)
        contacts.value = response.contacts || []
        totalContacts.value = response.total || 0
      } catch (err) {
        error.value = err.message || 'Error al cargar los contactos'
        console.error('Error loading contacts:', err)
      } finally {
        loading.value = false
      }
    }
    
    // Load contact stats
    const loadStats = async () => {
      try {
        const statsResponse = await api.getContactStats()
        stats.value = {
          total: statsResponse.total || 0,
          interesado: statsResponse.interest_level_distribution?.interesado || 0,
          contactado: statsResponse.interest_level_distribution?.contactado || 0,
          no_interesado: statsResponse.interest_level_distribution?.no_interesado || 0,
          nuevo: statsResponse.interest_level_distribution?.nuevo || 0,
          confirmado: statsResponse.interest_level_distribution?.confirmado || 0
        }
      } catch (err) {
        console.error('Error loading stats:', err)
      }
    }
    
    // Search contacts
    const searchContacts = () => {
      currentPage.value = 1
      loadContacts()
    }
    
    // Reset search
    const resetSearch = () => {
      searchQuery.value = ''
      currentPage.value = 1
      loadContacts()
    }
    
    // Pagination
    const prevPage = () => {
      if (currentPage.value > 1) {
        currentPage.value--
        loadContacts()
      }
    }
    
    const nextPage = () => {
      if (currentPage.value * pageSize.value < totalContacts.value) {
        currentPage.value++
        loadContacts()
      }
    }
    
    // File handling
    const handleFileSelect = (event) => {
      const file = event.target.files[0]
      if (file) {
        selectedFile.value = file
        importResult.value = null
      }
    }
    
    const formatFileSize = (bytes) => {
      if (bytes < 1024) return bytes + ' bytes'
      else if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB'
      else return (bytes / 1048576).toFixed(1) + ' MB'
    }
    
    const importContacts = async () => {
      if (!selectedFile.value || importing.value) return
      
      importing.value = true
      importResult.value = null
      
      try {
        const result = await api.importContacts(selectedFile.value)
        importResult.value = result
        
        if (result.success) {
          // Reload contacts and stats
          await loadContacts()
          await loadStats()
          
          // Clear file input
          selectedFile.value = null
        }
      } catch (err) {
        importResult.value = {
          success: false,
          message: err.message || 'Error al importar contactos'
        }
      } finally {
        importing.value = false
      }
    }
    
    // Contact actions
    const editContact = (contact) => {
      alert(`Editar contacto: ${contact.name}\nFuncionalidad en desarrollo`)
    }
    
    const deleteContact = async (contactId) => {
      if (!confirm('¿Estás seguro de que deseas eliminar este cliente?')) return
      
      try {
        await api.deleteContact(contactId)
        // Reload contacts and stats
        await loadContacts()
        await loadStats()
        alert('Cliente eliminado exitosamente')
      } catch (err) {
        console.error('Error deleting contact:', err)
        alert('Error al eliminar cliente: ' + (err.message || 'Error desconocido'))
      }
    }
    
    // Helper functions
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
    
    const getPercentage = (value) => {
      const total = stats.value.total || 1
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
      loadContacts()
      loadStats()
    })
    
    return {
      contacts,
      stats,
      searchQuery,
      currentPage,
      pageSize,
      totalContacts,
      loading,
      error,
      selectedFile,
      importing,
      importResult,
      interestStats,
      loadContacts,
      searchContacts,
      resetSearch,
      prevPage,
      nextPage,
      handleFileSelect,
      formatFileSize,
      importContacts,
      editContact,
      deleteContact,
      getInterestLevelClass,
      getInterestLevelText,
      getPercentage,
      getInterestBarClass,
      formatInterestLevel
    }
  }
}
</script>

<style scoped>
/* Add any additional styles here if needed */
</style>