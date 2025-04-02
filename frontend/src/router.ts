import { createRouter, createWebHistory } from 'vue-router'

import HomeView from './views/HomeView.vue'
import LoginView from './views/LoginView.vue'
import TicketsView from './views/TicketsView.vue'

type RouteKey = 'HOME' | 'LOGIN' | 'TICKETS'

interface RouteValue {
  name: string
  label: string
}

export const ROUTES: Record<RouteKey, RouteValue> = {
  HOME: {
    name: 'home',
    label: ''
  },
  LOGIN: {
    name: 'login',
    label: ''
  },
  TICKETS: {
    name: 'tickets',
    label: 'Minhas fichinhas'
  },
}

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: ROUTES.HOME.name,
      component: HomeView,
      children: [
        {
          path: 'tickets',
          name: ROUTES.TICKETS.name,
          component: TicketsView
        }
      ]
    },
    {
      path: '/login',
      name: ROUTES.LOGIN.name,
      component: LoginView,
    },
  ],
})

export default router
