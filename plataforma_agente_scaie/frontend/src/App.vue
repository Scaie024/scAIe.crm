<template>
  <div id="app">
    <nav class="bg-blue-600 text-white p-4 shadow-lg">
      <div class="container mx-auto flex justify-between items-center">
        <h1 class="text-xl font-bold">SCAIE - Sistema Agente</h1>
        <div class="space-x-4">
          <router-link to="/" class="hover:underline">Dashboard</router-link>
          <router-link to="/contacts" class="hover:underline">Contactos</router-link>
          <router-link to="/chat" class="hover:underline">Chat</router-link>
          <router-link to="/agent" class="hover:underline">Agente</router-link>
        </div>
      </div>
    </nav>
    <main class="container mx-auto p-4">
      <router-view></router-view>
    </main>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  min-height: 100vh;
}
</style>