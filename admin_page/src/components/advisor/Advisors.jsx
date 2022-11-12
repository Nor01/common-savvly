import { useEffect } from "react";
import { useUsers } from "../../contexts/UsersContext";
import { Link } from "react-router-dom";
import AdvisorRow from "./AdvisorRow";

const Advisors = () => {

    const { getAdvisors, advisors } = useUsers();

    useEffect(() => {
        getAdvisors();
    }, []);

    return (
        <>
            <div className="is-flex is-justify-content-space-between is-align-content-baseline	">
                <p className="title">Advisors</p>
                <Link to="create" className="button is-primary">Add New</Link>
            </div>
            <table className="table is-fullwidth is-hoverable">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Associated</th>
                        <th>CRD</th>
                    </tr>
                </thead>
                <tbody>
                    {
                        advisors.map((adv) => (
                            <AdvisorRow key={adv.idx} adv={adv} />
                        ))
                    }
                </tbody>
            </table>
        </>
    )
}

export default Advisors;