import "./PageLayout.scss";
import Sidebar from "../../components/Sidebar";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Dashboard from "../../pages/Dashboard/Dashboard";
import PageNotFound from "../../pages/PageNotFound";

import { useAppContext } from "../../contexts/AppContext";
import SidebarPage from "../SidebarPage";
import ContractCreation from "../../pages/ContractCreation/ContractCreation";
import Contracts from "../../pages/Contracts/Contracts";
import Estimator from "../../pages/Estimator/Estimator";
import Documentation from "../../pages/Documentation/Documentation";
import FAQ from "../../pages/FAQ/FAQ";

const PageLayout = () => {
  const { showSideBar } = useAppContext();

  return (
    <div id="savvlyDashboard">
      <Router>
        <div className="columns is-fullheight p-0 m-0">
          {showSideBar && (
            <div className="column p-0 m-0 is-2 background-pattern sidebar">
              <Sidebar />
            </div>
          )}

          <div className={"column p-0 " + (showSideBar ? "is-10" : "is-12")} style={ {"overflow-y": "auto"}}>
            <Routes>
              <Route
                path="/"
                element={
                  <SidebarPage>
                    <Dashboard />
                  </SidebarPage>
                }
              />
              <Route
                path="/contracts"
                element={
                  <SidebarPage>
                    <Contracts />
                  </SidebarPage>
                }
              />
              <Route
                path="/newcontract"
                element={
                  <SidebarPage value={false}>
                    <ContractCreation />
                  </SidebarPage>
                }
              />
              <Route
                path="/estimator"
                element={
                  <SidebarPage>
                    <Estimator />
                  </SidebarPage>
                }
              />
              <Route
                path="/documentation"
                element={
                  <SidebarPage>
                    <Documentation />
                  </SidebarPage>
                }
              />
              <Route
                path="/faq"
                element={
                  <SidebarPage>
                    <FAQ />
                  </SidebarPage>
                }
              />
              <Route
                path="*"
                element={
                  <SidebarPage value={false}>
                    <PageNotFound />
                  </SidebarPage>
                }
              />
            </Routes>
          </div>
        </div>
      </Router>
    </div>
  );
};

export default PageLayout;
