<script setup lang="ts">
import { onMounted, onBeforeUnmount } from 'vue'

import { useProductStore } from '@/stores/products'
import { useWalletStore } from '@/stores/wallet'
import ProductCard from '@/components/orders/ProductCard.vue'
import OrderConfirmation from '@/components/orders/OrderConfirmation.vue'

const productStore = useProductStore()
const walletStore = useWalletStore()

onMounted(() => {
  productStore.getProducts()
})

onBeforeUnmount(() => {
  walletStore.cleanCart()
})
</script>

<template>
  <div class="d-flex flex-column ga-2 mb-15">
    <ProductCard v-for="p in productStore.products" :key="p.uid" :product="p" />
  </div>
  <OrderConfirmation />
</template>
