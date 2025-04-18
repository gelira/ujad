<script setup lang="ts">
import { ref } from 'vue'
import VueQrcode from '@chenfengyuan/vue-qrcode'
import { useWalletStore } from '@/stores/wallet'

const open = ref(false)
const walletStore = useWalletStore()

function openDialog() {
  walletStore.getConsumingToken()
  open.value = true
}
</script>

<template>
  <v-btn
    icon="mdi-qrcode"
    color="green"
    @click="openDialog"
  ></v-btn>
  <v-dialog v-model="open">
    <v-card>
      <v-card-text>
        <p>Mostre este QRcode para o atendente:</p>
        <div class="d-flex justify-space-around">
          <v-skeleton-loader v-if="!walletStore.consumingToken" height="180" width="180"></v-skeleton-loader>
          <VueQrcode v-else :value="walletStore.consumingToken" :options="{ width: 180 }" />
        </div>
      </v-card-text>
      <v-card-actions>
        <v-btn color="red" @click="open = false">
          Fechar
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>