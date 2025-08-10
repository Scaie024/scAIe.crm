<template>
  <div class="bg-gradient-to-br from-purple-500 to-indigo-600 rounded-lg p-5 text-white">
    <div class="flex items-center mb-3">
      <div class="bg-white text-purple-600 rounded-full w-10 h-10 flex items-center justify-center font-bold mr-3">
        {{ config.name.charAt(0) }}
      </div>
      <div>
        <h3 class="font-bold">{{ config.name }}</h3>
        <p class="text-purple-200 text-sm">Agente de ventas</p>
      </div>
    </div>
    
    <div class="mt-4">
      <p class="text-sm mb-2">Personalidad:</p>
      <p class="text-sm bg-purple-400 bg-opacity-30 rounded p-2">{{ config.personality }}</p>
    </div>
    
    <div class="mt-3">
      <p class="text-sm mb-2">Tono:</p>
      <p class="text-sm bg-purple-400 bg-opacity-30 rounded p-2">{{ config.tone }}</p>
    </div>
    
    <div class="mt-3">
      <p class="text-sm mb-2">Objetivo:</p>
      <p class="text-sm bg-purple-400 bg-opacity-30 rounded p-2">{{ config.goal }}</p>
    </div>
    
    <div class="mt-4 pt-3 border-t border-purple-400 border-opacity-30">
      <h4 class="font-bold text-sm mb-2">Parámetros del Modelo</h4>
      <div class="grid grid-cols-2 gap-2 text-xs">
        <div class="flex justify-between">
          <span>Temperatura:</span>
          <span class="font-medium">{{ config.temperature }}</span>
        </div>
        <div class="flex justify-between">
          <span>Tokens Máx.:</span>
          <span class="font-medium">{{ config.maxTokens }}</span>
        </div>
        <div class="flex justify-between">
          <span>Top-P:</span>
          <span class="font-medium">{{ config.topP }}</span>
        </div>
        <div class="flex justify-between">
          <span>Top-K:</span>
          <span class="font-medium">{{ config.topK }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AgentPreview',
  props: {
    config: {
      type: Object,
      required: true
    }
  }
}
</script>