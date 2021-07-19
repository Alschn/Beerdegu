import React, {FC, useState} from "react";
import axiosClient from "../../api/axiosClient";
import {useHistory} from "react-router";
import {Button, Container, CssBaseline} from "@material-ui/core";
import Avatar from "@material-ui/core/Avatar";
import SupervisorAccountRoundedIcon from '@material-ui/icons/SupervisorAccountRounded';
import Typography from "@material-ui/core/Typography";
import TextField from "@material-ui/core/TextField";
import "./JoinCreateRoom.scss";

const JoinRoom: FC = () => {
  const history = useHistory();
  const [roomName, setRoomName] = useState<string>("");
  const [password, setPassword] = useState<string>("");

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.target.id === 'roomName' ? setRoomName(e.target.value) : setPassword(e.target.value);
  };

  const handleSubmit = () => {
    axiosClient.put(`/api/rooms/${roomName}/join`, {
      'name': roomName,
      'password': password,
    }).then(() => {
      history.push(`/room/${roomName}`);
    }).catch(err => console.log(err));
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
