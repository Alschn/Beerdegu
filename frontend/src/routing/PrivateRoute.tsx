import {FC} from "react";
import {Outlet} from "react-router";
import WrapWithHeader from "../components/layout/WrapWithHeader";
import {Navigate} from "react-router";

interface PrivateRouteProps {
  withHeader?: boolean
}

const PrivateRoute: FC<PrivateRouteProps> = ({withHeader = true}) => {
  const isAuthenticated = localStorage.getItem('token') !== null;

  if (isAuthenticated) {
    if (withHeader) {
      return (
        <WrapWithHeader>
          <Outlet/>
        </WrapWithHeader>
      );
    } else return (
      <Outlet/>
    );
  }
  return <Navigate to="/login"/>;
};

export default PrivateRoute;
