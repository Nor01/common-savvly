const { REACT_APP_MSAL_CLIENTID, REACT_APP_MSAL_TENANTID, REACT_APP_MSAL_REDIRECT_URI } = process.env;

export const msalConfig = {
    auth: {
      clientId: REACT_APP_MSAL_CLIENTID,
      //authority: "https://login.microsoftonline.com/" + REACT_APP_MSAL_TENANTID,
      authority: "https://savvlyb2c.b2clogin.com/savvlyb2c.onmicrosoft.com/B2C_1_Savvly_signin",
      knownAuthorities: ["savvlyb2c.b2clogin.com"]
    }
  };

  // Add scopes here for ID token to be used at Microsoft identity platform endpoints.
  export const loginRequest = {
    scopes: [ "openid", "offline_access" ]
  };

  export const registerRequest = {
    scopes: [ "openid", "offline_access" ],
    authority: "https://savvlyb2c.b2clogin.com/savvlyb2c.onmicrosoft.com/B2C_1_Savvly_ria_signup"
  };