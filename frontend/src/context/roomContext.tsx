import {createContext} from "react";
import {BeerObject, RatingsObject, UserObject} from "../utils/ws";

export type roomStateType = 'WAITING' | 'STARTING' | 'IN_PROGRESS' | 'FINISHED';

interface RoomContextProps {
  code: string,
  isHost: boolean,
  sendMessage: (jsonMessage: any) => void,
  wsState: string,
  message: string,
  messages: string[],
  beers: BeerObject[],
  users: UserObject[],
  roomState: roomStateType,
  results: RatingsObject[],
  userResults: any[],
}

const RoomContext = createContext<RoomContextProps>({} as RoomContextProps);
export default RoomContext;
