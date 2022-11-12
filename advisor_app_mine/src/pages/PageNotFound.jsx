import { useLocation, useNavigate } from "react-router-dom";
import { useEffect } from "react";

const PageNotFound = () => {
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    if (location.pathname == "/login" || location.pathname == "/register")
      navigate("/");
  }, []);

  return <div>PageNotFound</div>;
};

export default PageNotFound;
