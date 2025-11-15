import { authApiClient } from './client'

export function apiGetTickets(all = false) {
  return authApiClient().get<{ tickets: Ticket[] }>('/api/wallet/tickets', {
    params: all ? { all: 'true' } : {}
  })
}

export function apiNewOrder(products: { uid: string, quantity: number }[]) {
  return authApiClient().post<{ order_uid: string }>('/api/wallet/orders', { products })
}

export function apiConsumingToken() {
  return authApiClient().get<{ consuming_token_uid: string, expired_at: string }>('/api/wallet/consuming-token')
}

export function apiGetConsumingTokenInfo(consuming_token_uid: string) {
  return authApiClient().get<{ name: string, email: string, tickets: Ticket[] }>('/api/wallet/consume', {
    params: { consuming_token_uid }
  })
}

export function apiConsume(consuming_token_uid: string, tickets: string[]) {
  return authApiClient().post<{ tickets: string[] }>('/api/wallet/consume', { tickets }, {
    params: { consuming_token_uid }
  })
}