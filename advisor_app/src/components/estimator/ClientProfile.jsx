import React, { useState } from "react";
import Slider from "react-input-slider";
import { ProfileModal } from "./ProfileModal";
import { ReturnInvestmentModal } from "./ReturnInvestmentModal";
import {
  IconInfoEstimator,
  IconLumpSumWhite,
  IconLumpSumBlack,
  IconMultiplePayoutsWhite,
  IconMultiplePayoutsBlack,
} from "../../assets/images";

export const ClientProfile = ({
  setFunding_amount,
  gender,
  current_age,
  average_return,
  setGender,
  setAverage_return,
  setCurrent_age,
  setInvestment,
  investment,
  setPayout_age,
}) => {
  const [state, setState] = useState({ x: 50 });

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isReturnModalOpen, setIsReturnModalOpen] = useState(false);

  const toggleModal = () => {
    setIsModalOpen(!isModalOpen);
  };
  const toggleReturnModal = () => {
    setIsReturnModalOpen(!isReturnModalOpen);
  };

  const handleClick = (e) => {
    e.preventDefault();

    setInvestment(e.target.id);
  };

  const handleSliderChange = (x) => {
    setState((state) => ({ ...state, x }));
    setFunding_amount(x * 1000);
  };

  return (
    <div>
      <div className="card is-flex is-justify-content-center">
        <div className="card-content">
          <section className="client__profile">
            <strong className="is-size-6 ">CLIENT PROFILE</strong>
            <p className="is-size-7 genderSelect mt-2">
              <strong className="strongGenderSelect pl-2">
                Single: {gender}, Age {current_age}
                <a
                  href="#"
                  className="has-text-primary pl-2 is-underlined"
                  onClick={() => {
                    toggleModal();
                  }}
                  style={{ cursor: "pointer" }}
                >
                  <span>Edit</span>
                </a>
              </strong>
            </p>
          </section>

          <section className="investment__details">
            <div className="pt-4 pb-2">
              <p>
                <strong className="is-size-6">INVESTMENT DETAILS</strong>
              </p>
            </div>
            <div className="investment__details is-flex tabs is-toggle is-flex is-justify-content-center">
              <ul className="tab__list">
                <li
                  className={`t ${
                    investment === "Lump Sum" ? "is-active" : null
                  }`}
                  id="lump"
                >
                  <a onClick={(e) => handleClick(e)} id="Lump Sum">
                    <span id="Lump Sum">
                      <img
                        src={
                          investment === "Lump Sum"
                            ? IconLumpSumWhite
                            : IconLumpSumBlack
                        }
                        alt="icon lump sum"
                        className="IconLumpSum"
                      />
                      Lump Sum
                    </span>
                  </a>
                </li>
                <li
                  className={
                    investment === "Multiple Payouts" ? "is-active" : null
                  }
                >
                  <a onClick={(e) => handleClick(e)} id="Multiple Payouts">
                    <span id="Multiple Payouts">
                      <img
                        src={
                          investment === "Multiple Payouts"
                            ? IconMultiplePayoutsWhite
                            : IconMultiplePayoutsBlack
                        }
                        alt="icon multiple payouts"
                        className="IconMultiplePayouts"
                      />
                      Multiple Payouts
                    </span>
                  </a>
                </li>
              </ul>
            </div>
            <div className="is-size-7 py-0 has-text-grey infoEstimatorDiv">
              <img
                src={IconInfoEstimator}
                alt="icon info estimator"
                className="IconInfoEstimator"
              />
              <p>
                Client will be paid a single page large amount upon
                <br />
                reaching the Payout Age.
              </p>
            </div>
          </section>

          <section className="investment__amount">
            <div className="subtitle pt-2">
              <p>
                <strong className="is-size-6">INVESTMENT AMOUNT</strong>
              </p>
              <div className="slidecontainer pt-1">
                <Slider
                  styles={{
                    track: {
                      backgroundColor: "#dedede",
                      height: "4px",
                      width: "100%",
                    },
                    active: {
                      backgroundColor: "#0e6e7b",
                    },
                    thumb: {
                      width: 30,
                      height: 30,
                      border: "2px solid #0e6e7b",
                    },
                    disabled: {
                      opacity: 0.5,
                    },
                  }}
                  xmin={10}
                  xmax={300}
                  axis="x"
                  xstep={10}
                  x={state.x}
                  onChange={({ x }) => handleSliderChange(x)}
                />
              </div>
            </div>
            <div className="is-flex is-flex-direction-row is-justify-content-space-between ">
              <div className="is-size-7">
                <p>
                  <strong className="has-text-grey">$10K</strong>
                </p>
              </div>
              <div className="is-size-7 ">
                <p>
                  <strong className="has-text-grey">$300K</strong>
                </p>
              </div>
            </div>
            <div className="subtitle is-flex is-justify-content-center">
              <p>
                <strong className="is-size-4 has-text-primary">
                  ${state.x}K
                </strong>
              </p>
            </div>
          </section>

          <section className="investment__return pt-1 pb-3 is-flex is-justify-content-center">
            <p className="is-size-7 averageReturnSelect">
              <strong>
                Est. {average_return}% Return on Investment
                <a
                  className="has-text-primary pl-2"
                  onClick={() => {
                    toggleReturnModal();
                  }}
                >
                  <span className="is-underlined">Edit</span>
                </a>
              </strong>
            </p>
          </section>
        </div>
      </div>
      {isModalOpen && (
        <ProfileModal
          isModalOpen={isModalOpen}
          toggleModal={toggleModal}
          gender={gender}
          setGender={setGender}
          current_age={current_age}
          setCurrent_age={setCurrent_age}
          setPayout_age={setPayout_age}
        />
      )}
      {isReturnModalOpen && (
        <ReturnInvestmentModal
          isReturnModalOpen={isReturnModalOpen}
          toggleReturnModal={toggleReturnModal}
          average_return={average_return}
          setAverage_return={setAverage_return}
        />
      )}
    </div>
  );
};
