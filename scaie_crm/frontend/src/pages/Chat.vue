<template>
  <div class="chat-test flex flex-col h-full">
    <div class="bg-gradient-to-r from-primary-600 to-indigo-600 text-white p-6 rounded-2xl shadow-soft mb-6">
      <h1 class="text-2xl font-bold">Chat de Pruebas del Agente</h1>
      <p class="text-primary-100">Prueba las capacidades del agente de ventas automatizadas</p>
    </div>
    
    <div class="flex-1 flex flex-col md:flex-row gap-6">
      <!-- Panel lateral con información del agente -->
      <div class="w-full md:w-80">
        <div class="card mb-6">
          <div class="p-5">
            <h2 class="font-bold text-lg mb-3">Agente SCAI</h2>
            <div class="flex items-center mb-4">
              <div class="w-3 h-3 bg-success-500 rounded-full mr-2"></div>
              <span class="text-sm">En línea</span>
            </div>
            <p class="text-sm text-gray-600 mb-4">
              Asistente virtual especializado en ventas automatizadas de scaie.com.mx
            </p>
            <button @click="resetConversation" class="w-full btn btn-outline text-sm">
              Reiniciar Conversación
            </button>
          </div>
        </div>
        
        <div class="card">
          <div class="p-5">
            <h3 class="font-semibold mb-3">Información del Cliente</h3>
            <div class="space-y-3">
              <div>
                <label class="block text-xs text-gray-500 mb-1">Nombre</label>
                <input 
                  v-model="customerInfo.name" 
                  type="text" 
                  class="input w-full text-sm"
                  placeholder="Nombre del cliente"
                >
              </div>
              <div>
                <label class="block text-xs text-gray-500 mb-1">Empresa</label>
                <input 
                  v-model="customerInfo.company" 
                  type="text" 
                  class="input w-full text-sm"
                  placeholder="Empresa del cliente"
                >
              </div>
              <div>
                <label class="block text-xs text-gray-500 mb-1">Correo</label>
                <input 
                  v-model="customerInfo.email" 
                  type="email" 
                  class="input w-full text-sm"
                  placeholder="Email del cliente"
                >
              </div>
              <div>
                <label class="block text-xs text-gray-500 mb-1">Teléfono</label>
                <input 
                  v-model="customerInfo.phone" 
                  type="text" 
                  class="input w-full text-sm"
                  placeholder="Teléfono del cliente"
                >
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Área de chat -->
      <div class="flex-1 flex flex-col">
        <div class="card flex-1 flex flex-col mb-6">
          <div class="p-4 border-b border-gray-200">
            <h3 class="font-semibold">Conversación</h3>
          </div>
          
          <!-- Mensajes -->
          <div ref="chatContainer" class="flex-1 overflow-y-auto p-4 bg-gray-50">
            <div 
              v-for="message in messages" 
              :key="message.id"
              class="mb-4"
              :class="message.sender === 'user' ? 'text-right' : 'text-left'"
            >
              <div 
                class="inline-block max-w-xs md:max-w-md lg:max-w-lg px-4 py-2 rounded-2xl"
                :class="message.sender === 'user' ? 
                  'bg-primary-500 text-white rounded-tr-none' : 
                  'bg-white border border-gray-200 rounded-tl-none shadow-soft'"
              >
                <div class="flex items-center mb-1" v-if="message.sender === 'ai'">
                  <div class="w-6 h-6 rounded-full bg-primary-100 flex items-center justify-center text-primary-800 mr-2">
                    <span class="text-xs font-bold">A</span>
                  </div>
                  <span class="text-xs font-medium text-gray-700">Agente SCAI</span>
                </div>
                <div class="text-sm whitespace-pre-wrap">{{ message.text }}</div>
                <div class="text-xs mt-1" :class="message.sender === 'user' ? 'text-primary-100' : 'text-gray-500'">
                  {{ formatTime(message.timestamp) }}
                </div>
              </div>
            </div>
            
            <div v-if="isTyping" class="mb-4 text-left">
              <div class="inline-block px-4 py-2 rounded-2xl bg-white border border-gray-200 rounded-tl-none shadow-soft">
                <div class="flex items-center">
                  <div class="w-6 h-6 rounded-full bg-primary-100 flex items-center justify-center text-primary-800 mr-2">
                    <span class="text-xs font-bold">A</span>
                  </div>
                  <span class="text-xs font-medium text-gray-700">Agente SCAI</span>
                </div>
                <div class="flex space-x-1 mt-2">
                  <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                  <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.4s"></div>
                </div>
              </div>
            </div>
            
            <div v-if="errorMessage" class="mb-4 text-left">
              <div class="inline-block px-4 py-2 rounded-2xl bg-danger-100 border border-danger-200 rounded-tl-none">
                <div class="flex items-center">
                  <div class="w-6 h-6 rounded-full bg-danger-200 flex items-center justify-center text-danger-800 mr-2">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                  </div>
                  <span class="text-xs font-medium text-danger-700">Error</span>
                </div>
                <div class="text-sm text-danger-700 whitespace-pre-wrap">{{ errorMessage }}</div>
              </div>
            </div>
          </div>
          
          <!-- Área de entrada -->
          <div class="p-4 border-t border-gray-200">
            <div class="flex">
              <input
                v-model="newMessage"
                @keyup.enter="sendMessage"
                type="text"
                placeholder="Escribe tu mensaje..."
                class="input flex-1 mr-2"
                :disabled="isTyping"
              >
              <button
                @click="sendMessage"
                class="btn btn-primary"
                :disabled="!newMessage.trim() || isTyping"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
                </svg>
              </button>
            </div>
            <p class="text-xs text-gray-500 mt-2">
              Presiona Enter para enviar
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, nextTick } from 'vue';
import { chatService } from '../services/api';

