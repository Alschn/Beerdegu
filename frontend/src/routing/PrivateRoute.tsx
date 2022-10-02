import {FC} from "react";
import {Outlet} from "react-router";
import WrapWithHeader from "../components/layout/WrapWithHeader";
import {Navigate} from "react-router";
import {useAuth} from "../context/authContext";

interface PrivateRouteProps {
  withHeader?: boolean;
}

const PrivateRoute: FC<PrivateRouteProps> = ({withHeader = true}) => {
  const {isAuthenticated} = useAuth();

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
