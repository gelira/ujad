<script setup lang="ts">
import { computed, ref } from 'vue'

import { ROUTES } from '@/router'
import { useAuthStore } from '@/stores/auth'
import { useNavigationStore } from '@/stores/navigation'
import { removeToken } from '@/utils/localStorage'

const authStore = useAuthStore()
const navigationStore = useNavigationStore()

const drawerOpen = ref(false)

const activeRouteName = computed(() => {
  return navigationStore.activeRoute?.name ?? ''
})

function toggle() {
  drawerOpen.value = !drawerOpen.value
}

function logout() {
  removeToken()
  navigationStore.goToLogin()
}

function navigate(routeName: string) {
  navigationStore.navigate(routeName)
  toggle()
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
      <v-list-item
        @click="authStore.openUserNameDialog = true"
      >
        {{ authStore.user.name || authStore.user.email }}
      </v-list-item>

      <v-divider></v-divider>
      
      <v-list-item
        color="primary"
        append-icon="mdi-ticket"
        :active="activeRouteName === ROUTES.TICKETS.name"
        @click="navigate(ROUTES.TICKETS.name)"
      >
        {{ ROUTES.TICKETS.label }}
      </v-list-item>
      <v-list-item
        color="primary"
        append-icon="mdi-cart"
        :active="activeRouteName === ROUTES.NEW_ORDER.name"
        @click="navigate(ROUTES.NEW_ORDER.name)"
      >
        {{ ROUTES.NEW_ORDER.label }}
      </v-list-item>
      <v-list-item
        v-if="authStore.user.role === 'dispatcher'"
        color="primary"
        append-icon="mdi-silverware-fork-knife"
        :active="activeRouteName === ROUTES.CONSUME.name"
        @click="navigate(ROUTES.CONSUME.name)"
      >
        {{ ROUTES.CONSUME.label }}
      </v-list-item>
      
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