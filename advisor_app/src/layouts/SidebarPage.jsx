import { useAppContext } from "../contexts/AppContext";
import { useEffect } from "react";

const SidebarPage = ({ children, value = true }) => {
  const { setShowSideBar } = useAppContext();

  useEffect( () => {
    setShowSideBar(value);
  }, [value])
  

  return children;
};

export default SidebarPage;
