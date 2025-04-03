<script setup lang="ts">
import { ref } from 'vue'
import { useWalletStore } from '@/stores/wallet'
import ProductOrderResume from './ProductOrderResume.vue'
import { formatCurrency } from '@/utils/currency';

defineProps<{ orderValue: number }>()

const walletStore = useWalletStore()

const dialog = ref(false)
</script>

<template>
  <v-dialog
    v-model="dialog"
    transition="dialog-bottom-transition"
    persistent
  >
    <template v-slot:activator="{ props: activatorProps }">
      <v-btn
        v-bind="activatorProps"
        color="green"
      >
        Confirmar
      </v-btn>
    </template>

    <v-card>
      <v-card-title>Confirmação de compra</v-card-title>
      <v-card-text class="d-flex flex-column ga-3">
        <ProductOrderResume
          v-for="{ uid, quantity } in walletStore.orderItems"
          :key="uid"
          v-bind="{ uid, quantity }"  
        />
        <p class="d-flex justify-space-between">
          <span>Total =</span>
          <span>{{ formatCurrency(orderValue / 100) }}</span>
        </p>
      </v-card-text>
      <template v-slot:actions>
        <v-spacer></v-spacer>

        <v-btn @click="dialog = false">
          Disagree
        </v-btn>

        <v-btn @click="dialog = false">
          Agree
        </v-btn>
      </template>
    </v-card>
  </v-dialog>
</template>