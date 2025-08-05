<template>
  <div class="sandbox flex flex-col h-full">
    <div class="bg-gradient-to-r from-purple-600 to-indigo-700 text-white p-4 rounded-t-lg">
      <h1 class="text-2xl font-bold">Sandbox de Pruebas</h1>
      <p class="text-purple-100">Prueba las respuestas del agente conversacional</p>
    </div>
    
    <div class="flex-1 flex flex-col md:flex-row">
      <!-- Panel de configuración y control -->
      <div class="w-full md:w-80 bg-gray-50 p-4 border-r">
        <div class="bg-white rounded-lg shadow p-4 mb-4">
          <h2 class="font-bold text-lg mb-2">Configuración</h2>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Nombre del Agente</label>
              <input 
                v-model="agentName"
                type="text" 
                class="w-full border rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
                placeholder="Nombre del agente"
              >
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Personalidad</label>
              <textarea 
                v-model="agentPersonality"
                rows="3"
                class="w-full border rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
                placeholder="Personalidad del agente"
              ></textarea>
            </div>
            
            <button 
              @click="resetContext" 
              class="w-full bg-purple-100 hover:bg-purple-200 text-purple-700 py-2 px-3 rounded text-sm transition duration-200"
            >
              Reiniciar Contexto
            </button>
          </div>
        </div>
        
        <div class="bg-white rounded-lg shadow p-4">
          <h3 class="font-semibold mb-2">Información de Contexto</h3>
          <div v-if="lastContext" class="text-sm text-gray-600 space-y-2">
            <div>
              <span class="font-medium">Modelo:</span> {{ lastContext.model }}
            </div>
            <div>
              <span class="font-medium">Tokens usados:</span> {{ lastContext.tokens_used }}
            </div>
            <div v-if="lastContext.context_used && lastContext.context_used.length > 0">
              <span class="font-medium">Contexto usado:</span>
              <ul class="list-disc pl-5 mt-1">
                <li v-for="(item, index) in lastContext.context_used" :key="index">
                  {{ item }}
                </li>
              </ul>
            </div>
          </div>
          <div v-else class="text-sm text-gray-500">
            Aún no hay contexto disponible
          </div>
        </div>
      </div>
      
      <!-- Área principal de chat -->
      <div class="flex-1 flex flex-col">
        <div ref="chatContainer" class="flex-1 overflow-y-auto p-4 bg-white">
          <div v-if="messages.length === 0" class="flex flex-col items-center justify-center h-full text-gray-500">
            <div class="bg-gray-200 border-2 border-dashed rounded-xl w-16 h-16 mb-4"></div>
            <p class="text-lg mb-2">Sandbox de Pruebas del Agente</p>
            <p class="text-center">Escribe un mensaje para probar cómo responde el agente conversacional.</p>
          </div>
          
          <div v-for="(message, index) in messages" :key="index" class="mb-4">
            <div :class="[
              'flex',
              message.sender === 'user' ? 'justify-end' : 'justify-start'
            ]">
              <div :class="[
                'max-w-xs md:max-w-md lg:max-w-lg rounded-lg p-4',
                message.sender === 'user' 
                  ? 'bg-purple-500 text-white rounded-br-none' 
                  : 'bg-gray-200 text-gray-800 rounded-bl-none'
              ]">
                <div class="font-semibold mb-1" v-if="message.sender === 'agent'">
                  <div class="flex items-center">
                    <div class="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                    {{ agentName }}
                  </div>
                </div>
                <div class="font-semibold mb-1" v-if="message.sender === 'user'">Tú</div>
                <div class="whitespace-pre-wrap">{{ message.content }}</div>
                <div class="text-xs opacity-75 mt-1 text-right">{{ formatTime(message.timestamp) }}</div>
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
              placeholder="Escribe tu mensaje aquí..." 
              class="flex-1 border rounded-l-lg p-3 focus:outline-none focus:ring-2 focus:ring-purple-500"
              :disabled="loading"
            >
            <button 
              @click="sendMessage" 
              class="bg-purple-600 text-white px-6 py-3 rounded-r-lg hover:bg-purple-700 disabled:opacity-50 transition duration-200 flex items-center"
              :disabled="loading || !newMessage.trim()"
            >
              <span v-if="!loading">Enviar</span>
              <span v-else class="flex items-center">
                <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Enviando...
              </span>
            </button>
          </div>
          <div class="mt-2 text-xs text-gray-500">
            Este es un entorno de pruebas. Las conversaciones aquí no se guardan en la base de datos.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, nextTick } from 'vue'

export default {
  name: 'Sandbox',
  setup() {
    const chatContainer = ref(null)
    const newMessage = ref('')
    const loading = ref(false)
    const messages = ref([])
    const lastContext = ref(null)
    
    // Configuración del agente
    const agentName = ref('Asistente SCAIE')
    const agentPersonality = ref('amigable, empático, conversacional, natural')
    
    // Función para formatear la hora
    const formatTime = (timestamp) => {
      return new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
    
    // Función para desplazar el chat hacia abajo
    const scrollToBottom = () => {
      nextTick(() => {
        if (chatContainer.value) {
          chatContainer.value.scrollTop = chatContainer.value.scrollHeight
        }
      })
    }
    
    // Función para enviar un mensaje
    const sendMessage = async () => {
      if (!newMessage.value.trim() || loading.value) return
      
      const message = {
        sender: 'user',
        content: newMessage.value,
        timestamp: new Date()
      }
      
      messages.value.push(message)
      const userMessage = newMessage.value
      newMessage.value = ''
      loading.value = true
      scrollToBottom()
      
      try {
        // Enviar mensaje al sandbox endpoint
        const response = await fetch('/api/chat/sandbox', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            message: userMessage
          })
        })
        
        if (response.ok) {
          const data = await response.json()
          messages.value.push({
            sender: 'agent',
            content: data.response,
            timestamp: new Date()
          })
          lastContext.value = data.context_info
        } else {
          messages.value.push({
            sender: 'agent',
            content: 'Lo siento, ha ocurrido un error. Por favor intenta de nuevo.',
            timestamp: new Date()
          })
        }
      } catch (error) {
        messages.value.push({
          sender: 'agent',
          content: 'Lo siento, ha ocurrido un error de conexión. Por favor intenta de nuevo.',
          timestamp: new Date()
        })
      } finally {
        loading.value = false
        scrollToBottom()
      }
    }
    
    // Función para reiniciar el contexto
    const resetContext = async () => {
      try {
        const response = await fetch('/api/chat/sandbox', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            message: 'Hola',
            reset_context: true
          })
        })
        
        if (response.ok) {
          const data = await response.json()
          messages.value = [{
            sender: 'agent',
            content: data.response,
            timestamp: new Date()
          }]
          lastContext.value = data.context_info
        }
      } catch (error) {
        console.error('Error al reiniciar contexto:', error)
      }
    }
    
    // Mensaje de bienvenida
    onMounted(() => {
      messages.value.push({
        sender: 'agent',
        content: '¡Hola! Soy el asistente de pruebas de SCAIE. ¿En qué puedo ayudarte hoy?',
        timestamp: new Date()
      })
      scrollToBottom()
    })
    
    return {
      chatContainer,
      newMessage,
      loading,
      messages,
      lastContext,
      agentName,
      agentPersonality,
      formatTime,
      sendMessage,
      resetContext
    }
  }
}
</script>