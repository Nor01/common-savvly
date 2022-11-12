import { useEffect, useState } from "react";
import { useMsal } from "@azure/msal-react";
import { loginRequest } from "../config/authConfig";

const useFetch = (url) => {
  const { instance, accounts } = useMsal();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const generateFetch = async () => {
    setLoading(true);

    const request = {
      ...loginRequest,
      account: accounts[0],
    };

    const { accessToken } = await instance.acquireTokenSilent(request);
    
    fetch(url, {
      headers: {
        Authorization: "Bearer " + accessToken,
      },
    })
      .then((res) => res.json())
      .then((response) => {
        if (response.proxyres == "Fail")
          throw new Error("API FAIL");

        setData(response);
      })
      .catch((err) => {
        setError(err);
      })
      .finally(() => {
        setLoading(false);
      });
  };

  useEffect(() => {
    generateFetch();
  }, [url]);

  return { data, loading, error };
};

export default useFetch;
