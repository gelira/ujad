
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { defineStore } from 'pinia'

import { ROUTES } from '@/router'

export const useNavigationStore = defineStore('navigation', () => {
  const router = useRouter()
  const route = useRoute()

  function navigate(routeName: string) {
    route.name !== routeName && router.push({ name: routeName })
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
  }
})