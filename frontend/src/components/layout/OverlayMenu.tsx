import {FC, Fragment, useEffect} from "react";
import {logout} from "../../api/auth";
import "./OverlayMenu.scss";

interface OverlayMenuProps {
  isOpen: boolean;
  handleClose: () => void;
}

const toggleScroll = (open: boolean) => document.body.style.overflow = open ? 'hidden' : 'auto';

const OverlayMenu: FC<OverlayMenuProps> = ({isOpen, handleClose}) => {
  const isAuthenticated = localStorage.getItem('token') != null;

  useEffect(() => {
    // toggle body scroll when closing/opening menu
    toggleScroll(isOpen);
  }, [isOpen]);

  return (
    <div className={isOpen ? 'overlay open' : 'overlay'} id="overlay" onClick={handleClose}>
      <nav className="overlay-menu">
        <ul>
          <li><a href="/">Home</a></li>
          <li><a href="/browser">Browser</a></li>
          <li><a href="/lobby">Lobby</a></li>
          {isAuthenticated ? (
            <Fragment>
              <li><a href="/profile">Profile</a></li>
              <li><span onClick={logout}>Logout</span></li>
            </Fragment>
          ) : (
            <Fragment>
              <li><a href="/login">Login</a></li>
              <li><a href="/register">Register</a></li>
            </Fragment>
          )}
        </ul>
      </nav>
    </div>
  );
};

export default OverlayMenu;
