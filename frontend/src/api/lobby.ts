import AxiosClient from "./axiosClient";
import {Response} from "./types";

export const getRooms = (): Promise<Response<any>> => {
  return AxiosClient.get('/api/rooms/');
};

export const joinRoom = (roomName: string, password: string): Promise<Response<any>> => {
  return AxiosClient.put(`/api/rooms/${roomName}/join`, {
    name: roomName,
    password: password,
  });
};

export type createRoomForm = {
  name: string,
  password: string,
  slots: undefined | number
}

export const createRoom = (formState: createRoomForm): Promise<Response<any>> => {
  return AxiosClient.post('/api/rooms/', {...formState});
};

export const deleteRoom = (roomName: string): Promise<Response<any>> => {
  return AxiosClient.delete(`/api/rooms/${roomName}/`);
};
