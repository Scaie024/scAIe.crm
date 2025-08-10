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
                  @input="searchContacts"
                >
              </div>
              <div class="flex space-x-2">
                <select v-model="filterInterest" class="input" @change="searchContacts">
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
                <tr v-for="contact in contacts" :key="contact.id" class="hover:bg-gray-50" @click="selectContact(contact)" :class="{ 'bg-blue-50': selectedContact && selectedContact.id === contact.id }">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm font-medium text-gray-900">{{ contact.name }}</div>
                    <div class="text-xs text-gray-500" v-if="contact.platform">
                      <span class="inline-flex items-center">
                        <span class="w-2 h-2 rounded-full bg-blue-500 mr-1"></span>
                        {{ contact.platform }}
                      </span>
                    </div>
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
                    <button @click.stop="openEditModal(contact)" class="text-primary-600 hover:text-primary-900 mr-3">
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                      </svg>
                    </button>
                    <button @click.stop="deleteContact(contact.id)" class="text-danger-600 hover:text-danger-900">
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                      </svg>
                    </button>
                  </td>
                </tr>
                <tr v-if="contacts.length === 0">
                  <td colspan="5" class="px-6 py-4 text-center text-sm text-gray-500">
                    {{ loading ? 'Cargando contactos...' : 'No se encontraron contactos' }}
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
                @click="prevPage" 
                :disabled="currentPage === 1"
                class="px-3 py-1 rounded-md text-sm font-medium"
                :class="currentPage === 1 ? 'text-gray-400 cursor-not-allowed' : 'text-gray-700 hover:bg-gray-100'"
              >
                Anterior
              </button>
              <button 
                @click="nextPage" 
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
                  <p class="text-sm">{{ selectedContact.email || 'No especificado' }}</p>
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
                
                <div v-if="selectedContact.platform">
                  <p class="text-xs text-gray-500 uppercase tracking-wide">Plataforma</p>
                  <p class="text-sm capitalize">{{ selectedContact.platform }}</p>
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
    
    <!-- Add Contact Modal -->
    <div v-if="showAddModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-lg w-full max-w-md">
        <div class="p-5 border-b border-gray-200">
          <h3 class="text-lg font-semibold">Agregar Nuevo Contacto</h3>
        </div>
        <div class="p-5 space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Nombre *</label>
            <input v-model="newContact.name" type="text" class="input w-full" required>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Teléfono</label>
            <input v-model="newContact.phone" type="text" class="input w-full">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input v-model="newContact.email" type="email" class="input w-full">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Empresa</label>
            <input v-model="newContact.company" type="text" class="input w-full">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Nivel de Interés</label>
            <select v-model="newContact.interest_level" class="input w-full">
              <option value="nuevo">Nuevo</option>
              <option value="contactado">Contactado</option>
              <option value="interesado">Interesado</option>
              <option value="confirmado">Confirmado</option>
              <option value="no_interesado">No Interesado</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Notas</label>
            <textarea v-model="newContact.notes" class="input w-full" rows="3"></textarea>
          </div>
        </div>
        <div class="p-5 border-t border-gray-200 flex justify-end space-x-2">
          <button @click="showAddModal = false" class="btn btn-outline">Cancelar</button>
          <button @click="saveNewContact" class="btn btn-primary">Guardar</button>
        </div>
      </div>
    </div>
    
    <!-- Edit Contact Modal -->
    <div v-if="showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-lg w-full max-w-md">
        <div class="p-5 border-b border-gray-200">
          <h3 class="text-lg font-semibold">Editar Contacto</h3>
        </div>
        <div class="p-5 space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Nombre *</label>
            <input v-model="editContactData.name" type="text" class="input w-full" required>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Teléfono</label>
            <input v-model="editContactData.phone" type="text" class="input w-full">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input v-model="editContactData.email" type="email" class="input w-full">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Empresa</label>
            <input v-model="editContactData.company" type="text" class="input w-full">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Nivel de Interés</label>
            <select v-model="editContactData.interest_level" class="input w-full">
              <option value="nuevo">Nuevo</option>
              <option value="contactado">Contactado</option>
              <option value="interesado">Interesado</option>
              <option value="confirmado">Confirmado</option>
              <option value="no_interesado">No Interesado</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Notas</label>
            <textarea v-model="editContactData.notes" class="input w-full" rows="3"></textarea>
          </div>
        </div>
        <div class="p-5 border-t border-gray-200 flex justify-end space-x-2">
          <button @click="showEditModal = false" class="btn btn-outline">Cancelar</button>
          <button @click="updateContact" class="btn btn-primary">Actualizar</button>
        </div>
      </div>
    </div>
    
    <!-- Import Modal -->
    <div v-if="showImportModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-lg w-full max-w-md">
        <div class="p-5 border-b border-gray-200">
          <h3 class="text-lg font-semibold">Importar Contactos</h3>
        </div>
        <div class="p-5">
          <div class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
            <input type="file" @change="handleFileSelect" accept=".csv,.json" class="hidden" id="fileInput">
            <label for="fileInput" class="cursor-pointer">
              <svg class="w-12 h-12 mx-auto text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
              </svg>
              <p class="mt-2 text-sm text-gray-600">
                <span class="font-medium text-primary-600">Haz clic para seleccionar</span> un archivo
              </p>
              <p class="text-xs text-gray-500">Formatos soportados: CSV, JSON</p>
            </label>
          </div>
          
          <div v-if="selectedFile" class="mt-4 p-3 bg-gray-50 rounded-lg">
            <div class="flex justify-between">
              <div>
                <p class="text-sm font-medium text-gray-900">{{ selectedFile.name }}</p>
                <p class="text-xs text-gray-500">{{ formatFileSize(selectedFile.size) }}</p>
              </div>
              <button @click="selectedFile = null" class="text-gray-400 hover:text-gray-500">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
              </button>
            </div>
          </div>
          
          <div v-if="importResult" class="mt-4 p-3 rounded-lg" :class="importResult.success ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'">
            <p class="text-sm">{{ importResult.message }}</p>
            <p v-if="importResult.imported_count !== undefined" class="text-xs mt-1">Contactos importados: {{ importResult.imported_count }}</p>
          </div>
        </div>
        <div class="p-5 border-t border-gray-200 flex justify-end space-x-2">
          <button @click="showImportModal = false" class="btn btn-outline">Cancelar</button>
          <button @click="importContacts" :disabled="!selectedFile || importing" class="btn btn-primary" :class="{ 'opacity-50 cursor-not-allowed': !selectedFile || importing }">
            {{ importing ? 'Importando...' : 'Importar' }}
          </button>
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
      no_interesado: 0,
      nuevo: 0,
      confirmado: 0
    })
    
    const searchQuery = ref('')
    const filterInterest = ref('')
    const currentPage = ref(1)
    const pageSize = ref(10)
    const totalContacts = ref(0)
    const loading = ref(false)
    const error = ref('')
    
    const selectedFile = ref(null)
    const importing = ref(false)
    const importResult = ref(null)
    const selectedContact = ref(null)
    const showAddModal = ref(false)
    const showEditModal = ref(false)
    const showImportModal = ref(false)
    
    const newContact = ref({
      name: '',
      phone: '',
      email: '',
      company: '',
      notes: '',
      interest_level: 'nuevo'
    })
    
    const editContactData = ref({
      name: '',
      phone: '',
      email: '',
      company: '',
      notes: '',
      interest_level: 'nuevo'
    })
    
    // Load contacts
  const loadContacts = async () => {
      loading.value = true
      error.value = ''
      
      try {
  const response = await api.getContacts(currentPage.value, pageSize.value, searchQuery.value, filterInterest.value)
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
    
    // Helper functions
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
    
    // Export contacts
    const exportContacts = async () => {
      try {
        const blob = await api.exportContacts()
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `contacts_export_${new Date().toISOString().split('T')[0]}.csv`
        document.body.appendChild(a)
        a.click()
        window.URL.revokeObjectURL(url)
        document.body.removeChild(a)
      } catch (err) {
        console.error('Error exporting contacts:', err)
        alert('Error al exportar contactos: ' + (err.message || 'Error desconocido'))
      }
    }
    
    // Modal functions
    const openAddModal = () => {
      newContact.value = {
        name: '',
        phone: '',
        email: '',
        company: '',
        notes: '',
        interest_level: 'nuevo'
      }
      showAddModal.value = true
    }
    
    const openEditModal = (contact) => {
      editContactData.value = { ...contact }
      showEditModal.value = true
    }
    
    const openImportModal = () => {
      selectedFile.value = null
      importResult.value = null
      showImportModal.value = true
    }
    
    const saveNewContact = async () => {
      if (!newContact.value.name) {
        alert('El nombre es requerido')
        return
      }
      
      try {
        await api.createContact(newContact.value)
        showAddModal.value = false
        await loadContacts()
        await loadStats()
        alert('Contacto creado exitosamente')
      } catch (err) {
        console.error('Error creating contact:', err)
        alert('Error al crear contacto: ' + (err.message || 'Error desconocido'))
      }
    }
    
    const updateContact = async () => {
      if (!editContactData.value.name) {
        alert('El nombre es requerido')
        return
      }
      
      try {
        await api.updateContact(editContactData.value.id, editContactData.value)
        showEditModal.value = false
        await loadContacts()
        await loadStats()
        alert('Contacto actualizado exitosamente')
      } catch (err) {
        console.error('Error updating contact:', err)
        alert('Error al actualizar contacto: ' + (err.message || 'Error desconocido'))
      }
    }
    
    // Select contact for details panel
    const selectContact = (contact) => {
      selectedContact.value = contact
    }
    
    // Contact actions
    const deleteContact = async (contactId) => {
      if (!confirm('¿Estás seguro de que deseas eliminar este cliente?')) return
      
      try {
        await api.deleteContact(contactId)
        // Clear selected contact if it was the deleted one
        if (selectedContact.value && selectedContact.value.id === contactId) {
          selectedContact.value = null
        }
        // Reload contacts and stats
        await loadContacts()
        await loadStats()
        alert('Cliente eliminado exitosamente')
      } catch (err) {
        console.error('Error deleting contact:', err)
        alert('Error al eliminar cliente: ' + (err.message || 'Error desconocido'))
      }
    }
    
    const formatDate = (date) => {
      if (!date) return 'N/A'
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
      filterInterest,
      currentPage,
      pageSize,
      totalContacts,
      loading,
      error,
      selectedFile,
      importing,
      importResult,
      selectedContact,
      showAddModal,
      showEditModal,
      showImportModal,
      newContact,
      editContactData,
      loadContacts,
      searchContacts,
      prevPage,
      nextPage,
      handleFileSelect,
      formatFileSize,
      importContacts,
      exportContacts,
      openAddModal,
      openEditModal,
      openImportModal,
      saveNewContact,
      updateContact,
      deleteContact,
      selectContact,
      formatInterestLevel,
      formatDate
    }
  }
}
</script>

<style scoped>
/* Add any additional styles here if needed */
</style>
