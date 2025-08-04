<template>
  <div class="space-y-6">
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">Nombre del Agente</label>
      <input 
        v-model="config.name" 
        type="text" 
        class="w-full border rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-purple-500"
        placeholder="Nombre del agente"
      >
      <p class="mt-1 text-sm text-gray-500">El nombre que usará el agente en las conversaciones</p>
    </div>
    
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">Personalidad</label>
      <textarea 
        v-model="config.personality" 
        rows="3"
        class="w-full border rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-purple-500"
        placeholder="Describe la personalidad del agente"
      ></textarea>
      <p class="mt-1 text-sm text-gray-500">Define cómo se comportará el agente (ej. amigable, profesional, empático)</p>
    </div>
    
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">Tono de las respuestas</label>
      <textarea 
        v-model="config.tone" 
        rows="2"
        class="w-full border rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-purple-500"
        placeholder="Define el tono del agente"
      ></textarea>
      <p class="mt-1 text-sm text-gray-500">Estilo de comunicación (ej. conversacional y cercano)</p>
    </div>
    
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">Objetivo principal</label>
      <textarea 
        v-model="config.goal" 
        rows="2"
        class="w-full border rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-purple-500"
        placeholder="Define el objetivo del agente"
      ></textarea>
      <p class="mt-1 text-sm text-gray-500">Qué debe intentar lograr el agente en cada conversación</p>
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Temperatura</label>
        <input 
          v-model="config.temperature" 
          type="range" 
          min="0" 
          max="1" 
          step="0.1"
          class="w-full"
        >
        <div class="flex justify-between text-sm text-gray-500">
          <span>Preciso</span>
          <span>{{ config.temperature }}</span>
          <span>Creativo</span>
        </div>
        <p class="mt-1 text-sm text-gray-500">Controla la creatividad de las respuestas</p>
      </div>
      
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Tokens Máximos</label>
        <input 
          v-model="config.maxTokens" 
          type="range" 
          min="100" 
          max="2000" 
          step="100"
          class="w-full"
        >
        <div class="flex justify-between text-sm text-gray-500">
          <span>100</span>
          <span>{{ config.maxTokens }}</span>
          <span>2000</span>
        </div>
        <p class="mt-1 text-sm text-gray-500">Longitud máxima de las respuestas</p>
      </div>
      
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Top-P</label>
        <input 
          v-model="config.topP" 
          type="range" 
          min="0" 
          max="1" 
          step="0.1"
          class="w-full"
        >
        <div class="flex justify-between text-sm text-gray-500">
          <span>0</span>
          <span>{{ config.topP }}</span>
          <span>1</span>
        </div>
        <p class="mt-1 text-sm text-gray-500">Controla la diversidad de las respuestas</p>
      </div>
      
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Top-K</label>
        <input 
          v-model="config.topK" 
          type="range" 
          min="1" 
          max="100" 
          step="1"
          class="w-full"
        >
        <div class="flex justify-between text-sm text-gray-500">
          <span>1</span>
          <span>{{ config.topK }}</span>
          <span>100</span>
        </div>
        <p class="mt-1 text-sm text-gray-500">Controla la selección de palabras</p>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive, watch } from 'vue'

export default {
  name: 'AgentConfig',
  props: {
    modelValue: {
      type: Object,
      default: () => ({
        name: 'SCAI',
        personality: 'amigable, empático, profesional, persuasivo',
        tone: 'coloquial pero respetuoso',
        goal: 'ayudar a los usuarios a entender los beneficios de SCAIE de manera natural',
        temperature: 0.8,
        maxTokens: 1024,
        topP: 0.9,
        topK: 30
      })
    }
  },
  emits: ['update:modelValue'],
  setup(props, { emit }) {
    const config = reactive({ ...props.modelValue })
    
    // Watch for changes and emit update
    watch(config, (newConfig) => {
      emit('update:modelValue', { ...newConfig })
    }, { deep: true })
    
    // Watch for external changes
    watch(() => props.modelValue, (newVal) => {
      Object.assign(config, newVal)
    }, { deep: true })
    
    return {
      config
    }
  }
}
</script>

<style scoped>
input[type="range"] {
  height: 5px;
  background: #d1d5db;
  border-radius: 5px;
  outline: none;
}

input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 18px;
  height: 18px;
  background: #7e22ce;
  border-radius: 50%;
  cursor: pointer;
}

input[type="range"]::-moz-range-thumb {
  width: 18px;
  height: 18px;
  background: #7e22ce;
  border-radius: 50%;
  cursor: pointer;
  border: none;
}
</style>