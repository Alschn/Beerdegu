import {FC} from "react";
import {BrowserRouter, Route, Routes} from "react-router-dom";
import Home from "../components/pages/Home";
import Room from "../components/pages/Room";
import PageNotFound from "./PageNotFound";
import Login from "../components/auth/Login";
import Register from "../components/auth/Register";
import JoinRoom from "../components/pages/JoinRoom";
import CreateRoom from "../components/pages/CreateRoom";
import Lobby from "../components/pages/Lobby";
import PrivateRoute from "./PrivateRoute";
import AuthRoute from "./AuthRoute";
import PasswordChange from "../components/auth/PasswordChange";
import PasswordReset from "../components/auth/PasswordReset";
import PasswordResetConfirm from "../components/auth/PasswordResetConfirm";

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

        <Route path="/" element={<AuthRoute/>}>
          <Route path="login" element={<Login/>}/>
          <Route path="register" element={<Register/>}/>
          <Route path="password/reset" element={<PasswordReset/>}/>
          <Route path="password/reset/confirm/:user_id/:token" element={<PasswordResetConfirm/>}/>
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
