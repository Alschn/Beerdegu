import {FC} from "react";
import {Outlet} from "react-router";
import {Navigate} from "react-router-dom";
import MainLayout from "../components/layout/MainLayout";
import {useAuth} from "../context/authContext";


interface AuthRouteProps {

}

const AuthRoute: FC<AuthRouteProps> = () => {
  const {isAuthenticated} = useAuth();

  return isAuthenticated ? (
    <Navigate to=""/>
  ) : (
    <MainLayout>
      <Outlet/>
    </MainLayout>
  );
};

export default AuthRoute;
