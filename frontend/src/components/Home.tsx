import React, {FC, Fragment} from "react";
import beers from "../images/logo.svg";
import "./Home.scss";
import {Button} from "@material-ui/core";
import {useHistory} from "react-router";

const Home: FC = () => {
  const history = useHistory();
  const token = localStorage.getItem('token');

  const redirectTo = (path: string) => history.push(path);

  return (
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
                Join
              </Button>

              <Button variant="contained" color="secondary" onClick={() => redirectTo('/create')}>
                Create
              </Button>
            </Fragment>
          ) : (
            <Fragment>
              <Button variant="contained" color="primary" onClick={() => redirectTo('/login')}>
                Login
              </Button>

              <Button variant="contained" color="secondary" onClick={() => redirectTo('/register')}>
                Register
              </Button>
            </Fragment>
          )}
        </div>
      </div>
    </div>
  );
};

export default Home;
