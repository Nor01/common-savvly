import { useState, useEffect } from "react";
import { useUsers } from "../../contexts/UsersContext";

const ClientFilters = ({ setFilteredClients }) => {
  const { getAdvisors, advisors, clients } = useUsers();
  const [isOpen, setIsOpen] = useState(false);

  const [filters, setFilters] = useState({
    id: "",
    accountId: "",
    status: "All",
    name: "",
    mother: "",
    social: "",
    advisorsCheckboxes: {},
  });

  useEffect(() => {
    getAdvisors();
  }, []);

  useEffect(() => {
    let advisorsCheckboxes = {};
    for (const adv of advisors) advisorsCheckboxes[adv.idx] = true;
    setFilters({ ...filters, advisorsCheckboxes });
  }, [advisors]);

  useEffect(() => {
    executeFiltering(filters);
  }, [filters]);

  const executeFiltering = (filters) => {
    let result = JSON.parse(JSON.stringify(clients));

    let allowedAdvs = [];
    const { advisorsCheckboxes: checkboxes, id, status, accountId } = filters;

    for (var adv in checkboxes)
      if (checkboxes.hasOwnProperty(adv) && checkboxes[adv])
        allowedAdvs.push(adv);

    result = result.filter(
      (c) =>
        c.idx.indexOf(id) !== -1 && //By ID
        c.accountid.toString().indexOf(accountId) !== -1 && //By Account ID
        (status !== "All" ? c.statusflag == status : true) &&//By Status
        allowedAdvs.includes(c.parentid) // By Advisor Checkbox
    );

    setFilteredClients(result);
  };

  const adminCheckboxChanged = (e, id) => {
    setFilters({
      ...filters,
      advisorsCheckboxes: {
        ...filters.advisorsCheckboxes,
        [id]: e.target.checked,
      },
    });
  };

  return (
    <>
      <div className="clientFilterTab" onClick={() => setIsOpen(!isOpen)}>
        <span>+</span> <span className="">Filters</span>
      </div>
      {isOpen && (
        <div className="columns is-multiline my-2">
          <div className="column is-4">
            <p className="has-text-weight-bold">Advisors:</p>
            {advisors.map((adv) => (
              <label key={adv.idx} className="checkbox is-block py-1">
                <input
                  type="checkbox"
                  defaultChecked={true}
                  value={filters.advisorsCheckboxes[adv.idx]}
                  onChange={(e) => adminCheckboxChanged(e, adv.idx)}
                />
                <span className="ml-2">{adv.idx}</span>
              </label>
            ))}
          </div>
          <div className="column is-8">
            <div className="columns is-multiline">
              <div className="field column is-4 py-0">
                <label className="label">By ID</label>
                <div className="control">
                  <input
                    className="input"
                    type="text"
                    value={filters.id}
                    onChange={(e) =>
                      setFilters({ ...filters, id: e.target.value })
                    }
                  />
                </div>
              </div>
              <div className="field column is-4 py-0">
                <label className="label">By Account ID</label>
                <div className="control">
                  <input
                    className="input"
                    type="text"
                    name="id"
                    onChange={(e) =>
                      setFilters({ ...filters, accountId: e.target.value })
                    }
                  />
                </div>
              </div>
              <div className="field column is-4 py-0">
                <label className="label">By Status</label>
                <div className="control">
                  <div className="select is-fullwidth">
                    <select
                      name="sex"
                      onChange={(e) =>
                        setFilters({ ...filters, status: e.target.value })
                      }
                    >
                      <option value="All">All</option>
                      <option value="Pending">Pending</option>
                      <option value="Active">Active</option>
                    </select>
                  </div>
                </div>
              </div>
              <div className="field column is-4 py-0">
                <label className="label">By Name</label>
                <div className="control">
                  <input
                    className="input"
                    type="text"
                    name="id"
                    defaultValue={"API CHANGE NEEDED"}
                    // onChange={(e) =>
                    //   setFilters({ ...filters, name: e.target.value })
                    // }
                  />
                </div>
              </div>
              <div className="field column is-4 py-0">
                <label className="label">By Mother Name</label>
                <div className="control">
                  <input
                    className="input"
                    type="text"
                    name="id"
                    defaultValue={"API CHANGE NEEDED"}
                    // onChange={(e) =>
                    //   setFilters({ ...filters, mother: e.target.value })
                    // }
                  />
                </div>
              </div>
              <div className="field column is-4 py-0">
                <label className="label">By Social Security Number</label>
                <div className="control">
                  <input
                    className="input"
                    type="text"
                    name="id"
                    defaultValue={"API CHANGE NEEDED"}
                    // onChange={(e) =>
                    //   setFilters({ ...filters, social: e.target.value })
                    // }
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default ClientFilters;
