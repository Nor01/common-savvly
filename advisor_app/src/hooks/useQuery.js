import { useState, useEffect } from "react";
import { useMsal } from "@azure/msal-react";
import { loginRequest } from "../config/authConfig";

const useQuery = () => {
  const { instance, accounts } = useMsal();

  const query = async (url, debugMode = false) => {
    try {
      const request = {
        ...loginRequest,
        account: accounts[0],
      };

      const { accessToken } = await instance.acquireTokenSilent(request);

      const res = await fetch(url, {
        headers: {
          Authorization: "Bearer " + accessToken,
        },
      });

      if (debugMode)
        console.info("QUERY IN DEBUG MODE ", res);

      if (!res.ok) throw new Error(res.statusText);

      let response = await res.text();

      try {
        response = JSON.parse(response);
      } catch (error) {
        if (debugMode)
          console.info("PARSING JSON (DEBUG MODE):", error);
      }

      if (debugMode)
        console.info("JSON OF RESPONSE:", response);

      return {
        status: true,
        response,
      };
    } catch (err) {
      if (debugMode)
        console.error("QUERY ERROR (DEBUG MODE)", err);

      return {
        status: false,
        error: err,
      };
    }
  };

  return { query };
};

export default useQuery;
