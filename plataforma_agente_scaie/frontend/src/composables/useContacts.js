import { ref, reactive } from 'vue'
import api from '../services/api.js'

export function useContacts() {
  const contacts = ref([])
  const stats = ref({
    total: 0,
    interesado: 0,
    contactado: 0,
    no_interesado: 0
  })
  
  const loading = ref(false)
  const error = ref('')
  
  const pagination = reactive({
    currentPage: 1,
    pageSize: 10,
    total: 0
  })
  
  const searchQuery = ref('')
  
  const loadContacts = async (page = pagination.currentPage, size = pagination.pageSize, search = searchQuery.value) => {
    loading.value = true
    error.value = ''
    
    try {
      const response = await api.getContacts(page, size, search)
      contacts.value = response.contacts || []
      pagination.total = response.total || 0
      pagination.currentPage = page
      pagination.pageSize = size
      return response
    } catch (err) {
      error.value = err.message || 'Error al cargar los contactos'
      throw err
    } finally {
      loading.value = false
    }
  }
  
  const loadStats = async () => {
    try {
      const statsResponse = await api.getContactStats()
      stats.value = {
        total: statsResponse.total || 0,
        interesado: statsResponse.interest_level_distribution?.interesado || 0,
        contactado: statsResponse.interest_level_distribution?.contactado || 0,
        no_interesado: statsResponse.interest_level_distribution?.no_interesado || 0
      }
      return statsResponse
    } catch (err) {
      error.value = err.message || 'Error al cargar las estadísticas'
      throw err
    }
  }
  
  const createContact = async (contactData) => {
    try {
      const newContact = await api.createContact(contactData)
      // Reload contacts and stats after creation
      await loadContacts()
      await loadStats()
      return newContact
    } catch (err) {
      error.value = err.message || 'Error al crear el contacto'
      throw err
    }
  }
  
  const updateContact = async (contactId, contactData) => {
    try {
      const updatedContact = await api.updateContact(contactId, contactData)
      // Reload contacts and stats after update
      await loadContacts()
      await loadStats()
      return updatedContact
    } catch (err) {
      error.value = err.message || 'Error al actualizar el contacto'
      throw err
    }
  }
  
  const deleteContact = async (contactId) => {
    try {
      const result = await api.deleteContact(contactId)
      // Reload contacts and stats after deletion
      await loadContacts()
      await loadStats()
      return result
    } catch (err) {
      error.value = err.message || 'Error al eliminar el contacto'
      throw err
    }
  }
  
  const importContacts = async (file) => {
    try {
      const result = await api.importContacts(file)
      // Reload contacts and stats after import
      await loadContacts()
      await loadStats()
      return result
    } catch (err) {
      error.value = err.message || 'Error al importar contactos'
      throw err
    }
  }
  
  const searchContacts = async (query) => {
    searchQuery.value = query
    pagination.currentPage = 1
    return await loadContacts()
  }
  
  const resetSearch = async () => {
    searchQuery.value = ''
    pagination.currentPage = 1
    return await loadContacts()
  }
  
  const goToPage = async (page) => {
    if (page >= 1 && page <= Math.ceil(pagination.total / pagination.pageSize)) {
      return await loadContacts(page)
    }
  }
  
  const nextPage = async () => {
    if (pagination.currentPage * pagination.pageSize < pagination.total) {
      return await loadContacts(pagination.currentPage + 1)
    }
  }
  
  const prevPage = async () => {
    if (pagination.currentPage > 1) {
      return await loadContacts(pagination.currentPage - 1)
    }
  }
  
  return {
    // State
    contacts,
    stats,
    loading,
    error,
    pagination,
    searchQuery,
    
    // Methods
    loadContacts,
    loadStats,
    createContact,
    updateContact,
    deleteContact,
    importContacts,
    searchContacts,
    resetSearch,
    goToPage,
    nextPage,
    prevPage
  }
}