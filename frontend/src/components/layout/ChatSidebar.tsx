import React, {FC} from "react";
import Drawer from "@material-ui/core/Drawer";
import {SidebarProps} from "./Sidebar";
import "./Sidebar.scss";
import {useRoomContext} from "../../hooks/useContextHook";

interface ChatSidebarProps extends SidebarProps {
  handleSendMessage: () => void,
  handleChange: (e: React.BaseSyntheticEvent) => void,
}

const ChatSidebar: FC<ChatSidebarProps> = ({open, toggleDrawerHandler, handleSendMessage, handleChange}) => {
  const {message, messages} = useRoomContext();

  return (
    <Drawer open={open} onClose={toggleDrawerHandler} anchor="right">
      <div
        className="sidebar"
        role="presentation"
      >
        {/* to do sidebar chat */}
      </div>
    </Drawer>
  );
};

export default ChatSidebar;
