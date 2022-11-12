import { SavvlyLogo } from "../assets/images";
import { useMsal } from "@azure/msal-react";
import { NavLink } from "react-router-dom";
import { LogoutIcon, SettingsIcon } from "../assets/images";

const Sidebar = () => {
  const { instance } = useMsal();

  const logout = () => {
    instance
      .logoutPopup({
        mainWindowRedirectUri: "https://savvly.com",
      })
      .catch((e) => {
        console.error(e);
      });
  };

  return (
    <>
      <div className="sidebar-header">
        <div className="sidebar-logo">
          <img src={SavvlyLogo} alt="Savvly Inc. white logo" />
        </div>
        <div className="nav-links">
          <NavLink className="nav-link" to="/">
            Home
          </NavLink>
          <NavLink className="nav-link" to="/contracts">
            Clients + Contracts
          </NavLink>
          <NavLink className="nav-link" to="/estimator">
            Estimator
          </NavLink>
          <NavLink className="nav-link" to="/documentation">
            Documentation
          </NavLink>
          <NavLink className="nav-link" to="/faq">
            FAQ
          </NavLink>
        </div>
      </div>
      <div className="sidebar-footer">
          <p className="footer-link">Profile and Settings</p>
          <p className="footer-link" onClick={logout} >Logout</p>

          {/* <div className="buttons is-flex pr-2 is-clickable">
            <img src={SettingsIcon} alt="Settings" className="mr-2" />
            <img src={LogoutIcon} alt="Logout" onClick={logout} />
          </div> */}
      </div>
    </>
  );
};

export default Sidebar;
