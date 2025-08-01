<template>
  <div class="agent">
    <h1 class="text-2xl font-bold mb-4">Configuración del Agente AI</h1>
    <div class="bg-white rounded-lg shadow p-6">
      <p class="font-semibold">Configuración y personalización del agente de IA</p>
      <p class="mt-4">Aquí podrás configurar el comportamiento y las respuestas del agente AI.</p>
      <div class="mt-6">
        <h2 class="text-lg font-semibold mb-2">Parámetros del Agente</h2>
        <ul class="list-disc pl-5 space-y-1">
          <li>Personalidad del agente</li>
          <li>Tono de las respuestas</li>
          <li>Información de la empresa</li>
          <li>Productos y servicios</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Agent'
}
</script>