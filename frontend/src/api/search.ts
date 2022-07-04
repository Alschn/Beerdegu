import AxiosClient from "./axiosClient";
import {Response} from "./types";

export const getBeersByQuery = (query: string): Promise<Response<any>> => {
  return AxiosClient.get(`/api/beers/?search=${query}`);
};
