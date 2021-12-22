import React, {FC} from "react";
import {useRoomContext} from "../../hooks/useContextHook";
import {List, ListItem, ListItemText} from "@mui/material";


const Participants: FC = () => {
  const {users} = useRoomContext();

  return (
    <List>
      <ListItem>
        <ListItemText>
          <strong>Uczestnicy:</strong>
        </ListItemText>
      </ListItem>
      {users && users.length > 0 && users.map(
        ({username}, idx) => <ListItem key={`li-user-${idx}`}>
          <ListItemText>
            <strong>{idx + 1}.</strong> {username}
          </ListItemText>
        </ListItem>)
      }
    </List>
  );
};

export default Participants;
