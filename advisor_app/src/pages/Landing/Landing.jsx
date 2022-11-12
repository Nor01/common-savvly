import { SavvlyLogo } from "../../assets/images";
import "./Landing.scss";
import { Link } from "react-router-dom";
import LogInButton from "../../components/auth/LogInButton";

const Landing = () => {
  return (
    <div id="landingHero">
      <div className="landing-nav is-flex is-justify-content-space-between p-5">
        <div className="landing-logo">
          <img src={SavvlyLogo} />
        </div>
        <div className="login-btn">
            <LogInButton/>
        </div>
      </div>
      <div className="landing-hero is-flex is-justify-content-center is-align-items-center is-flex-direction-column">
        <h1 className="title has-text-white">Welcome to Savvly</h1>
        <p className="has-text-white mb-4">Savvly is an alternative investment fund that's designed to protect and perform.</p>
        <Link to="register" className="button is-primary">Register Now</Link>
      </div>
    </div>
  );
};

export default Landing;
