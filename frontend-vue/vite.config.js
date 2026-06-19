import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
    server: {
    // Esto hace que las llamadas a /api/ vayan a tu Django en el 8000
    proxy: {
      '/api': {
        target: 'https://sgcpbackend.vercel.app',
        changeOrigin: true
      }
    }
  }
})


