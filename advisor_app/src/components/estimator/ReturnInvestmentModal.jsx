/* eslint-disable react-hooks/exhaustive-deps */
import React, { useEffect } from "react";
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

import NumericInput from "react-numeric-input";

import { IconAverageReturn } from "../../assets/images";

export const ReturnInvestmentModal = ({
  isReturnModalOpen,
  toggleReturnModal,
  average_return,
  setAverage_return,
}) => {
  const handleSubmit = (e) => {
    e.preventDefault();
    toggleReturnModal();
  };

  const returnOutOfRange = () =>
    toast.warn("Please enter a return investment between 1-20 ", {
      position: "top-right",
      autoClose: 5000,
      hideProgressBar: false,
      closeOnClick: true,
      pauseOnHover: true,
      draggable: true,
      progress: undefined,
    });

  useEffect(() => {
    const timeout = setTimeout(() => {
      if (average_return < 1 || average_return > 20) {
        returnOutOfRange();
        setAverage_return(6);
      }
    }, 500);
    return () => {
      clearTimeout(timeout);
    };
  }, [average_return]);

  return (
    <div>
      <div className={`modal ${isReturnModalOpen ? "is-active" : null}`}>
        <div className="modal-background" onClick={toggleReturnModal}></div>

        <div className="modal-content">
          <div className="box box__container modalHeightAverageReturn">
            <div className="content is-flex is-flex-direction-column is-justify-content-center is-align-items-center">
              <h1 className="title is-3 has-text-primary">
                Return on Investment
              </h1>
              <div className="is-flex is-flex-direction-row is-justify-content-center is-align-items-center">
                <div className="card  is-rounded ">
                  
                   
                      <div className="card-content cardStyleBackground">
                        <div className="has-text-centered">
                          <img
                            src={IconAverageReturn}
                            alt="icon Average Return"
                            className="IconGender1"
                          />
                        </div>
                      </div>

                      <NumericInput
                        className="input"
                        value={average_return}
                        type="number"
                        required
                        min={1}
                        max={20}
                        step={0.5}
                        precision={1}
                        placeholder="Select Return on Investment"
                        onChange={(e) => setAverage_return(e)}
                      />
                      <ToastContainer
                        position="top-right"
                        autoClose={5000}
                        hideProgressBar={false}
                        newestOnTop={false}
                        closeOnClick
                        rtl={false}
                        pauseOnFocusLoss
                        draggable
                        pauseOnHover
                      />

                </div>
              </div>
            </div>
            <div className="field is-grouped m-3">
              <div className="control">
                <button className="button is-primary" onClick={handleSubmit}>
                  Save
                </button>
              </div>
              <div className="control">
                <button className="button is-text" onClick={toggleReturnModal}>
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
