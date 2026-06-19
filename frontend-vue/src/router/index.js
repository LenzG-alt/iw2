import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import LoginView from '@/views/LoginView.vue'
import DashboardView from '@/views/DashboardView.vue'
import PeluceriasView from '@/views/PeluceriasView.vue'
import UsuariosView from '@/views/UsuariosView.vue'
import EstilistasView from '@/views/EstilistasView.vue'
import ServiciosView from '@/views/ServiciosView.vue'
import CitasView from '@/views/CitasView.vue'
import HorariosView from '@/views/HorariosView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { requiresGuest: true }
    },
    {
      path: '/',
      name: 'dashboard',
      component: DashboardView,
      meta: { requiresAuth: false }  // Sin autenticación en desarrollo
    },
    {
      path: '/peluquerias',
      name: 'peluquerias',
      component: PeluceriasView,
      meta: { requiresAuth: false }
    },
    {
      path: '/usuarios',
      name: 'usuarios',
      component: UsuariosView,
      meta: { requiresAuth: false }
    },
    {
      path: '/estilistas',
      name: 'estilistas',
      component: EstilistasView,
      meta: { requiresAuth: false }
    },
    {
      path: '/servicios',
      name: 'servicios',
      component: ServiciosView,
      meta: { requiresAuth: false }
    },
    {
      path: '/citas',
      name: 'citas',
      component: CitasView,
      meta: { requiresAuth: false }
    },
    {
      path: '/horarios',
      name: 'horarios',
      component: HorariosView,
      meta: { requiresAuth: false }
    }
  ]
})

// Navigation Guard
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next('/') // Si ya está logueado, no mostrar login
  } else {
    next()
  }
})

export default router