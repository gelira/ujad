import { defineStore } from 'pinia'
import { reactive, ref } from 'vue'

import { apiGenerateAuthCode, apiGetUserInfo, apiPatchUserInfo, apiVerifyAuthCode } from '@/api/auth'
import { setToken } from '@/utils/localStorage'

export const useAuthStore = defineStore('auth', () => {
  const authCodeUid = ref('')
  const openUserNameDialog = ref(false)
  const user = reactive<User>({
    uid: '',
    name: '',
    email: '',
    role: ''
  })

  async function generateAuthCode({ email }: { email: string }) {
    const { data } = await apiGenerateAuthCode({ email })
    
    authCodeUid.value = data.auth_code_uid
  }

  async function verifyAuthCode({ code }: { code: string }) {
    if (!authCodeUid.value) {
      throw new Error('it needs generate a auth code first')
    }

    const { data } = await apiVerifyAuthCode({ auth_code_uid: authCodeUid.value, code })
    
    setToken(data.token)
  }

  async function getUserInfo() {
    try {
      const { data } = await apiGetUserInfo()
  
      user.uid = data.uid
      user.name = data.name
      user.email = data.email
      user.role = data.role
    } catch {
      user.uid = ''
      user.name = ''
      user.email = ''
      user.role = ''
    }
  }

  async function updateUserName(name: string) {
    await apiPatchUserInfo({ name })

    user.name = name
  }

  return {
    user,
    openUserNameDialog,
    generateAuthCode,
    verifyAuthCode,
    getUserInfo,
    updateUserName,
  }
})
