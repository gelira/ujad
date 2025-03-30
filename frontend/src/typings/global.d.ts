declare global {
  interface User {
    uid: string
    name: string
    email: string
    role: string
  }

  interface Product {
    uid: string
    name: string
    description: string
    price: number
    quantity: number
  }
}

export { }
