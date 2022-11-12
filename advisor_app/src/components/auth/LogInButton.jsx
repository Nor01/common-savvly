import { useMsal } from "@azure/msal-react";
import { loginRequest } from "../../config/authConfig";

const LogInButton = () => {
  const { instance } = useMsal();

  function handleLogin(instance) {
    instance.loginRedirect(loginRequest).catch((e) => {
      console.error(e);
    });
  }
 
  return <button className="button is-primary" onClick={() => handleLogin(instance)}>Advisor Log In</button>;
};

export default LogInButton;