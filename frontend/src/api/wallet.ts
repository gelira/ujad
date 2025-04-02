import { authApiClient } from './client'

export function apiGetTickets(all = false) {
  return authApiClient().get<{ tickets: Ticket[] }>('/wallet/tickets', {
    params: all ? { all: 'true' } : {}
  })
}