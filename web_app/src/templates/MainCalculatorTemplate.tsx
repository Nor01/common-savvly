/* eslint-disable prettier/prettier */
import "react-block-ui/style.css";

import { ReactNode } from "react";
import { useRouter } from 'next/router';

type IMainProps = {
  children: ReactNode;
};

const MainCalculatorTemplate = (props: IMainProps) => {
  const router = useRouter();


  const sendToCalendly = () => {
    const url = "https://calendly.com/savvly/learn-more";
    window.open(url, "_blank");
  };
  return (
    <div>
      <header className="hero" id="hero">
        <span className="hero-layer"></span>
        <div className="hero-logo">
            <img src={`${router.basePath}/assets/images/svgs/savvly-logo-white-shadow.svg`} alt="logo savvly" width={122} height={24} />
            <p className="yellow">Live more. Earn more.</p>
        </div>
        <article>
            <p className="hero-slogan">START PLANNING</p>
            <h1 className="hero-title">Introducing our prospect planner</h1>
            <p className="hero-desc">Start planning the future and decide the best solution for you. Enter your funding amount and payout age and see the benefits of our retirement plan.</p>

        </article>
    </header>

      <div >{props.children}</div>


      <main className="main" id="main">
        <section className="black black-patern-1">
          <div className="container">
            <div className="content center">
              <p className="slogan yellow">LET’S TALK ABOUT THE FUTURE</p>
              <h2 className="main-title">Schedule a meeting with Savvly</h2>
              <p className="sub-title">
                Whether you are an Adviser or a prospect client, book a meeting
                with us.
              </p>
              <div className="buttons center">
                <button
                  className="button-normal btn-blue-bg secondary-btn margin-top"
                  type="button"
                  style={{margin: 'auto'}}
                  onClick={sendToCalendly}
                >
                  Book a call
                </button>
              </div>
            </div>
          </div>
        </section>
      </main>

      <footer id="footer" className="footer">
        <div className="grid_flex jc-between ai-center container">
          <div className="footer-left">
            <div className="footer-logo">
              <img src={`${router.basePath}/assets/images/svgs/savvly-logo-white-shadow.svg`} alt="logo savvly" width={122} height={24} />
            </div>
            <div className="footer-nav margin-top-double">
              <ul className="footer-nav-list">
                <li>
                Boulder office:
                  <p className="yellow regular">Savvly, Inc.</p>
                  <p className="yellow regular">1035 Pearl St, Suite 322</p>
                  <p className="yellow regular">Boulder, CO 80302</p>
                </li>
                <li>
                Chicago office:
                  <p className="yellow regular">Savvly, Inc.</p>
                  <p className="yellow regular">444 West Lake St, Suite 1700</p>
                  <p className="yellow regular">Chicago, IL 60606</p>
                </li>
                <li>
                  Contact:
                  <p>
                    <a href="#" className="secondary">
                      info@savvly.com
                    </a>
                  </p>
                </li>
              </ul>
            </div>
            <div className="sub-footer">
              <ul className="copyrights">
                <li>
                  <span className="current-year">@ 2022 </span>Savvly. All
                  rights reserved.
                </li>
                <span className="vr-line-small"></span>
                <li>Terms & Conditions and Privacy Policy.</li>
              </ul>
            </div>
          </div>
          <div className="footer-right">
            <div className="footer-right-logo">
              <svg
                width="49"
                height="98"
                viewBox="0 0 49 98"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M29.8133 46.0461C32.2282 54.2262 33.8054 63.4311 31.2836 71.7806C28.0935 82.3489 18.4431 86.5192 9.79953 92.0528C8.31141 93.0063 6.61835 94.5924 7.33122 96.2053C8.04409 97.8181 10.3609 97.631 12.0629 97.1587C21.6064 94.539 31.2658 91.5538 39.3658 85.8687C42.6717 83.5519 45.7548 80.6915 47.3855 76.9578C52.5717 64.8034 40.2301 52.3817 32.4777 44.4867C32.2283 44.2367 31.9031 44.0766 31.5529 44.0313C31.2028 43.9861 30.8475 44.0583 30.5428 44.2366C30.2381 44.415 30.0012 44.6894 29.8692 45.0168C29.7372 45.3443 29.7175 45.7062 29.8133 46.0461Z"
                  fill="white"
                  fillOpacity="0.05"
                />
                <path
                  d="M18.2559 71.9856C15.1638 60.7312 13.2213 45.5649 22.7113 36.7877C29.7064 30.3808 39.5885 25.5957 48.1162 21.5947C48.4499 21.4543 48.7187 21.1937 48.8693 20.8644C49.0198 20.5351 49.0412 20.1613 48.929 19.817C48.8169 19.4728 48.5795 19.1832 48.2639 19.0058C47.9483 18.8284 47.5775 18.776 47.2251 18.8591C30.0806 21.8175 -0.652932 29.4719 0.175778 46.2065C0.183483 46.3564 0.168461 46.5067 0.131223 46.6521C-0.198478 47.8996 -1.15194 55.358 15.7965 73.3846C16.0191 73.6256 16.3167 73.7842 16.6408 73.8345C16.965 73.8848 17.2966 73.8239 17.5817 73.6617C17.8669 73.4995 18.0887 73.2456 18.2111 72.9413C18.3335 72.6369 18.3493 72.3001 18.2559 71.9856Z"
                  fill="white"
                  fillOpacity="0.05"
                />
                <path
                  d="M29.7599 7.62241C30.0617 9.36929 29.7997 11.1669 29.0118 12.7549C28.2239 14.343 26.951 15.639 25.3774 16.4554C23.8038 17.2718 22.0112 17.5661 20.2591 17.2958C18.5071 17.0254 16.8866 16.2045 15.6322 14.9518C14.3779 13.6991 13.5548 12.0796 13.2822 10.3279C13.0096 8.57627 13.3016 6.78329 14.1159 5.20862C14.9302 3.63396 16.2246 2.35934 17.8116 1.56935C19.3986 0.779351 21.1958 0.51498 22.9431 0.814515C24.6435 1.10601 26.2118 1.91704 27.4325 3.13611C28.6531 4.35518 29.4662 5.92244 29.7599 7.62241Z"
                  fill="white"
                  fillOpacity="0.05"
                />
              </svg>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export { MainCalculatorTemplate };
