import {FC} from "react";
import Participants from "../room/Participants";
import {useRoomContext} from "../../hooks/useContextHook";
import {Divider, Drawer, List, ListItem, ListItemText} from "@mui/material";
import logo from "../../images/logo.svg";
import {roomStateType} from "../../context/roomContext";
import {useNavigate} from "react-router-dom";
import {leaveRoom} from "../../api/room";

export interface SidebarProps {
  open: boolean,
  toggleDrawerHandler: () => void,
}

const Sidebar: FC<SidebarProps> = ({open, toggleDrawerHandler}) => {
  const {code, isHost, sendMessage, roomState} = useRoomContext();
  const navigate = useNavigate();

  const getRoomState = () => {
    sendMessage({
      command: 'get_room_state',
    });
  };

  const loadBeers = () => {
    sendMessage({
      command: 'load_beers',
    });
  };

  const changeRoomState = (new_state: roomStateType) => {
    sendMessage({
      command: 'change_room_state',
      data: new_state,
    });
  };

  const handleLeaveRoom = () => {
    leaveRoom(code).then((res) => {
        sendMessage({
          command: 'get_users',
        });
        navigate('/');
      }
    ).catch(err => console.log(err));
  };

  const getRatingsAndStatistics = () => {
    sendMessage({
      command: 'get_user_ratings',
    });

    sendMessage({
      command: 'get_final_ratings',
    });
  };

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
          <div className="logo-wrapper">
            <img src={logo} alt="" className="logo"/>
            <span className="title">Beerdegu</span>
          </div>

          <Divider/>

          <ListItem>
            <h2 style={{margin: '5px 0 5px 0', padding: 0}}>Pokój {code}</h2>
          </ListItem>

          {isHost && (
            <>
              <ListItem button onClick={() => getRoomState()}>
                <ListItemText>Odśwież informacje o pokoju</ListItemText>
              </ListItem>

              {roomState !== 'FINISHED' && (
                <ListItem button onClick={() => loadBeers()}>
                  <ListItemText>Załaduj/Odśwież piwa</ListItemText>
                </ListItem>
              )}

              {roomState === 'WAITING' && (
                <ListItem button onClick={() => changeRoomState('STARTING')}>
                  <ListItemText>Przejdź do wyboru piw</ListItemText>
                </ListItem>
              )}

              {roomState !== 'IN_PROGRESS' ? (
                <ListItem button onClick={() => {
                  changeRoomState('IN_PROGRESS');
                }}>
                  <ListItemText>
                    {roomState === 'WAITING' || roomState === 'STARTING' ? 'Rozpocznij' : 'Wznów'} degustację
                  </ListItemText>
                </ListItem>
              ) : (
                <>
                  <ListItem button onClick={() => changeRoomState('STARTING')}>
                    <ListItemText>Wróc do wyboru piw</ListItemText>
                  </ListItem>

                  <ListItem button onClick={() => changeRoomState('FINISHED')}>
                    <ListItemText>Zakończ degustację</ListItemText>
                  </ListItem>
                </>
              )}

              {roomState === 'FINISHED' && (
                <ListItem button onClick={() => getRatingsAndStatistics()}>
                  <ListItemText>Wyświetl statystyki</ListItemText>
                </ListItem>
              )}
              <Divider/>
            </>
          )}

          <ListItem button onClick={() => handleLeaveRoom()}>
            <ListItemText>Wyjdź</ListItemText>
          </ListItem>
          <Divider/>
        </List>

        <List>
          <ListItem>
            <ListItemText>
              <strong>Stan: </strong>
              {roomState}
            </ListItemText>
          </ListItem>
        </List>

        <Participants/>
      </div>
    </Drawer>
  );
};

export default Sidebar;
