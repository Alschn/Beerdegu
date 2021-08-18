import AxiosClient from "./axiosClient";

export const addBeerToRoom = (room_name: string, beer_id: number): Promise<any> => {
  return AxiosClient.put(`/api/rooms/${room_name}/beers`, {
    beer_id: beer_id
  });
};

export const removeBeerFromRoom = (room_name: string, beer_id: number): Promise<any> => {
  return AxiosClient.delete(`/api/rooms/${room_name}/beers?id=${beer_id}`);
};
