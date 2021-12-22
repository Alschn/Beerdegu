import {FC} from "react";
import {useRoomContext} from "../../hooks/useContextHook";
import {AppBar, Avatar, IconButton, Toolbar, Typography} from "@mui/material";
import {AvatarGroup} from "@mui/lab";
import ChatOutlinedIcon from '@mui/icons-material/ChatOutlined';
import MenuIcon from "@mui/icons-material/Menu";
import {makeStyles} from "@mui/styles";
import {Theme} from "@mui/system";


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
  avatars: {
    '& > *': {
      width: theme.spacing(4),
      height: theme.spacing(4),
      border: '1px solid #0080E3',
    }
  },
  chatIcon: {
    color: '#eeeeee'
  },
  blue: {
    backgroundColor: '#0074d0',
  },
  green: {
    backgroundColor: '#008a28'
  }
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
      <AppBar position="fixed">
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
            Pokój {code}
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
                className={idx === 0 ? classes.blue : classes.green}
              >
                {username.charAt(0) + username.charAt(1)}
              </Avatar>
            ))}
          </AvatarGroup>
        </Toolbar>
      </AppBar>
    </div>
  );
};

export default Header;
