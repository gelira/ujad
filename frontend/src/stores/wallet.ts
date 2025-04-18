import { defineStore } from 'pinia'
import { ref } from 'vue'

import { apiGetTickets, apiNewOrder, apiConsumingToken } from '@/api/wallet'

interface OrderItem {
  uid: string
  quantity: number
}

export const useWalletStore = defineStore('wallet', () => {
  const tickets = ref<Ticket[]>([])
  const orderItems = ref<OrderItem[]>([])
  const consumingToken = ref('')
  const consumingTokenExpireTime = ref(0)

  async function getTickets(all = false) {
    try {
      const { data } = await apiGetTickets(all)

      tickets.value = data.tickets.sort((a, b) => {
        if (!a.consumed && b.consumed) {
          return -1
        }
        if (a.consumed && !b.consumed) {
          return 1
        }
        return a.product_name.localeCompare(b.product_name)
      })
    } catch {
      tickets.value = []
    }
  }

  function updateItemQuantity(productUid: string, toSum: number) {
    const itemExists = orderItems.value.some(({ uid }) => uid === productUid)

    let newList: OrderItem[]

    if (itemExists) {
      newList = orderItems.value.map((i) => {
        if (i.uid === productUid) {
          return { ...i, quantity: i.quantity + toSum }
        }
        return i
      })
    } else {
      newList = [...orderItems.value, { uid: productUid, quantity: 1 }]
    }

    orderItems.value = newList.filter((i) => i.quantity > 0)
  }

  function incrementProduct(productUid: string) {
    updateItemQuantity(productUid, 1)
  }

  function decrementProduct(productUid: string) {
    updateItemQuantity(productUid, -1)
  }

  function cleanCart() {
    orderItems.value = []
  }

  function getConsumingToken() {
    const now = new Date().getTime()

    if (consumingTokenExpireTime.value > now) {
      return
    }

    apiConsumingToken()
      .then(({ data }) => {
        consumingToken.value = data.consuming_token_uid
        consumingTokenExpireTime.value = new Date(data.expired_at).getTime()
      })
      .catch(() => {
        consumingToken.value = ''
        consumingTokenExpireTime.value = 0
      })
  }

  function newOrder() {
    return apiNewOrder(orderItems.value)
  }

  return {
    tickets,
    orderItems,
    consumingToken,
    getTickets,
    incrementProduct,
    decrementProduct,
    cleanCart,
    getConsumingToken,
    newOrder,
  }
})
