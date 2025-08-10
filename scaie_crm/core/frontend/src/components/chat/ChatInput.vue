<template>
  <div class="border-t p-4 bg-white">
    <div class="flex">
      <input 
        v-model="message"
        @keyup.enter="sendMessage"
        type="text" 
        placeholder="Escribe tu mensaje aquí..." 
        class="flex-1 border rounded-l-lg p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
        :disabled="disabled"
      >
      <button 
        @click="sendMessage" 
        class="bg-blue-600 text-white px-6 py-3 rounded-r-lg hover:bg-blue-700 disabled:opacity-50 transition duration-200 flex items-center"
        :disabled="disabled || !message.trim()"
      >
        <span v-if="!sending">Enviar</span>
        <span v-else class="flex items-center">
          <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          Enviando...
        </span>
      </button>
    </div>
  </div>
</template>

<script>
import { ref, watch } from 'vue'

export default {
  name: 'ChatInput',
  props: {
    disabled: {
      type: Boolean,
      default: false
    },
    sending: {
      type: Boolean,
      default: false
    }
  },
  emits: ['send'],
  setup(props, { emit }) {
    const message = ref('')
    
    const sendMessage = () => {
      if (!message.value.trim() || props.disabled || props.sending) return
      
      emit('send', message.value)
      message.value = ''
    }
    
    // Clear message when disabled
    watch(() => props.disabled, (newDisabled) => {
      if (newDisabled) {
        message.value = ''
      }
    })
    
    return {
      message,
      sendMessage
    }
  }
}
</script>