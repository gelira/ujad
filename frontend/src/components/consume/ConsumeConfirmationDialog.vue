<script setup lang="ts">
import { ref } from 'vue'
import { useConsumeStore } from '@/stores/consume'

const consumeStore = useConsumeStore()

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

        <v-btn color="green" variant="elevated">
          Confirmar
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>