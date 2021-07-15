import React, {FC} from "react";
import {UserObject} from "../../utils/ws";


interface ParticipantsProps {
  users: UserObject[],
}

const Participants: FC<ParticipantsProps> = ({users}) => {
  return (
    <ol>
      {users.length > 0 && users.map(({id, username}) => <li>{id} {username}</li>)}
    </ol>
  );
};

export default Participants;
