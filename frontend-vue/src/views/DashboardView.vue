<template>
  <div class="dashboard-container">
    <header class="top-bar glass-panel">
      <div class="brand">
        <h1>SGCP</h1>
      </div>
      <div class="user-actions">
        <button @click="handleLogout" class="btn-logout">Cerrar Sesion</button>
      </div>
    </header>

    <nav class="navigation">
      <router-link to="/" class="nav-item active">Dashboard</router-link>
      <router-link to="/peluquerias" class="nav-item">Peluquerias</router-link>
      <router-link to="/usuarios" class="nav-item">Usuarios</router-link>
      <router-link to="/estilistas" class="nav-item">Estilistas</router-link>
      <router-link to="/servicios" class="nav-item">Servicios</router-link>
      <router-link to="/citas" class="nav-item">Citas</router-link>
      <router-link to="/horarios" class="nav-item">Horarios</router-link>
    </nav>

    <main class="main-content">
      <section class="stats-grid">
        <div class="stat-card glass-panel">
          <h3>Total Citas</h3>
          <div class="stat-value">{{ estadisticas.totalCitas }}</div>
        </div>
        <div class="stat-card glass-panel">
          <h3>Estilistas</h3>
          <div class="stat-value">{{ estadisticas.totalEstilistas }}</div>
        </div>
        <div class="stat-card glass-panel">
          <h3>Usuarios</h3>
          <div class="stat-value">{{ estadisticas.totalUsuarios }}</div>
        </div>
        <div class="stat-card glass-panel">
          <h3>Servicios</h3>
          <div class="stat-value">{{ estadisticas.totalServicios }}</div>
        </div>
      </section>

      <section class="recent-section glass-panel" v-if="ultimasCitas.length > 0">
        <h2>Ultimas Citas</h2>
        <table class="recent-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Cliente</th>
              <th>Estilista</th>
              <th>Fecha</th>
              <th>Estado</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="cita in ultimasCitas.slice(0, 5)" :key="cita.id">
              <td>#{{ cita.id }}</td>
              <td>{{ cita.user?.nombre || 'N/A' }}</td>
              <td>{{ cita.stylist?.nombre || 'N/A' }}</td>
              <td>{{ formatDate(cita.fecha) }}</td>
              <td><span :class="['status-badge', cita.estado]">{{ cita.estado }}</span></td>
            </tr>
          </tbody>
        </table>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'

const authStore = useAuthStore()
const estadisticas = ref({
  totalCitas: 0,
  totalEstilistas: 0,
  totalUsuarios: 0,
  totalServicios: 0
})
const ultimasCitas = ref([])

const formatDate = (dateStr) => {
  if (!dateStr) return 'N/A'
  const date = new Date(dateStr)
  return date.toLocaleDateString('es-ES')
}

const handleLogout = () => {
  authStore.logout()
  window.location.href = '/login'
}

const cargarEstadisticas = async () => {
  try {
    const [peluquerias, usuarios, estilistas, servicios, citas] = await Promise.all([
      api.get('/peluquerias/').catch(() => ({ data: [] })),
      api.get('/usuarios/').catch(() => ({ data: [] })),
      api.get('/estilistas/').catch(() => ({ data: [] })),
      api.get('/servicios/').catch(() => ({ data: [] })),
      api.get('/citas/').catch(() => ({ data: [] }))
    ])

    estadisticas.value = {
      totalCitas: citas.data.length,
      totalEstilistas: estilistas.data.length,
      totalUsuarios: usuarios.data.length,
      totalServicios: servicios.data.length
    }

    ultimasCitas.value = citas.data
  } catch (err) {
    console.error('Error cargando estadisticas:', err)
  }
}

onMounted(() => {
  cargarEstadisticas()
})
</script>

<style scoped>
* {
  box-sizing: border-box;
}

.dashboard-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
  overflow-x: hidden;
}

.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 30px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  margin: 10px;
  border-radius: 10px;
}

.brand {
  color: white;
  font-weight: bold;
}

.brand h1 {
  margin: 0;
  font-size: 24px;
}

.user-actions {
  display: flex;
  gap: 15px;
}

.btn-logout {
  padding: 10px 20px;
  background-color: #ff6b6b;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s;
}

.btn-logout:hover {
  background-color: #ff5252;
}

.navigation {
  display: flex;
  gap: 10px;
  padding: 20px 30px;
  flex-wrap: wrap;
  position: relative;
  z-index: 10;
}

.nav-item {
  padding: 10px 20px;
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
  text-decoration: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.nav-item:hover,
.nav-item.active {
  background-color: rgba(255, 255, 255, 0.4);
}

.main-content {
  padding: 20px 30px;
  position: relative;
  z-index: 10;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 20px;
  border-radius: 10px;
  color: white;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.stat-card h3 {
  margin: 0 0 10px 0;
  font-size: 14px;
  opacity: 0.9;
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
}

.recent-section {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  padding: 30px;
  color: white;
  margin-bottom: 30px;
}

.recent-section h2 {
  margin-top: 0;
}

.recent-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 15px;
}

.recent-table thead {
  background-color: rgba(255, 255, 255, 0.1);
}

.recent-table th,
.recent-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.status-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: bold;
}

.status-badge.confirmada {
  background-color: #c8e6c9;
  color: #2e7d32;
}

.status-badge.pendiente {
  background-color: #fff9c4;
  color: #f57f17;
}

.status-badge.completada {
  background-color: #bbdefb;
  color: #0d47a1;
}

.status-badge.cancelada {
  background-color: #ffccbc;
  color: #d84315;
}

.glass-panel {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}
</style>
