import {Grid, useMediaQuery, useTheme} from "@material-ui/core";
import React, {FC, useCallback, useEffect, useState} from "react";
import {useHistory, useParams} from "react-router";
import useWebSocket from "react-use-websocket";
import axiosClient from "../api/axiosClient";
import {UserObject, WebsocketConnectionState, WebsocketMessage} from "../utils/ws";
import "./Room.scss";
import BeerFormStepper from "./room/BeerFormStepper";
import {RoomContext} from "../context/roomContext";
import Sidebar from "./layout/Sidebar";
import Header from "./layout/Header";
import ChatSidebar from "./layout/ChatSidebar";
import DesktopChat from "./room/DesktopChat";

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
    return axiosClient.get(`/api/rooms/in?code=${code}`).then(({data}) => {
      const {is_host} = data;
      setIsHost(Boolean(is_host));
      return `ws://127.0.0.1:8000/ws/room/${code}/`;
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
          setBeers([...parsed.data])
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
  const [beers, setBeers] = useState<any[]>([]);

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
      })
    }, USER_PING_INTERVAL_MS)
    return () => clearInterval(pingInterval);
  }, [sendJsonMessage])

  useEffect(() => {
    // check if users in room changed
    const interval = setInterval(() => {
      sendJsonMessage({
        command: 'get_users'
      })
    }, USERS_FETCH_INTERVAL_MS)
    return () => clearInterval(interval);
  }, [sendJsonMessage])

  return (
    <RoomContext.Provider value={{
      code: code,
      isHost: isHost,
      wsState: connectionStatus,
      beers: beers,
      users: users,
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
          message={message}
          messages={messages}
          handleChange={handleChange}
          handleSendMessage={handleSendMessage}
        />
      )}

      <Grid container>
        <Grid item xs={12} md={8} lg={10} className="room-body">
          <BeerFormStepper beers={beers}/>

          <Grid item xs={12}>
            <button onClick={() => {
              sendJsonMessage({
                'command': 'get_beers'
              })
            }}>Get beers
            </button>
          </Grid>

        </Grid>

        {matches && (
          <Grid item md={4} lg={2} className="room-chat">
            <DesktopChat
              message={message} messages={messages}
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
