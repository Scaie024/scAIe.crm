<template>
  <div class="database">
    <div class="bg-gradient-to-r from-secondary-600 to-teal-600 text-white p-6 rounded-2xl shadow-soft mb-6">
      <h1 class="text-2xl font-bold">Administración de Base de Datos</h1>
      <p class="text-secondary-100">Gestión completa de clientes y contactos</p>
    </div>
    
    <!-- Estadísticas generales -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
      <div class="card">
        <div class="p-5">
          <div class="text-gray-500 text-sm mb-1">Total Contactos</div>
          <div class="text-2xl font-bold">{{ stats.total || 0 }}</div>
        </div>
      </div>
      <div class="card">
        <div class="p-5">
          <div class="text-gray-500 text-sm mb-1">Interesados</div>
          <div class="text-2xl font-bold text-success-600">{{ stats.interesado || 0 }}</div>
        </div>
      </div>
      <div class="card">
        <div class="p-5">
          <div class="text-gray-500 text-sm mb-1">Contactados</div>
          <div class="text-2xl font-bold text-primary-600">{{ stats.contactado || 0 }}</div>
        </div>
      </div>
      <div class="card">
        <div class="p-5">
          <div class="text-gray-500 text-sm mb-1">No Interesados</div>
          <div class="text-2xl font-bold text-danger-600">{{ stats.no_interesado || 0 }}</div>
        </div>
      </div>
    </div>
    
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Panel de búsqueda y acciones -->
      <div class="lg:col-span-2">
        <div class="card mb-6">
          <div class="p-5 border-b border-gray-200">
            <div class="flex flex-col md:flex-row md:items-center md:justify-between">
              <h2 class="text-lg font-semibold">Lista de Clientes</h2>
              <div class="mt-2 md:mt-0 flex space-x-2">
                <button @click="openImportModal" class="btn btn-outline text-sm">
                  <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3V10"></path>
                  </svg>
                  Importar
                </button>
                <button @click="exportContacts" class="btn btn-outline text-sm">
                  <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path>
                  </svg>
                  Exportar
                </button>
                <button @click="openAddModal" class="btn btn-primary text-sm">
                  <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
                  </svg>
                  Nuevo
                </button>
              </div>
            </div>
          </div>
          
          <div class="p-5 border-b border-gray-200">
            <div class="flex flex-col md:flex-row md:items-center md:justify-between">
              <div class="w-full md:w-64 mb-3 md:mb-0">
                <input 
                  v-model="searchQuery" 
                  type="text" 
                  placeholder="Buscar contactos..." 
                  class="input w-full"
                >
              </div>
              <div class="flex space-x-2">
                <select v-model="filterInterest" class="input">
                  <option value="">Todos los niveles</option>
                  <option value="nuevo">Nuevo</option>
                  <option value="contactado">Contactado</option>
                  <option value="interesado">Interesado</option>
                  <option value="confirmado">Confirmado</option>
                  <option value="no_interesado">No Interesado</option>
                </select>
              </div>
            </div>
          </div>
          
          <!-- Lista de contactos -->
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nombre</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Contacto</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Empresa</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nivel de interés</th>
                  <th scope="col" class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Acciones</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="contact in filteredContacts" :key="contact.id" class="hover:bg-gray-50">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm font-medium text-gray-900">{{ contact.name }}</div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm text-gray-900">{{ contact.email }}</div>
                    <div class="text-sm text-gray-500">{{ contact.phone }}</div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ contact.company }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span 
                      class="badge" 
                      :class="{
                        'badge-primary': contact.interest_level === 'nuevo',
                        'badge-warning': contact.interest_level === 'contactado',
                        'badge-success': contact.interest_level === 'interesado',
                        'badge-secondary': contact.interest_level === 'confirmado',
                        'badge-danger': contact.interest_level === 'no_interesado'
                      }"
                    >
                      {{ formatInterestLevel(contact.interest_level) }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <button @click="openEditModal(contact)" class="text-primary-600 hover:text-primary-900 mr-3">
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                      </svg>
                    </button>
                    <button @click="deleteContact(contact.id)" class="text-danger-600 hover:text-danger-900">
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                      </svg>
                    </button>
                  </td>
                </tr>
                <tr v-if="filteredContacts.length === 0">
                  <td colspan="5" class="px-6 py-4 text-center text-sm text-gray-500">
                    No se encontraron contactos
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <!-- Paginación -->
          <div class="px-5 py-4 border-t border-gray-200 flex items-center justify-between">
            <div class="text-sm text-gray-700">
              Mostrando <span class="font-medium">{{ (currentPage - 1) * pageSize + 1 }}</span> a 
              <span class="font-medium">{{ Math.min(currentPage * pageSize, totalContacts) }}</span> de 
              <span class="font-medium">{{ totalContacts }}</span> resultados
            </div>
            <div class="flex space-x-2">
              <button 
                @click="currentPage--" 
                :disabled="currentPage === 1"
                class="px-3 py-1 rounded-md text-sm font-medium"
                :class="currentPage === 1 ? 'text-gray-400 cursor-not-allowed' : 'text-gray-700 hover:bg-gray-100'"
              >
                Anterior
              </button>
              <button 
                @click="currentPage++" 
                :disabled="currentPage * pageSize >= totalContacts"
                class="px-3 py-1 rounded-md text-sm font-medium"
                :class="currentPage * pageSize >= totalContacts ? 'text-gray-400 cursor-not-allowed' : 'text-gray-700 hover:bg-gray-100'"
              >
                Siguiente
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Panel de detalles -->
      <div class="lg:col-span-1">
        <div class="card sticky top-6">
          <div class="p-5">
            <h3 class="text-lg font-semibold mb-4">Detalles del Contacto</h3>
            <div v-if="selectedContact">
              <div class="flex items-center mb-4">
                <div class="w-12 h-12 rounded-full bg-primary-100 flex items-center justify-center text-primary-800 font-bold mr-3">
                  {{ selectedContact.name.charAt(0) }}
                </div>
                <div>
                  <h4 class="font-medium">{{ selectedContact.name }}</h4>
                  <p class="text-sm text-gray-500">{{ selectedContact.company }}</p>
                </div>
              </div>
              
              <div class="space-y-3">
                <div>
                  <p class="text-xs text-gray-500 uppercase tracking-wide">Email</p>
                  <p class="text-sm">{{ selectedContact.email }}</p>
                </div>
                
                <div v-if="selectedContact.phone">
                  <p class="text-xs text-gray-500 uppercase tracking-wide">Teléfono</p>
                  <p class="text-sm">{{ selectedContact.phone }}</p>
                </div>
                
                <div>
                  <p class="text-xs text-gray-500 uppercase tracking-wide">Nivel de interés</p>
                  <span 
                    class="badge" 
                    :class="{
                      'badge-primary': selectedContact.interest_level === 'nuevo',
                      'badge-warning': selectedContact.interest_level === 'contactado',
                      'badge-success': selectedContact.interest_level === 'interesado',
                      'badge-secondary': selectedContact.interest_level === 'confirmado',
                      'badge-danger': selectedContact.interest_level === 'no_interesado'
                    }"
                  >
                    {{ formatInterestLevel(selectedContact.interest_level) }}
                  </span>
                </div>
                
                <div v-if="selectedContact.notes">
                  <p class="text-xs text-gray-500 uppercase tracking-wide">Notas</p>
                  <p class="text-sm">{{ selectedContact.notes }}</p>
                </div>
                
                <div>
                  <p class="text-xs text-gray-500 uppercase tracking-wide">Fecha de creación</p>
                  <p class="text-sm">{{ formatDate(selectedContact.created_at) }}</p>
                </div>
              </div>
            </div>
            <div v-else class="text-center py-8 text-gray-500">
              <svg class="w-12 h-12 mx-auto text-gray-300 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
              </svg>
              <p>Selecciona un contacto para ver los detalles</p>
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
    
    const filteredContacts = computed(() => {
      return contacts.value.filter(contact => {
        const matchesSearch = contact.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
          contact.email.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
          contact.phone.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
          contact.company.toLowerCase().includes(searchQuery.value.toLowerCase())
        const matchesInterest = filterInterest.value === '' || contact.interest_level === filterInterest.value
        return matchesSearch && matchesInterest
      })
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
    
    const formatDate = (date) => {
      const options = { year: 'numeric', month: 'long', day: 'numeric' }
      return new Date(date).toLocaleDateString(undefined, options)
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
      formatInterestLevel,
      formatDate
    }
  }
}
</script>

<style scoped>
/* Add any additional styles here if needed */
</style>