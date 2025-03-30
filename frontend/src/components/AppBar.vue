<script setup lang="ts">
import { reactive } from 'vue'

import { useNavigation } from '@/composables/navigation'
import { useAuthStore } from '@/stores/auth'
import { removeToken } from '@/utils/localStorage'

const authStore = useAuthStore()
const navigation = useNavigation()

const state = reactive({
  drawerOpen: false
})

function toggle() {
  state.drawerOpen = !state.drawerOpen
}

function logout() {
  removeToken()
  navigation.goToLogin()
}
</script>

<template>
  <v-app-bar elevation="2" color="primary">
    <template v-slot:prepend>
      <v-app-bar-nav-icon @click="toggle" />
    </template>
    <v-app-bar-title>UJAD</v-app-bar-title>
  </v-app-bar>
  <v-navigation-drawer
    v-model="state.drawerOpen"
    temporary
  >
    <v-list>
      <v-list-item>
        {{ authStore.user.name || authStore.user.email }}
      </v-list-item>
      <v-divider />
      <v-list-item
        title="Sair"
        append-icon="mdi-logout"
        class="logout"
        @click="logout"
      />
    </v-list>
  </v-navigation-drawer>
</template>

<style scoped>
.v-list {
  height: calc(100dvh - 64px);
}

.logout {
  color: red;
}
</style>