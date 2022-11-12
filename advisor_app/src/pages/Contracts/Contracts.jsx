import { useState, useEffect } from "react";
import { useMsal } from "@azure/msal-react";
import useQuery from "../../hooks/useQuery";
import ContractsTable from "../../components/contracts/ContractsTable";
import ContractPreview from "../../components/contracts/ContractPreview";

const Contracts = () => {
  const { accounts } = useMsal();
  const userid = accounts[0].idTokenClaims.oid;
  const [selectedContract, setSelectedContract] = useState();

  const { query } = useQuery();

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState();
  const [contracts, setContracts] = useState([]);

  useEffect(() => {
    if (!selectedContract) {
      fetchContracts();
    }
  }, [selectedContract])
  
  const fetchContracts = async () => {
    setLoading(true);
    const { status, response, errors } = await query(
      `https://savvly-dev-api.azurewebsites.net/getpotentialclients?userid=${userid}&status=%2A`
    );
    setLoading(false);
    
    if (errors)
      setError(errors);

    setContracts(response);
  }

  console.log(contracts);

  return (
    <div id="contractsPage" className="container p-4">
      {!selectedContract ? (
        <ContractsTable
          loading={loading}
          error={error}
          contracts={contracts}
          setSelectedContract={setSelectedContract}
        />
      ) : (
        <ContractPreview contract={selectedContract} setSelectedContract={setSelectedContract} />
      )}
    </div>
  );
};

export default Contracts;
