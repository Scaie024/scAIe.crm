<template>
  <div>
    <div class="mb-4">
      <label class="block text-sm font-medium text-gray-700 mb-2">Seleccionar archivo CSV o JSON</label>
      <input 
        type="file" 
        @change="handleFileSelect"
        :accept="acceptedFileTypes"
        class="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
      >
      <p class="mt-1 text-sm text-gray-500">
        El archivo debe tener columnas: nombre, teléfono, email, empresa (para CSV)
      </p>
    </div>
    
    <div v-if="fileSelected" class="bg-blue-50 p-4 rounded-lg mb-4">
      <h4 class="font-medium text-blue-800 mb-2">Archivo seleccionado</h4>
      <p class="text-sm text-blue-700">{{ fileName }}</p>
      <p class="text-xs text-blue-600 mt-1">{{ fileSize }}</p>
    </div>
    
    <div class="flex justify-end space-x-3">
      <button 
        type="button"
        @click="$emit('cancel')"
        class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200"
      >
        Cancelar
      </button>
      <button 
        type="button"
        @click="importContacts"
        :disabled="!fileSelected || importing"
        class="px-4 py-2 text-sm font-medium text-white bg-green-600 rounded-md hover:bg-green-700 disabled:opacity-50 flex items-center"
      >
        <svg v-if="importing" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <span>{{ importing ? 'Importando...' : 'Importar Contactos' }}</span>
      </button>
    </div>
    
    <div v-if="importResult" class="mt-4 p-4 rounded-lg" :class="{
      'bg-green-50 text-green-800': importResult.success,
      'bg-red-50 text-red-800': !importResult.success
    }">
      <h4 class="font-medium mb-2">{{ importResult.success ? 'Importación exitosa' : 'Error en la importación' }}</h4>
      <p class="text-sm">{{ importResult.message }}</p>
      <p v-if="importResult.imported_count !== undefined" class="text-sm mt-1">
        Contactos importados: {{ importResult.imported_count }}
      </p>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  name: 'ContactImport',
  emits: ['import', 'cancel'],
  setup(props, { emit }) {
    const selectedFile = ref(null)
    const importing = ref(false)
    const importResult = ref(null)
    
    const acceptedFileTypes = '.csv,.json'
    
    const fileSelected = computed(() => !!selectedFile.value)
    
    const fileName = computed(() => {
      return selectedFile.value ? selectedFile.value.name : ''
    })
    
    const fileSize = computed(() => {
      if (!selectedFile.value) return ''
      const size = selectedFile.value.size
      if (size < 1024) return `${size} bytes`
      if (size < 1024 * 1024) return `${(size / 1024).toFixed(1)} KB`
      return `${(size / (1024 * 1024)).toFixed(1)} MB`
    })
    
    const handleFileSelect = (event) => {
      const file = event.target.files[0]
      if (file) {
        selectedFile.value = file
        importResult.value = null
      }
    }
    
    const importContacts = () => {
      if (!selectedFile.value) return
      
      importing.value = true
      importResult.value = null
      
      emit('import', selectedFile.value)
    }
    
    const setImportResult = (result) => {
      importing.value = false
      importResult.value = result
      
      // Clear file input if successful
      if (result.success) {
        selectedFile.value = null
      }
    }
    
    return {
      selectedFile,
      importing,
      importResult,
      acceptedFileTypes,
      fileSelected,
      fileName,
      fileSize,
      handleFileSelect,
      importContacts,
      setImportResult
    }
  }
}
</script>