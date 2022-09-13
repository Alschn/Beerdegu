import {BaseSyntheticEvent, FC, FormEvent, useState} from "react";
import {Avatar, Button, Container, TextField, Typography} from "@mui/material";
import GroupAddRoundedIcon from '@mui/icons-material/GroupAddRounded';
import CollapsableAlert, {AlertContentObject} from "../utils/CollapsableAlert";
import type {createRoomForm} from "../../api/lobby";
import {createRoom} from "../../api/lobby";
import {useNavigate} from "react-router-dom";

interface CreateRoomProps {
  isRoute?: boolean,
}

const CreateRoom: FC<CreateRoomProps> = ({isRoute = true}) => {
  const navigate = useNavigate();

  const [formState, setFormState] = useState<createRoomForm>({
    name: '',
    password: '',
    slots: undefined,
  });

  const [response, setResponse] = useState<AlertContentObject>({
    message: '',
    severity: 'error',
  });

  const handleChange = (e: BaseSyntheticEvent): void => {
    const field = e.target.name;
    setFormState({
      ...formState,
      [field]: e.target.value,
    });
  };

  const submitForm = (e: FormEvent<HTMLFormElement>): void => {
    e.preventDefault();

    createRoom(formState).then(() => {
      setResponse({
        message: `Created room ${formState.name}! Redirecting ...`,
        severity: 'success',
      });
      setTimeout(() => navigate(`/room/${formState.name}`), 1000);
    }).catch(err => {
      if (err.response) setResponse({
        message: `${err.response.statusText} (${err.response.status})`,
        severity: 'error',
      });
    });
  };

  return (
    <Container component="main" maxWidth="xs">
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
        <form onSubmit={submitForm}>
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
              type="submit"
              fullWidth
              variant="contained"
              color="primary"
              className="room-button"
            >
              Create
            </Button>
          </div>
        </form>
      </div>
    </Container>
  );
};

export default CreateRoom;
