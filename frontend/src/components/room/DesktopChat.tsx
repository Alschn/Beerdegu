import React, {FC} from "react";
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
    <div className="desktop-chat">
      {/* to do desktop chat */}
      <List>
        {messages.length > 0 && messages.map((m, idx) => (
          <ListItem key={"message" + idx}>{m}</ListItem>
        ))}
      </List>

      <TextField
        value={message}
        onChange={handleChange}
        onKeyDown={handlePressEnter}
        variant="outlined"
      />

      <Button
        onClick={handleSendMessage}
        variant="contained"
        color="primary"
      >
        Wyślij
      </Button>
    </div>
  );
};

export default DesktopChat;
