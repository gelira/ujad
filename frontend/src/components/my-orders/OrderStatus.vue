<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  orderStatus: OrderStatus
}>()

const chipProps = computed(() => {
  if (props.orderStatus === 'created') {
    return {
      icon: 'mdi-invoice-send',
      text: 'Pedido criado',
      color: undefined
    }
  }

  if (props.orderStatus === 'pending') {
    return {
      icon: 'mdi-clock',
      text: 'Pagamento pendente',
      color: 'warning'
    }
  }

  if (props.orderStatus === 'confirmed') {
    return {
      icon: 'mdi-check-circle',
      text: 'Pedido confirmado',
      color: 'success'
    }
  }

  return {
    icon: 'mdi-close-circle',
    text: 'Pedido cancelado',
    color: 'error'
  }
})
</script>

<template>
  <v-chip
    :color="chipProps.color"
    :prepend-icon="chipProps.icon"
  >
    {{ chipProps.text }}
  </v-chip>
</template>