<template>
  <div class="hello">
    <h1 class="text-2xl font-bold mb-4">{{ msg }}</h1>
    <p class="mb-4">
      Bienvenido al Sistema Agente Conversacional de Ventas SCAIE.
      Esta es una aplicación Vue 3 construida con Tailwind CSS.
    </p>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
      <div class="bg-blue-100 p-4 rounded-lg">
        <h3 class="font-semibold text-lg mb-2">Frontend</h3>
        <ul class="list-disc pl-5 space-y-1">
          <li>Vue 3</li>
          <li>Vue Router</li>
          <li>Tailwind CSS</li>
          <li>Vite</li>
        </ul>
      </div>
      <div class="bg-green-100 p-4 rounded-lg">
        <h3 class="font-semibold text-lg mb-2">Backend</h3>
        <ul class="list-disc pl-5 space-y-1">
          <li>Python FastAPI</li>
          <li>SQLAlchemy</li>
          <li>SQLite</li>
          <li>Qwen AI Integration</li>
        </ul>
      </div>
    </div>
    <div class="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-4">
      <p>Consulta la <a href="/docs" class="text-blue-600 hover:underline">documentación de la API</a> para más información sobre los endpoints disponibles.</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  props: {
    msg: {
      type: String,
      default: '¡Bienvenido a SCAIE!'
    }
  }
}
</script>