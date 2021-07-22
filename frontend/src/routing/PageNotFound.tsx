import React, {PureComponent} from "react";
import "./PageNotFound.scss";
import empty from "../images/empty.svg";

class PageNotFound extends PureComponent<any, any> {
  render() {
    return (
      <div className="PageNotFound">
        <span className="text">Page not found!</span>
        <img className="image" src={empty} alt=""/>
      </div>
    );
  };
}

export default PageNotFound;
