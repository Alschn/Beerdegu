import {ReadyState} from "react-use-websocket";


export const WebsocketConnectionState = {
  [ReadyState.CONNECTING]: 'Connecting',
  [ReadyState.OPEN]: 'Open',
  [ReadyState.CLOSING]: 'Closing',
  [ReadyState.CLOSED]: 'Closed',
  [ReadyState.UNINSTANTIATED]: 'Uninstantiated',
};

export interface UserObject {
  id: string | number,
  username: string,
}

export interface BeerObject {
  id: number,
  name: string,
  percentage: number,
  volume_ml: number,
  extract: number,
  IBU: number,
  hop_rate: number,
  image?: string,
  description?: string,
  brewery?: any,
  style?: any,
  hops: any[]
}

export interface SimplifiedBeerObject {
  name: string,
  brewery: string,
  style: string,
}

export interface RatingsObject {
  beer: SimplifiedBeerObject,
  average_rating: number,
}

export interface UserRatingsObject {
  color: string,
  smell: string,
  foam: string,
  taste: string,
  opinion: string,
  note: number
}

export interface WebsocketMessage {
  data: any | UserObject[],
  extra?: any,
  command: CommandType,
}

export type CommandType =
  'set_new_message' | 'set_users' |
  'set_beers' | 'set_form_data' |
  'set_room_state' | 'set_final_results' |
  'set_user_results'
  ;

export interface ChatMessageObject {
  message: string,
  user: string,
}
