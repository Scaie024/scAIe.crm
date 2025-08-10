<template>
  <div class="flex-1 flex flex-col h-full">
    <div ref="chatContainer" class="flex-1 overflow-y-auto p-4 bg-white">
      <div v-if="messages.length === 0" class="flex flex-col items-center justify-center h-full text-gray-500">
        <div class="bg-gray-200 border-2 border-dashed rounded-xl w-16 h-16 mb-4"></div>
        <p class="text-lg mb-2">¡Bienvenido al chat con SCAI!</p>
        <p class="text-center">Empieza una conversación para explorar las capacidades de nuestro agente de ventas automatizadas.</p>
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
  </div>
</template>

<script>
import { ref, onMounted, nextTick } from 'vue'

export default {
  name: 'ChatWindow',
  props: {
    messages: {
      type: Array,
      default: () => []
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  setup(props, { emit }) {
    const chatContainer = ref(null)
    
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
    
    // Watch for new messages and scroll to bottom
    watch(() => props.messages, () => {
      scrollToBottom()
    }, { deep: true })
    
    // Scroll to bottom when loading changes
    watch(() => props.loading, () => {
      scrollToBottom()
    })
    
    // Initialize scroll position
    onMounted(() => {
      scrollToBottom()
    })
    
    return {
      chatContainer,
      formatTime,
      scrollToBottom
    }
  }
}
</script>

<style scoped>
.overflow-y-auto {
  scroll-behavior: smooth;
}
</style>