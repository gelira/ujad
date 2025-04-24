<script setup lang="ts">
import { useConsumeStore } from '@/stores/consume'
import QrcodeReaderDialog from '@/components/consume/QrcodeReaderDialog.vue'
import ConsumeConfirmationDialog from '@/components/consume/ConsumeConfirmationDialog.vue'

const consumeStore = useConsumeStore()
</script>

<template>
  <v-table class="elevation-1 mb-15" v-if="consumeStore.tickets.length > 0">
    <thead>
      <tr>
        <th>Consumidor: {{ consumeStore.name || consumeStore.email }}</th>
      </tr>
    </thead>
    <tbody>
      <tr
        v-for="t in consumeStore.tickets"
        :key="t.uid"
      >
        <td>
          <v-checkbox
            color="primary"
            v-model="consumeStore.ticketIdsSelected"
            :label="t.product_name"
            :value="t.uid"
          ></v-checkbox>
        </td>
      </tr>
    </tbody>
  </v-table>
  <v-sheet
    elevation="4"
    class="position-fixed left-0 right-0 bottom-0 w-100 pl-4 pr-4 pt-2 pb-2 d-flex align-center"
  >
    <QrcodeReaderDialog />
    <v-spacer></v-spacer>
    <ConsumeConfirmationDialog />
  </v-sheet>
</template>

<style scoped>
.v-checkbox :deep(.v-input__details) {
  display: none;
}
</style>
