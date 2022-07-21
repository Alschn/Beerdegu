import React, {FC, useState} from "react";
import {Button, Container, Grid, Link as MuiLink} from "@mui/material";
import {Link, useNavigate} from "react-router-dom";
import Avatar from "@mui/material/Avatar";
import Typography from "@mui/material/Typography";
import TextField from "@mui/material/TextField";
import LockOpenOutlinedIcon from '@mui/icons-material/LockOpenOutlined';
import {onLogin} from "../../api/auth";
import CollapsableAlert, {AlertContentObject} from "../utils/CollapsableAlert";
import {onSubmit, submitWithEnter} from "../../utils/forms";


const Login: FC = () => {
  const navigate = useNavigate();

  const [username, setUsername] = useState<string>("");
  const [password, setPassword] = useState<string>("");

  const [response, setResponse] = useState<AlertContentObject>({
    message: "",
    severity: "error",
  });

  const submitForm = (): void => {
    onLogin({
      username: username,
      password: password,
    }).then(({data}) => {
      const {key} = data;
      setResponse(
        {message: 'Logged in! Redirecting to home page ...', severity: 'success'}
      );
      localStorage.setItem('token', key);
      setTimeout(() => navigate("/"), 800);
    }).catch(err => {
      if (err.response) setResponse({
        message: `${err.response.statusText} (${err.response.status})`,
        severity: 'error',
      });
    });
  };

  const handleChange = (e: React.BaseSyntheticEvent) => {
    switch (e.target.id) {
      case 'username':
        setUsername(e.target.value);
        break;
      case 'password':
        setPassword(e.target.value);
        break;
      default:
        break;
    }
  };

  const onEnterKeyDown = (e: React.KeyboardEvent): void => submitWithEnter(e, submitForm);

  return (
    <Container component="main" maxWidth="xs">
      <div className="auth">
        <Avatar className="auth-icon">
          <LockOpenOutlinedIcon/>
        </Avatar>
        <Typography component="h1" variant="h5">
          Sign in
        </Typography>
        <div className="auth-alert">
          <CollapsableAlert content={response}/>
        </div>
        <form noValidate onSubmit={(e) => onSubmit(e, submitForm)}>
          <div className="auth-form">
            <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              id="username"
              label="User Name"
              name="username"
              autoFocus
              onChange={handleChange}
            />
            <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              name="password"
              label="Password"
              type="password"
              id="password"
              autoComplete="current-password"
              onChange={handleChange}
              onKeyDown={onEnterKeyDown}
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              color="primary"
              className="auth-button"
              onKeyDown={onEnterKeyDown}
            >
              Sign In
            </Button>
            <Grid container justifyContent="space-between">
              <Grid item>
                <Link to="/password/reset/">
                  <MuiLink variant="body2">
                    Forgot Password?
                  </MuiLink>
                </Link>
              </Grid>

              <Grid item>
                <Link to="/register/">
                  <MuiLink variant="body2">
                    Don't have an account? Sign Up
                  </MuiLink>
                </Link>
              </Grid>
            </Grid>
          </div>
        </form>
      </div>
    </Container>
  );
};

export default Login;
