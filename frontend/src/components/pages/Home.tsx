import {FC, Fragment} from "react";
import beers from "../../images/logo.svg";
import {Button} from "@mui/material";
import {logout} from "../../api/auth";
import WrapWithHeader from "../layout/WrapWithHeader";
import "./Home.scss";
import {useNavigate} from "react-router-dom";


const Home: FC = () => {
  const navigate = useNavigate();
  const token = localStorage.getItem('token');

  const redirectTo = (path: string) => navigate(path);

  return (
    <WrapWithHeader>
      <div className="App">
        <div className="App-body">
          <div className="App-logo-wrapper">
            <img className="App-logo" src={beers} alt="logo"/>
            <span className="App-title">Beerdegu</span>
          </div>

          <div className="App-button-group">
            {token !== null ? (
              <Fragment>
                <Button variant="contained" color="primary" onClick={() => redirectTo('/join')}>
                  Join Room
                </Button>

                <Button variant="contained" color="error" onClick={() => redirectTo('/create')}>
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
                <Button variant="contained" color="primary" onClick={() => redirectTo('/login')}>
                  Login
                </Button>

                <Button variant="contained" color="error" onClick={() => redirectTo('/register')}>
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
