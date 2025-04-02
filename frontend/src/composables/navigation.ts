import { useRouter, useRoute } from 'vue-router'

import { ROUTES } from '@/router'

export function useNavigation() {
  const router = useRouter()
  const route = useRoute()

  function goToHome() {
    route.name !== ROUTES.HOME && router.push({ name: ROUTES.HOME })
  }

  function goToLogin() {
    route.name !== ROUTES.LOGIN && router.push({ name: ROUTES.LOGIN })
  }

  function goToTickets() {
    route.name !== ROUTES.TICKETS && router.push({ name: ROUTES.TICKETS })
  }

  return {
    goToHome,
    goToLogin,
    goToTickets,
  }
}
