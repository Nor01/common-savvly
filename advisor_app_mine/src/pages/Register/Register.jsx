// import "./Register.scss";
// import savvlyLogo from "../../assets/images/logo-white.png";
// import { Link } from "react-router-dom";
// import { useState } from "react";
// import RegisterFormInput from "../../components/RegisterFormInput";
// import { useNavigate } from "react-router-dom";
// import LogInButton from "../../components/auth/LogInButton";

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

  // const navigate = useNavigate();
  // const [errors, setErrors] = useState({});

  // const validateForm = (data) => {
  //   const errors = {};
  //   let errorCount = 0;

  //   const requiredFields = [
  //     "crd",
  //     "associated",
  //     "firstname",
  //     "lastname",
  //     "email",
  //     "street",
  //     "city",
  //     "zip",
  //   ];

  //   for (var key in data) {
  //     let value = data[key];

  //     if (requiredFields.includes(key) && (value.trim() === "" || !value)) {
  //       errors[key] = "This field is required.";
  //       errorCount++;
  //     }

  //     if (
  //       key == "email" &&
  //       !value.match(
  //         /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/
  //       )
  //     ) {
  //       errors[key] = "This email is invalid.";
  //       errorCount++;
  //     }
  //   }

  //   setErrors(errors);
  //   return errorCount;
  // };

  // const handleSubmit = (e) => {
  //   e.preventDefault();

  //   const data = {
  //     crd: e.target.crd.value,
  //     associated: "Savvly",
  //     firstname: e.target.firstname.value,
  //     lastname: e.target.lastname.value,
  //     email: e.target.email.value,
  //     street: e.target.street.value,
  //     city: e.target.city.value,
  //     zip: e.target.zip.value,
  //   };

  //   const errorCount = validateForm(data);

  //   if (errorCount > 0) return;

  //   //Create the user in AD
  //   fetch(
  //     `https://savvly-dev-api.azurewebsites.net/createuser?firstname=${data.firstname}&lastname=${data.lastname}&email=${data.email}&street=${data.street}&city=${data.city}&zip=${data.zip}`
  //   )
  //     .then((res) => res.json())
  //     .then((userres) => {
  //       console.log("User added to Active Directory!");
  //       console.log({ userResponse: userres });
  //       if (userres.proxyres === "OK") {
  //         navigate("/login");
  //         //If the user was created succesfully, let's add it too in our database (as an Advisor)
  //         fetch(
  //           `https://savvly-dev-api.azurewebsites.net/addnewria?crd=${data.crd}&associated=${data.associated}`
  //         )
  //           .then((res) => res.json())
  //           .then((advres) => {
  //             console.log("User added to our database!");
  //             console.log({ advisorResponse: advres });
  //           })
  //           .catch((error) => console.error({ error }));
  //       }
  //     })
  //     .catch((error) => console.error({ error }));
  // };

  //return (
  //   <div id="registerApp" className="is-flex is-flex-direction-column">
  //     <div className="columns m-0">
  //       <div className="container section is-fullhd is-fullwidth has-background-img-blackpattern">
  //         <img src={savvlyLogo} alt="Savvly Inc. white logo" />
  //         <span className="is-text-color-white1" style={{ marginLeft: 50 }}>
  //           Need to Login Instead? | {" "}
  //           <LogInButton type="register" />
  //         </span>
  //         <p className="is-size-7 is-uppercase is-text-color-white1">
  //           live more. earn more.
  //         </p>
  //       </div>
  //     </div>
  //     <div className="columns is-flex-grow-1 m-0">
  //       <aside className="column is-5 is-narrow-mobile is-fullheight logo-login-section is-background-white p-0">
  //         <div className="container section is-fullhd">
  //           <p className="is-size-3">Advisor Registration</p>
  //           <hr />
  //           <br />
  //           <form onSubmit={handleSubmit}>
  //             <div className="field is-horizontal">
  //               <div className="field-body">
  //                 <RegisterFormInput
  //                   label="First Name"
  //                   placeholder="i.e. John"
  //                   name="firstname"
  //                   errors={errors?.firstname}
  //                 />
  //                 <RegisterFormInput
  //                   label="Last Name"
  //                   placeholder="i.e. Smith"
  //                   name="lastname"
  //                   errors={errors?.lastname}
  //                 />
  //               </div>
  //             </div>

  //             <RegisterFormInput
  //               label="Address"
  //               placeholder="i.e. 123 Main St."
  //               name="street"
  //               errors={errors?.street}
  //             />

  //             <div className="field is-horizontal">
  //               <div className="field-body">
  //                 <RegisterFormInput
  //                   label="City"
  //                   placeholder="i.e. Maintown"
  //                   name="city"
  //                   errors={errors?.city}
  //                 />
  //                 <RegisterFormInput
  //                   label="Zipcode"
  //                   placeholder="i.e. 92831"
  //                   name="zip"
  //                   errors={errors?.zip}
  //                 />
  //               </div>
  //             </div>
  //             <RegisterFormInput
  //               label="Finra Number"
  //               placeholder="i.e. T0017112"
  //               name="crd"
  //               errors={errors?.crd}
  //             />
  //             <br />
  //             <div className="field is-horizontal">
  //               <div className="field-body">
  //                 <RegisterFormInput
  //                   label="Email Address"
  //                   placeholder="john@savvly.com"
  //                   name="email"
  //                   errors={errors?.email}
  //                 />
  //               </div>
  //             </div>
  //             <p className="buttons is-right">
  //               <button type="submit" className="button button-primary ">
  //                 <span>Register</span>
  //               </button>
  //             </p>
  //           </form>
  //         </div>
  //       </aside>
  //       <div className="container is-fullheight column is-7 is-hidden-mobile has-background-img-advisor"></div>
  //     </div>
  //   </div>
  // );
};

export default Register;
