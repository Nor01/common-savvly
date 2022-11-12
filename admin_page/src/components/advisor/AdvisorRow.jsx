import { useState, useEffect } from "react";
import { useUsers } from "../../contexts/UsersContext";

const AdvisorRow = ({ adv }) => {

    const { getClientsByAdvisorId } = useUsers();

    const { idx, associated, crd } = adv;

    const [isOpen, setIsOpen] = useState(false);
    const [clientsLoaded, setClientsLoaded] = useState(false);
    const [clients, setClients] = useState([]);

    useEffect( () => {
        if (isOpen && !clientsLoaded)
            getClientsByAdvisorId(idx)
                .then((res) => {
                    setClients(res.mychildren);
                    setClientsLoaded(true);
                })
    },[isOpen])

    return (
        <>
            <tr onClick={() => setIsOpen(!isOpen)}>
                <td>{idx}</td>
                <td>{associated}</td>
                <td>{crd}</td>
            </tr>
            {
                isOpen && (
                    <tr>
                        <td colSpan={4} className="has-background-light p-5">
                            <div className="table-container">
                                <table className="table is-fullwidth">
                                    <thead>
                                        <tr>
                                            <th>ID</th>
                                            <th>Age</th>
                                            <th>Gender</th>
                                            <th>Status</th>
                                            <th>Shares</th>
                                            <th>...</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {
                                            clients.map((client) => (
                                                <tr>
                                                    <td>{client.idx}</td>
                                                    <td>{client.age}</td>
                                                    <td>{client.sex}</td>
                                                    <td>{client.statusflag}</td>
                                                    <td>{client.numshares}</td>
                                                    <td>
                                                        <span className="tag is-primary is-clickable mr-2">View</span>
                                                    </td>
                                                </tr>
                                            ))
                                        }
                                        {
                                            clients.length === 0 &&
                                            <tr>
                                                <td colSpan={6} className="has-text-centered">
                                                    <strong>{idx}</strong> has no clients.
                                                </td>
                                            </tr>
                                        }
                                    </tbody>
                                </table>
                            </div>
                        </td>
                    </tr>
                )
            }
        </>
    )
}

export default AdvisorRow