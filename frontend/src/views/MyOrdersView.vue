<script setup lang="ts">
import { apiListOrders } from '@/api/order'
import OrderCard from '@/components/my-orders/OrderCard.vue'
import { onMounted, ref } from 'vue'

const orders = ref<ListOrder[]>([])

onMounted(() => {
  apiListOrders()
    .then((res) => {
      orders.value = res.data.orders
    })
    .catch(() => {
      orders.value = []
    })
})
</script>

<template>
  <OrderCard
    v-for="order in orders"
    :key="order.id"
    :order="order"
  />
</template>