// function to format the tick labels k for thousands and m for millions
export const formatTickLabels = (value, index, ticks) => {
  return value > 999999
    ? `${(value / 1000000).toFixed(0)}M`
    : `${(value / 1000).toFixed(0)}K`;
};

// function for returning number with format 6,000,210
export const formatNumber = (value) => {
  return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
};

export const nFormatter = (num) => {
  if (num >= 1000000000) {
    return (num / 1000000000).toFixed(1).replace(/\.0$/, "") + "G";
  }
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1).replace(/\.0$/, "") + "M";
  }
  if (num >= 1000) {
    return (num / 1000).toFixed(1).replace(/\.0$/, "") + "K";
  }
  return num;
};
