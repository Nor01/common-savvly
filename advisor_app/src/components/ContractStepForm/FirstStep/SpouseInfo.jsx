import ContractDateInput from "../inputs/ContractDateInput";
import ContractRadioButtons from "../inputs/ContractRadioButtons";
import ContractTextInput from "../inputs/ContractTextInput";
import { useEffect } from "react";

const SpouseInfo = (props) => {
  const  { errors, setValidations } = props;

  useEffect(() => {
    setValidations([
      {
        field: "spouse_firstname",
        type: "required"
      },
      {
        field: "spouse_lastname",
        type: "required"
      },
      {
        field: "spouse_birthdate",
        type: "required"
      },
      {
        field: "spouse_birthdate",
        type: "18yo"
      },
      {
        field: "spouse_sex",
        type: "required"
      },
    ])
  }, []);

  return (
    <div id="spouseInfo">
      <h1 className="title has-text-centered has-text-weight-normal">
        Tell me about the spouse...
      </h1>

      <div className="columns is-multiline">
        <div className="column is-6">
          <ContractTextInput
            {...props}
            title="First Name"
            field="spouse_firstname"
            errors={errors?.spouse_firstname}
          />
        </div>
        <div className="column is-6">
          <ContractTextInput
            {...props}
            title="Last Name"
            field="spouse_lastname"
            errors={errors?.spouse_lastname}
          />
        </div>
        <div className="column is-6">
          <ContractDateInput
            {...props}
            title="Date of Birth"
            field="spouse_birthdate"
            errors={errors?.spouse_birthdate}
          />

          <ContractRadioButtons
            {...props}
            field="spouse_sex"
            title1="Male"
            title2="Female"
            value1="M"
            value2="F"
            errors={errors?.spouse_sex}
          />
        </div>
      </div>
    </div>
  );
};

export default SpouseInfo;
