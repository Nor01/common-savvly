import { useMsal } from "@azure/msal-react";
import { loginRequest } from "../../config/authConfig";

const LogInButton = ({type}) => {
//  const { instance } = useMsal();
//
//  function handleLogin(instance) {
//    instance.loginRedirect(loginRequest).catch((e) => {
//      console.error(e);
//    });
//  }
 

const login = () => {
  //fetch("https://savvly-dev-api.azurewebsites.net/login", {
  //fetch("http://localhost:5000/getloginurl",  {
    fetch("https://savvlyb2c.b2clogin.com/savvlyb2c.onmicrosoft.com/b2c_1_savvly_signin/oauth2/v2.0/authorize?client_id=e41831ff-9f6c-466d-bb12-e1f39cba16b8&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2FgetAToken&scope=https%3A%2F%2Fsavvlyb2c.onmicrosoft.com%2Fapi%2FAccounts.Read+https%3A%2F%2Fsavvlyb2c.onmicrosoft.com%2Fapi%2FAccounts.Write+offline_access+openid+profile&state=78ec3214-9a05-4103-8729-a6827f774676",  {
  })
  .then((response) => response.json())
  .then((responseData) => {
    console.log(responseData);
    //fetch(responseData.url,  { })
    return responseData;
  })
  .catch(error => console.warn(error));
}


  //const login = () => {
  //  //fetch("https://savvly-dev-api.azurewebsites.net/login", {
  //  fetch("http://localhost:5000/getloginurl", {
  //  }).then( r => r.json())
  //  .then( response => console.log(response));
  //}

  const signup = () => {
    //fetch("https://savvly-dev-api.azurewebsites.net/registerria", {
    fetch("http://localhost:5000/registerria", {
    }).then( r => r.json())
    .then( response => console.log(response));
  }


  if (type === "landing")
    //return <button className="button is-primary" onClick={() => handleLogin(instance)}>Adviser Log In</button>;
    return <button className="button is-primary" onClick={() => login()}>Adviser Log In</button>;

  if (type === "register")
    //return <a href="#" className="is-text-color-yellow advisor-registration-link" onClick={() => handleLogin(instance)}>Adviser Log In</a>
    return <a href="#" className="is-text-color-yellow advisor-registration-link" onClick={() => signup()}>Adviser Log In</a>
};

export default LogInButton;