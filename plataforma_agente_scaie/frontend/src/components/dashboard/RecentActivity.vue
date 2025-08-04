<template>
  <div class="bg-white rounded-lg shadow p-6">
    <h2 class="text-xl font-bold mb-4 text-gray-800">Actividad Reciente</h2>
    
    <div v-if="activities && activities.length > 0" class="space-y-4">
      <div 
        v-for="(activity, index) in activities" 
        :key="index" 
        class="flex items-start border-b pb-4 last:border-0 last:pb-0"
      >
        <div 
          class="rounded-full w-10 h-10 flex items-center justify-center mr-3 flex-shrink-0"
          :class="getActivityBgColor(activity.type)"
        >
          <component 
            :is="getActivityIcon(activity.type)" 
            class="w-5 h-5"
            :class="getActivityIconColor(activity.type)"
          />
        </div>
        <div class="flex-1">
          <p class="font-medium">{{ activity.title }}</p>
          <p class="text-gray-600 text-sm">{{ activity.description }}</p>
          <p class="text-gray-400 text-xs">{{ activity.time }}</p>
        </div>
      </div>
    </div>
    
    <div v-else class="text-center py-8 text-gray-500">
      <svg class="w-12 h-12 mx-auto text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
      </svg>
      <p class="mt-2">No hay actividad reciente</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RecentActivity',
  props: {
    activities: {
      type: Array,
      default: () => []
    }
  },
  setup() {
    const getActivityBgColor = (type) => {
      const colors = {
        contact: 'bg-blue-100',
        conversation: 'bg-green-100',
        message: 'bg-purple-100',
        system: 'bg-gray-100'
      }
      return colors[type] || 'bg-gray-100'
    }
    
    const getActivityIconColor = (type) => {
      const colors = {
        contact: 'text-blue-600',
        conversation: 'text-green-600',
        message: 'text-purple-600',
        system: 'text-gray-600'
      }
      return colors[type] || 'text-gray-600'
    }
    
    const getActivityIcon = (type) => {
      // Return component name for dynamic component
      return type + 'Icon'
    }

    // These would be registered globally or imported locally
    const contactIcon = {
      template: `
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
        </svg>
      `
    }

    const conversationIcon = {
      template: `
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
        </svg>
      `
    }

    const messageIcon = {
      template: `
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"></path>
        </svg>
      `
    }

    const systemIcon = {
      template: `
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path>
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
        </svg>
      `
    }
    
    return {
      getActivityBgColor,
      getActivityIconColor,
      getActivityIcon,
      contactIcon,
      conversationIcon,
      messageIcon,
      systemIcon
    }
  }
}
</script>