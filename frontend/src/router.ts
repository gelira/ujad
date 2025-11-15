import { createRouter, createWebHistory } from 'vue-router'

import { useAuthStore } from './stores/auth'
import ConsumeView from './views/ConsumeView.vue'
import HomeView from './views/HomeView.vue'
import LoginView from './views/LoginView.vue'
import MyOrdersView from './views/MyOrdersView.vue'
import NewOrderView from './views/NewOrderView.vue'
import TicketsView from './views/TicketsView.vue'

type RouteKey = 'HOME' | 'LOGIN' | 'TICKETS' | 'NEW_ORDER' | 'CONSUME' | 'MY_ORDERS'

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
  MY_ORDERS: {
    name: 'my-orders',
    label: 'Minhas compras',
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
          meta: { requiredRole: 'consumer' },
        },
        {
          path: 'new-order',
          name: ROUTES.NEW_ORDER.name,
          component: NewOrderView,
          meta: { requiredRole: 'consumer' },
        },
        {
          path: 'my-orders',
          name: ROUTES.MY_ORDERS.name,
          component: MyOrdersView,
          meta: { requiredRole: 'consumer' },
        },
        {
          path: 'consume',
          name: ROUTES.CONSUME.name,
          component: ConsumeView,
          meta: { requiredRole: 'dispatcher' },
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

  if (requiresAuth && (!authStore.user.uid || !authStore.user.role)) {
    return next({ name: ROUTES.LOGIN.name })
  }

  const requiredRole = to.matched.reduce((acc, record) => {
    const role = record.meta.requiredRole as string

    return role || acc
  }, '')

  if (requiredRole && authStore.user.role !== requiredRole) {
    if (requiredRole === 'dispatcher') {
      return next({ name: ROUTES.TICKETS.name })
    }

    return next({ name: ROUTES.CONSUME.name })
  }

  return next()
})

export default router
