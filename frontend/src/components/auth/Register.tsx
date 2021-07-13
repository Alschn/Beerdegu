import React, {FC, useCallback, useEffect, useState} from 'react';
import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
import Link from '@material-ui/core/Link';
import Grid from '@material-ui/core/Grid';
import LockOutlinedIcon from '@material-ui/icons/LockOutlined';
import Typography from '@material-ui/core/Typography';
import Container from '@material-ui/core/Container';
import "./Auth.scss";
import {Collapse} from '@material-ui/core';
import {Alert} from '@material-ui/lab';
import {onRegister} from "../../api/auth";

const validateEmail = (email: string): boolean => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
};

const Register: FC = () => {
  const [username, setUsername] = useState<string>("");
  const [email, setEmail] = useState<string>("");
  const [password1, setPassword1] = useState<string>("");
  const [password2, setPassword2] = useState<string>("");

  const [errorMessage, setErrorMessage] = useState<string>("");

  const [btnDisabled, setBtnDisabled] = useState<boolean>(true);

  const isFormFilled = useCallback(() => {
    return username.length !== 0
      && validateEmail(email)
      && password1.length !== 0
      && password1 === password2;
  }, [username, password1, password2, email])

  useEffect(() => {
    isFormFilled() && setBtnDisabled(false);
  }, [isFormFilled])

  const handleSubmit = (e: React.BaseSyntheticEvent): void => {
    e.preventDefault();
    onRegister({
      username: username,
      email: email,
      password1: password1,
      password2: password2,
    }).then(res => {
      console.log(res);
    }).catch(err => console.log(err))
  }

  const passwordsMatch = (): boolean => password1 === password2;

  return (
    <Container component="main" maxWidth="xs">
      <CssBaseline/>
      <div className="auth">
        <Avatar className="auth-icon">
          <LockOutlinedIcon/>
        </Avatar>
        <Typography component="h1" variant="h5">
          Sign up
        </Typography>
        <div className="auth-alert">
          <Collapse in={errorMessage !== ""}>
            {errorMessage && (
              <Alert
                severity="error"
                onClose={() => setErrorMessage("")}
              >
                {errorMessage}
              </Alert>
            )}
          </Collapse>
        </div>

        <form className="auth-form" noValidate onSubmit={handleSubmit}>
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
                error={!passwordsMatch()}
                helperText={
                  !passwordsMatch() && "Passwords don't match"
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
                error={!passwordsMatch()}
                helperText={
                  !passwordsMatch() && "Passwords don't match"
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
            disabled={btnDisabled}
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
