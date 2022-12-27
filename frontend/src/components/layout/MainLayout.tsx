import {FC, Fragment, ReactNode, useState} from "react";
import logo from "../../assets/logo.svg";
import {IconButton, useMediaQuery} from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import CloseIcon from "@mui/icons-material/Close";
import OverlayMenu from "./OverlayMenu";
import "./MainLayout.scss";
import {Link} from "react-router-dom";
import {useAuth} from "../../context/AuthContext";


interface WrapWithHeaderProps {
  children: ReactNode;
}


const MainLayout: FC<WrapWithHeaderProps> = ({children}) => {
  const {isAuthenticated, logout} = useAuth();

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
        <Link to="/" className="title">
          <img src={logo} alt=""/>
          <span>Beerdegu</span>
        </Link>

        {matchesForLinks && (
          <ul className="header-links">
            <li>
              <Link to="/">Home</Link>
            </li>
            {/*<li>*/}
            {/*  <Link to="/browser">Browser</Link>*/}
            {/*</li>*/}
            <li>
              <Link to="/lobby">Lobby</Link>
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
                {/*<li>*/}
                {/*  <Link to="/profile">Profile</Link>*/}
                {/*</li>*/}
                <li>
                  <Link to="/password/change">Change Password</Link>
                </li>
                <li onClick={logout}>
                  <span>Logout</span>
                </li>
              </ul>
            ) : (
              <ul className="header-links">
                <li>
                  <Link to="/login">Login</Link>
                </li>
                <li>
                  <Link to="/register">Register</Link>
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

export default MainLayout;
