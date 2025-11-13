<script setup lang="ts">
import { RouterView } from 'vue-router';

import AppBar from '@/components/AppBar.vue';
import UserNameDialog from '@/components/UserNameDialog.vue';
</script>

<template>
  <AppBar />
  <UserNameDialog />
  <v-container class="mt-16">
    <RouterView />
  </v-container>
</template>
