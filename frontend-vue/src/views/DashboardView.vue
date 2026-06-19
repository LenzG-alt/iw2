<template>
  <div class="dashboard">
    <header class="header">
      <h1>SGCP</h1>
      <button @click="handleLogout" class="btn-logout">Cerrar sesión</button>
    </header>

    <nav class="nav">
      <router-link to="/" class="nav-link">Dashboard</router-link>
      <router-link to="/peluquerias" class="nav-link">Peluquerías</router-link>
      <router-link to="/usuarios" class="nav-link">Usuarios</router-link>
      <router-link to="/estilistas" class="nav-link">Estilistas</router-link>
      <router-link to="/servicios" class="nav-link">Servicios</router-link>
      <router-link to="/citas" class="nav-link">Citas</router-link>
      <router-link to="/horarios" class="nav-link">Horarios</router-link>
    </nav>

    <main class="content">
      <div class="stats">
        <div class="stat">
          <span class="stat-label">Citas</span>
          <span class="stat-number">{{ totalCitas }}</span>
        </div>
        <div class="stat">
          <span class="stat-label">Estilistas</span>
          <span class="stat-number">{{ totalEstilistas }}</span>
        </div>
        <div class="stat">
          <span class="stat-label">Usuarios</span>
          <span class="stat-number">{{ totalUsuarios }}</span>
        </div>
        <div class="stat">
          <span class="stat-label">Servicios</span>
          <span class="stat-number">{{ totalServicios }}</span>
        </div>
        <div class="stat">
          <span class="stat-label">Confirmadas</span>
          <span class="stat-number">{{ confirmadasCount }}</span>
        </div>
        <div class="stat">
          <span class="stat-label">Pendientes</span>
          <span class="stat-number">{{ pendientesCount }}</span>
        </div>
        <div class="stat">
          <span class="stat-label">Canceladas</span>
          <span class="stat-number">{{ canceladasCount }}</span>
        </div>
        <div class="stat">
          <span class="stat-label">Ingresos Est.</span>
          <span class="stat-number stat-currency">{{ formatPrice(totalIngresos) }}</span>
        </div>
      </div>

      <section class="recent" v-if="citas.length > 0">
        <div class="recent-header">
          <h2>Citas</h2>
          <div class="filters">
            <input 
              v-model="searchQuery" 
              type="text" 
              placeholder="Buscar..." 
              class="input-search"
            />
            <select v-model="statusFilter" class="select-filter">
              <option value="">Todos</option>
              <option value="confirmada">Confirmada</option>
              <option value="pendiente">Pendiente</option>
              <option value="cancelada">Cancelada</option>
            </select>
          </div>
        </div>
        
        <table>
          <thead>
            <tr>
              <th>Cliente</th>
              <th>Servicio</th>
              <th>Estilista</th>
              <th>Fecha</th>
              <th>Importe</th>
              <th>Estado</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="cita in filteredCitas" :key="cita.id" @click="openModal(cita)">
              <td class="strong">{{ cita.user?.nombre || '—' }}</td>
              <td class="muted">{{ cita.service?.nombre || '—' }}</td>
              <td>{{ cita.stylist?.nombre || '—' }}</td>
              <td class="mono">{{ formatDate(cita.fecha) }} {{ formatTime(cita.hora_inicio) }}</td>
              <td class="mono">{{ formatPrice(cita.service?.precio) }}</td>
              <td>
                <span :class="['badge', cita.estado]">{{ formatEstado(cita.estado) }}</span>
              </td>
            </tr>
          </tbody>
        </table>
      </section>
      
      <div v-else class="empty-state">
        No hay citas registradas
      </div>
    </main>

    <!-- Modal -->
    <div v-if="selectedCita" class="modal-overlay" @click.self="selectedCita = null">
      <div class="modal">
        <div class="modal-header">
          <h2>Cita #{{ selectedCita.id }}</h2>
          <button @click="selectedCita = null" class="btn-close">&times;</button>
        </div>
        
        <div class="modal-body">
          <div class="modal-grid">
            <div class="modal-col">
              <h4>Cliente</h4>
              <p>{{ selectedCita.user?.nombre }}</p>
              <p class="muted">{{ selectedCita.user?.email }}</p>
              <p class="muted">{{ selectedCita.user?.telefono }}</p>
            </div>
            <div class="modal-col">
              <h4>Estilista</h4>
              <p>{{ selectedCita.stylist?.nombre }}</p>
              <p class="muted">{{ selectedCita.stylist?.especialidad }}</p>
            </div>
            <div class="modal-col">
              <h4>Servicio</h4>
              <p>{{ selectedCita.service?.nombre }}</p>
              <p>{{ formatPrice(selectedCita.service?.precio) }} · {{ selectedCita.service?.duracion_minutos }} min</p>
            </div>
            <div class="modal-col">
              <h4>Agenda</h4>
              <p>{{ formatDate(selectedCita.fecha) }}</p>
              <p>{{ formatTime(selectedCita.hora_inicio) }} - {{ formatTime(selectedCita.hora_fin) }}</p>
            </div>
          </div>
          
          <div class="modal-obs" v-if="selectedCita.observaciones">
            <h4>Observaciones</h4>
            <p>{{ selectedCita.observaciones }}</p>
          </div>
        </div>

        <div class="modal-footer">
          <span :class="['badge', selectedCita.estado]">{{ formatEstado(selectedCita.estado) }}</span>
          <button @click="selectedCita = null" class="btn-close-modal">Cerrar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'

