import AxiosClient from "./axiosClient";
import {Response} from "./types";
import {BeerObject} from "./ws";

export const getBeers = (): Promise<Response<BeerObject[]>> => {
  return AxiosClient.get(`/api/beers/`);
};
