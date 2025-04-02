<script setup lang="ts">
import { onMounted } from 'vue'
import { RouterView } from 'vue-router'

import { useAuthStore } from '@/stores/auth'
import { useNavigationStore } from '@/stores/navigation'
import { removeToken } from '@/utils/localStorage'
import AppBar from '@/components/AppBar.vue'

const authStore = useAuthStore()
const { goToTickets, goToLogin } = useNavigationStore()

onMounted(() => {
  authStore.getUserInfo()
    .then(() => {
      if (authStore.user.role === 'consumer') {
        goToTickets()
      }
    })
    .catch(() => {
      removeToken()
      goToLogin()
    })
})
</script>

<template>
  <AppBar />
  <v-container class="mt-16">
    <RouterView />
  </v-container>
</template>
