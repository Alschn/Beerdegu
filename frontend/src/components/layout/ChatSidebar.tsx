import React, {FC} from "react";
import Drawer from "@material-ui/core/Drawer";
import {SidebarProps} from "./Sidebar";
import "./Sidebar.scss";

interface ChatSidebarProps extends SidebarProps {
  message: string,
  messages: string[],
  handleSendMessage: () => void,
  handleChange: (e: React.BaseSyntheticEvent) => void,
}

const ChatSidebar: FC<ChatSidebarProps> = ({open, toggleDrawerHandler, handleSendMessage, handleChange}) => {
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
