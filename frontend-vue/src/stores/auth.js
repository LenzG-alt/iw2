import { defineStore } from 'pinia'
import api from '@/services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('auth_token') || null,
    user: JSON.parse(localStorage.getItem('auth_user')) || null,
    loading: false,
    error: null
  }),

  getters: {
    isAuthenticated: (state) => !!state.token
  },

  actions: {
    async login(username, password) {
      this.loading = true
      this.error = null
      try {
        const response = await api.post('/token/', { username, password })
        
        const token = response.data.token || response.data.access
        
        this.token = token
        localStorage.setItem('auth_token', token)
        this.user = { username } 

        return true
      } catch (err) {
        this.error = 'Credenciales inválidas o error de servidor'
        throw err
      } finally {
        this.loading = false
      }
    },

    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('auth_token')
      localStorage.removeItem('auth_user')
    }
  }
})

    