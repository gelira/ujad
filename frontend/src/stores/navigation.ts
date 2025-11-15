
import { defineStore } from 'pinia'
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { ROUTES } from '@/router'

export const useNavigationStore = defineStore('navigation', () => {
  const router = useRouter()
  const route = useRoute()

  function navigate(routeName: string, params?: Record<string, string>) {
    route.name !== routeName && router.push({ name: routeName, params })
  }

  function goToHome() {
    navigate(ROUTES.HOME.name)
  }

  function goToLogin() {
    navigate(ROUTES.LOGIN.name)
  }

  function goToTickets() {
    navigate(ROUTES.TICKETS.name)
  }

  function goToNewOrder() {
    navigate(ROUTES.NEW_ORDER.name)
  }

  function goToConsume() {
    navigate(ROUTES.CONSUME.name)
  }

  function goToMyOrders() {
    navigate(ROUTES.MY_ORDERS.name)
  }

  function goToOrder(uid: string) {
    navigate(ROUTES.ORDER.name, { uid })
  }

  const activeRoute = computed(() => {
    return Object.values(ROUTES).find((r) => r.name === route.name)
  })

  return {
    activeRoute,
    navigate,
    goToHome,
    goToLogin,
    goToTickets,
    goToNewOrder,
    goToConsume,
    goToOrder,
    goToMyOrders,
  }
})