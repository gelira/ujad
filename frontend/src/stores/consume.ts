import { defineStore } from 'pinia'
import { computed, ref, watch } from 'vue'

import { apiGetConsumingTokenInfo, apiConsume } from '@/api/wallet'

const sortTickets = (a: Ticket, b: Ticket) => a.product_name.localeCompare(b.product_name)

export const useConsumeStore = defineStore('consume', () => {
  const consumingToken = ref('')
  const name = ref('')
  const email = ref('')
  const tickets = ref<Ticket[]>([])
  const ticketIdsSelected = ref<string[]>([])

  const ticketsSelected = computed(() => {
    return tickets.value.filter((t) => ticketIdsSelected.value.includes(t.uid))
  })

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

  function consume() {
    return new Promise<void>((resolve, reject) => {
      if (!consumingToken.value || !ticketIdsSelected.value.length) {
        return resolve()
      }

      apiConsume(consumingToken.value, ticketIdsSelected.value)
        .then(() => resolve())
        .catch(() => reject())
    })
  }

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
    consume,
    clean,
    getConsumingTokenInfo,
  }
})
