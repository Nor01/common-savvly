import { useEffect, useState } from "react";
import PdfPreview from "../pdf/PdfPreview";
import { useMsal } from "@azure/msal-react";
import useQuery from "../../hooks/useQuery";
import { FormatContractData } from "../../utils/ContractHelpers";

import swal from "sweetalert2";

const ContractPreview = ({ contract, setSelectedContract }) => {
  const { accounts } = useMsal();
  const [pdfFile, setPdfFile] = useState();
  const { query } = useQuery();
  const userid = accounts[0].idTokenClaims.oid;

  const generatePdf = async (url) => {
    let parameters;
    if (contract.status == "Draft") {
      const clientdata = FormatContractData(contract.clientinfo);
      parameters = `userid=${userid}&email=${
        contract.email
      }&clientinfo=${JSON.stringify(clientdata)}`;
    } else {
      parameters = `userid=${userid}&contractid=${contract.contractid}`;
    }

    const { status, response, errors } = await query(
      `https://savvly-dev-api.azurewebsites.net/${url}?${parameters}`,
      true
    );

    setPdfFile("data:application/pdf;base64," + response);
  };

  const sendContract = async () => {
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
      `https://savvly-dev-api.azurewebsites.net/sendcontract?userid=${userid}&email=${contract.email}`
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

    swal.fire("Contract sent by email!", "Please check your inbox.", "success");
    setSelectedContract();
  };

  useEffect(() => {
    let url =
      contract.status == "Draft" ? "previewcontract" : "docusignretrieve";
    generatePdf(url);
  }, [contract]);

  return (
    <>
      <div className="buttons">
        <button
          className="button is-primary"
          onClick={() => setSelectedContract()}
        >
          Go Back
        </button>
        {pdfFile && contract.status == "Draft" && (
            <button className="button is-primary" onClick={sendContract}>
              Send Contract to {contract.email}
            </button>
        )}
      </div>

      <hr />

      <PdfPreview pdf={pdfFile} />
    </>
  );
};

export default ContractPreview;
