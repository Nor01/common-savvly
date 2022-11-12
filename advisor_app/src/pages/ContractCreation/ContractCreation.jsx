import { SavvlyLogo } from "../../assets/images";
import { useState, useEffect } from "react";
import FormRouter from "../../components/ContractStepForm/FormRouter";
import useQuery from "../../hooks/useQuery";
import { FormatContractData } from "../../utils/ContractHelpers";

import { useMsal } from "@azure/msal-react";
import { useNavigate } from "react-router-dom";

import swal from "sweetalert2";

const ContractCreation = () => {
  const navigate = useNavigate();
  const [page, setPage] = useState(1);
  const { accounts } = useMsal();

  const [step, setStep] = useState(1);
  const [validations, setValidations] = useState([]);
  const [progress, setProgress] = useState(0);
  const [executeContractGeneration, setExecuteContractGeneration] =
    useState(false);

  const { query } = useQuery();
  const userid = accounts[0].idTokenClaims.oid;

  const [contractData, setContractData] = useState({
    firstname: "",
    lastname: "",
    email: "",
    address: "",
    zip_code: "",
    city: "",
    state: "",
    birthdate: "",
    sex: "",
    is_US_citizen: "",
    is_married: "N",
    is_green_card: "",
    ssn: "",
    passport_data: "",
    passport_expiration: "",
    passport_country: "US",
    country: "US",
    alien_id_or_visa: "",
    alien_id_or_visa_expiration: "",
    spouse_firstname: "",
    spouse_lastname: "",
    spouse_birthdate: "",
    spouse_sex: "",
    spouse_ssn: "",
    spouse_is_US_citizen: "",
    spouse_is_green_card: "",
    spouse_alien_id_or_visa: "",
    spouse_alien_id_or_visa_expiration: "",
    spouse_passport_expiration: "",
    spouse_passport_country: "US",
    spouse_passport_data: "",
    spouse_address: "",
    spouse_email: "",
    investment_start_date: "",
    payout_options: 0,
    payout_ages: [85],
    advisor_fee: 0,
    ETF: "VOO Vanguard",
    funding: "",
    purchaser_type: "",
  });

  const [errors, setErrors] = useState({});

  useEffect(() => {
    swal.close();
    const totalPages = contractData.is_married == "Y" ? 8 : 6;
    setProgress((page / totalPages) * 100);
  }, [page]);

  const inputChanged = (field, value) =>
    setContractData({ ...contractData, [field]: value });

  const cancel = () => {
    swal
      .fire({
        title: "Are you sure you want to cancel?",
        showDenyButton: true,
        confirmButtonText: "Yes",
        denyButtonText: `No`,
        confirmButtonColor: "#0e6e7b",
        denyButtonColor: "#737373",
      })
      .then((result) => {
        if (result.isConfirmed) {
          navigate("/");
        }
      });
  };

  const formatData = () => {
    validateConflicts();
    return FormatContractData(contractData);
  };

  const validateConflicts = () => {
    if (contractData.is_married == "N") {
      setContractData({
        ...contractData,
        spouse_firstname: "",
        spouse_lastname: "",
        spouse_birthdate: "",
        spouse_sex: "",
        spouse_ssn: "",
        spouse_is_US_citizen: "",
        spouse_is_green_card: "",
        spouse_alien_id_or_visa: "",
        spouse_alien_id_or_visa_expiration: "",
        spouse_passport_expiration: "",
        spouse_passport_country: "",
        spouse_passport_data: "",
        spouse_address: "",
        spouse_email: "",
      });
    } else {
      if (contractData.spouse_is_US_citizen === "Y") {
        setContractData({
          ...contractData,
          spouse_is_green_card: "",
          spouse_alien_id_or_visa: "",
          spouse_alien_id_or_visa_expiration: "",
          spouse_passport_data: "",
          spouse_passport_expiration: "",
          spouse_passport_country: "",
        });
      }
    }

    if (contractData.is_US_citizen === "Y") {
      setContractData({
        ...contractData,
        is_green_card: "",
        alien_id_or_visa: "",
        alien_id_or_visa_expiration: "",
        passport_data: "",
        passport_expiration: "",
        passport_country: "",
      });
    }
  };

  const saveContract = async () => {
    const data = formatData();
    
    const parameters = `userid=${userid}&email=${
      contractData.email
    }&clientinfo=${JSON.stringify(data)}`;

    swal.fire({
      title: "Generating the Contract...",
      allowEscapeKey: false,
      allowOutsideClick: false,
      didOpen: () => {
        swal.showLoading();
      },
    });

    const {
      status: apcStatus,
      response: apcResponse,
      errors: apcErrors,
    } = await query(
      `https://savvly-dev-api.azurewebsites.net/addpotentialclient?${parameters}`
    );

    console.log(apcResponse);

    if (
      !apcStatus ||
      apcResponse.proxyres == "Fail" ||
      apcResponse.result == "failed"
    ) {
      console.error(apcErrors);
      swal.fire({
        icon: "error",
        title: "Oops...",
        text: "Something went wrong!",
      });
      return;
    }
  };

  const generateContract = async () => {
    await saveContract();

    swal.fire({
      title: "Sending the Contract by Email...",
      allowEscapeKey: false,
      allowOutsideClick: false,
      didOpen: () => {
        swal.showLoading();
      },
    });

    const {
      status: scStatus,
      response: scResponse,
      errors: scErrors,
    } = await query(
      `https://savvly-dev-api.azurewebsites.net/sendcontract?userid=${userid}&email=${contractData.email}`
    );

    console.log(scResponse);

    if (!scStatus || scResponse.proxyres == "Fail") {
      console.log(scErrors);
      swal.fire({
        icon: "error",
        title: "Oops...",
        text: "Something went wrong!",
      });
      return;
    }

    swal.close();
    navigate("/contracts");
  };

  const saveContractDraft = async () => {
    swal
      .fire({
        title: "Are you sure? Contract will be saved as a Draft.",
        showDenyButton: true,
        confirmButtonText: "Yes",
        denyButtonText: `No`,
        confirmButtonColor: "#0e6e7b",
        denyButtonColor: "#737373",
      })
      .then( async (result) => {
        if (result.isConfirmed) {
          await saveContract();
          swal.fire(
            'Contract saved!',
            'You can send the contract by email later.',
            'success'
          )
          navigate("/contracts");
        }
      });
  }

  const nextStep = () => {
    if (executeContractGeneration) {
      generateContract();
    } else {
      if (validateFormPerPage()) setPage(page + 1);
    }
  };

  const prevStep = () => {
    setPage(page - 1);
  };

  const validateFormPerPage = () => {
    let errs = {};
    validations.forEach((val) => {
      const type = val.type;
      const value = contractData[val.field];

      if (type == "required" && value.toString().trim() === "")
        errs[val.field] = "This field is required.";

      if (type == "length" && value.length !== val.length)
        errs[val.field] = `This field must have ${val.length} characters.`;

      if (type == "18yo" && value.trim() !== "") {
        let birthdate = value.replace(/-/g, "/");
        birthdate = new Date(birthdate);
        const currentDate = new Date().toJSON().slice(0, 10) + " 01:00:00";
        const myAge = ~~((Date.now(currentDate) - birthdate) / 31557600000);

        if (myAge < 18) errs[val.field] = `Needs to be at least 18 years old.`;

        if (myAge > 120) errs[val.field] = `Maximum age is 120 years.`;
      }

      if (type == "max10years" && value.trim() !== "") {
        let date = value.replace(/-/g, "/");
        date = new Date(date);

        let now = new Date();
        now.setHours(0, 0, 0, 0);

        if (date < now) errs[val.field] = `Document is expired.`;

        const diffInDays = Math.round((date - now) / (1000 * 60 * 60 * 24));

        if (diffInDays > 3652)
          errs[val.field] = `Document expiration can't be more than 10 years.`;
      }

      if (type == "validEmail" && value.trim() !== "")
        if (
          !value.match(
            /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/
          )
        )
          errs[val.field] = `This email is not valid.`;
    });

    setErrors(errs);
    return Object.keys(errs).length === 0 ? true : false;
  };

  return (
    <div id="contractCreation">
      <div id="nav">
        <img src={SavvlyLogo} alt="Savvly Inc. white logo" />
        <span
          id="headerTitle"
          onClick={() => console.log({ contractData, page })}
        >
          Generate Client Contract
        </span>
      </div>
      <div id="breadcrumb">
        <div id="stepDisplay">
          <span>Step {step} of 3</span>
        </div>
        <div id="contractTabs">
          <div className={"tab " + (step == 1 ? "active" : "")}>
            Client Data
          </div>
          <div className={"tab " + (step == 2 ? "active" : "")}>
            Contract Choices
          </div>
          <div className={"tab " + (step == 3 ? "active" : "")}>Contract</div>
        </div>
      </div>
      <div className="contractCanvas has-background-light is-flex-grow-1">
        <div className="container has-background-white main-container">
          {page != 1 && <i onClick={prevStep} className="backArrow"></i>}

          <div className="content">
            <div id="currentPage">
              <FormRouter
                page={page}
                inputChanged={inputChanged}
                data={contractData}
                errors={errors}
                setStep={setStep}
                setValidations={setValidations}
                generateContract={setExecuteContractGeneration}
                formatData={formatData}
              />
            </div>

            <progress
              className="progress is-primary"
              value={progress}
              max="100"
            ></progress>
            <div className="buttons is-flex is-justify-content-space-between">
              <a href="#" onClick={cancel}>
                Cancel
              </a>

              <div className="buttons">
                { (page == 5 || page == 6) && (
                  <button
                    className="button is-primary"
                    onClick={saveContractDraft}
                  >
                    Save
                  </button>
                )}

                <button className="button is-primary" onClick={nextStep}>
                  {executeContractGeneration
                    ? "Send via email"
                    : page == 1
                    ? "Let's Get Started!"
                    : "Next"}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ContractCreation;
