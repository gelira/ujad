import { defineStore } from 'pinia'
import { ref } from 'vue'

import { apiGetProducts } from '@/api/products'

export const useProductStore = defineStore('products', () => {
  const products = ref<Product[]>([])

  async function getProducts() {
    try {
      const { data } = await apiGetProducts()

      products.value = data.products
    } catch {
      products.value = []
    }
  }

  return { products, getProducts }
})
