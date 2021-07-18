import React, {useState} from "react";
import {Button, Container, CssBaseline} from "@material-ui/core";
import Avatar from "@material-ui/core/Avatar";
import GroupAddRoundedIcon from '@material-ui/icons/GroupAddRounded';
import Typography from "@material-ui/core/Typography";
import TextField from "@material-ui/core/TextField";
import axiosClient from "../../api/axiosClient";
import {useHistory} from "react-router";

const CreateRoom = () => {
  const history = useHistory();
  const [formState, setFormState] = useState<{
    name: string,
    password: string,
    slots: undefined | number
  }>({
    name: '',
    password: '',
    slots: undefined,
  });

  const handleChange = (e: React.BaseSyntheticEvent) => {
    const field = e.target.name;
    setFormState({
      ...formState,
      [field]: e.target.value,
    });
  };

  const handleSubmit = () => {
    axiosClient.post('/api/rooms/', {...formState}).then((res) => {
      console.log(res.data);
      // maybe display popup, freeze and then redirect
      history.push(`/room/${formState.name}`)
    }).catch(err => console.log(err));
  };

  return (
    <Container component="main" maxWidth="xs">
      <CssBaseline/>
      <div className="room">
        <Avatar className="room-icon">
          <GroupAddRoundedIcon/>
        </Avatar>
        <Typography component="h1" variant="h5">
          Create New Room
        </Typography>
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
            color="secondary"
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
