import React, {FC} from "react";
import {makeStyles, Theme} from "@material-ui/core/styles";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import IconButton from "@material-ui/core/IconButton";
import Typography from "@material-ui/core/Typography";
import MenuIcon from "@material-ui/icons/Menu";
import {useRoomContext} from "../../hooks/useContextHook";
import {Avatar} from "@material-ui/core";
import {AvatarGroup} from "@material-ui/lab";
import ChatOutlinedIcon from '@material-ui/icons/ChatOutlined';


const useStyles = makeStyles((theme: Theme) => ({
  grow: {
    flexGrow: 1
  },
  menuButton: {
    marginRight: theme.spacing(2)
  },
  title: {
    display: "block",
  },
  sectionDesktop: {
    display: "none",
    [theme.breakpoints.up("md")]: {
      display: "flex"
    }
  },
  sectionMobile: {
    display: "flex",
    [theme.breakpoints.up("md")]: {
      display: "none"
    }
  },
  chatIcon: {
    color: '#eeeeee'
  },
  avatars: {
    '& > *': {
      width: theme.spacing(4),
      height: theme.spacing(4),
      border: '1px solid #0080E3',
      backgroundColor: '#0074d0',
    }
  },
}));

interface HeaderProps {
  openDrawerHandler: () => any;
  openSideBarChatHandler: () => any;
}

const Header: FC<HeaderProps> = ({openDrawerHandler, openSideBarChatHandler}) => {
  const {code, users} = useRoomContext();
  const classes = useStyles();

  return (
    <div className={classes.grow}>
      <AppBar position="static">
        <Toolbar>
          <IconButton
            edge="start"
            className={classes.menuButton}
            color="inherit"
            aria-label="open drawer"
            onClick={openDrawerHandler}
          >
            <MenuIcon/>
          </IconButton>

          <Typography className={classes.title} variant="h6" noWrap>
            Room {code}
          </Typography>

          <div className={classes.grow}/>

          <div className={classes.sectionMobile}>
            <IconButton onClick={openSideBarChatHandler} className={classes.chatIcon}>
              <ChatOutlinedIcon/>
            </IconButton>
          </div>

          <AvatarGroup max={3} className={classes.avatars}>
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
    </div>
  );
}

export default Header;
