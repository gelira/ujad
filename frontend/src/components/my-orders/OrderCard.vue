<script setup lang="ts">
import { formatCurrency } from '@/utils/currency';
import { computed } from 'vue';
import OrderStatus from './OrderStatus.vue';

const props = defineProps<{
  order: ListOrder
}>()

const originalValue = computed(() => {
  return formatCurrency(props.order.original_value / 100)
})

const createdAt = computed(() => {
  const dt = new Date(props.order.created_at)
  
  const date = dt.toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  })

  const time = dt.toLocaleTimeString('pt-BR', {
    hour: '2-digit',
    minute: '2-digit'
  })

  return `${date} às ${time}`
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
      <p>Valor do pedido: {{ originalValue }}</p>
      <p>Data do pedido: {{ createdAt }}</p>
      <p v-if="order.status !== 'created'">Método de pagamento: {{ order.payment_method }}</p>
    </v-card-text>
    <v-card-actions class="justify-end">
      <v-btn
        icon="mdi-open-in-new"
      ></v-btn>
    </v-card-actions>
  </v-card>
</template>