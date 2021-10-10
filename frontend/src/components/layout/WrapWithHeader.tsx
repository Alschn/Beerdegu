import {FC, Fragment, ReactNode, useState} from "react";
import {logout} from "../../api/auth";
import logo from "../../images/logo.svg";
import {useMediaQuery} from "@material-ui/core";
import IconButton from "@material-ui/core/IconButton";
import MenuIcon from "@material-ui/icons/Menu";
import CloseIcon from "@material-ui/icons/Close";
import OverlayMenu from "./OverlayMenu";
import "./WrapWithHeader.scss";


interface WrapWithHeaderProps {
  children: ReactNode;
}


const WrapWithHeader: FC<WrapWithHeaderProps> = ({children}) => {
  const isAuthenticated = localStorage.getItem('token') !== null;

  const matchesForHamburgerMenu = useMediaQuery('(max-width: 679px)');
  const matchesForLinks = useMediaQuery('(min-width: 525px)');
  const matchesForFullNavbar = useMediaQuery('(min-width: 680px)');

  const [isMenuOpen, setIsMenuOpen] = useState<boolean>(false);
  const [isCloseIcon, setIsCloseIcon] = useState<boolean>(false);

  const openMenu = () => {
    setIsMenuOpen(true);
    setIsCloseIcon(true);
  };

  const closeMenu = () => {
    setIsMenuOpen(false);
    setTimeout(() => {
      setIsCloseIcon(false);
    }, 100);
  };

  return (
    <div className="main">
      <header className="header">
        <a href="/" className="title">
          <img src={logo} alt=""/>
          <span>Beerdegu</span>
        </a>

        {matchesForLinks && (
          <ul className="header-links">
            <li>
              <a href="/">Home</a>
            </li>
            <li>
              <a href="/">Browser</a>
            </li>
            <li>
              <a href="/lobby">Lobby</a>
            </li>
          </ul>
        )}

        {matchesForHamburgerMenu && (
          <Fragment>
            <div className="flex-grow"/>
            <IconButton onClick={openMenu}>
              {isCloseIcon ? (<CloseIcon/>) : (<MenuIcon/>)}
            </IconButton>
          </Fragment>
        )}

        {matchesForFullNavbar && (
          <Fragment>
            <div className="flex-grow"/>

            {isAuthenticated ? (
              <ul className="header-links">
                <li>
                  <a href="/profile">Profile</a>
                </li>
                <li onClick={logout}>
                  <span>Logout</span>
                </li>
              </ul>
            ) : (
              <ul className="header-links">
                <li>
                  <a href="/login">Login</a>
                </li>
                <li>
                  <a href="/register">Register</a>
                </li>
              </ul>
            )}
          </Fragment>
        )}
      </header>

      <OverlayMenu isOpen={isMenuOpen} handleClose={closeMenu}/>

      {children}
    </div>
  );
};

export default WrapWithHeader;
