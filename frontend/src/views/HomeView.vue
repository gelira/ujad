<script setup lang="ts">
import { onMounted } from 'vue'
import { RouterView } from 'vue-router'

import { useAuthStore } from '@/stores/auth'
import { useNavigationStore } from '@/stores/navigation'
import { removeToken } from '@/utils/localStorage'
import AppBar from '@/components/AppBar.vue'
import { ROUTES } from '@/router'

const authStore = useAuthStore()
const navigationStore = useNavigationStore()

onMounted(() => {
  authStore.getUserInfo()
    .then(() => {
      const routeName = navigationStore.activeRoute?.name

      if (
        routeName === ROUTES.HOME.name ||
        routeName === ROUTES.CONSUME.name
      ) {
        authStore.user.role === 'consumer'
          ? navigationStore.goToTickets()
          : navigationStore.goToConsume()
      }
    })
    .catch(() => {
      removeToken()
      navigationStore.goToLogin()
    })
})
</script>

<template>
  <AppBar />
  <v-container class="mt-16">
    <RouterView />
  </v-container>
</template>
