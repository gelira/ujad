import { authApiClient } from './client'

export function apiGetProducts() {
  return authApiClient().get<{ products: Product[] }>('/products')
}