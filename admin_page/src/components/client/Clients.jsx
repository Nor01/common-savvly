//React
import { Link } from "react-router-dom";
import { useEffect, useState } from "react";
import { useUsers } from "../../contexts/UsersContext";

//Components
import ViewClientModal from "./ViewClientModal";

//Libs
import Swal from "sweetalert2";
import ReactPaginate from "react-paginate";
import ClientFilters from "./ClientFilters";

const Clients = () => {
  const { getClients, clients, deleteClient, getUserPii } = useUsers();
  const [selectedClient, setSelectedClient] = useState();
  const [pii, setPii] = useState({
    address: "",
    dateofbirth: "",
    mothername: "",
    social: "",
  });

  
  const [currentClients, setCurrentClients] = useState([]);
  const [filteredClients, setFilteredClients] = useState([]);
  const [pageCount, setPageCount] = useState(0);
  const [itemOffset, setItemOffset] = useState(0);
  const [itemsPerPage, setItemsPerPage] = useState(10);

  useEffect(() => {
      getClients();
  }, []);

  useEffect( () => {
    setFilteredClients(clients);
  }, [clients]);

  //Pagination
  useEffect(() => {
    const endOffset = itemOffset + itemsPerPage;
    setCurrentClients(filteredClients.slice(itemOffset, endOffset));
    setPageCount(Math.ceil(filteredClients.length / itemsPerPage));
  }, [itemOffset, itemsPerPage, filteredClients]);

  const handlePageClick = (event) => {
    const newOffset = (event.selected * itemsPerPage) % clients.length;
    setItemOffset(newOffset);
  };
  //END pagination

  const handleClientModalClose = () => {
    setSelectedClient();
    setPii();
  };

  const viewClient = async (client) => {
    setSelectedClient(client);
    const piiRes = await getUserPii(client.idx);
    setPii(piiRes);
  };

  const deleteClientAlert = async (clientId) => {
    Swal.fire({
      title: "Are you sure?",
      text: "You are about to delete " + clientId,
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#d33",
      confirmButtonText: "Delete",
    }).then((result) => {
      if (result.isConfirmed) {
        Swal.fire({
          title: "Deleting " + clientId + "...",
          allowEscapeKey: false,
          allowOutsideClick: false,
          didOpen: () => {
            Swal.showLoading();
          },
        });

        deleteClient(clientId)
          .then((res) => res.json())
          .then(() => {
            Swal.fire({
              title: clientId + " deleted successfully.",
              confirmButtonColor: "#0e6e7b",
              icon: "success",
            });
            getClients();
          })
          .catch((err) => {
            Swal.fire({
              title: "Error occurred deleting this user",
              icon: "error",
            });
          });
      }
    });
  };

  return (
    <>
      <div className="is-flex is-justify-content-space-between is-align-content-baseline	">
        <p className="title">Clients</p>
        <Link to="create" className="button is-primary">
          Add New
        </Link>
      </div>
      <ClientFilters setFilteredClients={setFilteredClients} />
      <hr />
      <div className="is-flex mb-4">
        <div className="is-flex is-justify-content-center is-align-items-center">
          <label className="px-1">Clients per Page</label>
          <div className="select">
            <select
              value={itemsPerPage}
              onChange={(e) => setItemsPerPage(e.target.value)}
            >
              <option>10</option>
              <option>20</option>
              <option>50</option>
              <option>100</option>
            </select>
          </div>
        </div>
        <ReactPaginate
          nextLabel="next >"
          onPageChange={handlePageClick}
          pageRangeDisplayed={3}
          pageCount={pageCount}
          previousLabel="< prev"
          containerClassName="pagination-list is-flex is-justify-content-end"
          breakLinkClassName="pagination-link"
          pageLinkClassName="pagination-link"
          previousLinkClassName="pagination-previous"
          nextLinkClassName="pagination-next"
          activeClassName="active"
          breakLabel="..."
          renderOnZeroPageCount={null}
        />
      </div>

      <div className="table-container">
        <table className="table is-fullwidth is-hoverable">
          <thead>
            <tr>
              <th>ID</th>
              <th>Account ID</th>
              <th>Advisor ID</th>
              <th>Age</th>
              <th>Gender</th>
              <th>Status</th>
              <th>...</th>
            </tr>
          </thead>
          <tbody>
            {currentClients.map((client) => (
              <tr key={client.idx}>
                <td>{client.idx}</td>
                <td>{client.accountid}</td>
                <td>{client.parentid}</td>
                <td>{client.age}</td>
                <td>{client.sex}</td>
                <td>{client.statusflag}</td>
                <td>
                  <div className="tags">
                    <span
                      className="tag is-primary is-clickable mr-2"
                      onClick={() => viewClient(client)}
                    >
                      View
                    </span>
                    <span className="tag is-warning is-clickable mr-2">
                      Edit
                    </span>
                    <span
                      className="tag is-danger is-clickable mr-2"
                      onClick={() => deleteClientAlert(client.idx)}
                    >
                      Delete
                    </span>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <ViewClientModal
        pii={pii}
        client={selectedClient}
        closeModal={handleClientModalClose}
      />
    </>
  );
};

export default Clients;
