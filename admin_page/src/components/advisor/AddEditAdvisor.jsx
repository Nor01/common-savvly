import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useUsers } from "../../contexts/UsersContext";
import { toast } from "react-toastify";
import Swal from "sweetalert2";

const AddEditAdvisor = () => {
  //const { id } = match.params;

  const { addAdvisor } = useUsers();
  const defaultErrors = { userId: "", crd: "", associated: "", totalErrors: 0 };
  const [errors, setErrors] = useState(defaultErrors);

  let navigate = useNavigate();

  const validateForm = ({ userId, crd, associated }) => {
    const errorsFound = defaultErrors;

    if (crd.trim() === "") {
      errorsFound.crd = "CRD is required.";
      errorsFound.totalErrors++;
    }

    if (associated.trim() === "") {
      errorsFound.associated = "Associated is required.";
      errorsFound.totalErrors++;
    }

    setErrors({ ...errors, ...errorsFound });
    return errorsFound;
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    const formValues = {
      userId: e.target.userId.value,
      crd: e.target.crd.value,
      associated: e.target.associated.value,
    };

    const errs = validateForm(formValues);
    
    if (errs.totalErrors > 0) return;

    addAdvisor(formValues)
      .then((res) => res.json())
      .then((data) => {
        if (data.proxyres == "OK") {
          navigate("/advisors");
          toast.success(e.target.userId.value + " created successfully.", {
            position: "bottom-right",
            autoClose: 3000,
            hideProgressBar: false,
            closeOnClick: true,
            pauseOnHover: true,
            draggable: true,
            progress: undefined,
            theme: "colored",
          });
        } else if (data.proxyres == "FAIL")
          Swal.fire({
            title: "Error occurred adding this user",
            icon: "error",
          });
      })
      .catch((err) => {
        console.log(err);
        Swal.fire({
          title: "Error occurred adding this user",
          icon: "error",
        });
      });
  };

  return (
    <>
      <h1 className="title">New Advisor</h1>
      <hr />
      <form onSubmit={handleSubmit}>
        <div className="columns is-multiline">
          <div className="field column is-4 py-0">
            <label className="label">User ID</label>
            <div className="control">
              <input className="input" type="text" name="userId" />
            </div>
          </div>

          <div className="field column is-4 py-0">
            <label className="label">CRD</label>
            <div className="control">
              <input
                className={"input " + (errors.crd ? "is-danger" : "")}
                type="text"
                name="crd"
              />
            </div>
            <p className="help is-danger">{errors.crd ? errors.crd : ""}</p>
          </div>

          <div className="field column is-4 py-0">
            <label className="label">Associated</label>
            <div className="control">
              <input
                className={"input " + (errors.associated ? "is-danger" : "")}
                type="text"
                name="associated"
                defaultValue={"Savvly"}
              />
            </div>
            <p className="help is-danger">
              {errors.associated ? errors.associated : ""}
            </p>
          </div>

          <div className="field is-grouped is-justify-content-flex-end column is-12">
            <p className="control">
              <button type="submit" className="button is-primary">
                Submit
              </button>
            </p>
            <p className="control">
              <Link to="/advisors" className="button is-light">
                Cancel
              </Link>
            </p>
          </div>
        </div>
      </form>
    </>
  );
};

export default AddEditAdvisor;
