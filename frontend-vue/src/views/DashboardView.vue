<template>
  <div class="dashboard-container">
    <div class="glow-bg"></div>
    
    <!-- Barra Superior -->
    <header class="top-bar glass-panel">
      <div class="brand">
        <span class="logo-icon"></span>
        <h1>SGCP</h1>
        <span class="divider">|</span>
        <span class="panel-tag">Panel Administrativo</span>
      </div>
      <div class="user-actions">
        <div class="user-profile">
          <div class="user-avatar">{{ authStore.user?.username?.substring(0, 2).toUpperCase() || 'AD' }}</div>
          <div class="user-details">
            <span class="user-name">{{ authStore.user?.username || 'Administrador' }}</span>
            <span class="user-role">Personal</span>
          </div>
        </div>
        <button @click="handleLogout" class="btn-logout">
          Cerrar Sesión <span class="logout-icon">➔</span>
        </button>
      </div>
    </header>

    <main class="main-content">
      <!-- Estadísticas Grid -->
      <section class="stats-grid">
        <div class="stat-card glass-panel stat-indigo">
          <div class="stat-info">
            <h3>Citas Totales</h3>
            <div class="stat-value">{{ totalCitas }}</div>
          </div>
          <div class="stat-icon-wrapper">📅</div>
        </div>
        
        <div class="stat-card glass-panel stat-emerald">
          <div class="stat-info">
            <h3>Confirmadas</h3>
            <div class="stat-value">{{ confirmadasCount }}</div>
          </div>
          <div class="stat-icon-wrapper">✓</div>
        </div>

        <div class="stat-card glass-panel stat-rose">
          <div class="stat-info">
            <h3>Canceladas</h3>
            <div class="stat-value">{{ canceladasCount }}</div>
          </div>
          <div class="stat-icon-wrapper">✕</div>
        </div>

        <div class="stat-card glass-panel stat-cyan">
          <div class="stat-info">
            <h3>Ingresos Estimados</h3>
            <div class="stat-value">{{ formatPrice(totalIngresos) }}</div>
          </div>
          <div class="stat-icon-wrapper">💰</div>
        </div>
      </section>

      <!-- Panel de Búsqueda y Filtros -->
      <section class="filters-panel glass-panel">
        <div class="search-box">
          <span class="search-icon">🔍</span>
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="Buscar por cliente, estilista o servicio..." 
          />
        </div>
        <div class="filter-actions">
          <select v-model="statusFilter" class="filter-select">
            <option value="">Todos los estados</option>
            <option value="confirmada">Confirmada</option>
            <option value="cancelada">Cancelada</option>
            <option value="pendiente">Pendiente</option>
          </select>
          <button @click="fetchCitas" :disabled="loading" class="btn-refresh">
            <span :class="{'spin': loading}">🔄</span> Actualizar
          </button>
        </div>
      </section>

      <!-- Estado de carga -->
      <div v-if="loading" class="spinner-container glass-panel">
        <div class="spinner"></div>
        <p>Cargando citas...</p>
      </div>

      <!-- Error de carga -->
      <div v-else-if="error" class="error-box glass-panel">
        <div class="error-icon">⚠</div>
        <div class="error-text">
          <h3>Error de Conexión</h3>
          <p>{{ error }}</p>
        </div>
        <button @click="fetchCitas" class="btn-retry">Reintentar</button>
      </div>

      <!-- Listado de Citas -->
      <div v-else-if="filteredCitas.length > 0" class="citas-grid">
        <div 
          v-for="cita in filteredCitas" 
          :key="cita.id" 
          class="cita-card glass-panel"
          @click="selectedCita = cita"
        >
          <div class="card-header">
            <span class="id">Cita #{{ cita.id }}</span>
            <span :class="['badge', getStatusClass(cita.estado)]">
              {{ cita.estado }}
            </span>
          </div>
          
          <div class="card-body">
            <div class="client-info">
              <div class="avatar">
                {{ getInitials(cita.user.nombre) }}
              </div>
              <div class="client-meta">
                <h3>{{ cita.user.nombre }}</h3>
                <small>{{ cita.user.email }}</small>
              </div>
            </div>

            <div class="details">
              <div class="row">
                <span class="icon">✂️</span>
                <div class="row-info">
                  <span class="label">Servicio</span>
                  <span class="val">{{ cita.service.nombre }}</span>
                </div>
              </div>
              <div class="row">
                <span class="icon">👩‍🎨</span>
                <div class="row-info">
                  <span class="label">Estilista</span>
                  <span class="val">{{ cita.stylist.nombre }}</span>
                </div>
              </div>
              <div class="row">
                <span class="icon">📅</span>
                <div class="row-info">
                  <span class="label">Horario</span>
                  <span class="val">{{ formatDate(cita.fecha) }} a las {{ formatTime(cita.hora_inicio) }}</span>
                </div>
              </div>
            </div>
            
            <div class="card-footer">
              <span class="price">{{ formatPrice(cita.service.precio) }}</span>
              <span class="duration">⏱ {{ cita.service.duracion_minutos }} min</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Sin Resultados -->
      <div v-else class="empty-box glass-panel">
        <div class="empty-icon">📭</div>
        <h3>No se encontraron citas</h3>
        <p>Prueba ajustando los términos de búsqueda o filtros.</p>
      </div>
    </main>

    <!-- Modal de Detalles -->
    <transition name="fade">
      <div v-if="selectedCita" class="modal-overlay" @click.self="selectedCita = null">
        <div class="modal-card glass-panel">
          <div class="modal-header">
            <h2>Detalle de Cita #{{ selectedCita.id }}</h2>
            <button @click="selectedCita = null" class="btn-close">&times;</button>
          </div>
          <div class="modal-body">
            <div class="modal-status">
              <span :class="['badge', getStatusClass(selectedCita.estado)]">{{ selectedCita.estado }}</span>
              <small>Registrado: {{ new Date(selectedCita.fecha_creacion).toLocaleDateString() }}</small>
            </div>

            <div class="modal-grid">
              <div class="modal-section">
                <h4>Datos del Cliente</h4>
                <p><strong>Nombre:</strong> {{ selectedCita.user.nombre }}</p>
                <p><strong>Email:</strong> {{ selectedCita.user.email }}</p>
                <p><strong>Teléfono:</strong> {{ selectedCita.user.telefono }}</p>
              </div>

              <div class="modal-section">
                <h4>Estilista</h4>
                <p><strong>Nombre:</strong> {{ selectedCita.stylist.nombre }}</p>
                <p><strong>Especialidad:</strong> {{ selectedCita.stylist.especialidad }}</p>
                <p><strong>Teléfono:</strong> {{ selectedCita.stylist.telefono }}</p>
              </div>

              <div class="modal-section">
                <h4>Servicio Contratado</h4>
                <p><strong>Nombre:</strong> {{ selectedCita.service.nombre }}</p>
                <p><strong>Precio:</strong> <span class="modal-price">{{ formatPrice(selectedCita.service.precio) }}</span></p>
                <p><strong>Duración:</strong> {{ selectedCita.service.duracion_minutos }} min</p>
                <p><strong>Descripción:</strong> {{ selectedCita.service.descripcion }}</p>
              </div>

              <div class="modal-section">
                <h4>Fecha y Hora</h4>
                <p><strong>Fecha:</strong> {{ formatDate(selectedCita.fecha) }}</p>
                <p><strong>Horario:</strong> {{ formatTime(selectedCita.hora_inicio) }} - {{ formatTime(selectedCita.hora_fin) }}</p>
              </div>

              <div class="modal-section full-width">
                <h4>Observaciones</h4>
                <div class="obs-box">
                  {{ selectedCita.observaciones || 'Sin observaciones registradas.' }}
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button @click="selectedCita = null" class="btn-primary">Cerrar</button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'

