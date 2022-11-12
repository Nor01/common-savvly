import { useMsal } from "@azure/msal-react";
import { useState } from "react";
import {loginRequest} from "../config/authConfig";

const Dashboard = () => {
  const { instance, accounts, inProgress } = useMsal();
  const [accessToken, setAccessToken] = useState(null);

  const name = accounts[0] && `${accounts[0].idTokenClaims.given_name} ${accounts[0].idTokenClaims.family_name}`;
  
  const login = () => {
    //fetch("https://savvly-dev-api.azurewebsites.net/login", {
    fetch("http://localhost:5000/login", {
    }).then( r => r.json())
    .then( response => console.log(response));
  }

  const signup = () => {
    //fetch("https://savvly-dev-api.azurewebsites.net/registerria", {
    fetch("http://localhost:5000/registerria", {
    }).then( r => r.json())
    .then( response => console.log(response));
  }

  const getInfo = () => {
    //fetch("https://savvly-dev-api.azurewebsites.net/getinfo", {
    fetch("http://localhost:5000/getinfo", {
      headers: {
        "Authorization": "Bearer " + accessToken,
        "Content-Type": "application/json"
      }
    }).then( r => r.json())
    .then( response => console.log(response));
  }

  const generateToken = () => {
    const request = {
      ...loginRequest,
      account: accounts[0]
    };

    instance
    .acquireTokenSilent(request)
    .then((response) => {
      setAccessToken(response.accessToken);
      console.log(response);
    })
    .catch((e) => {
      console.log(e);
      instance.acquireTokenPopup(request).then((response) => {
        setAccessToken(response.accessToken);
        console.log(response);
      });
    });
  }

  return (
    <div className="container mt-2">
      <div className="header is-flex is-justify-content-space-between">
        <h1 className="title">Welcome {name}</h1>
        <div className="button is-primary">Start New Contract</div>
      </div>

      <button className="button is-primary" onClick={login}>Login</button>
      <button className="button is-primary" onClick={signup}>Signup</button>
      <button className="button is-primary" onClick={generateToken}>Generate Token</button>
      <button className="button is-primary" onClick={getInfo}>Get Info</button>
    </div>
  
  )
};

export default Dashboard;
