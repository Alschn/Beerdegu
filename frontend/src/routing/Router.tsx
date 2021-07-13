import React, {FC} from "react";
import {BrowserRouter, Route, Switch} from "react-router-dom";
import Home from "../components/Home";
import Room from "../components/Room";
import PageNotFound from "./PageNotFound";
import Login from "../components/auth/Login";
import Register from "../components/auth/Register";

const Router: FC = () => {
  return (
    <BrowserRouter>
      <Switch>
        <Route exact path="/" component={Home}/>

        <Route exact path="/login" component={Login}/>
        <Route exact path="/register" component={Register}/>

        <Route exact path="/room/:code" component={Room}/>

        <Route path="*" component={PageNotFound}/>
      </Switch>
    </BrowserRouter>
  )
};

export default Router;
