import React, { useEffect } from "react";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import ChartDataLabels from "chartjs-plugin-datalabels";

import { LumpSum } from "./LumpSum";
import { MultiplePayouts } from "./MultiplePayouts";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ChartDataLabels
);
const plugin = {
  id: "custom_canvas_background_color",
  beforeDatasetsDraw: (chart, args, options) => {
    const {
      ctx,
      chartArea: { top, width, height },
      scales: { x },
    } = chart;

    ctx.save();
    ctx.globalCompositeOperation = "destination-over";
    ctx.fillStyle = "rgba(251,245,181, 0.6)";

    const newWidth = x._gridLineItems[1].x1 - x._gridLineItems[0].x1 - 10;

    if (options.fullW) {
      ctx.fillRect(x._gridLineItems[0].x1, top, newWidth, height);
      ctx.fillRect(x._gridLineItems[1].x1, top, newWidth, height);
      ctx.fillRect(x._gridLineItems[2].x1, top, newWidth, height);
      ctx.fillRect(x._gridLineItems[3].x1, top, newWidth, height);
    } else {
      ctx.fillRect(x._gridLineItems[0].x1, top, newWidth, height);
    }
    ctx.restore();
  },
};
ChartJS.register(plugin);
export const Funds = ({
  setPayout_age,
  payout_age,
  planner,
  gender,
  investment,
}) => {
  const handleChange = (e) => {
    const age = parseInt(e.target.value);
    setPayout_age(age ? age : 0);
  };

  useEffect(() => {
    const timeout = setTimeout(() => {
      if (gender === "Male" && payout_age >= 70 && payout_age <= 90) {
      } else if (gender === "Male") {
        toast.warn(
          `Please enter a payout age between 70 and 90 for ${gender}`,
          {
            position: "top-right",
            autoClose: 5000,
            hideProgressBar: false,
            closeOnClick: true,
            pauseOnHover: true,
            draggable: true,
            progress: undefined,
          }
        );
        setPayout_age(75);
      }
      if (gender === "Female" && payout_age >= 75 && payout_age <= 95) {
      } else if (gender === "Female") {
        toast.warn(
          `Please enter a payout age between 75 and 95 for ${gender}`,
          {
            position: "top-right",
            autoClose: 5000,
            hideProgressBar: false,
            closeOnClick: true,
            pauseOnHover: true,
            draggable: true,
            progress: undefined,
          }
        );

        setPayout_age(75);
      }
    }, 500);
    return () => {
      clearTimeout(timeout);
    };
  }, [payout_age, gender, setPayout_age]);

  return (
    <div className="estimator__card__container ">
      <div className="card estimator__card__container">
        <div className="card-content is-flex is-flex-direction-column is-relative	">
          {investment === "Lump Sum" ? (
            <LumpSum
              planner={planner}
              gender={gender}
              setPayout_age={setPayout_age}
              handleChange={handleChange}
              payout_age={payout_age}
            />
          ) : (
            <MultiplePayouts planner={planner} gender={gender} />
          )}
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
  );
};
