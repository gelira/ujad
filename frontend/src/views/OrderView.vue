<script setup lang="ts">
import { apiGetOrder } from '@/api/order';
import OrderDetail from '@/components/order/OrderDetail.vue';
import { ref, watch } from 'vue';
import { useRoute } from 'vue-router';

const order = ref<Order | null>();

const route = useRoute();

function fetchOrder() {
  const uid = route.params.uid as string

  if (!uid) {
    order.value = null
    return
  }

  apiGetOrder(uid)
    .then((res) => {
      order.value = res.data
    })
    .catch(() => {
      order.value = null
    })
}

watch(
  () => route.params.uid as string,
  () => fetchOrder(),
  { immediate: true }
)
</script>

<template>
  <v-container>
    <OrderDetail
      v-if="order"
      :order="order"
      @refetch="fetchOrder"
    />
  </v-container>
</template>