<template>
  <div class="flex flex-col items-center justify-center" :class="containerClass">
    <div class="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2" :class="spinnerClass"></div>
    <p v-if="message" class="mt-2 text-gray-600">{{ message }}</p>
  </div>
</template>

<script>
export default {
  name: 'LoadingSpinner',
  props: {
    message: {
      type: String,
      default: ''
    },
    size: {
      type: String,
      default: 'md', // sm, md, lg
      validator: (value) => ['sm', 'md', 'lg'].includes(value)
    },
    color: {
      type: String,
      default: 'blue', // blue, green, purple, red, gray
      validator: (value) => ['blue', 'green', 'purple', 'red', 'gray'].includes(value)
    }
  },
  computed: {
    spinnerClass() {
      const sizes = {
        sm: 'h-4 w-4 border-t-1 border-b-1',
        md: 'h-8 w-8 border-t-2 border-b-2',
        lg: 'h-12 w-12 border-t-3 border-b-3'
      }
      
      const colors = {
        blue: 'border-blue-600',
        green: 'border-green-600',
        purple: 'border-purple-600',
        red: 'border-red-600',
        gray: 'border-gray-600'
      }
      
      return [sizes[this.size], colors[this.color]]
    },
    containerClass() {
      return this.size === 'lg' ? 'p-8' : this.size === 'sm' ? 'p-2' : 'p-4'
    }
  }
}
</script>