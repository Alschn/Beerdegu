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

export interface WebsocketMessage {
  data: any | UserObject[],
  command: CommandType,
}

export type CommandType =
  'set_new_message' | 'set_users' |
  ''
  ;
