import React, {FC} from "react";
import Drawer from "@material-ui/core/Drawer";
import Participants from "../room/Participants";
import {useRoomContext} from "../../hooks/useContextHook";
import {List, ListItem} from "@material-ui/core";

export interface SidebarProps {
  open: boolean,
  toggleDrawerHandler: () => void,
}

const Sidebar: FC<SidebarProps> = ({open, toggleDrawerHandler}) => {
  const {code} = useRoomContext();

  return (
    <Drawer open={open} onClose={toggleDrawerHandler}>
      <div
        className="sidebar"
        style={{width: 250}}
        role="presentation"
        onClick={toggleDrawerHandler}
        onKeyDown={toggleDrawerHandler}
      >
        <List>
          <ListItem>
            <h2>Room {code}</h2>
          </ListItem>
        </List>
        <Participants/>
      </div>
    </Drawer>
  );
};

export default Sidebar;
