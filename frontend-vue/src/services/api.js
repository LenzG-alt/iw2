import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api',
  headers: {
    'Content-Type': 'application/json',
  }
})

// INTERCEPTOR DE PETICIÓN
// Se ejecuta antes de enviar cada request
api.interceptors.request.use(
  (config) => {
    // En desarrollo, no requiere autenticación
    // Los endpoints son públicos (AllowAny)
    
    // Si necesitas agregar token más adelante, descomenta:
    // const token = localStorage.getItem('auth_token')
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`
    // }
    
    console.log("Enviando petición a:", config.url);
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)


// INTERCEPTOR DE RESPUESTA
// Para manejar errores globales
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Token inválido, limpiar y redirigir
      localStorage.removeItem('auth_token')
      // window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api

