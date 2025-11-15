<script setup lang="ts">
import { formatCurrency } from '@/utils/currency';
import { formatDate } from '@/utils/date';
import { computed } from 'vue';
import OrderStatus from '../my-orders/OrderStatus.vue';

const props = defineProps<{
  order: Order
}>()

const originalValue = computed(() => {
  return formatCurrency(props.order.original_value / 100)
})

const createdAt = computed(() => {
  return formatDate(props.order.created_at)
})
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
      <div class="d-flex flex-column ga-2">
        <p>Valor do pedido: {{ originalValue }}</p>
        <p>Data do pedido: {{ createdAt }}</p>
        <p v-if="order.status !== 'created'">Método de pagamento: {{ order.payment_method }}</p>
      </div>
    </v-card-text>
    <v-card-actions class="justify-end">
      <v-btn
        icon="mdi-open-in-new"
      ></v-btn>
    </v-card-actions>
  </v-card>
</template>

<style scoped>

</style>