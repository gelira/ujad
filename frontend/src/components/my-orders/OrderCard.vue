<script setup lang="ts">
import { useNavigationStore } from '@/stores/navigation';
import { formatCurrency } from '@/utils/currency';
import { formatDate } from '@/utils/date';
import { computed } from 'vue';
import OrderStatus from './OrderStatus.vue';

const props = defineProps<{
  order: ListOrder
}>()

const navigationStore = useNavigationStore()

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
        <p>Data do pedido: {{ createdAt }}</p>
        <p>Valor do pedido: <strong>{{ originalValue }}</strong></p>
        <p v-if="order.status !== 'created'">Método de pagamento: <strong>{{ order.payment_method }}</strong></p>
      </div>
    </v-card-text>
    <v-card-actions class="justify-end">
      <v-btn
        icon="mdi-open-in-new"
        @click="navigationStore.goToOrder(order.uid)"
      ></v-btn>
    </v-card-actions>
  </v-card>
</template>

<style scoped>
.v-card-text {
  padding-block: 12px 0;
}
</style>