import {FC, useState} from 'react';
import {Avatar, Button, Container, Grid, Link, TextField, Typography} from '@mui/material';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import {onRegister} from "../../api/auth";
import CollapsableAlert, {AlertContentObject} from "../utils/CollapsableAlert";
import {onSubmit, submitWithEnter} from '../../utils/forms';
import "./Auth.scss";
import {useNavigate} from "react-router-dom";


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

  const submitForm = (): void => {
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
      setTimeout(() => navigate("/login"), 1000);
    }).catch(err => {
      if (err.response) setResponse({
        message: `${err.response.statusText} (${err.response.status})`,
        severity: 'error',
      });
    });
  };

  const passwordsMatch = (): boolean => password1 === password2;

  const onEnterKeyDown = (e: React.KeyboardEvent): void => submitWithEnter(e, submitForm);

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
        <form className="auth-form" noValidate onSubmit={(e) => onSubmit(e, submitForm)}>
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
                onKeyDown={onEnterKeyDown}
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
                onKeyDown={onEnterKeyDown}
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
                error={!passwordsMatch()}
                helperText={
                  !passwordsMatch() && "Passwords don't match"
                }
                onKeyDown={onEnterKeyDown}
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
                error={!passwordsMatch()}
                helperText={
                  !passwordsMatch() && "Passwords don't match"
                }
                onKeyDown={onEnterKeyDown}
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
              <Link href="/login/" variant="body2">
                Already have an account? Sign in
              </Link>
            </Grid>
          </Grid>
        </form>
      </div>
    </Container>
  );

};

export default Register;
