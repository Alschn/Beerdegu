import AxiosClient from "./axiosClient";

export const getBeersByQuery = (query: string): Promise<any> => {
  return AxiosClient.get(`/api/beers/?search=${query}`);
};
