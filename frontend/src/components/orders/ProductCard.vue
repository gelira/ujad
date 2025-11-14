<script setup lang="ts">
import { useWalletStore } from '@/stores/wallet';
import { computed } from 'vue';

const props = defineProps<{ product: Product }>()

const walletStore = useWalletStore()

const orderItem = computed(() => {
  return walletStore.orderItems.find(
    (i) => i.uid === props.product.uid
  ) ?? { uid: '', quantity: 0 }
})

const price = computed(() => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  }).format(props.product.price / 100)
})
</script>

<template>
  <v-card elevation="2">
    <v-card-title>
      <div class="d-flex justify-space-between">
        <span>{{ product.name }}</span>
        <span>{{ price }}</span>
      </div>
    </v-card-title>
    <v-card-subtitle>{{ product.quantity }} disponíveis</v-card-subtitle>
    <v-card-text v-if="!!product.description">
      {{ product.description }}
    </v-card-text>
    <v-card-actions class="justify-space-between">
      <v-btn
        icon="mdi-minus"
        :disabled="orderItem.quantity <= 0"
        @click="walletStore.decrementProduct(product.uid)"
      ></v-btn>
      <span>{{ orderItem?.quantity ?? 0 }}</span>
      <v-btn
        icon="mdi-plus"
        :disabled="product.quantity <= orderItem.quantity"
        @click="walletStore.incrementProduct(product.uid)"
      ></v-btn>
    </v-card-actions>
  </v-card>
</template>