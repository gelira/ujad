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

  type OrderStatus = 'created' | 'pending' | 'canceled' | 'confirmed'

  interface ListOrder {
    id: number
    uid: string
    status: OrderStatus
    description: string
    payment_method: string
    original_value: number
    remaining_value: number
    created_at: string
  }

  interface OrderTicket {
    product_uid: string
    product_name: string
    product_price: number
  }

  interface Order extends ListOrder {
    tickets: OrderTicket[]
    consumer?: {
      name: string
      email: string
    }
  }
}

export { }
