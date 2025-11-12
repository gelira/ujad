import { createRouter, createWebHistory } from 'vue-router'

import { useAuthStore } from './stores/auth'
import ConsumeView from './views/ConsumeView.vue'
import HomeView from './views/HomeView.vue'
import LoginView from './views/LoginView.vue'
import NewOrderView from './views/NewOrderView.vue'
import TicketsView from './views/TicketsView.vue'

type RouteKey = 'HOME' | 'LOGIN' | 'TICKETS' | 'NEW_ORDER' | 'CONSUME'

interface RouteValue {
  name: string
  label: string
}

export const ROUTES: Record<RouteKey, RouteValue> = {
  HOME: {
    name: 'home',
    label: '',
  },
  LOGIN: {
    name: 'login',
    label: '',
  },
  TICKETS: {
    name: 'tickets',
    label: 'Minhas fichinhas',
  },
  NEW_ORDER: {
    name: 'new-order',
    label: 'Nova compra',
  },
  CONSUME: {
    name: 'consume',
    label: 'Registrar consumo',
  },
}

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: ROUTES.HOME.name,
      component: HomeView,
      meta: { requiresAuth: true },
      children: [
        {
          path: 'tickets',
          name: ROUTES.TICKETS.name,
          component: TicketsView,
        },
        {
          path: 'new-order',
          name: ROUTES.NEW_ORDER.name,
          component: NewOrderView,
        },
        {
          path: 'consume',
          name: ROUTES.CONSUME.name,
          component: ConsumeView,
        },
      ],
    },
    {
      path: '/login',
      name: ROUTES.LOGIN.name,
      component: LoginView,
      beforeEnter() {
        const authStore = useAuthStore()

        if (authStore.user.uid) {
          return { name: ROUTES.HOME.name }
        }
      }
    },
  ],
})

router.beforeEach(async (to, _, next) => {
  const authStore = useAuthStore()

  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth)

  if (requiresAuth && !authStore.user.uid) {
    await authStore.getUserInfo()
  }

  if (requiresAuth && !authStore.user.uid) {
    return next({ name: ROUTES.LOGIN.name })
  }

  next()
})

export default router
