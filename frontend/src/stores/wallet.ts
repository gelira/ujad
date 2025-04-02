import { defineStore } from 'pinia'
import { ref } from 'vue'

import { apiGetTickets } from '@/api/wallet'

export const useWalletStore = defineStore('wallet', () => {
  const tickets = ref<Ticket[]>([])

  async function getTickets(all = false) {
    try {
      const { data } = await apiGetTickets(all)

      tickets.value = data.tickets
    } catch {
      tickets.value = []
    }
  }

  return { tickets, getTickets }
})
