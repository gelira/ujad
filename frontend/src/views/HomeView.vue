<script setup lang="ts">
import { onMounted } from 'vue'
import { RouterView } from 'vue-router'

import { useNavigation } from '@/composables/navigation'
import { useAuthStore } from '@/stores/auth'
import { removeToken } from '@/utils/localStorage'
import AppBar from '@/components/AppBar.vue'

const authStore = useAuthStore()
const navigation = useNavigation()

onMounted(() => {
  authStore.getUserInfo()
    .then(() => {
      if (authStore.user.role === 'consumer') {
        navigation.goToTickets()
      }
    })
    .catch(() => {
      removeToken()
      navigation.goToLogin()
    })
})
</script>

<template>
  <AppBar />
  <v-container class="mt-16">
    <RouterView />
  </v-container>
</template>
