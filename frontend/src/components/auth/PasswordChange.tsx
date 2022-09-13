import {useNavigate} from "react-router-dom";
import React, {BaseSyntheticEvent, FC, FormEvent, useMemo, useState} from "react";
import CollapsableAlert, {AlertContentObject} from "../utils/CollapsableAlert";
import {changePassword} from "../../api/auth";
import {Button, Container} from "@mui/material";
import Avatar from "@mui/material/Avatar";
import LockOpenOutlinedIcon from "@mui/icons-material/LockOpenOutlined";
import Typography from "@mui/material/Typography";
import TextField from "@mui/material/TextField";
import "./Auth.scss";

const MIN_PASSWORD_LENGTH = 8;  // enforced by API

const PasswordChange: FC = () => {
  const navigate = useNavigate();

  const [oldPassword, setOldPassword] = useState<string>("");
  const [newPassword1, setNewPassword1] = useState<string>("");
  const [newPassword2, setNewPassword2] = useState<string>("");

  const [response, setResponse] = useState<AlertContentObject>({
    message: "",
    severity: "error",
  });

  const submitForm = (e: FormEvent): void => {
    e.preventDefault();

    changePassword({
      old_password: oldPassword,
      new_password1: newPassword1,
      new_password2: newPassword2
    }).then((res) => {
      setResponse({
        message: 'Successfully changed password! Redirecting to homepage ...',
        severity: 'success'
      });
      setTimeout(() => navigate("/login"), 1000);
    }).catch(err => {
      if (err.response) setResponse({
        message: `${err.response.statusText} (${err.response.status})`,
        severity: 'error',
      });
    });
  };

  const handleChange = (e: BaseSyntheticEvent) => {
    switch (e.target.id) {
      case 'old_password':
        setOldPassword(e.target.value);
        break;

      case 'new_password1':
        setNewPassword1(e.target.value);
        break;

      case 'new_password2':
        setNewPassword2(e.target.value);
        break;

      default:
        break;
    }
  };

  const helperText = useMemo(() => {
    if (oldPassword !== "" && (oldPassword === newPassword1 || oldPassword === newPassword2)) {
      return "New password has to be different than the old one";
    } else if (newPassword1 !== newPassword2) {
      return "Passwords do not match!";
    } else if (
      (newPassword1 && newPassword1.length < MIN_PASSWORD_LENGTH) ||
      (newPassword2 && newPassword2.length < MIN_PASSWORD_LENGTH)
    ) {
      return `New password should be at least ${MIN_PASSWORD_LENGTH} characters long`;
    }
    return "";
  }, [oldPassword, newPassword1, newPassword2]);

  return (
    <Container component="main" maxWidth="xs">
      <div className="auth">
        <Avatar className="auth-icon">
          <LockOpenOutlinedIcon/>
        </Avatar>
        <Typography component="h1" variant="h5">
          Change Password
        </Typography>
        <div className="auth-alert">
          <CollapsableAlert content={response}/>
        </div>
        <form onSubmit={submitForm}>
          <div className="auth-form">
            <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              name="old_password"
              label="Old Password"
              type="password"
              id="old_password"
              autoComplete="current-password"
              onChange={handleChange}
            />
            <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              name="new_password1"
              label="New Password"
              helperText={helperText}
              error={newPassword1 !== "" && (
                newPassword1 !== newPassword2 ||
                newPassword1.length < MIN_PASSWORD_LENGTH ||
                newPassword2.length < MIN_PASSWORD_LENGTH
              )}
              type="password"
              id="new_password1"
              autoComplete="new-password"
              onChange={handleChange}
            />
            <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              name="new_password2"
              label="Confirm New Password"
              helperText={helperText}
              error={newPassword2 !== "" && (
                newPassword1 !== newPassword2 ||
                newPassword1.length < MIN_PASSWORD_LENGTH ||
                newPassword2.length < MIN_PASSWORD_LENGTH
              )}
              type="password"
              id="new_password2"
              autoComplete="new-password"
              onChange={handleChange}
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              color="primary"
              className="auth-button"
            >
              Submit
            </Button>
          </div>
        </form>
      </div>
    </Container>
  );
};

export default PasswordChange;
