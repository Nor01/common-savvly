import { useEffect } from "react";
import { useMsal } from "@azure/msal-react";
import { Link, NavLink } from "react-router-dom";
import { LearnIcon, PlanIcon, StartIcon } from "../../assets/images";
import { loginRequest } from "../../config/authConfig";

const Dashboard = () => {

  useEffect(() => {
    getInfo();
  }, [])
  
  const getInfo = async () => {
    const request = {
      ...loginRequest,
      account: accounts[0],
    };

    const { accessToken } = await instance.acquireTokenSilent(request);
    fetch(`https://savvly-dev-api.azurewebsites.net/getinfo`, {
      headers: {
        Authorization: "Bearer " + accessToken,
      }
    });
  }

  const { instance, accounts, inProgress } = useMsal();

  const name = accounts[0]
    ? `${accounts[0].idTokenClaims.given_name} ${accounts[0].idTokenClaims.family_name}`
    : "Unknown";

  return (
    <div id="mainDash" className="container p-4">
      <br />
      <hr />
      <div className="main-dashboard has-text-centered">
        <h1 className="title is-size-2 mb-1">Welcome to Savvly, {name}</h1>
        <p className="has-text-primary is-size-5">
          We have a few ways you can get comfortable with the Savvly product
        </p>
      </div>

      <div className="dashboardLinks columns mt-6 is-variable is-8">
        <div className="column">
          <div className="dashLink card">
            <div className="card-content">
              <div className="content">
                <p className="linkTitle">Learn</p>
                <p>Download brochures and get Savvly documentation</p>
                <img src={LearnIcon} alt="Learn icon" />
                <NavLink to="/documentation" className="button is-primary">Download Brochures</NavLink>
              </div>
            </div>
          </div>
        </div>

        <div className="column">
          <div className="dashLink card">
            <div className="card-content">
              <div className="content">
                <p className="linkTitle">Plan</p>
                <p>Try different variables to estimate return in various scenarios</p>
                <img src={PlanIcon} alt="Learn icon" />
                <NavLink className="button is-primary" to="/estimator">Try the Estimator</NavLink>
              </div>
            </div>
          </div>
        </div>

        <div className="column">
          <div className="dashLink card">
            <div className="card-content">
              <div className="content">
                <p className="linkTitle">Start</p>
                <p>Ready to start? Our easy process will create a contract in minutes</p>
                <img src={StartIcon} alt="Learn icon" />
                <Link to="/newcontract" className="button is-primary">Start a Contract</Link>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="meeting mt-5">
        <p className="meetingTitle">Still have questions?</p>
        <p>Schedule a meeting with our financial advisor staff</p>
        <button className="button is-primary is-outlined mt-4" onClick={() => window.open("https://calendly.com/meet-savvly/discovery?utm_medium=website&utm_source=adviser&utm_content=hero", '_blank', 'noopener,noreferrer')}>Schedule a Meeting</button>
      </div>
    </div>
  );
};

export default Dashboard;
