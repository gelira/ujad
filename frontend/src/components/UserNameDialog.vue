<script setup lang="ts">
import { useAuthStore } from '@/stores/auth';
import { onMounted, ref, watch } from 'vue';

const authStore = useAuthStore()

const open = ref(false)
const name = ref('')

async function save() {
  try {
    await authStore.updateUserName(name.value)
  } catch {
    // do nothing
  } finally {
    open.value = false
  }
}

onMounted(() => {
  if (!authStore.user.name) {
    open.value = true
  }
})

watch(
  () => authStore.user.name,
  (value) => {
    name.value = value
  },
  { immediate: true }
)
</script>

<template>
  <v-dialog v-model="open" persistent>
    <v-card title="Informe seu nome">
      <v-card-text>
        <v-text-field
          label="Nome"
          variant="outlined"
          v-model="name"
        ></v-text-field>
      </v-card-text>
      <v-card-actions>
        <v-btn color="red" @click="open = false">
          Fechar
        </v-btn>
        <v-btn color="success" @click="save">
          Salvar
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>