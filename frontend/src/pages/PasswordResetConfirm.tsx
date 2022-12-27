import {FC, FormEvent, useState} from "react";
import {useParams} from "react-router";
import {Avatar, Button, Container, Grid, TextField, Typography} from "@mui/material";
import LockOutlinedIcon from "@mui/icons-material/LockOutlined";
import {useNavigate} from "react-router-dom";
import CollapsableAlert, {AlertContentObject} from "../components/utils/CollapsableAlert";
import {confirmResetPassword} from "../api/auth";


const PasswordResetConfirm: FC = () => {
  const navigate = useNavigate();
  const params = useParams<{ user_id: string, token: string }>();

  const [newPassword1, setNewPassword1] = useState("");
  const [newPassword2, setNewPassword2] = useState("");
  const [response, setResponse] = useState<AlertContentObject>({
    message: '',
  });

  const submitForm = (e: FormEvent): void => {
    e.preventDefault();

    if (!params.user_id || !params.token) {
      return;
    }

    confirmResetPassword(params.user_id!, params.token!, {
      new_password1: newPassword1,
      new_password2: newPassword2,
      uid: params.user_id!,
      token: params.token!
    }).then(() => {
      setResponse({
        message: 'Password changed successfully! Redirecting to login page...',
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

  const passwordsMatch = (): boolean => newPassword1 === newPassword2;

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
                name="newPassword2"
                label="Confirm password"
                type="password"
                id="newPassword2"
                autoComplete="current-password"
                onChange={(e) => setNewPassword2(e.target.value)}
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
          >
            Submit
          </Button>
        </form>
      </div>
    </Container>
  );
};

export default PasswordResetConfirm;
