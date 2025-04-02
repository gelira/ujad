<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'

import { useWalletStore } from '@/stores/wallet'

const walletStore = useWalletStore()

const toggle = ref<'not-consumed' | 'all'>('not-consumed')

watch(
  () => toggle.value,
  (v) => {
    walletStore.getTickets(v === 'all')
  }
)

onMounted(() => {
  walletStore.getTickets()
})
</script>

<template>
  <div class="d-flex justify-center mb-3">
    <v-btn-toggle
      v-model="toggle"
      color="primary"
      mandatory
    >
      <v-btn variant="outlined" value="not-consumed">Disponíveis</v-btn>
      <v-btn variant="outlined" value="all">Todas</v-btn>
    </v-btn-toggle>
  </div>
  <v-table class="elevation-1">
    <tbody>
      <tr
        v-for="t in walletStore.tickets"
        :key="t.uid"
      >
        <td>
          <span :class="{ 'text-decoration-line-through': t.consumed }">{{ t.product_name }}</span>
        </td>
      </tr>
    </tbody>
  </v-table>
</template>
