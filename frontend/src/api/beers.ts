import AxiosClient from "./axiosClient";
import {PaginatedResponse} from "./types";
import {BeerObject} from "./ws";

export const getBeers = (): Promise<PaginatedResponse<BeerObject>> => {
  return AxiosClient.get(`/api/beers/`);
};

export const getBeersByQuery = (query: string): Promise<PaginatedResponse<BeerObject>> => {
  return AxiosClient.get(`/api/beers/?search=${query}`);
};
