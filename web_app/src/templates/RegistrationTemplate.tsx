/* eslint-disable prettier/prettier */
// @ts-ignore
// @ts-nocheck

import "react-block-ui/style.css";

import { ReactNode } from "react";
import { useRouter } from 'next/router';

type IMainProps = {
  children: ReactNode;
};
// src={`${router.basePath}/assets/images/logo-white.png`}

const RegistrationTemplate = (props: IMainProps) => {

  const router = useRouter();

  return (
    <div className="login">
      <header className="header header--type1">
        <div className="container">
          <div className="flex-between">
            <div className="site-logo">
              <img src={`${router.basePath}/assets/images/logo-white.png`} alt="logo savvly" />
              <p className="main-sub-title">Live more. Earn more.</p>
            </div>
            <nav className="side-navigation grid_flex">
              <p>Need to Login Instead?</p>
              <span className="vr-line-small"></span>
              <a href="#" className="link-yellow">
                Advisor Registration
              </a>
            </nav>
          </div>
        </div>
      </header>
      <div className="divider flex-md-column">
        <div className="sidebar sidebar-white sidebar-signup">
          <div className="container">
          <div >{props.children}</div> 
          </div>
        </div>

        <div className="sign-up-main-container advisor">
          <div className="sign-up-nav flex-between">
            <div className="descriptive-form-title flex-end">
              <p>Advisor Registration</p>
            </div>
          </div>
          <div className="site site-bg">
            <div className="bg-container"></div>
            <div className="full-width container">
              <div className="bottom-caption-container">
                {/* <div className="bottom-caption">
                  <a href="#" className="support" title="support">
                    <svg
                      width="39"
                      height="39"
                      viewBox="0 0 39 39"
                      fill="none"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <path
                        d="M39 26.3935C39 21.5536 36.2235 17.2346 32.0653 15.1338C31.9358 24.413 24.413 31.9365 15.1338 32.0653C17.2346 36.2235 21.5543 39 26.3935 39C28.6627 39 30.8694 38.3959 32.808 37.2472L38.9451 38.9451L37.2472 32.808C38.3952 30.8694 39 28.6627 39 26.3935Z"
                        fill="white"
                      />
                      <path
                        d="M29.7832 14.8916C29.7832 6.68027 23.1029 0 14.8916 0C6.68027 0 0 6.68027 0 14.8916C0 17.5675 0.712207 20.1734 2.06502 22.4608L0.0548438 29.7284L7.3224 27.7182C9.60984 29.071 12.2157 29.7832 14.8916 29.7832C23.1029 29.7832 29.7832 23.1029 29.7832 14.8916ZM12.6064 11.4258H10.3213C10.3213 8.90525 12.3711 6.85547 14.8916 6.85547C17.4121 6.85547 19.4619 8.90525 19.4619 11.4258C19.4619 12.7047 18.9203 13.9341 17.9758 14.7987L16.0342 16.5758V18.3574H13.749V15.5688L16.4326 13.1122C16.9124 12.6735 17.1768 12.0748 17.1768 11.4258C17.1768 10.1659 16.1515 9.14063 14.8916 9.14063C13.6317 9.14063 12.6064 10.1659 12.6064 11.4258ZM13.749 20.6426H16.0342V22.9277H13.749V20.6426Z"
                        fill="white"
                      />
                    </svg>
                  </a>
                </div> */}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RegistrationTemplate;
