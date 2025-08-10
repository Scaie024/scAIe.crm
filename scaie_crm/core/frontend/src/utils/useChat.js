import { ref, reactive } from 'vue'
import { chatService } from '../services/api.js'

export function useChat() {
  const messages = ref([])
  const loading = ref(false)
  const sending = ref(false)
  const error = ref('')
  
  const addMessage = (message) => {
    messages.value.push({
      ...message,
      created_at: message.created_at || new Date().toISOString()
    })
  }
  
  const clearMessages = () => {
    messages.value = []
  }
  
  const sendMessage = async (messageText, contactInfo = { phone: '+525512345678' }) => {
    if (!messageText.trim() || loading.value || sending.value) return
    
    // Add user message to chat
    addMessage({
      sender: 'user',
      content: messageText
    })
    
    sending.value = true
    error.value = ''
    
    try {
      // Send message to backend using shared API service with contact_info
      const data = await chatService.sendMessage(messageText, contactInfo)
      
      // Add agent response to chat
      addMessage({
        sender: 'agent',
        content: data.response
      })
      
  return data
    } catch (err) {
      error.value = err.message || 'Error al enviar el mensaje'
      
      // Show error message in chat
      addMessage({
        sender: 'agent',
        content: 'Lo siento, ocurrió un error al procesar tu mensaje. Por favor, inténtalo de nuevo.'
      })
      
      throw err
    } finally {
      sending.value = false
    }
  }
  
  const initializeChat = (welcomeMessage = null) => {
    clearMessages()
    
    if (welcomeMessage) {
      addMessage({
        sender: 'agent',
        content: welcomeMessage
      })
    } else {
      addMessage({
        sender: 'agent',
        content: '¡Hola! Soy SCAI. Te ayudo a automatizar procesos con IA sin programación. ¿Qué necesitas?'
      })
    }
  }
  
  return {
    // State
    messages,
    loading,
    sending,
    error,
    
    // Methods
    addMessage,
    clearMessages,
    sendMessage,
    initializeChat
  }
}