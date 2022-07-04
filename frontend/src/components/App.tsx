import Router from "../routing/Router";
import {ThemeProvider, createTheme} from '@mui/material/styles';
import {QueryClient, QueryClientProvider} from "react-query";

const theme = createTheme();
const queryClient = new QueryClient();

function App() {
  return (
    <ThemeProvider theme={theme}>
      <QueryClientProvider client={queryClient}>
        <Router/>
      </QueryClientProvider>
    </ThemeProvider>
  );
}

export default App;
