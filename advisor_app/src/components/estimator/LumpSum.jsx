import React from "react";

import { Bar } from "react-chartjs-2";
import "chartjs-plugin-datalabels";
import { nFormatter, formatNumber } from "../../utils/NumberFormater";
export const LumpSum = ({ planner, gender, payout_age, handleChange }) => {
  const options = {
    plugins: {
      custom_canvas_background_color: {
        fullW: false,
      },
      legend: {
        position: "top",
        align: "start",
        boxHeight: 60,
        usePointStyle: true,
        pointStyle: "circle",

        labels: {
          usePointStyle: true,
          padding: 40,
        },
      },
      datalabels: {
        display: true,
        color: "black",
        anchor: "end",
        align: "end",
        formatter: (value, context) => {
          return "$ " + nFormatter(parseInt(value)).toLocaleString("en-US");
        },
        padding: 0,
        clip: true,
        font: {
          size: "13",
          weight: "bold",
        },
      },
    },
    responsive: true,
    maintainAspectRatio: true,
    scales: {
      y: {
        display: true,
        grace: "15%",
        ticks: {
          beginAtZero: false,
          callback: (value) => nFormatter(value),
          // stepSize: 0.5,
        },
        grid:{
          color:"transparent"
        }
      },
      x: {
        display: true,
        grid: {
          display: false,
        },
      },
    },
  };
  var data = {
    labels: ["", "", "", ""],

    datasets: [
      {
        label: "Index Funds Alone",
        data: Object.values(planner).map((entry) => {
          return parseInt(entry?.withoutRounded) || 0;
        }),
        backgroundColor: "rgb(155,164,179)",
        fill: {
          target: "origin",
          above: "rgba(255, 0, 0, 0.3)",
        },
      },
      {
        label: "With Savvly",
        data: Object.values(planner).map((entry) => {
          return parseInt(entry?.withRounded) || 0;
        }),
        backgroundColor: "rgb(23,106,120)",
      },
    ],
  };
  return (
    <>
      <div className="labels__container is-justify-content-flex-start ml-6 mt-6">
        {Object.values(planner).map((entry, index) => {
          return index === 0 ? (
            <div className="label__container " key={index}>
              <div className="card__payout ml-3" style={{ width: "165px" }}>
                <p>LUMP SUM PAYOUT</p>
                <span>${formatNumber(parseInt(entry?.withRounded) || 0)}</span>
              </div>
            </div>
          ) : null;
        })}
      </div>
      <Bar options={options} data={data} />
      <div className="payout__age multiple-payout__age  is-flex is-flex-direction-row is-align-content-center">
        <>
          <div className="payout__age payout__age-lump">
            {Object.values(planner).map((entry, index) => {
              return index === 0 ? (
                <div
                  className="is-flex is-flex-direction-row is-align-item-center is-text-align-center"
                  key={index}
                >
                  <strong className="pt-2 pr-3 is-text-align-center">
                    Custom Age
                  </strong>
                  <input
                    className="input is-primary payout__age__input"
                    type="number"
                    required
                    min={gender === "Male" ? 70 : 75}
                    max={gender === "Male" ? 90 : 95}
                    value={payout_age}
                    onChange={(e) => handleChange(e)}
                  />
                </div>
              ) : (
                <div className="label__container" key={index}>
                  <div
                    className="card__payout-age "
                    style={{
                      backgroundColor: "rgb(23,106,120)",
                      color: "white",
                    }}
                  >
                    <span>Age {entry?.payout_age}</span>
                  </div>
                </div>
              );
            })}
          </div>
        </>
      </div>
    </>
  );
};
