import React from 'react';
import ReactDOM from 'react-dom/client';
import AuthProvider from "./context/AuthContext";
import {ThemeProvider} from '@mui/material/styles';
import {QueryClient, QueryClientProvider} from "@tanstack/react-query";
import theme from "./theme";
import Router from "./routing/Router";
import "./main.scss";
import 'react-toastify/dist/ReactToastify.css';

const queryClient = new QueryClient();

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      <QueryClientProvider client={queryClient}>
        <AuthProvider>
          <Router/>
        </AuthProvider>
      </QueryClientProvider>
    </ThemeProvider>
  </React.StrictMode>,
);
