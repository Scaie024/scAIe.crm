<template>
  <div class="agent">
    <div class="bg-gradient-to-r from-purple-600 to-indigo-700 text-white p-4 rounded-t-lg mb-6">
      <h1 class="text-2xl font-bold">Configuración del Agente AI</h1>
      <p class="text-purple-100">Personaliza el comportamiento y las respuestas del agente conversacional</p>
    </div>
    
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Panel de configuración -->
      <div class="lg:col-span-2">
        <div class="bg-white rounded-lg shadow p-6 mb-6">
          <h2 class="text-xl font-bold mb-4 text-gray-800">Personalización del Agente</h2>
          
          <AgentConfig v-model="agentConfig" />
          
          <div class="mt-6 flex flex-wrap gap-3">
            <button 
              @click="saveConfig" 
              class="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition duration-200 flex items-center"
              :disabled="saving"
            >
              <svg v-if="saving" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span>{{ saving ? 'Guardando...' : 'Guardar Configuración' }}</span>
            </button>
            <button 
              @click="resetConfig" 
              class="bg-gray-200 text-gray-800 px-4 py-2 rounded-lg hover:bg-gray-300 transition duration-200"
              :disabled="saving"
            >
              Restablecer
            </button>
            <button 
              @click="testAgent" 
              class="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition duration-200 flex items-center"
              :disabled="saving"
            >
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              Probar Agente
            </button>
          </div>
        </div>
      </div>
      
      <!-- Panel de previsualización -->
      <div class="lg:col-span-1">
        <div class="bg-white rounded-lg shadow p-6 sticky top-6">
          <h2 class="text-xl font-bold mb-4 text-gray-800">Previsualización</h2>
          
          <AgentPreview :config="agentConfig" />
          
          <div v-if="testResponse" class="mt-4 bg-blue-50 rounded-lg p-4">
            <h3 class="font-bold text-gray-800 mb-2">Respuesta de prueba:</h3>
            <p class="text-sm text-gray-700">{{ testResponse }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import AgentConfig from '../components/agent/AgentConfig.vue'
import AgentPreview from '../components/agent/AgentPreview.vue'

export default {
  name: 'Agent',
  components: {
    AgentConfig,
    AgentPreview
  },
  setup() {
    const saving = ref(false)
    const testResponse = ref('')
    
    const agentConfig = reactive({
      name: 'SCAI',
      personality: 'amigable, empático, profesional, persuasivo',
      tone: 'coloquial pero respetuoso',
      goal: 'ayudar a los usuarios a entender los beneficios de SCAIE de manera natural',
      temperature: 0.8,
      maxTokens: 1024,
      topP: 0.9,
      topK: 30
    })
    
    // Load configuration from localStorage or use defaults
    const loadConfig = () => {
      const savedConfig = localStorage.getItem('agentConfig')
      if (savedConfig) {
        try {
          const parsed = JSON.parse(savedConfig)
          Object.assign(agentConfig, parsed)
        } catch (e) {
          console.error('Error loading agent config:', e)
        }
      }
    }
    
    // Save configuration to localStorage and backend
    const saveConfig = async () => {
      saving.value = true
      try {
        // Save to localStorage
        localStorage.setItem('agentConfig', JSON.stringify(agentConfig))
        
        // In a real implementation, you would also save to the backend
        // For now, we'll just simulate this
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        alert('Configuración guardada exitosamente')
      } catch (error) {
        console.error('Error saving config:', error)
        alert('Error al guardar la configuración')
      } finally {
        saving.value = false
      }
    }
    
    // Reset configuration to defaults
    const resetConfig = () => {
      if (confirm('¿Estás seguro de que deseas restablecer la configuración?')) {
        agentConfig.name = 'SCAI'
        agentConfig.personality = 'amigable, empático, profesional, persuasivo'
        agentConfig.tone = 'coloquial pero respetuoso'
        agentConfig.goal = 'ayudar a los usuarios a entender los beneficios de SCAIE de manera natural'
        agentConfig.temperature = 0.8
        agentConfig.maxTokens = 1024
        agentConfig.topP = 0.9
        agentConfig.topK = 30
      }
    }
    
    // Test the agent with a sample message
    const testAgent = async () => {
      testResponse.value = ''
      saving.value = true
      
      try {
        // Simulate agent response
        await new Promise(resolve => setTimeout(resolve, 1500))
        testResponse.value = `¡Hola! Soy ${agentConfig.name}, tu asistente virtual. Estoy configurado para ser ${agentConfig.personality} y mi objetivo es ${agentConfig.goal}. ¿En qué puedo ayudarte hoy?`
      } catch (error) {
        console.error('Error testing agent:', error)
        testResponse.value = 'Error al probar el agente. Por favor, inténtalo de nuevo.'
      } finally {
        saving.value = false
      }
    }
    
    // Load config on component mount
    onMounted(() => {
      loadConfig()
    })
    
    return {
      agentConfig,
      saving,
      testResponse,
      saveConfig,
      resetConfig,
      testAgent
    }
  }
}
</script>

<style scoped>
/* Add any additional styles here if needed */
</style>