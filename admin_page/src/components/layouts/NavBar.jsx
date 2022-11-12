import savvlyLogo from "../../savvly-logo.svg"
import { NavLink, Link } from "react-router-dom";

const NavBar = () => {
    return (
        <nav className="navbar is-white main-navbar">
            <div className="container">
                <div className="navbar-brand">
                    <Link className="navbar-item" to="/" style={{ background: "#0e6e7b" }}>
                        <img src={savvlyLogo} width={112} height={28} />
                    </Link>
                    <div className="navbar-burger burger" data-target="navMenu">
                        <span />
                        <span />
                        <span />
                    </div>
                </div>
                <div id="navMenu" className="navbar-menu">
                    <div className="navbar-start">
                        <NavLink className="navbar-item" to="admins">
                            Admins
                        </NavLink>
                        <NavLink className="navbar-item" to="advisors">
                            Advisors
                        </NavLink>
                        <NavLink className="navbar-item" to="clients">
                            Clients
                        </NavLink>
                    </div>
                </div>
            </div>
        </nav>
    )
}

export default NavBar;