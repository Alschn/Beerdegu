import {FC} from "react";
import {BrowserRouter, Route, Routes} from "react-router-dom";
import Home from "../pages/Home";
import Room from "../pages/Room";
import PageNotFound from "./PageNotFound";
import Login from "../pages/Login";
import Register from "../pages/Register";
import JoinRoom from "../pages/JoinRoom";
import CreateRoom from "../pages/CreateRoom";
import Lobby from "../pages/Lobby";
import PrivateRoute from "./PrivateRoute";
import AuthRoute from "./AuthRoute";
import PasswordChange from "../pages/PasswordChange";
import PasswordReset from "../pages/PasswordReset";
import PasswordResetConfirm from "../pages/PasswordResetConfirm";
import RegisterConfirm from "../pages/RegisterConfirm";

const Router: FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route index element={<Home/>}/>

        <Route path="/" element={<PrivateRoute withHeader/>}>
          <Route path="lobby" element={<Lobby/>}/>
          <Route path="join" element={<JoinRoom/>}/>
          <Route path="create" element={<CreateRoom/>}/>
          {/*<Route path="browser" element={<Browser/>}/>*/}
          {/*<Route path="profile" element={<Profile/>}/>*/}
          <Route path="password/change" element={<PasswordChange/>}/>
        </Route>

        <Route path="/auth" element={<AuthRoute/>}>
          <Route path="login" element={<Login/>}/>
          <Route path="register" element={<Register/>}/>
          <Route path="register/confirm" element={<RegisterConfirm/>}/>
          <Route path="password/reset" element={<PasswordReset/>}/>
          <Route path="password/reset/confirm" element={<PasswordResetConfirm/>}/>
        </Route>

        <Route path="/" element={<PrivateRoute withHeader={false}/>}>
          <Route path="room/:code" element={<Room/>}/>
        </Route>

        <Route path="*" element={<PageNotFound/>}/>
      </Routes>
    </BrowserRouter>
  );
};

export default Router;
