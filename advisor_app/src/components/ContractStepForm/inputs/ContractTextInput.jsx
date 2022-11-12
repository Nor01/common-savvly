const ContractTextInput = ({inputChanged, data, field, title, errors, min, max, mask = null, type}) => {

  const handleChange = (e) => {
    let {value} = e.target;
    if (mask == "ssn") {
      value = value.replace(/\D/g, '');
      value = value.replace(/^(\d{3})/, '$1-');
      value = value.replace(/-(\d{2})/, '-$1-');
      value = value.replace(/(\d)-(\d{4}).*/, '$1-$2');
    }

    if (mask == "uscis") {
      value = value.replace(/\D/g, '');
      value = value.replace(/^(\d{3})/, '$1-');
      value = value.replace(/-(\d{3})/, '-$1-');
      value = value.replace(/(\d)-(\d{4}).*/, '$1-$2');
    }

    inputChanged(field, value);
  }
  return (
    <div className="field">
      <label className="contractLabel">{title}</label>
      <div className="control">
        <input
          onChange={handleChange}
          value={data[field]}
          className={"input " + (errors ? "is-danger" : "")}
          type={type ? type : "text"}
          placeholder={title}
          minLength={min}
          maxLength={max}
        />
      </div>
      <span className="help is-danger">{errors}</span>
    </div>
  );
};

export default ContractTextInput;
