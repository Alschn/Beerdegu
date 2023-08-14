import {BaseSyntheticEvent, FC, FormEvent, useState} from "react";
import {Avatar, Container, TextField, Typography} from "@mui/material";
import GroupAddRoundedIcon from '@mui/icons-material/GroupAddRounded';
import {useNavigate} from "react-router-dom";
import CollapsableAlert, {AlertContentObject} from "../components/utils/CollapsableAlert";
import {createRoom, CreateRoomPayload} from "../api/rooms";
import {useMutation} from "@tanstack/react-query";
import {AxiosError} from "axios";
import {LoadingButton} from "@mui/lab";

const MAX_ROOM_NAME_LENGTH = 8;

interface CreateRoomProps {
  isRoute?: boolean,
}


const CreateRoom: FC<CreateRoomProps> = ({isRoute = true}) => {
  const navigate = useNavigate();

  const [name, setName] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [slots, setSlots] = useState<number | undefined>(undefined);

  const [response, setResponse] = useState<AlertContentObject>({
    message: '',
    severity: 'error',
  });

  const mutation = useMutation({
    mutationFn: (data: CreateRoomPayload) => createRoom(data),
    onSuccess: (_, variables) => {
      setResponse({
        message: `Created room ${variables.name}! Redirecting ...`,
        severity: 'success',
      });
      setTimeout(() => navigate(`/room/${variables.name}`), 1000);
    },
    onError: (err) => {
      if (!(err instanceof AxiosError)) return;
      if (err?.response?.data && err?.response.data?.host) {
        setResponse({
          message: 'You are already hosting a room that has not been finished!',
          severity: 'error',
        });
        return;
      }
      if (err?.response?.data && err?.response.data?.name) {
        setResponse({
          message: 'Room name is not unique or restricted!',
          severity: 'error',
        });
        return;
      }
      if (err.response) {
        setResponse({
          message: `${err.response.statusText} (${err.response.status})`,
          severity: 'error',
        });
        return;
      }
    }
  });

  const handleChangeName = (e: BaseSyntheticEvent) => {
    setName(e.target.value.toLowerCase());
  };

  const handleChangePassword = (e: BaseSyntheticEvent) => setPassword(e.target.value);

  const handleChangeSlots = (e: BaseSyntheticEvent) => setSlots(e.target.value);

  const handleSubmit = (e: FormEvent<HTMLFormElement>): void => {
    e.preventDefault();
    mutation.mutate({
      name: name,
      password: password,
      slots: slots,
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
        <form onSubmit={handleSubmit}>
          <div className="room-form">
            <TextField
              id="name"
              name="name"
              label="Room Name"
              helperText={`Name must be unique, lowercase, up to ${MAX_ROOM_NAME_LENGTH} characters`}
              variant="outlined"
              margin="normal"
              value={name}
              onChange={handleChangeName}
              InputProps={{
                inputProps: {maxLength: MAX_ROOM_NAME_LENGTH}
              }}
              required
              fullWidth
              autoFocus
            />
            <TextField
              id="password"
              name="password"
              type="password"
              label="Password"
              helperText="Leave blank if password is not required"
              variant="outlined"
              margin="normal"
              value={password}
              onChange={handleChangePassword}
              fullWidth
            />
            <TextField
              id="slots"
              name="slots"
              type="number"
              label="Slots"
              helperText="Maximum number of participants including host"
              variant="outlined"
              margin="normal"
              error={
                slots !== undefined &&
                (slots <= 0 || slots > 10)
              }
              InputProps={{
                inputProps: {min: 1, max: 10}
              }}
              value={slots}
              onChange={handleChangeSlots}
              required
              fullWidth
            />
            <LoadingButton
              type="submit"
              fullWidth
              variant="contained"
              color="primary"
              className="room-button"
              disabled={mutation.isSuccess}
              loading={mutation.isLoading}
            >
              Create
            </LoadingButton>
          </div>
        </form>
      </div>
    </Container>
  );
};

export default CreateRoom;
