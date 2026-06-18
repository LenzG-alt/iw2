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
    const token = localStorage.getItem('auth_token')
    
    // --- AGREGA ESTE LOG PARA DEPURAR ---
    console.log("Interceptor: Enviando petición a", config.url);
    console.log("Interceptor: Token encontrado:", token ? "SÍ" : "NO");
    
    if (token) {
      // PRUEBA 1: Intenta con 'Token' (Estándar DRF)
      config.headers.Authorization = `Bearer ${token}`
      
      // PRUEBA 2: Si la prueba 1 falla, cambia la línea de arriba por:
      // config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)


// INTERCEPTOR DE RESPUESTA
// Para manejar errores globales (ej. token expirado 401)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Token inválido, limpiar y redirigir
      localStorage.removeItem('auth_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api

