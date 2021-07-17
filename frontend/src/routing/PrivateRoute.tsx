import React, {ComponentType, FC} from "react";
import {Redirect, Route} from "react-router";

interface PrivateRouteProps {
  component: ComponentType,
  path: string,
  exact?: boolean,
  children?: React.ReactNode,
}

const PrivateRoute: FC<PrivateRouteProps> = ({component, children, path, exact}) => {
  const isAuthenticated = localStorage.getItem('token') !== null;

  return isAuthenticated ? (
    <Route path={path} exact component={component}>
      {children}
    </Route>
  ) : (
    <Redirect to="/login"/>
  );
};

export default PrivateRoute;
