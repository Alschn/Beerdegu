import AxiosClient from "./axiosClient";
import {PaginatedResponse} from "./types";
import {BeerObject} from "./ws";

export const getBeers = (page: number = 1): Promise<PaginatedResponse<BeerObject>> => {
  return AxiosClient.get(`/api/beers/?page=${page}`);
};

export const getBeersByQuery = (query: string, page: number = 1): Promise<PaginatedResponse<BeerObject>> => {
  return AxiosClient.get(`/api/beers/?search=${query}&page=${page}`);
};
