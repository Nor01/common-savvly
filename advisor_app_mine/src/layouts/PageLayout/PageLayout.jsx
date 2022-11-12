import "./PageLayout.scss";
import Sidebar from "../../components/Sidebar";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Dashboard from "../../components/Dashboard";
import PageNotFound from "../../pages/PageNotFound";

const PageLayout = () => {
  return (
    <div id="savvlyDashboard">
      <div className="columns is-fullheight p-0 m-0">
        <div className="column p-0 m-0 is-2 background-pattern sidebar">
          <Sidebar />
        </div>
        <div className="column is-10">
          <div className="container mt-2">
            <Router>
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="*" element={<PageNotFound />} />
              </Routes>
            </Router>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PageLayout;
