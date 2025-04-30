import { authApiClient, noAuthApiClient } from './client'

export function apiGenerateAuthCode({ email }: { email: string }) {
  return noAuthApiClient().post<{ auth_code_uid: string }>('/api/auth-code', { email })
}

export function apiVerifyAuthCode({ auth_code_uid, code }: { auth_code_uid: string, code: string }) {
  return noAuthApiClient().post<{ token: string}>('/api/auth-code/verify', { auth_code_uid, code })
}

export function apiGetUserInfo() {
  return authApiClient().get<User>('/api/user/info')
}