import React, {FC, useState} from "react";
import axiosClient from "../../api/axiosClient";
import {useHistory} from "react-router";

const JoinRoom: FC = () => {
  const history = useHistory();
  const [roomName, setRoomName] = useState<string>("");

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => setRoomName(e.target.value);

  const handleSubmit = () => {
    axiosClient.put(`/api/rooms/${roomName}/join`, {
      'name': roomName
    }).then(() => {
      history.push(`/room/${roomName}`);
    }).catch(err => console.log(err));
  };

  return (
    <div>
      <input value={roomName} onChange={handleChange}/>
      <button onClick={handleSubmit}>Join</button>
    </div>
  );
};

export default JoinRoom;
