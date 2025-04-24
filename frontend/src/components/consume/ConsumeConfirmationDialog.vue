<script setup lang="ts">
import { ref } from 'vue'
import { useAlertStore } from '@/stores/alert'
import { useConsumeStore } from '@/stores/consume'

const alertStore = useAlertStore()
const consumeStore = useConsumeStore()

const dialog = ref(false)

function consume() {
  consumeStore.consume()
    .then(() => {
      consumeStore.clean()
      alertStore.showAlert('Consumo registrado com sucesso.')

      dialog.value = false
    })
    .catch(() => {
      alertStore.showAlert('Algo deu errado. Tente novamente.')
    })
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
        :disabled="consumeStore.ticketsSelected.length === 0"
        color="green"
      >
        Confirmar
      </v-btn>
    </template>

    <v-card>
      <v-card-title>Confirmação do consumo</v-card-title>
      <v-card-text>
        <p v-for="t in consumeStore.ticketsSelected">
          {{ t.product_name }}
        </p>
      </v-card-text>
      <v-card-actions>
        <v-btn color="red" @click="dialog = false">
          Cancelar
        </v-btn>

        <v-spacer></v-spacer>

        <v-btn color="green" variant="elevated" @click="consume">
          Confirmar
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>