const router = useRouter()
const authStore = useAuthStore()

const citas = ref([])
const loading = ref(true)
const error = ref(null)

const searchQuery = ref('')
const statusFilter = ref('')
const selectedCita = ref(null)

// Computed Properties para Estadísticas
const totalCitas = computed(() => citas.value.length)
const confirmadasCount = computed(() => citas.value.filter(c => c.estado === 'confirmada').length)
const canceladasCount = computed(() => citas.value.filter(c => c.estado === 'cancelada').length)
const totalIngresos = computed(() => {
  return citas.value
    .filter(c => c.estado === 'confirmada')
    .reduce((sum, c) => sum + parseFloat(c.service?.precio || 0), 0)
    .toFixed(2)
})

// Computed Property para filtrar
const filteredCitas = computed(() => {
  return citas.value.filter(cita => {
    // Filtro de estado
    const matchesStatus = !statusFilter.value || cita.estado === statusFilter.value
    
    // Filtro de búsqueda
    const searchLower = searchQuery.value.toLowerCase()
    const clientName = (cita.user?.nombre || '').toLowerCase()
    const stylistName = (cita.stylist?.nombre || '').toLowerCase()
    const serviceName = (cita.service?.nombre || '').toLowerCase()
    const matchesSearch = !searchQuery.value || 
      clientName.includes(searchLower) ||
      stylistName.includes(searchLower) ||
      serviceName.includes(searchLower)

    return matchesStatus && matchesSearch
  })
})

