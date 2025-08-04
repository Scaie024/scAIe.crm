<template>
  <div id="app" class="flex flex-col min-h-screen bg-gray-100">
    <!-- Header -->
    <header class="bg-white shadow">
      <div class="container mx-auto px-4 py-4">
        <div class="flex justify-between items-center">
          <div class="flex items-center">
            <h1 class="text-xl font-bold text-gray-800">SCAIE - Sistema Agente</h1>
          </div>
          <nav class="hidden md:flex space-x-4">
            <router-link to="/" class="px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-100">Dashboard</router-link>
            <router-link to="/database" class="px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-100">Base de Datos</router-link>
            <router-link to="/chat" class="px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-100">Chat de Pruebas</router-link>
          </nav>
          <div class="md:hidden">
            <button @click="toggleMobileMenu" class="text-gray-500 hover:text-gray-700 focus:outline-none">
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path v-if="!mobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      </div>
      
      <!-- Mobile menu -->
      <div v-if="mobileMenuOpen" class="md:hidden">
        <div class="px-2 pt-2 pb-3 space-y-1 sm:px-3">
          <router-link to="/" class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-100" @click="mobileMenuOpen = false">Dashboard</router-link>
          <router-link to="/database" class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-100" @click="mobileMenuOpen = false">Base de Datos</router-link>
          <router-link to="/chat" class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-100" @click="mobileMenuOpen = false">Chat de Pruebas</router-link>
        </div>
      </div>
    </header>
    
    <!-- Main content -->
    <main class="flex-1 container mx-auto px-4 py-6">
      <router-view></router-view>
    </main>
    
    <!-- Footer -->
    <footer class="bg-white border-t">
      <div class="container mx-auto px-4 py-6">
        <p class="text-center text-gray-500 text-sm">
          SCAIE - Sistema Agente Conversacional Inteligente Empresarial
        </p>
      </div>
    </footer>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'App',
  setup() {
    const mobileMenuOpen = ref(false)
    
    const toggleMobileMenu = () => {
      mobileMenuOpen.value = !mobileMenuOpen.value
    }
    
    return {
      mobileMenuOpen,
      toggleMobileMenu
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  min-height: 100vh;
}
</style>