export default {
  name: 'Chat',
  setup() {
    const newMessage = ref('');
    const messages = ref([]);
    const isTyping = ref(false);
    const chatContainer = ref(null);
    const errorMessage = ref('');
    
    const customerInfo = ref({
      name: '',
      company: '',
      email: '',
      phone: ''
    });
    
    const scrollToBottom = () => {
      nextTick(() => {
        if (chatContainer.value) {
          chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
        }
      });
    };
    
    const formatTime = (timestamp) => {
      return new Date(timestamp).toLocaleTimeString('es-ES', {
        hour: '2-digit',
        minute: '2-digit'
      });
    };
    
    const addMessage = (text, sender) => {
      const message = {
        id: Date.now(),
        text: text,
        sender: sender,
        timestamp: new Date()
      };
      messages.value.push(message);
      scrollToBottom();
    };
    
    const sendMessage = async () => {
      const message = newMessage.value.trim();
      if (!message || isTyping.value) return;
      
      // Clear error message
      errorMessage.value = '';
      
      // Add user message
      addMessage(message, 'user');
      newMessage.value = '';
      isTyping.value = true;
      
      try {
        // Send message to backend
        const response = await chatService.sendMessage(message, customerInfo.value);
        
        // Add AI response
        isTyping.value = false;
        if (response && response.response) {
          addMessage(response.response, 'ai');
        } else {
          errorMessage.value = 'No se recibió una respuesta válida del servidor.';
        }
      } catch (error) {
        isTyping.value = false;
        console.error('Error sending message:', error);
        errorMessage.value = `Error al enviar el mensaje: ${error.message || 'Error desconocido'}`;
        addMessage('Lo siento, estoy teniendo problemas para responder en este momento. Por favor, inténtalo de nuevo.', 'ai');
      }
    };
    
    const resetConversation = () => {
      messages.value = [];
      errorMessage.value = '';
      addMessage('¡Hola! Soy tu asistente virtual de SCAIE. ¿En qué puedo ayudarte hoy?', 'ai');
    };
    
    onMounted(() => {
      // Add welcome message
      addMessage('¡Hola! Soy tu asistente virtual de SCAIE. ¿En qué puedo ayudarte hoy?', 'ai');
    });
    
    return {
      newMessage,
      messages,
      isTyping,
      chatContainer,
      customerInfo,
      errorMessage,
      sendMessage,
      resetConversation,
      formatTime
    };
  }
};
</script>

<style scoped>
/* Animaciones personalizadas */
@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}

.animate-bounce {
  animation: bounce 1s infinite;
}
</style>