import {Grid, useMediaQuery, useTheme} from "@material-ui/core";
import React, {FC, useCallback, useEffect, useReducer, useState} from "react";
import {useHistory, useParams} from "react-router";
import useWebSocket from "react-use-websocket";
import {BeerObject, RatingsObject, UserObject, WebsocketConnectionState, WebsocketMessage} from "../../utils/ws";
import RoomContext, {roomStateType} from "../../context/roomContext";
import Sidebar from "../layout/Sidebar";
import Header from "../layout/Header";
import ChatSidebar from "../layout/ChatSidebar";
import DesktopChat from "../room/DesktopChat";
import {HOST, WS_SCHEME} from "../../config";
import AxiosClient from "../../api/axiosClient";
import RoomStateComponent from "../room/RoomStateComponent";
import "./Room.scss";


const USER_PING_INTERVAL_MS = 14_000;
const USERS_FETCH_INTERVAL_MS = 12_000;

const TRY_RECONNECT_TIMES = 5;

interface RoomParamsProps {
  code: string;
}

interface State {
  messages: string[],
  beers: BeerObject[],
  users: UserObject[],
  roomState: roomStateType,
  results: RatingsObject[],
  userResults: any[],
}

type Action =
  | { type: 'set_new_message', payload: string }
  | { type: 'set_beers', payload: BeerObject[] }
  | { type: 'set_users', payload: UserObject[] }
  | { type: 'set_room_state', payload: roomStateType }
  | { type: 'set_final_results', payload: RatingsObject[] }
  | { type: 'set_user_results', payload: any[] }
  | { type: string, payload: any } // handles any other case which will not affect state

const initialState: State = {
  messages: [],
  beers: [],
  users: [],
  roomState: 'WAITING',
  results: [],
  userResults: [],
};

const roomReducer = (state = initialState, action: Action): State => {
  switch (action.type) {
    case "set_new_message":
      return {
        ...state,
        messages: [...state.messages, action.payload]
      };
    case "set_beers":
      return {
        ...state,
        beers: [...action.payload]
      };
    case "set_users":
      return {
        ...state,
        users: [...action.payload]
      };
    case "set_room_state":
      return {
        ...state,
        roomState: action.payload.state
      };
    case "set_final_results":
      return {
        ...state,
        results: [...action.payload]
      };
    case "set_user_results":
      return {
        ...state,
        userResults: [...action.payload]
      };
    default:
      return state;
  }
};


const Room: FC = () => {
  const {code} = useParams<RoomParamsProps>();
  const history = useHistory();
  const theme = useTheme();
  const matches = useMediaQuery(theme.breakpoints.up('md'));

  const [isHost, setIsHost] = useState<boolean>(false);
  const [shouldConnect, setShouldConnect] = useState<boolean>(false);

  const checkUserInRoom = useCallback(() => {
    return AxiosClient.get(`/api/rooms/in?code=${code}`).then(({data}) => {
      const {is_host} = data;
      setIsHost(Boolean(is_host));
      setShouldConnect(true);
    }).catch(() => {
      setShouldConnect(false);
      history.push('/');
    });
  }, [code, history]);

  useEffect(() => {
    // on mount decide if the client should connect to ws backend
    // or get directed back to home page
    checkUserInRoom().then(() => {
    });
  }, [checkUserInRoom]);

  // State related to data that comes via websockets
  const [state, dispatch] = useReducer(roomReducer, initialState);

  const {
    sendJsonMessage,
    readyState,
  } = useWebSocket(`${WS_SCHEME}://${HOST}/ws/room/${code}/`, {
    onOpen: () => console.log('Websocket open'),
    shouldReconnect: (closeEvent) => true,
    onMessage: (event) => {
      const parsed: WebsocketMessage = JSON.parse(event.data);
      dispatch({
        type: parsed.command,
        payload: parsed.data
      });
    },
    reconnectAttempts: TRY_RECONNECT_TIMES,
    share: true,
  }, shouldConnect);

  const connectionStatus = WebsocketConnectionState[readyState];

  const [message, setMessage] = useState<string>('');
  const [open, setOpen] = useState<boolean>(false);
  const [openSidebarChat, setOpenSidebarChat] = useState<boolean>(false);

  const handleChange = (e: React.BaseSyntheticEvent): void => setMessage(e.target.value);

  const handleSendMessage = (): void => {
    sendJsonMessage({
      data: message,
      command: 'get_new_message',
    });
  };

  useEffect(() => {
    // close sidebar chat if window size is smaller than md
    !matches && setOpenSidebarChat(false);
  }, [matches]);

  useEffect(() => {
    // users ping server to show that they are active
    const pingInterval = setInterval(() => {
      sendJsonMessage({
        command: 'user_active',
      });
    }, USER_PING_INTERVAL_MS);
    return () => clearInterval(pingInterval);
  }, [sendJsonMessage]);

  useEffect(() => {
    // check if users in room changed
    const interval = setInterval(() => {
      sendJsonMessage({
        command: 'get_users'
      });
    }, USERS_FETCH_INTERVAL_MS);
    return () => clearInterval(interval);
  }, [sendJsonMessage]);

  useEffect(() => {
    if (state.roomState === 'IN_PROGRESS') {
      sendJsonMessage({
        command: 'load_beers',
      });
    }
  }, [state.roomState, sendJsonMessage]);

  useEffect(() => {
    if (state.roomState === 'FINISHED') {
      sendJsonMessage({
        command: 'get_user_ratings',
      });
      sendJsonMessage({
        command: 'get_final_ratings',
      });
    }
  }, [state.roomState, sendJsonMessage]);

  return (
    <RoomContext.Provider value={{
      code: code,
      isHost: isHost,
      wsState: connectionStatus,
      sendMessage: sendJsonMessage,
      message: message,
      ...state,
      dispatch: dispatch,
    }}>
      <Header
        openDrawerHandler={() => setOpen(true)}
        openSideBarChatHandler={() => setOpenSidebarChat(true)}
      />
      <Sidebar
        open={open}
        toggleDrawerHandler={() => setOpen(false)}
      />
      {!matches && (
        <ChatSidebar
          open={openSidebarChat}
          toggleDrawerHandler={() => setOpenSidebarChat(false)}
          handleChange={handleChange}
          handleSendMessage={handleSendMessage}
        />
      )}

      <Grid container>
        <Grid item xs={12} md={8} lg={10} className="room-body">
          <RoomStateComponent state={state.roomState}/>
        </Grid>

        {matches && (
          <Grid item md={4} lg={2} className="room-chat">
            <DesktopChat
              handleSendMessage={handleSendMessage}
              handleChange={handleChange}
            />
          </Grid>
        )}
      </Grid>
    </RoomContext.Provider>
  );
};

export default Room;
