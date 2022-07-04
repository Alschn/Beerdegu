import AxiosClient from "./axiosClient";
import {Response} from "./types";

export const getBeers = (): Promise<Response<any>> => {
  return AxiosClient.get(`/api/beers/`);
};
