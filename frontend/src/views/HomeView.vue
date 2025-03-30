<script setup lang="ts">
import { onMounted } from 'vue'

import { useNavigation } from '@/composables/navigation'
import { useAuthStore } from '@/stores/auth'
import { removeToken } from '@/utils/localStorage'
import AppBar from '@/components/AppBar.vue'

const authStore = useAuthStore()
const navigation = useNavigation()

onMounted(() => {
  (async () => {
    try {
      await authStore.getUserInfo()
    } catch {
      removeToken()
      navigation.goToLogin()  
    }
  })()
})
</script>

<template>
  <AppBar />
  <v-container>
    <h1>Hello World</h1>
  </v-container>
</template>
