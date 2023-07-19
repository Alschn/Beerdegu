import {BaseSyntheticEvent, FC, FormEvent, useState} from "react";
import {Button, Container} from "@mui/material";
import Avatar from "@mui/material/Avatar";
import LockResetIcon from '@mui/icons-material/LockReset';
import Typography from "@mui/material/Typography";
import TextField from "@mui/material/TextField";
import "./Auth.scss";
import CollapsableAlert, {AlertContentObject} from "../components/utils/CollapsableAlert";
import {resetPassword} from "../api/auth";


const PasswordReset: FC = () => {
  const [email, setEmail] = useState<string>("");
  const [response, setResponse] = useState<AlertContentObject>({
    message: "",
  });

  const handleChange = (e: BaseSyntheticEvent) => setEmail(e.target.value);

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();

    resetPassword({email}).then((res) => {
      setResponse({
        message: `Sent a password reset link to ${email}`,
        severity: 'info'
      });
    }).catch(err => {
      if (err.response) setResponse({
        message: `${err.response.statusText} (${err.response.status})`,
        severity: 'error',
      });
    });
  };

  return (
    <Container component="main" maxWidth="xs">
      <div className="auth">
        <Avatar className="auth-icon">
          <LockResetIcon/>
        </Avatar>

        <Typography component="h1" variant="h5" marginBottom={2}>
          Reset Password
        </Typography>
        {response.severity !== "success" && (
          <Typography component="p" variant="subtitle1">
            Link will be sent to you via email
          </Typography>
        )}

        <div className="auth-alert">
          <CollapsableAlert content={response}/>
        </div>

        {response.severity !== "success" && (
          <form onSubmit={handleSubmit}>
            <div className="auth-form">
              <TextField
                variant="outlined"
                margin="normal"
                required
                fullWidth
                name="email"
                label="Email"
                type="email"
                id="email"
                autoComplete="email"
                value={email}
                onChange={handleChange}
              />
              <Button
                type="submit"
                fullWidth
                variant="contained"
                color="primary"
                className="auth-button"
              >
                Reset
              </Button>
            </div>
          </form>
        )}
      </div>
    </Container>
  );
};

export default PasswordReset;
