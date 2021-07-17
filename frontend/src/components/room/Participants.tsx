import React, {FC, useEffect, useState} from "react";
import {UserObject, WebsocketMessage} from "../../utils/ws";
import {useWebSocket} from "react-use-websocket/dist/lib/use-websocket";
import {useRoomContext} from "../../hooks/useContextHook";


const USERS_FETCH_INTERVAL_MS = 12_000;

const Participants: FC = () => {
  const {code} = useRoomContext();
  const [users, setUsers] = useState<UserObject[]>([]);

  const {
    sendJsonMessage,
  } = useWebSocket(`ws://127.0.0.1:8000/ws/room/${code}/`, {
    shouldReconnect: () => true,
    share: true,
    onMessage: (event) => {
      const parsed: WebsocketMessage = JSON.parse(event.data);
      if (parsed.command === 'set_users') {
        setUsers([...parsed.data]);
      }
    }
  });

  useEffect(() => {
    const interval = setInterval(() => {
      sendJsonMessage({
        command: 'get_users'
      })
    }, USERS_FETCH_INTERVAL_MS)
    return () => clearInterval(interval);
  }, [sendJsonMessage])

  return (
    <ol>
      {users.length > 0 && users.map(({id, username}) => <li>{id} {username}</li>)}
    </ol>
  );
};

export default Participants;
