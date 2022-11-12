import { useEffect, useState } from "react";
import useQuery from "../../../hooks/useQuery";
import { useMsal } from "@azure/msal-react";
import PdfPreview from "../../pdf/PdfPreview";

const ContractView = ({ generateContract, formatData, data }) => {
  const [pdfFile, setPdfFile] = useState();
  const { accounts } = useMsal();
  const { query } = useQuery();

  useEffect(() => {
    generateContract(true);
    generatePdf();
  }, []);

  const generatePdf = async () => {
    const clientinfo = formatData();

    const userid = accounts[0].idTokenClaims.oid;
    const parameters = `userid=${userid}&email=${
      data.email
    }&clientinfo=${JSON.stringify(clientinfo)}`;

    const { status, response, errors } = await query(
      `https://savvly-dev-api.azurewebsites.net/previewcontract?${parameters}`,
      true
    );

    setPdfFile("data:application/pdf;base64," + response);
  };

  return <PdfPreview pdf={pdfFile} />;
};

export default ContractView;
