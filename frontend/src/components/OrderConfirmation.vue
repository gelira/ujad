<script setup lang="ts">
import { computed } from 'vue'
import { useProductStore } from '@/stores/products'
import { useWalletStore } from '@/stores/wallet'
import { formatCurrency } from '@/utils/currency'
import OrderConfirmationDialog from './OrderConfirmationDialog.vue'

const productStore = useProductStore()
const walletStore = useWalletStore()

const orderValue = computed(() => {
  return walletStore.orderItems.reduce<number>((acc, { uid, quantity }) => {
    const productPrice = productStore.products.find((p) => p.uid === uid)?.price ?? 0
    
    return acc + productPrice * quantity
  }, 0)
})
</script>

<template>
  <v-sheet
    elevation="4"
    class="position-fixed left-0 right-0 bottom-0 w-100 pl-4 pr-4 pt-2 pb-2 d-flex justify-space-between align-center"
    v-if="walletStore.orderItems.length > 0"
  >
    <span>Total: {{ formatCurrency(orderValue / 100) }}</span>
    <OrderConfirmationDialog :order-value="orderValue" />
  </v-sheet>
</template>
