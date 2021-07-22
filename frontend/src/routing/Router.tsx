import React, {FC} from "react";
import {BrowserRouter, Route, Switch} from "react-router-dom";
import Home from "../components/pages/Home";
import Room from "../components/pages/Room";
import PageNotFound from "./PageNotFound";
import Login from "../components/auth/Login";
import Register from "../components/auth/Register";
import PrivateRoute from "./PrivateRoute";
import AuthRoute from "./AuthRoute";
import JoinRoom from "../components/pages/JoinRoom";
import CreateRoom from "../components/pages/CreateRoom";

const Router: FC = () => {
  return (
    <BrowserRouter>
      <Switch>
        <Route exact path="/" component={Home}/>

        <AuthRoute exact path="/login" component={Login}/>
        <AuthRoute exact path="/register" component={Register}/>

        <PrivateRoute exact path="/join" component={JoinRoom}/>
        <PrivateRoute exact path="/create" component={CreateRoom}/>

        <PrivateRoute exact path="/room/:code" component={Room}/>

        <Route path="*" component={PageNotFound}/>
      </Switch>
    </BrowserRouter>
  )
};

export default Router;
