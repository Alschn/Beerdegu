import axiosClient from "./axiosClient";
import {Response} from "./types";

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

interface PasswordChangeData {
  old_password: string,
  new_password1: string,
  new_password2: string
}

interface ResetPasswordData {
  email: string;
}

interface ConfirmPasswordResetData {
  new_password1: string,
  new_password2: string,
  uid: string,
  token: string,
}


interface JWTLoginResponseData {
  access: string,
  refresh: string,
}

interface RegisterResponseData {
  id: number,
  username: string,
}

interface LogoutResponseData {
  message: string;
}

interface PasswordChangeResponseData {
  // todo
}

interface ResetPasswordResponseData {
  // todo
}

interface ConfirmPasswordResetResponseData {
  // todo
}

export const onJWTLogin = (request_body: LoginData): Promise<Response<JWTLoginResponseData>> => {
  return axiosClient.post('/api/auth/token/', {...request_body});
};

export const onRegister = (request_body: RegisterData): Promise<Response<RegisterResponseData>> => {
  return axiosClient.post('/api/auth/register/', {...request_body});
};

export const onLogout = (): Promise<Response<LogoutResponseData>> => {
  return axiosClient.post('/api/auth/logout/', {});
};

export const changePassword = (request_body: PasswordChangeData): Promise<Response<PasswordChangeResponseData>> => {
  return axiosClient.post(`/api/auth/password/change/`, {...request_body});
};

export const resetPassword = (request_body: ResetPasswordData): Promise<Response<ResetPasswordResponseData>> => {
  return axiosClient.post(`/api/auth/password/reset/`, {...request_body});
};

export const confirmResetPassword = (uid: string, token: string, request_body: ConfirmPasswordResetData): Promise<Response<ConfirmPasswordResetResponseData>> => {
  return axiosClient.post(`/api/auth/password/reset/confirm/${uid}/${token}/`, {...request_body});
};

export const confirmRegister = (key: string) => {
  return axiosClient.post(`/api/auth/register/confirm-email/`, {key});
};

export const confirmResendRegisterEmail = () => {
  return axiosClient.post(`/api/auth/register/resend-email/`);
};
