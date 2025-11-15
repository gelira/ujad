<script setup lang="ts">
import OrderStatus from './OrderStatus.vue';

defineProps<{
  order: ListOrder
}>()
</script>

<template>
  <v-card elevation="2">
    <v-card-title>
      <div class="d-flex justify-space-between">
        <span>
          Pedido <strong>#{{ order.id }}</strong>
        </span>
        <OrderStatus :orderStatus="order.status" />
      </div>
    </v-card-title>
    <v-card-text>
      {{ order.original_value }}
    </v-card-text>
    <v-card-actions class="justify-space-between">
      <v-btn
        icon="mdi-minus"
      ></v-btn>
      <v-btn
        icon="mdi-plus"
      ></v-btn>
    </v-card-actions>
  </v-card>
</template>