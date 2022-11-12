const ContractDateInput = ({inputChanged, data, title, field, errors}) => {
  return (
    <div className="field">
      <label className="contractLabel">{title}</label>
      <div className="control">
        <input
          onChange={(e) => inputChanged(field, e.target.value)}
          value={data[field]}
          className={"input " + (errors ? "is-danger" : "")}
          type="date"
          max="9999-12-31"
        />
      </div>
      <span className="help is-danger">{errors}</span>
    </div>
  );
};

export default ContractDateInput;
