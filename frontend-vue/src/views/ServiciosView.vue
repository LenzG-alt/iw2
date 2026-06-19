<template>
  <div class="container">
    <h1>✂️ Servicios</h1>
    
    <div v-if="loading" class="loading">Cargando servicios...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <button @click="loadServicios" class="btn-refresh">🔄 Actualizar</button>
      
      <table v-if="servicios.length > 0" class="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Nombre</th>
            <th>Descripción</th>
            <th>Precio ($)</th>
            <th>Duración (min)</th>
            <th>Peluquería</th>
            <th>Estado</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="s in servicios" :key="s.id">
            <td>{{ s.id }}</td>
            <td>{{ s.nombre }}</td>
            <td>{{ s.descripcion || 'N/A' }}</td>
            <td>{{ parseFloat(s.precio).toFixed(2) }}</td>
            <td>{{ s.duracion_minutos }}</td>
            <td>{{ s.hair_salon?.nombre || 'N/A' }}</td>
            <td>
              <span :class="['status', s.status]">{{ s.status }}</span>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else class="no-data">No hay servicios disponibles</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const servicios = ref([])
const loading = ref(false)
const error = ref(null)

const loadServicios = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await api.get('/servicios/')
    servicios.value = response.data.results || response.data
  } catch (err) {
    error.value = 'Error al cargar servicios: ' + err.message
    console.error(err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadServicios()
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
  border-bottom: 3px solid #2196f3;
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
  background-color: #2196f3;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-bottom: 20px;
  font-weight: bold;
}

.btn-refresh:hover {
  background-color: #1976d2;
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

.status {
  padding: 4px 8px;
  border-radius: 3px;
  font-weight: bold;
  font-size: 12px;
}

.status.active {
  background-color: #c8e6c9;
  color: #2e7d32;
}

.status.inactive {
  background-color: #ffccbc;
  color: #d84315;
}
</style>
