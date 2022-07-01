import {PureComponent} from "react";
import { Link } from "react-router-dom";
import WrapWithHeader from "../components/layout/WrapWithHeader";
// import empty from "../images/empty.svg";
import "./PageNotFound.scss";


class PageNotFound extends PureComponent<any, any> {
  render() {
    return (
      <WrapWithHeader>
        <div className="PageNotFound">
          <span className="text">Page not found!</span>
          <Link to="/">
            <img className="image" src={""} alt=""/>
          </Link>
        </div>
      </WrapWithHeader>
    );
  };
}

export default PageNotFound;
