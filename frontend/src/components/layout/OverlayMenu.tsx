import {FC, Fragment, useEffect} from "react";
import {Link} from "react-router-dom";
import "./OverlayMenu.scss";
import {useAuth} from "../../context/authContext";

interface OverlayMenuProps {
  isOpen: boolean;
  handleClose: () => void;
}

const toggleScroll = (open: boolean) => document.body.style.overflow = open ? 'hidden' : 'auto';

const OverlayMenu: FC<OverlayMenuProps> = ({isOpen, handleClose}) => {
  const {isAuthenticated, logout} = useAuth();

  useEffect(() => {
    // toggle body scroll when closing/opening menu
    toggleScroll(isOpen);
  }, [isOpen]);

  return (
    <div className={isOpen ? 'overlay open' : 'overlay'} id="overlay" onClick={handleClose}>
      <nav className="overlay-menu">
        <ul>
          <li><Link to="/">Home</Link></li>
          {/*<li><Link to="/browser">Browser</Link></li>*/}
          <li><Link to="/lobby">Lobby</Link></li>
          {isAuthenticated ? (
            <Fragment>
              <li><Link to="/password/change">Change Password</Link></li>
              {/*<li><Link to="/profile">Profile</Link></li>*/}
              <li><span onClick={logout}>Logout</span></li>
            </Fragment>
          ) : (
            <Fragment>
              <li><Link to="/auth/login">Login</Link></li>
              <li><Link to="/auth/register">Register</Link></li>
              <li><Link to="/auth/password/reset">Reset Password</Link></li>
            </Fragment>
          )}
        </ul>
      </nav>
    </div>
  );
};

export default OverlayMenu;