const authStore = useAuthStore()

const citas = ref([])
const estilistas = ref([])
const usuarios = ref([])
const servicios = ref([])

const searchQuery = ref('')
const statusFilter = ref('')
const selectedCita = ref(null)

// Estadísticas generales
const totalCitas = computed(() => citas.value.length)
const totalEstilistas = computed(() => estilistas.value.length)
const totalUsuarios = computed(() => usuarios.value.length)
const totalServicios = computed(() => servicios.value.length)

// Estadísticas derivadas de citas
const confirmadasCount = computed(() => citas.value.filter(c => c.estado === 'confirmada').length)
const pendientesCount = computed(() => citas.value.filter(c => c.estado === 'pendiente').length)
const canceladasCount = computed(() => citas.value.filter(c => c.estado === 'cancelada').length)
const totalIngresos = computed(() => {
  return citas.value
    .filter(c => c.estado === 'confirmada')
    .reduce((sum, c) => sum + parseFloat(c.service?.precio || 0), 0)
})

// Filtros
const filteredCitas = computed(() => {
  return citas.value.filter(cita => {
    const matchesStatus = !statusFilter.value || cita.estado === statusFilter.value
    const q = searchQuery.value.toLowerCase()
    const matchesSearch = !q || 
      (cita.user?.nombre || '').toLowerCase().includes(q) ||
      (cita.stylist?.nombre || '').toLowerCase().includes(q) ||
      (cita.service?.nombre || '').toLowerCase().includes(q)
    return matchesStatus && matchesSearch
  })
})

// Formateo
const formatDate = (str) => {
  if (!str) return '—'
  return new Date(str).toLocaleDateString('es-ES', { day: '2-digit', month: 'short' })
}

const formatTime = (str) => {
  if (!str) return ''
  return str.slice(0, 5)
}

const formatEstado = (estado) => {
  return estado?.charAt(0).toUpperCase() + estado?.slice(1) || estado
}

const formatPrice = (price) => {
  if (!price && price !== 0) return 'S/. 0.00'
  return `S/. ${parseFloat(price).toFixed(2)}`
}

// Acciones
const handleLogout = () => {
  authStore.logout()
  window.location.href = '/login'
}

const openModal = (cita) => {
  selectedCita.value = cita
}

const cargarDatos = async () => {
  try {
    const [resCitas, resEstilistas, resUsuarios, resServicios] = await Promise.all([
      api.get('/citas/').catch(() => ({ data: [] })),
      api.get('/estilistas/').catch(() => ({ data: [] })),
      api.get('/usuarios/').catch(() => ({ data: [] })),
      api.get('/servicios/').catch(() => ({ data: [] }))
    ])

    citas.value = resCitas.data.results || resCitas.data
    estilistas.value = resEstilistas.data.results || resEstilistas.data
    usuarios.value = resUsuarios.data.results || resUsuarios.data
    servicios.value = resServicios.data.results || resServicios.data
  } catch (err) {
    console.error(err)
  }
}

onMounted(cargarDatos)
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  background: #0c0c0c;
  color: #ccc;
  font-family: 'Outfit', system-ui, sans-serif;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.85rem 1.5rem;
  border-bottom: 1px solid #1a1a1a;
}

.header h1 {
  font-size: 1rem;
  font-weight: 600;
  color: #e8e8e8;
  margin: 0;
  letter-spacing: -0.01em;
}

.btn-logout {
  padding: 0.4rem 0.85rem;
  background: none;
  border: 1px solid #2a2a2a;
  border-radius: 6px;
  color: #888;
  font-size: 0.8rem;
  font-family: inherit;
  cursor: pointer;
  transition: color 0.15s, border-color 0.15s;
}

.btn-logout:hover {
  color: #c47a7a;
  border-color: #3a2222;
}

.nav {
  display: flex;
  gap: 0;
  padding: 0 1.5rem;
  border-bottom: 1px solid #1a1a1a;
  overflow-x: auto;
}

.nav-link {
  padding: 0.7rem 1rem;
  color: #666;
  text-decoration: none;
  font-size: 0.825rem;
  font-weight: 500;
  border-bottom: 2px solid transparent;
  transition: color 0.15s, border-color 0.15s;
  white-space: nowrap;
}

.nav-link:hover {
  color: #aaa;
}

.nav-link.router-link-active {
  color: #e8e8e8;
  border-bottom-color: #e8e8e8;
}

