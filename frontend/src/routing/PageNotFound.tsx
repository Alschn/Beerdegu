import {PureComponent} from "react";
import { Link } from "react-router-dom";
import MainLayout from "../components/layout/MainLayout";
// import empty from "../images/empty.svg";
import "./PageNotFound.scss";


class PageNotFound extends PureComponent<any, any> {
  render() {
    return (
      <MainLayout>
        <div className="PageNotFound">
          <span className="text">Page not found!</span>
          <Link to="/">
            <img className="image" src={""} alt=""/>
          </Link>
        </div>
      </MainLayout>
    );
  };
}

export default PageNotFound;
