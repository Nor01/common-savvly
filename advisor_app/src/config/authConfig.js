const { REACT_APP_MSAL_CLIENTID } = process.env;

export const msalConfig = {
  auth: {
    clientId: REACT_APP_MSAL_CLIENTID,
    //authority: "https://login.microsoftonline.com/" + REACT_APP_MSAL_TENANTID,
    authority:
      "https://savvlyb2c.b2clogin.com/savvlyb2c.onmicrosoft.com/B2C_1_Savvly_signin",
    knownAuthorities: ["savvlyb2c.b2clogin.com"],
    //redirectUri: "https://savvly-dev-api.azurewebsites.net/getAToken",
  },
};

// Add scopes here for ID token to be used at Microsoft identity platform endpoints.
export const loginRequest = {
  scopes: ["openid", "offline_access", REACT_APP_MSAL_CLIENTID],
};

export const registerRequest = {
  authority:
    "https://savvlyb2c.b2clogin.com/savvlyb2c.onmicrosoft.com/B2C_1_Savvly_ria_signup",
  scopes: ["openid", "offline_access"],
};
