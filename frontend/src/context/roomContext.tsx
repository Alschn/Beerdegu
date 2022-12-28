import {createContext, Dispatch} from "react";
import {BeerObject, ChatMessageObject, RatingsObject, UserObject} from "../api/ws";

const RoomState = {
  WAITING: "WAITING",
  STARTING: "STARTING",
  IN_PROGRESS: "IN_PROGRESS",
  FINISHED: "FINISHED",
} as const;

export type RoomStateType = typeof RoomState[keyof typeof RoomState];

interface RoomContextProps {
  code: string,
  isHost: boolean,
  sendMessage: (jsonMessage: any) => void,
  wsState: string,
  message: string,
  messages: ChatMessageObject[],
  beers: BeerObject[],
  users: UserObject[],
  roomState: RoomStateType,
  results: RatingsObject[],
  userResults: any[],
  dispatch: Dispatch<any>,
}

const RoomContext = createContext<RoomContextProps>({} as RoomContextProps);

export default RoomContext;
