import {Grid} from "@material-ui/core";
import React, {FC, useCallback, useEffect, useState} from "react";
import {useHistory, useParams} from "react-router";
import useWebSocket from "react-use-websocket";
import axiosClient from "../api/axiosClient";
import {WebsocketConnectionState, WebsocketMessage} from "../utils/ws";
import "./Room.scss";
import Participants from "./room/Participants";
import BeerFormStepper from "./room/BeerFormStepper";
import {RoomContext} from "../context/roomContext";

interface RoomParamsProps {
  code: string;
}

const USER_PING_INTERVAL_MS = 14_000;

const Room: FC = () => {
  const {code} = useParams<RoomParamsProps>();
  const history = useHistory();

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

  const [message, setMessage] = useState<string>("");
  const [messages, setMessages] = useState<string[]>([]);

  const [beers, setBeers] = useState<any[]>([]);

  const handleChange = (e: React.BaseSyntheticEvent): void => setMessage(e.target.value);

  const handleSendMessage = (): void => {
    sendJsonMessage({
      data: message,
      command: 'get_new_message',
    });
  };

  useEffect(() => {
    const pingInterval = setInterval(() => {
      sendJsonMessage({
        command: 'user_active',
      })
    }, USER_PING_INTERVAL_MS)
    return () => clearInterval(pingInterval);
  }, [])

  const handlePressEnter = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter') {
      handleSendMessage();
    }
  };

  return (
    <RoomContext.Provider value={{
      code: code,
      isHost: isHost,
    }}>
      <Grid container justifyContent="center">
        <Grid item xs={12} style={{textAlign: 'center'}}>
          <h1>Room {code}</h1>
          <h2>IsHost: {String(isHost)}</h2>
          <h2>Websocket state: {connectionStatus}</h2>
        </Grid>

        <Grid item xs={12}>
          <ol>
            {messages.length > 0 && messages.map((m, idx) => (
              <li key={"message" + idx}>{m}</li>
            ))}
          </ol>

          <Participants/>
        </Grid>

        <BeerFormStepper beers={beers}/>

        <Grid item xs={12}>
          <input onChange={handleChange} onKeyDown={handlePressEnter}/>

          <button onClick={handleSendMessage}>
            Send message
          </button>

          <button onClick={() => {
            sendJsonMessage({
              'command': 'get_beers'
            })
          }}>Get beers
          </button>
        </Grid>
      </Grid>
    </RoomContext.Provider>
  );
};

export default Room;
