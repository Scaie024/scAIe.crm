<template>
  <div class="bg-white rounded-lg shadow p-6 hover:shadow-md transition-shadow duration-200">
    <div class="flex items-center">
      <div 
        class="p-3 rounded-full mr-4"
        :class="bgColor"
      >
        <slot name="icon"></slot>
      </div>
      <div>
        <p class="text-gray-500 text-sm">{{ title }}</p>
        <p class="text-2xl font-bold">{{ value }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'StatsCard',
  props: {
    title: {
      type: String,
      required: true
    },
    value: {
      type: [String, Number],
      required: true
    },
    color: {
      type: String,
      default: 'blue'
    }
  },
  setup(props) {
    const bgColor = computed(() => {
      const colors = {
        blue: 'bg-blue-100 text-blue-600',
        green: 'bg-green-100 text-green-600',
        purple: 'bg-purple-100 text-purple-600',
        yellow: 'bg-yellow-100 text-yellow-600',
        red: 'bg-red-100 text-red-600'
      }
      return colors[props.color] || colors.blue
    })

    return {
      bgColor
    }
  }
}
</script>