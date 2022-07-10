import {FC} from "react";
import {useRoomContext} from "../../hooks/useContextHook";
import {AppBar, Avatar, Box, IconButton, Toolbar, Typography} from "@mui/material";
import {AvatarGroup} from "@mui/lab";
import ChatOutlinedIcon from '@mui/icons-material/ChatOutlined';
import MenuIcon from "@mui/icons-material/Menu";


interface HeaderProps {
  openDrawerHandler: () => any;
  openSideBarChatHandler: () => any;
}

const Header: FC<HeaderProps> = ({openDrawerHandler, openSideBarChatHandler}) => {
  const {code, users} = useRoomContext();

  return (
    <Box flexGrow={1}>
      <AppBar position="fixed">
        <Toolbar>
          <IconButton
            edge="start"
            sx={(theme) => ({marginRight: theme.spacing(2)})}
            color="inherit"
            aria-label="open drawer"
            onClick={openDrawerHandler}
          >
            <MenuIcon/>
          </IconButton>

          <Typography display="block" variant="h6" noWrap>
            Pokój {code}
          </Typography>

          <Box flexGrow={1}/>

          <Box sx={(theme) => ({
            display: "flex",
            [theme.breakpoints.up("md")]: {
              display: "none"
            }
          })}>
            <IconButton onClick={openSideBarChatHandler} sx={{color: "#eeeeee"}}>
              <ChatOutlinedIcon/>
            </IconButton>
          </Box>

          <AvatarGroup max={3} sx={(theme) => (
            {
              '& > *': {
                width: theme.spacing(4),
                height: theme.spacing(4),
                border: '1px solid #0080E3',
              }
            }
          )}>
            {users && users.length > 0 && users.map(({username}, idx) => (
              <Avatar
                alt={username}
                src=""
                key={`avatar-${idx}`}
              >
                {username.charAt(0) + username.charAt(1)}
              </Avatar>
            ))}
          </AvatarGroup>
        </Toolbar>
      </AppBar>
    </Box>
  );
};

export default Header;
