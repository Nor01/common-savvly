import ContractDateInput from "../inputs/ContractDateInput";
import ContractTextInput from "../inputs/ContractTextInput";

import { useEffect } from "react";
import ContractRadioButtons from "../inputs/ContractRadioButtons";
import ContractMultipleSelect from "../inputs/ContractMultipleSelect";

const BasicPersonalInfo = (props) => {
  const { data, errors, setValidations } = props;

  useEffect(() => {
    setValidations([
      {
        field: "purchaser_type",
        type: "required",
      },
      {
        field: "firstname",
        type: "required",
      },
      {
        field: "lastname",
        type: "required",
      },
      {
        field: "sex",
        type: "required",
      },
      {
        field: "birthdate",
        type: "required",
      },
      {
        field: "birthdate",
        type: "18yo",
      },
    ]);
  }, []);

  return (
    <div id="basicPersonalInfo">
      <h1 className="title has-text-centered has-text-weight-normal">
        Create a contract in less than 5 minutes!
        <br />
        Tell me about the client.
      </h1>

      <div className="is-flex is-justify-content-center is-flex-direction-column is-align-items-center">
        <ContractRadioButtons
          {...props}
          field="purchaser_type"
          title1="Qualified Purchaser"
          title2="Accredited Investor"
          value1="Qualified Purchaser"
          value2="Accredited Investor"
          errors={errors?.purchaser_type}
        />
      </div>

      {data.purchaser_type && (
        <>
          <div className="columns is-multiline mt-4">
            <div className="column is-6">
              <ContractTextInput
                {...props}
                title="First Name"
                field="firstname"
                errors={errors?.firstname}
              />
            </div>
            <div className="column is-6">
              <ContractTextInput
                {...props}
                title="Last Name"
                field="lastname"
                errors={errors?.lastname}
              />
            </div>
            <div className="column is-6">
              <ContractDateInput
                {...props}
                title="Date of Birth"
                field="birthdate"
                errors={errors?.birthdate}
              />
              <div className="mt-4">
                <ContractRadioButtons
                  {...props}
                  field="sex"
                  title1="Male"
                  title2="Female"
                  value1="M"
                  value2="F"
                  errors={errors?.sex}
                />
              </div>
            </div>
          </div>
          <div className="columns">
            <div className="column is-6">
              <ContractMultipleSelect
                {...props}
                title="Marital Status"
                field="is_married"
                text1="Single"
                value1="N"
                text2="Married"
                value2="Y"
                errors={errors?.is_married}
              />
            </div>
            <div className="column is-6">
              {/* <div className="field">
                <label className="contractLabel">Purchasing As</label>
                <div className="control">
                  <div className="select is-fullwidth">
                    <select>
                      <option>Single's Purchaser</option>
                      <option>Couple's Purchaser</option>
                    </select>
                  </div>
                </div>
              </div> */}
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default BasicPersonalInfo;
