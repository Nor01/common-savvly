const RegisterFormInput = ({ label, placeholder, name, errors }) => {
  return (
    <div className="field">
      <label className="label">{label}</label>
      <div className="control">
        <input
          className={"input " + (errors ? "is-danger" : "")}
          type="text"
          placeholder={placeholder}
          name={name}
        />
      </div>
      <p className="help is-danger">{errors}</p>
    </div>
  );
};

export default RegisterFormInput;

/* <div className="field">
    <div className="control is-expanded">
    <label className="label">First Name</label>
    <input
        className={"input " + (errors.firstname ? "is-danger" : "")}
        type="text"
        placeholder="i.e. John"
        name="firstname"
    />
    </div>
    <p class="help is-danger">{errors?.firstname}</p>
    </div> */
