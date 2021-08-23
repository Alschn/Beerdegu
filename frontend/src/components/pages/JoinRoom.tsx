import React, {FC, useState} from "react";
import {useHistory} from "react-router";
import {Button, Container, CssBaseline} from "@material-ui/core";
import Avatar from "@material-ui/core/Avatar";
import SupervisorAccountRoundedIcon from '@material-ui/icons/SupervisorAccountRounded';
import Typography from "@material-ui/core/Typography";
import TextField from "@material-ui/core/TextField";
import "./JoinCreateRoom.scss";
import CollapsableAlert, {AlertContentObject} from "../utils/CollapsableAlert";
import useAxios from "../../hooks/useAxios";

const JoinRoom: FC = () => {
  const history = useHistory();
  const [roomName, setRoomName] = useState<string>("");
  const [password, setPassword] = useState<string>("");

  const {put} = useAxios();

  const [response, setResponse] = useState<AlertContentObject>({
    message: '',
    severity: 'error',
  })

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.target.id === 'roomName' ? setRoomName(e.target.value) : setPassword(e.target.value);
  };

  const handleSubmit = () => {
    put(`/api/rooms/${roomName}/join`, {
      'name': roomName,
      'password': password,
    }).then(() => {
      setResponse({
        message: `Joining room ${roomName} ...`,
        severity: 'success',
      })
      setTimeout(() => history.push(`/room/${roomName}`), 1000)
    }).catch(err => {
      if (err.response) setResponse({
        message: `${err.response.statusText} (${err.response.status})`,
        severity: 'error',
      });
    });
  };

  return (
    <Container component="main" maxWidth="xs">
      <CssBaseline/>
      <div className="room">
        <Avatar className="room-icon">
          <SupervisorAccountRoundedIcon/>
        </Avatar>
        <Typography component="h1" variant="h5">
          Join Room
        </Typography>
        <div className="auth-alert">
          <CollapsableAlert content={response}/>
        </div>
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
            onChange={handleChange}
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
          />
          <Button
            fullWidth
            variant="contained"
            color="primary"
            className="room-button"
            onClick={handleSubmit}
          >
            Join
          </Button>
        </div>
      </div>
    </Container>
  );
};

export default JoinRoom;
