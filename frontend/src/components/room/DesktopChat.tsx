import React, {FC, Fragment} from "react";
import {Button, List, ListItem, TextField} from "@material-ui/core";
import "./DesktopChat.scss";
import {useRoomContext} from "../../hooks/useContextHook";

interface ChatProps {
  handleSendMessage: () => void,
  handleChange: (e: React.BaseSyntheticEvent) => void,
}

const DesktopChat: FC<ChatProps> = (
  {handleChange, handleSendMessage}
) => {
  const {message, messages} = useRoomContext();

  const handlePressEnter = (event: React.KeyboardEvent) => event.key === 'Enter' && handleSendMessage();

  return (
    <Fragment>
      <List className="desktop-chat-messages">
        {messages.length > 0 && messages.map((m, idx) => (
          <ListItem key={"message" + idx} className="chat-message">
            <b>{m.user}:</b> <span>{m.message}</span>
          </ListItem>
        ))}
      </List>

      <div className="desktop-chat-input">
        <TextField
          value={message}
          onChange={handleChange}
          onKeyDown={handlePressEnter}
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
    </Fragment>
  );
};

export default DesktopChat;
