import React, {ComponentType, FC} from "react";
import {Redirect, Route} from "react-router";

type authPathType = "/login" | "/register";

interface PrivateRouteProps {
  component: ComponentType,
  path: authPathType,
  exact?: boolean,
  children?: React.ReactNode,
}

const AuthRoute: FC<PrivateRouteProps> = (
  {
    component,
    children,
    path,
    exact,
  }) => {
  const isAuthenticated = localStorage.getItem('token') !== null;

  return isAuthenticated ? (
    <Redirect to=""/>
  ) : (
    <Route path={path} exact={exact} component={component}>
      {children}
    </Route>
  );
};

export default AuthRoute;
