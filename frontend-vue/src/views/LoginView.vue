<template>
  <div class="login-page">
    <div class="glow-bg"></div>
    <form @submit.prevent="handleSubmit" class="login-form glass-panel">
      <div class="logo-container">
        <div class="scissors-icon">✂️</div>
        <h2>SGCP</h2>
        <p class="subtitle">Gestión de Citas para Peluquerías</p>
      </div>
      
      <div class="form-group">
        <label>Nombre de Usuario</label>
        <div class="input-wrapper">
          <span class="input-icon">👤</span>
          <input v-model="username" type="text" placeholder="Ingresa tu usuario" required autofocus />
        </div>
      </div>
      
      <div class="form-group">
        <label>Contraseña</label>
        <div class="input-wrapper">
          <span class="input-icon">🔒</span>
          <input v-model="password" type="password" placeholder="Ingresa tu contraseña" required />
        </div>
      </div>

      <button type="submit" class="btn-submit" :disabled="authStore.loading">
        <span v-if="authStore.loading" class="spinner"></span>
        <span>{{ authStore.loading ? 'Autenticando...' : 'Ingresar' }}</span>
        <span v-if="!authStore.loading" class="arrow">➔</span>
      </button>

      <transition name="fade">
        <p v-if="authStore.error" class="error-msg">
          <span class="warning-icon">⚠</span> {{ authStore.error }}
        </p>
      </transition>
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
    // El error se maneja en el store
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

.login-page {
  font-family: 'Outfit', sans-serif;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #0a0e17;
  position: relative;
  overflow: hidden;
  color: #f8fafc;
}

.glow-bg {
  position: absolute;
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, rgba(99, 102, 241, 0.15) 0%, transparent 70%);
  top: -10%;
  left: -10%;
  z-index: 1;
}

.login-page::after {
  content: '';
  position: absolute;
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, rgba(168, 85, 247, 0.12) 0%, transparent 70%);
  bottom: -10%;
  right: -10%;
  z-index: 1;
}

.login-form {
  position: relative;
  z-index: 10;
  background: rgba(20, 26, 46, 0.65);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  padding: 3rem 2.5rem;
  border-radius: 20px;
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
  width: 100%;
  max-width: 420px;
  transition: all 0.3s ease;
}

.logo-container {
  text-align: center;
  margin-bottom: 2.5rem;
}

.scissors-icon {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  display: inline-block;
  animation: snip 2s infinite ease-in-out;
}

h2 {
  font-size: 1.8rem;
  font-weight: 700;
  margin: 0;
  background: linear-gradient(135deg, #22d3ee, #6366f1, #a855f7);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.subtitle {
  color: #94a3b8;
  font-size: 0.9rem;
  margin-top: 0.5rem;
  font-weight: 400;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  font-size: 0.85rem;
  font-weight: 500;
  color: #94a3b8;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 1rem;
  font-size: 1rem;
  color: #64748b;
  pointer-events: none;
}

input {
  width: 100%;
  padding: 0.85rem 1rem 0.85rem 2.5rem;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  color: #f8fafc;
  font-size: 0.95rem;
  font-family: inherit;
  transition: all 0.25s ease;
}

input:focus {
  outline: none;
  border-color: #6366f1;
  background: rgba(255, 255, 255, 0.06);
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.3);
}

.btn-submit {
  width: 100%;
  padding: 0.9rem;
  margin-top: 1.5rem;
  background: linear-gradient(135deg, #6366f1, #a855f7);
  color: white;
  border: none;
  font-weight: 600;
  font-size: 1rem;
  border-radius: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  box-shadow: 0 4px 14px rgba(99, 102, 241, 0.4);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-family: inherit;
}

.btn-submit:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(99, 102, 241, 0.6);
}

.btn-submit:active {
  transform: translateY(0);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.arrow {
  transition: transform 0.2s ease;
}

.btn-submit:hover .arrow {
  transform: translateX(3px);
}

.spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s infinite linear;
}

.error-msg {
  background: rgba(239, 68, 68, 0.15);
  border: 1px solid rgba(239, 68, 68, 0.25);
  color: #fca5a5;
  padding: 0.8rem 1rem;
  border-radius: 12px;
  font-size: 0.85rem;
  margin-top: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  animation: shake 0.4s ease-in-out;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@keyframes snip {
  0%, 100% { transform: rotate(0deg); }
  50% { transform: rotate(-10deg) scale(1.05); }
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-6px); }
  75% { transform: translateX(6px); }
}

/* Vue Transitions */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>