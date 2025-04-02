<script setup lang="ts">
defineProps<{ product: Product }>()
</script>

<template>
  <v-card elevation="2">
    <v-card-title>{{ product.name }}</v-card-title>
    <v-card-subtitle>{{ product.quantity }} disponíveis</v-card-subtitle>
    <v-card-text v-if="!!product.description">
      {{ product.description }}
    </v-card-text>
    <v-card-actions class="justify-space-between">
      <v-btn icon="mdi-minus"></v-btn>
      <span>0</span>
      <v-btn icon="mdi-plus"></v-btn>
    </v-card-actions>
  </v-card>
</template>