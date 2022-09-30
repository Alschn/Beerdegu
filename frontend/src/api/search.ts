import AxiosClient from "./axiosClient";
import {Response} from "./types";
import {BeerObject} from "./ws";

export const getBeersByQuery = (query: string): Promise<Response<BeerObject[]>> => {
  return AxiosClient.get(`/api/beers/?search=${query}`);
};
