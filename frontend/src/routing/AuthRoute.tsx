import {FC} from "react";
import {Outlet} from "react-router";
import {Navigate} from "react-router-dom";
import WrapWithHeader from "../components/layout/WrapWithHeader";
import {useAuth} from "../context/authContext";


interface PrivateRouteProps {

}

const AuthRoute: FC<PrivateRouteProps> = () => {
  const {isAuthenticated} = useAuth();

  return isAuthenticated ? (
    <Navigate to=""/>
  ) : (
    <WrapWithHeader>
      <Outlet/>
    </WrapWithHeader>
  );
};

export default AuthRoute;
