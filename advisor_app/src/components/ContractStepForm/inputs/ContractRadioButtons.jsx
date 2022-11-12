const ContractRadioButtons = ({
  inputChanged,
  data,
  field,
  title1,
  title2,
  value1,
  value2,
  errors,
}) => {
  return (
    <>
      <div className="control">
        <label className="radio">
          <input
            type="radio"
            name={field}
            onChange={(e) => inputChanged(field, e.target.value)}
            value={value1}
            checked={data[field] === value1}
          />
          {title1}
        </label>
        <label className="radio">
          <input
            type="radio"
            name={field}
            onChange={(e) => inputChanged(field, e.target.value)}
            value={value2}
            checked={data[field] === value2}
          />
          {title2}
        </label>
      </div>
      <span className="help is-danger">{errors}</span>
    </>
  );
};

export default ContractRadioButtons;
