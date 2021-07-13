import axiosClient from "./axiosClient"

interface LoginData {
  username: string,
  password: string,
}

interface RegisterData {
  username: string,
  email: string,
  password1: string,
  password2: string,
}

export const onLogin = (request_body: LoginData): Promise<any> => {
  return axiosClient.post('/auth/login/', {...request_body});
};

export const onRegister = (request_body: RegisterData): Promise<any> => {
  return axiosClient.post('/auth/register/', {...request_body});
};

export const onLogout = (): Promise<any> => {
  return axiosClient.post('/auth/logout/', {});
};
