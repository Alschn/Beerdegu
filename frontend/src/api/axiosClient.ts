import axios, {AxiosRequestConfig} from "axios";
import {BACKEND_URL} from "../config";

const axiosConfig: AxiosRequestConfig = {
  headers: {'Content-Type': 'application/json'},
  baseURL: BACKEND_URL,
};

const AxiosClient = axios.create(axiosConfig);

// before sending request attach auth token
AxiosClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    config!.headers!.Authorization = token ? `Token ${token}` : '';
    return config;
  },
  error => {
    const {response, config} = error;

    if (response.status !== 401) {
      return Promise.reject(error);
    }

    // if 401 error, then remove token from local storage and reload the page
    if (localStorage.getItem('token')) {
      localStorage.removeItem('token');
      window.location.reload();
    }

    return AxiosClient(config);
  });

export default AxiosClient;
