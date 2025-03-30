<script setup lang="ts">
import { onMounted } from 'vue'

import { useNavigation } from '@/composables/navigation'
import { useAuthStore } from '@/stores/auth'
import { useProductStore } from '@/stores/products'
import { removeToken } from '@/utils/localStorage'
import AppBar from '@/components/AppBar.vue'

const authStore = useAuthStore()
const productStore = useProductStore()
const navigation = useNavigation()

onMounted(() => {
  authStore.getUserInfo()
    .then(() => productStore.getProducts())
    .catch(() => {
      removeToken()
      navigation.goToLogin()
    })
})
</script>

<template>
  <AppBar />
  <v-container>
    <h1>Hello World</h1>
  </v-container>
</template>
