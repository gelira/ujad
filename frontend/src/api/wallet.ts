import { authApiClient } from './client'

export function apiGetTickets(all = false) {
  return authApiClient().get<{ tickets: Ticket[] }>('/wallet/tickets', {
    params: all ? { all: 'true' } : {}
  })
}

export function apiNewOrder(products: { uid: string, quantity: number }[]) {
  return authApiClient().post('/wallet/orders', { products })
}

export function apiConsumingToken() {
  return authApiClient().get<{ consuming_token_uid: string, expired_at: string }>('/wallet/consuming-token')
}