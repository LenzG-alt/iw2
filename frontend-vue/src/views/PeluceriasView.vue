<template>
  <div class="page">
    <div class="page-header">
      <h1>Peluquerías</h1>
      <button @click="loadPeluquerias" class="btn-refresh" :disabled="loading">
        Actualizar
      </button>
    </div>

    <div v-if="loading" class="empty-state">Cargando...</div>
    <div v-else-if="error" class="empty-state error">{{ error }}</div>
    <div v-else-if="peluquerias.length === 0" class="empty-state">Sin resultados</div>
    <table v-else class="table">
      <thead>
        <tr>
          <th>Nombre</th>
          <th>Dirección</th>
          <th>Teléfono</th>
          <th>Descripción</th>
          <th>Estado</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="p in peluquerias" :key="p.id">
          <td class="strong">{{ p.nombre }}</td>
          <td>{{ p.direccion || '—' }}</td>
          <td class="mono">{{ p.telefono || '—' }}</td>
          <td class="muted">{{ p.descripcion || '—' }}</td>
          <td>
            <span :class="['badge', p.status]">
              {{ p.status === 'A' ? 'Activa' : 'Inactiva' }}
            </span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const peluquerias = ref([])
const loading = ref(false)
const error = ref(null)

const loadPeluquerias = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await api.get('/peluquerias/')
    peluquerias.value = response.data.results || response.data
  } catch (err) {
    error.value = 'No se pudieron cargar las peluquerías'
    console.error(err)
  } finally {
    loading.value = false
  }
}

onMounted(loadPeluquerias)
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

.empty-state {
  padding: 3rem 1rem;
  text-align: center;
  color: #666;
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
  color: #777;
  font-weight: 500;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  border-bottom: 1px solid #222;
}

tbody td {
  padding: 0.65rem 0.75rem;
  border-bottom: 1px solid #181818;
  color: #bbb;
}

tbody tr:last-child td {
  border-bottom: none;
}

.strong {
  color: #e8e8e8;
  font-weight: 500;
}

.muted {
  color: #666;
  max-width: 220px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.mono {
  font-variant-numeric: tabular-nums;
}

.badge {
  display: inline-block;
  padding: 0.15rem 0.55rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
}

.badge.active {
  background: #122218;
  color: #5fa868;
}

.badge.inactive {
  background: #1a1212;
  color: #b05a5a;
}
</style>