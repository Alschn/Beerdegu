import React, {FC, useState} from "react";
import axios from "axios";
import logo from "../logo.svg";
import "./Home.scss";

const Home: FC = () => {
  const [textInput, setTextInput] = useState<string>("");
  const [output, setOutput] = useState<string>("");

  const handleSubmit = () => {
    axios.get(`/api/test?text=${textInput}`).then(res => {
      setOutput(res.data.text);
    }).catch(err => console.log(err));
  };

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
        <a href="/room/abcd" className="App-link">Room abcd</a>

        <div>
          <label htmlFor='char-input'>Make this text uppercase: </label>
          <input
            id='char-input' type='text' value={textInput}
            onChange={(e) => setTextInput(e.target.value)}
          />
          <button onClick={handleSubmit}>Submit</button>
          <h3>{output}</h3>
        </div>
      </header>
    </div>
  );
};

export default Home;
