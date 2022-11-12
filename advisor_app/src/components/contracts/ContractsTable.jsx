import { Link } from "react-router-dom";

const ContractsTable = ({
  loading,
  error,
  contracts,
  setSelectedContract
}) => {
  return (
    <>
      <div className="header is-flex is-justify-content-space-between">
        <h1 className="title has-text-primary">Clients + Contracts</h1>
        <Link to="/newcontract" className="button is-primary">
          Start New Contract
        </Link>
      </div>

      <hr />
      <table id="contractsTable" className="table is-fullwidth is-hoverable">
        <thead>
          <tr>
            <th>CONTRACT ID</th>
            <th>CONTRACT MODIFIED</th>
            <th>FIRST, LAST NAME</th>
            <th>FUNDS</th>
            <th>CONTRACT STATUS</th>
            <th>...</th>
          </tr>
        </thead>
        <tbody>
          {loading && (
            <tr>
              <td colSpan={100}>
                <div className="is-flex is-justify-content-center is-align-items-center">
                  <div className="loadingSpinner"></div>
                </div>
              </td>
            </tr>
          )}

          {error && (
            <tr>
              <td colSpan={100}>
                <div className="notification is-danger">
                  Error loading contracts...
                </div>
              </td>
            </tr>
          )}

          {contracts?.potentialclients?.map((c) => (
            <tr key={c.idx}>
              <td>
                <a href="#" onClick={() => setSelectedContract(c)}>{c.contractid == "None" ? c.idx : c.contractid}</a>
              </td>
              <td>
                {new Date(c.lastupdate * 1000).toLocaleDateString("en-US", {
                  year: "numeric",
                  month: "long",
                  day: "numeric",
                })}
              </td>
              <td>
                {c.clientinfo.firstname} {c.clientinfo.lastname}
              </td>
              <td>${c.clientinfo.funding.toLocaleString("en-US")}</td>
              <td>{c.status}</td>
              <td>
                <button className="button is-primary is-outlined is-small">
                  Edit
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
};

export default ContractsTable;
