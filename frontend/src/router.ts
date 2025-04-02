import { createRouter, createWebHistory } from 'vue-router'

import HomeView from './views/HomeView.vue'
import LoginView from './views/LoginView.vue'
import TicketsView from './views/TicketsView.vue'

export const ROUTES = {
  HOME: 'home',
  LOGIN: 'login',
  TICKETS: 'tickets',
}

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: ROUTES.HOME,
      component: HomeView,
      children: [
        {
          path: 'tickets',
          name: ROUTES.TICKETS,
          component: TicketsView
        }
      ]
    },
    {
      path: '/login',
      name: ROUTES.LOGIN,
      component: LoginView,
    },
  ],
})

export default router
