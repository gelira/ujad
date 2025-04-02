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
      if (
        authStore.user.role === 'consumer' &&
        navigationStore.activeRoute?.name === ROUTES.HOME.name
      ) {
        navigationStore.goToTickets()
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
