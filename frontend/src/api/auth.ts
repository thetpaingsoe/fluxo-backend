import apiClient from './client';

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export async function login(username: string, password: string): Promise<LoginResponse> {
  const resp = await apiClient.post<LoginResponse>('/login', { username, password });
  return resp.data;
}
