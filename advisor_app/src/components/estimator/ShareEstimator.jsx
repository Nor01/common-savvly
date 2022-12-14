import React from "react";

export const ShareEstimator = () => {
  return (
    <div className="card estimator__card__container is-flex is-flex-direction-column is-justify-content-center">
      <div className="card-content ">
        <div className="subtitle ">
          <p>
            <strong className="is-size-6">SHARE INFORMATION</strong>
          </p>
        </div>
        <section className="email__input ">
          <input
            className="input is-normal "
            type="text"
            placeholder="i.e.client@email.com"
          />
        </section>

        <section className="email__btns is-flex is-flex-direction-row is-justify-content-space-between py-3">
          <button className="button is-primary is-outlined mr-1">
            <span>Share via Email</span>
          </button>
          <button className="button  is-primary is-inverted">
            <span>Download PDF</span>
          </button>
        </section>
      </div>
    </div>
  );
};
