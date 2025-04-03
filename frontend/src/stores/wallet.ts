import { defineStore } from 'pinia'
import { ref } from 'vue'

import { apiGetTickets, apiNewOrder } from '@/api/wallet'

interface OrderItem {
  uid: string
  quantity: number
}

export const useWalletStore = defineStore('wallet', () => {
  const tickets = ref<Ticket[]>([])
  const orderItems = ref<OrderItem[]>([])

  async function getTickets(all = false) {
    try {
      const { data } = await apiGetTickets(all)

      tickets.value = data.tickets
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

  function newOrder() {
    return apiNewOrder(orderItems.value)
  }

  return {
    tickets,
    orderItems,
    getTickets,
    incrementProduct,
    decrementProduct,
    cleanCart,
    newOrder,
  }
})
