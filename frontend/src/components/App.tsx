import React from 'react';
import Router from "../routing/Router";
import {ThemeProvider, createTheme} from '@mui/material/styles';

const theme = createTheme();

function App() {
  return (
    <ThemeProvider theme={theme}>
      <Router/>
    </ThemeProvider>
  );
}

export default App;
