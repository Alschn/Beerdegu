import Router from "../routing/Router";
import theme from "../theme";
import {ThemeProvider} from '@mui/material/styles';
import {QueryClient, QueryClientProvider} from "react-query";

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
