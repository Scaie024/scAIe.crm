<template>
  <div id="app" class="flex flex-col min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow-soft">
      <div class="container mx-auto px-4">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center space-x-2">
            <div class="w-8 h-8 rounded-lg bg-primary-600 flex items-center justify-center">
              <span class="text-white font-bold text-sm">S</span>
            </div>
            <h1 class="text-xl font-bold text-gray-900">SCAIE CRM</h1>
          </div>
          <nav class="hidden md:flex space-x-1">
            <router-link 
              to="/" 
              class="px-3 py-2 rounded-lg text-sm font-medium transition-colors duration-200"
              active-class="bg-primary-50 text-primary-700"
              exact-active-class="bg-primary-50 text-primary-700"
            >
              Dashboard
            </router-link>
            <router-link 
              to="/admin" 
              class="px-3 py-2 rounded-lg text-sm font-medium transition-colors duration-200"
              active-class="bg-primary-50 text-primary-700"
              exact-active-class="bg-primary-50 text-primary-700"
            >
              Administración
            </router-link>
            <router-link 
              to="/contacts" 
              class="px-3 py-2 rounded-lg text-sm font-medium transition-colors duration-200"
              active-class="bg-primary-50 text-primary-700"
              exact-active-class="bg-primary-50 text-primary-700"
            >
              Contactos
            </router-link>
            <router-link 
              to="/sandbox" 
              class="px-3 py-2 rounded-lg text-sm font-medium transition-colors duration-200"
              active-class="bg-primary-50 text-primary-700"
              exact-active-class="bg-primary-50 text-primary-700"
            >
              Sandbox
            </router-link>
            <router-link 
              to="/chat" 
              class="px-3 py-2 rounded-lg text-sm font-medium transition-colors duration-200"
              active-class="bg-primary-50 text-primary-700"
              exact-active-class="bg-primary-50 text-primary-700"
            >
              Chat
            </router-link>
            <router-link 
              to="/agent" 
              class="px-3 py-2 rounded-lg text-sm font-medium transition-colors duration-200"
              active-class="bg-primary-50 text-primary-700"
              exact-active-class="bg-primary-50 text-primary-700"
            >
              Agente
            </router-link>
          </nav>
          <div class="md:hidden">
            <button @click="toggleMobileMenu" class="text-gray-500 hover:text-gray-700 focus:outline-none focus:ring-2 focus:ring-primary-500 rounded-lg p-1">
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path v-if="!mobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      </div>
      
      <!-- Mobile menu -->
      <div v-if="mobileMenuOpen" class="md:hidden border-t border-gray-200">
        <div class="px-2 pt-2 pb-3 space-y-1">
          <router-link 
            to="/" 
            class="block px-3 py-2 rounded-md text-base font-medium transition-colors duration-200"
            active-class="bg-primary-50 text-primary-700"
            exact-active-class="bg-primary-50 text-primary-700"
            @click="mobileMenuOpen = false"
          >
            Dashboard
          </router-link>
          <router-link 
            to="/admin" 
            class="block px-3 py-2 rounded-md text-base font-medium transition-colors duration-200"
            active-class="bg-primary-50 text-primary-700"
            exact-active-class="bg-primary-50 text-primary-700"
            @click="mobileMenuOpen = false"
          >
            Administración
          </router-link>
          <router-link 
            to="/contacts" 
            class="block px-3 py-2 rounded-md text-base font-medium transition-colors duration-200"
            active-class="bg-primary-50 text-primary-700"
            exact-active-class="bg-primary-50 text-primary-700"
            @click="mobileMenuOpen = false"
          >
            Contactos
          </router-link>
          <router-link 
            to="/sandbox" 
            class="block px-3 py-2 rounded-md text-base font-medium transition-colors duration-200"
            active-class="bg-primary-50 text-primary-700"
            exact-active-class="bg-primary-50 text-primary-700"
            @click="mobileMenuOpen = false"
          >
            Sandbox
          </router-link>
          <router-link 
            to="/chat" 
            class="block px-3 py-2 rounded-md text-base font-medium transition-colors duration-200"
            active-class="bg-primary-50 text-primary-700"
            exact-active-class="bg-primary-50 text-primary-700"
            @click="mobileMenuOpen = false"
          >
            Chat
          </router-link>
          <router-link 
            to="/agent" 
            class="block px-3 py-2 rounded-md text-base font-medium transition-colors duration-200"
            active-class="bg-primary-50 text-primary-700"
            exact-active-class="bg-primary-50 text-primary-700"
            @click="mobileMenuOpen = false"
          >
            Agente
          </router-link>
        </div>
      </div>
    </header>
    
    <!-- Main content -->
    <main class="flex-1 container mx-auto px-4 py-6">
      <router-view></router-view>
    </main>
    
    <!-- Footer -->
    <footer class="bg-white border-t border-gray-200">
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
  font-family: 'Inter', ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: left;
  color: #1f2937;
  min-height: 100vh;
}
</style>