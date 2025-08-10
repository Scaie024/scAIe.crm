import { ref, reactive } from 'vue'

export function useAgent() {
  const config = reactive({
    name: 'SCAI',
    personality: 'amigable, empático, profesional, persuasivo',
    tone: 'coloquial pero respetuoso',
    goal: 'ayudar a los usuarios a entender los beneficios de SCAIE de manera natural',
    temperature: 0.8,
    maxTokens: 1024,
    topP: 0.9,
    topK: 30
  })
  
  const saving = ref(false)
  const testing = ref(false)
  const testResponse = ref('')
  const error = ref('')
  
  const loadConfig = () => {
    const savedConfig = localStorage.getItem('agentConfig')
    if (savedConfig) {
      try {
        const parsed = JSON.parse(savedConfig)
        Object.assign(config, parsed)
        return true
      } catch (e) {
        console.error('Error loading agent config:', e)
        error.value = 'Error al cargar la configuración'
        return false
      }
    }
    return true
  }
  
  const saveConfig = async () => {
    saving.value = true
    error.value = ''
    
    try {
      // Save to localStorage
      localStorage.setItem('agentConfig', JSON.stringify(config))
      
      // In a real implementation, you would also save to the backend
      // For now, we'll just simulate this
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      return true
    } catch (err) {
      error.value = err.message || 'Error al guardar la configuración'
      console.error('Error saving config:', err)
      return false
    } finally {
      saving.value = false
    }
  }
  
  const resetConfig = () => {
    config.name = 'SCAI'
    config.personality = 'amigable, empático, profesional, persuasivo'
    config.tone = 'coloquial pero respetuoso'
    config.goal = 'ayudar a los usuarios a entender los beneficios de SCAIE de manera natural'
    config.temperature = 0.8
    config.maxTokens = 1024
    config.topP = 0.9
    config.topK = 30
    
    return true
  }
  
  const testAgent = async () => {
    testResponse.value = ''
    testing.value = true
    error.value = ''
    
    try {
      // Simulate agent response
      await new Promise(resolve => setTimeout(resolve, 1500))
      testResponse.value = `¡Hola! Soy ${config.name}, tu asistente virtual. Estoy configurado para ser ${config.personality} y mi objetivo es ${config.goal}. ¿En qué puedo ayudarte hoy?`
      return testResponse.value
    } catch (err) {
      error.value = err.message || 'Error al probar el agente'
      console.error('Error testing agent:', err)
      throw err
    } finally {
      testing.value = false
    }
  }
  
  const updateConfig = (newConfig) => {
    Object.assign(config, newConfig)
  }
  
  // Load config on composable initialization
  loadConfig()
  
  return {
    // State
    config,
    saving,
    testing,
    testResponse,
    error,
    
    // Methods
    loadConfig,
    saveConfig,
    resetConfig,
    testAgent,
    updateConfig
  }
}