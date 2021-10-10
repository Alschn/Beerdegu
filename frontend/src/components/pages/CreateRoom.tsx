import React, {FC, useState} from "react";
import {Button, Container, CssBaseline} from "@material-ui/core";
import Avatar from "@material-ui/core/Avatar";
import GroupAddRoundedIcon from '@material-ui/icons/GroupAddRounded';
import Typography from "@material-ui/core/Typography";
import TextField from "@material-ui/core/TextField";
import {useHistory} from "react-router";
import CollapsableAlert, {AlertContentObject} from "../utils/CollapsableAlert";
import {createRoom} from "../../api/lobby";
import type {createRoomForm} from "../../api/lobby";

interface CreateRoomProps {
  isRoute?: boolean,
}

const CreateRoom: FC<CreateRoomProps> = ({isRoute = true}) => {
  const history = useHistory();

  const [formState, setFormState] = useState<createRoomForm>({
    name: '',
    password: '',
    slots: undefined,
  });

  const [response, setResponse] = useState<AlertContentObject>({
    message: '',
    severity: 'error',
  });

  const handleChange = (e: React.BaseSyntheticEvent): void => {
    const field = e.target.name;
    setFormState({
      ...formState,
      [field]: e.target.value,
    });
  };

  const handleSubmit = (): void => {
    createRoom(formState).then(() => {
      setResponse({
        message: `Created room ${formState.name}! Redirecting ...`,
        severity: 'success',
      });
      setTimeout(() => history.push(`/room/${formState.name}`), 1000);
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
      <div className={isRoute ? 'room room-route' : 'room room-embedded'}>
        <Avatar className="room-icon">
          <GroupAddRoundedIcon/>
        </Avatar>
        <Typography component="h1" variant="h5">
          Create New Room
        </Typography>
        <div className="room-alert">
          <CollapsableAlert content={response}/>
        </div>
        <div className="room-form">
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            id="name"
            label="Room Name"
            name="name"
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
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            name="slots"
            label="Slots"
            type="number"
            id="slots"
            error={
              formState.slots !== undefined &&
              (formState.slots <= 0 || formState.slots > 10)
            }
            InputProps={{
              inputProps: {min: 1, max: 10}
            }}
            onChange={handleChange}
          />
          <Button
            fullWidth
            variant="contained"
            color="primary"
            className="room-button"
            onClick={handleSubmit}
          >
            Create
          </Button>
        </div>
      </div>
    </Container>
  );
};

export default CreateRoom;
