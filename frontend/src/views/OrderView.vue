<script setup lang="ts">
import { apiGetOrder } from '@/api/order';
import OrderDetail from '@/components/order/OrderDetail.vue';
import { ref, watch } from 'vue';
import { useRoute } from 'vue-router';

const order = ref<Order | null>();

const route = useRoute();

watch(
  () => route.params.uid as string,
  (uid) => {
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
  },
  { immediate: true }
)
</script>

<template>
  <v-container>
    <OrderDetail
      v-if="order"
      :order="order"
    />
  </v-container>
</template>