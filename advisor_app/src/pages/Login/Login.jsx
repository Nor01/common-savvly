import { useEffect } from "react";
import { loginRequest } from "../../config/authConfig";
import { useMsal } from "@azure/msal-react";

const Login = () => {

  const { instance } = useMsal();

  useEffect( () => {
    instance.loginRedirect(loginRequest).catch((e) => {
      console.error(e);
    });
  }, []);

  return (
    "Loading..."
  );
};

export default Login;
