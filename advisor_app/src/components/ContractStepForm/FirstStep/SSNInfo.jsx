import ContractRadioButtons from "../inputs/ContractRadioButtons";
import ContractTextInput from "../inputs/ContractTextInput";
import ContractDateInput from "../inputs/ContractDateInput";
import {countries} from "../../../config/countries";

import { useEffect } from "react";

const SSNInfo = (props) => {
  const { data, errors, setValidations } = props;

  useEffect(() => {
    let validations = [
      {
        field: "is_US_citizen",
        type: "required",
      },
    ];

    if (data.is_US_citizen === "Y") {
      validations = [
        {
          field: "ssn",
          type: "required",
        },
      ];
    }

    if (data.is_US_citizen === "N") {
      validations = [
        {
          field: "ssn",
          type: "required",
        },
        {
          field: "is_green_card",
          type: "required",
        },
        {
          field: "alien_id_or_visa",
          type: "required",
        },
        {
          field: "alien_id_or_visa_expiration",
          type: "required",
        },
        {
          field: "alien_id_or_visa_expiration",
          type: "max10years",
        },
        {
          field: "passport_data",
          type: "required",
        },
        {
          field: "passport_expiration",
          type: "required",
        },
        {
          field: "passport_expiration",
          type: "max10years",
        },
        {
          field: "passport_country",
          type: "required",
        },
      ];
    }
    setValidations(validations);
  }, [data.is_US_citizen]);

  useEffect(() => {
    props.inputChanged("alien_id_or_visa", data.is_green_card == "Y" ? "" : data.alien_id_or_visa.replaceAll("-", ""));
  }, [data.is_green_card])
  
  return (
    <div id="ssnInfo">
      <h1 className="title has-text-centered has-text-weight-normal">
        Is the client an U.S. Citizen?
      </h1>
      <ContractRadioButtons
        {...props}
        field="is_US_citizen"
        title1="Yes"
        title2="No"
        value1="Y"
        value2="N"
        errors={errors?.is_US_citizen}
      />

      {data.is_US_citizen === "Y" && (
        <>
          <h1 className="title has-text-centered has-text-weight-normal">
            What is their Social Security Number?
          </h1>
          <ContractTextInput
            {...props}
            title="SSN"
            field="ssn"
            errors={errors?.ssn}
            mask={"ssn"}
          />
        </>
      )}
      {data.is_US_citizen === "N" && (
        <>
          <h1 className="title has-text-centered has-text-weight-normal">
            What is their resident status?
          </h1>
          <ContractRadioButtons
            {...props}
            field="is_green_card"
            title1="U.S. Permanent Resident (Green Card)"
            title2="U.S. Visa Holder"
            value1="Y"
            value2="N"
            errors={errors?.is_green_card}
          />
          <div className="columns is-multiline">
            <div className="column is-6">
              <ContractTextInput
                {...props}
                title="SSN"
                field="ssn"
                errors={errors?.ssn}
                mask={"ssn"}
              />
            </div>
            <div className="column is-6"></div>

            <div className="column is-6">
              <ContractTextInput
                {...props}
                title={
                  (data.is_green_card == "Y" ? "USCIS #" : "Visa Number")
                }
                mask={ data.is_green_card == "Y" ? "uscis" : "" }
                max={11}
                field="alien_id_or_visa"
                errors={errors?.alien_id_or_visa}
              />
            </div>
            <div className="column is-6">
              <ContractDateInput
                {...props}
                title={
                  (data.is_green_card == "Y" ? "USCIS #" : "Visa") +
                  " Expiration Date"
                }
                field="alien_id_or_visa_expiration"
                errors={errors?.alien_id_or_visa_expiration}
              />
            </div>

            <div className="column is-6">
              <ContractTextInput
                {...props}
                title="Passport Number"
                field="passport_data"
                errors={errors?.passport_data}
              />
            </div>

            <div className="column is-6">
              <ContractDateInput
                {...props}
                title="Passport Expiration Date"
                field="passport_expiration"
                errors={errors?.passport_expiration}
              />
            </div>

            <div className="column is-6">
              <div className="field">
                <label className="contractLabel">Country of Origin</label>
                <div className="control">
                  <div className="select is-fullwidth">
                    <select
                      onChange={(e) =>
                        props.inputChanged("passport_country", e.target.value)
                      }
                      value={data.passport_country}
                    >
                      {Object.keys(countries).map((country) => (
                        <option key={country} value={country}>
                          {countries[country]}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default SSNInfo;
