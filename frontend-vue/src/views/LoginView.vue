<template>
  <div class="login-page">
    <form @submit.prevent="handleSubmit" class="login-form">
      <header class="form-header">
        <span class="logo">✂</span>
        <h1>SGCP</h1>
        <p>Gestión de Citas para Peluquerías</p>
      </header>

      <div class="field">
        <label for="username">Usuario</label>
        <input
          id="username"
          v-model="username"
          type="text"
          placeholder="tu_usuario"
          required
          autocomplete="username"
          autofocus
        />
      </div>

      <div class="field">
        <label for="password">Contraseña</label>
        <input
          id="password"
          v-model="password"
          type="password"
          placeholder="••••••••"
          required
          autocomplete="current-password"
        />
      </div>

      <button type="submit" class="btn-login" :disabled="authStore.loading">
        <span v-if="authStore.loading" class="loader"></span>
        {{ authStore.loading ? 'Ingresando...' : 'Ingresar' }}
      </button>

      <p v-if="authStore.error" class="error">{{ authStore.error }}</p>
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
    // manejado en el store
  }
}
</script>

<style scoped>
.login-page {
  font-family: 'Outfit', system-ui, sans-serif;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: #0c0c0c;
  padding: 1.5rem;
}

.login-form {
  width: 100%;
  max-width: 360px;
}

.form-header {
  margin-bottom: 2.5rem;
}

.logo {
  display: inline-block;
  font-size: 1.4rem;
  margin-bottom: 0.75rem;
  opacity: 0.7;
}

.form-header h1 {
  font-size: 1.6rem;
  font-weight: 600;
  color: #e8e8e8;
  margin: 0 0 0.35rem;
  letter-spacing: -0.02em;
}

.form-header p {
  font-size: 0.875rem;
  color: #666;
  margin: 0;
}

.field {
  margin-bottom: 1.25rem;
}

label {
  display: block;
  font-size: 0.8rem;
  font-weight: 500;
  color: #888;
  margin-bottom: 0.4rem;
}

input {
  width: 100%;
  padding: 0.7rem 0.85rem;
  background: #161616;
  border: 1px solid #252525;
  border-radius: 8px;
  color: #e8e8e8;
  font-size: 0.9rem;
  font-family: inherit;
  transition: border-color 0.15s ease;
  box-sizing: border-box;
}

input::placeholder {
  color: #444;
}

input:focus {
  outline: none;
  border-color: #555;
}

.btn-login {
  width: 100%;
  padding: 0.75rem;
  margin-top: 0.75rem;
  background: #e8e8e8;
  color: #0c0c0c;
  border: none;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: opacity 0.15s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.btn-login:hover {
  opacity: 0.85;
}

.btn-login:active {
  opacity: 0.7;
}

.btn-login:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.loader {
  width: 14px;
  height: 14px;
  border: 1.5px solid transparent;
  border-top-color: #0c0c0c;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

.error {
  margin-top: 1rem;
  padding: 0.65rem 0.85rem;
  background: #1a1212;
  border: 1px solid #2a1a1a;
  border-radius: 8px;
  color: #c47a7a;
  font-size: 0.825rem;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>