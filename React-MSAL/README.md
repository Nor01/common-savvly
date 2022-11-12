# SAVVLY

![react + msal](https://miro.medium.com/max/1400/1*NUbnNtzUyfBYuPVWdkTAVw.png)

## React + Microsoft Authentication Library

**Use this project as reference for future Savvly's SPAs that need the Azure AD Login.**

`msalConfig` values are described here:

| Value Name                         | About                                                                                                                                             |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Enter_the_Application_Id_Here`    | The Application (client) ID of the application you registered or that you want to connect to.                                                     |
| `Enter_the_Cloud_Instance_Id_Here` | The Azure cloud instance in which your application is registered. For the main (or global) Azure cloud, enter `https://login.microsoftonline.com` |
| `Enter_the_Tenant_Info_Here`       | The Directory (Tenant) ID                                                                                                                         |
| `Enter_the_Redirect_Uri_Here`      | Replace with http://localhost:3000                                                                                                                |

More information:
https://docs.microsoft.com/en-us/azure/active-directory/develop/tutorial-v2-react
