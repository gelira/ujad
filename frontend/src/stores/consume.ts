import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

import { apiGetConsumingTokenInfo } from '@/api/wallet'

export const useConsumeStore = defineStore('consume', () => {
  const consumingToken = ref('')
  const name = ref('')
  const email = ref('')
  const tickets = ref<Ticket[]>([])

  function getConsumingTokenInfo(token: string) {
    consumingToken.value = token
  }

  function clean() {
    name.value = ''
    email.value = ''
    tickets.value = []
  }

  watch(
    consumingToken,
    (v) => {
      if (!v) {
        return clean()
      }

      apiGetConsumingTokenInfo(v)
        .then(({ data }) => {
          name.value = data.name
          email.value = data.email
          tickets.value = data.tickets.sort((a, b) => a.product_name.localeCompare(b.product_name))
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
    getConsumingTokenInfo,
  }
})
