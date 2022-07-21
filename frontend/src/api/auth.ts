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

export const onLogin = (request_body: LoginData): Promise<Response<any>> => {
  return axiosClient.post('/auth/login/', {...request_body});
};


export const onRegister = (request_body: RegisterData): Promise<Response<any>> => {
  return axiosClient.post('/auth/register/', {...request_body});
};

export const onLogout = (): Promise<Response<any>> => {
  return axiosClient.post('/auth/logout/', {});
};

export const changePassword = (request_body: PasswordChangeData): Promise<Response<any>> => {
  return axiosClient.post(`/auth/password/change/`, {...request_body});
};

export const resetPassword = (request_body: ResetPasswordData): Promise<Response<any>> => {
  return axiosClient.post(`/auth/password/reset/`, {...request_body});
};

export const confirmResetPassword = (uid: string, token: string, request_body: ConfirmPasswordResetData): Promise<Response<any>> => {
  return axiosClient.post(`/auth/password/reset/confirm/${uid}/${token}/`, {...request_body});
};

export const logout = () => {
  return onLogout().then(() => {
    localStorage.removeItem('token');
    window.location.reload();
  }).catch(err => {
    // remove token and reload either way;
    // even though user might still be logged on the backend with old creds
    localStorage.removeItem('token');
    window.location.reload();
  });
};
