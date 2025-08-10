<template>
  <div class="rounded-lg p-4" :class="containerClass">
    <div class="flex">
      <div class="flex-shrink-0">
        <svg class="h-5 w-5" :class="iconClass" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
        </svg>
      </div>
      <div class="ml-3">
        <h3 class="text-sm font-medium" :class="titleClass">
          {{ title }}
        </h3>
        <div v-if="message" class="mt-2 text-sm" :class="messageClass">
          <p>{{ message }}</p>
        </div>
        <div v-if="$slots.default" class="mt-2 text-sm" :class="messageClass">
          <slot></slot>
        </div>
        <div v-if="showRetry" class="mt-4">
          <button 
            @click="$emit('retry')"
            class="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded-full shadow-sm text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
          >
            Reintentar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ErrorMessage',
  props: {
    title: {
      type: String,
      default: 'Error'
    },
    message: {
      type: String,
      default: ''
    },
    showRetry: {
      type: Boolean,
      default: false
    },
    variant: {
      type: String,
      default: 'error', // error, warning
      validator: (value) => ['error', 'warning'].includes(value)
    }
  },
  emits: ['retry'],
  computed: {
    containerClass() {
      return this.variant === 'error' 
        ? 'bg-red-50 border border-red-200' 
        : 'bg-yellow-50 border border-yellow-200'
    },
    iconClass() {
      return this.variant === 'error' 
        ? 'text-red-400' 
        : 'text-yellow-400'
    },
    titleClass() {
      return this.variant === 'error' 
        ? 'text-red-800' 
        : 'text-yellow-800'
    },
    messageClass() {
      return this.variant === 'error' 
        ? 'text-red-700' 
        : 'text-yellow-700'
    }
  }
}
</script>