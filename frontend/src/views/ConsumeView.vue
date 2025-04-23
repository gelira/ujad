<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useConsumeStore } from '@/stores/consume'

const ticketsSelected = ref<string[]>([])

const consumeStore = useConsumeStore()

onMounted(() => {
  consumeStore.getConsumingTokenInfo('27c196fc-b463-40d7-8d11-2e2ae382b5fb')
})
</script>

<template>
  <div class="d-flex justify-space-between mb-3">
  </div>
  <v-table class="elevation-1">
    <tbody>
      <tr
        v-for="t in consumeStore.tickets"
        :key="t.uid"
      >
        <td>
          <v-checkbox
            v-model="ticketsSelected"
            color="primary"
            :label="t.product_name"
            :value="t.uid"
          ></v-checkbox>
        </td>
      </tr>
    </tbody>
  </v-table>
</template>

<style scoped>
.v-checkbox :deep(.v-input__details) {
  display: none;
}
</style>
