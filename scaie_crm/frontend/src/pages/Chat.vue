<template>
  <div class="chat-test flex flex-col h-full">
    <div class="bg-gradient-to-r from-blue-600 to-indigo-700 text-white p-4 rounded-t-lg">
      <h1 class="text-2xl font-bold">Chat de Pruebas del Agente</h1>
      <p class="text-blue-100">Prueba las capacidades del agente de ventas automatizadas</p>
    </div>
    
    <div class="flex-1 flex flex-col md:flex-row">
      <!-- Panel lateral con información del agente -->
      <div class="w-full md:w-80 bg-gray-50 p-4 border-r">
        <div class="bg-white rounded-lg shadow p-4 mb-4">
          <h2 class="font-bold text-lg mb-2">Agente SCAI</h2>
          <div class="flex items-center mb-3">
            <div class="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
            <span class="text-sm">En línea</span>
          </div>
          <p class="text-sm text-gray-600 mb-3">
            Asistente virtual especializado en ventas automatizadas de scaie.com.mx
          </p>
          <button @click="resetConversation" class="w-full bg-blue-100 hover:bg-blue-200 text-blue-700 py-2 px-3 rounded text-sm transition duration-200">
            Reiniciar Conversación
          </button>
        </div>
        
        <div class="bg-white rounded-lg shadow p-4 mb-4">
          <h3 class="font-semibold mb-2">Información del Cliente</h3>
          <div class="space-y-2">
            <div>
              <label class="block text-xs text-gray-500">Nombre</label>
              <input 
                v-model="customerInfo.name" 
                type="text" 
                class="w-full border rounded p-1 text-sm"
                placeholder="Nombre del cliente"
              >
            </div>
            <div>
              <label class="block text-xs text-gray-500">Teléfono</label>
              <input 
                v-model="customerInfo.phone" 
                type="text" 
                class="w-full border rounded p-1 text-sm"
                placeholder="+52 55 1234 5678"
              >
            </div>
            <div>
              <label class="block text-xs text-gray-500">Empresa</label>
              <input 
                v-model="customerInfo.company" 
                type="text" 
                class="w-full border rounded p-1 text-sm"
                placeholder="Nombre de la empresa"
              >
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-lg shadow p-4">
          <h3 class="font-semibold mb-2">Capacidades del Agente</h3>
          <ul class="text-sm text-gray-600 space-y-1">
            <li class="flex items-start">
              <svg class="w-4 h-4 text-green-500 mr-1 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
              </svg>
              <span>Ventas automatizadas de scaie.com.mx</span>
            </li>
            <li class="flex items-start">
              <svg class="w-4 h-4 text-green-500 mr-1 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
              </svg>
              <span>Respuestas personalizadas</span>
            </li>
            <li class="flex items-start">
              <svg class="w-4 h-4 text-green-500 mr-1 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
              </svg>
              <span>Integración con WhatsApp, Facebook, etc.</span>
            </li>
            <li class="flex items-start">
              <svg class="w-4 h-4 text-green-500 mr-1 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
              </svg>
              <span>Seguimiento de clientes interesados</span>
            </li>
          </ul>
        </div>
      </div>
      
      <!-- Área principal de chat -->
      <div class="flex-1 flex flex-col">
        <div ref="chatContainer" class="flex-1 overflow-y-auto p-4 bg-white">
          <div v-if="messages.length === 0" class="flex flex-col items-center justify-center h-full text-gray-500">
            <div class="bg-gray-200 border-2 border-dashed rounded-xl w-16 h-16 mb-4"></div>
            <p class="text-lg mb-2">¡Bienvenido al Chat de Pruebas!</p>
            <p class="text-center max-w-md">Esta es una prueba del agente de ventas automatizadas de SCAIE. Puedes simular conversaciones con clientes potenciales interesados en los servicios de scaie.com.mx.</p>
          </div>
          
          <div v-for="(message, index) in messages" :key="index" class="mb-4">
            <div :class="[
              'flex',
              message.sender === 'user' ? 'justify-end' : 'justify-start'
            ]">
              <div :class="[
                'max-w-xs md:max-w-md lg:max-w-lg rounded-lg p-4',
                message.sender === 'user' 
                  ? 'bg-blue-500 text-white rounded-br-none' 
                  : 'bg-gray-200 text-gray-800 rounded-bl-none'
              ]">
                <div class="font-semibold mb-1" v-if="message.sender === 'agent'">
                  <div class="flex items-center">
                    <div class="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                    SCAI
                  </div>
                </div>
                <div class="font-semibold mb-1" v-if="message.sender === 'user'">Tú</div>
                <div class="whitespace-pre-wrap">{{ message.content }}</div>
                <div class="text-xs opacity-75 mt-1 text-right">{{ formatTime(message.created_at) }}</div>
              </div>
            </div>
          </div>
          
          <!-- Loading indicator -->
          <div v-if="loading" class="mb-4 flex justify-start">
            <div class="max-w-xs md:max-w-md lg:max-w-lg rounded-lg p-4 bg-gray-200 text-gray-800 rounded-bl-none">
              <div class="font-semibold mb-1">
                <div class="flex items-center">
                  <div class="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                  SCAI
                </div>
              </div>
              <div class="flex space-x-2">
                <div class="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                <div class="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                <div class="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style="animation-delay: 0.4s"></div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="border-t p-4 bg-white">
          <div class="flex">
            <input 
              v-model="newMessage"
              @keyup.enter="sendMessage"
              type="text" 
              placeholder="Escribe tu mensaje de prueba aquí..." 
              class="flex-1 border rounded-l-lg p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
              :disabled="loading"
            >
            <button 
              @click="sendMessage" 
              class="bg-blue-600 text-white px-6 py-3 rounded-r-lg hover:bg-blue-700 disabled:opacity-50 transition duration-200 flex items-center"
              :disabled="loading || !newMessage.trim()"
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
          
          <div class="mt-2 text-sm text-gray-500">
            <p>Ejemplos de mensajes para probar:</p>
            <ul class="list-disc list-inside">
              <li>"Quiero información sobre SCAIE"</li>
              <li>"¿Cómo funciona el sistema de ventas automatizadas?"</li>
              <li>"¿Qué precio tiene el servicio?"</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, watch, onMounted, nextTick } from 'vue'

