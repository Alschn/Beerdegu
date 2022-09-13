import {createContext, Dispatch} from "react";
import {BeerObject, ChatMessageObject, RatingsObject, UserObject} from "../api/ws";

export type roomStateType = 'WAITING' | 'STARTING' | 'IN_PROGRESS' | 'FINISHED';

interface RoomContextProps {
  code: string,
  isHost: boolean,
  sendMessage: (jsonMessage: any) => void,
  wsState: string,
  message: string,
  messages: ChatMessageObject[],
  beers: BeerObject[],
  users: UserObject[],
  roomState: roomStateType,
  results: RatingsObject[],
  userResults: any[],
  dispatch: Dispatch<any>,
}

const RoomContext = createContext<RoomContextProps>({} as RoomContextProps);
export default RoomContext;
