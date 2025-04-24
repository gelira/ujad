import { defineStore } from 'pinia'
import { computed, ref, watch } from 'vue'

import { apiGetConsumingTokenInfo } from '@/api/wallet'

const sortTickets = (a: Ticket, b: Ticket) => a.product_name.localeCompare(b.product_name)

export const useConsumeStore = defineStore('consume', () => {
  const consumingToken = ref('')
  const name = ref('')
  const email = ref('')
  const tickets = ref<Ticket[]>([])
  const ticketIdsSelected = ref<string[]>([])

  function getConsumingTokenInfo(token: string) {
    consumingToken.value = token
  }

  function clean() {
    consumingToken.value = ''
    name.value = ''
    email.value = ''
    tickets.value = []
    ticketIdsSelected.value = []
  }

  const ticketsSelected = computed(() => {
    return tickets.value.filter((t) => ticketIdsSelected.value.includes(t.uid))
  })

  watch(
    consumingToken,
    (v) => {
      if (!v) {
        return
      }

      apiGetConsumingTokenInfo(v)
        .then(({ data }) => {
          name.value = data.name
          email.value = data.email
          tickets.value = data.tickets.sort(sortTickets)
        })
        .catch(() => {
          clean()
        })
    }
  )

  return {
    name,
    email,
    tickets,
    ticketIdsSelected,
    ticketsSelected,
    clean,
    getConsumingTokenInfo,
  }
})
