import { useEffect } from "react";

const ContractConfirmation = ({ data, setStep, generateContract }) => {
  useEffect(() => {
    setStep(3);
    generateContract(false);
  }, []);

  return (
    <>
      <div className="has-text-centered">
        <h1 className="title has-text-weight-normal mb-2">
          Let's verify the information is correct.
        </h1>
        <p>Then we can generate the contract.</p>
      </div>
      <div id="dataSummary" className="mt-5">
        <div id="dsHeader" className="has-text-centered">
          Review Summary
        </div>
        <div id="dsContent">
          <div className="dsTitle">
            <span>Client Info</span>
          </div>
          <div className="fieldList">
            <div>
              <ul className="mt-0">
                <li>Investor Type:</li>
                <li>First, Last Name:</li>
                <li>Date of Birth:</li>
                <li>Gender:</li>
                <li>Marital Status:</li>
                <li>SSN:</li>
                <li>Citizenship:</li>
              </ul>
            </div>
            <div>
              <span className="mt-0">{data.purchaser_type}</span>
              <span>
                {data.firstname} {data.lastname}
              </span>
              <span>{data.birthdate}</span>
              <span>{data.sex}</span>
              <span>{data.is_married == "Y" ? "Married" : "Single"}</span>
              <span>{data.ssn}</span>
              <span>
                {data.is_US_citizen == "Y"
                  ? "U.S. Citizen"
                  : "Green Card/Visa Holder"}
              </span>
            </div>
          </div>

          {data.is_married == "Y" && (
            <>
              <div className="dsTitle">
                <span>Spouse Info</span>
              </div>
              <div className="fieldList">
                <div>
                  <ul className="mt-0">
                    <li>First, Last Name:</li>
                    <li>Date of Birth:</li>
                    <li>Gender:</li>
                    <li>SSN:</li>
                    <li>Citizenship:</li>
                  </ul>
                </div>
                <div>
                  <span className="mt-0">
                    {data.spouse_firstname} {data.spouse_lastname}
                  </span>
                  <span>{data.spouse_birthdate}</span>
                  <span>{data.spouse_sex}</span>
                  <span>{data.spouse_ssn}</span>
                  <span>
                    {data.spouse_is_US_citizen == "Y"
                      ? "U.S. Citizen"
                      : "Green Card/Visa Holder"}
                  </span>
                </div>
              </div>
            </>
          )}

          <div className="dsTitle">
            <span>Fund Choices</span>
          </div>

          <div className="fieldList">
            <div>
              <ul className="mt-0">
                <li>Payout Age:</li>
                <li>Amount to Invest:</li>
                <li>Investment Fund:</li>
              </ul>
            </div>
            <div>
              <span className="mt-0">{String(data.payout_ages)}</span>
              <span>
                {parseFloat(data.funding.replaceAll(",", "")).toLocaleString(
                  "en-US",
                  {
                    style: "currency",
                    currency: "USD",
                  }
                )}
              </span>
              <span>{data.ETF}</span>
            </div>
          </div>

          <div className="dsTitle">
            <span>Contact Info</span>
          </div>

          <div className="fieldList">
            <div>
              <ul className="mt-0">
                <li>Email Address:</li>
                {data.is_married == "Y" && <li>Spouse Email Address:</li>}
                <li>Resident Address:</li>
              </ul>
            </div>
            <div>
              <span className="mt-0">{data.email}</span>
              {data.is_married == "Y" && <span>{data.spouse_email}</span>}
              <span>{data.address}</span>
              <span>
                {data.city}, {data.state} {data.zip_code}
              </span>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default ContractConfirmation;
