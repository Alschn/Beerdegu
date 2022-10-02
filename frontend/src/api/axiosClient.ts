import axios, {AxiosRequestConfig} from "axios";
import {ACCESS_TOKEN_KEY, BACKEND_URL, REFRESH_TOKEN_KEY} from "../config";

const axiosConfig: AxiosRequestConfig = {
  headers: {'Content-Type': 'application/json'},
  baseURL: BACKEND_URL,
};

const AxiosClient = axios.create(axiosConfig);

const AUTH_HEADER_TYPE = 'Bearer';
const REFRESH_TOKEN_TIMEOUT_MS = 10_000;

// before sending request attach auth token
AxiosClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem(ACCESS_TOKEN_KEY);
    config!.headers!.Authorization = token ? `${AUTH_HEADER_TYPE} ${token}` : '';
    return config;
  },
  error => {
    const {response, config} = error;

    const refreshToken = localStorage.getItem(REFRESH_TOKEN_KEY);

    if (response.status !== 401) {
      return Promise.reject(error);
    }

    // cannot refresh token
    if (!refreshToken) {
      localStorage.removeItem(ACCESS_TOKEN_KEY);
      window.location.pathname = "/login";
      return Promise.reject(error);
    }

    return axios.post(`/api/auth/token/refresh/`, {refresh: refreshToken}, {
      ...axiosConfig,
      timeout: REFRESH_TOKEN_TIMEOUT_MS,
    }).then((res) => {
      const {access} = res.data;
      localStorage.setItem(ACCESS_TOKEN_KEY, access);
      return AxiosClient(config);
    }).catch((err) => {
      // `refresh` is missing or has expired,
      // the only way to get new access token is to sign in again
      if (err?.response?.status === 400) {
        localStorage.removeItem(ACCESS_TOKEN_KEY);
        localStorage.removeItem(REFRESH_TOKEN_KEY);
        window.location.pathname = "/login";
      }

      return Promise.reject(error);
    });
  }
);

export default AxiosClient;
