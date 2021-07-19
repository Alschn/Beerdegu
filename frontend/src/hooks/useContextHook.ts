import RoomContext from "../context/roomContext";
import {useContext} from "react";

export function useRoomContext() {
  return useContext(RoomContext);
}
