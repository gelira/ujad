import { authApiClient, noAuthApiClient } from './client'

export function apiListOrders() {
  return authApiClient().get<{ orders: ListOrder[] }>('/api/orders')
}

export function apiGetOrder(uid: string) {
  return noAuthApiClient().get<Order>(`/api/orders/${uid}`)
}

export function apiPostOrderPayment(uid: string) {
  return noAuthApiClient().post(`/api/orders/${uid}/payment`)
}