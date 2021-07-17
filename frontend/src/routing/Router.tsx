import React, {FC} from "react";
import {BrowserRouter, Route, Switch} from "react-router-dom";
import Home from "../components/Home";
import Room from "../components/Room";
import PageNotFound from "./PageNotFound";
import Login from "../components/auth/Login";
import Register from "../components/auth/Register";
import PrivateRoute from "./PrivateRoute";
import AuthRoute from "./AuthRoute";

const Router: FC = () => {
  return (
    <BrowserRouter>
      <Switch>
        <Route exact path="/" component={Home}/>

        <AuthRoute exact path="/login" component={Login}/>
        <AuthRoute exact path="/register" component={Register}/>

        <PrivateRoute exact path="/room/:code" component={Room}/>

        <Route path="*" component={PageNotFound}/>
      </Switch>
    </BrowserRouter>
  )
};

export default Router;
