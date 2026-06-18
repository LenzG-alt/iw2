<template>
  <div class="login-page">
    <form @submit.prevent="handleSubmit" class="login-form">
      <h2>SGCP Access</h2>
      
      <div class="form-group">
        <label>Usuario</label>
        <input v-model="username" type="text" required autofocus />
      </div>
      
      <div class="form-group">
        <label>Contraseña</label>
        <input v-model="password" type="password" required />
      </div>

      <button type="submit" :disabled="authStore.loading">
        {{ authStore.loading ? 'Autenticando...' : 'Ingresar' }}
      </button>

      <p v-if="authStore.error" class="error-msg">{{ authStore.error }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')

const handleSubmit = async () => {
  try {
    await authStore.login(username.value, password.value)
    router.push('/')
  } catch (e) {
    // El error ya se maneja en el store, pero podrías hacer log aquí
  }
}
</script>

<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f3f4f6;
}
.login-form {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 400px;
}
.form-group { margin-bottom: 1rem; }
input, button {
  width: 100%;
  padding: 0.75rem;
  margin-top: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}
button { background-color: #4f46e5; color: white; border: none; cursor: pointer; }
button:disabled { opacity: 0.7; cursor: not-allowed; }
.error-msg { color: #ef4444; margin-top: 1rem; text-align: center; }
</style>