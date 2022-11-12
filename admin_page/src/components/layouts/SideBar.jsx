import { NavLink } from "react-router-dom";

export default function SideBar() {
    return (

        <aside className="menu is-hidden-mobile sidebar">
            <p className="menu-label">General</p>
            <ul className="menu-list">
                <li>
                    <NavLink className="navbar-item" to="/">Dashboard</NavLink>
                </li>
                <li>
                    <a>Customers</a>
                </li>
                <li>
                    <a>Other</a>
                </li>
            </ul>
            <p className="menu-label">Administration</p>
            <ul className="menu-list">
                <li>
                    <a className="menu-list-title">Manage Users</a>
                    <ul>
                        <li>
                        <NavLink className="navbar-item" to="admins">
                            Admins
                        </NavLink>
                        </li>
                        <li>
                        <NavLink className="navbar-item" to="advisors">
                            Advisors
                        </NavLink>
                        </li>
                        <li>
                        <NavLink className="navbar-item" to="clients">
                            Clients
                        </NavLink>
                        </li>
                    </ul>
                </li>
            </ul>
            <p className="menu-label">Transactions</p>
            <ul className="menu-list">
                <li>
                    <a>Deposits</a>
                </li>
                <li>
                    <a>Withdrawal</a>
                </li>
            </ul>
        </aside>
    )
}
