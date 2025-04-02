<script setup lang="ts">
import { ref } from 'vue'

import { useAuthStore } from '@/stores/auth'
import { useNavigationStore } from '@/stores/navigation'
import { removeToken } from '@/utils/localStorage'
import { ROUTES } from '@/router'

const authStore = useAuthStore()
const navigationStore = useNavigationStore()

const drawerOpen = ref(false)

function toggle() {
  drawerOpen.value = !drawerOpen.value
}

function logout() {
  removeToken()
  navigationStore.goToLogin()
}
</script>

<template>
  <v-app-bar elevation="2" color="primary">
    <template v-slot:prepend>
      <v-app-bar-nav-icon @click="toggle" />
    </template>
    <v-app-bar-title>{{ navigationStore.activeRoute?.label }}</v-app-bar-title>
  </v-app-bar>
  <v-navigation-drawer v-model="drawerOpen" temporary>
    <v-list>
      <v-list-item>
        {{ authStore.user.name || authStore.user.email }}
      </v-list-item>
      <v-divider></v-divider>
      <template v-if="authStore.user.role === 'consumer'">
        <v-list-item
          append-icon="mdi-ticket"
          @click="navigationStore.goToTickets(); toggle()"
          :active="navigationStore.activeRoute?.name === ROUTES.TICKETS.name"
          active-color="primary"
        >
          {{ ROUTES.TICKETS.label }}
        </v-list-item>
      </template>
      <v-divider></v-divider>
      <v-list-item
        append-icon="mdi-logout"
        class="logout"
        @click="logout"
      >Sair</v-list-item>
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