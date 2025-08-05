import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000
  },
  base: '/',
  root: __dirname,
  publicDir: 'public',
  build: {
    outDir: resolve(__dirname, '../backend/static'),
    emptyOutDir: true,
    assetsDir: 'assets',
    rollupOptions: {
      // Configuración mínima para la salida
      output: {
        entryFileNames: 'assets/[name].[hash].js',
        chunkFileNames: 'assets/[name].[hash].js',
        assetFileNames: 'assets/[name].[hash][extname]'
      }
    }
  },
  resolve: {
    alias: {
      '@': resolve(__dirname, './src')
    }
  }
})