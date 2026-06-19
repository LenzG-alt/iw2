<template>
  <div class="page">
    <div class="page-header">
      <h1>Citas</h1>
      <button @click="loadCitas" class="btn-refresh" :disabled="loading">
        Actualizar
      </button>
    </div>

    <div class="filters">
      <input 
        v-model="searchQuery" 
        type="text" 
        placeholder="Buscar cliente, estilista o servicio..." 
        class="input-search"
      />
      <select v-model="statusFilter" class="select-filter">
        <option value="">Todos</option>
        <option value="confirmada">Confirmada</option>
        <option value="pendiente">Pendiente</option>
        <option value="cancelada">Cancelada</option>
      </select>
    </div>

    <div v-if="loading" class="empty-state">Cargando...</div>
    <div v-else-if="error" class="empty-state error">{{ error }}</div>
    <div v-else-if="filteredCitas.length === 0" class="empty-state">Sin resultados</div>
    
    <table v-else class="table">
      <thead>
        <tr>
          <th>Cliente</th>
          <th>Servicio</th>
          <th>Estilista</th>
          <th>Fecha</th>
          <th>Hora</th>
          <th>Importe</th>
          <th>Estado</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="c in filteredCitas" :key="c.id" @click="openModal(c)">
          <td class="strong">{{ c.user?.nombre || '—' }}</td>
          <td class="muted">{{ c.service?.nombre || '—' }}</td>
          <td>{{ c.stylist?.nombre || '—' }}</td>
          <td class="mono">{{ formatDate(c.fecha) }}</td>
          <td class="mono">{{ formatTime(c.hora_inicio) }} - {{ formatTime(c.hora_fin) }}</td>
          <td class="mono">{{ formatPrice(c.service?.precio) }}</td>
          <td>
            <span :class="['badge', c.estado]">{{ formatEstado(c.estado) }}</span>
          </td>
        </tr>
      </tbody>
    </table>

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
import api from '@/services/api'

const citas = ref([])
const loading = ref(false)
const error = ref(null)

const searchQuery = ref('')
const statusFilter = ref('')
const selectedCita = ref(null)

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

const formatDate = (str) => {
  if (!str) return '—'
  return new Date(str).toLocaleDateString('es-ES', {
    day: '2-digit',
    month: 'short'
  })
}

const formatTime = (str) => {
  if (!str) return '—'
  return str.slice(0, 5)
}

const formatEstado = (estado) => {
  return estado?.charAt(0).toUpperCase() + estado?.slice(1) || estado
}

const formatPrice = (price) => {
  if (!price && price !== 0) return 'S/. 0.00'
  return `S/. ${parseFloat(price).toFixed(2)}`
}

const openModal = (cita) => {
  selectedCita.value = cita
}

const loadCitas = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await api.get('/citas/')
    citas.value = response.data.results || response.data
  } catch (err) {
    error.value = 'No se pudieron cargar las citas'
    console.error(err)
  } finally {
    loading.value = false
  }
}

onMounted(loadCitas)
</script>

<style scoped>
.page {
  padding: 1.5rem;
  max-width: auto;
  background: #0c0c0c;
  min-height: 100vh;
  color: #ccc;
  font-family: 'Outfit', system-ui, sans-serif;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.page-header h1 {
  font-size: 0.95rem;
  font-weight: 600;
  color: #e8e8e8;
  margin: 0;
}

.btn-refresh {
  padding: 0.35rem 0.75rem;
  background: none;
  border: 1px solid #2a2a2a;
  border-radius: 6px;
  color: #888;
  font-size: 0.8rem;
  font-family: inherit;
  cursor: pointer;
  transition: color 0.15s, border-color 0.15s;
}

.btn-refresh:hover {
  color: #ccc;
  border-color: #444;
}

.btn-refresh:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* Filtros */
.filters {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.input-search {
  flex: 1;
  padding: 0.55rem 0.85rem;
  background: #111;
  border: 1px solid #1a1a1a;
  border-radius: 6px;
  color: #e8e8e8;
  font-size: 0.825rem;
  font-family: inherit;
}

.input-search::placeholder {
  color: #444;
}

.input-search:focus {
  outline: none;
  border-color: #333;
}

.select-filter {
  padding: 0.55rem 0.85rem;
  background: #111;
  border: 1px solid #1a1a1a;
  border-radius: 6px;
  color: #ccc;
  font-size: 0.825rem;
  font-family: inherit;
  cursor: pointer;
}

.select-filter:focus {
  outline: none;
  border-color: #333;
}

/* Tabla */
.empty-state {
  padding: 3rem 1rem;
  text-align: center;
  color: #555;
  font-size: 0.85rem;
}

.empty-state.error {
  color: #b05a5a;
}

.table {
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

.badge.pendiente {
  background: #1a1812;
  color: #b8a44a;
}

.badge.confirmada {
  background: #122218;
  color: #5fa868;
}

.badge.completada {
  background: #121820;
  color: #5a8fbf;
}

.badge.cancelada {
  background: #1a1212;
  color: #b05a5a;
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
</style>