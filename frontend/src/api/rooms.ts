import AxiosClient from "./axiosClient";
import {PaginatedResponse, Response} from "./types";
import {AxiosRequestConfig} from "axios";
import {BeerObject} from "./ws";

interface CheckUserInRoomData {
  is_host: boolean;
}

interface LeaveRoomData {
  message: string;
}

export const getRooms = (): Promise<PaginatedResponse<any>> => {
  return AxiosClient.get('/api/rooms/');
};

export const joinRoom = (roomName: string, password: string): Promise<Response<any>> => {
  return AxiosClient.put(`/api/rooms/${roomName}/join/`, {
    password: password,
  });
};

export type CreateRoomPayload = {
  name: string,
  password: string,
  slots: undefined | number
}

interface CreateRoomData {

}

interface RemoveBeerData {
  message: string;
}

export const createRoom = (formState: CreateRoomPayload): Promise<Response<CreateRoomData>> => {
  return AxiosClient.post('/api/rooms/', {...formState});
};

export const getBeersInRoom = (room_name: string): Promise<Response<BeerObject[]>> => {
  return AxiosClient.get(`/api/rooms/${room_name}/beers/`);
};

export const addBeerToRoom = (room_name: string, beer_id: number): Promise<Response<BeerObject[]>> => {
  return AxiosClient.put(`/api/rooms/${room_name}/beers/`, {
    beer_id: beer_id
  });
};

export const removeBeerFromRoom = (room_name: string, beer_id: number): Promise<Response<RemoveBeerData>> => {
  return AxiosClient.delete(`/api/rooms/${room_name}/beers/?beer_id=${beer_id}`);
};


export const checkUserInRoom = (roomName: string): Promise<Response<CheckUserInRoomData>> => {
  return AxiosClient.get(`/api/rooms/${roomName}/in/`);
};


export const leaveRoom = (roomName: string): Promise<Response<LeaveRoomData>> => {
  return AxiosClient.delete(`/api/rooms/${roomName}/leave/`);
};

export const generateReport = (roomName: string, options?: AxiosRequestConfig): Promise<Response<Blob>> => {
  return AxiosClient.get(`/api/rooms/${roomName}/report/`, {
    responseType: 'blob',
    ...options
  });
};
