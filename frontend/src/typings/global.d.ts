declare global {
  interface User {
    uid: string
    name: string
    email: string
    role: 'consumer' | 'dispatcher' | ''
  }

  interface Product {
    uid: string
    name: string
    description: string
    price: number
    quantity: number
  }

  interface Ticket {
    uid: string
    product_name: string
    product_price: number
    consumed: boolean
  }
}

export { }
