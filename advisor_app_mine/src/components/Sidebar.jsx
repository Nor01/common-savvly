import savvlyLogo from "../assets/images/logo-white.png";
import { useMsal } from "@azure/msal-react";

const Sidebar = () => {
  const { instance } = useMsal();

  const logout = () => {
    instance.logoutPopup().catch((e) => {
      console.error(e);
    });
  };

  return (
    <>
      <div className="sidebar-header">
        <div className="sidebar-logo">
          <img src={savvlyLogo} alt="Savvly Inc. white logo" />
        </div>
        <ul className="nav-links">
          <li className="nav-link">Home</li>
          <li className="nav-link">Clients + Contract</li>
          <li className="nav-link">Estimator</li>
          <li className="nav-link">FAQ</li>
        </ul>
      </div>
      <div className="sidebar-footer">
        <p className="footer-link">Profile and Settings</p>
        <p className="footer-link" onClick={logout}>
          Logout
        </p>
      </div>
    </>
  );
};

export default Sidebar;
