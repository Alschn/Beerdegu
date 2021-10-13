import React, {FC} from "react";
import Drawer from "@material-ui/core/Drawer";
import {SidebarProps} from "./Sidebar";
import "./Sidebar.scss";
import {useRoomContext} from "../../hooks/useContextHook";
import {Button, List, ListItem, TextField} from "@material-ui/core";

interface ChatSidebarProps extends SidebarProps {
  handleSendMessage: () => void,
  handleChange: (e: React.BaseSyntheticEvent) => void,
}

const ChatSidebar: FC<ChatSidebarProps> = ({open, toggleDrawerHandler, handleSendMessage, handleChange}) => {
  const {message, messages} = useRoomContext();

  return (
    <Drawer open={open} onClose={toggleDrawerHandler} anchor="right">
      <div
        className="sidebar sidebar-chat"
      >
        <List className="sidebar-chat-messages">
          {messages.length > 0 && messages.map((m, idx) => (
            <ListItem key={"message" + idx} className="chat-message">
              <b>{m.user}:</b> <span>{m.message}</span>
            </ListItem>
          ))}
        </List>

        <div className="sidebar-chat-input">
          <TextField
            value={message}
            onChange={handleChange}
            variant="outlined"
            className="input-field"
          />

          <Button
            onClick={handleSendMessage}
            variant="contained"
            color="primary"
            className="submit-button"
          >
            Wyślij
          </Button>
        </div>
      </div>
    </Drawer>
  );
};

export default ChatSidebar;
