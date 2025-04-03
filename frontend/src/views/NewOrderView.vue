<script setup lang="ts">
import { onMounted } from 'vue'

import { useProductStore } from '@/stores/products'
import ProductCard from '@/components/ProductCard.vue'
import OrderConfirmation from '@/components/OrderConfirmation.vue'

const productStore = useProductStore()

onMounted(() => {
  productStore.getProducts()
})
</script>

<template>
  <div class="d-flex flex-column ga-2 mb-15">
    <ProductCard v-for="p in productStore.products" :key="p.uid" :product="p" />
  </div>
  <OrderConfirmation />
</template>