.content {
  padding: 1.5rem;
  max-width: 960px;
}

.stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1px;
  background: #1a1a1a;
  border: 1px solid #1a1a1a;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 2rem;
}

.stat {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  padding: 1.1rem 1.25rem;
  background: #111;
}

.stat-label {
  font-size: 0.75rem;
  color: #666;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.stat-number {
  font-size: 1.5rem;
  font-weight: 600;
  color: #e8e8e8;
}

.stat-currency {
  font-size: 1.2rem;
}

.recent-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.recent h2 {
  font-size: 0.9rem;
  font-weight: 600;
  color: #e8e8e8;
  margin: 0;
}

.filters {
  display: flex;
  gap: 0.5rem;
}

.input-search {
  padding: 0.4rem 0.7rem;
  background: #111;
  border: 1px solid #1a1a1a;
  border-radius: 6px;
  color: #e8e8e8;
  font-size: 0.8rem;
  font-family: inherit;
  width: 180px;
}

.input-search::placeholder {
  color: #444;
}

.input-search:focus {
  outline: none;
  border-color: #333;
}

.select-filter {
  padding: 0.4rem 0.5rem;
  background: #111;
  border: 1px solid #1a1a1a;
  border-radius: 6px;
  color: #ccc;
  font-size: 0.8rem;
  font-family: inherit;
  cursor: pointer;
}

.select-filter:focus {
  outline: none;
  border-color: #333;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.825rem;
}

thead th {
  text-align: left;
  padding: 0.6rem 0.75rem;
  color: #555;
  font-weight: 500;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  border-bottom: 1px solid #1a1a1a;
}

tbody tr {
  cursor: pointer;
  transition: background 0.1s;
}

tbody tr:hover {
  background: #141414;
}

tbody td {
  padding: 0.65rem 0.75rem;
  border-bottom: 1px solid #141414;
  color: #aaa;
}

tbody tr:last-child td {
  border-bottom: none;
}

.strong {
  color: #e8e8e8;
  font-weight: 500;
}

.muted {
  color: #555;
}

.mono {
  font-variant-numeric: tabular-nums;
  color: #888;
}

.badge {
  display: inline-block;
  padding: 0.15rem 0.55rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
}

.badge.confirmada {
  background: #122218;
  color: #5fa868;
}

.badge.pendiente {
  background: #1a1812;
  color: #b8a44a;
}

.badge.completada {
  background: #121820;
  color: #5a8fbf;
}

.badge.cancelada {
  background: #1a1212;
  color: #b05a5a;
}

.empty-state {
  text-align: center;
  padding: 3rem 1rem;
  color: #555;
  font-size: 0.85rem;
}

/* Modal */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
}

.modal {
  width: 100%;
  max-width: 560px;
  background: #141414;
  border: 1px solid #222;
  border-radius: 8px;
  overflow: hidden;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.25rem;
  border-bottom: 1px solid #1a1a1a;
}

.modal-header h2 {
  font-size: 0.95rem;
  font-weight: 600;
  color: #e8e8e8;
  margin: 0;
}

.btn-close {
  background: none;
  border: none;
  color: #555;
  font-size: 1.4rem;
  cursor: pointer;
  line-height: 1;
}

.btn-close:hover {
  color: #aaa;
}

.modal-body {
  padding: 1.25rem;
}

.modal-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.25rem;
  margin-bottom: 1.25rem;
}

.modal-col h4 {
  font-size: 0.7rem;
  color: #555;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin: 0 0 0.35rem;
}

.modal-col p {
  margin: 0;
  font-size: 0.85rem;
  color: #bbb;
  line-height: 1.5;
}

.modal-obs {
  border-top: 1px solid #1a1a1a;
  padding-top: 1rem;
}

.modal-obs h4 {
  font-size: 0.7rem;
  color: #555;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin: 0 0 0.35rem;
}

.modal-obs p {
  margin: 0;
  font-size: 0.85rem;
  color: #888;
  line-height: 1.5;
}

.modal-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.85rem 1.25rem;
  border-top: 1px solid #1a1a1a;
  background: #111;
}

.btn-close-modal {
  padding: 0.35rem 0.85rem;
  background: none;
  border: 1px solid #2a2a2a;
  border-radius: 6px;
  color: #888;
  font-size: 0.8rem;
  font-family: inherit;
  cursor: pointer;
}

.btn-close-modal:hover {
  color: #ccc;
  border-color: #444;
}

@media (max-width: 768px) {
  .stats {
    grid-template-columns: repeat(2, 1fr);
  }
  .recent-header {
    flex-direction: column;
    align-items: flex-start;
  }
  .filters {
    width: 100%;
  }
  .input-search {
    flex: 1;
    width: auto;
  }
}

@media (max-width: 640px) {
  .content {
    padding: 1rem;
  }
  .modal-grid {
    grid-template-columns: 1fr;
  }
}
</style>