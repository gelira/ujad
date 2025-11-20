<script setup lang="ts">
import { useAuthStore } from '@/stores/auth';
import { onMounted, ref, watch } from 'vue';

const authStore = useAuthStore()

const name = ref('')

async function save() {
  try {
    await authStore.updateUserName(name.value)
  } catch {
    // do nothing
  } finally {
    authStore.openUserNameDialog = false
  }
}

onMounted(() => {
  if (!authStore.user.name) {
    authStore.openUserNameDialog = true
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
  <v-dialog v-model="authStore.openUserNameDialog" persistent>
    <v-card title="Informe seu nome">
      <v-card-text>
        <v-text-field
          label="Nome"
          variant="outlined"
          v-model="name"
        ></v-text-field>
      </v-card-text>
      <v-card-actions>
        <v-btn color="red" @click="authStore.openUserNameDialog = false">
          Fechar
        </v-btn>
        <v-btn color="success" @click="save">
          Salvar
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>