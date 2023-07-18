import React from 'react';
import ReactDOM from 'react-dom/client';
import AuthProvider from './context/authContext';
import {ThemeProvider} from '@mui/material/styles';
import {QueryClient, QueryClientProvider} from "@tanstack/react-query";
import theme from "./theme";
import Router from './routing/Router';
import './main.scss';
import 'react-toastify/dist/ReactToastify.css';
import {ToastContainer} from 'react-toastify';

const queryClient = new QueryClient();

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      <ToastContainer
        position="top-right"
        autoClose={3000}
        pauseOnHover={false}
        pauseOnFocusLoss={false}
      />
      <QueryClientProvider client={queryClient}>
        <AuthProvider>
          <Router/>
        </AuthProvider>
      </QueryClientProvider>
    </ThemeProvider>
  </React.StrictMode>,
);
