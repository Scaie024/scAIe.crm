<template>
  <form @submit.prevent="submitForm" class="space-y-6">
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">Nombre *</label>
      <input 
        v-model="formData.name" 
        type="text" 
        class="w-full border rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
        :class="{ 'border-red-500': errors.name }"
        placeholder="Nombre completo"
        required
      >
      <p v-if="errors.name" class="mt-1 text-sm text-red-600">{{ errors.name }}</p>
    </div>
    
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">Teléfono *</label>
      <input 
        v-model="formData.phone" 
        type="tel" 
        class="w-full border rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
        :class="{ 'border-red-500': errors.phone }"
        placeholder="+52 55 1234 5678"
        required
      >
      <p v-if="errors.phone" class="mt-1 text-sm text-red-600">{{ errors.phone }}</p>
    </div>
    
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
      <input 
        v-model="formData.email" 
        type="email" 
        class="w-full border rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
        :class="{ 'border-red-500': errors.email }"
        placeholder="correo@ejemplo.com"
      >
      <p v-if="errors.email" class="mt-1 text-sm text-red-600">{{ errors.email }}</p>
    </div>
    
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">Empresa</label>
      <input 
        v-model="formData.company" 
        type="text" 
        class="w-full border rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
        placeholder="Nombre de la empresa"
      >
    </div>
    
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">Nivel de Interés</label>
      <select 
        v-model="formData.interest_level" 
        class="w-full border rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option value="nuevo">Nuevo</option>
        <option value="contactado">Contactado</option>
        <option value="interesado">Interesado</option>
        <option value="confirmado">Confirmado</option>
        <option value="no_interesado">No Interesado</option>
      </select>
    </div>
    
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">Notas</label>
      <textarea 
        v-model="formData.notes" 
        rows="3"
        class="w-full border rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
        placeholder="Notas adicionales sobre el contacto"
      ></textarea>
    </div>
    
    <div class="flex justify-end space-x-3 pt-4">
      <button 
        type="button" 
        @click="$emit('cancel')"
        class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200"
      >
        Cancelar
      </button>
      <button 
        type="submit" 
        :disabled="submitting"
        class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 disabled:opacity-50 flex items-center"
      >
        <svg v-if="submitting" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <span>{{ submitting ? 'Guardando...' : isEditing ? 'Actualizar' : 'Crear' }}</span>
      </button>
    </div>
  </form>
</template>

<script>
import { ref, reactive, watch } from 'vue'

export default {
  name: 'ContactForm',
  props: {
    contact: {
      type: Object,
      default: null
    },
    submitting: {
      type: Boolean,
      default: false
    }
  },
  emits: ['save', 'cancel'],
  setup(props, { emit }) {
    const isEditing = ref(false)
    const errors = ref({})
    
    const formData = reactive({
      name: '',
      phone: '',
      email: '',
      company: '',
      interest_level: 'nuevo',
      notes: ''
    })
    
    // Initialize form with contact data if editing
    watch(() => props.contact, (newContact) => {
      if (newContact) {
        isEditing.value = true
        Object.assign(formData, newContact)
      } else {
        isEditing.value = false
        // Reset form
        Object.assign(formData, {
          name: '',
          phone: '',
          email: '',
          company: '',
          interest_level: 'nuevo',
          notes: ''
        })
      }
    }, { immediate: true })
    
    const validateForm = () => {
      errors.value = {}
      
      if (!formData.name.trim()) {
        errors.value.name = 'El nombre es obligatorio'
      }
      
      if (!formData.phone.trim()) {
        errors.value.phone = 'El teléfono es obligatorio'
      } else if (!/^\+?[\d\s\-\(\)]+$/.test(formData.phone)) {
        errors.value.phone = 'Formato de teléfono inválido'
      }
      
      if (formData.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
        errors.value.email = 'Formato de email inválido'
      }
      
      return Object.keys(errors.value).length === 0
    }
    
    const submitForm = () => {
      if (validateForm()) {
        emit('save', { ...formData })
      }
    }
    
    return {
      isEditing,
      errors,
      formData,
      submitForm
    }
  }
}
</script>