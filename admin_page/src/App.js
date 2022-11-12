import "./Index.scss";

import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Home from './components/Home';
import NavBar from './components/layouts/NavBar';
import SideBar from './components/layouts/SideBar';

import Admins from "./components/admin/Admins";
import Advisors from "./components/advisor/Advisors";
import AddEditAdvisor from "./components/advisor/AddEditAdvisor";
import Clients from "./components/client/Clients";
import AddEditClient from './components/client/AddEditClient';

import PageNotFound from './components/PageNotFound';

import { ToastContainer } from 'react-toastify';


function App() {
  return (
    <Router>
      <NavBar />
      <div className="container">
        <div className="columns">
          <div className="column is-2">
            <SideBar />
          </div>
          <div className="column is-10 has-background-white is-rounded my-4">
            <div className="p-4">
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="admins" element={<Admins />} />
                
                <Route path="advisors" element={<Advisors />} />
                <Route path="advisors/create" element={<AddEditAdvisor />} />

                <Route path="clients" element={<Clients />} />
                <Route path="clients/create" element={<AddEditClient />} />

                <Route path="*" element={<PageNotFound />} />
              </Routes>
            </div>
          </div>
        </div>
      </div>
      <ToastContainer />
    </Router>

  );
}

export default App;
