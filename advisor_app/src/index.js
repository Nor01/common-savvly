import React from "react";
import ReactDOM from "react-dom/client";
import "./index.scss";
import App from "./App";

import { PublicClientApplication } from "@azure/msal-browser";
import { MsalProvider } from "@azure/msal-react";
import { msalConfig } from "./config/authConfig";
import { AppContextProvider } from "./contexts/AppContext";

const msalInstance = new PublicClientApplication(msalConfig);

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <MsalProvider instance={msalInstance}>
    <AppContextProvider>
      <App />
    </AppContextProvider>
  </MsalProvider>
);
