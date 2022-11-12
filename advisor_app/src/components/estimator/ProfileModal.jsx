/* eslint-disable react-hooks/exhaustive-deps */
import React, { useState, useEffect } from "react";

import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

import {
  IconGender1,
  IconDownArrow,
  IconSpouse,
  IconAddSpouse,
} from "../../assets/images";

export const ProfileModal = ({
  toggleModal,
  isModalOpen,
  gender,
  setGender,
  current_age,
  setCurrent_age,
  setPayout_age,
}) => {
  const [dropdownActive, setDropdownActive] = useState(false);

  const ageOutOfRange = () =>
    toast.warn("Please enter an age between 40 and 70 ", {
      position: "top-right",
      autoClose: 5000,
      hideProgressBar: false,
      closeOnClick: true,
      pauseOnHover: true,
      draggable: true,
      progress: undefined,
    });

  const handleGenderSelect = (e) => {
    setGender(e.target.id);
    // setPayout_age(95);
  };
  const handleSubmit = (e) => {
    e.preventDefault();
    toggleModal();
  };

  useEffect(() => {
    const timeout = setTimeout(() => {
      if (current_age < 40 || current_age > 70) {
        ageOutOfRange();
        setCurrent_age(45);
      }
    }, 500);
    return () => {
      clearTimeout(timeout);
    };
  }, [current_age]);

  const handleCancel = () => {
    toggleModal();
    setCurrent_age(45);
  };

  return (
    <div>
      <div className={`modal ${isModalOpen ? "is-active" : null}`}>
        <div className="modal-background" onClick={toggleModal}></div>
        <div className="modal-content">
          <div className="box box__container">
            <div className="content is-flex is-flex-direction-column is-justify-content-center is-align-items-center">
              <h1 className="title is-3 has-text-primary">Client Profile</h1>
              <div className="is-flex is-flex-direction-row is-justify-content-center is-align-items-center">
                <div className="card is-rounded marginSelectGender">
                  <div className="card-content cardStyleBackground">
                    <div className="has-text-centered">
                      <img
                        src={IconGender1}
                        alt="icon gender"
                        className="IconGender1"
                      />
                    </div>
                    {/* <label className="label">Select Gender</label> */}

                    <div className="has-text-centered">
                      <div
                        className={`dropdown mb-4 ${
                          dropdownActive ? "is-active" : null
                        }`}
                        onClick={() => setDropdownActive(!dropdownActive)}
                      >
                        <div className="dropdown-trigger ">
                          <button
                            className="button "
                            aria-haspopup="true"
                            aria-controls="dropdown-menu"
                          >
                            <span>
                              {gender}{" "}
                              <img
                                src={IconDownArrow}
                                alt="icon gender"
                                className="IconDownArrow"
                              />
                            </span>
                          </button>
                        </div>
                        <div
                          className="dropdown-menu dropdownSelectGender"
                          id="dropdown-menu"
                          role="menu"
                        >
                          <div className="dropdown-content">
                            <a
                              className="dropdown-item "
                              value="Male"
                              id="Male"
                              onClick={(e) => handleGenderSelect(e)}
                            >
                              Male
                            </a>
                            <a
                              className="dropdown-item"
                              value="Female"
                              id="Female"
                              onClick={(e) => handleGenderSelect(e)}
                            >
                              Female
                            </a>
                          </div>
                        </div>
                      </div>
                    </div>

                    <div className="is-flex flex-direction-row is-justify-content-center is-align-items-center">
                      <div className="field fieldSelectAge">
                        <label className="label">Age</label>
                        <div className="control">
                          <input
                            className="input"
                            type="number"
                            required
                            min="40"
                            max="70"
                            placeholder="Age"
                            value={current_age}
                            onChange={(e) =>
                              setCurrent_age(
                                e.target.value ? parseInt(e.target.value) : 0
                              )
                            }
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
                  </div>
                </div>

                <div className="card is-rounded">
                  <div className="card-content cardStyleBackground2">
                    {/* <label className="label">Select Gender</label> */}

                    <div className="has-text-centered">
                      <img
                        src={IconSpouse}
                        alt="icon gender"
                        className="IconGender1"
                      />
                    </div>

                    <div className="has-text-centered">
                      <img
                        src={IconAddSpouse}
                        alt="icon gender"
                        className="IconAddSpouse"
                      />

                      <label className="label">Add Spouse</label>
                    </div>
                  </div>
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
                <button
                  className="button is-text"
                  onClick={() => handleCancel()}
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>
        <button
          className="modal-close is-large"
          aria-label="close"
          onClick={toggleModal}
        ></button>
      </div>
    </div>
  );
};
