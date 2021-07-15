import React, {FC, useCallback, useState} from "react";
import {useHistory, useParams} from "react-router";
import useWebSocket from "react-use-websocket";
import axiosClient from "../api/axiosClient";
import {WebsocketConnectionState, WebsocketMessage} from "../utils/ws";
import "./Room.scss";

interface RoomParamsProps {
  code: string;
}

const Room: FC = () => {
  const {code} = useParams<RoomParamsProps>();
  const history = useHistory();

  const getWebsocketUrl = useCallback(() => {
    return axiosClient.get(`/api/in?code=${code}`).then(() => {
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
    shouldReconnect: (closeEvent) => false,
    onMessage: (event) => {
      const parsed: WebsocketMessage = JSON.parse(event.data);
      switch (parsed.command) {
        case 'set_new_message':
          setMessages(prevState => [...prevState, parsed.data]);
          break;
        default:
          break;
      }
    }
  });

  const connectionStatus = WebsocketConnectionState[readyState];

  const [message, setMessage] = useState<string>("");
  const [messages, setMessages] = useState<string[]>([]);

  const handleChange = (e: React.BaseSyntheticEvent): void => setMessage(e.target.value);

  const handleSend = (): void => {
    sendJsonMessage({
      message: message,
      command: 'get_new_message',
    });
  };

  const handlePressEnter = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter') {
      handleSend();
    }
  };

  return (
    <div>
      <h1>Room {code}</h1>

      <h2>Websocket state: {connectionStatus}</h2>

      <div>
        <input onChange={handleChange} onKeyDown={handlePressEnter}/>
        <button onClick={handleSend}>
          Send message
        </button>
      </div>

      <div>
        <ol>
          {messages.length > 0 && messages.map((m, idx) => (
            <li key={"message" + idx}>{m}</li>
          ))}
        </ol>
      </div>
    </div>
  );
};

export default Room;
