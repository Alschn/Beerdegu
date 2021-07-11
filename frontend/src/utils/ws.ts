import {ReadyState} from "react-use-websocket/dist";

export const WebsocketConnectionState = {
  [ReadyState.CONNECTING]: 'Connecting',
  [ReadyState.OPEN]: 'Open',
  [ReadyState.CLOSING]: 'Closing',
  [ReadyState.CLOSED]: 'Closed',
  [ReadyState.UNINSTANTIATED]: 'Uninstantiated',
};

export interface WebsocketMessage {
  data: any,
  command: CommandType,
}

export type CommandType =
  'set_new_message' |
  ''
  ;
