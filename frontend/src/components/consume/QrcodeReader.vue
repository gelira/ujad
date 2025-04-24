<script setup lang="ts">
import { ref, watch } from 'vue'
import { QrcodeStream } from 'vue-qrcode-reader'
import { useConsumeStore } from '@/stores/consume'

const consumeStore = useConsumeStore()

const dialog = ref(true)

function detected(data: { rawValue: string }[]) {
  dialog.value = false

  const value = data[0]?.rawValue

  if (value) {
    consumeStore.getConsumingTokenInfo(value)
  }
}

watch(
  dialog,
  (v) => {
    if (v) {
      consumeStore.clean()
    }
  },
  { immediate: true }
)
</script>

<template>
  <v-dialog
    v-model="dialog"
    transition="dialog-bottom-transition"
    persistent
  >
    <template v-slot:activator="{ props: activatorProps }">
      <v-btn icon="mdi-qrcode" color="primary" v-bind="activatorProps"></v-btn>
    </template>

    <v-card>
      <v-card-title>Ler QRcode</v-card-title>
      <v-card-text class="d-flex">
        <QrcodeStream @detect="detected" />
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="red" @click="dialog = false">
          Cancelar
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>