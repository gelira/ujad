<script setup lang="ts">
import { computed } from 'vue'
import { useProductStore } from '@/stores/products'
import { formatCurrency } from '@/utils/currency'

const props = defineProps<{ uid: string, quantity: number }>()

const productStore = useProductStore()

const product = computed(() => {
  return productStore.products.find((p) => p.uid === props.uid)
})
</script>

<template>
  <div class="border-b border-t-0 border-r-0 border-l-0">
    <p>{{ product?.name }}</p>
    <p class="d-flex justify-space-between">
      <span>{{ quantity }}x {{ formatCurrency((product?.price ?? 0) / 100) }} =</span>
      <span>{{ formatCurrency((product?.price ?? 0) * quantity / 100) }}</span>
    </p>
  </div>
</template>