import axios from "axios";

const client = (token: string | null = null) => {
  const defaultOptions = {
    headers: {
      "Authorization": token ? `Token ${token}` : '',
      "Content-Type": "application/json",
    },
  };

  return {
    get: (url: string, options: object = {}) => axios.get(url, {...defaultOptions, ...options}),
    post: (url: string, data: object, options: object = {}) => axios.post(url, data, {...defaultOptions, ...options}),
    put: (url: string, data: object, options: object = {}) => axios.put(url, data, {...defaultOptions, ...options}),
    patch: (url: string, data: object, options: object = {}) => axios.patch(url, data, {...defaultOptions, ...options}),
    delete: (url: string, options: object = {}) => axios.delete(url, {...defaultOptions, ...options}),
  };
};

const AxiosClient = client(localStorage.getItem('token'));

export default AxiosClient;
