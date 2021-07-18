import React, {createContext, FC} from "react";
import {UserObject} from "../utils/ws";

interface RoomContextProps {
  code?: string,
  isHost?: boolean,
  wsState?: string,
  beers?: any[],
  users?: UserObject[],
}

export const RoomContext = createContext<RoomContextProps>({});


interface RoomContextProviderProps {

}

const RoomContextProvider: FC<RoomContextProviderProps> = () => {
  return (
    <RoomContext.Provider value={{}}>
    {/* maybe will be needed */}
    </RoomContext.Provider>
  );
};

export default RoomContextProvider;
