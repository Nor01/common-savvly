import BasicPersonalInfo from "./FirstStep/BasicPersonalInfo";
import ContactInfo from "./FirstStep/ContactInfo";
import SpouseSSNInfo from "./FirstStep/SpouseSSNInfo";
import SpouseInfo from "./FirstStep/SpouseInfo";
import SSNInfo from "./FirstStep/SSNInfo";

import ContractChoice from "./SecondStep/ContractChoice";
import ContractConfirmation from "./SecondStep/ContractConfirmation";
import ContractView from "./ThirdStep/ContractView";

const FormRouter = (props) => {
  const { page, data } = props;
  let steps;

  if (data.is_married === "Y")
    steps = [
      <BasicPersonalInfo {...props} />,
      <SSNInfo {...props} />,
      <SpouseInfo {...props} />,
      <SpouseSSNInfo {...props} />,
      <ContactInfo {...props} />,
      <ContractChoice {...props} />,
      <ContractConfirmation {...props} />,
      <ContractView {...props} />,
    ];
  else
    steps = [
      <BasicPersonalInfo {...props} />,
      <SSNInfo {...props} />,
      <ContactInfo {...props} />,
      <ContractChoice {...props} />,
      <ContractConfirmation {...props} />,
      <ContractView {...props} />,
    ];

  return steps[page - 1];
};

export default FormRouter;
