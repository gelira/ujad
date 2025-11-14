<script setup lang="ts">
import { watch } from 'vue';
import { RouterView, useRoute } from 'vue-router';

import AppBar from '@/components/AppBar.vue';
import UserNameDialog from '@/components/UserNameDialog.vue';
import { ROUTES } from '@/router';
import { useAuthStore } from '@/stores/auth';
import { useNavigationStore } from '@/stores/navigation';

const route = useRoute()
const authStore = useAuthStore()
const navigationStore = useNavigationStore()

watch(
  () => [route.name, authStore.user.role],
  ([routeName, role]) => {
    if (routeName !== ROUTES.HOME.name) {
      return
    }

    role === 'consumer'
      ? navigationStore.goToTickets()
      : navigationStore.goToConsume()
  },
  { immediate: true }
)
</script>

<template>
  <AppBar />
  <UserNameDialog />
  <v-container class="mt-16">
    <RouterView />
  </v-container>
</template>
