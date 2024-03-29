import {FC, FormEvent, useState} from "react";
import {Avatar, Button, Container, Grid, TextField, Typography} from "@mui/material";
import LockOutlinedIcon from "@mui/icons-material/LockOutlined";
import {useNavigate, useSearchParams} from "react-router-dom";
import CollapsableAlert, {AlertContentObject} from "../components/utils/CollapsableAlert";
import {confirmResetPassword} from "../api/auth";
import EmailIcon from '@mui/icons-material/Email';

const PasswordResetConfirm: FC = () => {
  const navigate = useNavigate();

  // /auth/password/reset/confirm/?uid=<uid>&token=<token>
  const [queryParams] = useSearchParams();
  const userIdParam = queryParams.get('uid');
  const tokenParam = queryParams.get('token');

  const [newPassword1, setNewPassword1] = useState("");
  const [newPassword2, setNewPassword2] = useState("");
  const [response, setResponse] = useState<AlertContentObject>({
    message: '',
  });

  const submitForm = (e: FormEvent): void => {
    e.preventDefault();

    if (!userIdParam || !tokenParam) {
      return;
    }

    confirmResetPassword(userIdParam, tokenParam, {
      new_password1: newPassword1,
      new_password2: newPassword2,
      uid: userIdParam,
      token: tokenParam
    }).then(() => {
      setResponse({
        message: 'Password changed successfully! Redirecting to login page...',
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

  const passwordsMatch = newPassword1 === newPassword2;

  if (!userIdParam || !tokenParam) return (
    <Container component="main" maxWidth="sm">
      <div className="auth">
        <Avatar className="auth-icon">
          <EmailIcon/>
        </Avatar>
        <Typography component="h1" variant="h5">
          Password reset link is invalid or expired!
        </Typography>
        <div className="auth-alert">
          <CollapsableAlert
            content={{
              message: 'Invalid password reset link',
              severity: 'error',
            }}
          />
        </div>
      </div>
    </Container>
  );

  return (
    <Container component="main" maxWidth="xs">
      <div className="auth">
        <Avatar className="auth-icon">
          <LockOutlinedIcon/>
        </Avatar>
        <Typography component="h1" variant="h5">
          New Password
        </Typography>
        <div className="auth-alert">
          <CollapsableAlert content={response}/>
        </div>
        <form className="auth-form" onSubmit={submitForm}>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField
                variant="outlined"
                required
                fullWidth
                name="newPassword1"
                label="Password"
                type="password"
                id="newPassword1"
                autoComplete="current-password"
                onChange={(e) => setNewPassword1(e.target.value)}
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
                name="newPassword2"
                label="Confirm password"
                type="password"
                id="newPassword2"
                autoComplete="current-password"
                onChange={(e) => setNewPassword2(e.target.value)}
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
            Submit
          </Button>
        </form>
      </div>
    </Container>
  );
};

export default PasswordResetConfirm;
