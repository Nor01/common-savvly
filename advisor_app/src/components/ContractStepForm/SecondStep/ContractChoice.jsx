import ContractTextInput from "../inputs/ContractTextInput";
import ContractMoneyInput from "../inputs/ContractMoneyInput";

import { useEffect, useState } from "react";

const ContractChoice = (props) => {
  const {
    inputChanged,
    data,
    setStep,
    errors,
    setValidations,
    generateContract,
  } = props;
  const payoutAges = [];
  for (let i = 75; i <= 95; i++) payoutAges.push(i);

  useEffect(() => {
    setStep(2);
    generateContract(false);

    setValidations([
      {
        field: "funding",
        type: "required",
      },
      {
        field: "advisor_fee",
        type: "required",
      }
    ]);
  }, []);

  const handlePayoutChange = (e) => {
    data.payout_ages = e.target.value == 0 ? [85] : [80, 85, 90, 95];
    inputChanged("payout_options", e.target.value);
  };

  return (
    <>
      <h1 className="title has-text-centered has-text-weight-normal">
        Now the best part!
      </h1>
      <br />
      <div className="columns">
        <div className="column is-6">
          {/* <ContractDateInput {...props} title="Investment Start Date" field="investment_start_date" errors={errors?.investment_start_date} /> */}
          <ContractMoneyInput
            {...props}
            title="Amount To Invest"
            field="funding"
            errors={errors?.funding}
          />

          <div className="field">
            <label className="contractLabel">Investment Fund</label>
            <div className="control">
              <div className="select is-fullwidth">
                <select
                  onChange={(e) => inputChanged("ETF", e.target.value)}
                  value={data.ETF}
                >
                  <option value="VOO Vanguard">VOO Vanguard</option>
                </select>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="columns is-multiline">
        <div className="column is-6">
          <label className="contractLabel">Payout Options</label>
          <div className="control">
            <div className="select is-fullwidth">
              <select value={data.payout_options} onChange={handlePayoutChange}>
                <option value={0}>Lump Sum</option>
                <option value={1}>Multiple Payouts</option>
              </select>
            </div>
          </div>
        </div>

        <div className="column is-6">
          <div className="field">
            <label className="contractLabel">Payout Age</label>
            <div className="control">
              {data.payout_options == 0 ? (
                <div className="select is-fullwidth">
                  <select
                    onChange={(e) =>
                      inputChanged("payout_ages", [parseInt(e.target.value)])
                    }
                    value={data.payout_ages[0]}
                  >
                    {payoutAges.map((age) => (
                      <option key={age} value={age}>
                        {age}
                      </option>
                    ))}
                  </select>
                </div>
              ) : (
                <input
                  type="text"
                  className="input"
                  value={"80,85,90,95"}
                  disabled={true}
                />
              )}
            </div>
          </div>
        </div>

        <div className="column is-6">
          <ContractTextInput
            {...props}
            title="Advisor Fee"
            field="advisor_fee"
            type="number"
            max={100}
            min={0}
            errors={errors?.advisor_fee}
          />
        </div>
      </div>
    </>
  );
};

export default ContractChoice;
