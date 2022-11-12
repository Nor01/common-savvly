const ContractMultipleSelect = ({inputChanged, data, title, field, value1, value2, text1, text2}) => {
  return (
    <div className="field">
      <label className="contractLabel">{title}</label>
      <div className="control">
        <div className="select is-fullwidth">
          <select
            onChange={(e) => inputChanged(field, e.target.value)}
            value={data[field]}
          >
            <option value={value1}>{text1}</option>
            <option value={value2}>{text2}</option>
          </select>
        </div>
      </div>
    </div>
  );
};

export default ContractMultipleSelect;