export default {
  name: 'ChatTest',
  setup() {
    const chatContainer = ref(null)
    const messages = ref([])
    const newMessage = ref('')
    const loading = ref(false)
    const sending = ref(false)
    
    const customerInfo = ref({
      name: 'Cliente de Prueba',
      phone: '+525512345678',
      company: 'Empresa de Prueba'
    })
    
    // Scroll to bottom of chat
    const scrollToBottom = () => {
      nextTick(() => {
        if (chatContainer.value) {
          chatContainer.value.scrollTop = chatContainer.value.scrollHeight
        }
      })
    }
    
    // Format time for messages
    const formatTime = (dateString) => {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
    
    // Send message to backend
    const sendMessage = async () => {
      if (!newMessage.value.trim() || loading.value) return
      
      // Add user message to chat
      const userMessage = {
        sender: 'user',
        content: newMessage.value,
        created_at: new Date().toISOString()
      }
      
      messages.value.push(userMessage)
      const messageToSend = newMessage.value
      newMessage.value = ''
      sending.value = true
      
      try {
        // Send message to backend using the omnipotent agent
        const response = await fetch('/api/omnipotent-agent/process-message', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            message: messageToSend,
            platform: "web",
            contact_info: {
              name: customerInfo.value.name,
              phone: customerInfo.value.phone,
              company: customerInfo.value.company
            }
          })
        })
        
        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}))
          throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
        }
        
        const data = await response.json()
        
        // Add agent response to chat
        const agentMessage = {
          sender: 'agent',
          content: data.response,
          created_at: new Date().toISOString()
        }
        
        messages.value.push(agentMessage)
      } catch (error) {
        console.error('Error sending message:', error)
        
        // Show error message
        const errorMessage = {
          sender: 'agent',
          content: 'Lo siento, ocurrió un error al procesar tu mensaje. Por favor, inténtalo de nuevo.',
          created_at: new Date().toISOString()
        }
        
        messages.value.push(errorMessage)
      } finally {
        sending.value = false
      }
    }
    
    // Reset conversation
    const resetConversation = () => {
      messages.value = []
      
      // Add welcome message
      setTimeout(() => {
        const welcomeMessage = {
          sender: 'agent',
          content: '¡Hola! Soy SCAI, tu asistente virtual especializado en ventas automatizadas de scaie.com.mx. ¿En qué puedo ayudarte hoy?',
          created_at: new Date().toISOString()
        }
        messages.value.push(welcomeMessage)
      }, 500)
    }
    
    // Initialize with welcome message
    onMounted(() => {
      // Add welcome message
      setTimeout(() => {
        const welcomeMessage = {
          sender: 'agent',
          content: '¡Hola! Soy SCAI, tu asistente virtual especializado en ventas automatizadas de scaie.com.mx. ¿En qué puedo ayudarte hoy?',
          created_at: new Date().toISOString()
        }
        messages.value.push(welcomeMessage)
      }, 500)
    })
    
    // Watch for new messages and scroll to bottom
    watch(() => messages.value, () => {
      scrollToBottom()
    }, { deep: true })
    
    // Scroll to bottom when loading changes
    watch(() => loading.value, () => {
      scrollToBottom()
    })
    
    return {
      chatContainer,
      messages,
      newMessage,
      loading,
      sending,
      customerInfo,
      formatTime,
      sendMessage,
      resetConversation,
      scrollToBottom
    }
  }
}

// Necesitamos importar watch desde vue
</script>

<style scoped>
.chat-test {
  height: calc(100vh - 200px);
}

.overflow-y-auto {
  scroll-behavior: smooth;
}
</style>