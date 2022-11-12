import { useEffect } from "react";
import { registerRequest } from "../../config/authConfig";
import { useMsal } from "@azure/msal-react";

const Register = () => {

  const { instance } = useMsal();

  useEffect( () => {
    instance.loginRedirect(registerRequest).catch((e) => {
      console.error(e);
    });  }, [])

    return <p>Loading...</p>;
};

export default Register;
