<script setup lang="ts">
import { RouterView } from 'vue-router';

import Alert from './components/Alert.vue';
</script>

<template>
  <v-layout>
    <RouterView />
    <Alert />
  </v-layout>
</template>
