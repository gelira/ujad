import { createRouter, createWebHistory } from 'vue-router'

import HomeView from './views/HomeView.vue'
import LoginView from './views/LoginView.vue'

export const ROUTES = {
  HOME: 'home',
  LOGIN: 'login'
}

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: ROUTES.HOME,
      component: HomeView,
    },
    {
      path: '/login',
      name: ROUTES.LOGIN,
      component: LoginView,
    },
  ],
})

export default router
