import { authApiClient } from './client'

export function apiGetTickets(all = false) {
  return authApiClient().get<{ tickets: Ticket[] }>('/wallet/tickets', {
    params: all ? { all: 'true' } : {}
  })
}

export function apiNewOrder(products: { uid: string, quantity: number }[]) {
  return authApiClient().post('/wallet/orders', { products })
}