const fetchCitas = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await api.get('/citas/')
    citas.value = response.data.results ? response.data.results : (Array.isArray(response.data) ? response.data : [])
  } catch (err) {
    console.error(err)
    error.value = 'No se pudieron cargar las citas del servidor backend.'
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
const getStatusClass = (status) => {
  if (status === 'confirmada') return 'badge-confirmada'
  if (status === 'cancelada') return 'badge-cancelada'
  return 'badge-pendiente'
}
const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const parts = dateStr.split('-')
  if (parts.length === 3) {
    const date = new Date(parts[0], parts[1] - 1, parts[2])
    return date.toLocaleDateString('es-ES', { weekday: 'short', day: 'numeric', month: 'short' })
  }
  return dateStr
}
const formatTime = (timeStr) => {
  if (!timeStr) return ''
  const parts = timeStr.split(':')
  if (parts.length >= 2) {
    return `${parts[0]}:${parts[1]}`
  }
  return timeStr
}
const formatPrice = (price) => {
  if (price === undefined || price === null) return 'S/. 0.00'
  return `S/. ${parseFloat(price).toFixed(2)}`
}

onMounted(() => {
  fetchCitas()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

.dashboard-container {
  font-family: 'Outfit', sans-serif;
  background-color: #0a0e17;
  color: #f8fafc;
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
  padding-bottom: 3rem;
}

.glow-bg {
  position: absolute;
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, rgba(99, 102, 241, 0.08) 0%, transparent 70%);
  top: -10%;
  right: -10%;
  z-index: 1;
  pointer-events: none;
}

.glass-panel {
  background: rgba(20, 26, 46, 0.65);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
}

/* Header */
.top-bar {
  position: sticky;
  top: 0;
  z-index: 50;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 2rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 0 0 20px 20px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.logo-icon {
  font-size: 1.8rem;
  animation: snip 3s infinite ease-in-out;
}

h1 {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
  background: linear-gradient(135deg, #22d3ee, #6366f1);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.divider {
  color: rgba(255, 255, 255, 0.15);
  font-weight: 300;
}

.panel-tag {
  color: #94a3b8;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.user-actions {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.user-avatar {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #6366f1, #a855f7);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  color: white;
  font-size: 0.9rem;
  box-shadow: 0 0 10px rgba(99, 102, 241, 0.3);
}

.user-details {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-size: 0.9rem;
  font-weight: 600;
}

.user-role {
  font-size: 0.75rem;
  color: #22d3ee;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.btn-logout {
  background: rgba(239, 68, 68, 0.15);
  color: #fca5a5;
  border: 1px solid rgba(239, 68, 68, 0.3);
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-weight: 500;
  font-size: 0.85rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-family: inherit;
  transition: all 0.2s ease;
}

.btn-logout:hover {
  background: #ef4444;
  color: white;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

.logout-icon {
  transition: transform 0.2s ease;
}

.btn-logout:hover .logout-icon {
  transform: translateX(2px);
}

/* Main Content */
.main-content {
  position: relative;
  z-index: 10;
  max-width: 1300px;
  margin: 0 auto;
  padding: 2rem;
}

/* Stats */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  padding: 1.5rem;
  border-radius: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.stat-card:hover {
  transform: translateY(-4px);
  border-color: rgba(255, 255, 255, 0.15);
}

.stat-info h3 {
  font-size: 0.8rem;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.5rem;
}

.stat-value {
  font-size: 1.8rem;
  font-weight: 700;
}

.stat-icon-wrapper {
  font-size: 2rem;
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-indigo .stat-icon-wrapper { background: rgba(99, 102, 241, 0.15); color: #818cf8; }
.stat-emerald .stat-icon-wrapper { background: rgba(16, 185, 129, 0.15); color: #34d399; }
.stat-rose .stat-icon-wrapper { background: rgba(244, 63, 94, 0.15); color: #fb7185; }
.stat-cyan .stat-icon-wrapper { background: rgba(6, 182, 212, 0.15); color: #22d3ee; }

/* Filters Panel */
.filters-panel {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
  padding: 1.25rem;
  border-radius: 16px;
  margin-bottom: 2rem;
}

.search-box {
  position: relative;
  flex: 1;
  min-width: 280px;
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #64748b;
  font-size: 0.95rem;
}

.search-box input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  color: white;
  font-family: inherit;
  transition: all 0.2s ease;
}

.search-box input:focus {
  outline: none;
  border-color: #6366f1;
  background: rgba(255, 255, 255, 0.06);
}

.filter-actions {
  display: flex;
  gap: 1rem;
}

.filter-select {
  padding: 0.75rem 1rem;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  color: white;
  cursor: pointer;
  font-family: inherit;
}

.filter-select:focus {
  outline: none;
  border-color: #6366f1;
}

.btn-refresh {
  padding: 0.75rem 1.25rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-family: inherit;
  transition: all 0.2s ease;
}

.btn-refresh:hover {
  background: rgba(255, 255, 255, 0.1);
}

.btn-refresh:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.spin {
  animation: spin 1s infinite linear;
}

/* Cards Grid */
.citas-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}

.cita-card {
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

.cita-card:hover {
  transform: translateY(-6px);
  border-color: rgba(99, 102, 241, 0.4);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.4);
}

.card-header {
  padding: 1.25rem 1.5rem;
  background: rgba(255, 255, 255, 0.02);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.id {
  font-size: 0.85rem;
  font-weight: 600;
  color: #94a3b8;
}

.badge {
  padding: 0.3rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.025em;
  display: inline-flex;
  align-items: center;
}

.badge-confirmada {
  background: rgba(16, 185, 129, 0.12);
  color: #34d399;
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.badge-cancelada {
  background: rgba(244, 63, 94, 0.12);
  color: #fb7185;
  border: 1px solid rgba(244, 63, 94, 0.3);
}

.badge-pendiente {
  background: rgba(245, 158, 11, 0.12);
  color: #fcd34d;
  border: 1px solid rgba(245, 158, 11, 0.3);
}

.card-body {
  padding: 1.5rem;
}

.client-info {
  display: flex;
  gap: 0.75rem;
  align-items: center;
  margin-bottom: 1.25rem;
}

.avatar {
  width: 44px;
  height: 44px;
  background: rgba(99, 102, 241, 0.1);
  color: #818cf8;
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.95rem;
}

.client-meta h3 {
  font-size: 1rem;
  font-weight: 600;
  margin: 0;
}

.client-meta small {
  font-size: 0.8rem;
  color: #64748b;
}

.details {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.04);
  padding: 1rem;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1.25rem;
}

.row {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}

.icon {
  font-size: 1rem;
}

.row-info {
  display: flex;
  flex-direction: column;
}

.label {
  font-size: 0.7rem;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.025em;
}

.val {
  font-size: 0.85rem;
  color: #e2e8f0;
  font-weight: 500;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  padding-top: 1rem;
}

.price {
  font-size: 1.15rem;
  font-weight: 700;
  color: #34d399;
}

.duration {
  font-size: 0.8rem;
  color: #94a3b8;
}

/* Spinner and Messages */
.spinner-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 6rem;
  border-radius: 16px;
  gap: 1.5rem;
}

.spinner {
  width: 44px;
  height: 44px;
  border: 3px solid rgba(99, 102, 241, 0.1);
  border-top-color: #6366f1;
  border-radius: 50%;
  animation: spin 1s infinite linear;
}

.error-box {
  padding: 3rem;
  border-radius: 16px;
  text-align: center;
  border-color: rgba(239, 68, 68, 0.2);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.error-icon {
  font-size: 3rem;
  color: #ef4444;
}

.btn-retry {
  padding: 0.6rem 1.5rem;
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-family: inherit;
  transition: all 0.2s ease;
}

.btn-retry:hover {
  background: #dc2626;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

.empty-box {
  text-align: center;
  padding: 6rem 2rem;
  border-radius: 16px;
}

.empty-icon {
  font-size: 3.5rem;
  margin-bottom: 1rem;
}

/* Modal Overlay */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(8px);
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
}

.modal-card {
  width: 100%;
  max-width: 650px;
  border-radius: 20px;
  box-shadow: 0 20px 50px rgba(0,0,0,0.5);
  border: 1px solid rgba(255,255,255,0.1);
  overflow: hidden;
  animation: zoomIn 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.modal-header {
  padding: 1.5rem 2rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h2 {
  font-size: 1.25rem;
  margin: 0;
  font-weight: 700;
}

.btn-close {
  background: transparent;
  border: none;
  color: #94a3b8;
  font-size: 1.75rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-close:hover {
  color: white;
}

.modal-body {
  padding: 2rem;
  max-height: 70vh;
  overflow-y: auto;
}

.modal-status {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.modal-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.modal-section {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.modal-section h4 {
  margin: 0 0 0.25rem 0;
  font-size: 0.8rem;
  text-transform: uppercase;
  color: #64748b;
  letter-spacing: 0.05em;
}

.modal-price {
  color: #34d399;
  font-weight: 700;
}

.full-width {
  grid-column: 1 / span 2;
}

.obs-box {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  padding: 1rem;
  border-radius: 10px;
  font-size: 0.9rem;
  color: #cbd5e1;
  min-height: 60px;
}

.modal-footer {
  padding: 1.25rem 2rem;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  display: flex;
  justify-content: flex-end;
}

.btn-primary {
  padding: 0.6rem 1.5rem;
  background: linear-gradient(135deg, #6366f1, #a855f7);
  color: white;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  font-family: inherit;
  transition: all 0.2s ease;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@keyframes zoomIn {
  from { transform: scale(0.95); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

@keyframes snip {
  0%, 100% { transform: rotate(0deg); }
  50% { transform: rotate(-8deg); }
}

/* Transitions */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.25s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

@media (max-width: 600px) {
  .top-bar {
    padding: 1rem;
  }
  .panel-tag, .divider {
    display: none;
  }
  .user-details {
    display: none;
  }
  .filters-panel {
    flex-direction: column;
    align-items: stretch;
  }
  .filter-actions {
    width: 100%;
  }
  .filter-select, .btn-refresh {
    flex: 1;
  }
  .modal-grid {
    grid-template-columns: 1fr;
  }
  .full-width {
    grid-column: 1;
  }
}
</style>