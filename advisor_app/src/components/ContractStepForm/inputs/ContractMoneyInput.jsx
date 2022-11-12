const ContractMoneyInput = ({ inputChanged, data, field, title, errors, min, max }) => {

    const handleChange = (e) => {
        let value = 0;

        if (e.target.value != "")
            value = parseFloat(e.target.value.replaceAll(/\D+/g, '')).toLocaleString();
            
        inputChanged(field, value)
    }

    return (
        <div className="field">
            <label className="contractLabel">{title}</label>
            <div className="control has-icons-left">
                <input
                    onChange={handleChange}
                    value={data[field]}
                    className={"input " + (errors ? "is-danger" : "")}
                    type="text"
                    placeholder={title}
                    minLength={min}
                    maxLength={max}
                />
                <span className="icon is-left">
                    $
                </span>
            </div>
            <span className="help is-danger">{errors}</span>
        </div>
    );
};

export default ContractMoneyInput;
