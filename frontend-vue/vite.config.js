import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    // Proxy para desarrollo: /api -> http://backend:8000/api
    // Nota: Usa 'backend' si es el nombre del servicio en docker-compose
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000', 
        changeOrigin: true,
      }
    }
  }
})