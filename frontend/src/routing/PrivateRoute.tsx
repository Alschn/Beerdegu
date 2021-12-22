import {ComponentType, FC, ReactNode} from "react";
import {Redirect, Route} from "react-router";
import WrapWithHeader from "../components/layout/WrapWithHeader";

interface PrivateRouteProps {
  component: ComponentType,
  path: string,
  exact?: boolean,
  withHeader?: boolean,
  children?: ReactNode,
}

const PrivateRoute: FC<PrivateRouteProps> = ({component, children, path, exact, withHeader = true}) => {
  const isAuthenticated = localStorage.getItem('token') !== null;

  if (isAuthenticated) {
    if (withHeader) {
      return (
        <WrapWithHeader>
          <Route path={path} exact component={component}>
            {children}
          </Route>
        </WrapWithHeader>

      );
    } else return (
      <Route path={path} exact component={component}>
        {children}
      </Route>
    );
  }
  return <Redirect to="/login"/>;
};

export default PrivateRoute;
