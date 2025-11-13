<script setup lang="ts">
import { RouterView } from 'vue-router';

import AppBar from '@/components/AppBar.vue';
</script>

<template>
  <AppBar />
  <v-container class="mt-16">
    <RouterView />
  </v-container>
</template>
