import React, {FC} from "react";
import logo from "../logo.svg";
import "./Home.scss";

const Home: FC = () => {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo"/>
        <p>
          Edit <code>src/App.tsx</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>

        <a href="/login" className="App-link">Login</a>
        <a href="/register" className="App-link">Register</a>
        <a href="/join" className="App-link">Join</a>
        <a href="/create" className="App-link">Create</a>
        <a href="/room/abcd" className="App-link">Room abcd</a>
      </header>
    </div>
  );
};

export default Home;
