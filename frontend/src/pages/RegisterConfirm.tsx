import {useNavigate, useSearchParams} from "react-router-dom";
import {CircularProgress, Container, Typography} from "@mui/material";
import "./Auth.scss";
import {useEffect} from "react";
import {useMutation} from "@tanstack/react-query";
import {confirmRegister} from "../api/auth";
import {toast} from "react-toastify";
import {AxiosError} from "axios";
import CollapsableAlert from "../components/utils/CollapsableAlert";

const useRegisterConfirmMutation = () => {
  const navigate = useNavigate();

  return useMutation({
    mutationFn: (data: { key: string }) => confirmRegister(data.key),
    onSuccess: () => {
      toast.success('Account created! Redirecting to login page...');
      navigate('/auth/login');
    },
    onError: (err) => {
      if (err instanceof AxiosError) {
        toast.error('Invalid or expired link');
        return;
      }
      toast.error('Something went wrong');
    }
  });
};

export default function RegisterConfirm() {
  const [searchParams] = useSearchParams();
  const key = searchParams.get('key');

  const mutation = useRegisterConfirmMutation();

  useEffect(() => {
    if (!key) return;
    mutation.mutate({key});
  }, [key]);

  if (mutation.isLoading || mutation.isSuccess) return (
    <Container component="main" maxWidth="xs">
      <div className="auth">
        <CircularProgress/>
      </div>
    </Container>
  );

  if (!key || mutation.isError) return (
    <Container component="main" maxWidth="xs">
      <div className="auth">
        <Typography component="h1" variant="h5">
          Invalid or expired link
        </Typography>
        <div className="auth-alert">
          {mutation.isError && (
            <CollapsableAlert
              content={{
                message: 'Failed to confirm registration',
                severity: 'error',
              }}
            />
          )}
        </div>
      </div>
    </Container>
  );

  return null;
}
