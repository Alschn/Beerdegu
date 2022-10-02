import {FC, Fragment} from "react";
import beers from "../../images/logo.svg";
import {Button} from "@mui/material";
import WrapWithHeader from "../layout/WrapWithHeader";
import {useNavigate} from "react-router-dom";
import {useAuth} from "../../context/authContext";
import "./Home.scss";


const Home: FC = () => {
  const navigate = useNavigate();
  const {isAuthenticated, logout} = useAuth();

  return (
    <WrapWithHeader>
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
    </WrapWithHeader>
  );
};

export default Home;
