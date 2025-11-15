<script setup lang="ts">
import { formatCurrency } from '@/utils/currency';
import { formatDate } from '@/utils/date';
import { computed } from 'vue';
import OrderStatus from '../my-orders/OrderStatus.vue';

const props = defineProps<{
  order: Order
}>()

const consumerName = computed(() => {
  const consumer = props.order.consumer

  return consumer?.name || consumer?.email
})

const originalValue = computed(() => {
  return formatCurrency(props.order.original_value / 100)
})

const createdAt = computed(() => {
  return formatDate(props.order.created_at)
})

const items = computed(() => {
  const tickets = props.order.tickets

  return tickets.reduce<{
    product_uid: string,
    product_name: string,
    price: number,
    quantity: number
  }[]>((acc, ticket) => {
    const index = acc.findIndex((t) => t.product_uid === ticket.product_uid)

    if (index === -1) {
      acc.push({
        product_uid: ticket.product_uid,
        product_name: ticket.product_name,
        price: ticket.product_price,
        quantity: 1
      })
    } else {
      acc[index].quantity++
    }

    return acc
  }, [])
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
      <div class="d-flex flex-column ga-4">
        <p>Data do pedido: {{ createdAt }}</p>
        <p v-if="consumerName">Quem comprou: <strong>{{ consumerName }}</strong></p>
        <p v-if="order.description">Descrição: {{ order.description }}</p>
        <div>
          <p>Itens:</p>
          <v-list>
            <v-list-item
              v-for="item in items"
              :key="item.product_uid"
            >
              <span>{{ item.product_name }}</span>
              <span>{{ item.quantity }} x {{ formatCurrency(item.price / 100) }}</span>
            </v-list-item>
          </v-list>
        </div>
        <p class="d-flex justify-space-between"><span>Valor do pedido:</span><strong>{{ originalValue }}</strong></p>
        <p v-if="order.status !== 'created'">Método de pagamento: {{ order.payment_method }}</p>
      </div>
    </v-card-text>
    <v-card-actions class="justify-end">
      <v-btn
        icon="mdi-share-variant"
      >
      </v-btn>
      <v-spacer></v-spacer>
      <v-btn
        color="primary"
        variant="flat"
      >
        Voltar
      </v-btn>
      <v-btn
        color="success"
        variant="flat"
      >
        Pagar
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<style scoped>
.v-card-text {
  padding-block: 12px 0;
}

.v-list {
  padding-bottom: 0;
}

.v-list-item {
  min-height: 0;
  padding-right: 0 !important;
}

.v-list :deep(.v-list-item__content) {
  display: flex;
  justify-content: space-between
}
</style>