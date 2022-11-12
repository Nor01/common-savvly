import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useUsers } from "../../contexts/UsersContext";
import { toast } from 'react-toastify';
import Swal from 'sweetalert2';

const AddEditClient = () => {
    //const { id } = match.params;

    const { addClient } = useUsers();
    const defaultErrors = { userId: null, social: null, dob: null, address: null, sex: null, mother: null, totalErrors: 0 };
    const [errors, setErrors] = useState(defaultErrors);

    let navigate = useNavigate();

    const validateForm = ({ userId, social, dob, address, sex, mother }) => {

        const errorsFound = defaultErrors;

        if (social.length < 4) {
            errorsFound.social = "Social Security Number should be at least 4 characters long.";
            errorsFound.totalErrors++;
        }

        if (address.trim() === "") {
            errorsFound.address = "Address is required.";
            errorsFound.totalErrors++;
        }

        if (mother.trim() === "") {
            errorsFound.mother = "Mother name is required.";
            errorsFound.totalErrors++;
        }

        if (dob.trim() === "") {
            errorsFound.dob = "Day of Birth is required.";
            errorsFound.totalErrors++;
        }

        setErrors({ ...errors, ...errorsFound });
        return errorsFound;
    }

    const handleSubmit = (e) => {
        e.preventDefault();

        const formValues = {
            userId: e.target.userId.value,
            social: e.target.social.value,
            dob: e.target.dob.value,
            address: e.target.address.value,
            sex: e.target.sex.value,
            mother: e.target.mother.value
        }

        const errs = validateForm(formValues);

        if (errs.totalErrors > 0 )
            return;

        addClient(formValues)
            .then((res) => res.json())
            .then((data) => {
                if (data.proxyres == "OK") {
                    navigate("/clients");
                    toast.success(e.target.userId.value + ' created successfully.', {
                        position: "bottom-right",
                        autoClose: 3000,
                        hideProgressBar: false,
                        closeOnClick: true,
                        pauseOnHover: true,
                        draggable: true,
                        progress: undefined,
                        theme: "colored"
                    });
                } else if (data.proxyres == "FAIL")
                    Swal.fire({
                        title: "Error occurred adding this user",
                        icon: "error",
                    })
            })
            .catch((err) => {
                console.log(err);
                Swal.fire({
                    title: "Error occurred adding this user",
                    icon: "error",
                })
            });
    }

    return (
        <>
            <h1 className="title">New Client</h1>
            <hr />
            <form onSubmit={handleSubmit}>
                <div className="columns is-multiline">
                    <div className="field column is-3 py-0">
                        <label className="label">User ID</label>
                        <div className="control">
                            <input className="input" type="text" name="userId" />
                        </div>
                    </div>

                    <div className="field column is-3 py-0">
                        <label className="label">Social Number</label>
                        <div className="control">
                            <input className={"input " + (errors.social ? "is-danger" : "")} type="text" name="social" />
                        </div>
                        <p className="help is-danger">{(errors.social ? errors.social : "")}</p>
                    </div>

                    <div className="field column is-3 py-0">
                        <label className="label">Gender</label>
                        <div className="control">
                            <div className="select is-fullwidth">
                                <select name="sex">
                                    <option value="M">Male</option>
                                    <option value="F">Female</option>
                                </select>
                            </div>
                        </div>
                    </div>

                    <div className="field column is-3 py-0" >
                        <label className="label">Birthday</label>
                        <input type="date" className="datepicker" name="dob" />
                        <p className="help is-danger">{(errors.dob ? errors.dob : "")}</p>
                    </div>

                    <div className="field column is-8 py-0">
                        <label className="label">Address</label>
                        <div className="control">
                            <input className={"input " + (errors.address ? "is-danger" : "")} type="text" name="address" />
                        </div>
                        <p className="help is-danger">{(errors.address ? errors.address : "")}</p>
                    </div>

                    <div className="field column is-4 py-0">
                        <label className="label">Mother Name</label>
                        <div className="control">
                            <input className={"input " + (errors.mother ? "is-danger" : "")} type="text" name="mother" />
                        </div>
                        <p className="help is-danger">{(errors.mother ? errors.mother : "")}</p>
                    </div>

                    <div className="field is-grouped is-justify-content-flex-end column is-12">
                        <p className="control">
                            <button type="submit" className="button is-primary">Submit</button>
                        </p>
                        <p className="control">
                            <Link to="/clients" className="button is-light">Cancel</Link>
                        </p>
                    </div>
                </div>
            </form>
        </>
    )
}

export default AddEditClient;