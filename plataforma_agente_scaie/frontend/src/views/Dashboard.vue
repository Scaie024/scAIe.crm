<template>
  <div class="dashboard">
    <HelloWorld msg="¡Bienvenido al Panel de Control de SCAIE!" />
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div class="bg-white rounded-lg shadow p-6">
        <h2 class="text-lg font-semibold mb-2">Estadísticas</h2>
        <p>Bienvenido al panel de control de SCAIE - Sistema Agente</p>
      </div>
      <div class="bg-white rounded-lg shadow p-6">
        <h2 class="text-lg font-semibold mb-2">Contactos</h2>
        <p>Gestión de contactos y clientes potenciales</p>
      </div>
      <div class="bg-white rounded-lg shadow p-6">
        <h2 class="text-lg font-semibold mb-2">Conversaciones</h2>
        <p>Seguimiento de conversaciones con clientes</p>
      </div>
    </div>
  </div>
</template>

<script>
import HelloWorld from '../components/HelloWorld.vue'

export default {
  name: 'Dashboard',
  components: {
    HelloWorld
  }
}
</script>