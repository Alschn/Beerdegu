import {Grid, useMediaQuery, useTheme} from "@material-ui/core";
import React, {FC, useCallback, useEffect, useState} from "react";
import {useHistory, useParams} from "react-router";
import useWebSocket from "react-use-websocket";
import {BeerObject, RatingsObject, UserObject, WebsocketConnectionState, WebsocketMessage} from "../../utils/ws";
import BeerFormStepper from "../room/BeerFormStepper";
import RoomContext, {roomStateType} from "../../context/roomContext";
import Sidebar from "../layout/Sidebar";
import Header from "../layout/Header";
import ChatSidebar from "../layout/ChatSidebar";
import DesktopChat from "../room/DesktopChat";
import ResultsStepper from "../room/ResultsStepper";
import {HOST, WS_SCHEME} from "../../config";
import "./Room.scss";
import SearchAPI from "../room/SearchAPI";
import Waiting from "../room/Waiting";
import useAxios from "../../hooks/useAxios";
import AxiosClient from "../../api/axiosClient";


interface RoomParamsProps {
  code: string;
}

const USER_PING_INTERVAL_MS = 14_000;
const USERS_FETCH_INTERVAL_MS = 12_000;

const Room: FC = () => {
  const {code} = useParams<RoomParamsProps>();
  const history = useHistory();
  const theme = useTheme();
  const matches = useMediaQuery(theme.breakpoints.up('md'));

  const [isHost, setIsHost] = useState<boolean>(false);

  const getWebsocketUrl = useCallback(() => {
    return AxiosClient.get(`/api/rooms/in?code=${code}`).then(({data}) => {
      const {is_host} = data;
      setIsHost(Boolean(is_host));
      return `${WS_SCHEME}://${HOST}/ws/room/${code}/`;
    }).catch(() => {
      // idk if this is right approach
      history.push('/');
      return Promise.reject('User not in room!');
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [code])

  const {
    sendJsonMessage,
    readyState,
  } = useWebSocket(getWebsocketUrl, {
    onOpen: () => console.log('Websocket open'),
    shouldReconnect: (closeEvent) => true,
    onMessage: (event) => {
      const parsed: WebsocketMessage = JSON.parse(event.data);
      switch (parsed.command) {
        case 'set_new_message':
          setMessages(prevState => [...prevState, parsed.data]);
          break;
        case "set_users":
          setUsers([...parsed.data]);
          break;
        case "set_beers":
          setBeers([...parsed.data]);
          break;
        case "set_room_state":
          setRoomState(parsed.data.state);
          break;
        case "set_final_results":
          setResults([...parsed.data]);
          break;
        case "set_user_results":
          setUserResults([...parsed.data]);
          break;
        default:
          break;
      }
    },
    share: true,
  });

  const connectionStatus = WebsocketConnectionState[readyState];

  const [users, setUsers] = useState<UserObject[]>([]);
  const [message, setMessage] = useState<string>("");
  const [messages, setMessages] = useState<string[]>([]);
  const [beers, setBeers] = useState<BeerObject[]>([]);
  const [roomState, setRoomState] = useState<roomStateType>("WAITING");
  const [results, setResults] = useState<RatingsObject[]>([]);
  const [userResults, setUserResults] = useState<any[]>([]);

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
  }, [matches])

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
    }, USERS_FETCH_INTERVAL_MS)
    return () => clearInterval(interval);
  }, [sendJsonMessage]);

  useEffect(() => {
    if (roomState === 'IN_PROGRESS') {
      sendJsonMessage({
        command: 'load_beers',
      });
    }
  }, [roomState, sendJsonMessage]);

  useEffect(() => {
    if (roomState === 'FINISHED') {
      sendJsonMessage({
        command: 'get_user_ratings',
      });
      sendJsonMessage({
        command: 'get_final_ratings',
      });
    }
  }, [roomState, sendJsonMessage]);

  const renderComponentByRoomState = (): JSX.Element => {
    switch (roomState) {
      case "WAITING":
        return <Waiting/>;
      case "STARTING":
        return <SearchAPI/>;
      case "IN_PROGRESS":
        return <BeerFormStepper/>;
      case "FINISHED":
        return <ResultsStepper/>;
      default:
        return <></>;
    }
  };

  return (
    <RoomContext.Provider value={{
      code: code,
      isHost: isHost,
      wsState: connectionStatus,
      sendMessage: sendJsonMessage,
      message: message,
      messages: messages,
      beers: beers,
      users: users,
      roomState: roomState,
      results: results,
      userResults: userResults,
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
          {renderComponentByRoomState()}
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
