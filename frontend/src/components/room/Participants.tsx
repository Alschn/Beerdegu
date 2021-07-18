import React, {FC} from "react";
import {useRoomContext} from "../../hooks/useContextHook";
import {List, ListItem} from "@material-ui/core";


const Participants: FC = () => {
  const {users} = useRoomContext();

  return (
    <List>
      <ListItem><strong>Participants:</strong></ListItem>
      {users && users.length > 0 && users.map(
        ({username}, idx) => <ListItem>{idx + 1}. {username}</ListItem>)
      }
    </List>
  );
};

export default Participants;
