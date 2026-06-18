<template>
  <div class="dashboard-container">
    <header class="top-bar">
      <h1>Citas SGCP</h1>
      <button @click="handleLogout" class="btn-logout">Cerrar Sesión</button>
    </header>

    <main>
      <!-- Estado de carga -->
      <div v-if="loading" class="loading">Cargando citas...</div>

      <!-- Error de carga -->
      <div v-else-if="error" class="error-box">
        {{ error }}
        <button @click="fetchCitas">Reintentar</button>
      </div>

      <!-- Listado de Citas -->
      <div v-else class="citas-grid">
        <div 
          v-for="cita in citas" 
          :key="cita.id" 
          class="cita-card"
        >
          <div class="card-header">
            <span class="id">#{{ cita.id }}</span>
            <span :class="['badge', getStatusClass(cita.estado)]">
              {{ cita.estado }}
            </span>
          </div>
          
          <div class="card-body">
            <div class="client-info">
              <div class="avatar">
                {{ getInitials(cita.user.nombre) }}
              </div>
              <div>
                <h3>{{ cita.user.nombre }}</h3>
                <small>{{ cita.user.email }}</small>
              </div>
            </div>

            <div class="details">
              <div class="row">
                <i class="icon">✂️</i>
                <span>{{ cita.service.nombre }}</span>
              </div>
              <div class="row">
                <i class="icon">👩‍🎨</i>
                <span>{{ cita.stylist.nombre }}</span>
              </div>
              <div class="row">
                <i class="icon">📅</i>
                <span>{{ formatDate(cita.fecha) }} | {{ cita.hora_inicio }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'

const router = useRouter()
const authStore = useAuthStore()

const citas = ref([])
const loading = ref(true)
const error = ref(null)

const fetchCitas = async () => {
  loading.value = true
  error.value = null
  try {
    // Llamada limpia, el interceptor se encarga del Token
    const response = await api.get('/citas/')
    citas.value = response.data.results
  } catch (err) {
    console.error(err)
    error.value = 'No se pudieron cargar las citas.'
  } finally {
    loading.value = false
  }
}

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

// Helpers de formato
const getInitials = (name) => name ? name.substring(0, 2).toUpperCase() : 'NA'
const getStatusClass = (status) => status === 'confirmada' ? 'bg-green' : 'bg-red'
const formatDate = (dateStr) => new Date(dateStr).toLocaleDateString('es-ES', { weekday: 'short', day: 'numeric', month: 'short' })

onMounted(() => {
  fetchCitas()
})
</script>

<style scoped>
.dashboard-container { max-width: 1200px; margin: 0 auto; padding: 20px; }
.top-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
.btn-logout { padding: 8px 16px; background: #ef4444; color: white; border: none; border-radius: 4px; cursor: pointer; }

.citas-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
.cita-card { background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border: 1px solid #e5e7eb; }

.card-header { padding: 15px; background: #f9fafb; border-bottom: 1px solid #e5e7eb; display: flex; justify-content: space-between; font-weight: 600; font-size: 0.9rem; }
.badge { padding: 4px 8px; border-radius: 12px; font-size: 0.75rem; text-transform: uppercase; }
.bg-green { background: #d1fae5; color: #065f46; }
.bg-red { background: #fee2e2; color: #991b1b; }

.card-body { padding: 20px; }
.client-info { display: flex; gap: 12px; margin-bottom: 15px; align-items: center; }
.avatar { width: 40px; height: 40px; background: #e0e7ff; color: #4338ca; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; }

.details { background: #f8fafc; padding: 10px; border-radius: 6px; font-size: 0.9rem; }
.row { display: flex; gap: 8px; margin-bottom: 5px; align-items: center; }
.icon { font-style: normal; }
</style>