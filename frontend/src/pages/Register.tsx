import {FC, FormEvent, useState} from 'react';
import {Avatar, Button, Container, Grid, Link as MuiLink, TextField, Typography} from '@mui/material';
import {Link, useNavigate} from "react-router-dom";
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import "./Auth.scss";
import CollapsableAlert, {AlertContentObject} from "../components/utils/CollapsableAlert";
import {onRegister} from "../api/auth";


const validateEmail = (email: string): boolean => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
};

const Register: FC = () => {
  const navigate = useNavigate();

  const [username, setUsername] = useState<string>("");
  const [email, setEmail] = useState<string>("");
  const [password1, setPassword1] = useState<string>("");
  const [password2, setPassword2] = useState<string>("");

  const [response, setResponse] = useState<AlertContentObject>({
    message: '',
  });

  const submitForm = (e: FormEvent): void => {
    e.preventDefault();

    onRegister({
      username: username,
      email: email,
      password1: password1,
      password2: password2,
    }).then(() => {
      setResponse({
        message: 'Created account! Redirecting to login page...',
        severity: 'success',
      });
      setTimeout(() => navigate("/auth/login"), 1000);
    }).catch(err => {
      if (err.response) setResponse({
        message: `${err.response.statusText} (${err.response.status})`,
        severity: 'error',
      });
    });
  };

  const passwordsMatch = password1 === password2;

  return (
    <Container component="main" maxWidth="xs">
      <div className="auth">
        <Avatar className="auth-icon">
          <LockOutlinedIcon/>
        </Avatar>
        <Typography component="h1" variant="h5">
          Sign up
        </Typography>
        <div className="auth-alert">
          <CollapsableAlert content={response}/>
        </div>
        <form className="auth-form" onSubmit={submitForm}>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField
                autoComplete="uname"
                name="User Name"
                variant="outlined"
                required
                fullWidth
                id="username"
                label="User Name"
                autoFocus
                onChange={(e) => setUsername(e.target.value)}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                variant="outlined"
                required
                fullWidth
                id="email"
                label="Email Address"
                name="email"
                autoComplete="email"
                type="email"
                onChange={(e) => setEmail(e.target.value)}
                error={email !== "" && !validateEmail(email)}
                helperText={
                  email !== "" && !validateEmail(email) && "Invalid email format"
                }
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                variant="outlined"
                required
                fullWidth
                name="password"
                label="Password"
                type="password"
                id="password1"
                autoComplete="current-password"
                onChange={(e) => setPassword1(e.target.value)}
                error={!passwordsMatch}
                helperText={
                  !passwordsMatch && "Passwords don't match"
                }
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                variant="outlined"
                required
                fullWidth
                name="password2"
                label="Confirm password"
                type="password"
                id="password2"
                autoComplete="current-password"
                onChange={(e) => setPassword2(e.target.value)}
                error={!passwordsMatch}
                helperText={
                  !passwordsMatch && "Passwords don't match"
                }
              />
            </Grid>
          </Grid>
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="primary"
            className="auth-button"
          >
            Sign Up
          </Button>
          <Grid container justifyContent="flex-end">
            <Grid item>
              <Link to="/auth/login/">
                <MuiLink variant="body2">
                  Already have an account? Sign in
                </MuiLink>
              </Link>
            </Grid>
          </Grid>
        </form>
      </div>
    </Container>
  );
};

export default Register;
