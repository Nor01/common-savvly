import { useEffect } from "react";
import { useUsers } from "../../contexts/UsersContext";

const Admins = () => {
    
    const { admins, getAdmins } = useUsers();

    useEffect(() => {
        getAdmins();
    }, []);

    return (
        <>
            <p className="title">Admins</p>

            <table className="table is-fullwidth is-hoverable">
                <thead>
                    <tr>
                        <th>ID</th>
                    </tr>
                </thead>
                <tbody>
                    {
                        admins.map( (admin) => (
                            <tr>
                                <td>{admin}</td>
                            </tr>
                        ))
                    }
                </tbody>
            </table>
        </>
    )
}

export default Admins;