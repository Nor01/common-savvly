import React, { useContext, useState } from "react";

const UsersContext = React.createContext();
const SavvlyApiUrl = "https://savvly-dev-api.azurewebsites.net/";

export function useUsers() {
  return useContext(UsersContext);
}

export const UsersProvider = ({ children }) => {
  const [admins, setAdmins] = useState([]);
  const [advisors, setAdvisors] = useState([]);
  const [clients, setClients] = useState([]);

  const login = async () => {
    var myHeaders = new Headers();
    myHeaders.append("Cookie", "session=01fadb7b-4309-4244-9c42-6f6ce32be989");

    var requestOptions = {
      method: "GET",
      headers: myHeaders,
      redirect: "follow",
    };

    fetch("https://savvly-dev-api.azurewebsites.net/getinfo", requestOptions)
      .then((response) => response.text())
      .then((result) => console.log(JSON.parse(result)))
      .catch((error) => console.log("error", error));
  };

  const getAdmins = async () => {
    const response = await fetch(SavvlyApiUrl + "getadmins");
    const adminsObj = await response.json();
    const { admins, proxyres } = adminsObj;

    setAdmins(proxyres != "Fail" ? admins : []);
  };

  const getAdvisors = async () => {
    // const response = await fetch(
    //   SavvlyApiUrl + "getallassociatedrias?associated=Savvly"
    // );
    // const advisorsObject = await response.json();
    // const {getallassociatedrias, proxyres} = advisorsObject;

    // setAdvisors(proxyres != "Fail" ? getallassociatedrias : []);
    const generateAdvisors = (amount, maxRand) => {
      let res = [];
      for (let index = 0; index < amount; index++) {
        res.push({
          idx: "advisor" + (index + 1),
          associated: "Savvly",
          crd: Math.floor(Math.random() * maxRand) + 1,
        });
      }
      return res;
    };

    setAdvisors(generateAdvisors(3, 500));
  };

  const getClients = async () => {
    // const response = await fetch(SavvlyApiUrl + "usersdata");
    // const clientsObject = await response.json();
    // const {usersdata, proxyres} = clientsObject;

    // setClients(proxyres != "Fail" ? usersdata[0] : []);
    function create_UUID() {
      var dt = new Date().getTime();
      var uuid = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(
        /[xy]/g,
        function (c) {
          var r = (dt + Math.random() * 16) % 16 | 0;
          dt = Math.floor(dt / 16);
          return (c == "x" ? r : (r & 0x3) | 0x8).toString(16);
        }
      );
      return uuid;
    }

    const generateClients = (amount, maxRand) => {
      let res = [];
      for (let index = 0; index < amount; index++) {
        res.push({
          idx: create_UUID(),
          accountid: Math.floor(Math.random() * maxRand) + 1,
          parentid:
            (Math.floor(Math.random() * maxRand) + 1) % 2 == 0
              ? "advisor1"
              : "advisor2",
          age: Math.floor(Math.random() * 90) + 1,
          sex: (Math.floor(Math.random() * maxRand) + 1) % 2 == 0 ? "M" : "F",
          statusflag:
            (Math.floor(Math.random() * maxRand) + 1) % 2 == 0
              ? "Active"
              : "Pending",
        });
      }
      return res;
    };

    setClients(generateClients(50, 500));
  };

  //Functions without state

  const getUserPii = async (clientId) => {
    const response = await fetch(
      SavvlyApiUrl + "getuserpii?userid=" + clientId
    );
    const piiObj = await response.json();
    return piiObj.getuserpii;
  };

  const getClientsByAdvisorId = async (advisorId) => {
    const response = await fetch(
      SavvlyApiUrl + "getmychildren?userid=" + advisorId
    );
    const clientsObject = await response.json();
    return clientsObject;
  };

  const addClient = async ({ userId, social, dob, address, sex, mother }) => {
    return fetch(
      SavvlyApiUrl +
        `addnewuser?userid=${userId}&social=${social}&dob=${dob.replaceAll(
          "-",
          "/"
        )}&address=${address}&sex=${sex}&mother=${mother}`
    );
    //Note: would be cool if the API returned the new user object
  };

  const addAdvisor = async ({ userId, crd, associated }) => {
    return fetch(
      SavvlyApiUrl +
        `addnewria?userid=${userId}&crd=${crd}&associated=${associated}`
    );
  };

  const deleteClient = async (clientId) => {
    return fetch(SavvlyApiUrl + "deleteuser?userid=" + clientId);
  };

  return (
    <UsersContext.Provider
      value={{
        admins,
        advisors,
        clients,
        login,
        getAdmins,
        getAdvisors,
        getClients,
        getClientsByAdvisorId,
        addClient,
        deleteClient,
        getUserPii,
        addAdvisor,
      }}
    >
      {children}
    </UsersContext.Provider>
  );
};
