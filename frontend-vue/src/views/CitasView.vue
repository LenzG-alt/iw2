<template>
  <div class="container">
    <h1>📅 Citas</h1>
    
    <div v-if="loading" class="loading">Cargando citas...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <button @click="loadCitas" class="btn-refresh">🔄 Actualizar</button>
      
      <table v-if="citas.length > 0" class="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Cliente</th>
            <th>Estilista</th>
            <th>Servicio</th>
            <th>Fecha</th>
            <th>Hora</th>
            <th>Estado</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="c in citas" :key="c.id">
            <td>{{ c.id }}</td>
            <td>{{ c.user?.nombre || c.user_id }}</td>
            <td>{{ c.stylist?.nombre || c.stylist_id }}</td>
            <td>{{ c.service?.nombre || c.service_id }}</td>
            <td>{{ formatDate(c.fecha) }}</td>
            <td>{{ c.hora_inicio }} - {{ c.hora_fin }}</td>
            <td>
              <span :class="['estado', c.estado]">{{ c.estado }}</span>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else class="no-data">No hay citas disponibles</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const citas = ref([])
const loading = ref(false)
const error = ref(null)

const formatDate = (dateStr) => {
  if (!dateStr) return 'N/A'
  const date = new Date(dateStr)
  return date.toLocaleDateString('es-ES')
}

const loadCitas = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await api.get('/citas/')
    citas.value = response.data.results || response.data
  } catch (err) {
    error.value = 'Error al cargar citas: ' + err.message
    console.error(err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadCitas()
})
</script>

<style scoped>
.container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  color: #333;
  border-bottom: 3px solid #ff9800;
  padding-bottom: 10px;
}

.loading, .error, .no-data {
  padding: 20px;
  text-align: center;
  border-radius: 5px;
}

.loading {
  background-color: #e3f2fd;
  color: #1976d2;
}

.error {
  background-color: #ffebee;
  color: #c62828;
}

.no-data {
  background-color: #f5f5f5;
  color: #666;
}

.btn-refresh {
  padding: 10px 20px;
  background-color: #ff9800;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-bottom: 20px;
  font-weight: bold;
}

.btn-refresh:hover {
  background-color: #f57c00;
}

.table {
  width: 100%;
  border-collapse: collapse;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-radius: 5px;
  overflow: hidden;
}

.table thead {
  background-color: #f5f5f5;
  font-weight: bold;
}

.table th, .table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #e0e0e0;
}

.table tbody tr:hover {
  background-color: #fafafa;
}

.estado {
  padding: 4px 8px;
  border-radius: 3px;
  font-weight: bold;
  font-size: 12px;
}

.estado.pendiente {
  background-color: #fff9c4;
  color: #f57f17;
}

.estado.confirmada {
  background-color: #c8e6c9;
  color: #2e7d32;
}

.estado.completada {
  background-color: #bbdefb;
  color: #0d47a1;
}

.estado.cancelada {
  background-color: #ffccbc;
  color: #d84315;
}
</style>
