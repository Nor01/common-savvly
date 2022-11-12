import ContractDateInput from "../inputs/ContractDateInput";
import ContractRadioButtons from "../inputs/ContractRadioButtons";
import ContractTextInput from "../inputs/ContractTextInput";
import { useEffect } from "react";
import { countries } from "../../../config/countries";

const SpouseSSNInfo = (props) => {
  const { data, errors, setValidations } = props;

  useEffect(() => {
    let validations = [
      {
        field: "spouse_is_US_citizen",
        type: "required",
      },
    ];

    if (data.spouse_is_US_citizen === "Y") {
      validations = [
        {
          field: "spouse_ssn",
          type: "required",
        },
      ];
    }

    if (data.spouse_is_US_citizen === "N") {
      validations = [
        {
          field: "spouse_ssn",
          type: "required",
        },
        {
          field: "spouse_is_green_card",
          type: "required",
        },
        {
          field: "spouse_alien_id_or_visa",
          type: "required",
        },
        {
          field: "spouse_alien_id_or_visa_expiration",
          type: "required",
        },
        {
          field: "spouse_alien_id_or_visa_expiration",
          type: "max10years",
        },
        {
          field: "spouse_passport_data",
          type: "required",
        },
        {
          field: "spouse_passport_expiration",
          type: "required",
        },
        {
          field: "spouse_passport_expiration",
          type: "max10years",
        },
        {
          field: "spouse_passport_country",
          type: "required",
        },
      ];
    }
    setValidations(validations);
  }, [data.spouse_is_US_citizen]);

  useEffect(() => {
    props.inputChanged("spouse_alien_id_or_visa", data.spouse_is_green_card == "Y" ? "": data.spouse_alien_id_or_visa.replaceAll("-", ""));
  }, [data.spouse_is_green_card])

  return (
    <div id="spouseSsnInfo">
      <h1 className="title has-text-centered has-text-weight-normal">
        Is the spouse an U.S. Citizen?
      </h1>
      <ContractRadioButtons
        {...props}
        field="spouse_is_US_citizen"
        title1="Yes"
        title2="No"
        value1="Y"
        value2="N"
        errors={errors?.spouse_is_US_citizen}
      />

      {data.spouse_is_US_citizen === "Y" && (
        <>
          <h1 className="title has-text-centered has-text-weight-normal">
            What is their Social Security Number?
          </h1>
          <ContractTextInput
            {...props}
            title="SSN"
            field="spouse_ssn"
            errors={errors?.spouse_ssn}
            mask={"ssn"}
          />
        </>
      )}
      {data.spouse_is_US_citizen === "N" && (
        <>
          <h1 className="title has-text-centered has-text-weight-normal">
            What is their resident status?
          </h1>
          <ContractRadioButtons
            {...props}
            field="spouse_is_green_card"
            title1="U.S. Permanent Resident (Green Card)"
            title2="U.S. Visa Holder"
            value1="Y"
            value2="N"
            errors={errors?.spouse_is_green_card}
          />
          <div className="columns is-multiline">
            <div className="column is-6">
              <ContractTextInput
                {...props}
                title="SSN"
                field="spouse_ssn"
                errors={errors?.spouse_ssn}
                mask={"ssn"}
              />
            </div>
            <div className="column is-6"></div>

            <div className="column is-6">
              <ContractTextInput
                {...props}
                title={
                  data.spouse_is_green_card == "Y" ? "USCIS #" : "Visa Number"
                }
                max={11}
                field="spouse_alien_id_or_visa"
                mask={ data.is_green_card == "Y" ? "uscis" : "" }
                errors={errors?.spouse_alien_id_or_visa}
              />
            </div>
            <div className="column is-6">
              <ContractDateInput
                {...props}
                title={
                  (data.spouse_is_green_card == "Y" ? "USCIS #" : "Visa") +
                  " Expiration Date"
                }
                field="spouse_alien_id_or_visa_expiration"
                errors={errors?.spouse_alien_id_or_visa_expiration}
              />
            </div>

            <div className="column is-6">
              <ContractTextInput
                {...props}
                title="Passport Number"
                field="spouse_passport_data"
                errors={errors?.spouse_passport_data}
              />
            </div>

            <div className="column is-6">
              <ContractDateInput
                {...props}
                title="Passport Expiration Date"
                field="spouse_passport_expiration"
                errors={errors?.spouse_passport_expiration}
              />
            </div>

            <div className="column is-6">
              <div className="field">
                <label className="contractLabel">Country of Origin</label>
                <div className="control">
                  <div className="select is-fullwidth">
                    <select
                      onChange={(e) =>
                        props.inputChanged("spouse_passport_country", e.target.value)
                      }
                      value={data.spouse_passport_country}
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

export default SpouseSSNInfo;
