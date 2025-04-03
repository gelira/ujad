<script setup lang="ts">
import { ref } from 'vue'
import { useWalletStore } from '@/stores/wallet'
import { useAlertStore } from '@/stores/alert'
import ProductOrderResume from './ProductOrderResume.vue'
import { formatCurrency } from '@/utils/currency'

defineProps<{ orderValue: number }>()

const alertStore = useAlertStore()
const walletStore = useWalletStore()

const dialog = ref(false)

function confirmNewOrder() {
  walletStore.newOrder()
    .then(() => {
      dialog.value = false
      walletStore.cleanCart()
      alertStore.showAlert('Suas fichinhas estarão disponíveis assim que o pagamento for confirmado', 10000)
    })
    .catch(() => {})
}
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
        <ProductOrderResume v-for="i in walletStore.orderItems" :key="i.uid" v-bind="i" />
        <p class="d-flex justify-space-between">
          <span>Total =</span>
          <span>{{ formatCurrency(orderValue / 100) }}</span>
        </p>
      </v-card-text>
      <v-card-actions>
        <v-btn color="red" @click="dialog = false">
          Cancelar
        </v-btn>

        <v-spacer></v-spacer>

        <v-btn color="green" variant="elevated" @click="confirmNewOrder">
          Confirmar
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>