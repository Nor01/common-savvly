//Formats the Client Data to avoid issues in the backend.
export const FormatContractData = (contractData) => {
    console.log(contractData);
  let data = {};
  Object.keys(contractData).forEach((f) => {
    if (contractData[f] && contractData[f] !== undefined) {
      data[f] = contractData[f];
      if (f == "funding") data[f] = data[f].toString().replaceAll(",", "");

      if (typeof data[f] === "string") data[f] = data[f].replaceAll("+", "%2B");
    }
  });

  return data;
};