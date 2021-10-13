import React, {PureComponent} from "react";
import "./PageNotFound.scss";
import empty from "../images/empty.svg";
import WrapWithHeader from "../components/layout/WrapWithHeader";

class PageNotFound extends PureComponent<any, any> {
  render() {
    return (
      <WrapWithHeader>
        <div className="PageNotFound">
          <span className="text">Page not found!</span>
          <a href="/">
            <img className="image" src={empty} alt=""/>
          </a>
        </div>
      </WrapWithHeader>
    );
  };
}

export default PageNotFound;
