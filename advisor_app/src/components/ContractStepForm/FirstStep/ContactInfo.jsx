import ContractTextInput from "../inputs/ContractTextInput";
import { useState, useEffect } from "react";
import { countries } from "../../../config/countries";

const ContactInfo = (props) => {
  const { setStep, errors, data, setValidations } = props;
  const [spouseAddressDiff, setSpouseAddressDiff] = useState();

  useEffect(() => {
    setStep(1);
  }, []);

  useEffect(() => {
    let validations = [
      {
        field: "email",
        type: "required",
      },
      {
        field: "email",
        type: "validEmail",
      },
      {
        field: "address",
        type: "required",
      },
      {
        field: "zip_code",
        type: "length",
        length: 5
      },
    ];

    if (data.is_married === "Y") {
      validations = [
        ...validations,
        {
          field: "spouse_email",
          type: "required",
        },
        {
          field: "spouse_email",
          type: "validEmail",
        }
      ];

      if (spouseAddressDiff) {
        validations = [
          ...validations,
          {
            field: "spouse_address",
            type: "required",
          },
        ];
      } else {
        props.inputChanged("spouse_address", "");
      }
    }

    setValidations(validations);
  }, [spouseAddressDiff]);

  return (
    <div id="contactInfo">
      <h1 className="title has-text-centered has-text-weight-normal">
        How we should contact the client?
      </h1>
      <br />
      <ContractTextInput
        {...props}
        title="Email Address"
        field="email"
        errors={errors?.email}
      />
      {data.is_married == "Y" && (
        <ContractTextInput
          {...props}
          title="Spouse Email Address"
          field="spouse_email"
          errors={errors?.spouse_email}
        />
      )}
      <ContractTextInput
        {...props}
        title="Resident Address"
        field="address"
        errors={errors?.address}
      />

      <div className="columns is-multiline">
        <div className="column is-4">
          <ContractTextInput
            {...props}
            title="City"
            field="city"
            errors={errors?.city}
          />
        </div>
        <div className="column is-4">
          <ContractTextInput
            {...props}
            title="State"
            field="state"
            errors={errors?.state}
          />
        </div>
        <div className="column is-4">
          <ContractTextInput
            {...props}
            title="Zip Code"
            field="zip_code"
            max={5}
            errors={errors?.zip_code}
          />
        </div>

        <div className="column is-4">
              <div className="field">
                <label className="contractLabel">Country</label>
                <div className="control">
                  <div className="select is-fullwidth">
                    <select
                      onChange={(e) =>
                        props.inputChanged("country", e.target.value)
                      }
                      value={data.country}
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



      {data.is_married == "Y" && (
        <>
          <input
            type="checkbox"
            value={spouseAddressDiff}
            onChange={(e) => setSpouseAddressDiff(e.target.checked)}
          />
          <label className="ml-2">Spouse Resident Address Different</label>
        </>
      )}

      {spouseAddressDiff && (
        <ContractTextInput
          {...props}
          title="Spouse Resident Address"
          field="spouse_address"
          errors={errors?.spouse_address}
        />
      )}
    </div>
  );
};

export default ContactInfo;
