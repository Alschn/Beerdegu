import React, {createContext} from "react";

interface RoomContextProps {
  code?: string,
  isHost?: boolean,
}

export const RoomContext = createContext<RoomContextProps>({});
