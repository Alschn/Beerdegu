import {FC} from "react";
import {Outlet} from "react-router";
import {Navigate} from "react-router-dom";
import WrapWithHeader from "../components/layout/WrapWithHeader";


interface PrivateRouteProps {

}

const AuthRoute: FC<PrivateRouteProps> = () => {
  const isAuthenticated = localStorage.getItem('token') !== null;

  return isAuthenticated ? (
    <Navigate to=""/>
  ) : (
    <WrapWithHeader>
      <Outlet/>
    </WrapWithHeader>
  );
};

export default AuthRoute;
