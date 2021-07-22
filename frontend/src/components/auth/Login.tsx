import React, {FC, useState} from "react";
import {Button, Container, CssBaseline, Grid, Link} from "@material-ui/core";
import Avatar from "@material-ui/core/Avatar";
import Typography from "@material-ui/core/Typography";
import TextField from "@material-ui/core/TextField";
import LockOpenOutlinedIcon from '@material-ui/icons/LockOpenOutlined';
import {onLogin} from "../../api/auth";
import {useHistory} from "react-router";
import CollapsableAlert, {AlertContentObject} from "../utils/CollapsableAlert";
import "./Auth.scss";


const Login: FC = () => {
  const history = useHistory();

  const [username, setUsername] = useState<string>("");
  const [password, setPassword] = useState<string>("");

  const [response, setResponse] = useState<AlertContentObject>({
    message: "",
    severity: "error",
  });

  const handleSubmit = (e: React.BaseSyntheticEvent) => {
    e.preventDefault();
    onLogin({
      username: username,
      password: password,
    }).then(({data}) => {
      const {key} = data;
      setResponse(
        {message: 'Logged in! Redirecting to home page ...', severity: 'success'}
      );
      localStorage.setItem('token', key);
      setTimeout(() => history.push("/"), 800)
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

  return (
    <Container component="main" maxWidth="xs">
      <CssBaseline/>
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
          />
          <Button
            fullWidth
            variant="contained"
            color="primary"
            className="auth-button"
            onClick={handleSubmit}
          >
            Sign In
          </Button>
          <Grid container justifyContent="flex-end">
            <Grid item>
              <Link href="/register/" variant="body2">
                Don't have an account? Sign Up
              </Link>
            </Grid>
          </Grid>
        </div>
      </div>
    </Container>
  );
};

export default Login;
