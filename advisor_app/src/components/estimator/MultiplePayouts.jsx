import React from "react";
import { Bar } from "react-chartjs-2";
import "chartjs-plugin-datalabels";
import {
  formatTickLabels,
  nFormatter,
  formatNumber,
} from "../../utils/NumberFormater";

export const MultiplePayouts = ({ planner, investment }) => {
  const options = {
    plugins: {
      custom_canvas_background_color: {
        fullW: true,
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
        grace: "80%",
        ticks: {
          beginAtZero: false,
          callback: (value) => formatTickLabels(value),
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
        data: Object.values(planner).map((entry, index) => {
          return index === 0
            ? parseInt(entry.withoutRounded * 0.4) || 0
            : index === 1
            ? parseInt(entry.withoutRounded * 0.3) || 0
            : index === 2
            ? parseInt(entry.withoutRounded * 0.2) || 0
            : parseInt(entry.withoutRounded * 0.1) || 0;
        }),
        backgroundColor: "rgb(155,164,179)",
        fill: {
          target: "origin",
          above: "rgba(255, 0, 0, 0.3)",
        },
      },
      {
        label: "With Savvly",
        data: Object.values(planner).map((entry, index) => {
          return index === 0
            ? parseInt(entry?.withRounded * 0.4) || 0
            : index === 1
            ? parseInt(entry?.withRounded * 0.3) || 0
            : index === 2
            ? parseInt(entry?.withRounded * 0.2) || 0
            : index === 3
            ? parseInt(entry?.withRounded * 0.1) || 0
            : null;
        }),
        backgroundColor: "rgb(23,106,120)",
        padding: 30,
        fill: {
          target: "origin",
          above: "rgba(255, 0, 0, 0.3)",
        },
      },
    ],
  };

  return (
    <>
      <div className="labels__container">
        {Object.values(planner).map((entry, index) => {
          return (
            <div className="label__container" key={index}>
              <div className="card__payout">
                <p>PAYOUT</p>
                <span>
                  $
                  {index === 0
                    ? // 75
                      formatNumber(parseInt(entry.withRounded * 0.4) || 0)
                    : // 80
                    index === 1
                    ? formatNumber(parseInt(entry?.withRounded * 0.3) || 0)
                    : // 85
                    index === 2
                    ? formatNumber(parseInt(entry?.withRounded * 0.2) || 0)
                    : // 90
                    index === 3
                    ? formatNumber(parseInt(entry?.withRounded * 0.1) || 0)
                    : null}
                </span>
              </div>
            </div>
          );
        })}
      </div>
      <Bar options={options} data={data} />
      <div className="payout__age">
        <>
          <div className="payout__container is-flex is-justify-content-center is-align-items-center is-flex-direction-row pt-2 pl-6 ml-6">
            <div>
              <strong className="has-text-white">Age 75</strong>
            </div>
            <div>
              <strong className="has-text-white">Age 80</strong>
            </div>
            <div>
              <strong className="has-text-white">Age 85</strong>
            </div>
            <div>
              <strong className="has-text-white">Age 90</strong>
            </div>
          </div>
        </>
      </div>
    </>
  );
};
