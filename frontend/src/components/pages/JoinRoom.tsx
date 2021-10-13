import React, {FC, useState} from "react";
import {useHistory} from "react-router";
import {Button, Container} from "@material-ui/core";
import Avatar from "@material-ui/core/Avatar";
import SupervisorAccountRoundedIcon from '@material-ui/icons/SupervisorAccountRounded';
import Typography from "@material-ui/core/Typography";
import TextField from "@material-ui/core/TextField";
import "./JoinCreateRoom.scss";
import CollapsableAlert, {AlertContentObject} from "../utils/CollapsableAlert";
import {joinRoom} from "../../api/lobby";
import {onSubmit, submitWithEnter} from "../../utils/forms";

interface JoinRoomProps {
  roomNameProp?: string,
  isRoute?: boolean,
}

const JoinRoom: FC<JoinRoomProps> = ({roomNameProp, isRoute = true}) => {
  const history = useHistory();
  const [roomName, setRoomName] = useState<string>(roomNameProp != null ? String(roomNameProp) : '');
  const [password, setPassword] = useState<string>("");

  const [response, setResponse] = useState<AlertContentObject>({
    message: '',
    severity: 'error',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>): void => {
    e.target.id === 'roomName' ? setRoomName(e.target.value) : setPassword(e.target.value);
  };

  const submitForm = (): void => {
    if (!roomName) return;
    joinRoom(roomName, password).then(() => {
      setResponse({
        message: `Joining room ${roomName} ...`,
        severity: 'success',
      });
      setTimeout(() => history.push(`/room/${roomName}`), 1000);
    }).catch(err => {
      if (err.response) setResponse({
        message: `${err.response.statusText} (${err.response.status})`,
        severity: 'error',
      });
    });
  };

  const onEnterKeyDown = (e: React.KeyboardEvent): void => submitWithEnter(e, submitForm);

  return (
    <Container component="main" maxWidth="xs">
      <div className={isRoute ? 'room room-route' : 'room room-embedded'}>
        <Avatar className="room-icon">
          <SupervisorAccountRoundedIcon/>
        </Avatar>
        <Typography component="h1" variant="h5">
          Join Room
        </Typography>
        <div className="auth-alert">
          <CollapsableAlert content={response}/>
        </div>
        <form noValidate onSubmit={(e) => onSubmit(e, submitForm)}>
          <div className="room-form">
            <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              id="roomName"
              label="Room Name"
              name="roomName"
              autoFocus
              value={roomName}
              onChange={handleChange}
              onKeyDown={onEnterKeyDown}
            />
            <TextField
              variant="outlined"
              margin="normal"
              fullWidth
              name="password"
              label="Password"
              type="password"
              id="password"
              onChange={handleChange}
              onKeyDown={onEnterKeyDown}
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              color="primary"
              className="room-button"
            >
              Join
            </Button>
          </div>
        </form>
      </div>
    </Container>
  );
};

export default JoinRoom;
