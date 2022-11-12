import React, { useState, useEffect } from "react";
import { ClientProfile } from "../../components/estimator/ClientProfile";
import { Funds } from "../../components/estimator/Funds";
import { ShareEstimator } from "../../components/estimator/ShareEstimator";

import "./Estimator.css";

const Estimator = () => {
  const [planner, setPlanner] = useState({});

  const [gender, setGender] = useState("Male");
  const [current_age, setCurrent_age] = useState(45);
  const [average_return, setAverage_return] = useState(6);
  const [funding_amount, setFunding_amount] = useState(50000);
  const [payout_age, setPayout_age] = useState(75);
  const [investment, setInvestment] = useState("Lump Sum");

  const proxyUrlL = `https://simulator-dev-eastus.azurewebsites.net/simulate-prospect-planner?gender=${gender}&current_age=${current_age}&average_return=${average_return}&funding_amount=${funding_amount}&payout_age=${payout_age}`;
  const proxyUrlM = `https://savvly-dev-api.azurewebsites.net/simulate-prospect-planner?gender=${gender}&current_age=${current_age}&average_return=${average_return}&funding_amount=${funding_amount}&payout_age=75`;

  useEffect(() => {
    const fetchData = async () => {
      try {
        if (investment === "Lump Sum") {
          const response = await fetch(proxyUrlL);
          const data = await response.json();
          setPlanner(
            data.map((obj) => {
              let payoutage = obj[0];
              let info = obj[1];
              return { ...info, payoutage };
            })
          );
        } else {
          const response = await fetch(proxyUrlM);
          const data = await response.json();
          setPlanner(data.simulate);
        }
      } catch (error) {
        console.log(error);
      }
    };
    fetchData();
  }, [proxyUrlM, proxyUrlL, investment]);

  return (
    <div>
      <div className="page__container container is-flex is-flex-direction-column p-4">
        <div className="is-flex is-justify-content-space-between">
          <h1 className="title has-text-primary">Estimator</h1>
        </div>
        <hr />

        <div className="container__estimator">
          <div className="client__estimator">
            <ClientProfile
              current_age={current_age}
              setCurrent_age={setCurrent_age}
              gender={gender}
              investment={investment}
              setInvestment={setInvestment}
              setGender={setGender}
              average_return={average_return}
              setAverage_return={setAverage_return}
              funding_amount={funding_amount}
              setFunding_amount={setFunding_amount}
              setPayout_age={setPayout_age}
            />
          </div>
          <div className="share__estimator">
            <ShareEstimator />
          </div>
          <div className="funds__estimator">
            <Funds
              setPayout_age={setPayout_age}
              payout_age={payout_age}
              planner={planner}
              gender={gender}
              investment={investment}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Estimator;
