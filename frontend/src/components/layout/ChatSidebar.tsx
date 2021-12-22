import {BaseSyntheticEvent, FC} from "react";
import {SidebarProps} from "./Sidebar";
import {useRoomContext} from "../../hooks/useContextHook";
import {Button, List, ListItem, TextField, Drawer} from "@mui/material";
import "./Sidebar.scss";


interface ChatSidebarProps extends SidebarProps {
  handleSendMessage: () => void,
  handleChange: (e: BaseSyntheticEvent) => void,
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
