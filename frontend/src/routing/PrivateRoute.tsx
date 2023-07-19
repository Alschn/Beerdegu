import {FC} from "react";
import {Navigate, Outlet} from "react-router";
import MainLayout from "../components/layout/MainLayout";
import {useAuth} from "../context/authContext";

interface PrivateRouteProps {
  withHeader?: boolean;
}

const PrivateRoute: FC<PrivateRouteProps> = ({withHeader = true}) => {
  const {isAuthenticated} = useAuth();

  if (!isAuthenticated) return (<Navigate to="/auth/login"/>);

  if (withHeader) {
    return (
      <MainLayout>
        <Outlet/>
      </MainLayout>
    );
  }

  return (<Outlet/>);
};

export default PrivateRoute;
