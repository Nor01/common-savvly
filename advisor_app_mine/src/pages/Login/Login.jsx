// import "./Login.scss";
// import savvlyLogo from "../../logo-white.png";
// import LogInButton from "../../components/auth/LogInButton";
// import { Link } from "react-router-dom";
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
    // <div id="savvly-login">
    //   <div className="columns fullheight m-0">
    //     <aside className="column is-4 is-narrow-mobile is-fullheight logo-login-section is-background-white">
    //       <div className="container section is-fullhd has-background-img-blackpattern">
    //         <img src={savvlyLogo} alt="Savvly Inc. white logo" />
    //         <p className="is-size-7 is-uppercase is-text-color-white1">
    //           live more. earn more.
    //         </p>
    //       </div>
    //       <div className="container column is-12 is-hidden-tablet has-background-img-airplane background-mobile">
    //         <div className="section"></div>
    //       </div>
    //       <div className="container section is-fullhd">
    //         <div className="field">
    //           <div className="control">
    //             <i className="fa-solid fa-lock" />
    //             <span className="is-text-color-green has-text-weight-bold">
    //               Login
    //             </span>
    //             <br />
    //             <br />
    //             <LogInButton />
    //           </div>
    //         </div>
    //         <br />
    //       </div>
    //       <div className="container section is-fullhd">
    //         <p className="is-size-6">
    //           Forgot {""}
    //           <a className="has-text-weight-bold">password</a>?
    //         </p>
    //         <p className="is-size-6">
    //           Need an account? {""}
    //           <Link className="has-text-weight-bold" to="/register">Advisor registration</Link>
    //         </p>
    //       </div>
    //       <div className="mysection">
    //         <div className="container">
    //           <hr />
    //         </div>
    //       </div>
    //     </aside>
    //     <div className="container column is-8 is-hidden-mobile has-background-img-airplane">
    //       <div className="section">
    //         <h1 className="is-size-4 background-text has-text-weight-light	">
    //           Secure your lifestyle for the future.
    //         </h1>
    //       </div>
    //     </div>
    //   </div>
    // </div>
  );
};

export default Login;
