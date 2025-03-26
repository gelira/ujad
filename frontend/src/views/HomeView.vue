<script setup lang="ts">
import { onMounted } from 'vue'

import { useNavigation } from '@/composables/navigation'
import { useAuthStore } from '@/stores/auth'
import { removeToken } from '@/utils/localStorage'

const authStore = useAuthStore()
const navigation = useNavigation()

onMounted(() => {
  authStore.getUserInfo().catch(() => {
    removeToken()
    navigation.goToLogin()
  })
})
</script>

<template>
  <v-container>
    <h1>Hello World</h1>
  </v-container>
</template>
