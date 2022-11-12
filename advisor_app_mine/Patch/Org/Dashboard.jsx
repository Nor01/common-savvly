import { useMsal } from "@azure/msal-react";
import { useState } from "react";

const Dashboard = () => {
  const { instance, accounts, inProgress } = useMsal();
  const [accessToken, setAccessToken] = useState(null);

  const name = accounts[0] && `${accounts[0].idTokenClaims.given_name} ${accounts[0].idTokenClaims.family_name}`;
  
//   instance
//     .acquireTokenSilent(request)
//     .then((response) => {
//       setAccessToken(response.accessToken);
//       console.log(response.accessToken);
//     })
//     .catch((e) => {
//       instance.acquireTokenPopup(request).then((response) => {
//         setAccessToken(response.accessToken);
//       });
//     });

  return <h1 className="title">Welcome {name}</h1>;
};

export default Dashboard;
