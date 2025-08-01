<template>
  <div class="chat">
    <h1 class="text-2xl font-bold mb-4">Chat con Agente AI</h1>
    <div class="bg-white rounded-lg shadow p-6">
      <div class="mb-4">
        <p class="font-semibold">Conversación en tiempo real con el agente de IA</p>
        <p class="text-sm text-gray-600 mt-2">Interactúa con el agente AI para ventas automatizadas</p>
      </div>
      <div ref="chatContainer" class="border rounded-lg p-4 h-96 overflow-y-auto bg-gray-50 mb-4">
        <div v-if="messages.length === 0" class="text-center text-gray-500 py-8">
          <p>¡Bienvenido! Comienza a chatear con el agente AI.</p>
        </div>
        <div v-for="(message, index) in messages" :key="index" class="mb-3">
          <div :class="[
            'p-3 rounded-lg max-w-xs md:max-w-md lg:max-w-lg',
            message.sender === 'user' ? 'bg-blue-500 text-white ml-auto' : 'bg-gray-200 text-gray-800'
          ]">
            <div class="font-semibold mb-1" v-if="message.sender === 'agent'">Agente AI</div>
            <div class="font-semibold mb-1" v-if="message.sender === 'user'">Tú</div>
            {{ message.content }}
            <div class="text-xs opacity-75 mt-1">{{ formatTime(message.timestamp) }}</div>
          </div>
        </div>
      </div>
      <div class="flex">
        <input 
          v-model="newMessage"
          @keyup.enter="sendMessage"
          type="text" 
          placeholder="Escribe tu mensaje aquí..." 
          class="flex-1 border rounded-l-lg p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          :disabled="loading"
        >
        <button 
          @click="sendMessage" 
          class="bg-blue-600 text-white px-4 py-2 rounded-r-lg hover:bg-blue-700 disabled:opacity-50"
          :disabled="loading || !newMessage.trim()"
        >
          {{ loading ? 'Enviando...' : 'Enviar' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, nextTick } from 'vue'

export default {
  name: 'Chat',
  setup() {
    const chatContainer = ref(null)
    const newMessage = ref('')
    const loading = ref(false)
    const messages = ref([])

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
        // Simular llamada a API
        const response = await fetch('/api/chat/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            messages: [{ role: 'user', content: userMessage }]
          })
        })

        if (response.ok) {
          const data = await response.json()
          messages.value.push({
            sender: 'agent',
            content: data.response,
            timestamp: new Date()
          })
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

    // Mensaje de bienvenida
    onMounted(() => {
      messages.value.push({
        sender: 'agent',
        content: '¡Hola! Soy el asistente virtual de SCAIE. ¿En qué puedo ayudarte hoy?',
        timestamp: new Date()
      })
      scrollToBottom()
    })

    return {
      chatContainer,
      newMessage,
      loading,
      messages,
      formatTime,
      sendMessage
    }
  }
}
</script>