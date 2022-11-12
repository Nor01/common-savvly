/* eslint-disable prettier/prettier */
import "react-block-ui/style.css";
import { ReactNode } from "react";
import { useRouter } from 'next/router';

type IMainProps = {
  children: ReactNode;
};

const MainNew = (props: IMainProps) => {
  const router = useRouter();

  return (
    <div className="login no-header">
      <div className="divider">
        <div className="sidebar sidebar-black main-sidebar">
          <div className="sidebar-container full-width grid_flex fd-column jc-between full-height">
            <div className="full-size bg-wrapper">
              <div className="--main-bg-container"></div>
              <div className="main-sidebar-wrapper full-height grid_flex fd-column">
                <div className="main-sidebar-header-wrapper full-width">
                  <div className="sidebar-header">
                    <div className="site-logo">
                      <img
                        src={`${router.basePath}/assets/images/svgs/savvly-logo-white-shadow.svg`}
                        alt="logo savvly"
                        width={122}
                        height={24}
                      />
                    </div>
                  </div>
                </div>
                <div className="sidebar-main-content-wrapper full-size">
                  <div className="sidebar-main full-width grid_flex fd-column jc-between full-height">
                    <nav
                      className="nav-menu header-menu"
                      aria-labelledby="primary-navigation"
                    >
                      <ul>
                        <li className="menu-item">
                          <a href="https://wonderful-tree-0f57b720f.1.azurestaticapps.net/">Home</a>
                        </li>
                        <li className="menu-item">
                          <a href="https://wonderful-tree-0f57b720f.1.azurestaticapps.net/contracts">Client + Contracts</a>
                        </li>
                        <li className="menu-item active-menu">
                          <a href="#">Estimator</a>
                        </li>
                        <li className="menu-item">
                          <a href="#">FAQ</a>
                        </li>
                      </ul>
                    </nav>

                  </div>
                </div>
              </div>
            </div>


          </div>
        </div>
        <div className="site">
          <div >{props.children}</div>
        </div>
      </div>
    </div>)

}

export default MainNew