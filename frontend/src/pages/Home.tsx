import {FC, Fragment} from "react";
import beers from "../assets/logo.svg";
import {Button} from "@mui/material";
import {useNavigate} from "react-router-dom";
import "./Home.scss";
import MainLayout from "../components/layout/MainLayout";
import {useAuth} from "../context/AuthContext";


const Home: FC = () => {
  const navigate = useNavigate();
  const {isAuthenticated, logout} = useAuth();

  return (
    <MainLayout>
      <div className="App">
        <div className="App-body">
          <div className="App-logo-wrapper">
            <img className="App-logo" src={beers} alt="logo"/>
            <span className="App-title">Beerdegu</span>
          </div>

          <div className="App-button-group">
            {isAuthenticated ? (
              <Fragment>
                <Button variant="contained" color="primary" onClick={() => navigate('/join')}>
                  Join Room
                </Button>

                <Button variant="contained" color="error" onClick={() => navigate('/create')}>
                  Create Room
                </Button>

                <Button
                  variant="contained" color="secondary" onClick={logout}
                  className="App-button-logout"
                >
                  Logout
                </Button>
              </Fragment>
            ) : (
              <Fragment>
                <Button variant="contained" color="primary" onClick={() => navigate('/login')}>
                  Login
                </Button>

                <Button variant="contained" color="error" onClick={() => navigate('/register')}>
                  Register
                </Button>
              </Fragment>
            )}
          </div>
        </div>
      </div>
    </MainLayout>
  );
};

export default Home;
